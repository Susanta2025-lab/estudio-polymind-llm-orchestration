from llm.inference import ModelRole


DEFAULT_OLLAMA_MODELS = {
    ModelRole.GENERAL: "mistral",
    ModelRole.CODING: "qwen2.5:3b",
    ModelRole.SUMMARIZATION: "gemma2:2b",
    ModelRole.FAST: "phi3:mini",
}

# Kept for compatibility with existing experiment scripts. Application code routes
# by ModelRole and leaves served-model resolution to the inference adapter.
AVAILABLE_MODELS = {role.value: model for role, model in DEFAULT_OLLAMA_MODELS.items()}
