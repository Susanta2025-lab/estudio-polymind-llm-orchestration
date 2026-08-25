import asyncio
from pathlib import Path
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from config.settings import Settings
from rag import bm25, ingest
from rag.chroma_store import ChromaVectorStore
from rag.vector_store import VectorDocument, VectorStoreError


MODELS = {role: "served" for role in ("general", "coding", "summarization", "fast")}


def production_settings(**overrides):
    values = {
        "_env_file": None,
        "DEPLOYMENT_ENV": "production",
        "INFERENCE_PROVIDER": "openai_compatible",
        "OPENAI_COMPATIBLE_BASE_URL": "https://inference.internal/v1",
        "OPENAI_COMPATIBLE_MODEL_MAP": MODELS,
        "MEMORY_PROVIDER": "redis",
        "REDIS_URL": "rediss://memory.internal:6380/0",
        "VECTOR_STORE_PROVIDER": "chroma_http",
        "VECTOR_STORE_HOST": "vector.internal",
        "VECTOR_STORE_SSL": True,
        "BM25_CORPUS_VERSION": "corpus-2026-08-24",
        "API_AUTH_ENABLED": True,
        "API_AUTH_TOKEN": "synthetic-production-token-32-characters",
        "API_DOCS_ENABLED": False,
    }
    values.update(overrides)
    return Settings(**values)


def test_local_and_production_deployment_configuration_is_valid():
    assert Settings(_env_file=None).DEPLOYMENT_ENV == "local"
    config = production_settings()
    assert (config.MEMORY_PROVIDER, config.VECTOR_STORE_PROVIDER) == ("redis", "chroma_http")


@pytest.mark.parametrize("override", [
    {"API_AUTH_ENABLED": False},
    {"API_AUTH_TOKEN": None},
    {"API_AUTH_TOKEN": "too-short"},
    {"API_AUTH_TOKEN": " " * 32},
    {"API_AUTH_TOKEN": "synthetic token containing whitespace"},
    {"API_DOCS_ENABLED": True},
])
def test_insecure_production_api_configuration_fails_early(override):
    with pytest.raises(ValidationError):
        production_settings(**override)


@pytest.mark.parametrize("override", [
    {"INFERENCE_PROVIDER": "ollama"},
    {"MEMORY_PROVIDER": "file"},
    {"VECTOR_STORE_PROVIDER": "chroma_local"},
    {"OPENAI_COMPATIBLE_BASE_URL": "http://localhost:8000/v1"},
    {"REDIS_URL": "redis://127.0.0.1:6379/0"},
    {"VECTOR_STORE_HOST": "host.docker.internal"},
    {"BM25_CORPUS_VERSION": ""},
])
def test_invalid_production_or_version_configuration_fails_early(override):
    with pytest.raises(ValidationError):
        production_settings(**override)


class SnapshotStore:
    def __init__(self, version="v1"):
        self.version = version
        self.list_calls = 0

    def corpus_version(self):
        return self.version

    def list_documents(self):
        self.list_calls += 1
        return [
            VectorDocument("alpha document", {"source": "a.txt", "chunk_id": 1}),
            VectorDocument("beta document", {"source": "b.txt", "chunk_id": 2}),
        ]


def test_bm25_snapshot_version_match_mismatch_and_no_request_time_rebuild():
    store = SnapshotStore()
    bm25.clear_bm25_snapshot()
    with pytest.raises(bm25.BM25SnapshotUnavailable):
        bm25.bm25_search("alpha", vector_store=store)
    assert store.list_calls == 0

    bm25.build_bm25(store, expected_version="v1")
    assert bm25.loaded_corpus_version == "v1"
    assert bm25.check_bm25_readiness(store, "v1").ready
    store.version = "v2"
    stale = bm25.check_bm25_readiness(store, "v1")
    assert (stale.ready, stale.status, stale.loaded_version) == (False, "bm25_version_mismatch", "v1")
    assert store.list_calls == 1
    bm25.clear_bm25_snapshot()


def test_bm25_build_refuses_unpublished_or_unexpected_version():
    bm25.clear_bm25_snapshot()
    store = SnapshotStore(version="other")
    with pytest.raises(bm25.BM25SnapshotUnavailable):
        bm25.build_bm25(store, expected_version="expected")
    assert store.list_calls == 0


class Collection:
    metadata = {"polymind_corpus_version": "v1"}

    def query(self, **_kwargs):
        return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

    def modify(self, metadata):
        self.metadata = metadata


class Client:
    def __init__(self):
        self.collection = Collection()
        self.get_calls = 0
        self.create_calls = 0

    def get_collection(self, name):
        self.get_calls += 1
        return self.collection

    def get_or_create_collection(self, name):
        self.create_calls += 1
        return self.collection


def test_serving_store_is_query_only_and_admin_mutation_is_explicit():
    client = Client()
    serving = ChromaVectorStore(client, "knowledge", "chroma_http")
    serving.similarity_search([0.1], 1)
    assert (client.get_calls, client.create_calls) == (1, 0)
    with pytest.raises(VectorStoreError, match="vector_write_forbidden"):
        serving.publish_corpus_version("v2")
    with pytest.raises(VectorStoreError, match="vector_write_forbidden"):
        serving.upsert(["id"], ["doc"], [[0.1]], [{"source": "a"}])

    admin = ChromaVectorStore(client, "knowledge", "chroma_http", administrative=True)
    admin.publish_corpus_version("v2")
    assert client.create_calls == 1
    assert client.collection.metadata["polymind_corpus_version"] == "v2"


def test_serving_store_refreshes_published_corpus_version():
    class VersionedClient:
        def __init__(self):
            self.version = "v1"
            self.calls = 0

        def get_collection(self, name):
            assert name == "knowledge"
            self.calls += 1
            return SimpleNamespace(metadata={"polymind_corpus_version": self.version})

    client = VersionedClient()
    store = ChromaVectorStore(client, "knowledge", "chroma_http")
    assert store.corpus_version() == "v1"
    client.version = "v2"
    assert store.corpus_version() == "v2"
    assert client.calls == 2


def test_ingestion_publishes_version_only_after_all_upserts(monkeypatch, tmp_path):
    document = tmp_path / "doc.txt"
    document.write_text("content", encoding="utf-8")
    calls = []

    class Store:
        def upsert(self, **kwargs):
            calls.append(("upsert", kwargs["ids"][0]))

        def publish_corpus_version(self, version):
            calls.append(("publish", version))

    monkeypatch.setattr(ingest, "DOCS_PATH", Path(tmp_path))
    monkeypatch.setattr(ingest, "load_document", lambda path: "content")
    monkeypatch.setattr(ingest, "chunk_text", lambda text: ["same chunk"])
    monkeypatch.setattr(ingest, "get_embedding", lambda text: [0.1])
    monkeypatch.setattr(ingest.settings, "BM25_CORPUS_VERSION", "release-7")
    store = Store()
    ingest.ingest_documents(store)
    first = list(calls)
    calls.clear()
    ingest.ingest_documents(store)
    assert first[0] == calls[0]
    assert first[-1] == calls[-1] == ("publish", "release-7")


def test_lifespan_degrades_on_startup_failure_and_runs_cleanup(monkeypatch):
    from api import app as api_module

    calls = []
    monkeypatch.setattr(api_module, "build_bm25", lambda: (_ for _ in ()).throw(VectorStoreError("vector_unreachable")))
    monkeypatch.setattr(api_module, "clear_bm25_snapshot", lambda: calls.append("bm25"))
    monkeypatch.setattr(api_module, "close_memory_store", lambda: calls.append("memory"))
    monkeypatch.setattr(api_module, "close_vector_store", lambda: calls.append("vector"))
    monkeypatch.setattr(api_module.inference_provider, "close", lambda: calls.append("inference"), raising=False)

    async def exercise():
        async with api_module.lifespan(api_module.app):
            assert calls == []

    asyncio.run(exercise())
    assert calls == ["bm25", "memory", "vector", "inference"]


def test_deployment_metrics_have_no_corpus_version_label():
    from llm.metrics import Metrics
    from prometheus_client import CollectorRegistry

    metric_store = Metrics(CollectorRegistry())
    metric_store.set_component_readiness("bm25", False)
    metric_store.observe_bm25_build(0.1, False)
    output = metric_store.render().decode()
    assert 'component_readiness{component="bm25"} 0.0' in output
    assert "corpus_version" not in output


def test_embedding_and_ingestion_modules_import_without_constructing_model():
    import subprocess
    import sys

    completed = subprocess.run(
        [sys.executable, "-c", "import rag.embeddings, rag.ingest; print('safe')"],
        check=True, capture_output=True, text=True, timeout=20,
    )
    assert completed.stdout.strip() == "safe"
