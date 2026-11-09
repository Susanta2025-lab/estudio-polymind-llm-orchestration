# Phase 17H v7 claim-identity hardening and offline readiness

User task recorded 9 November 2026. This normalized task record authorizes only
offline implementation and validation; it grants no signing or live authority.

## Starting evidence and implementation

Read `AGENTS.md` and the v6 checkpoint/identity/readiness report, v5 reducer-sizing
reconciliation and v5 execution-window/RSA report. Verify `master` at reviewed
checkpoint `bdd7ab3039fbd9707c10d40a132007598a1921cb`, template
`managed-prompt/6` and generation SHA-256
`f6e568d450ac084c5977e4fef68823fb457cceacd22b361f047310c5d3512f5b`.
Inspect actual changes and the four existing investigation files, including all
34 identity regressions. Preserve unrelated work and completed engineering.

The historical first reducer emitted eight correct positional claim IDs with
the immediate child's stage UUID as every origin. G2 correctly rejected them.
The strongest explanation is current-generation/inherited-origin confusion;
prompt ambiguity is a hypothesis, not a proven validator defect.

Implement only the following explicit clarification under `managed-prompt/7`,
adapting only to actual prompt structure:

> Use CONTROL.claim_ids_in_order consecutively for this response. Set the result
> stage_id and every claims[i].originating_stage to the current CONTROL.stage_id,
> including claims that restate child findings. Copy source-stage identities only
> into lineage using CONTROL.required_child_links; never copy a child's
> originating_stage into a new claim.

Verify all four profiles, schemas, request construction and production validators.
Keep claim origins equal to the current request UUID, positional IDs generated
by the existing stable-ID algorithm, child identities in validated lineage and
original evidence IDs separate. No automatic response repair, substituted IDs,
G2 weakening, schema-semantic changes, new inference calls, retries or fallback.

## Compatibility, sizing and regression requirements

Recompute the complete production source-inventory digest; never reuse v6's
fingerprint. Prove the exact intended prompt difference and unchanged schema,
identity algorithm, G1/G2, response limits, 7,000-byte child limit, provider-neutral
interface and financial/governance contracts. Freeze v7 requests/generation/HTTP
payloads, preserve v5/v6 fingerprints and prove old configuration and checkpoint
bindings cannot execute under v7. Consumed approvals remain unusable.

Measure actual production serialization for chunk, intermediate, structural and
root generation, one/two-child reducers, structural paths and escaped/Unicode
source/child material. The preliminary 263-byte increase and 24,236-byte two-child
bound need verification against 24,800 input and the complete 28,000 context
reservation. Never expand limits to fit wording; minimize safely or report BLOCKED.

Retain the existing 34 identity cases and add only needed prompt-role, compatibility
and sizing coverage. Cover valid origins, all-eight and mixed wrong origins,
correct IDs/valid evidence with invalid identity, restated inherited claims,
lineage, qualifications/conflicts, rejection before commit, NON_RETRYABLE failure,
preserved settlements/checkpoints and no publication/Q&A after invalid digestion.
Use production renderer/validator and synthetic fixtures, with no private output.

Revalidate chunk, structural reducer, root and Q&A plus digest, publication,
retrieval, citation grounding and durable recovery. Preserve malformed identity,
fabricated evidence, invalid citation and oversized-material refusals. Exercise
legitimate 6,999/7,000/7,001-byte boundaries without loosening assertions.

Run focused identity, sizing, G1/G2, compatibility, full four-call and complete
offline pytest suites, Ruff, mypy, external-cache compilation, Compose validation
and whitespace checks. Keep network-disabled safeguards and report exact counts,
warnings and genuine failures. No unnecessary installs, builds or cluster work.

## Report, readiness and strict boundaries

Create the matching permanent report with starting state, historical failure and
uncertainty, exact correction, file/function manifest, v6/v7 comparison, new digest,
actual measurements, regression/E2E/full validation evidence, compatibility,
security, residual model/semantic risks, future operator prerequisites and ending
Git state. Update current README/runbook where needed; preserve dated reports.
Perform implementation self-review and a separate pre-commit/security review.

Assess generation, identity, G2, sizing, durability, synthetic workflow,
publication/Q&A, historical compatibility, unchanged financial governance,
operator authority, real-model behavior and semantic quality separately. Offline
success permits a separate operator-preparation review only. Fresh authentication,
configuration, window/consumer attestations, new RSA authorization and separate
paid approval remain required; the prior approval is consumed. Stronger guidance
reduces ambiguity but cannot guarantee compliance or complete Phase 17H.

No Git staging, commit, push, amend, reset, rebase, branch/tag mutation or history
rewrite. All work remains unstaged/uncommitted. No paid inference, Azure/Entra
authentication, inference-key retrieval, live configuration, operator signature,
approval consumption, live authority/store/private-package mutation or historical
settlement alteration. Do not undo the existing v6 commit.

Return PASS — V7 CLAIM-IDENTITY HARDENING COMPLETE; OFFLINE READINESS VERIFIED
only after all required checks pass; otherwise BLOCKED — V7 CONTRACT OR
VALIDATION ISSUE with the exact blocker. End with explicit NO confirmations for
Git staging/commit/push, paid Azure inference and RSA signing.
