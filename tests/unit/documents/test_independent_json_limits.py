"""Independent UTF-8 content, canonical JSON and token limits; synthetic only."""
from dataclasses import replace
import json

import pytest
from pydantic import ValidationError

from documents.models import stable_id
from documents.digestion.codec import encode
from documents.digestion.models import DigestionError
from documents.digestion.validation import validate_result
from tests.performance.fixtures import profile
from tests.unit.documents.test_output_limit_sizes import fixture
from tests.unit.documents.test_managed_inference import setup_adapter
from tests.unit.test_structured_provider import Response, client, payload, request
from llm.inference import InferenceOutputLimitError

SIZES = (2999, 3000, 6000, 9999, 10000, 10001)


def generation():
    base = request(output_parameter='max_completion_tokens')
    return replace(base, capability=base.capability.model_copy(update={'max_output_tokens': 3000}),
                   output_tokens=3000, response_bytes=10000, max_response_envelope_bytes=26192)


def padded(size):
    model = fixture(8)
    remaining = size - len(encode(model))
    claims = list(model.claims)
    for i, claim in enumerate(claims):
        amount = min(remaining, 4096-len(claim.text))
        claims[i] = claim.model_copy(update={'text': claim.text+'x'*amount})
        remaining -= amount
    result = model.model_copy(update={'claims': tuple(claims)})
    assert remaining == 0 and len(encode(result)) == size
    return result


@pytest.mark.parametrize('size', SIZES)
def test_provider_boundary_and_unchanged_completion_request(size):
    raw = encode(padded(size)).decode()
    response = Response(payload(choices=[{'message': {'content': raw}, 'finish_reason': 'stop'}]))
    assert len(response.raw) < 26192
    provider = client(response)
    if size <= 10000:
        assert provider.execute(generation()).text == raw
    else:
        with pytest.raises(InferenceOutputLimitError) as caught:
            provider.execute(generation())
        assert caught.value.diagnostics.failure_cause == 'response_bytes_exceeded'
        assert caught.value.diagnostics.response_bytes == size
    assert len(provider.http_client.calls) == 1
    assert provider.http_client.calls[0][1]['json']['max_completion_tokens'] == 3000


@pytest.mark.parametrize('size', SIZES)
def test_canonical_boundary(size, tmp_path):
    _, req, index, _, _ = setup_adapter(tmp_path)
    model = padded(size)
    eid = req.source_data[0].evidence_id()
    model = model.model_copy(update={'stage_id': req.stage_id, 'claims': tuple(
        c.model_copy(update={'claim_id': stable_id(str(req.stage_id), str(i)),
                            'originating_stage': req.stage_id, 'evidence_ids': (eid,)})
        for i, c in enumerate(model.claims))})
    assert len(encode(model)) == size
    chosen = profile(reserved_output_tokens=3000, max_result_characters=10000,
                     max_response_bytes=12000, max_claim_characters=4096)
    req = req.model_copy(update={'profile': chosen})
    if size <= 10000:
        assert validate_result(encode(model), req, index) == model
    else:
        with pytest.raises(DigestionError, match='synthesis_limit_exceeded'):
            validate_result(encode(model), req, index)


def test_raw_and_canonical_are_independent(tmp_path):
    _, req, index, _, _ = setup_adapter(tmp_path)
    chosen = profile(reserved_output_tokens=3000, max_result_characters=10000, max_response_bytes=10000)
    req = req.model_copy(update={'profile': chosen})
    model = padded(10001)
    raw = json.dumps(model.model_dump(mode='json', exclude_defaults=True), separators=(',', ':')).encode()
    assert len(raw) < 10000 < len(encode(model))
    with pytest.raises(DigestionError, match='synthesis_limit_exceeded'):
        validate_result(raw, req, index)
    # Whitespace makes provider content overflow even though canonical output fits.
    raw = encode(fixture()).decode() + ' '*(10001-len(encode(fixture())))
    provider = client(Response(payload(choices=[{'message': {'content': raw}, 'finish_reason': 'stop'}])))
    with pytest.raises(InferenceOutputLimitError) as caught:
        provider.execute(generation())
    assert caught.value.diagnostics.failure_cause == 'response_bytes_exceeded'


@pytest.mark.parametrize('reason', ['length', 'max_tokens'])
def test_token_truncation_still_fails(reason):
    provider = client(Response(payload(choices=[{'message': {'content': '{}'}, 'finish_reason': reason}],
        usage={'prompt_tokens': 21, 'completion_tokens': 3000, 'total_tokens': 3021})))
    with pytest.raises(InferenceOutputLimitError) as caught:
        provider.execute(generation())
    assert caught.value.diagnostics.failure_cause == 'provider_completion_truncated'
    assert caught.value.diagnostics.completion_tokens == caught.value.diagnostics.completion_token_limit == 3000
    assert len(provider.http_client.calls) == 1


def test_utf8_and_envelope_bounds():
    text = 'é'*5000
    response = Response(payload(choices=[{'message': {'content': text}, 'finish_reason': 'stop'}]))
    # Escaped wire Unicode can exceed the independent envelope bound even when
    # decoded content fits. Fail closed; no automatic enlargement or retry.
    assert len(text.encode()) == 10000 and len(response.raw) > 26192
    with pytest.raises(InferenceOutputLimitError) as caught:
        client(response).execute(generation())
    assert caught.value.diagnostics.failure_cause == 'unknown'
    utf8 = json.dumps(payload(choices=[{'message': {'content': text}, 'finish_reason': 'stop'}]),
                      ensure_ascii=False).encode()
    assert client(Response(raw=utf8)).execute(generation()).text == text


@pytest.mark.parametrize('field', ['max_result_characters', 'max_response_bytes', 'reserved_output_tokens'])
def test_independent_positive_validation(field):
    with pytest.raises(ValidationError):
        profile(**{field: 0})


def test_legacy_limits_and_runtime_binding(tmp_path):
    adapter, req, _, _, _ = setup_adapter(tmp_path)
    assert req.profile.response_byte_limit == req.profile.max_result_characters == 3000
    chosen = adapter.profile(profile(reserved_output_tokens=3000, max_result_characters=10000,
                                     max_response_bytes=9000))
    rendered, _ = adapter.render(req.model_copy(update={'profile': chosen}))
    control = json.loads(rendered.system.split('\nCONTROL\n')[1])
    assert rendered.response_bytes == control['max_response_bytes'] == 9000
    assert control['max_result_bytes'] == 10000
    assert rendered.output_tokens == 3000
    assert chosen.digest() != req.profile.digest()


def test_previous_contract_rejected_without_approval_access():
    from types import SimpleNamespace
    from tests.performance.foundry_l1 import LaunchConfiguration, generation_contract_digest
    previous = '8e096a3658ee49379c09c60d8e21b46a2d5704756d318889d63e4ae1b4f03304'
    assert generation_contract_digest() != previous
    stale = SimpleNamespace(contract=None, policy=None, generation_contract_sha256=previous,
                            governance_policy=SimpleNamespace(evaluation=None))
    with pytest.raises(ValueError, match='generation contract'):
        LaunchConfiguration.bounded(stale)


@pytest.mark.parametrize('character', ['x', 'é', '😀', '\\', '"'])
def test_valid_canonical_envelope_compatibility(character):
    model = fixture(8, text=character*50)
    raw = encode(model).decode()
    # Fill to exactly 10,000 canonical bytes with valid, schema-bounded prose.
    remaining = 10000-len(raw)
    claims = list(model.claims)
    for i, claim in enumerate(claims):
        amount = min(remaining, 4096-len(claim.text))
        claims[i] = claim.model_copy(update={'text': claim.text+'x'*amount})
        remaining -= amount
    raw = encode(model.model_copy(update={'claims': tuple(claims)})).decode()
    assert len(raw.encode()) == 10000
    response = Response(payload(choices=[{'message': {'content': raw}, 'finish_reason': 'stop'}]))
    assert len(response.raw) < 26192
    assert client(response).execute(generation()).text == raw
