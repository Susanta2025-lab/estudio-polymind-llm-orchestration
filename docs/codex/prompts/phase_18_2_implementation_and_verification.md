# CODEX MASTER PROMPT — PHASE 18.2

## Secure Document Frontend Integration — Implementation and Verification

**Project:** Estudio PolyMind
**Repository:** `Susanta2025-lab/estudio-polymind-llm-orchestration`
**Phase:** 18 — Secure Document Productization and Azure Deployment Readiness
**Stage:** 18.2 — Implementation and Verification
**Task type:** Full engineering implementation, automated verification, local integration testing and technical evidence report

# 1. Mission

Implement and comprehensively verify the architecture approved during **Phase 18.1 — Secure Document Frontend Integration and Azure Deployment Readiness Assessment**.

The central objective is:

**Transform Estudio PolyMind's existing document-intelligence backend into a usable, authenticated, locally running document application without rebuilding its existing RAG, document-processing, inference or governance capabilities.**

At completion, an authorized operator should be able to use a browser to:

1. Authenticate securely.
2. Access the new Documents interface.
3. Select an approved synthetic technical document.
4. Initiate a bounded document-processing job.
5. Observe durable processing status and progress.
6. Receive a validated complete document digest.
7. Explicitly authorize publication.
8. Navigate original-source evidence and citations.
9. Ask bounded questions about the selected document.
10. Receive evidence-grounded answers or appropriate abstentions.
11. Cancel, close or withdraw a session.
12. Inspect limits, permitted usage and residual-retention status.

This workflow must use the existing production-oriented domain components with synthetic test data and inference substitutes.

**Do not build another document-intelligence pipeline. Integrate the one already implemented.**

The intended deliverable is a working, locally verified, private operator application.

It is not a public SaaS platform, unrestricted document-upload product or production multi-tenant service.

# 2. Mandatory three-stage development policy

The project follows exactly THREE formal development stages per phase.

| Stage | Responsibility | Status |
|---|---|---|
| 18.1 | Assessment | COMPLETE |
| 18.2 | Implementation and Verification | ACTIVE — THIS TASK |
| 18.3 | Documentation and Closure | NOT STARTED |

Complete all feasible authorized implementation and verification within Stage 18.2.

Do not create additional formal stages, such as 18.2A, 18.2B or a separate testing stage.

Engineering workstreams and verification groups are internal organization only.

Do not begin Stage 18.3 documentation closure.

Do not prematurely declare Phase 18 formally complete.

# 3. Verify repository baseline

The last recorded assessment commit is:

`f0e420b6a4ab479ffaa166d000d55c91164f154b`

Commit message:

`docs: assess Phase 18 frontend integration and Azure deployment readiness`

GitHub Actions verification:

- Workflow: Estudio PolyMind CI
- Run ID: `43469571976`
- Conclusion: SUCCESS
- Reported duration: 11m04s

Verify that the actual current local HEAD matches the expected baseline, or document any subsequent changes.

Before editing, run:

```bash
git status --short --branch
git log --oneline -7
git rev-parse HEAD
git diff --check
```

Read and follow `AGENTS.md`.

Inspect existing tracked modifications and untracked files before proceeding.

The repository previously contained 28 inherited untracked Phase 17H prompt/report files.

Preserve them exactly.

Do not stage, delete, overwrite or accidentally include historical documents.

No Git commit, push, rebase, reset, clean or history rewrite is authorized.

# 4. Binding Phase 18.1 architecture decisions

The following committed documents are the authoritative basis for this task:

### Architecture assessment

`docs/codex/reports/phase_18_1_assessment.md`

### Frontend and API design

`docs/evaluation/phase_18_1_frontend_integration_architecture.md`

### Azure hosting and financial assessment

`docs/evaluation/phase_18_1_azure_deployment_readiness.md`

### Implementation and verification specification

`docs/evaluation/phase_18_implementation_and_verification_plan.md`

Read all four completely before implementation.

The Stage 18.1 decisions are:

| Architecture decision | Approved direction |
|---|---|
| Frontend | Extend existing Streamlit |
| Backend | Existing FastAPI |
| Document workflow | Reuse Phase 17 document services |
| Supervised verification | Existing `SupervisedPilot` behind a narrow operator boundary |
| Identity | OIDC-authenticated, explicitly enrolled operator |
| Initial documents | Server-approved synthetic PDFs/text |
| Inference | Deterministic, offline, fixture-only |
| Job execution | Single-host durable processing |
| Storage | Existing local object and SQLite reference authorities |
| Development | Local-first |
| Containerization | Docker/Compose, with Kind compatibility as applicable |
| Initial Azure candidate | Private Linux VM with Docker |
| AKS | `AKS_NOT_REQUIRED` |
| Distributed cloud infrastructure | Deferred |
| External-user verification | Deferred |
| Paid inference | Not authorized |

Do not reopen the local-first policy.

Do not add React, Next.js, AKS, Azure Blob, PostgreSQL, Service Bus, another vector database or a new inference framework without identifying an actual unavoidable requirement.

A major incompatibility with the approved architecture must be reported explicitly rather than silently resolved by expanding scope.

# 5. Inspect and preserve existing functionality

Before implementation, inspect the current source and tests.

## Frontend

- `ui/app.py`
- `ui/api_client.py`
- `config/settings.py`
- Current Streamlit/client tests.

## API and security

- `api/app.py`
- `api/security.py`
- `security/identity.py`
- `security/runtime.py`
- `security/authority.py`
- `security/services.py`
- `security/models.py`

## Document system

- `documents/extraction.py`
- `documents/storage.py`
- `documents/jobs/`
- `documents/digestion/`
- `documents/publication/`
- `documents/pilot/`

## Inference and financial governance

- `llm/`
- `governance/`
- Existing shared inference-admission and authorization tests.

## Deployment and operations

- `Dockerfile`
- `.dockerignore`
- `docker-compose.yml`
- `deployment/helm/polymind/`
- Existing readiness and observability implementation.

Identify interface consumers before changing shared contracts.

Preserve:

- LangGraph orchestration.
- Existing RAG retrieval and reranking.
- Ollama inference.
- OpenAI-compatible inference.
- Azure Foundry compatibility.
- Existing query and NDJSON streaming contracts.
- Existing conversation-memory behavior.
- Canonical document/source identities.
- Managed synthesis and checkpoint versions.
- Publication authority and generation fencing.
- Owner/tenant authorization.
- Financial settlement and provider quota enforcement.

The existing chat UI should remain compatible in its supported legacy local mode.

In the new OIDC Documents profile, legacy chat calls must remain disabled when the API intentionally denies them.

Do not bypass those denials to make the frontend appear functional.

# 6. Implement the Streamlit Documents interface

Extend the existing Streamlit application with a dedicated **Documents** view.

Do not replace the entire UI.

Keep the implementation modular, maintainable and consistent with the current Python stack.

## 6.1 Required sections

The Documents interface must provide:

### Authentication and operator context

Show the verified operator's permitted application context, session status and relevant restrictions.

Never treat user-entered email, username, browser state or decoded unverified token contents as authorization.

### Approved source selection

Display only server-approved synthetic sources.

Show safe identifying metadata, source type and applicable processing limits.

Do not implement unrestricted browser uploads in this phase.

### Document processing

Allow explicit creation and starting of an approved processing session.

Use stable idempotency keys so Streamlit reruns, browser refreshes, double-clicks and network retries do not create duplicate work.

### Processing status

Display authoritative backend status.

Represent queued, running, completed, partial, failed, cancelled and unavailable conditions accurately.

Polling must never initiate inference or publication.

### Digest viewer

Display the complete supported `DigestArtifact` structure, including:

- Main findings and summary.
- Source coverage.
- Material qualifications.
- Contradictions and limitations.
- Open questions.
- Original supporting evidence.
- Processing and validation status.

Do not present PARTIAL or FAILED output as COMPLETE.

### Evidence and citation navigation

Display canonical original-source references.

Preserve source/document identity, generation, page or line, span and excerpt.

A structurally valid citation does not automatically prove semantic entailment.

Preserve the explicit distinction between verified structural provenance and unverified semantic support.

### Selected-document Q&A

Provide one bounded question interface attached to the approved session and document.

Display:

- Answer.
- Evidence status.
- Canonical citations.
- Abstention when support is insufficient.
- Applicable question or execution limits.

Do not implement a second unrestricted inference path.

### Session controls

Provide distinct actions for:

- Cancel processing.
- Close session.
- Withdraw session.
- Clear frontend display state.
- Log out.
- Operator emergency stop.

These actions are not interchangeable.

Closing or clearing the browser cannot imply erasure of retained backend artifacts.

Display truthful retention information, including `PURGE_PENDING` when applicable.

## 6.2 UI security

Treat all source text and model output as untrusted.

Use inert or escaped presentation.

Do not render arbitrary source/model HTML, scripts, remote iframes or executable content.

Avoid global caching of protected document results.

Every protected rerender or retrieval must remain subject to current server authorization.

Use stable, session-scoped state without allowing cross-session content leakage.

# 7. Implement secure browser authentication

This is a critical Phase 18.2 requirement.

The local application must demonstrate real OIDC authorization-code behavior using an offline, loopback test identity provider and test JWKS.

Do not use live Azure Entra credentials for required local tests.

## Required behavior

Implement and verify:

1. OIDC authorization-code login.
2. Correct redirect and callback handling.
3. State and nonce verification.
4. Correct API-audience access-token acquisition.
5. Server-side JWT signature and claim validation.
6. Explicit operator enrollment/allowlisting.
7. Required `PUBLICATION_MANAGE` authorization.
8. Exact owning scope.
9. Token/session expiration.
10. Logout and subsequent access denial.
11. CSRF/origin/XSRF protection as applicable.
12. Secure cookie handling behind the chosen local TLS boundary.

Do not use pasted shared bearer tokens as a fallback.

Do not place access tokens in browser `localStorage`, displayed fields, logs or committed configuration.

Do not trust an ID token as an API access token.

The Streamlit pinned-runtime authentication behavior must be verified against its actual implementation.

If native authentication relies on signed browser cookies, document and test its cookie, token and expiry limitations.

Do not claim encrypted or server-side opaque sessions when only signed cookies exist.

### Mandatory security checkpoint

Before completing the rest of the UI, prove that the selected login mechanism can safely deliver the required verified API access token.

If it cannot, report a specific architectural blocker.

Do not weaken OIDC or introduce an insecure shortcut simply to complete the milestone.

A narrow, justified authentication dependency is permissible within the approved architecture, but substantial dependency or stack changes must be reported and justified.

# 8. Implement protected FastAPI operator contracts

Use the single authoritative proposed API contract table in:

`docs/evaluation/phase_18_1_frontend_integration_architecture.md`

Do not create an alternative or conflicting endpoint vocabulary.

Implement the following documented operator routes:

| Method | Route |
|---|---|
| GET | `/documents/operator/context` |
| GET | `/documents/operator/sources` |
| POST | `/documents/operator/sessions` |
| POST | `/documents/operator/sessions/{session_id}/start` |
| GET | `/documents/operator/sessions/{session_id}` |
| POST | `/documents/operator/sessions/{session_id}/publish` |
| GET | `/documents/operator/sessions/{session_id}/digest` |
| POST | `/documents/operator/sessions/{session_id}/questions` |
| POST | `/documents/operator/sessions/{session_id}/cancel` |
| POST | `/documents/operator/sessions/{session_id}/close` |
| POST | `/documents/operator/stop` |

Use the exact request/response and idempotency requirements defined in the assessment.

Additional supporting private interfaces are permitted only when necessary and fully justified.

## Security requirements

Every operator route must require:

- Verified OIDC access-token principal.
- Approved operator enrollment.
- Required publication-management permission.
- Correct owning scope.
- Valid session and source authorization.
- Current revocation/expiry state.
- Correct publication and generation binding where applicable.

The client must never supply authoritative:

- Owner or tenant.
- Security principal.
- Provider/model selection.
- Filesystem path.
- Arbitrary source URL.
- Financial allowance.
- Approval record.
- Role or privilege.
- Publication scope.

Use strict request models and sanitized error responses.

Ensure route ordering cannot let a dynamic document path intercept fixed operator routes.

Do not expose privileged Python methods through reflection or generic action dispatch.

Preserve existing routes and their behavior.

For the document-demo profile, keep unrestricted use of `/documents/analyze` unavailable; use the session-bound questions route, which reuses the established analysis service internally.

This must prevent bypassing the pilot's question allowance or execution authorization.

# 9. Implement a narrow operator workflow service

Create the smallest coherent service composition necessary to connect FastAPI to existing document authorities.

Reuse, rather than duplicate:

- `SecurityRuntime`.
- `SecurityAuthority`.
- `GovernanceLedger`.
- `SQLiteInferenceAdmission`.
- `LocalObjectStore`.
- `SQLiteJobLedger`.
- Existing ingestion/extraction contracts.
- `SupervisedPilot`.
- `AuthorizedPublication`.
- `AuthorizedAnalysis`.
- `PublicationReplica`.
- Existing managed synthesis and analysis services.

The trusted service must preserve exact owner, tenant, document, session, profile, model and authority bindings.

Do not introduce a second financial ledger or an independent authority namespace.

## `SupervisedPilot` boundary

Maintain `SupervisedPilot` as an owning-operator-controlled facade.

Do not expose participant-facing privileged functionality.

Do not grant ordinary users `PUBLICATION_MANAGE`.

The initial browser workflow uses server-created synthetic source and session approval fixtures.

These fixtures are not real participant consent.

The operator cannot create arbitrary source approval, reviewer findings, budgets or real execution authorization from browser-controlled fields.

Preserve existing session limits and validation.

# 10. Implement local synthetic execution

The default Phase 18.2 document profile must use:

- Approved synthetic PDF/text fixtures.
- Deterministic structured provider responses.
- Synthetic embeddings and reranking substitutes as appropriate.
- Existing production document-processing components.
- Explicit managed-prompt/11 profiles.
- Existing provenance and receipt validation.
- Existing publication and selected-document Q&A.

Do not import application fixtures from `tests/` into production modules.

If a reusable development-only fixture provider is required, introduce it under a clearly separated development/test adapter and prevent production configuration from selecting it.

## Required safety properties

- Zero Azure calls.
- Zero external provider attempts.
- Zero paid inference.
- No real provider credential access.
- No arbitrary fallback to a real model.
- No provider retry outside the documented controls.
- Production configuration rejects fixture-only execution.

Instrument transport boundaries so that these statements can be verified, not merely assumed.

Preserve the global managed-prompt/10 default outside the explicit v11 document workflow.

Do not change the accepted historical v11 evidence or its provenance contracts.

# 11. Implement durable job execution and recovery

Document processing must not depend on an active browser session or a long-running HTTP request.

Implement a bounded local worker/runner using existing job, lease, checkpoint, dispatch and financial-governance components.

## Required behavior

### Durable admission

A processing request creates one accepted durable job.

Repeated requests with the same accepted intent reuse that job.

Conflicting requests using the same idempotency key must be rejected.

### Independent processing

The runner continues independently of Streamlit reruns and HTTP client disconnects.

Status requests must not execute work.

### Checkpoints

Accepted compatible checkpoints may be reused following safe restart/reconciliation.

Stale or incompatible checkpoints are refused.

### Fencing

Expired leases and stale generations cannot commit newer results.

### Cancellation

Cancellation must fence new work and preserve known/unknown financial obligations.

An already-running external operation cannot be assumed refunded or physically stopped.

### Restart

After restart, restore only consistent recorded state and require valid operator authorization.

No silent authority, policy, quota or approval reset.

### Emergency stop

Durably deny new admission and protected output where applicable before acknowledging a stop.

Allow only permitted reconciliation and financial/audit settlement.

### Financial uncertainty

An UNKNOWN reservation or unsettled execution intent blocks unsafe continuation.

Never fabricate token usage, cost settlement or refunds.

## Existing execution bounds

Preserve Phase 17I restrictions:

- Maximum three approved sessions.
- One open job.
- One controlled execution lane.
- Maximum 1 MB source.
- Maximum four supported native PDF pages.
- Maximum 4,000 extracted characters.
- Maximum three synthesis attempts.
- Maximum three questions.
- Maximum six provider attempts total.
- Maximum 24,800 reserved input tokens.
- Maximum 3,000 output tokens per call.
- Existing 60-second provider timeout.
- Existing 600-second workflow deadline.

Existing tighter configuration limits continue to apply.

Do not automatically reset pilot databases to extend the demonstration.

Review job lease duration and renewal against actual bounded provider timeouts and safe commit margins.

# 12. Protect output at the actual response boundary

Authorization at the start of an operation is insufficient if session authority changes before output delivery.

For every protected digest, answer and status response, verify the relevant current authority and state before release.

Assess and implement the required FastAPI/ASGI response-send protection.

Test:

- Operator disablement.
- Permission revocation.
- Session expiry.
- Session withdrawal.
- Emergency stop.
- Publication-generation replacement.
- Source/document revocation.
- Tenant or owner scope mismatch.
- Restart with incompatible epochs.
- Delayed response after authorization changes.

If authorization is revoked before protected bytes are sent, the application must not release those bytes.

Previously delivered content cannot be recalled; document that boundary honestly.

Avoid holding authority/database transactions open during provider inference or long network operations.

Do not use globally cached answers as a shortcut around current authorization.

# 13. Local configuration and Docker integration

Implement a dedicated, explicit local document-demo configuration.

It must remain distinct from:

- The existing legacy chat configuration.
- The production deployment configuration.
- Live Azure Foundry execution settings.

Provide supported startup, shutdown and restart behavior using the existing development environment.

Prefer incremental Compose configuration rather than replacing the project's current Compose topology.

## Required persistence

Use dedicated local mounts/directories for:

- Canonical document objects.
- Private security authorities.
- Governance/admission ledgers.
- Job state and checkpoints.
- Pilot/session control.
- Action idempotency records.
- Publication authority and indexes.
- Bounded scratch space.

Prevent overlapping writers or incompatible authorities.

Ensure filesystem permissions work with the expected non-root container identity.

Do not casually change filesystem ownership outside this phase's intended runtime directories.

## Configuration safety

- No secrets in Docker images.
- No actual `.env` files committed.
- No OIDC session/token cache included in the build context.
- No real provider keys in fixture containers.
- No public access to Redis, Chroma, SQLite or privileged operator services.
- No unrestricted management endpoints.
- No production validator bypass.

Add a narrowly scoped TLS/test identity setup if required for browser authentication verification.

Document safe startup commands in the Stage 2 report; comprehensive operator documentation belongs to Stage 18.3.

Do not use `docker build --no-cache` without specific approval.

Do not run Docker global pruning or delete unrelated images.

# 14. Local readiness, metrics and observability

Extend existing readiness and observability functionality only as necessary.

The local document profile must be able to distinguish:

- Healthy idle state.
- Active worker.
- Processing progress.
- Unavailable authority.
- Expired or stopped session.
- Missing or mismatched publication generation.
- Inference admission blocked.
- Audit/financial uncertainty.
- Runner failure or stale worker.
- Unavailable derived index.

The initial empty publication catalog may be a healthy idle state.

When active publication is expected, missing or mismatched generations must fail closed.

Readiness and status polling must never cause billable inference.

Reuse existing Prometheus infrastructure.

Do not introduce another observability platform.

Avoid high-cardinality document IDs in metric labels.

Do not log source contents, questions, full digests, access tokens or private identifiers.

Use bounded sanitized status and correlation information.

# 15. Mandatory verification — T01 to T15

The committed Phase 18 implementation plan defines **15 verification groups**.

Treat all applicable required assertions as mandatory.

The detailed test table in:

`docs/evaluation/phase_18_implementation_and_verification_plan.md`

is authoritative.

Implement tests under the existing `tests/unit/` and `tests/integration/` structure, with focused supporting browser tests when necessary.

## T01 — Authentication

Verify:

- Valid local fixture OIDC flow.
- Wrong issuer, audience, tenant, key, algorithm and token purpose.
- Expired or premature tokens.
- Unknown roles.
- Unapproved operator enrollment.
- App-only or invalid subjects.
- Failure before document/provider effects.

## T02 — Browser session and cookies

Verify:

- Actual authorization-code callback.
- State/nonce.
- CSRF/XSRF/origin checks.
- Secure cookie attributes.
- Access-token confidentiality.
- Isolated browser contexts.
- Logout and expiry.

Do not consider a mocked `st.user` sufficient proof.

## T03 — Source eligibility

Verify approved synthetic PDF/text and rejection of:

- Invalid hashes.
- Expired approvals.
- Unsupported or malformed files.
- Unsafe filename/path inputs.
- Oversized requests.
- Unapproved sources.
- Owner/tenant injection.
- Unsupported scanned/encrypted/layout-dependent documents.

## T04 — Durable action idempotency

Verify duplicate browser actions, reconnects and HTTP retries cannot create duplicate jobs, publication or provider executions.

Test interruption between recording an intent and recording its accepted result.

## T05 — Worker recovery

Verify:

- Durable status.
- Browser disconnect/reconnect.
- Worker interruption.
- Checkpoint reuse.
- Lease expiry.
- Stale fencing.
- Reauthorization.
- Zero inference from polling.

## T06 — Cancellation and stop races

Verify queued/running cancellation, repeated close/withdraw, stop during work and release-time authorization changes.

Prevent new unauthorized work or output after acknowledged fencing.

Preserve in-flight liability and financial audit.

## T07 — Digest and provenance

Verify full digest presentation, COMPLETE/PARTIAL/FAILED distinctions, coverage gates, qualification preservation, generation identity and original source spans.

Reject forged or stale citations.

Do not claim semantic entailment from citation structure.

## T08 — Session-bound Q&A

Verify:

- Approved selected-document questions.
- Supported evidence.
- Insufficient or conflicting evidence.
- Cross-owner/tenant denial.
- Revocation during response.
- Generation replacement.
- No direct analyze bypass.

## T09 — Financial and provider controls

Verify:

- Owner/tenant attribution.
- Shared provider admission.
- RPM/TPM limits.
- Output reservation.
- Concurrent-call restrictions.
- Six-attempt ceiling.
- No automatic paid retry.
- UNKNOWN preservation.
- Zero external provider traffic.
- Zero real credential access.

## T10 — Fault and recovery

Exercise:

- Database unavailable/locked/corrupt.
- Missing immutable object.
- Vector unavailable.
- Audit exhaustion.
- Publication activation interruption.
- Stale replicas.
- Provider timeout/429/malformed response.

Ensure sanitized failures and no false COMPLETE status.

## T11 — Privacy and restore

Verify withdrawal/revocation, retention inventory, `PURGE_PENDING`, coherent local restore, preserved consumed approvals and no rollback of security or financial truth.

## T12 — UI and API integration

Verify the complete supported operator journey and compatibility with existing legacy chat/NDJSON behavior.

Check request resource cleanup, timeouts, UI error states and safe presentation.

## T13 — Container/deployment contracts

Verify:

- Compose configuration.
- Supported cached image build.
- Private mounts.
- Secret exclusions.
- Container permissions.
- Single-writer behavior.
- Fixture rejection under production configuration.
- Existing Helm compatibility.

Use Kind only when an existing appropriate dedicated local context is available.

No Azure fallback is authorized if Kind is unavailable.

## T14 — Operational readiness

Verify worker/readiness signals, stale status, financial/audit blocking and no inference from health/status checks.

## T15 — Real local authenticated end-to-end acceptance

This is a hard acceptance gate.

Demonstrate an actual browser/UI client over HTTP using the authenticated local API and worker.

The verified journey must include:

```text
OIDC Login
     ↓
Verified Operator
     ↓
Select Synthetic Source
     ↓
Create Session
     ↓
Start Durable Job
     ↓
Observe Progress
     ↓
Validate COMPLETE Digest
     ↓
Explicit Publication
     ↓
Read Canonical Evidence
     ↓
Ask Grounded Question
     ↓
View Answer + Citation
     ↓
Close / Withdraw
     ↓
Logout
```

Also verify cancellation, PARTIAL/FAILED, stale authorization, browser isolation and delayed-response revocation.

Use an available browser testing harness where possible.

Streamlit AppTest may verify presentation and application behavior but does not independently prove a real OAuth callback, TLS or browser cookie handling.

If full browser tooling is unavailable, report that specific acceptance gate as **NOT ESTABLISHED**.

Do not claim full browser-authenticated PASS from API-only tests.

# 16. Acceptance thresholds and engineering quality

Stage 18.2 must satisfy the committed Phase 18 acceptance matrix.

Required outcomes include:

1. All mandatory T01–T15 coverage groups pass.
2. No unresolved critical/high-severity implementation defects.
3. At least one complete integrated synthetic document-processing journey.
4. At least one cancellation scenario.
5. At least one PARTIAL or FAILED scenario.
6. At least one restart/reconciliation scenario.
7. No unauthorized access across owners, tenants or sessions.
8. No duplicated provider execution from reruns/retries.
9. No released protected result after relevant acknowledged revocation.
10. No false COMPLETE digest.
11. All displayed citations retain canonical source identity.
12. Zero real external-provider attempts.
13. Zero paid inference.
14. Zero real credential exposure.
15. Correct retained financial obligations and residual artifacts.
16. Existing application contracts remain compatible.
17. Local Docker/runtime configuration is reproducible.

Healthy local polling should reflect changed persisted state within the configured 2–5-second interval.

Do not invent a production latency or availability SLA using synthetic timings.

## Source freeze and regression

After implementation and focused tests:

- Freeze the intended implementation tree.
- Run the full regression suite on that tree.
- Record exact pass/fail/skip/warning counts and durations.
- Run applicable compile/lint/format checks.
- Validate Compose/Helm.
- Validate relevant container configuration and smoke tests.
- Inspect the complete changes.
- Perform a separate security/pre-commit review.

Do not reuse the historical 3,052-test Phase 17I result as evidence that newly introduced Phase 18 functionality passed.

Do not combine intermediate test counts into a fabricated total.

If a test fails, distinguish actual regressions, fixture/environment problems and unrelated pre-existing failures. Fix task-related defects rather than hiding them.

If full acceptance cannot be demonstrated, report the exact remaining blocker and a PARTIAL verdict.

# 17. Explicitly excluded implementation

Do not implement:

- General public document uploads.
- Ordinary-user registration.
- Multi-user commercial SaaS workflows.
- External participant recruitment.
- Private or sensitive real-document processing.
- Full physical deletion guarantees.
- Azure Blob authority.
- PostgreSQL/distributed security, job or governance ledgers.
- Distributed worker clusters.
- Azure Service Bus.
- New Kubernetes infrastructure.
- AKS deployment.
- Azure VM provisioning.
- Container Apps deployment.
- App Service deployment.
- Workload identity migration.
- New React/Next.js frontend.
- New vector database.
- OCR/layout service.
- Self-hosted vLLM or GPU inference.
- Live Azure Foundry calls.
- Provider quota/capacity increases.
- Automatic paid retries.
- Production HA/DR certification.

Do not activate external services.

Do not install a broad new dependency stack to solve a narrow integration problem.

If an excluded capability becomes a genuine prerequisite, document the reason and affected acceptance criterion. Do not silently broaden Phase 18.2.

# 18. Preserve existing deferred Phase 17 obligations

The following classifications remain unchanged:

`PHASE_17_ENGINEERING_COMPLETE`

`DEFERRED_PENDING_TWO_INDEPENDENT_REVIEWERS`

`PHASE_17_FORMAL_CLOSURE_PENDING`

`PHASE_17I_ENGINEERING_COMPLETE`

`PHASE_17I_EXTERNAL_VERIFICATION_DEFERRED`

`PHASE_17I_FORMAL_ACCEPTANCE_PENDING`

`SUBSEQUENT_ENGINEERING_PERMITTED`

Do not mark the two external human reviews complete.

Do not invent external participants or feedback.

The Phase 18 local synthetic browser acceptance is **not** Phase 17I's external-user verification.

A functional frontend is not automatically a production security or semantic-quality certification.

The accepted internal quality and evidence constraints remain binding.

# 19. Stage 18.2 documentation artifacts

Preserve this master prompt as:

`docs/codex/prompts/phase_18_2_implementation_and_verification.md`

Create the implementation and verification report:

`docs/codex/reports/phase_18_2_implementation_and_verification.md`

The report must include:

## Executive engineering decision

Provide an explicit stage verdict and implemented-scope classification.

## Baseline

Record actual starting HEAD, repository state and prior CI evidence.

## Implementation inventory

List every new or changed application file and explain its function.

## Architecture

Explain frontend, API, operator service, runtime identity, worker, publication, state and inference boundaries.

## Authentication verification

Document real local OIDC redirect/callback evidence, token checks, cookie/security behavior and negative authorization tests.

## Workflow verification

Document the successful integrated operator journey.

Include failure/cancellation/restart examples and exact observed outcomes.

## Test results

Provide:

- New test count.
- Unit/integration/browser test counts.
- T01–T15 dispositions.
- Full frozen-tree regression result.
- Duration.
- Skips/warnings/failures.
- Any test environment limitations.

## Financial and provider verification

Demonstrate synthetic-only execution, zero external calls and correct financial governance behavior.

## Reliability and recovery

Document durable processing, leases/fencing, revocation, stop/UNKNOWN and restore results.

## Deployment/configuration

List supported local startup/runtime modes, Docker validation, required persistent mounts and security boundaries.

## Remaining limitations

Distinguish completed local functionality from:

- Unverified real Entra integration.
- Unverified actual Azure VM deployment.
- Real-model semantic acceptance.
- External participants.
- Public exposure.
- Distributed production reliability.

## Stage 18.3 handoff

Identify exactly which documentation, operator instructions, architecture updates and administrative closure decisions remain for Stage 18.3.

Do not begin Stage 18.3.

# 20. Final code review and Git discipline

Before reporting completion:

1. Inspect the complete new implementation and diff.
2. Verify architectural consistency.
3. Review API compatibility.
4. Review authentication and authorization.
5. Inspect concurrency and idempotency.
6. Review provider invocation and settlement boundaries.
7. Check resource cleanup and error handling.
8. Inspect test quality and missing negative cases.
9. Review startup/shutdown and recovery.
10. Perform a separate pre-commit security review.

Check for:

- Secrets and credentials.
- Private keys.
- Real environment files.
- OIDC test tokens or generated test keys accidentally committed.
- Absolute local paths.
- Personal or private documents.
- Unintended database files.
- Generated outputs.
- Debug statements.
- Unnecessary dependencies.
- Protected runtime evidence.
- Accidental public routes.
- Unrelated refactors.
- Historical Phase 17H document changes.

Run:

```bash
git diff --check
git status --short --branch
git diff --stat
git diff --cached --name-only
```

Remember that untracked files are excluded from ordinary `git diff --stat`; include all intended new files separately in the final inventory.

**Do not stage, commit or push.**

Leave all implementation changes for manual operator review.

Suggested commit message:

`feat(documents): implement authenticated local document frontend and verification`

# 21. Final required verdict

If all required local implementation, security, workflow and verification gates pass, conclude:

**`PHASE_18_2_ENGINEERING_PASS`**

**`PHASE_18_2_LOCAL_INTEGRATION_PASS`**

**`PHASE_18_2_OFFLINE_VERIFICATION_PASS`**

**`AKS_NOT_REQUIRED`**

**`PHASE_18_3_DOCUMENTATION_PENDING`**

**`PRODUCTION_READINESS_NOT_ESTABLISHED`**

If mandatory functionality or verification is incomplete, report:

`PHASE_18_2_PARTIAL`

or

`PHASE_18_2_BLOCKED`

with exact reasons and remaining work.

Do not declare PASS based only on successful imports, mocked API handlers, existing Phase 17 tests or a partially implemented Streamlit interface.

Azure execution, real participant evidence and actual-model semantic quality are not acceptance requirements for this bounded local Stage 18.2. They remain separately gated future work.

# FINAL INSTRUCTION TO CODEX

Execute **Phase 18.2 — Implementation and Verification** now.

Implement the complete approved local operator-facing document workflow using existing Streamlit, FastAPI, Phase 17 document-intelligence services and financial/security authorities.

Build secure OIDC authentication, narrowly scoped operator API interfaces, durable execution, source selection, digest presentation, canonical citations, bounded Q&A, cancellation, withdrawal and recovery.

Use deterministic inference and synthetic technical documents.

Verify the complete application through meaningful unit, integration, security, browser and failure-recovery tests.

Preserve all existing application architecture and historical evidence.

Do not activate Azure resources, use real provider credentials, execute paid inference or deploy AKS.

Complete the feasible authorized engineering and verification within this single Stage 18.2.

Produce the full technical implementation report and leave the repository uncommitted for operator review.

**The required outcome is a working, authenticated, locally verified Estudio PolyMind document application—not another architecture proposal.**

# ADDENDUM — Phase 18.2: Command Execution Authorization

I explicitly authorize Codex to execute **all necessary local read-only, testing, verification, and diagnostic commands** required to complete Phase 18.2 Implementation and Verification.

## Authorized operations

- Repository inspection: `git status`, `git diff`, `git log`, `git show`, `grep`, `rg`, `find`, `ls`, `cat`, etc.
- Python testing: `pytest`, `python -m pytest`, `unittest`, compilation, import checks and test coverage.
- Static analysis: `ruff`, `mypy`, formatting checks and security diagnostics.
- Local API, authentication, browser and end-to-end integration tests.
- Docker and Docker Compose builds, configuration validation, startup, shutdown and testing of **project-specific local test containers**.
- Local Kind/Kubernetes testing using explicitly identified development contexts.
- Running local synthetic inference, fixture servers and test databases.
- Creating, modifying and deleting disposable files generated specifically for tests within approved test directories.
- Installing narrowly necessary project/test dependencies in the existing isolated development environment, consistent with repository dependency policies.
- Executing test commands repeatedly as necessary to diagnose failures and verify corrections.

## Permission policy

**Do not request my confirmation for each routine testing, inspection or diagnostic command.**

Treat this message as standing authorization for the local operations listed above throughout Phase 18.2.

Where the Codex execution environment supports persistent command permissions, use the appropriate scoped approval settings to minimize repeated prompts.

This authorization does not override mandatory approval prompts enforced by the Codex platform or sandbox.

## Restrictions that remain

The following still require my separate explicit approval:

- Azure/AWS/GCP resource creation, startup, modification or deployment.
- Paid inference or external API calls that may incur charges.
- Accessing real credentials, private keys or sensitive external data.
- Installing system-wide software or making substantial dependency changes.
- Destructive operations affecting existing project data, Docker volumes or unrelated containers.
- `docker system prune`, global cleanup or deletion of existing images.
- Git staging, commits, pushes, rebases, resets or history rewrites.
- Public exposure of services or external-user testing.

All local tests must use synthetic data and approved fixture providers by default.

## Execution instruction

Continue the existing Phase 18.2 task without restarting it.

Perform all necessary authorized local testing, diagnostics and verification autonomously. Fix implementation defects and rerun relevant tests until acceptance requirements are satisfied or a genuine blocker is identified.

**Avoid unnecessary permission requests for routine local development and testing. Preserve all existing security, financial and Git restrictions.**
