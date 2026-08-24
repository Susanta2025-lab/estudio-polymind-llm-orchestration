import threading

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
                    "sentence-transformers/all-MiniLM-L6-v2"
                )
    return _embedding_model

def get_embedding(text: str):
    return get_embedding_model().encode(text).tolist()
