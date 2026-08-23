import pytest

from config.settings import Settings
from llm.inference import ModelRole
from llm.provider_factory import create_inference_provider
from llm.router import select_model_role


@pytest.mark.parametrize(
    ("query", "role", "served_model"),
    [
        ("hello", ModelRole.GENERAL, "mistral"),
        ("write python code", ModelRole.CODING, "qwen2.5:3b"),
        ("summarize this", ModelRole.SUMMARIZATION, "gemma2:2b"),
        ("give me a quick answer", ModelRole.FAST, "phi3:mini"),
    ],
)
def test_logical_routing_maps_to_ollama_served_models(query, role, served_model):
    config = Settings(_env_file=None)
    provider = create_inference_provider(config)

    assert select_model_role(query) is role
    assert provider.model_id(role) == served_model


def test_model_mapping_requires_every_logical_role():
    with pytest.raises(ValueError, match="missing or empty roles"):
        Settings(_env_file=None, OLLAMA_MODEL_MAP={"general": "mistral"})
