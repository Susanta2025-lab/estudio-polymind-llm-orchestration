from rag.bm25 import bm25_search

results = bm25_search(
    "What is LangGraph?",
    top_k=10
)

for r in results:
    print(
        r["source"],
        r["chunk_id"],
        r["score"]
    )
