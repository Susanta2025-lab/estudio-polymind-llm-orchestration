"""Production v7 serialization across profiles, fan-in and escaped material."""

import json
from io import BytesIO
from uuid import UUID

import pytest

from documents.digestion.codec import encode
from documents.digestion.models import DigestionError
from documents.digestion.planning import build_plan, check_request
from documents.digestion.sizing import child_contribution, reduction_size
from documents.digestion.validation import EvidenceIndex, validate_result
from documents.digestion.workflow import DigestionHandler
from documents.extraction import extract
from documents.jobs.models import canonical
from documents.storage import LocalObjectStore
from tests.integration.test_final_offline_azure_compatibility import (
    legacy_v7_contracts as legacy_v7_contracts,  # noqa: PLC0414
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
def pinned_v7_adapter(monkeypatch, legacy_v7_contracts):
    from tests.unit.documents import test_managed_sizing

    def adapter(child_bytes=None):
        assert child_bytes == 7000
        return historical_adapter(legacy_v7_contracts["chunk"], "chunk")

    monkeypatch.setattr(test_managed_sizing, "adapter", adapter)


@pytest.fixture
def adapter():
    # The chunk test requests the same hash-pinned historical adapter.
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
@pytest.mark.parametrize("children", [1, 2])
@pytest.mark.parametrize("text", VARIANTS)
def test_reducer_profiles_fit_actual_v7_envelope(
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
    assert plan.profile.managed_input_budget.base_bytes == 10236
    assert reduction_size(plan.profile, (), 1) == 17236
    assert reduction_size(plan.profile, (), 2) == 24236
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
def test_chunk_escaped_original_sources_fit_v7(
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
