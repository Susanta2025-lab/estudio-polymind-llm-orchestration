from rag.hybrid_retriever import hybrid_retrieve
from rag.reranker import rerank


query = "What is LangGraph?"

docs = hybrid_retrieve(
    query
)

results = rerank(
    query,
    docs
)

for doc in results:

    print(
        doc["source"],
        doc["chunk_id"],
        round(
            doc["rerank_score"],
            3
        )
    )

    print("-" * 50)
