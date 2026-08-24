from typing import Callable

from graph.generation import direct_prompt, persist_exchange, rag_prompt_and_sources, tool_answer
from graph.semantic_router import semantic_route
from llm.inference import InferenceProvider, ModelRole
from llm.router import select_model_role
from memory.memory_store import ConversationMemoryStore


def router_node(state):
    state["route"] = semantic_route(state["query"])
    return state


def create_model_router_node(provider: InferenceProvider) -> Callable:
    def model_router_node(state):
        role = select_model_role(state["query"])
        state["model_role"] = role.value
        state["model"] = provider.model_id(role)
        return state

    return model_router_node


def create_direct_llm_node(provider: InferenceProvider, memory_store: ConversationMemoryStore) -> Callable:
    def direct_llm_node(state):
        role = ModelRole(state["model_role"])
        answer = provider.generate(direct_prompt(state["query"], state["session_id"], memory_store), role)
        persist_exchange(state["query"], answer, state["session_id"], memory_store)
        state.update(answer=answer, context="", sources=[])
        return state

    return direct_llm_node


def create_rag_node(provider: InferenceProvider, memory_store: ConversationMemoryStore) -> Callable:
    def rag_node(state):
        prompt, context, documents = rag_prompt_and_sources(state["query"], state["session_id"], memory_store=memory_store)
        answer = provider.generate(prompt, ModelRole(state["model_role"]))
        persist_exchange(state["query"], answer, state["session_id"], memory_store)
        state.update(context=context, answer=answer, sources=documents)
        return state

    return rag_node


def create_tool_node(memory_store: ConversationMemoryStore) -> Callable:
    def tool_node(state):
        answer = tool_answer(state["query"])
        persist_exchange(state["query"], answer, state["session_id"], memory_store)
        state.update(answer=answer, context="", sources=[])
        return state
    return tool_node
