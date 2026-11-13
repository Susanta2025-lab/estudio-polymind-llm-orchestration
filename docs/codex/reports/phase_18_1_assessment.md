# Phase 18.1 — Secure document frontend and Azure readiness assessment

Assessment completed 13 November 2026; operator review pending. **Assessment only: no Phase 18 functionality implemented.** Stage 18.2 Implementation and Verification and Stage 18.3 Documentation and Closure remain NOT STARTED. The [preserved master prompt](../prompts/phase_18_1_assessment.md) controls scope.

## Executive summary and recommendation

Extend **the existing Streamlit application** with an operator-only Documents view backed by narrowly scoped, OIDC-protected FastAPI adapters. Run the first integrated browser milestone **locally**, with synthetic technical sources, fake structured inference and existing private single-host authorities. Keep `SupervisedPilot` as an owning-operator boundary; do not turn its publication/approval capabilities into participant privileges. No separate React/Next.js application, AKS activation, new vector database, managed database or queue is needed for that first milestone.

The repository already supplies canonical extraction, immutable objects, durable jobs/checkpoints, bounded hierarchical synthesis, authorized publication, selected-document retrieval, original-source citations and governed Q&A. The missing work is protected runtime composition, browser identity/session integration, operator HTTP contracts, an independent bounded runner and honest presentation/recovery. Rebuilding the document pipeline would increase risk and duplicate tested capabilities.

The current Helm deployment is a historical query-plane topology, not a deployable Phase 18 document service: two replicas, temporary storage and static-bearer secret injection conflict with single-host document authorities and OIDC configuration. Production distributed authorities, privacy/erasure, ordinary-user identity and current Azure pricing/runtime evidence remain separate blockers. This assessment selects a bounded implementation stage rather than hiding those gaps behind a production-ready claim.

The operator's addendum leaves local-first fixed and makes the cloud question explicit. **Azure verdict: `AKS_NOT_REQUIRED`. Recommend avoiding AKS for the initial Azure deployment and using one small private Linux VM with Docker, persistent local disk, one document lane, tested restore and explicit host/security maintenance.** This is the lowest-cost suitable architecture candidate considering current-state migration and operations, subject to measured memory/recovery and current exact resource quotes. It is not a claim that an unverified VM SKU has the cheapest invoice under every workload. Container Apps Consumption is the preferred future managed-host candidate after shared durable authorities exist; App Service is also viable after that migration. No present Kubernetes-only requirement was found.

| Independent verdict | Classification | Meaning and evidence |
| --- | --- | --- |
| `LOCAL_FRONTEND_IMPLEMENTATION_READINESS` | **READY** | Existing ports, tests and a bounded specification permit local implementation after operator authorization. This is readiness to implement, not an already working/authenticated portal; new integration acceptance gates remain unmet |
| `PRIVATE_AZURE_VALIDATION_READINESS` | **BLOCKED** | Current runtime UNKNOWN; no reviewed current resource/cost/execution scope, persistent single-host document deployment, browser identity or private-network proof. Local implementation is not blocked by this |
| `PRODUCTION_EXTERNAL_EXPOSURE_READINESS` | **BLOCKED** | Missing shared distributed authorities, multi-user/session/privacy/restore/network evidence, representative quality and exposure approvals. Phase 17 review remains 0/2 and actual external participants remain zero |

## Verified repository and GitHub baseline

Initial read-only checks executed: `git status --short --branch`, `git log --oneline -7`, `git rev-parse HEAD`, `git diff --check`, `git diff --stat` and `git diff --cached --name-only`.

| Fact | Observed value |
| --- | --- |
| Branch | `master...origin/master` |
| HEAD | `faaddc271f5e3165e4707e72a0309cc1784a4c48` |
| Tracked working/index differences at start | Empty |
| Inherited untracked files | Exactly **28** Phase 17H prompt/report documents, preserved |
| Equivalent Phase 18 documents at start | None found in repository filename inventory |
| Repository instructions | [AGENTS.md](../../../AGENTS.md) read; narrower assessment restrictions override general Docker/Kubernetes permissions |
| Preservation snapshot | SHA-256 inventory of **596** pre-existing tracked/unignored files captured outside repository before editing |

The seven observed commits were:

```text
faaddc2 docs: finalize Phase 17I engineering closure with external verification deferred
ed7dbd5 feat(pilot): implement bounded supervised Phase 17I verification workflow
69c8f66 docs: complete Phase 17I readiness assessment and identify external pilot gates
b90f4ad docs: mark Phase 17 engineering complete with human semantic review deferred
9acfeb6 docs: preserve Phase 17H live evaluation history and v10 evidence
f8ba9c1 feat: implement Phase 17H v11 reducer improvements and live readiness
ec22fa3 feat(digestion): implement Phase 17H v8-v10 provenance and generation-wire hardening
```

Connected GitHub read-only workflow-job inspection returned the supplied run's `build` job completed/success, including tests/imports, Helm/Compose validation and Docker build. `gh run view 43395472477 --repo Susanta2025-lab/estudio-polymind-llm-orchestration --json headSha,status,conclusion,workflowName,url,createdAt,updatedAt` independently verified **Estudio PolyMind CI**, completed/success, exact current HEAD, created **2026-11-13T08:43:36Z**, updated **08:51:16Z**. [CI run](https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/43395472477). CI was read, not rerun. No cloud state or new assessment test result follows from it.

## Source investigation and existing capabilities

The [frontend/API decision](../../evaluation/phase_18_1_frontend_integration_architecture.md) is the detailed route, interface and journey authority. The [Azure assessment](../../evaluation/phase_18_1_azure_deployment_readiness.md) is the topology/cost authority, and the [implementation plan](../../evaluation/phase_18_implementation_and_verification_plan.md) owns scope classifications, test groups and acceptance gates. All proposed contracts are explicitly NOT IMPLEMENTED.

| Inspected implementation/configuration/tests | Finding and reuse boundary |
| --- | --- |
| [ui/app.py](../../../ui/app.py), [ui/api_client.py](../../../ui/api_client.py), [UI tests](../../../tests/unit/test_ui_api_client.py), [settings](../../../config/settings.py) | Chat-only UI sends query/session_id to legacy NDJSON without Authorization. Session messages are UI-local, Clear Chat does not clear backend memory. Sources show chunk/score metadata, not canonical citation navigation. No login, document selection/upload/progress/digest/selected-Q&A/share/withdrawal UI |
| [api/app.py](../../../api/app.py), [middleware](../../../api/security.py), [API security tests](../../../tests/unit/test_security_api.py) | Existing routes: GET `/`, `/health`, `/ready`, `/metrics`, `/memory/{session_id}`, `/usage`; POST `/query`, `/query/stream`, `/documents/analyze`, `/documents/{document_id}/shares`; DELETE document shares/document/memory; conditional docs/schema. No job/upload/catalog/digest/pilot/publication/login routes. `/jobs/` is a protected path class only |
| [identity](../../../security/identity.py), [models](../../../security/models.py), [authority](../../../security/authority.py), [runtime](../../../security/runtime.py), [authorized services](../../../security/services.py), [security contract](../../security/phase_17g.md) | Server-verified canonical principal, owner/tenant grants and epochs, bounded content-free audit and final response-release guard. OIDC requires explicit governance/runtime; authorized analysis registry is supplied by operator, not automatically constructed. Existing OIDC legacy query denial is intentional |
| [extraction](../../../documents/extraction.py), [storage](../../../documents/storage.py), [document tests](../../../tests/integration/test_document_plane.py) | Strict native PDF/UTF-8 extraction, canonical immutable scoped version/hash/artifact identity; LocalObjectStore put/read/inspect. No Blob adapter or deletion/list/erasure guarantee |
| [jobs service](../../../documents/jobs/service.py), [ledger](../../../documents/jobs/sqlite.py), [worker](../../../documents/jobs/worker.py), [job tests](../../../tests/integration/test_document_jobs.py) | Durable local idempotent DAG/outbox/leases/fences/checkpoints/reconciliation/cancel. LocalDispatcher is not durable truth; worker service/supervision not composed into HTTP/UI |
| [digestion workflow](../../../documents/digestion/workflow.py), [managed](../../../documents/digestion/managed.py), [digest model](../../../documents/digestion/models.py), [digestion tests](../../../tests/integration/test_document_digestion.py) | Hierarchical maps/reducers/validation with exact findings, qualifications/conflicts/coverage/checkpoints. Explicit v11 supported; global StageProfile default stays v10. Digest statuses COMPLETE/PARTIAL/FAILED are separate from job state |
| [publication service](../../../documents/publication/service.py), [authority](../../../documents/publication/authority.py), [retrieval](../../../documents/publication/retrieval.py), [analysis](../../../documents/publication/analysis.py), [publication tests](../../../tests/integration/test_publication_chroma.py) | Operator authorization, prepared immutable generations/CAS cutover/rollback, selected dense and per-document BM25, original-source Citation binding. Q&A is bounded/tool-free and may abstain; provenance validation does not prove semantics |
| [pilot facade](../../../documents/pilot/service.py), [policy/approvals](../../../documents/pilot/models.py), [intake](../../../documents/pilot/intake.py), [controls tests](../../../tests/unit/documents/test_pilot_controls.py), [integration](../../../tests/integration/test_supervised_pilot.py) | Private Python owning-operator facade integrates approved source→job→v11→publication→presentation/Q&A→closure. Policy/source/session/authority/model binding, conservative inventory and synthetic-only default execution hook reusable. No participant login/API or real consent from fixtures |
| [governance](../../../governance/ledger.py), [execution](../../../governance/execution.py), [evaluation overlay](../../../governance/evaluation.py), [admission](../../../llm/admission.py), [provider factory](../../../llm/provider_factory.py), [governed tests](../../../tests/integration/test_governed_digestion.py) | Owner+tenant cost/token/concurrency limits, reserve/settle and UNKNOWN retention; shared provider RPM/TPM/reserved output, per-job/background limits and exclusive pilot admission. Factory RestrictedProvider blocks unbound execution; no new browser action may bypass binding |
| [Dockerfile](../../../Dockerfile), [.dockerignore](../../../.dockerignore), [Compose](../../../docker-compose.yml), [Helm values](../../../deployment/helm/polymind/values.yaml), [deployment](../../../deployment/helm/polymind/templates/deployment.yaml), [runbook](../../security/production-security.md), [metrics](../../operations/observability.md) | Reuse non-root/offline-model container, existing local fixtures/monitoring. Need document mounts, OIDC secret omission, worker/frontend/TLS composition, no second SQLite writer; credentials must stay outside image |

Consumers of the proposed integration were searched across the repository: `SupervisedPilot` construction is in tests/helpers; `AuthorizedAnalysis` is operator/test supplied on app.state; the current UI only consumes `stream_query`. New adapters must not silently change existing contracts. Exact permission semantics, request/result schemas and proposed replacements are recorded in the architecture document rather than inferred from endpoint names.

## Historical evidence and unresolved acceptance

The [Phase 17I Stage 2 report](phase_17i_implementation_and_verification.md) records **3,052 passing tests**, **2,163 unit / 889 integration**, including **56 new cases** (27 unit / 29 integration), not 3,052 plus 56. Its synthetic end-to-end path used four deterministic calls, COMPLETE coverage 1.0, four synthetic settled reservations, zero outstanding synthetic reservations, one canonical Q&A citation and CLOSED/PURGE_PENDING. It established contract composition, not actual external participation or invoice measurements. No tests were rerun here.

The [v11 live report](phase_17h_v11_controlled_live_execution_and_reconciliation.md), including its later continuation rather than only its initial stop record, records **one successful four-call actual Foundry invocation on 12 November**: chunk, structural, root and grounded Q&A; **6,408 input / 1,327 output tokens**, local catalog settlement **EUR 0.009675030297596252**, one canonical page-1 citation and strict provenance/receipt checks. The actual input scope was four pages. These results support actual-model technical integration for that controlled example; independent human semantic entailment, representative source quality, larger real documents and public-product reliability remain unverified. The prior failure reports and missing raw v10 comparison artifacts were not rewritten or reopened.

The [17I closure](phase_17i_documentation_and_closure.md) and [completion decision](../../evaluation/phase_17i_engineering_completion_and_deferred_acceptance.md) remain authoritative. Preserve exactly:

```text
PHASE_17_ENGINEERING_COMPLETE
DEFERRED_PENDING_TWO_INDEPENDENT_REVIEWERS
PHASE_17_FORMAL_CLOSURE_PENDING
PHASE_17I_ENGINEERING_COMPLETE
PHASE_17I_EXTERNAL_VERIFICATION_DEFERRED
PHASE_17I_FORMAL_ACCEPTANCE_PENDING
SUBSEQUENT_ENGINEERING_PERMITTED
```

Independent review remains **0/2** and actual external-user verification remains deferred. Neither automatically blocks local synthetic engineering. A structurally valid citation must continue to show `semantic_support=not_evaluated`; this assessment is not a semantic review or participant acceptance decision.

## Architecture and security conclusions

The frontend comparison covers A Streamlit, B dedicated web stack and C minimal private operator app across integration, security, UX, reliability, cost, WSL/Docker/Kind, Azure, maintenance, effort and product scope. A is preferable because the workflow is forms/status/structured artifacts/Q&A over a strong existing Python backend. C is feasible but duplicates UI; B adds toolchain/session/hosting costs without solving the immediate protected-service gap. Plan about **12–20 focused engineer-days**, contingent on pinned login compatibility and no cloud/distributed scope; this estimate is relative engineering work, not a promise.

A private operator may retain publication-management authority only because the workflow explicitly remains operator controlled. Ordinary users must never receive that role to make the demonstration work. The existing Entra profile accepts only `PolyMind.L1Operator`, not a general user hierarchy. Browser login must obtain an API-audience access token and exercise actual verifier/authority checks. Identity email/ID token/Streamlit session state cannot become ownership claims. Enrollment restrictions are additional to token signature validity: configured-issuer authentication currently registers accepted principals, so fixed allowlists and issuer application assignment need explicit integration.

Current Streamlit official documentation and the installed pinned-runtime source were checked for authentication. Native token exposure is available, but exposed tokens are in signed HttpOnly cookies, not encrypted opaque server sessions; cookie Secure behavior and expiry need explicit TLS/proxy tests. Authlib is not pinned and needs a narrow dependency decision during implementation. The architecture specifies offline local IdP/JWKS fixtures, exact API token validation, no shared-token paste fallback, CSRF/origin/XSRF protection and per-rerun authorization. See [authentication design](../../evaluation/phase_18_1_frontend_integration_architecture.md#authentication-and-session-design--not-implemented) and its official documentation links. Production requires a stronger reviewed token/session design before external/confidential data.

The safe initial data class is **synthetic nonpersonal technical samples only**. Later licensed public/nonpersonal material requires explicit license, provider-transmission and retention decisions; public accessibility alone is insufficient. Private, proprietary, sensitive and erasure-dependent sources remain excluded. Native parser resource containment is not a complete hostile-file sandbox; catalog selection avoids unrestricted upload. Source/model content remains untrusted, inert and tool-free. Session withdrawal denies future output and records residual retained objects/answers/audit/backups; no full purge is claimed.

## Missing contracts and ranked engineering gaps

| Rank | Gap / dependency | Bounded remedy |
| --- | --- | --- |
| 1 | Browser identity/token/cookie/enrollment boundary and protected output release | OIDC login + fixture issuer + API bearer validation; owning-operator allowlist; expiry/logout; authority/session/publication guards at actual send |
| 2 | Service runtime and session/action contracts | Narrow operator adapter; same authority/admission/governance objects; catalog and server fixture approvals; durable idempotent intent mappings; no arbitrary facade method dispatch |
| 3 | Runner, dispatch/recovery and status authority | One host/lane, durable ledger/outbox, bounded operation versus lease, explicit reconciliation and reauthorization; polling without inference; UNKNOWN fail closed |
| 4 | Complete digest/citation/Q&A presentation and truthful state UX | Separate job/digest/session/error state, explicit publish, original evidence navigator, bounded session Q&A and abstention, honest residuals |
| 5 | Local configuration, readiness, restore and regression evidence | Private mounts/secret exclusions, fixture-only profile and no external transport, idle/publication/worker readiness, coherent backup/restore; all new negative cases |
| 6 | Azure/persistent/distributed operation | Conditional private single-host deployment after current inventory/price approval; shared relational/object/admission/queue/restore architecture deferred beyond Phase 18 |

Proposed operator API — **NOT IMPLEMENTED** — covers context, approved sources, create/select/start/status, explicit publication, digest/evidence packet, session-bound questions, cancel/close/withdrawal and stop. Every path and DTO is specified in the [single contract table](../../evaluation/phase_18_1_frontend_integration_architecture.md#proposed-http-contracts--not-implemented). No general upload, participant onboarding or publication-management API is invented as existing. Existing `/documents/analyze` needs explicit registry/provider composition; it cannot be a second unrestricted question path. Legacy `/query` and `/query/stream` remain OIDC-denied.

## Azure alternatives, persistence and cost conclusion

Local Architecture A remains the decided initial milestone. For cloud Architecture B, select a private single-host VM deployment; AKS remains a historical reference/conditional alternative, not the default. If later justified, the historical AKS cluster would need current inventory, private access, durable disk/backup, OIDC chart changes and enforced writer exclusion, not another ephemeral replica. Production C needs shared transactional implementations for jobs/security/governance/admission/publication/control, durable object authority, distributed dispatch/recovery and security release/restore correctness. PostgreSQL/Blob are sensible future candidates; Service Bus is not mandatory when a transactional DB outbox/dispatch may suffice. Stateless selected-document Q&A does not logically need chat Redis, but the **current production settings still require Redis and Chroma HTTP**. A VM using that profile must include private colocated services and their measured memory/disk/backup overhead; no managed Redis purchase is required and validators must not be bypassed. Chroma remains a derived/rebuildable index, not the archive.

| Azure hosting decision | Total cost and compatibility | Operations, security/reliability and scaling |
| --- | --- | --- |
| Container Apps Consumption | Potential low/zero app compute when idle, but current ephemeral disk/Azure Files cannot safely host local transactional authorities; external DB/object/index hosting and migration add cost | Managed restarts, Jobs/WebSockets/private ingress supported; shared-state/release correctness, job checkpoints, replica caps and cold-start/session tests required before use |
| App Service | Paid suitable plan plus external transactional state; network-shared persistent filesystem rules out current SQLite authority layout | Supported Linux WebJobs with Always On, app recycle/scaling tests, private-network tier costs and worker singleton required; ordinary app Stop does not pause a paid plan |
| **VM — selected initial cloud** | One measured small host + persistent OS/data disk, backup/private access/log/registry; no obligatory managed DB/Redis/queue or authority migration | Operator patches/hardens/TLS/backs up; single-host recovery, no HA claim; vertical scale and one job lane first |
| AKS — reference | Node/system-pool/disk/network/monitoring baseline plus document topology work; no necessary Kubernetes feature identified | Existing Phase 16 evidence useful; cluster/CNI/PVC/auth/upgrade operations add complexity; replicas don't solve shared state |

Official sources and full requirement-by-requirement comparison are in [mandatory hosting comparison](../../evaluation/phase_18_1_azure_deployment_readiness.md#mandatory-azure-hosting-comparison), including Streamlit/FastAPI, digestion, authorities, documents/indexes, Redis/workers, provider boundaries, recovery, observability/backup, private access and scaling. App Service's newly announced **10 November Premium v4 plan-stop preview** is distinguished from ordinary app Stop; availability is not assumed. No host is selected merely because it can run Docker.

The [Azure/cost document](../../evaluation/phase_18_1_azure_deployment_readiness.md) defines each service's necessity, ports, migration/rollback/correctness, operational dependencies and billing drivers. It quantifies zero-new-Azure local development, an illustrative **8-hour private window** and **730-hour always-on month**, including storage/network/DB/Redis/log/registry/key/backup residuals. Official pages were retrieved 13 November; unavailable selected rates are explicitly **UNVERIFIED**. No current numerical provider quote was fabricated.

The addendum's TCO comparison also covers **occasional weekly demonstration (20 compute hours/month including startup/backup/teardown)**, **intermittent 1–5-user demand** and **always-on availability** across all four hosts. A low-traffic VM still needs 730 hours if users expect access anytime. ACA scale-to-zero can save app compute, but not external transactional/index/backup/network services; open Streamlit WebSockets, polling and workers affect actual lifetime. App Service usually keeps a paid plan baseline; plan-stop preview is a separately constrained case. A candidate 2 vCPU/8 GiB VM must pass aggregate memory/CPU/storage measurements; no smallest SKU is declared sufficient without evidence. Azure pricing remains UNVERIFIED; formulas include inference and residual services plus setup/recurring operator labor. In illustrative unverified small-VM input sensitivity USD 0.05–0.15/hour, compute is USD 1–3/20 hours or 36.50–109.50/730 hours **before** disks/backups/access/logs/registry/inference/labor. These are not provider quotes or approved ceilings.

For scale only, the document's **hypothetical unverified** node input of USD 0.20–0.40/node-hour gives two-node compute USD 3.20–6.40/8 hours and USD 292–584/month, before every other service. This is sensitivity arithmetic, not an Azure quotation or approved ceiling. Always-on DB/Redis/network and retained storage can dominate tiny inference workloads. Inference maximum pilot envelope is six attempts × 24,800 input and 3,000 output reserved units/document; price using the exact approved model/SKU and current policy. Historical fractional-EUR v11 settlement is not permission or a new price estimate. The EUR 5 policy remains a limit, not a spend grant. Workload stop does not establish zero associated cloud charges.

## Reliability and observability assessment

| Failure/operation | Existing foundation | Missing local integration / production limit |
| --- | --- | --- |
| Long-running work/progress | Durable JobLedger, step state and digest coverage | Runner/status polling, stale progress and requested-versus-queued presentation; four-page bounded policy initially |
| Restart/checkpoint/resume | Outbox, lease/fence, accepted manifests and compatibility | Reconcile delivered dispatch/lease expiry; fresh auth; no possible duplicate inference; not autonomous distributed recovery |
| Provider timeout/429/backpressure | Normalized provider errors, shared admission/settlement | Honest capacity-wait/unknown UI, no paid auto retry/fallback; historical quotas not current capacity |
| Cancel/crash/emergency stop | Cancel fencing, pilot durable stop/close and conservative inventory | Integrated transport release races, worker shutdown/reopen; upstream may finish/bill |
| DB/vector/object outage | Fail-closed authorities, replica generation and integrity checks | New readiness/status projection, no index repair from read route; no false success |
| Publication rollback | Prepared/active CAS generations and security epochs | Explicit UI publication/reload/reconciliation, no restored revoked access |
| Audit exhaustion/UNKNOWN | Bounded audit fails closed; unsettled reservations remain | Operator-visible sanitized condition and emergency stop; no silent ledger recreation/reset |
| Backup/restore/multi-replica | Local interfaces and retained object inventory | Coherent local restore proof needed; shared/distributed recovery remains unestablished |

Reuse existing Prometheus/readiness and content-free correlation; add only missing bounded worker/job/admission/outcome signals. Job/document IDs belong in authorized status/audit records, not metric labels. No new observability platform or production SLO is justified. Synthetic tests, historical AKS validation, four-page actual-model evidence, future browser evidence and unestablished production scale remain distinct evidence categories.

## Explicit answers to the sixteen assessment decisions

| Question | Decision |
| --- | --- |
| 1. Extend Streamlit or replace? | Extend safely within operator/synthetic scope, with new authentication and protected adapters/tests. Dedicated web stack is not justified now |
| 2. Minimum FastAPI interface? | New operator workflow contracts in the architecture table; reuse secured analysis/authority services and preserve existing routes. No upload or ordinary-user publication privileges |
| 3. Reuse SupervisedPilot? | Yes, only behind its current owning-operator scope, ceilings and execution/quality gates. Not a participant-facing facade |
| 4. Private browser authentication? | Streamlit authorization-code login + API access token validated by FastAPI; native signed-cookie limitations mitigated/tested for private synthetic use. Local fixture issuer first; live Entra configuration separately authorized |
| 5. What works without Azure? | Entire bounded source→extraction/job→digest→publication→citation/Q&A→closure journey, authentication contracts, failure/recovery and budget enforcement with local fixtures |
| 6. Synthetic demonstration? | Actual production pipeline/services with deterministic provider responses and fixture vectors/embeddings, visibly synthetic and zero paid calls. No semantic or user-usefulness acceptance inferred |
| 7. Actual-model evidence? | Four-page v11 four-call digestion/publication/grounded Q&A technical success. Independent semantic review, larger representative workloads and integrated browser usability not established |
| 8. Is AKS necessary? | **AKS_NOT_REQUIRED**. Local-first is fixed; explicitly avoid AKS for initial cloud deployment and select the private small-VM candidate subject to sizing/security/quote gates |
| 9. Production service decisions now? | Preserve immutable object/JobLedger/provider/admission boundaries and single-host restriction. PostgreSQL/Blob candidates, DB dispatch first; no SKU/queue purchase now |
| 10. What can wait? | Distributed cloud adapters, queue, managed DB/Redis, workload identity, HA/HPA, public ingress, full erasure/DR and general user identity |
| 11. Minimum private Azure resources? | One suitable private Linux VM, persistent OS/data disks and coherent backup, TLS/operator access and image availability; approved provider access only if actual inference separately requested. Managed DB/Redis/queue and AKS not initially required; exact SKU/price/current resources unknown |
| 12. Recurring cost risks? | Idle node hours, always-on DB/Redis, persistent disks/backups, endpoints/IP/LB/NAT, registry/large images, logs and unchecked inference retries/UNKNOWN |
| 13. Accidental-charge controls? | Fixture-only runtime, no credentials/provider network, no cloud buttons/start scripts, production fixture rejection, shared quotas and UNKNOWN retention; independent exact future activation/spend approvals |
| 14. What implements 18.2? | Authenticated local operator Documents view, protected contracts/runtime, single-lane durable runner/replay, complete digest/evidence/Q&A/closure, safe limits/observability and T01–T15 verification |
| 15. Beyond Phase 18? | General public/multi-user production, sensitive uploads/erasure guarantees, shared relational/cloud authorities, distributed queue/workers, HA/DR/SLO/load certification and new frontend if later justified |
| 16. Private versus public evidence? | Private: all local gates plus current private topology/identity/persistence/cost/execution approval. Public: independently verified multi-user isolation/distribution, privacy/lifecycle/provider handling, network/restore/quality/capacity controls and explicit external exposure approval; design/CI alone cannot suffice |

## Stage 18.2 scope and acceptance recommendation

Approve only the bounded local scope in the [implementation plan](../../evaluation/phase_18_implementation_and_verification_plan.md). It classifies every candidate as REQUIRED_FOR_PHASE_18_2, CONDITIONAL_ON_APPROVED_PRIVATE_AZURE_TEST, DEFER_TO_PRODUCTION_HARDENING or OUT_OF_SCOPE. The plan defines proposed test groups T01–T15 and 17 acceptance gates with current evidence, missing action, severity, verification, decision owner and local/Azure/external blocker disposition.

Required acceptance includes real local browser authentication/token/cookie behavior, owner/tenant/enrollment denials, one integrated complete fixture journey, honest PARTIAL/FAILED/cancelled/insufficient states, canonical citations, durable duplicate/restart/recovery checks, authority/session/generation release races, financial exhaustion/UNKNOWN and zero external provider/credential access. Streamlit AppTest or API-only checks do not silently establish actual browser-login cookie behavior. Required integration gaps cannot be waived using old Phase 17 counts. Optional cloud evidence is not required for local implementation closure.

Local rollback disables the Documents profile and denies admission/output, preserves authorities/objects/financial history and consumed approvals, reconciles UNKNOWN and loads only a permitted consistent generation. Never restore a previous allowance/security epoch to make a rollout pass. Stage 18.3 later documents actual behavior and evidence only; there are exactly three formal stages and no implementation Codex prompt has been generated.

## Remaining approvals

The operator must review/authorize Stage 18.2 scope and the private synthetic security posture, including native-login cookie handling and the small required auth dependency. No review response is assumed. Separate future decisions are required for cloud activation/provisioning/deployment/retention/shutdown scope; IdP redirect/consent/assignment changes; provider credential use and paid execution; exact live execution hook and any required RSA approval; source license/provider transmission/privacy/retention; representative semantic quality; actual participants and external/public exposure. Nothing in historical CI, the EUR 5 policy, deferred human review or this assessment grants any of those decisions.

## Validation, self-review and separate pre-commit review

Assessment validation is documentation-only. The five requested files were independently read after writing; links/anchors, fences/tables, source paths, phase/status terminology, historical counts/outcomes, proposed-route labels, cost formulas and uncertainty were reviewed. A separate preservation comparison checks all 596 starting files and inherited untracked documents; no historical evidence, implementation, dependency/configuration or authority file is intentionally changed. Final command outcomes and exact document-check counts are recorded in the validation addendum below.

Architectural self-review identified and made explicit: native signed-token cookie exposure; missing Authlib pin; exact Entra role restrictions; owner-action semantics versus unused JOB enums; automatic registry absence; readiness before first publication; buffered-response session/generation races and ordered locks; delivered-dispatch/lease recovery versus max_attempts=1; uncertain question replay; pilot session exhaustion; unsupported physical purge; static-token Helm conflict; current production Redis/Chroma requirements versus VM sizing; settlement writes after cancellation; and single-host SQLite versus two-replica deployment. These are bounded implementation requirements or explicit production deferrals, not out-of-scope code fixes.

Separate pre-commit review checks only these five additions for credentials/private-key/JWT/credential-URL patterns, private data, hard-coded runtime paths, generated/debug files, stale TODOs, broken documentation, invented interfaces/permissions, accidental API/dependency changes and inherited-file modifications. It is a documentation heuristic/manual review, not a security certification. No pytest/full regression, compileall, Docker build, Helm execution, Kubernetes operation, cloud activation/login/renewal, model probe, private document processing, authority mutation, RSA execution approval, staging, commit or push occurred in this assessment. Public technical/pricing browsing and read-only GitHub inspection were the only external research.

## Files and Git disposition

Exactly five new Markdown files are assessment additions:

1. [Preserved prompt](../prompts/phase_18_1_assessment.md).
2. [This report](phase_18_1_assessment.md).
3. [Frontend and API architecture](../../evaluation/phase_18_1_frontend_integration_architecture.md).
4. [Azure readiness and finance](../../evaluation/phase_18_1_azure_deployment_readiness.md).
5. [Implementation and acceptance plan](../../evaluation/phase_18_implementation_and_verification_plan.md).

The **28 inherited untracked Phase 17H documents** are separate and unchanged. No existing file is modified. Final verified status is `master...origin/master` with **33 untracked Markdown files = 28 inherited + 5 assessment additions**, empty tracked `git diff --stat` and empty `git diff --cached --name-only`. Untracked additions do not appear in ordinary diff statistics; this is not a clean tree. Final verification confirms or corrects these values below.

Suggested commit message, for later operator use:

```text
docs: assess Phase 18 frontend integration and Azure deployment readiness
```

**No staging, commit or push. Stage 18.1 assessment complete; operator review is the next decision.**


## Final validation addendum

The cost-optimized Azure addendum was preserved with the original prompt and integrated into the Azure assessment, main report and implementation plan without restarting work or creating a stage. The explicit cloud verdict is **AKS_NOT_REQUIRED**; the selected initial private Azure candidate is the single-host VM, contingent on security/recovery/sizing and exact-price approval. Future managed Container Apps/Jobs remains a separate shared-authority migration requirement.

Documentation checks completed successfully: **96 local links/anchors**, balanced code fences and consistent table columns across all five files, **17 source interface names** verified through AST-only inspection, all **13 explicitly declared API routes** present in the inventory, **15 proposed verification groups** and **17 acceptance gates** consistent. Public provider references include retrieval date, planning region/currency/units and explicit nonzero-rate uncertainty. Cost arithmetic and historical 2,163 + 889 = 3,052 totals were checked. The prompt's Markdown hard-break trailing spaces were normalized after new-file whitespace inspection; its instruction content is preserved.

A separate pre-commit review found no credential/private-key/JWT/credential-URL payload, machine-specific private runtime path, newly introduced debug/TODO content, unrelated/generated artifact, dependency/code/API edit or altered historical evidence in the five additions. All **596 pre-existing tracked/unignored file hashes**, including the **28 inherited untracked documents**, remain unchanged. This scan/review is not a security certification.

`git diff --check` passed. New untracked files were also individually checked using `git diff --no-index --check /dev/null <file>`: no whitespace diagnostics (difference-only exit 1 is expected for added files). The final tracked `git diff --stat` and `git diff --cached --name-only` both have **empty output**. HEAD remains the exact baseline. No staging/commit/push or implementation occurred.

Final `git status --short --branch` output:

```text
## master...origin/master
?? docs/codex/prompts/phase_17h_current_authorization_and_token_headroom_assessment.md
?? docs/codex/prompts/phase_17h_final_approval_signing_and_controlled_execution.md
?? docs/codex/prompts/phase_17h_v10_authentication_renewal_and_final_operator_packet_preparation.md
?? docs/codex/prompts/phase_17h_v10_final_operator_verification_and_conditional_live_execution.md
?? docs/codex/prompts/phase_17h_v10_operator_preparation_and_readiness_assessment.md
?? docs/codex/prompts/phase_17h_v5_authorized_catalog_migration_and_commercial_reconciliation.md
?? docs/codex/prompts/phase_17h_v5_complete_financial_readiness_and_operator_preparation.md
?? docs/codex/prompts/phase_17h_v5_execution_window_renewal_and_rsa_authorization.md
?? docs/codex/prompts/phase_17h_v5_final_operator_preparation_continuation.md
?? docs/codex/prompts/phase_17h_v5_financial_reconciliation_and_second_four_call_readiness.md
?? docs/codex/prompts/phase_17h_v5_four_call_readiness_reassessment.md
?? docs/codex/prompts/phase_17h_v5_operator_preparation_signing_and_controlled_execution.md
?? docs/codex/prompts/phase_17h_v8_azure_operator_preparation_and_signing_readiness.md
?? docs/codex/prompts/phase_18_1_assessment.md
?? docs/codex/reports/phase_17h_current_authorization_and_token_headroom_assessment.md
?? docs/codex/reports/phase_17h_final_approval_signing_and_controlled_execution.md
?? docs/codex/reports/phase_17h_live_invalid_qualification_source_root_cause.md
?? docs/codex/reports/phase_17h_v10_authentication_renewal_and_final_operator_packet_preparation.md
?? docs/codex/reports/phase_17h_v10_final_operator_verification_and_conditional_live_execution.md
?? docs/codex/reports/phase_17h_v10_final_signing_and_controlled_live_outcome.md
?? docs/codex/reports/phase_17h_v10_operator_preparation_and_readiness_assessment.md
?? docs/codex/reports/phase_17h_v5_authorized_catalog_migration_and_commercial_reconciliation.md
?? docs/codex/reports/phase_17h_v5_complete_financial_readiness_and_operator_preparation.md
?? docs/codex/reports/phase_17h_v5_execution_window_renewal_and_rsa_authorization.md
?? docs/codex/reports/phase_17h_v5_final_operator_preparation_continuation.md
?? docs/codex/reports/phase_17h_v5_financial_reconciliation_and_second_four_call_readiness.md
?? docs/codex/reports/phase_17h_v5_four_call_readiness_reassessment.md
?? docs/codex/reports/phase_17h_v5_operator_preparation_signing_and_controlled_execution.md
?? docs/codex/reports/phase_17h_v8_azure_operator_preparation_and_signing_readiness.md
?? docs/codex/reports/phase_18_1_assessment.md
?? docs/evaluation/phase_18_1_azure_deployment_readiness.md
?? docs/evaluation/phase_18_1_frontend_integration_architecture.md
?? docs/evaluation/phase_18_implementation_and_verification_plan.md
```

There are **33 untracked documents**, comprising **five Phase 18.1 additions** and **28 unchanged inherited Phase 17H files**. Exactly three formal stages remain: 18.1 assessment COMPLETE pending operator review; 18.2 and 18.3 NOT STARTED. No cloud resources, paid calls, credentials, private documents or external participants were activated/accessed/processed by this assessment.
