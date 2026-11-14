"""Explicit fixture-only FastAPI entrypoint; never imports the legacy provider factory."""
import os
import time
from contextlib import asynccontextmanager
from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response

from api.operator import operator_router, pilot_error
from api.security import ApplicationSecurityMiddleware
from documents.pilot.models import PilotError
from governance.ledger import GovernanceError
from llm.metrics import CONTENT_TYPE_LATEST, metrics
from security.models import SecurityError


def create_app(runtime, workflow, runner, *, run_worker=True):
    @asynccontextmanager
    async def lifespan(app):
        if run_worker:
            runner.start()
        try:
            yield
        finally:
            runner.close()
    app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)
    app.state.security_runtime = runtime
    app.state.operator_workflow = workflow
    app.state.operator_runner = runner
    app.add_middleware(ApplicationSecurityMiddleware,
        configuration=SimpleNamespace(authentication_mode="oidc_jwt", API_AUTH_ENABLED=False, MAX_REQUEST_BYTES=8192),
        runtime_getter=lambda: runtime)
    app.include_router(operator_router())
    app.add_exception_handler(PilotError, pilot_error)

    def error(request, status, category, detail):
        return JSONResponse(dict(detail=detail, category=category,
            request_id=getattr(request.state, "request_id", "")), status_code=status,
            headers={"Cache-Control": "no-store"})

    @app.exception_handler(SecurityError)
    async def denied(request, exc):
        return error(request, 503 if exc.category == "security_unavailable" else 403,
                     exc.category, "Access unavailable.")

    @app.exception_handler(GovernanceError)
    async def limits(request, exc):
        return error(request, 429, "admission_denied", "Admission denied.")

    @app.exception_handler(RequestValidationError)
    async def invalid(request, exc):
        return error(request, 422, "invalid_request", "Invalid request.")

    @app.exception_handler(Exception)
    async def unavailable(request, exc):
        return error(request, 503, "service_unavailable", "Document service unavailable.")

    @app.get("/health")
    def health():
        return {"status": "alive"}

    @app.get("/ready")
    def ready():
        try:
            p = workflow.pilot
            with p.control.transaction() as db:
                stopped = bool(p.control._config(db)["stopped"])
                uncertain = bool(db.execute("SELECT 1 FROM operations WHERE state IN ('ACTIVE','UNKNOWN')").fetchone())
                audit_full = db.execute("SELECT COUNT(*) FROM events").fetchone()[0] >= p.policy.audit_limit
            with p.governance.transaction() as db:
                uncertain |= bool(db.execute("SELECT 1 FROM reservations WHERE state NOT IN ('SETTLED','RELEASED')").fetchone())
            active = p.publication.authority.active()
            publication = active.generation is None or (
                active.generation in p._replicas and p._replicas[active.generation].ready())
            worker = runner.thread is not None and runner.thread.is_alive() and time.monotonic() - runner.heartbeat < 70
            ok = runtime.ready() and p.control.ready() and workflow.actions.ready() and publication and worker
            ok &= not (stopped or uncertain or audit_full or runner.outcome == "RECONCILIATION_REQUIRED")
            metrics.set_component_readiness("document_operator", ok)
            return JSONResponse(dict(status="ready" if ok else "unavailable", worker=runner.outcome,
                publication="idle" if active.generation is None else "current" if publication else "unavailable",
                stopped=stopped, unsettled=uncertain, audit_full=audit_full), status_code=200 if ok else 503)
        except Exception:
            metrics.set_component_readiness("document_operator", False)
            return JSONResponse({"status": "authority_unavailable"}, status_code=503)

    @app.get("/metrics")
    def prometheus():
        return Response(metrics.render(), headers={"Content-Type": CONTENT_TYPE_LATEST})

    @app.post("/documents/analyze")
    def analyze():
        return JSONResponse({"detail": "Use the authorized session question contract."}, status_code=503)

    @app.post("/query")
    @app.post("/query/stream")
    def legacy():
        raise SecurityError("unsupported_execution")
    return app


def configured_app():
    from development.document_demo.runtime import build
    root = os.environ["DOCUMENT_DEMO_ROOT"]
    # OS lock spans API + runner ownership. No second authority writer process.
    from filelock import FileLock
    lock = FileLock(root + "/runtime.lock", timeout=0)
    lock.acquire()
    try:
        runtime, workflow, runner, _ = build(root, deployment_env=os.environ.get("DEPLOYMENT_ENV", "local"))
        app = create_app(runtime, workflow, runner)
        app.state.process_lock = lock
        return app
    except BaseException:
        lock.release()
        raise
