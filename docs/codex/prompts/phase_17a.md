# Phase 17A — Architecture, Cost & Risk Assessment

Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`  
Branch: `master`  
Major phase: **Phase 17 — Production Document Digestion & Intelligence**

This is the clean finalized task prompt, normalized to the unified Phase 17
numbering. Its scope is architecture, assessment and documentation only.

## 1. Preparation and repository safety

Read repository-root `AGENTS.md` completely before work. Inspect
`git status --short --branch`, `git rev-parse HEAD`, README, architecture and
operations documentation, relevant Phase 8A–8G and Phase 9–16 reports, especially
the final authoritative Phase 16 closure. Inspect existing RAG, ingestion,
vector-store, inference, memory, monitoring, Helm and deployment implementation
and tests. Verify the actual repository state.

Preserve all intentional working-tree edits, especially the Phase 16 report.
Do not reset, stash, checkout, discard or overwrite existing work. Work directly
on master; do not create a branch, commit or push. Do not expose API keys, Redis
credentials, bearer tokens, Azure access keys, subscription or tenant IDs,
private endpoints, connection strings or other secret values.

Do not implement document digestion, provision or mutate Azure resources,
modify Kubernetes, enable HPA, increase Foundry capacity, or create queues,
storage accounts, databases, OCR services, workers or other paid infrastructure.

## 2. Unified phase terminology

Search all tracked and intentional untracked project documentation, including
README, docs, prompts, reports, architecture, ADRs, runbooks, roadmaps, planning
notes and documentation elsewhere. Translate the retired nine-stage numbered
roadmap in order into Phase 17A through Phase 17I. Preserve historical substance
but retain no obsolete identifier, alias or “formerly” reference. Do not change
unrelated source-code identifiers.

The Phase 16 handoff must identify Phase 17 as the next major phase, beginning
with Phase 17A. Verify with `rg -n '\bDD[0-8]\b' README.md docs` and an expanded
repository-documentation search: expected no matches. Even this finalized prompt
and the report must use only the official phase identifiers.

## 3. Purpose

Define how PolyMind should process approximately 200, 500 and 1,000+ page
technical, regulatory, legal, policy, research, manual, due-diligence and
enterprise document packages before implementation begins. Answer architecture,
component ownership, synchronous/asynchronous work, large-file storage,
failure/restart recovery, provenance, inference and OCR placement,
security/privacy, cost, later-phase responsibilities and explicit exclusions.

## 4. Existing architecture

Extend rather than replace FastAPI, LangGraph, semantic/logical routing, RAG,
hybrid retrieval, BM25, RRF, cross-encoder reranking, conversation memory,
provider-neutral inference and Prometheus metrics. Preserve Ollama and
OpenAI-compatible inference, existing APIs, NDJSON streaming and security
boundaries. Respect external Foundry inference, Azure Managed Redis, shared
Chroma HTTP, AKS and separately operated Prometheus/Adapter.

## 5. Provider posture

Azure is the validated target. Keep internal application contracts
provider-neutral. Phase 16 Foundry validation is infrastructure preparation,
not completion of Phase 17E. Do not introduce another cloud as an active
dependency; discuss alternatives only for future portability where useful.

## 6. Candidate architecture

Assess and refine: upload/registration → durable objects → processing job →
extraction → selective OCR/layout → canonical normalized document → structural
segmentation → chunk analysis → section synthesis → document synthesis → evidence
validation → digest artifacts, RAG publication and interactive analysis.

## 7. Synchronous and asynchronous boundary

Keep request validation, registration/job creation, status/result retrieval,
cancellation requests and published-document interactive RAG synchronous within
bounded requests. Assess extraction, OCR/layout, normalization, preparation,
bulk embeddings, chunk LLM analysis, synthesis, retries and publication as durable
background work. Never hold a request open for a large-document pipeline. Do not
implement workers or queues.

## 8. Storage responsibilities

Separate immutable original objects/checksums/metadata/retention, processing
artifacts, authoritative job/state metadata, retrieval publication and existing
conversation state. Assess object storage versus metadata store versus Chroma
versus Redis. Redis conversation infrastructure is not durable document storage.

## 9. Canonical model

Specify requirements, not code: document identity, filename, MIME, hash, size,
page count, source pages, sections/headings/paragraphs/tables/figures, available
coordinates, extracted text, OCR provenance, extraction method, language, stable
chunk and parent/child identities, artifact/parser versions, timestamps and
evidence references. Explain citation-critical metadata.

## 10. Extraction, OCR and layout

Prefer native PDF/text extraction; escalate for structural fidelity and apply
OCR only to scanned/image or failed pages. Cover born-digital, scanned and mixed
PDFs, tables, columns, figures, headers/footers, page labels, malformed/encrypted
files and very large files. Define escalation criteria; install no OCR service.

## 11. Hierarchical digestion

Explain why flat RAG is insufficient for full-document digestion. Assess
section/subsection/chunk/evidence hierarchy, bounded overlap/context, tables,
cross-references, token and prompt budgets, map/reduce synthesis, evidence
retention and checkpoint/resume points. Do not implement prompts or pipelines.

## 12. Provenance

Require important conclusions to resolve to document, page, section, chunk,
extraction artifact/version, optional coordinates/blocks and model stage. Create
and preserve this traceability through the workflow instead of trusting
free-form generated page citations.

## 13. Durable orchestration

Define Phase 17C requirements and a state machine covering registration, upload,
queueing, extraction, normalization, analysis, synthesis, publication, completion,
failure, cancellation and partial results. Assess idempotency, retry/backoff,
poison/dead-letter work, recovery, checkpoints, duplicate content, artifact reuse,
resumability and honest progress. Compare technologies before selecting a queue.

## 14. Managed inference

Define Phase 17E: Foundry compatibility through the existing abstraction, batch
versus interactive work, concurrency, RPM/TPM, role/model selection, summarization,
optional extraction assistance, retries, overload and cost-aware routing.
Incorporate Phase 16's limited throughput; do not increase capacity or assume
application HPA resolves inference quotas.

## 15. Publication and interactive analysis

Define Phase 17F searchability, whole versus incremental publication, corpus and
document versions, stable chunks, metadata/provenance, BM25 snapshots, dense/hybrid
retrieval, reranking, citations, reprocessing, stale-vector prevention and
revocation/deletion. Reuse the existing RAG system.

## 16. Security, privacy and tenancy

Threat-model malicious PDFs, size/parser/decompression bombs, active content,
direct/indirect document prompt injection, poisoned content, cross-user/tenant
leakage, unsafe filenames/path traversal, unauthorized artifacts, storage and temp
exposure, content/secrets in logs, provider disclosure, deletion/retention, denial
of service and cost abuse. Define future controls without claiming implementation.
Phase 17G formalizes multi-user security, quotas and cost governance; earlier
phases must carry compatible ownership and authorization requirements.

## 17. Cost

Separate existing/fixed AKS, Redis, monitoring and retained Azure costs from
per-document storage, extraction, selective OCR/layout, embeddings, inference
input/output tokens, retries and publication, plus worker/concurrency/queue/
retained-artifact scaling costs. Provide 200/500/1,000-page scenarios with explicit
engineering assumptions. Use formulas and operator-supplied prices when current
applicable pricing is unavailable; do not fabricate money estimates. Include
native-first extraction, selective OCR, hashes/cache/reuse, idempotent retry,
hierarchical compression, batching, output caps and tiered model selection.

## 18. Reliability

Define future Phase 17H measurable gates for 200/500/1,000+ pages, scanned/mixed
files, concurrent jobs, extraction failures, inference 429/timeouts, worker
restart, queue retry, storage interruption, duplicates, cancellation,
reprocessing and publication failure. Do not run these tests now.

## 19. External verification

Phase 17I follows controlled completion of Phase 17A–17H. Define representative
documents, informed consent, privacy, bounded test scope, feedback on quality,
citations, latency, errors and usability. Do not contact or test external users.

## 20. Decisions and ADRs

Identify ADR candidates for asynchronous jobs, objects, canonical representation,
extraction escalation, state/queue technology, hierarchical synthesis, provenance,
publication, retention and managed inference. Distinguish DECIDED, PROPOSED,
DEFERRED, NEEDS BENCHMARK and NEEDS COST DATA; do not finalize unsupported choices.

## 21. Deliverables

Create this prompt and `docs/codex/reports/phase_17a_report.md`. The report must
cover executive summary/result, baseline/problem, functional/non-functional
requirements, architecture/ownership, sync/async, storage/model/extraction,
orchestration/hierarchy/provenance, inference/publication, security/tenancy,
reliability/cost/performance/observability/retention, alternatives/ADRs,
dependencies/acceptance/risks, Phase 17B starting boundary, terminology migration
and Git/validation state. Explain rationale and limits for another engineer.

## 22. Acceptance

PASS requires a coherent production design for 200–1,000+ pages; explicit work
and storage boundaries; extraction/selective OCR; canonical model; durable
recovery/idempotency; hierarchy/provenance; reuse of RAG; neutral Foundry
integration and Phase 16 rate-limit evidence; threats; honest cost formulas;
separated later phases; no premature implementation or resource mutation; and
complete removal of retired roadmap identifiers from documentation.

## 23. Official roadmap and dependencies

| Phase | Official title |
| --- | --- |
| Phase 17 | Production Document Digestion & Intelligence |
| Phase 17A | Architecture, Cost & Risk Assessment |
| Phase 17B | Canonical Document Model, Object Storage & Extraction Plane |
| Phase 17C | Durable Job Orchestration, Idempotency & Recovery |
| Phase 17D | Hierarchical Evidence-Grounded Digestion |
| Phase 17E | Managed Inference Integration |
| Phase 17F | RAG Publication, Provenance & Interactive Document Analysis |
| Phase 17G | Multi-User Security, Quotas & Cost Governance |
| Phase 17H | 200–1000+ Page Reliability, Failure & Quality Validation |
| Phase 17I | External User Verification |

Document dependency gates. Do not begin Phase 17B.

## 24. Documentation updates

Inspect README, prompts/reports, architecture/ADR/runbook folders where present
and other planning documentation. Make Phase 16 closure and Phase 17/17A handoff
clear. Translate only retired labels in historical content; avoid unrelated
rewrites and preserve intentional uncommitted edits.

## 25. Validation

Run `git diff --check`, inspect `git status --short --branch`, `git diff --stat`
and the complete intended diff including new documents. Search README/docs and
all other documentation for retired identifiers. Check accidental secret exposure
without printing matched values. Confirm application and infrastructure files
are unchanged. Do not run expensive integration/load tests or install dependencies.
Lightweight documentation/static validation is permitted.

## 26. Result

Conclude **Phase 17A — PASS** only when all assessment criteria are met. This
means architecture, boundaries, cost/risk models and roadmap are sufficiently
defined to begin Phase 17B; document digestion is not implemented.

## 27. Operator response

Report result, created/updated files, architecture, cost drivers, risks, decisions
and deferrals, terminology search and validation results. Confirm no Azure or
Kubernetes mutation, paid infrastructure, secret exposure, commit or push.
Give the exact next phase: **Phase 17B — Canonical Document Model, Object Storage
& Extraction Plane**. Leave all changes for operator review.
