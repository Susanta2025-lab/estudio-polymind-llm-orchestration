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

        if key not in fused_scores:

            fused_scores[key] = {
                "item": item.copy(),
                "rrf_score": 0.0
            }

        fused_scores[key]["rrf_score"] += (
            1 / (rrf_k + rank)
        )

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
                "item": item.copy(),
                "rrf_score": 0.0
            }

        fused_scores[key]["rrf_score"] += (
            1 / (rrf_k + rank)
        )

    results = []

    for value in fused_scores.values():

        item = value["item"]

        item["rrf_score"] = round(
            value["rrf_score"],
            5
        )

        results.append(item)

    results.sort(
        key=lambda x: x["rrf_score"],
        reverse=True
    )

    # Remove near-duplicates
    unique_results = []
    seen = set()

    for item in results:

        key = (
            item["source"],
            item["chunk_id"]
        )

        if key not in seen:

            unique_results.append(item)
            seen.add(key)

    # Dynamic relevance filtering
    if unique_results:

        best_score = unique_results[0]["rrf_score"]

        unique_results = [
            item
            for item in unique_results
            if item["rrf_score"] >= best_score * 0.8
        ]

    return unique_results[:top_k]
