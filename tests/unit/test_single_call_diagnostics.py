"""Closed rejection diagnostics; external networking is forbidden."""
import json
import socket
import pytest
from llm.bounded_http import request_json
from llm.inference import InferenceConfigurationError
from tests.unit.test_structured_provider import HTTP, Response


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    def deny(*a, **k): raise AssertionError('External network forbidden')
    for name in ('connect', 'connect_ex', 'sendto'): monkeypatch.setattr(socket.socket, name, deny)
    monkeypatch.setattr(socket, 'getaddrinfo', deny)


@pytest.mark.parametrize('status', [400, 422])
@pytest.mark.parametrize('error,expected', [
    ({'code':'invalid_json_schema', 'param':'response_format', 'message':'SECRET'}, 'strict_schema_rejected'),
    ({'code':'invalid_request_error', 'param':'response_format',
      'message':"Invalid schema for response_format 'private': nesting"}, 'strict_schema_rejected'),
    ({'code':'invalid_request_error', 'param':'response_format', 'message':'SECRET'}, 'request_configuration'),
    ({'code':'invalid_json_schema', 'param':'unrelated'}, 'request_configuration'),
    ({'code':['invalid_json_schema'], 'param':{}}, 'request_configuration'),
    ({'code':'arbitrary SECRET', 'message':'SECRET'}, 'request_configuration'),
    ('SECRET', 'request_configuration'),
    ({'code':'invalid_json_schema', 'param':'response_format', 'message':'x'*5000}, 'request_configuration'),
])
def test_bounded_closed_diagnostics(status, error, expected):
    response = Response({'error':error}, status=status)
    http = HTTP(response)
    with pytest.raises(InferenceConfigurationError) as caught:
        request_json(http, 'https://synthetic.invalid', headers={}, payload={}, timeout=(1,1),
                     total_seconds=1, max_bytes=26192)
    assert caught.value.rejection_diagnostics == {'http_status':status, 'reason':expected}
    assert 'SECRET' not in str(caught.value)
    assert len(http.calls) == 1 and response.closed


@pytest.mark.parametrize('raw', [b'not-json', b'[]', b'null', b'{"error":', b'\xff'])
def test_malformed_rejection_keeps_status_classification(raw):
    http = HTTP(Response(raw=raw, status=400))
    with pytest.raises(InferenceConfigurationError) as caught:
        request_json(http, 'https://synthetic.invalid', headers={}, payload={}, timeout=(1,1),
                     total_seconds=1, max_bytes=26192)
    assert caught.value.rejection_diagnostics['reason'] == 'request_configuration'
