# Estudio PolyMind — Phase 19A: Azure VM and Real-Model Readiness Verification

## Objective

Prepare Estudio PolyMind for its first controlled Azure deployment using a **small Linux VM running Docker Compose**, with subsequent integration of an approved real-model provider.

**This stage is assessment and readiness verification only. Do not implement or deploy Phase 19B.**

Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`

Baseline:
- Branch: `master`
- Expected HEAD: `b48dde4`
- Local pytest: 3,184 passed
- GitHub CI: `44409425956`, successful
- Phase 18 local frontend manually verified, including Q&A persistence and reauthentication

Phase 19 comprises exactly three stages:

- **19A — Readiness Verification** (this task)
- **19B — Deployment and Real-Model Integration**
- **19C — Validation and Documentation**

Preserve our current provider-neutral architecture and avoid unnecessary new services.

---

## 1. Baseline and architecture verification

Read `AGENTS.md`, `README.md`, existing Docker/Compose configurations, application settings, security/governance documentation, and relevant Phase 17–18 completion reports.

Inspect especially:

- `docs/evaluation/phase_18_engineering_completion_and_deferred_deployment.md`
- `docs/evaluation/phase_18_1_azure_deployment_readiness.md`
- `docs/operations/local_applications.md`
- `docs/operations/phase_18_local_document_demo.md`

Verify:

1. Current Chat/RAG and Documents application entrypoints.
2. FastAPI, Streamlit, worker and authentication dependencies.
3. Existing Docker image and Compose compatibility.
4. ChromaDB, Redis, SQLite, object storage, checkpoints and model-artifact requirements.
5. Persistent-directory and filesystem-locking requirements.
6. Single-host writer exclusion and restart/recovery requirements.
7. Configuration differences between local synthetic, local Ollama and production profiles.

Identify exactly which existing components are reusable, require configuration, or present blockers.

Do not treat local demo authentication, synthetic inference or disabled Chat authentication as production-ready.

## 2. Azure VM readiness and cost assessment

Use the previously selected architecture:

**One private Linux VM + Docker Compose + persistent managed disk + controlled HTTPS access.**

Review candidate VM configurations:

- Baseline candidate: 2 vCPU / 8 GiB RAM.
- Compare appropriate burstable and non-burstable Azure SKUs.
- Consider 4 vCPU / 16 GiB only if justified by measured resource requirements.
- No GPU or self-hosted vLLM in this phase.

Check whether the VM can support the required application services, including Redis and Chroma HTTP if mandated by the current production configuration.

Assess application memory, ML model artifacts, disk/image footprint, background worker requirements and potential CPU-credit limitations.

Estimate costs using **current official Azure pricing**, initially comparing suitable options in West Europe, and explicitly state:

- VM hourly and 730-hour monthly costs.
- Eight-hour controlled-validation cost.
- OS and persistent data disks.
- Backup/snapshot charges.
- Networking, public IP if unavoidable, and private access.
- Monitoring/log retention.
- Other necessary resources.
- Residual charges when the VM is deallocated.
- Currency, region, SKU, pricing date and assumptions.

Distinguish stopped versus **deallocated** VM billing.

Do not invent prices. If current official prices cannot be verified, mark them `UNVERIFIED` and identify the missing quote.

Recommend the **lowest-cost configuration that meets verified technical requirements**, not merely the cheapest VM.

Propose a conservative Azure spending ceiling for operator approval; do not assume historical Phase 17 inference budgets authorize Phase 19.

## 3. Deployment architecture verification

Assess the minimal, secure deployment topology:

```text
Authorized operator
        |
 Private HTTPS access
        |
 Azure Linux VM
        |
    Docker Compose
        |
   +----+----------------+
   |                     |
Streamlit              FastAPI
                         |
               Document worker
                         |
          Single-host durable state
                         |
             External real-model
             inference provider
```

Verify and document:

- Private operator access and HTTPS/TLS.
- Real OIDC/Entra integration requirements.
- No direct public exposure of FastAPI, Redis, Chroma, databases or worker ports.
- Persistent local filesystem with appropriate permissions and locking.
- Non-root containers and secret management.
- One authoritative document worker/writer.
- Service supervision and reboot behavior.
- Backup, restore and financial reconciliation.
- Readiness, health checks and bounded logging.
- Required outbound network access.

Verify whether the existing Compose configuration can be adapted narrowly or needs a dedicated Phase 19 deployment profile.

Do not create a new infrastructure framework or distributed architecture.

AKS, Container Apps, Kubernetes migration and multi-replica document workers are **out of scope**.

## 4. Real-model integration readiness

Assess the existing provider-neutral inference interface and OpenAI-compatible adapter.

Use **Azure Foundry/OpenAI-compatible inference as the initial evaluation candidate**, subject to fresh authorization.

Verify:

1. Existing provider adapter and model capability contracts.
2. Requirements for Chat/RAG inference and hierarchical document digestion.
3. Structured-output/schema compatibility.
4. Provider endpoint, deployment identity, authentication and credential custody.
5. Current model deployment availability, region and quota requirements.
6. RPM/TPM admission limits, timeout behavior and cost accounting.
7. Existing governance, authorization, idempotency and financial reconciliation.
8. Restrictions on document classification, external transmission and retention.
9. Whether the same approved deployment can serve both application planes or whether distinct capabilities/deployments are required.

Historical Phase 17H controlled live validation is supporting evidence, **not permission for new inference calls**.

Do not read or display API keys, invoke paid models, renew credentials, modify Azure deployments or change governance databases.

Identify the minimum independent approvals required before any real-model validation in 19B/19C.

Keep local Ollama support intact; do not assume four local Ollama models should run on the small Azure VM.

## 5. Readiness classifications

Use the following verdicts for each requirement:

- `PASS` — verified with evidence.
- `GAP` — requirement is achievable, but implementation or configuration is incomplete.
- `FAIL` — incompatible or unsafe under the proposed design.
- `UNKNOWN` — insufficient evidence to verify.

Produce a concise readiness matrix covering:

- Azure subscription and permissions.
- Suitable VM SKU and capacity.
- Cost estimate and spending controls.
- Docker/Compose deployment.
- Chat/RAG service readiness.
- Documents service and worker readiness.
- Persistent storage and backups.
- HTTPS and authentication.
- Secrets and network isolation.
- Real-model provider readiness.
- Governance and admission controls.
- Restart and recovery.
- Deployment and validation test plan.

Separate readiness for **private synthetic cloud validation** from readiness for **real-model execution** and **public production deployment**.

Do not classify the complete stage as `PASS` merely because CI and local tests pass.

## 6. Phase 19B implementation plan

Based on verified findings, prepare a minimal implementation plan.

Specify:

- Required Azure resources and their estimated costs.
- Exact repository files likely to change.
- Necessary Docker/Compose adaptations.
- Required persistent volumes and service dependencies.
- Security and credential prerequisites.
- Proposed startup and shutdown procedure.
- Synthetic deployment smoke tests.
- Controlled real-model validation gates.
- Backup/recovery validation.
- Rollback and resource-deallocation procedure.

Distinguish tasks that can be implemented without Azure spending from tasks that require explicit operator approval.

Do not implement this plan.

## 7. Allowed actions and restrictions

Allowed:

- Read-only repository and documentation inspection.
- Local configuration validation.
- Targeted offline checks when useful.
- Read-only public Azure pricing research.
- Existing local Docker inspection if necessary and non-destructive.
- Read-only cloud inventory only if already authenticated and explicitly authorized.
- Creation of the requested Phase 19A documentation.

Forbidden:

- Azure provisioning or modification.
- VM creation or activation.
- Paid inference calls.
- Credential renewal or authentication attempts.
- Changes to production configuration or governance authorities.
- Modification or deletion of existing runtime state.
- Backend/frontend feature implementation.
- New dependencies without justification.
- Git commit, push, reset, stash or clean.

Preserve the clean baseline and all existing functionality.

## 8. Deliverables

Create:

1. `docs/codex/prompts/phase_19a_readiness_verification.md` — clean copy of this instruction.
2. `docs/codex/reports/phase_19a_readiness_report.md` — assessment, evidence, cost comparison, risks and readiness matrix.
3. `docs/evaluation/phase_19_deployment_architecture.md` — selected VM topology, service dependencies, persistence and security boundaries.
4. `docs/evaluation/phase_19_implementation_plan.md` — bounded Phase 19B plan, acceptance criteria and independent approval gates.

Avoid unnecessary additional reports.

At completion, report:

- Baseline verification.
- Recommended VM SKU and estimated total cost, or precise pricing blockers.
- Reusable versus missing deployment components.
- Real-model readiness and outstanding authorizations.
- PASS/GAP/FAIL/UNKNOWN summary.
- Exact blockers for Phase 19B.
- Files created or modified.
- Tests/checks actually executed.
- Git status and confirmation that no commit/push occurred.

### Final decision

Give separate verdicts:

`PHASE_19A_ASSESSMENT_COMPLETE: YES/NO`

`PHASE_19B_OFFLINE_IMPLEMENTATION_READY: YES/NO/WITH_CONDITIONS`

`AZURE_PROVISIONING_AUTHORIZED: NO`

`LIVE_INFERENCE_AUTHORIZED: NO`

`PUBLIC_PRODUCTION_EXPOSURE_AUTHORIZED: NO`

**Stop after Phase 19A. Wait for operator review before proceeding to 19B.**
