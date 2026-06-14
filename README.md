# 🧠 Estudio PolyMind

### Multi-LLM RAG & Agent Orchestration Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)]()
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-orange.svg)]()
[![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-purple.svg)]()
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLMs-black.svg)]()

A production-style AI platform that combines **Multi-LLM orchestration**, **Retrieval-Augmented Generation (RAG)**, **semantic routing**, **hybrid retrieval**, **cross-encoder reranking**, **conversation memory**, and **local LLM inference** using Ollama.

Built to demonstrate modern AI Engineering practices including agent orchestration, retrieval pipelines, semantic search, model routing, and local-first deployment.

---

# 🚀 Key Features

## Multi-LLM Orchestration

Supports multiple local LLMs through Ollama:

- Mistral
- Qwen 2.5
- Gemma 2
- Phi-3 Mini

Dynamic model selection based on query type:

| Task | Model |
|--------|--------|
| General reasoning | Mistral |
| Coding | Qwen 2.5 |
| Summarization | Gemma 2 |
| Fast responses | Phi-3 Mini |

---

## Semantic Query Routing

Uses Sentence Transformers embeddings and cosine similarity for semantic intent classification.

Routes queries into:

- RAG Pipeline
- Tool Execution
- Direct LLM Response

Example:

| Query | Route |
|---------|---------|
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

Uses:

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

Integrated utility tools:

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

Swagger Documentation:

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

# 🏗 System Architecture

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
 │ Selected LLM    │
 └────────┬────────┘
          │
          ▼
      Final Answer
```

---

# 📂 Project Structure

```text
estudio-polymind-llm-orchestration
│
├── api/
│   └── app.py
│
├── graph/
│   ├── langgraph_flow.py
│   ├── nodes.py
│   ├── semantic_router.py
│   └── state.py
│
├── llm/
│   ├── models.py
│   ├── ollama_client.py
│   └── router.py
│
├── memory/
│   ├── chat_history.json
│   └── memory_store.py
│
├── rag/
│   ├── bm25.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── hybrid_retriever.py
│   ├── retriever.py
│   ├── reranker.py
│   ├── ingest.py
│   └── vectordb.py
│
├── tools/
│   ├── calculator.py
│   └── datetime_tool.py
│
├── ui/
│   └── app.py
│
├── experiments/
│
├── data/
│   └── docs/
│
└── chroma_db/
```

---

# 🧪 Evaluation Framework

Implemented evaluation workflows for:

### Retrieval

```bash
python experiments/test_retrieval_eval.py
```

Metrics:

- Recall
- Source retrieval accuracy

### Router

```bash
python experiments/test_router.py
```

Metrics:

- Intent classification accuracy

### Hybrid Search

```bash
python experiments/test_hybrid.py
```

### BM25

```bash
python experiments/test_bm25.py
```

### Reranker

```bash
python experiments/test_reranker.py
```

### Chunking

```bash
python experiments/test_langgraph_chunks.py
```

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

## Phase 1
- Multi-LLM Setup

## Phase 2
- ChromaDB Integration

## Phase 3
- RAG Pipeline

## Phase 4
- LangGraph Orchestration

## Phase 5
- Conversational Memory

## Phase 6 ✅
- Semantic Router
- Hybrid Retrieval
- BM25 Search
- RRF Fusion
- Cross-Encoder Reranking
- Retrieval Evaluation
- Streaming Generation
- FastAPI + Streamlit Integration

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

- GitHub: https://github.com/Susanta2025-lab
- LinkedIn: https://www.linkedin.com/in/susantahazra/

---

# ⭐ Project Status

**Version:** v0.6.0

**Status:** Stable

**Focus Areas:**

- Multi-LLM Orchestration
- Agentic AI
- Retrieval-Augmented Generation
- Semantic Search
- Local AI Infrastructure
- AI Engineering

---

# ⭐ If you found this project interesting, consider giving it a star!
