from rag.bm25 import bm25_search

results = bm25_search(
    "LangGraph"
)

for r in results:

    print(r["source"])
    print(r["score"])
    print("-" * 50)
