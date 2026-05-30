from fastapi import FastAPI
from pydantic import BaseModel

from llm.ollama_client import OllamaClient
from rag.retriever import retrieve

from graph.langgraph_flow import app_graph

app = FastAPI(title="Local RAG API")

llm = OllamaClient(model="mistral")


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def health():
    return {
        "status": "running",
        "message": "LLM API is live 🚀"
    }


@app.post("/query")
def query(req: QueryRequest):

    result = app_graph.invoke(
        {
            "query": req.query
        }
    )

    return result
