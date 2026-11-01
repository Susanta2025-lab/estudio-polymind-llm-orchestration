"""Content-free bounded diagnostics, using only synthetic envelopes."""
from dataclasses import asdict
import json

import pytest

from llm.inference import InferenceOutputLimitError, InferenceResponseError
from tests.unit.test_structured_provider import Response, client, payload, request


@pytest.mark.parametrize('size,reason,cause', [
    (2, 'stop', None), (2, None, None),
    (1001, 'stop', 'response_bytes_exceeded'),
    (2, 'length', 'provider_completion_truncated'),
    (2, 'max_tokens', 'provider_completion_truncated'),
    (1001, 'length', 'response_bytes_exceeded'),
    (1001, None, 'response_bytes_exceeded'),
    (1001, 'sensitive-provider-value', 'response_bytes_exceeded'),
])
@pytest.mark.parametrize('reasoning', [None, 0, 5])
def test_diagnostics(size, reason, cause, reasoning):
    value = payload(choices=[{'message': {'content': 'x'*size}, 'finish_reason': reason}])
    if reasoning is not None:
        value['usage']['completion_tokens_details'] = {'reasoning_tokens': reasoning, 'private': 'hidden'}
    p = client(Response(value))
    if cause is None:
        assert len(p.execute(request()).text) == size
    else:
        with pytest.raises(InferenceOutputLimitError) as caught:
            p.execute(request())
        d = asdict(caught.value.diagnostics)
        assert d == dict(failure_cause=cause, response_bytes=size, response_byte_limit=1000,
                        finish_reason=reason if reason != 'sensitive-provider-value' else 'other',
                        completion_tokens=7, completion_token_limit=500,
                        reasoning_tokens=reasoning, usage_available=True)
        assert 'hidden' not in json.dumps(d) and 'sensitive-provider-value' not in json.dumps(d)
    assert len(p.http_client.calls) == 1


@pytest.mark.parametrize('usage', ['private', {'prompt_tokens': 'secret'},
    {'prompt_tokens': True}, {'prompt_tokens': 1, 'completion_tokens': 2, 'total_tokens': 4},
    {'completion_tokens': 7, 'completion_tokens_details': []},
    {'completion_tokens': 7, 'completion_tokens_details': {'reasoning_tokens': True}},
    {'completion_tokens': 7, 'completion_tokens_details': {'reasoning_tokens': 8}},
    {'completion_tokens': 7, 'completion_tokens_details': {'reasoning_tokens': -1}},
])
def test_invalid_usage_fails_closed(usage):
    with pytest.raises(InferenceResponseError) as caught:
        client(Response(payload(usage=usage))).execute(request())
    assert caught.value.usage is None
    assert 'secret' not in str(caught.value)


@pytest.mark.parametrize('usage,available,completion', [(None, False, None), ({}, False, None),
    ({'completion_tokens': 0}, False, 0),
    ({'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}, True, 0)])
def test_missing_is_not_zero(usage, available, completion):
    value = payload(usage=usage, choices=[{'message': {'content': '{}'}, 'finish_reason': 'length'}])
    with pytest.raises(InferenceOutputLimitError) as caught:
        client(Response(value)).execute(request())
    assert caught.value.diagnostics.usage_available is available
    assert caught.value.diagnostics.completion_tokens == completion


def test_envelope_bound_is_unknown_content_cause():
    with pytest.raises(InferenceOutputLimitError) as caught:
        client(Response(raw=b'x'*15000)).execute(request())
    d = caught.value.diagnostics
    assert d.failure_cause == 'unknown' and d.response_bytes is None and d.finish_reason is None
    assert d.response_byte_limit == 1000 and d.completion_token_limit == 500


@pytest.mark.parametrize('reason', [[], {}, 7])
def test_malformed_finish_metadata(reason):
    with pytest.raises(InferenceResponseError):
        client(Response(payload(choices=[{'message': {'content': 'x'*1001}, 'finish_reason': reason}]))).execute(request())


def test_response_length_counts_utf8_bytes():
    value = payload(choices=[{'message': {'content': 'é'*501}, 'finish_reason': 'stop'}])
    with pytest.raises(InferenceOutputLimitError) as caught:
        client(Response(value)).execute(request())
    assert caught.value.diagnostics.response_bytes == 1002
