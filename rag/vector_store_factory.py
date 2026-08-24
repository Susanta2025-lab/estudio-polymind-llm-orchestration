"""Lazy vector-store construction; imports never require backend connectivity."""

import threading
import time
from typing import Optional

from config.settings import Settings, settings
from rag.chroma_store import ChromaVectorStore
from rag.vector_store import MutableVectorStore, VectorReadiness, VectorStoreError
from llm.metrics import metrics

_store: Optional[MutableVectorStore] = None
_store_lock = threading.Lock()


def create_vector_store(configuration: Settings = settings) -> MutableVectorStore:
    import chromadb
    if configuration.VECTOR_STORE_PROVIDER == "chroma_local":
        client = chromadb.PersistentClient(path=configuration.CHROMA_PATH)
    elif configuration.VECTOR_STORE_PROVIDER == "chroma_http":
        client = chromadb.HttpClient(
            host=configuration.VECTOR_STORE_HOST,
            port=configuration.VECTOR_STORE_PORT,
            ssl=configuration.VECTOR_STORE_SSL,
        )
    else:
        raise ValueError(f"Unsupported vector store provider: {configuration.VECTOR_STORE_PROVIDER}")
    return ChromaVectorStore(client, configuration.VECTOR_STORE_COLLECTION, configuration.VECTOR_STORE_PROVIDER)


def get_vector_store() -> MutableVectorStore:
    global _store
    if _store is None:
        with _store_lock:
            if _store is None:
                try:
                    _store = create_vector_store()
                except Exception:
                    raise VectorStoreError("vector_unreachable") from None
    return _store


def check_vector_store_readiness() -> VectorReadiness:
    started = time.perf_counter()
    try:
        return get_vector_store().check_readiness()
    except VectorStoreError as exc:
        result = VectorReadiness(settings.VECTOR_STORE_PROVIDER, False, exc.category)
        metrics.observe_vector_readiness(result.provider, result.status, time.perf_counter() - started)
        return result


def get_vector_store_admin() -> MutableVectorStore:
    """Explicit mutation boundary for offline/administrative commands only."""
    return get_vector_store()


def close_vector_store() -> None:
    global _store
    with _store_lock:
        if _store is not None:
            _store.close()
            _store = None
