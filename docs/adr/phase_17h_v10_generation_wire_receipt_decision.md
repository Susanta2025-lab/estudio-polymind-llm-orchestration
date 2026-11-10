# Phase 17H v10: generation-wire and durable decoding association

10 November 2026. Decision: additive immutable artifacts and existing fenced
manifest commitment. This supplements, and does not rewrite, the
[post-v9 assessment](phase_17h_post_v9_generation_wire_assessment.md).

## Responsibility and trust boundary

The model produces one `stage-proposal/1` object. Application code derives
request-local source and atomic child-pair tables, resolves explicit selections,
assigns canonical identities and returns `stage-result/1`. G2 and complete G1
child admission remain independent acceptance gates. No reference selection is
inferred, repaired, deduplicated or filled in. Enum membership does not establish
semantic support. Source authorization still comes from the verified extraction,
plan, authenticated scope and accepted child artifacts.

`E1..En` enumerate sorted authorized UUIDs. Authority is exactly v9's union of
current source pieces and immediate children's direct supporting/contradicting
IDs. Qualification-only inherited IDs do not expand it. `C1..Cm` enumerate full
(stage, claim) pairs in plan-child and accepted-claim order. There is no separate
model-facing choice of pair components. Application identity remains
`stable_id(str(request.stage_id), str(position))` with current-stage origins.

The table digest commits to `stage-decoder/1`, the complete canonical StageRequest
hash, sorted sources and ordered pairs. The request hash includes the profile,
stage, structural path, original evidence spans, complete child objects and their
ObjectRefs. The model copies a singleton request-binding value. This detects
transplantation across different requests; it is a consistency check, not
an authentication credential. The application-owned provider record and ledger
association establish where the bytes were received.

## Reused facilities and additive artifacts

No database/schema migration, checkpoint rewrite, new service or approval
credential is needed. The existing JobLedger supports multiple immutable
ObjectRefs in an atomically committed step manifest. IntentStore registers each
write under the current scope and lease/fence. LocalObjectStore writes/fsyncs a
private temporary file, atomically links without overwrite, checks idempotent
conflicts and fsyncs the directory. SQLiteJobLedger uses synchronous FULL and
commits the manifest, success state and dependent outbox activation together.

A v10 stage manifest is ordered:

1. Unchanged `synthesis-checkpoint/1` ObjectRef containing canonical StageResult.
2. `stage-decoding-receipt/1` ObjectRef.
3. `stage-provider-record/1` ObjectRef containing exact raw proposal text.

Historical stages retain their single checkpoint reference. This is an additive,
generation-specific manifest convention, not a change to canonical result or
checkpoint models. General job API tuple types remain compatible; consumers
assuming every synthesis manifest has exactly one member must recognize v10.
All repository readers are inspected/adapted through the shared durable handler.
Digest checkpoint references and ChildInput continue pointing only to canonical
checkpoints. Publication and retrieval receive no authoritative alias IDs.

The provider record binds plan ObjectRef, job/step, attempt/fence, request/table
hashes, managed configuration, full GenerationRequest hash, existing Foundry
audit request hash, raw response SHA-256 and raw text. The full generation hash
includes capability and transport limits. The audit hash uses the unchanged
provider recorder recipe, allowing direct comparison with `provider-calls.json`.
It is captured only from the actual provider return, under the handler's trusted
callback, after known usage settlement. Existing raw provider/usage evidence is
retained. The immutable object copy makes the new association independent of the
append-style evaluation audit file; it contains no headers or credentials.

The receipt binds that record's ObjectRef, canonical checkpoint ObjectRef,
request/table hashes, generation/audit hashes and canonical-result hash. It
contains hashes/references rather than another copy of the request or tables.
The tables are reconstructed from immutable parents and versioned code.

## Commitment and reopening

Execution ordering is: paid-call admission and provider execution; existing
usage settlement; fenced immutable raw record; strict wire validation and
construction; unchanged G2; inherited summary and complete G1 admission;
immutable checkpoint; immutable receipt; independent association verification;
worker inspection; atomic fenced ledger commit. Success/outbox activation happens
only at the last step. A receipt alone is never acceptance or inference authority.

Before consuming accepted child material, and during finalization/publication,
the handler reopens all accepted ancestors in topological order. It verifies
manifest arity/order, ObjectRef hashes and scope, plan identity, exact request
and tables, original successful attempt/fence, response hash and receipt links.
It decodes again, compares exact canonical bytes/hash and reruns G2, parent,
inherited-summary/proposition and complete G1 validation. Repeated checkpoint
resumes follow ledger-owned reuse edges, requiring the identical accepted
manifest at every hop, back to the original successful attempt. New job IDs do
not reassign or rewrite old provider evidence.

Managed execution compatibility fingerprints include all six local generation,
constructor, codec, sizing and workflow sources. Signed L1 configuration uses
`generation-inventory/2`, expanded from 15 to 25 files to include wire/receipts,
codec, identity functions, ledger/worker/storage and launcher/single-call binding.
All original inventory/1 bytes are frozen before transition. Old approvals and
configuration hashes cannot execute as v10; their evidence remains readable.

## Failure analysis and recovery policy

| Interruption or threat | Required result |
| --- | --- |
| Before provider response persistence | No canonical result/receipt/checkpoint; existing unknown-use obligations survive. No replacement paid attempt. |
| After provider/raw record persistence | Known usage remains settled; immutable bytes survive. No checkpoint without subsequent complete validation and commit. |
| During decoder validation | Invalid/incomplete proposal remains rejected; no speculative repair or downstream call. |
| After decoding, before checkpoint write/commit | No accepted stage; any raw/checkpoint objects are orphan candidates. |
| During receipt persistence | Atomic link exposes a complete verified object or no final object. Pending bytes are never readable through a valid manifest. |
| After receipt, before ledger commit | Receipt/checkpoint/raw objects remain unaccepted orphans; they cannot activate dependents. |
| After checkpoint manifest commit | Success and dependent outbox are durable together; duplicate delivery cannot claim the succeeded stage. |
| Process restart | Reopen/reconstruct/revalidate accepted associations. Existing one-attempt L1 policy expires interrupted work to terminal failure. |
| Duplicate workers | Existing claim and governance/admission logical-attempt controls prevent duplicate inference; duplicate committed delivery does no work. |
| Lease fencing | Every intent and commit checks current fence/lease/cancellation. A stale worker cannot commit its artifacts. |
| Old response against a different request | Singleton binding, record request/table hashes, plan/step identity and receipt comparison reject it. A bare binding string never authenticates raw bytes. |
| Repeated decoding | Pure construction returns identical canonical bytes, preserving order and identities. Immutable repeated writes return the same reference. |
| Partial/orphan receipt | Never inferred from object presence. Only the ledger manifest grants acceptance; existing orphan retention policy applies. |
| Generation mismatch | Current settings/profile/configuration/fingerprint checks deny execution; wire/decoder versions reject mixed receipts. |
| Mapping/artifact corruption | Recomputed table digest, raw/canonical hashes and scoped ObjectRef integrity checks fail closed. |

Recovery is conservative: it verifies accepted work and retains uncertain work;
it does not automatically adopt orphan proposals or reissue inference. A crash
can therefore leave a settled call with no accepted checkpoint. This is deliberate
preservation of zero paid retries, not a promise of exactly-once provider delivery
or automatic completion after every crash. Manual future authorization remains
necessary for any new attempt. Reusing already accepted complete checkpoints does
not execute inference or create settlements.

## Limits and consequences

Managed input 24,800, context 28,000, output reservation 3,000, complete child
7,000 and L1 four-call/no-retry/no-fallback policies remain. Both raw proposal and
expanded canonical result limits still apply. Receipt/raw-record storage is
additional bounded audit storage, outside model context and canonical child size.
Source projections reserve an additional conservative 64 bytes per source in
analysis planning; actual rendering is also checked before inference. Reduction
uses the existing conservative complete canonical child allocation. Exact
serialization and escaped/Unicode boundary regressions verify these bounds.

The strict converter is unchanged. Enums use its existing string/local-ref/anyOf
subset, with at most 128 keys per branch. Collection cardinalities and uniqueness
remain application-enforced because the converter rejects array-bound keywords.
No offline check establishes Azure acceptance of this exact schema, completion
sufficiency, semantic attribution or live model reliability. A separate manually
reviewed operator-preparation phase may assess a new controlled evaluation; this
decision authorizes no authentication, signing, approval consumption or inference.
