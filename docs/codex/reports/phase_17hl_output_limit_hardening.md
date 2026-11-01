# Phase 17H-L — Output-limit diagnostics and validation hardening

Status: **PASS — L1 OUTPUT DIAGNOSTICS HARDENED; LIMIT ASSESSMENT COMPLETE**

Date: 15 October 2026. Work performed on the existing `master` working tree, preserving prior tracked and untracked work. No Attempt 3 preparation or execution occurred.

## A. Implemented correction

`llm/inference.py` adds the frozen, provider-neutral `OutputLimitDiagnostics` record and an optional `diagnostics` argument on `InferenceOutputLimitError`. Existing exception categories and message-based construction remain compatible. The exact fields are `failure_cause`, `response_bytes`, `response_byte_limit`, `finish_reason`, `completion_tokens`, `completion_token_limit`, `reasoning_tokens`, and `usage_available`.

`llm/bounded_http.py:result_text` measures actual content UTF-8 bytes before raising. Its causes are `response_bytes_exceeded`, `provider_completion_truncated`, or `unknown` when the content envelope was unavailable. If both content overflow and truncation occur, byte overflow takes precedence in `failure_cause` and `finish_reason` retains `length` or `max_tokens`, recording both conditions without another field. Finish reasons are restricted to `stop`, `length`, `max_tokens`, `other`, or null. Missing metadata remains null, including missing reasoning counts; reported zero remains zero. Valid usage availability requires nonnegative integer input/output counts and a consistent total when supplied.

`llm/openai_compatible.py:execute` supplies reported usage and numeric reasoning-token counts before the envelope is discarded. Malformed usage, inconsistent totals, boolean counts, malformed reasoning details, and reasoning counts exceeding completion usage fail closed as protocol failures with unknown accounting usage. Missing/partial usage remains unknown rather than fabricated. Interactive generate/stream parsing is unchanged. `llm/ollama_client.py:execute` supplies its existing usage to the same neutral diagnostic boundary. Both adapters attach configured limits even when the HTTP envelope ceiling prevents content-level diagnosis; that case stays `unknown`, with no invented content length or finish reason. Existing HTTP, content-byte, and completion-token bounds remain enforced. No retries or fallback calls were added.

`tests/performance/foundry_preflight.py:recorded_execute` adds optional `output_limit_diagnostics` to failed provider-call audit records. The record is written in the existing finally path and carried into the run summary. This is an additive audit contract: old records need no migration, and missing historical fields remain unknown. No failed raw output, prompt, headers, authentication values, arbitrary provider strings, or reasoning content is added. Existing successful-response audit behavior is unchanged.

`tests/performance/foundry_budget.py:RunGuard.finish` still records a known failed call as finished/failed and durably stops the run with reason `provider`. It now raises `GovernanceError` only for unresolved/out-of-bound usage, not solely because a financially accounted provider call failed. Inspection of `governance/execution.py:GovernedExecution.execute` confirmed its existing re-raise/finally behavior correctly propagates the original provider exception once this erroneous finish-time exception is removed; changing that module was unnecessary. The next acquisition remains denied, including after reopening the guard. Reservations are not refunded and replay protections are unchanged.

Genuine ledger settlement and downstream admission-finish failures still propagate. Unknown usage remains unresolved and blocks continuation. When provider and accounting failures coexist, the persisted provider record retains `output_limit` and diagnostics, while the terminal category and governance/run records retain the accounting failure and unresolved state. Existing Python exception context also retains the provider error. Tests cover ledger `STARTED`, ledger `UNKNOWN`, and downstream finish failure after ledger `SETTLED`; no accounting exception is suppressed.

### Compatibility impact

The prompt remains `managed-prompt/2`, and no runtime profile or numeric limit changed. Nevertheless, `generation_contract_digest()` hashes the entire `foundry_preflight.py` source. Adding the audit field changes that digest:

- Before this task: `3da39a6b00a75a7f689a49e56a4dc3255576e0d16265a2d509f259f2d533e16f`
- After this task: `8e096a3658ee49379c09c60d8e21b46a2d5704756d318889d63e4ae1b4f03304`

Previously bound configuration/approval packets therefore do not validate against this code. No packet was regenerated or signed, no approval was consumed, and the digest check was not bypassed. Any future execution requires separate operator review and appropriately bound authorization.

## B. Offline JSON-size assessment

Deterministic synthetic fixtures use the actual `StageResult`, `Claim`, `Qualification`, `ClaimLink`, `generation_schema()`, `codec.decode`, `codec.encode`, and canonical serializer. IDs are synthetic UUIDs. Each ordinary claim has one evidence reference. Qualified claims add a 37-character qualification and one evidence reference; lineage cases add one child link per claim. The measured short claim text is `Synthetic observation.`; the minimal claim text is `x`.

| Synthetic response | Raw compact JSON with defaults omitted | Raw explicit compact ASCII JSON | Canonical bytes | Default expansion overhead |
|---|---:|---:|---:|---:|
| Minimal one-claim response | 272 | 484 | 484 | 212 |
| Eight short claims with evidence | 1,784 | 2,836 | 2,836 | 1,052 |
| Eight claims with evidence and qualifications | 2,776 | 3,668 | 3,668 | 892 |
| Eight claims with evidence, qualifications and lineage | 3,689 | 4,477 | 4,477 | 788 |

For these fixtures, top-level default fields contribute 92 bytes. Each ordinary evidence-bearing claim contributes another 120 bytes of otherwise omitted defaults: empty contradiction, qualification and lineage arrays, null subject, and default stance/status. When qualification/lineage fields contain data, they are no longer part of omitted-default overhead. These are measured fixture-specific overheads, not a universal constant for every response. The schema defaults remain valid to Pydantic when omitted, but the current generation template explicitly requires them; omitted-default fixtures deliberately test legacy expansion behavior rather than compliance with that instruction.

The raw 2,776-byte qualified fixture parses successfully under a 3,000-byte input bound and expands to 3,668 canonical bytes. Explicit compact ASCII serialization eliminates that expansion discrepancy but cannot reduce the canonical size itself. A non-ASCII/escaping fixture measures 509 raw UTF-8 bytes versus 521 canonical ASCII bytes: `é` contributes four extra bytes and the emoji eight when escaped. Quotes, backslashes, and newlines are also tested against actual JSON encoding. Whitespace can further increase raw provider content size; UTF-8 character count is not byte count.

Eight-claim fixtures also pass the actual evidence and lineage validator with synthetic source evidence and child links under an existing offline 6,000-byte test profile. This proves structural/evidence compatibility of the fixtures, not semantic quality, model capability, or coverage of a real document. No Azure response text was reconstructed.

| Configuration | Canonical validity | Byte compliance | Token reservation impact |
|---|---|---|---|
| Existing 3,000-byte limit | All four fixtures are schema-valid; size validation rejects the two richer fixtures | 484 and 2,836 fit; 3,668 and 4,477 fail | Existing 3,000-token reservation unchanged |
| Hypothetical 4,000-byte limit | All schema-valid; qualified fixture passes size validation | First three fit; 4,477 fails | Current profile rejects a 4,000-byte limit with a 3,000-token reservation; requires a separate contract correction or reservation change |
| Hypothetical 6,000-byte limit | All schema-valid and within size limit | All four fit | Same profile coupling; no inherent token/cost requirement follows from bytes alone |

The prompt is satisfiable for minimal and concise eight-claim outputs. It cannot guarantee preservation of arbitrary required evidence, qualifications and child links within 3,000 bytes. Even these short, legitimate richer examples exceed the ceiling, so 3,000 bytes is restrictive for the intended structured output. Six thousand bytes accommodates these examples, but is not proof that every legitimate response fits.

`GenerationRequest` already has separate response-byte and completion-token fields. Financial reservation uses estimated input and requested completion tokens, not the response-byte ceiling. Increasing only that provider byte ceiling would not itself increase reserved tokens or prices, although the larger HTTP envelope allowance consumes more local memory and actual usage still determines actual cost. It would also not cure a canonical overflow downstream.

Managed synthesis currently derives the provider response limit and canonical limit from the same `max_result_characters` field (despite the name, enforcement is byte-based). `DigestionProfile.budget` additionally requires `reserved_output_tokens >= max_result_characters`. Thus independent configuration is not currently available through the managed contract, and simply changing canonical bytes to 4,000/6,000 while keeping 3,000 reserved tokens is rejected. Tests verify this. A future separation of these constraints can retain the 3,000-token ceiling and financial reservation, but must explicitly revise the planning invariant and review input estimation/fingerprints. Changing the prompt's numerical budget can also change serialized input-estimate size, even without changing the output-token reservation.

Compact ASCII JSON with explicit fields is already compatible with the prompt and minimizes this raw/canonical discrepancy. Omitting defaults saves raw bytes but does not save canonical bytes under the current serializer and violates the generation instruction. Shortening field names or changing canonical serialization would alter stored schema/hash contracts and is a broader change than separating byte budgets. No such changes were made.

## C. Regression verification

Final affected offline selection: **227 passed, 1 deselected, 0 failed** (5.93 seconds). The deselected case is the existing L2 workflow; no L2 execution occurred. No full-suite run occurred.

Executed with the existing project Python environment:

```text
PYTHONPATH=/tmp/output-limit-tests:. python -m pytest -p offline_guard \
  tests/unit/test_output_limit_diagnostics.py \
  tests/unit/test_structured_provider.py \
  tests/unit/test_foundry_preflight.py \
  tests/unit/test_governance.py \
  tests/unit/documents/test_output_limit_sizes.py \
  tests/unit/documents/test_managed_inference.py \
  tests/integration/test_output_limit_hardening.py \
  tests/integration/test_foundry_offline_workflow.py -k 'not L2' -q
```

A temporary autouse test plugin blocked socket connect/connect_ex/sendto, create_connection, and DNS resolution. Fake HTTP remained in-process. The plugin also isolated the legacy ungoverned `test_managed_inference` module by monkeypatching its application setting to governance-disabled for those tests only; governed integration tests retained their real guard/ledger composition. No `.env` file was edited. Initial runs exposed two incorrect new fixture assertions (corrected to actual measured boundaries), then workspace governance-setting contamination in the legacy unit tests. A process-wide governance override was rejected by OIDC configuration validation; scoped test isolation resolved it. These were test setup/assertion corrections, not weakened runtime enforcement.

Coverage includes normal/missing finish reasons, bytes overflow, both truncation reasons, simultaneous overflow/truncation, malformed envelopes and usage, missing and zero reasoning counts, unknown HTTP-envelope overflow, UTF-8 counting, persisted content-free diagnostics, one-call terminal failures, genuine governance denial, unknown usage, downstream and ledger settlement failures, successful L1 synthetic composition, default expansion, eight-claim evidence/lineage, and unchanged prompt rendering checks.

Relevant Python compilation passed with `PYTHONPYCACHEPREFIX` outside the repository. `git diff --check` passed. No Docker/configuration/dependency changes required a build. No configured Python lint tool was found. Task-specific diffs were reviewed against pre-edit copies so prior changes in shared files were distinguishable. Separate pre-commit review found no newly added credentials, raw private responses, debug statements, dependencies, dead-code paths, generated runtime artifacts, or unrelated edits. Temporary logs/cache/baselines are under `/tmp`. No unresolved regression remains in the executed selection.

## D. Safety verification

- Historical audit directories for both attempts: unchanged; neither directory was opened or written during this task. This is an operation-scope statement, not a newly computed historical checksum comparison.
- Existing governance/financial records, replay markers and signed packets: unchanged. SQLite writes were exclusively synthetic test databases under pytest temporary directories.
- Azure inference calls: **0**. Other billable model calls: **0**.
- Azure resource changes: **0**. RSA signing: **0**. Authorization consumption: **0**.
- Git staging/commits/pushes: **0 / 0 / 0**. Branch remains `master`.
- Runtime model/deployment, `managed-prompt/2`, policy `phase17hl-l1/2`, byte/token limits, allowances, EUR 5 ceiling, RPM/TPM, embedding/Chroma architecture and four-request L1 composition remain unchanged.

Final `git status --short` confirms the original dirty working tree remains, with this task's new diagnostic/schema tests and report added. Final tracked `git diff --stat`: **14 files changed, 286 insertions, 18 deletions**; these totals include pre-existing edits and exclude untracked files, including the existing Foundry modules edited here. No staging, commit or push occurred.

## E. Recommendation for Attempt 3

The confirmed engineering defects corrected here are ambiguous output-limit diagnostics and finish-time masking of an already accounted provider failure. Attempt 2 remains indeterminate: no missing content-byte count or finish reason has been inferred. Its 1,922 reported completion tokens do not establish exhaustion of the configured 3,000-token ceiling. Historical recorded charges remain unchanged.

The smallest next engineering change is to separate managed provider-content bytes and canonical-result bytes from completion-token reservation, with targeted planning/serialization tests. The measured 4,477-byte qualified lineage response technically justifies evaluating a larger canonical allowance; 6,000 bytes accommodates the measured cases whereas 4,000 does not. This is an offline recommendation only, not an authorized production setting. Prefer that explicit budget separation over a canonical schema/serializer redesign, retaining the current completion-token ceiling unless independent token evidence justifies changing it.

A future L1 evaluation becomes technically reasonable after review of this correction, the byte-budget decision and its contract implications, and separately refreshed operator authorization for the changed fingerprint. Proceeding immediately with unchanged restrictive byte limits is not recommended. This task neither prepared nor authorized Attempt 3, and does not predict its success.
