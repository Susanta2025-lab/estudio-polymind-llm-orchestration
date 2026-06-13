from sentence_transformers import CrossEncoder


reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(
    query: str,
    docs: list,
    top_k: int = 3
):

    pairs = [

        (
            query,
            doc["text"]
        )

        for doc in docs
    ]

    scores = reranker.predict(
        pairs
    )

    for doc, score in zip(
        docs,
        scores
    ):

        doc["rerank_score"] = float(
            score
        )

    docs.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return docs[:top_k]
