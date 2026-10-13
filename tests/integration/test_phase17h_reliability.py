"""Bounded physical fixtures and real interpreter termination; no live services."""
from datetime import timedelta
from io import BytesIO
import json
from pathlib import Path
import subprocess
import sys
from uuid import UUID

import pytest
from pypdf import PdfReader, PdfWriter

from documents.config import ExtractionSettings
from documents.errors import DocumentError
from documents.extraction import extract
from documents.storage import LocalObjectStore
from documents.digestion.inference import FakeInference
from documents.digestion.models import DigestionError
from documents.digestion.planning import build_plan
from documents.digestion.workflow import prepare, admit, DigestionHandler, load_digest, classify_digestion
from documents.jobs.models import JobSettings
from documents.jobs.sqlite import SQLiteJobLedger
from documents.jobs.worker import LocalDispatcher, Worker, relay
from tests.performance.fixtures import pdf, NOW, SCOPE, profile
from tests.performance.phase17h import inventory, configuration, measure


@pytest.mark.parametrize('kind,status', [('text','native_text'),('blank','blank'),('image','image_only'),
    ('figure','unresolved'),('columns','native_text'),('table','native_text'),('mixed','native_text')])
def test_real_pdf_type_fidelity(tmp_path,kind,status):
    raw,manifest=pdf(2,kinds=('text',kind))
    assert raw==pdf(2,kinds=('text',kind))[0]
    assert len(PdfReader(BytesIO(raw)).pages)==manifest['physical_pages']==2
    artifact,ref=extract(BytesIO(raw),scope=SCOPE,document_id=UUID(int=2),display_filename='manual.pdf',
        declared_mime='application/pdf',store=LocalObjectStore(tmp_path/'objects'),created_at=NOW,extracted_at=NOW)
    assert artifact.units[1].status==status
    if kind in ('image','mixed'): assert artifact.units[1].decision.observations.has_images
    if kind == 'columns':
        # pypdf joins side-by-side cells: content retained, layout not certified.
        assert all(line in artifact.units[1].text for line in manifest['expected'][1]['lines'])
        assert len(artifact.units[1].text.splitlines()) == 3
    elif kind in ('text','table','mixed'):
        assert artifact.units[1].text.splitlines()==manifest['expected'][1]['lines']
    # Native tables/columns are text, with no invented cells or structure.
    assert all(b.visual is None and b.kind=='text' for u in artifact.units for b in u.blocks)
    chosen=profile(allow_partial=True,minimum_coverage=.5)
    plan=build_plan(artifact,ref,chosen)
    assert len(plan.eligible)+len(plan.skipped)+len(plan.unsupported)==2
    if kind in ('image','figure'): assert len(plan.unsupported)==1
    store=LocalObjectStore(tmp_path/'objects'); plan,pr=prepare(artifact,ref,chosen,store)
    ledger=SQLiteJobLedger(JobSettings(database_path=tmp_path/'jobs.sqlite'))
    job=admit(ledger,store,plan,pr,request_key='fidelity')
    queue=LocalDispatcher(); worker=Worker(ledger,queue,store,DigestionHandler(ledger,pr,FakeInference()),
                                         owner='type-test',classifier=classify_digestion)
    for _ in range(20):
        relay(ledger,queue)
        if not worker.once(): break
    digest=load_digest(ledger,store,SCOPE,job.job_id)
    assert digest.status==('PARTIAL' if kind in ('image','figure') else 'COMPLETE')


@pytest.mark.parametrize('case,category', [('malformed','invalid_document'),('encrypted','encrypted_document'),
    ('oversize','source_too_large'),('filename','invalid_document'),('misleading','unsupported_format'),
    ('artifact','extraction_limit_exceeded'),('scanned','coverage_failed')])
def test_refusal_and_unsupported_matrix(tmp_path,case,category):
    raw,_=pdf(2,kinds=('image','image') if case=='scanned' else None)
    name='manual.pdf'; limits=ExtractionSettings()
    if case=='malformed': raw=b'%PDF-invalid synthetic'
    if case=='encrypted':
        writer=PdfWriter(clone_from=BytesIO(raw)); writer.encrypt('synthetic-only'); stream=BytesIO();writer.write(stream);raw=stream.getvalue()
    if case=='oversize': limits=ExtractionSettings(max_source_bytes=len(raw)-1)
    if case=='filename': name='x'*513+'.pdf'
    if case=='misleading': name='manual.txt'
    if case=='artifact': limits=ExtractionSettings(max_artifact_bytes=100)
    with pytest.raises((DocumentError,DigestionError),match=category):
        artifact,ref=extract(BytesIO(raw),scope=SCOPE,document_id=UUID(int=3),display_filename=name,
            declared_mime='application/pdf',store=LocalObjectStore(tmp_path/'objects'),limits=limits)
        build_plan(artifact,ref,profile())


def test_small_fixture_cannot_bypass_chunk_step_or_character_limits(tmp_path):
    raw,_=pdf(4)
    artifact,ref=extract(BytesIO(raw),scope=SCOPE,document_id=UUID(int=4),display_filename='manual.pdf',
        declared_mime='application/pdf',store=LocalObjectStore(tmp_path/'objects'))
    for changes in ({'max_chunks':1,'chunk_characters':30},{'max_steps':3},{'max_source_units':1}):
        with pytest.raises(DigestionError,match='synthesis_limit_exceeded'):
            build_plan(artifact,ref,profile(**changes))


def test_resource_monitor_tolerates_disappearing_journal(tmp_path,monkeypatch):
    journal=tmp_path/'jobs.sqlite-journal';journal.write_bytes(b'transient')
    original=Path.stat
    def disappearing(path,*args,**kwargs):
        if path==journal: raise FileNotFoundError()
        return original(path,*args,**kwargs)
    monkeypatch.setattr(Path,'stat',disappearing)
    assert inventory(tmp_path)=={'files':0,'bytes':0}
    assert measure([.1,.2,.3])['p95_seconds'] is None
    assert measure([.1]*100)['p95_seconds']==.1


@pytest.mark.parametrize('key,value',[('pages',[100000]),('max_seconds',0),('max_files',True),('query_samples',1000)])
def test_benchmark_configuration_rejects_unbounded_runs(tmp_path,key,value):
    data=json.loads(Path('tests/fixtures/phase17h/profile.json').read_text());data[key]=value
    target=tmp_path/'profile.json';target.write_text(json.dumps(data))
    with pytest.raises(ValueError):configuration(target)


CRASH_SCRIPT = '''
from pathlib import Path
from datetime import datetime
from types import SimpleNamespace
from uuid import UUID
import os, sys
from documents.jobs.models import JobSettings
from documents.jobs.sqlite import SQLiteJobLedger
from documents.jobs.worker import IntentStore, ExtractionHandler
from documents.storage import LocalObjectStore
from documents.models import Scope
root=Path(sys.argv[1]); point=sys.argv[2]
clock=SimpleNamespace(now=lambda:datetime.fromisoformat(sys.argv[4]))
ledger=SQLiteJobLedger(JobSettings(database_path=root/'jobs.sqlite',lease_seconds=10),clock)
scope=Scope(tenant=UUID(int=100),owner=UUID(int=200));job=ledger.get_job(scope,UUID(sys.argv[3]))
step=ledger.steps(scope,job.job_id)[0]
lease=ledger.claim(scope,job.job_id,step.step_id,'child')
(root/'lease.json').write_text(lease.model_dump_json())
if point=='claim':os._exit(77)
refs=ExtractionHandler()(job,step,IntentStore(LocalObjectStore(root/'objects'),ledger,lease))
(root/'produced.json').write_text(refs[0].model_dump_json())
if point=='write':os._exit(77)
ledger.commit(lease,refs)
os._exit(77)
'''

# Reuse admission fixtures, keeping existing durability tests as authoritative contracts.
from test_document_jobs import setup, SCOPE as JOB_SCOPE


@pytest.mark.parametrize('point',['claim','write','commit','cancel'])
def test_hard_process_exit_recovers_without_accepting_uncommitted_work(setup,tmp_path,point,record_property):
    from documents.jobs.models import Lease
    from documents.jobs.errors import JobError
    from documents.jobs.worker import ExtractionHandler
    clock,settings,store,ledger,service,job=setup()
    before=__import__('time').perf_counter()
    child=subprocess.run([sys.executable,'-c',CRASH_SCRIPT,str(tmp_path),'write' if point=='cancel' else point,
                          str(job.job_id),clock.now().isoformat()],capture_output=True,text=True,timeout=20)
    assert child.returncode==77,child.stderr
    step=ledger.steps(JOB_SCOPE,job.job_id)[0]
    assert bool(step.manifest)==(point=='commit')
    if point=='cancel': ledger.cancel(JOB_SCOPE,job.job_id)
    clock.advance(10)
    fresh=SQLiteJobLedger(settings,clock); fresh.reconcile();clock.advance(1)
    queue=LocalDispatcher();relay(fresh,queue)
    worker=Worker(fresh,queue,store,ExtractionHandler(),owner='restarted')
    for _ in range(5):
        if not worker.once():break
    expected='CANCELLED' if point=='cancel' else 'COMPLETED'
    assert fresh.get_job(JOB_SCOPE,job.job_id).state==expected
    completed=fresh.steps(JOB_SCOPE,job.job_id)[0]
    assert bool(completed.manifest)==(point!='cancel')
    if point=='commit': assert completed.attempt_count==1
    if point=='write':
        from documents.models import ObjectRef
        assert completed.manifest==(ObjectRef.model_validate_json((tmp_path/'produced.json').read_text()),)
        stale=Lease.model_validate_json((tmp_path/'lease.json').read_text())
        with pytest.raises(JobError,match='stale_fence'):fresh.commit(stale,completed.manifest)
    record_property('recovery_wall_seconds',__import__('time').perf_counter()-before)
    record_property('controlled_clock_elapsed_seconds',11)
    record_property('lease_seconds',10)
