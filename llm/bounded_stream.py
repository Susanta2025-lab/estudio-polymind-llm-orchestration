"""Bounded SSE reader for the additive governed Chat streaming capability."""
import json
import time
import requests

from llm.bounded_http import retry_after
from llm.operational import error_for_status
from llm.inference import (InferenceConfigurationError, InferenceConnectionError,
    InferenceOutputLimitError, InferenceRateLimitError, InferenceResponseError, InferenceTimeoutError)


def request_stream(client, url, *, headers, payload, timeout, total_seconds, max_bytes, on_chunk, allowed_models=(), response_bytes=16000):
    """Bounded SSE → completion envelope, retaining usage for governed settlement."""
    response = None
    started = time.monotonic()
    content, usage, model, finish = [], None, None, None
    content_size = 0
    count, line = 0, bytearray()
    done = False
    try:
        payload = {**payload, 'stream': True, 'stream_options': {'include_usage': True}}
        response = client.post(url, headers=headers, json=payload, stream=True, allow_redirects=False,
            timeout=(min(timeout[0], total_seconds), min(timeout[1], total_seconds)))
        if response.status_code >= 300:
            if response.status_code in (429, 502, 503):
                raise InferenceRateLimitError(retry_after=retry_after(response.headers))
            if response.status_code < 400:
                raise InferenceConfigurationError('Inference redirects are forbidden.')
            raise error_for_status(response.status_code)
        for chunk in response.iter_content(chunk_size=1):
            count += len(chunk)
            if time.monotonic() - started > total_seconds:
                raise InferenceTimeoutError('Inference request deadline exceeded.')
            if count > max_bytes:
                raise InferenceOutputLimitError('Inference response limit exceeded.')
            if chunk != b'\n':
                line.extend(chunk)
                continue
            raw = bytes(line).strip(); line.clear()
            if not raw or raw.startswith(b':'):
                continue
            if not raw.startswith(b'data:'):
                raise InferenceResponseError('Invalid inference stream.')
            raw = raw[5:].strip()
            if raw == b'[DONE]':
                done = True
                break
            event = json.loads(raw)
            if not isinstance(event, dict) or not isinstance(event.get('choices'), list):
                raise InferenceResponseError('Invalid inference stream.')
            returned = event.get('model')
            if returned is not None:
                if type(returned) is not str or returned not in allowed_models or model is not None and model != returned:
                    raise InferenceResponseError('Invalid inference stream model.')
                model = returned
            if event.get('usage') is not None:
                if usage is not None:
                    raise InferenceResponseError('Duplicate inference usage.')
                usage = event['usage']
            choices = event['choices']
            if not choices:
                if event.get('usage') is None and not isinstance(event.get('prompt_filter_results'), list):
                    raise InferenceResponseError('Invalid inference stream metadata.')
                continue
            if len(choices) != 1 or not isinstance(choices[0], dict):
                raise InferenceResponseError('Invalid inference choices.')
            first = choices[0]
            delta = first.get('delta')
            if not isinstance(delta, dict) or delta.get('refusal') is not None:
                raise InferenceResponseError('Invalid inference content.')
            token = delta.get('content')
            if token is not None:
                if type(token) is not str or finish is not None:
                    raise InferenceResponseError('Invalid inference content.')
                content_size += len(token.encode('utf-8'))
                if content_size > response_bytes:
                    raise InferenceOutputLimitError('Inference content limit exceeded.')
                content.append(token)
                on_chunk(token)
            if first.get('finish_reason') is not None:
                if finish is not None:
                    raise InferenceResponseError('Duplicate inference termination.')
                finish = first['finish_reason']
        if not done or finish is None:
            raise InferenceResponseError('Incomplete inference stream.')
        return {'model': model or payload['model'], 'usage': usage,
                'choices': [{'message': {'content': ''.join(content)}, 'finish_reason': finish}]}
    except requests.Timeout:
        raise InferenceTimeoutError('Inference provider request timed out.') from None
    except requests.RequestException:
        raise InferenceConnectionError('Inference provider request failed.') from None
    except (ValueError, TypeError, UnicodeError):
        raise InferenceResponseError('Invalid inference stream.') from None
    finally:
        if response is not None:
            response.close()
