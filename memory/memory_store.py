import json
import os
from datetime import datetime

MEMORY_FILE = "memory/chat_history.json"


def ensure_file():

    os.makedirs("memory", exist_ok=True)

    if not os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "w") as f:

            json.dump([], f)

def add_message(role, content, session_id="default"):

    ensure_file()

    with open(MEMORY_FILE, "r") as f:

        data = json.load(f)

    data.append({
        "session_id": session_id,
        "role": role,
        "content": content,
        "timestamp": str(datetime.now())
    })

    with open(MEMORY_FILE, "w") as f:

        json.dump(data, f, indent=2)


def get_history(session_id="default", limit=20):

    ensure_file()

    with open(MEMORY_FILE, "r") as f:

        data = json.load(f)

    filtered = [
        d for d in data
        if d["session_id"] == session_id
    ]

    return filtered[-limit:]


def clear_memory():

    with open(MEMORY_FILE, "w") as f:

        json.dump([], f)
