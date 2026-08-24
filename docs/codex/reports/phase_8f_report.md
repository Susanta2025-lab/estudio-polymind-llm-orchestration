# Phase 8F — RAG Data-Plane Externalization & Multi-Replica Readiness Report

## 1. Phase Result

`PASS`

The production/shared RAG path no longer depends on module-level local Chroma
state. A lazy provider boundary supports backward-compatible local persistence
and shared Chroma HTTP access, with deterministic tests and a successful live
server validation. The documented BM25 refresh constraint does not prevent a
controlled replica rollout, but it is a deliberate future improvement.

## 2. RAG Data-Plane Architecture

`VectorStore` is the narrow read contract: normalized similarity search,
document snapshot reads for BM25, readiness, and lifecycle. `MutableVectorStore`
adds only upsert and reset. `ChromaVectorStore` owns Chroma collection/result
details. `vector_store_factory` selects `chroma_local` or `chroma_http`, lazily
creates one lock-protected client per worker, and closes it on application
shutdown where the client exposes lifecycle behavior.

Retriever and BM25 code consume normalized provider records; neither constructs
a Chroma client. The deleted `rag/vectordb.py` module-level `PersistentClient`,
hard-coded path, and collection global no longer exist. `CHROMA_PATH` is now used
by the local factory. External client creation is deferred until readiness or the
first RAG operation, so import/startup succeeds during a vector outage.

## 3. Backend Decision

Chroma server/client mode was selected for shared production-style access. The
already pinned Chroma 1.5.9 package supplies both adapters, backend-native
get-or-create, HTTP connection reuse, metadata, embeddings, distance semantics,
and a matching official image. This minimizes migration and image impact while
moving state out of API replicas.

Qdrant has a strong vector API and operational story but would add a client and
data migration without a Phase 8F retrieval requirement Chroma cannot meet.
pgvector would add PostgreSQL schema/migration/query work and is heavier for the
current collection-shaped workload. Elasticsearch/OpenSearch was disproportionate
and explicitly disfavored. Only Chroma HTTP is implemented as a shared backend.

## 4. Query vs Ingestion Separation

Online retrieval uses `get_vector_store`; it performs similarity search and the
BM25 source snapshot. Mutation is reached explicitly through
`get_vector_store_admin`, `rag/ingest.py`, or `python -m rag.admin reset`.
Serving startup never ingests or resets. Makefile rebuild/clean targets now call
the explicit admin operation instead of deleting a local directory.

Ingestion uses stable UUIDv5 IDs derived from source, chunk position, and content,
so retries and concurrent copies converge through Chroma upsert instead of
creating random duplicates. Reset remains an intentional destructive admin
command and is not exposed as an API endpoint.

## 5. Retrieval Compatibility

The embedding model and query embedding path are unchanged. Dense distances are
still converted to `max(0, 1-distance)`, rounded, filtered, deduplicated by
source/chunk, and sorted as before. BM25 tokenization/ranking, RRF fusion and its
dynamic threshold, cross-encoder inputs, reranking, and public source fields are
unchanged. Tests cover normalized dense results, BM25 provider snapshots, exact
RRF behavior, reranker inputs, and source metadata.

`/query` response fields and `/query/stream` NDJSON framing remain unchanged.
Only `/ready` intentionally gains a `vector_store` component. Vector failures
receive a sanitized HTTP 503 or NDJSON error event.

## 6. Multi-Replica Semantics

With `chroma_http`, all replicas address one server/collection and completed
upserts are visible through that shared collection. Chroma supports concurrent
reads and backend-managed upserts. Collection initialization uses its atomic
get-or-create API rather than a check-then-create sequence. Stable record IDs make
same-input concurrent ingestion idempotent.

There is no distributed transaction across a complete multi-document ingestion,
so queries may observe the collection while a batch is progressing. No stronger
snapshot guarantee is claimed. Local persistence remains explicitly unsuitable
for horizontally scaled replicas.

## 7. Readiness & Failure Behavior

`/health` remains process-only. `/ready` now requires inference, memory, and
vector readiness; vector failure makes global readiness 503 under the chosen
simple policy. The Chroma check uses heartbeat plus collection count and does not
embed or run semantic search. Process import/startup remains possible while an
external service is down.

Errors are normalized to `vector_unreachable`, `vector_timeout`,
`vector_protocol`, `collection_unavailable`, `vector_query_failure`, and
`vector_write_failure`. Backend messages, URLs, content, and credentials are not
returned. HTTP and streaming logs include the Phase 8C request ID and category.
No local fallback occurs in shared mode.

## 8. BM25 & Other Replica-State Review

`SAFE FOR REPLICAS`

- Dense retrieval with all replicas configured for the same Chroma HTTP service.
- Stateless embedding, RRF, reranking, routing, and inference behavior.
- Redis conversation memory when replicas share the same Redis service.

`REQUIRES SHARED STORAGE`

- Mutable vector data in production: use `chroma_http`, not `chroma_local`.
- Conversation memory in production: use Redis, not file memory.

`PROCESS-LOCAL BUT ACCEPTABLE`

- One lazily reused Chroma client/connection pool per worker.
- Immutable BM25 snapshot when replicas are restarted after a completed indexing
  workflow and therefore build from the same collection version.
- Prometheus registries when each worker is scraped and externally aggregated.

`FUTURE RISK`

- BM25 does not automatically refresh after live ingestion. A long-running mixed
  fleet can have different sparse snapshots until restart/rollout.
- Multi-document ingestion is not an atomic collection-version publication.

## 9. Observability

The phase adds `vector_operations_total`,
`vector_operation_duration_seconds`, `vector_errors_total`,
`vector_readiness_checks_total`, and `vector_readiness_duration_seconds`.
Labels are bounded to provider, fixed operation, outcome, and normalized error
category. Query/document text, source names, collection names, document IDs,
request IDs, and session IDs are excluded. Existing application/RAG route metrics
continue to cover end-to-end requests without duplicate route instrumentation.

## 10. Docker / Local Development

The default remains `chroma_local` using the configured `CHROMA_PATH`. An optional
`vector` Compose profile runs the official pinned Chroma 1.5.9 image, uses a
named persistent volume, publishes no host port, and has a validated Bash TCP
health check. The API can select it with `VECTOR_STORE_PROVIDER=chroma_http` and
the Compose service hostname.

This profile is development-only. Production means independently operated shared
Chroma with network isolation, authentication/TLS as appropriate, persistence,
backups, and availability controls. The local profile is unauthenticated and is
not presented as a production deployment.

## 11. Files Changed

Modified:

- `.env.example`
- `Makefile`
- `README.md`
- `api/app.py`
- `config/settings.py`
- `docker-compose.yml`
- `experiments/test_langgraph_chunks.py`
- `graph/streaming.py`
- `llm/metrics.py`
- `rag/bm25.py`
- `rag/ingest.py`
- `rag/retriever.py`
- `tests/unit/test_api_reliability.py`
- `tests/unit/test_streaming_orchestration.py`

Added:

- `docs/codex/prompts/phase_8f.md`
- `docs/codex/reports/phase_8f_report.md`
- `rag/admin.py`
- `rag/chroma_store.py`
- `rag/vector_store.py`
- `rag/vector_store_factory.py`
- `tests/unit/test_retrieval_regression.py`
- `tests/unit/test_vector_store.py`

Deleted:

- `rag/vectordb.py`

`AGENTS.md` is also modified in the working tree, but that was a pre-existing
user-owned change and was not edited during Phase 8F implementation.

## 12. Dependencies

No dependency was added or changed. The existing `chromadb==1.5.9` client is
reused for local and HTTP modes. The optional service image is pinned to the same
version. This avoids additional Python/image weight and migration machinery.

## 13. Tests Added / Updated

Vector contract tests cover successful/empty queries, malformed shapes,
collection absence, timeout, connection failure, readiness, upsert normalization,
local/shared factory selection, actual `CHROMA_PATH` use, SSL/host/port forwarding,
invalid/incomplete configuration, sanitization, and metric cardinality.

Retrieval regressions cover dense normalization/deduplication/source metadata,
BM25 snapshot construction, unchanged RRF filtering/scores, reranker inputs, and
source compatibility. API tests cover three-component readiness and independent
liveness. Streaming tests cover the sanitized vector NDJSON error. The factory
test proves external mode creates an HTTP rather than persistent client only when
explicitly requested; no live service is needed in CI.

## 14. Validation Results

- `pytest`: passed, **122 passed** on the final tree.
- Compile validation: `PYTHONPYCACHEPREFIX=/tmp/polymind-phase8f-final-pycache python -m compileall -q .` passed.
- `git diff --check`: passed with no output.
- Docker Compose validation: default and `--profile vector` configs passed.
- Docker build: `docker build .` passed with cache; `docker compose build api` also passed with cache. No `--no-cache` was used.
- Optional live vector integration: passed against Chroma 1.5.9; health became healthy and readiness, upsert, similarity query, and exact test-collection reset succeeded. The scoped container/network were removed afterward; the named development volume was retained per Docker safety rules.
- Linting: no separately configured lint command/tool was found.
- Security scan: focused secret/key/debug/TODO/content-label scan and tracked-file review passed; the ignored pre-existing `.env` and bytecode caches were not modified or added.

## 15. Implementation Self-Review

The complete diff and every RAG consumer were reviewed. Findings fixed were:
factory construction exceptions initially could escape unsanitized; lazy singleton
construction needed thread protection; random ingestion IDs made retries create
duplicates; streaming vector failures lacked their own request-correlated category;
and the first Compose health command assumed Python existed in the Chroma image.
All were corrected and retested.

The final architecture has no provider leakage into retrieval, no module-import
client, no unsafe fallback, no startup mutation/reset, no unbounded vector label,
and no query/source/API format regression. The phase remained a Chroma boundary
externalization rather than becoming a broader search-platform migration.

## 16. Pre-Commit Review

The working tree contains the scoped Phase 8F implementation, tests,
configuration, README and artifacts plus the pre-existing user `AGENTS.md` edit.
No runtime `.env`, secret, credential, private key, hard-coded machine path,
generated artifact, new TODO, debug breakpoint, unrelated dependency, or public
reset endpoint was introduced. Existing ignored local `.env`/bytecode files were
not staged or changed.

Compatibility review confirms `/query`, `/query/stream`, NDJSON event framing,
source attribution, Ollama/OpenAI-compatible inference, Redis/file memory,
routing, and tools remain intact. Docker build, Compose profile, and live Chroma
checks passed. The remaining warning is the documented BM25 refresh requirement.

No commit was created.
No push was performed.

## 17. Documentation

README documents the contract, local/shared configuration, backend decision,
query/admin separation, readiness, failure behavior, metrics, Chroma concurrency,
BM25 consistency, Compose workflow, production separation, and security boundary.
`.env.example` lists all vector settings. A clean Phase 8F prompt and this report
are stored under `docs/codex/` without modifying prior phase artifacts.

## 18. Remaining Risks / Technical Debt

### Phase 8F concerns

- BM25 snapshots require replica restart/rollout after ingestion; there is no
  collection-version-triggered refresh yet.
- A multi-document indexing run is incrementally visible rather than atomically
  published as one version.
- Chroma client/server request timeout customization is not exposed by the pinned
  synchronous client API used here; timeout exceptions are normalized when the
  client raises them, but deployers should also enforce infrastructure timeouts.
- Production Chroma durability, HA, backups, TLS/authentication, and upgrades are
  external operational responsibilities.

### Deliberately deferred infrastructure work

- Kubernetes/Helm/cloud or managed vector provisioning.
- Versioned blue/green collections and ingestion orchestration.
- Distributed locking, multi-tenancy, RBAC, and service-mesh/API-gateway controls.
- Prometheus/Grafana/alerting/tracing deployment and multiprocess aggregation.

## 19. Next-Phase Readiness

`READY WITH CONDITIONS`

The data-plane boundary is ready for shared-service replica deployment provided
production uses `chroma_http`, Redis memory, and a controlled ingest-then-rollout
procedure for BM25 consistency. The most appropriate next phase is deployment
topology and operational hardening for the already externalized inference,
memory, and vector services, with BM25 snapshot version/refresh design included;
it should not begin automatically.
