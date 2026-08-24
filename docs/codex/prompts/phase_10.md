# Phase 10 — Kubernetes Validation, Local Cluster Deployment & Operational Testing

Validate the Phase 9 Helm chart against a real, dedicated local Kubernetes
control plane (Kind preferred) without changing the production ownership
boundary. Build and load the actual PolyMind image, deploy test-only external
Redis, Chroma, and deterministic OpenAI-compatible inference infrastructure,
and install PolyMind with Helm in an isolated namespace.

Operationally verify static rendering, startup and non-root security, `/health`,
dependency- and BM25-aware `/ready`, deterministic corpus publication and
version gating, `/query`, NDJSON `/query/stream`, `/metrics`, two replicas,
dependency failure and recovery, pod reconciliation, rolling update, and Helm
rollback. Keep Ingress disabled and do not deploy vLLM, GPUs, cloud resources,
Prometheus, production dependency charts, or unrelated infrastructure.

Add narrowly scoped, context-guarded local automation and deterministic safety
tests where useful. Document the exact executed workflow and distinguish local
validation fixtures from production architecture. Run the complete automated,
compile, diff, Helm, Docker, Kubernetes, security, and secret validations;
perform implementation self-review and pre-commit review; save the detailed
report as `docs/codex/reports/phase_10_report.md`; and do not commit or push.
