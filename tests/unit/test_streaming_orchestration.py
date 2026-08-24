from llm.inference import InferenceConnectionError, ModelRole

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
