"""Two-layer generation contract, synthetic and offline only."""
from copy import deepcopy
from dataclasses import replace
import json
import socket

import jsonschema
import pytest

# Frozen canonical-output v9 characterization; v10 has separate wire regressions.
pytestmark = pytest.mark.usefixtures("managed_v9")

from pydantic import ValidationError

from tests.historical_managed import generation_schema, ManagedSettings
from documents.digestion.models import DigestionError, StageResult
from documents.digestion.validation import validate_result
from llm.azure_schema import provider_schema
from llm.inference import InferenceConfigurationError, InferenceResponseError, InferenceOutputLimitError
from tests.integration.test_attempt3_serialization import synthetic, corrupt
from tests.unit.documents.test_managed_inference import setup_adapter, settings
from tests.unit.documents.test_strict_schema_compatibility import nodes
from tests.unit.test_structured_provider import client, Response, payload, request
from tests.performance.foundry_recalibration import candidate_capability


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    def deny(*a, **kw):
        raise AssertionError('Network forbidden')
    for name in ('connect', 'connect_ex', 'sendto'):
        monkeypatch.setattr(socket.socket, name, deny)
    for name in ('create_connection', 'getaddrinfo', 'gethostbyname'):
        monkeypatch.setattr(socket, name, deny)


def strict_request():
    return replace(request(), capability=candidate_capability(strict_digestion=True),
                   schema=generation_schema(), output_tokens=3000, response_bytes=10000,
                   max_response_envelope_bytes=26192)


def test_conversion_preserves_structure_and_does_not_mutate():
    from documents.jobs.models import fingerprint

    original = generation_schema()
    before = deepcopy(original)
    schema = provider_schema(original)
    assert fingerprint(original) == 'a051949799a312d1aa15a5959bbe7d558265cfc38f6ce992eb97fbdbdff212ab'
    assert fingerprint(schema) == '4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2'
    assert original == before and schema == provider_schema(original)
    jsonschema.Draft202012Validator.check_schema(schema)
    objects = [n for n in nodes(schema) if n.get('type') == 'object']
    assert len(objects) == 4
    assert sum(len(n['properties']) for n in objects) == 22
    for obj in objects:
        assert obj['additionalProperties'] is False
        assert obj['required'] == list(obj['properties'])
    assert schema['properties']['schema_version']['enum'] == ['stage-result/1']
    assert schema['$defs']['Claim']['properties']['subject']['anyOf'] == [
        {'type': 'string'}, {'type': 'null'}]
    forbidden = {'format', 'minLength', 'maxLength', 'pattern', 'const', 'default', 'title'}
    assert not any(forbidden & n.keys() for n in nodes(schema))
    def compare(a, b):
        if 'properties' in a:
            assert a['properties'].keys() == b['properties'].keys()
        for key in ('type', '$ref', 'enum'):
            if key in a:
                assert a[key] == b[key]
        for key in ('properties', '$defs'):
            for name, value in a.get(key, {}).items():
                compare(value, b[key][name])
        for i, child in enumerate(a.get('anyOf', [])):
            compare(child, b['anyOf'][i])
        if 'items' in a:
            compare(a['items'], b['items'])
    compare(original, schema)


@pytest.mark.parametrize('kind', ['fact', 'unknown', 'unsupported', 'commentary', 'structural'])
@pytest.mark.parametrize('subject_case', ['null', 'token', 'missing', 'empty', 'blank', 'invalid', 'type'])
def test_subject_contract_matrix(tmp_path, kind, subject_case):
    # Real extraction/planning and deterministic IDs; all claims cover authorized source.
    _, req, index, _, _ = setup_adapter(tmp_path)
    req = req.model_copy(update={'profile': req.profile.model_copy(update={
        'max_response_bytes': 10000, 'max_result_characters': 10000})})
    data = synthetic(req)
    claim = data['claims'][0]
    claim.update(kind=kind, subject={
        'null': None, 'token': 'a' * 128, 'missing': None, 'empty': '',
        'blank': '   ', 'invalid': 'invalid subject!', 'type': 42,
    }[subject_case])
    if subject_case == 'missing':
        del claim['subject']
    assert jsonschema.Draft202012Validator(provider_schema(generation_schema())).is_valid(data) == (
        subject_case not in {'missing', 'type'})
    assert jsonschema.Draft202012Validator(generation_schema()).is_valid(data) == (
        subject_case in {'null', 'token'})
    raw = json.dumps(data).encode()
    if subject_case in {'empty', 'blank', 'invalid', 'type'}:
        with pytest.raises(ValidationError):
            StageResult.model_validate(data)
        with pytest.raises(DigestionError) as caught:
            validate_result(raw, req, index)
        assert caught.value.validation_diagnostic.value == 'pydantic_validation'
        assert caught.value.validation_reason.value == (
            'invalid_field_type' if subject_case == 'type' else 'invalid_subject_token')
    else:
        model = StageResult.model_validate(data)
        if subject_case == 'token' and kind != 'fact':
            # Both schemas and Pydantic intentionally permit this; domain validation rejects it.
            with pytest.raises(DigestionError) as caught:
                validate_result(raw, req, index)
            assert caught.value.validation_diagnostic.value == 'claim_contract'
            assert caught.value.validation_reason.value == 'subject_on_nonfact'
        else:
            assert validate_result(raw, req, index) == model
            assert model.claims[0].subject == ('a' * 128 if subject_case == 'token' else None)


def test_attempt5_bindings_rejected_without_loading_historical_configuration():
    from types import SimpleNamespace

    from tests.performance.foundry_l1 import (
        LaunchConfiguration,
        generation_contract_digest,
    )
    from tests.performance.foundry_single_call import (
        SingleCallConfiguration,
        executor_digest,
    )

    historical_generation = '7d387a8595cf63e2ac944a25c4987a1b37392aa4adba8889914acf51ff9f0f59'
    historical_executor = '82fc01aa0447d4be758124cec0120a06db49f139f69ee6425b51b8696a6ad26f'
    assert generation_contract_digest() != historical_generation
    assert executor_digest() != historical_executor
    stale = SimpleNamespace(contract=None, policy=None, generation_contract_sha256=historical_generation,
        governance_policy=SimpleNamespace(evaluation=None))
    with pytest.raises(ValueError, match='generation contract'):
        LaunchConfiguration.bounded(stale)
    for executor, generation in ((historical_executor, generation_contract_digest()),
                                 (executor_digest(), historical_generation)):
        stale = SimpleNamespace(executor_sha256=executor, generation_contract_sha256=generation)
        with pytest.raises(ValueError, match='Execution contract changed'):
            SingleCallConfiguration.bounded(stale)


@pytest.mark.parametrize('keyword,value', [('allOf', []), ('oneOf', []), ('minimum', 0),
    ('maxItems', 2), ('patternProperties', {}), ('unevaluatedProperties', False),
    ('unknown', True), ('format', 'date-time')])
def test_unknown_constructs_fail_before_transport(keyword, value):
    schema = generation_schema()
    schema['$defs']['Claim']['properties']['text'][keyword] = value
    p = client(Response(payload()))
    with pytest.raises(InferenceConfigurationError):
        p.execute(replace(strict_request(), schema=schema))
    assert not p.http_client.calls


@pytest.mark.parametrize('case', ['open_object', 'remote_ref', 'missing_ref', 'recursive', 'properties', 'depth'])
def test_complexity_and_references_fail_closed(case):
    schema = generation_schema()
    if case == 'open_object':
        schema['$defs']['Qualification']['additionalProperties'] = True
    elif case in ('remote_ref', 'missing_ref', 'recursive'):
        schema['$defs']['Claim']['properties']['text'] = {'$ref': {
            'remote_ref': 'https://example.invalid/schema', 'missing_ref': '#/$defs/Absent',
            'recursive': '#/$defs/Claim'}[case]}
    elif case == 'properties':
        schema['properties'].update({f'extra{i}': {'type': 'string'} for i in range(79)})
    else:
        node = {'type': 'string'}
        for _ in range(6):
            node = {'type': 'array', 'items': node}
        schema['properties']['deep'] = node
    with pytest.raises(InferenceConfigurationError):
        provider_schema(schema)


@pytest.mark.parametrize('case,structural,category', [
    ('valid', True, None), ('extras', False, 'inference_contract_error'),
    ('missing', False, 'inference_contract_error'), ('uuid', True, 'inference_contract_error'),
    ('evidence', True, 'evidence_validation_failed'), ('pattern', True, 'inference_contract_error'),
    ('empty', True, 'inference_contract_error'), ('long', True, 'inference_contract_error'),
    ('lineage', True, 'evidence_validation_failed'), ('origin', True, 'inference_contract_error'),
    ('order', True, 'inference_contract_error'), ('stage', True, 'inference_contract_error'),
    ('qualification', True, 'evidence_validation_failed'), ('missing_evidence', True, 'evidence_validation_failed'),
    ('contradiction', True, 'evidence_validation_failed'), ('version', False, 'inference_contract_error'),
])
def test_two_layers(tmp_path, case, structural, category):
    _, req, index, _, _ = setup_adapter(tmp_path)
    req = req.model_copy(update={'profile': req.profile.model_copy(update={
        'max_response_bytes': 10000, 'max_result_characters': 10000})})
    data = synthetic(req)
    claim = data['claims'][0]
    unknown = '00000000-0000-0000-0000-000000000099'
    if case == 'extras': data = corrupt(data, identifier=False)
    elif case == 'missing': del claim['text']
    elif case == 'uuid': claim['evidence_ids'] = ['malformed']
    elif case == 'evidence': claim['evidence_ids'] = [unknown]
    elif case == 'pattern': claim['subject'] = 'invalid subject'
    elif case == 'empty': claim['text'] = ''
    elif case == 'long': claim['text'] = 'x' * 4097
    elif case == 'lineage': claim['lineage'] = [dict(stage_id=unknown, claim_id=unknown)]
    elif case == 'origin': claim['originating_stage'] = unknown
    elif case == 'order': data['claims'].reverse()
    elif case == 'stage': data['stage_id'] = unknown
    elif case == 'qualification': claim['qualifications'] = [dict(text='Synthetic.', evidence_ids=[])]
    elif case == 'missing_evidence': claim['evidence_ids'] = []
    elif case == 'contradiction': claim['contradicting_evidence_ids'] = [unknown]
    elif case == 'version': data['schema_version'] = 'stage-result/2'
    validator = jsonschema.Draft202012Validator(provider_schema(generation_schema()))
    assert validator.is_valid(data) == structural
    if category:
        with pytest.raises(DigestionError, match=f'^{category}$'):
            validate_result(json.dumps(data).encode(), req, index)
    else:
        assert validate_result(json.dumps(data).encode(), req, index) == StageResult.model_validate(data)


def test_strict_wire_contract():
    p = client(Response(payload()), kind='foundry')
    p.model_map = {key: 'epolymind-gpt-54-mini' for key in p.model_map}
    p.http_client.response = Response(payload(model='gpt-5.4-mini-2026-03-17'))
    p.execute(strict_request())
    args, kw = p.http_client.calls[0]
    assert args[0] == 'https://managed.example/openai/v1/chat/completions'
    sent = kw['json']
    assert sent['model'] == 'epolymind-gpt-54-mini'
    assert sent['max_completion_tokens'] == 3000
    assert sent['response_format'] == {'type': 'json_schema', 'json_schema': {
        'name': 'polymind_stage_result', 'strict': True, 'schema': provider_schema(generation_schema())}}
    assert len(p.http_client.calls) == 1


@pytest.mark.parametrize('case', ['refusal', 'refusal_with_content', 'length', 'max_tokens', 'missing_finish', 'choices'])
def test_strict_failures_are_single_call_and_preserve_usage(case):
    value = payload()
    choice = value['choices'][0]
    if case.startswith('refusal'):
        choice['message']['refusal'] = 'Private refusal content'
        if case == 'refusal': choice['message']['content'] = None
    elif case == 'missing_finish': del choice['finish_reason']
    elif case == 'choices': value['choices'].append(deepcopy(choice))
    else: choice['finish_reason'] = case
    p = client(Response(value))
    error = InferenceOutputLimitError if case in ('length', 'max_tokens') else InferenceResponseError
    with pytest.raises(error) as caught:
        p.execute(strict_request())
    assert caught.value.usage.prompt_tokens == 21
    assert 'Private' not in str(caught.value)
    assert len(p.http_client.calls) == 1 and p.http_client.response.closed


def test_capability_and_managed_version_gate(monkeypatch):
    cap = candidate_capability(strict_digestion=True).model_copy(update={'context_tokens': 50000})
    with pytest.raises(ValidationError):
        type(cap).model_validate({**cap.model_dump(), 'structured_output': 'json_object'})
    with pytest.raises(ValidationError): settings(capability=cap)
    chosen = settings(capability=cap, generation_profile='managed-generation/2')
    assert chosen.generation_profile == 'managed-generation/2'
    from tests.historical_managed import _module as managed
    bad = generation_schema(); bad['unknown'] = True
    monkeypatch.setattr(managed, 'generation_schema', lambda: bad)
    with pytest.raises(InferenceConfigurationError):
        ManagedSettings.model_validate(chosen.model_dump())
    p = client(Response(payload()), kind='ollama')
    with pytest.raises(InferenceConfigurationError): p.execute(strict_request())
    assert not p.http_client.calls


def test_attempt3_contract_rejected_before_approval():
    from types import SimpleNamespace
    from tests.performance.foundry_l1 import LaunchConfiguration, generation_contract_digest
    old = '2ff2aff8f575ed99b23108dd5d10c2f7a73a55fb6cc7e073107e0597124c7290'
    assert generation_contract_digest() != old
    stale = SimpleNamespace(contract=None, policy=None, generation_contract_sha256=old,
                            governance_policy=SimpleNamespace(evaluation=None))
    with pytest.raises(ValueError, match='generation contract'):
        LaunchConfiguration.bounded(stale)


def test_real_offline_pipeline_enforces_both_layers(tmp_path, monkeypatch):
    from tests.performance.foundry_preflight import OfflineHTTP, execute
    original = OfflineHTTP.response
    modes = []
    def checked(self, sent, result, stage):
        fmt = sent['response_format']
        modes.append(fmt['type'])
        if fmt['type'] == 'json_schema':
            assert fmt['json_schema']['strict'] is True
            jsonschema.validate(json.loads(result), fmt['json_schema']['schema'])
        return original(self, sent, result, stage)
    monkeypatch.setattr(OfflineHTTP, 'response', checked)
    result = execute(tmp_path, 'L1')
    assert modes == ['json_schema'] * 3 + ['json_object']
    assert result['job_state'] == 'COMPLETED' and result['digest_status'] == 'COMPLETE'
    assert result['questions']['status'] == 'COMPLETE'
    assert result['calls'] == 4
    assert all(r['state'] == 'SETTLED' for r in result['governance_records'])


@pytest.mark.parametrize('case', ['uuid', 'refusal', 'unknown_usage'])
def test_strict_downstream_and_provider_failures_settle(tmp_path, monkeypatch, case):
    from tests.performance.foundry_preflight import OfflineHTTP, execute
    original = OfflineHTTP.response
    def invalid(self, sent, result, stage):
        data = json.loads(result)
        if case == 'uuid':
            data['claims'][0]['evidence_ids'][0] = 'malformed'
            assert not jsonschema.Draft202012Validator(
                sent['response_format']['json_schema']['schema']).is_valid(data)
            # Still return the malformed synthetic response: independent application
            # rejection must preserve known usage if a provider violates its schema.
        response = original(self, sent, json.dumps(data), stage)
        if case != 'uuid':
            envelope = json.loads(b''.join(response.iter_content(1)))
            if case == 'refusal':
                envelope['choices'][0]['message']['refusal'] = 'Synthetic refusal'
            else:
                envelope.pop('usage')
            raw = json.dumps(envelope).encode()
            response.iter_content = lambda chunk_size: iter([raw])
        return response
    monkeypatch.setattr(OfflineHTTP, 'response', invalid)
    result = execute(tmp_path, 'L1')
    assert result['job_state'] == 'FAILED' and result['calls'] == 1
    assert 'publication' not in result
    record = result['governance_records'][0]
    assert record['state'] == ('UNKNOWN' if case == 'unknown_usage' else 'SETTLED')
    if case != 'unknown_usage':
        assert record['actual_cost'] == '0.000011'


def test_historical_capability_and_managed_fingerprints_remain_readable(tmp_path):
    from documents.jobs.models import fingerprint
    from llm.structured import CapabilityProfile
    historical = candidate_capability().model_dump(mode='json')
    assert 'schema_profile' not in historical
    assert CapabilityProfile.model_validate(historical).model_dump(mode='json') == historical
    adapter, _, _, _, _ = setup_adapter(tmp_path)
    old_settings = adapter.settings.model_dump(mode='json')
    old_settings.pop('generation_profile')
    assert adapter.config == fingerprint({'settings': old_settings,
        'provider': adapter.provider.name, 'model': adapter.model})
    assert ManagedSettings.model_validate(old_settings).generation_profile == 'managed-generation/1'
