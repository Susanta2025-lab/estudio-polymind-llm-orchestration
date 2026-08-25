# Phase 14 Report — Production Observability Integration & Capacity Calibration

## 1. Phase Result

PASS

Phase 14 delivers and validates a monitoring-platform-neutral scrape, aggregation,
query, SLI, alert, and future custom-metric contract. It deliberately does not
deploy HPA. A representative multi-node cluster and external inference service
remain required before selecting a production HPA target.

## 2. Baseline Observability Architecture

Before Phase 14, every Python process exposed bounded Prometheus metrics at
unauthenticated `/metrics` on the application port. Metrics were process-local;
the chart had a configurable monitoring NetworkPolicy peer but no scrape metadata,
operator discovery resource, collector, recording rules, dashboard/query catalog,
custom-metrics path, or fleet aggregation validation.

## 3. Final Observability Architecture

The final boundary is PolyMind pods -> optional pod annotations or optional
ServiceMonitor -> separately operated Prometheus-compatible collector ->
deployment-neutral recording/alert rules -> portable PromQL/runbook -> future
adapter -> future HPA. The application still only exposes metrics. The chart owns
no Prometheus server, Grafana, Alertmanager, adapter, or HPA.

## 4. Metrics Inventory

No application metrics were added because the existing set was semantically
sufficient. The authoritative inventory in `docs/operations/observability.md`
records metric type, labels, unit/meaning, and operational use for application
requests/duration/active work, NDJSON streams, inference calls/duration/TTFT/
errors/tokens, readiness, memory, vector store, BM25 initialization,
authentication, and security rejection metrics. All are process-local. Existing
labels remain bounded; no request, session, prompt, document, URL, key, identity,
or exception-message label was introduced.

## 5. Scrape Discovery

`monitoring.scrapeAnnotations` optionally emits configurable path, port, scheme,
and scrape annotations on every pod. An empty annotation port follows
`application.port`. Existing `podAnnotations`, including rollout annotations,
remain mergeable. `monitoring.serviceMonitor` optionally renders a
`monitoring.coreos.com/v1` ServiceMonitor selecting the release Service. It is
absent by default, so normal installation needs no Operator CRDs. The Kind
collector used pod annotation discovery and found both intended replicas.

## 6. Multi-Replica Aggregation

Counters use `rate`/`increase` before fleet `sum`, which tolerates pod resets.
Gauges sum for fleet concurrency and group by pod for imbalance. Histogram p95
rules apply `histogram_quantile` only after summing bucket rates by `le`; pod p95s
are never averaged. Live validation found two `up == 1` targets. During one long
stream, exactly one pod reported active application/NDJSON value 1 and the fleet
sum was 1. After rollout, new per-pod readiness series were independently present.

## 7. Recording Rules

Ten recording rules provide application request rate/error ratio/p95, inference
p95, TTFT p95, active application work by pod, separate active query and stream
series by pod, NDJSON streams by pod, and component readiness by pod. The future
adapter candidate is `polymind:active_query_requests:sum_by_pod`. Prometheus 3.5.5
validated 15 total recording and alert rules. Deterministic rule tests proved a
2 request/second fleet rate, the aggregated histogram p95 interpolation, and a
per-pod active-query value of 2.

## 8. Operational Queries / Dashboard

The portable runbook supplies PromQL for request success/rate/distribution,
application and inference latency, TTFT, stream duration/outcomes, normalized
provider errors, Redis/vector failures, active work, readiness, CPU throttling,
memory working set, and replica availability. A Grafana JSON artifact was not
added because a query catalog avoids datasource, namespace, and cluster coupling.

## 9. Metrics Security Boundary

`/metrics` remains unauthenticated on port 8001; scrapers do not receive the
application bearer token. The public Ingress still excludes metrics and probes.
Production operators must explicitly permit only reviewed monitoring namespace/
pod selectors through NetworkPolicy or an equivalent platform control. Because
L4 policy cannot distinguish paths on a shared port, an allowed scraper can reach
that port, but query/stream/memory remain bearer-protected. A second server/port
was not justified by current evidence and would add lifecycle complexity.

## 10. Golden Signals Coverage

- Latency: application, inference, TTFT, stream, memory, vector, and readiness
  histograms.
- Traffic: application/inference/memory/vector counter rates and token rates.
- Errors: application and stream outcomes, normalized provider/dependency errors,
  authentication decisions, and security rejections.
- Saturation: active application requests and NDJSON streams, correlated with
  platform-owned CPU throttling, memory, and replica metrics.

## 11. SLI Definitions

Measurable SLIs are completed-request success ratio, successful request latency
below a chosen histogram bucket, terminal stream completion ratio, TTFT below a
chosen bucket paired with stream completion, component readiness, and platform
available-replica time. Authentication/rejection traffic is separately measurable.
The application error outcome currently includes cancelled streams; strict
availability must join stream outcomes or later add a bounded cancellation outcome.

## 12. Candidate SLOs

**CANDIDATE — NOT PRODUCTION COMMITMENT:** future engineering targets may cover
availability/request success, per-operation p95 latency, stream completion, and
TTFT. Phase 14 sets no production percentage or latency threshold. Business
criticality, denominator/exclusion policy, maintenance policy, representative
inference, and target observation windows are prerequisites.

## 13. Alerting Contract

Five candidate rules cover no ready replica, sustained application errors,
sustained provider errors, component readiness failure, and sustained query
saturation. Every alert has a hold duration and `calibration: required`. The 5%
error and greater-than-two active-query values are calibration placeholders, not
production policy; no Alertmanager was deployed.

## 14. Capacity Calibration

The Phase 13 authenticated harness was reused. On the single-node Kind environment
at SHA `688c34c`, image `polymind:phase13`, two replicas, 100m/384Mi requests and
1 CPU/2Gi limits, direct concurrency 4 completed 20/20 with 3.294 requests/second,
p50 0.767s and p95 3.369s. A post-rollout concurrency-8 run completed 40/40 with
3.713 requests/second, p50 2.107s and p95 2.867s. No errors occurred. These small
fixture-based samples validate correlation plumbing only; scheduling noise means
they do not replace Phase 13 results or represent cloud sizing.

## 15. Scaling Signal Analysis

Active queries remain the preferred leading signal. Query work correlated with
the local latency knee, while a long stream demonstrated that stream lifetime can
remain active independently of constant local compute. Query and stream targets
therefore remain separate; an unweighted sum is rejected. CPU throttling is a
useful corroborating infrastructure signal. A weighted stream signal lacks evidence.

## 16. HPA Metric Readiness

READY WITH CONDITIONS

The per-pod recorded query series, target labels, aggregation semantics, and future
adapter boundary are validated. An adapter mapping must associate `namespace` and
`pod` with Kubernetes pod resources and publish a renamed pods custom metric.
Adapter discovery/RBAC and representative target calibration remain Phase 15 work.

## 17. HPA Threshold Calibration

REQUIRES TARGET-CLUSTER CALIBRATION

Kind and deterministic fixture data do not justify a production target.

## 18. Dependency Capacity Assumptions

Application scaling is safe only while inference duration/TTFT/errors, Redis
operation latency/errors/readiness, and Chroma operation latency/errors/readiness
remain within target envelopes. Rising dependency latency without local CPU
pressure indicates dependency saturation; adding PolyMind replicas could amplify
that load. Phase 14 does not scale any dependency.

## 19. Resource Baseline

RETAIN CURRENT DEFAULTS

Production requests remain 250m CPU/512Mi and limits remain 1 CPU/2Gi. The local
fixture and single-node samples are not stronger than Phase 13 evidence.

## 20. PDB / Topology / Startup Probe

PDB: DEFER. Topology controls: DEFER. Startup probe: NOT NEEDED. No new evidence
changed the Phase 13 conclusions, and no such resources were added.

## 21. Rollout-Safe Streaming Regression

The existing guarded in-cluster rollout test passed with two replicas and the
135-second termination grace. The client received metadata, chunks 0 through 39,
and the final `done` event while the Deployment rolled successfully. Active gauges
were observed during the stream and returned to zero afterward.

## 22. Files Changed

Modified: `README.md`, Helm README, Helm deployment/values, and Helm tests.

Added: optional ServiceMonitor template; Prometheus rules and deterministic test
fixture; scoped Phase 14 Kind validator configuration/manifests/README; operations
observability runbook; monitoring-contract tests; Phase 14 prompt and report.

Deleted: none.

The pre-existing user-owned `AGENTS.md` modification is excluded from Phase 14.

## 23. Dependencies / Temporary Tools

Repository dependencies: unchanged. Temporary tool: pinned
`prom/prometheus:v3.5.5` LTS image for `promtool` and scoped Kind collection. The
existing Helm binary, Docker, kubectl, Kind cluster, and Phase 13 image were reused.

## 24. Tests Added / Updated

Tests cover secure disabled defaults, annotation and optional ServiceMonitor
rendering, monitoring NetworkPolicy integration, absence of monitoring CRDs in
default output, bounded rule dimensions, counter-rate semantics, histogram bucket
aggregation, and per-pod active-query aggregation. Existing observability,
authentication, NDJSON, Helm security, and rollout tests were rerun.

## 25. Validation Results

- Starting SHA synchronized with `origin/master`; latest CI run 32808823615: green.
- `python -m pytest -q` with Helm on PATH: 178 passed in 49.90s.
- External-bytecode-cache `compileall`: passed.
- `git diff --check`: passed.
- Helm lint: 1 chart linted, 0 failed; icon recommendation only.
- Default Helm template: passed; no ServiceMonitor.
- Monitoring-enabled Helm template: passed; annotations, ServiceMonitor, and
  restricted monitoring ingress rendered.
- Prometheus 3.5.5 `check rules`: 15 rules, success.
- Prometheus deterministic `test rules`: success.
- `docker compose config --quiet`: passed.
- Application Docker build: not rerun because no application/container source or
  dependency changed; existing `polymind:phase13` was reused.
- Kind: two replicas Ready; both exposed metrics and were independently scraped;
  `count(up == 1)` returned 2.
- Live fleet aggregation: one active stream on one pod produced fleet total 1;
  per-pod readiness exposed four ready components on both pods.
- Counter reset behavior: immediately after rollout, five-minute rate was zero and
  histogram quantile `NaN` until sufficient samples, confirming why raw totals and
  premature quantiles are invalid; deterministic fixture validated populated math.
- Capacity: concurrency 4, 20/20; concurrency 8, 40/40; exact values in section 14.
- Metrics/security: `/metrics` 200 without token; query 401 without token; query
  and stream 200 with token; NDJSON ended in `done`.
- Rollout-safe stream: chunks 0–39 plus `done`, passed.
- Offline/non-root/read-only image validation: passed as UID/GID 10001 with CPU
  Torch, local embedding/reranker artifacts, and semantic routing.

## 26. Implementation Self-Review

Review found and fixed a stale Helm test that confused monitoring configuration
with public Ingress paths; an initial numeric-user omission in the temporary
Prometheus pod; accidental one-replica effective Kind values during validation;
scrape-port drift risk; and an overbroad availability-SLI statement that omitted
stream cancellation ambiguity. The release was restored to two replicas, the
validator uses UID/GID 65534, annotation port defaults to the application port,
and the SLI limitation is explicit. No application metric lifecycle defect was
found; gauges, terminal outcomes, TTFT, usage, and cancellation tests passed.

## 27. Pre-Commit Review

The working tree contains intended Phase 14 chart, rule, test, Kind-validation,
runbook, prompt, and report changes plus the separate pre-existing user-owned
`AGENTS.md` modification. No secret, bearer token, runtime `.env`, private key,
time-series database, benchmark dump, machine-specific repository path, debug
code, high-cardinality label, new dependency, application API change, HPA, PDB,
topology control, or startup probe was introduced. Compatibility and scope checks
passed. Temporary cluster resources were removed after evidence capture.

No commit was created.
No push was performed.

## 28. Documentation

README and Helm documentation describe the optional integrations and security
boundary. The operations runbook contains architecture, ownership, complete metric
inventory, discovery, NetworkPolicy, multi-replica math, correct histogram and
counter patterns, golden signals, queries, infrastructure boundary, SLIs,
candidate SLOs/alerts, dependency diagnosis, future adapter contract, stabilization
considerations, and target calibration procedure. Phase prompt/report artifacts
are preserved under `docs/codex`.

## 29. Remaining Risks / Technical Debt

### Phase 14 concerns

The same-port metrics boundary relies on network isolation; ServiceMonitor service
discovery normally observes ready endpoints while pod annotations can observe all
selected pods. Strict application availability cannot currently separate client
stream cancellation from other application errors without joining the stream
series. Live five-minute rate/quantile samples are sensitive to short test windows
and restarts. No representative external inference or multi-node target was
available, and no production SLO exists.

### Deliberately deferred platform work

Prometheus/managed collector operation, retention, dashboards, Alertmanager,
custom-metrics adapter, HPA, PDB, topology/failure-domain policy, cloud sizing,
multi-node disruption, production SLO/error-budget governance, dependency HA, and
inference-plane scaling remain operator or later-phase work.

## 30. Phase 15 Readiness

READY WITH CONDITIONS

Phase 15 — Validated Application Autoscaling remains the correct next phase once
a representative multi-node target environment and external inference endpoint
are available. It should validate the adapter mapping, select a target from
query/stream mix and cold/steady/burst evidence, define scale-up and scale-down
stabilization around the 135-second grace, verify dependency headroom, and only
then deploy an application HPA.
