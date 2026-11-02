# Phase 17H — Four-Call L1 Operator Preparation and Final Authorization Readiness

## Context and objective

Work in `Susanta2025-lab/estudio-polymind-llm-orchestration`. The supplied checkpoint
is `b15713e`, with passing GitHub Actions CI. G1/G2 engineering, historical contract
reconciliation and the four-call offline L1 workflow have been validated. Phase
17H remains PARTIAL. No new Azure live inference is authorized.

Review existing Phase 17H reports and operator runbooks first. Reuse validated
evidence. Prepare the existing four-call Azure Foundry L1 evaluation for final
operator review, resolve safe local prerequisites, and assess readiness for
independent approval. **Do not sign, authorize or execute the evaluation.**

## Tasks

1. Verify HEAD, working-tree status and successful CI checkpoint; active
   `managed-prompt/4`, corrected G1 sizing, strict source/evidence/application
   validation, exactly four calls (chunk, structural, root, grounded Q&A), zero
   retries and durable accounting. Change no application code unless a concrete
   blocking defect is discovered; report defects without silently expanding scope.
2. Find the previously packaged regular-file embedding model using existing
   local evidence. Required model: `sentence-transformers/all-MiniLM-L6-v2`;
   revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`; expected tree SHA-256
   `96ab3cd391276cb159904c4d329318ae1f3330278a7fc0450256233cf8bb78db`.
   If temporary, preserve locally verified files in a safe, dedicated, durable
   directory outside Git, without overwriting existing approved directories.
   Verify the exact 11-file inventory, zero symlinks, content-tree hash, offline
   CPU load, launcher-compatible local retrieval, permissions and storage.
   Report a blocker if absent or unsafe; do not download anything.
3. Inspect the approved L1 launcher/configuration contracts. Reconstruct the
   deterministic four-page document using current source and preparation-only
   tooling. Verify extraction, one chunk/two reducers, dependencies and all four
   calls. Recalculate source/configuration/plan bindings, rendered input limits
   and output reservations, and identify durable output/publication artifacts.
   Separate public reproducible hashes from private operator-scope bindings.
   Do not fabricate an operator principal, replace authority state or create a
   falsely final launch configuration. Document protected actual-scope steps as
   pending for the operator.
4. Review prerequisites for current deployment/model/version/SKU, RPM/TPM and
   shared consumers, valid operator identity and inference credential, existing
   security/governance/financial authorities, applicable current EUR catalog and
   additional charges, remaining headroom/unresolved obligations, independent
   approval trust/replay protection, and the permitted execution window.
   Verify cost estimation with exact decimal arithmetic. Historical prices and
   quotas do not establish current values. Protected/cloud checks are PENDING
   for the operator; do not access protected credentials or authority databases.
5. Review stop conditions for authentication/approval failure, provider failure
   or timeout, invalid JSON/schema/domain output, missing evidence/child links,
   input/output breach, unknown usage/failed settlement, publication/retrieval/
   citation failure, and unexpected paid dependencies. No automatic replay,
   fallback, retry, budget enlargement or replacement-authority recovery.
   Define live acceptance evidence: COMPLETE digest, full source coverage,
   publication/retrieval, correct grounded answer, settled usage and independent
   semantic review. Distinguish structural acceptance from semantic support.
6. Classify engineering readiness GO/NO-GO, operator preparation READY/READY WITH
   GAPS/BLOCKED, and live execution AUTHORIZED/NOT AUTHORIZED independently.
   Authorization must remain NOT AUTHORIZED. Order remaining operator actions by
   dependency. Do not generate a signature, consume approval, reserve real funds
   or launch inference.

## Limits and restrictions

- Maximum four model calls, 25,000 input and 3,000 inclusive output tokens per
  call; cumulative maxima 100,000 input and 12,000 output tokens.
- Zero automatic paid retries; one outstanding inference call; retain minimum
  spacing and shared-quota reserves.
- Financial upper bound at most EUR 5, subject to actual remaining headroom and
  independently approved cost evidence; this task grants no spending authority.
- No paid inference, cloud creation/modification/deployment, AKS/Kubernetes
  operations, signing/consumption, real reservation, protected credential or
  authority-database access, incompatible historical checkpoint reuse, or
  unrelated engineering changes.
- No Git stage, commit, push, reset, clean or branch switch. Owner retains all
  Git operations. Local model packaging and the two Markdown deliverables are
  permitted. Execution-sandbox approvals still apply to writes outside its roots.

## Permanent deliverables and final handoff

Create this normalized prompt and
`docs/codex/reports/phase_17h_four_call_l1_operator_preparation_and_final_authorization_review.md`.
The report must contain executive summary, source/CI verification, durable model
validation, exact proposed plan, configuration/source bindings, current offline
evidence, Azure/financial prerequisites, security/independent approval, blockers
and ordered operator checklist, GO/NO-GO recommendation, authorization status,
and exact next recommended operator action. Report actual results; never mark
unverified private/cloud conditions PASS.

Summarize engineering and embedding readiness/fingerprint, plan compatibility,
financial/authorization verification, operator actions, technical blockers and
report location. Stop after preparation/readiness assessment. Final authorization
and all Git operations remain the repository owner's responsibility.
