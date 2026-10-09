from concurrent.futures import ThreadPoolExecutor
import threading
import time
from uuid import uuid4

import pytest

from governance.ledger import GovernanceLedger, GovernanceError, Limits, QuotaPolicy, PricingCatalog, Price
from governance.execution import GovernedExecution
from llm.admission import CallIdentity
from llm.inference import InferenceUsage, ModelRole, InferenceRateLimitError, InferenceTimeoutError
from llm.structured import CapabilityProfile, GenerationRequest, GenerationResult
from security.authority import SecurityAuthority
from security.models import _verified_principal


def configuration(budget='10'):
    limit=Limits(requests_per_window=100,window_seconds=60,interactive_concurrent=10,background_concurrent=10,
        reserved_tokens=10000000,daily_tokens=10000000,monthly_tokens=10000000,monthly_cost=budget)
    policy=QuotaPolicy(version='test/1',owner=limit,tenant=limit)
    catalog=PricingCatalog(version='test/1',currency='USD',effective_date='2026-01-01',operator_approved=True,
        prices=(Price(provider='fake',model='model',input_price='1',output_price='1',price_unit=1),))
    return policy,catalog


@pytest.fixture
def gov(tmp_path):
    authority=SecurityAuthority(tmp_path/'security.sqlite')
    a=_verified_principal('issuer','alice','tenant',expires=int(time.time())+3600)
    b=_verified_principal('issuer','bob','tenant',expires=int(time.time())+3600)
    authority.register(a);authority.register(b)
    ledger=GovernanceLedger(tmp_path/'governance.sqlite',*configuration())
    return ledger,authority,a,b


def identity(p,attempt=1,job=None,step=None):
    return CallIdentity(p.scope.identity(),job or uuid4(),step or uuid4(),attempt,'test/1','fake','general','model','test/1')


@pytest.mark.parametrize('tenant_race',[False,True])
def test_atomic_eight_of_ten_reservation_race(gov,tenant_race):
    ledger,auth,a,b=gov
    barrier=threading.Barrier(2)
    def reserve(person):
        barrier.wait()
        try: return ledger.reserve(person,identity(person),4,4)
        except GovernanceError: return None
    with ThreadPoolExecutor(2) as pool:
        outcomes=list(pool.map(reserve,[a,b if tenant_race else a]))
    assert sum(t is not None for t in outcomes)==1
    with ledger.transaction() as db:
        assert db.execute('SELECT COUNT(*) FROM reservations').fetchone()[0]==1


def test_duplicate_admission_settlement_retry_and_owner_visibility(gov):
    from dataclasses import replace
    ledger,auth,a,b=gov
    call=identity(a)
    ticket=ledger.reserve(a,call,4,4)
    assert ledger.reserve(a,call,4,4)==ticket
    with pytest.raises(GovernanceError): ledger.reserve(a,replace(call,profile='changed/2'),4,4)
    ledger.transition(ticket,'RESERVED','ADMITTING');ledger.transition(ticket,'ADMITTING','STARTED')
    with pytest.raises(GovernanceError): ledger.transition(ticket,'RESERVED','ADMITTING')
    ledger.settle(ticket,InferenceUsage(1,1,2));ledger.settle(ticket,InferenceUsage(1,1,2))
    with pytest.raises(GovernanceError): ledger.settle(ticket,InferenceUsage(0,0,0))
    retry=identity(a,2,call.job,call.step)
    assert ledger.reserve(a,retry,4,4)!=ticket
    assert len(ledger.usage(a,auth))==2
    assert ledger.usage(b,auth)==[]


def test_unknown_crash_restart_and_explicit_reconciliation(gov):
    ledger,auth,a,b=gov
    ticket=ledger.reserve(a,identity(a),4,4)
    ledger.transition(ticket,'RESERVED','ADMITTING');ledger.transition(ticket,'ADMITTING','STARTED')
    ledger.settle(ticket,None)
    reopened=GovernanceLedger(ledger.path,*configuration(),clock=lambda:time.time()+40*86400)
    # Use live principal for later simulated month; unsettled amount still counts.
    future=_verified_principal('issuer','alice','tenant',expires=int(time.time())+50*86400)
    with pytest.raises(GovernanceError): reopened.reserve(future,identity(future),4,4)
    reopened.settle(ticket,InferenceUsage(1,1,2))
    assert reopened.reserve(future,identity(future),4,4)


def test_missing_price_and_invalid_money(gov):
    from dataclasses import replace
    ledger,auth,a,b=gov
    with pytest.raises(GovernanceError): ledger.reserve(a,replace(identity(a),model='unknown'),1,1)
    for value in ('NaN','-1','Infinity',0.1):
        with pytest.raises(ValueError): Price(provider='fake',model='model',input_price=value,output_price='1',price_unit=1)


def execution(gov,*,admission_failure=False,provider_failure=False):
    ledger,auth,a,b=gov
    calls=[]
    class Provider:
        name='fake'
        def model_id(self,role):return 'model'
        def execute(self,request):
            calls.append(request)
            if provider_failure: raise InferenceTimeoutError('safe')
            return GenerationResult('answer',InferenceUsage(1,1,2),'model')
    class Admission:
        def acquire(self,*args):
            if admission_failure:raise InferenceRateLimitError()
            return 'provider-ticket'
        def finish(self,*args,**kwargs):pass
    cap=CapabilityProfile(version='test/1',context_tokens=10000,max_output_tokens=8,overhead_tokens=0,safety_tokens=0)
    request=GenerationRequest('s','d',ModelRole.GENERAL,cap,4,100,{},1)
    return GovernedExecution(Provider(),Admission(),ledger,auth,auth.snapshot(a)),request,calls


def test_governance_denial_makes_no_provider_call(gov):
    executor,request,calls=execution(gov)
    with pytest.raises(GovernanceError):executor.execute(request)
    assert not calls


@pytest.mark.parametrize('failure',['admission','timeout','success'])
def test_execution_release_unknown_and_actual(tmp_path,failure):
    auth=SecurityAuthority(tmp_path/'auth.sqlite')
    a=_verified_principal('issuer','a','t',expires=int(time.time())+3600);auth.register(a)
    ledger=GovernanceLedger(tmp_path/'gov.sqlite',*configuration('10000'))
    gov=(ledger,auth,a,a)
    executor,request,calls=execution(gov,admission_failure=failure=='admission',provider_failure=failure=='timeout')
    if failure=='success': executor.execute(request)
    else:
        with pytest.raises((InferenceRateLimitError,InferenceTimeoutError)): executor.execute(request)
    row=ledger.usage(a,auth)[0]
    assert row['state']=={'admission':'RELEASED','timeout':'UNKNOWN','success':'SETTLED'}[failure]
    assert len(calls)==(failure!='admission')
    assert row['actual_cost']==('2' if failure=='success' else None)


def test_duplicate_execution_calls_provider_and_charges_once(tmp_path):
    auth = SecurityAuthority(tmp_path/'auth.sqlite')
    principal = _verified_principal('issuer', 'duplicate', 'tenant', expires=int(time.time())+3600)
    auth.register(principal)
    ledger = GovernanceLedger(tmp_path/'gov.sqlite', *configuration('10000'))
    executor, request, calls = execution((ledger, auth, principal, principal))
    call = identity(principal)
    # The execution boundary checks role and capability as well as logical identity.
    from dataclasses import replace
    call = replace(call, role=request.role.value, capability=request.capability.version)
    executor.execute(request, identity=call)
    with pytest.raises(GovernanceError):
        executor.execute(request, identity=call)
    rows = ledger.usage(principal, auth)
    assert len(calls) == len(rows) == 1
    assert rows[0]['state'] == 'SETTLED' and rows[0]['actual_cost'] == '2'
