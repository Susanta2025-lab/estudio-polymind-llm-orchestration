# 🧠 Estudio PolyMind

### Multi-LLM RAG & Orchestration Platform

> Local AI infrastructure for Retrieval-Augmented Generation (RAG), multi-model orchestration, vector search, and agentic workflows using open-source LLMs.

---

## 🚀 Overview

Estudio PolyMind is a production-style local AI platform that combines:

* ⚡ Open-source LLMs (Mistral, Qwen, Gemma, Phi)
* 🧠 Retrieval-Augmented Generation (RAG)
* 🔍 Vector databases with semantic search
* 🔄 LangGraph orchestration workflows
* 🌐 FastAPI backend APIs
* 🐳 Docker-ready deployment
* 🖥️ Local inference with Ollama / vLLM

The project is designed as a modular LLM engineering system that simulates real-world AI infrastructure and agent orchestration pipelines.

---

# ✨ Features

## 🤖 Multi-LLM Support

* Mistral
* Qwen
* Gemma
* Phi
* Extensible architecture for additional models

## 🧠 RAG Pipeline

* Document ingestion
* Embedding generation
* Semantic retrieval
* Context-aware response generation

## 🔍 Vector Database Integration

* ChromaDB persistent storage
* Semantic similarity search
* Efficient retrieval pipelines

## ⚙️ AI Orchestration

* LangGraph workflow orchestration
* Dynamic routing pipelines
* Multi-step reasoning flows
* Agentic execution support

## 🌐 API Infrastructure

* FastAPI backend
* REST endpoints
* Swagger documentation
* Modular API architecture

## 🐳 Deployment Ready

* Docker support
* Ollama local serving
* vLLM compatibility
* Scalable architecture

---

# 🏗️ System Architecture

```text
# 🏗️ System Architecture

                 ┌────────────────────┐
                 │     User Query     │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │    FastAPI API     │
                 │   (api/app.py)     │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │   LangGraph Flow   │
                 │ (Orchestration)    │
                 └─────────┬──────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   ┌────────────┐   ┌────────────┐   ┌────────────┐
   │ Retriever  │   │ LLM Router │   │ Tool Agent │
   │  Pipeline  │   │ Multi-LLM  │   │ Extensible │
   └─────┬──────┘   └─────┬──────┘   └─────┬──────┘
         │                │                │
         ▼                ▼                ▼
 ┌────────────────────────────────────────────────┐
 │               RAG PIPELINE                     │
 ├────────────────────────────────────────────────┤
 │ PDF/TXT Loaders                               │
 │ Recursive Smart Chunking                      │
 │ Sentence-Transformer Embeddings               │
 │ ChromaDB Vector Storage                       │
 │ Semantic Similarity Retrieval                 │
 │ Metadata + Source Attribution                 │
 └────────────────────────────────────────────────┘
         │
         ▼
 ┌────────────────────────────────────────────────┐
 │        Open-Source LLM Runtime Layer           │
 ├────────────────────────────────────────────────┤
 │ Ollama                                         │
 │ Mistral • Qwen • Gemma • Phi                  │
 │ Local CPU-Based Inference                      │
 └────────────────────────────────────────────────┘
         │
         ▼
 ┌────────────────────────────────────────────────┐
 │            Context-Aware AI Response           │
 └────────────────────────────────────────────────┘
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
│   └── langgraph_flow.py
│
├── data/
│   └── docs/
│       ├── ai_notes.txt
│       ├── transformers.pdf
│       └── sample_docs/
│
├── chroma_db/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🛠️ Tech Stack

| Category      | Technologies              |
| ------------- | ------------------------- |
| LLM Runtime   | Ollama, vLLM              |
| Models        | Mistral, Qwen, Gemma, Phi |
| Backend       | FastAPI                   |
| Vector DB     | ChromaDB                  |
| Embeddings    | Sentence Transformers     |
| Orchestration | LangGraph                 |
| Deployment    | Docker                    |
| Language      | Python                    |

---

# ⚡ Quick Start

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration.git
cd estudio-polymind-llm-orchestration
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

---

## 4️⃣ Pull Open-Source Models

```bash
ollama pull mistral
ollama pull qwen2.5
ollama pull gemma
ollama pull phi3
```

---

## 5️⃣ Ingest Documents into Vector Database

```bash
python -m rag.ingest
```

---

## 6️⃣ Start FastAPI Server

```bash
uvicorn api.app:app --reload
```

---

## 7️⃣ Open API Docs

```text
http://127.0.0.1:8000/docs
```

---

# 🔥 Example Query

```json
{
  "query": "What is Retrieval-Augmented Generation?"
}
```

---

# 📈 Current Development Phases

## ✅ Phase 1 — Local LLM Infrastructure

* Ollama setup
* Mistral integration
* FastAPI backend
* API endpoints

## ✅ Phase 2 — RAG Pipeline

* Embedding generation
* ChromaDB vector database
* Semantic retrieval
* Context-aware generation

## 🚧 Phase 3 — LangGraph Orchestration

* Agent workflows
* Dynamic routing
* Multi-step reasoning
* Tool calling

## 🔮 Planned Features

* PDF ingestion
* Hybrid search
* Streaming responses
* Multi-agent collaboration
* Memory systems
* Docker Compose deployment
* React / Streamlit frontend
* Evaluation pipelines

---

# 🎯 Learning Objectives

This project demonstrates:

* LLM Engineering
* Retrieval-Augmented Generation (RAG)
* Vector Databases
* AI Agent Orchestration
* API Development
* Local AI Deployment
* Production-style ML Architecture
* Open-source AI Infrastructure

---

# 📌 Why This Project Matters

PolyMind RAG Studio is designed to simulate modern enterprise AI systems where:

* multiple LLMs collaborate,
* vector databases provide external memory,
* orchestration systems manage workflows,
* and APIs expose scalable AI services.

This architecture reflects real-world AI engineering patterns used in modern GenAI products.

---

# 🤝 Future Extensions

* Add Redis caching
* Integrate PostgreSQL
* Add observability with LangSmith
* Add GPU inference pipelines
* Deploy with Kubernetes
* Add authentication & user memory
* Add MCP tool integrations

---

# 📜 License

MIT License

---

# ⭐ Support

If you found this project useful:

* ⭐ Star the repository
* 🍴 Fork the project
* 🧠 Explore open-source AI systems
* 🚀 Build your own agentic workflows
