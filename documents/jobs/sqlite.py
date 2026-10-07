"""SQLite reference ledger. Local trusted filesystem only, not shared AKS state.

Short BEGIN IMMEDIATE transactions serialize writers across connections/processes.
No Python mutex and no transaction spans parser or object-store work. Connections
are per operation and always closed. UTC ISO strings have fixed microsecond width.
"""

from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import json
import os
import sqlite3
import stat
from uuid import UUID, uuid4

from pydantic import ValidationError

from documents.models import ObjectRef
from documents.jobs.errors import Failure, JobError
from documents.jobs.models import (
    Admission, Attempt, Clock, Dispatch, Job, JobSettings, Lease, Progress,
    Reconciliation, Step, StepSpec, SystemClock, canonical, fingerprint,
)

SCHEMA_VERSION = 1
TERMINAL = ('COMPLETED', 'FAILED', 'CANCELLED', 'PARTIAL')
SCHEMA = (
    """CREATE TABLE jobs (
        job_id TEXT PRIMARY KEY, run_id TEXT NOT NULL UNIQUE,
        scope TEXT NOT NULL, request_key TEXT NOT NULL, fingerprint TEXT NOT NULL,
        version_id TEXT NOT NULL, source_key TEXT NOT NULL, generation INTEGER NOT NULL CHECK(generation > 0),
        request TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
        document_created_at TEXT NOT NULL,
        state TEXT NOT NULL CHECK(state IN ('QUEUED','EXTRACTING','NORMALIZING','VALIDATING',
            'COMPLETED','FAILED','CANCEL_REQUESTED','CANCELLED','PARTIAL')),
        cancel_requested INTEGER NOT NULL DEFAULT 0 CHECK(cancel_requested IN (0,1)),
        progress TEXT NOT NULL, terminal_category TEXT,
        UNIQUE(scope, request_key), UNIQUE(scope, version_id, generation))""",
    """CREATE TABLE job_steps (
        step_id TEXT PRIMARY KEY, job_id TEXT NOT NULL REFERENCES jobs(job_id),
        unit_id TEXT NOT NULL, spec TEXT NOT NULL, step_key TEXT NOT NULL UNIQUE,
        input_fingerprint TEXT NOT NULL, execution_at TEXT NOT NULL,
        state TEXT NOT NULL CHECK(state IN ('PENDING','READY','RUNNING','RETRY_WAIT',
            'SUCCEEDED','FAILED','CANCELLED')),
        attempt_count INTEGER NOT NULL DEFAULT 0 CHECK(attempt_count >= 0),
        fence INTEGER NOT NULL DEFAULT 0 CHECK(fence >= 0),
        lease_owner TEXT, lease_expires_at TEXT, not_before TEXT NOT NULL,
        started_at TEXT, finished_at TEXT, failure_category TEXT,
        reused_from TEXT REFERENCES job_steps(step_id), UNIQUE(job_id, unit_id),
        CHECK((state = 'RUNNING' AND lease_owner IS NOT NULL AND lease_expires_at IS NOT NULL)
            OR (state != 'RUNNING' AND lease_owner IS NULL AND lease_expires_at IS NULL)))""",
    """CREATE TABLE step_attempts (
        step_id TEXT NOT NULL REFERENCES job_steps(step_id), number INTEGER NOT NULL,
        worker TEXT NOT NULL, fence INTEGER NOT NULL, started_at TEXT NOT NULL,
        finished_at TEXT, outcome TEXT NOT NULL, category TEXT, classification TEXT,
        not_before TEXT, PRIMARY KEY(step_id, number), UNIQUE(step_id, fence))""",
    """CREATE TABLE artifact_manifests (
        step_id TEXT PRIMARY KEY REFERENCES job_steps(step_id),
        manifest TEXT NOT NULL, committed_at TEXT NOT NULL, fence INTEGER NOT NULL)""",
    """CREATE TABLE manifest_objects (
        step_id TEXT NOT NULL REFERENCES artifact_manifests(step_id),
        object_key TEXT NOT NULL, PRIMARY KEY(step_id, object_key))""",
    """CREATE TABLE outbox (
        dispatch_id INTEGER PRIMARY KEY AUTOINCREMENT,
        step_id TEXT NOT NULL REFERENCES job_steps(step_id),
        created_at TEXT NOT NULL, available_at TEXT NOT NULL, delivered_at TEXT)""",
    """CREATE TABLE dead_letters (
        step_id TEXT PRIMARY KEY REFERENCES job_steps(step_id),
        category TEXT NOT NULL, classification TEXT NOT NULL, created_at TEXT NOT NULL)""",
    """CREATE TABLE object_intents (
        step_id TEXT NOT NULL REFERENCES job_steps(step_id), object_key TEXT NOT NULL,
        ref TEXT NOT NULL, created_at TEXT NOT NULL, PRIMARY KEY(step_id, object_key))""",
    'CREATE INDEX steps_scheduler ON job_steps(state, not_before, lease_expires_at)',
    'CREATE INDEX outbox_pending ON outbox(delivered_at, available_at)',
    'CREATE INDEX outbox_step ON outbox(step_id, created_at)',
    'CREATE INDEX objects_age ON object_intents(created_at)',
    'CREATE INDEX objects_key ON object_intents(object_key)',
    'CREATE INDEX manifest_key ON manifest_objects(object_key)',
    'CREATE INDEX source_key ON jobs(source_key)',
)


def stamp(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise JobError('invalid_configuration')
    return value.astimezone(timezone.utc).isoformat(timespec='microseconds')


def time_of(value: str) -> datetime:
    return datetime.fromisoformat(value)


def bounded(limit):
    if not isinstance(limit, int) or not 1 <= limit <= 1000:
        raise JobError('invalid_configuration')
    return limit


class SQLiteJobLedger:
    def __init__(self, settings: JobSettings, clock: Clock | None = None):
        self.settings = settings
        self.clock = clock or SystemClock()
        self.path = settings.database_path
        if not self.path.is_absolute() or '..' in self.path.parts:
            raise JobError('invalid_configuration')
        try:
            self._safe_path()
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
            except FileExistsError:
                pass
            else:
                os.close(fd)
            with self._transaction() as (db, _):
                version = db.execute('PRAGMA user_version').fetchone()[0]
                entries = {r['name']: r['sql'] for r in db.execute(
                    "SELECT name, sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'")}
                if version == 0 and not entries:
                    for statement in SCHEMA:
                        db.execute(statement)
                    db.execute(f'PRAGMA user_version = {SCHEMA_VERSION}')
                elif version != SCHEMA_VERSION or entries != {
                        statement.split()[2]: statement for statement in SCHEMA}:
                    raise JobError('schema_mismatch')
        except JobError:
            raise
        except (OSError, sqlite3.Error):
            raise JobError('ledger_error') from None

    def _safe_path(self):
        # Operator-controlled directory: reject obvious symlinks/special files,
        # not a defense against a hostile process replacing ancestors concurrently.
        for part in (*reversed(self.path.parents), self.path):
            if part.is_symlink():
                raise JobError('invalid_configuration')
        if self.path.exists():
            info = self.path.stat()
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise JobError('invalid_configuration')
        if not self.path.parent.is_dir():
            raise JobError('invalid_configuration')

    @contextmanager
    def _transaction(self, *, write=True):
        db = None
        try:
            self._safe_path()
            db = sqlite3.connect(str(self.path), timeout=self.settings.busy_timeout_seconds,
                                 isolation_level=None)
            db.row_factory = sqlite3.Row
            db.execute('PRAGMA foreign_keys = ON')
            db.execute('PRAGMA synchronous = FULL')
            db.execute('BEGIN IMMEDIATE' if write else 'BEGIN')
            now = stamp(self.clock.now())  # After acquiring writer authority.
            yield db, now
            db.commit()
        except BaseException as exc:
            if db is not None:
                try:
                    db.rollback()
                except sqlite3.Error:
                    raise JobError('ledger_error') from None
            if isinstance(exc, (sqlite3.Error, OSError, ValidationError, ValueError, TypeError)):
                raise JobError('ledger_error') from None
            raise
        finally:
            if db is not None:
                db.close()

    @staticmethod
    def _job(db, scope, job_id):
        row = db.execute('SELECT * FROM jobs WHERE job_id=? AND scope=?',
                         (str(job_id), scope.identity())).fetchone()
        if row is None:
            raise JobError('job_not_found')
        return row

    @staticmethod
    def _step(db, job_id, step_id):
        row = db.execute('SELECT * FROM job_steps WHERE step_id=? AND job_id=?',
                         (str(step_id), str(job_id))).fetchone()
        if row is None:
            raise JobError('step_not_found')
        return row

    @staticmethod
    def _job_model(row):
        return Job(job_id=row['job_id'], run_id=row['run_id'], generation=row['generation'],
                   admission=Admission.model_validate_json(row['request']),
                   request_fingerprint=row['fingerprint'], created_at=row['created_at'],
                   updated_at=row['updated_at'], document_created_at=row['document_created_at'],
                   state=row['state'], cancel_requested=bool(row['cancel_requested']),
                   progress=Progress.model_validate_json(row['progress']),
                   terminal_category=row['terminal_category'])

    @staticmethod
    def _manifest(db, step_id):
        row = db.execute('SELECT manifest FROM artifact_manifests WHERE step_id=?', (str(step_id),)).fetchone()
        return tuple(ObjectRef.model_validate(r) for r in json.loads(row[0])) if row else ()

    def _step_model(self, db, row):
        return Step(**{key: row[key] for key in (
            'step_id', 'job_id', 'step_key', 'input_fingerprint', 'execution_at', 'state',
            'attempt_count', 'fence', 'lease_owner', 'lease_expires_at', 'not_before',
            'started_at', 'finished_at', 'failure_category', 'reused_from')},
            spec=StepSpec.model_validate_json(row['spec']), manifest=self._manifest(db, row['step_id']))

    @staticmethod
    def _enqueue(db, step_id, now, available):
        db.execute('INSERT INTO outbox(step_id,created_at,available_at) VALUES(?,?,?)',
                   (step_id, now, available))

    def _activate(self, db, job, now):
        request = Admission.model_validate_json(job['request'])
        rows = {r['unit_id']: r for r in db.execute('SELECT * FROM job_steps WHERE job_id=?', (job['job_id'],))}
        for row in rows.values():
            if row['state'] != 'PENDING':
                continue
            spec = StepSpec.model_validate_json(row['spec'])
            if not all(rows[parent]['state'] == 'SUCCEEDED' for parent in spec.depends_on):
                continue
            parents = [[ref.model_dump(mode='json') for ref in self._manifest(db, rows[parent]['step_id'])]
                       for parent in spec.depends_on]
            inputs = fingerprint([request.compatibility(), spec.model_dump(mode='json'), parents])
            key = fingerprint([request.scope.identity(), str(request.document_version_id),
                               job['run_id'], job['generation'], inputs])
            db.execute("UPDATE job_steps SET state='READY', step_key=?, input_fingerprint=? WHERE step_id=?",
                       (key, inputs, row['step_id']))
            self._enqueue(db, row['step_id'], now, now)

    def _refresh(self, db, job_id, now):
        job = db.execute('SELECT * FROM jobs WHERE job_id=?', (job_id,)).fetchone()
        rows = list(db.execute('SELECT state,spec FROM job_steps WHERE job_id=?', (job_id,)))
        counts = {state: sum(r['state'] == state for r in rows) for state in (
            'PENDING', 'READY', 'RUNNING', 'RETRY_WAIT', 'SUCCEEDED', 'FAILED', 'CANCELLED')}
        current = next((json.loads(r['spec'])['stage'] for r in rows if r['state'] == 'RUNNING'), None)
        progress = Progress(total=len(rows), completed=counts['SUCCEEDED'], running=counts['RUNNING'],
                            retrying=counts['RETRY_WAIT'], failed=counts['FAILED'], cancelled=counts['CANCELLED'],
                            pending=counts['PENDING'] + counts['READY'], current_stage=current)
        if job['state'] in TERMINAL:
            state = job['state']
        elif job['cancel_requested']:
            state = 'CANCEL_REQUESTED' if counts['RUNNING'] else 'CANCELLED'
        elif counts['FAILED']:
            state = 'FAILED'
        elif counts['SUCCEEDED'] == len(rows):
            state = 'COMPLETED'
        else:
            state = current or 'QUEUED'
        db.execute('UPDATE jobs SET state=?,progress=?,updated_at=? WHERE job_id=?',
                   (state, progress.model_dump_json(), now, job_id))

    def admit(self, request):
        try:
            request = Admission.model_validate(request.model_dump(mode='json'))
        except Exception:
            raise JobError('invalid_configuration') from None
        with self._transaction() as (db, now):
            existing = db.execute('SELECT * FROM jobs WHERE scope=? AND request_key=?',
                                  (request.scope.identity(), request.request_idempotency_key)).fetchone()
            if existing:
                if existing['fingerprint'] != request.digest():
                    raise JobError('idempotency_conflict')
                return self._job_model(existing)
            prior, reusable = None, {}
            if request.resume_from:
                prior = self._job(db, request.scope, request.resume_from)
                if prior['state'] not in TERMINAL:
                    raise JobError('invalid_transition')
                old_request = Admission.model_validate_json(prior['request'])
                if (old_request.document_id != request.document_id or
                        old_request.document_version_id != request.document_version_id):
                    raise JobError('invalid_transition')
                if old_request.compatibility() == request.compatibility():
                    reusable = {r['unit_id']: r for r in db.execute(
                        "SELECT * FROM job_steps WHERE job_id=? AND state='SUCCEEDED'", (prior['job_id'],))}
            generation = db.execute('SELECT COALESCE(MAX(generation),0)+1 FROM jobs WHERE scope=? AND version_id=?',
                                    (request.scope.identity(), str(request.document_version_id))).fetchone()[0]
            job_id, run_id = str(uuid4()), str(uuid4())
            document_time = prior['document_created_at'] if prior else now
            db.execute('''INSERT INTO jobs(job_id,run_id,scope,request_key,fingerprint,version_id,source_key,generation,
                request,created_at,updated_at,document_created_at,state,progress) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                       (job_id, run_id, request.scope.identity(), request.request_idempotency_key, request.digest(),
                        str(request.document_version_id), str(request.source.key), generation, request.model_dump_json(), now, now,
                        document_time, 'QUEUED', Progress().model_dump_json()))
            # A deliberate reprocess must differ even if the clock has not advanced.
            last = db.execute('''SELECT MAX(s.execution_at) FROM job_steps s JOIN jobs j ON j.job_id=s.job_id
                WHERE j.scope=? AND j.version_id=?''',
                              (request.scope.identity(), str(request.document_version_id))).fetchone()[0]
            execution = max(now, stamp(time_of(last) + timedelta(microseconds=1))) if last else now
            copied = set()
            for spec in request.steps:
                step_id = str(uuid4())
                old = reusable.get(spec.unit_id)
                reuse = (old is not None and StepSpec.model_validate_json(old['spec']) == spec
                         and set(spec.depends_on).issubset(copied))
                key = (fingerprint([request.scope.identity(), str(request.document_version_id),
                                    run_id, generation, old['input_fingerprint']]) if reuse else
                       fingerprint([run_id, spec.model_dump(mode='json'), 'planned']))
                db.execute('''INSERT INTO job_steps(step_id,job_id,unit_id,spec,step_key,input_fingerprint,
                    execution_at,state,not_before,finished_at,reused_from) VALUES(?,?,?,?,?,?,?,?,?,?,?)''',
                           (step_id, job_id, spec.unit_id, spec.model_dump_json(), key,
                            old['input_fingerprint'] if reuse else request.compatibility(),
                            old['execution_at'] if reuse else execution, 'SUCCEEDED' if reuse else 'PENDING',
                            now, now if reuse else None, old['step_id'] if reuse else None))
                if reuse:
                    manifest = db.execute('SELECT manifest FROM artifact_manifests WHERE step_id=?', (old['step_id'],)).fetchone()[0]
                    db.execute('INSERT INTO artifact_manifests VALUES(?,?,?,?)', (step_id, manifest, now, 0))
                    for ref in json.loads(manifest):
                        db.execute('INSERT INTO manifest_objects VALUES(?,?)', (step_id, ref['key']))
                    copied.add(spec.unit_id)
            job = self._job(db, request.scope, job_id)
            self._activate(db, job, now)
            self._refresh(db, job_id, now)
            return self._job_model(self._job(db, request.scope, job_id))

    def get_job(self, scope, job_id):
        with self._transaction(write=False) as (db, _):
            return self._job_model(self._job(db, scope, job_id))

    def steps(self, scope, job_id):
        with self._transaction(write=False) as (db, _):
            self._job(db, scope, job_id)
            return tuple(self._step_model(db, row) for row in db.execute(
                'SELECT * FROM job_steps WHERE job_id=? ORDER BY rowid', (str(job_id),)))

    def attempts(self, scope, job_id, step_id):
        with self._transaction(write=False) as (db, _):
            self._job(db, scope, job_id)
            self._step(db, job_id, step_id)
            return tuple(Attempt(**{k: r[k] for k in Attempt.model_fields}) for r in db.execute(
                'SELECT * FROM step_attempts WHERE step_id=? ORDER BY number', (str(step_id),)))

    def _check_lease(self, db, lease, now, *, settling=False):
        job = self._job(db, lease.scope, lease.job_id)
        row = self._step(db, lease.job_id, lease.step_id)
        if row['fence'] != lease.fence or row['lease_owner'] != lease.owner:
            raise JobError('stale_fence')
        if row['state'] != 'RUNNING':
            raise JobError('invalid_transition')
        if not settling:
            if job['cancel_requested']:
                raise JobError('cancelled')
            if job['state'] in TERMINAL:
                raise JobError('invalid_transition')
            if row['lease_expires_at'] <= now:
                raise JobError('lease_expired')
        return job, row

    def claim(self, scope, job_id, step_id, owner):
        # Validate worker token without exposing validation input.
        try:
            Lease(scope=scope, job_id=job_id, step_id=step_id, owner=owner, fence=1)
        except ValidationError:
            raise JobError('invalid_configuration') from None
        with self._transaction() as (db, now):
            job = self._job(db, scope, job_id)
            row = self._step(db, job_id, step_id)
            if job['cancel_requested'] or job['state'] in TERMINAL:
                return None
            if row['state'] == 'RUNNING' and row['lease_expires_at'] <= now:
                self._failure(db, job, row, Failure(category='worker_interrupted', classification='RETRYABLE'), now)
                row = self._step(db, job_id, step_id)
            if row['state'] not in ('READY', 'RETRY_WAIT') or row['not_before'] > now:
                return None
            policy = Admission.model_validate_json(job['request']).profile.retry
            if row['started_at'] and time_of(now) >= time_of(row['started_at']) + timedelta(seconds=policy.budget_seconds):
                self._terminal_failure(db, row, Failure(category='retry_exhausted', classification='NON_RETRYABLE'), now)
                self._refresh(db, str(job_id), now)
                return None
            number, fence = row['attempt_count'] + 1, row['fence'] + 1
            expires = stamp(time_of(now) + timedelta(seconds=self.settings.lease_seconds))
            db.execute("""UPDATE job_steps SET state='RUNNING',attempt_count=?,fence=?,lease_owner=?,
                lease_expires_at=?,started_at=COALESCE(started_at,?),failure_category=NULL WHERE step_id=?""",
                       (number, fence, owner, expires, now, str(step_id)))
            db.execute('''INSERT INTO step_attempts(step_id,number,worker,fence,started_at,outcome)
                VALUES(?,?,?,?,?,?)''', (str(step_id), number, owner, fence, now, 'RUNNING'))
            self._refresh(db, str(job_id), now)
            return Lease(scope=scope, job_id=job_id, step_id=step_id, owner=owner, fence=fence)

    def renew(self, lease):
        with self._transaction() as (db, now):
            self._check_lease(db, lease, now)
            db.execute('UPDATE job_steps SET lease_expires_at=? WHERE step_id=?',
                       (stamp(time_of(now) + timedelta(seconds=self.settings.lease_seconds)), str(lease.step_id)))

    def commit(self, lease, manifest):
        try:
            refs = tuple(ObjectRef.model_validate(ref.model_dump(mode='json')) for ref in manifest)
            if (not 1 <= len(refs) <= 1000 or len({r.key for r in refs}) != len(refs)
                    or any(r.scope != lease.scope or r.kind != 'artifact' for r in refs)):
                raise ValueError()
            encoded = canonical([r.model_dump(mode='json') for r in refs])
        except Exception:
            raise JobError('manifest_conflict') from None
        with self._transaction() as (db, now):
            job = self._job(db, lease.scope, lease.job_id)
            row = self._step(db, lease.job_id, lease.step_id)
            if row['state'] == 'SUCCEEDED':
                prior = db.execute('SELECT * FROM artifact_manifests WHERE step_id=?', (str(lease.step_id),)).fetchone()
                attempt = db.execute('SELECT worker FROM step_attempts WHERE step_id=? AND fence=?',
                                     (str(lease.step_id), lease.fence)).fetchone()
                if prior['fence'] != lease.fence or not attempt or attempt[0] != lease.owner:
                    raise JobError('stale_fence')
                if prior['manifest'] != encoded:
                    raise JobError('manifest_conflict')
                return self._step_model(db, row)
            self._check_lease(db, lease, now)
            for ref in refs:
                intent = db.execute('SELECT ref FROM object_intents WHERE step_id=? AND object_key=?',
                                    (str(lease.step_id), str(ref.key))).fetchone()
                if not intent or ObjectRef.model_validate_json(intent[0]) != ref:
                    raise JobError('manifest_conflict')
            db.execute('INSERT INTO artifact_manifests VALUES(?,?,?,?)', (str(lease.step_id), encoded, now, lease.fence))
            for ref in refs:
                db.execute('INSERT INTO manifest_objects VALUES(?,?)', (str(lease.step_id), str(ref.key)))
            db.execute("""UPDATE job_steps SET state='SUCCEEDED',finished_at=?,lease_owner=NULL,
                lease_expires_at=NULL WHERE step_id=?""", (now, str(lease.step_id)))
            db.execute("UPDATE step_attempts SET outcome='SUCCEEDED',finished_at=? WHERE step_id=? AND fence=?",
                       (now, str(lease.step_id), lease.fence))
            self._activate(db, job, now)
            self._refresh(db, str(lease.job_id), now)
            return self._step_model(db, self._step(db, lease.job_id, lease.step_id))

    def _terminal_failure(self, db, row, failure, now):
        db.execute("""UPDATE job_steps SET state='FAILED',finished_at=?,failure_category=?,
            lease_owner=NULL,lease_expires_at=NULL WHERE step_id=?""", (now, failure.category, row['step_id']))
        db.execute('INSERT OR IGNORE INTO dead_letters VALUES(?,?,?,?)',
                   (row['step_id'], failure.category, failure.classification, now))
        db.execute("UPDATE jobs SET state='FAILED',terminal_category=? WHERE job_id=?",
                   (failure.category, row['job_id']))
        others = list(db.execute("SELECT * FROM job_steps WHERE job_id=? AND state IN ('PENDING','READY','RETRY_WAIT','RUNNING')",
                                 (row['job_id'],)))
        for other in others:
            self._cancel_step(db, other, now)

    def _failure(self, db, job, row, failure, now):
        policy = Admission.model_validate_json(job['request']).profile.retry
        delay = max(policy.delay(row['step_key'], max(row['attempt_count'], 1)), failure.retry_after or 0)
        retry_at = stamp(time_of(now) + timedelta(seconds=delay))
        deadline = stamp(time_of(row['started_at']) + timedelta(seconds=policy.budget_seconds))
        retry = (failure.classification == 'RETRYABLE' and row['attempt_count'] < policy.max_attempts
                 and retry_at < deadline)
        category = failure.category if retry or failure.classification != 'RETRYABLE' else 'retry_exhausted'
        db.execute('''UPDATE step_attempts SET outcome=?,finished_at=?,category=?,classification=?,not_before=?
            WHERE step_id=? AND fence=?''', ('RETRY_WAIT' if retry else 'FAILED', now, failure.category,
                                            failure.classification, retry_at if retry else None, row['step_id'], row['fence']))
        if retry:
            db.execute("""UPDATE job_steps SET state='RETRY_WAIT',not_before=?,failure_category=?,
                lease_owner=NULL,lease_expires_at=NULL WHERE step_id=?""", (retry_at, category, row['step_id']))
            self._enqueue(db, row['step_id'], now, retry_at)
        else:
            self._terminal_failure(db, row, Failure(category=category, classification=failure.classification), now)
        self._refresh(db, row['job_id'], now)

    def fail(self, lease, failure):
        failure = failure.sanitized()
        with self._transaction() as (db, now):
            job, row = self._check_lease(db, lease, now)
            if failure.classification == 'CANCELLED':
                self._cancel_job(db, job, now)
                self._cancel_step(db, row, now)
                self._refresh(db, row['job_id'], now)
            else:
                self._failure(db, job, row, failure, now)

    @staticmethod
    def _cancel_step(db, row, now):
        db.execute("""UPDATE job_steps SET state='CANCELLED',finished_at=?,failure_category='cancelled',
            lease_owner=NULL,lease_expires_at=NULL WHERE step_id=?""", (now, row['step_id']))
        db.execute("""UPDATE step_attempts SET outcome='CANCELLED',finished_at=?,category='cancelled',
            classification='CANCELLED' WHERE step_id=? AND outcome='RUNNING'""", (now, row['step_id']))

    def cancel(self, scope, job_id):
        with self._transaction() as (db, now):
            job = self._job(db, scope, job_id)
            if job['state'] in TERMINAL:
                return self._job_model(job)
            self._cancel_job(db, job, now)
            self._refresh(db, str(job_id), now)
            return self._job_model(self._job(db, scope, job_id))

    def _cancel_job(self, db, job, now):
        db.execute("UPDATE jobs SET cancel_requested=1,state='CANCEL_REQUESTED' WHERE job_id=?", (job['job_id'],))
        for row in list(db.execute("SELECT * FROM job_steps WHERE job_id=? AND state IN ('PENDING','READY','RETRY_WAIT')", (job['job_id'],))):
            self._cancel_step(db, row, now)

    def settle_cancel(self, lease):
        with self._transaction() as (db, now):
            job, row = self._check_lease(db, lease, now, settling=True)
            if not job['cancel_requested']:
                raise JobError('invalid_transition')
            self._cancel_step(db, row, now)
            self._refresh(db, str(lease.job_id), now)

    def register_object(self, lease, ref):
        try:
            ref = ObjectRef.model_validate(ref.model_dump(mode='json'))
        except Exception:
            raise JobError('manifest_conflict') from None
        if ref.scope != lease.scope:
            raise JobError('scope_mismatch')
        with self._transaction() as (db, now):
            self._check_lease(db, lease, now)
            existing = db.execute('SELECT ref FROM object_intents WHERE step_id=? AND object_key=?',
                                  (str(lease.step_id), str(ref.key))).fetchone()
            encoded = ref.model_dump_json()
            if existing and existing[0] != encoded:
                raise JobError('manifest_conflict')
            db.execute('INSERT OR IGNORE INTO object_intents VALUES(?,?,?,?)',
                       (str(lease.step_id), str(ref.key), encoded, now))

    def pending_dispatch(self, limit=100):
        with self._transaction(write=False) as (db, now):
            rows = db.execute('''SELECT o.dispatch_id,s.step_id,j.job_id,j.request FROM outbox o
                JOIN job_steps s ON s.step_id=o.step_id JOIN jobs j ON j.job_id=s.job_id
                WHERE o.delivered_at IS NULL AND o.available_at<=? AND j.cancel_requested=0
                AND s.state IN ('READY','RETRY_WAIT') AND s.not_before<=? AND j.state NOT IN ('COMPLETED','FAILED','CANCELLED','PARTIAL')
                ORDER BY o.dispatch_id LIMIT ?''', (now, now, bounded(limit)))
            return tuple(Dispatch(dispatch_id=r['dispatch_id'], scope=Admission.model_validate_json(r['request']).scope,
                                  job_id=r['job_id'], step_id=r['step_id']) for r in rows)

    def mark_delivered(self, dispatch):
        with self._transaction() as (db, now):
            self._job(db, dispatch.scope, dispatch.job_id)
            self._step(db, dispatch.job_id, dispatch.step_id)
            changed = db.execute('UPDATE outbox SET delivered_at=COALESCE(delivered_at,?) WHERE dispatch_id=? AND step_id=?',
                                 (now, dispatch.dispatch_id, str(dispatch.step_id))).rowcount
            if not changed:
                raise JobError('dispatch_error')

    def orphan_candidates(self, limit=100):
        with self._transaction(write=False) as (db, now):
            return self._orphans(db, now, bounded(limit))

    def _orphans(self, db, now, limit):
        cutoff = stamp(time_of(now) - timedelta(seconds=self.settings.orphan_grace_seconds))
        rows = db.execute("""SELECT DISTINCT i.ref FROM object_intents i
            JOIN job_steps s ON s.step_id=i.step_id
            WHERE i.created_at<=? AND s.state IN ('SUCCEEDED','FAILED','CANCELLED')
            AND NOT EXISTS(SELECT 1 FROM jobs j WHERE j.source_key=i.object_key)
            AND NOT EXISTS(SELECT 1 FROM manifest_objects m WHERE m.object_key=i.object_key)
            AND NOT EXISTS(SELECT 1 FROM object_intents active JOIN job_steps a ON a.step_id=active.step_id
                WHERE active.object_key=i.object_key AND a.state IN ('PENDING','READY','RUNNING','RETRY_WAIT'))
            ORDER BY i.created_at,i.step_id,i.object_key LIMIT ?""", (cutoff, limit))
        return tuple(ObjectRef.model_validate_json(row[0]) for row in rows)

    def reconcile(self, limit=100):
        limit = bounded(limit)
        with self._transaction() as (db, now):
            expired = dispatch_repairs = terminal_repairs = 0
            rows = list(db.execute("SELECT * FROM job_steps WHERE state='RUNNING' AND lease_expires_at<=? ORDER BY lease_expires_at LIMIT ?", (now, limit)))
            for row in rows:
                # Earlier failure may have settled sibling rows in this batch.
                row = self._step(db, row['job_id'], row['step_id'])
                if row['state'] != 'RUNNING':
                    continue
                job = db.execute('SELECT * FROM jobs WHERE job_id=?', (row['job_id'],)).fetchone()
                if job['cancel_requested'] or job['state'] in TERMINAL:
                    self._cancel_step(db, row, now)
                    self._refresh(db, row['job_id'], now)
                else:
                    self._failure(db, job, row, Failure(category='worker_interrupted', classification='RETRYABLE'), now)
                expired += 1
            rows = list(db.execute("""SELECT s.* FROM job_steps s JOIN jobs j ON j.job_id=s.job_id
                WHERE j.state IN ('COMPLETED','FAILED','CANCELLED','PARTIAL')
                AND s.state IN ('PENDING','READY','RETRY_WAIT','RUNNING') LIMIT ?""", (limit,)))
            for row in rows:
                self._cancel_step(db, row, now)
                self._refresh(db, row['job_id'], now)
                terminal_repairs += 1
            cutoff = stamp(time_of(now) - timedelta(seconds=self.settings.redelivery_seconds))
            rows = db.execute('''SELECT s.* FROM job_steps s JOIN jobs j ON j.job_id=s.job_id
                WHERE s.state IN ('READY','RETRY_WAIT') AND s.not_before<=? AND j.cancel_requested=0
                AND j.state NOT IN ('COMPLETED','FAILED','CANCELLED','PARTIAL')
                AND NOT EXISTS(SELECT 1 FROM outbox o WHERE o.step_id=s.step_id
                    AND (o.delivered_at IS NULL OR o.delivered_at>?)) LIMIT ?''', (now, cutoff, limit)).fetchall()
            for row in rows:
                self._enqueue(db, row['step_id'], now, now)
                dispatch_repairs += 1
            count = db.execute("""SELECT COUNT(*) FROM outbox o JOIN job_steps s ON s.step_id=o.step_id
                JOIN jobs j ON j.job_id=s.job_id WHERE o.delivered_at IS NULL
                AND s.state IN ('READY','RETRY_WAIT') AND j.cancel_requested=0
                AND j.state NOT IN ('COMPLETED','FAILED','CANCELLED','PARTIAL')""").fetchone()[0]
            return Reconciliation(expired=expired, dispatch_repairs=dispatch_repairs,
                                  terminal_repairs=terminal_repairs, pending_outbox=count,
                                  orphan_candidates=len(self._orphans(db, now, limit)))

    def dead_letters(self, scope, job_id):
        with self._transaction(write=False) as (db, _):
            self._job(db, scope, job_id)
            return tuple(dict(r) for r in db.execute('''SELECT d.* FROM dead_letters d
                JOIN job_steps s ON s.step_id=d.step_id WHERE s.job_id=?''', (str(job_id),)))
