import threading

from config.model_artifacts import EMBEDDING_MODEL, model_source
from config.settings import settings

_embedding_model = None
_model_lock = threading.Lock()


def get_embedding_model():
    """Load the local embedding runtime lazily; imports never download a model."""
    global _embedding_model
    if _embedding_model is None:
        with _model_lock:
            if _embedding_model is None:
                from sentence_transformers import SentenceTransformer
                _embedding_model = SentenceTransformer(
                    model_source(EMBEDDING_MODEL, settings.MODEL_ARTIFACT_DIR),
                    revision=None if settings.MODEL_ARTIFACT_DIR else EMBEDDING_MODEL.revision,
                    local_files_only=settings.MODEL_OFFLINE_MODE,
                    device="cpu",
                )
    return _embedding_model

def get_embedding(text: str):
    return get_embedding_model().encode(text).tolist()
