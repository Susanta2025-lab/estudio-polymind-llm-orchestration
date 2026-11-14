# CODEX MASTER PROMPT — PHASE 18.3

## Documentation, Engineering Closure and Deployment Handoff

**Project:** Estudio PolyMind
**Repository:** `Susanta2025-lab/estudio-polymind-llm-orchestration`
**Phase:** 18 — Secure Document Productization and Azure Deployment Readiness
**Stage:** 18.3 — Documentation and Closure
**Task type:** Documentation reconciliation, verified engineering closure, operational handoff and pre-commit review

---

# 1. Mission

Complete **Phase 18.3 — Documentation and Closure** using the implemented and verified results of Phase 18.2.

The objective is to establish an accurate, reproducible and professionally documented engineering baseline for Estudio PolyMind's new authenticated document-intelligence application.

This task must:

1. Verify the committed Phase 18.2 implementation baseline.
2. Independently inspect the actual implemented architecture.
3. Reconcile implementation evidence against the Phase 18.1 requirements.
4. Document the supported local runtime and user workflow.
5. Document authentication, authorization and data-protection boundaries.
6. Document API contracts and operational recovery.
7. Preserve the exact Phase 18.2 verification evidence.
8. Explain supported deployment configurations and limitations.
9. Update the README, relevant runbooks and roadmap.
10. Issue an evidence-based Phase 18 engineering-completion decision.
11. Preserve all deferred external verification, Azure deployment and production-readiness obligations.
12. Leave all changes uncommitted for operator review.

**This is a documentation and engineering-closure task, not another implementation phase.**

Do not introduce new application features or attempt to obtain missing acceptance evidence through unapproved cloud or paid-model execution.

---

# 2. Mandatory three-stage policy

The project uses exactly three formal development stages.

| Stage | Scope | Required state |
| --- | --- | --- |
| 18.1 | Assessment | COMPLETE |
| 18.2 | Implementation and Verification | ENGINEERING PASS |
| 18.3 | Documentation and Closure | ACTIVE — THIS TASK |

Do not introduce Stage 18.4 or new formal Phase 18 substages.

Phase 18.3 completes the bounded engineering/documentation lifecycle. It does not automatically establish public-product or production deployment acceptance.

---

# 3. Baseline and Git safety

The Phase 18.2 report records its starting HEAD as:

`f0e420b6a4ab479ffaa166d000d55c91164f154b`

That is the Phase 18.1 assessment commit, **not the subsequent Phase 18.2 implementation commit**.

The Phase 18.2 report explicitly states that its application changes were left uncommitted for operator review.

Before beginning substantive closure, verify that the operator has committed the intended Phase 18.2 implementation.

Execute:

```bash
git status --short --branch
git log --oneline -8
git rev-parse HEAD
git diff --check
git diff --cached --name-only
```

Read `AGENTS.md`.

Identify:

- Actual current HEAD.
- Phase 18.2 implementation commit.
- Current working-tree modifications.
- Existing untracked files.
- Latest relevant GitHub Actions result.

Do not infer a commit hash that has not been observed.

### Baseline gate

If the Phase 18.2 implementation is still uncommitted, report:

`PHASE_18_3_BASELINE_PENDING_OPERATOR_COMMIT`

Do not automatically commit it.

A clean, operator-approved implementation commit is the preferred foundation for Stage 18.3 documentation.

If the implementation commit exists, continue with the assessment and documentation work.

If its CI has not yet completed, do not claim CI-verified completion. Record the pending status accurately.

### Preserve historical files

The previous implementation report recorded:

- 12 changed tracked files.
- 24 new files.
- 36 intended Phase 18.2 files in total.
- 28 inherited untracked Phase 17H documents.
- 25 unchanged managed-prompt/11 source inventory hashes.

Preserve unrelated historical files and accepted model-evaluation evidence exactly.

Do not use `git add -A`, `git clean`, `git reset --hard` or any destructive cleanup.

No commit, push, merge, rebase, tag or remote mutation is authorized.

---

# 4. Authoritative sources

Read the following documents completely.

## Phase 18.1

`docs/codex/reports/phase_18_1_assessment.md`

`docs/evaluation/phase_18_1_frontend_integration_architecture.md`

`docs/evaluation/phase_18_1_azure_deployment_readiness.md`

`docs/evaluation/phase_18_implementation_and_verification_plan.md`

## Phase 18.2

`docs/codex/prompts/phase_18_2_implementation_and_verification.md`

`docs/codex/reports/phase_18_2_implementation_and_verification.md`

## Prior-phase handoff

`docs/evaluation/phase_17i_engineering_completion_and_deferred_acceptance.md`

`docs/evaluation/phase_17i_deferred_external_verification.md`

`docs/evaluation/phase_17_engineering_completion_and_deferred_acceptance.md`

`docs/evaluation/phase_17_deferred_human_semantic_review.md`

`docs/security/phase_17g.md`

`docs/security/entra_v2.md`

`docs/security/production-security.md`

Also inspect README, deployment configuration and relevant operational documentation.

**Source-code behavior takes precedence over proposed design text when documenting what was actually implemented.**

Historical results must remain historical evidence. Do not rewrite old reports to make them appear newly verified.

---

# 5. Verified Phase 18.2 evidence

The supplied Phase 18.2 report records these results:

| Item | Recorded result |
| --- | --- |
| Engineering verdict | `PHASE_18_2_ENGINEERING_PASS` |
| Local integration | `PHASE_18_2_LOCAL_INTEGRATION_PASS` |
| Offline verification | `PHASE_18_2_OFFLINE_VERIFICATION_PASS` |
| Full regression | 3,128 passed |
| Unit tests | 2,192 passed |
| Integration tests | 936 passed |
| New tests | 76 |
| New unit tests | 29 |
| New integration tests | 47 |
| Failures/errors/skips/pytest warnings | 0 |
| Regression duration | 1,130.78 seconds |
| Verification groups | T01–T15 PASS |
| Real Chromium browser journey | PASS |
| Local container validation | PASS |
| External inference attempts | 0 |
| Azure deployment | Not performed |
| AKS requirement | `AKS_NOT_REQUIRED` |
| Production readiness | Not established |

The report records a completed authenticated browser journey using Streamlit, a local OIDC issuer, FastAPI, the existing document engine, a durable worker and synthetic inference.

It also records cancellation, token-expiry rejection, browser isolation, missing-object failure, server restart, local restore and authorization-revocation tests.

These results are **reported Stage 18.2 verification evidence**, not fresh Stage 18.3 test results.

Verify their consistency with the retained report and current source.

Do not rerun the complete regression suite solely to generate additional documentation evidence.

If source code differs materially from the verified implementation, identify the resulting evidence gap rather than carrying forward unconditional PASS.

---

# 6. Reconcile the implemented architecture

Inspect the actual source files and produce an accurate current-state architecture.

At minimum inspect:

### Frontend

- `ui/app.py`
- `ui/documents.py`
- `ui/documents_client.py`
- `ui/api_client.py`

### API

- `api/app.py`
- `api/operator.py`
- `api/security.py`

### Operator workflow

- `documents/operator/actions.py`
- `documents/operator/service.py`
- `documents/pilot/service.py`
- `documents/pilot/scheduling.py`

### Local document runtime

- `development/document_demo/__main__.py`
- `development/document_demo/app.py`
- `development/document_demo/runtime.py`
- `development/document_demo/fixtures.py`
- `development/document_demo/identity.py`
- `development/document_demo/provision.py`
- `development/document_demo/gateway.py`

### Security and financial authorities

Inspect the actual relevant `security/`, `governance/` and `llm/` integrations, including existing admission and provider restrictions.

### Deployment

- `docker-compose.documents.yml`
- `docker-compose.yml`
- `Dockerfile`
- `.dockerignore`
- `.gitignore`
- `config/settings.py`
- `requirements.txt`

Check actual imports, runtime composition and application routes.

Document the implementation precisely.

Do not describe architectural components as deployed cloud services merely because a deployment option was analyzed.

---

# 7. Document the complete user workflow

Produce an accurate operational description of:

```text
Authenticated Operator
          ↓
Approved Synthetic Source
          ↓
Durable Session Creation
          ↓
Processing Admission
          ↓
Independent Local Runner
          ↓
Hierarchical Document Synthesis
          ↓
Validated COMPLETE Digest
          ↓
Explicit Publication
          ↓
Canonical Evidence and Citations
          ↓
Bounded Document Q&A
          ↓
Close / Withdraw / Stop
```

Explain:

- What the operator sees.
- What the backend actually performs.
- Which authority owns each decision.
- Which information is durable.
- Which actions are idempotent.
- What survives browser disconnect or process restart.
- What requires renewed operator authorization.
- Which operations could fail closed.
- What is retained after closure.

Include a clear distinction between:

- Browser session state.
- Durable processing/job state.
- Financial/admission state.
- Publication-generation state.
- Security/revocation state.
- Retention and residual inventory.

The browser must not be described as the source of authoritative document or financial state.

---

# 8. Authentication and security documentation

Document the actual Phase 18.2 security design.

The recorded local configuration uses:

- Streamlit native authorization-code login.
- A loopback test identity provider.
- PKCE S256.
- State and nonce validation.
- Separate identity and API-audience tokens.
- Server-side API JWT verification.
- Explicit operator enrollment.
- Owning-scope authorization.
- Private local HTTPS gateway.
- Secure, HttpOnly and SameSite cookie controls where applicable.

Record the exact supported configuration and tested behavior.

### Mandatory limitations

Clearly explain:

1. The local test issuer is not Azure Entra production authentication.
2. Local ephemeral certificates are not publicly trusted production certificates.
3. Native Streamlit identity/token cookies are signed and browser-readable rather than encrypted opaque server-side sessions.
4. Browser logout is not guaranteed to revoke every previously copied bearer token.
5. Durable authority revocation remains the relevant security mechanism.
6. Previously delivered information cannot be recalled.
7. The implementation remains an operator-only synthetic application.
8. Ordinary users are not authorized to manage publication.
9. Public/confidential workloads require additional independent security and privacy review.

Do not describe the authenticated local test as proof of production security.

Do not claim that API token expiry and identity-cookie expiry are identical.

Preserve the exact distinction between authentication, enrollment, permissions and scope authorization.

---

# 9. Document actual API contracts

Inspect `api/operator.py` and `documents/operator/service.py`.

Document the eleven implemented operator endpoints:

| Method | Endpoint |
| --- | --- |
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

For each endpoint, document:

- Authentication requirement.
- Authorization requirement.
- Input contract.
- Output contract.
- Idempotency behavior.
- Relevant side effects.
- Failure categories.
- Durable state changes.
- Release/revocation behavior.

Use exact implemented DTO field names and status codes rather than relying on the original proposed design.

Do not publish private fixture credentials, signing keys, internal source bytes or protected runtime state.

Preserve the existing query, streaming, memory and authorized-analysis API contracts.

Explain that the synthetic Documents profile does not provide an unrestricted `/documents/analyze` inference shortcut.

---

# 10. Local setup and operation guide

Create a reproducible, security-conscious operator guide.

Use the actual Phase 18.2 implementation, not hypothetical setup commands.

The Stage 18.2 report records the following local entrypoint:

```bash
python -m development.document_demo initialize /tmp/polymind-documents
python -m development.document_demo serve /tmp/polymind-documents
```

The recorded browser entrypoint is:

`https://localhost:9443`

The synthetic identity provider uses loopback HTTPS port 9444.

The API and internal Streamlit services bind to loopback and should not be presented as public browser endpoints.

Verify exact commands against the current implementation before publishing.

## Explain

- Required Python environment.
- Pinned authentication dependencies.
- First-time initialization.
- Private runtime directory.
- Generated fixture identities and certificates.
- Safe test-certificate handling.
- Application startup.
- Login and source selection.
- Processing and polling.
- Publication and Q&A.
- Cancellation and withdrawal.
- Logout.
- Safe shutdown.
- Restart and reauthorization.
- Session expiry.
- Handling unsupported or expired sources.
- Preserving or disposing of test runtime data appropriately.

The Stage 18.2 report identifies fixture approval expiry of roughly one hour, API token expiry of 15 minutes and test TLS expiry of two days.

Verify these against code and label them development-only configuration, not production defaults.

Do not expose or print generated secrets in the documentation.

---

# 11. Docker and Compose operations

Document the actual dedicated Compose profile.

The report identifies:

`docker-compose.documents.yml`

The runtime uses a separately initialized private directory and a single-host authority model.

Document the verified initialization, build, startup, restart, shutdown and log-inspection commands.

The reported initialization model requires container-side authority paths under:

`/runtime/state`

Do not suggest initializing databases at host absolute paths and then moving them to different container paths if authority bindings are path-sensitive.

Explain:

- Intended host-to-container mapping.
- Non-root execution.
- Local TLS endpoint exposure.
- Internal API and Streamlit isolation.
- Persistent mounts.
- Credential exclusion.
- Read-only container root filesystem.
- Bounded temporary storage.
- Single-writer enforcement.
- Container restart behavior.
- Safe backup prerequisites.

Document only the supported use of the existing Docker image.

The report records an approximately 3.04 GB built image. Do not present that historical byte count as a newly measured optimized image.

No broad Docker refactor or image optimization is authorized.

Do not recommend global Docker cleanup.

---

# 12. Recovery, backup and retention guide

Provide a complete operational guide to the implemented local recovery boundary.

Cover:

## Worker interruption

Explain how persisted jobs, leases, fences, checkpoints and action intents behave when a runner or application process stops.

Explain the explicit operator reauthorization requirement on restart.

Do not promise autonomous recovery of a possibly executed call whose result is uncertain.

## Financial uncertainty

Document the meaning and consequences of UNKNOWN reservations or unsettled execution history.

No database reset, manual counter deletion or invented refund is acceptable as a recovery technique.

## Cancellation and emergency stop

Document:

- Queued cancellation.
- In-flight work limitations.
- Durable stop.
- Protected output denial.
- Remaining settlement/audit obligations.

## Publication failure

Explain generation activation, stale replicas, guarded result release and safe fail-closed conditions.

## Backup

The Phase 18.2 report records the supported quiesced backup command:

```bash
python -m development.document_demo backup /tmp/polymind-documents --destination /tmp/polymind-documents-snapshot
```

Verify its current syntax.

Explain that the destination must be outside the runtime and that all relevant security, governance, job, object, publication and control authorities must be captured coherently.

## Restore

Explain:

- Original-path requirements.
- Preserving consumed approvals.
- Preserving security revocations.
- Preserving financial obligations.
- Revalidating publication generations.
- Reauthorization.
- Rejecting incomplete or incompatible state.

Do not claim arbitrary stale-backup recovery or distributed disaster-recovery guarantees.

## Retention

Clearly distinguish:

- Logical closure.
- Access revocation.
- Metadata retirement where supported.
- Retained audit and financial state.
- Retained immutable artifacts.
- Physical erasure.

`PURGE_PENDING` must not be presented as proof of physical deletion.

---

# 13. Verification and test evidence reconciliation

Use the Phase 18.2 implementation report as the authority for executed tests.

Record the final frozen-tree result:

**3,128 tests passed**
**2,192 unit tests**
**936 integration tests**
**76 new tests**
**0 failures/errors/skips/pytest warnings**

Recorded final duration:

**1,130.78 seconds**

Summarize T01–T15 in a concise verification matrix.

Distinguish:

- Actual pytest results.
- Separate Chromium/browser harness results.
- Local Docker image verification.
- Compose validation.
- Helm validation.
- Kind unavailable/conditional testing.
- Historical Phase 16 AKS evidence.
- Historical Phase 17H live model results.

Do not add browser checks to the pytest count.

Do not add intermediate regression runs to the accepted total.

Do not claim the frozen source/test inventory proves that the current repository is unchanged without checking the actual committed baseline.

If GitHub CI has passed on the Phase 18.2 implementation commit, record the exact run ID and commit SHA.

If not, preserve the actual status.

No need to repeat the 18-minute full regression merely for Stage 18.3 documentation.

---

# 14. Update the project roadmap and README

Update `README.md` to reflect the completed local Stage 18.2 engineering capability and the Stage 18.3 documentation decision.

The README should accurately explain that Estudio PolyMind now includes:

- The existing multi-LLM orchestration and hybrid RAG system.
- Evidence-grounded document synthesis.
- Durable document processing.
- Authorized publication and canonical citations.
- A locally verified authenticated Streamlit Documents interface.
- Selected-document Q&A.
- Synthetic offline inference.
- Local security and financial governance.
- Docker-based private document demonstration.

Do not claim a public SaaS application, general upload portal or production multi-user deployment.

Update the Phase 18 roadmap entry to distinguish:

**Assessment complete**

**Local implementation and verification complete**

**Documentation and engineering closure complete, if actually verified**

**Azure deployment not performed**

**Production readiness not established**

Maintain a link to the operator guide and Stage 18 completion decision.

Preserve existing historical Phase 17 statuses.

---

# 15. Azure and AKS decision reconciliation

The approved Phase 18.1 architecture determined:

`AKS_NOT_REQUIRED`

The selected initial cloud candidate is a small private Linux VM using Docker and persistent storage.

Stage 18.2 intentionally performed no Azure deployment.

In Stage 18.3, update the deployment documentation to distinguish:

### Completed

- Local application implementation.
- Synthetic frontend integration.
- Local authentication verification.
- Local durable processing.
- Local Docker validation.

### Not completed

- Actual Azure VM deployment.
- Current regional VM pricing verification.
- Final memory/storage sizing on an Azure VM.
- Azure network/identity configuration.
- Production backup and recovery.
- Real Azure Entra browser authentication.
- Production monitoring and availability.
- Public access.
- Distributed document authorities.

Explicitly state:

**AKS was previously validated during Phase 16, but is not required for the initial Phase 18 document application deployment.**

Do not reopen the local-first decision.

Do not infer that a future VM has already been provisioned.

Do not introduce a new cloud dependency, Azure service or paid validation requirement as part of documentation closure.

If a cloud deployment is undertaken later, it requires a separately reviewed resource, security, cost and authorization plan.

---

# 16. Phase 17 deferred obligations

Preserve the exact classifications:

```text
PHASE_17_ENGINEERING_COMPLETE
DEFERRED_PENDING_TWO_INDEPENDENT_REVIEWERS
PHASE_17_FORMAL_CLOSURE_PENDING
PHASE_17I_ENGINEERING_COMPLETE
PHASE_17I_EXTERNAL_VERIFICATION_DEFERRED
PHASE_17I_FORMAL_ACCEPTANCE_PENDING
SUBSEQUENT_ENGINEERING_PERMITTED
```

Independent human reviews remain 0/2.

Actual external-user verification has not occurred.

The new synthetic browser demonstrations do not satisfy the earlier external participant requirement.

Do not modify historical human-review rubrics, retrospectively approve participants or fabricate semantic-quality results.

Development and formal external acceptance remain distinct.

---

# 17. Phase 18 closure decision

Create a durable engineering-completion decision distinguishing:

1. Completed local engineering.
2. Completed documentation.
3. Pending operator administrative acceptance, if not explicitly granted.
4. Deferred actual Azure deployment.
5. Unestablished production readiness.
6. Existing deferred Phase 17 obligations.

Recommended classifications, subject to verified evidence:

`PHASE_18_1_ASSESSMENT_COMPLETE`

`PHASE_18_2_ENGINEERING_PASS`

`PHASE_18_2_LOCAL_INTEGRATION_PASS`

`PHASE_18_2_OFFLINE_VERIFICATION_PASS`

`PHASE_18_3_DOCUMENTATION_PASS`

`PHASE_18_ENGINEERING_COMPLETE_LOCAL_SCOPE`

`AKS_NOT_REQUIRED`

`AZURE_DEPLOYMENT_NOT_PERFORMED`

`PRODUCTION_READINESS_NOT_ESTABLISHED`

`SUBSEQUENT_ENGINEERING_PERMITTED`

Do not invent an operator signature, deployment acceptance, participant approval or production certification.

If the documentation and evidence are not sufficiently reconciled, use an explicit PARTIAL/BLOCKED classification and name the unresolved item.

The completed scope must remain clearly limited to the private, synthetic, owning-operator application.

---

# 18. Required documentation deliverables

Create or update these files.

## A. Preserved Stage 18.3 prompt

`docs/codex/prompts/phase_18_3_documentation_and_closure.md`

Preserve the Stage 18.3 instruction.

## B. Stage 18.3 technical report

`docs/codex/reports/phase_18_3_documentation_and_closure.md`

Include:

- Executive conclusion.
- Actual committed baseline.
- Phase 18.2 verification reconciliation.
- Complete documentation inventory.
- API and architecture consistency.
- Security and operations documentation.
- Current roadmap classifications.
- Deferred obligations.
- Validation results.
- Pre-commit review.
- Git disposition.

## C. Local document-demo operator guide

Preferred path:

`docs/operations/phase_18_local_document_demo.md`

Use an existing equivalent guide instead if one already exists.

Cover local initialization, login, source selection, processing, publication, Q&A, cancellation, stop, backup, restore, TLS, Docker and limitations.

## D. Phase 18 engineering-completion decision

`docs/evaluation/phase_18_engineering_completion_and_deferred_deployment.md`

Record the exact scope, evidence, acceptance boundaries and subsequent-engineering handoff.

## E. README and existing documentation

Update as appropriate:

- `README.md`
- `docs/evaluation/phase_18_implementation_and_verification_plan.md`
- `docs/security/production-security.md`
- `docs/operations/observability.md`
- Relevant existing authentication or deployment documentation.

Do not modify every historical document merely to replace historical NOT IMPLEMENTED statements.

Preserve the original dated Phase 18.1 assessments as historical decision evidence. Where reconciliation is needed, append a clearly dated implementation-status section instead of rewriting what was proposed before Stage 18.2.

Do not create duplicate documents that contradict an existing authoritative runbook.

---

# 19. Stage 18.3 validation

This is a documentation-only stage.

Run relevant read-only checks and documentation validation.

At minimum:

```bash
git status --short --branch
git diff --check
git diff --stat
git diff --cached --name-only
```

Verify:

- Markdown formatting.
- Relative links.
- Referenced anchors.
- Actual source paths.
- Real endpoint names.
- Documented commands versus implemented CLI.
- Correct authentication descriptions.
- Correct test counts.
- Current commit and CI binding.
- Exact phase classifications.
- Preservation of historical evidence.
- No accidental source changes.
- No new paid operations or provider access.
- No secrets/private keys/tokens in staged or new documentation.
- No unintentional inclusion of historical untracked files.

If a lightweight local static check is useful, run it without creating billable work or modifying project authorities.

Do not run the full regression suite, activate containers or regenerate test certificates solely to write documentation.

Do not modify implementation code to make documentation assertions pass.

If a previously unrecognized code defect is discovered, document it separately and assess whether it prevents engineering closure; do not silently expand Stage 18.3 into an implementation stage.

---

# 20. Separate pre-commit review

Perform a dedicated final review after completing the documentation edits.

Inspect:

- Every new or changed Markdown document.
- Consistency across README, roadmap and completion decision.
- Auth/security terminology.
- Local-only versus production claims.
- Cost and AKS claims.
- Historical test evidence.
- Exact supported commands.
- Retention and erasure limitations.
- Current source and configuration contracts.
- Stage 18.2 source immutability.
- Historical Phase 17 evidence.
- Git status and complete new-file inventory.

The previous report recorded 28 inherited Phase 17H untracked documents.

Confirm that these remain untouched.

Do not stage them.

Do not delete generated user data or alter runtime authority stores during cleanup.

---

# 21. Final response requirements

Report the results in this structure.

## 1. Stage 18.3 verdict

State PASS, PARTIAL or BLOCKED based on actual evidence.

## 2. Phase 18 engineering disposition

Explain the completed local engineering scope and distinguish operator formal acceptance.

## 3. Documentation deliverables

List every created and modified file.

## 4. Verified implementation baseline

Record the actual Phase 18.2 commit SHA and CI result.

## 5. Verification evidence

Record the accepted 3,128-test result and actual browser/container verification without claiming a new rerun.

## 6. Operational readiness

Explain the exact locally supported run/restore procedure and its known limitations.

## 7. Cloud architecture

Preserve `AKS_NOT_REQUIRED`, recommended private VM candidate and unperformed Azure deployment status.

## 8. Deferred acceptance

Preserve the existing Phase 17 human/user obligations and Phase 18 production/external limitations.

## 9. Remaining engineering work

Identify separately what would be required for:

- Actual Azure VM deployment.
- Real-provider application use.
- General user document uploads.
- External-user verification.
- Production multi-user operation.

Do not automatically assign another phase number or begin that work.

## 10. Git disposition

Provide:

```bash
git status --short --branch
git diff --stat
git diff --cached --name-only
```

Include all new untracked Stage 18.3 documents in the review inventory.

Suggested commit message:

`docs: finalize Phase 18 local engineering closure and deployment handoff`

Do not stage, commit or push.

---

# 22. Final instruction

Execute **Phase 18.3 — Documentation and Closure** after verifying the committed Phase 18.2 implementation baseline.

Reconcile the actual implementation, tests, security, frontend, APIs, local runtime, Docker configuration, operational recovery and cloud-deployment decision.

Produce complete, accurate documentation suitable for another engineer to reproduce the local document-intelligence application.

Close the verified local Phase 18 engineering/documentation scope without claiming production readiness, Azure deployment or external-user acceptance.

Preserve all Phase 17 deferred obligations and the approved `AKS_NOT_REQUIRED` decision.

Do not change application source code, restart cloud infrastructure, execute inference or perform unapproved external operations.

**Leave the complete Stage 18.3 documentation changes uncommitted for operator review.**

The expected result is an evidence-based engineering closure and operational handoff for Estudio PolyMind's authenticated local document application.

## Operator follow-up — Phase 18.2 committed and CI-verified

Phase 18.2 Implementation and Verification has been successfully committed and pushed to the `master` branch.

- **Commit message:** `feat(documents): implement authenticated local document frontend and verification`
- **GitHub Actions workflow:** Estudio PolyMind CI
- **Workflow run ID:** `43543837534`
- **CI status:** SUCCESS
- **Execution duration:** 9m23s
- **Local verification:** 3,128 tests passed; T01–T15 PASS.

Codex must verify the actual Phase 18.2 commit SHA using `git log` and use that commit as the baseline for Phase 18.3 Documentation and Closure.

**Phase 18.2 is committed and CI-verified. Phase 18.3 is authorized to proceed without repeating Phase 18.2 implementation or testing.**
