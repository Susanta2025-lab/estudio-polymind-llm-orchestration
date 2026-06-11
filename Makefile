# ==========================================
# Estudio PolyMind
# Multi-LLM RAG & Agent Orchestration Platform
# ==========================================

.PHONY: \
	install \
	api \
	ui \
	ingest \
	test \
	test-retriever \
	test-bm25 \
	test-hybrid \
	validate \
	clean \
	rebuild \
	dev \
	help

# ------------------------------------------
# Install dependencies
# ------------------------------------------
install:
	pip install -r requirements.txt

# ------------------------------------------
# Start FastAPI Backend
# ------------------------------------------
api:
	uvicorn api.app:app --reload --port 8001

# ------------------------------------------
# Start Streamlit UI
# ------------------------------------------
ui:
	streamlit run ui/app.py

# ------------------------------------------
# Ingest documents into ChromaDB
# ------------------------------------------
ingest:
	python rag/ingest.py

# ------------------------------------------
# Vector Retrieval Test
# ------------------------------------------
test-retriever:
	python rag/test_retriever.py

# ------------------------------------------
# BM25 Retrieval Test
# ------------------------------------------
test-bm25:
	python rag/test_bm25.py

# ------------------------------------------
# Hybrid Retrieval Test
# ------------------------------------------
test-hybrid:
	python rag/test_hybrid.py

# ------------------------------------------
# Legacy Test Alias
# ------------------------------------------
test:
	python rag/test_retriever.py

# ------------------------------------------
# Run all retrieval validations
# ------------------------------------------
validate:
	python rag/test_retriever.py
	python rag/test_bm25.py
	python rag/test_hybrid.py

# ------------------------------------------
# Remove vector database
# ------------------------------------------
clean:
	rm -rf chroma_db

# ------------------------------------------
# Rebuild vector database
# ------------------------------------------
rebuild:
	rm -rf chroma_db
	python rag/ingest.py

# ------------------------------------------
# Run API + UI together
# Linux/macOS
# ------------------------------------------
dev:
	uvicorn api.app:app --reload --port 8001 & \
	streamlit run ui/app.py

# ------------------------------------------
# Help Menu
# ------------------------------------------
help:
	@echo ""
	@echo "Estudio PolyMind Commands"
	@echo "========================="
	@echo ""
	@echo "make install         Install dependencies"
	@echo "make api             Start FastAPI backend"
	@echo "make ui              Start Streamlit UI"
	@echo "make ingest          Ingest documents"
	@echo "make rebuild         Rebuild ChromaDB"
	@echo "make clean           Remove ChromaDB"
	@echo ""
	@echo "Testing"
	@echo "-------"
	@echo "make test-retriever  Test vector search"
	@echo "make test-bm25       Test BM25 search"
	@echo "make test-hybrid     Test hybrid search"
	@echo "make validate        Run all retrieval tests"
	@echo ""
	@echo "Development"
	@echo "-----------"
	@echo "make dev             Start API + Streamlit"
	@echo ""
