# Phase 17H v11: versioned reducer semantic-quality implementation

12 November 2026. **OFFLINE IMPLEMENTATION PASS**. The complete offline suite
passes 2,991 tests with zero failures, errors, skips or recorded network attempts.
Real-model semantic improvement remains unverified and formal Phase 17H closure
remains pending; neither follows from deterministic fixtures.

## Starting state and Step 1 preservation gate

The starting branch is `master`, HEAD
`ec22fa3d116696b80a1bb12ad17e2eb37db38cb3`, exactly the supplied successful
11 November v10 baseline. Initial Git status has **two modified tracked files,
33 untracked Markdown documents, zero staged changes**. The tracked delta is
exactly five added lines: one in `tests/performance/foundry_preflight.py` and
four in `tests/integration/test_foundry_l1_launcher.py`. All 33 inherited
untracked documents, including the history and history-documentation report,
are preserved. The supplied earlier 3-pass/5.43-second result remains an
attributed user-reported result, not a test performed by this task.

Before edits, read-only status, branch/HEAD, complete binary diff, diff statistics
and **199 file hashes** covering existing documentation and initially changed
files were recorded under `/tmp/phase17h-v11-preservation/`. The preservation
manifest contains no credentials, private keys, approvals or financial databases.
Hashes of the two inherited files are:

| File | Starting SHA-256, required unchanged |
| --- | --- |
| `tests/performance/foundry_preflight.py` | `64eab823cb076ba05961fdbd1de09d3c66c13fd9a41ef04574d6d5cc57620f2a` |
| `tests/integration/test_foundry_l1_launcher.py` | `7e14a46a95617d87339f3aa6237aaeb8b58691a37694c334383253e071327ae4` |

AGENTS.md, the required evaluation history, v10 implementation report, wire/receipt
ADR and readiness document were inspected. Inspection traced stage profiles and
settings, all explicit v10 checks, the 25-file inventory recipe, six-file managed
configuration binding, historical renderer fixtures, complete-envelope sizing,
G2, worker/ledger/storage, receipt reopening and publication consumers. Relevant
existing tests were read before changing their version-characterization setup.

All **25/25 committed source blobs** at the baseline match the unchanged
`managed_prompt10.json` source inventory. Hashing their sorted compact JSON
SHA-256 mapping reproduces exactly:

```text
e5fb249cc9b166b5e438f1534eb855fa5ab7531e08aa09314c110a1905327ebd
```

The starting working-tree fingerprint is already different:
`18bf21045291c9db08374696bdd1847bb906291019bb14d443720ec5f104fd7a`.
Its only inventoried difference from the executed commit is the pre-existing
`billable_calls` reporting correction. It is not represented as the executed
v10 fingerprint.

The [original execution/reconciliation report](phase_17h_v10_controlled_four_call_evaluation_and_reconciliation.md)
is unchanged. Its four calls, three accepted stages, nine associated objects,
complete digest, publication/Q&A, consumed-once approval, settled reservations,
EUR 0.010707841465063252 actual catalog token cost and EUR 0.242439068182 approved
ceiling remain historical facts. No historical provider response, rejected result,
checkpoint, receipt, source fingerprint, approval or settlement is rewritten or
regenerated. Private live artifacts are unavailable in this workspace, as already
recorded in the history; this task neither opens private authority stores nor
claims fresh receipt-level verification of unavailable originals. Preservation
here combines exact repository-byte verification with non-access to those stores.

Step 1 passes before implementation: exact baseline and hashing identified,
existing edits inventoried, original evidence protected and additive version
isolation established.

## Version registration and isolation

V11 is an **explicit opt-in** `StageProfile.template_version="managed-prompt/11"`
on all four configured profiles. The existing v10 default and its rendered task
prose remain unchanged. `ManagedSettings` rejects mixed template versions. This
avoids silently enabling an unvalidated quality change for existing callers.
The existing profiles configuration/environment mechanism is sufficient; no
new provider-specific setting, endpoint, service or dependency is introduced.

The protected controlled-L1 composition still constructs the default v10
profiles. This task does not add a turnkey v11 Azure-launch configuration or
change that composition. A future live-comparison task must explicitly bind
v11 selection in its reviewed harness/configuration, rather than use test
monkeypatches or assume the existing launcher selects v11. General managed
inference already accepts explicit v11 settings; offline tests select them
through that supported constructor. The preflight/reporting correction remains
byte-identical as required.

Both versions use `stage-proposal/1`, `stage-decoder/1`, canonical `stage-result/1`
and the existing three-object manifest. The wire constructor, workflow and source
sizing recognize both explicit versions; the single-analysis consumer recognizes
the same proposal path. V11 never falls back to canonical provider-generated IDs
or the historical one-object manifest convention. The G2 validator, receipt
implementation, canonical schemas/codec, planner, stable identity function,
provider transport, security/governance and database implementation are unchanged.

All new production instructions live in the already inventoried `managed.py`.
The existing 25-member `generation-inventory/2` remains complete; no new inventory
format is needed. The **current implementation fingerprint** is:

```text
managed-prompt/11 — generation-inventory/2
072aa2cd2a3be2ddb8e63b0577119e87312f44613c9532b56b6d6d9c5ff78fba
```

`managed_prompt11.json` separately pins all 25 current source hashes and nine
representative synthetic request, generation and real HTTP-builder payload hashes.
The source digest identifies the implementation supporting both selectable
profiles. The chosen template, complete settings/capability, provider/model and
six constructor/receipt/sizing/workflow source hashes further bind the managed
configuration; every plan, request/table and raw/receipt association includes
that compatibility identity. A fingerprint is not an execution approval.

For the unchanged bounded synthetic capability/provider witness, current v10
managed config is `c1e04f41cab9294a06d3fd8eba4da234626a86e6feda28005804b4f2a44b32da`;
v11 is `ea1e6adf01b6ca8ca8213b291dfb8ada6cfdf528d6df7372e5846ab65182565b`.
These are fixture bindings, not new production launch configurations. Current
source changes also change a newly constructed v10 config; old executed config
bytes are not falsely attributed to the working tree.

Six inventoried files that differ from the executed baseline are copied verbatim
from that commit to `tests/fixtures/digestion_contracts/v10_sources/`. They include
the original pre-correction preflight source. The other nineteen inventory files
must still match their original hashes. A test-only loader verifies every byte,
materializes the original source binding in temporary stores and renders v10
without changing its original golden JSON. All nine historical request/generation/
payload hashes remain meaningful and unchanged. The original commit also remains
available without checkout or history changes. Production never imports the
frozen test renderer.

Tests establish bidirectional v10/v11 renderer incompatibility, proposal-binding
mismatch and refusal to run an accepted job under the other managed config.
The existing general reprocessing API can admit a new queued job with a changed
profile; **zero** accepted manifests, reused stages or attempts are transferred
across versions. No worker runs that job in the incompatibility test. Same-version
multi-hop accepted reuse still succeeds without additional provider calls.
The original accepted v10 contract is reproduced synthetically and reopened
through current publication readers after the frozen renderer is deactivated.
This is accepted historical-contract testing, not rewriting/recreating actual
historical live outputs. Old generation bindings also fail the current launcher
inventory check; the consumed real approval is never loaded or reused.

## Reducer content and provenance responsibilities

Structural instructions now require useful section-level conclusions drawn from
substantive immediate-child findings. They retain important named entities,
measurements, procedures, requirements, results and genuine relationships, merge
related findings and avoid equivalent repetition while preserving distinctions.
The model must preserve material qualifications, uncertainty, conflicts and
limitations in readable synthesis as well as structured fields. Enumerating child
claims, counts or wrappers is explicitly inadequate.

Root instructions require a coherent concise standalone whole-document synthesis,
including the supported subject/purpose, important conclusions across sections,
essential relationships and consequential exceptions/contradictions. Unsupported
cross-section conclusions and pretending to inspect unavailable original material
are prohibited. Intermediate reducers share the content/provenance distinction
so metadata-heavy material is not encouraged earlier in a larger reduction tree.
Chunk task prose stays unchanged; all four profiles nevertheless carry the v11
identity so one plan cannot silently mix generation versions.

`claim.text` carries grounded domain meaning. Supporting, contradicting,
qualification-source and child selections stay in their existing dedicated
fields. Generated request-local E/C aliases must not replace explanatory prose;
literal identifiers appearing in the source domain remain valid. Machinery may
be summarized when it is itself the source subject. Complete immediate-child
coverage must use actual support; no unrelated citation, invented fact,
grandchild substitution or fabricated direct authority may fill a coverage gap.
The source data, generated material and inherited metadata remain visible and
untrusted; provenance is neither hidden nor removed to improve prose.

This is a generation instruction contract. It intentionally does not add a
keyword-based runtime semantic filter or weaken G2 to improve completion rates.
A pure negative counterexample demonstrates that G2-valid metadata prose can
still fail the semantic fixture checklist. Human source-grounding review remains
necessary for arbitrary claims.

## G1 calculations and unchanged limits

The renderer measures canonical ASCII JSON containing complete system instructions,
trusted CONTROL, escaped input data and schema. Existing capability overhead and
safety remain 100+100; reserved completion remains 3,000. `profile()` measures the
largest empty envelope across all four stage profiles, including nonempty-enum
scaffolding reserve. V11's longer root instructions automatically raise the fixed
planning base from **5,502 to 6,990 bytes**, a 1,488-byte increase. Conservative
planning retains the full canonical child wrapper and per-source reserve; actual
rendering remains an independent admission check.

| Limit | V10 and v11 |
| --- | ---: |
| Managed input allocation | 24,800 |
| Context window | 28,000 |
| Reserved output tokens | 3,000 |
| Overhead / safety tokens | 100 / 100 |
| Complete child material | 7,000 bytes |
| Raw proposal / canonical result | 10,000 / 10,000 bytes in L1 |
| HTTP response envelope | 26,192 bytes |
| Managed settings max request bytes | 256,000; tighter stage/context admission still applies |
| Source cardinality | 256 maximum; capacity alone never guarantees input admission |

The one-child/eight-claim synthetic witness measures:

| Stage | V10 system bytes | V11 system bytes | V11 data / schema bytes | V10 complete input | V11 complete input | V11 input estimate + output |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| Chunk | 2,937 | 2,937 | 1,917 / 2,423 | 7,485 | 7,485 | 7,685 + 3,000 = 10,685 |
| Intermediate | 2,993 | 4,238 | 2,056 / 2,474 | 7,959 | 9,204 | 9,404 + 3,000 = 12,404 |
| Structural | 3,002 | 4,346 | 2,056 / 2,474 | 7,968 | 9,312 | 9,512 + 3,000 = 12,512 |
| Root | 3,005 | 4,493 | 2,056 / 2,474 | 7,971 | 9,459 | 9,659 + 3,000 = 12,659 |

These are newly measured synthetic envelopes, not the actual v10 provider outputs
or tokenizer usage. Schema, data and equivalent canonical child storage do not
grow. Complete child contributions in this witness are 5,333 for structural and
6,206 for root. A separate two-chunk witness gives v11 structural data/schema
924/2,444, complete input 7,920 and context reservation 11,120, with two 1,410-byte
children. Intermediate measures 7,812/11,012 input/context, root 7,351/10,551.
Raw measurements are in `/tmp/phase17h-v11-validation/sizing.json`.

With fixed base 6,990, two full 7,000-byte children reserve 20,990 before path
cost, below 24,800. Three reserve 27,990 and are rejected; no fan-in or budget is
increased. Longer instructions reduce available headroom. Source/path JSON
escaping, Unicode and complete wrappers remain counted. Both-profile tests cover
0/1/4/128/129/256 sources, 257 rejection, exact admission/+1 boundaries and
one/two-child material. Raw and canonical output limits remain independent.

The permanent v5 witness preserves **4,783 canonical bytes**, **7,271** for the
obsolete result-plus-fixed-wrapper estimate and **6,867** for the complete actual
child. Both profiles accept that valid shape under the existing 7,000 allowance;
wrong identities, foreign references and oversize material remain rejected.
Terminal provider completion limits stop chunk, structural or root execution
without retry, repair, truncation, publication or downstream Q&A.

No financial catalog, quota policy, token allowance or ceiling changes. Extra
instruction bytes do not confer spend authority or promise actual output-token
sufficiency. No live model is used to measure quality, usage, cost or latency.

## G2 and durability assessment

E keys still enumerate only authorized sources; C keys still select full atomic
immediate-child pairs. Provider proposals cannot construct stage/origin/claim UUIDs
or arbitrary child pair components. Deterministic canonical construction and exact
request/table binding remain unchanged except for admitting the explicitly named
new version. Invalid/duplicate/missing/foreign keys and descendant substitution
still fail. Complete coverage remains mandatory without manufacturing support.

The unchanged G2 implementation independently validates canonical IDs, stage,
source spans, qualification authority, immediate-child pairs, support and coverage.
Inherited qualifications, contradictions and unresolved conflict handling survive
through the existing summaries and links. Pure structural validity still does not
establish semantic entailment or relevance.

Provider bytes remain immutable, captured after known usage settlement. The
checkpoint/receipt/raw-record manifest is atomically committed with step success
and dependent activation under the existing lease/fence authority. Replay verifies
the original accepted association, request/config/table hashes, raw/canonical
hashes and source/child/inherited material. Repeated resumes follow the original
ledger-owned association. Interrupted and orphan objects confer no acceptance or
inference authority. No schema migration, repair or relaxed validation is added.

## Offline validation and evidence

All commands use the existing project interpreter
`/home/home/.pyenv/versions/estudio_polymind/bin/python`, without installing packages
or models. A pre-collection plugin at
`/tmp/phase17h-v11-validation/offline_guard.py` denies external socket connection
and DNS before importing application code. Existing test settings isolation
suppresses implicit application dotenv loading. Tests use local HTTP fakes,
disposable authorities/ledgers/object stores, and fake embeddings. Synthetic
security/approval/accounting tests operate only on their test fixtures; no real
operator credentials, approvals or financial authorities are accessed.

Common command prefix:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=.:/tmp/phase17h-v11-validation \
/home/home/.pyenv/versions/estudio_polymind/bin/python -m pytest \
-p offline_guard -p no:cacheprovider
```

| Check, appended arguments | Actual result |
| --- | --- |
| `tests/integration/test_managed_prompt10_contract.py tests/integration/test_foundry_l1_launcher.py -q --basetemp=/tmp/phase17h-v11-validation/first --junitxml=/tmp/phase17h-v11-validation/first.xml` | 45 passed in 17.27 s; zero network attempts |
| `tests/unit/documents/test_generation_wire_v10_decoder.py tests/unit/documents/test_generation_wire_v10_sizing.py tests/integration/test_generation_wire_v10.py -q --basetemp=/tmp/phase17h-v11-validation/wire --junitxml=/tmp/phase17h-v11-validation/wire.xml` | 742 passed in 139.08 s; both profiles; zero network attempts; before five additional cases per profile |
| `tests/unit/documents/test_reducer_semantic_contract_v11.py tests/integration/test_reducer_semantic_quality_v11.py -q --basetemp=/tmp/phase17h-v11-validation/semantic3 --junitxml=/tmp/phase17h-v11-validation/semantic3.xml` | 10 passed in 5.85 s; zero network attempts |
| `tests/integration/test_generation_wire_v10.py tests/integration/test_managed_prompt10_contract.py -q -k 'version_change or original_v5 or output_limit_is or frozen_executed' --basetemp=/tmp/phase17h-v11-validation/extra --junitxml=/tmp/phase17h-v11-validation/extra.xml` | 11 passed, 132 deselected in 12.07 s; zero network attempts |
| `tests/integration/test_managed_prompt11_contract.py -q --basetemp=/tmp/phase17h-v11-validation/pin --junitxml=/tmp/phase17h-v11-validation/pin.xml` | 4 passed in 2.06 s; zero network attempts |
| Final corrected domain fixtures, `tests/integration/test_reducer_semantic_quality_v11.py -q --basetemp=/tmp/phase17h-v11-validation/semantic-final --junitxml=/tmp/phase17h-v11-validation/semantic-final.xml` | 3 passed in 7.27 s; zero network attempts |
| Self-review selection, `tests/unit/documents/test_reducer_semantic_contract_v11.py tests/integration/test_reducer_semantic_quality_v11.py tests/integration/test_managed_prompt10_contract.py tests/integration/test_generation_wire_v10.py -q -k 'authored_content or substantive_content or frozen_executed or original_v5 or version_change' --basetemp=/tmp/phase17h-v11-validation/review --junitxml=/tmp/phase17h-v11-validation/review.xml` | 11 passed, 142 deselected in 21.52 s; zero network attempts; before final per-unit fixture correction |
| Full default testpaths suite, `--basetemp=/tmp/phase17h-v11-validation/verified --junitxml=/tmp/phase17h-v11-validation/verified.xml -o junit_family=xunit1 -q` | **2,991 passed**, 0 failures/errors/skips, 1 warning in **897.80 s**; zero recorded network attempts; exit 0 |

JUnit independently confirms **2,136 unit and 855 integration cases**, with zero
failures/errors/skips. The three shared wire/decoder/sizing modules contribute
**752** final cases across both profiles. One pre-existing OpenTelemetry
`SelectableGroups` deprecation warning comes from the local real-Chroma
publication test; no test fails and no network attempt is recorded. No unresolved
implementation regression or unrelated baseline failure remains in this run.

Focused runs overlap the full suite and must not be summed as independent tests.
The semantic3 run includes the G2-valid metadata counterexample and predates the
final science wording and per-unit reference fixture corrections. The final
full suite validates the corrected files.
The first semantic run had 8 passes and 2 fixture setup failures: new synthetic
PDFs provided one line while the unchanged historical smoke harness expects a
heading and first content line. Supplying a synthetic heading corrected the
fixtures without altering production or the historical benchmark; semantic2 then
passed 10 tests in 7.38 s. No failed/exploratory run is presented as a pass.

Two incomplete full-suite attempts were deliberately interrupted (exit 130, no
final count) during self-review. The authored science summary had described effects
at other temperatures as untested, while its source only said they were not
established. The final fixture now preserves that exact epistemic distinction;
field safety alone is described as untested. This is a corrected fixture-quality
finding, not a production/G2 change or a model observation. The second review tightened the authored valve selections to each summary's
actual unit group and its corresponding immediate-child claims at root, rather
than assigning every child to both summaries. Domain fixtures also mark their
material caveats explicitly. These changes avoid treating valid-but-unrelated
reference selections as good quality witnesses. The full run below was restarted
after those corrections and test-only formatting/cleanup.

Ruff critical `E9,F63,F7,F82` passes across `documents`, `llm` and `tests`.
Default Ruff and format checks pass for the five new Python files and the two
modified wire/historical-contract integration modules. Existing
modules retain repository formatting; no broad formatting refactor is performed.
Initial new-fixture lint findings were import order, dict spelling and explicit
string concatenation formatting, corrected before full validation.

Whole-workspace compilation was actually executed:

```bash
PYTHONPYCACHEPREFIX=/tmp/phase17h-v11-validation/pycache \
/home/home/.pyenv/versions/estudio_polymind/bin/python -m compileall -q .
```

It exits 0, with bytecode outside the repository and no ownership changes.
`git diff --check` passes. Docker build/Compose and Kubernetes validation are not
applicable: no dependency, image, deployment or container configuration changes;
none are invoked under this offline task. No unrestricted mypy result is claimed.

The domain fixtures and small explicit rubric are explained in the
[quality/closure assessment](../../evaluation/phase_17h_v11_reducer_quality_and_closure_assessment.md).
They establish that valid substantive summaries can pass the protocol and lineage
contract. They cannot establish that Azure or any actual model generates them.
The full seven-dimension rubric is an independent review requirement, not an
automated entailment evaluator or measured expert-supported-claim rate.

## Implementation review and separate pre-commit review

A complete diff review traced profile registration, unchanged default v10 prose,
explicit all-stage version binding, config/source inventory, every version-specific
workflow/constructor/sizing consumer, original golden replay, G1 growth, strict G2,
receipt/fence/orphan behavior and publication/Q&A compatibility. No provider-specific
logic reaches application graph/API/UI/RAG. Resource cleanup and error paths reuse
the existing implementation; no new network/session/resource lifecycle is added.
The replay loader is test-only and verifies sources before executing a frozen
fixture. New inventory data pins actual bytes rather than regenerating old goldens.

A separate pre-commit review checks task-owned code, fixtures and documentation for
secrets, credentials, key material, environment files, local runtime paths in
production code, debug code, stale TODOs, dead code, generated artifacts, accidental
dependencies, API drift, unrelated edits and broken links. Frozen files are exact
historical source, not additional production implementations. Diagnostic logs,
JUnit, synthetic stores and bytecode stay in `/tmp`. No .env, credentials, private
key, operator database, cloud source, signed approval or historical response is
opened by the implementation or reports. Final review finds **zero secret-pattern findings, zero broken relative links,
zero changed protected files and zero staged files**. All 199 starting preservation
hashes match, both inherited files and their combined five-line diff are exactly
unchanged, all six frozen sources match their committed blobs, and the unchanged
v10 JSON still reconstructs its original fingerprint. All 25 current inventory
hashes match the v11 fixture. `git diff --check` passes after report finalization.

## Complete task-owned file inventory

Modified files:

1. `documents/digestion/managed.py`
2. `documents/digestion/sizing.py`
3. `documents/digestion/wire.py`
4. `documents/digestion/workflow.py`
5. `tests/conftest.py`
6. `tests/fixtures/digestion_contracts/README.md`
7. `tests/integration/test_final_offline_azure_compatibility.py`
8. `tests/integration/test_generation_wire_v10.py`
9. `tests/integration/test_managed_prompt10_contract.py`
10. `tests/performance/foundry_single_call.py`
11. `tests/unit/documents/test_generation_wire_v10_decoder.py`
12. `tests/unit/documents/test_generation_wire_v10_sizing.py`

Added files:

1. `tests/fixtures/digestion_contracts/managed_prompt11.json`
2. `tests/fixtures/digestion_contracts/v10_sources/documents/digestion/managed.py.txt`
3. `tests/fixtures/digestion_contracts/v10_sources/documents/digestion/sizing.py.txt`
4. `tests/fixtures/digestion_contracts/v10_sources/documents/digestion/wire.py.txt`
5. `tests/fixtures/digestion_contracts/v10_sources/documents/digestion/workflow.py.txt`
6. `tests/fixtures/digestion_contracts/v10_sources/tests/performance/foundry_preflight.py.txt`
7. `tests/fixtures/digestion_contracts/v10_sources/tests/performance/foundry_single_call.py.txt`
8. `tests/historical_managed_v10.py`
9. `tests/reducer_semantic_fixtures.py`
10. `tests/integration/test_managed_prompt11_contract.py`
11. `tests/integration/test_reducer_semantic_quality_v11.py`
12. `tests/unit/documents/test_reducer_semantic_contract_v11.py`
13. `docs/codex/prompts/phase_17h_v11_reducer_semantic_quality.md`
14. `docs/codex/reports/phase_17h_v11_reducer_semantic_quality_implementation.md`
15. `docs/evaluation/phase_17h_v11_reducer_quality_and_closure_assessment.md`

The inherited changes to `tests/performance/foundry_preflight.py` and
`tests/integration/test_foundry_l1_launcher.py` are **not task-owned edits**;
their complete bytes remain unchanged. All inherited untracked documents remain.
Documentation adds explicit opt-in/version/replay guidance, the condensed phase
prompt, this engineering report and the separate reusable rubric/closure assessment.
No original historical report is updated.

## Remaining concerns and disposition

No evidence yet demonstrates that real v11 reducers improve semantic content,
select relevant authorized support, avoid unsupported inference, preserve every
material caveat, resist untrusted instructions or finish within the existing
completion budget. Full model/human/representative-document and broader readiness
gates remain separate. The bounded synthetic examples are deliberately modest;
metadata-valid output can remain semantically poor. Exact live evidence remains
historical v10 evidence, with original judgments and limits preserved.

Final `git status` remains on `master` at
`ec22fa3d116696b80a1bb12ad17e2eb37db38cb3`: **14 modified tracked files,
48 untracked files, zero staged files**. This consists of 12 task-modified files
and 15 task additions, plus the two inherited modifications and 33 inherited
untracked documents. Every inherited file is preserved. `git diff --stat` reports
only tracked changes, including the inherited five added lines; it excludes all
15 task additions and the inherited untracked documentation:

```text
documents/digestion/managed.py                     |  36 +++++-
 documents/digestion/sizing.py                      |   2 +-
 documents/digestion/wire.py                        |   2 +-
 documents/digestion/workflow.py                    |   6 +-
 tests/conftest.py                                  |  16 +++
 tests/fixtures/digestion_contracts/README.md       |  52 ++++++++
 .../test_final_offline_azure_compatibility.py      |   2 +-
 tests/integration/test_foundry_l1_launcher.py      |   4 +
 tests/integration/test_generation_wire_v10.py      | 138 +++++++++++++++++++++
 .../integration/test_managed_prompt10_contract.py  |  53 ++++++--
 tests/performance/foundry_preflight.py             |   1 +
 tests/performance/foundry_single_call.py           |   2 +-
 .../documents/test_generation_wire_v10_decoder.py  |   4 +-
 .../documents/test_generation_wire_v10_sizing.py   |   2 +
 14 files changed, 304 insertions(+), 16 deletions(-)
```

**Step 1: PASS. Step 2: PASS. Step 3: PASS. Step 4: assessment completed;
real-model quality/expert acceptance/representative reliability and formal closure
remain pending. Overall: OFFLINE IMPLEMENTATION PASS.**

Historical v10 controlled live evaluation remains VERIFIED SUCCESS for its
recorded bounded workflow, with original semantic-review limitations intact.
V11 engineering and offline integration/regressions pass. V11 Azure/model
semantic improvement is NOT YET VERIFIED. Independent expert semantic approval
is PENDING; representative document reliability is NOT ESTABLISHED. Phase 17H
is **not formally complete**.

No staging, commit, push, reset, stash, checkout, branch or remote mutation occurs.
Paid inference calls: **0**. Real cloud/authentication/key/signing/approval/
financial/deployment operations: **0**. No subsequent phase or paid evaluation
is started or authorized.
