from typing import Dict, Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # =========================
    # LLM (Ollama)
    # =========================
    INFERENCE_PROVIDER: Literal["ollama"] = "ollama"
    OLLAMA_URL: str = "http://localhost:11434/api/chat"
    INFERENCE_CONNECT_TIMEOUT: float = Field(default=5.0, gt=0)
    INFERENCE_READ_TIMEOUT: float = Field(default=120.0, gt=0)
    OLLAMA_MODEL_MAP: Dict[str, str] = {
        "general": "mistral",
        "coding": "qwen2.5:3b",
        "summarization": "gemma2:2b",
        "fast": "phi3:mini",
    }

    # =========================
    # FastAPI Server
    # =========================
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8001

    # =========================
    # ChromaDB
    # =========================
    CHROMA_PATH: str = "./chroma_db"

    # =========================
    # Retrieval
    # =========================
    RETRIEVAL_TOP_K: int = 5
    RERANK_TOP_K: int = 3

    # =========================
    # Memory
    # =========================
    MEMORY_HISTORY: int = 6

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
    def validate_model_map(self):
        required = {"general", "coding", "summarization", "fast"}
        missing = required.difference(self.OLLAMA_MODEL_MAP)
        empty = {key for key, value in self.OLLAMA_MODEL_MAP.items() if not value.strip()}
        if missing or empty:
            details = sorted(missing | empty)
            raise ValueError(f"OLLAMA_MODEL_MAP has missing or empty roles: {details}")
        return self


settings = Settings()
