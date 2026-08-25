"""Offline smoke test for the immutable production image's local ML runtime."""

import os
import time

import torch

from config.model_artifacts import validate_model_artifacts
from graph.semantic_router import semantic_route
from rag.embeddings import get_embedding
from rag.reranker import rerank


def timed(label, operation):
    started = time.perf_counter()
    result = operation()
    print(f"{label}_seconds={time.perf_counter() - started:.3f}")
    return result


def main() -> None:
    if os.environ.get("HF_HUB_OFFLINE") != "1" or os.environ.get("TRANSFORMERS_OFFLINE") != "1":
        raise RuntimeError("offline Hugging Face mode is required")
    validate_model_artifacts(os.environ["MODEL_ARTIFACT_DIR"])
    print(f"uid={os.getuid()} gid={os.getgid()}")
    print(f"torch={torch.__version__} cuda={torch.version.cuda}")
    import api.app  # noqa: F401 -- application import is part of the smoke contract

    embedding = timed("embedding_load_and_encode", lambda: get_embedding("offline model validation"))
    if len(embedding) != 384:
        raise RuntimeError(f"unexpected embedding dimension: {len(embedding)}")
    ranked = timed(
        "reranker_load_and_predict",
        lambda: rerank(
            "relevant",
            [{"text": "relevant document"}, {"text": "unrelated material"}],
            1,
        ),
    )
    if len(ranked) != 1:
        raise RuntimeError("reranker returned an unexpected result count")
    route = timed("semantic_router", lambda: semantic_route("search my knowledge base"))
    if route != "rag":
        raise RuntimeError(f"unexpected semantic route: {route}")
    print("offline_model_validation=passed")


if __name__ == "__main__":
    main()
