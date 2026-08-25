# PolyMind production security runbook

## Application authentication and endpoints

Local and Compose development default to `API_AUTH_ENABLED=false` and
`API_DOCS_ENABLED=true`. Production must set `API_AUTH_ENABLED=true`, provide an
`API_AUTH_TOKEN` containing at least 32 non-whitespace characters, and set
`API_DOCS_ENABLED=false`; invalid static configuration stops startup.

Clients send `Authorization: Bearer <token>`. Missing, malformed, and incorrect
credentials receive the same sanitized 401 response and `WWW-Authenticate:
Bearer`. Authentication protects `/query`, `/query/stream`, and
`/memory/{session_id}`. The latter is cluster-internal by default but is protected
because it contains conversation history. The comparison uses
`secrets.compare_digest`. Tokens and request content are never logged.

`/health` and `/ready` remain unauthenticated for Kubernetes probes. `/metrics`
remains unauthenticated for cluster monitoring. Production docs, ReDoc, and the
OpenAPI URL are disabled. The chart's public Ingress routes only the `/query`
prefix, covering both query endpoints while excluding memory, probes, metrics,
docs, and schema routes.

`MAX_REQUEST_BYTES` defaults to 1 MiB and may be configured from 1 byte through
10 MiB. The ASGI boundary counts received chunks as well as validating
Content-Length and rejects oversized requests before graph/inference execution.
Configure the ingress/gateway with an equal or smaller limit for defense in depth.
Global rate limiting belongs at that gateway; no per-process limit is presented
as replica-wide enforcement.

## Kubernetes Secrets and rotation

Production defaults use `secrets.create=false` and
`secrets.existingSecret=polymind-secrets`. The Secret must contain the configured
`redis-url` and `api-auth-token` keys; `openai-compatible-api-key` is optional.
External Secrets Operator, CSI secret providers, and Azure/AWS/GCP secret stores
can all materialize the same Kubernetes Secret without application coupling.
The chart does not deploy those systems.

Chart-managed Secret creation is for controlled validation only. Values are empty
by default and Helm fails rendering unless Redis and API token values are supplied.
Never commit them or put production values in a shared values file.

Secrets are read at process startup. Rotate the external value, confirm the
Kubernetes Secret has the new version, then trigger and monitor a rolling
Deployment restart. During bearer-token rotation there is no dual-token window;
coordinate client cutover with the rollout or use an upstream gateway capable of
overlapping credentials.

## NetworkPolicy

`networkPolicy.enabled=true` is the production chart default. The policy selects
only this Helm release's pods and applies both ingress and egress isolation.
Defaults allow the configured ingress-controller selector and DNS through
CoreDNS. Optional monitoring ingress permits direct per-pod scraping. Redis,
Chroma, and inference egress each have a namespace/pod selector, TCP port, and an
optional list of `ipBlocks`.

Replace the example namespaces, labels, ports, and CIDRs with the operated
environment. Empty external CIDR lists do not permit external endpoints. Vanilla
Kubernetes NetworkPolicy cannot filter by domain name; use stable reviewed CIDRs,
private endpoints, or a supported CNI/egress gateway. Never use `0.0.0.0/0` merely
to make readiness pass. Node-originated Kubernetes probes are normally permitted
by NetworkPolicy semantics, but this must be confirmed with the selected CNI.

Kind's default CNI does not enforce NetworkPolicy. The Phase 10 override disables
it and validates the rendered production policy structurally. Do not claim local
enforcement without installing and testing a policy-capable CNI.

## Ingress, TLS, metrics, and proxies

Ingress is disabled by default. When enabled, configure the host, ingress class,
TLS Secret, annotations, and `/query` path. Operators provide the ingress/gateway,
certificate, DNS, and TLS policy. The chart installs none of them.

If TLS terminates upstream, restrict direct Service access and configure Uvicorn
proxy-header trust only for known proxy addresses. PolyMind does not use forwarded
headers for security decisions and this phase does not blindly trust arbitrary
`Forwarded` or `X-Forwarded-*` input.

Do not add `/metrics`, `/health`, `/ready`, `/docs`, `/redoc`, `/openapi.json`, or
`/memory` to the public Ingress. NetworkPolicy is L3/L4: a monitoring peer allowed
to port 8001 can technically reach other routes, but bearer authentication still
protects application/history routes. A separate metrics listener can be evaluated
in a later observability phase if stronger path separation is required.

## Container, service account, and filesystem

The image and chart both run as UID/GID 10001. The pod uses RuntimeDefault seccomp,
drops all capabilities, disables privilege escalation, and does not automount a
service-account token. PolyMind does not call the Kubernetes API, so it requires
no Role or RoleBinding.

`readOnlyRootFilesystem` remains false. Current embedding/reranker downloads and
Python/Hugging Face/Torch caches need writable home/cache paths; local file memory,
local Chroma, and temporary files also need writes in development. Phase 12 should
package immutable model artifacts, set explicit cache/temp paths, and determine
the smallest `emptyDir` mounts before enabling a read-only production root.

## Security operations

Monitor bounded `authentication_requests_total` and
`request_rejections_total` metrics. Logs contain request ID, endpoint class,
reason, and outcome only. Investigate sustained auth rejection or oversized-body
rates without collecting raw client credentials, IPs, or request content.

Run ingestion/reset only as a separately authorized internal job or operator
command. Use immutable image tags or digests for production. Dependency scanning,
container scanning, SBOMs, signing, gateway rate limiting, OAuth/OIDC, mTLS, and
cloud secret-manager deployment remain explicit future controls.
