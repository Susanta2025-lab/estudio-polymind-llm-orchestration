# Phase 17H-L first live failure diagnosis

## Finding

The failure occurred in first-chunk **analysis**, inside the durable **NORMALIZING**
step, after successful provider execution. It was a canonical result-size violation,
not a PDF extraction failure or failed provider call.

`documents/digestion/validation.py:49`, `validate_result`, raised
`DigestionError('synthesis_limit_exceeded')` because
`len(encode(result)) > profile.max_result_characters`.
The persisted profile sets that limit to **3,000 canonical ASCII JSON bytes** despite
its historical `max_result_characters` name. The response was **2,597 UTF-8 bytes**;
Pydantic default expansion followed by canonical encoding produced **3,471 bytes**:
**471 bytes (15.7%) over the limit**.

The response omitted top-level `schema_version` and, in each of eight claims,
`contradicting_evidence_ids`, `lineage`, `qualifications`, `stance`, and `status`.
Inserting these defaults added **874 bytes**. Compacting the supplied JSON alone
still measured 2,597 bytes, excluding whitespace as the explanation.

## Evidence and exact path

The response copies in `result.json`, `provider-calls.json`, and `responses.json`
match each other and their recorded SHA-256 digests. Private object inspection
recovered the original immutable plan and extraction artifact. Read-only SQLite
inspection confirmed the planning step succeeded, analysis failed on attempt one,
and the remaining three steps were cancelled without attempts. The recorded failure
is NON_RETRYABLE. No accepted analysis checkpoint exists among the stored objects.

The code path is:

1. `ManagedDigestionHandler.analyze` binds the chunk execution context.
2. `ManagedSynthesisInference.analyze` obtains the successful governed response and
   checks its UTF-8 length against 3,000 bytes; 2,597 passes.
3. `DigestionHandler.__call__` passes those bytes to `validate_result`.
4. `check_request` passes. `codec.decode` passes the raw size check, strict JSON
   duplicate-key handling, and `StageResult` model validation.
5. `codec.encode` serializes the validated model with defaults using
   `documents.jobs.models.canonical` (compact, sorted, ASCII JSON).
6. `validate_result` rejects 3,471 > 3,000 before evidence validation/checkpoint write.
7. `classify_managed` delegates to `classify_digestion`, whose legacy mapping converts
   `synthesis_limit_exceeded` to `DocumentError('extraction_limit_exceeded')`.
   The worker persists that sanitized category.

An isolated call to the existing validator with the persisted request and response
reproduced that exact exception and line. A separate in-memory diagnostic suppressed
only the canonical-size check to inspect later checks: all passed. This was diagnostic
only; no accepted result, checkpoint, plan or ledger was written and no production
validation was relaxed.

## Response and source assessment

The stored response is complete, valid JSON and compatible with the existing
`StageResult` schema. It contains eight claims (maximum eight); claim text lengths
are 75, 73, 75, 73, 75, 172, 75 and 73 characters (maximum 256). It has no
qualifications, open questions or limitations. Every one of the four supplied
evidence IDs is referenced, and IDs/spans/claim identities pass existing validation.
The extracted source has four pages and 1,491 characters, partitioned into four
pieces in one chunk. There is no source truncation in this failure.

Usage records show 1,460 output tokens against a 3,000-token reservation. The audit
stores generated text, not the original HTTP envelope/finish reason. Consequently
an exact finish reason cannot be recovered. Successful current adapter handling
means it was `stop` or absent: `result_text` rejects `length`/`max_tokens` and other
non-completion reasons. The complete parse and recorded success provide no evidence
of truncation. Structural citation validation is not independent semantic review;
this diagnosis does not certify factual support or complete semantic coverage.

## Minimal correction

The mismatch is between the **generation representation and canonical pipeline
representation**, not demonstrated insufficiency of the model's context window.
The prompt supplied a schema permitting omission of defaults while enforcing a
post-expansion byte limit. The configured JSON-object provider does not itself
enforce the application JSON schema; trusted prompt instructions carry it.
The 3,000 output tokens and 3,000 canonical bytes are different measures, even
though the conservative planning profile uses the same numeric reservation.

Changed `documents/digestion/managed.py` only in the rendering contract:

- Generate a schema requiring all object properties, including defaulted fields,
  at every nested definition; use the same schema in trusted CONTROL and the
  provider-neutral GenerationRequest.
- Explain the total compact ASCII JSON budget, including defaults and Unicode
  escapes, and require concise output without dropping coverage or lineage.
- Version this changed template as `managed-prompt/2`, including the bound planning
  profile, so configuration fingerprints cannot silently reuse old checkpoints.

The stored `StageResult` schema, canonical serializer, size limits, evidence checks,
provider boundary and governance behavior remain unchanged. Explicit configurations
pinning `managed-prompt/1` must be updated intentionally; the new renderer rejects
that old template version. Old immutable objects remain readable. This correction
does not make the original oversized result acceptable and does not repair or retry it.

A pure offline rendering against the original extracted source, with a new in-memory
plan and a provider stub that cannot execute, measured 10,720 estimated input tokens
including overhead/safety, plus 3,000 reserved output tokens, below context 28,000.
The DAG remains one chunk and two reducers. No original plan was altered.

Because JSON-object mode cannot guarantee schema adherence or byte counting, a new
response can still fail closed. A larger budget, changed chunking, or capability
upgrade is not justified merely by this failure. No content is truncated or silently
removed to force success.

## Validation and review

Two synthetic regression tests cover the new generation contract/version and the
original failure mechanism: a raw response below 3,000 expands above 3,000 and must
still fail with the same classification; a concise explicit-default response retains
all eight synthetic claims and citations and passes. No private response text was
copied into tests or repository documentation.

The focused isolated run passed **169 tests**, with **one L2 workflow case deselected**:
managed inference, digestion validation, managed and governed digestion integrations,
Foundry preflight, and offline workflow. Socket connections were blocked in that
process. The workspace's live settings initially caused 25 failures in a 98-test run
(73 passed); an additional 98-test run had 93 passes and five envelope setup errors
because its local replica lacked OIDC authorization. These were test-environment
coupling, addressed by process-local `GOVERNANCE_ENABLED=False` and disabled API auth
for legacy fake-provider tests. Governed tests configure their own authorities;
production settings files were not modified.

The separate `tests/unit/test_foundry_30k.py` run passed **26 tests** under the same
isolated settings and socket block. These include existing pure synthetic envelope
calculations for four- and 200-page fixtures, not live L2 execution. Total final
offline validation: **195 passed, one workflow case deselected**.

`git diff --check` passed. `compileall` passed for both changed Python files with
an external bytecode cache. Full repository pytest, Docker and infrastructure
validation were not run for this focused offline correction.

Implementation self-review and separate pre-commit review checked the complete
change: no provider-specific logic, canonical format change, acceptance bypass,
retry, dependency, secret, raw response, temporary artifact or unrelated code change
was introduced. The prompt/report document the representation mismatch and template
compatibility impact. Existing unrelated uncommitted work was preserved.

All **14 original audit files** matched before/after SHA-256 hashes, including both
SQLite ledgers and private objects. Original evidence was read only; no finance
reset/reconciliation, RSA approval, Azure operation or model call occurred.

## Recommendation and repository state

A **new, separately approved L1 execution is technically justified after review of
this correction**, as a test of model compliance with the now-explicit canonical
output contract. It is not evidence that L1 will succeed. Do not resume the failed
job or reuse its accepted plan under the changed template. No L1 rerun or live L2
execution was performed in this task.

`git status --short` shows the two task code/test modifications alongside existing
uncommitted work and the new task prompt/report. At review, aggregate tracked
`git diff --stat` was 12 files, 211 insertions and 12 deletions, including pre-existing
changes; this task's tracked delta is two files, 73 insertions and four deletions.
New prompt/report files are untracked and excluded from that stat.
**No commit or push occurred.**
