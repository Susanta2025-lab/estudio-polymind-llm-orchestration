"""Immutable v1 contracts. Offsets are half-open Unicode code-point intervals."""

import json
from datetime import timezone
from typing import Annotated, Literal
from uuid import UUID, NAMESPACE_URL, uuid5

from pydantic import BaseModel, ConfigDict, Field, AwareDatetime, model_validator

DOCUMENT_SCHEMA = "document/1"
ARTIFACT_SCHEMA = "extraction/1"
NORMALIZATION_PROFILE = "identity/1"
NATIVE_PROFILE = "native/1"
POLICY_PROFILE = "native-policy/1"
Digest = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]


def stable_id(*parts: str) -> UUID:
    # Length/escaping unambiguous, unlike delimiter concatenation.
    return uuid5(NAMESPACE_URL, json.dumps(parts, ensure_ascii=True, separators=(",", ":")))


class FrozenModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", allow_inf_nan=False)


class Scope(FrozenModel):
    tenant: UUID
    owner: UUID

    def identity(self) -> str:
        return f"{self.tenant}:{self.owner}"


class ObjectRef(FrozenModel):
    scope: Scope
    kind: Literal["source", "artifact"]
    object_id: UUID
    key: UUID
    sha256: Digest
    byte_size: int = Field(ge=0)
    hash_algorithm: Literal["sha256"] = "sha256"

    @model_validator(mode="after")
    def valid_key(self):
        if self.key != stable_id(self.scope.identity(), self.kind, str(self.object_id)):
            raise ValueError("invalid object key")
        return self


class Document(FrozenModel):
    schema_version: Literal["document/1"] = DOCUMENT_SCHEMA
    document_id: UUID
    document_version_id: UUID
    scope: Scope
    source: ObjectRef
    display_filename: str = Field(max_length=512)
    declared_mime: str
    detected_mime: Literal["application/pdf", "text/plain"]
    page_count: int | None = Field(default=None, ge=1)
    language: str | None = None
    language_confidence: float | None = Field(default=None, ge=0, le=1)
    created_at: AwareDatetime

    @model_validator(mode="after")
    def lineage(self):
        expected = stable_id(self.scope.identity(), str(self.document_id), self.source.sha256)
        if (self.source.scope != self.scope or self.source.kind != "source"
                or self.document_version_id != expected or self.source.object_id != expected):
            raise ValueError("invalid source lineage")
        if (self.detected_mime == "application/pdf") != (self.page_count is not None):
            raise ValueError("invalid page count")
        return self


class Span(FrozenModel):
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    # For plain text, 1-based inclusive line numbers. PDF offsets address parser text.
    line_start: int | None = Field(default=None, ge=1)
    line_end: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def ordered(self):
        if self.end < self.start or ((self.line_start is None) != (self.line_end is None)):
            raise ValueError("invalid span")
        if self.line_start is not None and self.line_end < self.line_start:
            raise ValueError("invalid lines")
        return self


class Geometry(FrozenModel):
    # PDF user space: points, lower-left origin. Other adapters must declare their frame.
    coordinates: tuple[float, ...]
    units: Literal["points", "pixels", "relative"]
    origin: Literal["top_left", "bottom_left"]


class Visual(FrozenModel):
    state: Literal["unparsed", "unsupported", "parsed"] = "unparsed"
    caption: str | None = None
    cells: tuple[tuple[str, ...], ...] | None = None
    image: ObjectRef | None = None


class Block(FrozenModel):
    block_id: UUID
    source_id: UUID
    kind: Literal["text", "paragraph", "heading", "table", "figure", "caption", "unknown"]
    reading_order: int = Field(ge=0)
    source_text: str
    span: Span
    # Identity normalization in v1; alternate normalization needs a new mapping schema.
    normalized_text: str | None = None
    geometry: Geometry | None = None
    parent_id: UUID | None = None
    child_ids: tuple[UUID, ...] = ()
    visual: Visual | None = None


class Observations(FrozenModel):
    character_count: int = Field(ge=0)
    printable_ratio: float = Field(ge=0, le=1)
    replacement_ratio: float = Field(ge=0, le=1)
    has_native_text: bool
    has_images: bool | None = None
    has_graphics: bool | None = None
    parser_failed: bool = False
    structure_required: bool = False
    block_count: int = Field(ge=0)


class Decision(FrozenModel):
    source_id: UUID
    policy_version: Literal["native-policy/1"] = POLICY_PROFILE
    observations: Observations
    outcome: Literal["native_accepted", "layout_required", "ocr_required", "unsupported", "failed", "manual_review"]
    next_tier: Literal["native", "layout", "ocr", "none"]
    reason: Literal["native_text", "blank", "image_without_text", "structure_requested", "unusable_text", "parser_failure", "unresolved_graphics"]


class TextUnit(FrozenModel):
    source_id: UUID
    document_version_id: UUID
    # None for plain text; PDFs use 1-based physical ordinals.
    physical_page: int | None = Field(default=None, ge=1)
    printed_label: str | None = None
    width: float | None = Field(default=None, gt=0)
    height: float | None = Field(default=None, gt=0)
    rotation: int | None = None
    status: Literal["native_text", "blank", "image_only", "unresolved", "failed"]
    method: Literal["native", "ocr", "layout"] = "native"
    parser_version: str
    text: str
    blocks: tuple[Block, ...]
    decision: Decision
    ocr_engine: str | None = None
    ocr_model_version: str | None = None
    ocr_confidence: float | None = Field(default=None, ge=0, le=1)


class EvidenceRef(FrozenModel):
    scope: Scope
    document_version_id: UUID
    extraction_id: UUID
    source_id: UUID
    block_id: UUID
    span: Span


def extraction_identity(scope, version_id, parser_version, extracted_at,
                        max_source_bytes, max_pages, max_characters, max_blocks, structure_required):
    return stable_id(
        scope.identity(), str(version_id), ARTIFACT_SCHEMA, NATIVE_PROFILE,
        NORMALIZATION_PROFILE, POLICY_PROFILE, parser_version,
        extracted_at.astimezone(timezone.utc).isoformat(), str(max_source_bytes),
        str(max_pages), str(max_characters), str(max_blocks), str(structure_required),
    )


class ExtractionArtifact(FrozenModel):
    schema_version: Literal["extraction/1"] = ARTIFACT_SCHEMA
    document: Document
    extraction_id: UUID
    extraction_profile: Literal["native/1"] = NATIVE_PROFILE
    normalization_profile: Literal["identity/1"] = NORMALIZATION_PROFILE
    parser_version: str
    extracted_at: AwareDatetime
    # Effective configuration is part of replay metadata and extraction identity.
    max_source_bytes: int = Field(gt=0)
    max_pages: int = Field(gt=0)
    max_characters: int = Field(gt=0)
    max_blocks: int = Field(gt=0)
    structure_required: bool = False
    units: tuple[TextUnit, ...]

    @model_validator(mode="after")
    def validate_graph(self):
        doc = self.document
        if self.extraction_id != extraction_identity(
                doc.scope, doc.document_version_id, self.parser_version, self.extracted_at,
                self.max_source_bytes, self.max_pages, self.max_characters,
                self.max_blocks, self.structure_required):
            raise ValueError("invalid extraction identity")
        if doc.source.byte_size > self.max_source_bytes or (doc.page_count or 0) > self.max_pages:
            raise ValueError("invalid source budget")
        pages = [u.physical_page for u in self.units]
        expected = list(range(1, doc.page_count + 1)) if doc.page_count else [None]
        if pages != expected:
            raise ValueError("incomplete source inventory")
        ids = set()
        for unit in self.units:
            if (unit.document_version_id != doc.document_version_id
                    or unit.source_id in ids or unit.decision.source_id != unit.source_id
                    or unit.parser_version != self.parser_version):
                raise ValueError("invalid unit lineage")
            expected_source = stable_id(str(doc.document_version_id),
                                        "text" if unit.physical_page is None else f"page:{unit.physical_page}")
            if unit.source_id != expected_source:
                raise ValueError("invalid source identity")
            ids.add(unit.source_id)
            if unit.decision.observations.character_count != len(unit.text):
                raise ValueError("invalid observations")
            observations = unit.decision.observations
            if (observations.block_count != len(unit.blocks)
                    or observations.has_native_text != bool(unit.text.strip())
                    or observations.structure_required != self.structure_required
                    or observations.parser_failed != (unit.status == "failed")):
                raise ValueError("inconsistent observations")
            if unit.physical_page is None and any(value is not None for value in
                    (unit.printed_label, unit.width, unit.height, unit.rotation)):
                raise ValueError("fabricated page metadata")
            printable = sum(c.isprintable() or c in "\r\n\t" for c in unit.text)
            if (observations.printable_ratio != (printable / len(unit.text) if unit.text else 1)
                    or observations.replacement_ratio != (unit.text.count("\ufffd") / len(unit.text) if unit.text else 0)):
                raise ValueError("invalid text quality observations")
            block_ids = {b.block_id for b in unit.blocks}
            if len(block_ids) != len(unit.blocks):
                raise ValueError("duplicate blocks")
            covered = 0
            line = 1
            for index, block in enumerate(unit.blocks):
                if (block.block_id != stable_id(str(self.extraction_id), str(unit.source_id), str(index))
                        or block.source_id != unit.source_id or block.reading_order != index
                        or block.span.start != covered
                        or block.span.end > len(unit.text)
                        or unit.text[block.span.start:block.span.end] != block.source_text
                        or block.normalized_text not in (None, block.source_text)
                        or (block.parent_id is not None and block.parent_id not in block_ids)
                        or not set(block.child_ids).issubset(block_ids)):
                    raise ValueError("invalid block provenance")
                if doc.page_count is None:
                    start = line
                    end = start + block.source_text.rstrip("\n").count("\n")
                    if (block.span.line_start, block.span.line_end) != (start, end):
                        raise ValueError("invalid line provenance")
                elif block.span.line_start is not None:
                    raise ValueError("invalid PDF span")
                if block.visual is not None and block.visual.image is not None:
                    if block.visual.image.scope != doc.scope:
                        raise ValueError("invalid visual scope")
                covered = block.span.end
                line += block.source_text.count("\n")
            if covered != len(unit.text):
                raise ValueError("incomplete text coverage")
        if sum(len(u.text) for u in self.units) > self.max_characters:
            raise ValueError("invalid character budget")
        if sum(len(u.blocks) for u in self.units) > self.max_blocks:
            raise ValueError("invalid block budget")
        return self
