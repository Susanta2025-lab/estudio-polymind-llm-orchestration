import json
import logging
from typing import Iterator, Mapping, Optional

import requests

from config.settings import settings
from llm.inference import (
    InferenceConnectionError,
    InferenceResponseError,
    ModelRole,
)

logger = logging.getLogger(__name__)


class OllamaClient:
    def __init__(
        self,
        model: Optional[str] = None,
        *,
        url: Optional[str] = None,
        model_map: Optional[Mapping[str, str]] = None,
        connect_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None,
        http_client=requests,
    ):
        self.model = model
        self.url = url or settings.OLLAMA_URL
        self.model_map = dict(model_map or settings.OLLAMA_MODEL_MAP)
        self.timeout = (
            connect_timeout or settings.INFERENCE_CONNECT_TIMEOUT,
            read_timeout or settings.INFERENCE_READ_TIMEOUT,
        )
        self.http_client = http_client

    @property
    def name(self) -> str:
        return "ollama"

    def model_id(self, role: ModelRole) -> str:
        try:
            return self.model or self.model_map[role.value]
        except KeyError as exc:
            raise InferenceResponseError(
                f"No served model is configured for role '{role.value}'."
            ) from exc

    def _payload(self, prompt: str, role: ModelRole, stream: bool) -> dict:
        return {
            "model": self.model_id(role),
            "messages": [{"role": "user", "content": prompt}],
            "stream": stream,
        }

    def generate(
        self,
        prompt: str,
        role: ModelRole = ModelRole.GENERAL,
    ) -> str:
        response = None
        try:
            response = self.http_client.post(
                self.url,
                json=self._payload(prompt, role, stream=False),
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            logger.exception("Ollama request failed (status=%s)", status)
            raise InferenceConnectionError("Inference provider request failed.") from exc
        else:
            try:
                content = response.json()["message"]["content"]
                if not isinstance(content, str):
                    raise TypeError("message.content is not text")
                return content
            except (ValueError, KeyError, TypeError) as exc:
                logger.exception("Ollama returned an invalid non-streaming response")
                raise InferenceResponseError("Inference provider returned an invalid response.") from exc
        finally:
            if response is not None and hasattr(response, "close"):
                response.close()

    def generate_stream(
        self,
        prompt: str,
        role: ModelRole = ModelRole.GENERAL,
    ) -> Iterator[str]:
        response = None
        try:
            response = self.http_client.post(
                self.url,
                json=self._payload(prompt, role, stream=True),
                stream=True,
                timeout=self.timeout,
            )
            response.raise_for_status()
            for line_number, line in enumerate(response.iter_lines(), start=1):
                if not line:
                    continue
                try:
                    chunk = json.loads(line.decode("utf-8"))
                    content = chunk["message"]["content"]
                    if not isinstance(content, str):
                        raise TypeError("message.content is not text")
                except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
                    logger.exception("Malformed Ollama stream chunk at line %d", line_number)
                    raise InferenceResponseError(
                        "Inference provider returned a malformed stream."
                    ) from exc
                if content:
                    yield content
        except requests.RequestException as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            logger.exception("Ollama streaming request failed (status=%s)", status)
            raise InferenceConnectionError("Inference provider request failed.") from exc
        finally:
            if response is not None and hasattr(response, "close"):
                response.close()
