from graph.semantic_router import semantic_route


queries = [

    "What is LangGraph?",

    "Retrieve information about RAG",

    "What time is it?",

    "Calculate 45 * 78",

    "Tell me a joke",

    "Write a poem",

    "Search my documents",

    "Explain embeddings"
]


for query in queries:

    route = semantic_route(
        query
    )

    print(
        f"{query}"
    )

    print(
        f"→ {route}"
    )

    print("-" * 50)
