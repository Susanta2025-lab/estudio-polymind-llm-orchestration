from rag.embeddings import get_embedding
from rag.vectordb import collection


def retrieve(query: str, n_results: int = 4):

    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    docs = results["documents"][0]
    metadata = results["metadatas"][0]

    combined = []

    for doc, meta in zip(docs, metadata):

        combined.append({
            "text": doc,
            "source": meta["source"],
            "chunk_id": meta["chunk_id"]
        })

    return combined
