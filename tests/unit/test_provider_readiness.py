import pytest
import requests

from llm.inference import ModelRole, ReadinessStatus
from llm.ollama_client import OllamaClient
from llm.openai_compatible import OpenAICompatibleProvider


class Response:
    def __init__(self, payload=None, status=None):
        self.payload = payload
        self.status = status
        self.closed = False

    def raise_for_status(self):
        if self.status:
            error = requests.HTTPError("private upstream body")
            error.response = type("ErrorResponse", (), {"status_code": self.status})()
            raise error

    def json(self):
        if isinstance(self.payload, Exception):
            raise self.payload
        return self.payload

    def close(self):
        self.closed = True


class HTTP:
    def __init__(self, outcomes):
        self.outcomes = iter(outcomes)
        self.calls = []

    def get(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        outcome = next(self.outcomes)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def make(kind, outcomes, retries=0, backoff=0):
    models = {role.value: f"served-{role.value}" for role in ModelRole}
    http = HTTP(outcomes)
    kwargs = dict(model_map=models, http_client=http, readiness_retries=retries,
                  readiness_backoff=backoff)
    if kind == "openai_compatible":
        provider = OpenAICompatibleProvider(base_url="http://inference/v1", **kwargs)
    else:
        provider = OllamaClient(url="http://ollama:11434/api/chat", **kwargs)
    return provider, http


def payload(kind, names):
    key = "data" if kind == "openai_compatible" else "models"
    name_key = "id" if kind == "openai_compatible" else "name"
    return {key: [{name_key: name} for name in names]}


@pytest.mark.parametrize("kind", ["ollama", "openai_compatible"])
def test_readiness_contract_ready_and_uses_lightweight_discovery(kind):
    names = [f"served-{role.value}" for role in ModelRole]
    response = Response(payload(kind, names))
    provider, http = make(kind, [response])
    result = provider.check_readiness()
    assert result.ready is True
    assert result.status is ReadinessStatus.READY
    assert response.closed is True
    assert http.calls[0][0][0].endswith("/api/tags" if kind == "ollama" else "/models")


@pytest.mark.parametrize(("outcome", "status"), [
    (requests.ConnectionError("private"), ReadinessStatus.UNREACHABLE),
    (requests.Timeout("private"), ReadinessStatus.TIMEOUT),
    (Response(status=401), ReadinessStatus.AUTHENTICATION_FAILURE),
    (Response(status=403), ReadinessStatus.AUTHENTICATION_FAILURE),
    (Response(status=429), ReadinessStatus.OVERLOADED),
    (Response(status=500), ReadinessStatus.UPSTREAM_FAILURE),
    (Response(status=502), ReadinessStatus.OVERLOADED),
    (Response(status=503), ReadinessStatus.OVERLOADED),
    (Response(status=504), ReadinessStatus.TIMEOUT),
])
def test_openai_readiness_classifies_operational_failures(outcome, status):
    provider, _ = make("openai_compatible", [outcome])
    assert provider.check_readiness().status is status


@pytest.mark.parametrize("kind", ["ollama", "openai_compatible"])
def test_readiness_reports_missing_model_and_malformed_protocol(kind):
    missing, _ = make(kind, [Response(payload(kind, ["served-general"]))])
    malformed, _ = make(kind, [Response({"wrong": []})])
    assert missing.check_readiness().status is ReadinessStatus.MODEL_UNAVAILABLE
    assert malformed.check_readiness().status is ReadinessStatus.PROTOCOL_FAILURE


def test_readiness_retries_transient_failure_then_succeeds(monkeypatch):
    sleeps = []
    names = [f"served-{role.value}" for role in ModelRole]
    provider, http = make("openai_compatible", [requests.ConnectionError("private"),
                           Response(payload("openai_compatible", names))], retries=1, backoff=0.2)
    monkeypatch.setattr("llm.openai_compatible.time.sleep", sleeps.append)
    assert provider.check_readiness().ready
    assert len(http.calls) == 2
    assert sleeps == [0.2]


def test_readiness_retry_limit_and_non_retryable_error(monkeypatch):
    monkeypatch.setattr("llm.openai_compatible.time.sleep", lambda _: None)
    retrying, retry_http = make("openai_compatible", [Response(status=503), Response(status=503)], retries=1)
    auth, auth_http = make("openai_compatible", [Response(status=401)], retries=3)
    assert retrying.check_readiness().status is ReadinessStatus.OVERLOADED
    assert len(retry_http.calls) == 2
    assert auth.check_readiness().status is ReadinessStatus.AUTHENTICATION_FAILURE
    assert len(auth_http.calls) == 1
