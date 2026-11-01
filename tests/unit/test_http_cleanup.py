"""Real requests cleanup boundaries with synthetic streams and no network."""

import json
from dataclasses import asdict, replace
from io import BytesIO
from unittest.mock import Mock

import pytest
import requests
from urllib3.exceptions import ReadTimeoutError

from documents.digestion.managed import classify_managed
from llm.bounded_http import request_json
from llm.inference import (
    InferenceAuthenticationError,
    InferenceConfigurationError,
    InferenceConnectionError,
    InferenceOutputLimitError,
    InferenceRateLimitError,
    InferenceResponseError,
    InferenceTimeoutError,
    InferenceUsage,
    OutputLimitDiagnostics,
)
from llm.openai_compatible import OpenAICompatibleProvider
from tests.unit.test_structured_provider import HTTP, payload, request

SECRET = "SYNTHETIC_PRIVATE_CLEANUP_DETAIL"
LIMIT = 26192


class Raw(BytesIO):
    def __init__(self, body, *, cleanup_error=None, read_error=None):
        super().__init__(body)
        self.cleanup_error = cleanup_error
        self.read_error = read_error
        self.closes = 0
        self.releases = 0

    def read(self, size=-1):
        if self.read_error is not None:
            raise self.read_error
        return super().read(size)

    def close(self):
        self.closes += 1
        super().close()
        if self.cleanup_error is not None:
            raise self.cleanup_error

    def release_conn(self):
        self.releases += 1
        if self.cleanup_error is not None:
            raise self.cleanup_error


def real_response(body=b"{}", *, status=200, cleanup_error=None, read_error=None):
    response = requests.Response()
    response.status_code = status
    response.headers["Retry-After"] = "17"
    response.raw = Raw(body, cleanup_error=cleanup_error, read_error=read_error)
    return response


def bounded(http):
    return request_json(
        http,
        "https://offline.invalid/v1",
        headers={},
        payload={},
        timeout=(1, 1),
        total_seconds=10,
        max_bytes=LIMIT,
    )


def provider(http=None):
    kwargs = {} if http is None else {"http_client": http}
    return OpenAICompatibleProvider(
        base_url="https://offline.invalid/v1",
        model_map={"summarization": "served-alias"},
        **kwargs,
    )


CASES = [
    (
        "redirect",
        InferenceConfigurationError,
        "configuration_failure",
        "inference_configuration",
    ),
    ("oversize", InferenceOutputLimitError, "output_limit", "inference_output_limit"),
    ("timeout", InferenceTimeoutError, "timeout", "inference_timeout"),
    ("wrapped_timeout", InferenceTimeoutError, "timeout", "inference_timeout"),
    (
        "malformed",
        InferenceResponseError,
        "protocol_failure",
        "inference_invalid_response",
    ),
    (
        "duplicate",
        InferenceResponseError,
        "protocol_failure",
        "inference_invalid_response",
    ),
    (
        "unicode",
        InferenceResponseError,
        "protocol_failure",
        "inference_invalid_response",
    ),
    (
        "rejection",
        InferenceConfigurationError,
        "configuration_failure",
        "inference_configuration",
    ),
    (
        "authentication",
        InferenceAuthenticationError,
        "authentication_failure",
        "inference_authentication",
    ),
    ("overloaded", InferenceRateLimitError, "overloaded", "inference_rate_limited"),
    ("gateway_timeout", InferenceTimeoutError, "timeout", "inference_timeout"),
]


def scenario(case, cleanup_error=None):
    body = {
        "oversize": b"x" * (LIMIT + 1),
        "malformed": b"{",
        "duplicate": b'{"x":1,"x":2}',
        "unicode": b"\xff",
        "rejection": json.dumps(
            {
                "error": {
                    "code": "invalid_json_schema",
                    "param": "response_format",
                    "message": SECRET,
                }
            }
        ).encode(),
    }.get(case, b"{}")
    read_error = None
    if case == "timeout":
        read_error = requests.Timeout(SECRET)
    elif case == "wrapped_timeout":
        read_error = requests.ConnectionError(ReadTimeoutError(None, None, SECRET))
    return real_response(
        body,
        status={
            "redirect": 302,
            "rejection": 400,
            "authentication": 401,
            "overloaded": 429,
            "gateway_timeout": 504,
        }.get(case, 200),
        cleanup_error=cleanup_error,
        read_error=read_error,
    )


@pytest.mark.parametrize("failing_cleanup", [False, True])
@pytest.mark.parametrize("case,expected,category,public", CASES)
def test_response_primary_precedence(case, expected, category, public, failing_cleanup):
    response = scenario(case, OSError(SECRET) if failing_cleanup else None)
    http = HTTP(response)
    with pytest.raises(expected) as caught:
        bounded(http)
    error = caught.value
    assert type(error) is expected
    assert error.category == category
    assert classify_managed(error).category == public
    assert SECRET not in str(error)
    assert len(http.calls) == 1
    assert response.raw.closes + response.raw.releases >= 1
    if case == "oversize":
        assert asdict(error.diagnostics) == asdict(OutputLimitDiagnostics())
    elif case == "rejection":
        assert error.rejection_diagnostics == {
            "http_status": 400,
            "reason": "strict_schema_rejected",
        }
    elif case == "overloaded":
        assert error.retry_after == 17
    sent = http.calls[0][1]
    assert sent["stream"] is True and sent["allow_redirects"] is False
    assert sent["timeout"] == (1, 1)


@pytest.mark.parametrize(
    "cleanup_type", [None, OSError, requests.ConnectionError, requests.Timeout]
)
def test_success_and_cleanup_only_failure(cleanup_type):
    response = real_response(
        b'{"value":1}', cleanup_error=cleanup_type(SECRET) if cleanup_type else None
    )
    http = HTTP(response)
    if cleanup_type is None:
        assert bounded(http) == {"value": 1}
    else:
        with pytest.raises(InferenceConnectionError) as caught:
            bounded(http)
        assert type(caught.value) is InferenceConnectionError
        assert caught.value.category == "provider_unreachable"
        assert classify_managed(caught.value).category == "inference_unavailable"
        assert str(caught.value) == "Inference provider cleanup failed."
        assert caught.value.__suppress_context__ and caught.value.__cause__ is None
        assert getattr(caught.value, "usage", None) is None
    assert len(http.calls) == 1
    # requests skips raw.close after complete iteration, but invokes release_conn.
    assert response.raw.closes == 0 and response.raw.releases == 1


@pytest.mark.parametrize(
    "failure,expected",
    [
        (requests.Timeout, InferenceTimeoutError),
        (requests.ConnectionError, InferenceConnectionError),
    ],
)
def test_post_failure_without_response(failure, expected):
    http = HTTP(error=failure(SECRET))
    with pytest.raises(expected) as caught:
        bounded(http)
    assert type(caught.value) is expected and SECRET not in str(caught.value)
    assert len(http.calls) == 1


@pytest.mark.parametrize(
    "primary",
    [
        InferenceOutputLimitError(),
        AssertionError("programming defect"),
        KeyboardInterrupt(),
    ],
)
def test_active_error_identity_preserved(primary):
    primary.usage = InferenceUsage(21, 7, 28)
    response = real_response(read_error=primary, cleanup_error=OSError(SECRET))
    with pytest.raises(type(primary)) as caught:
        bounded(HTTP(response))
    assert caught.value is primary
    assert primary.usage == InferenceUsage(21, 7, 28)
    assert primary.__context__ is None


@pytest.mark.parametrize(
    "cleanup_type", [AssertionError, RuntimeError, KeyboardInterrupt, SystemExit]
)
def test_unexpected_cleanup_defects_and_control_flow_propagate(cleanup_type):
    cleanup = cleanup_type(SECRET)
    with pytest.raises(cleanup_type) as caught:
        bounded(HTTP(real_response(cleanup_error=cleanup)))
    assert caught.value is cleanup


class Session(requests.Session):
    def __init__(self, response, *, cleanup_error=None):
        super().__init__()
        self.post = Mock(return_value=response)
        self.cleanup_error = cleanup_error
        self.closes = 0

    def close(self):
        self.closes += 1
        super().close()
        if self.cleanup_error is not None:
            raise self.cleanup_error


@pytest.mark.parametrize("provider_failure", [False, True])
@pytest.mark.parametrize("cleanup_failure", [False, True])
def test_owned_session_precedence(monkeypatch, provider_failure, cleanup_failure):
    value = payload()
    if provider_failure:
        value["choices"][0]["finish_reason"] = "length"
    session = Session(
        real_response(json.dumps(value).encode()),
        cleanup_error=OSError(SECRET) if cleanup_failure else None,
    )
    monkeypatch.setattr(requests, "Session", lambda: session)
    adapter = provider()
    primary = None
    result = None

    def execute_and_close():
        nonlocal primary, result
        try:
            try:
                result = adapter.execute(request())
            except InferenceOutputLimitError as exc:
                primary = exc
                raise
        finally:
            adapter.close()

    if provider_failure:
        with pytest.raises(InferenceOutputLimitError) as caught:
            execute_and_close()
        assert caught.value is primary and primary.category == "output_limit"
        assert classify_managed(primary).category == "inference_output_limit"
        assert primary.usage == InferenceUsage(21, 7, 28)
        assert primary.provider_metadata.completion_tokens == 7
        assert primary.diagnostics.failure_cause == "provider_completion_truncated"
    elif cleanup_failure:
        with pytest.raises(InferenceConnectionError) as caught:
            execute_and_close()
        assert type(caught.value) is InferenceConnectionError
        assert str(caught.value) == "Inference provider cleanup failed."
        assert caught.value.__suppress_context__
        assert result.usage == InferenceUsage(21, 7, 28)
    else:
        execute_and_close()
        assert result.text == '{"value":1}'
    assert session.closes == 1 and session.post.call_count == 1


@pytest.mark.parametrize("status", [200, 302])
def test_external_session_is_not_closed(status):
    session = Session(
        real_response(json.dumps(payload()).encode(), status=status),
        cleanup_error=OSError(SECRET),
    )
    adapter = provider(session)
    try:
        if status == 302:
            with pytest.raises(InferenceConfigurationError):
                adapter.execute(request())
        else:
            assert adapter.execute(request()).usage == InferenceUsage(21, 7, 28)
    finally:
        adapter.close()
    assert session.closes == 0 and session.post.call_count == 1


@pytest.mark.parametrize("case,expected,category,public", CASES[:6])
def test_adapter_retains_transport_error(case, expected, category, public):
    response = scenario(case, OSError(SECRET))
    http = HTTP(response)
    adapter = provider(http)
    with pytest.raises(expected) as caught:
        adapter.execute(replace(request(), max_response_envelope_bytes=LIMIT))
    assert type(caught.value) is expected
    assert caught.value.category == category
    assert classify_managed(caught.value).category == public
    assert getattr(caught.value, "usage", None) is None
    metadata = caught.value.provider_metadata.evidence()
    assert metadata["prompt_tokens"] is None and metadata["completion_tokens"] is None
    assert SECRET not in json.dumps(metadata)
    assert len(http.calls) == 1


def test_success_cleanup_failure_is_not_hidden_by_callers_handled_exception():
    try:
        raise ValueError("already handled")
    except ValueError:
        with pytest.raises(InferenceConnectionError) as caught:
            bounded(HTTP(real_response(cleanup_error=OSError(SECRET))))
    assert type(caught.value) is InferenceConnectionError
    assert str(caught.value) == "Inference provider cleanup failed."


def test_deadline_after_response_acquisition_survives_cleanup(monkeypatch):
    import llm.bounded_http as transport

    clock = iter((0, 11))
    monkeypatch.setattr(transport.time, "monotonic", lambda: next(clock))
    http = HTTP(real_response(cleanup_error=OSError(SECRET)))
    with pytest.raises(InferenceTimeoutError) as caught:
        bounded(http)
    assert type(caught.value) is InferenceTimeoutError
    assert caught.value.category == "timeout"
    assert classify_managed(caught.value).category == "inference_timeout"
    assert len(http.calls) == 1


def test_exact_envelope_ceiling_still_succeeds():
    response = real_response(b"{}" + b" " * (LIMIT - 2))
    assert bounded(HTTP(response)) == {}
    assert response.raw.tell() == LIMIT


@pytest.mark.parametrize("cleanup_type", [OSError, requests.RequestException])
def test_owned_session_timeout_preserves_exact_primary(monkeypatch, cleanup_type):
    session = Session(scenario("timeout"), cleanup_error=cleanup_type(SECRET))
    monkeypatch.setattr(requests, "Session", lambda: session)
    adapter = provider()
    original = None
    with pytest.raises(InferenceTimeoutError) as caught:
        try:
            try:
                adapter.execute(request())
            except InferenceTimeoutError as exc:
                original = exc
                raise
        finally:
            adapter.close()
    assert caught.value is original and original.category == "timeout"
    assert classify_managed(original).category == "inference_timeout"
    assert original.provider_metadata.prompt_tokens is None
    assert session.closes == session.post.call_count == 1


@pytest.mark.parametrize(
    "cleanup_type",
    [requests.RequestException, AssertionError, KeyboardInterrupt, SystemExit],
)
def test_owned_session_cleanup_only_exception_policy(monkeypatch, cleanup_type):
    session = Session(None, cleanup_error=cleanup_type(SECRET))
    monkeypatch.setattr(requests, "Session", lambda: session)
    adapter = provider()
    expected = (
        InferenceConnectionError
        if cleanup_type is requests.RequestException
        else cleanup_type
    )
    with pytest.raises(expected) as caught:
        adapter.close()
    assert type(caught.value) is expected
    if expected is InferenceConnectionError:
        assert str(caught.value) == "Inference provider cleanup failed."
    assert session.closes == 1 and session.post.call_count == 0
