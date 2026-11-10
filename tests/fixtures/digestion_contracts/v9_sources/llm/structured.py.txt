"""Additive bounded generation contracts; existing text/stream APIs stay unchanged."""
from dataclasses import dataclass
from typing import Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field, model_serializer, model_validator

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
    # Explicit endpoint capability; never inferred from the served model name.
    reasoning_effort: Literal['none', 'minimal', 'low', 'medium', 'high', 'xhigh'] | None = None

    schema_profile: Literal['azure-strict/1'] | None = None

    @model_validator(mode='after')
    def strict_mode(self):
        if self.schema_profile is not None and self.structured_output != 'json_schema':
            raise ValueError('Strict schema profile requires json_schema mode')
        return self

    @model_serializer(mode='wrap')
    def serialize(self, handler):
        value = handler(self)
        # Keep historical managed-profile fingerprints when this option is unset.
        if self.reasoning_effort is None:
            value.pop('reasoning_effort', None)
        if self.schema_profile is None:
            value.pop('schema_profile', None)
        return value


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
    max_response_envelope_bytes: int | None = None


@dataclass(frozen=True)
class ProviderResultMetadata:
    """Sanitized observations only; absent numeric fields remain unknown."""

    finish_reason: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    reasoning_tokens: int | None = None
    raw_response_byte_count: int | None = None
    completion_token_limit: int | None = None
    response_byte_limit: int | None = None

    def evidence(self):
        def numeric(value):
            return value if type(value) is int and 0 <= value <= 2**63 - 1 else None

        reason = self.finish_reason
        return dict(
            finish_reason=(
                reason
                if type(reason) is str and reason in ("stop", "length", "max_tokens")
                else None
                if reason is None
                else "other"
            ),
            **{
                name: numeric(getattr(self, name))
                for name in (
                    "prompt_tokens",
                    "completion_tokens",
                    "total_tokens",
                    "reasoning_tokens",
                    "raw_response_byte_count",
                    "completion_token_limit",
                    "response_byte_limit",
                )
            },
        )


@dataclass(frozen=True)
class GenerationResult:
    text: str
    usage: InferenceUsage | None = None
    served_model: str | None = None
    finish_reason: str | None = None
    metadata: ProviderResultMetadata | None = None


class StructuredInferenceProvider(InferenceProvider, Protocol):
    """Optional capability. Do not emulate with unbounded legacy generate()."""
    def execute(self, request: GenerationRequest) -> GenerationResult: ...


def generation_schema_for_capability(capability, schema):
    """Provider infrastructure owns subset selection; callers retain the full schema."""
    if capability.schema_profile is None:
        return schema
    from llm.azure_schema import PROFILE, provider_schema
    from llm.inference import InferenceConfigurationError
    if capability.schema_profile != PROFILE or capability.structured_output != 'json_schema':
        raise InferenceConfigurationError('Unsupported strict schema capability.')
    return provider_schema(schema)


def validate_schema_provider(capability, provider_name):
    if capability.schema_profile is not None and provider_name != 'openai_compatible':
        from llm.inference import InferenceConfigurationError
        raise InferenceConfigurationError('Unsupported strict schema provider.')
