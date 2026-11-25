# CODEX MASTER PROMPT — PHASE 19B
## POST-AZURE DEPLOYMENT READINESS, OFFLINE VALIDATION AND EVIDENCE RECONCILIATION

**Project:** Estudio PolyMind — Provider-Neutral LLM Orchestration Platform
**Repository:** `Susanta2025-lab/estudio-polymind-llm-orchestration`
**Branch:** `master`
**Expected starting HEAD:** `7bf82dc2da4a9f29561a5f493b690502c0090eb0`
**Phase:** 19B — Azure Linux VM Deployment and Real-Model Integration
**Task:** Post-Azure readiness, remaining offline engineering, regression verification,
evidence reconciliation and pre-commit review
**Execution environment:** Local WSL Ubuntu, Python environment and Docker Desktop
**Date:** 24 November 2026
**Azure VM status:** Operator reports VM deallocated
**Live Azure execution:** NOT AUTHORIZED
**Real-model inference:** NOT AUTHORIZED
**Public exposure:** NOT AUTHORIZED
**Git commit/push:** NOT AUTHORIZED in this run

Clean repository copy of the operator instruction, with list/paragraph formatting consolidated.
The supplied instruction governs execution; this copy grants no additional authorization.

# 1. OBJECTIVE AND MISSION

Continue existing Phase 19B without repeating completed work. The operator completed the
controlled private Azure VM foundation, persistent disk, Docker/Compose, image transfer,
service configuration and isolated CPU-only model execution. The five-service production
application has not been activated. Real identity, TLS, provider credentials, governance
configuration and runtime authorities remain incomplete.

Independently inspect and reconcile repository/Azure evidence; identify remaining offline
work; implement only narrow technically justified improvements; execute meaningful local
Docker/security/persistence/integration/regression tests; prepare configuration/procedures
for the next separately authorized Azure session; update Phase 19B reports, architecture,
operations and relevant README; perform engineering self-review and pre-commit review;
leave uncommitted work for operator review.

Maximize verified readiness without Azure activation, real inference, fabricated authority
or historical-authority mutation. Offline implementation readiness, Azure infrastructure
readiness, real-model authorization and production acceptance are separate states; never
collapse them into a single PASS.

# 2. MANDATORY REPOSITORY INSPECTION AND BASELINE PROTECTION

Read complete root `AGENTS.md`; follow architecture/security/testing/Git/Docker/pre-commit
rules and existing conventions. Before edits execute:

```bash
git status --short --branch
git rev-parse HEAD
git log --oneline -5
git diff --stat
git diff --check
```

Expected HEAD: `7bf82dc2da4a9f29561a5f493b690502c0090eb0`. Historically modified files:
README, `docs/evaluation/phase_19_deployment_architecture.md`,
`docs/evaluation/phase_19_implementation_plan.md`, `docs/operations/phase_19_vm.md`.
Historically untracked prompts and corresponding reports:

- `phase_19b_live_deployment_readiness_continuation.md`
- `phase_19b_post_vm_creation_verification.md`
- `phase_19b_ssh_bootstrap_repair_and_revalidation.md`

Inventory actual tracked/untracked/staged state, rather than assuming those observations.
Preserve every pre-existing user-owned change. Never reset/restore/clean/stash/rebase/discard,
overwrite an unread prompt/report, change branches/history, stage/commit/push/tag or modify
unrelated repositories. Investigate/document unexpected HEAD/state before edits; never reset.

Read complete relevant contents of AGENTS, the Phase 19A readiness prompt/report, Phase 19B
offline implementation prompt/report, architecture/implementation-plan/VM guide,
`docker-compose.phase19.yml`, `deployment/phase19/`, Dockerfile and `.dockerignore`, plus
current untracked Phase 19B prompts/reports. Pay particular attention to **Integration Gap
Resolution** in the existing offline report: scoped Chat OIDC and distinct governed Documents
execution permission and tests already exist. Verify current code/evidence; never reopen
superseded GAPs as though that continuation did not happen.

Inspect implementation/tests in security, governance, documents, deployment/phase19, llm,
config, api, ui, tests/unit and tests/integration. Find actual module/test paths; proposed
19A paths need not be implemented paths. Inspect consumers before changing interfaces.

# 3. ESTABLISHED AZURE EVIDENCE — 24 NOVEMBER 2026

Treat supplied terminal observations as **operator-reported executed evidence**. Cross-check
available local reports/command records. Never claim Codex independently reran cloud checks
unless it did so during independently authorized execution.

## 3.1 Azure infrastructure

Recorded deployment: resource group `rg-epolymind`, VM `vm-epolymind-dev`, Spain Central,
Ubuntu 24.04 LTS, `Standard_D2s_v4`, 2 vCPU/8 GiB, 64-GiB OS and dedicated 64-GiB data disk,
no VM public IP, private Tailscale + OpenSSH access. Private VNet/subnet, restrictive NSG and
NAT Gateway supply controlled outbound connectivity. Compose isolation is not proof of a
complete host destination allowlist. Cloud-init SSH ordering was repaired; later reboot
confirmed ssh.service, tailscaled.service and docker.service active, with private reconnect.

## 3.2 Persistent storage

Data disk ext4 at `/srv/polymind`, authoritative filesystem UUID
`c95e5fce-443b-4d90-9160-8b67758f12d9`; UUID fstab validation and subsequent reboot remount
passed. Directories operator 10001:10001, Redis 999:999 and Chroma 10001:10001, all 0700;
operator private/objects/sources also restrictive. Device letters `/dev/sda` and `/dev/sdb`
changed earlier. Never recommend formatting/initialization, repartitioning, filesystem
changes or overwriting existing runtime data. UUID is authoritative.

## 3.3 Docker and Compose

Azure Docker Engine 29.10.0, Compose v5.8.0, linux/amd64. Locally built/static-inspected/
offline-executed image securely transferred/imported:

```text
polymind:phase19-reviewed
sha256:9f386acf8bddcb5d01bb028151caae24b5df604f8a56c00b7b39c7e0f8298c02
source revision: 7bf82dc2da4a9f29561a5f493b690502c0090eb0
application UID:GID: 10001:10001
```

Image includes Phase 19 entrypoints, FastAPI/Streamlit, provider-neutral infrastructure and
offline embedding/cross-encoder artifacts. Models executed without container networking
locally and on Azure. Azure results: NON_ROOT_EXECUTION_PASS, PHASE19_IMPORTS_PASS,
AZURE_EMBEDDING_PASS, AZURE_RERANKER_PASS, PHASE19_AZURE_OFFLINE_RUNTIME_PASS. Nonfatal
Transformers cache_dir deprecation warning is not an application failure without evidence.

## 3.4 Vendor images

```text
redis@sha256:7f7d30b7fdd09467bac58198a1f166dd69789d348d4fe859cccb20e0cf287fbe
chromadb/chroma@sha256:1e0b73a187a28757c572acba508c46f48c9e8b0acaf5c20e6d95cdedce1acdf6
```

Azure digest-pinned Compose validated; api/ui/gateway share the same application image;
Redis/Chroma are the other two services.

## 3.5 Security preflight

Configuration checks PASS: non-root apps, read-only roots, dropped capabilities, HTTPS
loopback binding, internal backend/frontend networks, missing bind mounts fail closed,
five-service syntax. Gateway publishes only `127.0.0.1:9443`. No containers running at
final inventory. These configuration checks do not prove live HTTPS/Entra/network policy.

## 3.6 Canonical deployment path

Root-owned verified pinned configuration staged at `/opt/polymind/docker-compose.phase19.yml`
and `/opt/polymind/compose.env.example`. Repository systemd template is mount-aware and
expects `/opt/polymind`; it was not installed/enabled as an active production service.

## 3.7 Outstanding production inputs

Expected missing paths: `/etc/polymind/compose.env`, `/etc/polymind/secrets/provider`,
`streamlit.toml`, `tls.crt`, `tls.key`; `/etc/polymind/execution-authority`;
`/srv/polymind/operator/deployment.json`, `configuration.json`, `manifest.json`.
Never fill with fake production credentials/approvals. Seven production SQLite authorities
were not initialized; five-service production stack not started. Real Entra/browser,
HTTPS/provider integration and production recovery unverified.

## 3.8 VM lifecycle closure

Operator reports VM deallocated after four-hour compute session, without production startup
or paid inference. This is not fresh Codex API verification. Disk/NAT/PIP may still charge.
Never start/restart/resize/modify/redeploy the VM in this task.

# 4. MANDATORY SAFETY AND ARCHITECTURAL BOUNDARIES

## 4.1 Azure and infrastructure

Without separate explicit authorization, forbid VM start/restart/redeploy; Azure resource,
network/NSG/NAT/DNS/Entra, managed-disk/snapshot/backup mutations; remote SSH; production
Compose startup; remote Kubernetes/AKS operations; new paid services. Historical four-hour
window ended; local source inspection/offline Docker remain permitted.

## 4.2 Secrets and identity

Never retrieve/print/copy/rotate/renew/expose real Foundry keys, Entra secrets/certificates,
provider credentials, TLS/signing private keys, access/refresh tokens or session cookies.
Do not read secrets to see whether configuration might work. New temporary fake credentials
are allowed solely in isolated tests, never production paths.

## 4.3 Financial and provider safety

No real provider request, paid inference, Foundry endpoint probe/discovery/schema/streaming
request, new execution permissions or approval signatures. No invented tariffs, assumed
historical prices/quota/exclusivity, budget changes, resetting UNKNOWN/unsettled obligations,
reusing Phase 17H authority or bypassing admission/accounting. Infrastructure spend does
not authorize model spend. Only ephemeral test-purpose signing in isolated mocks is allowed.

## 4.4 Runtime/storage invariants

Preserve one owned API/runner, persistent exclusive lock, seven separate SQLite authorities,
stable canonical/authority paths, Redis/Chroma persistence, InferenceProvider, reservations/
settlement/UNKNOWN, owner/tenant isolation, durable results/idempotency, explicit initialize
versus serve, fail-closed startup, mount-aware systemd, historical fingerprints/compatibility.
Never auto-initialize missing state on startup or reset/rename/delete DBs to bypass checks.

## 4.5 Local compatibility

Preserve make chat-* and docs-*, Ollama, FastAPI/Streamlit, NDJSON/SSE, RAG/retrieval/routing,
memory/governance/tests. No new DB, queue, Kubernetes workload, GPU/vLLM/runtime or unrelated
dependency.

# 5. STAGE 1 — POST-AZURE READINESS VERIFICATION

Purpose: establish completion, offline work and independent external blockers. Verify
architecture/baseline before implementation edits.

## 1.1 Evidence reconciliation matrix

For each major requirement distinguish implemented repository behavior, historical offline
tests, operator Azure execution, independently reverified local evidence, outstanding input/
authorization and next action. Use PASS/GAP/FAIL/BLOCKED/DEFERRED/UNKNOWN. Placeholders and
proposed tests never earn PASS. Preserve prior results; explain supersession.

## 1.2 Entra/OIDC

Inspect tenant issuer/JWKS, audience/delegated access_as_user, PolyMind.L1Operator, enrollment/
principal binding, native Streamlit login/access-token forwarding, API authorization,
Chat/Documents scopes, expiry/session isolation/cross-owner/tenant denial. Verify Integration
Gap Resolution. Separate defects from missing real configuration; produce exact non-secret
operator inputs. No registrations, consent, login or development issuer production substitute.

## 1.3 Private HTTPS

Inspect deployment/phase19/gateway.py, ui.py and Compose: private origin, TLS cert/key,
protocols, Host/Origin, callback consistency, WebSockets, forwarded sanitization, loopback,
SSH tunnel and missing/invalid certificate failure. Separate TLS contracts from browser trust;
never label a production-looking self-signed certificate complete. Document hostname/SAN/
callback/trust choices without inventing values.

## 1.4 Provider/governance

Inspect settings, factory, runtime, security/execution and consumers. Verify HTTPS
/openai/v1/ candidate, general/summarization mappings, header choice, credential file,
Azure strict output, usage/token bounds, timeout/malformed/429, shared RPM/TPM, approved
catalog, reservations/settlement/UNKNOWN, independent permission and version-1 zero-paid
versus version-2 approval. Run mocks; never invent approved endpoint/tariff/limit/window.

## 1.5 Durable storage

Verify actual seven names and initialization dependencies, deployment/config/manifest,
approved source files, independent trust, Redis/Chroma, schemas, complete reopen, lock,
backup/recovery/integrity. Produce dependency-ordered future initialization runbook. Never
initialize production. Output source-grounded matrix and concise Stage 2 plan; reuse
completed work, do not change code merely to regenerate PASS.

# 6. STAGE 2 — OFFLINE IMPLEMENTATION AND VALIDATION

## 2.1 Verified missing requirements only

For actual defects identify requirement/implementation/consumers, add failing regression
where practical, minimally fix/retest/document. No rewrites or weakened production checks.
Broad redesign becomes BLOCKED with explanation.

## 2.2 OIDC security tests

Use mock transports/synthetic signed tokens/existing helpers. Verify valid scoped identity;
wrong issuer/audience/tenant, missing role/scope, expired/malformed/bad signature; owner
isolation, inactive/revoked authority, absent config/no dev fallback, unauthenticated denial,
Chat/Documents separation, logout/reauthentication never grants execution. Test JWT success
is not real Entra acceptance.

## 2.3 TLS/gateway tests

Use temporary test-only material for valid handshake, Host/Origin allow/deny, WebSocket,
forwarded sanitization, absent cert/key, invalid/unsafe key, endpoint non-exposure and
backend-admin isolation. Keep certificates outside production, preserve actual origin.

## 2.4 Governance/execution tests

Verify v1 cannot authorize paid execution, v2 needs valid independent permission, absent/
expired/revoked/mismatched/replayed permission denies before dispatch, principal/tenant/
source/config/financial bindings, credentials alone insufficient, synthetic permissions
mock-only, authoritative budget/admission, UNKNOWN retention, duplicates/no billable repeat,
restart/no external replay and no alternate Chat bypass. Never sign real approval.

## 2.5 Seven-authority synthetic lifecycle

Use only unique new temporary state: initialize exact schemas, restrictive ownership/modes,
integrity reopen, absent/damaged/truncated/partial rejection, duplicate writer/persistent
lock, durable jobs/results, source/object integrity, accepted replay, Redis/Chroma persistence,
quiesced backup/isolated restore, no reset or paid replay. Never overwrite an older tree or
point tests at historical/production authorities.

## 2.6 Five-service local integration

Inspect existing harness/reports first; avoid redundant expensive workloads. Where needed,
run bounded api/ui/gateway/redis/chroma with no public exposure, real credentials/cloud auth,
external inference route or unrelated container/state mutation. Use dedicated temporary
volumes/networks, cached CPU image/models, real Redis/Chroma, synthetic identity/mock provider,
resource/time bounds. Exercise synthetic authorized operator → approved synthetic source →
durable job → digestion → coverage/provenance → review/explicit publication → canonical
retrieval → grounded question → accepted persistence → replay/reopen. Preserve review/
acceptance; synthetic review never manufactures human acceptance. Confirm zero real calls.

## 2.7 Failure/recovery

Exercise supported missing mount/bind, owner/mode, secret/independent authority, incomplete
SQLite, duplicate writer, absent Redis/Chroma/failed health, interrupted workflow, unsettled
reservation, expired authority, restart/controlled stop, backup/isolated restore. Appropriate
result is fail-closed/unavailable/recovery-required. Never replace state silently. Local
container restart is not Azure reboot/restore acceptance.

## 2.8 Resources/provenance

Review prior measurements; where useful measure startup/memory/CPU/model load/image bytes/
state growth/stop/recovery. Compare actual 2 vCPU/8 GiB, 64-GiB OS/data disks. Azure isolated
retrieval models passed; sustained five-service capacity remains unestablished. Source,
dependency, Dockerfile or packaging edits invalidate old image evidence for changed runtime;
mark rebuild/verify/transfer pending, never claim old image includes new code.

## 2.9 Required validation

Focused first; locate actual files corresponding to:

```bash
python -m pytest -q \
 tests/unit/test_phase19_deployment.py \
 tests/integration/test_phase19_operator.py \
 tests/integration/test_phase19_execution_bridge.py \
 tests/integration/test_document_operator.py \
 tests/unit/test_structured_provider.py tests/unit/test_security_entra.py
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python -m pytest -q
git diff --check
```

Cover affected Chat/Documents/OIDC/finance/provider/persistence consumers. Compile with
external bytecode cache; parse inert Compose; applicable configured lint/type checks;
systemd syntax without install/enable. Respect resources, no installs/uncontrolled downloads/
global prune. Record exact commands/exits/counts/warnings/failures/fixes/retests and unrun
checks/reasons. Never suppress failures or sum overlapping suites.

# 7. STAGE 3 — EVIDENCE RECONCILIATION AND DOCUMENTATION

## 3.1 Prompt

Preserve this clean instruction under
`docs/codex/prompts/phase_19b_post_azure_readiness_offline_validation_evidence_reconciliation.md`.
Inspect before overwriting any existing file; use a single normal repository-relative path.

## 3.2 Report

Create corresponding report under `docs/codex/reports/` with these sections:

1. Executive summary/exact scope.
2. Starting Git baseline.
3. Sources/provenance.
4. Azure foundation outcomes.
5. Storage/reboot evidence.
6. Image provenance/transfer.
7. Pinned Compose/security.
8. Azure offline models.
9. Entra readiness.
10. HTTPS readiness.
11. Provider/governance/permission.
12. SQLite lifecycle.
13. Local topology.
14. Persistence/security/failure/recovery.
15. Resources/limits.
16. Implementation/rationale.
17. Exact regressions/warnings.
18. Self-review.
19. Pre-commit findings.
20. Blockers/approvals/next session.
21. Final matrix.
22. Git handoff.

Separate historical, operator cloud and fresh local evidence. Never infer browser/trust/
real-model acceptance from offline checks.

## 3.3 Reconcile documents

Update README, architecture, plan and VM guide only where necessary. Preserve historical
19A/19B assessments; dated addenda rather than retroactive rewriting. Reflect private VM,
access/storage reboot/Docker/images/pinned parser/Azure ML passes, missing production inputs,
no seven-authority initialization/five-service startup/Entra/paid-provider acceptance and
reported deallocation. Distinguish tracked portable Compose from Azure-staged pinned copy;
assess tests/portability/image resolution before changing tracked image refs.

## 3.4 Next authorized session runbook

- Gate A: exact Entra registrations, private name/certificate/trust, approved source/enrollment,
  provider endpoint/model/caps, credential custody, approved tariff/budget/quota, independent
  permission if inference proposed.
- Gate B: fresh cost/window, exact state/deallocation/restart/cutoff owner, private SSH/network,
  UUID/mount/owners, image/digests and actual outbound controls.
- Gate C: private configuration/modes, source hashes/manifest, independent authority structure,
  initialize only an approved new authority set; never reinitialize existing state.
- Gate D: data services/readiness/persistence, one API/runner, UI/HTTPS, authorized Entra browser,
  unauthorized-operation denial and approved private workflows.
- Gate E: controlled stop/restart, authorized backup/isolated restore, obligations, resources/
  costs, deallocation/power confirmation and residual inventory.

Make separately executable reviewed steps; no Azure action in this run.

## 3.5 Self-review

Review authorization/provider/finance/idempotency/state/local-launcher compatibility,
dependencies/abstractions/tests, misleading PASS, recovery/resource/cost claims and stale
docs. Fix material in-scope findings; record unresolved issues.

## 3.6 Pre-commit

Run status/diff stat/check/name-status; inspect index and untracked separately. Check keys,
credentials/tokens/private keys, env secrets, local machine paths, DBs/logs/archives/test
fixtures in production paths, irrelevant binaries, unrelated changes and unsupported claims.
Inspect final docs/report. Propose only reviewed checkpoint files and message; no stage,
commit or push. Operator authorizes checkpoint separately.

# 8. ACCEPTANCE GATES

1. Baseline preservation: actual Git recorded, existing work intact, no historical authority
   mutation/destructive Git.
2. Offline readiness: contracts inspected, claimed checks executed, missing external inputs
   identified, defaults fail closed.
3. Synthetic integration/recovery: applicable tests prove isolation, valid test authority,
   zero live inference, durable workflow, finance/idempotency/reopen/denial; untested stays
   GAP/BLOCKED/UNKNOWN.
4. Regression: focused/full accurately recorded, local compatibility, failures fixed/reported.
5. Documentation: accurate dated provenance, reproducible new evidence, no live overclaims,
   independent next-session approvals.
6. Git: reviewed diff, no secrets/unrelated artifacts, candidate scope, no commit/push.

# 9. REQUIRED FINAL READINESS MATRIX

Classify separately: Azure foundation, private SSH/Tailscale, ext4/reboot, Docker/Compose,
verified app image, vendor identity, security configuration, Azure offline models (each
PASS/GAP/FAIL); real Entra, production HTTPS, provider, governance pricing/admission,
independent permission, production authority initialization, Azure functional acceptance,
Azure backup/DR (each PASS/GAP/BLOCKED); local synthetic topology, offline regressions,
documentation/reconciliation, pre-commit (PASS/GAP/FAIL).

Configured PASS is not runtime PASS; offline PASS is not Azure PASS; past cloud PASS grants
no new execution.

# 10. FINAL STATUS CONTRACT

End report and response with explicit evidence-derived values:

```text
PHASE19_POST_AZURE_BASELINE_VERIFIED: YES/NO
AZURE_INFRASTRUCTURE_FOUNDATION: PASS/GAP/FAIL
AZURE_VM_DEALLOCATED: OPERATOR_REPORTED/INDEPENDENTLY_VERIFIED/UNKNOWN
AZURE_OFFLINE_RUNTIME_EVIDENCE: PASS/GAP/FAIL
ENTRA_OIDC_OFFLINE_READINESS: PASS/GAP/FAIL
REAL_ENTRA_AUTHENTICATION: BLOCKED/VERIFIED
PRIVATE_TLS_OFFLINE_READINESS: PASS/GAP/FAIL
PRODUCTION_PRIVATE_HTTPS: BLOCKED/VERIFIED
PROVIDER_GOVERNANCE_OFFLINE_READINESS: PASS/GAP/FAIL
REAL_PROVIDER_COMPATIBILITY: BLOCKED/VERIFIED
INDEPENDENT_LIVE_EXECUTION_AUTHORITY: BLOCKED/VERIFIED
SQLITE_SYNTHETIC_LIFECYCLE: PASS/GAP/FAIL
PRODUCTION_AUTHORITY_INITIALIZATION: NOT_PERFORMED/VERIFIED
LOCAL_FIVE_SERVICE_INTEGRATION: PASS/GAP/FAIL
AZURE_FIVE_SERVICE_ACCEPTANCE: NOT_PERFORMED/VERIFIED
REGRESSION_TESTS: PASS/GAP/FAIL
EVIDENCE_RECONCILIATION: PASS/GAP/FAIL
DOCUMENTATION: PASS/GAP/FAIL
PRE_COMMIT_REVIEW: PASS/GAP/FAIL
PHASE19B_OFFLINE_READINESS: PASS/WITH_CONDITIONS/FAIL
PHASE19B_OVERALL_COMPLETION: COMPLETE/WITH_CONDITIONS/BLOCKED
PHASE19C_READY: YES/WITH_CONDITIONS/NO
AZURE_ACTIVATION_AUTHORIZED: NO
LIVE_INFERENCE_AUTHORIZED: NO
PUBLIC_EXPOSURE_AUTHORIZED: NO
GIT_COMMIT_PERFORMED: NO
GIT_PUSH_PERFORMED: NO
```

Do not mechanically assign PASS from this template.

# 11. REQUIRED FINAL RESPONSE

Concise technically complete handoff: baseline/preservation, three stages, reused versus new,
exact files, focused/full counts, Docker/recovery, any future redeploy, real input blockers,
new-session prerequisites, matrix/status contract, Git status and checkpoint message. Never
request credentials/new Azure merely to complete report. No Phase 19C beyond its handoff.

# 12. FINAL EXECUTION INSTRUCTION

Proceed Stage 1 verification → Stage 2 narrow offline fixes/tests → Stage 3 evidence/docs/
reviews. Complete all safely possible local work. For missing input/authority preserve
boundary, record exact blocker, complete independent work, never invent production evidence.
No Azure restart, paid inference, production authorities, stage/commit/push or automatic
Phase 19C. Stop after report and proposed checkpoint for review.

**MISSION: PHASE 19B POST-AZURE OFFLINE READINESS AND EVIDENCE RECONCILIATION.**
