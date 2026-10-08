"""Immutable publication contracts, independent of vector-provider metadata."""
from typing import Literal
from uuid import UUID

from pydantic import Field, model_validator

from config.model_artifacts import EMBEDDING_MODEL
from documents.jobs.models import Token, fingerprint
from documents.models import Digest, EvidenceRef, FrozenModel, ObjectRef, Scope, stable_id


class PublicationError(RuntimeError):
    def __init__(self, category='publication_validation_failed'):
        allowed = {'publication_invalid_input', 'publication_validation_failed',
                   'publication_write_failure', 'publication_stale_candidate',
                   'publication_generation_mismatch', 'publication_unavailable',
                   'publication_incompatible', 'provenance_invalid',
                   'citation_invalid', 'retrieval_scope_invalid', 'embedding_limit', 'analysis_limit'}
        self.category = category if category in allowed else 'publication_validation_failed'
        super().__init__(self.category)


class RetrievalProfile(FrozenModel):
    version: Token = 'source-retrieval/1'
    embedding_model: Token = EMBEDDING_MODEL.identifier
    embedding_revision: Token = EMBEDDING_MODEL.revision
    dimension: int = Field(default=384, gt=0)
    normalized: Literal[True] = True
    max_tokens: int = Field(default=240, ge=8, le=240)
    max_characters: int = Field(default=4096, ge=8, le=4096)
    provenance_schema: Literal['evidence/1'] = 'evidence/1'
    publication_schema: Literal['publication/1'] = 'publication/1'

    def digest(self):
        return fingerprint(self.model_dump(mode='json'))


class ActivePublication(FrozenModel):
    generation: UUID | None = None
    epoch: int = Field(default=0, ge=0)


class AcceptedDocument(FrozenModel):
    scope: Scope
    job_id: UUID
    document_id: UUID
    document_version_id: UUID
    extraction_id: UUID
    extraction: ObjectRef
    digest: ObjectRef
    status: Literal['COMPLETE'] = 'COMPLETE'


class RetrievalRecord(FrozenModel):
    record_id: UUID
    document_id: UUID
    document_version_id: UUID
    extraction_id: UUID
    material: Literal['SOURCE_TEXT'] = 'SOURCE_TEXT'
    classification: Literal['ORIGINAL'] = 'ORIGINAL'
    text: str = Field(min_length=1, max_length=4096)
    evidence: EvidenceRef
    structural_path: tuple[str, ...] = Field(max_length=32)
    source_kind: str = Field(max_length=32)
    limitation: Literal['none', 'uninterpreted_visual'] = 'none'
    profile: Digest

    def identity(self):
        return stable_id('retrieval-record/1', fingerprint(self.model_dump(
            mode='json', exclude={'record_id'})))

    @model_validator(mode='after')
    def valid(self):
        if (self.record_id != self.identity() or self.document_version_id != self.evidence.document_version_id
                or self.extraction_id != self.evidence.extraction_id):
            raise ValueError('invalid retrieval identity')
        return self


class PublicationManifest(FrozenModel):
    schema_version: Literal['publication/1'] = 'publication/1'
    generation: UUID
    scope: Scope
    base: ActivePublication
    profile: RetrievalProfile
    documents: tuple[AcceptedDocument, ...]
    records: tuple[RetrievalRecord, ...]
    removed_versions: tuple[UUID, ...] = ()
    policy: Literal['COMPLETE_ONLY'] = 'COMPLETE_ONLY'

    def identity(self):
        # Job execution identity is audit data, not retrieval compatibility.
        payload = self.model_dump(mode='json', exclude={'generation'})
        for doc in payload['documents']:
            doc.pop('job_id')
        return stable_id('publication/1', fingerprint(payload))

    @model_validator(mode='after')
    def valid(self):
        docs = {d.document_id: d for d in self.documents}
        if (len(docs) != len(self.documents) or self.generation != self.identity()
                or len({r.record_id for r in self.records}) != len(self.records)):
            raise ValueError('invalid publication inventory')
        for d in self.documents:
            if d.scope != self.scope or d.extraction.scope != self.scope or d.digest.scope != self.scope:
                raise ValueError('invalid publication scope')
        for r in self.records:
            d = docs.get(r.document_id)
            if (d is None or r.evidence.scope != self.scope or r.profile != self.profile.digest()
                    or r.document_version_id != d.document_version_id or r.extraction_id != d.extraction_id):
                raise ValueError('invalid publication provenance')
        if set(docs) != {r.document_id for r in self.records}:
            raise ValueError('empty published document')
        return self


def record_values(**values):
    identity = UUID(int=0)
    # Normalize UUIDs and defaults through the model before deriving identity.
    draft = RetrievalRecord.model_construct(record_id=identity, **values)
    return RetrievalRecord.model_validate({**draft.model_dump(mode='json'), 'record_id': draft.identity()})


def manifest_values(**values):
    draft = PublicationManifest.model_construct(generation=UUID(int=0), **values)
    return PublicationManifest.model_validate({**draft.model_dump(mode='json'), 'generation': draft.identity()})


def vector_metadata(manifest, record):
    return {'generation': str(manifest.generation), 'record_id': str(record.record_id),
            'document_id': str(record.document_id), 'version': str(record.document_version_id),
            'material': record.material, 'classification': record.classification,
            'profile': record.profile, 'source': str(record.document_id),
            'chunk_id': str(record.record_id)}


def physical_id(generation, record_id):
    return str(stable_id('publication-vector/1', str(generation), str(record_id)))
