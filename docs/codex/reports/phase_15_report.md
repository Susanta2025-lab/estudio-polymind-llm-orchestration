# Phase 15 Report — Validated Application Autoscaling

## 1. Phase Result

PASS

## 2. Baseline

- Starting branch: `master`.
- Starting HEAD: `8ea8e24234eea73ea541d97ea751b6c3f9b0404b`.
- Remote synchronization: read-only `git ls-remote` showed `origin/master` at the same SHA.
- Starting CI: Estudio PolyMind CI run 32826557410 completed successfully for that SHA.
- Initial working tree: clean; `git status --short --branch` was `master...origin/master`.

## 3. Final Autoscaling Architecture

PolyMind → Prometheus scrape → `polymind:active_query_requests:sum_by_pod` →
Prometheus Adapter → `custom.metrics.k8s.io` → `autoscaling/v2` HPA → PolyMind
Deployment replicas. Prometheus and adapter remain separately operated cluster
infrastructure.

## 4. Scaling Signal

The primary signal is the average number of active synchronous `/query` requests
per selected PolyMind pod. It is a Pods custom metric with `AverageValue`; fleet
totals, active streams, and CPU are not substituted for it.

## 5. Idle-Zero Metric Hardening

`Metrics` eagerly initializes the bounded `query` and `stream` gauge children to
zero. Fresh Ready pods therefore publish honest zero before first traffic. Existing
context-manager `finally` cleanup preserves success/error/cancellation semantics;
tests prove repeated use returns to zero and never produces a negative sample.

## 6. Recording Rule

The rule sums only `operation="query"` by `namespace,pod`, then intersects it with
a successful `up == 1` target on the same labels. No dynamic labels survive. Idle
live pods remain zero; missing/failed targets are not indiscriminately zero-filled.

## 7. Prometheus Adapter Contract

`deployment/monitoring/prometheus-adapter-values.yaml` maps only namespace and pod
resources, renames the series to `polymind_active_query_requests`, and filters with
adapter label matchers. It is outside the application chart and is portable to an
equivalent managed custom-metrics provider.

## 8. Custom Metrics API

The Kind APIService became Available and discovery exposed
`pods/polymind_active_query_requests`. Both current pods independently returned
zero when idle. A deleted scale-up pod returned `NotFound`, proving it was not
associated with its stale Prometheus series.

## 9. HPA Design

- API: `autoscaling/v2`.
- Metric: `Pods` custom metric `polymind_active_query_requests`.
- Target: `AverageValue`.
- Enablement: disabled by default; enabling requires explicit maximum and target.

## 10. Replica Bounds

The availability-oriented chart minimum is 2. Kind uses maximum 4 only to bound
the test. Production `maxReplicas` has no default and requires target-cluster and
dependency-capacity calibration; two replicas alone is not a production HA claim.

## 11. Scale-Up Behavior

The chart supplies bounded Pods/Percent policies and a short stabilization window.
The Kind override uses one pod per 15 seconds with no stabilization for a bounded,
deterministic functional test. This is not a production-tuned policy.

## 12. Scale-Down Behavior

Chart scale-down is materially more conservative (300-second stabilization and
bounded policies). Kind shortens it to 60 seconds and one pod per 30 seconds. The
135-second termination grace remains; a 40-second live stream completed safely
while the query metric stayed zero.

## 13. Dependency Capacity Safeguards

HPA scales neither inference, Redis, nor Chroma. The Kind maximum is bounded, all
three dependencies stayed Ready, and direct/RAG/load requests succeeded. Production
enablement requires latency, TTFT, error, readiness, CPU/throttling, memory, and
dependency-headroom rollback criteria; no composite metric was invented.

## 14. Security / RBAC

PolyMind retains `automountServiceAccountToken: false`, mounts no API token, and
`auth can-i get pods` returned `no`. Adapter aggregation RBAC/TLS is separate. No
bearer token is in monitoring config; `/metrics` remains absent from public Ingress.

## 15. Helm Integration

New values and `templates/hpa.yaml` follow chart names/selectors. Default rendering
contains no HPA and keeps `replicas: 2`. Enabled rendering targets the Deployment,
has explicit behavior, and omits Deployment `spec.replicas` so Helm does not fight
the HPA. Existing probes, grace, security, and monitoring defaults remain intact.

## 16. Kind End-to-End Validation

On positively identified `kind-polymind-phase10`, two Ready pods exposed idle zero;
Prometheus scraped them; the hardened rule evaluated; adapter discovery and pod
queries succeeded; HPA consumed the metric; authenticated load raised it; replicas
scaled and became Ready; load remained serviceable; metrics returned to zero; and
replicas stabilized back at two.

## 17. Scale-Up Result

During 8-way load Prometheus observed per-pod query values 8 and 0 and HPA showed
`4/100m`. Deployment moved 2 → 4; new pods were Ready at approximately 14 and 29
seconds. All 120 requests succeeded in 50.825 seconds.

## 18. Scale-Down Result

After load, the query metric returned zero. With the Kind 60-second stabilization
and one-pod/30-second policy, replicas transitioned 4 → 3 → 2. Final HPA conditions
were AbleToScale/ReadyForNewScale and ScalingActive/ValidMetricFound.

## 19. Streaming Regression

A long authenticated stream produced 42 events: metadata, 40 chunks, and one done,
with zero errors. During it, query gauge was 0, stream and NDJSON gauges were 1,
so it did not drive query autoscaling. Completed assistant memory was present.

## 20. Authentication Regression

Unauthenticated `/query` returned 401. Authenticated direct, RAG, stream, and memory
requests succeeded. Public health/metrics behavior and protected-route bearer
semantics were unchanged.

## 21. Metrics / Adapter Validation

Promtool found 15 valid rules and deterministic rule tests passed. Adapter static
tests validated exact series/name/resource mapping and bounded dimensions. Live
API discovery, two independent idle zeros, active values, HPA consumption, removed
pod `NotFound`, and final zero were observed.

## 22. Tests Added / Updated

Tests cover initial zero, repeated/error cleanup, non-negative bounded gauges,
live-target rule gating, adapter mapping, HPA disabled default, explicit required
settings, API/type/target/ref/behavior, and omission of Deployment replicas. Kind
fixtures add only a synthetic delayed query path and a bounded load client.

## 23. Validation Results

- Final full suite: 181 passed in 33.98 seconds (initial full run: 22.82 seconds).
- Targeted initial run: 22 passed, 2 PATH-based Helm skips; explicit-Helm run: 11 passed.
- Helm lint: 1 chart, 0 failures; default and HPA renders passed.
- Prometheus: 15 rules valid; deterministic tests SUCCESS.
- Compile with external cache: passed.
- `git diff --check`: passed at validation time.
- `docker compose config --quiet`: passed.
- Kind control loop, auth, direct/RAG, NDJSON, memory, RBAC, and stale-pod tests: passed.

## 24. Docker / Image Regression

Cached `polymind:phase15` build passed with no dependency change. Image ID is
`sha256:97892234...`, inspect size 732,443,727 bytes, user `10001:10001`, with no
CUDA/NVIDIA/Triton history match. Live chart pods retained read-only root, bounded
`/tmp`, non-root identity, baked offline artifacts, and became Ready.

## 25. Implementation Self-Review

Review replaced naive idle-series assumptions with eager initialization, rejected
PromQL blanket zero-fill, added `up == 1` gating, required explicit HPA target/max,
omitted Deployment replicas under HPA, and verified deleted pods cannot resolve a
stale metric. An initial adapter discovery check occurred before APIService startup;
diagnostics showed healthy TLS/API aggregation and subsequent availability.

## 26. Pre-Commit Review

Final review covered every changed file, secret patterns, generated artifacts,
dependencies, RBAC, public exposure, HPA defaults, production-value leakage, and
scope. `git diff --check` passed. Git status contains only the 12 intended modified
files and 8 intended new Phase 15 files summarized in this report;
no unrelated tracked change is present.

## 27. Documentation

Updated README, Helm README, and observability runbook. Added Phase 15 Kind guide,
reference adapter values, clean prompt artifact, and this report.

## 28. Production Calibration Status

REQUIRES TARGET-CLUSTER CALIBRATION

## 29. Production Enablement Status

READY WITH CONDITIONS

The portable control loop is correct. Operators must calibrate target, maximum,
policies, and windows on representative target infrastructure and validate external
inference, Redis, and Chroma headroom plus rollback thresholds before enablement.

## 30. Remaining Risks / Technical Debt

Phase 15 concerns: the same-port metrics boundary remains network-policy dependent;
Kind is single-node with deterministic inference; adapter/rule/scrape delays and
scale behavior differ by platform; application fan-out can saturate dependencies.

Deliberately deferred infrastructure: PDB, topology/failure-domain controls, VPA,
Cluster Autoscaler, KEDA, cloud-specific integration, inference/Redis/Chroma/GPU
autoscaling, production monitoring ownership, SLOs, and multi-node disruption.

## 31. Phase 16 Readiness

The next useful phase should be target-environment calibration and dependency
headroom/rollback validation if representative infrastructure is available.
Otherwise no production autoscaling phase should proceed from Kind evidence alone.

## 32. Completion Confirmation

No commit was created. No push was performed.
