import re
import threading
from dataclasses import dataclass

from rank_bm25 import BM25Okapi

from rag.vector_store_factory import get_vector_store
from rag.vector_store import VectorStoreError


bm25_index = None
documents = []
metadata = []
loaded_corpus_version = None
_build_lock = threading.Lock()


@dataclass(frozen=True)
class BM25Readiness:
    ready: bool
    status: str
    loaded_version: str | None
    expected_version: str


class BM25SnapshotUnavailable(VectorStoreError):
    def __init__(self):
        super().__init__("bm25_snapshot_unavailable")


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


def build_bm25(vector_store=None, expected_version=None):

    global bm25_index
    global documents
    global metadata
    global loaded_corpus_version

    from config.settings import settings
    expected_version = expected_version or settings.BM25_CORPUS_VERSION
    store = vector_store or get_vector_store()

    with _build_lock:
        published_version = store.corpus_version()
        if published_version != expected_version:
            raise BM25SnapshotUnavailable()

        data = sorted(
            store.list_documents(),
            key=lambda item: (
                str(item.metadata.get("source", "")),
                str(item.metadata.get("chunk_id", "")),
                item.document,
            ),
        )
        new_documents = [item.document for item in data]
        new_metadata = [item.metadata for item in data]

        tokenized_docs = [tokenize(doc) for doc in new_documents]
        new_index = BM25Okapi(tokenized_docs)

        documents = new_documents
        metadata = new_metadata
        bm25_index = new_index
        loaded_corpus_version = published_version


def check_bm25_readiness(vector_store=None, expected_version=None, published_version=None, vector_ready=True):
    from config.settings import settings
    expected = expected_version or settings.BM25_CORPUS_VERSION
    loaded = loaded_corpus_version
    if bm25_index is None or loaded is None:
        return BM25Readiness(False, "bm25_uninitialized", loaded, expected)
    if not vector_ready:
        return BM25Readiness(False, "bm25_version_unavailable", loaded, expected)
    try:
        published = published_version
        if published is None:
            published = (vector_store or get_vector_store()).corpus_version()
    except Exception:
        return BM25Readiness(False, "bm25_version_unavailable", loaded, expected)
    if loaded != expected or published != expected:
        return BM25Readiness(False, "bm25_version_mismatch", loaded, expected)
    return BM25Readiness(True, "ready", loaded, expected)


def clear_bm25_snapshot():
    global bm25_index, documents, metadata, loaded_corpus_version
    with _build_lock:
        bm25_index = None
        documents = []
        metadata = []
        loaded_corpus_version = None


def bm25_search(
    query: str,
    top_k: int = 5,
    vector_store=None,
):

    if bm25_index is None:
        raise BM25SnapshotUnavailable()

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
