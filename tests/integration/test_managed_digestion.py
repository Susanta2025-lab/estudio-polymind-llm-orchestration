"""Managed provider results through real 17B extraction/17C fences/17D validation."""
import json
from uuid import uuid4

import pytest

from test_document_digestion import setup, profile, SCOPE
from documents.digestion.managed import (
    ManagedDigestionHandler, ManagedSettings, ManagedSynthesisInference, StageProfile, classify_managed,
)
from documents.digestion.workflow import admit, load_digest, prepare
from documents.jobs.models import RetryPolicy
from documents.jobs.worker import LocalDispatcher, Worker, relay
from llm.admission import AdmissionPolicy, SQLiteInferenceAdmission
from llm.inference import InferenceRateLimitError, InferenceTimeoutError, InferenceUsage
from llm.structured import CapabilityProfile, GenerationResult


class Provider:
    name='contract'
    model='served'
    def __init__(self): self.calls=[]; self.hook=None; self.error=None; self.forged=False
    def model_id(self,role): return self.model
    def execute(self,request):
        c=json.loads(request.system.split('\nCONTROL\n')[1]); self.calls.append(c)
        if self.hook: self.hook(c)
        if self.error: raise self.error
        result={'stage_id':c['stage_id'],'kind':c['kind'],'claims':[{
            'claim_id':c['claim_ids_in_order'][0],'originating_stage':c['stage_id'],
            'kind':'fact' if c['kind']=='analysis' else 'commentary','text':'Synthetic supported finding.',
            'evidence_ids':[str(uuid4())] if self.forged else c['allowed_evidence_ids'],
            'lineage':c['required_child_links']}]}
        return GenerationResult(json.dumps(result),InferenceUsage(30,40,70),'served','stop')


def managed_setup(tmp_path, retry=None, http=False):
    provider=Provider()
    settings=ManagedSettings(capability=CapabilityProfile(version='contract/1',context_tokens=60000,
        max_output_tokens=4000,overhead_tokens=100,safety_tokens=100),
        profiles=tuple(StageProfile(stage=s,input_tokens=50000,output_tokens=3000)
                       for s in ('chunk','intermediate','structural','root')))
    admission=SQLiteInferenceAdmission(tmp_path/'inference.sqlite','quota',AdmissionPolicy(
        rpm=1000,tpm=10000000,concurrent=4,interactive_rpm=10,interactive_tpm=10000,
        interactive_slots=1,per_job_concurrent=1,per_job_rpm=990))
    selected=provider
    if http:
        from llm.openai_compatible import OpenAICompatibleProvider
        from types import SimpleNamespace
        class Response:
            status_code=200
            headers={}
            def __init__(self, result):
                self.data=json.dumps({'model':'served','choices':[{'message':{'content':result.text},
                    'finish_reason':'stop'}],'usage':{'prompt_tokens':30,'completion_tokens':40,'total_tokens':70}}).encode()
            def iter_content(self,chunk_size):
                for i in range(0,len(self.data),chunk_size): yield self.data[i:i+chunk_size]
            def close(self): pass
        class HTTP:
            def post(self, url, **kwargs):
                sent=kwargs['json']
                assert sent['stream'] is False and 'tools' not in sent
                return Response(provider.execute(SimpleNamespace(system=sent['messages'][0]['content'])))
        selected=OpenAICompatibleProvider(base_url='http://synthetic.example/v1',
            model_map={'summarization':'served'},http_client=HTTP())
    inference=ManagedSynthesisInference(selected,settings,admission)
    clock,js,store,ledger,artifact,plan,ref,job=setup(tmp_path,chosen=inference.profile(
        profile(chunk_characters=26,max_fan_in=2)))
    if retry:
        ledger.cancel(SCOPE,job.job_id)
        job=admit(ledger,store,plan,ref,request_key='retry-policy',retry=retry)
    handler=ManagedDigestionHandler(ledger,ref,inference)
    return clock,store,ledger,plan,ref,job,provider,inference,admission,handler


def pump(ledger,store,handler):
    queue=LocalDispatcher()
    worker=Worker(ledger,queue,store,handler,owner='managed-test',classifier=classify_managed)
    for _ in range(100):
        relay(ledger,queue)
        if not worker.once(): return
    pytest.fail('unbounded execution')


def test_managed_end_to_end_reopen_and_checkpoint_reuse(tmp_path):
    clock,store,ledger,plan,ref,job,p,inf,account,h=managed_setup(tmp_path)
    pump(ledger,store,h)
    digest=load_digest(ledger,store,SCOPE,job.job_id)
    assert digest.status=='COMPLETE' and digest.coverage.fraction==1
    assert len(digest.evidence)==6
    calls=len(p.calls)
    assert calls==len(plan.chunks)+len(plan.reducers)
    assert {c['profile']['stage'] for c in p.calls}=={'chunk','intermediate','structural','root'}
    rows=account.records(SCOPE.identity(),job.job_id)
    assert len(rows)==calls and all(json.loads(r['usage'])['total_tokens']==70 for r in rows)
    from documents.jobs.sqlite import SQLiteJobLedger
    reopened=SQLiteJobLedger(ledger.settings,clock)
    resumed=admit(reopened,store,plan,ref,request_key='resume',resume_from=job.job_id)
    pump(reopened,store,ManagedDigestionHandler(reopened,ref,inf))
    assert len(p.calls)==calls
    assert load_digest(reopened,store,SCOPE,resumed.job_id)==digest
    assert not account.records(SCOPE.identity(),resumed.job_id)


@pytest.mark.parametrize('change',['model','prompt','capability'])
def test_profile_changes_invalidate_reuse(tmp_path,change):
    clock,store,ledger,plan,ref,job,p,inf,account,h=managed_setup(tmp_path)
    pump(ledger,store,h)
    settings=inf.settings
    if change=='model': p.model='new-model'
    if change=='prompt':
        settings=settings.model_copy(update={'profiles':tuple(x.model_copy(update={'version':'managed-stage/2'}) for x in settings.profiles)})
    if change=='capability':
        settings=settings.model_copy(update={'capability':settings.capability.model_copy(update={'version':'contract/2'})})
    new=ManagedSynthesisInference(p,settings,account)
    artifact=h._loaded[1].artifact
    newplan,newref=prepare(artifact,plan.structure.extraction,new.profile(plan.profile),store)
    resumed=admit(ledger,store,newplan,newref,request_key='changed',resume_from=job.job_id)
    assert all(s.reused_from is None for s in ledger.steps(SCOPE,resumed.job_id))


@pytest.mark.parametrize('error,category',[(InferenceRateLimitError(retry_after=23),'inference_rate_limited'),
                                          (InferenceTimeoutError('safe'),'inference_timeout')])
def test_durable_retry_usage_and_single_manifest(tmp_path,error,category):
    clock,store,ledger,plan,ref,job,p,inf,account,h=managed_setup(tmp_path)
    p.error=error
    pump(ledger,store,h)
    waiting=[s for s in ledger.steps(SCOPE,job.job_id) if s.state=='RETRY_WAIT']
    assert waiting and all(s.failure_category==category and not s.manifest for s in waiting)
    delay=23 if category=='inference_rate_limited' else 1
    assert all((s.not_before-clock.now()).total_seconds()==delay for s in waiting)
    assert all(r['usage'] is None for r in account.records(SCOPE.identity(),job.job_id))
    p.error=None; clock.advance(delay)
    pump(ledger,store,h)
    assert load_digest(ledger,store,SCOPE,job.job_id).status=='COMPLETE'
    for s in ledger.steps(SCOPE,job.job_id):
        assert len(s.manifest)==(2 if s.spec.unit_id=='digest' or s.spec.unit_id.startswith('plan/') else 1)
    rows=account.records(SCOPE.identity(),job.job_id)
    assert any(r['attempt']==2 for r in rows)


def test_retry_after_exceeding_budget_is_terminal(tmp_path):
    clock,store,ledger,plan,ref,job,p,inf,account,h=managed_setup(tmp_path,RetryPolicy(budget_seconds=10))
    p.error=InferenceRateLimitError(retry_after=20)
    pump(ledger,store,h)
    assert ledger.get_job(SCOPE,job.job_id).terminal_category=='retry_exhausted'
    assert not ledger.pending_dispatch()


@pytest.mark.parametrize('action',['cancel','expire'])
def test_inflight_response_cannot_commit(tmp_path,action):
    clock,store,ledger,plan,ref,job,p,inf,account,h=managed_setup(tmp_path)
    def hook(control):
        if action=='cancel': ledger.cancel(SCOPE,job.job_id)
        else: clock.advance(11)
    p.hook=hook
    pump(ledger,store,h)
    assert not any(s.manifest for s in ledger.steps(SCOPE,job.job_id) if s.spec.unit_id==p.calls[0]['stage_id'])
    row=account.records(SCOPE.identity(),job.job_id)[0]
    assert json.loads(row['usage'])['total_tokens']==70  # Charged response != accepted result.


def test_forged_evidence_has_usage_but_no_accepted_result(tmp_path):
    clock,store,ledger,plan,ref,job,p,inf,account,h=managed_setup(tmp_path)
    p.forged=True
    pump(ledger,store,h)
    assert ledger.get_job(SCOPE,job.job_id).terminal_category=='invalid_reference'
    failed=[s for s in ledger.steps(SCOPE,job.job_id) if s.state=='FAILED']
    assert len(failed)==1 and not failed[0].manifest
    assert account.records(SCOPE.identity(),job.job_id)[0]['usage'] is not None


def test_existing_openai_provider_through_entire_durable_pipeline(tmp_path):
    clock,store,ledger,plan,ref,job,p,inf,account,h=managed_setup(tmp_path,http=True)
    pump(ledger,store,h)
    digest=load_digest(ledger,store,SCOPE,job.job_id)
    assert digest.status=='COMPLETE' and len(digest.evidence)==6
    assert all(json.loads(r['usage'])['total_tokens']==70 for r in account.records(SCOPE.identity(),job.job_id))
