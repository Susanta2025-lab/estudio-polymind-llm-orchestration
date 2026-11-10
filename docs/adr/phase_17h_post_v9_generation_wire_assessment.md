# Post-v9 generation responsibility assessment

Date: 10 November 2026. Status: design reviewed; implementation deferred.
This assessment was written before any production edit. No production edit is
selected. The [final review](../codex/reports/phase_17h_post_v9_architecture_review_and_inference_simplification.md)
records research, measurements, verification and disposition. Proposed formats in
this document are design examples, not implemented capabilities.

## Baseline and execution boundary

The working baseline is HEAD `6e0319e29984ad019edced0e076b3b0a4ae8c007`
plus the existing uncommitted v8/v9 implementation. Entry status has 16 modified
tracked files and 42 untracked files. V9 is `managed-prompt/9`, generation digest
`f270aa81cbd5764d2b4739bf3ac3692653b1fe4c8ffbd67860e642137cb2579d`.
The complete v9 report was read. Its 2,206-test result is historical until a fresh
run completes. Existing files were inventoried by SHA-256 outside the repository.

Native extraction produces scoped immutable original evidence. Deterministic
planning assigns chunk/reduction IDs and a complete fixed DAG. Managed generation
renders a StageRequest through the provider-neutral GenerationRequest port.
GovernedExecution reserves/admit/settles usage around provider execution; it
does not decide evidence acceptance. The durable handler applies independent
G2 result validation and G1 complete child-material admission before committing
a canonical Checkpoint. Finalization reopens and revalidates the accepted graph.
Publication independently reconstructs that graph and indexes original source
excerpts. Pinned retrieval resolves citations back to original offsets; grounded
Q&A selects application citation IDs and retains `semantic_support=not_evaluated`.

The hierarchical digestion executor is the existing durable fixed-plan worker,
not a second LangGraph workflow. The conversational application also has LangGraph;
that is a different boundary. Neither framework needs replacement for this work.

## Observed failures and responsibilities

The v5 reducer had eight correct positional claim IDs and eight child-stage
origins instead of current-stage origins. Corrected child sizing exposed this
independent identity failure; it did not make the response valid. V7 root had
eight correct current identities but paired the immediate reducer stage with
eight chunk claim IDs. V8 chunk had a foreign direct source UUID with segments
matching two authorized IDs; the intended citation remains unknown. These are
different observable violations, not proof of one internal model cause.

V9 prevents foreign original-source values in a schema-conforming strict
response, including qualification and contradictory evidence. Its shared bounded
enum and independent G2 are preserved. Exact live Azure acceptance of this new
schema remains unverified. Prompt-only modes, current/positional identities,
atomic child-pair membership, coverage and semantic attribution remain separate
risks. Short keys would change the error domain; they would not prove entailment.

| Responsibility | Current owner | Recommended owner |
| --- | --- | --- |
| Source scope, document/version, extraction spans | Application | Application, unchanged |
| Stage ID and ordered claim UUID candidates | Application computes; model reproduces | Application constructs canonical identities |
| Claim content, kind, status, stance, subject | Model; application validates contracts | Model, unchanged |
| Direct supporting/contradicting selections | Model copies original UUIDs | Model selects scoped source keys |
| Qualification text and explicit direct evidence | Model | Model selects source keys; application resolves |
| Immediate-child pair selections | Model independently emits pair components | Model selects atomic child-pair keys |
| Child qualification/proposition preservation | Application graph and inherited metadata | Application, unchanged |
| Coverage, original text resolution, publication authorization | Application | Application, unchanged |
| Semantic support for selected citations | Not established by G2 | Independent quality review, still necessary |

## Research that informs the boundary

Read-only public source was inspected at fixed commits, including implementation,
not only README prose. The final report gives immutable file/function links.

RAPTOR's tree builder constructs node indices and child-index sets in Python;
the summarizer returns text. This supports application ownership of identity and
topology. Its cluster membership is group-level provenance, not justified
claim-level evidence; automatically linking every PolyMind claim to a cluster's
sources would weaken the existing contract. Its clustering/embedding dependency
stack and retry policy are unnecessary here.

wdoc performs sequential chunk summaries with previous-summary context and
optional recursive condensation; intermediate summaries and embeddings are
reused. Its explicit query methods use original loaded documents for retrieval
rather than treating a summary as original evidence; combined initialization's
switch log does not by itself establish execution of a query. At the inspected
revision its summary routine also appends missing page citations from chunk
metadata. That behavior must not be imported into PolyMind: it could conceal a
missing model selection. Its caching, retry and context heuristics are not
financial/governance substitutes.

LangChain map-reduce constructs new Document objects from model text and copies
input metadata in application code. Its reducer splits according to a length
function and collapses only while oversized. Its default collapsed metadata
concatenates values as strings, which is unsuitable for exact typed ClaimLink
pairs. Structured parsers check output types; they do not establish source authority.
These are design principles to adapt without adopting the classic chain framework.

AI Document Assistant has one injected service behind Streamlit and FastAPI,
programmatic page/chunk metadata in Chroma, and a small retrieve/answer graph.
Summarization uses a direct path for small documents and batched map/reduce for
larger ones. Its answer source list is built from retrieved pages, rather than
independently validating citations for each answer statement. Its simplicity is
useful; its provenance and multi-user controls are not equivalent to PolyMind's.
No license file was found in the inspected tree; do not copy its implementation.
RAPTOR/LangChain are MIT; wdoc is AGPL-3.0. No external code or dependency is added.

## Candidate mapping and wire design

Recommend one new generation contract, provisionally `managed-prompt/10` with
`stage-proposal/1`, and one small deterministic constructor at the existing
managed/domain boundary. Keep stored `stage-result/1`, Checkpoint semantics,
publication and Q&A interfaces. Do not add a parallel orchestration framework.
Version numbers here are proposals only; v10 is not activated or fingerprinted.

Use exact string keys `E1`, `E2`, ... and `C1`, `C2`, ... rather than JSON numeric
indices. Typed namespaces avoid source/child confusion, remain readable in audit,
and fit the existing converter's string-enum subset. Integer indices are slightly
smaller but need exact type checks against booleans/floats/numeric-string coercion;
the current converter deliberately cannot express range/array uniqueness rules.
No key normalization, trimming, case folding, fuzzy matching or prefix parsing.

The source table is the sorted unique union of SourcePiece.evidence_id() and
immediate-child direct supporting/contradicting evidence IDs, exactly as v9 and
G2 independently derive it. Qualification-only ancestor references stay inherited
through lineage and do not create new direct authority. A child-pair table is
enumerated in immutable Plan node.children order, then validated child claims'
stored array order. Each entry resolves to one exact `(stage_id, claim_id)` pair.
Never enumerate sets, database row-return order or completion-arrival order.

Derive tables from a fully validated StageRequest, verified plan/extraction and
accepted immutable child ObjectRefs. Maintain immutable tuples, no global cache
or mutable dictionary shared across requests. Bind the table recipe version,
scoped plan and stage, managed configuration, complete request fingerprint and
ordered child artifact hashes to a reference manifest digest. On recovery,
reconstruct and compare the manifest before decoding; never rebuild it from a
model response or current vector database. A Plan alone cannot enumerate future
child claims: their accepted results and hashes are necessary immutable inputs.

Crucially, **bare E1/C1 values are not globally request-specific**. Two requests
can both authorize E1 for different objects. A decoder receiving only raw JSON
and a table cannot distinguish a response transplanted from another request
when its keys overlap. Rejecting only E99 does not meet cross-request isolation.
Bind a verified response envelope to the exact request/manifest. For detached
wire replay, require an exact request-binding field (singleton schema value,
checked before resolution), or retain an immutable application-issued receipt
associating raw response hash with that request manifest. The latter must never
be fabricated for arbitrary detached bytes. A binding hash is a consistency
check, not an authorization credential or proof of model intent. A wrong valid
key chosen under the right binding remains a semantic error.

Illustrative payload, with the verified request binding carried by the proposal
envelope/receipt rather than an unbound global key table:

```json
{
  "outcome": "analyzed",
  "claims": [{
    "text": "The stated limit applies only in the tested regime.",
    "kind": "fact", "status": "supported", "subject": null,
    "stance": "unknown", "evidence_refs": ["E2"],
    "contradicting_evidence_refs": [],
    "qualifications": [{"text": "Only the tested regime is covered.", "evidence_refs": ["E2"]}],
    "child_refs": ["C1"]
  }],
  "open_questions": [], "limitations": []
}
```

The example is a reducer shape; a chunk cannot select C1. The actual production
schema must explicitly specify all required fields and binding/version semantics,
including empty tables, rather than treating this illustration as a complete
approved schema. The application supplies schema_version, stage_id and kind,
assigns claim_id=`stable_id(str(request.stage_id), str(position))`, and sets every
originating_stage to the same request.stage_id. Positions are the exact generated
array order. No reordering, deduplication or missing claims are allowed.

The decoder first bounds raw bytes, rejects duplicate JSON keys and extra/missing
fields, checks the wire contract and request binding, validates all collection,
string and reference types, validates exact membership/within-array uniqueness,
and resolves only explicit model selections. It constructs a fresh canonical
StageResult and invokes unchanged independent G2. Canonical byte limits and the
actual complete child wrapper are checked independently before checkpoint
commit. Unknown/malformed/cross-scope keys, grandchild references, mixed source
UUID fragments, claim/stage IDs as sources and omitted coverage all fail. No
empty selections are filled from the table; no parent claims receive all child
links automatically. The model must still make justified selections.

Qualification source references resolve through the same authorized table.
There is no new canonical qualification-lineage field. Qualifiers inherited via
selected child claims retain their original text/references in accepted historical
checkpoints; inherited_summary and final graph traversal retain them. New direct
qualification evidence needs explicit selections. Supporting and contradicting
arrays remain distinct even when an ID legitimately appears in both roles.

## Independent G1/G2 and compatibility

Preserve G1's complete escaped ChildInput accounting, 7,000 bytes per child,
24,800 managed input bytes, 28,000 context and 3,000 reserved output tokens.
Raw proposal bytes can be much smaller than reconstructed canonical bytes;
do not substitute wire size for StageResult or child admission. Keep existing
10,000 raw and canonical response ceilings. Measure actual system/data/schema
and HTTP serialization across all four profiles; no speculative fixed allowance.

Do not route historical StageResult bytes through the new decoder, repair old
IDs, rewrite accepted checkpoints or resume old plans with a new profile. Freeze
the complete v9 source byte-for-byte and verify its existing fingerprints before
any active transition. Preserve v5-v9 fixtures and historical approvals verbatim.
Add explicit v9-to-v10 refusal cases alongside historical readability tests.
New decoder sources must enter the generation digest's source inventory; an
unhashed imported decoder would leave approval binding incomplete. Existing
15-file inventory and LaunchConfiguration refuse stale code bindings today.

Publication continues consuming canonical evidence and original text only.
E/C keys never become persistent citation authority, vector IDs or Q&A citations.
Resolve source UUIDs to the existing scoped EvidenceRef, including its exact
document/extraction/block spans. No source meaning or offsets are regenerated.

## Simplification and calls

Removing output current IDs and pair components eliminates the copying
instructions, claim_ids_in_order list and repeated source/child UUIDs from the
model-facing projection. A minimal child view can expose substantive claims,
their local source keys and inherited qualification/conflict context; full
canonical wrappers remain authoritative application objects. Do not remove
qualifiers or contradictory content merely to shrink input. Artifact refs can
stay out of model output while still binding the application request manifest.

The planner currently creates a reducer even for one child at each structural
unit and at root. A single-child reducer can provide compression or a distinct
section/document synthesis, but identity-only wrapping is not inherently semantic
work. For a future new production planning policy, consider direct analysis plus
retrieval for small documents, one reduction for medium documents and bounded
recursive fan-in when the actual envelope requires it. Collapse empty structural
wrappers in the plan rather than inventing reducer claims. Reuse accepted
intermediate summaries under exact plan/model/prompt/source hashes and current
authorization; never a global content-only cross-tenant cache. These choices
change DAG/stage IDs, cost reservations and publication root expectations and
need separate review. Existing L1 stays chunk, first reducer, root, Q&A: maximum
four paid calls, zero retries, no fallback. No deterministic fake reducer may
silently replace its semantic benchmark call.

## Separate critical design review and decision

The following findings were evaluated after the initial design was formulated:

1. Local names alone do not prove request isolation. A table digest stored beside
   arbitrary response bytes does not prove those bytes came from that request.
   Envelope/receipt provenance must be specified and replay tested independently.
2. Current Checkpoint stores plan_hash, parents, canonical result and inherited
   summaries/propositions. It has no raw-proposal/table/decoder receipt link.
   The provider recorder stores raw response/request hashes, but no explicit
   proposal-to-canonical commitment. Existing v9 reconstruction is sufficient
   for the current representation; do not silently claim it already specifies
   the new two-representation audit contract.
3. There is a potentially bounded **no checkpoint migration** design: reconstruct
   tables from plan/child refs and versioned code, retain an additive immutable
   per-call receipt outside canonical Checkpoint, and independently reproduce the
   result. This is preferred over changing storage. It still needs a reviewed
   receipt schema, accepted-checkpoint association, orphan/crash behavior,
   idempotent restart and generation-inventory binding. A different design embeds
   receipt refs in a new checkpoint version; that is explicitly outside this task.
4. Wire enums do not establish semantic grounding, coverage, qualifier support or
   current source authorization. Independent G2 and EvidenceIndex stay mandatory.
5. Canonical expansion can fail after paid usage is known. Settle provider usage
   first, preserve raw capture, then reject without another call or checkpoint.
6. Automatic inheritance of every source/pair would launder provenance. Reject
   missing selections even when application code could guess the intended source.
7. Per-field stage/claim enums permit unauthorized cross-pairs. Use atomic pair
   keys; do not introduce deep tuple-union schemas merely to retain opaque IDs.
8. Mutable table caches, arrival-order numbering, qualification-only authority
   expansion and output-order sorting would violate recovery or provenance rules.
9. Strict provider support for the proposed exact schema composition, refusals
   and completion sufficiency remain unobserved. No offline suite can establish
   the deployment's exact model behavior.

**Decision:** recommend the small wire/constructor boundary, but defer its active
implementation until the proposal/manifest/receipt replay contract is independently
reviewed as an explicit design decision. This is a broader generation-to-audit
binding change than a source-enum extension. The task expressly requires deferral
where durable storage/approval binding must be redesigned; no checkpoint rewrite
or new approval fields are undertaken here. The no-migration receipt alternative
should be resolved first; this review does not claim storage migration is
intrinsically necessary or that the recommended constructor is impossible.

Do not introduce another intermediate prompt-only release just to make progress:
singleton origin restrictions are a useful fallback option, but preserve most
bookkeeping/output costs and would immediately be superseded by the proposed wire
contract. Keep v9 active, including its source enums, while reviewing the coherent
proposal migration. No new generation version is assigned in this task.

Selected scope is source-level research, architectural responsibility/design
analysis, measured unchanged-v9 envelopes, fresh baseline offline verification,
and permanent decision/report artifacts. Decoder, wire schema, reference receipts,
active identity assignment, prompt/schema changes, adaptive planning, Q&A changes,
new dependencies/frameworks and all live evaluation are explicitly deferred.
