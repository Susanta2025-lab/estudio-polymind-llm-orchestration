"""Production v8 serialization across profiles, fan-in and escaped material."""

import json
from io import BytesIO
from uuid import UUID

import pytest

from documents.digestion.codec import encode
from documents.digestion.models import DigestionError
from documents.digestion.planning import build_plan, check_request
from documents.digestion.sizing import (
    child_contribution,
    escaped_size,
    reduction_size,
)
from documents.digestion.validation import EvidenceIndex, validate_result
from documents.digestion.workflow import DigestionHandler
from documents.extraction import extract
from documents.jobs.models import canonical
from documents.storage import LocalObjectStore
from tests.integration.test_final_offline_azure_compatibility import (
    legacy_v8_contracts as legacy_v8_contracts,  # noqa: PLC0414
)
from tests.integration.test_managed_prompt7_contract import (
    adapter as historical_adapter,
)
from tests.performance.fixtures import NOW, SCOPE, profile
from tests.performance.foundry_envelopes import maximal_result
from tests.unit.documents.test_managed_sizing import (
    checkpoint,
    plain_result,
    setup,
)


@pytest.fixture(autouse=True)
def pinned_v8_adapter(monkeypatch, legacy_v8_contracts):
    from tests.unit.documents import test_managed_sizing

    def adapter(child_bytes=None):
        assert child_bytes == 7000
        return historical_adapter(legacy_v8_contracts["chunk"], "chunk")

    monkeypatch.setattr(test_managed_sizing, "adapter", adapter)


@pytest.fixture
def adapter():
    from tests.unit.documents import test_managed_sizing

    return test_managed_sizing.adapter


VARIANTS = ["ordinary", 'Section "A"\\path\n', "é\u0800😀"]


def measured(generation):
    return len(
        canonical(
            {
                "system": generation.system,
                "data": generation.data,
                "schema": generation.schema,
            }
        ).encode("ascii")
    )


@pytest.mark.parametrize("stage", ["intermediate", "structural", "root"])
@pytest.mark.parametrize(
    "path,overhead,planned_input,accepted",
    [
        pytest.param((), 0, 24630, True, id="empty"),
        pytest.param(("a",), 5, 24635, True, id="ascii-1"),
        pytest.param(("a" * 165,), 169, 24799, True, id="ascii-165"),
        pytest.param(("a" * 166,), 170, 24800, True, id="ascii-166"),
        pytest.param(("a" * 167,), 171, 24801, False, id="ascii-167"),
        pytest.param(('"\\\n' + "a" * 155,), 170, 24800, True, id="escaped-170"),
        pytest.param(('"\\\n' + "a" * 156,), 171, 24801, False, id="escaped-171"),
        pytest.param(("é\u0800😀" + "a" * 138,), 170, 24800, True, id="unicode-170"),
        pytest.param(("é\u0800😀" + "a" * 139,), 171, 24801, False, id="unicode-171"),
    ],
)
def test_exact_structural_path_boundary(
    tmp_path, stage, path, overhead, planned_input, accepted
):
    store, artifact, inference, plan = setup(tmp_path, bounded=True)
    assert len(plan.chunks) == 2
    index, cps, refs = EvidenceIndex(artifact), {}, {}
    for chunk in plan.chunks:
        request = DigestionHandler.request(plan, chunk.chunk_id, cps, refs)
        result, _ = plain_result(request, index)
        checkpoint(store, plan, request, result, cps, refs)
    request = DigestionHandler.request(plan, plan.reducers[0].stage_id, cps, refs)
    empty = request.model_copy(update={"structural_path": ()})
    request = request.model_copy(update={"structural_path": path})
    bound = inference.bind(None, stage)
    baseline, _ = bound.render(empty)
    # Diagnostic serialization also measures rejected paths; admission below
    # always uses the checked production path, with no substituted validator.
    generation, estimate = bound.render(request, _check_limits=False)
    assert measured(generation) - measured(baseline) == overhead
    assert escaped_size(path) - escaped_size(()) == overhead
    assert json.loads(generation.data)["UNTRUSTED_STRUCTURAL_PATH"] == list(path)
    assert json.loads(generation.data)["GENERATED_CHILD_MATERIAL"] == [
        c.model_dump(mode="json") for c in request.children
    ]

    budget = plan.profile.managed_input_budget
    assert plan.profile.prompt_profile == "managed-prompt/8"
    assert budget.base_bytes == 10630
    assert budget.child_bytes == 7000
    assert len(request.children) == 2
    assert all(child_contribution(c) <= budget.child_bytes for c in request.children)
    assert reduction_size(plan.profile, (), 2) == 10630 + 14000 == 24630
    assert reduction_size(plan.profile, path, 2) == 24630 + overhead == planned_input
    assert budget.input_bytes == 24800
    cap = generation.capability
    assert cap.overhead_tokens == cap.safety_tokens == 100
    assert generation.output_tokens == plan.profile.reserved_output_tokens == 3000
    assert cap.context_tokens == plan.profile.context_tokens == 28000
    assert estimate == measured(generation) + cap.overhead_tokens + cap.safety_tokens
    assert measured(generation) <= planned_input
    planned_context = (
        planned_input
        + cap.overhead_tokens
        + cap.safety_tokens
        + generation.output_tokens
    )
    assert planned_context == planned_input + 3200

    if accepted:
        assert check_request(request) == planned_input
        assert bound.render(request) == (generation, estimate)
        assert (
            estimate + generation.output_tokens <= planned_context <= cap.context_tokens
        )
    else:
        assert planned_input == budget.input_bytes + 1
        assert planned_context == cap.context_tokens + 1
        with pytest.raises(DigestionError, match="^synthesis_limit_exceeded$"):
            check_request(request)
        with pytest.raises(DigestionError, match="^synthesis_limit_exceeded$"):
            bound.render(request)


@pytest.mark.parametrize("stage", ["intermediate", "structural", "root"])
@pytest.mark.parametrize("children", [1, 2])
@pytest.mark.parametrize("text", VARIANTS)
def test_reducer_profiles_fit_actual_v8_envelope(
    tmp_path, stage, children, text, record_property
):
    store, artifact, inference, plan = setup(
        tmp_path, bounded=True, chunk_characters=3200 if children == 1 else 800
    )
    assert len(plan.chunks) == children
    index, cps, refs = EvidenceIndex(artifact), {}, {}
    for chunk in plan.chunks:
        request = DigestionHandler.request(plan, chunk.chunk_id, cps, refs)
        result, _ = plain_result(request, index)
        claim = result.claims[0].model_copy(update={"text": text * 5})
        result = result.model_copy(update={"claims": (claim, *result.claims[1:])})
        assert validate_result(encode(result), request, index) == result
        checkpoint(store, plan, request, result, cps, refs)
    request = DigestionHandler.request(plan, plan.reducers[0].stage_id, cps, refs)
    request = request.model_copy(update={"structural_path": (text,)})
    generation, estimate = inference.bind(None, stage).render(request)
    size = measured(generation)
    bound = reduction_size(plan.profile, request.structural_path, children)
    assert plan.profile.managed_input_budget.base_bytes == 10630
    assert reduction_size(plan.profile, (), 1) == 17630
    assert reduction_size(plan.profile, (), 2) == 24630
    assert all(child_contribution(c) <= 7000 for c in request.children)
    assert size <= bound <= 24800
    assert estimate == size + 200
    assert estimate + generation.output_tokens <= 28000
    assert check_request(request) <= bound
    assert json.loads(generation.data)["GENERATED_CHILD_MATERIAL"] == [
        c.model_dump(mode="json") for c in request.children
    ]
    # Path overhead is still enforced; wording cannot expand the allocation.
    excessive = request.model_copy(update={"structural_path": (text * 2000,)})
    with pytest.raises(DigestionError, match="synthesis_limit_exceeded"):
        inference.bind(None, stage).render(excessive)
    record_property(
        "sizing",
        json.dumps(
            {
                "stage": stage,
                "children": children,
                "text": text,
                "input": size,
                "bound": bound,
                "context": estimate + 3000,
            }
        ),
    )


@pytest.mark.parametrize("text", VARIANTS)
def test_chunk_escaped_original_sources_fit_v8(
    tmp_path, text, record_property, adapter
):
    store = LocalObjectStore(tmp_path / "objects")
    artifact, ref = extract(
        BytesIO((text + "\n").encode("utf-8")),
        scope=SCOPE,
        document_id=UUID(int=7),
        display_filename="synthetic.txt",
        declared_mime="text/plain",
        store=store,
        created_at=NOW,
        extracted_at=NOW,
    )
    inference = adapter(7000)
    chosen = inference.profile(
        profile(
            context_tokens=28000,
            reserved_output_tokens=3000,
            max_result_characters=10000,
            max_response_bytes=10000,
        )
    )
    plan = build_plan(artifact, ref, chosen)
    request = DigestionHandler.request(plan, plan.chunks[0].chunk_id, {}, {})
    generation, estimate = inference.render(request)
    result, _ = maximal_result(request, EvidenceIndex(artifact), "claims")
    assert validate_result(encode(result), request, EvidenceIndex(artifact)) == result
    assert text in "".join(p.text for p in request.source_data)
    assert measured(generation) <= plan.chunks[0].estimated_tokens <= 24800
    assert estimate == measured(generation) + 200
    assert estimate + generation.output_tokens <= 28000
    record_property(
        "sizing",
        json.dumps(
            {
                "stage": "chunk",
                "text": text,
                "input": measured(generation),
                "context": estimate + 3000,
            }
        ),
    )
