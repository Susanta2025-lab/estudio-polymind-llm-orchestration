from rag.hybrid_retriever import hybrid_retrieve

results = hybrid_retrieve(
    "LangGraph"
)

for r in results:

    print(
        r["source"],
        r["chunk_id"],
        r["rrf_score"]
    )
