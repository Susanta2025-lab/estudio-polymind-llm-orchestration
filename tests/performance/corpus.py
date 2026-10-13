"""Explicit local Chroma corpus benchmark with selected-document authorization.

Constant embeddings and identity reranking characterize contracts, not semantics.
"""
from io import BytesIO
import json
from pathlib import Path
import time
from uuid import UUID

from tests.performance.fixtures import NOW, pdf, profile
from tests.performance.phase17h import CountingStore, SyntheticModel, measure, inventory, write
from tests.performance.quality import ranking


def run(root, sizes=(1,8,32)):
    import chromadb
    from chromadb.config import Settings
    from documents.storage import LocalObjectStore
    from documents.extraction import extract
    from documents.jobs.models import JobSettings
    from documents.jobs.sqlite import SQLiteJobLedger
    from documents.jobs.worker import LocalDispatcher, Worker, relay
    from documents.digestion.inference import FakeInference
    from documents.digestion.workflow import prepare, admit, DigestionHandler, classify_digestion
    from documents.publication.authority import SQLitePublicationAuthority
    from documents.publication.encoding import RetrievalEncoder
    from documents.publication.models import RetrievalProfile
    from documents.publication.service import PublicationService
    from documents.publication.retrieval import PublicationReplica
    from rag.chroma_store import ChromaVectorStore
    from security.authority import SecurityAuthority
    from security.models import Action, _verified_principal, SecurityError
    root=Path(root).resolve();root.mkdir(parents=True,exist_ok=True)
    started=time.perf_counter()
    auth=SecurityAuthority(root/'security.sqlite')
    owner=_verified_principal('offline','owner','A',expires=int(time.time())+3600)
    shared=_verified_principal('offline','shared','A',expires=int(time.time())+3600)
    foreign=_verified_principal('offline','foreign','B',expires=int(time.time())+3600)
    op=_verified_principal('offline','operator','A',frozenset({Action.PUBLICATION_MANAGE}),expires=int(time.time())+3600)
    for p in (owner,shared,foreign,op):auth.register(p)
    objects=CountingStore(LocalObjectStore(root/'objects'))
    jobs=SQLiteJobLedger(JobSettings(database_path=root/'jobs.sqlite',lease_seconds=120))
    client=chromadb.PersistentClient(path=str(root/'chroma'),settings=Settings(anonymized_telemetry=False))
    vectors=ChromaVectorStore(client,'phase17h-local-only','chroma_local',administrative=True)
    model=SyntheticModel();encoder=RetrievalEncoder(RetrievalProfile(),model)
    authority=SQLitePublicationAuthority(root/'publication.sqlite')
    service=PublicationService(authority,objects,jobs,vectors,encoder,owner.scope)
    job_ids=[];results=[]; previous=None
    for size in sizes:
        for i in range(len(job_ids),size):
            artifact,ref=extract(BytesIO(pdf(4,seed=1708+i)[0]),scope=owner.scope,document_id=UUID(int=1000+i),
                display_filename='similar-report.pdf',declared_mime='application/pdf',store=objects,
                created_at=NOW,extracted_at=NOW)
            auth.register_document(op,artifact.document)
            plan,pr=prepare(artifact,ref,profile(),objects)
            job=admit(jobs,objects,plan,pr,request_key=str(i))
            queue=LocalDispatcher();worker=Worker(jobs,queue,objects,DigestionHandler(jobs,pr,FakeInference()),
                owner='corpus',classifier=classify_digestion)
            for _ in range(20):
                relay(jobs,queue)
                if not worker.once():break
            assert jobs.get_job(owner.scope,job.job_id).state=='COMPLETED'
            job_ids.append(job.job_id)
        timing={}
        def timed(name,fn):
            start=time.perf_counter();value=fn();timing[name]=time.perf_counter()-start;return value
        manifest=timed('plan',lambda:service.plan(job_ids))
        # Interrupt a real local Chroma candidate after one upsert, then reopen authority.
        if previous:
            def fault(point):
                if point=='after_write':raise RuntimeError('synthetic upsert interruption')
            from documents.publication.models import PublicationError
            try:service.prepare(manifest.generation,checkpoint=fault)
            except PublicationError:pass
            else:raise AssertionError('fault did not occur')
            assert authority.active()==previous
            assert len(service.validate(previous.generation).documents)<size
            service.authority=SQLitePublicationAuthority(root/'publication.sqlite')
        timed('prepare',lambda:service.prepare(manifest.generation))
        timed('validate',lambda:service.validate(manifest.generation))
        active=timed('activate',lambda:service.activate(manifest.generation))
        replica=PublicationReplica(service,manifest.generation);timed('load',replica.load)
        assert timed('ready',replica.ready)
        selected=(UUID(int=1000),)
        auth.share(owner,selected[0],shared.scope.owner)
        for principal in (foreign,):
            try:auth.snapshot(principal,selected)
            except SecurityError:pass
            else:raise AssertionError('cross-tenant authorization')
        snapshot=auth.snapshot(shared,selected)
        pin=replica.pin(selected,authorization=(auth,snapshot))
        # Whole-corpus sparse statistics must never participate in authorized search.
        replica.snapshot[1].get_scores=lambda _:(_ for _ in ()).throw(AssertionError('unscoped sparse'))
        retrieve_times=[];citation_times=[];dense_times=[];sparse_times=[];fusion_times=[];rerank_times=[]
        original_search=vectors.similarity_search
        def search(*args,**kwargs):
            assert kwargs['scope'].document_ids==(str(selected[0]),)
            start=time.perf_counter();hits=original_search(*args,**kwargs);dense_times.append(time.perf_counter()-start);return hits
        vectors.similarity_search=search
        isolated=pin.sparse_indexes[selected[0]][1];original_scores=isolated.get_scores
        def scores(query):
            start=time.perf_counter();values=original_scores(query);sparse_times.append(time.perf_counter()-start);return values
        isolated.get_scores=scores
        import documents.publication.retrieval as retrieval_module
        original_fuse=retrieval_module.fuse_rankings
        def fuse(*args):
            start=time.perf_counter();value=original_fuse(*args);fusion_times.append(time.perf_counter()-start);return value
        retrieval_module.fuse_rankings=fuse
        def rerank(query,docs,top_k):
            start=time.perf_counter();value=docs[:top_k];rerank_times.append(time.perf_counter()-start);return value
        io_before=objects.counts.copy()
        try:
            for _ in range(5):
                start=time.perf_counter();hits=replica.retrieve('Unit 0001',pin,top_k=8,reranker=rerank)
                retrieve_times.append(time.perf_counter()-start)
                start=time.perf_counter();citations=replica.citations(pin,hits);citation_times.append(time.perf_counter()-start)
                assert all(c.document_id==selected[0] and c.generation==manifest.generation for c in citations)
        finally:
            vectors.similarity_search=original_search;isolated.get_scores=original_scores
            retrieval_module.fuse_rankings=original_fuse
        # Explicit labels identify page 1's source ID, not vector insertion order.
        from documents.serialization import deserialize
        selected_doc=next(d for d in manifest.documents if d.document_id==selected[0])
        canonical=deserialize(objects.read(selected_doc.scope,selected_doc.extraction,max_bytes=32000000))
        page1=next(u.source_id for u in canonical.units if u.physical_page==1)
        relevant={str(r.record_id) for r in manifest.records if r.document_id==selected[0] and r.evidence.source_id==page1}
        metrics=ranking([h['record_id'] for h in hits],relevant,8)
        # Compare separately labelled dense and sparse contributions without claiming entailment.
        from rag.vector_store import VectorFilter
        dense=original_search(encoder.embed('Unit 0001'),8,scope=VectorFilter(str(manifest.generation),(str(selected[0]),)))
        from rag.bm25 import tokenize
        positions,index=pin.sparse_indexes[selected[0]]
        scores_values=index.get_scores(tokenize('Unit 0001'))
        ordered=sorted(range(len(positions)),key=lambda j:(-scores_values[j],str(manifest.records[positions[j]].record_id)))
        sparse=[str(manifest.records[positions[j]].record_id) for j in ordered if scores_values[j]>0][:8]
        result={'documents':size,'physical_pages':size*4,'selected_documents':1,'unauthorized_documents':size-1,
            'records':len(manifest.records),'retained_chroma_rows':len(vectors.list_documents()),
            'timings':timing,'retrieval':measure(retrieve_times),'citations':measure(citation_times),
            'dense':measure(dense_times),'sparse':measure(sparse_times),'rrf':measure(fusion_times),
            'identity_reranker':measure(rerank_times),'ranking':metrics,
            'dense_ranking':ranking([h.metadata['record_id'] for h in dense],relevant,8),
            'sparse_ranking':ranking(sparse,relevant,8), 'reranking_impact':'identity; no quality inference',
            'query_object_io':dict(objects.counts-io_before),'failures':0,
            'fake_embedding_calls':model.calls,'generation':str(manifest.generation),
            'peak_rss_bytes':__import__('resource').getrusage(__import__('resource').RUSAGE_SELF).ru_maxrss*1024,
            'disk':inventory(root)}
        if size>=8:
            # Multiple selected authorized docs in the same owning generation.
            selection=(UUID(int=1000),UUID(int=1001));auth.share(owner,selection[1],shared.scope.owner)
            multi=replica.pin(selection,authorization=(auth,auth.snapshot(shared,selection)))
            multi_hits=replica.retrieve('procedure',multi,reranker=rerank)
            assert {h['document_id'] for h in multi_hits}<={str(d) for d in selection}
            result['multiple_selected_hits']=len(multi_hits)
        results.append(result);write(root/'results.json',results)
        previous=active
    # Rollback cannot reauthorize a tombstone with retained vector rows.
    auth.tombstone(owner,UUID(int=1000));auth=SecurityAuthority(auth.path)
    service.rollback(UUID(results[0]['generation']),service.authority.active())
    for principal in (owner,shared,foreign):
        try:auth.snapshot(principal,(UUID(int=1000),))
        except SecurityError:pass
        else:raise AssertionError('rollback restored authority')
    assert auth.track_purge(op,UUID(int=1000))['state']=='PURGE_PENDING'
    write(root/'closure.json',{'elapsed_seconds':time.perf_counter()-started,'rollback_tombstone':'denied',
        'candidate_failure':'old active preserved; deterministic upsert recovered',
        'backend':'temporary local persistent Chroma','embedding':'constant fake',
        'model_semantics':'NOT VALIDATED','environment':__import__('platform').platform()})
    return results


if __name__=='__main__':
    import argparse, resource
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    if args.output.exists() or args.output.resolve().is_relative_to(Path.cwd()):raise ValueError('new outside-repository directory required')
    resource.setrlimit(resource.RLIMIT_CPU,(180,181))
    import signal
    signal.alarm(240)
    print(json.dumps(run(args.output),indent=2))
