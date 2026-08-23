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
from llm.openai_compatible import OpenAICompatibleProvider


class ContractResponse:
    def __init__(self, payload=None, lines=(), error=None):
        self.payload = payload
        self.lines = lines
        self.error = error
        self.closed = False

    def raise_for_status(self):
        if self.error:
            raise self.error

    def json(self):
        return self.payload

    def iter_lines(self, decode_unicode=False):
        return iter(self.lines)

    def close(self):
        self.closed = True


class ContractHTTP:
    def __init__(self, response):
        self.response = response

    def post(self, *args, **kwargs):
        return self.response


def make_provider(kind, response):
    model_map = {role.value: f"contract-{role.value}" for role in ModelRole}
    if kind == "ollama":
        return OllamaClient(
            url="http://ollama/api/chat",
            model_map=model_map,
            http_client=ContractHTTP(response),
        )
    return OpenAICompatibleProvider(
        base_url="http://inference/v1",
        model_map=model_map,
        http_client=ContractHTTP(response),
    )


@pytest.mark.parametrize("kind", ["ollama", "openai_compatible"])
def test_provider_contract_model_roles_resolve_independently(kind):
    client = make_provider(kind, ContractResponse())

    assert [client.model_id(role) for role in ModelRole] == [
        f"contract-{role.value}" for role in ModelRole
    ]


@pytest.mark.parametrize(
    ("kind", "payload"),
    [
        ("ollama", {"message": {"content": "answer"}}),
        ("openai_compatible", {"choices": [{"message": {"content": "answer"}}]}),
    ],
)
def test_provider_contract_normal_generation_and_cleanup(kind, payload):
    response = ContractResponse(payload=payload)

    assert make_provider(kind, response).generate("prompt") == "answer"
    assert response.closed is True


@pytest.mark.parametrize(
    ("kind", "lines"),
    [
        ("ollama", [json.dumps({"message": {"content": "token"}}).encode()]),
        (
            "openai_compatible",
            [
                'data: {"choices":[{"delta":{"content":"token"}}]}',
                "data: [DONE]",
            ],
        ),
    ],
)
def test_provider_contract_streaming_generation_and_cleanup(kind, lines):
    response = ContractResponse(lines=lines)

    assert list(make_provider(kind, response).generate_stream("prompt")) == ["token"]
    assert response.closed is True


@pytest.mark.parametrize("kind", ["ollama", "openai_compatible"])
def test_provider_contract_connection_errors_are_normalized_and_sanitized(kind):
    response = ContractResponse(error=requests.ConnectionError("private details"))

    with pytest.raises(InferenceConnectionError) as caught:
        make_provider(kind, response).generate("prompt")

    assert "private" not in str(caught.value)
    assert response.closed is True


@pytest.mark.parametrize("kind", ["ollama", "openai_compatible"])
def test_provider_contract_timeouts_are_normalized_and_cleaned_up(kind):
    response = ContractResponse(error=requests.Timeout("private timeout details"))

    with pytest.raises(InferenceTimeoutError) as caught:
        make_provider(kind, response).generate("prompt")

    assert "private" not in str(caught.value)
    assert response.closed is True


@pytest.mark.parametrize(
    ("kind", "lines"),
    [
        ("ollama", [b"not-json"]),
        ("openai_compatible", ["data: not-json", "data: [DONE]"]),
    ],
)
def test_provider_contract_malformed_streams_are_normalized_and_cleaned_up(kind, lines):
    response = ContractResponse(lines=lines)

    with pytest.raises(InferenceResponseError):
        list(make_provider(kind, response).generate_stream("prompt"))

    assert response.closed is True
