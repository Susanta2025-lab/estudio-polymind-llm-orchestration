"""Offline verification of separately signed L1 operator approvals; never signs.

Trust is provisioned independently of launch configuration and approval input.
Replay protection is single-host durable consumption, not hostile-host protection.
"""
from hashlib import sha256
import json
import os
from pathlib import Path
import stat
import time
from typing import Literal
from uuid import UUID

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import jwt
from pydantic import Field, model_validator

from documents.models import FrozenModel
from security.models import SecurityError


class ApprovalTrust(FrozenModel):
    version: Literal['polymind-approval-trust/1']
    purpose: Literal['live', 'test']
    key_id: str = Field(pattern=r'^[A-Za-z0-9_-]{1,128}$')
    public_key_pem: str = Field(min_length=1, max_length=8192)
    operator_issuer: str = Field(min_length=1, max_length=2048)
    operator_subject: str = Field(min_length=1, max_length=2048)
    operator_tenant: str = Field(min_length=1, max_length=2048)
    replay_directory: Path

    @model_validator(mode='after')
    def public_key(self):
        key = serialization.load_pem_public_key(self.public_key_pem.encode())
        if not isinstance(key, rsa.RSAPublicKey) or not 2048 <= key.key_size <= 8192:
            raise ValueError('Approval requires an RSA public key of 2048–8192 bits')
        return self


def private_path(path, *, directory=False, exists=True):
    path = Path(path)
    repository = Path(__file__).resolve().parents[2]
    if (not path.is_absolute() or '..' in path.parts or path.resolve().is_relative_to(repository)
            or any(p.is_symlink() for p in (path, *path.parents))):
        raise ValueError('Private outside-repository path required')
    if exists:
        info = path.stat()
        if (info.st_uid != os.geteuid() or info.st_mode & 0o077
                or (not stat.S_ISDIR(info.st_mode) if directory else
                    not stat.S_ISREG(info.st_mode) or info.st_nlink != 1)):
            raise ValueError('Private operator-owned artifact required')
    return path


def read_private(path, limit):
    path = private_path(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
                or info.st_uid != os.geteuid() or info.st_mode & 0o077):
            raise SecurityError()
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise SecurityError()
    return raw


def load_trust(path):
    trust = ApprovalTrust.model_validate_json(read_private(path, 16384))
    private_path(trust.replay_directory, directory=True)
    if trust.purpose != 'live':
        raise SecurityError()
    return trust


def bindings(config, principal, digest):
    """Unsigned review material only. A trusted operator must independently review it."""
    contract = config.contract.model_dump(mode='json')
    value = {
        'configuration_sha256': digest,
        'operator': {'issuer': principal.issuer, 'subject': principal.subject,
                     'tenant': principal.tenant_identity, 'owner_scope': principal.scope.identity()},
        'foundry': {**{name: getattr(config, name) for name in
                      ('resource', 'deployment', 'endpoint', 'model', 'model_version', 'sku')},
                   'region': contract['region']},
        'budget': {name: contract[name] for name in ('currency', 'maximum', 'fixed_cost', 'extra_cost')},
        'limits': {name: contract[name] for name in ('attempts', 'input_tokens', 'output_tokens',
                  'total_input', 'total_output', 'rpm', 'tpm', 'context')},
        'expires': config.approval_expires,
    }
    if getattr(config, 'executor', None) is not None:
        value['execution'] = {'executor': config.executor,
                              'sha256': config.executor_sha256,
                              'generation_sha256': config.generation_contract_sha256,
                              'schema_sha256': config.provider_schema_sha256}
    return value


def verify_artifact(artifact, trust, config, principal, digest):
    try:
        if (type(artifact) is not str or not 1 <= len(artifact) <= 16384
                or not isinstance(trust, ApprovalTrust) or trust.purpose != 'live'
                or principal.kind != 'user'
                or trust.replay_directory.resolve().is_relative_to(config.audit_directory.resolve())
                or (principal.issuer, principal.subject, principal.tenant_identity) !=
                   (trust.operator_issuer, trust.operator_subject, trust.operator_tenant)):
            raise ValueError()
        header = jwt.get_unverified_header(artifact)
        if header != {'alg': 'RS256', 'typ': 'polymind-approval+jwt', 'kid': trust.key_id}:
            raise ValueError()
        claims = jwt.decode(artifact, trust.public_key_pem, algorithms=['RS256'],
            issuer='polymind-operator-approval/1',
            audience=('polymind-single-analysis-live' if getattr(config, 'executor', None)
                      == 'polymind-single-analysis/1' else 'polymind-l1-live'),
            options={'strict_aud': True, 'require': ['iss', 'aud', 'jti', 'iat', 'nbf', 'exp', 'purpose', 'binding']})
        if (set(claims) != {'iss', 'aud', 'jti', 'iat', 'nbf', 'exp', 'purpose', 'binding'}
                or claims['purpose'] != 'live' or str(UUID(claims['jti'])) != claims['jti']
                or any(type(claims[name]) is not int for name in ('iat', 'nbf', 'exp'))
                or not claims['iat'] <= claims['nbf'] < claims['exp']
                or claims['exp'] - claims['iat'] > 86400
                or claims['exp'] != config.approval_expires
                or min(claims['exp'], principal.expires, config.credential_valid_until) <= time.time() + 60
                or json.dumps(claims['binding'], sort_keys=True, separators=(',', ':')) !=
                   json.dumps(bindings(config, principal, digest), sort_keys=True, separators=(',', ':'))):
            raise ValueError()
        return claims
    except Exception:
        raise SecurityError('access_denied') from None


def fsync_directory(directory):
    fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def consume(approval, trust, artifact):
    """Exclusive creation survives restart and signature/key changes for the same ID.

    No removal/rollback: a partial write or later launch failure consumes approval.
    """
    try:
        root = private_path(trust.replay_directory, directory=True)
        path = root / (approval['jti'] + '.consumed.json')
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, 'w') as stream:
            json.dump({'approval_id': approval['jti'], 'key_id': trust.key_id,
                       'artifact_sha256': sha256(artifact.encode()).hexdigest(),
                       'configuration_sha256': approval['binding']['configuration_sha256']}, stream)
            stream.flush()
            os.fsync(stream.fileno())
        fsync_directory(root)
    except Exception:
        raise SecurityError('access_denied') from None
