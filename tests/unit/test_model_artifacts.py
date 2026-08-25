from pathlib import Path

import pytest

from config.model_artifacts import (
    EMBEDDING_MODEL,
    LOCAL_MODELS,
    RERANKER_MODEL,
    model_source,
    validate_model_artifacts,
)


def test_local_model_inventory_is_revision_pinned_and_role_complete():
    assert LOCAL_MODELS == (EMBEDDING_MODEL, RERANKER_MODEL)
    assert {model.role for model in LOCAL_MODELS} == {"embedding", "reranker"}
    assert all(len(model.revision) == 40 for model in LOCAL_MODELS)
    assert EMBEDDING_MODEL.identifier == "sentence-transformers/all-MiniLM-L6-v2"
    assert RERANKER_MODEL.identifier == "cross-encoder/ms-marco-MiniLM-L-6-v2"


def test_model_source_prefers_baked_role_directory():
    assert model_source(EMBEDDING_MODEL, "/opt/models") == "/opt/models/embedding"
    assert model_source(EMBEDDING_MODEL, None) == EMBEDDING_MODEL.identifier


def test_artifact_validation_requires_absolute_complete_inventory(tmp_path: Path):
    with pytest.raises(ValueError, match="absolute"):
        validate_model_artifacts("relative")
    with pytest.raises(ValueError, match="embedding.*reranker"):
        validate_model_artifacts(str(tmp_path))
    for model in LOCAL_MODELS:
        directory = tmp_path / model.directory
        directory.mkdir()
        (directory / "config.json").write_text("{}")
    validate_model_artifacts(str(tmp_path))


def test_reranker_module_import_is_lazy():
    from rag import reranker

    assert reranker._reranker is None
