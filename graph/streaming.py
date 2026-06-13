from llm.ollama_client import OllamaClient
from llm.router import select_model

from rag.hybrid_retriever import hybrid_retrieve
from rag.reranker import rerank


def stream_rag_response(query: str):

    model = select_model(query)

    docs = hybrid_retrieve(query)

    docs = rerank(
        query,
        docs
    )

    context = "\n\n".join(
        doc["text"]
        for doc in docs[:3]
    )

    prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{query}
"""

    llm = OllamaClient(
        model=model
    )

    for token in llm.generate_stream(
        prompt
    ):
        yield token
