"""Explicit Phase 17H-L policy migration; preserves the authority schema and history.

The migration evidence is an event in the existing append-only event model. All
writers serialize on BEGIN IMMEDIATE, including policy checks in reserve(). This
is an operator administration operation, never an application admission fallback.
"""
from hashlib import sha256
import json
import os
from pathlib import Path
import sqlite3
import time

from governance.ledger import GovernanceLedger, QuotaPolicy, SCHEMA
from security.models import SecurityError

MIGRATION = 'phase17hl-l1-policy/2'
EVENT_ID = '3ee2b8d9-ec07-54bf-b2b3-a42c49cd2f90'
CHANGES = {'requests_per_window': [4, 5], 'daily_tokens': [112000, 115305],
           'monthly_tokens': [112000, 115305]}


def target_policy(old):
    expected = dict(requests_per_window=4, window_seconds=86400,
                    interactive_concurrent=1, background_concurrent=1,
                    reserved_tokens=112000, daily_tokens=112000,
                    monthly_tokens=112000, monthly_cost='5.00')
    if old.model_dump(mode='json') != dict(version='phase17hl-l1/1', owner=expected, tenant=expected):
        raise SecurityError('security_configuration')
    data = old.model_dump(mode='json')
    data['version'] = 'phase17hl-l1/2'
    for scope in ('owner', 'tenant'):
        data[scope].update({key: values[1] for key, values in CHANGES.items()})
    return QuotaPolicy.model_validate(data)


def history_digest(db):
    data = {table: [dict(row) for row in db.execute(f'SELECT * FROM {table} ORDER BY 1')]
            for table in ('reservations', 'events')}
    return sha256(json.dumps(data, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def migrate_l1_policy(path, old, catalog, scope, backup_path):
    """Compare-and-swap exact policy, with a durable exclusive pre-mutation backup.

    Idempotence requires the exact retained migration event and target policy.
    Unexpected schemas, policies, catalogs or unresolved obligations fail closed.
    A failed backup/transaction leaves any backup file in place for investigation.
    """
    new = target_policy(old)
    # Do not construct/create/reinitialize an authority to migrate it.
    ledger = GovernanceLedger.__new__(GovernanceLedger)
    ledger.path = Path(path)
    ledger._safe()
    if not ledger.path.is_file():
        raise SecurityError('security_configuration')
    tenant, owner = scope.split(':')
    backup_path = Path(backup_path)
    backup_guard = GovernanceLedger.__new__(GovernanceLedger)
    backup_guard.path = backup_path
    backup_guard._safe()
    if backup_path.parent.stat().st_mode & 0o077:
        raise SecurityError('security_configuration')
    with ledger.transaction() as db:
        entries = {r['name']: r['sql'] for r in db.execute("SELECT name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'")}
        if (entries != {s.split()[2]: s for s in SCHEMA}
                or db.execute('PRAGMA user_version').fetchone()[0] != 1
                or db.execute('PRAGMA quick_check').fetchone()[0] != 'ok'):
            raise SecurityError('security_configuration')
        rows = list(db.execute('SELECT * FROM configuration'))
        if len(rows) != 1 or rows[0]['singleton'] != 1 or rows[0]['catalog'] != catalog.model_dump_json():
            raise SecurityError('security_configuration')
        expected = dict(migration=MIGRATION, old_policy=json.loads(old.model_dump_json()),
                        new_policy=json.loads(new.model_dump_json()),
                        changes={s: CHANGES for s in ('owner', 'tenant')},
                        catalog_sha256=sha256(catalog.model_dump_json().encode()).hexdigest())
        event = db.execute('SELECT * FROM events WHERE event_id=?', (EVENT_ID,)).fetchone()
        if event is not None:
            evidence = json.loads(event['action'])
            if (rows[0]['policy'] != new.model_dump_json() or event['tenant'] != tenant
                    or event['owner'] != owner or any(evidence.get(k) != v for k, v in expected.items())):
                raise SecurityError('security_configuration')
            return evidence
        if (rows[0]['policy'] != old.model_dump_json()
                or db.execute("SELECT COUNT(*) FROM reservations WHERE state NOT IN ('SETTLED','RELEASED')").fetchone()[0]
                or db.execute('SELECT COUNT(*) FROM events').fetchone()[0] >= 100000):
            raise SecurityError('security_configuration')
        evidence = dict(expected, history_sha256=history_digest(db), backup_path=str(backup_path))
        fd = os.open(backup_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
        os.close(fd)
        # A separate reader sees the same committed snapshot while this writer
        # holds the reservation lock; backup API includes WAL contents if present.
        source = sqlite3.connect(ledger.path.as_uri()+'?mode=ro', uri=True)
        destination = sqlite3.connect(backup_path)
        try:
            source.backup(destination)
        finally:
            destination.close()
            source.close()
        with backup_path.open('rb') as stream:
            os.fsync(stream.fileno())
            evidence['backup_sha256'] = sha256(stream.read()).hexdigest()
        directory_fd = os.open(backup_path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
        db.execute('UPDATE configuration SET policy=? WHERE singleton=1', (new.model_dump_json(),))
        db.execute('INSERT INTO events VALUES(?,?,?,?,?)',
                   (EVENT_ID, tenant, owner, json.dumps(evidence, sort_keys=True), time.time()))
        return evidence
