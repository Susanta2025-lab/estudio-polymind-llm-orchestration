"""Offline evidence for the Azure exact-schema blocker, not deployment proof."""
import json
import socket
from copy import deepcopy
from dataclasses import replace

import pytest

from documents.digestion.managed import generation_schema
from documents.digestion.models import DigestionError
from documents.digestion.validation import validate_result
from tests.integration.test_attempt3_serialization import corrupt, synthetic
from tests.unit.documents.test_managed_inference import setup_adapter
from tests.unit.test_structured_provider import Response, client, payload, request


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    def deny(*args, **kwargs):
        raise AssertionError('Network forbidden')
    for name in ('connect', 'connect_ex', 'sendto'):
        monkeypatch.setattr(socket.socket, name, deny)
    for name in ('create_connection', 'getaddrinfo', 'gethostbyname'):
        monkeypatch.setattr(socket, name, deny)


def nodes(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from nodes(child)


def test_actual_schema_has_documented_azure_blockers():
    # Microsoft Learn structured-outputs, "Unsupported type-specific keywords".
    schema = generation_schema()
    unsupported = {'minLength', 'maxLength', 'pattern', 'format'}
    assert {key for node in nodes(schema) for key in node if key in unsupported} == unsupported
    claim = schema['$defs']['Claim']['properties']
    assert claim['text']['minLength'] == 1
    assert claim['text']['maxLength'] == 4096
    assert claim['subject']['anyOf'][0]['pattern'] == '^[a-zA-Z0-9_./:-]+$'
    assert claim['evidence_ids']['items']['format'] == 'uuid'
    objects = [node for node in nodes(schema) if node.get('type') == 'object']
    assert len(objects) == 4
    assert sum(len(node['properties']) for node in objects) == 22
    for node in objects:
        assert node['additionalProperties'] is False
        assert node['required'] == list(node['properties'])
    for node in nodes(schema):
        if '$ref' in node:
            assert node['$ref'].startswith('#/$defs/')
            assert node['$ref'].removeprefix('#/$defs/') in schema['$defs']


@pytest.mark.parametrize('mode', ['json_object', 'json_schema'])
def test_existing_modes_are_not_strict_schema_support(mode):
    from tests.performance.foundry_recalibration import candidate_capability
    assert candidate_capability().structured_output == 'json_object'
    provider = client(Response(payload()), kind='foundry')
    schema = generation_schema()
    generation = replace(request(structured_output=mode,
        output_parameter='max_completion_tokens'), schema=schema)
    provider.execute(generation)
    assert len(provider.http_client.calls) == 1
    args, kwargs = provider.http_client.calls[0]
    assert args[0] == 'https://managed.example/openai/v1/chat/completions'
    expected = {'type': 'json_object'} if mode == 'json_object' else {
        'type': 'json_schema', 'json_schema': {
            'name': 'stage_result', 'strict': False, 'schema': schema}}
    assert kwargs['json']['response_format'] == expected


@pytest.mark.parametrize('case', [
    'malformed_uuid', 'eight_extras', 'both', 'nested_extra',
    'qualification_extra', 'lineage_extra', 'missing_required', 'valid', 'unknown_evidence',
])
def test_schema_and_application_rejections(tmp_path, case):
    jsonschema = pytest.importorskip('jsonschema')
    _, request, index, _, _ = setup_adapter(tmp_path)
    data = synthetic(request)
    if case in ('malformed_uuid', 'eight_extras', 'both'):
        data = corrupt(data, extras=case != 'malformed_uuid', identifier=case != 'eight_extras')
    elif case == 'nested_extra':
        data['claims'][0]['unused'] = None
    elif case == 'qualification_extra':
        data['claims'][0]['qualifications'] = [dict(text='Synthetic qualification.',
            evidence_ids=data['claims'][0]['evidence_ids'], unused=None)]
    elif case == 'lineage_extra':
        data['claims'][0]['lineage'] = [dict(stage_id=str(request.stage_id),
            claim_id=data['claims'][0]['claim_id'], unused=None)]
    elif case == 'missing_required':
        del data['claims'][0]['text']
    elif case == 'unknown_evidence':
        data['claims'][0]['evidence_ids'] = ['00000000-0000-0000-0000-000000000099']
    schema = generation_schema()
    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    errors = list(validator.iter_errors(data))
    assert bool(errors) == (case not in ('valid', 'unknown_evidence'))
    raw = json.dumps(data).encode()
    if case == 'valid':
        assert validate_result(raw, request, index).stage_id == request.stage_id
    else:
        category = 'evidence_validation_failed' if case == 'unknown_evidence' else 'inference_contract_error'
        with pytest.raises(DigestionError, match=f'^{category}$'):
            validate_result(raw, request, index)


def test_stripping_constraints_is_not_contract_preserving(tmp_path):
    jsonschema = pytest.importorskip('jsonschema')
    _, request, _, _, _ = setup_adapter(tmp_path)
    original = generation_schema()
    weakened = deepcopy(original)
    # Counterfactual only: never used by a provider or an application decoder.
    for node in nodes(weakened):
        for keyword in ('minLength', 'maxLength', 'pattern', 'format'):
            node.pop(keyword, None)
    for field, value in (('text', ''), ('text', 'x' * 4097),
                         ('subject', 'invalid subject'), ('claim_id', 'not-a-uuid')):
        data = synthetic(request)
        data['claims'][0][field] = value
        jsonschema.validate(data, weakened, format_checker=jsonschema.FormatChecker())
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(data, original, format_checker=jsonschema.FormatChecker())
