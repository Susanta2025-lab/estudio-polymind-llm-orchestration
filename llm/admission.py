"""Shared quota admission and durable observations, never a retry scheduler.

All workers sharing a provider quota MUST use the same authority/key/policy.
SQLite is a multi-process single-host reference, not a shared AKS database.
Unfinished calls retain slots indefinitely: a crash must not silently release an
external call that could still be running. Reconciliation needs operator proof
of termination; it must never guess that an expired worker implies zero cost.
"""
from contextlib import contextmanager
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import sqlite3
import stat
import time
from typing import Literal, Protocol
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator

from llm.inference import InferenceConfigurationError, InferenceRateLimitError, InferenceUsage


class AdmissionPolicy(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid')
    rpm: int = Field(gt=0)
    tpm: int = Field(gt=0)
    concurrent: int = Field(gt=1)
    interactive_rpm: int = Field(gt=0)
    interactive_tpm: int = Field(gt=0)
    interactive_slots: int = Field(gt=0)
    per_job_concurrent: int = Field(default=1, gt=0)
    per_job_rpm: int = Field(gt=0)

    @model_validator(mode='after')
    def bounds(self):
        if (self.interactive_rpm >= self.rpm or self.interactive_tpm >= self.tpm
                or self.interactive_slots >= self.concurrent
                or self.per_job_concurrent > self.concurrent - self.interactive_slots
                or self.per_job_rpm > self.rpm - self.interactive_rpm):
            raise ValueError('Invalid admission policy')
        return self


@dataclass(frozen=True)
class CallIdentity:
    scope: str
    job: UUID
    step: UUID
    attempt: int
    profile: str
    provider: str
    role: str
    model: str
    capability: str


class InferenceAdmissionPort(Protocol):
    def acquire(self, identity: CallIdentity, estimated_input: int, reserved_output: int,
                workload: Literal['INTERACTIVE', 'DOCUMENT_BACKGROUND'] = 'DOCUMENT_BACKGROUND') -> str: ...
    def finish(self, ticket: str, *, usage: InferenceUsage | None, outcome: str) -> None: ...


class SQLiteInferenceAdmission:
    def __init__(self, path: Path, quota_key: str, policy: AdmissionPolicy, *, clock=time.time):
        self.path, self.quota_key, self.policy, self.clock = Path(path), quota_key, policy, clock
        if not quota_key or len(quota_key) > 128:
            raise InferenceConfigurationError('Invalid quota identity.')
        self._safe_path()
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
        except FileExistsError:
            pass
        else:
            os.close(fd)
        with self._transaction() as db:
            schema = (
                'CREATE TABLE quota_policy (quota TEXT PRIMARY KEY, policy TEXT NOT NULL)',
                """CREATE TABLE inference_calls (
                    ticket TEXT PRIMARY KEY, quota TEXT NOT NULL, identity TEXT NOT NULL,
                    scope TEXT NOT NULL, job TEXT NOT NULL, step TEXT NOT NULL, attempt INTEGER NOT NULL,
                    workload TEXT NOT NULL, started REAL NOT NULL, estimated_input INTEGER NOT NULL,
                    reserved_output INTEGER NOT NULL, active INTEGER NOT NULL,
                    outcome TEXT NOT NULL, usage TEXT, UNIQUE(quota,scope,job,step,attempt))""",
                'CREATE INDEX calls_window ON inference_calls(quota,started)',
            )
            version = db.execute('PRAGMA user_version').fetchone()[0]
            entries = {r['name']: r['sql'] for r in db.execute(
                "SELECT name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'")}
            if version == 0 and not entries:
                for statement in schema:
                    db.execute(statement)
                db.execute('PRAGMA user_version=1')
            elif version != 1 or entries != {s.split()[2]: s for s in schema}:
                raise InferenceConfigurationError('Incompatible admission database schema.')
            encoded = policy.model_dump_json()
            row = db.execute('SELECT policy FROM quota_policy WHERE quota=?', (quota_key,)).fetchone()
            if row and row[0] != encoded:
                raise InferenceConfigurationError('Shared admission policy mismatch.')
            db.execute('INSERT OR IGNORE INTO quota_policy VALUES(?,?)', (quota_key, encoded))

    def _safe_path(self):
        if (not self.path.is_absolute() or '..' in self.path.parts or not self.path.parent.is_dir()
                or any(p.is_symlink() for p in (*self.path.parents, self.path))):
            raise InferenceConfigurationError('Invalid admission database path.')
        if self.path.exists():
            info = self.path.stat()
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise InferenceConfigurationError('Invalid admission database path.')

    @contextmanager
    def _transaction(self):
        db = None
        try:
            self._safe_path()
            db = sqlite3.connect(self.path, timeout=5, isolation_level=None)
            db.row_factory = sqlite3.Row
            db.execute('PRAGMA synchronous=FULL')
            db.execute('BEGIN IMMEDIATE')
            yield db
            db.commit()
        except (sqlite3.Error, OSError):
            raise InferenceConfigurationError('Admission state unavailable.') from None
        finally:
            if db is not None:
                db.close()  # Rolls back any uncommitted exception path.

    def acquire(self, identity, estimated_input, reserved_output, workload='DOCUMENT_BACKGROUND'):
        if (workload not in ('INTERACTIVE', 'DOCUMENT_BACKGROUND')
                or type(estimated_input) is not int or estimated_input < 0
                or type(reserved_output) is not int or reserved_output <= 0
                or identity.attempt < 1):
            raise InferenceConfigurationError('Invalid inference reservation.')
        tokens = estimated_input + reserved_output
        p = self.policy
        background = workload == 'DOCUMENT_BACKGROUND'
        token_cap = p.tpm - p.interactive_tpm if background else p.tpm
        if tokens > token_cap:
            raise InferenceConfigurationError('Request cannot fit quota reservation.')
        with self._transaction() as db:
            now = self.clock()
            # Failed calls retain their full minute reservation; actual usage never refunds it.
            rows = list(db.execute('SELECT * FROM inference_calls WHERE quota=? AND (started>? OR active=1)',
                                   (self.quota_key, now-60)))
            recent = [r for r in rows if r['started'] > now-60]
            active = [r for r in rows if r['active']]
            docs = [r for r in recent if r['workload'] == 'DOCUMENT_BACKGROUND']
            doc_active = [r for r in active if r['workload'] == 'DOCUMENT_BACKGROUND']
            same = lambda r: r['job'] == str(identity.job) and r['scope'] == identity.scope
            reserved = lambda rs: sum(r['estimated_input'] + r['reserved_output'] for r in rs)
            denied = (len(recent) >= p.rpm or reserved(recent)+tokens > p.tpm
                      or len(active) >= p.concurrent)
            if background:
                denied |= (len(docs) >= p.rpm-p.interactive_rpm
                           or reserved(docs)+tokens > token_cap
                           or len(doc_active) >= p.concurrent-p.interactive_slots
                           or sum(same(r) for r in doc_active) >= p.per_job_concurrent
                           or sum(same(r) for r in docs) >= p.per_job_rpm)
            if denied:
                raise InferenceRateLimitError('Inference admission deferred.', retry_after=60)
            ticket = str(uuid4())
            db.execute('INSERT INTO inference_calls VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                       (ticket, self.quota_key, json.dumps(asdict(identity), default=str, sort_keys=True),
                        identity.scope, str(identity.job), str(identity.step), identity.attempt,
                        workload, now, estimated_input, reserved_output, 1, 'unknown', None))
            return ticket

    def finish(self, ticket, *, usage, outcome):
        allowed = {'success', 'timeout', 'overloaded', 'provider_unreachable', 'authentication_failure',
                   'configuration_failure', 'protocol_failure', 'model_unavailable', 'output_limit',
                   'context_exceeded', 'upstream_failure', 'unknown'}
        if outcome not in allowed:
            outcome = 'unknown'
        with self._transaction() as db:
            row = db.execute('SELECT * FROM inference_calls WHERE ticket=? AND quota=?',
                             (ticket, self.quota_key)).fetchone()
            if row is None or not row['active']:
                raise InferenceConfigurationError('Unknown or settled inference reservation.')
            db.execute('UPDATE inference_calls SET active=0,outcome=?,usage=? WHERE ticket=?',
                       (outcome, json.dumps(asdict(usage)) if usage is not None else None, ticket))

    def records(self, scope, job):
        """Trusted scoped audit access, not a public authorization API."""
        with self._transaction() as db:
            return tuple(dict(r) for r in db.execute(
                'SELECT * FROM inference_calls WHERE quota=? AND scope=? AND job=? ORDER BY started,rowid',
                (self.quota_key, scope, str(job))))
