# Phase 17H–L — managed-prompt/4 subject-contract implementation

Date: 29 October 2026. Scope: local implementation and offline regression only.

## 1. Executive summary

**COMPLETE for the authorized engineering implementation.** The active managed
prompt now explicitly restricts populated subjects to factual claims. It tells
all four non-factual kinds to emit null, permits null factual subjects, preserves
Token constraints and source-supported facts, and prohibits changing kind merely
to retain a subject. This addresses the confirmed instruction omission behind the
Attempt 5 `claim_contract / subject_on_nonfact` rejection without changing the
authoritative domain validator or either generation schema.

The migration selects **v4-only active execution with fail-closed stale bindings**.
New StageProfiles and planned requests use `managed-prompt/4`; explicit v3 stage
settings fail configuration validation. Rendering also checks prompt and inference
profile labels alongside the existing configuration fingerprint. Original v3
source and nine request witnesses remain independently reproducible in isolated
offline tests, outside the production execution path.

**447 distinct selected tests passed; final failures 0, skips 0, observed network
attempts 0.** A final 22-test recheck passed after improving the synthetic historical
checkpoint-readability control. Compilation and whitespace checks passed. Ruff
reports 42 findings on pre-existing code; unrelated lint cleanup was deliberately
excluded. Actual future model compliance remains untested.

Attempt 6 engineering status: **CONDITIONAL GO for a separately authorized future
preparation/review task**. There is no live authorization, eligible configuration,
new signed approval or financial authority from this implementation. No Attempt 6
packet or actual-scope request was prepared.

## 2. Starting repository state

The measured baseline was **20 modified tracked files, 122 untracked files and
zero staged files**. Tracked diff: **832 insertions, 79 deletions**. This confirms
the supplied 121+ untracked estimate; it is not a clean-checkout baseline.

Already modified tracked files:

- `.env.example`
- `docs/security/phase_17g.md`
- `documents/digestion/codec.py`
- `documents/digestion/managed.py`
- `documents/digestion/models.py`
- `documents/digestion/validation.py`
- `documents/publication/analysis.py`
- `governance/execution.py`
- `governance/ledger.py`
- `llm/bounded_http.py`
- `llm/inference.py`
- `llm/ollama_client.py`
- `llm/openai_compatible.py`
- `llm/structured.py`
- `security/identity.py`
- `security/runtime.py`
- `tests/integration/test_managed_digestion.py`
- `tests/unit/documents/test_managed_inference.py`
- `tests/unit/publication/test_analysis.py`
- `tests/unit/test_structured_provider.py`

Before modifying source, the task captured a file-level SHA-256 inventory of 405
tracked/untracked repository files, full file-level status, tracked diff/stat, and
copies of the two already-modified tracked files this task edits. Temporary
snapshots and test output live under `/tmp/polymind-prompt4-implementation/`.
The v3 managed source checksum and historical executor/generation/schema/settings
fingerprints were independently verified before editing. Ten existing frozen
checks passed at baseline with zero network attempts.

This task changes nine existing files and adds five files, all listed in section
11. Only two of its existing-file edits are tracked in the starting checkout:
`managed.py` and `test_managed_inference.py`. The other edited files were already
untracked work and must be retained during any later user review. No reset,
cleanup, stash, commit, push or unrelated formatting was performed.

## 3. Source implementation

Only `documents/digestion/managed.py` changes production behavior:

- `StageProfile.template_version` accepts/defaults to `managed-prompt/4`.
- `ManagedSynthesisInference.profile()` derives the planning prompt binding from
  the configured chunk StageProfile. Every valid StageProfile has the same v4
  literal, so chunk, intermediate, structural and root agree.
- `ManagedSynthesisInference.render()` rejects mismatched prompt/inference profile
  labels with `incompatible_checkpoint`, in addition to the existing settings
  fingerprint check. It inserts exactly the following paragraph beside the
  existing claim kind/status instruction.

```text
Only kind="fact" may have a non-null subject.
For kind="unknown", "unsupported", "commentary", or "structural", include subject=null.
Never use an empty or blank string instead of null.
For a fact, subject may also be null. A populated subject must be 1–128 characters
matching ^[a-zA-Z0-9_./:-]+$ and identifies a structured proposition, not a general topic.
Do not change a claim's kind to fact merely to retain a subject.
Facts must still have supported status and authorized source support.
```

`generation_schema()` is unchanged. There is no provider-specific prompt branch,
prompt registry, fallback, normalization, second pass or extra inference stage.
Three tests compare complete old/new instruction prose after removing exactly the
new paragraph; all remaining prose, including the deferred source-coverage
ambiguity, is identical. All four stage task variants render under v4 and retain
field completeness, evidence restrictions and deterministic identity instructions.

## 4. Domain-contract preservation

`documents/digestion/models.py`, `validation.py`, `diagnostics.py` and `codec.py`
match their starting file hashes. Existing dirty changes in those files were not
reverted or attributed to this task. `stage-result/1` remains authoritative.

The new **35-case matrix** uses real extraction, evidence resolution, planning,
deterministic IDs and complete `validate_result()` acceptance. It covers each of
fact, unknown, unsupported, commentary and structural against explicit null, a
128-character valid token, missing field, empty string, whitespace-only string,
invalid token and wrong type. Null is accepted for all kinds; a populated valid
subject is accepted only for facts. Missing subject remains application-default
compatible while both generation schemas reject omission. Invalid tokens/types
retain Pydantic rejection and sanitized reason attribution.

A valid populated non-factual subject still passes both schemas and Pydantic,
then yields **`serialization_error / claim_contract / subject_on_nonfact`**.
Four counting-fake tests prove exactly one attempt, non-retryable classification,
completed admission accounting, unchanged raw response and content-free error
information. Diagnostics exclude claim text, subject value, source text, evidence
IDs and complete raw content. Existing privacy tests also retain arbitrary-error
and credential-marker protections.

Existing negative controls continue rejecting wrong positional IDs, wrong origin,
foreign evidence, unsupported/source-free facts, extra fields, invalid tokens,
incomplete source coverage, malformed JSON and duplicate keys. Evidence lineage,
qualification inheritance, contradiction handling and claim ordering are unchanged.
The source-contract suite independently protects the domain declarations and all
acceptance predicates/order against mutations.

## 5. Provider-schema preservation

Recomputed before and after:

- `fingerprint(generation_schema())`:
  `a051949799a312d1aa15a5959bbe7d558265cfc38f6ce992eb97fbdbdff212ab`.
- `fingerprint(provider_schema(generation_schema()))`:
  `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2`.

Regression assertions pin both complete structural outputs. `azure-strict/1`
still has the same closed objects, all fields required, enums and nullable subject
shape. It intentionally does not enforce subject/kind coupling. The matrix
preserves a witness of that gap instead of claiming schema enforcement improved.
`llm/azure_schema.py` and `llm/openai_compatible.py` match baseline bytes.

Tests retain **3,000 completion tokens; 10,000 raw bytes; 10,000 canonical bytes;
26,192 HTTP envelope bytes**. Request options, reasoning settings, no-tool mode,
retry/fallback policy and provider-attempt limits are unchanged. Existing fake
transport failure tests assert one call. The new subject-failure workflow test
also stops after one call and settles known synthetic usage once.

## 6. Version migration and historical evidence

Fixture classifications were applied explicitly:

| Classification | Treatment |
| --- | --- |
| HISTORICAL_IMMUTABLE | Original `MANAGED_SOURCE_SHA`, all nine `FROZEN_REQUESTS` values, model/validator excerpts, Attempt 5 reports and source bindings remain unchanged. |
| ACTIVE_VERSION_EXPECTATION | Version labels in managed unit, final compatibility, launcher and output-limit tests move to v4 because those tests construct new default profiles. |
| NEW_VERSION_4_EXPECTATION | Separate reviewed subject paragraph and new active source/request/generation/payload checksums in `managed_prompt4_subject.txt` and `managed_prompt4.json`. |
| UNRELATED_REGRESSION | No production regression found. An initial new test used an incorrect exception-message regex; it was corrected to the existing message without changing production. |

`managed_prompt3.py.txt` is a byte-exact copy of the pre-task source, SHA-256
`5b272d4a7591692eeeb328da09bc39b35d402bebd1d8ada3b891f6b1d6e8928c`.
A dedicated test fixture verifies that checksum before executing it under a
separate test module name. It temporarily substitutes three managed classes,
replays the existing synthetic offline workflow and restores the substitutions
before returning records. All nine original request/generation/payload hashes
match unchanged. This is test-only historical reproduction; production has no
v3 selection branch and never loads the archive.

The active source SHA-256 is
`fa6cd701b73c0cdd486b645a64748f3bb70509b17d310b40c9455c619dbc91a9`.
Separate v4 snapshots cover chunk, structural and root; intermediate is covered
by explicit rendering/validation tests using valid child material. Active hashes
differ from all corresponding v3 hashes.

Migration implications:

1. Explicit v3 StageProfile settings reject during parsing for every stage.
   Requests carrying a stale prompt label, inference label or settings digest
   fail before admission/provider execution. Historical launch source bindings
   are rejected by existing single-call and L1 validators before approval work.
2. Already validated StageResults remain readable and pass full acceptance against
   their original synthetic requests/evidence. An actual synthetic v3 checkpoint
   is read through the immutable object store and round-tripped unchanged.
3. Checkpoint schemas, content hashes, parent/plan checks and validators are
   unchanged. Readability does not grant permission to resume an old plan: the
   active managed handler retains its configuration check, and rendering rejects
   the historical request. No real historical checkpoint was opened or migrated.
4. New configuration/profile digests change planned stage IDs because planning
   binds them into IDs. The deterministic positional claim-ID algorithm is
   unchanged; new claims must use IDs supplied by the new plan.
5. New plans/requests must be generated explicitly for future work. Do not splice
   old checkpoint results or old rendered controls into those plans. Existing
   signed approval/configuration digests cannot authorize changed source.

No historical golden value was regenerated to make a failure disappear.

## 7. Offline regression results

The existing `/tmp/polymind_e2e_offline_guard.py` was inspected and installed
before application imports. It denies Python socket connect/send/DNS operations,
counts attempts including swallowed audit events, and fails a session if any are
observed. The task-local runner clears application/credential environment inputs,
disables third-party pytest autoload and bytecode writes, and uses the existing
`tests.settings_isolation` helper to suppress implicit application dotenv loading.
All stores/databases/caches/basetemps are disposable paths under `/tmp`.
This is Python-level network denial, not a claim of an operating-system firewall.
No inference-provider service was contacted.

| Module | Executed | Passed | Failed | Skipped | Observed network attempts |
| --- | ---: | ---: | ---: | ---: | ---: |
| `tests/unit/documents/test_managed_inference.py` | 49 | 49 | 0 | 0 | 0 |
| `tests/unit/documents/test_two_layer_output.py` | 81 | 81 | 0 | 0 | 0 |
| `tests/integration/test_final_offline_azure_compatibility.py` | 116 | 116 | 0 | 0 | 0 |
| `tests/integration/test_live_failure_observability.py` | 114 | 114 | 0 | 0 | 0 |
| `tests/integration/test_attempt3_serialization.py` | 7 | 7 | 0 | 0 | 0 |
| `tests/integration/test_output_limit_hardening.py` | 6 | 6 | 0 | 0 | 0 |
| `tests/unit/test_single_call_diagnostics.py` | 21 | 21 | 0 | 0 | 0 |
| `tests/unit/test_source_contracts.py` | 47 | 47 | 0 | 0 | 0 |
| `tests/integration/test_foundry_l1_launcher.py` — default offline command only | 1 | 1 | 0 | 0 | 0 |
| `tests/integration/test_validation_diagnostics.py` — untyped metadata and codec privacy only | 5 | 5 | 0 | 0 | 0 |
| **Distinct selected total** | **447** | **447** | **0** | **0** | **0** |

The first eight modules were run together with
`-k 'not sanitized_governed_audit'`: **441 passed, 5 deselected in 15.27 seconds**.
The excluded cases create/consume synthetic signed approvals. The remaining six
selected node instances passed in **1.49 seconds**. Signed-launcher integration
cases and approval-dependent diagnostic fixtures were inspected but not run.
Synthetic unsigned workflows still exercise temporary governance settlement,
admission and durable checkpoint behavior. No real financial authority is used.
Network counters are session-wide; every session reported zero, hence zero for
each listed module.

There are **55 new parameterized test cases in existing modules**: 11 managed
binding/counting cases, 35 matrix cases plus one historical-source gate case,
seven historical/v4 comparison cases, and one synthetic settlement case.
No new test module was created. Four existing stage-witness cases were strengthened
and active-version assertions migrated separately.

Additional verification is not added to the distinct total: pre-edit baseline
10 passed; initial new-tests run 47 passed/1 failed due solely to the wrong
exception-message regex; early version selection 18 passed; final version/source
and historical-checkpoint recheck **22 passed, 178 deselected in 2.66 seconds**.
That recheck followed test-only import cleanup and stronger checkpoint assertions.
No current failure remains. Historical 39/111/426/1,755 test counts were not reused.

The exact task-local runner invocations and JUnit XML are retained under
`/tmp/polymind-prompt4-implementation/` (`focused.xml`,
`launcher-diagnostics.xml`, `final-version.xml`). They are temporary verification
artifacts, not launch material. No full expensive suite was run.

## 8. Fingerprint results

The following were computed using the existing `executor_digest()`,
`generation_contract_digest()`, schema `fingerprint()` and managed adapter binding
mechanisms, before/after source editing, with network denial and settings isolation.
No private launch configuration was loaded or created.

| Binding | Before | After |
| --- | --- | --- |
| `executor_sha256` | `82fc01aa0447d4be758124cec0120a06db49f139f69ee6425b51b8696a6ad26f` | `d9af24e556305246ec145d15b3511e3e65fcf4e955e5b5f0dc550b4119b58a75` |
| `generation_contract_sha256` | `7d387a8595cf63e2ac944a25c4987a1b37392aa4adba8889914acf51ff9f0f59` | `74cf9320b0ebf6d45df531e81827c5a8710b5b4d58fa75aad05dfa5039552290` |
| `provider_schema_sha256` | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` |
| `inference_configuration` | `7eaa6b52ad387f9f0c82e318e9c74fa378ffda0baec85d0f7157cc4ab0553519` | `71adc072da8e99d47b81afa859e78bde4866e633ae0e841e0b17f48d6450b831` |

The inference configuration calculation uses the same public settings and
render-only model identity as `prepare_analysis()`, without invoking preparation
on an actual scope or constructing transport. The source/default changes explain
the executor, generation-source and settings digest changes. Schema fingerprints
remain identical. There are no unexpected fingerprint changes.

The synthetic offline-model chunk request changes from
`12f09a58b2798efd124334559d8c1c692d0614422ec748475b6a8b6bf69a7f3b` to
`62eb2c247d2c55117920a5908a6e7de6ef00b14ee7eac23f47fc8d99037ab6bd`.
Its rendered `GenerationRequest` changes from
`cb41fb6fbca5f160b97ac16152955e5a5029dc83c400702821b4302232d71659` to
`0094d4bf941fa88ac95de483bc9561674457acb0ebfebaf133699967426c71f2`.
Its wire payload changes from
`b2a6745cbe2607f0bc44ff6c9b1b679c223ee66994401942e84b48461c0c5533` to
`8c5065034bdab1c16e355fa03bf2c63eb95828489a8cfce36fb70cc947e24c92`.
All structural/root component bindings are recorded separately in the new fixture.
These are synthetic regression identities, not future actual-scope launch hashes.

A complete future private configuration digest must be recomputed from a new,
separately authorized actual-scope configuration. None is provided here. Historical
Attempt 5 hashes remain unchanged in historical reports and protected artifacts.

## 9. Implementation limitations

The confirmed correction is explicit generation guidance, proven present across
all four profiles. Offline synthetic results prove acceptance/rejection boundaries
and binding integrity, not how a future GPT-5.4-mini completion will behave.
Successful strict provider output may still fail application validation, and the
existing validator must continue to reject it without repair or extra calls.

Kind-specific structural schema alternatives remain deferred pending compatibility
assessment. The unavailable-analysis/source-coverage ambiguity, qualification
wording and broader prompt simplification remain deferred. No part of the inactive
proposal's full patch was applied. The task's `docs/proposals/...` reference does
not exist in this checkout; the historical material was found and reviewed at
`docs/codex/proposals/phase_17hl_generation_instruction_clarifications.md` and kept
unchanged. Prior live-execution report checkpoints were also kept unchanged; the
completed post-execution diagnostic remains the terminal outcome authority.

Ruff's scoped command returned nonzero with **42 existing findings** in unchanged
imports, fixture imports/shadowing, broad exception assertions, dict constructors
and unused variables. Newly introduced local import warnings were fixed; the
hash-pinned historical fixture execution has a documented narrow S102 suppression.
No unrelated autoformat or lint cleanup was performed. The complete lint check is
therefore not reported as passing. No dependency or deployment validation was
needed; Docker/Kubernetes/Azure checks were deliberately not run.

## 10. Attempt 6 preparation implications

Separately authorized future work must complete all of the following:

1. New generation preparation using the actual authorized owner scope and v4 plans.
2. Fresh rendered request, executor, generation, schema and settings bindings.
3. A new private launch configuration and complete validated configuration digest.
4. New operator attestations covering exact capacity, credentials, costs and scope.
5. Fresh verified Entra authentication through the existing identity boundary.
6. A new independently signed approval for the exact new configuration and
   appropriate single-analysis audience; Attempt 5 approval is non-transferable.
7. New financial authority under existing governance policy and accounting checks.
8. A new eligible execution window satisfying all existing validity margins.
9. Exactly one separately authorized provider attempt, with retries/fallbacks zero.

These are prerequisites only. None was prepared, signed, authenticated or executed
in this task. Attempt 5 remains completed, rejected at the subject contract and
financially SETTLED; its run, replay markers and credential window are immutable.

## 11. Repository integrity and safety

Implementation self-review inspected the complete production delta against the
captured dirty baseline, all new tests/fixtures and migrated expectations. Only
one production file is necessary. The other prompt instructions, generation schema,
provider settings, public error mapping, resource handling and validation paths
are unchanged. All new cases use synthetic data. The v3 fixture's checksum is
verified before test-only execution and class substitutions are restored.

A separate pre-commit review found no secrets, private configuration, model-response
content, credential paths, debugging statements, introduced TODOs, dependency
changes or generated runtime artifacts in task additions. Reports contain fixed
instructions and public source/configuration hashes only. Temporary test output
and bytecode remain outside the repository. No real trust, signing key, replay,
run directory or authority database was opened. No signing or approval consumption
occurred. Disposable synthetic ledgers were created/settled only by offline tests.

All **22 protected repository files** selected from the forbidden domain/provider,
admission/budget/approval files and every existing `security/`/`governance/` source
match baseline SHA-256 values. Every other pre-existing repository file outside
the nine intended edits also matches baseline; none was removed. Protected private
state was not opened for a separate inventory, so this report does not claim an
independent audit of that state. There was no operation targeting it.

Existing files changed by this task:

- `documents/digestion/managed.py`
- `tests/unit/documents/test_managed_inference.py`
- `tests/unit/documents/test_two_layer_output.py`
- `tests/integration/test_live_failure_observability.py`
- `tests/integration/test_final_offline_azure_compatibility.py`
- `tests/integration/test_foundry_l1_launcher.py`
- `tests/integration/test_output_limit_hardening.py`
- `tests/fixtures/digestion_contracts/README.md`
- `docs/engineering/llm_structured_output_validation.md`

New files:

- `tests/fixtures/digestion_contracts/managed_prompt3.py.txt`
- `tests/fixtures/digestion_contracts/managed_prompt4_subject.txt`
- `tests/fixtures/digestion_contracts/managed_prompt4.json`
- `docs/codex/prompts/phase_17hl_managed_prompt4_subject_contract_implementation.md`
- `docs/codex/reports/phase_17hl_managed_prompt4_subject_contract_implementation.md`

Validation outcomes:

- `git diff --check`: PASS.
- `PYTHONPYCACHEPREFIX=/tmp/polymind-prompt4-implementation/bytecode python -m compileall -q .`:
  PASS (external bytecode cache; no ownership changes).
- Focused offline pytest: PASS, 447 distinct cases; final affected-version recheck:
  PASS, 22 cases.
- Scoped `ruff check --no-cache`: nonzero, 42 existing findings as explained above.
- Full suite, cloud/deployment tools, inference and signed-approval tests: not run.

Final `git status --short --untracked-files=no`:

```text
 M .env.example
 M docs/security/phase_17g.md
 M documents/digestion/codec.py
 M documents/digestion/managed.py
 M documents/digestion/models.py
 M documents/digestion/validation.py
 M documents/publication/analysis.py
 M governance/execution.py
 M governance/ledger.py
 M llm/bounded_http.py
 M llm/inference.py
 M llm/ollama_client.py
 M llm/openai_compatible.py
 M llm/structured.py
 M security/identity.py
 M security/runtime.py
 M tests/integration/test_managed_digestion.py
 M tests/unit/documents/test_managed_inference.py
 M tests/unit/publication/test_analysis.py
 M tests/unit/test_structured_provider.py
```

Final file-level status: **20 modified tracked files, 127 untracked files, zero
staged files**. The five additional untracked files are exactly the new files
listed above. No new test modules exist.

Final `git diff --stat` (includes preserved pre-existing work and excludes all
untracked content):

```text
 .env.example                                   |   5 +
 docs/security/phase_17g.md                     |   2 +
 documents/digestion/codec.py                   |  52 +++++++-
 documents/digestion/managed.py                 |  76 ++++++++++--
 documents/digestion/models.py                  |  41 +++++-
 documents/digestion/validation.py              | 165 +++++++++++++++++++++----
 documents/publication/analysis.py              |   7 +-
 governance/execution.py                        |  28 ++++-
 governance/ledger.py                           |  74 ++++++++++-
 llm/bounded_http.py                            |  75 +++++++++--
 llm/inference.py                               |  18 +++
 llm/ollama_client.py                           |  16 ++-
 llm/openai_compatible.py                       |  95 ++++++++++++--
 llm/structured.py                              |  82 +++++++++++-
 security/identity.py                           |  61 ++++++++-
 security/runtime.py                            |   5 +-
 tests/integration/test_managed_digestion.py    |  10 ++
 tests/unit/documents/test_managed_inference.py | 117 ++++++++++++++++++
 tests/unit/publication/test_analysis.py        |   3 +
 tests/unit/test_structured_provider.py         |  43 +++++++
 20 files changed, 894 insertions(+), 81 deletions(-)
```

The tracked total is **894 insertions and 81 deletions across 20 files**, compared
with 832/79 at baseline. This is not the total size of this task: most test/doc
files were already untracked and are absent from Git's tracked diff statistics.

**External provider calls: 0. Azure/cloud/deployment operations: 0. Approval/signing
operations: 0. Real financial mutations: 0. Protected-state modifications: 0.
Commits: 0. Pushes: 0.**

All implementation acceptance criteria are established within the authorized
offline scope. Future model compliance, private configuration readiness and live
authorization remain explicitly unverified prerequisites, not automatic passes.
