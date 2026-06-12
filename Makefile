# ==========================================
# Estudio PolyMind
# Multi-LLM RAG & Agent Orchestration Platform
# ==========================================

.PHONY: install api ui dev ingest rebuild clean test validate help

# ------------------------------------------
# Install dependencies
# ------------------------------------------
install:
	pip install -r requirements.txt

# ------------------------------------------
# FastAPI backend
# ------------------------------------------
api:
	uvicorn api.app:app --reload --port 8001

# ------------------------------------------
# Streamlit UI
# ------------------------------------------
ui:
	streamlit run ui/app.py

# ------------------------------------------
# Run full system (API + UI)
# ------------------------------------------
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

# Clean vector database
clean:
	rm -rf chroma_db

# ==========================================
# EXPERIMENTS / TESTS
# (aligned with your actual structure)
# ==========================================

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

test:
	python experiments/test_retriever.py

# Run all validation tests
validate:
	python experiments/test_retriever.py && \
	python experiments/test_bm25.py && \
	python experiments/test_hybrid.py && \
	python experiments/test_router.py && \
	python experiments/test_langgraph_chunks.py && \
	python experiments/test_pdf.py

# ==========================================
# HELP
# ==========================================
help:
	@echo ""
	@echo "Estudio PolyMind Commands"
	@echo "========================="
	@echo ""
	@echo "Core:"
	@echo "  make install     Install dependencies"
	@echo "  make api         Start FastAPI backend"
	@echo "  make ui          Start Streamlit UI"
	@echo "  make dev         Run full system"
	@echo ""
	@echo "RAG:"
	@echo "  make ingest      Build ChromaDB"
	@echo "  make rebuild     Rebuild ChromaDB"
	@echo "  make clean       Delete ChromaDB"
	@echo ""
	@echo "Experiments:"
	@echo "  make test-*      Run individual tests"
	@echo "  make validate    Run all tests"
