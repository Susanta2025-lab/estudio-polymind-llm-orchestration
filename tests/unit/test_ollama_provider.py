import json

import pytest
import requests

from llm.inference import (
    InferenceConnectionError,
    InferenceResponseError,
    InferenceTimeoutError,
    ModelRole,
)
from llm.ollama_client import OllamaClient


class FakeResponse:
    def __init__(self, payload=None, lines=(), error=None):
        self.payload = payload
        self.lines = lines
        self.error = error

    def raise_for_status(self):
        if self.error:
            raise self.error

    def json(self):
        return self.payload

    def iter_lines(self):
        return iter(self.lines)


class FakeHTTP:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def post(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return self.response


def provider(response):
    return OllamaClient(
        url="http://ollama/api/chat",
        model_map={role.value: f"served-{role.value}" for role in ModelRole},
        connect_timeout=2,
        read_timeout=30,
        http_client=FakeHTTP(response),
    )


def test_normal_response_and_configured_model_mapping():
    client = provider(FakeResponse({"message": {"content": "hello"}}))

    assert client.generate("prompt", ModelRole.CODING) == "hello"
    assert client.model_id(ModelRole.CODING) == "served-coding"
    _, request = client.http_client.calls[0]
    assert request["json"]["model"] == "served-coding"
    assert request["timeout"] == (2, 30)


def test_provider_failure_is_normalized_without_response_body():
    upstream = requests.HTTPError("secret upstream response body")
    client = provider(FakeResponse(error=upstream))

    with pytest.raises(InferenceConnectionError, match="provider request failed") as caught:
        client.generate("prompt", ModelRole.GENERAL)

    assert "secret" not in str(caught.value)


def test_normal_streaming_chunks():
    lines = [
        json.dumps({"message": {"content": "one"}}).encode(),
        b"",
        json.dumps({"message": {"content": " two"}}).encode(),
    ]
    client = provider(FakeResponse(lines=lines))

    assert list(client.generate_stream("prompt", ModelRole.FAST)) == ["one", " two"]


def test_malformed_stream_chunk_is_reported():
    client = provider(FakeResponse(lines=[b"not-json"]))

    with pytest.raises(InferenceResponseError, match="malformed stream"):
        list(client.generate_stream("prompt", ModelRole.GENERAL))


def test_streaming_upstream_failure_is_normalized():
    client = provider(FakeResponse(error=requests.ConnectionError("upstream details")))

    with pytest.raises(InferenceConnectionError, match="provider request failed"):
        list(client.generate_stream("prompt", ModelRole.GENERAL))


def test_timeout_is_distinguished_from_other_connection_failures():
    client = provider(FakeResponse(error=requests.Timeout("upstream details")))

    with pytest.raises(InferenceTimeoutError, match="request timed out"):
        client.generate("prompt", ModelRole.GENERAL)
