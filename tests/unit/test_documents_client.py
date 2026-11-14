"""Protected client confidentiality, lifecycle and strict operator schemas."""
import pytest

from api.operator import CloseSession, CreateSession, PublishSession, Question
from config.settings import Settings
from pydantic import ValidationError
from ui.documents_client import DocumentClientError, DocumentsClient


@pytest.mark.parametrize("status", [200, 201, 202, 401, 403, 409, 413, 422, 429, 500, 503])
def test_document_client_closes_and_sanitizes(status):
    calls, closed = [], []
    class Response:
        status_code = status
        def json(self):
            return {"accepted": True}
        def close(self):
            closed.append(True)
    def request(*args, **kwargs):
        calls.append((args, kwargs))
        return Response()
    client = DocumentsClient("http://private-api", "secret-test-token", request=request)
    if status in {200, 201, 202}:
        assert client.call("GET", "/context") == {"accepted": True}
    else:
        with pytest.raises(DocumentClientError) as error:
            client.call("GET", "/context")
        assert "secret" not in str(error.value)
    assert closed == [True]
    assert calls[0][1]["headers"] == {"Authorization": "Bearer secret-test-token"}
    assert calls[0][1]["timeout"] == (3, 65) and calls[0][1]["allow_redirects"] is False


@pytest.mark.parametrize("model,body", [
    (CreateSession, {"source_approval_id": "../x", "request_key": "valid-request-0001", "owner": "injected"}),
    (Question, {"query": "x" * 4097, "request_key": "valid-request-0001"}),
    (CloseSession, {"withdrawal": "true"}),
    (PublishSession, {"expected_job_id": "a" * 36}),
])
def test_strict_operator_requests(model, body):
    with pytest.raises(ValidationError):
        model.model_validate(body)


def test_fixture_profile_rejected_in_production():
    with pytest.raises(ValidationError, match="Fixture document profile"):
        Settings(_env_file=None, DOCUMENTS_PROFILE="synthetic", DEPLOYMENT_ENV="production")


def test_backup_cannot_recurse_into_its_runtime(tmp_path, monkeypatch):
    from development.document_demo.__main__ import main
    monkeypatch.setattr("sys.argv", ["document_demo", "backup", str(tmp_path),
                                    "--destination", str(tmp_path / "recursive-copy")])
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 2
    assert not (tmp_path / "recursive-copy").exists()
