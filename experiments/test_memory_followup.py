import requests

URL = "http://127.0.0.1:8001/query"

session = "memory_test"

queries = [

    "What is LangGraph?",

    "What are its main concepts?"
]

for q in queries:

    r = requests.post(
        URL,
        json={
            "query": q,
            "session_id": session
        }
    )

    print()
    print("Query:", q)
    print(
        r.json()["response"]
    )
