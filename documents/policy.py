"""Observations are facts; this conservative, uncalibrated policy is replaceable."""

from uuid import UUID
from documents.models import Decision, Observations


def decide(source_id: UUID, observations: Observations) -> Decision:
    o = observations
    if o.parser_failed:
        outcome, tier, reason = "failed", "none", "parser_failure"
    elif not o.has_native_text and o.has_images:
        outcome, tier, reason = "ocr_required", "ocr", "image_without_text"
    elif o.replacement_ratio > 0 or (o.has_native_text and o.printable_ratio < 1):
        outcome, tier, reason = "manual_review", "none", "unusable_text"
    elif o.has_native_text and o.structure_required:
        outcome, tier, reason = "layout_required", "layout", "structure_requested"
    elif o.has_native_text:
        outcome, tier, reason = "native_accepted", "native", "native_text"
    elif o.has_graphics is not False:
        outcome, tier, reason = "manual_review", "none", "unresolved_graphics"
    else:
        outcome, tier, reason = "native_accepted", "native", "blank"
    return Decision(source_id=source_id, observations=o, outcome=outcome,
                    next_tier=tier, reason=reason)
