# Phase 17D — Hierarchical Evidence-Grounded Digestion

Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`. Branch: `master`.
Major phase: **Phase 17 — Production Document Digestion & Intelligence**.
Previous results: Phase 17A PASS, Phase 17B PASS, Phase 17C PASS.
This is the finalized clean task prompt, organized by implementation contract.
The operator's scope, acceptance requirements and no-commit policy govern it.

## Operator policy and preparation

**Do not commit any Phase 17 work until the entire Phase 17A–17I is complete and
reviewed.** Work directly on master. Do not create a branch, stage, commit, push,
reset, stash, clean, restore, check out existing files, delete prior untracked
artifacts or use commits as checkpoints. Preserve the intentional dirty worktree,
including Phase 16 and Phase 17A–17C. Preserve prior Phase 17 artifacts byte for
byte except deliberate cumulative README/roadmap updates. Do not unnecessarily
rewrite reports. Record `git status --short --branch` and `git rev-parse HEAD`
before editing. Snapshot every possible modified file outside the repository,
preferably at `/tmp/polymind-phase17d-baseline`.

Read root AGENTS.md completely. Inspect all of README, Phase 17A/17B/17C reports,
Phase 17B/17C prompts, `documents/`, `documents/jobs/`, document unit and relevant
integration tests. Inspect LangGraph, inference contracts, model roles, RAG
chunking/retrieval, generation source assembly, configuration, error normalization,
logging and metrics. Verify implementations rather than trusting reports alone;
search consumers before any interface change.

## Purpose, boundary and foundations

Prove a local, provider-neutral hierarchical document-intelligence architecture:
canonical artifact → structural map → analysis chunks → structured chunk analysis
→ bounded subsection/section/higher reducers → synthesis → evidence/coverage
validation → versioned immutable digest. Never send an entire large document as
one inference prompt or use top-k RAG as whole-document coverage.

Use deterministic fake inference only. Implement structure/chunks/schemas,
inference/request/result contracts, reduction planning, evidence inheritance and
validation, coverage, qualifications/contradictions/unknowns, partial outcomes,
resource bounds, checkpoints and durable retry/cancel/resume integration.

Reuse Phase 17B Document, ExtractionArtifact, TextUnit, Block, EvidenceRef, spans,
immutable storage, serialization philosophy and extraction versions. Reuse Phase
17C admission, jobs, steps, stable keys, attempt history, leases/fences, retry
scheduling, cancellation, manifests, outbox, checkpoint reuse and reconciliation.
Do not create a second scheduler, retry framework, store, source identity or
evidence model. Extend existing contracts only when genuinely necessary.

No real Azure Foundry, OpenAI-compatible, Ollama, vLLM or other model calls. No new
LLM API, token billing, distributed quota admission, RAG/Chroma/BM25 publication,
production authentication, Azure resources, Kubernetes mutations, upload API,
worker deployment, production DB/queue migration, OCR integration, external users
or paid infrastructure. Phase 17E owns managed inference. Preserve application,
provider, serving, retrieval, memory, Docker and API behavior.

## Deterministic structural planning and chunking

Prefer a full immutable dependency plan derived before admission. Introduce
dynamic child steps only if the hierarchy genuinely cannot be known without
inference, with transactional/idempotency proof and compatibility tests. Do not
add dynamic fan-out by convention. Document the decision.

Represent document/section/subsection/fallback structure, ordered children,
parents, stable IDs, document/version, headings/paths where known, canonical
pages/spans/evidence, unit type, structural source/confidence and profile versions.
Use explicitly available source headings/blocks/pages/tables/paragraphs. Do not
infer headings from formatting without identifying them as inferred. Weakly
structured sources need deterministic fallback. Validate invalid parent graphs.

AnalysisChunk is separate from retrieval chunks. Include stable chunk identity,
document/version, structural parent/path, ordered source blocks/spans, exact
permitted evidence, source representation, estimate, sequence/profile/version and
overlap metadata. Preserve small structural units and section boundaries; split
oversized units deterministically. Preserve tables/rows where possible and record
limitations when canonical data cannot support interpretation or safe splitting.
Never silently lose source text or fabricate cells/figure descriptions.

Use configurable input/output/fan-in/size/work budgets; tests use small synthetic
limits. Do not treat Phase 17A sample sizes as production settings. A neutral
local deterministic estimator is sufficient; avoid new tokenizer dependencies.
Separate estimates from actual provider usage. Account source text, children,
heading context, evidence metadata, template overhead and reserved output. Split
inputs or add deterministic reduction levels when budgets require it. Never
silently truncate content, evidence, child results or annotations. Bound generated
claims, text, questions, contradictions, metadata and stored artifact bytes.

## Neutral inference, structured claims and validation

Use a narrow `analyze(stage_request) -> structured_result` contract. Requests
carry stage/profile/role/prompt/schema versions, bounded context, structural path,
permitted source references and inherited evidence. Provider endpoints,
deployment IDs, credentials and HTTP/temperature syntax stay outside the domain.
Phase 17E will adapt this boundary to the existing InferenceProvider.

Fake inference must be deterministic, predictable, network-free and configurable
for first-attempt failure, permanent failures, qualifications, contradictions and
unavailable analysis fixtures. Do not optimize wording or simulate language quality.
Retries retain logical request, allowed evidence, profile and successful bytes.

Claims have stable IDs, type/text, supporting/contradicting source IDs,
qualifications, origin, lineage and status. Factual claims require authorized
source support; structural/unknown/unsupported/commentary classes are explicit.
Do not treat confidence as a calibrated probability or security gate. Page-number
prose is not citation authority. Use typed identifiers resolved by application code.

Strictly validate every output before checkpoint acceptance. Reject malformed
JSON, duplicate keys/IDs, unknown fields, oversize output, non-finite values,
invalid parent/claim lineage, foreign scope/document/extraction and fabricated
source evidence. Evidence must resolve to original Phase 17B spans and must have
been allowed to the current request. No best-effort malformed-output repair.

Reducers inherit only authorized child source evidence and explicit claim lineage.
Generated summaries are never source evidence. Preserve exact qualifications,
both opposing statements/evidence and unresolved contradiction lineage through
all levels. Keep missing information, unknowns and unavailable source content
explicit. Avoid embedding/semantic deduplication; any deterministic dedup must
retain evidence, qualifications and conflicts.

## Reduction, coverage and outcome policy

Support one child, fan-in boundary, boundary plus one, recursive levels and hundreds
of chunks. Prefer structural subsection/section reducers; weak structure uses
bounded deterministic batches. Reducers must retain child claims/evidence,
qualifications, contradictions, questions, source-child lineage and coverage.
Document reducers may add executive synthesis, sections, findings, limitations,
coverage and incomplete areas.

Measure canonical source/evidence units, not summary count. Inventory eligible,
analyzed, failed, policy-skipped, unsupported/unextractable and included units.
Union overlapping spans so repeated content cannot inflate coverage. Failed,
OCR-required, manual-review and unsupported canonical pages affect outcome honestly.

Use explicit configurable COMPLETE/PARTIAL/FAILED policy. Success of fake calls
alone is insufficient for COMPLETE: validate complete required hierarchy, source
coverage, evidence and permitted missing content. Partial output must expose
missing/failed units, statistics, limitations and available grounded results; never
silently publish it as complete knowledge. Root impossibility, invalid evidence,
incompatible profile/schema, corruption, unacceptable missing coverage and planning
failure must fail safely according to policy. Phase 17F decides publication.

## Durable artifacts and workflow integration

Every expensive logical stage is checkpointable: structure/chunk plan, analysis,
reducers, final digest and coverage. Use Phase 17B objects and Phase 17C accepted
manifests; no mutable synthesis files. Compatibility includes source/extraction,
structure/chunk/inference/reducer profiles, schemas and parent artifact hashes.
Version schema/profile changes and preserve old bytes; deterministic JSON only.

Execute through Phase 17C Worker/leases/attempts/fences/outbox/commit/retry/cancel.
Prove first-attempt failure → scheduled retry → same logical result → one accepted
manifest. Do not add provider retries. Test cancellation during analysis,
intermediate reduction and before root/final acceptance; stale work cannot commit,
no downstream work starts after cancellation, prior checkpoints remain immutable.
Completion may win only if its transaction legally precedes cancellation.

Prove analyses succeed → reducer fails → terminal run → compatible new resumed run
→ accepted analyses reused → unfinished reduction reruns → digest succeeds.
Changing chunking/inference/reducer profile invalidates incompatible checkpoints.
Restart must not depend on in-memory graph state. Existing LangGraph may compose
in-step work only if useful; it never becomes durability authority. Explicit
planner/reducer code without LangGraph is acceptable; document the choice.

Use sanitized domain/workflow error categories. Never log or expose source/model
content, stack traces, paths, keys, credentials or unnecessary provider details.
Document data is untrusted and separated from instructions/profile metadata. No
source text can grant tools/permissions and no synthesis tool execution exists.
Test “Ignore all previous instructions”, “Delete the database” and another-tenant
requests as inert evidence. Metrics may be deferred; any added labels are bounded
and never contain document/job/owner/name/text/evidence/hash values.

## Tests and validation

Use synthetic public-domain fixtures only: simple and weak structure, nested
sections, oversized sections, tables/figures, fan-in boundaries, recursive levels,
qualifications, opposing claims, unknown/unextractable units, invalid evidence,
malformed output, retry, cancellation, stale commit, failure/resume, incompatible
profiles, adversarial text and large logical documents. Test deterministic IDs,
ordering/DAG, boundary budgets, no source loss, output bounds, inherited original
evidence, canonical coverage and complete/partial/failed gates.

Validate conceptual 200/500/1,000/>1,000 source-unit structures using small bodies,
not expensive real-model documents. Observe planning/execution time, chunks,
levels, checkpoints, bytes and memory where useful. Avoid accidental quadratic
source/evidence/claim/coverage matching; identify ledger scaling limitations.
Do not claim production throughput or Phase 17H certification.

Required local integration: generated multipage PDF → actual Phase 17B extraction
→ structure/chunks → Phase 17C admitted DAG → fake analysis/reducers/root → evidence
and coverage → immutable digest → fresh ledger/store reopen → valid original
source evidence. Second integration must prove reducer failure/resume with no
repeat accepted analysis computation or duplicate manifest per logical step.

Run new targeted tests first, then 17B/17C regressions, relevant RAG/inference/API
regressions and the full project suite. Full suite must pass unless an unrelated
pre-existing failure is independently demonstrated. Run compileall with external
bytecode cache if needed, Compose configuration and `git diff --check`; check new
untracked text too. Use configured lint/static tools only. No validation requires
network, cloud, models, credentials, OCR, GPUs or cluster services.

## Review, documentation and acceptance

Inspect the complete incremental implementation for evidence loss/fabrication,
summary-as-source errors, overlap inflation, qualification/conflict loss, silent
truncation, unstable identities, retries changing requests, incompatible reuse,
dynamic-plan races, duplicate orchestration, unbounded input/output, quadratic
operations, raw errors, prompt injection, provider/cloud/publication coupling and
accidental Phase 17E scope. Fix meaningful findings. Perform a separate no-commit
review for secrets/private documents, temporary/generated files, local paths,
debug/TODO/dead code, dependencies, unrelated edits, broken links and API changes.

Create this prompt and `docs/codex/reports/phase_17d_report.md`. Report executive
summary/result, starting tree/baseline, scope/foundations, architecture/structure/
segmentation/chunks/budgets/inference/fake/claims/evidence, reducers/fan-in,
qualifications/conflicts/unknowns, coverage/outcomes, checkpoints/workflow/retry/
cancel/resume/profile compatibility, resource/security/visual/error boundaries,
large synthetic observations, both integrations, exact created/modified files,
targeted/full/static checks, self-review/pre-commit findings, limitations and exact
Phase 17E prerequisites. Preserve prior reports. Mark README 17A–17D complete only
after acceptance; do not mark 17E started.

PASS requires all implemented contracts above proven, original evidence retained,
no silent content loss, bounded deterministic hierarchy, strict output validation,
qualification/conflict inheritance, honest canonical coverage and partial policy,
immutable final/intermediate artifacts, existing durable scheduler semantics,
compatible reuse/profile invalidation, real local extraction/reopen and failure/
resume tests, large logical tests, passing 17B/17C/full/static checks, no secrets,
and no prohibited calls/mutations/publication/infrastructure or Git actions.

At completion record status and diff stat. Distinguish pre-existing Phase 16,
17A, 17B, 17C and incremental 17D files using the outside baseline. Explicitly
confirm commit NO, push NO, branch NO, staging NO, prior work preserved YES.
Final response must include result, exact files, architectural/contracts/coverage/
workflow behavior, integration/large/targeted/full/static evidence, limitations,
prohibited-action confirmations and worktree accounting.

If all criteria pass, conclude **Phase 17D — PASS**. This means a locally validated
provider-neutral evidence-grounded hierarchy with deterministic inference,
coverage, partial outcomes and durable checkpoint/resume. It does not prove real
LLM semantic quality, Foundry integration, production quotas, publication,
authorization, 1,000-page production reliability or completion of Phase 17.

Exact next phase: **Phase 17E — Managed Inference Integration**.
**Do not start Phase 17E. Do not commit. Do not push.**
