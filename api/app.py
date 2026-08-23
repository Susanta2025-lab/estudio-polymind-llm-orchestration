import json
import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from graph.generation import public_sources
from graph.langgraph_flow import app_graph, inference_provider
from graph.streaming import stream_rag_response
from llm.inference import InferenceError
from memory.memory_store import get_history
from utils.logger import log_request

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Estudio PolyMind - API",
    version="1.0.0",
    description="A platform that orchestrates multiple LLMs and RAG techniques.",
)


class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"


@app.exception_handler(InferenceError)
async def inference_error_handler(_request: Request, exc: InferenceError):
    logger.exception("Inference request failed", exc_info=exc)
    return JSONResponse(status_code=502, content={"detail": "Inference service is unavailable."})


@app.get("/")
def health():
    return {
        "status": "running",
        "project": "Estudio PolyMind",
        "version": "1.0.0",
        "message": "Multi-LLM RAG & Orchestration Platform 🚀",
    }


@app.post("/query")
def query(req: QueryRequest):
    start_time = time.time()
    result = app_graph.invoke({"query": req.query, "session_id": req.session_id})
    log_request(
        query=req.query,
        route=result.get("route"),
        model=result.get("model"),
        session_id=req.session_id,
        start_time=start_time,
    )
    return {
        "query": req.query,
        "session_id": req.session_id,
        "route": result.get("route"),
        "model_role": result.get("model_role"),
        "model": result.get("model"),
        "response": result.get("answer"),
        "sources": public_sources(result.get("sources", [])),
    }


@app.post("/query/stream")
def query_stream(req: QueryRequest):
    def encode_events():
        start_time = time.time()
        metadata = {}
        for event in stream_rag_response(req.query, req.session_id, inference_provider):
            if event["type"] == "metadata":
                metadata = event
            elif event["type"] == "done":
                log_request(
                    query=req.query,
                    route=metadata.get("route"),
                    model=metadata.get("model"),
                    session_id=req.session_id,
                    start_time=start_time,
                )
            yield json.dumps(event, ensure_ascii=False) + "\n"

    return StreamingResponse(encode_events(), media_type="application/x-ndjson")


@app.get("/memory/{session_id}")
def memory(session_id: str):
    return {"session_id": session_id, "history": get_history(session_id)}
