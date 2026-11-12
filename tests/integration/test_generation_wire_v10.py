"""V10 production workflow, receipts, restart and fail-closed provider selections."""

import json

import pytest

from tests.performance import foundry_preflight

pytestmark = pytest.mark.usefixtures("managed_wire_version")


def test_v10_native_four_call_workflow(tmp_path, monkeypatch):
    from documents.digestion import managed

    errors = []
    original = managed.classify_managed

    def classify(error):
        errors.append(repr(error))
        return original(error)

    monkeypatch.setattr(managed, "classify_managed", classify)
    result = foundry_preflight.execute(tmp_path, "L1")
    assert result["job_state"] == "COMPLETED", (result, errors)
    assert result["digest_status"] == "COMPLETE"
    assert result["calls"] == 4


@pytest.fixture
def run(tmp_path, monkeypatch):
    """Observe real local authorities, worker, HTTP and publication boundaries."""
    from types import SimpleNamespace

    from documents.digestion import workflow
    from documents.digestion.managed import ManagedDigestionHandler
    from tests.generation_wire_fixtures import proposal

    state = SimpleNamespace(root=tmp_path, requests=[], outputs=[], faults=[], calls=[])
    original_prepare, original_admit = workflow.prepare, workflow.admit
    original_analyze = ManagedDigestionHandler.analyze
    original_publish = foundry_preflight.publish

    def prepare(artifact, extraction, profile, store):
        state.artifact, state.store = artifact, store
        state.plan, state.plan_ref = original_prepare(
            artifact, extraction, profile, store
        )
        return state.plan, state.plan_ref

    def admit(ledger, store, plan, ref, **kwargs):
        state.ledger = ledger
        state.job = original_admit(ledger, store, plan, ref, **kwargs)
        return state.job

    def analyze(handler, request, *args):
        state.handler, state.request = handler, request
        state.requests.append(request)
        return original_analyze(handler, request, *args)

    def publish(*args, **kwargs):
        summary, state.replica = original_publish(*args, **kwargs)
        return summary, state.replica

    class HTTP(foundry_preflight.OfflineHTTP):
        def response(self, sent, result, stage):
            if stage != "question":
                value = proposal(state.request)
                result = json.dumps(value)
                if state.fault is not None:
                    result = state.fault(result, stage)
                state.outputs.append((stage, result))
            else:
                data = json.loads(sent["messages"][1]["content"])
                evidence = data["ORIGINAL_SOURCE_EVIDENCE"][0]
                result = json.dumps(
                    {
                        "answer": evidence["excerpt"],
                        "evidence_status": "available",
                        "citation_ids": [evidence["citation_id"]],
                    }
                )
            state.calls.append(stage)
            return super().response(sent, result, stage)

    monkeypatch.setattr(workflow, "prepare", prepare)
    monkeypatch.setattr(workflow, "admit", admit)
    monkeypatch.setattr(ManagedDigestionHandler, "analyze", analyze)
    monkeypatch.setattr(foundry_preflight, "publish", publish)
    monkeypatch.setattr(foundry_preflight, "OfflineHTTP", HTTP)

    def execute(fault=None):
        state.fault = fault
        state.result = foundry_preflight.execute(tmp_path, "L1")
        return state

    execute.state = state
    return execute


def reopen(state):
    from documents.jobs.sqlite import SQLiteJobLedger
    from documents.storage import LocalObjectStore

    ledger = SQLiteJobLedger(state.ledger.settings)
    store = LocalObjectStore(state.root / "objects")
    job = ledger.get_job(state.job.admission.scope, state.job.job_id)
    return ledger, store, job


def test_eight_claim_workflow_receipts_offsets_contradictions_and_reopening(run):
    from hashlib import sha256

    from documents.digestion.codec import read
    from documents.digestion.models import Checkpoint
    from documents.digestion.receipts import DecodingReceipt, ProposalRecord
    from documents.digestion.workflow import load_digest
    from documents.publication.planning import accepted

    state = run()
    assert state.result["job_state"] == "COMPLETED"
    assert state.calls == ["chunk", "structural", "root", "question"]
    assert state.result["calls"] == 4 and state.result["billable_calls"] == 0
    assert state.result["questions"]["status"] == "COMPLETE"
    assert all(r["state"] == "SETTLED" for r in state.result["governance_records"])
    ledger, store, job = reopen(state)
    scope, limit = job.admission.scope, job.admission.profile.max_artifact_bytes
    stages = [s for s in ledger.steps(scope, job.job_id) if len(s.manifest) == 3]
    assert len(stages) == 3
    for step in stages:
        cp = read(store, scope, step.manifest[0], Checkpoint, limit)
        receipt = read(store, scope, step.manifest[1], DecodingReceipt, limit)
        record = read(store, scope, step.manifest[2], ProposalRecord, limit)
        assert len(cp.result.claims) == 8
        assert (
            receipt.checkpoint == step.manifest[0]
            and receipt.proposal == step.manifest[2]
        )
        assert record.raw_sha256 == sha256(record.raw.encode()).hexdigest()
        assert record.audit_request_sha256 in {
            r["request_sha256"] for r in state.result["provider_records"]
        }
    digest = load_digest(ledger, store, scope, job.job_id)
    assert digest.status == "COMPLETE" and digest.coverage.fraction == 1
    assert digest.qualifications and len(digest.contradictions) == 1
    assert digest.contradictions[0].resolution == "unresolved"
    assert len(digest.evidence) == 4
    assert accepted(ledger, store, scope, job.job_id)[2] == digest
    assert accepted(ledger, store, scope, job.job_id)[2] == digest
    # All original-source offsets and excerpt membership are revalidated by the
    # publication graph and real Q&A interfaces, after fresh store/ledger reopen.
    assert len(state.calls) == 4
    assert not {r.key for s in stages for r in s.manifest} & {
        r.key for r in ledger.orphan_candidates()
    }


@pytest.mark.parametrize("stage,count", [("chunk", 1), ("structural", 2), ("root", 3)])
@pytest.mark.parametrize(
    "fault",
    [
        "unknown_source",
        "unknown_child",
        "binding",
        "coverage",
        "duplicate",
        "extra",
        "version",
    ],
)
def test_invalid_stage_blocks_dependents_and_settles_known_usage(
    run, stage, count, fault
):
    def corrupt(raw, current):
        if current != stage:
            return raw
        value = json.loads(raw)
        if fault == "unknown_source":
            value["claims"][0]["evidence_refs"] = ["E99"]
        elif fault == "unknown_child":
            value["claims"][0]["child_refs"] = ["C99"]
        elif fault == "binding":
            value["request_binding"] = "0" * 64
        elif fault == "coverage":
            for c in value["claims"]:
                c.update(
                    kind="commentary",
                    subject=None,
                    evidence_refs=[],
                    contradicting_evidence_refs=[],
                    child_refs=[],
                    qualifications=[],
                )
        elif fault == "duplicate":
            value["claims"][0]["evidence_refs"] = ["E1", "E1"]
        elif fault == "extra":
            value["stage_id"] = "not-model-owned"
        elif fault == "version":
            value["schema_version"] = "stage-proposal/999"
        return json.dumps(value)

    state = run(corrupt)
    assert state.result["job_state"] == "FAILED"
    assert state.result["calls"] == count
    assert "publication" not in state.result and "questions" not in state.result
    assert all(r["state"] == "SETTLED" for r in state.result["governance_records"])
    ledger, _store, job = reopen(state)
    steps = ledger.steps(job.admission.scope, job.job_id)
    failed = [s for s in steps if s.state == "FAILED"]
    assert len(failed) == 1 and failed[0].attempt_count == 1 and not failed[0].manifest
    assert all(s.attempt_count == 0 for s in steps if s.state == "CANCELLED")
    assert len([s for s in steps if len(s.manifest) == 3]) == count - 1
    assert len(state.calls) == count


class Interrupted(BaseException):
    pass


@pytest.mark.parametrize(
    "point",
    [
        "before_raw",
        "after_raw",
        "decode",
        "before_receipt",
        "during_receipt",
        "after_receipt",
        "before_commit",
        "after_commit",
    ],
)
def test_crash_windows_never_reinfer_or_accept_orphans(run, monkeypatch, point):
    from datetime import timedelta

    from documents.digestion import codec, wire
    from documents.digestion.managed import ManagedDigestionHandler, classify_managed
    from documents.digestion.receipts import DecodingReceipt, ProposalRecord
    from documents.jobs.sqlite import SQLiteJobLedger
    from documents.jobs.worker import LocalDispatcher, Worker, relay

    original_put, original_construct = codec.put, wire.construct
    original_commit = SQLiteJobLedger.commit
    interrupted = [False]

    def crash():
        if not interrupted[0]:
            interrupted[0] = True
            raise Interrupted()

    def put(store, scope, model, limit):
        if isinstance(model, ProposalRecord) and point == "before_raw":
            crash()
        if isinstance(model, DecodingReceipt) and point == "before_receipt":
            crash()
        if isinstance(model, DecodingReceipt) and point == "during_receipt":
            from documents import storage

            with monkeypatch.context() as patch:
                patch.setattr(storage.os, "link", lambda *a, **kw: crash())
                return original_put(store, scope, model, limit)
        result = original_put(store, scope, model, limit)
        if isinstance(model, ProposalRecord) and point == "after_raw":
            crash()
        if isinstance(model, DecodingReceipt) and point == "after_receipt":
            crash()
        return result

    def construct(*args):
        if point == "decode":
            crash()
        return original_construct(*args)

    def commit(ledger, lease, manifest):
        if len(manifest) == 3 and point == "before_commit":
            crash()
        result = original_commit(ledger, lease, manifest)
        if len(manifest) == 3 and point == "after_commit":
            crash()
        return result

    monkeypatch.setattr(codec, "put", put)
    from documents.digestion import workflow

    monkeypatch.setattr(workflow, "put", put)
    monkeypatch.setattr(wire, "construct", construct)
    monkeypatch.setattr(SQLiteJobLedger, "commit", commit)
    with pytest.raises(Interrupted):
        run()
    state = run.state
    ledger, store, job = reopen(state)
    scope = job.admission.scope
    steps = ledger.steps(scope, job.job_id)
    assert len(state.calls) == 1
    committed = [s for s in steps if len(s.manifest) == 3]
    assert len(committed) == (1 if point == "after_commit" else 0)

    # Expiry reconciliation uses the existing one-attempt policy. There is no
    # attempt to decode arbitrary orphan bytes or to make a replacement call.
    class Clock:
        def now(self):
            return max(s.execution_at for s in steps) + timedelta(days=1)

    ledger = SQLiteJobLedger(ledger.settings, clock=Clock())
    ledger.reconcile()
    if point != "after_commit":
        assert ledger.get_job(scope, job.job_id).state == "FAILED"
    queue = LocalDispatcher()
    relay(ledger, queue)

    class NoInference:
        def __call__(self, *args):
            raise AssertionError("Unauthorized extra execution")

    # Redelivering the interrupted stage itself never claims again.
    from documents.jobs.models import Dispatch

    stage = next(
        s for s in steps if s.spec.unit_id == str(state.plan.chunks[0].chunk_id)
    )
    queue.messages.clear()
    queue.send(
        Dispatch(dispatch_id=999, scope=scope, job_id=job.job_id, step_id=stage.step_id)
    )
    Worker(
        ledger,
        queue,
        store,
        NoInference(),
        owner="restarted",
        classifier=classify_managed,
    ).once()
    assert len(state.calls) == 1
    if point == "after_commit":
        # The earlier accepted checkpoint still verifies independently after restart.
        handler = ManagedDigestionHandler(
            ledger, state.plan_ref, state.handler.inference
        )
        handler._load(store, scope, job.admission.profile.max_artifact_bytes)
        handler._verify_proposals(
            store,
            job,
            {s.spec.unit_id: s for s in ledger.steps(scope, job.job_id)},
            state.plan,
        )


@pytest.mark.parametrize(
    "field",
    [
        "request_sha256",
        "table_sha256",
        "canonical_sha256",
        "generation_sha256",
        "audit_request_sha256",
        "wire_version",
        "decoder_version",
        "checkpoint",
        "proposal",
    ],
)
def test_corrupt_receipt_cannot_reopen_checkpoint(run, field):
    from documents.digestion.codec import read
    from documents.digestion.models import Checkpoint, DigestionError
    from documents.digestion.receipts import DecodingReceipt, verify

    state = run()
    ledger, store, job = reopen(state)
    scope, limit = job.admission.scope, job.admission.profile.max_artifact_bytes
    step = next(s for s in ledger.steps(scope, job.job_id) if len(s.manifest) == 3)
    cp = read(store, scope, step.manifest[0], Checkpoint, limit)
    receipt = read(store, scope, step.manifest[1], DecodingReceipt, limit)
    value = receipt.model_dump(mode="json")
    value[field] = (
        step.manifest[2 if field == "checkpoint" else 0].model_dump(mode="json")
        if field in ("checkpoint", "proposal")
        else "corrupt/2"
        if field.endswith("version")
        else "0" * 64
    )
    from hashlib import sha256
    from io import BytesIO

    from documents.jobs.models import canonical
    from documents.models import stable_id

    raw = canonical(value).encode()
    bad = store.put(
        scope,
        "artifact",
        stable_id("corrupt-receipt", sha256(raw).hexdigest()),
        BytesIO(raw),
        max_bytes=limit,
    )
    step = step.model_copy(
        update={"manifest": (step.manifest[0], bad, step.manifest[2])}
    )
    with pytest.raises(DigestionError):
        verify(
            ledger,
            store,
            job,
            step,
            state.plan_ref,
            state.requests[0],
            step.manifest[0],
            cp,
        )
    assert len(state.calls) == 4


@pytest.mark.parametrize(
    "field",
    [
        "request_sha256",
        "table_sha256",
        "raw_sha256",
        "config_sha256",
        "generation_sha256",
        "audit_request_sha256",
        "attempt",
        "fence",
        "job_id",
        "step_id",
        "plan",
        "raw",
    ],
)
def test_corrupt_provider_association_cannot_reopen(run, field):
    from uuid import UUID

    from documents.digestion.codec import put, read
    from documents.digestion.models import Checkpoint, DigestionError
    from documents.digestion.receipts import DecodingReceipt, ProposalRecord, verify

    state = run()
    ledger, store, job = reopen(state)
    scope, limit = job.admission.scope, job.admission.profile.max_artifact_bytes
    step = next(s for s in ledger.steps(scope, job.job_id) if len(s.manifest) == 3)
    cp = read(store, scope, step.manifest[0], Checkpoint, limit)
    receipt = read(store, scope, step.manifest[1], DecodingReceipt, limit)
    record = read(store, scope, step.manifest[2], ProposalRecord, limit)
    value = (
        "0" * 64
        if field.endswith("sha256")
        else 99
        if field in ("attempt", "fence")
        else UUID(int=9)
        if field.endswith("_id")
        else step.manifest[0]
        if field == "plan"
        else record.raw + " "
    )
    changed = record.model_copy(update={field: value})
    raw_ref = put(store, scope, changed, limit)
    new_receipt = receipt.model_copy(update={"proposal": raw_ref})
    receipt_ref = put(store, scope, new_receipt, limit)
    step = step.model_copy(
        update={"manifest": (step.manifest[0], receipt_ref, raw_ref)}
    )
    with pytest.raises(DigestionError):
        verify(
            ledger,
            store,
            job,
            step,
            state.plan_ref,
            state.requests[0],
            step.manifest[0],
            cp,
        )
    assert len(state.calls) == 4


def test_repeated_checkpoint_reuse_has_no_provider_calls(run):
    from documents.digestion.workflow import admit
    from documents.publication.planning import accepted

    state = run()
    ledger, store, job = reopen(state)
    original = accepted(ledger, store, job.admission.scope, job.job_id)[2]
    for i in range(3):
        job = admit(
            ledger,
            store,
            state.plan,
            state.plan_ref,
            request_key=f"resume-{i}",
            resume_from=job.job_id,
            retry=job.admission.profile.retry,
        )
        assert job.state == "COMPLETED"
        assert accepted(ledger, store, job.admission.scope, job.job_id)[2] == original
    assert state.calls == ["chunk", "structural", "root", "question"]


def test_manifest_commit_is_idempotent_and_fenced(run):
    from documents.jobs.errors import JobError
    from documents.jobs.models import Lease

    state = run()
    ledger, store, job = reopen(state)
    scope = job.admission.scope
    step = next(s for s in ledger.steps(scope, job.job_id) if len(s.manifest) == 3)
    attempt = ledger.attempts(scope, job.job_id, step.step_id)[0]
    lease = Lease(
        scope=scope,
        job_id=job.job_id,
        step_id=step.step_id,
        owner=attempt.worker,
        fence=attempt.fence,
    )
    original = [
        store.read(scope, r, max_bytes=job.admission.profile.max_artifact_bytes)
        for r in step.manifest
    ]
    assert ledger.commit(lease, step.manifest).manifest == step.manifest
    with pytest.raises(JobError, match="stale_fence"):
        ledger.commit(
            lease.model_copy(update={"fence": lease.fence + 1}), step.manifest
        )
    assert [
        store.read(scope, r, max_bytes=job.admission.profile.max_artifact_bytes)
        for r in step.manifest
    ] == original
    assert len(state.calls) == 4


@pytest.mark.parametrize("position", [0, 1, 2])
def test_corrupted_artifact_hash_is_rejected(run, position):
    from documents.digestion.codec import read
    from documents.digestion.models import Checkpoint
    from documents.digestion.receipts import verify
    from documents.errors import DocumentError

    state = run()
    ledger, store, job = reopen(state)
    scope, limit = job.admission.scope, job.admission.profile.max_artifact_bytes
    step = next(s for s in ledger.steps(scope, job.job_id) if len(s.manifest) == 3)
    cp = read(store, scope, step.manifest[0], Checkpoint, limit)
    values = list(step.manifest)
    values[position] = values[position].model_copy(update={"sha256": "0" * 64})
    altered = step.model_copy(update={"manifest": tuple(values)})
    if position == 0:
        with pytest.raises(DocumentError):
            store.inspect(scope, values[0], max_bytes=limit)
    else:
        with pytest.raises(DocumentError):
            verify(
                ledger,
                store,
                job,
                altered,
                state.plan_ref,
                state.requests[0],
                step.manifest[0],
                cp,
            )
    assert len(state.calls) == 4


def test_version_change_cannot_execute_or_reuse_accepted_checkpoints(run):
    from documents.digestion.managed import (
        ManagedDigestionHandler,
        ManagedSynthesisInference,
    )
    from documents.digestion.models import DigestionError
    from documents.digestion.workflow import admit, prepare

    state = run()
    ledger, store, job = reopen(state)
    original = state.handler.inference
    other = (
        "managed-prompt/11"
        if state.plan.profile.prompt_profile == "managed-prompt/10"
        else "managed-prompt/10"
    )
    settings = original.settings.model_copy(
        update={
            "profiles": tuple(
                p.model_copy(update={"template_version": other})
                for p in original.settings.profiles
            )
        }
    )
    inference = ManagedSynthesisInference(
        original.provider, settings, original.admission
    )
    assert inference.config != original.config
    wrong = ManagedDigestionHandler(ledger, state.plan_ref, inference)
    step = next(
        s for s in ledger.steps(job.admission.scope, job.job_id) if len(s.manifest) == 3
    )
    with pytest.raises(DigestionError, match="incompatible_checkpoint"):
        wrong(job, step, store)
    plan, ref = prepare(
        state.artifact,
        state.plan.structure.extraction,
        inference.profile(state.plan.profile),
        store,
    )
    resumed = admit(
        ledger,
        store,
        plan,
        ref,
        request_key="cross-version",
        resume_from=job.job_id,
        retry=job.admission.profile.retry,
    )
    # The general reprocessing API permits a new queued job, but transfers no
    # checkpoint authority across the incompatible generation. Do not run it.
    assert resumed.state == "QUEUED"
    assert all(
        not s.manifest and s.reused_from is None and s.attempt_count == 0
        for s in ledger.steps(job.admission.scope, resumed.job_id)
    )
    assert state.calls == ["chunk", "structural", "root", "question"]


def test_original_v5_wrapper_shape_remains_admissible_without_budget_expansion(run):
    from documents.digestion.codec import encode, read
    from documents.digestion.models import Checkpoint, ChildInput
    from documents.digestion.sizing import child_contribution, result_contribution
    from documents.jobs.models import canonical
    from tests.generation_wire_fixtures import proposal
    from tests.reducer_sizing_fixtures import eight_claim_result

    def witness(raw, stage):
        if stage not in ("structural", "root"):
            return raw
        request = run.state.requests[-1]
        result = eight_claim_result(request, canonical_bytes=4783)
        assert len(encode(result)) == 4783
        assert result_contribution(result) + 1024 == 7271
        return canonical(proposal(request, result))

    state = run(witness)
    assert state.result["job_state"] == "COMPLETED" and state.result["calls"] == 4
    ledger, store, job = reopen(state)
    for step in ledger.steps(job.admission.scope, job.job_id):
        if len(step.manifest) != 3:
            continue
        cp = read(store, job.admission.scope, step.manifest[0], Checkpoint, 32000000)
        if cp.result.kind != "reduction":
            continue
        child = ChildInput(
            artifact=step.manifest[0].model_copy(update={"byte_size": 32000000}),
            result=cp.result,
            inherited=cp.inherited,
        )
        assert child_contribution(child) == 6867
        assert state.plan.profile.managed_input_budget.child_bytes == 7000


@pytest.mark.parametrize("stage,count", [("chunk", 1), ("structural", 2), ("root", 3)])
def test_output_limit_is_terminal_without_retry_or_downstream_calls(
    run, monkeypatch, stage, count
):
    from tests.unit.test_structured_provider import Response

    original = foundry_preflight.OfflineHTTP.response

    def response(http, sent, result, current):
        if current == stage:
            return Response(
                {
                    "model": "offline-model",
                    "choices": [
                        {
                            "message": {"content": "Incomplete proposal"},
                            "finish_reason": "length",
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 30,
                        "completion_tokens": 40,
                        "total_tokens": 70,
                    },
                }
            )
        return original(http, sent, result, current)

    monkeypatch.setattr(foundry_preflight.OfflineHTTP, "response", response)
    state = run()
    assert state.result["job_state"] == "FAILED"
    assert state.result["terminal_category"] == "inference_output_limit"
    assert state.result["calls"] == count
    assert "publication" not in state.result and "questions" not in state.result
    assert all(r["state"] == "SETTLED" for r in state.result["governance_records"])
    ledger, _, job = reopen(state)
    failed = [
        s for s in ledger.steps(job.admission.scope, job.job_id) if s.state == "FAILED"
    ]
    assert len(failed) == 1 and failed[0].attempt_count == 1 and not failed[0].manifest
