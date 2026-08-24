from typing import Any, Dict, Literal, Optional

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

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

    # =========================
    # Vector store
    # =========================
    VECTOR_STORE_PROVIDER: Literal["chroma_local", "chroma_http"] = "chroma_local"
    CHROMA_PATH: str = "./chroma_db"
    VECTOR_STORE_HOST: str = "localhost"
    VECTOR_STORE_PORT: int = Field(default=8000, ge=1, le=65535)
    VECTOR_STORE_SSL: bool = False
    VECTOR_STORE_COLLECTION: str = "knowledge_base"

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
        return self


settings = Settings()
