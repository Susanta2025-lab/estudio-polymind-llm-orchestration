# Phase 10 — Kubernetes Validation, Local Cluster Deployment & Operational Testing

## 1. Phase Result

`PASS`

The Phase 9 chart was exercised on a real dedicated Kind control plane. The
actual repository image ran under the chart security context, reached readiness,
served normal and streaming requests, operated with two replicas, degraded and
recovered correctly, reconciled a deleted pod, rolled forward, and rolled back.

## 2. Local Kubernetes Environment

- Platform: Kind, selected because Docker was already available and there was no
  existing Kubernetes context to protect.
- Docker: 29.5.2 (build `79eb04c`).
- Docker Compose: 5.4.0.
- Kubernetes server: 1.33.1 (`kindest/node:v1.33.1`).
- kubectl client: 1.36.1, Kustomize 5.8.1.
- Helm: 3.18.6.
- Kind: 0.29.0 (Go 1.24.2, linux/amd64).
- Cluster/context: `polymind-phase10` / `kind-polymind-phase10`.
- Namespace/release: `polymind-phase10` / `polymind`.

kubectl warned that client 1.36 and server 1.33 exceed the supported one-minor
skew. No command failed because of the skew, but matching kubectl to the cluster
minor is recommended for repeat validation.

## 3. Deployment Architecture

The Helm release owns only the PolyMind Deployment, ClusterIP Service,
ConfigMap, ServiceAccount, and references to a separately created Secret. Test
fixtures outside the chart provide ephemeral Redis 7.4, Chroma 1.5.9, and a tiny
OpenAI-compatible HTTP stub. A short-lived pod based on the real PolyMind image
performs deterministic Chroma upsert/version publication.

This topology proves external-service integration but is not production
infrastructure. The fixtures make no durability, HA, capacity, authentication,
or security-hardening claim. Redis, Chroma, and inference were not added to the
production chart.

## 4. Static Helm Validation

`helm lint deployment/helm/polymind` linted one chart with zero failures; Helm
only recommended an optional chart icon. Default and Phase 10 `helm template`
commands succeeded. Kubernetes server-side dry-run accepted the rendered
ServiceAccount, ConfigMap, Service, Deployment, and all seven fixture resources.

Selectors, ports, probe paths, Secret/ConfigMap references, security contexts,
resource values, local image policy, and disabled-by-default Ingress were
inspected. No Redis, Chroma, inference, StatefulSet, hostPath, Docker socket, or
Ingress workload appeared in the default production render.

## 5. Image Build & Cluster Loading

The application image was tagged `polymind:phase10`, built with ordinary cached
`docker build`, and loaded directly with `kind load docker-image`; nothing was
pushed. `imagePullPolicy: Never` exists only in the Phase 10 values file. The
large Python/ML dependency installation layer remained cached on every rebuild.

The first real pod found that UID 10001 had no passwd entry and Torch failed at
import-time username resolution. The Dockerfile now creates the matching
`polymind` UID/GID 10001 account. Rebuilt pods then started successfully without
relaxing Kubernetes security.

## 6. Cluster Deployment

The dedicated namespace contains the `polymind` Helm release, two PolyMind API
pods, one Redis fixture pod, one Chroma fixture pod, one inference stub pod, and
their ClusterIP Services. Configuration is in `polymind-polymind`; the Redis URL
is in the separately created `polymind-phase10-secrets` Secret. The optional API
key is absent because the test stub does not require authentication.

The initial Redis fixture failed because its root entrypoint could not call
`setpriv` after all capabilities were dropped. Running it directly as the
image's built-in UID 999/GID 1000 fixed startup while retaining dropped
capabilities and disabled privilege escalation.

## 7. Liveness & Readiness

Before corpus bootstrap the fixed application process stayed Running,
`/health` returned 200 `{"status":"alive"}`, `/ready` returned 503 with Chroma
`collection_unavailable` and `bm25_uninitialized`, and the Service had no API
endpoint. After bootstrap/restart, inference, Redis, Chroma, and BM25 all
reported ready and the endpoint appeared.

During Redis outage `/health` remained 200 while `/ready` returned 503
`memory_unreachable`; the same two processes stayed Running. Redis restoration
returned both pods to readiness without restarting them.

## 8. BM25 Operational Validation

The deterministic bootstrap upserted one synthetic document and published
`phase10-v1`; startup loaded that version and readiness became true. Later
publications exercised v2 and v3. Operational testing discovered that Chroma's
collection object cached metadata, so existing pods initially missed a new
publication. `corpus_version()` now refreshes the collection from Chroma on each
check, with a focused regression test.

After the fix, publishing v3 while two pods loaded/expected v2 caused both to
return 503 `bm25_version_mismatch` and leave Service endpoints while remaining
alive. A Helm rollout setting expected v3 created two new ready replicas whose
startup snapshots matched the published version. No request-time rebuild was
introduced.

## 9. End-to-End API Validation

`POST /query` with synthetic content routed `direct` and returned the configured
logical role/model plus `Phase 10 response` from the real OpenAI-compatible
adapter. `X-Request-ID: phase10-correlation` was preserved in the response.

`POST /query/stream` returned newline-delimited JSON metadata, two chunks
(`Phase 10 ` and `response`), and a done event. Upstream SSE therefore remained
behind the provider boundary and the PolyMind client contract remained NDJSON.

## 10. Multi-Replica Validation

Helm revision 3 scaled the release to two replicas. Both became Ready and the
EndpointSlice contained two ready pod IPs. Both built the same process-local
BM25 version and contacted the shared Chroma and Redis Services. A synthetic
query created a two-message Redis list, and the API could read that state through
the Service. This validates replica compatibility, not production HA.

## 11. Failure & Recovery Tests

Scaling only `deployment/phase10-redis` to zero made both API endpoints not-ready
while both containers remained Running and live. Restoring it to one recovered
2/2 readiness and both endpoints.

Deleting the explicitly resolved pod UID
`708e5adb-6e71-4792-a617-b4d7eeab2865` caused the Deployment to create a
replacement with a different UID. The release returned to 2/2 Ready, and the
Service still read the synthetic two-message Redis session after replacement.

## 12. Rolling Update & Rollback

The v3 corpus/config upgrade rolled two replicas with `maxUnavailable: 0` and
`maxSurge: 1`; each replacement became ready before the old pod terminated.
A separate harmless annotation upgrade created revision 6. `helm rollback
polymind 5 --wait` created revision 7, restored annotation `corpus-v3`, retained
BM25 v3, and completed at two desired/two ready replicas.

One earlier revision was intentionally retained as failed evidence after an
incorrect CLI `--set` key rendered an annotation object. Kubernetes rejected it
and the live revision remained healthy; using a simple string key fixed the
operational command. No template change was required.

## 13. Security Validation

Live PolyMind containers ran as UID 10001 with `runAsNonRoot: true`, GID/fsGroup
10001, RuntimeDefault seccomp, `allowPrivilegeEscalation: false`, and all Linux
capabilities dropped. Service-account token automount was false. Requests were
100m CPU/384Mi memory and limits were 1 CPU/2Gi memory under the local override.

No privileged mode, hostPath, Docker socket, host mount, or chart-bundled
dependency was present. Secrets were referenced through a Secret, not embedded
in the ConfigMap. The ephemeral Chroma fixture runs with its upstream image
identity and is explicitly not presented as production-hardened infrastructure.

## 14. Metrics Validation

`/metrics` returned Prometheus exposition beginning with
`# HELP inference_requests_total`. No Prometheus server was deployed, no Ingress
was enabled, and access used a local port-forward. Metrics remain per process;
production monitoring must scrape each replica and aggregate externally.

## 15. Files Changed

Modified:

- `Dockerfile`
- `Makefile`
- `README.md`
- `rag/chroma_store.py`
- `tests/unit/test_deployment_topology.py`
- `tests/unit/test_helm_chart.py`

Added:

- `deployment/kind/phase10/README.md`
- `deployment/kind/phase10/bootstrap_corpus.py`
- `deployment/kind/phase10/fixtures.yaml`
- `deployment/kind/phase10/kind-config.yaml`
- `deployment/kind/phase10/phase10.sh`
- `deployment/kind/phase10/values.yaml`
- `docs/codex/prompts/phase_10.md`
- `docs/codex/reports/phase_10_report.md`

Deleted:

- None.

## 16. Dependencies / Tooling

Repository dependency changes: none.

Local tooling was not installed globally. Standalone Helm 3.18.6 and Kind 0.29.0
were downloaded under `/tmp/polymind-phase10-tools`; they are the smallest tools
required for native chart and local-control-plane validation. No vLLM, CUDA,
GPU, cloud CLI, schema validator, or unrelated package was installed.

## 17. Tests Added / Updated

Tests now cover non-sensitive local overrides, fixed image policy, fixture/chart
separation, exact cluster/context/namespace guards, scoped destructive commands,
absence of hostPath/Docker socket/global prune, fixture non-root identity, the
image's UID 10001 passwd contract, and native Helm lint/render when Helm exists.

A focused adapter regression changes a simulated remote corpus version and
proves two consecutive `corpus_version()` calls observe v1 then v2 instead of
returning cached collection metadata.

## 18. Validation Results

- `pytest`: 146 passed in 13.45 seconds on the final run.
- Compile validation: passed with `PYTHONPYCACHEPREFIX` pointing to a temporary
  external directory.
- `git diff --check`: passed.
- `helm lint`: 1 chart linted, 0 failed; optional icon recommendation only.
- `helm template`: default and Phase 10 renders passed.
- kubectl dry-run: server accepted four rendered chart resources and seven
  fixture resources.
- Docker build: passed; final dependency layers cached; tag `polymind:phase10`.
- Cluster creation: passed; dedicated Kind Kubernetes 1.33.1 node Ready.
- Helm deployment: install revision 1 passed; final deployed revision 7.
- Readiness: verified 503 before corpus, 200 after bootstrap, 503 for Redis
  outage, recovery to 200, and 503 for stale BM25 followed by rollout recovery.
- API smoke: `/query` 200; request correlation passed; `/query/stream` NDJSON
  metadata/chunks/done passed.
- Multi-replica: two ready pods and two ready endpoints passed.
- Failure/recovery: Redis outage/recovery and pod replacement passed.
- Rollout: v3 and harmless annotation rollouts passed.
- Rollback: revision 6 back to revision 5 configuration passed as revision 7.
- Security inspection: live UID, seccomp, capabilities, escalation, token,
  resources, mounts, ConfigMap, and Secret boundaries passed.
- Secret scan: no committed credential, key, private key, `.env`, or sensitive
  Secret value finding.

## 19. Implementation Self-Review

Review found three material defects and one command error. The Redis fixture
needed its known non-root UID because capability dropping prevented its
entrypoint transition. The application image needed a real UID 10001 passwd
entry. Chroma version readiness needed a fresh collection metadata read. All
three were fixed and regression-covered. The malformed annotation `--set` was
corrected operationally; Kubernetes safely rejected that revision.

The complete diff preserves API formats, provider boundaries, external-service
ownership, process-only liveness, controlled BM25 lifecycle, and cloud/GPU-free
CI. No automatic rebuild, production dependency bundling, or unrelated platform
work was introduced.

## 20. Pre-Commit Review

The working tree contains only Phase 10 changes and remains based on
`master...origin/master` at Phase 9 commit `185f02e`. Secret/configuration scans
found only obvious synthetic local endpoints and the ephemeral Redis URL created
at runtime. No `.env`, API key, private key, host-specific path, debug artifact,
generated manifest, unsafe arbitrary-cluster command, privileged workload,
hostPath, Docker socket, production Redis/Chroma/vLLM bundle, or unrelated
dependency was introduced.

The dedicated cluster remains available for user inspection; the guarded
`destroy` command deletes only `polymind-phase10`.

No commit was created.
No push was performed.

## 21. Documentation

The root README now distinguishes local Kind validation from production
Kubernetes, describes creation/build/load/deploy/bootstrap/readiness/versioning,
scaling, outage recovery, pod replacement, rollback, port-forwarding, and
teardown. The fixture README documents prerequisites, fixed safety boundaries,
workflow, and non-production limitations. The Phase 10 prompt and this report
are preserved under `docs/codex/`.

## 22. Remaining Risks / Technical Debt

### Phase 10 concerns

- kubectl 1.36 versus Kubernetes 1.33 exceeds supported minor skew; use a 1.33
  client for the cleanest repeat run.
- The first semantic-router query downloads/initializes the configured
  sentence-transformer model and is materially slower than subsequent calls.
- The local Redis/Chroma fixtures are ephemeral and intentionally unauthenticated.
- One failed Helm revision remains in the disposable local release history as
  evidence of safe API rejection.
- The dedicated test cluster was retained for review and still consumes local
  Docker resources until `make k8s-phase10-destroy` is run.

### Deliberately deferred production infrastructure work

Managed Kubernetes, external durable/HA Redis and Chroma, production inference,
TLS/authentication, secret management, ingress, network policy, observability
infrastructure, autoscaling, disruption budgets, multi-node/failure-domain
testing, capacity/load testing, GPU/vLLM deployment, and cloud provisioning
remain outside Phase 10.

## 23. Next-Phase Readiness

`READY WITH CONDITIONS`

The deployment foundation is operationally proven and the two discovered
production-path defects are fixed. The next phase should define a production
environment contract/runbook (external service security, secrets, network
policy, disruption and availability objectives, and observability integration)
before any cloud-specific rollout. Repeat the Kind workflow with a Kubernetes
1.33-compatible kubectl and decide whether the semantic-router model should be
prepackaged or otherwise managed for deterministic cold starts.
