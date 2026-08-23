from langgraph.graph import StateGraph

from graph.nodes import (
    create_direct_llm_node,
    create_model_router_node,
    create_rag_node,
    router_node,
    tool_node,
)
from graph.state import GraphState
from llm.inference import InferenceProvider
from llm.provider_factory import create_inference_provider


def create_app_graph(provider: InferenceProvider):
    builder = StateGraph(GraphState)
    builder.add_node("router", router_node)
    builder.add_node("model_router", create_model_router_node(provider))
    builder.add_node("direct", create_direct_llm_node(provider))
    builder.add_node("rag", create_rag_node(provider))
    builder.add_node("tool", tool_node)
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


inference_provider = create_inference_provider()
app_graph = create_app_graph(inference_provider)
