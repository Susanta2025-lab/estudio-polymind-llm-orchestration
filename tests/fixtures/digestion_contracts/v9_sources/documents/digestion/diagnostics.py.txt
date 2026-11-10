"""Closed, content-free supplemental validation diagnostics.

Pydantic selection uses reason declaration order, then static path order. Counts
saturate at 64 (64 means at least 64); no rejected values or messages survive.
"""

from dataclasses import dataclass
from enum import Enum


class ValidationReason(Enum):
    MALFORMED_JSON = "malformed_json"
    DUPLICATE_JSON_KEY = "duplicate_json_key"
    INVALID_UUID = "invalid_uuid"
    INVALID_SUBJECT_TOKEN = "invalid_subject_token"
    INVALID_TEXT_BOUND = "invalid_text_bound"
    MISSING_REQUIRED_FIELD = "missing_required_field"
    INVALID_FIELD_TYPE = "invalid_field_type"
    FORBIDDEN_EXTRA_FIELD = "forbidden_extra_field"
    INVALID_ENUM = "invalid_enum"
    OTHER_PYDANTIC_VALIDATION = "other_pydantic_validation"
    CANONICAL_ENCODING_FAILED = "canonical_encoding_failed"
    CANONICAL_REVALIDATION_FAILED = "canonical_revalidation_failed"
    OTHER_CANONICAL_FAILURE = "other_canonical_failure"
    STAGE_ID_MISMATCH = "stage_id_mismatch"
    STAGE_KIND_MISMATCH = "stage_kind_mismatch"
    UNAVAILABLE_WITH_CLAIMS = "unavailable_with_claims"
    UNAVAILABLE_MISSING_LIMITATION = "unavailable_missing_limitation"
    ANALYZED_WITHOUT_CLAIMS = "analyzed_without_claims"
    UNAVAILABLE_REDUCTION = "unavailable_reduction"
    CLAIM_ID_MISMATCH = "claim_id_mismatch"
    DUPLICATE_CLAIM_ID = "duplicate_claim_id"
    ORIGINATING_STAGE_MISMATCH = "originating_stage_mismatch"
    SUBJECT_ON_NONFACT = "subject_on_nonfact"
    FOREIGN_EVIDENCE = "foreign_evidence"
    DUPLICATE_EVIDENCE = "duplicate_evidence"
    INVALID_QUALIFICATION_SOURCE = "invalid_qualification_source"
    INVALID_CHILD_LINK = "invalid_child_link"
    DUPLICATE_CHILD_LINK = "duplicate_child_link"
    UNSUPPORTED_FACT = "unsupported_fact"
    OTHER_EVIDENCE_VALIDATION = "other_evidence_validation"
    MISSING_SOURCE_COVERAGE = "missing_source_coverage"
    MISSING_CHILD_COVERAGE = "missing_child_coverage"
    OTHER_COVERAGE_FAILURE = "other_coverage_failure"
    RAW_RESPONSE_LIMIT = "raw_response_limit"
    CANONICAL_RESPONSE_LIMIT = "canonical_response_limit"
    CHILD_MATERIAL_LIMIT = "child_material_limit"
    CLAIM_LIMIT = "claim_limit"
    ANNOTATION_LIMIT = "annotation_limit"
    TEXT_LIMIT = "text_limit"


# Known StageResult structure only. No arbitrary keys or union labels survive.
_SCALARS = ("schema_version", "stage_id", "kind", "outcome")
_CLAIM = (
    "claim_id",
    "originating_stage",
    "text",
    "kind",
    "subject",
    "stance",
    "status",
)


def safe_path(path):
    if type(path) is not tuple:
        return ()

    def index(value, limit):
        return type(value) is int and 0 <= value < limit

    if len(path) == 1 and path[0] in (
        *_SCALARS,
        "claims",
        "open_questions",
        "limitations",
    ):
        return path
    if (
        len(path) == 2
        and path[0] in ("open_questions", "limitations")
        and index(path[1], 64)
    ):
        return path
    if len(path) < 2 or path[0] != "claims" or not index(path[1], 64):
        return ()
    tail = path[2:]
    if (
        not tail
        or len(tail) == 1
        and tail[0]
        in (
            *_CLAIM,
            "evidence_ids",
            "contradicting_evidence_ids",
            "qualifications",
            "lineage",
        )
    ):
        return path
    if (
        len(tail) == 2
        and tail[0] in ("evidence_ids", "contradicting_evidence_ids")
        and index(tail[1], 4096)
    ):
        return path
    if (
        len(tail) >= 2
        and tail[0] in ("qualifications", "lineage")
        and index(tail[1], 64)
    ):
        if len(tail) == 2:
            return path
        fields = (
            ("text", "evidence_ids")
            if tail[0] == "qualifications"
            else ("stage_id", "claim_id")
        )
        if len(tail) == 3 and tail[2] in fields:
            return path
        if (
            len(tail) == 4
            and tail[0] == "qualifications"
            and tail[2] == "evidence_ids"
            and index(tail[3], 4096)
        ):
            return path
    return ()


@dataclass(frozen=True)
class PydanticDiagnostic:
    reason: ValidationReason
    path: tuple = ()
    error_count: int = 1

    def evidence(self):
        # Recheck at serialization, including unchecked/forged records.
        if type(self.reason) is not ValidationReason:
            return {}
        count = self.error_count
        return {
            "reason": self.reason.value,
            "path": list(safe_path(self.path)),
            "error_count": min(count, 64) if type(count) is int and count > 0 else 1,
        }


def classify_pydantic(exc):
    from pydantic import ValidationError

    if not isinstance(exc, ValidationError):
        return PydanticDiagnostic(ValidationReason.OTHER_PYDANTIC_VALIDATION)
    errors = exc.errors(include_input=False, include_context=False, include_url=False)
    candidates = []
    for error in errors:
        path = safe_path(error.get("loc"))
        kind = error.get("type")
        reason = ValidationReason.OTHER_PYDANTIC_VALIDATION
        # Extra keys are always discarded, even when their name is a known field.
        if kind == "extra_forbidden":
            reason, path = ValidationReason.FORBIDDEN_EXTRA_FIELD, ()
        elif path:
            if kind in ("uuid_parsing", "uuid_type", "uuid_version"):
                reason = ValidationReason.INVALID_UUID
            elif path[-1] == "subject" and kind in (
                "string_pattern_mismatch",
                "string_too_long",
                "string_too_short",
            ):
                reason = ValidationReason.INVALID_SUBJECT_TOKEN
            elif kind in ("string_too_long", "string_too_short"):
                reason = ValidationReason.INVALID_TEXT_BOUND
            elif kind == "missing":
                reason = ValidationReason.MISSING_REQUIRED_FIELD
            elif kind == "literal_error":
                reason = ValidationReason.INVALID_ENUM
            elif kind in (
                "string_type",
                "tuple_type",
                "list_type",
                "model_type",
                "dict_type",
            ):
                reason = ValidationReason.INVALID_FIELD_TYPE
        candidates.append(PydanticDiagnostic(reason, path, min(len(errors), 64)))
    priorities = {reason: i for i, reason in enumerate(ValidationReason)}
    return (
        min(candidates, key=lambda d: (priorities[d.reason], repr(d.path)))
        if candidates
        else PydanticDiagnostic(ValidationReason.OTHER_PYDANTIC_VALIDATION)
    )
