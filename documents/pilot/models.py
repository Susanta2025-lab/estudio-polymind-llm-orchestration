"""Versioned operator records. Templates are never consent or spending authority."""

from typing import Literal
from uuid import UUID

from pydantic import AwareDatetime, Field, model_validator

from documents.jobs.models import Token
from documents.models import Digest, FrozenModel, Scope


class PilotError(RuntimeError):
    def __init__(self, category="pilot_denied"):
        self.category = (
            category
            if category
            in {
                "pilot_denied",
                "pilot_stopped",
                "pilot_limit",
                "pilot_not_ready",
                "pilot_source_refused",
                "pilot_reconciliation_required",
            }
            else "pilot_denied"
        )
        super().__init__(self.category)


class PilotPolicy(FrozenModel):
    version: Literal["supervised-pilot/1"] = "supervised-pilot/1"
    max_source_bytes: int = Field(default=1_000_000, gt=0, le=1_000_000)
    max_pages: int = Field(default=4, gt=0, le=4)
    max_characters: int = Field(default=4000, gt=0, le=4000)
    max_synthesis_calls: int = Field(default=3, gt=0, le=3)
    max_questions: int = Field(default=3, gt=0, le=3)
    max_input: int = Field(default=24800, gt=0, le=24800)
    max_output: int = Field(default=3000, gt=0, le=3000)
    session_seconds: int = Field(default=3600, gt=0, le=86400)
    workflow_seconds: int = Field(default=600, gt=0, le=600)
    provider_seconds: int = Field(default=60, gt=0, le=60)
    audit_limit: int = Field(default=10000, gt=0, le=100000)
    max_sessions: int = Field(default=3, gt=0, le=3)


class SourceApproval(FrozenModel):
    version: Literal["pilot-source/1"] = "pilot-source/1"
    approval_id: Token
    document_id: UUID
    owner: Scope
    source_id: Token
    sha256: Digest
    filename: str = Field(pattern=r"^[A-Za-z0-9_.-]{1,128}\.(pdf|txt)$")
    mime: Literal["application/pdf", "text/plain"]
    classification: Literal["synthetic", "licensed_public"]
    rights_reference: Token
    rights_approved: Literal[True]
    native_text_reviewed: Literal[True]
    provider_processing_approved: Literal[True]
    retention: Literal["approved_retained_nonpersonal"]
    erasure_required: Literal[False]
    approved_by: UUID
    approved_at: AwareDatetime
    expires_at: AwareDatetime
    retained_digest_sha256: Digest | None = None

    @model_validator(mode="after")
    def valid(self):
        if (
            ".." in self.filename
            or self.filename.startswith(".")
            or self.filename.endswith(".pdf") != (self.mime == "application/pdf")
            or self.expires_at <= self.approved_at
        ):
            raise ValueError("invalid source approval")
        return self


class SessionApproval(FrozenModel):
    version: Literal["pilot-session/1"] = "pilot-session/1"
    session_id: UUID
    study_code: str = Field(pattern=r"^P[0-9]{3}$")
    notice_version: Token
    purpose: Literal["supervised_document_verification"]
    mode: Literal["synthetic", "external"]
    consent: Literal["synthetic_fixture", "provided"]
    consent_at: AwareDatetime | None
    approval_reference: Token
    source_approval: Token
    approved_by: UUID
    approved_at: AwareDatetime
    expires_at: AwareDatetime
    provider_processing_approved: Literal[True]
    retention_reference: Token
    metadata_retention_until: AwareDatetime
    # Separate decisions, not populated automatically from a fixture or CI.
    exposure_approval: Token | None = None
    privacy_approval: Token | None = None
    quality_approval: Token | None = None
    zero_paid_execution: Literal[True] = True

    @model_validator(mode="after")
    def valid(self):
        if (
            self.expires_at <= self.approved_at
            or self.metadata_retention_until < self.expires_at
        ):
            raise ValueError("invalid session dates")
        if self.mode == "synthetic":
            if self.consent != "synthetic_fixture" or self.consent_at is not None:
                raise ValueError("fixtures are not consent")
        elif (
            self.consent != "provided"
            or self.consent_at is None
            or self.consent_at > self.approved_at
            or not all(
                (self.exposure_approval, self.privacy_approval, self.quality_approval)
            )
        ):
            raise ValueError("separate consent and exposure decisions required")
        return self


class Feedback(FrozenModel):
    version: Literal["pilot-feedback/1"] = "pilot-feedback/1"
    usefulness: int = Field(ge=1, le=5)
    would_repeat: bool
    notice_understood: bool
    issue: Literal["none", "citation", "coverage", "incorrect", "usability", "other"]
    # No free text: source content, names and credentials do not belong in analytics.


class ReviewFinding(FrozenModel):
    version: Literal["pilot-review/1"] = "pilot-review/1"
    reviewer_code: Token
    evidence_sha256: Digest
    findings_reference: Token
    completed_at: AwareDatetime
    qualified: Literal[True]
    independent: Literal[True]
    outcome: Literal["accepted", "changes_required"]
