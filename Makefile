# ==========================================
# Estudio PolyMind
# ==========================================

.PHONY: api ui ingest test clean

# Start FastAPI
api:
	uvicorn api.app:app --reload --port 8001

# Start Streamlit UI
ui:
	streamlit run ui/app.py

# Ingest documents into ChromaDB
ingest:
	python rag/ingest.py

# Test retriever
test:
	python rag/test_retriever.py

# Clean vector database
clean:
	rm -rf chroma_db

# Rebuild vector database
rebuild:
	rm -rf chroma_db
	python rag/ingest.py

# Run API + UI together (Linux/macOS)
dev:
	uvicorn api.app:app --reload --port 8001 & \
	streamlit run ui/app.py
