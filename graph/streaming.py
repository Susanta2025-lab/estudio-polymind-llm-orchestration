import logging
from typing import Callable, Dict, Iterator, Optional

from graph.generation import (
    direct_prompt,
    persist_exchange,
    public_sources,
    rag_prompt_and_sources,
    tool_answer,
)
from llm.inference import InferenceError, InferenceProvider
from llm.provider_factory import create_inference_provider
from llm.router import select_model_role

logger = logging.getLogger(__name__)


def stream_rag_response(
    query: str,
    session_id: str = "default",
    provider: Optional[InferenceProvider] = None,
    route_query: Optional[Callable[[str], str]] = None,
) -> Iterator[Dict]:
    """Run one request and yield structured events from that same execution."""
    route = "unknown"
    try:
        provider = provider or create_inference_provider()
        if route_query is None:
            from graph.semantic_router import semantic_route

            route_query = semantic_route
        route = route_query(query)
        role = select_model_role(query)
        model = provider.model_id(role)
        sources = []
        if route == "tool":
            answer = tool_answer(query)
            yield {
                "type": "metadata",
                "session_id": session_id,
                "route": route,
                "model_role": role.value,
                "model": model,
                "sources": sources,
            }
            yield {"type": "chunk", "content": answer}
        else:
            if route == "rag":
                prompt, _, documents = rag_prompt_and_sources(query, session_id)
                sources = public_sources(documents)
            else:
                prompt = direct_prompt(query, session_id)

            yield {
                "type": "metadata",
                "session_id": session_id,
                "route": route,
                "model_role": role.value,
                "model": model,
                "sources": sources,
            }
            chunks = []
            for chunk in provider.generate_stream(prompt, role):
                chunks.append(chunk)
                yield {"type": "chunk", "content": chunk}
            answer = "".join(chunks)

        persist_exchange(query, answer, session_id)
        yield {"type": "done", "response": answer}
    except InferenceError:
        logger.exception(
            "Inference failed for session=%s route=%s provider=%s",
            session_id,
            route,
            getattr(provider, "name", "unknown"),
        )
        yield {"type": "error", "message": "Inference service is unavailable."}
    except Exception:
        logger.exception("Streaming request failed for session=%s route=%s", session_id, route)
        yield {"type": "error", "message": "Request processing failed."}
