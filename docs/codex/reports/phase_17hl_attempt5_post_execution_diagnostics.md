# Phase 17H–L — Attempt 5 post-execution diagnostics

Date: 29 October 2026. Scope: offline investigation and proposed correction only.

## 1. Executive conclusion

Attempt 5 made one governed request and **completed a strict provider response**, then failed application acceptance with `serialization_error`, supplemental diagnostic **`claim_contract / subject_on_nonfact`**. The operator-supplied durable outcome reports one run, one governance record, `accounting_failed=false` and **SETTLED** usage. Application rejection does not undo the completed, accounted provider work.

**CONFIRMED contract misalignment; VALIDATOR_CORRECT.** The application permits a non-null `Claim.subject` only when `Claim.kind == 'fact'`. Neither `managed-prompt/3` nor `generation_schema()` expresses that conditional rule. The converted `azure-strict/1` schema also permits the combination. The omission exists before Azure schema conversion: the Pydantic-generated application schema itself accepts a populated subject on every claim kind. Pydantic parsing likewise accepts that combination; the application-owned `validate_result()` rejects it later.

An isolated reproduction using real extraction, planning, evidence resolution, deterministic claim IDs, models and `validate_result()` confirms this boundary. All four non-fact kinds pass both JSON schemas and Pydantic with a populated valid-token subject, then fail with the exact reported diagnostic. Changing only that subject to null yields full `validate_result()` acceptance. **39 synthetic cases passed their expected assertions; 111 selected existing offline tests passed.** No production or existing test file changed.

The confirmed finding explains how strict structural success and domain rejection coexist. It does **not** establish the exact historical claim kind, subject, claim index, number of violations, or why the model chose that combination. No historical raw response was opened or reconstructed. Whether the response remains retained was not investigated. Improved model compliance after clarification remains an untested hypothesis.

Recommend a separately authorized, narrowly versioned prompt correction: explicitly state the fact-only subject rule, retain optional subjects on facts and preserve all evidence/identity checks. Use a new `managed-prompt/4` binding; do not relabel or rewrite version 3 or Attempt 5 artifacts. Keep the provider schema, validators, token/byte limits, retry policy and financial policy unchanged. Attempt 6 engineering status is **NO-GO pending implementation and offline regression review**; no live execution is authorized here.

## 2. Immutable Attempt 5 evidence

The terminal values below are the authoritative **operator-observed evidence supplied with this task**. They were not independently reread from private launch configurations, audit files or authority databases.

```text
state: FAILED                       calls: 1
provider_acceptance: completed_strict_response
application_validation: failed      failure: serialization_error
validation_diagnostic: claim_contract
validation_reason: subject_on_nonfact
accounting_failed: false
```

| Provider metric | Value | Interpretation |
| --- | ---: | --- |
| Prompt tokens | 2,342 | Measured input |
| Completion tokens | 1,852 | Includes the reported reasoning tokens |
| Reasoning tokens | 320 | Subset of completion usage; do not add again |
| Total tokens | 4,194 | 2,342 + 1,852 |
| Completion ceiling | 3,000 | No observed breach; 1,148 tokens below ceiling |
| Finish reason | `stop` | Completed response |
| Raw response bytes | 4,395 | UTF-8 content measurement, not total HTTP envelope size |
| Raw response ceiling | 10,000 | No observed breach; 5,605 bytes below ceiling |

The one supplied governance row is `SETTLED`, with `actual_input=2342`, `actual_output=1852`, `actual_cost=0.008879355860613052`, and `cost=0.019075369588175428`. These are EUR catalog-accounting amounts, not an independently issued Azure invoice.

Execution identity: resource `epolymind-foundry-dev-susanta`; deployment `epolymind-gpt-54-mini`; model `gpt-5.4-mini`, version `2026-03-17`; Spain Central; `GlobalStandard`. Executor `polymind-single-analysis/1`, generation `managed-generation/2`, prompt `managed-prompt/3`, provider schema `azure-strict/1`, domain `stage-result/1`. Fixture `pdf(4, seed=1708)`; one first-chunk analysis; maximum provider attempts 1, retries 0, fallbacks 0. The supplied history establishes successful independent approval verification for audience `polymind-single-analysis-live`. No Kubernetes/AKS workload was involved.

Recomputed through established functions with application settings isolated and network denial installed before application imports:

| Binding | Historical and current SHA-256, equal |
| --- | --- |
| `executor_digest()` | `82fc01aa0447d4be758124cec0120a06db49f139f69ee6425b51b8696a6ad26f` |
| `generation_contract_digest()` | `7d387a8595cf63e2ac944a25c4987a1b37392aa4adba8889914acf51ff9f0f59` |
| `fingerprint(provider_schema(generation_schema()))` | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` |
| `ManagedSynthesisInference.config` | `7eaa6b52ad387f9f0c82e318e9c74fa378ffda0baec85d0f7157cc4ab0553519` |

Sources: `tests/performance/foundry_single_call.py:42` hashes transitive Python source; `tests/performance/foundry_l1.py:31` hashes its explicit generation-source inventory; `documents/digestion/managed.py:129` fingerprints settings/provider/model/schema. The configuration calculation used the public `prepare_analysis()` settings and a no-execution stub with the identical provider/model identity. It did not construct an HTTP client, invoke preparation on historical data, or load signed configuration. This inference-settings digest is distinct from the complete private `configuration_digest()`.

The matching bindings support applying this source diagnosis to the historical implementation. Existing dirty working-tree changes are part of the matching baseline; they are not new changes from this investigation. No hash was forced, updated or inserted into protected state.

## 3. Historical failure progression

| Attempt | Supported finding and engineering progression |
| --- | --- |
| 1 | Retained [first-failure diagnosis](phase_17hl_first_failure_diagnosis.md) identifies 2,597 raw bytes expanding to 3,471 canonical bytes against a 3,000-byte ceiling. Explicit default fields and aggregate ASCII budgeting were added; subsequent work separated/increased byte limits. This was not proof of token truncation. |
| 2 | [Output-limit hardening](phase_17hl_output_limit_hardening.md) records output-limit ambiguity and finish-time accounting classification/masking corrections. Historical missing finish/size evidence remained unknown; the reported 1,922 completion tokens alone did not establish exhaustion. Independent raw/canonical limits were addressed subsequently. |
| 3 | Valid JSON violated the application structural contract. The supplied task broadly describes identity and extra-field problems; the retained [detailed diagnosis](phase_17hl_l1_attempt3_serialization_root_cause.md) specifically identifies a malformed **evidence UUID** and eight forbidden top-level fields. It does not establish a deterministic `claim_id` mismatch. Preserve that distinction rather than retroactively substituting one identity failure for another. |
| 4 | Operator history and [the prior contract review](phase_17hl_live_failure_observability_and_contract_options.md) establish strict completion followed by `serialization_error`; the exact rejected predicate remains unproven. Subsequent diagnostics added closed reason identifiers. The completed [F1 cleanup fix](phase_17hl_f1_http_cleanup_failure_preservation.md) is preserved and not reopened. |
| 5 | Strict completion again; the new reason identifies the actual boundary: `claim_contract / subject_on_nonfact`. It is a more precise instance of a previously documented semantic generation-contract gap, not demonstrated recurrence of Attempt 3's malformed UUID/extra fields. No evidence establishes that Attempt 4 failed this same predicate. |

The requested reports exist at their named paths. The [operator checklist](phase_17hl_attempt5_operator_checklist_verification.md), [final readiness](phase_17hl_attempt5_final_readiness_and_operator_preparation.md), [authorization/preparation report](phase_17hl_attempt5_operator_authorization_and_single_call_execution.md), and existing [live-execution report](phase_17hl_attempt5_live_execution_report.md) contain preparation-era checkpoints. In particular, the latter still states blocked/unexecuted at its retained checkpoints. Those statements describe earlier observations; they do not override this task's later authoritative terminal result. None was edited.

The [earlier compatibility audit](phase_17hl_final_offline_azure_compatibility_audit.md), in its prompt audit and field matrix, had already identified fact-only subjects as absent from explicit prompt prose. The [inactive clarification proposal](../proposals/phase_17hl_generation_instruction_clarifications.md) also describes this rule. Neither proposal nor `managed-prompt/4` is active in the matching source. This investigation supplies specific Attempt 5 attribution and reproduction, not a new broad readiness audit.

## 4. Execution-to-validation trace

References below use current line numbers in the fingerprint-matching working tree.

| Boundary / functions | Input → output, invariants and failure handling | Existing associated tests |
| --- | --- | --- |
| `tests/performance/fixtures.py:49` `pdf`; `foundry_single_call.py:186` `prepare_analysis` | Four-page deterministic fixture → extraction/plan/first analysis. `prepare_analysis` requires four units and one chunk, compares resolved pieces with extraction, renders and hashes the request, and checks estimate ≤25,000. This function was inspected, not executed against Attempt 5. | `test_final_offline_azure_compatibility.py:605`; preparation/harness tests inspected historically |
| `documents/extraction.py:101` `extract`; `documents/digestion/planning.py:106` `build_plan` | Bytes → immutable extraction refs → deterministic plan/chunks. `SourcePiece.evidence_id()` (`models.py:161`) hashes the actual evidence ref; it is not an arbitrary model citation. | `test_digestion.py:77,95`; synthetic extraction used in this reproduction |
| `documents/digestion/workflow.py:108` `DigestionHandler.request`; `models.py:261` `StageRequest` | First chunk → `stage='analysis'`, nonempty source data, no children, distinct input IDs, no tools. `check_request` (`planning.py:30`) revalidates/encodes and enforces context budgeting. | `test_digestion.py:225`; managed rendering tests |
| `documents/digestion/managed.py:151` `render` | Request → provider-neutral `GenerationRequest`. Validates configuration, chunk/analysis pairing, role/model, output reservation and request budget. Supplies allowed evidence IDs, deterministic claim IDs, stage binding, field-complete schema, untrusted-data separation and all four stage task variants. | `test_managed_inference.py:270,286`; frozen rendering tests inspected |
| `managed.py:30` `generation_schema`; `llm/structured.py:115`; `llm/azure_schema.py:12` `provider_schema` | Pydantic schema → all properties required → narrow Azure structural schema. Unknown constructs fail closed with configuration error; semantic `validate_result` predicates are not discovered or compiled. | `test_two_layer_output.py:39,75,85,114` |
| `llm/openai_compatible.py:378` `execute` | Generation → nonstreaming Chat Completions request with `max_completion_tokens=3000`, strict `response_format`, no tools/retries. Validates response envelope, usage, refusal/finish/model metadata and raw byte bound. Returns content/usage/closed metadata; it does not locally prove every output satisfies JSON Schema or domain policy. | `test_two_layer_output.py:145,161`; fake transport only in selected tests |
| `governance/execution.py:15` `GovernedExecution.execute`; `foundry_budget.py:103,136` `RunGuard.acquire/finish` | Governed request → provider attempt and settlement. Reservation/STARTED precede execution; settlement and admission finish occur in `finally` before returning. Guard records one bounded attempt; known usage and completion finalize it. | Governed harness/diagnostic tests inspected; not executed here to avoid financial/approval operations |
| `tests/performance/foundry_single_call.py:236` `execute_stage` | Governed response → sets provider acceptance and application validation to failed pending acceptance, then invokes `validate_result` at line 280. No full digestion/reduction run is launched by this single-analysis path. | `test_validation_diagnostics.py:41` inspected |
| `documents/digestion/validation.py:64`; `codec.py:33` `decode` | Raw UTF-8 bytes → duplicate-key-safe JSON → `StageResult.model_validate`. Enforces raw bound, UUID/type/enum/text/token/extra-field structure. Decoding and Pydantic failures receive separate closed diagnostics. | Selected Attempt 3 tests; two-layer tests; diagnostics metadata/codec tests |
| `codec.py:13` `encode`; `validation.py:68–128` | Parsed model → canonical ASCII/default-expanded bytes, canonical byte check, stage/outcome/count checks, actual source resolution and allowed source/link sets. Encoding errors are `canonical_serialization`; stage failures `stage_binding`; source errors `evidence_validation`. | Canonical positive-control tests; synthetic full validator |
| `validation.py:130–197` claim loop | Per ordered claim: deterministic ID/origin, bounds, unique/member references, valid child links, fact source/status, qualification support. Identity and evidence failures are separately tagged. | Two-layer identity/evidence/qualification tests; synthetic controls |
| **`validation.py:198–203`** | **If `claim.subject is not None and claim.kind != 'fact'`, raise `DigestionError('inference_contract_error', diagnostic=CLAIM_CONTRACT, reason=SUBJECT_ON_NONFACT)`.** First boundary enforcing the relationship. | `test_live_failure_observability.py:205` subject case; `test_final_offline_azure_compatibility.py:313` commentary case; new temporary reproduction |
| `validation.py:204–224` | Only after the claim loop: analyzed-analysis source coverage, reduction child coverage and annotation text limits; return accepted result. The reported subject error does not certify these later checks passed historically. | Missing-evidence/coverage controls; synthetic positive control |
| `managed.py:86`; `workflow.py:23`; `foundry_single_call.py:286–320` | Domain error → `serialization_error / NON_RETRYABLE`; serialize only typed diagnostic/reason, stop guard and persist sanitized terminal outcome. | `test_validation_diagnostics.py:41`; existing audit privacy tests inspected; classifier exercised in reproduction |

The general durable workflow also uses this exact validator before checkpoint creation (`workflow.py:173–181`) and revalidates checkpoints before final digest construction (`workflow.py:153–166`). `ManagedSynthesisInference.analyze()` (`managed.py:222`) supplies bytes without repair in that workflow. The single-call launcher instead invokes governed execution and `validate_result()` directly. It would be inaccurate to describe Attempt 5 as a Kubernetes worker or a completed reduction/publication workflow.

From the reported predicate one can infer successful JSON/Pydantic decoding, canonical byte check, stage/outcome/count checks and real input-evidence resolution. Per-claim identity/evidence/qualification checks have passed **through the offending claim**, not necessarily for later claims. The offending subject is a non-null value accepted by the `Token` type. Its exact value, kind among the four alternatives, and downstream validity cannot be recovered from the diagnostic.

## 5. Claim-domain contract matrix

Actual model: [Claim](../../../documents/digestion/models.py#L209); shared [Token](../../../documents/jobs/models.py#L17); acceptance authority: [validate_result](../../../documents/digestion/validation.py#L198).

| Actual claim kind | Subject required | Non-null subject permitted | Non-null subject forbidden | Enforcing validator |
| --- | --- | --- | --- | --- |
| `fact` | No | Yes, valid `Token` only | No | Pydantic validates token; `validate_result:198` permits fact |
| `unknown` | No | No | Yes | `validate_result:198` |
| `unsupported` | No | No | Yes | `validate_result:198` |
| `commentary` | No | No | Yes | `validate_result:198` |
| `structural` | No | No | Yes | `validate_result:198` |

All five accept null. At the application model/validator boundary, an omitted subject defaults to `None`, so missing and explicit null have the same semantic result. **For generation, every field is required:** both generation and provider schemas reject a missing `subject`; the prompt requires explicit null/default fields. Application backward-compatible default expansion is intentional and is not schema-generation compliance.

`Token` is a string, length 1–128, matching `^[a-zA-Z0-9_./:-]+$`. Empty strings and whitespace are not substitutes for null. Non-null subjects must pass that independent lexical/type validation before the kind-dependent predicate. The reproduction confirms empty/whitespace strings yield `pydantic_validation / invalid_subject_token`, and integer subjects yield `pydantic_validation / invalid_field_type`. A populated valid token on a non-fact reaches `claim_contract / subject_on_nonfact`.

The predicate uses **claim.kind**, not result.kind, status, stance or iteration over a set. Claim order is the defined tuple order. It is identical across analysis and all reduction profiles. `stance` is `affirmed|denied|unknown`; `status` is `supported|unknown|unsupported`. There is no confidence field on Claim. No stance/status value grants a non-fact permission to carry a subject. Separately, a fact requires source support and `status='supported'` (`validation.py:180–185`). The implementation does not impose an additional unknown/unsupported kind-status pairing for non-facts; examples should not misdescribe such a pairing as an enforced invariant.

Malformed claim structure, enum, UUID, text/token type, missing required field or extra field is rejected by `codec.decode`/Pydantic before this predicate, with a content-free structural reason. A wrong deterministic UUID that is syntactically valid instead reaches `claim_identity`. A foreign syntactically valid evidence UUID reaches `evidence_validation`.

**VALIDATOR_CORRECT** within the established domain contract. Evidence of intent includes the explicit fact-only predicate, the matching earlier field audit, synthetic factual proposition fixtures (`documents/digestion/inference.py:65`), reducer commentary without subjects (`inference.py:77`), and the existing subject-on-commentary regressions. `inherited_summary()` and `make_digest()` (`validation.py:234,312`) use subjects and stances as structured proposition/conflict keys, not generic topics. Permitting subjects on commentary or unsupported findings would extend that authority without a domain justification. Those aggregation helpers assume previously validated results; their absence of a duplicate kind check is not an alternative acceptance path. No contradictory documented permission or reproducible validator defect was found. No new domain policy decision is required for the present rejection.

## 6. Active prompt audit

The active system text is built only by `ManagedSynthesisInference.render()` (`managed.py:181–202`). `StageProfile.template_version` and the planning binding both pin `managed-prompt/3` (`managed.py:55,141`). There are no subject examples or explicit claim-kind/subject conditions in its system prose. The full Claim schema in CONTROL lists enums and the subject string/null alternatives independently; its Python comment about propositions is not a JSON Schema field description.

| Domain requirement | Active prompt / CONTROL instruction | Validator enforcement | Alignment |
| --- | --- | --- | --- |
| Output object/closed fields | Exactly one JSON object matching schema, all fields/defaults/nulls/arrays; no prose (`185–187`) | `FrozenModel.extra='forbid'`, duplicate-safe decode, typed schema | ALIGNED |
| Claim kinds | Enum supplied in CONTROL.schema; unknown/unsupported conclusions explicitly use kind/status (`197`) | `Claim.kind` literal and separate status literal | ALIGNED for permitted names; no new pairing rule implied |
| Subject allowed only on fact | No conditional instruction; independent nullable subject schema | `validation.py:198` | **MISSING_IN_PROMPT** |
| Subject optional on facts | Schema shows null/string, token syntax/length; no explanation of proposition key versus topic | Pydantic token plus fact-only predicate | PARTIALLY_ALIGNED |
| Facts require supported status and source | “Cite ONLY allowed evidence IDs”; unknown/unsupported guidance, without explicit fact support conditional | `validation.py:180` | PARTIALLY_ALIGNED |
| Allowed evidence membership | Allowed IDs in CONTROL; never invent references (`195`) | Membership/resolution at `114–166` | ALIGNED |
| Deterministic claim IDs and origin | Supplied IDs consecutively; `originating_stage=stage_id` (`196`) | Exact positional `stable_id` and origin at `130–143` | ALIGNED |
| Unique evidence/links and nonempty qualification evidence | Shapes and allowed values supplied; uniqueness/nonempty constraints not fully explained | `155–197` | PARTIALLY_ALIGNED |
| Complete analyzed-analysis source coverage | Reference every allowed evidence ID across claims (`199`) | Union of evidence/contradicting arrays at `204`; qualification-only IDs do not satisfy coverage | PARTIALLY_ALIGNED |
| Unavailable analysis must have no claims and nonempty limitations | Unconditional analysis coverage instruction; schema independently permits outcome unavailable | `84–102` allows no-claim unavailable analysis; coverage is conditional on analyzed | **CONTRADICTORY for unavailable branch** |
| Reducer child coverage/retained qualifications/conflicts | Every child link; generated text is not source; preserve qualifications/conflicts (`200–201`) | Link coverage and immutable graph propagation | PARTIALLY_ALIGNED: copying a qualification is not always equivalent to lineage inheritance |
| Stage/task and no tools | Task-specific sentence, controlled kind/stage ID, untrusted data and no tools (`181–202`) | StageRequest material boundary, stage binding, no tool capability | ALIGNED |
| Text, byte and token limits | Concise claims; canonical ASCII/raw UTF-8 and separate token ceiling (`188–192`), dynamic limits | Decode, canonical check, per-claim/annotation bounds, provider finish/byte checks | ALIGNED |
| Confidence | No Claim confidence field or instruction | No Claim confidence policy | NOT_APPLICABLE |

A model following the independent schema fields and current prose can choose `kind='commentary'` and `subject='synthetic-topic'` without violating any explicit subject instruction. There is no instruction requiring populated subjects for all claims, nor a contradictory subject example: the specific subject problem is an **omitted conditional**, not a proven contradictory prompt sentence or required-subject rule.

The unavailable ambiguity is real and separately reproduced: a no-claim unavailable analysis with a nonempty limitation passes full validation but cannot cite every supplied source across claims. It is not evidence of the Attempt 5 cause: the observed subject predicate is inside a nonempty claim loop, after unavailable-with-claims would already have failed. Thus the offending historical result reached the analyzed branch. No unavailable wording change is bundled into the preferred subject fix.

## 7. Provider JSON Schema audit

`generation_schema()` starts from `StageResult.model_json_schema()` and recursively requires all properties. It does not add cross-field domain predicates. `provider_schema()` then copies that schema to the repository's deliberately narrow `azure-strict/1` subset. Four closed object definitions have 22 properties in total; all nested properties are required. Claim fields include `kind`, `subject`, `stance` and `status`, with no dependency between them.

The effective relevant fragments are:

```json
{
  "kind": {"type": "string", "enum": ["fact", "unknown", "unsupported", "commentary", "structural"]},
  "subject": {"anyOf": [{"type": "string"}, {"type": "null"}]}
}
```

This is a property fragment, not a complete claim or the historical output. There is one shared Claim shape referenced by the claims array, not kind-specific object alternatives. `additionalProperties=false` rejects unknown keys throughout. Required-and-nullable `subject` allows explicit null but not omission at the provider boundary.

The converter strips `title`, `default`, UUID `format`, and string length/pattern constraints; converts `const` to singleton enum; and retains allowed descriptions if present (`azure_schema.py:20–43`). There is no Claim.subject field description establishing fact-only semantics. More importantly, the conditional is absent even from the pre-conversion schema; removing string constraints did not introduce this cross-field gap.

| Validation layer | What it establishes | What it does not establish |
| --- | --- | --- |
| Syntactic JSON | Decodable object/content; application separately rejects duplicate keys | Types, evidence authority, domain consistency |
| Provider JSON Schema | Closed structural shapes, required fields, enums, nullable alternatives | Subject-kind coupling, token lexical bounds, supplied IDs or provenance |
| Pydantic | UUID/type/enum/text/token constraints, defaults, forbidden extras | This fact-only subject predicate, deterministic positional identity or source membership |
| Domain contract | Stage/outcome/claim count/fact-support/subject restrictions | Natural-language entailment or model truthfulness |
| Evidence lineage/coverage | Exact source resolution, allowed references, inherited links and complete structural coverage | Semantic entailment from prose alone |
| Deterministic identity | `stable_id(stage_id, position)`, unique IDs, correct origin | Factuality of generated text |

The last three are interleaved within `validate_result`, rather than separate wholesale passes. Structural “strict” does not mean these application-owned predicates have been moved into Azure.

Repository compatibility rules: nested `anyOf` with recursively supported branches is allowed; root `anyOf` is rejected. `if/then/else`, `allOf`, `oneOf`, discriminator and unknown keywords are outside the converter's allowlist. Local refs must resolve, recursion is rejected, all object properties are required, object boundaries are closed, total properties ≤100 and container depth ≤5 (`azure_schema.py:17–115`). Do not propose a generic conditional keyword as immediately usable.

A future schema option could use a nested `anyOf` of two closed Claim object variants: `kind='fact'` with nullable-token subject, and the other four kinds with `subject` restricted to null. This uses constructs recognized locally in principle, but the **exact transformed schema, reference structure, depth/property budget and Azure deployment compatibility remain unverified**. No alternative schema was submitted or activated. Existing [two-layer engineering guidance](../../engineering/llm_structured_output_validation.md) documents the deliberately narrow subset and warns that local JSON Schema validation is not deployment acceptance. This task did not browse or contact Azure to refresh those historical compatibility findings.

## 8. Offline reproduction

Temporary driver: `/tmp/polymind_attempt5_diagnostics.py`. Evidence directory: `/tmp/polymind-attempt5-post-diagnostics/`. These are disposable synthetic artifacts outside the repository, not launch helpers or historical audit artifacts.

The driver installs the inspected existing `/tmp/polymind_e2e_offline_guard.py` before application imports. It denies Python socket connection/send/DNS operations and registers an audit hook that also counts swallowed attempts. Application/credential environment is cleared, implicit application dotenv is suppressed with the existing test isolation helper, bytecode writes are disabled, and no provider factory, authority constructor, RunGuard or governance ledger is used in the reproduction. A stub supplies only provider name/model ID; its `execute` raises unconditionally and is never called. This is Python-level denial, not a claim of an OS firewall.

Fixture construction uses new ASCII synthetic text, `extract(BytesIO(...))`, temporary `LocalObjectStore`, synthetic scope/document UUIDs, real `build_plan()`, and a real analysis `StageRequest`. There is one real evidence piece, verified by `EvidenceIndex.resolve`. The existing small planning profile is bound to the public Attempt 5 managed settings, retaining 3,000 completion tokens and 10,000 raw/canonical bytes. Request rendering runs without execution. No Attempt 5 source document or response is reused.

The essential claim construction is:

```python
claim = Claim(
    claim_id=stable_id(str(request.stage_id), '0'),
    originating_stage=request.stage_id,
    text='Synthetic observation.', kind='commentary',
    evidence_ids=tuple(p.evidence_id() for p in request.source_data),
)
payload = StageResult(stage_id=request.stage_id, kind='analysis', claims=(claim,)).model_dump(mode='json')
payload['claims'][0]['subject'] = 'synthetic-topic'
# Both generation_schema() and provider_schema(...) accept this payload.
# StageResult.model_validate(payload) accepts it.
validate_result(json.dumps(payload).encode(), request, index)
# Raises inference_contract_error / claim_contract / subject_on_nonfact.
```

`classify_managed` gives `serialization_error / NON_RETRYABLE`. The positive control changes **only** `subject` to null, then passes the **entire** validator, including source coverage. Identity, source membership, bounds and all other values are retained. Deleting subject instead also passes application acceptance via its default, but fails both generation schemas; explicit null is the correct generated representation.

| Synthetic cases | Observed result |
| --- | --- |
| Five kinds × explicit null | All five pass both schemas, Pydantic and full validation |
| Five kinds × populated valid-token subject | Fact fully accepted; four non-facts pass schemas/Pydantic and fail exact subject predicate |
| Five kinds × missing subject | Pydantic/full application acceptance; both generation schemas reject missing required property |
| Five kinds × empty string or whitespace | Provider schema accepts; generation schema/Pydantic reject; `invalid_subject_token` |
| Five kinds × integer subject | Both schemas/Pydantic reject; `invalid_field_type` |
| Mixed factual/non-factual claims | Fully accepted with null non-fact subject; changing only second claim's subject produces `subject_on_nonfact` |
| Empty unavailable analysis plus limitation | Both schemas/Pydantic and full validation accept; distinct from analyzed empty claims |
| Foreign evidence | `evidence_validation / foreign_evidence`, public `invalid_reference` |
| Fact with unsupported status; fact without source | Both reject as `evidence_validation / unsupported_fact` |
| Wrong deterministic claim ID | `claim_identity / claim_id_mismatch`, public `serialization_error` |
| Missing analyzed source coverage | `coverage_validation / missing_source_coverage`, public `extraction_failed` |
| Prohibited extra claim field | Both schemas reject; `pydantic_validation / forbidden_extra_field` |

Total: **39 cases**, expected assertions all passed. Thirteen were fully application-accepted controls; 26 were expected rejections. Five rejections reached the exact subject reason: four single-kind cases and the mixed case. Synthetic data proves the acceptance boundary, not the historical output contents or a model's reasoning.

Executed with the existing Python 3.10.13 project interpreter:

```text
python -B /tmp/polymind_attempt5_diagnostics.py snapshot
python -B /tmp/polymind_attempt5_diagnostics.py bindings
python -B /tmp/polymind_attempt5_diagnostics.py repro
python -B /tmp/polymind_attempt5_diagnostics.py tests
python -B /tmp/polymind_attempt5_diagnostics.py preservation
```

Bindings and reproduction each exited 0 with **network attempts 0**. Synthetic assertions, schema/Pydantic decisions and sanitized categories are saved in `reproduction.json`; bindings in `bindings.json`; pure pricing arithmetic in `arithmetic.json`. No full prompt or model/document evidence appears in these saved summaries.

Selected existing tests ran through an external working directory, explicit repository `pytest.ini`, external basetemp/cache/JUnit paths, disabled automatic plugin loading, precollection network guard and a public tests symlink. The exact selector list and invocation are in `test-command.json`; results in `focused.log`/`focused.xml`.

| Existing module | Executed selection | Passed |
| --- | --- | ---: |
| `tests/unit/documents/test_two_layer_output.py` | Schema conversion, unsupported constructs/complexity, two validation layers, strict wire format, single fake-call failure/usage preservation | 38 |
| `tests/unit/documents/test_managed_inference.py` | Generation defaults/version exposure and bounded complete-result control only | 2 |
| `tests/integration/test_attempt3_serialization.py` | Independent structural violations, canonical positive control and malformed/duplicate JSON only | 6 |
| `tests/unit/test_single_call_diagnostics.py` | Closed bounded provider rejection diagnostics and malformed rejection privacy | 21 |
| `tests/integration/test_live_failure_observability.py` | Safe/unsafe paths, deterministic Pydantic priority, unknown/saturated counts, codec, truncation, provider metadata and forged metadata | 44 |
| **Total** | **No failures, errors, skips or warnings; 1.51 seconds** | **111** |

The test guard observed **0 network attempts**. Selected tests may create disposable synthetic admission databases under basetemp; they do not create/consume approvals or construct financial ledgers. Fake HTTP interactions are local method calls, not provider calls.

Existing subject-specific tests were also located: `test_live_failure_observability.py:205`, `test_final_offline_azure_compatibility.py:313,329,349`, and governed audit mapping in `test_validation_diagnostics.py:41`. Their shared fixtures run broader governed workflows or financial harnesses; those fixture-dependent tests were **inspected, not run**. The separate reproduction exercises the actual subject predicate without those mutations. Historical 1,755 full-suite and 426 readiness passing results remain historical; neither suite was rerun. No new repository tests were added.

## 9. Root-cause analysis

| Candidate cause | Classification | Evidence and limits |
| --- | --- | --- |
| Prompt omits nonfact-subject restriction | **CONFIRMED** | Active `render:185–202` has no conditional; explicit domain rule at `validation:198` |
| Prompt contradicts fact-only subject policy | **NOT_SUPPORTED** | Independent schema alternatives and absent guidance, not a command to populate every subject |
| Provider schema admits prohibited combination | **CONFIRMED** | Both generated schemas accept all four synthetic non-fact/populated-subject cases |
| Missing prompt rule caused this particular model choice | **SUPPORTED_HYPOTHESIS** | Contract gap demonstrably permits it; no raw response or internal model reasoning establishes behavioral causality |
| Azure failed to honor its schema | **NOT_SUPPORTED** | The observed failure is permitted by the schema; no historical response was available to this investigation for independent schema replay |
| Application subject validator is incorrect | **RULED_OUT within established contract** | Exact intentional predicate, prior documentation and fixtures agree; positive controls pass |
| Diagnostic mapped to wrong domain predicate | **RULED_OUT** | Exact typed enum at predicate; synthetic classifier reproduces reported tuple |
| Output truncated / response-size breach | **RULED_OUT as observed failure** | `stop`, 1,852 <3,000 and 4,395 <10,000; canonical size check precedes the reported domain predicate |
| Invalid deterministic claim identity caused failure | **NOT_SUPPORTED** | Actual reason is subject contract. Identity checks passed through offending claim; later claims remain unexamined historically |
| Evidence lineage caused failure | **NOT_SUPPORTED** | Exact input-evidence and relevant per-claim checks precede the subject reason. Later checks/claims could still fail independently |
| Accounting failed | **RULED_OUT for supplied Attempt 5 outcome** | One SETTLED row, exact actual-cost arithmetic, accounting_failed false |
| Transport failure caused rejection | **RULED_OUT** | Completed provider response, usage and domain-specific application reason |
| Provider-specific structured-output defect/limitation caused subject failure | **NOT_SUPPORTED** | Same bad combination passes pre-conversion schema and Pydantic; gap is provider-neutral. Known stripped string constraints are a separate intentional boundary |
| Additional unseen generated errors | **UNKNOWN** | Fail-fast subject diagnostic does not enumerate the complete historical response |

The **earliest demonstrable misalignment** is the generation contract's projection of independently typed Claim fields without the application-owned subject-kind invariant, compounded by omitted explanatory prompt prose. Azure schema conversion preserves that pre-existing gap. The final exception is correct enforcement, and `serialization_error` is the legacy public classification, not proof that JSON serialization itself failed.

## 10. Diagnostic quality

The pipeline now distinguishes transport (`provider_unreachable` → `inference_unavailable`), timeout, authentication/configuration, strict-schema request rejection (`provider_acceptance='schema_rejected'` plus closed rejection reason), output limits (`inference_output_limit` and bounded metadata), JSON decoding, duplicate keys, Pydantic structure, canonical encoding/revalidation, stage binding, claim identity, claim contract, evidence and coverage. Sources: `managed.py:86–107`, `workflow.py:23–32`, `diagnostics.py:11–49`, `codec.py:13–73`, and `foundry_single_call.py:286–304`.

The subject exception carries only fixed category/enum values. The launcher persists supplemental diagnostics only while application validation is failed and only for exact approved diagnostic types. Pydantic failures separately use an allowlisted field path, bounded indices, saturated error count and deterministic priority; extra-field names/values are discarded (`diagnostics.py:64–191`). Subject-domain errors currently do not carry that Pydantic record. No arbitrary exception message, raw subject, claim text or evidence is needed to reach this diagnosis.

Current telemetry is sufficient to select the responsible domain rule and exclude observed output/transport/accounting failures. It cannot enumerate hidden later failures or identify the exact offending claim. Additional telemetry is **optional**, not part of the minimal fix:

| Possible field | Data-minimization assessment |
| --- | --- |
| Fixed validation stage/reason | Already present; retain |
| Static `claims.*.subject` path | Low additional disclosure if application-owned and allowlisted; useful but largely redundant with reason |
| Claim index | Could be bounded 0–63, but reveals ordering/cardinality; restrict to existing private audit retention/access policy and require demonstrated debugging need |
| Claim kind identifier | Finite application enum, never arbitrary content; nevertheless reveals document-classification information, so not necessary for the immediate fix |
| Number of rejected claims | Current validator stops at first failure. Do not invent a count or introduce a second scan solely for telemetry; any future count must state its scope and saturation |
| Prohibited field present/non-null | Fixed boolean can be derived from this reason. Distinguish presence from non-null, since null is schema-required and valid; recording the value is unnecessary |

No proposal includes raw claim/source/reasoning text, actual subject tokens, evidence identifiers, operator identity or credentials. Any additive audit change needs its own closed-type/privacy tests and review under existing retention/storage decisions, not a new logging platform.

## 11. Financial and governance reconciliation

Public catalog rates supplied by the operator: EUR `0.659978880676` input and `3.959873284055` output per 1,000,000 tokens. Pure `Price.cost()` (`governance/ledger.py:48`) and independent Decimal arithmetic yield:

```text
input:   2342 × 0.659978880676 / 1,000,000 = 0.001545670538543192
output:  1852 × 3.959873284055 / 1,000,000 = 0.007333685322069860
total EUR                                      0.008879355860613052
```

This matches reported `actual_cost` exactly. The 320 reasoning tokens are already included in the 1,852 completion tokens; neither `_usage()`/metadata handling (`openai_compatible.py:231,429–456`) nor settlement (`ledger.py:262–280`) adds reasoning again. Total 4,194 is an integrity check, not another priced class.

`cost` is the original **pre-call reservation amount**, calculated from conservative rendered-input estimate and reserved output tokens (`GovernedExecution:26–30`, `ledger.reserve:210,246–248`). It is retained as historical reservation evidence when `settle()` writes `actual_input`, `actual_output`, `actual_cost` and terminal state. It is not an additional debit, provider invoice or duplicate charge. Budget aggregation uses `actual_cost` for settled rows and `cost` for unsettled rows (`ledger.py:228–241,290–299`).

The supplied `cost=0.019075369588175428` exactly equals the public rates applied to **10,903 estimated input + 3,000 reserved output**. That estimate is inferred algebraically assuming the configured 3,000 reservation; the row's original `input` field was not supplied or independently inspected. It is compatible with source semantics. The run's broader 25,000-input safety envelope is distinct from the actual rendered-input governance reservation; at 25,000/3,000 the catalog envelope is EUR `0.028379091869065`.

Settlement runs in `GovernedExecution.execute()`'s `finally` before `execute_stage()` validates StageResult. Thus provider success/usage settlement and application rejection can correctly coexist. The one-call guard inserts a durable attempt at admission (`foundry_budget.py:103–134`), finishes it with known bounded usage (`136–160`), and checks cumulative attempts; the application failure subsequently stops the guard (`foundry_single_call.py:306`). The supplied one run/one governance row agrees with this path. No replay or second attempt is implied.

**Accounting path sound within supplied evidence.** A SETTLED record has no outstanding/UNKNOWN obligation for that Attempt 5 row. `accounting_failed=false` alone would not prove that; terminal state and measured usage do. This report does not independently certify tenant-wide obligations or current balances, since no protected financial database was opened. It does not reopen commercial authorization, historical cleanup failures, rates, allowances or Azure billing. No ledger was mutated.

## 12. Remediation alternatives

**A — Versioned prompt clarification.** Explicitly express the demonstrated missing condition using actual enum values; distinguish null from blank/omitted output; facts may omit semantic subject by emitting null. Retain fact source/status rules, deterministic IDs and all evidence safeguards. This addresses confirmed missing guidance without pretending model compliance is guaranteed. It changes source/configuration bindings. The existing inactive M1 proposal is useful design evidence, but its broader M1/M2/M3 patch must not be silently applied as the subject fix.

**B — Kind-specific provider schema alternatives.** Could prevent this specific combination structurally, but exact Azure and provider portability validation is unverified. Keep every field required in each closed branch, non-fact subjects null, facts nullable; retain downstream validation and token constraints. Do not introduce unsupported `if/then`, `oneOf` or a discriminator. This changes schema and source fingerprints, grows regression scope and still cannot enforce evidence/identity dynamically. Defer pending a separately scoped compatibility review.

**C — Validator correction.** Not justified. No independent semantic evidence permits non-fact subjects. Relaxing the predicate would change proposition authority and contradict the established contract. Preserve the validator.

**D — Controlled normalization.** Reject automatic subject deletion, conversion of kind to fact, or rewriting claims. Positional IDs are independent of subject text, so deletion need not change the UUID arithmetic, but it changes accepted content/meaning and artifact hashes, can erase intended proposition information, and masks generation errors. Reclassifying as fact also changes source/status obligations. Evidence membership remaining unchanged would not prove semantic equivalence. Any future normalization policy would require an explicit domain decision, immutable original/provenance, versioned hashes and financial/security review; none is warranted here.

**E — Separate classification and detailed generation.** Potentially useful only as an architectural hypothesis. It adds calls/stages, new intermediate contracts and spend/approval bindings without demonstrated necessity. Out of scope for the immediate fix; no new orchestration, dependency or inference experiment proposed.

| Criterion | A: prompt | B: schema alternatives | C: relax validator | D: drop/normalize subject | E: extra generation stage |
| --- | --- | --- | --- | --- | --- |
| Addresses confirmed cause | Yes: missing guidance | Yes: admitted combination, if compatible | No | No: hides violation | Unknown |
| Preserves domain semantics | Yes | Yes if equivalent branches | No | Not demonstrated | Unknown |
| Preserves evidence integrity | Yes | Yes with original validation | Not assured | Membership alone insufficient | Needs new proof |
| Preserves deterministic IDs | Yes | Yes | UUID formula can remain, policy changes | UUID formula can remain, content/provenance change | Needs new bindings |
| Azure structured-output compatibility | Confirmed existing schema unchanged; new response behavior unverified | Unverified exact proposed shape | Existing schema unchanged | Existing schema unchanged | Unverified |
| Provider-neutral compatibility risk | Low | Medium | High domain-contract risk | High content/audit risk | High |
| Complexity | Low | Medium | Low code, unjustified policy change | Medium if audited | High |
| Regression scope | Small focused change | Medium | Large semantic review | Large | Large |
| Affects source fingerprints | Yes | Yes | Yes | Yes | Yes |
| New live authorization if used | Yes | Yes | Yes | Yes | Yes, including changed spend/call contract |

Preferred ranking: **A first**, B only after separate evidence, E deferred; C and D rejected for this failure. No implementation or paid verification is part of this recommendation.

## 13. Preferred minimal correction

Proposed new instruction, adjacent to the existing kind/status sentence:

```text
Only kind="fact" may have a non-null subject. For kind="unknown", "unsupported",
"commentary", or "structural", include subject=null. Never use an empty or blank
string instead of null. For a fact, subject may also be null; a populated subject
must be 1–128 characters matching ^[a-zA-Z0-9_./:-]+$ and identifies a structured
proposition, not a general topic. Do not change a claim's kind to fact to retain
a subject. Facts still require supported status and authorized source support.
```

A concise field-pair example `kind="commentary", subject=null` is sufficient; avoid a lengthy competing StageResult example. The existing field-complete schema, claim ordering, origin, source coverage and unsupported/unknown representation remain in force. Do not add new enforced non-fact kind/status pairings or infer prose truthfulness.

For a separately authorized patch, version `StageProfile.template_version`, the adapter's `profile()` prompt binding and renderer wording together as `managed-prompt/4`. Preserve the version-3 text/source evidence and frozen historical fixtures; never change wording while claiming it is still version 3. A deliberate active-version migration can reject stale generation configurations while leaving stored `stage-result/1` artifacts readable. If simultaneous version-3 execution compatibility is required, retain an explicit version-selected old renderer rather than relabeling it; that compatibility requirement must be specified before implementation. Reusing Attempt 5 execution is forbidden in either design.

This is a generation-only correction. `Claim`, `StageResult`, `validate_result`, `azure-strict/1`, provider transport, governance, approval/replay semantics, byte/token caps and financial policy should remain unchanged. The unrelated unavailable/qualification wording issues remain separately documented; do not bundle the inactive broader proposal automatically.

## 14. Regression-test plan

Add focused parameterized cases to existing relevant modules rather than a new fixture framework. Use real synthetic extraction/evidence/IDs with pre-import network denial and temporary storage, like this reproduction. No repeated Azure calls are a primary test mechanism.

1. All four non-fact kinds with a populated valid-token subject still reject with `claim_contract / subject_on_nonfact`; null controls pass full validation. Exercise all stance/status enum choices to prove they do not authorize non-fact subjects.
2. Facts with a valid token and facts with null pass with authorized source and supported status; unsupported/source-free facts retain their existing evidence rejection.
3. Missing subjects remain application-default-compatible but generation-schema-invalid; blank/whitespace/invalid-token and wrong-type subjects keep their earlier Pydantic reasons. Do not normalize them.
4. Render all four profiles and assert the exact new instruction, version/profile coherence, explicit null/default instructions, deterministic output IDs, untrusted-data separation and absence of tools. Assert no non-fact subjects are encouraged by an example.
5. Preserve the current two-layer schema contract and schema fingerprint for a prompt-only fix. Explicitly retain a synthetic provider-schema-valid/domain-invalid non-fact witness; a test must not falsely assert the schema now enforces the rule. Any later schema-branch correction requires its own supported-subset tests and portability review.
6. Preserve deterministic positional identity: wrong ID, duplicate ID, wrong origin, changed order and malformed UUID reject through their existing layers. No application-generated repair or model reclassification is introduced.
7. Preserve exact source membership, input resolution, full analyzed coverage, unique citations, child links and qualification lineage; positive synthetic multi-claim analysis must pass all of `validate_result`.
8. Reject prohibited extra fields at all closed boundaries, including null-valued extras. Confirm byte/default/canonical encoding controls still apply.
9. Keep sanitized classifier/audit outputs fixed and content-free. Confirm subject values, text, source evidence, raw model output and arbitrary exception messages never reach diagnostics. If new safe metadata is separately approved, test its allowlist/bounds.
10. Retain one-attempt/no-retry/no-fallback behavior using a local counting fake only; do not invoke a launcher consuming an approval. Existing governed regressions may be reviewed/run in a separately authorized implementation task using disposable synthetic authority state, never Attempt 5 state.
11. Preserve immutable historical prompt/request fixtures and add separately reviewed version-4 expectations; do not overwrite old hashes merely to make tests green. Verify unchanged domain-source and acceptance-order fixtures independently.
12. Recompute all affected bindings and rendered-request/fixture/profile hashes offline before any new operator review; verify stale bindings fail closed. Do not reuse historical checkpoints under a new generation profile.

Expected result: direct positive StageResult acceptance and precise negative diagnostics offline, with unchanged schema/domain policy. These tests establish correctness of the proposed contract, not future model acceptance probability.

## 15. Attempt 6 readiness

**NO-GO now.** The authorized diagnostic is complete; the recommended correction has intentionally not been applied or validated as an implementation. No new generation fingerprint, private configuration, execution window or independent approval was produced.

Proposed change boundaries for a future authorized implementation:

| File / component | Proposed change and tests | Fingerprint impact / compatibility / preserved behavior |
| --- | --- | --- |
| `documents/digestion/managed.py` — `StageProfile`, `ManagedSynthesisInference.profile/render` | New version-4 subject wording and coherent active version binding; preserve immutable v3 evidence. Add four-profile instruction and full synthetic subject-contract controls in managed tests. | Executor and generation-source hashes change; inference settings binding changes. Provider schema does not. Generation-version compatibility changes explicitly; stored StageResult remains unchanged. |
| `tests/unit/documents/test_managed_inference.py` | Add subject matrix, positive full validation and new-version prompt assertions, preserving v3 expectations as historical fixtures. | Not in executor/generation source hash inventories; test-only. Existing evidence/identity/limits remain enforced. |
| `tests/unit/documents/test_two_layer_output.py` | Add explicit subject-gap witness and maintain exact structural schema expectations. | No direct source binding change; schema fingerprint must remain identical for prompt-only correction. |
| `tests/integration/test_live_failure_observability.py` | Add/update version-specific renderer/source witnesses while retaining historical constants; keep domain predicate/order comparison unchanged. | Test-only; do not refresh historical `MANAGED_SOURCE_SHA`/`FROZEN_REQUESTS` in place as a substitute for reviewed new-version fixtures. |
| `tests/integration/test_final_offline_azure_compatibility.py` | Make active version expectation intentional and keep separate historical request witness; preserve provider/domain distinction and zero-claim semantics. | Test-only; existing strict wire schema, lineage and domain policy retained. |
| `tests/integration/test_foundry_l1_launcher.py`, `tests/integration/test_output_limit_hardening.py` | Existing literal prompt-version consumers need explicit version-aware expectation migration if the active default changes. | Test-only; preserve launch guards and limits. |
| `docs/engineering/llm_structured_output_validation.md` and a new implementation phase report | Document implemented version/rule, unchanged validation/schema boundary and binding consequences after implementation. | Documentation-only; no binding change. Historical reports/proposals remain unmodified. |

No change is needed to `models.py`, `validation.py`, `diagnostics.py`, `codec.py`, `azure_schema.py`, `openai_compatible.py`, financial/authentication code, manifests or dependencies for the preferred fix. `tests/performance/foundry_single_call.py:186` already derives profiles from `StageProfile`; it need not change for an intentional global active-default version migration. If version 4 is opt-in instead, `prepare_analysis` must explicitly select it, a separate small reviewed composition change. Do not silently rely on the old default.

| Binding | Preferred prompt-only migration |
| --- | --- |
| `executor_sha256` | **Changes**: its transitive inventory includes `managed.py` |
| `generation_contract_sha256` | **Changes**: explicit inventory includes `managed.py` |
| `provider_schema_sha256` | **Unchanged**: generation/model schema and converter unchanged |
| Inference configuration digest (`ManagedSynthesisInference.config`) | **Changes**: template version is serialized in managed stage settings |
| Complete private configuration digest | **Changes** when new source/settings/request bindings are prepared |
| Planning profile / stage IDs / rendered request hash | Must be recomputed; inference configuration and prompt/profile bindings change |

Engineering GO requires separate implementation authorization, reviewed versioning/compatibility choice, focused offline tests and self-review, reviewed new bindings and updated documentation. Paid execution additionally requires fresh actual-scope preparation/configuration, valid current operator/credential/capacity/financial evidence, a fresh independent signed approval for `polymind-single-analysis-live` and a new execution window under the existing 600-second margin and other lifetime gates. Existing runbook: [single-analysis timing and preparation](../../evaluation/phase_17hl_operator_approval.md#single-analysis-timing-and-preparation-handoff). No extra call budget, retry or fallback is proposed.

Attempt 5's consumed approval, replay markers, outcome and settlement are immutable. A new signature/configuration never authorizes resetting those records. Do not reuse its approval for Attempt 6 even if a schema fingerprint remains unchanged. Any future live task requires explicit fresh authorization; this report supplies none.

## 16. Unresolved questions

1. The actual non-fact kind, subject, position and number of historical violations remain unknown; the sanitized reason intentionally does not identify them. No raw output was examined, and absence of retained output was not asserted. These details are unnecessary to locate the confirmed contract gap.
2. Attempt 4's exact predicate remains unknown; do not assume subject recurrence. For Attempt 3, the retained report's evidence-UUID diagnosis is more specific than the task's broad claim-identity description; no private historical reinspection was needed or performed here.
3. A clarified prompt's real-model compliance rate is unknown. Offline correctness cannot certify future acceptance; any future paid experiment needs fresh independent authorization.
4. Exact kind-specific union schema compatibility on this Azure deployment and across supported providers is unverified. No such schema change is needed for the recommended minimal action.
5. If simultaneous execution support for old prompt configurations is a product requirement, choose explicit version-selected rendering before implementation. Historical readability/immutability and rejection of stale approvals remain mandatory either way.

The separate unavailable-coverage and qualification-inheritance instruction ambiguities are established findings already documented, not unanswered causes of this subject failure. Tenant-wide current balances and Azure invoice attribution were outside this narrow task and were not re-investigated.

## 17. Repository state and safety declaration

Read `AGENTS.md` first; inspected relevant source, consumers, existing tests, requested preparation reports, earlier failure diagnoses, two-layer guidance and inactive proposal. Read-only shell work used `rg`, `nl`, `sed`, `cat`, Git status/diff, and narrowly targeted temporary helper reads. Python actions were the five driver modes above, JUnit result aggregation and pure Decimal reconciliation. No historical authentication, private launch configuration, raw response, signing key or authority database was opened.

Validation newly executed: four authoritative fingerprints **match**; **39 synthetic assertions pass**; **111 selected existing tests pass**, zero failures/errors/skips/warnings, zero observed network attempts. The historical 1,755/426 baselines were not rerun. No production compilation/build/deployment was needed for this report-only change; full pytest, compileall, Docker and Kubernetes checks were deliberately not run.

Self-review checked fail-fast order, same-predicate positive/negative controls, omitted/null distinction, schema-before-conversion gap, provider-versus-domain success, existing consumers, exact source-binding coverage, and settlement ordering/arithmetic. Separate pre-commit review checked only this new report for secrets, operator PII, source/document/model text, credentials/JWS values, accidental code changes, misleading claims and broken local file links. Temporary scripts/fixtures/results remain outside the checkout.

Starting public-file inventory contains **404 pre-existing tracked/untracked files**. Content SHA-256, mode and modification time are preserved for every inventoried file; the sole allowed addition is this report. No pre-existing tracked modification or untracked artifact was replaced. Protected state was not independently snapshotted or reread: preservation rests on never opening its paths or executing its mutating APIs, not a claimed comparison of inaccessible private records.

Final checks: `git diff --check` passes; report-specific whitespace/local-link/sensitive-marker review passes; public-file preservation reports **404 compared, changed 0, unexpected additions 0** (the report is explicitly excluded). `git status --short --branch` retains the dirty `master...origin/master` baseline: **20 modified tracked files, 121 pre-existing untracked files plus this one new report, zero staged changes**. `git diff --stat` remains **20 files changed, 832 insertions(+), 79 deletions(-)**, all pre-existing; Git's tracked diff statistic excludes this untracked report.

Safety totals for this investigation: external provider calls **0**; Azure/cloud/authentication operations **0**; deployments/containers/clusters started **0**; approvals created/signed/consumed **0**; protected auth/trust/replay/audit/outcome writes **0**; governance/financial mutations **0**; production/existing test modifications **0**; commits/pushes/staging **0**. Only `docs/codex/reports/phase_17hl_attempt5_post_execution_diagnostics.md` was added to the repository.
