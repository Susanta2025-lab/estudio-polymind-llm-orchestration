from enum import Enum
from typing import Iterator, Protocol, runtime_checkable


class ModelRole(str, Enum):
    GENERAL = "general"
    CODING = "coding"
    SUMMARIZATION = "summarization"
    FAST = "fast"


class InferenceError(RuntimeError):
    """Safe, provider-neutral inference failure."""


class InferenceConnectionError(InferenceError):
    """The configured provider could not complete an HTTP request."""


class InferenceResponseError(InferenceError):
    """The provider returned an invalid response."""


@runtime_checkable
class InferenceProvider(Protocol):
    @property
    def name(self) -> str: ...

    def model_id(self, role: ModelRole) -> str: ...

    def generate(self, prompt: str, role: ModelRole) -> str: ...

    def generate_stream(self, prompt: str, role: ModelRole) -> Iterator[str]: ...
