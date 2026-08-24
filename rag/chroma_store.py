"""Chroma adapters. Concrete client behavior is isolated in this module."""

import time
from typing import Any, Dict, List, Sequence

from llm.metrics import metrics
from rag.vector_store import VectorDocument, VectorMatch, VectorReadiness, VectorStoreError


def _category(error: BaseException, operation: str) -> str:
    if isinstance(error, TimeoutError):
        return "vector_timeout"
    if isinstance(error, (ConnectionError, OSError)):
        return "vector_unreachable"
    if isinstance(error, (KeyError, TypeError, ValueError, IndexError)):
        return "vector_protocol"
    if error.__class__.__name__ in {"NotFoundError", "InvalidCollectionException"}:
        return "collection_unavailable"
    return "vector_write_failure" if operation in {"upsert", "reset"} else "vector_query_failure"


class ChromaVectorStore:
    def __init__(self, client, collection_name: str, provider: str, metric_store=metrics, administrative: bool = False):
        self.client = client
        self.collection_name = collection_name
        self.provider = provider
        self.metrics = metric_store
        self.administrative = administrative
        self._collection = None

    def _observe(self, operation, callback):
        started = time.perf_counter()
        error = None
        try:
            return callback()
        except VectorStoreError:
            raise
        except Exception as exc:
            error = VectorStoreError(_category(exc, operation))
            raise error from None
        finally:
            self.metrics.observe_vector(self.provider, operation, error, time.perf_counter() - started)

    def _get_collection(self):
        if self._collection is None:
            operation = self.client.get_or_create_collection if self.administrative else self.client.get_collection
            self._collection = operation(name=self.collection_name)
        return self._collection

    def corpus_version(self) -> str | None:
        def read_version():
            metadata = self._get_collection().metadata or {}
            value = metadata.get("polymind_corpus_version")
            return value if isinstance(value, str) and value else None
        return self._observe("version", read_version)

    def publish_corpus_version(self, version: str) -> None:
        if not self.administrative:
            raise VectorStoreError("vector_write_forbidden")
        def publish():
            collection = self._get_collection()
            metadata = dict(collection.metadata or {})
            metadata["polymind_corpus_version"] = version
            collection.modify(metadata=metadata)
        self._observe("publish_version", publish)

    def similarity_search(self, embedding: Sequence[float], limit: int) -> List[VectorMatch]:
        def query():
            result = self._get_collection().query(
                query_embeddings=[list(embedding)], n_results=limit,
                include=["documents", "metadatas", "distances"],
            )
            documents = result["documents"][0]
            metadatas = result["metadatas"][0]
            distances = result["distances"][0]
            if not (len(documents) == len(metadatas) == len(distances)):
                raise ValueError("inconsistent vector response")
            return [VectorMatch(doc, dict(meta or {}), float(distance)) for doc, meta, distance in zip(documents, metadatas, distances)]
        return self._observe("query", query)

    def list_documents(self) -> List[VectorDocument]:
        def get():
            result = self._get_collection().get(include=["documents", "metadatas"])
            documents, metadatas = result["documents"], result["metadatas"]
            if len(documents) != len(metadatas):
                raise ValueError("inconsistent vector response")
            return [VectorDocument(doc, dict(meta or {})) for doc, meta in zip(documents, metadatas)]
        return self._observe("list", get)

    def upsert(self, ids: Sequence[str], documents: Sequence[str], embeddings: Sequence[Sequence[float]], metadatas: Sequence[Dict[str, Any]]) -> None:
        if not self.administrative:
            raise VectorStoreError("vector_write_forbidden")
        self._observe("upsert", lambda: self._get_collection().upsert(
            ids=list(ids), documents=list(documents), embeddings=[list(item) for item in embeddings], metadatas=list(metadatas)
        ))

    def reset(self) -> None:
        if not self.administrative:
            raise VectorStoreError("vector_write_forbidden")
        def reset_collection():
            try:
                self.client.delete_collection(name=self.collection_name)
            except Exception as exc:
                # Chroma's idempotent get-or-create is used after a missing collection.
                if exc.__class__.__name__ not in {"NotFoundError", "InvalidCollectionException"}:
                    raise
            self._collection = self.client.get_or_create_collection(name=self.collection_name)
        self._observe("reset", reset_collection)

    def check_readiness(self) -> VectorReadiness:
        started = time.perf_counter()
        status = "ready"
        try:
            self.client.heartbeat()
            self._get_collection().count()
            return VectorReadiness(self.provider, True, status, self.corpus_version())
        except Exception as exc:
            status = _category(exc, "readiness")
            return VectorReadiness(self.provider, False, status)
        finally:
            self.metrics.observe_vector_readiness(self.provider, status, time.perf_counter() - started)

    def close(self) -> None:
        session = getattr(getattr(self.client, "_server", None), "_session", None)
        close = getattr(session, "close", None)
        if close is not None:
            close()
