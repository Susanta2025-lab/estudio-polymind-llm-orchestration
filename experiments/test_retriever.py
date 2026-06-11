from rag.retriever import retrieve

results = retrieve(
    "What is LangGraph?",
    n_results=10
)

for r in results:
    print(
        r["source"],
        r["chunk_id"],
        r["score"]
    )
