import json
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Path, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from pydantic import BaseModel, Field

from graph.generation import public_sources
from graph.langgraph_flow import app_graph, inference_provider, memory_store
from graph.streaming import stream_rag_response
from llm.inference import InferenceError
from llm.metrics import CONTENT_TYPE_LATEST, metrics
from llm.operational import (
    application_status,
    normalize_request_id,
    request_id,
    reset_request_id,
    set_request_id,
)
from memory.memory_store import MemoryError
from memory.provider_factory import close_memory_store
from utils.logger import log_request

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    close_memory_store()

app = FastAPI(
    title="Estudio PolyMind - API",
    version="1.0.0",
    description="A platform that orchestrates multiple LLMs and RAG techniques.",
    lifespan=lifespan,
)


class QueryRequest(BaseModel):
    query: str
    session_id: str = Field(default="default", min_length=1, max_length=256)


@app.middleware("http")
async def request_correlation(request: Request, call_next):
    correlation_id = normalize_request_id(request.headers.get("X-Request-ID"))
    token = set_request_id(correlation_id)
    request.state.request_id = correlation_id
    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = correlation_id
        return response
    finally:
        reset_request_id(token)


@app.exception_handler(InferenceError)
async def inference_error_handler(_request: Request, exc: InferenceError):
    logger.warning(
        "Inference request failed request_id=%s category=%s",
        _request.state.request_id,
        exc.category,
    )
    return JSONResponse(
        status_code=application_status(exc),
        content={"detail": "Inference service is unavailable."},
    )


@app.exception_handler(MemoryError)
async def memory_error_handler(request: Request, exc: MemoryError):
    logger.warning("Memory request failed request_id=%s category=%s", request.state.request_id, exc.category)
    return JSONResponse(status_code=503, content={"detail": "Conversation memory is unavailable."})


@app.get("/")
def health():
    return {
        "status": "running",
        "project": "Estudio PolyMind",
        "version": "1.0.0",
        "message": "Multi-LLM RAG & Orchestration Platform 🚀",
    }


@app.get("/health")
def liveness():
    return {"status": "alive"}


@app.get("/ready")
def readiness():
    started = time.perf_counter()
    result = inference_provider.check_readiness()
    memory_result = memory_store.check_readiness()
    duration = time.perf_counter() - started
    metrics.observe_readiness(result, duration)
    logger.info(
        "Readiness probe request_id=%s inference_provider=%s inference_outcome=%s memory_provider=%s memory_outcome=%s",
        request_id(),
        result.provider,
        result.status.value,
        memory_result.provider,
        memory_result.status,
    )
    ready = result.ready and memory_result.ready
    overall_status = "ready" if ready else (result.status.value if not result.ready else memory_result.status)
    content = {
        "status": overall_status,
        "provider": result.provider,
        "inference": {"status": result.status.value, "provider": result.provider},
        "memory": {"status": memory_result.status, "provider": memory_result.provider},
        "models": dict(result.models),
    }
    return JSONResponse(status_code=200 if ready else 503, content=content)


@app.get("/metrics", include_in_schema=False)
def application_metrics():
    return Response(content=metrics.render(), headers={"Content-Type": CONTENT_TYPE_LATEST})


@app.post("/query")
def query(req: QueryRequest):
    started = time.perf_counter()
    route = "unknown"
    outcome = "error"
    try:
        result = app_graph.invoke({"query": req.query, "session_id": req.session_id})
        route = result.get("route") or "unknown"
        response = {
            "query": req.query,
            "session_id": req.session_id,
            "route": result.get("route"),
            "model_role": result.get("model_role"),
            "model": result.get("model"),
            "response": result.get("answer"),
            "sources": public_sources(result.get("sources", [])),
        }
        outcome = "success"
        return response
    finally:
        duration = time.perf_counter() - started
        metrics.observe_application(route, "query", outcome, duration)
        log_request(route=route, operation="query", outcome=outcome, duration=duration)


@app.post("/query/stream")
def query_stream(req: QueryRequest):
    correlation_id = request_id()

    def encode_events():
        token = set_request_id(correlation_id)
        started = time.perf_counter()
        metadata = {}
        outcome = "error"
        try:
            for event in stream_rag_response(req.query, req.session_id, inference_provider, memory_store=memory_store):
                if event["type"] == "metadata":
                    metadata = event
                elif event["type"] == "done":
                    outcome = "success"
                yield json.dumps(event, ensure_ascii=False) + "\n"
        finally:
            route = metadata.get("route") or "unknown"
            duration = time.perf_counter() - started
            metrics.observe_application(route, "stream", outcome, duration)
            log_request(route=route, operation="stream", outcome=outcome, duration=duration)
            reset_request_id(token)

    return StreamingResponse(encode_events(), media_type="application/x-ndjson")


@app.get("/memory/{session_id}")
def memory(session_id: str = Path(min_length=1, max_length=256)):
    return {"session_id": session_id, "history": memory_store.get_history(session_id)}
