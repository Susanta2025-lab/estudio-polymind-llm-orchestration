"""Immutable server-issued identity; HTTP schemas never accept this type."""
from dataclasses import dataclass
from enum import Enum
import hashlib
import json
import time
from uuid import UUID

from documents.models import Scope, stable_id


class SecurityError(RuntimeError):
    def __init__(self, category='access_denied'):
        self.category = category if category in {
            'access_denied', 'authentication_required', 'security_unavailable',
            'security_configuration', 'unsupported_execution', 'mixed_owners',
        } else 'access_denied'
        super().__init__(self.category)


class Action(str, Enum):
    DOCUMENT_READ = 'DOCUMENT_READ'
    DOCUMENT_ANALYZE = 'DOCUMENT_ANALYZE'
    DOCUMENT_SHARE = 'DOCUMENT_SHARE'
    DOCUMENT_DELETE = 'DOCUMENT_DELETE'
    JOB_READ = 'JOB_READ'
    JOB_CANCEL = 'JOB_CANCEL'
    SESSION_READ = 'SESSION_READ'
    SESSION_WRITE = 'SESSION_WRITE'
    PUBLICATION_MANAGE = 'PUBLICATION_MANAGE'
    USAGE_READ = 'USAGE_READ'
    TENANT_ADMIN = 'TENANT_ADMIN'


_VERIFIED = object()


@dataclass(frozen=True, init=False)
class Principal:
    issuer: str
    subject: str
    tenant_identity: str
    scope: Scope
    permissions: frozenset[Action]
    kind: str
    expires: int

    def __init__(self, issuer, subject, tenant_identity, permissions, kind, expires, *, _seal=None):
        if _seal is not _VERIFIED:
            raise SecurityError('authentication_required')
        if (any(type(s) is not str or not s or len(s) > 2048 for s in (issuer, subject, tenant_identity))
                or kind not in {'user', 'service'} or type(expires) is not int or expires <= time.time()
                or not isinstance(permissions, frozenset) or any(type(a) is not Action for a in permissions)):
            raise SecurityError('authentication_required')
        tenant = stable_id('polymind-identity/1/tenant', issuer, tenant_identity)
        owner = stable_id('polymind-identity/1/owner', issuer, tenant_identity, subject)
        for k, v in dict(issuer=issuer, subject=subject, tenant_identity=tenant_identity,
                         scope=Scope(tenant=tenant, owner=owner), permissions=permissions,
                         kind=kind, expires=expires).items():
            object.__setattr__(self, k, v)


def _verified_principal(issuer, subject, tenant, permissions=frozenset(), kind='user', expires=None):
    """Verifier/test-fixture boundary only; never consume an HTTP principal payload."""
    return Principal(issuer, subject, tenant, permissions, kind, expires, _seal=_VERIFIED)


def session_key(principal, session_id):
    if type(principal) is not Principal or type(session_id) is not str or not 1 <= len(session_id) <= 256:
        raise SecurityError()
    payload = json.dumps(['polymind-session/1', str(principal.scope.tenant),
                          str(principal.scope.owner), session_id], separators=(',', ':'), ensure_ascii=True)
    return 's1-' + hashlib.sha256(payload.encode()).hexdigest()


@dataclass(frozen=True)
class AuthorizationSnapshot:
    principal: Principal
    principal_epoch: int
    documents: tuple[tuple[UUID, Scope, int], ...]
    action: Action = Action.DOCUMENT_ANALYZE
    policy_version: str = 'authorization/1'
