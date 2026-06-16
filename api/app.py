from fastapi import FastAPI
from pydantic import BaseModel
import time

from graph.langgraph_flow import app_graph

from memory.memory_store import (
    get_history
)

from utils.logger import log_request

from fastapi.responses import StreamingResponse

from graph.streaming import stream_rag_response

from config.settings import settings



app = FastAPI(
    title="Estudio PolyMind - API",
    version="1.0.0",
    description="A platform that orchestrates multiple LLMs and RAG techniques to provide comprehensive and accurate responses. 🚀"
)


class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"


def stream_response(query):

    for token in stream_rag_response(
        query
    ):
        yield token

@app.get("/")
def health():

    return {
        "status": "running",

        "project": "Estudio PolyMind",

        "version": "1.0.0",

        "message": "Multi-LLM RAG & Orchestration Platform 🚀"
    }


@app.post("/query")
def query(req: QueryRequest):

    start_time = time.time()

    result = app_graph.invoke(
        {
            "query": req.query,
            "session_id": req.session_id
        }
    )

    log_request(
        query=req.query,
        route=result.get("route"),
        model=result.get("model"),
        session_id=req.session_id,
        start_time=start_time
    )

    return {
        "query": req.query,
        "session_id": req.session_id,
        "route": result.get("route"),
        "model": result.get("model"),
        "response": result.get("answer"),
        "sources": [
            {
                "source": doc.get("source"),
                "chunk_id": doc.get("chunk_id"),
                "score": doc.get("score")
            }
            for doc in result.get("sources", [])
        ]
    }

@app.post("/query/stream")
def query_stream(
    req: QueryRequest
):

    return StreamingResponse(
        stream_response(
            req.query
        ),
        media_type="text/plain"
    )


@app.get("/memory/{session_id}")
def memory(session_id: str):

    return {
        "session_id": session_id,
        "history": get_history(session_id)
    }
