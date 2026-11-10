"""Current generation identity is separate from immutable source lineage."""

import json
from uuid import UUID

import pytest

# Frozen canonical-output v9 characterization; v10 has separate wire regressions.
pytestmark = pytest.mark.usefixtures("managed_v9")

from jsonschema import Draft202012Validator

from documents.digestion.codec import encode
from documents.digestion.models import DigestionError
from documents.digestion.validation import EvidenceIndex, validate_result
from documents.digestion.workflow import DigestionHandler
from documents.models import stable_id
from tests.integration.test_final_offline_azure_compatibility import schema_source_ids
from tests.reducer_sizing_fixtures import eight_claim_result
from tests.unit.documents.test_managed_sizing import checkpoint, setup


@pytest.fixture(params=["chunk", "intermediate", "structural", "root"])
def stage_case(tmp_path, request):
    stage = request.param
    store, artifact, inference, plan = setup(
        tmp_path, bounded=True, chunk_characters=3200
    )
    index, cps, refs = EvidenceIndex(artifact), {}, {}
    target = {
        "chunk": plan.chunks[0].chunk_id,
        "intermediate": plan.reducers[0].stage_id,
        "structural": plan.reducers[0].stage_id,
        "root": plan.root_id,
    }[stage]
    for node in (*plan.chunks, *plan.reducers):
        key = getattr(node, "chunk_id", None) or node.stage_id
        current = DigestionHandler.request(plan, key, cps, refs)
        result = eight_claim_result(current)
        assert validate_result(encode(result), current, index) == result
        if key == target:
            generation, _ = inference.bind(None, stage).render(current)
            return stage, current, result, index, generation
        checkpoint(store, plan, current, result, cps, refs)
    raise AssertionError("Missing synthesis stage")


def test_current_stage_identity_and_rendered_control_are_consistent(stage_case):
    stage, request, result, index, generation = stage_case
    control = json.loads(generation.system.split("\nCONTROL\n")[1])
    assert control["profile"]["stage"] == stage
    assert control["kind"] == request.stage
    assert control["stage_id"] == str(request.stage_id)
    assert (
        "Use CONTROL.claim_ids_in_order consecutively for this response."
        in generation.system
    )
    assert (
        "every claims[i].originating_stage to the current CONTROL.stage_id"
        in generation.system
    )
    assert "including claims that restate child findings" in generation.system
    assert (
        "Copy source-stage identities only into lineage using CONTROL.required_child_links"
        in generation.system
    )
    assert (
        "never copy a child's originating_stage into a new claim" in generation.system
    )
    assert "Claim/stage IDs are not source IDs" in generation.system
    assert control["profile"]["template_version"] == "managed-prompt/9"
    child_bytes = [encode(child) for child in request.children]
    assert validate_result(encode(result), request, index) == result
    for i, claim in enumerate(result.claims):
        assert claim.originating_stage == request.stage_id
        assert claim.claim_id == stable_id(str(request.stage_id), str(i))
        assert str(claim.claim_id) == control["claim_ids_in_order"][i]
    if request.children:
        links = {
            (str(child.result.stage_id), str(c.claim_id))
            for child in request.children
            for c in child.result.claims
        }
        assert links == {
            (v["stage_id"], v["claim_id"]) for v in control["required_child_links"]
        }
        assert all(
            child.result.stage_id != request.stage_id for child in request.children
        )
        assert all(
            c.originating_stage == child.result.stage_id
            for child in request.children
            for c in child.result.claims
        )
        assert all(
            link.stage_id != request.stage_id
            for c in result.claims
            for link in c.lineage
        )
    assert child_bytes == [encode(child) for child in request.children]


@pytest.mark.parametrize("positions", [(0,), (7,), tuple(range(8))])
def test_correct_ids_and_valid_evidence_cannot_mask_incorrect_origin(
    stage_case, positions
):
    _, request, result, index, generation = stage_case
    payload = result.model_dump(mode="json")
    wrong_stage = (
        request.children[0].result.stage_id if request.children else UUID(int=99)
    )
    for position in positions:
        payload["claims"][position]["originating_stage"] = str(wrong_stage)
    # Shape/schema compliance cannot express the cross-field identity predicate.
    Draft202012Validator(generation.schema).validate(payload)
    raw = json.dumps(payload).encode()
    original = encode(result)
    children = [encode(c) for c in request.children]
    allowed = set(schema_source_ids(generation.schema))
    assert all(set(c["evidence_ids"]) <= allowed for c in payload["claims"])
    assert all(
        c["claim_id"] == str(stable_id(str(request.stage_id), str(i)))
        for i, c in enumerate(payload["claims"])
    )
    with pytest.raises(DigestionError) as caught:
        validate_result(raw, request, index)
    assert caught.value.category == "inference_contract_error"
    assert caught.value.validation_diagnostic.value == "claim_identity"
    assert caught.value.validation_reason.value == "originating_stage_mismatch"
    assert json.loads(raw) == payload and encode(result) == original
    assert [encode(c) for c in request.children] == children


def test_claim_ids_remain_bound_to_current_stage_even_with_correct_origin(stage_case):
    _, request, result, index, _ = stage_case
    payload = result.model_dump(mode="json")
    payload["claims"][0]["claim_id"] = str(stable_id(str(UUID(int=99)), "0"))
    with pytest.raises(DigestionError) as caught:
        validate_result(json.dumps(payload).encode(), request, index)
    assert caught.value.validation_reason.value == "claim_id_mismatch"


def test_profile_names_are_not_originating_stage_values(stage_case):
    stage, request, result, index, _ = stage_case
    payload = result.model_dump(mode="json")
    payload["claims"][0]["originating_stage"] = stage
    with pytest.raises(DigestionError) as caught:
        validate_result(json.dumps(payload).encode(), request, index)
    assert caught.value.validation_diagnostic.value == "pydantic_validation"
