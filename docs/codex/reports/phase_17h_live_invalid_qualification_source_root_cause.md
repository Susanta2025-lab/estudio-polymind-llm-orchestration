# Phase 17H — Offline investigation of invalid qualification provenance

Investigation date: 7 November 2026. Branch: `master`. Scope: original-artifact
forensics, deterministic replay, existing isolated regressions and recommendations.
No application, prompt, schema, validator, test or configuration was changed.

## 1. Executive summary

**The original failure is reproduced offline without modifying the response or
weakening validation.** The first retained provider response contains one foreign
evidence reference, at `claims[7].qualifications[0].evidence_ids[3]`. Its primary
claim references are all valid. The invalid reference is already present in the
provider-returned content before application decoding.

The original source inventory contains four authorized evidence IDs. They resolve
to the original extraction, survive an exact deterministic plan rebuild, appear
unchanged in the rendered request, and match the validator's allowlist. Recreating
the recorded request-material hash produces an exact match. Neither the invalid
ID nor a legitimate alternative role for it exists in those inputs.

The invalid UUID combines the first segment of one allowed ID with the remaining
segments of another. This lexical composition is confirmed; a model copying or
blending error is the best-supported mechanism. The model's internal reasoning
and the cause of that generation error are not observable. The current prompt
already distinguishes evidence and claim IDs and prohibits invented references.
Its lack of explicit qualification-specific copying guidance is a possible
contributor, not a demonstrated cause.

The static schemas do not enforce the request-specific evidence allowlist.
Consequently, the foreign but syntactically valid UUID passes schema decoding and
is correctly rejected by G2's application-level membership check. This is an
**application acceptance failure following successful provider transport**.
It is not evidence of a broken source inventory, normalization defect, incorrect
validator, or successful analysis checkpoint.

The smallest initial correction is a versioned generation-only clarification for
exact evidence copying, including qualifications and stage-local reducer rules,
with a regression for mixed valid/foreign qualification references. Request-bound
schema enums are a stronger, separately assessed generation safeguard. Neither
approach warrants relaxing G2, repairing output, or automatically retrying.
Phase 17H remains **PARTIAL**.

## 2. Original failure and evidence provenance

The [execution report](phase_17h_final_approval_signing_and_controlled_execution.md)
records one authorized launcher invocation and one paid call on 7 November 2026.
The call completed at approximately 01:29:02 UTC. Usage was 2,506 input and 2,130
output tokens, total 4,636, with EUR 0.010088437170011206 accounted under
`phase17hl-pricing-eur-202610/1`. Governance settled; shared admission finished
with `active=0`; the run guard stopped with `evidence`. Approval was consumed.
No new accounting transaction or approval operation was performed here.

Primary material inspected was the retained PDF, native extraction, structure,
plan, provider-call record, response copies, job ledger, result, execution receipt
and independent review. No substitute extraction, PDF, model result or accepted
checkpoint was generated. The extraction's source hash matches the retained PDF;
the extraction object's canonical bytes match the plan's extraction reference.
The separately stored structure equals the structure embedded in the plan.

The retained response text is identical in `provider-calls.json`, `responses.json`
and the provider record in `result.json`. These are three copies of **one**
observation, not three independent provider responses. Its verified SHA-256 is
`f3edc09234a31ded2c0ce7acafcecb6c8a1275356e5045292a5bd382764520e1`.
The raw response envelope and a separately persisted decoded `StageResult` were
not found. The decoded result used below is reconstructed directly from the
unchanged retained response text.

A before/after SHA-256, byte-size and permission inventory covers all **17** files
present in the original audit directory at investigation start. Fourteen are
original execution artifacts; three are the previously preserved execution
receipt, independent review and inventory. All remained unchanged. Temporary
analysis, pytest artifacts and network guards were kept outside that directory
and outside the repository. The private evidence location, credentials and
operator identities are intentionally omitted from this report.

## 3. Exact authorized evidence inventory

Native extraction owns source units, blocks, spans and version lineage; it does
not assign the model-facing `source-evidence/1` IDs directly. During planning,
[`SourcePiece.evidence_id`](../../../documents/digestion/models.py) computes:

```python
stable_id('source-evidence/1', fingerprint(evidence.model_dump(mode='json')))
```

[`stable_id`](../../../documents/models.py) is UUIDv5 over an unambiguously
JSON-encoded tuple using `NAMESPACE_URL`. The fingerprint binds the complete
`EvidenceRef`, including scope, document version, extraction, source, block and
span. Thus an ID is deterministic for the same reference, not a universal page
ID across changed documents, scopes or chunk boundaries.

The failed chunk contains four pieces, all with `limitation=none`. Sanitized
inventory, in original source order:

| Label | Exact canonical evidence ID | Source span | Extraction resolution | Rendered data / CONTROL / validator |
| --- | --- | --- | --- | --- |
| E1 | `bdbc33a9-64d8-5157-998f-b774c9d5664d` | `[0, 346)` | Exact match | Same value in all three |
| E2 | `1b51f2e5-e236-5dc3-8af1-bc008e8951e4` | `[0, 346)` | Exact match | Same value in all three |
| E3 | `4bf2d425-3346-5a1b-b3bf-a91ad02cadc0` | `[0, 453)` | Exact match | Same value in all three |
| E4 | `2cd2bfa9-dbe8-532a-9681-2a68892e372f` | `[0, 346)` | Exact match | Same value in all three |

All four are UUIDv5 values, and each `EvidenceIndex.resolve(piece.evidence)`
returns exactly `piece.text`. Rebuilding the complete plan with the retained
extraction, extraction reference and original `DigestionProfile` produces a plan
equal to the retained plan: one chunk and two reducers. No re-extraction was
necessary. No source text is reproduced in this comparison.

The invalid ID, `2cd2bfa9-64d8-5157-998f-b774c9d5664d`, is absent from every
source/extraction/structure/plan identifier set. It is not a source ID, block ID,
structural parent, chunk/reducer stage ID, supplied claim ID or inherited claim.
This analysis chunk has no child material or inherited links. Within retained
audit files, that string occurs only in the three response-bearing JSON files and
the subsequent independent review; none constitutes an input authority for it.

Its exact lexical decomposition is:

```text
E4 first segment:       2cd2bfa9
E1 remaining segments: 64d8-5157-998f-b774c9d5664d
Observed invalid ID:   2cd2bfa9-64d8-5157-998f-b774c9d5664d
```

This is evidence of the output's composition, not proof of the model's internal
copying process or permission to substitute E4 for it.

## 4. Model-facing request and reconstruction limits

The original full HTTP request was not retained. Its generation inputs can,
however, be reconstructed deterministically using the original plan and source
pieces, [`DigestionHandler.request`](../../../documents/digestion/workflow.py),
the existing strict L1 settings in
[`foundry_preflight.execute`](../../../tests/performance/foundry_preflight.py),
[`candidate_capability`](../../../tests/performance/foundry_recalibration.py),
and [`ManagedSynthesisInference.render`](../../../documents/digestion/managed.py).
Only a render-only model-identity adapter was supplied; its inference method
raises if called and was never called. No provider result was simulated.

The reconstructed managed inference configuration matches the plan's stored
`inference_config`. The current generation-contract SHA-256 matches the recorded
configuration binding:
`00bf895290e1da2fb81372ff1ea921d8d7f464ea14f41110f54313d0423ad904`.

The L1 recorder hashes this exact serialization:

```python
sha256(json.dumps(dict(system=request.system, data=request.data,
                       schema=request.schema, output=request.output_tokens),
                  sort_keys=True).encode()).hexdigest()
```

Both retained and reconstructed hashes are
`1a2d26a7ab1136be73bb071e78dc18f3102f5ee41785f0cb35d2dddd78f64fc6`.
This establishes equality of the hashed generation material under the recorder's
serialization, subject to normal SHA-256 collision assumptions. It does **not**
establish captured HTTP wire-byte identity: headers, HTTP serialization and the
complete transmitted envelope were not recorded by that hash. The adapter's
logical payload can be traced in source; its original wire bytes remain absent.

The reconstructed request shows:

- All four evidence IDs are explicitly visible twice: in
  `CONTROL.allowed_evidence_ids` and on individual `UNTRUSTED_DOCUMENT_DATA`
  pieces. CONTROL sorts its set; source data preserves source order. Sorting and
  nested ASCII JSON escaping alter representation/order, not identifier values.
- Eight `claim_ids_in_order` and the current `stage_id` are separately labeled.
  UUID syntax is shared across identifier roles, but the actual evidence IDs are
  distinct from all supplied claim/stage IDs. The bad ID is absent from system
  instructions, data and schema.
- The trusted prompt says “Cite ONLY allowed evidence IDs; never invent
  references” and separately instructs consecutive claim IDs and
  `originating_stage=stage_id`. The global evidence rule covers qualifications,
  but no sentence explicitly names nested qualification arrays or says to copy
  an entire UUID without recombining segments.
- The prompt requires preserving qualifications/conflicts and complete source
  coverage. It provides no qualification-specific dynamic enum. There is no
  evidence that an instruction explicitly authorized the invalid value.

[`generation_schema`](../../../documents/digestion/managed.py) expands required
fields on a static `StageResult` schema. The domain schema represents qualification
evidence items as UUID-formatted strings; it has no request-specific enumeration.
[`provider_schema`](../../../llm/azure_schema.py) deliberately removes UUID format,
string length and pattern constraints for the local Azure strict subset. The
resulting evidence items are strings. Both the original domain JSON schema with
UUID format checking and the converted provider schema accept the unchanged
response structurally. Valid UUID syntax alone cannot prove source membership.

The renderer estimated 11,626 tokens conservatively, corresponding to 11,426
canonical envelope bytes plus 200 overhead/safety units. The original request
reserves 3,000 output tokens, permits 10,000 raw response bytes and retains the
7,000-byte downstream child contribution budget. No bound was changed for replay.

## 5. Original generated StageResult

The response contains eight claims. All eight claim IDs and originating stages
match their application-defined identities. There are **17 primary evidence
reference occurrences**, all authorized, zero contradicting evidence references,
and zero child-lineage links, as expected for this analysis input.

| Claims | Primary references | Qualifications | Evidence result |
| --- | --- | --- | --- |
| 0–3 | One each | None | All valid |
| 4 | Four | None | All valid |
| 5 | One | None | All valid |
| 6 | Four | None | All valid |
| 7 | Four | One, containing four references | Primary references valid; qualification has three valid and one foreign ID |

The foreign reference occurs exactly once within the original generated result,
as the qualification's fourth reference. It is not reused in another claim,
contradiction or lineage field. All other evidence references pass set membership;
the union of primary references covers all four authorized source pieces.
The exact invalid string is unchanged between JSON text and decoded UUID value.
The decoder did not create, truncate or normalize a valid ID into this value.

The qualification is a scope limitation consistent with a bounded four-piece
request, rather than a verbatim extracted assertion. That is compatible with the
request's limited context, but it does not establish the associated claim's
semantic correctness or cure invalid provenance. No independent semantic
acceptance or human judgment was retained. Valid primary IDs are not, by
themselves, proof that a generated statement is grounded.

The JSON is complete and decodes successfully. Raw UTF-8 and canonical ASCII
sizes are both 4,302 bytes, below 10,000. Its downstream contribution plus wrapper
is 6,734 bytes, below 7,000. Completion usage is 2,130, below 3,000. Eight claims
use the profile's maximum claim count, and downstream byte headroom is only 266
bytes, but neither observation proves budget-induced reference corruption.

No raw finish-reason or reasoning-token metadata was retained by the four-call
recorder. Source inspection of
[`OpenAICompatibleProvider.execute`](../../../llm/openai_compatible.py) and
[`result_text`](../../../llm/bounded_http.py) shows that a successful strict return
requires non-null termination metadata and accepts only `stop`; truncation or byte
overflow would instead raise an output-limit error. That path, complete JSON and
known usage rule out observed truncation as this rejection's mechanism. A
reasoning-budget effect on token selection remains unobservable. There is no
evidence justifying larger output limits or a different reasoning setting.

## 6. Deterministic offline replay

Replay used the original response bytes, decoded original extraction/structure/
plan, original plan profile, `DigestionHandler.request`, `EvidenceIndex` and the
unchanged `validate_result`. Three repeated in-memory validations yielded exactly:

```text
DigestionError.category:       evidence_validation_failed
validation_diagnostic:        evidence_validation
validation_reason:            invalid_qualification_source
worker failure category:      invalid_reference
worker classification:        NON_RETRYABLE
```

Socket connection functions were disabled before imports. No provider inference,
HTTP request, credential operation, database constructor, authority transaction,
checkpoint write or replacement response was involved. The retained job ledger
was opened with SQLite read-only mode and `query_only=ON`. It confirms a successful
plan anchor, one failed chunk attempt, two unattempted cancelled reducers and a
cancelled final digest step. Its one committed manifest belongs to the plan
anchor, not an accepted analysis checkpoint.

Separate schema analysis validated the **original unchanged response** against
the current domain/provider schemas. A clearly non-production sensitivity probe
added the four-item allowlist as enums to three evidence-item schema locations on
an in-memory schema copy only. The existing Azure converter accepted that schema
copy, and local JSON-schema validation then rejected exactly the offending
qualification element. Each full/provider schema copy grew by 495 ASCII bytes.
This was not a production implementation, output repair or live provider test;
no modified result was generated or accepted. Empty allowlists, larger inventories
and actual service compatibility remain additional design cases.

## 7. Acceptance call path and exact rejection predicate

The original path is:

```text
Native ExtractionArtifact and immutable source reference
  -> build_plan / SourcePiece.evidence_id
  -> DigestionHandler.request
  -> ManagedSynthesisInference.render
  -> OpenAICompatibleProvider.execute / unchanged response content
  -> ManagedDigestionHandler / DigestionHandler.__call__
  -> validate_result: check_request, decode, size/stage/identity checks
  -> EvidenceIndex.resolve for every original source piece
  -> primary evidence and lineage checks
  -> qualification membership check: reject
  -> classify_digestion / classify_managed: invalid_reference, NON_RETRYABLE
```

For analysis, `permitted` maps the four computed source evidence IDs to their
validated `EvidenceRef` values. `inherited` is empty. The resulting
`allowed = set(permitted) | inherited` therefore contains exactly E1–E4.
[`validate_result`](../../../documents/digestion/validation.py) checks:

```python
if (not qualification.evidence_ids
        or len(qualification.text) > profile.max_claim_characters
        or len(set(qualification.evidence_ids)) != len(qualification.evidence_ids)
        or not set(qualification.evidence_ids) <= allowed):
    raise DigestionError(
        'evidence_validation_failed',
        diagnostic=ValidationDiagnostic.EVIDENCE_VALIDATION,
        reason=Reason.INVALID_QUALIFICATION_SOURCE,
    )
```

This is the rejecting branch expressed for this case; the implementation also
selects a separate `TEXT_LIMIT` reason when text length is the failing predicate.
Here the list is nonempty, text is within bounds and all four elements are unique.
Only the subset predicate is false: three references belong to `allowed`, one
does not. Primary references and original `EvidenceIndex` resolutions have
already succeeded.

`Qualification.evidence_ids: tuple[UUID, ...]` validates types and syntax, not a
particular request's provenance. That explains decoder acceptance followed by
semantic membership rejection. The validator is correct under G2. It rejects
before `Checkpoint` construction, inherited-summary acceptance and object commit.
No error category, source allowlist or acceptance order should be weakened.

## 8. Root-cause hypothesis matrix

| Hypothesis | Classification | Evidence, source and conclusion |
| --- | --- | --- |
| H1: model-generated invalid ID | **CONFIRMED at the returned-output boundary** | The foreign value first appears in retained provider content, is absent from hash-matched model inputs and is returned unchanged by provider content handling. `SourcePiece.evidence_id`, `render` and `decode` do not manufacture it. Internal generation reasoning is not retained. |
| H2: ambiguous ID guidance | **SUPPORTED BUT NOT PROVEN as a contributor** | `render` separates evidence, claim and stage roles and globally prohibits invented references. UUID syntax is shared, and exact copying/nested qualification guidance is implicit. This is a concrete improvement opportunity; it does not prove that ambiguity caused the error or that instruction changes will prevent recurrence. |
| H3: schema lacks allowlist constraint | **CONFIRMED** | `generation_schema` is static; `Qualification` specifies UUID syntax only; `provider_schema` removes format. Both schemas accept this original result. The dynamic-enum sensitivity probe rejects it locally. This is a generation constraint gap, not a reason to merge schema and provenance acceptance. |
| H4: extraction/planning mismatch | **RULED OUT for this run** | Source hash/reference checks, exact `build_plan` equality, four successful `EvidenceIndex.resolve` calls and matching rendered/validation ID sets establish a consistent chain. The bad ID has no alternate legitimate role in the retained inputs. |
| H5: serialization/canonicalization defect | **RULED OUT in the inspected application path** | Recorded/reconstructed generation-material hashes match. Sorting/escaping preserve all source ID values. The invalid reference is identical before/after `decode`, and response copies agree. Missing raw HTTP captures limit claims about external internals, not the demonstrated application behavior. |
| H6: qualification-specific generation weakness | **SUPPORTED BUT NOT PROVEN as a general tendency** | In this response all 17 primary reference occurrences are correct, while one of four qualification references is foreign. The localized symptom is confirmed; a single sample cannot establish a systematic qualification failure rate or prove other fields immune. |
| H7a: truncated/incomplete output | **RULED OUT as the observed mechanism** | Complete JSON, successful strict-adapter path, 4,302 response bytes and 2,130 completion tokens; the rejection is membership, not `output_limit`. `result_text` would reject reported truncation. |
| H7b: budget/reasoning pressure caused the bad ID | **INSUFFICIENT EVIDENCE** | The original request used low reasoning effort, eight claims and 6,734/7,000 child bytes. These are observations only. Reasoning-token details and internal generation decisions were not retained. No budget change follows from them. |

The confirmed proximate cause is one unauthorized generated evidence reference.
The confirmed permissive condition is structural schema acceptance without
dynamic membership constraints. Prompt-copying difficulty and qualification-local
generation behavior are plausible contributing factors. No defect in extraction,
ID construction or application rejection was demonstrated.

## 9. Wider G1/G2 risk assessment

| Area | Reach of this mechanism and existing boundary |
| --- | --- |
| Chunk analysis | Generated primary, contradictory and qualification references can all be syntactically valid but foreign. All are checked against source membership; this instance was qualification-local. |
| Structural/intermediate/root reduction | The same static output schema and validator are used. New direct references must come from the current child-derived allowlist; complete child lineage is separately mandatory. No live reducer behavior was observed in this run. |
| Qualification inheritance | `inherited_summary` and the reachable checkpoint graph retain original qualifications. Copying a child qualification verbatim into a new reducer claim is not equivalent to inheriting it through a valid child link. IDs appearing only in a child qualification are not automatically in the next stage's direct-reference allowlist. Renderer and validator implement the same restriction. |
| Conflict handling | Contradictory references and claim links have the same generation-versus-membership distinction. Proposition/contradiction propagation is application owned; no conflict-path failure was observed here. |
| Final digest | `DigestionHandler.__call__` revalidates accepted checkpoints in topological order before `make_digest`. Rejected output cannot become a valid digest through normal workflow progression. |
| Publication/retrieval | `publication.planning.accepted` requires a completed job and complete digest and reconstructs/revalidates the accepted graph. This failed job cannot publish through that path. Publication does not make generated references authoritative. |
| Grounded Q&A | `DocumentAnalysis` uses separate application citation IDs. Its static string schema likewise cannot enforce request-specific membership, but duplicate/foreign citations are explicitly rejected after decoding. The general copying risk applies; this particular qualification predicate is not the Q&A predicate. |

The related reducer inheritance constraint is already demonstrated by
`test_qualification_copy_is_not_equivalent_to_lineage_inheritance`; it is not a
new source-inventory mismatch discovered in this run. A remedy must not expand a
reducer's permitted set to every UUID visible in child material or remove
qualifications to avoid their validation. Preserve them through accepted lineage.
Source-ID validity also remains distinct from semantic support for prose.

## 10. Minimal corrective recommendations

These are proposals for a separately scoped engineering task. None was applied.

**R0 — Add the precise mixed-reference regression before changing generation.**
Extend `test_final_offline_azure_compatibility` and
`test_live_failure_observability` with valid primary references and a nested list
containing valid IDs plus one foreign but well-formed UUID, including a segment
blend. This targets the observed shape rather than claiming qualification
rejection is wholly untested. Accepted behavior should not change. There is no
prompt/token or provider effect, and test-only edits do not change the current
generation-contract hash. Another live attempt would still require a fresh
approval because the prior approval is consumed.

**R1 — Make the existing evidence rule explicit at generation time.**
In `ManagedSynthesisInference.render`, give every evidence-bearing field,
especially `claims[*].qualifications[*].evidence_ids`, an explicit instruction to
select complete, unchanged IDs from the **current** `allowed_evidence_ids`, never
compose UUID segments, and never use claim/stage IDs as source evidence. Clarify
that reducer qualification inheritance follows required child links; newly
emitted direct references must still be allowed at that stage. Preserve the
existing requirement to retain qualifications and conflicts.

Use a separately reviewed `StageProfile.template_version`/generation binding and
update generation-specific fixtures intentionally, while retaining the existing
domain schema and G2 predicates. Risk is changed model behavior, verbosity or
reducer copying decisions; clearer instructions are not a guarantee of compliant
generation. Regression requirements are role-distinction assertions, unchanged
domain rejection/coverage behavior, all-stage qualification inheritance and G1
size/admission checks. Prefer a few targeted sentences over repeating the full ID
inventory again. Additional instruction bytes consume prompt headroom and change
G1's measured base envelope; measure exact escaped sizes and plan identities
before accepting the change. Keep the existing token, byte, cost and retry
ceilings. This is provider-neutral guidance, although effects may differ by model.
Editing `managed.py` changes the generation-contract SHA-256; new plan/configuration
bindings and independent approval are required. Do not reuse old checkpoints as
compatible with a newly bound generation contract.

**R2 — Assess request-bound schema enums as a stronger generation constraint.**
Within the generation-schema/rendering boundary, consider request-specific enums
on primary, contradictory and qualification evidence items. Keep `StageResult`
decoding and strict G2 validation independent and unchanged. The local probe shows
that the present converter accepts four-item enums and rejects this unchanged
response at the exact foreign element. It does not establish live Azure
compatibility or successful semantic generation.

Risk includes empty allowlists, larger inventories, provider enum limits and
overconstraining reducers. The current converter rejects an empty enum; some
valid reducers have no directly allowed source IDs and preserve source evidence
only through lineage. Do not emit `enum=[]`, permit unrelated IDs, or silently
drop inherited qualifications to solve that case. Define and test an explicit
generation policy for it before implementation. Generic/prompt-only adapters and
strict adapters must retain the same application acceptance rules, with subset
conversion remaining in provider infrastructure.

The measured four-ID schema-only increase is **495 ASCII bytes per schema copy**;
the schema also appears in CONTROL, so complete escaped request growth exceeds
that single-copy figure and must be measured through the existing renderer.
No token-limit increase is proposed. Required tests cover all evidence fields,
empty/nonempty reducer sets, strict/generic capabilities, schema size and depth,
cardinality limits and unchanged G2 rejection. A production `managed.py` or schema
infrastructure change changes the generation digest and requires regenerated
configuration/approval. Treat R2 as a deliberate reliability enhancement rather
than a prerequisite for weakening the current validator.

**R3 — Preserve closed validation and successful-provider metadata in the L1 audit.**
The four-call recorder in `foundry_preflight.execute` retains response content,
hashes and usage but drops successful `GenerationResult` metadata; the job ledger
retains the broad failure category. Reuse existing typed validation diagnostics
and `ProviderResultMetadata.evidence()` at the evaluation handler/recorder boundary
to persist stage, closed reason and bounded location when available, plus sanitized
finish/usage/limit metadata. Prefer that small evaluator change over redesigning
the job ledger or exposing model text in errors. A precise application-error
location would require deliberate supplemental diagnostic plumbing; it is not
already present simply because the reason enum exists.

This improves future forensics but cannot correct generation. Risk is accidental
content/identifier leakage or a diagnostic exception masking the original error.
Tests must verify omission of forged/untyped fields, bounded index/path handling,
redaction, unchanged classification/settlement and single-attempt behavior. There
is no model prompt/token or provider request change from audit-only recording.
Nevertheless `foundry_preflight.py` is part of the launcher generation digest, so
editing it still requires a new digest, reviewed configuration and approval.

Renaming all evidence IDs, introducing nearest-match repair, deleting
qualifications, relaxing coverage, increasing budgets or adding paid correction
retries is not justified as a minimal response to this evidence.

## 11. Existing coverage and required regressions

Existing tests already exercise foreign qualification rejection:

- `test_final_offline_azure_compatibility.test_provider_valid_application_invalid`
  includes empty and foreign qualification sources for chunk, structural and root
  profiles, with valid surrounding primary fields.
- `test_live_failure_observability.test_application_reasons` expects
  `invalid_qualification_source`; its text-limit test distinguishes a text-bound
  failure from a source failure.
- `test_source_contracts` detects removal of the qualification membership
  predicate and changes to the qualification UUID type.
- Existing two-layer tests cover empty qualification sources; digestion and
  two-chunk integration tests cover retained qualifications, unresolved conflicts,
  publication, grounded citations, reuse and downstream failure barriers.
- G1 sizing tests and exact source-compatibility guards protect escaped child
  budgets and prevent admission changes from being mislabeled harmless.

The missing focused cases are a mixed valid/foreign qualification list with valid
primary references, a foreign segment-blended UUID in a late claim/list element,
and that precise fault passing schema checks but failing strict acceptance while
retaining paid accounting and preventing subsequent stages. Extend existing
fixtures using sanitized deterministic IDs; do not ship private response text.

Before another live evaluation, the engineering task should also verify valid
multi-reference qualification acceptance, duplicate/empty/foreign qualification
rejection, equivalent checks on primary/contradictory references, inherited-only
reducer source sets, reopening/checkpoint integrity, no publication after rejection,
zero retries, settled known usage and complete request sizing. Any enum proposal
needs dedicated capability/empty-set/size tests; any new prompt needs exact
generation-contract and compatibility expectations. No such tests were added here.

For this investigation, a network-denying guard was installed before pytest
collection; application settings isolation remained in place. Only existing
tests were run, using temporary synthetic authorities and authored offline
fixtures. Those fixtures were not substituted into the original-artifact replay.
The focused selection produced **35 passed, 275 deselected, 0 failures, 0 errors**
in **10.54 seconds**:

| Existing test module | Selected tests passed |
| --- | ---: |
| `test_final_offline_azure_compatibility` | 10 |
| `test_live_failure_observability` | 3 |
| `test_source_contracts` | 6 |
| `test_g1_source_compatibility` | 7 |
| `test_phase17h_two_chunk` | 9 |

Nine pytest warnings concern the existing `record_property`/JUnit xunit2
combination. They are reporting warnings, not evidence-validation failures.
No full suite, live test, model load or infrastructure validation was necessary.

## 12. Remaining uncertainties and investigation boundaries

The model's internal generation process, reasoning-token count, raw upstream
envelope and original HTTP wire bytes were not retained. Prompt wording or budget
pressure cannot be assigned causal weight from one response. Hash matching gives
strong evidence for the reconstructed generation inputs, not a packet capture.
No frequency estimate, live reducer behavior or guarantee that R1/R2 will complete
the hierarchy can be inferred. Semantic correctness of the generated claims was
not independently established by source-ID membership.

The original audit directory and its 17 files were immutable throughout. No
production authority was opened for mutation, no consumed approval was reused,
and no credential, signing, inference or cloud operation occurred. No replacement
output or hypothetical repaired result was constructed. The only schema change
was an explicitly labeled in-memory compatibility probe; production schemas were
unchanged. All pre-existing tracked and untracked repository files were preserved.
Only this requested permanent report was added. Documentation whitespace,
relative links, secret/private-path exclusions and final Git scope were reviewed;
no staging, commit or push occurred.

## 13. Next engineering task and Phase 17H status

Authorize a narrow offline generation-contract hardening task: first add the
mixed-reference regression, then implement/version the qualification-copying and
stage-local inheritance guidance, and assess whether request-bound enums warrant
a separate production change. Preserve source provenance, G1 sizing, G2 rejection,
checkpoint compatibility, provider-neutral architecture, zero automatic paid
retries and financial/security controls. Retain the original failed evidence.

That future generation change will change the generation-contract digest and
require fresh configuration/binding review and independent signing/execution
authorizations. Test-only changes do not themselves alter the current digest;
they still cannot revive a consumed approval. This investigation grants no
authority for another paid attempt.

**Phase 17H remains PARTIAL until the complete hierarchy, publication and grounded
Q&A pass separately authorized live validation.**
