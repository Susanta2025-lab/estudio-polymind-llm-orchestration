"""Deterministic schema/serializer measurements, never model-quality claims."""
import json
from uuid import UUID

import pytest
from pydantic import ValidationError

from documents.digestion.codec import decode, encode
from documents.digestion.managed import generation_schema
from documents.digestion.models import Claim, ClaimLink, Qualification, StageResult
from documents.jobs.models import canonical
from documents.models import stable_id


def fixture(count=1, *, qualified=False, lineage=False, text='Synthetic observation.'):
    stage = UUID(int=1)
    claims = tuple(Claim(claim_id=stable_id(str(stage), str(i)), originating_stage=stage,
        text=text, kind='fact', evidence_ids=(UUID(int=100+i),),
        qualifications=(Qualification(text='Only under synthetic test conditions.',
                                     evidence_ids=(UUID(int=100+i),)),) if qualified else (),
        lineage=(ClaimLink(stage_id=UUID(int=2), claim_id=UUID(int=200+i)),) if lineage else ())
        for i in range(count))
    return StageResult(stage_id=stage, kind='reduction' if lineage else 'analysis', claims=claims)


def measurements():
    result = {}
    for name, model in [('minimal', fixture(text='x')), ('eight_plain', fixture(8)),
                        ('eight_qualified', fixture(8, qualified=True)),
                        ('eight_qualified_lineage', fixture(8, qualified=True, lineage=True))]:
        omitted = canonical(model.model_dump(mode='json', exclude_defaults=True)).encode('ascii')
        explicit = encode(model)
        result[name] = dict(omitted_raw=len(omitted), explicit_raw=len(explicit), canonical=len(explicit),
                           default_overhead=len(explicit)-len(omitted))
    return result


@pytest.mark.parametrize('limit', [3000, 4000, 6000])
def test_scenarios(limit):
    expected = {3000: [True, True, False, False], 4000: [True, True, True, False],
                6000: [True, True, True, True]}
    assert [row['canonical'] <= limit for row in measurements().values()] == expected[limit]
    model = fixture(8, qualified=True, lineage=True)
    assert decode(encode(model), StageResult, 6000) == model
    assert generation_schema()['properties']['schema_version']['default'] == 'stage-result/1'


def test_default_expansion_overflows_while_raw_fits():
    model = fixture(8, qualified=True)
    raw = canonical(model.model_dump(mode='json', exclude_defaults=True)).encode('ascii')
    parsed = decode(raw, StageResult, 3000)
    assert len(raw) <= 3000 < len(encode(parsed))
    assert parsed == model
    assert decode(encode(model), StageResult, 6000) == parsed


def test_minimal_explicit_response_fits():
    model = fixture(text='x')
    assert len(encode(model)) < 3000
    assert decode(encode(model), StageResult, 3000) == model
    assert set(json.loads(encode(model))) == set(StageResult.model_fields)
    assert set(json.loads(encode(model))['claims'][0]) == set(Claim.model_fields)


def test_unicode_and_escaping_bytes():
    model = fixture(text='é😀 "quote" \\ path\n')
    raw = json.dumps(model.model_dump(mode='json'), ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    escaped = encode(model)
    assert len(escaped) - len(raw) == 12  # é: 2 -> 6 bytes; emoji: 4 -> 12 bytes (12 total)
    assert b'\\u00e9' in escaped and b'\\ud83d\\ude00' in escaped
    assert b'\\"quote\\"' in escaped and b'\\\\ path\\n' in escaped
    assert decode(raw, StageResult, 3000) == decode(escaped, StageResult, 3000)


def test_profile_accepts_independent_byte_increase():
    from tests.performance.fixtures import profile
    for limit in (4000, 6000, 10000):
        chosen = profile(reserved_output_tokens=3000, max_result_characters=limit, max_response_bytes=10000)
        assert chosen.reserved_output_tokens == 3000


def test_eight_claims_pass_real_evidence_and_lineage_validation(tmp_path):
    from tests.unit.documents.test_managed_inference import setup_adapter
    from tests.performance.fixtures import profile
    from documents.digestion.models import ChildInput, InheritedSummary, StageRequest
    from documents.digestion.validation import validate_result
    from documents.models import ObjectRef
    adapter, request, index, _, _ = setup_adapter(tmp_path)
    eid = request.source_data[0].evidence_id()
    claims = tuple(Claim(claim_id=stable_id(str(request.stage_id), str(i)),
        originating_stage=request.stage_id, text='Synthetic observation.', kind='fact', evidence_ids=(eid,),
        qualifications=(Qualification(text='Only under synthetic test conditions.', evidence_ids=(eid,)),))
        for i in range(8))
    child = StageResult(stage_id=request.stage_id, kind='analysis', claims=claims)
    chosen = profile(reserved_output_tokens=3000, max_result_characters=10000, max_response_bytes=10000)
    request = request.model_copy(update={'profile': chosen})
    assert validate_result(encode(child), request, index) == child
    scope = index.artifact.document.scope
    object_id = UUID(int=500)
    ref = ObjectRef(scope=scope, kind='artifact', object_id=object_id,
        key=stable_id(scope.identity(), 'artifact', str(object_id)), sha256='0'*64, byte_size=0)
    parent = fixture(8, qualified=True, lineage=True)
    parent = parent.model_copy(update={'claims': tuple(c.model_copy(update={
        'evidence_ids': (eid,), 'qualifications': child.claims[i].qualifications,
        'lineage': (ClaimLink(stage_id=child.stage_id, claim_id=child.claims[i].claim_id),)})
        for i, c in enumerate(parent.claims))})
    reduction = StageRequest(stage_id=parent.stage_id, stage='reduction', profile=chosen, structural_path=(),
        children=(ChildInput(artifact=ref, result=child, inherited=InheritedSummary()),))
    assert validate_result(encode(parent), reduction, index) == parent
    assert len(encode(child)) == measurements()['eight_qualified']['canonical']
    assert len(encode(parent)) == measurements()['eight_qualified_lineage']['canonical']
