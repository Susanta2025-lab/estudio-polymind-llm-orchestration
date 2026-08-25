"""Narrow application-edge security controls."""

from __future__ import annotations

import secrets
import logging
from dataclasses import dataclass
from typing import Optional

from starlette.responses import JSONResponse

from llm.metrics import metrics
from llm.operational import normalize_request_id, reset_request_id, set_request_id


logger = logging.getLogger(__name__)


PROTECTED_EXACT_PATHS = frozenset({"/query", "/query/stream"})
PROTECTED_PREFIXES = ("/memory/",)


@dataclass(frozen=True)
class AuthenticationResult:
    allowed: bool
    reason: str
    endpoint_class: str


def endpoint_class(path: str) -> Optional[str]:
    if path in PROTECTED_EXACT_PATHS:
        return "query"
    if any(path.startswith(prefix) for prefix in PROTECTED_PREFIXES):
        return "memory"
    return None


def documentation_urls(enabled: bool) -> tuple[Optional[str], Optional[str], Optional[str]]:
    if enabled:
        return "/docs", "/redoc", "/openapi.json"
    return None, None, None


def authenticate_bearer(path: str, authorization: Optional[str], expected_token: str) -> AuthenticationResult:
    protected_class = endpoint_class(path)
    if protected_class is None:
        return AuthenticationResult(True, "not_required", "other")
    if not authorization:
        return AuthenticationResult(False, "missing", protected_class)
    scheme, separator, provided = authorization.partition(" ")
    if not separator or scheme.lower() != "bearer" or not provided or " " in provided:
        return AuthenticationResult(False, "malformed", protected_class)
    if not secrets.compare_digest(provided, expected_token):
        return AuthenticationResult(False, "invalid", protected_class)
    return AuthenticationResult(True, "accepted", protected_class)


class _RequestTooLarge(Exception):
    pass


class ApplicationSecurityMiddleware:
    """Correlate, authenticate, and bound requests without buffering bodies."""

    def __init__(self, app, configuration):
        self.app = app
        self.configuration = configuration

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = {name.lower(): value for name, value in scope.get("headers", ())}
        supplied_request_id = headers.get(b"x-request-id")
        correlation_id = normalize_request_id(
            supplied_request_id.decode("ascii", errors="ignore") if supplied_request_id else None
        )
        context_token = set_request_id(correlation_id)
        scope.setdefault("state", {})["request_id"] = correlation_id
        protected_class = endpoint_class(scope.get("path", ""))

        async def correlated_send(message):
            if message["type"] == "http.response.start":
                message.setdefault("headers", []).append((b"x-request-id", correlation_id.encode("ascii")))
            await send(message)

        async def respond(status_code: int, detail: str, authenticate: bool = False):
            response_headers = {"WWW-Authenticate": "Bearer"} if authenticate else None
            response = JSONResponse(status_code=status_code, content={"detail": detail}, headers=response_headers)
            await response(scope, receive, correlated_send)

        try:
            if protected_class is not None and self.configuration.API_AUTH_ENABLED:
                authorization = headers.get(b"authorization")
                auth = authenticate_bearer(
                    scope.get("path", ""),
                    authorization.decode("latin-1") if authorization else None,
                    self.configuration.API_AUTH_TOKEN.get_secret_value(),
                )
                metrics.observe_authentication(
                    auth.endpoint_class, "accepted" if auth.allowed else "rejected"
                )
                if not auth.allowed:
                    metrics.observe_request_rejection(auth.endpoint_class, f"auth_{auth.reason}")
                    logger.warning(
                        "Authentication rejected request_id=%s endpoint_class=%s reason=%s",
                        correlation_id,
                        auth.endpoint_class,
                        auth.reason,
                    )
                    await respond(401, "Authentication required.", authenticate=True)
                    return

            if protected_class != "query":
                await self.app(scope, receive, correlated_send)
                return

            limit = self.configuration.MAX_REQUEST_BYTES

            async def reject():
                metrics.observe_request_rejection("query", "request_too_large")
                logger.warning(
                    "Request rejected request_id=%s endpoint_class=query reason=request_too_large",
                    correlation_id,
                )
                await respond(413, "Request body is too large.")

            declared = headers.get(b"content-length")
            if declared is not None:
                try:
                    if int(declared) < 0 or int(declared) > limit:
                        await reject()
                        return
                except ValueError:
                    await reject()
                    return

            consumed = 0

            async def limited_receive():
                nonlocal consumed
                message = await receive()
                if message["type"] == "http.request":
                    consumed += len(message.get("body", b""))
                    if consumed > limit:
                        raise _RequestTooLarge
                return message

            try:
                await self.app(scope, limited_receive, correlated_send)
            except _RequestTooLarge:
                await reject()
        finally:
            reset_request_id(context_token)
