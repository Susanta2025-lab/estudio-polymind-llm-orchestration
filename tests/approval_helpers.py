"""Ephemeral approval signing for offline tests only; never imported by launcher."""
import time
from uuid import uuid4

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import jwt
import pytest

from tests.performance.foundry_approval import ApprovalTrust, bindings


@pytest.fixture
def approval_signer(tmp_path):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public = key.public_key().public_bytes(serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo).decode()
    replay = tmp_path / 'approval-consumption'
    replay.mkdir(mode=0o700)

    def issue(config, principal, *, changes=None, headers=None, trust_changes=None, signing_key=None, algorithm='RS256'):
        from tests.performance.foundry_l1 import configuration_digest
        trust = ApprovalTrust(version='polymind-approval-trust/1', purpose='live', key_id='ephemeral-offline-key',
            public_key_pem=public, operator_issuer=principal.issuer, operator_subject=principal.subject,
            operator_tenant=principal.tenant_identity, replay_directory=replay)
        if trust_changes:
            trust = ApprovalTrust.model_validate({**trust.model_dump(), **trust_changes})
        claims = {'iss':'polymind-operator-approval/1', 'aud':'polymind-l1-live',
                  'jti':str(uuid4()), 'iat':int(time.time())-1, 'nbf':int(time.time())-1,
                  'exp':config.approval_expires, 'purpose':'live',
                  'binding':bindings(config, principal, configuration_digest(config))}
        claims.update(changes or {})
        claims = {k:v for k,v in claims.items() if v is not None}
        encoded = jwt.encode(claims, signing_key or key, algorithm=algorithm,
            headers=headers or {'kid':trust.key_id, 'typ':'polymind-approval+jwt'})
        return encoded, trust
    return issue
