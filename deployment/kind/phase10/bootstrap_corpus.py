"""Publish a tiny deterministic corpus for local Phase 10 validation."""

import os

import chromadb


host = os.environ.get("VECTOR_STORE_HOST", "phase10-chroma")
port = int(os.environ.get("VECTOR_STORE_PORT", "8000"))
collection_name = os.environ.get("VECTOR_STORE_COLLECTION", "phase10_knowledge")
version = os.environ.get("BM25_CORPUS_VERSION", "phase10-v1")

client = chromadb.HttpClient(host=host, port=port)
collection = client.get_or_create_collection(name=collection_name)
collection.upsert(
    ids=["phase10-document"],
    documents=["PolyMind Phase 10 validates Kubernetes operations with synthetic content."],
    embeddings=[[0.01] * 384],
    metadatas=[{"source": "phase10.txt", "chunk_id": 0, "file_type": ".txt"}],
)
metadata = dict(collection.metadata or {})
metadata["polymind_corpus_version"] = version
collection.modify(metadata=metadata)
print(f"Published corpus version {version} with {collection.count()} document(s).")

