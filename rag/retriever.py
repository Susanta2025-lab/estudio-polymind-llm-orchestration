from rag.embeddings import get_embedding
from rag.vectordb import collection


def retrieve(query: str, n_results: int = 5):

    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    docs = results["documents"][0]
    metadatas = results["metadatas"][0]

    distances = results.get(
        "distances",
        [[0.0] * len(docs)]
    )[0]

    retrieved_docs = []

    for doc, metadata, distance in zip(
        docs,
        metadatas,
        distances
    ):

        score = round(
            max(0.0, 1 - distance),
            3
        )

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
