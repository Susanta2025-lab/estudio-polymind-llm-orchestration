from llm.ollama_client import (
    OllamaClient
)

llm = OllamaClient(
    model="mistral"
)

for token in llm.generate_stream(
    "Explain LangGraph in one paragraph."
):

    print(
        token,
        end="",
        flush=True
    )
