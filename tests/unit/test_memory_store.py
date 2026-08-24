import json
import threading

import pytest
from prometheus_client import CollectorRegistry
from pydantic import ValidationError

from config.settings import Settings
from llm.metrics import Metrics
from memory import memory_store as memory_module
from memory.memory_store import (
    FileMemoryStore,
    MemoryProtocolError,
    MemoryReadError,
    MemoryTimeoutError,
    MemoryUnavailableError,
    MemoryWriteError,
    RedisMemoryStore,
)


class FakePipeline:
    def __init__(self, client):
        self.client = client
        self.commands = []

    def rpush(self, key, *values):
        self.commands.append(("rpush", key, values))
        return self

    def ltrim(self, key, start, end):
        self.commands.append(("ltrim", key, start, end))
        return self

    def expire(self, key, ttl):
        self.commands.append(("expire", key, ttl))
        return self

    def execute(self):
        if self.client.write_error:
            raise self.client.write_error
        with self.client.lock:
            for command in self.commands:
                if command[0] == "rpush":
                    self.client.data.setdefault(command[1], []).extend(command[2])
                elif command[0] == "ltrim":
                    self.client.data[command[1]] = self.client.data.get(command[1], [])[command[2]:]
                else:
                    self.client.expirations[command[1]] = command[2]
        return [True] * len(self.commands)


class FakeRedis:
    def __init__(self):
        self.data = {}
        self.expirations = {}
        self.lock = threading.Lock()
        self.read_error = None
        self.write_error = None
        self.ping_result = True
        self.pipeline_transactions = []
        self.closed = False

    def pipeline(self, transaction):
        self.pipeline_transactions.append(transaction)
        return FakePipeline(self)

    def lrange(self, key, start, end):
        if self.read_error:
            raise self.read_error
        return self.data.get(key, [])[start:]

    def delete(self, key):
        if self.write_error:
            raise self.write_error
        self.data.pop(key, None)

    def ping(self):
        if self.read_error:
            raise self.read_error
        return self.ping_result

    def close(self):
        self.closed = True


def contents(history):
    return [(message["role"], message["content"]) for message in history]


def test_file_contract_empty_append_order_limit_isolation_and_clear(tmp_path, monkeypatch):
    monkeypatch.setattr(memory_module, "metrics", Metrics(CollectorRegistry()))
    store = FileMemoryStore(str(tmp_path / "history.json"), history_limit=4)
    assert store.get_history("a") == []
    store.append_exchange("a", "q1", "a1")
    store.append_exchange("b", "qb", "ab")
    store.append_exchange("a", "q2", "a2")
    store.append_exchange("a", "q3", "a3")
    assert contents(store.get_history("a")) == [("user", "q2"), ("assistant", "a2"), ("user", "q3"), ("assistant", "a3")]
    assert contents(store.get_history("b")) == [("user", "qb"), ("assistant", "ab")]
    store.clear_session("a")
    assert store.get_history("a") == []
    assert len(store.get_history("b")) == 2


def test_file_concurrent_exchanges_do_not_lose_updates(tmp_path, monkeypatch):
    monkeypatch.setattr(memory_module, "metrics", Metrics(CollectorRegistry()))
    store = FileMemoryStore(str(tmp_path / "history.json"), history_limit=100)
    barrier = threading.Barrier(9)

    def append(number):
        barrier.wait()
        store.append_exchange("shared", f"q{number}", f"a{number}")

    threads = [threading.Thread(target=append, args=(number,)) for number in range(8)]
    for thread in threads:
        thread.start()
    barrier.wait()
    for thread in threads:
        thread.join()
    history = store.get_history("shared")
    assert len(history) == 16
    for number in range(8):
        query_index = next(index for index, item in enumerate(history) if item["content"] == f"q{number}")
        assert history[query_index + 1]["content"] == f"a{number}"


def test_redis_atomic_append_order_trim_ttl_isolation_and_clear(monkeypatch):
    monkeypatch.setattr(memory_module, "metrics", Metrics(CollectorRegistry()))
    client = FakeRedis()
    store = RedisMemoryStore(client, history_limit=4, ttl_seconds=60)
    store.append_exchange("a/path:session", "q1", "a1")
    store.append_exchange("a/path:session", "q2", "a2")
    store.append_exchange("a/path:session", "q3", "a3")
    store.append_exchange("other", "qb", "ab")
    assert contents(store.get_history("a/path:session")) == [("user", "q2"), ("assistant", "a2"), ("user", "q3"), ("assistant", "a3")]
    assert len(store.get_history("other")) == 2
    assert all(client.pipeline_transactions)
    assert client.expirations[store._key("a/path:session")] == 60
    assert "a/path:session" not in store._key("a/path:session")
    store.clear_session("a/path:session")
    assert store.get_history("a/path:session") == []


def test_redis_concurrent_appends_are_atomic_pairs(monkeypatch):
    monkeypatch.setattr(memory_module, "metrics", Metrics(CollectorRegistry()))
    client = FakeRedis()
    store = RedisMemoryStore(client, history_limit=100)
    threads = [threading.Thread(target=store.append_exchange, args=("shared", f"q{i}", f"a{i}")) for i in range(12)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    history = store.get_history("shared")
    assert len(history) == 24
    assert all(history[index]["role"] == "user" and history[index + 1]["role"] == "assistant" for index in range(0, 24, 2))


@pytest.mark.parametrize("error,expected", [(ConnectionError("private"), MemoryUnavailableError), (TimeoutError("private"), MemoryTimeoutError)])
def test_redis_read_operational_errors_are_normalized(error, expected, monkeypatch):
    monkeypatch.setattr(memory_module, "metrics", Metrics(CollectorRegistry()))
    client = FakeRedis()
    client.read_error = error
    with pytest.raises(expected, match="Conversation memory") as caught:
        RedisMemoryStore(client, 6).get_history("session")
    assert "private" not in str(caught.value)


def test_redis_malformed_read_and_generic_read_write_failures(monkeypatch):
    monkeypatch.setattr(memory_module, "metrics", Metrics(CollectorRegistry()))
    client = FakeRedis()
    store = RedisMemoryStore(client, 6)
    client.data[store._key("session")] = [b"not-json"]
    with pytest.raises(MemoryProtocolError):
        store.get_history("session")
    client.data.clear()
    client.read_error = RuntimeError("private")
    with pytest.raises(MemoryReadError):
        store.get_history("session")
    client.read_error = None
    client.write_error = RuntimeError("private")
    with pytest.raises(MemoryWriteError):
        store.append_exchange("session", "q", "a")
    assert store.get_history("session") == []


def test_memory_metrics_are_bounded(monkeypatch):
    metric_store = Metrics(CollectorRegistry())
    monkeypatch.setattr(memory_module, "metrics", metric_store)
    store = RedisMemoryStore(FakeRedis(), 6)
    store.append_exchange("secret-session", "private query", "private answer")
    store.get_history("secret-session")
    output = metric_store.render().decode()
    assert 'memory_operations_total{operation="append",outcome="success",provider="redis"} 1.0' in output
    assert "secret-session" not in output
    assert "private query" not in output
    assert "request_id" not in output


def test_memory_configuration_validation():
    assert Settings(MEMORY_PROVIDER="file").MEMORY_PROVIDER == "file"
    assert Settings(MEMORY_PROVIDER="redis", REDIS_URL="redis://memory:6379/0").MEMORY_PROVIDER == "redis"
    for values in (
        {"MEMORY_PROVIDER": "unknown"}, {"MEMORY_HISTORY": 0}, {"MEMORY_TTL": -1},
        {"MEMORY_CONNECT_TIMEOUT": 0}, {"MEMORY_OPERATION_TIMEOUT": 0},
        {"MEMORY_PROVIDER": "redis", "REDIS_URL": ""},
    ):
        with pytest.raises(ValidationError):
            Settings(**values)
