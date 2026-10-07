"""Transactional contracts use separate SQLite connections and controlled UTC time."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import hashlib
from io import BytesIO
import multiprocessing
from pathlib import Path
import sqlite3
from threading import Barrier
from uuid import UUID

import pytest
from pydantic import ValidationError

from documents.errors import DocumentError
from documents.models import ObjectRef, Scope, stable_id
from documents.jobs.errors import Failure, JobError, classify
from documents.jobs.models import Admission, JobSettings, ProcessingProfile, RetryPolicy, StepSpec
from documents.jobs.sqlite import SQLiteJobLedger
from documents.jobs.worker import IntentStore, LocalDispatcher, relay

SCOPE = Scope(tenant=UUID(int=1), owner=UUID(int=2))
OTHER = Scope(tenant=UUID(int=3), owner=UUID(int=2))
NOW = datetime(2026, 10, 7, tzinfo=timezone.utc)


class Clock:
    def __init__(self):
        self.value = NOW

    def now(self):
        return self.value

    def advance(self, seconds):
        self.value += timedelta(seconds=seconds)


def request(scope=SCOPE, key='request-1', **changes):
    document_id = UUID(int=10)
    checksum = hashlib.sha256(b'synthetic').hexdigest()
    version = stable_id(scope.identity(), str(document_id), checksum)
    source = ObjectRef(scope=scope, kind='source', object_id=version,
                       key=stable_id(scope.identity(), 'source', str(version)),
                       sha256=checksum, byte_size=9)
    return Admission(scope=scope, document_id=document_id, document_version_id=version,
                     source=source, request_idempotency_key=key, **changes)


@pytest.fixture
def env(tmp_path):
    clock = Clock()
    settings = JobSettings(database_path=tmp_path / 'jobs.sqlite', lease_seconds=10,
                           redelivery_seconds=5, orphan_grace_seconds=20)
    ledger = SQLiteJobLedger(settings, clock)
    return ledger, clock, settings


def begin(ledger, req=None, owner='worker-a'):
    job = ledger.admit(req or request())
    step = next(s for s in ledger.steps(SCOPE, job.job_id) if s.state == 'READY')
    lease = ledger.claim(SCOPE, job.job_id, step.step_id, owner)
    return job, step, lease


def artifact(ledger, lease, number=20):
    oid = UUID(int=number)
    ref = ObjectRef(scope=lease.scope, kind='artifact', object_id=oid,
                    key=stable_id(lease.scope.identity(), 'artifact', str(oid)),
                    sha256=hashlib.sha256(str(number).encode()).hexdigest(), byte_size=2)
    ledger.register_object(lease, ref)
    return (ref,)


def test_admission_and_restart_idempotency(env):
    ledger, clock, settings = env
    first = ledger.admit(request())
    clock.advance(90)
    second = SQLiteJobLedger(settings, clock).admit(request())
    assert first == second
    assert first.state == 'QUEUED' and first.progress.total == first.progress.pending == 1
    assert len(ledger.pending_dispatch()) == 1
    with pytest.raises(JobError, match='^idempotency_conflict$'):
        ledger.admit(request(display_filename='different.txt'))
    other = ledger.admit(request(scope=OTHER))
    assert other.job_id != first.job_id
    assert other.generation == first.generation == 1


@pytest.mark.parametrize('operation', ['get', 'steps', 'attempts', 'claim', 'cancel', 'dead'])
def test_scope_lookup_is_non_disclosing(env, operation):
    ledger, _, _ = env
    job, step, _ = begin(ledger)
    calls = {
        'get': lambda: ledger.get_job(OTHER, job.job_id),
        'steps': lambda: ledger.steps(OTHER, job.job_id),
        'attempts': lambda: ledger.attempts(OTHER, job.job_id, step.step_id),
        'claim': lambda: ledger.claim(OTHER, job.job_id, step.step_id, 'worker'),
        'cancel': lambda: ledger.cancel(OTHER, job.job_id),
        'dead': lambda: ledger.dead_letters(OTHER, job.job_id),
    }
    with pytest.raises(JobError, match='^job_not_found$'):
        calls[operation]()


def test_admission_revalidates_forged_scope_and_plan(env):
    ledger, _, _ = env
    with pytest.raises(JobError, match='invalid_configuration'):
        ledger.admit(request().model_copy(update={'scope': OTHER}))
    with pytest.raises(ValidationError):
        request(steps=(StepSpec(depends_on=('missing',)),))
    with pytest.raises(ValidationError):
        request(steps=(StepSpec(), StepSpec()))
    with pytest.raises(ValidationError):
        request(steps=())


def test_success_and_conditional_duplicate_commit(env):
    ledger, clock, settings = env
    job, step, lease = begin(ledger)
    refs = artifact(ledger, lease)
    result = ledger.commit(lease, refs)
    clock.advance(100)
    assert ledger.commit(lease, refs) == result
    assert SQLiteJobLedger(settings, clock).steps(SCOPE, job.job_id)[0] == result
    assert ledger.get_job(SCOPE, job.job_id).state == 'COMPLETED'
    assert ledger.get_job(SCOPE, job.job_id).progress.completed == 1
    assert ledger.attempts(SCOPE, job.job_id, step.step_id)[0].outcome == 'SUCCEEDED'
    assert ledger.claim(SCOPE, job.job_id, step.step_id, 'next') is None
    with pytest.raises(JobError, match='manifest_conflict'):
        ledger.commit(lease, (refs[0].model_copy(update={'sha256': '0'*64}),))
    with pytest.raises(JobError, match='stale_fence'):
        ledger.commit(lease.model_copy(update={'owner': 'forged'}), refs)
    assert ledger.cancel(SCOPE, job.job_id).state == 'COMPLETED'


def test_manifest_requires_registered_valid_scoped_artifact(env):
    ledger, _, _ = env
    job, _, lease = begin(ledger)
    with pytest.raises(JobError, match='manifest_conflict'):
        ledger.commit(lease, ())
    with pytest.raises(JobError, match='manifest_conflict'):
        ledger.commit(lease, (job.admission.source,))
    refs = artifact(ledger, lease)
    with pytest.raises(JobError, match='manifest_conflict'):
        ledger.commit(lease, refs + refs)
    with pytest.raises(JobError, match='manifest_conflict'):
        ledger.commit(lease, (refs[0].model_copy(update={'key': UUID(int=9)}),))
    with pytest.raises(JobError, match='manifest_conflict'):
        ledger.register_object(lease, refs[0].model_copy(update={'sha256': '0'*64}))
    assert ledger.steps(SCOPE, job.job_id)[0].state == 'RUNNING'


def test_lease_renewal_expiry_and_fenced_takeover(env):
    ledger, clock, settings = env
    job, step, a = begin(ledger)
    refs = artifact(ledger, a)
    clock.advance(9)
    ledger.renew(a)
    clock.advance(2)
    assert ledger.claim(SCOPE, job.job_id, step.step_id, 'worker-b') is None
    clock.advance(8)
    with pytest.raises(JobError, match='lease_expired'):
        ledger.commit(a, refs)
    with pytest.raises(JobError, match='lease_expired'):
        ledger.renew(a)
    assert ledger.reconcile().expired == 1
    assert ledger.steps(SCOPE, job.job_id)[0].state == 'RETRY_WAIT'
    clock.advance(1)
    b = SQLiteJobLedger(settings, clock).claim(SCOPE, job.job_id, step.step_id, 'worker-b')
    assert b.fence == a.fence + 1
    ledger.commit(b, refs)
    with pytest.raises(JobError, match='stale_fence'):
        ledger.commit(a, refs)
    with pytest.raises(JobError, match='stale_fence'):
        ledger.renew(a)
    attempts = ledger.attempts(SCOPE, job.job_id, step.step_id)
    assert [a.number for a in attempts] == [1, 2]
    assert attempts[0].category == 'worker_interrupted'
    assert attempts[1].outcome == 'SUCCEEDED'


def test_claim_recovers_expired_lease_with_backoff(env):
    ledger, clock, _ = env
    job, step, first = begin(ledger)
    clock.advance(11)
    assert ledger.claim(SCOPE, job.job_id, step.step_id, 'second') is None
    clock.advance(1)
    assert ledger.claim(SCOPE, job.job_id, step.step_id, 'second').fence == first.fence + 1


@pytest.mark.parametrize('terminal_method', ['renew', 'fail', 'settle'])
def test_terminal_steps_cannot_be_retried_or_mutated(env, terminal_method):
    ledger, _, _ = env
    job, _, lease = begin(ledger)
    ledger.fail(lease, Failure(category='invalid_document', classification='NON_RETRYABLE'))
    calls = {'renew': lambda: ledger.renew(lease),
             'fail': lambda: ledger.fail(lease, Failure(category='worker_interrupted', classification='RETRYABLE')),
             'settle': lambda: ledger.settle_cancel(lease)}
    with pytest.raises(JobError):
        calls[terminal_method]()
    assert ledger.get_job(SCOPE, job.job_id).state == 'FAILED'
    assert len(ledger.dead_letters(SCOPE, job.job_id)) == 1


def test_retry_backoff_persists_identity_and_exhausts(env):
    ledger, clock, settings = env
    job, original, lease = begin(ledger)
    for attempt, delay in [(1, 1), (2, 2), (3, None)]:
        ledger.fail(lease, Failure(category='storage_error', classification='RETRYABLE'))
        ledger = SQLiteJobLedger(settings, clock)
        step = ledger.steps(SCOPE, job.job_id)[0]
        assert step.step_key == original.step_key
        assert step.execution_at == original.execution_at
        assert step.attempt_count == attempt
        if delay:
            assert (step.not_before - clock.now()).total_seconds() == delay
            assert ledger.claim(SCOPE, job.job_id, step.step_id, 'retry') is None
            clock.advance(delay)
            lease = ledger.claim(SCOPE, job.job_id, step.step_id, 'retry')
        else:
            assert step.state == 'FAILED' and step.failure_category == 'retry_exhausted'
    assert ledger.get_job(SCOPE, job.job_id).progress.failed == 1
    assert not ledger.pending_dispatch()
    assert ledger.reconcile().dispatch_repairs == 0
    assert ledger.dead_letters(SCOPE, job.job_id)[0]['category'] == 'retry_exhausted'
    assert len(ledger.attempts(SCOPE, job.job_id, step.step_id)) == 3


@pytest.mark.parametrize('budget', [0.5, 1, 5])
def test_total_retry_deadline_is_enforced(env, budget):
    ledger, clock, _ = env
    policy = RetryPolicy(budget_seconds=budget)
    job, step, lease = begin(ledger, request(profile=ProcessingProfile(retry=policy)))
    ledger.fail(lease, Failure(category='worker_interrupted', classification='RETRYABLE'))
    clock.advance(10)
    assert ledger.claim(SCOPE, job.job_id, step.step_id, 'late') is None
    assert ledger.get_job(SCOPE, job.job_id).state == 'FAILED'


def test_deterministic_jitter_and_cap():
    p = RetryPolicy(base_seconds=2, max_seconds=5, jitter_fraction=.2)
    assert p.delay('a', 5) == p.delay('a', 5)
    assert 4 <= p.delay('a', 5) <= 5
    assert 1.6 <= p.delay('a', 1) <= 2
    assert p.delay('a', 5) != p.delay('b', 5)


@pytest.mark.parametrize('error,transient,kind,category', [
    (DocumentError('unsupported_format'), False, 'NON_RETRYABLE', 'unsupported_format'),
    (DocumentError('invalid_document'), False, 'NON_RETRYABLE', 'invalid_document'),
    (DocumentError('encrypted_document'), False, 'NON_RETRYABLE', 'encrypted_document'),
    (DocumentError('source_too_large'), False, 'NON_RETRYABLE', 'source_too_large'),
    (DocumentError('page_limit_exceeded'), False, 'NON_RETRYABLE', 'page_limit_exceeded'),
    (DocumentError('integrity_error'), False, 'NON_RETRYABLE', 'integrity_error'),
    (DocumentError('storage_error'), False, 'NON_RETRYABLE', 'storage_error'),
    (DocumentError('storage_error'), True, 'RETRYABLE', 'storage_error'),
    (RuntimeError('/private/file secret=document'), False, 'NON_RETRYABLE', 'worker_failed'),
    (DocumentError('malicious document'), False, 'NON_RETRYABLE', 'worker_failed'),
    (JobError('cancelled'), False, 'CANCELLED', 'cancelled'),
])
def test_failure_classification(error, transient, kind, category):
    result = classify(error, transient_storage=transient)
    assert result.classification == kind and result.category == category


def test_raw_failure_never_persisted_or_logged(env, caplog):
    ledger, _, settings = env
    job, step, lease = begin(ledger)
    ledger.fail(lease, Failure(category='secret private source /path', classification='NON_RETRYABLE'))
    assert 'secret' not in settings.database_path.read_bytes().decode('utf8', errors='ignore')
    assert not caplog.records
    assert ledger.attempts(SCOPE, job.job_id, step.step_id)[0].category == 'worker_failed'


@pytest.mark.parametrize('leased', [False, True])
def test_cancellation_lifecycle(env, leased):
    ledger, clock, settings = env
    job = ledger.admit(request())
    step = ledger.steps(SCOPE, job.job_id)[0]
    lease = ledger.claim(SCOPE, job.job_id, step.step_id, 'active') if leased else None
    refs = artifact(ledger, lease) if leased else None
    cancelled = ledger.cancel(SCOPE, job.job_id)
    assert cancelled.state == ('CANCEL_REQUESTED' if leased else 'CANCELLED')
    ledger = SQLiteJobLedger(settings, clock)
    assert not ledger.pending_dispatch()
    assert ledger.claim(SCOPE, job.job_id, step.step_id, 'late') is None
    if leased:
        with pytest.raises(JobError, match='cancelled'):
            ledger.commit(lease, refs)
        with pytest.raises(JobError, match='cancelled'):
            ledger.renew(lease)
        ledger.settle_cancel(lease)
    assert ledger.get_job(SCOPE, job.job_id).state == 'CANCELLED'
    assert ledger.get_job(SCOPE, job.job_id).progress.cancelled == 1
    assert ledger.admit(request()).job_id == job.job_id


def test_cancellation_expiry_settles_crashed_worker(env):
    ledger, clock, _ = env
    job, _, _ = begin(ledger)
    ledger.cancel(SCOPE, job.job_id)
    clock.advance(10)
    assert ledger.reconcile().expired == 1
    assert ledger.get_job(SCOPE, job.job_id).state == 'CANCELLED'


def test_stale_cancel_failure_cannot_cancel_new_owner(env):
    ledger, clock, _ = env
    job, step, lease = begin(ledger)
    clock.advance(10)
    ledger.reconcile()
    clock.advance(1)
    newer = ledger.claim(SCOPE, job.job_id, step.step_id, 'newer')
    with pytest.raises(JobError, match='stale_fence'):
        ledger.fail(lease, Failure(category='cancelled', classification='CANCELLED'))
    assert not ledger.get_job(SCOPE, job.job_id).cancel_requested
    assert ledger.steps(SCOPE, job.job_id)[0].fence == newer.fence


def test_worker_initiated_cancellation_is_atomic(env):
    ledger, _, _ = env
    job, _, lease = begin(ledger)
    ledger.fail(lease, Failure(category='cancelled', classification='CANCELLED'))
    assert ledger.get_job(SCOPE, job.job_id).state == 'CANCELLED'


def test_successor_parent_hashes_outbox_and_progress(env):
    ledger, _, _ = env
    plan = (StepSpec(), StepSpec(unit_id='check', stage='VALIDATING', depends_on=('document',)))
    job, root, lease = begin(ledger, request(steps=plan))
    pending = ledger.steps(SCOPE, job.job_id)[1]
    assert pending.state == 'PENDING'
    assert len(ledger.pending_dispatch()) == 0  # Root currently running.
    ledger.commit(lease, artifact(ledger, lease))
    child = ledger.steps(SCOPE, job.job_id)[1]
    assert child.state == 'READY' and child.step_key != pending.step_key
    assert child.input_fingerprint != root.input_fingerprint
    messages = ledger.pending_dispatch()
    assert len(messages) == 1 and messages[0].step_id == child.step_id
    progress = ledger.get_job(SCOPE, job.job_id).progress
    assert progress.total == 2 and progress.completed == 1 and progress.pending == 1


def test_manifest_successor_outbox_rollback_as_one_transaction(env):
    ledger, _, settings = env
    plan = (StepSpec(), StepSpec(unit_id='next', depends_on=('document',)))
    job, step, lease = begin(ledger, request(steps=plan))
    refs = artifact(ledger, lease)
    with sqlite3.connect(settings.database_path) as db:
        db.execute("CREATE TRIGGER inject_failure BEFORE INSERT ON outbox BEGIN SELECT RAISE(ABORT, 'private SQL'); END")
    with pytest.raises(JobError, match='^ledger_error$'):
        ledger.commit(lease, refs)
    states = ledger.steps(SCOPE, job.job_id)
    assert states[0].state == 'RUNNING' and states[0].manifest == ()
    assert states[1].state == 'PENDING'
    assert ledger.attempts(SCOPE, job.job_id, step.step_id)[0].outcome == 'RUNNING'


def test_admission_outbox_failure_leaves_no_job(env):
    ledger, _, settings = env
    with sqlite3.connect(settings.database_path) as db:
        db.execute("CREATE TRIGGER inject_failure BEFORE INSERT ON outbox BEGIN SELECT RAISE(ABORT, 'private SQL'); END")
    with pytest.raises(JobError, match='ledger_error'):
        ledger.admit(request())
    with sqlite3.connect(settings.database_path) as db:
        assert db.execute('SELECT COUNT(*) FROM jobs').fetchone()[0] == 0
        assert db.execute('SELECT COUNT(*) FROM job_steps').fetchone()[0] == 0


def test_outbox_lost_ack_duplicate_and_restart(env):
    ledger, clock, settings = env
    job = ledger.admit(request())
    message = ledger.pending_dispatch()[0]
    queue = LocalDispatcher()
    queue.send(message)  # Crash after send before marking delivered.
    restarted = SQLiteJobLedger(settings, clock)
    assert relay(restarted, queue) == 1
    assert len(queue.messages) == 2
    first = restarted.claim(SCOPE, job.job_id, message.step_id, 'first')
    assert restarted.claim(SCOPE, job.job_id, message.step_id, 'duplicate') is None
    refs = artifact(restarted, first)
    restarted.commit(first, refs)  # Crash before consuming either message.
    for delivered in queue.messages:
        assert restarted.claim(delivered.scope, delivered.job_id, delivered.step_id, 'restart') is None
    assert restarted.steps(SCOPE, job.job_id)[0].attempt_count == 1


def test_lost_in_memory_queue_redispatched_after_restart(env):
    ledger, clock, settings = env
    job = ledger.admit(request())
    relay(ledger, LocalDispatcher())  # Delivered but queue process disappears.
    clock.advance(5)
    ledger = SQLiteJobLedger(settings, clock)
    assert ledger.reconcile().dispatch_repairs == 1
    assert ledger.reconcile().dispatch_repairs == 0
    assert ledger.pending_dispatch()[0].job_id == job.job_id


def test_reconciliation_repairs_missing_dispatch_and_terminal_work(env):
    ledger, _, settings = env
    job = ledger.admit(request())
    with sqlite3.connect(settings.database_path) as db:
        db.execute('DELETE FROM outbox')  # Controlled corruption fixture.
    assert ledger.reconcile().dispatch_repairs == 1
    with sqlite3.connect(settings.database_path) as db:
        db.execute("UPDATE jobs SET state='FAILED'")
    assert ledger.reconcile().terminal_repairs == 1
    assert not ledger.pending_dispatch()
    assert ledger.get_job(SCOPE, job.job_id).progress.cancelled == 1


def test_checkpoint_resume_and_incompatible_profile(env):
    ledger, _, _ = env
    plan = (StepSpec(), StepSpec(unit_id='check', stage='VALIDATING', depends_on=('document',)))
    job, _, lease = begin(ledger, request(steps=plan))
    refs = artifact(ledger, lease)
    ledger.commit(lease, refs)
    second = ledger.steps(SCOPE, job.job_id)[1]
    child = ledger.claim(SCOPE, job.job_id, second.step_id, 'check')
    ledger.fail(child, Failure(category='worker_failed', classification='NON_RETRYABLE'))
    original = ledger.steps(SCOPE, job.job_id)
    resumed = ledger.admit(request(key='resume', steps=plan, resume_from=job.job_id))
    steps = ledger.steps(SCOPE, resumed.job_id)
    assert resumed.generation == job.generation + 1 and resumed.run_id != job.run_id
    assert steps[0].manifest == refs and steps[0].attempt_count == 0
    assert steps[0].reused_from == original[0].step_id
    assert steps[0].execution_at == original[0].execution_at
    assert steps[1].state == 'READY' and steps[1].step_key != original[1].step_key
    changed = ledger.admit(request(key='changed', steps=plan, resume_from=job.job_id,
                                   profile=ProcessingProfile(version='local-extraction/2')))
    new_steps = ledger.steps(SCOPE, changed.job_id)
    assert new_steps[0].state == 'READY' and not new_steps[0].manifest
    assert new_steps[0].execution_at > original[0].execution_at
    assert ledger.get_job(SCOPE, job.job_id).state == 'FAILED'


def test_changed_parent_spec_invalidates_descendant_checkpoints(env):
    ledger, _, _ = env
    plan = (StepSpec(), StepSpec(unit_id='child', depends_on=('document',)))
    job, _, lease = begin(ledger, request(steps=plan))
    ledger.commit(lease, artifact(ledger, lease))
    child = ledger.steps(SCOPE, job.job_id)[1]
    lease = ledger.claim(SCOPE, job.job_id, child.step_id, 'child')
    ledger.commit(lease, artifact(ledger, lease, 21))
    changed_plan = (StepSpec(config_fingerprint='1'*64), plan[1])
    resumed = ledger.admit(request(key='new', steps=changed_plan, resume_from=job.job_id))
    assert [s.state for s in ledger.steps(SCOPE, resumed.job_id)] == ['READY', 'PENDING']


def test_resume_requires_terminal_same_scoped_source(env):
    ledger, _, _ = env
    job = ledger.admit(request())
    with pytest.raises(JobError, match='invalid_transition'):
        ledger.admit(request(key='new', resume_from=job.job_id))
    with pytest.raises(JobError, match='job_not_found'):
        ledger.admit(request(scope=OTHER, key='new', resume_from=job.job_id))


def test_orphan_intent_grace_reference_and_active_protection(env):
    ledger, clock, _ = env
    job, _, lease = begin(ledger)
    accepted = artifact(ledger, lease, 20)
    orphan = artifact(ledger, lease, 21)
    ledger.register_object(lease, job.admission.source)
    ledger.commit(lease, accepted)
    assert ledger.orphan_candidates() == ()
    clock.advance(20)
    assert ledger.orphan_candidates() == orphan
    assert ledger.reconcile().orphan_candidates == 1
    assert ledger.orphan_candidates() == orphan  # No deletion or mutation.
    other_job, _, active = begin(ledger, request(key='new'))
    ledger.register_object(active, orphan[0])
    assert ledger.orphan_candidates() == ()
    ledger.commit(active, orphan)
    assert ledger.orphan_candidates() == ()


def test_orphan_registered_before_crashing_put(env, tmp_path):
    ledger, clock, _ = env
    job, _, lease = begin(ledger)
    class CrashStore:
        def put(self, *args, **kwargs):
            raise SystemExit('simulated termination')
    tracked = IntentStore(CrashStore(), ledger, lease)
    with pytest.raises(SystemExit):
        tracked.put(SCOPE, 'artifact', UUID(int=22), BytesIO(b'out'), max_bytes=10)
    ledger.cancel(SCOPE, job.job_id)
    clock.advance(20)
    ledger.reconcile()
    assert len(ledger.orphan_candidates()) == 1  # Intent may represent absent bytes.


@pytest.mark.parametrize('scenario', ['relative', 'directory', 'symlink', 'ancestor', 'hardlink', 'missing_parent'])
def test_database_path_safety(tmp_path, scenario):
    real = tmp_path / 'real.sqlite'
    real.touch()
    path = real
    if scenario == 'relative':
        path = Path('implicit.sqlite')
    elif scenario == 'directory':
        path = tmp_path
    elif scenario == 'symlink':
        path = tmp_path / 'link'; path.symlink_to(real)
    elif scenario == 'ancestor':
        folder = tmp_path / 'link'; folder.symlink_to(tmp_path, target_is_directory=True)
        path = folder / 'new.sqlite'
    elif scenario == 'hardlink':
        path = tmp_path / 'link'; path.hardlink_to(real)
    else:
        path = tmp_path / 'absent' / 'new.sqlite'
    with pytest.raises(JobError, match='invalid_configuration'):
        SQLiteJobLedger(JobSettings(database_path=path))


@pytest.mark.parametrize('corruption', ['version', 'unknown', 'missing_index', 'raw'])
def test_incompatible_schema_rejected(env, corruption):
    _, clock, settings = env
    if corruption == 'raw':
        settings.database_path.write_bytes(b'private invalid database')
    else:
        with sqlite3.connect(settings.database_path) as db:
            if corruption == 'version':
                db.execute('PRAGMA user_version=99')
            elif corruption == 'unknown':
                db.execute('CREATE TABLE alien(value TEXT)')
            else:
                db.execute('DROP INDEX steps_scheduler')
    with pytest.raises(JobError, match='^(schema_mismatch|ledger_error)$'):
        SQLiteJobLedger(settings, clock)


def test_environment_and_required_explicit_configuration(monkeypatch, tmp_path):
    monkeypatch.delenv('DOCUMENT_JOBS_DATABASE_PATH', raising=False)
    with pytest.raises(ValidationError):
        JobSettings()
    monkeypatch.setenv('DOCUMENT_JOBS_DATABASE_PATH', str(tmp_path / 'jobs.sqlite'))
    assert JobSettings().database_path == tmp_path / 'jobs.sqlite'


def race(functions):
    barrier = Barrier(len(functions))
    def run(fn):
        barrier.wait(timeout=10)
        try:
            return fn()
        except JobError as exc:
            return exc.category
    with ThreadPoolExecutor(max_workers=len(functions)) as pool:
        return list(pool.map(run, functions))


def test_concurrent_admission_returns_one_logical_job(env):
    _, clock, settings = env
    a, b = SQLiteJobLedger(settings, clock), SQLiteJobLedger(settings, clock)
    results = race([lambda: a.admit(request()), lambda: b.admit(request())])
    assert results[0] == results[1]
    assert len(a.pending_dispatch()) == 1


def test_concurrent_conflicting_admission_rejected(env):
    ledger, _, _ = env
    results = race([lambda: ledger.admit(request()), lambda: ledger.admit(request(display_filename='changed.txt'))])
    assert sum(r == 'idempotency_conflict' for r in results) == 1


def test_concurrent_claim_and_completion(env):
    ledger, clock, settings = env
    other = SQLiteJobLedger(settings, clock)
    job = ledger.admit(request())
    step = ledger.steps(SCOPE, job.job_id)[0]
    leases = race([lambda: ledger.claim(SCOPE, job.job_id, step.step_id, 'one'),
                   lambda: other.claim(SCOPE, job.job_id, step.step_id, 'two')])
    assert sum(lease is not None for lease in leases) == 1
    lease = next(lease for lease in leases if lease is not None)
    refs = artifact(ledger, lease)
    results = race([lambda: ledger.commit(lease, refs), lambda: other.commit(lease, refs)])
    assert all(result.state == 'SUCCEEDED' for result in results)
    assert len(ledger.attempts(SCOPE, job.job_id, step.step_id)) == 1


def test_cancellation_commit_race_serializes(env):
    ledger, clock, settings = env
    other = SQLiteJobLedger(settings, clock)
    job, _, lease = begin(ledger)
    refs = artifact(ledger, lease)
    results = race([lambda: ledger.commit(lease, refs), lambda: other.cancel(SCOPE, job.job_id)])
    job = ledger.get_job(SCOPE, job.job_id)
    if job.state == 'COMPLETED':
        assert results[0].state == 'SUCCEEDED'
    else:
        assert job.state == 'CANCEL_REQUESTED' and results[0] == 'cancelled'
        assert not ledger.steps(SCOPE, job.job_id)[0].manifest


def test_expired_renewal_takeover_race(env):
    ledger, clock, settings = env
    job, step, lease = begin(ledger)
    clock.advance(10)
    other = SQLiteJobLedger(settings, clock)
    results = race([lambda: ledger.renew(lease), lambda: other.claim(SCOPE, job.job_id, step.step_id, 'new')])
    assert results[0] in ('lease_expired', 'stale_fence')
    assert results[1] is None
    clock.advance(1)
    assert other.claim(SCOPE, job.job_id, step.step_id, 'new').fence == 2


def process_admit(path, barrier, output):
    ledger = SQLiteJobLedger(JobSettings(database_path=Path(path)), Clock())
    barrier.wait(timeout=10)
    output.put(str(ledger.admit(request()).job_id))


def test_separate_process_admission_sqlite_authority(env):
    _, _, settings = env
    ctx = multiprocessing.get_context('fork')
    barrier, output = ctx.Barrier(2), ctx.Queue()
    processes = [ctx.Process(target=process_admit, args=(str(settings.database_path), barrier, output)) for _ in range(2)]
    for process in processes:
        process.start()
    results = [output.get(timeout=10) for _ in processes]
    for process in processes:
        process.join(timeout=10)
        assert process.exitcode == 0
    assert results[0] == results[1]
    output.close()


def test_pending_step_cannot_be_claimed_and_settle_requires_cancellation(env):
    ledger, _, _ = env
    plan = (StepSpec(), StepSpec(unit_id='later', depends_on=('document',)))
    job, _, lease = begin(ledger, request(steps=plan))
    pending = ledger.steps(SCOPE, job.job_id)[1]
    assert ledger.claim(SCOPE, job.job_id, pending.step_id, 'early') is None
    with pytest.raises(JobError, match='invalid_transition'):
        ledger.settle_cancel(lease)


def test_cancellation_waits_for_all_active_leases_and_preserves_checkpoints(env):
    ledger, clock, _ = env
    plan = (StepSpec(unit_id='a'), StepSpec(unit_id='b'), StepSpec(unit_id='c'))
    job = ledger.admit(request(steps=plan))
    a, b, c = [ledger.claim(SCOPE, job.job_id, s.step_id, s.spec.unit_id) for s in ledger.steps(SCOPE, job.job_id)]
    ledger.commit(a, artifact(ledger, a))
    ledger.cancel(SCOPE, job.job_id)
    ledger.settle_cancel(b)
    assert ledger.get_job(SCOPE, job.job_id).state == 'CANCEL_REQUESTED'
    clock.advance(10)
    ledger.reconcile()
    progress = ledger.get_job(SCOPE, job.job_id).progress
    assert progress.completed == 1 and progress.cancelled == 2
    assert ledger.get_job(SCOPE, job.job_id).state == 'CANCELLED'


def test_sibling_failure_fences_running_workers(env):
    ledger, _, _ = env
    job = ledger.admit(request(steps=(StepSpec(unit_id='a'), StepSpec(unit_id='b'))))
    steps = ledger.steps(SCOPE, job.job_id)
    a, b = [ledger.claim(SCOPE, job.job_id, s.step_id, s.spec.unit_id) for s in steps]
    refs = artifact(ledger, b)
    ledger.fail(a, Failure(category='invalid_document', classification='NON_RETRYABLE'))
    with pytest.raises(JobError, match='stale_fence'):
        ledger.commit(b, refs)
    assert ledger.get_job(SCOPE, job.job_id).state == 'FAILED'
    assert [s.state for s in ledger.steps(SCOPE, job.job_id)] == ['FAILED', 'CANCELLED']


def test_poison_interruption_exhaustion_and_reconcile_batch_limit(env):
    ledger, clock, _ = env
    policy = ProcessingProfile(retry=RetryPolicy(max_attempts=1))
    for i in range(3):
        begin(ledger, request(key=f'job-{i}', profile=policy))
    clock.advance(10)
    assert ledger.reconcile(limit=1).expired == 1
    assert ledger.reconcile(limit=1).expired == 1
    assert ledger.reconcile(limit=1).expired == 1
    assert ledger.reconcile(limit=1).expired == 0
    assert not ledger.pending_dispatch()


def test_two_conflicting_commits_accept_only_one_manifest(env):
    ledger, clock, settings = env
    other = SQLiteJobLedger(settings, clock)
    job, _, lease = begin(ledger)
    one, two = artifact(ledger, lease, 20), artifact(ledger, lease, 21)
    results = race([lambda: ledger.commit(lease, one), lambda: other.commit(lease, two)])
    assert sum(r == 'manifest_conflict' for r in results) == 1
    assert ledger.steps(SCOPE, job.job_id)[0].manifest in (one, two)


def test_retry_outbox_does_not_deliver_old_message_early(env):
    ledger, clock, _ = env
    _, _, lease = begin(ledger)
    ledger.fail(lease, Failure(category='worker_interrupted', classification='RETRYABLE'))
    assert not ledger.pending_dispatch()
    clock.advance(1)
    assert ledger.pending_dispatch()


def test_same_profile_completed_resume_reuses_all_work(env):
    ledger, _, _ = env
    job, _, lease = begin(ledger)
    refs = artifact(ledger, lease)
    ledger.commit(lease, refs)
    resumed = ledger.admit(request(key='resume-all', resume_from=job.job_id))
    assert resumed.state == 'COMPLETED'
    assert ledger.steps(SCOPE, resumed.job_id)[0].manifest == refs
    assert not ledger.pending_dispatch()


def test_unregistered_manifest_rejected(env):
    ledger, _, _ = env
    job, _, lease = begin(ledger)
    oid = UUID(int=40)
    ref = ObjectRef(scope=SCOPE, kind='artifact', object_id=oid,
                    key=stable_id(SCOPE.identity(), 'artifact', str(oid)), sha256='a'*64, byte_size=1)
    with pytest.raises(JobError, match='manifest_conflict'):
        ledger.commit(lease, (ref,))
    assert ledger.steps(SCOPE, job.job_id)[0].state == 'RUNNING'


def test_clock_requires_aware_utc_and_normalizes_offset(env):
    ledger, clock, _ = env
    clock.value = NOW.astimezone(timezone(timedelta(hours=3)))
    assert ledger.admit(request()).created_at == NOW
    clock.value = datetime(2026, 1, 1)
    with pytest.raises(JobError, match='invalid_configuration'):
        ledger.admit(request(key='naive'))


@pytest.mark.parametrize('field,value', [('fence', 999), ('owner', 'forged')])
def test_forged_active_lease_cannot_commit(env, field, value):
    ledger, _, _ = env
    _, _, lease = begin(ledger)
    refs = artifact(ledger, lease)
    with pytest.raises(JobError, match='stale_fence'):
        ledger.commit(lease.model_copy(update={field: value}), refs)


def test_sqlite_state_and_lease_constraints(env):
    ledger, _, settings = env
    ledger.admit(request())
    for statement in ["UPDATE job_steps SET state='UNKNOWN'", "UPDATE job_steps SET state='RUNNING'",
                      "UPDATE jobs SET generation=0", "UPDATE job_steps SET fence=-1"]:
        with sqlite3.connect(settings.database_path) as db:
            with pytest.raises(sqlite3.IntegrityError):
                db.execute(statement)


def test_profile_fingerprint_is_deterministic_and_semantic():
    original = ProcessingProfile()
    assert original.digest() == ProcessingProfile.model_validate_json(original.model_dump_json()).digest()
    assert original.digest() != ProcessingProfile(max_pages=1).digest()
    assert request().compatibility() != request(profile=ProcessingProfile(max_pages=1)).compatibility()
