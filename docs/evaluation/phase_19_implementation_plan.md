# Phase 19B bounded implementation plan

Current evidence and conditional runbook: [27 November Gate A review](../codex/reports/phase_19b_operational_evidence_reconciliation_and_gate_a_readiness_review.md).
Earlier dated plans below retain their historical scope; no operational authorization is granted.

Current stage boundary — 21 November 2026: **19A COMPLETE; 19B ACTIVE** for offline
implementation, Azure deployment, live integration and validation; **19C NOT STARTED**
for final documentation and engineering closure. Earlier dated plans below are historical;
the final continuation addendum governs the current execution sequence and approvals.

Prepared in Phase 19A, 18 November 2026, against `master` at `b48dde4`. **Not implemented or authorized to begin.** Phase 19 consists only of 19A readiness, 19B deployment/real-model integration, and 19C validation/documentation. This plan does not add a stage or authorize cloud/inference/public access.

## Proposed implementation boundary

Implement a dedicated single-host Compose deployment over existing image, API/services, operator workflow, one runner, durable authorities and provider adapters. Start with **private Documents-first synthetic cloud validation**, then enable a real provider only after its separate gates. Keep existing local Chat/Ollama and Documents demo commands unchanged. Do not widen accepted document classifications, pilot size limits or ordinary-user privileges.

The current Chat API deliberately denies OIDC and the UI does not forward API credentials. Operator approval of the 19B scope must choose either (a) Documents-first cloud validation while retaining local Chat, or (b) a separately reviewed bounded Chat authorization/governance integration within the agreed 19B change. Do not count (a) as delivering both real-model planes. Do not remove the guard, use ungoverned generation, relabel static auth as Entra or silently broaden into a multi-user redesign. If (b) cannot be implemented without that redesign, report the conflict and preserve the guard.

## Resources and cost decision to approve

Required proposed resources: dedicated resource group/tags; one private Linux amd64 VM, NIC/VNet/subnet/NSG; 64-GiB E6 Standard SSD LRS OS disk and separate 64-GiB E6 data disk; coherent protected managed-disk snapshots; existing approved private client route and explicit outbound path, or separately approved P2S VPN/NAT resources; operator-managed private HTTPS name/certificate. No public IP on the application VM.

Candidate capacity: 2 vCPU / 8 GiB. B2as v2 is USD 0.0864/hour (63.072/730 h; 0.6912/8 h); D2as v5 is 0.104/hour (75.92/730 h; 0.832/8 h). Choose B only after measured credit-baseline/memory/recovery fit; use D if the B CPU gate fails while 8 GiB fits. Neither is qualified yet. Do not move to D4as v5 (0.208/hour) without measured need and approval. No GPU, vLLM or local generation-model installation.

Two E6 disks total USD 9.60/month; illustrative incremental snapshot retention is 20 billed GB × 0.05 = 1.00/month; operations allowance 0.20. A standalone VpnGw1 + Standard NAT + two gateway IPs adds 0.245/hour plus traffic (178.85/730 h). Illustrative all-in totals are **253.259/month B** or **266.107/month D**; eight VM/network hours with disks/snapshots retained a month are **13.9882 / 14.1290**. See the [readiness report's official meter evidence and assumptions](../codex/reports/phase_19a_readiness_report.md#current-official-azure-retail-cost-evidence). VpnGw1 eligibility, actual private-access resources, subscription rate/tax/FX and optional services must be settled before resource approval; a retail row is not capacity/eligibility evidence.

Proposed first infrastructure ceiling: **USD 30**, at most eight allocated VM hours, twelve gateway/IP hours including setup/teardown, bounded storage/snapshots retained 30 days, named owner and alerts at 50/75/90%. This requires gateway teardown or an approved existing route. It is not approved and is separate from the model execution budget. Continuous standalone private access needs a different envelope, provisionally USD 300/month, and its own approval. Explicitly inventory residual charges; deallocation alone is insufficient.

## Work possible without Azure spending, after operator approves 19B

1. Confirm baseline and approved scope. Preserve existing tests/contracts, Ollama support, synthetic demo and all historical authorities. Build an exact configuration inventory of paths, model-role maps, capability versions, issuer/audience/role/scope and pricing/admission identities. Do not copy old production/evaluation databases into a new resettable demo.
2. Add a dedicated Compose profile using the current application image. Define private gateway/UI/API, required Redis/Chroma dependencies, fixed one-runner ownership, data/secret mounts, non-root vendor users, read-only roots, tmpfs sizes, resource/log limits, health ordering and shutdown grace. No dependency framework or new queue. Validate rendered configuration offline without secrets.
3. Add a narrow **non-fixture** runtime assembly with explicit initialize-versus-reopen lifecycle. Supply real `SecurityRuntime`, enrolled operator/source approvals, `LocalObjectStore`, SQLite job/control/action/publication state, actual retrieval encoder/vector adapter/reranker, and provider-neutral bounded execution. Reuse workflow/runner logic; do not modify the demo to bypass production rejection. Acquire the host lock before opening authorities; refuse missing/truncated/incompatible reopen state or missing data mount.
4. Separate runtime capability from fixture labeling in Settings/UI/operator context while preserving existing synthetic defaults and API compatibility. Proposed profile name `operator` is a design choice, not an existing supported value. Paid operation cannot retain `SYNTHETIC_FIXTURE`, `synthetic=True` usage, `zero_paid_execution=True` approval semantics or the default fixture permission. Design the smallest explicit live permission extension; require exact trusted configuration binding before every possible call. Keep historical serialized fingerprints stable or explicitly version changes.
5. Configure real browser OIDC: exact private HTTPS callback/origin, tenant-specific Entra verifier, delegated API scope/audience/role, native login access-token forwarding, enrollment and controlled secret/cookie custody. Test with synthetic identity transports before touching Entra. Confirm ID-token substitution, wrong audience/scope/role, revoked principal, expired token, logout/reauthentication and concurrent browser isolation deny correctly. A new cloud app registration or consent is a later administrative approval, not an offline action.
6. Integrate the independent execution-permission port with the retained authorization mechanism, shared financial/admission authority and replay protection. Do not directly turn a historical CLI packet into an unattended web permission or create a parallel budget. Exact approval, schema/capability/source/configuration and time-window bindings need review. Default-deny until fresh live approval is present; cloud synthetic mode has no provider credentials or paid egress.
7. Run a no-network capacity rehearsal on a dedicated disposable state tree with the final image/service set and actual pinned retrieval models. Measure process/cgroup/host peak memory, startup/rebuild/digestion CPU, index/state size, disk usage and shutdown/recovery. Proposed 8-GiB gate: total below 6 GiB, no OOM or sustained swap, at least 20% disk free and bounded readiness/worker latency. B-series must pass sustained credit-baseline CPU, not a short burst test. Do not manufacture an aggregate benchmark from isolated fixture RSS.
8. Add mount-aware host service supervision and bounded backup/recovery/deallocation procedures; test using fake commands/local dedicated resources. Keep all startup/deployment logic short and reviewable. No Azure provisioning script needs to run to make this change reviewable.

### Exact repository files likely to change

These are proposed paths for 19B, not files created by 19A. Final diff depends on approved scope; avoid editing every listed file merely because it is listed.

| Paths | Narrow purpose |
| --- | --- |
| New `docker-compose.phase19.yml` | Explicit private synthetic/real deployment selection, dependencies, mounts, limits, health/restart/log settings; no automatic live inference startup |
| New `deployment/vm/runtime.py`, `deployment/vm/app.py`, `deployment/vm/__main__.py` | Small non-fixture single-host assembly, lifecycle/lock, application factory and explicit maintenance/start commands; use existing services |
| New `deployment/vm/polymind.service` and gateway configuration under `deployment/vm/` | Mount prerequisite, boot/stop supervision, private TLS/WebSocket forwarding and internal route restrictions |
| `config/settings.py`, `.env.example` | Additive approved operator profile/central configuration; placeholder-only examples, no weakening of production requirements |
| `ui/app.py`, `ui/documents_view.py`, `documents/operator/service.py` | Explicit runtime selection, real operator context/usage labels and auth/session handling; synthetic mode stays truthful |
| `documents/pilot/models.py`, `documents/pilot/execution.py` | Only if required by reviewed live permission/approval semantics; preserve default fixture denial and historical fingerprints |
| `llm/provider_factory.py`, optionally `llm/openai_compatible.py` | Only an evidenced endpoint/header/credential-lifecycle gap; keep provider-specific behavior within infrastructure |
| `Dockerfile`, `.dockerignore` | Only if narrowly needed for gateway packaging/runtime support or new secret exclusion; reuse CPU stack and build cache, no speculative dependency/image optimization |
| `api/app.py`, `graph/nodes.py`, `graph/generation.py`, `graph/streaming.py`, `ui/api_client.py` | **Conditional Chat scope only.** Consumers of governed Chat/auth/streaming; require approved design before changes. Preserve NDJSON and local contracts. |
| New `tests/unit/test_phase19_configuration.py`, `tests/unit/test_phase19_runtime.py`, `tests/integration/test_phase19_operator.py` | Production/fixture separation, lock/reopen, credential denial, shared budget/admission, real labels, readiness/restore and mock-provider contracts |
| Existing `tests/unit/test_security_configuration.py`, `tests/unit/test_security_api.py`, `tests/unit/test_documents_client.py`, `tests/integration/test_document_operator.py` | Meaningful regressions for affected consumers; no live credentials/services in offline tests |
| `docs/operations/phase_19_vm.md`, README and these Phase 19 evaluation documents | Implemented setup/operations, actual approved boundaries; 19C records final acceptance evidence and limitations |

Do not change `docker-compose.yml`, `docker-compose.documents.yml`, local launchers, governance policies/catalogs or database schemas unless a verified dependency makes it necessary and it is part of the reviewed scope. No existing authority mutation is part of offline implementation.

## Independent approval gates

| Gate | Required evidence / independent operator decision | Blocks |
| --- | --- | --- |
| A0 — 19B scope | Review 19A, select Documents-first versus approved bounded Chat integration, agree exact files/semantics | All 19B work; no automatic continuation |
| A1 — Azure resource/spend | Named subscription/resource group/operator, permission/policy/SKU quota, final region/resources/rates/billing currency, ceiling/window/retention/residual owner and private access/egress | Provisioning, resource activation or new paid services |
| A2 — Identity/network administration | Real Entra app/redirect/scope/consent/enrollment, certificate/session custody, private route, NSG/host policy, outbound paths | Registration/credential/network changes; operator browser use |
| A3 — Provider and data | Exact model/deployment/version/type/region, endpoint/header/auth custody, verified capabilities/context/schema/streaming/usage, current quota/shared consumers, eligible source hashes/rights/classification/transmission/retention | Any external provider transmission, including synthetic content |
| A4 — Model financial authority | Current applicable token tariff/FX/additional fees, independent model ceiling and exact request/token/time bounds, existing obligations settled/reconciled, reviewed shared authority binding | Paid inference; infrastructure budget grants none |
| A5 — Per-execution permission | Fresh authenticated/enrolled operator and configuration-bound independent approval/signature/replay consumption where required, approved source/profile/window, current policy, fail-closed uncertainty handling | Each controlled real-model validation intent; historical Phase 17 signatures grant none |
| A6 — Acceptance/public exposure | 19C evidence and applicable independent quality/privacy/security/external-user acceptance, explicit new public exposure authorization | Public launch or claim of production acceptance |

These are separate decisions, not a requirement for six different people. Preserve existing documented independent signer/reviewer requirements where they apply. Do not renew credentials, consume old approvals or reset budget/consent state during preparation. Existing 0/2 Phase 17 reviews and deferred external-user verification remain recorded obligations.

## Startup and private synthetic smoke tests

After A0 and offline acceptance, and only after A1/A2 for Azure work:

1. Verify exact subscription/resource scope and approved private path; provision only the reviewed resources. Confirm no VM public IP, no public app/service ports and an explicit outbound method. Verify shutdown/deallocation owner and deadline before starting.
2. Attach/mount disks and verify local filesystem/lock semantics, stable paths, numeric owners/private modes and image digest. Transfer the prebuilt image through the approved path. Create or reopen the new Phase 19 runtime deliberately; never run initialize on an existing authority. Mount secrets read-only, without printing rendered credential values.
3. Start Redis/Chroma and verify protocol health, persistence and resource limits, then the single locked API/runner, UI and private HTTPS gateway. Distinct internal ports if both planes are explicitly enabled. Keep Uvicorn workers at one, reload off. Synthetic mode has no inference secret and cannot reach paid endpoints.
4. Test private HTTPS/WebSockets and real operator login if A2 is satisfied; deny unauthenticated/wrong-tenant/wrong-role requests. The localhost automatic issuer must never be network-exposed as a substitute. Probe liveness and component readiness separately; an empty/mismatched index must stay unready.
5. Exercise approved fixture source selection → create/replay → start → bounded digestion → COMPLETE/coverage/provenance validation → explicit publish → canonical citations → selected-document question → saved-answer replay/refresh/reauthentication → close/withdraw. Assert **zero external model attempts**, truthful synthetic labeling, bounded counters and no duplicate worker/call on action replay.
6. Attempt a second writer against the same mounted authority; it must refuse before effects. Test mount absent, source missing/hash mismatch, exhausted/expired approval, stopped/unsettled financial history and full disk via isolated fixtures, with no authority-reset fallback. Inspect only sanitized logs/metrics.

Private cloud synthetic acceptance needs an actual cloud/private identity/network test; local tests cannot grant it. If this gate fails, stop before supplying provider credentials.

## Controlled real-model integration and 19C acceptance

After A3–A5, verify authorized endpoint/model metadata without generation first. Record current limits and catalog binding without logging credentials. Model discovery is not proof of schema/generation compatibility. Freeze exact source, prompt/profile/schema, role maps, deadline, one serial call schedule and allowed worst-case cost. A small proposed sequence is three synthesis stages plus one question for the tiny accepted fixture, **only if the measured plan actually requires those calls** and the fresh approval binds that exact count. Readiness probes never generate tokens; no exploratory retries.

Use the existing bounded execution path, shared admission/reservation ledger, idempotency keys, raw-result/receipt/checkpoint persistence and full validators. Preserve streaming SSE → provider-neutral tokens → PolyMind NDJSON for any separately approved Chat test. Validate output schema and G1/G2 independently from human semantic usefulness. Record actual usage and compare with the approved catalog/ceiling and later Azure billing evidence. A timeout, missing usage, crash or uncertain response stops further calls until evidence-based reconciliation; do not call again merely to obtain a PASS.

19C validates the deployed image/configuration, actual private browser identity, resources, latency/memory/credits, controlled provider evidence, recovery and cost reconciliation. It updates documentation with observed results and unresolved limits. No number of structural passes constitutes independent semantic acceptance or public production authorization.

## Backup, reboot, rollback and shutdown acceptance

Before any restart/backup, stop new intent/admission, wait for bounded work, inspect unsettled actions/reservations, then stop writers and flush disk state. Snapshot the complete authoritative state/index set with protected custody and evidence of completion. Retain a manifest/digest and exact configuration/path/image identities. A same-disk copy is not the sole backup.

Reboot/startup tests must prove the data disk mounts before application startup, only one writer starts, no empty replacement authority is created, consumed approvals/revocations persist, and no paid call resumes automatically. Require fresh login and authorized replica reload; readiness can remain denied pending reconciliation. Restore into an isolated test location retaining the same container paths, with separate lock exclusion, verify full-tree/database/object integrity and compare against any newer security/financial truth. Never run the restored clone concurrently against the same provider authority or replay consumed permission.

Rollback means stop admission, quiesce, retain full current evidence and switch to the previous compatible image/configuration on the **same** authorities. Do not restore an old financial/security database to undo a bad deployment. If schema/profile compatibility is unproven, remain stopped for trusted reconciliation rather than guessing. Test this path offline and then in the approved synthetic cloud window before real-provider operation.

Shutdown order: close/stop permitted workflow intent, finish or conservatively record uncertainty, stop runner/API/UI/gateway and supporting writers, verify snapshots/evidence, then **deallocate the VM and verify `Stopped (deallocated)`**. Guest shutdown/Compose stop is insufficient for compute billing. Remove only separately approved dedicated gateway/IP resources to end their hourly charges; retain disks/snapshots/financial records for the approved period. Record exact residual resources and owner, review cost after billing lag, and obtain separate disposal approval for retained state. Do not delete unrelated resources, global Docker data or historical evidence.

## Offline and deployment acceptance checks

Run meaningful unit/integration tests for the new composition and all affected contracts, full pytest before a major implementation handoff, compilation with external bytecode cache, `git diff --check`, both existing Compose validations plus the new profile, and a cached Docker build when image/package changes warrant it. Exercise non-root UID/permissions, lock exclusion, actual health dependency behavior, secret exclusion, snapshot/restore, missing mount and boot/restart using dedicated test state. Existing approved local Docker/Kind permissions do not authorize Azure operations.

Before implementation completion, perform separate architecture/compatibility and pre-commit reviews, fix meaningful findings, document actual check counts/outcomes and report Git status/diff statistics. Leave changes uncommitted. Stop for operator review before 19C; record remaining acceptance gates rather than silently expanding scope.

## 19 November 2026 — Phase 19B offline implementation addendum

The initial plan above is retained unchanged as 19A evidence. The user's 19B instruction
authorizes offline implementation and explicitly permits leaving Chat disabled when safe
integration would require substantial redesign. The implemented path is Documents-first,
with production execution blocked rather than expanding authorization semantics.

Completed offline foundations: separate hardened five-service Compose; stable local mount
and complete-authority checks; persistent POSIX writer exclusion; explicit initialize/reopen;
shared Documents HTTP/TLS factories with compatibility re-exports; external Entra-only runtime
assembly; real retrieval adapters; truthful usage/execution labels; runtime credential-file/
header configuration; quiesced backup and isolated restore; focused tests, full regression,
container/resource/synthetic publication and recovery verification; operational instructions.

The independent live permission extension proposed in item 4 remains **not implemented**.
`SessionApproval.zero_paid_execution=True` and historical serialized fingerprints were not
changed. Non-fixture start/question return unavailable, before financial reservations.
A configuration switch cannot enable paid operation. Chat's OIDC guard remains intact.
These are blockers to claiming both application planes support real-model execution.

19C must first receive operator review of those blockers and an accepted bounded authorization
integration, then the original A1–A5 decisions: current subscription/access/egress and identity,
source/provider/capability/quota/tariff, shared authority obligations, budget/window and fresh
execution permission. Real browser Entra/TLS, Azure mount/reboot/restore, model compatibility,
independent acceptance and B2as_v2 CPU-credit/D2as_v5 capacity measurements remain outstanding.
The USD 30 proposal grants no spending permission. The [19B report](../codex/reports/phase_19b_offline_implementation_and_verification.md)
records actual checks and explicit verdicts. Do not automatically continue into deployment.

## 19 November 2026 — Integration Gap Resolution addendum

The continuation implements the two previously deferred execution integrations. Historical 19A
and initial 19B assessments above are preserved. No Azure work or new phase is started.

Implemented: independently verified permission records over the existing action/financial/admission
authorities; a distinct version-2 paid-capable session contract retaining version-1 zero-paid
semantics; selected-session backend execution flags; the existing independent digest/answer review
workflow and durable accepted-result reload; scoped OIDC Chat using the same provider/governance,
LangGraph, canonical hybrid retrieval and conversation memory; native access-token forwarding;
bounded streaming/usage handling and transport-independent intent replay. Production trust and
revocations require a read-only mount; test-purpose records never satisfy the live verifier.

The source, endpoint/deployment-role map, capabilities, exact financial/quota policy/catalog and
application execution scope are configuration-bound. Missing/expired/revoked/mismatched inputs,
insufficient call window and UNKNOWN/unfinished obligations deny external dispatch. No historical
record, signer approval, price, quota or schema was changed. Legacy local Chat and synthetic
Documents remain regression targets.

The [Integration Gap Resolution report](../codex/reports/phase_19b_offline_implementation_and_verification.md#integration-gap-resolution)
records new executed evidence separately from earlier overlapping counts. Both corrected paths are
also exercised in the existing private Compose topology with fake providers and real local
Redis/Chroma/retrieval models. Remaining work is independent operator review and the original
A1–A5 activation gates, real Entra/browser/model/capacity proof and applicable semantic acceptance.
No infrastructure/model budget, live signature, deployment or public-access permission is granted
by this implementation. Do not proceed automatically to Phase 19C.

## 21 November 2026 — Phase 19B live-deployment readiness continuation

The Phase 19B offline foundation is committed at `7bf82dc`; exact-commit CI run
`44805275341` succeeded. Its live-deployment readiness preparation is reclassified as a
dated Phase 19B continuation. The [continuation report](../codex/reports/phase_19b_live_deployment_readiness_continuation.md) records refreshed
retail estimates, actual subscription SKU/quota observations, focused offline verification
and the concrete operator approval packet. A1–A5 remain pending; cloud validation has not run.
Both candidate VM families have zero West Europe quota. Select and authorize a quota remedy
or a separately researched region before allocation; do not substitute another SKU automatically.
The revised current boundaries are 19A Readiness Assessment COMPLETE; 19B Offline
Implementation, Azure Deployment, Live Integration and Validation ACTIVE; 19C Final
Documentation and Engineering Closure NOT STARTED. Earlier dated plans remain historical;
their allocation of execution/validation to 19C is superseded for current work.

The next 19B sequence is: resolve and obtain A1 approval of subscription/resource scope,
region/SKU/quota, private access/egress and spending/window/owners; obtain applicable A2
identity/network administration approval; deploy the approved private five-service VM;
validate real browser/API identity and zero-paid synthetic workflows; measure capacity
and persistence/recovery; obtain independent A3 provider/data, A4 finance/quota and A5
fresh signed permission for an exact serial plan; execute authorized Foundry tests and
reconcile uncertainty, shutdown/deallocation, cost and residual resources. Retain dated
19B evidence throughout. Stop now at the A1 decisions; do not start 19C closure documentation.

## 24 November 2026 — Post-Azure bounded continuation

The later operator evidence establishes the Spain Central private VM/storage/Docker/image
foundation and isolated Azure CPU retrieval-model execution, followed by reported VM
deallocation. It supersedes earlier undeployed-state findings within that scope; no current
West Europe allocation decision or new provisioning is needed. Preserve all historical
reports, including the cloud-init failure and repair. Do not reuse their expired windows.

Offline follow-up adds direct production-gateway TLS tests and per-authority missing/damaged/
partial-state tests, reruns the signed-fixture topology and regression suite, and reconciles
evidence. It changes no runtime or image input and initializes no production authority.
The [continuation report](../codex/reports/phase_19b_post_azure_readiness_offline_validation_evidence_reconciliation.md)
records exact outcomes and unresolved limits. Repeated local passes grant no real identity,
TLS, provider, semantic-review or Azure functional acceptance.

Next follow [Gates A–E](../operations/phase_19_vm.md#next-authorized-session--gates-ae):
operator-controlled identity/name/trust/source/provider/finance/permission decisions;
fresh resource/cost/window approval and existing infrastructure revalidation; reviewed
private files and deliberate new-authority initialization; data services then one API/runner
and UI/gateway under controlled startup; authorized recovery, financial/cost reconciliation
and verified deallocation. Never reformat the UUID-mounted disk or reset an existing database.
Production startup, live inference and public exposure need their independent authorizations.
Phase 19C remains NOT STARTED; this work prepares its eventual handoff only.

## 25 November 2026 — Private HTTPS configuration task within Phase 19B

Repository configuration now selects `PHASE19_ORIGIN=https://polymind.test:9443` and an
inert Streamlit native OIDC template with exact callback
`https://polymind.test:9443/oauth2callback`. Keep SAN `DNS:polymind.test`, Windows mapping
`127.0.0.1 polymind.test`, browser Host/Origin and Windows-native SSH loopback forwarding on
9443 consistent. No gateway/application logic, five-service topology, dependency or authority
schema change is required. The [verification report](../codex/reports/phase_19b_private_https_origin_configuration_and_integration_verification.md)
records fresh offline tests and provenance limitations; historical results above are retained.

Gate A origin selection is resolved in repository templates; the API role assignment is
operator-reported configuration PASS only. Dedicated `estudio-polymind-streamlit-dev`
registration, exact redirect acceptance, browser UUID, delegated permission/consent and private
credentials remain pending. After review, the next separately authorized action is that
registration using the selected exact Web callback. Tenant UUID is still operator-supplied.
No login/token acquisition, VM activation or certificate issuance is authorized now.

The [operator procedures](../operations/phase_19_vm.md#25-november-2026--selected-private-https-origin-and-gate-a-update)
cover duplicate-safe individually reviewed registration, Windows hostname/tunnel, private CA,
server SAN/chain, restrictive file custody and trust removal. Operator must decide CA/leaf
lifetimes, custodians and effective revocation. Actual hosts resolution, browser trust,
API token subject enrollment and production private HTTPS remain unverified. Preserve all
other Gate A source/provider/finance/quota/independent-permission blockers and Gates B–E.

No runtime rebuild/transfer is required to adopt the externally mounted configuration;
new example files change Docker build-context contents but do not alter executable image
behavior. The old Azure image does not contain these new examples. Update the Azure-staged
origin template and provision reviewed external files only in a later authorized session;
preserve the existing pinned Compose/vendor and application image identities. Phase 19A
COMPLETE; 19B ACTIVE; 19C Final Documentation and Engineering Closure NOT STARTED.

## 26 November 2026 — OIDC preparation and next operator action

The operator's 25–26 November evidence resolves browser registration, exact redirect acceptance,
SP creation/enabling, delegated API permission, persisted operator-specific consent and one
client credential's metadata at OPERATOR_REPORTED_PASS level. No tenant-wide consent or new
Graph permission is requested. Do not repeat the earlier registration plan. Historical
findings above remain unchanged.

The [current OIDC report](../codex/reports/phase_19b_streamlit_oidc_configuration_preparation.md)
prepares exact non-secret native configuration, a complete operator-run hidden-prompt/exclusive
private-file procedure, independent cookie generation, optional existing-GPG staging and future
verified Tailscale/OpenSSH handoff. Synthetic local verification and focused regression cover
the procedure and existing contracts. No reusable runtime utility, dependency or image rebuild
is needed. Next action is operator review, then independent private preparation outside Codex.

Actual secret custody/encryption, operational cookie/TOML, Azure installation, CA/leaf/trust,
actual private browser identity and API token sub/enrollment remain unverified/pending/blocked
as classified in the report. Do not invent subjects or initialize authorities. Separate
resource/cost/VM, provider/data/finance/quota and fresh execution approvals remain mandatory;
no VM activation, Entra mutation, real login or inference is authorized by this task.
Phase 19A COMPLETE; 19B ACTIVE; 19C NOT STARTED. Stop at this handoff.


## 27 November 2026 — Complete Gate A reconciliation and conditional execution plan

The [current operational review](../codex/reports/phase_19b_operational_evidence_reconciliation_and_gate_a_readiness_review.md)
supersedes earlier pending descriptions only for the newly reported completed actions:
operational native TOML/cookie generation, encrypted staging/integrity/plaintext cleanup,
approved PKI/root/leaf/CRL and local encrypted CA backup, Windows current-user trust/hostname
resolution, OpenSSH/Tailscale local readiness and dedicated authentication-key verification.
All are OPERATOR_REPORTED_PASS; actual Entra credential validity, independent backup custody/
restoration, manual revocation-risk acceptance and remote/browser acceptance remain pending.
Do not repeat registration, generate another cookie or issue replacement certificates merely
to complete documentation. Preserve the existing cookie and Azure-staged pinned artifacts.

Gate A remains BLOCKED. Its full source/privacy/consent/independent semantic/session,
provider/capability, tariff/budget/shared-admission/obligation and independent execution inputs
are still required. No approved source/hash, token subject, tariff or current permission is
invented. The production API requires enrolled subject/source before initialization, while
standard UI startup depends on API health: review a separate narrow identity-only bootstrap
implementation, not placeholder enrollment or a production initialization workaround.
Execution-disabled Documents startup exists only after real complete inputs; it cannot bootstrap.

Next action is offline operator review of that engineering scope, custody/recovery/revocation
risk and actual approval inputs. The report's conditional Gates B–E prepare fresh resource/
subscription/UTC/cost/cutoff/deallocation/owner authorization; trusted host-key/private network/
UUID/image/staged-Compose/egress revalidation; protected file provisioning with interactive
Windows SSH and a fixed encrypted-TOML receiver (old BatchMode recipe blocked); data service
health before deliberately approved initialization/reuse; no-inference startup/private browser
acceptance; bounded settlement/quiesced backup/recovery and verified deallocation/residual costs.
All commands are PREPARED_NOT_EXECUTED. Production state, real login, Azure and inference are
NOT_AUTHORIZED here. No runtime change/image rebuild from this review. Phase 19A COMPLETE;
19B ACTIVE; 19C NOT_STARTED. Do not start the next phase.
