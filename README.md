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

### Hybrid Retrieval

PolyMind combines:

- ChromaDB Semantic Search
- BM25 Keyword Search

to improve retrieval quality and reduce missed document matches.

---

## 🏗 System Architecture

### High-Level Component Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE LAYER                          │
├────────────────────────────────┬────────────────────────────────────────┤
│                                │                                        │
│   Streamlit Web UI             │        FastAPI REST API               │
│   (Port: 8501)                 │        (Port: 8000)                   │
│  ┌──────────────────────────┐  │   ┌──────────────────────────────┐   │
│  │ • Query Input            │  │   │ • POST /query                │   │
│  │ • Document Upload        │  │   │ • GET /memory/{session_id}   │   │
│  │ • Chat History Display   │  │   │ • GET /                      │   │
│  │ • Model Selection        │  │   │ • Response Serialization     │   │
│  │ • Settings Management    │  │   │ • OpenAPI Documentation      │   │
│  └──────────────────────────┘  │   └──────────────────────────────┘   │
│                                │                                        │
└────────────────────────────────┼────────────────────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  REQUEST ROUTER LAYER   │
                    │                         │
                    │ • Session Management    │
                    │ • Request Validation    │
                    │ • Context Preparation   │
                    └────────────┬────────────┘
                                 │
        ┌────────────────────────▼────────────────────────────┐
        │      LANGGRAPH ORCHESTRATION ENGINE                 │
        │                                                     │
        │  ┌────────────────────────────────────────────┐    │
        │  │        GRAPH STATE MANAGEMENT              │    │
        │  │  (GraphState with Messages & Context)      │    │
        │  └────────────┬───────────────────────────────┘    │
        │               │                                     │
        │       ┌───────▼────────┐                           │
        │       │  ROUTER NODE   │                           │
        │       │  (Intent       │                           │
        │       │   Detection)   │                           │
        │       └───────┬────────┘                           │
        │               │                                     │
        │       ┌───────▼──────────────┐                     │
        │       │ MODEL ROUTER NODE    │                     │
        │       │ (Route Decision)     │                     │
        │       └───────┬──────────────┘                     │
        │               │                                     │
        │    ┌──────────┼──────────┐                         │
        │    │          │          │                         │
        │    ▼          ▼          ▼                         │
        │  ┌────┐   ┌──────┐   ┌──────┐                      │
        │  │RAG │   │DIRECT│   │TOOL  │                      │
        │  │NODE│   │ LLM  │   │NODE  │                      │
        │  │    │   │ NODE │   │      │                      │
        │  └────┘   └──────┘   └──────┘                      │
        └────────────────────────────────────────────────────┘
         │                    │                      │
         │                    │                      │
         ▼                    ▼                      ▼
    ┌─────────────┐    ┌────────────┐    ┌──────────────────┐
    │ RAG PIPELINE│    │ OLLAMA LLM │    │ TOOL EXECUTION   │
    │             │    │ INFERENCE  │    │                  │
    │ ┌─────────┐ │    │            │    │ • Calculator     │
    │ │Retriever│ │    │ • Mistral  │    │ • Date/Time      │
    │ │(Query   │ │    │ • Qwen     │    │ • Extensible     │
    │ │Parser)  │ │    │ • Gemma    │    │                  │
    │ └────┬────┘ │    │ • Phi      │    └──────────────────┘
    │      │      │    │            │           │
    │ ┌────▼────┐ │    └────────────┘           │
    │ │Embedding│ │           │                 │
    │ │Generation│    │                 │
    │ └────┬────┘ │    │                 │
    │      │      │    │                 │
    │ ┌────▼─────────────────────────────┐
    │ │ ChromaDB + BM25 Retrieval        │
    │ │  • Vector Search                 │
    │ │  • Keyword Search (BM25)         │
    │ │  • Hybrid Combination            │
    │ │  • Relevance Ranking             │
    │ └────┬────────────────────────────┘
    │      │                             │
    │ ┌────▼──────────────────────┐      │
    │ │ Retrieved Documents       │      │
    │ │ with Metadata & Scores    │      │
    │ └────┬──────────────────────┘      │
    │      │                             │
    └──────┴──────────────────────────────┘
           │              │               │
           └──────────────┼───────────────┘
                          │
                ┌─────────▼──────────┐
                │ RESPONSE GENERATION│
                │ (LLM Inference)    │
                └────────┬───────────┘
                         │
            ┌────────────▼────────────┐
            │ POST-PROCESSING LAYER   │
            │  • Format Normalization │
            │  • Source Attribution   │
            │  • Metadata Enrichment  │
            └────────┬─────────────────┘
                     │
         ┌───────────▼────────────┐
         │  MEMORY PERSISTENCE    │
         │  • Chat History Store  │
         │  • Session Context     │
         │  • JSON Storage        │
         └───────────┬────────────┘
                     │
         ┌───────────▼────────────┐
         │ RESPONSE TRANSMISSION  │
         │ (API/UI Output)        │
         └───────────────────────┘
```

### Execution Flow Details

#### **1. Request Entry Points**

- **FastAPI Endpoint**: `POST /query` - Receives query and session_id
- **Streamlit UI**: Direct graph invocation through web interface
- **Memory Retrieval**: `GET /memory/{session_id}` - Fetches conversation history

#### **2. Router Node** 
- Identifies query intent
- Extracts entities and context
- Determines if context is needed
- Passes intent classification to next node

#### **3. Model Router Node** (Conditional Logic)
Decision tree that determines execution path:
- **RAG Path**: For knowledge-base dependent queries
- **Direct LLM Path**: For general conversation and reasoning
- **Tool Path**: For calculable/utility queries

#### **4. Parallel Processing Paths**

**RAG Path:**
1. Query parsing and preprocessing
2. Embedding generation via Sentence Transformers
3. ChromaDB semantic search + BM25 keyword search
4. Hybrid ranking and deduplication
5. Context-augmented prompt generation
6. LLM inference with retrieved documents

**Direct LLM Path:**
1. Session context retrieval
2. Prompt construction from conversation history
3. Direct model inference
4. Response formatting

**Tool Path:**
1. Tool identification and parameter extraction
2. Tool execution (Calculator, DateTime)
3. Result formatting and response generation

#### **5. Response Consolidation**
- Unified response format with metadata
- Source attribution and scoring
- Memory persistence
- Output serialization

---

## 📂 Project Structure

```
estudio-polymind-llm-orchestration/
│
├── 📁 api/                              # FastAPI Backend Application
│   └── app.py                           # Main FastAPI server
│       ├── Health check endpoint (GET /)
│       ├── Query processing (POST /query)
│       ├── Memory retrieval (GET /memory/{session_id})
│       ├── Request/Response models
│       ├── Logging integration
│       └── Performance tracking
│
├── 📁 ui/                               # Streamlit User Interface
│   ├── app.py                           # Streamlit application
│   │   ├── Chat interface
│   │   ├── Query input handling
│   │   ├── Response rendering
│   │   ├── Document upload/ingestion UI
│   │   ├── Session management
│   │   ├── Model selection dropdown
│   │   └── Conversation history display
│   └── assets/
│       └── susanta.png                  # Author profile image
│
├── 📁 graph/                            # LangGraph Workflow Orchestration
│   ├── langgraph_flow.py               # Graph definition & compilation
│   │   ├── StateGraph initialization
│   │   ├── Node registration
│   │   ├── Edge definitions
│   │   ├── Conditional routing logic
│   │   ├── Entry/finish point setup
│   │   └── Graph compilation
│   ├── nodes.py                        # Node implementations
│   │   ├── router_node()
│   │   │   └── Intent detection & context extraction
│   │   ├── model_router_node()
│   │   │   └── Route decision (rag/direct/tool)
│   │   ├── direct_llm_node()
│   │   │   └── Direct model inference
│   │   ├── rag_node()
│   │   │   └── Retrieval-augmented generation
│   │   └── tool_node()
│   │       └── Tool execution handler
│   └── state.py                        # GraphState schema definition
│       ├── Message history tracking
│       ├── Route state management
│       ├── Intermediate results storage
│       ├── Context variables
│       └── Source attribution
│
├── 📁 llm/                              # LLM Integration & Routing
│   ├── models.py                       # LLM model definitions
│   │   ├── Model configurations
│   │   ├── Capability mappings
│   │   ├── Parameter settings
│   │   └── Model metadata
│   ├── ollama_client.py                # Ollama integration client
│   │   ├── Connection management
│   │   ├── Model loading
│   │   ├── Inference execution
│   │   ├── Streaming support
│   │   └── Error handling
│   └── router.py                       # LLM routing logic
│       ├── Model selection algorithm
│       ├── Query-to-model mapping
│       ├── Load balancing
│       └── Fallback mechanisms
│
├── 📁 rag/                              # Retrieval-Augmented Generation Pipeline
│   ├── chunking.py                     # Document chunking strategies
│   │   ├── Semantic chunking
│   │   ├── Fixed-size chunking
│   │   ├── Overlap configuration
│   │   └── Chunk optimization
│   ├── embeddings.py                   # Embedding generation layer
│   │   ├── Sentence Transformers wrapper
│   │   ├── Batch embedding processing
│   │   ├── Embedding caching
│   │   └── Dimension handling
│   ├── ingest.py                       # Main ingestion orchestrator
│   │   ├── Multi-format support
│   │   ├── Document validation
│   │   ├── Progress tracking
│   │   ├── Error recovery
│   │   └── Batch processing
│   ├── retriever.py                    # Retrieval execution engine
│   │   ├── Query embedding generation
│   │   ├── ChromaDB vector search
│   │   ├── Duplicate deduplication
│   │   ├── Score calculation (1 - distance)
│   │   ├── Relevance filtering
│   │   └── Results ranking
│   ├── test_retriever.py               # Retriever unit tests
│   │   ├── Search accuracy validation
│   │   ├── Score calibration tests
│   │   └── Edge case handling
│   ├── vectordb.py                     # ChromaDB wrapper layer
│   │   ├── Collection management
│   │   ├── Document storage
│   │   ├── Query execution
│   │   ├── Metadata handling
│   │   └── Persistence management
│   └── loaders/                        # Document format loaders
│       ├── pdf_loader.py               # PDF document processing
│       │   ├── Text extraction
│       │   ├── Metadata parsing
│       │   ├── Multi-page handling
│       │   └── OCR support (optional)
│       └── text_loader.py              # Text file processing
│           ├── Plain text ingestion
│           ├── Encoding detection
│           └── Format normalization
│
├── 📁 data/                             # Sample & Training Data
│   └── docs/                            # Reference documents for RAG
│       ├── ai_notes.text                # AI concepts reference
│       ├── LangGraph_Documentation.pdf  # Framework documentation
│       ├── original_rag_paper.pdf       # Foundational RAG research
│       ├── rag_survey.pdf               # RAG techniques survey
│       ├── rag_using_llm.pdf            # RAG implementation guide
│       └── information_retrieval_...    # Information retrieval fundamentals
│
├── 📁 memory/                           # Conversation Memory Management
│   ├── memory_store.py                 # Memory store implementation
│   │   ├── Session-based storage
│   │   ├── History persistence
│   │   ├── Context retrieval
│   │   ├── Cleanup policies
│   │   ├── JSON serialization
│   │   └── Multi-session support
│   └── chat_history.json               # Persistent storage file
│       ├── JSON-based conversation history
│       ├── Multi-session organization
│       └── Metadata tracking
│
├── 📁 tools/                            # Extensible Tool System
│   ├── calculator.py                   # Mathematical calculator tool
│   │   ├── Arithmetic operations
│   │   ├── Expression parsing
│   │   ├── Error handling
│   │   └── Result formatting
│   └── datetime_tool.py                # Date/time utility tool
│       ├── Current date/time retrieval
│       ├── Timezone handling
│       ├── Date arithmetic operations
│       └── Format conversion
│
├── 📁 utils/                            # Utility Modules
│   └── logger.py                       # Centralized logging configuration
│       ├── Log level configuration
│       ├── Output formatting
│       ├── File logging
│       ├── Console output
│       ├── Request logging
│       └── Performance metrics
│
├── 📁 experiments/                      # Experimental Testing & Prototyping
│   ├── test_bm25.py                    # BM25 keyword search testing
│   ├── test_hybrid.py                  # Hybrid retrieval testing
│   ├── test_langgraph_chunks.py        # LangGraph chunking experiments
│   ├── test_pdf.py                     # PDF ingestion testing
│   └── test_retriever.py               # Retriever evaluation
│
├── 📁 media/                            # Screenshots & Visualizations
│   ├── streamlit_ui.png                # Streamlit interface screenshot
│   ├── swagger_ui.png                  # FastAPI Swagger documentation
│   ├── model_routing.png               # Model selection visualization
│   └── rag_query.png                   # RAG query results example
│
├── 📁 chroma_db/                        # ChromaDB Vector Storage (auto-created)
│   │                                    # Runtime-generated directory
│   └── [Collection data files]         # Persisted embeddings & metadata
│
├── .gitignore                           # Git ignore patterns
├── Makefile                             # Development automation commands
│   ├── make api              → Start FastAPI server
│   ├── make ui               → Launch Streamlit UI
│   ├── make ingest           → Run document ingestion
│   ├── make test             → Execute test suite
│   └── Other development targets
│
├── requirements.txt                    # Python dependencies
│   ├── Core Frameworks
│   │   ├── fastapi==0.x.x              # Web framework
│   │   ├── streamlit==1.x.x            # UI framework
│   │   ├── langgraph==0.x.x            # Graph orchestration
│   │   └── langchain==0.x.x            # LLM utilities
│   ├── LLM Integration
│   │   ├── ollama==0.x.x               # Ollama client
│   │   ├── transformers==4.x.x         # HuggingFace models
│   │   └── sentence-transformers==2.x.x # Embedding models
│   ├── Vector Database
│   │   └── chromadb==0.x.x             # Vector storage
│   ├── Data Processing
│   │   ├── pydantic==2.x.x             # Data validation
│   │   ├── pypdf==3.x.x                # PDF parsing
│   │   └── python-dotenv==1.x.x        # Environment variables
│   └── Utilities
│       ├── numpy==1.x.x                # Numerical computing
│       ├── scipy==1.x.x                # Scientific computing
│       └── python-dateutil==2.x.x      # Date utilities
│
└── README.md                            # Project documentation (this file)
```

### Directory Usage Guide

#### **api/** - FastAPI REST Server
Entry point for external integrations. Manages HTTP request/response lifecycle, validation, and integration with the LangGraph orchestrator.

#### **ui/** - Streamlit Web Application
Interactive user interface for chat, document management, and configuration. Directly invokes the LangGraph workflow without HTTP overhead.

#### **graph/** - LangGraph Orchestration Core
The heart of the system - defines the workflow DAG with multiple execution paths. Manages state transitions and conditional routing.

#### **llm/** - LLM Integration Layer
Abstracts Ollama interaction and model selection logic. Ensures consistent inference interface across different models.

#### **rag/** - Retrieval-Augmented Generation Pipeline
Complete implementation of the RAG lifecycle from document ingestion through retrieval and ranking. Includes hybrid search combining vector similarity and keyword matching.

#### **memory/** - Persistent Conversation State
Maintains user sessions and conversation history. Enables multi-turn interactions with context continuity.

#### **tools/** - Extensible Tool System
Plugin architecture for adding new capabilities (Calculator, DateTime, etc.). Easy to extend with custom tools.

#### **experiments/** - Research & Development
Isolated testing ground for new features like BM25 search, hybrid retrieval optimization, and LangGraph workflow variations.

#### **media/** - Demonstration Assets
Visual documentation of system capabilities and user interface examples.

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
