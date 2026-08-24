import logging
import re
from contextvars import ContextVar
from typing import Optional
from uuid import uuid4

from llm.inference import (
    InferenceAuthenticationError,
    InferenceConnectionError,
    InferenceError,
    InferenceModelUnavailableError,
    InferenceRateLimitError,
    InferenceTimeoutError,
)

logger = logging.getLogger(__name__)
_request_id: ContextVar[str] = ContextVar("request_id", default="-")
_SAFE_REQUEST_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,63}$")


def normalize_request_id(value: Optional[str]) -> str:
    if value and _SAFE_REQUEST_ID.fullmatch(value):
        return value
    return uuid4().hex


def set_request_id(value: str):
    return _request_id.set(value)


def reset_request_id(token) -> None:
    _request_id.reset(token)


def request_id() -> str:
    return _request_id.get()


def error_for_status(status: Optional[int]) -> InferenceError:
    if status in (401, 403):
        return InferenceAuthenticationError("Inference provider authentication failed.")
    if status == 404:
        return InferenceModelUnavailableError("Inference model is unavailable.")
    if status in (408, 504):
        return InferenceTimeoutError("Inference provider request timed out.")
    if status == 429 or status in (502, 503):
        return InferenceRateLimitError("Inference provider is temporarily unavailable.")
    if status is not None:
        return InferenceError("Inference provider request failed.")
    return InferenceConnectionError("Inference provider request failed.")


def application_status(error: InferenceError) -> int:
    """Map provider failures without reflecting upstream HTTP status directly."""
    if error.category in {
        "provider_unreachable",
        "timeout",
        "authentication_failure",
        "overloaded",
        "model_unavailable",
    }:
        return 503
    return 502
