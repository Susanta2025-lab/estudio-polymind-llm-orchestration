# CODEX IMPLEMENTATION PROMPT
## ESTUDIO POLYMIND — PHASE 17H–L: FULL-SUITE TEST CONFIGURATION ISOLATION & RECONCILIATION

Clean Markdown task record of the externally supplied implementation prompt.

## Operator workflow and repository context

Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`.
Expected branch: `master`. Work directly on that branch; do not create or switch
branches. Execution model requested: GPT-6.1-Sol, High reasoning.

Task: offline test infrastructure hardening, fixture reconciliation,
implementation, verification and independent review within Phase 17H–L Azure
Foundry L1 evaluation and document-intelligence reliability validation.

Previous results:

- Offline diagnostic hardening: PASS, 25 sanitized diagnostic regressions;
  strict StageResult/evidence validation and financial safeguards preserved.
- Offline regression reconciliation: PASS, all 36 previous failures/errors fixed
  through fixture/expectation reconciliation, 1,013 selected tests passed.
- Offline E2E contract verification: PASS within scope, 31 new integration tests,
  synthetic four-call L1 execution, analysis/two reductions/root digest,
  publication/retrieval, grounded Q&A/citations, provenance/persistence,
  governance/accounting and corrected CLI failure exit status. Selected regression:
  1,044 passed. This does not establish successful real-model inference.

**Phase 17H overall remains PARTIAL. Do not initiate a fifth Azure Foundry live
experiment.**

Historical full-suite results:

| Run | Collected | Passed | Failed | Setup errors | Skipped | Network attempts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Ordinary implicit operator dotenv | 1380 | 1316 | 56 | 8 | 0 | 0 |
| Temporary synthetic-settings isolation | 1380 | 1380 | 0 | 0 | 0 | 0 |

The temporary mechanism prevented implicit repository-root `.env` loading during
test Settings construction; it did not disable governance, change production
configuration or skip tests. All 64 failures/errors reproduced with the pre-E2E
launcher implementation. Verify the hypothesis that older standalone fixtures
inherit operator OIDC/governed configuration against actual code/evidence.

## Objective and scope

Make `python -m pytest -q` reproducible without an external temporary
settings-isolation plugin: all 1,380 existing cases plus justified new tests,
zero failures/errors/unexpected skips/unauthorized network attempts.

This is a test-only fixture-isolation task. Permitted changes: pytest
configuration, test fixtures/helpers/modules/startup hooks, isolation regression
tests, test configuration documentation and this phase's prompt/report.
Do not change production modules unless an independently established production
defect requires it; document the root cause and classify PARTIAL/BLOCKED instead
of silently expanding scope. Do not edit AGENTS.md to accommodate a different
model. Prefer one narrow shared boundary over repairing 64 tests independently.

Historical affected groups (recover exact node IDs or reproduce):

| Area | Cases |
| --- | ---: |
| Publication analysis | 10 |
| Publication API | 2 |
| Lifecycle | 16 |
| Load | 2 |
| Planning | 9 |
| Retrieval | 6 |
| Security | 6 |
| Workflow | 1 |
| Legacy API reliability | 2 |
| Memory integration | 1 |
| Retrieval regression | 1 |
| Streaming | 8 |
| Total | 64 |

## Git and safety requirements

Read AGENTS.md before implementation. Inspect actual branch, HEAD and working
tree; do not assume historical checkpoints are current. Run and record:

```sh
git status --short --branch
git rev-parse HEAD
git diff --check
git diff --stat
git diff --cached --name-only
```

Preserve all tracked/untracked work and historical reports/audits. Do not commit,
push, merge, rebase, reset, stash, clean, restore, discard or stage files.
Do not modify operator `.env` or private configuration. Do not inspect credential
or secret values, private approvals, keys, JWTs or historical response material.

Prohibited: Azure Foundry or other live inference; AKS startup; container
deployment; cloud provisioning/modification; RSA operator signing; creating or
consuming live approvals; paid services; automatic inference retries. All
experiments remain local, deterministic and offline. Synthetic identities,
temporary authorities, fake responses and test-generated keys are test fixtures,
not operator authorization.

Activate network denial before collection/import. Unexpected attempts must fail
the run even when an application catches the network exception. The established
network-denial guard may remain explicit and separate from settings isolation.
Never run genuine live integrations merely because they are discoverable.

## Required assessment

Read and verify actual paths for:

- AGENTS.md and current architecture documentation.
- `docs/codex/reports/phase_17hl_diagnostic_hardening.md`.
- `docs/codex/reports/phase_17hl_regression_reconciliation.md`.
- `docs/codex/reports/phase_17hl_offline_e2e_contract_verification.md`.
- Current security/governance configuration and test configuration documentation.

Inspect `pytest.ini`, `pyproject.toml` and `tests/conftest.py` where present.
Locate Pydantic Settings definitions, validation, implicit/explicit dotenv
loading, environment precedence, OIDC, standalone/governed-background modes,
identity/authority helpers, overrides, import-time construction, cached Settings,
pytest startup/collection hooks and all consumers. Search for `Settings(...)`,
`get_settings(...)`, `lru_cache`, `env_file`, `DotEnvSettingsSource`, `OIDC`,
`governed`, `standalone`, and `monkeypatch`. Never print/read secret values.

Reproduce the current complete configured suite under pre-collection network
denial. Recover all 64 node IDs from retained evidence or reproduction. Record
differences if the inventory changed. For each group trace settings timing,
configuration source, intended execution mode, missing fixture selection,
caching, collection/setup/execution failure stage and suitability of a shared fix.

The proposed leak remains a hypothesis until verified:

```text
Pytest startup -> collection/import -> Settings construction
-> implicit repository .env -> operator OIDC/governance mode
-> standalone fixture -> unexpected authorization/preparation rejection
```

## Non-negotiable behavioral boundaries

Production defaults, normal environment precedence, OIDC, authentication,
authorization, tenant/owner isolation, governance policy, provider admission,
accounting, quotas and Azure deployment configuration must remain unchanged.
Do not globally force authentication/governance/authorization off.

Preserve strict StageResult validation, deterministic claim IDs, coverage,
provenance, lineage, hierarchical digestion, structured-output policy, byte
limits, canonical serialization and sanitized diagnostics.

Preserve reservation/settlement, known provider error precedence, unknown-usage
fail-closed behavior, replay protection, single-call boundaries and immutable
financial records. Do not touch real accounting records.

Intentional OIDC/token/credential-negative tests, authorization denial,
revocation, environment/explicit dotenv tests, settings precedence/validation,
governed-background execution and security errors must remain meaningful.
Do not skip, xfail, delete, weaken assertions, return unconditional authorization
success, suppress exceptions globally, mutate production settings to match tests,
or alter collection to hide cases. Document any genuinely obsolete expectation
and retain equivalent behavioral coverage.

## Durable isolation implementation

Use an established pytest boundary active early enough for collection-time
Settings construction. Function-scoped fixtures run too late. Scope it strictly
to tests and document installation/removal. Prefer supported public configuration
inputs over private dependency monkeypatches. If private behavior is unavoidable,
isolate it in a tested adapter and verify the installed dependency version.

| Source | Required behavior |
| --- | --- |
| Implicit operator `.env` | Ignored for ordinary tests |
| Explicit synthetic environment variables | Preserved |
| Explicit synthetic env files | Preserved |
| Settings defaults and validators | Preserved |
| Explicit per-test overrides | Preserved |
| Synthetic OIDC/governed configuration | Preserved |
| Production execution outside pytest | Unchanged |

Genuine standalone publication/API/lifecycle/planning/retrieval/streaming/memory/
workflow fixtures use synthetic standalone settings without real credentials or
network dependencies. Governed/security fixtures retain synthetic authenticated
identities, explicit owner/tenant scope, grants/revocation, GovernedExecution,
provider admission, quota/financial state. Unauthorized, revoked, cross-tenant
and missing-admission paths still reject.

Add regressions for:

1. Implicit operator dotenv cannot affect ordinary Settings.
2. Explicit synthetic environment variables remain effective.
3. Explicit synthetic env files remain readable.
4. Defaults remain intact.
5. Validators reject invalid inputs.
6. OIDC can be explicitly activated.
7. GovernedExecution remains enforceable.
8. Unauthorized standalone-to-governed transitions fail closed.
9. Settings caches do not contaminate unrelated tests.
10. Production settings outside the isolation boundary remain unchanged.
11. Isolation precedes collection-time Settings initialization.
12. The mechanism needs no secret access.

Use temporary synthetic files and sentinel values; never copy/parse real dotenv.
Check contrasting scenarios: standalone defaults; synthetic governed/OIDC-like
implicit operator settings; explicit governed settings; explicit synthetic dotenv.

## Validation and review

Run focused isolation tests (positive/negative, import/runtime), all 64 recovered
node IDs, security/governance suites (OIDC, grants, revocation, GovernedExecution,
provider quota, accounting, replay, tenant isolation), the established 1,044-case
selected suite and full normal configured suite. Retain 25 diagnostics, all 36
previously reconciled cases and all 31 L1 E2E cases. Verify four-interaction L1,
StageResult/evidence, two reductions, digest, publication/retrieval, Q&A/citations,
governance/accounting and CLI exit behavior. Record exact collection/pass/fail/
error/skip counts. Contrast synthetic configurations where feasible.

Run `git diff --check`, applicable Ruff lint/format checks, compilation with an
external bytecode cache if needed, and collection checks. Compare existing lint/
format findings with baseline; no unrelated formatting cleanup. Do not claim a
check passed without running it. No Docker/deployment work is needed here.

Perform implementation self-review and separate independent review: import-time
leaks, caches, restoration, explicit overrides, private API fragility, order
independence, security-negative coverage, missing calls, financial/evidence/
publication false positives, production startup isolation (FastAPI/Streamlit/
workers/Foundry/Docker/Kubernetes), secrets, dependencies, artifacts and scope.
Fix meaningful findings.

Perform a separate pre-commit review without committing. Repeat starting Git
commands. Distinguish new work from existing dirty files; confirm production
modules/operator dotenv/historical audits untouched by this task, no private
approvals accessed, no staging/unrelated changes and all existing work preserved.

## Acceptance and reporting

PASS requires reconciliation of all 56 failures and 8 errors; a green normal
suite with 1,380 existing tests plus justified additions; no temporary settings
plugin; no implicit dotenv contamination; explicit source/validation/security/
governance/accounting coverage retained; all historical selected regressions
green; no hidden tests; no network/provider/cloud/approval/Git mutations; quality
checks pass or unchanged debt documented; complete implementation report.

PARTIAL: improvements with remaining original failures, non-green normal suite,
source coupling, weakened security coverage or important unverified boundaries.
BLOCKED: essential unavailable dependencies, architectural decision or prohibited
external access. FAIL: concealed failures, weakened security or unresolved new
regressions. Never declare PASS by disabling security or hiding tests.

Save this prompt and report at:

- `docs/codex/prompts/phase_17hl_full_suite_configuration_isolation.md`.
- `docs/codex/reports/phase_17hl_full_suite_configuration_isolation.md`.

Report: executive result; starting branch/HEAD/dirty/staged state; historical and
reproduced baseline; source/timing/cache/fixture root cause without secret values;
design/lifecycle/explicit sources/negative tests/compatibility; full 64-row matrix
(node ID, original classification, verified cause, correction, final outcome);
focused/64-case/selected/full/matrix/security/governance/lint/compile/network
evidence; production isolation; self-review/pre-commit findings; limitations.

Final response fields requested: PHASE/TASK; OVERALL RESULT; STARTING STATE
(branch/HEAD/tree); HISTORICAL BASELINE (1380/1316/56/8); CONFIGURATION ROOT CAUSE
(dotenv/collection/caching/groups); IMPLEMENTATION (mechanism/created/modified/
production files/explicit env and dotenv); RECONCILIATION (X/56, X/8, X/64);
VERIFICATION (new/diagnostic/36/31/selected/full/matrix/security/governance/Ruff/
compile/diff); SAFETY (production/dotenv/authentication/authorization/financial
controls/network/provider/cloud/approvals/commits/pushes); REMAINING FAILURES;
KNOWN LIMITATIONS; REPORT PATH; NEXT RECOMMENDED TASK.

If PASS, recommend **Phase 17H–L — Final Offline Azure Strict-Schema and
Application-Validator Compatibility Audit**, analyzing provider-structurally-valid
responses rejected by application validation without live inference. Do not begin
that separately scoped task. Phase 17H remains PARTIAL.
