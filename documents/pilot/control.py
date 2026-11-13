"""Durable session/stop authority. Operational intents, never a financial ledger."""

import json
import sqlite3
import time
from contextlib import closing, contextmanager
from pathlib import Path
from uuid import uuid4

from documents.jobs.models import canonical
from documents.models import ObjectRef
from documents.pilot.models import PilotError, SessionApproval, SourceApproval
from security.database import Database
from security.models import SecurityError

SCHEMA = (
    "CREATE TABLE configuration (singleton INTEGER PRIMARY KEY, binding TEXT NOT NULL, stopped INTEGER NOT NULL, epoch INTEGER NOT NULL)",
    "CREATE TABLE sessions (id TEXT PRIMARY KEY, owner TEXT NOT NULL, approval TEXT NOT NULL, source TEXT NOT NULL, state TEXT NOT NULL, epoch INTEGER NOT NULL, data TEXT NOT NULL)",
    "CREATE TABLE operations (id TEXT PRIMARY KEY, session TEXT NOT NULL REFERENCES sessions(id), kind TEXT NOT NULL, state TEXT NOT NULL)",
    "CREATE TABLE objects (session TEXT NOT NULL REFERENCES sessions(id), ref TEXT NOT NULL, state TEXT NOT NULL, PRIMARY KEY(session,ref))",
    "CREATE TABLE events (id TEXT PRIMARY KEY, session TEXT, action TEXT NOT NULL, at REAL NOT NULL)",
    "CREATE TABLE feedback (session TEXT PRIMARY KEY REFERENCES sessions(id), record TEXT NOT NULL)",
    "CREATE TABLE reviews (session TEXT NOT NULL REFERENCES sessions(id), reviewer TEXT NOT NULL, evidence TEXT NOT NULL, record TEXT NOT NULL, PRIMARY KEY(session,reviewer,evidence))",
    "CREATE TABLE answers (id TEXT PRIMARY KEY, session TEXT NOT NULL REFERENCES sessions(id), evidence TEXT NOT NULL, record TEXT NOT NULL)",
)


class PilotControl(Database):
    def __init__(self, path, binding, policy, *, clock=time.time, initialize=False):
        if type(initialize) is not bool:
            raise PilotError()
        exists = Path(path).exists()
        if (initialize and exists) or (not initialize and not exists):
            # A missing authority is an outage, not a new pilot. Only explicit
            # first-time initialization may create an empty control database.
            raise PilotError("pilot_reconciliation_required")
        self.path = Path(path)
        self._allow_initial_creation = initialize
        self._safe()
        if not initialize:
            # The shared Database base initializes empty files. Reopen must
            # instead require an already initialized, bound authority.
            try:
                with closing(
                    sqlite3.connect(self.path.as_uri() + "?mode=ro", uri=True)
                ) as db:
                    if db.execute("PRAGMA user_version").fetchone()[0] != 1:
                        raise PilotError("pilot_reconciliation_required")
                    row = db.execute(
                        "SELECT binding FROM configuration WHERE singleton=1"
                    ).fetchone()
                    if row is None or row[0] != canonical(binding):
                        raise PilotError("pilot_reconciliation_required")
            except sqlite3.Error:
                raise PilotError("pilot_reconciliation_required") from None
        self.binding, self.policy, self.clock = canonical(binding), policy, clock
        super().__init__(path, SCHEMA)
        self._allow_initial_creation = False
        with self.transaction() as db:
            row = db.execute("SELECT binding FROM configuration").fetchone()
            if row and row[0] != self.binding:
                raise PilotError()
            db.execute(
                "INSERT OR IGNORE INTO configuration VALUES(1,?,0,0)", (self.binding,)
            )

    def _safe(self):
        super()._safe()
        if not self._allow_initial_creation and not self.path.exists():
            raise SecurityError("security_unavailable")

    def event(self, db, session, action):
        if (
            db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
            >= self.policy.audit_limit
        ):
            raise PilotError("pilot_limit")
        db.execute(
            "INSERT INTO events VALUES(?,?,?,?)",
            (str(uuid4()), str(session) if session else None, action, self.clock()),
        )

    def _config(self, db):
        row = db.execute("SELECT * FROM configuration WHERE singleton=1").fetchone()
        if row is None or row["binding"] != self.binding:
            raise PilotError()
        return row

    def get(self, db, session, owner, *, active=True, execution=False):
        cfg = self._config(db)
        row = db.execute(
            "SELECT * FROM sessions WHERE id=? AND owner=?", (str(session), owner)
        ).fetchone()
        if row is None:
            raise PilotError()
        result = dict(row)
        result["approval"] = (
            None
            if row["approval"] == "REDACTED"
            else SessionApproval.model_validate_json(row["approval"])
        )
        result["source"] = SourceApproval.model_validate_json(row["source"])
        result["data"] = json.loads(row["data"])
        if active and (cfg["stopped"] or row["state"] != "OPEN"):
            raise PilotError("pilot_stopped")
        if active and result["approval"] is None:
            raise PilotError()
        if (
            active
            and db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
            >= self.policy.audit_limit
        ):
            raise PilotError("pilot_limit")
        if active and (
            result["approval"].expires_at.timestamp() <= self.clock()
            or result["source"].expires_at.timestamp() <= self.clock()
        ):
            raise PilotError()
        if execution and (
            not result["data"].get("execution_authorized")
            or self.clock() >= result["data"]["deadline"]
        ):
            raise PilotError("pilot_limit")
        return result

    def create(self, approval, source, owner):
        with self.transaction() as db:
            if self._config(db)["stopped"]:
                raise PilotError("pilot_stopped")
            if db.execute("SELECT 1 FROM sessions WHERE state='OPEN'").fetchone():
                raise PilotError("pilot_limit")
            if (
                db.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
                >= self.policy.max_sessions
            ):
                raise PilotError("pilot_limit")
            db.execute(
                "INSERT INTO sessions VALUES(?,?,?,?,?,0,?)",
                (
                    str(approval.session_id),
                    owner,
                    approval.model_dump_json(),
                    source.model_dump_json(),
                    "OPEN",
                    "{}",
                ),
            )
            self.event(db, approval.session_id, "SESSION_APPROVED")

    def update(self, db, row, **values):
        data = {**row["data"], **values}
        db.execute(
            "UPDATE sessions SET data=? WHERE id=?", (canonical(data), row["id"])
        )

    def check(self, session, owner, *, execution=False):
        with self.transaction() as db:
            return self.get(db, session, owner, execution=execution)

    def object(self, session, ref, state):
        with self.transaction() as db:
            self._config(db)
            db.execute(
                "INSERT INTO objects VALUES(?,?,?) ON CONFLICT(session,ref) DO UPDATE SET state=excluded.state",
                (str(session), ref.model_dump_json(), state),
            )

    def begin(self, session, owner, operation, kind):
        with self.transaction() as db:
            row = self.get(db, session, owner, execution=True)
            # One provider request across ALL pilot sessions, retained after crash.
            if db.execute(
                "SELECT 1 FROM operations WHERE state IN ('ACTIVE','UNKNOWN')"
            ).fetchone():
                raise PilotError("pilot_reconciliation_required")
            limit = (
                row["data"]["planned_calls"]
                if kind == "synthesis"
                else self.policy.max_questions
            )
            if (
                db.execute(
                    "SELECT COUNT(*) FROM operations WHERE session=? AND kind=?",
                    (str(session), kind),
                ).fetchone()[0]
                >= limit
            ):
                raise PilotError("pilot_limit")
            if db.execute(
                "SELECT 1 FROM operations WHERE id=?", (str(operation),)
            ).fetchone():
                raise PilotError()  # No replay, including failed/denied attempts.
            db.execute(
                "INSERT INTO operations VALUES(?,?,?,?)",
                (str(operation), str(session), kind, "ACTIVE"),
            )
            self.event(db, session, "CALL_INTENT")

    def finish(self, operation, *, uncertain=False):
        with self.transaction() as db:
            self._config(db)
            db.execute(
                "UPDATE operations SET state=? WHERE id=? AND state='ACTIVE'",
                ("UNKNOWN" if uncertain else "DONE", str(operation)),
            )
            self.event(db, None, "CALL_UNCERTAIN" if uncertain else "CALL_FINISHED")
            if uncertain:
                db.execute("UPDATE configuration SET stopped=1,epoch=epoch+1")

    @contextmanager
    def release(self, session, owner, epoch):
        with self.transaction() as db:
            row = self.get(db, session, owner)
            if row["epoch"] != epoch:
                raise PilotError()
            yield row

    def stop(self):
        with self.transaction() as db:
            self._config(db)
            db.execute("UPDATE configuration SET stopped=1,epoch=epoch+1")
            db.execute(
                "UPDATE sessions SET state='STOPPED',epoch=epoch+1 WHERE state='OPEN'"
            )
            # Stop must remain durable even if append-only audit capacity is
            # exhausted. The stop flag/epoch itself is retained evidence.
            if (
                db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
                < self.policy.audit_limit
            ):
                self.event(db, None, "EMERGENCY_STOP")

    def close(self, session, owner, *, withdrawal=False):
        with self.transaction() as db:
            row = self.get(db, session, owner, active=False)
            if row["state"] not in {"CLOSED", "WITHDRAWN"}:
                db.execute(
                    "UPDATE sessions SET state=?,epoch=epoch+1 WHERE id=?",
                    ("WITHDRAWN" if withdrawal else "CLOSED", row["id"]),
                )
                # No cached presentation or question/answer text is persisted.
                self.event(db, session, "WITHDRAWN" if withdrawal else "SESSION_CLOSED")
            return row

    def inventory(self, session, owner):
        with self.transaction() as db:
            row = self.get(db, session, owner, active=False)
            objects = [
                (ObjectRef.model_validate_json(r["ref"]), r["state"])
                for r in db.execute(
                    "SELECT ref,state FROM objects WHERE session=?", (row["id"],)
                )
            ]
            operations = [
                dict(r)
                for r in db.execute(
                    "SELECT id,kind,state FROM operations WHERE session=?", (row["id"],)
                )
            ]
            return row, objects, operations

    def reopen_intake(self):
        # This never reopens a stopped session or clears an uncertain intent.
        with self.transaction() as db:
            self._config(db)
            if db.execute(
                "SELECT 1 FROM operations WHERE state IN ('ACTIVE','UNKNOWN')"
            ).fetchone():
                raise PilotError("pilot_reconciliation_required")
            db.execute("UPDATE configuration SET stopped=0,epoch=epoch+1")
            self.event(db, None, "INTAKE_REOPENED")

    def retire_metadata(self, session, owner):
        with self.transaction() as db:
            row = self.get(db, session, owner, active=False)
            if row["state"] not in {"CLOSED", "WITHDRAWN", "STOPPED"}:
                raise PilotError()
            if row["approval"] is None:
                return
            approval = row["approval"]
            if self.clock() < approval.metadata_retention_until.timestamp():
                raise PilotError()
            self.update(
                db,
                row,
                metadata_redacted=True,
                metadata_retention_until=approval.metadata_retention_until.isoformat(),
                retention_reference=approval.retention_reference,
                original_mode=approval.mode,
            )
            db.execute(
                "UPDATE sessions SET approval='REDACTED' WHERE id=?", (row["id"],)
            )
            for table in ("feedback", "reviews", "answers"):
                db.execute(f"DELETE FROM {table} WHERE session=?", (row["id"],))
            self.event(db, session, "METADATA_LOGICALLY_REDACTED")
