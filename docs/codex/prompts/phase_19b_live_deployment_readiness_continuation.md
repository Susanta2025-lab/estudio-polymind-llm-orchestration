# CODEX MASTER PROMPT — PHASE 19B — LIVE-DEPLOYMENT READINESS CONTINUATION

## Controlled Azure Deployment, Live Integration and Validation

**Project:** Estudio PolyMind
**Repository:** `Susanta2025-lab/estudio-polymind-llm-orchestration`
**Phase:** 19 — Azure VM Deployment and Real-Model Integration
**Stage:** 19B — Offline Implementation, Azure Deployment, Live Integration and Validation
**Task type:** Deployment readiness, controlled infrastructure validation, authenticated end-to-end verification, governed real-model evaluation, recovery, cost reconciliation and documentation

---

**Stage-boundary correction — 21 November 2026.** This is the corrected operative
Phase 19B continuation prompt. It replaces the uncommitted prompt previously labelled
Phase 19C; historical committed Phase 19A/19B prompts and reports remain unchanged.
The original authorization gates, technical restrictions and validation requirements below
remain in force. This relabelling grants no cloud spending, identity administration,
paid inference or live-permission issuance.

The operator's controlling correction is:

> Phase 19A: Readiness Assessment — COMPLETE.
> Phase 19B: Offline Implementation, Azure Deployment, Live Integration and Validation — ACTIVE.
> Phase 19C: Final Documentation and Engineering Closure — NOT STARTED.
>
> Reclassify the current preparation evidence as a dated Phase 19B live-deployment readiness
> continuation. Preserve all existing observations, PASS/GAP/FAIL outcomes, Azure quota
> findings, spending estimates, and historical Phase 19A/19B records. Correct the current
> uncommitted prompt/report and related documentation. Do not prematurely write Phase 19C
> final closure documentation.
>
> The next Phase 19B work is to resolve the A1 resource, subscription, region, VM quota,
> private access and spending prerequisites, followed by explicitly authorized deployment,
> synthetic cloud validation and separately authorized live Foundry testing. Do not provision
> Azure resources, make paid requests, issue live permissions or modify identities without
> the corresponding independent operator approvals. Do not stage, commit or push Git changes.
> Stop after presenting the corrected plan, the precise A1 blockers and required operator decisions.

## 1. Mission

Continue **Phase 19B — Offline Implementation, Azure Deployment, Live Integration and Validation**, using the completed offline implementation. Phase 19B remains ACTIVE; Phase 19C — Final Documentation and Engineering Closure is NOT STARTED.

The objective is to verify that Estudio PolyMind's existing application can operate securely on a small private Azure Linux VM, including:

1. The existing five-service Docker Compose deployment.
2. Authenticated Chat/RAG with LangGraph, hybrid retrieval, memory and streaming.
3. Authenticated Document Intelligence with hierarchical digestion, publication, citations and selected-document Q&A.
4. Existing security, financial governance, execution-permission and source-ownership controls.
5. Controlled real-model inference through the existing provider-neutral integration.
6. Persistent storage, restart, backup, restore and operational recovery.
7. Measured resource consumption and Azure cost.
8. Dated readiness and validation evidence for the later Phase 19C final documentation and engineering closure. Do not begin that closure now.

**Do not rebuild functionality already implemented and verified in Phase 19B.**

This phase is not a production SaaS launch, unrestricted document-upload service, public deployment, distributed architecture migration or general multi-user expansion.

Beginning Phase 19B authorizes **read-only preparation and permitted local verification**, not cloud spending, provisioning, credential administration, signed live permission issuance or paid inference. Execution must progress through the independent authorization gates below.

---

## 2. Confirmed repository baseline

The operator has committed and pushed Phase 19A and the Phase 19B offline implementation. The expanded Phase 19B deployment/live-validation scope remains active.

| Item | Verified baseline |
|---|---|
| Branch | `master` |
| Expected HEAD | `7bf82dc2da4a9f29561a5f493b690502c0090eb0` |
| Commit | `feat: complete Phase 19B offline Azure deployment foundation` |
| GitHub Actions run | `44805275341` |
| Workflow | Estudio PolyMind CI |
| CI conclusion | SUCCESS |
| CI completion | 20 November 2026 |
| CI build job | SUCCESS |
| Phase 19B final local regression | 3,278 passed, 1 non-fatal warning |
| Phase 19B offline integration | PASS |
| Azure deployment | NOT PERFORMED |
| Live execution authorization | NOT GRANTED |

The CI workflow passed import validation, automated tests, Helm security checks, Compose validation and Docker build.

**Distinguish the reported 3,278-test local Phase 19B result from the GitHub CI result.** Do not claim that CI independently reproduced every browser, container integration or real-provider acceptance test.

Before proceeding:

```bash
git status --short --branch
git log --oneline -8
git rev-parse HEAD
git diff --check
git diff --cached --name-only
```

Read `AGENTS.md`.

Verify the actual local baseline against the expected commit and the successful CI run. If the working tree differs, investigate without overwriting any files.

Do not automatically commit, push, merge, rebase, reset, stash, clean or modify Git history.

---

## 3. Mandatory project-stage policy

Phase 19 consists of exactly three formal stages:

| Stage | Responsibility | Status |
|---|---|---|
| 19A | Readiness Assessment | COMPLETE |
| 19B | Offline Implementation, Azure Deployment, Live Integration and Validation | ACTIVE |
| 19C | Final Documentation and Engineering Closure | NOT STARTED |

Do not introduce Phase 19D or additional formal substages.

Readiness continuation, Azure deployment, real browser authentication, synthetic cloud validation, live Foundry testing, recovery and cost validation remain within **the same Phase 19B**. Dated evidence updates are permitted; Phase 19C final documentation and engineering closure remain NOT STARTED.

If a required approval is missing, report the exact gate and stop the affected action. Continue independently safe, approved work where possible.

---

## 4. Authoritative documents

Before substantive work, read the following committed files completely:

**Phase 19A**

- `docs/codex/prompts/phase_19a_readiness_verification.md`
- `docs/codex/reports/phase_19a_readiness_report.md`

**Phase 19B**

- `docs/codex/prompts/phase_19b_offline_implementation.md`
- `docs/codex/reports/phase_19b_offline_implementation_and_verification.md`

Read the complete **Integration Gap Resolution** appendices, not only the initial Phase 19B findings.

**Architecture and operations**

- `docs/evaluation/phase_19_deployment_architecture.md`
- `docs/evaluation/phase_19_implementation_plan.md`
- `docs/operations/phase_19_vm.md`

**Repository and historical constraints**

- `AGENTS.md`
- `README.md`
- Relevant Phase 17G/17H, Phase 17I and Phase 18 security, governance, evaluation and deployment documents.

Inspect the actual relevant application, deployment and test files.

Current implementation takes precedence over historical proposals. Preserve historical findings and append dated changes rather than rewriting past evidence.

---

## 5. Preserve the completed Phase 19B architecture

Phase 19B delivered a private five-service Docker Compose deployment:

```text
Authorized operator browser
            |
    Approved private access
            |
      HTTPS gateway
            |
    Streamlit application
       /           \
     Chat        Documents
       \           /
       Internal FastAPI
            |
   Single durable runner
            |
  Existing security, governance,
  financial and document state
       /             \
     Redis          Chroma
            |
 Governed provider-neutral inference
            |
 Approved external model endpoint
```

The document runner remains inside the controlled API process; it is not an independently scalable queue service.

Preserve:

- `docker-compose.phase19.yml`
- `deployment/phase19/`
- One locked API/runner process.
- Durable SQLite security, governance, execution, job, action and publication authorities.
- Existing Redis and Chroma implementations.
- Source-bound hybrid retrieval and owner/tenant-scoped memory.
- Existing LangGraph routing and provider-neutral inference.
- The bounded SSE-to-NDJSON streaming contract.
- Independent signed execution permission and revocation controls.
- Explicit financial admission, reservation, settlement and UNKNOWN handling.
- Existing local Ollama, Chat and Documents demo behavior.

Do not substitute ephemeral storage for durable authorities.

Do not migrate to PostgreSQL, Azure Container Apps, AKS, Azure Files, Kubernetes, an external Redis service or a distributed job system as part of Phase 19B.

Such changes require a separate architectural decision outside this bounded validation scope.

---

## 6. Initial Phase 19B readiness verification

Perform read-only verification of the committed Phase 19B release candidate.

### 6.1 Image and deployment consistency

Verify:

- The exact source commit and reproducible image identity.
- The five-service Compose configuration.
- Required environment inputs and mounts.
- Private container networking.
- Non-root execution and filesystem permissions.
- Resource limits, health checks and shutdown behavior.
- Read-only trust/revocation/permission custody.
- Absence of embedded credentials or runtime databases.
- Compatibility with existing Redis, Chroma and retrieval artifacts.

The previously recorded local image SHA is historical evidence, not proof that an Azure image has been deployed.

Prefer immutable image digests over mutable tags.

Do not rebuild images unnecessarily if the existing verified artifact and its provenance are sufficient.

### 6.2 Verify the resolved integration gaps

Confirm the committed implementation of:

**Chat/RAG**

- Real OIDC token verification and native Streamlit access-token forwarding.
- Server-authoritative principal, scope and document authorization.
- Isolated memory and source-bound retrieval.
- Canonical dense/BM25/reranker retrieval.
- LangGraph routing and existing provider contracts.
- Shared financial governance and durable request identity.
- `/query` and `/query/stream` compatibility.
- Bounded streaming and NDJSON responses.

**Documents**

- Non-fixture runtime composition.
- Independent signed execution permission.
- Version-2 execution sessions.
- Immutable version-1 `zero_paid_execution=True` semantics.
- Source, principal, session, model and financial-policy bindings.
- Digest and answer review gates.
- Durable published results and accepted-answer replay.

Do not reopen either previously resolved integration gap without new contradictory evidence.

### 6.3 Capacity evidence

Phase 19B's small synthetic workload is insufficient to certify an 8 GiB Azure VM.

Inspect actual local resource evidence and determine what further measurements are required for:

- Sustained CPU and memory use.
- Startup and embedding/reranker load.
- Redis/Chroma persistence and disk I/O.
- Concurrent frontend responsiveness.
- Worker execution.
- Reboot and recovery.
- Burstable CPU-credit behavior.

Do not infer VM sizing from Docker image size alone.

---

## 7. Azure infrastructure and spending authorization

Before any Azure resource creation, modification, activation or billable action, require **A1 — explicit Azure resource and spending approval**.

Verify the current, actual:

1. Azure subscription and tenant.
2. Resource group and permitted RBAC scope.
3. Region, VM SKU availability and quota.
4. VM, disk, networking, snapshot and monitoring costs.
5. Selected private operator-access method.
6. Outbound connectivity and associated charges.
7. Total approved spending ceiling and evaluation window.
8. Shutdown, deallocation, residual-retention and billing owner.

Candidate VM configurations from Phase 19A:

- `Standard_B2as_v2` — 2 vCPU / 8 GiB, burstable.
- `Standard_D2as_v5` — 2 vCPU / 8 GiB, non-burstable.

Neither SKU has been finally approved or capacity-certified.

The original **USD 30 infrastructure ceiling** is a proposal, not spending authorization. Refresh applicable pricing rather than treating historical estimates as current quotations.

If B-series CPU credits cannot sustain the required workload, compare the D-series candidate using measured evidence.

Do not provision larger machines, GPUs, managed databases, NAT gateways, VPN gateways or other additional paid services automatically.

**Stop condition:** If A1 is incomplete, do not issue Azure mutation commands. Report the missing decision, proposed resource inventory, cost envelope and exact operator action.

A successful CI run does not satisfy A1.

---

## 8. Identity, networking and secret custody

Require **A2 — explicit identity and network administration approval** before the relevant live changes.

Verify:

- Real Microsoft Entra OIDC configuration.
- Correct issuer, audience, JWKS and delegated API scope.
- Native Streamlit browser login configuration.
- Enrolled operator identity and authorization.
- Browser redirect URIs.
- Private HTTPS certificate and hostname.
- Secure browser session/token handling.
- API-side authorization enforcement.
- Secrets and credentials stored outside Git.
- Private VM network access and explicit outbound policy.

Do not expose the VM application through an unapproved public IP or public ingress.

Do not use the development fixture identity provider or its certificates as a substitute for real Entra authentication.

An authenticated browser session alone must not authorize model inference.

Never print, commit or include authentication credentials, private keys, access tokens or signed live permissions in reports.

If interactive authentication, independent identity administration or consent is required, identify the action for the operator. Do not bypass the gate.

---

## 9. Controlled Azure deployment and synthetic validation

**Execute this section only after A1 and applicable A2 authorizations are explicitly recorded.**

Use the existing Phase 19 VM runbook and deployment files. Do not invent an alternative deployment stack.

### 9.1 Infrastructure deployment

Within the approved scope:

1. Provision or reuse only the approved Azure resources.
2. Confirm the intended subscription and resource identities.
3. Verify private access and absence of unauthorized public exposure.
4. Attach the approved durable data disk.
5. Confirm ext4/xfs/btrfs filesystem and required ownership/locking behavior.
6. Establish stable host and container state paths.
7. Transfer and verify immutable application/vendor image digests.
8. Configure approved read-only secrets and permission-trust mounts.
9. Start the existing five services with the documented dependency ordering.
10. Verify liveness, readiness, resource limits and sanitized logs.

Initialization must be explicit and only for a new, approved empty authority.

Never silently create replacement financial/security databases when previously expected state is missing.

Do not enable multiple workers, extra API replicas or automatic model execution during restart.

### 9.2 Private synthetic application validation

Before introducing real-provider credentials, verify:

**Authentication and authorization**

- Browser authentication through real Entra where A2 permits it.
- API-side JWT verification.
- Unauthorized and cross-scope rejection.
- Operator enrollment and source ownership.
- Permission expiry and revocation enforcement.

**Documents workflow**

```text
Authenticate
    ↓
Select approved synthetic source
    ↓
Create durable session
    ↓
Start bounded processing
    ↓
Produce validated digest
    ↓
Apply independent review gates
    ↓
Explicit publication
    ↓
Verify canonical citations
    ↓
Ask selected-document question
    ↓
Apply answer review gates
    ↓
Reload accepted answer
    ↓
Close / withdraw
```

**Chat/RAG workflow**

```text
Authenticate
    ↓
Select permitted execution scope
    ↓
Submit bounded Chat request
    ↓
Authorized routing / retrieval
    ↓
Scoped memory
    ↓
Receive JSON or NDJSON
    ↓
Verify durable intent and replay
```

The synthetic validation must use isolated approved test state and zero paid-provider calls.

Verify that browser refresh, repeated requests and container restart do not trigger duplicate execution.

If the real identity or private deployment cannot be validated, stop before enabling live inference.

---

## 10. Controlled real-model integration

Real-model verification requires separate approvals:

| Gate | Requirement |
|---|---|
| A3 | Provider, model, capability, source and data approval |
| A4 | Independent financial, quota and cost approval |
| A5 | Fresh signed, configuration-bound execution permission |

All three gates must be satisfied independently of infrastructure approval.

### A3 — Provider and source

Verify the actual Azure Foundry endpoint, deployed model, version, region, provider capabilities, structured-output compatibility, streaming behavior, usage reporting and available quota.

Verify source eligibility, ownership, transmission permissions, classification and retention terms.

Do not assume that Phase 17H's earlier model configuration, credentials, quotas or authorizations are still valid.

### A4 — Financial authority

Verify current token pricing, spending ceiling, RPM/TPM, shared consumers, time window and outstanding financial obligations.

Do not create a new financial ledger, reset prior financial truth or erase UNKNOWN records to obtain admission.

### A5 — Independent execution permission

Require a fresh, independently signed, configuration-bound live execution permission with valid scope, principal, session, source, model, policy, amount and timing.

Test-purpose signed permissions are not live authorization.

Version-1 zero-paid approvals must remain non-billable.

### Real-model test plan

Before the first paid request, produce an exact execution plan covering:

- Number and purpose of calls.
- Approved source and output schema.
- Model/deployment identity.
- Maximum input/output tokens.
- Request timeout.
- Aggregate worst-case inference cost.
- Deadline and launch cutoff.
- Failure and uncertainty handling.
- Evidence collection and settlement.

The historical small four-call document workflow may be used as a planning reference **only if the new evaluation independently authorizes its exact calls**.

Do not assume four calls are mandatory or authorized.

Run calls serially through the existing governed execution path.

For any separately authorized Chat test, preserve the SSE → provider-neutral token → PolyMind NDJSON contract.

On timeout, missing usage, truncation, uncertain completion, revocation or financial mismatch:

**STOP further provider execution until trusted reconciliation.**

Do not retry an uncertain request merely to obtain a passing result.

---

## 11. Persistence, recovery and operational safety

Validate the actual Azure deployment against Phase 19B's single-host authority invariants.

Required checks:

1. Missing data disk prevents application startup.
2. A second writer cannot acquire the active authority.
3. Redis and Chroma state survives controlled restart.
4. SQLite authorities and publication state survive reboot.
5. Previously consumed permissions remain consumed.
6. Revocations and financial obligations remain durable.
7. Incomplete/UNKNOWN operations do not automatically replay.
8. Backup uses a coherent stopped-writer boundary.
9. A protected off-disk snapshot or backup can be verified.
10. Isolated restore preserves required identity/path and authority integrity.
11. Rollback does not replace current financial/security truth with stale state.
12. Shutdown and VM deallocation are explicitly verified.

Do not start an isolated restored instance as a concurrent live consumer of the original financial/provider authority.

Do not automatically delete managed disks, snapshots, financial evidence or historical records.

Measure observed recovery behavior and report any unverified RPO/RTO assumptions.

A guest shutdown or stopped Docker Compose project does not prove that Azure compute billing has stopped.

---

## 12. Performance, reliability and cost verification

Collect actual Phase 19B evidence for:

- VM CPU/memory utilization.
- B-series CPU-credit behavior, if applicable.
- Disk utilization and I/O.
- Redis/Chroma readiness and persistence.
- API and Streamlit startup.
- Document processing duration.
- Chat/RAG request latency.
- Real-model latency and usage, where authorized.
- Application errors, restarts and health transitions.
- Actual VM allocation hours.
- Disk, snapshot, network and monitoring charges.
- Provider-token billing and financial-ledger reconciliation.

Use existing diagnostics where sufficient; do not add an observability platform merely for this validation.

Distinguish measured service cost, provisional Azure cost data and final invoice charges.

Record resources that remain billable after VM deallocation.

---

## 13. Regression testing and evidence requirements

Preserve the successful Phase 19B baseline.

Run focused checks for deployment-specific changes and newly discovered integration risks.

Where feasible, verify:

- Current Phase 19 security and financial tests.
- Chat/RAG authorization, retrieval and streaming.
- Documents governance, publication and Q&A.
- Existing legacy local behavior.
- All three Compose configurations.
- Relevant compilation and configuration validation.
- Filesystem permissions and locking.
- Container restart, missing-mount and recovery scenarios.

Do not rerun the complete 3,278-test suite solely to duplicate existing CI evidence when no code has changed.

If Phase 19B requires meaningful application changes, run affected regressions and the full suite before declaring the new implementation verified.

For every validation result, distinguish:

**PASS:** Executed and supported by evidence.
**GAP:** Missing prerequisite or insufficient evidence.
**FAIL:** Executed test contradicts expected behavior.
**NOT EXECUTED:** Not attempted because authorization or conditions were absent.

Never classify a simulated identity, mocked provider or local filesystem test as real Azure/Entra/Foundry acceptance.

---

## 14. Documentation and required deliverables

Save a clean copy of this instruction as:

`docs/codex/prompts/phase_19b_live_deployment_readiness_continuation.md`

Create:

`docs/codex/reports/phase_19b_live_deployment_readiness_continuation.md`

Update existing Phase 19 documents only where the executed results justify changes:

- `docs/evaluation/phase_19_deployment_architecture.md`
- `docs/evaluation/phase_19_implementation_plan.md`
- `docs/operations/phase_19_vm.md`
- `README.md`, where necessary.

Do not create unnecessary parallel runbooks or duplicate historical reports. These are Phase 19B continuation records, not Phase 19C final closure documentation.

The Phase 19B report must contain:

1. Actual repository and CI baseline.
2. Explicit operator approvals and their scope.
3. Azure resource inventory and immutable deployment identifiers.
4. Selected VM and capacity justification.
5. Identity, TLS and network validation.
6. Chat/RAG functional and security evidence.
7. Documents functional and security evidence.
8. Real-provider validation and model execution evidence.
9. Independent quality-review status.
10. Persistence, recovery and rollback evidence.
11. Cost measurements, settlement and residual resources.
12. Test commands and exact results.
13. Failures, corrective changes and unresolved risks.
14. Documentation updates.
15. Implementation self-review and separate pre-commit review.
16. Current validation/readiness matrix and remaining operator decisions; final closure is deferred to Phase 19C.
17. Git status and file inventory.

Record partial results when cloud approvals or access are unavailable. Do not manufacture deployment or model-execution evidence.

---

## 15. Mandatory restrictions

Throughout Phase 19B:

- Do not provision or change Azure resources without A1 approval.
- Do not alter production identity/network configuration without A2 approval.
- Do not transmit content to an external model without A3.
- Do not incur model inference without A4 and A5.
- Do not use expired, historical, revoked or test-purpose approval records for live execution.
- Do not expose the application publicly without separate A6 authorization.
- Do not weaken OIDC, source ownership, financial admission, signed execution permission, idempotency or UNKNOWN handling.
- Do not silently bypass independent digest/answer review requirements.
- Do not upgrade dependency stacks or redesign the deployment without a demonstrated need.
- Do not erase, reset or replace historical authority state.
- Do not perform global Docker cleanup or delete unrelated cloud resources.
- Do not stage, commit or push Git changes.
- Do not infer production readiness from a successful CI workflow or synthetic validation.

Preserve all historical Phase 17 and Phase 18 deferred external-review and acceptance obligations.

**No cloud or paid-model action should be launched based solely on this prompt.**

---

## 16. Continuation status

Report the following independently, using actual evidence:

```text
PHASE_19B_BASELINE_AND_CI: PASS/GAP/FAIL

AZURE_RESOURCE_AUTHORIZATION: APPROVED/PENDING
AZURE_IDENTITY_NETWORK_AUTHORIZATION: APPROVED/PENDING
REAL_PROVIDER_DATA_AUTHORIZATION: APPROVED/PENDING
FINANCIAL_EXECUTION_AUTHORIZATION: APPROVED/PENDING
SIGNED_LIVE_EXECUTION_PERMISSION: VALID/PENDING

AZURE_PRIVATE_VM_DEPLOYMENT: PASS/GAP/FAIL/NOT_EXECUTED
REAL_ENTRA_BROWSER_AUTHENTICATION: PASS/GAP/FAIL/NOT_EXECUTED
CHAT_RAG_CLOUD_VALIDATION: PASS/GAP/FAIL/NOT_EXECUTED
DOCUMENTS_CLOUD_VALIDATION: PASS/GAP/FAIL/NOT_EXECUTED
REAL_MODEL_VALIDATION: PASS/GAP/FAIL/NOT_EXECUTED
PERSISTENCE_RECOVERY_VALIDATION: PASS/GAP/FAIL/NOT_EXECUTED
VM_CAPACITY_VALIDATION: PASS/GAP/FAIL/NOT_EXECUTED
COST_AND_FINANCIAL_RECONCILIATION: PASS/GAP/FAIL/NOT_EXECUTED

PHASE_19A_READINESS_ASSESSMENT: COMPLETE
PHASE_19B_EXECUTION_STAGE: ACTIVE
PHASE_19B_LIVE_DEPLOYMENT_READINESS: READY_WITH_CONDITIONS/BLOCKED
PHASE_19C_FINAL_DOCUMENTATION_AND_ENGINEERING_CLOSURE: NOT_STARTED
PHASE_19_ENGINEERING_CLOSURE: DEFERRED

PUBLIC_PRODUCTION_EXPOSURE_AUTHORIZED: NO
```

Phase 19B validation requires executed evidence for its agreed scope. Completion of offline implementation alone does not complete the expanded stage. Record unresolved acceptance requirements; do not start Phase 19C final closure now.

Successful engineering validation does not establish external-user acceptance, independent semantic certification, high availability or public production readiness.

---

## 17. Immediate stage-boundary correction and stop

The immediate task is documentation correction only:

1. Verify repository/index state and preserve all existing uncommitted work.
2. Reclassify the uncommitted preparation prompt/report as a dated Phase 19B
   live-deployment readiness continuation; correct current documentation links and status.
3. Preserve every observation, PASS/GAP/FAIL outcome, Azure quota finding, spending
   estimate and historical committed Phase 19A/19B record. Keep original test/log paths
   as evidence provenance; do not rerun cloud discovery or tests just to rename a stage.
4. Present the revised stage plan, precise A1 blockers and required operator decisions.
5. Stop. Do not provision Azure resources, make paid requests, issue live permissions,
   modify identities, stage, commit or push. Phase 19C final closure remains NOT STARTED.

The next Phase 19B work is to resolve A1 resource, subscription, region, VM quota,
private access/egress and spending prerequisites. Deployment follows only after explicit
A1 and applicable A2 approval; synthetic cloud validation precedes separately authorized
live Foundry testing under A3–A5. Preserve the existing five-service architecture and
all security, financial, source-ownership and uncertainty controls.

After those independently approved Phase 19B execution/validation workstreams, retain
actual results for later Phase 19C final documentation and engineering closure. No
automatic transition to another stage is authorized.
