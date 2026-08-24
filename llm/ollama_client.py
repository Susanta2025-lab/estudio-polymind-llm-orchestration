import json
import logging
import time
from typing import Iterator, Mapping, Optional

import requests

from config.settings import settings
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


class OllamaClient:
    def __init__(
        self,
        model: Optional[str] = None,
        *,
        url: Optional[str] = None,
        model_map: Optional[Mapping[str, str]] = None,
        connect_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None,
        readiness_timeout: float = 3.0,
        readiness_retries: int = 1,
        readiness_backoff: float = 0.1,
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
        self.readiness_timeout = readiness_timeout
        self.readiness_retries = readiness_retries
        self.readiness_backoff = readiness_backoff
        self.tags_url = self.url.split("/api/", 1)[0].rstrip("/") + "/api/tags"

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

    def check_readiness(self) -> ReadinessResult:
        models = {role.value: self.model_id(role) for role in ModelRole}
        for attempt in range(self.readiness_retries + 1):
            response = None
            try:
                response = self.http_client.get(self.tags_url, timeout=self.readiness_timeout)
                response.raise_for_status()
                items = response.json()["models"]
                if not isinstance(items, list):
                    raise TypeError("models is not a list")
                available = {
                    item["name"] for item in items
                    if isinstance(item, dict) and isinstance(item.get("name"), str)
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
                status = ReadinessStatus(error_for_status(code).category)
            except (ValueError, KeyError, TypeError):
                status = ReadinessStatus.PROTOCOL_FAILURE
            finally:
                if response is not None and hasattr(response, "close"):
                    response.close()
            if attempt < self.readiness_retries and status in {
                ReadinessStatus.UNREACHABLE, ReadinessStatus.TIMEOUT,
                ReadinessStatus.OVERLOADED, ReadinessStatus.UPSTREAM_FAILURE,
            }:
                time.sleep(self.readiness_backoff * (attempt + 1))
                continue
            return ReadinessResult(status, self.name, models)
        raise AssertionError("readiness attempts exhausted")

    def generate(
        self,
        prompt: str,
        role: ModelRole = ModelRole.GENERAL,
    ) -> str:
        response = None
        model = self.model_id(role)
        try:
            response = self.http_client.post(
                self.url,
                json=self._payload(prompt, role, stream=False),
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.Timeout as exc:
            logger.warning(
                "Inference timed out request_id=%s provider=%s role=%s model=%s stream=false",
                request_id(),
                self.name,
                role.value,
                model,
            )
            raise InferenceTimeoutError("Inference provider request timed out.") from exc
        except requests.RequestException as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            logger.warning(
                "Inference failed request_id=%s provider=%s role=%s model=%s stream=false status=%s",
                request_id(),
                self.name,
                role.value,
                model,
                status,
            )
            raise error_for_status(status) from exc
        else:
            try:
                content = response.json()["message"]["content"]
                if not isinstance(content, str):
                    raise TypeError("message.content is not text")
                logger.info(
                    "Inference succeeded provider=%s role=%s model=%s stream=false",
                    self.name,
                    role.value,
                    model,
                )
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
        model = self.model_id(role)
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
            logger.info(
                "Inference succeeded provider=%s role=%s model=%s stream=true",
                self.name,
                role.value,
                model,
            )
        except requests.Timeout as exc:
            logger.warning(
                "Inference timed out request_id=%s provider=%s role=%s model=%s stream=true",
                request_id(),
                self.name,
                role.value,
                model,
            )
            raise InferenceTimeoutError("Inference provider request timed out.") from exc
        except requests.RequestException as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            logger.warning(
                "Inference failed request_id=%s provider=%s role=%s model=%s stream=true status=%s",
                request_id(),
                self.name,
                role.value,
                model,
                status,
            )
            raise error_for_status(status) from exc
        finally:
            if response is not None and hasattr(response, "close"):
                response.close()
