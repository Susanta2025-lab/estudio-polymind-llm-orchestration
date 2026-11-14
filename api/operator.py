"""Strict private operator contracts; no paths, scopes or authority supplied by clients."""
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

from documents.pilot.models import PilotError
from security.models import SecurityError


class StrictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class CreateSession(StrictRequest):
    source_approval_id: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_./:-]+$")
    request_key: str = Field(min_length=16, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")


class PublishSession(StrictRequest):
    expected_job_id: str = Field(pattern=r"^[0-9a-f-]{36}$")

    @field_validator("expected_job_id")
    @classmethod
    def canonical_job_id(cls, value):
        return str(UUID(value))


class Question(StrictRequest):
    query: str = Field(min_length=1, max_length=4096)
    request_key: str = Field(min_length=16, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")


class CloseSession(StrictRequest):
    withdrawal: bool


class EmptyAction(StrictRequest):
    pass


def operator_router():
    router = APIRouter(prefix="/documents/operator")

    def service(request):
        p = getattr(request.state, "principal", None)
        w = getattr(request.app.state, "operator_workflow", None)
        if p is None:
            raise SecurityError("authentication_required")
        if w is None:
            raise SecurityError("security_unavailable")
        w.operator(p)
        return w, p

    def deliver(request, execute, session=None, *, active=False, status=200):
        w, p = service(request)
        before = w.release_guard(p, session, active=active)
        result = execute(w, p)
        with before():
            pass
        request.state.release_guard = w.release_guard(p, session, active=active)
        return JSONResponse(result, status_code=status, headers={"Cache-Control": "no-store"})

    @router.get("/context")
    def context(request: Request):
        return deliver(request, lambda w, p: w.context(p))

    @router.get("/sources")
    def sources(request: Request):
        return deliver(request, lambda w, p: w.sources(p))

    @router.post("/sessions")
    def create(body: CreateSession, request: Request):
        w, p = service(request)
        result, replay = w.create(p, body.source_approval_id, body.request_key)
        request.state.release_guard = w.release_guard(p, UUID(result["session_id"]), active=True)
        return JSONResponse(result, status_code=200 if replay else 201, headers={"Cache-Control": "no-store"})

    @router.post("/sessions/{session_id}/start", status_code=202)
    def start(session_id: UUID, request: Request, body: EmptyAction | None = None):
        def execute(w, p):
            result = w.start(p, session_id)
            request.app.state.operator_runner.authorize(p, session_id)
            return result
        return deliver(request, execute, session_id, active=True, status=202)

    @router.get("/sessions/{session_id}")
    def status(session_id: UUID, request: Request):
        def read(w, p):
            result = w.status(p, session_id)
            result["worker"] = request.app.state.operator_runner.outcome
            return result
        return deliver(request, read, session_id)

    @router.post("/sessions/{session_id}/publish")
    def publish(session_id: UUID, body: PublishSession, request: Request):
        return deliver(request, lambda w, p: w.publish(p, session_id, UUID(body.expected_job_id)), session_id, active=True)

    @router.get("/sessions/{session_id}/digest")
    def digest(session_id: UUID, request: Request):
        return deliver(request, lambda w, p: w.digest(p, session_id), session_id, active=True)

    @router.post("/sessions/{session_id}/questions")
    def question(session_id: UUID, body: Question, request: Request):
        return deliver(request, lambda w, p: w.question(p, session_id, body.query, body.request_key), session_id, active=True)

    @router.post("/sessions/{session_id}/cancel")
    def cancel(session_id: UUID, request: Request, body: EmptyAction | None = None):
        return deliver(request, lambda w, p: w.cancel(p, session_id), session_id, status=202)

    @router.post("/sessions/{session_id}/close")
    def close(session_id: UUID, body: CloseSession, request: Request):
        w, p = service(request)
        result = w.close(p, session_id, body.withdrawal)
        request.state.release_guard = w.release_guard(p, session_id)
        return JSONResponse(result, headers={"Cache-Control": "no-store"})

    @router.post("/stop")
    def stop(request: Request, body: EmptyAction | None = None):
        w, p = service(request)
        result = w.stop(p)
        request.state.release_guard = w.release_guard(p)
        return JSONResponse(result, headers={"Cache-Control": "no-store"})

    return router


async def pilot_error(request, exc: PilotError):
    category = exc.category
    code = {"pilot_denied": 409, "pilot_stopped": 403, "pilot_limit": 429,
            "pilot_source_refused": 422, "pilot_not_ready": 503,
            "pilot_reconciliation_required": 409}[category]
    return JSONResponse({"detail": "Document action unavailable.", "category": category,
                         "request_id": getattr(request.state, "request_id", "")}, status_code=code)
