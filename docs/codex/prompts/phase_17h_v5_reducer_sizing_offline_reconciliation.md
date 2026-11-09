# Phase 17H v5 reducer sizing: offline diagnosis, correction and validation

User task recorded 9 November 2026. This is a normalized engineering record of
the supplied task; it grants no future live authorization.

## Objective and starting evidence

Investigate the reproducible first-reducer failure after the second authorized
v5 evaluation. Expected starting HEAD is
`2b8a5ac73beb32d7febc53f77d0c3a459c8e3394`. Read
`docs/codex/reports/phase_17h_v5_execution_window_renewal_and_rsa_authorization.md`
and inspect implementation, planning, sizing, validation, worker and tests before
editing. Inspect Git and preserve unrelated work.

The historical evaluation made two successful provider calls. Chunk analysis
committed a validated checkpoint. The first reducer failed application validation;
root reduction, publication and Q&A were not executed. Failure was
`extraction_limit_exceeded` / `synthesis_limit_exceeded` / diagnostic
`response_limit`, with a NON_RETRYABLE attempt. Raw and canonical reducer response
were each 4,783 bytes, below independent 10,000-byte limits. Escaped child material
plus the 1,024-byte reserved wrapper was 7,271 bytes, exceeding the 7,000-byte
budget by 271. First-reducer estimated input was 16,007 tokens with 3,000 output
reserved. Its consumed approval must never be reused.

## Required investigation and correction

Start by reproducing 7,271 bytes deterministically, without an LLM. Establish
result construction, both JSON escaping layers, UTF-8 byte counts, wrapper
reservation, stage limits, planner/runtime representations and downstream
material, including evidence and qualification lineage. Distinguish deliberate
fail-closed rejection from an engineering inconsistency. Explain whether the
planner can predict or prevent the incompatibility and why prior tests missed it.
Do not implement before understanding the discrepancy.

Select the smallest defensible correction. Preserve G1 sizing, G2 provenance,
source IDs, qualifications, contradictions, deterministic hierarchy/planning,
provider independence and durable checkpoints/recovery. Reconcile inconsistent
contracts or use bounded deterministic validation for valid outputs. Never
silently truncate, discard, repair, rewrite or invent evidence. No compression
call, extra paid stage, automatic retry, broad refactoring or new dependencies.
Do not raise 7,000 bytes without quantified downstream justification. If safe
correction requires a contract change that cannot be made within scope, preserve
rejection and report that requirement rather than weakening safeguards.

## Permanent regression and complete synthetic workflow

Use synthetic/sanitized tracked fixtures, never private live payloads. Exercise
production sizing functions for the original 7,271-byte witness; 6,999/7,000/7,001
bytes; escaping; Unicode/UTF-8; wrapper reservation; multiple children;
planner/runtime consistency; evidence IDs/source references/qualifications;
genuinely incompatible outputs; accounting and durable checkpoint behavior.

Revalidate the complete established L1 workflow offline: chunk analysis, first
reducer, root reducer, local completion/publication/retrieval, grounded Q&A.
Verify per-stage and next-stage material/input/output/context/token limits,
source lineage, contradictions/qualifications, no fabricated evidence, G1/G2,
checkpoint transitions, valid publication and source-grounded responses, and
invalid-fixture rejections. Run relevant unit/integration/offline end-to-end
checks, Ruff, mypy and applicable existing quality checks. Investigate failures;
do not weaken assertions. Synthetic success proves neither Azure output
acceptance nor semantic correctness or a guarantee of future success.

## Deliverable and boundaries

Create `docs/codex/reports/phase_17h_v5_reducer_sizing_offline_reconciliation.md`
with exact original evidence/calculations, root cause, planner/runtime comparison,
7,000-byte rationale, modified functions, chosen correction, permanent regression
coverage, complete offline workflow results, remaining failures, security and
provenance impact, generation/configuration compatibility, risks and verdict.
Report any changed prompt/schema/generation-source/compatibility digest and the
need for fresh configurations/approvals; never reuse an obsolete digest.

Offline only. No Azure inference, paid calls, Microsoft Entra authentication,
RSA signing, approval consumption, governance-authority mutation,
historical settlement/audit modification, Kubernetes/AKS/cloud changes, Git
staging, commits or pushes. Leave changes uncommitted for review.

Completion requires reproduced failure, established cause, justified correction
where appropriate, passing permanent tests and full synthetic L1 workflow, G1/G2
preservation, applicable quality checks, complete report and no live/financial
authority consumed. Final verdict must be either
`PASS — OFFLINE REDUCER SIZING RECONCILED` or
`BLOCKED — GENERATION OR SIZING CONTRACT CHANGE REQUIRED`.
A PASS is eligibility for a separate live-readiness review, not authorization
for paid evaluation or completion of Phase 17H. Final response should concisely
report cause, correction, files, test counts, digest change, risks, Git state and
verdict.
