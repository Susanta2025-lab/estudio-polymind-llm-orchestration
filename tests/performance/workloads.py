"""Small governed jobs with real shared SQLite and a synchronized fake provider."""
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import json
from pathlib import Path
import threading
import time
from uuid import UUID

from documents.digestion.managed import ManagedDigestionHandler, ManagedSettings, ManagedSynthesisInference, StageProfile, classify_managed
from documents.digestion.workflow import prepare, admit, load_digest
from documents.extraction import extract
from documents.jobs.models import JobSettings
from documents.jobs.sqlite import SQLiteJobLedger
from documents.jobs.worker import Worker, LocalDispatcher
from documents.storage import LocalObjectStore
from governance.execution import GovernedExecution
from governance.ledger import GovernanceLedger, Limits, QuotaPolicy, PricingCatalog, Price
from llm.admission import AdmissionPolicy, SQLiteInferenceAdmission
from llm.inference import InferenceUsage
from llm.structured import CapabilityProfile, GenerationResult
from security.authority import SecurityAuthority
from security.models import Action, _verified_principal
from tests.performance.fixtures import NOW, profile, pdf


class SharedProvider:
    name='synthetic'
    def __init__(self,count):
        self.barrier=threading.Barrier(count,timeout=20)
        self.lock=threading.Lock(); self.seen=set(); self.calls=[]; self.active=0;self.peak=0
    def model_id(self,role):return 'offline'
    def execute(self,request):
        control=json.loads(request.system.split('\nCONTROL\n')[1])
        ident=threading.get_ident()
        with self.lock:
            first=ident not in self.seen;self.seen.add(ident)
            self.active+=1;self.peak=max(self.peak,self.active);self.calls.append(control['stage_id'])
        try:
            if first:self.barrier.wait()
            result={'stage_id':control['stage_id'],'kind':control['kind'],'claims':[{
                'claim_id':control['claim_ids_in_order'][0],'originating_stage':control['stage_id'],
                'kind':'fact' if control['kind']=='analysis' else 'commentary',
                'text':'Synthetic source observation; no semantic evaluation.',
                'evidence_ids':control['allowed_evidence_ids'],'lineage':control['required_child_links']}]}
            return GenerationResult(json.dumps(result),InferenceUsage(30,40,70),'offline','stop')
        finally:
            with self.lock:self.active-=1


def governed_jobs(root,count):
    if count not in (1,2,4):raise ValueError('bounded concurrency required')
    root=Path(root).resolve();root.mkdir(parents=True,exist_ok=True)
    started=time.perf_counter();provider=SharedProvider(count)
    auth=SecurityAuthority(root/'security.sqlite');store=LocalObjectStore(root/'objects')
    jobs=SQLiteJobLedger(JobSettings(database_path=root/'jobs.sqlite',lease_seconds=120))
    limits=Limits(requests_per_window=1000,window_seconds=60,interactive_concurrent=8,background_concurrent=4,
        reserved_tokens=10000000,daily_tokens=10000000,monthly_tokens=10000000,monthly_cost='10000000')
    policy=QuotaPolicy(version='phase17h/1',owner=limits,tenant=limits)
    catalog=PricingCatalog(version='synthetic/1',currency='USD',effective_date='2026-01-01',operator_approved=True,
        prices=(Price(provider='synthetic',model='offline',input_price='1',output_price='1',price_unit=1),))
    gov=GovernanceLedger(root/'governance.sqlite',policy,catalog)
    quota=AdmissionPolicy(rpm=1000,tpm=10000000,concurrent=5,interactive_rpm=100,interactive_tpm=1000000,
                          interactive_slots=1,per_job_concurrent=1,per_job_rpm=100)
    admission=SQLiteInferenceAdmission(root/'provider.sqlite','shared-offline',quota)
    settings=ManagedSettings(capability=CapabilityProfile(version='offline/1',context_tokens=100000,
        max_output_tokens=6000,overhead_tokens=100,safety_tokens=100),
        profiles=tuple(StageProfile(stage=s,input_tokens=85000,output_tokens=6000)
                       for s in ('chunk','intermediate','structural','root')))
    entries=[]
    for i in range(count):
        tenant=f'tenant-{i%2}'
        principal=_verified_principal('synthetic-issuer',f'owner-{i}',tenant,expires=int(time.time())+3600)
        operator=_verified_principal('synthetic-issuer',f'operator-{i}',tenant,
                                     frozenset({Action.PUBLICATION_MANAGE}),expires=int(time.time())+3600)
        auth.register(principal);auth.register(operator)
        artifact,ref=extract(BytesIO(pdf(4,seed=1708+i)[0]),scope=principal.scope,document_id=UUID(int=100+i),
            display_filename='concurrent.pdf',declared_mime='application/pdf',store=store,created_at=NOW,extracted_at=NOW)
        auth.register_document(operator,artifact.document)
        # Distinct authority objects coordinate through the same trusted files.
        authority=SecurityAuthority(auth.path)
        accounting=GovernanceLedger(gov.path,policy,catalog)
        account=SQLiteInferenceAdmission(root/'provider.sqlite','shared-offline',quota)
        execution=GovernedExecution(provider,account,accounting,authority,
            authority.snapshot(principal,(artifact.document.document_id,),Action.DOCUMENT_DELETE))
        inference=ManagedSynthesisInference(provider,settings,account,governance=execution)
        plan,pr=prepare(artifact,ref,inference.profile(profile()),store)
        job=admit(jobs,store,plan,pr,request_key=f'job-{i}')
        ledger=SQLiteJobLedger(jobs.settings)
        handler=ManagedDigestionHandler(ledger,pr,inference)
        entries.append((principal,job,ledger,handler))
    def run(entry):
        principal,job,ledger,handler=entry
        start=time.perf_counter();queue=LocalDispatcher()
        worker=Worker(ledger,queue,store,handler,owner=f'worker-{job.job_id}',classifier=classify_managed)
        # This bounded driver is not a new application scheduler.
        for _ in range(50):
            for message in ledger.pending_dispatch(100):
                if message.job_id==job.job_id:
                    queue.send(message);ledger.mark_delivered(message)
            if not worker.once():break
        assert ledger.get_job(principal.scope,job.job_id).state=='COMPLETED'
        digest=load_digest(ledger,store,principal.scope,job.job_id)
        assert digest.status=='COMPLETE' and digest.coverage.fraction==1
        rows=gov.usage(principal,auth)
        calls=admission.records(principal.scope.identity(),job.job_id)
        assert len(rows)==len(calls) and all(r['state']=='SETTLED' and r['actual_cost']=='70' for r in rows)
        assert all(r['owner']==str(principal.scope.owner) and r['tenant']==str(principal.scope.tenant) for r in rows)
        return {'owner':str(principal.scope.owner),'tenant':str(principal.scope.tenant),
            'seconds':time.perf_counter()-start,'calls':len(calls),'status':digest.status,
            'attempts':sum(s.attempt_count for s in ledger.steps(principal.scope,job.job_id))}
    with ThreadPoolExecutor(count) as pool:results=list(pool.map(run,entries))
    assert provider.peak==count and provider.active==0
    assert len(provider.calls)==len(set(provider.calls))==sum(r['calls'] for r in results)
    return {'concurrent_jobs':count,'peak_fake_provider_calls':provider.peak,'provider_limit':5,
            'reserved_interactive_slots':1,'elapsed_seconds':time.perf_counter()-started,
            'jobs':results,'fairness':'all progressed in this controlled sample; no general guarantee',
            'cost':'synthetic catalog arithmetic; no billing','failures':0}


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():raise ValueError('new isolated output required')
    args.output.mkdir(parents=True)
    results=[governed_jobs(args.output/str(n),n) for n in (1,2,4)]
    (args.output/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
