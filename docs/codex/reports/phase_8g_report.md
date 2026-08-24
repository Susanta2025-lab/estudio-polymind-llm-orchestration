# Phase 8G — Production Deployment Topology and Operational Hardening Report

## 1. Phase Result

`PASS`

Phase 8G formalizes PolyMind as the application/control plane for separately
operated inference, conversation-memory, and vector services. Static production
configuration is validated early, temporary dependency failure leaves the process
alive but unready, serving Chroma access is query-only, and BM25 now has an
explicit deterministic rollout/version contract.

## 2. Final Deployment Topology

```text
External clients
      |
PolyMind API replicas (FastAPI / LangGraph / RAG control plane)
      |----------------------|----------------------|
      v                      v                      v
External OpenAI-         Shared Redis          Shared Chroma HTTP
compatible inference    conversation state    vectors + corpus version

Controlled ingestion/admin -> Shared Chroma -> publish corpus version
                                      -> controlled API replica rollout
```

The repository contains no Kubernetes, cloud provisioning, vLLM runtime, GPU
runtime, Prometheus server, or distributed data-service lifecycle management.

## 3. Service Boundaries

PolyMind owns FastAPI, LangGraph, semantic routing, provider selection, RAG
orchestration, request correlation, readiness, and process-local metrics. The
inference provider owns model serving and OpenAI-compatible protocol behavior;
Redis owns shared ordered conversation state; Chroma owns shared vector records
and corpus publication metadata. Ingestion/admin is a separate command workflow
that creates collections, upserts deterministic records, resets explicitly, and
publishes completed corpus versions. Normal serving does none of those mutations.

## 4. Startup & Shutdown Semantics

Settings and provider objects are created without remote calls. Embedding model
and semantic-route embedding initialization were made lazy so module import does
not download or construct a model. FastAPI lifespan attempts one BM25 build from
the configured published version. A vector outage or mismatch is logged as a
bounded category and does not abort process startup.

Shutdown clears the local BM25 snapshot, closes Redis, closes vector-store-owned
HTTP resources, and closes the OpenAI-compatible session owned by its provider.
Ollama's default module client has no owned pool to close. There are no startup
ingestion/reset actions and no retry loops.

## 5. Readiness Policy

`/health` remains process liveness only. `/ready` uses the simple production-safe
policy that inference, configured memory, vector storage, and BM25 must all be
ready. Any required component failure returns 503, while the process remains
alive. Component responses contain only provider names, normalized statuses,
configured model IDs, and bounded BM25 expected/loaded identifiers; credentials,
URLs, upstream bodies, and exception text are excluded.

Vector loss after startup and Redis/inference loss are visible on the next probe.
BM25 readiness consumes the version already returned by the vector check and does
not rebuild or make a second version call when the vector component is down.

## 6. BM25 Version / Refresh Strategy

`BM25_CORPUS_VERSION` is a required safe 1–64 character identifier. Ingestion
retains Phase 8F UUIDv5 upserts, refuses to publish an empty ingestion, and writes
the version to Chroma collection metadata only after every chunk succeeds.

At replica startup, the expected version must equal Chroma's published version.
Documents are sorted by source, chunk identifier, and content before the existing
tokenization and `BM25Okapi` construction, producing deterministic snapshots.
The loaded version is retained per process and exposed by sanitized readiness.

Refresh is rollout-based: ingest and publish a new immutable version, then roll
all replicas with that expected version. Old replicas become unready on mismatch;
new replicas become ready only after loading the new snapshot. No request or
readiness thread builds/rebuilds BM25. This guarantees that ready replicas agree
on the declared corpus version, but does not make multi-document ingestion one
transaction or provide blue/green publication.

## 7. Serving vs Ingestion/Admin Separation

Serving uses Chroma `get_collection`, never `get_or_create_collection`. Concrete
serving adapters reject `upsert`, reset, and version publication with the safe
`vector_write_forbidden` category. A separately cached administrative factory is
used only by `rag.ingest` and `rag.admin`; no admin/reset endpoint exists and API
startup never imports or invokes those commands.

## 8. Local Compose vs Production

Local defaults remain Ollama, file memory, and local Chroma. Optional `redis` and
`vector` Compose profiles provide isolated development services with named
volumes, health checks, and no Redis/Chroma host-port publication. Compose sets
`DEPLOYMENT_ENV=compose` and is explicitly documented as non-production.

Production uses `DEPLOYMENT_ENV=production`, external OpenAI-compatible inference,
Redis, and Chroma HTTP. Validation rejects file/local backends and loopback or
`host.docker.internal` service hosts. Docker Compose does not own the production
service topology.

## 9. Security & Network Boundaries

Production operators are expected to network-restrict vLLM, Redis, Chroma,
`/metrics`, and ingestion/admin execution. Redis authentication/TLS (`rediss`) and
Chroma/vLLM authentication and TLS should be enabled where supported by the
operated services. The phase does not claim OAuth, RBAC, gateways, or service-mesh
controls. Runtime secrets remain environment-provided and are not logged or
returned.

## 10. Observability

Existing safe provider/memory/vector/request metrics remain. Phase 8G adds the
bounded `component_readiness{component=...}` gauge,
`bm25_snapshot_build_duration_seconds`, and
`bm25_snapshot_refresh_total{outcome=...}`. No corpus-version label exists.
Readiness and lifecycle logs use normalized states; versions may be inspected in
the bounded readiness payload. Metrics remain per worker/replica and every replica
must be scraped independently.

## 11. Multi-Replica Readiness

`READY FOR REPLICAS`

- Stateless inference adapters, provider-neutral orchestration, request IDs,
  Redis memory, and Chroma HTTP dense retrieval when all replicas share config.

`PROCESS-LOCAL BUT ACCEPTABLE`

- BM25 immutable snapshots with version-gated readiness.
- Provider/Redis/Chroma clients and Prometheus registries per replica.

`REQUIRES OPERATIONAL CONTROL`

- Versioned ingestion followed by controlled replica rollout.
- Independent scraping and external aggregation of replica metrics.
- External service security, persistence, backup, and availability.

`FUTURE RISK`

- Corpus publication is not an atomic multi-document transaction.
- No automatic BM25 reload, blue/green vector collection, Chroma HA, Redis HA, or
  coordinated ingestion scheduler exists.

## 12. Files Changed

Modified:

- `.env.example`, `Makefile`, `README.md`, `docker-compose.yml`
- `api/app.py`, `config/settings.py`
- `graph/semantic_router.py`
- `llm/inference.py`, `llm/metrics.py`, `llm/ollama_client.py`,
  `llm/openai_compatible.py`
- `rag/bm25.py`, `rag/chroma_store.py`, `rag/embeddings.py`, `rag/ingest.py`,
  `rag/vector_store.py`, `rag/vector_store_factory.py`
- `tests/unit/test_api_reliability.py`,
  `tests/unit/test_retrieval_regression.py`, `tests/unit/test_vector_store.py`

Added:

- `docs/codex/prompts/phase_8g.md`
- `docs/codex/reports/phase_8g_report.md`
- `tests/unit/test_deployment_topology.py`

Deleted:

- None.

## 13. Dependencies

No dependency or version changed. The implementation uses existing pinned
Chroma, HTTPX, Pydantic, Prometheus client, Redis, and BM25 packages. Chroma 1.5.9
creates its HTTPX session with no timeout and exposes no public timeout argument;
the factory therefore verifies the pinned client's known session layout, applies
`VECTOR_STORE_TIMEOUT`, and fails early if that layout changes.

## 14. Tests Added / Updated

The suite now covers local and production deployment configuration; invalid
providers/endpoints/versions; all existing composite dependency failures; stale
BM25 composite readiness; deterministic version load/match/mismatch; absence of
request-time rebuild; publication ordering and repeated-ingestion IDs; query-only
serving/admin mutation enforcement; degraded startup and complete shutdown paths;
safe imports; bounded metrics without corpus-version labels; and Chroma timeout
construction. Phase 8A–8F regression tests remain unchanged in behavior.

## 15. Validation Results

- `pytest -q`: passed, **138 passed in 20.61s**.
- Compile validation: passed with
  `PYTHONPYCACHEPREFIX=/tmp/polymind-phase8g-final-pycache python -m compileall -q .`.
- `git diff --check`: passed.
- Docker Compose validation: base, `--profile redis`, and `--profile vector` all
  passed with `config --quiet`.
- Docker build: `docker build .` passed with cache; scoped `docker compose build
  api` also passed with cache.
- Local Compose integration: Redis 7.4 and Chroma 1.5.9 both became healthy with
  no host ports; a one-off API image check returned `ready ready development` for
  Redis readiness, Chroma readiness, and version publication/readback. Scoped
  containers/network were stopped and removed; persistent volumes were retained.
- Linting: no repository lint command/configuration was found; not run.
- Security scan: no dedicated scanner is configured. A targeted secret/private-key
  pattern scan found only configuration variable references and deliberate dummy
  test tokens, with no credential material.

## 16. Implementation Self-Review

Review found and fixed: serving's concrete `upsert` path needed its own runtime
guard; failed vector readiness could cause a redundant BM25 remote call; BM25
errors needed the existing sanitized vector error path; document ordering needed
canonicalization; version values needed bounded syntax; empty ingestion should
not publish; embedding/router import performed model construction; and Chroma's
default HTTP session was unbounded and not closed. Tests were added for each
material finding. Review confirmed no provider-specific logic leaked into graph,
API contracts remain stable except the intentional additive BM25 readiness field,
and no request-time sparse rebuild remains.

## 17. Pre-Commit Review

The working tree contains only Phase 8G modified/added files listed above. Diff
scope contains no Kubernetes/cloud work, new dependency, public admin endpoint,
startup ingestion/reset, credential, `.env`, private key, local absolute path,
temporary artifact, or generated bytecode. Existing `/query`, `/query/stream`,
NDJSON, request ID, Ollama, OpenAI-compatible, Redis memory, and retrieval tests
pass. Compose profiles and cached image builds pass. The only operational warning
is the explicitly documented pinned Chroma private-session timeout integration,
which fails early on incompatible upgrades.

No commit was created.
No push was performed.

## 18. Documentation

README now documents the final topology, ownership boundaries, production-profile
validation, alive/not-ready startup, cleanup, composite readiness, versioned BM25
rollout, serving/admin split, local Compose distinction, security expectations,
per-replica metrics, and known consistency limits. `.env.example` and Make help
describe the new settings/workflow. The phase prompt and this report are stored
under `docs/codex` without modifying earlier artifacts.

## 19. Remaining Risks / Technical Debt

### Phase 8G concerns

- The pinned Chroma 1.5.9 client has no public timeout configuration; the bounded
  session integration intentionally depends on a verified private client field.
- A very large BM25 corpus can lengthen startup, although remote calls are bounded
  and failure does not kill the process.
- Collection version publication follows completed upserts but cannot roll them
  back atomically if an ingestion fails partway through.

### Deliberately deferred infrastructure work

- Kubernetes/Helm/cloud/Terraform, autoscaling, gateways, OAuth/RBAC, tenant
  isolation, service mesh, managed secrets, Prometheus/Grafana/tracing.
- Redis Cluster/Sentinel, Chroma HA, blue/green collections, distributed locking,
  and a full ingestion scheduler/orchestrator.
- vLLM installation, GPU/CUDA, and model deployment.

## 20. Next-Phase Readiness

`READY WITH CONDITIONS`

The codebase is ready for a deployment-manifest/operations phase that consumes
these explicit external-service contracts. The most appropriate next phase is a
Kubernetes deployment design and manifests phase only after operators choose
actual inference, Redis, and Chroma service endpoints/security mechanisms and
accept the rollout-based corpus publication procedure. Chroma timeout integration
should be revalidated whenever the pinned client is upgraded.
