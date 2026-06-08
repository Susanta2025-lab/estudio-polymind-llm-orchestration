# 🧠 Estudio PolyMind

### Multi-LLM RAG & Agent Orchestration Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)]()
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-orange.svg)]()
[![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-purple.svg)]()
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLMs-black.svg)]()

---

## 🚀 Overview

Estudio PolyMind is a production-style Multi-LLM Retrieval-Augmented Generation (RAG) platform that orchestrates multiple open-source Large Language Models through LangGraph workflows.

The platform supports:

- Multi-LLM routing
- Retrieval-Augmented Generation (RAG)
- Persistent conversation memory
- Tool calling
- Dynamic workflow orchestration
- Local-first deployment using Ollama
- Source-aware document retrieval

Built to demonstrate modern AI Engineering and Agentic AI architecture patterns.

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration.git

cd estudio-polymind-llm-orchestration
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Ollama

```bash
ollama serve
```

Pull any required models:

```bash
ollama pull mistral
ollama pull qwen
ollama pull gemma
ollama pull phi
```

### 4. Ingest Documents

```bash
make ingest
```

### 5. Start FastAPI Backend

```bash
make api
```

### 6. Launch Streamlit UI

```bash
make ui
```

### 7. Open the Application

```text
http://localhost:8501
```

---

## ✨ Key Features

### 🧠 Multi-LLM Orchestration

Dynamically routes requests between:

- Mistral
- Qwen
- Gemma
- Phi

based on query type and workflow requirements.

---

### 🔍 Retrieval-Augmented Generation (RAG)

- PDF ingestion pipeline
- Text document ingestion
- Embedding generation
- ChromaDB vector storage
- Semantic retrieval
- Source tracking
- Relevance scoring

---

### 🔄 LangGraph Workflow Engine

Implements graph-based orchestration:

```text
 User Query
      │
      ▼
 Router Node
      │
      ▼
 Model Router
      │
 ┌────┼────┐
 │    │    │
 ▼    ▼    ▼
RAG Direct Tool
 │    │    │
 └────┴────┘
      │
      ▼
 Response
```

---

### 🧾 Persistent Memory

Stores conversation history across sessions.

Features:

- Session-based memory
- Persistent storage
- Context continuity
- Long-running interactions

---

### 🛠 Tool Calling

Current tools include:

- Calculator
- Date & Time Utility

Extensible architecture for future tools.

---

## 🏗 System Architecture

```text
                     User
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
   Streamlit UI                FastAPI API
         │                           │
         └─────────────┬─────────────┘
                       │
                       ▼
                 LangGraph Flow
                       │
                Router Node
                       │
                       ▼
                 Model Router
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
      Direct LLM      RAG         Tools
          │            │            │
          ▼            ▼            ▼
     Ollama Models   ChromaDB   Utilities
          │            │
          ▼            ▼
   Mistral / Qwen   Vector Search
   Gemma / Phi
          │
          ▼
   Persistent Memory
          │
          ▼
       Response
```

---

## 📂 Project Structure

```text
estudio-polymind-llm-orchestration/
│
├── api/
│   └── app.py
│
├── ui/
│   ├── app.py
│   └── assets/
│       └── susanta.png
│
├── graph/
│   ├── langgraph_flow.py
│   ├── nodes.py
│   └── state.py
│
├── llm/
│   ├── models.py
│   ├── ollama_client.py
│   └── router.py
│
├── rag/
│   ├── chunking.py
│   ├── embeddings.py
│   ├── ingest.py
│   ├── retriever.py
│   ├── test_retriever.py
│   ├── vectordb.py
│   └── loaders/
│       ├── pdf_loader.py
│       └── text_loader.py
│
├── data/
│   └── docs/
│       ├── ai_notes.text
│       ├── LangGraph_Documentation.pdf
│       ├── original_rag_paper.pdf
│       ├── rag_survey.pdf
│       ├── rag_using_llm.pdf
│       └── information_retrieval_retrieval_augmented_generation.pdf
│
├── memory/
│   ├── memory_store.py
│   └── chat_history.json
│
├── tools/
│   ├── calculator.py
│   └── datetime_tool.py
│
├── utils/
│   └── logger.py
│
├── media/
│   ├── streamlit_ui.png
│   ├── swagger_ui.png
│   ├── model_routing.png
│   └── rag_query.png
│
├── chroma_db/
│
├── Makefile
├── requirements.txt
└── README.md
```
---

## 📸 Demo

### Streamlit User Interface

Interactive web-based interface for querying and managing RAG pipelines.

![Streamlit UI](media/streamlit_ui.png)

---
### FastAPI API Interface

![Swagger UI](media/swagger_ui.png)

---
### Dynamic Model Selection

PolyMind automatically routes requests to the most suitable model.

![Model Routing](media/model_routing.png)

---
### Source-Aware RAG

![RAG Retrieval](media/rag_query.png)

---
## 🔄 Workflow Example

### Example Query

```json
{
  "query": "What is LangGraph?",
  "session_id": "default"
}
```

### Workflow Execution

```text
User Query
    │
    ▼
Router Node
    │
    ▼
Model Router
    │
    ▼
RAG Path
    │
    ▼
Retriever
    │
    ▼
ChromaDB
    │
    ▼
Mistral
    │
    ▼
Response + Sources
```

### Example Response

```json
{
  "route": "rag",
  "model": "mistral",
  "response": "LangGraph is a framework for building stateful AI workflows...",
  "sources": [
    {
      "source": "LangGraph_Documentation.pdf",
      "chunk_id": 0
    }
  ]
}
```

---

## ⚙️ Technology Stack

### LLMs

- Mistral
- Qwen
- Gemma
- Phi

### AI Frameworks

- LangGraph
- Ollama
- Sentence Transformers

### Backend

- FastAPI
- Pydantic

### Frontend

- Streamlit

### Retrieval

- ChromaDB
- Vector Embeddings
- Semantic Search

### Infrastructure

- Local LLM Deployment
- Persistent Storage
- Session Memory

### Development

- Makefile
- Git
- GitHub

---

## 📈 Current Capabilities

✅ Multi-LLM Routing

✅ Local LLM Inference

✅ RAG Pipeline

✅ ChromaDB Vector Search

✅ Source-Aware Retrieval

✅ LangGraph Orchestration

✅ Persistent Conversation Memory

✅ Tool Calling

✅ FastAPI Backend

✅ Streamlit UI

✅ Session-Based Context

✅ PDF & Text Document Ingestion

✅ Dynamic Model Selection

✅ Makefile-Based Development Workflow


---

## 🔮 Upcoming Roadmap

### Phase 6

- Hybrid Search (BM25 + Vector Search)
- Reranking Pipeline
- Multi-Agent Collaboration
- Streaming Responses
- Evaluation Framework

### Phase 7

- vLLM Deployment
- GPU Inference
- Distributed Agents
- MCP Integration
- Production Monitoring

---

## 🎯 Learning Outcomes

This project demonstrates:

- Agentic AI Systems
- Multi-LLM Architectures
- Retrieval-Augmented Generation
- Graph-Based Orchestration
- Vector Databases
- Memory Systems
- Local AI Deployment
- Production AI Engineering

---

## 👨‍💻 Author

### Susanta Hazra

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
