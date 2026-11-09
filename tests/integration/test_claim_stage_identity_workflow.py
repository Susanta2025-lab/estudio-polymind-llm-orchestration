"""Synthetic identity faults fail before commit and preserve settled usage."""

import json
from uuid import UUID

import pytest
from test_phase17hl_offline_e2e import assert_accounting, reopen
from test_phase17hl_offline_e2e import l1 as l1  # noqa: PLC0414
from test_phase17hl_offline_e2e import offline as offline  # noqa: PLC0414
from test_reducer_sizing_offline_workflow import sized_transform

from documents.digestion.codec import encode, read
from documents.digestion.models import Checkpoint, DigestionError
from documents.digestion.validation import EvidenceIndex, validate_result
from documents.jobs.sqlite import SQLiteJobLedger
from documents.models import stable_id
from documents.storage import LocalObjectStore


def test_valid_stage_identity_keeps_source_qualifications_through_publication(l1):
    state = l1(sized_transform(l1, 6867))
    jobs, store, scope, digest = reopen(state)
    assert_accounting(state, 4)
    assert digest.status == "COMPLETE"
    assert len(digest.qualifications) == 2
    assert {q.text for q in digest.qualifications} == {"Synthetic qualification."}
    assert len(digest.contradictions) == 1
    assert digest.contradictions[0].resolution == "unresolved"
    assert len(digest.evidence) == 4
    for request in state.requests:
        step = next(
            s
            for s in jobs.steps(scope, state.job.job_id)
            if s.spec.unit_id == str(request.stage_id)
        )
        cp = read(
            store,
            scope,
            step.manifest[0],
            Checkpoint,
            request.profile.max_artifact_bytes,
        )
        assert all(c.originating_stage == request.stage_id for c in cp.result.claims)
        assert all(
            c.claim_id == stable_id(str(request.stage_id), str(i))
            for i, c in enumerate(cp.result.claims)
        )
        assert cp.inherited.contradictions == 1
        if request.children:
            assert cp.inherited.qualifications >= sum(
                c.inherited.qualifications for c in request.children
            )
            assert {
                (link.stage_id, link.claim_id)
                for c in cp.result.claims
                for link in c.lineage
            } == {
                (c.result.stage_id, claim.claim_id)
                for c in request.children
                for claim in c.result.claims
            }
    assert state.result["questions"]["status"] == "COMPLETE"
    assert state.result["publication"]["citations"] == 8
    assert state.replica.ready()
    qa_data = json.loads(state.generations[-1].data)
    assert (
        qa_data["DERIVED_RETRIEVAL_MATERIAL"][0]["contradictions"][0]["resolution"]
        == "unresolved"
    )


@pytest.mark.parametrize("stage,calls", [("chunk", 1), ("structural", 2), ("root", 3)])
@pytest.mark.parametrize("positions", [(0,), (7,), tuple(range(8))])
def test_identity_fault_never_commits_or_publishes_and_keeps_prior_usage(
    l1, stage, calls, positions
):
    sized = sized_transform(l1, 6867, stage)
    previous = []
    rejected = []

    def transform(value, current):
        value = sized(value, current)
        if current == stage:
            request = l1.state.requests[-1]
            wrong = (
                request.children[0].result.stage_id
                if request.children
                else UUID(int=99)
            )
            payload = json.loads(value)
            assert len(payload["claims"]) == 8
            assert all(
                c["claim_id"] == str(stable_id(str(request.stage_id), str(i)))
                for i, c in enumerate(payload["claims"])
            )
            for i in positions:
                payload["claims"][i]["originating_stage"] = str(wrong)
            for step in l1.state.jobs.steps(
                l1.state.artifact.document.scope, l1.state.job.job_id
            ):
                if step.state == "SUCCEEDED":
                    previous.append((step.step_id, step.manifest))
            value = json.dumps(payload)
            rejected.append(value)
        return value

    state = l1(transform)
    assert state.result["job_state"] == "FAILED"
    assert state.result["terminal_category"] == "serialization_error"
    assert state.errors[-1].category == "inference_contract_error"
    assert state.errors[-1].validation_reason.value == "originating_stage_mismatch"
    assert_accounting(state, calls)
    assert "publication" not in state.result and "questions" not in state.result
    assert not hasattr(state, "replica")
    assert state.result["provider_records"][-1]["response"] == rejected[0]
    assert all(r["outcome"] == "success" for r in state.result["provider_records"])
    scope = state.artifact.document.scope
    jobs = SQLiteJobLedger(state.jobs.settings)
    store = LocalObjectStore(state.root / "objects")
    steps = jobs.steps(scope, state.job.job_id)
    (failed,) = [s for s in steps if s.state == "FAILED"]
    assert failed.attempt_count == 1 and not failed.manifest
    (attempt,) = jobs.attempts(scope, state.job.job_id, failed.step_id)
    assert attempt.classification == "NON_RETRYABLE"
    assert all(
        s.attempt_count == 0 and not s.manifest for s in steps if s.state == "CANCELLED"
    )
    for step_id, manifest in previous:
        saved = next(s for s in steps if s.step_id == step_id)
        assert saved.state == "SUCCEEDED" and saved.manifest == manifest
        for ref in manifest:
            store.inspect(scope, ref, max_bytes=state.plan.profile.max_artifact_bytes)
    for request in state.requests[:-1]:
        saved = next(s for s in steps if s.spec.unit_id == str(request.stage_id))
        cp = read(
            store,
            scope,
            saved.manifest[0],
            Checkpoint,
            request.profile.max_artifact_bytes,
        )
        assert (
            validate_result(encode(cp.result), request, EvidenceIndex(state.artifact))
            == cp.result
        )
        assert cp.inherited.qualifications > 0
        assert cp.inherited.contradictions == 1
    with pytest.raises(DigestionError):
        reopen(state)
