# Phase 17H–L — documentation remediation and README synchronization

Date: 1 November 2026. Branch: master. Mode: documentation-only implementation
and offline static verification. [Normalized operator task](../prompts/phase_17hl_documentation_remediation_and_readme_sync.md).

## 1. Executive summary and verdict

**DOCUMENTATION REMEDIATION: PASS.** All twelve original publication artifacts
were reviewed and their findings resolved. Five identifier findings and five
machine-path findings are sanitized; both proposal artifacts are clearly situated
as inactive history through the companion notice. The patch itself is unchanged.
Eight Git-visible READMEs were reviewed; four were updated. This task modifies
36 existing Markdown files and adds two Markdown files: 38 documentation changes
in total, including the required report. No executable behavior changes.

**C2: READY for manual documentation/publication review. C1: CONDITIONALLY READY**
for manual engineering review, preserving all 69 original engineering members.
The condition concerns the separate engineering acceptance/review boundary and
historical lint/regression limitations, not an unresolved documentation blocker.
There are **0 publication blockers, 0 HOLD files and 0 EXCLUDE files** in this
Git-visible pending inventory. READY does not authorize staging, committing,
deployment or inference. Full Phase 17H remains PARTIAL.

## 2. Scope and restrictions

Work was limited to Markdown, publication sanitization, cross-references, dated
scope notices and static verification. The operator's restrictions supersede
general implementation-phase test/deployment guidance: no application imports,
runtime rehearsal, pytest, compileall, Docker/Kubernetes, cloud operation or paid
inference was needed or performed. No dependency was installed. No private
credential, JWT payload, key, raw provider output, ignored operator directory or
protected private artifact was read. All inventory/scan inputs came from Git's
cached plus nonignored untracked file lists. Temporary audit scripts/snapshots
remain outside the checkout under task-specific `/tmp` paths.

No production Python, test implementation, frozen fixture, runtime configuration,
policy, `.gitignore`, managed prompt implementation or source binding was edited.
AGENTS.md's prompt/report convention is satisfied by the normalized task record
and this report. Existing uncommitted work remains in place, uncommitted/unstaged.

## 3. Starting Git state and preservation baseline

Actual initial branch was `master`; HEAD was
`af4a7a076c918ef13aea05d74bf239c0af909133`. File-level porcelain status measured
**20 modified tracked files + 129 untracked files = 149 pending files**, with
**0 staged files**. Initial tracked diff was **894 insertions, 81 deletions across
20 files**. This independently matches the supplied audit observation.

The baseline captured the exact 149 pending paths, 412 existing Git-visible file
SHA-256 values, index entries, branch/HEAD and all eight README paths before edits.
Original public Markdown/patch copies support full task-only diff inspection.
Every initial pending path is retained. The complete final manifest in section 15
labels the exact preserved engineering membership and expanded documentation set;
it also accounts for all original pending paths without directory collapsing.

## 4. Original twelve findings and resolutions

Placeholders are descriptive publication text, not replacement runtime settings.
Original identifier values are intentionally absent here. PASS includes a fresh
static original-value/path recheck and manual semantic review of the correction.

| # | File | Original finding category | Correction performed | Verification | Remaining concern |
|---|---|---|---|---|---|
| 1 | [docs/codex/prompts/phase_17hl_attempt5_operator_authorization_and_single_call_execution.md](../prompts/phase_17hl_attempt5_operator_authorization_and_single_call_execution.md) | Actual subscription, tenant and resource identifiers | Replaced with AZURE_SUBSCRIPTION_ID, AZURE_TENANT_ID and FOUNDRY_RESOURCE_NAME placeholders; resource URI/host structure preserved. | PASS | None within publication scope |
| 2 | [docs/codex/reports/phase_17hl_attempt5_operator_authorization_and_single_call_execution.md](phase_17hl_attempt5_operator_authorization_and_single_call_execution.md) | Actual subscription/tenant identifiers | Replaced only the historical environment UUIDs; deployment/account observations and financial figures preserved. | PASS | None within publication scope |
| 3 | [docs/codex/reports/phase_17hl_attempt5_live_execution_report.md](phase_17hl_attempt5_live_execution_report.md) | Actual Entra public-client identifier | Replaced with ENTRA_PUBLIC_CLIENT_ID; delegated authentication semantics preserved. | PASS | None within publication scope |
| 4 | [docs/codex/reports/phase_17hl_final_operator_authorization.md](phase_17hl_final_operator_authorization.md) | Actual API application scope identifier | Replaced with `api://<ENTRA_API_CLIENT_ID>/access_as_user`; scope semantics preserved. | PASS | None within publication scope |
| 5 | [docs/codex/reports/phase_17hl_launch_authorization_final.md](phase_17hl_launch_authorization_final.md) | Actual API application scope identifier | Same API scope placeholder; independent signing and authentication remain separate. | PASS | None within publication scope |
| 6 | [docs/codex/reports/phase_17hl_ast_test_portability_fix.md](phase_17hl_ast_test_portability_fix.md) | Machine-specific interpreter paths | Replaced with PYTHON_311/PYTHON_312 symbolic shell variables; definitions and original interpreter versions documented. | PASS | None within publication scope |
| 7 | [docs/codex/reports/phase_17hl_attempt5_final_readiness_and_operator_preparation.md](phase_17hl_attempt5_final_readiness_and_operator_preparation.md) | Machine-specific project interpreter | Replaced with PYTHON; explicit local assignment instructions; retained the historical external driver and outcomes. | PASS | None within publication scope |
| 8 | [docs/codex/reports/phase_17hl_f1_http_cleanup_failure_preservation.md](phase_17hl_f1_http_cleanup_failure_preservation.md) | Machine-specific interpreter/checkout paths | Replaced with PYTHON/PROJECT_ROOT, quoted historical commands and documented assignments; test counts and source bindings retained. | PASS | None within publication scope |
| 9 | [docs/codex/reports/phase_17hl_live_execution_preparation.md](phase_17hl_live_execution_preparation.md) | Personal home/private handoff paths | Replaced with symbolic operator/trust locations; historical live command marked inactive text, with closure link. | PASS | None within publication scope |
| 10 | [docs/codex/reports/phase_17hl_single_call_execution_failure_diagnosis.md](phase_17hl_single_call_execution_failure_diagnosis.md) | Private audit location | Replaced with PRIVATE_AUDIT_DIRECTORY and related symbolic packet/authority/replay locations; private job/approval IDs also abstracted. | PASS | None within publication scope |
| 11 | [docs/codex/proposals/managed_prompt_4.patch](../proposals/managed_prompt_4.patch) | Inactive broader proposal patch could be mistaken for deployed v4 | Reviewed without mutation; companion archival notice explicitly prohibits applying it as a current runtime update. | PASS | None within publication scope |
| 12 | [docs/codex/proposals/phase_17hl_generation_instruction_clarifications.md](../proposals/phase_17hl_generation_instruction_clarifications.md) | Ambiguous proposal-era runtime status | Added dated ARCHIVED notice, narrower active-v4 explanation and authoritative implementation/closure links; retained original proposal text. | PASS | None within publication scope |

The five identifier files retain dates, decisions, scope names, permission semantics,
test/financial figures and historical execution conclusions. Sanitization does not
touch Foundry source allowlists, Entra runtime settings or protected configurations.

## 5. Complete README inventory and review decisions

Discovery used `git ls-files --cached --others --exclude-standard -z`, then a
case-insensitive README basename inventory. All eight files were read; no ignored
or private directory walk was needed. Four were updated and four left byte-identical.

| Path | Reviewed | Updated | Audience, reason and disposition | Current validation |
|---|---|---|---|---|
| [README.md](../../../README.md) | YES | YES | Developer/reviewer entry point; replaced stale live-pending claims, added bounded status table and operational/test links. | PASS: static content and relative links; unchanged bytes for NO rows |
| [deployment/helm/polymind/README.md](../../../deployment/helm/polymind/README.md) | YES | YES | Deployment operator guide; clarified static-bearer chart versus single-host OIDC authorities and bounded Attempt 6 evidence; corrected security cross-references. | PASS: static content and relative links; unchanged bytes for NO rows |
| [deployment/kind/phase10/README.md](../../../deployment/kind/phase10/README.md) | YES | NO | Dedicated Kind smoke workflow with synthetic dependencies; no affected Phase 17H–L claim. | PASS: static content and relative links; unchanged bytes for NO rows |
| [deployment/kind/phase13/README.md](../../../deployment/kind/phase13/README.md) | YES | NO | Local availability baseline and synthetic token/stream workflow; no affected Phase 17H–L claim. | PASS: static content and relative links; unchanged bytes for NO rows |
| [deployment/kind/phase14/README.md](../../../deployment/kind/phase14/README.md) | YES | NO | Scoped Prometheus validation fixture; no affected Phase 17H–L claim. | PASS: static content and relative links; unchanged bytes for NO rows |
| [deployment/kind/phase15/README.md](../../../deployment/kind/phase15/README.md) | YES | NO | Kind autoscaling interoperability fixture; explicitly avoids production capacity claims; no affected Phase 17H–L content. | PASS: static content and relative links; unchanged bytes for NO rows |
| [tests/README.md](../../../tests/README.md) | YES | YES | Test contributor guide; separates offline units/integration, synthetic Foundry/RSA/governance, settings isolation and live boundaries. | PASS: static content and relative links; unchanged bytes for NO rows |
| [tests/fixtures/digestion_contracts/README.md](../../../tests/fixtures/digestion_contracts/README.md) | YES | YES | Contract maintainer provenance; clarified historical v3 checksum versus active v4 and linked later evidence. | PASS: static content and relative links; unchanged bytes for NO rows |

## 6. Root README changes

The opening status table now links Phase 17G acceptance, Phase 17H evaluation,
the active v4 implementation, offline integration and Attempt 6 closure. The
provider table, Phase 17E limitation, roadmap, limitations and closing milestone
now agree: one accepted first-chunk analysis is a narrow live milestone, while
full live L1 digestion and subsequent grounded Q&A remain unvalidated.

Architecture remains FastAPI/Streamlit/LangGraph over the provider-neutral
InferenceProvider boundary, with Ollama and external OpenAI-compatible inference.
RAG, extraction, hierarchical synthesis, publication, citations and provenance
remain described as implemented contracts with reference-adapter limitations.
SecurityAuthority, explicit Entra verification, quota/cost governance, separate
RSA approval and UNKNOWN accounting are explained without advertising production
deployment. The README links security, governance, evaluation and test runbooks
instead of reproducing the live failure postmortem.

## 7. Test README synchronization and command verification

The test guide distinguishes offline units, offline integration, synthetic Foundry
transport/workflow tests, synthetic financial ledgers and temporary RSA approvals,
historical frozen v3 contracts, active v4 witnesses and live-capable performance
harnesses. The fixture README clarifies the original historical renderer checksum,
test-only execution of hash-pinned v3 source and unchanged authoritative acceptance.
No frozen fixture was edited or regenerated.

The published `python -m pytest tests/unit -q`, `python -m pytest tests/integration -q`
and existing default pytest command were statically checked against `pytest.ini`,
the directory/module inventory, root conftest, settings-isolation helper and relevant
test/harness source. They were **not executed by this documentation task**. Default
collection is offline; performance modules require explicit invocation. No test
README contains a paid live execution example.

Settings isolation suppresses implicit application dotenv loading; exported values
and explicit controlled dotenv inputs still apply. It does not itself deny network.
The guide explains pre-collection network denial and environment/output isolation
without assuming historical external verification plugins are installed. No new
no-network test result is claimed here.

## 8. Security and governance documentation

[17G operations](../../security/phase_17g.md) now states its accepted reference
PASS and the later single-call success while retaining OIDC restrictions, private
authority requirements, tenant/owner isolation, revocation and UNKNOWN obligations.
[Entra v2](../../security/entra_v2.md) separates original no-live implementation
observations from later evidence and retains exact tenant-specific issuer, API
audience, delegated scope and role requirements. Synthetic UUID examples remain.

[Evaluation governance](../../governance/evaluation-policy.md) links the settled
result without resetting allowances, changing the EUR 5 overlay, modifying any
allowlist or asserting current Azure commercial terms. The [production runbook](../../security/production-security.md)
and [threat model](../../security/threat-model.md) clarify static-bearer/Phase 11
scope versus later reference OIDC and container hardening. They do not certify a
distributed deployment. These are documentation changes; policy and authorization
requirements remain unchanged.

## 9. Evaluation/runbook synchronization and historical chronology

[Foundry validation](../../evaluation/phase_17h_foundry_validation.md) now opens
with a dated current interpretation, explicitly separating historical L0 proposals
and dated handoffs from active v4/strict-output contracts. [Operator approval](../../evaluation/phase_17hl_operator_approval.md)
records consumed Attempt 6 authority, distinct L1/single-analysis audiences and
symbolic private key location. Its independent RSA review, exact configuration
digest, replay protection, 600-second exclusive launch cutoff and financial gates
remain intact. API-key credential-use deadlines remain operator attestations.
[17H methodology](../../evaluation/phase_17h.md) retains offline commands and
quality/reliability gates. [Structured-output engineering](../../engineering/llm_structured_output_validation.md)
adds exact-deployment single-analysis evidence without equating provider structure
with domain acceptance or semantic support.

The authoritative [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md)
is unchanged. Its failure chronology remains:

| Attempt | Retained conclusion |
|---|---|
| 1 | Canonical serialization expanded beyond the configured byte ceiling. |
| 2 | Provider output-limit failure was masked by later governance handling; exact original trigger remains UNKNOWN. |
| 3 | Malformed evidence UUID and eight forbidden top-level fields. |
| 4 | Completed strict response, application rejection; exact rejecting predicate remains UNKNOWN. |
| 5 | `subject_on_nonfact`; confirmed managed-prompt/3 instruction-to-validator gap. Earlier blocked/preparation checkpoints remain accurate for their dates. |
| 6 | Active managed-prompt/4 produced one accepted live analysis with durably settled known usage and no automatic retries. |

The separate non-billable preflight launch failure remains separate from billable
Attempts 1–5. No missing Attempt 4 measurements, original Attempt 2 trigger or
additional historical explanation is invented.

| Attempt 6 measure | Retained value |
|---|---|
| State / calls | SUCCEEDED / 1 |
| Application validation | accepted |
| accounting_failed | false |
| Financial settlement | SETTLED |
| Input / output / total tokens | 2476 / 1814 / 4290 |
| Catalog-accounted cost, EUR | 0.008817317845829546 |

This cost is local catalog accounting, not an independently verified Azure invoice.
The original closure, v4 implementation and offline integration reports remain
byte-identical; their historical test counts are attributed evidence, not reruns.

Current-state search dispositions:

| Classification | Evidence and action |
|---|---|
| CURRENT BUT OUTDATED | Root README's live-pending statements and 17G operations' blanket BLOCKED/PENDING statement corrected. Production security's blanket future-OIDC statement qualified. |
| AMBIGUOUS | Legacy Foundry runbook, operator procedure, original threat model and earlier handoffs receive dated scope/status notices and closure links. |
| HISTORICALLY CORRECT | October v3 usage, Attempt 5 blocked checkpoints and 29 October future-Attempt-6 readiness statements preserved. The historical proposal body remains proposal-era text. |
| CURRENT AND CORRECT | Active structured-output v4 contract, accepted reference 17G scope, unchanged Kind fixture documentation and base evaluation methodology preserved. |
| UNVERIFIED | Full live L1 reductions/digest/Q&A, representative semantic quality, current independent Azure billing, distributed/production readiness and independent 17J–17L definitions remain unclaimed. |

## 10. Historical proposal archival clarification

The companion now visibly says ARCHIVED, dated 1 November 2026; prohibits applying
the patch as a current runtime update; separates broader qualification/unavailable
analysis changes from the deployed narrow subject-contract correction; and links
the authoritative v4 implementation and successful Attempt 6 closure. Original
proposal-era wording and activation discussion remain historical evidence under
that notice, not a new instruction to patch runtime.

| Patch byte evidence | SHA-256 |
|---|---|
| Before | `e96c2e784ea587f12f49ef4f64ce82229e296a821107bab8f84b7db165900201` |
| After | `e96c2e784ea587f12f49ef4f64ce82229e296a821107bab8f84b7db165900201` |

**MATCH / byte-for-byte preservation: YES.** The patch was read/hash-checked only;
it was not applied, regenerated, reformatted, moved, renamed or deleted.

## 11. Publication/security recheck

**PASS after contextual review.** The final offline scan covers 91
Git-visible pending documentation/configuration-example artifacts plus reviewed
READMEs, including Markdown, the preserved patch, two JSON templates and
`.env.example`. Ignored protected directories were excluded. The scanner reports
only safe paths, line numbers and categories; no removed operational identifier
or confidential value is reproduced here.

Checks covered the known original environment identifiers, UUID context,
personal/private location patterns, credential-shaped values/assignments,
credential URLs, JWT shapes and private PEM markers. Manual diff/content review
checked raw response/source content, private scopes, runtime artifacts, misleading
live instructions and generated/debug material. All literal retained UUIDs were
classified: synthetic tenant/API examples, all-zero template scopes, or intentional
public migration-event identifiers. Public project/deployment names are deliberate
historical context, not hidden credentials. The Helm sample's replacement-key
assignment is explicitly schematic; no operational secret was found.

Additional private paths in historical preparation, activation, handoff and
postmortem documents were abstracted. Historical packet file names and report/date
context retain provenance; separate attempt audit placeholders remain distinct.
Private job/approval identifiers in the preflight diagnosis were abstracted.
Historical live/signing command blocks with replaced paths are inactive text and
explicitly must not be executed. No runtime database or protected artifact was
added to the manifest. A heuristic publication scan is not a general security audit.

## 12. Documentation/link and whitespace verification

| Executed static check | Outcome |
|---|---|
| `git diff --check` | PASS, exit 0 |
| Separate UTF-8/newline/trailing-whitespace check, including untracked documentation | PASS; intentional Markdown two-space hard breaks permitted |
| Relative Markdown targets in 87 reviewed/pending Markdown files | PASS, 478 relative links checked; 0 broken targets |
| Markdown heading fragments and source line references | PASS, 37 fragments/line references checked |
| Original five identifier and five machine-path findings | PASS, absent after scoped replacement |
| Both proposal artifacts | PASS, dated notice and matching patch bytes |
| Complete task-only documentation diff and pre-commit review | PASS within authorized scope |

Link checks resolve file/directory targets relative to each document, reference
definitions, heading slugs including duplicate headings, and source `#L` bounds.
Code fences, external URLs and badges are excluded from local link resolution.
No external website verification or cloud contact was performed. Published new
test commands were verified statically, not executed. No unrelated application
suite, cloud check, paid request or cryptographic operation was run.

## 13. Source and historical evidence preservation

All 69 original C1 members remain byte-identical to the task baseline. Every
production Python file, test implementation, frozen fixture and runtime/example
configuration retains its baseline bytes, including pre-existing dirty changes.
The 36 existing-file edits are Markdown only; all other 376 captured files remain
unchanged. There are no removals, unexpected edits or unknown additions.

Without importing application code, static stdlib calculation reproduced the
inspected executor/generation digest algorithms over Git-visible Python source:

| Binding | Recomputed value |
|---|---|
| Executor source | `d9af24e556305246ec145d15b3511e3e65fcf4e955e5b5f0dc550b4119b58a75` |
| Generation contract source | `74cf9320b0ebf6d45df531e81827c5a8710b5b4d58fa75aad05dfa5039552290` |

Both match the unchanged authoritative closure/v4 reports. Provider-schema and
inference-configuration input bytes are unchanged; those runtime calculations
were not rerun. No fingerprint was rewritten. A separate historical comparison
preserved **1,514 numeric lines** in remediated historical documents, excluding
only the expressly sanitized path/identifier lines, and retained every original
64-hex source/evidence hash. Manual review covered excluded lines and confirmed
that only location/identifier text changed, not outcomes. Attempts 1–6 measurement
authority remains the unchanged closure report.

Implementation self-review found and fixed an intermediate symbolic-path mapping
that confused an approval artifact filename with the signing-key directory.
Final handoffs preserve the distinction between private operator packet, signing,
trust, audit, replay and authority locations. Separate pre-commit review checked
secrets, paths, generated artifacts, source/configuration changes, historical
claims and links; no unresolved publication issue remains.

## 14. Exact task changed-file manifest

This is the task delta relative to captured starting bytes, not the entire dirty
working tree. There are **36 existing Markdown edits + 2 new Markdown artifacts
= 38 files**, consisting of four README edits and 34 other documentation files.
The preserved patch is intentionally absent here because its bytes did not change.

| File | Task state | Purpose |
|---|---|---|
| [README.md](../../../README.md) | MODIFIED | README synchronization |
| [deployment/helm/polymind/README.md](../../../deployment/helm/polymind/README.md) | MODIFIED | README synchronization |
| [docs/codex/prompts/phase_17hl_attempt5_operator_authorization_and_single_call_execution.md](../prompts/phase_17hl_attempt5_operator_authorization_and_single_call_execution.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/prompts/phase_17hl_documentation_remediation_and_readme_sync.md](../prompts/phase_17hl_documentation_remediation_and_readme_sync.md) | NEW | Task/report evidence |
| [docs/codex/prompts/phase_17hl_first_failure_diagnosis.md](../prompts/phase_17hl_first_failure_diagnosis.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/prompts/phase_17hl_offline_readiness.md](../prompts/phase_17hl_offline_readiness.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/proposals/phase_17hl_generation_instruction_clarifications.md](../proposals/phase_17hl_generation_instruction_clarifications.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17h_live_preflight.md](phase_17h_live_preflight.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17hl_ast_test_portability_fix.md](phase_17hl_ast_test_portability_fix.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17hl_attempt5_final_readiness_and_operator_preparation.md](phase_17hl_attempt5_final_readiness_and_operator_preparation.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17hl_attempt5_live_execution_report.md](phase_17hl_attempt5_live_execution_report.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17hl_attempt5_operator_authorization_and_single_call_execution.md](phase_17hl_attempt5_operator_authorization_and_single_call_execution.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17hl_attempt5_operator_checklist_verification.md](phase_17hl_attempt5_operator_checklist_verification.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17hl_azure_strict_schema_live_compatibility.md](phase_17hl_azure_strict_schema_live_compatibility.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17hl_documentation_remediation_and_readme_sync.md](phase_17hl_documentation_remediation_and_readme_sync.md) | NEW | Task/report evidence |
| [docs/codex/reports/phase_17hl_evaluation_activation_readiness.md](phase_17hl_evaluation_activation_readiness.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17hl_evaluation_policy_activation.md](phase_17hl_evaluation_policy_activation.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17hl_f1_http_cleanup_failure_preservation.md](phase_17hl_f1_http_cleanup_failure_preservation.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17hl_final_operator_authorization.md](phase_17hl_final_operator_authorization.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17hl_l1_attempt3_preparation.md](phase_17hl_l1_attempt3_preparation.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17hl_launch_authorization_final.md](phase_17hl_launch_authorization_final.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17hl_live_execution_preparation.md](phase_17hl_live_execution_preparation.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17hl_same_day_attempt2_handoff.md](phase_17hl_same_day_attempt2_handoff.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17hl_second_attempt_preparation.md](phase_17hl_second_attempt_preparation.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17hl_single_call_execution_failure_diagnosis.md](phase_17hl_single_call_execution_failure_diagnosis.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/codex/reports/phase_17hl_single_call_harness_offline.md](phase_17hl_single_call_harness_offline.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/engineering/llm_structured_output_validation.md](../../engineering/llm_structured_output_validation.md) | MODIFIED | Current-state scope / runbook synchronization |
| [docs/engineering/postmortems/Estudio_PolyMind_Phase17HL_L1_Three_Attempts_Postmortem_2026-10-16.md](../../engineering/postmortems/Estudio_PolyMind_Phase17HL_L1_Three_Attempts_Postmortem_2026-10-16.md) | MODIFIED | Publication sanitization / archival clarification |
| [docs/evaluation/phase_17h.md](../../evaluation/phase_17h.md) | MODIFIED | Current-state scope / runbook synchronization |
| [docs/evaluation/phase_17h_foundry_validation.md](../../evaluation/phase_17h_foundry_validation.md) | MODIFIED | Current-state scope / runbook synchronization |
| [docs/evaluation/phase_17hl_operator_approval.md](../../evaluation/phase_17hl_operator_approval.md) | MODIFIED | Current-state scope / runbook synchronization |
| [docs/governance/evaluation-policy.md](../../governance/evaluation-policy.md) | MODIFIED | Current-state scope / runbook synchronization |
| [docs/security/entra_v2.md](../../security/entra_v2.md) | MODIFIED | Current-state scope / runbook synchronization |
| [docs/security/phase_17g.md](../../security/phase_17g.md) | MODIFIED | Current-state scope / runbook synchronization |
| [docs/security/production-security.md](../../security/production-security.md) | MODIFIED | Current-state scope / runbook synchronization |
| [docs/security/threat-model.md](../../security/threat-model.md) | MODIFIED | Current-state scope / runbook synchronization |
| [tests/README.md](../../../tests/README.md) | MODIFIED | README synchronization |
| [tests/fixtures/digestion_contracts/README.md](../../../tests/fixtures/digestion_contracts/README.md) | MODIFIED | README synchronization |

## 15. Updated C1/C2 commit-readiness assessment and complete pending manifest

**C1 — 69 files, CONDITIONALLY READY.** Original engineering membership is
unchanged. Keep coupled runtime modules, tests and frozen fixture evidence together.
This documentation task introduces no engineering blocker, but does not substitute
for operator review/acceptance of that pre-existing implementation. The v4 report
records 447 selected passing tests and 42 existing Ruff findings; the later
offline readiness report records 108 distinct passing checks. Historical full-suite
evidence predates the final v4 edits. Those counts are not added or presented as
a fresh complete-suite pass. No new full-suite run is required or claimed here.

**C2 — 87 files, READY for manual documentation/publication review.** Original
80 documentation/configuration-example members remain, plus five newly pending
tracked documents (root README, Helm README, 17H methodology, production security
and threat model) and two new Markdown artifacts (normalized prompt and this report).
Sanitized historical files were already in C2 and are not double-counted. Commit
C1 before C2 or review them together so active-source links describe the included
implementation; do not apply the archived patch.

**HOLD: 0. EXCLUDE: 0.** This means no pending Git-visible file is omitted or
requires publication remediation outside scope. Ignored protected private storage
is outside this inventory and must remain private; it is not silently included
as commit material. Manual staging must use the exact file manifest, not ignored
directories or an indiscriminate forced add.

| Every pending file | Classification | Review rationale |
|---|---|---|
| [.env.example](../../../.env.example) | C2 | Pre-existing configuration example; synthetic placeholders; unchanged by remediation |
| [README.md](../../../README.md) | C2 | Documentation / historical evidence |
| [deployment/helm/polymind/README.md](../../../deployment/helm/polymind/README.md) | C2 | Documentation / historical evidence |
| [docs/adr/phase_17hl_application_owned_identifiers_assessment.md](../../adr/phase_17hl_application_owned_identifiers_assessment.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17h_live_preflight.md](../prompts/phase_17h_live_preflight.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_ast_test_portability_fix.md](../prompts/phase_17hl_ast_test_portability_fix.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_attempt5_final_readiness_and_operator_preparation.md](../prompts/phase_17hl_attempt5_final_readiness_and_operator_preparation.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_attempt5_operator_authorization_and_single_call_execution.md](../prompts/phase_17hl_attempt5_operator_authorization_and_single_call_execution.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_attempt5_readiness_authorization_assessment.md](../prompts/phase_17hl_attempt5_readiness_authorization_assessment.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_diagnostic_hardening.md](../prompts/phase_17hl_diagnostic_hardening.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_documentation_remediation_and_readme_sync.md](../prompts/phase_17hl_documentation_remediation_and_readme_sync.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_entra_v2.md](../prompts/phase_17hl_entra_v2.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_f1_http_cleanup_failure_preservation.md](../prompts/phase_17hl_f1_http_cleanup_failure_preservation.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_final_handoff.md](../prompts/phase_17hl_final_handoff.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_final_offline_azure_compatibility_audit.md](../prompts/phase_17hl_final_offline_azure_compatibility_audit.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_first_failure_diagnosis.md](../prompts/phase_17hl_first_failure_diagnosis.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_full_suite_configuration_isolation.md](../prompts/phase_17hl_full_suite_configuration_isolation.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_l1_attempt3_serialization.md](../prompts/phase_17hl_l1_attempt3_serialization.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_live_execution_preparation.md](../prompts/phase_17hl_live_execution_preparation.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_live_failure_observability_and_contract_options.md](../prompts/phase_17hl_live_failure_observability_and_contract_options.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_managed_prompt4_subject_contract_implementation.md](../prompts/phase_17hl_managed_prompt4_subject_contract_implementation.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_offline_e2e_contract_verification.md](../prompts/phase_17hl_offline_e2e_contract_verification.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_offline_readiness.md](../prompts/phase_17hl_offline_readiness.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_operator_approval.md](../prompts/phase_17hl_operator_approval.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_preflight_observability_timing_hardening.md](../prompts/phase_17hl_preflight_observability_timing_hardening.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_regression_reconciliation.md](../prompts/phase_17hl_regression_reconciliation.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_reusable_evaluation_governance.md](../prompts/phase_17hl_reusable_evaluation_governance.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_same_day_attempt2.md](../prompts/phase_17hl_same_day_attempt2.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_second_attempt_preparation.md](../prompts/phase_17hl_second_attempt_preparation.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_structured_output_compatibility.md](../prompts/phase_17hl_structured_output_compatibility.md) | C2 | Documentation / historical evidence |
| [docs/codex/prompts/phase_17hl_two_layer_structured_output.md](../prompts/phase_17hl_two_layer_structured_output.md) | C2 | Documentation / historical evidence |
| [docs/codex/proposals/managed_prompt_4.patch](../proposals/managed_prompt_4.patch) | C2 | Inactive historical patch; preserve bytes; companion archive notice required |
| [docs/codex/proposals/phase_17hl_generation_instruction_clarifications.md](../proposals/phase_17hl_generation_instruction_clarifications.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17h_live_preflight.md](phase_17h_live_preflight.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_ast_test_portability_fix.md](phase_17hl_ast_test_portability_fix.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_attempt5_final_readiness_and_operator_preparation.md](phase_17hl_attempt5_final_readiness_and_operator_preparation.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_attempt5_live_execution_report.md](phase_17hl_attempt5_live_execution_report.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_attempt5_operator_authorization_and_single_call_execution.md](phase_17hl_attempt5_operator_authorization_and_single_call_execution.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_attempt5_operator_checklist_verification.md](phase_17hl_attempt5_operator_checklist_verification.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_attempt5_post_execution_diagnostics.md](phase_17hl_attempt5_post_execution_diagnostics.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_attempt5_readiness_authorization_assessment.md](phase_17hl_attempt5_readiness_authorization_assessment.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_attempt6_offline_integration_readiness.md](phase_17hl_attempt6_offline_integration_readiness.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_azure_strict_schema_live_compatibility.md](phase_17hl_azure_strict_schema_live_compatibility.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_diagnostic_hardening.md](phase_17hl_diagnostic_hardening.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_documentation_remediation_and_readme_sync.md](phase_17hl_documentation_remediation_and_readme_sync.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_entra_v2_report.md](phase_17hl_entra_v2_report.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_evaluation_activation_readiness.md](phase_17hl_evaluation_activation_readiness.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_evaluation_policy_activation.md](phase_17hl_evaluation_policy_activation.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_f1_http_cleanup_failure_preservation.md](phase_17hl_f1_http_cleanup_failure_preservation.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_final_offline_azure_compatibility_audit.md](phase_17hl_final_offline_azure_compatibility_audit.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_final_operator_authorization.md](phase_17hl_final_operator_authorization.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_first_failure_diagnosis.md](phase_17hl_first_failure_diagnosis.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_full_suite_configuration_isolation.md](phase_17hl_full_suite_configuration_isolation.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_independent_json_byte_limits.md](phase_17hl_independent_json_byte_limits.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_l1_attempt3_preparation.md](phase_17hl_l1_attempt3_preparation.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_l1_attempt3_serialization_root_cause.md](phase_17hl_l1_attempt3_serialization_root_cause.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_launch_authorization_final.md](phase_17hl_launch_authorization_final.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_live_execution_preparation.md](phase_17hl_live_execution_preparation.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_live_failure_observability_and_contract_options.md](phase_17hl_live_failure_observability_and_contract_options.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_managed_prompt4_subject_contract_implementation.md](phase_17hl_managed_prompt4_subject_contract_implementation.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_offline_e2e_contract_verification.md](phase_17hl_offline_e2e_contract_verification.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_operator_approval_report.md](phase_17hl_operator_approval_report.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_output_limit_hardening.md](phase_17hl_output_limit_hardening.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_preflight_observability_timing_hardening.md](phase_17hl_preflight_observability_timing_hardening.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_regression_reconciliation.md](phase_17hl_regression_reconciliation.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_reusable_evaluation_governance.md](phase_17hl_reusable_evaluation_governance.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_same_day_attempt2_handoff.md](phase_17hl_same_day_attempt2_handoff.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_second_attempt_preparation.md](phase_17hl_second_attempt_preparation.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_single_call_execution_failure_diagnosis.md](phase_17hl_single_call_execution_failure_diagnosis.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_single_call_harness_offline.md](phase_17hl_single_call_harness_offline.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_structured_output_compatibility.md](phase_17hl_structured_output_compatibility.md) | C2 | Documentation / historical evidence |
| [docs/codex/reports/phase_17hl_two_layer_structured_output.md](phase_17hl_two_layer_structured_output.md) | C2 | Documentation / historical evidence |
| [docs/engineering/llm_structured_output_validation.md](../../engineering/llm_structured_output_validation.md) | C2 | Documentation / historical evidence |
| [docs/engineering/postmortems/Estudio_PolyMind_Phase17HL_L1_Three_Attempts_Postmortem_2026-10-16.md](../../engineering/postmortems/Estudio_PolyMind_Phase17HL_L1_Three_Attempts_Postmortem_2026-10-16.md) | C2 | Documentation / historical evidence |
| [docs/evaluation/phase_17h.md](../../evaluation/phase_17h.md) | C2 | Documentation / historical evidence |
| [docs/evaluation/phase_17h_foundry_approval.template.json](../../evaluation/phase_17h_foundry_approval.template.json) | C2 | Non-deployable historical/synthetic documentation template; unchanged |
| [docs/evaluation/phase_17h_foundry_validation.md](../../evaluation/phase_17h_foundry_validation.md) | C2 | Documentation / historical evidence |
| [docs/evaluation/phase_17hl_operator_approval.md](../../evaluation/phase_17hl_operator_approval.md) | C2 | Documentation / historical evidence |
| [docs/governance/evaluation-binding.template.json](../../governance/evaluation-binding.template.json) | C2 | Non-deployable historical/synthetic documentation template; unchanged |
| [docs/governance/evaluation-policy.md](../../governance/evaluation-policy.md) | C2 | Documentation / historical evidence |
| [docs/security/entra_v2.md](../../security/entra_v2.md) | C2 | Documentation / historical evidence |
| [docs/security/phase_17g.md](../../security/phase_17g.md) | C2 | Documentation / historical evidence |
| [docs/security/production-security.md](../../security/production-security.md) | C2 | Documentation / historical evidence |
| [docs/security/threat-model.md](../../security/threat-model.md) | C2 | Documentation / historical evidence |
| [documents/digestion/codec.py](../../../documents/digestion/codec.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [documents/digestion/diagnostics.py](../../../documents/digestion/diagnostics.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [documents/digestion/managed.py](../../../documents/digestion/managed.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [documents/digestion/models.py](../../../documents/digestion/models.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [documents/digestion/validation.py](../../../documents/digestion/validation.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [documents/publication/analysis.py](../../../documents/publication/analysis.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [governance/evaluation.py](../../../governance/evaluation.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [governance/execution.py](../../../governance/execution.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [governance/ledger.py](../../../governance/ledger.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [governance/migration.py](../../../governance/migration.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [llm/azure_schema.py](../../../llm/azure_schema.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [llm/bounded_http.py](../../../llm/bounded_http.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [llm/inference.py](../../../llm/inference.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [llm/ollama_client.py](../../../llm/ollama_client.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [llm/openai_compatible.py](../../../llm/openai_compatible.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [llm/structured.py](../../../llm/structured.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [security/identity.py](../../../security/identity.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [security/runtime.py](../../../security/runtime.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/README.md](../../../tests/README.md) | C2 | Documentation / historical evidence |
| [tests/approval_helpers.py](../../../tests/approval_helpers.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/conftest.py](../../../tests/conftest.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/fixtures/digestion_contracts/README.md](../../../tests/fixtures/digestion_contracts/README.md) | C2 | Documentation / historical evidence |
| [tests/fixtures/digestion_contracts/managed_prompt3.py.txt](../../../tests/fixtures/digestion_contracts/managed_prompt3.py.txt) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/fixtures/digestion_contracts/managed_prompt4.json](../../../tests/fixtures/digestion_contracts/managed_prompt4.json) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/fixtures/digestion_contracts/managed_prompt4_subject.txt](../../../tests/fixtures/digestion_contracts/managed_prompt4_subject.txt) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/fixtures/digestion_contracts/models.py.txt](../../../tests/fixtures/digestion_contracts/models.py.txt) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/fixtures/digestion_contracts/validation.py.txt](../../../tests/fixtures/digestion_contracts/validation.py.txt) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/integration/test_attempt3_serialization.py](../../../tests/integration/test_attempt3_serialization.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/integration/test_final_offline_azure_compatibility.py](../../../tests/integration/test_final_offline_azure_compatibility.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/integration/test_foundry_l1_entra.py](../../../tests/integration/test_foundry_l1_entra.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/integration/test_foundry_l1_launcher.py](../../../tests/integration/test_foundry_l1_launcher.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/integration/test_foundry_offline_workflow.py](../../../tests/integration/test_foundry_offline_workflow.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/integration/test_http_cleanup_governance.py](../../../tests/integration/test_http_cleanup_governance.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/integration/test_live_failure_observability.py](../../../tests/integration/test_live_failure_observability.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/integration/test_managed_digestion.py](../../../tests/integration/test_managed_digestion.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/integration/test_output_limit_hardening.py](../../../tests/integration/test_output_limit_hardening.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/integration/test_phase17hl_offline_e2e.py](../../../tests/integration/test_phase17hl_offline_e2e.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/integration/test_single_call_harness.py](../../../tests/integration/test_single_call_harness.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/integration/test_single_call_preflight.py](../../../tests/integration/test_single_call_preflight.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/integration/test_validation_diagnostics.py](../../../tests/integration/test_validation_diagnostics.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/performance/foundry_approval.py](../../../tests/performance/foundry_approval.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/performance/foundry_budget.py](../../../tests/performance/foundry_budget.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/performance/foundry_envelopes.py](../../../tests/performance/foundry_envelopes.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/performance/foundry_l1.py](../../../tests/performance/foundry_l1.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/performance/foundry_preflight.py](../../../tests/performance/foundry_preflight.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/performance/foundry_recalibration.py](../../../tests/performance/foundry_recalibration.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/performance/foundry_schema_diagnostics.py](../../../tests/performance/foundry_schema_diagnostics.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/performance/foundry_schema_probe.py](../../../tests/performance/foundry_schema_probe.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/performance/foundry_single_call.py](../../../tests/performance/foundry_single_call.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/settings_isolation.py](../../../tests/settings_isolation.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/source_contracts.py](../../../tests/source_contracts.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/documents/test_independent_json_limits.py](../../../tests/unit/documents/test_independent_json_limits.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/documents/test_managed_inference.py](../../../tests/unit/documents/test_managed_inference.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/documents/test_output_limit_sizes.py](../../../tests/unit/documents/test_output_limit_sizes.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/documents/test_strict_schema_compatibility.py](../../../tests/unit/documents/test_strict_schema_compatibility.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/documents/test_two_layer_output.py](../../../tests/unit/documents/test_two_layer_output.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/publication/test_analysis.py](../../../tests/unit/publication/test_analysis.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/test_evaluation_activation.py](../../../tests/unit/test_evaluation_activation.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/test_evaluation_governance.py](../../../tests/unit/test_evaluation_governance.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/test_foundry_30k.py](../../../tests/unit/test_foundry_30k.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/test_foundry_approval.py](../../../tests/unit/test_foundry_approval.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/test_foundry_preflight.py](../../../tests/unit/test_foundry_preflight.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/test_foundry_schema_probe.py](../../../tests/unit/test_foundry_schema_probe.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/test_governance_migration.py](../../../tests/unit/test_governance_migration.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/test_http_cleanup.py](../../../tests/unit/test_http_cleanup.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/test_output_limit_diagnostics.py](../../../tests/unit/test_output_limit_diagnostics.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/test_security_entra.py](../../../tests/unit/test_security_entra.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/test_settings_isolation.py](../../../tests/unit/test_settings_isolation.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/test_single_call_diagnostics.py](../../../tests/unit/test_single_call_diagnostics.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/test_source_contracts.py](../../../tests/unit/test_source_contracts.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |
| [tests/unit/test_structured_provider.py](../../../tests/unit/test_structured_provider.py) | C1 | Coupled engineering source/test/contract fixture; preserve original membership |

## 16. Remaining limitations and non-blocking recommendations

No documentation publication blocker remains. Operator engineering review should
consider the existing lint findings and the scope/date of regression evidence,
then stage C1/C2 manually using the exact inventory. This task changes no test
requirement or acceptance policy. Local static scans do not certify all past
history, ignored private storage, cloud billing or live reliability.

The next evaluation milestone remains separately reviewed full live L1 hierarchy,
publication/retrieval and grounded Q&A with independent claim/citation assessment.
Representative documents and workload reliability remain needed for broader 17H.
No configuration, approval, signature, reservation, execution window or further
provider call is prepared or authorized by this documentation work.

## 17. Final project phase status

| Scope | Current status |
|---|---|
| Phase 17G | COMPLETED/PASS within accepted single-host/reference scope |
| Phase 17H | PARTIAL |
| Scoped offline diagnostic hardening | COMPLETE |
| managed-prompt/4 implementation | PASS within tested scope; active |
| Azure Foundry Attempt 6 | CLOSED/PASS |
| Full live L1 hierarchical workflow | NOT VALIDATED |
| Grounded Q&A after full live digestion | NOT VALIDATED |
| Phase 17I | PLANNED, subject to established approval gates |
| Independent 17J–17L definitions/completion | Not established by authoritative evidence; no completion inferred |
| Production readiness | NOT ESTABLISHED |

## 18. Final Git inventory and safety attestation

Final file-level status is **25 modified tracked + 131 untracked = 156 pending
files**, with **0 staged files**. This reconciles the initial 149: five previously
clean tracked documentation files become pending, and two new Markdown artifacts
are added. All 149 original pending paths remain. The index entries, branch and
HEAD are unchanged. The exact final pending manifest is section 15.

Executed `git status --porcelain=v1 --untracked-files=all`, `git diff --stat`,
`git diff --check`, index/HEAD/branch comparisons, baseline SHA-256 comparisons,
untracked whitespace, local Markdown link/fragment checks, publication scanning,
and the independent historical/source preservation checks described above.

Final `git diff --stat` (tracked changes only, including pre-existing engineering):

```text
.env.example                                   |   5 +
 README.md                                      |  66 ++++++++--
 deployment/helm/polymind/README.md             |  12 +-
 docs/evaluation/phase_17h.md                   |   7 ++
 docs/security/phase_17g.md                     |  15 ++-
 docs/security/production-security.md           |  16 ++-
 docs/security/threat-model.md                  |  11 ++
 documents/digestion/codec.py                   |  52 +++++++-
 documents/digestion/managed.py                 |  76 ++++++++++--
 documents/digestion/models.py                  |  41 +++++-
 documents/digestion/validation.py              | 165 +++++++++++++++++++++----
 documents/publication/analysis.py              |   7 +-
 governance/execution.py                        |  28 ++++-
 governance/ledger.py                           |  74 ++++++++++-
 llm/bounded_http.py                            |  75 +++++++++--
 llm/inference.py                               |  18 +++
 llm/ollama_client.py                           |  16 ++-
 llm/openai_compatible.py                       |  95 ++++++++++++--
 llm/structured.py                              |  82 +++++++++++-
 security/identity.py                           |  61 ++++++++-
 security/runtime.py                            |   5 +-
 tests/integration/test_managed_digestion.py    |  10 ++
 tests/unit/documents/test_managed_inference.py | 117 ++++++++++++++++++
 tests/unit/publication/test_analysis.py        |   3 +
 tests/unit/test_structured_provider.py         |  43 +++++++
 25 files changed, 1001 insertions(+), 99 deletions(-)
```

That statistic excludes the 131 untracked files; neither it nor the 38-file task
delta replaces the complete 156-file commit classification.

| Safety counter | This task |
|---|---:|
| Staged files | 0 |
| Commits created / pushes | 0 / 0 |
| Branch switches / resets / restores / stashes / merges / rebases | 0 |
| Azure inference / cloud operations | 0 / 0 |
| Financial reservations, settlement or policy mutations | 0 |
| Signing / approval verification or consumption operations | 0 |
| Unexpected source/test/fixture/runtime configuration modifications | 0 |
| Protected private artifact operations | 0 |

**No commit or push occurred.** All changes remain unstaged for the operator's
manual review. Documentation acceptance is PASS; it does not close Phase 17H or
authorize any next execution phase.
