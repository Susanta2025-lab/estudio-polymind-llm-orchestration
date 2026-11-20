"""Independently signed, configuration-bound execution permissions.

No signing or credential acquisition. Trust/revocation files are independently
provisioned. Consumption uses the existing action authority, never a budget ledger.
"""
from dataclasses import asdict
import json
import os
from pathlib import Path
import time
from typing import Literal
from uuid import UUID

import jwt
from pydantic import Field, model_validator
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from config.runtime_secrets import private_file
from documents.jobs.models import canonical, fingerprint
from documents.models import FrozenModel
from security.models import SecurityError


class ApprovalTrust(FrozenModel):
    # Same trust document as the retained Foundry launcher; no historical digest change.
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


def read_record(path, limit=65536):
    path = private_file(path)
    if path.stat().st_size > limit:
        raise SecurityError()
    return path.read_text()


class ExecutionPermissions:
    def __init__(self, root, trust_path, actions, authority, binding, *, purpose='live', clock=time.time, ledger=None):
        if purpose not in {'live', 'test'}:
            raise SecurityError()
        self.root, self.trust_path = Path(root), Path(trust_path)
        self.actions, self.authority, self.binding = actions, authority, binding
        self.purpose, self.clock, self.ledger = purpose, clock, ledger

    def check(self, principal, permission_id, scope, resource):
        try:
            permission_id = str(UUID(str(permission_id)))
            if self.purpose == 'live' and not os.statvfs(self.root).f_flag & os.ST_RDONLY:
                raise ValueError('Independent execution authority must be mounted read-only')
            self.authority.revalidate(self.authority.snapshot(principal))
            trust = ApprovalTrust.model_validate_json(read_record(self.trust_path, 16384))
            if (trust.purpose != self.purpose or principal.kind != 'user' or
                    (principal.issuer, principal.subject, principal.tenant_identity) !=
                    (trust.operator_issuer, trust.operator_subject, trust.operator_tenant)):
                raise ValueError()
            revoked = json.loads(read_record(self.root / 'revoked.json'))
            if not isinstance(revoked, list) or any(str(UUID(x)) != x for x in revoked) or permission_id in revoked:
                raise ValueError()
            raw = read_record(self.root / (permission_id + '.jwt'), 16384)
            if jwt.get_unverified_header(raw) != {'alg': 'RS256', 'typ': 'polymind-execution+jwt', 'kid': trust.key_id}:
                raise ValueError()
            claims = jwt.decode(raw, trust.public_key_pem, algorithms=['RS256'],
                issuer='polymind-independent-execution/1', audience='polymind-execution/1',
                options={'strict_aud': True, 'verify_exp': False, 'verify_nbf': False,
                         'verify_iat': False, 'require': ['iss','aud','jti','iat','nbf','exp','purpose','binding','scopes','resource','max_calls']})
            if (set(claims) != {'iss','aud','jti','iat','nbf','exp','purpose','binding','scopes','resource','max_calls'}
                    or claims['jti'] != permission_id or claims['purpose'] != self.purpose
                    or any(type(claims[k]) is not int for k in ('iat','nbf','exp','max_calls'))
                    or not claims['iat'] <= claims['nbf'] <= self.clock() < claims['exp']
                    or not 0 < claims['exp'] - claims['iat'] <= 86400 or not 1 <= claims['max_calls'] <= 32
                    or not isinstance(claims['scopes'], list) or scope not in claims['scopes']
                    or set(claims['scopes']) - {'chat', 'documents_synthesis', 'documents_question'}
                    or claims['resource'] != resource or claims['binding'] != fingerprint(self.binding())):
                raise ValueError()
            return claims
        except Exception:
            raise SecurityError() from None

    def remaining(self, claims):
        with self.actions.transaction() as db:
            used = db.execute('SELECT COUNT(*) FROM actions WHERE action=?',
                              ('execution/' + claims['jti'],)).fetchone()[0]
        return max(0, claims['max_calls'] - used)

    def claim(self, principal, permission_id, scope, resource, identity, *, minimum_seconds=0):
        claims = self.check(principal, permission_id, scope, resource)
        if min(claims['exp'], principal.expires) - self.clock() < minimum_seconds:
            raise SecurityError()
        if self.ledger is None:
            raise SecurityError('security_unavailable')
        with self.ledger.transaction() as db:
            if db.execute("SELECT 1 FROM reservations WHERE state NOT IN ('SETTLED','RELEASED')").fetchone():
                raise SecurityError('security_unavailable')
        if identity.scope != principal.scope.identity() or identity.attempt != 1:
            raise SecurityError()
        action, key = 'execution/' + claims['jti'], fingerprint({k:str(v) if isinstance(v, UUID) else v for k,v in asdict(identity).items()})
        with self.actions.transaction() as db:
            if (db.execute('SELECT 1 FROM actions WHERE action=? AND key=?', (action,key)).fetchone()
                    or db.execute('SELECT COUNT(*) FROM actions WHERE action=?', (action,)).fetchone()[0] >= claims['max_calls']):
                raise SecurityError()
            db.execute('INSERT INTO actions VALUES(?,?,?,?,?)',
                (principal.scope.identity(), action, key, claims['binding'], canonical({'consumed': True})))
        return claims



class DocumentsExecutionPermission:
    def __init__(self, permissions):
        self.permissions = permissions

    @staticmethod
    def resource(approval, source):
        from documents.pilot.models import ExecutionSessionApproval
        if type(approval) is not ExecutionSessionApproval or approval.zero_paid_execution is not False:
            raise SecurityError()
        return {'session': str(approval.session_id), 'source': fingerprint(source.model_dump(mode='json'))}

    def authorize(self, principal, approval, source, kind):
        return self.permissions.check(principal, approval.execution_permission, kind, self.resource(approval, source))

    def __call__(self, principal, approval, source, request):
        # The actual workload is checked by claim; request/role/capability and
        # financial bindings are also enforced by the retained PilotExecution.
        resource = self.resource(approval, source)
        for kind in ('documents_synthesis', 'documents_question'):
            try:
                return self.permissions.check(principal, approval.execution_permission, kind, resource)
            except SecurityError:
                pass
        raise SecurityError()

    def claim(self, principal, approval, source, request, identity, kind):
        if min(approval.expires_at.timestamp(), source.expires_at.timestamp()) - self.permissions.clock() < request.total_seconds:
            raise SecurityError()
        self.permissions.claim(principal, approval.execution_permission, 'documents_' + kind,
                               self.resource(approval, source), identity, minimum_seconds=request.total_seconds)
