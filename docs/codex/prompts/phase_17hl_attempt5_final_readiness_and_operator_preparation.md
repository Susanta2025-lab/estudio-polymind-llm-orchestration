# CODEX PROMPT — ESTUDIO POLYMIND
## Phase 17H–L: Attempt 5 Final Readiness Reassessment and Operator Preparation

---

## 0. ROLE AND OBJECTIVE

Act as a Principal AI Systems Engineer, Python Reliability Engineer, Azure Foundry Integration Specialist, and Release Readiness Reviewer.

**Repository:** `Susanta2025-lab/estudio-polymind-llm-orchestration`

**Working branch:** `master`

### Primary objective

Complete a focused final readiness reassessment following the successful F1 HTTP Cleanup Failure Preservation correction.

Prepare the existing operator-authorization workflow for **Attempt 5: one governed Azure Foundry chunk-analysis diagnostic inference**.

Do not restart comprehensive engineering investigations or repeat checks that have already been satisfactorily verified.

### Execution strategy

This task has three work packages:

**WP-A — Final engineering readiness**

Verify that the F1 correction remains intact, relevant contracts are preserved, and there are no outstanding confirmed engineering blockers for the intended single-analysis execution.

**WP-B — Existing authorization evidence reconciliation**

Reuse previously verified deployment, pricing, governance, identity, budget, and capacity evidence. Identify only information that genuinely requires renewal or immediate operator confirmation.

**WP-C — Operator preparation**

Prepare a precise, non-executing operator handoff for the existing single-call authorization and execution workflow.

### Explicit restrictions

Do not:

- Execute Attempt 5.
- Perform paid inference.
- Create or sign a live approval.
- Consume an existing approval.
- Reserve live funds.
- Modify production cloud resources.
- Commit or push source code.
- Modify production implementation.
- Change prompt, schema, model configuration, or financial policies.

**The goal is readiness for operator authorization, not the authorization or execution itself.**

---

## 1. PROJECT BASELINE

The latest completed work is:

**Phase 17H–L — F1 HTTP Cleanup Failure Preservation**

Report:

`docs/codex/reports/phase_17hl_f1_http_cleanup_failure_preservation.md`

Reported results:

```text
F1 FIX: PASS

Full regression: 1755 passed
New tests: 77
Failures: 0
Errors: 0
Skipped: 0
Network attempts: 0

Paid inference calls: 0
Cloud operations: 0
```

The correction modified only:

```text
llm/bounded_http.py
llm/openai_compatible.py
```

It addressed:

- HTTP response-close errors masking primary inference failures.
- Owned-session-close errors masking primary failures.
- Cleanup-only I/O failures.
- Preservation of output-limit and configuration error classifications.

The active generation contract remained unchanged.

### Current source bindings

The latest verified fingerprints are:

**Executor**

```text
82fc01aa0447d4be758124cec0120a06db49f139f69ee6425b51b8696a6ad26f
```

**Generation source**

```text
7d387a8595cf63e2ac944a25c4987a1b37392aa4adba8889914acf51ff9f0f59
```

**Provider schema**

```text
4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2
```

**Inference configuration**

```text
7eaa6b52ad387f9f0c82e318e9c74fa378ffda0baec85d0f7157cc4ab0553519
```

Recompute these values using the repository's authoritative functions.

Do not assume they are unchanged without checking.

Do not replace existing fingerprint algorithms.

---

## 2. IMPORTANT: DO NOT REPEAT C1–C7 VERIFICATION UNNECESSARILY

The previous Attempt 5 assessment examined seven categories:

```text
C1 — Azure deployment and model compatibility
C2 — Commercial pricing
C3 — Governance authorities and funds
C4 — Operator identity and approval
C5 — Credentials and execution timing
C6 — Shared RPM/TPM capacity
C7 — Exact execution configuration
```

These topics have already been examined extensively during earlier phases.

### Required approach

**Do not perform another full C1–C7 audit.**

Instead:

1. Read the relevant previous reports.
2. Identify the latest available evidence for each condition.
3. Reuse evidence that remains applicable.
4. Do not rerun already completed static compatibility tests without a specific reason.
5. Do not repeat deployment, financial, or policy analysis merely for documentation completeness.
6. Identify only genuinely time-sensitive, source-dependent, or previously unverified information.
7. Keep operator-only checks separate from engineering readiness.

A prior report describing a condition as NOT VERIFIED does not establish that the condition has since been satisfied.

Equally, do not require the operator to repeat verification simply because the same condition was listed in an older checklist.

### Evidence-reuse classification

Use:

```text
VERIFIED — Reusable prior evidence is sufficient.

REQUIRES REFRESH — Previously verified evidence is stale,
expired, source-bound, or execution-time-dependent.

OPERATOR-OWNED — Verification requires protected operator
information unavailable to this assessment.

BLOCKED — A demonstrated condition prevents safe preparation.
```

Do not substitute assumptions for missing evidence.

Do not contact Azure, inspect protected financial stores, or retrieve credentials during this task.

### Important distinction

Static application compatibility may be established using previous offline reports.

However, expiring credentials, signed approval validity, current capacity, unresolved financial obligations, and actual source-bound execution configuration cannot be presumed valid from historical evidence.

These should become concise operator handoff checks, not another large engineering investigation.

---

## 3. REQUIRED SOURCE AND REPORT INSPECTION

Start with:

`AGENTS.md`

Review only the relevant parts of the current local working tree.

### Reports

```text
docs/codex/reports/phase_17hl_f1_http_cleanup_failure_preservation.md

docs/codex/reports/phase_17hl_attempt5_readiness_authorization_assessment.md

docs/codex/reports/phase_17hl_live_failure_observability_and_contract_options.md

docs/codex/reports/phase_17hl_ast_test_portability_fix.md

docs/codex/reports/phase_17hl_final_offline_azure_compatibility_audit.md

docs/codex/reports/phase_17hl_final_operator_authorization.md
```

Inspect additional reports only when they resolve a specific outstanding issue.

### Implementation

```text
llm/bounded_http.py
llm/openai_compatible.py
llm/structured.py
llm/azure_schema.py

documents/digestion/managed.py
documents/digestion/models.py
documents/digestion/validation.py

tests/performance/foundry_single_call.py
tests/performance/foundry_approval.py
tests/performance/foundry_budget.py

governance/execution.py
governance/evaluation.py
```

Inspect relevant authorization policy and code only as needed to construct the final operator handoff.

Do not read private approvals, credentials, signing keys, actual financial databases, or retained responses.

---

# WORK PACKAGE A — FINAL ENGINEERING READINESS

## 4. Verify F1 preservation

Confirm that the current code includes the corrected behavior.

### Response cleanup

Verify:

- A primary exception survives a subsequent expected I/O cleanup failure.
- Cleanup-only I/O failure is normalized and rejected.
- Output-limit and HTTP configuration failures retain their original categories.
- No retry is introduced.
- Response cleanup is performed once.
- No incomplete response is accepted.

### Owned-session cleanup

Verify:

- Existing primary failures survive owned-session cleanup errors.
- Externally owned sessions are not closed by the provider.
- Cleanup does not erase settled financial usage.
- Normal success behavior is unchanged.

Reuse the existing F1 regression tests.

Do not repeat the entire initial root-cause investigation.

### Residual externally owned session boundary

The single-call launcher manages its externally owned session separately.

This was already documented as a limited, nonblocking lifecycle consideration.

Confirm that it has not changed.

Do not expand the task into another session-lifecycle redesign unless a new reproducible blocker exists.

---

## 5. Confirm generation-contract preservation

Verify the following remain unchanged:

```text
managed-prompt/3
managed-generation/2
azure-strict/1
stage-result/1
```

Verify:

- Strict Azure JSON Schema.
- `reasoning_effort=low`.
- `max_completion_tokens=3000`.
- Raw response limit: 10,000 bytes.
- Canonical JSON limit: 10,000 bytes.
- HTTP envelope: 26,192 bytes.
- Deterministic claim IDs.
- Evidence and lineage validation.
- No automatic repair.
- No fallback model.
- No retry.

Confirm the inactive `managed-prompt/4` proposal remains inactive.

Do not activate the application-owned-identifier proposal.

### Fingerprint verification

Use:

```text
foundry_single_call.executor_digest()
foundry_l1.generation_contract_digest()
fingerprint(provider_schema(generation_schema()))
ManagedSynthesisInference.config
```

Record the results.

Confirm that any differences from the F1 report have a specific explanation.

Do not refresh an operator approval simply to accommodate a changed fingerprint.

---

## 6. Confirm single-call containment

Review the existing governed diagnostic runner.

Verify that Attempt 5 is still limited to:

```text
Experiment: Single chunk analysis
Maximum provider attempts: 1
Automatic retries: 0
Fallback calls: 0
Structural reduction: Not permitted
Root reduction: Not permitted
Q&A: Not permitted
```

The actual requested experiment is the first analysis chunk of the established deterministic four-page synthetic diagnostic fixture.

Do not substitute a different document.

Verify that the runner:

- Enforces the one-call ceiling before provider execution.
- Rejects duplicate execution.
- Preserves approval-consumption and replay protections.
- Retains UNKNOWN financial obligations.
- Records a sanitized terminal result.
- Stops after a single accepted or failed attempt.

Do not invoke the full four-call `foundry_l1` launcher.

---

## 7. Targeted verification only

The most recent full regression passed 1,755 tests.

Do not rerun the full suite simply to repeat evidence, unless:

- Relevant production source has changed since the verified F1 result.
- Current focused tests reveal a regression.
- An established repository policy explicitly requires a new full-suite run for this assessment.
- The recorded result cannot be matched to the current code.

Otherwise, run a focused guarded offline selection covering:

```text
tests/unit/test_http_cleanup.py
tests/integration/test_http_cleanup_governance.py
tests/integration/test_live_failure_observability.py
tests/integration/test_single_call_harness.py
tests/integration/test_single_call_preflight.py
tests/integration/test_final_offline_azure_compatibility.py
tests/unit/test_source_contracts.py
```

Use the previously verified pre-import network-denial guard.

Do not run unreviewed live-capable scripts.

Do not install packages or alter the environment.

If the focused suite passes and fingerprints match, accept the previous full-regression evidence, subject to the conditions above.

Report exactly what was executed and what was reused.

---

# WORK PACKAGE B — OPERATOR AUTHORIZATION RECONCILIATION

## 8. Reuse the established operator workflow

Do not design a new authorization system.

Reuse the existing implementation for:

- Entra v2 operator identity.
- Registered operator permissions.
- Independent RSA approval trust.
- Single-call JWS binding.
- Approval replay prevention.
- RunGuard.
- Shared admission.
- Owner/tenant financial limits.
- Sanitized one-call outcome.

The intended approval audience remains:

```text
polymind-single-analysis-live
```

Do not use the historical four-call audience.

The existing source checks, signature validation, nonce/replay rules, time windows and financial constraints remain authoritative.

Do not weaken them.

---

## 9. Prepare the current execution binding inventory

Produce a non-secret table containing the fields necessary for a future operator approval.

Include:

### Source bindings

- Current executor fingerprint.
- Current generation-source fingerprint.
- Current provider-schema fingerprint.
- Current inference-configuration fingerprint.

### Execution identity and scope

- Single-call executor/version.
- Intended experiment purpose.
- Requested model/deployment.
- Scope-dependent configuration fields.
- Operator-controlled identity and authority requirements.

Do not invent private identities or actual scope UUIDs.

### Provider configuration

Verify from current code:

```text
Resource: epolymind-foundry-dev-susanta
Deployment: epolymind-gpt-54-mini
Model: gpt-5.4-mini
Model version: 2026-03-17
SKU: GlobalStandard

Interface: Azure OpenAI v1 Chat Completions
Strict schema: true
Reasoning effort: low
```

These are intended configuration values, not fresh verification of cloud resource state.

### Token and response ceilings

```text
Maximum calls: 1

Maximum input reservation: 25000 tokens
Maximum completion: 3000 tokens

Raw content: 10000 bytes
Canonical JSON: 10000 bytes
HTTP envelope: 26192 bytes
```

### Financial binding

Reuse the existing approved contract structure and its validated cost limits.

Do not replace the pinned pricing catalog.

Do not treat the synthetic pricing fixture as a current commercial quotation.

Do not claim that a historical EUR ceiling is presently authorized expenditure.

### Request-specific bindings

Identify which fields cannot be finalized without:

- The real verified operator scope.
- The current private execution configuration.
- Actual-scope fixture and rendered-request digests.
- Current authority references.
- Current approval and execution windows.

Report these as operator-owned inputs.

Do not fill them with synthetic placeholder UUIDs that might be mistaken for executable values.

---

## 10. Prepare a minimal operator checklist

Create a concise checklist, referencing the existing instructions instead of repeating their full contents.

It should establish the sequence for a future authorized operation:

1. Review final source fingerprints and configuration.
2. Confirm that previously established deployment/pricing/capacity evidence is still applicable.
3. Confirm existing authorities, financial allowances and unresolved obligations.
4. Establish the actual operator identity and protected execution configuration.
5. Obtain or verify a fresh exact-source-bound approval through the independent signing workflow.
6. Confirm approval, credentials and time-window validity immediately before any future launch.
7. Execute at most one governed analysis call, only after explicit user authorization.
8. Inspect the sanitized outcome and durable accounting result.
9. Stop after the single call, regardless of success or failure.

Do not turn this checklist into an automatically executing script.

Do not construct or sign a real JWS.

Do not consume an approval.

Do not access protected operator records.

---

# WORK PACKAGE C — FINAL READINESS DECISION AND HANDOFF

## 11. Readiness decision

Determine whether the F1 engineering blocker has been resolved and whether any additional confirmed engineering defect prevents safe single-analysis preparation.

Use the following outcomes.

### ENGINEERING GO

Use when:

- F1 is resolved.
- Current source bindings are reconciled.
- Generation contract is unchanged.
- Focused tests pass.
- The one-call limit remains enforced.
- Governance and sanitized diagnostics remain intact.
- No confirmed engineering blocker remains.

This does not establish current execution authorization.

### ENGINEERING CONDITIONAL GO

Use when engineering checks pass but a specific unresolved technical prerequisite must be completed before approval.

Identify the exact condition without repeating all historical C1–C7 descriptions.

### ENGINEERING NO-GO

Use only if a demonstrated unresolved engineering or safety blocker remains.

Describe the code location, evidence and smallest required correction.

### Separate operator status

Always report independently:

```text
OPERATOR PREPARATION:
READY / PARTIAL / BLOCKED

EXECUTION AUTHORIZED NOW:
YES / NO / NOT VERIFIED
```

Do not report execution authorized unless the existing complete approval process has legitimately established it.

This task is not permitted to create that authorization.

---

## 12. Documentation deliverables

Create:

```text
docs/codex/reports/phase_17hl_attempt5_final_readiness_and_operator_preparation.md
```

Save the prompt under:

```text
docs/codex/prompts/phase_17hl_attempt5_final_readiness_and_operator_preparation.md
```

The report must contain:

### A. Executive summary

- Engineering readiness.
- Operator-preparation status.
- Execution-authorization status.
- Outstanding engineering blockers, if any.

### B. F1 closure

- Confirmation of corrected behavior.
- Relevant regression results.
- Any remaining limitations.

### C. Current source bindings

- Executor fingerprint.
- Generation-source fingerprint.
- Provider-schema fingerprint.
- Inference-configuration fingerprint.
- Comparison with the F1 report.

### D. Preserved generation contract

Confirm the active prompt, schema, limits, model and request payload.

### E. Single-call safety

Confirm actual-attempt containment, no retries, no fallback, replay protection and financial accounting.

### F. Reused operator evidence

Use a compact table:

```text
Condition | Latest evidence | Reusable / Refresh /
Operator-owned / Blocked | Required next action
```

Do not reproduce all earlier assessments.

### G. Operator preparation

Identify exactly what is ready and what requires protected operator action.

### H. Test results

Separate newly executed checks from previously verified evidence.

### I. Final decision

Provide a clear readiness verdict and remaining operator steps.

---

## 13. REPOSITORY, SECURITY AND FINANCIAL RESTRICTIONS

### Git

Remain on the existing `master` branch.

Do not:

- Create branches.
- Commit.
- Push.
- Stage.
- Reset.
- Clean.
- Restore.
- Stash.
- Rebase.
- Merge.
- Remove untracked files.
- Overwrite historical reports.

Preserve all current Phase 17H–L modifications.

### Source code

Do not modify production implementation or tests.

Do not change:

- Azure provider configuration.
- Generation instructions.
- Validation contracts.
- Prompt versions.
- Fingerprints or fingerprint algorithms.
- Approval policies.
- Operator identities.
- Financial limits.
- RunGuard.
- Retry behavior.

### Cloud

Do not:

- Call Azure inference.
- Use Azure CLI against live resources.
- Provision or change cloud services.
- Execute the live single-call launcher.
- Reserve live funds.
- Query protected billing or operator databases.
- Sign or consume approvals.

### Privacy

Do not read or disclose:

- Private credentials.
- Real dotenv files.
- API keys.
- Entra access tokens.
- Private signing keys.
- Protected approval contents.
- Raw inference responses.
- Real document material.

Only report sanitized, non-secret information.

---

## 14. REQUIRED FINAL CODEX RESPONSE

Return the following concise handoff.

```text
TASK:
Phase 17H–L — Attempt 5 Final Readiness
and Operator Preparation

BRANCH:
HEAD:

F1:
Status:
Response cleanup:
Owned-session cleanup:
Focused regression:

CONTRACT:
Active prompt:
Generation schema:
Model/deployment:
Single-call limit:
Retries:
Fallbacks:

FINGERPRINTS:
Executor:
Generation source:
Provider schema:
Inference configuration:
Matches latest F1 report:

TESTING:
Previous full regression: 1755 passed
New focused tests executed:
Failures:
Errors:
Skipped:
Network attempts:

OPERATOR PREPARATION:
Previously verified evidence reused:
Evidence requiring refresh:
Operator-owned requirements:
Current configuration readiness:
Fresh source-bound approval needed:

SAFETY:
Paid inference calls: 0
Cloud operations: 0
Financial reservations: 0
Approval signing/consumption: 0
Production modifications: 0
Commits: 0
Pushes: 0

ENGINEERING READINESS:
GO / CONDITIONAL GO / NO-GO

OPERATOR PREPARATION:
READY / PARTIAL / BLOCKED

EXECUTION AUTHORIZED NOW:
NO / NOT VERIFIED

REMAINING BLOCKERS:
NEXT OPERATOR ACTION:
REPORT PATH:
```

---

## FINAL INSTRUCTION

Do not restart broad development, auditing or compatibility testing.

The previous 1,755-test regression and extensive C1–C7 assessments are reusable evidence where still applicable.

Focus exclusively on:

1. Confirming the completed F1 correction.
2. Reconciling the final source fingerprints.
3. Verifying that the strict generation contract remains frozen.
4. Confirming exactly-one-call containment.
5. Preparing the existing operator authorization workflow.
6. Identifying only genuinely outstanding or time-sensitive operator requirements.

**Do not create or sign an approval, and do not execute Attempt 5.**

The expected deliverable is a short, evidence-based final readiness report and an actionable operator handoff—not another general engineering audit.

Phase 17H remains PARTIAL until live-model acceptance and the remaining evaluation requirements have been demonstrated.
