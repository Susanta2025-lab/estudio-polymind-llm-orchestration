# Phase 17H — CI Failure Correction and Historical Contract Compatibility

## Context and objective

Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`.
Starting commits: `d940443` (G1/G2 engineering) and `f3a2a87` (documentation).
The supplied Estudio PolyMind CI run `41451173192` failed in job `build`,
step `Run automated tests`, with **1,803 passed, 15 failed, 13 errors**.
Run reference: https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/41451173192.

Restore the complete offline CI suite while preserving the G1 7,000-byte
rendered-child admission policy, independent 10,000-byte raw/canonical output
limits, G2 strict two-chunk workflow, historical contracts/checkpoint readability,
and strict validation, provenance, security and financial governance. Do not
change contract fingerprints merely to satisfy tests.

Observed symptoms, not assumed independent causes:

- Historical `ManagedSettings` fixtures reject `child_input_bytes=7000` as extra.
- Frozen source contracts, configuration fingerprints and historical generation
  assertions fail.
- Result/checkpoint validation reports `synthesis_limit_exceeded` and
  `incompatible_checkpoint`.
- Affected tests concentrate in `test_live_failure_observability.py` and
  `test_final_offline_azure_compatibility.py`.

## Required work

1. Inspect the checked-in workflow, repository state, implementations, consumers,
   tests and relevant documentation before editing. Reproduce offline using the
   CI Python/dependency configuration where practical. Classify every failure as
   fixture isolation/configuration, legitimate historical incompatibility,
   intended G1 behavior needing a scoped assertion, implementation regression,
   or CI-specific behavior. Establish causes with evidence first.
2. Trace settings rejection to source snapshots, serialized configurations,
   fixture construction or current handling. Apply the smallest correction that
   reconstructs historical fixtures under their original contracts. Preserve
   the active G1 policy and compatibility when unset; do not silently upgrade
   old requests, bypass Pydantic, or weaken checkpoint rejection.
3. Distinguish frozen historical source from intentional G1/G2 current changes
   and historical configuration bindings. Preserve original evidence and all
   approved hashes/goldens. If exact frozen source equality conflicts with an
   intentional change, document it and implement a narrow, independently
   reviewable compatibility approach. Do not blindly refresh fixtures.
4. Trace output and checkpoint failures. Verify independent 10,000-byte
   raw/canonical bounds, current 7,000-byte L1 child admission, historical
   profiles without that policy, fail-closed invalid checkpoints and unchanged
   complete evidence. Keep historical semantics and current policy assertions
   correctly scoped. Do not remove negative tests or truncate output/evidence.
5. Re-run all affected cases, G1 sizing tests, G2 integration tests, the four-call
   L1 synthetic workflow, historical source/fingerprint tests and the complete
   offline suite run by CI. Use existing isolation; record exact commands and
   counts. No silent skips, deselection or expected-failure markers. Report any
   remaining failures candidly.
6. Preserve this normalized prompt and a permanent report at the corresponding
   `docs/codex/prompts/` and `docs/codex/reports/` paths named
   `phase_17h_ci_failure_and_historical_contract_reconciliation.md`.

## Report and final response requirements

The permanent report must contain an executive summary, failure classification,
established root causes distinguished from hypotheses, minimal corrections,
historical compatibility evidence, G1/G2 results, complete CI-equivalent offline
results, remaining risks, exact changed-file inventory, **PASS / PARTIAL / FAIL**
readiness decision and suggested conventional commit message. Include self-review,
pre-commit review, validation outcomes, architectural impact and limitations.

The final response must provide root causes, corrections, previously failing
tests PASS/FAIL, exact full-suite pass/fail/error/skip counts, G1/G2 status,
modified files, suggested commit message and permanent report path.

Declare PASS only if every reported failure/error is resolved, historical
integrity remains intact, G1/G2 and four-call L1 remain valid, the complete
CI-equivalent suite passes without artificial exclusions, the report is complete,
and no paid/cloud operation occurred. Otherwise report PARTIAL or FAIL and blockers.

## Restrictions

- No network access, paid inference, automatic paid retries, deployment, cloud
  resources or private operator approvals/credentials.
- Do not start Docker, Kubernetes or AKS unless strictly necessary and separately
  authorized. No such operation is needed for this offline correction.
- Do not weaken validation, evidence lineage, security, governance or financial
  policy, or alter historical fingerprints solely to pass assertions.
- Modify implementation, test isolation and fixtures only as justified by verified
  causes. No unrelated changes, dependency additions or mass formatting.
- Do not stage, commit, push, reset, clean, switch branches or otherwise mutate
  Git state. The owner reviews and performs Git operations manually.
- Do not proceed to Phase 17H live operator authorization before resolving CI.

Repository `AGENTS.md` guidance remains applicable, including inspection,
architecture preservation, validation, separate self/pre-commit review and final
`git status` / `git diff --stat` reporting.
