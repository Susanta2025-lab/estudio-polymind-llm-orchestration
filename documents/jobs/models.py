"""Immutable orchestration contracts; clocks and IDs are not execution authority."""

from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
from pathlib import Path
from typing import Annotated, Literal, Protocol
from uuid import UUID

from pydantic import AwareDatetime, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from documents.config import ExtractionSettings
from documents.models import Digest, FrozenModel, ObjectRef, Scope, stable_id

Token = Annotated[str, Field(min_length=1, max_length=128, pattern=r'^[a-zA-Z0-9_./:-]+$')]


def canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)


def fingerprint(value) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


class Clock(Protocol):
    def now(self) -> datetime: ...


class SystemClock:
    def now(self):
        return datetime.now(timezone.utc)


class JobState(str, Enum):
    QUEUED = 'QUEUED'
    EXTRACTING = 'EXTRACTING'
    NORMALIZING = 'NORMALIZING'
    VALIDATING = 'VALIDATING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    CANCEL_REQUESTED = 'CANCEL_REQUESTED'
    CANCELLED = 'CANCELLED'
    PARTIAL = 'PARTIAL'


class StepState(str, Enum):
    PENDING = 'PENDING'
    READY = 'READY'
    RUNNING = 'RUNNING'
    RETRY_WAIT = 'RETRY_WAIT'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'
    CANCELLED = 'CANCELLED'


class RetryPolicy(FrozenModel):
    max_attempts: int = Field(default=3, ge=1, le=100)
    base_seconds: float = Field(default=1, gt=0, le=86400)
    max_seconds: float = Field(default=60, gt=0, le=86400)
    budget_seconds: float = Field(default=3600, gt=0, le=604800)
    # Deterministic per-key jitter, [1-fraction, 1]; no mutable RNG to persist.
    jitter_fraction: float = Field(default=0, ge=0, le=1)

    def delay(self, key: str, attempt: int) -> float:
        fraction = int(fingerprint([key, attempt])[:8], 16) / 0xffffffff
        return min(self.max_seconds, self.base_seconds * 2 ** (attempt - 1)) * (
            1 - self.jitter_fraction * fraction)


class ProcessingProfile(FrozenModel):
    version: Token = 'local-extraction/1'
    artifact_schema: Literal['extraction/1'] = 'extraction/1'
    extraction_profile: Literal['native/1'] = 'native/1'
    normalization_profile: Literal['identity/1'] = 'identity/1'
    policy_profile: Literal['native-policy/1'] = 'native-policy/1'
    parser_version: Token = 'utf8-strict/1'
    max_source_bytes: int = Field(default=16_000_000, gt=0)
    max_pages: int = Field(default=1000, gt=0)
    max_characters: int = Field(default=4_000_000, gt=0)
    max_blocks: int = Field(default=100_000, gt=0)
    max_artifact_bytes: int = Field(default=32_000_000, gt=0)
    structure_required: bool = False
    retry: RetryPolicy = RetryPolicy()

    def digest(self):
        return fingerprint(self.model_dump(mode='json'))

    def limits(self):
        return ExtractionSettings(**{name: getattr(self, name) for name in (
            'max_source_bytes', 'max_pages', 'max_characters', 'max_blocks', 'max_artifact_bytes')})


class StepSpec(FrozenModel):
    unit_id: Token = 'document'
    stage: Literal['EXTRACTING', 'NORMALIZING', 'VALIDATING'] = 'EXTRACTING'
    schema_version: Token = 'extraction/1'
    config_fingerprint: Digest = fingerprint({})
    depends_on: tuple[Token, ...] = ()


class Admission(FrozenModel):
    scope: Scope
    document_id: UUID
    document_version_id: UUID
    source: ObjectRef
    request_idempotency_key: Token
    display_filename: str = Field(default='source.txt', max_length=512)
    mime: Literal['text/plain', 'application/pdf'] = 'text/plain'
    profile: ProcessingProfile = ProcessingProfile()
    steps: tuple[StepSpec, ...] = (StepSpec(),)
    resume_from: UUID | None = None

    @model_validator(mode='after')
    def valid(self):
        expected = stable_id(self.scope.identity(), str(self.document_id), self.source.sha256)
        if (self.source.scope != self.scope or self.source.kind != 'source'
                or self.document_version_id != expected or self.source.object_id != expected
                or self.source.byte_size > self.profile.max_source_bytes):
            raise ValueError('invalid source lineage')
        seen = set()
        if not 1 <= len(self.steps) <= 1000:
            raise ValueError('invalid plan')
        for step in self.steps:
            if (step.unit_id in seen or not set(step.depends_on).issubset(seen)
                    or len(step.depends_on) != len(set(step.depends_on))):
                raise ValueError('invalid plan')
            seen.add(step.unit_id)
        return self

    def digest(self):
        return fingerprint(self.model_dump(mode='json', exclude={'request_idempotency_key'}))

    def compatibility(self):
        value = self.model_dump(mode='json', exclude={
            'request_idempotency_key', 'resume_from', 'steps'})
        value['profile'] = self.profile.digest()
        return fingerprint(value)


class Progress(FrozenModel):
    total: int = Field(default=0, ge=0)
    completed: int = Field(default=0, ge=0)
    running: int = Field(default=0, ge=0)
    retrying: int = Field(default=0, ge=0)
    failed: int = Field(default=0, ge=0)
    cancelled: int = Field(default=0, ge=0)
    pending: int = Field(default=0, ge=0)
    current_stage: str | None = None


class Job(FrozenModel):
    job_id: UUID
    run_id: UUID
    generation: int = Field(gt=0)
    admission: Admission
    request_fingerprint: Digest
    created_at: AwareDatetime
    updated_at: AwareDatetime
    document_created_at: AwareDatetime
    state: JobState
    cancel_requested: bool
    progress: Progress
    terminal_category: str | None = None


class Step(FrozenModel):
    step_id: UUID
    job_id: UUID
    spec: StepSpec
    step_key: Digest
    input_fingerprint: Digest
    execution_at: AwareDatetime
    state: StepState
    attempt_count: int = Field(ge=0)
    fence: int = Field(ge=0)
    lease_owner: str | None
    lease_expires_at: AwareDatetime | None
    not_before: AwareDatetime
    started_at: AwareDatetime | None
    finished_at: AwareDatetime | None
    failure_category: str | None
    manifest: tuple[ObjectRef, ...] = ()
    reused_from: UUID | None = None


class Lease(FrozenModel):
    scope: Scope
    job_id: UUID
    step_id: UUID
    owner: Token
    fence: int = Field(gt=0)


class Attempt(FrozenModel):
    number: int
    worker: str
    fence: int = Field(ge=0)
    started_at: AwareDatetime
    finished_at: AwareDatetime | None
    outcome: str
    category: str | None
    classification: str | None
    not_before: AwareDatetime | None


class Dispatch(FrozenModel):
    dispatch_id: int
    scope: Scope
    job_id: UUID
    step_id: UUID


class Reconciliation(FrozenModel):
    expired: int = 0
    dispatch_repairs: int = 0
    terminal_repairs: int = 0
    pending_outbox: int = 0
    orphan_candidates: int = 0


class JobSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='DOCUMENT_JOBS_', frozen=True, extra='forbid')
    database_path: Path  # Deliberately no implicit location.
    busy_timeout_seconds: float = Field(default=5, gt=0, le=60)
    lease_seconds: float = Field(default=30, gt=0, le=3600)
    redelivery_seconds: float = Field(default=30, gt=0, le=3600)
    orphan_grace_seconds: float = Field(default=86400, ge=0, le=31536000)
