# Phase 16 Report — Target-Environment Capacity Calibration & Dependency Headroom Validation

## Current status — 2026-10-04 operator-created AKS assessment

Gate: **PARTIALLY READY — INFRASTRUCTURE READY, DEPENDENCIES INCOMPLETE**.

AKS is now positively identified and reachable: two Ready nodes, no observed node
pressure, and successful read-only inventory. The earlier infrastructure/access
blockers are resolved. Representative inference, Redis, Chroma and an approved
AKS-pullable PolyMind image are not established; Prometheus/Adapter/custom metrics
are not installed. No deployment or load testing was performed.

Final Phase 16 verdict: **BLOCKED — REPRESENTATIVE DEPENDENCIES NOT AVAILABLE**.
See **2026-10-04 — Operator-created AKS readiness assessment** at the end for
current evidence. All preceding attempts below remain historical records.


## Historical status after the 2026-10-03 AKS continuation

**BLOCKED — AKS ACCESS INCOMPLETE**. AKS is now the explicit deployment decision,
but refreshed Azure discovery returned one accessible subscription and zero AKS
clusters. The intended cluster has not been positively identified. No AKS power
state, dependency readiness or calibration result can be established.

See **Phase 16 AKS Continuation** below for the current evidence and prerequisites.
Sections 1–38 immediately below preserve the initial assessment as historical
context; their deployment-choice uncertainty and authorization limits describe
that earlier attempt, not the user's subsequent AKS decision and scoped permission.

## Initial readiness attempt — historical record

Assessment date: 2026-10-03.

## 1. Phase result

**BLOCKED**

Readiness classification: **BLOCKED — TARGET ENVIRONMENT NOT REPRESENTATIVE**.

No representative PolyMind target was positively identified. The only configured
Kubernetes context is local Kind and its API is unavailable. Read-only Azure
inspection found a Container App, but did not establish that it serves PolyMind
or is the intended target. No AKS resource was listed in the successfully
inspected subscription. A second cached subscription could not be inspected.
Consequently, this is a bounded discovery result, not proof that suitable
infrastructure exists nowhere.

The readiness gate stopped implementation and calibration. No load, inference
request, cloud deployment, scaling change, dependency interruption, or Kubernetes
mutation was performed. All production capacity values remain unknown.

## 2. Starting repository state

- Branch: existing `master`.
- HEAD: `036b847ae3a722d3aa261d332ccd99928360d672`.
- Initial `git status --short --branch`: `## master...origin/master`, clean.
- No fetch or remote-state check was performed; the tracking display is local metadata.

Reviewed `AGENTS.md`, README, the Phase 15 report, observability runbook, chart
values/templates and runbook, monitoring rules/adapter mapping, Kind assets, and
relevant Helm, monitoring, provider/readiness and streaming tests. The current
chart confirms the Phase 15 HPA contract. Prior Kind results were treated as
historical functional evidence only.

## 3. Target-environment description and discovery evidence

| Read-only inspection | Observed result | Limit |
| --- | --- | --- |
| `kubectl config current-context` and `get-contexts -o name` | Only `kind-polymind-phase10` | No configured representative remote Kubernetes target |
| `docker ps` after sandbox-approved retry | Exit 0, no running containers listed | Applies to the selected Docker daemon only |
| Explicit-context Kind node, Deployment/HPA and custom-metrics APIService reads | Connection refused, exit 1 | Live node count, replicas and metrics cannot be established |
| Filtered `az account show` | Enabled default account; user authentication | Does not prove least-privilege RBAC or target data-plane access |
| Filtered `az account list` | Two cached Enabled subscription entries | Cached account entries do not prove live access |
| `az resource list` for the default subscription | Successful inventory of 12 resources | No claim about resources outside visible scope |
| `az resource list` for the second subscription | Exit 3, `SubscriptionNotFound` | Its inventory is unknown; no login or account change attempted |
| `az containerapp list` for the successfully inspected subscription | One app, provisioning Succeeded, Running; minimum 0, maximum 1 | Configured bounds, not measured current replica count or capacity |

The 12 visible resources comprise a Cognitive Services account and project,
a registry, two managed identities, a Container Apps environment and app, a Log
Analytics workspace, a Key Vault, a static site, a PostgreSQL flexible server and
a CIAM directory. No AKS, VM, managed Redis, or Azure Monitor workspace resource
was listed. This does not rule out external dependencies or services hidden by
scope/access limits.

The Container App and both container images did not match `polymind` by name.
Environment variable names indicated a different application configuration and
did not include the PolyMind inference/memory/vector/BM25 configuration contract.
These observations do not establish ownership or intended use; the app was not
adopted as a benchmark target. Its containers request 0.5 CPU/1 GiB and 1 CPU/2 GiB
respectively. Those settings are not PolyMind sizing evidence.

Most visible resources are in Spain Central; the static site is in West US 2 and
the directory reports Europe. Inventory locations establish no application
network path, latency, inference throughput or cross-region behavior.

Azure CLI initially could not write its local session metadata within the
sandbox; the approved retry succeeded. Docker and Kubernetes reads also required
sandbox-approved retries. Only local CLI session metadata and temporary tooling
were written by discovery; no cloud resource was changed. Reports retain no
subscription IDs, tenant IDs, cloud resource names/IDs, endpoints, secret values,
connection strings or raw upstream error bodies.

## 4. Readiness gate

| Requirement | Finding |
| --- | --- |
| Identified representative environment | Not established; local Kind configuration and an unconfirmed Azure app only |
| External inference | Cognitive Services resources exist, but no PolyMind-compatible endpoint, served-model mapping, access, health or capacity verified |
| Shared Redis | No target service identified; external service availability unknown |
| Shared Chroma | No target service identified; external service availability unknown |
| Monitoring | Log Analytics exists; PolyMind scraping/rules/telemetry not verified |
| HPA custom metrics | Repository contract exists; no accessible target API path verified |
| Multiple application replicas | Not demonstrated; discovered app is configured for at most one replica |
| Multiple nodes/failure domains | Not established; Kind source configuration has one control-plane node |
| Scoped credentials/permissions | Some Azure inventory reads succeeded; second scope unavailable; target RBAC/data-plane permissions unknown |

Readiness remains **BLOCKED — TARGET ENVIRONMENT NOT REPRESENTATIVE**. Successful
read-only calls demonstrate only those operations, not that credentials permit
only scoped work. No writes were used to test permissions, and no Kubernetes
credentials were imported or contexts changed.

## 5. Deployment-model compatibility

The implemented chart requires a Kubernetes Deployment and `autoscaling/v2` HPA,
a Pods metric exposed by `custom.metrics.k8s.io`, and the Phase 15 recording rule.
The discovered Container App is not evidence of that control loop. Its replica
bounds cannot calibrate the chart's `AverageValue`, HPA policies, adapter delay,
or Kubernetes scale/termination behavior.

If Container Apps is confirmed as the sole intended deployment target, the HPA
calibration objective has a deployment-model mismatch and needs an explicit scope
or architecture decision. That choice was not inferred from an unrelated or
unconfirmed existing app. No KEDA integration or alternative scaler was added.

A representative PolyMind deployment on Container Apps could eventually measure
single-container direct/RAG/stream behavior, dependency latency, resource usage,
network effects and dependency headroom under approved bounded tests. It could
not validate this Kubernetes HPA implementation, multi-node Kubernetes behavior,
or transfer its platform scaling observations into Kubernetes production values.
None of those Container Apps workload measurements was performed here.

## 6. Application topology

No live PolyMind target topology was established. Source defaults are recorded
below for traceability, not as a deployed baseline:

| Chart setting | Existing value |
| --- | --- |
| Fixed replicas / HPA minimum | 2 / 2 |
| Autoscaling enabled | false |
| Maximum / active-query target | null / null |
| CPU request / limit | 250m / 1 CPU |
| Memory request / limit | 512Mi / 2Gi |
| Termination grace | 135 seconds |
| Rolling update | zero unavailable, one surge |
| Inference / memory / vectors | openai_compatible / redis / chroma_http |
| Corpus version | `production-v1`, example configuration, not a verified publication |
| Pod annotations / ServiceMonitor | disabled / disabled |

Live image revision, current replica count, resource usage, HPA configuration and
health/readiness are unknown. Code and existing tests retain process-only
`/health` and dependency/BM25-aware `/ready`; no live target probes were sent.

## 7. Inference topology

The application retains its provider-neutral inference boundary. The chart uses
an external OpenAI-compatible service and logical-role model mapping. The Kind
fixture is a deterministic inference stub. Neither the example chart endpoint
nor the existence of Cognitive Services proves a usable representative inference
service. No model discovery, generation, GPU activation or inference mutation
was attempted.

## 8. Redis topology

Production chart configuration expects shared Redis through an externally managed
Secret. Kind fixtures describe ephemeral Redis. No target Redis endpoint,
connection budget, memory capacity or replica-shared history behavior was
verified. Secrets were not retrieved to search for a possible service.

## 9. Chroma topology

The chart expects shared Chroma HTTP and an immutable published corpus version
matching each process's startup BM25 snapshot. Kind supplies a fixture service.
No live target collection, publication version, persistence, vector query latency
or concurrent-replica behavior was verified. No ingestion or reset was run.

## 10. Monitoring/custom-metrics topology

The source contract remains:

```text
Per-pod query gauge -> Prometheus recording rule
-> polymind:active_query_requests:sum_by_pod
-> adapter -> pods/polymind_active_query_requests
-> custom.metrics.k8s.io -> autoscaling/v2 HPA
```

The recording rule requires successful scrape targets; missing telemetry must
not be interpreted as idle zero. Active streams remain excluded. The chart owns
no monitoring stack or adapter. A visible Log Analytics workspace does not prove
Prometheus scraping, rule evaluation, adapter registration or metric availability.
The local Kind APIService could not be read because the API was unavailable.

## 11. Benchmark methodology

No benchmark was executed because the gate failed. Discovery used read-only
control-plane calls and sanitized summaries. No laptop or Kind timing was
substituted for target measurements. Local automated-test duration is software
regression evidence only.

On resumption, first freeze the deployed baseline, identify the client location,
workload/corpus/model mix, token budgets and warm/cold state, and agree finite
request, duration and cost budgets plus abort criteria. Correlate client results,
per-pod metrics, HPA observations and dependency telemetry over the same time
windows. Record sample counts and tail-latency uncertainty, successful and failed
requests separately, and routing evidence for direct versus RAG requests.

## 12. Workload matrix

| Workload | Idle, steady, burst, sustained, recovery | Concurrency 1, 2, 4, 8 |
| --- | --- | --- |
| `/query`, direct | Not run | Not run |
| `/query`, RAG | Not run | Not run |
| `/query/stream` | Not run | Not run |

These concurrency levels are a proposed staged sequence only. Starting at one
and advancing requires a passed gate, explicit budgets and stable guardrails;
eight is not a demonstrated safe level. No numeric durations or sample sizes
were invented without knowing the available service and cost envelope.

## 13. Direct-query results

Not measured. Throughput, active-query saturation, p50/p95/p99, errors and timeouts
are unknown. No safe per-replica traffic rate can be recommended.

## 14. RAG-query results

Not measured. Retrieval/reranking contribution, Chroma latency, BM25 version
consistency and concurrent-replica memory semantics remain unverified on target.
Existing mocked/local tests do not establish target capacity or consistency.

## 15. Streaming results

Not measured on target. TTFT, generation duration, completion, cancellation
cleanup and rollout/termination outcomes have no Phase 16 target evidence.
Existing streaming tests ran in the local suite. The separate stream gauges and
135-second termination grace were preserved without modification.

## 16. Application capacity observations

**PolyMind API headroom: unknown.** No representative running replica or workload
measurements were available. CPU, memory, throttling, restarts, readiness churn,
queueing and latency knee cannot be classified. Container App resource settings
and historical Kind measurements do not answer these questions.

## 17. Inference headroom

**Inference headroom: unknown.** No verified target telemetry for latency, TTFT,
errors, overload, queueing, concurrency, token throughput or GPU utilization.
Supported PolyMind replica count is unknown.

## 18. Redis headroom

**Redis headroom: unknown.** No target command latency, connection count, memory
pressure, timeout rate or readiness telemetry. Supported replica count is unknown.

## 19. Chroma headroom

**Chroma headroom: unknown.** No target query latency, concurrent-query behavior,
errors or readiness telemetry. Supported replica count is unknown.

## 20. Network observations

No client-to-PolyMind or PolyMind-to-inference/Redis/Chroma latency measurements
were made. Azure control-plane discovery is not a measurement of those paths.
No regional or cross-region performance claim is supported.

## 21. Scale-up behavior

Unmeasured on target. Existing chart defaults are a 30-second stabilization window,
`Max` selection, and policies of one pod or 100 percent per 60 seconds. These are
source configuration only; no reaction time, readiness delay or scaling benefit
was observed in Phase 16.

## 22. Scale-down behavior

Unmeasured on target. Existing defaults are a 300-second stabilization window,
`Min` selection, and policies of one pod or 50 percent per 60 seconds. The
135-second grace remains unchanged. Terminating replicas and rollout surge can
continue consuming dependency capacity; HPA maximum alone is not a complete
concurrency budget.

## 23. Recommended HPA target

**Unknown; no numeric recommendation.** Keep autoscaling disabled pending
calibration. The actual chart key is `autoscaling.targetAverageActiveQueries`,
which renders `spec.metrics[].pods.target.averageValue` with type `AverageValue`.
The prompt's `targetAverageValue` denotes that objective; it is not an existing
values key and no alias or rename was introduced.

There is no evidence supporting a value or range. The Kind `100m` target must not
be copied into a production values file.

## 24. Recommended maximum replicas

**Unknown; no numeric recommendation.** `autoscaling.maxReplicas` remains null.
Neither the Kind maximum of four nor the discovered app maximum of one establishes
a safe PolyMind ceiling. No production override was created.

## 25. Recommended scaling policies/windows

No calibrated replacement is justified. Existing disabled-chart defaults remain
unchanged and are not endorsed as production-tuned values. Selecting policies
requires measured dependency ceilings, scale effectiveness, cold-start and
monitoring delays, request/stream durations and termination overlap. Do not
shorten the 135-second grace to force faster convergence.

## 26. Dependency capacity ceiling

| Component | Headroom | Evidence basis |
| --- | --- | --- |
| PolyMind API | unknown | No identified representative running target |
| Inference | unknown | No verified endpoint/model/capacity telemetry |
| Redis | unknown | No verified shared target or telemetry |
| Chroma | unknown | No verified shared target/corpus or telemetry |
| Monitoring/custom metrics | unknown | No verified target scrape/rule/adapter path |

The weakest dependency, safe fan-out and operational reserve remain unknown.
No formula can turn missing observations into a maximum. Future capacity planning
must include simultaneous streams, probes, cold starts, surge and terminating
pods, as well as synchronous queries driving the HPA.

## 27. Rollback criteria

Observed capacity thresholds: **none**. Numeric latency, error, timeout, memory,
restart and stabilization thresholds remain **unknown**. Existing alert thresholds
are calibration placeholders and were not adopted as production rollback policy.

Provisional safety rules for a future approved test, not validated business SLOs:
stop issuing load if required custom metrics disappear, a required component
becomes unready, a test-induced overload/OOM/restart occurs, or the agreed
request/time/token budget is reached. Do not increase concurrency while application
or dependency errors are unexplained. Before testing, set baseline-relative
p95/TTFT and timeout/error stop thresholds with an observation window and adequate
sample count; those numbers cannot yet be supplied.

Before any future autoscaling enablement, record a reviewed fixed replica count
and prior Helm revision. A rollback would restore that known-safe configuration
and disable autoscaling deliberately, preserving stream grace. There is no
verified safe fixed count or deployed revision to select today, and no rollback
was executed. Increasing API replicas must not be used to conceal dependency
failure.

## 28. Candidate operational SLOs

No business SLO or numeric candidate was established. Future candidate dimensions
remain availability, direct/RAG latency, TTFT, stream completion and readiness
stability. Define denominators, distinguish client cancellation from server
failure, and pair TTFT with pre-first-token failures. Targets and time windows
require representative evidence and owner agreement.

## 29. Failure/recovery observations

No live failure injection, dependency interruption, rollout or recovery test was
performed. The unavailable local Kind API is a discovery limitation, not a
controlled recovery experiment. Existing mocked failure and cleanup tests provide
regression evidence only; autoscaling under target dependency failure remains
unverified.

## 30. Tests and validation

| Command/check | Outcome |
| --- | --- |
| `python -m pytest -q` | **179 passed, 2 skipped in 19.78 seconds**, exit 0 |
| `PYTHONPYCACHEPREFIX=/tmp/polymind-phase16-pycache python -m compileall -q .` | Exit 0 |
| `docker compose config --quiet` | Exit 0 |
| `helm lint deployment/helm/polymind` | Could not execute: Helm not installed/on PATH, shell exit 127 |
| `helm template polymind deployment/helm/polymind` | Could not execute: Helm not installed/on PATH, shell exit 127 |
| Previously used temporary Helm binary | Absent in this session |
| `git diff --check` | Exit 0 at final review |

The two skipped tests are the Helm lint/render test and explicit HPA required-value
test. Static Helm/monitoring tests and the remaining suite passed. No dependencies
were installed to complete an already-blocked calibration. Docker build and
live Prometheus/Kind checks were not run: implementation, dependencies, images
and deployment configuration are unchanged. No new tests were added for these
documentation-only artifacts.

## 31. Implementation self-review

Reviewed the prompt/report and source contract for unsupported claims, environment
confusion, architecture impact and benchmark bias. The report distinguishes
unknown from absent, configured replica limits from running replicas, and cloud
inventory from usable PolyMind dependencies. The second subscription's failure
prevents an exhaustive Azure absence claim. The discovered Container App is not
asserted to be the intended target. All headroom classifications are unknown.

No application interfaces, provider boundaries, streaming signal, termination
behavior or configuration keys changed. No target benchmark was executed and no
historic local measurement was promoted to production evidence.

## 32. Pre-commit review

The change set contains only the requested prompt and this report. Review covers
secret/token/private-key patterns, connection strings, cloud identifiers, local
paths, temporary artifacts, debug output, dependency changes and unsupported
claims. No credentials or private configuration were copied. Temporary discovery
tooling and the external bytecode cache remain outside the repository; no load
harness or raw Azure output was added. The `/tmp` compile path records the cache
workaround and is not runtime configuration. No generated logs or `.env` changes
are included. No staging, commit or remote operation was performed.

## 33. Documentation changes

Added the clean supplied prompt at `docs/codex/prompts/phase_16.md` and this report
at `docs/codex/reports/phase_16_report.md`. No production values, runtime code,
chart or operational configuration changed. Azure is the intended cloud direction;
provider-neutral application boundaries remain intact.

## 34. Remaining risks

The intended deployment model and actual PolyMind service ownership are unresolved.
An inaccessible subscription or unlisted external services could contain relevant
resources. Discovery does not certify least privilege, data-plane connectivity,
monitoring completeness or failure domains. Phase 15 establishes interoperability,
not a production scale target or safe dependency ceiling. All Phase 16 success
questions about throughput, scale trigger, replica ceiling and scaling timing
remain unanswered.

## 35. Deferred work

Target baseline, workload execution, inference/Redis/Chroma/network profiling,
per-replica capacity, HPA policy/window calibration, rollback thresholds and safe
failure/recovery validation are deferred until readiness passes. No additional
infrastructure, scaler or cloud SDK was introduced. Infrastructure provisioning
and any Container Apps architecture adaptation require separate authorization
and scope; they were not performed to make this phase pass.

## 36. Next-step readiness and smallest prerequisites

Phase 16 must resume before claiming calibrated autoscaling; Phase 17 was not
started. The smallest concrete prerequisites are:

1. Identify the actual existing Azure PolyMind target and its owner. If it is in
   the unreadable subscription, restore the required read-only access or supply
   access to the correct scope. Confirm whether Kubernetes HPA is still the
   deployment objective. If Container Apps is the sole choice, explicitly resolve
   that architecture/scope mismatch before HPA calibration.
2. For the current HPA objective, provide access to an already-existing,
   representative, dedicated PolyMind Kubernetes test environment with multiple
   application replicas and verified nodes/failure domains. Record scope and
   permissions; continue to prohibit mutations of remote/shared/production
   environments under the current instructions. Any needed remote test mutation
   requires separate explicit authorization resolving that restriction.
3. Identify already-running representative external inference, shared Redis and
   Chroma, the served-model mapping and published BM25 corpus, and verify their
   health, connectivity and capacity telemetry without exposing secrets. Provide
   the per-pod scrape/rule/custom-metrics path and platform resource telemetry.
4. Agree a finite request/time/token/cost envelope, representative workloads,
   observation windows, stop criteria and a reviewed rollback configuration.
   Rerun the readiness gate before executing any load or tuning.

These are access, identification and evidence prerequisites, not instructions to
provision paid services. If the required infrastructure does not already exist,
the blocker remains until a separately authorized infrastructure decision is made.

## 37. Final Git state

`git status` reports branch `master`, locally up to date with `origin/master`, and
two untracked files:

```text
docs/codex/prompts/phase_16.md
docs/codex/reports/phase_16_report.md
```

`git diff --stat` has no output because both additions are untracked. They were
reviewed directly and with no-index diff checks; no staging was used to make them
appear in the tracked diff. `git diff --check` exits 0. HEAD remains the starting
SHA. No other tracked changes are present.

## 38. Completion confirmation

```text
Commit created: NO
Push performed: NO
Branch created: NO
```

Overall status: **BLOCKED**.

---

# Phase 16 AKS Continuation

Continuation assessment date: 2026-10-03. This is the same Phase 16, not Phase 16B.

## C1. Initial blocked result

The initial **BLOCKED — TARGET ENVIRONMENT NOT REPRESENTATIVE** result and its
measurements remain above. It correctly described visibility at the first attempt.
No earlier evidence has been replaced with a claim that AKS was visible then.

## C2. Reason for resumption

The user explicitly selected AKS as the intended PolyMind target and authorized
scoped operations once a dedicated non-production PolyMind AKS environment is
positively verified. The prior deployment-choice uncertainty is resolved. The
application/Helm/HPA architecture remains unchanged; Container Apps is not a
candidate replacement for this calibration.

## C3. AKS identification evidence

Resumed discovery refreshed the Azure account inventory rather than selecting a
subscription by guess. Resource names and scope IDs were used only in process
memory; output was restricted to sanitized properties. No credentials were fetched.

| Inspection | Current outcome |
| --- | --- |
| `az account list --refresh` | Exit 0; one accessible subscription entry, Enabled and default |
| `az aks list --subscription <discovered-scope>` | Exit 0; empty list, zero AKS clusters |
| `az account list --all` with state/default projection | Exit 0; one Enabled default entry |
| `az resource list` with type/location projection | Exit 0; 12 visible resources, no `Microsoft.ContainerService/managedClusters` |
| `kubectl config current-context` | `kind-polymind-phase10`; no AKS context selected |

The refreshed account list no longer contains the second cached subscription
seen in the initial attempt. That earlier entry had returned SubscriptionNotFound.
Refresh is a local authentication-cache discovery operation, not a cloud resource
mutation. No subscription was selected with `az account set`, and no login or
credential import was attempted.

The resource-type inventory still contains the previously observed Cognitive
Services account/project, registry, two managed identities, Container Apps
environment/app, Log Analytics workspace, Key Vault, static site, PostgreSQL server
and CIAM directory. None identifies the requested AKS cluster.

The intended cluster name, resource group and owning subscription remain unknown
to this assessment. There are zero visible candidates, not multiple ambiguous
candidates. This does not prove AKS does not exist in another scope or tenant.
The user was asked for the cluster name, resource group and subscription alias;
no identifying answer was available when this report was finalized.

## C4. Resumed AKS readiness result

**BLOCKED — AKS ACCESS INCOMPLETE**.

The blocker is inability to identify/access the intended cluster from the current
Azure account visibility, not an observed stopped cluster or failed dependency.
Read-only listing succeeded for the visible scope; access to the intended scope
and Kubernetes RBAC are not established.

```text
AKS target deployment decision: YES
Actual AKS target identified: NO
AKS state: UNKNOWN
Cluster activation performed: NO
```

Do not report STOPPED or RUNNING without evidence. If later discovery identifies
a stopped cluster, the continuation's power-state rule requires separate user
authorization before `az aks start`. No such call was made here.

## C5. Cluster topology

Cluster name, resource group, region, provisioning state, power state, Kubernetes
version and node resource group: **unknown**. No dedicated/test ownership or
production/shared classification can be made without identifying the cluster.
The conditional mutation authorization therefore never became applicable.

## C6. Node topology

Node pools, VM sizes, counts, availability zones, autoscaler settings, available
CPU/memory, pressure and schedulability: **unknown**. There was no candidate on
which to call nodepool inspection. No node or pool creation, resize or activation
was performed.

## C7. PolyMind deployment topology

Live replicas, image, Helm release/revision, placement, security settings,
requests/limits, grace and health/readiness/authentication: **unknown**. The source
chart still describes the defaults in historical section 6. Source configuration
is not a deployed AKS baseline. No Helm installation or application deployment
was attempted.

## C8. Inference topology

Provider, endpoint reachability, served-model mapping, readiness, generation and
streaming capability for AKS: **unknown**. Visible Cognitive Services resources
were not assumed to be the AKS inference backend. No generation requests were sent.

## C9. Redis topology

Shared target, connectivity, readiness, latency and replica-A-to-replica-B history
semantics: **unknown**. No Secret values were read or file-memory fallback introduced.

## C10. Chroma topology

Target collection, query capability, publication version, BM25 snapshot and
multi-replica access: **unknown**. No corpus ingestion, rebuild or reset occurred.

## C11. Prometheus/custom-metrics topology

Per-pod metrics, scrape targets, recording rule, adapter, APIService and
`pods/polymind_active_query_requests`: **unverified on AKS**. Existing source
contracts remain intact. No monitoring infrastructure was provisioned.

## C12. Fixed-replica baseline

Not established. The proposed two-replica starting point was not deployed because
no dedicated target or dependencies were verified. There is no known-safe deployed
configuration or Helm revision available for rollback.

## C13. Workload methodology

The gate stopped execution before fixture implementation or load generation.
Direct, RAG and streaming stages at concurrency 1/2/4/8 are all **not run**.
No prompt, route, role, token or timeout fixture was presented as validated.
A future run must observe actual routes and fix finite request, time, concurrency,
token and abort budgets before generating load. It must review each stage before
progressing, rather than assuming the full suggested sequence is safe.

## C14. Direct-query measurements

Not measured. Throughput, p50/p95/p99, active queries, errors and timeout rate are
unknown; no per-replica synchronous traffic claim is supported.

## C15. RAG-query measurements

Not measured. Route correctness, vector contribution, corpus consistency and RAG
latency/error distributions remain unknown on AKS.

## C16. Streaming measurements

Not measured on AKS. Completion, truncation, duplicate responses, success-only
memory persistence, cancellation cleanup and stream behavior during HPA activity
remain unverified on target. The source's separate stream signal and 135-second
grace were not changed.

## C17. Per-replica capacity

**PolyMind API headroom: unknown.** No running AKS replica, resource telemetry or
saturation knee was observed. Local test runtime is not capacity evidence.

## C18. Inference headroom

**Unknown.** No target TTFT, generation latency, token throughput, queueing,
concurrency, provider errors, overload or existing GPU telemetry was observed.
Safe request pressure and supported replica count remain unknown.

## C19. Redis headroom

**Unknown.** No target connection, command latency, timeout, memory or readiness
telemetry, and no cross-replica conversation validation.

## C20. Chroma headroom

**Unknown.** No target query latency, concurrency, errors, timeouts or BM25/corpus
consistency observations.

## C21. Metric propagation delay

Not measured. **Monitoring/custom-metrics headroom: unknown.** No timing from
application gauge through scrape/rule/adapter/custom API to HPA was observed.
No Kind timing was substituted.

## C22. HPA scale-up results

Not run. Metric reaction, scheduling, image pull, startup, readiness and effective
latency improvement are unknown. HPA was not enabled.

## C23. HPA scale-down results

Not run. Recovery/stabilization timing, terminating overlap, stream completion
and memory behavior are unknown. Grace was not shortened.

## C24. Recommended targetAverageActiveQueries

**Unknown; no numeric recommendation.** The chart's null value is unchanged.
There is no measured saturation region, headroom margin or latency/dependency
basis for selecting a target. Production enablement remains deferred.

## C25. Recommended maxReplicas

**Unknown; no numeric recommendation.** The chart's null value is unchanged.
Neither AKS schedulable capacity nor downstream safe capacity has been measured.

## C26. Recommended policies/windows

No calibrated policy/window is justified. The existing disabled-chart scale-up
and scale-down defaults remain unchanged and unvalidated for AKS. The 135-second
termination grace remains part of the preserved contract.

## C27. Dependency capacity ceiling

**Unknown.** API, inference, Redis, Chroma and monitoring headroom are all unknown.
No weakest dependency, safe ceiling or operational reserve can be identified.

## C28. Multi-node observations

None. No live node placement, multi-node readiness, cross-replica service routing
or pod replacement was observed. No topology policy or PDB was introduced.

## C29. Failure/recovery results

Not run. No deletion, rollout, dependency interruption or failure simulation was
performed on AKS or shared infrastructure. Local mocked regression tests do not
validate target failure recovery or HPA behavior under dependency failure.

## C30. Rollback criteria

Observed thresholds: none. Numeric p95, error/timeout, pressure, restart and
stabilization limits: unknown. Historical section 27 remains a provisional future
test safety proposal, not measured AKS rollback policy. Readiness loss, missing
metrics, test-induced overload/restarts or exhausted test budget should stop a
future bounded test, with numeric thresholds and windows agreed before execution.
No rollback was performed and no deployed baseline was invented.

## C31. Candidate operational SLOs

No numerical SLO was established. Availability, direct/RAG latency, TTFT, stream
completion, errors and readiness remain candidate dimensions requiring target
measurements and owner agreement, not business commitments.

## C32. Cost/runtime observations

Calibration duration and generated inference requests: **0**. This continuation
used read-only Azure control-plane discovery and local validation. No cluster or
GPU was started/stopped, no infrastructure was provisioned/resized, and no load
was sent. Existing AKS node runtime/billing is unknown. No euro estimate or claim
of zero pre-existing cloud cost is made.

## C33. Automated tests

Fresh continuation validation:

- `python -m pytest -q`: **179 passed, 2 skipped in 19.10 seconds**, exit 0.
- External-cache `python -m compileall -q .`: exit 0.
- `docker compose config --quiet`: exit 0.
- Final `git diff --check`: exit 0; documentation additions also checked directly.

The two skips remain Helm-dependent tests. No application changes or new tests
were needed for this discovery/report update. No Docker image rebuild was needed.

## C34. Helm validation

Helm remains absent from PATH. An existing-binary search under temporary tooling,
`/usr/local/bin`, `/opt` and the user-local binary directory found no Helm binary.
Lint/render could not run; the initial command-not-found evidence is retained
above. No permanent project dependency was added. Deployment was not required or
safe with the discovery gate blocked. Before actual AKS deployment, Helm tooling
must be available and lint/render must pass; skipped tests are not substitutes.

## C35. Implementation self-review

Reviewed the continuation additions against the unchanged chart and prior report.
The key correction is that AKS is now the explicit intended model, while actual
AKS discovery remains incomplete. Earlier evidence is preserved and clearly
marked historical. Successful empty inventory is not interpreted as proof of
nonexistence. No target state, dependency ceiling or benchmark was fabricated.
Provider boundaries, APIs, security, HPA signal and streaming behavior are unchanged.

## C36. Pre-commit review

Reviewed the two documentation artifacts and the continuation-only diffs against
saved initial copies. No subscription/tenant identifiers, resource IDs, endpoints,
kubeconfig, tokens, connection strings, secrets, raw cloud inventory or benchmark
logs were added. Temporary discovery tooling remains outside the repository.
No tracked code/configuration/dependency change is present. No Git staging,
commit or remote operation occurred.

## C37. Documentation changes

Added this continuation and current-status/historical markers to the existing
Phase 16 report. Appended an explicitly labeled summary of the continuation
instructions to the existing prompt. The original clean prompt and initial report
body are retained. No separate Phase 16B artifact was created.

## C38. Remaining risks

The authenticated Azure scope may differ from the intended AKS scope; current
inventory cannot resolve ownership, power state, nodes, RBAC or dependencies.
An inaccessible target may already exist elsewhere. Read permissions in the
visible subscription prove nothing about mutation permissions on that target.
AKS existence alone will not establish representativeness or capacity.

## C39. Deferred work

Target identification, running-state verification, Kubernetes access, full
readiness, baseline, fixtures, dependency profiling, metric-delay measurement,
HPA tuning, streaming/multi-node/failure tests and calibrated rollback criteria
remain deferred. No paid replacement infrastructure or Kind workaround was used.

## C40. Smallest prerequisite and next-step readiness

Provide the intended cluster name, resource group and subscription name/alias,
and make that scope visible to the existing Azure authentication workflow with
the required read access. Do not send credentials or tokens. This is the immediate
prerequisite; starting or provisioning a cluster is not yet justified.

Then repeat read-only AKS discovery. If stopped, obtain separate start authorization;
if running, positively verify dedicated PolyMind test ownership and context before
any scoped mutation. The continuation's conditional authorization covers those
verified test operations; it does not permit ambiguous/shared/production changes.
Verify real dependencies, multiple nodes/replicas and custom metrics before load.
Phase 17 has not started; Phase 16 remains incomplete.

## C41. Final Git state

Branch remains `master`, HEAD `036b847ae3a722d3aa261d332ccd99928360d672`. The existing
Phase 16 prompt and report remain the only two untracked files. No tracked files
changed. `git diff --stat` is empty because untracked artifacts are excluded;
continuation additions were separately reviewed against their initial copies.
`git diff --check` passes. Local upstream tracking metadata was not refreshed by
any Git remote operation.

## C42. Final confirmation

```text
Branch created: NO
Commit created: NO
Push performed: NO
```

Final overall Phase 16 status: **BLOCKED**.

---

# 2026-10-04 — Operator-created AKS readiness assessment

Date uses Europe/Lisbon. The local clock check during assessment read
2026-10-03 23:38:58 UTC (2026-10-04 in Lisbon). This continues Phase 16.

## D1. Executive result

Gate: **PARTIALLY READY — INFRASTRUCTURE READY, DEPENDENCIES INCOMPLETE**.

The dedicated AKS target is reachable and has spare resources at the observed
system-only baseline. That does not establish application or dependency capacity.
No representative external inference, Redis or Chroma configuration, approved
pullable image, or live application/custom-metrics chain was identified. The
readiness gate therefore stopped deployment and calibration.

## D2. Previous blockers and repository state

The initial no-representative-target result and the subsequent AKS-access blocker
remain above as history. Both infrastructure identification/access issues are
resolved by this operator-created cluster and the successful reads below.

Branch remains `master`, HEAD `036b847ae3a722d3aa261d332ccd99928360d672`.
At resumption, the existing Phase 16 prompt and report were the only untracked
files; tracked files were clean. Reviewed the full existing report, AGENTS,
Phase 15 report, chart/templates, monitoring/Kind assets, inference/memory/vector
settings, Docker packaging, CI image assumptions and relevant existing tests.

## D3. Operator-created environment and discovery scope

Azure account inspection confirmed the named Enabled default subscription
`ECI-Development`. All resource inspection for this attempt was explicitly
limited to the supplied PolyMind cluster/resource group; unrelated ECI services
were not inspected or used.

`az aks show`, nodepool listing and resource-type listing succeeded. Read-only
Kubernetes queries used the operator-installed kubectl and kubelogin through the
existing Azure CLI authentication. No kubeconfig conversion, credential import,
Azure role assignment or subscription change was performed.

| Inspection | Result |
| --- | --- |
| Current context | `epolymind-aks-dev` |
| Nodes wide / node JSON / node descriptions | Successful; two Ready nodes |
| All-namespace pods | 22 system pods, all Running; all listed containers Ready, zero restarts |
| Namespaces | default, kube-node-lease, kube-public, kube-system |
| Services | Four ClusterIP services: Kubernetes API, workload-identity webhook, DNS, Metrics Server |
| Deployments | Six system Deployments, all desired replicas Ready |
| StatefulSets / HPAs | None / none |
| StorageClasses | Ten built-in Azure disk/file CSI classes |
| API discovery / APIServices | Resource metrics present; custom metrics absent |
| Node and pod resource metrics | `kubectl top nodes` and `top pods -A` succeeded |

No PolyMind namespace, application, Redis, Chroma, Prometheus or adapter workload
was found. StorageClasses do not demonstrate already-provisioned application
storage. No PVC, LoadBalancer Service or other resource was created.

## D4. Exact AKS topology

| Property | Observed value |
| --- | --- |
| Resource group | `rg-epolymind` |
| Cluster | `epolymind-aks-dev` |
| Region | Spain Central (`spaincentral`) |
| Provisioning / power | Succeeded / Running |
| Configured/current Kubernetes | 1.35.7 / 1.35.7 |
| Node resource group | `MC_rg-epolymind_epolymind-aks-dev_spaincentral` |
| Tier | Free |
| API exposure | Public; private-cluster flag false |
| Pool | `agentpool`, System, two `Standard_D4s_v4` nodes |
| Pool provisioning / power | Succeeded / Running |
| Pool autoscaler | Disabled; min/max not configured |
| Pool configured zones | 1, 2, 3 |
| Observed node zones | Spain Central 1 and 2, one node each |
| OS / runtime | Ubuntu 24.04.5 LTS / containerd 2.3.3-2 |
| Network | Azure CNI Overlay; Azure dataplane; `networkPolicy: none` |

Configured zones 1/2/3 do not imply three populated failure domains: only two
nodes were observed, in zones 1 and 2. No cross-zone application behavior was tested.
Dedicated development ownership is established by the operator's explicit scope,
matching resource identity, and the system-only observed inventory.

## D5. Authentication configuration

Managed Microsoft Entra integration and Azure RBAC are enabled; local AKS accounts
are disabled. Read-only cluster/node/workload discovery succeeded. This establishes
those read permissions, not unrestricted mutation permission or least-privilege
certification. No admin credentials or broad Azure roles were requested.

## D6. OIDC and Workload Identity

OIDC issuer and Workload Identity are enabled. The workload-identity webhook has
two Ready replicas. The PolyMind resource group contains the AKS resource and one
user-assigned managed identity. Identity identifiers and issuer URLs are omitted.

Federation absence is operator-supplied information, not an independently queried
federation inventory. The existing PolyMind chart uses Secret references and a
ServiceAccount with token automount disabled; the inspected application contracts
do not require Azure SDK authentication or a federated identity. No demonstrable
federation requirement was found, and none was created. Cluster login and
application workload identity are separate concerns.

## D7. Node capacity and pressure

Node suffixes identify the two observed pool members without reproducing IPs.
These are point-in-time observations during read-only discovery.

| Measure | Node 000000, zone 1 | Node 000001, zone 2 |
| --- | --- | --- |
| Capacity CPU | 4 | 4 |
| Capacity memory | 16,372,464 Ki | 16,372,460 Ki |
| Allocatable CPU | 3,860m | 3,860m |
| Allocatable memory | 13,966,064 Ki | 13,966,060 Ki |
| Allocatable pod slots | 110 | 110 |
| Existing CPU requests | 767m (19%) | 695m (18%) |
| Existing memory requests | 892 Mi (6%) | 676 Mi (4%) |
| Existing CPU limits | 5,092m (131%) | 5,540m (143%) |
| Existing memory limits | 9,952 Mi (72%) | 10,981,664 Ki (78%) |
| Observed CPU usage | 120m (3%) | 104m (2%) |
| Observed memory usage | 1,325 Mi (9%) | 1,298 Mi (9%) |
| Ready | True | True |
| Memory/Disk/PID pressure | All False | All False |
| Unschedulable / taints | false / none | false / none |

Arithmetic unrequested CPU is 3,093m and 3,165m, respectively, before any new
workload. At source defaults (250m CPU/512 Mi memory requested per application
pod), two PolyMind replicas fit the observed request budget in principle. This is
not scheduling, startup, security or readiness proof. Existing system CPU limits
are overcommitted; requests, limits and measured usage are different quantities.
No safe application `maxReplicas` is inferred from idle nodes or pod-slot counts.

## D8. Dependency readiness gate

| Dependency | Evidence and readiness |
| --- | --- |
| AKS-pullable image | Not identified. Chart defaults to `polymind:1.0.0`; Kind uses local tags. CI builds but does not publish an image. Public availability/registry authorization is unverified. |
| Helm | Binary absent from PATH and searched existing tooling locations. Lint/render cannot execute locally. |
| External inference | No target endpoint/model configuration supplied or found in deployment assets. Example endpoint and Kind stub are not representative. AKS reachability/generation/streaming untested. |
| Shared Redis | No cluster workload/service or approved external endpoint identified. History sharing/readiness/latency unknown. |
| Chroma | No cluster workload/service or approved external endpoint/corpus identified. Query and BM25 compatibility unknown. |
| Prometheus | Not installed; Azure managed monitoring not enabled. Repository self-hosted test assets exist. |
| Adapter/custom metrics | Not installed; no custom-metrics APIService or Pods custom metric available. |

A sanitized configuration check found no explicit inference/memory/vector provider
or endpoint settings in either the local `.env` or process environment. Their
contents were not printed or copied. Runtime defaults are local Ollama/file/local
vectors; chart production settings require external OpenAI-compatible inference,
Redis and Chroma HTTP. No local defaults were adopted as an AKS deployment.

The operator was asked for an approved image reference and configuration/Secret
reference locations for existing dependencies, without requesting secret values.
No such configuration was available at report completion. Absence from this
scope does not prove those services exist nowhere. No unrelated ECI registry or
Foundry resource was selected, attached or tested.

## D9. Deployment evidence and chart compatibility

No application deployment was attempted because required dependencies were not
established. Kubernetes 1.35.7 advertises the chart's core APIs: apps/v1,
networking.k8s.io/v1, rbac.authorization.k8s.io/v1 and autoscaling/v2, along with
core v1. Source inspection found no required Azure-specific application change.
This is API-level compatibility evidence only: Helm rendering, admission and
runtime compatibility remain unvalidated. The optional ServiceMonitor remains
disabled and would require its separately operated CRD if enabled.

The container contract remains non-root, CPU model artifacts baked into the image,
offline runtime, read-only filesystem, bounded temporary storage, Secret-based
authentication and external inference. The 135-second grace remains unchanged.

The cluster reports `networkPolicy: none`. Existing chart policy resources and
placeholder selectors are insufficient evidence of enforced isolation. Before
production-oriented serving, the operator must establish an approved, effective
network boundary for metrics and dependencies. No network plugin, cluster policy
or subscription setting was changed to resolve this issue.

## D10. Monitoring/custom-metric feasibility

Metrics Server currently serves nodes/pods through `metrics.k8s.io/v1beta1`.
It does not satisfy the custom active-query metric. The observed cluster has no
`custom.metrics.k8s.io` APIService, Prometheus or adapter.

Existing Phase 14/15 assets can form the basis of a scoped self-hosted test stack
without Azure Managed Prometheus or a new workspace. Source requests are 50m CPU/
128 Mi for Prometheus and 50m/64 Mi for the adapter; these requests are small
relative to the observed unrequested resources. This is a feasibility assessment,
not evidence that the stack is deployed or has adequate measured headroom.

The fixtures require deliberate adaptation before use: replace the fixed Kind
namespace in discovery/RBAC and the adapter's Prometheus service address, create
the expected rule/config ConfigMaps, and align monitoring ingress selectors with
the actual scraper labels. In particular, the chart example uses a `prometheus`
label while the fixture uses `phase14-prometheus`; copying both unchanged would
not produce matching selectors under enforced policies.

The adapter also needs its existing aggregation RBAC/TLS/APIService integration,
including cluster-scoped objects and access to delegated authentication config.
That scope must be reviewed before installation; no kube-system change or broad
permission grant was made. Verify image pulls, API permissions and real idle/active
pod metrics after the dependency gate passes. Retain the fixture's bounded
retention/emptyDir storage for testing; do not create a PVC that dynamically
provisions paid storage. No public LoadBalancer is needed for this assessment.

## D11. Baseline measurements

The table in D7 is a system-only node baseline. Six Deployments have ready/desired
counts 2/2 (identity webhook), 2/2 (DNS), 1/1 (DNS autoscaler), 2/2 (konnectivity),
1/1 (konnectivity autoscaler) and 2/2 (Metrics Server). All 22 observed pods were
Running with zero container restarts; none were Pending in the snapshot.

There is no application baseline: zero deployed PolyMind replicas, no Helm release,
no live inference/Redis/Chroma/corpus configuration, and no HPA metric. Authentication,
health/readiness and service routing were not tested on a nonexistent application.
No application rollback configuration can be recorded yet.

## D12. Load stages

Direct `/query`, RAG `/query` and `/query/stream`: **not run**, at every proposed
concurrency (1, 2, 4, 8). No request count, throughput, latency percentiles, token
usage, stream result or dependency error rate was fabricated. Application/inference
traffic generated for calibration: **0**. No synthetic service was deployed to
turn an infrastructure baseline into capacity evidence.

## D13. HPA calibration

No HPA was created or enabled. `targetAverageActiveQueries` and `maxReplicas` remain
null, and autoscaling remains disabled in the chart. The existing minimum of two
is unchanged, not newly calibrated. Scale-up/down policies, stabilization windows,
metric propagation, termination overlap and scaling benefit remain unmeasured.
Streams remain excluded from the synchronous-query signal. Kind values were not
transferred to AKS. No numeric HPA recommendation is justified.

## D14. Independent headroom assessment

| Component | Classification | Evidence limit |
| --- | --- | --- |
| AKS CPU at observed system-only baseline | comfortable | 2–3% usage; substantial unrequested CPU; existing limits overcommitted; no load evidence |
| AKS memory at observed system-only baseline | comfortable | 9% usage per node; no memory pressure; no application/model load measured |
| PolyMind application | unknown | Not deployed |
| Inference | unknown | No representative endpoint or telemetry |
| Redis | unknown | No representative endpoint or telemetry |
| Chroma | unknown | No representative endpoint/corpus or telemetry |
| Prometheus/Adapter | unknown | Not deployed; source resource requests are not capacity measurements |

The two comfortable classifications apply only to the observed idle infrastructure,
not production traffic, failover reserve or sustained capacity.

## D15. Bottlenecks and capacity boundaries

The immediate blocker is dependency/image availability and configuration, not
observed AKS CPU or memory saturation. The first runtime bottleneck cannot be
identified without measurements. Application scaling capacity, downstream service
capacity and node scheduling limits remain separate unknown ceilings. Two healthy
nodes alone cannot establish any of them or justify a production maximum.

## D16. Safety limits and cost

No AKS resources were created/modified. No Azure resources were created/modified.
No pool scaling, restart/stop/start, autoscaler, federation, identity permission,
registry operation, GPU or paid monitoring action occurred. Existing cluster
runtime continued under operator control; no cost estimate was invented.

Load remains prohibited until dependencies and fixed replicas are healthy. Before
a future run, set finite stage request/time/token/concurrency budgets and stop
conditions for readiness loss, restarts, node pressure, provider overload and
unstable latency/error rates. Numeric operational thresholds and business SLOs
remain unknown. No failure injection, rollout or rollback was attempted.

## D17. Tests, validation and reviews

- `python -m pytest -q`: **179 passed, 2 skipped in 19.02 seconds**, exit 0.
- External-cache `python -m compileall -q .`: exit 0.
- `docker compose config --quiet`: exit 0.
- Helm lint and template: shell exit 127, command not found. Existing-path search
  found no Helm binary; two corresponding automated tests skipped.
- Kubernetes read-only discovery and node/pod resource metrics: successful.
- `git diff --check` and direct documentation whitespace checks: passed.

No dependencies were installed or images rebuilt for a documentation-only blocked
assessment. Runtime Helm/AKS compatibility is explicitly not claimed. Before
actual deployment, obtain Helm tooling and execute lint/render successfully.

Self-review checked history preservation, exact node measurements, configured
versus populated zones, system-only versus application capacity, API compatibility
limits, monitoring namespace/selector requirements and unsupported dependency
claims. No application/provider/API/configuration changes were needed.

Pre-commit review covered the complete documentation changes, secret patterns,
cloud IDs/URLs, kubeconfig, `.env`, logs, temporary artifacts and unrelated files.
No identity/client/principal/subscription/tenant IDs or endpoints were copied.
Only operator-supplied PolyMind resource names needed to identify scope appear.
Temporary discovery code stays outside the repository; no raw inventory or
benchmark log was added. The original prompt and both prior assessment bodies
remain intact, with their current-status headings clearly historical.

## D18. Git state and documentation

Updated only the existing Phase 16 prompt and report; both remain untracked on
`master`. No tracked file changed. `git diff --stat` is empty because it excludes
untracked additions; continuation changes were reviewed against saved prior copies.
Final `git status`, `git diff --stat` and `git diff --check` were run.

```text
Branch created: NO
Commit created: NO
Push performed: NO
```

## D19. Remaining blockers and next operator action

The smallest next input is an approved immutable AKS-pullable PolyMind image
reference and approved configuration/Secret-reference locations for **existing**
representative inference, Redis and Chroma, including served-model mapping and
published BM25 corpus version. Do not send secrets in chat. If these services do
not exist, their provisioning is a separate operator decision outside this task;
no paid replacements will be created under Phase 16 authorization.

Then establish Helm tooling and an approved network-isolation boundary, verify
dependency connectivity/readiness, and review the existing self-hosted monitoring
adaptation and adapter aggregation permissions. Only after the gate genuinely
passes should scoped deployment establish two fixed Ready replicas and the full
custom-metrics chain, followed by bounded calibration. The absence of managed
Azure monitoring does not require enabling it.

No federation is presently required by the inspected application contract. No
additional nodes, GPUs, ACR or new cloud resources are justified by this assessment.

## D20. Final Phase 16 verdict

**BLOCKED — REPRESENTATIVE DEPENDENCIES NOT AVAILABLE**.

AKS infrastructure discovery/access is complete for this attempt. Capacity
calibration remains incomplete. Phase 17 was not started.

---

# 2026-10-04 — External inference discovery

## E1. Result and inspection boundary

Candidate classification: **C. TECHNICALLY USABLE BUT SHOULD NOT BE REUSED BECAUSE
IT IS ECI-SPECIFIC**. This is a protocol-level candidate assessment, not an
end-to-end compatibility or capacity certification. The only deployed candidate
is ECI-owned by naming/resource-group evidence; no independent PolyMind or generic
shared inference deployment was discovered in the accessible subscription.

Phase 16 remains **BLOCKED**. No inference request, data-plane readiness call,
credential retrieval, resource mutation or Kubernetes operation occurred in this
inspection. Earlier infrastructure and dependency assessments remain historical
records. A real model deployment is now identified, but it is not an approved
PolyMind dependency.

## E2. Commands and categories inspected

All Azure calls were read-only and explicitly scoped to the named accessible
subscription where applicable:

- `az account show`, with only account name/state/user-type retained: confirmed
  Enabled `ECI-Development` and user authentication.
- `az resource list`: identified Cognitive Services accounts/projects, possible
  Machine Learning workspaces and user-assigned identities. No
  `Microsoft.MachineLearningServices/workspaces` appeared in this inventory.
- `az cognitiveservices account show` and `account deployment list`: inspected
  provisioning, network/authentication flags, endpoint categories and deployment
  model/SKU/rate-limit metadata. Actual endpoint addresses were not retained.
- `az resource show` for the AI project: inspected provisioning and identity type.
- `az identity show` for the PolyMind identity; its principal identifier was used
  only in memory to filter role assignments and was not printed or retained.
- `az role assignment list` for that principal across the subscription and at the
  AI account with inherited scope included: both returned empty lists.
- `az identity federated-credential list`: zero federated credentials.
- `az role definition list` for Cognitive Services OpenAI User: inspected existing
  read and inference data actions; no assignment or role definition was changed.
- `az cognitiveservices account list-models`: confirmed the matching model/version
  and advertised chat-completion/Responses capabilities in control-plane metadata.

An initial scoped role-list command combined incompatible CLI options and failed.
The corrected scoped query without `--all` succeeded; permission conclusions use
that successful query, not the failed attempt. Model-catalog parsing was adjusted
for its top-level model fields before recording its result.

No list-keys, connection-string, Key Vault, token-printing or generation command
was used. Discovery used temporary local scripts that captured only safe summaries.
Microsoft documentation was consulted for API/authentication semantics; it does
not substitute for testing this deployment.

## E3. Discovered resources and ownership assessment

| Resource | Resource group | Region | Type/kind | State | Assessment |
| --- | --- | --- | --- | --- | --- |
| `eci-foundry-dev-susanta` | `rg-eci-dev` | Spain Central | Microsoft.CognitiveServices/accounts, AIServices, S0 | Succeeded | ECI-specific by account and group names |
| `eci-foundry-dev-susanta/eci-project-dev` | `rg-eci-dev` | Spain Central | Microsoft.CognitiveServices/accounts/projects, AIServices | Succeeded | ECI-specific child project; not a separate inference deployment |

Account and project both report SystemAssigned identities. Their identifiers are
omitted. User-assigned identities visible in the inventory were
`eci-ca-identity-dev` and `eci-github-deploy-dev` in `rg-eci-deploy-dev`,
`epolymind-identity-dev` in `rg-epolymind`, and the AKS-generated
`epolymind-aks-dev-agentpool` identity in its node resource group, all Spain Central.
Identity existence does not confer inference rights. ECI identities were neither
adopted nor modified; their application permissions were not borrowed.

No PolyMind-specific AI account/model deployment or generic shared AI workspace
was found in visible inventory. This statement is limited to accessible resources,
not other subscriptions, tenants or external services. Naming is ownership
assessment evidence, not proof of current ECI traffic volume or an owner approval.

## E4. Deployment metadata

Exactly one deployment was returned for the discovered account:

| Field | Observed value |
| --- | --- |
| Deployment | `eci-gpt-54-mini` |
| Model / format | `gpt-5.4-mini` / OpenAI |
| Model version | `2026-03-17` |
| Provisioning | Succeeded |
| Deployment SKU | DataZoneStandard |
| SKU capacity field | 10 |
| Advertised request rate | 10 per 60 seconds |
| Advertised token rate | 10,000 per 60 seconds |
| Advertised capabilities | chatCompletion=true, responses=true, assistants=true, agentsV2=true |
| Advertised area | EUR |
| Version upgrade policy | OnceNewDefaultVersionAvailable |

Capacity 10 is a deployment metadata unit, not ten GPUs or ten concurrent requests.
Rate limits are advertised allocations, not observed throughput, remaining quota
or headroom. Existing ECI consumption is unknown. The upgrade policy can change
the served version over time; a later calibration must record the actual version
again rather than assuming this snapshot is immutable.

The project is not an additional candidate endpoint to use in place of the
account's OpenAI v1 API. Neither the additional advertised endpoint categories
nor the model catalog imply additional deployed models.

## E5. PolyMind provider contract

Inspected `llm/inference.py`, `llm/provider_factory.py`,
`llm/openai_compatible.py`, settings and chart wiring. Application/graph/RAG depend
on `InferenceProvider`; Azure-specific behavior need not leak into those layers.

The current `openai_compatible` adapter:

- strips a trailing slash from its base URL and appends `/chat/completions` and
  `/models`; it does not construct legacy Azure deployment/API-version routes;
- sends a user `messages` array, the mapped served-model identifier and `stream`;
- requires a mapping for general, coding, summarization and fast; roles may share
  one deployment, though equal mapping does not prove task quality;
- sends `Authorization: Bearer <configured-value>` when
  `OPENAI_COMPATIBLE_API_KEY` is set; it has no credential acquisition/refresh
  callback, Azure Identity SDK integration or per-request token renewal;
- performs readiness using GET `/models`, requires `data` containing valid string
  IDs, and requires every distinct configured model ID to be present;
- parses ordinary chat text and SSE `data:` JSON chunks with text deltas, permits
  usage-only empty-choice chunks, and requires explicit `[DONE]` termination;
- preserves provider-neutral streaming for PolyMind's downstream NDJSON API.

Default inference connect/read limits are 5/120 seconds; readiness defaults are
3 seconds, one retry and 0.1-second backoff. Generation parameters are configurable
but cannot override model/messages/stream. No code, configuration or timeouts were
changed during discovery.

## E6. Azure compatibility and limitations

Azure OpenAI v1 uses an account base URL ending `/openai/v1`, accepts deployment
names in `model`, and does not require the legacy mandatory `api-version` query.
Both documented OpenAI and services.ai account host forms are supported. This
aligns with PolyMind's appended chat route; a project endpoint or legacy
`/openai/deployments/...` base is not interchangeable.
[Microsoft v1 API documentation](https://learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle).

The REST chat API documents API-key authorization and OAuth, and `stream=true`
uses SSE. Deployment and catalog metadata both advertise chat completions. Thus
non-streaming and streaming are theoretically usable, but no runtime streaming
capability was tested here; metadata exposed no explicit stream flag. Azure
stream variants, including filtering/annotation chunks, must still satisfy the
adapter's strict parser and `[DONE]` requirement.
[Microsoft chat API reference](https://learn.microsoft.com/en-us/rest/api/microsoft-foundry/azureopenai/chat).

**Readiness is unresolved.** The control-plane deployment name is
`eci-gpt-54-mini`, distinct from model family `gpt-5.4-mini`. No authorized
resource `/openai/v1/models` request was made. Documentation/control-plane lists
alone do not prove that its returned `data[].id` contains the deployment alias
required by PolyMind. If it exposes catalog model IDs instead, or that route is
unavailable, generation could be valid while PolyMind remains unready. Do not
substitute the model family merely to satisfy readiness or bypass readiness.
A future authorized contract check must establish this behavior first. This
uncertainty prevents classification A or a claim that B is fully demonstrated.

Managed identity is not configuration-only for the current adapter. Azure supports
Entra tokens, but production use needs acquisition and renewal. Passing a copied
short-lived token through the static API-key setting is not a durable solution.
Any future adaptation must stay within the provider/auth infrastructure boundary
and requires separate scope; none was implemented.

## E7. Illustrative configuration, not an applied override

If reuse were separately approved and the full contract verified, the existing
configuration names would be:

```text
INFERENCE_PROVIDER=openai_compatible
OPENAI_COMPATIBLE_BASE_URL=https://<approved-account-host>/openai/v1
OPENAI_COMPATIBLE_MODEL_MAP={"general":"eci-gpt-54-mini","coding":"eci-gpt-54-mini","summarization":"eci-gpt-54-mini","fast":"eci-gpt-54-mini"}
```

Use the actual approved account endpoint from operator configuration, not the
placeholder above. Chart counterparts are `application.inferenceProvider`,
`application.openaiCompatibleBaseUrl` and `application.openaiCompatibleModelMap`.
An owner-provided existing API key would use the existing Secret reference and
`OPENAI_COMPATIBLE_API_KEY`; no value was requested or retrieved here. The v1
key path is theoretically compatible with the Bearer-header convention, unlike
assuming legacy Azure `api-key` behavior works with every base route.

A later workload must set a supported finite generation budget, such as
`max_completion_tokens`, through the existing generation-parameter configuration
and choose timeout/budget values from actual testing. No numerical token budget
or HPA values are calibrated by this metadata inspection.

## E8. Authentication and identity/RBAC status

Account metadata: publicNetworkAccess=Enabled; disableLocalAuth was null/not
explicitly reported, rather than a verified false flag. Key authentication is
supported by the documented API, but successful key authentication and effective
account policy were not tested. No key was read. Network ACL default action was
also not reported; public-network enablement does not prove AKS reachability.

The dedicated PolyMind identity exists. Direct assignment listing across the
subscription and direct/inherited listing at the AI account both returned **zero**
assignments for that principal. Its federation list returned **zero** credentials.
Therefore no current assigned inference access for that identity was established.
This is not an exhaustive audit of group-derived/PIM/effective access or a live
authentication test. Operator CLI visibility is not the application's permission.

For a future Entra-based call to this OpenAI deployment, the appropriate minimal
standard built-in inference role is **Cognitive Services OpenAI User**, scoped to
the selected AI account rather than the subscription. The inspected role includes
OpenAI read and chat-completion inference data actions. It is narrower than
Contributor/Owner but still broader than a custom chat-only role; no broad role
is needed merely to infer. Account-scoped permissions would span other OpenAI
capabilities/deployments there, another isolation consideration.
[Microsoft Azure OpenAI RBAC documentation](https://learn.microsoft.com/en-us/azure/foundry-classic/openai/how-to/role-based-access-control).

RBAC would not be sufficient by itself: AKS workload federation and supported
token acquisition/renewal would also need an approved design. Neither was created.
For owner-provisioned API-key access, the caller's managed-identity inference role
is not how each request is authorized; key custody and rotation become the boundary.
This is not a recommendation to retrieve or share ECI's account key.

## E9. Region, isolation and cost implications

The account/project are in Spain Central, matching the AKS resource region.
However, DataZoneStandard area EUR is data-zone processing, not proof that requests
execute in Spain Central or share a low-latency network path. No AKS-to-inference
latency or connectivity was measured.

DataZoneStandard is pay-per-token, not a reserved GPU capacity guarantee. Future
traffic would incur usage charges and share this deployment's rate allocation
with ECI. No monetary price, remaining capacity or idle-cost estimate was observed
or invented. The advertised 10 requests/minute is a material constraint for any
future concurrency experiment; it does not justify a PolyMind replica ceiling.
[Microsoft deployment types](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types).

Reuse would couple PolyMind to ECI's deployment lifetime/version upgrades, quota,
model settings, content-filter policy, billing and operational incidents. It could
confound capacity results with unrelated ECI load and widen credential/access
scope. This is operational coupling even if the application interface stays
provider-neutral. No ECI traffic level, safety-policy configuration or shared-use
approval was inferred from its name.

## E10. Candidate decisions

| Candidate | Classification | Decision |
| --- | --- | --- |
| `eci-foundry-dev-susanta` / `eci-gpt-54-mini` | C — technically usable but ECI-specific | Best technical candidate found; do not reuse automatically. Full readiness/auth/stream contract remains unverified. |
| `eci-project-dev` child project | C — ECI-specific access context, not an independent deployment | Not an isolation alternative; project API is not PolyMind's base URL contract. |

No A/B-ready independent candidate was discovered. This is not E (no deployment
exists), because one real deployment does exist; nor is D asserted, because the
v1 chat protocol appears viable and unresolved readiness is not proof of failure.

A dedicated PolyMind inference deployment/resource boundary is preferable for
independent credentials, workload budgets and calibration. A second deployment
inside the same ECI account alone would not eliminate account-level coupling.
No deployment, account, quota change or RBAC assignment is authorized by this
inspection and none was performed.

## E11. New paid infrastructure and next operator decision

New infrastructure is **not technically proven necessary**: an existing service
could potentially generate PolyMind-compatible responses. But no isolated,
approved existing dependency was found, and reuse of this ECI-specific resource
is not recommended. For the recommended isolated path, the operator must identify
another existing dedicated service or separately approve dedicated inference
provisioning and its cost. This task neither provisions it nor requests quota.

Next operator decision: choose isolation versus explicitly approved shared use.
If shared use is selected despite the coupling, approve the precise account,
authentication method and finite traffic budget, then separately authorize contract
validation for model discovery, generation and streaming. Those data-plane checks
were prohibited in this task. Resolve token renewal/federation for Entra use or
approved Secret custody for key use before claiming deployability.

Other Phase 16 blockers (image, shared Redis, Chroma/corpus, Helm and custom metrics)
remain as documented in D19. This discovery does not calibrate inference headroom,
HPA target/maximum, rollback thresholds or SLOs.

## E12. Tests, review and final state

Targeted offline contract validation:

```text
python -m pytest -q tests/unit/test_openai_compatible_provider.py
  tests/unit/test_provider_contract.py tests/unit/test_provider_readiness.py
  tests/unit/test_streaming_orchestration.py
65 passed in 0.31 seconds
```

These tests use mocks and do not authenticate to Azure or generate model traffic.
No application code changed, so prior full-suite/compile/Compose/Helm results
remain historical and are not claimed as rerun here. Final diff/whitespace review
covered this addition and checked for cloud identifiers, credentials, real endpoint
addresses, raw inventory and unrelated changes. Only this report changed in this
inspection; the previously untracked prompt remains unchanged.

`git status`, `git diff --stat` and `git diff --check` were run. Branch remains
`master`; the existing two Phase 16 documentation artifacts remain untracked and
tracked diff-stat remains empty. No files were staged.

```text
Azure resources modified: NONE
AKS resources modified: NONE
Inference/data-plane calls: NONE
Commit created: NO
Push performed: NO
Branch created: NO
```

Phase 16 remains **BLOCKED**; inference candidate classification is **C**.

## F. 2026-10-05 — Foundry/OpenAI v1 compatibility update

Operator-provided live endpoint evidence identified two compatibility gaps after
successful non-streaming and streaming inference: Azure emits an initial empty
`choices` event containing prompt-filter metadata, and its `/models` catalog may
advertise underlying model IDs rather than the configured deployment aliases.
The previous parser rejected that metadata event, and strict catalog membership
could incorrectly report an otherwise usable deployment as unavailable. This
update uses the supplied observations; Codex did not independently validate the
live Foundry endpoint.

The existing `openai_compatible` provider now accepts empty `choices` only when
`usage` is a dictionary or `prompt_filter_results` is a list of dictionaries.
Subsequent text deltas are yielded normally. Plain empty choices, malformed JSON,
unknown non-SSE lines and malformed metadata remain errors; `[DONE]` remains
mandatory. No provider type, hostname detection or application-layer branching
was added, and the provider-neutral token stream and API contracts are unchanged.

`OPENAI_COMPATIBLE_READINESS_MODEL_CHECK` defaults to `true` in Settings and is
passed through the factory to `readiness_model_check=True`. The Helm setting
`application.openaiCompatibleReadinessModelCheck` also defaults to `true`. Setting
it to `false` skips only configured-model membership enforcement after the
existing `/models` HTTP, JSON and structural validation. It neither bypasses
discovery nor generates tokens. Strict vLLM readiness behavior is preserved.
Relaxed readiness does not establish that a configured alias supports inference;
that remains a separate operator validation responsibility. No Foundry deployment
override was created.

Regression coverage includes the observed metadata/text stream, completion-marker
requirement, invalid metadata types, strict versus relaxed catalog membership,
malformed discovery and invalid JSON in relaxed mode, operational failures in
both modes, constructor defaults, and environment-to-factory boolean propagation.
Existing plain-empty-choices and usage-only stream tests remain intact. README
and `.env.example` document the new option and its limits.

Validation for this update:

| Check | Result |
| --- | --- |
| Requested four targeted test files | **89 passed in 0.37s**, exit 0 |
| `python -m pytest -q` | **207 passed in 18.35s**, exit 0 |
| `PYTHONPYCACHEPREFIX=/tmp/polymind-phase16-pycache python -m compileall -q .` | Exit 0 |
| `docker compose config --quiet` | Exit 0 |
| `helm lint deployment/helm/polymind` | 1 chart linted, 0 failed; informational icon recommendation only |
| Default `helm template` | Exit 0; parsed ConfigMap value verified as string `"true"` |
| Template with `--set application.openaiCompatibleReadinessModelCheck=false` | Exit 0; parsed ConfigMap value verified as string `"false"` |
| `git diff --check` | Exit 0 |

Implementation self-review and a separate pre-commit review checked protocol
validation, default compatibility, resource cleanup, complete tracked diff and
this report addition. No secrets, real endpoint/resource names, dependencies,
generated repository artifacts, unrelated formatting changes or unintended API
changes were introduced. Rendered manifests and compilation cache stayed under
`/tmp`. No additional lint/format configuration was found. Historical report
sections and the existing untracked Phase 16 prompt were preserved.

Final working state remains `master`, with 10 tracked files modified (107
insertions, 8 deletions) plus this appended, previously untracked report. The
previously untracked prompt is unchanged. `git status` and `git diff --stat` were
inspected; nothing was staged. This compatibility update passes its offline
checks, but **Phase 16 is not complete** and the earlier deployment/calibration
blockers are not resolved by this patch. Foundry live endpoint validation remains
operator-provided evidence.

```text
Azure/cloud resources modified: NONE
Kubernetes resources modified: NONE
Live inference requests performed by Codex: NONE
Chart deployed: NO
Branch created: NO
Commit created: NO
Push performed: NO
```


## G. 2026-10-05 — Duplicate model IDs in readiness discovery

Operator-provided live Azure Foundry `/models` diagnostics reported **443 total
entries, 430 unique IDs, 13 duplicates and 0 malformed entries**. The response was
an object with `data` and `object` keys, and `data` was an array. Operator tests
reported readiness `protocol_failure` while generation and streaming succeeded;
Codex did not independently issue live requests.

The root cause was a set-cardinality check that incorrectly treated valid duplicate
IDs as malformed entries. Readiness now validates every entry as an object with a
string `id` before building the unique-ID set for membership lookup. Strict vLLM
membership checking and relaxed Foundry membership semantics remain unchanged.
Streaming, SSE handling, completion-marker behavior and all other provider logic
are untouched by this patch.

A duplicate-ID regression test with the configured model present covers both
strict and relaxed modes: both cases reproduced `PROTOCOL_FAILURE` before the
fix and pass afterward. Existing malformed-discovery coverage is preserved and
extended to both modes, including non-string IDs, missing IDs and missing `data`.

| Validation | Result |
| --- | --- |
| Duplicate-ID regression | 2 cases passed within targeted/full suites |
| Requested four targeted test files | 97 passed in 0.25s; exit 0 |
| `python -m pytest -q` | 215 passed in 17.65s; exit 0 |
| Compile with `/tmp/polymind-phase16-pycache` | Exit 0 |
| `docker compose config --quiet` | Exit 0 |
| `helm lint deployment/helm/polymind` | 1 chart linted, 0 failed; informational icon recommendation only |
| `helm template polymind deployment/helm/polymind` | Exit 0; output at `/tmp/polymind-rendered.yaml` |
| `git diff --check` | Exit 0 |

Implementation self-review and a separate pre-commit review found no unintended
interface changes, secrets, dependencies or generated repository artifacts in
this patch. Comparison against the starting working files confirmed that only
readiness validation, its tests and this appended note changed. Existing Phase 16
work and report history were preserved. `git status` and `git diff --stat` show
10 tracked modified files (130 insertions, 13 deletions) from the combined existing
work, plus the previously untracked Phase 16 prompt and report. Work remains on
`master`, uncommitted and unstaged for operator review. **Phase 16 is not complete.**

Azure/cloud resources modified: **NONE**. Kubernetes resources modified: **NONE**.
Live inference traffic performed by Codex: **NONE**. Branch created: **NO**.
Commit created: **NO**. Push performed: **NO**.
