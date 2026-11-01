"""Focused activation tests; synthetic SQLite only, no network or inference."""
import json
import sqlite3

import pytest

from governance.evaluation import apply_evaluation_migration, prepare_evaluation_migration
from governance.ledger import GovernanceLedger
from governance.migration import history_digest
from security.models import SecurityError
from tests.unit.test_evaluation_governance import state, no_network, settled


@pytest.mark.parametrize('failure', [None, 'history', 'backup', 'event_insert', 'repeat'])
def test_activation_atomicity_and_history(state, tmp_path, failure):
    ledger, p, _, _, now, old, binding, kwargs = state
    path = tmp_path / 'legacy.sqlite'
    legacy = GovernanceLedger(path, old, ledger.catalog, clock=lambda: now[0])
    settled(legacy, p, 3305)
    binding = binding.model_copy(update={'governance_path': str(path)})
    plan = prepare_evaluation_migration(path, old, ledger.catalog, binding,
                                      provider_policy=kwargs['provider_policy'], now=now[0])
    backup_path = tmp_path / 'backup.sqlite'
    tmp_path.chmod(0o700)
    with sqlite3.connect(path) as source, sqlite3.connect(backup_path) as backup:
        source.backup(backup)
    backup_path.chmod(0o600)
    before = path.read_bytes()
    if failure == 'history': plan['history_sha256'] = '0' * 64
    if failure == 'backup': backup_path.chmod(0o644)
    def apply():
        with legacy.transaction() as db:
            if failure == 'event_insert':
                db.set_authorizer(lambda action, table, *args:
                    sqlite3.SQLITE_DENY if action == sqlite3.SQLITE_INSERT and table == 'events'
                    else sqlite3.SQLITE_OK)
            return apply_evaluation_migration(db, plan, backup_path=backup_path,
                authorization_reference='synthetic-authorization', authority_evidence={'synthetic': True}, now=now[0])
    if failure in {'history', 'backup', 'event_insert'}:
        with pytest.raises((SecurityError, sqlite3.DatabaseError)): apply()
        assert path.read_bytes() == before
        return
    evidence = apply()
    with sqlite3.connect(path) as db:
        db.row_factory = sqlite3.Row
        assert json.loads(db.execute('SELECT policy FROM configuration').fetchone()[0]) == plan['new_policy']
        assert db.execute('SELECT COUNT(*) FROM reservations').fetchone()[0] == 1
        assert db.execute('SELECT actual_input+actual_output FROM reservations').fetchone()[0] == 3305
        action = db.execute('SELECT action FROM events WHERE event_id=?', (plan['event_id'],)).fetchone()[0]
        assert json.loads(action) == evidence
        db.execute('BEGIN')
        db.execute('DELETE FROM events WHERE event_id=?', (plan['event_id'],))
        assert history_digest(db) == plan['history_sha256']
        db.rollback()
    if failure == 'repeat':
        after = path.read_bytes()
        with pytest.raises(SecurityError): apply()
        assert path.read_bytes() == after
