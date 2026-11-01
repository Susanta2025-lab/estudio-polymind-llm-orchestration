# Phase 17H–L: live-failure observability and contract options

Date: 2026-10-22. Branch: `master`.
HEAD: `af4a7a076c918ef13aea05d74bf239c0af909133`.
Scope: deterministic offline engineering and verification only.

## Executive result

| Work package | Result |
| --- | --- |
| WP-A diagnostic implementation | **PASS** |
| WP-B comparison preservation | **PASS**, semantic requests frozen; source hashes changed as explained |
| WP-C prompt candidate | **READY FOR REVIEW**, inactive |
| WP-D identifier alternative | **ASSESSED**, no migration |
| Overall offline task | **PASS** |

The final guarded regression is **1631 passed**, including all 1519 baseline
cases and 112 additions, with zero failures, errors, skips or network attempts. Live readiness remains
**CONDITIONAL**; Phase 17H remains **PARTIAL**. This task provides no spending
or inference authorization and does not demonstrate real-model acceptance.

## Assessment and baseline

AGENTS.md, the specified provider, document, planning/workflow, executor and
verification files were inspected in the current dirty working tree. The five
required audit/isolation/E2E/diagnostic/reconciliation reports and relevant safe
historical preparation/failure/byte-limit reports informed the assessment. No
operator packet, response archive, key, credential or real document was opened.

The starting inventory contains **20 modified tracked files and 94 untracked
files**, with an empty index. The original tracked stat is **20 files changed,
607 insertions, 71 deletions**. The complete starting inventory is preserved in
this report's appendix. Public Python/document snapshots and task-only pre-edit
copies were retained under `/tmp/polymind-observability`, alongside temporary
synthetic artifacts and verification logs. Historical artifacts were not rewritten.

The local strict configuration is `managed-generation/2`, `managed-prompt/3`,
`azure-strict/1`, strict `json_schema`, reasoning `low`, 3000 completion tokens,
10000 raw UTF-8 bytes, 10000 canonical ASCII JSON bytes and 26192 envelope bytes.
All four StageProfiles reserve 3000 output tokens. The live preparation binding is
`epolymind-gpt-54-mini`, model/version `gpt-5.4-mini` / `2026-03-17`, GlobalStandard,
with `/openai/v1/chat/completions`; these are local configuration observations,
not newly verified Azure resource properties. No model-name capability inference
or external documentation/cloud lookup was performed.

## Diagnostic implementation

### Existing contract and closed supplemental taxonomy

`ValidationDiagnostic` is unchanged: json_decode, duplicate_json_key,
pydantic_validation, canonical_serialization, stage_binding, claim_identity,
claim_contract, evidence_validation, coverage_validation, response_limit.
`DigestionError` gains optional typed `validation_reason` and a frozen
`PydanticDiagnostic`. The category and ordinary exception string remain unchanged.
The exact domain-to-public mappings remain:

| Domain category | Public category |
| --- | --- |
| inference_contract_error | serialization_error |
| evidence_validation_failed | invalid_reference |
| coverage_failed | extraction_failed |
| synthesis_limit_exceeded | extraction_limit_exceeded |

`documents/digestion/diagnostics.py` owns the closed ValidationReason enum.
No provider/model string can become a reason. The implemented attributions are:

| Diagnostic stage | Reasons emitted when established |
| --- | --- |
| JSON | malformed_json; duplicate_json_key |
| Pydantic | invalid_uuid; invalid_subject_token; invalid_text_bound; missing_required_field; invalid_field_type; forbidden_extra_field; invalid_enum; other_pydantic_validation |
| Canonical | canonical_encoding_failed; canonical_revalidation_failed |
| Stage | stage_id_mismatch; stage_kind_mismatch; unavailable_with_claims; unavailable_missing_limitation; analyzed_without_claims; unavailable_reduction |
| Identity | claim_id_mismatch; duplicate_claim_id; originating_stage_mismatch |
| Claim | subject_on_nonfact |
| Evidence | foreign_evidence; duplicate_evidence; invalid_qualification_source; invalid_child_link; duplicate_child_link; unsupported_fact; other_evidence_validation |
| Coverage | missing_source_coverage; missing_child_coverage |
| Limits | raw_response_limit; canonical_response_limit; claim_limit; annotation_limit; text_limit |

Generic canonical/coverage fallback enum values are reserved, not represented as
newly observed production failures. Existing unrelated make_digest/planning errors
are not broadly rewritten or attributed beyond the inspected stage boundary.

### Safe Pydantic attribution

The classifier requests `errors(include_input=False, include_context=False,
include_url=False)` and immediately reduces each error to an allowlisted type
classification and structural path. Raw dictionaries, values, messages, contexts
and URLs are not attached to the domain exception or audit. Paths consist only of
StageResult field names and bounded integer indices: claims/annotations/lineage/
qualifications below 64; evidence positions below 4096. Booleans, negative or
oversized positions, dynamic names, union labels and unknown structures are
omitted. Unknown paths receive the generic Pydantic reason. Forbidden-extra errors
have a known extra-field predicate but always omit their potentially dynamic path.

The primary error is selected by enum declaration priority (UUID, subject, text,
missing, type, extra, enum, generic among Pydantic reasons), then lexical `repr`
of the sanitized tuple path. Selection is independent of errors iteration order.
The failure count saturates at 64: 64 means at least 64, not an exact upper count.
The primary reason is not a claim that no other defect exists. A classifier failure
falls back to generic metadata while preserving the original normalized rejection.
Audit serialization rechecks type, path and numeric bounds, including forged data.

### Deterministic validators and canonical order

The same predicates, loops, state updates, return value and ordering remain in
`validate_result()`. Only DigestionError keyword metadata differs. A regression
normalizes away those keywords and compares the entire function AST with its
pre-edit digest. Separate source checks freeze domain class ASTs and the complete
managed renderer file. Immutable checkpoints, authorization and workflow code are
unchanged by this task.

Within an already rejected combined identity branch, duplicate ID takes diagnostic
priority over wrong positional ID, then wrong originating stage. A repeated ID
necessarily also violates the expected ID at its later position; duplicate would
otherwise be unobservable as a specific reason. This does not move the identity
branch relative to any other validator. Other combined branches retain their
existing predicate priority. Qualification text overflow is identified as text_limit
when its evidence is nonempty; it retains the existing evidence diagnostic/category
and public invalid_reference outcome. No rejection policy changes.

`decode()` separates malformed JSON, duplicate keys and model rejection.
`encode()` distinguishes dump/JSON/ASCII encoding from model revalidation. Raw and
canonical byte overflows remain independent. **validate_result performs canonical
encoding before stage and claim checks**, not only after checkpoint persistence.
A canonical diagnostic therefore does not establish that any checkpoint was saved.

### Provider metadata and output-limit correction

A frozen optional ProviderResultMetadata is appended to GenerationResult; existing
positional construction remains compatible. It retains only sanitized finish reason,
prompt/completion/total/reasoning token counts, raw content-byte count and configured
completion-token/response-byte limits. Numeric audit values are nonnegative exact
integers bounded to signed 64-bit; booleans, negative/oversized values and strings
are omitted as unknown. Known zero remains zero. Finish reasons are stop, length,
max_tokens, other or null; free-form provider values never enter the audit.
Raw bytes count means message content UTF-8 bytes, not HTTP envelope bytes.
Invalid Unicode measurement becomes unknown rather than masking a primary refusal.

The adapter already validated reasoning-token details but previously discarded
successful reasoning counts before the final single-call audit. The new record
survives both adapter success and exceptions. The single-call ObservedProvider
copies sanitized metadata before governance cleanup or application validation.
Thus known successful provider usage remains available even when StageResult
validation rejects the result or a cleanup fails. ManagedSynthesisInference still
returns its existing text interface; durable workflow acceptance is unchanged.
This task adds no new logging of bodies, prompts, headers, model-generated prose,
provider free-form metadata or reasoning content.

Offline reproduction confirmed that length plus null content previously failed in
_completion_content before result_text could classify truncation. The adapter now
passes null/absent content to the bounded classifier only for truncation; the classifier
always raises output_limit and records content byte count as unknown. Missing content keys also remain unknown. Empty and
partial text retain measured sizes and also raise output_limit. Refusal, malformed
strict choices, missing/malformed finish metadata and unexpected models remain
protocol failures. Null stop content is still invalid; empty stop content retains
its prior adapter behavior and is subject to downstream strict decoding. No
incomplete content is accepted, repaired, retried or persisted as a checkpoint.

Usage validation, unknown-usage accounting, financial settlement and cleanup order
are unchanged. Reasoning counts remain included in completion usage; the metadata
is observational and never adds a second charge. GovernedExecution settles before application validation. Unknown or
invalid usage still leaves unresolved/UNKNOWN accounting and stops the run; no
missing count is fabricated as zero. With output_limit plus settlement failure,
output_limit remains primary and accounting_failed is true. Only temporary synthetic
authorities were used for these tests; no live reservation/settlement occurred.

### Optional schema observation and marker meaning

`tests/performance/foundry_schema_diagnostics.py:observe_schema()` is an explicitly
callable offline helper using the installed jsonschema dependency and the exact
production provider_schema(generation_schema()). It returns only an enum:
response_limit, invalid_json, schema_rejected or schema_conformant. It rejects
duplicate keys/non-JSON constants without retaining body/path/error messages.
It is not imported by live execution and adds no runtime dependency requirement.
Local schema validity is neither Azure certification nor StageResult acceptance:
for example, the converted schema deliberately cannot enforce UUID formatting.
`completed_strict_response` continues to mean adapter completion only. No new live
schema check or acceptance gate was introduced.

## Contract preservation and Attempt 4 comparison

Authoritative values were recomputed through executor_digest(),
generation_contract_digest() and the production schema fingerprint before any
production edit. They exactly match the preceding independent audit.

| Binding | Before | After |
| --- | --- | --- |
| Executor | `9cd6711b61f2896090d351468e42dcc9a7c00f77e8f6cfc41c6f273172897b5a` | `de11d7cbeb269591caa607494d29a76b894bd48af15d17ab2095ffb51b96e598` |
| Generation source digest | `82ecad5d4cb2e8fd2e0981c7d3710bbb3a582e56ef9eebca07ab0f314a4d05f9` | `4c37473513e2f1455cfa44a84c687b661a484e2fea0a390dedf9396269610d05` |
| Provider schema | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` |

**The active semantic generation contract and request payloads are unchanged.
The authoritative source-based generation digest changes.** Its policy hashes
entire files including models, validation, structured result metadata, bounded_http
and openai_compatible. Diagnostic-only edits therefore change it. That fingerprint
policy was not changed, bypassed or redefined. New offline helper code also falls
under the broader executor path set. Old configurations/approvals do not become
valid for this implementation, despite identical generation requests. None was
regenerated, finalized, signed, refreshed or consumed.

Complete synthetic StageRequest, GenerationRequest (all fields), provider payload
and schema representations for chunk, structural and root were captured before
edits and compared byte-for-byte as deterministic sorted JSON afterward, without
removing any field. **All nine component comparisons are identical.** Permanent
regressions bind those pre-edit checksums. The unchanged full managed.py source
and domain ASTs additionally freeze instructions, serialization, all four profile
versions, model/configuration bindings and acceptance structure. A separate
all-four-profile witness verifies intermediate rendering and valid reduction;
no claim is made that the three-stage production fixture naturally executes an
intermediate stage. Limits, strict mode, reasoning and model bindings stay fixed.

The safe historical strict-schema preparation report documents generation
`6f936342efb8e22faf23d59ebf71f7846d3255692d398c27d1e6a449ef41e247`
and schema `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2`.
That report explicitly describes preparation with zero Attempt 4 calls; it is
**not original evidence of the exact submitted live schema/executor**. The supplied
Attempt 4 summary and prior independent audit establish adapter completion plus
serialization_error but do not identify a rejected predicate. Exact historical
request equivalence cannot be independently established from accessible public
material. The next comparison is meaningful against the verified current
pre-edit semantic contract, with that historical limitation clearly retained.
No Attempt 3 UUID/extra defect is attributed to Attempt 4.

## Inactive instruction proposal and architecture assessment

[The clarification proposal](../proposals/phase_17hl_generation_instruction_clarifications.md)
contains exact original fragments, replacement wording, rationale and predicates.
M1 explains subjects, fact support and unique authorized references. M2 distinguishes
immutable child-lineage preservation from directly copying an unauthorized ancestor
qualification. M3 conditions coverage on analyzed analysis and describes valid
unavailable analysis. Positive/negative synthetic inheritance examples map to the
persisted graph/digest tests. The candidate is `managed-prompt/4`; the patch changes
both the StageProfile template and adapter prompt-profile binding, and stays a
reviewable documentation artifact. `git apply --check` passes; the proposal was also reconstructed in memory and
compiled without execution, with both version bindings and M1/M2/M3 fragments
verified. It was not applied.

Four-profile analyzed witnesses and analysis-only unavailable witnesses establish
consistency with current validators; the existing compatibility suite additionally
exercises persisted qualification/contradiction retention. These tests do not import
or activate the proposed patch, or measure GPT-5.4-mini compliance. Activation needs
separate authorization or completion/review of the next diagnostic experiment,
new fingerprints and appropriately reviewed plan/checkpoint/approval bindings.

[The proposed ADR](../../adr/phase_17hl_application_owned_identifiers_assessment.md)
compares complete StageResult against a constrained semantic proposal resolved
through application-owned trusted mapping tables. It addresses security, selection
errors, deterministic ordering, token/byte overhead, coverage, qualifications,
contradictions, durable replay, migration, rollback and request-specific UUID enums.
Indices remove some metadata-copying burden but relocate errors and do not prove
semantic source correctness. UUID enums preserve storage shape but still alter
request/schema/fingerprints and cannot simply enforce pair relationships/coverage.
Retain option A for the diagnostic comparison. Consider a separately authorized
prototype only after identity/reference-specific live evidence or a substantial
independent offline advantage. No production alternative or repair path exists.

## Validation record

Python 3.10.13; pytest 8.4.2, Pydantic 2.13.4, pydantic-settings 2.14.1 and
jsonschema 4.26.0 were already installed. No package was installed or upgraded.

| Completed check | Result |
| --- | --- |
| Historical configured baseline | 1519 passed, as documented by the prior independent audit |
| Initial focused diagnostic/provider/harness selection | 126 passed, 23.91 s; zero network attempts |
| Broad focused document/provider/schema/security/governance/E2E selection | 973 passed, 35 baseline warnings, 106.82 s; zero network attempts |
| First full regression before the final four review cases | 1627 passed, 42 baseline warnings, 401.12 s; zero network attempts |
| Final new diagnostic/contract/proposal-witness module | 112 passed, 6.08 s; zero failures/errors/skips/network attempts |
| Final full configured regression | **1631 passed**, 42 baseline warnings, **414.27 s**; zero failures/errors/skips/network attempts |
| Ruff check and format, three new Python files | PASS, zero findings; all three formatted |
| Ruff check, all ten changed Python files | 24 existing findings versus 26 before; zero newly introduced findings |
| Ruff format check, all ten changed Python files | Seven pre-existing files require formatting both before and after; three new files pass |
| Repository compileall with external cache | PASS, exit 0 |
| Tracked diff and explicit new-file whitespace checks | PASS, no whitespace errors |
| Inactive candidate patch check and in-memory compilation | PASS; no application/execution |
| Public source/document preservation | 255/262 pre-existing files unchanged, seven intended edits |

The final JUnit inventory verifies **1519 existing + 112 new = 1631 passing**
cases. Every one of the earlier 1627 passing cases remains present and passed;
the final four review cases are additional. The full count should
include every historical baseline case and all 112 additions; overlapping focused
runs are not counted as extra unique tests. No skip or xfail was introduced.
The baseline warning class is record_property versus JUnit xunit2, not a new
production warning. An intermediate final rerun was deliberately interrupted to
add omitted-content-key truncation cases, then restarted from collection; that
interrupted run is not represented as passing validation. Development fixtures
also needed Pydantic context and an absent-content expected-byte correction, both
fixed without weakening assertions.

Existing Ruff findings comprise BLE001 (7), I001 (2), SIM114 (1), UP035 (1), F401
(2), UP045 (5), C408 (5) and S110 (1). They remain in codec.py, bounded_http.py,
openai_compatible.py and the pre-existing single-call harness. Before/after checks
use exact pre-edit copies verified against the starting manifest. Import ordering
was corrected where adding imports; unrelated lint/whole-file formatting debt was
left scoped. The all-changed-file commands therefore exit 1 for existing debt;
this report does not label them globally green.

Verification preserves the existing tests/conftest.py and settings_isolation.py.
The inspected existing `/tmp/polymind_e2e_offline_guard.py` is loaded as a startup
plugin before collection. It denies socket connection/DNS operations, adds an audit
hook and forces session failure for even swallowed attempts. A separate deliberate
DNS probe was blocked before resolution, counted one attempt and produced session
exit 1 despite its caught test passing. The actual regression/snapshot runs count
zero attempts. This is Python socket/DNS denial, not an assertion of an OS firewall
for arbitrary subprocess binaries. Existing subprocess tests have their own guards.
No external inference or Azure CLI operation was executed.

Commands for reproducibility:

```sh
PYTHONPATH=/tmp:. PYTEST_PLUGINS=polymind_e2e_offline_guard \
 PYTEST_ADDOPTS=--junitxml=/tmp/polymind-observability/full-final.xml \
 python -m pytest -q
PYTHONPATH=/tmp:. python -m pytest -p polymind_e2e_offline_guard \
 tests/integration/test_live_failure_observability.py -q
ruff check <the ten changed Python files>
ruff format --check <the ten changed Python files>
PYTHONPYCACHEPREFIX=/tmp/polymind-observability/pycache python -m compileall -q .
git apply --check docs/codex/proposals/managed_prompt_4.patch
git diff --check
git status --short --branch
git diff --stat
git diff --cached --name-only
```

The changed-file Ruff commands cover the seven edited Python files and three new
Python files listed below. The two startup tools remain unchanged. No dependencies,
Docker files or deployment configuration changed, so Docker builds/cluster operations
were not applicable and were not performed. Compilation uses an external cache.

## Independent self-review and pre-commit review

A separate review of task-only before/after diffs, all new untracked files and the
complete relevant working-tree diff checked frozen prompt/schema/payload/profile,
acceptance predicates and validation order, public categories/retry behavior,
usage/accounting/cleanup paths, privacy, deterministic selection, unknown errors,
network/test isolation, inactive proposal and absence of production ID migration.
Known findings corrected during review were qualification text attribution and
Unicode diagnostic measurement masking a refusal. Test development also corrected
a synthetic Pydantic fixture context and an initially mistyped focused-test path;
that failed selection collected no tests and is not counted as validation evidence.

No newly introduced credentials, .env reads, private keys, real provider bodies,
operator paths, generated runtime artifacts, debug statements, dependency changes,
security-policy migrations or unrelated code edits were found. Static synthetic
UUIDs and the known public deployment binding are test/configuration material.
The report's new links resolve locally; the proposed patch is review-only.
No historical report or existing test-isolation infrastructure was modified.

## Files, Git and safety

New files:

- documents/digestion/diagnostics.py
- tests/performance/foundry_schema_diagnostics.py
- tests/integration/test_live_failure_observability.py
- docs/codex/prompts/phase_17hl_live_failure_observability_and_contract_options.md
- docs/codex/proposals/phase_17hl_generation_instruction_clarifications.md
- docs/codex/proposals/managed_prompt_4.patch
- docs/adr/phase_17hl_application_owned_identifiers_assessment.md
- this report

Pre-existing files edited by this task:

- documents/digestion/codec.py
- documents/digestion/models.py (exception metadata only)
- documents/digestion/validation.py (diagnostic attribution only)
- llm/structured.py (optional result metadata only)
- llm/openai_compatible.py (response observations/classification only)
- llm/bounded_http.py (null-content truncation classification only)
- tests/performance/foundry_single_call.py (sanitized audit extension)

The final inventory is exactly the starting inventory plus the eight new paths
listed above: **20 modified tracked files and 102 untracked files**, no removed
starting path and no staged file. HEAD remains unchanged. All **255** other public
files in the 262-file baseline manifest are byte-identical; only the seven
explicit diagnostic edits differ. All 114 starting status paths remain present.
The complete final status and tracked stat are also captured in
`/tmp/polymind-observability/final-status.txt` and `final-diff-stat.txt`.
The final tracked stat is **20 files changed, 812 insertions, 76 deletions**,
including pre-existing work and excluding every untracked file. These totals are
not presented as task-only code counts.

Paid inference calls, cloud operations, live financial reservations/settlements,
operator approval creation/signing, historical audit modifications, commits and
pushes: **0 each**. Existing RSA/financial tests exercise only synthetic fixtures
and disposable local authorities; those are not operator approvals or live funds.
No branch/index/history operation occurred.

## Unresolved risks and next experiment

Confirmed limitations are the unknown Attempt 4 predicate, lack of accessible
original submitted-request evidence, existing whole-file fingerprint coupling,
unchanged known prompt ambiguities pending review, and pre-existing lint/format
findings. A source-digest change is required by diagnostics and invalidates old
configuration bindings; it is not silently treated as exact approval equivalence.

Potential real-model failures from identity copying, semantic evidence choices,
coverage, token exhaustion, refusal or Azure subset interpretation remain hypotheses
unless observed. Local schema checks cannot certify service behavior. Offline green
tests do not establish an improved acceptance rate or resolve the remaining Phase
17H evaluation requirements. The prior authorization-action coupling observation
is outside this diagnostic scope; authority/security code is unchanged.

Recommend only a **separately authorized, governed single-analysis diagnostic
call**, after operator review of changed source hashes and fresh required authority
bindings. Preserve the verified semantic generation contract for that experiment,
retain the new sanitized metadata and stop terminally after one call. Do not
activate the prompt candidate or identifier design beforehand merely to improve
model compliance. This task does not prepare, authorize or execute that call.

## Appendix: starting inventory

```text
 M .env.example
 M docs/security/phase_17g.md
 M documents/digestion/codec.py
 M documents/digestion/managed.py
 M documents/digestion/models.py
 M documents/digestion/validation.py
 M documents/publication/analysis.py
 M governance/execution.py
 M governance/ledger.py
 M llm/bounded_http.py
 M llm/inference.py
 M llm/ollama_client.py
 M llm/openai_compatible.py
 M llm/structured.py
 M security/identity.py
 M security/runtime.py
 M tests/integration/test_managed_digestion.py
 M tests/unit/documents/test_managed_inference.py
 M tests/unit/publication/test_analysis.py
 M tests/unit/test_structured_provider.py
?? docs/codex/prompts/phase_17h_live_preflight.md
?? docs/codex/prompts/phase_17hl_diagnostic_hardening.md
?? docs/codex/prompts/phase_17hl_entra_v2.md
?? docs/codex/prompts/phase_17hl_final_handoff.md
?? docs/codex/prompts/phase_17hl_final_offline_azure_compatibility_audit.md
?? docs/codex/prompts/phase_17hl_first_failure_diagnosis.md
?? docs/codex/prompts/phase_17hl_full_suite_configuration_isolation.md
?? docs/codex/prompts/phase_17hl_l1_attempt3_serialization.md
?? docs/codex/prompts/phase_17hl_live_execution_preparation.md
?? docs/codex/prompts/phase_17hl_offline_e2e_contract_verification.md
?? docs/codex/prompts/phase_17hl_offline_readiness.md
?? docs/codex/prompts/phase_17hl_operator_approval.md
?? docs/codex/prompts/phase_17hl_preflight_observability_timing_hardening.md
?? docs/codex/prompts/phase_17hl_regression_reconciliation.md
?? docs/codex/prompts/phase_17hl_reusable_evaluation_governance.md
?? docs/codex/prompts/phase_17hl_same_day_attempt2.md
?? docs/codex/prompts/phase_17hl_second_attempt_preparation.md
?? docs/codex/prompts/phase_17hl_structured_output_compatibility.md
?? docs/codex/prompts/phase_17hl_two_layer_structured_output.md
?? docs/codex/reports/phase_17h_live_preflight.md
?? docs/codex/reports/phase_17hl_azure_strict_schema_live_compatibility.md
?? docs/codex/reports/phase_17hl_diagnostic_hardening.md
?? docs/codex/reports/phase_17hl_entra_v2_report.md
?? docs/codex/reports/phase_17hl_evaluation_activation_readiness.md
?? docs/codex/reports/phase_17hl_evaluation_policy_activation.md
?? docs/codex/reports/phase_17hl_final_offline_azure_compatibility_audit.md
?? docs/codex/reports/phase_17hl_final_operator_authorization.md
?? docs/codex/reports/phase_17hl_first_failure_diagnosis.md
?? docs/codex/reports/phase_17hl_full_suite_configuration_isolation.md
?? docs/codex/reports/phase_17hl_independent_json_byte_limits.md
?? docs/codex/reports/phase_17hl_l1_attempt3_preparation.md
?? docs/codex/reports/phase_17hl_l1_attempt3_serialization_root_cause.md
?? docs/codex/reports/phase_17hl_launch_authorization_final.md
?? docs/codex/reports/phase_17hl_live_execution_preparation.md
?? docs/codex/reports/phase_17hl_offline_e2e_contract_verification.md
?? docs/codex/reports/phase_17hl_operator_approval_report.md
?? docs/codex/reports/phase_17hl_output_limit_hardening.md
?? docs/codex/reports/phase_17hl_preflight_observability_timing_hardening.md
?? docs/codex/reports/phase_17hl_regression_reconciliation.md
?? docs/codex/reports/phase_17hl_reusable_evaluation_governance.md
?? docs/codex/reports/phase_17hl_same_day_attempt2_handoff.md
?? docs/codex/reports/phase_17hl_second_attempt_preparation.md
?? docs/codex/reports/phase_17hl_single_call_execution_failure_diagnosis.md
?? docs/codex/reports/phase_17hl_single_call_harness_offline.md
?? docs/codex/reports/phase_17hl_structured_output_compatibility.md
?? docs/codex/reports/phase_17hl_two_layer_structured_output.md
?? docs/engineering/llm_structured_output_validation.md
?? docs/engineering/postmortems/Estudio_PolyMind_Phase17HL_L1_Three_Attempts_Postmortem_2026-10-16.md
?? docs/evaluation/phase_17h_foundry_approval.template.json
?? docs/evaluation/phase_17h_foundry_validation.md
?? docs/evaluation/phase_17hl_operator_approval.md
?? docs/governance/evaluation-binding.template.json
?? docs/governance/evaluation-policy.md
?? docs/security/entra_v2.md
?? governance/evaluation.py
?? governance/migration.py
?? llm/azure_schema.py
?? tests/README.md
?? tests/approval_helpers.py
?? tests/conftest.py
?? tests/integration/test_attempt3_serialization.py
?? tests/integration/test_final_offline_azure_compatibility.py
?? tests/integration/test_foundry_l1_entra.py
?? tests/integration/test_foundry_l1_launcher.py
?? tests/integration/test_foundry_offline_workflow.py
?? tests/integration/test_output_limit_hardening.py
?? tests/integration/test_phase17hl_offline_e2e.py
?? tests/integration/test_single_call_harness.py
?? tests/integration/test_single_call_preflight.py
?? tests/integration/test_validation_diagnostics.py
?? tests/performance/foundry_approval.py
?? tests/performance/foundry_budget.py
?? tests/performance/foundry_envelopes.py
?? tests/performance/foundry_l1.py
?? tests/performance/foundry_preflight.py
?? tests/performance/foundry_recalibration.py
?? tests/performance/foundry_schema_probe.py
?? tests/performance/foundry_single_call.py
?? tests/settings_isolation.py
?? tests/unit/documents/test_independent_json_limits.py
?? tests/unit/documents/test_output_limit_sizes.py
?? tests/unit/documents/test_strict_schema_compatibility.py
?? tests/unit/documents/test_two_layer_output.py
?? tests/unit/test_evaluation_activation.py
?? tests/unit/test_evaluation_governance.py
?? tests/unit/test_foundry_30k.py
?? tests/unit/test_foundry_approval.py
?? tests/unit/test_foundry_preflight.py
?? tests/unit/test_foundry_schema_probe.py
?? tests/unit/test_governance_migration.py
?? tests/unit/test_output_limit_diagnostics.py
?? tests/unit/test_security_entra.py
?? tests/unit/test_settings_isolation.py
?? tests/unit/test_single_call_diagnostics.py
```
