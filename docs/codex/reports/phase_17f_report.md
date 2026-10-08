# Phase 17F — RAG Publication, Provenance & Interactive Document Analysis

Date: 2026-10-08. Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`.
Authority: [finalized prompt](../prompts/phase_17f.md).

## 1. Executive summary

Validated accepted Phase 17 digests can now produce independently chunked original-
source retrieval records, immutable corpus manifests and isolated candidate vector
rows. A local transactional authority switches one logical active generation using
an expected-generation/epoch fence. Read-only replicas load deterministic sparse
snapshots, reject stale admission and pin dense/sparse/provenance to one generation.
An additive, explicitly composed analysis service uses the existing bounded
inference provider and application-issued canonical citations.

## 2. Phase result

**Phase 17F — PASS**, within the local application/data-contract acceptance boundary.
The complete suite passed **590 tests**, including **47 new Phase 17F cases**.
No live inference, cloud service or production distributed authority was required.
This establishes coherent logical publication and structurally validated citation
contracts, not physical Chroma transactions, semantic entailment, production tenant
security or 200–1000-page reliability certification.

## 3. Starting HEAD and baseline

Started on clean `master` at `cb70b26f8de8db1f4e9285d49e4434dbf0ed5004`.
The expected five-commit history matched. Both post-17E README commits (`94945f0`
and `cb70b26`) were part of the baseline. `/tmp/polymind-phase17f-baseline` records
HEAD, status, tracked/unignored inventory, SHA-256 hashes for all 222 initial files,
empty initial tracked diff stat, design decisions and local validation observations.
Final committed HEAD remains identical. No branch or index operation occurred.

## 4. Scope and exclusions

Implemented publication models/planning, explicit encoder bounds, immutable
provenance, candidate lifecycle, transactional CAS, recovery, supersession,
revocation, rollback, generation-aware hybrid retrieval, canonical citations,
selected-document analysis, optional API/readiness composition, tests and docs.
No dependencies, job schema, deployment settings, Docker files or infrastructure
changed. No identity system, tenant authorization, quotas/billing/retention, public
upload, OCR, Azure Blob, queue/database provisioning, GPU or later phase was added.

## 5. Existing RAG architecture inspected

Inspected vector ports/factory/Chroma, ingest/admin, legacy chunking/embedding,
BM25, dense retrieval, hybrid RRF, cross-encoder reranking, graph generation/source
assembly, query/stream/readiness contracts, model pins and relevant regression tests.
Existing RAG drops vector metadata into display source/chunk fields; that remains
appropriate only to its legacy contract. Phase 17 requires an explicit richer path.

## 6. Phase 8G publication behavior and limitations

Legacy ingestion deterministically upserts into a live collection, then writes
`polymind_corpus_version`. Startup checks `BM25_CORPUS_VERSION`, lists all rows and
builds a process-local immutable BM25 index. Readiness gates expected/published/
loaded versions. This does not isolate partially written candidate rows or provide
atomic multi-document publication. The old path remains unchanged for legacy use.

## 7. Phase 17F architecture

`documents/publication/` composes existing ObjectStore, JobLedger and accepted 17D
artifacts with a narrow local publication authority and the vector port. Publication
preparation may run through the existing 17C Worker using PublicationHandler.
Activation is a separate explicit administrative decision, not a public endpoint.
PublicationReplica serves an immutable snapshot; DocumentAnalysis consumes it.
No new scheduler, provider client, LangGraph publication workflow or Redis authority
was introduced. Earlier document schemas and job database remain unchanged.

## 8. Publication strategy alternatives

Considered generation labels in the existing legacy collection, per-generation
blue/green collections, and labels in a separate Phase 17 collection. Sharing the
legacy collection would expose candidates to existing unfiltered readers. A
collection per generation would require more collection lifecycle/factory handling.
Destructive reset cannot preserve the old generation across failed preparation.

## 9. Selected strategy and rationale

Use generation-labelled rows in a **separate Phase 17 collection**, derived as
`VECTOR_STORE_COLLECTION + '_documents'` by the factory. Chroma applies generation
and selected-document filters before top-k. This reuses the pinned adapter/client,
preserves legacy readers, permits incremental preparation, and retains rollback
inventories without creating a collection per generation. Storage grows with
retained generations; cleanup is deliberately deferred. No silent migration/reset.

## 10. Publication domain model

Frozen, extra-forbidden Pydantic models include RetrievalProfile, ActivePublication,
AcceptedDocument, RetrievalRecord, PublicationManifest and Citation. Schemas,
source classification, compatible profiles, exact evidence, accepted digest refs,
full corpus membership, predecessor epoch and removed versions are explicit.
Unknown publication schemas, forged identities and mismatched record lineage fail.
PublicationError carries allowlisted content-free categories.

## 11. Generation identity

UUIDv5 derives from canonical semantic manifest content: base generation/epoch,
scope, document/version/extraction/digest references, record inventory, profile,
removed versions and COMPLETE-only policy. Accepted job IDs are audit references,
not semantic identity inputs. Equivalent retries return the same candidate; an
already active compatible corpus is a validated no-op. A deliberately different
base epoch distinguishes a new publication decision, including after rollback.

## 12. Candidate versus active state

The authority durably records PREPARING, READY, FAILED, STALE and ACCEPTED.
A separate singleton `(generation, epoch)` identifies which accepted generation
is ACTIVE. ACCEPTED is retained for historical rollback/audit; it does not imply
currently active. The immutable manifest never changes as operational state advances.
Each generation represents the full selected corpus, not a patch over live rows.

## 13. Logical atomicity guarantee

After complete validation, a short SQLite `BEGIN IMMEDIATE` transaction updates
the active pointer, monotonically increments its epoch, records acceptance and
appends an activation event. This is one coherent logical decision. Serving uses
a captured generation to select both physical dense rows and its sparse snapshot.
Failed preparation or validation leaves the previous active generation untouched.

## 14. Physically non-transactional work

Object writes, per-record vector upserts, tokenization, validation and snapshot
construction are outside the authority transaction. No SQL transaction spans
Chroma or ObjectStore. Upserts can repeat after interruption; inactive bytes can
remain indefinitely. The guarantee assumes immutable accepted artifacts and
administratively controlled vector mutation. Concurrent malicious external
corruption cannot be made transactional by this reference adapter; subsequent
validation fails closed rather than silently repairing it.

## 15. Concurrent publication and fencing

Every forward activation compares the candidate's complete expected base tuple.
Two prepared candidates from one base race through independent SQLite connections:
only one succeeds. The loser and its retries are stale. The epoch prevents ABA
when rollback selects an earlier generation. A lost activation response is
idempotent only for the exact recorded next epoch and operation; an old successful
worker cannot later reactivate itself. Tests exercise real concurrent threads and
SQLite transactions, stale retries, rollback ABA and late successful publishers.

## 16. Multi-replica switchover

Replicas must share one authoritative publication database/service and immutable
object/vector inventory. A G1 replica observing active G2 becomes unready; a freshly
loaded G2 replica becomes ready. No hot reload occurs. The local SQLite implementation
coordinates processes on a trusted single host; it is not a shared AKS database
approval. A future distributed adapter must preserve the same CAS semantics.
Independent copied databases are not a supported multi-replica authority.

## 17. Request-level generation pinning

Admission captures an active generation and the already loaded snapshot. Dense,
sparse, RRF, reranking, evidence and citations use that immutable pin. If activation
occurs after admission, the old request may finish against the old intact inventory;
new admission on that stale replica fails. Revocation therefore affects newly
admitted work; it is not physical cancellation of already admitted requests.
Historical retrieval is not exposed as a user-selectable mode.

## 18. Durable recovery

Reopening the authority restores candidate refs, base epochs, states and activation
history. Preparation reads its manifest and repeats deterministic upserts; accepted
generations are validated rather than rewritten. Interrupted incomplete candidates
never become active. READY candidates are revalidated before activation. A candidate
with a superseded base is marked/rejected as stale. No Python lock or worker memory
owns publication state. The optional 17C preparation handler returns its immutable
manifest through IntentStore and the existing fenced worker commit.

## 19. Manifest and provenance authority

ObjectStore contains the checksummed immutable complete manifest, including full
EvidenceRefs once per record. AcceptedDocument links job acceptance, extraction
identity/ref and accepted digest hash/ref. Planning requires a completed, uncancelled
job and accepted final digest/coverage manifests. It replays the actual 17D final
DAG/evidence validator without inference or writes, verifies original source bytes,
and compares rebuilt output. Unordered 17D checkpoint/qualification collections are
normalized for comparison across interpreter hash ordering; no substantive evidence
or coverage check is weakened. Chroma stores compact lookup metadata only.

## 20. Retrieval material types

Version 1 intentionally indexes **SOURCE_TEXT / ORIGINAL** only. Analysis chunks,
summaries, generated questions and claims are not embedded or indexed. Digest
qualifications, both conflicting findings, limitations and open questions enter
analysis only as explicitly named DERIVED_RETRIEVAL_MATERIAL. Derived-record
citation reconstruction is consequently not offered; attempts to classify a
retrieval row as a generated original source fail the schema. Adding derived recall
later requires a separately versioned lineage-aware representation.

## 21. Retrieval chunking

Canonical eligible/included blocks are traversed in source reading order and split
independently of AnalysisChunk. Whole small blocks remain intact; oversized blocks
are deterministically halved until the special-inclusive token bound is satisfied.
Exact text slices concatenate back to the original block; no trimming, overlap,
normalization or silent source loss. Each slice retains the canonical EvidenceRef
and corrected real line/span coordinates. Structural paths come from the accepted
plan. Tables/figures retain source text and an uninterpreted-visual limitation;
no synthetic cells or visual interpretation are invented.

## 22. Encoder/tokenizer validation

Inspected and loaded the locally cached pinned model revision
`1110a243fdf4706b3f48f1d95db1a4f5529b4d41` without network. Model files declare
SentenceTransformer `max_seq_length=256`, tokenizer config 512, base positions 512,
384-dimensional output and a Normalize module. The loaded wrapper sets tokenizer
maximum to **256**. A 602-token input was observed to truncate to **256** through
the library's normal preprocessing. The new application bound is **240 total tokens,
including special tokens**, plus 4,096 characters. Explicit nontruncating tokenization
splits that input into three lossless chunks of 152/227/227 tokens; direct oversized
embedding is rejected and a valid chunk produced 384 dimensions. Evidence is in
`/tmp/polymind-phase17f-baseline/encoder.json`. Automated fixtures use bounded stubs;
the real offline observation does not impose a model-download requirement on CI.

## 23. Embedding/profile compatibility

Fingerprint covers pinned model/revision, dimension, normalization, token/character
bounds, independently versioned chunk profile, provenance schema and publication
schema. RetrievalEncoder rejects unsupported model/revision/dimension combinations,
checks runtime limits, validates each actual input immediately before encode, and
requests normalization. Nonfinite/wrong-size vectors fail. Reprofiling creates a
new candidate; rollback to a profile incompatible with the serving encoder fails.

## 24. Chroma integration

VectorFilter is an additive provider-neutral keyword parameter for query/list.
Only ChromaVectorStore translates it to `$eq`, `$in` and `$and`. Default unfiltered
calls remain compatible. Physical IDs include generation plus logical record ID,
so identical compatible records can exist in multiple generations. Exact logical
row inventory, source text and bounded metadata are checked before acceptance.
A real temporary local PersistentClient test proves pre-top-k generation/document
filtering, candidate isolation, listing, repeated upserts and read-only rejection.
No cloud Chroma was contacted, reset or restarted.

## 25. BM25 generation integration

PublicationReplica builds BM25Okapi once during explicit load/startup from the
validated manifest's exact record order, after verifying dense equality. Empty
revocation generations and all-tokenless corpora have an explicit empty sparse
index. The same existing tokenizer/stopword behavior is reused. Selected-document
filtering happens before sparse top-k selection. No request or readiness call
constructs BM25; tests replace both possible constructors with failure sentinels.

## 26. Dense/sparse coherence and version contract

For the document plane, expected corpus version **is exactly the manifest generation
UUID**; loaded sparse generation and dense filter must equal it and the authority's
active generation. There is no independent Chroma activation metadata alias to drift.
Legacy `BM25_CORPUS_VERSION` continues to govern only its isolated legacy collection.
These are explicitly distinct corpora, not two competing version pointers for one
corpus. API readiness retains legacy gates and additionally gates configured document
publication. Activation may temporarily leave no ready document replica until rollout.

## 27. Legacy compatibility

Legacy ingest/admin/chunking/dense/BM25/graph/source assembly remain unchanged.
The Phase 17 collection suffix prevents legacy unfiltered queries from seeing
candidates or canonical records. `/query`, `/query/stream`, source display and UI
contracts remain functional. Automatic blending of legacy rows into canonical
citations is intentionally not offered; legacy rows lack canonical authority.

## 28. Reprocessing

Same accepted compatible input and active record/digest inventory returns the
existing validated generation. Repeated candidate preparation repeats physical
upserts without duplicate logical records. New canonical bytes/version, extraction,
digest or retrieval/embedding compatibility produce different representations.
The canonical extraction contract already includes persisted execution identity;
Phase 17F does not rewrite it or pretend a newly extracted artifact is identical.

## 29. Supersession

The caller supplies complete desired accepted-job membership. A new version of
one logical document replaces that membership in the candidate, while the old
active generation remains available. Duplicate versions of one logical document
cannot coexist in a manifest. Failed writes/validation retain V1; successful
activation makes V2 the new admission target. Old manifests remain auditable.

## 30. Revocation

Administrative revoke builds a generation omitting selected logical documents,
prepares it and activates with the same fence. Revoking the last document yields
a valid empty generation. Dense filters, sparse membership, hybrid hits, reranking,
citations and new interactive requests all exclude revoked content. Explicit
selection of an absent document is rejected rather than widened. Canonical bytes
are retained; retention/deletion governance is not implemented.

## 31. Rollback validation

Rollback requires a previously ACCEPTED target, current expected generation/epoch,
compatible manifest, validated accepted documents/source/checkpoints, exact dense
inventory and sparse reconstructability. The same transactional authority records
the new epoch. Tests prove forward activation, rollback, lost-response retry and
refusal for missing dense rows or corrupted source, digest and manifest bytes.
Rollback intentionally can restore previously superseded/revoked membership only
through this explicit administrative operation.

## 32. COMPLETE/PARTIAL/FAILED/CANCELLED policy

Policy is COMPLETE_ONLY. PARTIAL is rejected even when the job completed; FAILED
and CANCELLED jobs never enter publication. Missing final manifests, corrupt digest
bytes and unresolved canonical evidence fail. Real accepted PARTIAL fixtures and
failed/cancelled jobs are tested. No partial content is silently upgraded, and no
API policy switch bypasses this boundary.

## 33. Canonical evidence resolution

EvidenceIndex checks document version, extraction, scope, source/block identity,
half-open spans, exact source text and real line coordinates. Reader validation
reconstructs records from verified accepted artifacts, rejecting a forged manifest
or row. Citation resolution reopens and verifies extraction and original source,
then issues bounded excerpts. A vector record ID or filename string alone is never
accepted as proof. Corruption fails closed; no fabricated fallback citation.

## 34. Hybrid retrieval

The document path reuses dense Chroma search, existing BM25 tokenization/Okapi,
RRF and the existing cross-encoder rerank function. It preserves independent dense-
only and sparse-only hits and does not apply the legacy relative-RRF cutoff, which
could drop a separate source side. All ranking remains bounded top-k retrieval,
not a claim of exhaustive whole-document coverage or semantic relevance certification.

## 35. Deduplication

New fuse_rankings uses stable publication record ID, retaining generation and all
provenance metadata. The same hit from dense/sparse receives both reciprocal-rank
contributions; repeated hits inside one path count once. Distinct records with
identical display source/chunk fields remain distinct. Legacy fallback identity
uses source/chunk. No text-similarity dedup removes opposing evidence.

## 36. Reranking

The existing reranker changes only score/order. The document adapter independently
checks returned IDs are from its retrieved set, unique, within top-k, within selected
scope, and carry unchanged generation/text/provenance metadata. Both the actual
rerank function with a fake cross-encoder and malicious metadata fixtures are tested.

## 37. Interactive analysis architecture and composition

DocumentAnalysis takes an explicit PublicationReplica, the existing provider's
bounded execute capability and an explicit CapabilityProfile. It admits/pins,
retrieves/reranks, resolves citations, assembles bounded source/derived context and
executes one tool-free structured call. It uses GENERAL's existing logical mapping,
not another inference client. It never routes source instructions into LangGraph
tools. No conversation memory is added to this dedicated analysis request.

Trusted composition, with operator-supplied stores/paths/scope and generation:

```python
from api.app import app, inference_provider
from documents.publication.service import PublicationReader, PublicationService
from documents.publication.retrieval import PublicationReplica
from documents.publication.analysis import DocumentAnalysis
from rag.vector_store_factory import create_publication_vector_store

# objects, jobs, authority, encoder and scope are explicit trusted components.
admin_vectors = create_publication_vector_store(administrative=True)
publisher = PublicationService(authority, objects, jobs, admin_vectors, encoder, scope)
candidate = publisher.plan(accepted_digest_job_ids)  # full intended corpus
publisher.prepare(candidate.generation)             # optionally via 17C handler
publisher.activate(candidate.generation)            # trusted admin operation

# Separate read-only vector access for serving. Set before FastAPI lifespan startup.
reader = PublicationReader(authority, objects, jobs,
    create_publication_vector_store(), encoder, scope)
replica = PublicationReplica(reader, expected_generation)
app.state.document_analysis = DocumentAnalysis(replica, inference_provider, capability)
```

Objects use existing LocalObjectStore and SQLiteJobLedger; publication authority is
SQLitePublicationAuthority with an explicit absolute path in an existing trusted
directory. Encoder is RetrievalEncoder(RetrievalProfile()). Capability and expected
generation are required operator inputs, not inferred deployment limits. Application
lifespan loads the configured snapshot and closes its serving vector resources.
The composing administrative caller owns admin client lifetime. Without composition,
the new analysis route fails closed; ordinary queries remain available. No default
runtime database, filesystem path, cloud adapter or auto-publication is installed.

## 38. Document selection and functional scope

AnalysisRequest requires 1–32 explicit document UUIDs and a bounded query. Selection
must be a nonempty subset of the pinned published membership. Dense filtering occurs
inside Chroma, sparse filtering before selection, and canonical citation scope is
checked again. Missing/revoked/foreign selections cannot silently expand the search.
Scope is supplied by trusted application composition; it is not proof of ownership.

## 39. API compatibility

Added `POST /documents/analyze`; no mutation endpoints. Existing QueryRequest,
query responses, Streamlit source assumptions and NDJSON streaming are unchanged.
The new route requires opt-in service composition, returns bounded canonical
citations and normalized errors, and does not accept uploads or runtime store paths.
Invalid functional scope maps to 422; unavailable publication/provider evidence
fails safely. Existing application security middleware also covers this route,
but its shared bearer token is not document-level authorization.

## 40. Citation representation

Each request receives C1, C2, ... IDs generated by application code. Citation carries
generation, record, document/version and extraction IDs, display source, structural
path, canonical page or line/span, bounded exact excerpt, `provenance=validated`,
and `semantic_support=not_evaluated`. Plain text never receives a fabricated page;
synthetic native PDF tests preserve actual physical ordinals 1 and 2.

## 41. Citation validation

Model output must satisfy an extra-forbidden bounded schema and return only IDs
supplied for that request. Foreign IDs, duplicate IDs and available answers without
citations fail. Canonical objects are validated again before returning the result.
Citation coordinate/source fields are issued by application code, not copied from
model prose. Unstructured answer text is not parsed as authoritative citation metadata.

## 42. Citation validity versus semantic support

The implementation enforces request membership and canonical resolution. It does
not decide whether the cited passage entails the answer. A deliberately irrelevant
question/structurally valid citation fixture still reports `not_evaluated`, never
semantically verified. Real-model hallucination, faithfulness, contradiction
recognition and relevance thresholds remain Phase 17H evaluation work.

## 43. Original versus derived context

ORIGINAL_SOURCE_EVIDENCE contains canonical citations/excerpts. The separately
labelled DERIVED_RETRIEVAL_MATERIAL contains generated qualifications, conflicting
findings and their links, limitations and open questions. Generated summaries are
not searchable source records and cannot become original quoted evidence. Both
sides of explicitly recorded contradictions and exact qualifications are retained.
If this context exceeds the configured bound, analysis rejects instead of silently
truncating away conflicting information.

## 44. Prompt-injection and insufficient evidence

System control and data are separate GenerationRequest fields. The system explicitly
treats source text, filenames and annotations as untrusted. No tools are supplied
or executable; forged structured citation IDs are rejected. Injection fixtures
remain in the data field. Prompt wording is not a semantic security certification.
No hits returns an insufficient-evidence response without inference. Model output
can explicitly represent available, insufficient, conflicting or incomplete evidence.
Top-k context is identified as selected excerpts, not full-document knowledge.

## 45. Crash/recovery tests

Tests interrupt before any write, after a row, after all rows, after validation,
before activation and immediately after activation. Fresh authority instances resume
from durable manifests and repeat upserts idempotently. Revocation and rollback are
interrupted on both sides of activation. Previous knowledge remains active before
the transaction; committed activation survives a lost response afterward. Failures
record a sanitized category. Orphan/inactive physical rows are discoverable without
cleanup; active inventory corruption is a hard reconciliation/readiness failure.

## 46. Readiness

Configured document replicas join `/ready`'s existing dependency gates. Expected,
active and loaded document generations must match and the active inventory/manifest/
provenance must validate. `/health` stays liveness-only. Startup failures leave the
process alive and unready. Readiness never writes authority state, repairs vectors
or rebuilds BM25. Request admission also gates generation, so bypassing a load
balancer cannot produce mixed dense/sparse answers.

## 47. Observability and bounded observations

Existing normalized vector metrics cover adapter operations. Added startup logging
contains only a bounded unavailable message; no source, query, answer, prompt,
evidence or embedding content is logged. Readiness includes expected/loaded document
generation as payload fields, never metric labels. No new high-cardinality metrics.

One 300-unit synthetic text document, with stub embeddings, produced 300 records
and a **257,265-byte manifest**. Planning 1.046 s; candidate preparation 1.166 s;
validation 0.996 s; validated activation 1.040 s; validated snapshot load 1.040 s;
eight-citation resolution 0.020 s. There were **300 publication embedding calls plus
one query call**. Timings include conservative graph verification, not just the SQL
CAS or BM25 constructor. This is a bounded scaling observation, not a real 300-page
benchmark, production SLO or Phase 17H certification. Raw observations are outside
the repository in the baseline directory.

## 48. Security and Phase 17G deferral

Functional selection is not authorization. No authenticated document ownership,
tenant isolation, cross-user protection, retention/deletion governance, monetary
quota or cost enforcement is claimed. Database files use private creation mode
and reject obvious symlinks/special files/incompatible schemas in a trusted directory;
this is not hostile-host isolation. Do not expose trusted document composition to
external users before the Phase 17G controls and later verification gates.

## 49. Files created

19 files:

- `docs/codex/prompts/phase_17f.md`
- `docs/codex/reports/phase_17f_report.md`
- `documents/publication/__init__.py`
- `documents/publication/models.py`
- `documents/publication/encoding.py`
- `documents/publication/planning.py`
- `documents/publication/authority.py`
- `documents/publication/service.py`
- `documents/publication/workflow.py`
- `documents/publication/retrieval.py`
- `documents/publication/analysis.py`
- `tests/unit/publication/conftest.py`
- `tests/unit/publication/test_planning.py`
- `tests/unit/publication/test_lifecycle.py`
- `tests/unit/publication/test_retrieval.py`
- `tests/unit/publication/test_analysis.py`
- `tests/unit/publication/test_api.py`
- `tests/unit/publication/test_workflow.py`
- `tests/integration/test_publication_chroma.py`

## 50. Files modified and deleted

Modified six existing files: `README.md`, `api/app.py`, `rag/vector_store.py`,
`rag/chroma_store.py`, `rag/vector_store_factory.py`, `rag/hybrid_retriever.py`.
Deleted files: **none**. Prior reports/prompts, job and digestion implementations,
legacy ingestion, memory, provider adapters, deployment and dependencies are intact.
README retains the refreshed organization/badges and limits its edits to real 17F
capabilities, status, usage/readiness notes and report links.

## 51. Targeted Phase 17F results

Incremental runs: initial planning 4 passed; lifecycle 16 passed; retrieval 4 passed;
analysis 8 passed; expanded combined publication tests 38 passed; real Chroma plus
expanded planning 8 passed; expanded planning/API 10 passed; consolidated new suite
46 passed in 40.19 s. Final retrieval/API focused run passed 10 in 13.82 s. One
additional dense-only/sparse-only case and final source review fixes are included
in the final complete suite: **47 new Phase 17F tests pass**. These overlapping
runs must not be added together. All fixtures are synthetic and locally scoped.

## 52. Existing RAG regression results

Vector-store, retrieval, deployment-topology/BM25 and model-artifact groups:
**39 passed in 19.72 s**. The full suite additionally includes all existing related
observability/security/deployment tests. Real Chroma filtering is independently
covered by the new temporary local adapter contract, with no configured runtime
collection access.

## 53. Phase 17B–17E regression results

`tests/unit/documents` plus document-plane, job, digestion and managed-digestion
integration suites: **261 passed in 46.68 s**. The structured-provider tests are
also included in the following provider group. No earlier document contract was
weakened or schema migrated.

## 54. API/provider/streaming and full suite

API reliability, streaming orchestration, provider contract, Ollama, compatible
provider, structured provider, provider readiness, memory, routing and UI-client
group: **213 passed in 1.76 s**. Final `python -m pytest -q`:
**590 passed in 100.71 s**, no failures or skips. Log:
`/tmp/polymind-phase17f-baseline/full-suite.log`. All final production code and test
changes precede this run; subsequent repository edits are documentation only.

## 55. Compile/config/diff validation

`PYTHONPYCACHEPREFIX=/tmp/polymind-phase17f-pycache python -m compileall -q .`:
PASS. `docker compose config --quiet`: PASS. `git diff --check`: PASS.
No deployment settings/chart contracts changed; existing Helm tests pass in the
complete suite. Additional offline `helm lint deployment/helm/polymind` passed
(one chart, icon recommendation only), and `helm template polymind
deployment/helm/polymind` passed. No Kubernetes API was contacted. No Docker build is required for unchanged dependencies/images/
Docker configuration. No configured linter/type checker was found or installed.
Final documentation and inventory validation are recorded below before handoff.

## 56. Self-review and pre-commit findings

Review fixed accidental sparse reconstructability work on the readiness path;
readiness now only verifies, never constructs BM25. It normalized unordered 17D
checkpoint/qualification sets when replaying final acceptance, so cross-process
iteration ordering cannot change evidence validity. It enabled deliberate active
corpus reprofiling while retaining rollback compatibility rejection, reused semantic
candidate identity across compatible audit job IDs, preserved canonical reading
order, retained opposing finding text as derived annotations, and rejected reranker
injected/duplicate IDs. Tests cover these boundaries and the full suite passes.

The complete existing-file diff and all new source/test files were reviewed for
scope, resource lifetimes, stale activation, ABA, mixed snapshots, provenance,
source/derived separation, bounds, admin exposure and provider leakage. The separate
artifact review found no credentials/private keys, private documents, real `.env`,
SQLite/runtime DB files, generated bytecode/cache files, debug logging, new dependencies
or machine-specific paths in changed Python. Temporary test/model observations stay
outside Git. Secret checks are heuristics, not a security certification.

## 57. Remaining limitations

SQLite and LocalObjectStore remain local reference implementations, not production
AKS shared state. Whole-generation retention costs storage. Cleanup and automatic
hot reload are absent. Readiness and request admission conservatively revalidate
the whole accepted graph/dense inventory, so larger-corpus latency needs Phase 17H
measurement and a future integrity-preserving optimization. No quality-calibrated
retrieval threshold or semantic faithfulness check exists. A valid citation can be
irrelevant; the response explicitly says semantic support was not evaluated.

The v1 publication profile excludes PARTIAL and generated retrieval records.
Oversized context/query fails explicitly rather than truncating. Native extraction
and table/visual limitations remain. Application composition is explicit; no default
runtime paths, public upload, auto-ingestion or automatic document-plane deployment
is created. Stronger distributed transactions/replica infrastructure, external-user
security and large-scale reliability remain unimplemented, not hidden PASS claims.

## 58. Phase 17E Foundry pending gate

Phase 17E application integration and OpenAI-compatible/external-vLLM/OpenAI-style
protocol compatibility remain PASS. **Live Azure Foundry document-digestion validation
remains BLOCKED / pending.** Phase 17E had no endpoint/model-map/provider/key
configuration and made zero live digestion calls. Phase 17F made zero live calls,
retrieved no credentials and did not alter that status. Preserve this gate for 17H.

## 59. Exact Phase 17G prerequisites

Next phase: **Phase 17G — Multi-User Security, Quotas & Cost Governance**.
It must replace trusted scope with authenticated ownership and enforce document,
retrieval, publication and session authorization, including the new analysis route.
Define sharing/tenant isolation, retention/deletion/revocation and rollback policy,
per-owner quotas, cost/usage governance and appropriate trusted administration.
Preserve generation pinning, CAS, immutable provenance and the pending live-model/
semantic-quality gates. Distributed production adapters need their own approved
scope. No Phase 17G, 17H, 17I or Phase 18 implementation was started.

## 60. Final Git state and prohibited actions

Starting/final HEAD: `cb70b26f8de8db1f4e9285d49e4434dbf0ed5004`; branch `master`.
19 created, six modified, zero deleted files; all remain uncommitted and unstaged.
Starting committed baseline and intentional README history are preserved.

Commit created **NO**. Push performed **NO**. Branch created **NO**. Azure mutation
**NO**. Foundry capacity change **NO**. Kubernetes mutation **NO**. Cloud Chroma
reset/restart **NO**. vLLM deployment **NO**. GPU provisioning **NO**. OCR integration
**NO**. Production multi-user authorization claim **NO**. Semantic entailment
certification claim **NO**. Secret exposure **NO**. Private document added **NO**.

Final handoff validation: compileall, Compose configuration and diff check each
returned exit 0; Helm lint/template returned exit 0. Artifact/link checks cover all
new and modified files, with intentional inherited Markdown hard line breaks
excluded from the new-file whitespace heuristic. All **216 unchanged baseline
files** match their starting hashes. Index remains empty. Final tracked diff stat
(excludes the 19 untracked new files):

```text
 README.md                   | 36 ++++++++++++++++++++----------------
 api/app.py                  | 36 ++++++++++++++++++++++++++++++++++++
 rag/chroma_store.py         | 19 ++++++++++++++-----
 rag/hybrid_retriever.py     | 23 +++++++++++++++++++++++
 rag/vector_store.py         | 10 ++++++++--
 rag/vector_store_factory.py |  8 ++++++++
 6 files changed, 109 insertions(+), 23 deletions(-)
```

Final status is `master...origin/master`, with precisely those six modified files,
the new prompt/report, `documents/publication/`, `tests/unit/publication/`, and
`tests/integration/test_publication_chroma.py` untracked. Detailed expanded
inventory and validation outcomes are retained outside the repository in
`/tmp/polymind-phase17f-baseline/final-audit.json`.
