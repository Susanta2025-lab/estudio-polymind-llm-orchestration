import sys
from types import ModuleType

embeddings = ModuleType("rag.embeddings")
embeddings.get_embedding = lambda query: [0.5]
previous_embeddings = sys.modules.get("rag.embeddings")
sys.modules["rag.embeddings"] = embeddings
from rag import bm25, hybrid_retriever, retriever
if previous_embeddings is None:
    sys.modules.pop("rag.embeddings", None)
else:
    sys.modules["rag.embeddings"] = previous_embeddings
from rag.vector_store import VectorDocument, VectorMatch
from graph.generation import rag_prompt_and_sources


class Store:
    def similarity_search(self, embedding, limit):
        return [
            VectorMatch("dense", {"source": "doc.txt", "chunk_id": 1}, 0.2),
            VectorMatch("duplicate", {"source": "doc.txt", "chunk_id": 1}, 0.3),
            VectorMatch("irrelevant", {"source": "low.txt", "chunk_id": 2}, 1.1),
        ]

    def list_documents(self):
        return [
            VectorDocument("alpha dense", {"source": "doc.txt", "chunk_id": 1}),
            VectorDocument("beta text", {"source": "b.txt", "chunk_id": 2}),
            VectorDocument("gamma text", {"source": "c.txt", "chunk_id": 3}),
        ]


def test_dense_retrieval_preserves_normalization_deduplication_and_metadata(monkeypatch):
    monkeypatch.setattr(retriever, "get_embedding", lambda query: [0.5])
    assert retriever.retrieve("alpha", vector_store=Store()) == [
        {"text": "dense", "source": "doc.txt", "chunk_id": 1, "score": 0.8}
    ]


def test_bm25_builds_from_provider_snapshot(monkeypatch):
    monkeypatch.setattr(bm25, "bm25_index", None)
    results = bm25.bm25_search("alpha", vector_store=Store())
    assert results[0]["text"] == "alpha dense"
    assert results[0]["source"] == "doc.txt"


def test_hybrid_rrf_behavior_and_inputs_are_unchanged(monkeypatch):
    monkeypatch.setattr(hybrid_retriever, "retrieve", lambda query, n_results: [{"text": "dense", "source": "a", "chunk_id": 1, "score": .8}])
    monkeypatch.setattr(hybrid_retriever, "bm25_search", lambda query, top_k: [
        {"text": "dense", "source": "a", "chunk_id": 1, "score": 2.0},
        {"text": "sparse", "source": "b", "chunk_id": 2, "score": 1.0},
    ])
    result = hybrid_retriever.hybrid_retrieve("q", top_k=2)
    assert result[0]["source"] == "a"
    assert result[0]["rrf_score"] == round(2 / 61, 5)
    # Existing dynamic relevance filtering removes the lower sparse-only hit.
    assert [item["source"] for item in result] == ["a"]


def test_reranker_receives_retrieval_documents_and_sources_stay_compatible():
    retrieved = [{"text": "context", "source": "doc.pdf", "chunk_id": 4, "score": 0.7}]
    calls = []

    class Memory:
        def get_history(self, session_id):
            return []

    def rerank(query, documents, top_k):
        calls.append((query, documents, top_k))
        return [{**documents[0], "rerank_score": 0.9}]

    _prompt, context, sources = rag_prompt_and_sources(
        "question", "session", retrieve=lambda query: retrieved,
        rerank_documents=rerank, memory_store=Memory(),
    )
    assert calls == [("question", retrieved, 3)]
    assert context == "context"
    assert sources == [{"text": "context", "source": "doc.pdf", "chunk_id": 4, "score": 0.7, "rerank_score": 0.9}]
