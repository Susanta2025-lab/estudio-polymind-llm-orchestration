"""Explicit latency characterization with held fake background inference.

This isolates quota headroom and SQLite contention. Paused fake providers are not
representative real-model/CPU load; the proposed 20% production target is not tested.
"""
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import json
from pathlib import Path
import threading
import time
from uuid import UUID

from tests.performance.fixtures import NOW, pdf, profile
from tests.performance.phase17h import measure, write


def run(root, samples=100):
    import pytest
    from tests.unit.publication.conftest import env
    from tests.unit.publication.test_security import secure_publication
    from tests.unit.test_governance import configuration
    from documents.publication.analysis import AnalysisRequest
    from documents.extraction import extract
    from documents.digestion.managed import ManagedSettings, StageProfile, ManagedSynthesisInference, ManagedDigestionHandler, classify_managed
    from documents.digestion.workflow import prepare, admit, load_digest
    from documents.jobs.worker import LocalDispatcher, Worker
    from governance.execution import GovernedExecution
    from governance.ledger import GovernanceLedger
    from llm.admission import AdmissionPolicy, SQLiteInferenceAdmission
    from llm.structured import CapabilityProfile, GenerationResult
    from llm.inference import InferenceUsage
    from security.models import Action
    root.mkdir(parents=True)
    results=[]
    for count in (0,1,4):
        directory=root/str(count);directory.mkdir()
        monkey=pytest.MonkeyPatch()
        try:
            secured,auth,(owner,shared,foreign,op),service,analysis,original=secure_publication.__wrapped__(
                env.__wrapped__(directory),directory,monkey)
            policy,catalog=configuration('10000000')
            policy=policy.model_copy(update={key:getattr(policy,key).model_copy(update={'requests_per_window':1000}) for key in ('owner','tenant')})
            ledger=GovernanceLedger(directory/'latency-governance.sqlite',policy,catalog)
            admission=SQLiteInferenceAdmission(directory/'latency-provider.sqlite','latency',AdmissionPolicy(
                rpm=1000,tpm=10000000,concurrent=5,interactive_rpm=500,interactive_tpm=5000000,
                interactive_slots=1,per_job_concurrent=1,per_job_rpm=100))
            secured.ledger=ledger;secured.admission=admission
            release=threading.Event();entered=[threading.Event() for _ in range(count)]
            class Provider:
                name='fake'
                def model_id(self,role):return 'model'
                def execute(self,request):return original.execute(request)
            interactive=Provider();analysis.provider=interactive
            handlers=[]
            settings=ManagedSettings(capability=CapabilityProfile(version='latency/1',context_tokens=100000,
                max_output_tokens=6000,overhead_tokens=100,safety_tokens=100),profiles=tuple(
                StageProfile(stage=s,input_tokens=85000,output_tokens=6000) for s in ('chunk','intermediate','structural','root')))
            for i in range(count):
                class Background(Provider):
                    def __init__(self,event):self.event=event;self.once=True
                    def execute(self,request):
                        if self.once:
                            self.once=False;self.event.set()
                            if not release.wait(120):raise TimeoutError('benchmark background deadline')
                        c=json.loads(request.system.split('\nCONTROL\n')[1])
                        data={'stage_id':c['stage_id'],'kind':c['kind'],'claims':[{
                            'claim_id':c['claim_ids_in_order'][0],'originating_stage':c['stage_id'],
                            'kind':'fact' if c['kind']=='analysis' else 'commentary','text':'Synthetic observation',
                            'evidence_ids':c['allowed_evidence_ids'],'lineage':c['required_child_links']}]}
                        return GenerationResult(json.dumps(data),InferenceUsage(30,40,70),'model','stop')
                artifact,ref=extract(BytesIO(pdf(2)[0]),scope=owner.scope,document_id=UUID(int=200+i),
                    display_filename='background.pdf',declared_mime='application/pdf',store=service.objects,created_at=NOW,extracted_at=NOW)
                auth.register_document(op,artifact.document)
                provider=Background(entered[i])
                executor=GovernedExecution(provider,admission,ledger,auth,auth.snapshot(owner,(artifact.document.document_id,),Action.DOCUMENT_DELETE))
                inference=ManagedSynthesisInference(provider,settings,admission,governance=executor)
                plan,pr=prepare(artifact,ref,inference.profile(profile()),service.objects)
                job=admit(service.jobs,service.objects,plan,pr,request_key=f'latency-{i}')
                handlers.append((job,ManagedDigestionHandler(service.jobs,pr,inference)))
            def background(entry):
                job,handler=entry;queue=LocalDispatcher()
                worker=Worker(service.jobs,queue,service.objects,handler,owner=str(job.job_id),classifier=classify_managed)
                for _ in range(30):
                    for message in service.jobs.pending_dispatch(100):
                        if message.job_id==job.job_id:queue.send(message);service.jobs.mark_delivered(message)
                    if not worker.once():break
                assert load_digest(service.jobs,service.objects,owner.scope,job.job_id).status=='COMPLETE'
            durations=[];failures=[]
            with ThreadPoolExecutor(max(1,count)) as pool:
                futures=[pool.submit(background,entry) for entry in handlers]
                try:
                    assert all(e.wait(20) for e in entered)
                    for _ in range(samples):
                        start=time.perf_counter()
                        try:
                            result,_=secured.analyze(owner,AnalysisRequest(query='alpha',document_ids=(UUID(int=3),)))
                            assert result['citations']
                        except Exception as exc:failures.append(type(exc).__name__)
                        finally:durations.append(time.perf_counter()-start)
                finally:release.set()
                for future in futures:future.result(30)
            result={'active_background_jobs':count,**measure(durations),'samples':durations,
                'failures':failures,'warmup':'publication loaded; no requests discarded',
                'workload':'held fake upstream inference; real authorized analysis and shared accounting',
                'target_20_percent':'NOT ESTABLISHED for representative workload',
                'background_jobs_completed':len(futures),'provider_slots':5,'reserved_interactive_slots':1}
            results.append(result);write(root/'results.json',results)
            if failures:raise AssertionError('latency request failures recorded')
        finally:monkey.undo()
    return results


if __name__=='__main__':
    import argparse,signal,resource
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);args=p.parse_args()
    if args.output.exists() or args.output.resolve().is_relative_to(Path.cwd()):raise ValueError('new outside-repository output required')
    resource.setrlimit(resource.RLIMIT_CPU,(180,181));signal.alarm(240)
    run(args.output.resolve())
