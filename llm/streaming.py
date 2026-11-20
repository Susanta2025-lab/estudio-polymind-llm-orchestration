"""Optional provider-neutral bounded token callback with final usage evidence."""
from typing import Callable, Protocol
from llm.structured import StructuredInferenceProvider, GenerationRequest, GenerationResult


class StreamingStructuredInferenceProvider(StructuredInferenceProvider, Protocol):
    """Optional bounded stream with final usage; chunks never replace settlement."""
    def execute(self, request: GenerationRequest, *, on_chunk: Callable[[str], None] | None = None) -> GenerationResult: ...
