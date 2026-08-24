# Phase 8F — RAG Data-Plane Externalization & Multi-Replica Readiness

Implement a production-style RAG storage boundary that removes the module-level
local Chroma assumption while preserving backward-compatible local development,
retrieval semantics, API contracts, inference providers, and Redis memory.

The required architecture is:

```text
PolyMind RAG / retrieval
        ↓
VectorStore provider contract
      ↙        ↘
local Chroma   one shared external vector service
```

Evaluate Chroma server/client mode against credible alternatives and choose only
one production backend. Centralize and validate provider, endpoint, collection,
and local-path configuration. Do not connect during module import, silently fall
back, or let API startup reset data. Separate online query access from explicit
offline/admin ingestion and reset, use backend-native idempotent collection
initialization and safe writes, and document concurrency and consistency.

Preserve dense retrieval, BM25, RRF, reranking, source metadata, `/query`, and
NDJSON streaming. Classify BM25 and all remaining process-local state for replica
safety. Add sanitized vector operational errors, request-correlated logs, bounded
Prometheus metrics without content or identifiers, and make `/ready` require the
vector store while `/health` remains process-only.

Core tests must use fakes and cover query success/empty/malformed/failures,
readiness, writes, provider selection/validation, local `CHROMA_PATH`, retrieval
regression, shared-mode construction, composite readiness, safe metrics, and API
regression. CI must remain CPU-only and independent of all live services.

An optional development-only Compose Chroma service may be added with a health
check and intentional persistence; it must not be described as production.
Update `.env.example`, README, and the Phase 8F report. Run pytest, external-cache
compile validation, `git diff --check`, Compose validation, Docker build, relevant
lint/security checks, full diff self-review, and pre-commit review. Do not commit
or push, do not start a later phase, and report exact outcomes and remaining risks.

Out of scope: Kubernetes, Helm, cloud provisioning, multiple production vector
backends, full ingestion orchestration, distributed locking without demonstrated
need, authentication/RBAC platforms, GPU/vLLM installation, and monitoring
platform deployment.
