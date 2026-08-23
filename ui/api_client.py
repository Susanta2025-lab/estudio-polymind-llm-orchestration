import json
from typing import Callable, Dict, Iterator

import requests


class APIStreamError(RuntimeError):
    pass


def stream_query(
    url: str,
    query: str,
    session_id: str,
    timeout: float,
    *,
    post: Callable = requests.post,
) -> Iterator[Dict]:
    """Issue exactly one API request and parse its NDJSON event stream."""
    response = None
    try:
        response = post(
            url,
            json={"query": query, "session_id": session_id},
            stream=True,
            timeout=timeout,
        )
        response.raise_for_status()
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue
            try:
                event = json.loads(line)
            except (TypeError, json.JSONDecodeError) as exc:
                raise APIStreamError("API returned a malformed stream.") from exc
            if not isinstance(event, dict) or "type" not in event:
                raise APIStreamError("API returned an invalid stream event.")
            yield event
    except requests.RequestException as exc:
        raise APIStreamError("Unable to connect to the PolyMind API.") from exc
    finally:
        if response is not None and hasattr(response, "close"):
            response.close()
