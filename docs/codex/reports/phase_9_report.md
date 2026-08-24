# Phase 9 — Kubernetes & Helm Deployment Foundation Report

## 1. Phase Result

`CONDITIONAL PASS`

The requested production-style Kubernetes foundation is implemented and all
available repository, static chart, compile, Compose, and Docker validations
pass. The result is conditional only because the `helm` executable is not
installed in the validation environment, so native `helm lint` and `helm
template` execution could not be completed locally. No live cluster is required
or used.

## 2. Kubernetes/Helm Architecture

The chart deploys a configurable number of PolyMind FastAPI control-plane pods
behind one Kubernetes Service. A rolling Deployment connects every replica to
the same separately operated OpenAI-compatible inference endpoint, Redis memory,
and Chroma HTTP vector store. Configuration is held in a ConfigMap and sensitive
connection material comes from a Kubernetes Secret. An Ingress can route to the
Service but is disabled by default.

The chart does not contain StatefulSets, dependency subcharts, data-plane
Deployments, cloud resources, or cluster provisioning.

## 3. Chart Structure

The chart is located at `deployment/helm/polymind` and contains:

- `Chart.yaml` and production-oriented `values.yaml`;
- helper-based names, labels, and selectors;
- Deployment, Service, ConfigMap, Secret, ServiceAccount, and Ingress templates;
- a chart-specific deployment and operations runbook.

Make targets provide `helm-lint`, `helm-template`, and combined `helm-validate`
commands. They perform client-side validation and do not require a cluster.

## 4. Configuration and Secret Strategy

The ConfigMap exposes only application-supported settings: production deployment
mode, OpenAI-compatible inference and model mapping, Redis memory selection,
Chroma HTTP location/collection/TLS, BM25 corpus version, API port, and bounded
dependency/readiness timeouts. Uvicorn is explicitly started on the configured
application port, avoiding divergence from the image's fixed default command.

`REDIS_URL` is a mandatory Secret key. `OPENAI_COMPATIBLE_API_KEY` is an optional
Secret key because some private inference services do not require one. By
default, the chart references a separately managed `polymind-secrets` Secret.
Optional chart-managed Secret creation requires the Redis value at render time;
all committed secret values are empty. No real credentials are present.

Logging level and metrics enablement were not added because the application has
no corresponding settings. Inventing chart-only variables would imply behavior
that does not exist. The existing `/metrics` endpoint remains available.

## 5. Liveness/Readiness Probes

Liveness calls `/health`, which is process-only and does not contact dependencies.
Readiness calls `/ready`, which preserves Phase 8G behavior: inference discovery,
Redis, Chroma, and the local BM25 snapshot/version must all be ready. Probe timing
and thresholds are configurable. `/metrics` is not used as a probe.

This separation lets dependency outages remove pods from Service endpoints while
avoiding restarts of otherwise live API processes.

## 6. Security Context

Default pod/container controls run as UID/GID 10001, require non-root execution,
drop all Linux capabilities, deny privilege escalation, and select the runtime
default seccomp profile. Service-account token automounting is disabled. The
container is not privileged.

The root filesystem remains writable because the current Python/ML runtime may
write caches. Tightening this requires an image/runtime change and writable
volume review, so it was not asserted speculatively in this deployment-only
phase. Ingress is off by default. `/metrics` shares the API port and the runbook
requires network restriction; this phase does not introduce a network policy,
authentication system, or service mesh.

## 7. External Service Boundaries

PolyMind owns FastAPI, LangGraph/RAG orchestration, request correlation,
provider configuration, health/readiness, and per-process metrics. External
operators own inference/vLLM, Redis persistence/availability, Chroma storage and
availability, TLS, credentials, backup, and network access.

No Redis, Chroma, vLLM, GPU, Prometheus, ingress-controller, certificate-manager,
or cloud-provider resource is bundled or deployed. The defaults use non-loopback
placeholder DNS names and production provider selections, consistent with Phase
8G startup validation.

## 8. Files Changed

Modified:

- `Makefile`
- `README.md`

Added:

- `deployment/helm/polymind/Chart.yaml`
- `deployment/helm/polymind/values.yaml`
- `deployment/helm/polymind/README.md`
- `deployment/helm/polymind/templates/_helpers.tpl`
- `deployment/helm/polymind/templates/configmap.yaml`
- `deployment/helm/polymind/templates/deployment.yaml`
- `deployment/helm/polymind/templates/ingress.yaml`
- `deployment/helm/polymind/templates/secret.yaml`
- `deployment/helm/polymind/templates/service.yaml`
- `deployment/helm/polymind/templates/serviceaccount.yaml`
- `tests/unit/test_helm_chart.py`
- `docs/codex/prompts/phase_9.md`
- `docs/codex/reports/phase_9_report.md`

No application interface, endpoint, dependency, Docker topology, or GitHub
Actions workflow was changed.

## 9. Tests Added/Updated

`tests/unit/test_helm_chart.py` checks the complete chart file set, production and
secret-safe defaults, required environment names, probe paths, ConfigMap/Secret
separation, security settings, and disabled Ingress. When Helm is installed, it
also runs native lint/render checks and asserts the expected rendered resource
set. The test skips that one integration check cleanly when Helm is absent.

## 10. Validation Results

- `python -m pytest`: **passed**, 140 passed and 1 Helm-dependent test skipped.
- Targeted Phase 9/topology tests: **passed**, 17 passed and 1 skipped.
- `git diff --check`: **passed**.
- `PYTHONPYCACHEPREFIX=/tmp/polymind-phase9-pycache python -m compileall -q .`:
  **passed**.
- `docker compose config --quiet`: **passed**.
- `docker build .`: **passed**, using cached dependency layers and without
  `--no-cache`.
- `helm lint deployment/helm/polymind`: **not run**, Helm unavailable.
- `helm template polymind deployment/helm/polymind`: **not run**, Helm
  unavailable.

No Kubernetes cluster, external inference, Redis, or Chroma service was contacted.
CI was not changed because adding a Helm installation solely for this phase would
expand the existing workflow; the Helm-aware automated test will activate in an
environment where Helm is already installed.

## 11. Documentation Updates

The main README identifies the chart, topology, external dependencies, validation
command, probe semantics, and metrics warning. The chart runbook covers Secret
creation, values, lint/render, install/upgrade, rollout observation, rollback,
BM25 publication ordering, security defaults, metrics restriction, and excluded
infrastructure. The Phase 9 prompt is preserved under `docs/codex/prompts`.

## 12. Remaining Risks/Technical Debt

- Native Helm lint/render remains to be executed in a Helm-equipped environment.
- The default image repository and external DNS endpoints are explicit
  placeholders and must be overridden before deployment.
- A production image tag or digest should be pinned; the chart's empty tag falls
  back to the chart app version for a renderable default.
- Resource defaults are starting points and require workload-specific tuning.
- The writable root filesystem reflects current image/runtime behavior.
- Metrics, API authentication, network policy, TLS termination, disruption
  budgets, autoscaling, and dependency HA remain operator/platform concerns.
- BM25 publication and rollout ordering remains the Phase 8G operational contract;
  this chart does not automate ingestion or corpus coordination.

Self-review found no provider-specific behavior leaking into application code,
no new API behavior, and no bundled external services. Pre-commit review found no
credentials, private keys, `.env` files, debug statements, generated artifacts,
new dependencies, or unrelated modifications.

## 13. Next-Phase Recommendation

Before a real environment rollout, run `make helm-validate` with a supported Helm
release, render a reviewed environment-specific values file, publish and verify
the matching BM25 corpus version, confirm the image runs under UID 10001, and
exercise a staged upgrade/rollback in a non-production namespace. A later,
explicitly scoped platform phase can decide on network policy, PodDisruptionBudget,
autoscaling, secret-manager integration, ingress/TLS, and managed dependency HA.

No commit was created.
No push was performed.

