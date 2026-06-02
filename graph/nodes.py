from llm.ollama_client import OllamaClient

from rag.retriever import retrieve

from tools.calculator import calculate
from tools.datetime_tool import current_time

from memory.conversation_memory import add_message


llm = OllamaClient(model="mistral")


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
        "knowledge"
    ]):
        state["route"] = "rag"

    else:
        state["route"] = "direct"

    return state


def direct_llm_node(state):

    answer = llm.generate(
        state["query"]
    )

    add_message(
        "user",
        state["query"]
    )

    add_message(
        "assistant",
        answer
    )

    state["answer"] = answer

    state["context"] = ""

    state["sources"] = []

    return state


def rag_node(state):

    docs = retrieve(
        state["query"]
    )

    context = "\n".join(
        doc["text"]
        for doc in docs
    )

    prompt = f"""
    Answer the question using the context below.

    Context:
    {context}

    Question:
    {state['query']}
    """

    answer = llm.generate(prompt)

    add_message(
        "user",
        state["query"]
    )

    add_message(
        "assistant",
        answer
    )

    state["context"] = context

    state["answer"] = answer

    state["sources"] = docs

    return state


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

        answer = calculate(expression)

    else:

        answer = "Tool unavailable."

    add_message(
        "user",
        state["query"]
    )

    add_message(
        "assistant",
        answer
    )

    state["answer"] = answer

    state["context"] = ""

    state["sources"] = []

    return state
