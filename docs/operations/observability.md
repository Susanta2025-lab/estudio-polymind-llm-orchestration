# PolyMind observability contract

## Architecture and ownership

PolyMind exposes bounded Prometheus text at `GET /metrics` from every process.
The platform operator owns discovery, scraping, retention, rule evaluation,
dashboards, alert delivery, and any future custom-metrics adapter:

```text
PolyMind pods -> Prometheus-compatible scraper -> recording rules
              -> queries/alerts -> future adapter -> future HPA
```

The Helm chart does not install Prometheus, Grafana, Alertmanager, an adapter, or
an HPA. Generic pod annotations and a Prometheus Operator `ServiceMonitor` are
independently opt-in. Normal chart rendering requires no monitoring CRDs.

## Metrics inventory

All metrics are process-local. Scrape labels such as `namespace`, `pod`, and
`instance` are attached by the monitoring platform, not the application.

| Metric | Type | Application labels | Unit and meaning | Primary use |
| --- | --- | --- | --- | --- |
| `application_requests_total` | counter | `route`, `operation`, `outcome` | completed application requests | traffic, errors, availability |
| `application_request_duration_seconds` | histogram | `route`, `operation`, `outcome` | full query or iterator lifetime | latency |
| `active_application_requests` | gauge | `operation` | orchestration/iterator work currently active | saturation, future scaling |
| `active_ndjson_streams` | gauge | none | active response iterators | stream saturation/diagnosis |
| `ndjson_stream_outcomes_total` | counter | `outcome` | successful, errored, or cancelled iterators | streaming reliability |
| `inference_requests_total` | counter | `provider`, `logical_role`, `served_model`, `operation`, `outcome` | completed provider calls | provider traffic/errors |
| `inference_request_duration_seconds` | histogram | same as inference requests | provider call lifetime | provider latency |
| `inference_time_to_first_token_seconds` | histogram | `provider`, `logical_role`, `served_model` | first non-empty stream token | TTFT |
| `inference_stream_duration_seconds` | histogram | prior labels plus `outcome` | provider stream lifetime | stream latency/outcome |
| `inference_errors_total` | counter | `provider`, `operation`, `error_category` | normalized provider failures | provider errors |
| `inference_tokens_total` | counter | `provider`, `logical_role`, `served_model`, `token_type` | provider-reported tokens | workload characterization |
| `readiness_checks_total` | counter | `provider`, `outcome` | inference readiness decisions | dependency availability |
| `readiness_check_duration_seconds` | histogram | `provider`, `outcome` | readiness call duration | readiness latency |
| `memory_operations_total` | counter | `provider`, `operation`, `outcome` | memory operations | Redis/file traffic/errors |
| `memory_operation_duration_seconds` | histogram | same as memory operations | memory operation latency | dependency latency |
| `memory_errors_total` | counter | `provider`, `operation`, `error_category` | normalized memory failures | dependency errors |
| `memory_readiness_checks_total` | counter | `provider`, `outcome` | memory readiness decisions | dependency availability |
| `memory_readiness_check_duration_seconds` | histogram | `provider`, `outcome` | memory readiness latency | dependency latency |
| `vector_operations_total` | counter | `provider`, `operation`, `outcome` | vector operations | Chroma/local traffic/errors |
| `vector_operation_duration_seconds` | histogram | same as vector operations | vector operation latency | dependency latency |
| `vector_errors_total` | counter | `provider`, `operation`, `error_category` | normalized vector failures | dependency errors |
| `vector_readiness_checks_total` | counter | `provider`, `outcome` | vector readiness decisions | dependency availability |
| `vector_readiness_duration_seconds` | histogram | `provider`, `outcome` | vector readiness latency | dependency latency |
| `component_readiness` | gauge | `component` | latest readiness result, 1 ready/0 not ready | availability diagnosis |
| `bm25_snapshot_build_duration_seconds` | histogram | none | startup snapshot build latency | initialization |
| `bm25_snapshot_refresh_total` | counter | `outcome` | completed snapshot builds | initialization errors |
| `authentication_requests_total` | counter | `endpoint_class`, `outcome` | authentication decisions | security traffic/errors |
| `request_rejections_total` | counter | `endpoint_class`, `reason` | security-boundary rejections | security errors |

The label domains are configured or normalized and bounded. Request/session IDs,
queries, document IDs, URLs, keys, client identities, and exception strings are
forbidden. `_created` series emitted by the Python client are implementation
metadata, not operational SLIs.

## Discovery and security

Enable generic discovery with:

```yaml
monitoring:
  scrapeAnnotations:
    enabled: true
    path: /metrics
    port: "8001"
    scheme: http
networkPolicy:
  ingress:
    monitoring:
      enabled: true
      namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: monitoring
      podSelector:
        matchLabels:
          app.kubernetes.io/name: prometheus
```

For Prometheus Operator, enable `monitoring.serviceMonitor.enabled` and set
`additionalLabels` to labels selected by the operated Prometheus resource. The
ServiceMonitor selects the release Service, whose endpoint discovery yields all
ready pod endpoints. Annotation discovery targets pods directly. Preserve `pod`
and `namespace` target labels in either configuration.

`/metrics` is intentionally unauthenticated and shares port 8001 with probes and
the bearer-protected API. Scrapers do not need the application bearer token and
tokens never enter monitoring configuration or labels. The public Ingress does
not route `/metrics`; production must enable the chart's monitoring ingress rule
with reviewed namespace and pod selectors (or equivalent platform policy). A
standard L4 NetworkPolicy cannot distinguish paths on one port, so an allowed
scraper can technically reach the port's other routes; bearer authentication
still protects query, stream, and memory routes. A dedicated server/port would
add lifecycle and probe complexity and is deferred unless the target platform
cannot enforce this network boundary.

## Aggregation and query catalog

Counters reset when pods restart. Use `rate()` or `increase()`, then sum. Never
treat raw counter values as fleet lifetime totals. Gauges are summed for fleet
concurrency and grouped by `pod` for replica imbalance. Histograms must sum
bucket rates by `le` before `histogram_quantile`; averaging pod p95 values is
mathematically invalid. Install `deployment/monitoring/prometheus-rules.yaml` in
the separately operated Prometheus-compatible collector.

Traffic and success:

```promql
sum by (operation) (rate(application_requests_total[5m]))
sum(rate(application_requests_total{outcome="success"}[5m]))
  / clamp_min(sum(rate(application_requests_total[5m])), 1e-12)
```

Latency and TTFT:

```promql
histogram_quantile(0.95,
  sum by (operation, le) (rate(application_request_duration_seconds_bucket[5m])))
histogram_quantile(0.95,
  sum by (provider, operation, le) (rate(inference_request_duration_seconds_bucket[5m])))
histogram_quantile(0.95,
  sum by (provider, logical_role, le) (rate(inference_time_to_first_token_seconds_bucket[5m])))
histogram_quantile(0.95,
  sum by (outcome, le) (rate(inference_stream_duration_seconds_bucket[5m])))
```

Errors and dependency diagnosis:

```promql
sum by (operation) (rate(application_requests_total{outcome="error"}[5m]))
sum by (provider, operation, error_category) (rate(inference_errors_total[5m]))
sum by (outcome) (rate(ndjson_stream_outcomes_total[5m]))
sum by (provider, operation, error_category) (rate(memory_errors_total[5m]))
sum by (provider, operation, error_category) (rate(vector_errors_total[5m]))
min by (pod, component) (component_readiness)
```

Saturation and availability:

```promql
sum by (pod, operation) (active_application_requests)
sum(active_application_requests)
sum by (pod) (active_ndjson_streams)
kube_deployment_status_replicas_available{deployment=~".*polymind.*"}
sum by (pod) (rate(container_cpu_cfs_throttled_periods_total{container="polymind"}[5m]))
sum by (pod) (container_memory_working_set_bytes{container="polymind"})
```

CPU, memory, throttling, restart, replica, and node signals belong to
kubelet/cAdvisor, kube-state-metrics, Metrics Server, or the managed monitoring
platform. PolyMind does not duplicate them with process inspection.

## Golden signals and dependency saturation

- Latency: application duration, inference duration/TTFT/stream duration, memory
  and vector duration.
- Traffic: application, inference, memory, and vector counter rates and token rate.
- Errors: application outcomes, normalized provider/dependency failures, stream
  outcomes, authentication decisions, and rejections.
- Saturation: active application requests and streams, correlated with platform
  CPU throttling and memory metrics.

Rising active queries with application latency and CPU throttling, while provider,
memory, and vector latency remain stable, indicates application saturation. Rising
inference duration/TTFT or provider errors without corresponding local CPU pressure
indicates inference saturation. Rising memory or vector latency/errors/readiness
failures indicates Redis or Chroma saturation. Scaling PolyMind cannot repair the
latter cases and may amplify dependency load.

## SLIs, candidate SLOs, and error budgets

The following SLIs are technically measurable:

- request success: successful completed application requests divided by all
  completed valid application requests;
- request latency: successful request histogram observations below a selected
  bucket divided by successful observations;
- stream completion: successful terminal stream outcomes divided by all terminal
  stream outcomes;
- TTFT: successful stream observations below a selected TTFT bucket divided by
  successful streams with a recorded first token;
- component readiness: time-weighted readiness gauge and platform available
  replica signals.

Authentication failures and request-size rejections are excluded from the service
availability denominator unless product policy says otherwise. The application
counter currently combines cancelled streams with other `error` outcomes, so a
strict availability SLI must join the separate stream-outcome series or add a
future bounded cancellation outcome before adopting an error budget. Client
cancellation must be reported separately from server stream failure. TTFT currently
excludes streams that fail before first content, so pair it with stream completion.

**CANDIDATE — NOT PRODUCTION COMMITMENT:** target-environment data may support an
availability/success objective, an application p95 latency objective by operation,
a streaming completion objective, and a TTFT objective. No percentage or latency
threshold is committed in Phase 14. Business criticality, maintenance/exclusion
policy, representative external inference, and a multi-node observation window
are missing. Once selected, availability error budget is calculable as
`1 - SLO target` over the agreed valid-request denominator.

## Candidate alerts

The rule file includes candidate alerts for no ready replica, sustained application
errors, provider errors, component readiness failure, and sustained query
concurrency. Every alert has a `for` duration and `calibration: required`. The 5%
error ratio and two-query saturation threshold are placeholders for operational
validation, not production policy. Route alerts through dependency-specific
runbooks and tune them against target traffic to avoid low-volume noise.

## Application HPA contract

`polymind:active_query_requests:sum_by_pod` is the preferred adapter input.
Queries represent active synchronous orchestration and correlated best with the
Phase 13 local saturation region. Streams remain separate because a long-lived
stream can be active while consuming little local CPU. Do not sum query and stream
counts into one unweighted target. CPU is a corroborating guardrail, not the
application contract.

The reference Prometheus Adapter rule matches
`polymind:active_query_requests:sum_by_pod`, associates `namespace` and `pod` with
Kubernetes resources, and expose a renamed pods custom metric through
`custom.metrics.k8s.io`. Managed platforms may map the same recorded series; the
adapter is cluster infrastructure, not chart-owned or a mandatory vendor choice.

Metrics Server provides CPU/memory through `metrics.k8s.io`. It does not provide
this signal. Prometheus Adapter or an equivalent provider exposes the application
metric through `custom.metrics.k8s.io`; Phase 15 does not require Metrics Server.

Fresh processes eagerly expose `active_application_requests{operation="query"} 0`.
The recording rule retains only `namespace` and `pod` and requires a successful
current `up == 1` target, so idle is zero but scrape failure stays missing. The
adapter maps only Namespace and Pod and publishes
`polymind_active_query_requests`; removed pod resources cannot consume stale data.

The optional `autoscaling/v2` HPA uses a Pods metric and `AverageValue`. It is
disabled by default and requires explicit `maxReplicas` and
`targetAverageActiveQueries`. When enabled the Deployment omits `spec.replicas`,
so Helm does not fight HPA state. Scale-up is explicitly bounded; scale-down is
more conservative and must account for churn, long streams, rollout overlap, and
the 135-second termination grace. Disable by setting `autoscaling.enabled=false`
and deliberately restoring `replicaCount`.

The exact production target and maximum remain uncalibrated. Production needs
representative nodes and external inference, steady and burst traffic,
query/stream mixes, cold
replicas, dependency headroom, rollout overlap, and observation of latency, errors,
CPU throttling, memory, and dependency latency. Scale-up should react faster than
the sustained latency knee; scale-down needs stabilization longer than ordinary
stream/request churn and must respect the 135-second termination grace. Provider,
Redis, and Chroma capacity must be checked before increasing replica fan-out.

Calibration must measure per-replica active queries, latency, throughput, TTFT,
inference latency/errors, CPU/throttling, memory, readiness/cold-start distribution,
direct/RAG/stream mix, Redis/Chroma latency and headroom, external inference
headroom, scrape/rule/adapter delay, rollout overlap, and scale effectiveness.
Those observations determine target, maximum, policies, and stabilization. Roll
back when replicas rise without application improvement or dependency health
deteriorates.

Kind's `100m` target, maximum 4, and 60-second scale-down window prove only the
control loop. They do not establish production sizing, HA, dependency capacity, or
SLOs. Scaling PolyMind does not scale inference, Redis, or Chroma. CPU, memory,
latency, TTFT, errors, readiness, and streams remain calibration/rollback evidence,
not an unvalidated composite HPA signal.

Adapter aggregation-layer RBAC and TLS/APIService ownership remain separate. It
receives no application bearer token. PolyMind retains
`automountServiceAccountToken: false` and needs no Kubernetes API permissions.
`/metrics` remains excluded from public Ingress and requires network restriction.
PDB and topology defaults remain deferred pending SLO/failure-domain policy;
single-node Kind remains supported. Startup probe remains unnecessary because HPA
did not change the measured startup lifecycle.
