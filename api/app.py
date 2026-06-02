from fastapi import FastAPI
from pydantic import BaseModel

from graph.langgraph_flow import app_graph
from memory.conversation_memory import get_history

app = FastAPI(
    title="Estudio PolyMind - Multi-LLM RAG & Orchestration Platform API",
    version="1.0.0"
)


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def health():

    return {
        "status": "running",
        "project": "Estudio PolyMind - Multi-LLM RAG & Orchestration Platform 🚀",
        "version": "1.0.0",
        "description": "API for handling user queries with dynamic routing to multiple LLMs, RAG, and tools based on query content."
    }


@app.post("/query")
def query(req: QueryRequest):

    result = app_graph.invoke(
        {
            "query": req.query
        }
    )

    return result


@app.get("/memory")
def memory():

    return {
        "history": get_history()
    }
