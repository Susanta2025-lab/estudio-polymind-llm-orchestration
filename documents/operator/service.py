"""Authenticated, enrolled owning operator over the existing supervised facade."""
import threading
import time
from decimal import Decimal
from contextlib import contextmanager
from uuid import UUID, uuid4

from documents.jobs.service import DocumentJobs
from documents.pilot.models import PilotError
from security.models import SecurityError
from security.services import AuthorizedJobs


class OperatorWorkflow:
    def __init__(self, pilot, actions, enrollment, catalog, approvals, *,
                 synthetic=True, execution_enabled=True):
        if not synthetic and execution_enabled:
            from security.execution import DocumentsExecutionPermission
            if not isinstance(getattr(pilot, 'execution_permission', None), DocumentsExecutionPermission):
                raise ValueError("External execution permission integration required")
        self.synthetic, self.execution_enabled = synthetic, execution_enabled
        self.pilot, self.actions = pilot, actions
        self.enrollment = tuple(enrollment)
        self.catalog, self.approvals = catalog, approvals
        self._mutation = threading.Lock()

    def operator(self, principal):
        if (principal is None or principal.kind != "user" or
                (principal.issuer, principal.tenant_identity, principal.subject) != self.enrollment):
            raise SecurityError()
        self.pilot._operator(principal)
        return principal.scope.identity()

    def execution_available(self, p, approval, source, kind):
        if not self.execution_enabled:
            return False
        if self.synthetic:
            return True
        try:
            claims = self.pilot.execution_permission.authorize(p, approval, source, kind)
            return (self.pilot.execution_permission.permissions.remaining(claims) > 0
                    and min(claims['exp'], p.expires, approval.expires_at.timestamp(), source.expires_at.timestamp()) - self.pilot.clock() >= self.pilot.policy.provider_seconds)
        except (SecurityError, PilotError):
            return False

    def context(self, p):
        self.operator(p)
        with self.pilot.control.transaction() as db:
            stopped = bool(self.pilot.control._config(db)["stopped"])
        available = self.synthetic and self.execution_enabled or any(
            self.execution_available(p, a, self.pilot.sources.get(a.source_approval), 'documents_synthesis')
            for a in self.approvals)
        return dict(owner_id=str(p.scope.owner), tenant_id=str(p.scope.tenant), expires=p.expires,
                    enrolled=True, mode="SYNTHETIC_FIXTURE" if self.synthetic else "GOVERNED_EXTERNAL" if available else "EXTERNAL_EXECUTION_BLOCKED",
                    execution_enabled=available, limits=self.pilot.policy.model_dump(mode="json"),
                    stopped=stopped, allowed_actions=["inspect", "close", "withdraw", "stop"] if stopped else
                    ["select", "inspect", "publish", "cancel", "close", "withdraw", "stop"] if not available else
                    ["select", "start", "publish", "question", "cancel", "close", "withdraw", "stop"])

    def sources(self, p):
        self.operator(p)
        return [dict(source_approval_id=s.approval_id, name=s.filename, type=s.mime, sha256=s.sha256,
                     classification=s.classification, expires=s.expires_at.isoformat(),
                     eligible=s.approved_at.timestamp() <= self.pilot.clock() < s.expires_at.timestamp(),
                     limits=self.pilot.policy.model_dump(mode="json")) for s in self.pilot.sources.values()]

    def create(self, p, source, key):
        owner = self.operator(p)
        if source not in self.catalog:
            raise PilotError("pilot_source_refused")
        with self._mutation:
            def execute():
                with self.pilot.control.transaction() as db:
                    consumed = {r[0] for r in db.execute("SELECT id FROM sessions")}
                approval = next((a for a in self.approvals if a.source_approval == source
                                 and str(a.session_id) not in consumed), None)
                if approval is None:
                    raise PilotError("pilot_limit")
                self.pilot.create_session(p, approval)
                self.pilot.select_source(p, approval.session_id, self.catalog[source])
                return dict(session_id=str(approval.session_id), source_id=self.pilot.sources[source].source_id,
                            state="OPEN")
            return self.actions.run(owner, "create", key, {"source": source}, execute)

    def start(self, p, session):
        self.operator(p)
        if not self.execution_enabled:
            raise PilotError("pilot_not_ready")
        with self._mutation:
            row = self.pilot._session(p, session)
            if not self.execution_available(p, row['approval'], row['source'], 'documents_synthesis'):
                raise SecurityError()
            self.pilot.start(p, session)
        row = self.pilot._session(p, session)
        return dict(job_id=row["data"]["job"], state=self.pilot.status(p, session)["job_state"])

    def status(self, p, session):
        self.operator(p)
        row = self.pilot._session(p, session, active=False)
        state = self.pilot.status(p, session)
        state.update(job_id=row["data"].get("job"), generation=row["data"].get("generation"),
                     source_id=row["source"].source_id, source_sha256=row["source"].sha256,
                     limits=self.pilot.policy.model_dump(mode="json"),
                     questions_used=row["data"].get("questions", 0),
                     authorization_expiry=min(p.expires, row["approval"].expires_at.timestamp()),
                     semantic_support="not_evaluated", retention="RETAINED_BY_POLICY")
        if row["data"].get("job"):
            job = self.pilot.jobs.get_job(p.scope, UUID(row["data"]["job"]))
            state["last_update"] = job.updated_at.isoformat()
            state["steps"] = [dict(stage=s.spec.stage, state=s.state.value)
                              for s in self.pilot.jobs.steps(p.scope, job.job_id)]
        usage = self.pilot.governance.usage(p, self.pilot.authority)
        settled = [r for r in usage if r["state"] == "SETTLED"]
        unsettled = [r for r in usage if r["state"] not in {"SETTLED", "RELEASED"}]
        state["usage"] = dict(synthetic=self.synthetic, attempts=len(usage),
            currency=self.pilot.governance.catalog.currency, unsettled=len(unsettled),
            unknown=sum(r["state"] == "UNKNOWN" for r in usage),
            measured_input_tokens=sum(r["actual_input"] for r in settled),
            measured_output_tokens=sum(r["actual_output"] for r in settled),
            measured_cost=str(sum((Decimal(r["actual_cost"]) for r in settled), Decimal(0))),
            unsettled_reserved_tokens=sum(r["input"] + r["output"] for r in unsettled),
            unsettled_reserved_cost=str(sum((Decimal(r["cost"]) for r in unsettled), Decimal(0))))
        state["outcome"] = state.get("digest_status") or state.get("job_state") or state["session_state"]
        state["retry_eligible"] = False
        state['start_enabled'] = self.execution_available(p, row['approval'], row['source'], 'documents_synthesis')
        state['question_enabled'] = self.execution_available(p, row['approval'], row['source'], 'documents_question')
        state["execution_enabled"] = state['question_enabled'] if row['data'].get('generation') else state['start_enabled']
        state["allowed_actions"] = ["close", "withdraw"]
        if state["session_state"] == "OPEN":
            state["allowed_actions"] += ["start", "cancel"]
            if state.get("digest_status") == "COMPLETE":
                state["allowed_actions"].append("publish")
            if state.get("generation") and state["questions_used"] < self.pilot.policy.max_questions:
                state["allowed_actions"].append("question")
        if not self.synthetic and row['data'].get('generation'):
            try:
                self.pilot._quality(row)
                state['review_state'] = 'REVIEW_ATTACHED'
            except PilotError as exc:
                if exc.category != 'pilot_not_ready':
                    raise
                state['review_state'] = 'EXPERT_REVIEW_REQUIRED'
                state['question_enabled'] = False
        state['start_enabled'] &= 'start' in state['allowed_actions']
        state['question_enabled'] &= 'question' in state['allowed_actions']
        state['execution_enabled'] = state['question_enabled'] if row['data'].get('generation') else state['start_enabled']
        if not state["execution_enabled"]:
            state["allowed_actions"] = [a for a in state["allowed_actions"] if a not in {"start", "question"}]
        return state

    def publish(self, p, session, expected):
        owner = self.operator(p)
        with self._mutation:
            row = self.pilot._session(p, session)
            if row["data"].get("job") != str(expected):
                raise PilotError()
            def execute():
                generation = self.pilot.publish(p, session)
                return dict(generation=generation, state="PUBLISHED")
            result, _ = self.actions.run(owner, "publish/" + str(session), str(expected),
                                         {"job": str(expected)}, execute)
            if self.pilot.publication.authority.active().generation != UUID(result["generation"]):
                raise PilotError("pilot_denied")
            return result

    def digest(self, p, session):
        self.operator(p)
        packet = self.pilot.present(p, session, lambda packet: packet)
        # Re-authorized read of already accepted bounded answers; polling never
        # submits a question. Private action records are retained, not erased.
        import json
        with self.actions.transaction() as db:
            records = list(db.execute("SELECT result FROM actions WHERE owner=? AND action=? AND result IS NOT NULL LIMIT 3",
                           (p.scope.identity(), "question/" + str(session))))
        packet['answers'], pending_answers = [], []
        if not self.synthetic:
            packet['pending_answers'] = pending_answers
        for record in records:
            answer = json.loads(record[0])
            if answer.get('state') == 'EXPERT_REVIEW_REQUIRED':
                try:
                    accepted = self.pilot.present_answer(p, session, UUID(answer['answer_id']), lambda value: value)
                    answer = dict(accepted, answer_id=answer['answer_id'])
                except PilotError as exc:
                    if exc.category != 'pilot_not_ready':
                        raise
                    pending_answers.append(answer)
                    continue
            packet['answers'].append(answer)
        if any(a["generation"] != packet["generation"] for a in packet["answers"]):
            raise PilotError("pilot_not_ready")
        return packet

    def question(self, p, session, query, key):
        owner = self.operator(p)
        if not self.execution_enabled:
            raise PilotError("pilot_not_ready")
        with self._mutation:
            self.pilot._session(p, session)
            def execute():
                row = self.pilot._session(p, session)
                if not self.execution_available(p, row['approval'], row['source'], 'documents_question'):
                    raise SecurityError()
                result = self.pilot.question(p, session, query, lambda packet: packet)
                return result if result.get('state') == 'EXPERT_REVIEW_REQUIRED' else dict(result, answer_id=str(uuid4()))
            result, _ = self.actions.run(owner, "question/" + str(session), key, {"query": query}, execute)
            row = self.pilot._session(p, session)
            if result.get('state') != 'EXPERT_REVIEW_REQUIRED' and result["generation"] != row["data"].get("generation"):
                raise PilotError("pilot_not_ready")
            return result

    def reload(self, p, session):
        self.operator(p)
        self.pilot.load_presentation(p, session)
        return self.status(p, session)

    def cancel(self, p, session):
        self.operator(p)
        row = self.pilot._session(p, session, active=False)
        if row["data"].get("job"):
            AuthorizedJobs(self.pilot.authority, DocumentJobs(self.pilot.jobs, self.pilot.objects)).cancel(
                p, UUID(row["data"]["job"]))
        return dict(state="CANCEL_REQUESTED", may_complete_and_bill=True)

    def close(self, p, session, withdrawal):
        self.operator(p)
        result = self.pilot.close(p, session, withdrawal=withdrawal)
        with self.pilot.control.transaction() as db:
            actual = self.pilot.control.get(db, session, p.scope.identity(), active=False)["state"]
        # The trusted facade inventory includes financial tickets/provider
        # records for operator maintenance. HTTP returns retention categories,
        # never those raw records or immutable object/checkpoint identifiers.
        residuals = [{k: item[k] for k in ("class", "state", "custodian", "location", "reason", "deadline")
                      if k in item} for item in result["inventory"]]
        return dict(state=actual, retention="PURGE_PENDING",
                    physical_erasure=False, residuals=residuals,
                    unsettled_execution_intents=sum(o["state"] in {"ACTIVE", "UNKNOWN"} for o in result["operations"]),
                    adapter_answers="RETAINED_PRIVATE_ACTION_RECORDS")

    def stop(self, p):
        self.operator(p)
        return self.pilot.stop(p)

    def release_guard(self, p, session=None, *, active=False):
        """Capture facts now; recheck in canonical lock order at ASGI send."""
        self.operator(p)
        pilot = self.pilot
        row = pilot._session(p, session, active=active) if session else None
        documents = (row["source"].document_id,) if row and row["data"].get("plan") else ()
        snapshot = pilot.authority.snapshot(p, documents)
        with pilot.control.transaction() as db:
            config_epoch = pilot.control._config(db)["epoch"]

        @contextmanager
        def guard():
            try:
                with pilot.control.transaction() as db:
                    cfg = pilot.control._config(db)
                    if cfg["epoch"] != config_epoch:
                        raise SecurityError()
                    if row:
                        current = pilot.control.get(db, session, p.scope.identity(), active=active)
                        if current["epoch"] != row["epoch"]:
                            raise SecurityError()
                    with pilot.authority.release(snapshot):
                        if row and row["data"].get("generation"):
                            with pilot.publication.authority.transaction() as publication_db:
                                published = pilot.publication.authority._active(publication_db)
                                if (str(published.generation) != row["data"]["generation"] or
                                        published.epoch != row["data"]["publication_epoch"]):
                                    raise SecurityError()
                                yield
                        else:
                            yield
            except PilotError:
                raise SecurityError() from None
        return guard


class LocalRunner:
    """One controlled lane independent of requests. Restart discards bearer grants.

    Durable job/checkpoint/outbox state is authoritative. No token is persisted.
    Fresh start replay is required to reauthorize after restart. A claimed call
    with uncertain outcome remains blocked by the existing pilot authority.
    """
    def __init__(self, workflow, *, interval=2, admission_ready=lambda: True):
        self.workflow, self.interval = workflow, interval
        self.admission_ready = admission_ready
        self.grants = {}
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.thread = None
        self.heartbeat = 0
        self.outcome = "IDLE"

    def authorize(self, p, session):
        self.workflow.operator(p)
        with self.lock:
            self.grants[session] = p
        # Explicit authorized reload, never status-time index building.
        row = self.workflow.pilot._session(p, session)
        if row["data"].get("generation"):
            self.workflow.pilot.load_presentation(p, session)

    def once(self):
        self.heartbeat = time.monotonic()
        pilot = self.workflow.pilot
        with self.lock:
            grants = list(self.grants.items())
        for session, principal in grants:
            try:
                self.workflow.operator(principal)
                pilot._session(principal, session, execution=True)
                pilot.jobs.reconcile()
                status = pilot.status(principal, session)
                if status.get("job_state") in {"COMPLETED", "FAILED", "PARTIAL", "CANCELLED"}:
                    self.outcome = "IDLE"
                    continue
                self.outcome = "ACTIVE"
                if self.admission_ready():
                    pilot.step(principal, session)
                else:
                    self.outcome = "WAITING_ADMISSION"
            except Exception:
                # Never retry an uncertain effect. Fresh explicit authorization
                # cannot clear pilot UNKNOWN or terminal job state.
                self.outcome = "RECONCILIATION_REQUIRED"
                with self.lock:
                    self.grants.pop(session, None)

    def start(self):
        def run():
            while not self.stop_event.is_set():
                self.once()
                self.stop_event.wait(self.interval)
        with self.lock:
            if self.thread is not None or self.stop_event.is_set():
                raise RuntimeError("Document runner already started or stopped")
            self.thread = threading.Thread(target=run, name="document-demo-runner", daemon=True)
            self.thread.start()

    def close(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=65)
            if self.thread.is_alive():
                raise RuntimeError("Document runner requires shutdown reconciliation")
