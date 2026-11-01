# Estudio PolyMind — Phase 17H-L L1 Live Evaluation: Three-Attempt Postmortem

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](../../codex/reports/phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

**Prepared:** 16 October 2026\
**Suggested repository destination:** `docs/engineering/postmortems/phase17hl_l1_three_attempts_2026-10.md`\
**Status:** Three real-model L1 attempts failed; offline root causes/evidence preserved; **Phase 17H live quality remains unvalidated**.\
**Purpose:** Permanent engineering record and reusable guardrails for Estudio PolyMind and future LLM/RAG/document-intelligence projects.

> **Evidence boundary:** The conclusions below distinguish confirmed root causes from hypotheses. No subsequent live experiment, Azure modification, or change to the user's repository was performed in producing this document. Private response text, credentials, exact owner/tenant IDs, RSA approvals, and ledger contents are intentionally omitted. Financial numbers below are application-ledger settlements using the project’s approved EUR catalog, not an independent Azure invoice.

## 1. Executive summary

Three attempts to process the **same deterministic 4-page PDF** using the Azure Foundry deployment `epolymind-gpt-54-mini` (`gpt-5.4-mini`, model version `2026-03-17`, GlobalStandard, Spain Central) stopped after **one billable model call each**. The intended four-call sequence was **chunk analysis → reduction 1 → reduction 2 → grounded Q&A**. Neither a complete live digest nor a successful end-to-end live Q&A was produced.

| Attempt | Date (2026) | Provider outcome | Terminal job category | Verified interpretation | Input / output tokens | Actual settled inference cost |
|---|---|---|---|---|---:|---:|
| **L1-1** | 15 Oct | `success` | `extraction_limit_exceeded` | Valid model result became **3,471 canonical bytes** after default expansion, exceeding the **3,000-byte canonical ceiling**. Misclassified by legacy error mapping. | 1,845 / 1,460 | €0.00699907602956752 |
| **L1-2** | 15 Oct | `output_limit` | `governance_denied` | Original provider output-limit error **masked** by `RunGuard.finish`. Historical audit did **not** preserve enough data to establish byte overflow versus model completion truncation. | 1,955 / 1,922 | €0.00890113516367529 |
| **L1-3** | 16 Oct | `success` | `serialization_error` | **Nine strict schema-validation errors:** malformed evidence UUID in second claim plus eight forbidden `unused1`–`unused8` top-level fields. Not a JSON serialization or byte-limit failure. | 1,994 / 932 | €0.005006599788807204 |
| **Total** | 15–16 Oct | **3 billable calls** | **3 FAILED jobs** | No automatic retry; no downstream stage reached | **5,794 / 4,314** | **€0.020906810982050014** |

**Total tokens reported:** 10,108 (= 5,794 input + 4,314 output). These are *actual* tokens used, not the larger authorization/reservation envelopes. All three calls were financially **SETTLED**. Failure after inference does not cancel provider charges.

## 2. Common test context

- **Fixture:** `phase17h-pdf/1`, seed `1708`, 4 physical pages, six low-density lines/page. PDF SHA-256: `1be99e19a56040fb55c74682a19f874d4d4573f18d9f52a9a7ae19c8158ea92d`.
- **Extracted material:** 1,491 characters; four document pieces grouped into one chunk; includes a page-3 adversarial instruction-injection example.
- **Intended execution:** 4 LLM calls total, no retry and no fallback, ≥61 seconds between calls. Each attempt stopped after call 1 in analysis/normalization.
- **Completion reservation:** 3,000 output tokens/call; 25,000 input tokens/call, four-call aggregate at most 100,000 input / 12,000 output reserved tokens; 28,000-token planning context.
- **Cost catalog:** `phase17hl-pricing-eur-202610/1`; €0.659978880676 per million input tokens and €3.959873284055 per million output tokens. Max planned inference reservation for a full four-call run: €0.11351636747626; monthly policy ceiling €5.
- **Important distinction:** Model *completion tokens*, raw provider *UTF-8 response bytes*, canonical application *ASCII JSON bytes*, and the HTTP *transport envelope bytes* are independent constraints. Do not equate them numerically.

## 3. Incident L1-1 — Canonical JSON expansion (confirmed)

**Observed:** The Azure call succeeded and returned valid, schema-compatible JSON containing eight claims. The provider-content response measured **2,597 UTF-8 bytes**, within the original 3,000-byte content limit. Pydantic inserted omitted default fields (including `schema_version`, claim lineage/qualifications/stance/status), adding **874 bytes** when canonically encoded. Canonical ASCII JSON measured **3,471 bytes**, **471 bytes (15.7%) over the 3,000-byte canonical bound**.

**Exact failure path:** `documents/digestion/validation.py:validate_result()` rejected `len(encode(result)) > profile.max_result_characters` with `DigestionError('synthesis_limit_exceeded')`. Legacy classification surfaced **`extraction_limit_exceeded`** despite extraction and provider execution having succeeded. Offline replay reproduced the error; bypassing only the limit for inspection showed other structural and evidence checks would have passed, but **no bypass was persisted**.

**Underlying design error:** A canonical serialization budget was undersized and conflated with the raw response budget and completion-token reservation. Prompt-level omission of defaults made raw and canonical sizes diverge; a misleading terminal category delayed diagnosis.

**Corrections completed afterward:**

1. A managed prompt revision originally requested explicit default/schema fields.
2. Independent **10,000-byte provider-content and 10,000-byte canonical-result limits** were implemented and validated offline, while keeping **3,000 completion tokens** (`managed-prompt/3`).
3. Boundary tests covered default expansion, evidence/lineage payloads, Unicode escaping, and over-limit rejection; no schema/evidence validator was disabled.

**Forward prevention:** Measure both raw UTF-8 size **and** post-Pydantic canonical size with worst-case/representative payloads *before* live inference. Require byte-budget headroom for default expansion, evidence lists, qualifications, conflicts and lineage. Error taxonomy should identify `canonical_result_size_exceeded`, not extraction failure.

## 4. Incident L1-2 — Output-limit error obscured by governance error (partially diagnosed)

**Observed:** A second billable inference call stopped with provider outcome **`output_limit`** and terminal category **`governance_denied`**; reported usage was **1,955 input + 1,922 output tokens**, settled for **€0.00890113516367529**.

**Confirmed code defect:** `llm/bounded_http.py:result_text()` could raise `InferenceOutputLimitError` for either raw provider content exceeding **3,000 UTF-8 bytes** or a provider finish reason such as `length`/`max_tokens`. The old audit recorded **neither the raw response byte count nor the finish reason**. Subsequently, `tests/performance/foundry_budget.py:RunGuard.finish()` raised `GovernanceError` after an already-settled failed call, **masking the original provider exception**. The displayed `governance_denied` was *not* proof of a genuine owner/tenant quota denial.

**What cannot be concluded:** The exact trigger—**content byte overflow versus provider completion truncation**—is unrecoverable from preserved Attempt 2 evidence. **1,922 output tokens is below the 3,000-token ceiling**, but this fact alone does not identify the trigger. Do **not** retroactively label it a token-limit failure or a byte-limit failure.

**Corrections completed afterward:**

1. Added provider-neutral **`OutputLimitDiagnostics`**, preserving sanitized `failure_cause`, response byte measurements/limits (when available), finish reason, usage availability, completion/reasoning tokens, and configured limits.
2. Audited failures retain content-free output diagnostics, without storing private failed response text.
3. `RunGuard.finish()` no longer replaces a known, settled provider error merely because the call failed; genuine accounting problems and unknown usage remain fail-closed.
4. Provider/canonical size limits later became separately configurable at **10,000 bytes**; the 3,000-token ceiling was retained.

**Forward prevention:** Preserve the **original causal error** through accounting and worker layers. Record structured, content-free provider metadata **at the boundary before discarding the envelope**. Keep provider, application validation, governance admission, financial settlement and launcher status as separate concepts. Never infer a missing metric.

## 5. Incident L1-3 — Invalid structured output, not a serializer bug (confirmed)

**Observed:** Under `managed-prompt/3` and the independent **10,000/10,000-byte** limits, the model returned **valid JSON** with four claims, **2,144 UTF-8 response bytes** and usage **1,994 input + 932 output tokens**. The provider call succeeded; ledger settlement was **€0.005006599788807204**. Downstream validation produced **nine Pydantic errors**:

- `claims.1.evidence_ids.0`: `uuid_parsing` — invalid group 4 length (expected 12, found 13), therefore the evidence identifier was malformed.
- `unused1`, `unused2`, …, `unused8`: each `extra_forbidden` — these top-level fields are not in `stage-result/1`, even though their values were `null`.

**Exact failure path:** `documents.digestion.codec.decode()` parsed valid JSON, then `StageResult.model_validate(...)` raised Pydantic `ValidationError`. `decode()` wrapped it in `DigestionError('inference_contract_error')`. Legacy taxonomy exposed **`serialization_error` / `NON_RETRYABLE`**, even though canonical encoding **had not yet been reached**. Evidence/lineage/coverage validation and checkpoint write were never reached. A replay of the preserved provider response confirmed this path. Seven focused offline regression tests passed.

**Why not simply “fix the JSON”?** Deleting the eight fields **and** altering the UUID would modify model-generated content and evidence references. An in-memory counterfactual with both changes validated and serialized (2,023 canonical ASCII bytes), but this was **diagnostic only**, not permitted runtime repair. Either single change alone still failed. The original strict rejection was correct.

**Design limitation uncovered:** The capability requested **`structured_output='json_object'`**; this asks for a JSON object but **does not enforce the full `StageResult` schema at generation time**. `managed-prompt/3` conveyed the schema in text. The model violated it. The application-side Pydantic validation behaved as designed.

**Next improvement to assess, not yet implemented:** Verify the actual Azure deployment and OpenAI-compatible adapter support for a suitable schema-constrained response mode (e.g., `json_schema` with strict enforcement), including accepted schema subset and deployment behavior. If verified, use **provider-side structural constraints plus unchanged strict application validation**. Provider-side constraints still cannot prove that evidence UUIDs **belong to the supplied evidence set** or that factual claims are semantically grounded: perform membership, coverage, qualification, lineage, ordering, and prompt-injection checks locally.

**Separate CLI defect:** The launcher printed `{"state":"FAILED"}` but exited with **code 0**, because failed jobs returned a result normally and only raised exceptions became nonzero process exits. Fix in a separate focused change: after saving audit/finalizing accounting, unsuccessful terminal state should map to a nonzero CLI code; regression-test shell exit behavior. This is **not** the cause of the schema failure.

## 6. Preventive engineering rules for future AI projects

These are reusable **design and test requirements**, not claims that every measure has already been implemented.

| ID | Rule | Required proof/check |
|---|---|---|
| **LLM-01** | Treat *valid JSON* and *schema-valid JSON* as different states. | Test JSON that parses but violates required fields, types, UUID format and `extra='forbid'`. |
| **LLM-02** | Prefer provider-enforced structured output **when supported and verified**, but never replace application validation with it. | Provider capability matrix, accepted schema subset, strict response tests, fallback behavior explicitly documented (not silent). |
| **LLM-03** | Enforce evidence IDs and citation lineage against the **actual supplied evidence index**. | Unknown-but-well-formed UUID, malformed UUID, invented citation, duplicate/out-of-order claims, incomplete coverage and unsupported lineage all rejected. |
| **LLM-04** | Keep the **four limits independent**: completion tokens, provider raw UTF-8 bytes, canonical ASCII bytes, HTTP envelope bytes. | Separate off-by-one/Unicode/default-expansion tests; reservation arithmetic and limit combinations tested. |
| **LLM-05** | Budget from **fully materialized canonical models**, not the shortest model output. | Real schema with defaults, maximum claims/evidence, qualifications, contradictions and lineage fits chosen canonical budget. |
| **LLM-06** | Keep domain error categories precise; preserve original cause across wrappers and `finally` accounting. | Recorded cause plus terminal mapping distinguishes provider cap, schema, evidence, canonical size and genuine governance denial. |
| **LLM-07** | Capture **sanitized usage, finish reason and bytes** before discarding provider envelope. | Output-limit regression proves observed metadata is retained and missing metadata stays *unknown*, not fabricated. |
| **LLM-08** | Settle actual billable usage even when downstream validation fails. | One-call malformed-provider fixture ends FAILED with correct settled cost and no retry or next step. |
| **LLM-09** | Never automatically edit evidence IDs, drop forbidden fields or retry paid inference merely to pass validation without a separately justified, audited policy. | Counterexamples fail closed; no silent normalization, repair or fallback. |
| **LLM-10** | Test the **actual generation contract** with intercepted/offline exact-schema fixtures before expensive live tests. | Golden valid result; malformed UUID; top-level/nested extras; default expansion; full evidence coverage; planned stage composition. |
| **LLM-11** | Use **distinct development governance scopes** and reusable bounded evaluation policy; bind approvals to current configuration. | Historical costs retained, no new quota pool, current policy/provider/signer digests checked, old approvals invalidated when contract changes. |
| **LLM-12** | CLI exit codes must reflect terminal job success/failure, not only uncaught exceptions. | `FAILED` ⇒ nonzero exit after durable audit; `SUCCEEDED` ⇒ zero; both preserve financial settlement. |
| **LLM-13** | Make paid experiments **single-use, diagnostically complete and cheap**. | Preflight, explicit maximum cost, one-use signed approval when required, no implicit retries, immutable audit, stop at first error. |
| **LLM-14** | Do not generalize small-fixture acceptance to 200-page L2 or production. | Escalate from local 4-page smoke to representative documents and L2 only after completing true end-to-end L1 quality gates. |

### Suggested pre-live gate (apply to Estudio PolyMind and new projects)

- [ ] Run a **four-call end-to-end offline** test with the actual schema and deterministic fake provider, including normal reduction and grounded Q&A.
- [ ] Replay at least one **realistically shaped** accepted stage result through the exact decode → Pydantic → evidence validation → canonical encode → persistence path.
- [ ] Confirm separate raw-content, canonical-content, completion-token and transport bounds at 0/boundary/over-boundary and with Unicode/explicit defaults.
- [ ] Verify malformed UUIDs, extraneous fields, wrong evidence membership, incomplete coverage and fabricated lineage **all reject cleanly**, with no silent repair.
- [ ] Establish whether schema-constrained provider responses are **actually supported for the selected deployed model**; record the capability decision.
- [ ] Verify provider exception propagation, sanitized cause diagnostics, settled financial accounting and terminal **nonzero exit** on failed jobs.
- [ ] Check current development governance, shared provider capacity, approval/configuration fingerprint, cost ceiling and no already-active runs; run once only with explicit approval.
- [ ] Keep sensitive source content, raw provider responses, access tokens, RSA materials and owner/tenant bindings outside Git. Preserve hashes and sanitized postmortems in the repository.

## 7. Current state, fixes and open questions

**Implemented/verified offline after earlier failures:** managed prompt contract `managed-prompt/3`; independent 10,000-byte provider/canonical limits; 3,000 completion-token ceiling retained; sanitized output-limit diagnostics; correct propagation of settled provider errors; reusable evaluation governance overlay `polymind-evaluation/1` activated for verified development scope; nine-error Attempt 3 diagnosis reproduced; strict fail-closed Pydantic/evidence enforcement preserved.

**Still unresolved or not implemented:** the exact Attempt 2 output-limit trigger is historically **unknown**; the existing L1 model generation uses `json_object`, not verified schema-constrained generation; no valid fix for Attempt 3's already-generated schema-invalid content; terminal FAILED can still return CLI exit code 0; live complete L1 semantic/publication/Q&A quality remains **unproven**. L2 should not inherit assumed L1 success.

**Safest immediate engineering sequence:** (1) focused offline assessment of schema-constrained generation support and minimal adapter changes if feasible; (2) preserve strict Pydantic/evidence validation and prove schema-compliance regression cases without paid calls; (3) separately correct terminal CLI exit semantics; (4) review any changed generation-contract hash and approve a **new** packet before another live attempt; (5) require successful four-call live L1 before expanding to L2.

## 8. Evidence index and reproducibility

Primary project reports (repository-relative destinations, if present in the same checkout):

- `docs/codex/reports/phase_17hl_first_failure_diagnosis.md` — first-attempt canonical expansion and misleading category.
- `docs/codex/reports/phase_17hl_output_limit_hardening.md` — second-attempt diagnostic uncertainty, `RunGuard.finish` masking, remediation and limits.
- `docs/codex/reports/phase_17hl_independent_json_byte_limits.md` — independent 10,000-byte controls, prompt/contract update and offline tests.
- `docs/codex/reports/phase_17hl_reusable_evaluation_governance.md` — separate evaluation scope implementation.
- `docs/codex/reports/phase_17hl_evaluation_policy_activation.md` — authorized activation, unchanged historical accounting.
- `docs/codex/reports/phase_17hl_l1_attempt3_preparation.md` — fresh packet, fixture/cost/provenance.
- `docs/codex/reports/phase_17hl_l1_attempt3_serialization_root_cause.md` — exact Pydantic failure, offline replay, seven tests and exit-code finding.

Private attempt evidence (retain locally and **do not commit**):

- L1-1: `<PRIVATE_AUDIT_DIRECTORY_ATTEMPT_1>/`
- L1-2: `<PRIVATE_AUDIT_DIRECTORY_ATTEMPT_2>/`
- L1-3: `<PRIVATE_AUDIT_DIRECTORY_ATTEMPT_3>/`

**Confidence:** L1-1 and L1-3 causal mechanisms were exactly reproduced offline. L1-2's output-limit failure and masking are confirmed, but its internal limit trigger remains **indeterminate** because historical diagnostic metadata is absent.

---

## 9. Portable project memory — paste into a future project kickoff

> In Estudio PolyMind Phase 17H-L, three Oct 2026 Azure GPT-5.4 mini L1 live attempts each ended FAILED after one billable inference. Attempt 1: provider success but Pydantic default expansion made 2,597 raw UTF-8 bytes become 3,471 canonical ASCII JSON bytes, exceeding a 3,000-byte cap; surfaced misleadingly as `extraction_limit_exceeded`. Attempt 2: provider `output_limit` at 1,922 output tokens, with the precise byte-overflow-vs-token-truncation cause unrecoverable because no response-byte/finish-reason metadata was retained; downstream `RunGuard.finish()` masked the original error as `governance_denied`. Attempt 3: provider success but strict Pydantic validation rejected a malformed evidence UUID and eight forbidden `unused1`–`unused8` fields; terminal `serialization_error` occurred before canonical serialization. The model was asked for `json_object`, not schema-enforced generation. Total usage: 10,108 tokens, three settled calls, €0.020906810982050014. Reusable lessons: distinguish raw bytes/canonical bytes/HTTP bytes/completion tokens; budget fully materialized canonical models; prefer verified provider schema constraints *plus* strict application/evidence validation; reject invented/malformed IDs and unknown fields without silent repair; preserve sanitized provider diagnostics and original exception through settlement; keep budgeted single-use runs and immutable audits; make FAILED return nonzero CLI exit; prove complete offline contract before paid L1/L2. Do not assume schema-constrained generation is yet implemented, nor claim Attempt 2’s precise trigger is known.
