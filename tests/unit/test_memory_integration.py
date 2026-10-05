import sys
import socket
import ssl
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from config.settings import Settings
from graph.generation import persist_exchange
from memory import provider_factory
from memory.memory_store import MemoryReadiness, MemoryUnavailableError, RedisMemoryStore
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


@pytest.mark.parametrize("url", [
    "redis://shared:6379/2",
    "rediss://:phase16-password@redis.example.invalid:6380/0",
    "rediss://phase16-user:phase16-password@redis.example.invalid:6380/0",
])
def test_redis_factory_uses_pool_configuration_without_connecting(monkeypatch, url):
    calls = []
    client = object()

    class Redis:
        @staticmethod
        def from_url(*args, **kwargs):
            calls.append((args, kwargs))
            return client

    monkeypatch.setitem(sys.modules, "redis", SimpleNamespace(Redis=Redis))
    settings = Settings(
        _env_file=None, MEMORY_PROVIDER="redis", REDIS_URL=url,
        MEMORY_CONNECT_TIMEOUT=1.5, MEMORY_OPERATION_TIMEOUT=2.5,
        MEMORY_HISTORY=8, MEMORY_TTL=30,
    )
    store = create_memory_store(settings)
    assert isinstance(store, RedisMemoryStore)
    assert settings.REDIS_URL == url
    assert store.client is client
    assert store.history_limit == 8
    assert store.ttl_seconds == 30
    assert calls == [((url,), {
        "socket_connect_timeout": 1.5, "socket_timeout": 2.5,
        "decode_responses": False, "health_check_interval": 30,
    })]


@pytest.mark.parametrize("username", [None, "phase16-user"])
def test_pinned_redis_tls_and_static_auth_parsing_without_network(monkeypatch, username):
    redis = pytest.importorskip("redis", reason="Pinned redis==6.4.0 is not installed locally")
    assert redis.__version__ == "6.4.0"

    def forbid_network(*args, **kwargs):
        pytest.fail("Redis construction must not resolve DNS or open a socket")

    monkeypatch.setattr(socket, "getaddrinfo", forbid_network)
    monkeypatch.setattr(socket, "socket", forbid_network)
    monkeypatch.setattr(redis.connection.Connection, "connect", forbid_network)
    configuration = Settings(
        _env_file=None, MEMORY_PROVIDER="redis",
        REDIS_URL=f"rediss://{username or ''}:phase16-password%40test@redis.example.invalid:6380/0",
        MEMORY_CONNECT_TIMEOUT=1.5, MEMORY_OPERATION_TIMEOUT=2.5,
    )
    store = create_memory_store(configuration)
    try:
        pool = store.client.connection_pool
        assert pool.connection_class is redis.connection.SSLConnection
        options = pool.connection_kwargs
        assert options.get("username") == username
        assert options["password"] == "phase16-password@test"
        assert (options["host"], options["port"], options["db"]) == ("redis.example.invalid", 6380, 0)
        assert options["socket_connect_timeout"] == 1.5
        assert options["socket_timeout"] == 2.5
        assert options["decode_responses"] is False
        assert options["health_check_interval"] == 30
        connection = pool.connection_class(**options)
        try:
            assert connection.cert_reqs == ssl.CERT_REQUIRED
            assert connection.check_hostname is True
        finally:
            connection.disconnect()
    finally:
        store.close()


@pytest.mark.parametrize("failure_point", ["construction", "runtime"])
def test_redis_failures_never_fall_back_to_file(monkeypatch, tmp_path, failure_point):
    file_store = Mock(side_effect=AssertionError("File memory must never be constructed"))
    monkeypatch.setattr(provider_factory, "FileMemoryStore", file_store)
    failure = ConnectionError("synthetic Redis outage")
    client = SimpleNamespace(
        lrange=Mock(side_effect=failure), ping=Mock(side_effect=failure), close=Mock(),
    )
    constructor = Mock(return_value=client)
    if failure_point == "construction":
        constructor.side_effect = failure
    monkeypatch.setitem(sys.modules, "redis", SimpleNamespace(Redis=SimpleNamespace(from_url=constructor)))
    configuration = Settings(
        _env_file=None, MEMORY_PROVIDER="redis",
        REDIS_URL="rediss://redis.example.invalid:6380/0",
        MEMORY_FILE=str(tmp_path / "must-not-exist" / "history.json"),
    )
    if failure_point == "construction":
        with pytest.raises(ConnectionError) as caught:
            create_memory_store(configuration)
        assert caught.value is failure
    else:
        store = create_memory_store(configuration)
        try:
            with pytest.raises(MemoryUnavailableError) as caught:
                store.get_history("phase16-session")
            assert caught.value.__cause__ is failure
            assert store.check_readiness() == MemoryReadiness("redis", False, "memory_unreachable")
            assert store.provider == "redis"
        finally:
            store.close()
        client.close.assert_called_once_with()
    file_store.assert_not_called()
    assert configuration.MEMORY_PROVIDER == "redis"
    assert list(tmp_path.iterdir()) == []
