# Phase 17H — CI failure and historical contract reconciliation

Date: 2026-11-02. Starting HEAD: `f3a2a87`, following G1/G2 commit `d940443`.

## Executive summary

Final readiness decision: **PASS — offline CI compatibility restored**.

The complete CI-equivalent offline suite passed **1,850 tests, 0 failures,
0 errors, 0 skips**, with 51 warnings, in **530.73 seconds** (exit 0).
JUnit inventory comparison proves that all **1,831 original tests** remain
present, all **28 previously failing/error nodes** pass, and **19 new regression
cases** were added. The main-interpreter network guard recorded **0 attempts**.

The two affected modules reproduced exactly the supplied CI failure shape:
**207 passed, 15 failed, 13 errors**. The failures arose from historical fixtures
and assertions sharing the newly bounded L1 configuration, and from exact source
equality assertions that did not account for the intentional G1 additions.
No application implementation regression was established. Corrections are limited
to test construction, contract scoping, a fixed source compatibility delta and
documentation. Application code, approved fingerprints, original golden files,
security/governance policy, provider behavior and dependencies are unchanged.

Historical v3 and pre-G1 v4 requests retain their original bindings. Current L1
retains the 7,000-byte rendered-child admission policy, separate 10,000-byte raw
and canonical output ceilings, and strict G2 integration behavior. Stored data
readability remains distinct from permission to resume a request under a different
configuration. No output/evidence is repaired or truncated.

No network access, paid inference, credential/approval inspection, Docker,
Kubernetes, Azure or other cloud operation was performed. No staging, commit,
push, reset, clean or branch change occurred. Live operator authorization was
not started.

## CI scope and reproduction environment

The checked-in `.github/workflows/ci.yml` defines the `build` job on Ubuntu with
Python 3.10. It installs `requirements-ml-cpu.txt` with `--no-deps`, then
`requirements.txt`, compiles the repository and runs **`python -m pytest`**.
`pytest.ini` sets `testpaths = tests` and `addopts = -ra`; there is no special
CI-only test selection. Helm, Compose and Docker checks follow the test step.

This task used the existing Python **3.10.13**, pytest **8.4.2** environment.
Metadata inspection found all **142** pinned distributions installed: all
**141** `requirements.txt` pins matched; Torch reported `2.12.0` rather than the
CI-specific `2.12.0+cpu` wheel. No installation or download was attempted. These
changes concern settings, JSON contracts and test fixtures, not ML execution.
The OS/Python minor environment matches CI where practical; exact runner/image
identity and the CPU wheel are not claimed.

The supplied remote run is
[Estudio PolyMind CI 41451173192](https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/41451173192).
Its result/step details are user-supplied. The remote logs were deliberately not
fetched because this task prohibits network access. The checked-in workflow and
local reproduction establish the executable CI scope and causes independently.

Tests use the existing `tests/conftest.py` / `tests/settings_isolation.py`
configuration isolation, which disables implicit application dotenv input before
collection. No operator dotenv or private packet was opened. A pre-existing
temporary `offline_guard` plugin was inspected before use; it denies socket
`connect`, `connect_ex`, `sendto`, `create_connection`, `getaddrinfo` and
`gethostbyname` before collection and counts attempted access. Existing per-test
guards and explicit HTTP fakes remain in use. The guard count describes the main
pytest interpreter; it is not a separate network audit of child interpreters.

## CI failure classification and established causes

All 28 failing/error nodes are accounted for below. Parameter counts are the
pre-correction counts; the final run retains their node IDs and adds tests.

| Original tests | Count | Classification | Established cause and correction |
| --- | ---: | --- | --- |
| `test_complete_pre_edit_generation_contract` (nine combinations), `test_v4_changes_only_subject_guidance` (three stages), `test_historical_results_readable_but_requests_cannot_resume` | 13 errors | Test fixture isolation/configuration | `historical_contracts` loads the hash-pinned v3 renderer/settings source, then invokes the current L1 composition. That composition now explicitly supplies `child_input_bytes=7000`. The frozen v3 `ManagedSettings` has no such field and correctly rejects it with `extra_forbidden`. Replay now omits that one current-only constructor input before calling the original strict constructor. |
| `test_generation_schema_and_renderer_source_remain_frozen`, `test_application_acceptance_predicates_and_order_are_unchanged` | 2 failures | Legitimate conflict between literal historical source equality and intended G1 additions | G1 adds the optional profile budget/omission serializer and a conditional child admission check. They cannot literally equal the pre-G1 declarations. A fixed exact G1 delta is reversed only for the original frozen-source comparisons; the live implementation and original references are unchanged. |
| `test_active_v4_generation_contract` (three stages) | 3 failures | Historical configuration binding / fixture isolation | The golden describes pre-G1 v4 requests. The shared current L1 fixture now has a new settings fingerprint, profile budget, stage identities and rendered instructions/control. A separately scoped pre-G1 v4 fixture runs current code with policy unset and reproduces the original nine hashes. The original v4 whole-source checksum is checked after the exact G1 source projection. |
| `test_active_subject_rules_have_valid_witnesses_for_all_profiles` (four profiles), `test_render_rejects_wrong_profile_and_config_before_provider` (three stages) | 7 failures | Test configuration reconstruction issue; intended fail-closed checkpoint rejection | These tests construct an adapter without the child policy and try to render a request captured from current G1 L1. Their inference configuration fingerprints must differ. Current tests now reconstruct `child_input_bytes=7000`; wrong-profile/config/model negative assertions remain. |
| `test_canonical_boundary_under_unchanged_l1_profile[10000-*]` | 3 failures | Intended new G1 admission behavior requiring a correctly scoped test | A canonical 10,000-byte result fits the independent output ceiling but exceeds 7,000 bytes as escaped child material with links, evidence and wrapper reserve. Original 10,000/10,001-byte semantics are tested with the historical unbounded profile; new current-L1 tests require the 10,000-byte witness to be rejected and independently check canonical overflow. |

The historical fixture failure is not a corrupt serialized checkpoint and is not
a current Pydantic bug. It originates at constructor input assembly. The config
mismatches are deterministic contract differences, not intermittent suite state
or CI-specific dependency behavior. The output failure is not an accidental
reduction of the 10,000-byte raw/canonical ceiling. Those ceilings and downstream
child-material admission are independent and both remain enforced.

No CI-only cause or unintended application regression was demonstrated. Before
reproduction these were hypotheses; the identical failing-node inventory and
targeted constructor/render/validation evidence resolve the observed symptoms.

## Minimal corrections and architecture impact

`capture_contracts` factors the existing observer fixture into a reusable test-only
capture function. The default `contracts` fixture still exercises the unchanged
current L1 composition with G1 enabled. `legacy_v4_contracts` explicitly requests
historical settings. The existing v3 replay uses that same explicit historical
mode while its hash-pinned classes are temporarily installed.

Historical mode accepts only the known current harness input of 7,000, omits the
single new keyword, and invokes the original settings constructor. It asserts
that the serialized settings do not acquire the new field. It does not catch a
`ValidationError`, use `model_construct`, set `extra=ignore`, remove arbitrary
fields, mutate accepted requests or provide a live execution option. Monkeypatch
contexts restore settings/classes and observation hooks at fixture exit.

Current adapter-reconstruction tests now include the current child policy.
Historical golden comparisons and the subject-only v3-to-v4 migration comparison
use the policy-unset v4 fixture. Historical canonical-boundary tests retain both
the accepted 10,000-byte witness and rejected 10,001-byte witness. Current tests
add three stage-specific 10,000-byte child-budget rejections and three independent
canonical-limit rejections using compact UTF-8 below the raw ceiling. Raw-boundary
tests continue running against current L1 unchanged.

There is no change to the inference boundary, workflow scheduling, transport,
application error handling, API, persistence, security, financial admission,
publication, Q&A or production configuration handling. No dependencies were added.

## Frozen-source conflict and narrow compatibility approach

Literal pre-G1 source equality and the intentional G1 additions cannot both hold
for complete current declarations. Broadly ignoring new AST nodes or replacing
the old hashes would erase useful contract protection. Instead,
`managed_g1.patch` records the exact three-module delta already present in
engineering commit `d940443`, generated once for review with:

```sh
git diff d940443^ d940443 -- documents/digestion/managed.py documents/digestion/models.py documents/digestion/validation.py
```

The file is fixed test evidence; tests never regenerate it. The test-only
`source_before_g1` helper requires a recognized module and exactly one matching
patch section. It reverses mandatory contextual hunks, each occurring exactly
once, in memory. It neither executes projected code nor writes any module.
Altered/missing admission predicates, serializers or settings extensions fail
before comparison. Unrelated text remains visible to the existing contract
checks. Seven new tests mutate/remove the additions, preserve unrelated edits
and reject unknown modules; the original source canonicalizer and its mutation
suite remain unchanged.

The projected renderer must still reproduce the **original** v4 whole-file
checksum `fa6cd701b73c0cdd486b645a64748f3bb70509b17d310b40c9455c619dbc91a9`.
The projected domain declarations and validator must still match the original
fixed excerpts with the original restricted diagnostic exception. This is an
explicit reviewable exception for the known G1 delta, not a new approved
fingerprint for arbitrary current implementation changes.

The fixture README now explains that `managed_prompt4.json` describes pre-G1 v4,
and documents this source exception and historical/current configuration scoping.
No prior report or original historical evidence was rewritten.

## Historical contract and checkpoint verification

The original v3 source checksum remains
`5b272d4a7591692eeeb328da09bc39b35d402bebd1d8ada3b891f6b1d6e8928c`.
All nine original v3 request/generation/payload hashes and all nine original v4
hashes remain unchanged. The provider-schema fingerprint remains
`4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2`.
The original `models.py.txt`, `validation.py.txt`, `managed_prompt3.py.txt`,
`managed_prompt4.json` and subject paragraph retain their original bytes.

New parametrized tests reconstruct both policy-unset v4 and G1 settings under
strict Pydantic validation. Settings/profile JSON round trips preserve equality,
profile digests and configuration bindings; absent optional policy fields remain
absent. Unexpected configuration fields still raise `ValidationError`. A matching
adapter reproduces its original `GenerationRequest`; cross-policy requests are
rejected in both directions with `incompatible_checkpoint` before transport.

Actual synthetic v3 checkpoints remain readable through the immutable object
store and codec. Actual v4/G1 child checkpoints are also read under their original
profiles and retain their exact results. Existing tampered checkpoint, policy
removal, wrong model/config/profile and v3-to-v4 stale-request negatives remain.
Readable stored data does not authorize silent request/profile migration.

## Exact commands and regression results

All pytest invocations below used this command prefix from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/phase17h-g1-g2:. PYTEST_PLUGINS=offline_guard HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python -m pytest
```

The inspected existing plugin is `/tmp/phase17h-g1-g2/offline_guard.py`; logs and
JUnit XML are outside the repository in `/tmp/phase17h-ci-reconciliation/`.
There is no `-k`, `-m`, `--ignore`, deselection, xfail addition or skip addition.

| Run | Arguments appended to the prefix | Result |
| --- | --- | --- |
| Original full CI scope | `--junitxml=/tmp/phase17h-ci-reconciliation/baseline.xml` | **1,803 passed, 15 failed, 13 errors, 0 skipped**, 51 warnings, 435.18 s. The process collected the original 1,831 tests before edits. |
| Original affected modules | `-q tests/integration/test_live_failure_observability.py tests/integration/test_final_offline_azure_compatibility.py --junitxml=/tmp/phase17h-ci-reconciliation/affected-before.xml` | **207 passed, 15 failed, 13 errors, 0 skipped**, 9.11 s. |
| First corrected run plus source guard | `-q tests/integration/test_live_failure_observability.py tests/integration/test_final_offline_azure_compatibility.py tests/unit/test_g1_source_compatibility.py --junitxml=/tmp/phase17h-ci-reconciliation/affected-after.xml` | **245 passed**, 22.22 s, after correcting one newly introduced test described below. |
| Final affected and historical/source regression | `-q tests/integration/test_live_failure_observability.py tests/integration/test_final_offline_azure_compatibility.py tests/unit/test_g1_source_compatibility.py tests/unit/test_source_contracts.py --junitxml=/tmp/phase17h-ci-reconciliation/affected-historical-final.xml` | **301 passed, 0 failed, 0 errors, 0 skipped**, 33.59 s. JUnit comparison confirms all original 28 failing/error node IDs are present and passing. |
| G1, G2, four-call L1 and existing preflight workflows | `-q tests/unit/documents/test_managed_sizing.py tests/integration/test_phase17h_two_chunk.py tests/integration/test_phase17hl_offline_e2e.py tests/integration/test_foundry_offline_workflow.py --junitxml=/tmp/phase17h-ci-reconciliation/g1-g2-l1.xml` | **56 passed, 0 failed, 0 errors, 0 skipped**, 40 warnings, 172.35 s. |
| Final complete CI-equivalent offline suite | `--junitxml=/tmp/phase17h-ci-reconciliation/full-final.xml` | **1,850 passed, 0 failed, 0 errors, 0 skipped**, 51 warnings, **530.73 s**, exit **0**. All original 1,831 node IDs are present; all original 28 failing/error nodes pass. |

The first new guard test attempted to token-compare an entire renderer module
containing formatted strings. The pre-existing canonicalizer deliberately rejects
that grammar. One new test failed while all 28 original failures/errors were
resolved. The test was corrected to check that an unrelated edit survives source
projection exactly, without widening the canonicalizer. An intermediate expanded
historical run passed **298 tests** in **26.72 s**; the final run also includes
three subsequent independent current canonical-boundary tests. The final full
suite contains 125 live-failure-observability cases, 122 final-compatibility cases,
47 original source-contract cases and seven new source-exception cases. Nineteen
new cases comprise six binding/checkpoint cases, six current output/admission
cases and seven source-exception cases. Final XML contains no failure, error or
skip elements. The final network-guard count is **0**. Both original and final
full runs emitted 51 nonfatal warnings, including existing `record_property` /
JUnit xunit2 warnings; none were hidden or converted to exclusions.

Compilation succeeded with exit 0:

```sh
PYTHONPYCACHEPREFIX=/tmp/phase17h-ci-reconciliation/bytecode HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python -m compileall -q .
```

Scoped fatal-error lint and full lint of the new Python modules both succeeded:

```sh
ruff check --no-cache --select E9,F63,F7,F82 tests/g1_source_compatibility.py tests/unit/test_g1_source_compatibility.py tests/integration/test_live_failure_observability.py tests/integration/test_final_offline_azure_compatibility.py
ruff check --no-cache tests/g1_source_compatibility.py tests/unit/test_g1_source_compatibility.py
git diff --check
```

Docker/Compose/Helm/Kubernetes checks were not run: there are no related changes,
and they are outside the necessary offline test correction. This report claims
the CI-equivalent **test** scope, not execution of every infrastructure step in
the GitHub workflow or a successful new remote CI run.

## G1/G2 and four-call L1 evidence

G1 tests retain legacy escaped-envelope overflow reproduction, near-10,000-byte
historical acceptance, current child-budget rejection, escaped/Unicode handling,
planner fan-in bounds, exact complete child material, and removed-policy rejection.
G2 retains the two-analysis/structural/root/Q&A five-call hierarchy with complete
coverage, qualifications, unresolved contradictions, original citations, immutable
checkpoints, publication readiness, checkpoint reuse and negative containment.
The existing four-call L1 fixture retains chunk/structural/root/Q&A execution,
settlement, publication and citation checks. No fake replaces an application
acceptance decision or repairs evidence. The focused group passed all 56 cases;
per-module results are **11 G1 sizing**, **9 G2 two-chunk**, **31 L1 end-to-end**,
and **5 existing preflight workflow** passes. Each module has zero failures,
errors or skips. Baseline, focused historical and G1/G2/L1 main-interpreter
network-guard counts are all **0**.

## Implementation self-review and separate pre-commit review

Self-review examined the complete test diff, fixture ordering/restoration,
constructor validation, historical source execution checksum, config provenance,
checkpoint binding, output-check order, no-truncation assertions, source-exception
scope and mutation tests. It confirmed that the default current fixture and
production L1 harness keep G1, while historical construction is explicit and
limited to test-only replay. No application refactor was required.

The separate pre-commit review checked the exact eight-file inventory, empty
index, complete changed/new Python, fixture provenance, Markdown links, trailing
whitespace/newlines, common credential/private-key patterns and scope. It found
no added test exclusions, validation bypasses, private configuration, debug
statements, temporary outputs, dependencies or unrelated application/API changes.
All five original evidence fixtures were compared byte-for-byte to HEAD; the
fixed delta was compared byte-for-byte to the original G1 diff. Fatal-error lint
and `git diff --check` were rerun successfully on the final Python changes.
Generated logs, XML, databases and bytecode remain outside the repository.
No Git mutation occurred during review. Final `git status --short --branch`,
`git diff --stat`, `git diff --cached --name-only` and `git log -1 --oneline`
confirm:

```text
Branch: master; HEAD: f3a2a87 (unchanged)
Status: 3 modified tracked files, 5 new untracked files
Tracked diff stat: 3 files changed, 176 insertions(+), 18 deletions(-)
Index: empty
Commit/push: none
```

The five new files do not appear in the tracked-only diff stat. The eight-file
inventory below includes them. Final documentation/whitespace/link checks were
also repeated after recording the complete results.

## Changed-file inventory

Exactly these eight task files are intended:

1. `tests/integration/test_final_offline_azure_compatibility.py` — explicit
   historical/current capture, matching current config, scoped historical byte
   acceptance and new current output/admission negatives.
2. `tests/integration/test_live_failure_observability.py` — correctly configured
   v3/v4 replay, unchanged golden comparisons with the G1 source exception,
   current subject tests and historical/current binding/checkpoint verification.
3. `tests/g1_source_compatibility.py` — fail-closed, in-memory exact G1 source
   projection used only for historical comparisons.
4. `tests/unit/test_g1_source_compatibility.py` — seven source-exception boundary
   and mutation cases.
5. `tests/fixtures/digestion_contracts/managed_g1.patch` — fixed reviewable delta
   of the three approved G1 source changes, without altering old references.
6. `tests/fixtures/digestion_contracts/README.md` — explains historical/current
   contract scope, delta provenance and restrictions.
7. `docs/codex/prompts/phase_17h_ci_failure_and_historical_contract_reconciliation.md`
   — normalized task prompt.
8. `docs/codex/reports/phase_17h_ci_failure_and_historical_contract_reconciliation.md`
   — this permanent engineering report.

## Remaining risks and readiness

**PASS** applies to this offline CI correction: every reported failure/error is
resolved, all historical evidence/hash checks pass, G1/G2 and four-call L1 remain
valid, the complete suite passes without exclusions, and the permanent prompt and
report are complete. There are no remaining observed compatibility failures.
Exact-runner parity is limited by the Torch wheel label and local runner
environment described above.
The fixed source delta is deliberately strict: future edits inside its contextual
hunks require explicit review, even when behavior-neutral. It must not be
automatically refreshed. Synthetic contracts prove structural/operational
compatibility, not model quality or new live operator readiness.

No historical request is automatically upgraded, no invalid checkpoint is made
acceptable, and no new live execution is authorized by this correction. The
owner must review the uncommitted files and run remote CI after their own Git
operations. Subsequent live authorization remains a separate phase.

Suggested conventional commit message:

```text
test(digestion): reconcile G1 admission with historical CI contracts
```
