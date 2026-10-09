# Phase 17G — Multi-User Security, Quotas & Cost Governance

Normalized implementation and finalization instructions from the operator.
Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`.
Work directly on master; expected baseline `76ec11c`, Phase 17F implementation.
The original operator prompt supplied 57 detailed sections; this artifact retains
the substantive contracts and the later continuation constraints, not a verbatim
transcript.

## Baseline and safety

Before implementation verify clean status, HEAD, five-commit history and diff
whitespace. Stop on unexpected state. Record external baseline inventory/hashes
under `/tmp/polymind-phase17g-baseline`. Read AGENTS.md, current README, relevant
Phase 8G/16/17A–17F reports/prompts, implementation, tests and consumers.
Preserve existing architecture and all earlier history. Never branch, stage,
commit, push, reset, stash, clean, merge, rebase, discard work or modify remote
resources. No Azure/AKS/Kubernetes mutations, Foundry calls/capacity changes,
cloud Chroma/Redis resets, identity provisioning or production database work.
Phase 17E live Foundry digestion remains BLOCKED/PENDING.

## Architecture and readiness assessment

Record existing authentication/protected paths, session propagation, legacy versus
document retrieval, publication generation/ownership boundaries, cross-owner
sharing, dense/BM25 constraints, inference admission/accounting, purge capabilities
and the smallest backward-compatible design before production edits.

Keep identity/authorization/governance independent of inference provider:
verified token -> immutable Principal -> authorization/scope -> owner/tenant
governance -> existing provider admission -> existing InferenceProvider -> usage
settlement -> final authorization -> response. Do not duplicate providers,
workflow scheduling, publication authority, memory or vector abstractions.

## Identity and authorization

Correct `/documents/analyze` protection first; cover new document/job/usage routes
and bounded mutation bodies. Preserve operational health/ready/metrics policy.
Support explicit disabled/static-bearer/OIDC modes without redefining legacy
variables or treating a shared bearer secret as a user identity. Unsafe mode
combinations fail validation; verification failures never downgrade modes.

Use maintained JWT cryptography, fixed issuer/audience/JWKS anchors, explicit
algorithm/key relationship, expiry/nbf, subject, required tenant and token-purpose
checks. Bound cached refresh/network behavior. Reject malformed/oversized tokens,
untrusted key URLs, wrong signatures/audiences/issuers, algorithm confusion and
self-declared privileges. Test local synthetic signing keys; no live IdP needed.

Derive canonical tenant/owner UUIDs from verified identity with versioned,
domain-separated mapping. Never accept HTTP scope overrides. Keep authentication
separate from durable authorization. Add a private local SQLite authority with
schema validation, short transactions, ownership references, grants, epochs,
tombstones/retention and bounded content-free audit records. Keep job schema.

Use deny-by-default actions for document, job, session, publication, usage and
tenant administration. Owners can share/revoke/delete; same-tenant registered
grantees can READ/ANALYZE only. Approved administrators require trusted issuer
roles plus operator mappings. Missing/foreign resources disclose no existence.

## Retrieval, sharing, memory and revocation

Sharing must use the original owner's accepted publication. Never relabel objects
or derive storage paths from client scope. For v1, mixed-owner selections may be
explicitly rejected. Authorization must constrain dense and sparse candidates
before ranking/top-k, then preserve RRF/reranker provenance and canonical citation
checks. Maintain generation pinning and immutable BM25 snapshots with no request
rebuild. Preserve existing accepted manifests/metadata; version incompatible
representations instead of rewriting rows or resetting collections.

Use immutable authorization snapshots and final revalidation of principal,
grants, epochs and tombstones. Define response-release versus revocation
acknowledgement semantics; future protected streaming output and persistence must
stop after revocation. Already emitted bytes cannot be recalled.

Legacy RAG is not automatically authorized by an authenticated request. Fail
closed in OIDC mode if private retrieval lacks authoritative scope. Propagate
trusted immutable context explicitly through applicable graph/streaming paths.
Derive effective memory keys from tenant+owner+visible session, covering file and
Redis read/write/delete. Do not adopt legacy unscoped history or expose internal
keys. Preserve visible API identities and legacy contracts where safe.

Keep publication preparation/activation/rollback/mutation behind explicit trusted
administration. Security tombstones and revoked grants override publication
history and rollback.

## Governance and pricing

Add narrow provider-neutral quota/pricing/reservation/accounting contracts.
Owner and tenant admission must be one durable atomic decision before provider
admission; no paid governed path may bypass it. Unsupported unbounded/unattributed
paths must refuse execution. Keep Phase 17C scheduling and Phase 17E admission.

Policies are operator supplied. Implement a small enforceable v1 set and state
unsupported quota dimensions honestly. Preserve attempt identity, idempotent
admission/settlement, and separately accountable genuine retries. No second retry
loop, model fallback to evade budgets, or release of potentially spent reservations.

Use a versioned, explicitly approved pricing catalog with provider/model/currency,
effective date, nonnegative decimal token prices and units. Unknown pricing fails
closed when monetary governance is required. Reserve conservative input/output
tokens and expense; do not promise a provider bill ceiling without proof.

Measured usage reconciles under the recorded catalog. Absent/partial usage stays
unknown/unsettled across crashes, cancellation and restarts; no TTL refund or
zero-usage fiction. Provider-admission rejection before upstream execution may
release unspent reservations. Budget denial makes no provider call and must not
erase prior checkpoints/expense. Owner usage is private; tenant detail requires
explicit administrative authority. Streaming without provable bounds/accounting
may be refused instead of bypassing budgets.

## Retention, privacy and readiness

Implement idempotent deletion/tombstone/purge tracking. Inventory content-bearing
references and preserve shared immutable objects/accepted manifests. No collection
reset or unsafe per-document deletion. Unsupported deletion adapters must retain
PURGE_PENDING/blocked state; never claim PURGED without reconciled proof.
Tombstones and minimal audit evidence survive deletion; cloud backups/providers
are not certified erased.

Audit authentication/authorization denials, grants, revocations, tombstones, purge,
admission denials and publication administration with bounded safe identifiers.
No tokens, raw claims, queries, prompts, source text, answers or embeddings in
audit/logs/metrics; no high-cardinality identity labels. Required mutation audit
failure must fail closed. `/health` remains liveness; `/ready` gates required
security/governance alongside existing dependencies without revealing secrets.

## Checkpoints and acceptance

G1 audit/design; G2 identity/authority; G3 sharing/retrieval/session isolation;
G4 governance/pricing/accounting; G5 retention/audit; G6 adversarial closure.
These are internal checkpoints, not roadmap phases or commits.

Test synthetic A/B users in tenant A and C in tenant B; owner access, cross-owner/
tenant denial, sharing/revocation, no resharing/deletion escalation, tombstones and
rollback precedence. Observe candidate sets and provider context, not just HTTP
status. Test cryptographic rejection/rotation cases, controlled revocation during
paused inference/streaming, concurrent owner/tenant 8-of-10 budget reservations,
idempotency/retries/unknown usage/crash recovery, and file/Redis session isolation.
Preserve prior 590-test baseline and meaningful Phase 17B–17F/API/provider/deployment
regressions. Perform self-review and separate pre-commit review; fix genuine defects.

Original validation scope included pytest, external-cache compileall, diff check,
Compose and available offline Helm/lint checks; record only measured outcomes.
Create prompt/report artifacts and minimally update README. Report exact files,
tests, architecture, compatibility changes, limitations, prohibited-action
confirmation and Phase 17H prerequisites. PASS requires every mandatory safety
gate supported; otherwise PARTIAL/BLOCKED. Do not start 17H/17I.

## Continuation: finalization without redundant execution

The operator subsequently required resuming the existing work, not restarting it.
Reuse historical successful results. Do not repeat completed tests/test files/
groups/full suite, cached Docker build, Compose/Helm/compile/lint checks or verified
file inspections. If evidence cannot be established, mark NOT VERIFIED.
Only a genuinely new, never-executed test may run individually. If code changed
after a test, explicitly state that the result predates the change.

Determine whether the final edits to governance/ledger.py, llm/admission.py,
security/authority.py, security/runtime.py and tests/unit/test_security_api.py
completed. Finish only unfinished documentation/review/report tasks. Preserve
OIDC legacy query/stream denial and PURGE_PENDING semantics. Do not conceal final
readiness or acceptance verification gaps.

At final handoff, perform only outstanding Git state/stat/whitespace checks,
list untracked additions separately, and leave everything unstaged/uncommitted.
The operator decides when to commit/push. Earlier passing tests alone do not
justify final PASS.
