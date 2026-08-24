import json
import logging
import time
from typing import Any, Iterator, Mapping, Optional

import requests

from llm.inference import (
    InferenceConnectionError,
    InferenceResponseError,
    InferenceTimeoutError,
    ModelRole,
    ReadinessResult,
    ReadinessStatus,
)
from llm.operational import error_for_status, request_id

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
        readiness_timeout: float = 3.0,
        readiness_retries: int = 1,
        readiness_backoff: float = 0.1,
        http_client=None,
    ):
        self.base_url = base_url.rstrip("/")
        self.url = f"{self.base_url}/chat/completions"
        self.models_url = f"{self.base_url}/models"
        self.model_map = dict(model_map)
        self.timeout = (connect_timeout, read_timeout)
        self.generation_parameters = dict(generation_parameters or {})
        self.readiness_timeout = readiness_timeout
        self.readiness_retries = readiness_retries
        self.readiness_backoff = readiness_backoff
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

    def check_readiness(self) -> ReadinessResult:
        models = {role.value: self.model_id(role) for role in ModelRole}
        for attempt in range(self.readiness_retries + 1):
            response = None
            try:
                response = self.http_client.get(
                    self.models_url, headers=self.headers, timeout=self.readiness_timeout
                )
                response.raise_for_status()
                payload = response.json()
                items = payload["data"]
                if not isinstance(items, list):
                    raise TypeError("data is not a list")
                available = {
                    item["id"] for item in items
                    if isinstance(item, dict) and isinstance(item.get("id"), str)
                }
                if len(available) != len(items):
                    raise TypeError("model entry is malformed")
                status = (ReadinessStatus.READY if set(models.values()) <= available
                          else ReadinessStatus.MODEL_UNAVAILABLE)
                return ReadinessResult(status, self.name, models)
            except requests.Timeout:
                status = ReadinessStatus.TIMEOUT
            except requests.RequestException as exc:
                code = getattr(getattr(exc, "response", None), "status_code", None)
                category = error_for_status(code).category
                status = ReadinessStatus(category)
            except (ValueError, KeyError, TypeError):
                status = ReadinessStatus.PROTOCOL_FAILURE
            finally:
                if response is not None:
                    response.close()
            if attempt < self.readiness_retries and status in {
                ReadinessStatus.UNREACHABLE, ReadinessStatus.TIMEOUT,
                ReadinessStatus.OVERLOADED, ReadinessStatus.UPSTREAM_FAILURE,
            }:
                time.sleep(self.readiness_backoff * (attempt + 1))
                continue
            return ReadinessResult(status, self.name, models)
        raise AssertionError("readiness attempts exhausted")

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
                "OpenAI-compatible inference timed out request_id=%s provider=%s role=%s model=%s",
                request_id(),
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
                "model=%s status=%s request_id=%s",
                self.name,
                role.value,
                self.model_id(role),
                status,
                request_id(),
            )
            raise error_for_status(status) from exc

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
