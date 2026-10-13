# Phase 17H — Large-Document Reliability, Failure & Quality Validation

Date: 2026-10-12. Branch: master. Authority: [phase prompt](../prompts/phase_17h.md).
Reproduction: [methodology/runbook](../../evaluation/phase_17h.md).
Machine-readable evidence: [compact observations](../../evaluation/phase_17h_observations.json).

## 1. Executive summary

Implemented deterministic physical-PDF generation, resource-bounded subprocess
benchmarks, real local Chroma corpus measurements, governed concurrent workloads,
hard-process-exit recovery tests, synchronized multi-user revocation tests, and a
versioned annotation-driven quality evaluator. The existing application handled
all executed 4/200/500/1000-page low-density PDFs with complete native coverage,
accepted durable digests and coherent publication. The 1001-page document was
refused under the unchanged page limit. No production source, runtime interface,
dependency, deployment or schema was changed.

The results demonstrate a specific bounded offline workload, not arbitrary
1000-page manuals or real-model quality. Full-graph verification has substantial
measured cost: 1000-page readiness was about 3.64 seconds and median retrieval was
about 3.37 seconds. Integrity checks were preserved. Expert semantic evaluation
and live Foundry digestion remain unperformed and separately gated.

## 2. Exact phase verdict

**Overall: PARTIAL — actual-model semantic/expert quality and live Foundry
validation remain PENDING / NOT VALIDATED. FULL PHASE 17H PASS is not claimed.**

**LOCAL RELIABILITY PASS** applies to the executed low-density page matrix, local
single-host correctness/recovery/security/accounting/publication tests and bounded
benchmarks. **QUALITY EVALUATION IMPLEMENTED** applies to the rubric, structural
checks, independent-annotation metric calculations, four deterministic accepted
facts and adversarial evaluator controls. Neither label certifies semantic output
from a real model, distributed deployment, production throughput or public use.

| Mandatory gate | Local result and qualification |
| --- | --- |
| Size/completeness | PASS: real PDF counts and all accepted spans/units checked; 1001 safely refused |
| Durability/failures | PASS: hard exits, stale fences, lost ACK/reuse/persistence/cancellation and provider contracts |
| Concurrency/governance | PASS: 1/2/4 jobs, shared quota, eight-way reservation and duplicate execution races |
| Publication/retrieval | PASS: pinned generations, local Chroma partial writes/recovery, selected indexes and tombstone rollback |
| Offline evaluation | IMPLEMENTED and exercised; synthetic judgments only |
| Representative semantic/expert targets | NOT VALIDATED |
| Live Foundry digestion | PENDING; no authorization or calls |
| Proposed interactive <=20% target | NOT ESTABLISHED; even held-provider synthetic p95 exceeded the candidate delta |
| Automatic recovery within two leases | NOT ESTABLISHED; harness invokes reconcile/relay explicitly |

## 3. Starting Git HEAD and baseline

Verified clean `master...origin/master` at
`45555394c350da7dfc18ed9409569dedefc8e789`, with the requested Phase 17G commit and
five-commit history. Initial `git diff --check` passed. The external baseline at
`/tmp/polymind-phase17h-baseline` records HEAD/branch/status/index/diff, all **264
tracked paths and SHA-256 hashes**, environment, limits and test inventory.
No pre-existing work was reset or discarded. Phase 17G's **690 passed in 94.03 s**
is historical comparison evidence, not a claimed rerun.

## 4. Current system limits

Extraction defaults remain 16,000,000 source bytes; 1000 physical pages; 4,000,000
characters; 100,000 blocks; 32,000,000 artifact bytes. Digestion requires an explicit
profile, capped at 900 chunks and 1000 steps, plus context/result/fan-in/depth/source
bounds. No supported larger-page profile was introduced. Deliberate refusal is
not successful processing. Native text coverage does not imply visual/OCR recall.

The benchmark profile uses 60,000 JSON-character context units, 6000 reserved
output/max-result characters, 3200 source characters/chunk, fan-in four, at most
5000 source units, depth 32 and no partial coverage for the page matrix. Those
are fake-planning budgets, not verified real-model token capacities. Maximum
fan-in observed was four (one for the control's single-child reductions).

## 5. Readiness assessment

The [pre-implementation assessment](../../evaluation/phase_17h_readiness.md) answers
all twelve readiness questions and distinguishes hard invariants, proposed 17A
targets, harness resource caps and unmeasured properties. It was written before
harness implementation; no production correction was needed.

Key findings: pypdf/canonical JSON/plans are materialized; the production parser
has no process CPU/RSS sandbox. Job steps are repeatedly scanned; final digests
and publication admission/readiness/retrieval reconstruct accepted graphs. Job
writes use BEGIN IMMEDIATE, while security/governance/provider operations serialize
on trusted single-host SQLite files. Uncertain usage remains reserved across
restart/periods. Publication activation is logical CAS, not physical vector
transactionality. Security epochs override retained generations. Phase 16's
historical limited Foundry quota, volatile Chroma/storage and disabled HPA do not
certify today's production throughput or durable distributed authorities.

## 6. Benchmark architecture

`tests/performance/` is an opt-in harness, not a production service. It calls the
existing extraction, LocalObjectStore, job worker, fake/managed inference,
publication, security and governance ports. Page cases run sequentially in fresh
children, with 180-second wall/CPU budget, 2 GiB address-space limit, 1 GiB aggregate
disk, 5000 files and 16 MB fixture limit. Parent sampling is every 200 ms; disk/file
caps can overshoot within that interval. Corpus/latency watchdogs enforce sampled
RSS/disk/files/wall. No model factory, model server or container was started.

Host: Python 3.10.13, pypdf 6.12.2,
Linux/WSL2, eight logical CPUs, about 15.54 GiB total RAM and 12.79 GiB available at
baseline. Temporary storage is ext4 (`/dev/sdd`), about 816 GiB initially free.
The host is not dedicated benchmarking hardware. Large page measurements overlapped
some small development tests; they are exploratory observations. Final latency
measurement was repeated without competing test runs. Results retain run counts
and all latency samples; there is no confidence-interval or production-SLO claim.

## 7. Fixture manifest

Version `phase17h-pdf/1`, seed **1708**, six low-density text lines per page,
fixed source timestamp, actual pypdf page objects. Each generated `fixture.json`
contains expected lines and physical page identities, with actual reader count.
Every admitted page's exact native text is compared to those expected lines.

| Pages | Fixture SHA-256 |
| --- | --- |
| 4 | `1be99e19a56040fb55c74682a19f874d4d4573f18d9f52a9a7ae19c8158ea92d` |
| 200 | `e0e6cc4d5e3227898bbade6abcb8466be1372035801a6e1eb2c33801646b180f` |
| 500 | `fc44b02d2fde92cf4494c3048dfc1b696bebaf75d12a4c8ce072b0fb7c62b66a` |
| 1000 | `e32ce6ba164d62277def0f94257f2e325f33b8c7f3047945625828afefaeb082` |
| 1001 | `c477773653977d5fd3ef684a8e588601f04cab37e0d63b32ba8e4f0a37a5c075` |

Native density is about 348–349 characters/page for larger fixtures, far below
4,000,000 total characters. This does not exercise the densest legal/manual PDF
possible under all byte/character limits. Sources and full outputs remain outside
Git. Compact observations/checksums are intentionally versioned for review.

## 8. Page-count and document-type matrix

| Physical pages | PDF bytes | Native characters | Status | Child wall s | CPU s | Peak RSS MiB |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 3537 | 1491 | PASS | 0.654 | 0.560 | 68.98 |
| 200 | 153221 | 69611 | PASS | 10.808 | 10.944 | 91.78 |
| 500 | 383033 | 174311 | PASS | 30.662 | 31.943 | 126.22 |
| 1000 | 768035 | 348812 | PASS | 82.758 | 87.305 | 183.73 |
| 1001 | 768806 | — | EXPECTED_REFUSAL | 0.568 | 0.631 | 65.62 |

Child wall includes generation, extraction, repeated plan checks, durable digestion,
publication, readiness and three query/citation samples. Parent elapsed also includes
interpreter startup: 1.20/11.25/31.08/83.44/1.20 seconds in page order. Run count is
one final executed sample per size. No 1001-page extraction/digestion is claimed.

| Type | Expected and observed behavior |
| --- | --- |
| Native prose/manual, section/subsection-looking labels | Text retained; canonical native blocks remain generic text, not semantic headings |
| Blank + native pages | Blank explicitly inventoried/skipped; accepted native coverage COMPLETE |
| Image-only synthetic scan | image_only/ocr_required; all-image digestion refuses coverage_failed |
| Native + image-only page | Unsupported image page counted; explicit PARTIAL with chosen partial profile |
| Figure/graphics-only | unresolved/manual_review; unsupported counted, no invented description |
| Native text and image on same page | has_images retained; native text accepted; COMPLETE is native coverage only |
| Columns | Text substrings retained; side-by-side lines merged; reading-layout fidelity not certified |
| Native table/caption | Text retained, no table cells or visual semantics invented |
| Malformed/encrypted | invalid_document/encrypted_document refusal |
| Source/artifact over configured bytes | source_too_large/extraction_limit_exceeded |
| Filename >512 chars / misleading suffix | invalid_document / unsupported_format |
| Prompt injection text | Retained as untrusted source; no tool/authority added; real-model resistance unverified |

These image fixtures are known synthetic XObjects, not an OCR accuracy benchmark.
Existing structured-heading/parsed-table contracts are rerun in the full suite;
native extraction does not discover such structure merely because it is printed.

## 9. Extraction completeness results

All admitted physical ordinals were exactly `1..N`. Native unit counts were
4/200/500/1000, with no failed/unsupported/blank units in the ordinary page matrix.
Canonical artifact bytes were 8331/350275/874675/1748679. Serialization round-trip
and SHA-256 matched; re-planning was byte deterministic. All planned source pieces
resolved to exact source text and concatenated to the full native extraction.

No missing unit was reclassified as success. Small mixed/failure cases separately
exercise PARTIAL/FAILED policy. Existing parser-failed-unit tests remain intact.
The document's immutable original source remains citation authority; generated
summaries and vector rows never replace it.

## 10. Hierarchical digestion results

| Pages | Chunks | Reducers | Depth | Steps / attempts | Checkpoints | Included / eligible | Digest bytes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 1 | 2 | 2 | 5 | 3 | 4 / 4 | 5315 |
| 200 | 23 | 10 | 4 | 35 | 33 | 200 / 200 | 131227 |
| 500 | 56 | 20 | 4 | 78 | 76 | 500 / 500 | 319670 |
| 1000 | 112 | 39 | 5 | 153 | 151 | 1000 / 1000 | 635208 |

Coverage was 1.0 for every accepted page case. No failed/unsupported analysis unit
was accepted as COMPLETE. Each fake stage call corresponded to one checkpoint:
3/33/76/151 calls, with five/35/78/153 accepted workflow steps including plan/final
steps. These counts are not fabricated transition-event counts: the ledger does
not expose a general transition-history metric, so attempts and accepted steps
are reported explicitly.

Distant page-5 and page-180 findings retained two qualifications and one unresolved
opposition in each >=200-page digest. Provisional/revised capacity findings on
pages 100/199 remained linked. Evidence for beginning/middle/final physical units
survived the full graph. These are operator-defined fake findings, not a model
recognizing or resolving natural-language conflicts. No whole-document prompt
bypassed the reduction hierarchy.

## 11. Resource and latency measurements

| Pages | Extraction s | Plan s | Digestion s | Publication plan s | Prepare s | Load s | Readiness s | Retrieval median s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 0.019 | 0.009 | 0.155 | 0.029 | 0.026 | 0.019 | 0.017 | 0.018 |
| 200 | 0.340 | 0.223 | 1.607 | 0.655 | 0.625 | 0.548 | 0.585 | 0.541 |
| 500 | 0.940 | 0.689 | 4.069 | 1.539 | 1.730 | 2.012 | 1.813 | 1.472 |
| 1000 | 1.905 | 1.358 | 12.235 | 10.106 | 6.323 | 4.192 | 3.642 | 3.367 |

| Pages | Object bytes / files | SQLite bytes | Manifest bytes | Fake vectors | Object reads / bytes |
| --- | --- | --- | --- | --- | --- |
| 4 | 40189 / 10 | 131072 | 9751 | 8 | 153 / 771389 |
| 200 | 1361076 / 40 | 233472 | 401471 | 400 | 633 / 26794918 |
| 500 | 3373030 / 83 | 401408 | 1001471 | 1000 | 1321 / 66474729 |
| 1000 | 6735894 / 158 | 692224 | 2001473 | 2000 | 2521 / 132740934 |

Object read counts include admission, finalization and repeated publication/query
validation; they are cumulative operations, not unique objects. The 1000-page run
read roughly 132.7 MB through 2521 ObjectStore calls for about 6.7 MB of retained
objects. CPU/RSS and detailed timing/denominators are preserved in observations.
Python allocation tracing was omitted to avoid changing the timing workload.
Average CPU consumption can be derived from recorded process CPU / wall; no sampled
CPU utilization or process-isolation claim is made.

For interactive analysis on a small authorized corpus with held fake upstream
background stages, the final watchdog run retained all 100 samples per condition:

| Held background jobs | Requests | Median s | Observed p95 s | Max s | Failures | p95 delta |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 100 | 0.0935 | 0.1112 | 0.1469 | 0 | 0.0% |
| 1 | 100 | 0.1102 | 0.1382 | 0.2032 | 0 | 24.3% |
| 4 | 100 | 0.1116 | 0.1356 | 0.2164 | 0 | 21.9% |

All background jobs subsequently completed. No request/timeouts were discarded;
publication was loaded before samples with no omitted query warmup. Observed p95
uses nearest rank. The +24.3%/+21.9% p95 changes exceed the proposed 20% candidate
threshold in this synthetic experiment. That does **not** establish or disprove a
production SLO: providers were paused, not running representative inference/CPU
work, only one run per condition was made, and order/hardware variability remain.
Representative latency target: **NOT ESTABLISHED**. Initial contended measurements
(+38%/+52% approximately) are retained outside Git, not silently replaced as passes.

## 12. Concurrency results

| Jobs | Peak provider calls | Total wall s | Completed | Calls / job | Attempts / job |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0.877 | 1 | 3 | 5 |
| 2 | 2 | 1.146 | 2 | 3 | 5 |
| 4 | 4 | 2.410 | 4 | 3 | 5 |

Every job processes a four-page PDF with the managed StageRequest/provider boundary,
real durable manifests, own principal and shared SQLite authorities. Four jobs span
four owners and two tenants. Provider capacity is five, with one slot reserved for
interactive work; background peak is four. Each owner has exactly three measured
fake usage rows, isolated from other owners/tenants. All progressed in this sample;
no general fairness, queue admission cap or AKS scaling claim follows.

## 13. Worker failure and recovery

Fresh interpreters terminate with `os._exit(77)` after claim, artifact persistence
or manifest commit. Reopened authority/worker instances recover uncommitted work;
committed outputs stay accepted with one attempt after lost acknowledgement.
The write-before-commit case reused exactly the original immutable object bytes,
then refused the old lease as stale. Cancellation before recovery prevented a
manifest from becoming accepted. No source/citation identity was fabricated.

Measured wall time including subprocess start/exit/recovery was 0.407 s (claim),
0.477 s (write), 0.395 s (commit), 0.490 s (cancel) in the focused run. Controlled
clock advanced 11 seconds with a ten-second lease. Reconciliation and relay were
explicitly called. This is executable durable recovery, **not** an automatic
scheduler recovering within two real lease intervals. Existing tests cover source
read restart in a fresh interpreter, corrupt checkpoint refusal, storage failure,
resume without reanalysis and publication recovery without repeating synthesis.

## 14. Provider 429, timeout and protocol behavior

The focused 107-test contract run reused managed inference, managed digestion,
governed digestion and job/publication suites. Fake 429 preserves Retry-After (23
seconds in its case), timeout uses the bounded durable retry policy, and excessive
retry-after exhausts the configured budget. Missing/malformed/oversized responses,
provider unavailable, model/capability mismatch and forged evidence remain denied.
Failed execution with missing usage retains unknown observations, not zero tokens.
Repeated retries have distinct attempt records; no hidden model fallback or retry
storm was introduced. Full provider/transport contracts run again in regression.

## 15. Quota and cost-accounting evidence

Eight concurrent separate authority connections contend for synthetic balance 20
with reservation cost eight. Exactly two reserve (16 total); six are denied. Both
single-owner and multi-owner/shared-tenant variants pass. An eight-way race on one
logical execution identity performs one provider call and one settlement; duplicate
attempts are denied. Concurrent jobs share provider admission and owner/tenant
reservation authority rather than Python-only counters.

Existing tests cover RPM/TPM/slot exhaustion, interactive headroom, idempotent
reservation, cancellation after paid work, missing/partial usage, interrupted
execution, month rollover and trusted reconciliation. Governance denial makes no
provider call. Fake 30-input/40-output usage costs 70 under an explicitly synthetic
one-unit/token catalog. That is test arithmetic, not commercial pricing/billing.
Uncertain provider execution can retain a slot indefinitely until trusted evidence
resolves it; this is fail-closed behavior, not automatic operational recovery.

## 16. Publication failure, activation and rollback

Full corpus candidates use isolated generation rows. At medium/larger local Chroma
sizes the harness interrupts after one upsert, verifies the previous generation
still validates/serves, reopens publication authority, retries deterministic
upserts and activates only after complete validation. Historical rows remain.
Rollback after tombstone plus security-authority reopen denies owner/shared/foreign
access and remains PURGE_PENDING. No collection was reset or claimed transactional.

Existing lifecycle tests additionally exercise before/after writes/validation/
activation, concurrent CAS candidates, ABA/stale replicas, corrupt inventory and
recovery of publication without repeating completed synthesis. Dense, sparse and
canonical citations stay pinned to one admitted generation.

## 17. Retrieval scaling and quality

Final local persistent Chroma corpus run (constant fake embeddings):

| Docs / pages | Active records / retained rows | Prepare s | Load s | Readiness s | Selected retrieval median s | Peak RSS MiB |
| --- | --- | --- | --- | --- | --- | --- |
| 1 / 4 | 8 / 8 | 0.157 | 0.021 | 0.020 | 0.0216 | 117.16 |
| 8 / 32 | 64 / 72 | 1.474 | 0.151 | 0.154 | 0.0330 | 123.41 |
| 32 / 128 | 256 / 328 | 7.924 | 1.182 | 0.937 | 0.0393 | 143.96 |

Each size measured five selected-document queries with no discarded samples; p95
is intentionally null. Corpus size is bounded at 32 documents/128 pages/256 active
rows, while the single-document PDF benchmark reaches 2000 fake-vector rows. This
is not an enterprise-scale corpus certification. Full-generation readiness/load
cost rises with corpus size; selected retrieval remained about 20–30 ms because
unselected documents were not opened for provenance validation.

The harness separately times actual Chroma dense calls, per-document sparse scores,
RRF, identity reranking and citation reconstruction; exact values are in the JSON.
It also validates two-document selection and rejects use of the whole-corpus BM25
index in authorized queries. Every candidate/citation belongs to the selected
canonical document/generation. Many unshared documents cannot affect sparse corpus
statistics; cross-tenant authorization fails before retrieval.

Page-1 exact canonical source IDs define two relevant records for query `Unit 0001`.
For each of three corpus sizes, dense, sparse and fused top-eight results have
Recall@8 **2/2**, Precision@8 **2/8**, reciprocal rank **1.0** in the executed fake
embedding fixture. This is a narrow controlled lookup label, not broad retrieval
quality. Identity reranking has no learned quality effect. Distant-page source
retention is proven by digestion; representative dense-model recall and learned
reranker impact remain unvalidated.

## 18. Multi-user isolation and revocation

New synchronized tests run owner/shared/cross-tenant requests concurrently, pause
the two authorized provider calls, mutate grants/tombstones from a fresh authority
instance on the same DB, then finish inference. Both old snapshots are denied
conservatively after epoch change; cross-tenant work never reaches the provider.
Measured cost remains attributed separately to the two requesting principals.
An unaffected private document remains available to its owner.

Existing middleware tests guard actual final response release and simulated
streaming sends after revocation acknowledgement. Previously sent bytes cannot
be recalled. OIDC legacy query/stream remains disabled. Session isolation and
missing/corrupt authority fail-closed behavior remain covered by regression.
Shared SQLite is trusted single-host state; copies are not distributed authority.

## 19. Citation provenance versus semantic quality

Canonical version/extraction/source/block/span/page/excerpt checks are independently
exercised with wrong page, out-of-range span, foreign version and denied authority.
A deliberate evaluator control has **one valid citation out of one**, but **zero
supported claims out of one** and **one critical unsupported conclusion**. This
explicitly prevents the mistaken conclusion that valid citations prove entailment.
Production outputs continue to label semantic support `not_evaluated`.

## 20. Evaluation rubric and metrics

Dataset `phase17h-ground-truth/1` and rubric `phase17h-rubric/1` contain 12 authored
questions for direct/section/distant synthesis, conflicts, qualifications, revised
values, year limits, missing data, false premises, quoted malicious instructions,
inaccessible table values, similar reports and unauthorized evidence. Expected
answer class, sufficiency, findings, criticality and physical pages are explicit.
Canonical IDs/spans are materialized against accepted benchmark artifacts.

Citation validity = authorized structurally valid citations / evaluated citations.
Claim support = independently judged supported factual claims / evaluated factual
claims. Coverage = distinct correctly represented required findings / required
findings. Critical unsupported conclusions are a count. Abstention correctness =
correct insufficient-evidence decisions without factual assertions / insufficient
cases. Preservation = cases retaining required opposition/qualification / relevant
cases. Denominators of zero produce null, never a fabricated percentage. Ranking
metrics are separate. Model confidence is not an input to any metric.

## 21. Actual supported-claim and coverage observations

Four expected synthetic factual leaf findings in the accepted 200-page digest
were checked against exact independently recorded source strings and canonical
references: citation validity **4/4**, deterministic support **4/4**, required
finding coverage **4/4**, qualification/opposition preservation **2/2**, critical
unsupported conclusions **0**. No insufficient-evidence answer was produced by
this digest check, so abstention is **0 evaluated / null rate**, not 100%.

These fake findings establish pipeline retention and evaluator mechanics only.
The 12-case rubric arithmetic unit test uses authored judgments, including four
insufficient-evidence cases; it is not twelve actual model answers. No expert-
sampled real-model observations exist. Proposed 95%/90% semantic targets remain
**NOT VALIDATED**. Reviewer provenance, representative sampling and actual model
outputs are prerequisites for certification.

## 22. Prompt injection and insufficient evidence

Source page 3 includes requests to override instructions, reveal unrelated text,
invent citations, exfiltrate secrets, change selection, bypass authorization and
suppress contradictions. Exact bytes remain source data; existing StageRequest
and managed prompt contracts expose no tools or authority, and forged references
fail application validation. The fake does not execute commands. No real network
exfiltration was attempted. Actual-model prompt-injection resilience remains open.
Missing/false-premise/unauthorized cases are explicit in the rubric. Abstention
arithmetic rejects claiming to abstain while asserting unsupported factual claims.

## 23. Live Foundry status and bounded specification

**PENDING / NOT EXECUTED.** No credentials, endpoint discovery, deployment checks,
provider calls or capacity modifications were performed. The runbook includes a
separate proposed operator approval contract: exact project/deployment/capability,
operator prices and monetary budget, small then one 200-page synthetic document,
<=50 attempts including retries, <=1.25M reserved input and <=150k output tokens,
one concurrent call, <=2 RPM / <=30k TPM or lower available quota. Actual rendered
requests must fit the verified model and approved plan. Unknown usage, repeated
429/timeouts, capability/provenance/security failure or budget boundaries stop the
run. Representative review/privacy/retention/audit and bounded cleanup are required.
These proposals authorize no call and assume no existing model availability.

## 24. Defects discovered and corrections

No demonstrated critical production-contract defect required a code change.
The first benchmark monitor raced a transient SQLite journal disappearing between
listing and stat; its child was terminated and the 500-page case retained as
HARNESS_INTERRUPTED. The monitor now tolerates only FileNotFoundError for transient
files, persists JSON atomically and has a focused regression test. Run 1's 4/200
successes and interrupted 500 are retained; run 2 executed the complete matrix.

A new column-fixture assertion incorrectly required per-drawn-line extraction.
Observed text was merged by pypdf; the test now checks retained content and records
unsupported layout, rather than claiming cell/reading-order fidelity. A JUnit
record_property warning in the first concurrency run was removed by rerunning
with xunit1 reporting; warnings/results remain in the historical log. Later corpus
label review tightened page identity selection to the canonical physical-page
unit, followed by a fresh bounded corpus run. No validation/security check was
removed to improve performance.

## 25. Targeted test outcomes

| Checkpoint command/group | Exact outcome |
| --- | --- |
| Evaluator unit tests | 10 passed in 0.17 s |
| Initial type/recovery tests | 23 passed, 1 failed in 7.05 s (column layout assumption) |
| Corrected type/recovery + evaluator | 34 passed in 4.17 s |
| Initial managed concurrency, xunit2 | 3 passed, 3 reporting warnings in 2.88 s |
| Concurrent jobs + budget race | 5 passed in 3.44 s |
| Existing job/provider/governance/publication focused contracts | 107 passed in 31.79 s |
| Final concurrency/revocation/evaluator group, xunit1 | 18 passed in 7.83 s |

These overlapping counts are **not added together**. Commands/logs/JUnit are in
the outside-repository baseline. Separate benchmark outcomes are recorded above;
they are not pytest cases and are not included in regression count.

## 26. Final complete regression outcome

`python -m pytest -q` was run once after final implementation and exited 0:

```text
732 passed in 111.95s (0:01:51)
```

**Passed: 732. Failed: 0. Skipped: 0. Warnings: 0 reported.** This is 42 more
cases than the historical 690-test baseline. No existing tests were weakened or
removed. Large benchmark cases are separate and are not included in 732.
Only documentation/audit updates followed this regression; no runtime or test
source changed. The complete log is retained in the external baseline.

## 27. Compile, Compose, lint and configuration

External-cache compileall and `docker compose config --quiet` exited zero.
`git diff --check` passed. No configured formatter/linter/type-checker gate exists
in Makefile/CI/project configuration. Helm/deployment contracts were unchanged, so
Helm was not rerun. No Docker image build or Kubernetes contact was performed.
The full compile used `/tmp/polymind-phase17h-pycache`; no ownership changes occurred.

## 28. Complete changed-file inventory

**2 modified tracked files + 19 new untracked files = 21 files.**

```text
Modified tracked:
README.md
docs/security/phase_17g.md

New untracked:
docs/codex/prompts/phase_17h.md
docs/codex/reports/phase_17h_report.md
docs/evaluation/phase_17h.md
docs/evaluation/phase_17h_observations.json
docs/evaluation/phase_17h_readiness.md
tests/fixtures/phase17h/profile.json
tests/fixtures/phase17h/quality.json
tests/integration/test_phase17h_concurrency.py
tests/integration/test_phase17h_reliability.py
tests/performance/__init__.py
tests/performance/bounded.py
tests/performance/corpus.py
tests/performance/fixtures.py
tests/performance/latency.py
tests/performance/phase17h.py
tests/performance/quality.py
tests/performance/workloads.py
tests/unit/documents/test_phase17h_evaluation.py
tests/unit/publication/test_phase17h_load.py
```

Only documentation and test/evaluation harness files change. No production runtime,
API, provider schema, dependency, Docker/Helm or existing historical report changes.
README and the current 17G operator contract now reflect the authoritative committed
local/reference PASS and keep live/distributed limits. Badge structure is preserved.

## 29. Implementation and pre-commit review

Reviewed the full tracked documentation diff and all new harness/tests, fixture
profiles, rubric and report. Source review checked bounded loops/timeouts, child
termination in finally blocks, authority sharing, deterministic fixture identity,
artifact lineage, source coverage, error paths, quota attribution, temporary
instrumentation restoration and the separation of synthetic judgments from model
quality. No test-only behavior enters application runtime. No provider-specific
condition, security bypass, provenance cache or contract weakening was introduced.

A separate bounded pre-commit scan examined all 21 changed/new UTF-8 files for
private keys, JWT-shaped credentials, credential URLs, long secret literals,
machine-specific home paths, runtime PDFs/DBs/models/logs, excess file sizes and
whitespace. It found no such issue. Local Markdown links resolved. Historical
README Markdown line breaks were retained. Baseline hash comparison confirms
**all 262 other tracked files**, including every production module and historical
report, are unchanged. The compact observation JSON is an intentional 38.7 KB
text artifact, not a generated PDF/database. No unrelated dependency or temporary
file entered the checkout. This heuristic scan is not security certification.

The early monitor/stat race and column-layout assumption were resolved and
retested; no critical production finding remains within the executed scope.
Resource watchdogs reap their children; process inspection found no surviving
benchmark/provider process. Generated fixtures and local databases are deliberately
retained only in the named temporary audit directories, not deleted or published.

## 30. Remaining limitations

Physical page success covers a low-density born-digital profile, not every 1000-page
input or dense tables/images. No OCR/layout reconstruction, real embedding/reranker
quality, representative model entailment or expert certification is established.
No 1001-page support, production parser process sandbox, automatic scheduler,
load fairness/SLO, distributed SQLite authority, backup/restore/deletion certification,
physical purge or public multi-user deployment is claimed.

Repeated full graph/source/inventory validation measurably affects readiness and
interactive latency. Per-record vector upserts and per-document BM25 scans are
conservative and potentially expensive. No unsafe caching was added. Safe scalable
verification or batching needs a separately scoped design with immutable identity,
revocation and coherence preserved. Current local measurements do not certify
AKS or paid inference throughput; uncertain call reconciliation remains operational.

## 31. Phase 17I prerequisites

Phase 17I remains **External User Verification — NOT STARTED**. Before exposure:
operator acceptance of this bounded reliability evidence, appropriate actual-model
and independent expert quality evidence, explicit current-limit communication,
authenticated isolation, bounded owner/tenant/provider cost configuration, consent
for representative documents, privacy/retention expectations, approved external
exposure and controlled audit/cleanup procedure. PARTIAL 17H does not authorize
unrestricted external-user onboarding or any paid validation.

## 32. Final Git status and prohibited-action confirmation

`git status --short --branch` — exit 0:

```text
## master...origin/master
 M README.md
 M docs/security/phase_17g.md
?? docs/codex/prompts/phase_17h.md
?? docs/codex/reports/phase_17h_report.md
?? docs/evaluation/
?? tests/fixtures/
?? tests/integration/test_phase17h_concurrency.py
?? tests/integration/test_phase17h_reliability.py
?? tests/performance/
?? tests/unit/documents/test_phase17h_evaluation.py
?? tests/unit/publication/test_phase17h_load.py
```

`git diff --stat` — exit 0:

```text
 README.md                  | 15 +++++++++------
 docs/security/phase_17g.md |  9 +++++----
 2 files changed, 14 insertions(+), 10 deletions(-)
```

`git diff --check` — exit 0:

```text
(no output)
```

`git diff --cached --name-only` — exit 0:

```text
(no output)
```

`git log -1 --oneline` — exit 0:

```text
4555539 feat: implement Phase 17G multi-user security and cost governance
```

The tracked stat excludes the 19 new files listed separately in section 28.
The index is empty and HEAD remains the verified starting commit.

Commit created: **NO**. Push performed: **NO**. Branch created: **NO**.
Azure mutation: **NO**. Kubernetes mutation: **NO**. Foundry capacity change: **NO**.
Live Foundry inference: **NO**. Cloud Chroma reset/restart: **NO**.
Cloud Redis reset/restart: **NO**. Paid provider call: **NO**.
New GPU deployment: **NO**. Production database provisioning: **NO**.
External-user verification: **NO**. Phase 17I implementation: **NO**.
All Phase 17H changes are left **uncommitted and unstaged** for operator review.
