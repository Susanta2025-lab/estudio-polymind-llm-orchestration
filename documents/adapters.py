"""Future OCR/layout result contract. No engine or network implementation."""

from typing import Literal, Protocol
from uuid import UUID
from pydantic import Field, model_validator
from documents.models import FrozenModel, ObjectRef, Scope, TextUnit


class EnhancementRequest(FrozenModel):
    scope: Scope
    source: ObjectRef
    document_version_id: UUID
    parent_extraction_id: UUID
    physical_pages: tuple[int, ...]
    tier: Literal["layout", "ocr"]

    @model_validator(mode="after")
    def lineage(self):
        if (self.scope != self.source.scope or self.source.kind != "source"
                or self.source.object_id != self.document_version_id
                or not self.physical_pages or any(p < 1 for p in self.physical_pages)
                or len(set(self.physical_pages)) != len(self.physical_pages)):
            raise ValueError("invalid enhancement request")
        return self


class EnhancementResult(FrozenModel):
    request: EnhancementRequest
    engine: str = Field(min_length=1)
    engine_version: str = Field(min_length=1)
    model_version: str | None = None
    units: tuple[TextUnit, ...]

    @model_validator(mode="after")
    def mapping(self):
        if tuple(u.physical_page for u in self.units) != self.request.physical_pages:
            raise ValueError("invalid physical page mapping")
        if any(u.document_version_id != self.request.document_version_id
               or u.method != self.request.tier for u in self.units):
            raise ValueError("invalid enhancement lineage")
        return self


class EnhancementAdapter(Protocol):
    def enhance(self, request: EnhancementRequest) -> EnhancementResult: ...
