from rank_bm25 import BM25Okapi

from rag.vectordb import collection

bm25_index = None
documents = []
metadata = []


def build_bm25():

    global bm25_index
    global documents
    global metadata

    data = collection.get()

    documents = data["documents"]
    metadata = data["metadatas"]

    tokenized_docs = [
        doc.lower().split()
        for doc in documents
    ]

    bm25_index = BM25Okapi(
        tokenized_docs
    )


def bm25_search(
    query,
    top_k=5
):

    if bm25_index is None:
        build_bm25()

    scores = bm25_index.get_scores(
        query.lower().split()
    )

    ranked = sorted(
        enumerate(scores),
        key=lambda x: x[1],
        reverse=True
    )

    results = []

    for idx, score in ranked[:top_k]:

        results.append(
            {
                "text": documents[idx],
                "source": metadata[idx]["source"],
                "chunk_id": metadata[idx]["chunk_id"],
                "score": round(
                    float(score),
                    3
                )
            }
        )

    return results
