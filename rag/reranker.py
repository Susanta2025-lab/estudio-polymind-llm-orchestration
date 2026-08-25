import threading

from config.model_artifacts import RERANKER_MODEL, model_source
from config.settings import settings


_reranker = None
_reranker_lock = threading.Lock()


def get_reranker_model():
    """Load the pinned CPU reranker lazily from the configured artifact path."""
    global _reranker
    if _reranker is None:
        with _reranker_lock:
            if _reranker is None:
                from sentence_transformers import CrossEncoder
                _reranker = CrossEncoder(
                    model_source(RERANKER_MODEL, settings.MODEL_ARTIFACT_DIR),
                    revision=None if settings.MODEL_ARTIFACT_DIR else RERANKER_MODEL.revision,
                    local_files_only=settings.MODEL_OFFLINE_MODE,
                    device="cpu",
                )
    return _reranker


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

    scores = get_reranker_model().predict(
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
