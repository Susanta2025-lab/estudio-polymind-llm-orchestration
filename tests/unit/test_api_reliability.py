import sys
import asyncio
import json
from types import ModuleType

import pytest
from llm.inference import (
    InferenceAuthenticationError,
    InferenceResponseError,
    ModelRole,
    ReadinessResult,
    ReadinessStatus,
)
from llm.operational import application_status, normalize_request_id
from llm.metrics import Metrics
from prometheus_client import CollectorRegistry
from pydantic import SecretStr

from api.security import ApplicationSecurityMiddleware, documentation_urls


class Provider:
    def check_readiness(self):
        return result(ReadinessStatus.READY)


generation = ModuleType("graph.generation")
generation.public_sources = lambda sources: sources
flow = ModuleType("graph.langgraph_flow")
flow.app_graph = type("Graph", (), {"invoke": lambda self, state: {}})()
flow.inference_provider = Provider()
flow.memory_store = type("Memory", (), {
    "provider": "file",
    "check_readiness": lambda self: type("Result", (), {"ready": True, "status": "ready", "provider": "file"})(),
    "get_history": lambda self, session: [],
})()
streaming = ModuleType("graph.streaming")
streaming.stream_rag_response = lambda *args: iter(())
memory = ModuleType("memory.memory_store")
memory.MemoryError = type("MemoryError", (RuntimeError,), {"category": "memory_failure"})
memory_provider = ModuleType("memory.provider_factory")
memory_provider.close_memory_store = lambda: None
logging_utils = ModuleType("utils.logger")
logging_utils.log_request = lambda **kwargs: None
_stubs = {
    "graph.generation": generation,
    "graph.langgraph_flow": flow,
    "graph.streaming": streaming,
    "memory.memory_store": memory,
    "memory.provider_factory": memory_provider,
    "utils.logger": logging_utils,
}
_previous = {name: sys.modules.get(name) for name in _stubs}
sys.modules.update(_stubs)

from api import app as api_module

for _name, _module in _previous.items():
    if _module is None:
        sys.modules.pop(_name, None)
    else:
        sys.modules[_name] = _module


def result(status):
    return ReadinessResult(status, "fake", {ModelRole.GENERAL.value: "served"})


def test_health_is_independent_of_provider(monkeypatch):
    monkeypatch.setattr(api_module.inference_provider, "check_readiness", lambda: (_ for _ in ()).throw(AssertionError()))
    assert api_module.liveness() == {"status": "alive"}


def test_memory_unavailable_makes_readiness_fail_but_not_liveness(monkeypatch):
    monkeypatch.setattr(api_module, "check_vector_store_readiness", lambda: type("Result", (), {"ready": True, "status": "ready", "provider": "chroma_http", "corpus_version": "v1"})())
    monkeypatch.setattr(api_module.inference_provider, "check_readiness", lambda: result(ReadinessStatus.READY))
    unavailable = type("MemoryResult", (), {"ready": False, "status": "memory_unreachable", "provider": "redis"})()
    monkeypatch.setattr(api_module.memory_store, "check_readiness", lambda: unavailable)
    response = api_module.readiness()
    assert response.status_code == 503
    assert b'"inference":{"status":"ready"' in response.body
    assert b'"memory":{"status":"memory_unreachable","provider":"redis"}' in response.body
    assert api_module.liveness() == {"status": "alive"}


def test_metrics_scrape_is_prometheus_text_and_provider_independent(monkeypatch):
    monkeypatch.setattr(api_module.inference_provider, "check_readiness", lambda: (_ for _ in ()).throw(AssertionError()))
    response = api_module.application_metrics()
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert b"inference_requests" in response.body


def test_tool_only_query_records_route_but_not_inference(monkeypatch):
    store = Metrics(CollectorRegistry())
    monkeypatch.setattr(api_module, "metrics", store)
    monkeypatch.setattr(api_module.app_graph, "invoke", lambda state: {
        "route": "tool", "model_role": "general", "model": "configured-model",
        "answer": "tool answer", "sources": [],
    })
    response = api_module.query(api_module.QueryRequest(query="what time is it"))
    output = store.render().decode()
    assert response["route"] == "tool"
    assert 'application_requests_total{operation="query",outcome="success",route="tool"} 1.0' in output
    assert 'inference_requests_total{' not in output


def test_ready_returns_sanitized_200_or_503(monkeypatch):
    monkeypatch.setattr(api_module, "check_vector_store_readiness", lambda: type("Result", (), {"ready": True, "status": "ready", "provider": "chroma_http"})())
    monkeypatch.setattr(api_module.inference_provider, "check_readiness", lambda: result(ReadinessStatus.READY))
    monkeypatch.setattr(api_module, "check_bm25_readiness", lambda **kwargs: type("Result", (), {"ready": True, "status": "ready", "loaded_version": "v1", "expected_version": "v1"})())
    ready = api_module.readiness()
    monkeypatch.setattr(api_module.inference_provider, "check_readiness", lambda: result(ReadinessStatus.AUTHENTICATION_FAILURE))
    unavailable = api_module.readiness()
    assert ready.status_code == 200
    assert ready.body == b'{"status":"ready","provider":"fake","inference":{"status":"ready","provider":"fake"},"memory":{"status":"ready","provider":"file"},"vector_store":{"status":"ready","provider":"chroma_http"},"bm25":{"status":"ready","loaded_version":"v1","expected_version":"v1"},"models":{"general":"served"}}'
    assert unavailable.status_code == 503
    assert b'"status":"authentication_failure"' in unavailable.body


def test_vector_unavailable_makes_readiness_fail_but_health_stays_alive(monkeypatch):
    monkeypatch.setattr(api_module.inference_provider, "check_readiness", lambda: result(ReadinessStatus.READY))
    monkeypatch.setattr(api_module, "check_vector_store_readiness", lambda: type("Result", (), {"ready": False, "status": "vector_unreachable", "provider": "chroma_http"})())
    response = api_module.readiness()
    assert response.status_code == 503
    assert b'"vector_store":{"status":"vector_unreachable","provider":"chroma_http"}' in response.body
    assert api_module.liveness() == {"status": "alive"}


def test_stale_bm25_makes_composite_readiness_fail(monkeypatch):
    monkeypatch.setattr(api_module.inference_provider, "check_readiness", lambda: result(ReadinessStatus.READY))
    monkeypatch.setattr(api_module, "check_vector_store_readiness", lambda: type("Result", (), {
        "ready": True, "status": "ready", "provider": "chroma_http", "corpus_version": "v2",
    })())
    monkeypatch.setattr(api_module, "check_bm25_readiness", lambda **kwargs: type("Result", (), {
        "ready": False, "status": "bm25_version_mismatch",
        "loaded_version": "v1", "expected_version": "v2",
    })())
    response = api_module.readiness()
    assert response.status_code == 503
    assert b'"bm25":{"status":"bm25_version_mismatch","loaded_version":"v1","expected_version":"v2"}' in response.body


def test_request_id_is_generated_or_accepts_only_bounded_safe_input():
    generated = normalize_request_id(None)
    assert len(generated) == 32
    assert normalize_request_id("client-id:42") == "client-id:42"
    assert normalize_request_id("unsafe id with spaces") != "unsafe id with spaces"
    assert normalize_request_id("a" * 65) != "a" * 65


def test_application_status_is_normalized_by_category():
    assert application_status(InferenceAuthenticationError("safe")) == 503
    assert application_status(InferenceResponseError("safe")) == 502


def security_response(path, authorization=None, body=b'{"query":"hello"}', enabled=True, limit=1024):
    sent = []
    consumed = []
    configuration = type("SecurityConfiguration", (), {
        "API_AUTH_ENABLED": enabled,
        "API_AUTH_TOKEN": SecretStr("synthetic-api-token-that-is-long-enough"),
        "MAX_REQUEST_BYTES": limit,
    })()

    async def downstream(_scope, receive, send):
        consumed.append(await receive())
        await send({"type": "http.response.start", "status": 204, "headers": []})
        await send({"type": "http.response.body", "body": b""})

    headers = [(b"content-length", str(len(body)).encode())]
    if authorization is not None:
        headers.append((b"authorization", authorization.encode()))
    scope = {"type": "http", "method": "POST", "path": path, "headers": headers}
    received = False

    async def receive():
        nonlocal received
        if received:
            return {"type": "http.disconnect"}
        received = True
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(message):
        sent.append(message)

    asyncio.run(ApplicationSecurityMiddleware(downstream, configuration)(scope, receive, send))
    status = next(message["status"] for message in sent if message["type"] == "http.response.start")
    response_body = b"".join(message.get("body", b"") for message in sent if message["type"] == "http.response.body")
    return status, response_body, consumed


def test_local_auth_disabled_preserves_query_access():
    status, _body, consumed = security_response("/query", enabled=False)
    assert status == 204
    assert consumed


@pytest.mark.parametrize("authorization", [None, "Basic value", "Bearer", "Bearer wrong", "Bearer value extra"])
def test_protected_query_rejects_missing_malformed_or_invalid_auth(monkeypatch, authorization):
    status, body, consumed = security_response("/query", authorization)
    assert status == 401
    assert json.loads(body) == {"detail": "Authentication required."}
    assert consumed == []
    assert "synthetic-api-token" not in body.decode()


def test_correct_token_protects_normal_streaming_and_memory_paths():
    token = "synthetic-api-token-that-is-long-enough"
    for path in ("/query", "/query/stream", "/memory/session"):
        status, _body, consumed = security_response(path, f"Bearer {token}")
        assert status == 204
        assert consumed
        assert security_response(path)[0] == 401


def test_auth_rejection_logs_and_metrics_do_not_contain_token(monkeypatch, caplog):
    token = "synthetic-api-token-that-must-not-leak"
    status, body, _consumed = security_response("/query", f"Bearer {token}-wrong")
    assert status == 401
    assert token not in caplog.text and token not in body.decode()


def test_request_size_limit_rejects_before_orchestration_for_query_and_stream():
    for path in ("/query", "/query/stream"):
        status, body, consumed = security_response(path, enabled=False, limit=32, body=b"x" * 64)
        assert status == 413
        assert json.loads(body) == {"detail": "Request body is too large."}
        assert consumed == []


def test_docs_urls_are_available_locally_and_disabled_in_production():
    assert documentation_urls(True) == ("/docs", "/redoc", "/openapi.json")
    assert documentation_urls(False) == (None, None, None)
