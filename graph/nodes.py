from llm.ollama_client import OllamaClient
from rag.retriever import retrieve

llm = OllamaClient(model="mistral")

#router node
def router_node(state):

    query = state["query"].lower()

    if any(word in query for word in [
        "document",
        "pdf",
        "knowledge",
        "retrieve"
    ]):
        state["route"] = "rag"

    else:
        state["route"] = "direct"

    return state

#direct llm node
def direct_llm_node(state):

    answer = llm.generate(
        state["query"]
    )

    state["answer"] = answer

    return state

#rag node
def rag_node(state):

    docs = retrieve(state["query"])

    context = "\n".join([
        doc["text"]
        for doc in docs
    ])

    prompt = f"""
    Context:
    {context}

    Question:
    {state['query']}
    """

    answer = llm.generate(prompt)

    state["context"] = context
    state["answer"] = answer

    return state
