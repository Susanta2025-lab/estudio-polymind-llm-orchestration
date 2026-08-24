import sys
from types import SimpleNamespace

from config.settings import Settings
from graph.generation import persist_exchange
from memory.memory_store import MemoryReadiness
from memory.provider_factory import create_memory_store


class Store:
    provider = "fake"

    def __init__(self):
        self.history = []
        self.appends = []

    def get_history(self, session_id, limit=None):
        return self.history

    def append_exchange(self, session_id, query, answer):
        self.appends.append((session_id, query, answer))

    def clear_session(self, session_id):
        self.history = []

    def check_readiness(self):
        return MemoryReadiness("fake", True, "ready")

    def close(self):
        pass


def test_exchange_persistence_uses_injected_store_exactly_once():
    store = Store()
    persist_exchange("question", "answer", "session", store)
    assert store.appends == [("session", "question", "answer")]


def test_redis_factory_uses_pool_configuration_without_connecting(monkeypatch):
    calls = []
    client = object()

    class Redis:
        @staticmethod
        def from_url(*args, **kwargs):
            calls.append((args, kwargs))
            return client

    monkeypatch.setitem(sys.modules, "redis", SimpleNamespace(Redis=Redis))
    settings = Settings(
        MEMORY_PROVIDER="redis", REDIS_URL="redis://shared:6379/2",
        MEMORY_CONNECT_TIMEOUT=1.5, MEMORY_OPERATION_TIMEOUT=2.5,
        MEMORY_HISTORY=8, MEMORY_TTL=30,
    )
    store = create_memory_store(settings)
    assert store.client is client
    assert store.history_limit == 8
    assert store.ttl_seconds == 30
    assert calls == [(('redis://shared:6379/2',), {
        "socket_connect_timeout": 1.5, "socket_timeout": 2.5,
        "decode_responses": False, "health_check_interval": 30,
    })]
