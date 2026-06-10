from rag.retriever import retrieve

results = retrieve(
    "LangGraph"
)

for r in results:

    print()
    print(
        f"Source: {r['source']}"
    )
    print(
        f"Chunk: {r['chunk_id']}"
    )
    print(
        f"Score: {r['score']}"
    )
