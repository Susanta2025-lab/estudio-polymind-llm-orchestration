"""Real local Chroma adapter contracts; never the cloud or configured runtime DB."""
import pytest
from rag.chroma_store import ChromaVectorStore
from rag.vector_store import VectorFilter, VectorStoreError


def test_real_chroma_generation_and_selection_are_prefiltered(tmp_path):
    import chromadb
    from chromadb.config import Settings
    client = chromadb.PersistentClient(path=str(tmp_path/'chroma'), settings=Settings(anonymized_telemetry=False))
    admin = ChromaVectorStore(client, 'synthetic-publication', 'chroma_local', administrative=True)
    serving = ChromaVectorStore(client, 'synthetic-publication', 'chroma_local')
    admin.upsert(['g1-a','g2-a','g1-b'], ['active alpha','candidate alpha','other document'],
                 [[1.,0.],[1.,0.],[1.,0.]], [
                     {'generation':'g1','document_id':'a'}, {'generation':'g2','document_id':'a'},
                     {'generation':'g1','document_id':'b'}])
    assert [r.document for r in serving.list_documents(scope=VectorFilter('g2'))] == ['candidate alpha']
    # Candidate and unrelated document cannot consume top-k before filtering.
    hits = serving.similarity_search([1.,0.],1,scope=VectorFilter('g1',('a',)))
    assert [r.document for r in hits] == ['active alpha']
    assert serving.similarity_search([1.,0.],1,scope=VectorFilter('missing')) == []
    admin.upsert(['g1-a'], ['active alpha'], [[1.,0.]], [{'generation':'g1','document_id':'a'}])
    assert len(serving.list_documents()) == 3
    with pytest.raises(VectorStoreError,match='vector_write_forbidden'):
        serving.upsert([],[],[],[])
