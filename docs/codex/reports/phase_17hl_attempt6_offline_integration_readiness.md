# Phase 17H–L — Attempt 6 offline integration readiness

Date: 29 October 2026. Assessment of the current working tree; no live authorization.

## 1. Executive conclusion

**OFFLINE GO for recommending a separately authorized operator-preparation task.**
The actual `prepare_analysis()` path succeeded with `pdf(4, seed=1708)`, selected
one first-chunk analysis and rendered the active `managed-prompt/4` subject rules.
All four managed stages rendered consistent v4 instructions. A predetermined
synthetic response passed strict schema checks, decoding, Pydantic and the full
application `validate_result()` boundary. Each of the four non-factual claim kinds
with a populated subject was rejected as `serialization_error`, with
`claim_contract / subject_on_nonfact`, without repair or another provider attempt.

All four authoritative fingerprints match the implementation report. Disposable
governance admitted one attempt, settled known usage once, and denied another
admission. No critical integration blocker was found. There are **108 distinct
passing checks**, zero final assertion failures, zero skips and zero observed
network attempts. An initial historical-test setup error caused by a relative
synthetic-fixture path was resolved entirely within disposable storage; its
original evidence is retained and explained in section 13.

These findings establish engineering integration under local fakes. They do not
predict future GPT-5.4-mini compliance or grant permission for inference.

## 2. Scope and authorization

Work was limited to source/documentation inspection, selected existing offline
tests, disposable synthetic integration tests and this new report. `AGENTS.md`,
both mandatory Phase 17H–L reports, the operator-approval documentation and the
structured-output engineering documentation were reviewed before test execution.
The narrower task restrictions take precedence over general repository guidance.

No Azure CLI, cloud authentication, web search, external request, Docker,
Kubernetes, deployment, live launcher, signing, approval verification/consumption
or actual-scope launch configuration was performed. No real credentials,
historical raw responses, private operator packet, production financial database
or protected Attempt 5 launch artifact was opened. Attempt 5 remains immutable.
No production source, existing test, fixture, configuration, dependency or
historical documentation was changed. No new permanent test module was added.

## 3. Starting repository state

The measured baseline was **20 modified tracked files, 127 untracked files and
0 staged files**. `git diff --stat` reported **894 insertions, 81 deletions across
20 files**. These are actual observations, independent of prior reports.

Before application imports or testing, `baseline.py` saved full porcelain status,
diff statistics, staged paths, SHA-256 values for **405 existing Git-visible source
and documentation files**, and mode/size/mtime metadata for **854 existing files**
outside `.git`. Potentially sensitive/runtime/binary extensions were excluded
from content hashing; metadata was recorded without reading their contents.
The hash-exclusion list is retained in `baseline.json`. Existing ignored files
were covered by metadata comparison; `.git` was checked through status/staged
state, without history or index mutations. Relevant content hashes appear below.
All assessment files and test output except this report are outside the repository.

The final check found no changed baseline hash or file metadata, no removed
existing file, and exactly this report as the added file. Full starting status
and its observed ending delta appear in section 18.

## 4. Source and implementation inventory

The integration boundaries inspected were:

| Source reference | Role in this assessment |
| --- | --- |
| [fixtures.py:49](../../../tests/performance/fixtures.py#L49) | Seeded PDF construction with existing pypdf; four physical pages checked by PdfReader. |
| [foundry_single_call.py:186](../../../tests/performance/foundry_single_call.py#L186) | Real render-only preparation, extraction, one-chunk selection, evidence checks and input bound. |
| [workflow.py:51](../../../documents/digestion/workflow.py#L51), [workflow.py:108](../../../documents/digestion/workflow.py#L108) | Immutable preparation and analysis StageRequest construction. |
| [planning.py:30](../../../documents/digestion/planning.py#L30), [planning.py:106](../../../documents/digestion/planning.py#L106) | Budget enforcement and deterministic source/profile-bound planning. |
| [managed.py:48](../../../documents/digestion/managed.py#L48), [managed.py:116](../../../documents/digestion/managed.py#L116) | Active stage settings, inference configuration, profile binding and renderer. |
| [models.py:209](../../../documents/digestion/models.py#L209), [models.py:261](../../../documents/digestion/models.py#L261) | Claim, StageResult and StageRequest contracts. |
| [structured.py:115](../../../llm/structured.py#L115), [azure_schema.py:12](../../../llm/azure_schema.py#L12) | Provider schema selection and strict structural conversion. |
| [openai_compatible.py:378](../../../llm/openai_compatible.py#L378), [bounded_http.py:60](../../../llm/bounded_http.py#L60) | Nonstreaming request construction, bounded envelope, metadata and normalized failures. |
| [codec.py:33](../../../documents/digestion/codec.py#L33), [validation.py:64](../../../documents/digestion/validation.py#L64) | Duplicate-safe decoding, structural parsing, canonical bounds, identity/evidence/domain acceptance. |
| [foundry_single_call.py:236](../../../tests/performance/foundry_single_call.py#L236) | Single-analysis composition, post-accounting validation and sanitized terminal audit; inspected statically. |
| [execution.py:10](../../../governance/execution.py#L10), [foundry_budget.py:78](../../../tests/performance/foundry_budget.py#L78), [ledger.py:151](../../../governance/ledger.py#L151) | Governed reservation, admission, attempt and settlement. |
| [foundry_single_call.py:347](../../../tests/performance/foundry_single_call.py#L347), [foundry_approval.py:104](../../../tests/performance/foundry_approval.py#L104) | Pre-consumption configuration revalidation, exact approval binding and replay fences; inspected only. |

The named unit/integration modules were inspected for imports, fixtures and side
effects before selection. Additional reads traced extraction/storage, security
authority, settings isolation, fake transport and source-contract helpers. There
was no architectural redesign or reopening of the completed cleanup investigation.

Relevant starting SHA-256 values, all unchanged at final verification:

| File | SHA-256 |
| --- | --- |
| `documents/digestion/managed.py` | `fa6cd701b73c0cdd486b645a64748f3bb70509b17d310b40c9455c619dbc91a9` |
| `documents/digestion/models.py` | `f767ee7e6cfced13b321028999aee042146ef4265755d7dfd054ae1d5cb96e67` |
| `documents/digestion/planning.py` | `c8cdee6ad7bab07bfc8bbad146923415fd54fe98bc271b78a2300323d8432025` |
| `documents/digestion/validation.py` | `5b6c4efa905758d11b179495f49c88f56e0cfbdcc079274b9d03044ee110a8b4` |
| `documents/digestion/workflow.py` | `54807af2a1a61098e676f1086d9dd3c5716b4990bfbf4e2e0e15f2d9fc652e28` |
| `documents/digestion/codec.py` | `9e5c7afbb0ac2574a909fda4da7eaacc9376e61b7e10960daa8c4e327953b768` |
| `llm/structured.py` | `ce24763d62ce3ded77c41630fcdd9aa2766212183d89baac5bc24777d13c9334` |
| `llm/azure_schema.py` | `36cab2377fb6cbf850c1e58e83f03e8861c056ee4d44bba8cc6e0749cc7abf25` |
| `llm/openai_compatible.py` | `d0505c5297e8259f6737324cfe5a65867d7551c0f2b98949c103f2a14df752db` |
| `tests/performance/foundry_single_call.py` | `c016a3c90bd5fef7a3a35ccfaa5efe26e21019ced02c9db1782629e37275e761` |
| `tests/performance/foundry_l1.py` | `7f90695897cb4056b290f3ff79d414aa274469824b5e7f2155f10cd82679fc3c` |
| `tests/performance/fixtures.py` | `a33f17840fa31080086afea070256f6616e1d315cef79517a3c3c60b0d944dbc` |
| `governance/execution.py` | `979abd479f0b8cdddc79193b5dc76fe1f2a7e07269e9c5eb6264c84f1b2fd134` |
| `governance/ledger.py` | `de6f45b910b2ecadab466cd26119ebda0b4facac5d35037f0c9df6c19c4f28d6` |
| `tests/performance/foundry_budget.py` | `07305ea077f9003192e72120c5d4c61443f9254fc4dfcee4f305c967d8dd81da` |
| `docs/codex/reports/phase_17hl_attempt5_post_execution_diagnostics.md` | `5de835200ce0d302cd95e4e1885a6208d5cd97c268f510d4ac54da7e9cd83556` |
| `docs/codex/reports/phase_17hl_managed_prompt4_subject_contract_implementation.md` | `d23f558d0222f4c29b61a9ba0e225e02564f1d0f2e0746e401d646051e192e11` |

## 5. Deterministic fixture preparation

Two independent invocations of the actual public `prepare_analysis()` function
used separate disposable object-store roots and the same explicitly synthetic
owner scope. `PreparationProvider` supplied only the deployment identity. An
observer that would fail on its execution recorded **0 calls**. No alternate
preparation implementation was substituted.

| Observation | Measured result |
| --- | --- |
| Fixture | `phase17h-pdf/1`, `pdf(4, seed=1708)`, six lines per page |
| Extracted document units | 4 |
| Planned analysis chunks / selected stages | 1 / 1, first chunk |
| Request source pieces / distinct evidence IDs | 4 / 4 |
| Source evidence resolution | Every piece resolves to its extracted text |
| Cross-preparation stability | Source IDs, StageRequest, rendered generation, fixture hash and request hash equal |
| Rendered request sizing | 11,213 canonical ASCII bytes; conservative input estimate 11,413 |
| StageRequest size including template allowance | 4,517 estimated tokens |
| Completion reservation / context envelope | 3,000 / 28,000 tokens |
| Raw / canonical / HTTP-envelope ceilings | 10,000 / 10,000 / 26,192 bytes |
| Provider calls / network attempts in preparation | 0 / 0 |

The input estimate is a conservative project estimator, not measured model tokens.
It is below 25,000 and, with output, below 28,000; rendered size also remains below
the 24,800 stage input bound. The fixture SHA-256 was
`1be99e19a56040fb55c74682a19f874d4d4573f18d9f52a9a7ae19c8158ea92d`.
The freshly computed synthetic rendered-request SHA-256 was
`871a243b3317103ab8b143750aad6597b0daded1458e887bedb2fe8f79f0dcdf`.
This is synthetic-scope evidence, not an Attempt 6 launch binding.

`DigestionHandler.request(plan, plan.chunks[0].chunk_id, {}, {})` supplies the
analysis-stage ID and source pieces; the function itself checks one chunk and
four units. The request has no children or tools. Preparation wrote immutable
synthetic extraction/planning objects only: no SQLite authority, approval, replay
marker or financial record was created. Current source generated every binding;
no historical v3 request/hash was reused.

## 6. Active prompt/version integration

Direct rendering tests covered `chunk`, `intermediate`, `structural` and `root`.
StageProfile, planning prompt profile and renderer control all agree on
`managed-prompt/4`; strict settings use `managed-generation/2`. The intermediate
test renders real validated reduction child material through that stage profile.
Historical/active request tests independently compare the rendered contents.

The actual provider-facing system text contains the following subject guidance,
verified as a complete paragraph rather than inferred from a version constant:

| Claim kind | Rendered subject instruction |
| --- | --- |
| `fact` | Null or a populated valid Token is allowed. |
| `unknown` | `subject=null` |
| `unsupported` | `subject=null` |
| `commentary` | `subject=null` |
| `structural` | `subject=null` |

It also forbids empty/blank substitutes, retains the 1–128 character
`^[a-zA-Z0-9_./:-]+$` Token rule, forbids changing kind to fact merely to retain a
subject, and requires supported factual status with authorized evidence. Required
fields, explicit defaults/nulls, deterministic ordered claim IDs, stage origin,
untrusted-data separation and no-tools instructions remain present. Analysis
references source evidence; reducers retain required child lineage. No semantic
normalization, repair or additional inference pass was introduced. The unrelated
source-coverage/qualification wording topics were left untouched.

## 7. Historical v3 rejection

The 11 selected managed tests establish four-stage rejection of explicit v3
settings, rejection of stale prompt/inference/configuration labels before any
provider call or admission, and non-retryable subject rejection for all four
non-factual kinds. The isolated historical-source test calls the real
configuration model validators using public old executor/generation hashes;
they fail with `Execution contract changed` without loading a private configuration.

Nine frozen v3 request/generation/payload witnesses reproduced their original
hashes under the existing hash-pinned test-only historical module. All corresponding
v4 witnesses differ. The archived renderer checksum is still
`5b272d4a7591692eeeb328da09bc39b35d402bebd1d8ada3b891f6b1d6e8928c`.
No witness was regenerated or overwritten. Historical synthetic StageResults and
an actual stored synthetic v3 checkpoint remain readable and valid under their
original evidence context. The active renderer refuses the old request; it does
not upgrade a stale plan in place.

Old signed approval behavior was assessed through source binding, not signing or
consumption: `_launch()` revalidates the current configuration before identity,
approval and replay work; the model requires current executor/generation/schema
hashes. `verify_artifact()` compares the exact reviewed configuration binding.
The old source hashes fail independently in the non-signing tests. This establishes
that an old v3 approval cannot authorize the changed executor without changing
its signed binding. Cryptographic/replay execution was deliberately excluded.

## 8. Fingerprint verification

The disposable test invoked `executor_digest()`, `generation_contract_digest()`,
`fingerprint(provider_schema(generation_schema()))` and the actual managed adapter
configuration calculation with the non-executing preparation identity stub.

| Binding | Recomputed SHA-256 | Comparison with v4 implementation report |
| --- | --- | --- |
| executor | `d9af24e556305246ec145d15b3511e3e65fcf4e955e5b5f0dc550b4119b58a75` | MATCH |
| generation | `74cf9320b0ebf6d45df531e81827c5a8710b5b4d58fa75aad05dfa5039552290` | MATCH |
| inference_configuration | `71adc072da8e99d47b81afa859e78bde4866e633ae0e841e0b17f48d6450b831` | MATCH |
| provider_schema | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` | MATCH |

`executor_digest()` hashes all Python sources beneath documents, governance,
security, llm and tests/performance. `generation_contract_digest()` hashes its
explicit twelve-file source inventory, including managed rendering/planning,
provider/schema code, fixtures and preflight composition. The configuration
digest binds serialized current settings, provider identity, deployment model
and converted provider schema. These are executed deterministic calculations,
not copied-constant comparisons alone. No mismatch or post-report contributing
source change was detected. No full private launch-configuration digest was made.

## 9. Provider-facing request verification

The real OpenAI-compatible adapter executed only against the existing in-memory
`HTTP`/`Response` fakes at `https://offline.invalid/openai/v1`. No requests.Session
or network-connected transport was constructed. Captured payloads used deployment
`epolymind-gpt-54-mini`, `stream=false`, `max_completion_tokens=3000`,
`reasoning_effort=low`, and strict `response_format.json_schema` named
`polymind_stage_result`. The emitted schema equals the established converter
output. There are no tools, tool choice, legacy max_tokens or temperature fields.

The schema profile remains `azure-strict/1`; the domain contract remains
`stage-result/1`. The unchanged schema hash and conversion test cover closed
objects, all required fields and nullable subject structure. Conditional subject
semantics remain application-owned. Raw response, canonical result and HTTP
envelope ceilings remain separate at 10,000, 10,000 and 26,192 bytes; request
deadline is 60 seconds. Bounded HTTP reading uses one post with redirects disabled.
Source inspection confirms the actual launcher installs an HTTPS adapter with
`max_retries=0`, disables environment trust, and provides no fallback or repair
loop. Fake response bodies are closed after reading.

Resource `epolymind-foundry-dev-susanta`, deployment `epolymind-gpt-54-mini`, model
`gpt-5.4-mini` (allowed versioned response `2026-03-17`), Spain Central and
GlobalStandard are intended future operator bindings from supplied history/public
source. Their current live existence, state and actual private configuration were
not checked. No public constant is treated as current cloud evidence.

## 10. Synthetic end-to-end StageResult acceptance

The disposable valid test used actual `prepare_analysis()` extraction/planning,
real source evidence and the active renderer. One predetermined, field-complete
factual claim used the supplied first claim ID, exact originating stage, supported
status, a valid factual subject and all four authorized evidence IDs.

That authored response traversed the real OpenAI-compatible envelope/metadata
handling, `GovernedExecution`, bounded decoding and the complete `validate_result()`
call after authority revalidation. Both generation/provider JSON schemas, Pydantic
and duplicate-safe decoding accepted it; domain validation checked canonical
serialization, stage/claim identity, source resolution/membership and full coverage.
The 648-byte raw result also fit canonical serialization within 10,000 bytes.
The accepted result equaled the authored model; observed usage was 21 input,
7 output, 28 total tokens, entirely synthetic.

An existing single-analysis/deployment-alias integration test independently passed
the same provider-to-full-validator boundary. The protected `launch()` and
`execute_stage()` wrapper were not invoked. The disposable composition called
their real preparation, governed execution, decoding and validation components;
wrapper-specific order and closed audit handling were assessed statically. No
acceptance decision or security check was monkeypatched away. No digest publication
or reduction was invoked by this synthetic single-analysis composition.

The fake response proves wiring and acceptance behavior only. It provides no
evidence that the live model will produce an equally valid result.

## 11. Negative subject-contract control

Four controls reused the same real preparation/validation path, changing claim
kind to each non-factual kind and supplying a populated valid-token subject.
Each passed provider JSON Schema, generation JSON Schema, JSON decoding and
Pydantic. Each then failed the actual domain validator at the fact-only predicate:

```text
provider response: completed structured output
application validation: rejected
public failure: serialization_error
classification: NON_RETRYABLE
diagnostic: claim_contract
reason: subject_on_nonfact
provider attempts: 1
```

No field deletion, kind rewrite, retry, fallback, second-pass correction or silent
acceptance occurred. Invalid raw content and synthetic private marker did not
appear in serialized sanitized error evidence. The existing 35-case subject
matrix additionally exercises null/missing/valid/blank/invalid/type cases, retaining
the structural-versus-domain distinction and null factual subjects.

## 12. Governance and settlement

Each disposable case used synthetic unsigned principal issuance from the existing
test seam, a new local SecurityAuthority, GovernanceLedger, SQLiteInferenceAdmission
and a real RunGuard with `attempts=1`, 25,000 input and 3,000 output limits. Prices
were explicitly synthetic arithmetic: EUR 0.1/0.2 per million input/output tokens.
These are not Azure prices or an operational financial approval.

Observer wrappers counted calls without changing underlying decisions: exactly
one reserve, downstream admission, settlement invocation and admission finish per
case. One run record, one provider attempt and one financial row resulted.
Known usage settled to `SETTLED` in both the accepted case and all four application
rejections. Another scoped admission was refused by the real max-one guard before
downstream admission/provider execution.

For these cases `cost=0.0017413` represented the conservative pre-call reservation;
`actual_cost=0.0000035` represented settled 21/7 token usage. Neither was overwritten
with the other. Application failure therefore legitimately coexists with completed
provider usage and `SETTLED` finance, consistent with the supplied Attempt 5 outcome.

A fake transport connection failure produced `inference_unavailable`, one attempt,
an unresolved `UNKNOWN` row and a stopped guard; it never retried. Its generic
classifier remains `RETRYABLE`, but the single-call policy does not schedule a
retry. Unknown usage was not falsely settled as known. Completed calls retained
one finished run record even when subsequent application validation rejected them.
There were six isolated synthetic financial cases, no real financial mutations.

## 13. Tests and safety

The prior 447-test result is historical and was not reused as current evidence.
The selected current checks cover the remaining narrow integration questions:

| Test/module selection | Executed distinct cases | Passed | Failed | Skipped | Network attempts |
| --- | ---: | ---: | ---: | ---: | ---: |
| `test_managed_inference.py`: stale labels, explicit v3 settings, subject rejection/no retry | 11 | 11 | 0 | 0 | 0 |
| `test_two_layer_output.py`: conversion, 35-case subject matrix, public historical source gates | 37 | 37 | 0 | 0 | 0 |
| `test_source_contracts.py`: frozen domain types/validation/serialization | 9 | 9 | 0 | 0 | 0 |
| `test_single_call_diagnostics.py`: bounded closed HTTP rejection/privacy | 21 | 21 | 0 | 0 | 0 |
| `test_final_offline_azure_compatibility.py`: actual single-analysis/deployment alias | 1 | 1 | 0 | 0 | 0 |
| `test_live_failure_observability.py`: historical witnesses, active rendering, checkpoint readability, all four stages | 21 | 21 | 0 | 0 | 0 |
| Disposable `/tmp/.../test_readiness.py`: real preparation, fingerprints, valid/four invalid/transport governed paths | 8 | 8 | 0 | 0 | 0 |
| **Final distinct total** | **108** | **108** | **0** | **0** | **0** |

Session evidence, including the initial environment error:

| Session / retained JUnit | Executed | Passed | Assertion failures | Setup errors | Skipped | Network attempts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `core.xml` | 78 | 78 | 0 | 0 | 0 | 0 |
| `history.xml`, first invocation | 22 | 2 | 0 | 20 | 0 | 0 |
| `history-recheck.xml` | 22 | 22 | 0 | 0 | 0 | 0 |
| `synthetic.xml` | 8 | 8 | 0 | 0 | 0 | 0 |

The initial 20 setup errors were `FileNotFoundError` at
`foundry_preflight.questions():292` for relative
`tests/fixtures/phase17h/quality.json` in the disposable cwd. The fixture-dependent
workflow had reached its later synthetic question stage; these were not v4
assertion failures. After inspecting that public synthetic JSON, an unchanged
copy was placed at the expected relative path within `/tmp`. The same selected
22 cases passed. No production/test path, decision, safeguard or frozen witness
was patched. The original log/JUnit remain retained. Across all invocations there
were 130 case instances: 110 passes and 20 resolved setup errors; the final distinct
set is 108. This environment correction does not conceal a current test failure.

The previous `/tmp/polymind_e2e_offline_guard.py` was read: it denies connect,
connect_ex, sendto and DNS and records attempts. A disposable stricter alternative
was installed before relevant imports, additionally denying send/sendall/sendmsg,
using socket audit hooks, and denying subprocess execution and writes outside
`/tmp` in the test sessions. Protected secret path access was denied as an extra
guard. This is Python-level isolation, not an OS firewall. All four session safety
files show **0 network attempts and 0 safety violations**; no prohibited operation
attempt required investigation.

The subprocess environment was built from a small explicit allowlist, with no
inherited Azure/OpenAI/Entra/operator credential variables. HOME and cwd were
disposable. Existing `tests.settings_isolation` disabled implicit application
dotenv loading before application settings imports; ManagedSettings also used
no private environment. Bytecode writes and third-party pytest plugin autoload
were disabled. Cache, basetemp, logs and JUnit were redirected under the single
temporary root. Each session emitted only a benign pytest warning that the
already-installed guard could not be assertion-rewritten.

Excluded from execution: approval-dependent `rig`/`composition` tests in
single-call harness, validation diagnostics, signed launcher and live failure
audit modules; identity token-signing and approval/replay tests; live CLI paths;
private pricing/authority configuration. Source inspection plus unsigned local
component tests supplied the relevant evidence. The L1 historical witness fixture
does run its existing multi-stage synthetic workflow to reproduce immutable
history; those fake calls are separate from the counted one-attempt cases and
do not indicate a second call in single-analysis execution. No other broad suite
was run after the required checks passed. Compileall, lint-fix, Docker and cloud
checks were unnecessary/out of scope for this read-only assessment and were not run.

## 14. Readiness gate matrix

| Gate | Result | Direct or specific source-backed evidence |
| --- | --- | --- |
| Deterministic fixture preparation | PASS | Two real preparations, four units, identical source/request hashes. |
| First-chunk analysis selection | PASS | Real function requires one chunk, selects `plan.chunks[0]`, no children. |
| Active v4 prompt rendering | PASS | Actual subject paragraph and fresh current-source generation. |
| Four-stage version consistency | PASS | Four rendering/acceptance witnesses and four explicit-v3 rejection cases. |
| Historical v3 rejection | PASS | Pre-admission stale-label tests, old source-gate rejection, archived request refusal; approval binding inspected statically. |
| Source fingerprint consistency | PASS | All four authoritative calculations equal recorded v4 values. |
| Provider schema invariance | PASS | Same hash, strict schema conversion and frozen domain checks. |
| Valid StageResult acceptance | PASS | Real preparation → fake HTTP → governance → full validator. |
| Invalid subject rejection | PASS | Four completed negative controls; exact non-retryable diagnostic. |
| One-provider-attempt enforcement | PASS | One counted attempt per case; real RunGuard denies another; launcher has one execute path/no retry loop. |
| Disposable financial settlement | PASS | Counted reserve/admit/settle/finish, known usage SETTLED, transport UNKNOWN. |
| Sanitized diagnostics | PASS | Synthetic marker/raw-body exclusion and 21 existing closed-diagnostic controls; wrapper audit allowlist inspected. |
| Repository preservation | PASS | 405 content hashes/854 metadata entries unchanged; only this report added. |
| Network isolation | PASS | Guard active before imports; zero attempts/violations in every session. |

PASS on a source-backed boundary does not claim execution of excluded cryptographic
or live authorization paths. The exact tested acceptance boundary is stated in
section 10. All critical offline gates have sufficient evidence; none remains
NOT_TESTED or INCONCLUSIVE within this task's engineering scope.

## 15. Remaining uncertainties

No unresolved engineering blocker was identified. The cwd-dependent existing
historical fixture needs its public JSON available when run outside the repository;
the disposable copy resolved this assessment without changing source.

Future operator-only prerequisites remain unverified: current Azure deployment
availability and resource/model/region/SKU binding; valid inference credentials;
current Entra operator token and authority; quota, rate limits and shared-consumer
attestation; financial authorization/allowances; current pricing and charge bounds;
a fresh private launch configuration and newly computed actual-scope request
bindings; an independent JWS approval; an eligible execution window; and explicit
final live authorization. Existing protected artifacts were not inspected for
freshness. No inference about current billing or quota is made from local arithmetic.
Future model adherence and semantic response quality remain unknown.

## 16. Final decision

```text
OFFLINE GO
```

The actual preparation path, rendered v4 instructions, unchanged structural/domain
contracts, stale-binding rejection, full synthetic acceptance, exact subject
rejection, one-attempt governance and known-usage settlement all integrate as
intended. Source hashes match and repository/network safeguards were preserved.
The resolved fixture-location setup errors do not establish an implementation
defect. This decision applies only to engineering readiness for a separately
authorized operator-preparation stage.

## 17. Next authorized boundary

A future operator-preparation task requires separate authorization. It must review
fresh actual-scope bindings and the operator prerequisites above. This assessment
creates no launch configuration, signing material, approval, executable live
command, execution window or inference authority. Live inference and Attempt 6
execution remain unauthorized. Work stops after this report and preservation check.

## 18. Repository integrity and safety declaration

Starting full `git status --porcelain=v1 --untracked-files=all`:

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
?? docs/adr/phase_17hl_application_owned_identifiers_assessment.md
?? docs/codex/prompts/phase_17h_live_preflight.md
?? docs/codex/prompts/phase_17hl_ast_test_portability_fix.md
?? docs/codex/prompts/phase_17hl_attempt5_final_readiness_and_operator_preparation.md
?? docs/codex/prompts/phase_17hl_attempt5_operator_authorization_and_single_call_execution.md
?? docs/codex/prompts/phase_17hl_attempt5_readiness_authorization_assessment.md
?? docs/codex/prompts/phase_17hl_diagnostic_hardening.md
?? docs/codex/prompts/phase_17hl_entra_v2.md
?? docs/codex/prompts/phase_17hl_f1_http_cleanup_failure_preservation.md
?? docs/codex/prompts/phase_17hl_final_handoff.md
?? docs/codex/prompts/phase_17hl_final_offline_azure_compatibility_audit.md
?? docs/codex/prompts/phase_17hl_first_failure_diagnosis.md
?? docs/codex/prompts/phase_17hl_full_suite_configuration_isolation.md
?? docs/codex/prompts/phase_17hl_l1_attempt3_serialization.md
?? docs/codex/prompts/phase_17hl_live_execution_preparation.md
?? docs/codex/prompts/phase_17hl_live_failure_observability_and_contract_options.md
?? docs/codex/prompts/phase_17hl_managed_prompt4_subject_contract_implementation.md
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
?? docs/codex/reports/phase_17hl_attempt5_final_readiness_and_operator_preparation.md
?? docs/codex/reports/phase_17hl_attempt5_live_execution_report.md
?? docs/codex/reports/phase_17hl_attempt5_operator_authorization_and_single_call_execution.md
?? docs/codex/reports/phase_17hl_attempt5_operator_checklist_verification.md
?? docs/codex/reports/phase_17hl_attempt5_post_execution_diagnostics.md
?? docs/codex/reports/phase_17hl_attempt5_readiness_authorization_assessment.md
?? docs/codex/reports/phase_17hl_azure_strict_schema_live_compatibility.md
?? docs/codex/reports/phase_17hl_diagnostic_hardening.md
?? docs/codex/reports/phase_17hl_entra_v2_report.md
?? docs/codex/reports/phase_17hl_evaluation_activation_readiness.md
?? docs/codex/reports/phase_17hl_evaluation_policy_activation.md
?? docs/codex/reports/phase_17hl_f1_http_cleanup_failure_preservation.md
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
?? docs/codex/reports/phase_17hl_managed_prompt4_subject_contract_implementation.md
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
?? tests/fixtures/digestion_contracts/managed_prompt3.py.txt
?? tests/fixtures/digestion_contracts/managed_prompt4.json
?? tests/fixtures/digestion_contracts/managed_prompt4_subject.txt
?? tests/fixtures/digestion_contracts/models.py.txt
?? tests/fixtures/digestion_contracts/validation.py.txt
?? tests/integration/test_attempt3_serialization.py
?? tests/integration/test_final_offline_azure_compatibility.py
?? tests/integration/test_foundry_l1_entra.py
?? tests/integration/test_foundry_l1_launcher.py
?? tests/integration/test_foundry_offline_workflow.py
?? tests/integration/test_http_cleanup_governance.py
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
?? tests/unit/test_http_cleanup.py
?? tests/unit/test_output_limit_diagnostics.py
?? tests/unit/test_security_entra.py
?? tests/unit/test_settings_isolation.py
?? tests/unit/test_single_call_diagnostics.py
?? tests/unit/test_source_contracts.py
```

The observed ending status consists of **exactly the same entries above**, plus:

```text
?? docs/codex/reports/phase_17hl_attempt6_offline_integration_readiness.md
```

Ending totals: **20 modified tracked, 128 untracked, 0 staged**. The existing
tracked `git diff --stat` is unchanged at start and end:

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

Git's tracked diff statistics exclude the new untracked report. Final integrity
verification compares actual ending status with the full starting status plus
that exact report path, compares every captured hash and metadata entry, and
compares the diff statistics/staged list. Results: **0 existing-file changes,
0 removals, 1 new report, 0 staged changes**. `git diff --check` exited **0** with
no output; the report was separately checked for trailing whitespace/final newline
because Git does not include untracked files in that command. Review of this
report found no secrets, private identity data, raw historical response, executable
live command or unrelated change.

All temporary artifacts are beneath `/tmp/polymind-attempt6-offline-readiness/`:
`baseline.py`, `baseline.json`, `offline_guard.py`, `run.py`, `test_readiness.py`,
`verify.py`, `write_report.py`, `integrity.json`, `observations.json`,
`test-counts.json`, `core.log/xml`, `history.log/xml`, `history-recheck.log/xml`,
`synthetic.log/xml`, per-session `*-safety.json`, `home/`, `pytest-cache/`,
`core-tmp/`, `history-tmp/`, `history-recheck-tmp/`, `synthetic-tmp/`, and the
unchanged copied synthetic `tests/fixtures/phase17h/quality.json`. Databases,
generated PDFs, objects, historical synthetic checkpoints and workflow output
are contained within those disposable test roots. The pre-existing
`/tmp/polymind_e2e_offline_guard.py` was only read, not modified.

| Safety observation | Result |
| --- | --- |
| New repository file | `docs/codex/reports/phase_17hl_attempt6_offline_integration_readiness.md` |
| Existing repository files changed by this assessment | 0 |
| Actual external provider calls | 0 |
| Observed network attempts | 0 |
| Approval/signing/consumption operations | 0 |
| Real financial mutations | 0; six disposable synthetic cases only |
| Protected-state modifications | 0 |
| Source/configuration/fixture fingerprint edits | 0 |
| Commits / pushes | 0 / 0 |
