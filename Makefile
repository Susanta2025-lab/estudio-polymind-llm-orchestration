# ==========================================
# Estudio PolyMind
# Multi-LLM RAG & Agent Orchestration Platform
# ==========================================

.PHONY: \
	install \
	api \
	ui \
	dev \
	ingest \
	rebuild \
	clean \
	router \
	test \
	validate \
	test-retriever \
	test-bm25 \
	test-hybrid \
	test-router \
	test-langgraph \
	test-pdf \
	help

# ==========================================
# INSTALLATION
# ==========================================

install:
	pip install -r requirements.txt

# ==========================================
# APPLICATIONS
# ==========================================

# FastAPI backend
api:
	uvicorn api.app:app --reload --port 8001

# Streamlit UI
ui:
	streamlit run ui/app.py

# Run API + UI together
dev:
	uvicorn api.app:app --reload --port 8001 & \
	streamlit run ui/app.py

# ==========================================
# RAG PIPELINE
# ==========================================

# Ingest documents into ChromaDB
ingest:
	python rag/ingest.py

# Rebuild vector database
rebuild:
	rm -rf chroma_db
	python rag/ingest.py

# Delete vector database
clean:
	rm -rf chroma_db

# ==========================================
# SEMANTIC ROUTING
# ==========================================

router:
	python experiments/test_router.py

# ==========================================
# EXPERIMENTS / TESTS
# ==========================================

test-stream:
	python experiments/test_streaming.py

test-reranker:
	python experiments/test_reranker.py

test-retriever:
	python experiments/test_retriever.py

test-bm25:
	python experiments/test_bm25.py

test-hybrid:
	python experiments/test_hybrid.py

test-router:
	python experiments/test_router.py

test-langgraph:
	python experiments/test_langgraph_chunks.py

test-pdf:
	python experiments/test_pdf.py

test-eval:
	python experiments/test_router_eval.py

test-retrieval-eval:
	python experiments/test_retrieval_eval.py

# Default test
test:
	python experiments/test_retriever.py

# Run all validation tests
validate:
	python experiments/test_retriever.py && \
	python experiments/test_bm25.py && \
	python experiments/test_hybrid.py && \
	python experiments/test_router.py && \
	python experiments/test_langgraph_chunks.py && \
	python experiments/test_reranker.py && \
	python experiments/test_streaming.py && \
	python experiments/test_pdf.py

# ==========================================
# HELP
# ==========================================

help:
	@echo ""
	@echo "Estudio PolyMind Commands"
	@echo "========================="
	@echo ""
	@echo "Applications:"
	@echo "  make api              Start FastAPI backend"
	@echo "  make ui               Start Streamlit UI"
	@echo "  make dev              Run API + UI"
	@echo ""
	@echo "Installation:"
	@echo "  make install          Install dependencies"
	@echo ""
	@echo "RAG Pipeline:"
	@echo "  make ingest           Build ChromaDB index"
	@echo "  make rebuild          Rebuild ChromaDB index"
	@echo "  make clean            Delete ChromaDB database"
	@echo ""
	@echo "Semantic Routing:"
	@echo "  make router           Test semantic router"
	@echo ""
	@echo "Experiments:"
	@echo "  make test-retriever   Test vector retrieval"
	@echo "  make test-bm25        Test BM25 retrieval"
	@echo "  make test-hybrid      Test hybrid retrieval"
	@echo "  make test-router      Test semantic routing"
	@echo "  make test-langgraph   Test chunking pipeline"
	@echo "  make test-pdf         Test PDF loader"
	@echo "  make test-reranker    Test reranker"
	@echo "  make test-stream      Test streaming"
	@echo ""
	@echo "Validation:"
	@echo "  make test             Run default test"
	@echo "  make validate         Run all tests"
	@echo ""
