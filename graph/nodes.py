from llm.ollama_client import OllamaClient
from llm.router import select_model

from rag.hybrid_retriever import hybrid_retrieve
from rag.reranker import rerank

from tools.calculator import calculate
from tools.datetime_tool import current_time
from graph.semantic_router import semantic_route

from memory.memory_store import add_message, get_history

# This node routes the query to the appropriate processing path (direct LLM, RAG, or tool) based on simple keyword matching.
def router_node(state):

    state["route"] = semantic_route(
        state["query"]
    )

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

    history = get_history(
        state["session_id"]
    )

    conversation = ""

    for msg in history[-6:]:

        conversation += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    prompt = f"""
    Conversation History:

    {conversation}

    User:
    {state["query"]}
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

    docs = rerank(
        state["query"],
        docs,
        top_k=3
    )

    print("\n===== FINAL DOCS =====")

    for doc in docs:
        print(
            doc["source"],
            doc["chunk_id"],
            round(
                doc["rerank_score"],
                3
            )
        )

    context = "\n\n".join(
    doc["text"]
    for doc in docs[:3]
)



    history = get_history(
        state["session_id"]
    )

    conversation = ""

    for msg in history[-6:]:

        conversation += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    prompt = f"""
    Conversation History:
    {conversation}

    Context:
    {context}

    Question:
    {state['query']}

    Answer using the context and
    conversation history.
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
