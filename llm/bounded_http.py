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
    InferenceTimeoutError, OutputLimitDiagnostics,
)
from llm.operational import error_for_status


def rejection_diagnostics(response, started, total_seconds):
    """Read a small error envelope, emit only closed classifications, never prose."""
    result = {'http_status': response.status_code, 'reason': 'request_configuration'}
    data = bytearray()
    try:
        for chunk in response.iter_content(chunk_size=1):
            if time.monotonic() - started > total_seconds or len(data) + len(chunk) > 4096:
                return result
            data.extend(chunk)
        value = json.loads(data)
        error = value.get('error') if isinstance(value, dict) else None
        if isinstance(error, dict):
            # Status alone is never evidence of schema rejection. Do not retain
            # arbitrary codes, parameters or messages supplied by the upstream.
            code, param = error.get('code'), error.get('param')
            if code in ('invalid_json_schema', 'json_schema_invalid') and param in (
                    'response_format', 'response_format.json_schema', 'response_format.json_schema.schema'):
                result['reason'] = 'strict_schema_rejected'
            elif (code == 'invalid_request_error' and param == 'response_format'
                    and isinstance(error.get('message'), str)
                    and error['message'].startswith('Invalid schema for response_format')):
                result['reason'] = 'strict_schema_rejected'
    except (ValueError, TypeError, UnicodeError, RecursionError, requests.RequestException):
        pass  # Preserve the known HTTP classification if diagnostics are unavailable.
    return result


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
    completed = False
    started = time.monotonic()
    try:
        response = client.post(url, headers=headers, json=payload, stream=True,
                               allow_redirects=False,
                               timeout=(min(timeout[0], total_seconds), min(timeout[1], total_seconds)))
        status = response.status_code
        if 300 <= status < 400:
            raise InferenceConfigurationError('Inference redirects are forbidden.')
        if status >= 400:
            if status in (429, 502, 503):
                raise InferenceRateLimitError(retry_after=retry_after(response.headers))
            if status in (400, 422):
                error = InferenceConfigurationError('Inference request configuration rejected.')
                error.rejection_diagnostics = rejection_diagnostics(response, started, total_seconds)
                raise error
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
        value = json.loads(data, object_pairs_hook=unique)
        completed = True
        return value
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
            try:
                response.close()
            except (OSError, requests.RequestException):
                # Expected transport cleanup failures cannot replace an active
                # error (including cancellation). Programming defects propagate.
                if completed:
                    raise InferenceConnectionError('Inference provider cleanup failed.') from None


def validate_request(request):
    envelope = request.max_response_envelope_bytes
    if envelope is not None and (type(envelope) is not int or not 0 < envelope <= 24008192):
        raise InferenceConfigurationError('Invalid bounded inference configuration.')
    cap = request.capability
    if (type(request.output_tokens) is not int or not 0 < request.output_tokens <= cap.max_output_tokens
            or type(request.response_bytes) is not int or not 0 < request.response_bytes <= 4_000_000
            or not 0 < request.total_seconds <= 600):
        raise InferenceConfigurationError('Invalid bounded inference configuration.')


def result_text(text, request, finish_reason, *, usage=None, reasoning_tokens=None):
    if not isinstance(text, str) and not (text is None and finish_reason in ('length', 'max_tokens')):
        raise InferenceResponseError('Inference provider returned invalid content.')
    size = len(text.encode('utf-8')) if text is not None else None
    if finish_reason is not None and not isinstance(finish_reason, str):
        raise InferenceResponseError('Inference provider returned invalid termination metadata.')
    overflow = size is not None and size > request.response_bytes
    if overflow or finish_reason in ('length', 'max_tokens'):
        counts = (getattr(usage, 'prompt_tokens', None), getattr(usage, 'completion_tokens', None))
        total = getattr(usage, 'total_tokens', None)
        known = (all(type(x) is int and x >= 0 for x in counts)
                 and (total is None or type(total) is int and total == sum(counts)))
        raise InferenceOutputLimitError(diagnostics=OutputLimitDiagnostics(
            failure_cause=('response_bytes_exceeded' if overflow
                           else 'provider_completion_truncated'),
            response_bytes=size, response_byte_limit=request.response_bytes,
            finish_reason=(finish_reason if finish_reason in (None, 'stop', 'length', 'max_tokens') else 'other'),
            completion_tokens=counts[1] if type(counts[1]) is int and counts[1] >= 0 else None,
            completion_token_limit=request.output_tokens, reasoning_tokens=reasoning_tokens,
            usage_available=known))
    if finish_reason not in (None, 'stop'):
        raise InferenceResponseError('Inference provider did not complete structured output.')
    return text
