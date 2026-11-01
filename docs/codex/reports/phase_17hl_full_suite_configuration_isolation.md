# Phase 17H–L — Full-Suite Test Configuration Isolation & Reconciliation

## Executive result

**PASS for test configuration isolation and reconciliation.** The normal configured
repository-root invocation passes **1,403 tests: the original 1,380 plus 23 new
isolation cases**, with zero failures, setup/collection errors, skips, xfails or
observed network attempts. No external settings-isolation plugin is needed.
The network-denial plugin remains an explicit, separate verification safeguard.

**Phase 17H overall remains PARTIAL.** This is deterministic offline evidence,
not successful real-model inference or authorization for another experiment.
No fifth Azure Foundry experiment, next-phase audit, cloud operation, operator signing,
operator approval consumption, commit or push was performed.

## Starting state and assessment

The branch was `master`, HEAD `af4a7a076c918ef13aea05d74bf239c0af909133`.
The starting index was empty. `git status --short --branch` recorded **20 modified
tracked paths and 83 untracked entries** (directory entries can contain multiple
files). The tracked diff was **607 insertions / 71 deletions across 20 files**.
`git diff --check` passed. The prior report's 80-entry untracked count predates its
three E2E artifacts; the actual current baseline was verified instead of assumed.

Before implementation, SHA-256 fingerprints of all **368 pre-existing nonignored
repository files** were retained under `/tmp/polymind-config-isolation/` together
with starting status. This inventory uses Git's tracked/nonignored path list and
excludes ignored private configuration/storage. It is not a hash or inspection
of operator dotenv, credentials, approval packets or authority databases.

Required reading included AGENTS.md, README architecture/testing documentation,
production security and Phase 17G configuration documentation, reusable evaluation
policy, all three requested diagnostic/reconciliation/E2E reports, pytest.ini,
Settings and its consumers, publication/analysis fixtures, graph/API/memory/
streaming code, security configuration/authority tests and actual Pydantic source.
There was no root test conftest or repository pyproject.toml at baseline.
Dependencies already installed: pydantic-settings **2.14.1** (pinned in
requirements.txt), pytest **8.4.2**; no installation was needed.

### Reproduced baseline

| Run | Collected | Passed | Failed | Errors | Skipped | Network attempts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Historical ordinary dotenv run | 1380 | 1316 | 56 | 8 | 0 | 0 |
| Historical temporary-isolated run | 1380 | 1380 | 0 | 0 | 0 | 0 |
| Current pre-change reproduction | 1380 | 1316 | 56 | 8 | 0 | 0 |
| Normal permanent-isolation run | 1403 | 1403 | 0 | 0 | 0 | 0 |

The current reproduction took **215.82 s** (42 warnings). Its 64 failure/error
node IDs exactly equal the retained historical inventory at
`/tmp/phase17hl-e2e-full-failures.json`; no cases disappeared or changed category.
The current eight errors were fixture setup errors, not import/collection errors.
JUnit evidence is `/tmp/polymind-config-isolation/baseline.xml` and
`reconciled.xml`; this report durably includes the complete node inventory below.

## Verified root cause

The leak is **implicit dotenv configuration at first import**, followed by shared
module references. `config/settings.py` declares `env_file=".env"` and eagerly
executes `settings = Settings()` at module end. Pydantic normally reads this path
relative to the working directory; constructor values precede exported environment
variables, then dotenv, then defaults. Many tests construct fresh Settings with
`_env_file=None`, but that does not replace the eagerly initialized singleton
already imported by graph/API/publication consumers. There is no application
`get_settings`/`lru_cache` Settings factory to clear. Caching here means the module
singleton and references/default arguments retaining that same object.

The source-level paths and sanitized baseline failures establish that the implicit
configuration activated OIDC behavior (`API_AUTH_MODE` / `authentication_mode`)
and its required governed configuration (`GOVERNANCE_ENABLED`). No actual operator
values, OIDC JSON, credentials, paths, policies or pricing were dumped or inspected.
The causal comparison changes only omitted dotenv input, leaves environment and
validators intact, and converts the exact 64 failing/error cases to passes.
Contrasting synthetic files independently verify this source boundary.

Construction happens **during collection/import**, before function fixtures.
Most failures then occur **during test execution** when standalone fixture helpers
call publication administration, document analysis, legacy graph/API/persistence
or streaming. Security/load failures occur **during fixture setup**, because
`secure_publication` first prepares a synthetic standalone publication before
building the real AuthorizedAnalysis service. It lacks an OIDC publication
administration context at that preparation stage. Therefore those eight errors
prevented the intended security assertions from running at all.

| Code | Verified boundary and affected purpose |
| --- | --- |
| P1 | `PublicationService._manage` rejects standalone plan/prepare/activate/lifecycle work under implicit OIDC; affects analysis, lifecycle, planning, retrieval and workflow preparation. |
| P2 | The same publication management rejection occurs inside `secure_publication`, producing six security and two load setup errors before authorized execution. |
| A1 | `analyze_documents` chooses the authenticated route and requires a principal/runtime instead of the standalone injected service. |
| A2 | API readiness adds an unavailable security runtime gate, defeating otherwise ready dependency fakes. |
| L1 | `legacy_query_guard` correctly refuses the legacy query path in OIDC mode. |
| L2 | `graph.generation._legacy_only` correctly rejects standalone retrieval/prompt/persistence using the imported singleton. |
| L3 | Streaming calls the same legacy guard before routing/provider/memory; its existing generic sanitized error changes the expected events and call counts. |

These are valid production protections exercised under unintended fixture
configuration, not defects to remove from production. The historical grouping is
complete and unchanged: 56 failures plus eight setup errors across 12 test modules.

## Implemented solution

This task **adds six files and modifies no pre-existing file**:

- `tests/conftest.py`: installs isolation at conftest import, before collection;
  restores the constructor via `pytest_unconfigure`, even after collection errors.
- `tests/settings_isolation.py`: narrow adapter around public `BaseSettings.__init__`.
- `tests/unit/test_settings_isolation.py`: 23 synthetic regression cases.
- `tests/README.md`: normal command, lifecycle, explicit sources and boundaries.
- This implementation report and the matching clean Markdown prompt record.

The adapter identifies the application Settings model by module/class in its MRO
without importing it first. Only **omitted** `_env_file` input becomes the supported
public `_env_file=None`. All application Settings subclasses receive the same
implicit-source policy. Other BaseSettings models are forwarded unchanged.
`inspect.signature(...).bind_partial` distinguishes omitted from explicit keyword
or positional input; `functools.wraps` preserves introspection. No model_config,
validator, settings value, environment variable or private source reader changes.

The public source-customization hook is not sufficient for the no-read boundary
in the pinned Pydantic version: the dotenv source is constructed (and reads its
file) before `settings_customise_sources` is called. Changing Settings.model_config
after importing the module would likewise be too late for its singleton. The
constructor adapter avoids both problems and the historical private-reader patch.

Explicit `_env_file=path`, `_env_file=None`, controlled files named `.env`, ordinary
synthetic environment variables and constructor overrides keep their normal
precedence. Complete OIDC/governed settings remain loadable by environment and
explicit dotenv; invalid/incomplete settings still reject. The isolation tests
also prove positional `_env_file`, unrelated settings models, inherited Settings,
constructor restoration, collection failure cleanup and module-singleton stability.

A settings import by an external pytest startup plugin **before** the conftest is
reported as `pytest.UsageError`. It cannot silently retain an earlier polluted
singleton. No external plugin is needed by the normal suite. There is no global
security-off assignment: ordinary tests receive original defaults while explicit
security/governance fixtures retain their chosen configuration and real controls.

### Security-negative and production checks

The new tests exercise real restricted-provider denial for generate/stream/execute,
a real GovernedExecution financial rejection with zero provider calls/reservations,
and protected analysis denial before data/provider sentinels. The executor's
financial authority is independently enforced; settings do not dynamically switch
that executor's policy. Existing security tests continue to use real synthetic
principals, owner/tenant scopes, grants, revalidation and revocation. They now
reach their assertions instead of failing during preparation.

Synthetic child processes copy only the exact public Settings/conftest/adapter
source, create their own dotenv, and install socket/DNS denial before application
imports. They prove collection-time Settings and singleton construction ignore
implicit values, teardown restores the constructor after success and collection
failure, a preloaded singleton is reported, and normal imports outside pytest
continue loading a synthetic implicit dotenv. No operator file is required by
these regressions. Production source hashes are unchanged. Fresh FastAPI,
Streamlit, worker, Docker and cloud runtime imports do not import this conftest.

## Verification evidence

| Check | Result |
| --- | --- |
| Focused isolation, final reviewed source | **23 passed**, 2.71 s; no failures/errors/skips/network attempts |
| Reversed new-case order with exported `MEMORY_HISTORY=61` | **23 passed**, 2.83 s; explicit environment preserved and restored |
| Original failing tests | **56/56 reconciled** |
| Original setup errors | **8/8 reconciled** |
| Exact 64-case standalone rerun | **64 passed**, 28.21 s |
| Same 64 with synthetic standalone implicit dotenv | **64 passed**, 110.79 s |
| Same 64 with complete synthetic OIDC/governed implicit dotenv | **64 passed**, 77.08 s |
| Established selected offline regression | **1044 passed**, 35 warnings, 292.60 s |
| Diagnostic-hardening cases in selected/full JUnit | **25/25 passed** |
| Exact previous reconciliation inventory in selected/full JUnit | **36/36 passed** |
| Actual L1 E2E integration cases in selected/full JUnit | **31/31 passed** |
| Normal configured root invocation | **1403 passed**, 42 warnings, 412.92 s |
| Full synthetic-governed confirmation | **1403 passed**, 42 warnings, 396.84 s; zero network attempts |
| Collection-only | **1403 collected**, 8.63 s, zero collection errors |
| Unit OIDC/security modules in normal full suite | **177 passed** |
| Publication security/load cases in normal full suite | **8 passed** |
| Governance/migration/evaluation unit modules in normal full suite | **47 passed** |
| Single-call harness/preflight integration modules | **74 passed** |
| Ruff on all three new Python files | PASS, zero findings |
| Ruff formatting on all three new Python files | PASS, three already formatted |
| Repository compilation with external bytecode cache | PASS, exit 0 |
| Git diff check | PASS |

These security/governance subsets overlap the broad suite; they are not additional
tests. Provider admission, known-error precedence, UNKNOWN reservations, settlement,
replay and owner/tenant controls remain covered by the unchanged managed inference,
governance, evaluation, single-call and E2E suites. The 31 E2E cases still exercise
four synthetic interactions, both hierarchical reductions, strict StageResult and
evidence acceptance/rejection, durable digest/publication/retrieval, grounded Q&A,
citations, accounting and CLI success/failure exit reporting. No assertions were
weakened and no existing test was edited, removed, skipped or xfailed.

### Commands and offline safeguard

The network-only plugin `/tmp/polymind_e2e_offline_guard.py` was retained from the
previous task and inspected before use. It replaces socket connect/connect_ex/
sendto and DNS entry points before collection, adds a CPython socket/DNS audit
hook, counts attempts and makes the session fail even for swallowed exceptions.
It performs **no Settings patch**. All completed verification runs report zero
network attempts; new child regressions maintain their own denial/attempt checks.
Existing subprocess workflows use their own pre-import denial. This is Python
socket/DNS verification, not a claim of an OS-wide network policy for arbitrary
external programs; the discovered Helm calls only lint/render local templates.

Baseline (before adding conftest) used:

```sh
PYTHONPATH=/tmp:. python -m pytest -p polymind_e2e_offline_guard -q --tb=no \
  --junitxml=/tmp/polymind-config-isolation/baseline.xml
```

The normal invocation used the standard command with network-only safeguard and
JUnit reporting selected through pytest environment settings:

```sh
PYTHONPATH=/tmp:. \
PYTEST_PLUGINS=polymind_e2e_offline_guard \
PYTEST_ADDOPTS=--junitxml=/tmp/polymind-config-isolation/full-normal.xml \
python -m pytest -q
```

The exact 64 nodes came from the inventory below and were passed as individual
subprocess argv entries (preserving spaces in parametrized IDs). The established
selected command was:

```sh
PYTHONPATH=/tmp:. python -m pytest -p polymind_e2e_offline_guard \
 tests/integration/test_validation_diagnostics.py tests/unit/documents \
 tests/unit/test_governance*.py tests/unit/test_security*.py \
 tests/unit/test_evaluation*.py tests/unit/test_foundry*.py \
 tests/unit/test_single_call_diagnostics.py tests/unit/test_output_limit_diagnostics.py \
 tests/unit/test_structured_provider.py tests/integration/test_*digestion.py \
 tests/integration/test_single_call*.py tests/integration/test_foundry*.py \
 tests/integration/test_attempt3_serialization.py \
 tests/integration/test_output_limit_hardening.py \
 tests/integration/test_phase17hl_offline_e2e.py -q \
 --junitxml=/tmp/polymind-config-isolation/selected.xml

ruff check tests/conftest.py tests/settings_isolation.py tests/unit/test_settings_isolation.py
ruff format --check tests/conftest.py tests/settings_isolation.py tests/unit/test_settings_isolation.py
PYTHONPYCACHEPREFIX=/tmp/polymind-config-isolation/pycache python -m compileall -q .
git diff --check
```

### Contrasting configuration matrix and experiment corrections

A temporary standalone working directory held synthetic `MEMORY_HISTORY` and
standalone-mode dotenv values. Another held a complete synthetic OIDC/governance
configuration generated from the existing public test helper, using only temporary
paths and test policies. Both exact 64-case runs passed. Explicit OIDC and explicit
synthetic dotenv are tested independently among the 23 new cases, including invalid
configurations; this distinguishes intentional configuration from ignored implicit
configuration. New-case reverse-order testing also preserves a deliberately
exported sentinel without polluting subsequent construction.

An initial optional alternate-directory full-suite launch used the directory's
other pyenv interpreter and encountered 19 dependency collection errors. No
installation was attempted. Re-running with the repository's already-installed
absolute interpreter removed that launch mismatch. The wider run then exposed
pre-existing relative fixture paths and was interrupted (exit 130); a focused
probe reproduced `FileNotFoundError: tests/fixtures/phase17h/quality.json`, with
zero network attempts. This was a working-directory experiment, not the supported
root invocation or a configuration-isolation regression. A temporary `tests`
symlink to the public test tree supplies those fixture paths without modifying
repository files. The completed final contrasting result is recorded below.

**Full contrasting governed confirmation: 1,403 passed, 42 warnings, 396.84 s;
zero failures, errors, skips or network attempts.** Evidence:
`/tmp/polymind-config-isolation/full-synthetic-governed-with-fixtures.xml`.
It used the same already-installed interpreter as the root run, the repository
pytest.ini/test paths, the temporary public-fixture symlink and only the network
guard. The permanent conftest adapter supplies isolation; there is no temporary
settings override. The final reviewed source was exercised by this full rerun.

The equivalent command from the synthetic directory is:

```sh
PYTHONPATH=/tmp:<repository> \
PYTEST_PLUGINS=polymind_e2e_offline_guard \
PYTEST_ADDOPTS=--junitxml=/tmp/polymind-config-isolation/full-synthetic-governed-with-fixtures.xml \
<same-test-python> -m pytest -q -c <repository>/pytest.ini <repository>/tests
```

### Existing quality debt

Ruff evaluated the **211 pre-task Python paths**, whose bytes remain identical
to the starting fingerprints: **752 existing findings**. The three new Python
files add **zero**. This is broader than historical reports' six-file lint sample,
so its count is not compared numerically with that narrower sample. Starting and
current inputs for the 211-file comparison are byte-identical; no unrelated lint
or formatting cleanup was performed. Compilation succeeded for the repository
using an external cache, avoiding ownership changes. Docker, deployment and cloud
checks are inapplicable to this test-only change and were not run.

## Complete historical failure inventory

Correction **T1** in every row is the shared early pytest constructor adapter:
omitted dotenv input is `None`; no per-test production bypass or weakened assertion.
Root-cause codes refer to the verified boundaries above. Every row passed in the
focused 64-case run, the normal full suite and both 64-case synthetic contrasts.

| Node ID | Original classification | Verified root cause | Correction | Final outcome |
| --- | --- | --- | --- | --- |
| `tests/unit/publication/test_analysis.py::test_selected_document_canonical_citations_not_semantic_certification` | analysis; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_analysis.py::test_forged_citation_rejected[foreign]` | analysis; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_analysis.py::test_forged_citation_rejected[C999]` | analysis; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_analysis.py::test_forged_citation_rejected[other-document-page-2]` | analysis; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_analysis.py::test_prompt_injection_remains_data_and_no_tools` | analysis; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_analysis.py::test_no_evidence_skips_inference_and_multiple_scope_allowed` | analysis; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_analysis.py::test_revoked_selection_cannot_analyze` | analysis; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_analysis.py::test_context_overflow_rejected_without_truncating_annotations` | analysis; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_analysis.py::test_qualifications_and_both_conflicting_propositions_retained` | analysis; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_analysis.py::test_pdf_uses_canonical_physical_page` | analysis; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_api.py::test_api_additive_route_and_unconfigured_failure` | api; failure | A1: implicit OIDC enters authenticated document endpoint | T1 | PASS |
| `tests/unit/publication/test_api.py::test_stale_publication_replica_health_and_readiness` | api; failure | A2: implicit OIDC adds unavailable security readiness gate | T1 | PASS |
| `tests/unit/publication/test_lifecycle.py::test_concurrent_candidates_fencing_retry_and_aba` | lifecycle; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_lifecycle.py::test_durable_crash_resume[before_writes]` | lifecycle; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_lifecycle.py::test_durable_crash_resume[after_write]` | lifecycle; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_lifecycle.py::test_durable_crash_resume[after_writes]` | lifecycle; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_lifecycle.py::test_durable_crash_resume[after_validation]` | lifecycle; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_lifecycle.py::test_durable_crash_resume[before_activation]` | lifecycle; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_lifecycle.py::test_durable_crash_resume[after_activation]` | lifecycle; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_lifecycle.py::test_failed_supersession_and_orphan_detection` | lifecycle; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_lifecycle.py::test_revocation_rollback_interruption[before_activation-revocation]` | lifecycle; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_lifecycle.py::test_revocation_rollback_interruption[before_activation-rollback]` | lifecycle; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_lifecycle.py::test_revocation_rollback_interruption[after_activation-revocation]` | lifecycle; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_lifecycle.py::test_revocation_rollback_interruption[after_activation-rollback]` | lifecycle; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_lifecycle.py::test_rollback_revalidates_inventory_and_provenance[dense]` | lifecycle; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_lifecycle.py::test_rollback_revalidates_inventory_and_provenance[source]` | lifecycle; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_lifecycle.py::test_rollback_revalidates_inventory_and_provenance[manifest]` | lifecycle; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_lifecycle.py::test_rollback_revalidates_inventory_and_provenance[digest]` | lifecycle; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_phase17h_load.py::test_concurrent_owner_shared_and_cross_tenant_with_fresh_revoker[revoke]` | phase17h_load; setup error | P2: secure_publication fixture fails at standalone publication plan before protected assertions | T1 | PASS |
| `tests/unit/publication/test_phase17h_load.py::test_concurrent_owner_shared_and_cross_tenant_with_fresh_revoker[tombstone]` | phase17h_load; setup error | P2: secure_publication fixture fails at standalone publication plan before protected assertions | T1 | PASS |
| `tests/unit/publication/test_planning.py::test_deterministic_complete_immutable_manifest_and_records` | planning; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_planning.py::test_span_splitting_no_loss_or_truncation` | planning; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_planning.py::test_profile_change_invalidates_identity` | planning; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_planning.py::test_corrupt_digest_and_missing_manifest_rejected` | planning; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_planning.py::test_complete_only_policy_and_cancelled_inputs` | planning; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_planning.py::test_wrong_version_extraction_and_derived_forgery_rejected` | planning; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_planning.py::test_reprofile_active_corpus_creates_new_generation` | planning; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_planning.py::test_partial_failed_digest_never_published[PARTIAL]` | planning; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_planning.py::test_partial_failed_digest_never_published[FAILED]` | planning; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_retrieval.py::test_generation_pinning_stale_replica_and_revocation` | retrieval; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_retrieval.py::test_reranker_provenance_tampering_rejected` | retrieval; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_retrieval.py::test_candidate_invisible_and_active_loss_unready` | retrieval; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_retrieval.py::test_real_reranker_preserves_metadata` | retrieval; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_retrieval.py::test_wrong_document_and_generation_citation_fail_closed` | retrieval; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_retrieval.py::test_sparse_only_and_dense_only_paths` | retrieval; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/publication/test_security.py::test_real_analysis_denies_before_search_or_provider_and_shared_owner_resolution` | security; setup error | P2: secure_publication fixture fails at standalone publication plan before protected assertions | T1 | PASS |
| `tests/unit/publication/test_security.py::test_provider_paused_then_revocation_blocks_answer_and_keeps_usage[revoke]` | security; setup error | P2: secure_publication fixture fails at standalone publication plan before protected assertions | T1 | PASS |
| `tests/unit/publication/test_security.py::test_provider_paused_then_revocation_blocks_answer_and_keeps_usage[tombstone]` | security; setup error | P2: secure_publication fixture fails at standalone publication plan before protected assertions | T1 | PASS |
| `tests/unit/publication/test_security.py::test_rollback_never_restores_revoked_or_tombstoned_access` | security; setup error | P2: secure_publication fixture fails at standalone publication plan before protected assertions | T1 | PASS |
| `tests/unit/publication/test_security.py::test_job_ownership_and_publication_administration` | security; setup error | P2: secure_publication fixture fails at standalone publication plan before protected assertions | T1 | PASS |
| `tests/unit/publication/test_security.py::test_authorized_reranker_cannot_insert_unselected_record` | security; setup error | P2: secure_publication fixture fails at standalone publication plan before protected assertions | T1 | PASS |
| `tests/unit/publication/test_workflow.py::test_preparation_runs_in_existing_durable_worker` | workflow; failure | P1: standalone publication operation lacks OIDC administration context | T1 | PASS |
| `tests/unit/test_api_reliability.py::test_tool_only_query_records_route_but_not_inference` | legacy API reliability; failure | L1: implicit OIDC rejects legacy API execution | T1 | PASS |
| `tests/unit/test_api_reliability.py::test_ready_returns_sanitized_200_or_503` | legacy API reliability; failure | A2: implicit OIDC adds unavailable security readiness gate | T1 | PASS |
| `tests/unit/test_memory_integration.py::test_exchange_persistence_uses_injected_store_exactly_once` | memory integration; failure | L2: cached implicit OIDC singleton rejects standalone persistence | T1 | PASS |
| `tests/unit/test_retrieval_regression.py::test_reranker_receives_retrieval_documents_and_sources_stay_compatible` | retrieval regression; failure | L2: cached implicit OIDC singleton rejects standalone prompt/retrieval | T1 | PASS |
| `tests/unit/test_streaming_orchestration.py::test_direct_stream_preserves_session_metadata_and_persists_once` | streaming; failure | L3: legacy guard rejects stream before route/provider/memory; generic error changes assertions | T1 | PASS |
| `tests/unit/test_streaming_orchestration.py::test_rag_stream_propagates_sources_and_uses_same_request` | streaming; failure | L3: legacy guard rejects stream before route/provider/memory; generic error changes assertions | T1 | PASS |
| `tests/unit/test_streaming_orchestration.py::test_tool_route_does_not_invoke_inference` | streaming; failure | L3: legacy guard rejects stream before route/provider/memory; generic error changes assertions | T1 | PASS |
| `tests/unit/test_streaming_orchestration.py::test_upstream_failure_is_a_sanitized_visible_event` | streaming; failure | L3: legacy guard rejects stream before route/provider/memory; generic error changes assertions | T1 | PASS |
| `tests/unit/test_streaming_orchestration.py::test_partial_stream_failure_is_not_retried_or_persisted` | streaming; failure | L3: legacy guard rejects stream before route/provider/memory; generic error changes assertions | T1 | PASS |
| `tests/unit/test_streaming_orchestration.py::test_vector_failure_is_a_sanitized_ndjson_event` | streaming; failure | L3: legacy guard rejects stream before route/provider/memory; generic error changes assertions | T1 | PASS |
| `tests/unit/test_streaming_orchestration.py::test_memory_failure_logs_no_chained_secrets_or_content[read]` | streaming; failure | L3: legacy guard rejects stream before route/provider/memory; generic error changes assertions | T1 | PASS |
| `tests/unit/test_streaming_orchestration.py::test_memory_failure_logs_no_chained_secrets_or_content[append]` | streaming; failure | L3: legacy guard rejects stream before route/provider/memory; generic error changes assertions | T1 | PASS |

## Self-review, independent review and pre-commit review

Implementation self-review covered the complete added source, explicit source
precedence, collection timing, singleton references, subclass/unrelated-model
handling, positional API compatibility, restoration/error paths and real security
negatives. A separate read-only agent reviewed the design and final three Python
files. It confirmed the public boundary and meaningful protected-path coverage,
found no material isolation/security defect, and identified one robustness issue:
a collection-time test assumed an exported MEMORY_HISTORY must equal the default.
The regression now captures and checks its original value instead. Child tests
independently prove clean synthetic defaults; reversed-order/exported-sentinel
verification passes. No application code was changed to resolve findings.

A separate pre-commit review checked new files for secrets, actual approvals,
private paths, debug output, temporary/generated artifacts, stale TODOs, dead code,
dependencies, documentation links, test hiding and API/security changes. Synthetic
sentinels and test-only credential-negative strings are intentional. All generated
logs, JUnit, fixtures, databases and bytecode are under temporary storage. The
clean prompt record preserves the supplied task requirements; prior phase reports
and audits were not edited.

Final Git review remained on `master` at the starting HEAD, with **20 tracked
modifications and 89 untracked status entries**: the original 83 plus these six
new files. All **368 pre-existing nonignored files are byte-identical** to the
starting inventory. Thus no production module, prior test, existing documentation,
historical report or audit in that inventory was modified by this task. The index
is still empty. `git status --short --branch`, `git diff --check`,
`git diff --stat` and `git diff --cached --name-only` were rerun.

The tracked diff stat is unchanged: **20 files, 607 insertions, 71 deletions**;
it describes preserved pre-existing work. This task's six additions are untracked
and therefore do not appear in that tracked-only stat. New-file whitespace and
Markdown link checks also pass, so the untracked additions are reviewed directly
rather than relying only on `git diff --check`.

No operator dotenv was edited or opened for manual inspection. The authorized
pre-change baseline let the existing Settings source load it implicitly; after
isolation ordinary test Settings do not read that source. No real credential,
operator key, live approval, historical private packet or real financial ledger
was inspected or mutated. All new authorities/records are synthetic and temporary.
Authentication, authorization, provider admission and financial safeguards remain
unchanged. Real provider calls, cloud modifications, operator signing/approvals,
commits and pushes: **zero**. No files were staged and no branch changed.

## Remaining limitations and next task

There are no remaining failures in the configured offline suite or the historical
64-case inventory. Exported application environment variables are intentionally
preserved; isolation is not a blanket environment reset. Tests deliberately
changing configuration must supply complete synthetic settings and restore changes.
An external startup plugin importing Settings before conftest fails clearly rather
than retaining an unisolated singleton. Fresh production processes are unchanged;
an application embedded in the same interpreter after `pytest.main` would retain
ordinary imported module objects, although the constructor is restored. Starting
production in a previously used pytest interpreter is not certified here.

The adapter relies only on public constructor inputs in pinned dependencies;
its positional/introspection/restoration tests should be rerun on dependency
upgrades. Existing relative fixture paths require repository-root execution or
an equivalent fixture tree when experimenting from another directory. Offline
socket/DNS denial remains an explicit verification safeguard, as authorized.
Existing lint and pytest warning debt is documented, not silently repaired.

Recommended next task: **Phase 17H–L — Final Offline Azure Strict-Schema and
Application-Validator Compatibility Audit**, examining where structurally valid
provider responses still fail application validation, without live inference.
This task has not begun that audit or authorized another experiment.
**Phase 17H remains PARTIAL.**
