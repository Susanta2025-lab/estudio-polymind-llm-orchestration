# Phase 9 — Kubernetes & Helm Deployment Foundation

## Objective

Create a production-style Kubernetes and Helm deployment foundation for PolyMind
API replicas while keeping OpenAI-compatible/vLLM inference, Redis memory, and
Chroma HTTP vector storage external.

## Required scope

- Add a Helm chart containing Deployment, Service, ConfigMap, Secret-reference,
  optional Secret, ServiceAccount, and disabled-by-default Ingress templates.
- Make replicas, image, port, probes, rolling update, resources, external-service
  configuration, service account, ingress, and baseline security configurable.
- Use `/health` for liveness and composite `/ready` for readiness.
- Add cluster-free lint/render commands and useful automated chart tests.
- Document install, configuration, secret handling, upgrades, rollback, metrics,
  external dependencies, and explicitly excluded infrastructure.
- Preserve provider-neutral application architecture and Phase 8G semantics.
- Do not deploy or bundle Kubernetes, cloud infrastructure, vLLM, Redis, Chroma,
  monitoring, ingress controllers, certificate management, or authentication.
- Run repository, Docker, Helm, and pre-commit validation; do not commit or push.

