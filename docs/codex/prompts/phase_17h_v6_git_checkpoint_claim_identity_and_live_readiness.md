# Phase 17H v6 checkpoint, claim identity and live-readiness task

User task recorded 9 November 2026. This normalized task record preserves the
authorized scope; it grants no signing or paid execution authority.

## Sequential objectives

1. Independently inspect the v6 sizing implementation, all changes and eight new
   files, tests, historical compatibility and sensitive-content boundaries.
   Verify `master` at `2b8a5ac73beb32d7febc53f77d0c3a459c8e3394`, the actual
   file manifest and current generation-contract digest. Read the v5 reducer-sizing
   reconciliation and execution-window/RSA reports. Confirm the original
   7,271-byte rejection has permanent coverage, the actual 7,000-byte child limit
   remains enforced before checkpoint commit and during finalization, and G1/G2,
   source evidence, qualifications, contradictions and lineage remain strict.
2. Run applicable regressions and quality checks, preferably the complete offline
   suite. Stage only the reviewed 16 tracked changes and eight task additions,
   inspect the staged manifest/diff and run `git diff --cached --check`.
   Create exactly one local commit, suggested message
   `fix(digestion): reconcile reducer child sizing and preserve v6 contracts`.
   Preserve the 19 unrelated untracked Markdown files. Do not use broad staging,
   amend, rewrite history or push. Stop checkpointing for material discrepancies.
3. Only after preserving that checkpoint, investigate historical
   `originating_stage_mismatch` entirely offline. Establish exact stage UUID and
   positional claim-ID rules for chunk, intermediate, structural and root
   synthesis, how prompts/schema communicate them, and whether the evidence
   supports ambiguity, construction inconsistency or model noncompliance.
   Distinguish demonstrated facts from causal hypotheses. The eight rejected
   historical claims remain invalid; never repair or fabricate provider output.
4. Add deterministic synthetic/sanitized regressions using production validation.
   Cover valid and invalid stage identities, mixed results, correct claim IDs
   with wrong stages, inherited versus new identity, valid evidence with invalid
   identity, qualification/conflict propagation, rejection before checkpoint
   commit, preserved prior checkpoints/settled usage and no invalid publication.
   Run relevant unit/integration, compatibility, G2, Ruff and mypy checks.
   Leave all investigation changes uncommitted.
5. Assess fresh engineering readiness of the four-call workflow, strict sizing
   and provenance, checkpoint/recovery/finalization, publication/Q&A,
   provider-neutral boundaries, zero retry and no fallback. Explicitly assess
   the unresolved historical eight-claim failure under unchanged v6 wording.
   Recommend the smallest generation correction if warranted, with compatibility
   impact, before implementation. Never silently change `managed-prompt/6`;
   changed generation behavior requires a new identity and digest.
6. Review preserved operator evidence and authorized local non-billable checks:
   Azure target/model, November catalog, EUR 0.242439068181288 allowance and EUR 5
   ceiling, tokens/concurrency, governance/admission, independent RSA trust,
   replay, operator permissions, consumer exclusions, credentials and window.
   Label old observations with their actual timestamps. The consumed approval
   cannot be reused. Future execution requires a new validated configuration,
   new RSA authorization and separate paid authorization.

Expected template: `managed-prompt/6`. Expected generation-contract SHA-256:
`f6e568d450ac084c5977e4fef68823fb457cceacd22b361f047310c5d3512f5b`.

## Deliverable and boundaries

Create the corresponding report with the reviewed manifest, commit SHA,
starting/ending Git status, digest, identity findings and exact rules,
prompt/validator consistency, regression/quality evidence, separately recorded
generation proposal, compatibility/security implications, readiness conclusions,
risks and operator prerequisites. Report separate engineering, acceptance-risk,
generation, financial/governance, authorization and future-evaluation conclusions.

No paid inference or external LLM; no Entra login or inference-key retrieval;
no operator RSA signing or approval consumption; no authority mutation,
settlement alteration, replay reset, automatic identity repair, G1/G2 weakening,
unrelated staging, second commit or push. Store no private response text,
identity values, credentials or signing keys in Git. Read-only local evidence is
permitted; stale observations must never imply current authentication or quota.

Use one final classification: PASS — V6 CHECKPOINTED; TECHNICAL LIVE READINESS
ACCEPTABLE; CONDITIONAL — V6 CHECKPOINTED; CLAIM-IDENTITY RISK REQUIRES REVIEW;
NO-GO — CLAIM-IDENTITY CONTRACT CORRECTION REQUIRED; or BLOCKED — CHECKPOINT OR
VALIDATION FAILED. None authorizes signing or paid inference.
