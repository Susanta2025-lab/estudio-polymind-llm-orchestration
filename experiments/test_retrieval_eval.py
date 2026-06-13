from rag.hybrid_retriever import hybrid_retrieve
import json

with open("experiments/eval_dataset.json") as f:
    data = json.load(f)

hits = 0

for item in data:

    if item["expected_route"] != "rag":
        continue

    docs = hybrid_retrieve(item["query"])

    sources = [d["source"] for d in docs]

    print("\nQuery:", item["query"])
    print("Retrieved:", sources)

    expected_source = item.get("expected_source")

    if expected_source and expected_source in sources:
        hits += 1

score = hits / len([d for d in data if d["expected_route"] == "rag"])

print("\n======================")
print("Retrieval Recall:", score)
print("======================")
