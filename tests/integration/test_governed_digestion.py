"""Governance composed with real checkpoint scheduling and provider admission."""
import time

import test_document_digestion as digestion_fixture
import test_managed_digestion as managed_fixture
from documents.serialization import deserialize
from documents.digestion.workflow import load_digest
from governance.execution import GovernedExecution
from governance.ledger import GovernanceLedger, PricingCatalog, Price
from security.authority import SecurityAuthority
from security.models import Action, _verified_principal
from tests.unit.test_governance import configuration


def setup(tmp_path,monkeypatch,budget='1000000'):
    a=_verified_principal('issuer','alice','tenant',expires=int(time.time())+3600)
    op=_verified_principal('issuer','operator','tenant',frozenset({Action.PUBLICATION_MANAGE}),expires=int(time.time())+3600)
    monkeypatch.setattr(digestion_fixture,'SCOPE',a.scope)
    monkeypatch.setattr(managed_fixture,'SCOPE',a.scope)
    clock,store,jobs,plan,ref,job,p,inf,admission,handler=managed_fixture.managed_setup(tmp_path)
    auth=SecurityAuthority(tmp_path/'security.sqlite');auth.register(a);auth.register(op)
    artifact=deserialize(store.read(a.scope,plan.structure.extraction,max_bytes=16000000))
    auth.register_document(op,artifact.document)
    policy,_=configuration(budget)
    catalog=PricingCatalog(version='test/1',currency='USD',effective_date='2026-01-01',operator_approved=True,
        prices=(Price(provider=p.name,model=p.model,input_price='1',output_price='1',price_unit=1),))
    ledger=GovernanceLedger(tmp_path/'gov.sqlite',policy,catalog)
    inf.governance=GovernedExecution(p,admission,ledger,auth,auth.snapshot(a,(artifact.document.document_id,),Action.DOCUMENT_DELETE))
    return clock,store,jobs,plan,job,p,inf,admission,handler,ledger,auth,a


def test_governed_background_stages_reconcile_once(tmp_path,monkeypatch):
    clock,store,jobs,plan,job,p,inf,admission,handler,ledger,auth,a=setup(tmp_path,monkeypatch)
    managed_fixture.pump(jobs,store,handler)
    assert load_digest(jobs,store,a.scope,job.job_id).status=='COMPLETE'
    rows=ledger.usage(a,auth)
    assert len(rows)==len(p.calls)==len(admission.records(a.scope.identity(),job.job_id))
    assert all(r['workload']=='DOCUMENT_BACKGROUND' and r['state']=='SETTLED' and r['actual_cost']=='70' for r in rows)


def test_budget_exhaustion_keeps_checkpoints_without_upstream_or_retry_storm(tmp_path,monkeypatch):
    clock,store,jobs,plan,job,p,inf,admission,handler,ledger,auth,a=setup(tmp_path,monkeypatch,'1')
    managed_fixture.pump(jobs,store,handler)
    assert jobs.get_job(a.scope,job.job_id).terminal_category=='governance_denied'
    assert any(step.manifest for step in jobs.steps(a.scope,job.job_id))
    assert not p.calls and not admission.records(a.scope.identity(),job.job_id)
    assert not ledger.usage(a,auth)


def test_cancellation_after_paid_work_preserves_both_ledgers(tmp_path,monkeypatch):
    clock,store,jobs,plan,job,p,inf,admission,handler,ledger,auth,a=setup(tmp_path,monkeypatch)
    p.hook=lambda _:jobs.cancel(a.scope,job.job_id)
    managed_fixture.pump(jobs,store,handler)
    assert len(p.calls)==1
    assert ledger.usage(a,auth)[0]['actual_cost']=='70'
    assert len(admission.records(a.scope.identity(),job.job_id))==1
    assert not any(step.manifest for step in jobs.steps(a.scope,job.job_id) if step.spec.unit_id==p.calls[0]['stage_id'])
