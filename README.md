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

RAG code depends on a provider-neutral vector-store contract rather than a
concrete client. `chroma_local` (the backward-compatible default) persists under
`CHROMA_PATH` for local, single-replica development. `chroma_http` connects each
API worker to one external Chroma server and is the supported shared mode for
horizontal replicas. It never falls back to local persistence.
Serving clients use Chroma's read-only collection lookup. Collection creation,
upsert, reset, and corpus-version publication require the explicit admin client.

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

Graph and API code use a narrow provider-neutral contract for ordered history
reads, atomic exchange appends, session clearing, and readiness checks.

- `file` (default) preserves `memory/chat_history.json` for local development.
  It uses process/file locks and atomic replacement, but remains a single-host
  backend and is not shared replica storage.
- `redis` stores each session in a shared Redis list. Each user/assistant exchange
  is appended, trimmed, and optionally given a TTL in one transaction, preventing
  concurrent replicas from overwriting one another's history.

Redis keys contain a fixed namespace plus a SHA-256 digest of the bounded session
ID. `MEMORY_HISTORY` limits retained messages; `MEMORY_TTL=0` disables expiry and
a positive value is an idle-session TTL refreshed by successful exchanges. Failed
inference, incomplete streams, and failed transactions do not persist partial
exchanges.

| Environment variable | Default | Purpose |
|---|---|---|
| `MEMORY_PROVIDER` | `file` | `file` or `redis`; no runtime fallback |
| `MEMORY_FILE` | `memory/chat_history.json` | Local file-provider path |
| `MEMORY_HISTORY` | `6` | Positive retained-message limit per session |
| `REDIS_URL` | `redis://localhost:6379/0` | Shared Redis endpoint |
| `MEMORY_CONNECT_TIMEOUT` | `2` | Connection timeout in seconds |
| `MEMORY_OPERATION_TIMEOUT` | `2` | Socket/operation timeout in seconds |
| `MEMORY_TTL` | `0` | Idle-session expiry seconds; zero disables it |

For local Redis development, run `MEMORY_PROVIDER=redis docker compose --profile
redis up`. The optional Compose service is not a production deployment model.
Production replicas must use the same external Redis service with suitable
authentication, encryption, network policy, persistence, and availability
controls. Connection URLs and credentials are never returned or logged.

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

Production enables a narrow bearer-token boundary for `/query`,
`/query/stream`, and conversation-history access. Local development keeps auth
disabled and interactive docs enabled; production configuration requires auth,
a runtime token of at least 32 non-whitespace characters, and disabled docs,
ReDoc, and OpenAPI URLs. Query bodies default to a 1 MiB ASGI-enforced limit.

Health/readiness and metrics remain unauthenticated cluster-operational endpoints
and are excluded from the default public Ingress. NetworkPolicy is enabled by
default in the production chart with explicit gateway, monitoring, DNS, Redis,
Chroma, and inference rules. See
[`docs/security/production-security.md`](docs/security/production-security.md)
and [`docs/security/threat-model.md`](docs/security/threat-model.md).

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
`GET /` response is preserved for compatibility. `GET /ready` performs bounded
inference, memory, vector-store, and BM25-version checks. OpenAI-compatible providers use
`GET /v1/models`, while Ollama uses `GET /api/tags`. It returns HTTP 200 with
`status: ready` only when every configured logical-role model is advertised,
memory and vector storage are available, and the process-local BM25 snapshot
matches the configured and published corpus version. Redis uses `PING`; the file
backend checks local path access. The response includes sanitized `inference`,
`memory`, `vector_store`, and `bm25` component states;
unreachable, timeout, authentication, overload, missing-model, malformed-protocol,
and other upstream states return a sanitized HTTP 503 response.

In other words, API alive does not imply inference ready. A temporary provider
outage does not prevent PolyMind from starting. Startup attempts one bounded BM25
build and enters an alive/not-ready state if it fails. Readiness never builds BM25
or generates tokens. Transient readiness probes receive at most the configured number of
additional attempts with bounded linear backoff. Generation and streaming are not
automatically retried because the provider may already have accepted the request;
restarting could duplicate work or user-visible tokens. A stream failure emits the
existing sanitized NDJSON `error` event and incomplete output is not persisted.
Memory connectivity, timeout, malformed-data, read, and write failures are also
normalized. If Redis is selected, failure stays visible and never triggers a
file fallback, avoiding split-brain state between replicas.

Shutdown clears the local BM25 snapshot, closes Redis/vector lifecycle objects,
and closes the OpenAI-compatible HTTP session owned by the process. PolyMind does
not own the lifecycle of production inference, Redis, or Chroma services.

Every API response includes `X-Request-ID`. A caller-provided ID is accepted only
when it is 1–64 characters from a bounded safe character set; otherwise PolyMind
generates one. Provider and failure logs include the identifier and operational
category without prompts, credentials, authorization headers, or upstream bodies.

## Observability and inference metrics

`GET /metrics` exposes process-local metrics in the Prometheus text exposition
format. Scraping it performs no provider, readiness, retrieval, or inference call.
The instrumentation covers inference outcomes and latency, normalized errors,
stream lifetime, time to first token (TTFT), exact provider-reported token usage,
bounded semantic-route behavior, readiness outcomes/latency, and bounded memory
operation/readiness outcomes, latency, and normalized errors. Vector operations
and readiness add the same bounded outcome, duration, and error-category views;
dense queries, BM25 snapshot reads, upserts, and resets are distinguished only by
a fixed operation label. `component_readiness` is a bounded per-component gauge;
`bm25_snapshot_build_duration_seconds` and `bm25_snapshot_refresh_total` describe
the startup snapshot attempt. Corpus versions are never Prometheus labels.

TTFT is the time until the first non-empty generated content chunk; SSE comments,
role deltas, empty deltas, and usage-only chunks do not count. OpenAI-compatible
token metrics use a valid `usage` object when supplied, including optional stream
usage chunks. Ollama uses non-negative `prompt_eval_count` and `eval_count` fields.
Missing values remain unknown: PolyMind does not tokenize prompts or fabricate
counts. Completion-token throughput can be derived from the completion-token
counter and measured time/rate instead of storing a redundant gauge.

Labels are limited to provider, configured logical role and served model,
operation, outcome, route, normalized error category, and token type. Request IDs,
session IDs, queries, prompts, documents, URLs, and exception messages are
excluded. Request IDs remain in operational logs for individual diagnosis while
metrics describe aggregate behavior.

This is instrumentation only; Prometheus, Grafana, dashboards, alerts, and tracing
are not deployed. Metrics registries remain process-local: scrape every worker or
replica independently and aggregate in the monitoring system, or configure a
supported Prometheus multiprocess deployment. Redis is application state and is
not used as a metrics registry. In a
production deployment, `/metrics` should be network-restricted or protected by
infrastructure because the application has no endpoint authentication layer.

## Production topology and multi-replica deployment constraints

### Kubernetes and Helm

The production control-plane chart is at
[`deployment/helm/polymind`](deployment/helm/polymind/README.md). It deploys
replicated PolyMind API pods and a Service, with an optional disabled-by-default
Ingress. It deliberately does **not** deploy vLLM/OpenAI-compatible inference,
Redis, Chroma, Prometheus, an ingress controller, or cloud infrastructure.

Production values must identify externally operated inference and Chroma
endpoints, an already-published BM25 corpus version, and a pre-created Kubernetes
Secret containing the Redis URL and (when needed) inference API key. Validate the
chart locally without a cluster using:

```bash
make helm-validate
```

Liveness uses `/health`; readiness uses `/ready` and therefore requires
inference, Redis, Chroma, and the version-matched BM25 snapshot. `/metrics` shares
the application port and must be network-restricted in production. The chart
runbook documents installation, upgrades, rollback, and security defaults.

### Local Kubernetes operational validation

Phase 10 validates the chart on a dedicated Kind cluster named
`polymind-phase10`. This is an explicit laptop/CI-style operational workflow,
not a production topology. Its fixtures provide ephemeral Redis, Chroma 1.5.9,
and a deterministic OpenAI-compatible inference stub in the isolated
`polymind-phase10` namespace; none are dependencies of the production Helm
chart. Docker, kubectl, Helm 3, and Kind are prerequisites.

```bash
make k8s-phase10-create
make k8s-phase10-build
make k8s-phase10-load-image
make k8s-phase10-deploy
deployment/kind/phase10/phase10.sh bootstrap phase10-v1
make k8s-phase10-test
```

The deployment initially starts before a corpus exists: `/health` remains 200
while `/ready` is 503 with BM25 uninitialized. The bootstrap command performs a
deterministic administrative upsert and publishes `phase10-v1`; restart the
Deployment so every process builds that immutable snapshot at startup:

```bash
kubectl --context kind-polymind-phase10 -n polymind-phase10 \
  rollout restart deployment/polymind-polymind
kubectl --context kind-polymind-phase10 -n polymind-phase10 \
  rollout status deployment/polymind-polymind --timeout=300s
```

To validate version gating, publish `phase10-v2` while pods still expect
`phase10-v1`: readiness becomes 503 and Service endpoints are removed. Upgrade
the release with `application.bm25CorpusVersion=phase10-v2`; replacement pods
load the current snapshot and recover. Use `helm history` and `helm rollback`
against the fixed namespace to validate revision restoration.

For replica compatibility, set `replicaCount=2`, wait for rollout, and verify
both ready pods use the shared Redis and Chroma Services. A scoped Redis outage
can be tested by scaling `deployment/phase10-redis` to zero: PolyMind `/health`
stays 200 while `/ready` becomes 503; scale Redis back to one and readiness
recovers. Delete one PolyMind pod to observe Deployment reconciliation. Use
port-forwarding rather than Ingress for `/query`, `/query/stream`, and `/metrics`.

The guarded commands and fixture caveats are in
[`deployment/kind/phase10/README.md`](deployment/kind/phase10/README.md). Teardown
is deliberately limited to the named Kind cluster:

```bash
make k8s-phase10-destroy
```

```text
External clients
      |
PolyMind API replicas (FastAPI / LangGraph / RAG control plane)
      |----------------------|----------------------|
      v                      v                      v
External OpenAI-         Shared Redis          Shared Chroma HTTP
compatible inference    conversation state    vectors + corpus version

Controlled ingestion/admin -> Shared Chroma -> publish corpus version
                                      -> controlled API replica rollout
```

PolyMind owns serving, orchestration, routing, request correlation, readiness,
and per-process metrics. Operators separately own inference, Redis, and Chroma
lifecycle, durability, availability, and security. `DEPLOYMENT_ENV=production`
requires OpenAI-compatible inference, Redis, and Chroma HTTP with non-loopback
service hosts. Static configuration errors fail early; network outages degrade
readiness. Docker Compose profiles remain local-development conveniences and are
not the production deployment model.

Conversation memory is replica-safe when all workers use `MEMORY_PROVIDER=redis`
and the same external service. Inference adapters are stateless, configuration is
immutable after startup, and request correlation uses request-local context.

RAG dense retrieval is replica-safe when every worker uses
`VECTOR_STORE_PROVIDER=chroma_http` and the same external Chroma service and
collection. Client and collection initialization are lazy and imports perform no
remote service access. Startup performs one bounded BM25 attempt and survives
failure. `/health` remains process-only, while `/ready` requires inference,
memory, vector, and current BM25 readiness. There is no silent local fallback.

Serving code receives only retrieval access through the vector-store boundary.
Ingestion and reset use the explicit `rag.ingest` and `rag.admin` administrative
commands. Stable content-derived IDs make repeated/concurrent upserts idempotent.
Only the admin client uses Chroma's backend-native get-or-create operation.
Chroma provides concurrent server reads and makes completed upserts visible to
clients through the shared collection. This repository does not add distributed
locking or claim transactional consistency across a multi-document ingestion.

BM25 is a process-local immutable startup snapshot. `BM25_CORPUS_VERSION` is a
safe 1–64 character publication identifier. Ingestion performs deterministic
UUIDv5 upserts and publishes that version in Chroma collection metadata only
after all chunks succeed. Each replica configured with that expected version
canonically sorts the shared documents and builds BM25 once during startup.
Readiness returns 503 when the snapshot is uninitialized or its loaded/configured
version differs from Chroma. It never rebuilds in request or readiness threads.

The rollout procedure is: select a new immutable version, complete ingestion and
publication, then restart/roll all replicas with that same value. Old replicas
become unready when they observe the new publication; new replicas become ready
only after loading it. Publication is not a transaction over the full ingestion,
and automatic reload and blue/green vector publication remain future work. Dense
retrieval, BM25 tokenization/ranking, RRF, reranking, and source metadata remain
compatible.

Production networks should restrict vLLM, Redis, and Chroma to trusted service
paths. Use Redis authentication/TLS (`rediss`) and Chroma/vLLM authentication and
TLS where supported by the operated services. Restrict `/metrics`, scrape every
replica independently, and run ingestion/admin as a controlled job rather than a
public API.

### Deterministic CPU model packaging

The production control-plane image installs `torch==2.12.0+cpu` from PyTorch's
CPU wheel index before installing the fully pinned application requirements. It
contains no NVIDIA, CUDA, Triton, vLLM, Ollama, or generative-model runtime.
External LLM inference remains behind the provider-neutral Ollama or
OpenAI-compatible adapters.

Two local model snapshots are acquired during `docker build` and stored read-only
under `/opt/polymind/models`: `sentence-transformers/all-MiniLM-L6-v2` at revision
`1110a243fdf4706b3f48f1d95db1a4f5529b4d41` for dense retrieval and semantic
routing, and `cross-encoder/ms-marco-MiniLM-L-6-v2` at revision
`c5ee24cb16019beea0893ab7796b1df96625c6b8` for reranking. A failed acquisition
fails the build. Runtime uses `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, and
`MODEL_OFFLINE_MODE=true`; missing artifacts fail model loading instead of
triggering a download.

Local development may leave `MODEL_ARTIFACT_DIR` unset and
`MODEL_OFFLINE_MODE=false`; the same pinned revisions then use the developer's
normal Hugging Face cache. To update a model, change its identifier/revision in
`config/model_artifacts.py`, review retrieval-quality implications, rebuild the
image, and rerun the offline smoke test:

```bash
docker run --rm --network none --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=256m \
  --entrypoint python polymind:phase12 -m scripts.validate_container_models
```

The production Helm chart enables `readOnlyRootFilesystem` and mounts a bounded
256 MiB `/tmp` `emptyDir`; transient caches live at `/tmp/polymind-cache`.

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

The command writes to whichever provider is configured. Reset is deliberately an
administrative action (`python -m rag.admin reset`) and is never performed by API
startup. For local persistence, the defaults are sufficient:

```bash
VECTOR_STORE_PROVIDER=chroma_local
CHROMA_PATH=./chroma_db
VECTOR_STORE_COLLECTION=knowledge_base
```

For a shared service:

```bash
VECTOR_STORE_PROVIDER=chroma_http
VECTOR_STORE_HOST=chroma.example.internal
VECTOR_STORE_PORT=8000
VECTOR_STORE_SSL=true
VECTOR_STORE_COLLECTION=knowledge_base
VECTOR_STORE_TIMEOUT=5
BM25_CORPUS_VERSION=release-2026-08-24
```

After changing `BM25_CORPUS_VERSION`, run ingestion to completion and then roll
every API replica with the same value. `make rebuild` and `make clean` are explicit
destructive admin actions; API startup and serving expose no ingestion/reset path.

The optional Compose profile is development-only and deliberately publishes no
Chroma host port:

```bash
VECTOR_STORE_PROVIDER=chroma_http docker compose --profile vector up
docker compose exec api python rag/ingest.py
```

Production deployments should point all PolyMind replicas at a separately
operated shared Chroma service with appropriate network isolation, TLS and/or
authentication controls, persistence, backups, and availability management.
The Compose profile is not a production topology and its local service is
unauthenticated.

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
