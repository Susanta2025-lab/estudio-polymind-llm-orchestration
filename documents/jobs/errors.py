"""Allowlisted operational categories, never arbitrary exception text."""

from typing import Literal, get_args
from pydantic import Field
from documents.errors import Category, DocumentError
from documents.models import FrozenModel

CATEGORIES = frozenset(get_args(Category)) | frozenset({
    'idempotency_conflict', 'invalid_transition', 'job_not_found', 'step_not_found',
    'lease_conflict', 'stale_fence', 'lease_expired', 'retry_exhausted', 'cancelled',
    'ledger_error', 'dispatch_error', 'manifest_conflict', 'invalid_configuration',
    'schema_mismatch', 'worker_interrupted', 'worker_failed', 'profile_mismatch',
    'inference_rate_limited', 'inference_timeout', 'inference_unavailable',
    'inference_authentication', 'inference_configuration', 'inference_invalid_response',
    'inference_context_exceeded', 'inference_output_limit', 'inference_unknown',
})


class JobError(RuntimeError):
    def __init__(self, category: str):
        self.category = category if category in CATEGORIES else 'ledger_error'
        super().__init__(self.category)


class Failure(FrozenModel):
    category: str
    classification: Literal['RETRYABLE', 'NON_RETRYABLE', 'CANCELLED']
    retry_after: float | None = Field(default=None, ge=0, le=604800)

    def sanitized(self):
        return Failure(category=self.category if self.category in CATEGORIES else 'worker_failed',
                       classification=self.classification, retry_after=self.retry_after)


def classify(error: Exception, *, transient_storage: bool = False) -> Failure:
    """Storage retry needs explicit adapter/caller knowledge of transience."""
    category = error.category if isinstance(error, (DocumentError, JobError)) else 'worker_failed'
    category = category if category in CATEGORIES else 'worker_failed'
    kind = ('CANCELLED' if category == 'cancelled' else
            'RETRYABLE' if category == 'worker_interrupted' or
            (category == 'storage_error' and transient_storage) else 'NON_RETRYABLE')
    return Failure(category=category, classification=kind)
