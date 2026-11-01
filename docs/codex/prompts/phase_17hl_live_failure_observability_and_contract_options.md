# CODEX IMPLEMENTATION PROMPT — ESTUDIO POLYMIND PHASE 17H–L

## Targeted Live-Failure Observability, Attempt 4 Contract Preservation,
## Generation-Instruction Clarification and Application-Owned Identifier Assessment

Clean execution copy of the supplied phase prompt. Repeated requirements are
consolidated here; this is not a verbatim conversation transcript.

## Role, objective and execution strategy

Act as Senior AI Systems Architect, Python Engineer, Azure Foundry Integration
Specialist and Independent Reliability Auditor in
`Susanta2025-lab/estudio-polymind-llm-orchestration`, existing branch `master`.
Work is authorized for offline development and deterministic verification only.

- WP-A IMPLEMENT: improve validation/provider-result diagnostics without changing
  the active generation contract.
- WP-B VERIFY: preserve a meaningful technical comparison with Azure Attempt 4.
- WP-C DESIGN AND VERIFY OFFLINE: prepare precise inactive generation-instruction
  corrections, with a versioned reviewable proposed patch.
- WP-D ASSESS: evaluate application-owned deterministic identifiers; do not migrate
  production without evidence and separate authorization.

Critical sequence: freeze the generation contract for the next diagnostic
experiment. Diagnostics may change executor fingerprints. Do not modify active
render instructions, StageResult/Claim/Qualification/ClaimLink, generation_schema,
provider_schema, response_format, strict mode, model/deployment, reasoning effort,
stage budgets, generation controls or request serialization. If a conflict arises,
stop that subtask, explain it and continue independent safe work. Do not redefine
fingerprinting to manufacture equivalence.

## Verified project history to verify against current implementation

Historical Azure deployment: ECI-Development, Spain Central,
`epolymind-foundry-dev-susanta`, `epolymind-gpt-54-mini`, model `gpt-5.4-mini`,
version `2026-03-17`, GlobalStandard, `/openai/v1/chat/completions`.
Previously audited settings: strict `json_schema`, reasoning `low`, 3000 completion
tokens, independent 10000 raw UTF-8 and canonical ASCII JSON bytes, 26192 envelope
bytes. Verify locally; never infer capabilities from a model name.

Attempt 1 (15 October): completed response, canonical expansion exceeded the old
3000-byte result limit; independent limits were subsequently introduced.
Attempt 2 (15 October): output-limit failure masked by governance; precedence was
subsequently corrected, historical trigger remains unknown.
Attempt 3 (16 October): valid JSON with one invalid UUID and eight forbidden extra
fields, using json_object. Attempt 4 (19 October): first strict-schema experiment,
`completed_strict_response`, application FAILED, public `serialization_error`,
accounting_failed false, one provider call, no retry. Its rejected predicate was
not preserved. **Attempt 4 cause remains UNKNOWN; never attribute Attempt 3's
UUID/extra defects to Attempt 4.** Do not open private response archives.

Previous independent offline audit: PASS, live readiness CONDITIONAL; 1519 passing
full regressions, 116 new compatibility cases, zero critical/high findings, four
medium and one low finding, zero inference. Valid responses can satisfy both
schemas and semantic contracts, but provider-schema validity alone is insufficient.
Real-model acceptance remains unverified. Phase 17H remains PARTIAL.

## Required inspection

Read AGENTS.md first. Inspect current local implementation, consumers, tests and
configuration before edits. Required provider files: `llm/azure_schema.py`,
`structured.py`, `openai_compatible.py`, `bounded_http.py`, `inference.py`,
`admission.py`. Required document files: `documents/digestion/managed.py`,
`models.py`, `codec.py`, `validation.py`, `planning.py`, `workflow.py`,
`documents/jobs/models.py`, `documents/models.py`. Inspect actual executors
`tests/performance/foundry_preflight.py`, `foundry_single_call.py`, `foundry_l1.py`.

Read integration tests `test_final_offline_azure_compatibility.py`,
`test_phase17hl_offline_e2e.py`, `test_validation_diagnostics.py`, and existing
single-call/output-limit/governance tests. Read reports under docs/codex/reports:
`phase_17hl_final_offline_azure_compatibility_audit.md`,
`phase_17hl_full_suite_configuration_isolation.md`,
`phase_17hl_offline_e2e_contract_verification.md`,
`phase_17hl_diagnostic_hardening.md`, `phase_17hl_regression_reconciliation.md`.
Inspect safe historical reports only; do not invent absent evidence.

## Non-negotiable safety

Preserve every starting modified/untracked file and record starting/final
inventories. Stay on master; no staging, commit, push, new branch, reset, clean,
restore, stash, rebase, merge or historical report rewrites. Do not overwrite test
isolation. No unrelated implementation changes.

No Azure/other paid inference, Azure CLI cloud operations, provisioning, AKS
activation, secret retrieval, credential generation, RSA operator signing,
operator approval creation, live launcher execution or financial reservation/
settlement against live resources. Existing deterministic synthetic tests may
exercise isolated temporary authorities; no real provider availability is allowed.

Do not read dotenv secrets, keys/tokens, private approval/signing material, real
model bodies, sensitive document text or historical user evidence UUIDs. Never
write raw provider output into sanitized audit. Preserve authorization, strict
decoding/forbidden extras, deterministic IDs, evidence membership, coverage,
lineage, qualifications/contradictions, immutable checkpoints, canonical encoding,
response limits, fail-closed accounting, original public categories and error
precedence. No runtime repair or automatic retries.

## WP-A diagnostics

Preserve ValidationDiagnostic values: json_decode, duplicate_json_key,
pydantic_validation, canonical_serialization, stage_binding, claim_identity,
claim_contract, evidence_validation, coverage_validation, response_limit.
Preserve public mappings inference_contract_error→serialization_error,
evidence_validation_failed→invalid_reference, coverage_failed→extraction_failed,
synthesis_limit_exceeded→extraction_limit_exceeded.

Add immutable typed, bounded, allowlisted supplemental reasons at the narrowest
appropriate boundary. Reasons must identify established predicates only. Suggested
classes include malformed/duplicate JSON; invalid UUID/subject/text bounds,
missing field, invalid type/enum, forbidden extra and generic Pydantic failure;
canonical encoding/revalidation; stage ID/kind/unavailable/analyzed binding;
claim mismatch/duplicate/origin; non-fact subject; foreign/duplicate evidence,
qualification source, invalid/duplicate child link, unsupported fact; missing
source/child coverage; raw/canonical/claim/annotation/text limits. Generic fallbacks
are required when precise predicates are unknown. Never accept generated reasons.

Pydantic: call errors(include_input=False, include_context=False,
include_url=False), then sanitize rather than retaining dictionaries/messages.
Permit only fixed reason, static StageResult field path, bounded integer indices
and saturated failure count. Reject arbitrary/dynamic paths, IDs, input values,
messages, contexts and URLs. Multiple failures need deterministic primary selection
with documented priority; a primary reason is not necessarily the sole defect.

Refine combined validator causes without changing predicates or first-failure
order. Distinguish parsing, duplicate keys, Pydantic rejection, canonical failures
and canonical overflow. Diagnostics must never mask the original failure.

Trace provider execute → GenerationResult → GovernedExecution → managed adapter →
single-call observation/audit. Retain sanitized finish_reason, prompt/completion/
total/reasoning tokens, raw content-byte count and configured token/byte limits
where available. Missing is unknown, never zero. Preserve settlement before
application rejection, known/unknown usage, accounting cleanup markers, primary
provider failures and one-call terminal semantics. Never retain arbitrary provider
metadata or raw output.

Reproduce finish_reason=length with null content. If the completion-content parser
masks output_limit, make the smallest safe ordering correction. Test length with
null/empty/partial content; stop, refusal, missing choices and malformed finish
metadata. Never accept truncated content or retry.

Evaluate an optional exact production-schema diagnostic using installed offline
dependencies only. It must not change acceptance, requests or certify Azure service
support. Prefer a separately callable offline check if runtime risk would increase.

## WP-B comparison preservation

Verify authoritative pre-edit fingerprints rather than assuming historical values:
executor `9cd6711b61f2896090d351468e42dcc9a7c00f77e8f6cfc41c6f273172897b5a`,
generation `82ecad5d4cb2e8fd2e0981c7d3710bbb3a582e56ef9eebca07ab0f314a4d05f9`,
provider schema `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2`.
Distinguish current configuration, executor, provider schema and documented
historical Attempt 4 bindings. A preparation report is not proof of the exact live
submitted schema. Do not refresh approvals.

Capture complete deterministic GenerationRequest, Azure schema, provider payload,
profile/model bindings and rendered instructions for chunk/structural/root before
and after. Exclude only metadata already excluded by authoritative policy. Explain
any source-fingerprint change; unchanged semantic requests do not imply unchanged
approval hashes. All four profiles must remain satisfiable.

## WP-C inactive prompt candidate

Derive exact original render fragments. Prepare minimal M1/M2/M3 replacements,
rationale, exact predicate mapping, versioned patch and activation requirements in
`docs/codex/proposals/phase_17hl_generation_instruction_clarifications.md`.
Do not import/apply candidate instructions in runtime or reuse an old version.

M1: non-fact subjects null; fact subjects obey actual Token pattern/length
(historically ^[a-zA-Z0-9_./:-]+$, maximum 128). Facts need status=supported and
valid direct or acceptable child support. Unknown/unsupported findings use valid
kind/status; do not invent references. No duplicate evidence in each array or child
links within a claim; source IDs and child stage/claim pairs must match allowed sets.

M2: preserve qualifying information through required child lineage. Copy a
qualification directly only with currently allowed direct evidence; never invent
ancestor sources or discard required links. Explain immutable artifact retention
of qualifications/contradictions using actual validator/digest behavior. Include
positive lineage and negative ancestor-copy synthetic examples.

M3: analyzed analysis requires source coverage and evidence/support rules.
Unavailable is analysis-only, zero claims and nonempty limitation; do not fabricate
coverage/findings. Reduction cannot declare unavailable. Domain validators stay
unchanged. Test consistency for all profiles and both outcome branches; do not
claim improved real-model acceptance without live comparative evidence.

## WP-D architecture assessment

Create `docs/adr/phase_17hl_application_owned_identifiers_assessment.md` with
Proposed/Under Review status. Compare A (model returns complete StageResult) with B
(model returns semantic proposal and explicit source/child indices; trusted
application validates selections, supplies stage metadata, computes ordered claim
IDs, resolves only selected authorized relationships, constructs StageResult and
applies unchanged validators). No repair or fabricated relationship is permitted.

Assess security/authority, semantic responsibility, token/byte overhead, stable
ordering/mappings, all-profile coverage, qualification provenance, contradictions,
checkpoints, audits/fingerprints, migration/rollback and effect on historical
Phase 17H–L evidence. Indices may relocate failures; compare request-specific UUID
enums as a possible intermediate alternative. Recommend prototype/migration only
with identity/reference-specific future live evidence or substantial separate
offline advantage justifying explicit operator approval. Plan new schema/template
versions, construction boundary, no-bypass guarantee, tests, compatibility and
fresh approval implications. Do not implement production migration.

## Testing, review and quality

Use verified existing network denial before collection; prove the guard works,
count attempted accesses and expect zero attempts in real regressions. Preserve
permanent configuration isolation. Required new cases: malformed claim/stage/
evidence UUIDs, invalid/overlong subject, empty/overlong text, missing/type/enum/
extra errors, multiple errors, unsafe locations; stage/kind/identity/origin/duplicate
claims, non-fact subject, invalid unavailable, foreign/duplicate evidence,
qualification, child lineage, missing source/reduction coverage; provider success/
reasoning/unknown/invalid usage, truncation variants, refusal, missing finish,
unexpected model, output-limit plus cleanup failure. Verify privacy against input,
exception, arbitrary path, evidence UUID, document text, API token and raw body.

Run existing named compatibility/E2E/diagnostic suites and relevant document,
provider, schema, output-limit, single-call, governance, security, admission and
settlement regressions. Finally run the full suite; baseline 1519 passes, new cases
increase it. No hidden skips/xfails. Run Ruff check/format check on changed Python,
compileall with external cache, git diff --check/status/stat/cached names. Inspect
untracked files explicitly. Separate old lint debt from new issues; do not reformat
unrelated code.

Perform independent self-review and pre-commit review: frozen prompts/schema/
payload/predicates, public errors/retries, diagnostics privacy/determinism/fallbacks,
usage/error precedence, meaningful tests, preserved isolation, inactive candidate,
no identifier migration, accurately interpreted fingerprints and separate live
readiness. Check secrets/debug/temp/dependencies/unrelated changes and links.
Fix material findings before reporting; never mask blockers to return PASS.

## Documentation, acceptance and final handoff

Create report `docs/codex/reports/phase_17hl_live_failure_observability_and_contract_options.md`
and preserve this prompt at the matching prompts path. Report executive WP statuses,
diagnostics, exact before/after fingerprints, proposal/ADR, exact validation,
self/pre-commit review, unresolved confirmed versus hypothetical concerns, and
future separately authorized governed single-analysis recommendation only.

WP-A PASS requires precise private diagnostics, strict unchanged domain/public
semantics, preserved usage/output limits, meaningful tests and no unauthorized
operations. WP-B PASS requires unchanged active generation instructions/schema/
configuration/payload, verified hashes and honest historical comparison limits.
WP-C READY FOR REVIEW requires complete inactive versioned M1/M2/M3 evidence.
WP-D ASSESSED requires alternatives, safeguards, migration implications and
conditional decision with no production migration. Overall PASS requires all four
and green full offline regressions. PASS does not establish live compatibility or
authorize spending. Phase 17H remains PARTIAL.

Final structured response fields: TASK, BRANCH, HEAD, STARTING WORKTREE; WP-A status/
reasons/location/usage/output-limit/privacy; WP-B previous/current executor,
generation and schema hashes, semantic/request equivalence and limits; WP-C
M1/M2/M3/version/inactive/proposal; WP-D alternatives/security/evidence/complexity/
recommendation/no migration; TESTING baseline/new/full/failed/errors/skipped/
network/Ruff/compilation; SAFETY zero paid/cloud/operator approvals/live finances/
historical edits/commits/pushes; FILES CREATED/MODIFIED, PRODUCTION VALIDATORS
MODIFIED, ACTIVE GENERATION CONTRACT MODIFIED, UNRESOLVED ISSUES, REPORT PATH and
FINAL RECOMMENDATION.

Do not conduct a fifth Azure inference, create/sign approval or commit/push.
