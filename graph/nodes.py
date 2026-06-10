from llm.ollama_client import OllamaClient
from llm.router import select_model

from rag.hybrid_retriever import hybrid_retrieve

from tools.calculator import calculate
from tools.datetime_tool import current_time

from memory.memory_store import add_message

# This node routes the query to the appropriate processing path (direct LLM, RAG, or tool) based on simple keyword matching.
def router_node(state):

    query = state["query"].lower()

    if any(word in query for word in [
        "time",
        "calculate",
        "+",
        "-",
        "*",
        "/"
    ]):
        state["route"] = "tool"

    elif any(word in query for word in [
        "document",
        "pdf",
        "retrieve",
        "knowledge",
        "langgraph",
        "rag",
        "embedding",
        "vector",
        "chromadb",
        "agent",
        "memory"
    ]):
        state["route"] = "rag"

    else:
        state["route"] = "direct"

    return state

# This node selects the appropriate model based on the query content and adds it to the state.
def model_router_node(state):

    model = select_model(
        state["query"]
    )

    state["model"] = model

    return state

# This node handles direct LLM queries without retrieval, using the selected model.
def direct_llm_node(state):

    llm = OllamaClient(
        model=state["model"]
    )

    answer = llm.generate(
        state["query"]
    )

    add_message(
        "user",
        state["query"],
        state["session_id"]
    )

    add_message(
        "assistant",
        answer,
        state["session_id"]
    )

    state["answer"] = answer
    state["context"] = ""
    state["sources"] = []

    return state

# This node handles RAG-based queries, retrieving relevant documents and using them as context for the LLM.
def rag_node(state):

    llm = OllamaClient(
        model=state["model"]
    )

    docs = hybrid_retrieve(
        state["query"]
    )

    print("\n===== FINAL DOCS =====")

    for doc in docs:
        print(
            doc["source"],
            doc["chunk_id"],
            doc.get("rrf_score")
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
    {state['query']}
    """

    answer = llm.generate(
        prompt
    )

    add_message(
        "user",
        state["query"],
        state["session_id"]
    )

    add_message(
        "assistant",
        answer,
        state["session_id"]
    )

    state["context"] = context
    state["answer"] = answer
    state["sources"] = docs

    return state


# This node handles simple tool-based queries like time and calculations.
def tool_node(state):

    query = state["query"].lower()

    if "time" in query:

        answer = current_time()

    elif any(op in query for op in [
        "+",
        "-",
        "*",
        "/"
    ]):

        expression = (
            query
            .replace("calculate", "")
            .strip()
        )

        answer = calculate(
            expression
        )

    else:

        answer = "Tool unavailable."

    add_message(
        "user",
        state["query"],
        state["session_id"]
    )

    add_message(
        "assistant",
        answer,
        state["session_id"]
    )

    state["answer"] = answer
    state["context"] = ""
    state["sources"] = []

    return state
