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


def record_identity(item):
    """Publication IDs take precedence; legacy display identity remains compatible."""
    if item.get('record_id'):
        return ('publication', item['record_id'])
    return ('legacy', item.get('source'), item.get('chunk_id'))


def fuse_rankings(dense, sparse, *, rrf_k=60):
    """RRF without discarding one side of conflicting evidence by text similarity."""
    fused = {}
    for ranking in (dense, sparse):
        seen = set()
        for rank, item in enumerate(ranking, 1):
            key = record_identity(item)
            if key in seen:
                continue
            seen.add(key)
            if key not in fused:
                fused[key] = {**item, 'rrf_score': 0.0}
            fused[key]['rrf_score'] += 1 / (rrf_k + rank)
    return sorted(fused.values(), key=lambda item: (-item['rrf_score'], str(record_identity(item))))
