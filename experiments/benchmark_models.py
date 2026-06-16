import time
from pathlib import Path

import pandas as pd

from llm.ollama_client import OllamaClient


# =====================================================
# CONFIGURATION
# =====================================================

OUTPUT_FILE = (
    Path("results")
    / "benchmark_results.csv"
)

MODELS = [

    "phi3:mini",

    "gemma2:2b",

    "qwen2.5:3b",

    "mistral"

]


TEST_QUERIES = [

    {
        "task": "general",

        "query": "Tell me a joke"
    },

    {
        "task": "rag",

        "query": "What is LangGraph?"
    },

    {
        "task": "summarization",

        "query": (
            "Summarize retrieval "
            "augmented generation"
        )
    },

    {
        "task": "coding",

        "query": (
            "Write a Python function "
            "to compute factorial"
        )
    }

]


# =====================================================
# BENCHMARK
# =====================================================

results = []

print()

print("=" * 60)

print("MULTI-LLM BENCHMARK")

print("=" * 60)


for model in MODELS:

    print()

    print(f"Testing: {model}")

    print("-" * 60)

    llm = OllamaClient(
        model=model
    )

    for item in TEST_QUERIES:

        task = item["task"]

        query = item["query"]

        try:

            start = time.time()

            answer = llm.generate(
                query
            )

            latency = round(

                time.time() - start,

                3

            )

            word_count = len(

                answer.split()

            )

            char_count = len(

                answer

            )

            print()

            print(
                f"Task: {task}"
            )

            print(
                f"Latency: {latency} sec"
            )

            print(
                f"Words: {word_count}"
            )

            results.append(

                {

                    "model": model,

                    "task": task,

                    "query": query,

                    "latency_sec": latency,

                    "word_count": word_count,

                    "char_count": char_count

                }

            )

        except Exception as e:

            print()

            print(
                f"ERROR: {model}"
            )

            print(
                e
            )

            results.append(

                {

                    "model": model,

                    "task": task,

                    "query": query,

                    "latency_sec": None,

                    "word_count": None,

                    "char_count": None

                }

            )


# =====================================================
# SAVE RESULTS
# =====================================================

OUTPUT_FILE.parent.mkdir(

    exist_ok=True

)

df = pd.DataFrame(

    results

)

df.to_csv(

    OUTPUT_FILE,

    index=False

)


print()

print("=" * 60)

print("BENCHMARK COMPLETE")

print("=" * 60)

print()

print(df)

print()

print(
    f"Saved to: {OUTPUT_FILE}"
)
