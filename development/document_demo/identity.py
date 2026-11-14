"""Loopback-only test issuer. Ephemeral keys are runtime files, never fixtures in Git.

This deliberately authenticates one synthetic operator without credentials. It
must never be exposed publicly or confused with a real identity provider.
"""
import base64
import hashlib
import json
import secrets
import time
from pathlib import Path
from urllib.parse import urlencode

import jwt
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from security.identity import OIDCVerifier
from security.models import SecurityError


class FixtureOperatorVerifier(OIDCVerifier):
    """Additional strict user-token contract for this one synthetic issuer.

    Keep the established generic verifier and Entra profiles unchanged. The
    development operator contract rejects service/app identities and any extra
    role, even if another claim would grant a known operator permission.
    """
    def verify(self, access_token):
        principal = super().verify(access_token)
        try:
            header = jwt.get_unverified_header(access_token)  # already verified by the base
            claims = jwt.decode(access_token, self._key(header["kid"]), algorithms=["RS256"],
                                issuer=self.config.issuer, audience=self.config.audience)
            if claims.get("idtyp", "user") != "user" or claims.get("roles") != ["operator"]:
                raise ValueError()
            return principal
        except Exception:
            raise SecurityError("authentication_required") from None


def issuer_app(root, *, nonce_transform=lambda value: value):
    root = Path(root)
    cfg = json.loads((root / "identity.json").read_text())
    key = (root / "signing.pem").read_bytes()
    codes = {}
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    @app.get("/.well-known/openid-configuration")
    def metadata():
        issuer = cfg["issuer"]
        return dict(issuer=issuer, authorization_endpoint=issuer + "/authorize",
                    token_endpoint=issuer + "/token", jwks_uri=issuer + "/jwks",
                    response_types_supported=["code"], subject_types_supported=["public"],
                    id_token_signing_alg_values_supported=["RS256"],
                    token_endpoint_auth_methods_supported=["client_secret_basic"],
                    code_challenge_methods_supported=["S256"])

    @app.get("/jwks")
    def jwks():
        return {"keys": [cfg["jwk"]]}

    @app.get("/authorize")
    def authorize(request: Request):
        q = request.query_params
        if (q.get("client_id") != cfg["client_id"] or q.get("redirect_uri") != cfg["redirect_uri"]
                or q.get("response_type") != "code" or not q.get("state") or not q.get("nonce")
                or q.get("code_challenge_method") != "S256" or not q.get("code_challenge")
                or set(q.get("scope", "").split()) != {"openid", "documents"}):
            return JSONResponse({"error": "invalid_request"}, status_code=400)
        code = secrets.token_urlsafe(32)
        codes[code] = (dict(q), time.time() + 60)
        return RedirectResponse(cfg["redirect_uri"] + "?" + urlencode({"code": code, "state": q["state"]}), 302)

    @app.post("/token")
    async def token(request: Request):
        # No token, code, claim or key material is logged.
        expected = "Basic " + base64.b64encode((cfg["client_id"] + ":" + cfg["client_secret"]).encode()).decode()
        if not secrets.compare_digest(request.headers.get("authorization", ""), expected):
            return JSONResponse({"error": "invalid_client"}, status_code=401)
        form = await request.form()
        record = codes.pop(form.get("code"), None)
        verifier = form.get("code_verifier", "")
        challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
        if (not record or record[1] <= time.time() or form.get("grant_type") != "authorization_code"
                or form.get("redirect_uri") != cfg["redirect_uri"] or challenge != record[0]["code_challenge"]):
            return JSONResponse({"error": "invalid_grant"}, status_code=400)
        now = int(time.time())
        claims = dict(iss=cfg["issuer"], sub="operator", tid="synthetic", iat=now, nbf=now,
                      exp=now + 900)
        access = jwt.encode(dict(claims, aud="polymind-documents", token_use="access", roles=["operator"]),
                            key, algorithm="RS256", headers={"kid": "fixture"})
        identity = jwt.encode(dict(claims, aud=cfg["client_id"], nonce=nonce_transform(record[0]["nonce"])),
                              key, algorithm="RS256", headers={"kid": "fixture"})
        return JSONResponse(dict(access_token=access, id_token=identity, token_type="Bearer", expires_in=900),
                            headers={"Cache-Control": "no-store"})

    return app
