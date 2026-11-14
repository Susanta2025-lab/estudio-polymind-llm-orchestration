import json

import pytest
import requests

from ui.api_client import APIStreamError, stream_query


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


@pytest.mark.parametrize("lines,exception,message", [
    (['{"type":"error","message":"Request failed."}'], None, None),
    (["invalid json"], APIStreamError, "malformed stream"),
    (["[]"], APIStreamError, "invalid stream event"),
    (["{}"], APIStreamError, "invalid stream event"),
])
def test_stream_errors_and_response_cleanup(lines, exception, message):
    closed = []

    class Response(FakeResponse):
        def iter_lines(self, decode_unicode=False):
            return iter(lines)

        def close(self):
            closed.append(True)

    events = stream_query("http://api/query/stream", "hello", "s", 10,
                          post=lambda *a, **k: Response())
    if exception:
        with pytest.raises(exception, match=message):
            list(events)
    else:
        assert list(events) == [{"type": "error", "message": "Request failed."}]
    assert closed == [True]


def test_stream_connection_failure_is_normalized():
    def unavailable(*args, **kwargs):
        raise requests.ConnectionError("upstream private detail")

    with pytest.raises(APIStreamError, match="Unable to connect to the PolyMind API") as error:
        list(stream_query("http://api/query/stream", "hello", "s", 10, post=unavailable))
    assert "private detail" not in str(error.value)
