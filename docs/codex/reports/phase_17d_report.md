# Phase 17D — Hierarchical Evidence-Grounded Digestion

Date: 2026-10-07. Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`.
Branch: `master`. Task: [finalized prompt](../prompts/phase_17d.md).
Foundations: [Phase 17B](phase_17b_report.md), [Phase 17C](phase_17c_report.md).
Architectural authority: [Phase 17A](phase_17a_report.md).

## 1. Executive summary

Implemented a local, provider-neutral digestion package that builds a deterministic
structural map, separate analysis chunks and a complete reduction DAG before
admission. The existing Phase 17C worker executes the plan with deterministic fake
inference, immutable checkpoints and validated original-source evidence. Final
artifacts preserve findings, qualifications, conflicts, questions, section/root
synthesis, coverage and checkpoint lineage.

The implementation adds no scheduler, storage adapter, provider API, dependency,
public endpoint or deployment. All Phase 17B/17C implementation and tests remain
byte-identical to the starting baseline. The only modified existing file is README.

## 2. Phase result

**Phase 17D — PASS.** The local structural, evidence, resource-bound, coverage and
durable execution acceptance boundary is validated. The final full suite passed
**446 tests in 39.02 seconds**. Closure resumed after an execution usage limit;
implementation and test files were unchanged after that run, so the successful
result was retained rather than unnecessarily rerun.

This is structural quality validation with deterministic fake inference. It does
not establish real-model semantic accuracy, Foundry document inference, quotas,
publication, production authorization, 1,000-page production reliability or
completion of Phase 17. Phase 17E has not started.

## 3. Starting worktree state

HEAD was and remains `f9b47fda4658935b64826f1d4abe0488c64f21ae`, on `master`.
Starting status, recorded before edits:

```text
## master...origin/master
 M README.md
 M docs/codex/reports/phase_16_report.md
?? docs/codex/prompts/phase_17a.md
?? docs/codex/prompts/phase_17b.md
?? docs/codex/prompts/phase_17c.md
?? docs/codex/reports/phase_17a_report.md
?? docs/codex/reports/phase_17b_report.md
?? docs/codex/reports/phase_17c_report.md
?? documents/
?? tests/integration/
?? tests/unit/documents/
```

`/tmp/polymind-phase17d-baseline` contains copies and SHA-256 inventory of **202**
tracked/unignored files, status, HEAD, tracked diff stat and the empty index diff.
The starting tracked stat was **1,671 insertions / 1 deletion** across README and
the Phase 16 report; those are accumulated prior changes, not Phase 17D work.
Closure verified every baseline file unchanged before updating README. Final
baseline comparison permits only that intentional cumulative README update.

## 4. Scope and exclusions

Included structure, chunking, fixed hierarchy, bounded structured inference,
deterministic fake behavior, source evidence/claim lineage, qualifications,
contradictions, coverage, partial/failure policy, immutable artifacts and integration
with existing durable execution. Excluded every real model/provider call, cloud
operation, cluster mutation, OCR integration, retrieval publication, authentication,
queue/database deployment, paid infrastructure and external document testing.

Serving APIs, LangGraph, RAG chunking/retrieval/source assembly, inference adapters,
Redis, Chroma, Docker, dependencies and configuration files are unchanged.

## 5. Existing 17B/17C foundations used

Phase 17B supplies frozen canonical documents, extraction versions, ordered source
units/blocks, Unicode spans, EvidenceRef, verified source/artifact ObjectRefs,
serialization and the immutable local object store. Digestion retains these
identities; it does not introduce another evidence coordinate system.

Phase 17C supplies Admission, ProcessingProfile, StepSpec, DocumentJobs, JobLedger,
SQLiteJobLedger, Worker, IntentStore, LocalDispatcher, relay, retry policy, leases,
fences, manifests, outbox, cancellation and compatible checkpoint reuse. No old
source file or SQL schema was changed. Scope remains trusted caller context, not
authentication.

## 6. Digestion architecture

```text
Verified canonical extraction
  -> deterministic structure/chunks/reduction plan
  -> immutable plan object and Phase 17C admission
  -> planning checkpoint
  -> bounded chunk analyses
  -> structural/batch reducers and root
  -> evidence + lineage + coverage validation
  -> immutable digest and coverage manifest
```

`prepare()` plans and stores immutable plan bytes. `admit()` verifies those bytes,
reconstructs the plan from the canonical artifact and submits the fixed DAG through
DocumentJobs. `DigestionHandler` is an injected StepHandler; `load_digest()` exposes
only an accepted final manifest. There is no autonomous daemon or new scheduler.

The entire DAG is knowable before inference. Dynamic fan-out is unnecessary.
LangGraph adds no useful durability here, so the explicit planner/reducers are
used without it. Existing application LangGraph remains unchanged.

## 7. Structural document model

StructuralMap carries schema, extraction ObjectRef/hash, document version, profile
fingerprint and ordered StructuralUnits. Units carry stable UUIDs, parent/children,
order, kind, heading/path, source/confidence classification, canonical block/source
IDs and physical pages. Source spans and evidence resolve through those canonical
block IDs and the extraction reference; they are not duplicated as a new model.

The root inventories physical pages and source units, including unavailable pages.
Parent links, child order, reachability, duplicate IDs and cycles are validated.
Structure uses `structure/1`; confidence is a categorical source declaration or
fallback marker, never a calibrated model probability.

## 8. Structural segmentation

Explicit canonical heading blocks establish sections. Heading parent links establish
subsections; text can explicitly refer back to a parent heading. Forward, cyclic or
non-heading parent relationships that make the hierarchy ambiguous are rejected.
Native extraction does not discover semantic headings, so ordinary native PDF/text
uses a marked deterministic fallback with canonical page/block boundaries retained.

No formatting heuristic invents headings. Discontiguous parent-owned text is chunked
in canonical reading order, including text following a subsection. Reducer inputs
are ordered by the earliest source position of their children.

## 9. Analysis chunk model

AnalysisChunk includes its schema, stable chunk ID, document version, structural
parent/path, sequence, profile fingerprint, ordered SourcePieces, estimated input
size and overlap metadata. Each piece contains an original Phase 17B EvidenceRef,
exact source text, block kind and available cells/limitations.

The application-owned `evidence_id()` accessor deterministically identifies the
supplied EvidenceRef. The fake selects IDs through that accessor; it does not
invent source coordinates or arbitrary citation IDs. Returned IDs are independently
checked against the permitted input set. Analysis chunks never enter RAG or an
embedding encoder in this phase.

## 10. Chunking algorithm

Adjacent blocks with the same structural owner are packed within explicit character
and serialized-request budgets. Complete small blocks stay intact. Oversized text
splits deterministically, preferring available newline boundaries; if metadata and
escaped content exceed the request budget, a fragment is reduced further until it
fits or even the minimum request is impossible. No text is trimmed or normalized.

Exact half-open spans and plain-text line coordinates accompany every fragment.
Canonical ordering is preserved across parent/subsection transitions. Version 1
uses **zero overlap**; overlap metadata is explicitly empty. Coverage nevertheless
uses interval union and has a duplicate-span accounting test.

## 11. Planning/token-budget model

DigestionProfile requires explicit context, reserved output, template, chunk,
fan-in, result, claim/text/annotation, source-unit, chunk, step, artifact-byte and
depth limits. It also requires a coverage threshold and allowed failed-unit count.
There are no implicit production token sizes. DigestionSettings accepts an explicit
profile through `DOCUMENT_DIGESTION_PROFILE` or nested environment settings.

The neutral estimator uses one canonical JSON character per estimated token,
including escaped Unicode, source/evidence metadata, profiles and paths, plus
explicit template overhead. Reserved output must cover the configured serialized
result bound. These are deterministic planning units, **not actual provider usage**.

Reducer planning reserves the maximum child-result size plus bounded reference/
metadata allowance, and conservative request/path overhead. Effective fan-in is
the smaller of configured fan-in and budget capacity. Actual requests are checked
again before inference and output acceptance. An impossible budget fails explicitly.

## 12. Inference contract

`SynthesisInference.analyze(StageRequest) -> bytes` returns structured JSON.
StageRequest separates immutable instructions/profile metadata from source data
and generated child material. It includes stage identity, role, prompt/output
schema versions, path, permitted evidence, child artifact hashes and inherited
coverage/annotation summaries. No endpoint, deployment, secret or provider syntax
appears in this contract.

The returned bytes are only an encoding boundary: schema, size, evidence and lineage
validation are mandatory before a StageResult becomes a checkpoint. No arbitrary
prose parser or malformed-output repair is used.

## 13. Fake deterministic inference

FakeInference emits predictable generic findings and lineage-based reducer
commentary. Explicit operator fixtures supply synthetic propositions and exact
qualifications; the fake does not infer linguistic meaning. Fixture configuration
is fingerprinted in the inference profile. Document instructions are never parsed
as control instructions.

Fault modes include a first-call interruption, permanent stage failure and an
explicit unavailable analysis result. Successful retries reproduce the same
structured result. Counters are fault-fixture state only; the ledger owns actual
retry scheduling, attempts and acceptance. No model/client/network implementation
is imported or invoked.

## 14. Chunk analysis schema

StageResult uses `stage-result/1` with an analysis/reduction kind discriminator,
stage ID, analyzed/unavailable outcome, bounded claims, questions and limitations.
An unavailable analysis must have no claims and an explicit limitation. An analyzed
chunk must account for every permitted source piece. Unknown fields, duplicate
JSON keys, malformed IDs, invalid origins, oversized values and unsupported schema
versions are rejected. Models are frozen, collections are tuples and non-finite
numbers are forbidden.

## 15. Claim model

Claims include stable claim ID, originating stage, text/type, supporting and
contradicting source IDs, qualifications, child claim links, status and optional
structured subject/stance. Factual claims need source support directly or through
validated inherited lineage. Unknown, unsupported, structural and commentary
classes are explicit. There is no confidence score.

Final artifacts retain exact leaf findings, root synthesis claims, inherited
qualifications and all checkpoint links. Claim IDs derive from stage identity and
position; retries cannot change origin or manufacture another stage's claims.

## 16. Evidence validation

EvidenceIndex builds source/block lookup once and checks scope, document version,
extraction identity, source/block association, span bounds, exact text and line
coordinates. Its indexed resolver preserves Phase 17B semantics; integration tests
also use the original Phase 17B `resolve()` after reopening storage.

Application validation rejects fabricated IDs, existing but foreign evidence,
wrong scope/version/extraction, invalid spans, duplicate references and citations
outside the current permitted set. Invalid output never receives an accepted
analysis manifest. Finalization revalidates all accepted stages and reinspects
canonical/plan object integrity before accepting a digest.

## 17. Evidence inheritance

Reducer inputs identify exact immutable child artifacts and expose their bounded
results and inherited metadata. Output claim links must cover **all** supplied
child claims. Direct citation IDs must occur in the supplied source/child claims;
other inherited support is carried through validated claim links.

The application retains the full original-source graph outside the bounded model
request. Every root claim can be traversed through checkpoint claim links to original
EvidenceRefs. The fake cannot drop a child claim or create a foreign source set.
Generated intermediate artifacts are explicitly classified as generated material,
never as direct source evidence.

## 18. Hierarchical reducer architecture

Chunks reduce within structural owners, subsection results feed parent sections,
and the document root reduces their ordered outputs. Weak structure uses recursive
batch reduction. Checkpoints retain parent ObjectRefs/hashes, result schema, plan
hash, inherited annotation/coverage counts and structured proposition state.

The application merges inherited proposition state and retains original qualifiers.
This prevents recursive summary text from becoming the authority for evidence or
qualifications. Model requests remain bounded even as original-source lineage grows
in immutable artifacts. Final validation traverses the accepted claim graph.

## 19. Fan-in/reduction tree

Tests exercise one child, exact fan-in, fan-in plus one and multiple recursive
levels. A tighter input budget produces additional levels rather than truncation.
A one-child structural/root reducer is legitimate. IDs depend on extraction,
profile, structural owner and ordered children, not worker, time or attempt.

The unchanged Phase 17C admission cap remains **1,000 steps**. Digestion has explicit
limits within that cap and fails planning before admission if they are exceeded.
Thousands of logical source units can still fit by packing several into bounded
chunks. This is not a claim that every 1,000-page document fits the local plan cap.

## 20. Qualification preservation

Synthetic “System improved performance” / “only under low load” fixtures prove
that the exact qualifier and original evidence survive all reducer levels. Child
claim links are mandatory, inherited qualification counts are application-owned,
and the final artifact retains qualifications explicitly as well as on leaf claims.
A reducer cannot erase them by omitting words from its generated summary.

This proves structural retention, not semantic entailment of future model wording.
Any later renderer must present applicable qualifiers alongside generated claims.

## 21. Contradiction handling

Fixtures declare opposing affirmed/denied statements for one structured subject.
Both claims and evidence survive. Application-owned proposition propagation records
an unresolved conflict when opposing sides meet and carries that state to the root.
Final Contradiction records name both sets of original claim IDs and remain
`unresolved`; the fake never silently selects a winner.

There is no general natural-language contradiction detector. Subject/stance fixtures
prove the contract; extracting and evaluating real propositions belongs to later
managed-inference and quality work.

## 22. Unknown/open-question handling

Unknown claims keep their explicit class/status. Questions and limitations are
retained across checkpoints and collected in the final artifact. Unsupported source
inventory produces an explicit missing-content question; conflicting propositions
produce an unresolved-conflict question. Absence is never rewritten into a source
fact. An all-unavailable analysis run cannot accept a final digest.

## 23. Coverage model

Coverage inventories canonical block IDs, using a source-unit ID for units without
blocks. It records eligible, analyzed, failed, skipped, unsupported and included IDs,
plus a measured fraction. A split block counts as analyzed/included only when the
union of its successful spans covers the entire original block. Duplicated spans
do not inflate counts.

The denominator is eligible plus unsupported units. Known blank units are explicitly
skipped by policy. Failed/OCR/manual-review/layout-required/unsupported canonical
units are conservatively unavailable to this native-only profile. Analysis failures
are separately recorded in `failed`; canonical extraction failures appear in
`unsupported`. Piece counts passed to reducers are not final canonical coverage.

## 24. Completion/partial/failure policy

COMPLETE requires full eligible coverage, no failed or unsupported units, a complete
validated reduction tree and the configured threshold. PARTIAL additionally requires
explicit permission, nonempty included coverage, the configured threshold and the
allowed failed-unit count. It retains available findings and missing-unit lists,
and carries a warning that it is not complete publishable knowledge.

A failed coverage decision can be represented by the pure digest builder as FAILED;
the durable handler rejects that final artifact and Phase 17C records a FAILED job.
Evidence/contract/integrity/planning failures also fail safely. There is no accepted
final digest for a failed or cancelled workflow.

Phase 17C COMPLETED means computational workflow completion. An accepted PARTIAL
digest therefore belongs to a COMPLETED workflow with **digest status PARTIAL**.
This distinction is explicit, tested and preserves the existing ledger contract;
consumers must inspect digest status, not infer publication quality from job state.
No publication path exists.

## 25. Checkpoint artifacts

Schemas include `structure/1`, `analysis-chunk/1`, `digestion-plan/1`,
`stage-request/1`, `stage-result/1`, `synthesis-checkpoint/1`, `coverage/1` and
`document-digest/1`. Analysis and reduction share a discriminated result schema.
The plan checkpoints both structural map and chunk/reduction plan. Each analysis
and reducer has its own checkpoint; finalization accepts digest and coverage refs.

Sorted compact JSON, explicit versions and validated finite data produce deterministic
bytes. Duplicate keys are rejected. Objects are content-derived, scoped and
immutable through the existing store. Checkpoints bind exact parent artifact hashes;
old bytes are never migrated or overwritten in place.

## 26. Phase 17C orchestration integration

The adapter deliberately uses existing NORMALIZING for computational digestion
steps and VALIDATING for finalization. Unit IDs and schema versions distinguish
planning, analysis and reducers. This avoids changing stage vocabulary, SQLite
schema or prior Phase 17C files merely for new progress labels.

The fixed plan is admitted by DocumentJobs. Worker uses IntentStore to register
writes, inspect bytes and conditionally commit under existing leases/fences.
Outbox, reconciliation, cancellation and attempts retain their original authority.
An immutable plan cache improves local execution but never owns accepted state;
a fresh handler rebuilds it from verified persisted artifacts.

## 27. Retry/cancellation/resume

A first-attempt synthetic interruption enters RETRY_WAIT, retains step identity and
request, and accepts one manifest on the second attempt. The test compares the
accepted result with a fresh fault-free fake. Persisted attempt outcomes are
RETRY_WAIT then SUCCEEDED.

Cancellation is tested during analysis, intermediate reduction, root synthesis and
finalization. In-flight output cannot be accepted after cancellation; downstream
work stops and prior manifests remain unchanged. Written-but-uncommitted synthesis
followed by lease expiry/recovery reproduces the same object and rejects the old
fence's late commit.

Reducer failure produces a terminal failed run. A compatible resumed run copies
accepted checkpoint references with `reused_from`, dispatches unfinished reducers,
and performs zero repeat analysis calls. Corrupt analysis bytes prevent reuse.
Old failure/attempt records remain intact.

## 28. Profile/version compatibility

Plan identity includes canonical extraction/hash, all structure/chunk/inference/
reducer/prompt/schema identifiers, budgets, policy and fixture configuration.
Step config fingerprints seal the plan; activation additionally seals parent
manifest hashes using Phase 17C. Changed chunking, inference or reducer profiles
produce different IDs/specs and reuse no incompatible checkpoints.

Accepted unavailable-analysis checkpoints are immutable outcomes. Replaying that
same compatible plan preserves those outcomes; deliberately reevaluating them
requires a new incompatible profile/plan. Selective repair of already accepted
partial analyses is not a new scheduler feature in this phase.

## 29. Input/output resource bounds

Every fake request is measured before execution and again during validation.
Result bytes, claims, strings and per-result annotations have explicit caps.
Source inventory, chunks, steps, hierarchy depth and stored object bytes are also
bounded. Growing provenance/proposition/final arrays are bounded by the admitted
source/step/claim limits and artifact-byte limit; they are not all copied into a
root inference prompt.

Canonical artifacts and final validation are still bounded in-memory operations.
Serialization checks do not provide OS memory, CPU or wall-clock isolation. The
existing worker requires lease renewal supervision for genuinely long steps;
no automatic heartbeat or subprocess sandbox was added.

## 30. Security/prompt-injection boundary

Document text lives only in `source_data`; fixed instructions, profiles and the
empty tools contract are separate. Adversarial fixtures include ignoring prior
instructions, deleting a database and requesting another tenant's document.
They remain inert source text. There is no tool execution or external inference
implementation in digestion.

No source/generated content or operational secret is logged. Errors are sanitized
at the workflow boundary. Scope remains a trusted domain input, not proof of user
identity. Public uploads and production multi-user access remain out of scope.

## 31. Tables/figures/unextractable content

Small structured tables retain existing cell data and exact references. Unparsed
tables/figures retain source text/references and `visual_uninterpreted` limitations;
no cells or image descriptions are fabricated. Oversized unstructured text can be
hard-split with an explicit limitation.

Phase 17B cells lack row-to-text span mapping. A structured table that cannot fit
whole is therefore rejected with a size-limit error rather than inventing a safe
row split. Native extraction still does not parse headings/tables or perform OCR.
A mixed fixture contains one native page, failed/OCR/manual-review pages and a blank:
coverage is **1/4**, with **3 unsupported** and **1 skipped**; explicit policy yields
PARTIAL or FAILED as tested. COMPLETE describes accounted native source coverage,
not visual interpretation or real semantic quality.

## 32. Error model

DigestionError has content-free categories for structural planning, analysis,
reduction, evidence validation, coverage, inference contract, synthesis limits and
checkpoint incompatibility. `classify_digestion` maps them into Phase 17C's existing
allowlist: invalid_document, invalid_reference, serialization_error,
extraction_limit_exceeded, profile_mismatch or extraction_failed. No ledger taxonomy
or retry framework was duplicated or changed.

Synthetic transient interruption uses existing worker_interrupted classification;
permanent domain/validation failures do not retry automatically. Unknown exceptions
remain sanitized by the existing worker classifier. Raw Pydantic exceptions remain
internal construction errors, not a public API contract.

## 33. Large synthetic document tests

Synthetic text fixtures represent 200, 500, 1,000 and 1,200 canonical logical blocks,
with short bodies and four blocks per analysis chunk. All achieve exact full source
coverage and retain one original evidence reference per logical block. No private,
copyrighted or generated binary document was committed.

These are structural/reduction tests with immutable local checkpoints, not 200–1,200
real-page quality tests or large durable SQLite throughput certification. Actual
native multipage PDF extraction is tested separately through the durable workflow.

## 34. Performance observations

Measurements from the final targeted JUnit artifact, excluding fixture extraction:

| Logical units | Chunks | Reducers | Levels | Planning seconds | Planning + fake/checkpoints seconds | Checkpoint bytes |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 200 | 50 | 19 | 4 | 0.162 | 0.574 | 129,218 |
| 500 | 125 | 44 | 5 | 0.383 | 1.398 | 319,321 |
| 1,000 | 250 | 85 | 5 | 0.762 | 2.775 | 635,215 |
| 1,200 | 300 | 103 | 6 | 0.930 | 3.350 | 763,640 |

These are local observations, not production throughput or SLOs. Source/block
lookup is indexed; line lookup uses newline indexing; coverage uses interval union;
claim traversal uses visited sets. Plan fingerprints and node indexes are cached
within execution. Proposition propagation is bounded by hierarchy depth.

Phase 17C's reference ledger still scans bounded per-job state during transitions,
and its worker/service reads step inventories. Total durable scheduling can have
quadratic work in step count. The existing 1,000-step cap is retained; this phase
does not claim to optimize or certify that scheduler for production scale.

## 35. End-to-end integration evidence

A generated six-page native PDF runs through actual Phase 17B extraction, Phase
17D planning, Phase 17C admission/dispatch/worker, fake analyses and multi-level
reducers, final evidence/coverage checks and accepted immutable digest. Every step
has one attempt, coverage is **6/6**, and digest status is COMPLETE.

A fresh SQLiteJobLedger and LocalObjectStore reopen accepted state. The stored plan
matches, the canonical artifact is identical, and every final EvidenceRef resolves
through the original Phase 17B resolver to its synthetic page text. No network,
Foundry, Chroma, cloud storage or external OCR is involved.

## 36. Failure/resume integration evidence

All six analysis steps succeed before an injected first reducer fails. The run is
FAILED. A fresh ledger admits a compatible resumed run; successful analyses retain
identical ObjectRefs, record origin steps and have zero new attempts. A fresh fake
records no analysis calls; only unfinished reduction/finalization runs, and the
new digest is COMPLETE. The original failed run remains FAILED.

The ledger has one accepted manifest per originating analysis step. Resume creates
reference/audit rows for the new run, not duplicate analysis objects or repeated
computation. Corruption, profile changes, cancellation and stale writes have
separate negative integration cases.

## 37. Exact files created/modified

Created **11 files**:

```text
documents/digestion/__init__.py
documents/digestion/codec.py
documents/digestion/inference.py
documents/digestion/models.py
documents/digestion/planning.py
documents/digestion/validation.py
documents/digestion/workflow.py
tests/unit/documents/test_digestion.py
tests/integration/test_document_digestion.py
docs/codex/prompts/phase_17d.md
docs/codex/reports/phase_17d_report.md
```

Modified existing file: **README.md only**, for cumulative Phase 17D status and a
report link. Phase 16 report, all Phase 17A–17C prompts/reports, existing document/
job modules and existing tests remain byte-identical to the pre-17D baseline.

## 38. Targeted tests

Final Phase 17D tests: **66 passed in 20.61 seconds**:

```bash
python -m pytest tests/unit/documents/test_digestion.py tests/integration/test_document_digestion.py -q -o junit_family=legacy --junitxml=/tmp/polymind-phase17d-targeted.xml
```

Unchanged Phase 17B/17C tests: **149 passed in 4.09 seconds**, covering canonical
contracts/extraction/storage, ledger and both previous integration modules.
Selected serving/retrieval/vector/routing/API/OpenAI-compatible/Ollama/streaming
regressions: **121 passed in 14.63 seconds**. These overlap the full suite; counts
must not be added to 446. Logs are under `/tmp/polymind-phase17d-*.log`.

## 39. Full-suite/static validation

`python -m pytest -q`: **446 passed in 39.02 seconds**, no failures or skips.
This is all 380 baseline tests plus 66 Phase 17D tests. The preserved log is
`/tmp/polymind-phase17d-full.log`. At closure, source/test modification times precede
that completed log, the session records no subsequent implementation changes,
and closure hashes preserve the tested files. The successful run is reused as
explicitly requested by the operator.

Already executed successfully on the final code:

```bash
PYTHONPYCACHEPREFIX=/tmp/polymind-phase17d-pycache python -m compileall -q .
docker compose config --quiet
git diff --check
```

The external cache avoids unrelated ownership changes. No formatter/linter/type
checker is configured as a project gate; none was invented. Docker build was not
needed because dependencies, container and deployment configuration did not change.
No cluster validation or mutation was needed. Final documentation/whitespace/link/
secret checks and baseline verification are recorded in section 43.

## 40. Self-review and pre-commit findings

Reviewed all incremental source/tests and the full plan/worker/evidence path.
Implementation review fixed canonical ordering when parent content follows a
subsection; request-budget repartitioning; inherited qualification/conflict counts;
explicit final qualification/root-claim retention; cached node/fingerprint lookup;
repeated coverage-set construction; and canonical integrity reinspection before
final acceptance. Targeted and full-suite results above include these fixes.

Reviewed fake citation behavior: evidence IDs come from the application accessor
over supplied canonical references, not arbitrary fake text. Reducers must retain
all child claim links; original evidence is resolved from those links rather than
accepting generated summaries as sources. Final model-schema validation and plan
reconstruction prevent copied-model tampering at admission.

The resumed closure review found no further genuine code defect requiring a change.
It completed documentation and the separate pre-commit audit without repeating
implementation work. Reviewed imports, resource handling, compatibility, error
normalization, cancellation/retry boundaries, no silent truncation, annotation
retention, profile invalidation and scope exclusions. No commit is part of this
review. Heuristic checks do not constitute a formal security certification.

## 41. Remaining limitations

Real-model language quality, semantic support and natural-language contradiction
extraction are unproven. Reducers receive bounded generated material and immutable
source-lineage handles; full qualifier/source details remain in linked artifacts.
Phase 17E must calibrate real prompts and any authorized bounded source expansion
without weakening inheritance or request bounds. No source-fetch tool exists now.

Native extraction's structure/visual limits remain. Oversized structured tables
without row-span mappings fail safely. No hard process isolation, production
storage/queue, authentication, quota, billing, publication or deletion policy is
implemented. Metrics remain deferred to worker integration; no serving-metrics
coupling was introduced. SQLite/local storage remain reference adapters, and
large structural fixture results do not certify large production documents.

## 42. Exact Phase 17E prerequisites

The next phase can consume the neutral StageRequest/StageResult boundary, explicit
profiles/budgets, canonical evidence, immutable checkpoints and existing durable
failure/retry semantics. It must adapt to the existing InferenceProvider without
breaking interactive generation/streaming, establish actual context/output
capabilities, calibrate structured prompts, define exact-versus-estimated usage,
normalized provider failures and approved inference admission/accounting.

Validate real semantic fidelity, qualifications, conflicts, source support and
formatting behavior before making quality claims. Production model/provider
configuration and any live validation require the next phase's explicit scope;
Phase 16 connectivity alone is not document-inference integration. Retain existing
publication/authentication gates for 17F/17G and reliability/quality certification
for 17H. **Phase 17E — Managed Inference Integration** is next, not started.

## 43. Final Git state and closure audit

Work remains on master at the starting HEAD with an empty index. Git's tracked
stat includes accumulated Phase 16 and README changes and excludes all new
untracked source/test/document files; section 37 is the incremental 17D inventory.

Prior work accounting: the Phase 16 report contains the pre-existing closure;
Phase 17A contributes its prompt/report and original roadmap; Phase 17B contributes
canonical document modules and extraction/storage tests; Phase 17C contributes
`documents/jobs/`, ledger tests and job integration tests. None is attributed to
17D or changed by it. README alone receives the intentional cumulative update.

Commit created: **NO**. Push performed: **NO**. Branch created: **NO**.
Files staged: **NO**. Prior Phase 17 work preserved: **YES**.
No real model call, Foundry call, Azure mutation, Kubernetes mutation, RAG
publication, external OCR, new paid infrastructure or secret exposure occurred.
No Phase 17E implementation was started. All work remains uncommitted for the
operator's complete Phase 17A–17I review policy.

Final lightweight audit passed: `git diff --check`; individual no-index whitespace
checks for all 11 new untracked files; explicit final-newline/trailing-whitespace
checks; four relative links in the new report and the new README report target;
secret/private-key/credential-URL and source debug/local-path heuristics. No runtime
secret, private document, database, binary fixture, temporary log, dependency or
unrelated file was introduced. The prompt remained unchanged during closure.

Baseline hashes confirm all 202 prior files preserved except README's intentional
**9 added / 6 removed lines**. Closure hashes confirm all previously tested Phase
17D source/test files unchanged. Compile and Compose checks remain valid and were
not repeated during documentation-only closure. Full-suite and targeted test logs
were retained; no unnecessary test rerun occurred. Audit inventory is retained
outside the repository at `/tmp/polymind-phase17d-closure-audit.json`.

Final `git status --short --branch`:

```text
## master...origin/master
 M README.md
 M docs/codex/reports/phase_16_report.md
?? docs/codex/prompts/phase_17a.md
?? docs/codex/prompts/phase_17b.md
?? docs/codex/prompts/phase_17c.md
?? docs/codex/prompts/phase_17d.md
?? docs/codex/reports/phase_17a_report.md
?? docs/codex/reports/phase_17b_report.md
?? docs/codex/reports/phase_17c_report.md
?? docs/codex/reports/phase_17d_report.md
?? documents/
?? tests/integration/
?? tests/unit/documents/
```

Final tracked `git diff --stat`:

```text
 README.md                             |   44 +
 docs/codex/reports/phase_16_report.md | 1631 ++++++++++++++++++++++++++++++++-
 2 files changed, 1674 insertions(+), 1 deletion(-)
```
