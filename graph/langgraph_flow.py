from langgraph.graph import StateGraph
from graph.state import GraphState

from graph.nodes import router_node, model_router_node, direct_llm_node, rag_node, tool_node

# Initialize the graph builder
builder = StateGraph(GraphState)

# Add nodes to the graph
builder.add_node("router", router_node)
builder.add_node("model_router", model_router_node)
builder.add_node("direct", direct_llm_node)
builder.add_node("rag", rag_node)
builder.add_node("tool", tool_node)



#define routing logic
def route_decision(state):

    return state["route"]


builder.add_edge(
    "router",
    "model_router"
)

#Conditional edges based on routing logic
builder.add_conditional_edges(
    "model_router",
    route_decision,
    {
        "rag": "rag",
        "direct": "direct",
        "tool": "tool"
    }
)

#build entry
builder.set_entry_point("router")

#finish points
builder.set_finish_point("direct")
builder.set_finish_point("rag")
builder.set_finish_point("tool")

#compile
app_graph = builder.compile()
