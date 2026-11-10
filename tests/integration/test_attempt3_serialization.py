"""Synthetic Attempt 3 failure shape; no private response or live authorities."""
import json
import socket
from copy import deepcopy

import pytest

# Frozen canonical-output v9 characterization; v10 has separate wire regressions.
pytestmark = pytest.mark.usefixtures("managed_v9")

from pydantic import ValidationError

from documents.digestion.codec import decode, encode
from documents.digestion.managed import classify_managed, generation_schema
from documents.digestion.models import DigestionError, StageResult
from documents.digestion.validation import validate_result
from documents.models import stable_id
from tests.performance.foundry_preflight import OfflineHTTP, execute
from tests.unit.documents.test_managed_inference import setup_adapter


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    def deny(*args, **kwargs):
        raise AssertionError('Network forbidden')
    monkeypatch.setattr(socket.socket, 'connect', deny)
    monkeypatch.setattr(socket, 'create_connection', deny)


def synthetic(request):
    return StageResult(stage_id=request.stage_id, kind='analysis', claims=tuple(
        dict(claim_id=stable_id(str(request.stage_id), str(i)),
             originating_stage=request.stage_id, text='Synthetic source observation.',
             kind='fact', evidence_ids=[request.source_data[0].evidence_id()])
        for i in range(4))).model_dump(mode='json')


def corrupt(data, *, extras=True, identifier=True):
    data = deepcopy(data)
    if extras:
        data.update({f'unused{i}': None for i in range(1, 9)})
    if identifier:
        data['claims'][1]['evidence_ids'][0] += '0'
    return data


@pytest.mark.parametrize('extras,identifier', [(True, True), (True, False), (False, True)])
def test_independent_schema_violations(tmp_path, extras, identifier):
    _, request, index, _, _ = setup_adapter(tmp_path)
    data = corrupt(synthetic(request), extras=extras, identifier=identifier)
    with pytest.raises(ValidationError) as caught:
        StageResult.model_validate(data)
    errors = caught.value.errors(include_input=False)
    assert len(errors) == 8 * extras + identifier
    assert {e['type'] for e in errors} == (
        ({'extra_forbidden'} if extras else set()) |
        ({'uuid_parsing'} if identifier else set()))
    with pytest.raises(DigestionError, match='^inference_contract_error$') as caught:
        validate_result(json.dumps(data).encode(), request, index)
    failure = classify_managed(caught.value)
    assert failure.category == 'serialization_error'
    assert failure.classification == 'NON_RETRYABLE'


def test_schema_and_valid_control_serialization(tmp_path):
    _, request, index, _, _ = setup_adapter(tmp_path)
    request = request.model_copy(update={'profile': request.profile.model_copy(update={
        'max_response_bytes': 10000, 'max_result_characters': 10000})})
    schema = generation_schema()
    for node in (schema, *schema['$defs'].values()):
        assert node['additionalProperties'] is False
        assert set(node['required']) == set(node['properties'])
    data = synthetic(request)
    data['claims'][0]['text'] = 'Synthetic café observation.'
    result = validate_result(json.dumps(data, ensure_ascii=False).encode(), request, index)
    canonical = encode(result)
    assert b'caf\\u00e9' in canonical
    assert decode(canonical, StageResult, 10000) == result
    at_limit = request.model_copy(update={'profile': request.profile.model_copy(update={
        'max_result_characters': len(canonical)})})
    assert validate_result(canonical, at_limit, index) == result
    too_small = at_limit.model_copy(update={'profile': at_limit.profile.model_copy(update={
        'max_result_characters': len(canonical)-1})})
    with pytest.raises(DigestionError, match='synthesis_limit_exceeded'):
        validate_result(canonical, too_small, index)
    with pytest.raises(DigestionError, match='synthesis_limit_exceeded'):
        validate_result(canonical + b' ' * (10001-len(canonical)), request, index)


@pytest.mark.parametrize('raw', [b'{', b'{"kind":"analysis","kind":"analysis"}'])
def test_invalid_json_rejected(raw):
    with pytest.raises(DigestionError, match='inference_contract_error'):
        decode(raw, StageResult, 10000)


def test_downstream_rejection_settles_once_without_retry(tmp_path, monkeypatch):
    original = OfflineHTTP.response

    def invalid_response(self, sent, result, stage):
        control = json.loads(sent['messages'][0]['content'].split('\nCONTROL\n')[1])
        assert sent['max_completion_tokens'] == 3000
        assert control['max_response_bytes'] == control['max_result_bytes'] == 10000
        data = json.loads(result)
        # Use entirely synthetic source identities and text from the offline harness.
        data['claims'] *= 4
        for i, claim in enumerate(deepcopy(data['claims'])):
            claim['claim_id'] = control['claim_ids_in_order'][i]
            data['claims'][i] = claim
        return original(self, sent, json.dumps(corrupt(data)), stage)

    monkeypatch.setattr(OfflineHTTP, 'response', invalid_response)
    result = execute(tmp_path, 'L1')
    assert result['job_state'] == 'FAILED'
    assert result['terminal_category'] == 'serialization_error'
    assert result['calls'] == 1
    assert result['billable_calls'] == 0
    assert 'publication' not in result
    assert len(result['run_records']) == len(result['governance_records']) == 1
    assert result['run_records'][0]['finished'] is not None
    assert result['run_records'][0]['outcome'] == 'success'
    assert result['governance_records'][0]['state'] == 'SETTLED'
    # Synthetic rates: (30 * 0.1 + 40 * 0.2) / 1,000,000 EUR.
    assert result['governance_records'][0]['actual_cost'] == '0.000011'
    assert result['provider_records'][0]['outcome'] == 'success'
