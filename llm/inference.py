from dataclasses import dataclass
from enum import Enum
from typing import Iterator, Mapping, Protocol, runtime_checkable


class ModelRole(str, Enum):
    GENERAL = "general"
    CODING = "coding"
    SUMMARIZATION = "summarization"
    FAST = "fast"


class InferenceError(RuntimeError):
    """Safe, provider-neutral inference failure."""

    category = "upstream_failure"


class InferenceConnectionError(InferenceError):
    """The configured provider could not complete an HTTP request."""

    category = "provider_unreachable"


class InferenceTimeoutError(InferenceConnectionError):
    """The configured provider exceeded an HTTP timeout."""

    category = "timeout"


class InferenceAuthenticationError(InferenceError):
    """The provider rejected its configured credentials."""

    category = "authentication_failure"


class InferenceRateLimitError(InferenceConnectionError):
    """The provider is temporarily rate limited or overloaded."""

    category = "overloaded"


class InferenceModelUnavailableError(InferenceError):
    """The requested or configured model is not available."""

    category = "model_unavailable"


class InferenceResponseError(InferenceError):
    """The provider returned an invalid response."""

    category = "protocol_failure"


class ReadinessStatus(str, Enum):
    READY = "ready"
    UNREACHABLE = "provider_unreachable"
    TIMEOUT = "timeout"
    AUTHENTICATION_FAILURE = "authentication_failure"
    OVERLOADED = "overloaded"
    MODEL_UNAVAILABLE = "model_unavailable"
    PROTOCOL_FAILURE = "protocol_failure"
    UPSTREAM_FAILURE = "upstream_failure"


@dataclass(frozen=True)
class ReadinessResult:
    status: ReadinessStatus
    provider: str
    models: Mapping[str, str]

    @property
    def ready(self) -> bool:
        return self.status is ReadinessStatus.READY


@runtime_checkable
class InferenceProvider(Protocol):
    @property
    def name(self) -> str: ...

    def model_id(self, role: ModelRole) -> str: ...

    def check_readiness(self) -> ReadinessResult: ...

    def generate(self, prompt: str, role: ModelRole) -> str: ...

    def generate_stream(self, prompt: str, role: ModelRole) -> Iterator[str]: ...
