# 🧠 Estudio PolyMind

### Multi-LLM RAG & Agent Orchestration Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)]()
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-orange.svg)]()
[![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-purple.svg)]()
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLMs-black.svg)]()
[![CI](https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/workflows/ci.yml/badge.svg)]()

A production-style AI Engineering platform that combines **Multi-LLM orchestration**, **Retrieval-Augmented Generation (RAG)**, **semantic routing**, **hybrid retrieval**, **cross-encoder reranking**, **conversation memory**, and provider-neutral LLM inference using Ollama or an external OpenAI-compatible service.

Built to demonstrate modern AI Engineering practices including:

- Multi-LLM orchestration
- Retrieval pipelines
- Semantic search
- Agent workflows
- Model routing
- Local-first deployment

---

# 🎯 System Overview

Estudio PolyMind orchestrates LLMs through LangGraph workflows and a
provider-neutral inference contract. The current adapters are Ollama and an
OpenAI-compatible HTTP adapter intended for a separately deployed vLLM server.

```text
User Query

↓

Semantic Router

↓

Model Router

↓

RAG / Tool / Direct LLM

↓

Conversation Memory

↓

Inference Provider Contract

↓

Ollama or OpenAI-Compatible Adapter

↓

Selected Served Model

↓

Final Response
```

Core capabilities:

- Multi-LLM orchestration
- Semantic query routing
- Hybrid retrieval
- Cross-encoder reranking
- Persistent conversation memory
- Local or separately hosted AI inference

---

# 🚀 Key Features

## Multi-LLM Orchestration

Supports logical model routing independently of the selected inference provider.
The default Ollama mapping uses:

- Mistral
- Qwen 2.5
- Gemma 2
- Phi-3 Mini

Dynamic model selection:

| Task | Model |
|------|------|
| General reasoning | Mistral |
| Coding | Qwen 2.5 |
| Summarization | Gemma 2 |
| Fast responses | Phi-3 Mini |

Application routing uses logical roles (`general`, `coding`, `summarization`, and
`fast`). Each adapter owns an independent mapping from those roles to its served
model identifiers, so LangGraph nodes do not depend on Ollama tags, vLLM model IDs,
or provider HTTP details. Multiple roles may intentionally map to one served model.

---

## Semantic Query Routing

Uses Sentence Transformers embeddings and cosine similarity for semantic intent classification.

Routes queries into:

- RAG Pipeline
- Tool Execution
- Direct LLM Response

Example:

| Query | Route |
|------|------|
| What is LangGraph? | RAG |
| What time is it? | Tool |
| Tell me a joke | Direct |

---

## Advanced RAG Pipeline

### Document Ingestion

Supports:

- PDF documents
- Text files

### Chunking

Documents are split into semantic chunks before indexing.

### Embeddings

```text
sentence-transformers/all-MiniLM-L6-v2
```

### Vector Database

```text
ChromaDB
```

---

## Hybrid Retrieval

Combines:

### Dense Retrieval

- Semantic embeddings
- ChromaDB similarity search

### Sparse Retrieval

- BM25 keyword retrieval

### Fusion

Uses:

```text
Reciprocal Rank Fusion (RRF)
```

to combine dense and sparse rankings.

---

## Cross-Encoder Reranking

Retrieved documents are reranked using:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

Benefits:

- Better relevance ranking
- Improved context quality
- Reduced retrieval noise

---

## Conversational Memory

Persistent session-based memory:

- User history tracking
- Context-aware conversations
- Session persistence

Storage:

```text
memory/chat_history.json
```

---

## Tool Calling

Integrated utility tools.

### Calculator

```text
Calculate 45 * 78
```

### Current Time

```text
What time is it?
```

---

## FastAPI Backend

REST API for:

- Query processing
- Memory retrieval
- Multi-LLM orchestration
- RAG execution

`POST /query` provides a non-streaming response. `POST /query/stream` provides one
newline-delimited JSON (`application/x-ndjson`) event stream for each request:

- `metadata`: session ID, route, logical model role, served model, and sources
- `chunk`: generated text
- `done`: the completed answer
- `error`: a sanitized failure message

The Streamlit UI uses only the streaming endpoint for a prompt, avoiding duplicate
orchestration and inference runs. Both paths use the same prompt construction,
retrieval, routing, session-history, and successful memory-persistence semantics.

Swagger documentation:

```text
http://localhost:8001/docs
```

---

## Streamlit Interface

Interactive chat interface featuring:

- Chat history
- Source attribution
- Route visualization
- Model visualization
- Session management

---

# 🏗️ System Architecture

```text
                    User Query
                         │
                         ▼
                Semantic Router
          (RAG / Tool / Direct LLM)
                         │
                         ▼
                  Model Router
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
      RAG             Tool Node      Direct LLM
        │
        ▼
 ┌─────────────────┐
 │ Dense Retrieval │
 │   (ChromaDB)    │
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │ BM25 Retrieval  │
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │  RRF Fusion     │
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │ Cross Encoder   │
 │   Reranker      │
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │ Conversation    │
 │ Memory Context  │
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │ Inference       │
 │ Provider        │
 └────────┬────────┘
          │
          ▼
       ┌───────────────┴───────────────┐
       ▼                               ▼
┌─────────────────┐          ┌─────────────────────┐
│ Ollama Adapter  │          │ OpenAI-Compatible   │
│                 │          │ Adapter             │
└────────┬────────┘          └──────────┬──────────┘
         │                              │
         ▼                              ▼
 Local Ollama runtime          External vLLM service
         │                              │
         └───────────────┬──────────────┘
                         ▼
                    Final Answer
```

The OpenAI-compatible path is a control-plane/data-plane boundary: PolyMind owns
routing, RAG, tools, memory, and its application API, while vLLM runs separately
and is contacted over the network. This repository does not bundle or install
vLLM, download `gpt-oss-20b`, or configure GPU infrastructure.

## Inference Configuration

Defaults preserve local Ollama operation. Set `INFERENCE_PROVIDER` explicitly to
select the external adapter; invalid values fail during settings initialization and
there is no automatic fallback. Pydantic validates positive timeout values and all
logical roles for the selected provider.

| Environment variable | Default | Purpose |
|---|---|---|
| `INFERENCE_PROVIDER` | `ollama` | `ollama` or `openai_compatible` |
| `OLLAMA_URL` | `http://localhost:11434/api/chat` | Ollama chat endpoint |
| `INFERENCE_CONNECT_TIMEOUT` | `5` | HTTP connection timeout in seconds |
| `INFERENCE_READ_TIMEOUT` | `120` | HTTP read/inactivity timeout in seconds, including streaming reads |
| `OLLAMA_MODEL_MAP` | built-in role mapping | JSON object mapping logical roles to Ollama model tags |
| `OPENAI_COMPATIBLE_BASE_URL` | `http://localhost:8000/v1` | Base URL whose `/chat/completions` endpoint implements the OpenAI-compatible protocol |
| `OPENAI_COMPATIBLE_API_KEY` | unset | Optional Bearer credential; no authorization header is sent when unset or blank |
| `OPENAI_COMPATIBLE_CONNECT_TIMEOUT` | `5` | External provider connection timeout in seconds |
| `OPENAI_COMPATIBLE_READ_TIMEOUT` | `120` | External provider read/inactivity timeout in seconds, including SSE reads |
| `OPENAI_COMPATIBLE_MODEL_MAP` | all roles map to `gpt-oss-20b` | JSON object mapping logical roles to server-visible model IDs; this is configuration only, not a deployment claim |
| `OPENAI_COMPATIBLE_GENERATION_PARAMETERS` | `{}` | Optional JSON object of chat generation parameters such as `temperature`; `model`, `messages`, and `stream` are reserved |
| `PROVIDER_READINESS_TIMEOUT` | `3` | Timeout in seconds for lightweight provider discovery probes |
| `PROVIDER_READINESS_RETRIES` | `1` | Additional attempts for transient readiness failures (maximum 5) |
| `PROVIDER_READINESS_BACKOFF` | `0.1` | Linear readiness retry backoff in seconds (maximum 5) |

Example model-map override:

```bash
export OLLAMA_MODEL_MAP='{"general":"mistral","coding":"qwen2.5:3b","summarization":"gemma2:2b","fast":"phi3:mini"}'
```

In Docker Compose, `OLLAMA_URL` continues to point at Ollama on the host through
`host.docker.internal`. To use an external vLLM deployment instead, provide the
OpenAI-compatible variables to Compose; no inference container or GPU requirement
is added to this stack.

Example external vLLM configuration (replace the endpoint, model IDs, and optional
credential with values from the actual deployment):

```bash
export INFERENCE_PROVIDER=openai_compatible
export OPENAI_COMPATIBLE_BASE_URL='https://vllm.example/v1'
export OPENAI_COMPATIBLE_API_KEY='replace-with-runtime-secret'
export OPENAI_COMPATIBLE_CONNECT_TIMEOUT=5
export OPENAI_COMPATIBLE_READ_TIMEOUT=120
export OPENAI_COMPATIBLE_MODEL_MAP='{"general":"gpt-oss-20b","coding":"gpt-oss-20b","summarization":"gpt-oss-20b","fast":"gpt-oss-20b"}'
export OPENAI_COMPATIBLE_GENERATION_PARAMETERS='{"temperature":0.2}'
```

The adapter sends non-streaming and streaming chat requests to
`/v1/chat/completions`. Upstream streaming uses SSE (`data: {...}` followed by
`data: [DONE]`); the adapter converts that into provider-neutral text chunks.
This matches the [vLLM OpenAI-compatible server API](https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/).
PolyMind continues to expose its own NDJSON event contract from `/query/stream` and
does not proxy vLLM SSE to clients. HTTP connections are pooled, connect/read
timeouts are explicit, responses are closed, and public errors do not contain
upstream bodies or credentials.

## Liveness, readiness, and failure handling

`GET /health` reports only that the PolyMind API process is alive. The existing
`GET /` response is preserved for compatibility. `GET /ready` performs lightweight
model discovery against the selected provider: OpenAI-compatible providers use
`GET /v1/models`, while Ollama uses `GET /api/tags`. It returns HTTP 200 with
`status: ready` only when every configured logical-role model is advertised;
unreachable, timeout, authentication, overload, missing-model, malformed-protocol,
and other upstream states return a sanitized HTTP 503 response.

In other words, API alive does not imply inference ready. A temporary provider
outage does not prevent PolyMind from starting, and readiness never generates
tokens. Transient readiness probes receive at most the configured number of
additional attempts with bounded linear backoff. Generation and streaming are not
automatically retried because the provider may already have accepted the request;
restarting could duplicate work or user-visible tokens. A stream failure emits the
existing sanitized NDJSON `error` event and incomplete output is not persisted.

Every API response includes `X-Request-ID`. A caller-provided ID is accepted only
when it is 1–64 characters from a bounded safe character set; otherwise PolyMind
generates one. Provider and failure logs include the identifier and operational
category without prompts, credentials, authorization headers, or upstream bodies.

---

# 📊 Multi-LLM Benchmark

The platform benchmarks local LLMs to drive evidence-based routing decisions.

| Model | Role | Strength | Typical Usage |
|------|------|----------|--------------|
| Phi3 Mini | Fast inference | Lowest latency | Quick responses |
| Gemma 2 | Summarization | Detailed summaries | Document summarization |
| Qwen 2.5 | Coding | Strong code generation | Programming tasks |
| Mistral | General reasoning | Balanced performance | Default assistant |

Benchmark metrics:

- Response latency
- Response length
- Task specialization
- Overall efficiency

## Latency Comparison

<p align="center">
  <img src="./results/benchmark_latency.png" width="850">
</p>

## Response Length Comparison

<p align="center">
  <img src="./results/benchmark_words.png" width="850">
</p>

These benchmarks justify the dynamic model router implemented in Estudio PolyMind.

---

# 📂 Project Structure

```text
estudio-polymind-llm-orchestration
│
├── api/
├── config/
├── graph/
├── llm/
├── memory/
├── rag/
├── tools/
├── ui/
├── experiments/
├── results/
├── data/docs/
└── chroma_db/
```

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| Workflow Engine | LangGraph |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| Reranker | Cross Encoder |
| Retrieval | BM25 + RRF |
| LLM Runtime | Ollama or external OpenAI-compatible service (target: vLLM) |
| Models | Mistral, Qwen2.5, Gemma2, Phi3 |

---

# 🧪 Evaluation Framework

Implemented evaluation workflows for:

```bash
python experiments/test_retriever.py
python experiments/test_bm25.py
python experiments/test_hybrid.py
python experiments/test_router.py
python experiments/test_langgraph_chunks.py
python experiments/test_reranker.py
python experiments/test_retrieval_eval.py
python experiments/test_streaming.py
python experiments/test_pdf.py
```

Metrics:

- Retrieval recall
- Source accuracy
- Router accuracy
- Hybrid retrieval performance
- Reranking quality

The automated unit suite is separate from experiments and does not require Ollama,
model downloads, a vector database, or a GPU:

```bash
python -m pytest
# or
make test
```

GitHub Actions runs this suite after compile validation and before the Docker build.

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration.git

cd estudio-polymind-llm-orchestration
```

## Create Environment

```bash
python -m venv .venv

source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🚀 Running the Project

## Build Vector Database

```bash
make ingest
```

## Start API

```bash
make api
```

## Start UI

```bash
make ui
```

## Run Full System

```bash
make dev
```

---

# 🔬 Phase Roadmap

## Phase 1 ✅

- Multi-LLM Setup

## Phase 2 ✅

- ChromaDB Integration

## Phase 3 ✅

- RAG Pipeline

## Phase 4 ✅

- LangGraph Orchestration

## Phase 5 ✅

- Conversational Memory

## Phase 6 ✅

- Semantic Routing
- Hybrid Retrieval
- BM25 Search
- RRF Fusion
- Cross-Encoder Reranking
- Retrieval Evaluation
- Streaming Generation
- FastAPI + Streamlit Integration

## Phase 7 ✅

- Configuration Management
- Environment Variables
- Observability
- Multi-Session Support
- Multi-LLM Benchmarking
- Dockerization
- GitHub Actions CI

## Phase 8A ✅

- Provider-neutral inference contract
- Ollama inference adapter and logical model-role mapping
- Explicit inference timeouts and normalized provider errors
- Single-request streaming with metadata and session preservation
- Automated unit tests in CI

## Phase 8B ✅

- OpenAI-compatible chat-completions adapter for an external vLLM service
- Configurable optional Bearer authentication, model mappings, generation parameters, and timeouts
- OpenAI-compatible SSE parsing with explicit `[DONE]` termination
- Shared provider contracts and mocked protocol tests that require no live inference server or GPU
- Preserved PolyMind NDJSON streaming and Ollama behavior

---

# 📸 Screenshots

### Streamlit Interface

![UI](media/streamlit_ui.png)

### Swagger API

![Swagger](media/swagger_ui.png)

### Model Routing

![Routing](media/model_routing.png)

### RAG Query

![RAG](media/rag_query.png)

---

# 👨‍💻 Author

**Susanta Hazra**

AI Engineer | ML Engineer | Generative AI Enthusiast

Specializing in:

- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- LangGraph & AI Agents
- FastAPI & MLOps
- Production AI Systems

GitHub:

https://github.com/Susanta2025-lab

LinkedIn:

https://www.linkedin.com/in/susantahazra/

---

# ⭐ Project Status

**Version:** v1.0.0

**Status:** Production-Ready Portfolio Project

## Implemented Components

✅ Multi-LLM Orchestration

✅ RAG Pipeline

✅ LangGraph Workflows

✅ Semantic Routing

✅ Hybrid Retrieval

✅ BM25 + RRF Fusion

✅ Cross-Encoder Reranking

✅ Conversational Memory

✅ FastAPI + Streamlit

✅ Multi-LLM Benchmarking

✅ Dockerization

✅ GitHub Actions CI

## Focus Areas

- Multi-LLM Orchestration
- Agentic AI
- Retrieval-Augmented Generation
- Semantic Search
- Local AI Infrastructure
- AI Engineering

---

# ⭐ If you found this project interesting, consider giving it a star!
