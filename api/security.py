"""Narrow application-edge security controls."""

from __future__ import annotations

import secrets
import logging
import asyncio
from dataclasses import dataclass
from typing import Optional

from starlette.responses import JSONResponse

from llm.metrics import metrics
from llm.operational import normalize_request_id, reset_request_id, set_request_id


logger = logging.getLogger(__name__)


PROTECTED_EXACT_PATHS = frozenset({"/query", "/query/stream", "/documents/analyze"})


@dataclass(frozen=True)
class AuthenticationResult:
    allowed: bool
    reason: str
    endpoint_class: str


def endpoint_class(path: str) -> Optional[str]:
    if path in PROTECTED_EXACT_PATHS:
        return 'document' if path.startswith('/documents/') else 'query'
    if path.startswith('/memory/'):
        return "memory"
    if path.startswith('/documents/'):
        return 'document'
    if path.startswith('/jobs/'):
        return 'job'
    if path == '/usage' or path.startswith('/usage/'):
        return 'usage'
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

    def __init__(self, app, configuration, runtime_getter=None):
        self.app = app
        self.configuration = configuration
        self.runtime_getter = runtime_getter

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
        mode = getattr(self.configuration, 'authentication_mode',
                       'static_bearer' if self.configuration.API_AUTH_ENABLED else 'disabled')
        runtime = None
        response_started = False

        async def correlated_send(message):
            nonlocal response_started
            if message["type"] == "http.response.start":
                message.setdefault("headers", []).append((b"x-request-id", correlation_id.encode("ascii")))
            snapshot = scope['state'].get('release_snapshot')
            if mode == 'oidc_jwt' and snapshot is not None:
                with runtime.authority.release(snapshot):
                    await asyncio.wait_for(send(message),timeout=5)
            else:
                await send(message)
            if message['type'] == 'http.response.start':
                response_started = True

        async def respond(status_code: int, detail: str, authenticate: bool = False):
            response_headers = {"WWW-Authenticate": "Bearer"} if authenticate else None
            response = JSONResponse(status_code=status_code, content={"detail": detail}, headers=response_headers)
            await response(scope, receive, correlated_send)

        try:
            if protected_class is not None and mode == 'oidc_jwt':
                from security.models import SecurityError
                try:
                    runtime = self.runtime_getter() if self.runtime_getter else None
                    if runtime is None:
                        await respond(503, 'Security service is unavailable.')
                        return
                    values = [v for k,v in scope.get('headers',()) if k.lower() == b'authorization']
                    if len(values) != 1:
                        raise SecurityError('authentication_required')
                    scheme,separator,token=values[0].decode('ascii').partition(' ')
                    if not separator or scheme.lower() != 'bearer' or not token or any(c.isspace() for c in token):
                        raise SecurityError('authentication_required')
                    principal=runtime.verifier.verify(token)
                    runtime.authority.register(principal)
                    scope['state']['principal']=principal
                    scope['state']['release_snapshot']=runtime.authority.snapshot(principal)
                    metrics.observe_authentication(protected_class,'accepted')
                except (SecurityError,UnicodeError):
                    metrics.observe_authentication(protected_class,'rejected')
                    if runtime is not None:
                        try:
                            runtime.authority.audit_authentication(False)
                        except SecurityError:
                            await respond(503,'Security service is unavailable.')
                            return
                    await respond(401,'Authentication required.',authenticate=True)
                    return
            if protected_class is not None and mode == 'static_bearer':
                if sum(k.lower()==b'authorization' for k,v in scope.get('headers',())) > 1:
                    await respond(401,'Authentication required.',authenticate=True)
                    return
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

            if protected_class is None or scope.get("method") not in {"POST", "PUT", "PATCH", "DELETE"}:
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
        except Exception as exc:
            from security.models import SecurityError
            if not isinstance(exc, SecurityError):
                raise
            # Final release can fail after endpoint execution or between chunks.
            scope['state'].pop('release_snapshot',None)
            if response_started:
                await send({'type':'http.response.body','body':b'', 'more_body':False})
            else:
                await respond(403,'Access denied.')
        finally:
            reset_request_id(context_token)
