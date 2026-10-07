"""Optional extraction-plane configuration; does not alter API request limits."""

from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ExtractionSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DOCUMENT_", frozen=True, extra="ignore")
    # No root default: the embedding application must choose an isolated directory.
    storage_root: Path | None = None
    max_source_bytes: int = Field(default=16_000_000, gt=0)
    max_pages: int = Field(default=1000, gt=0)
    max_characters: int = Field(default=4_000_000, gt=0)
    max_blocks: int = Field(default=100_000, gt=0)
    max_artifact_bytes: int = Field(default=32_000_000, gt=0)
