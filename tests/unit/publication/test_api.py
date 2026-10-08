from types import SimpleNamespace
from uuid import UUID
import pytest
from documents.publication.analysis import AnalysisRequest
from documents.publication.models import PublicationError


def test_api_additive_route_and_unconfigured_failure():
    from api.app import app, analyze_documents, QueryRequest
    assert QueryRequest(query='legacy').session_id == 'default'
    req = AnalysisRequest(query='alpha', document_ids=(UUID(int=3),))
    old = getattr(app.state,'document_analysis',None)
    try:
        app.state.document_analysis = None
        with pytest.raises(PublicationError,match='publication_unavailable'):
            analyze_documents(req)
        app.state.document_analysis = SimpleNamespace(analyze=lambda request: {'answer':request.query})
        assert analyze_documents(req) == {'answer':'alpha'}
        paths = {r.path for r in app.routes}
        assert {'/query','/query/stream','/documents/analyze'} <= paths
        assert not any('publish' in p or 'revoke' in p or 'rollback' in p for p in paths)
    finally:
        app.state.document_analysis = old


def test_publication_collection_separate_from_legacy(monkeypatch):
    from config.settings import Settings
    from rag import vector_store_factory as factory
    calls=[]
    monkeypatch.setattr(factory,'create_vector_store',lambda conf,administrative: calls.append((conf.VECTOR_STORE_COLLECTION,administrative)))
    config=Settings(VECTOR_STORE_COLLECTION='legacy')
    factory.create_publication_vector_store(config)
    factory.create_publication_vector_store(config,administrative=True)
    assert calls == [('legacy_documents',False),('legacy_documents',True)]


def test_stale_publication_replica_health_and_readiness(monkeypatch):
    from api import app as module
    from llm.inference import ReadinessResult,ReadinessStatus
    from rag.bm25 import BM25Readiness
    monkeypatch.setattr(module,'inference_provider',SimpleNamespace(check_readiness=lambda:ReadinessResult(ReadinessStatus.READY,'fake',{})))
    monkeypatch.setattr(module,'memory_store',SimpleNamespace(check_readiness=lambda:SimpleNamespace(ready=True,status='ready',provider='file')))
    monkeypatch.setattr(module,'check_vector_store_readiness',lambda:SimpleNamespace(ready=True,status='ready',provider='fake',corpus_version='legacy'))
    monkeypatch.setattr(module,'check_bm25_readiness',lambda **kwargs:BM25Readiness(True,'ready','legacy','legacy'))
    replica=SimpleNamespace(ready=lambda:False,expected_version='g2',snapshot=None)
    old=getattr(module.app.state,'document_analysis',None)
    try:
        module.app.state.document_analysis=SimpleNamespace(replica=replica)
        assert module.liveness()=={'status':'alive'}
        assert module.readiness().status_code==503
        replica.ready=lambda:True
        assert module.readiness().status_code==200
    finally:
        module.app.state.document_analysis=old
