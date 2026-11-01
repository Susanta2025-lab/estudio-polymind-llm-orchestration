# CODEX IMPLEMENTATION PROMPT
## ESTUDIO POLYMIND — PHASE 17H–L: FINAL OFFLINE AZURE STRICT-SCHEMA & APPLICATION-VALIDATOR COMPATIBILITY AUDIT

Clean Markdown execution-scope record of the supplied implementation prompt,
20 October 2026. The operator's original detailed requirements govern this task;
this record preserves its objectives, prohibitions, matrices and acceptance gates.

### Operator workflow and context

Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`.
Expected branch: `master`. Preferred model: GPT-6.1-Sol, high reasoning.
Task: independent offline architecture, schema, negative-testing and readiness audit.
Work directly on the current dirty tree. Inspect AGENTS.md and actual HEAD/status.
Preserve every existing implementation, diagnostic and test-isolation change.
Do not create/switch branches, stage, commit, push, merge, rebase, reset, stash,
restore, clean or discard files. Do not change runtime configuration.

Historical results: full normal offline regression 1,403 passed; previous 64
configuration failures/errors and 36 regression failures/errors reconciled;
31 offline L1 E2E and 25 diagnostic-hardening cases passed. External inference,
cloud changes and commits/pushes were zero. Phase 17H remains PARTIAL and real-model
L1 acceptance is NOT ESTABLISHED.

Historical Azure context (do not rediscover through Azure): ECI-Development;
Spain Central; resource `epolymind-foundry-dev-susanta`;
deployment `epolymind-gpt-54-mini`; model `gpt-5.4-mini`, version `2026-03-17`;
GlobalStandard; `/openai/v1` Chat Completions through the OpenAI-compatible adapter.
Use current nonsecret repository contracts as the source of truth.

Four previous billable attempts failed application acceptance. Attempt 1 involved
canonical byte expansion. Attempt 2's original output-limit trigger is unknown;
downstream error masking was corrected. Attempt 3 used JSON-object mode and had
a malformed evidence UUID and eight forbidden top-level fields. Attempt 4 used
strict JSON Schema and completed provider execution but failed local validation
with `serialization_error`; its precise cause is UNKNOWN. There is no retained
Attempt 4 response in the supplied sanitized evidence. Do not transfer Attempt 3's
diagnosis, reconstruct history or claim synthetic examples recover it.

### Strict offline and privacy boundary

No Azure or other model inference, endpoint HTTP, Azure management, Entra token
acquisition, RSA operator signing, live launcher execution, deployment, AKS startup,
paid operation, financial reservation or automatic provider retry. No new resources.
Do not read credentials, operator dotenv values, approval JWTs, private keys,
private responses, private approval packets or protected historical audit material.
Use fake providers, deterministic synthetic responses and temporary test authorities.
Do not install or upgrade packages or fetch documentation over the network.

Keep production validation, schema, prompts, converter and adapter unchanged.
Reproduce genuine defects and propose the smallest correction with implications
and regression coverage; leave production remediation for separate authorization.
Never repair model output by changing UUIDs, IDs, evidence, fields or lineage.
Never weaken Pydantic, closure, identity, stage binding, evidence membership,
coverage, qualification/conflict preservation, provenance, byte limits, financial
accounting, authorization or authentication. Preserve primary provider errors and
fail-closed unknown usage. Do not change historical audits or financial records.
Sanitized diagnostics must contain no raw response, prompt, document text, UUID,
evidence ID or confidential exception message.

### Objective

Compare all three actual production layers:

1. Application: StageResult/Pydantic, deterministic identities, stage binding,
   evidence, lineage, coverage, qualifications/conflicts, canonical serialization,
   limits and governance.
2. Provider: production-generated Azure-compatible schema, GenerationRequest and
   exact adapter HTTP payload for chunk, structural and root profiles.
3. Instructions: exact `ManagedSynthesisInference.render()` trusted instructions
   and dynamic controls.

Answer whether a provider-schema-valid result can satisfy every local acceptance
rule simultaneously without content repair. Provider-schema validity is not local
acceptance. Audit PASS means investigation complete, not live readiness or spend
authorization. This is not a fifth live attempt.

### Required reading and baseline

Read AGENTS.md, README/architecture, Phase 17A–17H reports, provider integration,
schema conversion, governance/accounting and current Phase 17H–L reports.
Specifically locate and inspect:

- `phase_17hl_diagnostic_hardening.md`
- `phase_17hl_regression_reconciliation.md`
- `phase_17hl_offline_e2e_contract_verification.md`
- `phase_17hl_full_suite_configuration_isolation.md`
- `phase_17hl_l1_attempt3_serialization_root_cause.md`
- `phase_17hl_output_limit_hardening.md`
- `phase_17hl_independent_json_byte_limits.md`

Inspect actual implementations and consumers of digestion models, codec, validation,
managed rendering, workflow, planning, EvidenceIndex and claim IDs; llm structured
contracts, Azure converter, OpenAI-compatible adapter and bounded HTTP;
`tests/performance/foundry_l1.py`, `foundry_single_call.py`; existing schema,
negative, E2E and diagnostic tests. Resolve real paths and report missing material.

Use only existing local material for Microsoft's structured-output, model capability
and reasoning documentation:

- https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs
- https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure
- https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning

Review required properties, nullable unions, closed objects, supported types/enums,
references, property/depth limits, unsupported string/numeric/array constraints,
and Chat Completions `response_format` versus Responses `text.format`. Local schema
validation cannot certify Azure acceptance. Do not install a validator.

Record `git status --short --branch`, HEAD, `git diff --check`, `git diff --stat`,
`git diff --cached --name-only`. Compare fingerprints only through repository hashing:
historical executor `9cd6711b61f2896090d351468e42dcc9a7c00f77e8f6cfc41c6f273172897b5a`;
generation contract `82ecad5d4cb2e8fd2e0981c7d3710bbb3a582e56ef9eebca07ab0f314a4d05f9`.
Never refresh approvals. Establish baseline with permanent settings isolation and
an independently verified network-denial safeguard active before collection.

### Required contract investigation

For each managed chunk/structural/root request, derive the Pydantic schema,
generation schema, converted provider schema, rendered request and HTTP payload
through actual production paths. Verify `json_schema`, name
`polymind_stage_result`, `strict=true`, exact populated schema and correct API route.

Compare every StageResult, Claim, Qualification and ClaimLink field: type,
required/default status, nullability, Pydantic constraints, provider constraints,
removed/transformed constraints, local responsibilities and possible local rejection.
Verify the historical four definitions/22 properties, depth, references and schema
size. Classify conversion as exact preservation, provider weakening with retained
local validation, ambiguity, unexpected accepted-value change or unsatisfiability.
Provide reproducible evidence for ambiguity, changed acceptance or contradictions.

Audit all application-only rules, including UUID/text/token bounds, exact types,
closed fields, serialization and normalized values. Verify claim IDs against
`stable_id(str(request.stage_id), str(position))`, supplied consecutive IDs,
zero/multiple claims, reductions, wrong valid UUIDs, malformed UUIDs, duplicates
and order. Verify stage/kind/outcome/origin/profile/config/role/model bindings.

Trace original-source allowed evidence through analysis and child reductions.
Verify membership, duplicates, missing/foreign references, contradiction sources,
qualification sources, required child links and source coverage. Generated summaries
are never original evidence. Confirm actual four-page → one analysis → structural
reduction → root reduction → COMPLETE digest topology and outcome transitions.

Inspect exact dynamic controls: stage_id, kind, allowed_evidence_ids,
claim_ids_in_order, required_child_links, max_claim_characters, max_annotations,
max_result_bytes, max_response_bytes and schema. Do not claim existing controls
are missing. Identify actual ambiguities or impossible branches with source evidence.

Create deterministic valid witnesses for every stage, accepted by provider schema,
Pydantic, stage/claim, evidence/lineage/coverage, canonical serialization and bounds.
Verify schema validity before claiming a counterexample is provider-valid. Mutate
IDs, stage, evidence, lineage, coverage and strings to isolate local rejection.
No bypass or post-generation repair is permitted.

Independently verify 3,000 completion tokens, 10,000 raw UTF-8 bytes, 10,000 canonical
ASCII JSON bytes and 26,192 envelope bytes against current configuration. Test
exact/one-over boundaries, defaults/nulls, Unicode/encoding differences, duplicate
JSON keys, truncation, incomplete finish reasons, missing usage and envelope overflow.
Do not raise limits. Determine whether schema-valid responses can exceed local caps.

Trace fake HTTP → bounded decoder → adapter usage/finish metadata → raw text →
Pydantic/application validation → canonical result → settlement/durable outcome,
correcting this proposed ordering to the actual implementation. Inspect refusal,
filtering, absent/empty content, output-limit/schema errors, incomplete usage and
cleanup error precedence. Preserve known usage and UNKNOWN reservations.

Verify first applicable diagnostic among json_decode, duplicate_json_key,
pydantic_validation, canonical_serialization, stage_binding, claim_identity,
claim_contract, evidence_validation, coverage_validation and response_limit.
Public categories must remain unchanged; diagnostics must be typed/allowlisted,
content-free and optional without suppressing failure. Stage attribution does not
identify an exact offending field.

Separate confirmed local defects, documented Azure limitations, potential live
incompatibilities and unsupported hypotheses. Do not claim an offline fake proves
GPT-5.4-mini generation, exact historical cause or deployment compatibility.

### Testing and review

Add targeted deterministic synthetic tests with meaningful failure assertions.
Cover schema/conversion/closure/nullability/requiredness/bounds, stage rendering,
IDs, membership/lineage/coverage, structural/local counterexamples, canonical
expansion, finish metadata, classification and sanitized diagnostics.

Rerun E2E, diagnostic, unit documents, foundry unit/integration, structured provider,
output-limit, relevant security/governance and full normal configured regression:
`python -m pytest -q`. Activate the separate network guard before collection.
Preserve all 1,403 existing tests including 23 settings-isolation tests; do not
hide failures with skips or xfails. New cases increase the expected total.

Run Ruff lint/format checks on new Python files, compilation with an external
cache, and `git diff --check`. Do not format unrelated code. Record exact counts,
commands, limitations and existing warning/lint debt. No dependency installation.

Perform a separate self-review for exact schema fidelity, genuinely accepted
witnesses, mutation-test effectiveness, privacy, accounting/replay/error precedence
and evidence-qualified conclusions. Pre-commit review must check secrets, paths,
debug/temp/generated artifacts, dependencies, historical files, accidental API or
runtime changes and all untracked files. Re-run Git status/diff/index checks.
Do not stage or commit.

### Acceptance and reporting

Audit PASS requires complete schema/payload/transformation/application/instruction
analysis, all-stage witnesses, verified counterexamples, independent limits,
diagnostics/accounting evidence, green full offline regression, complete matrices,
documented findings/uncertainties, defensible readiness and no prohibited action.
PARTIAL means incomplete analysis/evidence or unexplained tests; BLOCKED means
essential evidence/tooling unavailable; FAIL means critical requirement violation,
regression, weakened controls, secret exposure or prohibited activity.

Independently choose READY (no known offline blocker), CONDITIONAL (no critical
blocker but risks/safeguards need review), or NOT READY (critical incompatibility,
unsafe path, unsatisfiable contract or unresolved correctness defect).

Create `docs/codex/reports/phase_17hl_final_offline_azure_compatibility_audit.md` and
this prompt record. Include executive result, detailed field/cross-rule compatibility
matrix, rejection/diagnostic matrix, exact production contracts/fingerprints,
instruction ambiguities/conflicts, accounting, commands/counts/network guard,
independent reviews and severity-classified findings. Each finding needs evidence,
root cause/uncertainty, impact, smallest proposed correction, verification and
whether live inference is needed. Distinguish audit PASS from readiness.

For any recommended future single call, require fresh executor/config/generation
review, fresh identity/credentials, independent RSA approval, explicit single-call
authorization, existing shared financial ceiling/pricing/reservation, no retries,
sanitized diagnostics, one-call stop condition and post-call/accounting review.
Do not create/sign/execute those artifacts or reuse historical approvals.

Explicit limitations:

```text
Offline schema compatibility != Azure service-side acceptance
Schema-valid JSON != Application-valid StageResult
Application-valid StageResult != Semantically correct model output
Successful synthetic workflow != Successful live workflow
Audit PASS != Authorization to spend
```

Final response must concisely report task/result/readiness, starting Git state,
contract/provider/negative-testing conclusions, severity counts, exact validation
results, all zero-activity safety counts, files created/modified, production changes,
unresolved risks, report link and recommendation. Phase 17H remains PARTIAL.
The next live inference requires a new independently reviewed and explicitly
authorized operator action. This task provides analysis only.
