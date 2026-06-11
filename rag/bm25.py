import re

from rank_bm25 import BM25Okapi

from rag.vectordb import collection


bm25_index = None
documents = []
metadata = []


STOPWORDS = {
    "a",
    "an",
    "the",
    "is",
    "are",
    "was",
    "were",
    "what",
    "who",
    "when",
    "where",
    "why",
    "how",
    "of",
    "to",
    "for",
    "in",
    "on",
    "at",
    "and",
    "or",
    "with",
    "about"
}


def tokenize(text: str):

    text = text.lower()

    tokens = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text
    )

    tokens = [
        token
        for token in tokens
        if token not in STOPWORDS
    ]

    return tokens


def build_bm25():

    global bm25_index
    global documents
    global metadata

    data = collection.get()

    documents = data["documents"]
    metadata = data["metadatas"]

    tokenized_docs = [
        tokenize(doc)
        for doc in documents
    ]

    bm25_index = BM25Okapi(
        tokenized_docs
    )


def bm25_search(
    query: str,
    top_k: int = 5
):

    if bm25_index is None:
        build_bm25()

    query_tokens = tokenize(
        query
    )

    scores = bm25_index.get_scores(
        query_tokens
    )

    ranked = sorted(
        enumerate(scores),
        key=lambda x: x[1],
        reverse=True
    )

    results = []

    for idx, score in ranked[:top_k]:
        if score <= 0:
            continue

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

        if len(results) >= top_k:
            break


    return results
