from graph.semantic_router import semantic_route
import json

with open("experiments/eval_dataset.json") as f:
    data = json.load(f)

correct = 0

for item in data:

    pred = semantic_route(item["query"])

    expected = item["expected_route"]

    print("\nQuery:", item["query"])
    print("Pred:", pred)
    print("Expected:", expected)

    if pred == expected:
        correct += 1

accuracy = correct / len(data)

print("\n======================")
print("Router Accuracy:", accuracy)
print("======================")
