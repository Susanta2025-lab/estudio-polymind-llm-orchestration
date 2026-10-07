"""17B -> 17C -> 17D locally, including durable reopen and failure/resume."""

from datetime import datetime, timedelta, timezone
from io import BytesIO
import sqlite3
from uuid import UUID

import pytest
from pypdf import PdfWriter
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject

from documents.config import ExtractionSettings
from documents.extraction import extract
from documents.jobs.errors import JobError
from documents.jobs.models import JobSettings, RetryPolicy
from documents.jobs.sqlite import SQLiteJobLedger
from documents.jobs.worker import IntentStore, LocalDispatcher, Worker, relay
from documents.models import Scope
from documents.parser import ParsedPage
from documents.provenance import resolve
from documents.serialization import deserialize
from documents.storage import LocalObjectStore
from documents.digestion.codec import read
from documents.digestion.inference import FakeInference
from documents.digestion.models import Checkpoint, DigestionError, DigestionProfile, Plan
from documents.digestion.workflow import (
    DigestionHandler, admit, classify_digestion, load_digest, prepare,
)
def profile(**changes):
    values = dict(context_tokens=30000, reserved_output_tokens=3000, template_tokens=64,
                  chunk_characters=100, max_fan_in=4, max_result_characters=3000,
                  max_claims=4, max_claim_characters=256, max_annotations=8,
                  max_source_units=5000, max_chunks=800, max_steps=1000,
                  max_artifact_bytes=16000000, max_depth=32,
                  minimum_coverage=1, max_failed_units=0)
    values.update(changes)
    return DigestionProfile(**values)

SCOPE = Scope(tenant=UUID(int=1), owner=UUID(int=2))


class Clock:
    def __init__(self):
        self.value = datetime(2026,10,7,tzinfo=timezone.utc)
    def now(self):
        return self.value
    def advance(self, seconds):
        self.value += timedelta(seconds=seconds)


def pdf(pages=6):
    writer = PdfWriter()
    for i in range(pages):
        page = writer.add_blank_page(width=300,height=400)
        font = DictionaryObject({NameObject('/Type'):NameObject('/Font'),
                                 NameObject('/Subtype'):NameObject('/Type1'),
                                 NameObject('/BaseFont'):NameObject('/Helvetica')})
        page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'):
            DictionaryObject({NameObject('/F1'):writer._add_object(font)})})
        stream = DecodedStreamObject()
        stream.set_data(f'BT /F1 12 Tf 20 350 Td (Synthetic page {i+1} evidence) Tj ET'.encode())
        page[NameObject('/Contents')] = writer._add_object(stream)
    result=BytesIO(); writer.write(result)
    return result.getvalue()


def setup(tmp_path, *, data=None, runner=None, chosen=None):
    clock = Clock()
    store = LocalObjectStore(tmp_path/'objects')
    settings = JobSettings(database_path=tmp_path/'jobs.sqlite', lease_seconds=10)
    ledger = SQLiteJobLedger(settings, clock)
    artifact, extraction_ref = extract(BytesIO(data or pdf()), scope=SCOPE, document_id=UUID(int=3),
                                      display_filename='synthetic.pdf', declared_mime='application/pdf',
                                      store=store, created_at=clock.now(), extracted_at=clock.now(), runner=runner)
    plan, plan_ref = prepare(artifact, extraction_ref, chosen or profile(chunk_characters=26, max_fan_in=2), store)
    job = admit(ledger,store,plan,plan_ref,request_key='initial')
    return clock,settings,store,ledger,artifact,plan,plan_ref,job


def pump(ledger, store, handler, clock, *, stop=None):
    queue = LocalDispatcher()
    worker = Worker(ledger, queue, store, handler, owner='digestion', classifier=classify_digestion)
    for _ in range(5000):
        relay(ledger,queue)
        if not worker.once():
            return
        if stop and stop():
            return
    pytest.fail('unexpected unbounded execution')


def test_real_pdf_durable_digest_reopen_and_resolvable_evidence(tmp_path):
    clock,settings,store,ledger,artifact,plan,plan_ref,job = setup(tmp_path)
    fake = FakeInference()
    pump(ledger,store,DigestionHandler(ledger,plan_ref,fake),clock)
    assert ledger.get_job(SCOPE,job.job_id).state == 'COMPLETED'
    ledger = SQLiteJobLedger(settings,clock)
    store = LocalObjectStore(store.root)
    digest = load_digest(ledger,store,SCOPE,job.job_id)
    assert digest.status == 'COMPLETE' and digest.coverage.fraction == 1
    assert len(digest.coverage.included) == 6
    canonical = deserialize(store.read(SCOPE,digest.extraction,max_bytes=16000000))
    assert canonical == artifact
    assert len(digest.evidence) == 6
    assert all(resolve(canonical,SCOPE,e).startswith('Synthetic page') for e in digest.evidence)
    assert len(fake.calls) == len(plan.chunks)+len(plan.reducers)
    assert max(n.level for n in plan.reducers) >= 3
    assert len(digest.checkpoints) == len(fake.calls)
    assert all(s.attempt_count == 1 for s in ledger.steps(SCOPE,job.job_id))
    assert read(store,SCOPE,digest.plan,Plan,16000000) == plan


def test_reducer_failure_resumes_only_unfinished_work(tmp_path):
    clock,settings,store,ledger,artifact,plan,plan_ref,job = setup(tmp_path)
    failed = plan.reducers[0].stage_id
    fake = FakeInference(fail_always=(failed,))
    pump(ledger,store,DigestionHandler(ledger,plan_ref,fake),clock)
    assert ledger.get_job(SCOPE,job.job_id).state == 'FAILED'
    old = {s.spec.unit_id:s for s in ledger.steps(SCOPE,job.job_id)}
    analyses = [old[str(c.chunk_id)] for c in plan.chunks]
    assert all(s.state == 'SUCCEEDED' for s in analyses)
    ledger = SQLiteJobLedger(settings,clock)
    resumed = admit(ledger,store,plan,plan_ref,request_key='resume',resume_from=job.job_id)
    fresh = FakeInference()
    pump(ledger,store,DigestionHandler(ledger,plan_ref,fresh),clock)
    assert load_digest(ledger,store,SCOPE,resumed.job_id).status == 'COMPLETE'
    assert not set(fresh.calls) & {c.chunk_id for c in plan.chunks}
    steps = {s.spec.unit_id:s for s in ledger.steps(SCOPE,resumed.job_id)}
    for original in analyses:
        new = steps[original.spec.unit_id]
        assert new.reused_from == original.step_id and new.manifest == original.manifest
        assert new.attempt_count == 0
    # Reuse rows reference the SAME immutable analysis objects; no repeated inference/manifests in a step.
    with sqlite3.connect(settings.database_path) as db:
        assert db.execute('SELECT COUNT(*) FROM artifact_manifests WHERE step_id=?',
                          (str(analyses[0].step_id),)).fetchone()[0] == 1
    assert ledger.get_job(SCOPE,job.job_id).state == 'FAILED'


def test_transient_retry_retains_identity_allowed_data_and_one_manifest(tmp_path):
    clock,settings,store,ledger,artifact,plan,plan_ref,job = setup(tmp_path)
    key = plan.chunks[0].chunk_id
    fake = FakeInference(fail_first=(key,))
    handler = DigestionHandler(ledger,plan_ref,fake)
    pump(ledger,store,handler,clock)
    first = next(s for s in ledger.steps(SCOPE,job.job_id) if s.spec.unit_id == str(key))
    assert first.state == 'RETRY_WAIT'
    clock.advance(1)
    pump(ledger,store,handler,clock)
    second = next(s for s in ledger.steps(SCOPE,job.job_id) if s.spec.unit_id == str(key))
    assert second.step_key == first.step_key and second.attempt_count == 2
    assert len(second.manifest) == 1
    cp = read(store,SCOPE,second.manifest[0],Checkpoint,16000000)
    request = handler.request(plan,key,{}, {})
    assert cp.result.model_dump_json() == __import__('documents.digestion.codec',fromlist=['decode']).decode(
        FakeInference().analyze(request),type(cp.result),3000).model_dump_json()
    assert load_digest(ledger,store,SCOPE,job.job_id).status == 'COMPLETE'
    attempts = ledger.attempts(SCOPE,job.job_id,second.step_id)
    assert [a.outcome for a in attempts] == ['RETRY_WAIT','SUCCEEDED']


@pytest.mark.parametrize('when', ['analysis','intermediate','root','digest'])
def test_cancellation_blocks_acceptance_and_preserves_prior_checkpoints(tmp_path,when):
    clock,settings,store,ledger,artifact,plan,plan_ref,job = setup(tmp_path)
    target = {'analysis':str(plan.chunks[0].chunk_id), 'intermediate':str(plan.reducers[0].stage_id),
              'root':str(plan.root_id),'digest':'digest'}[when]
    real = DigestionHandler(ledger,plan_ref,FakeInference())
    preserved = {}
    def handler(job,step,tracked):
        refs = real(job,step,tracked)
        if step.spec.unit_id == target:
            preserved.update({s.step_id:s.manifest for s in ledger.steps(SCOPE,job.job_id) if s.state == 'SUCCEEDED'})
            ledger.cancel(SCOPE,job.job_id)
        return refs
    pump(ledger,store,handler,clock)
    assert ledger.get_job(SCOPE,job.job_id).state == 'CANCELLED'
    assert not ledger.pending_dispatch()
    for s in ledger.steps(SCOPE,job.job_id):
        if s.step_id in preserved:
            assert s.manifest == preserved[s.step_id]
        if s.spec.unit_id == target or s.spec.unit_id == 'digest':
            assert not s.manifest
    with pytest.raises(DigestionError):
        load_digest(ledger,store,SCOPE,job.job_id)


def test_synthesis_crash_written_checkpoint_and_stale_fence(tmp_path):
    clock,settings,store,ledger,artifact,plan,plan_ref,job = setup(tmp_path)
    queue = LocalDispatcher(); relay(ledger,queue)
    handler = DigestionHandler(ledger,plan_ref,FakeInference())
    Worker(ledger,queue,store,handler,owner='anchor').once()
    step = next(s for s in ledger.steps(SCOPE,job.job_id) if s.spec.unit_id == str(plan.chunks[0].chunk_id))
    lease = ledger.claim(SCOPE,job.job_id,step.step_id,'crashed')
    produced = handler(job,step,IntentStore(store,ledger,lease))
    clock.advance(10); ledger.reconcile(); clock.advance(1)
    ledger = SQLiteJobLedger(settings,clock)
    pump(ledger,store,DigestionHandler(ledger,plan_ref,FakeInference()),clock)
    current = next(s for s in ledger.steps(SCOPE,job.job_id) if s.step_id == step.step_id)
    assert current.manifest == produced and current.attempt_count == 2
    with pytest.raises(JobError,match='stale_fence'):
        ledger.commit(lease,produced)
    assert load_digest(ledger,store,SCOPE,job.job_id).status == 'COMPLETE'


@pytest.mark.parametrize('field,value',[('chunking_profile','analysis-chunks/2'),
                                         ('inference_profile','fake/2'),('reducer_profile','reducer/2')])
def test_changed_profiles_do_not_reuse_checkpoints(tmp_path,field,value):
    clock,settings,store,ledger,artifact,plan,plan_ref,job = setup(tmp_path)
    pump(ledger,store,DigestionHandler(ledger,plan_ref,FakeInference()),clock)
    changed,ref = prepare(artifact,plan.structure.extraction,
                        plan.profile.model_copy(update={field:value}),store)
    new = admit(ledger,store,changed,ref,request_key='changed',resume_from=job.job_id)
    assert all(s.reused_from is None for s in ledger.steps(SCOPE,new.job_id))
    pump(ledger,store,DigestionHandler(ledger,ref,FakeInference()),clock)
    assert load_digest(ledger,store,SCOPE,new.job_id).status == 'COMPLETE'


@pytest.mark.parametrize('policy,outcome',[(True,'PARTIAL'),(False,'FAILED')])
def test_unextractable_pages_coverage_and_policy(tmp_path,policy,outcome):
    class Runner:
        version='synthetic/1'
        def parse(self,data,limits):
            return (ParsedPage(1,'evidence',has_graphics=False),ParsedPage(2,failed=True),
                    ParsedPage(3,has_images=True),ParsedPage(4,has_graphics=True),
                    ParsedPage(5,has_graphics=False))
    chosen = profile(allow_partial=policy,minimum_coverage=.25)
    clock,settings,store,ledger,artifact,plan,plan_ref,job = setup(tmp_path,runner=Runner(),chosen=chosen)
    pump(ledger,store,DigestionHandler(ledger,plan_ref,FakeInference()),clock)
    if outcome == 'FAILED':
        assert ledger.get_job(SCOPE,job.job_id).state == 'FAILED'
        with pytest.raises(DigestionError):
            load_digest(ledger,store,SCOPE,job.job_id)
    else:
        digest=load_digest(ledger,store,SCOPE,job.job_id)
        assert digest.status == 'PARTIAL'
        assert len(digest.coverage.unsupported) == 3
        assert len(digest.coverage.skipped) == 1
        assert digest.coverage.fraction == .25 and digest.open_questions


def test_invalid_evidence_never_accepted_checkpoint(tmp_path):
    clock,settings,store,ledger,artifact,plan,plan_ref,job = setup(tmp_path)
    import json
    class Invalid(FakeInference):
        def analyze(self,request):
            result=json.loads(super().analyze(request))
            result['claims'][0]['evidence_ids']=[str(UUID(int=999))]
            return json.dumps(result).encode()
    pump(ledger,store,DigestionHandler(ledger,plan_ref,Invalid()),clock)
    failed=[s for s in ledger.steps(SCOPE,job.job_id) if s.state == 'FAILED']
    assert len(failed) == 1 and failed[0].manifest == ()
    assert failed[0].failure_category == 'invalid_reference'
    assert ledger.get_job(SCOPE,job.job_id).state == 'FAILED'


def test_corrupt_analysis_checkpoint_rejected_on_resume(tmp_path):
    from documents.errors import DocumentError
    clock,settings,store,ledger,artifact,plan,plan_ref,job=setup(tmp_path)
    pump(ledger,store,DigestionHandler(ledger,plan_ref,
         FakeInference(fail_always=(plan.reducers[0].stage_id,))),clock)
    analysis=next(s for s in ledger.steps(SCOPE,job.job_id) if s.spec.unit_id == str(plan.chunks[0].chunk_id))
    (store.root/str(analysis.manifest[0].key)).write_bytes(b'corrupt synthetic checkpoint')
    with pytest.raises(DocumentError,match='integrity_error'):
        admit(ledger,store,plan,plan_ref,request_key='corrupt-resume',resume_from=job.job_id)


def test_tampered_complete_plan_is_rejected_before_admission(tmp_path):
    from documents.digestion.codec import put
    clock,settings,store,ledger,artifact,plan,plan_ref,job=setup(tmp_path)
    tampered=plan.model_copy(update={'eligible':()})
    tampered_ref=put(store,SCOPE,tampered,16000000)
    with pytest.raises(DigestionError,match='incompatible_checkpoint'):
        admit(ledger,store,tampered,tampered_ref,request_key='tampered')


def test_partial_analysis_is_explicit_in_accepted_digest(tmp_path):
    chosen=profile(chunk_characters=26,max_fan_in=2,allow_partial=True,
                   minimum_coverage=.5,max_failed_units=1)
    clock,settings,store,ledger,artifact,plan,plan_ref,job=setup(tmp_path,chosen=chosen)
    fake=FakeInference(unavailable=(plan.chunks[0].chunk_id,))
    pump(ledger,store,DigestionHandler(ledger,plan_ref,fake),clock)
    digest=load_digest(ledger,store,SCOPE,job.job_id)
    assert digest.status == 'PARTIAL'
    assert len(digest.coverage.failed) == 1
    assert len(digest.coverage.included) == 5
    assert digest.coverage.fraction == 5/6


def test_all_unavailable_analysis_cannot_accept_root_digest(tmp_path):
    chosen=profile(chunk_characters=26,max_fan_in=2,allow_partial=True,
                   minimum_coverage=0,max_failed_units=6)
    clock,settings,store,ledger,artifact,plan,plan_ref,job=setup(tmp_path,chosen=chosen)
    fake=FakeInference(unavailable=tuple(c.chunk_id for c in plan.chunks))
    pump(ledger,store,DigestionHandler(ledger,plan_ref,fake),clock)
    assert ledger.get_job(SCOPE,job.job_id).state == 'FAILED'
    with pytest.raises(DigestionError):
        load_digest(ledger,store,SCOPE,job.job_id)


def test_canonical_corruption_detected_before_final_manifest(tmp_path):
    clock,settings,store,ledger,artifact,plan,plan_ref,job=setup(tmp_path)
    real=DigestionHandler(ledger,plan_ref,FakeInference())
    def handler(job,step,tracked):
        if step.spec.unit_id == 'digest':
            (store.root/str(plan.structure.extraction.key)).write_bytes(b'corrupt canonical data')
        return real(job,step,tracked)
    pump(ledger,store,handler,clock)
    assert ledger.get_job(SCOPE,job.job_id).state == 'FAILED'
    final=next(s for s in ledger.steps(SCOPE,job.job_id) if s.spec.unit_id == 'digest')
    assert final.failure_category == 'integrity_error' and not final.manifest
