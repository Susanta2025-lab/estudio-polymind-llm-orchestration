"""Versioned digestion contracts. Source references remain Phase 17B EvidenceRefs."""

from typing import Annotated, Literal
from uuid import UUID

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from documents.jobs.models import Token, fingerprint
from documents.models import Digest, EvidenceRef, FrozenModel, ObjectRef, stable_id

Text = Annotated[str, Field(min_length=1, max_length=4096)]


class DigestionError(RuntimeError):
    """Content-free domain failures; workflow classification is an adapter concern."""
    def __init__(self, category):
        allowed = {'structural_planning_failed', 'analysis_failed', 'reducer_failed',
                   'evidence_validation_failed', 'coverage_failed', 'inference_contract_error',
                   'synthesis_limit_exceeded', 'incompatible_checkpoint'}
        self.category = category if category in allowed else 'inference_contract_error'
        super().__init__(self.category)


class DigestionProfile(FrozenModel):
    version: Token = 'digestion/1'
    structure_profile: Token = 'source-structure/1'
    chunking_profile: Token = 'analysis-chunks/1'
    inference_profile: Token = 'deterministic/1'
    inference_config: Digest = fingerprint([])
    reducer_profile: Token = 'lineage-reduction/1'
    prompt_profile: Token = 'structured-data/1'
    output_schema: Literal['stage-result/1'] = 'stage-result/1'
    role: Literal['summarization'] = 'summarization'
    capability: Literal['structured-output'] = 'structured-output'
    # Required planning choices, not purported production model sizes.
    context_tokens: int = Field(gt=0)
    reserved_output_tokens: int = Field(gt=0)
    template_tokens: int = Field(ge=0)
    chunk_characters: int = Field(gt=0)
    max_fan_in: int = Field(ge=2, le=64)
    max_result_characters: int = Field(gt=0)
    max_claims: int = Field(ge=1, le=64)
    max_claim_characters: int = Field(ge=64, le=4096)
    max_annotations: int = Field(ge=0, le=64)
    max_source_units: int = Field(gt=0, le=100000)
    max_chunks: int = Field(gt=0, le=900)
    max_steps: int = Field(ge=3, le=1000)
    max_artifact_bytes: int = Field(gt=0)
    max_depth: int = Field(ge=1, le=64)
    overlap_characters: Literal[0] = 0  # No duplicated source in v1.
    estimator: Literal['json-characters/1'] = 'json-characters/1'
    allow_partial: bool = False
    minimum_coverage: float = Field(ge=0, le=1)
    max_failed_units: int = Field(ge=0)

    @model_validator(mode='after')
    def budget(self):
        if (self.reserved_output_tokens < self.max_result_characters or
                self.context_tokens <= self.reserved_output_tokens + self.template_tokens):
            raise ValueError('invalid synthesis budget')
        return self

    def digest(self):
        return fingerprint(self.model_dump(mode='json'))


class DigestionSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='DOCUMENT_DIGESTION_',
                                     env_nested_delimiter='__', frozen=True, extra='forbid')
    profile: DigestionProfile  # No implicit production sizing.


class StructuralUnit(FrozenModel):
    structural_unit_id: UUID
    parent_id: UUID | None
    child_ids: tuple[UUID, ...]
    order: int = Field(ge=0)
    kind: Literal['document', 'section', 'subsection', 'fallback']
    heading: str | None = None
    path: tuple[str, ...] = ()
    source: Literal['canonical-heading', 'canonical-page', 'canonical-text', 'root']
    confidence: Literal['source-declared', 'fallback']
    block_ids: tuple[UUID, ...] = ()
    source_ids: tuple[UUID, ...] = ()
    physical_pages: tuple[int, ...] = ()


class StructuralMap(FrozenModel):
    schema_version: Literal['structure/1'] = 'structure/1'
    extraction: ObjectRef
    document_version_id: UUID
    profile: Digest
    units: tuple[StructuralUnit, ...]

    @model_validator(mode='after')
    def tree(self):
        by_id = {u.structural_unit_id: u for u in self.units}
        if not self.units or len(by_id) != len(self.units):
            raise ValueError('invalid structural tree')
        root = self.units[0]
        if root.parent_id is not None or root.kind != 'document':
            raise ValueError('invalid structural root')
        visited = set()
        stack = [root.structural_unit_id]
        while stack:
            key = stack.pop()
            if key in visited or key not in by_id:
                raise ValueError('invalid structural relationship')
            visited.add(key)
            unit = by_id[key]
            for index, child in enumerate(unit.child_ids):
                if child not in by_id or by_id[child].parent_id != key or by_id[child].order != index:
                    raise ValueError('invalid structural relationship')
            stack.extend(unit.child_ids)
        if len(visited) != len(by_id):
            raise ValueError('unreachable structural unit')
        return self


class SourcePiece(FrozenModel):
    evidence: EvidenceRef
    text: str
    kind: str
    cells: tuple[tuple[str, ...], ...] | None = None
    limitation: Literal['visual_uninterpreted', 'hard_split', 'none'] = 'none'

    def evidence_id(self):
        return stable_id('source-evidence/1', fingerprint(self.evidence.model_dump(mode='json')))


class AnalysisChunk(FrozenModel):
    schema_version: Literal['analysis-chunk/1'] = 'analysis-chunk/1'
    chunk_id: UUID
    document_version_id: UUID
    structural_parent: UUID
    path: tuple[str, ...]
    sequence: int = Field(ge=0)
    profile: Digest
    pieces: tuple[SourcePiece, ...]
    estimated_tokens: int = Field(ge=0)
    overlap_with: tuple[UUID, ...] = ()


class ReductionNode(FrozenModel):
    stage_id: UUID
    structural_parent: UUID
    children: tuple[UUID, ...]
    level: int = Field(ge=1)
    path: tuple[str, ...]
    estimated_tokens: int = Field(ge=0)


class Plan(FrozenModel):
    schema_version: Literal['digestion-plan/1'] = 'digestion-plan/1'
    profile: DigestionProfile
    structure: StructuralMap
    chunks: tuple[AnalysisChunk, ...]
    reducers: tuple[ReductionNode, ...]
    root_id: UUID
    eligible: tuple[UUID, ...]
    skipped: tuple[UUID, ...]
    unsupported: tuple[UUID, ...]


class ClaimLink(FrozenModel):
    stage_id: UUID
    claim_id: UUID


class Qualification(FrozenModel):
    text: Text
    evidence_ids: tuple[UUID, ...]


class Claim(FrozenModel):
    claim_id: UUID
    originating_stage: UUID
    text: Text
    kind: Literal['fact', 'unknown', 'unsupported', 'commentary', 'structural']
    evidence_ids: tuple[UUID, ...] = ()
    contradicting_evidence_ids: tuple[UUID, ...] = ()
    qualifications: tuple[Qualification, ...] = ()
    lineage: tuple[ClaimLink, ...] = ()
    # Optional synthetic/structured propositions; no language inference here.
    subject: Token | None = None
    stance: Literal['affirmed', 'denied', 'unknown'] = 'unknown'
    status: Literal['supported', 'unknown', 'unsupported'] = 'supported'


class StageResult(FrozenModel):
    schema_version: Literal['stage-result/1'] = 'stage-result/1'
    stage_id: UUID
    kind: Literal['analysis', 'reduction']
    outcome: Literal['analyzed', 'unavailable'] = 'analyzed'
    claims: tuple[Claim, ...]
    open_questions: tuple[Text, ...] = ()
    limitations: tuple[Text, ...] = ()


class Proposition(FrozenModel):
    subject: Token
    affirmed: bool
    denied: bool


class InheritedSummary(FrozenModel):
    analyzed_pieces: int = Field(default=0, ge=0)
    failed_pieces: int = Field(default=0, ge=0)
    qualifications: int = Field(default=0, ge=0)
    contradictions: int = Field(default=0, ge=0)
    open_questions: int = Field(default=0, ge=0)
    source_set: Literal['application-owned-source-lineage'] = 'application-owned-source-lineage'


class ChildInput(FrozenModel):
    """Generated material; its lineage is an application-owned source-set handle.

    The child artifact hash binds the exact inherited evidence/annotation graph.
    It is NEVER classified as source evidence or executable instructions.
    """
    artifact: ObjectRef
    result: StageResult
    inherited: InheritedSummary
    material_kind: Literal['generated-intermediate'] = 'generated-intermediate'


class StageRequest(FrozenModel):
    schema_version: Literal['stage-request/1'] = 'stage-request/1'
    stage_id: UUID
    stage: Literal['analysis', 'reduction']
    profile: DigestionProfile
    structural_path: tuple[str, ...]
    source_data: tuple[SourcePiece, ...] = ()
    children: tuple[ChildInput, ...] = ()
    instructions: Literal['Analyze data; inherit all child claims and their qualifications/conflicts.'] = (
        'Analyze data; inherit all child claims and their qualifications/conflicts.')
    tools: tuple[()] = ()

    @model_validator(mode='after')
    def material_boundary(self):
        if self.stage == 'analysis':
            if not self.source_data or self.children:
                raise ValueError('invalid analysis input')
            ids = [p.evidence_id() for p in self.source_data]
        else:
            if self.source_data or len(self.children) > self.profile.max_fan_in:
                raise ValueError('invalid reduction input')
            ids = [c.result.stage_id for c in self.children]
        if len(ids) != len(set(ids)):
            raise ValueError('duplicate input identity')
        return self


class Checkpoint(FrozenModel):
    schema_version: Literal['synthesis-checkpoint/1'] = 'synthesis-checkpoint/1'
    plan_hash: Digest
    parents: tuple[ObjectRef, ...]
    result: StageResult
    inherited: InheritedSummary
    propositions: tuple[Proposition, ...]


class Coverage(FrozenModel):
    schema_version: Literal['coverage/1'] = 'coverage/1'
    eligible: tuple[UUID, ...]
    analyzed: tuple[UUID, ...]
    failed: tuple[UUID, ...]
    skipped: tuple[UUID, ...]
    unsupported: tuple[UUID, ...]
    included: tuple[UUID, ...]
    fraction: float = Field(ge=0, le=1)


class Contradiction(FrozenModel):
    subject: Token
    affirmed: tuple[UUID, ...]
    denied: tuple[UUID, ...]
    resolution: Literal['unresolved'] = 'unresolved'


class SectionSummary(FrozenModel):
    structural_unit_id: UUID
    stage_id: UUID
    synthesis: Text


class DigestArtifact(FrozenModel):
    schema_version: Literal['document-digest/1'] = 'document-digest/1'
    document_version_id: UUID
    extraction: ObjectRef
    plan: ObjectRef
    profile: Digest
    status: Literal['COMPLETE', 'PARTIAL', 'FAILED']
    executive_summary: Text
    root: UUID
    sections: tuple[SectionSummary, ...]
    # Exact leaf findings, including qualifications, preserved alongside bounded synthesis.
    findings: tuple[Claim, ...]
    synthesis_claims: tuple[Claim, ...]
    qualifications: tuple[Qualification, ...]
    contradictions: tuple[Contradiction, ...]
    open_questions: tuple[Text, ...]
    coverage: Coverage
    limitations: tuple[Text, ...]
    evidence: tuple[EvidenceRef, ...]
    checkpoints: tuple[ObjectRef, ...]
