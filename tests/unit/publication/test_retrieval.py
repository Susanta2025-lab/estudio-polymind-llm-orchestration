from uuid import UUID
import pytest
from documents.publication.models import PublicationError
from documents.publication.retrieval import PublicationReplica
from rag.hybrid_retriever import fuse_rankings


def publish(service, jobs):
    m = service.plan(jobs); service.prepare(m.generation); service.activate(m.generation)
    return m


def unchanged(query, docs, top_k):
    return [{**d, 'rerank_score': 1.} for d in docs[:top_k]]


def test_generation_pinning_stale_replica_and_revocation(env, monkeypatch):
    service, document = env
    a,b = document(), document('another alpha\n', identity=4)
    first = publish(service, [a,b])
    replica = PublicationReplica(service, first.generation); replica.load()
    pin = replica.pin([UUID(int=3)])
    hits = replica.retrieve('alpha', pin, reranker=unchanged)
    assert hits and all(h['document_id'] == str(UUID(int=3)) for h in hits)
    citations = replica.citations(pin, hits)
    assert citations[0].span.line_start == 1 and citations[0].physical_page is None
    next_active = service.revoke([UUID(int=3)])
    assert not replica.ready()
    with pytest.raises(PublicationError, match='publication_generation_mismatch'):
        replica.pin()
    # Already admitted request finishes against G1, not G2 dense + G1 sparse.
    assert replica.retrieve('alpha', pin, reranker=unchanged)
    fresh = PublicationReplica(service, next_active.generation); fresh.load()
    assert fresh.ready()
    with pytest.raises(PublicationError, match='retrieval_scope_invalid'):
        fresh.pin([UUID(int=3)])
    assert all(h['document_id'] == str(UUID(int=4)) for h in fresh.retrieve('alpha', fresh.pin(), reranker=unchanged))
    # Readiness/request checks must never rebuild BM25.
    monkeypatch.setattr('documents.publication.service.BM25Okapi', lambda *_: pytest.fail('read-time build'))
    monkeypatch.setattr('documents.publication.retrieval.BM25Okapi', lambda *_: pytest.fail('read-time build'))
    assert fresh.ready()
    assert fresh.retrieve('alpha', fresh.pin(), reranker=unchanged)


def test_rrf_stable_identity_dense_sparse_and_legacy():
    a = dict(record_id='one', generation='g', source='x',chunk_id=0, text='dense')
    b = dict(record_id='two', generation='g', source='x',chunk_id=0, text='sparse')
    result = fuse_rankings([a,a], [a,b])
    assert len(result) == 2
    assert result[0]['record_id'] == 'one' and result[0]['rrf_score'] == 2/61
    assert len(fuse_rankings([], [b])) == 1
    assert len(fuse_rankings([a], [])) == 1
    assert len(fuse_rankings([{'source':'x','chunk_id':0}], [{'source':'x','chunk_id':0}])) == 1


def test_reranker_provenance_tampering_rejected(env):
    service, document = env
    m = publish(service, [document()]); replica = PublicationReplica(service, m.generation); replica.load()
    with pytest.raises(PublicationError, match='provenance_invalid'):
        replica.retrieve('alpha', replica.pin(), reranker=lambda q,ds,top_k: [{**ds[0],'generation':'foreign'}])


def test_candidate_invisible_and_active_loss_unready(env):
    service, document = env
    m = publish(service, [document()]); replica = PublicationReplica(service, m.generation); replica.load()
    candidate = service.plan([document('new candidate\n')]); service.prepare(candidate.generation)
    hits = replica.retrieve('alpha', replica.pin(), reranker=unchanged)
    assert all(h['generation'] == str(m.generation) for h in hits)
    key = next(k for k,v in service.vectors.rows.items() if v.metadata['generation'] == str(m.generation))
    del service.vectors.rows[key]
    assert not replica.ready()


def test_real_reranker_preserves_metadata(env,monkeypatch):
    from rag import reranker
    service, document = env
    m = publish(service,[document()]); replica=PublicationReplica(service,m.generation); replica.load()
    class Model:
        def predict(self,pairs):
            return list(range(len(pairs)))
    monkeypatch.setattr(reranker,'get_reranker_model',lambda:Model())
    pin=replica.pin(); hits=replica.retrieve('alpha',pin,reranker=reranker.rerank)
    assert hits and all(h['generation']==str(m.generation) and h['record_id'] for h in hits)
    assert replica.citations(pin,hits)


def test_wrong_document_and_generation_citation_fail_closed(env):
    service, document = env
    m = publish(service,[document(),document('other\n',identity=4)])
    replica=PublicationReplica(service,m.generation);replica.load()
    all_hits=replica.retrieve('alpha',replica.pin(),reranker=unchanged)
    other=next(h for h in all_hits if h['document_id']==str(UUID(int=4)))
    with pytest.raises(PublicationError,match='provenance_invalid'):
        replica.citations(replica.pin([UUID(int=3)]),[other])
    with pytest.raises(PublicationError,match='provenance_invalid'):
        replica.citations(replica.pin(),[{**all_hits[0],'generation':'foreign'}])


def test_sparse_only_and_dense_only_paths(env,monkeypatch):
    service, document = env
    m=publish(service,[document()]);replica=PublicationReplica(service,m.generation);replica.load()
    original=service.vectors.similarity_search
    monkeypatch.setattr(service.vectors,'similarity_search',lambda *args,**kwargs:[])
    sparse=replica.retrieve('alpha',replica.pin(),reranker=unchanged)
    assert sparse and sparse[0]['text']=='alpha evidence\n'
    monkeypatch.setattr(service.vectors,'similarity_search',original)
    dense=replica.retrieve('absentkeyword',replica.pin(),reranker=unchanged)
    assert dense and all(h['record_id'] for h in dense)
