# Phase 17H v8 — Hierarchical lineage hardening and offline readiness

Task received 9 November 2026. This clean engineering task record preserves the
supplied objective, required evidence, acceptance conditions and authority limits.
The original user prompt remains authoritative.

## Objective and starting checkpoint

Resolve the hierarchical claim-lineage risk from the latest v7 Azure Foundry
evaluation through offline engineering only. Expected branch `master`, HEAD
`6e0319e29984ad019edced0e076b3b0a4ae8c007`, generation `managed-prompt/7`, digest
`8426ab5cfef3e4d1925c68a5f8558c5bafc487dd746f0f7ccda799c03be16c3a`.
Follow AGENTS.md, inspect actual implementation/tests/consumers/configuration,
and read the v7 execution, v7 readiness, v6 checkpoint and current Foundry
evaluation runbook. Preserve unrelated untracked documents and private evidence.

The live evaluation made three successful provider calls. Chunk and first
reducer passed; root failed `evidence_validation_failed` / `evidence_validation`
/ `invalid_child_link`, mapped to `invalid_reference`, `NON_RETRYABLE`. Eight
root claims had correct current identities but combined the immediate reducer's
stage ID with chunk claim IDs. Publication and Q&A were not reached. All paid
calls were settled and the signed approval was consumed permanently.

## Required engineering activities

1. **Reconstruct first.** Disable network access; verify immutable sizes and
   hashes before inspecting accepted chunk/reducer checkpoints, deterministic
   root plan, actual StageRequest, full GenerationRequest and provider response.
   Use the production renderer and match the preserved live request SHA-256.
   Inspect CONTROL stage, positional claim IDs, allowed source evidence and
   required child links. Reproduce the exact strict G2 rejection without edits.
2. **Diagnose.** Compare authorized/observed pairs, establish grandchild identity
   reuse and cross-level pairing, distinguish observed noncompliance from prompt
   ambiguity hypotheses, and assess intermediate/structural/multi-child exposure.
   Do not claim knowledge of model reasoning or retrospectively repair output.
3. **Implement the smallest v8 correction.** Every generated direct lineage
   link must copy an exact `(stage_id, claim_id)` pair together from
   `CONTROL.required_child_links`, without modification or mixing hierarchy
   levels. Distinguish current result stage and new claim IDs, immediate child
   pairs, earlier/grandchild/ancestor identities, original source evidence and
   inherited qualifications/conflicts/provenance. Retain v7 identity rules and
   application-owned coverage/inheritance. Prefer only the shared managed prompt
   and necessary compatibility/tests; no schema or architecture redesign.
4. **Measure full envelopes.** Compute a new source-inventory generation digest.
   Keep `stage-result/1`, 24,800 managed input, 28,000 context, 7,000 complete child
   bytes, 10,000 raw/canonical digestion bytes, 3,000 output tokens, at most four
   L1 calls, zero automatic retries and no fallback. V7 fixed envelope was 10,236;
   two-child empty-path reservation 24,236, with only 564 bytes spare. Measure all
   four profiles, one/two children, paths, escaping and Unicode using production
   system/data/schema serialization and full context. Shorten instructions if
   needed; do not raise limits. BLOCK if no safe wording fits.
5. **Permanent regressions.** Use synthetic text/IDs and production renderer,
   codec and validators. Cover valid immediate-child links, eight mixed-level
   pairs, wrong claim/stage, cross-child mismatches, valid evidence/current IDs
   with invalid lineage, missing coverage, prohibited duplicates, inherited
   qualifications/contradictions and all profiles. Verify rejection before
   checkpoint commit, NON_RETRYABLE classification, preserved checkpoints and
   settled usage, and no publication/Q&A. Retain all 34 identity cases and
   historical v6/v7 sizing and exact 6,999/7,000/7,001-byte regressions.
6. **Complete offline workflow and compatibility.** Run chunk, first reducer,
   root and grounded Q&A with network disabled. Check digest completion, durable
   storage/recovery, publication/retrieval, source citations, all provenance and
   coverage, qualification/conflict inheritance, G1/G2, raw/canonical/child/input/
   context bounds, settlement and no repair. Reopening accepted checkpoints must
   not repeat provider calls. Preserve frozen v5/v6/v7 sources/fingerprints,
   create a frozen v8 fixture, prove exact prompt delta/schema invariance, reject
   stale configurations/checkpoint execution, and preserve consumed approvals,
   historical evidence/settlements and provider/security/governance interfaces.

Run targeted lineage, identity, G1/G2, sizing, historical and four-call tests;
then full offline pytest, Ruff, mypy, compilation, applicable Compose checks and
`git diff --check`. Investigate failures; do not weaken assertions, install
dependencies or rebuild unrelated infrastructure. Perform separate implementation
self-review and pre-commit/security review.

## Permanent report and readiness decision

Create `docs/codex/reports/phase_17h_v8_lineage_hardening_and_offline_readiness.md`
with sanitized reconstruction and pair comparisons, supported cause/uncertainty,
exact changes/functions, new digest, complete sizing and regression evidence,
workflow and historical compatibility results, G2 impact, remaining risks,
operator-preparation requirements, final Git status/file manifest and verdict.
Update README/current runbook only as necessary; preserve dated reports.

Offline correctness does not establish Azure compliance or independent semantic
quality. Assess eligibility only for a separate operator-preparation review.
Future inference needs a fresh v8 configuration, new RSA signing authorization
and separate paid-inference authorization. Never reuse the consumed approval.

## Mandatory boundaries and final response

Do not stage, commit, push, amend/rebase/reset, mutate branches/tags/history,
change remotes or GitHub state. No paid/external inference, Entra login,
resource-key retrieval, operator RSA signing, approval consumption, authority or
settlement modification, replay reset, Azure/AKS/Kubernetes mutation, automatic
retry, fallback, fabricated source links, identifier substitution, response
repair, evidence truncation or extra LLM calls is authorized.

Return `PASS — V8 LINEAGE HARDENING COMPLETE; OFFLINE READINESS VERIFIED` only
after reconstruction, narrow hardening, strict unchanged G2/current identity,
explicit hierarchy semantics, sizing, permanent regressions, full four-call
workflow, historical compatibility and applicable quality checks all pass.
Otherwise return `BLOCKED — V8 LINEAGE CONTRACT OR VALIDATION ISSUE` with the
exact unresolved issue and no weakened safeguards.

The final summary must include cause/evidence, correction, digest, file changes,
test counts/outcomes, sizing, G1/G2/historical preservation, live risks and
operator requirements, plus Git status. End with explicit NO confirmations for
Git staging, commit, push, Azure inference, RSA signing and approval consumption.
