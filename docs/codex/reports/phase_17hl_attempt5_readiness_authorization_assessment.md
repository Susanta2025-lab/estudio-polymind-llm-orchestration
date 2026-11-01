# Phase 17H–L — Attempt 5 readiness and authorization assessment

Assessment date: 23 October 2026. Scope: independent, offline assessment of the
actual local working tree. [Preserved prompt](../prompts/phase_17hl_attempt5_readiness_authorization_assessment.md).

## A. Executive summary

**Technical readiness: NO-GO. Execution authorized now: NOT VERIFIED.**

There is **one confirmed engineering blocker**, F1: HTTP response cleanup can
replace an existing normalized inference failure, removing its diagnostic category
from the final audit. Four controlled comparisons using the real
`requests.Response` class reproduce this, including loss of `inference_output_limit`.
The run still stops after one attempted request and retains an UNKNOWN financial
obligation. This is a diagnostic reliability defect, not evidence of extra spending,
evidence bypass or leaked content. It fails this assessment's explicit requirement
that cleanup preserve the primary failure. No production correction was made.

The remaining principal mechanisms pass offline assessment: strict payload and
schema construction, preserved generation contract, detailed sanitized domain
reasons, actual-attempt containment, governance settlement, approval verification
and replay prevention. The complete current regression passed **1,678 tests**,
with **0 failures, 0 errors, 0 skips, 42 existing warnings and 0 observed network
attempts**. That green suite does not cover F1's response-close failure combination.

There are **seven grouped external verification conditions**, C1–C7 in section J.
They cover deployment, commercial rates, budget/authority state, operator approval,
credentials/time, shared capacity and the actual private execution configuration.
None was established by reading protected artifacts or contacting Azure.

The proposed experiment remains one first-chunk analysis of the existing fixed
four-page diagnostic fixture. It does not authorize reductions, whole-document
digestion, publication, Q&A or deployment. **Attempt 5 was not executed. Phase 17H
remains PARTIAL.** Resolve F1 in a separately scoped offline correction, then
reassess the changed fingerprints before requesting a fresh operator authorization.
External attestations alone cannot resolve the current engineering NO-GO.

## B. Current code and configuration

### Repository and evidence boundaries

Branch: `master`, tracking `origin/master`. HEAD:
`af4a7a076c918ef13aea05d74bf239c0af909133`.
Initial complete porcelain inventory: **20 modified tracked files and 109 untracked
files**, with no staged files. Initial tracked `git diff --stat`:
**20 files changed, 812 insertions(+), 76 deletions(-)**. This assessment creates
only its prompt and report; those additions are not included in tracked diff stats.
The prior work was inspected in place, without restoring or replacing it.

All eight requested reports were present and reviewed:

| Report | How its evidence was used |
|---|---|
| [Final offline Azure compatibility audit](phase_17hl_final_offline_azure_compatibility_audit.md) | Contract derivation, structural/local validation distinction, witnesses, nesting limits and historical evidence boundary |
| [Live-failure observability and contract options](phase_17hl_live_failure_observability_and_contract_options.md) | Current reason taxonomy, metadata propagation, frozen representations, source changes and inactive proposals |
| [AST portability correction](phase_17hl_ast_test_portability_fix.md) | Fixture provenance, lexical comparison exclusions, 1,678-test baseline and interpreter limits |
| [Full-suite configuration isolation](phase_17hl_full_suite_configuration_isolation.md) | Pre-collection settings isolation, explicit configuration semantics and historical 64-case reconciliation |
| [Offline E2E verification](phase_17hl_offline_e2e_contract_verification.md) | Durable checkpoint/evidence/lineage, CLI and financial assertions; distinct four-call full workflow |
| [Diagnostic hardening](phase_17hl_diagnostic_hardening.md) | Original diagnostic stages and first-rejection ordering |
| [Regression reconciliation](phase_17hl_regression_reconciliation.md) | Historical fixture failures, stale helper guard and corrected accounting expectations |
| [Single-call execution failure diagnosis](phase_17hl_single_call_execution_failure_diagnosis.md) | Historical pre-provider launch/timing uncertainty, not the later Attempt 4 rejection predicate |

The public strict-schema preparation report was also cross-checked. It establishes
preparation values, not what was actually submitted in Attempt 4. No separate
locally named independent code-review report was found; the independent compatibility
audit's findings above were used. No absent report is treated as evidence.

Current inspection covered all requested digestion, provider, harness, financial
and test files, `tests/source_contracts.py` and both fixed source fixtures, plus
`foundry_recalibration.py`, `foundry_schema_probe.py`, `foundry_schema_diagnostics.py`,
`security/identity.py`, `security/runtime.py`, relevant `SecurityAuthority` checks,
and the public evaluation/governance/security documentation and templates.
Protected approvals, trust values, private keys, credentials, real dotenv files,
operator financial databases and retained private responses were not opened.

### Effective configuration derived from the single-call source

These are current code-enforced/preparation settings, **not verification of an
existing private launch packet or current Azure resource properties**.

| Setting | Current local value / evidence |
|---|---|
| Intended region | Spain Central (`spaincentral`) in public reviewed financial fixture/history; actual region NOT VERIFIED. The configuration's contract region is a signed string, not a fixed region Literal. |
| Resource | `epolymind-foundry-dev-susanta` |
| Deployment | `epolymind-gpt-54-mini`, both general and summarization role mappings |
| Model / version / SKU | `gpt-5.4-mini` / `2026-03-17` / `GlobalStandard` configuration Literals |
| API | Azure OpenAI v1 Chat Completions, `/openai/v1/chat/completions` |
| Generation / inference / prompt | `managed-generation/2` / `managed/1` / `managed-prompt/3` |
| Explicit capability | `gpt54mini-30k/2`, `azure-strict/1`, `json_schema`, usage reporting, no streaming |
| Generation options | `max_completion_tokens=3000`, `reasoning_effort=low`, no temperature or tools |
| Raw / canonical / HTTP envelope | 10,000 UTF-8 bytes / 10,000 compact ASCII JSON bytes / 26,192 bytes |
| Context | 28,000; stage input allowance 24,800 plus 100 overhead and 100 safety |
| Experiment reservation | At most 25,000 input + 3,000 completion tokens, one call |
| Other local bounds | 8 claims, 256 characters per claim/annotation, 8 annotations; 60-second generation deadline, connect timeout 5 seconds, read timeout 60 seconds |

The single-call preparation explicitly constructs the managed settings and
capability; it does not select them from generic application generation options.
StageProfile only permits prompt 3. The renderer file checksum and fixed model/
validation excerpts match their approved references. Prompt 4 remains a documentation
proposal; application-owned-ID generation has not been activated. The model must
still copy supplied ordered claim UUIDs and authorized source IDs. No prompt,
schema, validator, response limit or generation instruction changed in this task.

Current full-suite interpreter: **Python 3.10.13**, using the existing
`estudio_polymind` environment. Installed versions inspected: pytest 8.4.2,
Pydantic 2.13.4, pydantic-settings 2.14.1, jsonschema 4.26.0, requests 2.34.2.
The existing dependency-free portability probe was rerun successfully on 3.10.13,
3.11.8 and 3.12.9. No full application suite on 3.11/3.12 is claimed. Python 3.13
remains unverified; no dependency or interpreter was installed.

## C. Source and fingerprint verification

The following values were recomputed by importing the authoritative repository
functions under pre-import network denial and settings isolation. No approved
configuration, approval artifact or fingerprint constant was regenerated.

| Binding | Current full value | Authoritative computation |
|---|---|---|
| Executor | `de11d7cbeb269591caa607494d29a76b894bd48af15d17ab2095ffb51b96e598` | `foundry_single_call.executor_digest()`; sorted Python source hashes under documents, governance, security, llm and tests/performance, using its existing digest function |
| Generation source | `4c37473513e2f1455cfa44a84c687b661a484e2fea0a390dedf9396269610d05` | `foundry_l1.generation_contract_digest()`; existing twelve-file mapping and canonical JSON hashing |
| Provider schema | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` | `documents.jobs.models.fingerprint(provider_schema(generation_schema()))`; same canonical digest used by the harness |
| Inference configuration | `7eaa6b52ad387f9f0c82e318e9c74fa378ffda0baec85d0f7157cc4ab0553519` | `ManagedSynthesisInference.config`, bound to explicit settings, provider identity, deployment and converted schema |
| Managed renderer source | `5b272d4a7591692eeeb328da09bc39b35d402bebd1d8ada3b891f6b1d6e8928c` | Existing complete managed.py source-check regression |
| Pinned catalog | `dad37bc0f349cdfbea16e25cae028a0b5042e4e3e3daac4f141f9b566c5bc65e` | Existing `sha256(catalog.model_dump_json().encode())` check in `one_call_contract`; public fixture matches |

Executor and generation source match the supplied post-diagnostic reference values
exactly. Compared with the earlier references, executor changed from
`9cd6711b61f2896090d351468e42dcc9a7c00f77e8f6cfc41c6f273172897b5a`
and generation source from
`82ecad5d4cb2e8fd2e0981c7d3710bbb3a582e56ef9eebca07ab0f314a4d05f9`.
The prior observability report documents why: diagnostic/provider metadata code
resides inside whole files included in these source hashes. These changes are
binding changes even though the semantic generation request is preserved.
The AST portability helper/tests are outside those binding path sets and did not
change either value. Provider schema matches both earlier reference values.

The historical preparation helper still pins generation source
`6f936342efb8e22faf23d59ebf71f7846d3255692d398c27d1e6a449ef41e247`.
Its `verified_schema()` rejects current source, intentionally and before output.
This is an inactive historical preparation guard, not a defect in
`foundry_single_call.prepare_analysis()`, which the actual launcher uses. Do not
change the constant or reuse old packets to circumvent that rejection.

### Deterministic representation comparisons

The existing `test_complete_pre_edit_generation_contract` representation and its
fixed oracles were used separately from authorization fingerprints. All nine
comparisons below were recomputed and match. These cover the entire StageRequest,
GenerationRequest and wire payload, without dropping diagnostic-sensitive fields.
The three-stage records use the established synthetic workflow's `offline-model`
binding; they are not private operator-request hashes.

| Stage | Component | Actual SHA-256, matching preserved oracle |
|---|---|---|
| chunk | request | `12f09a58b2798efd124334559d8c1c692d0614422ec748475b6a8b6bf69a7f3b` |
| chunk | generation | `cb41fb6fbca5f160b97ac16152955e5a5029dc83c400702821b4302232d71659` |
| chunk | payload | `b2a6745cbe2607f0bc44ff6c9b1b679c223ee66994401942e84b48461c0c5533` |
| structural | request | `ad3eac20bd5fd5c3871b8c43540720d3f5eb98fe0317fc9f84f0f9533513dddf` |
| structural | generation | `d4ce5cbbce3b55d7b8ddbb83b5b118b01435ad974cb2e42c68a36d77f5ac846f` |
| structural | payload | `409106cd46830c65f2305356a86c583e5f3403721c9bbfa43605765e6a8b7c72` |
| root | request | `419a71edd3a494700bdd8c9c1426793fc75650fd9d61eac90ca5cfae8ac1ddf2` |
| root | generation | `997a01bf07d9ebf16fb4ed886e7d7ada608ed1b7aa0f4b1d8d969a9d4ec53541` |
| root | payload | `bce41543e4b435f299a7123b748cb22c320581b37b5f32b34ced107989839b78` |

The actual single-analysis preparation was additionally rendered with synthetic
scope UUIDs 1 and 2 through `prepare_analysis`, and its real provider adapter was
exercised with an in-memory HTTP fake and the intended deployment mapping.
Its existing `digest({system,data,schema})` result is
`bb4d0a9f7e24b6dd7baa702006dbc0055ccc3fe7f5766b4d79fd68497e10666d`.
Fixture SHA-256 is
`1be99e19a56040fb55c74682a19f874d4d4573f18d9f52a9a7ae19c8158ea92d`.
There are four source pieces, no children and an estimated 10,903 input tokens.
Neither identifier values nor source/prompt contents are copied into this report.

That rendered digest is **synthetic-scope-specific**. The actual operator's derived
scope changes evidence/stage identities and request bytes. Its current private
rendered-request binding and whole-configuration digest are **NOT VERIFIED**.
No synthetic digest here is an approval or a value to transplant into that packet.

**Current semantic contract: UNCHANGED relative to the preserved pre-diagnostic
contract.** Fixed source fixtures additionally protect domain constraints,
deterministic identity, evidence membership, child links, coverage, categories,
serialization and predicate ordering. The token comparator ignores locations,
comments and cosmetic whitespace, with narrow inert diagnostic metadata exceptions;
it rejects executable metadata and semantic mutations. A schema hash alone was
not used to reach this conclusion.

**Attempt 4 comparability: PARTIALLY COMPARABLE.** The current preserved contract
comparison itself is exact, and intended strict-mode settings are semantically
comparable to documented historical preparation. Original submitted Attempt 4
request/schema evidence is unavailable in the permitted material, so exact live
equivalence cannot be established. Its rejection remains UNKNOWN. None of the
synthetic failures below, or F1, is attributed to Attempt 4.

## D. Azure request compatibility

Local request compatibility: **PASS**. Current deployment/service compatibility:
**REQUIRES OPERATOR VERIFICATION**.

`OpenAICompatibleProvider.execute()` constructs a distinct bounded payload instead
of using general-purpose `generation_parameters`. Its exact top-level keys are
`model`, `stream`, `messages`, `max_completion_tokens`, `reasoning_effort` and
`response_format`. Messages are one system and one user message. The payload
selects `epolymind-gpt-54-mini`, `stream=false`, 3,000 completion tokens and low
reasoning effort. The response format is `json_schema`, name
`polymind_stage_result`, `strict=true`, with the production converted schema.
No temperature, tools, tool choice, fallback model or unexpected generation
option is injected. This is Chat Completions response_format, not Responses API.

The explicit capability selects `max_completion_tokens` and permits returned
model identifiers `gpt-5.4-mini` and `gpt-5.4-mini-2026-03-17`, in addition to the
requested deployment alias. Compatibility is configured explicitly, not inferred
from the deployment name. The endpoint allowlist accepts only the intended resource's
HTTPS openai.azure.com/services.ai.azure.com v1 host, with no userinfo, port, query
or fragment. Authentication mode explicitly chooses api-key or Bearer headers.
No credential value was supplied to a real network session.

The recomputed provider schema is **1,790 canonical JSON bytes**, with StageResult
as its non-anyOf root object, all seven root fields required, three `$defs`
(Claim, Qualification, ClaimLink), four closed object schemas and **22 properties**.
Every property on each object is required and additionalProperties is false.
Claim.subject remains string-or-null. Arrays retain their element schemas; finite
local references resolve. The deepest container path reaches level five when
root is level zero, including arrays: StageResult → claims → Claim → qualifications
→ Qualification → evidence_ids. This is the converter's convention, not independent
certification of Azure's nesting interpretation.

`azure-strict/1` removes UUID format and string length/pattern constraints for local
validation, removes title/default annotations, and maps const to a singleton enum.
It refuses unsupported constructs, open objects, invalid/external/recursive refs
and excessive local complexity. Pydantic's closed fields, UUID/Token/Text constraints
and the application evidence/identity/coverage validators remain mandatory.
Pydantic is not globally configured with strict type coercion disabled: normal
JSON-array-to-tuple and UUID-string conversion remain existing behavior.
Synthetic provider-valid witnesses pass all local validators across the profiles;
schema-valid witnesses with semantic defects are correctly rejected locally.

Model support, current region/SKU/version/endpoint availability and current Microsoft
service rules were not freshly queried. Dated public documentation evidence in the
prior audit is not upgraded to a current service guarantee. The exact server-side
nesting/subset behavior remains C1. No Azure CLI, SDK discovery or public-site fetch
was performed during this offline assessment.

## E. Diagnostic capability and privacy

### Actual ordering and propagation

The real single-call order is:

1. Validate configuration/window, private authorities, identity, signed approval,
   fixture/request hashes, policy bindings and replay state; consume the separately
   authorized approval only in a future live run, before provider construction.
2. Render with ManagedSynthesisInference during preparation. The single-call runner
   then calls GovernedExecution directly; it does not run the durable handler's
   ManagedSynthesisInference.analyze path or full workflow.
3. GovernedExecution revalidates authorization, reserves owner/tenant finance,
   transitions RESERVED → ADMITTING, acquires RunGuard/shared provider admission,
   revalidates active authorization and transitions to STARTED before provider.execute.
4. Inside that call, ObservedProvider wraps the real adapter. It captures sanitized
   ProviderResultMetadata and adapter completion **before** governance cleanup.
   The adapter converts the schema, performs bounded HTTP, validates usage and
   strict envelope/refusal/model/finish/content rules and enforces raw bytes.
5. GovernedExecution's finally settles known usage or retains unknown obligations,
   then finishes admission, before returning or raising to the runner.
6. The runner revalidates authority and calls validate_result: request check → raw
   byte bound → unique-key JSON decode → Pydantic → canonical dump/revalidation/
   byte bound → stage/outcome/cardinality → source authority → claim identity,
   bounds, evidence/lineage/support/qualification/subject → coverage → text bounds.
7. The runner writes only sanitized terminal evidence. Success stores result hash
   and canonical byte count. This diagnostic does not persist a StageResult
   checkpoint or advance the durable DAG. The separate workflow persists immutable
   checkpoints only after validation and revalidates them at finalization.

This corrects the simplified prompt diagram: governance surrounds provider
execution; metadata observation occurs inside it, before accounting cleanup;
canonical encoding precedes domain stage/claim checks.

### Requested synthetic demonstrations

All ten cases were independently exercised through the **existing governed
single-call harness**, using ephemeral test identities/signatures, isolated
temporary authorities and HTTP fakes. They are demonstrations, not a reconstruction
of Attempt 4. Every row produced public **serialization_error**, terminal FAILED,
provider marker completed_strict_response, one actual HTTP attempt, SETTLED known
usage and accounting_failed=false.

| Authored failure | Validation stage | Retained reason | Safe Pydantic detail |
|---|---|---|---|
| invalid_uuid | pydantic_validation | invalid_uuid | claims[0].claim_id; count 1 |
| invalid_subject_token | pydantic_validation | invalid_subject_token | claims[0].subject; count 1 |
| subject_on_nonfact | claim_contract | subject_on_nonfact | absent |
| claim_id_mismatch | claim_identity | claim_id_mismatch | absent |
| originating_stage_mismatch | claim_identity | originating_stage_mismatch | absent |
| stage_id_mismatch | stage_binding | stage_id_mismatch | absent |
| unavailable_with_claims | stage_binding | unavailable_with_claims | absent |
| malformed_json | json_decode | malformed_json | absent |
| duplicate_json_key | duplicate_json_key | duplicate_json_key | absent |
| canonical_revalidation_failed | canonical_serialization | canonical_revalidation_failed | absent |

Canonical revalidation failure was injected only at the synthetic second
StageResult validation call; production code was not edited. Each case retained
finish_reason=stop, prompt/completion/total tokens=30/40/70 and supplied reasoning
tokens=5. Those are test values, not historical/live usage. Raw response-byte counts
were measured from each synthetic content value. Caps 3,000 and 10,000 were retained.

### Supported fixed taxonomy

| Diagnostic group | Supported emitted reasons |
|---|---|
| JSON | malformed_json, duplicate_json_key |
| Pydantic | invalid_uuid, invalid_subject_token, invalid_text_bound, missing_required_field, invalid_field_type, forbidden_extra_field, invalid_enum, other_pydantic_validation |
| Canonical | canonical_encoding_failed, canonical_revalidation_failed |
| Stage | stage_id_mismatch, stage_kind_mismatch, unavailable_with_claims, unavailable_missing_limitation, analyzed_without_claims, unavailable_reduction |
| Claim identity / contract | claim_id_mismatch, duplicate_claim_id, originating_stage_mismatch, subject_on_nonfact |
| Evidence | foreign_evidence, duplicate_evidence, invalid_qualification_source, invalid_child_link, duplicate_child_link, unsupported_fact, other_evidence_validation |
| Coverage | missing_source_coverage, missing_child_coverage |
| Limits | raw_response_limit, canonical_response_limit, claim_limit, annotation_limit, text_limit |

The enum also reserves other_canonical_failure and other_coverage_failure; these
are not claimed as observed branch outputs. Public mappings stay unchanged:
contract → serialization_error, evidence → invalid_reference, coverage →
extraction_failed, synthesis bounds → extraction_limit_exceeded. Qualification
text overflow retains its existing evidence-stage/public invalid_reference
classification while reporting text_limit. Provider truncation/raw overflow maps
to inference_output_limit, subject to F1's HTTP cleanup exception.

### Retained metadata and its limits

The audit can retain adapter completion, sanitized finish reason, prompt/completion/
total/reasoning usage, raw UTF-8 content byte count, completion/raw-content caps,
validation stage/reason, safe structural Pydantic path, saturated error count,
public category, accounting_failed and terminal execution state. Unknown values
remain null/absent. Numeric metadata accepts exact nonnegative integers through
signed 64-bit; booleans and invalid values are excluded. Reasoning counts must not
exceed completion counts and are not charged a second time.

Pydantic input/context/URL are excluded at extraction. The selected reason has
fixed priority and safe-path tie-breaking; the count saturates at 64, meaning at
least 64, and unknown/dynamic field names are discarded. A classifier failure
cannot suppress the underlying rejection. HTTP schema errors retain only bounded
status and closed reason classifications, never provider messages.

`completed_strict_response` establishes adapter completion, **not** an independent
JSON Schema validation or application acceptance. Provider/schema rejection,
truncation, missing usage and errors before decoding need not have all metadata.
Canonical/envelope ceilings are established in the bound configuration/source
and this report; they are not extra fields copied into ProviderResultMetadata.
The general durable job failure record retains its existing public category,
not all of the single-call supplemental fields.

Sanitized outcome/preflight records retain no model text, prompt, document prose,
evidence UUID values, credentials, Pydantic input values, free-form upstream messages,
JWTs, signatures or signing keys. Privacy sentinels were absent from the actual
synthetic outcomes. Outcome writing is exclusive, mode 0600 and fsynced; unsafe
paths/symlinks are rejected. Governance rows contain their existing opaque
owner/job/request identities and numeric usage, not evidence or response content.

The private audit directory is not synonymous with its sanitized outcome JSON:
preparation stores the fixed synthetic fixture extraction/plan under objects, and
replay/live-start markers retain minimal opaque approval IDs/hashes by design.
Those are existing private lifecycle artifacts, not raw model-response archives;
none was exported from operator storage during this assessment. Do not substitute
the broad L1 response/review artifact writer for this runner. The optional offline
schema-observation helper remains outside the live path and was not enabled there.

## F. Single-call containment and failure handling

**Actual-attempt ceiling: VERIFIED, one. Primary-failure preservation: FAILED
for F1's response-close combination.**

SingleCallConfiguration requires executor polymind-single-analysis/1, maximum_calls=1,
matching executor/generation/schema fingerprints and an exact `one_call_contract`.
`execute_stage` rejects non-analysis requests, children, scope/fixture/request hash
mismatches, non-one-call contracts and a substituted guard contract. It executes
one prepared GenerationRequest, not a scheduler/worker/full-workflow launcher.

RunGuard.acquire durably inserts a full one-call reservation **before** downstream
admission and HTTP. The insert is not contingent on accepted output. Outstanding
or stopped work blocks continuation; the second attempt fails fits(2), even with a
different logical identity. Governance's unique identity and compare-and-swap
STARTED transition independently prevent duplicate execution. A failed downstream
admission may conservatively count a reservation without any HTTP attempt;
`calls` therefore bounds attempted work, not merely successful responses.

Persistent approval consumption and exclusive live-start markers prevent reusing
the approval in another run directory. A fresh directory does not reset shared
ledgers/replay state. No automatic resume, repair, fallback, retry, structural/root
execution, Q&A, embeddings or paid telemetry path is invoked. The owned requests
session uses max_retries=0 and trust_env=false; request_json makes one post and
forbids redirects. HTTP `stream=True` only bounds body reading; model stream is false.
The runner has no call to check_readiness and imports no executing full launcher.
Tests count fake post attempts even when they raise, test restart/second-call denial,
and install forbidden sentinels on the full workflow/publication/Q&A paths.

Normal errors stop the guard, finalize audit collection and yield nonzero CLI
status. Known primary provider failures survive governance settlement/admission
cleanup errors, with accounting_failed=true. Audit-collection failures preserve
an existing category. HTTP/session close paths do not have the same protection;
F1 documents the demonstrated HTTP path. A write failure itself fails the CLI;
retained run/replay/financial evidence must be investigated rather than retried.

## G. Financial assessment

**Financial mechanism: VERIFIED offline. Current rates/budget: REQUIRES OPERATOR
VERIFICATION. Current authorized expenditure is not established by this report.**

`one_call_contract` pins catalog version phase17hl-pricing-eur-202610/1 and its exact
serialized hash shown above. It requires the intended provider/deployment/SKU,
one attempt, 25,000/3,000 per-call and aggregate token ceilings, 28,000 context,
one request per minute, zero fixed cost, zero additional cost and fits(1)=true,
fits(2)=false. The Contract enforces approved EUR amounts and **0 < maximum ≤ EUR 5**.
Missing, future-effective, unapproved, mismatched or insufficient pricing/bounds
fail closed. Decimal arithmetic uses explicit decimal rates and power-of-ten units.

The public regression fixture reproduces the pinned catalog with input/output
rates **EUR 0.659978880676 / EUR 3.959873284055 per 1,000,000 tokens**. Its provenance
string explicitly says **Synthetic review fixture**. The verified arithmetic is:

```text
(25,000 × 0.659978880676 + 3,000 × 3.959873284055) / 1,000,000
  + fixed 0 + extra 0 = EUR 0.028379091869065
```

This is the local pinned-catalog maximum token-cost calculation, **not a verified
current Azure quotation or total account-billing guarantee**. The fixture's allowed
contract maximum is EUR 5; the actual private signed maximum and current remaining
EUR balance were not read. No present authorization to spend EUR 5 or EUR 0.028379...
is implied. Input estimation conservatively counts rendered canonical ASCII bytes
plus overhead/safety; it is not billed token usage. The measured synthetic request
estimate is 10,903, while RunGuard reserves the full 25,000/3,000 experiment ceiling.

The operator must verify the exact catalog's present commercial applicability,
EUR conversion/billing unit, effective date and absence of fixed/separate charges.
If those facts do not agree with the pinned catalog/zero-extras contract, stop:
the existing binding needs separately reviewed remediation, never an invented rate
or an override. No pricing or billing API was called here.

Governance reserves owner and tenant budgets before provider execution. The
polymind-evaluation/1 overlay uses exact allowlisted internal scopes on existing
authorities: 16 requests/rolling 86,400 seconds, 500,000 tokens/UTC day, 1,500,000
tokens/UTC month, EUR 5/month, 112,000 reserved tokens, one concurrent request in
each workload class. Historical rows across policy versions remain chargeable;
the overlay is not a fresh budget pool. Authority paths, quota key and provider
policy hash must match, and stored policy/catalog must equal runtime models.

Known prompt/completion usage settles before StageResult validation. All ten
synthetic domain rejections retained SETTLED known charges. Invalid/missing usage
is not zero; it leaves UNKNOWN or unresolved STARTED state and unfinished/stopped
run work. Known partial observations cannot be contradicted on reconciliation;
conflicting/duplicate settlements fail. Unresolved cost/tokens survive period
boundaries. A downstream validation error cannot erase or refund that usage.
Both governance settlement and admission finish are attempted; their cleanup
errors retain a known primary inference error. F1 occurs earlier in HTTP cleanup.

UNKNOWN is not a universal ban on every separately authorized future experiment:
it consumes persistent budget/capacity and blocks this run's repetition. The
operator procedure requires investigation/reconciliation before seeking a retry;
new identities or cloned ledgers cannot be used to forgive debt. The assessment
did not construct any real authority, reserve funds or reconcile live usage.

## H. Authorization assessment

```text
Authorization mechanism: VERIFIED (source inspection and synthetic regressions)
Current operator approval: NOT VERIFIED
Source-binding consistency: PARTIAL (current local hashes verified; private bindings not inspected)
Current authorization state: UNKNOWN
Execution authorized now: NOT VERIFIED
```

No authentication or approval was inferred from reports, model names, a readiness
verdict, the historical preparation helper or unsigned configuration booleans.
The exact required mechanisms are:

1. A validated current SingleCallConfiguration with exact current executor,
   generation-source and provider-schema hashes, intended deployment bindings,
   one-call financial contract, fixture/rendered-request hashes, owner scope,
   job/request identities, endpoint/authentication choice, policies and paths.
   The separate acknowledgement equals `configuration_digest(config)`, which hashes
   validated model_dump_json bytes, not raw file bytes.
2. Existing private operator-owned outside-repository authorities and audit storage,
   with safe absolute paths/no symlinks. Evaluation binding version must be
   polymind-evaluation/1, owner must be allowlisted, and governance/provider paths,
   shared key and exact AdmissionPolicy hash must agree. Existing authority policy,
   catalog, schema, history and available owner/tenant/provider capacity still govern.
   No new activation or database replacement is authorized here.
3. Entra_v2 user authentication: pinned tenant-specific issuer/JWKS, RS256 key,
   exact scalar API audience, matching tid/ver=2.0, valid integer lifetimes,
   delegated access_as_user scope, user identity and exact role set
   {PolyMind.L1Operator}. This maps to PUBLICATION_MANAGE only. Principal scope
   must equal owner_scope, and the same principal must already be registered,
   enabled and authorized in SecurityAuthority. Owned fixture access is revalidated
   through the existing DOCUMENT_DELETE snapshot; no privilege policy was changed.
4. Independently provisioned ApprovalTrust version polymind-approval-trust/1,
   purpose=live, pinned RSA public key 2048–8192 bits, key ID and exact operator
   issuer/subject/tenant. Replay directory must be private, persistent and outside
   the run audit directory. The private signing key is never launcher input.
5. A compact signed JWS whose header is exactly alg=RS256,
   typ=polymind-approval+jwt, kid=trusted key ID. Required claims are exactly iss,
   aud, jti, iat, nbf, exp, purpose, binding. Issuer is polymind-operator-approval/1;
   audience for this executor is **polymind-single-analysis-live**, not polymind-l1-live.
   Purpose is live, jti is a canonical UUID, timestamps are exact integers,
   iat ≤ nbf < exp and exp-iat ≤ 86,400 seconds, with current validity enforced.
6. The signed binding equals `foundry_approval.bindings()` exactly: validated
   configuration digest; operator; resource/endpoint/deployment/model/version/SKU/
   region; EUR maximum/fixed/extra costs; attempts/token/aggregate/rate/context limits;
   expiry; and execution executor/version/source-generation/schema hashes. The
   configuration digest transitively binds catalog, policies, authorities, request,
   fixture and all attestations, including fields not repeated in explicit binding.
7. All nine live attestations must be present: credential_valid_until,
   approval_expires, execution_not_before, credential_audience_verified,
   quota_verified, shared_consumers_verified, charges_verified, actual_azure_rpm
   and actual_azure_tpm. Current time must be at/after start and strictly before
   min(approval_expires, credential_valid_until)-600 seconds. The exact cutoff is
   ineligible. Actual capacity must cover configured policy. Approval, principal
   token and credential validity must also have more than 60 seconds remaining
   at final verification/execution. A separate nonblank Azure credential is required;
   an API-key use deadline is an operator attestation, not measured key expiry.
8. No prior RunGuard records/live-start marker; approval verification repeated
   before exclusive fsynced one-use consumption, then exclusive live-start evidence.
   A consumed approval stays consumed on failure. A different signature/key/run
   directory cannot replay the same ID. Cancellation/expiry/authorization are
   rechecked before the attempt. Financial and provider admission still may deny
   a correctly signed request; signature alone does not reserve or guarantee funds.

The runtime does not consult the legacy polymind_l1_approval identity claim.
It performs no token acquisition/refresh and cannot turn the review into approval.
Historical approvals bound to a differing **required executor/generation source**
cannot validate current code, even when semantic request comparisons match.
By contrast, changing a non-authoritative test observation alone does not invalidate
approval. No old approval was read or declared currently valid/invalid by inspecting
its protected values; current real approval and source consistency remain unverified.

## I. Regression and quality results

The complete configured suite was run once against this working tree, using its
normal pytest.ini/test paths and permanent root conftest. Execution directory was
a temporary directory with a symlink to the public tests tree for relative fixtures.
This avoids the real operator dotenv for child interpreters as well as the main
process. The repository's installed absolute Python interpreter was retained.
Application settings fields and Azure/OpenAI/PolyMind/OIDC/governance credential
environment prefixes were removed in the verification subprocess without printing
values. Existing tests still explicitly exercise synthetic env/dotenv precedence.

The inspected existing polymind_e2e_offline_guard startup plugin is loaded before
collection/application imports. It patches socket connect/connect_ex/sendto,
connection and DNS functions, adds socket/DNS audit hooks, counts attempted
operations and fails a session even if its blocked exception is swallowed.
The permanent conftest separately intercepts omitted `_env_file` before application
settings singleton creation, preserving explicit settings and validators.

This is Python-level denial, not an OS firewall or blanket promise about native
extensions/arbitrary subprocess binaries. Child workflow and configuration tests
install their own inspected denial; other inspected children perform only local
ledger/extraction operations. Local Helm subprocesses render/lint, not deploy.
The parent counter does not aggregate every child counter. Zero observed attempts
is reported within that scope; no Azure CLI operation or unmocked live-inference
entrypoint was invoked.

Temporary evidence directory: `/tmp/polymind-attempt5-assessment/`.
Primary invocation: `python /tmp/polymind_attempt5_verify.py --full`, whose inspected
driver calls the absolute interpreter with `-m pytest -q -c <repository>/pytest.ini
<repository>/tests`, external basetemp/JUnit/cache paths, sanitized environment and
PYTEST_PLUGINS=polymind_e2e_offline_guard. No test path was deselected.

| Executed check | Actual result |
|---|---|
| Full current regression | **1,678 passed**, 0 failures/errors/skips, 42 warnings, **235.09 s**, exit 0 |
| Baseline identity comparison | Same 1,678 (classname,name) identities as retained AST-portability full JUnit; none removed |
| Focused required coverage within that full run | **645 passed**, overlapping subset, not a separate additional pytest run |
| Requested synthetic governed diagnostics | **10/10 expected reasons/public categories/accounting/privacy checks passed**, one fake HTTP attempt each |
| Additional cleanup probe | Initial synthetic demonstration plus **4/4 controlled real-requests.Response observations** reproduced F1; these are defect demonstrations, not passing readiness requirements |
| Network attempts | **0** in full suite, contract inspection, diagnostic probes and portability runs |
| Portability | Python 3.10.13/3.11.8/3.12.9: 8 source sections match, 7 semantic/prompt mutations detected, inert diagnostic edit matches |
| Relevant source compilation | `PYTHONPYCACHEPREFIX=/tmp/polymind-attempt5-assessment/pycache python -m compileall -q documents llm governance security tests`: exit 0 |
| Source-contract/observability Ruff lint and format | Both pass; three files already formatted |
| Eight relevant implementation/harness files, Ruff | Exit 1, **24 existing findings**: BLE001=7, I001=2, SIM114=1, UP035=1, F401=2, UP045=5, C408=5, S110=1; same rule counts as prior observability report |
| Git whitespace/index | git diff --check passes; index empty |

Focused subset counts from the actual full JUnit:

| Module | Passed |
|---|---:|
| final_offline_azure_compatibility | 116 |
| live_failure_observability | 112 |
| phase17hl_offline_e2e | 31 |
| single_call_harness / single_call_preflight | 46 / 28 |
| source_contracts | 47 |
| output_limit_diagnostics / single_call_diagnostics | 41 / 21 |
| evaluation_governance / evaluation_activation | 23 / 5 |
| foundry_approval | 69 |
| managed_inference / strict_schema_compatibility | 38 / 13 |
| structured_provider | 55 |

The 42 warnings are the existing record_property/JUnit xunit2 compatibility warnings.
No skip/xfail or weaker assertion was introduced. Temporary synthetic authorities
and ephemeral signing fixtures are not live financial/approval operations.
An initial standalone contract-inspection script failed on its relative public
quality.json path when launched from `/tmp`; rerunning from the prepared public-test
symlink directory succeeded. That tooling invocation is not hidden as a passing
check or counted as a regression error. No source/configuration was repaired.

Evidence files include full.log/full.xml, contract.json, synthetic-diagnostics.json,
cleanup-reproduction.json and their assessment-only scripts. Their temporary
availability is supplementary: the durable report includes the measured fingerprints,
classifications and F1 reproduction below. No generated test output enters Git.
Docker/Compose/build/deployment checks are inapplicable to a two-document assessment
with unchanged runtime/container configuration and were not run.

## J. Blockers, external conditions and residual risks

### F1 — HTTP response close can mask the primary inference failure

**Severity: medium reliability defect; blocking for this diagnostic assessment's
explicit primary-failure preservation requirement.**

Exact source: [llm/bounded_http.py:110](../../../llm/bounded_http.py#L110), in
request_json's finally block; response.close at line 112 is unguarded. This block
executes after any normalized HTTP, timeout, envelope-size or protocol error. A close
exception replaces that error before OpenAICompatibleProvider can propagate its
category/output-limit diagnostics. GovernedExecution correctly preserves the
exception it actually receives, but by then it is the cleanup exception.

The offline reproduction used the **installed real requests.Response**, with a
local BytesIO raw stream whose close raises OSError. No remote transport or provider
was used. The single-call rig used only synthetic authorities and ephemeral test
approval fixtures. The controlled comparison changed only whether raw.close raised:

| Fake transport response | Raw close | Observed public failure | Output-limit record | Calls / financial state |
|---|---|---|---|---|
| HTTP 302 | normal | inference_configuration | absent | 1 / UNKNOWN |
| HTTP 302 | OSError | **worker_failed** | absent | 1 / UNKNOWN |
| HTTP 200, 26,193 envelope bytes | normal | inference_output_limit | present | 1 / UNKNOWN |
| HTTP 200, same envelope | OSError | **worker_failed** | **lost** | 1 / UNKNOWN |

All four were FAILED with accounting_failed=true because usage was not established;
the original budget obligation remains and no second request occurred. Private
exception sentinels were absent from every sanitized outcome. This does not
demonstrate an accounting refund or infinite call path. It demonstrates that an
expected diagnostic category can disappear despite current governance cleanup fixes.

A minimal direct reproduction of the same boundary, independent of any approval
or authority, is the following **offline-only** Python fragment under the inspected
pre-import network guard:

```python
import io
import requests
from llm.bounded_http import request_json

class Raw(io.BytesIO):
    def close(self):
        raise OSError("synthetic cleanup failure")

class LocalHTTP:
    def post(self, *args, **kwargs):
        response = requests.Response()
        response.status_code = 302
        response.raw = Raw(b"")
        return response

request_json(LocalHTTP(), "https://offline.invalid", headers={}, payload={},
             timeout=(1, 1), total_seconds=1, max_bytes=26192)
# Actual: OSError; the redirect's InferenceConfigurationError is replaced.
```

**Smallest correction recommended, not implemented:** preserve an already active
normalized failure across response cleanup, using the same primary-error precedence
principle as GovernedExecution. If cleanup alone fails, fail closed with a sanitized
normalized error; never return success after unhandled cleanup failure. Add narrow
synthetic regressions covering redirect/output-limit plus close failure and a
cleanup-only failure. Check the owned session-close boundary in the same small
review. Preserve usage, one-call state, rejection predicates, prompt and schema.
This will change source fingerprints; recompute them through existing functions
and review fresh configuration bindings after the fix. Do not refresh approvals
inside this assessment or silently label current hashes ready for corrected code.

This failure combination was not covered by the passing full suite. It is not a
reconstruction of Attempt 2 or Attempt 4, and no claim is made that Azure caused it.
No other substantive engineering blocker was demonstrated in the assessed path.

### Seven external operator verification conditions

These conditions remain required **after** F1 is corrected and reassessed. They
summarize existing policy, not new approval requirements.

| ID | Required operator-side evidence; present status |
|---|---|
| C1 — deployment | Confirm the intended resource, Spain Central region, deployment/model version/SKU, v1 Chat Completions and exact strict-schema/low-reasoning support/availability. **NOT VERIFIED**; dated preparation is insufficient. |
| C2 — commercial terms | Confirm current exact EUR rates/unit/provenance and zero fixed/separate charges against the pinned catalog; verify signed maximum covers one bounded attempt. **REQUIRES OPERATOR VERIFICATION**; public fixture arithmetic is not a current quote. |
| C3 — authorities and funds | Confirm existing evaluation overlay/scope, exact shared policies/paths/key/catalog, ledger integrity/history, unresolved obligations, available owner/tenant monthly funds/token/request allowances and account budget. **NOT VERIFIED**; no protected database or billing API was opened. |
| C4 — operator authorization | Independently verify current Entra operator and registered permissions, trusted signer/replay authority, fresh exact single-analysis JWS bindings, validity and unused ID. **NOT VERIFIED**; no approval created/read/signed/consumed. |
| C5 — credential and timing | Verify inference credential target/audience/permissions, nonblank separate runtime credentials, correct auth header and fresh deadlines; start within the exclusive 600-second margin and retain >60-second token validity. **NOT VERIFIED**. |
| C6 — shared capacity | Confirm actual Azure RPM/TPM, all shared consumers, matching provider policy, at least protected 2,000 interactive TPM and capacity for 25,000+3,000 tokens; configured actual TPM range is 28,000–30,000 but a full 28,000 background reservation plus 2,000 protected TPM requires 30,000. **NOT VERIFIED**. |
| C7 — exact execution handoff | Verify final corrected-source configuration/acknowledgement, actual-scope fixture/request hashes, new one-call run identities, safe existing authority/audit paths, persistent replay state, storage/retention owner and reviewer. **NOT VERIFIED**; no packet was generated here. |

### Historical limitations and nonblocking recommendations

Attempt 4's exact payload/schema and rejected predicate remain unavailable; its
completed-strict marker is not proof of application validity. Synthetic failures
cannot establish historical cause. The pre-diagnostic semantic contract is
preserved independently of that historical uncertainty.

Keep prompt 3 for this comparison. Its known unavailable-analysis coverage wording
and qualification-copying/lineage ambiguities remain review topics, not reasons to
silently activate prompt 4 or change identifiers. Valid analyzed witnesses show the
current contract is satisfiable. Model obedience, semantic entailment, live latency/
reliability, reasoning-token consumption and acceptance frequency remain unproven.
Byte allowances do not guarantee completion within 3,000 tokens.

Single-host SQLite governance and file-based replay assume a trusted administrator
and persistent state; they are not distributed production/AKS controls. Existing
lint debt and Python 3.13 verification remain nonblocking for this assessed 3.10
diagnostic environment. Neither necessitates broad hardening in this task.

## K. Proposed operator checklist and handoff

This is a checklist of prerequisites for a **future separately authorized task**,
not a prepared approval, execution command or instruction to run now.

1. Obtain the narrow offline F1 correction and regressions, then repeat the relevant
   assessment. Preserve managed-prompt/3, strict schema and all domain predicates.
   Record the resulting executor/generation/schema/inference configuration values
   using the authoritative functions; today's source hashes will no longer suffice.
2. Establish C1–C3 and C6 from the actual target and existing shared authorities.
   Retain prior accounting/replay/history; investigate unknown obligations. A pricing
   or policy mismatch requires its existing separate review, not a bypass.
3. Review a single-analysis configuration against those exact bindings and the
   real verified operator's scope-specific fixture/request hashes. Confirm one
   call, 25,000/3,000 tokens, EUR ceiling and 10,000/10,000/26,192 byte bounds,
   endpoint/authentication, shared policies/paths, audit retention and reviewer.
4. In the separate authorized operator process, establish current Entra identity,
   registered permission, independent signing trust, persistent replay state and
   credential/time attestations. Any approval decision must bind the complete
   configuration plus single-analysis audience/purpose and current source hashes.
   Use the existing independent signing workflow only after that review.
5. Recheck launch eligibility and budget/capacity immediately before any separately
   approved invocation. Do not use the four-call foundry_l1 launcher. Stop on expiry,
   consumed ID, source/configuration mismatch, unavailable budget or uncertainty.
6. After a future authorized single attempt, inspect only sanitized terminal reasons,
   provider metadata, actual attempt count and durable financial settlement. A failure
   or UNKNOWN obligation ends that run; it never authorizes repair/retry/resume.
   Successful application validation would still leave other Phase 17H evaluation
   requirements to demonstrate separately.

### Assessment review, preservation and final state

Assessment self-review compared request/schema/source bindings with the preserved
references, followed metadata/accounting/error ordering, and independently reproduced
F1 with real requests.Response behavior. No domain/model/provider-specific
application redesign or production edit was made. The recommendation was changed
to NO-GO because external conditions cannot cure this demonstrated code defect.

Separate pre-commit review covers both new Markdown documents: no active credential,
private signature/key/packet, actual operator identity, full prompt/response body,
evidence UUID value or private authority contents are included. Public deployment
names, public schema/type names, synthetic diagnostic values and source hashes
are review evidence. Links point to existing sources/reports. No runtime artifact,
new dependency, debug implementation, policy migration or historical report edit
was added. The saved prompt records the supplied task, not execution authority.

Final public-file manifest comparison and git status/diff checks verify that all
391 pre-existing inventoried public files remain unchanged, with only the two requested
documents added. The manifest excludes .env-prefixed files and ignored/private
storage; this is not a claim to have hashed protected material. Final tracked
`git diff --stat` remains **20 files changed, 812 insertions(+), 76 deletions(-)**.
Final complete status is **20 modified tracked files, 111 untracked files**, no
staged files, same branch and HEAD. Existing .env.example was not edited by this
assessment. Tracked whitespace and explicit new-document whitespace checks pass.

Azure inference calls: **0**. Paid inference: **0**. Cloud operations: **0**.
Live financial reservations/settlements: **0**. Operator approval creation,
regeneration, refresh, signing, activation or consumption: **0**. Protected artifact
access: **0**. Production/test/policy/configuration modifications: **0**. Commits,
pushes, staging, branch/history changes and deployments: **0**. Synthetic local
regression identities/signatures/reservations are explicitly separate from these
operator/live counts.

**Final recommendation: NO-GO for requesting execution authorization on the present
implementation. Resolve F1 offline, reassess, then establish C1–C7 through the existing
operator process. Execution authorization remains NOT VERIFIED. Attempt 5 must not
be run from this assessment. Phase 17H remains PARTIAL.**
