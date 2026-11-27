# CODEX MASTER PROMPT — PHASE 19B

## Local Identity Bootstrap Utility — CI Failure Investigation and Portability Correction

**Project:** Estudio PolyMind
**Branch:** master
**Current commit:** `94c13e6`
**Task:** Resolve the isolated Identity Bootstrap integration-test CI failure.

### 1. Verified failure evidence

GitHub Actions run: `45958176991`
Job ID: `140369436971`
Conclusion: FAILURE

```text
3416 passed
1 failed
5 warnings
466.68 seconds
```

Failing test:

```text
tests/integration/test_identity_bootstrap_flow.py
::test_native_worker_flags_and_real_loopback_start_stop
```

Root exception at line 237:

```python
value["PYTHONPATH"] = os.environ["PYTHONPATH"]
```

```text
KeyError: 'PYTHONPATH'
```

The local offline verification environment supplied PYTHONPATH, whereas GitHub Actions did not.

### 2. Mandatory investigation

Read AGENTS.md and inspect:

- `tests/integration/test_identity_bootstrap_flow.py`
- `tests/identity_bootstrap_fixtures.py`
- `deployment/phase19/identity_bootstrap/__main__.py`
- `tests/conftest.py`
- Relevant GitHub Actions workflow.
- Previous Identity Bootstrap Utility implementation report.

Retrieve the failed CI logs and independently confirm the reported root cause.
Inspect all newly introduced tests for equivalent uncontrolled environment-variable assumptions.

### 3. Implementation

Apply the smallest justified test portability correction.
Preserve the launcher's controlled default environment when the parent PYTHONPATH variable is absent.
Preserve the synthetic offline network guard when explicitly supplied by the approved test runner.
Consider the conditional pattern already used in the other synthetic integration test:

```python
if "PYTHONPATH" in os.environ:
    value["PYTHONPATH"] = os.environ["PYTHONPATH"]
```

Verify that this correction is sufficient rather than assuming it.
Ensure offline network restrictions remain effective independently of incidental environment-variable
presence. Do not modify production environment isolation to accommodate the test. Do not introduce
a mandatory global PYTHONPATH setting into GitHub Actions merely to conceal the portability defect.
Do not skip, mock away or weaken actual native Streamlit startup, health and shutdown integration.

### 4. Verification

Reproduce the original failure before applying the correction. After implementation, verify:

- PYTHONPATH present with the approved synthetic offline guard.
- PYTHONPATH absent, matching the CI environment.

Exercise both with appropriate offline network isolation. Confirm actual native worker startup,
health, shutdown and release of both loopback ports. Run:

1. Corrected failing integration test.
2. Complete Identity Bootstrap integration suite.
3. Complete Identity Bootstrap unit suite.
4. Applicable Phase 19 deployment and TLS regressions.
5. Full offline regression suite using a CI-compatible environment.
6. Applicable lint, compilation and Git whitespace checks.

Report exact commands, results and limitations.

### 5. Boundaries

Do not change production identity verification, enrollment, gateway security, authority initialization,
provider boundaries or financial controls. No Azure activation, operational credential access, actual
Entra authentication, provider requests or model inference. No new dependencies unless separately
authorized. Do not stage, commit or push. Preserve historical reports.

### 6. Documentation

Create:

```text
docs/codex/prompts/phase_19b_identity_bootstrap_ci_portability_correction.md
docs/codex/reports/phase_19b_identity_bootstrap_ci_portability_correction.md
```

Include verified CI failure evidence, root-cause analysis, reproduction, exact correction,
environment portability verification, regressions, security isolation preservation, changed-file
inventory and separate pre-commit review.

### 7. Final status contract

```text
CI_FAILURE_ROOT_CAUSE:
ORIGINAL_FAILURE_REPRODUCED:
TEST_PORTABILITY_CORRECTION:
PYTHONPATH_PRESENT_VERIFICATION:
PYTHONPATH_ABSENT_VERIFICATION:
OFFLINE_NETWORK_ISOLATION:
NATIVE_STREAMLIT_STARTUP:
NATIVE_STREAMLIT_SHUTDOWN:
LOOPBACK_PORT_RELEASE:
BOOTSTRAP_UNIT_REGRESSION:
BOOTSTRAP_INTEGRATION_REGRESSION:
FULL_OFFLINE_REGRESSION:
PRODUCTION_CODE_CHANGED:
GITHUB_WORKFLOW_CHANGED:
PRE_COMMIT_REVIEW:

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

Proposed future commit:

```text
fix: resolve identity bootstrap integration test CI portability
```

STOP after completing correction, offline verification and engineering report.
