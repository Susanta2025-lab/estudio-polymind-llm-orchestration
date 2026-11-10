"""Unchanged provider output is rejected before checkpoint/publication boundaries."""

import json

import pytest

# Frozen canonical-output v9 characterization; v10 has separate wire regressions.
pytestmark = pytest.mark.usefixtures("managed_v9")

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


def test_eight_claim_root_completes_all_four_calls_with_exact_lineage(
    l1, record_property
):
    state = l1(sized_transform(l1, 6867, "root"))
    jobs, store, scope, digest = reopen(state)
    assert_accounting(state, 4)
    assert digest.status == "COMPLETE" and digest.coverage.fraction == 1
    assert len(digest.synthesis_claims) == 8 and len(digest.evidence) == 4
    assert {q.text for q in digest.qualifications} == {"Synthetic qualification."}
    assert len(digest.contradictions) == 1
    assert digest.contradictions[0].resolution == "unresolved"
    assert state.result["publication"]["citations"] == 8
    assert state.result["questions"]["status"] == "COMPLETE"
    assert state.replica.ready()
    rows = []
    for request, generation, call in zip(
        state.requests, state.generations[:3], state.http.calls[:3], strict=True
    ):
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
        assert (
            validate_result(
                call["response"].encode(), request, EvidenceIndex(state.artifact)
            )
            == cp.result
        )
        assert cp.result == validate_result(
            encode(cp.result), request, EvidenceIndex(state.artifact)
        )
        assert len(cp.result.claims) == 8
        assert {
            (l.stage_id, l.claim_id) for c in cp.result.claims for l in c.lineage
        } == {
            (child.result.stage_id, c.claim_id)
            for child in request.children
            for c in child.result.claims
        }
        from documents.digestion.models import ChildInput
        from documents.digestion.sizing import child_contribution
        from documents.jobs.models import canonical

        material = ChildInput(
            artifact=step.manifest[0].model_copy(
                update={"byte_size": request.profile.max_artifact_bytes}
            ),
            result=cp.result,
            inherited=cp.inherited,
        )
        actual = len(
            canonical(
                {
                    "system": generation.system,
                    "data": generation.data,
                    "schema": generation.schema,
                }
            ).encode()
        )
        complete_context = (
            actual
            + generation.capability.overhead_tokens
            + generation.capability.safety_tokens
            + generation.output_tokens
        )
        assert actual <= 24800 and complete_context <= 28000
        assert (
            len(call["response"].encode()) <= 10000 and len(encode(cp.result)) <= 10000
        )
        assert child_contribution(material) <= 7000
        rows.append(
            {
                "stage": str(request.stage_id),
                "input": actual,
                "context": complete_context,
                "raw": len(call["response"].encode()),
                "canonical": len(encode(cp.result)),
                "child": child_contribution(material),
            }
        )
    record_property("eight_claim_workflow_sizing", json.dumps(rows))
    # Citation construction resolves original source offsets, never claim UUIDs.
    packet = json.loads((state.root / "review-packets.json").read_text())[0]
    for citation in packet["response"]["citations"]:
        unit = next(
            u
            for u in state.artifact.units
            if u.physical_page == citation["physical_page"]
        )
        assert (
            citation["excerpt"]
            == unit.text[citation["span"]["start"] : citation["span"]["end"]]
        )
        assert citation["provenance"] == "validated"
    assert len(state.sent) == 4


@pytest.mark.parametrize("stage,calls", [("structural", 2), ("root", 3)])
@pytest.mark.parametrize(
    "fault", ["earlier_claims", "wrong_stage", "missing", "duplicate"]
)
def test_invalid_direct_lineage_preserves_prior_checkpoints_and_settled_usage(
    l1, stage, calls, fault
):
    sized = sized_transform(l1, 6867, stage)
    previous, rejected = [], []

    def transform(value, current):
        value = sized(value, current)
        if current != stage:
            return value
        request = l1.state.requests[-1]
        payload = json.loads(value)
        assert len(payload["claims"]) == 8
        child = request.children[0].result
        earlier = tuple(l.claim_id for c in child.claims for l in c.lineage)
        if not earlier:
            # No grandchild exists at the first reducer; wrong next-level IDs
            # still demonstrate the strict exact-pair boundary.
            earlier = tuple(stable_id(str(request.stage_id), str(i)) for i in range(8))
        for i, claim in enumerate(payload["claims"]):
            assert claim["claim_id"] == str(stable_id(str(request.stage_id), str(i)))
            assert claim["originating_stage"] == str(request.stage_id)
            if fault == "earlier_claims":
                claim["lineage"] = [
                    {"stage_id": str(child.stage_id), "claim_id": str(earlier[i])}
                ]
            elif fault == "wrong_stage":
                claim["lineage"][0]["stage_id"] = str(request.stage_id)
            elif fault == "duplicate" and i == 0:
                claim["lineage"].append(dict(claim["lineage"][0]))
            elif fault == "missing":
                claim["lineage"] = []
        for step in l1.state.jobs.steps(
            l1.state.artifact.document.scope, l1.state.job.job_id
        ):
            if step.state == "SUCCEEDED":
                previous.extend(
                    (
                        ref,
                        l1.state.store.read(
                            ref.scope, ref, max_bytes=request.profile.max_artifact_bytes
                        ),
                    )
                    for ref in step.manifest
                )
        # Raw whitespace is removed solely in this synthetic transport fixture
        # to keep byte sizing independent of the lineage fault.
        value = json.dumps(payload, separators=(",", ":"))
        rejected.append(value)
        return value

    state = l1(transform)
    assert state.result["job_state"] == "FAILED"
    expected = {
        "earlier_claims": "invalid_child_link",
        "wrong_stage": "invalid_child_link",
        "duplicate": "duplicate_child_link",
        "missing": "missing_child_coverage",
    }[fault]
    assert state.errors[-1].validation_reason.value == expected
    assert state.result["terminal_category"] == (
        "extraction_failed" if fault == "missing" else "invalid_reference"
    )
    assert_accounting(state, calls)
    assert "publication" not in state.result and "questions" not in state.result
    assert not hasattr(state, "replica")
    assert state.result["provider_records"][-1]["response"] == rejected[0]
    assert all(r["outcome"] == "success" for r in state.result["provider_records"])
    scope = state.artifact.document.scope
    jobs, store = (
        SQLiteJobLedger(state.jobs.settings),
        LocalObjectStore(state.root / "objects"),
    )
    steps = jobs.steps(scope, state.job.job_id)
    (failed,) = [s for s in steps if s.state == "FAILED"]
    assert failed.attempt_count == 1 and not failed.manifest
    (attempt,) = jobs.attempts(scope, state.job.job_id, failed.step_id)
    assert attempt.classification == "NON_RETRYABLE"
    assert all(
        s.attempt_count == 0 and not s.manifest for s in steps if s.state == "CANCELLED"
    )
    for ref, original in previous:
        assert (
            store.read(scope, ref, max_bytes=state.plan.profile.max_artifact_bytes)
            == original
        )
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
        assert cp.inherited.qualifications > 0 and cp.inherited.contradictions == 1
    with pytest.raises(DigestionError):
        reopen(state)
