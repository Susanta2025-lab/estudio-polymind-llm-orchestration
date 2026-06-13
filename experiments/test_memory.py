from memory.memory_store import get_history

history = get_history(
    "default"
)

for msg in history[-10:]:

    print(
        msg["role"],
        ":",
        msg["content"]
    )
