from rag.embeddings import get_embedding
from rag.vectordb import collection


def retrieve(query: str, n_results: int = 3):

    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results["documents"][0]
