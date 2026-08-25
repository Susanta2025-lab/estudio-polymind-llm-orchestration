"""Fetch revision-pinned model snapshots for the production image build."""

import argparse
import shutil
from pathlib import Path

from huggingface_hub import snapshot_download

from config.model_artifacts import LOCAL_MODELS, validate_model_artifacts

REQUIRED_FILES = (
    "1_Pooling/config.json",
    "config.json",
    "config_sentence_transformers.json",
    "model.safetensors",
    "modules.json",
    "sentence_bert_config.json",
    "special_tokens_map.json",
    "tokenizer_config.json",
    "tokenizer.json",
    "vocab.txt",
)


def fetch_models(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for model in LOCAL_MODELS:
        target = destination / model.directory
        snapshot_download(
            repo_id=model.identifier,
            revision=model.revision,
            local_dir=target,
            allow_patterns=REQUIRED_FILES,
        )
        shutil.rmtree(target / ".cache", ignore_errors=True)
    validate_model_artifacts(str(destination.resolve()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", type=Path)
    fetch_models(parser.parse_args().destination)
