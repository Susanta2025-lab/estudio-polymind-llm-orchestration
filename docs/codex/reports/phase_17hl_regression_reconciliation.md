# Phase 17H–L: offline regression baseline reconciliation

## Scope and baseline

The branch was verified as `master`; no branch was created or switched. The starting tree contained substantial tracked and untracked work, including the previous validation diagnostic implementation. Only six existing test modules and this phase's prompt/report were changed. Baseline copies of those six test files were saved outside the repository for phase-specific review.

The previous diagnostic report and its retained offline logs establish 31 failing tests and five setup errors, all reproduced against the earlier implementation. This task reconciles those tests with the current application contracts. It does not assess real model quality, establish historical failure causation, authorize another inference attempt, or declare Phase 17H passed.

## Findings and changes

| Baseline cases | Cause | Reconciliation |
| --- | --- | --- |
| 17 managed-inference unit failures | The standalone adapter tests inherited local governed-mode settings without supplying a governed execution context. | A module-local, automatically restored fixture supplies an explicit synthetic standalone setting. A new negative test enables governed mode and verifies refusal before provider execution or admission. |
| 8 managed-digestion integration failures | The older durable pipeline tests had the same implicit runtime-setting dependency. | A module-local fixture selects the supported standalone adapter path. Governed digestion tests retain their real synthetic authority, governance ledger, and admission composition. |
| 5 envelope setup errors | Render-only Q&A fixtures inherited OIDC mode, failed before rendering, and then indexed an empty capture array. | The envelope fixture explicitly supplies synthetic standalone renderer settings inside a temporary MonkeyPatch context. Its fake replica/provider and all envelope, coverage, and byte-limit assertions remain intact. |
| 1 schema-probe failure | The positive preparation test used a historical generation fingerprint that correctly rejects current code. | Bind only the synthetic positive test to the current generation hash. Keep the production historical constant unchanged and add a negative test proving stale preparation still fails before creating output. |
| 2 legacy launcher failures | Tests expected JSON-object mode for every call, although digestion now uses strict JSON Schema. | Assert the exact strict converted StageResult schema for the three digestion calls, and retain the exact JSON-object assertion for interactive Q&A. |
| 3 output-limit failures | Tests expected cleanup/accounting failures to replace the primary provider error and assumed settlement failure prevents admission finalization. | Assert the preserved `inference_output_limit` category while retaining separate UNKNOWN/STARTED/SETTLED ledger-state checks. Admission finalization is expected for successful usage accounting even when governance settlement fails. |

Changed tests:

- `tests/unit/documents/test_managed_inference.py`
- `tests/integration/test_managed_digestion.py`
- `tests/unit/test_foundry_30k.py`
- `tests/unit/test_foundry_schema_probe.py`
- `tests/integration/test_foundry_l1_launcher.py`
- `tests/integration/test_output_limit_hardening.py`

The setting overrides replace only the imported settings reference inside the selected tests, with pytest restoring it afterward. No `.env`, deployed configuration, security policy, or runtime implementation was edited. The independent governed integration and security suites continue to exercise authorization and accounting. No test was skipped, removed, xfailed, or relaxed to accept multiple incompatible categories.

## Verification

- Initial rerun of the exact 36 cases: **34 passed, 2 failed in 22.15s**. The remaining two exposed the digestion/Q&A schema-mode distinction; the final assertion checks both exact contracts.
- Final focused follow-up after strengthening independent schema-drift checks: **9 passed in 0.49s** (all schema-probe tests plus the new governed-mode refusal test).
- Exact 36 previously failing/error cases, final rerun: **36 passed in 25.11s**.
- Broad offline regression: **1013 passed in 168.17s**, with **0 failures and 0 errors**. This includes all 25 diagnostic-hardening cases and the governed digestion, security, governance, accounting, single-call, and approval/replay tests.
- Ruff: **70 pre-existing findings**, with identical rule counts before and after this phase. No new findings remain. Both baseline and current formatting checks report all six files would be reformatted; unrelated whole-file reformatting was left out of scope.
- Scoped `compileall` with `PYTHONPYCACHEPREFIX=/tmp/polymind-reconciliation-pycache`: passed for all six changed test modules.
- `git diff --check`: passed. `git status --short` and `git diff --stat` were run; the tree remains dirty, with existing work preserved and this phase uncommitted.

The broad command repeats the diagnostic-hardening regression selection with the three final diagnostic cases and two new negative tests included:

```sh
PYTHONPATH=/tmp:. python -m pytest -p polymind_offline_guard tests/integration/test_validation_diagnostics.py tests/unit/documents tests/unit/test_governance*.py tests/unit/test_security*.py tests/unit/test_evaluation*.py tests/unit/test_foundry*.py tests/unit/test_single_call_diagnostics.py tests/unit/test_output_limit_diagnostics.py tests/unit/test_structured_provider.py tests/integration/test_*digestion.py tests/integration/test_single_call*.py tests/integration/test_foundry*.py tests/integration/test_attempt3_serialization.py tests/integration/test_output_limit_hardening.py -q --disable-warnings
```

The temporary offline plugin blocks socket connections and name resolution before collection. All provider results are synthetic. No live CLI was invoked. Synthetic identity/approval fixtures create their own test keys in memory; no operator keys, credentials, JWTs, or private approval packets were read.

## Review and compatibility

Self-review used diffs against the saved starting versions of the six files, preserving previous uncommitted work. Assertions still cover full source coverage, all child lineage, byte budgets, claim/evidence rejection, retries and fencing, accounting outcomes, immutable audit output, and approval consumption. The launcher now checks schema contents rather than merely accepting a format label. The two new negative tests protect the controls most likely to be obscured by test-only configuration isolation.

Pre-commit review found no new dependencies, production API changes, secrets, generated runtime artifacts, approval changes, or unrelated implementation changes. Test settings are deliberately synthetic; output-limit privacy markers and synthetic credentials already used by the existing tests remain test-only. Historical audit, approved configuration and consumption evidence were not modified. The previous diagnostic report remains unchanged.

Ruff and formatting results are compared with the saved pre-task files, without broad unrelated formatting cleanup. Docker/build/deployment validation is unnecessary for this tests-only change and was not performed.

## Fingerprints, safety and remaining scope

The executor fingerprint remains `a93d62df2af1086fb6c2404f7171a9bbb6bd5320a267060728ec945c3357dc9d`: this task changes no source included in the executor or generation-contract bindings. It does not revalidate older approvals invalidated by previous implementation changes. The historical schema-probe generation constant remains stale and fail-closed by design.

This is a selected offline regression, not the entire repository suite. Render-only envelope tests explicitly select standalone mode; direct execution of the legacy envelope utility under an operator OIDC configuration is not certified by these tests. No new live execution is authorized. A future live attempt still requires separate review and fresh configuration/approval bindings under the existing controls.

Azure/provider inference calls: **0**. Cloud modifications: **0**. Commits: **0**. Pushes: **0**. No dependency installation or branch changes occurred.

## Outcome

**Offline regression baseline reconciliation: PASS.** All 36 identified failures/errors are reconciled, and the selected 1013-test offline suite is green. The historical approval binding remains blocked, and no production implementation or diagnostic behavior changed. This does not declare the entire repository regression green or Phase 17H complete. Any decision about another live test remains a separate operator-authorized step.
