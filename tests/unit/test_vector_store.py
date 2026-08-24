import sys
from types import SimpleNamespace

import pytest
from pydantic import ValidationError
from prometheus_client import CollectorRegistry

from config.settings import Settings
from llm.metrics import Metrics
from rag.chroma_store import ChromaVectorStore
from rag.vector_store import VectorStoreError
from rag.vector_store_factory import create_vector_store


class Collection:
    def __init__(self, query_result=None, get_result=None, error=None):
        self.query_result = query_result or {"documents": [[]], "metadatas": [[]], "distances": [[]]}
        self.get_result = get_result or {"documents": [], "metadatas": []}
        self.error = error
        self.upserts = []

    def query(self, **kwargs):
        if self.error:
            raise self.error
        return self.query_result

    def get(self, **kwargs):
        if self.error:
            raise self.error
        return self.get_result

    def upsert(self, **kwargs):
        if self.error:
            raise self.error
        self.upserts.append(kwargs)

    def count(self):
        if self.error:
            raise self.error
        return len(self.get_result["documents"])


class Client:
    def __init__(self, collection, heartbeat_error=None):
        self.collection = collection
        self.heartbeat_error = heartbeat_error

    def get_or_create_collection(self, name):
        return self.collection

    def heartbeat(self):
        if self.heartbeat_error:
            raise self.heartbeat_error
        return 1


def store(collection=None, heartbeat_error=None, metrics=None):
    return ChromaVectorStore(Client(collection or Collection(), heartbeat_error), "knowledge", "chroma_http", metrics or Metrics(CollectorRegistry()))


def test_query_success_empty_and_normalized_documents():
    populated = Collection(query_result={
        "documents": [["alpha"]], "metadatas": [[{"source": "a.txt", "chunk_id": 2}]], "distances": [[0.25]],
    })
    match = store(populated).similarity_search([1.0], 3)[0]
    assert (match.document, match.metadata, match.distance) == ("alpha", {"source": "a.txt", "chunk_id": 2}, 0.25)
    assert store().similarity_search([1.0], 3) == []


@pytest.mark.parametrize("error,category", [
    (TimeoutError("private"), "vector_timeout"),
    (ConnectionError("private"), "vector_unreachable"),
])
def test_query_failures_are_categorized_and_sanitized(error, category):
    with pytest.raises(VectorStoreError) as caught:
        store(Collection(error=error)).similarity_search([1.0], 1)
    assert caught.value.category == category
    assert "private" not in str(caught.value)


def test_malformed_response_and_unavailable_collection_are_normalized():
    malformed = Collection(query_result={"documents": [["a"]], "metadatas": [[]], "distances": [[0.1]]})
    with pytest.raises(VectorStoreError, match="vector_protocol"):
        store(malformed).similarity_search([1.0], 1)
    with pytest.raises(VectorStoreError, match="vector_query_failure"):
        store(Collection(error=RuntimeError("collection missing"))).list_documents()
    NotFoundError = type("NotFoundError", (RuntimeError,), {})
    with pytest.raises(VectorStoreError, match="collection_unavailable"):
        store(Collection(error=NotFoundError("private collection"))).list_documents()


def test_readiness_and_upsert_contract():
    collection = Collection()
    target = store(collection)
    assert target.check_readiness().ready is True
    target.upsert(["id"], ["doc"], [[1.0]], [{"source": "x"}])
    assert collection.upserts == [{"ids": ["id"], "documents": ["doc"], "embeddings": [[1.0]], "metadatas": [{"source": "x"}]}]
    unavailable = store(Collection(), ConnectionError("secret")).check_readiness()
    assert (unavailable.ready, unavailable.status) == (False, "vector_unreachable")


def test_factory_selects_local_and_shared_without_module_level_client(monkeypatch):
    calls = []
    fake_client = Client(Collection())
    module = SimpleNamespace(
        PersistentClient=lambda **kwargs: calls.append(("local", kwargs)) or fake_client,
        HttpClient=lambda **kwargs: calls.append(("http", kwargs)) or fake_client,
    )
    monkeypatch.setitem(sys.modules, "chromadb", module)
    local = create_vector_store(Settings(VECTOR_STORE_PROVIDER="chroma_local", CHROMA_PATH="custom/path"))
    shared = create_vector_store(Settings(VECTOR_STORE_PROVIDER="chroma_http", VECTOR_STORE_HOST="vector.internal", VECTOR_STORE_PORT=9000, VECTOR_STORE_SSL=True))
    assert local.provider == "chroma_local"
    assert shared.provider == "chroma_http"
    assert calls == [("local", {"path": "custom/path"}), ("http", {"host": "vector.internal", "port": 9000, "ssl": True})]


def test_vector_configuration_rejects_invalid_or_incomplete_values():
    with pytest.raises(ValidationError):
        Settings(VECTOR_STORE_PROVIDER="unknown")
    with pytest.raises(ValidationError):
        Settings(VECTOR_STORE_PROVIDER="chroma_http", VECTOR_STORE_HOST="")
    with pytest.raises(ValidationError):
        Settings(VECTOR_STORE_PROVIDER="chroma_local", CHROMA_PATH="")


def test_metrics_are_bounded_and_exclude_content():
    metric_store = Metrics(CollectorRegistry())
    target = store(Collection(error=ConnectionError("query text private-id")), metrics=metric_store)
    with pytest.raises(VectorStoreError):
        target.similarity_search([1.0], 1)
    output = metric_store.render().decode()
    assert 'vector_errors_total{error_category="vector_unreachable",operation="query",provider="chroma_http"} 1.0' in output
    for forbidden in ("query text", "private-id", "request_id", "collection"):
        assert forbidden not in output
