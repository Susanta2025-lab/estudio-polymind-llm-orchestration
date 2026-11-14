"""Issuer protocol negatives. Real browser callback proof is a separate runner."""
import base64
import hashlib
import json
from urllib.parse import parse_qs, urlsplit

import pytest
from fastapi.testclient import TestClient

from development.document_demo.identity import issuer_app
from development.document_demo.provision import provision


@pytest.fixture
def issuer(tmp_path):
    root = provision(tmp_path / "identity")
    cfg = json.loads((root / "identity.json").read_text())
    return TestClient(issuer_app(root)), cfg


def authorization(cfg):
    verifier = "a" * 64
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    return dict(client_id=cfg["client_id"], redirect_uri=cfg["redirect_uri"], response_type="code",
                state="bound-state", nonce="bound-nonce", scope="openid documents",
                code_challenge_method="S256", code_challenge=challenge), verifier


@pytest.mark.parametrize("change", [{"redirect_uri": "https://foreign.invalid"}, {"client_id": "foreign"},
    {"response_type": "token"}, {"state": ""}, {"nonce": ""}, {"code_challenge_method": "plain"},
    {"scope": "openid"}])
def test_test_issuer_rejects_redirect_scope_and_protocol_changes(issuer, change):
    client, cfg = issuer
    params, _ = authorization(cfg)
    assert client.get("/authorize", params={**params, **change}, follow_redirects=False).status_code == 400


@pytest.mark.parametrize("fault", ["client", "verifier", "redirect", "code", "replay"])
def test_one_time_code_and_pkce_binding(issuer, fault):
    client, cfg = issuer
    params, verifier = authorization(cfg)
    response = client.get("/authorize", params=params, follow_redirects=False)
    code = parse_qs(urlsplit(response.headers["location"]).query)["code"][0]
    form = dict(code=code, grant_type="authorization_code", redirect_uri=cfg["redirect_uri"], code_verifier=verifier)
    auth = (cfg["client_id"], cfg["client_secret"])
    if fault == "replay":
        assert client.post("/token", data=form, auth=auth).status_code == 200
    elif fault == "client":
        auth = (cfg["client_id"], "invalid")
    elif fault == "verifier":
        form["code_verifier"] = "wrong"
    elif fault == "redirect":
        form["redirect_uri"] = "https://foreign.invalid"
    else:
        form["code"] = "forged"
    assert client.post("/token", data=form, auth=auth).status_code in {400, 401}
