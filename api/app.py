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
    return {
        "status": "running",
        "message": "LLM API is live 🚀"
    }


@app.post("/query")
def query(req: QueryRequest):

    # Retrieve relevant chunks with metadata
    context_docs = retrieve(req.query)

    # Combine retrieved text into context
    context = "\n".join([
        doc["text"]
        for doc in context_docs
    ])

    # Prompt template
    prompt = f"""
    Answer the question using the context below.

    Context:
    {context}

    User Question:
    {req.query}
    """

    # Generate response from LLM
    answer = llm.generate(prompt)

    return {
        "query": req.query,
        "sources": context_docs,
        "response": answer
    }
