from argparse import Namespace
import io
import json
import urllib.error

import pytest

from scripts import capacity_baseline


class Response(io.BytesIO):
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.close()


def test_authenticated_stream_parses_ttft_and_done(monkeypatch):
    captured = {}

    def open_request(request, timeout):
        captured["authorization"] = request.headers["Authorization"]
        captured["timeout"] = timeout
        return Response(
            b'{"type":"metadata","route":"direct"}\n'
            b'{"type":"chunk","content":"ok"}\n'
            b'{"type":"done","response":"ok"}\n'
        )

    monkeypatch.setattr(capacity_baseline.urllib.request, "urlopen", open_request)
    result = capacity_baseline.one_request("http://api", "synthetic", "stream", 3, 1)
    assert result.success is True
    assert result.ttft_seconds is not None
    assert captured == {"authorization": "Bearer synthetic", "timeout": 3}


def test_http_errors_are_bounded_without_response_body(monkeypatch):
    monkeypatch.setattr(
        capacity_baseline.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            urllib.error.HTTPError("http://api", 503, "private", {}, None)
        ),
    )
    result = capacity_baseline.one_request("http://api", "token", "direct", 1, 1)
    assert result.error == "http_error"
    assert result.status == 503


def test_percentiles_and_safety_bounds():
    assert capacity_baseline.percentile([4, 1, 2, 3], 0.50) == 2
    args = Namespace(
        concurrency=33, requests=1, duration=0, base_url="", token="", workload="direct",
        timeout=1, image="", replicas=1, environment="", resources="",
    )
    with pytest.raises(ValueError, match="safety bounds"):
        capacity_baseline.execute(args)


def test_duration_mode_still_honors_request_cap(monkeypatch):
    monkeypatch.setattr(
        capacity_baseline, "one_request", lambda *_args: capacity_baseline.Observation(True, 0.001)
    )
    args = Namespace(
        concurrency=2, requests=3, duration=10, base_url="http://api", token="token",
        workload="direct", timeout=1, image="", replicas=1, environment="", resources="",
    )
    result = capacity_baseline.execute(args)
    assert result["requests"] == 3
