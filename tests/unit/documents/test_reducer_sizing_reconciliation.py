"""Actual downstream material boundaries, independently of response byte limits."""

import json

import pytest

from documents.digestion.codec import encode
from documents.digestion.models import ChildInput, DigestionError, InheritedSummary
from documents.digestion.planning import check_request
from documents.digestion.sizing import (
    CHILD_WRAPPER_BYTES,
    child_contribution,
    escaped_size,
    reduction_size,
    result_contribution,
)
from documents.digestion.validation import (
    EvidenceIndex,
    inherited_summary,
    validate_child_material,
    validate_result,
)
from documents.digestion.workflow import DigestionHandler
from documents.jobs.models import canonical
from tests.reducer_sizing_fixtures import eight_claim_result
from tests.unit.documents.test_managed_sizing import checkpoint, setup


@pytest.fixture
def reducer(tmp_path):
    store, artifact, inference, plan = setup(
        tmp_path, bounded=True, chunk_characters=3200
    )
    index, cps, refs = EvidenceIndex(artifact), {}, {}
    leaf = DigestionHandler.request(plan, plan.chunks[0].chunk_id, cps, refs)
    result = eight_claim_result(leaf)
    validate_result(encode(result), leaf, index)
    checkpoint(store, plan, leaf, result, cps, refs)
    request = DigestionHandler.request(plan, plan.reducers[0].stage_id, cps, refs)
    return store, inference, plan, index, cps, refs, request


def material_for(result, request, cps, ref):
    inherited, _ = inherited_summary(
        result, request, tuple(cps[c.result.stage_id] for c in request.children)
    )
    return ChildInput(
        artifact=ref.model_copy(
            update={"byte_size": request.profile.max_artifact_bytes}
        ),
        result=result,
        inherited=inherited,
    )


def test_original_7271_witness_is_losslessly_admitted(reducer):
    _, inference, plan, index, cps, refs, request = reducer
    result = eight_claim_result(request, canonical_bytes=4783)
    material = material_for(result, request, cps, refs[plan.chunks[0].chunk_id])
    raw = encode(result)
    assert len(raw) == 4783
    assert escaped_size(result.model_dump(mode="json")) == 5193
    assert result_contribution(result) == 5193 + 881 + 165 + 8 == 6247
    assert result_contribution(result) + CHILD_WRAPPER_BYTES == 7271
    assert child_contribution(material) - result_contribution(result) == 620
    assert child_contribution(material) == 6867
    assert validate_result(raw, request, index) == result
    validate_child_material(
        result, material.inherited, material.artifact, request.profile
    )
    assert encode(result) == raw  # No repair or content reduction.
    assert material.result.claims == result.claims
    assert (
        material.inherited.qualifications == 2
        and material.inherited.contradictions == 1
    )
    generation, estimate = inference.bind(None, "structural").render(request)
    assert estimate + generation.output_tokens <= 28000
    assert check_request(request) <= plan.reducers[0].estimated_tokens


@pytest.mark.parametrize("target", [6999, 7000, 7001])
def test_exact_full_child_boundary_and_wrapper_reservation(reducer, target):
    _, _, plan, index, cps, refs, request = reducer
    result = eight_claim_result(request, canonical_bytes=4783 + target - 6867)
    material = material_for(result, request, cps, refs[plan.chunks[0].chunk_id])
    assert child_contribution(material) == target
    assert len(encode(result)) < 10000
    assert validate_result(encode(result), request, index) == result
    if target <= 7000:
        validate_child_material(
            result, material.inherited, material.artifact, request.profile
        )
    else:
        with pytest.raises(DigestionError) as caught:
            validate_child_material(
                result, material.inherited, material.artifact, request.profile
            )
        assert caught.value.validation_reason.value == "child_material_limit"
    # Integer widths, not the value of a guessed wrapper, affect serialization.
    assert (
        child_contribution(
            material.model_copy(
                update={
                    "artifact": material.artifact.model_copy(update={"byte_size": 1})
                }
            )
        )
        == target - 7
    )


@pytest.mark.parametrize(
    "text,utf8,canonical_bytes,escaped",
    [
        ('"', 1, 4, 8),
        ("\\", 1, 4, 8),
        ("\n", 1, 4, 7),
        ("é", 2, 8, 11),
        ("\u0800", 3, 8, 11),
        ("😀", 4, 14, 18),
    ],
)
def test_utf8_and_both_json_escaping_layers(text, utf8, canonical_bytes, escaped):
    assert len(text.encode("utf-8")) == utf8
    assert len(canonical(text).encode("ascii")) == canonical_bytes
    assert escaped_size(text) == escaped
    assert json.loads(json.loads(canonical(canonical(text)))) == text


@pytest.mark.parametrize("text", ['"\\\n', "é\u0800😀"])
def test_escape_heavy_results_keep_provenance_and_qualifications(reducer, text):
    _, _, plan, index, cps, refs, request = reducer
    original = eight_claim_result(request)
    claim = original.claims[0].model_copy(update={"text": text * 5})
    result = original.model_copy(update={"claims": (claim, *original.claims[1:])})
    utf8 = json.dumps(result.model_dump(mode="json"), ensure_ascii=False).encode(
        "utf-8"
    )
    assert validate_result(utf8, request, index) == result
    material = material_for(result, request, cps, refs[plan.chunks[0].chunk_id])
    validate_child_material(
        result, material.inherited, material.artifact, request.profile
    )
    assert result.claims[0].evidence_ids == original.claims[0].evidence_ids
    assert result.claims[0].lineage == original.claims[0].lineage
    assert result.claims[2].qualifications == original.claims[2].qualifications


def test_unbounded_inherited_metadata_is_never_hidden_by_fixed_reserve(reducer):
    _, _, plan, _, cps, refs, request = reducer
    result = eight_claim_result(request, canonical_bytes=4783)
    material = material_for(result, request, cps, refs[plan.chunks[0].chunk_id])
    inherited = InheritedSummary(qualifications=10**1000)
    assert (
        child_contribution(material.model_copy(update={"inherited": inherited})) > 7000
    )
    with pytest.raises(DigestionError, match="synthesis_limit_exceeded"):
        validate_child_material(result, inherited, material.artifact, request.profile)


def test_multi_child_planning_upper_bounds_actual_render_and_preserves_all_links(
    tmp_path,
):
    store, artifact, inference, plan = setup(tmp_path, bounded=True)
    from tests.unit.documents.test_managed_sizing import plain_result

    index, cps, refs = EvidenceIndex(artifact), {}, {}
    assert len(plan.chunks) == 2
    for chunk in plan.chunks:
        request = DigestionHandler.request(plan, chunk.chunk_id, cps, refs)
        result, _ = plain_result(request, index)
        checkpoint(store, plan, request, result, cps, refs)
    node = plan.reducers[0]
    request = DigestionHandler.request(plan, node.stage_id, cps, refs)
    generation, estimate = inference.bind(None, "structural").render(request)
    bound = reduction_size(plan.profile, request.structural_path, 2)
    actual = len(
        canonical(
            {
                "system": generation.system,
                "data": generation.data,
                "schema": generation.schema,
            }
        ).encode("ascii")
    )
    assert actual <= bound == node.estimated_tokens <= 24800
    assert estimate + generation.output_tokens <= 28000
    assert sum(child_contribution(c) for c in request.children) <= 14000
    control = json.loads(generation.system.split("\nCONTROL\n")[1])
    assert len(control["required_child_links"]) == sum(
        len(c.result.claims) for c in request.children
    )
    assert json.loads(generation.data)["GENERATED_CHILD_MATERIAL"] == [
        c.model_dump(mode="json") for c in request.children
    ]
    assert all(
        cps[c.result.stage_id].inherited == c.inherited for c in request.children
    )
