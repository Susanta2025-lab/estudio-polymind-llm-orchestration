"""Strict four-call L1 rehearsal at the measured child-material boundary."""

import json
from hashlib import sha256
from pathlib import Path
from types import SimpleNamespace

import pytest
from test_phase17hl_offline_e2e import assert_accounting, reopen
from test_phase17hl_offline_e2e import l1 as l1  # noqa: PLC0414
from test_phase17hl_offline_e2e import offline as offline  # noqa: PLC0414

from documents.digestion.codec import encode, read
from documents.digestion.managed import StageProfile
from documents.digestion.models import Checkpoint, ChildInput, DigestionError
from documents.digestion.sizing import (
    child_contribution,
    reduction_size,
    result_contribution,
)
from documents.digestion.validation import inherited_summary
from documents.jobs.models import canonical
from tests.performance.foundry_l1 import LaunchConfiguration, generation_contract_digest
from tests.reducer_sizing_fixtures import eight_claim_result


def material(state, result):
    request = state.requests[-1]
    children = tuple(
        read(
            state.store,
            child.artifact.scope,
            child.artifact,
            Checkpoint,
            request.profile.max_artifact_bytes,
        )
        for child in request.children
    )
    inherited, _ = inherited_summary(result, request, children)
    return ChildInput(
        artifact=state.plan_ref.model_copy(
            update={"byte_size": request.profile.max_artifact_bytes}
        ),
        result=result,
        inherited=inherited,
    )


def sized_transform(l1, target, stage="structural"):
    def transform(value, current):
        if current == "chunk":
            result = eight_claim_result(l1.state.requests[-1])
        elif current == stage or current == "structural" and stage == "root":
            result = eight_claim_result(l1.state.requests[-1], canonical_bytes=4783)
        else:
            return value
        if current == stage:
            contribution = child_contribution(material(l1.state, result))
            result = eight_claim_result(
                l1.state.requests[-1],
                canonical_bytes=len(encode(result)) + target - contribution,
            )
            assert child_contribution(material(l1.state, result)) == target
        return encode(result).decode("ascii")

    return transform


@pytest.mark.parametrize("target", [6867, 6999, 7000])
def test_four_call_completion_publication_retrieval_and_qa_at_boundary(
    l1, target, record_property, monkeypatch
):
    from documents.digestion import workflow

    accepted_material = []
    original_validate = workflow.validate_child_material

    def validate(*args):
        original_validate(*args)
        accepted_material.append(args[0].stage_id)

    monkeypatch.setattr(workflow, "validate_child_material", validate)
    state = l1(sized_transform(l1, target))
    assert (
        state.result["mode"] == "OFFLINE ONLY" and state.result["billable_calls"] == 0
    )
    assert [c["stage"] for c in state.http.calls] == [
        "chunk",
        "structural",
        "root",
        "question",
    ]
    assert_accounting(state, 4)
    jobs, store, scope, digest = reopen(state)
    assert digest.status == "COMPLETE" and digest.coverage.fraction == 1
    assert state.result["questions"]["status"] == "COMPLETE"
    assert state.result["publication"]["citations"] == 8 and state.replica.ready()
    assert {q.text for q in digest.qualifications} == {"Synthetic qualification."}
    (conflict,) = digest.contradictions
    assert (
        conflict.subject == "synthetic-access" and conflict.resolution == "unresolved"
    )
    assert len(digest.evidence) == 4
    rows = []
    for request, generation, step in zip(
        state.requests,
        state.generations[:3],
        jobs.steps(scope, state.job.job_id)[1:4],
        strict=True,
    ):
        cp = read(
            store,
            scope,
            step.manifest[0],
            Checkpoint,
            request.profile.max_artifact_bytes,
        )
        measured = child_contribution(
            ChildInput(
                artifact=step.manifest[0].model_copy(
                    update={"byte_size": request.profile.max_artifact_bytes}
                ),
                result=cp.result,
                inherited=cp.inherited,
            )
        )
        assert measured <= 7000
        actual = len(
            canonical(
                {
                    "system": generation.system,
                    "data": generation.data,
                    "schema": generation.schema,
                }
            ).encode("ascii")
        )
        assert actual <= 24800
        cap = generation.capability
        assert (
            actual + cap.overhead_tokens + cap.safety_tokens + generation.output_tokens
            <= 28000
        )
        assert generation.output_tokens == 3000
        assert len(encode(cp.result)) <= 10000
        assert (
            len(state.http.calls[len(rows)]["response"].encode("utf-8"))
            <= generation.response_bytes
            == 10000
        )
        assert accepted_material.count(request.stage_id) >= 2
        if request.children:
            node = next(
                n for n in state.plan.reducers if n.stage_id == request.stage_id
            )
            assert (
                actual
                <= node.estimated_tokens
                == reduction_size(
                    state.plan.profile, request.structural_path, len(request.children)
                )
            )
            assert {
                link.claim_id for claim in cp.result.claims for link in claim.lineage
            } == {
                claim.claim_id
                for child in request.children
                for claim in child.result.claims
            }
            planned = node.estimated_tokens
        else:
            planned = next(
                c.estimated_tokens
                for c in state.plan.chunks
                if c.chunk_id == request.stage_id
            )
            assert actual <= planned
        rows.append(
            {
                "kind": request.stage,
                "canonical": len(encode(cp.result)),
                "child": measured,
                "input": actual,
                "planned": planned,
                "reserved_output": generation.output_tokens,
            }
        )
        if request.stage_id == state.plan.reducers[0].stage_id:
            assert measured == target
            if target == 6867:
                assert len(encode(cp.result)) == 4783
                assert result_contribution(cp.result) + 1024 == 7271
    # Q&A has its own actual full-envelope context check and original evidence.
    qa = state.generations[-1]
    qa_output = len(state.http.calls[-1]["response"].encode("utf-8"))
    assert qa_output <= qa.response_bytes == 12000
    assert qa.output_tokens == 3000
    qa_input = len(
        canonical({"system": qa.system, "data": qa.data, "schema": qa.schema}).encode(
            "ascii"
        )
    )
    assert (
        qa_input
        + qa.capability.overhead_tokens
        + qa.capability.safety_tokens
        + qa.output_tokens
        <= 28000
    )
    qa_data = json.loads(qa.data)
    (annotations,) = qa_data["DERIVED_RETRIEVAL_MATERIAL"]
    assert annotations["contradictions"][0]["resolution"] == "unresolved"
    (packet,) = json.loads((state.root / "review-packets.json").read_text())
    citation = packet["response"]["citations"][0]
    assert citation["provenance"] == "validated"
    assert packet["response"]["answer"] == citation["excerpt"]
    assert all(s.state == "SUCCEEDED" for s in jobs.steps(scope, state.job.job_id))
    record_property("stage_bytes", json.dumps(rows, sort_keys=True))
    record_property("qa_input_bytes", qa_input)
    record_property("qa_output_utf8_bytes", qa_output)
    if target == 7000:
        from documents.digestion.managed import (
            ManagedDigestionHandler,
            classify_managed,
        )
        from documents.jobs.worker import LocalDispatcher, Worker, relay

        resumed = workflow.admit(
            jobs,
            store,
            state.plan,
            state.plan_ref,
            request_key="sizing-boundary-resume",
            resume_from=state.job.job_id,
            retry=state.job.admission.profile.retry,
        )
        queue = LocalDispatcher()
        worker = Worker(
            jobs,
            queue,
            store,
            ManagedDigestionHandler(jobs, state.plan_ref, state.handler.inference),
            owner="offline-sizing-resume",
            classifier=classify_managed,
        )
        for _ in range(state.plan.profile.max_steps):
            relay(jobs, queue)
            if not worker.once():
                break
        assert jobs.get_job(scope, resumed.job_id).state == "COMPLETED"
        assert workflow.load_digest(jobs, store, scope, resumed.job_id) == digest
        assert len(state.sent) == 4
        assert (
            state.handler.inference.governance.ledger.usage(
                state.principal, state.authority
            )
            == state.result["governance_records"]
        )


@pytest.mark.parametrize("stage,calls", [("chunk", 1), ("structural", 2), ("root", 3)])
def test_one_byte_incompatible_output_fails_before_checkpoint_without_retry(
    l1, stage, calls
):
    state = l1(sized_transform(l1, 7001, stage))
    assert state.result["job_state"] == "FAILED"
    assert state.result["terminal_category"] == "extraction_limit_exceeded"
    assert "publication" not in state.result and "questions" not in state.result
    assert_accounting(state, calls)
    steps = state.jobs.steps(state.artifact.document.scope, state.job.job_id)
    (failed,) = [s for s in steps if s.state == "FAILED"]
    assert failed.attempt_count == 1 and not failed.manifest
    (attempt,) = state.jobs.attempts(
        state.artifact.document.scope, state.job.job_id, failed.step_id
    )
    assert attempt.classification == "NON_RETRYABLE"
    assert (
        len([s for s in steps if s.state == "SUCCEEDED"]) == calls
    )  # Plan plus prior calls.
    assert all(
        s.attempt_count == 0 and not s.manifest for s in steps if s.state == "CANCELLED"
    )
    with pytest.raises(DigestionError):
        reopen(state)


@pytest.mark.parametrize(
    "old,template",
    [
        (
            "de9492c536c1435464e8d9e406cbd1491ea358bc45f817df72eb2ea2a0f69a71",
            "managed-prompt/5",
        ),
        (
            "f6e568d450ac084c5977e4fef68823fb457cceacd22b361f047310c5d3512f5b",
            "managed-prompt/6",
        ),
    ],
)
def test_new_contract_rejects_stale_generation_digest_and_prompt_version(old, template):
    assert generation_contract_digest() != old
    stale = SimpleNamespace(
        contract=None,
        policy=None,
        generation_contract_sha256=old,
        governance_policy=SimpleNamespace(evaluation=None),
    )
    with pytest.raises(ValueError, match="Reviewed generation contract"):
        LaunchConfiguration.bounded(stale)
    assert (
        StageProfile(
            stage="root", input_tokens=24800, output_tokens=3000
        ).template_version
        == "managed-prompt/7"
    )
    with pytest.raises(ValueError):
        StageProfile(
            stage="root",
            input_tokens=24800,
            output_tokens=3000,
            template_version=template,
        )


def test_generation_digest_binds_child_sizing_and_checkpoint_validation():
    root = Path(__file__).resolve().parents[2]
    paths = (
        "documents/digestion/managed.py",
        "documents/digestion/models.py",
        "documents/digestion/validation.py",
        "documents/digestion/planning.py",
        "documents/digestion/sizing.py",
        "documents/digestion/workflow.py",
        "documents/digestion/diagnostics.py",
        "documents/publication/analysis.py",
        "llm/structured.py",
        "llm/bounded_http.py",
        "llm/openai_compatible.py",
        "llm/azure_schema.py",
        "tests/performance/fixtures.py",
        "tests/performance/foundry_preflight.py",
        "tests/performance/foundry_recalibration.py",
    )
    hashes = {p: sha256((root / p).read_bytes()).hexdigest() for p in paths}
    assert (
        generation_contract_digest()
        == sha256(
            json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
    )


def test_original_sizing_shape_still_rejects_wrong_originating_stage(l1):
    sized = sized_transform(l1, 6867)

    def transform(value, stage):
        value = sized(value, stage)
        if stage == "structural":
            result = json.loads(value)
            parent = l1.state.requests[-1].children[0].result.stage_id
            for claim in result["claims"]:
                claim["originating_stage"] = str(parent)
            # UUID width is fixed: reproduce the secondary live failure without
            # changing the 4,783 / 7,271 / 6,867 sizing witness.
            from documents.digestion.models import StageResult

            output = StageResult.model_validate(result)
            assert len(encode(output)) == 4783
            assert result_contribution(output) + 1024 == 7271
            assert child_contribution(material(l1.state, output)) == 6867
            return encode(output).decode("ascii")
        return value

    state = l1(transform)
    assert state.result["job_state"] == "FAILED"
    assert state.result["terminal_category"] == "serialization_error"
    assert state.errors[-1].validation_reason.value == "originating_stage_mismatch"
    assert_accounting(state, 2)
    steps = state.jobs.steps(state.artifact.document.scope, state.job.job_id)
    (failed,) = [s for s in steps if s.state == "FAILED"]
    assert failed.attempt_count == 1 and not failed.manifest
    assert "publication" not in state.result and "questions" not in state.result
