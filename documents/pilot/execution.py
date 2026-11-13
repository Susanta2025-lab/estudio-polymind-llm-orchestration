"""Pilot bounds wrap, rather than replace, governed execution and settlement."""

from uuid import uuid4

from documents.jobs.models import canonical
from documents.pilot.models import PilotError
from governance.execution import GovernedExecution, RestrictedProvider
from llm.admission import CallIdentity
from llm.inference import ModelRole


class SerialAdmission:
    """An exclusive request in the same quota authority, without new capacity."""

    def __init__(self, shared, control, session, owner):
        self.shared = shared
        self.control, self.session, self.owner = control, session, owner

    def acquire(self, identity, estimated_input, reserved_output, workload):
        # Linearize admission against the pilot stop acknowledgment. This short
        # guard never spans provider execution or financial settlement.
        with self.control.transaction() as db:
            self.control.get(db, self.session, self.owner, execution=True)
            return self.shared.acquire(
                identity, estimated_input, reserved_output, workload, exclusive=True
            )

    def finish(self, *args, **kwargs):
        return self.shared.finish(*args, **kwargs)


class PilotExecution:
    def __init__(self, pilot, principal, session, governed):
        self.pilot, self.principal, self.session = pilot, principal, session
        self.governed = governed
        self.governed.admission = SerialAdmission(
            pilot.admission, pilot.control, session, principal.scope.identity()
        )
        # ManagedDigestionHandler checks this same owner/document snapshot.
        self.authority, self.snapshot = governed.authority, governed.snapshot

    def execute(
        self,
        request,
        *,
        identity=None,
        check_active=lambda: None,
        workload="INTERACTIVE",
    ):
        p, principal = self.pilot, self.principal
        row = p._session(principal, self.session, execution=True)
        kind = "synthesis" if workload == "DOCUMENT_BACKGROUND" else "question"
        if identity is None:
            identity = CallIdentity(
                principal.scope.identity(),
                uuid4(),
                uuid4(),
                1,
                "interactive/1",
                p.provider.name,
                request.role.value,
                p.provider.model_id(request.role),
                request.capability.version,
            )
        estimate = len(
            canonical(
                {
                    "system": request.system,
                    "data": request.data,
                    "schema": request.schema,
                }
            ).encode()
        )
        if (
            identity.scope != principal.scope.identity()
            or identity.attempt != 1
            or identity.provider != p.provider.name
            or identity.model != p.provider.model_id(request.role)
            or identity.capability != request.capability.version
            or request.capability
            != (
                p.managed_settings.capability
                if kind == "synthesis"
                else p.analysis_capability
            )
            or identity.role != request.role.value
            or (kind == "synthesis" and str(identity.job) != row["data"].get("job"))
            or request.output_tokens > p.policy.max_output
            or estimate
            + request.capability.overhead_tokens
            + request.capability.safety_tokens
            > p.policy.max_input
            or request.total_seconds > p.policy.provider_seconds
            or (kind == "question" and request.role != ModelRole.GENERAL)
        ):
            raise PilotError()
        if kind == "synthesis":
            job = p.jobs.get_job(principal.scope, identity.job)
            steps = p.jobs.steps(principal.scope, identity.job)
            if (
                not any(
                    s.step_id == identity.step
                    and s.state == "RUNNING"
                    and s.attempt_count == identity.attempt
                    for s in steps
                )
                or job.cancel_requested
            ):
                raise PilotError()
        p.execution_permission(principal, row["approval"], row["source"], request)
        # No financial reservation exists yet. This durable intent serializes
        # pilot calls, caps attempts and blocks ambiguous crash recovery.
        operation = identity.step
        p.control.begin(self.session, principal.scope.identity(), operation, kind)

        def active():
            p._session(principal, self.session, execution=True)
            p.execution_permission(principal, row["approval"], row["source"], request)
            check_active()

        uncertain = True
        try:
            result = self.governed.execute(
                request, identity=identity, workload=workload, check_active=active
            )
            uncertain = (
                result.usage is None
                or result.usage.prompt_tokens is None
                or result.usage.completion_tokens is None
            )
            active()  # Stop after in-flight work prevents acceptance/presentation.
            return result
        except BaseException:
            # Settlement is authoritative. Never infer zero usage from an error.
            with p.governance.transaction() as db:
                rows = list(
                    db.execute(
                        "SELECT state FROM reservations WHERE tenant=? AND owner=? AND identity_key=?",
                        (
                            str(principal.scope.tenant),
                            str(principal.scope.owner),
                            canonical(
                                [
                                    str(identity.job),
                                    str(identity.step),
                                    identity.attempt,
                                ]
                            ),
                        ),
                    )
                )
            uncertain = any(r["state"] not in {"SETTLED", "RELEASED"} for r in rows)
            raise
        finally:
            p.control.finish(operation, uncertain=uncertain)


class PilotProvider(RestrictedProvider):
    """AuthorizedAnalysis retains its normal ownership/governance binding path."""

    def __init__(self, pilot, principal, session):
        super().__init__(pilot.provider)
        self.pilot, self.principal, self.session = pilot, principal, session

    def bind(self, admission, ledger, authority, snapshot):
        p = self.pilot
        if (
            admission is not p.admission
            or ledger is not p.governance
            or authority is not p.authority
        ):
            raise PilotError()
        return PilotExecution(
            p,
            self.principal,
            self.session,
            GovernedExecution(p.provider, admission, ledger, authority, snapshot),
        )


def fixture_execution_only(principal, approval, source, request):
    """Default permission never authorizes external/paid execution.

    A trusted composition must also supply an explicitly marked deterministic
    provider. Future paid composition needs its independent authorization hook;
    no credentials, signed approval consumption or provider factory exists here.
    """
    if approval.mode != "synthetic":
        raise PilotError()
