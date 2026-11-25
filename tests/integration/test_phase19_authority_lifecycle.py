"""Missing and damaged real runtime authorities must never be repaired by serving."""
import os
import sqlite3

import pytest

from deployment.phase19.backup import inventory
from deployment.phase19.storage import DATABASES, ownership
from tests.integration.test_phase19_operator import external


def test_actual_authority_set_initialized_private_and_integrity_checked(external):
    root, runtime, workflow, *_ = external
    assert {p.name for p in (root / 'private').glob('*.sqlite')} == set(DATABASES)
    for name in DATABASES:
        path = root / 'private' / name
        assert path.stat().st_uid == os.geteuid()
        assert path.stat().st_mode & 0o077 == 0
        with sqlite3.connect(path.as_uri() + '?mode=ro', uri=True) as db:
            assert db.execute('PRAGMA user_version').fetchone()[0] == 1
            assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
            assert db.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0] > 0
    assert runtime.authority.ready() and runtime.governance.ready() and runtime.admission.ready()
    assert workflow.pilot.control.ready()


@pytest.mark.parametrize('name', DATABASES)
@pytest.mark.parametrize('fault', ['missing', 'truncated'])
def test_complete_reopen_denies_each_missing_or_damaged_authority(external, name, fault):
    root = external[0]
    path = root / 'private' / name
    if fault == 'missing':
        path.unlink()
    else:
        path.write_bytes(b'not a SQLite database')
    before = inventory(root / 'private')
    with pytest.raises((ValueError, OSError, sqlite3.Error)):
        with ownership(root):
            pytest.fail('Incomplete authority set was accepted')
    assert inventory(root / 'private') == before


@pytest.mark.parametrize('name', DATABASES)
def test_partial_initialization_never_overwrites_surviving_authority(external, name):
    root = external[0]
    for other in DATABASES:
        if other != name:
            (root / 'private' / other).unlink()
    before = inventory(root / 'private')
    with pytest.raises(ValueError, match='Existing authority'):
        with ownership(root, initialize=True):
            pytest.fail('Partial initialization was accepted')
    assert inventory(root / 'private') == before
