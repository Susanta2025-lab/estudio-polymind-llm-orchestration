"""G2 rejects mixed hierarchy levels independently of correct current identity."""

import json
from uuid import UUID

import pytest

# Frozen canonical-output v9 characterization; v10 has separate wire regressions.
pytestmark = pytest.mark.usefixtures("managed_v9")

from jsonschema import Draft202012Validator

from documents.digestion.codec import decode, encode
from documents.digestion.managed import classify_managed
from documents.digestion.models import ClaimLink, DigestionError, StageResult
from documents.digestion.validation import EvidenceIndex, validate_result
from documents.digestion.workflow import DigestionHandler
from documents.models import stable_id
from tests.integration.test_managed_prompt8_contract import LINEAGE_V8
from tests.reducer_sizing_fixtures import eight_claim_result
from tests.unit.documents.test_claim_stage_identity import (
    stage_case as stage_case,  # noqa: PLC0414
)
from tests.unit.documents.test_managed_sizing import checkpoint, plain_result, setup


def test_exact_direct_links_and_empty_chunk_authority(stage_case):
    _, request, result, index, generation = stage_case
    control = json.loads(generation.system.split("\nCONTROL\n")[1])
    assert LINEAGE_V8 in generation.system
    expected = {
        (str(c.result.stage_id), str(claim.claim_id))
        for c in request.children
        for claim in c.result.claims
    }
    assert expected == {
        (v["stage_id"], v["claim_id"]) for v in control["required_child_links"]
    }
    assert validate_result(encode(result), request, index) == result
    assert bool(expected) == (request.stage == "reduction")
    for child in request.children:
        # Earlier links are visible in child material, but are not direct authority.
        earlier = {
            (str(l.stage_id), str(l.claim_id))
            for c in child.result.claims
            for l in c.lineage
        }
        assert not earlier & expected


@pytest.mark.parametrize("fault", ["wrong_claim", "wrong_stage", "duplicate"])
def test_valid_source_and_identity_do_not_authorize_bad_child_pairs(stage_case, fault):
    _, request, result, index, generation = stage_case
    payload = result.model_dump(mode="json")
    claim = payload["claims"][0]
    if request.children:
        link = dict(claim["lineage"][0])
    else:
        link = {"stage_id": str(UUID(int=99)), "claim_id": str(UUID(int=100))}
    if fault == "wrong_claim":
        link["claim_id"] = str(stable_id(str(UUID(int=99)), "0"))
    elif fault == "wrong_stage":
        link["stage_id"] = str(UUID(int=99))
    claim["lineage"] = [link, link] if fault == "duplicate" else [link]
    raw = encode(StageResult.model_validate(payload))
    Draft202012Validator(generation.schema).validate(payload)
    assert decode(
        raw, StageResult, request.profile.response_byte_limit
    ) == StageResult.model_validate(payload)
    before = [encode(c) for c in request.children]
    with pytest.raises(DigestionError) as caught:
        validate_result(raw, request, index)
    assert caught.value.validation_reason.value == (
        "duplicate_child_link" if fault == "duplicate" else "invalid_child_link"
    )
    assert caught.value.category == "evidence_validation_failed"
    assert classify_managed(caught.value).classification == "NON_RETRYABLE"
    assert classify_managed(caught.value).category == "invalid_reference"
    assert [encode(c) for c in request.children] == before
    assert encode(StageResult.model_validate(payload)) == raw


@pytest.fixture(params=["intermediate", "structural", "root"])
def reducer_case(tmp_path, request):
    store, artifact, inference, plan = setup(
        tmp_path, bounded=True, chunk_characters=3200
    )
    index, cps, refs = EvidenceIndex(artifact), {}, {}
    target = plan.root_id if request.param == "root" else plan.reducers[0].stage_id
    for node in (*plan.chunks, *plan.reducers):
        key = getattr(node, "chunk_id", None) or node.stage_id
        current = DigestionHandler.request(plan, key, cps, refs)
        result = eight_claim_result(current)
        assert validate_result(encode(result), current, index) == result
        if key == target:
            generation, _ = inference.bind(None, request.param).render(current)
            return current, result, index, generation
        checkpoint(store, plan, current, result, cps, refs)
    raise AssertionError("Missing reducer")


def test_missing_one_required_link_is_not_repaired(reducer_case):
    request, result, index, _ = reducer_case
    first = result.claims[0].model_copy(update={"lineage": ()})
    bad = result.model_copy(update={"claims": (first, *result.claims[1:])})
    with pytest.raises(DigestionError) as caught:
        validate_result(encode(bad), request, index)
    assert caught.value.validation_reason.value == "missing_child_coverage"
    assert classify_managed(caught.value).classification == "NON_RETRYABLE"


def test_all_eight_correct_child_stages_with_earlier_claim_ids_are_rejected(
    reducer_case,
):
    request, result, index, generation = reducer_case
    child = request.children[0].result
    # At root these are actual grandchild IDs read from the accepted first reducer.
    # At the first reducer synthetic earlier IDs demonstrate the same membership rule.
    earlier = tuple(l.claim_id for c in child.claims for l in c.lineage) or tuple(
        stable_id(str(UUID(int=99)), str(i)) for i in range(8)
    )
    assert len(earlier) == 8
    bad = result.model_copy(
        update={
            "claims": tuple(
                c.model_copy(
                    update={
                        "lineage": (
                            ClaimLink(stage_id=child.stage_id, claim_id=earlier[i]),
                        )
                    }
                )
                for i, c in enumerate(result.claims)
            )
        }
    )
    assert all(
        c.originating_stage == request.stage_id
        and c.claim_id == stable_id(str(request.stage_id), str(i))
        for i, c in enumerate(bad.claims)
    )
    allowed = {
        (v["stage_id"], v["claim_id"])
        for v in json.loads(generation.system.split("\nCONTROL\n")[1])[
            "required_child_links"
        ]
    }
    assert all(
        (str(l.stage_id), str(l.claim_id)) not in allowed
        for c in bad.claims
        for l in c.lineage
    )
    with pytest.raises(DigestionError) as caught:
        validate_result(encode(bad), request, index)
    assert caught.value.validation_reason.value == "invalid_child_link"


@pytest.mark.parametrize("stage", ["intermediate", "structural", "root"])
def test_cross_child_pair_mixing_fails_even_when_each_identifier_is_authorized(
    tmp_path, stage
):
    store, artifact, inference, plan = setup(
        tmp_path, bounded=True, chunk_characters=800
    )
    index, cps, refs = EvidenceIndex(artifact), {}, {}
    assert len(plan.chunks) == 2
    for chunk in plan.chunks:
        current = DigestionHandler.request(plan, chunk.chunk_id, cps, refs)
        result, _ = plain_result(current, index)
        checkpoint(store, plan, current, result, cps, refs)
    current = DigestionHandler.request(plan, plan.reducers[0].stage_id, cps, refs)
    generation, _ = inference.bind(None, stage).render(current)
    valid, _ = plain_result(current, index)
    assert validate_result(encode(valid), current, index) == valid
    a, b = current.children
    mixed = ClaimLink(stage_id=a.result.stage_id, claim_id=b.result.claims[0].claim_id)
    claim = valid.claims[0].model_copy(
        update={"lineage": (mixed, *valid.claims[0].lineage)}
    )
    bad = valid.model_copy(update={"claims": (claim, *valid.claims[1:])})
    control = json.loads(generation.system.split("\nCONTROL\n")[1])
    assert str(mixed.stage_id) in {
        v["stage_id"] for v in control["required_child_links"]
    }
    assert str(mixed.claim_id) in {
        v["claim_id"] for v in control["required_child_links"]
    }
    with pytest.raises(DigestionError) as caught:
        validate_result(encode(bad), current, index)
    assert caught.value.validation_reason.value == "invalid_child_link"
