# Phase 17H — G1/G2 Offline Engineering and Integration Hardening

## Context

Phase 17H remains PARTIAL. Read
`docs/codex/reports/phase_17h_hierarchical_digestion_readiness_assessment.md`
before starting. Its engineering gaps are:

- G1: application-valid chunk results can exceed downstream reducer limits after
  rendering schema, child links, inherited metadata and JSON escaping.
- G2: the strict managed-inference contract lacks a complete two-chunk integration
  test covering hierarchy, governance, publication, retrieval and grounded Q&A.

The existing single-chunk Azure Foundry analysis was successful. Establish reliable
**offline** readiness for the complete hierarchical workflow.

## Required work

1. Add permanent G1 regressions using the current strict contract: valid outputs
   approaching the 10,000-byte canonical limit; intermediate/structural and root
   rendering; claims, evidence links, inherited metadata and JSON escaping; and
   Q&A with retrieved evidence and derived annotations. Reject oversize before
   inference and never silently truncate required information.
2. Reconcile planning/capacity estimates, permitted outputs, actual rendered
   inputs, provider context/token limits, and Q&A envelopes. Prefer the smallest
   predictable, enforceable policy. Preserve evidence coverage, lineage,
   qualifications, conflicts and strict validators. Do not simply restore the
   3,000-byte limit: an accepted historical response exceeded it. Explicitly
   reject shapes that cannot fit during appropriate planning/admission.
3. Add one deterministic synthetic document requiring exactly two analysis
   chunks. Use strict fake responses and synthetic accounting through two chunk
   analyses, structural reduction, root synthesis, persistence/reopening,
   authorized publication/activation, retrieval with canonical citations and one
   grounded Q&A call. Verify exactly five calls, complete coverage, parent-child
   links, cross-chunk qualifications/conflicts, publication/retrieval, valid
   citations, settlement and checkpoint reuse. Include invalid links, omitted
   children and oversized downstream results. Reuse existing test infrastructure.
4. Run affected G1/G2 tests and relevant managed-digestion/publication tests.
   Revalidate the existing four-call L1 synthetic workflow and strict validation,
   authorization, accounting and provenance. Use isolated offline infrastructure;
   avoid repeating the entire suite without justification. Record actual commands
   and outcomes.
5. Produce
   `docs/codex/reports/phase_17h_g1_g2_offline_engineering_and_integration_hardening.md`
   with executive summary, G1 cause/correction/rationale, permanent tests, G2 and
   four-call results, limitations, READY / READY WITH GAPS / NOT READY assessment,
   and recommended next controlled live L1 action. Distinguish verification from
   assumptions. Do not claim full Phase 17H or production readiness.

## Restrictions

All inference must be offline/synthetic. No Azure Foundry, paid provider, AKS,
cloud deployment, private operator approvals or credentials. Do not weaken
security, governance, financial safeguards or strict validation. No automatic
paid retries, unrelated refactoring, dependencies or mass formatting. Preserve
source/checkpoint compatibility where possible and all historical evidence.
Do not stage, commit, push, reset, clean, switch branches or execute live inference.
The original task additionally requested no Git operations.

The continuation instruction was to inspect existing modifications, retain valid
completed work, avoid unnecessary repetition, finish verification and the report,
and provide actual test results and final readiness.

## Acceptance and handoff

Permanent G1 tests must reproduce the original incompatibility and verify the
correction. The policy must be enforceable against rendered inputs. Strict G2
and the existing four-call L1 must pass, with no required evidence, qualifications
or links discarded. All relevant executed checks must pass or have explicit
remaining-failure documentation. The final response should concisely identify
G1 resolution/limits, G2 outcome, four-call verification, readiness, modified files
and report path. Changes remain uncommitted for review.
