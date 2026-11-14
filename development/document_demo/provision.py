"""Explicit first-time test identity/TLS provisioning outside the source tree."""
import ipaddress
import json
import os
import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID


def provision(root, *, ui_port=9443, identity_port=9444):
    root = Path(root).resolve()
    root.mkdir(mode=0o700, parents=True, exist_ok=False)
    signing = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    tls = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    for name, key in (("signing.pem", signing), ("tls.key", tls)):
        (root / name).write_bytes(key.private_bytes(serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
        os.chmod(root / name, 0o600)
    now = datetime.now(timezone.utc)
    subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "PolyMind loopback fixture")])
    cert = (x509.CertificateBuilder().subject_name(subject).issuer_name(subject).public_key(tls.public_key())
            .serial_number(x509.random_serial_number()).not_valid_before(now - timedelta(minutes=1))
            .not_valid_after(now + timedelta(days=2))
            .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
            .add_extension(x509.SubjectAlternativeName([x509.DNSName("localhost"),
                x509.IPAddress(ipaddress.ip_address("127.0.0.1"))]), critical=False).sign(tls, hashes.SHA256()))
    (root / "tls.crt").write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    jwk = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(signing.public_key()))
    jwk.update(kid="fixture", alg="RS256", use="sig")
    cfg = dict(issuer=f"https://localhost:{identity_port}", client_id="fixture-ui",
               client_secret=secrets.token_urlsafe(32), redirect_uri=f"https://localhost:{ui_port}/oauth2callback", jwk=jwk)
    (root / "identity.json").write_text(json.dumps(cfg))
    os.chmod(root / "identity.json", 0o600)
    streamlit = root / ".streamlit"
    streamlit.mkdir(mode=0o700)
    # Native auth token exposure is explicitly limited to the API access token.
    (streamlit / "secrets.toml").write_text(
        '[auth]\nredirect_uri = ' + json.dumps(cfg["redirect_uri"]) + '\ncookie_secret = '
        + json.dumps(secrets.token_urlsafe(48)) + '\nexpose_tokens = ["access"]\n'
        + 'client_id = "fixture-ui"\nclient_secret = ' + json.dumps(cfg["client_secret"])
        + '\nserver_metadata_url = ' + json.dumps(cfg["issuer"] + '/.well-known/openid-configuration')
        + '\n[auth.client_kwargs]\nscope = "openid documents"\n')
    os.chmod(streamlit / "secrets.toml", 0o600)
    return root
