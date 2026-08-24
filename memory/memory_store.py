"""Provider-neutral conversation-memory stores."""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

from filelock import FileLock

from llm.metrics import metrics


class MemoryError(RuntimeError):
    """Safe, provider-neutral conversation-memory failure."""
    category = "memory_failure"


class MemoryUnavailableError(MemoryError):
    category = "memory_unreachable"


class MemoryTimeoutError(MemoryUnavailableError):
    category = "memory_timeout"


class MemoryProtocolError(MemoryError):
    category = "memory_protocol"


class MemoryReadError(MemoryError):
    category = "memory_read_failure"


class MemoryWriteError(MemoryError):
    category = "memory_write_failure"


@dataclass(frozen=True)
class MemoryReadiness:
    provider: str
    ready: bool
    status: str


@runtime_checkable
class ConversationMemoryStore(Protocol):
    @property
    def provider(self) -> str: ...
    def get_history(self, session_id: str, limit: Optional[int] = None) -> List[Dict[str, str]]: ...
    def append_exchange(self, session_id: str, query: str, answer: str) -> None: ...
    def clear_session(self, session_id: str) -> None: ...
    def check_readiness(self) -> MemoryReadiness: ...
    def close(self) -> None: ...


def _message(role: str, content: str) -> Dict[str, str]:
    return {"role": role, "content": content, "timestamp": datetime.now(timezone.utc).isoformat()}


class FileMemoryStore:
    """Locked, atomic file store for local development and a single host only."""
    provider = "file"

    def __init__(self, path: str, history_limit: int):
        self.path = Path(path)
        self.history_limit = history_limit
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._thread_lock = threading.RLock()
        self._file_lock = FileLock(f"{self.path}.lock")

    def _read_unlocked(self) -> List[Dict[str, Any]]:
        if not self.path.exists():
            return []
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise MemoryProtocolError("Conversation memory contains invalid data.") from exc
        except OSError as exc:
            raise MemoryReadError("Conversation memory could not be read.") from exc
        if not isinstance(value, list):
            raise MemoryProtocolError("Conversation memory contains invalid data.")
        return value

    def _write_unlocked(self, value: List[Dict[str, Any]]) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporary = tempfile.mkstemp(dir=self.path.parent, prefix=".memory-", suffix=".json")
            try:
                with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                    json.dump(value, handle, indent=2, ensure_ascii=False)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(temporary, self.path)
            except BaseException:
                if os.path.exists(temporary):
                    os.unlink(temporary)
                raise
        except OSError as exc:
            raise MemoryWriteError("Conversation memory could not be written.") from exc

    def get_history(self, session_id: str, limit: Optional[int] = None) -> List[Dict[str, str]]:
        with metrics.memory(self.provider, "read"):
            with self._thread_lock, self._file_lock:
                history = [item for item in self._read_unlocked() if item.get("session_id") == session_id]
            effective_limit = self.history_limit if limit is None else limit
            return history[-effective_limit:] if effective_limit else []

    def append_exchange(self, session_id: str, query: str, answer: str) -> None:
        with metrics.memory(self.provider, "append"):
            with self._thread_lock, self._file_lock:
                data = self._read_unlocked()
                for item in (_message("user", query), _message("assistant", answer)):
                    data.append({"session_id": session_id, **item})
                indexes = [index for index, item in enumerate(data) if item.get("session_id") == session_id]
                remove = set(indexes[:-self.history_limit])
                if remove:
                    data = [item for index, item in enumerate(data) if index not in remove]
                self._write_unlocked(data)

    def clear_session(self, session_id: str) -> None:
        with metrics.memory(self.provider, "clear"):
            with self._thread_lock, self._file_lock:
                self._write_unlocked([item for item in self._read_unlocked() if item.get("session_id") != session_id])

    def clear_all(self) -> None:
        with metrics.memory(self.provider, "clear"):
            with self._thread_lock, self._file_lock:
                self._write_unlocked([])

    def check_readiness(self) -> MemoryReadiness:
        started = time.perf_counter()
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            ready = os.access(self.path.parent, os.W_OK) and (not self.path.exists() or os.access(self.path, os.R_OK | os.W_OK))
        except OSError:
            ready = False
        result = MemoryReadiness(self.provider, ready, "ready" if ready else "memory_unavailable")
        metrics.observe_memory_readiness(result, time.perf_counter() - started)
        return result

    def close(self) -> None:
        return None


class RedisMemoryStore:
    """Shared store using one atomic Redis transaction per exchange."""
    provider = "redis"

    def __init__(self, client: Any, history_limit: int, ttl_seconds: int = 0, key_prefix: str = "polymind:memory"):
        self.client = client
        self.history_limit = history_limit
        self.ttl_seconds = ttl_seconds
        self.key_prefix = key_prefix

    def _key(self, session_id: str) -> str:
        return f"{self.key_prefix}:{hashlib.sha256(session_id.encode('utf-8')).hexdigest()}"

    @staticmethod
    def _normalize_error(exc: BaseException, operation: str) -> MemoryError:
        name = type(exc).__name__.lower()
        if "timeout" in name:
            return MemoryTimeoutError("Conversation memory timed out.")
        if "connection" in name:
            return MemoryUnavailableError("Conversation memory is unavailable.")
        error_type = MemoryReadError if operation == "read" else MemoryWriteError
        return error_type("Conversation memory operation failed.")

    def get_history(self, session_id: str, limit: Optional[int] = None) -> List[Dict[str, str]]:
        with metrics.memory(self.provider, "read"):
            effective_limit = self.history_limit if limit is None else limit
            if effective_limit == 0:
                return []
            try:
                values = self.client.lrange(self._key(session_id), -effective_limit, -1)
            except Exception as exc:
                raise self._normalize_error(exc, "read") from exc
            history = []
            for value in values:
                try:
                    if isinstance(value, bytes):
                        value = value.decode("utf-8")
                    message = json.loads(value)
                    if (
                        not isinstance(message, dict)
                        or message.get("role") not in {"user", "assistant"}
                        or not isinstance(message.get("content"), str)
                        or not isinstance(message.get("timestamp"), str)
                    ):
                        raise ValueError
                    history.append(message)
                except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
                    raise MemoryProtocolError("Conversation memory contains invalid data.") from exc
            return history

    def append_exchange(self, session_id: str, query: str, answer: str) -> None:
        with metrics.memory(self.provider, "append"):
            key = self._key(session_id)
            values = [json.dumps(_message("user", query)), json.dumps(_message("assistant", answer))]
            try:
                pipeline = self.client.pipeline(transaction=True)
                pipeline.rpush(key, *values)
                pipeline.ltrim(key, -self.history_limit, -1)
                if self.ttl_seconds:
                    pipeline.expire(key, self.ttl_seconds)
                pipeline.execute()
            except Exception as exc:
                raise self._normalize_error(exc, "write") from exc

    def clear_session(self, session_id: str) -> None:
        with metrics.memory(self.provider, "clear"):
            try:
                self.client.delete(self._key(session_id))
            except Exception as exc:
                raise self._normalize_error(exc, "write") from exc

    def check_readiness(self) -> MemoryReadiness:
        started = time.perf_counter()
        try:
            ready = bool(self.client.ping())
            result = MemoryReadiness(self.provider, ready, "ready" if ready else "memory_unavailable")
        except Exception as exc:
            result = MemoryReadiness(self.provider, False, self._normalize_error(exc, "read").category)
        metrics.observe_memory_readiness(result, time.perf_counter() - started)
        return result

    def close(self) -> None:
        self.client.close()


__all__ = ["ConversationMemoryStore", "FileMemoryStore", "MemoryError", "MemoryProtocolError", "MemoryReadError", "MemoryReadiness", "MemoryTimeoutError", "MemoryUnavailableError", "MemoryWriteError", "RedisMemoryStore"]
