from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):

    # =========================
    # LLM (Ollama)
    # =========================
    OLLAMA_URL: str = os.getenv(
        "OLLAMA_URL",
        "http://localhost:11434/api/chat"
    )

    # =========================
    # FastAPI Server
    # =========================
    API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
    API_PORT: int = int(os.getenv("API_PORT", 8001))

    # =========================
    # ChromaDB
    # =========================
    CHROMA_PATH: str = os.getenv("CHROMA_PATH", "./chroma_db")

    # =========================
    # Retrieval
    # =========================
    RETRIEVAL_TOP_K: int = int(os.getenv("RETRIEVAL_TOP_K", 5))
    RERANK_TOP_K: int = int(os.getenv("RERANK_TOP_K", 3))

    # =========================
    # Memory
    # =========================
    MEMORY_HISTORY: int = int(os.getenv("MEMORY_HISTORY", 6))

    # =========================
    # API (IMPORTANT FIX)
    # =========================
    API_URL: str = os.getenv(
        "API_URL",
        "http://127.0.0.1:8001/query"
    )

    STREAM_URL: str = os.getenv(
        "STREAM_URL",
        "http://127.0.0.1:8001/query/stream"
    )

    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", 120))

    # =========================
    # Pydantic Config
    # =========================
    class Config:
        env_file = ".env"


settings = Settings()
