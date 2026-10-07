"""Bounded local service: verified bytes -> immutable canonical artifact.

No jobs, publication, inference, OCR calls, or public upload endpoints.
"""

import hashlib
from datetime import datetime, timezone
from io import BytesIO
from pathlib import PurePosixPath
from typing import BinaryIO
from uuid import UUID

from pydantic import ValidationError

from documents.config import ExtractionSettings
from documents.errors import DocumentError
from documents.models import (
    Block, Document, ExtractionArtifact, ObjectRef, Observations, Scope, Span, TextUnit, stable_id, extraction_identity,
)
from documents.parser import NativePdfRunner, ParsedPage, ParserRunner
from documents.policy import decide
from documents.serialization import serialize
from documents.storage import ObjectStore


def _bounded_read(stream: BinaryIO, limit: int) -> bytes:
    data = bytearray()
    try:
        while chunk := stream.read(min(65536, limit - len(data) + 1)):
            if not isinstance(chunk, bytes):
                raise DocumentError("invalid_document")
            data.extend(chunk)
            if len(data) > limit:
                raise DocumentError("source_too_large")
    except DocumentError:
        raise
    except Exception:
        raise DocumentError("invalid_document") from None
    return bytes(data)


def _format(data: bytes, filename: str, declared_mime: str) -> str:
    if not data:
        raise DocumentError("invalid_document")
    detected = "application/pdf" if data.startswith(b"%PDF-") else "text/plain"
    # Extensions are a consistency signal only; never a filesystem path or authority.
    suffix = PurePosixPath(filename.replace("\\", "/")).suffix.lower()
    extension = {".pdf": "application/pdf", ".txt": "text/plain"}.get(suffix)
    if (declared_mime not in ("application/pdf", "text/plain") or declared_mime != detected
            or (suffix and extension != detected)):
        raise DocumentError("unsupported_format")
    return detected


def _unit(page: ParsedPage, version_id: UUID, extraction_id: UUID,
          parser_version: str, limits: ExtractionSettings, structure_required: bool,
          *, plain_text: bool = False) -> TextUnit:
    source_id = stable_id(str(version_id), "text" if plain_text else f"page:{page.ordinal}")
    blocks = []
    # One native PDF text block; plain text has one block per LF-delimited line.
    # No semantic paragraph/heading/table claims are inferred.
    if plain_text:
        if page.text.count("\n") + (not page.text.endswith("\n")) > limits.max_blocks:
            raise DocumentError("extraction_limit_exceeded")
        # LF is the sole line delimiter, including CRLF where CR remains source text.
        pieces = page.text.split("\n")
        pieces = [piece + ("\n" if i < len(pieces) - 1 else "") for i, piece in enumerate(pieces)]
    else:
        pieces = [page.text] if page.text else []
    offset = 0
    for piece in pieces:
        if not piece:
            continue
        if len(blocks) >= limits.max_blocks:
            raise DocumentError("extraction_limit_exceeded")
        index = len(blocks)
        span = Span(start=offset, end=offset + len(piece),
                    line_start=index + 1 if plain_text else None,
                    line_end=index + 1 if plain_text else None)
        blocks.append(Block(block_id=stable_id(str(extraction_id), str(source_id), str(index)),
                            source_id=source_id, kind="text", reading_order=index,
                            source_text=piece, span=span))
        offset += len(piece)
    text = page.text
    observations = Observations(
        character_count=len(text), has_native_text=bool(text.strip()),
        printable_ratio=sum(c.isprintable() or c in "\r\n\t" for c in text) / len(text) if text else 1,
        replacement_ratio=text.count("\ufffd") / len(text) if text else 0,
        has_images=page.has_images, has_graphics=page.has_graphics,
        parser_failed=page.failed, structure_required=structure_required, block_count=len(blocks),
    )
    status = ("failed" if page.failed else "native_text" if text.strip() else
              "image_only" if page.has_images else "unresolved" if page.has_graphics is not False else "blank")
    return TextUnit(source_id=source_id, document_version_id=version_id,
                    physical_page=None if plain_text else page.ordinal, printed_label=page.label,
                    width=page.width, height=page.height, rotation=page.rotation,
                    status=status, parser_version=parser_version, text=text, blocks=tuple(blocks),
                    decision=decide(source_id, observations))


def extract(stream: BinaryIO, *, scope: Scope, document_id: UUID, display_filename: str,
            declared_mime: str, store: ObjectStore, limits: ExtractionSettings | None = None,
            created_at: datetime | None = None, extracted_at: datetime | None = None,
            expected_sha256: str | None = None, structure_required: bool = False,
            runner: ParserRunner | None = None) -> tuple[ExtractionArtifact, ObjectRef]:
    """Caller must authorize scope. Supply timestamps for reproducible replay.

    Returns canonical artifact and its object reference. Failed admission does not
    publish a source; failures after source write can leave an orphan for 17C.
    """
    limits = limits or ExtractionSettings()
    if not isinstance(document_id, UUID) or not isinstance(scope, Scope) or len(display_filename) > 512:
        raise DocumentError("invalid_document")
    created_at = created_at or datetime.now(timezone.utc)
    extracted_at = extracted_at or datetime.now(timezone.utc)
    if any(value.tzinfo is None or value.utcoffset() is None for value in (created_at, extracted_at)):
        raise DocumentError("invalid_document")
    created_at, extracted_at = (value.astimezone(timezone.utc) for value in (created_at, extracted_at))
    data = _bounded_read(stream, limits.max_source_bytes)
    checksum = hashlib.sha256(data).hexdigest()
    if expected_sha256 is not None and expected_sha256 != checksum:
        raise DocumentError("integrity_error")
    detected = _format(data, display_filename, declared_mime)
    if detected == "text/plain":
        try:
            text = data.decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            raise DocumentError("invalid_document") from None
        if not text.strip() or any(ord(c) < 32 and c not in "\r\n\t" for c in text):
            raise DocumentError("invalid_document")
        if len(text) > limits.max_characters:
            raise DocumentError("extraction_limit_exceeded")
        pages = (ParsedPage(1, text, has_images=False, has_graphics=False),)
        parser_version = "utf8-strict/1"
    else:
        runner = runner or NativePdfRunner()
        try:
            pages = runner.parse(data, limits)
        except DocumentError:
            raise
        except Exception:
            raise DocumentError("extraction_failed") from None
        parser_version = runner.version
        if not pages:
            raise DocumentError("invalid_document")
        if len(pages) > limits.max_pages:
            raise DocumentError("page_limit_exceeded")
        if [page.ordinal for page in pages] != list(range(1, len(pages) + 1)):
            raise DocumentError("extraction_failed")
    if sum(len(page.text) for page in pages) > limits.max_characters:
        raise DocumentError("extraction_limit_exceeded")
    version_id = stable_id(scope.identity(), str(document_id), checksum)
    extraction_id = extraction_identity(
        scope, version_id, parser_version, extracted_at, limits.max_source_bytes,
        limits.max_pages, limits.max_characters, limits.max_blocks, structure_required,
    )
    try:
        units = tuple(_unit(page, version_id, extraction_id, parser_version, limits,
                            structure_required, plain_text=detected == "text/plain") for page in pages)
    except ValidationError:
        raise DocumentError("extraction_failed") from None
    if sum(len(unit.blocks) for unit in units) > limits.max_blocks:
        raise DocumentError("extraction_limit_exceeded")
    source = store.put(scope, "source", version_id, BytesIO(data),
                       max_bytes=limits.max_source_bytes, expected_sha256=checksum)
    try:
        document = Document(document_id=document_id, document_version_id=version_id,
                            scope=scope, source=source, display_filename=display_filename,
                            declared_mime=declared_mime, detected_mime=detected,
                            page_count=len(pages) if detected == "application/pdf" else None,
                            created_at=created_at)
        artifact = ExtractionArtifact(document=document, extraction_id=extraction_id,
                                      parser_version=parser_version, extracted_at=extracted_at,
                                      max_source_bytes=limits.max_source_bytes, max_pages=limits.max_pages,
                                      max_characters=limits.max_characters, max_blocks=limits.max_blocks,
                                      structure_required=structure_required, units=units)
    except ValidationError:
        raise DocumentError("extraction_failed") from None
    encoded = serialize(artifact)
    if len(encoded) > limits.max_artifact_bytes:
        raise DocumentError("extraction_limit_exceeded")
    ref = store.put(scope, "artifact", extraction_id, BytesIO(encoded),
                    max_bytes=limits.max_artifact_bytes, expected_sha256=hashlib.sha256(encoded).hexdigest())
    return artifact, ref
