"""Explicit synthetic-only five-service validation; no ports or provider egress.

Requires a NEW temporary directory and a locally built application image.
Creates fixture keys only below that directory; never use its state for production.
"""
import argparse
import json
import pathlib
import subprocess
import time
from uuid import uuid4
import yaml
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', required=True, type=pathlib.Path)
parser.add_argument('--image', required=True)
parser.add_argument('--integration-tests', action='store_true', help='Explicit signed-test-permission Chat/Documents fixture')
args = parser.parse_args()
repo = pathlib.Path(__file__).resolve().parents[1]
base = args.root.absolute()
base.mkdir(mode=0o755, exist_ok=False)
image = args.image
def run(args, **kwargs):
    return subprocess.run(args, check=True, capture_output=True, text=True, **kwargs).stdout
# Dedicated directories only. Container root prepares numeric service ownership.
run(['docker','run','--rm','--user','0:0','--network','none','-v',str(base)+':/validation',image,'python','-c',
     "import os; from pathlib import Path;\nfor n,u in [('runtime',10001),('redis',999),('chroma',10001)]:\n p=Path('/validation')/n; p.mkdir(mode=0o700,exist_ok=True); os.chown(p,u,u)\n"])
# No real credential, Azure operation or external provider route.
if run(['docker','run','--rm','--network','none','-v',str(base/'runtime')+':/runtime',image,'python','-c',
        "from pathlib import Path; print(Path('/runtime/state').exists())"]).strip() == 'False':
    run(['docker','run','--rm','--network','none','-v',str(base/'runtime')+':/runtime',
         '-e','DOCUMENTS_PROFILE=synthetic','-e','DEPLOYMENT_ENV=compose',image,
         'python','-m','development.document_demo','initialize','/runtime/state'])
serve = '''import json, os, time
from pathlib import Path
from development.document_demo.runtime import build
from documents.operator.app import create_app
from rag.vector_store_factory import create_publication_vector_store
from documents.publication.encoding import RetrievalEncoder
from documents.publication.models import RetrievalProfile
from rag.reranker import get_reranker_model, rerank
from config.settings import settings
from filelock import FileLock
import uvicorn
root=Path('/runtime/state')
identity=json.loads((root/'identity.json').read_text())
lock=FileLock(str(root/'runtime.lock'),timeout=0); lock.acquire()
r,w,runner,_=build(root,fetch=lambda: {'keys':[identity['jwk']]})
started=time.monotonic()
w.pilot.publication.vectors=create_publication_vector_store(settings,administrative=True)
w.pilot.publication.encoder=RetrievalEncoder(RetrievalProfile())
get_reranker_model(); w.pilot.reranker=rerank
print('MODEL_LOADING_SECONDS='+str(time.monotonic()-started), flush=True)
uvicorn.run(create_app(r,w,runner),host='0.0.0.0',port=8001,access_log=False)
'''
if args.integration_tests:
    serve = "from tests.phase19_container_app import main\nmain()\n"
(base/'serve.py').write_text(serve)
workflow = '''import json, time
from pathlib import Path
import requests, jwt
root=Path('/runtime/state'); ident=json.loads((root/'identity.json').read_text())
claims=dict(iss=ident['issuer'],sub='operator',tid='synthetic',aud='polymind-documents',token_use='access',roles=['operator'],nbf=int(time.time())-1,exp=int(time.time())+3600)
token=jwt.encode(claims,(root/'signing.pem').read_bytes(),algorithm='RS256',headers={'kid':'fixture'})
s=requests.Session();s.trust_env=False;s.headers['Authorization']='Bearer '+token
url='http://127.0.0.1:8001/documents/operator'
def call(method,path,**kwargs):
 v=s.request(method,url+path,timeout=65,**kwargs);v.raise_for_status();return v.json()
sid=call('POST','/sessions',json=dict(source_approval_id='synthetic-1',request_key='docker-offline-create-0001'))['session_id']
call('POST','/sessions/'+sid+'/start')
for _ in range(100):
 status=call('GET','/sessions/'+sid)
 if status.get('job_state') in ('COMPLETED','FAILED','PARTIAL','CANCELLED'):break
 time.sleep(2)
assert status['digest_status']=='COMPLETE',status
call('POST','/sessions/'+sid+'/publish',json={'expected_job_id':status['job_id']})
packet=call('GET','/sessions/'+sid+'/digest')
print(json.dumps(dict(session=sid,state=status['job_state'],digest_status=status['digest_status'],usage=status['usage'],generation=packet['generation'],external_provider_attempts=0)))
'''
(base/'workflow.py').write_text("from tests.phase19_container_driver import main\nmain()\n" if args.integration_tests else workflow)
# Trusted enrollment before any authoritative runner starts.
enroll=workflow[:workflow.index('s=requests.Session()')] + "\nfrom development.document_demo.runtime import build\nr,w,runner,_=build(root,fetch=lambda:{'keys':[ident['jwk']]})\nr.authority.register(r.verifier.verify(token))\n"
run(['docker','run','--rm','--network','none','-v',str(base/'runtime')+':/runtime',
     '-e','DOCUMENTS_PROFILE=synthetic','-e','DEPLOYMENT_ENV=compose',image,'python','-c',enroll])

# Start with the actual hardened profile and change ONLY fixture inputs/entrypoints.
config=yaml.safe_load((repo/'docker-compose.phase19.yml').read_text())
config.pop('x-app',None)
sv=config['services']
for n in ('api','ui','gateway'):sv[n]['image']=image
for n in ('api','ui'):
    sv[n]['networks']=[x for x in sv[n]['networks'] if x!='egress']
sv['api']['command']=['python','/validation/serve.py']
sv['api']['working_dir']='/runtime/state'
sv['api']['volumes']=[dict(type='bind',source=str(base/'runtime'),target='/runtime',bind={'create_host_path':False}),dict(type='bind',source=str(base),target='/validation',read_only=True,bind={'create_host_path':False})]
if args.integration_tests:
    sv['api']['volumes'].append(dict(type='bind',source=str(repo/'tests'),target='/app/tests',read_only=True,bind={'create_host_path':False}))
sv['api']['environment'].update(DOCUMENTS_PROFILE='synthetic',DEPLOYMENT_ENV='compose',MEMORY_PROVIDER='redis',REDIS_URL='redis://redis:6379/0',VECTOR_STORE_PROVIDER='chroma_http',VECTOR_STORE_HOST='chroma')
sv['ui']['command']=['python','-m','streamlit','run','/app/ui/app.py','--server.address=0.0.0.0','--server.port=8501','--server.headless=true','--browser.gatherUsageStats=false','--server.fileWatcherType=none']
sv['ui']['environment'].update(DOCUMENTS_PROFILE='synthetic',DEPLOYMENT_ENV='compose',DOCUMENTS_API_URL='http://api:8001')
sv['ui']['volumes']=[dict(type='bind',source=str(base/'runtime/state/.streamlit/secrets.toml'),target='/tmp/.streamlit/secrets.toml',read_only=True,bind={'create_host_path':False})]
sv['gateway'].pop('ports')
sv['gateway']['environment']['PHASE19_ORIGIN']='https://polymind.private.example:9443'
for mount in sv['gateway']['volumes']:
    mount['source']=str(base/'runtime/state'/pathlib.Path(mount['target']).name)
for n in ('redis','chroma'):sv[n]['volumes'][0]['source']=str(base/n)
config['networks'].pop('egress')
path=base/'compose.yml';path.write_text(yaml.safe_dump(config))
compose=['docker','compose','-p','polymind19b-offline-'+uuid4().hex[:8],'-f',str(path)]
start=time.monotonic()
try:
    run(compose+['config','--quiet'])
    try:
        run(compose+['up','-d','--wait','--wait-timeout','240'])
    except subprocess.CalledProcessError as e:
        print(e.stdout, e.stderr, flush=True)
        print(run(compose+['logs','--no-color','--tail','50']),flush=True)
        raise
    print('READY_SECONDS='+str(time.monotonic()-start),flush=True)
    print(run(compose+['ps','--format','json']),flush=True)
    api=run(compose+['ps','-q','api']).strip()
    # Image contains no local dotenv, authorities, keys or private documents.
    run(['docker','exec',api,'python','-c',"from pathlib import Path; p=Path('/app'); assert not (p/'.env').exists(); assert not list(p.rglob('*.sqlite')); assert not list(p.rglob('*.pem')); assert not list(p.rglob('*.key')); "])
    ids=run(compose+['ps','-q']).split()
    print('IDLE_STATS='+run(['docker','stats','--no-stream','--format','{{json .}}',*ids]),flush=True)
    print('IMAGE='+run(['docker','image','inspect',image,'--format','{{.Size}}']),flush=True)
    process=subprocess.Popen(['docker','exec',api,'python','/validation/workflow.py'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    while process.poll() is None:
        print('WORK_STATS='+run(['docker','stats','--no-stream','--format','{{json .}}',*ids]),flush=True)
        time.sleep(8)
    stdout,stderr=process.communicate();print('WORKFLOW='+stdout,flush=True)
    if process.returncode:raise RuntimeError(stderr)
    print('MODEL_LOG='+run(compose+['logs','--no-color','api']),flush=True)
    run(compose+['stop','--timeout','90'])
    print('STOPPED='+run(compose+['ps','--all','--format','json']),flush=True)
finally:
    run(compose+['down','--timeout','90'])
