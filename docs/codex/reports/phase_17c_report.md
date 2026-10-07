# Phase 17C — Durable Job Orchestration, Idempotency & Recovery

Date: 2026-10-07. Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`.
Branch: `master`. Authorities: [Phase 17A](phase_17a_report.md),
[Phase 17B](phase_17b_report.md). Task: [finalized prompt](../prompts/phase_17c.md).

## 1. Executive summary

Implemented a local durable orchestration package around the unchanged Phase 17B
contracts. A transactional ledger owns admission, plans, attempts, leases, accepted
manifests, cancellation, progress and recovery. Immutable bytes remain in the
object store. A provider-neutral ledger port has a standard-library SQLite
reference adapter; an injected worker and local dispatch adapter prove at-least-
once recovery without a broker, cloud service or public upload endpoint.

The critical result is one accepted committed manifest per logical execution key,
including under competing claims, lease takeover, cancellation and redelivery.
Retries reuse persisted timestamps/configuration and reproduce Phase 17B artifact
identity. Successful compatible checkpoints are retained across new resumed runs.
No exactly-once execution or billing guarantee is made.

## 2. Phase result

**Phase 17C — PASS.** Local durable job orchestration, idempotency, leasing/fencing,
bounded retry, cancellation, outbox, manifest acceptance and recovery contracts
are implemented and validated. This establishes readiness for **Phase 17D —
Hierarchical Evidence-Grounded Digestion**, which has not been started.

SQLite is a local/reference adapter, **not approved shared multi-replica AKS
production state**. This result does not establish production database/queue
infrastructure, public-upload safety, LLM digestion, Foundry document integration,
RAG publication, multi-user authorization or completion of Phase 17.

## 3. Starting worktree state

HEAD: `f9b47fda4658935b64826f1d4abe0488c64f21ae`. Starting status:

```text
## master...origin/master
 M README.md
 M docs/codex/reports/phase_16_report.md
?? docs/codex/prompts/phase_17a.md
?? docs/codex/prompts/phase_17b.md
?? docs/codex/reports/phase_17a_report.md
?? docs/codex/reports/phase_17b_report.md
?? documents/
?? tests/integration/
?? tests/unit/documents/
```

Before edits, `/tmp/polymind-phase17c-baseline` captured exact expanded status,
HEAD, tracked diff/stat, SHA-256 hashes of every Git tracked/unignored file and
snapshots of README, documents, document/integration tests and Codex artifacts.
The starting tracked diff was 1,667 insertions / 1 deletion: README 37 added lines;
Phase 16 report 1,630 additions / 1 deletion. These are prior work, not 17C edits.
All baseline files except the intentional cumulative README change remain
byte-identical. No previous prompt/report or Phase 17B implementation/test changed.

## 4. Scope and exclusions

Included local domain models, transactional persistence, service verification,
profile/step identity, lease/attempt/retry/cancellation semantics, manifests,
outbox/local dispatch, injected execution, compatible resume, reconciliation,
orphan candidates, deterministic tests and documentation.

Excluded production storage/queues, deployment changes, cloud SDKs, public APIs,
LLM/prompt/synthesis behavior, quotas, OCR integration, retrieval publication and
authentication. No dependency was added. Existing FastAPI lifecycle, inference,
Redis conversation memory, Chroma, RAG, Docker and Helm semantics are unchanged.

## 5. Architecture

```text
Trusted caller -> DocumentJobs -> JobLedger -> SQLite reference adapter
                       |               |
                  ObjectStore       transactional outbox
                       |               |
                 immutable bytes <- injected worker <- local dispatcher
```

`DocumentJobs` validates and verifies sources/checkpoints outside database
transactions, then invokes the ledger. Workers use `StepHandler` and `ObjectStore`
ports, not SQLite APIs. `IntentStore` decorates the existing immutable storage port
with durable write intents. The relay and reconciler use ledger operations.
Messages carry opaque scoped IDs, not content or authoritative state history.

## 6. Job model

Frozen validated `Admission` contains scope, document/version, source reference,
bounded idempotency key, display metadata, MIME, complete processing profile,
ordered dependency plan and optional `resume_from`. Source lineage must match the
Phase 17B scoped content-version derivation. Plans have 1–1,000 unique units;
dependencies must name earlier units, preventing cycles and missing parents.

Frozen `Job` snapshots expose UUID job/run identity, a positive generation,
admission/fingerprint, created/updated/document-created timestamps, state,
cancellation flag, persisted progress and terminal category. Generation increases
within `(scope, document_version)` under the admission transaction. No public
identity/authentication system is introduced.

## 7. Step and state model

The executable vocabulary is deliberately small. Initial admission requires an
already verified source and atomically creates QUEUED state; separate registration/
upload transfer states would describe an upload protocol not implemented here.
Job states are QUEUED, EXTRACTING, NORMALIZING, VALIDATING, COMPLETED, FAILED,
CANCEL_REQUESTED and CANCELLED. PARTIAL is reserved terminal vocabulary; no partial
completion or quality policy is implemented. Only extraction has a concrete
production-domain handler. Other stage names support injected local contract tests.

| Step transition | Required operation/precondition |
| --- | --- |
| PENDING → READY | All specified parents succeeded; seal inputs/key and enqueue atomically |
| READY/RETRY_WAIT → RUNNING | Eligible time, active job, no cancellation; acquire lease/attempt |
| RUNNING → RUNNING | Current unexpired owner/fence renewal |
| RUNNING → SUCCEEDED | Valid owner/fence/expiry, no cancel, valid registered manifest |
| RUNNING → RETRY_WAIT | Classified transient failure or expired lease, within retry budget |
| RUNNING/eligible retry → FAILED | Permanent failure or exhausted attempts/deadline |
| PENDING/READY/RETRY_WAIT → CANCELLED | Durable cancellation or sibling terminal failure |
| RUNNING → CANCELLED | Cooperative cancel settlement/expiry or terminal sibling fencing |

Terminal steps are never reset. Resume inserts a new job/run and leaves old audit
rows intact. There is no arbitrary state setter. RUNNING includes acquisition;
a separate LEASED state adds no useful local guarantee. CHECK constraints enforce
state vocabulary, nonnegative fences and lease-field consistency.

## 8. Idempotency design

A database UNIQUE constraint on `(scope, request_key)` plus an immediate write
transaction arbitrates concurrent admission. Matching fingerprints return the
original immutable job without new steps, attempts or dispatch. Differing inputs
raise `idempotency_conflict`. Identical keys in another scope are independent.
Cross-scope lookup returns `job_not_found`, the same as a nonexistent job.

The service checks source integrity on admission; an unavailable/corrupt source
can therefore fail verification even for an otherwise duplicate request. The
ledger's admission operation itself is idempotent independently of object access.

## 9. Request and processing-profile fingerprints

Canonical sorted compact JSON is hashed with SHA-256. The request fingerprint
covers scope, document/version, full source ref/hash/size, display metadata, MIME,
profile, ordered plan and resume origin. Display metadata affects Phase 17B bytes,
so changes intentionally conflict. Only the idempotency key is excluded; incidental
admission/execution timestamps never enter this fingerprint.

The profile fingerprint covers explicit schema, extraction/normalization/policy/
parser versions, processing version, effective limits, structural intent and retry
policy. A compatibility fingerprint substitutes that profile digest and excludes
request key, resume origin and plan. Individual specs and recursively compatible
parents determine which planned checkpoints can actually be reused. Changing retry
policy conservatively invalidates reuse along with other profile changes.

## 10. Step-key design

Every step has a stable UUID row identity for dispatch and dependency bookkeeping.
PENDING rows have a deterministic reservation key derived from run and spec. Before
first becoming runnable, the transaction seals the execution input fingerprint
from request compatibility, stage/unit/schema/config/dependency spec and ordered
parent ObjectRefs, including hashes. The execution key hashes scope, version,
run UUID, generation and that input fingerprint.

Thus the reservation key is finalized once at PENDING → READY; it is not an
execution/cache key before then. After activation, retries never change it.
Worker/lease owner, fence, attempt and current time are excluded. Reused checkpoints
receive new-run keys from their preserved input fingerprints and explicit
`reused_from` links. No already executed key is rewritten.

## 11. Stable retry and extraction execution identity

Admission persists document creation time, a step execution timestamp, parser
version and all effective resource limits before dispatch. Extraction uses those
values explicitly. Environment changes after admission cannot change effective
limits. A mismatched installed parser, step schema or unsupported handler-specific
configuration fails `profile_mismatch` rather than silently changing bytes.

Retries retain timestamp, key, source, configuration and display metadata. The
object-written/no-manifest integration test reproduces exactly the same canonical
bytes and ObjectRef after expiry and restart. No Phase 17B file needed modification.

A deliberately new run reserves a timestamp at least one microsecond after prior
execution timestamps for that scoped version, even if the controlled wall clock is
unchanged. This is an execution-identity reservation, not measured work start time;
attempt start/end retain the actual injected clock. Compatible reused checkpoints
preserve their old execution timestamp and object identity.

## 12. Ledger abstraction

`JobLedger` defines explicit admission, scoped reads, attempts, claim, renewal,
commit, failure, cancellation/settlement, object intents, outbox discovery/receipt,
reconciliation, orphan candidates and dead-letter operations. It contains no SQL,
SQLite paths, provider-specific queue code or generic update API. Future adapters
must reproduce atomic preconditions and pass these contract scenarios.

## 13. SQLite reference adapter and configuration

`SQLiteJobLedger(JobSettings(...), clock)` opens/closes a connection per operation.
Writers use `BEGIN IMMEDIATE`; reads use snapshot transactions. SQLite arbitrates
threads and processes; there are no Python locks. Foreign keys are enabled,
synchronous mode is FULL and connection busy timeout is explicit. Default rollback
journaling is sufficient for these short serialized transactions; WAL was not
introduced without a need. There is no ORM or connection-pool dependency.

`DOCUMENT_JOBS_` settings: DATABASE_PATH is required; BUSY_TIMEOUT_SECONDS defaults
to 5; LEASE_SECONDS to 30; REDELIVERY_SECONDS to 30; ORPHAN_GRACE_SECONDS to 86,400.
The database must have an absolute path in an existing operator-controlled
parent. Obvious symlinks/ancestor symlinks, directories, hard links and relative
paths are rejected. New files use mode 0600. This is not protection against a
hostile account replacing filesystem ancestors concurrently. No default root DB,
shared filesystem/AKS approval, database provisioning or migration framework exists.

## 14. Database schema and version

`PRAGMA user_version=1`; initialization is transactional. Reopening validates the
version and exact expected user table/index definitions. Unknown databases,
additional/incompatible schema objects, missing indexes and malformed database
files fail safely rather than being silently accepted or migrated.

Eight tables are used: `jobs`, `job_steps`, `step_attempts`, `artifact_manifests`,
`manifest_objects`, `outbox`, `dead_letters`, `object_intents`. The normalized
manifest-object key index enables conservative orphan anti-joins without parsing
all stored JSON or requiring SQLite JSON extensions. Indexes cover scheduler
eligibility/expiry, outbox eligibility/per-step recovery, object age/key, source
references and accepted manifest keys. PK/FK/UNIQUE/CHECK constraints back the
workflow preconditions. Structured immutable inputs remain validated JSON.

## 15. Transaction boundaries

Admission inserts job, all planned steps, reused manifests if applicable, initial
runnable outbox and progress atomically. Claim creates the attempt and increments
fence/attempt together. Retry records the finished attempt, not-before state and
outbox together. Cancellation records intent and cancels unstarted work together.
Commit accepts one manifest, succeeds the attempt/step, activates dependency-ready
successors, creates their outbox and updates progress in one transaction.

No parser, source read, object write or queue send occurs while holding a database
transaction. Failure-injection triggers prove admission/outbox rollback and prove
manifest/successor/outbox rollback retains RUNNING with no accepted manifest.
Raw SQLite failures are normalized and failed operations roll back.

## 16. Lease semantics

Claim returns a scoped `Lease` with job/step, owner and increasing fence. Only READY
or eligible RETRY_WAIT can claim; pending, terminal, cancelled and already-active
work cannot. Renewal validates current owner/fence and unexpired time. Expiry is
`lease_expires_at <= now`; both claim and reconciliation recover it through the
same retry policy, including backoff and bounded interruption attempts.

The harness has no automatic background heartbeat. A bounded handler must finish
inside its lease or a supervising runner must call `renew`; renewal is a tested
ledger operation. Lease expiry is a correctness boundary, not parser preemption.

## 17. Fencing semantics

The active owner and monotonically increasing fence are checked inside the writer
transaction, together with state, job cancellation and lease expiry. Job/run
identity is fixed through the immutable step-to-job relation. The A/fence-1 →
expiry → B/fence-2 → B commit → A late-commit test rejects A. Forged higher fences
and other owner IDs also fail. Fencing does not rely on timestamps alone.

For an already accepted manifest, only the committing fence/attempt owner can
repeat the identical commit idempotently; another manifest conflicts. Repeated
receipt does not activate successors again. A previously accepted result is not
retroactively undone by later cancellation of another step in the same job.

## 18. Attempt history

Each acquisition appends `(step_id, attempt_number)` with unique fence, worker,
start/end, outcome, safe category/classification and optional retry time. Crashes
remain RUNNING until durable recovery records worker_interrupted. Successful,
failed, cancelled and retried attempts persist across fresh adapters and processes.
Reused checkpoints add no fabricated attempts; their origin is explicit.

## 19. Retry and backoff model

Default policy: maximum 3 attempts, base 1 second, cap 60 seconds, total retry
window 3,600 seconds, zero jitter. Configured jitter deterministically derives a
fraction from key/attempt and scales capped exponential delay within the declared
range. The selected `not_before` is persisted; restarts do not resample it.

The window begins with first actual acquisition. A retry cannot be scheduled at
or beyond the deadline; a delayed claim after the deadline fails terminally. This
is a retry/admission budget, not a hard timeout on running parser code. Maximum
attempts include interrupted attempts. Exhaustion becomes `retry_exhausted`, while
audit history retains the original failure category/classification.

Document validation/integrity failures are non-retryable. `storage_error` is
non-retryable by default; an injected classifier must have explicit knowledge of
transience to retry it. No LLM/provider retry or billing assumption is added.

## 20. Cancellation semantics

Cancellation durably sets intent and cancels PENDING/READY/RETRY_WAIT steps. Active
leases remain represented until cooperative settlement or expiry; the job stays
CANCEL_REQUESTED while any remain. All new commits, renewals, write intents and
successor activation require no cancellation. Commit/cancel races serialize at
the database: either acceptance precedes cancellation, or acceptance is rejected.

A worker reporting CANCELLED must first pass the current lease check in the same
transaction; a stale worker cannot cancel a newer owner's job. Multiple-active-
lease tests prove final CANCELLED waits for settlement. Completed checkpoints are
retained. Arbitrary third-party calls may continue physically after lease expiry;
no immediate termination or refund is promised.

## 21. Artifact-manifest commit

`IntentStore` registers the expected scoped reference before writing, including a
hash computed over bounded bytes. The store returns an identical immutable ref;
the worker inspects returned artifacts to verify bytes before conditional commit.
The ledger requires nonempty distinct artifact refs, matching scope and registered
intents, and checks all lease/state conditions transactionally. Direct ledger
callers are trusted to provide verified refs; the worker/service enforce object
verification. The ledger never pretends SQL can verify external bytes atomically.

A stale/cancelled writer may leave bytes but cannot make them accepted output.
Manifests are insert-once per step. Hash/reference conflicts never overwrite them.
`manifest_objects` preserves accepted-key protection for original and resumed runs.

## 22. Transactional outbox

Admission, dependency activation and retry transitions insert dispatch rows in the
same transaction. Relay sends first and records delivery afterwards. A send with
lost receipt can be repeated. Pending discovery excludes work that is terminal,
cancelled, already running or not yet eligible, including old outbox rows for a
step now in backoff. Multiple relays/deliveries remain safe through ledger claims.

Delivered means handed to transport, not processed. An in-memory transport may
lose all messages; reconciliation recreates dispatch after the redelivery interval
if an eligible step remains unclaimed. Old delivery rows remain audit information.
No queue retention or exactly-once delivery assumption determines job correctness.

## 23. Local dispatcher and worker model

`WorkDispatcher` exposes send, receive and acknowledge. `LocalDispatcher` is a
small deterministic deque fixture: receive leaves the head until acknowledgement.
`relay` is bounded. `Worker.once` claims, loads durable metadata, invokes an
injected `StepHandler` through tracked storage, verifies output and conditionally
commits or records failure before acknowledgement.

Ledger/manifest errors leave delivery unacknowledged; expiry/reconciliation can
recover. Stale leases cannot mutate results. `BaseException` process-interruption
fixtures escape the ordinary failure handler so leases really remain unsettled.
The worker does not start automatically at import or FastAPI startup. No threads,
async task framework, cloud queue, broker or service deployment was added.

## 24. Recovery model

All accepted state survives a fresh connection and fresh interpreter. Source and
artifact objects are immutable and separately durable. Unsent outbox survives
admission/relay crashes. Sent-but-unclaimed work is redispatched after the recovery
interval. Interrupted attempts expire through bounded retry; committed-but-unacked
work is not reexecuted. RETRY_WAIT preserves both eligibility time and execution
identity. Old attempt/terminal rows remain evidence, never reset to hide failure.

Tests simulate most crash boundaries by stopping orchestration at a boundary or
raising SystemExit. Fresh-interpreter reads and separate-process concurrent
admission are also tested. These are not power-loss, kernel/filesystem fault or
cloud-backup/restore certifications.

## 25. Reconciliation

`reconcile(limit)` bounds each repair query to 1–1,000 rows: recover expired leases,
settle inconsistent runnable work under terminal jobs, and recreate missing/lost
runnable dispatch. Per-job propagation is additionally bounded by the 1,000-unit
plan cap. It reports repairs, actionable undelivered outbox and orphan candidates.
Undelivered records are replayed by the relay rather than marked sent speculatively.
Normal successor activation is already atomic, so it has no ordinary split-commit
recovery window. Tests inject missing dispatch and terminal/runnable inconsistency.

This is a bounded local repair pass, not a scheduler daemon, global fairness/SLO
implementation, complete database-corruption repair or destructive collector.

## 26. Orphan-object handling

Durable write intents precede managed worker puts, so a crash inside/after a put
leaves a known candidate even when the physical write never completes. After the
configured grace interval, candidates require a settled originating step and no
job-source reference, committed manifest reference or active intent for that key.
Indexed anti-joins protect references across other runs, including reused results.
Read-only candidate enumeration and reconciliation are idempotent.

**Physical deletion is deferred.** Candidates are retention/inspection plans;
they may represent absent bytes. Any future collector must inspect existence,
recheck all references and active writers transactionally under an appropriate
cleanup protocol, observe grace/retention policy, and never delete accepted data.
No ObjectStore list/delete API was added. Unregistered source uploads, writes
outside IntentStore and Phase 17B `.pending`/hard-link leftovers are outside this
registry; low-level interrupted-filesystem-write repair is not implemented.
The workflow guarantees tested here cover completed immutable puts followed by
worker interruption. All job-referenced sources are retained conservatively.

## 27. Dead-letter and terminal failure

Permanent failures/exhausted budgets mark the step and job FAILED, retain a
sanitized dead-letter row, and cancel/fence sibling runnable/active work. Previously
successful checkpoints remain readable. Late sibling commits fail. No infinite
redispatch occurs. Failed runs never become runnable again; trusted manual resume
means new admission/key/run referencing the old run, not an operator replay API.
A terminal sibling failure fences other active work immediately; this differs from
user cancellation's explicit cooperative settlement status.

## 28. Checkpoint reuse and resume

A new request may name a terminal prior job in the same scope and source version.
With compatible source/metadata/profile, a successful step is reused only when its
spec is identical and all dependencies are themselves reused. Therefore inherited
parent manifests/hashes remain identical; changing an ancestor invalidates its
descendant checkpoints. Changed profiles require new work. Existing failed jobs
and attempts are byte-preserved database records, not reclassified successes.

The service verifies candidate checkpoint bytes before new admission. Corruption
fails integrity checks. The ledger copies accepted refs transactionally, records
origin, and dispatches only unfinished compatible-plan work. Tests show real
extraction is not dispatched again after later validation failure, all-complete
resume needs no execution, and changed profiles produce new artifacts even with
an unchanged clock. No cross-scope content cache exists.

## 29. Progress model

Persisted snapshots count total known steps, completed, running, retrying, failed,
cancelled and pending/ready work plus the first active stage. A plan is fixed at
admission in this reference implementation; dynamic fan-out is not implemented.
Counts mean logical units, not page-quality percentages. COMPLETED means the
requested local workflow accepted every planned manifest; it does not assert every
PDF page is extractable or that a digest/publication is complete. Phase 17B's page
failure/OCR/layout decisions remain inside canonical artifacts for later policy.

## 30. Security considerations and observability

Every job/step operation checks trusted scope; another tenant cannot distinguish
unknown jobs through the lookup boundary. Immutable lineage is revalidated at
admission/manifest boundaries, including unchecked model-copy attempts. Tokens
are bounded; SQL uses parameters. Errors retain only allowlisted categories;
unknown/raw document, parser, queue and SQL text is suppressed at operational
boundaries. Tests include malicious synthetic text; no real credentials or private
documents were introduced. Internal Pydantic construction errors are not a public
API contract and must not be exposed by future endpoints.

No logs or metric labels containing content/IDs/paths were added. Existing serving
metrics are tightly coupled to inference/memory/retrieval, so worker instrumentation
is deferred instead of importing that stack. Future bounded job/step state,
retry/dead-letter/expiry and repair counters belong in worker observability;
job/document/tenant IDs, names, hashes and keys must never become metric labels.
SQLite files/audit refs require operator-controlled access and later retention.

## 31. Process-isolation boundary

`StepHandler` is the orchestration execution boundary and Phase 17B `ParserRunner`
remains the parser boundary. A future supervising subprocess can implement them,
renew leases and enforce execution limits without moving authority out of the
ledger. Parser exceptions produce safe failure state; interrupted workers leave
recoverable leases and cannot publish after fencing.

The current handler runs in process. No hard CPU/RSS/time/pixel/decompression
sandbox, malicious-host filesystem defense or arbitrary-call preemption exists.
A hung parser can keep consuming resources despite losing commit authority. This
remains a production/untrusted-upload gate, not a hidden Phase 17C guarantee.

## 32. Concurrency tests

Tests synchronize two separate adapters/connections with barriers for identical
and conflicting admission, competing claims, identical/conflicting commits,
cancellation versus commit and expired renewal versus takeover. They accept either
legal transaction ordering while asserting one active claimant/accepted manifest.
Two actual OS processes also concurrently admit the same request and obtain one
job. No test relies on an application mutex or real sleep for correctness.

## 33. Failure-injection matrix

| Boundary | Evidence and durable result |
| --- | --- |
| A. Admission before dispatch | Reopened ledger retains job, READY step and outbox |
| B. Send before relay receipt | Same outbox message is sent again safely |
| C. Duplicate message | Second claim cannot own an active lease; committed step is not executed again |
| D. Lease before work | SystemExit leaves RUNNING; expiry/retry recovers |
| E. Object before manifest | Real extraction writes; restart retry reproduces identical bytes/ref |
| F. Manifest before worker ack | Ack exception leaves committed result; redelivery skips handler |
| G. Lease expiry/takeover | New attempt/fence follows persisted backoff |
| H. Stale first worker | Old fence rejected after newer accepted result |
| I. Retry-wait restart | Not-before, key, execution metadata and attempts survive |
| J. Cancellation while leased | Commit blocked; cooperative/expiry settlement produces CANCELLED |
| Outbox transaction failure | Trigger abort rolls back job or manifest/successor changes together |
| Poison/parser error | Safe FAILED/dead letter; no redispatch loop |
| Object intent before failed put | Candidate survives even when bytes never existed |
| Missing dispatch/terminal inconsistency | Bounded reconciliation repairs the ledger |
| Corrupt checkpoint before resume | Service rejects reuse with integrity_error |

## 34. Phase 17B integration evidence

Seventeen integration cases exercise actual text extraction, generated two-page
native PDF extraction, fresh-interpreter committed-result reads, exact retry
identity, same-clock profile reprocessing, explicitly transient storage failure,
malformed PDF terminal failure, cancellation/orphans, lost ack, pre-work process
interruption, dispatch failure, later-failure checkpoint reuse, source/scope
verification, parser/schema/config mismatch, persisted environment-independent
limits and corrupt checkpoint rejection. Fixtures are generated in temporary
directories using existing pypdf and stdlib. No external OCR, model, network service,
credential or retrieval publication is involved.

## 35. Performance observations

No throughput/scale benchmark was run and no production latency, capacity or SLO is
claimed. Reported pytest durations are local validation runtimes only. Plans,
manifest cardinality, reconciliation/relay batches and attempts are bounded.
SQLite serializes writers; each state transition can inspect up to the bounded
per-job plan. Large fan-out, fairness, database growth, archival and real parser
resource costs need Phase 17H evidence and an independently selected production
adapter. The adapter deliberately avoids speculative tuning.

## 36. Files created and modified

Created **11 files**:

- `documents/jobs/__init__.py`
- `documents/jobs/models.py`
- `documents/jobs/errors.py`
- `documents/jobs/ledger.py`
- `documents/jobs/sqlite.py`
- `documents/jobs/service.py`
- `documents/jobs/worker.py`
- `tests/unit/documents/test_job_ledger.py`
- `tests/integration/test_document_jobs.py`
- `docs/codex/prompts/phase_17c.md`
- `docs/codex/reports/phase_17c_report.md`

Modified incrementally: `README.md` only, updating Phase 17C status and linking
this local/reference implementation report. All other dirty paths predate 17C.

## 37. Targeted tests

Final Phase 17C suite: **95 passed** (78 ledger/unit cases and 17 integration
cases), in 3.41 seconds before final documentation edits. Commands:

```bash
python -m pytest tests/unit/documents/test_job_ledger.py tests/integration/test_document_jobs.py -q
python -m pytest tests/unit/documents/test_contracts.py tests/unit/documents/test_extraction.py tests/unit/documents/test_storage.py tests/integration/test_document_plane.py -q
python -m pytest tests/unit/test_deployment_topology.py tests/unit/test_retrieval_regression.py tests/unit/test_vector_store.py tests/unit/test_model_routing.py tests/unit/test_api_reliability.py -q
```

Phase 17B/document regressions: **54 passed in 1.12 s**. Selected serving/retrieval/
vector/config/deployment regressions: **68 passed in 15.41 s**. These counts overlap
the full suite; they are not additional to it. Validation logs are outside the repo
under `/tmp/polymind-phase17c-*.log`.

## 38. Full-suite and static validation

Final complete project suite: **380 passed in 18.49 seconds**, no failures or
skips (`python -m pytest -q`). This includes all 285 baseline tests and 95 new
Phase 17C cases. The final run includes the checkpoint-integrity, copied-key and
profile-fingerprint review fixes. Exact final worktree evidence follows in section 42.

`PYTHONPYCACHEPREFIX=/tmp/polymind-phase17c-pycache python -m compileall -q .`
passed, using external bytecode cache. `docker compose config --quiet` passed;
this was configuration inspection only. `git diff --check` passed; added untracked
text also received a separate whitespace/EOF check. No configured Python formatter,
linter or type gate exists in Makefile/CI; none was invented or installed.
No Docker build was needed: dependencies, Dockerfile and deployment were unchanged.
No Helm/cloud/cluster mutation or validation environment was required.

## 39. Implementation self-review and separate pre-commit review

Inspected the complete new models/port/adapter/service/worker/tests and incremental
documentation against the outside-repository baseline. Specific fixes included:

- A stale worker's CANCELLED failure initially risked cancelling a newer lease;
  cancellation now validates and mutates in one transaction, with a regression.
- Orphan lookup initially parsed all reference JSON; normalized accepted-key
  indexing and anti-joins now keep candidate results bounded and conservative.
- Old unsent messages could be exposed during a later retry wait; eligibility is
  now checked against the step as well as the outbox timestamp.
- Resume now verifies stored checkpoint bytes at the service boundary and derives
  copied keys from the preserved execution inputs under the new run.
- The concrete extraction handler rejects unsupported schema/config fingerprints
  rather than silently ignoring semantic changes.
- Rollback errors are normalized; additional tests cover conflicting completion,
  multi-lease cancellation, terminal sibling fencing, budget/reconcile bounds,
  schema constraints, forged active fences and persisted resource configuration.

Reviewed state/manifest/outbox atomicity, timestamp versus token fencing, scope,
terminal immutability, retry off-by-one/deadline behavior, cancellation, accepted
object protection, resource closure and conservative recovery limits. No
provider-specific inference or Redis/Chroma job authority was introduced.

The separate pre-commit review checked exact new-file inventory, baseline hashes,
README-only cumulative changes, secrets/private keys/credential URLs, debug/TODO/
local runtime paths, database/generated/temp files, dependencies, dead code,
documentation links and unintended API/deployment edits. Synthetic malicious
exception strings are test data, not real secrets. No stage/commit/push occurs.

## 40. Remaining limitations

Production database/queue/object adapter selection, HA/backups/restore and security
are unproven. SQLite and local POSIX storage are not a shared AKS solution. Physical
orphan deletion, pre-admission raw-upload orphan inventory and low-level filesystem
pending-file recovery remain deferred. No public authentication/authorization,
retention/deletion policy, cost quota or sandbox exists. Public uploads remain out
of scope and unsafe to claim production-ready.

The plan is bounded and fixed at admission; no dynamic fan-out or distributed
scheduler/fairness exists. The worker has no automatic heartbeat or hard timeout.
Normalization/validation are stage vocabulary for injected handlers, not new
content transformations. PARTIAL quality policy, large partitioned artifacts and
structural/LLM digestion remain later work. COMPLETED is local workflow completion,
not evidence-quality approval or publication. Duplicate external execution/billing
can still occur despite one accepted manifest.

## 41. Exact Phase 17D prerequisites

**Phase 17D — Hierarchical Evidence-Grounded Digestion** may now build on Phase 17B
canonical evidence and immutable objects plus Phase 17C scoped admission, stable
execution metadata, conditional checkpoints, attempts/leases, retries, cancellation,
outbox and resume. Preserve the provider-neutral boundary and begin with fake
inference as required by the Phase 17A roadmap.

Before expanding the plan, explicitly define structural units/dependency fan-in,
chunk/reducer schemas and profiles, evidence inheritance/coverage validation,
quality/partial-result policy and bounded output/resource budgets. Extend the
currently fixed local stage/plan contract intentionally if dynamic discovery is
needed; add schema/compatibility tests. Keep LLM/provider billing ambiguity and
production isolation/storage/security gates visible. Real managed inference is
17E, RAG publication 17F, authorization 17G and large-scale validation 17H.
This report does not authorize starting 17D or provisioning anything.

## 42. Git and no-commit state

Work remained on master at the original HEAD. Prior Phase 16 report changes and
Phase 17A/17B artifacts/code/tests were byte-preserved. Only README received an
intentional cumulative status update. Git's tracked diff includes earlier work
and excludes new untracked implementation; it must not be attributed entirely to
17C. Exact final status/stat and incremental counts are recorded below.

Commit created: **NO**. Push performed: **NO**. Branch created: **NO**.
Files staged: **NO**. Prior Phase 17 work preserved: **YES**.
No Azure mutation, Kubernetes mutation, Foundry call, external OCR call, production
DB/queue provisioning, new paid infrastructure or secret exposure occurred.
Phase 17D was not started. Phase 17 remains incomplete; all work stays uncommitted
for the operator's full 17A–17I review policy.

Final `git status --short --branch`:

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

Final tracked `git diff --stat`:

```text
 README.md                             |   41 +
 docs/codex/reports/phase_16_report.md | 1631 ++++++++++++++++++++++++++++++++-
 2 files changed, 1671 insertions(+), 1 deletion(-)
```

Incremental Phase 17C accounting: **11 new untracked files**, listed in section 36,
and **README 8 added / 4 removed lines** against the pre-17C snapshot. The tracked
stat above includes the accumulated Phase 16 report and Phase 17A/17B README edits;
it omits all untracked files. Phase 17A's two documents and Phase 17B's 18 files
remain unchanged, as does the complete starting Phase 16 report. No previous
implementation, test, dependency, API or deployment file was modified.

Final pre-commit audit verified all baseline hashes except intentional README,
all 11 new files with `git diff --no-index --check /dev/null <file>` and explicit
EOF/whitespace checks, four new relative documentation links, unchanged HEAD and
master, and an empty index. Secret/private-key/credential-URL/debug heuristics found
no issues; TODO mentions in documentation describe the review checklist, with no
new source TODO/FIXME. This is a scoped heuristic review, not a secret-scanner
certification. No database, binary fixture, runtime secret or temporary validation
log was introduced into the Git inventory. Final `git diff --check` passed.
