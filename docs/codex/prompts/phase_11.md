# Phase 11 — Production Security & Network Controls

Implement a vendor-neutral production security baseline after the validated
Phase 10 Kubernetes foundation. Preserve local development and existing API,
streaming, provider, Redis, Chroma, BM25, Helm, and Kind contracts.

Required scope:

- environment/Secret-sourced timing-safe bearer authentication;
- production rejection of disabled auth, absent credentials, or exposed docs;
- explicit query, probe, metrics, docs/OpenAPI, memory, and admin exposure policy;
- bounded request bodies without a distributed rate-limiter platform;
- externally managed Secret compatibility and rollout-based rotation contract;
- default-deny-capable Helm NetworkPolicy with gateway, monitoring, DNS, Redis,
  Chroma, and external inference controls;
- optional TLS-capable Ingress that does not publicly route internal endpoints;
- non-root Docker default while preserving the Kubernetes pod security context;
- security tests, scoped Phase 10 Kind validation, CI Helm validation, a concise
  threat model, and production security runbook.

Do not add cloud-specific identity/secrets, OAuth/OIDC, service mesh, cert-manager,
ingress controllers, dependency authentication infrastructure, autoscaling,
availability controls, model packaging, observability platforms, vLLM/GPU, or
cloud deployment. Do not commit or push.
