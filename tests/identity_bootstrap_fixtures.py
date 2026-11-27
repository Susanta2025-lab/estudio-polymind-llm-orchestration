"""Synthetic bootstrap material only; no operational file discovery."""

import json
import os
import stat
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
import pytest
import toml
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

from deployment.phase19.identity_bootstrap import core, files


@pytest.fixture
def bootstrap_identity():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    jwk = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(key.public_key()))
    jwk.update(kid="bootstrap-synthetic", alg="RS256", use="sig")
    verifier = core.BootstrapVerifier(fetch=lambda: {"keys": [jwk]})

    def token(
        changes=None, *, signing_key=None, algorithm="RS256", kid="bootstrap-synthetic"
    ):
        now = int(time.time())
        claims = dict(
            iss=core.settings().issuer,
            tid=core.TENANT,
            aud=core.API_CLIENT,
            azp=core.BROWSER_CLIENT,
            sub="synthetic-api-subject",
            oid="unused-directory-object",
            ver="2.0",
            iat=now - 1,
            nbf=now - 1,
            exp=now + 3600,
            scp="access_as_user",
            roles=["PolyMind.L1Operator"],
        )
        claims.update(changes or {})
        return jwt.encode(
            {k: v for k, v in claims.items() if v is not None},
            signing_key or key,
            algorithm=algorithm,
            headers={"kid": kid},
        )

    return verifier, token


@pytest.fixture
def private_tree(tmp_path, monkeypatch):
    original = files.ancestor

    def synthetic_ancestor(info):
        # Tests alone permit the root-owned sticky /tmp ancestor. Operational
        # code has no exception for shared temporary storage.
        if (
            info.st_uid == 0
            and stat.S_IMODE(info.st_mode) == 0o1777
            and (info.st_dev, info.st_ino)
            == (Path("/tmp").stat().st_dev, Path("/tmp").stat().st_ino)
        ):
            return
        original(info)

    monkeypatch.setattr(files, "ancestor", synthetic_ancestor)
    tmp_path.chmod(0o700)
    evidence = tmp_path / "evidence"
    evidence.mkdir(mode=0o700)
    session = tmp_path / "session"
    session.mkdir(mode=0o700)
    (session / ".streamlit").mkdir(mode=0o700)
    auth = dict(
        redirect_uri=core.ORIGIN + "/oauth2callback",
        server_metadata_url=core.AUTHORITY + "/v2.0/.well-known/openid-configuration",
        client_id=core.BROWSER_CLIENT,
        client_secret="synthetic-client-secret-value",
        cookie_secret="synthetic-cookie-secret-" + "a" * 64,
        expose_tokens=["access"],
        client_kwargs={"scope": f"openid api://{core.API_CLIENT}/access_as_user"},
    )
    path = session / ".streamlit/secrets.toml"
    path.write_text(toml.dumps({"auth": auth}))
    path.chmod(0o600)
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "polymind.test")])
    now = datetime.now(timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=1))
        .not_valid_after(now + timedelta(minutes=30))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName("polymind.test")]), critical=False
        )
        .add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False
        )
        .sign(key, hashes.SHA256())
    )
    for name, data in [
        ("tls.crt", cert.public_bytes(serialization.Encoding.PEM)),
        (
            "tls.key",
            key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.PKCS8,
                serialization.NoEncryption(),
            ),
        ),
    ]:
        (session / name).write_bytes(data)
        (session / name).chmod(0o600)
    assert os.geteuid() == evidence.stat().st_uid
    return session, evidence, auth
