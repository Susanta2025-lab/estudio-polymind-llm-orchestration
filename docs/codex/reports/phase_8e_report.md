# Phase 8E — Externalized Memory & Multi-Replica Readiness Report

## 1. Phase Result

`CONDITIONAL PASS`

Conversation memory is now suitable for multi-worker and multi-replica use when
all replicas select the Redis provider and use the same external service. The
result is conditional because the repository's local, module-level ChromaDB
client remains a separate RAG replica-readiness constraint; migrating it was
explicitly outside Phase 8E.

## 2. Memory Architecture

`ConversationMemoryStore` is a narrow provider-neutral protocol with history
read, atomic exchange append, per-session clear, readiness, and close operations.
Graph construction injects one configured store into direct, RAG, tool, and
streaming execution. API readiness and memory retrieval use that same instance;
application modules do not import Redis or construct concrete stores.

`FileMemoryStore` preserves the existing JSON format for local development. It
serializes threads and local processes with an `RLock` plus the existing
`filelock` dependency, writes through a temporary file with `fsync`, and replaces
the target atomically. This improves single-host behavior but is deliberately not
classified as shared replica storage. `RedisMemoryStore` is the shared backend.

## 3. External Memory Backend Decision

Redis was selected. Conversation history is an append/read-tail/trim workload for
which Redis lists and transactions are a direct match. Redis provides atomic
multi-command transactions, TTL, pooled connections, lightweight `PING`
readiness, common managed-service availability, and straightforward deterministic
testing without an ORM or schema migration layer.

PostgreSQL would offer stronger relational/durable querying semantics, but current
requirements do not need relational access. Adding a driver, schema, migrations,
and transaction model would be substantially heavier. Redis persistence and HA
remain deployment responsibilities; this phase does not claim Cluster, Sentinel,
or managed-service provisioning.

## 4. Concurrency & Atomicity

One Redis transaction performs `RPUSH` of the user and assistant messages,
`LTRIM` to the configured bound, and optional `EXPIRE`. Concurrent exchanges are
serialized by Redis transaction execution: no exchange performs a read-modify-
overwrite cycle, and the two messages of an exchange remain adjacent. Ordering
between genuinely simultaneous exchanges is Redis execution order, not client
wall-clock order; within every exchange, user precedes assistant.

File writes place the complete read-modify-write sequence under thread and file
locks and atomically replace the file. This prevents obvious same-host lost and
partial writes but does not make a container-local file a distributed store.

## 5. Session Isolation & Retention

Redis keys are `polymind:memory:<sha256(session_id)>`, preventing path traversal,
namespace injection, unsafe characters, and excessive key length. API session IDs
are non-empty and limited to 256 characters. File records retain the established
explicit session field and filter exactly by it.

`MEMORY_HISTORY` is validated positive and bounds stored messages per session in
both backends. `MEMORY_TTL` is validated non-negative; zero disables expiry and a
positive value refreshes the Redis session's idle TTL after each successful
exchange. Sessions have independent keys and retention.

## 6. Failure Behavior

Redis connectivity, timeout, protocol/malformed-data, read, and write failures are
normalized into a small provider-neutral taxonomy with sanitized messages. The
non-streaming API returns a sanitized 503 through its memory exception handler;
streaming returns an NDJSON `error` event. Logs contain request ID, provider, route
where available, and category, but not URLs, credentials, keys, or content.

An exchange is persisted only after successful generation/stream completion and
is one transaction. A failed transaction cannot intentionally persist only the
user half. With `MEMORY_PROVIDER=redis`, construction and operations never fall
back to the file backend, preventing split-brain state.

## 7. Liveness & Readiness Integration

`/health` remains process-only and does not contact inference or memory.
`/ready` combines inference discovery with memory readiness. Redis uses `PING`;
the file provider checks path access. HTTP 200 requires both components. HTTP 503
includes sanitized `inference` and `memory` states. The prior top-level inference
`provider` and inference failure status remain for compatibility, while successful
status remains `ready`. Memory readiness metrics and correlated component logs are
recorded.

## 8. Multi-Replica Readiness Review

`SAFE FOR REPLICAS`

- Conversation history when every replica uses the same Redis service.
- Inference adapters and provider-neutral routing, which hold pooled clients but
  no cross-request conversational state.
- Request IDs, which use request-local `ContextVar` state.

`REQUIRES SHARED STORAGE`

- Conversation history in production; the file provider is not sufficient.
- Mutable RAG/vector data. Current local Chroma persistence cannot be a shared
  distributed data plane between replicas.

`PROCESS-LOCAL BUT ACCEPTABLE`

- Prometheus registries and counters when every worker/replica is scraped
  independently and aggregation happens in the monitoring system.
- Immutable configuration and initialized client pools within each worker.

`FUTURE RISK`

- `rag/vectordb.py` hard-codes `./chroma_db`, creates a module-level
  `PersistentClient`, and does not consume `CHROMA_PATH`. Shared-filesystem writes
  or independent mutable copies can diverge. A server/shared vector-store boundary
  is deferred.
- Local document mounts and ingestion/reset commands remain single-node
  operational workflows.
- Prometheus multiprocess mode is not configured if several workers share one
  scrape endpoint; per-worker/replica scraping is the documented pattern.

## 9. Observability

The phase adds `memory_operations_total`,
`memory_operation_duration_seconds`, `memory_errors_total`,
`memory_readiness_checks_total`, and
`memory_readiness_check_duration_seconds`. Labels are restricted to provider,
operation, outcome, and normalized error category. Tests verify session IDs,
request IDs, and content are absent. Redis is not used for metric aggregation.

## 10. Files Changed

Modified:

- `.env.example`
- `README.md`
- `api/app.py`
- `config/settings.py`
- `docker-compose.yml`
- `experiments/test_memory.py`
- `graph/generation.py`
- `graph/langgraph_flow.py`
- `graph/nodes.py`
- `graph/streaming.py`
- `llm/metrics.py`
- `memory/memory_store.py`
- `requirements.txt`
- `tests/unit/test_api_reliability.py`
- `tests/unit/test_streaming_orchestration.py`

Added:

- `docs/codex/prompts/phase_8e.md`
- `docs/codex/reports/phase_8e_report.md`
- `memory/provider_factory.py`
- `tests/unit/test_memory_integration.py`
- `tests/unit/test_memory_store.py`

Deleted:

- None.

## 11. Dependencies

`redis==6.4.0` was added as the maintained minimal Python Redis client. It supplies
URL configuration, connection pooling, transaction pipelines, explicit socket
timeouts, `PING`, and clean client/pool closure. `filelock` was already pinned and
is reused. No database framework, ORM, GPU, or infrastructure dependency was
added.

## 12. Tests Added / Updated

The new tests cover empty reads, ordered exchange appends, session clearing,
history trimming, isolation, hashed key safety, TTL, atomic Redis pipelines,
threaded concurrent exchange pairs, file lost-update protection, connection and
timeout normalization, malformed data, read/write failures, no partial write on
failure, bounded metrics, provider/timeout/TTL configuration validation, factory
pool settings, injected exactly-once persistence, composite readiness, and
liveness independence. Existing streaming tests continue to prove one persistence
call on success and none after an incomplete stream. Phase 8A–8D regression tests
remain included.

## 13. Validation Results

- `pytest -q`: passed, **108 passed in 0.59s** on the final documented tree.
- Compile validation: `PYTHONPYCACHEPREFIX=/tmp/polymind-phase8e-final-pycache python -m compileall -q .` passed with no output.
- `git diff --check`: passed with no output.
- `docker compose config --quiet`: passed.
- `docker compose --profile redis config --quiet`: passed.
- Docker build: `docker build .` passed using normal cache behavior; Redis 6.4.0 resolved and installed in Python 3.10. No `--no-cache` was used.
- Optional integration validation: not run; no live Redis was required or started.
- Linting: no separate configured lint command/tool was found.
- Security scan: focused repository diff/secret/debug/TODO pattern review passed; only documented placeholders and pre-existing test fixtures/debug prints were found.

## 14. Implementation Self-Review

The full diff and all memory consumers were reviewed. Findings fixed before final
validation were: preserving legacy readiness top-level provider/failure status
while adding component detail; updating the old experiment's removed direct file
helper; bounding the memory path session parameter; classifying malformed file
JSON as protocol failure; validating Redis message timestamps; recording file
readiness metrics; and adding request-correlated memory readiness detail. Graph
construction retains its prior one-argument compatibility while supporting store
injection.

The final review found no concrete Redis/file leakage into graph or API behavior,
no read-modify-overwrite Redis path, no silent fallback, no unbounded metric
label, and no change to query or NDJSON response shapes.

## 15. Pre-Commit Review

The working tree contains only uncommitted Phase 8E implementation,
tests, configuration, documentation, and the small legacy experiment consumer
update. `git status` lists 15 modified and 5 added files after this report is
included; there are no deletions. No real `.env`, credentials, private key,
machine-specific absolute path, generated bytecode, temporary file, new TODO,
debug statement, or unrelated infrastructure change was introduced.

Compatibility review confirms `/query`, `/query/stream`, NDJSON events, request
IDs, inference providers, routing, tools, and successful persistence timing remain
intact. `/ready` intentionally gains component detail and memory dependency while
retaining the former top-level inference provider/status behavior where possible.

No commit was created.
No push was performed.

## 16. Documentation

README now describes the memory contract, file limitations, Redis configuration,
atomicity, TTL/history semantics, failure behavior, local optional Compose use,
production external-service expectations, readiness, safe metrics cardinality,
per-replica scraping, and the Chroma/local-ingestion constraint. `.env.example`
documents every validated memory setting. The clean phase prompt and this report
are stored under `docs/codex/`.

## 17. Remaining Risks / Technical Debt

### Phase 8E concerns

- Redis durability and availability depend on external service configuration;
  this repository does not supply production HA, backups, TLS, or credential
  rotation.
- Concurrent exchanges are ordered by Redis execution order. The design does not
  impose client-side causal ordering between simultaneous requests for one
  session.
- The file backend is safer locally but remains unsuitable for replicas.
- No live Redis integration test was run; core behavior is covered by a
  deterministic transactional fake and the client dependency was Docker-built.

### Deliberately deferred infrastructure work

- Shared/server-mode vector storage and Chroma migration.
- Redis Cluster/Sentinel/managed provisioning and disaster recovery.
- Kubernetes, autoscaling, load balancing, and service discovery.
- Prometheus server, multiprocess collector deployment, dashboards, and alerts.
- Distributed tracing and broader platform/security controls.

## 18. Next-Phase Readiness

`READY WITH CONDITIONS`

The inference and conversational-memory boundaries are ready for a production
platform phase that defines deployment topology and validates shared services.
The most appropriate next phase is a focused **RAG data-plane externalization and
replica-readiness assessment/implementation**, beginning with removal of the
hard-coded module-level local Chroma assumption. Production rollout should also
define externally managed Redis security/durability and per-replica metrics
scraping, without coupling those concerns to conversation memory.
