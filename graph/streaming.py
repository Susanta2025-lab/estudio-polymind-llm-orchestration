from llm.ollama_client import OllamaClient
from llm.router import select_model

from rag.hybrid_retriever import hybrid_retrieve
from rag.reranker import rerank

from graph.semantic_router import semantic_route

from tools.datetime_tool import current_time
from tools.calculator import calculate


def stream_rag_response(query: str):

    route = semantic_route(query)

    # -----------------
    # TOOL ROUTE
    # -----------------

    if route == "tool":

        query_lower = query.lower()

        if "time" in query_lower:

            yield current_time()

            return

        elif any(
            op in query_lower
            for op in [
                "+",
                "-",
                "*",
                "/"
            ]
        ):

            expression = (
                query_lower
                .replace(
                    "calculate",
                    ""
                )
                .strip()
            )

            yield calculate(
                expression
            )

            return

        yield "Tool unavailable."

        return

    # -----------------
    # DIRECT ROUTE
    # -----------------

    model = select_model(
        query
    )

    llm = OllamaClient(
        model=model
    )

    if route == "direct":

        for token in llm.generate_stream(
            query
        ):

            yield token

        return

    # -----------------
    # RAG ROUTE
    # -----------------

    docs = hybrid_retrieve(
        query
    )

    docs = rerank(
        query,
        docs
    )

    context = "\n\n".join(

        doc["text"]

        for doc in docs[:3]

    )

    prompt = f"""
Answer the question using
the context below.

Context:

{context}

Question:

{query}
"""

    for token in llm.generate_stream(
        prompt
    ):

        yield token
