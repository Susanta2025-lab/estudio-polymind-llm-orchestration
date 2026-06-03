from fastapi import FastAPI
from pydantic import BaseModel
import time

from graph.langgraph_flow import app_graph

from memory.memory_store import (
    get_history
)

from utils.logger import log_request


app = FastAPI(
    title="Estudio PolyMind - Multi-LLM RAG & Orchestration Platform API",
    version="1.0.0"
)


class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"


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


@app.get("/memory/{session_id}")
def memory(session_id: str):

    return {
        "session_id": session_id,
        "history": get_history(session_id)
    }
