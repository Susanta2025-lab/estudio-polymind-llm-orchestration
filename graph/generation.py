from typing import Callable, Dict, List, Tuple

from config.settings import settings
from memory.memory_store import ConversationMemoryStore
from memory.provider_factory import get_memory_store
from prompts.direct_prompt import build_direct_prompt
from prompts.rag_prompt import build_rag_prompt
from tools.calculator import calculate
from tools.datetime_tool import current_time


def conversation_history(session_id: str, memory_store: ConversationMemoryStore = None, *, execution=None) -> str:
    _legacy_only(execution)
    store = memory_store or get_memory_store()
    history = store.get_history(session_id)
    return "".join(
        f"{message['role']}: {message['content']}\n"
        for message in history[-settings.MEMORY_HISTORY :]
    )


def direct_prompt(query: str, session_id: str, memory_store: ConversationMemoryStore = None, *, execution=None) -> str:
    return build_direct_prompt(conversation_history(session_id, memory_store, **({} if execution is None else {"execution": execution})), query)


def rag_prompt_and_sources(
    query: str,
    session_id: str,
    retrieve: Callable = None,
    rerank_documents: Callable = None,
    memory_store: ConversationMemoryStore = None,
    execution=None,
) -> Tuple[str, str, List[Dict]]:
    _legacy_only(execution)
    if execution is not None:
        retrieve = execution.retrieve
        rerank_documents = lambda q, docs, top_k: docs[:top_k]
    if retrieve is None:
        from rag.hybrid_retriever import hybrid_retrieve

        retrieve = hybrid_retrieve
    if rerank_documents is None:
        from rag.reranker import rerank

        rerank_documents = rerank
    documents = retrieve(query)
    documents = rerank_documents(query, documents, top_k=settings.RERANK_TOP_K)
    context = "\n\n".join(document["text"] for document in documents[:3])
    prompt = build_rag_prompt(conversation_history(session_id, memory_store, **({} if execution is None else {"execution": execution})), context, query)
    return prompt, context, documents


def tool_answer(query: str) -> str:
    normalized = query.lower()
    if "time" in normalized:
        return current_time()
    if any(operator in normalized for operator in ("+", "-", "*", "/")):
        return calculate(normalized.replace("calculate", "").strip())
    return "Tool unavailable."


def persist_exchange(query: str, answer: str, session_id: str, memory_store: ConversationMemoryStore = None, *, execution=None) -> None:
    _legacy_only(execution)
    (memory_store or get_memory_store()).append_exchange(session_id, query, answer)


def _legacy_only(execution=None):
    if execution is not None:
        from security.chat import ChatContext
        if type(execution) is not ChatContext:
            from security.models import SecurityError
            raise SecurityError()
        execution.check()
        return
    if settings.authentication_mode == 'oidc_jwt':
        from security.models import SecurityError
        raise SecurityError('unsupported_execution')


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
