# Phase 17H–L: application-owned deterministic identifiers

Status: **Proposed / Under Review — assessment only**. Date: 2026-10-22.
No production contract migration is implemented or approved.

## Context and decision

Keep the current full `StageResult` interface for the next separately authorized
diagnostic experiment. Attempt 4's exact failure remains UNKNOWN. Current evidence
does not justify attributing its failure to identifier copying, or replacing the
interface before collecting a rule-level diagnostic. A semantic-proposal prototype
is conditional on a future live response implicating identity/reference copying,
or an independently reviewed offline evaluation demonstrating a substantial
advantage sufficient to justify explicit operator approval.

The application already computes stage IDs and `claim_ids_in_order` and supplies
exact source UUIDs and child pairs. Option A asks the model to reproduce them. It
is implemented, tested, compatible with durable checkpoints and governed approval
bindings, but cannot enforce deterministic identity or reference membership through
the Azure structural schema alone. A single incorrect generated identifier rejects
the stage. UUIDs consume completion tokens and bytes; token savings cannot be
estimated exactly from character counts without the deployment's tokenizer.

## Alternatives

| Concern | A: complete StageResult | B: semantic proposal with selected indices |
| --- | --- | --- |
| Application metadata | Model copies schema/stage/kind/claim/origin identifiers | Trusted application supplies metadata and computes claim IDs |
| References | Model copies allowed UUIDs and exact child pairs | Model selects trusted source-table and child-pair-table indices |
| Security | Current membership, scope and immutable artifact checks | Same checks plus strict index validation and immutable mapping binding |
| Semantic responsibility | Claim text/kind/status, support and provenance selections | Unchanged; application cannot infer missing selections |
| Failure modes | Wrong UUID/copy/order/membership | Wrong/out-of-range/duplicate index or wrong valid selection |
| Durable storage | Existing StageResult/checkpoints | Construct same canonical StageResult, with new proposal provenance/version binding |
| Compatibility | Existing evidence applies directly | Requires new evidence; past model acceptance evidence cannot be transferred |
| Complexity | Existing implementation | Moderate to high: tables, schema, fingerprints, governance, replay, rollback |

A future B contract could be `stage-proposal/1`, with `managed-prompt/4` or a later
unused version dedicated to that migration, and a distinct managed-generation
profile. The current inactive prompt clarification already reserves
`managed-prompt/4`; do not conflate its wording-only release with an identifier
migration. Prefer `managed-prompt/5` if both proceed.

## Deterministic construction and no-bypass boundary

After bounded provider decoding, validate the entire proposal before constructing
anything durable. Indices must be integers (reject booleans/coercions), nonnegative,
within bound, unique in each selected array and explicitly present as selected
relationships. Source tables come only from authorized current source pieces and
immediate child direct evidence; child-link tables contain exact supplied
stage/claim pairs. Freeze ordering and bind both tables and their digests into the
request, audit, plan and proposal fingerprint. A canonical sorted UUID source
order and stable supplied-child/claim order avoid map-iteration dependence.

Compute `stable_id(str(stage_id), str(position))` for claims in the exact validated
proposal array order; never reorder, deduplicate or drop a proposed claim. Resolve
only relationships selected by the model. Supply trusted schema/stage/kind/origin
fields, construct StageResult, then run **unchanged** `validate_result()`, canonical
size checks and checkpoint verification. Reject any error. Do not repair unsupported
facts, insert missing coverage, infer a source, select omitted lineage, promote
ancestor references or reinterpret unknown indices. This is an explicit new
construction contract, not an output-repair mechanism for old StageResult output.

Qualification sources need their own explicit selections into the currently allowed
direct table. Empty qualification references remain invalid. Contradicting evidence
selections remain distinct from supporting references. Preserve all required child
links and immutable inherited qualifications/propositions. Index tables must never
expose another tenant/document or be resolved against a later table snapshot.
Shorter references do not make a semantically wrong valid selection correct.

## Cost, coverage and profile implications

Source and child indices reduce output UUID strings but move mapping descriptions
into input. For a UUID string, its quoted compact JSON scalar uses 38 bytes; index
0 uses 1 byte, before schema/field overhead. A child pair with two UUIDs has at
least 76 bytes of scalar content versus a short index, excluding field names and
braces. These arithmetic differences are not an end-to-end measured saving or
proof of lower failure probability. Dense source tables, schema field names,
qualification references and prompt instructions also have costs. Full canonical
StageResult storage is still unchanged in size, so its 10,000-byte ceiling remains.
A shorter generation can still fail after deterministic construction.

Chunk analysis selects source indices; all required sources must be covered when
analyzed. Unavailable analysis still emits no claims and nonempty limitations.
Intermediate, structural and root reducers select immediate child pairs, preserving
every required link across claims, with exact current direct evidence membership.
A source-free fact cannot be made supported by constructing an ID. Root ancestor
qualification copying remains prohibited when not directly allowed. Empty child
claim sets and partial/unavailable children need explicit witnesses; an index-based
interface must not accidentally require an unavailable source or erase its limits.

Choosing indices plausibly removes UUID syntax/copying and metadata manufacture,
but errors can relocate to wrong valid selections, table order or omitted lineage.
No observed live acceptance rate comparison exists. A prototype must measure both
selection correctness and rejection classes, not just JSON-valid or in-range output.

## Lower-risk intermediate alternative

Request-specific UUID enums could constrain stage/claim/origin IDs and evidence
membership without changing stored StageResult. They retain output UUID overhead
and still cannot generally bind claim position, child stage/claim pairing, coverage,
or provenance/support semantics. Independent enums for child stage and claim IDs
could allow invalid cross-pairs. Per-request schemas introduce schema construction,
size/capability, cache, fingerprint and approval changes, and must not be described
as the currently frozen provider schema. Enum limits and service behavior would
need separate verification; no cloud discovery was performed. This is potentially
less storage migration than B, but is not automatically lower overall risk.

## Conditional migration and rollback plan

1. Establish a trigger from sanitized live diagnostic evidence or a substantial
   independently reviewed offline advantage. Obtain separate prototype approval.
2. Version a proposal schema, template, managed-generation capability/profile and
   deterministic constructor. Bind exact trusted mapping tables to requests.
3. Build offline tests for all four profiles, malformed/negative/boolean/overflow
   indices, duplicate selections, wrong-but-valid selections, order stability,
   qualification/contradiction provenance, source/child coverage, adversarial text,
   tenant/document boundaries, construction byte overflow and canonical round trips.
4. Add durable restart/cancellation/replay and accounting-error tests; preserve
   settlement before downstream rejection. Never invoke inference to fix output.
5. Retain old StageResult/checkpoint readers. Isolate new plans by profile/config
   fingerprints; do not rewrite existing checkpoints or silently resume an old
   plan under the new constructor. Additive sanitized provenance must distinguish
   proposal validation from final domain acceptance without retaining raw content.
6. Recompute all authoritative fingerprints, payload and schema bindings. Previous
   Phase 17H–L evidence remains historical for A; it is not evidence of B's model
   compliance. Obtain fresh operator approval for any governed live comparison;
   prior signatures cannot authorize changed code/schema/mapping tables.
7. Evaluate accepted-stage rate, reference-selection accuracy, token/byte cost,
   rejection reasons and restart behavior. Promote only after review. Rollback by
   selecting the old profile for new plans and using each immutable plan's matching
   executor; never reinterpret already selected indices under another table.

This task performs none of those production steps. Phase 17H remains PARTIAL.
