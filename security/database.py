"""Private single-host SQLite foundation; no hostile-host or distributed claim."""
from contextlib import contextmanager
import os
from pathlib import Path
import sqlite3
import stat

from security.models import SecurityError


class Database:
    def __init__(self, path, schema):
        self.path = Path(path)
        self._expected_schema = {s.split()[2]: s for s in schema}
        self._safe()
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
        except FileExistsError:
            pass
        else:
            os.close(fd)
        with self.transaction() as db:
            entries = {r['name']: r['sql'] for r in db.execute("SELECT name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'")}
            version = db.execute('PRAGMA user_version').fetchone()[0]
            if not entries and version == 0:
                for statement in schema:
                    db.execute(statement)
                db.execute('PRAGMA user_version=1')
            elif version != 1 or entries != {s.split()[2]: s for s in schema}:
                raise SecurityError('security_configuration')

    def _safe(self):
        if (not self.path.is_absolute() or '..' in self.path.parts or not self.path.parent.is_dir()
                or any(p.is_symlink() for p in (*self.path.parents, self.path))):
            raise SecurityError('security_configuration')
        if self.path.exists():
            s = self.path.stat()
            if not stat.S_ISREG(s.st_mode) or s.st_nlink != 1 or s.st_mode & 0o077 or s.st_uid != os.geteuid():
                raise SecurityError('security_configuration')

    @contextmanager
    def transaction(self):
        db = None
        try:
            self._safe()
            db = sqlite3.connect(self.path, timeout=5, isolation_level=None)
            db.row_factory = sqlite3.Row
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('PRAGMA synchronous=FULL')
            db.execute('BEGIN IMMEDIATE')
            yield db
            db.commit()
        except (sqlite3.Error, OSError):
            raise SecurityError('security_unavailable') from None
        finally:
            if db is not None:
                db.close()

    def ready(self):
        try:
            with self.transaction() as db:
                entries = {r['name']: r['sql'] for r in db.execute(
                    "SELECT name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'")}
                return (db.execute('PRAGMA user_version').fetchone()[0] == 1
                        and entries == self._expected_schema
                        and db.execute('PRAGMA quick_check').fetchone()[0] == 'ok')
        except Exception:
            return False
