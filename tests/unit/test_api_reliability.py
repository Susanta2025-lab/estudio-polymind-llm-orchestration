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


class Provider:
    def check_readiness(self):
        return result(ReadinessStatus.READY)


generation = ModuleType("graph.generation")
generation.public_sources = lambda sources: sources
flow = ModuleType("graph.langgraph_flow")
flow.app_graph = type("Graph", (), {"invoke": lambda self, state: {}})()
flow.inference_provider = Provider()
streaming = ModuleType("graph.streaming")
streaming.stream_rag_response = lambda *args: iter(())
memory = ModuleType("memory.memory_store")
memory.get_history = lambda session: []
logging_utils = ModuleType("utils.logger")
logging_utils.log_request = lambda **kwargs: None
_stubs = {
    "graph.generation": generation,
    "graph.langgraph_flow": flow,
    "graph.streaming": streaming,
    "memory.memory_store": memory,
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


def test_ready_returns_sanitized_200_or_503(monkeypatch):
    monkeypatch.setattr(api_module.inference_provider, "check_readiness", lambda: result(ReadinessStatus.READY))
    ready = api_module.readiness()
    monkeypatch.setattr(api_module.inference_provider, "check_readiness", lambda: result(ReadinessStatus.AUTHENTICATION_FAILURE))
    unavailable = api_module.readiness()
    assert ready.status_code == 200
    assert ready.body == b'{"status":"ready","provider":"fake","models":{"general":"served"}}'
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
