# Phase 17H — R0/R1 offline evidence-provenance hardening

User task received 7 November 2026 for `master` in
`Susanta2025-lab/estudio-polymind-llm-orchestration`. This clean task record
preserves the implementation scope and acceptance requirements.

## Context and source reports

Read `docs/codex/reports/phase_17h_live_invalid_qualification_source_root_cause.md`
and `docs/codex/reports/phase_17h_final_approval_signing_and_controlled_execution.md`.
The authorized four-call evaluation stopped after one successful provider response
failed G2: `invalid_reference / evidence_validation / invalid_qualification_source`
at `claims[7].qualifications[0].evidence_ids[3]`. Eight claims contained 17 valid
primary evidence-reference occurrences. The final qualification had three valid
references and one foreign UUID combining segments from two authorized IDs.
Schema decoding succeeded; G2 correctly rejected membership. Usage was 2,506
input and 2,130 output tokens, EUR 0.010088437170011206 under the approved catalog.
The approval is consumed. No additional paid inference or retry is authorized.

## R0 — Permanent regression coverage

Resolve actual test paths before editing. Inspect the final offline Azure
compatibility, live-failure observability, qualification source-contract, managed
digestion and two-chunk integration tests.

- Add a deterministic synthetic `StageResult` with valid primary evidence and
  surrounding claim identities/provenance, several valid qualification references,
  and a syntactically valid foreign UUID late in that list. Expect
  `evidence_validation_failed / invalid_qualification_source`; no accepted checkpoint.
- Construct a segment-blended UUID from two synthetic authorized IDs, prove UUID
  syntax and schema decoding succeed, and prove G2 rejects membership. Never use
  private response content or exact live evidence IDs as fixtures.
- Add a positive multi-reference qualification control using distinct authorized IDs.
- Confirm empty/duplicate/foreign qualification references, excessive qualification
  text, invalid primary/contradictory evidence and incorrect reducer inheritance
  are rejected. Add only missing coverage.
- Through established isolated synthetic authorities and mocked HTTP, verify a
  schema-valid provenance failure stops application acceptance with the established
  category, commits no analysis checkpoint, runs no structural/root synthesis,
  publishes no digest, starts no grounded Q&A, makes no automatic retry, and
  preserves known usage and settlement.

## R1 — Minimal provider-neutral generation clarification

Inspect `documents/digestion/managed.py`, especially
`ManagedSynthesisInference.render`, trusted instructions, CONTROL and schemas.
Add concise instructions applying equally to primary, contradictory and nested
qualification evidence references:

- Select every evidence reference from current `CONTROL.allowed_evidence_ids`.
- Copy complete, unchanged identifiers, including every UUID segment. Never
  invent, reconstruct, shorten, combine or modify IDs.
- Claim IDs and stage IDs do not substitute for source evidence IDs.
- Distinguish directly permitted current-stage evidence from inherited child
  provenance. Preserve inherited qualifications/conflicts through valid child
  lineage. Do not copy inherited qualification IDs into new direct-reference
  fields unless explicitly allowed at this stage.
- Preserve existing coverage, claim identities, conflict propagation and G1/G2.

Use a few precise instructions without repeating the evidence inventory. No output
repair, retry, fallback, extra provider call, qualification deletion, evidence
omission or relaxed validation. Keep structured-output/provider compatibility.

## Versioning and limits

Increment the prompt template using the existing stage/profile/configuration
fingerprints. Preserve historical identities and fixtures; old checkpoints must
not silently become compatible. Do not change unrelated schema/application versions.
Compute `generation_contract_digest()` and compare against
`00bf895290e1da2fb81372ff1ea921d8d7f464ea14f41110f54313d0423ad904`.
Do not overwrite hashes to force compatibility. Confirm old signed approval
bindings cannot authorize the new contract; leave the failed run and approval immutable.

Verify escaped JSON, system/CONTROL envelopes, rendered input, child contribution,
raw/canonical result, HTTP envelope, planning and checkpoint fingerprints. Do not
increase the established per-call 25,000 input/3,000 output, four-call
100,000 input/12,000 output, 28,000 context, 7,000-byte child or 10,000-byte result
ceilings. Stop and document any genuine admission incompatibility; never truncate
provenance or weaken coverage to force a pass.

## Verification sequence and report

First run R0 against unchanged validation; then implement/version R1; then run
focused contracts, G1/G2, qualification/conflict inheritance, chunk/reducer/root,
two-chunk digestion, deterministic checkpoints, publication and grounded citations.
Verify Azure strict schema, generic OpenAI-compatible and JSON-object contracts,
schema conversion, bounded HTTP, settlement and no retries. Run the full offline
suite if feasible, applicable configured quality checks, diff/compile checks,
implementation self-review and separate pre-commit review. Do not hide failures
with skips, xfails or replacement mocks. Offline instruction tests do not establish
that a live model always complies.

Create `docs/codex/reports/phase_17h_r0_r1_evidence_provenance_hardening.md` with
failure/root-cause evidence, R0/R1 implementation, exact changed files, versioning,
G1 sizes, G2 lineage, exact offline/provider test results, old/new generation
digests, remaining risks, future live preparation and engineering readiness.

## Restrictions and final response

No Azure inference/resources, paid calls, live approvals/signatures/consumption,
operator-token acquisition, private-key access, production authority database
changes, run-guard reset, replacement checkpoints, changes to retained live evidence,
financial/governance policy edits, Kubernetes/AKS operations, or Git staging,
commits, pushes, resets or branch changes. No R2 dynamic schema enums, R3 diagnostics
or unrelated architectural refactors. Use only isolated synthetic test state.

Final response must give R0/R1 PASS/FAIL, exact changed files, prompt before/after,
old/new generation digests, G1/G2/integration/full-suite results, blockers and
readiness for separately authorized reassessment. Do not mark Phase 17H live
validation complete. End with `R0/R1 OFFLINE ENGINEERING: PASS` or
`R0/R1 OFFLINE ENGINEERING: BLOCKED`. Stop after offline work and documentation.
