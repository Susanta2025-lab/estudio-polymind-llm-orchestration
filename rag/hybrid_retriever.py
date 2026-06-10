from rag.retriever import retrieve
from rag.bm25 import bm25_search


def hybrid_retrieve(
    query: str,
    top_k: int = 5,
    rrf_k: int = 60
):

    vector_results = retrieve(
        query,
        n_results=top_k
    )

    bm25_results = bm25_search(
        query,
        top_k=top_k
    )

    fused_scores = {}

    # Vector ranking
    for rank, item in enumerate(
        vector_results,
        start=1
    ):

        key = (
            item["source"],
            item["chunk_id"]
        )

        fused_scores[key] = {
            "item": item,
            "score": 1 / (
                rrf_k + rank
            )
        }

    # BM25 ranking
    for rank, item in enumerate(
        bm25_results,
        start=1
    ):

        key = (
            item["source"],
            item["chunk_id"]
        )

        if key not in fused_scores:

            fused_scores[key] = {
                "item": item,
                "score": 0
            }

        fused_scores[key]["score"] += (
            1 / (
                rrf_k + rank
            )
        )

    results = []

    for value in fused_scores.values():

        item = value["item"].copy()

        item["rrf_score"] = round(
            value["score"],
            5
        )

        results.append(item)

    # Sort by fused score
    results.sort(
        key=lambda x: x["rrf_score"],
        reverse=True
    )

    # Nothing found
    if not results:
        return []

    # Keep only highly relevant chunks
    best_score = results[0]["rrf_score"]

    relevance_threshold = (
        best_score * 0.75
    )

    filtered_results = [
        r
        for r in results
        if r["rrf_score"] >= relevance_threshold
    ]

    return filtered_results[:top_k]
