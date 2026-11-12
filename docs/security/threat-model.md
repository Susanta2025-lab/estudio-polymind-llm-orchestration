# PolyMind production threat model

Scope update — 12 November 2026: the Phase 11 mitigations and residual-risk snapshot
below describe the original static-bearer deployment boundary. Subsequent chart
hardening implements a read-only root filesystem and graceful bounded stream
draining; see the [current deployment/security runbook](production-security.md).
The separate [Phase 17G contract](phase_17g.md) adds reference OIDC/Entra identity,
tenant/owner authorization, revocation and durable quota/cost governance.
Distributed authority, physical purge and public-user production readiness remain
unestablished. The [v11 controlled workflow](../codex/reports/phase_17h_v11_controlled_live_execution_and_reconciliation.md)
passed full live digestion, provenance, publication and grounded Q&A within one
bounded benchmark. The [completion decision](../evaluation/phase_17_engineering_completion_and_deferred_acceptance.md)
records `PHASE_17_ENGINEERING_COMPLETE`,
`DEFERRED_PENDING_TWO_INDEPENDENT_REVIEWERS` (0/2),
`PHASE_17_FORMAL_CLOSURE_PENDING` and `NEXT_PHASE_DEVELOPMENT_PERMITTED`.
Historical deferred items below must be read against later scoped implementations;
this status does not establish production security or general semantic reliability.

## Scope and assets

This model covers the FastAPI control plane and its connections to an ingress or
gateway, external inference, Redis, Chroma, and controlled ingestion jobs. Assets
include the PolyMind API token, inference credential, Redis conversation state,
indexed Chroma documents, user prompts, retrieved context, and model responses.

## Trust boundaries

```text
external client -> TLS ingress/gateway -> PolyMind
PolyMind -> OpenAI-compatible inference
PolyMind -> Redis
PolyMind -> Chroma
restricted administrator/ingestion job -> Chroma
monitoring system -> PolyMind /metrics
```

The ingress authenticates its own clients where applicable, but PolyMind still
requires its application bearer token in production. Redis, Chroma, inference,
monitoring, and administrative workloads are separately operated trust domains.

## Threats and Phase 11 mitigations

| Threat | Mitigation |
|---|---|
| Unauthenticated inference or conversation access | Timing-safe bearer validation on query, stream, and memory routes; production fails without a strong configured token |
| Credential or prompt leakage | Secrets use environment/Kubernetes Secret sources; logs contain bounded event fields and never headers, tokens, prompts, history, or documents |
| Public metrics, probes, or docs | Public Ingress defaults to `/query` only; docs/OpenAPI are disabled in production; metrics and probes remain cluster-internal |
| Oversized or chunked request bodies | Per-replica ASGI receive limit rejects before orchestration with sanitized 413 |
| Lateral movement or unrestricted egress | Optional default-deny NetworkPolicy explicitly permits selected gateway/monitoring peers, DNS, Redis, Chroma, and inference |
| Secret misconfiguration | Pydantic startup validation rejects production auth bypass, missing/short/whitespace tokens, and enabled docs |
| Destructive ingestion misuse | No HTTP ingestion/reset route exists; mutation remains an explicit restricted CLI/job operation |
| Dependency impersonation | Network selectors/CIDRs narrow destinations; operators must provide dependency TLS and authentication where supported |
| Supply-chain/image vulnerability | Dependencies are pinned, the image defaults to non-root, CI builds the image and validates Helm; scanning/signing remain deferred |

## Residual risks

One shared API port means Kubernetes NetworkPolicy cannot distinguish `/metrics`
from application paths; monitoring peers can reach the port, while application
authentication still protects query/history routes. Standard NetworkPolicy
cannot select an external service by DNS name, so external services require
reviewed stable CIDRs, a private network endpoint, or CNI/gateway-specific policy.

Gateway-level rate limiting, distributed abuse prevention, dependency mTLS,
automated secret-store integration, image scanning/SBOM/signing, read-only root
filesystems, graceful stream draining, and multi-node availability controls are
deliberately deferred. Prompt injection and untrusted retrieved content remain
LLM/application risks rather than authentication bypasses.
