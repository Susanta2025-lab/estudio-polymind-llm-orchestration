# Phase 17H–L: offline diagnostic hardening

## Baseline and historical limitation

The supplied historical audit records a completed strict provider response followed by application rejection (`serialization_error`), one consumed call, and no accounting failure. The response was not retained. This change cannot determine the historical cause and makes no retrospective diagnosis. Historical audit, configuration, approval, and replay material was neither opened nor modified.

The checkout already had substantial tracked and untracked implementation work. This phase preserves it. Baseline copies of the four edited implementation files were retained outside the checkout to review only this phase's changes.

Inspection covered codec, validation, models, managed inference, workflow, Azure schema conversion, structured contracts, governance execution, the single-call runner, and existing digestion/schema/runner tests. The runner invokes provider execution through governance, settles provider usage, then calls `validate_result`. That checks request integrity, decodes and validates StageResult, canonically serializes/revalidates it, checks contracts and evidence, and raises content-free DigestionError on rejection. `classify_managed` delegates to `classify_digestion`; the existing private immutable outcome writer persists the category.

All explicit `inference_contract_error` branches were inspected: codec encoding and decoding; stage ID/kind, unavailable outcome and empty analyzed claims; deterministic claim ID/duplicate ID/origin; non-fact subject; and duplicate fixture blocks in FakeInference construction. DigestionError also normalizes unknown categories to that error. The fixture-construction and unknown-category fallbacks remain without a diagnostic because they do not establish a result-validation stage.

## Changes and taxonomy

- `documents/digestion/models.py`: fixed enum and optional keyword-only diagnostic on DigestionError. Invalid/untyped metadata is omitted; exception category/message is unchanged. No Pydantic model field or schema was changed.
- `documents/digestion/codec.py`: separates JSON parsing, duplicate rejection, and model validation; canonical dump/revalidation/encoding remains a single bounded diagnostic stage. Existing broad normalization and byte checks remain intact.
- `documents/digestion/validation.py`: labels existing rejection branches and EvidenceIndex reference checks without changing predicates or their order.
- `tests/performance/foundry_single_call.py`: persists the optional enum value only for application-validation failures. Existing public classification, accounting, security, private paths, and durable writing remain intact.
- `tests/integration/test_validation_diagnostics.py`: synthetic governed runner regressions and direct codec/exception checks.
- `docs/codex/prompts/phase_17hl_diagnostic_hardening.md` and this report: task scope, evidence, and limitations.

| Diagnostic | Rejection stage | Existing public category |
| --- | --- | --- |
| json_decode | JSON parsing | serialization_error |
| duplicate_json_key | Duplicate object key | serialization_error |
| pydantic_validation | StageResult structure/UUID validation | serialization_error |
| canonical_serialization | Dump, round-trip model validation, canonical encoding | serialization_error |
| stage_binding | Stage ID/kind/outcome contract | serialization_error |
| claim_identity | Deterministic ID, duplicate ID, originating stage | serialization_error |
| claim_contract | Non-fact claim with subject | serialization_error |
| evidence_validation | Source reference, lineage, support, qualification | invalid_reference |
| coverage_validation | Missing source/child coverage | extraction_failed |
| response_limit | Raw/canonical byte, collection, text limits | extraction_limit_exceeded |

Internal `evidence_validation_failed` and `coverage_failed` categories remain unchanged. Public names above reflect the actual existing classifier, not a new taxonomy. Provider-side output limits retain their existing InferenceOutputLimitError diagnostics. Successful StageResult values and success audit fields remain unchanged.

## Privacy, safety, and review

The diagnostic is an exact enum member, never an exception string, JSON path, UUID, content fragment, or dynamically constructed label. The runner independently checks its type. Missing or forged string metadata cannot suppress a failure. Existing audit fields are preserved; only the optional fixed identifier is added. No raw response, prompt, evidence, claim, Pydantic details, or exception traceback is added to the audit.

Tests use synthetic keys and identities generated in memory and temporary local authorities. No operator credential, key, JWT, approval packet, consumed approval, or historical audit is used. A temporary pytest plugin denies socket connections and name resolution before collection for regression runs. No live CLI, provider factory operation, cloud operation, deployment, Docker operation, or dependency installation was performed. Azure inference calls: **0**. Commits/pushes: **0**.

Self-review compared phase changes against saved starting files, checked unchanged predicates and normalization, and confirmed the optional diagnostic cannot authorize execution. Pre-commit review found no new runtime secrets, private material, generated artifacts, dependencies, debug statements, or unrelated implementation changes. Synthetic secret markers are deliberate privacy-test inputs. Existing audit writing still uses exclusive creation, no symlink following, mode 0600, file fsync and directory fsync; regression tests verify permissions and refusal to overwrite.

## Validation

- New diagnostic suite, final run: **25 passed in 8.05s**. The initial run had 21 passed and one test-injection failure; the synthetic fault was restricted to StageResult canonicalization, then rerun successfully. No acceptance rule changed to fix the test.
- Broad offline suite: **972 passed, 31 failed, 5 errors in 172.94s**. This run collected the original 22 new cases; the three subsequently added forged/missing-audit cases passed in the final targeted run.
- `ruff check tests/integration/test_validation_diagnostics.py`: passed. `ruff format --check` for that file: passed.
- Ruff on the four existing implementation files: **17 findings**, exactly matching saved pre-task source counts by rule (I001=3, BLE001=7, F401=1, C408=5, S110=1). Their format checks report all four files would be reformatted both before and after this phase. Unrelated formatting/lint cleanup was not performed. The split model-validation catch explicitly preserves the existing broad fail-closed normalization.
- `PYTHONPYCACHEPREFIX=/tmp/polymind-diagnostic-pycache python -m compileall -q documents/digestion governance security llm tests/performance tests/integration/test_validation_diagnostics.py`: passed. Compilation was scoped to the relevant source/test packages; a repository-wide compile and Docker build were not necessary for this additive Python-only change.
- `git diff --check`: passed. `git status --short` and `git diff --stat` were run; the working tree remains dirty with pre-existing work and this uncommitted phase. Git's tracked diff stat includes pre-existing modifications and excludes the already-untracked runner and new test/docs, so it is not a phase-only change count.

Commands for the pytest runs (the temporary plugin blocks external sockets before collection):

```sh
PYTHONPATH=/tmp:. python -m pytest -p polymind_offline_guard tests/integration/test_validation_diagnostics.py -q --disable-warnings
PYTHONPATH=/tmp:. python -m pytest -p polymind_offline_guard tests/integration/test_validation_diagnostics.py tests/unit/documents tests/unit/test_governance*.py tests/unit/test_security*.py tests/unit/test_evaluation*.py tests/unit/test_foundry*.py tests/unit/test_single_call_diagnostics.py tests/unit/test_output_limit_diagnostics.py tests/unit/test_structured_provider.py tests/integration/test_*digestion.py tests/integration/test_single_call*.py tests/integration/test_foundry*.py tests/integration/test_attempt3_serialization.py tests/integration/test_output_limit_hardening.py -q --disable-warnings
```

Failure groups in the broad run:

- 17 managed-inference unit failures and 8 managed-digestion integration failures: older ungoverned fixture paths encounter the existing governed-background requirement.
- 5 Foundry envelope setup errors: capture arrays remain empty in the older Q&A fixture path.
- 1 schema-probe failure: existing generation-contract binding check rejects an outdated expectation.
- 2 legacy launcher failures: expected json_object differs from current strict json_schema output mode.
- 3 output-limit tests: older expectations assume accounting errors replace the primary provider error; existing execution now retains that primary error.

The exact 31 failures and 5 errors were selected for a baseline comparison using a temporary import loader that executes the saved pre-task versions of the four edited files in memory. The loader preserves original module paths and leaves the working tree untouched. Both runs use the same socket-denial plugin. **Baseline comparison: 31 failed, 5 errors in 6.45s, with exactly the same 36 failure/error node IDs.** All broad-suite failures reproduce without this phase's changes. They remain documented and unmodified. The first baseline-selection command truncated a parametrized node ID containing spaces and collected no tests; correcting only that selection produced the comparison above.

## Approval bindings and remaining limits

Executor SHA-256 computed using the runner's existing transitive source hashing algorithm:

- Before this phase: `584ad53eec07266b16c0b5b197972ddf03abc198e859e5133c0f563fe1b7a4b2`
- After this phase: `a93d62df2af1086fb6c2404f7171a9bbb6bd5320a267060728ec945c3357dc9d`

This is an observation of source fingerprints, not modification of any approved configuration. Existing approvals bound to the old executor cannot authorize this code. Schema, generation contract, prompt, profile, budgets, and deterministic IDs were not changed by this phase. Any future live test requires newly prepared and independently authorized bindings; the consumed attempt remains consumed.

Diagnostics identify the first failed validation stage, not the offending field or content. Unexpected non-domain exceptions and pre-validation failures can still have no validation diagnostic. Canonical serialization groups dump/revalidation/encoding failures deliberately. Historical causation remains unknowable from the supplied sanitized audit alone.

## Outcome and recommendation

**Diagnostic hardening: PASS.** All 25 new checks pass, and every failure/error in the broader regression reproduces against the pre-task source. The overall repository regression is not green. Before considering another authorized live test, reconcile those existing fixture/contract failures in a separately scoped offline task and repeat the relevant regression, then prepare fresh executor/configuration approval bindings. This phase provides prospective stage attribution only; it does not establish historical cause or authorize a new attempt.
