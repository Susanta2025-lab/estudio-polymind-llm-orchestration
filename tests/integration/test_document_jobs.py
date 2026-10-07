"""Actual Phase 17B extraction through durable dispatch, interruption and restart."""

from datetime import datetime, timedelta, timezone
from io import BytesIO
import hashlib
import subprocess
import sys
from uuid import UUID

import pytest
from pypdf import PdfWriter

from documents.errors import DocumentError
from documents.jobs.errors import JobError, classify
from documents.jobs.models import Admission, JobSettings, ProcessingProfile, StepSpec
from documents.jobs.service import DocumentJobs
from documents.jobs.sqlite import SQLiteJobLedger
from documents.jobs.worker import ExtractionHandler, IntentStore, LocalDispatcher, Worker, relay
from documents.models import Scope, stable_id
from documents.parser import PARSER_VERSION
from documents.serialization import deserialize
from documents.storage import LocalObjectStore

SCOPE = Scope(tenant=UUID(int=100), owner=UUID(int=200))


class ControlledClock:
    def __init__(self):
        self.value = datetime(2026, 10, 7, tzinfo=timezone.utc)

    def now(self):
        return self.value

    def advance(self, seconds):
        self.value += timedelta(seconds=seconds)


@pytest.fixture
def setup(tmp_path):
    def create(data=b'Synthetic alpha\nSynthetic beta', *, mime='text/plain', profile=None, steps=None):
        clock = ControlledClock()
        settings = JobSettings(database_path=tmp_path / 'jobs.sqlite', lease_seconds=10,
                               orphan_grace_seconds=20, redelivery_seconds=5)
        store = LocalObjectStore(tmp_path / 'objects')
        document = UUID(int=300)
        version = stable_id(SCOPE.identity(), str(document), hashlib.sha256(data).hexdigest())
        source = store.put(SCOPE, 'source', version, BytesIO(data), max_bytes=100000)
        request = Admission(scope=SCOPE, document_id=document, document_version_id=version, source=source,
                            request_idempotency_key='integration', mime=mime,
                            display_filename='synthetic.pdf' if mime == 'application/pdf' else 'synthetic.txt',
                            profile=profile or ProcessingProfile(parser_version=PARSER_VERSION if mime == 'application/pdf' else 'utf8-strict/1'),
                            steps=steps or (StepSpec(),))
        ledger = SQLiteJobLedger(settings, clock)
        service = DocumentJobs(ledger, store)
        job = service.admit(request)
        return clock, settings, store, ledger, service, job
    return create


def test_real_text_extraction_and_fresh_process_read(setup):
    clock, settings, store, ledger, service, job = setup()
    queue = LocalDispatcher()
    assert relay(ledger, queue) == 1
    assert Worker(ledger, queue, store, ExtractionHandler(), owner='extractor').once()
    step = ledger.steps(SCOPE, job.job_id)[0]
    artifact = deserialize(store.read(SCOPE, step.manifest[0], max_bytes=100000))
    assert artifact.units[0].text == 'Synthetic alpha\nSynthetic beta'
    assert artifact.extracted_at == step.execution_at
    assert artifact.document.created_at == job.document_created_at
    assert ledger.get_job(SCOPE, job.job_id).state == 'COMPLETED'
    # A fresh interpreter (not merely another Python object) sees the result.
    script = '''
from pathlib import Path
import sys
from uuid import UUID
from documents.jobs.sqlite import SQLiteJobLedger
from documents.jobs.models import JobSettings
from documents.models import Scope
ledger=SQLiteJobLedger(JobSettings(database_path=Path(sys.argv[1])))
scope=Scope(tenant=UUID(int=100), owner=UUID(int=200))
job=ledger.get_job(scope, UUID(sys.argv[2]))
assert job.state == 'COMPLETED'
print(ledger.steps(scope,job.job_id)[0].manifest[0].sha256)
'''
    result = subprocess.run([sys.executable, '-c', script, str(settings.database_path), str(job.job_id)],
                            capture_output=True, text=True, timeout=20, check=True)
    assert result.stdout.strip() == step.manifest[0].sha256
    assert service.admit(job.admission).job_id == job.job_id


def test_real_pdf_extraction(setup):
    writer = PdfWriter()
    writer.add_blank_page(width=300, height=400)
    writer.add_blank_page(width=300, height=400)
    stream = BytesIO(); writer.write(stream)
    _, _, store, ledger, _, job = setup(stream.getvalue(), mime='application/pdf')
    queue = LocalDispatcher(); relay(ledger, queue)
    Worker(ledger, queue, store, ExtractionHandler(), owner='pdf').once()
    step = ledger.steps(SCOPE, job.job_id)[0]
    artifact = deserialize(store.read(SCOPE, step.manifest[0], max_bytes=100000))
    assert [u.physical_page for u in artifact.units] == [1, 2]
    assert artifact.parser_version == PARSER_VERSION


def test_real_extraction_retry_after_object_write_reuses_exact_identity(setup):
    clock, settings, store, ledger, _, job = setup()
    step = ledger.steps(SCOPE, job.job_id)[0]
    lease = ledger.claim(SCOPE, job.job_id, step.step_id, 'crashed')
    handler = ExtractionHandler()
    produced = handler(job, step, IntentStore(store, ledger, lease))
    # No manifest commit: object bytes survive a process interruption.
    original_bytes = store.read(SCOPE, produced[0], max_bytes=100000)
    clock.advance(10)
    ledger = SQLiteJobLedger(settings, clock)
    assert ledger.reconcile().expired == 1
    clock.advance(1)
    queue = LocalDispatcher(); relay(ledger, queue)
    Worker(ledger, queue, store, handler, owner='resumed').once()
    resumed = ledger.steps(SCOPE, job.job_id)[0]
    assert resumed.manifest == produced and resumed.execution_at == step.execution_at
    assert store.read(SCOPE, produced[0], max_bytes=100000) == original_bytes
    assert resumed.attempt_count == 2 and resumed.step_key == step.step_key
    with pytest.raises(JobError, match='stale_fence'):
        ledger.commit(lease, produced)
    clock.advance(100)
    assert ledger.orphan_candidates() == ()


def test_changed_profile_creates_distinct_real_artifact_even_same_clock(setup):
    _, _, store, ledger, service, job = setup()
    queue = LocalDispatcher(); relay(ledger, queue)
    Worker(ledger, queue, store, ExtractionHandler(), owner='first').once()
    original = ledger.steps(SCOPE, job.job_id)[0]
    request = job.admission.model_copy(update={
        'request_idempotency_key': 'reprocess', 'resume_from': job.job_id,
        'profile': ProcessingProfile(version='local-extraction/2'),
    })
    new = service.admit(request)
    relay(ledger, queue)
    Worker(ledger, queue, store, ExtractionHandler(), owner='new').once()
    changed = ledger.steps(SCOPE, new.job_id)[0]
    assert changed.manifest[0].object_id != original.manifest[0].object_id
    assert changed.execution_at > original.execution_at
    assert changed.step_key != original.step_key


def test_real_transient_storage_failure_then_restart(setup):
    clock, settings, store, ledger, _, job = setup()
    class TransientStore:
        def inspect(self, *args, **kwargs):
            return store.inspect(*args, **kwargs)
        def read(self, *args, **kwargs):
            raise DocumentError('storage_error')
    queue = LocalDispatcher(); relay(ledger, queue)
    Worker(ledger, queue, TransientStore(), ExtractionHandler(), owner='first',
           classifier=lambda error: classify(error, transient_storage=True)).once()
    first = ledger.steps(SCOPE, job.job_id)[0]
    assert first.state == 'RETRY_WAIT'
    clock.advance(1)
    ledger = SQLiteJobLedger(settings, clock)
    queue = LocalDispatcher(); relay(ledger, queue)
    Worker(ledger, queue, store, ExtractionHandler(), owner='second').once()
    assert ledger.get_job(SCOPE, job.job_id).state == 'COMPLETED'
    assert ledger.steps(SCOPE, job.job_id)[0].attempt_count == 2


def test_malformed_source_poison_no_redispatch(setup, caplog):
    _, _, store, ledger, _, job = setup(b'%PDF-private malformed document', mime='application/pdf')
    queue = LocalDispatcher(); relay(ledger, queue)
    Worker(ledger, queue, store, ExtractionHandler(), owner='parser').once()
    assert ledger.get_job(SCOPE, job.job_id).state == 'FAILED'
    assert ledger.dead_letters(SCOPE, job.job_id)[0]['category'] == 'invalid_document'
    assert ledger.reconcile().dispatch_repairs == 0
    assert not queue.messages and not ledger.pending_dispatch()
    assert 'private' not in caplog.text


def test_worker_cancellation_after_artifact_write_leaves_orphan(setup):
    clock, settings, store, ledger, _, job = setup()
    produced = []
    def handler(job, step, tracked):
        refs = ExtractionHandler()(job, step, tracked)
        produced.extend(refs)
        ledger.cancel(SCOPE, job.job_id)
        return refs
    queue = LocalDispatcher(); relay(ledger, queue)
    Worker(ledger, queue, store, handler, owner='cancelled').once()
    assert ledger.get_job(SCOPE, job.job_id).state == 'CANCELLED'
    assert ledger.steps(SCOPE, job.job_id)[0].manifest == ()
    clock.advance(20)
    assert SQLiteJobLedger(settings, clock).orphan_candidates() == tuple(produced)
    assert store.inspect(SCOPE, produced[0], max_bytes=100000) == produced[0]  # Retained, never deleted.


def test_commit_before_lost_worker_ack_never_reexecutes(setup):
    _, _, store, ledger, _, job = setup()
    class LostAck(LocalDispatcher):
        def acknowledge(self, message):
            raise RuntimeError('private queue diagnostics')
    queue = LostAck(); relay(ledger, queue)
    with pytest.raises(JobError, match='^dispatch_error$'):
        Worker(ledger, queue, store, ExtractionHandler(), owner='first').once()
    assert ledger.get_job(SCOPE, job.job_id).state == 'COMPLETED'
    replacement = LocalDispatcher(); replacement.send(queue.receive())
    def forbidden(*args):
        pytest.fail('committed work was reexecuted')
    Worker(ledger, replacement, store, forbidden, owner='redelivered').once()
    assert ledger.steps(SCOPE, job.job_id)[0].attempt_count == 1


def test_worker_crash_after_lease_before_handler_returns(setup):
    clock, settings, store, ledger, _, job = setup()
    def crash(*args):
        raise SystemExit('simulated process termination')
    queue = LocalDispatcher(); relay(ledger, queue)
    with pytest.raises(SystemExit):
        Worker(ledger, queue, store, crash, owner='crashed').once()
    assert ledger.steps(SCOPE, job.job_id)[0].state == 'RUNNING'
    clock.advance(10)
    ledger = SQLiteJobLedger(settings, clock)
    ledger.reconcile(); clock.advance(1)
    replacement = LocalDispatcher(); relay(ledger, replacement)
    Worker(ledger, replacement, store, ExtractionHandler(), owner='recovered').once()
    assert ledger.get_job(SCOPE, job.job_id).state == 'COMPLETED'


def test_outbox_delivery_failure_retains_record(setup):
    _, _, _, ledger, _, _ = setup()
    class Broken(LocalDispatcher):
        def send(self, message):
            raise RuntimeError('private dispatch endpoint')
    with pytest.raises(JobError, match='^dispatch_error$'):
        relay(ledger, Broken())
    assert len(ledger.pending_dispatch()) == 1


def test_resume_later_failure_does_not_call_extraction_again(setup):
    plan = (StepSpec(), StepSpec(unit_id='check', stage='VALIDATING', depends_on=('document',)))
    _, _, store, ledger, service, job = setup(steps=plan)
    queue = LocalDispatcher(); relay(ledger, queue)
    Worker(ledger, queue, store, ExtractionHandler(), owner='extract').once()
    relay(ledger, queue)
    def fail_later(*args):
        raise RuntimeError('synthetic later-stage failure')
    Worker(ledger, queue, store, fail_later, owner='later').once()
    old = ledger.steps(SCOPE, job.job_id)[0]
    resumed = service.admit(job.admission.model_copy(update={'request_idempotency_key': 'resume', 'resume_from': job.job_id}))
    assert ledger.steps(SCOPE, resumed.job_id)[0].manifest == old.manifest
    delivered = ledger.pending_dispatch()
    assert len(delivered) == 1
    assert delivered[0].step_id == ledger.steps(SCOPE, resumed.job_id)[1].step_id


def test_service_verifies_objects_and_scope(setup):
    _, _, store, ledger, service, job = setup()
    other = Scope(tenant=UUID(int=999), owner=SCOPE.owner)
    with pytest.raises(JobError, match='job_not_found'):
        service.get(other, job.job_id)
    with pytest.raises(JobError, match='job_not_found'):
        service.cancel(other, job.job_id)
    with pytest.raises(JobError, match='invalid_configuration'):
        service.admit(job.admission.model_copy(update={'scope': other}))
    (store.root / str(job.admission.source.key)).write_bytes(b'corrupt')
    with pytest.raises(DocumentError, match='integrity_error'):
        service.admit(job.admission.model_copy(update={'request_idempotency_key': 'corrupt'}))


def test_handler_parser_version_mismatch_is_terminal(setup):
    _, _, store, ledger, _, job = setup(profile=ProcessingProfile(parser_version='not-installed/1'))
    queue = LocalDispatcher(); relay(ledger, queue)
    Worker(ledger, queue, store, ExtractionHandler(), owner='wrong-version').once()
    assert ledger.get_job(SCOPE, job.job_id).terminal_category == 'profile_mismatch'


def test_persisted_limits_override_changed_environment(setup, monkeypatch):
    _, _, store, ledger, _, job = setup()
    monkeypatch.setenv('DOCUMENT_MAX_CHARACTERS', '1')
    monkeypatch.setenv('DOCUMENT_MAX_SOURCE_BYTES', '1')
    queue = LocalDispatcher(); relay(ledger, queue)
    Worker(ledger, queue, store, ExtractionHandler(), owner='persisted').once()
    assert ledger.get_job(SCOPE, job.job_id).state == 'COMPLETED'


@pytest.mark.parametrize('spec', [StepSpec(schema_version='future/2'), StepSpec(config_fingerprint='1'*64)])
def test_real_handler_rejects_unimplemented_step_profile(setup, spec):
    _, _, store, ledger, _, job = setup(steps=(spec,))
    queue = LocalDispatcher(); relay(ledger, queue)
    Worker(ledger, queue, store, ExtractionHandler(), owner='unsupported').once()
    assert ledger.get_job(SCOPE, job.job_id).terminal_category == 'profile_mismatch'


def test_resume_verifies_checkpoint_bytes_before_acceptance(setup):
    _, _, store, ledger, service, job = setup()
    queue = LocalDispatcher(); relay(ledger, queue)
    Worker(ledger, queue, store, ExtractionHandler(), owner='initial').once()
    ref = ledger.steps(SCOPE, job.job_id)[0].manifest[0]
    (store.root / str(ref.key)).write_bytes(b'corrupted synthetic artifact')
    with pytest.raises(DocumentError, match='integrity_error'):
        service.admit(job.admission.model_copy(update={'request_idempotency_key': 'resume-corrupt', 'resume_from': job.job_id}))
