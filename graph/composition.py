"""Graph factory without process-global provider or memory initialization."""
from langgraph.graph import StateGraph

from graph.nodes import (
    create_direct_llm_node,
    create_model_router_node,
    create_rag_node,
    router_node,
    create_tool_node,
)
from graph.state import GraphState
from llm.inference import InferenceProvider
from memory.memory_store import ConversationMemoryStore
from memory.provider_factory import get_memory_store


def create_app_graph(provider: InferenceProvider, memory_store: ConversationMemoryStore = None, *, execution=None):
    memory_store = memory_store or get_memory_store()
    builder = StateGraph(GraphState)
    def scoped_router(state):
        state['route'] = execution.route(state)
        return state
    builder.add_node("router", router_node if execution is None else scoped_router)
    builder.add_node("model_router", create_model_router_node(provider))
    builder.add_node("direct", create_direct_llm_node(provider, memory_store, **({} if execution is None else {"execution": execution})))
    builder.add_node("rag", create_rag_node(provider, memory_store, **({} if execution is None else {"execution": execution})))
    builder.add_node("tool", create_tool_node(memory_store, **({} if execution is None else {"execution": execution})))
    builder.add_edge("router", "model_router")
    builder.add_conditional_edges(
        "model_router",
        lambda state: state["route"],
        {"rag": "rag", "direct": "direct", "tool": "tool"},
    )
    builder.set_entry_point("router")
    builder.set_finish_point("direct")
    builder.set_finish_point("rag")
    builder.set_finish_point("tool")
    return builder.compile()
