import json

from ui.api_client import stream_query


class FakeResponse:
    def raise_for_status(self):
        pass

    def iter_lines(self, decode_unicode=False):
        assert decode_unicode is True
        return iter(
            [
                json.dumps({"type": "metadata", "session_id": "session-7"}),
                json.dumps({"type": "chunk", "content": "answer"}),
                json.dumps({"type": "done", "response": "answer"}),
            ]
        )


def test_one_user_request_uses_one_http_generation_path():
    calls = []

    def post(*args, **kwargs):
        calls.append((args, kwargs))
        return FakeResponse()

    events = list(stream_query("http://api/query/stream", "hello", "session-7", 10, post=post))

    assert len(calls) == 1
    assert calls[0][1]["json"]["session_id"] == "session-7"
    assert [event["type"] for event in events] == ["metadata", "chunk", "done"]
