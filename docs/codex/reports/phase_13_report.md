# Phase 13 Report — Availability & Capacity Baseline with Rollout-Safe Streaming

## 1. Phase Result

PASS

Phase 13 established a bounded authenticated HTTP baseline, found an unsafe
30-second termination boundary for a 40-second stream, implemented a measured
135-second grace budget, and proved the same stream completes during direct pod
termination and a two-replica rollout. Local capacity evidence is explicitly a
single-node Kind baseline, not a production sizing guarantee.

## 2. Baseline Configuration

The unchanged production chart used two replicas; requests of 250m CPU/512Mi;
limits of 1 CPU/2Gi; liveness `/health` after 10 seconds every 10 seconds with a
2-second timeout and three failures; readiness `/ready` after 5 seconds every 10
seconds with a 5-second timeout and three failures; rolling update
`maxUnavailable: 0`, `maxSurge: 1`; and Kubernetes' implicit 30-second termination
grace. There was no startup probe, preStop, PDB, topology spread, HPA, or explicit
application drain state. Kind overrides requests to 100m/384Mi and shorter probe
delays but preserves the 1 CPU/2Gi limits.

Application generation read timeout was 120 seconds; readiness calls were bounded
to 1–5 seconds by dependency-specific configuration. Request bodies were capped
at 1 MiB. BM25 built synchronously in lifespan startup; embedding, reranker, and
semantic-route vectors loaded lazily. Uvicorn stopped accepting work on SIGTERM
and waited for responses, but Kubernetes killed work exceeding 30 seconds.

The image baseline was 732,420,653 bytes by Docker inspection. The Phase 13 image
is 732,428,052 bytes. The small source-only increase does not alter its CPU-only,
offline artifact architecture.

## 3. Benchmark Architecture

`scripts/capacity_baseline.py` is a Python-standard-library, real-HTTP harness.
It requires bearer authentication, supports direct, RAG, and NDJSON streaming
workloads, configurable URL/token/concurrency/count/duration/timeout, and hard
bounds of 32 workers, 1,000 requests, and 300 seconds. Count remains a hard cap in
duration mode. JSON output records run context, success/failure counts, bounded
error classes, throughput, latency p50/p95/p99, TTFT p50/p95, and stream duration.

The deterministic OpenAI-compatible Kind fixture isolates control-plane behavior.
Normal requests return fixed content; a Phase 13 marker returns 40 one-second
stream chunks. Tool routing was excluded from load curves because it bypasses
external inference and does not represent the target capacity boundary.

## 4. Measurement Environment

Measurements ran on Linux 6.6 WSL2, Docker 29.7.2, a single-node Kind cluster,
Git SHA `853d44c216631c0c63a7ca9cd9bdfee5ac98697f`, image
`polymind:phase13` (`sha256:d289ef…`), two API replicas, one deterministic Python
inference fixture, Redis 7.4 Alpine, and Chroma 1.5.9. The Kind override was
100m/384Mi request and 1 CPU/2Gi limit per API pod. Laptop scheduling, shared CPU,
single-node topology, fixture latency, and 20-request samples limit portability.
p99 from 20 samples is directional only.

## 5. Cold-Start Results

Fresh pods reached Kubernetes Ready 12 and 13 seconds after creation. BM25 build
was 0.655 seconds. Before lazy models, container working set was about 358.5 MiB.
The first direct request, including embedding load and semantic intent setup, took
1.604 seconds and raised working set to 381.8 MiB. The subsequent first RAG request,
including first reranker use, took 0.286 seconds and raised it to 389.5 MiB.

Independent offline container validation measured embedding load/encode 0.489
seconds, reranker load/predict 0.289 seconds, and semantic routing 0.328 seconds.
These overlap with the end-to-end observations and are not summed as separate
startup stages. Readiness does not initialize these lazy models.

## 6. Warm Performance Baseline

At concurrency 1 with 20 requests, direct p50/p95 was 0.053/0.087 seconds and
7.39 requests/s (one cold-tail sample made p99 1.671 seconds); RAG was
0.090/0.099 seconds and 10.17 requests/s; streaming was 0.046/0.057 seconds,
20.04 requests/s, with TTFT 0.044/0.055 seconds. The fixture and CPU scheduling
explain why route throughput is not a model-quality or external-vLLM result.

## 7. Concurrency & Capacity Results

| Workload | Concurrency | Success | RPS | p50 | p95 | TTFT p95 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| direct | 1 | 20/20 | 7.39 | 0.053s | 0.087s | n/a |
| direct | 4 | 20/20 | 8.44 | 0.497s | 0.629s | n/a |
| direct | 8 | 20/20 | 6.37 | 1.156s | 1.672s | n/a |
| RAG | 1 | 20/20 | 10.17 | 0.090s | 0.099s | n/a |
| RAG | 4 | 20/20 | 4.74 | 0.843s | 1.061s | n/a |
| RAG | 8 | 20/20 | 3.66 | 2.023s | 2.640s | n/a |
| stream | 1 | 20/20 | 20.04 | 0.046s | 0.057s | 0.055s |
| stream | 4 | 20/20 | 7.25 | 0.514s | 0.686s | 0.681s |
| stream | 8 | 20/20 | 4.92 | 1.453s | 2.234s | 2.187s |

The approximate local saturation region is 2–4 concurrent requests per replica:
latency rises steeply and throughput flattens or falls above it. This is an
engineering region, not an exact maximum. No errors occurred in the bounded final
curve.

## 8. CPU & Memory Results

Fresh working set was about 358.5 MiB; warm pods were approximately 389–405 MiB;
observed cgroup peak was approximately 406.5 MiB. Post-load state stayed stable
near 389–405 MiB; no leak trend was observed in these short samples. The cgroup
reported CPU throttling under the 1-core limit: the more-loaded pod accumulated
22.18 CPU-seconds throttled across 353 of 1,337 periods. This aligns with the
concurrency curve. No OOM or memory throttling occurred.

## 9. Dependency Behavior

The deterministic inference fixture kept upstream generation nearly constant, so
the concurrency curve primarily reflects semantic routing, embedding/reranking,
Python scheduling, and HTTP orchestration. Redis and Chroma latency did not show a
separate saturation signature in the modest curve. Scoped Redis loss made
readiness and query return sanitized 503; Chroma loss made readiness and RAG query
return sanitized 503; fully removed inference made readiness and direct query
return sanitized 503. Redis and inference recovered after restoration. Restarting
the intentionally ephemeral Chroma fixture removed its synthetic corpus, so the
documented bootstrap republished `phase10-v1` before API replicas rolled and
returned to Ready. An initial
inference scale-down observation remained 200 while its terminating fixture still
served, so it was repeated only after waiting for pod deletion.

## 10. Client Disconnect Behavior

A client disconnected before content and another during a long stream. After the
iterator boundary observed cancellation, `active_application_requests` and
`active_ndjson_streams` returned to zero and the cancellation counter reached two.
Both unique Redis histories remained empty; no incomplete answer was persisted and
no generation was retried. Provider responses close when generator cleanup runs.

The provider stack is synchronous. A thread already blocked in `requests.iter_lines`
cannot be forcibly cancelled safely; cancellation propagates when iterator control
returns. Phase 13 does not claim immediate upstream cancellation.

## 11. SIGTERM & Graceful Shutdown

Original behavior was measured first. Deleting the exact pod owning a controlled
40-second stream under the 30-second implicit grace produced 26 chunks and no
`done` event. After the change, the identical test produced all 40 chunks and the
final `done` event while the Deployment supplied its replacement. Lifespan cleanup
then closed BM25, Redis, Chroma, and the provider session.

## 12. Rolling-Update Streaming Test

The authoritative rollout test used a disposable in-cluster authenticated client
through the Kubernetes Service, avoiding port-forward pod-selection artifacts.
With two replicas, it opened the 40-second stream, waited five seconds, and
restarted the Deployment. The client received chunks 0–39 and `done`; new replicas
became ready and the rollout completed with at least one ready replica throughout.

An earlier host service-port-forward attempt truncated when the port-forward's
selected pod changed. That measured the tunnel, not Kubernetes Service drain, and
is deliberately excluded from acceptance evidence.

## 13. Availability Controls

The chart now explicitly sets `terminationGracePeriodSeconds: 135`: the 120-second
provider read timeout plus 15 seconds for application/transport shutdown. Streams
exceeding that bounded budget can be killed and remain non-retriable/non-persistent.
No preStop sleep or application drain coordinator was added. Kubernetes removes a
terminating pod from Service endpoints and Uvicorn stops new acceptance on SIGTERM;
the in-cluster evidence showed this was sufficient. Existing probe values were
retained.

## 14. Resource Recommendation

RETAIN CURRENT DEFAULTS

The production 512Mi request exceeds observed warm/peak local use, and 2Gi is far
above it. CPU throttling deserves target-cluster calibration, but a WSL2 single-node
Kind run cannot justify universal CPU changes. Values remain configurable.

## 15. Startup Probe Decision

NOT NEEDED

Ready occurred in 12–13 seconds, BM25 took 0.655 seconds, and liveness tolerates
roughly 30 seconds after its initial delay. Startup stayed well inside that window.

## 16. PDB Decision

DEFER UNTIL TARGET CLUSTER/SLO

Two replicas and `maxUnavailable: 0` protect controlled rollout, but PDB policy
requires voluntary-disruption expectations, node capacity, and a production SLO.

## 17. Topology Decision

Defer topology spread/anti-affinity until target-cluster topology is known. The
single-node Kind environment cannot validate failure-domain placement, and a hard
default would make the supported local deployment unschedulable.

## 18. HPA Readiness

HPA NOT YET READY

Active application requests is the best candidate leading signal because latency
degradation correlated with concurrent in-flight control-plane work and it avoids
scaling on long idle stream lifetime alone. CPU is a useful guardrail but is also
affected by local scheduling and model initialization. Process-local metrics still
need external aggregation/custom-metrics delivery and target-cluster calibration.
No HPA was deployed.

## 19. Observability Changes

Phase 13 adds `active_application_requests{operation}`,
`active_ndjson_streams`, and `ndjson_stream_outcomes_total{outcome}`. Labels are
bounded. Iterator-lifetime context managers guarantee decrements on success,
failure, `GeneratorExit`, and cancellation; they contain no request, session,
prompt, token, IP, or URL labels.

## 20. Files Changed

Modified: `README.md`, `api/app.py`, Helm README/deployment/values, the scoped Kind
inference fixture, `llm/metrics.py`, and Helm/observability tests.

Added: `scripts/capacity_baseline.py`, `tests/unit/test_capacity_baseline.py`,
`deployment/kind/phase13/README.md`, `deployment/kind/phase13/rollout_stream.sh`,
the Phase 13 prompt artifact, and this report.

Deleted: none.

## 21. Dependencies / Local Tools

Repository dependencies: unchanged. The harness uses the standard library.

Local tools: existing Docker 29.7.2, kubectl, and previously downloaded scoped
Kind/Helm binaries under `/tmp/polymind-phase10-tools`; no new tool was installed.

## 22. Tests Added / Updated

New harness tests cover authenticated headers, NDJSON TTFT/done parsing, bounded
HTTP errors, percentiles, safety limits, and duration-mode request caps. Metrics
tests cover active request and cancelled-stream cleanup. Helm tests cover the
explicit grace value and rendering. Existing API, provider, memory, retrieval,
streaming, security, container, and chart regression suites remain active.

## 23. Validation Results

- Latest CI for the starting SHA: success.
- `python -m pytest -q`: 173 passed, 1 skipped in 17.24 seconds. The only skip was
  PATH-based Helm discovery; direct Helm commands passed.
- External-cache compile validation: passed.
- `git diff --check`: passed.
- Helm lint: 1 chart linted, 0 failed; icon recommendation only.
- Helm template: passed and rendered two-replica security/rollout/grace controls.
- `docker compose config --quiet`: passed.
- Cached `docker build --tag polymind:phase13 .`: passed.
- Offline, networkless, read-only container model validation as UID/GID 10001:
  passed; CPU Torch, both artifacts, and semantic routing succeeded.
- Benchmark harness tests: 4 passed as part of the suite.
- Cold start/readiness, warm requests, concurrency, CPU, memory, client disconnect,
  direct SIGTERM, long-stream termination, two-replica rollout, dependency recovery,
  health/readiness, authentication, query, NDJSON, and security regressions: passed
  with the measurements reported above.
- Final live smoke: `/health` and composite `/ready` 200, unauthenticated query
  401, authenticated direct query successful, NDJSON ended in `done`, and 2/2
  Phase 13 replicas Ready with 135-second grace.

## 24. Implementation Self-Review

Review found and fixed a duration-mode safety bug that allowed rapid failures to
exceed the intended request count. Count is now always a hard cap and has a test.
Review also rejected service port-forward truncation as rollout evidence and
replaced it with an in-cluster Service client. Metrics were checked for bounded
labels and `finally` cleanup; provider-neutral boundaries and persistence semantics
remain unchanged. Final smoke also found that the ephemeral Chroma outage test had
discarded its corpus; the synthetic version was republished and readiness was
revalidated rather than masking the 503.

## 25. Pre-Commit Review

The working tree contains only intended Phase 13 source, chart, test, fixture, and
documentation changes. Secret scans found examples/placeholders and synthetic test
values only; no runtime `.env`, credential, private key, generated benchmark dump,
machine-specific repository path, debug code, unbounded load path, unsafe sleep in
production, dependency, or unrelated refactor was introduced. API/NDJSON contracts
remain compatible. The test-only sleeps are isolated to the deterministic Kind
fixture.

No commit was created.
No push was performed.

## 26. Documentation

README and Helm runbook document active metrics and the bounded termination budget.
The Phase 13 Kind guide documents methodology, limitations, harness use, and the
guarded in-cluster rollout test. This prompt and report are stored under
`docs/codex` without rewriting previous phase reports.

## 27. Remaining Risks / Technical Debt

### Phase 13 concerns

The capacity sample is small and laptop-specific; no production node, real vLLM,
or external metrics aggregator was measured. Synchronous provider reads delay
cancellation until iterator control returns. A stream beyond 135 seconds can be
terminated. Per-process gauges require aggregation across replicas. CPU throttling
needs target-cluster study.

### Deliberately deferred platform work

HPA, PDB, topology/failure-domain controls, cloud sizing, production SLOs,
Prometheus aggregation, multi-node disruption testing, external inference-plane
capacity, and dependency HA remain deferred.

## 28. Phase 14 Readiness

READY WITH CONDITIONS

**Evidence-Based Autoscaling & Disruption Controls** remains the correct tentative
next phase only after collecting the same harness and active-request signal on the
target cluster with representative external inference. That phase can then decide
custom-metric aggregation, HPA policy, PDB, and topology controls from a stated SLO;
it should not infer them solely from this Kind baseline.
