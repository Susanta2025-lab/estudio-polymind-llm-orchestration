# Phase 17B — Canonical Document Model, Object Storage & Extraction Plane

Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`. Branch: `master`.
Major phase: **Phase 17 — Production Document Digestion & Intelligence**.
Phase 17A: **PASS / COMPLETE**, architectural authority for this implementation.

This is the clean finalized implementation prompt, organized by deliverable.
The operator's acceptance boundary and no-commit policy apply throughout.

## Preparation and worktree protection

Read root AGENTS.md completely. Inspect status, HEAD, README, Phase 17A prompt
and report, final authoritative Phase 16 closure, existing RAG ingestion/PDF/text
loaders/chunking/vector/retrieval code, consumers, tests, security/configuration,
dependencies and coding conventions. Inventory the starting dirty worktree before
editing; snapshot files outside the repository if needed for incremental accounting.

Work directly on master. Do not create a branch, stage, commit, push, reset,
stash, restore, clean, discard prior work or rewrite Phase 17A artifacts. Preserve
all Phase 16 closure and Phase 17A modifications. **No Phase 17 work may be
committed until all of 17A–17I is complete and reviewed.** Do not recommend an
intermediate commit. This same accumulated working tree continues into later phases.

## Scope and architecture

Implement a cohesive, shallow `document/` or `documents/` domain consistent with
repository conventions: canonical immutable models, storage port, local/fake
adapter, PDF/text extraction, provenance/serialization, quality observations and
policy. Keep domain, storage implementation, extraction and policy boundaries
clear. Preserve provider-neutral inference and every existing application/API path.

Raw source objects are immutable; artifacts are versioned. Object storage is
separate from job state. Redis remains conversation memory; Chroma remains derived
retrieval data. Carry owner/tenant scope now, before Phase 17G authentication.
Native extraction is default; layout/OCR are conditional escalation contracts.
No cloud service is needed: use deterministic fixtures and temporary local storage.

Exclude durable queues, workers, leases/fences/outbox/retry scheduling, synthesis,
summarization, managed inference integration, quota admission, corpus cutover,
identity providers, multi-user production access, HPA, database/Blob/Document
Intelligence/Service Bus provisioning and external user testing. No Azure or
Kubernetes mutation, Foundry call or external OCR submission is permitted.

## Canonical domain and evidence

Implement explicit schema/extraction/parser/normalization versions, opaque scoped
IDs and immutable document/version identity. Include source SHA-256/hash algorithm,
actual bytes, declared/detected MIME, display filename, page count when applicable,
known language/confidence, creation/extraction times and extraction profile.

PDF pages carry stable source IDs, **explicit physical indexing convention**,
separate printed labels when known, document version, dimensions/rotation when
known, extraction method/status/parser version, text/spans and optional OCR fields.
Account for every physical page, including blank, image-only, failed and unsupported
cases. Unknown information stays unknown.

Blocks support text/paragraph, heading, table, figure/caption and unknown units,
stable IDs, page/source association, reading order, source text, optional normalized
text, spans/geometry and parent/child relationships. Tables/figures can retain
caption, source relation, actual cells and image object references when available,
with explicit unparsed/unsupported states. Do not invent semantic structure from
native text or claim the parser identifies reliable tables/headings/columns.

Evidence must resolve by owner, document version, extraction version, page/text
source, block and span. Filename plus chunk number is insufficient. Text sources
use character/line provenance, never fabricated pages. Define offset units and
normalization-to-source behavior. Preserve raw text; conservative identity/newline/
Unicode normalization only with adequate mappings. No semantic rewriting,
translation, repeated-text deletion or invented table prose.

Use deterministic scoped IDs where reproducibility matters and opaque external
representations independent of filenames. UUIDv5/content hash approaches must not
collide across owners/documents. Hash equality never confers access. Serialize
explicit versions and nulls deterministically with stable JSON fields; no pickle
or large binary base64 payloads. Test round trips and parent hash/version lineage.
Future profiles produce new immutable artifacts. Document version-readability and
migration expectations without a speculative migration framework.

## Object storage

Create the smallest provider-neutral interface supporting immutable source/artifact
puts, bounded read/inspection and checksum verification. Server-compute SHA-256;
reject mismatched declarations and conflicting writes. Generated keys must not
use uploaded filenames as filesystem paths. Define bounded metadata, safe errors
and explicit collision behavior. Delete only if needed for scoped tests/admin.

Implement an isolated configurable local/fake store using atomic creation where
practical, traversal/symlink resistance, immutable writes and temporary-directory
tests. It is not conversation file memory. Keep metadata distinct from filenames.
Document future Azure Blob conditional creation/integrity adaptation, but do not
add an unused Azure SDK, access an account/container or provision anything.

## Ingestion, extraction and parser safety

Prefer a domain/service entry point; no public upload endpoint is required and
the API query-body limit must not increase. Validate actual byte count, configured
bytes/pages/characters/work limits, supported format rather than filename/MIME
alone, malformed/encrypted PDFs, empty input, UTF-8 behavior and checksum.

Inspect and extend PDF behavior safely: either preserve legacy
`rag/loaders/pdf_loader.py`, `rag/chunking.py`, `rag/ingest.py` unchanged with a
future migration plan (strategy A), or share low-level extraction with exact
compatibility wrappers and regression tests (strategy B). Do not change Chroma,
BM25, live corpus publication or retrieval semantics. Canonical output must allow
Phase 17F encoder-compatible evidence chunks/citations without publishing now.

PDF extraction is per physical page, with native/blank/image/failed distinctions,
safe observations, parser version and artifact identity. Plain text has strict,
documented decoding and line/character spans, bounded memory where practical and
predictable rejection of invalid/empty content. No automatic external OCR.

Separate measured observations (characters, printable/replacement ratios,
images/native text, emptiness, block count, parser failure) from policy. Avoid
unvalidated universal minimum-character OCR thresholds. Decisions include native
acceptance, layout/OCR required, unsupported/failed/manual review, source identity,
observations, policy version, reason and next tier. Define a minimal future
OCR/layout adapter returning physical mapping, text/blocks/tables/geometry/
confidence/engine/model/version/lineage where supported; test fakes if useful.

Implement practical application limits and exception isolation. Use a small
parser-runner boundary if portable process isolation cannot fit cleanly. Explicitly
document deferred CPU/wall-clock/memory/decompression/pixel sandbox limits; never
claim Python/library checks impose OS guarantees. Normalize errors without paths,
raw parser messages, source contents, credentials, endpoints or connection strings.

## Fixtures, fidelity, security and performance

Generate small public-domain synthetic fixtures in tests: multipage born-digital
PDF, blank/mixed pages, image-only if feasible, malformed/truncated/encrypted PDF,
UTF-8/Unicode/empty/large text, and columns/table-like content when meaningful.
Do not commit real/private/copyrighted documents or generated binary fixtures.

Create a bounded fidelity matrix: expected/accounted physical pages, text-bearing
pages/native success, blank classification, OCR/layout choices, preserved physical
numbers, span/evidence correctness and malformed/encrypted outcomes. Prefer exact
expectations. Do not claim representative OCR recall calibration or Phase 17H
candidate thresholds validated from synthetic fixtures.

Test traversal and absolute filenames, unsafe references, symlinks, duplicate keys,
immutable overwrite, corrupted/mismatched checksums, MIME/extension disagreement,
byte/page/work limits, malformed/encrypted PDFs and owner isolation. Test same/changed
bytes, stable round trips and immutable version/profile lineage. Avoid content logs.

Measure synthetic extraction time, approximate/peak memory, serialized size and
verified writes/reads where practical, without extrapolating production SLOs.
Do not add dependencies unless existing packages/stdlib cannot meet a concrete
requirement. No new LLM/cloud/queue/ORM frameworks. Metrics are optional; never use
owner/document IDs, names, hashes, keys, text or URLs as labels. Defer full worker
observability to 17C/17H.

## Validation and review

Run focused new tests, relevant legacy RAG/retrieval/vector/config/security tests
and the full automated suite if feasible. Full suite must pass unless an unrelated
pre-existing failure is independently demonstrated. Run project-standard compileall
(using an external bytecode cache if needed), configured lint/type checks if any,
and `git diff --check`. No test requires cloud, GPU, credentials or network OCR.

Review full implementation and incremental diff for architecture/compatibility,
error/resource handling, stable IDs, missing pages/provenance/scope, source mutation,
unsafe paths, fabricated semantics, normalization loss, large duplicate allocations,
unbounded reads, dependencies, cloud coupling, accidental publication/jobs and
content leaks. Fix meaningful in-scope findings. Perform a separate pre-commit
review for secrets, local paths, debug/temp/generated files, dead code/TODOs,
unrelated changes and broken documentation; do not commit.

## Deliverables and acceptance

Create this prompt and `docs/codex/reports/phase_17b_report.md`. Report executive
summary/result, baseline/scope, models/IDs/versions, source/artifact/storage,
PDF/text/provenance/normalization, observations/policy/adapter, limits/integrity/
serialization, RAG compatibility, scope/security/errors, fixtures/fidelity/
performance, exact files/tests/checks, reviews, limitations, 17C prerequisites and
final Git state. Distinguish implemented behavior from 17C–17I proposals.

PASS requires all applicable contracts above demonstrated: versioned immutable
models, scoped identities, complete physical page inventory, valid non-page text
spans and evidence, explicit unknowns, separate immutable source/artifact storage,
verified hashes/safe local paths, deterministic JSON, native PDF/text extraction,
separate observations and per-page escalation, predictable invalid-input handling,
legacy RAG preserved, no prohibited infrastructure/runtime expansion, passing new/
regression/full/static checks, no secrets, and complete truthful documentation.
Only after acceptance passes may README mark 17A and 17B complete. Do not start 17C.

Record final `git status --short --branch`, `git diff --stat` and incremental Phase
17B accounting against the baseline. Confirm: commit NO, push NO, branch NO,
prior work preserved YES. Leave everything unstaged for operator review.

Final response must state result, exact created/modified files, canonical/storage/
PDF/text/provenance/escalation behavior, safeguards, fixture/fidelity/test results,
full/static checks, compatibility, limitations, prior-versus-new worktree summary,
and no Azure/Kubernetes mutation, OCR/Foundry call, paid infrastructure, secrets,
commit, push or branch. If every criterion passes, conclude **Phase 17B — PASS**.
This establishes readiness for **Phase 17C — Durable Job Orchestration, Idempotency
& Recovery**, not completion of cloud storage, OCR, jobs, digestion, publication,
multi-user production access or all Phase 17. Do not start the next phase.
