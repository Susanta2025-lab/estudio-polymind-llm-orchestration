# CODEX MASTER PROMPT — PHASE 18.1

## Secure Document Frontend Integration and Azure Deployment Readiness Assessment

**Project:** Estudio PolyMind

**Repository:** `Susanta2025-lab/estudio-polymind-llm-orchestration`

**Phase:** 18 — Secure Document Productization and Azure Deployment Readiness

**Stage:** 1 of 3 — Assessment

**Task:** Comprehensive architecture, integration, security, deployment, cost and implementation-readiness assessment

---

# 1. Mission

Conduct a comprehensive, source-grounded assessment of the next major engineering milestone for Estudio PolyMind.

The principal objective is:

**Determine how to integrate the existing document-intelligence backend with an authenticated, usable frontend, and establish the minimum architecture necessary for safe, cost-controlled Azure deployment.**

The project already contains substantial backend functionality.

Do not redesign or rebuild existing capabilities merely because they have not yet been exposed through a frontend.

This is an **assessment-only task**.

It must produce a concrete technical decision and executable Phase 18.2 implementation specification, but must not implement Phase 18 functionality.

## Mandatory three-stage policy

Every project phase has exactly three formal stages:

| Stage | Scope | Status |
|---|---|---|
| 18.1 | Assessment | ACTIVE |
| 18.2 | Implementation and Verification | NOT STARTED |
| 18.3 | Documentation and Closure | NOT STARTED |

Do not subdivide Phase 18 into additional formal development stages.

Architectural workstreams, verification groups and milestones within Stage 18.2 are permitted, but these are not separate stages.

Do not start Stage 18.2 or Stage 18.3.

---

# 2. Repository baseline and project history

Repository:

`Susanta2025-lab/estudio-polymind-llm-orchestration`

Last reported committed baseline:

`faaddc2` — `docs: finalize Phase 17I engineering closure with external verification deferred`

Associated GitHub Actions run:

- ID: `43395472477`
- Workflow: Estudio PolyMind CI
- Reported conclusion: SUCCESS

Verify the actual repository state before proceeding.

Run read-only Git commands:

```bash
git status --short --branch
git log --oneline -7
git rev-parse HEAD
git diff --check
```

Read and follow `AGENTS.md`.

Preserve all existing tracked changes and untracked files.

Historically, the working tree included 28 unrelated untracked Phase 17H prompt/report files. Do not modify, delete or stage them.

Do not assume the working tree is clean merely because the latest commit and `origin/master` match.

## Historical engineering baseline

The relevant completed work includes:

- Phases 1–7: multi-LLM, RAG, LangGraph, memory, routing, FastAPI, Streamlit and Docker.
- Phases 8–15: provider neutrality, OpenAI-compatible inference, Kubernetes/Helm, security and observability.
- Phase 16: previously validated Azure AKS deployment, Foundry, Redis, Chroma/BM25 and application metrics.
- Phase 17B: immutable canonical documents and native extraction.
- Phase 17C: durable local job orchestration and recovery.
- Phase 17D: hierarchical evidence-grounded synthesis.
- Phase 17E: bounded managed inference.
- Phase 17F: authorized publication and canonical citations.
- Phase 17G: reference security, quotas and financial governance.
- Phase 17H: bounded reliability and successful controlled Azure Foundry v11 technical execution.
- Phase 17I: bounded private supervised document verification, all three engineering stages complete.

The Phase 17I Stage 2 report records:

- 3,052 passing automated tests.
- 2,163 unit tests and 889 integration tests.
- 56 new Phase 17I tests.
- Successful synthetic end-to-end document processing.
- No actual external-user verification.
- No new paid inference.

These are historical results, not tests to repeat during this assessment.

## Deferred acceptance

Preserve:

`PHASE_17_ENGINEERING_COMPLETE`

`DEFERRED_PENDING_TWO_INDEPENDENT_REVIEWERS`

`PHASE_17_FORMAL_CLOSURE_PENDING`

`PHASE_17I_ENGINEERING_COMPLETE`

`PHASE_17I_EXTERNAL_VERIFICATION_DEFERRED`

`PHASE_17I_FORMAL_ACCEPTANCE_PENDING`

`SUBSEQUENT_ENGINEERING_PERMITTED`

The project-defined two-human-review requirement remains deferred at 0/2.

Actual Phase 17I external-user participation also remains deferred.

Neither requirement automatically blocks local Phase 18 engineering.

Do not alter or silently close these obligations.

---

# 3. Required repository investigation

Read the current implementation, not merely the README.

At minimum inspect the following.

## 3.1 Existing frontend

- `ui/app.py`
- `ui/api_client.py`
- `config/settings.py`
- Frontend-related tests.
- Relevant container and deployment configuration.

Determine exactly what the existing Streamlit interface supports.

Evaluate:

- Current chat workflow.
- API request construction.
- Streaming response handling.
- Session state.
- Authentication behavior.
- Error handling.
- Source rendering.
- Document-selection capability.
- Upload functionality, if any.
- Processing-status display.
- Digest rendering.
- Q&A integration.
- Citation navigation.
- Sharing and withdrawal workflows.

Distinguish implemented functionality from missing functionality.

Do not assume Streamlit already integrates the Phase 17 document plane.

## 3.2 FastAPI and security

Inspect:

- `api/app.py`
- `api/security.py`
- `security/identity.py`
- `security/runtime.py`
- `security/services.py`
- `security/authority.py`
- `security/models.py`
- Relevant authentication and API tests.

Create an exact route-and-capability inventory.

For each relevant operation, identify:

- Existing endpoint or Python-only interface.
- Authentication method.
- Required permissions.
- Owner/tenant scope.
- Input and output contracts.
- Existing implementation coverage.
- Missing frontend integration.
- Missing public-service composition.
- Security constraints.
- Required new or adapted interfaces.

Pay particular attention to the fact that legacy `/query` and `/query/stream` do not provide a supported shortcut for the OIDC-governed document workflow.

Do not recommend bypassing those protections.

## 3.3 Document-intelligence system

Inspect:

- `documents/extraction.py`
- `documents/storage.py`
- `documents/jobs/`
- `documents/digestion/`
- `documents/publication/`
- `documents/pilot/`
- Relevant tests.

Examine the complete path:

```text
Document admission
       ↓
Canonical extraction
       ↓
Durable job creation
       ↓
Hierarchical synthesis
       ↓
Validated digest
       ↓
Authorized publication
       ↓
Selected-document retrieval
       ↓
Grounded Q&A
       ↓
Canonical citations
```

Identify which components can be reused directly through a secure application service and which require additional adapters, routes, orchestration or deployment work.

Evaluate whether `documents.pilot.SupervisedPilot` should be reused, adapted or kept as a separate operator-controlled verification boundary.

Do not automatically convert this privileged facade into a participant-facing API.

## 3.4 Financial and provider boundaries

Inspect:

- `governance/`
- `llm/admission.py`
- `llm/provider_factory.py`
- Managed synthesis provider configuration.
- Historical Foundry execution reports.

Confirm existing:

- Owner/tenant financial attribution.
- Call reservations.
- RPM/TPM policies.
- Provider concurrency.
- Bounded output reservations.
- Cost settlement.
- UNKNOWN obligations.
- Retry and timeout controls.
- Explicit managed-prompt/11 selection.
- Independent paid-execution authorization requirements.

No frontend action may bypass these controls.

---

# 4. Frontend architecture alternatives

Evaluate at least three realistic alternatives.

### Option A — Extend the existing Streamlit application

Assess the effort required to add:

- Authenticated operator access.
- Approved document selection.
- Restricted document intake.
- Processing progress.
- Complete digest presentation.
- Canonical citation navigation.
- Selected-document Q&A.
- Usage/limit visibility.
- Clear error and cancellation states.
- Session reset and withdrawal.

Evaluate technical compatibility with Streamlit's execution/session model and the existing FastAPI security architecture.

### Option B — Separate dedicated document frontend

Evaluate a dedicated web frontend communicating with secured FastAPI document endpoints.

Only propose a framework such as React/Next.js if its operational or architectural benefits justify introducing another frontend stack.

Assess:

- User authentication.
- Session management.
- Document workflow usability.
- API contracts.
- Streaming/progress delivery.
- Deployment complexity.
- Maintenance burden.
- Security.
- Implementation effort.

### Option C — Minimal private operator application

Evaluate a small controlled browser interface designed only for private, operator-managed document demonstration.

This option should reuse existing backend contracts and minimize new infrastructure.

It may be a reasonable intermediate product experience but must not be misrepresented as a general public service.

## Comparison requirements

Provide a decision matrix covering:

| Criterion | Required analysis |
|---|---|
| Integration effort | Reuse versus replacement |
| Security | Authentication, permissions, session isolation |
| User experience | Document processing and Q&A |
| Reliability | Errors, resume, cancellation and progress |
| Cost | Additional infrastructure and maintenance |
| Local development | WSL, Docker and Kind compatibility |
| Azure compatibility | AKS/private deployment |
| Long-term maintainability | Complexity and future extensibility |
| Time/engineering effort | Relative complexity, with justified assumptions |
| Product readiness | Private demo versus external product |

Choose a **recommended primary option** and explain why.

Do not recommend the most complex architecture merely because it seems more enterprise-oriented.

Prefer minimal sound integration with the existing code.

---

# 5. Define the proposed user journey

Design the desired Phase 18 document experience.

A candidate journey is:

```text
Operator / authorized user
          |
          v
Authenticated application
          |
          v
Approved document selection or intake
          |
          v
Document validation
          |
          v
Durable processing job
          |
          v
Status / progress / errors
          |
          v
Validated digest
          |
          v
Evidence and citations
          |
          v
Selected-document questions
          |
          v
Grounded answers / abstentions
          |
          v
Session closure / revocation
```

Determine exactly which steps can be implemented locally with the existing architecture.

For each step, define:

1. Frontend component.
2. Backend interface.
3. Authentication/authorization boundary.
4. State authority.
5. Persistent data requirements.
6. Error behavior.
7. Cancellation/recovery behavior.
8. Audit and privacy implications.
9. Required tests.

Use source-based names for existing interfaces.

For missing interfaces, describe proposed contracts clearly and label them NOT IMPLEMENTED.

Do not invent existing endpoints.

## Critical usability requirements

The future UI must distinguish:

- Requested processing.
- Queued.
- Running.
- Completed.
- Partial.
- Failed.
- Cancelled.
- Authorization denied.
- Provider capacity unavailable.
- Document unsupported.
- Evidence insufficient.

Do not show a PARTIAL or FAILED digest as COMPLETE.

Citation display must bind to original source/document/generation/span.

A structurally valid citation must not be labeled semantically verified without supporting review evidence.

---

# 6. Security architecture assessment

Design the minimum secure frontend-to-backend boundary.

Evaluate:

- OIDC login/session architecture.
- Operator versus document-user roles.
- Least privilege.
- Issuer enrollment restrictions.
- Owner/tenant authorization.
- Session expiry and logout.
- CSRF considerations for cookie-based authentication.
- Browser token exposure and storage.
- API bearer validation.
- HTTPS/TLS.
- Upload/request limits.
- Cross-document access.
- Publication-generation fencing.
- Safe content presentation.
- Prompt injection.
- Audit data minimization.
- Secret handling.
- Error sanitization.
- Withdrawal and revocation.
- Sensitive/private document restrictions.

Do not grant publication-management privileges to ordinary users.

Do not expose application storage, Redis, Chroma, raw checkpoints, governance databases or Kubernetes administration through the frontend.

Identify security controls that are already implemented and those requiring additional engineering.

Define an explicit **private-demo security baseline** and a stronger **multi-user production security baseline**.

Do not treat those two levels as equivalent.

## Document classes

Determine the safest initial document scope.

Prefer:

- Synthetic technical documents.
- Nonpersonal sample documents.
- Appropriately licensed public materials.

Exclude private, sensitive, proprietary or erasure-dependent documents until the necessary controls are demonstrably implemented and accepted.

Do not infer that access to a public document automatically permits forwarding it to a managed inference provider.

---

# 7. Azure deployment-readiness assessment

The project already completed a previous AKS validation in Phase 16.

Read:

- `docs/codex/reports/phase_16_report.md`
- `docs/codex/reports/phase_17a_report.md`
- `README.md`
- Kubernetes and Helm configuration.
- Existing Docker/Compose configuration.
- Security and deployment runbooks.

Reconcile the earlier successful AKS deployment with the newer Phase 17 document-processing requirements.

**Do not mistake historical deployment success for current live infrastructure availability or Phase 18 readiness.**

The current AKS cluster may be stopped, changed or unavailable.

Unless a safe read-only current inspection establishes otherwise, label current cloud runtime state UNKNOWN.

## 7.1 Compare deployment architectures

Evaluate:

**Architecture A — Local-only product validation**

- Streamlit/FastAPI or selected frontend.
- Existing local reference authorities.
- Local immutable object storage.
- Existing document job implementation.
- Docker or Kind when useful.
- Synthetic inference.

**Architecture B — Private Azure demonstration**

- Reuse the existing AKS architecture where justified.
- Private exposure and least-privilege access.
- Existing managed inference boundary.
- Controlled persistence and limited workload.
- Explicit resource and financial constraints.

**Architecture C — Production-oriented distributed deployment**

- Durable cloud object storage.
- Shared transactional job/security/governance state.
- Distributed worker dispatch and recovery.
- Shared inference admission.
- Durable publication state.
- Operational backup and restoration.
- Multi-user authentication.
- Network isolation and secret management.
- Monitoring and cost control.

Identify which architecture is sufficient for the initial Phase 18 product milestone.

Do not select full production architecture automatically.

## 7.2 Storage, databases and workers

Assess the need and compatibility of:

- Azure Blob Storage.
- Azure Database for PostgreSQL or another justified transactional authority.
- Azure Service Bus versus Storage Queue versus database-backed dispatch.
- Azure Managed Redis.
- Chroma persistence/derived-index reconstruction.
- Worker containers.
- AKS workloads.
- Kubernetes Secrets versus managed secret services.
- Workload identity.
- Backup and recovery mechanisms.

The original Phase 17A architecture identified several of these as proposals, not deployed capabilities.

For each service, state:

- Whether it is required now.
- Whether it can be postponed.
- Which existing interface it replaces or implements.
- Required correctness properties.
- Migration and rollback implications.
- Operational dependencies.
- Expected cost drivers.

Do not introduce Kafka, additional Kubernetes systems or a new vector database without specific justification.

## 7.3 Distributed correctness

Pay special attention to the current SQLite-based authorities.

Assess what changes are required before multiple application replicas or workers can safely share:

- Document ownership.
- Job state.
- Lease/fencing epochs.
- Inference reservations.
- Quotas.
- Publication activation.
- Revocation.
- Generation identity.
- Audit events.
- Cancellation.
- Restore/rollback state.

Do not assume that deploying two replicas makes a single-host design distributed-safe.

Specify required integration, concurrency and failure tests.

---

# 8. Azure financial assessment

This project is developed independently and must remain cost-conscious.

Provide a realistic cost model before recommending cloud activation.

The analysis must include:

### Compute

- AKS control-plane and node costs.
- Minimum node configuration.
- Persistent node hours.
- Idle resource charges.
- Optional smaller private deployment alternatives.

### Data

- Blob storage.
- Transactions and egress.
- Database capacity and storage.
- Backups.
- Redis.
- Vector storage.
- Monitoring/log ingestion.

### AI inference

- Azure Foundry model pricing.
- Input/output token usage.
- RPM/TPM restrictions.
- Potential 429 responses.
- Reservation and retry exposure.
- Existing financial approval rules.

### Operational costs

- Networking.
- Private endpoints/public IP/load balancing.
- Container registry.
- Key management.
- Backup and log retention.
- Resource startup/shutdown overhead.

## Required cost scenarios

Estimate three clearly labeled scenarios:

1. **Offline local development:** no incremental Azure resources or provider calls.
2. **Short-duration private Azure validation:** explicitly limited runtime and calls.
3. **Always-on Azure application:** approximate monthly infrastructure and inference exposure.

Use official current provider pricing where accessible.

Record:

- Source.
- Retrieval date.
- Region.
- Currency.
- Billing unit.
- Runtime assumptions.
- Estimated monthly usage.
- Uncertainty.

If current pricing cannot be verified, provide transparent formulas and **UNVERIFIED** inputs rather than fabricated numerical quotes.

Separate zero-cost development assumptions from actual infrastructure charges.

Do not infer that a stopped AKS workload has zero ongoing associated storage/network/managed-service costs.

No paid execution or cloud activation follows from this analysis.

---

# 9. Reliability and observability assessment

The project already contains meaningful technical validation.

Preserve this evidence without overstating its scope.

Assess readiness for:

- Long-running document jobs.
- Reliable progress reporting.
- Restart and resume.
- Durable checkpoints.
- Provider timeout.
- Provider 429/overload.
- Backpressure.
- Cancellation.
- Worker crash.
- Database outage.
- Vector-store outage.
- Publication rollback.
- Audit exhaustion.
- Unknown financial settlement.
- Backup/restore.
- Multi-replica operation.
- Operator emergency stop.

Determine the minimum observability needed for the initial browser workflow.

Reuse existing Prometheus metrics and readiness contracts where applicable.

Do not recommend a new observability platform unless the current one is demonstrably inadequate.

Keep separate:

- Existing synthetic/offline evidence.
- Historical AKS validation.
- Actual-model four-page evidence.
- Future integrated frontend evidence.
- Unestablished production-scale reliability.

---

# 10. Phase 18.2 implementation definition

Develop a concrete specification for the next implementation stage.

It must be realistic for a single AI engineer working with Codex and existing repository tooling.

Avoid vague deliverables such as "make the application production-ready."

Specify:

- Selected frontend architecture.
- Minimum browser features.
- Required backend interfaces.
- Authentication integration.
- State/persistence decisions.
- Reused services.
- New adapters.
- Protected service composition.
- Local Docker/Kind environment.
- Required fixtures.
- Unit tests.
- Integration tests.
- Security negative tests.
- End-to-end browser or API testing.
- Failure/recovery testing.
- Cost and approval gates.
- Acceptance thresholds.
- Rollback strategy.
- Documentation handoff.

Prioritize the **minimum independently useful frontend-to-backend document experience**.

Classify each candidate item:

`REQUIRED_FOR_PHASE_18_2`

`CONDITIONAL_ON_APPROVED_PRIVATE_AZURE_TEST`

`DEFER_TO_PRODUCTION_HARDENING`

`OUT_OF_SCOPE`

If the assessment demonstrates that both a complete frontend and full distributed Azure productionization are too large or risky for one implementation stage, choose a bounded Stage 18.2 scope.

Do not create new formal subphases to conceal the scope problem.

Keep exactly three stages and record deferred capabilities as future requirements.

---

# 11. Proposed acceptance gates

Define a focused Phase 18 acceptance matrix.

At minimum cover:

| Gate | Required evidence |
|---|---|
| Frontend integration | Actual supported backend operations |
| Authentication | Verified user/operator identity |
| Authorization | Correct owner/tenant and role restrictions |
| Document eligibility | Bounded, permitted source intake |
| Durable processing | Correct job lifecycle and resume |
| Digest integrity | COMPLETE versus PARTIAL/FAILED |
| Citation provenance | Canonical original-source binding |
| Grounded Q&A | Authorized selected-document answers |
| Error handling | No raw exception or credential leakage |
| Privacy/retention | Approved data class and honest residuals |
| Financial governance | No calls outside shared admission/budget |
| Reliability | Deterministic failure/recovery coverage |
| Observability | Traceable document/job/request status |
| Azure readiness | Safe topology, persistence and deployment constraints |
| Cost control | Exact approved resource and usage scope |
| Rollback | Recovery or safe fail-closed behavior |
| External exposure | Separate explicit approval |

For each gate record:

- Current implementation evidence.
- Missing requirement.
- Severity.
- Required Phase 18.2 action.
- Verification method.
- Responsible decision-maker.
- Hard blocker versus deferred improvement.

Do not mark security or production gates PASS solely because old Phase 17 tests passed.

---

# 12. Assessment decisions and verdicts

The assessment must produce explicit answers to these questions:

1. Can existing Streamlit be extended safely, or is a separate document frontend justified?
2. What is the minimum new FastAPI interface required?
3. Can Phase 17I's `SupervisedPilot` be reused without expanding its privileged trust boundary?
4. Which authentication path is suitable for a private browser demonstration?
5. Which functionality can be implemented without Azure?
6. What can be demonstrated with synthetic documents and fake providers?
7. Which actual-model functionality is already evidenced, and what remains unverified?
8. Is AKS necessary for the first integrated browser demonstration?
9. Which production storage/database/queue choices need decisions now?
10. Which infrastructure changes can wait?
11. What minimum Azure resources would a private pilot require?
12. What are the primary recurring cost risks?
13. What controls prevent accidental cloud charges?
14. What should Phase 18.2 actually implement?
15. What is explicitly deferred beyond Phase 18?
16. What evidence would justify private deployment versus public launch?

Provide three independent readiness verdicts:

`LOCAL_FRONTEND_IMPLEMENTATION_READINESS`

`PRIVATE_AZURE_VALIDATION_READINESS`

`PRODUCTION_EXTERNAL_EXPOSURE_READINESS`

Use only:

- `READY`
- `READY_WITH_BLOCKERS`
- `BLOCKED`
- `NOT_ESTABLISHED`

Explain each classification with evidence.

Do not infer production readiness from architectural design alone.

---

# 13. Scope and authorization restrictions

This assessment authorizes repository inspection, offline reasoning, documentation creation and safe read-only verification.

It does not authorize:

- Production code changes.
- New API routes.
- Frontend implementation.
- Container image builds.
- Kubernetes deployment or mutation.
- AKS startup.
- Azure resource provisioning.
- Cloud subscriptions or paid-service activation.
- Foundry inference.
- Provider credential use.
- Live model probes.
- IdP configuration changes.
- Participant onboarding.
- External-user testing.
- Processing private documents.
- Financial ledger resets.
- Increasing provider quotas.
- Generating or consuming RSA execution approval.
- Re-running the full test suite merely for assessment.
- Git staging, commit or push.

Use current GitHub and repository evidence first.

An optional read-only cloud or Kubernetes inspection is permitted only if a suitable already-authorized session is available and no authentication renewal, secret access, resource mutation or billable operation is required.

Do not initiate device-code login or credentials renewal.

If no trustworthy current cloud evidence is available, document the current runtime status as UNKNOWN.

Do not guess whether AKS is running or stopped.

No financial authorization is implied by the existing €5 evaluation policy or earlier successful live calls.

---

# 14. Required assessment deliverables

Create the following documents.

## A. Preserved assessment prompt

`docs/codex/prompts/phase_18_1_assessment.md`

Store a faithful copy of this master instruction.

## B. Main assessment report

`docs/codex/reports/phase_18_1_assessment.md`

Include:

- Executive summary.
- Verified repository baseline.
- Existing frontend/backend capability inventory.
- Missing integration contracts.
- Frontend architecture comparison.
- Selected option and rationale.
- Security assessment.
- Azure deployment alternatives.
- Storage/database/queue decisions.
- Financial model.
- Technical risks.
- Current readiness verdicts.
- Recommended Stage 18.2 scope.
- Remaining approvals.
- Validation and Git status.

## C. Frontend and API architecture decision

`docs/evaluation/phase_18_1_frontend_integration_architecture.md`

Include:

- Existing versus proposed component diagram.
- Frontend comparison.
- Source-to-UI workflow.
- Proposed API contracts.
- Authentication flow.
- Authorization boundaries.
- State and persistence responsibilities.
- Failure/recovery design.
- Explicit compatibility requirements.
- Recommended minimal architecture.

Mark every proposed contract as NOT IMPLEMENTED.

## D. Azure deployment and financial assessment

`docs/evaluation/phase_18_1_azure_deployment_readiness.md`

Include:

- Reconciliation with Phase 16.
- Current versus historical infrastructure state.
- Local/private-Azure/production comparison.
- Durable storage and worker design decisions.
- Identity and network controls.
- Persistence and recovery requirements.
- Cost scenarios.
- Potential resource shutdown strategy.
- Deployment risks.
- Required separate authorizations.

## E. Phase 18 implementation and acceptance plan

`docs/evaluation/phase_18_implementation_and_verification_plan.md`

Include:

- Exactly three formal development stages.
- Assessment result.
- Selected Stage 18.2 scope.
- Required functionality.
- Excluded/deferred functionality.
- Interface specification.
- Automated verification matrix.
- Acceptance gates.
- Rollback criteria.
- Stage 18.3 documentation and closure scope.

Do not generate an implementation Codex prompt yet.

The operator will review this assessment before authorizing Stage 18.2.

Reuse existing documentation if an equivalent Phase 18 document is already present, rather than creating conflicting duplicate authorities.

---

# 15. Documentation validation

Because this is an assessment task, do not repeat the complete Phase 17 regression suite.

Perform relevant checks:

```bash
git diff --check
git status --short --branch
git diff --stat
git diff --cached --name-only
```

Validate:

- Markdown relative links and anchors.
- Newly created document formatting.
- Consistency of phase numbers and statuses.
- Source paths and actual interface names.
- Historical test counts.
- Historical AKS outcomes.
- Current deployment uncertainty.
- Internal architectural consistency.
- Cost-estimate assumptions and citations.
- No invented endpoints or permissions.
- No false deployment claims.
- No credentials or private material.
- No unrelated code changes.
- No accidental modification of historical evidence.

Inspect each newly written file independently before final reporting.

Run a separate pre-commit review.

Do not stage or commit.

---

# 16. Required final response

At the end of the assessment, provide:

### 1. Recommended architecture

State one clear recommended frontend and deployment approach.

Explain why it is preferable to the alternatives.

### 2. Current readiness

Report:

- Local frontend implementation readiness.
- Private Azure validation readiness.
- Public/production exposure readiness.

### 3. Main engineering gaps

Rank the gaps by impact and implementation dependency.

### 4. Phase 18.2 implementation specification

Identify the complete bounded implementation scope and acceptance tests.

No additional development stages.

### 5. Azure cost implications

Summarize local, private-validation and always-on deployment cost drivers.

Do not report unverified prices as facts.

### 6. Authorization requirements

Identify exactly which future operations require user approval, especially cloud activation, paid inference and external data processing.

### 7. Files and Git disposition

List every new or modified file.

Separate assessment changes from inherited unrelated files.

Report:

```bash
git status --short --branch
git diff --stat
git diff --cached --name-only
```

Provide a suggested commit message:

`docs: assess Phase 18 frontend integration and Azure deployment readiness`

Do not commit or push.

---

# Final instruction

**Execute Phase 18.1 — Assessment now.**

Determine the most practical, secure and cost-effective architecture for turning Estudio PolyMind into a usable document-intelligence application.

Use the completed Phase 17 functionality as the foundation.

Prefer extending existing components over replacing them.

Assess Streamlit, secure FastAPI integration, authentication, durable processing, Azure/AKS readiness, deployment costs and production boundaries.

Produce a technically concrete Stage 18.2 implementation specification, but do not implement it.

Maintain exactly three formal stages.

Do not activate cloud resources, perform paid inference, expose participants or change production code.

End with an evidence-based readiness verdict and clear recommendation for operator review.

---

# ADDENDUM — Phase 18.1 Assessment: Cost-Optimized Azure Deployment

This instruction supplements the existing **Phase 18.1 — Secure Document Frontend Integration and Azure Deployment Readiness Assessment**.

**Do not restart the assessment, discard completed work, or create another development stage.** Incorporate these requirements into the current assessment and its final deliverables.

## 1. Revised primary objective

The local-first development strategy is **already decided** and must not be reconsidered.

The primary cloud-architecture question is:

**Can Estudio PolyMind be deployed securely, reliably and cost-effectively on Azure without using the comparatively expensive Azure Kubernetes Service (AKS)?**

AKS was successfully validated during Phase 16. However, prior AKS success does not make AKS mandatory for subsequent deployments.

The assessment must identify the **lowest-cost technically suitable Azure architecture**, considering the application's complete requirements rather than infrastructure cost alone.

## 2. Mandatory Azure hosting comparison

Evaluate these deployment alternatives:

1. **Azure Container Apps (Consumption)** — including scale-to-zero feasibility, long-running document processing, background workers and external dependencies.
2. **Azure App Service** — including frontend/API hosting, background processing limitations, scaling and operational costs.
3. **Azure Virtual Machine** — including a small single-host Docker deployment, persistent storage, security responsibilities, availability and maintenance.
4. **Azure Kubernetes Service (AKS)** — as the previously validated reference architecture, not the default choice.

For each alternative, assess compatibility with:

- Streamlit and FastAPI.
- Hierarchical document digestion and durable jobs.
- Shared authentication, authorization and governance.
- Persistent documents, databases and vector indexes.
- Redis and background workers.
- Azure Foundry or provider-neutral inference.
- Long-running jobs and restart/recovery.
- Logging, monitoring and backup.
- Private versus public access.
- Future scaling requirements.

Do not assume an alternative is suitable solely because it supports Docker containers.

## 3. Total cost of ownership

Compare realistic costs for three operating scenarios:

- **Occasional private demonstration:** a few hours per week.
- **Low-traffic application:** approximately 1–5 users, with intermittent document processing.
- **Always-on application:** continuous monthly availability.

Include infrastructure, persistent storage, databases, networking, monitoring, backups and inference.

Account for idle charges, minimum resource requirements, scale-to-zero limitations and costs of supporting services.

Use current official Azure prices where accessible. Otherwise, provide explicit cost formulas and label prices UNVERIFIED.

Identify which costs remain even when application containers are stopped.

## 4. Decision criteria

Recommend the cheapest option that satisfies the necessary technical and security requirements.

Use AKS only if a specific, demonstrated requirement justifies Kubernetes-level complexity or cost.

If Container Apps, App Service or a VM is sufficient, explicitly recommend avoiding AKS for the initial deployment.

Separate:

- **Recommended initial deployment architecture.**
- **Potential future enterprise-scale architecture.**

Do not overengineer the initial deployment for hypothetical traffic.

## 5. Required deliverable updates

Integrate this analysis into:

- `docs/evaluation/phase_18_1_azure_deployment_readiness.md`
- `docs/codex/reports/phase_18_1_assessment.md`
- `docs/evaluation/phase_18_implementation_and_verification_plan.md`

Add a comparative decision matrix covering total cost, architectural compatibility, operational complexity, security, reliability and scaling.

Provide an explicit final verdict:

`AKS_REQUIRED`

or

`AKS_NOT_REQUIRED`

or

`AKS_DECISION_PENDING_EVIDENCE`

Explain the evidence supporting the verdict.

## 6. Preserve existing restrictions

This is still **Phase 18.1 — Assessment only**.

Do not provision, start, stop or modify Azure resources. Do not deploy applications, perform paid inference, install dependencies or change application code.

Maintain exactly three formal development stages.

Leave all changes uncommitted for operator review.

**Final objective: Select a cost-effective Azure deployment strategy without sacrificing the essential document-intelligence, security and reliability requirements of Estudio PolyMind.**
