from typing import Optional

from config.settings import Settings, settings
from memory.memory_store import ConversationMemoryStore, FileMemoryStore, RedisMemoryStore

_store: Optional[ConversationMemoryStore] = None


def create_memory_store(configuration: Settings = settings) -> ConversationMemoryStore:
    if configuration.MEMORY_PROVIDER == "file":
        return FileMemoryStore(configuration.MEMORY_FILE, configuration.MEMORY_HISTORY)
    import redis
    client = redis.Redis.from_url(
        configuration.REDIS_URL,
        socket_connect_timeout=configuration.MEMORY_CONNECT_TIMEOUT,
        socket_timeout=configuration.MEMORY_OPERATION_TIMEOUT,
        decode_responses=False,
        health_check_interval=30,
    )
    return RedisMemoryStore(client, configuration.MEMORY_HISTORY, configuration.MEMORY_TTL)


def get_memory_store() -> ConversationMemoryStore:
    global _store
    if _store is None:
        _store = create_memory_store()
    return _store


def close_memory_store() -> None:
    global _store
    if _store is not None:
        _store.close()
        _store = None
