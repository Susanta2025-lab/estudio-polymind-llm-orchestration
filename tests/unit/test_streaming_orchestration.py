import json
import logging

import pytest

from llm.inference import InferenceConnectionError, ModelRole
from llm.operational import reset_request_id, set_request_id
from memory.memory_store import RedisMemoryStore
from rag.vector_store import VectorStoreError

from graph import streaming  # noqa: E402


class FakeProvider:
    name = "fake"

    def __init__(self, chunks=None, error=None):
        self.chunks = chunks or []
        self.error = error
        self.calls = []

    def model_id(self, role):
        return f"served-{role.value}"

    def generate(self, prompt, role):
        raise AssertionError("streaming must not call non-streaming inference")

    def generate_stream(self, prompt, role):
        self.calls.append((prompt, role))
        if self.error:
            raise self.error
        yield from self.chunks


def test_direct_stream_preserves_session_metadata_and_persists_once(monkeypatch):
    persisted = []
    monkeypatch.setattr(streaming, "direct_prompt", lambda query, session, memory=None: f"{session}:{query}")
    monkeypatch.setattr(streaming, "persist_exchange", lambda *args: persisted.append(args))
    provider = FakeProvider(["hello", " world"])

    events = list(
        streaming.stream_rag_response(
            "question", "session-42", provider, route_query=lambda query: "direct"
        )
    )

    assert len(provider.calls) == 1
    assert provider.calls[0][1] is ModelRole.GENERAL
    assert events[0]["session_id"] == "session-42"
    assert events[0]["route"] == "direct"
    assert events[-1] == {"type": "done", "response": "hello world"}
    assert len(persisted) == 1
    assert persisted[0][:3] == ("question", "hello world", "session-42")


def test_rag_stream_propagates_sources_and_uses_same_request(monkeypatch):
    monkeypatch.setattr(
        streaming,
        "rag_prompt_and_sources",
        lambda query, session, memory_store=None: (
            f"rag-history:{session}\nquery:{query}",
            "context",
            [{"source": "doc.pdf", "chunk_id": 3, "rerank_score": 0.9}],
        ),
    )
    provider = FakeProvider(["grounded"])

    events = list(
        streaming.stream_rag_response(
            "what is rag", "rag-session", provider, route_query=lambda query: "rag"
        )
    )

    assert len(provider.calls) == 1
    assert "rag-history:rag-session" in provider.calls[0][0]
    assert events[0]["sources"] == [
        {"source": "doc.pdf", "chunk_id": 3, "score": None, "rerank_score": 0.9}
    ]


def test_tool_route_does_not_invoke_inference(monkeypatch):
    monkeypatch.setattr(streaming, "tool_answer", lambda query: "tool answer")
    provider = FakeProvider(["must not run"])

    events = list(
        streaming.stream_rag_response(
            "what time is it", "tool-session", provider, route_query=lambda query: "tool"
        )
    )

    assert provider.calls == []
    assert events[1] == {"type": "chunk", "content": "tool answer"}


def test_upstream_failure_is_a_sanitized_visible_event(monkeypatch):
    monkeypatch.setattr(streaming, "direct_prompt", lambda query, session, memory=None: query)
    provider = FakeProvider(error=InferenceConnectionError("private diagnostics"))

    events = list(
        streaming.stream_rag_response(
            "question", "session", provider, route_query=lambda query: "direct"
        )
    )

    assert events[-1] == {"type": "error", "message": "Inference service is unavailable."}
    assert "private diagnostics" not in events[-1]["message"]


def test_partial_stream_failure_is_not_retried_or_persisted(monkeypatch):
    persisted = []
    monkeypatch.setattr(streaming, "direct_prompt", lambda query, session, memory=None: query)
    monkeypatch.setattr(streaming, "persist_exchange", lambda *args: persisted.append(args))

    class PartialProvider(FakeProvider):
        def generate_stream(self, prompt, role):
            self.calls.append((prompt, role))
            yield "partial"
            raise InferenceConnectionError("private diagnostics")

    provider = PartialProvider()
    events = list(streaming.stream_rag_response("question", "session", provider, lambda _: "direct"))

    assert [event["type"] for event in events] == ["metadata", "chunk", "error"]
    assert len(provider.calls) == 1
    assert persisted == []


def test_vector_failure_is_a_sanitized_ndjson_event(monkeypatch):
    def fail(*args, **kwargs):
        raise VectorStoreError("vector_unreachable")

    monkeypatch.setattr(streaming, "rag_prompt_and_sources", fail)
    events = list(
        streaming.stream_rag_response(
            "private query", "session", FakeProvider(["unused"]), lambda _: "rag"
        )
    )
    assert events == [{"type": "error", "message": "Knowledge retrieval is unavailable."}]


@pytest.mark.parametrize("operation", ["read", "append"])
def test_memory_failure_logs_no_chained_secrets_or_content(operation, caplog):
    # Fake credentials/content only; the real store normalizes this fake client's error.
    sentinels = (
        "phase16-user-secret", "phase16-password-secret", "example.invalid",
        "rediss://phase16-user-secret:phase16-password-secret@example.invalid:6380/0",
        "PHASE16_PRIVATE_MESSAGE_CONTENT",
    )

    class FailingClient:
        def lrange(self, *args):
            if operation == "read":
                raise ConnectionError(" ".join(sentinels))
            return []

        def pipeline(self, **kwargs):
            raise ConnectionError(" ".join(sentinels))

    store = RedisMemoryStore(FailingClient(), history_limit=6)
    token = set_request_id("phase16-memory-request")
    try:
        with caplog.at_level(logging.ERROR, logger=streaming.__name__):
            events = list(streaming.stream_rag_response(
                "PHASE16_PRIVATE_QUERY", "PHASE16_PRIVATE_SESSION",
                FakeProvider(["synthetic answer"]), lambda _: "direct", store,
            ))
    finally:
        reset_request_id(token)

    assert events[-1] == {"type": "error", "message": "Conversation memory is unavailable."}
    assert [event["type"] for event in events] == (
        ["error"] if operation == "read" else ["metadata", "chunk", "error"]
    )
    records = [record for record in caplog.records if record.name == streaming.__name__]
    assert len(records) == 1
    assert records[0].getMessage() == (
        "Memory operation failed request_id=phase16-memory-request "
        "route=direct provider=redis category=memory_unreachable"
    )
    for sentinel in sentinels:
        assert sentinel not in caplog.text
        assert sentinel not in json.dumps(events)
        assert all(sentinel not in (record.exc_text or "") for record in records)
    assert "PHASE16_PRIVATE_QUERY" not in caplog.text
    assert "PHASE16_PRIVATE_SESSION" not in caplog.text
    assert all(record.exc_info is None and record.exc_text is None for record in records)
