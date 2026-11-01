"""Preparation and explicitly authorized application of the evaluation overlay."""
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5
import sqlite3

from governance.ledger import EvaluationBinding, GovernanceLedger, PricingCatalog, QuotaPolicy, SCHEMA
from governance.migration import history_digest
from security.models import SecurityError

MIGRATION = 'polymind-evaluation-migration/1'


def evaluation_policy(old, binding):
    old = QuotaPolicy.model_validate(old.model_dump())
    binding = EvaluationBinding.model_validate(binding.model_dump())
    # Adding an overlay never edits the existing production policy or replaces
    # a previous allowlist. Later changes require a separately reviewed migration.
    if old.evaluation is not None or old.version.startswith('polymind-evaluation/'):
        raise SecurityError('security_configuration')
    return QuotaPolicy.model_validate({**old.model_dump(), 'evaluation': binding.model_dump()})


def impact(rows, limits, now):
    date = datetime.fromtimestamp(now, timezone.utc)
    day = date.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    month = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0).timestamp()
    spent = [r for r in rows if r['state'] != 'RELEASED']
    unknown = lambda r: r['state'] not in {'SETTLED', 'RELEASED'}
    tokens = lambda r: r['input'] + r['output'] if unknown(r) else r['actual_input'] + r['actual_output']
    with localcontext() as ctx:
        ctx.prec = 60
        cost = sum((Decimal(r['cost'] if unknown(r) else r['actual_cost'])
                    for r in spent if r['created'] >= month or unknown(r)), Decimal(0))
        remaining_cost = str(limits.monthly_cost-cost)
    return dict(requests_remaining=limits.requests_per_window-sum(r['created'] > now-limits.window_seconds for r in rows),
                daily_tokens_remaining=limits.daily_tokens-sum(tokens(r) for r in spent if r['created'] >= day or unknown(r)),
                monthly_tokens_remaining=limits.monthly_tokens-sum(tokens(r) for r in spent if r['created'] >= month or unknown(r)),
                reserved_tokens_remaining=limits.reserved_tokens-sum(tokens(r) for r in spent if unknown(r)),
                monthly_eur_remaining=remaining_cost)


def prepare_evaluation_migration(path, old, catalog, binding, *, provider_policy, now):
    """Read-only snapshot, exact comparisons, in-memory apply/rollback rehearsal.

    No production database constructor, write transaction, backup, or activation.
    The operator must repeat preparation on quiesced authorities before activation.
    """
    new = evaluation_policy(old, binding)
    catalog = PricingCatalog.model_validate(catalog.model_dump())
    binding.validate_authorities(path, binding.provider_path, binding.provider_key, provider_policy)
    if catalog.currency != 'EUR':
        raise SecurityError('security_configuration')
    guard = GovernanceLedger.__new__(GovernanceLedger)
    guard.path = Path(path)
    guard._safe()
    source = db = None
    try:
        source = sqlite3.connect(guard.path.as_uri()+'?mode=ro', uri=True)
        db = sqlite3.connect(':memory:')
        db.row_factory = sqlite3.Row
        source.backup(db)
        entries = {r['name']: r['sql'] for r in db.execute("SELECT name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'")}
        config = list(db.execute('SELECT * FROM configuration'))
        if (entries != {s.split()[2]: s for s in SCHEMA}
                or db.execute('PRAGMA user_version').fetchone()[0] != 1
                or db.execute('PRAGMA quick_check').fetchone()[0] != 'ok'
                or len(config) != 1 or config[0]['singleton'] != 1
                or (config[0]['policy'], config[0]['catalog']) != (old.model_dump_json(), catalog.model_dump_json())):
            raise SecurityError('security_configuration')
        rows = [dict(r) for r in db.execute('SELECT * FROM reservations')]
        if (any(r['state'] not in {'SETTLED', 'RELEASED'} for r in rows)
                or db.execute('SELECT COUNT(*) FROM events').fetchone()[0] >= 100000):
            raise SecurityError('security_configuration')
        before = history_digest(db)
        quotas = {}
        for scope in binding.scopes:
            tenant = [r for r in rows if r['tenant'] == str(scope.tenant)]
            owner = [r for r in tenant if r['owner'] == str(scope.owner)]
            quotas[scope.identity()] = {
                name: {'before': impact(records, limit, now), 'after': impact(records, binding.limits(), now)}
                for name, records, limit in (('owner', owner, old.owner), ('tenant', tenant, old.tenant))}
        evidence = dict(migration=MIGRATION, old_policy=json.loads(old.model_dump_json()),
                        new_policy=json.loads(new.model_dump_json()),
                        catalog_sha256=sha256(catalog.model_dump_json().encode()).hexdigest(),
                        history_sha256=before, evaluated_at=now, quotas=quotas)
        db.execute('BEGIN IMMEDIATE')
        db.execute('UPDATE configuration SET policy=? WHERE singleton=1', (new.model_dump_json(),))
        if history_digest(db) != before:
            raise SecurityError('security_configuration')
        event_id = str(uuid5(NAMESPACE_URL, MIGRATION + new.model_dump_json()))
        scope = binding.scopes[0]
        db.execute('INSERT INTO events VALUES(?,?,?,?,?)',
                   (event_id, str(scope.tenant), str(scope.owner), json.dumps(evidence, sort_keys=True), now))
        db.rollback()
        if (db.execute('SELECT policy FROM configuration').fetchone()[0] != old.model_dump_json()
                or history_digest(db) != before):
            raise SecurityError('security_configuration')
        return dict(evidence, event_id=event_id, dry_run='PASS', rollback='PASS', activation='PENDING')
    except sqlite3.Error:
        raise SecurityError('security_configuration') from None
    finally:
        if db is not None:
            db.close()
        if source is not None:
            source.close()


def apply_evaluation_migration(db, plan, *, backup_path, authorization_reference,
                               authority_evidence, now):
    """Apply a prepared overlay inside the caller's BEGIN IMMEDIATE transaction.

    Caller must quiesce consumers, securely back up the authority, and synchronize
    local configuration before reopening consumers. This function never commits.
    Repeated activation fails closed without adding an event or changing history.
    """
    if not db.in_transaction or not authorization_reference or not authority_evidence:
        raise SecurityError('security_configuration')
    old = QuotaPolicy.model_validate(plan['old_policy'])
    new = QuotaPolicy.model_validate(plan['new_policy'])
    if (old.version != 'phase17hl-l1/2' or new.evaluation is None
            or evaluation_policy(old, new.evaluation) != new
            or plan['migration'] != MIGRATION
            or plan['dry_run'] != 'PASS' or plan['rollback'] != 'PASS'
            or plan['event_id'] != str(uuid5(NAMESPACE_URL, MIGRATION + new.model_dump_json()))):
        raise SecurityError('security_configuration')
    entries = {r['name']: r['sql'] for r in db.execute(
        "SELECT name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'")}
    config = list(db.execute('SELECT * FROM configuration'))
    if (entries != {s.split()[2]: s for s in SCHEMA}
            or db.execute('PRAGMA user_version').fetchone()[0] != 1
            or db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok'
            or len(config) != 1 or config[0]['singleton'] != 1
            or config[0]['policy'] != old.model_dump_json()
            or sha256(config[0]['catalog'].encode()).hexdigest() != plan['catalog_sha256']
            or history_digest(db) != plan['history_sha256']
            or db.execute("SELECT COUNT(*) FROM reservations WHERE state NOT IN ('SETTLED','RELEASED')").fetchone()[0]
            or db.execute('SELECT COUNT(*) FROM events').fetchone()[0] >= 100000
            or db.execute('SELECT 1 FROM events WHERE event_id=?', (plan['event_id'],)).fetchone()):
        raise SecurityError('security_configuration')
    backup_path = Path(backup_path)
    if (backup_path.is_symlink() or not backup_path.is_file()
            or backup_path.stat().st_mode & 0o077 or backup_path.parent.stat().st_mode & 0o077):
        raise SecurityError('security_configuration')
    backup = sqlite3.connect(backup_path.as_uri() + '?mode=ro', uri=True)
    try:
        backup.row_factory = sqlite3.Row
        backup.execute('PRAGMA query_only=ON')
        if (backup.execute('PRAGMA integrity_check').fetchone()[0] != 'ok'
                or [dict(r) for r in backup.execute('SELECT * FROM configuration')] != [dict(r) for r in config]
                or history_digest(backup) != plan['history_sha256']):
            raise SecurityError('security_configuration')
    finally:
        backup.close()
    evidence = dict(plan, activation='APPLIED', applied_at=now,
                    backup_path=str(backup_path),
                    backup_sha256=sha256(backup_path.read_bytes()).hexdigest(),
                    authorization_reference=authorization_reference,
                    authority_evidence=authority_evidence)
    changed = db.execute(
        'UPDATE configuration SET policy=? WHERE singleton=1 AND policy=? AND catalog=?',
        (new.model_dump_json(), old.model_dump_json(), config[0]['catalog'])).rowcount
    if changed != 1:
        raise SecurityError('security_configuration')
    scope = new.evaluation.scopes[0]
    db.execute('INSERT INTO events VALUES(?,?,?,?,?)',
               (plan['event_id'], str(scope.tenant), str(scope.owner),
                json.dumps(evidence, sort_keys=True), now))
    return evidence
