"""Complete v10 envelopes and exact G1 boundaries; no model or network."""

from io import BytesIO
from uuid import UUID

import pytest

from documents.digestion.models import DigestionError, SourcePiece, StageRequest
from documents.digestion.planning import check_request
from documents.digestion.sizing import (
    analysis_size,
    child_contribution,
    escaped_size,
    reduction_size,
)
from documents.digestion.wire import references
from documents.extraction import extract
from documents.jobs.models import canonical
from documents.models import EvidenceRef, Span
from documents.storage import LocalObjectStore
from llm.azure_schema import provider_schema
from llm.inference import InferenceContextError
from tests.generation_wire_fixtures import cases, inference
from tests.performance.fixtures import NOW, SCOPE, profile

pytestmark = pytest.mark.usefixtures("managed_wire_version")


def measured(generation):
    return len(
        canonical(
            {
                "system": generation.system,
                "data": generation.data,
                "schema": generation.schema,
            }
        ).encode()
    )


@pytest.mark.parametrize("stage", ["chunk", "intermediate", "structural", "root"])
@pytest.mark.parametrize("count", [0, 1, 4, 128, 129, 256, 257])
def test_cardinality_complete_serialization_and_admission(tmp_path, stage, count):
    adapter = inference()
    store = LocalObjectStore(tmp_path / "objects")
    artifact, _ = extract(
        BytesIO(b"x" * max(count, 1)),
        scope=SCOPE,
        document_id=UUID(int=8),
        display_filename="synthetic.txt",
        declared_mime="text/plain",
        store=store,
        created_at=NOW,
        extracted_at=NOW,
    )
    unit, block = artifact.units[0], artifact.units[0].blocks[0]
    chosen = adapter.profile(
        profile(
            context_tokens=28000,
            reserved_output_tokens=3000,
            max_result_characters=10000,
            max_response_bytes=10000,
        )
    )
    pieces = tuple(
        SourcePiece(
            evidence=EvidenceRef(
                scope=SCOPE,
                document_version_id=artifact.document.document_version_id,
                extraction_id=artifact.extraction_id,
                source_id=unit.source_id,
                block_id=block.block_id,
                span=Span(start=i, end=i + 1, line_start=1, line_end=1),
            ),
            text="x",
            kind="text",
        )
        for i in range(count)
    )
    request = StageRequest(
        stage_id=UUID(int=9), stage="reduction", profile=chosen, structural_path=()
    )
    if stage == "chunk":
        request = request.model_copy(
            update={"stage": "analysis", "source_data": pieces}
        )
    else:
        # Measure the same authority through an actual canonical child claim.
        from documents.digestion.codec import put
        from documents.digestion.models import (
            ChildInput,
            Claim,
            InheritedSummary,
            StageResult,
        )
        from documents.models import stable_id

        result = StageResult(
            stage_id=UUID(int=7),
            kind="analysis",
            claims=(
                Claim(
                    claim_id=stable_id(str(UUID(int=7)), "0"),
                    originating_stage=UUID(int=7),
                    text="Synthetic.",
                    kind="commentary",
                    evidence_ids=tuple(p.evidence_id() for p in pieces),
                ),
            ),
        )
        ref = put(store, SCOPE, result, chosen.max_artifact_bytes)
        request = request.model_copy(
            update={
                "children": (
                    ChildInput(
                        artifact=ref, result=result, inherited=InheritedSummary()
                    ),
                )
            }
        )
    if count == 257:
        with pytest.raises(DigestionError):
            references(request)
        with pytest.raises(DigestionError):
            adapter.bind(None, stage).render(request, _check_limits=False)
        return
    bound = adapter.bind(None, stage)
    generation, estimate = bound.render(request, _check_limits=False)
    table = references(request)
    assert len(table.evidence) == count
    converted = provider_schema(generation.schema)
    assert len(canonical(converted)) <= len(canonical(generation.schema))
    source = converted["$defs"]["SourceEvidence"]
    branches = source.get("anyOf", [source])
    assert sum(len(b.get("enum", [])) for b in branches) == count
    assert all(len(b.get("enum", [])) <= 128 for b in branches)
    assert generation.response_bytes == 10000 and generation.output_tokens == 3000
    assert generation.capability.context_tokens == 28000
    # Conservative planner admission and actual renderer are independent; neither
    # the 256-ID schema bound nor wire output size promises G1 admissibility.
    try:
        check_request(request)
        checked, _ = bound.render(request)
    except (DigestionError, InferenceContextError):
        assert count == 0 and stage == "chunk" or count >= 128
    else:
        assert measured(checked) == measured(generation)
        reservation = (
            analysis_size(request)
            if stage == "chunk"
            else reduction_size(chosen, (), len(request.children))
        )
        assert measured(generation) <= reservation <= 24800
        assert estimate + 3000 <= 28000


@pytest.mark.parametrize("stage", ["intermediate", "structural", "root"])
@pytest.mark.parametrize("children", [1, 2])
@pytest.mark.parametrize("prefix", ["", '"\\\n', "é\u0800😀"])
def test_exact_path_boundaries_and_complete_child_accounting(
    tmp_path, stage, children, prefix
):
    adapter, records, plan, _, _ = cases(
        tmp_path, chunk_characters=3200 if children == 1 else 800
    )
    request = records["structural"][0]
    assert len(request.children) == children
    bound = adapter.bind(None, stage)
    base = reduction_size(plan.profile, (), children)
    room = 24800 - base - (escaped_size((prefix,)) - escaped_size(()))
    assert room > 0
    for delta, accepted in [(0, True), (1, False)]:
        path = (prefix + "a" * (room + delta),)
        changed = request.model_copy(update={"structural_path": path})
        diagnostic, _ = bound.render(changed, _check_limits=False)
        reservation = reduction_size(plan.profile, path, children)
        assert reservation == 24800 + delta
        assert all(child_contribution(c) <= 7000 for c in changed.children)
        if accepted:
            check_request(changed)
            generation, estimate = bound.render(changed)
            assert measured(generation) == measured(diagnostic) <= reservation
            assert estimate + 3000 <= 28000
        else:
            with pytest.raises((DigestionError, InferenceContextError)):
                bound.render(changed)
