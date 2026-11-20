"""Real Entra middleware + signed test permissions + governed provider HTTP mocks."""
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID, uuid4

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient
import jwt
import pytest

from tests.integration.test_phase19_operator import external
from development.document_demo.fixtures import FixtureHTTP
from deployment.phase19.runtime import build
from deployment.phase19.storage import ownership
from documents.jobs.models import fingerprint
from documents.operator.app import create_app
from documents.pilot.models import ExecutionSessionApproval, SessionApproval
from security.execution import ExecutionPermissions, DocumentsExecutionPermission
from security.chat import ChatPolicy


class Body:
    status_code = 200
    headers = {}
    def __init__(self, raw):
        self.raw, self.closed = raw, False
    def iter_content(self, chunk_size):
        for i in range(0, len(self.raw), chunk_size):
            yield self.raw[i:i+chunk_size]
    def close(self):
        self.closed = True


class MockHTTP:
    def __init__(self):
        self.calls, self.requests, self.mode, self.hook = 0, [], 'ok', lambda: None
        self.fixture = FixtureHTTP()
    def post(self, url, **kwargs):
        self.calls += 1; self.requests.append(kwargs['json']); self.hook()
        if self.mode == 'timeout':
            import requests
            raise requests.Timeout('private upstream details')
        if self.mode == 'rate_limit':
            result = Body(b'upstream private body'); result.status_code = 429
            return result
        payload = kwargs['json']
        if payload['messages'][0]['content'].startswith('Answer the user.'):
            usage = dict(prompt_tokens=30, completion_tokens=40, total_tokens=70)
            if payload['stream']:
                events = [dict(model='offline-model', choices=[dict(delta={'content':token}, finish_reason=None)])
                          for token in ('Authorized ', 'answer.')]
                events.append(dict(model='offline-model', choices=[dict(delta={}, finish_reason='stop')]))
                if self.mode != 'no_usage':
                    events.append(dict(model='offline-model', choices=[], usage=usage))
                raw = ''.join('data: ' + json.dumps(e) + '\n\n' for e in events)
                if self.mode != 'truncated':
                    raw += 'data: [DONE]\n\n'
                return Body(raw.encode())
            result = dict(model='offline-model', choices=[dict(message={'content':'Authorized answer.'}, finish_reason='stop')])
            if self.mode != 'no_usage':result['usage']=usage
            return Body(json.dumps(result).encode())
        result = self.fixture.post('https://fixture.invalid/v1/chat/completions', **kwargs)
        if self.mode == 'no_usage':
            raw = b''.join(result.iter_content(1)); value = json.loads(raw); value.pop('usage')
            return Body(json.dumps(value).encode())
        return result


@pytest.fixture
def bridge(external, monkeypatch):
    root, old_runtime, old_workflow, _, _, token, identity = external
    clock = [time.time() + 1]
    doc_permission, chat_permission = uuid4(), uuid4()
    old = old_workflow.approvals[0]
    value = old.model_dump(mode='json')
    value.update(version='pilot-execution-session/2', zero_paid_execution=False,
        execution_permission=str(doc_permission), mode='external', consent='provided',
        consent_at=old.approved_at.isoformat(), exposure_approval='offline-exposure/1',
        privacy_approval='offline-privacy/1', quality_approval='offline-quality/1')
    approval = ExecutionSessionApproval.model_validate(value)
    manifest_path = root / 'manifest.json'; manifest = json.loads(manifest_path.read_text())
    manifest.update(execution_permissions=True, execution_authority_root=str(root/'permissions'), approvals=[approval.model_dump(mode='json')],
        chat=dict(permission_id=str(chat_permission), sessions=['private'],
            document_ids=[str(old_workflow.pilot.sources[old.source_approval].document_id)], output_tokens=1000,
            capability=dict(version='offline-chat/1', context_tokens=28000, max_output_tokens=3000,
                overhead_tokens=100, safety_tokens=100, streaming=True, usage_reporting=True, structured_output='prompt')))
    manifest_path.write_text(json.dumps(manifest))
    folder = root / 'permissions'; folder.mkdir(mode=0o700)
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public = key.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode()
    enrollment = manifest['enrollment']
    trust = dict(version='polymind-approval-trust/1', purpose='test', key_id='offline-independent', public_key_pem=public,
        operator_issuer=enrollment[0], operator_subject=enrollment[2], operator_tenant=enrollment[1], replay_directory=str(folder))
    (folder / 'trust.json').write_text(json.dumps(trust)); (folder / 'trust.json').chmod(0o600)
    (folder / 'revoked.json').write_text('[]'); (folder / 'revoked.json').chmod(0o600)
    # Test composition changes purpose, never signature verification or permission checks.
    import security.execution
    real = ExecutionPermissions
    monkeypatch.setattr(security.execution, 'ExecutionPermissions', lambda *a, **k: real(*a, **k, purpose='test', clock=lambda:clock[0]))
    from memory.memory_store import FileMemoryStore
    import memory.provider_factory
    monkeypatch.setattr(memory.provider_factory, 'create_memory_store', lambda cfg=None: FileMemoryStore(str(root / 'private/chat.json'), 20))
    with ownership(root):
        runtime, workflow, runner, cleanup = build(root)
    runtime.verifier.fetch = lambda: {'keys':[identity['jwk']]}
    for target in (runtime.authority, runtime.governance, runtime.admission, workflow.pilot, workflow.pilot.control):
        target.clock = lambda: clock[0]
    workflow.pilot.provider.http_client.close()
    http = MockHTTP(); workflow.pilot.provider.http_client = http; workflow.pilot.provider._owns_http_client = False
    workflow.pilot.reranker = lambda q, docs, top_k: docs[:top_k]
    runner.chat.reranker = workflow.pilot.reranker
    runner.chat.route = lambda q: 'rag' if 'valve' in q.lower() else 'tool' if 'calculate' in q else 'direct'
    runner.admission_ready = lambda: True
    permissions = workflow.pilot.execution_permission.permissions
    def sign(permission_id, grant_scopes, grant_resource, **changes):
        claims = dict(iss='polymind-independent-execution/1', aud='polymind-execution/1', jti=str(permission_id),
            iat=int(clock[0])-1, nbf=int(clock[0])-1, exp=int(clock[0])+1800, purpose='test',
            binding=fingerprint(permissions.binding()), scopes=grant_scopes, resource=grant_resource, max_calls=8)
        claims.update(changes)
        raw = jwt.encode(claims, key, algorithm='RS256', headers={'typ':'polymind-execution+jwt','kid':'offline-independent'})
        path = folder / (str(permission_id)+'.jwt'); path.write_text(raw); path.chmod(0o600)
        return claims
    source = workflow.pilot.sources[approval.source_approval]
    resource = DocumentsExecutionPermission.resource(approval, source)
    sign(doc_permission, ['documents_synthesis','documents_question'], resource)
    chat_resource = {'sessions':['private'], 'documents':[str(source.document_id)]}
    sign(chat_permission, ['chat'], chat_resource)
    client = TestClient(create_app(runtime, workflow, runner, run_worker=False, chat=runner.chat), raise_server_exceptions=True)
    client.headers['Authorization'] = 'Bearer ' + token()
    created = client.post('/documents/operator/sessions', json={'source_approval_id':source.approval_id,'request_key':'bridge-create-00000001'})
    assert created.status_code == 201, created.text
    session = created.json()['session_id']
    env = dict(root=root, runtime=runtime, workflow=workflow, runner=runner, chat=runner.chat, client=client,
        http=http, clock=clock, token=token, sign=sign, folder=folder, session=session,
        doc_permission=doc_permission, chat_permission=chat_permission, doc_resource=resource, chat_resource=chat_resource)
    yield env
    runner.close(); cleanup()


def finish(env):
    client, runner, clock, session = (env[k] for k in ('client','runner','clock','session'))
    prefix = '/documents/operator/sessions/' + session
    response = client.post(prefix+'/start'); assert response.status_code == 202, response.text
    for _ in range(10):
        clock[0] += 61; runner.once()
        response = client.get(prefix); assert response.status_code == 200, response.text
        if response.json().get('job_state') in {'COMPLETED','FAILED','PARTIAL','CANCELLED'}:break
    assert response.json()['digest_status']=='COMPLETE', response.text
    published = client.post(prefix+'/publish',json={'expected_job_id':response.json()['job_id']})
    assert published.status_code == 200,published.text
    attach_reviews(env, env['workflow'].pilot.review_packet(
        env['runtime'].verifier.verify(env['token']()), UUID(session))['evidence_sha256'])
    return prefix


def attach_reviews(env, evidence):
    from documents.pilot.models import ReviewFinding
    p = env['runtime'].verifier.verify(env['token']())
    for n in (1,2):
        env['workflow'].pilot.attach_review(p, UUID(env['session']), ReviewFinding(
            reviewer_code='offline-independent-'+str(n), evidence_sha256=evidence,
            findings_reference='offline-review-record/'+str(n), completed_at=datetime.fromtimestamp(int(env['clock'][0])-1,timezone.utc),
            qualified=True, independent=True, outcome='accepted'))


def test_documents_external_bridge_complete_question_replay_reload(bridge):
    e=bridge; prefix=finish(e); c=e['client']; e['clock'][0]+=61
    assert c.get('/documents/operator/context').json()['mode']=='GOVERNED_EXTERNAL'
    answer=c.post(prefix+'/questions',json={'query':'What valve inspection is required?','request_key':'bridge-question-000001'})
    assert answer.status_code==200,answer.text
    calls=e['http'].calls
    assert c.post(prefix+'/questions',json={'query':'What valve inspection is required?','request_key':'bridge-question-000001'}).json()==answer.json()
    assert e['http'].calls==calls==4
    status=c.get(prefix).json(); assert status['usage']['unsettled']==0 and status['usage']['synthetic'] is False
    e['workflow'].pilot._replicas.clear()
    assert c.post(prefix+'/reload').status_code==200
    pending=c.get(prefix+'/digest').json()
    assert pending['answers']==[] and pending['pending_answers']==[answer.json()]
    attach_reviews(e,answer.json()['evidence_sha256'])
    accepted=c.get(prefix+'/digest').json()['answers']
    assert len(accepted)==1 and accepted[0]['answer_id']==answer.json()['answer_id']
    assert accepted[0]['generation']==status['generation']
    assert e['http'].calls==calls
    with e['runtime'].governance.transaction() as db:
        assert db.execute("SELECT COUNT(*) FROM reservations WHERE state='SETTLED'").fetchone()[0]==4


@pytest.mark.parametrize('fault',['missing','expired','revoked','binding','scope','resource','signature'])
def test_documents_permission_denial_before_provider(bridge,fault):
    e=bridge; path=e['folder']/(str(e['doc_permission'])+'.jwt')
    if fault=='missing':path.unlink()
    elif fault=='revoked':(e['folder']/'revoked.json').write_text(json.dumps([str(e['doc_permission'])]))
    elif fault=='signature':path.write_text(path.read_text()[:-5]+'wrong')
    else:
        changes={'expired':{'exp':int(e['clock'][0])-1},'binding':{'binding':'0'*64},
            'scope':{'scopes':['chat']},'resource':{'resource':{'session':str(uuid4())}}}[fault]
        e['sign'](e['doc_permission'],['documents_synthesis','documents_question'],e['doc_resource'],**changes)
    c=e['client']; assert c.get('/documents/operator/context').json()['execution_enabled'] is False
    assert c.post('/documents/operator/sessions/'+e['session']+'/start').status_code==403
    assert e['http'].calls==0
    with e['runtime'].governance.transaction() as db:assert db.execute('SELECT COUNT(*) FROM reservations').fetchone()[0]==0


def test_historical_zero_paid_is_not_an_execution_session(bridge):
    e=bridge; source=next(iter(e['workflow'].pilot.sources.values()))
    old=e['workflow'].approvals[0].model_dump(mode='json');old.update(version='pilot-session/1',zero_paid_execution=True)
    old.pop('execution_permission'); approval=SessionApproval.model_validate(old)
    with pytest.raises(Exception):e['workflow'].pilot.execution_permission.authorize(
        e['runtime'].verifier.verify(e['token']()),approval,source,'documents_synthesis')
    assert e['http'].calls==0


def test_documents_revalidate_after_admission_before_dispatch(bridge,monkeypatch):
    e=bridge; prefix='/documents/operator/sessions/'+e['session']
    assert e['client'].post(prefix+'/start').status_code==202
    original=e['runtime'].admission.acquire
    def revoke(*args,**kwargs):
        ticket=original(*args,**kwargs)
        (e['folder']/'revoked.json').write_text(json.dumps([str(e['doc_permission'])]))
        return ticket
    monkeypatch.setattr(e['runtime'].admission,'acquire',revoke)
    for _ in range(3):
        e['clock'][0]+=61;e['runner'].once()
    assert e['http'].calls==0
    with e['runtime'].governance.transaction() as db:
        assert db.execute('SELECT state FROM reservations').fetchone()[0]=='RELEASED'


@pytest.mark.parametrize('mode',['no_usage','timeout'])
def test_documents_unknown_never_retries(bridge,mode):
    e=bridge;e['http'].mode=mode
    prefix='/documents/operator/sessions/'+e['session']
    assert e['client'].post(prefix+'/start').status_code==202
    for _ in range(3):e['clock'][0]+=61;e['runner'].once()
    assert e['http'].calls==1
    with e['runtime'].governance.transaction() as db:
        assert db.execute('SELECT state FROM reservations').fetchone()[0]=='UNKNOWN'
    e['client'].post(prefix+'/start');e['runner'].once();assert e['http'].calls==1


def test_chat_oidc_langgraph_stream_memory_rag_and_replay(bridge):
    e=bridge;c=e['client']
    payload={'query':'hello','session_id':'private','request_key':'chat-query-00000001'}
    response=c.post('/query',json=payload);assert response.status_code==200,response.text
    assert response.json()['response']=='Authorized answer.'
    calls=e['http'].calls;assert c.post('/query',json=payload).json()==response.json();assert e['http'].calls==calls
    e['clock'][0]+=61
    streaming=c.post('/query/stream',json={**payload,'request_key':'chat-stream-0000001'})
    assert streaming.status_code==200,streaming.text
    events=[json.loads(line) for line in streaming.text.splitlines()]
    assert [v['type'] for v in events]==['metadata','chunk','chunk','done']
    assert events[-1]['response']=='Authorized answer.'
    history=c.get('/memory/private');assert history.status_code==200,history.text
    assert len(history.json()['history'])==4
    prefix=finish(e);e['clock'][0]+=61
    rag=c.post('/query',json={'query':'What valve inspection?','session_id':'private','request_key':'chat-rag-0000000001'})
    assert rag.status_code==200,rag.text
    assert rag.json()['route']=='rag' and rag.json()['sources']
    assert 'Valve inspection' in e['http'].requests[-1]['messages'][1]['content']
    assert not e['workflow'].pilot.provider.pilot_fixture if hasattr(e['workflow'].pilot.provider,'pilot_fixture') else True


@pytest.mark.parametrize('claims',[None,{'exp':1},{'sub':'other'},{'tid':'foreign'},{'roles':['admin']},{'token_use':'id'}])
def test_chat_identity_and_memory_denied(bridge,claims):
    e=bridge;c=e['client']
    if claims is None:c.headers.pop('Authorization')
    else:c.headers['Authorization']='Bearer '+e['token'](**claims)
    for path in ('/query','/query/stream'):
        r=c.post(path,json={'query':'hello','session_id':'private','request_key':'denied-chat-0000001'})
        assert r.status_code in {401,403},r.text
    assert c.get('/memory/private').status_code in {401,403}
    assert e['http'].calls==0


@pytest.mark.parametrize('fault',['missing','expired','revoked','binding','scope','session'])
def test_chat_permission_denied(bridge,fault):
    e=bridge;c=e['client'];session='private'
    if fault=='missing':(e['folder']/(str(e['chat_permission'])+'.jwt')).unlink()
    elif fault=='revoked':(e['folder']/'revoked.json').write_text(json.dumps([str(e['chat_permission'])]))
    elif fault=='session':session='foreign'
    else:
        changes={'expired':{'exp':int(e['clock'][0])-1},'binding':{'binding':'0'*64},'scope':{'scopes':['documents_question']}}[fault]
        e['sign'](e['chat_permission'],['chat'],e['chat_resource'],**changes)
    r=c.post('/query',json={'query':'hello','session_id':session,'request_key':'permission-chat-0001'})
    assert r.status_code==403,r.text
    assert e['http'].calls==0


@pytest.mark.parametrize('mode',['no_usage','timeout','truncated','rate_limit'])
def test_chat_unknown_and_provider_errors_never_retry(bridge,mode):
    e=bridge;e['http'].mode=mode;c=e['client']
    payload={'query':'hello','session_id':'private','request_key':'uncertain-chat-00001'}
    response=c.post('/query/stream',json=payload)
    assert response.status_code==200 and '"type": "error"' in response.text
    assert '"type": "done"' not in response.text
    c.post('/query/stream',json=payload)
    c.post('/query',json={**payload,'request_key':'fresh-chat-00000001'})
    assert e['http'].calls==1
    assert c.get('/memory/private').json()['history']==[]
    with e['runtime'].governance.transaction() as db:assert db.execute('SELECT state FROM reservations').fetchone()[0]=='UNKNOWN'


def test_chat_document_revocation_blocks_history_and_retrieval(bridge):
    e=bridge;finish(e);e['clock'][0]+=61;c=e['client']
    r=c.post('/query',json={'query':'What valve inspection?','session_id':'private','request_key':'revocation-chat-0001'})
    assert r.status_code==200,r.text
    p=e['runtime'].verifier.verify(e['token']());source=next(iter(e['workflow'].pilot.sources.values()))
    e['runtime'].authority.tombstone(p,source.document_id)
    assert c.get('/memory/private').status_code==403
    assert c.post('/query',json={'query':'hello','session_id':'private','request_key':'after-revoke-0000001'}).status_code==403


def test_chat_shared_provider_admission_denial_releases_reservation(bridge):
    from llm.admission import CallIdentity
    from llm.inference import InferenceUsage
    e=bridge;p=e['runtime'].verifier.verify(e['token']())
    admission=e['runtime'].admission
    tickets=[]
    for workload in ('INTERACTIVE','DOCUMENT_BACKGROUND'):
        identity=CallIdentity(p.scope.identity(),uuid4(),uuid4(),1,'other-consumer/1',
            'openai_compatible','general','offline-model','offline-chat/1')
        tickets.append(admission.acquire(identity,1,1,workload))
    try:
        r=e['client'].post('/query',json={'query':'hello','session_id':'private','request_key':'admission-chat-00001'})
        assert r.status_code==503,r.text
        assert e['http'].calls==0
        with e['runtime'].governance.transaction() as db:
            assert db.execute('SELECT state FROM reservations').fetchone()[0]=='RELEASED'
    finally:
        for ticket in tickets:admission.finish(ticket,usage=InferenceUsage(1,1,2),outcome='success')


def test_chat_financial_request_limit_denies_before_provider(bridge):
    from llm.admission import CallIdentity
    from llm.inference import InferenceUsage
    e=bridge;p=e['runtime'].verifier.verify(e['token']());ledger=e['runtime'].governance
    for _ in range(ledger.policy.owner.requests_per_window):
        identity=CallIdentity(p.scope.identity(),uuid4(),uuid4(),1,'historical-test/1',
            'openai_compatible','general','offline-model','offline-chat/1')
        ticket=ledger.reserve(p,identity,0,1)
        ledger.transition(ticket,'RESERVED','ADMITTING');ledger.transition(ticket,'ADMITTING','STARTED')
        ledger.settle(ticket,InferenceUsage(0,0,0))
    r=e['client'].post('/query',json={'query':'hello','session_id':'private','request_key':'budget-chat-00000001'})
    assert r.status_code==429,r.text
    assert e['http'].calls==0


def test_permission_consumption_survives_reopen_and_enforces_call_bound(bridge):
    e=bridge;c=e['client']
    e['sign'](e['chat_permission'],['chat'],e['chat_resource'],max_calls=1)
    payload={'query':'hello','session_id':'private','request_key':'one-call-chat-000001'}
    assert c.post('/query',json=payload).status_code==200
    e['clock'][0]+=61
    assert c.post('/query',json={**payload,'request_key':'second-call-chat-001'}).status_code==403
    assert e['http'].calls==1
    from documents.operator.actions import Actions
    restored=Actions(e['root']/'private/actions.sqlite')
    with restored.transaction() as db:
        assert db.execute('SELECT COUNT(*) FROM actions WHERE action=?',('execution/'+str(e['chat_permission']),)).fetchone()[0]==1


def test_expired_source_denies_chat_memory_and_generation(bridge):
    e=bridge;e['clock'][0]=max(s.expires_at.timestamp() for s in e['workflow'].pilot.sources.values())+1
    # Renew only test identity/grant, retaining the expired source approval.
    e['client'].headers['Authorization']='Bearer '+e['token'](exp=int(e['clock'][0])+3600)
    e['sign'](e['chat_permission'],['chat'],e['chat_resource'])
    assert e['client'].get('/memory/private').status_code==403
    assert e['http'].calls==0


def test_chat_revalidates_permission_after_admission(bridge,monkeypatch):
    e=bridge; original=e['runtime'].admission.acquire
    def revoke(*args,**kwargs):
        ticket=original(*args,**kwargs)
        (e['folder']/'revoked.json').write_text(json.dumps([str(e['chat_permission'])]))
        return ticket
    monkeypatch.setattr(e['runtime'].admission,'acquire',revoke)
    r=e['client'].post('/query',json={'query':'hello','session_id':'private','request_key':'dispatch-chat-000001'})
    assert r.status_code==403,r.text
    assert e['http'].calls==0
    with e['runtime'].governance.transaction() as db:
        assert db.execute('SELECT state FROM reservations').fetchone()[0]=='RELEASED'


def test_legacy_record_cannot_be_relabelled_as_paid(bridge):
    from documents.pilot.models import parse_session_approval
    e=bridge
    record=e['workflow'].approvals[0].model_dump(mode='json')
    record['zero_paid_execution']=True
    with pytest.raises(ValueError):parse_session_approval(record)
    assert e['http'].calls==0


def test_full_composition_reopen_preserves_accepted_answers_and_permissions(bridge):
    e=bridge; prefix=finish(e);e['clock'][0]+=61
    answer=e['client'].post(prefix+'/questions',json={'query':'What valve inspection?','request_key':'restart-question-001'})
    assert answer.status_code==200,answer.text
    attach_reviews(e,answer.json()['evidence_sha256'])
    before=e['client'].get(prefix+'/digest').json()['answers'];calls=e['http'].calls
    e['runner'].close()
    with ownership(e['root']):
        runtime,workflow,runner,cleanup=build(e['root'])
    runtime.verifier.fetch=e['runtime'].verifier.fetch
    for target in (runtime.authority,runtime.governance,runtime.admission,workflow.pilot,workflow.pilot.control):
        target.clock=lambda:e['clock'][0]
    workflow.pilot.provider.http_client.close();workflow.pilot.provider.http_client=e['http'];workflow.pilot.provider._owns_http_client=False
    try:
        assert not runner.grants
        client=TestClient(create_app(runtime,workflow,runner,run_worker=False,chat=runner.chat))
        client.headers['Authorization']='Bearer '+e['token']()
        assert client.post(prefix+'/reload').status_code==200
        assert client.get(prefix+'/digest').json()['answers']==before
        assert e['http'].calls==calls
    finally:runner.close();cleanup()


@pytest.mark.parametrize('change',['model','capability','endpoint'])
def test_unsigned_runtime_changes_cannot_reuse_permission(bridge,change):
    e=bridge
    if change=='model':e['workflow'].pilot.provider.model_map['general']='unapproved-model'
    elif change=='endpoint':e['workflow'].pilot.provider.url='https://other.invalid/v1/chat/completions'
    else:e['chat'].policy=e['chat'].policy.model_copy(update={'output_tokens':2000})
    r=e['client'].post('/query',json={'query':'hello','session_id':'private','request_key':'mismatch-chat-000001'})
    assert r.status_code==403,r.text
    assert e['http'].calls==0


def test_test_purpose_grant_cannot_satisfy_production_verifier(bridge,monkeypatch):
    from types import SimpleNamespace
    import os
    from security.models import SecurityError
    e=bridge;gate=e['workflow'].pilot.execution_permission.permissions
    live=type(gate)(gate.root,gate.trust_path,gate.actions,gate.authority,gate.binding,purpose='live',ledger=gate.ledger)
    p=e['runtime'].verifier.verify(e['token']())
    # Check purpose separately from the production read-only-mount requirement.
    monkeypatch.setattr(os,'statvfs',lambda path:SimpleNamespace(f_flag=os.ST_RDONLY))
    with pytest.raises(SecurityError):live.check(p,e['chat_permission'],'chat',e['chat_resource'])
    assert e['http'].calls==0


@pytest.mark.parametrize('plane',['chat','documents'])
def test_insufficient_permission_window_denied_before_provider(bridge,plane):
    e=bridge
    if plane=='chat':
        e['sign'](e['chat_permission'],['chat'],e['chat_resource'],exp=int(e['clock'][0])+10)
        r=e['client'].post('/query',json={'query':'hello','session_id':'private','request_key':'short-window-chat-001'})
        assert r.status_code==403,r.text
    else:
        e['sign'](e['doc_permission'],['documents_synthesis','documents_question'],e['doc_resource'],exp=int(e['clock'][0])+10)
        assert e['client'].get('/documents/operator/context').json()['execution_enabled'] is False
        r=e['client'].post('/documents/operator/sessions/'+e['session']+'/start')
        assert r.status_code==403,r.text
    assert e['http'].calls==0


@pytest.mark.parametrize('first',['/query','/query/stream'])
def test_chat_intent_is_idempotent_across_transports(bridge,first):
    e=bridge;payload={'query':'hello','session_id':'private','request_key':'same-intent-both-0001'}
    response=e['client'].post(first,json=payload)
    assert response.status_code==200,response.text
    other='/query/stream' if first=='/query' else '/query'
    replay=e['client'].post(other,json=payload)
    assert replay.status_code==200,replay.text
    if other=='/query/stream':
        events=[json.loads(line) for line in replay.text.splitlines()]
        assert events[-1]=={'type':'done','response':'Authorized answer.'}
    else:assert replay.json()['response']=='Authorized answer.'
    assert e['http'].calls==1
    assert len(e['client'].get('/memory/private').json()['history'])==2


def test_exhausted_document_permission_disables_new_question(bridge):
    e=bridge
    e['sign'](e['doc_permission'],['documents_synthesis','documents_question'],e['doc_resource'],max_calls=3)
    prefix=finish(e)
    assert e['client'].get(prefix).json()['question_enabled'] is False
    result=e['client'].post(prefix+'/questions',json={'query':'What valve?','request_key':'exhausted-question-01'})
    assert result.status_code==403,result.text
    assert e['http'].calls==3


def test_exhausted_chat_permission_disables_input_but_preserves_reads_and_replay(bridge):
    e=bridge
    e['sign'](e['chat_permission'],['chat'],e['chat_resource'],max_calls=1)
    payload={'query':'hello','session_id':'private','request_key':'exhausted-chat-00001'}
    first=e['client'].post('/query',json=payload);assert first.status_code==200
    assert e['client'].get('/chat/context').json()['execution_enabled'] is False
    assert e['client'].get('/memory/private').status_code==200
    assert e['client'].post('/query',json=payload).json()==first.json()
    assert e['http'].calls==1
