# Phase 17H — G1/G2 Git Checkpoint Verification and Local Embedding Packaging

Normalized task received 2026-11-02. Repository: Estudio PolyMind.

## Context

Phase 17H remains PARTIAL. G1/G2 offline engineering passed; the subsequent
four-call L1 assessment gave GO for operator preparation and NOT AUTHORIZED for
execution. Source and documentation remain uncommitted. The local embedding
cache loads but its eleven symlinked files fail the launcher's regular-file rule.

Read:

- `docs/codex/reports/phase_17h_g1_g2_offline_engineering_and_integration_hardening.md`
- `docs/codex/reports/phase_17h_four_call_l1_live_preparation_and_authorization_readiness.md`

## Required work

1. Audit Git read-only: current branch/HEAD, tracked modifications, untracked
   files, staged changes, relevant implementation/tests/configuration/docs,
   consumers, generated/private artifacts, secrets, whitespace and documentation
   references. Reconcile actual pending files with the engineering reports;
   identify missing checkpoint files. Do not cosmetically change existing files.
2. Propose C1 engineering and C2 documentation commits with exact file lists,
   grouping rationale, conventional messages, exclusions and exact manual
   staging/commit/push commands marked NOT EXECUTED. The owner performs them.
3. Verify the actual cache for `sentence-transformers/all-MiniLM-L6-v2`, revision
   `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`. Using existing local bytes only,
   create a separate dedicated directory outside Git if required. Never download,
   reinstall, modify/delete the cache, replace approved operator directories or
   overwrite an existing model tree. Materialize verified cache links as regular
   files with required relative structure, no duplicate/extra/unverified files.
   Reject destination symlinks, broken source links, unexpected entries and unsafe
   traversal. Verify revision and the exact launcher content-tree SHA-256.
4. Load offline with `local_files_only=True` on CPU; verify an actual finite,
   normalized 384-dimensional embedding and the launcher local-validation
   contract. With isolated temporary storage, create a small Chroma collection,
   embed/query/inventory it and check generation/document/version isolation where
   supported. Never touch production/operator publication databases or require
   network/cloud services. Report a blocker if safe packaging is impossible.
5. Run targeted offline G1 sizing, strict G2 two-chunk, existing four-call L1 and
   historical configuration/fingerprint regressions plus local packaging and
   retrieval validation. Avoid full-suite execution. Record exact commands,
   actual outcomes and failures; investigate failures without unauthorized code
   changes. Verify repository engineering files and historical contracts remain
   unchanged by this task.
6. Produce
   `docs/codex/reports/phase_17h_g1_g2_git_checkpoint_and_embedding_packaging.md`
   and this normalized prompt. Include executive summary, current Git inventory,
   engineering/documentation review, C1/C2 plan/messages/manual commands, cache
   assessment, packaged-model results/revision/fingerprint, Chroma verification,
   targeted results, remaining risks/blockers and final recommendation.

## Restrictions

No staging, commits, pushes, branch switching, resets, clean operations or history
changes. No Azure inference, paid cloud work, Kubernetes/AKS, downloads, dependency
installation, private approval-artifact modification or authorization/financial
budget consumption. No application, existing-test or configuration edits without
separate engineering authorization. Only the new isolated embedding directory,
disposable verification artifacts and required Markdown records are authorized.
Do not expose credentials or private operator paths in permanent documentation.

## Acceptance and final handoff

Review all pending G1/G2 files; document exact proposed commit contents/messages;
package the model safely or report an explicit blocker; verify the launcher hash,
CPU embedding and isolated retrieval; pass relevant regressions or document all
failures; finish the permanent report. Classify Git checkpoint readiness and
local embedding readiness independently as READY / READY WITH GAPS / NOT READY.
Never claim Azure execution authorization.

Final response must include both classifications, C1/C2 messages and exact file
counts, embedding results/fingerprint, executed offline test outcomes, blockers
and report location. Explicitly confirm no staging, commit, push, cloud inference
or authorization consumption occurred. The repository owner reviews and executes
any Git mutation manually.
