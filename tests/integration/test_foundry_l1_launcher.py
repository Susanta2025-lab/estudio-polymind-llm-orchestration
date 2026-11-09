"""Real L1 composition with signed test identity and intercepted provider HTTP only."""
import json
import socket
import time

import pytest

from tests.unit.test_security_identity import identity
from tests.approval_helpers import approval_signer
from tests.performance import foundry_l1 as launch
from tests.performance.foundry_preflight import OfflineHTTP, synthetic_contract
from tests.performance.foundry_recalibration import DEPLOYMENT, RESOURCE, candidate_policy
from tests.performance.phase17h import SyntheticModel, SyntheticVectors
from security.authority import SecurityAuthority
from governance.ledger import GovernanceLedger, Limits, QuotaPolicy
from llm.admission import SQLiteInferenceAdmission


@pytest.fixture(autouse=True)
def deny_network(monkeypatch):
    def deny(*args,**kwargs):
        raise AssertionError('Network forbidden')
    monkeypatch.setattr(socket.socket,'connect',deny)
    monkeypatch.setattr(socket,'create_connection',deny)


@pytest.fixture
def composition(tmp_path,identity,monkeypatch,approval_signer):
    verifier,token,_,_ = identity
    principal = verifier.verify(token({'roles':['operator']}))
    tmp_path.chmod(0o700)
    root=tmp_path/'audit';root.mkdir(mode=0o700)
    c=synthetic_contract().model_dump(mode='json')
    c.update(model=DEPLOYMENT,region='TEST-REGION',tier='GlobalStandard', attempts=4,
             total_input=100000,total_output=12000,rpm=1)
    c['catalog']['prices'][0]['model']=DEPLOYMENT
    limits=Limits(requests_per_window=2,window_seconds=60,interactive_concurrent=1,
        background_concurrent=1,reserved_tokens=28000,daily_tokens=112000,monthly_tokens=112000,monthly_cost='5')
    cfg=launch.LaunchConfiguration(resource=RESOURCE,deployment=DEPLOYMENT,model='gpt-5.4-mini',
        model_version='2026-03-17',sku='GlobalStandard',endpoint=f'https://{RESOURCE}.openai.azure.com/openai/v1',
        authentication='api_key',credential_valid_until=int(time.time())+3600,credential_audience_verified=True,
        quota_verified=True,shared_consumers_verified=True,charges_verified=True,approval_expires=int(time.time())+3600,
        owner_scope=principal.scope.identity(),oidc=verifier.config,security_path=tmp_path/'security.sqlite',
        governance_path=tmp_path/'governance.sqlite',admission_path=tmp_path/'admission.sqlite',quota_key=DEPLOYMENT,
        audit_directory=root,embedding_directory=tmp_path/'embedding',embedding_tree_sha256='0'*64,
        actual_azure_rpm=10,actual_azure_tpm=30000,policy=candidate_policy(),
        governance_policy=QuotaPolicy(version='test/1',owner=limits,tenant=limits),contract=c)
    authority=SecurityAuthority(cfg.security_path);authority.register(principal)
    GovernanceLedger(cfg.governance_path,cfg.governance_policy,cfg.contract.catalog)
    SQLiteInferenceAdmission(cfg.admission_path,cfg.quota_key,cfg.policy)
    monkeypatch.setattr(launch,'OIDCVerifier',lambda _:verifier)
    from documents.publication.encoding import RetrievalEncoder
    from documents.publication.models import RetrievalProfile
    vectors=SyntheticVectors();vectors.close=lambda:None
    monkeypatch.setattr(launch,'local_retrieval',lambda _: (vectors,RetrievalEncoder(RetrievalProfile(),SyntheticModel())))
    now=[time.time()]
    def advance(runtime):
        now[0]+=61
        runtime.guard.clock=runtime.ledger.clock=runtime.guard.admission.clock=lambda:now[0]
    monkeypatch.setattr(launch.Runtime,'wait',advance)
    class HTTP(OfflineHTTP):
        def __init__(self):
            super().__init__();self.sent=[];self.closed=False
        def post(self,url,**kwargs):
            self.sent.append((url,kwargs))
            response=super().post(url,**kwargs)
            raw=json.loads(b''.join(response.iter_content(1)))
            raw['model']='gpt-5.4-mini-2026-03-17'
            from tests.unit.test_structured_provider import Response
            return Response(raw)
        def close(self): self.closed=True
    http=HTTP()
    import requests
    monkeypatch.setattr(requests,'Session',lambda:http)
    def run(config=cfg,approved=True):
        digest=launch.configuration_digest(config)
        access=token({'roles':['operator']})
        artifact,trust=approval_signer(config,verifier.verify(access))
        return launch.launch(config,digest,digest,access,'TEST-CREDENTIAL',
                             approval=artifact if approved else None,approval_trust=trust)
    return cfg,run,http,token,verifier


@pytest.mark.parametrize('auth,header,value',[('api_key','api-key','TEST-CREDENTIAL'),
                                             ('entra_bearer','Authorization','Bearer TEST-CREDENTIAL')])
def test_authorized_composition_with_intercepted_http(composition,auth,header,value):
    cfg,run,http,_,_=composition
    cfg=launch.LaunchConfiguration.model_validate({**cfg.model_dump(),'authentication':auth})
    result=run(cfg)
    assert result['job_state']=='COMPLETED' and result['questions']['status']=='COMPLETE'
    assert result['calls']==4 and len(result['run_records'])==4
    assert all(r['state']=='SETTLED' for r in result['governance_records'])
    assert len({r['identity'] for r in result['governance_records']})==4
    assert result['publication']['citations']==8
    assert cfg.generation_contract_sha256 == launch.generation_contract_digest()
    for _, kwargs in http.sent[:3]:
        control = json.loads(kwargs['json']['messages'][0]['content'].split('\nCONTROL\n')[1])
        assert control['profile']['template_version'] == 'managed-prompt/6'
        assert set(control['schema']['required']) == set(control['schema']['properties'])
    assert {json.loads(kwargs['json']['messages'][0]['content'].split('\nCONTROL\n')[1])
            ['profile']['stage'] for _, kwargs in http.sent[:3]} == {'chunk', 'structural', 'root'}
    for url,kwargs in http.sent:
        assert url==cfg.endpoint+'/chat/completions'
        assert kwargs['headers'][header]==value
        assert kwargs['allow_redirects'] is False
        assert kwargs['json']['model']==DEPLOYMENT
        assert kwargs['json']['reasoning_effort']=='low'
        assert kwargs['json']['max_completion_tokens']==3000
        response_format = kwargs['json']['response_format']
        if '\nCONTROL\n' in kwargs['json']['messages'][0]['content']:
            from documents.digestion.managed import generation_schema
            from llm.azure_schema import provider_schema
            assert response_format == {'type': 'json_schema', 'json_schema': {
                'name': 'polymind_stage_result', 'strict': True,
                'schema': provider_schema(generation_schema())}}
        else:
            # Interactive Q&A retains its separate JSON-object contract.
            assert response_format == {'type': 'json_object'}
    assert http.closed and http.trust_env is False
    question_system = http.sent[-1][1]['json']['messages'][0]['content']
    assert set(json.loads(question_system.split('\nOUTPUT_SCHEMA\n')[1])['required']) == {
        'answer', 'evidence_status', 'citation_ids'}
    assert (cfg.audit_directory/'financial-audit.json').is_file()
    packets=json.loads((cfg.audit_directory/'review-packets.json').read_text())
    assert packets[0]['independent_reviewer'] is None
    with pytest.raises(Exception): run(cfg)
    assert len(http.sent)==4  # Approval consumption and accounting survive reopening.


def test_missing_signed_approval_never_constructs_provider(composition):
    cfg,run,http,_,_=composition
    with pytest.raises(Exception):run(approved=False)
    assert not http.sent and not (cfg.audit_directory/'live-started.json').exists()


@pytest.mark.parametrize('change',[
    {'resource':'eci-foundry-dev-susanta'}, {'deployment':'eci-gpt-54-mini'},
    {'model':'gpt-4o'}, {'endpoint':'https://eci-foundry-dev-susanta.openai.azure.com/openai/v1'},
    {'quota_verified':False}, {'charges_verified':False}, {'actual_azure_tpm':10000},
    {'actual_azure_rpm':1}, {'authentication':'unknown'}, {'credential_valid_until':1},
])
def test_bad_configuration_refused(composition,change):
    cfg,_,http,_,_=composition
    with pytest.raises(Exception):launch.LaunchConfiguration.model_validate({**cfg.model_dump(),**change})
    assert not http.sent


@pytest.mark.parametrize('change',[{'approved':False},{'currency':'USD'},{'maximum':'0.01'},
                                   {'attempts':5},{'extra_cost':None}])
def test_financial_configuration_refused(composition,change):
    cfg,_,http,_,_=composition
    raw=cfg.model_dump();raw['contract'].update(change)
    with pytest.raises(Exception):launch.LaunchConfiguration.model_validate(raw)
    assert not http.sent


def test_unknown_usage_stops_and_survives_restart(composition,monkeypatch):
    cfg,run,http,_,_=composition
    monkeypatch.setattr(launch.OpenAICompatibleProvider,'_usage',staticmethod(lambda _:None))
    result=run()
    assert result['job_state']=='FAILED' and len(http.sent)==1
    audit=json.loads((cfg.audit_directory/'financial-audit.json').read_text())
    assert audit['run'][0]['finished'] is None and audit['governance'][0]['state']=='UNKNOWN'
    with pytest.raises(Exception):run()
    assert len(http.sent)==1


def test_configuration_hash_and_private_path(composition):
    cfg,_,_,token,verifier=composition
    digest=launch.configuration_digest(cfg)
    with pytest.raises(Exception):
        launch.verify_approval(cfg,digest,'0'*64,token({'roles':['operator'],'polymind_l1_approval':digest}),verifier)
    with pytest.raises(Exception):launch.private_path(__file__)


def test_default_command_is_offline(tmp_path,monkeypatch,capsys):
    import sys
    monkeypatch.setattr(sys,'argv',['foundry_l1','--output',str(tmp_path/'dry')])
    monkeypatch.setattr(launch,'launch',lambda *a:pytest.fail('Live path reached'))
    launch.main()
    assert json.loads(capsys.readouterr().out)['calls']==4


def test_timeout_keeps_financial_obligation(composition,monkeypatch):
    cfg,run,http,_,_=composition
    import requests
    def timeout(url,**kwargs):
        http.sent.append((url,kwargs))
        raise requests.Timeout('PRIVATE UPSTREAM DETAIL')
    monkeypatch.setattr(http,'post',timeout)
    result=run()
    assert result['job_state']=='FAILED' and len(http.sent)==1
    audit=(cfg.audit_directory/'financial-audit.json').read_text()
    assert 'PRIVATE UPSTREAM DETAIL' not in audit
    assert json.loads(audit)['governance'][0]['state']=='UNKNOWN'
    with pytest.raises(Exception):run()
    assert len(http.sent)==1


def test_changed_configuration_invalidates_signed_approval(composition):
    cfg,_,http,token,verifier=composition
    original=launch.configuration_digest(cfg)
    changed=launch.LaunchConfiguration.model_validate({**cfg.model_dump(),'authentication':'entra_bearer'})
    access=token({'roles':['operator'],'polymind_l1_approval':original})
    with pytest.raises(Exception):
        launch.verify_approval(changed,original,original,access,verifier)
    assert not http.sent


def test_audit_failure_still_closes_transport(composition,monkeypatch):
    cfg,run,http,_,_=composition
    from tests.performance import phase17h
    original=phase17h.write
    def fail_audit(path,value):
        if path.name=='financial-audit.json':
            raise OSError('disk unavailable')
        return original(path,value)
    monkeypatch.setattr(phase17h,'write',fail_audit)
    with pytest.raises(OSError):run()
    assert http.closed and len(http.sent)==4
    assert (cfg.audit_directory/'live-started.json').is_file()


def test_generation_contract_change_refused_before_approval_consumption(composition, monkeypatch):
    cfg, _, http, _, _ = composition
    monkeypatch.setattr(launch, 'generation_contract_digest', lambda: '0' * 64)
    with pytest.raises(ValueError):
        launch.launch(cfg, launch.configuration_digest(cfg), '', '', '')
    assert not http.sent
    assert not (cfg.audit_directory/'run.sqlite').exists()
    assert not (cfg.audit_directory/'live-started.json').exists()


def test_previous_generation_configuration_cannot_authorize_v5(composition):
    cfg, _, http, _, _ = composition
    previous = '00bf895290e1da2fb81372ff1ea921d8d7f464ea14f41110f54313d0423ad904'
    assert launch.generation_contract_digest() != previous
    with pytest.raises(ValueError, match='Reviewed generation contract'):
        launch.LaunchConfiguration.model_validate({**cfg.model_dump(),
            'generation_contract_sha256': previous})
    assert not http.sent
    assert not (cfg.audit_directory/'run.sqlite').exists()
    assert not (cfg.audit_directory/'live-started.json').exists()


def test_future_window_refused_before_authority_or_approval_access(composition):
    cfg, _, http, _, _ = composition
    cfg = launch.LaunchConfiguration.model_validate({**cfg.model_dump(),
        'execution_not_before': int(time.time()) + 1200})
    with pytest.raises(Exception):
        launch.launch(cfg, launch.configuration_digest(cfg), '', '', '')
    assert not http.sent
    assert not (cfg.audit_directory/'run.sqlite').exists()
    assert not (cfg.audit_directory/'live-started.json').exists()
