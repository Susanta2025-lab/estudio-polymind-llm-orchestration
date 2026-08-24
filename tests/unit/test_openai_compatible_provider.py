import json

import pytest
import requests

from llm.inference import (
    InferenceAuthenticationError,
    InferenceConnectionError,
    InferenceError,
    InferenceModelUnavailableError,
    InferenceRateLimitError,
    InferenceResponseError,
    InferenceTimeoutError,
    ModelRole,
)
from llm.openai_compatible import OpenAICompatibleProvider


class FakeResponse:
    def __init__(self, payload=None, lines=(), error=None, iteration_error=None):
        self.payload = payload
        self.lines = lines
        self.error = error
        self.iteration_error = iteration_error
        self.closed = False

    def raise_for_status(self):
        if self.error:
            raise self.error

    def json(self):
        if isinstance(self.payload, Exception):
            raise self.payload
        return self.payload

    def iter_lines(self, decode_unicode=False):
        assert decode_unicode is True
        yield from self.lines
        if self.iteration_error:
            raise self.iteration_error

    def close(self):
        self.closed = True


class FakeHTTP:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error
        self.calls = []

    def post(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        if self.error:
            raise self.error
        return self.response


def provider(response=None, *, error=None, api_key=None, parameters=None):
    return OpenAICompatibleProvider(
        base_url="http://inference.example/v1/",
        api_key=api_key,
        model_map={role.value: f"served-{role.value}" for role in ModelRole},
        connect_timeout=2,
        read_timeout=30,
        generation_parameters=parameters,
        http_client=FakeHTTP(response, error),
    )


def sse(payload):
    return f"data: {json.dumps(payload)}"


def test_normal_chat_completion_uses_protocol_configuration_and_closes_response():
    response = FakeResponse({"choices": [{"message": {"content": "hello"}}]})
    client = provider(response, api_key="private-token", parameters={"temperature": 0.2})

    assert client.generate("prompt", ModelRole.CODING) == "hello"
    assert response.closed is True
    args, request = client.http_client.calls[0]
    assert args == ("http://inference.example/v1/chat/completions",)
    assert request["json"] == {
        "model": "served-coding",
        "messages": [{"role": "user", "content": "prompt"}],
        "stream": False,
        "temperature": 0.2,
    }
    assert request["headers"]["Authorization"] == "Bearer private-token"
    assert request["timeout"] == (2, 30)
    assert request["stream"] is False


def test_api_key_is_optional():
    response = FakeResponse({"choices": [{"message": {"content": "hello"}}]})
    client = provider(response)

    client.generate("prompt")

    assert "Authorization" not in client.http_client.calls[0][1]["headers"]


def test_streaming_sse_yields_content_ignores_role_chunk_and_stops_at_done():
    response = FakeResponse(
        lines=[
            ": keep-alive",
            sse({"choices": [{"delta": {"role": "assistant"}}]}),
            sse({"choices": [{"delta": {"content": "one"}}]}),
            "",
            sse({"choices": [{"delta": {"content": " two"}}]}),
            sse({"choices": [], "usage": {"completion_tokens": 2}}),
            "data: [DONE]",
            sse({"choices": [{"delta": {"content": "ignored"}}]}),
        ]
    )
    client = provider(response)

    assert list(client.generate_stream("prompt", ModelRole.FAST)) == ["one", " two"]
    assert response.closed is True
    request = client.http_client.calls[0][1]
    assert request["json"]["stream"] is True
    assert request["stream"] is True


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"choices": []},
        {"choices": [{}]},
        {"choices": [{"message": {}}]},
        {"choices": [{"message": {"content": 3}}]},
    ],
)
def test_invalid_completion_structure_is_normalized_and_closed(payload):
    response = FakeResponse(payload)

    with pytest.raises(InferenceResponseError, match="invalid response"):
        provider(response).generate("prompt")

    assert response.closed is True


def test_malformed_non_streaming_json_is_normalized():
    response = FakeResponse(ValueError("private malformed body"))

    with pytest.raises(InferenceResponseError, match="invalid response") as caught:
        provider(response).generate("prompt")

    assert "private" not in str(caught.value)
    assert response.closed is True


@pytest.mark.parametrize(
    "line",
    [
        "data: not-json",
        sse({}),
        sse({"choices": []}),
        sse({"choices": [{"delta": {"content": 3}}]}),
        "event: completion",
    ],
)
def test_malformed_sse_is_normalized_and_closed(line):
    response = FakeResponse(lines=[line, "data: [DONE]"])

    with pytest.raises(InferenceResponseError, match="malformed stream"):
        list(provider(response).generate_stream("prompt"))

    assert response.closed is True


def test_stream_must_end_with_done_marker():
    response = FakeResponse(
        lines=[sse({"choices": [{"delta": {"content": "partial"}}]})]
    )

    with pytest.raises(InferenceResponseError, match="before completion"):
        list(provider(response).generate_stream("prompt"))

    assert response.closed is True


def test_http_error_is_sanitized_in_exception_and_logs_and_response_is_closed(caplog):
    upstream = requests.HTTPError("secret response body")
    upstream.response = type("ErrorResponse", (), {"status_code": 503})()
    response = FakeResponse(error=upstream)

    with pytest.raises(InferenceConnectionError, match="temporarily unavailable") as caught:
        provider(response, api_key="secret-key").generate("prompt")

    assert "secret" not in str(caught.value)
    assert "secret" not in caplog.text
    assert response.closed is True


def test_connection_error_is_normalized():
    client = provider(error=requests.ConnectionError("private host details"))

    with pytest.raises(InferenceConnectionError, match="provider request failed") as caught:
        client.generate("prompt")

    assert "private" not in str(caught.value)


@pytest.mark.parametrize("stream", [False, True])
def test_request_timeout_is_normalized(stream):
    client = provider(error=requests.Timeout("private timeout details"))

    with pytest.raises(InferenceTimeoutError, match="request timed out") as caught:
        result = client.generate_stream("prompt") if stream else client.generate("prompt")
        if stream:
            list(result)

    assert "private" not in str(caught.value)


def test_timeout_while_reading_stream_is_normalized_and_closed():
    response = FakeResponse(iteration_error=requests.Timeout("private read timeout"))

    with pytest.raises(InferenceTimeoutError, match="request timed out"):
        list(provider(response).generate_stream("prompt"))

    assert response.closed is True


def test_model_mapping_failure_is_provider_neutral():
    client = OpenAICompatibleProvider(
        base_url="http://inference.example/v1",
        model_map={},
        http_client=FakeHTTP(),
    )

    with pytest.raises(InferenceResponseError, match="role 'general'"):
        client.model_id(ModelRole.GENERAL)


def test_reserved_generation_parameters_are_rejected():
    with pytest.raises(ValueError, match="reserved keys"):
        provider(parameters={"model": "override"})


@pytest.mark.parametrize(("status", "error_type"), [
    (400, InferenceError),
    (401, InferenceAuthenticationError),
    (403, InferenceAuthenticationError),
    (404, InferenceModelUnavailableError),
    (408, InferenceTimeoutError),
    (429, InferenceRateLimitError),
    (500, InferenceError),
    (502, InferenceRateLimitError),
    (503, InferenceRateLimitError),
    (504, InferenceTimeoutError),
])
def test_generation_http_statuses_have_provider_neutral_categories(status, error_type):
    upstream = requests.HTTPError("private upstream body")
    upstream.response = type("ErrorResponse", (), {"status_code": status})()
    response = FakeResponse(error=upstream)
    with pytest.raises(error_type) as caught:
        provider(response).generate("prompt")
    assert "private" not in str(caught.value)
