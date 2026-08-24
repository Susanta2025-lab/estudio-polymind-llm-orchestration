# Phase 10 local Kubernetes validation

This directory is a local operational test fixture for the dedicated Kind
cluster `polymind-phase10`. It is not a production dependency topology. The
production Helm chart continues to deploy only the PolyMind control plane;
Redis, Chroma, and inference remain externally operated services.

Run `deployment/kind/phase10/phase10.sh help` for the guarded workflow. The
script always uses context `kind-polymind-phase10` and namespace
`polymind-phase10`; it refuses to mutate any other cluster. Prerequisites are
Docker, kubectl, Helm 3, and Kind. Override tool paths with `HELM_BIN` and
`KIND_BIN` when using standalone binaries.

The normal sequence is:

```bash
deployment/kind/phase10/phase10.sh create
deployment/kind/phase10/phase10.sh build
deployment/kind/phase10/phase10.sh load
deployment/kind/phase10/phase10.sh deploy
deployment/kind/phase10/phase10.sh bootstrap phase10-v1
deployment/kind/phase10/phase10.sh smoke
```

The fixtures use ephemeral, unauthenticated Redis and Chroma plus a deterministic
OpenAI-compatible stub. They are isolated in the test namespace and make no HA,
durability, security, capacity, or production-readiness claim. `smoke` uses a
scoped port-forward and validates `/health`, `/ready`, `/metrics`, `/query`, and
the NDJSON `/query/stream` response. Use `destroy` only for the dedicated cluster.

Operational transitions (scaling, corpus-version rollout, dependency outage,
pod replacement, Helm upgrade, and rollback) are documented in the root README
and Phase 10 report because they require observation between commands.

