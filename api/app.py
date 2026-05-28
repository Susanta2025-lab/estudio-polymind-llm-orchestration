from fastapi import FastAPI
from pydantic import BaseModel

from llm.ollama_client import OllamaClient
from rag.retriever import retrieve

app = FastAPI(title="Local RAG API")

llm = OllamaClient(model="mistral")


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def health():
    return {"status": "running", "message": "LLM API is live 🚀"}


class QueryRequest(BaseModel):
    query: str


@app.post("/query")
def query(req: QueryRequest):

    context_docs = retrieve(req.query)

    context = "\n".join(context_docs)

    prompt = f"""
    Answer the question using the context below.

    Context:
    {context}

    User Question:
    {req.query}
    """

    answer = llm.generate(prompt)

    return {
        "query": req.query,
        "retrieved_context": context_docs,
        "response": answer
    }
