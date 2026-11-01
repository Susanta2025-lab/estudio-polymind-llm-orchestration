# CODEX PROMPT — Phase 17H–L: AST Test Portability Correction

## 0. Role and Objective

Act as a Senior Python Engineer specializing in cross-version compatibility, regression testing, source-code integrity and AI system reliability.

**Project:** Estudio PolyMind
**Repository:** `Susanta2025-lab/estudio-polymind-llm-orchestration`
**Working branch:** `master`

### Primary objective

Correct the interpreter-dependent AST fingerprint assertions introduced during the latest Phase 17H–L live-failure observability implementation.

The independent code review identified that some tests compute SHA-256 hashes from Python AST representations. Those representations are not guaranteed to remain identical across Python interpreter versions.

The tests were originally executed under **Python 3.10.13**, while independent verification under **Python 3.13.5** produced different AST hashes for unchanged source code.

This can cause false-positive regression failures.

**Fix the portability issue without weakening the existing regression protections.**

The test must still detect unauthorized changes to production validation predicates, generation instructions and other frozen contracts.

## 1. Required Initial Inspection

First read:

```text
AGENTS.md
```

Then inspect:

```text
tests/integration/test_live_failure_observability.py
documents/digestion/validation.py
documents/digestion/models.py
documents/digestion/managed.py
documents/digestion/codec.py
```

Also inspect relevant tests and reports:

```text
docs/codex/reports/phase_17hl_live_failure_observability_and_contract_options.md
docs/codex/reports/phase_17hl_final_offline_azure_compatibility_audit.md
```

Search the relevant test files for:

```text
ast.dump
ast.parse
hashlib.sha256
AST fingerprints
normalized AST
source checksums
```

Identify all newly introduced tests whose results can vary because of interpreter-specific AST representations.

Do not assume that every AST test is defective.

Determine exactly which serialization or AST representation causes the portability mismatch.

## 2. Reproduce and Explain the Problem

Before modifying tests:

1. Identify the affected test functions.
2. Record the expected hardcoded fingerprints.
3. Recompute the fingerprints using the current interpreter.
4. Inspect how normalization and hashing are performed.
5. Determine whether interpreter differences, rather than actual source changes, explain the mismatch.

Check the available Python versions:

```bash
python --version
python3 --version
```

If multiple Python interpreters are already available, compare their outputs.

Do not install additional Python versions or dependencies without authorization.

The investigation must distinguish:

- A genuine production-code change.
- An AST serialization difference.
- A Python grammar/representation difference.
- An incorrectly constructed source baseline.
- A true contract-regression failure.

Document the reproducible cause.

## 3. Implement a Portable Regression Mechanism

Replace interpreter-dependent AST hashing with a reliable mechanism that preserves meaningful regression detection.

### Required properties

The revised test must be:

- Deterministic.
- Independent of Python AST serialization differences.
- Compatible with supported project Python versions.
- Sensitive to unauthorized semantic changes.
- Safe to run offline.
- Independent of Azure services.
- Independent of dynamically generated approval artifacts.
- Easy to maintain and review.

### Preferred approach

Evaluate a stable source-comparison or canonicalization strategy that does not depend on version-specific `ast.dump()` representations.

Acceptable approaches may include:

- Stable token-based source normalization with independently frozen reference data.
- A version-independent canonical representation of the relevant source structure.
- Explicit structural and behavioral regression assertions backed by fixed approved baselines.
- Another small, dependency-free approach with demonstrably equivalent or stronger coverage.

Choose the simplest technically defensible solution.

**Do not merely replace AST hashes with weaker tests that allow production-contract changes to pass unnoticed.**

Avoid dynamic baselines such as:

```python
expected = hash(current_source)
actual = hash(current_source)
```

Such tests provide no meaningful regression protection.

Approved expected values must remain independent of the implementation being tested.

Do not silently regenerate or update baseline fingerprints when code changes.

If canonicalization ignores comments, whitespace, or diagnostic-only fields, document precisely what is excluded and why. Do not accidentally exclude acceptance predicates or generation instructions.

## 4. Preserve All Existing Contract Protections

The revised tests must continue protecting the following invariants.

### 4.1 Validation semantics

The accepted/rejected behavior of:

```text
documents/digestion/validation.py::validate_result
```

must remain unchanged.

The test must detect unauthorized changes to:

- Stage binding.
- Deterministic claim identities.
- Evidence membership.
- Qualification validation.
- Child lineage.
- Source coverage.
- Reduction coverage.
- Claim contract rules.
- Response and annotation limits.

Diagnostic metadata additions may be excluded only if they are explicitly verified to have no effect on acceptance semantics.

### 4.2 Generation contract

Preserve regression coverage for:

```text
documents/digestion/managed.py
```

Specifically protect:

- Active system instructions.
- Prompt-template version.
- Generation schema.
- Stage profiles.
- Request-control construction.
- Azure-facing payload configuration.
- Reasoning-effort configuration.
- Token and byte limits.

Do not update production prompt versions or schema fingerprints to accommodate this test fix.

### 4.3 Domain models

Preserve tests that detect changes to:

```text
StageResult
Claim
ClaimLink
Qualification
DigestionProfile
```

Especially preserve field types, constraints, validation semantics and serialization behavior.

## 5. Add Targeted Regression Tests

Introduce focused tests proving that the replacement mechanism works correctly.

### Positive cases

Verify that:

1. The unchanged approved source passes.
2. Repeated executions produce identical results.
3. Diagnostic-only changes permitted by the existing policy do not trigger a false regression.
4. The chosen canonical representation is stable under the supported interpreters.

### Negative cases

Using temporary synthetic source fixtures, verify that the test fails when:

1. A claim-identity predicate is removed.
2. A source-coverage requirement is weakened.
3. An evidence-validation condition is removed.
4. A stage-binding condition changes.
5. A frozen generation instruction changes.
6. A relevant domain constraint changes.

Use synthetic fixtures or controlled temporary source copies.

Do not mutate production files to simulate negative cases.

The tests must fail for the intended reason, not merely because of an unrelated syntax or import error.

### Cross-version checks

If Python 3.10 and 3.13 are both available:

- Run the relevant tests under both.
- Confirm identical semantic acceptance.
- Confirm that no false fingerprint mismatch occurs.

If only one interpreter is available:

- Run all possible local checks.
- Use deterministic representative fixtures to test the canonicalization rules.
- Clearly report that actual cross-interpreter execution remains unverified.

Do not claim multi-version verification without executing it.

## 6. Strict Scope Restrictions

This is a **test portability correction only**.

### Allowed modifications

- Affected AST fingerprint tests.
- Small reusable test-only canonicalization helpers, if necessary.
- Focused test fixtures.
- Documentation explaining the corrected comparison mechanism.
- New tests directly related to AST portability.

### Prohibited modifications

Do not change production implementation files, including:

```text
documents/digestion/managed.py
documents/digestion/models.py
documents/digestion/codec.py
documents/digestion/validation.py
documents/digestion/diagnostics.py
llm/azure_schema.py
llm/structured.py
llm/openai_compatible.py
llm/bounded_http.py
```

Do not modify:

- StageResult contracts.
- Generation prompts.
- Azure request payloads.
- Provider/schema fingerprints.
- Domain validation predicates.
- Error classification.
- Governance rules.
- Financial accounting.
- Security policies.
- Production logging.
- Durable checkpoint behavior.

If a production change appears necessary, stop that subtask and document the issue.

## 7. Git, Security and Cloud Restrictions

Work directly on the existing `master` branch.

Do not:

- Create a branch.
- Commit.
- Push.
- Stage files.
- Reset.
- Clean.
- Restore.
- Rebase.
- Merge.
- Stash.
- Delete existing untracked files.

Preserve the entire current working tree.

### Cloud restrictions

No:

- Azure inference.
- OpenAI inference.
- Cloud API calls.
- Azure CLI operations.
- Paid external services.
- Cloud provisioning.
- Live financial reservation.
- Operator approval generation or signing.

### Privacy restrictions

Do not read or expose:

- `.env` secrets.
- Private keys.
- Authentication tokens.
- Historical private approval packets.
- Raw provider response archives.
- Real document contents.

Use synthetic fixtures exclusively.

## 8. Verification Requirements

First, run focused tests covering the modified portability mechanism.

Then run the repository's existing offline-guarded integration and full regression tests.

Reuse the established pre-import network guard.

Do not replace or weaken the existing test-isolation infrastructure.

### Quality checks

Execute the applicable commands:

```bash
ruff check <changed_python_files>
ruff format --check <changed_python_files>
git diff --check
git status --short --branch
git diff --stat
git diff --cached --name-only
```

Run Python compilation checks where applicable.

### Full regression

The previous reported baseline was:

```text
1631 passed
0 failed
0 errors
0 skipped
0 network attempts
```

Preserve all existing tests.

If new tests are added, the total count should increase appropriately.

Distinguish pre-existing lint findings from newly introduced errors.

Do not conceal failures using skips, xfails or weakened assertions.

## 9. Acceptance Criteria

Declare PASS only when all the following conditions hold.

**Portability**

- The interpreter-dependent fingerprint issue is understood.
- The affected mechanism no longer depends on unstable AST representations.
- No test baseline is computed from the current code under test.
- Cross-version checks pass where the required interpreters are available.

**Regression protection**

- Existing contract protections remain.
- Deliberate semantic changes in synthetic fixtures are detected.
- Diagnostic-only permitted changes do not create false failures.
- Generation instructions remain protected.

**Engineering safety**

- Production files are unchanged.
- No generation or provider contract changes occur.
- No approvals or fingerprints are refreshed.
- Full offline regression passes.
- No network access occurs.
- No commits or pushes occur.

If cross-interpreter execution is unavailable, report the task as locally verified with cross-version verification pending rather than asserting unobserved compatibility.

## 10. Documentation and Final Handoff

Create the report:

```text
docs/codex/reports/phase_17hl_ast_test_portability_fix.md
```

Save the prompt under:

```text
docs/codex/prompts/phase_17hl_ast_test_portability_fix.md
```

The report must include:

1. Root cause.
2. Affected test locations.
3. Old versus new regression mechanism.
4. Explanation of cross-version stability.
5. Evidence that semantic contract changes remain detectable.
6. Evidence that diagnostic-only changes do not cause false failures.
7. Python versions actually tested.
8. Exact verification results.
9. Complete task-only file inventory.
10. Remaining limitations.

### Required final response format

```text
TASK:
Phase 17H–L — AST Test Portability Correction

BRANCH:
HEAD:

ROOT CAUSE:
Affected test functions:
Previous fingerprint mechanism:
New comparison mechanism:

IMPLEMENTATION:
Files modified:
Files created:
Production code modified: NO
Generation contract modified: NO
Validation predicates modified: NO

PORTABILITY:
Python 3.10 verification:
Python 3.13 verification:
Cross-version consistency:
Unverified environments:

REGRESSION PROTECTION:
Approved source passes:
Claim-identity mutation detected:
Evidence-validation mutation detected:
Coverage mutation detected:
Prompt mutation detected:
Domain-model mutation detected:

TESTS:
Previous baseline: 1631
Focused tests:
Full regression:
Failures:
Errors:
Skipped:
Network attempts:
Ruff:
Compilation:

SAFETY:
Azure calls: 0
Paid inference calls: 0
Cloud operations: 0
Operator approvals: 0
Commits: 0
Pushes: 0

REPORT PATH:
FINAL VERDICT:
```

## FINAL INSTRUCTION

Fix only the AST test-portability issue.

Preserve or improve the strength of regression detection.

Do not weaken tests, alter production behavior, change generation fingerprints, or restart broad offline hardening.

This task must not modify Azure compatibility or inference contracts.

**Phase 17H remains PARTIAL. This correction does not authorize another live inference attempt.**
