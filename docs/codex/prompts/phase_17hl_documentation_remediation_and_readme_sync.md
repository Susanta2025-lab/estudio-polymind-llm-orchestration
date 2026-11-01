# Phase 17H–L — publication remediation and README synchronization

Date: 1 November 2026. Normalized operator task, preserved under AGENTS.md's
major-phase documentation convention. This record preserves the requirements;
it grants no future live authorization.

## Objective and boundary

On the existing `master` branch, resolve the twelve publication findings from the
commit-readiness audit, review every Git-visible README, synchronize relevant
current documentation with the verified Phase 17H–L state and Attempt 6 closure,
and create a permanent implementation report. Inventory tracked and untracked
pending files individually. All staging, commits and pushes belong to a subsequent
manual operator task.

Only documentation review, Markdown edits, historical sanitization, archival
notices, link checking and static verification are authorized. Preserve all
pre-existing source and uncommitted work. Do not change production Python, tests,
frozen fixtures, managed-prompt/4 behavior, generation/validation contracts,
fingerprints, active security/governance policy, runtime configuration or
`.gitignore`. Do not apply historical proposal patches. Do not read credentials,
approval JWT contents, private keys, raw provider responses or protected private
operator artifacts. No cloud authentication/resource operation, Azure inference,
financial mutation, signing or approval consumption is authorized. No Git index,
history, branch or remote mutation is authorized.

## Preparation and authoritative evidence

Read AGENTS.md, actual branch/HEAD/status, README.md, the Phase 17G and Phase 17H
reports, all twelve flagged artifacts, README inventory and documentation/link
conventions before editing. Required later evidence:

- [Attempt 6 closure and phase assessment](../reports/phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md).
- [managed-prompt/4 implementation](../reports/phase_17hl_managed_prompt4_subject_contract_implementation.md).
- [Attempt 6 offline integration readiness](../reports/phase_17hl_attempt6_offline_integration_readiness.md).

The supplied historical baseline was master at
`af4a7a076c918ef13aea05d74bf239c0af909133`, with 20 modified tracked files,
129 untracked files, zero staged files and 894 insertions/81 deletions. Verify
actual state independently, record all pending paths and pre-existing hashes,
identify intended edits, and hash the archived patch before changes.

## Twelve original findings

Sanitize actual subscription/tenant/resource identifiers in
`phase_17hl_attempt5_operator_authorization_and_single_call_execution.md` under
both `docs/codex/prompts/` and `docs/codex/reports/`. Sanitize the public-client
identifier in report `phase_17hl_attempt5_live_execution_report.md`, and API scope
identifiers in reports `phase_17hl_final_operator_authorization.md` and
`phase_17hl_launch_authorization_final.md`. Use descriptive placeholders such as
`<AZURE_SUBSCRIPTION_ID>`, `<AZURE_TENANT_ID>`, `<FOUNDRY_RESOURCE_NAME>`,
`<ENTRA_PUBLIC_CLIENT_ID>` and `api://<ENTRA_API_CLIENT_ID>/access_as_user`.
Preserve authorization semantics, historical dates, decisions, measurements,
fingerprints, diagnoses and conclusions. Do not sanitize unrelated source
allowlists or protected configurations. Never publish the removed values.

Sanitize machine-specific interpreter paths, home paths and private audit paths in these reports:

- `phase_17hl_ast_test_portability_fix.md`.
- `phase_17hl_attempt5_final_readiness_and_operator_preparation.md`.
- `phase_17hl_f1_http_cleanup_failure_preservation.md`.
- `phase_17hl_live_execution_preparation.md`.
- `phase_17hl_single_call_execution_failure_diagnosis.md`.

Use portable/symbolic locations, explain how any suggested shell variables are
defined, preserve historical command purpose/provenance, and avoid turning old
commands into current executable live instructions.

Review `docs/codex/proposals/managed_prompt_4.patch` and its companion
`phase_17hl_generation_instruction_clarifications.md`. The patch MUST remain
byte-for-byte unchanged: no apply, regenerate, reformat, rename, move or delete.
Add a visible dated archival notice to the companion: the broader qualification
and unavailable-analysis proposal is inactive and was not automatically deployed;
active v4 is the separately validated, narrower subject-contract correction.
Link the authoritative implementation and Attempt 6 closure reports. Preserve
the original proposal's chronology and content. Record matching before/after
patch SHA-256 values in the implementation report.

## README and operational documentation review

Discover every Git-visible README, tracked or untracked. Record each path,
audience/purpose, affected content, review/update decision and validation result.
Do not change unaffected READMEs just for wording consistency.

Prioritize the root README: retain readable architecture/capability descriptions
for FastAPI, Streamlit, LangGraph, provider-neutral Ollama/OpenAI-compatible/Foundry
inference, RAG, extraction, hierarchical digestion, grounded claims, citations,
provenance, multi-user authorization, SecurityAuthority, quota and cost governance,
strict output validation and offline/live boundaries. Distinguish implemented
reference foundations from deployed production capability. Prefer a concise
status table with links to 17G acceptance, 17H evaluation, v4 implementation,
Attempt 6 closure and relevant security/evaluation runbooks.

Review test READMEs, including `tests/README.md` and the digestion-contract README.
Distinguish offline units, offline integration, synthetic Foundry harnesses,
historical frozen v3 contracts, active v4 witnesses and separately authorized
live Azure execution. Explain source contracts, strict JSON Schema versus domain
acceptance, settings isolation versus network denial, synthetic governance and
RSA/approval fixtures, and live-capable harness restrictions. Publish commands
only after static verification against the repository. Do not suggest live mode
for regression or provide ordinary test examples that trigger paid inference.

Review security/governance/evaluation documentation, particularly
`docs/security/phase_17g.md`, `docs/security/entra_v2.md`,
`docs/governance/evaluation-policy.md`, `docs/evaluation/phase_17h_foundry_validation.md`
and `docs/evaluation/phase_17hl_operator_approval.md`. Verify generic OIDC versus
explicit Entra v2 issuer/audience/scope/role checks, authority isolation, separate
RSA approval, exact digest binding, consumption/replay protection, execution
windows/cutoff, attested API-key use deadlines, RPM/TPM, reservations/settlement,
UNKNOWN accounting and zero automatic paid retries. Preserve authorization gates.

Search Git-visible Markdown for misleading current claims. Classify findings as
HISTORICALLY CORRECT, CURRENT AND CORRECT, CURRENT BUT OUTDATED, AMBIGUOUS or
UNVERIFIED. Preserve dated historical observations; use small dated status notes
for ambiguous legacy runbooks, with closure links. Avoid rewriting archival
reports merely because later events happened.

## Required historical and phase accuracy

Preserve Attempts 1–6: canonical serialization exceeded the byte ceiling (1);
output-limit failure was masked by governance handling, original trigger unknown
(2); malformed evidence UUID plus eight extra fields (3); completed strict output
failed application validation, exact predicate unknown (4); `subject_on_nonfact`
confirmed the v3 instruction/validator gap (5); active v4 produced one accepted,
financially settled live analysis (6). Keep the separate non-billable preflight
failure distinct. Never invent missing measurements or diagnoses.

Attempt 6 retained measurements are SUCCEEDED, one call, application accepted,
accounting_failed=false, SETTLED, 2476 input/1814 output/4290 total tokens and
EUR 0.008817317845829546 catalog-accounted cost. Local catalog accounting is not
an independently verified Azure invoice.

Current statuses: 17G COMPLETED/PASS in reference scope; 17H PARTIAL; scoped offline
diagnostic hardening COMPLETE; managed-prompt/4 PASS within tested scope; Attempt 6
CLOSED/PASS; full live L1 and subsequent grounded Q&A NOT VALIDATED; 17I PLANNED
subject to established gates; no unsupported independent 17J–17L completion or
definition inferred; production readiness NOT ESTABLISHED. Remaining 17H gates
include accepted first/second-root reductions, complete digest, publication and
retrieval, grounded Q&A, independent quality review, representative documents and
workload reliability.

## Verification and required deliverable

Scan Git-visible pending documentation and modified READMEs offline for actual
environment IDs, credentials, JWT/private-key material, personal/private paths,
private scopes, raw response content, runtime artifacts, bad links and misleading
operational instructions. Never scan ignored protected directories or print
confidential values. Distinguish public deployment names and synthetic fixtures
from private identifiers. Fix additional documentation publication issues within
scope; report restricted-file blockers without changing those files.

Execute `git diff --check`, separate untracked whitespace checks, relative file
and fragment link validation, original-finding rechecks, patch hash comparison,
source/test/fixture/runtime preservation checks, historical numeric/fingerprint
preservation checks, branch/HEAD/index preservation and complete final inventory
reconciliation. Documentation-only verification is sufficient; no live inference
or unrelated application test suite is authorized.

Create [the required implementation report](../reports/phase_17hl_documentation_remediation_and_readme_sync.md)
with executive verdict, restrictions, initial Git state, twelve resolutions,
all README dispositions, root/test/security/governance/evaluation changes, archive
clarification, scan/link results, evidence preservation, exact changed-file manifest,
updated C1/C2 readiness, remaining concerns, phase status and Git/safety attestation.

Classify EVERY pending file as C1 engineering, C2 documentation/historical
evidence, HOLD requiring resolution, or EXCLUDE with justification. Preserve the
original 69-file engineering membership unless evidence requires otherwise;
reconcile the original 80-file documentation group with all new edits/additions.
Do not split coupled runtime modules into incomplete commits. Mark documentation
READY, CONDITIONALLY READY or BLOCKED with evidence. No file may be omitted.

The final response must report PASS/PARTIAL/BLOCKED/FAIL; 12 original findings and
resolved/blocker counts; README review/update paths; additional documentation
paths; patch/link/security/fingerprint results; exact C1/C2/HOLD counts/readiness;
required report path; zero staging/commits/pushes/cloud calls/financial mutations/
approval-signing operations/unexpected source changes; and concise next steps.
PASS requires all acceptance conditions above; otherwise state the concrete gap.
