import json
import logging
from typing import Any, Iterator, Mapping, Optional

import requests

from llm.inference import (
    InferenceConnectionError,
    InferenceResponseError,
    InferenceTimeoutError,
    ModelRole,
)

logger = logging.getLogger(__name__)


class OpenAICompatibleProvider:
    """Chat-completions adapter for external OpenAI-compatible servers such as vLLM."""

    def __init__(
        self,
        *,
        base_url: str,
        model_map: Mapping[str, str],
        api_key: Optional[str] = None,
        connect_timeout: float = 5.0,
        read_timeout: float = 120.0,
        generation_parameters: Optional[Mapping[str, Any]] = None,
        http_client=None,
    ):
        self.url = f"{base_url.rstrip('/')}/chat/completions"
        self.model_map = dict(model_map)
        self.timeout = (connect_timeout, read_timeout)
        self.generation_parameters = dict(generation_parameters or {})
        reserved = {"model", "messages", "stream"}.intersection(
            self.generation_parameters
        )
        if reserved:
            raise ValueError(
                "Generation parameters contain reserved keys: "
                f"{sorted(reserved)}"
            )
        self.http_client = http_client if http_client is not None else requests.Session()
        self.headers = {"Accept": "application/json"}
        if api_key and api_key.strip():
            self.headers["Authorization"] = f"Bearer {api_key}"

    @property
    def name(self) -> str:
        return "openai_compatible"

    def model_id(self, role: ModelRole) -> str:
        try:
            return self.model_map[role.value]
        except KeyError as exc:
            raise InferenceResponseError(
                f"No served model is configured for role '{role.value}'."
            ) from exc

    def _payload(self, prompt: str, role: ModelRole, stream: bool) -> dict:
        return {
            "model": self.model_id(role),
            "messages": [{"role": "user", "content": prompt}],
            "stream": stream,
            **self.generation_parameters,
        }

    def _request(self, prompt: str, role: ModelRole, stream: bool):
        response = None
        try:
            response = self.http_client.post(
                self.url,
                headers=self.headers,
                json=self._payload(prompt, role, stream),
                stream=stream,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response
        except requests.Timeout as exc:
            if response is not None:
                response.close()
            logger.warning(
                "OpenAI-compatible inference timed out provider=%s role=%s model=%s",
                self.name,
                role.value,
                self.model_id(role),
            )
            raise InferenceTimeoutError("Inference provider request timed out.") from exc
        except requests.RequestException as exc:
            if response is not None:
                response.close()
            status = getattr(getattr(exc, "response", None), "status_code", None)
            logger.warning(
                "OpenAI-compatible inference request failed provider=%s role=%s "
                "model=%s status=%s",
                self.name,
                role.value,
                self.model_id(role),
                status,
            )
            raise InferenceConnectionError("Inference provider request failed.") from exc

    @staticmethod
    def _completion_content(payload: Any) -> str:
        try:
            choices = payload["choices"]
            if not isinstance(choices, list) or not choices:
                raise TypeError("choices is not a non-empty list")
            message = choices[0]["message"]
            content = message["content"]
            if not isinstance(content, str):
                raise TypeError("message.content is not text")
            return content
        except (KeyError, IndexError, TypeError) as exc:
            raise InferenceResponseError(
                "Inference provider returned an invalid response."
            ) from exc

    @staticmethod
    def _stream_content(payload: Any) -> Optional[str]:
        try:
            choices = payload["choices"]
            if not isinstance(choices, list):
                raise TypeError("choices is not a list")
            if not choices:
                if isinstance(payload.get("usage"), dict):
                    return None
                raise TypeError("choices is empty without usage")
            delta = choices[0]["delta"]
            if not isinstance(delta, dict):
                raise TypeError("delta is not an object")
            content = delta.get("content")
            if content is not None and not isinstance(content, str):
                raise TypeError("delta.content is not text")
            return content
        except (KeyError, IndexError, TypeError) as exc:
            raise InferenceResponseError(
                "Inference provider returned a malformed stream."
            ) from exc

    def generate(
        self,
        prompt: str,
        role: ModelRole = ModelRole.GENERAL,
    ) -> str:
        response = None
        model = self.model_id(role)
        try:
            response = self._request(prompt, role, stream=False)
            try:
                content = self._completion_content(response.json())
            except ValueError as exc:
                raise InferenceResponseError(
                    "Inference provider returned an invalid response."
                ) from exc
            logger.info(
                "Inference succeeded provider=%s role=%s model=%s stream=false",
                self.name,
                role.value,
                model,
            )
            return content
        except InferenceResponseError:
            logger.warning(
                "Invalid inference response provider=%s role=%s model=%s stream=false",
                self.name,
                role.value,
                model,
            )
            raise
        finally:
            if response is not None:
                response.close()

    def generate_stream(
        self,
        prompt: str,
        role: ModelRole = ModelRole.GENERAL,
    ) -> Iterator[str]:
        response = None
        model = self.model_id(role)
        completed = False
        try:
            response = self._request(prompt, role, stream=True)
            for line_number, line in enumerate(
                response.iter_lines(decode_unicode=True), start=1
            ):
                if not line or line.startswith(":"):
                    continue
                if not line.startswith("data:"):
                    raise InferenceResponseError(
                        "Inference provider returned a malformed stream."
                    )
                data = line[5:].strip()
                if data == "[DONE]":
                    completed = True
                    break
                try:
                    payload = json.loads(data)
                except (TypeError, json.JSONDecodeError) as exc:
                    logger.warning(
                        "Malformed OpenAI-compatible SSE JSON provider=%s line=%d",
                        self.name,
                        line_number,
                    )
                    raise InferenceResponseError(
                        "Inference provider returned a malformed stream."
                    ) from exc
                content = self._stream_content(payload)
                if content:
                    yield content
            if not completed:
                raise InferenceResponseError(
                    "Inference provider stream ended before completion."
                )
            logger.info(
                "Inference succeeded provider=%s role=%s model=%s stream=true",
                self.name,
                role.value,
                model,
            )
        except requests.Timeout as exc:
            logger.warning(
                "Inference stream timed out provider=%s role=%s model=%s",
                self.name,
                role.value,
                model,
            )
            raise InferenceTimeoutError("Inference provider request timed out.") from exc
        except requests.RequestException as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            logger.warning(
                "Inference stream failed provider=%s role=%s model=%s status=%s",
                self.name,
                role.value,
                model,
                status,
            )
            raise InferenceConnectionError("Inference provider request failed.") from exc
        except InferenceResponseError:
            logger.warning(
                "Invalid inference response provider=%s role=%s model=%s stream=true",
                self.name,
                role.value,
                model,
            )
            raise
        finally:
            if response is not None:
                response.close()
