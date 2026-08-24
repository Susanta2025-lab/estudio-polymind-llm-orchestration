from rag.embeddings import get_embedding
from rag.vector_store_factory import get_vector_store


def retrieve(query: str, n_results: int = 5, vector_store=None):

    query_embedding = get_embedding(query)

    matches = (vector_store or get_vector_store()).similarity_search(query_embedding, n_results)

    retrieved_docs = []
    seen = set()

    for match in matches:
        doc, metadata, distance = match.document, match.metadata, match.distance

        score = round(
            max(0.0, 1 - distance),
            3
        )

        if score <= 0:
            continue

        key = (
            metadata.get("source"),
            metadata.get("chunk_id")
        )

        if key in seen:
            continue

        seen.add(key)

        retrieved_docs.append(
            {
                "text": doc,
                "source": metadata.get(
                    "source",
                    "Unknown"
                ),
                "chunk_id": metadata.get(
                    "chunk_id",
                    -1
                ),
                "score": score
            }
        )

    retrieved_docs.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return retrieved_docs
