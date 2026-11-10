# Phase 17H v8 structural-path boundary regressions

Date: 2026-11-09. This test-only supplement addresses the independent Antigravity
audit finding that the measured 166-character acceptance and 167-character
rejection lacked permanent exact assertions. The original
[v8 engineering report](phase_17h_v8_lineage_hardening_and_offline_readiness.md)
and historical execution evidence remain unchanged.

The only existing file edited by this task is
[test_managed_prompt8_sizing.py](../../../tests/unit/documents/test_managed_prompt8_sizing.py).
Its new parameterized test exercises production `reduction_size`, `escaped_size`,
`check_request` and the managed renderer with two validated, checkpointed children.
Each child reserves the existing maximum 7,000 bytes; actual child contributions
are also checked against that ceiling. No test-only admission validator is used.

The fixed envelope is 10,630 bytes and two maximum child reservations total 14,000,
leaving exactly **170 bytes** for the structural path within 24,800 input bytes.
All nonempty examples below are single tuple elements, not separate components.

| Path | Measured path overhead | Planned input | Complete planned context | Admission |
| --- | ---: | ---: | ---: | --- |
| `()` | 0 | 24,630 | 27,830 | Accepted |
| `("a",)` | 5 | 24,635 | 27,835 | Accepted |
| `("a" * 165,)` | 169 | 24,799 | 27,999 | Accepted |
| `("a" * 166,)` | 170 | 24,800 | 28,000 | Accepted |
| `("a" * 167,)` | 171 | 24,801 | 28,001 | `synthesis_limit_exceeded` |

Complete context adds 100 overhead, 100 safety and 3,000 reserved output tokens.
These are conservative byte-based planning estimates, not billed provider tokens.
The test measures each path's delta in the complete serialized system/data/schema
envelope and independently compares it with production `escaped_size`; it does
not infer escaping costs solely from character count. It checks actual rendered
context against the planned reservation too. Diagnostic rendering disables limits
only to measure serialization; both checked rendering and production
`check_request` must reject every 24,801-byte case with the exact category above.

Additional exact-limit/one-byte-over cases use quote, backslash and newline
together, and accented/BMP/astral Unicode together. After both JSON escaping
layers, the first prefix contributes 11 content bytes and the Unicode prefix 28;
the nonempty single-element path adds four punctuation bytes relative to `()`.
Thus 155/156 ASCII padding bytes give escaped overhead 170/171, and 138/139 give
Unicode overhead 170/171. All nine cases run against intermediate, structural and
root profiles: **27 new regressions**, with identical admission outcomes.

Validation used the existing `estudio_polymind` Python 3.10.13 environment,
application-settings isolation and the established independent `offline_guard`
loaded before collection. Plugin autoload, bytecode writes and pytest cache were
disabled. Logs/JUnit and the preservation inventory remain outside the repository.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  PYTHONPATH=.:/tmp/phase17h-g1-g2 python -m pytest \
  -p offline_guard -p no:cacheprovider \
  --basetemp=/tmp/phase17h-v8-path-boundary/compatibility \
  --junitxml=/tmp/phase17h-v8-path-boundary/compatibility.xml \
  -o junit_family=xunit1 -q \
  tests/unit/documents/test_managed_prompt8_sizing.py \
  tests/unit/documents/test_managed_prompt7_sizing.py \
  tests/unit/documents/test_managed_sizing.py \
  tests/unit/documents/test_reducer_sizing_reconciliation.py \
  tests/unit/test_g1_source_compatibility.py \
  tests/unit/documents/test_direct_child_lineage.py \
  tests/unit/documents/test_claim_stage_identity.py \
  tests/integration/test_reducer_sizing_offline_workflow.py \
  tests/integration/test_direct_child_lineage_workflow.py \
  tests/integration/test_claim_stage_identity_workflow.py \
  tests/integration/test_managed_prompt8_contract.py \
  tests/integration/test_managed_prompt7_contract.py
```

| Validation | Result |
| --- | --- |
| Boundary-only pytest selection, same safeguards, `-k test_exact_structural_path_boundary`, separate `exact` temp/JUnit destinations | Exit 0; 27 passed, 21 deselected in 14.87s |
| Complete focused command above | Exit 0; 216 passed in 77.66s |
| V8 sizing / v7 historical sizing within the focused run | 48 / 21 passed |
| Managed sizing / child-material reconciliation / G1 source compatibility | 11 / 14 / 10 passed |
| Direct-child lineage / claim-stage identity units | 25 / 24 passed |
| Reducer sizing / direct-child lineage / claim-stage identity workflows | 10 / 9 / 10 passed |
| V8 / v7 contract compatibility | 19 / 15 passed |
| Offline guard, both pytest runs | Zero network attempts |
| JUnit, both runs | Zero failures, errors or skips |
| `ruff check tests/unit/documents/test_managed_prompt8_sizing.py` | Exit 0; all checks passed |
| `ruff format --check tests/unit/documents/test_managed_prompt8_sizing.py` | Exit 0; one file already formatted |
| `python -m py_compile tests/unit/documents/test_managed_prompt8_sizing.py`, external `PYTHONPYCACHEPREFIX` | Exit 0 |
| `git diff --check` | Exit 0 |

The boundary selection overlaps the 216-test run; counts must not be added.
The original **2,067-test offline baseline remains applicable as historical
validation of the unchanged production contract**. That full suite was not rerun
in this task. The 27 new cases extend its coverage; no new full-suite pass is
claimed. Docker builds and broader testing were unnecessary for this test-only
addition.

The production `generation_contract_digest()` was recomputed under the network
guard and settings isolation. `managed-prompt/8` and the complete SHA-256 remain:

```text
93ca9066491c197987f919c5d185417bf4f3d2787384acf2833011e32641c0df
```

Self-review verified the full task diff, exact serialization, admission/error
paths, context arithmetic and unchanged child data. The separate pre-commit review
found no credentials, private data, new dependencies, generated artifacts,
production/interface changes or unrelated edits. A before/after SHA-256 inventory
confirms all **483 other existing Git-visible files** remain byte-identical,
including production modules, historical fixtures, original reports and unrelated
uncommitted work. The existing test file was already untracked at entry. This note
is the only new file created by this task; the staged diff remains empty.

Production behavior is unchanged and requires no fix. G1 child-material and G2
lineage regressions pass without validator edits. The 170-byte two-child path
constraint remains; this does not certify arbitrary paths or increase any limit.
No Azure inference, authentication, operator RSA signing or approval consumption
was performed.

**PASS — V8 STRUCTURAL-PATH BOUNDARY REGRESSIONS VERIFIED**

Git staging: **NO**. Git commit: **NO**. Git push: **NO**.
Production changes by this task: **NO**. Azure inference: **NO**.
