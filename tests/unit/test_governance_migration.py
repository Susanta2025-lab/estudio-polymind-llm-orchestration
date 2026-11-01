from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import json
import sqlite3
import time

import pytest

from governance.ledger import GovernanceLedger, Limits, QuotaPolicy, Price, PricingCatalog, GovernanceError
from governance.migration import migrate_l1_policy, target_policy, history_digest
from llm.inference import InferenceUsage
from security.models import SecurityError, _verified_principal
from tests.unit.test_governance import identity


@pytest.fixture
def state(tmp_path):
    limits = Limits(requests_per_window=4, window_seconds=86400, interactive_concurrent=1,
                    background_concurrent=1, reserved_tokens=112000, daily_tokens=112000,
                    monthly_tokens=112000, monthly_cost='5.00')
    old = QuotaPolicy(version='phase17hl-l1/1', owner=limits, tenant=limits)
    catalog = PricingCatalog(version='test/1', currency='EUR', effective_date='2026-01-01',
        operator_approved=True, prices=(Price(provider='fake', model='model', input_price='0.659978880676',
                                            output_price='3.959873284055', price_unit=1000000),))
    ledger = GovernanceLedger(tmp_path/'governance.sqlite', old, catalog)
    principal = _verified_principal('issuer', 'alice', 'tenant', expires=int(time.time())+3600)
    ticket = ledger.reserve(principal, identity(principal), 10052, 3000)
    ledger.transition(ticket, 'RESERVED', 'ADMITTING')
    ledger.transition(ticket, 'ADMITTING', 'STARTED')
    ledger.settle(ticket, InferenceUsage(1845, 1460, 3305))
    return ledger, old, catalog, principal, tmp_path/'backup.sqlite'


def migrate(state):
    ledger, old, catalog, principal, backup = state
    return migrate_l1_policy(ledger.path, old, catalog, principal.scope.identity(), backup)


def test_history_backup_idempotency_and_four_call_admission(state):
    ledger, old, catalog, principal, backup = state
    with ledger.transaction() as db:
        before = history_digest(db)
        historical = tuple(db.execute('SELECT * FROM reservations').fetchone())
    evidence = migrate(state)
    assert evidence['history_sha256'] == before
    assert backup.stat().st_mode & 0o777 == 0o600
    with sqlite3.connect(backup) as db:
        assert db.execute('SELECT policy FROM configuration').fetchone()[0] == old.model_dump_json()
    assert migrate(state) == evidence
    with ledger.transaction() as db:
        assert tuple(db.execute('SELECT * FROM reservations').fetchone()) == historical
        assert db.execute('SELECT COUNT(*) FROM events').fetchone()[0] == 2
    assert not ledger.ready()
    with pytest.raises(SecurityError): ledger.reserve(principal, identity(principal), 1, 1)
    with pytest.raises(SecurityError): GovernanceLedger(ledger.path, old, catalog)
    current = GovernanceLedger(ledger.path, target_policy(old), catalog)
    assert current.ready()
    for _ in range(4):
        ticket = current.reserve(principal, identity(principal), 25000, 3000)
        current.transition(ticket, 'RESERVED', 'ADMITTING')
        current.transition(ticket, 'ADMITTING', 'STARTED')
        current.settle(ticket, InferenceUsage(25000, 3000, 28000))
    with pytest.raises(GovernanceError): current.reserve(principal, identity(principal), 1, 1)
    with current.transaction() as db:
        assert sum(r[0]+r[1] for r in db.execute('SELECT actual_input,actual_output FROM reservations')) == 115305


def test_concurrent_migration_has_one_event_and_backup(state):
    with ThreadPoolExecutor(2) as pool:
        a, b = list(pool.map(lambda _: migrate(state), range(2)))
    assert a == b


def test_rollback_after_policy_write(state, monkeypatch):
    import governance.migration as module
    def fail(): raise RuntimeError('injected event failure')
    monkeypatch.setattr(module.time, 'time', fail)
    with pytest.raises(RuntimeError): migrate(state)
    ledger, old, *_ = state
    with ledger.transaction() as db:
        assert db.execute('SELECT policy FROM configuration').fetchone()[0] == old.model_dump_json()
        assert db.execute('SELECT COUNT(*) FROM events').fetchone()[0] == 1


@pytest.mark.parametrize('kind', ['version', 'limit', 'catalog', 'schema', 'unsettled', 'backup'])
def test_fail_closed(state, kind):
    ledger, old, catalog, principal, backup = state
    if kind in ('version', 'limit'):
        altered = old.model_dump()
        if kind == 'version': altered['version'] = 'unexpected/1'
        else: altered['owner']['monthly_cost'] = '6'
        old = QuotaPolicy.model_validate(altered)
    elif kind == 'catalog': catalog = catalog.model_copy(update={'version':'unexpected/1'})
    elif kind == 'schema':
        with ledger.transaction() as db: db.execute('CREATE TABLE unexpected (id INTEGER)')
    elif kind == 'unsettled': ledger.reserve(principal, identity(principal), 1, 1)
    else: backup.write_text('preserve'); backup.chmod(0o600)
    with pytest.raises(SecurityError):
        migrate_l1_policy(ledger.path, old, catalog, principal.scope.identity(), backup)
    with ledger.transaction() as db:
        assert json.loads(db.execute('SELECT policy FROM configuration').fetchone()[0])['version'] == 'phase17hl-l1/1'
    if kind == 'backup': assert backup.read_text() == 'preserve'
