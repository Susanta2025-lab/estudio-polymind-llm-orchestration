"""Trusted local runner composing existing authorized document services.

Every entry takes a verified operator. Participants only see an explicitly
released presentation; no principal, filesystem path, store or token is exposed.
"""

import json
import time
from datetime import datetime, timezone
from hashlib import sha256
from uuid import UUID, uuid4

from documents.digestion.codec import read
from documents.digestion.managed import (
    ManagedDigestionHandler,
    ManagedSynthesisInference,
    classify_managed,
)
from documents.digestion.models import Plan
from documents.digestion.workflow import admit, load_digest, prepare
from documents.jobs.models import RetryPolicy, fingerprint
from documents.jobs.service import DocumentJobs
from documents.jobs.worker import LocalDispatcher, Worker
from documents.pilot.control import PilotControl
from documents.pilot.execution import (
    PilotExecution,
    PilotProvider,
    fixture_execution_only,
)
from documents.pilot.intake import RecordingStore, intake
from documents.pilot.models import (
    Feedback,
    PilotError,
    PilotPolicy,
    ReviewFinding,
    SessionApproval,
    SourceApproval,
)
from documents.publication.analysis import AnalysisRequest, DocumentAnalysis
from documents.publication.retrieval import PublicationReplica
from governance.execution import GovernedExecution
from llm.inference import ModelRole
from security.models import Action
from security.services import AuthorizedAnalysis, AuthorizedJobs, AuthorizedPublication


class SupervisedPilot:
    def __init__(
        self,
        *,
        control_path,
        authority,
        objects,
        jobs,
        governance,
        admission,
        provider,
        managed_settings,
        analysis_capability,
        planning_profile,
        publication,
        sources,
        policy=None,
        execution_permission=fixture_execution_only,
        clock=time.time,
        extraction_limits=None,
        reranker=None,
        initialize=False,
    ):
        policy = policy or PilotPolicy()
        self.authority, self.objects, self.jobs = authority, objects, jobs
        self.governance, self.admission, self.provider = governance, admission, provider
        self.managed_settings, self.planning_profile = (
            managed_settings,
            planning_profile,
        )
        self.analysis_capability = analysis_capability
        self.publication, self.policy, self.clock = publication, policy, clock
        self._replicas = {}
        self.execution_permission, self.extraction_limits = (
            execution_permission,
            extraction_limits,
        )
        self.reranker = reranker
        self.sources = {
            s.approval_id: SourceApproval.model_validate(s.model_dump())
            for s in sources
        }
        if (
            not self.sources
            or len(self.sources) != len(sources)
            or publication.objects is not objects
            or publication.jobs is not jobs
            or any(s.owner != publication.scope for s in self.sources.values())
            or any(
                p.template_version != "managed-prompt/11"
                for p in managed_settings.profiles
            )
            or managed_settings.total_seconds > policy.provider_seconds
            or any(
                p.output_tokens > policy.max_output
                or p.input_tokens
                + managed_settings.capability.overhead_tokens
                + managed_settings.capability.safety_tokens
                > policy.max_input
                for p in managed_settings.profiles
            )
            or (
                execution_permission is fixture_execution_only
                and not getattr(provider, "pilot_fixture", False)
            )
        ):
            raise PilotError()
        self.model_binding = {
            r.value: provider.model_id(r)
            for r in (ModelRole.GENERAL, ModelRole.SUMMARIZATION)
        }
        # Bind reopen to exact existing authorities, policy, profile, source
        # approvals and models. No cloned financial authority/allowance.
        binding = {
            "policy": policy.model_dump(mode="json"),
            "sources": [s.model_dump(mode="json") for s in self.sources.values()],
            "managed": managed_settings.model_dump(mode="json"),
            "analysis": analysis_capability.model_dump(mode="json"),
            "planning": planning_profile.model_dump(mode="json"),
            "models": self.model_binding,
            "provider": provider.name,
            "authority": str(authority.path),
            "governance": str(governance.path),
            "admission": str(admission.path),
            "objects": str(objects.root),
            "jobs": str(jobs.path),
            "publication": str(publication.authority.path),
            "quota": admission.quota_key,
            "provider_policy": admission.policy.model_dump(mode="json"),
            "governance_policy": governance.policy.model_dump(mode="json"),
            "catalog": governance.catalog.model_dump(mode="json"),
        }
        self.control = PilotControl(
            control_path, binding, policy, clock=clock, initialize=initialize
        )

    def _operator(self, principal):
        self.authority.authorize(principal, Action.PUBLICATION_MANAGE)
        if principal.scope != self.publication.scope:
            raise PilotError()
        if any(
            self.provider.model_id(ModelRole(role)) != model
            for role, model in self.model_binding.items()
        ):
            raise PilotError()

    def _session(self, principal, session, *, execution=False, active=True):
        self._operator(principal)
        with self.control.transaction() as db:
            row = self.control.get(
                db,
                session,
                principal.scope.identity(),
                active=active,
                execution=execution,
            )
        if row["source"] != self.sources.get(row["source"].approval_id):
            raise PilotError()
        if row["data"].get("plan") and active:
            self.authority.authorize(
                principal, Action.DOCUMENT_READ, row["source"].document_id
            )
        return row

    def create_session(self, principal, approval):
        self._operator(principal)
        approval = SessionApproval.model_validate(approval.model_dump())
        source = self.sources.get(approval.source_approval)
        now = self.clock()
        if (
            source is None
            or source.owner != principal.scope
            or source.approved_by != principal.scope.owner
            or approval.approved_by != principal.scope.owner
            or not source.approved_at.timestamp() <= now < source.expires_at.timestamp()
            or not approval.approved_at.timestamp()
            <= now
            < approval.expires_at.timestamp()
            or approval.expires_at.timestamp() - approval.approved_at.timestamp()
            > self.policy.session_seconds
            or (approval.mode == "synthetic" and source.classification != "synthetic")
        ):
            raise PilotError()
        with self.control.transaction() as db:
            prior = [
                json.loads(r[0]).get("job")
                for r in db.execute("SELECT data FROM sessions")
            ]
        for job in filter(None, prior):
            if self.jobs.get_job(principal.scope, UUID(job)).state not in {
                "COMPLETED",
                "FAILED",
                "CANCELLED",
                "PARTIAL",
            }:
                raise PilotError("pilot_limit")
        self.control.create(approval, source, principal.scope.identity())
        return {
            "session_id": str(approval.session_id),
            "operator": "OPERATOR_AUTHENTICATED",
            "session": "PARTICIPANT_SESSION_APPROVED",
            "document": "DOCUMENT_APPROVED",
            "execution": "NOT_AUTHORIZED",
            "consent": approval.consent,
        }

    def select_source(self, principal, session, data):
        row = self._session(principal, session)
        if row["data"].get("plan"):
            if (
                type(data) is not bytes
                or sha256(data).hexdigest() != row["source"].sha256
            ):
                raise PilotError("pilot_source_refused")
            return self._plan(row)
        with self.control.transaction() as db:
            current = self.control.get(db, session, principal.scope.identity())
            if current["data"].get("intake_started"):
                raise PilotError("pilot_reconciliation_required")
            self.control.update(db, current, intake_started=True)
            self.control.event(db, session, "INTAKE_STARTED")
        store = RecordingStore(self.objects, self.control, session)
        artifact, ref = intake(
            data,
            row["source"],
            principal.scope,
            store,
            self.policy,
            now=datetime.fromtimestamp(self.clock(), timezone.utc),
            limits=self.extraction_limits,
        )
        self.authority.register_document(principal, artifact.document)
        inference = ManagedSynthesisInference(
            self.provider, self.managed_settings, self.admission
        )
        profile = inference.profile(self.planning_profile)
        plan, plan_ref = prepare(artifact, ref, profile, store)
        calls = len(plan.chunks) + len(plan.reducers)
        if not 0 < calls <= self.policy.max_synthesis_calls:
            raise PilotError("pilot_limit")
        # Render every leaf before financial reservation. Reducers remain bound
        # by the conservative complete-child plan and runtime G1/G2 validation.
        for chunk in plan.chunks:
            request = ManagedDigestionHandler.request(plan, chunk.chunk_id, {}, {})
            _, estimated_input = inference.bind(None, "chunk").render(request)
            if estimated_input > self.policy.max_input:
                raise PilotError("pilot_limit")
        with self.control.transaction() as db:
            current = self.control.get(db, session, principal.scope.identity())
            self.control.update(
                db,
                current,
                plan=plan_ref.model_dump(mode="json"),
                planned_calls=calls,
                extraction=ref.model_dump(mode="json"),
            )
            self.control.event(db, session, "SOURCE_PREFLIGHT_ACCEPTED")
        return plan

    def _plan(self, row):
        from documents.models import ObjectRef

        ref = ObjectRef.model_validate(row["data"]["plan"])
        plan = read(
            self.objects,
            row["source"].owner,
            ref,
            Plan,
            self.planning_profile.max_artifact_bytes,
        )
        if plan.profile.prompt_profile != "managed-prompt/11":
            raise PilotError()
        return plan

    def associate_retained(self, principal, session, job_id):
        """Bind an explicitly preapproved unchanged digest without regeneration.

        The approval pins the digest object hash (and therefore its source,
        profile, plan and receipts). This grants no new inference permission.
        """
        row = self._session(principal, session)
        if row["data"] or row["source"].retained_digest_sha256 is None:
            raise PilotError()
        AuthorizedJobs(self.authority, DocumentJobs(self.jobs, self.objects)).get(
            principal, job_id
        )
        from documents.publication.planning import accepted

        verified, artifact, digest, plan = accepted(
            self.jobs, self.objects, principal.scope, job_id
        )
        if (
            verified.digest.sha256 != row["source"].retained_digest_sha256
            or verified.document_id != row["source"].document_id
            or artifact.document.source.sha256 != row["source"].sha256
            or artifact.document.source.byte_size > self.policy.max_source_bytes
            or (artifact.document.page_count or 0) > self.policy.max_pages
            or sum(len(u.text) for u in artifact.units) > self.policy.max_characters
            or plan.profile.prompt_profile != "managed-prompt/11"
            or len(plan.chunks) + len(plan.reducers) > self.policy.max_synthesis_calls
            or any(
                u.decision.outcome != "native_accepted"
                or u.decision.observations.has_images is not False
                or u.decision.observations.has_graphics is not False
                for u in artifact.units
            )
        ):
            raise PilotError("pilot_source_refused")
        for ref in (
            artifact.document.source,
            verified.extraction,
            verified.digest,
            digest.plan,
            *digest.checkpoints,
        ):
            self.control.object(session, ref, "RETAINED_APPROVED")
        with self.control.transaction() as db:
            current = self.control.get(db, session, principal.scope.identity())
            if current["data"]:
                raise PilotError()
            self.control.update(
                db,
                current,
                job=str(job_id),
                plan=digest.plan.model_dump(mode="json"),
                extraction=verified.extraction.model_dump(mode="json"),
                planned_calls=len(plan.chunks) + len(plan.reducers),
                retained=True,
                execution_authorized=False,
            )
            self.control.event(db, session, "RETAINED_OUTPUT_ASSOCIATED")
        return self.status(principal, session)

    def start(self, principal, session):
        row = self._session(principal, session)
        if "plan" not in row["data"]:
            raise PilotError("pilot_not_ready")
        if row["data"].get("job"):
            return self.status(principal, session)
        plan = self._plan(row)
        from documents.models import ObjectRef
        from documents.pilot.scheduling import forecast

        calls = []
        for i in range(row["data"]["planned_calls"] + self.policy.max_questions):
            synthesis = i < row["data"]["planned_calls"]
            role = ModelRole.SUMMARIZATION if synthesis else ModelRole.GENERAL
            calls.append(
                {
                    "at": self.clock() + 61 * i,
                    "input": self.policy.max_input,
                    "output": self.policy.max_output,
                    "provider": self.provider.name,
                    "model": self.provider.model_id(role),
                    "workload": "DOCUMENT_BACKGROUND" if synthesis else "INTERACTIVE",
                }
            )
        forecast_result = forecast(
            self.governance, self.admission, self.authority, principal, calls
        )

        # Idempotent replay after a crash between admission and session update
        # returns the same durable job; it never creates another execution.
        job = admit(
            self.jobs,
            RecordingStore(self.objects, self.control, session),
            plan,
            ObjectRef.model_validate(row["data"]["plan"]),
            request_key=f"pilot/{session}",
            retry=RetryPolicy(
                max_attempts=1, budget_seconds=self.policy.workflow_seconds
            ),
        )
        with self.control.transaction() as db:
            current = self.control.get(db, session, principal.scope.identity())
            if current["data"].get("job") not in (None, str(job.job_id)):
                raise PilotError()
            self.control.update(
                db,
                current,
                job=str(job.job_id),
                execution_authorized=True,
                deadline=current["data"].get(
                    "deadline", self.clock() + self.policy.workflow_seconds
                ),
                capacity_forecast=forecast_result,
            )
            self.control.event(db, session, "EXECUTION_AUTHORIZED")
        return self.status(principal, session)

    def step(self, principal, session):
        row = self._session(principal, session, execution=True)
        from documents.models import ObjectRef

        snapshot = self.authority.snapshot(
            principal, (row["source"].document_id,), Action.DOCUMENT_DELETE
        )
        governed = PilotExecution(
            self,
            principal,
            session,
            GovernedExecution(
                self.provider, self.admission, self.governance, self.authority, snapshot
            ),
        )
        inference = ManagedSynthesisInference(
            self.provider, self.managed_settings, self.admission, governance=governed
        )
        handler = ManagedDigestionHandler(
            self.jobs, ObjectRef.model_validate(row["data"]["plan"]), inference
        )
        queue = LocalDispatcher()
        for message in self.jobs.pending_dispatch(1000):
            if (
                str(message.job_id) == row["data"]["job"]
                and message.scope == principal.scope
            ):
                queue.send(message)
                # Leave undispatched unrelated work untouched.
                self.jobs.mark_delivered(message)
        worker = Worker(
            self.jobs,
            queue,
            RecordingStore(self.objects, self.control, session),
            handler,
            owner="supervised-pilot",
            classifier=classify_managed,
        )
        worker.once()
        return self.status(principal, session)

    def status(self, principal, session):
        row = self._session(principal, session, active=False)
        with self.control.transaction() as db:
            stopped = bool(self.control._config(db)["stopped"])
        document_current = row["source"].expires_at.timestamp() > self.clock()
        session_state = row["state"]
        if session_state == "OPEN" and stopped:
            session_state = "STOPPED"
        elif (
            session_state == "OPEN"
            and row["approval"].expires_at.timestamp() <= self.clock()
        ):
            session_state = "EXPIRED"
        result = {
            "session_id": str(session),
            "session_state": session_state,
            "operator": "OPERATOR_AUTHENTICATED",
            "participant": "PARTICIPANT_SESSION_APPROVED",
            "document": "DOCUMENT_APPROVED"
            if document_current
            else "DOCUMENT_APPROVAL_EXPIRED",
            "execution": "NOT_AUTHORIZED",
            "result": "NOT_READY",
        }
        if row["data"].get("job"):
            job = AuthorizedJobs(
                self.authority, DocumentJobs(self.jobs, self.objects)
            ).get(principal, UUID(row["data"]["job"]))
            result.update(
                execution="RETAINED_RESULT_NO_NEW_EXECUTION"
                if row["data"].get("retained")
                else "EXECUTION_AUTHORIZED",
                job_state=job.state.value,
                progress=job.progress.model_dump(mode="json"),
            )
            if job.state in {"COMPLETED", "PARTIAL"}:
                digest = load_digest(
                    self.jobs, self.objects, principal.scope, job.job_id
                )
                result.update(
                    digest_status=digest.status,
                    coverage=digest.coverage.model_dump(mode="json"),
                )
                if (
                    digest.status == "COMPLETE"
                    and session_state == "OPEN"
                    and document_current
                ):
                    result["result"] = "RESULT_READY"
            elif job.state in {"FAILED", "CANCELLED"}:
                result["digest_status"] = "FAILED"
        if session_state in {"CLOSED", "WITHDRAWN", "STOPPED", "EXPIRED"}:
            result["result"] = "SESSION_CLOSED"
        return result

    def publish(self, principal, session):
        row = self._session(principal, session)
        digest = load_digest(
            self.jobs, self.objects, principal.scope, UUID(row["data"]["job"])
        )
        if digest.status != "COMPLETE" or digest.coverage.fraction != 1:
            raise PilotError("pilot_not_ready")
        from documents.publication.service import PublicationService

        tracked_publication = PublicationService(
            self.publication.authority,
            RecordingStore(self.objects, self.control, session),
            self.jobs,
            self.publication.vectors,
            self.publication.encoder,
            principal.scope,
        )
        authorized = AuthorizedPublication(self.authority, tracked_publication)
        manifest = authorized.run(principal, "plan", [UUID(row["data"]["job"])])
        # Publication writes join the same conservative inventory, including
        # candidates that fail before activation. Existing manifests are retained.
        ref, _, _ = self.publication.authority.candidate(manifest.generation)
        self.control.object(session, ref, "WRITTEN")
        authorized.run(principal, "prepare", manifest.generation)
        self._session(principal, session)
        with self.control.release(session, principal.scope.identity(), row["epoch"]):
            active = authorized.run(principal, "activate", manifest.generation)
        with self.control.transaction() as db:
            current = self.control.get(db, session, principal.scope.identity())
            self.control.update(
                db,
                current,
                generation=str(manifest.generation),
                publication_epoch=active.epoch,
                evidence_sha256=fingerprint(digest.model_dump(mode="json")),
            )
            self.control.event(db, session, "PUBLICATION_ACCEPTED")
        self.load_presentation(principal, session)
        return str(manifest.generation)

    def _replica(self, row):
        generation = UUID(row["data"]["generation"])
        active = self.publication.authority.active()
        if (
            active.generation != generation
            or active.epoch != row["data"]["publication_epoch"]
        ):
            raise PilotError("pilot_not_ready")
        replica = self._replicas.get(generation)
        if replica is None:
            raise PilotError("pilot_not_ready")
        return replica

    def load_presentation(self, principal, session):
        """Explicit operator/startup load; serving never rebuilds sparse state."""
        row = self._session(principal, session)
        generation = UUID(row["data"]["generation"])
        active = self.publication.authority.active()
        if (
            active.generation != generation
            or active.epoch != row["data"]["publication_epoch"]
        ):
            raise PilotError("pilot_not_ready")
        replica = PublicationReplica(self.publication, generation)
        replica.load()
        self._session(principal, session)
        self._replicas[generation] = replica

    def _quality(self, row, evidence=None):
        if row["approval"].mode != "external":
            return
        with self.control.transaction() as db:
            reviews = [
                ReviewFinding.model_validate_json(r[0])
                for r in db.execute(
                    "SELECT record FROM reviews WHERE session=? AND evidence=?",
                    (row["id"], evidence or row["data"]["evidence_sha256"]),
                )
            ]
        if len(reviews) < 2 or any(r.outcome != "accepted" for r in reviews):
            raise PilotError("pilot_not_ready")

    def present(self, principal, session, sink):
        row = self._session(principal, session)
        self._quality(row)
        replica = self._replica(row)
        snapshot = self.authority.snapshot(principal, (row["source"].document_id,))
        pin = replica.pin(
            (row["source"].document_id,), authorization=(self.authority, snapshot)
        )
        replica.validate_pin(pin)
        digest = load_digest(
            self.jobs, self.objects, principal.scope, UUID(row["data"]["job"])
        )
        if digest.status != "COMPLETE" or digest.coverage.fraction != 1:
            raise PilotError("pilot_not_ready")
        manifest = pin.snapshot[0]
        citations = replica.citations(
            pin,
            [
                {
                    "record_id": str(r.record_id),
                    "generation": str(manifest.generation),
                    "text": r.text,
                }
                for r in manifest.records
                if r.document_id == row["source"].document_id
            ],
        )
        from documents.digestion.models import SourcePiece
        from documents.digestion.validation import EvidenceIndex
        from documents.serialization import deserialize

        index = EvidenceIndex(
            deserialize(
                self.objects.read(
                    principal.scope,
                    digest.extraction,
                    max_bytes=self.planning_profile.max_artifact_bytes,
                )
            )
        )
        evidence = [
            {
                "evidence_id": str(
                    SourcePiece(evidence=e, text="", kind="text").evidence_id()
                ),
                "reference": e.model_dump(mode="json"),
                "excerpt": index.resolve(e),
                "physical_page": index.blocks[e.block_id][0].physical_page,
            }
            for e in digest.evidence
        ]
        packet = {
            "document_id": str(row["source"].document_id),
            "source_sha256": row["source"].sha256,
            "generation": str(manifest.generation),
            "digest_version": digest.schema_version,
            "evidence_sha256": row["data"]["evidence_sha256"],
            "status": digest.status,
            "coverage": digest.coverage.model_dump(mode="json"),
            "findings": [c.model_dump(mode="json") for c in digest.findings],
            "executive_summary": digest.executive_summary,
            "sections": [s.model_dump(mode="json") for s in digest.sections],
            "synthesis_claims": [
                c.model_dump(mode="json") for c in digest.synthesis_claims
            ],
            "evidence": evidence,
            "qualifications": [
                q.model_dump(mode="json") for q in digest.qualifications
            ],
            "contradictions": [
                c.model_dump(mode="json") for c in digest.contradictions
            ],
            "limitations": list(digest.limitations),
            "open_questions": list(digest.open_questions),
            "citations": [c.model_dump(mode="json") for c in citations],
            "semantic_support": "not_evaluated",
            "verification": "SYNTHETIC_FIXTURE"
            if row["approval"].mode == "synthetic"
            else "EXTERNAL_REVIEW_ATTACHED",
        }
        return self._release(principal, session, row, replica, snapshot, packet, sink)

    def _release(self, principal, session, row, replica, snapshot, packet, sink):
        # Only a bounded synchronous local presentation sink belongs here. No
        # cached packet is authority; revalidate at the actual handoff.
        with (
            self.control.release(session, principal.scope.identity(), row["epoch"]),
            self.authority.release(snapshot),
            self.publication.authority.transaction() as db,
        ):
            active = self.publication.authority._active(db)
            if (
                str(active.generation) != row["data"]["generation"]
                or active.epoch != row["data"]["publication_epoch"]
            ):
                raise PilotError("pilot_not_ready")
            return sink(packet)

    def question(self, principal, session, query, sink):
        row = self._session(principal, session, execution=True)
        self._quality(row)
        replica = self._replica(row)
        service = DocumentAnalysis(
            replica,
            PilotProvider(self, principal, session),
            self.analysis_capability,
            input_bytes=self.policy.max_input
            - self.analysis_capability.overhead_tokens
            - self.analysis_capability.safety_tokens,
            output_tokens=min(
                self.policy.max_output, self.analysis_capability.max_output_tokens
            ),
            reranker=self.reranker,
        )
        # Selected IDs are always server-derived; query text cannot change them.
        authorized = AuthorizedAnalysis(
            self.authority,
            self.governance,
            self.admission,
            {principal.scope.identity(): service},
        )
        request = AnalysisRequest(
            query=query, document_ids=(row["source"].document_id,)
        )
        with self.control.transaction() as db:
            current = self.control.get(
                db, session, principal.scope.identity(), execution=True
            )
            questions = current["data"].get("questions", 0)
            if questions >= self.policy.max_questions:
                raise PilotError("pilot_limit")
            self.control.update(db, current, questions=questions + 1)
            self.control.event(db, session, "QUESTION_SUBMITTED")
        result, snapshot = authorized.analyze(principal, request)
        result["limitations"] = [
            "Selected excerpts only; citation validity does not establish semantic entailment."
        ]
        if row["approval"].mode == "external":
            # New answers require their own expert-quality review. Never borrow
            # a digest's review for generated Q&A, and never release unreviewed
            # content through the participant sink.
            answer_id = uuid4()
            evidence = fingerprint(result)
            with self.control.transaction() as db:
                self.control.get(db, session, principal.scope.identity())
                db.execute(
                    "INSERT INTO answers VALUES(?,?,?,?)",
                    (str(answer_id), row["id"], evidence, json.dumps(result)),
                )
                self.control.event(db, session, "ANSWER_REVIEW_PENDING")
            return {
                "answer_id": str(answer_id),
                "evidence_sha256": evidence,
                "state": "EXPERT_REVIEW_REQUIRED",
            }
        return self._release(principal, session, row, replica, snapshot, result, sink)

    def answer_review_packet(self, principal, session, answer_id):
        row = self._session(principal, session)
        with self.control.transaction() as db:
            answer = db.execute(
                "SELECT record,evidence FROM answers WHERE id=? AND session=?",
                (str(answer_id), row["id"]),
            ).fetchone()
            if not answer:
                raise PilotError()
            return {
                "answer": json.loads(answer["record"]),
                "evidence_sha256": answer["evidence"],
                "reviewer_1": None,
                "reviewer_2": None,
            }

    def present_answer(self, principal, session, answer_id, sink):
        row = self._session(principal, session)
        packet = self.answer_review_packet(principal, session, answer_id)
        self._quality(row, packet["evidence_sha256"])
        replica = self._replica(row)
        snapshot = self.authority.snapshot(principal, (row["source"].document_id,))
        pin = replica.pin(
            (row["source"].document_id,), authorization=(self.authority, snapshot)
        )
        replica.validate_pin(pin)
        if packet["answer"]["generation"] != row["data"]["generation"]:
            raise PilotError()
        return self._release(
            principal, session, row, replica, snapshot, packet["answer"], sink
        )

    def feedback(self, principal, session, record):
        row = self._session(principal, session)
        record = Feedback.model_validate(record.model_dump())
        with self.control.transaction() as db:
            self.control.get(db, session, principal.scope.identity())
            db.execute(
                "INSERT INTO feedback VALUES(?,?) ON CONFLICT(session) DO UPDATE SET record=excluded.record",
                (row["id"], record.model_dump_json()),
            )
            self.control.event(db, session, "FEEDBACK_RECORDED")

    def attach_review(self, principal, session, record):
        row = self._session(principal, session)
        record = ReviewFinding.model_validate(record.model_dump())
        with self.control.transaction() as db:
            self.control.get(db, session, principal.scope.identity())
            if (
                record.evidence_sha256 != row["data"].get("evidence_sha256")
                and not db.execute(
                    "SELECT 1 FROM answers WHERE session=? AND evidence=?",
                    (row["id"], record.evidence_sha256),
                ).fetchone()
                or record.completed_at.timestamp() > self.clock()
            ):
                raise PilotError()
            db.execute(
                "INSERT INTO reviews VALUES(?,?,?,?)",
                (
                    row["id"],
                    record.reviewer_code,
                    record.evidence_sha256,
                    record.model_dump_json(),
                ),
            )
            self.control.event(db, session, "REVIEW_ATTACHED")

    def stop(self, principal):
        self._operator(principal)
        self.control.stop()  # Durable denial precedes best-effort job cancellation.
        with self.control.transaction() as db:
            rows = [
                dict(r)
                for r in db.execute(
                    "SELECT id,data FROM sessions WHERE owner=?",
                    (principal.scope.identity(),),
                )
            ]
        failures = 0
        for row in rows:
            job = json.loads(row["data"]).get("job")
            if job:
                try:
                    AuthorizedJobs(
                        self.authority, DocumentJobs(self.jobs, self.objects)
                    ).cancel(principal, UUID(job))
                except Exception:  # noqa: BLE001 - durable stop precedes best-effort cancellation
                    failures += 1
        return {
            "state": "PILOT_STOPPED",
            "cancellation_reconciliation_required": failures,
            "in_flight_usage": "MAY_COMPLETE_AND_BILL",
            "refund_claimed": False,
        }

    def close(self, principal, session, *, withdrawal=False):
        self._session(principal, session, active=False)
        self.control.close(session, principal.scope.identity(), withdrawal=withdrawal)
        row, _, _ = self.control.inventory(session, principal.scope.identity())
        if row["data"].get("job"):
            # Cancellation fences queued/running writes. Immutable accepted
            # artifacts/generations are preserved; presentation authority closes.
            AuthorizedJobs(
                self.authority, DocumentJobs(self.jobs, self.objects)
            ).cancel(principal, UUID(row["data"]["job"]))
        return self.inventory(principal, session)

    def inventory(self, principal, session):
        self._operator(principal)
        from documents.pilot.retention import inventory

        return inventory(self, principal, session)

    def reopen_intake(self, principal):
        self._operator(principal)
        self.control.reopen_intake()

    def retire_metadata(self, principal, session):
        self._operator(principal)
        self.control.retire_metadata(session, principal.scope.identity())
        return self.inventory(principal, session)

    def reconcile_operation(
        self, principal, session, operation, *, quiescence_reference
    ):
        """Observe trusted settlement, never invent usage or release money.

        The operator first stops/quiesces workers and reconciles financial and
        provider records using trusted evidence through their existing ports.
        This only clears the pilot's operational stop after verifying that state.
        """
        from pydantic import TypeAdapter

        from documents.jobs.models import Token

        TypeAdapter(Token).validate_python(quiescence_reference)
        row = self._session(principal, session, active=False)
        if row["state"] == "OPEN":
            raise PilotError()
        with self.governance.transaction() as db:
            self.governance._current_policy(db)
            rows = [
                dict(r)
                for r in db.execute(
                    "SELECT * FROM reservations WHERE tenant=? AND owner=?",
                    (str(principal.scope.tenant), str(principal.scope.owner)),
                )
            ]
        rows = [r for r in rows if json.loads(r["identity"])["step"] == str(operation)]
        if len(rows) != 1 or rows[0]["state"] not in {"SETTLED", "RELEASED"}:
            raise PilotError("pilot_reconciliation_required")
        identity = json.loads(rows[0]["identity"])
        calls = [
            r
            for r in self.admission.records(
                principal.scope.identity(), UUID(identity["job"])
            )
            if r["step"] == str(operation)
        ]
        if any(r["active"] for r in calls) or (
            rows[0]["state"] == "SETTLED" and len(calls) != 1
        ):
            raise PilotError("pilot_reconciliation_required")
        with self.control.transaction() as db:
            if not self.control._config(db)["stopped"]:
                raise PilotError()
            changed = db.execute(
                "UPDATE operations SET state='DONE' WHERE id=? AND session=? AND state IN ('ACTIVE','UNKNOWN')",
                (str(operation), str(session)),
            ).rowcount
            if changed != 1:
                raise PilotError()
            self.control.update(
                db,
                row,
                reconciliation_references={
                    **row["data"].get("reconciliation_references", {}),
                    str(operation): quiescence_reference,
                },
            )
            self.control.event(db, session, "OPERATION_RECONCILED")

    def review_packet(self, principal, session):
        # Protected operator evidence, not participant presentation. It does not
        # count as an independent completed review and performs no inference.
        row = self._session(principal, session)
        plan = self._plan(row)
        from documents.models import ObjectRef
        from documents.serialization import deserialize

        artifact = deserialize(
            self.objects.read(
                principal.scope,
                ObjectRef.model_validate(row["data"]["extraction"]),
                max_bytes=plan.profile.max_artifact_bytes,
            )
        )
        digest = load_digest(
            self.jobs, self.objects, principal.scope, UUID(row["data"]["job"])
        )
        return {
            "source_sha256": row["source"].sha256,
            "source": artifact.model_dump(mode="json"),
            "digest": digest.model_dump(mode="json"),
            "evidence_sha256": fingerprint(digest.model_dump(mode="json")),
            "reviewer_1": None,
            "reviewer_2": None,
            "semantic_acceptance": "PENDING",
            "historical_phase17_review": "DEFERRED_PENDING_TWO_INDEPENDENT_REVIEWERS",
        }


def _sanitized(method):
    from functools import wraps

    from documents.digestion.models import DigestionError
    from documents.errors import DocumentError
    from documents.jobs.errors import JobError
    from documents.publication.models import PublicationError
    from governance.ledger import GovernanceError
    from llm.inference import InferenceError
    from security.models import SecurityError

    @wraps(method)
    def run(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except (
            PilotError,
            SecurityError,
            DocumentError,
            DigestionError,
            JobError,
            PublicationError,
            GovernanceError,
        ):
            raise
        except InferenceError:
            raise PilotError("pilot_not_ready") from None
        except Exception:  # noqa: BLE001 - sanitized boundary includes injected adapters/sinks
            raise PilotError() from None

    return run


# The trusted local caller receives only content-free operational categories,
# including storage/validation/callback failures. No new HTTP error surface.
for _name in (
    "create_session",
    "select_source",
    "start",
    "step",
    "status",
    "publish",
    "present",
    "question",
    "feedback",
    "attach_review",
    "stop",
    "close",
    "inventory",
    "reopen_intake",
    "review_packet",
    "answer_review_packet",
    "present_answer",
    "retire_metadata",
    "reconcile_operation",
    "load_presentation",
    "associate_retained",
):
    setattr(SupervisedPilot, _name, _sanitized(getattr(SupervisedPilot, _name)))
