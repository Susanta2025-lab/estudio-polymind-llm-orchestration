# Phase 17H evaluation methodology and operator runbook

## Current project decision — 12 November 2026

`PHASE_17_ENGINEERING_COMPLETE` within the implemented reference scope.
Human acceptance: `DEFERRED_PENDING_TWO_INDEPENDENT_REVIEWERS` (0/2 completed).
Administrative acceptance: `PHASE_17_FORMAL_CLOSURE_PENDING`.
Progression: `NEXT_PHASE_DEVELOPMENT_PERMITTED`, subject to each workstream's own
prerequisites. Technical completion and controlled v11 live validation are PASS;
bounded source-grounded semantic assessment is PASS as preliminary assistant
evidence. This does not establish general production semantic reliability.

See the [completion decision and handoff](phase_17_engineering_completion_and_deferred_acceptance.md),
[deferred-review register](phase_17_deferred_human_semantic_review.md) and unchanged
[frozen human protocol](phase_17h_v11_live_semantic_validation_protocol.md).
The successful v11 run needs no repetition for human review. Two qualified human
reviews and any necessary adjudication remain required for formal acceptance;
no human scores or reviewer approvals have been populated.

## Historical methodology status — 1 November 2026

At the 1 November 2026 checkpoint, this methodology remains the offline reliability and
quality rubric. [Attempt 6](../codex/reports/phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md)
adds one accepted, financially settled live analysis under then-active managed-prompt/4;
it does not close full Phase 17H, which remains PARTIAL. Full live hierarchical
digestion, subsequent grounded Q&A, representative independent semantic/citation
review and workload reliability remain open. The commands below remain offline.

The 7 November four-call live evaluation failed G2 qualification provenance after
one call. Current [managed-prompt/5 R0/R1 hardening](../codex/reports/phase_17h_r0_r1_evidence_provenance_hardening.md)
is offline only; it does not establish model compliance or complete live validation.

This harness runs only synthetic offline work. It never constructs a configured
inference provider, downloads models or accesses configured cloud stores. Run from
the repository root with its existing Python environment; no dependencies need
installation. See [readiness](phase_17h_readiness.md) and the
[phase report](../codex/reports/phase_17h_report.md) for evidence and limitations.

## Reproduction

Choose **new** outside-repository output directories. Existing outputs are never
overwritten. The page driver stops on the first unexpected failure and retains
fixtures, progress, child logs and accepted objects for diagnosis.

```bash
python -m tests.performance.phase17h --output /tmp/polymind-17h-pages
python -m tests.performance.bounded --module corpus --output /tmp/polymind-17h-corpus
python -m tests.performance.bounded --module latency --output /tmp/polymind-17h-latency
python -m tests.performance.bounded --module workloads --output /tmp/polymind-17h-jobs
python -m tests.performance.quality --benchmark /tmp/polymind-17h-pages/200 --output /tmp/polymind-17h-quality.json
```

The explicit profile is `tests/fixtures/phase17h/profile.json`; pass a bounded
alternative with `--config` to the page driver/watchdog. Run suites sequentially
on an otherwise idle host for comparisons. Report other activity, storage,
versions and cold/warm conditions. The corpus and latency modules are implementation
entry points; use the watchdog commands above to enforce aggregate resource caps.
Do not run large cases automatically in CI. Default pytest generates only small
PDFs plus existing logical-block tests.

Page child processes impose address-space/CPU/file limits and the parent monitors
wall time, aggregate disk and file count at 200 ms intervals. The watchdog for
other suites monitors resident memory, wall, disk and files at the same interval.
These sampled caps can overshoot by one polling interval; they are not hostile
input containment. Peak RSS is process-wide, not incremental allocation attribution.
The page benchmark records child CPU and wall; watchdog results include elapsed
and sampled resource peaks. Filesystem/SQLite fsync time is included. Sparse/fusion
instrumentation is temporary harness instrumentation, restored before exit.

Default bounds: sequential 4/200/500/1000/1001 pages, seed 1708, six text lines/page,
16 MB fixture, 180 seconds per case/suite, 2 GiB memory, 1 GiB disk, 5000 files,
120-second worker lease. Corpus sizes are 1/8/32 four-page documents. Background
jobs are 1/2/4, provider capacity five with one interactive slot. Profiles never
increase extraction's 1000-page limit. A 1001-page refusal is an expected safety
outcome, not successful digestion. Increased page support is not evaluated.

## Fixture fidelity and reproducibility

`fixtures.py` creates actual pypdf page objects and content streams, with fixed
font/resources, seed and source facts. `fixture.json` retains expected lines for
every physical page; actual PdfReader counts are checked. Checksums bind PDF bytes
and canonical artifacts. Dependencies (including pypdf) are part of reproducibility:
a different writer/parser version may change bytes and canonical identities.

Low-density technical prose includes section labels and unique page/procedure
facts, page-5/page-180 opposing performance observations limited to 2025 and load,
and page-100/page-199 provisional/revised capacity. The page-3 payload contains
untrusted instructions. Exact source text and all source intervals are checked;
fixed facts are injected into the existing deterministic fake and verified in the
accepted digest. No true model comprehension is asserted. Native text does not
infer semantic headings, table cells, column order or OCR.

Small tests cover blank, image-only, graphics-only, native/image, columns, tables,
malformed/encrypted, misleading/long filenames, configured byte/artifact/chunk/step
refusals and partial coverage. Image fixtures are synthetic image XObjects, not an
annotated scan corpus. A mixed **page** can be native_accepted while retaining
has_images=true: COMPLETE measures accepted native coverage, not visual recovery.
Image-only units remain unsupported; mixed native/image-only documents are PARTIAL.
Columns can be flattened/merged. These are declared fidelity limits.

## Measurements and interpretation

Page results include source/artifact/plan/digest/manifest bytes, stages/depth/fan-in,
accepted steps/attempts/checkpoints, coverage, wall/CPU/RSS, ObjectStore calls/bytes,
SQLite size, vectors/embedding calls, publication/load/readiness and retrieval/
citation times. Constant fake vectors and identity reranking cannot demonstrate
semantic ranking quality. The separate corpus benchmark uses **real temporary local
Chroma** with those fake embeddings; no collection reset is performed.

Corpus queries select a shared document and disallow whole-corpus sparse scoring.
Explicit labels identify exact records from physical page 1, not semantic similarity.
Recall@8 = relevant returned / all labelled relevant; Precision@8 = relevant
returned / 8, counting unfilled slots as misses; reciprocal rank = 1 / rank of the
first relevant record. Empty relevance sets are unevaluated. Dense and sparse
metrics are separate; identity reranking has no learned-quality interpretation.
The corpus also executes multi-selection, interrupted candidate recovery, rollback
and tombstone enforcement with retained rows.

Latency runs retain every one of 100 samples for no/one/four background jobs.
The background workers hold a fake provider call while interactive requests use
real authorized retrieval/accounting. They finish afterward. This isolates
headroom and authority contention, not active model or CPU-saturating work. An
observed nearest-rank p95 is reported only with at least 100 samples, alongside
median/max/failures. It is not a statistically established production p95. The 17A
20% candidate target remains NOT ESTABLISHED for representative workloads, even
when the synthetic observation is above or below it. No sample is trimmed.

## Quality rubric and annotations

`quality.json` versions 12 authored questions, expected major findings, physical
pages, qualifications/opposition, sufficiency, criticality and identity rules.
`quality.py` materializes canonical document/version/EvidenceRef/span/excerpts from
an actually accepted 200-page benchmark digest. Its four exact synthetic factual
findings are checked against independently recorded source strings. A negative
control pairs valid coordinates with an unsupported critical conclusion.

The metrics API accepts explicit per-claim judgments with an annotation source;
it does not infer support from citations, similarity or model confidence. Required
findings are counted once per case. An abstention with factual claims is not a
correct insufficient-evidence abstention. Report numerator, denominator and null
for an empty denominator. Citation validity checks canonical identity/span/page/
excerpt and a separately supplied authorization decision. Live authority behavior
is tested separately; that boolean is not an authorization implementation.

For actual model evaluation, retain output hashes and source/selection snapshots;
have independent reviewers segment factual claims and judge support, criticality,
required findings, qualifications/opposition and abstentions. Instantiate
`Observation` / `ClaimJudgment` with category `human-reviewed-model` and a traceable
reviewer record. A category label alone is not certification. Preserve all negative
and insufficient-evidence cases, disagreements, sample selection and denominators.
Use the proposed 100%/95%/90%/zero-critical targets only after representative
independent review. Independent human question-answer semantic acceptance is DEFERRED; representative quality remains unestablished.

## Recovery and cleanup

Tests terminate a fresh interpreter with os._exit after claim/write/commit and
reopen the durable authority. Controlled clocks avoid sleep-dependent lease tests.
Accepted manifests survive; unaccepted work is retried/fenced; cancellation blocks
acceptance. The harness explicitly invokes reconcile and dispatch. There is no
automatic scheduler or two-lease autonomous recovery guarantee. Uncertain paid
usage must remain reserved until trusted usage evidence reconciles it.

Generated directories are retained intentionally for audit and operator cleanup.
No background child should remain after a watchdog finishes. Do not delete shared
runtime state, reset a Chroma collection, or mark purge complete. Review the exact
synthetic output path before optional manual cleanup. No cleanup is needed in
cloud services because none are used.

## Separately gated Foundry validation specification — DO NOT EXECUTE

The operator must supply and explicitly approve subscription/project/deployment,
endpoint/credential handling, verified exact model/capability/structured-output
profile, quota availability and applicable input/output prices. Do not discover
these through existing credentials. Use only synthetic or consented redacted
sources, approved region/retention, and private audit output.

Start with one small control document, then at most one 200-page low-density
fixture; 500/1000-page real-model cases need a new explicit budget after inspecting
results. Pre-plan the DAG and stop if it cannot fit the approved capability.
Proposed ceiling: 50 total attempts including retries, 25,000 reserved input tokens
and 3,000 output tokens per attempt, <=1,250,000 input and <=150,000 output tokens
in total, concurrency 1, RPM <=2 and TPM <=30,000 **or lower operator quota**.
These are proposed caps, not verified model capabilities. Reject any rendered
request that exceeds the caps. Retries consume the same total call/token budget.

Estimate maximum planned expense as `(reserved_input * operator_input_price +
reserved_output * operator_output_price) / operator_price_unit`, plus explicit
other billable charges if applicable. A maximum monetary budget and prices must
be supplied and approved by the operator before any call. Reserve through both
existing governance/admission authorities. Missing/partial usage remains unknown;
stop on uncertain outstanding exposure, repeated 429, timeout, missing usage,
capability mismatch, output/provenance/security failure or approved budget limit.
Do not switch models or raise quota automatically.

Preserve source/fixture/profile hashes, plan/attempt IDs, redacted requests/results,
usage versus reservation, pricing version, latency/errors, canonical citations and
independent rubric judgments. Test direct/distant/qualified/conflicting/absent and
adversarial cases; include unsupported critical conclusions in the review. Cleanup
means bounded local audit retention and operator-approved removal of temporary
validation artifacts, never deletion of shared documents/deployments. No capacity
changes, model deployments or credentials retrieval are authorized by this spec.
The historical specification above is not a new execution requirement. Controlled
v11 Foundry validation is now PASS; independent human semantic acceptance is
DEFERRED. Phase 17I preparation may proceed independently, with external exposure
subject to appropriate quality evidence and separate consent/privacy/quota/cleanup
approval. See the current completion decision for the exact handoff.
