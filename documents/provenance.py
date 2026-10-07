"""Evidence resolves against one immutable artifact, with explicit caller scope."""

from documents.errors import DocumentError
from documents.models import EvidenceRef, ExtractionArtifact, Scope


def resolve(artifact: ExtractionArtifact, scope: Scope, ref: EvidenceRef) -> str:
    if scope != artifact.document.scope or scope != ref.scope:
        raise DocumentError("scope_mismatch")
    if (ref.document_version_id != artifact.document.document_version_id
            or ref.extraction_id != artifact.extraction_id):
        raise DocumentError("invalid_reference")
    for unit in artifact.units:
        if unit.source_id != ref.source_id:
            continue
        for block in unit.blocks:
            if block.block_id == ref.block_id:
                if not (block.span.start <= ref.span.start <= ref.span.end <= block.span.end):
                    break
                if unit.physical_page is None:
                    text = unit.text[ref.span.start:ref.span.end]
                    start = 1 + unit.text[:ref.span.start].count("\n")
                    end = start + text.rstrip("\n").count("\n")
                    if (ref.span.line_start, ref.span.line_end) != (start, end):
                        break
                elif ref.span.line_start is not None:
                    break
                return unit.text[ref.span.start:ref.span.end]
    raise DocumentError("invalid_reference")
