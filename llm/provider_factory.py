from config.settings import Settings, settings
from llm.inference import InferenceProvider
from llm.ollama_client import OllamaClient


def create_inference_provider(config: Settings = settings) -> InferenceProvider:
    if config.INFERENCE_PROVIDER == "ollama":
        return OllamaClient(
            url=config.OLLAMA_URL,
            model_map=config.OLLAMA_MODEL_MAP,
            connect_timeout=config.INFERENCE_CONNECT_TIMEOUT,
            read_timeout=config.INFERENCE_READ_TIMEOUT,
        )
    # Settings validation currently prevents this branch, but retaining the guard
    # keeps the factory safe if configuration sources change.
    raise ValueError(f"Unsupported inference provider: {config.INFERENCE_PROVIDER}")
