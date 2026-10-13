import pytest
from tests.performance.workloads import governed_jobs


@pytest.mark.parametrize('count',[1,2,4])
def test_governed_jobs_share_quota_and_keep_principals_separate(tmp_path,count,record_property):
    result=governed_jobs(tmp_path,count)
    assert result['peak_fake_provider_calls']==count
    assert len(result['jobs'])==count
    record_property('observations',__import__('json').dumps(result))


@pytest.mark.parametrize('shared_tenant',[False,True])
def test_eight_authority_connections_cannot_spend_one_balance_twice(tmp_path,shared_tenant):
    from concurrent.futures import ThreadPoolExecutor
    import threading,time
    from decimal import Decimal
    from governance.ledger import GovernanceLedger, GovernanceError
    from security.authority import SecurityAuthority
    from security.models import _verified_principal
    from tests.unit.test_governance import configuration, identity
    policy,catalog=configuration('20')
    auth=SecurityAuthority(tmp_path/'security.sqlite')
    people=[_verified_principal('offline',str(i) if shared_tenant else 'owner','A',expires=int(time.time())+3600) for i in range(8)]
    for person in people:auth.register(person)
    ledgers=[GovernanceLedger(tmp_path/'governance.sqlite',policy,catalog) for _ in people]
    barrier=threading.Barrier(8,timeout=10)
    def reserve(pair):
        ledger,person=pair;barrier.wait()
        try:return ledger.reserve(person,identity(person),4,4)
        except GovernanceError:return None
    with ThreadPoolExecutor(8) as pool:outcomes=list(pool.map(reserve,zip(ledgers,people)))
    assert sum(o is not None for o in outcomes)==2
    with ledgers[0].transaction() as db:
        rows=list(db.execute('SELECT cost,state FROM reservations'))
    assert len(rows)==2 and sum(Decimal(r['cost']) for r in rows)==16
    assert all(r['state']=='RESERVED' for r in rows)


def test_concurrent_duplicate_logical_attempt_executes_provider_once(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    from dataclasses import replace
    import threading,time
    from governance.ledger import GovernanceLedger, GovernanceError
    from security.authority import SecurityAuthority
    from security.models import _verified_principal
    from tests.unit.test_governance import configuration, identity, execution
    auth=SecurityAuthority(tmp_path/'auth.sqlite')
    principal=_verified_principal('offline','owner','A',expires=int(time.time())+3600);auth.register(principal)
    ledger=GovernanceLedger(tmp_path/'governance.sqlite',*configuration('10000'))
    executor,request,calls=execution((ledger,auth,principal,principal))
    call=replace(identity(principal),role=request.role.value,capability=request.capability.version)
    barrier=threading.Barrier(8,timeout=10)
    def attempt(_):
        barrier.wait()
        try:executor.execute(request,identity=call);return True
        except GovernanceError:return False
    with ThreadPoolExecutor(8) as pool:results=list(pool.map(attempt,range(8)))
    assert sum(results)==len(calls)==1
    rows=ledger.usage(principal,auth)
    assert len(rows)==1 and rows[0]['actual_cost']=='2'
