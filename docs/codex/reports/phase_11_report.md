# Phase 11 — Production Security & Network Controls

## 1. Phase Result

`PASS`

Phase 11 establishes a vendor-neutral security boundary without adding an
identity platform, cloud coupling, or provider-specific behavior. Production
startup now rejects disabled authentication, invalid bearer-token configuration,
or exposed documentation. The Helm chart defaults to external Secrets,
deny-by-default NetworkPolicy behavior, disabled public ingress, and a public
path limited to authenticated query traffic when ingress is enabled.

## 2. Security Architecture

External clients terminate TLS at an operator-provided ingress or gateway and
then cross PolyMind's application bearer boundary. PolyMind continues to own only
the control plane and connects outward to separately operated inference, Redis,
and Chroma. Ingress and egress isolation is expressed through a release-scoped
NetworkPolicy. Monitoring and Kubernetes probes remain cluster-operational
surfaces rather than public application endpoints.

## 3. Authentication Model

Local and Compose modes default to disabled authentication and enabled developer
docs. Production requires `API_AUTH_ENABLED=true`, a whitespace-free
`API_AUTH_TOKEN` of at least 32 characters, and `API_DOCS_ENABLED=false`.

Protected requests use `Authorization: Bearer <token>`. Missing, malformed, and
incorrect credentials receive the same sanitized 401 and `WWW-Authenticate:
Bearer`; comparison uses `secrets.compare_digest`. `/query`, `/query/stream`, and
conversation-history access are protected. Authentication occurs before request
body parsing and applies unchanged throughout NDJSON streaming.

## 4. Endpoint Exposure Policy

- `/query` and `/query/stream`: authenticated; the only routes selected by the
  default public Ingress `/query` prefix.
- `/memory/{session_id}`: authenticated but not publicly routed.
- `/health` and `/ready`: unauthenticated for Kubernetes probes and excluded from
  public Ingress.
- `/metrics`: unauthenticated for cluster monitoring, excluded from public
  Ingress, and intended to be NetworkPolicy-restricted.
- `/docs`, `/redoc`, and `/openapi.json`: available locally and disabled in
  production.
- Ingestion/reset: CLI/admin operations only; no HTTP routes were added.

## 5. Secret Management

The chart retains `secrets.create=false` and `secrets.existingSecret` as the
production default. The external Secret supplies Redis URL, required PolyMind API
token, and optional inference key. Empty committed defaults contain no secret
material. Optional chart-created Secrets require Redis and token values at render
time and are documented for controlled validation only.

The interface is compatible with Secrets materialized by External Secrets
Operator, CSI providers, or cloud secret managers without coupling application
code to them. Secrets are read at startup. Rotation is update Secret, trigger a
rolling restart, and verify new pods; hot reload and dual-token overlap were not
implemented.

## 6. NetworkPolicy

The chart now renders a policy selecting only the release's pods with Ingress and
Egress policy types. Ingress permits configured gateway peers and optionally
monitoring peers. Egress permits selected CoreDNS pods on TCP/UDP 53 and selected
Redis, Chroma, and inference peers on configured TCP ports. Each dependency also
accepts reviewed `ipBlocks` for external endpoints.

No wildcard egress is present. Standard NetworkPolicy cannot select FQDNs, so
operators must use stable CIDRs, private endpoints, or CNI/egress-gateway
features. L4 policy cannot isolate `/metrics` from other routes on port 8001;
application auth still protects query/history traffic. Kind's default CNI does
not enforce NetworkPolicy, so Phase 10 disables it and policy structure is
validated through Helm rendering and tests.

## 7. Ingress & TLS Contract

Ingress remains disabled by default. It supports host, class, annotations, path,
service port, and TLS Secret configuration. Its default path is `/query`, covering
both query variants while excluding probes, metrics, docs, schema, memory, and
admin operations. No controller, certificate, cert-manager, DNS, or gateway was
installed. Forwarded headers are not used for security decisions; trusted proxy
configuration remains an operator/runtime responsibility.

## 8. Container / Pod Security

The Docker image now declares `USER 10001:10001` and copies application content
with matching ownership. Final inspection and execution confirmed that identity.
The Helm chart retains fixed non-root UID/GID, RuntimeDefault seccomp, all
capabilities dropped, no privilege escalation, no privileged mode, and disabled
service-account-token automount. No RBAC objects were added because PolyMind does
not call the Kubernetes API.

`readOnlyRootFilesystem` remains false. Current runtime model downloads and
Python/Hugging Face/Torch caches require writable home/cache paths; local memory,
local Chroma, and temporary-file workflows also write in development. Phase 12
must package models and identify explicit minimal writable mounts first.

## 9. Request Abuse Controls

`MAX_REQUEST_BYTES` defaults to 1 MiB and is validated between 1 byte and 10 MiB.
A pure ASGI middleware checks declared length and counts received chunks, rejecting
oversized normal and streaming requests with sanitized 413 before orchestration.
Ingress/gateway limits are still recommended for defense in depth.

No concurrency semaphore or rate limiter was added. A per-process limiter would
not be replica-consistent, and safe capacity values do not exist yet. Gateway rate
limiting and capacity-derived concurrency bounds remain later work.

## 10. Threat Model

`docs/security/threat-model.md` identifies credentials, conversation state,
indexed data, prompts, retrieved content, and model output as assets. It describes
client, ingress, inference, Redis, Chroma, monitoring, and ingestion trust
boundaries. Threats include unauthenticated use, leakage, public metrics, lateral
movement, unrestricted egress, oversized requests, destructive ingestion,
dependency impersonation, and supply-chain risk, with implemented and residual
mitigations stated separately.

## 11. Security Observability

Two bounded metric families were added: `authentication_requests_total` with
endpoint-class/outcome labels and `request_rejections_total` with
endpoint-class/reason labels. Security logs contain request ID, endpoint class,
reason, and outcome only. Tokens, Authorization headers, prompts, IPs, history,
and documents are not logged or used as metric labels.

## 12. CI Security

CI now installs Helm 3 through the pinned `azure/setup-helm@v4.3.0` action, lints
and renders the chart, and validates Compose configuration in addition to compile,
pytest, and Docker build checks. Dedicated gitleaks, pip-audit, and Trivy binaries
were not locally available and were not added as fragile decorative steps.
Dependency/container scanning, SBOM generation, signing, and digest-based releases
remain future supply-chain work, preferably after Phase 12 reduces the image and
dependency surface.

## 13. Files Changed

Modified:

- `.env.example`
- `.github/workflows/ci.yml`
- `Dockerfile`
- `README.md`
- `api/app.py`
- `config/settings.py`
- `deployment/helm/polymind/README.md`
- `deployment/helm/polymind/templates/configmap.yaml`
- `deployment/helm/polymind/templates/deployment.yaml`
- `deployment/helm/polymind/templates/secret.yaml`
- `deployment/helm/polymind/values.yaml`
- `deployment/kind/phase10/phase10.sh`
- `deployment/kind/phase10/values.yaml`
- `docker-compose.yml`
- `llm/metrics.py`
- `tests/unit/test_api_reliability.py`
- `tests/unit/test_deployment_topology.py`
- `tests/unit/test_helm_chart.py`

Added:

- `api/security.py`
- `deployment/helm/polymind/templates/networkpolicy.yaml`
- `docs/security/threat-model.md`
- `docs/security/production-security.md`
- `docs/codex/prompts/phase_11.md`
- `docs/codex/reports/phase_11_report.md`

Deleted:

- None.

## 14. Dependencies / Tooling

Repository dependencies: none added, removed, or upgraded.

Local tools: existing Python environment, Docker, kubectl, and the Phase 10
temporary Helm 3.18.6/Kind 0.29.0 tools were reused. No dependency, scanner,
identity platform, CNI, ingress controller, or certificate tool was installed.

## 15. Tests Added / Updated

Tests cover local auth-disabled behavior; missing, malformed, incorrect, and valid
bearer credentials; query, streaming, and memory route protection; absence of
token leakage; request-size rejection before processing; docs URL policy;
production rejection of disabled auth, missing/short/whitespace tokens, and
enabled docs; Secret/ConfigMap wiring; secure chart defaults; NetworkPolicy
selectors and DNS; public Ingress exclusions; TLS rendering support; non-root
image declaration; Phase 10 auth compatibility; and exact request-size rendering.

The final full suite passed 164 tests.

## 16. Validation Results

- `pytest`: 164 passed in 15.65 seconds on the final run with Helm on PATH; no skips.
- Compile validation: passed using
  `PYTHONPYCACHEPREFIX=/tmp/polymind-phase11-compile python -m compileall -q .`.
- `git diff --check`: passed.
- Helm lint: one chart linted, zero failures; optional icon recommendation only.
- Helm template: default, TLS-enabled Ingress, and empty-ingress-deny renders
  passed; exact `MAX_REQUEST_BYTES: "1048576"` rendering verified.
- Docker build: passed using cache as `polymind:phase11`.
- Docker runtime: configured/running user was UID/GID 10001; image size was
  3,175,517,003 bytes.
- Kind: guarded `kind-polymind-phase10` / `polymind-phase10` release revision 10
  reached two ready replicas. `/health`, `/ready`, and `/metrics` passed;
  unauthenticated query returned 401; `/docs` returned 404; authenticated query
  and authenticated NDJSON metadata/chunks/done streaming passed.
- NetworkPolicy enforcement: not claimed; Kind's default CNI does not enforce it.
- Secret scan: targeted diff/repository key, credential, private-key, wildcard
  egress, and privilege patterns passed. The pre-existing ignored `.env` was not
  read, modified, or tracked; one explicitly named synthetic Kind token remains.
- Dependency scan: not run; no scanner installed.
- Container scan: not run; no scanner installed.

## 17. Implementation Self-Review

Review and live validation found four material defects. Initial body pre-reading
through function middleware could deadlock, so security and size enforcement were
implemented as one pure ASGI boundary. Helm serialized an unquoted request limit
in scientific notation, so the value is now explicitly string-typed and
regression-tested. The first live stream exposed a cross-worker ContextVar reset;
the redundant generator token handling was removed because the ASGI middleware
owns correlation for the whole stream. Finally, whitespace-only bearer tokens and
null ingress rules were hardened through validation and explicit `ingress: []`.

After fixes, review confirmed protected-mode enforcement, uniform 401 behavior,
token-safe logs, streaming completion, bounded labels, production docs shutdown,
external Secret wiring, bounded selectors, DNS rules, no public metrics path,
unchanged probe behavior, preserved provider boundaries, and no later-phase work.

## 18. Pre-Commit Review

The working tree contains only Phase 11 implementation, tests, chart, CI,
documentation, and phase artifacts. No `.env`, credential, private key, generated
manifest, unrestricted egress, privileged setting, cloud integration, OAuth,
service mesh, dependency change, or unrelated refactor is included. API response
and NDJSON formats, request IDs, probes, metrics, Redis, Chroma, BM25, both
inference providers, Helm, Compose, and Phase 10 behavior remain compatible.

Remaining warnings are the synthetic local-only Kind token, Helm's optional chart
icon recommendation, the non-enforcing Kind CNI, and the large image/read-write
root filesystem already assigned to Phase 12.

No commit was created.
No push was performed.

## 19. Documentation

The root README and Helm runbook now describe authentication, local/production
defaults, request size, endpoint exposure, Secret rotation, NetworkPolicy,
external egress limitations, TLS/Ingress, metrics protection, and Kind behavior.
`docs/security/production-security.md` is the production security runbook;
`docs/security/threat-model.md` captures assets, trust boundaries, threats,
mitigations, and residual risks. The prompt and this report are preserved under
`docs/codex/` without changing earlier phase artifacts.

## 20. Remaining Risks / Technical Debt

### Phase 11 concerns

- One static bearer token has no identity, tenant, scope, or dual-token rotation.
- NetworkPolicy is L3/L4, cannot select FQDNs, and shares port 8001 with metrics.
- Policy enforcement depends on the production CNI and was not enforced in Kind.
- Ingress/gateway TLS, certificate, request limit, and rate-limit behavior remain
  operator responsibilities.
- The chart defaults are intentionally restrictive and require real environment
  selectors/CIDRs before dependencies become reachable.
- No dedicated secret, dependency, or container scanner was executed.

### Deliberately deferred security/platform work

- OAuth/OIDC, tenant authorization, gateway deployment, distributed rate limits,
  service mesh/mTLS, external secret operators, cloud secret stores, certificate
  automation, dedicated metrics listener, SBOM/signing/admission policy, PDB,
  topology spread, graceful stream draining, autoscaling, monitoring platforms,
  load testing, vLLM/GPU, and cloud deployment.

## 21. Phase 12 Readiness

`READY`

The security boundary is operationally validated and introduces no dependency or
provider coupling. Phase 12 can focus on deterministic embedding/reranker artifact
packaging, eliminating runtime downloads, splitting control-plane dependencies,
removing unnecessary CUDA/GPU packages, reducing the 3.18 GB image, defining
explicit writable cache/temp paths, and determining whether production can enable
a read-only root filesystem. It should preserve the Phase 11 auth, Secret,
NetworkPolicy, ingress, and non-root contracts.
