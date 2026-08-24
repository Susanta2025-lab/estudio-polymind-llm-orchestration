import sys
from types import ModuleType

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
    monkeypatch.setattr(api_module.inference_provider, "check_readiness", lambda: result(ReadinessStatus.READY))
    ready = api_module.readiness()
    monkeypatch.setattr(api_module.inference_provider, "check_readiness", lambda: result(ReadinessStatus.AUTHENTICATION_FAILURE))
    unavailable = api_module.readiness()
    assert ready.status_code == 200
    assert ready.body == b'{"status":"ready","provider":"fake","inference":{"status":"ready","provider":"fake"},"memory":{"status":"ready","provider":"file"},"models":{"general":"served"}}'
    assert unavailable.status_code == 503
    assert b'"status":"authentication_failure"' in unavailable.body


def test_request_id_is_generated_or_accepts_only_bounded_safe_input():
    generated = normalize_request_id(None)
    assert len(generated) == 32
    assert normalize_request_id("client-id:42") == "client-id:42"
    assert normalize_request_id("unsafe id with spaces") != "unsafe id with spaces"
    assert normalize_request_id("a" * 65) != "a" * 65


def test_application_status_is_normalized_by_category():
    assert application_status(InferenceAuthenticationError("safe")) == 503
    assert application_status(InferenceResponseError("safe")) == 502
