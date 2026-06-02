from fastapi import FastAPI
from pydantic import BaseModel

from llm.ollama_client import OllamaClient
from rag.retriever import retrieve

from graph.langgraph_flow import app_graph
from memory.conversation_memory import get_history


# Initialize FastAPI app
app = FastAPI(title="Local RAG API")

# Initialize the Ollama client with the desired model
llm = OllamaClient(model="mistral")

# Define the request model for incoming queries
class QueryRequest(BaseModel):
    query: str

# Health check endpoint
@app.get("/")
def health():
    return {
        "status": "running",
        "message": "LLM API is live 🚀"
    }

# Endpoint to handle user queries
@app.post("/query")
def query(req: QueryRequest):

    result = app_graph.invoke(
        {
            "query": req.query
        }
    )

    return result

# Endpoint to retrieve conversation history
@app.get("/memory")
def memory():

    return {
        "history": get_history()
    }
