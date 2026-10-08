# Phase 17F — RAG Publication, Provenance & Interactive Document Analysis

Finalized implementation prompt, organized by contract from the operator's Phase
17F instructions. Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`.
Work directly on `master`. Expected initial HEAD: `cb70b26` (docs: refresh technology
badges). Preserve `94945f0` and `cb70b26`, the intentional README refresh after
`dce3e6b` (17A–17E implementation).

## Baseline and operator policy

Before editing run `git status --short --branch`, `git rev-parse HEAD`, and
`git log --oneline -5`. Stop implementation on an unexpected HEAD or dirty tree.
Record starting HEAD, status, tracked/unignored inventory, hashes of likely changed
files and initial tracked diff stat in `/tmp/polymind-phase17f-baseline`.
Do not branch, commit, push, merge, rebase, reset, stash, clean, restore unrelated
files, rewrite history, modify GitHub or remote state. All changes remain for review.

Read root AGENTS.md, CURRENT README, reports 8G, 16, 17A–17E, and finalized prompts
17A–17E. Inspect actual documents/digestion/jobs, RAG/vector/Chroma/factory/ingest/
admin/BM25/dense/hybrid/RRF/reranker/chunking/embeddings, graph/source assembly,
API query/stream/readiness, settings, inference and memory, their tests and consumers.
Preserve architecture and backward compatibility; use the smallest sound design.

Phase 16 is CLOSED/PASS. 17A–17E application contracts PASS. Phase 17E live Azure
Foundry document digestion remains **BLOCKED / pending**, with missing endpoint,
model map, provider/key configuration and **zero live calls**. Do not hide that gate,
retrieve credentials, fabricate success or require live inference for 17F.

## Central invariant and ownership

Retrieval representation is not source authority. Summaries, generated claims,
embeddings, BM25 tokens and synthetic retrieval text may improve discovery but
cannot masquerade as source text. Resolve user citations through publication
provenance -> document/version -> canonical extraction -> source block/span ->
EvidenceRef -> immutable original artifact. Source/derived classifications must
be explicit. Chroma remains derived retrieval state; ObjectStore owns canonical
artifacts; JobLedger owns document workflow; Redis/file memory owns conversations.

Preserve provider-neutral InferenceProvider, existing dense + BM25 + RRF + cross-
encoder RAG, read-only serving versus administrative vector access, and API/NDJSON
contracts. Do not simply call legacy rag.ingest and declare publication complete.

## Scope and explicit exclusions

Implement publication models, deterministic records/chunks, generations, immutable
manifests/provenance, candidate/active state, dense and sparse integration, coherent
activation, fencing, request pinning, stale-replica readiness, durable recovery,
idempotency, reprocessing, supersession, revocation, validated rollback, canonical
citations, selected-document interactive analysis, quality policy, legacy
compatibility, crash tests, documentation and a truthful report.

Do not implement 17G identity/authorization/tenant isolation/quotas/billing/cost or
retention governance, 17H certification, 17I users, public uploads, OCR/image
understanding, Azure Blob, distributed production job DB/queue, Kafka/Celery/new
workflow engine/vector database/RAG framework, Azure provisioning, AKS/HPA/Redis/
Chroma infrastructure changes, self-hosted vLLM, GPU provisioning, or Phase 18.
No Azure/Foundry-capacity/Kubernetes/cloud Chroma mutation or restart is allowed.
Use local/fake/in-memory dependencies and synthetic data only.

## Publication design and semantics

Before production edits evaluate actual Chroma capabilities: generation-labelled
rows with pre-top-k filters, blue/green collections, or another narrow compatible
mechanism. Explain choice, alternatives, availability, rollback, migration and
legacy implications. No ordinary destructive reset.

Immutable versioned models must represent generation/corpus identity, document and
version, extraction, accepted digest/hash, record inventory/material/classification,
evidence/provenance, retrieval/embedding profile, compatibility fingerprint,
expected predecessor, supersession/revocation and durable acceptance state.
Manifests belong in ObjectStore; Chroma metadata is bounded lookup data, not the
complete audit graph. Display source/chunk fields never confer evidence authority.

Prepare deterministic candidate -> validate manifest -> write dense incrementally
-> verify exact inventory -> verify sparse reconstructability -> mark READY ->
fenced logical activation. Any pre-activation failure retains the prior generation.
Candidates/orphans are invisible to serving and sparse snapshots. Physical Chroma
writes may repeat; do not claim physical atomicity or exactly-once writes.

One logical active generation controls dense, sparse and provenance. Activation
requires a durable CAS/fence and the candidate's expected base. Concurrent G2/G3
from G1: first valid activation succeeds, stale second and its retries fail.
Protect against stale workers, including old successful workers and rollback ABA.
Persist PREPARING/READY/ACTIVE-or-accepted/FAILED/STALE semantics and immutable
candidate input. Reopen/resume incomplete writes idempotently; revalidate prepared
candidates; never activate stale-base work. No second scheduler; reuse 17C concepts
and an admitted step/service composition where useful.

Pin a generation when admitting retrieval and use it for dense, BM25, fusion,
reranking, evidence and citations. An admitted older request may finish only if
its generation remains intact. New requests use active generation. A replica with
G1 sparse while active G2 is alive but unready and must reject mixed-generation
serving. Controlled startup/rollout loads sparse snapshots; no request/readiness
rebuild or state mutation. Make the corpus-version relationship explicit.

Reprocessing same compatible accepted inputs reuses representations; new version
or extraction/digest/retrieval/embedding profile produces new representations.
V1 stays authoritative until V2 activation. Superseded/revoked versions must be
absent from new dense/sparse/hybrid/rerank/citation/analysis results. Revocation is
retrieval exclusion, not canonical deletion. Retain historical audit artifacts.

Rollback revalidates manifest integrity, compatibility, dense inventory, provenance,
source/version/checksums and sparse reconstructability, then uses the same CAS.
Test G1 -> G2 -> validated G1 and reject missing/corrupt rollback targets.
Reconciliation detects inconsistent manifests/inventories/metadata/sparse versions
and orphan candidate data without implicit repair or mandatory deletion.

## Accepted inputs, chunking and embedding limits

Verify accepted final digest/checkpoint manifests, source and extraction integrity,
correct document version, resolvable evidence, profiles and quality policy.
COMPLETED job alone is insufficient. COMPLETE may publish; FAILED/CANCELLED never.
Default PARTIAL rejection; if supported only explicit policy with warnings,
coverage and unsupported/missing units, never upgraded to COMPLETE.

AnalysisChunk is not a retrieval chunk. Independently version retrieval chunking,
retain exact spans and canonical structure where known, deterministic order,
bounded text/metadata and explicit table/unavailable limitations. Never silently
truncate or invent interpreted tables. Do not index every digest artifact by default.
If derived records are indexed, retain canonical inherited lineage and resolve it
before source citation; unresolved derived material cannot become factual evidence.

Record IDs derive from semantic document/version, extraction, source evidence,
material/structure and retrieval/embedding/provenance profile, not worker, attempt,
path, process, random execution identity or incidental order. Bound vector metadata.
Fingerprint model identity and pinned revision, dimension, normalization, chunk,
provenance and publication schema. Incompatible profiles cannot silently reuse data.

Inspect actual pinned all-MiniLM-L6-v2 tokenizer/model and library truncation behavior.
Record observed maximum and safe application bound. Explicitly split/check input
before embedding; test oversize inputs and exact source mapping.

## Retrieval, analysis and citations

Keep Chroma syntax inside the adapter and serving read-only. Preserve legacy
`data/docs` ingestion/corpus functionality with an explicit coexistence strategy.
Carry stable record identity/provenance through dense and BM25, RRF and reranking.
Deduplicate Phase 17 records by stable record ID; legacy identity may remain
source/chunk based. Reranking changes relevance/order only.

Implement query -> explicit selected published documents -> pinned generation ->
hybrid/rerank -> canonical evidence -> bounded context -> existing provider ->
answer with application-controlled citations. Document filtering is trusted
functional scope, NOT authorization. Selected analysis cannot search unrelated
Phase 17 documents. Use a minimally disruptive additive service/API, no public
publication/admin mutation. Preserve old clients and streaming.

Citations carry application-issued IDs, document/version/extraction/record identity,
source display, canonical PDF physical page or real text line/span, structure,
bounded excerpt and resolution state. Never invent pages. Verify canonical
source/block/span association and exact text; vector strings alone are insufficient.
Prompts distinguish ORIGINAL_SOURCE_EVIDENCE from DERIVED_RETRIEVAL_MATERIAL.
Document instructions remain untrusted data and cannot invoke tools or become
system control. Bound context without silently dropping qualifications/conflicts.

Reject model-returned citation IDs not allowed for that request and independently
validate selected scope and canonical resolution. Distinguish allowed IDs,
provenance validity, and semantic support. Report provenance validated/structurally
grounded, never semantically verified. Include an irrelevant-but-valid citation
test. Represent insufficient/incomplete/conflicting evidence honestly. Semantic
faithfulness/entailment certification belongs to 17H.

## Internal checkpoints and test order

F1 audit/design; F2 models/records/provenance/chunk bounds/input validation; F3
candidate/activation/CAS/recovery/lifecycle; F4 pinned hybrid/citations/readiness;
F5 selected interactive analysis; F6 complete validation/review/report. These are
internal checkpoints, not branches, commits or authorization for later phases.
At each, run targeted tests, inspect scoped diff, review/fix findings and continue.

Test publication identity/immutability/schema/compatibility; COMPLETE/PARTIAL/FAILED/
CANCELLED/missing/corrupt inputs; structure/oversize/token limits/no text loss;
inactive/idempotent dense writes; active-only sparse; activation/failure/races;
stale replicas; reprocessing/supersession; revocation at every serving stage;
rollback validation; fresh-process recovery/orphans; wrong version/extraction/
source evidence and derived-source boundary.

Inject interruption before writes, midway, after writes, after validation, before
activation, after activation, during revocation and rollback. No partial candidate
may become active. Test dense-only, sparse-only, shared-ID fusion, metadata through
actual reranker, selected scope, active generation, revoked/superseded and legacy.
Test single/multiple documents, no evidence, PDF/text citations, qualifications,
contradictions, forged/foreign/wrong-document IDs, irrelevant valid IDs, injection,
old queries and streaming if changed. Test actual local Chroma filter behavior.

Run targeted tests in order: domain; chunk/bounds; provenance/citations;
activation/fencing; recovery/lifecycle; dense/sparse coherence; hybrid/reranking;
interactive; old RAG/vector/BM25; 17B–17E; API/streaming/provider/memory; full suite;
compileall; Compose config; Helm if deployment-facing interfaces change; diff check.
Do not repeatedly run the full suite for small changes. Record exact results.
Use LocalObjectStore, SQLite reference authority, synthetic docs and fake providers.
Bounded multi-hundred-unit observations are useful, not Phase 17H certification.

## Review, artifacts and completion

Review complete diff for candidate visibility, stale/CAS/ABA races, mixed snapshots,
stale-ready replicas, superseded/revoked leakage, display identity as evidence,
generated source masquerading, metadata explosion, implicit tokenizer truncation,
post-top-k scope filters, adapter leakage, resets, request/probe rebuilds, public
admin, authorization overclaims, arbitrary IDs, entailment claims, incompatible
reuse, unvalidated rollback, process-memory recovery, duplicate generations,
high-cardinality metrics, content/secret logs and prohibited infrastructure actions.
Fix meaningful in-scope findings; never mask unresolved architecture for PASS.

Separate pre-commit review: secrets/private keys/.env, private documents, local
paths, debug/TODO/dead code, dependencies, temporary/cache/bytecode/runtime DB files,
unrelated changes, broken links and API changes. Do not commit. No body/prompt/
answer/evidence/embedding/credential logging; metrics use bounded categories only.

Create this prompt and `docs/codex/reports/phase_17f_report.md`. Report architecture,
strategy alternatives/rationale, identities/state/manifests, transaction boundary,
fencing/recovery/pinning/replicas, records/chunks/encoder/profile, Chroma/BM25/legacy,
reprocessing/supersession/revocation/rollback/policy, evidence/hybrid/reranker,
analysis/scope/API/citations/control-data boundaries, crashes/readiness/observability,
17G security deferrals, exact files/tests/validation/reviews/limitations/Foundry gate,
next-phase prerequisites and final no-commit Git state.

Only after genuine PASS, incrementally update CURRENT README to 17F complete,
preserving its organization, badges, prior documentation and production-claim
discipline. Keep 17E live Foundry pending, 17G/H/I planned; do not mark all 17 complete,
claim production multi-user security, semantic entailment, or 1000-page certification.

At completion record status, HEAD, diff stat/check, exact created/modified/deleted
inventory and artifact checks. HEAD remains cb70b26; commit NO, push NO, branch NO,
starting baseline preserved YES. Concisely report all implemented guarantees,
test counts, observations, limitations and prohibited-action confirmations.
Conclude **Phase 17F — PASS** only if all applicable acceptance criteria are proved.
Exact next phase: **Phase 17G — Multi-User Security, Quotas & Cost Governance**.
Do not start 17G, 17H, 17I or Phase 18.
