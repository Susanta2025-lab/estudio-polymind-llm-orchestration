# Phase 17H–L — F1 HTTP Cleanup Failure Preservation

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

For the historical examples below, `PROJECT_ROOT` means the absolute path to a local checkout; `PYTHON` means the absolute path to the project Python 3.10.13 interpreter. Define them with shell assignments such as `PROJECT_ROOT="<absolute checkout path>"` and `PYTHON="<absolute project interpreter path>"`, substituting local paths; these schematic values are not executable examples. `PYTHON_311` and `PYTHON_312`, where used, mean absolute paths to the independently installed Python 3.11.8 and 3.12.9 interpreters. Define them analogously with `PYTHON_311="<absolute Python 3.11.8 path>"` and `PYTHON_312="<absolute Python 3.12.9 path>"`. Their original execution results are retained; temporary drivers and guards are historical evidence, not installed project commands.

Date: 24 October 2026. Branch: `master`.
HEAD: `af4a7a076c918ef13aea05d74bf239c0af909133`.
[Task prompt](../prompts/phase_17hl_f1_http_cleanup_failure_preservation.md).

## A. Executive summary

The narrow F1 correction is implemented in `llm/bounded_http.py`, with the directly
analogous owned-session correction in `llm/openai_compatible.py`. Expected I/O
cleanup failures preserve an existing primary exception. Cleanup-only I/O failure
raises the existing sanitized `InferenceConnectionError`, publicly classified as
`inference_unavailable`. No request, parsing policy, retry, generation contract or
financial rule changed.

**F1 FIX PASS.** The complete offline regression passed **1,755 tests** with
**0 failures, 0 errors, 0 skips, 42 existing warnings and 0 observed network
attempts** (365.09 s, exit 0). All **1,678** earlier case identities remain present
and passed, with exactly **77** additions in the two new test modules.
The focused selection passed **581 tests**, including **77 new cases** (56 unit,
21 integration), with zero failures/errors/skips and zero observed network attempts.
The separate initial pre-fix run demonstrated **25 failures and 22 passes**; the
same initial 47 cases passed after the correction. These regressions detect the
original defect rather than merely observing that some exception occurred.

F1 removes the confirmed engineering blocker within this transport-cleanup scope.
It does not establish live-model acceptance, current deployment availability,
commercial terms, remaining funds, fresh operator authorization or execution
eligibility. **Attempt 5 is not authorized. Phase 17H remains PARTIAL.**

## B. Root cause and reproduction

The original `request_json()` called `response.close()` unguarded in `finally`.
Python runs `finally` while an earlier exception is unwinding. A new cleanup
exception replaces the active exception as the one propagated to the caller.
Thus the adapter and governance received `OSError` instead of the original
configuration/output-limit error. The outer governance cleanup correctly preserved
the exception it received, but could not recover the category already lost here.

Real installed `requests.Response` objects, backed by an in-memory `BytesIO`
subclass, reproduce the behavior without a socket. The pre-edit tests failed for
redirects, envelope overflow, socket/wrapped read timeouts, malformed/duplicate/
invalid-Unicode JSON, rejected configuration, authentication and overload status,
as well as cleanup-only failures, primary identity preservation and owned-session
cleanup. The failing tests expected exact classes/categories; they received raw
cleanup errors. No public classifier was modified.

The four historical comparisons now produce:

| Response | Cleanup | Public classification | Calls | Finance |
|---|---|---|---:|---|
| HTTP 302 | Normal | `inference_configuration` | 1 | UNKNOWN |
| HTTP 302 | OSError | `inference_configuration` | 1 | UNKNOWN |
| HTTP 200, 26,193 bytes | Normal | `inference_output_limit` | 1 | UNKNOWN |
| HTTP 200, 26,193 bytes | OSError | `inference_output_limit` | 1 | UNKNOWN |

All four are terminal FAILED with `accounting_failed=true`. The 26,192-byte
ceiling is unchanged. The two oversized cases retain the original output-limit
record, including unknown cause/content measurements and configured application
caps. No observation establishes a billable second call or a historical Azure cause.

### Real Response cleanup reachability

For an unread/partially read response, `Response.close()` calls `raw.close()`.
Redirect and oversized-envelope cases exercise that exact path. When iteration
finishes, requests marks `_content_consumed=true` and skips `raw.close()`, but
still invokes `raw.release_conn()` when present. The malformed-JSON and successful
bounded-response cleanup tests therefore inject the failure at `release_conn()`.
This exercises the real Response close method rather than manufacturing an
unreachable raw-close call after complete consumption. Raw streams close at most
once in the exercised incomplete-body paths; the production correction adds no
second cleanup operation.

### Session ownership and timing

The adapter creates `requests.Session()` only when `http_client` is omitted and
records `_owns_http_client`. Its explicit `close()` previously called the owned
session's close unguarded. It can therefore replace a provider failure when the
owner invokes close in `finally`, or expose a raw cleanup-only I/O failure.
The correction normalizes/preserves errors at this explicit boundary; it does not
move session cleanup into `execute()` or change provider lifetime. API shutdown
calls this explicit close. Externally supplied clients remain untouched.

The single-call launcher supplies an **externally owned** no-retry session and
closes it in its own `finally`, after `execute_stage()` has persisted its outcome.
That caller-owned lifecycle and its direct close are unchanged; the adapter must
not take ownership or double-close it. This task does not claim to harden arbitrary
external callers' cleanup, readiness/interactive response paths or unrelated
resources. In the new owned-session integration tests, a late close failure raises
a sanitized terminal exception while the already persisted provider-stage audit
and SETTLED financial observations remain unchanged. A provider-stage success
record is not retroactively rewritten as a session-shutdown outcome.

## C. Implementation and exception taxonomy

Only these existing production files were edited relative to the starting tree:

- [bounded_http.py](../../../llm/bounded_http.py): add a local `completed` flag,
  set only after the existing unique-key JSON decode succeeds, and guard the
  existing single response-close call.
- [openai_compatible.py](../../../llm/openai_compatible.py): import standard-library
  `sys`, inspect the active exception before owned-session cleanup, and guard
  the existing single close call.

The response flag distinguishes successful local processing from all earlier
failure paths, including `post()`, status evaluation, body iteration, deadline,
size checking and JSON decoding. It also avoids mistaking an unrelated exception
being handled by the caller for a failure of this successful request. No response
means no close. Successful JSON is returned unchanged after successful cleanup.

Both boundaries intercept exactly **`OSError` and `requests.RequestException`**.
These describe expected transport/resource I/O failures; requests errors are
named explicitly even though the installed base class also inherits OSError.
A handled cleanup error is discarded if a primary failure is active. The primary
object is neither reconstructed nor reclassified, so its exact class, category,
usage, diagnostics and metadata survive. Session close detects an active error
through `sys.exc_info()` in the owning caller's exception/finally context.

On cleanup-only I/O failure, both raise:

```python
InferenceConnectionError('Inference provider cleanup failed.')
```

using `from None`. Its existing internal category is `provider_unreachable`,
publicly `inference_unavailable`. This reflects failure to complete the HTTP
resource lifecycle and introduces no category. No cleanup message is copied,
logged or attached as application metadata. Python retains implicit context
internally, but `from None` suppresses its display; the audited boundary serializes
only closed classifications and sanitized metadata, never exception objects,
`__context__`, tracebacks or exception prose. Privacy sentinels remain absent.

Unexpected cleanup programming errors such as AssertionError/RuntimeError and
cleanup-originated KeyboardInterrupt/SystemExit are deliberately **not** intercepted.
They propagate rather than being silently hidden or converted into retryable
transport errors. An already active cancellation/programming exception survives
an expected I/O cleanup error unchanged. Tests cover both directions. The F1
preservation policy is for expected transport cleanup exceptions, not suppression
of arbitrary defects or BaseException control flow.

This is a small correction: no new production abstraction, package, parameter,
background task, retry loop, extra request or lifecycle operation. Existing
bounded reading, redirects, timeout values, status handling, rejection diagnostics,
authentication and duplicate-key parsing are unchanged. True absolute wall-clock
deadline redesign remains outside scope.

## D. Verification and accounting evidence

### New tests

[Unit regressions](../../../tests/unit/test_http_cleanup.py) contain **56 cases**:
11 failure scenarios crossed with normal/failing response cleanup; valid/cleanup-only
cases for OSError/requests connection/timeout failures; post failure before a response;
exact primary object and known usage preservation; unexpected cleanup/control-flow
propagation; all four owned-session success/failure combinations; external-session
ownership; real adapter propagation; an unrelated handled caller exception;
post-acquisition total deadline; exact envelope ceiling; owned-session timeout and
cleanup exception policy. They use real responses and a real Session subclass with
synthetic post/close behavior. All HTTP operations remain in-memory.

[Governed regressions](../../../tests/integration/test_http_cleanup_governance.py)
contain **21 cases**. They compose the actual adapter, `GovernedExecution`,
`RunGuard`, SQLite admission, finance ledger and `execute_stage()` with temporary
synthetic authorities. They never invoke the live launcher or create/sign/consume
an approval. Eighteen cases cross response cleanup success/failure with redirects,
envelope overflow, timeout, malformed JSON, valid output, truncation, invalid usage,
missing usage and downstream application rejection. Three cases verify that later
owned-session failure cannot erase legitimately settled usage or stored metadata.

Every governed case makes exactly one fake HTTP attempt and one RunGuard record.
A subsequent guard acquisition with another logical identity is denied. Forbidden
sentinels on the full launcher, retrieval, publication and Q&A entrypoints remain
unreached. The single-analysis path contains no embedding or reduction request.
No retry or fallback was added to either production file.

Known usage remains 30 input / 40 completion / 70 total in the synthetic fixture,
settled before application validation. Truncation and application rejection retain
known charge and metadata. Later owned-session close failure leaves those SETTLED
rows and existing audit bytes intact. Missing/inconsistent/unparsed usage is never
zero: rows retain UNKNOWN with null actual counts/cost and RunGuard blocks reuse.

Response cleanup occurs **before** adapter usage processing. Even a syntactically
valid envelope with a failing release is therefore rejected with unknown usage;
bytes present in an unaccepted envelope are not fabricated into established usage.
`accounting_failed=true` records failed accounting cleanup when a provider error
is already primary. Existing missing-usage-after-provider-success behavior instead
reports primary `governance_denied` with `accounting_failed=false`; this is not a
claim that accounting succeeded or the obligation is zero. The UNKNOWN row and
terminal guard remain authoritative. One initial new assertion incorrectly equated
UNKNOWN universally with that marker; correcting this test expectation preserved
the existing implementation and financial contract.

### Reproducible offline environment

Python **3.10.13**, existing `estudio_polymind` environment, executable
`$PYTHON`. Installed versions:
pytest 8.4.2, requests 2.34.2, Pydantic 2.13.4, pydantic-settings 2.14.1,
jsonschema 4.26.0; standalone Ruff 0.16.1. Nothing installed/upgraded.

Before use, `/tmp/polymind_e2e_offline_guard.py` was inspected. It patches socket
connect/connect_ex/sendto and connection/DNS entrypoints before collection, installs
a CPython audit hook, counts attempts and fails even when a denied attempt is
swallowed. Root conftest separately isolates implicit dotenv before application
imports. The verification driver removes application setting names and credential/
provider/OIDC/governance environment prefixes without printing values, then runs
from `/tmp/polymind-f1/work` with a public tests symlink, avoiding an operator dotenv
in child processes too. It invokes no cloud utility or live execution command.
This is Python socket/DNS denial, not a claim of an OS firewall or aggregation of
all native/subprocess operations; existing subprocess tests install their own guards.

The reviewed driver was run as:

```sh
python /tmp/polymind-f1/verify.py full
```

Its exact full-suite subprocess command, with no deselection, is:

```sh
"$PYTHON" -m pytest -q \
 -c "$PROJECT_ROOT/pytest.ini" \
 --basetemp=/tmp/polymind-f1/full-temp \
 --junitxml=/tmp/polymind-f1/full.xml \
 "$PROJECT_ROOT/tests"
```

Environment overrides: `PYTHONPATH=/tmp:<repository>`,
`PYTEST_PLUGINS=polymind_e2e_offline_guard`, `PYTHONDONTWRITEBYTECODE=1`,
`PYTEST_ADDOPTS=-o cache_dir=/tmp/polymind-f1/pytest-cache`, plus the described
removal of application/credential environment input. CWD is the external work
directory above. Logs, JUnit, commands, public snapshots and compilation cache
are under `/tmp/polymind-f1/`, outside Git.

The final focused command was:

```sh
python /tmp/polymind-f1/verify.py focused-final \
 tests/unit/test_http_cleanup.py tests/integration/test_http_cleanup_governance.py \
 tests/unit/test_structured_provider.py tests/unit/test_output_limit_diagnostics.py \
 tests/unit/test_single_call_diagnostics.py tests/integration/test_live_failure_observability.py \
 tests/integration/test_single_call_harness.py tests/integration/test_single_call_preflight.py \
 tests/integration/test_output_limit_hardening.py tests/unit/test_evaluation_governance.py \
 tests/unit/test_governance.py tests/integration/test_final_offline_azure_compatibility.py \
 tests/unit/test_source_contracts.py
```

| Verification | Result |
|---|---|
| Original 47 new cases before production edit | 25 failed, 22 passed; F1 reproduced; zero network attempts |
| Same 47 cases immediately after edit | 47 passed; zero network attempts |
| Initial 21 integration cases | 20 passed, 1 test-expectation failure described above |
| Final focused selection | 581 passed, 0 failures/errors/skips, 0 warnings, 46.47 s, exit 0, zero network attempts |
| Full regression | 1,755 passed, 0 failures/errors/skips, 42 existing warnings, 365.09 s, exit 0, zero network attempts |
| Baseline node inventory | All 1,678 earlier case identities retained and passed; exactly 77 additions, no removed/weakened/skipped cases |
| New test Ruff lint/format | PASS; two files formatted, no findings |
| All four changed Python files, Ruff lint | 8 pre-existing findings, exit 1; zero new findings (9 before, one unused import now legitimately used) |
| Existing production-file format checks | Same two files require formatting before and after; unrelated formatting preserved |
| External-cache repository compileall | PASS, exit 0 |
| Tracked and four new-file whitespace checks | PASS, exit 0 |

The pre-existing lint findings are I001=1, SIM114=1, UP035=1, UP045=5 after the
change. The pre-edit F401 on the adapter's unused InferenceConnectionError import
is eliminated because the correction uses that existing exception. No unrelated
lint finding was changed. The existing production files were not broadly formatted.

Quality commands:

```sh
ruff check llm/bounded_http.py llm/openai_compatible.py \
 tests/unit/test_http_cleanup.py tests/integration/test_http_cleanup_governance.py
ruff format --check llm/bounded_http.py llm/openai_compatible.py \
 tests/unit/test_http_cleanup.py tests/integration/test_http_cleanup_governance.py
PYTHONPYCACHEPREFIX=/tmp/polymind-f1/pycache python -m compileall -q .
git diff --check
git status --short --branch
git diff --stat
git diff --cached --name-only
```

Each new file also receives `git diff --no-index --check /dev/null <path>` because
ordinary tracked diff excludes untracked files. Docker/Compose/build/Kubernetes
checks are inapplicable to this transport-only correction with no packaging,
configuration or deployment change; none was performed.

## E. Contracts and authoritative fingerprints

The authoritative bindings were recomputed **before** the correction and matched
all four supplied historical values. They were recomputed again after the final
production edit under settings isolation and network denial; attempts were zero.

| Binding | Before | After |
|---|---|---|
| Executor | `de11d7cbeb269591caa607494d29a76b894bd48af15d17ab2095ffb51b96e598` | `82fc01aa0447d4be758124cec0120a06db49f139f69ee6425b51b8696a6ad26f` |
| Generation source | `4c37473513e2f1455cfa44a84c687b661a484e2fea0a390dedf9396269610d05` | `7d387a8595cf63e2ac944a25c4987a1b37392aa4adba8889914acf51ff9f0f59` |
| Provider schema | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` |
| Inference configuration | `7eaa6b52ad387f9f0c82e318e9c74fa378ffda0baec85d0f7157cc4ab0553519` | `7eaa6b52ad387f9f0c82e318e9c74fa378ffda0baec85d0f7157cc4ab0553519` |

Computations use `foundry_single_call.executor_digest()`,
`foundry_l1.generation_contract_digest()`,
`fingerprint(provider_schema(generation_schema()))`, and
`ManagedSynthesisInference.config` with the actual explicit strict generation
settings and intended deployment binding. No replacement value is hardcoded in
production, an approval or a test oracle. The first two functions hash whole
production source files, including both corrected files, so their changes are
required even with unchanged semantic payloads. New unit/integration tests and
these documents are outside those binding path sets.

The nine unchanged frozen component oracles cover the complete synthetic
StageRequest, GenerationRequest and actual provider payload for chunk, structural
and root. The source-contract tests retain the exact renderer checksum, prompt
instructions, model/capability bindings, strict schema, domain models and validation
predicates. All four-profile witnesses also cover intermediate rendering; the
three-stage workflow has no separate frozen intermediate payload oracle, and none
was invented or refreshed. Every protected source file is byte-identical to its
starting snapshot, including managed.py, structured.py, azure_schema.py, codec.py,
models.py, validation.py and diagnostics.py.

The active contract stays **managed-prompt/3**, **managed-generation/2**,
**azure-strict/1**, **stage-result/1**. The strict schema and local validators,
3,000 completion tokens, low reasoning, configured deployment/model aliases,
10,000 raw/canonical bytes and 26,192 envelope bytes remain unchanged. Prompt 4
stays inactive and the application-owned-identifier proposal unimplemented.

Old executor/generation bindings must not be used for corrected source. Current
private configurations/approvals were neither inspected nor refreshed. Fresh exact
bindings require independent evaluation after source review; matching semantic
payloads do not preserve old source authorization. No approval was generated,
re-signed, consumed or declared valid by this task.

## F. Separate implementation review and pre-commit review

After initial tests, a separate review inspected both task-only production diffs
against saved starting bytes, the complete relevant Git diff (which includes
pre-existing work), both new test modules and documentation. It traced resource
ownership, normalization, deadlines, bounded reading, result/metadata timing,
settlement, audit serialization and guard containment. The following answers are
limited to this authorized bounded/owned-session I/O-cleanup scope.

| Review question | Evidence and answer |
|---|---|
| 1. Response cleanup masks normalized primary? | No for intercepted I/O errors; exact classes/categories preserved across 11 scenarios. Arbitrary programming/control-flow cleanup defects deliberately propagate. |
| 2. Owned-session cleanup masks primary? | No for I/O errors; exact output-limit object/usage/metadata and timeout survive owner-finally close. |
| 3. Cleanup-only returns success? | No accepted transport result; normalized exception replaces pending return. Explicit session close raises. A previously written provider-stage audit is not rewritten by later shutdown. |
| 4. Cleanup triggers retry? | No retry code added; primary categories unchanged; terminal guard denies continuation. |
| 5. Second HTTP request? | One post in each governed execution; attempted second guard acquisition denied. |
| 6. Output-limit becomes worker_failed? | No for the reproduced I/O-close defect; both historical oversized cases retain inference_output_limit. |
| 7. Status categories preserved? | Configuration, authentication, rate limit and gateway timeout cases retain exact taxonomy; fixed rejection and retry hint retained. |
| 8. Byte limits changed? | No; exact 26,192 bytes succeeds for valid padded JSON; 26,193 is rejected. |
| 9. Incomplete output rejected? | Truncation, malformed/duplicate/invalid-Unicode JSON and oversized bodies fail without repair. |
| 10. Known usage preserved? | Primary object usage/metadata preserved; settled 30/40 charges survive late owned-session close. |
| 11. Unknown usage fail-closed? | Null actual counts/cost, durable UNKNOWN and terminal guard; never zero. |
| 12. Audits content-free? | Sentinel, content/text keys and document marker absent; only existing closed diagnostics/numeric metadata/opaque governance identities retained. |
| 13. Provider payload changed? | No; all nine frozen component comparisons pass. |
| 14. Generation instructions changed? | No; managed source byte checksum and prompt remain frozen. |
| 15. StageResult validators changed? | No; byte-identical sources plus independent source contracts. |
| 16. Governance/authorization changed? | No; both source sets byte-identical and existing regression tests retained. |
| 17. Tests detect original defect? | Initial 47 cases produce 25 failures on pre-edit code, then all pass. |
| 18. Source-contract protections preserved? | All 47 existing portability/mutation cases pass; fixtures and oracles untouched. |
| 19. Fingerprints accurate? | Four authoritative functions recomputed before/after; only source hashes change. |
| 20. Old approvals potentially stale? | Required source bindings change; no old approval reused/refreshed or current authorization inferred. |

The separate pre-commit review checked task files for credentials/private keys,
real dotenv, document/response content, hardcoded runtime paths, debug statements,
new TODOs/dead code, dependencies, generated artifacts, unrelated edits, broken
local documentation links and unintended public API changes. New test strings and
UUIDs are synthetic. Temporary runtime paths appear only as validation evidence
in documentation, not application configuration. No secret or new dependency,
policy/schema migration, logging or unrelated production change was introduced.
No tracked/untracked prior file was discarded. No staging or commit occurred.

## G. Remaining limitations and operator conditions

No current external Azure state, pricing, budget, credentials, shared load or
private execution packet was verified. The seven existing conditions remain:

1. **C1 deployment:** intended resource/region/model/version/SKU, endpoint and exact
   strict-schema/low-reasoning service support and availability.
2. **C2 commercial terms:** current pinned EUR rates/unit/provenance, zero separate
   charges and signed maximum sufficient for one bounded attempt.
3. **C3 authorities/funds:** existing shared policy/catalog/paths/scopes, persistent
   ledger integrity/history, unresolved obligations and available funds/allowances.
4. **C4 authorization:** current operator identity/permissions, independent signing
   trust/replay authority, fresh exact source/configuration bindings and unused ID.
5. **C5 credentials/timing:** correct target/audience/header/permissions and fresh
   lifetimes with the existing exclusive 600-second launch margin.
6. **C6 shared capacity:** actual RPM/TPM and all consumers; 25,000+3,000 tokens plus
   protected 2,000 interactive TPM require 30,000 TPM for the full reservation.
7. **C7 exact handoff:** final reviewed corrected-source configuration/acknowledgement,
   actual-scope fixture/request hashes, run identities, existing safe authorities,
   persistent replay and audit ownership/retention.

These are inherited external conditions, not new approval policies. Current
Attempt 5 eligibility remains unverified and **execution authorized: NO**.
The exact historical Attempt 4 rejection and live-model acceptance remain unknown.
Offline tests do not prove semantic quality, service-side schema acceptance,
model compliance, latency, acceptance frequency or the rest of Phase 17H evaluation.
No scope expansion, prompt activation, identifier migration or live attempt follows.

## H. Git preservation and safety

Starting inventory: **20 modified tracked files, 111 untracked files, empty index**.
Starting tracked stat: **20 files changed, 812 insertions(+), 76 deletions(-)**.
This includes substantial earlier Phase 17H–L work and is not an F1 change count.

The task changes only the two existing production files listed above and creates:

- `tests/unit/test_http_cleanup.py`
- `tests/integration/test_http_cleanup_governance.py`
- `docs/codex/prompts/phase_17hl_f1_http_cleanup_failure_preservation.md`
- `docs/codex/reports/phase_17hl_f1_http_cleanup_failure_preservation.md`

Final inventory: **20 modified tracked files and 115 untracked files**, exactly
the starting inventory plus the four new files above. Every starting path remains
present. Final index is empty, and HEAD/branch are unchanged. Final tracked stat:
**20 files changed, 832 insertions(+), 79 deletions(-)**. All 1,678 baseline test
identities are retained and passed; 77 new cases account for the full increase.
No pre-existing test or historical report was edited.
The public source/doc snapshot contains 260 pre-existing Python/Markdown/text
files; 258 are byte-identical, and only the two authorized production paths differ.
It excludes protected/ignored material and real dotenv files; none was opened.
The complete starting inventory and final status/stat are recorded below/in the
external verification directory; no historical report was rewritten.

Paid inference calls, cloud operations, live financial reservations, operator
approval creation/signing/consumption, commits and pushes: **0 each**. Existing
full-suite authentication/approval tests use ephemeral synthetic signatures and
temporary ledgers; these are not operator approvals or real financial operations.
The new governed F1 tests require no signing fixture at all.

## Final verdict

**F1 FIX PASS** for the confirmed expected-I/O cleanup error-precedence defect
and the equivalent owned-session boundary. No remaining engineering blocker was
identified within this narrow task. External conditions and live acceptance remain
unverified. **Attempt 5 execution authorized: NO. Phase 17H remains PARTIAL.**

## Appendix: preserved starting worktree inventory

The final worktree contains every following starting path plus the four task files
listed in section H; only the two permitted production files received F1 edits.
This inventory lists filenames only and does not read secret configuration.

```text
## master...origin/master
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
?? docs/adr/phase_17hl_application_owned_identifiers_assessment.md
?? docs/codex/prompts/phase_17h_live_preflight.md
?? docs/codex/prompts/phase_17hl_ast_test_portability_fix.md
?? docs/codex/prompts/phase_17hl_attempt5_readiness_authorization_assessment.md
?? docs/codex/prompts/phase_17hl_diagnostic_hardening.md
?? docs/codex/prompts/phase_17hl_entra_v2.md
?? docs/codex/prompts/phase_17hl_final_handoff.md
?? docs/codex/prompts/phase_17hl_final_offline_azure_compatibility_audit.md
?? docs/codex/prompts/phase_17hl_first_failure_diagnosis.md
?? docs/codex/prompts/phase_17hl_full_suite_configuration_isolation.md
?? docs/codex/prompts/phase_17hl_l1_attempt3_serialization.md
?? docs/codex/prompts/phase_17hl_live_execution_preparation.md
?? docs/codex/prompts/phase_17hl_live_failure_observability_and_contract_options.md
?? docs/codex/prompts/phase_17hl_offline_e2e_contract_verification.md
?? docs/codex/prompts/phase_17hl_offline_readiness.md
?? docs/codex/prompts/phase_17hl_operator_approval.md
?? docs/codex/prompts/phase_17hl_preflight_observability_timing_hardening.md
?? docs/codex/prompts/phase_17hl_regression_reconciliation.md
?? docs/codex/prompts/phase_17hl_reusable_evaluation_governance.md
?? docs/codex/prompts/phase_17hl_same_day_attempt2.md
?? docs/codex/prompts/phase_17hl_second_attempt_preparation.md
?? docs/codex/prompts/phase_17hl_structured_output_compatibility.md
?? docs/codex/prompts/phase_17hl_two_layer_structured_output.md
?? docs/codex/proposals/managed_prompt_4.patch
?? docs/codex/proposals/phase_17hl_generation_instruction_clarifications.md
?? docs/codex/reports/phase_17h_live_preflight.md
?? docs/codex/reports/phase_17hl_ast_test_portability_fix.md
?? docs/codex/reports/phase_17hl_attempt5_readiness_authorization_assessment.md
?? docs/codex/reports/phase_17hl_azure_strict_schema_live_compatibility.md
?? docs/codex/reports/phase_17hl_diagnostic_hardening.md
?? docs/codex/reports/phase_17hl_entra_v2_report.md
?? docs/codex/reports/phase_17hl_evaluation_activation_readiness.md
?? docs/codex/reports/phase_17hl_evaluation_policy_activation.md
?? docs/codex/reports/phase_17hl_final_offline_azure_compatibility_audit.md
?? docs/codex/reports/phase_17hl_final_operator_authorization.md
?? docs/codex/reports/phase_17hl_first_failure_diagnosis.md
?? docs/codex/reports/phase_17hl_full_suite_configuration_isolation.md
?? docs/codex/reports/phase_17hl_independent_json_byte_limits.md
?? docs/codex/reports/phase_17hl_l1_attempt3_preparation.md
?? docs/codex/reports/phase_17hl_l1_attempt3_serialization_root_cause.md
?? docs/codex/reports/phase_17hl_launch_authorization_final.md
?? docs/codex/reports/phase_17hl_live_execution_preparation.md
?? docs/codex/reports/phase_17hl_live_failure_observability_and_contract_options.md
?? docs/codex/reports/phase_17hl_offline_e2e_contract_verification.md
?? docs/codex/reports/phase_17hl_operator_approval_report.md
?? docs/codex/reports/phase_17hl_output_limit_hardening.md
?? docs/codex/reports/phase_17hl_preflight_observability_timing_hardening.md
?? docs/codex/reports/phase_17hl_regression_reconciliation.md
?? docs/codex/reports/phase_17hl_reusable_evaluation_governance.md
?? docs/codex/reports/phase_17hl_same_day_attempt2_handoff.md
?? docs/codex/reports/phase_17hl_second_attempt_preparation.md
?? docs/codex/reports/phase_17hl_single_call_execution_failure_diagnosis.md
?? docs/codex/reports/phase_17hl_single_call_harness_offline.md
?? docs/codex/reports/phase_17hl_structured_output_compatibility.md
?? docs/codex/reports/phase_17hl_two_layer_structured_output.md
?? docs/engineering/llm_structured_output_validation.md
?? docs/engineering/postmortems/Estudio_PolyMind_Phase17HL_L1_Three_Attempts_Postmortem_2026-10-16.md
?? docs/evaluation/phase_17h_foundry_approval.template.json
?? docs/evaluation/phase_17h_foundry_validation.md
?? docs/evaluation/phase_17hl_operator_approval.md
?? docs/governance/evaluation-binding.template.json
?? docs/governance/evaluation-policy.md
?? docs/security/entra_v2.md
?? documents/digestion/diagnostics.py
?? governance/evaluation.py
?? governance/migration.py
?? llm/azure_schema.py
?? tests/README.md
?? tests/approval_helpers.py
?? tests/conftest.py
?? tests/fixtures/digestion_contracts/README.md
?? tests/fixtures/digestion_contracts/models.py.txt
?? tests/fixtures/digestion_contracts/validation.py.txt
?? tests/integration/test_attempt3_serialization.py
?? tests/integration/test_final_offline_azure_compatibility.py
?? tests/integration/test_foundry_l1_entra.py
?? tests/integration/test_foundry_l1_launcher.py
?? tests/integration/test_foundry_offline_workflow.py
?? tests/integration/test_live_failure_observability.py
?? tests/integration/test_output_limit_hardening.py
?? tests/integration/test_phase17hl_offline_e2e.py
?? tests/integration/test_single_call_harness.py
?? tests/integration/test_single_call_preflight.py
?? tests/integration/test_validation_diagnostics.py
?? tests/performance/foundry_approval.py
?? tests/performance/foundry_budget.py
?? tests/performance/foundry_envelopes.py
?? tests/performance/foundry_l1.py
?? tests/performance/foundry_preflight.py
?? tests/performance/foundry_recalibration.py
?? tests/performance/foundry_schema_diagnostics.py
?? tests/performance/foundry_schema_probe.py
?? tests/performance/foundry_single_call.py
?? tests/settings_isolation.py
?? tests/source_contracts.py
?? tests/unit/documents/test_independent_json_limits.py
?? tests/unit/documents/test_output_limit_sizes.py
?? tests/unit/documents/test_strict_schema_compatibility.py
?? tests/unit/documents/test_two_layer_output.py
?? tests/unit/test_evaluation_activation.py
?? tests/unit/test_evaluation_governance.py
?? tests/unit/test_foundry_30k.py
?? tests/unit/test_foundry_approval.py
?? tests/unit/test_foundry_preflight.py
?? tests/unit/test_foundry_schema_probe.py
?? tests/unit/test_governance_migration.py
?? tests/unit/test_output_limit_diagnostics.py
?? tests/unit/test_security_entra.py
?? tests/unit/test_settings_isolation.py
?? tests/unit/test_single_call_diagnostics.py
?? tests/unit/test_source_contracts.py
```
