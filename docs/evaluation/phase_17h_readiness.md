# Phase 17H readiness and predeclared evaluation design

Baseline: clean master, `45555394c350da7dfc18ed9409569dedefc8e789`.
Assessment precedes implementation. No production limits are changed.

1. **Validated sizes:** extraction permits 16,000,000 source bytes, 1,000 physical
   pages, 4,000,000 characters, 100,000 blocks and 32,000,000 artifact bytes.
   Earlier digestion tests use 200/500/1000/1200 logical text blocks, not physical
   PDFs. There is no default production digestion profile or measured real-model
   1,000-page contract. Historical 690 passing tests do not establish scale.
2. **Larger inputs:** PDF page admission rejects 1001. Digestion additionally caps
   chunks at 900 and steps at 1000, with explicit source-unit, depth, fan-in,
   character, JSON/context and result budgets. Extraction success does not imply
   digestion acceptance. Keep these limits; test deliberate refusal separately.
3. **Growth:** pypdf materializes pages/content; canonical text is duplicated in
   blocks and serialized JSON. Plans, job admissions, checkpoint graphs and
   publication inventories are materialized. The parser has no hard internal CPU,
   decompression or memory sandbox. Use external bounded subprocesses for stress.
4. **Repeated validation:** `admit` rebuilds the plan. Each worker fetches all job
   steps; finalization reopens and validates every checkpoint. Publication
   `accepted` recomputes the final digest. Prepare/activate/load/pin/retrieve/
   citations/annotations revalidate inventory and source graphs. Authorized
   retrieval limits validation to selected documents, but readiness validates the
   full generation. Per-document BM25 construction scans all generation records.
   Record costs; no integrity/authorization caching is introduced.
5. **Concurrency:** SQLiteJobLedger opens short transactions, BEGIN IMMEDIATE for
   writers and BEGIN for reads. Security/governance and provider authorities use
   BEGIN IMMEDIATE with five-second busy timeout, including protected response
   release. Same-host shared database files coordinate connections/processes;
   copied databases and distributed replicas do not. Inference-attempt limits
   are not queued/running-job quotas. No scheduler or fairness guarantee exists.
6. **Failed attempts:** governance reserves owner and tenant balances atomically,
   then provider admission must succeed. Admission failure releases unspent
   reservation; execution with missing/partial usage stays unsettled. Genuine
   retries have separate attempt identities. Unknown expense crosses periods.
   Unfinished provider slots require trusted reconciliation, not timeout refunds.
7. **Interruption:** job leases fence late writes; outbox and reconciliation permit
   redelivery. Artifact writes before ledger commit can leave retained orphans.
   Candidate vectors are incremental; old activation remains authoritative until
   CAS activation. Deterministic upserts recover candidates. A scheduler must
   invoke reconciliation/relay; two-lease autonomous recovery is not established.
8. **Existing executable evidence:** job integration covers fresh interpreter
   reads, stale leases, cancellation, lost ACK, storage retry and checkpoint reuse;
   managed tests cover retry-after/timeout/usage and bounded retry exhaustion;
   publication tests cover partial writes, activation interruption, rollback,
   corruption and local Chroma filtering. Extend process termination and workload
   evidence rather than duplicate these suites.
9. **Revocation:** snapshots revalidate before provider execution and after result;
   middleware serializes actual response sends with authority mutations. Revocation
   acknowledged before a send prevents protected bytes. Earlier bytes cannot be
   recalled. Tombstones override rollback; purge remains PURGE_PENDING. OIDC legacy
   query/stream remains disabled. Test multiple authority instances on one DB.
10. **Quality:** offline tests can establish exact coordinates, authorization,
    inheritance, evaluator arithmetic, known synthetic assertions and ranking
    against explicit labels. Semantic support, useful synthesis and natural-language
    prompt-injection resilience require representative real-model output and
    independent review. Citation shape alone is insufficient.
11. **17A targets:** 100% structural validity is testable on executed samples.
    95% expert-supported claims, 90% major findings and zero critical unsupported
    conclusions remain proposed targets, not certified by fake output. Interactive
    p95 degradation <=20% and recovery within two leases remain NOT ESTABLISHED
    unless workload/scheduling evidence supports the comparison.
12. **Bounds:** inspected host reports 8 CPUs, 16,684,544,000 RAM bytes (approximate
    from /proc), >12 GiB available RAM and >800 GiB free temporary filesystem.
    Sequential page cases: 4,200,500,1000,1001. Per child: 180 seconds, 2 GiB address
    space, 1 GiB disk, 5000 generated files, 16 MB fixture. Parent enforces wall,
    sampled disk/file budgets; limits are benchmark budgets, not application SLOs.
    Concurrency tests use 1/2/4 small jobs and synthetic shared admission. No
    simultaneous 1000-page jobs, cloud calls, model downloads or containers.

## Evidence categories and checkpoints

H1 records this assessment and fixed profiles. H2 executes physical PDFs and type
fidelity. H3 tests concurrent jobs/process interruption and reuses fault contracts.
H4 exercises full publication and authorized retrieval with fake embeddings plus
local Chroma contracts. H5 versions a rubric, observations and explicit metrics.
H6 records resource costs and only corrects reproduced critical defects. H7 runs
one final full regression, compile/Compose, diff/secret/artifact review and report.

Hard invariants are application limits, authorization, provenance, fencing and
accounting. Resource budgets are operator-adjustable harness caps. Timing is an
empirical single-host observation; fake token counts are not provider billing.
Real-model/expert and live Foundry gates remain PENDING; Phase 17I is not started.
