from memory.provider_factory import get_memory_store

history = get_memory_store().get_history(
    "default"
)

for msg in history[-10:]:

    print(
        msg["role"],
        ":",
        msg["content"]
    )
