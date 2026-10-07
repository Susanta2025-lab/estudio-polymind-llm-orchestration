"""Additive bounded generation contracts; existing text/stream APIs stay unchanged."""
from dataclasses import dataclass
from typing import Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field

from llm.inference import InferenceProvider, InferenceUsage, ModelRole


class CapabilityProfile(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid', allow_inf_nan=False)
    version: str = Field(pattern=r'^[A-Za-z0-9_./:-]{1,128}$')
    # Operator verified or deliberately conservative deployment bounds, never name inference.
    context_tokens: int = Field(gt=0)
    max_output_tokens: int = Field(gt=0)
    overhead_tokens: int = Field(ge=0)
    safety_tokens: int = Field(ge=0)
    structured_output: Literal['prompt', 'json_object', 'json_schema'] = 'prompt'
    output_parameter: Literal['max_tokens', 'max_completion_tokens'] = 'max_tokens'
    streaming: bool = True
    usage_reporting: bool = False
    temperature: float | None = Field(default=None, ge=0, le=2)
    # Some managed endpoints return a versioned model ID rather than the alias.
    response_models: tuple[str, ...] = ()


@dataclass(frozen=True)
class GenerationRequest:
    system: str
    data: str
    role: ModelRole
    capability: CapabilityProfile
    output_tokens: int
    response_bytes: int
    schema: dict
    total_seconds: float = 120


@dataclass(frozen=True)
class GenerationResult:
    text: str
    usage: InferenceUsage | None = None
    served_model: str | None = None
    finish_reason: str | None = None


class StructuredInferenceProvider(InferenceProvider, Protocol):
    """Optional capability. Do not emulate with unbounded legacy generate()."""
    def execute(self, request: GenerationRequest) -> GenerationResult: ...
