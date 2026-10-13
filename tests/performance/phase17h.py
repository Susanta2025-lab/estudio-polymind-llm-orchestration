"""Run explicitly: python -m tests.performance.phase17h --output /tmp/NAME.

Synthetic offline benchmark; subprocess limits are harness limits, not production
parser isolation. No model factory, network client or configured storage is used.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from io import BytesIO
import json
import os
from pathlib import Path
import platform
import resource
import shutil
import subprocess
import sys
import time
from uuid import UUID

from tests.performance.fixtures import FACTS, NOW, SCOPE, pdf, profile


def write(path, value):
    pending = path.with_suffix(path.suffix + '.pending')
    pending.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    pending.replace(path)


def inventory(root):
    count = size = 0
    for path in root.rglob('*'):
        try:
            if path.is_file():
                size += path.stat().st_size
                count += 1
        except FileNotFoundError:
            continue  # SQLite journals and ObjectStore pending files are transient.
    return {'files':count, 'bytes':size}


class CountingStore:
    def __init__(self, store):
        self.store, self.counts = store, Counter()
    def read(self, *args, **kwargs):
        data = self.store.read(*args, **kwargs)
        self.counts['read_calls'] += 1; self.counts['read_bytes'] += len(data)
        return data
    def inspect(self, *args, **kwargs):
        self.counts['inspect_calls'] += 1
        return self.store.inspect(*args, **kwargs)
    def put(self, *args, **kwargs):
        self.counts['put_calls'] += 1
        return self.store.put(*args, **kwargs)


class SyntheticModel:
    """Constant fake vectors: measures plumbing, never semantic dense relevance."""
    max_seq_length = 256
    class Tokenizer:
        model_max_length = 512
        def __call__(self, text, **kwargs):
            if kwargs.get('truncation') is not False:
                raise AssertionError('truncation forbidden')
            return {'input_ids':list(range(len(text)+2))}
    tokenizer = Tokenizer()
    def __init__(self): self.calls = 0
    def get_sentence_embedding_dimension(self): return 384
    def encode(self, text, **kwargs):
        self.calls += 1
        class Vector:
            def tolist(self): return [1.] + [0.] * 383
        return Vector()


class SyntheticVectors:
    def __init__(self): self.rows = {}; self.query_seconds = []
    def upsert(self, ids, documents, embeddings, metadatas):
        from rag.vector_store import VectorDocument
        for key, text, meta in zip(ids, documents, metadatas):
            self.rows[key] = VectorDocument(text, meta)
    def list_documents(self, *, scope=None):
        return [r for r in self.rows.values() if scope is None or (
            r.metadata['generation'] == scope.generation and
            (not scope.document_ids or r.metadata['document_id'] in scope.document_ids))]
    def similarity_search(self, embedding, limit, *, scope=None):
        from rag.vector_store import VectorMatch
        started = time.perf_counter()
        result = [VectorMatch(r.document,r.metadata,.1) for r in self.list_documents(scope=scope)[:limit]]
        self.query_seconds.append(time.perf_counter()-started)
        return result


def measure(samples):
    import statistics
    ordered = sorted(samples)
    return {'n':len(samples), 'median_seconds':statistics.median(samples) if samples else None,
            'p95_seconds':ordered[__import__('math').ceil(.95*len(samples))-1] if len(samples)>=100 else None,
            'max_seconds':max(samples) if samples else None,
            'p95_status':'observed nearest-rank' if len(samples)>=100 else 'NOT ESTABLISHED: fewer than 100 samples'}


def execute_case(root, pages, config):
    from documents.config import ExtractionSettings
    from documents.errors import DocumentError
    from documents.extraction import extract
    from documents.serialization import serialize, deserialize
    from documents.storage import LocalObjectStore
    from documents.digestion.codec import encode
    from documents.digestion.inference import FakeInference, Fixture
    from documents.digestion.planning import build_plan
    from documents.digestion.validation import EvidenceIndex
    from documents.digestion.workflow import prepare, admit, DigestionHandler, classify_digestion, load_digest
    from documents.jobs.models import JobSettings
    from documents.jobs.sqlite import SQLiteJobLedger
    from documents.jobs.worker import LocalDispatcher, Worker, relay
    root.mkdir(parents=True, exist_ok=True)
    wall, cpu = time.perf_counter(), time.process_time()
    result = {'version':config['version'], 'pages':pages, 'run_count':1, 'concurrency':1,
              'model':'deterministic fake', 'embedding':'constant fake', 'status':'RUNNING',
              'limits':config, 'timings':{}, 'failures':[], 'phase':'fixture'}
    def save():
        result.update(elapsed_seconds=time.perf_counter()-wall, cpu_seconds=time.process_time()-cpu,
                      peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                      disk=inventory(root))
        write(root/'result.json',result)
    def timed(name, function):
        result['phase']=name; save(); start=time.perf_counter()
        value=function(); result['timings'][name]=time.perf_counter()-start; save(); return value
    try:
        raw, manifest = timed('fixture',lambda:pdf(pages,seed=config['seed'],lines_per_page=config['lines_per_page']))
        if len(raw)>config['max_fixture_bytes']: raise ValueError('fixture_budget')
        (root/'source.pdf').write_bytes(raw); write(root/'fixture.json',manifest)
        result['fixture']={k:v for k,v in manifest.items() if k!='expected'}
        store=CountingStore(LocalObjectStore(root/'objects'))
        limits=ExtractionSettings(max_source_bytes=16000000,max_pages=1000,max_characters=4000000,
                                  max_blocks=100000,max_artifact_bytes=32000000)
        try:
            artifact,ref=timed('extraction',lambda:extract(BytesIO(raw),scope=SCOPE,document_id=UUID(int=pages),
                display_filename='manual.pdf',declared_mime='application/pdf',store=store,limits=limits,
                created_at=NOW,extracted_at=NOW))
        except DocumentError as exc:
            if pages==1001 and exc.category=='page_limit_exceeded':
                result['status']='EXPECTED_REFUSAL'; result['refusal']=exc.category
                return result
            raise
        assert [u.physical_page for u in artifact.units]==list(range(1,pages+1))
        for unit,expected in zip(artifact.units,manifest['expected']):
            assert unit.text.splitlines()==expected['lines'], 'silent native text loss'
        data=serialize(artifact)
        assert serialize(deserialize(data))==data and sha256(data).hexdigest()==ref.sha256
        result['extraction']={'unit_statuses':dict(Counter(u.status for u in artifact.units)),
            'characters':sum(len(u.text) for u in artifact.units), 'artifact_bytes':ref.byte_size,
            'sha256':ref.sha256,'accounted_pages':len(artifact.units)}
        fake=FakeInference(tuple(Fixture(block_id=artifact.units[n-1].blocks[0].block_id,
            text=text, qualification='Only in 2025 and the specified load regime.' if n in (5,180) else None,
            subject='orion-performance' if n in (5,180) else None,
            stance='affirmed' if n==5 else 'denied' if n==180 else 'unknown')
            for n,text in FACTS.items() if n<=pages))
        chosen=profile(inference_config=fake.config)
        plan,plan_ref=timed('planning',lambda:prepare(artifact,ref,chosen,store))
        assert encode(build_plan(artifact,ref,chosen))==encode(plan)
        index=EvidenceIndex(artifact)
        pieces=[p for c in plan.chunks for p in c.pieces]
        assert ''.join(p.text for p in pieces)==''.join(u.text for u in artifact.units)
        assert all(index.resolve(p.evidence)==p.text for p in pieces)
        result['plan']={'chunks':len(plan.chunks),'reducers':len(plan.reducers),
            'depth':max(n.level for n in plan.reducers),'max_fan_in':max(len(n.children) for n in plan.reducers),
            'steps':len(plan.chunks)+len(plan.reducers)+2,'bytes':plan_ref.byte_size,
            'structure_bytes':len(encode(plan.structure)), 'eligible':len(plan.eligible),
            'max_estimated_input':max([c.estimated_tokens for c in plan.chunks]+[n.estimated_tokens for n in plan.reducers]),
            'profile':chosen.model_dump(mode='json')}
        ledger=SQLiteJobLedger(JobSettings(database_path=root/'jobs.sqlite',lease_seconds=config['worker_timeout_seconds']))
        job=timed('admission',lambda:admit(ledger,store,plan,plan_ref,request_key='phase17h'))
        queue=LocalDispatcher()
        worker=Worker(ledger,queue,store,DigestionHandler(ledger,plan_ref,fake),owner='benchmark',classifier=classify_digestion)
        def pump():
            for _ in range(chosen.max_steps+1):
                relay(ledger,queue)
                if not worker.once(): break
            assert ledger.get_job(SCOPE,job.job_id).state=='COMPLETED'
            return load_digest(ledger,store,SCOPE,job.job_id)
        digest=timed('digestion',pump)
        assert digest.status=='COMPLETE' and set(digest.coverage.included)==set(plan.eligible)
        assert not digest.coverage.failed and not digest.coverage.unsupported
        assert len(digest.evidence)==len(pieces)
        if pages>=180:
            assert digest.contradictions and len(digest.qualifications)==2
        steps=ledger.steps(SCOPE,job.job_id)
        result['digest']={'status':digest.status,'coverage':digest.coverage.fraction,
            'included':len(digest.coverage.included),'evidence':len(digest.evidence),
            'qualifications':len(digest.qualifications),'contradictions':len(digest.contradictions),
            'checkpoint_count':len(digest.checkpoints),'bytes':len(encode(digest)),
            'accepted_steps':len(steps),'attempts':sum(s.attempt_count for s in steps),
            'provider_calls':sum(fake.calls.values()),'sqlite_bytes':ledger.path.stat().st_size}
        result['object_io_before_publication']=dict(store.counts)
        benchmark_publication(root,ledger,store,job,config,result,timed)
        result['object_io_total']=dict(store.counts)
        result['objects']=inventory(root/'objects')
        result['status']='PASS'
    except Exception as exc:
        result['status']='FAIL'
        result['failures'].append({'phase':result['phase'],'type':type(exc).__name__,
            'category':getattr(exc,'category',None)})
        raise
    finally:
        save()
    return result


def benchmark_publication(root, ledger, store, job, config, result, timed):
    from documents.publication.authority import SQLitePublicationAuthority
    from documents.publication.encoding import RetrievalEncoder
    from documents.publication.models import RetrievalProfile
    from documents.publication.service import PublicationService
    from documents.publication.retrieval import PublicationReplica
    model=SyntheticModel(); vectors=SyntheticVectors()
    service=PublicationService(SQLitePublicationAuthority(root/'publication.sqlite'),store,ledger,vectors,
                               RetrievalEncoder(RetrievalProfile(),model),SCOPE)
    manifest=timed('publication_plan',lambda:service.plan([job.job_id]))
    timed('publication_prepare',lambda:service.prepare(manifest.generation))
    timed('publication_activation',lambda:service.activate(manifest.generation))
    replica=PublicationReplica(service,manifest.generation)
    timed('generation_load',replica.load)
    assert timed('readiness',replica.ready)
    retrieval,citations,pins=[],[],[]
    hits=[]
    for _ in range(config['query_samples']):
        start=time.perf_counter(); pin=replica.pin((job.admission.document_id,)); pins.append(time.perf_counter()-start)
        start=time.perf_counter(); hits=replica.retrieve('ORION performance',pin,top_k=8,
            reranker=lambda q,docs,top_k:docs[:top_k]); retrieval.append(time.perf_counter()-start)
        start=time.perf_counter(); refs=replica.citations(pin,hits); citations.append(time.perf_counter()-start)
        assert all(c.document_id==job.admission.document_id and 1<=c.physical_page<=result['pages'] for c in refs)
    result['publication']={'records':len(manifest.records),'vector_rows':len(vectors.rows),
        'manifest_bytes':len(__import__('documents.digestion.codec',fromlist=['encode']).encode(manifest)),
        'embedding_calls':model.calls, 'pin':measure(pins),'retrieval':measure(retrieval),
        'dense_fake':measure(vectors.query_seconds),'citations':measure(citations),
        'warmup':'generation loaded; no query discarded', 'failures':0,
        'retrieved_record_ids':[h['record_id'] for h in hits]}


def configuration(path):
    config=json.loads(path.read_text())
    if (config['version']!='phase17h/1' or not config['pages'] or len(config['pages'])>5
            or any(type(p) is not int or p not in (4,200,500,1000,1001) for p in config['pages'])
            or len(set(config['pages']))!=len(config['pages'])):
        raise ValueError('invalid page matrix')
    bounds={'max_fixture_bytes':(1,16000000),'max_seconds':(1,600),
        'max_address_bytes':(128*1024**2,4*1024**3),'max_disk_bytes':(1024,2*1024**3),
        'max_files':(1,10000),'query_samples':(1,100),'lines_per_page':(2,40),
        'worker_timeout_seconds':(1,600)}
    for key,(low,high) in bounds.items():
        if type(config[key]) is not int or not low<=config[key]<=high:
            raise ValueError('invalid resource budget')
    return config


def main():
    parser=argparse.ArgumentParser(__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--config',type=Path,default=Path('tests/fixtures/phase17h/profile.json'))
    parser.add_argument('--child',type=int)
    args=parser.parse_args(); config=configuration(args.config)
    root=args.output.resolve()
    if args.child is not None:
        resource.setrlimit(resource.RLIMIT_AS,(config['max_address_bytes'],config['max_address_bytes']))
        resource.setrlimit(resource.RLIMIT_CPU,(config['max_seconds'],config['max_seconds']+1))
        resource.setrlimit(resource.RLIMIT_FSIZE,(config['max_disk_bytes'],config['max_disk_bytes']))
        execute_case(root,args.child,config); return
    if root.exists(): raise ValueError('choose a new output directory; existing results are never overwritten')
    # Keep generated PDFs/database artifacts outside this checkout.
    if root.is_relative_to(Path.cwd().resolve()): raise ValueError('output must be outside repository')
    root.mkdir(parents=True)
    write(root/'environment.json',{'python':platform.python_version(),'platform':platform.platform(),
        'cpu_count':os.cpu_count(),'memory':Path('/proc/meminfo').read_text(),
        'disk':shutil.disk_usage(root)._asdict(),'profile_sha256':sha256(args.config.read_bytes()).hexdigest(),
        'pypdf':__import__('pypdf').__version__, 'started_utc':datetime.now(timezone.utc).isoformat()})
    write(root/'profile.json',config)
    results=[]
    for pages in sorted(config['pages']):
        case=root/str(pages); case.mkdir()
        start=time.monotonic(); stopped=None
        with (case/'child.log').open('w') as log:
            process=subprocess.Popen([sys.executable,'-m','tests.performance.phase17h','--output',str(case),
                '--config',str(args.config.resolve()),'--child',str(pages)],stdout=log,stderr=log,
                env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'})
            try:
                while process.poll() is None:
                    sizes=inventory(case)
                    if time.monotonic()-start>config['max_seconds']: stopped='wall_budget'
                    if sizes['bytes']>config['max_disk_bytes']: stopped='disk_budget'
                    if sizes['files']>config['max_files']: stopped='file_budget'
                    if stopped:
                        process.kill(); break
                    time.sleep(.2)
                process.wait(timeout=10)
            finally:
                if process.poll() is None: process.kill(); process.wait(timeout=10)
        result=json.loads((case/'result.json').read_text()) if (case/'result.json').exists() else {'pages':pages}
        if stopped or process.returncode:
            result.update(status='RESOURCE_LIMIT' if stopped else 'FAIL',stop_reason=stopped,exit_code=process.returncode)
        result['parent_elapsed_seconds']=time.monotonic()-start
        write(case/'result.json',result); results.append(result); write(root/'results.json',results)
        print(f"{pages} pages: {result['status']} ({result['parent_elapsed_seconds']:.2f}s)",flush=True)
        if result['status'] not in ('PASS','EXPECTED_REFUSAL'):
            break  # Preserve evidence; do not escalate automatically after a failure.
    lines=['# Phase 17H offline benchmark','', '| Pages | Status | Seconds | Peak RSS bytes |',
           '| ---: | --- | ---: | ---: |']
    lines += [f"| {r['pages']} | {r['status']} | {r['parent_elapsed_seconds']:.3f} | {r.get('peak_rss_bytes','unknown')} |" for r in results]
    (root/'summary.md').write_text('\n'.join(lines)+'\n')
    if len(results)!=len(config['pages']) or any(r['status'] not in ('PASS','EXPECTED_REFUSAL') for r in results):
        raise SystemExit(1)


if __name__=='__main__': main()
