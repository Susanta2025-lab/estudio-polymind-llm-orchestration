# 🧠 Estudio PolyMind

### Multi-LLM RAG & AI Orchestration Platform

> Local-first AI infrastructure for Retrieval-Augmented Generation (RAG), semantic search, intelligent routing, and multi-LLM orchestration using open-source language models.

---

## 🚀 Overview

**Estudio PolyMind** is a modular LLM engineering platform designed to simulate real-world enterprise GenAI systems.

The project combines:

- 🤖 Open-source LLMs via Ollama
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔍 ChromaDB vector search
- 📄 PDF/TXT document ingestion
- ⚡ FastAPI backend services
- 🔄 LangGraph workflow orchestration
- 🧩 Intelligent query routing
- 🖥️ Local AI deployment

Unlike traditional chatbot projects, PolyMind focuses on **LLM orchestration architecture**, where queries are dynamically routed through different execution paths such as direct inference or retrieval-augmented reasoning.

---

# ✨ Core Features

## 🤖 Multi-LLM Ready

Supports local inference through Ollama with:

- Mistral
- Qwen
- Gemma
- Phi

Current active model:

```text
Mistral
```

Future phases introduce dynamic model routing and specialization.

---

## 🧠 Retrieval-Augmented Generation (RAG)

- Semantic document retrieval
- Context-aware generation
- Source-aware responses
- Metadata tracking
- Persistent vector storage

---

## 📄 Advanced Document Processing

Supported formats:

- PDF
- TXT

Pipeline:

```text
Documents
    ↓
Loaders
    ↓
Smart Chunking
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Retrieval
```

---

## 🔍 Vector Database Integration

Powered by:

**ChromaDB**

Capabilities:

- Persistent vector storage
- Similarity search
- Semantic retrieval
- Metadata indexing

---

## 🔄 LangGraph Orchestration

Current workflow:

```text
User Query
      ↓
Router Node
      ↓
 ┌─────────────┬─────────────┐
 │ Direct LLM  │ RAG Agent   │
 └─────────────┴─────────────┘
      ↓
 Response
```

This creates a foundation for:

- Agent workflows
- Tool calling
- Multi-step reasoning
- Model routing

---

# 🏗️ System Architecture

```text
                 ┌────────────────────┐
                 │     User Query     │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │    FastAPI API     │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │   LangGraph Flow   │
                 │ (Query Routing)    │
                 └─────────┬──────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
      ┌──────────────┐          ┌──────────────┐
      │ Direct LLM   │          │  RAG Agent   │
      └──────┬───────┘          └──────┬───────┘
             │                         │
             │                         ▼
             │              ┌────────────────────┐
             │              │ Semantic Retrieval │
             │              └─────────┬──────────┘
             │                        │
             │                        ▼
             │              ┌────────────────────┐
             │              │     ChromaDB       │
             │              │   Vector Store     │
             │              └─────────┬──────────┘
             │                        ▲
             │                        │
             │              ┌────────────────────┐
             │              │ Embedding Pipeline │
             │              └─────────┬──────────┘
             │                        ▲
             │                        │
             │              ┌────────────────────┐
             │              │ PDF/TXT Loaders    │
             │              │ Smart Chunking     │
             │              │ Metadata Tracking  │
             │              └────────────────────┘
             │
             ▼
      ┌──────────────┐
      │   Ollama     │
      │   Mistral    │
      └──────┬───────┘
             │
             ▼
      ┌──────────────┐
      │   Response   │
      └──────────────┘
```

---

# 📂 Project Structure

```text
polymind-rag-studio/
│
├── api/
│   └── app.py
│
├── llm/
│   ├── ollama_client.py
│   └── router.py
│
├── rag/
│   ├── loaders/
│   │   ├── pdf_loader.py
│   │   └── text_loader.py
│   │
│   ├── chunking.py
│   ├── embeddings.py
│   ├── ingest.py
│   ├── retriever.py
│   └── vectordb.py
│
├── graph/
│   ├── state.py
│   ├── nodes.py
│   └── langgraph_flow.py
│
├── data/
│   └── docs/
│
├── chroma_db/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Technology Stack

| Layer | Technologies |
|---------|---------|
| LLM Runtime | Ollama |
| Models | Mistral, Qwen, Gemma, Phi |
| Backend | FastAPI |
| Orchestration | LangGraph |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| Document Processing | PyPDF |
| Chunking | Recursive Text Splitters |
| Language | Python |
| Deployment | Docker (Planned) |

---

# ⚡ Quick Start

## Clone Repository

```bash
git clone https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration.git

cd estudio-polymind-llm-orchestration
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Pull Model

```bash
ollama pull mistral
```

## Add Documents

Place files inside:

```text
data/docs/
```

Supported:

```text
.pdf
.txt
```

## Ingest Documents

```bash
python -m rag.ingest
```

## Start API

```bash
uvicorn api.app:app --reload
```

## Open Swagger Docs

```text
http://127.0.0.1:8000/docs
```

---

# 📈 Development Roadmap

## ✅ Phase 1 — Local LLM Infrastructure

- Ollama setup
- Mistral integration
- FastAPI backend
- Local inference

## ✅ Phase 2 — RAG Pipeline

- Embeddings generation
- ChromaDB integration
- Semantic retrieval
- Context injection

## ✅ Phase 2.5 — Production RAG Upgrade

- PDF ingestion
- Smart chunking
- Metadata tracking
- Source attribution
- Persistent vector storage

## 🚧 Phase 3 — LangGraph Orchestration

- Query routing
- Workflow graph
- Direct LLM node
- RAG node
- Conditional execution

## 🔮 Upcoming Phases

### Multi-Model Routing

```text
Query
   ↓
Model Router
   ↓
Mistral / Qwen / Gemma / Phi
```

### Future Additions

- Tool calling
- Memory systems
- Agent workflows
- Hybrid search
- Re-ranking
- Streaming responses
- Docker deployment
- Frontend UI
- vLLM integration
- Evaluation pipelines

---

# 🎯 Learning Objectives

This project demonstrates:

- LLM Engineering
- Retrieval-Augmented Generation
- Vector Databases
- LangGraph Workflows
- AI Orchestration
- FastAPI Development
- Local AI Infrastructure
- Open-Source LLM Deployment
- Semantic Search Systems
- Production-Style AI Architecture

---

# 🏆 Why This Project Matters

Modern AI systems are no longer single-model chatbots.

They require:

- retrieval systems
- orchestration engines
- workflow routing
- vector databases
- memory layers
- model specialization

Estudio PolyMind is designed as a practical implementation of these modern AI engineering patterns using entirely local and open-source infrastructure.

---

## ⭐ Support

If you find this project useful:

- ⭐ Star the repository
- 🍴 Fork the project
- 🧠 Explore LLM orchestration systems
- 🚀 Build your own AI agents
