# Phase 17H post-v9 architecture review — task scope record

Received 9 November 2026; review continued 10 November 2026.
This is a clean scope record of the supplied major-phase task, not a replacement
for its detailed requirements or authorization boundaries.

Review the completed `managed-prompt/9` baseline at HEAD
`6e0319e29984ad019edced0e076b3b0a4ae8c007` plus preserved uncommitted work.
Expected generation SHA-256:
`f270aa81cbd5764d2b4739bf3ac3692653b1fe4c8ffbd67860e642137cb2579d`.
Read AGENTS.md, the complete v9 engineering report, relevant v5-v8 engineering
and controlled execution reports, and the current Foundry runbook. Inspect actual
generation/conversion/storage/planning/sizing/durable validation, publication,
retrieval, Q&A, historical fixtures and consumers before any production edit.

Begin with responsibility ownership, not another prompt revision. Investigate
whether application code should own current stage and positional claim identity,
original-source reference resolution and exact immediate-child pair resolution,
while the model owns substantive content and justified evidence selections.
Distinguish historical wrong origins, invalid stage/claim pairings and the v8
foreign source UUID; do not infer a single internal model cause. Preserve v9's
bounded request-specific source-enum correction, generic StageResult, G1/G2 and
historical v5-v9 contracts.

Inspect public source implementations and documentation for RAPTOR, wdoc,
LangChain and prakash22-26/ai-document-assistant. Identify exact files/functions,
application versus model ownership, reusable principles, compatibility, complexity,
call/token implications and licenses. Prefer principles over copied code or new
dependencies. Record limitations where source access is unavailable.

Compare unchanged v9, stronger schema constraints, short source references,
atomic child-pair references, a separate generation-wire model and adaptive
hierarchical map-reduce. Assess reliability, provenance, lineage, semantic risk,
complexity, token efficiency, provider/historical compatibility, governance,
testability and migration risk. Create an initial architecture assessment and
perform a separate critical self-review before selecting any implementation.

Mappings must be deterministic from explicitly bound immutable authorized inputs,
isolated between requests, stable on recovery and auditable. Unknown, malformed,
foreign, duplicate or omitted selections must fail. Never repair UUID fragments,
guess evidence, attach all child claims, invent missing claims, hide incorrect
attribution or relax independent validation. Preserve source offsets, qualification
and contradiction provenance, canonical publication and grounded citations.

Implement only a bounded compatible improvement if justified. Changed generation
behavior needs a fresh version such as `managed-prompt/10`; freeze complete v9
source/fingerprints first. Keep stored StageResult semantics. If implementation
requires redesigning durable storage, approval binding, canonical publication or
the controlled benchmark, defer it and document the separate decision. Do not
automatically implement every investigated alternative.

The controlled L1 remains chunk analysis, first reducer, root reducer, grounded
Q&A: maximum four paid calls, zero automatic paid retries, no model fallback.
Preserve 24,800 managed input allocation, 28,000 complete context, 7,000 complete
child bytes and 3,000 output-token reservation. Evaluate ordinary production
call reductions separately. Measure real production serialization/builders across
all four profiles, empty/boundary source sets, one/two children, escaping/Unicode,
maximum child material and raw/canonical expansion. Bytes are not provider billing.

For an implementation, add permanent reference/identity/lineage, schema/transport,
historical compatibility, durable failure/recovery, no publication/Q&A after
failure, settlement, no-retry/fallback and quality regressions. Run focused/full
offline tests under the existing network guard and disposable stores, Ruff,
scoped mypy, compilation, applicable Compose checks and git diff --check.
Assess an already available local model without downloading/installing one; keep
deterministic correctness, local behavior and exact Azure compliance separate.

No paid inference, live authentication, credential retrieval, private-key access,
RSA operator signing, approval creation/consumption, cloud mutation, authority or
historical settlement/replay changes, new Kubernetes resources or Git mutation
is authorized. Do not stage, commit, push, reset, switch branches or alter remote
state. Preserve prior untracked work and historical reports/audit evidence.

Create the permanent explanatory report at
`docs/codex/reports/phase_17h_post_v9_architecture_review_and_inference_simplification.md`.
Return one of the supplied PASS-with-hardening, PASS-with-deferral or BLOCKED
outcomes with exact validation evidence, final file manifest, unchanged/new
generation fingerprint, next Azure prerequisites and final Git status. Explicitly
distinguish engineering confidence from live model compliance and end with the
required NO staging/commit/push/Azure/signing/consumption declarations.
