from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# =====================================================
# CONFIGURATION
# =====================================================

RESULTS = (
    Path("results")
    / "benchmark_results.csv"
)

LATENCY_PLOT = (
    Path("results")
    / "benchmark_latency.png"
)

WORDS_PLOT = (
    Path("results")
    / "benchmark_words.png"
)


# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    RESULTS
)


# =====================================================
# LATENCY CHART
# =====================================================

pivot_latency = df.pivot(

    index="task",

    columns="model",

    values="latency_sec"

)

plt.figure(
    figsize=(10, 6)
)

pivot_latency.plot(
    kind="bar"
)

plt.title(
    "Model Latency Benchmark"
)

plt.ylabel(
    "Seconds"
)

plt.xlabel(
    "Task"
)

plt.xticks(
    rotation=0
)

plt.tight_layout()

plt.savefig(
    LATENCY_PLOT
)

plt.close()


# =====================================================
# WORD COUNT CHART
# =====================================================

pivot_words = df.pivot(

    index="task",

    columns="model",

    values="word_count"

)

plt.figure(
    figsize=(10, 6)
)

pivot_words.plot(
    kind="bar"
)

plt.title(
    "Response Length Benchmark"
)

plt.ylabel(
    "Words"
)

plt.xlabel(
    "Task"
)

plt.xticks(
    rotation=0
)

plt.tight_layout()

plt.savefig(
    WORDS_PLOT
)

plt.close()


# =====================================================
# SUMMARY
# =====================================================

print()

print("=" * 60)

print(
    "BENCHMARK VISUALIZATION COMPLETE"
)

print("=" * 60)

print()

print(
    f"Saved: {LATENCY_PLOT}"
)

print(
    f"Saved: {WORDS_PLOT}"
)
