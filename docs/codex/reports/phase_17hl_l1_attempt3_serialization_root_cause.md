# Phase 17H-L — Attempt 3 serialization root cause

**BLOCKED — EXACT UNRESOLVED CAUSE**

The cause is reproduced and known: the successful provider response violates
`stage-result/1` in nine places. The second claim has a malformed evidence UUID,
and eight top-level `unused1`–`unused8` fields are forbidden. There is no demonstrated
serializer defect to correct. Accepting this recorded response would require
repairing an evidence identifier and deleting unsupported content, contrary to
the requested fail-closed boundary. No runtime correction was implemented and
the historical FAILED result remains unchanged.

## Evidence and offline reproduction

Read-only inputs were the Attempt 3 packet's `audit/responses.json`, configuration,
and persisted extraction and digestion-plan objects. The response SHA-256 matches
its recorded hash. The current generation-contract fingerprint matches the packet:
`2ff2aff8f575ed99b23108dd5d10c2f7a73a55fb6cc7e073107e0597124c7290`.
The existing preparation report and relevant implementation/tests were inspected.
No private response text, source text, evidence identifiers, credentials, or
approval artifacts were copied into repository fixtures.

The preserved content is valid JSON: 2,144 UTF-8 bytes, four claims, and all
defined stage and claim fields present. Recorded usage is 1,994 input and 932
output tokens. Successful provider execution does not imply schema compliance.

The exact failure path is:

1. `OpenAICompatibleProvider.execute()` decodes the provider envelope and returns
   text plus usage. An offline fake HTTP envelope containing the exact preserved
   text and recorded usage passed the original provider decoder unchanged, in
   one fake call. The original wire envelope was not preserved in these response
   records; the replay envelope was explicitly synthetic, not claimed as original.
2. `ManagedSynthesisInference.analyze()` converts text to UTF-8 and enforces the
   10,000-byte provider limit. The preserved text fits. In governed execution,
   financial settlement has already occurred before this method returns bytes.
3. `DigestionHandler.__call__()` invokes `validate_result()`. Its request was
   reconstructed from the persisted plan with `DigestionHandler.request()`;
   `EvidenceIndex` used the persisted extraction artifact. No live authority,
   database writer, model client, or worker was constructed for this private replay.
4. `validate_result()` calls `documents.digestion.codec.decode()`.
   Duplicate-checking JSON parsing succeeds. The exact failing operation is
   `StageResult.model_validate(...)` inside `decode()`.
5. Pydantic raises `pydantic_core._pydantic_core.ValidationError` with nine errors:
   `claims.1.evidence_ids.0`: `uuid_parsing`, sanitized message
   **“Input should be a valid UUID, invalid group length in group 4: expected 12,
   found 13”**; and each `unused1`–`unused8`: `extra_forbidden`, sanitized message
   **“Extra inputs are not permitted”**. No input values were printed with errors.
6. `decode()` catches the validation exception and raises
   `documents.digestion.models.DigestionError`, message
   **`inference_contract_error`**, suppressing the original exception context.
   `classify_managed()` delegates to `classify_digestion()`, which maps this to
   **`serialization_error` / `NON_RETRYABLE`**. The taxonomy intentionally groups
   decoding/model-contract failures under this legacy category; it does not mean
   `json.dumps()` failed.
7. Canonical encoding, evidence/lineage checks, inherited-summary construction and
   checkpoint persistence are **not reached** for the unchanged response. Reduction,
   final digest and publication cannot proceed from this failed analysis stage.

Two diagnostic counterfactuals isolate causality. Removing only the eight unknown
fields still fails UUID parsing. Repairing only the malformed UUID still produces
eight forbidden-field errors. There is one supplied evidence identifier reachable
by deleting one character from the malformed value. A strictly in-memory
counterfactual with both changes passes the original evidence/lineage/coverage
validation, serializes to 2,023 canonical ASCII bytes and round-trips successfully.
Its inherited summary retains four analyzed pieces and one qualification. This
experiment was neither accepted nor persisted and is **not** an automatic repair
proposal. It shows that neither byte limits nor canonical serialization caused
the recorded failure.

## Contract assessment and correction boundary

`FrozenModel` uses `extra='forbid'`. `StageResult` permits exactly
`schema_version`, `stage_id`, `kind`, `outcome`, `claims`, `open_questions` and
`limitations`. Its model-required fields are `stage_id`, `kind`, `claims`; the
others have defaults. Claims require `claim_id`, `originating_stage`, `text` and
`kind`. Evidence identifiers must parse as UUIDs; application validation then
requires membership in the supplied evidence set, correct claim ordering,
originating stage, complete coverage and valid child links. Unknown fields are
forbidden at nested model boundaries too, regardless of whether their values
are null.

`generation_schema()` marks every defined property required, exposing defaults
to generation without changing storage compatibility. `managed-prompt/3` asks
for exactly that schema, explicitly includes default/null/empty-array fields,
restricts citations to supplied evidence IDs, and specifies lineage and claim
identity rules. Its null instruction does not authorize invented fields. The
prompt is stricter about including default fields than the storage model, but
that distinction did not cause this failure: all defined fields were present.

The candidate capability uses `structured_output='json_object'`. The provider
therefore requests JSON-object output, not server-enforced schema output; the
schema is supplied through the prompt. The generated object violated that
contract despite valid JSON syntax. The application applies the intended strict
contract correctly. Changing generation mode would be a separate capability and
contract change, would not repair this recorded response, and cannot be claimed
to prevent invalid evidence without further verification. No such change,
prompt rewrite, content filtering, identifier repair, retry or fallback was made.

The 10,000-byte provider/canonical limits and 3,000-token completion ceiling remain
unchanged. Evidence, qualifications, contradictions, lineage, governance and
pricing remain unchanged. Generation fingerprint: **unchanged**, as above.

## Focused verification and financial settlement

Added `tests/integration/test_attempt3_serialization.py`, using entirely synthetic
content and identities with socket access forbidden. Command:

```text
python -m pytest tests/integration/test_attempt3_serialization.py -q
7 passed in 0.85s
```

Three parametrized cases reproduce both violations together and each independently,
including the exact validation error types and terminal classification. A valid
control verifies the generation schema, actual ASCII canonical serialization,
Unicode escaping, round-trip decoding, acceptance at the canonical byte limit,
rejection one byte above it and rejection above the 10,000-byte raw bound. Two
cases reject malformed and duplicate-key JSON. The final case runs the actual
offline governed workflow with a synthetic malformed provider response: one
provider call, FAILED/serialization_error, no retry or publication, completed run
settlement and a SETTLED financial record. It checks the original 3,000-token and
10,000-byte request limits. Synthetic pricing produces exactly EUR 0.000011 for
30 input / 40 output tokens; it does not substitute synthetic rates into history.

The private record independently confirms the actual Attempt 3 settlement is
SETTLED, EUR 0.005006599788807204, with provider outcome success.
`GovernedExecution.execute()` settles usage and finishes admission in its
`finally` block before downstream validation. Downstream rejection does not undo
billable provider work. No historical financial or governance record was altered.

There is no corrected-response success regression because there is no permissible
runtime correction. The valid synthetic control demonstrates the existing accepted
contract; it must not be mistaken for successful recovery of Attempt 3.

## Separate launcher exit-code finding

`foundry_l1.launch()` calls `guard.stop('evidence')` when the job fails, then
returns the result normally. `main()` prints the returned job state and reaches
normal process completion. Its exit-code-1 path handles exceptions only. Thus
a terminal FAILED job can yield process exit code 0. A separate future change
could map unsuccessful job/question status to a nonzero CLI exit after preserving
audit finalization. No launcher correction is included in this investigation.

## Review, scope and remaining risk

Self-review and separate pre-commit review found no runtime changes, dependencies,
secret material, private fixtures, generated repository artifacts, or API changes
introduced by this investigation. Only synthetic regression tests, a task summary
and this report were added. Existing uncommitted work on `master` was preserved.
`git diff --check` and focused bytecode compilation were run; full JSON-limit,
governance and repository suites were deliberately not repeated. Docker validation
is not applicable to these test/documentation additions.

The remaining blocker is acceptance of schema-invalid generated content under a
strict no-repair contract. More specific sanitized diagnostics may improve future
triage, but would not correct this response. No Azure inference, live authority
initialization, new signing, approval, Attempt 4 work, infrastructure changes,
staging, commits or pushes occurred.

Final repository status remains `master` with the pre-existing 17 modified tracked
files (386 insertions, 33 deletions) plus pre-existing untracked phase artifacts
and the three new investigation files. `git status --short` and `git diff --stat`
were inspected; the tracked diff stat is unchanged by this task because its
additions remain untracked.
