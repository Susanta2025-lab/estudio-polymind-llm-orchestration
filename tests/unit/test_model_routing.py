import pytest

from config.settings import Settings
from llm.inference import ModelRole
from llm.openai_compatible import OpenAICompatibleProvider
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


def test_openai_compatible_provider_selection_and_independent_model_mapping():
    model_map = {role.value: "shared-vllm-model" for role in ModelRole}
    config = Settings(
        _env_file=None,
        INFERENCE_PROVIDER="openai_compatible",
        OPENAI_COMPATIBLE_BASE_URL="http://vllm.internal:8000/v1",
        OPENAI_COMPATIBLE_MODEL_MAP=model_map,
    )

    provider = create_inference_provider(config)

    assert isinstance(provider, OpenAICompatibleProvider)
    assert provider.name == "openai_compatible"
    assert provider.model_id(ModelRole.CODING) == "shared-vllm-model"


def test_openai_compatible_model_mapping_requires_every_logical_role():
    with pytest.raises(ValueError, match="OPENAI_COMPATIBLE_MODEL_MAP"):
        Settings(
            _env_file=None,
            INFERENCE_PROVIDER="openai_compatible",
            OPENAI_COMPATIBLE_MODEL_MAP={"general": "model"},
        )


def test_invalid_provider_configuration_fails_during_settings_initialization():
    with pytest.raises(ValueError, match="INFERENCE_PROVIDER"):
        Settings(_env_file=None, INFERENCE_PROVIDER="vllm")
