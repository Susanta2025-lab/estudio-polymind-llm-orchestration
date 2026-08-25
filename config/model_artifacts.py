"""Authoritative inventory and resolution of local control-plane models."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModelArtifact:
    role: str
    identifier: str
    revision: str
    directory: str


EMBEDDING_MODEL = ModelArtifact(
    role="embedding",
    identifier="sentence-transformers/all-MiniLM-L6-v2",
    revision="1110a243fdf4706b3f48f1d95db1a4f5529b4d41",
    directory="embedding",
)
RERANKER_MODEL = ModelArtifact(
    role="reranker",
    identifier="cross-encoder/ms-marco-MiniLM-L-6-v2",
    revision="c5ee24cb16019beea0893ab7796b1df96625c6b8",
    directory="reranker",
)
LOCAL_MODELS = (EMBEDDING_MODEL, RERANKER_MODEL)


def model_source(model: ModelArtifact, artifact_dir: str | None) -> str:
    """Return a baked path when configured, otherwise the pinned upstream ID."""
    if artifact_dir:
        return str(Path(artifact_dir) / model.directory)
    return model.identifier


def validate_model_artifacts(artifact_dir: str) -> None:
    """Fail clearly when a configured immutable model directory is incomplete."""
    root = Path(artifact_dir)
    if not root.is_absolute():
        raise ValueError("MODEL_ARTIFACT_DIR must be an absolute path")
    missing = [model.role for model in LOCAL_MODELS if not (root / model.directory / "config.json").is_file()]
    if missing:
        raise ValueError(f"missing local model artifacts for roles: {missing}")
