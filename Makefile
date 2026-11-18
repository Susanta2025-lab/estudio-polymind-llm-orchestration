# ==========================================
# Estudio PolyMind
# Multi-LLM RAG & Agent Orchestration Platform
# ==========================================

PYTHON ?= python
LOCAL_LAUNCHER := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))development/local_apps.py

.PHONY: chat-api chat-ui chat-dev docs-init docs-serve

.PHONY: \
	install \
	api \
	ui \
	dev \
	ci \
	ingest \
	rebuild \
	clean \
	router \
	test \
	helm-lint \
	helm-template \
	helm-validate \
	k8s-phase10-create \
	k8s-phase10-build \
	k8s-phase10-load-image \
	k8s-phase10-deploy \
	k8s-phase10-test \
	k8s-phase10-destroy \
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
	pip install --no-deps -r requirements-ml-cpu.txt
	pip install -r requirements.txt

# ==========================================
# APPLICATIONS
# ==========================================

# FastAPI backend
api:
	$(PYTHON) -m uvicorn api.app:app \
	--reload \
	--host 0.0.0.0 \
	--port 8001

# Streamlit UI
ui:
	$(PYTHON) -m streamlit run ui/app.py \
	--server.address 0.0.0.0 \
	--server.port 8501

# Run API + UI together
dev:
	@exec "$(PYTHON)" "$(LOCAL_LAUNCHER)" dev

# Explicit isolated local development; historical api/ui/dev keep their config.
chat-api chat-ui chat-dev:
	@exec "$(PYTHON)" "$(LOCAL_LAUNCHER)" $@

# Export values as data, never interpolate operator paths into shell code.
export DOCS_RUNTIME CHAT_RUNTIME CHAT_CHROMA_PATH CHAT_CORPUS_VERSION CHAT_HF_HOME CHAT_MODEL_ARTIFACT_DIR
docs-init docs-serve:
	@exec "$(PYTHON)" "$(LOCAL_LAUNCHER)" $@


# ==========================================
# RAG PIPELINE
# ==========================================

# Ingest documents and publish BM25_CORPUS_VERSION after all upserts succeed
ingest:
	python rag/ingest.py

# Rebuild vector database
rebuild:
	python -m rag.admin reset
	python rag/ingest.py

# Delete vector database
clean:
	python -m rag.admin reset

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

# Automated test suite (does not require Ollama)
test:
	python -m pytest

# Validate the production control-plane chart without requiring a cluster.
helm-lint:
	helm lint deployment/helm/polymind

helm-template:
	helm template polymind deployment/helm/polymind

helm-validate: helm-lint helm-template

k8s-phase10-create:
	deployment/kind/phase10/phase10.sh create

k8s-phase10-build:
	deployment/kind/phase10/phase10.sh build

k8s-phase10-load-image:
	deployment/kind/phase10/phase10.sh load

k8s-phase10-deploy:
	deployment/kind/phase10/phase10.sh deploy

k8s-phase10-test:
	deployment/kind/phase10/phase10.sh smoke

k8s-phase10-destroy:
	deployment/kind/phase10/phase10.sh destroy

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
# DOCKER
# ==========================================

docker-build:
	docker compose build

docker-up:
	docker compose up

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

#=========================================
# GitHub Actions CI/CD
#=========================================

ci:

	make validate && \

	docker compose build

# ==========================================
# HELP
# ==========================================

help:
	@echo ""
	@echo "Estudio PolyMind Commands"
	@echo "========================="
	@echo ""
	@echo "Applications:"
	@echo "  make api              Historical configured API (including repository .env)"
	@echo "  make ui               Historical configured Streamlit frontend"
	@echo "  make dev              Supervise the historical configured API + UI"
	@echo "  make chat-api         Isolated local Ollama API at 127.0.0.1:8001"
	@echo "  make chat-ui          Matching Chat UI at http://127.0.0.1:8501"
	@echo "  make chat-dev         Supervise both Chat services; Ctrl-C stops both"
	@echo "  make docs-init DOCS_RUNTIME=/tmp/NEW-private-directory"
	@echo "                        Initialize a NEW synthetic Documents runtime"
	@echo "  make docs-serve DOCS_RUNTIME=/tmp/NEW-private-directory"
	@echo "                        Serve authenticated Documents at https://localhost:9443"
	@echo "  PYTHON=/path/to/python Select project interpreter (default: python)"
	@echo "  CHAT_RUNTIME          Private directory outside repo (default: /tmp/polymind-chat-UID)"
	@echo "  CHAT_CHROMA_PATH      Existing local index (default: CHAT_RUNTIME/chroma_db)"
	@echo "  CHAT_CORPUS_VERSION   Published index version (default: development)"
	@echo "  CHAT_HF_HOME          Existing offline HF cache (default: ~/.cache/huggingface)"
	@echo "  CHAT_MODEL_ARTIFACT_DIR  Optional existing embedding/reranker artifact directory"
	@echo "  Stop with Ctrl-C. Chat and Documents share 8001/8501; launch separately."
	@echo "  Guide: docs/operations/local_applications.md"
	@echo ""
	@echo "Installation:"
	@echo "  make install          Install dependencies"
	@echo ""
	@echo "RAG Pipeline:"
	@echo "  make ingest           Upsert Chroma documents and publish corpus version"
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
	@echo "  make helm-validate    Lint and render the Helm chart"
	@echo "  make k8s-phase10-*    Run the guarded local Kind validation workflow"
	@echo ""
	@echo "CI:"
	@echo "  make ci								Run local CI pipeline"
	@echo ""
