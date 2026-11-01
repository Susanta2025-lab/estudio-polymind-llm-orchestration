# CODEX IMPLEMENTATION PROMPT
# ESTUDIO POLYMIND — PHASE 17H–L
## F1: HTTP Cleanup Failure Preservation and Regression Verification

## 0. ROLE AND PRIMARY OBJECTIVE

Act as a **Principal Python Engineer, AI Inference Reliability Specialist, HTTP Transport Engineer and Independent Software Quality Reviewer**.

**Project:** Estudio PolyMind
**Repository:** `Susanta2025-lab/estudio-polymind-llm-orchestration`
**Expected branch:** `master`

Implement the smallest safe correction for **F1 — HTTP response cleanup can mask an existing inference failure**, identified during the Attempt 5 readiness and authorization assessment dated 23 October 2026. Current technical readiness is **NO-GO — one confirmed engineering blocker**.

The unguarded `response.close()` in `request_json()`'s `finally` block can replace a normalized inference exception with a cleanup exception, losing the primary diagnostic category.

Required result:

1. A primary inference failure survives response cleanup failure.
2. Cleanup-only failure fails closed with an appropriate sanitized error.
3. No incomplete or invalid response is accepted.
4. Cleanup exceptions do not trigger another provider request.
5. Existing one-call governance and accounting behavior remains unchanged.
6. The active Azure generation contract remains unchanged.
7. Offline regressions cover response-close and owned session-close failure paths.

This is a narrowly scoped implementation task, not a new architecture or broad hardening phase.

## 1. REQUIRED INITIAL INSPECTION

Read `AGENTS.md`, then inspect the latest actual local working-tree source.

Primary implementation:

- `llm/bounded_http.py`
- `llm/openai_compatible.py`
- `llm/inference.py`
- `llm/structured.py`

Provider lifecycle and governance:

- `llm/admission.py`
- `governance/execution.py`
- `governance/ledger.py`
- `tests/performance/foundry_single_call.py`

Relevant tests:

- `tests/unit/test_structured_provider.py`
- `tests/unit/test_output_limit_diagnostics.py`
- `tests/unit/test_single_call_diagnostics.py`
- `tests/integration/test_live_failure_observability.py`
- `tests/integration/test_single_call_harness.py`
- `tests/integration/test_single_call_preflight.py`

Locate existing tests for `request_json()`, redirects, provider timeouts, HTTP envelope limits, output-limit classification, `requests.Response.close()`, owned `requests.Session.close()`, known/unknown usage accounting, cleanup-error precedence and one-call execution containment.

Read:

- `docs/codex/reports/phase_17hl_attempt5_readiness_authorization_assessment.md`
- `docs/codex/reports/phase_17hl_live_failure_observability_and_contract_options.md`
- `docs/codex/reports/phase_17hl_ast_test_portability_fix.md`
- `docs/codex/reports/phase_17hl_final_offline_azure_compatibility_audit.md`

These establish prior contracts, test baselines and the F1 reproduction. Do not rely on older committed GitHub source when newer local code exists.

## 2. CONFIRMED F1 DEFECT

The problematic implementation in `llm/bounded_http.py`, inside `request_json()`, is:

```python
finally:
    if response is not None:
        response.close()
```

A cleanup exception can replace an exception already propagating from the protected block.

The readiness report used the installed real `requests.Response` with a synthetic raw stream whose `close()` raises `OSError`:

| Scenario | Normal cleanup | Failing cleanup |
|---|---|---|
| HTTP 302 redirect | `inference_configuration` | `worker_failed` |
| HTTP 200 with oversized 26,193-byte envelope | `inference_output_limit` | `worker_failed` |

The intended envelope ceiling is 26,192 bytes. The original output-limit classification disappeared. The governed single-call harness still reported one attempted request, terminal failure, no second inference, UNKNOWN financial obligation and `accounting_failed=true`.

This establishes a diagnostic reliability defect. It does not establish unauthorized spending, an accounting refund, a privacy leak, or the cause of a previous Azure attempt.

Outer governance cleanup already preserves known primary inference failures. F1 occurs earlier, so governance receives the replacement cleanup exception. Correct this earlier boundary; do not merely modify the public classifier.

## WORK PACKAGE A — MINIMAL HTTP RESPONSE CLEANUP CORRECTION

## 3. Preserve the primary exception

Guarantee:

- **A: Primary inference failure, cleanup succeeds.** Retain the original normalized exception, using actual source classes/categories (`inference_configuration`, `inference_output_limit`, `inference_timeout`, `inference_invalid_response`).
- **B: Primary failure and cleanup failure.** Preserve exact type, internal category, fixed diagnostic metadata and public classification. Do not replace with `OSError`, `worker_failed` or unrelated category, expose cleanup prose, request again, or return success.
- **C: Successful response processing, cleanup fails.** Fail closed using an existing appropriate sanitized transport/protocol exception after inspecting the taxonomy. No new public category without separate justification; no fabricated usage.
- **D: Processing and cleanup succeed.** Preserve successful return behavior exactly, without additional parsing, validation, content transformation or request mutation.
- **E: No response object.** Preserve original behavior and never close an uninitialized response.

Choose the smallest correct exception-handling pattern after examining control flow. Explicit primary tracking or guarded cleanup may be appropriate. Verify exceptions during `post()`, status evaluation, body iteration, JSON decoding, size enforcement and cleanup.

Do not convert cancellation, process-exit or unrelated `BaseException` subclasses into ordinary retryable provider errors. Do not suppress arbitrary exceptions in a way that obscures programming defects. Document exactly which cleanup exception types are intercepted and why.

Cleanup sanitization must exclude URL credentials, headers, API keys, provider response text, document content, arbitrary exception messages, source UUIDs and model prose. Use existing content-free normalized categories. Check that public and audit boundaries sanitize chained exceptions.

Preserve the HTTP contract:

- `requests.post(..., stream=True)` and `allow_redirects=False`.
- Existing timeouts and total-deadline behavior.
- Envelope byte enforcement and bounded reading.
- HTTP status classification and sanitized rejection diagnostics.
- Duplicate/malformed JSON treatment.
- Request headers and provider authentication.

The socket-read versus true absolute wall-clock deadline distinction is outside F1. Do not redesign transport/deadlines.

## WORK PACKAGE B — REVIEW OWNED SESSION CLEANUP

## 4. Inspect the session lifecycle

Locate creation, ownership and cleanup of `OpenAICompatibleProvider`'s session, including `session.close()` and context managers. Determine whether cleanup can mask a primary `InferenceError`, replace output-limit/timeout, turn success into unclassified failure, expose requests exceptions, alter accounting observations or cause another call.

Owned adapter cleanup must use the same primary-preservation policy. Do not close externally owned sessions contrary to the existing contract, introduce double-close, or unnecessarily change lifetime.

If an analogous owned-session defect exists, implement the smallest correction. Otherwise document inspected behavior. Do not expand to unrelated lifecycle management.

## WORK PACKAGE C — TARGETED OFFLINE REGRESSION TESTS

## 5. Test real requests.Response behavior

Use actual installed responses with synthetic in-memory bodies/raw streams; no network. Historical reproduction used a `BytesIO` subclass whose `close()` raises `OSError`. Reproduce before editing where practical, then verify the correction.

Mandatory response-close matrix:

| Scenario | Cleanup | Expected |
|---|---|---|
| HTTP redirect | Normal | Existing configuration failure |
| HTTP redirect | OSError | Same primary configuration failure |
| Oversized envelope | Normal | Existing output-limit failure |
| Oversized envelope | OSError | Same primary output-limit failure |
| Timeout after response acquisition | Raises | Original timeout retained |
| Malformed response JSON | Raises | Original normalized protocol/decoding failure |
| Valid bounded response | Normal | Existing success |
| Valid bounded response | Raises | Sanitized cleanup-only failure |
| Request failure before response exists | N/A | Existing primary failure |

If a scenario is unreachable, document why and test the nearest reachable boundary instead of inventing unsupported behavior.

For combined failures assert exact exception class, existing category and public classification, no raw exception, no successful return and no second `post()`.

For cleanup-only failure assert terminal failure, content-free category, no accepted result, no retry and no fabricated usage.

Owned-session tests must include provider failure plus failing close, provider success plus failing close, failure plus normal close and normal success/close. Preserve ownership exactly.

## 6. Provider and single-call integration verification

Exercise corrected transport through the real adapter using synthetic offline HTTP objects. Verify original normalized errors reach the adapter, output-limit is not converted to generic protocol failure, public single-call categories survive, established observations remain available, unknown usage stays unknown, financial accounting stays fail-closed, and `accounting_failed` matches the actual state.

Verify RunGuard counts attempts, terminates after one permitted request, introduces no retry/fallback and makes no reduction, publication, Q&A or embedding call.

Repeat the original four real-Response observations. Expected after correction:

```text
HTTP 302 + normal cleanup: inference_configuration
HTTP 302 + failing cleanup: inference_configuration
Oversized envelope + normal cleanup: inference_output_limit
Oversized envelope + failing cleanup: inference_output_limit
```

Retain original financial behavior for unknown usage. Cleanup failure is not a billable second call.

## WORK PACKAGE D — CONTRACT AND GOVERNANCE PRESERVATION

## 7. Freeze production generation behavior

Do not modify:

```text
documents/digestion/managed.py
documents/digestion/models.py
documents/digestion/validation.py
documents/digestion/codec.py
documents/digestion/diagnostics.py
llm/azure_schema.py
llm/structured.py
```

Do not change `managed-prompt/3`, `managed-generation/2`, `azure-strict/1`, StageResult, claim identity, evidence/lineage validation, application limits, request payload, model selection, reasoning effort, token ceilings, prompts/versions, authentication, admission, financial policy or retry policy.

Keep `managed-prompt/4` inactive and application-owned identifiers unimplemented. Preserve `ProviderResultMetadata`; modify propagation only if directly necessary for cleanup precedence. Do not store raw model responses.

Verify known usage settles before application validation, missing/invalid usage is never zero, UNKNOWN obligations stay durable, cleanup never refunds/erases charges, settlement preserves the primary failure and cleanup does not make a run retryable. Do not modify real authority databases.

## WORK PACKAGE E — FINGERPRINT RECONCILIATION

## 8. Recompute source bindings

Historical pre-F1 values:

```text
Executor: de11d7cbeb269591caa607494d29a76b894bd48af15d17ab2095ffb51b96e598
Generation source: 4c37473513e2f1455cfa44a84c687b661a484e2fea0a390dedf9396269610d05
Provider schema: 4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2
Inference configuration: 7eaa6b52ad387f9f0c82e318e9c74fa378ffda0baec85d0f7157cc4ab0553519
```

Recompute all four with authoritative repository functions; never hardcode replacement values. Executor and generation-source hashes may change because bounded_http participates. Schema should remain unchanged; inference configuration should remain unchanged if binding/configuration is unchanged. Verify.

Confirm byte-for-byte deterministic request/payload preservation with existing frozen oracles for chunk, intermediate where applicable, structural and root: complete GenerationRequest, payload, strict schema, active renderer source, prompt template, model/capability bindings.

Source changes may invalidate approvals. Do not reuse old fingerprints, re-sign approvals, generate approvals, alter policies or claim authorization. Fresh bindings must be evaluated after source review.

## WORK PACKAGE F — OFFLINE REGRESSION VERIFICATION

## 9. Baseline

Latest full baseline:

```text
1678 passed
0 failures
0 errors
0 skips
42 existing warnings
0 observed network attempts
```

Preserve every existing test and add meaningful F1 cases. Passing count must increase by the actual new cases.

Run focused cleanup, redirect, envelope, output-limit, timeout, session, metadata, single-call, governance, unknown-accounting and containment coverage using the existing environment.

Run the complete suite with the existing inspected pre-import network-denial setup. Never execute an unreviewed Azure-capable script. Record passes, failures, errors, skips, warnings, attempts, exact command, Python/environment and execution status.

Run applicable:

```bash
ruff check <changed-python-files>
ruff format --check <changed-python-files>
git diff --check
git status --short --branch
git diff --stat
git diff --cached --name-only
```

Compile without writing bytecode into the repository. Preserve unrelated formatting/lint debt and distinguish it from task findings.

## 10. STRICT GIT, CLOUD AND SECURITY RULES

Work on existing `master`. Do not branch, commit, push, stage, reset, restore, clean, stash, rebase, merge, rewrite historical reports, delete untracked files or discard existing work. Capture starting/final Git state; preserve substantial uncommitted Phase 17H–L work.

No Azure/OpenAI inference, cloud API calls, Azure CLI remote operations, deployment changes, provisioning, live financial reservations, approval creation/signing/consumption or live tests. All tests use synthetic fixtures.

Do not inspect/disclose real dotenv, keys, credentials, Entra tokens, private approval packets/signing keys, raw historical responses or real documents. Never add raw-response logging.

## 11. IMPLEMENTATION SCOPE

Production modifications only where directly needed:

- `llm/bounded_http.py`.
- `llm/openai_compatible.py` only if owned session lifecycle needs correction.

Create/update focused tests, task prompt and report. Do not alter generation contracts, validators, cloud config, governance/security policies, financial limits, approval verification, durable jobs, model configuration, prompt versions, schema conversion or general RAG.

If larger architecture is required, implement only independently safe narrow work and report the blocker. Do not expand scope without authorization.

## 12. INDEPENDENT SELF-REVIEW

After implementation, separately review and answer with evidence:

1. Can response cleanup mask an active normalized inference exception?
2. Can session cleanup mask the primary failure?
3. Can cleanup-only failure incorrectly return success?
4. Can cleanup trigger retry?
5. Is a second HTTP request possible?
6. Can normalized output-limit become worker_failed?
7. Are status categories preserved?
8. Are byte limits unchanged?
9. Is incomplete output rejected?
10. Is known usage preserved?
11. Does unknown usage stay fail-closed?
12. Are audits content-free?
13. Did any payload change?
14. Did generation instructions change?
15. Did StageResult validators change?
16. Did governance/authorization change?
17. Do new tests detect the original defect?
18. Are source-contract protections preserved?
19. Are fingerprint changes accurately explained?
20. Are old approvals potentially stale?

Fix regressions only within scope. Passing tests do not certify live readiness.

## 13. REQUIRED DOCUMENTATION

Create:

- `docs/codex/reports/phase_17hl_f1_http_cleanup_failure_preservation.md`
- `docs/codex/prompts/phase_17hl_f1_http_cleanup_failure_preservation.md`

The report must explain executive result, F1 status/blockers/offline/live implications; exact root cause and Python precedence/reproduction/response-session differences; files/approach/minimality/taxonomy/primary and cleanup-only handling; transport/provider/governed/accounting/full-suite/network verification; request/schema/validators/fingerprints; external Azure/pricing/budget/approval/shared-capacity/Attempt 5 limitations; starting/final Git inventories and no staging/commit/push/paid inference/cloud operations.

## 14. ACCEPTANCE CRITERIA

Declare **F1 FIX PASS** only if all are satisfied:

- Primary errors survive response and owned-session cleanup failure.
- Cleanup-only failures fail closed; no raw cleanup exception reaches public audit.
- Redirect/output-limit cases preserve categories; success remains success and invalid output is rejected.
- One provider attempt maximum, no retry/fallback, correct obligations, known usage retained, unknown stays unknown, safe termination.
- Prompt/strict schema/StageResult/validators/payload/model config preserved; hash changes explained.
- All 1,678 previous tests and new cases pass, no skipped/weakened tests, no network attempts, no new lint findings, production edits limited to permitted scope.
- No paid call, operator approval, live reservation, deployment change, commit or push.

Otherwise report PARTIAL or FAIL with exact reasons.

## 15. REQUIRED FINAL CODEX HANDOFF

```text
TASK:
Phase 17H–L — F1 HTTP Cleanup Failure Preservation

BRANCH:
HEAD:
STARTING WORKTREE:

F1 ROOT CAUSE:
Confirmed:
Affected function:
Exception-precedence mechanism:

IMPLEMENTATION:
Response-close correction:
Session-close correction:
Cleanup-only handling:
Original failure preservation:
Files modified:
Files created:

REGRESSION:
Redirect + cleanup failure:
Output-limit + cleanup failure:
Timeout + cleanup failure:
Malformed JSON + cleanup failure:
Success + cleanup failure:
Owned session-close failure:
Original four-case reproduction:
Additional synthetic tests:

GOVERNANCE:
Actual provider attempts:
Retries:
Fallbacks:
Known-usage accounting:
Unknown-usage accounting:
Terminal failure handling:

CONTRACTS:
Active prompt:
StageResult schema:
Domain validators:
Provider request payload:
Provider schema:

FINGERPRINTS:
Executor before:
Executor after:
Generation source before:
Generation source after:
Provider schema before:
Provider schema after:
Inference configuration before:
Inference configuration after:

TESTING:
Previous baseline: 1678
New tests:
Full regression:
Failures:
Errors:
Skipped:
Warnings:
Network attempts:
Ruff:
Compilation:

SAFETY:
Paid inference calls: 0
Cloud operations: 0
Live financial reservations: 0
Operator approvals created: 0
Approval signatures: 0
Commits: 0
Pushes: 0

REMAINING BLOCKERS:
EXTERNAL OPERATOR CONDITIONS:
REPORT PATH:

FINAL VERDICT:
F1 FIX PASS / PARTIAL / FAIL

ATTEMPT 5 EXECUTION AUTHORIZED:
NO
```

## FINAL INSTRUCTION

Correct only F1 and any directly equivalent owned-session defect. Preserve normalized primary errors; fail closed with sanitized cleanup-only errors. Do not change generation instructions, schemas, model config, validators, finance or retry policy. Run targeted and complete offline regressions; recompute authoritative fingerprints.

**Do not execute Attempt 5. Do not create or sign operator approval. Do not commit or push.**

The objective is removing the single confirmed engineering blocker. Phase 17H remains PARTIAL until live-model acceptance and remaining evaluation requirements are demonstrated.
