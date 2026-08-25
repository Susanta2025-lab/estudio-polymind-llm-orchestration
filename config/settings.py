from typing import Any, Dict, Literal, Optional
from urllib.parse import urlparse
import re

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DEPLOYMENT_ENV: Literal["local", "compose", "production"] = "local"

    # =========================
    # Inference providers
    # =========================
    INFERENCE_PROVIDER: Literal["ollama", "openai_compatible"] = "ollama"
    OLLAMA_URL: str = "http://localhost:11434/api/chat"
    INFERENCE_CONNECT_TIMEOUT: float = Field(default=5.0, gt=0)
    INFERENCE_READ_TIMEOUT: float = Field(default=120.0, gt=0)
    OLLAMA_MODEL_MAP: Dict[str, str] = Field(
        default_factory=lambda: {
            "general": "mistral",
            "coding": "qwen2.5:3b",
            "summarization": "gemma2:2b",
            "fast": "phi3:mini",
        }
    )
    OPENAI_COMPATIBLE_BASE_URL: str = "http://localhost:8000/v1"
    OPENAI_COMPATIBLE_API_KEY: Optional[str] = None
    OPENAI_COMPATIBLE_CONNECT_TIMEOUT: float = Field(default=5.0, gt=0)
    OPENAI_COMPATIBLE_READ_TIMEOUT: float = Field(default=120.0, gt=0)
    OPENAI_COMPATIBLE_MODEL_MAP: Dict[str, str] = Field(
        default_factory=lambda: {
            "general": "gpt-oss-20b",
            "coding": "gpt-oss-20b",
            "summarization": "gpt-oss-20b",
            "fast": "gpt-oss-20b",
        }
    )
    OPENAI_COMPATIBLE_GENERATION_PARAMETERS: Dict[str, Any] = Field(
        default_factory=dict
    )
    PROVIDER_READINESS_TIMEOUT: float = Field(default=3.0, gt=0)
    PROVIDER_READINESS_RETRIES: int = Field(default=1, ge=0, le=5)
    PROVIDER_READINESS_BACKOFF: float = Field(default=0.1, ge=0, le=5)

    # =========================
    # FastAPI Server
    # =========================
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8001
    API_AUTH_ENABLED: bool = False
    API_AUTH_TOKEN: Optional[SecretStr] = None
    API_DOCS_ENABLED: bool = True
    MAX_REQUEST_BYTES: int = Field(default=1_048_576, ge=1, le=10_485_760)

    # =========================
    # Vector store
    # =========================
    VECTOR_STORE_PROVIDER: Literal["chroma_local", "chroma_http"] = "chroma_local"
    CHROMA_PATH: str = "./chroma_db"
    VECTOR_STORE_HOST: str = "localhost"
    VECTOR_STORE_PORT: int = Field(default=8000, ge=1, le=65535)
    VECTOR_STORE_SSL: bool = False
    VECTOR_STORE_COLLECTION: str = "knowledge_base"
    VECTOR_STORE_TIMEOUT: float = Field(default=5.0, gt=0)
    BM25_CORPUS_VERSION: str = "development"

    # =========================
    # Retrieval
    # =========================
    RETRIEVAL_TOP_K: int = 5
    RERANK_TOP_K: int = 3

    # =========================
    # Memory
    # =========================
    MEMORY_PROVIDER: Literal["file", "redis"] = "file"
    MEMORY_FILE: str = "memory/chat_history.json"
    MEMORY_HISTORY: int = Field(default=6, gt=0)
    REDIS_URL: str = "redis://localhost:6379/0"
    MEMORY_CONNECT_TIMEOUT: float = Field(default=2.0, gt=0)
    MEMORY_OPERATION_TIMEOUT: float = Field(default=2.0, gt=0)
    MEMORY_TTL: int = Field(default=0, ge=0)

    # =========================
    # API (IMPORTANT FIX)
    # =========================
    API_URL: str = "http://127.0.0.1:8001/query"
    STREAM_URL: str = "http://127.0.0.1:8001/query/stream"
    REQUEST_TIMEOUT: int = 120

    # =========================
    # Pydantic Config
    # =========================
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @model_validator(mode="after")
    def validate_inference_configuration(self):
        required = {"general", "coding", "summarization", "fast"}
        name, model_map = (
            ("OLLAMA_MODEL_MAP", self.OLLAMA_MODEL_MAP)
            if self.INFERENCE_PROVIDER == "ollama"
            else ("OPENAI_COMPATIBLE_MODEL_MAP", self.OPENAI_COMPATIBLE_MODEL_MAP)
        )
        missing = required.difference(model_map)
        empty = {
            key
            for key, value in model_map.items()
            if not isinstance(value, str) or not value.strip()
        }
        if missing or empty:
            details = sorted(missing | empty)
            raise ValueError(f"{name} has missing or empty roles: {details}")

        if (
            self.INFERENCE_PROVIDER == "openai_compatible"
            and not self.OPENAI_COMPATIBLE_BASE_URL.strip()
        ):
            raise ValueError("OPENAI_COMPATIBLE_BASE_URL must not be empty")

        reserved = (
            {"model", "messages", "stream"}.intersection(
                self.OPENAI_COMPATIBLE_GENERATION_PARAMETERS
            )
            if self.INFERENCE_PROVIDER == "openai_compatible"
            else set()
        )
        if reserved:
            raise ValueError(
                "OPENAI_COMPATIBLE_GENERATION_PARAMETERS contains reserved keys: "
                f"{sorted(reserved)}"
            )
        if self.MEMORY_PROVIDER == "redis" and not self.REDIS_URL.strip():
            raise ValueError("REDIS_URL must not be empty when MEMORY_PROVIDER=redis")
        if not self.VECTOR_STORE_COLLECTION.strip():
            raise ValueError("VECTOR_STORE_COLLECTION must not be empty")
        if self.VECTOR_STORE_PROVIDER == "chroma_local" and not self.CHROMA_PATH.strip():
            raise ValueError("CHROMA_PATH must not be empty for chroma_local")
        if self.VECTOR_STORE_PROVIDER == "chroma_http" and not self.VECTOR_STORE_HOST.strip():
            raise ValueError("VECTOR_STORE_HOST must not be empty for chroma_http")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", self.BM25_CORPUS_VERSION):
            raise ValueError("BM25_CORPUS_VERSION must be a safe 1-64 character identifier")

        active_endpoint = (
            ("OLLAMA_URL", self.OLLAMA_URL)
            if self.INFERENCE_PROVIDER == "ollama"
            else ("OPENAI_COMPATIBLE_BASE_URL", self.OPENAI_COMPATIBLE_BASE_URL)
        )
        for name, value in (active_endpoint,):
            parsed = urlparse(value)
            if parsed.scheme not in {"http", "https"} or not parsed.hostname:
                raise ValueError(f"{name} must be an HTTP(S) URL")

        if self.MEMORY_PROVIDER == "redis":
            parsed = urlparse(self.REDIS_URL)
            if parsed.scheme not in {"redis", "rediss"} or not parsed.hostname:
                raise ValueError("REDIS_URL must be a valid Redis URL")

        if self.DEPLOYMENT_ENV == "production":
            if self.INFERENCE_PROVIDER != "openai_compatible":
                raise ValueError("production requires INFERENCE_PROVIDER=openai_compatible")
            if self.MEMORY_PROVIDER != "redis":
                raise ValueError("production requires MEMORY_PROVIDER=redis")
            if self.VECTOR_STORE_PROVIDER != "chroma_http":
                raise ValueError("production requires VECTOR_STORE_PROVIDER=chroma_http")
            loopback = {"localhost", "127.0.0.1", "::1", "host.docker.internal"}
            endpoints = {
                "OPENAI_COMPATIBLE_BASE_URL": urlparse(self.OPENAI_COMPATIBLE_BASE_URL).hostname,
                "REDIS_URL": urlparse(self.REDIS_URL).hostname,
                "VECTOR_STORE_HOST": self.VECTOR_STORE_HOST,
            }
            invalid = [name for name, host in endpoints.items() if host in loopback]
            if invalid:
                raise ValueError(f"production external services must not use loopback hosts: {sorted(invalid)}")
            if not self.API_AUTH_ENABLED:
                raise ValueError("production requires API_AUTH_ENABLED=true")
            if self.API_DOCS_ENABLED:
                raise ValueError("production requires API_DOCS_ENABLED=false")

        if self.API_AUTH_ENABLED:
            token = self.API_AUTH_TOKEN.get_secret_value() if self.API_AUTH_TOKEN else ""
            if len(token) < 32 or token != token.strip() or any(character.isspace() for character in token):
                raise ValueError(
                    "API_AUTH_TOKEN must contain at least 32 non-whitespace characters "
                    "and no whitespace when authentication is enabled"
                )
        return self


settings = Settings()
