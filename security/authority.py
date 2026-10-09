"""Durable ownership/grants/epochs and bounded content-free audit events."""
from contextlib import contextmanager
import json
from functools import wraps
import time
from uuid import UUID, uuid4

from documents.models import Scope
from security.database import Database
from security.models import Action, AuthorizationSnapshot, Principal, SecurityError


SCHEMA = (
    'CREATE TABLE principals (owner TEXT PRIMARY KEY, tenant TEXT NOT NULL, identity TEXT NOT NULL, permissions TEXT NOT NULL, kind TEXT NOT NULL, epoch INTEGER NOT NULL, disabled INTEGER NOT NULL)',
    'CREATE TABLE documents (document TEXT PRIMARY KEY, tenant TEXT NOT NULL, owner TEXT NOT NULL REFERENCES principals(owner), epoch INTEGER NOT NULL, state TEXT NOT NULL)',
    'CREATE TABLE grants (grant_id TEXT PRIMARY KEY, document TEXT NOT NULL REFERENCES documents(document), grantee TEXT NOT NULL REFERENCES principals(owner), created REAL NOT NULL, revoked REAL, UNIQUE(document,grantee))',
    'CREATE TABLE audit (event_id TEXT PRIMARY KEY, at REAL NOT NULL, principal TEXT, tenant TEXT, action TEXT NOT NULL, resource TEXT, outcome TEXT NOT NULL, policy TEXT NOT NULL)',
    'CREATE TABLE purge (document TEXT PRIMARY KEY REFERENCES documents(document), inventory TEXT NOT NULL, state TEXT NOT NULL, reason TEXT NOT NULL)',
)


def audited_mutation(action):
    def decorate(method):
        @wraps(method)
        def run(self, principal, resource, *args, **kwargs):
            try:
                return method(self,principal,resource,*args,**kwargs)
            except SecurityError:
                with self.transaction() as db:
                    self._audit(db,principal if type(principal) is Principal else None,action,
                                resource if type(resource) is UUID else None,'denied')
                raise
        return run
    return decorate


class SecurityAuthority(Database):
    def __init__(self, path, *, audit_limit=100000, clock=time.time):
        if type(audit_limit) is not int or not 1 <= audit_limit <= 10000000:
            raise SecurityError('security_configuration')
        self.audit_limit, self.clock = audit_limit, clock
        super().__init__(path, SCHEMA)

    def ready(self):
        if not super().ready():
            return False
        try:
            with self.transaction() as db:
                return db.execute('SELECT COUNT(*) FROM audit').fetchone()[0] < self.audit_limit
        except SecurityError:
            return False

    def _audit(self, db, principal, action, resource=None, outcome='allowed'):
        # Append-only within configured capacity; full ledger fails closed until
        # trusted archival/replacement. Never silently evict tombstone evidence.
        if db.execute('SELECT COUNT(*) FROM audit').fetchone()[0] >= self.audit_limit:
            raise SecurityError('security_unavailable')
        db.execute('INSERT INTO audit VALUES(?,?,?,?,?,?,?,?)', (str(uuid4()), self.clock(),
            str(principal.scope.owner) if principal else None,
            str(principal.scope.tenant) if principal else None, action,
            str(resource) if isinstance(resource, UUID) else None, outcome, 'authorization/1'))

    def audit_authentication(self, accepted):
        with self.transaction() as db:
            self._audit(db, None, 'AUTHENTICATION', outcome='allowed' if accepted else 'denied')

    @staticmethod
    def _identity(p):
        return json.dumps([p.issuer, p.tenant_identity, p.subject], separators=(',', ':'))

    @staticmethod
    def _permissions(p):
        return json.dumps(sorted(a.value for a in p.permissions))

    def register(self, principal):
        if type(principal) is not Principal or principal.expires <= self.clock():
            raise SecurityError('authentication_required')
        with self.transaction() as db:
            row = db.execute('SELECT * FROM principals WHERE owner=?', (str(principal.scope.owner),)).fetchone()
            if row:
                if row['identity'] != self._identity(principal) or row['tenant'] != str(principal.scope.tenant) or row['disabled']:
                    raise SecurityError()
                # Role changes invalidate existing request snapshots.
                if row['permissions'] != self._permissions(principal) or row['kind'] != principal.kind:
                    db.execute('UPDATE principals SET permissions=?,kind=?,epoch=epoch+1 WHERE owner=?',
                               (self._permissions(principal), principal.kind, str(principal.scope.owner)))
            else:
                db.execute('INSERT INTO principals VALUES(?,?,?,?,?,0,0)', (str(principal.scope.owner),
                    str(principal.scope.tenant), self._identity(principal), self._permissions(principal), principal.kind))
            self._audit(db, principal, 'AUTHENTICATION')

    def _principal(self, db, p):
        if type(p) is not Principal or p.expires <= self.clock():
            raise SecurityError('authentication_required')
        row = db.execute('SELECT * FROM principals WHERE owner=?', (str(p.scope.owner),)).fetchone()
        if (not row or row['disabled'] or row['tenant'] != str(p.scope.tenant)
                or row['identity'] != self._identity(p) or row['permissions'] != self._permissions(p) or row['kind'] != p.kind):
            raise SecurityError()
        return row

    @audited_mutation('DOCUMENT_REGISTER')
    def register_document(self, operator, document):
        """Trusted canonical Document only, never ownership from an HTTP payload."""
        from documents.models import Document
        document = Document.model_validate(document.model_dump())
        with self.transaction() as db:
            self._principal(db, operator)
            if (Action.PUBLICATION_MANAGE not in operator.permissions
                    or document.scope.tenant != operator.scope.tenant):
                raise SecurityError()
            owner = db.execute('SELECT tenant FROM principals WHERE owner=?', (str(document.scope.owner),)).fetchone()
            if not owner or owner['tenant'] != str(document.scope.tenant):
                raise SecurityError()
            row = db.execute('SELECT * FROM documents WHERE document=?', (str(document.document_id),)).fetchone()
            if row:
                if (row['owner'] != str(document.scope.owner) or row['tenant'] != str(document.scope.tenant)
                        or row['state'] != 'ACTIVE'):
                    raise SecurityError()
                return
            db.execute('INSERT INTO documents VALUES(?,?,?,0,?)', (str(document.document_id),
                       str(document.scope.tenant), str(document.scope.owner), 'ACTIVE'))
            self._audit(db, operator, 'DOCUMENT_REGISTER', document.document_id)

    def _document(self, db, p, action, document_id):
        self._principal(db, p)
        if type(action) is not Action or type(document_id) is not UUID:
            raise SecurityError()
        row = db.execute('SELECT * FROM documents WHERE document=?', (str(document_id),)).fetchone()
        if not row or row['tenant'] != str(p.scope.tenant) or row['state'] != 'ACTIVE':
            raise SecurityError()
        if action not in {Action.DOCUMENT_READ, Action.DOCUMENT_ANALYZE, Action.DOCUMENT_SHARE, Action.DOCUMENT_DELETE}:
            raise SecurityError()
        if row['owner'] != str(p.scope.owner) and Action.TENANT_ADMIN not in p.permissions:
            if action not in {Action.DOCUMENT_READ, Action.DOCUMENT_ANALYZE} or not db.execute(
                    'SELECT 1 FROM grants WHERE document=? AND grantee=? AND revoked IS NULL',
                    (str(document_id), str(p.scope.owner))).fetchone():
                raise SecurityError()
        return row

    def authorize(self, principal, action, resource=None):
        denied = False
        with self.transaction() as db:
            try:
                self._principal(db, principal)
                if action in {Action.PUBLICATION_MANAGE, Action.TENANT_ADMIN}:
                    if type(action) is not Action or action not in principal.permissions:
                        raise SecurityError()
                elif action in {Action.SESSION_READ, Action.SESSION_WRITE, Action.USAGE_READ}:
                    if type(action) is not Action or resource != principal.scope:
                        raise SecurityError()
                else:
                    self._document(db, principal, action, resource)
            except SecurityError:
                denied = True
            self._audit(db, principal if type(principal) is Principal else None,
                        action.value if type(action) is Action else 'UNKNOWN', resource,
                        'denied' if denied else 'allowed')
        if denied:
            raise SecurityError()

    def snapshot(self, principal, document_ids=(), action=Action.DOCUMENT_ANALYZE):
        if not isinstance(document_ids, tuple) or len(document_ids) > 32 or len(set(document_ids)) != len(document_ids):
            raise SecurityError()
        denied = False
        with self.transaction() as db:
            try:
                p = self._principal(db, principal)
                docs = tuple((d, Scope(tenant=r['tenant'], owner=r['owner']), r['epoch'])
                    for d in document_ids for r in [self._document(db, principal, action, d)])
                snapshot = AuthorizationSnapshot(principal, p['epoch'], docs, action)
            except SecurityError:
                denied = True
            self._audit(db, principal if type(principal) is Principal else None, 'AUTHORIZE',
                        outcome='denied' if denied else 'allowed')
        if denied:
            raise SecurityError()
        return snapshot

    def _revalidate(self, db, snapshot):
        if type(snapshot) is not AuthorizationSnapshot or snapshot.policy_version != 'authorization/1':
            raise SecurityError()
        p = self._principal(db, snapshot.principal)
        if p['epoch'] != snapshot.principal_epoch:
            raise SecurityError()
        for doc, scope, epoch in snapshot.documents:
            r = self._document(db, snapshot.principal, snapshot.action, doc)
            if r['epoch'] != epoch or scope != Scope(tenant=r['tenant'], owner=r['owner']):
                raise SecurityError()

    @contextmanager
    def release(self, snapshot):
        """Serialize bounded local output/persistence with revocation commit.

        Keep this guard around the actual release, never the upstream call. A
        revocation acknowledged before guard acquisition blocks output. Bytes
        already handed to the transport cannot be withdrawn.
        """
        with self.transaction() as db:
            self._revalidate(db, snapshot)
            yield

    def revalidate(self, snapshot):
        with self.release(snapshot):
            pass

    @audited_mutation('SHARE_MUTATION')
    def share(self, principal, document_id, grantee_id, *, revoke=False):
        if type(grantee_id) is not UUID:
            raise SecurityError()
        with self.transaction() as db:
            self._document(db, principal, Action.DOCUMENT_SHARE, document_id)
            grantee = db.execute('SELECT * FROM principals WHERE owner=?', (str(grantee_id),)).fetchone()
            if not grantee or grantee['tenant'] != str(principal.scope.tenant) or grantee['disabled']:
                raise SecurityError()
            row = db.execute('SELECT * FROM grants WHERE document=? AND grantee=?',
                             (str(document_id), str(grantee_id))).fetchone()
            if row and ((row['revoked'] is not None) == revoke):
                return row['grant_id']
            if revoke and not row:
                raise SecurityError()
            grant_id = row['grant_id'] if row else str(uuid4())
            db.execute('INSERT INTO grants VALUES(?,?,?,?,?) ON CONFLICT(document,grantee) DO UPDATE SET revoked=excluded.revoked',
                (grant_id, str(document_id), str(grantee_id), self.clock(), self.clock() if revoke else None))
            db.execute('UPDATE documents SET epoch=epoch+1 WHERE document=?', (str(document_id),))
            self._audit(db, principal, 'SHARE_REVOKE' if revoke else 'SHARE_CREATE', document_id)
            return grant_id

    @audited_mutation('TOMBSTONED')
    def tombstone(self, principal, document_id):
        with self.transaction() as db:
            self._principal(db, principal)
            r = db.execute('SELECT * FROM documents WHERE document=?', (str(document_id),)).fetchone()
            if (not r or r['tenant'] != str(principal.scope.tenant)
                    or (r['owner'] != str(principal.scope.owner) and Action.TENANT_ADMIN not in principal.permissions)):
                raise SecurityError()
            if r['state'] != 'ACTIVE':
                return r['state']
            # DELETE_REQUESTED and TOMBSTONED are one atomic local transition.
            self._audit(db, principal, 'DELETE_REQUESTED', document_id)
            db.execute("UPDATE documents SET state='TOMBSTONED',epoch=epoch+1 WHERE document=?", (str(document_id),))
            db.execute('UPDATE grants SET revoked=COALESCE(revoked,?) WHERE document=?', (self.clock(), str(document_id)))
            self._audit(db, principal, 'TOMBSTONED', document_id)
            return 'TOMBSTONED'

    @audited_mutation('PURGE_PENDING')
    def track_purge(self, operator, document_id):
        """No unsafe deletion: existing adapters cannot prove a complete inventory."""
        with self.transaction() as db:
            self._principal(db, operator)
            r = db.execute('SELECT * FROM documents WHERE document=?', (str(document_id),)).fetchone()
            if (Action.PUBLICATION_MANAGE not in operator.permissions or not r
                    or r['tenant'] != str(operator.scope.tenant) or r['state'] not in {'TOMBSTONED', 'PURGE_PENDING'}):
                raise SecurityError()
            inventory = json.dumps(['canonical_source', 'extraction', 'digestion_checkpoints',
                                    'retained_publication_manifests', 'retained_vectors', 'temporary_objects',
                                    'conversation_references'])
            db.execute('INSERT OR IGNORE INTO purge VALUES(?,?,?,?)',
                       (str(document_id), inventory, 'PURGE_PENDING', 'complete_reference_inventory_and_delete_adapters_required'))
            db.execute("UPDATE documents SET state='PURGE_PENDING' WHERE document=?", (str(document_id),))
            self._audit(db, operator, 'PURGE_PENDING', document_id)
            return dict(db.execute('SELECT * FROM purge WHERE document=?', (str(document_id),)).fetchone())

    @audited_mutation('PRINCIPAL_DISABLE')
    def disable_principal(self, operator, owner):
        with self.transaction() as db:
            self._principal(db,operator)
            target=db.execute('SELECT tenant FROM principals WHERE owner=?',(str(owner),)).fetchone()
            if (Action.TENANT_ADMIN not in operator.permissions or type(owner) is not UUID
                    or not target or target['tenant']!=str(operator.scope.tenant)):
                raise SecurityError()
            db.execute('UPDATE principals SET disabled=1,epoch=epoch+1 WHERE owner=? AND disabled=0',(str(owner),))
            self._audit(db,operator,'PRINCIPAL_DISABLE',owner)
