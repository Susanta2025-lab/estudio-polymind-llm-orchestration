"""Durable action intents. An ambiguous mutation is never automatically retried."""
import json
import sqlite3
from contextlib import closing
from pathlib import Path

from documents.jobs.models import fingerprint
from documents.pilot.models import PilotError
from security.database import Database
from security.models import SecurityError

SCHEMA = (
    "CREATE TABLE actions (owner TEXT NOT NULL, action TEXT NOT NULL, key TEXT NOT NULL, payload TEXT NOT NULL, result TEXT, PRIMARY KEY(owner,action,key))",
)


class Actions(Database):
    def __init__(self, path, *, initialize=False):
        if type(initialize) is not bool or initialize == Path(path).exists():
            raise PilotError("pilot_reconciliation_required")
        self.creating = initialize
        if not initialize:
            with closing(sqlite3.connect(Path(path).as_uri() + "?mode=ro", uri=True)) as db:
                if db.execute("PRAGMA user_version").fetchone()[0] != 1:
                    raise PilotError("pilot_reconciliation_required")
        super().__init__(path, SCHEMA)
        self.creating = False

    def _safe(self):
        super()._safe()
        if not self.creating and not self.path.exists():
            raise SecurityError("security_unavailable")

    def run(self, owner, action, key, payload, execute):
        digest = fingerprint(payload)
        with self.transaction() as db:
            row = db.execute("SELECT * FROM actions WHERE owner=? AND action=? AND key=?",
                             (owner, action, key)).fetchone()
            if row:
                if row["payload"] != digest:
                    raise PilotError("pilot_denied")
                if row["result"] is None:
                    raise PilotError("pilot_reconciliation_required")
                return json.loads(row["result"]), True
            db.execute("INSERT INTO actions VALUES(?,?,?,?,NULL)", (owner, action, key, digest))
        # No database/authority transaction spans inference or extraction.
        result = execute()
        with self.transaction() as db:
            db.execute("UPDATE actions SET result=? WHERE owner=? AND action=? AND key=?",
                       (json.dumps(result), owner, action, key))
        return result, False
