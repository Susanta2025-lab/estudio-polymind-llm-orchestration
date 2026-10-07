# Phase 16 Report — Target-Environment Capacity Calibration & Dependency Headroom Validation

## Current phase result — 2026-10-07 closure

**PASS — PHASE CLOSED.**

**AKS DEPLOYMENT / RUNTIME VALIDATION: COMPLETE / PASS.** The operator's final
live evidence confirms two healthy real PolyMind replicas, the expected image
digest, Foundry generation, shared Redis memory, Chroma/BM25 and real RAG, and the
real application Prometheus/Adapter/custom-metrics path, including active values
and return to idle zero. The final validation posture is two fixed replicas,
HPA absent/disabled, and Foundry capacity unchanged at 10.

**HPA TARGET-CLUSTER SCALE-UP/SCALE-DOWN CALIBRATION: DEFERRED / NOT REQUIRED TO
CLOSE PHASE 16.** Foundry's 10 requests per 60 seconds limit produced an upstream
429 during bounded C2 testing. This dependency-capacity constraint prevents a
useful higher-load AKS autoscaling experiment; it does not invalidate the runtime
validation or block closure. Production readiness and HA are not claimed.

Section O, **Final AKS Application Validation and Phase 16 Closure**, is the
final authoritative status, based on operator-provided evidence recorded on
2026-10-07. It supersedes all earlier blocked/incomplete, awaiting/pending,
not-yet-deployed and next-step statements through N7. Those sections remain
historical evidence of their respective checkpoints, including their original
validation limits; they are not statements of the final retained environment.
Next: **Phase 17 — Production Document Digestion & Intelligence**.
Beginning with **Phase 17A — Architecture, Cost & Risk Assessment**, a
design/read-only assessment. No document-digestion implementation begins here.

## Historical status — 2026-10-04 operator-created AKS assessment

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

## H. 2026-10-05 — Azure-Managed Redis Readiness Assessment

### H1. Decision, scope, and evidence status

**Current managed-Redis compatibility: PARTIAL. Redis is not live-validated or
READY; Phase 16 remains incomplete.** The generic implementation can consume a
standard Redis/TLS endpoint with static credentials without an Azure-specific
adapter. The remaining conditions are service protocol/topology compatibility,
network access, credential delivery, security findings below, and live evidence.

The operator selected **Option B: externally managed Azure Redis** for an
enterprise-style architecture. Every PolyMind replica must use the same external
service and database, with TLS and authentication. Redis has a lifecycle outside
the PolyMind Helm release and outside AKS application pods. No in-cluster Redis
production topology is proposed.

The operator reports AKS `epolymind-aks-dev`, resource group `rg-epolymind`, Spain
Central, ACR `epolymindacrdev`, and a published versioned image. The supplied live
Foundry evidence reports provider `openai_compatible`, model
`epolymind-gpt-54-mini`, readiness `ready`/True, generation
`POLYMIND_PROVIDER_OK`, and streaming `POLYMIND_PROVIDER_STREAM_OK` against
`epolymind-foundry-dev-susanta`. This supersedes earlier inference-blocker notes
for the present assessment; Codex did not repeat those live calls. Redis is the
next dependency. Other Phase 16 prerequisites are not declared resolved here.

Work started on an unchanged `master` working tree. Repository instructions,
all three memory package files, settings, graph consumers, API lifecycle and
probes, Helm templates/values/helpers, requirements, Dockerfile, relevant tests,
README and security documentation were inspected. Only this report was changed.
Public primary-source documentation was consulted to verify client and Azure
semantics; no Azure CLI, Azure account query, Kubernetes command, credential
retrieval, or real Redis connection was performed.

### H2. Runtime path and existing configuration

`Settings` validates `MEMORY_PROVIDER`; `create_memory_store()` returns
`FileMemoryStore` only for an explicitly selected `file` provider. Otherwise it
imports redis-py, calls `redis.Redis.from_url(REDIS_URL, ...)`, and wraps that
client in `RedisMemoryStore`. `get_memory_store()` caches the store per process.
`graph/langgraph_flow.py` obtains it at import and injects it into graph nodes;
`graph/generation.py` reads history before inference and appends the completed
exchange. Streaming appends before emitting `done`. The API history endpoint
reads from the same store, and `/ready` invokes its readiness method.

| Setting | Current behavior |
| --- | --- |
| `MEMORY_PROVIDER` | `file` locally by default; `redis` required in production and selected by chart defaults |
| `REDIS_URL` | Required nonempty for Redis; settings accept `redis://` and `rediss://` with a hostname; Unix-socket URLs are rejected by PolyMind |
| `MEMORY_CONNECT_TIMEOUT` | Positive seconds, default 2; passed as `socket_connect_timeout` |
| `MEMORY_OPERATION_TIMEOUT` | Positive seconds, default 2; passed as `socket_timeout`, not an overall request deadline |
| `MEMORY_HISTORY` | Positive retained-message count, default 6, not six exchanges |
| `MEMORY_TTL` | Nonnegative seconds, default 0; positive values add EXPIRE on each append |
| Client options | `decode_responses=False`; `health_check_interval=30`; no explicit retry policy, pool cap, identity provider, or cluster client |

**There is no silent Redis-to-file fallback.** Construction failure propagates;
operational failures are normalized or make readiness false. Neither path creates
a local memory store. This preserves the shared-state boundary during outages.

Each key is `polymind:memory:` plus the SHA-256 hex digest of the UTF-8 session ID.
The value is a Redis list of JSON messages containing `role`, `content`, and a UTC
ISO timestamp. Reads use LRANGE for the newest requested message count and
validate UTF-8/JSON and message field types. Append queues one RPUSH with both
user/assistant messages, LTRIM, and optional EXPIRE in a transactional pipeline.
Session clearing uses DEL on one derived key. Positive TTL is refreshed by writes,
not reads. TTL zero omits EXPIRE; it does not explicitly remove an existing TTL
after a configuration change. Defaults retain six messages indefinitely per
session, so total session cardinality still determines storage growth.

### H3. redis-py version, TLS, authentication, and service compatibility

`requirements.txt` pins **redis==6.4.0** and Dockerfile installs that requirements
file. However, `import redis` in this assessment's active Python environment
failed with `ModuleNotFoundError`; `python -m pip show redis pytest` confirmed
redis is absent and pytest is 8.4.2. No dependency was installed. The deployed
image's actual installed client was not inspected. Thus client-library findings
below are source inspection of the exact upstream pin, not a local or deployed
runtime demonstration.

In 6.4.0, `rediss` selects SSLConnection. Its actual constructor defaults are
certificate verification `required` and hostname checking `True` (an adjacent
docstring incorrectly says False). It uses the system trust context and SNI.
Percent-decoded username/password support ACL-style or password-only AUTH.
Database selection is supported. URL options can disable verification or override
timeouts; PolyMind does not constrain them. The pool has no practical default cap.
Connections are lazy; health checks run on use, not a background timer. Without
retry options this pool path uses zero configured retries. DNS resolution precedes
socket connection timeouts. These findings follow the
[pinned connection implementation](https://raw.githubusercontent.com/redis/redis-py/v6.4.0/redis/connection.py).

`Redis.from_url()` constructs a pool before constructing Redis: the ordinary
Redis constructor's three-retry default is therefore not applied to that pool.
URL query options take precedence over supplied keyword arguments. Database
precedence is query `db`, path, then default zero. Client close owns/disconnects
this pool; pipeline execution releases its connection in a finally block.
Later calls can reconnect after disconnection, but there is no guarantee a failed
write is replay-safe. See the
[pinned client implementation](https://raw.githubusercontent.com/redis/redis-py/v6.4.0/redis/client.py).

The abstract input shape is
`rediss://<credentials>@<managed-host>:<tls-port>/<db>`; these are placeholders,
not an endpoint or credential recommendation. Use the operator-confirmed hostname
and port, correctly URL-encode credentials, retain verification, and confirm the
runtime trust store. Do not connect using an IP merely to bypass DNS/certificate
checks. A privately signed certificate would additionally require an approved CA
delivery mechanism; the current chart has no dedicated CA volume configuration.

**Service clustering policy is a prerequisite.** The factory constructs `Redis`,
not `RedisCluster`; it has no cluster discovery or MOVED/ASK routing logic.
Select/verify a service mode presenting a compatible non-cluster client endpoint,
and confirm support for this single-key transactional command sequence. Azure
Managed Redis documents Enterprise proxy and Non-clustered policies as alternatives
to OSS clustering. This is a compatibility criterion, not a SKU selection.
An OSS-cluster-required endpoint would need separately scoped generic client work
or a different operator-selected service mode. Verify database-index restrictions
instead of assuming nonzero databases work. See
[Azure Managed Redis architecture](https://learn.microsoft.com/en-us/azure/redis/architecture).

### H4. Authentication choices and credential lifetime

| Approach | Current PolyMind support | Assessment |
| --- | --- | --- |
| Static/access-key-style password | Supported through URL | Smallest Phase 16 path if permitted by service and organizational policy; use TLS, protected delivery, and a rotation runbook |
| Static ACL username/password | Supported by the generic client path | Service must expose the corresponding authentication mode; narrow key and command privileges where available |
| Entra token supplied once as a password | Could authenticate while valid, subject to correct identity/service configuration | Not renewable identity support and unsuitable as a durable deployment configuration |
| Managed identity / renewable Entra authentication | Not implemented | No acquisition, expiry tracking, refresh, pooled-connection reauthentication, or workload-identity setup exists |

Microsoft requires refreshed token authentication before token expiry. A frozen
URL cannot do this. Longer-term enterprise authentication should evaluate managed
identity/Entra with supported renewal and reauthentication, confined to client
configuration infrastructure. It requires additional application integration and
likely an identity/credential-provider dependency plus platform identity work;
none was added. If organizational policy forbids static credentials, identity
integration becomes a blocker rather than a reason to weaken policy. See
[Microsoft Entra authentication requirements](https://learn.microsoft.com/en-us/azure/redis/entra-for-authentication).

Static rotation also is not automatic: update the externally delivered Secret,
roll all application processes, verify recovery, then retire the old credential
using an overlap window if the service permits one. Existing environment variables
and pooled clients do not adopt a changed Secret in place. No secret should be
pasted into this report, a chat, a values file, or a command-line argument.

### H5. Production validation and secret handling

Production requires Redis plus the existing openai-compatible inference,
chroma_http, API authentication, disabled docs, and offline model configuration.
Redis alone cannot satisfy all production checks. The loopback guard compares
host strings against `localhost`, `127.0.0.1`, `::1`, and `host.docker.internal`.
It does not cover every loopback spelling/range or resolve names to reject local
addresses. URL validation does not fully validate port, database, or query options.

**An external `redis://` URL can pass production validation.** Credentials are not
required by settings, and insecure TLS query overrides are not rejected. Production
therefore supports the desired configuration but does not enforce the required
TLS/authentication policy. Use an explicitly reviewed secure URL for validation;
add fail-closed validation later as generic hardening.

The chart path is exact: `application.memoryProvider` becomes ConfigMap
`MEMORY_PROVIDER`; Deployment `envFrom` loads it. Deployment `env.REDIS_URL`
uses `secretKeyRef`, whose name comes from `polymind.secretName` and whose key
comes from `secrets.redisUrlKey`. Defaults are `secrets.create=false`,
`secrets.existingSecret=polymind-secrets`, and key `redis-url`. The URL is absent
from ConfigMap. The Secret must also contain the configured API authentication
token key; the inference key reference is optional. Every replica uses this same
pod template and therefore the same Secret reference.

No committed URL values or chart edits are necessary. Externally materialize a
pre-created Secret in the application namespace through the platform secret
workflow. Optional chart-managed creation uses `stringData` from values and could
expose credentials in rendered manifests/Helm release values; avoid it for this
integration. The pod checksum covers ConfigMap, not external Secret updates.
`MEMORY_HISTORY` and `MEMORY_TTL` exist in Settings but have no chart values/env
wiring; unmodified chart deployments use defaults. Exposing them is optional
unless a retention requirement makes it necessary.

Secret injection puts the URI into the process environment; authorized pod
execution/debugging and dumps can expose it. Secret objects are not automatically
a complete encryption/access-control solution: platform operations must verify
RBAC, backing-store encryption and access restrictions. No such cloud controls
were inspected. See [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/).
The Docker context excludes `.env`, `.env.*` except `.env.example`, and runtime
logs; no real credentials were inspected or added.

### H6. Readiness, errors, cleanup, and failure behavior

`RedisMemoryStore.check_readiness()` executes PING, including connection/TLS/AUTH
when a connection is opened, and catches ordinary exceptions. A truthy response
means ready; false gives `memory_unavailable`. Class names containing `timeout`
normalize to `memory_timeout`; those containing `connection` to
`memory_unreachable`; other read failures become `memory_read_failure`.
AuthenticationError is consequently not given a distinct authentication category.
Reads/writes raise safe `MemoryError` subclasses with fixed messages and retain
the original exception as their cause.

`/ready` checks inference, memory, vector store, and BM25 sequentially. It returns
200 only when all are ready, otherwise 503 with component statuses. `/health`
returns process liveness independently. This separation is suitable for removing
unready replicas from Kubernetes traffic without dependency-driven restarts.
PING validates connectivity/authentication/command execution, but does not prove
write permission, memory headroom, transaction support, durability, or that
previously committed history survived failover.

Socket waits have finite defaults; **there is no strict end-to-end readiness
deadline**. DNS, multiple addresses, handshake steps, URL overrides, and sequential
dependency checks prevent claiming a two-second overall bound. The Helm readiness
probe timeout is five seconds. Kubernetes can time out that probe while the worker
is still running. Failure duration and recovery need measurement, and a global
budget is a hardening candidate. Valid configuration plus a TLS/auth outage
normally produces sanitized unready status without crashing the process; invalid
client options or missing redis-py can instead fail construction at graph import.

| Failure | Expected application behavior, without URL retry overrides |
| --- | --- |
| Redis unavailable / refused connection | Request fails safely; PING makes memory unready; later calls may reconnect; no local fallback |
| DNS failure | Usually normalized as connection failure; OS resolver duration is not guaranteed by socket timeout |
| TLS/certificate failure | Caught by store operations/readiness; exact category depends on exception class; never disable verification to recover |
| Authentication failure | Readiness false, generally `memory_read_failure`; request errors sanitized; no credential refresh |
| Expired or rotated credential | Authentication failures when enforced by service/on reconnect; remains broken until valid credentials and processes are updated |
| Connect timeout | `memory_timeout` when raised as a timeout class; request fails/readiness false |
| Operation timeout | Same visible failure; an already-sent write may have committed despite its lost response |
| Restart/failover | Affected requests can fail; subsequent pool reconnection can recover with a valid endpoint/credential; state survival is service-dependent |
| Transient disconnect | No application retry; failed request is not transparently guaranteed success; later access can recover |

These are implementation/source expectations, not live observations. No row
falls back to file. Reconnection is not token renewal or exactly-once delivery.
Readiness/client-facing error bodies do not include the URI. However, log leakage
is a real residual risk described below, so safe logging cannot be asserted for
all failure paths.

Shutdown invokes `close_memory_store()` from FastAPI lifespan, then vector and
inference cleanup. The store delegates to client close, and the cached singleton
is reset. There is no isolation around a close exception: memory cleanup failure
could prevent subsequent component cleanup. Factory-created standalone test
stores must be closed explicitly; closing only the singleton would miss them.

### H7. Security and two-replica semantics

**Logging gap:** `graph/streaming.py` handles MemoryError with `logger.exception`.
Because the store raises `from exc`, the full chained upstream exception is logged.
An upstream exception can contain sensitive values or a pipeline command's
synthetic/real message content. No direct normal-path Redis URL logging was found,
but safe outer messages do not sanitize chained tracebacks. This conflicts with
README's unconditional no-leak claim. Fix this path and add sentinel-based log
tests before credentialed streaming failure validation. Generic streaming catches
deserve the same review. Normal API memory handlers and readiness logs use bounded
categories, not raw exceptions.

`REDIS_URL` is a plain `str`, not a secret type. Settings representations/dumps,
Pydantic validation input rendering, and uncaught constructor errors are additional
potential exposure paths. No settings dump logger was found. Masking settings and
normalizing early construction errors are recommended, without silently hiding
configuration failures. Keep debug tracing and raw settings/error dumps out of
the later operator harness.

Both replicas see the same history when hostname/service, DB and session ID agree.
There is no per-pod namespace. Append avoids a read/modify/write overwrite: both
messages are in one RPUSH and the transaction serializes append/trim/expiry against
other clients. Trimming intentionally removes older entries. Odd history limits
may retain a partial oldest pair. This is not a lock over read → inference → write:
simultaneous requests may generate from the same old history and append in
completion order, not arrival order. Clear-versus-append and expiration-versus-read
races also remain possible. Avoid parallel requests to one synthetic session when
validating basic conversational continuity.

Redis transactions do not roll back commands that encounter execution-time
errors; lost EXEC acknowledgments can leave the commit outcome unknown. Therefore
README's statement that failed transactions never persist partial exchanges is
too broad. RPUSH itself writes the pair together, but a later trim/expiry failure
may leave retention inconsistent. Caller retries can duplicate exchanges; there
is no idempotency token, durable acknowledgement, or distributed conversation
lock. These qualifications follow
[Redis transaction semantics](https://redis.io/docs/latest/develop/using-commands/transactions/).

SHA-256 collision risk is negligible for practical use, but intentional reuse of
the same session ID shares data. API requests default to session `default` and
allow caller-supplied IDs up to 256 characters. There is no tenant/user ownership
binding: a shared API token is not per-session authorization. Use unique session
IDs and a dedicated service/database scope for this validation. The fixed key
prefix also means unrelated deployments sharing the same DB/session IDs collide
logically. A constructor prefix exists but is not settings/factory configurable.
Tenant isolation and configurable environment namespacing are future scope if
the deployment expands beyond one trusted application boundary.

Least privilege should cover only the application's key prefix and required
LRANGE, RPUSH, LTRIM, EXPIRE when enabled, DEL, PING and transaction commands,
plus service/client-required authentication/connection initialization commands.
Confirm the selected service's ACL capabilities; do not assume access keys are
fine-grained identities. Diagnostic SET/GET require separately considered test
permissions and must not unnecessarily expand production privileges.

### H8. Helm policy versus actual network security

The chart defaults Redis egress to TCP 6379 and a combined namespace/pod selector
for an in-cluster dependency, with empty `ipBlocks`. That default does **not**
describe the managed endpoint. Existing `networkPolicy.egress.redis.port` and
`ipBlocks` already allow a reviewed external TCP port and destination CIDRs, so
no template change is necessary for a stable, known external destination.

Within the selector peer, namespaceSelector AND podSelector must match. The
additional ipBlock peers are alternatives. The template always retains its
selector peer; adding CIDRs does not remove that allowance. If tightening it,
choose appropriately restrictive labels; empty selectors would broaden access.
Removing selector peers entirely would require optional-peer template work, which
is not necessary merely to connect. DNS is allowed over UDP/TCP 53 to selected
CoreDNS pods; verify actual AKS resolver labels, NodeLocal DNS if present, and
private-zone forwarding rather than assuming these defaults match.

Standard NetworkPolicy has no FQDN matching. Dynamic public IPs or changing
private endpoint addresses need a platform-maintained CIDR strategy or a separately
selected policy/egress mechanism. NAT and CNI behavior must be checked in the
actual topology. See [Kubernetes NetworkPolicy semantics](https://kubernetes.io/docs/concepts/services-networking/network-policies/).

**Operator-provided Phase 16 fact: AKS NetworkPolicy enforcement is not enabled.**
Rendering or applying this chart policy would not prove enforcement. Actual
protection must be assessed from Azure routing, NSGs/firewalls, service public
access settings, and private networking. No such controls were queried here.
This is an unresolved enterprise security evidence gap even if connectivity works.

### H9. Preferred enterprise networking and operator ownership

Prefer a private endpoint/private-network path from AKS with correct private DNS,
TLS and authentication, and no unrestricted public application path. Azure Managed
Redis supports Private Link; validate support and behavior for the selected
resource/service. Preserve the service's certificate-valid client hostname while
resolving it through private DNS. Private endpoint approval, zone links and public
access restrictions require explicit platform configuration. See
[Azure Managed Redis Private Link](https://learn.microsoft.com/en-us/azure/redis/private-link).

A public endpoint with TLS/authentication and narrowly restricted network rules
is a possible policy-approved validation alternative only if the selected service
supports the required restrictions. It depends on known AKS egress identity/IPs
and exposes more network surface. Do not substitute unrestricted public access
for missing private connectivity. No existing VNet/subnet arrangement is assumed.

Before choosing, the operator must inspect AKS node and pod network mode, VNet
and subnet IDs/address ranges, managed node resource group where relevant,
peering, endpoint-subnet suitability, routes/UDRs, outbound NAT/egress IPs,
NSGs/firewalls, and address-space overlap. Confirm service private endpoint
support/approval, DNS zone and VNet links, custom DNS forwarding, resolution from
pods, and bidirectional routing. Determine actual NetworkPolicy/CNI enforcement
separately from chart values. None of this inspection was run in this task.

| Owner | Responsibility |
| --- | --- |
| PolyMind | Provider-neutral memory abstraction, client configuration, timeouts, JSON/list storage, session semantics, readiness, safe errors, cleanup |
| Azure-managed Redis service | Server/infrastructure lifecycle and patching; availability, replication, persistence and backup/recovery only to the extent offered/configured by the chosen service/tier |
| AKS/platform operators | Network/DNS reachability and enforcement, secret delivery and rotation, workload/image deployment, identity setup if later selected, monitoring integration and recovery procedures |

No HA, backup, persistence, recovery point, or service-level guarantee can be
inferred from PolyMind code. Phase 16 needs a small development workload with
shared state, TLS, authentication, sufficient connections/latency and availability
for validation, preferably private access. Large memory capacity is not justified
at this stage. Select capacity, eviction/retention and availability deliberately;
actual SKU and cost selection is separate and requires current Azure information.
No price estimate or resource provisioning is part of this assessment.

### H10. Test coverage, missing tests, and local validation

| Area | Existing coverage | Gap before live managed-service validation |
| --- | --- | --- |
| Factory | Mock verifies URL, timeouts, binary responses, health interval, history and TTL | Real pinned client construction without connecting; TLS class/defaults, auth decoding, DB, URL overrides, pool ownership/retries |
| Settings | Provider, nonempty URL, positive limits/timeouts, production Redis and rediss example, selected loopback rejection | Malformed URL/port/DB/query; insecure external URL acceptance documented; later TLS/verification/secret masking regressions |
| Memory data | Fake verifies ordering, trim, TTL command, session hashing/isolation, clear, concurrent pairs and malformed reads | Two independent stores; actual expiry; odd limits; mixed TTL settings; managed transaction contract |
| Failures | Fake connection/timeout/read/write normalization | Real redis exception types for DNS/TLS/AUTH; failed append/clear; explicit no-FileMemoryStore spy across construction and runtime failures |
| Readiness | API fake proves memory failure → 503 and independent liveness; sanitized response shape | Direct Redis PING true/false/errors, ACL write-denied despite PING, measured timeout/recovery; HTTP boundary with real store + mocked transport |
| Shutdown | Lifespan test verifies cleanup callbacks | Factory singleton reset, real pool close ownership, store/client close, cleanup when one close raises |
| Helm | Defaults ≥2 replicas, external services, Secret refs, no URL in ConfigMap, lint/render | Parsed custom Secret/key reference assertions; external Redis CIDR/TLS-port render; absence of generated Secret; rotation contract |
| Security | Bounded metrics and safe outer error strings | Sentinel username/password/token/URI and message-content absence from streaming logs, settings validation and constructor failures |

The fakes implement an idealized successful transaction under a Python lock; they
do not prove real Redis rollback, failover, expiry, TLS or cluster behavior. The
tests do not assert an automatic file fallback because none exists in code; an
explicit negative regression is still valuable. No tests were modified or added.

Local checks actually run:

| Command/check | Result |
| --- | --- |
| `python -m pytest -q -p no:cacheprovider tests/unit/test_memory_store.py tests/unit/test_memory_integration.py tests/unit/test_deployment_topology.py tests/unit/test_helm_chart.py` | **45 passed in 17.85s**, exit 0 |
| `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider tests/unit/test_api_reliability.py tests/unit/test_streaming_orchestration.py` | **25 passed in 0.48s**, exit 0 |
| `helm lint deployment/helm/polymind` | 1 chart linted, 0 failed; informational icon recommendation |
| `helm template polymind deployment/helm/polymind > /tmp/polymind-redis-assessment.yaml` | Exit 0; local manifest only, no deployment |
| Parsed default and synthetic override renders | Verified two replicas, Redis selection, URL absent from ConfigMap, no generated Secret, default/custom Secret references, configurable external CIDR and TCP port; exit 0 |
| Local redis import / package metadata | redis absent; no installation or real-client execution claimed |
| `git diff --check` and append-only comparison with HEAD | Passed; historical report preserved byte-for-byte |

Full pytest, compilation and Docker builds were not necessary for this
documentation-only assessment and were not run. These 70 passing tests are
repository regression evidence, not managed Redis readiness evidence.

### H11. Required changes versus hardening

No Azure-specific Redis abstraction, application connectivity rewrite, new cloud
SDK, or Helm Secret template change is required for a compatible standard endpoint.
The following separates connection prerequisites from safe end-to-end validation.
All proposed changes remain unimplemented.

| Category | File(s)/owner | Reason and scope | Behavior changes | Test requirement |
| --- | --- | --- | --- | --- |
| **A. REQUIRED BEFORE MANAGED REDIS VALIDATION** | Operator runtime; existing `requirements.txt` | Ensure the validation/deployed runtime actually contains pinned redis-py; absent locally | Environment only; no new dependency declaration | Offline real-client construction/version check |
| A | Operator service/network/Secret configuration; external deployment values | Confirm standard-client mode, DB/transactions, actual TLS endpoint, route/DNS, static-auth policy and shared Secret; set existing egress port/CIDRs as applicable | Deployment configuration only | DNS/TLS/AUTH and transaction/shared-session checks below |
| A, before credentialed API/streaming failure tests | `graph/streaming.py`, `tests/unit/test_streaming_orchestration.py` | Eliminate raw chained memory exception logging; broader generic catch review | Logging only, retain client error contract | Sentinel credentials/URI/content absent from logs and responses |
| A, validation evidence | Existing memory/topology/Helm/API test files | Add focused offline rediss/auth/factory, no-fallback, PING errors/close and external Secret/policy checks identified above | Tests only | Run with the pinned real client and mocked transport, no service required |
| **B. RECOMMENDED HARDENING** | `config/settings.py`, factory, settings tests | Require production TLS/auth policy, reject insecure verification overrides, validate URL options/port/DB and broader loopback forms; protect URL repr/validation errors | Rejects previously accepted insecure/malformed config; unwrap secret internally if introduced | Positive secure and negative insecure inputs, secret-redaction tests |
| B | `memory/provider_factory.py`, `api/app.py`, chart probe values | Explicit pool/retry policy and overall readiness budget; protect all shutdown cleanup | Operational limits; do not add blind write retries | Timeout, pool exhaustion, lost-ack and cleanup cases |
| B | Chart values/configmap, memory factory/settings if required | Expose retention/history and environment prefix only when needed; optional external-only policy peer support | Optional configuration, preserve defaults deliberately | Render/TTL/key compatibility tests |
| B | `README.md`, security/deployment docs | Qualify no-leak, transaction, deadline and secret-rotation claims | Documentation only | Cross-check against implementation and sentinel tests |
| **C. NOT REQUIRED FOR PHASE 16** | Future identity infrastructure/factory | Entra token acquisition/renewal, Azure identity dependencies | New authentication mode, separately scoped; becomes required only if static auth is forbidden | Renewal, reauthentication, expiry and identity-failure tests in that future scope |
| C | Future generic client work | RedisCluster support if a standard-client-compatible endpoint is selected | No change now; required later only if service mode demands it | Cluster routing/failover tests if introduced |
| C | Graph/API/storage design | Distributed conversation locks, idempotent writes, tenant authorization redesign, in-cluster Redis | No speculative redesign; in-cluster production Redis is excluded | Scope separately when requirements demand stronger guarantees |

### H12. Non-secret operator inputs needed later

After separate authorized resource selection/creation, provide only:

1. Exact Azure service/product and resource name, resource group, region and
   selected tier/capabilities; Redis protocol/version and clustering policy.
2. Certificate-valid client hostname, actual TLS port, required TLS version/CA
   trust, database/index support and selected index; supported transaction commands.
3. Authentication mode, whether static keys are allowed, whether a username is
   required, privilege scope and rotation/expiry policy. Do not supply keys/tokens.
4. Private/public access mode, public-access restrictions, endpoint approval and
   private IP/subnet information, relevant VNet/peering/routing/NSG facts, DNS
   zone/link/forwarding configuration and pod-side resolution result.
5. AKS egress identity/IPs if public access is selected; actual policy enforcement
   status and approved destination CIDRs/ports, separately from Helm declarations.
6. Application namespace, existing Secret name and key names, protected delivery
   mechanism and rollout owner; deployed image tag/digest and installed client version.
7. Intended replica count (at least two), connection limit, history/TTL/eviction
   policy, persistence/availability expectations and agreed validation/failure window.

Credentials belong in the operator's approved secret store and the referenced
Kubernetes Secret, delivered without source control, shell-history or report
exposure. No secret contents are required to resolve the non-secret design choices.

### H13. Later live validation plan — designed, not executed

Run only after separate operator authorization, the relevant security fix/tests,
and protected credential delivery. Use an approved environment on the intended
AKS network path and the deployed application image where possible. Bound each
test with a wall-clock deadline as well as socket timeouts. Record pass/fail,
duration, non-secret endpoint facts and sanitized categories, not connection URIs
or raw exception tracebacks. Do not enable verbose command logging.

1. Resolve the supplied hostname from the intended environment, eventually from
   each application pod. Compare to approved private/public addresses and verify
   private DNS/route expectations.
2. Establish TLS with hostname and certificate verification enabled. Verify the
   expected certificate identity/trust without bypass flags.
3. Load credentials through the protected environment/Secret, authenticate and
   PING using the pinned client; never print the URL or credentials.
4. Generate a unique `polymind:phase16:<random-run-id>:probe` key. Perform a small
   SET with a short expiry and collision protection, GET/compare the synthetic
   value, then DEL that exact key in a finally block. Keep a cleanup ledger; TTL
   protects against interrupted cleanup. No key scans or database-wide deletion.
5. Construct `Settings` and `create_memory_store()` with the real approved
   configuration; verify provider `redis` and store readiness. Do not dump Settings.
6. Through the real RedisMemoryStore, use a fresh
   `phase16:<random-run-id>:<session>` session, read empty history, append synthetic
   exchanges, read back ordered content, test trimming/isolation and optional
   expiry. Factory keys remain `polymind:memory:<sha256(session)>`; record these
   exact derived test keys for cleanup. The factory does not expose a custom
   prefix, so do not pretend a session prefix appears literally in Redis keys.
   Apply a short safety TTL to exact test keys if needed; always clear the session
   through the store and close clients in finally blocks.
7. Confirm the full application `/ready` returns 200 with memory ready. Inference,
   Chroma and BM25 must also be ready; isolate their failures rather than attributing
   every 503 to Redis. Check `/health` independently.
8. With two replicas referencing the same external Secret/DB, direct a synthetic
   write/query to pod A, verify its history on pod B, then reverse direction using
   the same session. Test another session remains isolated. Use approved direct
   pod access to prove routing actually crossed pods, not just repeated load-balancer
   calls. Exercise API persistence as well as independently constructed stores.
9. Optionally test simultaneous appends with small synthetic payloads and a large
   enough history limit. Assert intact pairs and expected retention, without
   asserting request-arrival ordering or exactly-once retries.
10. In an isolated validation instance/canary, inject unreachable endpoint, DNS,
    TLS and invalid-auth conditions or an approved scoped network interruption.
    Do not stop/delete the managed service, rotate a shared live credential, or
    disrupt unrelated workloads. Verify `/health` remains 200, `/ready` fails or
    reaches its probe deadline, requests return safe errors, no file fallback
    occurs, and logs contain no sentinels/credentials. Restore configuration and
    prove readiness/reconnection recovery. Actual service failover testing, if
    desired, needs its own approved service-specific plan.
11. Delete only the exact recorded synthetic keys/sessions, confirm cleanup,
    close clients and record results. **Never use FLUSHALL or FLUSHDB.**

### H14. Conclusion and review record

The safest minimal path is a standard-client-compatible, external Azure-managed
Redis endpoint, private connectivity where appropriate, verified TLS, and static
credentials delivered through the existing Secret path if policy allows. Preserve
the provider-neutral abstraction. No application or chart connectivity feature
has been shown to require Azure-specific code. Fix the demonstrated logging risk
before credentialed streaming failure validation and add focused missing tests.

Outstanding blockers are endpoint/service/auth/DB selection, actual client runtime
verification, network/DNS/security evidence, secret delivery, the logging/test
gate, and live shared-session/failure evidence. Entra-only policy or a mandatory
cluster-aware service mode would add explicit implementation work. Production
hardening and broader Phase 16 dependency/operational validation remain open.

Assessment self-review checked architecture, compatibility, concurrent writes,
failure handling, lifecycle, sources and test limitations. Separate pre-commit
review checked the report for secrets, executable provisioning instructions,
unproven readiness claims, unrelated changes and historical preservation. No
implementation, tests, Helm files or dependencies were modified. Existing report
history is preserved; this assessment is intentionally not a deployment approval
or a declaration that Redis/Phase 16 is READY.

Final `git status --short --branch` shows `master...origin/master` and only
`docs/codex/reports/phase_16_report.md` modified. `git diff --stat` records one
file changed, with an append-only assessment; nothing is staged.

Azure resources created/modified: **NONE**. Kubernetes resources created/modified:
**NONE**. Live Redis calls: **NONE**. Branch created: **NO**. Commit created: **NO**.
Push performed: **NO**. Work remains on `master`, uncommitted for operator review.

## I. 2026-10-05 — Redis streaming security and offline regression patch

This narrow follow-up addresses the streaming memory log-leak finding in section
H and protects the existing generic external Redis contract. Managed-Redis
compatibility remains **PARTIAL**, Redis is **not READY**, and Phase 16 remains
incomplete. No managed-service connection or deployment was attempted.

### I1. Security change and compatibility

`graph/streaming.py` now uses `logger.error` instead of `logger.exception` in the
`MemoryError` handler. Previously, the normalized exception retained its upstream
cause and logging included the chained traceback. Now the log contains only the
existing request ID, route, memory provider and bounded category. It does not
attach exception information or render the exception/cause. The existing key=value
logging format is preserved; unrelated inference/vector/generic handlers are
unchanged. This is a memory-handler fix, not a claim that all previously identified
settings, construction or unrelated exception-logging risks have been resolved.

The client error remains exactly `{"type": "error", "message": "Conversation
memory is unavailable."}`. A failed history read emits only the error; a failed
append after generation retains prior metadata/chunks, emits the error and does
not emit `done`. No retry, fallback, provider boundary, configuration or memory
storage behavior changed.

Two security regressions exercise the real `RedisMemoryStore` with a fake failing
client, covering both read and append. The upstream exceptions carry clearly
synthetic username, password, hostname, full URI and private message sentinels.
Both tests failed before the fix and pass afterward. They assert sentinel absence
from rendered logs, captured exception text and client events; log records must
have neither `exc_info` nor `exc_text`. They also assert the exact bounded log,
request correlation, unchanged client error, and absence of query/session content
from logs. All URI/authentication values added by this patch are test-only values
using reserved `.invalid` domains.

### I2. Regression coverage and dependency verification

`tests/unit/test_memory_integration.py` extends factory coverage to rediss URLs
carrying password-only and ACL username/password authentication. These cases
verify Settings acceptance, RedisMemoryStore selection, exact URL forwarding,
connect/operation timeouts, binary responses, health interval 30, history and TTL.
Separate construction/runtime failure cases spy on FileMemoryStore, check that
no local memory directory/file is created, retain `MEMORY_PROVIDER=redis`, and
verify propagated construction errors, normalized runtime errors and unready
PING results. The runtime test also closes its client.

Two real-client parsing cases are included for environments with the project
dependency installed. They check redis-py 6.4.0, SSLConnection selection,
certificate-required and hostname-verification defaults, percent-decoded fake
passwords, optional ACL username, host/port/database and propagated options. DNS,
socket creation and connection calls are guarded to fail the tests rather than
access a network; clients/connections are closed. **These two cases were skipped
locally** because redis-py is absent. No dependency installation or version change
was performed, and real-client parsing is not reported as executed evidence.

`tests/unit/test_memory_store.py` adds six PING cases: success, false response,
connection error, timeout, authentication-style exception and generic read error.
These use offline doubles (including the authentication exception name) and
assert existing readiness categories without inventing a new auth category.
Existing API tests still verify `/ready` failure independently of `/health`.

`tests/unit/test_helm_chart.py` parses default-name and custom-name external Secret
renders. It verifies Redis selection in ConfigMap, no Redis URL there, exact
secretKeyRef name/key, no chart-owned Secret, and a shared Deployment pod template
for at least two replicas. A synthetic `192.0.2.0/24` CIDR and custom TCP port
are asserted in the same egress rule. No chart values/templates changed; Redis
remains externally operated. This proves rendering only: operator-reported AKS
NetworkPolicy enforcement remains disabled and no isolation test was performed.

`requirements.txt` still pins **redis==6.4.0**. Dockerfile copies the requirements
file and installs it with `pip install -r requirements.txt`. Local package metadata
confirmed redis-py is absent. The deployed image was not inspected or rebuilt.
There are no new dependencies, Azure-specific code, Entra/identity support,
cluster clients, locks or retry-on-write changes.

### I3. Validation and reviews

| Check | Result |
| --- | --- |
| Sentinel regression before fix | 2 failed, 6 deselected in 0.25s; reproduced chained exception disclosure |
| Requested six-file targeted pytest run | **84 passed, 2 skipped in 18.30s**, exit 0 |
| `python -m pytest -q` | **229 passed, 2 skipped in 12.97s**, exit 0 |
| Skips in both suites | Only the two real-client TLS/static-auth parsing cases; pinned redis-py absent locally |
| Compile with `PYTHONPYCACHEPREFIX=/tmp/polymind-phase16-redis-pycache` | Exit 0 |
| `docker compose config --quiet` | Exit 0 |
| `helm lint deployment/helm/polymind` | 1 chart linted, 0 failed; informational icon suggestion |
| `helm template polymind deployment/helm/polymind` | Exit 0; output `/tmp/polymind-phase16-redis.yaml` |
| `git diff --check` | Exit 0 |

Implementation self-review inspected the complete implementation/test diff,
client contract, correlation, failure causes, test isolation, no-fallback checks,
cleanup and render assertions. A separate pre-commit security review confirmed
that the only runtime change is the memory logging call/comment, test credentials
are synthetic, no settings dumps or raw exception formatting were introduced,
and there are no dependency, chart, configuration or unrelated implementation
changes. No configured lint/format tool was found. Temporary logs/manifests and
the compile cache are under `/tmp`; no generated artifact is included in the diff.
The report's prior history, including the uncommitted assessment, is preserved.

This patch passes its executed offline checks, with the explicit real-client
environment limitation above. Repeat those two construction tests in the approved
runtime containing the pinned dependency before treating TLS/auth parsing as
locally verified. Live DNS/TLS/authentication, two-pod state sharing and failure
recovery remain operator validation work; this patch does not establish managed
Redis readiness.

Work remains directly on `master`, unstaged and uncommitted. `git status` and
`git diff --stat` show six modified files: the streaming module, four test files,
and this report (including the earlier assessment). No new branch was created.

Azure resources modified: **NONE**. Kubernetes resources modified: **NONE**.
Live Redis calls: **NONE**. Branch created: **NO**. Commit created: **NO**.
Push performed: **NO**.

## J. 2026-10-05 — Azure Managed Redis Stage A discovery and approval plan

**Stage A only; STOP before provisioning.** No approval for Stage B has been
received. Redis remains **PARTIAL / NOT LIVE VALIDATED** and Phase 16 is incomplete.
This section records read-only Azure/Kubernetes discovery and a proposed plan,
not deployed resources or successful Redis connectivity. The working tree was
clean on `master` at the start; the earlier security patch is now in repository
history. The active local Python environment now contains redis-py **6.4.0**.

### J1. Verified subscription, tools and service availability

The active subscription is `ECI-Development`, state Enabled. `rg-epolymind` exists
in `spaincentral` with provisioning state Succeeded; its group-level tags are
currently null. No `Microsoft.Cache/redisEnterprise` resource was returned by
subscription inventory, so no existing Managed Redis instance can be reused.
`Microsoft.Cache` is **NotRegistered**; `Microsoft.Network` is Registered.
No policy assignments were returned by the subscription policy-assignment list.
This does not substitute for successful service-side policy/RBAC validation.
Do not bypass any denial of access-key authentication or other policy at creation.

Azure CLI is **2.89.1**. The `redisenterprise` extension was initially absent;
the installed CLI's dynamic-install behavior installed stable **1.4.0** when
its help was requested. This was a local tooling change, not an Azure mutation.
Installed `az redisenterprise create --help` and database create help were read.
The extension uses stable API **2025-07-01** for creation. Verified flags include
`--sku Balanced_B0`, `--high-availability Disabled`,
`--public-network-access Disabled`, `--minimum-tls-version 1.2`,
`--client-protocol Encrypted`, `--clustering-policy EnterpriseCluster`,
`--port 10000`, and `--access-keys-auth Enabled`. No create command was executed.
The CLI help has conflicting descriptions of authentication defaults; Stage B
must explicitly set the approved value. Do not use legacy `az redis create`.
See [current CLI reference](https://learn.microsoft.com/en-us/cli/azure/redisenterprise?view=azure-cli-latest).

Provider metadata lists Spain Central for redisEnterprise and includes stable API
versions. Current Spain Central retail meters exist for B0, B1, B3, B5, X3 and M10.
The smallest catalog candidate is **Balanced_B0**, a GA in-memory SKU (not marked
preview in current pricing/creation documentation). This is catalog/region
evidence, **not guaranteed allocatable capacity or quota for this subscription**.
The CLI's SKU-list operation is for scaling an existing instance, not pre-creation
capacity discovery. If Azure rejects B0/EnterpriseCluster/non-HA in Spain Central,
stop and report; do not silently choose a larger SKU, OSSCluster or another region.

Memory-size caveat: the current Microsoft pricing page labels B0 as **1 GB**,
while the overview lists the Balanced range starting at **0.5 GB**. Treat B0 as
the approximately 0.5–1 GB development class; the documentation is inconsistent
and this assessment does not claim a measured usable-memory figure. No workload
requires resolving that discrepancy by increasing capacity. Service properties
and the later bounded test must confirm the actual available memory.
Non-HA is documented for dev/test and explicitly supported by the CLI; there is
no HA availability guarantee in that mode. Sources:
[pricing](https://azure.microsoft.com/en-us/pricing/details/managed-redis/),
[overview](https://learn.microsoft.com/en-us/azure/redis/overview), and
[creation guidance](https://learn.microsoft.com/en-us/azure/redis/quickstart-create-managed-redis).

EnterpriseCluster presents the proxy endpoint needed by the existing `Redis`
client. PING, LRANGE, RPUSH, LTRIM, EXPIRE, DEL and single-key MULTI/EXEC are
compatible with the documented command model; actual execution remains to be
proved. All commands in PolyMind's append transaction address one key. SELECT is
blocked by the service, so use DB 0 (the client need not issue SELECT for DB 0).
No modules, geo-replication, OSSCluster or preview NoCluster are proposed. Sources:
[architecture](https://learn.microsoft.com/en-us/azure/redis/architecture) and
[command restrictions](https://learn.microsoft.com/en-us/azure/redis/configure).

### J2. Observed AKS network and safer topology

AKS `epolymind-aks-dev` is provisioned successfully in Spain Central, with an
agent pool configured for two Standard_D4s_v4 nodes. It uses Azure CNI Overlay,
Azure dataplane, public API, OIDC and workload identity enabled, and
`networkPolicy=none`. Node readiness was operator-provided; this discovery did
not replace that with a fresh node readiness measurement.

| Network fact | Read-only finding |
| --- | --- |
| Node resource group | `MC_rg-epolymind_epolymind-aks-dev_spaincentral` |
| VNet | `aks-vnet-36185111`, `10.224.0.0/12`, in the managed node resource group |
| Node subnet | `aks-subnet`, `10.224.0.0/16`; verified from VM scale-set NIC configuration because AKS agent-pool subnet ID was null |
| Other subnets | `aks-appgateway`, `10.238.0.0/24`, delegated to traffic controllers; `aks-virtualkubelet`, `10.239.0.0/16`, delegated to container groups |
| Pod / service CIDRs | `10.244.0.0/16` / `10.0.0.0/16`; DNS service IP `10.0.0.10` |
| Outbound | Standard load balancer, one effective static public outbound IP; its resource/value were verified but are unnecessary for private Redis access |
| Routes | No subnet route-table association; no route-table resources returned in the node resource group; future effective peering routes are not yet validated |
| NSG | `aks-agentpool-36185111-nsg` on node subnet; no custom rules, only default VNet/LB/Internet allow and terminal deny rules; no VMSS NIC-level NSG |
| VNet DNS | No custom DHCP DNS settings; CoreDNS forwards to `/etc/resolv.conf`; `coredns-custom` has no data |
| Existing connectivity | No VNet peerings, private endpoints or private DNS zones found in subscription inventory |
| Managed-resource controls | Node resource-group lockdown profile null; no locks returned for that resource group |
| Kubernetes namespaces | Only default/system namespaces; no PolyMind namespace exists yet |

The subscription inventory exposed only the AKS-managed VNet. There is no observed
operator-controlled reachable subnet to reuse, and the existing non-node subnets
are delegated. **Choose topology C:** a separate operator-controlled PolyMind
VNet/private-endpoint subnet, with explicit bidirectional peering. Do not add a
subnet inside the AKS-managed VNet, change its address space, or modify node/NSG/
route/AKS properties. One peering child resource in the managed VNet is the only
proposed write under the MC_ resource group and requires the Stage B approval.
Microsoft documents peering with the AKS node-resource-group VNet, while warning
against arbitrary changes to managed resources. Sources:
[documented AKS peering](https://learn.microsoft.com/en-us/azure/aks/private-cluster-connect)
and [managed-resource cautions](https://learn.microsoft.com/en-us/azure/aks/faq).

Proposed `vnet-epolymind-private-dev` uses `10.50.0.0/24`; its
`snet-private-endpoints` uses `10.50.0.0/27`. These do not overlap any discovered
VNet/pod/service range. Recheck inventory before writes; unseen external network
plans remain an operator consideration. Peerings allow VNet access only: no
gateway transit, remote gateway, or forwarded-traffic feature is needed.
No new NSG, route table, public IP, NAT gateway, DNS resolver appliance or AKS
network-policy change is proposed.

Expected data path is pod → node-side overlay egress → VNet peering → private
endpoint → Redis, on TCP 10000. This is a design expectation, not a live routing
result. Redis public network access must be disabled from creation onward.

Create zone `privatelink.redis.azure.net` in `rg-epolymind`, with non-registering
links to both the AKS VNet and new endpoint VNet, and an endpoint DNS zone group.
Clients use the normal certificate-valid service hostname, never the private-link
alias directly. Given Azure-provided VNet DNS and the observed CoreDNS forwarding,
pod resolution is expected to use the linked private zone without a CoreDNS edit;
prove this in Stage B. Peering alone does not provide the required DNS link.
See [Private DNS service mapping](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns)
and [Managed Redis Private Link](https://learn.microsoft.com/en-us/azure/redis/private-link).

### J3. Verified retail pricing before approval

Public [Azure Retail Prices API](https://prices.azure.com/api/retail/prices)
queried on **2026-10-05**, USD Consumption prices, with region `spaincentral` and
product names containing `Azure Managed Redis`. Redis meters below have effective
start date 2025-06-01 and unit `1 Hour`. These are current API-returned public
retail rates, not a subscription-discount quote. Monthly arithmetic uses 730 hours.

| Candidate, non-HA one-node basis | Hourly USD | Monthly USD |
| --- | --- | --- |
| Balanced B0 — proposed | 0.019 | 13.87 |
| Balanced B1 | 0.038 | 27.74 |
| Balanced B3 | 0.077 | 56.21 |
| Balanced B5 | 0.186 | 135.78 |
| Memory Optimized M10 | 0.257 | 187.61 |
| Compute Optimized X3 | 0.261 | 190.53 |

The proposed B0 meter ID is `1278b376-3839-55e1-bf63-9f486dc4e204`, product
`Azure Managed Redis - Balanced`, ARM SKU `Azure_Managed_Redis_Balanced_B0`.
Microsoft's pricing page distinguishes one-node non-HA from two-node HA pricing;
this estimate is explicitly one-node, not a production HA configuration.

Additional current public meters: one Standard Private Endpoint is **USD 0.01/h**
(**7.30/month**); one Private DNS zone in the first tier is **USD 0.50/month**.
Fixed estimate: **USD 0.029/h plus USD 0.50/month**, or **USD 21.67/month**.
Private Link data processing adds USD 0.01/GB in each direction at the first tier;
same-region peering adds USD 0.01/GB for ingress and USD 0.01/GB for egress at the
applicable ends; private DNS queries are USD 0.40/million. No traffic volume is
assumed. Taxes, exchange rates, commercial discounts, and existing AKS costs are
excluded. No paid resolver, fixed-capacity Private Link tier, or new public IP is
included. Sources: [Private Link pricing](https://azure.microsoft.com/en-us/pricing/details/private-link/),
[DNS pricing](https://azure.microsoft.com/en-us/pricing/details/dns/), and the
retail API's Global Private Link/peering and Private DNS meters. Pricing responses
were retained only under `/tmp`; they contain no credentials.

### J4. REDIS PROVISIONING PLAN — awaiting operator approval

| Field | Proposed value |
| --- | --- |
| Subscription / resource group / region | ECI-Development / rg-epolymind / spaincentral |
| Service / name | Azure Managed Redis (`Microsoft.Cache/redisEnterprise`) / `epolymind-redis-dev-970e5901` |
| Naming | 28 characters, legal letters/digits/single hyphens; within documented regional-name length constraint. Regional uniqueness is not reserved or guaranteed; stop on conflict rather than overwrite |
| SKU / release status / memory | Balanced_B0 / GA catalog candidate / approximately 0.5–1 GB class, published size discrepancy documented above |
| HA / clustering | Disabled for dev/test / EnterpriseCluster |
| TLS / protocol / port / database | Minimum TLS 1.2 / Encrypted / 10000 / default database, client DB 0 |
| Authentication | Explicit access-key authentication enabled, temporary Phase 16 choice; stop if policy disallows it; no Entra integration |
| Persistence / geo-replication / modules | None / none / none |
| Encryption / eviction | Microsoft-managed encryption / NoEviction, so capacity exhaustion is visible rather than silent history eviction |
| Public network | Disabled from creation; never enabled for troubleshooting |
| Endpoint | `pe-epolymind-redis-dev`, subresource `redisEnterprise`, in rg-epolymind |
| Endpoint VNet / subnet | `vnet-epolymind-private-dev` (`10.50.0.0/24`) / `snet-private-endpoints` (`10.50.0.0/27`) |
| DNS | `privatelink.redis.azure.net`, two non-registering VNet links and endpoint DNS zone group |
| Tags on supported new resources | Project=epolymind, Environment=dev, Workload=polymind, Purpose=phase16, ManagedBy=manual |

**Azure resources to CREATE:** one Redis cluster and its default database; one
VNet and subnet; one private endpoint and its managed NIC; one private DNS zone,
two VNet links, DNS zone group and service-managed record; two peering child
resources named `epolymind-private-to-aks` and `aks-to-epolymind-private`.

**Azure state/resources to MODIFY:** register Microsoft.Cache for the subscription;
add only the approved `aks-to-epolymind-private` peering child to
`aks-vnet-36185111` in its MC_ group. The reciprocal peering belongs to the new
VNet. No existing NSG, subnet, route, node pool, ACR, Foundry, ECI workload, AKS
configuration or resource-group tags will be changed. DNS linking references the
AKS VNet without changing its DHCP DNS configuration.

**Kubernetes resources to CREATE in Stage B:** namespace `polymind`; temporary
Secret `polymind-redis-phase16` containing only `redis-url`; two short-lived
validation pods and, if needed, a replacement failure-test pod (at most two
concurrent pods). Use the existing published PolyMind image, after verifying its
immutable reference. No application Deployment, Service, LoadBalancer or Helm
release is created. **Existing Kubernetes resources to MODIFY: none.** Recheck
namespace/Secret state before acting; never overwrite another object's data.
The temporary Secret is necessary because the final application Secret is not
yet populated with API/inference configuration. No missing values are fabricated.

Key retrieval is deferred until actually needed after provisioning. It must stay
in protected process memory, be URL-encoded, and be delivered to the temporary
Secret without command-line literals or output. No keys or Secret contents were
retrieved in Stage A. Do not emit raw credential-bearing errors.

### J5. Stage B validation, risks and cleanup boundaries

After the exact approval phrase, reconfirm subscription/group/context and absence
of duplicates; register the provider and stop on any permission/policy/capacity
denial. Provision only the approved SKU and topology. Record creation time and
sanitized properties; verify public access disabled, TLS, authentication mode,
clustering, endpoint approval and DNS group state before data-plane testing.

Bounded validation uses synthetic data and the pinned application image: normal
hostname DNS resolves privately, TCP 10000 connects, certificate/hostname-verified
TLS succeeds, authentication/PING succeeds, and one unique short-TTL key passes
SET/GET/compare/DEL. Then exercise Settings → create_memory_store → RedisMemoryStore
for readiness, empty session, append/read/order/trim/isolation/clear/close. Two pods
must independently write/read the same synthetic session in both directions.
This is shared-client evidence, not final application Deployment validation.
A separate pod-only invalid configuration should fail within a wall-clock budget
without local fallback or secret logging; do not interrupt Redis or rotate its key.

Known risks: non-HA/no-persistence data loss and downtime; access-key rotation
remains operational; B0 memory documentation discrepancy; allocation/quota/name
availability cannot be guaranteed by catalog discovery; peering grants private
reachability rather than per-workload isolation; policy/RBAC can still block writes.
NetworkPolicy enforcement is none and will remain so. If DNS, capacity, policy or
command compatibility fails, stop rather than enabling public access, disabling
TLS, expanding privileges, changing service mode, or spending on a larger SKU.

Normal cleanup deletes only exact synthetic keys/sessions, closes clients, and
removes validation pods and the temporary Secret. Keep the namespace and intended
Redis/private-network resources for subsequent Phase 16 work. **Redis remains
billable while provisioned**; no resource exists or incurs new Redis charges yet.
Never run FLUSHALL, FLUSHDB, KEYS *, a load test, or an unrelated-data scan.

Rollback is a separately confirmed decommission of only resources recorded as
created by this task: first remove test clients/Secret and decommission Redis,
then endpoint/NIC/DNS group, task-owned links/zone and the two named peerings,
then the new subnet/VNet when empty. Do not delete the AKS managed VNet or either
resource group, remove unrelated DNS records, unregister a shared provider, or
leave a service publicly reachable while dismantling its endpoint. On an incomplete
deployment, report exact residual/billable resources rather than silently deleting
the service intended for the next phase.

### J6. Stage A validation and status

No application/test/chart/dependency files changed. Only this report is appended;
historical sections are preserved. Local redis-py version check returned 6.4.0.
Compile with the requested `/tmp` bytecode cache, Compose validation, Helm lint
(one informational icon suggestion), and template rendering all exited 0.
The default rendered manifest is `/tmp/polymind-phase16-redis-rendered.yaml` and
contains no live credential values. Full pytest: **231 passed in 18.59s**, exit 0.
`git diff --check`: exit 0. Stage B must repeat relevant checks after its
operational work; Stage A results do not establish Redis readiness.

Azure resources created/modified: **NONE**. Kubernetes resources created/modified:
**NONE**. Redis DNS/TCP/TLS/PING/SET/GET/DEL/memory/two-pod validation: **NOT RUN**.
Secrets printed: **NO**. Public Redis exposure: **NO**. TLS bypass: **NO**.
Local fallback introduced: **NO**. Branch/commit/push: **NO**.

**Approval gate:** the operator must explicitly supply
`APPROVE REDIS PROVISIONING` before any Stage B mutation. This gate comes from
the current task prompt, not from an inferred repository rule. Phase 16's Chroma,
Prometheus/Adapter, actual application deployment and HPA calibration remain
separate work.

### J7. Interrupted-run recovery — 2026-10-05

The operator reported a usage-limit interruption. Recovery inspected the working
tree, complete report diff, saved discovery/pricing outputs and validation
results before continuing. The saved Stage A discovery and provisioning plan
were complete; the approval handoff remained pending. No explicit
`APPROVE REDIS PROVISIONING` occurs in the available session evidence.

A fresh read-only metadata check reconfirmed ECI-Development is Enabled and
rg-epolymind is Succeeded in Spain Central. Subscription inventories again returned
no Managed Redis resources, private endpoints or private DNS zones (therefore no
zone links to inspect). The only observed VNet remains aks-vnet-36185111, with no
peerings, unchanged subnet ranges/NSG associations, no subnet route-table
associations, and no custom VNet DNS. AKS remains Succeeded with Azure CNI Overlay,
the recorded pod/service CIDRs, load-balancer outbound and networkPolicy none.
Microsoft.Cache remains NotRegistered. Namespace metadata again contains only
the four default/system namespaces; no PolyMind namespace or task-created
validation resources exist. No credentials or Secret contents were retrieved.

| Recovered item | Classification |
| --- | --- |
| Stage A repository, CLI, service, network and pricing discovery | COMPLETE |
| Proposed design, cost estimate and saved local validation | COMPLETE |
| Operator approval handoff | PARTIAL — plan restored; explicit approval pending |
| Stage B provider registration, Redis and private-network creation | NOT STARTED |
| Kubernetes namespace, temporary Secret and validation pods | NOT STARTED |
| Redis DNS/TLS/data-plane/memory/two-pod validation | NOT STARTED |
| Actual B0 allocation, name reservation and usable memory | UNKNOWN until service-side validation |

Azure resources created or partially configured by this task: none. Kubernetes
resources created by this task: none. Only this report is modified on master;
application code is unchanged. Previously completed local checks were retained,
not rerun solely because execution resumed; the final report diff check was
rerun. No branch, commit or push occurred. The next safe operation is the operator
approval handoff for J4, not provisioning. Redis remains PARTIAL / NOT LIVE
VALIDATED; Phase 16 remains incomplete.

## K. Approved Azure Managed Redis provisioning and private validation — 2026-10-05

The operator explicitly supplied `APPROVE REDIS PROVISIONING` and authorized
Stage B exactly as planned, with an additional guardrail permitting only the
peering child on the AKS-managed VNet. Preflight reconfirmed subscription/group
and absence of duplicate resources. Microsoft.Cache registration was requested;
Azure Managed Redis `epolymind-redis-dev-970e5901` and its default database were
created in rg-epolymind, Spain Central. Both subsequently reported Succeeded /
Running. The resource was first timestamped after creation at
**2026-10-05T13:47:25Z**; this observation is not an exact billing-start timestamp.

Verified service metadata: Balanced_B0, highAvailability Disabled, minimum TLS
1.2, publicNetworkAccess Disabled, EnterpriseCluster, Encrypted client protocol,
port 10000, accessKeysAuthentication Enabled, NoEviction. Persistence, modules and
geo-replication were unset. The GA catalog evidence and approved retail estimate
remain those in J1/J3; no larger SKU or preview option was substituted.

The dedicated vnet-epolymind-private-dev and snet-private-endpoints were created,
then the two approved peering children. The managed-VNet guard initially stopped
on a nested ETag difference. A recursive comparison of before/after snapshots
proved that only the peering child and Azure-generated ETags changed; all other
properties, including nested subnet properties, were identical. No managed VNet,
subnet, route, NSG or address-space update was issued. Execution resumed only at
the uncompleted DNS/private-endpoint steps. An earlier read-only database-show
CLI argument mismatch was corrected before any network resource creation.

At this checkpoint private DNS linking is underway; live validation and cleanup
are pending. Redis is not yet READY. The provisioned service is billable and will
be retained for subsequent Phase 16 work. No application files have changed.

### K1. Completed private networking and guardrail verification

The checkpoint above was followed by successful completion of the approved
network plan. The private endpoint pe-epolymind-redis-dev is Succeeded, with its
Redis connection Approved. The endpoint uses snet-private-endpoints
(10.50.0.0/27) in vnet-epolymind-private-dev (10.50.0.0/24). The zone
privatelink.redis.azure.net contains the service-managed record; both
link-epolymind-aks and link-epolymind-private report Completed, with registration
disabled. Both peerings report Connected. Microsoft.Cache reports Registered.

The normal service hostname resolved from AKS into the approved private endpoint
subnet. The verified path is Azure CNI Overlay pod/node egress → reciprocal VNet
peering → private endpoint → Azure Managed Redis. CoreDNS configuration was not
modified. Public Redis access remained Disabled throughout. AKS NetworkPolicy
remains none: no Kubernetes NetworkPolicy enforcement claim is made.

A final read-only comparison again confirmed every AKS-managed VNet/subnet
property was unchanged apart from the approved peering child and Azure-generated
ETags. No AKS cluster/node-pool, existing subnet, address space, NSG or route
configuration was modified. No Foundry, ACR or unrelated ECI resource was changed.
There is one intended Redis instance and one intended private endpoint, with no
duplicate resources. The private DNS zone is global; regional resources are in
Spain Central, as planned.

### K2. Credential delivery and bounded live results

The active Kubernetes context was verified as epolymind-aks-dev before mutations;
all Kubernetes writes were limited to the approved PolyMind validation resources.
The polymind namespace was created. The final polymind-secrets Secret was absent;
no missing inference/API configuration was fabricated. Instead, the temporary
polymind-redis-phase16 Secret carried only the redis-url key.

The Redis access key was retrieved only into a protected subprocess pipe/process
memory, URL-encoded in memory, and sent to Kubernetes as Secret JSON over stdin.
No credential-bearing file, command argument, report text, rendered manifest or
log output was produced. No key was regenerated. The URI used the normal
certificate-valid service hostname, TLS port 10000 and DB 0. No Entra/token-refresh
code or Azure SDK dependency was added.

Two temporary pods used the existing published image at immutable digest
`sha256:bce37944a1785f4c56b4afa870e83bddbe9872c6953bacb470a7cce2ff1a5c9b`.
The initial image reference incorrectly assumed the registry's unqualified name
was its login-server hostname; Kubernetes reported image-pull DNS failures.
Read-only ACR metadata supplied the actual generated login-server hostname, and
only the two temporary pods' image references were corrected, retaining the same
digest. No AKS DNS, ACR or Azure networking change was made for this correction.
Both pods then became ready. Runtime redis-py was verified as **6.4.0**.

| Live check | Observed result |
| --- | --- |
| Normal Redis hostname resolution inside AKS | PASS; every resolved address in the approved private endpoint subnet |
| TCP 10000 | PASS |
| TLS/certificate/hostname verification | PASS; TLS 1.3 negotiated with normal certificate verification, no bypass |
| Access-key authentication and PING | PASS |
| Unique synthetic SET with short TTL, GET and value comparison | PASS |
| DEL exact probe key | PASS |
| Settings → create_memory_store → RedisMemoryStore | PASS; actual Redis provider selected |
| Memory PING readiness | ready |
| Empty synthetic session | PASS |
| Atomic append, ordered read and trimming | PASS; three exchanges trimmed to four ordered messages |
| TTL and session isolation | PASS; positive TTL bounded by configured 180 seconds; independent session empty |
| Clear exact session and client close | PASS |
| Pod A write → independent Pod B read | PASS |
| Pod B write → independent Pod A read | PASS; final exact session cleared |
| Isolated invalid configuration | PASS; pod-only loopback/closed-port TLS endpoint produced memory_unreachable |
| Bounded failure/no fallback/no credential logging | PASS; readiness plus read failure completed within 30 seconds, FileMemoryStore construction forbidden by the probe, no local memory file created, captured logs contained neither the real URI nor its password |

The synthetic direct probe key used a unique phase16 run prefix and a 120-second
TTL. Memory sessions used unique Phase 16 IDs, the existing hashed memory key
scheme and a 180-second TTL. Cleanup touched only those exact keys. No FLUSHALL,
FLUSHDB, KEYS *, scans, load tests, key rotation or service outage injection ran.
The failure case never targeted the live service and did not mutate Redis.
Probe errors were caught and bounded; raw exception bodies and tracebacks were
suppressed. Clients were closed after each operation group.

These checks exercise the real Redis memory factory/store without starting the
full application. Settings used local deployment validation mode solely to avoid
fabricating the other production dependency configuration; memory was explicitly
redis throughout. This is not a live application HTTP /ready test or final
multi-replica application Deployment proof. It does establish private shared
Redis access from two independent AKS pods using the pinned client.

### K3. Cleanup, retained resources and cost

Exact synthetic-key cleanup passed. Both validation pods and the temporary Redis
Secret were deleted, and final read-only checks confirmed their absence. The
polymind namespace is retained. No application Deployment, Service, LoadBalancer
or Helm release was created. The final application Secret still needs safe
completion during the actual deployment task.

The intended Redis instance/database, dedicated VNet/subnet, reciprocal peerings,
private endpoint/managed NIC, private DNS zone/links and zone group/record remain
for the next Phase 16 steps. **Azure Managed Redis remains billable while
provisioned.** No automatic deletion or scale-up occurred.

The approved 2026-10-05 public retail estimate in J3 remains USD 0.019/hour
(USD 13.87/month at 730 hours) for Redis, plus one private endpoint at USD
0.01/hour and a USD 0.50/month DNS zone: **approximately USD 21.67/month fixed**,
plus traffic/query charges and taxes. This is an estimate, not measured billing
or a subscription-discount quote. No HA, persistence, geo-replication, paid
monitoring, DNS resolver appliance or additional paid capacity was enabled.

### K4. Repository validation and final dependency status

No application code, tests, chart, dependency pin or architecture changed. Only
this report was appended; pre-existing report history is preserved.

| Validation | Result |
| --- | --- |
| Full pytest after live validation | 231 passed in 13.91s |
| Compile with requested /tmp bytecode cache | Exit 0 |
| docker compose config --quiet | Exit 0 |
| helm lint deployment/helm/polymind | Exit 0; informational icon recommendation only |
| helm template to /tmp/polymind-phase16-redis-rendered.yaml | Exit 0; no live credentials supplied |
| git diff --check | Exit 0 |
| Final managed-VNet and Kubernetes cleanup verification | PASS |

Self-review confirmed the credential existed only in process memory/Secret
delivery, temporary scripts contain no actual key/URI, no application fallback
was introduced, and no unrelated implementation/dependency changes occurred.
No branch was created; no commit or push occurred. Changes remain uncommitted.

**Redis is READY for the bounded Phase 16 dependency gate. Phase 16 remains
incomplete.** Remaining work includes Chroma, Prometheus/Adapter, actual
application configuration/deployment, full application readiness and two-replica
proof, and HPA calibration. Non-HA/no-persistence durability limitations, static
credential rotation, the unresolved published B0 usable-memory discrepancy and
lack of AKS NetworkPolicy enforcement remain recorded limitations.

The published validation image is tagged 036b847, whereas current master is
f9b47fd and also includes the intervening Foundry compatibility commit. The image
therefore predates the current source's Foundry/log-sanitization patches. Its
Redis factory/store contract passed; no streaming path was exercised. Before
actual application deployment, publish and select an image containing the current
validated source. This task did not rebuild, push or alter ACR content.


## L. Current-master image publication and AKS pull verification — 2026-10-05

### L1. Source, scope and clean build provenance

Published committed `master` at full SHA
`f9b47fda4658935b64826f1d4abe0488c64f21ae` (short SHA `f9b47fd`). A read-only
`git ls-remote origin refs/heads/master` returned that same full SHA. The only
starting working-tree modification was this report (466 existing added lines);
there were no runtime-relevant dirty or untracked files. All operator report
content was preserved byte-for-byte before this append.

The build used a temporary `/tmp` directory extracted entirely from
`git archive --format=tar <full-SHA>`, without a branch, checkout or worktree
mutation. All 171 archive files came from committed HEAD; the unchanged
`.dockerignore` excluded documentation, tests, data documents, caches and local
environment files from the Docker context. The only tracked environment sample
was `.env.example`; the Helm Secret file was a value-driven template, not a live
Kubernetes Secret. Archive inspection found no credential/cache directories,
actual `.env`, private-key files or private-key markers. No host Azure, Docker,
SSH, Git or Kubernetes authentication files were copied into the context.

The existing Dockerfile and CI production path were retained: Python 3.10 slim,
pinned CPU Torch and application requirements, revision-pinned model snapshots,
and non-root UID/GID 10001. No application, dependency, Dockerfile, chart or
entrypoint changes were made. The two existing AKS nodes both reported
`linux/amd64`, so the build explicitly selected that platform and reused normal
Docker cache. No cloud build or new build service was used.

### L2. Required pre-build validation

| Check | Actual result |
| --- | --- |
| `python -m pytest -q` | PASS: 231 passed in 19.73s |
| `PYTHONPYCACHEPREFIX=/tmp/polymind-phase16-image-pycache python -m compileall -q .` | PASS: exit 0 |
| `docker compose config --quiet` | PASS: exit 0 |
| `helm lint deployment/helm/polymind` | PASS: exit 0; informational icon recommendation only |
| `helm template polymind deployment/helm/polymind` | PASS: exit 0; rendered to `/tmp/polymind-phase16-current-master.yaml` |
| `git diff --check` before build | PASS: exit 0 |

All gates passed before the build. Docker initially reported a missing socket;
subsequent read-only diagnostics confirmed Docker Desktop was available, and the
retry succeeded. An inspection template was corrected to handle an absent
Entrypoint field. Neither issue required a source or infrastructure change.

### L3. Local image and registry publication

Azure metadata, rather than the resource name, supplied the registry hostname:
`epolymindacrdev-b7bxdheagnerb8ep.azurecr.io`. The active subscription was verified
as `ECI-Development`. The registry admin account was already disabled and remained
unchanged. Normal `az acr login` using existing Azure user authentication passed.
No admin credentials, new identity or role assignment were used.

| Image evidence | Result |
| --- | --- |
| Build | PASS; existing Dockerfile, normal cache, clean committed-HEAD context |
| Repository / version tag | `polymind-api:f9b47fd` |
| Platform | `linux/amd64` |
| Docker-reported local image size | 3,022,151,112 bytes |
| Local image/index ID | `sha256:f81886ebfec049bab446be0513d2ee0c987561272f605bdf4c0506de3e29746c` |
| Runtime configuration digest | `sha256:93aaefdfb4e9f36794481f65c003c56ed7c785e8611843bfa141235fa71d783f` |
| Configured user | `10001:10001` |
| Entrypoint / CMD | No explicit entrypoint; `uvicorn api.app:app --host 0.0.0.0 --port 8001` |
| Offline local smoke | PASS; exit 0, 60-second alarm, network disabled, read-only root filesystem |
| redis-py | Exactly `6.4.0` |
| Push | PASS; exactly one versioned tag |
| Registry manifest digest | `sha256:fcc9cac926f6527975b3128a8e145d30bbd5f8578e7739b4956764806999f9eb` |

The smoke imported `llm.openai_compatible`, `memory.provider_factory`,
`memory.memory_store` and `graph.streaming`. It also verified SHA-256 file hashes
against committed HEAD for all four modules, proving the artifact contains the
current Foundry-compatible provider and sanitized streaming memory-error code.
It checked redis-py 6.4.0 and effective UID 10001. Socket connection attempts were
forbidden by the smoke command; no Foundry, Redis or Chroma call was made and the
API was not started.

Docker built a local OCI index with an attestation. Publication used
`docker push --platform linux/amd64` to publish only the runtime platform manifest,
so the registry reference and Kubernetes imageID can be compared directly.
The local index ID therefore intentionally differs from the published runtime
manifest digest; the local attestation was not published. Read-only
`az acr manifest show-metadata` confirmed the new tag's digest, and
`docker manifest inspect --verbose` confirmed the registry manifest is
`linux/amd64`. ACR tags changed from only `036b847` to exactly `036b847` and
`f9b47fd`. No tag was overwritten, deleted or purged.

The immutable image reference for subsequent Phase 16 deployment work is:

```text
epolymindacrdev-b7bxdheagnerb8ep.azurecr.io/polymind-api@sha256:fcc9cac926f6527975b3128a8e145d30bbd5f8578e7739b4956764806999f9eb
```

This records exact committed-source provenance and the resulting immutable image;
it is not a claim of bit-for-bit future rebuild reproducibility, since the
unchanged Dockerfile uses a mutable Python base tag. This build resolved that
base to `sha256:c1aaf3d03e14944a039a1647e0b3f6f34c6bee517bac6ff380215ee099c4e808`.

### L4. AKS pull, smoke and cleanup

The active context was explicitly checked as `epolymind-aks-dev` before pod
creation and again before deletion; no context switch occurred. The `polymind`
namespace already existed. Exactly one pod, `polymind-image-verify-f9b47fd`, was
created there with the new image referenced by digest and `imagePullPolicy: Always`.
It used no application Secret, environment credentials or service-account token.
The pod had a 180-second active deadline, bounded resources, non-root execution,
a read-only root filesystem and a temporary `/tmp` volume. Its overridden Python
command ran the same bounded module/version/source-hash smoke as the local test.

| AKS evidence | Result |
| --- | --- |
| Node | `aks-agentpool-40344793-vmss000001` |
| Pull by digest and container startup | PASS |
| Pod phase / exit code | `Succeeded` / 0 |
| Source hashes, critical module imports, redis-py 6.4.0, UID 10001 | PASS |
| Kubernetes imageID | Same complete immutable reference shown in L3 |
| Expected ACR digest equals pulled imageID digest | YES; exact string comparison passed |
| Temporary pod deleted | YES; deletion completed and subsequent get with `--ignore-not-found` returned no object |
| Temporary clean build context removed | YES; absence verified |
| Locally built Docker image retained | YES |

### L5. Security, review and remaining gate

Secrets used in the build: **NO**. Credentials copied into the image: **NO**.
ACR admin enabled: **NO**. New Azure identities or roles: **NO**. Application
credentials/Secrets used: **NO**. No credential-bearing build argument, ENV,
label, mounted file or command literal was supplied. Existing authentication was
used only outside the build for ACR and Kubernetes operations.

Cloud mutations were limited to the one new ACR image tag and creation/deletion
of the single temporary verification pod. No Azure infrastructure was created or
modified. No Redis, Foundry, networking or AKS infrastructure settings changed.
No application Deployment, Service, HPA, Helm release or LoadBalancer was created.
No Chroma/BM25 or Prometheus work began.

Self-review and pre-commit review confirmed source/packaging stayed unchanged,
pre-existing report content was preserved, publication used the intended SHA,
the digest comparison passed, and cleanup completed. The only repository change
from this task is this report append. Final `git status`, `git diff --stat` and
`git diff --check` were run; the latter passed. No branch, staging, commit or Git
push occurred. All report changes remain uncommitted for operator review.

**The current-master immutable image is READY for later AKS deployment. Redis
remains READY on the previously recorded evidence; it was not contacted or
revalidated in this task. Phase 16 is NOT complete.** The next dependency step is
representative Chroma/BM25 setup and validation. Application deployment remains
subject to the remaining dependency and Secret/configuration gates.


## M. Representative Chroma/BM25 setup and validation — 2026-10-05

### M1. Result, source and scope

**READY FOR BOUNDED PHASE 16 DEPENDENCY GATE. Phase 16 remains incomplete.**
The real ingestion and retrieval implementations passed against shared Chroma
HTTP, including independently built BM25 snapshots in two AKS pods using the
current-master immutable image. This is validation-representative and explicitly
not production-durable.

Work stayed on `master`, HEAD `f9b47fda4658935b64826f1d4abe0488c64f21ae`.
Application code, requirements, Docker configuration and Helm chart changed: NO.
The existing report was already modified (613 added lines relative to HEAD);
its entire starting content was preserved byte-for-byte before this append.
No branch, staging, commit or Git push occurred.

Inspection covered AGENTS.md, README, requirements, settings/model inventory,
all requested vector/ingestion/BM25/retrieval/reranker modules, API readiness,
Compose, Helm values/documentation, Phase 10 fixtures, Phase 8F/8G reports and
this report's latest evidence. Tests confirmed deterministic ingestion IDs and
publication ordering, serving/admin separation, version gating and no fallback.
The source matches the requested architecture: local Chroma is development-only;
shared serving uses get_collection without creation/reset; administrative
publication follows successful chunks; BM25 is an immutable process-local startup
snapshot built from Chroma and checked against expected/published versions;
application readiness requires both vector and BM25 readiness. No compatibility
patch or new image was needed.

### M2. Preflight and retained topology

The active context was `epolymind-aks-dev`, explicitly verified before creation
and cleanup mutations. The task-specific AKS authorization superseded the
repository's default Kind-only mutation scope for these exact resources.
Read-only inspection found no application objects in `polymind`, no existing
`polymind-dependencies` namespace, and no Chroma Deployment, Service or PVC there.
Both AKS nodes were Ready, without memory/disk/PID pressure. Each advertised
3860m allocatable CPU and about 13.3 GiB allocatable memory; initial requested CPU
was 767m/695m and requested memory 892/676 MiB. This was a scheduling preflight,
not a capacity or headroom benchmark. AKS reported provisioning Succeeded and
networkPolicy none.

| Property | Retained configuration |
| --- | --- |
| Namespace | `polymind-dependencies` |
| Deployment / Service | `polymind-chroma-phase16` |
| Image | `chromadb/chroma:1.5.9` |
| Observed pulled image digest | `sha256:1e0b73a187a28757c572acba508c46f48c9e8b0acaf5c20e6d95cdedce1acdf6` |
| Replicas / ready replicas | 1 / 1 |
| Service | ClusterIP `10.0.137.240`, TCP 8000; no external IP |
| Shared DNS | `polymind-chroma-phase16.polymind-dependencies.svc.cluster.local` |
| Data volume | `emptyDir`, 2 GiB sizeLimit, mounted at `/data` |
| Resource requests | 250m CPU, 512 MiB memory, 256 MiB ephemeral storage |
| Resource limits | 1 CPU, 2 GiB memory, 3 GiB ephemeral storage |
| Readiness | HTTP `/api/v2/heartbeat`, 5-second interval, 3-second timeout |
| Deployment strategy | Recreate; no deliberate restart/replacement tested |

The image's bundled `/config.yaml` was inspected with networking disabled and
confirmed persist_path `/data`. CPU/memory bounds reuse the repository chart's
existing modest resource defaults; the Phase 10 fixture supplied the pinned
image/port and token-free dependency pattern. Chroma drops capabilities and
disallows privilege escalation; no service-account token is mounted. Namespace
and pod labels preserve the chart convention, including app.kubernetes.io/name
chroma. Chroma is operated separately from the application Helm release.

Local and both image-resident Python clients reported chromadb 1.5.9, matching
the repository pins. A supplementary assertion initially expected the server's
version endpoint to equal the image release and failed: it returns `1.0.0`.
This was investigated, not hidden or treated as a runtime upgrade: the official
[tagged 1.5.9 Rust server source](https://github.com/chroma-core/chroma/blob/1.5.9/rust/frontend/src/server.rs#L628)
hardcodes that response. Image tag/pulled digest and successful real client
operations establish the tested artifact/compatibility; the endpoint alone
cannot identify the release. The external probe assertion was corrected;
application code and server configuration were unchanged.

### M3. Corpus identity and publication

The following existing repository PDFs were copied into a temporary `/tmp`
working directory; originals were untouched. Total selected bytes: **8,675,717**.
The larger rag_using_llm.pdf was excluded. ai_notes.text was not renamed or
forced through an unsupported loader. No document body is included here.

| Selected source | Bytes | SHA-256 |
| --- | ---: | --- |
| `LangGraph_Documentation.pdf` | 4,242 | `f58575a163a9c6ba3decaee1af0fa16529f919a53a52e9b5e893f89f632bd40f` |
| `information_retrieval_augmented_generation.pdf` | 6,123,585 | `55b72095a74e43184c6e9ee0bde7fab80d3f2dade7b0a102d11d7f010c149ad6` |
| `original_rag_paper.pdf` | 885,323 | `23e3249e9a1e75418d82efecab0ea8c4d033b89c93742f63208d47ce01f21233` |
| `rag_survey.pdf` | 1,662,567 | `396a0fadeb4cd40f5c8ccc36b73a0815f6cb4d7f6bfa53b6c48c1f9aba7c7e02` |

Version derivation: sort repository-relative paths lexicographically; for each
file append its lowercase SHA-256, two ASCII spaces, repository-relative path,
and one LF. SHA-256 the concatenated UTF-8 manifest, take the first 12 lowercase
hexadecimal characters, and prefix `phase16-rag-`. Result:
**`phase16-rag-62f3e0a6f547`**. This satisfies the existing safe 1–64 character
identifier validation and identifies corpus inputs, not the application image.

The dedicated collection is **`phase16_knowledge`**. Pre-ingestion list_collections
was empty, so no existing or ambiguous collection was reused/reset. The real
rag.ingest.ingest_documents/get_vector_store_admin path ran from the temporary
working directory with the unchanged relative data/docs layout. Existing PDF
loader, 500-character chunking with 30-character overlap, pinned MiniLM embedding
and UUIDv5 IDs were used. A clean subprocess environment supplied chroma_http,
127.0.0.1:18016, SSL false, the collection and exact corpus version. It ran outside
the repository .env location with only PATH/HOME inherited and explicit task
variables; no Redis/Foundry/API credentials were supplied. The revision-pinned
local embedding cache was used with offline flags, without model download.

The temporary kubectl forward bound only 127.0.0.1:18016. Sandbox restrictions
initially prevented Azure cache access and local ingestion connectivity; the
execution approval mechanism allowed the same scoped commands outside the
sandbox. No credential files were copied and no alternate public endpoint used.

Publication PASS: **4 source files, 1,058 chunks/vectors, 127.561 seconds**.
Per-file chunk counts were LangGraph 5, information_retrieval_augmented_generation
669, original_rag_paper 150, and rag_survey 234. Every retrieved record had a
selected source filename, non-negative integer chunk_id, .pdf file_type and
chunk_length equal to actual content length, bounded at 500. Collection metadata
was exactly `{polymind_corpus_version: phase16-rag-62f3e0a6f547}`. Heartbeat,
collection readiness and non-empty count passed. No other collection changed.

Idempotence PASS used one exact existing chunk/ID/embedding/metadata upsert through
the real admin adapter and verified the count stayed 1,058, supplemented by the
automated deterministic-ID test. A complete second embedding/ingestion pass was
not run because the bounded probe covered upsert convergence without repeating
all 1,058 embedding calls. The timing is diagnostic, not production throughput.

### M4. Two independent AKS clients and retrieval evidence

Pods `polymind-chroma-phase16-a` and `polymind-chroma-phase16-b` used exactly:

```text
epolymindacrdev-b7bxdheagnerb8ep.azurecr.io/polymind-api@sha256:fcc9cac926f6527975b3128a8e145d30bbd5f8578e7739b4956764806999f9eb
```

Both pulled imageIDs matched that digest and both Succeeded with exit 0. Pod A
ran on node suffix 000000; Pod B ran on 000001. Each used UID/GID 10001, read-only
root filesystem, dropped capabilities, no privilege escalation, runtime-default
seccomp, no service-account token, a 256 MiB /tmp emptyDir, 300-second active
deadline and 240-second Python alarm. Each requested 250m CPU/512 MiB memory and
was limited to 1 CPU/2 GiB memory/512 MiB ephemeral storage. No application
Deployment or shared BM25 filesystem artifact was created.

Both explicitly selected chroma_http, the shared Service DNS, TCP 8000, SSL false,
the dedicated collection/version, MODEL_OFFLINE_MODE=true and
MODEL_ARTIFACT_DIR=/opt/polymind/models. Settings used local deployment validation
mode only to avoid fabricating unrelated production credentials; the vector
provider remained shared HTTP. HF/Transformers offline flags were also set.

The actual Settings → create_vector_store → ChromaVectorStore path passed in
both pods. Guard functions rejected attempted local-client construction or
serving collection creation/deletion; HTTP reads, embeddings, retrieval and
reranking were real, not mocked. Both opened the existing collection, passed
heartbeat/readiness, listed 1,058 records, and built independent BM25 snapshots.
Expected, published and loaded versions all equaled phase16-rag-62f3e0a6f547.
BM25 build/readiness/search PASS in both; snapshot count 1,058 each.

| Query topic | Dense top source/chunk, both pods | BM25 top source/chunk, both pods | Reranked top, both pods |
| --- | --- | --- | --- |
| Retrieval augmented generation for knowledge intensive NLP tasks | original_rag_paper.pdf / 0 | rag_survey.pdf / 1 | original_rag_paper.pdf / 0 |
| Dense and sparse retrieval | rag_survey.pdf / 84 | rag_survey.pdf / 84 | rag_survey.pdf / 84 |
| LangGraph graph orchestration | LangGraph_Documentation.pdf / 0 | LangGraph_Documentation.pdf / 0 | LangGraph_Documentation.pdf / 0 |

Corpus extraction confirmed the relevant terminology before query selection.
The existing retrieve, bm25_search, hybrid_retrieve and rerank functions produced
non-empty results with valid selected-source/chunk identities for all three
queries. RRF scores and finite cross-encoder scores were present. Top identities
matched across both pods for dense, sparse, hybrid and reranked results. This is
bounded relevance evidence, not a broad retrieval-quality evaluation.

Both used baked /opt/polymind/models/embedding and /opt/polymind/models/reranker
artifacts with local_files_only enabled. Offline artifact use YES; runtime model
download NO; Foundry/generation call NO. A canonical content fingerprint over
sorted source/chunk/document-hash tuples matched between pods and a final local
read: `05fe45281965cb2fb10ce2a66986db0f3bf91b651c177bff88c0ed353083da3c`.
No transactional consistency beyond these observations is claimed.

Diagnostic BM25 build durations were 0.113s (A) and 0.089s (B). Initial dense
queries, including lazy model load, took 5.428s/4.366s; subsequent dense queries
were 0.014–0.024s and sparse queries 0.001–0.003s. These are single-operation
observations, not load tests, percentiles, capacity/headroom or HPA guidance.

### M5. Negative checks and cleanup

Each pod launched an isolated subprocess with expected version
phase16-intentionally-stale. Real build_bm25 raised BM25SnapshotUnavailable;
readiness was false/bm25_uninitialized because the rejected startup never loaded
a snapshot. Valid-version readiness was reconfirmed in the parent afterwards.
No Chroma version metadata was modified and no corpus was reset.

Each also tested chroma_http against its own loopback closed port 9, with an outer
20-second alarm. Actual check_vector_store_readiness returned sanitized
vector_unreachable in 0.113s (A) and 0.096s (B). Local-client construction guards
were never reached, no ./chroma_db directory appeared, and captured output had
no traceback. No real-service outage was injected. Final version, count and
content fingerprint remained unchanged. Application /health semantics were not
modified or represented as a full live API health test.

Both temporary pods were deleted and a final polymind pod listing was empty.
Negative subprocesses ended with their parent pods. The exact temporary
port-forward process was stopped. Temporary corpus copies, helper scripts,
manifests, logs, rendered Helm YAML and compile cache were removed after report
preparation; no source corpus or retained Chroma data was deleted. Namespace,
Chroma Deployment, ClusterIP Service and published collection/version remain
for subsequent Phase 16 work. Final retained-service checks found one healthy
replica with zero restarts. No restart/rescheduling recovery test was performed.

### M6. Security and durability boundary

| Boundary | Result |
| --- | --- |
| Public Chroma exposure / public DNS | NO |
| NodePort / LoadBalancer / Ingress | NO / NO / NO |
| New Azure infrastructure | NO |
| PVC / Azure Disk / paid storage provisioned | NO |
| Foundry/Redis/API credentials used in ingestion or probes | NO |
| New application Secret | NO |
| NetworkPolicy enforcement claimed | NO; AKS networkPolicy remains none |
| Internal transport | Plain HTTP, unauthenticated, ClusterIP reachability |

Existing operator Azure/Kubernetes authentication was needed for control-plane
operations; “no credentials” refers to application/dependency credentials, not
anonymous AKS administration. No Foundry, Redis, ACR or AKS network configuration
changed. No Prometheus, Adapter, HPA, application Deployment or Azure resource was
created. The current meaningful boundary is cluster-internal Service reachability;
this is not the final production authentication/TLS posture.

The emptyDir corpus can be lost on Chroma pod replacement. Chroma HA, durable
restart recovery, rescheduling recovery, backups/restore and production vector
capacity remain unproven. Do not roll/recreate this dependency assuming retained
corpus durability. Later operators must resolve persistence separately.

### M7. Repository validation, review and remaining sequence

| Validation | Actual result |
| --- | --- |
| python -m pytest -q | 231 passed in 14.24s |
| Compile with /tmp/polymind-phase16-chroma-pycache | Exit 0 |
| docker compose config --quiet | Exit 0 |
| helm lint deployment/helm/polymind | Exit 0; informational icon recommendation only |
| helm template polymind deployment/helm/polymind | Exit 0; default placeholders, no live values or credentials injected |
| git diff --check | Exit 0 |

Self-review checked source/image provenance, real retrieval calls, independent
snapshots, deterministic identities, failure paths, collection non-mutation,
offline artifacts and bounded resources. The only corrected probe issue was the
supplementary server-version assumption described in M2. No application defect
requiring a compatibility patch was found. Pre-commit review found no runtime
source/dependency/chart edits, secrets, document bodies, generated artifacts or
unrelated additions. All historical report content remains intact; only this
section was appended. Changes are uncommitted for operator review.

Foundry READY, Redis READY and current-master image READY retain their earlier
recorded evidence; Foundry and Redis were not revalidated here. Chroma/BM25 is now
READY FOR BOUNDED PHASE 16 DEPENDENCY GATE. **Phase 16 complete: NO.**
The remaining sequence, not started in this task, is:

1. Prometheus plus Prometheus Adapter/custom-metrics setup.
2. Prepare final application configuration and Secret safely.
3. Deploy exactly two fixed PolyMind replicas with autoscaling disabled.
4. Validate full application /health and /ready.
5. Prove shared Redis, shared Chroma and independent BM25 across actual replicas.
6. Establish the monitoring/custom-metric path.
7. Only then perform bounded HPA/capacity calibration.

## N. Prometheus + Adapter/custom-metrics setup — 2026-10-06

### N1. Outcome and source provenance

**PARTIAL — stopped at the explicit adapter-render RBAC gate before any Kubernetes
mutation. Monitoring is NOT READY FOR ACTUAL APPLICATION INTEGRATION.** Neither
Prometheus nor Adapter was installed. This is a preflight/offline-validation
result, not a failed live pipeline test and not completion of Phase 16.

Branch remained `master`; full HEAD was
`f9b47fda4658935b64826f1d4abe0488c64f21ae` (short `f9b47fd`), matching the source
represented by the supplied immutable image. Initial status had only this report
modified: 877 existing added lines relative to HEAD. No runtime, application,
monitoring, chart, dependency or configuration source was dirty. Application code
changed: NO. Monitoring contract changed: NO. Adapter mapping changed: NO.
No branch, commit, push, reset, staging or history operation occurred.

Before appending, all 184,501 bytes of the existing report were preserved and
compared with a temporary baseline. Its SHA-256 was
`e7551429561329672d706daae693b3e4a0b0c10d3343efc798c1f1b323d3b7f9`.
The final prefix comparison passed; prior content was not rewritten.

Inspection covered AGENTS.md, relevant README and observability guidance,
llm.metrics, API metric/query/stream integration, canonical rules/tests/mapping,
Phase 14/15 fixtures and reports, Helm deployment/HPA/defaults, monitoring and
Helm contract tests, and the latest Phase 16 Chroma/BM25 evidence. The canonical
contract remains:

```text
active_application_requests{operation="query"}
  -> polymind:active_query_requests:sum_by_pod
  -> pods/polymind_active_query_requests
```

The rule retains namespace/pod labels and its `up == 1` guard, with no blanket
zero fill. Stream requests remain separate. Fresh registries eagerly initialize
query and stream zeros. HPA remains disabled by default and uses Pods/AverageValue
when explicitly enabled. No live HPA was created.

### N2. Fresh cluster preflight

Current context was exactly `epolymind-aks-dev`. Both nodes were Ready on v1.35.7.
Namespaces, pods, Deployments, Services, HPAs, APIServices, ClusterRole and
ClusterRoleBinding names, and Helm releases were inspected. There was no
monitoring namespace, Prometheus/Adapter Deployment or release, or custom-metrics
APIService. Existing `system:prometheus` RBAC is AKS-managed and was left untouched;
it is not a PolyMind collector installation.

The only non-system workload was the retained healthy Chroma Deployment in
polymind-dependencies. The polymind namespace had no pods, Deployments or HPAs.
Helm listed only the AKS-managed overlay and workload-identity releases.
Metrics Server had two Ready pods, zero restarts, and
`v1beta1.metrics.k8s.io` Available=True. `kubectl top nodes` succeeded (143m/115m
CPU and 1,365Mi/1,394Mi memory at that observation); these are diagnostic samples,
not capacity/headroom evidence. Final Metrics Server conditions still reported
Available=True, reason Passed, message "all checks passed".

Initial sandbox reads could not use Azure CLI's session cache; the normal
execution approval mechanism enabled the same scoped commands. No credential
cache was copied, no application credential was supplied, and no Secret was read.

### N3. Prometheus preparation and offline validation

A temporary AKS manifest was derived from the existing Phase 14 fixture. It was
validated but never applied. Planned resources were monitoring namespace,
polymind-prometheus ServiceAccount, pod-only get/list/watch Role and RoleBinding
in polymind, two monitoring ConfigMaps, one Deployment and one ClusterIP Service.
The cross-namespace RoleBinding subjects the monitoring ServiceAccount; no
Prometheus ClusterRole or broader discovery access was proposed.

The configuration discovers annotated pods only in polymind. It preserves path,
port, scrape-enabled and namespace/pod relabeling. The old Kind fixture did not
contain scheme relabeling; the temporary adaptation adds the requested
prometheus.io/scheme mapping with an http/https match. Global scrape/evaluation
intervals remain 5s. The unchanged canonical recording group explicitly has a
30s interval, which overrides global evaluation for that group; it was preserved.
The rule ConfigMap copied the complete repository file directly, including all
15 recording/candidate-alert rules. Candidate alerts are not a deployed alerting
service; no Alertmanager or kube-state-metrics was installed.

| Prepared setting (not deployed) | Value |
| --- | --- |
| Namespace / name | monitoring / polymind-prometheus |
| Repository-pinned image | prom/prometheus:v3.5.5 |
| Replicas | 1 |
| Service | ClusterIP, TCP 9090 |
| Retention / storage | 1h / emptyDir, sizeLimit 512Mi |
| Requests / limits | 50m CPU, 128Mi / 500m CPU, 512Mi |
| Security | UID/GID/fsGroup 65534, non-root, RuntimeDefault, no privilege escalation, ALL capabilities dropped |
| Pod name label | app.kubernetes.io/name: prometheus |
| Rules ConfigMap | polymind-prometheus-rules, exact canonical file |
| Config ConfigMap | polymind-prometheus-config, temporary AKS adaptation |

No suitable local promtool was found. The pinned Docker image ran `check config`
with the exact temporary config and canonical rules mounted at their deployment
paths: SUCCESS. Separate `check rules`: SUCCESS, 15 rules. Existing `test rules`
ran from the correct mounted working directory: SUCCESS. No rule was changed.
There is no deployed Prometheus image digest, readiness, endpoint or target result.

### N4. Exact chart render and blocking RBAC finding

Chart `prometheus-community/prometheus-adapter` version **5.3.0** was obtained
successfully from the official chart repository and rendered from that local
package. Package SHA-256:
`aa6752b6207ed788522714c3ef7f67f27d423eb4d9512fecb52dc641b6434f31`.
No newer chart was substituted. `helm show values` confirmed the actual keys.
The temporary overlay contained only Prometheus URL/port, replicas and resources;
the canonical repository mapping supplied the sole custom rule.

Resolved image: `registry.k8s.io/prometheus-adapter/prometheus-adapter:v0.12.0`.
Planned release: polymind-prometheus-adapter in monitoring, one replica, requests
50m CPU/64Mi and limits 250m CPU/256Mi. Rendered Prometheus URL:
`http://polymind-prometheus.monitoring.svc:9090`. The chart default
`metricsRelistInterval: 1m` was retained, not shortened or production-tuned.

Every rendered object was reviewed:

| Scope | Objects |
| --- | --- |
| monitoring | ServiceAccount, ConfigMap, ClusterIP Service (443 to 6443), Deployment, all named polymind-prometheus-adapter |
| ClusterRole | prometheus-adapter-resource-reader; prometheus-adapter-server-resources |
| ClusterRoleBinding | prometheus-adapter-system-auth-delegator; prometheus-adapter-resource-reader; prometheus-adapter-hpa-controller |
| kube-system RoleBinding | prometheus-adapter-auth-reader |
| APIService | v1beta1.custom.metrics.k8s.io |

The **blocking** rendered ClusterRole `prometheus-adapter-server-resources` grants:

```yaml
apiGroups: [custom.metrics.k8s.io]
resources: ['*']
verbs: ['*']
```

Its chart-created binding targets the adapter ServiceAccount. This is confined
to the custom-metrics group: it is not cluster-admin and does not grant mutation
of core pods/nodes/Secrets. Nevertheless wildcard verbs authorize mutation verbs
in that API group, contrary to task section 13's explicit no-wildcard-mutation
render gate. The chart template hardcodes `verbs: ["*"]`; its supported
`rbac.customMetrics.resources` value can narrow resources but cannot narrow verbs.
Installation was therefore stopped as instructed, before either stack component
was applied. No task-created broken APIService needs rollback.

Other rendered permissions were read-only get/list/watch on namespaces, pods,
services and ConfigMaps cluster-wide; delegated authentication through the
existing system:auth-delegator role (create tokenreviews and subjectaccessreviews);
and the existing kube-system extension-apiserver-authentication-reader Role.
The live latter Role permits get/list/watch only of the named
extension-apiserver-authentication ConfigMap. No application Secret read, node
mutation, namespace deletion or Azure permission was rendered. No new Role,
CRD, cert-manager controller, certificate Secret or Helm hook was rendered.
Effective post-install permissions and ServiceAccount impersonation checks are
not available because the accounts were never created.

Default certificate handling renders `/tmp/cert` for adapter-generated serving
material on emptyDir and `insecureSkipTLSVerify: true` in the APIService. This is
the chart's validation default, not certificate-verified aggregation TLS. No TLS
or availability test was performed. The initial offline Helm capability set chose
apiregistration.k8s.io/v1beta1; re-rendering with the cluster's observed
apiregistration.k8s.io/v1 capability correctly emitted the v1 APIService object.
Its served custom-metrics group version remains v1beta1. That render adjustment
does not resolve the independent wildcard RBAC blocker.

A concrete follow-up option is a reviewed temporary Helm post-renderer that
narrows this one ClusterRole to read verbs and the intended custom metric resource,
while retaining the exact chart package and canonical mapping. It would require
explicit scope resolution because this task said to stop on this finding and
allowed only environment-operational values in the temporary overlay. No
post-renderer, patched chart or permanent AKS profile was introduced here.

### N5. Live metric gates, security and cleanup

No metric probe pods, runner ConfigMap, temporary Service or port-forward were
created. The supplied immutable image remains
`epolymindacrdev-b7bxdheagnerb8ep.azurecr.io/polymind-api@sha256:fcc9cac926f6527975b3128a8e145d30bbd5f8578e7739b4956764806999f9eb`,
but was NOT launched in this task. Real llm.metrics registry use, two UP targets,
raw/recorded A=1/B=0, adapter discovery, wildcard/individual queries, A=0/B=0
return, and live missing-target behavior are all **NOT RUN**, not PASS. Source
inspection confirms the intended zero/stream/up-guard semantics only.

Public exposure NO; application credentials used NO; Azure resources created NO;
PVC/Azure Disk/paid storage created NO; AKS networking/node pools changed NO;
NetworkPolicy enforcement claimed NO. The prior report records networkPolicy
none; no fresh Azure network-setting query or policy change was performed.
Foundry, Redis, Chroma data/corpus and ACR content were untouched.

Final polymind resource listing was empty and monitoring namespace was absent.
There are no task-created probes, ConfigMaps, forwards, collector, adapter, or
APIService to remove or retain. The temporary downloaded chart, overlay, rendered
manifests, config, local report baseline and compile cache were removed after
recording evidence and checking report-prefix preservation. No unrelated
resources or files were deleted. Prometheus retained: NO; Adapter retained: NO.

### N6. Validation, review and readiness

| Validation | Actual result |
| --- | --- |
| Pinned promtool check config | PASS, exact temporary config and canonical rules |
| Pinned promtool check rules | PASS, 15 rules |
| Pinned promtool test rules | PASS |
| python -m pytest -q | 231 passed in 14.92s |
| Monitoring + Helm contract tests | 17 passed in 1.01s |
| PYTHONPYCACHEPREFIX=/tmp/polymind-phase16-monitoring-pycache python -m compileall -q . | Exit 0 |
| docker compose config --quiet | Exit 0 |
| helm lint deployment/helm/polymind | Exit 0, 1 chart, informational icon recommendation |
| helm template polymind deployment/helm/polymind | Exit 0, no live credentials |
| Adapter local render with observed v1 APIService capability | Exit 0; RBAC policy gate FAIL as explained above |
| git diff --check | Exit 0 |

Self-review distinguished offline configuration correctness from live readiness,
identified the chart wildcard grant and group-specific 30s evaluation interval,
and verified no metric/API contract changed. Pre-commit review checked the report
append and repository status: no application sources, credentials, generated
manifests, dependency additions or unrelated edits were introduced. The only
repository change is this appended report section, on top of its pre-existing
operator content. It remains uncommitted for review.

Foundry READY, Redis READY, immutable image READY and Chroma/BM25 READY refer to
prior Phase 16 evidence and were not revalidated here. Monitoring infrastructure:
**PARTIAL / BLOCKED AT RENDER REVIEW**. Actual application deployed NO; HPA enabled
NO; calibration performed NO; Phase 16 complete NO. The immediate next step is
resolution of the adapter RBAC render gate and completion of this monitoring task.
Final application configuration + Secret preparation remains the next planned
Phase 16 task only after monitoring reaches READY FOR ACTUAL APPLICATION
INTEGRATION. Actual two-replica scraping/custom-metric validation remains pending;
no claim of ACTUAL POLYMIND METRIC PATH FULLY VALIDATED is made.

### N7. Focused Adapter RBAC-resolution continuation — 2026-10-06

**RESOLVED — SAFE TO CONTINUE MONITORING INSTALLATION**, in a separate authorized
task. This decision resolves the local render/RBAC gate only. Installation remained
explicitly unauthorized, and no Kubernetes or Azure mutation occurred. No live
adapter, aggregation, metric-probe or HPA test was performed in this continuation.

The operator explicitly authorized the temporary post-renderer, exact-chart
reproduction, analysis, local validation and report append. Branch remained
`master`, HEAD `f9b47fda4658935b64826f1d4abe0488c64f21ae`. Only this report was dirty
on entry (1,103 existing added lines versus HEAD); all application, runtime,
monitoring and Helm source files were clean. The pre-append baseline contained
197,605 bytes, SHA-256
`eb4527d66edccf13559c4f5cfe2d2fb0b5a7aa9ca5a083d1ce9a14b029bfea51`.
All those bytes were preserved exactly, including section N's historical stop.

**Chart and reproduced binding.** The official repository supplied chart
prometheus-adapter **5.3.0** again. Its package SHA-256 exactly matched:
`aa6752b6207ed788522714c3ef7f67f27d423eb4d9512fecb52dc641b6434f31`.
The upstream package was never patched or vendored. The canonical PolyMind mapping
was merged with a temporary operational overlay: Prometheus URL
`http://polymind-prometheus.monitoring.svc`, port 9090, one replica, requests
50m CPU/64Mi, limits 250m CPU/256Mi. The verified chart default relist interval
remained 1m. Both renders explicitly supplied apiregistration.k8s.io/v1 capability.
Image remained `registry.k8s.io/prometheus-adapter/prometheus-adapter:v0.12.0`.

Actual packaged templates, rather than binding names alone, established:

- ClusterRole `prometheus-adapter-server-resources` contains one rule:
  apiGroups `[custom.metrics.k8s.io]`, resources `['*']`, verbs `['*']`.
- ClusterRoleBinding `prometheus-adapter-hpa-controller` references that role and
  binds ServiceAccount `monitoring/polymind-prometheus-adapter`.
- Both templates are conditional on rbac.create and custom/default metric rules.
  The chart provides a generic custom-metric API access grant when such rules are
  enabled; its README describes serving metrics for HPA consumers but gives no
  technical justification for wildcard verbs. The binding's name is misleading:
  it does not bind the kube-controller-manager or an HPA controller ServiceAccount.

This is a metric-consumer permission granted to the adapter identity, not the
permission that allows an aggregation server to publish an APIService or perform
delegated authentication. Serving a metric does not intrinsically require the
server identity to read its own custom-metric endpoint. Keeping a narrowly scoped
read grant preserves the chart object/binding under the authorized one-rule scope;
we do not claim that self-read is an indispensable server permission. Future
clients/HPA identities need their own authorization; this binding grants them
nothing. No such identities or bindings were modified here.

**Least-privilege analysis.** The hardened target rule is:

```yaml
apiGroups:
  - custom.metrics.k8s.io
resources:
  - pods/polymind_active_query_requests
verbs:
  - get
```

The exact [Adapter v0.12.0 dependency manifest](https://github.com/kubernetes-sigs/prometheus-adapter/blob/v0.12.0/go.mod)
pins custom-metrics-apiserver v1.30.0 and apiserver v0.30.0. Its
[custom metric route installer](https://github.com/kubernetes-sigs/custom-metrics-apiserver/blob/v1.30.0/pkg/apiserver/installer/cmhandlers.go)
registers GET on `namespaces/{namespace}/{resource}/{name}/{subresource}`.
The [storage handler](https://github.com/kubernetes-sigs/custom-metrics-apiserver/blob/v1.30.0/pkg/registry/custom_metrics/reststorage.go)
selects individual versus wildcard retrieval internally. The HTTP response may
be MetricValueList, and the internal handler is named List; neither determines
the RBAC verb.

The inspected [adapter-side request parser](https://github.com/kubernetes/apiserver/blob/v0.30.0/pkg/endpoints/request/requestinfo.go)
and [Kubernetes 1.35 request parser](https://github.com/kubernetes/kubernetes/blob/v1.35.0/staging/src/k8s.io/apiserver/pkg/endpoints/request/requestinfo.go)
assign GET requests verb get, extract resource/name/subresource, and convert to
list/watch only when the name is absent. Both an individual pod name and literal
`*` occupy that name slot. Thus both intended pod-metric query forms authorize
as get on resource pods, subresource polymind_active_query_requests. Label
selectors do not change this. The [RBAC authorizer](https://github.com/kubernetes/kubernetes/blob/v1.35.0/plugin/pkg/auth/authorizer/rbac/rbac.go)
combines resource/subresource, and its [resource matcher](https://github.com/kubernetes/kubernetes/blob/v1.35.0/pkg/apis/rbac/v1/evaluation_helpers.go)
accepts an exact match. The slash-separated resource above is valid; dynamic pod
names do not require resources `*`. No resourceNames restriction is added, so
both individual and wildcard names remain usable. This ClusterRole grant remains
cluster-scoped; namespace-scoping its binding would exceed the one-rule task.

| Verb in this custom-metrics rule | Required for the intended queries? |
| --- | --- |
| get | YES, individual and wildcard pod-metric GET routes |
| list | NO, wildcard occupies the name segment; this is not a nameless collection request |
| watch | NO, not part of the supported metric query contract |
| create, update, patch, delete, deletecollection | NO, no metric mutation route is needed |

API discovery is separate non-resource authorization, not list on the metric.
The existing Phase 15 report proves the original chart's broader configuration
worked in Kind; it does not prove wildcard/list/watch rights are necessary or
constitute live evidence for this new narrowed rule. The technical sufficiency
conclusion here is source-based, backed by local manifest tests, not a live SAR
or a newly deployed API test.

**Post-renderer and exact diff.** The executable Python post-renderer existed only
under `/tmp/polymind-phase16-rbac/`, using already-installed PyYAML. It parsed the
complete input with duplicate-key rejection, rejected YAML aliases, required
exactly one target ClusterRole with the expected API version and one exact
original rule, and rejected unexpected top-level/RBAC fields. It used YAML node
source offsets to replace only the resources and verbs scalar values. Before
emitting any stdout, it reparsed the result and compared against a deep copy
with only those two intended fields changed. Errors return nonzero with empty
stdout. Zero/duplicate targets, wrong kind/version/group/resource/verbs, extra
rules/keys, aggregation rules, duplicate keys, aliases, already-hardened input and
malformed YAML were exercised as rejection cases. It deliberately rejects a
second hardening pass rather than silently accepting unexpected input.

Helm rendered both original and hardened YAML from the same exact package and
values. Of **11 objects**, **one** changed, at `rules[0].resources[0]` and
`rules[0].verbs[0]`. Unified diff showed only `'*'` to the exact metric resource
and `"*"` to `"get"`. A byte comparison proved the entire output was identical
apart from those two replacements. Deployment, Service, ServiceAccount,
ConfigMap/mapping, APIService/TLS settings, Prometheus URL, image, resources,
all other roles and every binding were unchanged. No unexpected differences.

Evidence SHA-256 values, before required temporary cleanup:

| Artifact | SHA-256 |
| --- | --- |
| Original render | `0a31142420a4a72c95ab6db4802f4a98ec059f4f4d2ea8edea3e6425c2e2b2aa` |
| Hardened render | `efc58a7da6ae1917275e83a5ee24b0b7c2d75796ec41612cfde79fcbef289d7d` |
| Temporary post-renderer | `8cf730e8e155556662e6e2f581161f3fe1a2d6c724c43dff54033bb2c0a51d30` |
| Temporary policy tests | `43790a9dc5a3aee3fc9c01a3d0d2d003900547242b60d2e00fc02da5346e77ca` |

**Complete RBAC/security review.** The target rule has no wildcard resources,
wildcard verbs or mutation verbs. The other rendered ClusterRole retains
get/list/watch on the explicit core resources namespaces, pods, services and
ConfigMaps; it does not include Secrets. There is no cluster-admin binding,
wildcard core-resource grant, Pod/Node/Namespace/Deployment mutation, or
Azure/cloud permission. These conclusions concern this render and its identified
role references, not an audit of every pre-existing cluster binding.

The unchanged system:auth-delegator binding allows create of TokenReview and
SubjectAccessReview requests. Those are expected delegated authentication and
authorization checks, distinct from metric or workload mutation. The unchanged
kube-system RoleBinding references extension-apiserver-authentication-reader for
reads of the named authentication ConfigMap, as inspected in N4. This follows the
[Kubernetes aggregation authorization model](https://kubernetes.io/docs/tasks/extend-kubernetes/configure-aggregation-layer/).
No broad mutation grant was added. Chart-default insecureSkipTLSVerify remains
unchanged, as already documented in N4; this continuation does not claim verified
serving-certificate TLS. No Secret contents or application credentials were used.

**Validation and review.** No new dependencies were installed. Temporary policy
tests verified target uniqueness/exact rule, all other objects unchanged, no
mutation/wildcard verbs, canonical metric mapping, APIService identity/version,
image, interval, URL, resources and binding subject, plus 14 fail-closed cases.

| Check | Actual result |
| --- | --- |
| Exact chart checksum | MATCH |
| Original + post-rendered Helm templates | PASS |
| Temporary static policy/failure tests | 16 passed in 1.58s |
| python -m pytest -q | 231 passed in 13.90s |
| pytest -q tests/unit/test_monitoring_contract.py tests/unit/test_helm_chart.py | 17 passed in 1.08s |
| Compile using /tmp/polymind-phase16-rbac-pycache | Exit 0 |
| docker compose config --quiet | Exit 0 |
| helm lint deployment/helm/polymind | Exit 0; 1 chart, icon recommendation only |
| helm template polymind deployment/helm/polymind | Exit 0, no live credentials |
| git diff --check | Exit 0 |

No client/server Kubernetes dry-run or live authorization request was necessary.
No kubectl, Helm install/upgrade, Azure mutation, probe or application deployment
was executed. Self-review checked the GET-versus-List distinction, binding subject,
remaining delegated-auth permissions, failure behavior and complete diff.
Pre-commit review confirmed only a report append, preserved prior bytes, no
source/contract change, credentials, vendored chart or generated repo artifacts.

After recording this evidence, the downloaded chart, overlay, post-renderer,
original/hardened YAML, temporary tests/source downloads, report baseline, compile
cache and application render were removed from /tmp. No repository file was
deleted. No branch, commit or push occurred; the report remains uncommitted.

**Next:** resume the full Prometheus + Adapter setup and live metric validation
in a separate Codex task, recreating and verifying this narrowly scoped
post-renderer before installation. Fresh cluster ownership/context checks and
all original monitoring gates still apply. Nothing has been installed or made
live-ready by this RBAC-only continuation; Phase 16 is not complete.

## O. Final AKS Application Validation and Phase 16 Closure — 2026-10-07

### O1. Evidence authority, scope and reconciliation

**Phase 16: PASS — PHASE CLOSED. AKS DEPLOYMENT / RUNTIME VALIDATION:
COMPLETE / PASS.** The operator completed the final live deployment and validation
and supplied the authoritative results below. This closure task only reconciles
documentation; Codex did not repeat live checks or tests, inspect secret values,
change resources, or independently remeasure these results. Validation-time
observations are not a claim of continuous health after that window.

Repository preflight confirmed branch master and HEAD
`f9b47fda4658935b64826f1d4abe0488c64f21ae`. Only this report was already modified.
All prior evidence was retained; the former top-level current-status heading was
reclassified as historical and a new closure summary was inserted. This section
supersedes the initial/AKS-continuation blockers, dependency readiness checkpoints
in K–M, N1–N6's uninstalled monitoring status, and N7's pending-installation handoff.
The operator's later live evidence now establishes real deployment and monitoring
integration. Prior proposed Secret/configuration/deployment work is no longer the
next phase; no Secret names, values or delivery mechanism are inferred here.

The original broad capacity/HPA ambition is reconciled with the operator's final
acceptance decision: bounded target-cluster baseline and dependency-limit evidence
are complete, while full AKS HPA calibration is explicitly deferred and is not
required to close Phase 16. Historical statements about incomplete gates remain
accurate for their original checkpoints only.

### O2. Real application deployment and runtime readiness

| Validation-time property | Operator-provided result |
| --- | --- |
| AKS context | epolymind-aks-dev |
| Helm release / namespace | polymind / polymind |
| Deployment | polymind-polymind |
| Replicas | 2/2 Ready, 2 available, zero restarts |
| Observed pods | polymind-polymind-7c5ddd8764-l748p; polymind-polymind-7c5ddd8764-sqvfr |
| Observed node placement | Distributed across aks-agentpool-40344793-vmss000000 and aks-agentpool-40344793-vmss000001 |
| Application Service | polymind-polymind, ClusterIP, 10.0.222.129:8001 |
| Public exposure | No external IP, no Ingress, no public application exposure introduced |
| HPA / final replica posture | Absent/disabled; two fixed replicas |

The pod names are observations, not permanent architecture requirements. The
supplied evidence establishes distribution across both nodes without assigning
a particular listed pod to a particular node. Application image tag:

```text
epolymindacrdev-b7bxdheagnerb8ep.azurecr.io/polymind-api:f9b47fd
```

Both replicas' observed imageID was:

```text
epolymindacrdev-b7bxdheagnerb8ep.azurecr.io/polymind-api@sha256:fcc9cac926f6527975b3128a8e145d30bbd5f8578e7739b4956764806999f9eb
```

Thus both real replicas ran the expected immutable digest, even though the
application image reference used a tag. Both returned HTTP 200 for `/health`,
`/ready` and `/metrics`. The composite `/ready` result validates the configured
Foundry, Redis, Chroma HTTP and BM25 snapshot/version readiness checks. `/health`
alone does not check those dependencies. Multi-node placement and these health
results do not establish production HA or disruption/recovery behavior.

### O3. Foundry inference and Redis cross-replica persistence

The real authenticated direct query returned HTTP 200, route `direct`,
model_role `general`, model `epolymind-gpt-54-mini`, and exact response
`POLYMIND_AKS_QUERY_OK`. This proves real application-to-Foundry generation.

| Foundry property | Validated configuration |
| --- | --- |
| Resource | epolymind-foundry-dev-susanta |
| Deployment | epolymind-gpt-54-mini |
| Model / version | gpt-5.4-mini / 2026-03-17 |
| SKU / capacity | GlobalStandard / 10 |
| Observed deployment limits | 10 requests per 60 seconds; 10,000 tokens per 60 seconds |
| Subscription quota tier | Tier 1 |

The direct exchange used a unique synthetic session. After one replica wrote the
exchange, the other independently read two history messages: the user request
and assistant response `POLYMIND_AKS_QUERY_OK`. This validates shared Redis-backed
conversation memory across the real application replicas. The session was later
cleaned. No Redis credential or reconstructed connection URI is recorded.

### O4. Real RAG, shared Chroma and independent BM25

A real authenticated request asked: "Answer from uploaded documents: What is
retrieval augmented generation for knowledge intensive NLP tasks?" The result
was HTTP 200, route `rag`, model `epolymind-gpt-54-mini`, and one source:
`original_rag_paper.pdf`, chunk_id 0, rerank_score 5.1913838386535645. The returned
answer was grounded in the retrieved paper context. Reading that session through
the other replica returned HTTP 200 and two history items; the session was later
cleared.

This validates the live application path through semantic routing, Chroma dense
retrieval, BM25, hybrid/RRF, cross-encoder reranking, Foundry generation, Redis
persistence and a cross-replica memory read. It is one bounded end-to-end example,
not broad RAG quality validation.

Section M's corpus evidence remains authoritative: collection `phase16_knowledge`,
version `phase16-rag-62f3e0a6f547`, four PDFs and 1,058 chunks/vectors. Earlier
independent client validation proved heartbeat/readiness, record visibility,
independent BM25 snapshots, matching expected/published/loaded versions, dense
and sparse retrieval, hybrid retrieval and reranking. The final application
request adds actual deployed-path evidence to those earlier component checks.
Chroma remains emptyDir-backed and volatile. Corpus durability/recovery across
Chroma pod replacement or restart is NOT validated; no restart was performed
for this closure.

### O5. Live monitoring and custom-metrics delivery

Prometheus `polymind-prometheus` and Adapter release
`polymind-prometheus-adapter` run in monitoring. Both monitoring pods were Running
with zero restarts during validation. Services remained ClusterIP-only with no
public exposure. Adapter chart is prometheus-community/prometheus-adapter 5.3.0;
the previously verified package SHA-256 is
`aa6752b6207ed788522714c3ef7f67f27d423eb4d9512fecb52dc641b6434f31`.
Both `v1beta1.custom.metrics.k8s.io` and `v1beta1.metrics.k8s.io` reported
Available=True. The operator verified the live hardened rule exactly:

```yaml
apiGroups:
- custom.metrics.k8s.io
resources:
- pods/polymind_active_query_requests
verbs:
- get
```

Both real application pods were scraped and exposed through the custom-metrics
API. Idle values were 0/0. During C2, one observed sample was 2/0; the evidence
does not assign those values to permanent pod identities or establish balanced
request distribution. After completion, values eventually returned to 0/0.
No exact propagation latency is claimed.

The actual application metric path is now validated:

```text
PolyMind Pods: active_application_requests{operation="query"}
  -> Prometheus scraping
  -> polymind:active_query_requests:sum_by_pod
  -> Prometheus Adapter
  -> custom.metrics.k8s.io: pods/polymind_active_query_requests
```

This supersedes the probe-only/uninstalled limitations in N for the real
application path. Streams remain excluded from the primary signal. A final
post-deletion missing-series check was NOT captured in this Azure environment;
no PASS is claimed for it. The APIService retains insecureSkipTLSVerify=true,
which is a validation-environment limitation, not production TLS posture.

### O6. Bounded target-cluster C1/C2 capacity baseline

HPA stayed disabled throughout the operator's calibration. Both workloads were
direct queries against the fixed two-replica application deployment.

| Measurement | C1 | Correct C2 |
| --- | ---: | ---: |
| Concurrency | 1 | 2 |
| Requested requests | 6 | 12 |
| Completed requests | 6 | 12 |
| Successes / failures | 6 / 0 | 11 / 1 |
| Duration (s) | 5.795326 | 4.488056 |
| Successful throughput (req/s) | 1.035317 | 2.45095 |
| p50 latency (s) | 0.847064 | 0.739507 |
| p95 latency (s) | 1.510164 | 1.074616 |
| p99 latency (s) | 1.510164 | 1.074616 |
| Benchmark failure category | None | http_error |

An accidental second C1-equivalent run occurred because a sed-based manifest
transformation did not change concurrency/request arguments. It is not C2 evidence;
only the corrected C2 measurements above are used for that classification.
Successful-request latency does not establish C2 production safety: one request
failed. These small bounded runs are not production capacity ceilings, SLOs or
HPA sizing recommendations.

Post-C1 application resource samples were approximately Pod A 8m CPU/404 MiB and
Pod B 17m CPU/392 MiB. Post-C2 samples were approximately Pod A 15m CPU/406 MiB and
Pod B 6m CPU/394 MiB. These are post-run samples, not measured peaks or proof of
production headroom. Both replicas remained healthy/Ready with zero restarts.

### O7. C2 failure attribution and inference-capacity boundary

The operator's application logs definitively correlated request
`phase13-direct-11` with an OpenAI-compatible provider failure: role general,
model epolymind-gpt-54-mini, upstream status 429; then normalized category
`overloaded`; then `POST /query` HTTP 503 Service Unavailable. The failure was
Azure Foundry rate limiting, normalized by PolyMind to overloaded/503. It was not
AKS saturation, Redis/Chroma/BM25 failure or an application crash.

Provider/application counters on the affected replica supported the diagnosis:

| Observed counter | Value |
| --- | ---: |
| Inference generate success / error | 15 / 1 |
| Inference error category overloaded | 1 |
| Direct application success | 14 |
| RAG application success | 1 |
| Application error route unknown | 1 |

Redis reads/appends remained successful; the other replica showed no inference
errors. These are observed counters across the validation window, not counters
asserted to equal the C2-only request totals.

Read-only Foundry inspection confirmed capacity 10, GlobalStandard, Tier 1,
10 requests/60 seconds and 10,000 tokens/60 seconds. Available Azure Monitor
metrics included ModelRequests, AzureOpenAIRequests, InputTokens, OutputTokens,
TotalTokens, AzureOpenAIAvailabilityRate, AzureOpenAITimeToResponse,
AzureOpenAINormalizedTTFTInMS, AzureOpenAINormalizedTBTInMS and
AzureOpenAITokenPerSecond. A narrow recent query yielded limited/lagged data:
one visible HTTP 200 request and TotalTokens=901. That is not an exhaustive
application request count. The application/provider logs and counters are the
authoritative evidence of the real 429.

### O8. HPA decision and acceptance boundary

**HPA TARGET-CLUSTER SCALE-UP/SCALE-DOWN CALIBRATION: DEFERRED / NOT REQUIRED TO
CLOSE PHASE 16.** The current external Foundry deployment reaches its rate limit
before a meaningful higher-load AKS autoscaling experiment can be completed.
This is a dependency-capacity limitation, not an AKS runtime validation failure.

The HPA control-plane architecture retains Phase 15 validation, and Phase 16 now
validates the real AKS custom-metrics delivery path. Neither AKS scale-up nor
AKS scale-down is claimed to have passed. No production autoscaling is enabled;
no calibrated target, maximum replica count or scaling policy is established.
Final state stays two fixed real replicas, HPA absent/disabled, and Foundry
capacity unchanged at 10. Capacity was not increased merely to force an HPA test.

### O9. Retained security, durability and production limitations

- AKS networkPolicy provider is **NONE**. No Kubernetes NetworkPolicy enforcement
  or namespace-isolation claim is made. The application chart NetworkPolicy was
  intentionally disabled for this deployment because no provider enforces it and
  default chart topology assumptions do not match external Azure Redis/Foundry.
- Redis Private Link/private networking does not provide per-workload Kubernetes
  isolation. Chroma, Prometheus and Adapter are ClusterIP-only but lack an enforced
  namespace-level NetworkPolicy boundary.
- Adapter aggregation uses insecureSkipTLSVerify=true; production certificate
  verification remains deferred.
- Chroma emptyDir storage is volatile. Persistence, recovery after replacement or
  restart, backups and production HA are unproven.
- Azure Managed Redis remains non-HA/no-persistence dev/test infrastructure.
- Foundry access-key-style credentials are the Phase 16 validation posture;
  workload identity integration has not been completed.
- Broad RAG quality, production HA/readiness and higher-load autoscaling are not
  established by the bounded acceptance evidence. The Azure post-deletion
  missing-series test remains unproven.

These are retained limitations and deferred production work, not concealed PASS
claims. The phase's acceptance boundary is a working target-environment control
plane and dependency/monitoring integration with a bounded capacity baseline.

### O10. Cleanup, retained resources and cost posture

The operator cleaned the unique direct-test session and the synthetic RAG session.
Benchmark sessions `phase13-direct-0` through `phase13-direct-11` were also
explicitly cleared and verified empty. Earlier cleanup evidence in K–N remains
historical evidence; this closure does not infer removal of any other final-run
probe, benchmark pod, port-forward or artifact whose removal was not supplied.
No cleanup or resource operation was executed during this documentation task.

The two application replicas and supporting Phase 16 resources are retained.
No Foundry capacity increase or additional paid infrastructure was intentionally
provisioned to force autoscaling validation. Existing Azure resources remain
billable while retained. No new cost calculation is made; prior estimates remain
historical estimates. Future cost optimization or resource cleanup is an operator
decision, not an action performed by closure.

### O11. Documentation review and verification

Documentation-only validation checked `git diff --check`, reviewed
`git diff -- docs/codex/reports/phase_16_report.md`, and compared the closure edits
with the pre-task report baseline. The previous report body was preserved except
for reclassifying its old current-status heading as historical. Status and diff
scope confirmed only this already-modified report changed. A non-printing scan
of the report and diff checked obvious credential/private-key/token/credential-URL
and subscription-ID patterns; no exposed values were identified.

Review confirmed PASS/CLOSED, AKS runtime COMPLETE, HPA calibration DEFERRED,
Foundry 10 RPM as the limiting dependency, HPA disabled, and explicit emptyDir,
networkPolicy NONE and production-readiness limitations. Earlier pending and
incomplete statuses are explicitly superseded, not erased. No runtime code,
configuration, tests, Helm assets or dependency contracts changed. No additional
pytest, Helm, cluster/cloud inspection, load test or capacity change was run;
earlier validation counts remain evidence of their dated tasks only. No secrets
were inspected, no Azure or Kubernetes mutation occurred, and no commit or push
was performed. The report remains uncommitted for operator review.

### O12. Document Digestion roadmap handoff and final verdict

Next: **Phase 17 — Production Document Digestion & Intelligence**.
Beginning with **Phase 17A — Architecture, Cost & Risk Assessment**.
Phase 17A is a design/read-only assessment for the 200–1000+ page
document-digestion capability, not an implementation or provisioning phase.
The planned sequence remains:

| Phase | Planned scope |
| --- | --- |
| Phase 17A | Architecture, Cost & Risk Assessment |
| Phase 17B | Canonical Document Model, Object Storage & Extraction Plane |
| Phase 17C | Durable Job Orchestration, Idempotency & Recovery |
| Phase 17D | Hierarchical Evidence-Grounded Digestion |
| Phase 17E | Managed Inference Integration |
| Phase 17F | RAG Publication, Provenance & Interactive Document Analysis |
| Phase 17G | Multi-User Security, Quotas & Cost Governance |
| Phase 17H | 200–1000+ Page Reliability, Failure & Quality Validation |
| Phase 17I | External User Verification |

Phase 16 Foundry work is preparatory infrastructure relevant to future Phase 17E;
it does not mean Phase 17E has started or completed. The next activity is
Phase 17A, not Phase 17B or Phase 17E. This closure does not start any Document
Digestion work.

**Phase 16 PASS / CLOSED.** The Azure/AKS target environment has validated the real
PolyMind application control plane and its required Phase 16 dependencies:
Foundry, Redis, Chroma/BM25, monitoring and the custom-metrics delivery path. The
two-replica AKS deployment was healthy and operational for validation. Full AKS
HPA scale-up/scale-down calibration is deliberately deferred because the current
Foundry GlobalStandard deployment is limited to 10 requests per 60 seconds and
became the bottleneck during bounded C2 testing. This does not block Phase 16
closure. Production hardening remains outside the Phase 16 acceptance boundary.
