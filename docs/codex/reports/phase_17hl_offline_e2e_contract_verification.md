# Phase 17H–L — Offline End-to-End Contract Verification

## Executive result

**PASS — offline L1 application contract integration verified.** The final selected
regression passes 1,044 tests, and the full configured `tests/` suite passes 1,380
under an explicitly isolated synthetic settings environment. Ordinary full-suite
execution with implicit operator `.env` settings still has the 64 baseline
fixture failures/errors described below; those were reproduced without this
task's launcher change and are not silently omitted or repaired.

This task verifies application contracts with deterministic synthetic inference.
It does not determine the
latest historical strict-response rejection, whose offending response is not
available in the sanitized audit. The older Attempt 3 investigation is historical
evidence about a different retained response; its diagnosis is not transferred to
the latest attempt. No historical response or private execution packet was read.

**Phase 17H remains PARTIAL** pending live-model semantic-quality and reliability
criteria. No live experiment is authorized by this report.

## Starting state and preservation

Work began on `master`, HEAD `af4a7a076c918ef13aea05d74bf239c0af909133`.
`git status --short --branch` showed 20 modified tracked files and 80 untracked
entries (some entries represent directories). The index was empty.
`git diff --check` passed. The tracked diff was 607 insertions and 71 deletions
across 20 files. These are pre-existing workspace statistics, not this task's
changes. The tree was never reset, cleaned, restored, stashed or switched.

Before editing, hashes of repository tracked and nonignored untracked files and
a copy of the existing launcher were saved under `/tmp`. The final comparison
identifies only `tests/performance/foundry_l1.py` as changed among pre-existing
paths. This task adds its test module, prompt record and report. No application
core module, previous test, historical report, audit, approved configuration,
consumption evidence or authority database was changed. Ignored private records
were not inventoried or opened; preservation of those records is an operation
scope statement, not a claim to have hashed private operator storage.

Reading covered `AGENTS.md`, the relevant Phase 17A–17H reports and evaluation
methodology, all seven specifically requested Phase 17H–L reports, and current
ingestion, planner, job, digestion, provider, publication, security and accounting
implementations and tests. Existing diagnostic and regression work was preserved.
The original selected baseline was rerun first: **1,013 passed, zero failures,
errors or skips, four warnings, 161.96 seconds**. All 36 formerly failing/error
node IDs were recovered from the retained diagnostic baseline log and matched to
passing cases in the new baseline JUnit output.

## Actual L1 topology

The existing `tests/performance/fixtures.py:pdf` generator produces real PDF bytes,
not substituted extracted text: `phase17h-pdf/1`, seed 1708, four pages, six lines
per page. Repeated generation yields identical bytes and manifest under the
installed writer version. The source SHA-256 matches stored source metadata;
native extraction is compared line-for-line with all four expected pages.
Page 3 includes the existing injection payload unchanged.

| Item | Observed contract |
| --- | --- |
| Extracted pieces / structural chunks | Four canonical page pieces / one chunk |
| Structural units | Document root and canonical-page fallback container |
| Analysis | One chunk-analysis stage covering all four evidence IDs |
| Reduction level 1 | One structural reducer, child = analysis stage |
| Reduction level 2 | One root reducer, child = structural reducer |
| Required lineage | Every child claim at each reducer, with its exact child stage and claim ID |
| Durable job steps | Plan anchor, analysis, structural reduction, root reduction, digest validation |
| Managed digestion requests | Three: profiles `chunk`, `structural`, `root` |
| Separate interactive request | One `DocumentAnalysis` request after explicit publication |
| Positive fake invocations | Four, exactly matching the verified four-interaction design |

The two single-child reductions are intentional consequences of preserving the
fallback container and document root. Their depth is structural, not a requirement
for multiple analysis chunks. No DAG stage, dependency or call was bypassed.
The positive run accepts one evidence-bearing leaf claim, its qualification and
two linked synthesis claims. COMPLETE requires all five durable steps, validated
checkpoint graph and complete coverage, not merely three successful HTTP replies.

## Integration boundaries

| Component | How exercised |
| --- | --- |
| PDF generation and canonical extraction | Actual deterministic PDF generator, native extractor, serializer and object references |
| Structural planning and DAG admission | Actual `prepare`, `build_plan`, `admit`, fixed step specifications and profile fingerprints |
| Durable execution | Actual `SQLiteJobLedger`, dispatcher, fenced Worker, managed handler and immutable object store |
| Generation instructions and provider request | Actual `ManagedSynthesisInference.render`, GenerationRequest, schema conversion and OpenAI-compatible payload rendering |
| Provider transport/parser | Actual adapter and bounded HTTP decoder; explicit in-memory HTTP fake supplies every response |
| Decode/validation/evidence | Actual strict codec, Pydantic StageResult, canonical serializer and EvidenceIndex |
| Reductions/finalization | Actual dependency requests, inherited summaries, root graph walk, coverage and digest manifests |
| Publication | Actual AuthorizedPublication → plan → prepare → activate; a separate explicit operation |
| Retrieval and citations | Actual publication validation, replica pinning, BM25/fusion, original-source citation reconstruction |
| Embeddings/vector service/reranking | Existing constant synthetic model, in-memory vector port and deterministic reranker; ranking quality simulated |
| Q&A | Actual DocumentAnalysis with authorization snapshot and GovernedExecution; fake returns a supplied source excerpt and its application citation ID |
| Governance/accounting | Actual security authority, governance ledger, run guard, provider SQLite admission and settlement; temporary synthetic policies, prices and identities |
| Authentication | Positive L1 starts beneath external authentication using the established test-only principal issuer; existing synthetic OIDC/JWT/Entra regressions exercise verification independently |
| Operator approval/live runtime | Not invoked by the new harness; existing regressions use test-only identities/keys/packets, never operator material |
| Audits/diagnostics | Existing allowlisted diagnostic runner regressions and real ledger/audit writes; the new worker tests observe DigestionError at its actual validation boundary |
| Process reporting | Real default offline command in isolated child interpreters, plus actual-result tests of success, digestion failure and Q&A failure mapping |

The observation wrappers call their original implementations and return their
unchanged results. Only synthetic response authoring, test identity issuance,
pricing, vector operations, reranking and quota-clock advancement are simulated.
There is no production response repair or authorization bypass.

## Positive execution, persistence and provenance

All three requests bind the exact requested stage, consecutive deterministic
claim UUIDs, allowed source IDs, child links, schema and trusted control limits.
The positive returned JSON validates against the exact converted provider schema
and then through the actual application validator without mutation. Each stage
is validated again from accepted persisted checkpoints during finalization and
publication. The test checks the provider-authored StageResult equals the accepted
application object, rather than counting successful transport as acceptance.

The test fake adds a source-linked `Before operation.` qualification. Its inherited
count remains one through both reducers and its exact text is preserved in the
digest. This four-page fixture contains no opposing ORION facts, so contradictions
are correctly absent; the unchanged L2 offline workflow and publication/security
tests cover opposing claims and qualification/conflict propagation separately.

The accepted digest has COMPLETE status, coverage fraction 1, all four eligible
blocks included, no failed/unsupported source units, original extraction/plan
references, exact profile fingerprint and expected root ID. All three checkpoints
and the digest/coverage manifests survive fresh ledger/store construction. Same-key
admission returns the original job; supported resume reuses accepted checkpoints,
produces the identical digest and completes without further fake calls or charges.
Repeating compatible publication returns the active generation without adding
inventory or changing the active publication.

Publication produces eight ORIGINAL retrieval records from canonical source spans.
They are not invented evidence from the synthesis prose. The fake Q&A response
uses a citation already supplied in ORIGINAL_SOURCE_EVIDENCE. The application
resolves it back to the original extraction, document version, physical page and
exact source substring. The final answer equals that source excerpt. This proves
contract and provenance handling, not semantic adequacy of an actual model answer.
The public `semantic_support=not_evaluated` distinction remains intact.

## Negative execution and classifications

| Injected fault | Durable/public result | Diagnostic or accounting boundary |
| --- | --- | --- |
| Invalid JSON / duplicate keys | FAILED / serialization_error | json_decode / duplicate_json_key |
| Forbidden field / malformed UUID | FAILED / serialization_error | pydantic_validation |
| Wrong stage / kind | FAILED / serialization_error | stage_binding |
| Wrong claim ID / originating stage | FAILED / serialization_error | claim_identity |
| Foreign source evidence | FAILED / invalid_reference | evidence_validation |
| Missing analysis source coverage | FAILED / extraction_failed | coverage_validation |
| Invalid child links, levels 1 and 2 | FAILED / invalid_reference | evidence_validation |
| Missing child links, levels 1 and 2 | FAILED / extraction_failed | coverage_validation |
| Invalid root claim/evidence | FAILED / serialization_error or invalid_reference | claim_identity or evidence_validation |
| Raw UTF-8 fits, canonical ASCII exceeds limit | FAILED / extraction_limit_exceeded | response_limit |
| Raw content overflow / completion truncation | FAILED / inference_output_limit | Original provider error; known usage settled |
| HTTP envelope overflow | FAILED / inference_output_limit | Envelope rejected before usage can be trusted; UNKNOWN obligation retained |
| Missing provider usage | FAILED / governance_denied | UNKNOWN, unfinished run reservation, no second call |
| Unexpected stage/provider exception | FAILED / worker_failed | Sanitized existing classifier; UNKNOWN obligation retained |
| Revoked background authorization | FAILED / security_denied | Zero provider calls and zero financial/run reservations |
| Unsupported Q&A citation | Digest job stays COMPLETED; Q&A BLOCKED / citation_invalid | Four known calls settled; persisted digest remains COMPLETE |

Each invalid stage has no accepted failed-step manifest, no accepted final digest,
no publication and no subsequent provider operation. A root rejection retains
the earlier accepted checkpoints and all three incurred charges. Validation errors
are observed before checkpoint publication. Existing diagnostic regressions also
cover canonical-serialization/round-trip errors, claim-contract rejection,
forged/untyped metadata and closed audit taxonomy. No new public category is added.

## Strict schema and independent limits

Digestion payloads have the exact `response_format={type: json_schema,
json_schema: {name: polymind_stage_result, strict: true, schema: ...}}` shape and
the complete `provider_schema(generation_schema())` value. Trusted CONTROL retains
the application generation schema. Existing converter regressions independently
validate the closed four-object/22-property structure, all-fields-required behavior,
nulls/enums/references, supported depth, and fail-closed unknown constructs.

The provider representation deliberately removes string UUID formats, length and
pattern constraints, titles/default annotations and translates const to enum.
Pydantic and application validation still enforce UUIDs, text bounds, deterministic
IDs, stage binding, source membership, lineage and coverage. Provider-valid JSON
is therefore not sufficient for application acceptance. No Azure server acceptance
or real model obedience is demonstrated by the fake or local JSON Schema validator.

| Limit | Verified L1 value |
| --- | --- |
| Completion request | 3,000 tokens, `max_completion_tokens` |
| Raw digestion response | 10,000 UTF-8 bytes |
| Canonical digestion result | 10,000 ASCII JSON bytes including default expansion and Unicode escaping |
| Digestion HTTP envelope | 26,192 bytes |
| Managed rendered input / context | 24,800 plus 200 overhead/safety / 28,000 tokens |
| Run input/output reservations | 25,000 / 3,000 per call; 100,000 / 12,000 across four requests |
| Q&A mode / response bound | Existing `json_object` / 12,000 bytes; separate output schema in trusted instructions |

The test-local contract explicitly bounds the existing shared rehearsal contract
to four attempts and the L1 aggregate totals; production configuration is not
edited. Existing independent-limit tests cover exact 10,000/10,001 boundaries,
omitted default expansion, Unicode/escaping, truncation and transport envelopes.
No allowance is raised or conflated with token reservation.

## Governance, security and privacy

Each positive fake call reports exactly 30 input and 40 output tokens. Existing
synthetic EUR prices are 0.1 and 0.2 per million tokens, respectively: settled cost
is **EUR 0.000011 per invocation**, **EUR 0.000044 for four calls**. Tests distinguish
this from larger estimated governance and maximum run reservations, check unique
logical identities, actual token columns, settled records and completed admission
records, and compare the actual ledger after resume to its prior rows. Validation
rejection does not refund or erase already incurred synthetic usage. Unknown
accounting remains unresolved and blocks continuation. Existing concurrent quota,
duplicate settlement/execution, release and primary-error regressions are retained.

Same-tenant strangers, foreign tenants, unselected documents, unauthorized
publication and tombstoned/revoked snapshots are denied by real authority/service
checks. A revocation inserted immediately before background execution is caught
before reserve/provider execution. Existing multi-document tests cover retrieval
filtering, malicious reranker insertion, sharing, in-flight revocation and final
answer release. No user data or operator credential was supplied to the harness.

The fixture's injection is present in the untrusted source data and absent from
trusted system/control instructions. Requests retain their authorized document,
evidence constraints, fixed budgets and lack of tools. Forged evidence/citations
and revoked authorization are rejected independently of returned prose. This
establishes tested application trust boundaries, not a general guarantee that an
unseen live model cannot follow malicious source instructions in its language.
Model-level instruction following, secret-request handling and semantic quality
remain unverified; the test runtime supplies no real secrets or executable tools.

The pre-collection plugin denies socket connection/sendto and DNS, with an audit
hook and a session-level attempt counter so swallowed attempts also fail the run.
New child processes install socket/DNS denial before importing application code.
All actual HTTP responses in the new workflow come from the explicit fake; no
provider factory, SDK, real session, Entra token, operator signing key or approval
packet is used. Existing authentication/approval regressions generate their own
synthetic keys and test packets in temporary storage; they are not new live
authorizations or operator signing operations.

The unchanged 25 diagnostic tests exercise fixed enum identifiers, omission of
untyped/forged metadata, content-free errors, 0600 outcome files, exclusive creation
and refusal to overwrite durable audit output. The new worker tests do not claim
that the general job ledger persists validation diagnostics: it retains its
existing public category; the diagnostic is observed on the real domain exception.
The rehearsal's existing response/review artifacts intentionally contain synthetic
model/evidence content under temporary storage and are not promoted into sanitized
diagnostic records or historical audits.

## Reproduced defect and narrow correction

Before correction, tests generated real FAILED/serialization_error and
COMPLETED-digest/BLOCKED-Q&A results, passed them into the safely callable offline
CLI mapping, and demonstrated that `main()` returned normally in both cases.
This independently reproduces the known shell-success defect without `--live`.

The launcher now exits 1 if digestion is not COMPLETED **or** Q&A is not COMPLETE,
after the execution and audit finalization return. Successful complete L1 work
still exits 0. Existing `stage`, `state` and `calls` output values are retained;
the additive `questions_status` field exposes COMPLETE/BLOCKED, or null when Q&A
was never reached. Thus a completed digest with failed Q&A remains accurately
reported as a completed digestion job while clearly failing the overall L1 run.
This is a CLI reporting correction, not a change to job states, public error
categories, provider execution, API behavior or financial finalization.

Actual isolated default-offline child interpreters also verify exit 0 versus 1
against durable result.json and machine output. Live authentication, real provider
transport and the actual live outer CLI branch are explicitly not executed.

## Testing and quality checks

The ordinary full run inherited the repository's operator-mode configuration and
collected 1,380 cases: **1,316 passed, 56 failed, 8 setup errors, zero skips, zero
xfails, zero network attempts, 397.27 seconds**. These additional failures are
outside the selected 1,013-case baseline. They must not be hidden by the green
selected result.

The exact 64 failing/error node IDs were then rerun with the saved pre-task
launcher executed in memory at its original module path. No checkout file was
replaced. Result: **56 failed, 8 errors, zero passed/skipped/xfails, zero network
attempts, 63.29 seconds**; the complete node-ID and failure/error-type maps are
identical. No core implementation or previous test changed during this task.

The affected groups are publication analysis (10), API (2), lifecycle (16), load
(2), planning (9), retrieval (6), security (6), workflow (1), and legacy API
reliability (2), memory integration (1), retrieval regression (1) and streaming
(8). The publication fixtures call standalone publication methods without
authorization while implicitly inheriting operator OIDC mode; legacy graph/API
fixtures similarly assume standalone execution/readiness. The authority correctly
denies these calls. This is pre-existing test-environment coupling, not evidence
that the new governed L1 workflow bypasses or breaks authorization.

A separate larger run uses a temporary plugin that suppresses **only** the
implicit repository `.env` source during settings construction. Explicit env-file
fixtures, environment variables, Settings defaults/validators, per-test overrides,
OIDC tests and GovernedExecution remain active. It does not assign a disabled
governance flag or alter production code. This controlled full run is additional
evidence, not replacement of the unchanged selected baseline or a claim that plain
pytest under the operator configuration is green. Its final result follows below.

The final 57-case new-integration/launcher selection passed in **55.76 seconds**
after the additive CLI status field. The 31 new cases perform **58 synthetic HTTP
invocations per complete module run**, including five invocations in two isolated
child processes; the primary positive L1 uses four. Legacy regression fakes are
not included in that 58-call count. No live invocation occurs in any run.

The **final source** selected regression collected and passed **1,044 tests in
394.57 seconds**, with zero failures, errors, skips, expected failures or network
attempts. It contains all 1,013 original baseline cases plus the 31 new cases.
JUnit comparison confirms **all 36 previously reconciled cases**, **all 25
diagnostic-hardening cases**, 177 security-prefixed unit cases, 19 governance-
prefixed cases and 28 evaluation-prefixed cases pass. The 31 new cases contribute
58 counted fake HTTP invocations in that run. The earlier broad 1,044-case run
also passed in 307.62 seconds; the final repeat followed the CLI metadata change
and strengthened idempotency observer. Runs overlapped other local test work, so
these durations are validation evidence, not performance measurements.

Development runs exposed test-authoring mistakes in an observation argument
slice, an assumed validation-read count, the stage-exception category and retry
profile matching. These were corrected against inspected production contracts;
no acceptance predicate or existing test assertion was relaxed. The independent
exit-status reproduction failed before the launcher correction and passed after it.

Exact final selected command (the initial baseline used the same selection without
the new module, the existing `polymind_offline_guard` plugin, `--disable-warnings`,
and `/tmp/phase17hl-e2e-baseline.xml`):

```sh
PYTHONPATH=/tmp:. python -m pytest -p polymind_e2e_offline_guard tests/integration/test_validation_diagnostics.py tests/unit/documents tests/unit/test_governance*.py tests/unit/test_security*.py tests/unit/test_evaluation*.py tests/unit/test_foundry*.py tests/unit/test_single_call_diagnostics.py tests/unit/test_output_limit_diagnostics.py tests/unit/test_structured_provider.py tests/integration/test_*digestion.py tests/integration/test_single_call*.py tests/integration/test_foundry*.py tests/integration/test_attempt3_serialization.py tests/integration/test_output_limit_hardening.py tests/integration/test_phase17hl_offline_e2e.py -q -o junit_family=legacy --junitxml=/tmp/phase17hl-e2e-broad-final.xml

PYTHONPATH=/tmp:. python -m pytest -p polymind_e2e_offline_guard tests/integration/test_phase17hl_offline_e2e.py tests/integration/test_foundry_l1_launcher.py -q -o junit_family=legacy --junitxml=/tmp/phase17hl-e2e-cli-final.xml

PYTHONPATH=/tmp:. python -m pytest -p polymind_e2e_offline_guard -q -o junit_family=legacy --junitxml=/tmp/phase17hl-e2e-full.xml

PYTHONPATH=/tmp:. python -m pytest -p polymind_e2e_offline_guard -p polymind_e2e_synthetic_settings -q -o junit_family=legacy --junitxml=/tmp/phase17hl-e2e-full-synthetic-settings.xml

PYTHONPYCACHEPREFIX=/tmp/phase17hl-e2e-pycache python -m compileall -q .
ruff check tests/integration/test_phase17hl_offline_e2e.py
ruff format --check tests/integration/test_phase17hl_offline_e2e.py
git diff --check
```

The 64-case comparison command is generated without shell node-ID interpolation:
`python -m pytest -p polymind_e2e_offline_guard -p polymind_e2e_starting_launcher
<the exact 64 node IDs from full-suite JUnit> -q -o junit_family=legacy
--junitxml=/tmp/phase17hl-e2e-full-baseline-failures.xml`. The temporary comparison
plugin imports the launcher and executes the saved original source in its module
dictionary, retaining the original `__file__` and source-fingerprint resolution.

Full-repository compilation passed with external bytecode output. The new test's
Ruff lint and format checks pass. Launcher lint has exactly the same five existing
findings before/after (I001 × 3, F401 × 1, BLE001 × 1); both saved and current
launcher fail the same whole-file formatting check. No unrelated formatting is
applied. `git diff --check` passes. No cases are explicitly excluded or deselected
within either selected command; the selected suite deliberately omits tests outside
its listed paths. The full command excludes no configured `tests/` case and does
not collect `experiments/`, which pytest.ini excludes from its testpaths.

The final controlled-settings full run collected and passed **1,380 tests in
483.38 seconds**, with **zero failures, setup errors, skips, expected failures,
warnings or network attempts**. This includes all 54 publication unit cases,
all six publication-security cases, both load/revocation cases, real local Chroma
adapter coverage and the 31 new integration cases. All 64 cases affected by
implicit operator configuration pass under the synthetic default settings.
No test or assertion was skipped, xfailed or changed to obtain that result.

| Completed run | Collected | Passed | Failed | Setup errors | Skips / xfails | Duration |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| Starting selected baseline | 1,013 | 1,013 | 0 | 0 | 0 / 0 | 161.96 s |
| Qualified 31-case new module, before final reporting addition | 31 | 31 | 0 | 0 | 0 / 0 | 16.11 s |
| Second-review stronger assertions | 31 | 31 | 0 | 0 | 0 / 0 | 44.40 s |
| Final new module + existing launcher tests | 57 | 57 | 0 | 0 | 0 / 0 | 55.76 s |
| Final selected baseline + new tests | 1,044 | 1,044 | 0 | 0 | 0 / 0 | 394.57 s |
| Full suite, implicit operator configuration | 1,380 | 1,316 | 56 | 8 | 0 / 0 | 397.27 s |
| Exact failed/error cases with starting launcher | 64 | 0 | 56 | 8 | 0 / 0 | 63.29 s |
| Full suite, explicit synthetic settings isolation | 1,380 | 1,380 | 0 | 0 | 0 / 0 | 483.38 s |

These rows overlap and must not be added into a unique-test count. The original
baseline reported four warnings with its historical command options; final legacy
JUnit-mode commands reported none. Network attempts were zero in every completed
guarded regression. Actual live provider calls were zero throughout.

All logs, JUnit files, baseline source/hashes and temporary network plugins are
outside the repository under `/tmp/phase17hl-e2e-*` and
`/tmp/polymind_e2e_offline_guard.py`. No Docker/Helm build or deployment operation
was launched by this task. The existing full-suite chart tests may invoke local
Helm rendering; no cluster or deployment mutation is involved.

### Recreating the temporary isolation plugins

Save the following as `/tmp/polymind_e2e_offline_guard.py` before reproducing the
commands. It is imported before collection and records only an attempt count:

```python
import socket
import sys

attempts = []

def deny(*args, **kwargs):
    attempts.append('socket_or_dns')
    raise AssertionError('Network forbidden for offline contract verification')

for name in ('connect', 'connect_ex', 'sendto'):
    setattr(socket.socket, name, deny)
for name in ('create_connection', 'getaddrinfo', 'gethostbyname',
             'gethostbyname_ex', 'gethostbyaddr'):
    setattr(socket, name, deny)

def audit(event, args):
    if event in ('socket.connect', 'socket.sendto', 'socket.getaddrinfo',
                 'socket.gethostbyname', 'socket.gethostbyaddr'):
        deny()

sys.addaudithook(audit)

def pytest_sessionfinish(session, exitstatus):
    if attempts:
        session.exitstatus = 1

def pytest_terminal_summary(terminalreporter):
    terminalreporter.write_line('Offline network attempts: ' + str(len(attempts)))
```

The additional full-suite plugin, `/tmp/polymind_e2e_synthetic_settings.py`, is:

```python
from pathlib import Path
from pydantic_settings.sources.providers.dotenv import DotEnvSettingsSource

original = DotEnvSettingsSource._read_env_file
operator_env = Path.cwd() / '.env'

def read_env_file(self, file_path):
    if Path(file_path).absolute() == operator_env:
        return {}
    return original(self, file_path)

DotEnvSettingsSource._read_env_file = read_env_file
```

It is test-only infrastructure using the installed settings dependency, not a
production configuration change. Unisolated baseline runs used ordinary Settings
loading; no credential value was inspected, printed or supplied to an execution.
The isolated larger run avoids reading the implicit repository `.env` entirely.

## Separate self-review and pre-commit review

A second read of the complete new test module and launcher-only diff checked
request/schema fidelity, no response repair, successful real validations, full
source/child coverage, persisted manifests, citations and accounting assertions.
Review found that the observer originally replaced its saved job during duplicate
admission, making an identity comparison self-referential. The observer now retains
the original job, and the final resume assertion also checks terminal COMPLETED.
Reservation assertions now check the distinct maximum run values explicitly.
The final targeted rerun verifies these stronger tests.

The source change remains limited to launcher reporting. Provider-neutral
architecture, canonical evidence, synthesis lineage, job/object-store separation,
publication immutability and unknown-usage controls are unchanged. The fake
authors its controlled results before the application sees them; no acceptance
decision is mocked. Constant vectors and synthetic answers are explicitly scoped.

The separate pre-commit inventory checks baseline hashes, empty index, no deleted
files and only this task's additions plus launcher modification. Review covers
secrets/private keys/tokens, .env/runtime files, hard-coded deployment paths,
debug/dead code, dependencies, unrelated changes and documentation links. Synthetic
privacy markers, `.invalid` endpoints and inline child-test code are intentional.
There are no installed dependencies, generated repository artifacts or core
production implementation changes. No commit or push occurs.

Final Git inventory is **20 pre-existing modified tracked files and 83 untracked
entries**, with an empty index and no deletions. The tracked diff remains exactly
**20 files, 607 insertions, 71 deletions**. It excludes this task's additions and
the already-untracked launcher. The phase-specific inventory is:

- Created `tests/integration/test_phase17hl_offline_e2e.py`.
- Created `docs/codex/prompts/phase_17hl_offline_e2e_contract_verification.md`.
- Created this report.
- Modified only the existing `tests/performance/foundry_l1.py` CLI reporting path.

`git status --short --branch`, `git diff --stat`, `git diff --cached --name-only`
and `git diff --check` were run. The branch remains `master` at the starting HEAD.
New-file and launcher scans found no serialized token, private-key block,
machine-home path, debug statement or introduced TODO. No file was staged.

### Source binding observations

The existing transitive executor hashing algorithm gives:

```text
Before: a93d62df2af1086fb6c2404f7171a9bbb6bd5320a267060728ec945c3357dc9d
After:  9cd6711b61f2896090d351468e42dcc9a7c00f77e8f6cfc41c6f273172897b5a
```

It includes the launcher source, so the reporting correction changes that
fingerprint even though the inference path is unchanged. The narrower generation
fingerprint is unchanged from the saved starting files:
`82ecad5d4cb2e8fd2e0981c7d3710bbb3a582e56ef9eebca07ab0f314a4d05f9`.
No approved configuration or packet was updated, regenerated, signed or consumed.
These are read-only source observations, not refreshed authorization.

## Limitations and next recommendation

Offline integration verified does not mean Azure Foundry runtime verified.
Synthetic semantic quality does not establish actual model semantic quality.
Strict schema representation does not guarantee provider acceptance or returned
application semantics. A successful fake digest does not demonstrate a successful
live digest. Selected regression PASS is not full production certification.

This is a local SQLite/object-store reference composition. Distributed execution,
real embedding/reranker quality, live provider reliability, real Entra issuance,
network transport and billing semantics remain outside the proof. Test review
packets still require independent human semantic judgment. No missing latest
historical failure content was reconstructed.

A separately authorized limited live contract experiment can be considered only
after review of the final offline result and current source/configuration bindings.
It must retain strict no-repair validation, fresh reviewed authorization, one-call
stop conditions, known pricing/usage, private immutable sanitized diagnostics,
no automatic paid retry and independent semantic review. Existing consumed/stale
approvals must not be reused. No new experiment, approval or packet was prepared
or executed here. Phase 17H remains PARTIAL regardless of this task's offline result.

The application contract path is ready for that separate technical review; this
report does not authorize the experiment. Ordinary full-suite operator-settings
coupling remains a known test-workflow limitation and should be addressed in a
separate fixture-configuration reconciliation, with all governed/security tests
preserved. No unresolved in-scope production defect remains after the CLI fix.

Safety totals: **Azure inference 0; other live inference 0; cloud modifications 0;
operator RSA signing 0; new live authorizations 0; operator approval consumption 0;
commits 0; pushes 0; branch changes 0; dependency installations 0.**
