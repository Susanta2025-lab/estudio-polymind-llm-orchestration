import json

import pytest
import requests
from prometheus_client import CollectorRegistry

from llm.inference import InferenceConnectionError, ModelRole, ReadinessResult, ReadinessStatus
from llm.metrics import Metrics
from llm.ollama_client import OllamaClient
from llm.openai_compatible import OpenAICompatibleProvider


class Response:
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
        yield from self.lines

    def close(self):
        self.closed = True


class HTTP:
    def __init__(self, response):
        self.response = response
        self.calls = 0

    def post(self, *args, **kwargs):
        self.calls += 1
        return self.response


def metric_store():
    return Metrics(CollectorRegistry())


def openai_provider(response, store):
    return OpenAICompatibleProvider(
        base_url="http://inference/v1",
        model_map={role.value: f"served-{role.value}" for role in ModelRole},
        http_client=HTTP(response),
        metric_store=store,
    )


def sample_value(store, name, labels):
    return store.registry.get_sample_value(name, labels) or 0


def sse(payload):
    return f"data: {json.dumps(payload)}"


def test_success_and_normalized_failure_update_inference_metrics_once():
    successful = metric_store()
    openai_provider(
        Response({"choices": [{"message": {"content": "ok"}}]}), successful
    ).generate("secret prompt", ModelRole.GENERAL)
    labels = {
        "provider": "openai_compatible", "logical_role": "general",
        "served_model": "served-general", "operation": "generate", "outcome": "success",
    }
    assert sample_value(successful, "inference_requests_total", labels) == 1
    assert sample_value(successful, "inference_request_duration_seconds_count", labels) == 1

    failed = metric_store()
    error = requests.ConnectionError("raw-private-error")
    with pytest.raises(InferenceConnectionError):
        openai_provider(Response(error=error), failed).generate("prompt", ModelRole.GENERAL)
    error_labels = {**labels, "outcome": "error"}
    assert sample_value(failed, "inference_requests_total", error_labels) == 1
    assert sample_value(failed, "inference_errors_total", {
        "provider": "openai_compatible", "operation": "generate",
        "error_category": "provider_unreachable",
    }) == 1
    rendered = failed.render().decode()
    assert "raw-private-error" not in rendered
    assert "prompt" not in rendered


def test_ttft_ignores_metadata_and_records_first_content_once():
    store = metric_store()
    response = Response(lines=[
        sse({"choices": [{"delta": {"role": "assistant"}}]}),
        sse({"choices": [{"delta": {"content": ""}}]}),
        sse({"choices": [{"delta": {"content": "first"}}]}),
        sse({"choices": [{"delta": {"content": "second"}}]}),
        "data: [DONE]",
    ])
    assert list(openai_provider(response, store).generate_stream("prompt")) == ["first", "second"]
    labels = {
        "provider": "openai_compatible", "logical_role": "general",
        "served_model": "served-general",
    }
    assert sample_value(store, "inference_time_to_first_token_seconds_count", labels) == 1


def test_failure_before_content_has_no_fake_ttft_and_stream_is_error():
    store = metric_store()
    response = Response(lines=[
        sse({"choices": [{"delta": {"role": "assistant"}}]}),
        "data: malformed",
        "data: [DONE]",
    ])
    with pytest.raises(Exception):
        list(openai_provider(response, store).generate_stream("prompt"))
    base = {
        "provider": "openai_compatible", "logical_role": "general",
        "served_model": "served-general",
    }
    assert sample_value(store, "inference_time_to_first_token_seconds_count", base) == 0
    assert sample_value(store, "inference_stream_duration_seconds_count", {**base, "outcome": "error"}) == 1


def test_partial_stream_records_one_ttft_then_preserves_error_outcome():
    store = metric_store()
    response = Response(lines=[
        sse({"choices": [{"delta": {"content": "partial"}}]}),
        "data: malformed",
    ])
    with pytest.raises(Exception):
        list(openai_provider(response, store).generate_stream("prompt"))
    base = {
        "provider": "openai_compatible", "logical_role": "general",
        "served_model": "served-general",
    }
    assert sample_value(store, "inference_time_to_first_token_seconds_count", base) == 1
    assert sample_value(store, "inference_stream_duration_seconds_count", {**base, "outcome": "error"}) == 1


def test_openai_completion_and_stream_usage_are_exact_and_absence_is_honest():
    normal = metric_store()
    openai_provider(Response({
        "choices": [{"message": {"content": "ok"}}],
        "usage": {"prompt_tokens": 3, "completion_tokens": 2, "total_tokens": 5},
    }), normal).generate("prompt")
    base = {"provider": "openai_compatible", "logical_role": "general", "served_model": "served-general"}
    for token_type, expected in (("prompt", 3), ("completion", 2), ("total", 5)):
        assert sample_value(normal, "inference_tokens_total", {**base, "token_type": token_type}) == expected

    streamed = metric_store()
    lines = [
        sse({"choices": [{"delta": {"content": "ok"}}]}),
        sse({"choices": [], "usage": {"prompt_tokens": 4, "completion_tokens": 1, "total_tokens": 5}}),
        "data: [DONE]",
    ]
    list(openai_provider(Response(lines=lines), streamed).generate_stream("prompt"))
    assert sample_value(streamed, "inference_tokens_total", {**base, "token_type": "total"}) == 5

    absent = metric_store()
    openai_provider(Response({"choices": [{"message": {"content": "ok"}}]}), absent).generate("prompt")
    assert sample_value(absent, "inference_tokens_total", {**base, "token_type": "total"}) == 0


def test_ollama_native_usage_is_recorded_without_estimation():
    store = metric_store()
    response = Response({
        "message": {"content": "ok"}, "prompt_eval_count": 6, "eval_count": 4,
    })
    provider = OllamaClient(
        url="http://ollama/api/chat",
        model_map={role.value: f"ollama-{role.value}" for role in ModelRole},
        http_client=HTTP(response), metric_store=store,
    )
    provider.generate("prompt")
    base = {"provider": "ollama", "logical_role": "general", "served_model": "ollama-general"}
    assert sample_value(store, "inference_tokens_total", {**base, "token_type": "prompt"}) == 6
    assert sample_value(store, "inference_tokens_total", {**base, "token_type": "completion"}) == 4
    assert sample_value(store, "inference_tokens_total", {**base, "token_type": "total"}) == 10


def test_readiness_and_application_metrics_use_bounded_dimensions():
    store = metric_store()
    result = ReadinessResult(ReadinessStatus.TIMEOUT, "fake", {"general": "served"})
    store.observe_readiness(result, 0.25)
    store.observe_application("user-controlled-route", "query", "error", 0.5)
    assert sample_value(store, "readiness_checks_total", {"provider": "fake", "outcome": "timeout"}) == 1
    assert sample_value(store, "readiness_check_duration_seconds_count", {"provider": "fake", "outcome": "timeout"}) == 1
    assert sample_value(store, "application_requests_total", {
        "route": "unknown", "operation": "query", "outcome": "error",
    }) == 1
    output = store.render().decode()
    for forbidden in ("request_id", "session_id", "user-controlled-route"):
        assert forbidden not in output


def test_active_request_and_stream_metrics_cleanup_on_success_and_cancellation():
    store = metric_store()
    with store.active_request("query"):
        assert sample_value(store, "active_application_requests", {"operation": "query"}) == 1
    assert sample_value(store, "active_application_requests", {"operation": "query"}) == 0

    stream = store.active_stream()
    stream.__enter__()
    assert sample_value(store, "active_ndjson_streams", {}) == 1
    stream.__exit__(GeneratorExit, GeneratorExit(), None)
    assert sample_value(store, "active_ndjson_streams", {}) == 0
    assert sample_value(store, "ndjson_stream_outcomes_total", {"outcome": "cancelled"}) == 1
