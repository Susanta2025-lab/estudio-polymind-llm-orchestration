from uuid import UUID
import pytest
from pydantic import ValidationError

from documents.adapters import EnhancementRequest, EnhancementResult
from documents.models import Observations, Visual
from documents.policy import decide
from test_extraction import run


@pytest.mark.parametrize('changes,outcome,tier', [
    ({}, 'native_accepted', 'native'),
    ({'structure_required': True}, 'layout_required', 'layout'),
    ({'replacement_ratio': .1}, 'manual_review', 'none'),
    ({'parser_failed': True}, 'failed', 'none'),
    ({'has_native_text': False, 'character_count': 0, 'has_images': True}, 'ocr_required', 'ocr'),
    ({'has_native_text': False, 'character_count': 0, 'has_graphics': False}, 'native_accepted', 'native'),
    ({'has_native_text': False, 'character_count': 0}, 'manual_review', 'none'),
])
def test_observations_policy_separation(changes, outcome, tier):
    facts = dict(character_count=1, printable_ratio=1, replacement_ratio=0,
                 has_native_text=True, block_count=1)
    facts.update(changes)
    obs = Observations(**facts)
    decision = decide(UUID(int=1), obs)
    assert decision.observations == obs
    assert (decision.outcome, decision.next_tier) == (outcome, tier)


def test_future_adapter_requires_physical_mapping(tmp_path, pdf_bytes):
    artifact, _ = run(tmp_path, pdf_bytes(('image',)), 'application/pdf')
    request = EnhancementRequest(scope=artifact.document.scope, source=artifact.document.source,
                                 document_version_id=artifact.document.document_version_id,
                                 parent_extraction_id=artifact.extraction_id,
                                 physical_pages=(1,), tier='ocr')
    unit = artifact.units[0].model_copy(update={'method': 'ocr', 'ocr_engine': 'fake', 'ocr_confidence': .9})
    result = EnhancementResult(request=request, engine='fake', engine_version='1', units=(unit,))
    assert result.units[0].physical_page == 1
    with pytest.raises(ValidationError):
        EnhancementResult(request=request, engine='fake', engine_version='1', units=())
    with pytest.raises(ValidationError):
        EnhancementRequest(**{**request.model_dump(), 'physical_pages': (0,)})
    assert Visual().state == 'unparsed' and Visual().cells is None
