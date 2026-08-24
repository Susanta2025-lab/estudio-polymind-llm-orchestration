from config.settings import Settings, settings
from llm.inference import InferenceProvider
from llm.ollama_client import OllamaClient
from llm.openai_compatible import OpenAICompatibleProvider


def create_inference_provider(config: Settings = settings) -> InferenceProvider:
    if config.INFERENCE_PROVIDER == "ollama":
        return OllamaClient(
            url=config.OLLAMA_URL,
            model_map=config.OLLAMA_MODEL_MAP,
            connect_timeout=config.INFERENCE_CONNECT_TIMEOUT,
            read_timeout=config.INFERENCE_READ_TIMEOUT,
            readiness_timeout=config.PROVIDER_READINESS_TIMEOUT,
            readiness_retries=config.PROVIDER_READINESS_RETRIES,
            readiness_backoff=config.PROVIDER_READINESS_BACKOFF,
        )
    if config.INFERENCE_PROVIDER == "openai_compatible":
        return OpenAICompatibleProvider(
            base_url=config.OPENAI_COMPATIBLE_BASE_URL,
            api_key=config.OPENAI_COMPATIBLE_API_KEY,
            model_map=config.OPENAI_COMPATIBLE_MODEL_MAP,
            connect_timeout=config.OPENAI_COMPATIBLE_CONNECT_TIMEOUT,
            read_timeout=config.OPENAI_COMPATIBLE_READ_TIMEOUT,
            generation_parameters=config.OPENAI_COMPATIBLE_GENERATION_PARAMETERS,
            readiness_timeout=config.PROVIDER_READINESS_TIMEOUT,
            readiness_retries=config.PROVIDER_READINESS_RETRIES,
            readiness_backoff=config.PROVIDER_READINESS_BACKOFF,
        )
    # Settings validation currently prevents this branch, but retaining the guard
    # keeps the factory safe if configuration sources change.
    raise ValueError(f"Unsupported inference provider: {config.INFERENCE_PROVIDER}")
