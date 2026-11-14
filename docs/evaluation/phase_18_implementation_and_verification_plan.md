# Phase 18 — Implementation and verification plan

13 November 2026. Proposed bounded implementation specification, not implementation authorization or a Codex execution prompt.

Current disposition: see [14 November implementation reconciliation](#implementation-status--14-november-2026).
The original assessment-era tables below remain historical requirements, not current unfinished-stage claims.

## Exactly three formal stages

| Stage | Scope | Status at this handoff |
| --- | --- | --- |
| 18.1 | Assessment | COMPLETE — operator review pending |
| 18.2 | Implementation and Verification | NOT STARTED |
| 18.3 | Documentation and Closure | NOT STARTED |

Workstreams and verification groups below are activities within Stage 18.2, not additional formal stages. Do not start either later stage under this assessment. Phase 17 engineering completion, deferred independent semantic review at 0/2 and deferred external-user acceptance are unchanged. See [assessment report](../codex/reports/phase_18_1_assessment.md), [frontend decision](phase_18_1_frontend_integration_architecture.md) and [Azure/cost assessment](phase_18_1_azure_deployment_readiness.md).

## Assessment result and bounded outcome

Select frontend Option A: existing Streamlit plus a Documents view. Select deployment Architecture A: local single-host private operator workflow, synthetic sources and fake structured inference. Reuse `SupervisedPilot` behind an explicit owning-operator service, not a participant API. Do not combine this stage with distributed cloud migration. The independently useful outcome is: operator logs in, selects a preapproved synthetic source, submits once, observes a durable job, cancels or obtains a validated digest, publishes explicitly, navigates original evidence, asks bounded selected-source questions and closes/withdraws with honest retention residuals.

Local-first is already decided. Incorporating the cost-optimized Azure addendum, **`AKS_NOT_REQUIRED`**: the eventual initial private cloud candidate is **one small Linux VM running the local Docker composition**, persistent managed disk, private operator access, explicit host supervision/patching, coherent backups and single-host recovery. Avoid AKS unless a demonstrated new requirement warrants it. Exact suitable VM size/current pricing remain gates; 2 vCPU/8 GiB is a measurement candidate, not a proven minimum. Cloud deployment itself remains conditional, not required for local completion.

All new interfaces/features in this plan are **NOT IMPLEMENTED**. Existing named Python services and routes are described in the architecture decision; no route is created by this plan. A reviewer can approve this complete scope without also approving cloud activation or paid inference.

## Candidate classification

| Candidate | Classification | Concrete deliverable / boundary |
| --- | --- | --- |
| Streamlit Documents view and protected API client | REQUIRED_FOR_PHASE_18_2 | Catalog, mode/identity/limit display, session actions, progress, digest/evidence panes, bounded Q&A, closure and stop |
| OIDC browser login and operator enrollment | REQUIRED_FOR_PHASE_18_2 | Native login/access token adapter, API bearer validation, fixed allowlist, expiry/logout, TLS/cookie/CSRF controls; generic local test issuer for offline proof |
| Small login dependency and local TLS gateway/configuration | REQUIRED_FOR_PHASE_18_2 | Review/pin compatible Authlib if needed; use existing ingress capability where available or a minimal scoped development TLS proxy; no runtime/ML dependency expansion |
| Protected composition and operator HTTP contracts | REQUIRED_FOR_PHASE_18_2 | Exact runtime authority reuse, request DTOs, source/session bindings, action idempotency and final release guards |
| Synthetic source/approval catalog, native intake | REQUIRED_FOR_PHASE_18_2 | Preapproved byte/hash fixtures, strict policy ceilings, PDF/text eligibility and truthful fixture notices |
| Durable runner, restart/reconcile, cancel and stop | REQUIRED_FOR_PHASE_18_2 | One owner/job lane, ledger dispatch/recovery, deadlines, lease safety, UNKNOWN stop; no browser-driven step execution |
| Full validated digest and canonical citations | REQUIRED_FOR_PHASE_18_2 | COMPLETE/PARTIAL/FAILED visible, full supported fields, original evidence identity and no semantic verification claim |
| Session-bound selected-document Q&A | REQUIRED_FOR_PHASE_18_2 | Reuse pilot/DocumentAnalysis and existing governed execution; no legacy route bypass, no free unbounded second analysis path |
| Usage/limits and minimal observability | REQUIRED_FOR_PHASE_18_2 | Authorized summary/UNKNOWN, status freshness, sanitized errors/request IDs, worker/authority readiness and existing Prometheus reuse |
| Local durable mounts, coherent backup/restore and compatibility checks | REQUIRED_FOR_PHASE_18_2 | One host, no distributed SQLite, explicit fixture runtime/credential exclusion, Docker/Compose source configuration and smoke verification after implementation approval |
| Existing Kind validation | REQUIRED_FOR_PHASE_18_2 | Render/inspect compatibility where available; local Docker/API/browser proof is mandatory, actual Kind workload test only if dedicated context is available; inability documented without Azure fallback |
| Private Azure VM topology, disk/backup, host/TLS/OIDC secrets and lifecycle | CONDITIONAL_ON_APPROVED_PRIVATE_AZURE_TEST | Preferred cloud candidate; recheck exact suitable size/prices and private access; one authority domain, no overlapping writer, persistent disk; no activation for local acceptance |
| AKS-specific OIDC/Secret/Helm/PVC adaptation | CONDITIONAL_ON_APPROVED_PRIVATE_AZURE_TEST | Reference only, not default; require a separately demonstrated Kubernetes need and approval; no AKS dependency added to local implementation |
| Live Entra redirect/consent/assignment and real browser identity | CONDITIONAL_ON_APPROVED_PRIVATE_AZURE_TEST | Separate issuer approval; local OIDC fixture proves application contracts, not real tenant acceptance |
| New paid inference or retained real-model evidence presentation | CONDITIONAL_ON_APPROVED_PRIVATE_AZURE_TEST | Independent explicit data/quality/exposure/execution approvals; local acceptance uses neither; live calls need separately reviewed execution hook |
| Blob/PostgreSQL/shared admission/queue adapters and multi-replica workers | DEFER_TO_PRODUCTION_HARDENING | Contract and migration decisions recorded; no distributed adapter implementation in this stage |
| Ordinary-user access, share UI, unrestricted/hostile uploads, full erasure | DEFER_TO_PRODUCTION_HARDENING | New role/enrollment/privacy/isolation/lifecycle acceptance before enabling |
| Production BFF/session vault, HA, workload identity, DR/SLO/load certification | DEFER_TO_PRODUCTION_HARDENING | Distinct evidence gates beyond private operator synthetic posture |
| New React/Next stack, vector DB, Kafka, GPU/vLLM embedding, OCR service | OUT_OF_SCOPE | No demonstrated need for this milestone |
| External participants, private/proprietary/sensitive source processing, public launch | OUT_OF_SCOPE | Require future explicit authorization and applicable security/privacy/quality gates; no implied Phase 17 closure |
| Finance resets, quota increases, automatic paid retries/fallback or reused RSA approval | OUT_OF_SCOPE | Never implementation shortcuts |

## Required interfaces and composition — NOT IMPLEMENTED

### Azure hosting decision within the existing three-stage plan

| Alternative | Total cost / architecture | Operations / security / reliability / scaling | Disposition |
| --- | --- | --- | --- |
| Container Apps Consumption | App compute can scale to zero; durable DB/object/index and migration costs persist; current SQLite on ephemeral/network-share storage unacceptable | Managed hosts/Jobs/WebSockets viable after shared state; cold restart, tokens/session, checkpoint and replica/financial safety tests mandatory | Future managed-host candidate after production authorities; no migration in 18.2 |
| App Service | Suitable paid plan/worker plus shared transactional state; network filesystem incompatible with current authorities | Managed web/compatible WebJobs; Always On, recycle/scale and private-tier controls; app Stop vs eligible Premium plan-stop preview distinct | Future alternative; no reason to migrate the current private workflow now |
| **VM** | Single compute/disk/backup/access/log/registry baseline, existing authority reuse; size/quotes UNVERIFIED | Operator OS/TLS/backup ownership, one host/lane and tested restore, vertical scaling, no HA claim | **Recommended initial private Azure architecture; AKS_NOT_REQUIRED** |
| AKS | Higher node/platform baseline and document topology changes | Existing query validation reusable; cluster/CNI/volumes/upgrade costs, shared-state problem remains | Reference only; explicit requirement needed before selection |

The [Azure assessment](phase_18_1_azure_deployment_readiness.md#hosting-total-cost-of-ownership-across-operating-patterns) owns the detailed cost matrix/formulas for occasional weekly demos, intermittent 1–5-user demand and always-on availability. Do not assume intermittent traffic means intermittent billing. Local implementation must remain ordinary Docker/HTTP/process/volume configuration; no Kubernetes API or cloud-only queue/storage dependencies. Conditional private-VM verification must prove host reboot/reopen, volume durability/permissions, backup restore, expired authorization/UNKNOWN denial, private TLS routing, costed startup/deallocation/residuals and secret exclusion, not just an image that starts. Container Apps/App Service requires shared-authority migration and cannot be selected as a cheaper substitute by mounting SQLite on Azure Files. Future enterprise scaling may use Container Apps/Jobs plus shared services without AKS; it is deferred beyond this implementation scope.

Implement only the proposed operator API table and DTO/error contracts in [frontend architecture](phase_18_1_frontend_integration_architecture.md#proposed-http-contracts--not-implemented): context/catalog, session select/start/status/publish/digest/question/cancel/close, and emergency stop. This linked table is the single contract authority; do not create a second route vocabulary. Keep all paths in the existing `/documents/` protected class, typed extra-field-forbidding requests, safe fixed-path ordering and current middleware byte limits. Existing `/documents/analyze`, usage/sharing/deletion/memory/query routes remain compatible.

Introduce a narrow trusted composition module, operator-workflow service and HTTP adapter. Instantiate `SecurityRuntime` once; supply the same authority/governance/admission objects to pilot, publication and analysis. Construct source/session approval records from explicit operator fixture provisioning, never browser claims. Serve only enrolled owning operators. Generic OIDC test keys issue real test access tokens with the existing verifier contract; never call `_verified_principal` from a production HTTP path. Service boot must reject fixture issuers/providers under production configuration. Environment-provided paid credentials must not activate or be read by the fixture runtime. Test the public factory/readiness paths as well as button handlers.

The default local profile must use fake provider HTTP responses, fixture-marked structured execution and synthetic vectors/embeddings with transport instrumentation. Reuse the production extraction/job/digestion/publication/analysis paths and fixture ideas in [pilot helpers](../../tests/pilot_helpers.py), but do not import `tests` into production modules. If a demo fixture provider is necessary, place it in an explicit development-only adapter with production startup rejection. No silent synthetic fallback in an actual inference configuration.

Add a private action-intent database only for owner/session/action payload hashes and accepted operation IDs, with explicit initialize/reopen semantics. It must not become a second identity, job or financial ledger. Browser rerun, reconnect and HTTP retry use accepted job/generation/answer IDs. A pending uncertain call is reconciliation-required, never re-executed to manufacture idempotency. Existing pilot limits remain unchanged: maximum three total sessions, one open job, 1 MB source, four native pages, 4,000 extracted characters, three synthesis attempts, three questions/six overall attempts, 24,800 input and 3,000 output reservations, 60 s provider and 600 s workflow deadlines; actual compatible plan/capability limits may refuse smaller files too. No automatic reset to extend the demo.

Protect digest/answer/status response release against authority revocation, session close/expiry and generation cutover. Integrate with the actual ASGI send boundary, not only the point where a Python method returns. Preserve bounded send timeouts and no upstream call while holding authority transactions. Avoid browser/UI response caches; every protected rerender reauthorizes. Add minimized scope-filtered usage projection rather than returning raw authority databases.

For Stage 18.2 **leave `/documents/analyze` unconfigured/fail closed in the document-demo profile** and use the session questions route, reusing `DocumentAnalysis` through the pilot internally. Preserve existing authorized-analysis behavior in separately composed profiles. Direct API requests therefore cannot obtain extra calls beyond the pilot. Extend readiness with an explicit document-demo runtime branch: require the operator workflow/authorities/runner and configured fixture dependencies to be healthy, permit an empty not-yet-published catalog as idle, and require active replicas only when publication exists. Legacy readiness outside that explicit profile remains unchanged. No provider probe may be billable. Establish generation load outside request retrieval. Private operators publish explicitly; ordinary users receive no publication-management role.

## Browser, local environment and recovery — NOT IMPLEMENTED

Keep legacy Chat behavior in its supported local/static configuration; the OIDC Documents profile must not send chat through blocked legacy endpoints. Use separate per-session UI state keyed to backend verified scope; do not cache protected results globally with `st.cache_data`/shared mutable clients. Use forms and stable request keys; refresh/poll reads never start/publish/question. Present named lifecycle states, exact stage/progress and coverage, safe digest sections/qualifications/conflicts/open questions, canonical evidence pane and explicit semantic-support disclaimer. Escape model/source text, prohibit remote content fetch from rendered output and show sanitized categories with request IDs. Cancel, Close, Withdraw, Clear UI and Logout are distinct actions with distinct outcomes.

The local login proof must cover an actual authorization-code redirect/callback, state/nonce, API-audience access token, verified API principal, operator enrollment, identity-cookie versus bearer expiry and secure logout. Require TLS and tested Secure/HttpOnly/SameSite cookie behavior; native exposed tokens are signed browser cookies, not a server-side token vault. A test-only loopback IdP/JWKS/TLS fixture avoids Azure access. Use the existing cryptography dependency for ephemeral **test** keys; do not generate execution approval. Native login compatibility is an early workstream checkpoint: if cookie/token support cannot be made safe in the pinned runtime, report a blocker and revise the assessment decision with operator review, rather than introduce a pasted token or weaken OIDC.

Compose should add only explicit document-profile processes/mounts/secrets/TLS configuration. Separate immutable object directory, private authorities/control/action database directory and bounded scratch; ensure UID 10001 can access intended mounts without changing unrelated filesystem ownership. Keep file permissions and fail-closed reopen behavior. Exclude new `.streamlit/secrets.toml`, token/test-key caches and session state from build context/Git; existing `.dockerignore` excludes `.env`, SQLite, docs/tests and runtime legacy data but does not itself establish exclusion for every new auth file. Do not bake real secrets. No dependency additions beyond justified login support without renewed scope review. No vLLM/CUDA/GPU/OCR package installation.

The runner drives existing steps on one host independently of the WebSocket and API request. Persist dispatch/job truth in the ledger, reconcile after worker crash, and configure lease duration/renewal for the bounded 60-second provider path plus safe commit margin. Simulated long calls prove no stale commit. After restart require fresh operator authorization; accepted checkpoints can resume only with compatible source/profile/model identity and no outstanding UNKNOWN obligations. Stop admission on unavailable database, generation mismatch, exhausted audit or financial uncertainty. Upstream work already started may finish/bill; cancellation is not a refund mechanism. Local quiesced backup captures all authorities/objects coherently; restore must preserve revocation/consumed approvals/unknown financial amounts and remain closed until reconciled.

## Verification matrix — proposed tests, NOT RUN in 18.1

Use `tests/unit/` for projections/parsers/client rules and `tests/integration/` for real local authorities/HTTP/worker composition. Every named case below is a required coverage group, not an asserted count of already passing tests. Reuse current 3,052-test baseline evidence during assessment; Stage 18.2 runs relevant new tests and the regression suite once the implementation is ready. New checks must verify behavior, not mirror code.

| ID | Group and fixtures | Required assertions / acceptance threshold |
| --- | --- | --- |
| T01 | Authentication unit/API negative + local login integration | Valid fixture login reaches verified principal; wrong issuer/audience/tenant/key/algorithm/purpose, ID token, expired/nbf token, duplicate Authorization, app-only/unknown role and unapproved enrollment rejected before document/provider work. Exact Entra profile contract retained |
| T02 | Browser session/cookie/security | Real local callback state/nonce and XSRF/origin protection; secure cookie attributes, token never rendered/logged/localStorage; two isolated browser/session contexts; expiry/logout clears UI and blocks subsequent action. Do not equate mocked `st.user` with login verification |
| T03 | Intake/catalog unit+API | Valid synthetic PDF/text; hash/approval mismatch, expiry, MIME/filename traversal, source URL/owner injection, oversized actual streaming body, encrypted/scanned/layout-dependent/unsupported/malformed input refused. No object/provider side effect after refusal; all policy bounds enforced |
| T04 | Durable action/API integration | Double submit/rerun/reconnect/start replay uses one source/job/action; mismatched payload same key 409; restart between intent and job/publication/result association reconciles safely; no automatic extra call |
| T05 | Worker/status recovery integration | Job counters/stage match ledger; read-only polling causes zero calls; disconnect/reconnect retains job; kill before/after dispatch delivery and after checkpoint; stale leases/fences rejected; fresh authorization required on restart; accepted checkpoints reused |
| T06 | Cancel/stop/close races | Cancel queued/running, repeat close/withdraw/stop, close during provider execution and before send; durable denial before acknowledgment; no unauthorized new calls, accepted result commits or protected output after fencing; settlement/audit/cancellation writes remain permitted and in-flight liability honestly reported |
| T07 | Digest/publication/citation integration | Full `DigestArtifact` presentation; COMPLETE plus coverage 1 required for publish; PARTIAL/FAILED never shown completed; generation/document/version/extraction/span/excerpt binding; forged/stale citation rejected; semantic_support stays not_evaluated |
| T08 | Selected Q&A and authorization negatives | One selected document only in first UI; approved owner answers and insufficient/conflicting/incomplete evidence; cross-owner/tenant/unselected/mixed-owner denial, revocation/generation cutover during response; existing direct analyze route cannot bypass session/attempt controls |
| T09 | Financial/provider negative integration | Every attempted synthesis/Q&A admitted and attributed; exhausted owner/tenant budget/RPM/TPM/concurrency rejects; timeout/429/unknown usage remains accounted; zero automatic paid retry; exclusive slot and six-attempt ceiling; fake settlements labeled synthetic; no live credential read or non-loopback provider attempt |
| T10 | Fault/recovery integration | Database lock/outage/corruption, audit full, missing/corrupt object, vector outage, publication prepare/activate crash, stale replica, provider malformed protocol/timeout/429; sanitized errors, non-ready or honest recoverable status; no false COMPLETE; no silent ledger recreation |
| T11 | Privacy/restore integration | Withdrawal fences presentation; residual inventory/PURGE_PENDING and retained evidence/audit explicit; coherent snapshot/restore with tombstone/revocation/UNKNOWN and consumed marker preservation; rebuild index or fail closed; no fresh allowance on rollback |
| T12 | UI client/unit and Streamlit AppTest/API E2E | Complete fixture source→job→digest→publish→citation→question→closure journey; all required UI states rendered; no error data leaked; response resource cleanup and request timeouts; legacy UI request/NDJSON compatibility unchanged |
| T13 | Deployment/configuration contracts | Compose validates, cached image build succeeds after implementation authorization, credential exclusions/private mounts/UID/single writer verified; fixture production-start rejection; existing Helm contracts pass; explicit dedicated Kind context if live Kind smoke test performed |
| T14 | Observability/readiness integration | Traceable request/job status without content logs/high-cardinality labels; healthy idle versus running/unavailable; dependency/worker stale/UNKNOWN/audit exhaustion visible; readiness/polling cause zero inference and no index rebuild |
| T15 | Full local authenticated browser/API acceptance | Actual UI client over HTTP against secured local API and runner; authenticated login/logout fixture in a browser or supported browser harness plus API transcript, two-session isolation, delayed-response revocation tests and synthetic-only network capture. If browser tooling unavailable, record the browser-login gate unestablished; API-only proof cannot silently satisfy it |

Browser tooling already available should be reused. Streamlit AppTest is useful for presentation but cannot independently prove cookie/TLS/callback behavior. If adding a browser runner is necessary, assess that narrow dependency explicitly instead of installing a large framework for convenience. API E2E can establish service correctness while the real-browser authentication gate remains blocked. Any live provider/Azure tests are outside these required offline cases and need separate approval.

## Focused acceptance gates

No integrated Phase 18 gate is marked PASS by this assessment. Severity C = critical security/financial boundary, H = functional/reliability blocker, M = bounded operational improvement. The operator is accountable for scope/exposure/spend decisions; the engineer supplies reproducible verification. A security/privacy reviewer may be the operator for synthetic private development only; external/sensitive processing requires appropriately qualified review.

| Gate | Current implementation evidence | Missing requirement / severity | Required 18.2 action and verification | Decision-maker / blocker disposition |
| --- | --- | --- | --- | --- |
| Frontend integration | Legacy `ui/app.py`; pilot synthetic Python E2E | No document browser/API integration / H | Required journey/client/adapter; T04/T12/T15 | Engineer + operator; hard local acceptance blocker |
| Authentication | `OIDCVerifier`, security API/Entra tests | Browser login/API-token/cookie/enrollment proof / C | Native login, offline fixture and expiry; T01/T02/T15 | Operator identity owner + engineer; hard local blocker; live tenant remains separate |
| Authorization | `SecurityAuthority`, `AuthorizedAnalysis`, output snapshots | New operator routes and session/publication final release / C | Exact owning operator and guards; T01/T06/T08 | Security reviewer/operator; hard local blocker |
| Document eligibility | Pilot SourceApproval/intake/isolated parser | Catalog/admission UI and approved fixture lifecycle / H | Synthetic-only exact hash selection; T03 | Operator/source custodian; hard local blocker; private sources excluded |
| Durable processing | SQLiteJobLedger/outbox/fences/checkpoints | Runner, reconnect/action replay/recovery / H | Single lane, intent reconciliation and lease safety; T04/T05 | Engineer/operator responder; hard local blocker |
| Digest integrity | `load_digest`, validated COMPLETE/PARTIAL/FAILED | Honest UI/status projection and operator publish / H | Coverage/status gates, complete fields; T07/T12 | Engineer; hard local blocker |
| Citation provenance | Original EvidenceIndex and Citation model | Secure canonical navigation/release / H | Document/version/generation/span tests; T07/T08 | Engineer; hard local blocker; semantic review separately deferred |
| Grounded Q&A | DocumentAnalysis/pilot question synthetic and historical live example | Session-bound browser calls/limits/abstention / H | No legacy shortcut or second unbounded route; T08/T09 | Engineer; hard local blocker; representative live quality deferred |
| Error handling | Existing sanitized API/provider exceptions | New DTO mappings and transport cleanup / H | Bounded categories/request ID, failure presentation; T10/T12 | Engineer/security reviewer; hard local blocker |
| Privacy/retention | Session close, tombstone, conservative inventory/PURGE_PENDING | Notice/residual display and cache clearing / C | Synthetic only, restore/tombstone checks; T06/T11 | Operator/privacy reviewer; hard private baseline blocker; full erasure deferred and blocks sensitive data |
| Financial governance | GovernedExecution, shared RPM/TPM and owner/tenant reservations | All new routes/readiness/factory proof / C | Credential-free fixture default, UNKNOWN retention; T09/T14 | Operator financial owner; hard local blocker; independent live approval still required |
| Reliability | Deterministic Phase 17 jobs/fault tests | Integrated disconnect/crash/rollback races / H | T04–T06/T10/T11; no silent auto paid retry | Engineer/operator responder; hard local blocker; distributed SLO deferred |
| Observability | Prometheus and readiness contracts | Worker/status/idle document readiness and safe projections / H | T14 with counters/status and content-free logs | Engineer/operator responder; hard initial status/readiness blocker; richer dashboards deferred |
| Azure readiness | Phase 16 historical AKS runtime PASS; current state UNKNOWN; VM selected | Current inventory/quote, suitable VM size, private topology, persistence/auth/host recovery proof / C | No required activation; prepare VM B delta and conditional validation; AKS changes only if independently justified | Operator platform owner; hard Azure blocker, not local blocker |
| Cost control | Evaluation policy and historical settlement | Exact current meters/resource/retention scope absent / C | Offline zero external calls T09; conditional dated quote/window/ceiling | Operator financial owner; hard Azure/paid blocker; no spend implied |
| Rollback | Ledger fences/publication CAS and revocation epochs | Whole local state restore/reopen evidence / H | T10/T11, preserve UNKNOWN and output denial | Engineer/operator responder; hard local blocker; distributed DR deferred |
| External exposure | No actual participants; independent review remains 0/2 | Consent/privacy/real identity/quality/production controls / C | Keep exposure disabled, preserve obligations; no local acceptance substitution | Operator + qualified security/privacy/domain reviewers; hard external blocker, outside 18.2 |

## Acceptance thresholds and evidence handoff

All required applicable T01–T15 assertions must pass with no critical/high unresolved findings; no mandatory denial/failure case may be skipped and called success. Record exact counts, durations, fixture/runtime version and commands. Complete at least one **actual integrated local** synthetic source→COMPLETE digest→explicit publication→grounded answer/canonical citation→closed session path, one cancellation path, one PARTIAL/FAILED path and one restart/reconcile path. Every shown COMPLETE must have validated coverage 1; every citation binds original canonical evidence; semantic status remains honest. Capture zero external provider attempts/zero paid calls and zero credential exposure. UI refresh/status polling must cause zero new inference; duplicate actions yield one accepted durable identity. Stop/revoke acknowledged before release must block subsequent protected output. No arbitrary wall-time production SLO is imposed from synthetic fixture timings; status polling must display changed persisted state within its configured 2–5 second interval in a healthy local test, with stale/unavailable displayed on outage.

Run relevant unit/integration/security tests, full regression once at a frozen implementation tree, `git diff --check`, external-cache `compileall`, configured lint/format checks and applicable Compose/Helm/image validation **during authorized 18.2**. No cloud test or real-user input is necessary for local acceptance. Inspect complete diff, conduct separate pre-commit review, fix material findings and preserve evidence. Local completion may explicitly retain cloud/production blockers; it may not retain a mandatory browser-authentication gap and claim authenticated browser completion.

## Rollback and emergency criteria — NOT IMPLEMENTED

Disable the Documents feature/profile and deny new admission on authorization leak, mismatched generation/evidence, duplicated possible provider execution, UNKNOWN settlement, incompatible authority binding, audit exhaustion, data corruption or failed cookie/session isolation. Durable stop/output-denial precedes UI reset. Preserve authorities and objects, never delete ledger rows or consumed approvals. Revert the code/configuration to the previous compatible local profile only after quiescing; do not roll financial/security state backward. Keep legacy routes OIDC-denied even while the new feature is disabled.

On publication failure retain the last consistent generation only if current document/security/session authorization still permits it; otherwise remain unavailable. Restore objects/indexes from accepted manifests and reconcile all authority epochs before serving. A deployment/image rollback is not permission to resurrect old grants, clear UNKNOWN or execute another paid call. For a future Azure test, stop/deallocate only the approved resources after preserving evidence and enumerate continuing retained-service charges; destructive cleanup is a separate decision.

## Stage 18.3 handoff and closure scope

After independently authorized Stage 18.2, Stage 18.3 should document actual implemented behavior/configuration/login setup, local fixture/TLS/run/recovery commands, API contracts, retention and threat limitations, exact tests and costs, operational stop/restore, screenshots/evidence without secrets, and unchanged Phase 17 deferred acceptance. Update README and relevant security/deployment runbooks to implemented capability only; preserve major prompt/report artifacts. Distinguish local completion, any separately approved Azure result and unestablished production readiness. Do not perform new implementation, external-user verification or paid probes to manufacture closure. No implementation prompt is produced in Stage 18.1.

## Implementation status — 14 November 2026

The historical plan above is reconciled against implementation commit
`f7d091ad16a458c4d4a7403e3fe3ad2b47fafc67` and the unchanged
[Stage 18.2 report](../codex/reports/phase_18_2_implementation_and_verification.md).
The [Stage 18.3 report](../codex/reports/phase_18_3_documentation_and_closure.md)
maps every acceptance gate and verification group. Current contracts are in the
[implemented API reference](../operations/phase_18_operator_api.md); proposed
DTO/error fields above must not override actual source behavior.

| Formal stage / boundary | Current status |
| --- | --- |
| 18.1 Assessment | COMPLETE — `PHASE_18_1_ASSESSMENT_COMPLETE` |
| 18.2 Implementation and Verification | ENGINEERING PASS; local integration and offline verification PASS |
| 18.3 Documentation and Closure | `PHASE_18_3_DOCUMENTATION_PASS`; operator administrative acceptance pending |
| Bounded engineering | `PHASE_18_ENGINEERING_COMPLETE_LOCAL_SCOPE` |
| Cloud / production | `AKS_NOT_REQUIRED`; `AZURE_DEPLOYMENT_NOT_PERFORMED`; `PRODUCTION_READINESS_NOT_ESTABLISHED` |

Recorded final verification is **3,128 passed** (2,192 unit / 936 integration,
76 new cases), zero failures/errors/skips/pytest warnings, **1,130.78 seconds**.
Required local T01–T15 pass, including separate actual Chromium/browser and
Docker evidence. Conditional live Kind was unavailable; historical Phase 16 AKS
is not a Phase 18 deployment. Exact-commit
[CI run 43543837534](https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/43543837534)
succeeded. Stage 18.3 inspected preservation/source/documentation without
rerunning regression, activating containers or executing inference.

The required local integration now exists: native fixture login, strict enrolled
operator API, shared authorities, independent local runner, durable actions,
COMPLETE publication, canonical evidence/Q&A, actual-send revocation, closure
and coherent same-path restore. The [local guide](../operations/phase_18_local_document_demo.md)
documents its exact Python/Compose runtime, signed-cookie limitations,
reauthorization, uncertainty, backup and residual retention.

All conditional cloud/execution and deferred production/external requirements
remain deferred at their original boundaries. The candidate remains a private
Linux VM with Docker/persistent storage; no Azure deployment, current pricing,
final VM sizing, real Entra browser authentication, distributed authorities or
production acceptance is established. Human reviews remain 0/2 and actual
external participants 0. The [completion decision](phase_18_engineering_completion_and_deferred_deployment.md)
owns the current local engineering disposition. Exactly three formal stages
remain; no new stage or execution/deployment authority is introduced.
