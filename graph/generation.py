from typing import Callable, Dict, List, Tuple

from config.settings import settings
from memory.memory_store import add_message, get_history
from prompts.direct_prompt import build_direct_prompt
from prompts.rag_prompt import build_rag_prompt
from tools.calculator import calculate
from tools.datetime_tool import current_time


def conversation_history(session_id: str) -> str:
    history = get_history(session_id)
    return "".join(
        f"{message['role']}: {message['content']}\n"
        for message in history[-settings.MEMORY_HISTORY :]
    )


def direct_prompt(query: str, session_id: str) -> str:
    return build_direct_prompt(conversation_history(session_id), query)


def rag_prompt_and_sources(
    query: str,
    session_id: str,
    retrieve: Callable = None,
    rerank_documents: Callable = None,
) -> Tuple[str, str, List[Dict]]:
    if retrieve is None:
        from rag.hybrid_retriever import hybrid_retrieve

        retrieve = hybrid_retrieve
    if rerank_documents is None:
        from rag.reranker import rerank

        rerank_documents = rerank
    documents = retrieve(query)
    documents = rerank_documents(query, documents, top_k=settings.RERANK_TOP_K)
    context = "\n\n".join(document["text"] for document in documents[:3])
    prompt = build_rag_prompt(conversation_history(session_id), context, query)
    return prompt, context, documents


def tool_answer(query: str) -> str:
    normalized = query.lower()
    if "time" in normalized:
        return current_time()
    if any(operator in normalized for operator in ("+", "-", "*", "/")):
        return calculate(normalized.replace("calculate", "").strip())
    return "Tool unavailable."


def persist_exchange(query: str, answer: str, session_id: str) -> None:
    add_message("user", query, session_id)
    add_message("assistant", answer, session_id)


def public_sources(documents: List[Dict]) -> List[Dict]:
    return [
        {
            "source": document.get("source"),
            "chunk_id": document.get("chunk_id"),
            "score": document.get("score"),
            "rerank_score": document.get("rerank_score"),
        }
        for document in documents
    ]
