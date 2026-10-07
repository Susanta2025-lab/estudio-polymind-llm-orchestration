"""Bounded HTTP response reading for the existing provider adapters only."""
import json
import math
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import requests
from urllib3.exceptions import ReadTimeoutError

from llm.inference import (
    InferenceConfigurationError, InferenceConnectionError,
    InferenceOutputLimitError, InferenceRateLimitError, InferenceResponseError,
    InferenceTimeoutError,
)
from llm.operational import error_for_status


def retry_after(headers, now=None):
    value = headers.get('Retry-After')
    if value is None:
        return None
    try:
        seconds = float(value)
    except (ValueError, TypeError):
        try:
            seconds = (parsedate_to_datetime(value) - (now or datetime.now(timezone.utc))).total_seconds()
        except (ValueError, TypeError, OverflowError):
            return None
    # Clamp very long valid hints to the maximum job budget, which fails closed
    # at its deadline rather than ignoring the hint and retrying early.
    return min(604800, max(0, seconds)) if math.isfinite(seconds) else None


def request_json(client, url, *, headers, payload, timeout, total_seconds, max_bytes):
    response = None
    started = time.monotonic()
    try:
        response = client.post(url, headers=headers, json=payload, stream=True,
                               timeout=(min(timeout[0], total_seconds), min(timeout[1], total_seconds)))
        status = response.status_code
        if status >= 400:
            if status in (429, 502, 503):
                raise InferenceRateLimitError(retry_after=retry_after(response.headers))
            if status in (400, 422):
                raise InferenceConfigurationError('Inference request configuration rejected.')
            if status >= 500 and status not in (502, 503, 504):
                raise InferenceConnectionError('Inference provider is unavailable.')
            raise error_for_status(status)
        data = bytearray()
        # One-byte reads ensure a trickling peer cannot hide indefinitely inside
        # a large buffered read. The socket inactivity timeout bounds each read.
        for chunk in response.iter_content(chunk_size=1):
            if time.monotonic() - started > total_seconds:
                raise InferenceTimeoutError('Inference request deadline exceeded.')
            if len(data) + len(chunk) > max_bytes:
                raise InferenceOutputLimitError('Inference response limit exceeded.')
            data.extend(chunk)
        if time.monotonic() - started > total_seconds:
            raise InferenceTimeoutError('Inference request deadline exceeded.')
        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError()
                result[key] = value
            return result
        return json.loads(data, object_pairs_hook=unique)
    except requests.Timeout:
        raise InferenceTimeoutError('Inference provider request timed out.') from None
    except requests.RequestException as exc:
        # requests wraps a socket read timeout while consuming a streamed body.
        if any(isinstance(arg, ReadTimeoutError) for arg in exc.args):
            raise InferenceTimeoutError('Inference provider request timed out.') from None
        raise InferenceConnectionError('Inference provider request failed.') from None
    except (ValueError, TypeError, UnicodeError, RecursionError):
        raise InferenceResponseError('Inference provider returned an invalid response.') from None
    finally:
        if response is not None:
            response.close()


def validate_request(request):
    cap = request.capability
    if (type(request.output_tokens) is not int or not 0 < request.output_tokens <= cap.max_output_tokens
            or type(request.response_bytes) is not int or not 0 < request.response_bytes <= 4_000_000
            or not 0 < request.total_seconds <= 600):
        raise InferenceConfigurationError('Invalid bounded inference configuration.')


def result_text(text, request, finish_reason):
    if not isinstance(text, str):
        raise InferenceResponseError('Inference provider returned invalid content.')
    if len(text.encode('utf-8')) > request.response_bytes or finish_reason in ('length', 'max_tokens'):
        raise InferenceOutputLimitError('Inference output limit exceeded.')
    if finish_reason not in (None, 'stop'):
        raise InferenceResponseError('Inference provider did not complete structured output.')
    return text
