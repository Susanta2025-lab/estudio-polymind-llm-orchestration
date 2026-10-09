import asyncio
from types import SimpleNamespace

import pytest

from api.security import ApplicationSecurityMiddleware
from security.models import SecurityError
from tests.unit.test_security_identity import identity
from tests.unit.test_security_authority import secured


def run_middleware(runtime,token,path='/documents/analyze',downstream=None,body=b'{}',limit=1024):
    sent=[];consumed=[]
    async def app(scope,receive,send):
        consumed.append(await receive())
        await send({'type':'http.response.start','status':200,'headers':[]})
        await send({'type':'http.response.body','body':b'ok'})
    async def receive():return {'type':'http.request','body':body,'more_body':False}
    async def send(m):sent.append(m)
    conf=SimpleNamespace(authentication_mode='oidc_jwt',API_AUTH_ENABLED=False,MAX_REQUEST_BYTES=limit)
    headers=[] if token is None else [(b'authorization',('Bearer '+token).encode())]
    headers.append((b'content-length',str(len(body)).encode()))
    asyncio.run(ApplicationSecurityMiddleware(downstream or app,conf,runtime_getter=lambda:runtime)(
        {'type':'http','method':'POST','path':path,'headers':headers},receive,send))
    return sent,consumed


def test_verified_oidc_middleware_and_no_static_fallback(identity,tmp_path):
    from security.authority import SecurityAuthority
    verifier,token,_,_=identity
    runtime=SimpleNamespace(verifier=verifier,authority=SecurityAuthority(tmp_path/'auth.sqlite'))
    for credential in (None,'static-token','malformed'):
        sent,consumed=run_middleware(runtime,credential)
        assert sent[0]['status']==401 and not consumed
    sent,consumed=run_middleware(runtime,token())
    assert sent[0]['status']==200 and consumed
    sent,consumed=run_middleware(runtime,token(),body=b'x'*100,limit=50)
    assert sent[0]['status']==413 and not consumed


@pytest.mark.parametrize('path',['/documents/analyze','/documents/id/shares','/jobs/id','/usage','/memory/session'])
def test_all_new_protected_classes(path,identity,tmp_path):
    from security.authority import SecurityAuthority
    runtime=SimpleNamespace(verifier=identity[0],authority=SecurityAuthority(tmp_path/'auth.sqlite'))
    sent,consumed=run_middleware(runtime,None,path=path)
    assert sent[0]['status']==401 and not consumed


def test_stream_revocation_blocks_future_bytes_after_acknowledgement(secured):
    authority,(a,b,c,op),(x,y,z)=secured
    authority.share(a,x.document_id,b.scope.owner)
    runtime=SimpleNamespace(authority=authority,verifier=SimpleNamespace(verify=lambda token:b))
    async def downstream(scope,receive,send):
        scope['state']['release_snapshot']=authority.snapshot(b,(x.document_id,))
        await send({'type':'http.response.start','status':200,'headers':[]})
        await send({'type':'http.response.body','body':b'already delivered','more_body':True})
        authority.share(a,x.document_id,b.scope.owner,revoke=True)
        await send({'type':'http.response.body','body':b'future protected output','more_body':True})
        raise AssertionError('revoked stream continued')
    sent,_=run_middleware(runtime,'synthetic-fixture',downstream=downstream)
    data=b''.join(m.get('body',b'') for m in sent)
    assert data==b'already delivered'
    assert sent[-1]['more_body'] is False


def test_final_release_blocks_after_analysis_before_response_start(secured):
    authority,(a,b,c,op),(x,y,z)=secured
    authority.share(a,x.document_id,b.scope.owner)
    runtime=SimpleNamespace(authority=authority,verifier=SimpleNamespace(verify=lambda token:b))
    async def downstream(scope,receive,send):
        scope['state']['release_snapshot']=authority.snapshot(b,(x.document_id,))
        authority.share(a,x.document_id,b.scope.owner,revoke=True)
        await send({'type':'http.response.start','status':200,'headers':[]})
        await send({'type':'http.response.body','body':b'protected answer'})
    sent,_=run_middleware(runtime,'fixture',downstream=downstream)
    assert sent[0]['status']==403
    assert b'protected answer' not in b''.join(m.get('body',b'') for m in sent)


def test_oidc_legacy_api_fails_before_graph_or_stream(monkeypatch):
    from api import app as module
    monkeypatch.setattr(module.settings,'API_AUTH_MODE','oidc_jwt')
    monkeypatch.setattr(module.app_graph,'invoke',lambda *a:(_ for _ in ()).throw(AssertionError('graph called')))
    request=module.QueryRequest(query='private',session_id='other-user')
    for handler in (module.query,module.query_stream):
        with pytest.raises(SecurityError):handler(request)


def test_direct_graph_helpers_cannot_bypass_multiuser_policy(monkeypatch):
    from config.settings import settings
    from graph import generation
    from graph.nodes import router_node,create_direct_llm_node,create_rag_node
    monkeypatch.setattr(settings,'API_AUTH_MODE','oidc_jwt')
    def forbidden(*args,**kwargs):raise AssertionError('private data touched')
    provider=SimpleNamespace(generate=forbidden)
    memory=SimpleNamespace(get_history=forbidden,append_exchange=forbidden)
    state={'query':'q','session_id':'victim','model_role':'general','principal':{'owner':'victim'}}
    for node in (router_node,create_direct_llm_node(provider,memory),create_rag_node(provider,memory)):
        with pytest.raises(SecurityError):node(state)
    with pytest.raises(SecurityError):generation.rag_prompt_and_sources('q','victim',retrieve=forbidden)


def test_document_endpoint_static_auth_and_body_limit():
    from tests.unit.test_api_reliability import security_response
    assert security_response('/documents/analyze')[0]==401
    assert security_response('/documents/analyze','Bearer synthetic-api-token-that-is-long-enough')[0]==204
    assert security_response('/documents/analyze',enabled=False,body=b'x'*64,limit=32)[0]==413
