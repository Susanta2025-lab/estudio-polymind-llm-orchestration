# Phase 17H v5 reducer sizing: offline reconciliation

Recorded 9 November 2026. Starting HEAD:
`2b8a5ac73beb32d7febc53f77d0c3a459c8e3394`, on `master`.
The [task record](../prompts/phase_17h_v5_reducer_sizing_offline_reconciliation.md)
preserves the objective and execution boundaries.

**Final verdict: PASS — OFFLINE REDUCER SIZING RECONCILED.** This report concerns offline engineering
only. It neither completes Phase 17H nor authorizes another paid evaluation.

## Original failure and deterministic reproduction

The [historical execution report](phase_17h_v5_execution_window_renewal_and_rsa_authorization.md)
records two successful provider calls: an accepted chunk analysis and a rejected
first reducer. Root reduction, publication and Q&A did not run. The reducer
attempt was NON_RETRYABLE; application failure was `extraction_limit_exceeded`,
from `synthesis_limit_exceeded`, diagnostic `response_limit`. This was not the
separate raw/canonical response-byte limit. The 16,007-token input estimate plus
3,000 reserved output tokens fit the configured context. Those estimates are
conservative admission quantities, not the provider's billed token counts.

Before changing implementation, a network-disabled, read-only reconstruction
loaded the saved plan, extraction, accepted checkpoint and responses from the
private audit. Immutable object sizes/hashes were checked. No configuration was
loaded through the live launcher, and no authorization/signing helper was run.
Committed `validate_result` reproduced the exact original rejection:

| Contribution | Bytes |
|---|---:|
| Raw response, UTF-8 | 4,783 |
| Complete canonical ASCII result JSON | 4,783 |
| Result after embedding canonical JSON in the outer JSON string | 5,193 |
| Escaped required links for eight claims | 881 |
| Escaped allowed evidence-ID array, four distinct IDs | 165 |
| Conservative child-array punctuation | 8 |
| Unwrapped result contribution | **6,247** |
| Historical fixed wrapper reservation | 1,024 |
| Historical admission quantity | **7,271** |
| Configured per-child limit | **7,000** |
| Historical excess | **271** |

The recorded response is ASCII, with 410 double quotes and zero backslashes.
Thus UTF-8 and canonical byte lengths are both 4,783; escaping those 410 quotes
adds exactly 410 bytes. The eight-link array is 817 canonical bytes plus 64
escaped quotes, giving 881. The evidence array is 157 canonical bytes plus eight
escaped quotes, giving 165. `escaped_size` excludes the two outer string quotes;
its value already includes the JSON syntax of the embedded value.

The actual `ChildInput` wrapper, including its immutable artifact reference,
`material_kind`, inherited counts and `source_set`, contributes **620 bytes**.
This measurement reserves `max_artifact_bytes=32,000,000` in the artifact
reference's `byte_size` field before storage. Therefore the bounded actual
contribution is **6,247 + 620 = 6,867 bytes**, leaving **133 bytes** of real
per-child allowance. The fixed reservation exceeds the measured wrapper by
404 bytes, explaining both the rejection and the unused allowance:
`7,271 - 404 = 6,867`. Hash inventories of the private audit matched before and
after both investigations. No private response text or identifiers were copied
into permanent fixtures.

## Root cause and planning-versus-validation contract

There was no UTF-8 counting bug, escaping omission or accidental double addition
of the 1,024-byte reservation. The original result validator deliberately
reserved that amount once, exactly as the v5 prompt instructed. This was a
conservative, intentional fail-closed rejection under the original generation
contract. It was stricter than the actual downstream material contract and the
worker's existing second check, which already measured the complete child before
writing its checkpoint. The unnecessary fixed allowance caused this particular
sizing rejection; it did not establish that the actual next-stage material was
too large.

| Boundary | Historical v5 | Reconciled v6 |
|---|---|---|
| Raw response | UTF-8 bytes <= 10,000 | Unchanged |
| Canonical result | Complete compact ASCII JSON <= 10,000 | Unchanged |
| Early generated-result admission | Escaped contribution + 1,024 <= 7,000 | Escaped contribution alone <= 7,000; necessary early bound |
| Pre-checkpoint material admission | Complete child contribution <= 7,000 | Same bound, centralized, with explicit diagnostic |
| Finalization/replay | Content/provenance and inherited metadata revalidation | Same, plus explicit complete-child admission |
| Reducer planning | Fixed envelope + escaped path + 7,000 per child | Unchanged algorithm and per-child bound |
| Runtime reducer input | Actual child bound and full rendered envelope/context | Unchanged |

`result_contribution` includes the escaped generated result, next-stage required
links, evidence IDs and eight bytes of conservative punctuation.
`child_contribution` replaces the bare-result encoding with the complete
`ChildInput` encoding, retaining those links/evidence/punctuation. Evidence IDs
are counted per child even though the renderer deduplicates the combined allowed
ID set. Consequently multi-child summation remains an upper bound.

The planner cannot know future generated prose, qualifications, links or source
reference choices. It plans safely for accepted children of at most 7,000 bytes;
it does not promise that every schema-valid or 10,000-byte response will be
accepted. Long prose, many repeated IDs/links, escaping or Unicode can exceed
that bound while satisfying the separate schema, response and completion-token
limits. Such incompatibility remains a legitimate rejection.

The unchanged 7,000-byte boundary is a configured downstream safety allocation,
not a model's intrinsic context limit. With the new prompt, the fixed managed
envelope bound is **9,973 bytes**. For empty structural paths, one child reserves
**16,973** and two reserve **23,973**, below the 24,800-byte stage input limit.
Three would require 30,973 and cannot be planned. The complete maximum configured
reservation is `24,800 + 100 overhead + 100 safety + 3,000 output = 28,000`.
An 8,000-byte allocation would require 25,973 for two children and fails this
planning contract, as the existing impossible-fan-in tests verify. There is no
reason to increase the allocation to resolve an unrealized wrapper reservation.

## Selected correction and modified functions

The correction retains the result and lineage bytes exactly and defers only the
wrapper-dependent part of admission until application-owned inherited metadata
is available. It introduces no compression, truncation, evidence repair, extra
inference stage, retry, dependency or provider-specific branch.

In `documents/digestion/validation.py`, `validate_result` retains all existing
raw/canonical, identity, source, qualification, coverage and schema predicates.
It rejects a bare escaped contribution over the child limit immediately. Its
new docstring makes the two-part validation contract explicit: this function
alone does not admit a complete checkpoint. New `validate_child_material`
measures the unchanged result together with actual inherited metadata and a
worst-size artifact reference. UUIDs, scope identifiers and hashes have fixed
serialized widths; the maximum permitted artifact-size integer conservatively
bounds the future reference before storage.

In `documents/digestion/workflow.py`, `DigestionHandler.__call__` uses that helper
before checkpoint storage, replacing its existing inline equivalent. Finalization
also runs it after reconstructing and comparing inherited metadata for every
checkpoint, including the root. Failed material cannot acquire a committed
checkpoint manifest, final digest or publication through this path. Consumer
inspection found both production callers of `validate_result` in this workflow;
the standalone single-analysis harness has no managed child budget and does not
publish a hierarchical checkpoint.

`documents/digestion/diagnostics.py` adds the fixed, content-free
`child_material_limit` reason. Failure mapping remains
`extraction_limit_exceeded` / NON_RETRYABLE. `sizing.py` changes only a comment:
`CHILD_WRAPPER_BYTES=1024` remains exported for historical diagnostics/API
compatibility and is no longer an active output restriction. Planning and
serialization functions are unchanged.

`documents/digestion/managed.py` changes the wrapper instruction and prompt
version to `managed-prompt/6`. All schema, source-copying, stage-local reference,
qualification, contradiction, coverage and claim identity rules remain intact.
`tests/performance/foundry_l1.py::generation_contract_digest` additionally binds
`sizing.py`, `workflow.py` and `diagnostics.py`, so the complete admission behavior
is represented in the reviewed source inventory.

## An additional rejection exposed by deeper validation

Removing the excessive reservation does **not** make the original live response
acceptable. Read-only validation under the corrected sizing checks reaches
`inference_contract_error`, diagnostic `claim_identity`, reason
`originating_stage_mismatch`. All eight originating-stage values violate the
reducer-stage binding. All eight positional claim IDs are correct, with no
duplicates; the failure is specifically originating-stage identity. The earlier
sizing rejection had prevented this check from being reached.

No identifier was repaired, no response was rewritten, and no historical
checkpoint or execution status was changed. Further predicates after this first
identity failure are not claimed to pass. A permanent synthetic regression has
the same 4,783/7,271/6,867-byte shape and wrong originating-stage values; it remains
NON_RETRYABLE, preserves both settled synthetic calls and commits no reducer
checkpoint. This finding is an additional risk for future live acceptance, not
a reason to weaken G2 or the stage-identity contract.

## Permanent regression coverage and historical contracts

`tests/reducer_sizing_fixtures.py` constructs synthetic eight-claim/four-evidence
results with one qualification and complete child links. Placeholder text,
synthetic IDs and production encoding reproduce the exact serialized sizes,
without copying private model output. `tests/unit/documents/
test_reducer_sizing_reconciliation.py` contains **14 cases** covering the original
witness, 6,999/7,000/7,001 full-child boundaries, the artifact-size reservation,
quotes, backslashes, control characters, accented/BMP/astral Unicode, raw UTF-8
versus both JSON layers, preserved evidence/qualification/lineage, large inherited
metadata, and multi-child planner/runtime consistency.

The scalar escaping regressions measure these production-codec quantities;
canonical scalar sizes include their JSON string delimiters, and embedded sizes
exclude only the outermost encoding's two delimiters:

| Scalar | Raw UTF-8 bytes | Canonical ASCII JSON | Embedded contribution |
|---|---:|---:|---:|
| Double quote | 1 | 4 | 8 |
| Backslash | 1 | 4 | 8 |
| Newline | 1 | 4 | 7 |
| `é` | 2 | 8 | 11 |
| U+0800 | 3 | 8 | 11 |
| U+1F600 | 4 | 14 | 18 |

`tests/integration/test_reducer_sizing_offline_workflow.py` contains **9 cases**:
three complete boundary workflows, one-byte-over rejection at chunk/first/root
stages, stale generation/template rejection, binding of the complete sizing
source inventory, and the originating-stage failure exposed in the original
response. The 7,000-byte successful run is reopened and resumed with the same
checkpoint graph, without another provider call or ledger charge. Full material
validation is observed both before commit and during finalization.

Earlier tests exercised large 10 KB outputs and conservative successful shapes,
but successful fixture generation itself stayed below the fixed 1,024-byte
reservation. They did not isolate the region where actual material fits while
the reservation rejects it. They also did not test exact complete-child
6,999/7,000/7,001 boundaries through all durable stages. These gaps are now
permanent regression cases, rather than relying on the private live witness.

Existing current-template assertions are updated in the managed inference,
launcher, output-limit and compatibility tests. Historical v5 fingerprints and
their assertions are preserved, using a new byte-identical, checksum-pinned
snapshot `managed_prompt5.py.txt` from starting HEAD. New `managed_prompt6.json`
freezes complete current requests, generations and HTTP payloads. The compatibility
suite retains explicit v4 and v5 bounded/unbounded round trips and adds v6; it
verifies old bindings cannot be rendered by the current adapter.

The frozen G1 acceptance/source tests needed an explicit account of this
intentional sizing-contract change. `tests/fixtures/digestion_contracts/
reducer_sizing.patch` and `tests/g1_source_compatibility.py` reverse only the exact
new validation delta before applying the unchanged historical G1 projection.
Every patch hunk must match exactly once; unrelated changes remain visible.
Three additional mutation cases reject changed comparison operators or removal
of the maximum-artifact-size reservation. The old patch, v3/v4/v5 fingerprints,
G2 acceptance assertions and historical reports were not rewritten to accept
arbitrary changes.

## Complete offline four-call results

The established L1 PDF fixture, deterministic production planner, actual managed
renderer, provider HTTP adapter with an explicit synthetic transport, governance
and admission accounting, durable worker, local object/SQLite stores, digest
finalization, publication, retrieval and grounded Q&A were exercised. Socket/DNS
access was denied. Test authorities, prices, usage and transport responses are
synthetic and isolated in temporary directories.

For the 6,867-byte analogue of the original witness:

| Stage | Actual rendered input bytes | Planner input bound | Overhead + safety | Output reserved | Total context reservation | Canonical result | Complete child |
|---|---:|---:|---:|---:|---:|---:|---:|
| Chunk | 12,157 | 12,190 | 200 | 3,000 | 15,357 | 3,317 | 5,337 |
| First reducer | 15,291 | 16,973 | 200 | 3,000 | 18,491 | 4,783 | 6,867 |
| Root reducer | 16,824 | 16,973 | 200 | 3,000 | 20,024 | 1,311 | 2,172 |
| Grounded Q&A | 9,174 | Actual retrieved-envelope check | 200 | 3,000 | 12,374 | Valid source-cited answer | Not a reducer child |

The Q&A fixture returns **245 raw UTF-8 bytes**, within its separate unchanged
**12,000-byte** response bound. Its 3,000-token output reservation is unchanged.

Actual rendered input includes the complete system, nested data and schema
representation; the estimator intentionally treats ASCII JSON bytes as tokens.
All inputs fit 24,800 bytes and all combined reservations fit 28,000. This is
independent of the synthetic usage receipts and the four-call run guard's
25,000-input/3,000-output per-call reservations.

The two further successful runs use first-reducer canonical sizes **4,915** and
**4,916**, yielding complete child sizes **6,999** and **7,000**. Root actual inputs
are respectively **16,956** and **16,957**, still below 16,973. A **7,001-byte**
contribution is rejected before checkpoint commit at each of the three digestion
stages, despite being below raw/canonical response limits. The failed attempt
has classification NON_RETRYABLE and count one; dependants have no attempt or
manifest. Successful earlier checkpoints remain readable and known synthetic
usage remains SETTLED. No publication or Q&A follows failed digestion.

Successful runs have five SUCCEEDED durable steps (plan, three synthesis
checkpoints, digest), complete coverage of all four original evidence pieces,
two linked synthetic qualifications, an unresolved source contradiction,
publication with eight canonical citations, ready local retrieval and a Q&A
answer whose citation excerpt matches original extraction offsets. Qualification
text, source IDs and contradiction annotations reach Q&A through immutable
lineage; generated findings do not become source evidence. Broader existing
negative tests retain fabricated-ID, qualification, coverage, lineage, schema,
raw/canonical/transport-limit and citation refusals.

This is **synthetic offline success**, not Azure model-output acceptance.
Placeholder findings test structural/provenance contracts, not semantic truth.
Nothing here guarantees that another model response will satisfy all limits,
identity/provenance rules or independent human semantic review.

## Validation evidence and corrected intermediate failures

The final complete suite passed **1,910 tests in 491.75s (8m11s)**, with
**zero failures, errors, skips or xfails and zero network attempts**. JUnit
independently records 1,910 successful cases: **1,326 unit and 584 integration**.
The only warning is the existing
OpenTelemetry `SelectableGroups` deprecation in the real local Chroma test.
This is 38 additional cases relative to the starting 1,872-case suite, including
retention of the historical v5 round trips while adding v6 coverage.

The full command was:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  PYTHONPATH=.:/tmp/phase17h-g1-g2 python -m pytest \
  -p offline_guard -p no:cacheprovider \
  --basetemp=/tmp/phase17h-reducer-sizing-offline/full-final \
  --junitxml=/tmp/phase17h-reducer-sizing-offline/full-final.xml \
  -o junit_family=xunit1 -q
```

The pre-collection guard denies socket connect/connect_ex/sendto and connection/
DNS helpers; the permanent workflow modules also install their own offline
fixture. No tests were excluded from the complete run. The final 23-case focused
regression run additionally checks the latest raw Q&A output-size assertions.

| Final check | Result |
|---|---|
| Complete offline pytest suite | 1,910 passed |
| New unit/workflow regressions | 23 passed |
| Ruff critical rules, 17 Python files | PASS |
| Full default Ruff, five standalone test/helper modules | PASS |
| Ruff formatting, those five modules | PASS |
| Mypy scoped to all 17 Python files | Success: no issues found |
| External-cache `python -m compileall -q .` | Exit 0 |
| `git diff --check` | Exit 0 |
| New historical managed snapshot vs starting HEAD | Byte-identical |
| Exact validation-delta restoration vs starting HEAD | Byte-identical |
| Local Markdown links in the four changed/new documents | PASS |
| Changed/new file secret-pattern review | No findings |


The initial focused pre-regression run passed **284 tests in 22.39s**. The final
new unit/workflow modules passed **23 tests in 15.95s**, including boundary
recovery and per-stage/Q&A output checks. An earlier updated workflow-only run
passed **9 tests in 11.62s**.
The expanded observability/historical-contract module passed **149 tests in
20.11s**. Each used a pre-collection offline guard with zero network attempts.
These are overlapping runs, not counts to add to the complete-suite total.

Intermediate failures were investigated without changing production safeguards:
new scalar-escaping expectations had omitted the escaped quotes delimiting the
inner JSON string, a Unicode acceptance fixture actually exceeded 7,000 bytes,
and the root-failure fixture had only one supplied child claim while constructing
eight links. Correct expected byte counts, a bounded Unicode fixture and a full
eight-link synthetic parent resolve those fixture errors. The first complete
suite had **1,900 passed and three failed in 388.04s**: all three were a missing
local `OpenAICompatibleProvider` import in the new v6 compatibility test. Adding
the import passed all six new v6 tests; no assertion or acceptance predicate was
weakened to obtain a pass.

Ruff critical rules (`E9,F63,F7,F82`) run across all 17 changed/new Python files.
Full default Ruff and formatting checks run on the five new/reworked standalone
fixture/source-projection/regression modules. Mypy uses the existing separately
installed executable, Python 3.10, the repository interpreter for dependency
resolution, `--follow-imports=skip --ignore-missing-imports`, across the same
17 files. This is a scoped check, not a claim of repository-wide strict typing.
No tool or dependency was installed. Compilation uses an external bytecode-cache
directory to avoid unrelated ownership changes.

No Docker image, dependency or deployment configuration changed; a Docker build,
Compose operation, Kubernetes or cloud validation is inapplicable to this offline
source/validation correction. No such operation was performed.

## Compatibility, security and generation binding

Current generation-contract SHA-256:

```text
f6e568d450ac084c5977e4fef68823fb457cceacd22b361f047310c5d3512f5b
```

This intentionally supersedes the v5 digest:

```text
de9492c536c1435464e8d9e406cbd1491ea358bc45f817df72eb2ea2a0f69a71
```

The current managed source SHA-256 is
`6d744cf9ef412beaa2e25a48c80c2959ed6edf9d5fc8f873eaf1643686839f8f`.
The generation inventory now has 15 source files, including the three additional
admission/checkpoint/diagnostic modules. The stage schema remains `stage-result/1`;
no stored model or API response schema changes. The raw/canonical result limits,
HTTP envelope, completion tokens, child limit, provider capabilities, governance
policy and prices are unchanged.

`StageProfile` now accepts `managed-prompt/6`; an explicitly serialized v5 template
is incompatible. Fresh settings must select the new template deliberately, derive
the current inference/profile/plan bindings and recompute the generation digest.
Unbounded settings also acquire the new template identity; this is not a silent
upgrade of existing hashes. Existing stored domain artifacts remain readable,
but v5 requests/checkpoints cannot be resumed under a different v6 inference
binding. Old reviewed launch configurations and approval bindings must not be
reused or edited in place. Any future live work requires a separate readiness
review, fresh configuration and the existing independent authorization gates.
No new configuration or approval was created here, and the consumed approval
remains consumed.

The provider-neutral boundary, untrusted-data envelope, G2 predicates,
application-owned source/qualification lineage and contradiction propagation are
preserved. The new reason contains no provider content. No prompt or provider
response is logged by the new validation path. Actual result/checkpoint content
is never rewritten to satisfy sizing. Private audit files and historical
settlements/authority state were only read, never altered. No Azure inference,
Entra authentication, operator signing, real approval consumption, paid operation
or cloud mutation occurred. The complete regression suite includes existing
synthetic cryptographic/replay tests using test keys and temporary authorities;
these do not use operator keys or the consumed live approval.

## Self-review, pre-commit review and remaining risks

Implementation self-review traced both production result-validation callers,
all source consumers, both serialization layers, maximum artifact-reference
integer width, actual inherited metadata, root handling, pre-storage failure,
finalization/recovery, downstream rendering and immutable provenance traversal.
The actual child bound remains conservative even with duplicate evidence across
children. Large inherited integers are measured, not assumed to fit a fixed
wrapper. No provider-specific conditions, retries, resource handles or dependency
changes were introduced.

A separate pre-commit review covers the complete application/test diff and new
fixtures: no secrets, private responses, private IDs, `.env` files, temporary logs,
machine-specific production paths, debug output, introduced TODOs, accidental
imports/dependencies or unrelated changes. Frozen source projections are narrowly
specified and tested; historical snapshot bytes and hashes are retained. README
and the current evaluation runbook now identify v6 and link this report; dated
historical reports and private execution evidence remain untouched.

Remaining failures are explicit: oversized actual results or inherited metadata,
escaping/Unicode growth, insufficient room for mandatory lineage, malformed or
truncated provider output, wrong originating-stage/claim identity, unauthorized
or omitted source IDs, invalid qualifications, missing coverage, invalid Q&A
citations, unknown usage and revoked authority still fail closed. The planner
bounds admitted material; it cannot guarantee future generation behavior.
The original response's newly exposed originating-stage failure is unresolved
and must not be described as accepted or repaired. Future live readiness must
reassess complete current bindings, context, quotas, authority and financial
conditions without replaying old approval. No further paid attempt is authorized.

## Complete file manifest

The task changes 16 tracked files and adds eight files, all left uncommitted:

```text
README.md
docs/evaluation/phase_17h_foundry_validation.md
documents/digestion/diagnostics.py
documents/digestion/managed.py
documents/digestion/sizing.py
documents/digestion/validation.py
documents/digestion/workflow.py
tests/g1_source_compatibility.py
tests/integration/test_final_offline_azure_compatibility.py
tests/integration/test_foundry_l1_launcher.py
tests/integration/test_live_failure_observability.py
tests/integration/test_output_limit_hardening.py
tests/integration/test_phase17hl_offline_e2e.py
tests/performance/foundry_l1.py
tests/unit/documents/test_managed_inference.py
tests/unit/test_g1_source_compatibility.py
docs/codex/prompts/phase_17h_v5_reducer_sizing_offline_reconciliation.md (new)
docs/codex/reports/phase_17h_v5_reducer_sizing_offline_reconciliation.md (new)
tests/fixtures/digestion_contracts/managed_prompt5.py.txt (new)
tests/fixtures/digestion_contracts/managed_prompt6.json (new)
tests/fixtures/digestion_contracts/reducer_sizing.patch (new)
tests/integration/test_reducer_sizing_offline_workflow.py (new)
tests/reducer_sizing_fixtures.py (new)
tests/unit/documents/test_reducer_sizing_reconciliation.py (new)
```

## Git disposition and engineering verdict

Executed `git status --short --branch`, `git diff --stat`,
`git diff --cached --stat` and `git rev-parse HEAD` at final review.
Branch remains `master`; HEAD remains the starting commit. There are **16 modified
tracked files and eight new task files**, alongside **19 pre-existing untracked
Markdown documents preserved unchanged**. The tracked diff is **220 insertions,
58 deletions across 16 files**; the eight untracked deliverables do not appear in
`git diff --stat`. The staged diff is empty. No Git staging, commit, push or
remote-state modification occurred.

**PASS — OFFLINE REDUCER SIZING RECONCILED.** The original sizing failure was
reproduced, its conservative-wrapper cause quantified, and actual downstream
admission reconciled without increasing 7,000 bytes or changing result content.
Permanent regressions, the complete four-call synthetic workflow and applicable
quality checks pass. Strict identity/provenance and genuinely oversized-material
rejections remain. The original live response is still rejected for its separate
originating-stage violation; neither live acceptance nor semantic correctness
is established. This implementation is eligible only for a separate future
live-readiness review. Phase 17H remains partial; no paid evaluation is authorized.
