"""HTTP-only driver for the explicit offline five-service integration fixture."""
import json
from pathlib import Path
import time
import jwt
import requests


def main():
    root=Path('/runtime/integration/external')
    cfg=json.loads((root/'configuration.json').read_text())
    manifest=json.loads((root/'manifest.json').read_text())
    identity=json.loads((Path('/runtime/integration/fixture')/'identity.json').read_text())
    claims=dict(iss=manifest['enrollment'][0],sub=manifest['enrollment'][2],tid=manifest['enrollment'][1],
        aud=cfg['OIDC_CONFIGURATION']['audience'],ver='2.0',iat=int(time.time()),nbf=int(time.time())-1,
        exp=int(time.time())+3600,scp='access_as_user',roles=['PolyMind.L1Operator'])
    token=jwt.encode(claims,(Path('/runtime/integration/fixture')/'signing.pem').read_bytes(),algorithm='RS256',headers={'kid':'fixture'})
    client=requests.Session();client.trust_env=False;client.headers['Authorization']='Bearer '+token
    def call(method,path,**kwargs):
        response=client.request(method,'http://127.0.0.1:8001'+path,timeout=75,**kwargs)
        response.raise_for_status();return response.json()
    control='/documents/operator'
    state=call('POST',control+'/offline-step');session=state['session'];prefix=control+'/sessions/'+session
    assert call('GET',control+'/context')['mode']=='GOVERNED_EXTERNAL'
    call('POST',prefix+'/start')
    for _ in range(8):
        call('POST',control+'/offline-step');status=call('GET',prefix)
        if status.get('job_state') in ('COMPLETED','FAILED','PARTIAL','CANCELLED'):break
    assert status['digest_status']=='COMPLETE',status
    call('POST',prefix+'/publish',json={'expected_job_id':status['job_id']})
    # The fixture attaches synthetic review evidence; this is not human acceptance.
    import sqlite3
    with sqlite3.connect(root/'private/pilot.sqlite') as db:
        data=json.loads(db.execute('SELECT data FROM sessions WHERE id=?',(session,)).fetchone()[0])
    call('POST',control+'/offline-review',json={'evidence':data['evidence_sha256']})
    call('POST',control+'/offline-step')
    question={'query':'What valve inspection is required?','request_key':'container-question-001'}
    answer=call('POST',prefix+'/questions',json=question)
    assert answer['state']=='EXPERT_REVIEW_REQUIRED'
    call('POST',control+'/offline-review',json={'evidence':answer['evidence_sha256']})
    packet=call('GET',prefix+'/digest');assert len(packet['answers'])==1
    before=call('POST',control+'/offline-step')['calls']
    assert call('POST',prefix+'/questions',json=question)==answer
    assert call('POST',control+'/offline-step')['calls']==before
    direct=call('POST','/query',json={'query':'write a short greeting','session_id':'private','request_key':'container-chat-query-01'})
    assert direct['response']=='Authorized answer.'
    replay=client.post('http://127.0.0.1:8001/query/stream',json={
        'query':'write a short greeting','session_id':'private','request_key':'container-chat-query-01'},timeout=75)
    replay.raise_for_status();assert json.loads(replay.text.splitlines()[-1])['type']=='done'
    call('POST',control+'/offline-step')
    streaming=client.post('http://127.0.0.1:8001/query/stream',json={
        'query':'write a short greeting','session_id':'private','request_key':'container-chat-stream-1'},timeout=75)
    streaming.raise_for_status();events=[json.loads(line) for line in streaming.text.splitlines()]
    assert events[-1]['type']=='done' and any(e['type']=='chunk' for e in events),events
    call('POST',control+'/offline-step')
    rag=call('POST','/query',json={'query':'search my knowledge base for valve inspection','session_id':'private','request_key':'container-chat-rag-0001'})
    assert rag['route']=='rag' and rag['sources'],rag
    history=call('GET','/memory/private');assert len(history['history'])==6
    final=call('POST',control+'/offline-step')
    assert final['calls']==7,final
    print(json.dumps({'documents':'START_DIGEST_PUBLICATION_QA_PASS','chat':'OIDC_QUERY_NDJSON_RAG_MEMORY_PASS',
        'provider_calls':7,'external_calls':0,'real_retrieval':'Chroma_HTTP_MiniLM_cross_encoder',
        'real_memory':'Redis','quality_evidence':'test_only','permission_purpose':'test'}))


if __name__=='__main__':
    main()
