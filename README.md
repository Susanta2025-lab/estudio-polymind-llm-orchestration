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
                    User Query
                         │
                         ▼
                    FastAPI API
                         │
                         ▼
                    LangGraph
                         │
              ┌──────────┼──────────┐
              │          │          │
              ▼          ▼          ▼
         Direct LLM     RAG       Tools
              │          │          │
              ▼          ▼          ▼
         Model Router   ChromaDB   Utilities
              │
              ▼
   Mistral / Qwen / Gemma / Phi
              │
              ▼
       Persistent Memory
              │
              ▼
         API Response
```

---

## 📂 Project Structure

```text
estudio-polymind-llm-orchestration/
│
├── api/
│   └── app.py
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
│   ├── vectordb.py
│   └── loaders/
│
├── data/
│   └── docs/
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
├── chroma_db/
│
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

**Susanta Hazra**

AI Engineer | Data Scientist | Generative AI Enthusiast

Building production-ready AI systems with LLMs, RAG, Agents, and MLOps.
