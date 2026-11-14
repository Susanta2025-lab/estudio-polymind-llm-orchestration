# Phase 18 engineering completion and deferred deployment

Decision prepared **14 November 2026** under the [Stage 18.3 instruction](../codex/prompts/phase_18_3_documentation_and_closure.md). **Local engineering and documentation are complete within the private, synthetic, owning-operator scope. Operator administrative acceptance of this closure remains pending.** No signature, production approval, cloud deployment acceptance or external-user acceptance is inferred.

## Engineering disposition

| Scope | Classification / disposition |
| --- | --- |
| 18.1 Assessment | `PHASE_18_1_ASSESSMENT_COMPLETE` |
| 18.2 Implementation and Verification | `PHASE_18_2_ENGINEERING_PASS` |
| Local integration | `PHASE_18_2_LOCAL_INTEGRATION_PASS` |
| Offline verification | `PHASE_18_2_OFFLINE_VERIFICATION_PASS` |
| 18.3 Documentation and Closure | `PHASE_18_3_DOCUMENTATION_PASS` |
| Bounded Phase 18 engineering | `PHASE_18_ENGINEERING_COMPLETE_LOCAL_SCOPE` |
| Operator administrative acceptance | PENDING operator review of these uncommitted closure documents |
| Initial cloud architecture | `AKS_NOT_REQUIRED` |
| Azure deployment | `AZURE_DEPLOYMENT_NOT_PERFORMED` |
| Production readiness | `PRODUCTION_READINESS_NOT_ESTABLISHED` |
| Subsequent engineering | `SUBSEQUENT_ENGINEERING_PERMITTED`, subject to its own scope/authorization/prerequisites |

Exactly three formal development stages apply: assessment, implementation/verification, documentation/closure. Deferred deployment or external acceptance is an obligation, not another Phase 18 stage. This decision does not begin subsequent engineering.

## Committed baseline and evidence binding

Observed local HEAD and Phase 18.2 implementation commit: **`f7d091ad16a458c4d4a7403e3fe3ad2b47fafc67`**, `feat(documents): implement authenticated local document frontend and verification`. Its parent `f0e420b6a4ab479ffaa166d000d55c91164f154b` is the assessment commit. The Stage 18.2 report's uncommitted/starting-HEAD statements remain historical, not incorrect current-state claims to rewrite.

Read-only GitHub inspection verifies [Estudio PolyMind CI run 43543837534](https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/43543837534), completed/success for the exact implementation SHA, started 2026-11-14 02:00:22 UTC and updated 02:09:45 UTC (9m23s). Job `132290312190` and its imports/tests/Helm/original-Compose/Docker-build steps succeeded. CI was not rerun; the workflow does not run the separate browser harness or dedicated Documents Compose validation.

The commit contains the reported 36 intended files: 12 modified and 24 added. Stage 18.3 began with no tracked/index changes and 28 inherited untracked Phase 17H documents. A direct SHA-256 comparison before documentation edits matched **all 397** entries of the retained Stage 18.2 freeze manifest, whose serialized hash is `628b50100ede0b017961e4cf93db7c6f92630889fc9f5176c661d2fc248ae34c`. All **25** managed-prompt/11 source hashes also match. Final preservation checks distinguish intentional README edits from the unchanged application/test/configuration surface. No implementation change or new verification gap was found within this reconciliation.

## Accepted verification and local capability

The unchanged [Stage 18.2 report](../codex/reports/phase_18_2_implementation_and_verification.md) is the authority for executed verification: **3,128 passed = 2,192 unit + 936 integration**, including **76 new = 29 unit + 47 integration**; **0 failures/errors/skips/pytest warnings**, duration **1,130.78 seconds**. T01–T15 passed in required local scope. Browser runs are separate from pytest counts; intermediate runs are not added. Stage 18.3 did not rerun regression, browser, containers, Helm or inference.

The report records an actual Chromium/native Streamlit authorization-code journey through local TLS/issuer, verified API, enrolled operator, approved source, durable runner, hierarchical v11 synthesis, COMPLETE/coverage 1, explicit publication, original evidence, canonical citation, bounded Q&A, withdrawal/PURGE_PENDING and logout. Cancellation, state/nonce, token expiry while the identity cookie remains valid, browser isolation, missing-object failure, server restart, same-path restore and delayed-response authorization revocation were separately exercised.

Local container verification established UID 10001, secret exclusion, read-only root/private mounts, loopback TLS, idle readiness, denied unauthenticated requests, writer exclusion and restart. The recorded image was 3,042,328,251 bytes, not a fresh Stage 18.3 measurement. Original and Documents Compose configuration, Helm lint/template, compilation and relevant Ruff F checks passed in Stage 18.2. Conditional Kind workload validation was unavailable because the dedicated context refused connections; no remote Azure fallback was used. Historical Phase 16 AKS and Phase 17H actual-model evidence remain separate.

The integrated synthetic HTTP example has three synthesis attempts and one question, four SETTLED synthetic records and zero external provider attempts. Its usage/cost arithmetic is fixture evidence. Historical Phase 17H v11's four real Foundry calls and EUR 0.009675030297596252 local settlement do not authorize another call, certify current pricing or establish this browser profile with real providers.

## Requirements and documentation reconciliation

The [Stage 18.1 frontend decision](phase_18_1_frontend_integration_architecture.md) and [implementation plan](phase_18_implementation_and_verification_plan.md) remain dated design evidence. The [Stage 18.3 report](../codex/reports/phase_18_3_documentation_and_closure.md) maps all seventeen acceptance gates and T01–T15 to retained implementation evidence. Proposed DTO fields and categories were reconciled to current dictionaries/status codes rather than copied as implemented promises.

Current operation is documented in the [local guide](../operations/phase_18_local_document_demo.md), including private initialization, native login, sources, publication, Q&A, controls, original-path backup/restore and retention. The [implemented API reference](../operations/phase_18_operator_api.md) covers all eleven endpoints, strict inputs, exact response names, idempotency, durable side effects, errors and release guards. README, authentication/security, observability and dated deployment/architecture status addenda point to the same scope.

Architecture is preserved: Streamlit → narrow FastAPI workflow → existing pilot/document services → provider-neutral bounded inference. One locked host/process owns the runner and shared security/governance/admission/job/publication/control/action state. Browser state is not document or financial authority. No raw upstream SSE shortcut, ordinary-user publication privilege, generic analysis bypass, unrestricted upload or parallel financial ledger is introduced.

## Operational acceptance limits

Supported startup is `python -m development.document_demo initialize <new-private-root>` then `serve <same-root>`, or dedicated Compose initialization at `/runtime/state`. The browser entrypoint is `https://localhost:9443`; the automatic synthetic issuer on 9444 and internal loopback API/UI are private development infrastructure. Fixture approvals expire roughly one hour after initialization, API tokens after 15 minutes and TLS after two days. These are development-only values.

Restart requires fresh operator authentication/Start replay for permitted continuation and replica reload. Unknown execution/action outcomes require trusted reconciliation, not automatic repeat inference. The backup command copies a stopped, coherent runtime; restore is a trusted whole-tree copy at original absolute paths, preserving consumed approvals, security revocations, financial obligations and immutable artifacts. Arbitrary stale-backup recovery, distributed disaster recovery, HA and physical erasure are not established.

Native signed, browser-readable identity/token cookies are not encrypted opaque server sessions. Local protocol/cookie/PKCE verification is not real Entra or production authentication. Logout does not revoke every copied bearer token; durable authority/session revocation is decisive. Already delivered information cannot be recalled. Closure and any supported logical metadata retirement remain distinct from erasure; `PURGE_PENDING` is not deletion. Public/confidential workloads need additional independent security/privacy review.

## Cloud handoff and remaining engineering

**AKS was previously validated during Phase 16, but is not required for the initial Phase 18 document application deployment.** `AKS_NOT_REQUIRED` remains approved. The candidate is one small private Linux VM with Docker and persistent local storage. Nothing was provisioned or deployed by Phase 18.2/18.3. Current regional pricing, final aggregate memory/storage sizing, Azure identity/networking, real Entra browser login, production backup/recovery, monitoring/availability, public access and distributed authorities are not completed.

Any later deployment needs a separately reviewed resource, security, cost and authorization plan, including exact SKU/current prices, private access/TLS, persistent path/locking guarantees, host patching, secret custody, reboot/restore, limits and named shutdown/residual-cost responsibilities. Existing production settings still require external OpenAI-compatible inference, Redis, Chroma HTTP, authentication, disabled docs and offline model artifacts; the synthetic profile cannot be relabeled production. The historical two-replica static-token Helm chart is not a document deployment recipe.

Remaining scopes are independent:

- **Real-provider application use:** reviewed bound execution-permission integration, eligible sources/transmission/retention, current provider/capability/catalog/quota, credential and any required independent per-execution approval, uncertainty reconciliation and representative quality evidence. Environment variables alone do not authorize it.
- **General uploads:** a separately designed ordinary-user intake boundary, source rights/classification/privacy, pre-intake limits, quarantine/parser/hostile-file controls, ownership and lifecycle/erasure evidence. Existing parser resource containment is not a hostile-file sandbox.
- **External-user verification:** applicable quality, identity, consent/privacy/retention, participation/exposure and financial gates, actual supervised observations, reconciliation and explicit acceptance. Synthetic demonstrations do not satisfy this.
- **Production multi-user operation:** ordinary-user roles, reviewed token/session architecture, shared transactional/distributed authorities and dispatch, cross-host release/revocation/restore, isolation, retention, monitoring, capacity and availability evidence. Container Apps/Jobs remains a future candidate after shared-authority engineering; no new cloud dependency is selected here.

## Preserved Phase 17 obligations

```text
PHASE_17_ENGINEERING_COMPLETE
DEFERRED_PENDING_TWO_INDEPENDENT_REVIEWERS
PHASE_17_FORMAL_CLOSURE_PENDING
PHASE_17I_ENGINEERING_COMPLETE
PHASE_17I_EXTERNAL_VERIFICATION_DEFERRED
PHASE_17I_FORMAL_ACCEPTANCE_PENDING
SUBSEQUENT_ENGINEERING_PERMITTED
```

Independent human review remains **0/2** under the unchanged [human-review register](phase_17_deferred_human_semantic_review.md). Actual external-user verification has not occurred: **0 participants**, per the unchanged [17I deferred obligation](phase_17i_deferred_external_verification.md). Rubrics, accepted outputs, historical financial/model evidence and prior completion decisions remain untouched. Operator approval of Phase 18.2 and authorization of Stage 18.3 do not constitute acceptance of these still-open obligations or a signature on this closure.

All Stage 18.3 changes are documentation only, left unstaged/uncommitted for operator review. No commit or push occurred in Stage 18.3.
