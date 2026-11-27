# Phase 19B — Identity Bootstrap CI portability correction

27 November 2026. Test-only correction; operational Gate A remains BLOCKED.
Phase 19A COMPLETE; Phase 19B ACTIVE; Phase 19C NOT_STARTED.

## Outcome and scope

The reported CI failure was independently confirmed and reproduced before editing. The native
worker test assumed a parent PYTHONPATH because the earlier local offline runner supplied one.
GitHub Actions did not, so the test helper raised KeyError before launching Streamlit. The
production launcher already provides the correct controlled repository path and needs no change.

The correction conditionally preserves an explicitly supplied test path and otherwise retains
the launcher's default. The same real lifecycle test now exercises both parent-variable states
and asserts the exact selected path. Real Streamlit startup, successful health polling, bounded
shutdown and both loopback-port rebinds remain mandatory. No skip, fake server, or startup/health/
shutdown mock was introduced. Production source, dependencies, workflow and historical records
are unchanged. A new successful GitHub run is not claimed; changes remain uncommitted.

## Baseline and independently verified CI evidence

Read complete root AGENTS.md; instruction discovery found no applicable nested AGENTS.md.
Initial status was only `## master...origin/master`, with empty tracked/untracked/index diffs.
HEAD/local origin/master: **94c13e6fed46b306087bd92bd2b8061cc6e7d878**,
`feat: implement Phase 19B local identity bootstrap utility`, matching the supplied checkpoint.
Initial status/revision/log/stat/whitespace/index commands exited 0. No fetch or Git mutation.

Read the integration file, complete synthetic fixtures, bootstrap launcher, tests/conftest and
settings isolation helper, `.github/workflows/ci.yml`, all environment accesses in the new tests,
and the [previous implementation report](phase_19b_local_identity_bootstrap_utility.md).
The workflow runs Python 3.10 and `python -m pytest`; it sets no global PYTHONPATH.

Exact read-only retrieval commands:

```bash
gh run view 45958176991 --repo Susanta2025-lab/estudio-polymind-llm-orchestration \
 --json headBranch,headSha,status,conclusion,event,name,url
gh run view 45958176991 --job 140369436971 \
 --repo Susanta2025-lab/estudio-polymind-llm-orchestration --log-failed \
 > /tmp/phase19-bootstrap-ci-failed.log
```

Both exited 0. Metadata confirms master/push/completed/failure, workflow Estudio PolyMind CI and
exact current SHA. The [failed run/job](https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/45958176991/job/140369436971)
logs show the only failing test is test_native_worker_flags_and_real_loopback_start_stop.
Its stack reaches launch.supervise's environment construction, then the test helper at line 237:

```text
value["PYTHONPATH"] = os.environ["PYTHONPATH"]
KeyError: 'PYTHONPATH'
1 failed, 3416 passed, 5 warnings in 466.68s (0:07:46)
Process completed with exit code 1
```

The five CI warnings are the existing aiohttp NotAppKeyWarning in proxy tests. Native worker
startup never reached its gateway in the failing case, so its additional warning did not occur.
No other failing test or production exception is indicated. CI used Python 3.10.22; local
verification uses existing Python 3.10.13 dependencies. Local environment matching below concerns
parent-variable absence and actual test behavior, not an assertion of identical hosted machines.

## Root cause and environment-assumption audit

`launch.environment(root, evidence)` constructs a fresh explicit mapping, including
PYTHONPATH=str(REPO), private HOME and evidence/session paths. The failing test overwrote that
valid default by directly indexing an optional parent variable. Python evaluated the helper
before create_subprocess_exec, so failure prevented child construction; it was not a native
Streamlit, TLS, authentication, or production-runtime failure.

The earlier synthetic E2E integration already handles optional parent PYTHONPATH conditionally.
The previous offline runner inserted its sitecustomize guard directory and repository in
PYTHONPATH; its local full pass therefore did not expose the missing-variable branch. That
historical local result remains accurate for its stated environment and is preserved unchanged.

Audit of every new bootstrap test/helper found no other uncontrolled required environment key:

| Access | Assessment |
|---|---|
| Earlier synthetic E2E parent PYTHONPATH | Already guarded by membership check; retains launcher default when absent |
| Embedded child's SYNTHETIC_AUTH | Explicitly set in its private env before subprocess.run |
| Unit AppTest POLYMIND_BOOTSTRAP_EVIDENCE | Explicitly supplied with monkeypatch.setenv by the owning fixture |
| Synthetic fixtures | Use tmp_path, generated keys/certificates and current UID; no optional env lookup |
| Production worker session/evidence variables | Required internal launcher contract, supplied by launch.environment; unchanged |

Linux permission/loopback requirements are intentional target-platform contracts, not accidental
parent-variable assumptions. No operational environment or credential was inspected to do this audit.

## Reproduction before editing and exact correction

With the original tracked test unchanged, an offline-guarded interpreter launched pytest with
PYTHONPATH absent. Exact command:

```bash
python /tmp/polymind-bootstrap-ci-portability/run.py original-absent absent \
 tests/integration/test_identity_bootstrap_flow.py::test_native_worker_flags_and_real_loopback_start_stop
```

Result: **1 failed, 0 passed, 0 errors/skips/warnings, 0.65 seconds; exit 1**. Stack reproduced
the exact line-237 KeyError before native worker construction. There was no alternate runtime
fallback. The new independent network guard had already been installed before this reproduction.

The functional correction is only:

```python
if "PYTHONPATH" in os.environ:
    value["PYTHONPATH"] = os.environ["PYTHONPATH"]
```

The existing test additionally receives absent/present parameters. The absent case removes the
variable through monkeypatch, then checks that the child's value remains exactly str(launch.REPO).
The present case preserves an inherited approved test path; when CI has none it explicitly creates
a valid synthetic repository/session search path. The helper asserts exact preservation. Fixture
cleanup restores the parent environment after each case. This adds one collected lifecycle case
(3 integrations become 4; the full suite grows from 3,417 to 3,418).

Neither production defaults nor workflow settings were changed to accommodate the test. Both
cases still run launch.preflight and launch.supervise, start the actual pinned native worker,
wait for real HTTP health, terminate it through the real supervisor and successfully reserve
9443 and 8503 afterward. Only the existing 0.5-second test serving window remains shortened.

## Offline isolation independent of PYTHONPATH

No Entra/Azure/provider traffic or operational credentials were permitted. A temporary verification
interpreter was created outside Git using existing stdlib venv with `--without-pip`; it reuses
installed project dependencies via a .pth search entry. Exact creation command:
`python -m venv --without-pip /tmp/polymind-bootstrap-ci-portability/python`. No package was installed/downloaded and
no existing project/interpreter configuration was modified.

The temporary interpreter's site-packages .pth hook installs the scoped offline socket guard at
Python startup, before pytest or application imports. This works in parent and native child even
when PYTHONPATH is absent or contains only the production launcher's controlled repository path.
The guard allows loopback/Unix transport, denies external DNS/connect/connect_ex and public bind
before the underlying syscall, and records only PID/parent PID/guard and variable-presence booleans
in protected temporary attestations. It imports no application settings or credentials.

For the present scenario the environment also includes the earlier approved synthetic
sitecustomize path, preserving the original runner's explicit guard forwarding. For the absent
scenario there is no parent PYTHONPATH at process startup; the independent .pth hook supplies
protection. The child's normal PYTHONPATH still exists by production design and is asserted to
remain unchanged. No mandatory environment variable was added to CI or production.

A separate real parent/child guard check ran with parent PYTHONPATH absent:

```bash
python /tmp/polymind-bootstrap-ci-portability/run.py guard-absent absent \
 /tmp/polymind-bootstrap-ci-portability/test_guard.py
```

**1 passed in 0.28 seconds, exit 0; no warnings/failures/errors/skips.** It verifies installed
socket function identity and rejects documentation-range external connect/connect_ex, external
DNS and public bind before any packet/listener syscall. A child created using the exact unchanged
launch.environment also passes the same checks with only the default repository PYTHONPATH.
Actual native-worker startups across the targeted, integration and full runs also recorded
active parent/child guard attestations with both initially present-PYTHONPATH and initially
absent-PYTHONPATH parents. These are overlapping test executions, not
additional production sessions. This is Python-process test isolation, not a newly implemented
operational firewall or OS sandbox.
No real external request was used to prove denial.

Runner whitelist: temporary interpreter/bin plus the directory of the existing Helm executable and standard PATH,
synthetic HOME, C.UTF-8 locale,
PYTHONDONTWRITEBYTECODE=1, HF_HUB_OFFLINE=1, TRANSFORMERS_OFFLINE=1,
HF_HUB_DISABLE_TELEMETRY=1, ANONYMIZED_TELEMETRY=false, OMP_NUM_THREADS=1,
TOKENIZERS_PARALLELISM=false; optional PYTHONPATH only in present mode. Operational/provider/proxy
variables are excluded. Existing tests/conftest suppresses implicit dotenv before collection.
No production .env, state, TLS/CA/SSH private material or encrypted recovery artifact was read.

## Exact portability and regression verification

All wrapper invocations below execute the temporary existing-dependency interpreter as:

```text
/tmp/polymind-bootstrap-ci-portability/python/bin/python -m pytest -q <paths>
 --junitxml=/tmp/polymind-bootstrap-ci-portability/<name>.xml
 --basetemp=/tmp/polymind-bootstrap-ci-portability/<name>-state
 -o cache_dir=/tmp/polymind-bootstrap-ci-portability/<name>-cache
```

The wrapper creates a fresh whitelist environment with PYTHONPATH present or completely absent
according to its second argument. Every named state/log/XML path is scoped synthetic evidence;
no pre-existing operator file is deleted or overwritten.

```bash
python /tmp/polymind-bootstrap-ci-portability/run.py corrected-present present \
 tests/integration/test_identity_bootstrap_flow.py::test_native_worker_flags_and_real_loopback_start_stop
python /tmp/polymind-bootstrap-ci-portability/run.py corrected-absent absent \
 tests/integration/test_identity_bootstrap_flow.py::test_native_worker_flags_and_real_loopback_start_stop
python /tmp/polymind-bootstrap-ci-portability/run.py integration-absent absent \
 tests/integration/test_identity_bootstrap_flow.py
python /tmp/polymind-bootstrap-ci-portability/run.py unit-absent absent \
 tests/unit/test_identity_bootstrap.py
python /tmp/polymind-bootstrap-ci-portability/run.py phase19-absent absent \
 tests/unit/test_phase19_deployment.py tests/unit/test_phase19_tls.py \
 tests/unit/test_phase19_oidc_template.py tests/integration/test_phase19_operator.py \
 tests/integration/test_phase19_execution_bridge.py tests/integration/test_phase19_authority_lifecycle.py
python /tmp/polymind-bootstrap-ci-portability/run.py full-absent absent
python /tmp/polymind-bootstrap-ci-portability/run.py helm-absent absent tests/unit/test_helm_chart.py
python /tmp/polymind-bootstrap-ci-portability/run.py full-final-absent absent
```

| Verification | Exact result |
|---|---|
| Corrected native worker, guarded parent path present | Exit 0; 2 passed, 2 warnings, 5.13 s |
| Corrected native worker, parent path absent | Exit 0; 2 passed, 2 warnings, 4.80 s |
| Complete bootstrap integration | Exit 0; 4 passed, 3 warnings, 15.49 s |
| Complete bootstrap unit | Exit 0; 85 passed, no warnings, 6.44 s |
| Phase 19 deployment/TLS/runtime | Exit 0; 134 passed, 4 warnings, 112.50 s |
| Initial full run, parent path absent | Exit 0; 3,414 passed, 4 Helm skips, 163 warnings, 1,307.40 s |
| Helm regression after restoring existing tool path | Exit 0; 13 passed, no warnings/skips, 0.61 s |
| Final full offline regression, parent path absent | Exit 0; 3,418 passed, 0 skipped, 163 warnings, 1,377.69 s (22m57s) |

Completed targeted rows have zero failures, errors and skips, independently checked against
JUnit. The initial full run had zero failures/errors but four explicitly recorded Helm skips. Counts overlap full regression and must not be summed. Targeted runs each exercise both
parameter states; complete integration additionally verifies actual synthetic TLS/proxy and
signature → principal → protected candidate → logout with forbidden imports/network/database/
write guards. All identities/tokens/certificates are synthetic.

The initial full run exposed one verification-harness issue: its reduced PATH omitted the
already installed Helm directory. Existing test_helm_chart.py skipif decorators consequently
skipped four cases; no native-worker case was skipped. This was not a new dependency blocker.
The temporary harness was corrected to discover the existing Helm executable and include only
its directory alongside the temporary interpreter and standard PATH. No test, production or
workflow change was needed. The initial log/XML is retained; a Helm-only run and fresh full
run use distinct names and state directories. No package installation, cluster connection or
Kubernetes mutation occurs during local Helm lint/template checks.

The final full run exited 0 with **3,418 passed, 0 failures, 0 errors and 0 skips** in
**1,377.69 seconds (22m57s)**. JUnit independently records all 3,418 cases, zero
failures/errors/skips and 1,377.596 seconds. This is a fresh full invocation after the harness
PATH correction, not the sum of partial runs. It includes all 89 bootstrap cases and the four
Helm cases skipped in the first invocation. Source checksum remained unchanged throughout.

The final full run reports **163 warnings**: 156 existing pytest record_property/xunit2
advisories and 7 occurrences of the existing aiohttp NotAppKeyWarning at ui/tls_gateway.py:18
(four existing proxy cases, synthetic bootstrap TLS, and both successful native lifecycle cases).
Targeted warning counts in the table are solely this existing AppKey advisory. No category was
suppressed and no unrelated tests were edited to obtain a pass. The original failure, initial
full-run skips, corrected tool discovery and final rerun all remain explicitly recorded.

Additional commands:

```bash
ruff check --isolated --select E4,E7,E9,F,I tests/integration/test_identity_bootstrap_flow.py
ruff format --isolated --check tests/integration/test_identity_bootstrap_flow.py
PYTHONPYCACHEPREFIX=/tmp/polymind-bootstrap-ci-portability/bytecode python -m compileall -q .
git diff --check
```

All four checks exited 0; correctness/import lint and formatting pass for the changed file,
whole-repository compilation uses only the external bytecode cache, and Git whitespace is clean.
No lint/type tools or dependencies were installed. No configured type-checking step is changed
or required by this test-only correction; the earlier missing-mypy limitation remains.

No production-code/Docker/Compose/dependency/workflow change warrants an image rebuild, Compose
startup or Azure provenance replacement. No new successful hosted CI run is claimed: that
requires a later user checkpoint/push. Local Python patch-version/host timing differ from CI.
No real Microsoft Entra browser acceptance is authorized or inferred from these tests.

## Engineering self-review, pre-commit review and changed-file inventory

Engineering review traced both helper branches and assertion evaluation, monkeypatch restoration,
real child startup/health/finally cleanup, fixed loopback port release, and process-start network
isolation. The controlled default is preserved exactly and the optional approved guard path is
copied only in test code when explicitly present. Both actual branches pass, rather than replacing
the failure with a fallback/skip. Audit found no equivalent unowned required variable in the other
new tests. Production identity/enrollment/transport/authority/provider/financial behavior is unchanged.

Separate pre-commit review inspects all three candidates and the complete diff, checks no new
secrets/private keys/JWT payloads, credential arguments or logs, hard-coded operator paths,
.env/provider/production inputs, generated artifacts, stale TODOs/dead code, dependency/workflow
changes, skips/mocked native lifecycle or unrelated modifications. The test change contains only
the conditional copy, real environment-case setup and default/preservation assertion. Temporary
runner/guard/interpreter/logs are outside Git. No material unresolved implementation finding.

The final checker verifies exact candidate inventory, unchanged checkpoint HEAD, empty index,
all **219 tracked historical prompts/reports byte-identical**, unchanged production bootstrap and
workflow bytes, Markdown links, source/snippet syntax and whitespace, and no credential-payload
pattern findings. Command: `python /tmp/polymind-bootstrap-ci-portability/review.py`; its final result is recorded
in the handoff below.
The reviewed test checksum is checked again at handoff. None of this stages or commits files.

Complete candidate inventory:

```text
M  tests/integration/test_identity_bootstrap_flow.py
?? docs/codex/prompts/phase_19b_identity_bootstrap_ci_portability_correction.md
?? docs/codex/reports/phase_19b_identity_bootstrap_ci_portability_correction.md
```

The prompt is a clean record of the supplied maintenance task. This report records new evidence
without rewriting the historical bootstrap report, which only established its stated local
verification. No repository-wide documentation, runner/dependency or workflow changes were needed.

Proposed future user checkpoint only:

```text
fix: resolve identity bootstrap integration test CI portability
```

## Final status contract

```text
CI_FAILURE_ROOT_CAUSE: VERIFIED_OPTIONAL_PARENT_PYTHONPATH_INDEXED_BEFORE_NATIVE_STARTUP
ORIGINAL_FAILURE_REPRODUCED: YES_EXIT_1_KEYERROR_PYTHONPATH_BEFORE_EDIT
TEST_PORTABILITY_CORRECTION: CONDITIONAL_TEST_OVERRIDE_PLUS_TWO_REAL_LIFECYCLE_CASES
PYTHONPATH_PRESENT_VERIFICATION: PASS_2_CASES_5_13_SECONDS
PYTHONPATH_ABSENT_VERIFICATION: PASS_2_CASES_4_80_SECONDS
OFFLINE_NETWORK_ISOLATION: PASS_INDEPENDENT_PTH_PARENT_CHILD_GUARD_ABSENT_VARIABLE
NATIVE_STREAMLIT_STARTUP: PASS_ACTUAL_CHILD_AND_REAL_HEALTH
NATIVE_STREAMLIT_SHUTDOWN: PASS_ACTUAL_SUPERVISOR
LOOPBACK_PORT_RELEASE: PASS_9443_AND_8503_REBOUND
BOOTSTRAP_UNIT_REGRESSION: PASS_85
BOOTSTRAP_INTEGRATION_REGRESSION: PASS_4
FULL_OFFLINE_REGRESSION: PASS_3418_0_FAILURES_ERRORS_SKIPS_163_WARNINGS_1377_69_SECONDS
PRODUCTION_CODE_CHANGED: NO
GITHUB_WORKFLOW_CHANGED: NO
PRE_COMMIT_REVIEW: PASS_3_CANDIDATES_219_HISTORICAL_RECORDS_UNCHANGED_EMPTY_INDEX

ACTUAL_ENTRA_AUTHENTICATION: NOT_AUTHORIZED
AZURE_VM_ACTIVATED: NO
REAL_INFERENCE_CALLS: 0

GIT_STAGED: NO
GIT_COMMITTED: NO
GIT_PUSHED: NO

PHASE19A_STATUS: COMPLETE
PHASE19B_STATUS: ACTIVE
PHASE19C_STATUS: NOT_STARTED
GATE_A_OPERATIONAL_CLOSURE: BLOCKED
```

## Final validation and Git handoff

All required test groups completed. The final full suite ran with parent PYTHONPATH absent,
the independent parent/child guard active, existing Helm discoverable, and no failures/errors/
skips. The sole repository code change remains the reviewed integration test; the original
failure is reproduced and the default/present-path assertions both pass with actual native
startup, health, shutdown and port release. No test weakening or production/workflow change.

Lint/format/whole-repository external-cache compilation/whitespace checks exited 0. Historical
records, production source and workflow preservation, candidate syntax/links and final index
checks are verified by the separate final review command. Its observed result follows this
Git record. No new hosted CI run was triggered or claimed, and no operational Entra/browser/
Azure/SSH/provider/state/inference action occurred. No staging, commit or push. Gate A remains
BLOCKED; 19B ACTIVE; 19C NOT_STARTED. Stop at operator review of this correction.

```text
$ git status --short --branch
## master...origin/master
 M tests/integration/test_identity_bootstrap_flow.py
?? docs/codex/prompts/phase_19b_identity_bootstrap_ci_portability_correction.md
?? docs/codex/reports/phase_19b_identity_bootstrap_ci_portability_correction.md
exit 0

$ git diff --stat
 tests/integration/test_identity_bootstrap_flow.py | 18 ++++++++++++++++--
 1 file changed, 16 insertions(+), 2 deletions(-)
exit 0

$ git diff --check
(no output)
exit 0

$ git diff --cached --name-only
(no output)
exit 0
```


Final review command `python /tmp/polymind-bootstrap-ci-portability/review.py` exited 0:

```text
PRE_COMMIT_REVIEW: PASS; 3 candidates (1 test, 2 documents)
HISTORICAL_RECORDS_BYTE_IDENTICAL: 219
PRODUCTION_AND_WORKFLOWS_UNCHANGED: YES; LOCAL_LINKS: 1
INDEX_EMPTY: YES; HEAD_UNCHANGED: YES; SECRET_PAYLOAD_SCAN: NO_FINDINGS
```

The reviewed test checksum also matches. All status fields and this final validation addendum
are populated. The first-run Helm skips are resolved by the final zero-skip full run; they
remain in the evidence rather than being omitted. No commit or push occurred.
