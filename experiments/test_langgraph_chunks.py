from rag.vectordb import collection

data = collection.get()

count = 0

for meta in data["metadatas"]:
    if meta["source"] == "LangGraph_Documentation.pdf":
        count += 1

print("Chunks:", count)
