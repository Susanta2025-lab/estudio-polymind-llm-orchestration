from rag.vector_store_factory import get_vector_store

data = get_vector_store().list_documents()

count = 0

for item in data:
    meta = item.metadata
    if meta["source"] == "LangGraph_Documentation.pdf":
        count += 1

print("Chunks:", count)
