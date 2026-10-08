"""Local transactional publication authority. No scheduler or physical vector transaction.

Like the Phase 17C adapter, each operation uses its own short SQLite transaction.
An epoch protects against ABA (G1 -> G2 -> G1) as well as stale expected bases.
"""
from contextlib import contextmanager
import os
from pathlib import Path
import sqlite3
import stat
from uuid import UUID

from documents.models import ObjectRef
from documents.publication.models import ActivePublication, PublicationError

SCHEMA = (
    'CREATE TABLE active (singleton INTEGER PRIMARY KEY CHECK(singleton=1), generation TEXT, epoch INTEGER NOT NULL)',
    "CREATE TABLE candidates (generation TEXT PRIMARY KEY, manifest TEXT NOT NULL, base TEXT NOT NULL, state TEXT NOT NULL CHECK(state IN ('PREPARING','READY','ACCEPTED','FAILED','STALE')), error TEXT)",
    'CREATE TABLE activations (epoch INTEGER PRIMARY KEY, generation TEXT NOT NULL, expected TEXT NOT NULL, operation TEXT NOT NULL)',
)


class SQLitePublicationAuthority:
    def __init__(self, path):
        self.path = Path(path)
        self._safe_path()
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
        except FileExistsError:
            pass
        except OSError:
            raise PublicationError('publication_unavailable') from None
        else:
            os.close(fd)
        with self.transaction() as db:
            entries = {r['name']: r['sql'] for r in db.execute(
                "SELECT name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'")}
            version = db.execute('PRAGMA user_version').fetchone()[0]
            if not entries and version == 0:
                for statement in SCHEMA:
                    db.execute(statement)
                db.execute('PRAGMA user_version=1')
                db.execute('INSERT INTO active VALUES(1,NULL,0)')
            elif version != 1 or entries != {s.split()[2]: s for s in SCHEMA}:
                raise PublicationError('publication_incompatible')

    def _safe_path(self):
        if not self.path.is_absolute() or not self.path.parent.is_dir():
            raise PublicationError('publication_invalid_input')
        for p in (*self.path.parents, self.path):
            if p.is_symlink():
                raise PublicationError('publication_invalid_input')
        if self.path.exists():
            info = self.path.stat()
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise PublicationError('publication_invalid_input')

    @contextmanager
    def transaction(self, write=True):
        db = None
        try:
            self._safe_path()
            db = sqlite3.connect(self.path, timeout=5, isolation_level=None)
            db.row_factory = sqlite3.Row
            db.execute('PRAGMA synchronous=FULL')
            db.execute('BEGIN IMMEDIATE' if write else 'BEGIN')
            yield db
            db.commit()
        except BaseException as exc:
            if db:
                db.rollback()
            if isinstance(exc, (sqlite3.Error, OSError, ValueError, TypeError)):
                raise PublicationError('publication_unavailable') from None
            raise
        finally:
            if db:
                db.close()

    @staticmethod
    def _active(db):
        row = db.execute('SELECT generation,epoch FROM active WHERE singleton=1').fetchone()
        return ActivePublication(generation=row['generation'], epoch=row['epoch'])

    def active(self):
        with self.transaction(False) as db:
            return self._active(db)

    def register(self, manifest, ref):
        with self.transaction() as db:
            row = db.execute('SELECT * FROM candidates WHERE generation=?', (str(manifest.generation),)).fetchone()
            if row:
                if ObjectRef.model_validate_json(row['manifest']) != ref:
                    raise PublicationError('publication_invalid_input')
                return
            if self._active(db) != manifest.base:
                raise PublicationError('publication_stale_candidate')
            db.execute('INSERT INTO candidates VALUES(?,?,?,?,NULL)', (
                str(manifest.generation), ref.model_dump_json(), manifest.base.model_dump_json(), 'PREPARING'))

    def candidate(self, generation):
        with self.transaction(False) as db:
            row = db.execute('SELECT * FROM candidates WHERE generation=?', (str(generation),)).fetchone()
            if row is None:
                raise PublicationError('publication_unavailable')
            return ObjectRef.model_validate_json(row['manifest']), row['state'], ActivePublication.model_validate_json(row['base'])

    def mark(self, generation, state, error=None):
        if state not in ('READY', 'FAILED', 'STALE'):
            raise PublicationError('publication_invalid_input')
        with self.transaction() as db:
            db.execute("UPDATE candidates SET state=?,error=? WHERE generation=? AND state IN ('PREPARING','READY','FAILED')",
                       (state, error, str(generation)))

    def activate(self, generation, expected, *, rollback=False):
        """Trusted service calls only, AFTER external-object and inventory validation."""
        with self.transaction() as db:
            current = self._active(db)
            row = db.execute('SELECT * FROM candidates WHERE generation=?', (str(generation),)).fetchone()
            operation = 'rollback' if rollback else 'forward'
            # Lost activation response is idempotent only at the SAME epoch.
            event = db.execute('SELECT * FROM activations WHERE epoch=?', (expected.epoch + 1,)).fetchone()
            if (current == ActivePublication(generation=generation, epoch=expected.epoch+1) and event
                    and event['generation'] == str(generation) and event['expected'] == expected.model_dump_json()
                    and event['operation'] == operation):
                return current
            if current != expected:
                raise PublicationError('publication_stale_candidate')
            if row is None or (rollback and row['state'] != 'ACCEPTED') or (not rollback and (
                    row['state'] != 'READY' or ActivePublication.model_validate_json(row['base']) != expected)):
                raise PublicationError('publication_stale_candidate')
            result = ActivePublication(generation=generation, epoch=current.epoch+1)
            db.execute('UPDATE active SET generation=?,epoch=? WHERE singleton=1', (str(generation), result.epoch))
            db.execute("UPDATE candidates SET state='ACCEPTED',error=NULL WHERE generation=?", (str(generation),))
            db.execute('INSERT INTO activations VALUES(?,?,?,?)',
                       (result.epoch, str(generation), expected.model_dump_json(), operation))
            return result

    def inventory(self):
        with self.transaction(False) as db:
            return {UUID(r['generation']): r['state'] for r in db.execute('SELECT generation,state FROM candidates')}
