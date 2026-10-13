# Phase 17H — 200–1000+ Page Reliability, Failure & Quality Validation

Clean implementation contract normalized from the operator's Phase 17H prompt.
Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`, branch `master`.
Expected clean starting HEAD: `45555394c350da7dfc18ed9409569dedefc8e789`
(`feat: implement Phase 17G multi-user security and cost governance`).

## Mission and authorization

Establish reproducible measurable evidence for large documents, resource growth,
durable execution, faults/recovery, provider quotas/costs, multi-user isolation,
publication consistency, retrieval/citation quality, factual support, coverage,
contradictions and deployment limits. Use existing architecture and make only
small corrections to demonstrated critical defects. Local code, synthetic
fixtures, offline benchmarks, tests and documentation are authorized. Cloud
inference and cloud mutations are not authorized.

## H1 — Baseline and readiness

Before edits run status, HEAD, five-commit log and diff whitespace checks. Stop on
unexpected HEAD or dirty worktree. Record HEAD/branch, index/worktree, inventory,
hashes, tests/benchmarks, limits and initial diff outside Git at
`/tmp/polymind-phase17h-baseline`. Never restore the baseline destructively.
Read AGENTS, current README, Phase 17A prompt/report, 17B–17F reports, 17G
report/design/operator contract and relevant Phase 16 limitations. The historical
17G baseline is 690 passing tests in 94.03 seconds, not the final expected count.
Reconcile stale README PARTIAL statements with the committed 17G local PASS report
without rewriting historical evidence.

Inspect canonical extraction/models/parser/serialization/ObjectStore; jobs,
leases/fences/retries/cancellation/outbox/checkpoints; digestion planning/reduction/
coverage/evidence/managed inference; publication, Chroma/BM25/RRF/reranking/citations;
security, governance, admission and structured inference; API/settings/metrics,
Docker/Helm and tests. Search consumers before shared-interface changes.

Record supported sizes, limiting contracts, disproportionate CPU/memory growth,
repeated artifact-graph validation, SQLite concurrency, failed-attempt accounting,
worker/publication recovery, existing executable evidence, revocation/release
semantics, offline versus semantic evaluation, feasibility of 17A targets, and
local resource/time bounds before production changes.

## Invariants

Original immutable source artifacts and canonical EvidenceRefs are citation
authority. The 17C ledger owns durable job/step state. Dense/sparse/provenance must
share a pinned generation. Security overrides historical publication/rollback.
Owner/tenant budgets and provider admission both precede paid inference. Valid
coordinates do not establish semantic support. Missing/corrupt/uncertain state
must fail closed. Never weaken limits or integrity checks to pass benchmarks.

## H2 — Large-document extraction and digestion

Create deterministic, seed/version/checksum-manifested real PDF fixtures: small
control, 200, 500, 1000, and 1001 physical pages. Verify page counts with the actual
reader. Character count or metadata is not physical-page evidence. Record bytes,
text density, facts and source locations. Keep generated PDFs outside Git.

Verify source/page/span numbering, all native/blank/unsupported/failed units,
no silent truncation, deterministic serialization/checksums and artifact bounds.
COMPLETE must not conceal failed units. Test native paragraphs, headings/manuals,
tables/captions, blank/native mixtures, columns, figures/images, scanned-only,
mixed scanned/native, malformed/encrypted, oversized files, long/misleading names
and injected instructions. No OCR, invented table cells or image recall claims.

Verify actual defaults: 16,000,000 source bytes; 1000 pages; 4,000,000 characters;
100,000 blocks; 32,000,000 artifact bytes. Digestion max_chunks <=900 and
max_steps <=1000 plus explicit context/output/source/depth/fan-in limits. Do not
raise limits silently. Distinguish success, incomplete, deliberate refusal,
unsupported and failure. A rejected 1001-page PDF is not processed successfully.

Measure structural maps, chunks, DAG levels/fan-in/stages/budgets, checkpoints,
coverage and artifact sizes. Every eligible block must be accounted for. Use fake
inference and existing stage schemas, with beginning/middle/end and distant
qualifying/opposing facts. Do not concatenate a document into one model prompt.

## H3 — Concurrency, faults and recovery

Run 1, 2 and at least 4 jobs within explicit local quotas. Include multiple owners
and two tenants. Distinguish job concurrency from inference-attempt concurrency;
measure progress without claiming fairness from a small sample. Use shared fake
provider capacity. Test owner/tenant budget races, RPM/TPM/slot exhaustion,
idempotent attempts, genuine retries, cancellation after paid work, uncertain
usage/restart/reconciliation and period rollover. No invented commercial prices.

Inject deterministic failures through existing ports at claim/extraction/artifact/
checkpoint/ledger/ACK/admission/provider/accounting/publication/activation/revocation
boundaries. Use real process termination where durable guarantees depend on it.
Verify accepted checkpoint reuse, no partial accepted artifacts, no duplicate
accepted logical work, stale-fence rejection, cancellation fencing, bounded retries,
unknown usage retention and publication recovery without rerunning synthesis.
Record recovery timing/leases; do not invent an automatic scheduler.

Test fake overload/429, timeout, unavailable provider, malformed/oversized output,
known/missing/partial usage and model mismatch. Timeout is not zero usage. Budget
denial must prevent calls; no hidden fallback or retry storm.

## H4 — Publication, retrieval and security under load

Exercise coherent full-corpus candidates, isolated/incomplete writes, idempotent
upserts, inventory/provenance validation, activation, supersession, revocation,
rollback, restart and stale replicas. Preserve old active generation on failure;
never mix generations or claim physically transactional Chroma. Use temporary
local collections only; do not reset collections.

Measure dense/sparse/fusion/reranking/citation/load/readiness costs and memory for
small/medium/large inventories, multiple selections and many unauthorized documents.
Authorization precedes retrieval; unauthorized text must not affect selected BM25
statistics. Reranking preserves source identity. Analyze revalidation bottlenecks
without removing security/integrity checks.

Use owner A, shared user B in tenant A and user C in tenant B. Concurrent access,
revocation during paused inference, tombstones during queries and rollback must
release no newly unauthorized answers/citations. Separate authority objects must
share the same trusted SQLite file. Never claim distributed guarantees from copies.
Test actual response-release guards; earlier sent bytes cannot be recalled.
OIDC legacy query/stream stays disabled. Tombstones survive restart and old rows;
physical purge stays PURGE_PENDING. No destructive deletion implementation.

## H5 — Evidence and answer-quality evaluation

Version synthetic ground truth and rubric with document/version, page/span, fact,
qualification, opposing evidence, expected answer class, sufficiency/abstention,
permitted citations and criticality. Cover direct/section/cross-section synthesis,
conflicts, exceptions, absent answers, false premises, quoted malicious commands,
similar documents and unauthorized/revoked evidence. Label synthetic authorship
honestly; no fabricated expert review.

Separate structural validity from semantic support. Report exact denominators for
citation validity, supported factual claims, required findings, critical unsupported
conclusions, correct insufficient-evidence abstention, contradiction/qualification
preservation. Zero denominators produce no percentage. Keep Recall@k/Precision@k/
MRR separate, using exact evidence IDs, explicit k/corpus/labels; compare dense,
sparse and reranking without treating similarity as entailment.

Include page-5/page-180 qualifications, later policy revision, opposing numbers,
year-limited conclusions, inaccessible table data, similar named entities, missing
answers and unauthorized best-looking answers. Untrusted document instructions
must not become authority/tools; no real exfiltration attempt. A model's confidence
is not independent truth.

17A candidate targets remain 100% structural citation validity, >=95%
expert-supported claims, >=90% major findings and zero critical unsupported
conclusions. Fake outputs can validate contracts/evaluator behavior, not certify
real-model quality. Category A is offline deterministic validation; Category B is
separately justified actual-model/expert evaluation. No live model is authorized.

## H6 — Measurements and essential corrections

Measure wall/CPU/RSS, useful allocation information, temporary/ObjectStore bytes
and file counts, SQLite sizes, steps/checkpoints/manifests, embeddings/vector rows,
BM25/publication validation and interactive latency. Record hardware, Python,
storage and profiles. Investigate repeated graph reads, scans/serialized writers,
per-record upserts, inventories, sparse loading, dense filters, reconstruction and
readiness. Do not create unsafe validation caches.

Use explicit permitted pages, fixture bytes, time, memory/disk/files, concurrency,
worker timeout and provider limits. Inspect machine resources. Run sizes
incrementally/sequentially; stop safely on bounds and preserve precise failure
state. Expensive benchmarks must remain separate from default pytest.

Measure interactive requests without, with one, and with multiple background jobs;
record sample count/warmup/median/p95/max/failures/context. Do not claim a reliable
p95 from insufficient samples. Proposed <=20% degradation is not an SLO, and
recovery within two leases requires a supported measurable scheduling contract.
Declare hard invariants, candidate targets, resource budgets and observations
before benchmarking. Synthetic timing is not AKS throughput or a real-model SLA.

For any production fix, reproduce with a focused test, identify the smallest
correction, inspect consumers, preserve contracts, run affected tests and record
before/after evidence. No speculative redesign.

## H7 — Validation, documentation and handoff

Run relevant focused tests at each checkpoint and reuse existing contracts. Run
one final `python -m pytest -q` after implementation; preserve exact counts/duration
and failures/skips, without summing overlapping runs. Run external-cache
compileall, Compose config and diff whitespace checks; run configured lint/type
gates. Helm offline only if relevant. No Kubernetes contact or Docker rebuild.

Create this prompt, `docs/codex/reports/phase_17h_report.md`, methodology/runbook,
compact versioned fixtures/rubric and truthful README updates. Keep large fixtures,
logs, runtime DBs and outputs outside Git. Report limits, measurements, failures,
quality distinction, OCR/security/governance limitations, pending Foundry and 17I
prerequisites. Prepare a bounded live Foundry specification with operator-supplied
configuration/capability/prices/budget, max calls/tokens/concurrency/RPM/TPM,
representative documents/rubric, stop/privacy/cleanup/audit criteria. Do not execute
it or inspect secrets/credentials.

The report must cover executive summary/verdict/baseline, limits/readiness,
benchmark design/manifests/matrices/extraction/digestion/resources/concurrency,
worker/provider/accounting/publication/retrieval/security evidence, provenance and
semantic distinction/rubric/observations/injection/abstention, live specification,
defects/corrections, targeted/full/static validation, changed inventory,
self-review/pre-commit, limitations, 17I prerequisites and final Git confirmation.
Review all new/changed code and error/resource paths, bounds, immutable identities,
provenance, authorization, accounting, cleanup, binaries/DBs/secrets/local paths,
logging/dependencies/docs. Run bounded heuristic secret/artifact checks; these are
not security certification.

Use exact verdicts: LOCAL RELIABILITY PASS only with mandatory local evidence;
QUALITY EVALUATION IMPLEMENTED describes evaluator capability, not model quality;
FULL PHASE 17H PASS needs representative semantic/live evidence; otherwise PARTIAL /
BLOCKED with precise remaining gates. Finish achievable local work. Do not promote
synthetic success to full PASS.

At handoff run status, diff stat/check, cached names and latest log. List untracked
files separately. Leave all edits unstaged/uncommitted on master. Confirm NO commit,
push, branch creation, Azure/Kubernetes mutation, Foundry capacity/inference,
cloud Chroma/Redis reset/restart, paid call, GPU deployment, production DB,
external-user verification or Phase 17I implementation.

## Non-goals and subsequent gates

No OCR, public upload, replacement RAG/vector framework, scheduler/queues,
PostgreSQL/distributed authorities, autoscaling/AKS/Entra/Foundry changes, public
sharing, deletion certification, login/registration, commercial billing, HA/DR,
self-certified LLM evaluator, external users, Phase 17I or Phase 18 work. No new
substantial dependencies or paid resources. No commit/push/branches/reset/stash/
clean/merge/rebase/history/remote-setting changes or unrelated deletions.

Phase 17I remains External User Verification. It requires accepted reliability,
appropriate actual-model quality, documented limitations, authentication/isolation,
quota/cost bounds, consent/privacy/retention for representative documents, explicit
exposure approval and controlled cleanup. PARTIAL 17H does not authorize external
onboarding. The operator reviews and decides on live validation, closure and Git.
