from config.settings import Settings, settings
from llm.inference import InferenceProvider
from llm.ollama_client import OllamaClient
from llm.openai_streaming import StreamingOpenAICompatibleProvider as OpenAICompatibleProvider


def create_inference_provider(config: Settings = settings) -> InferenceProvider:
    provider = _create_inference_provider(config)
    if config.GOVERNANCE_ENABLED:
        from governance.execution import RestrictedProvider
        return RestrictedProvider(provider)
    return provider


def _create_inference_provider(config):
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
            api_key=provider_credential(config),
            authentication_header=config.OPENAI_COMPATIBLE_AUTHENTICATION_HEADER,
            model_map=config.OPENAI_COMPATIBLE_MODEL_MAP,
            connect_timeout=config.OPENAI_COMPATIBLE_CONNECT_TIMEOUT,
            read_timeout=config.OPENAI_COMPATIBLE_READ_TIMEOUT,
            generation_parameters=config.OPENAI_COMPATIBLE_GENERATION_PARAMETERS,
            readiness_model_check=config.OPENAI_COMPATIBLE_READINESS_MODEL_CHECK,
            readiness_timeout=config.PROVIDER_READINESS_TIMEOUT,
            readiness_retries=config.PROVIDER_READINESS_RETRIES,
            readiness_backoff=config.PROVIDER_READINESS_BACKOFF,
        )
    # Settings validation currently prevents this branch, but retaining the guard
    # keeps the factory safe if configuration sources change.
    raise ValueError(f"Unsupported inference provider: {config.INFERENCE_PROVIDER}")


def provider_credential(config):
    """Explicit mounted secret; no discovery, renewal or credential logging."""
    if not config.OPENAI_COMPATIBLE_API_KEY_FILE:
        return config.OPENAI_COMPATIBLE_API_KEY
    from config.runtime_secrets import private_file
    path = private_file(config.OPENAI_COMPATIBLE_API_KEY_FILE)
    if path.stat().st_size > 16384:
        raise ValueError("Provider credential unavailable")
    value = path.read_text().strip()
    if not value or any(c.isspace() for c in value):
        raise ValueError("Provider credential unavailable")
    return value
