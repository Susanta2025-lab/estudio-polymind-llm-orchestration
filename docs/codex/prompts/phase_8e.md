# Phase 8E — Externalized Memory & Multi-Replica Readiness

## Objective

Make Estudio PolyMind safe for multiple API workers and application replicas by
placing conversational state behind a narrow provider-neutral store and providing
a credible shared external backend without deploying distributed infrastructure.

## Required architecture

```text
Application / LangGraph
        ↓
ConversationMemoryStore
      ↙       ↘
local file   external Redis
```

Preserve session history, RAG, tools, LangGraph, both inference providers,
`/query`, NDJSON `/query/stream`, request correlation, health, readiness, metrics,
and Docker behavior. The file provider may remain for local single-process use but
must not be represented as replica-safe. Redis must remain an external service,
use pooled connections and explicit timeouts, atomically append ordered exchanges,
bound history, optionally apply TTL, isolate safe session keys, normalize failures,
and never silently fall back to a local file.

Centralize and validate memory configuration. Inject the configured contract into
graph/application code. Keep `/health` process-only and make `/ready` account for
required shared memory. Add bounded memory instrumentation without session IDs,
request IDs, keys, or content as labels, while retaining request IDs in sanitized
operational logs.

Add deterministic infrastructure-independent tests covering the memory contract,
Redis success and failure behavior, atomic/concurrent updates, ordering, isolation,
retention, TTL, readiness, configuration, API/stream regression, exactly-once
persistence, incomplete-stream behavior, and metrics cardinality. Keep CI free of
live Redis, inference services, GPU, and credentials.

Review other replica-local state, especially process-local Prometheus registries
and local Chroma persistence. Classify findings, but do not migrate Chroma or add
Kubernetes, HA Redis, distributed metrics infrastructure, or unrelated platform
work.

Follow the repository inspect/plan/implement/test/self-review/pre-commit/document/
validate/report workflow. Update README, `.env.example`, appropriate Compose
development wiring, and create this prompt plus `phase_8e_report.md`. Run pytest,
external-cache compile validation, `git diff --check`, Compose validation, and a
cache-reusing Docker build where available. Do not commit or push.
