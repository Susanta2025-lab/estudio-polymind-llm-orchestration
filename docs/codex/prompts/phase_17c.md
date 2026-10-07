# Phase 17C — Durable Job Orchestration, Idempotency & Recovery

Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`. Branch: `master`.
Major phase: **Phase 17 — Production Document Digestion & Intelligence**.
Previous results: Phase 17A PASS; Phase 17B PASS, with 285 passing project tests.
This is the finalized clean task prompt, organized by implementation contract.
The operator's complete scope, acceptance boundary and no-commit policy govern it.

## Operator Git policy and preparation

**Do not commit any Phase 17 work until all of 17A–17I is complete and reviewed.**
Work directly on master; do not create a branch, stage, commit, push, reset, stash,
clean, restore, check out existing files, delete prior untracked files, rewrite
history or use Git as an intermediate Phase 17 checkpoint. The dirty tree is
intentional. Preserve Phase 16, 17A and 17B bytes, except necessary cumulative
README/roadmap updates. Keep temporary snapshots outside the repository.

Before editing, read root AGENTS.md completely, inspect `git status --short
--branch` and `git rev-parse HEAD`, and record an exact working-tree inventory and
outside-repository baseline. Read README, the full Phase 17A and Phase 17B reports,
and `docs/codex/prompts/phase_17b.md`. Inspect all `documents/` implementation,
`tests/unit/documents/`, relevant integration tests, interface consumers and
project persistence/configuration/error/service/lifecycle/concurrency/test/logging/
metrics conventions. Treat 17A/17B reports as architectural authorities.

## Purpose, scope and exclusions

Implement a durable local workflow foundation: validated jobs and logical steps,
idempotent admission, profile fingerprints, stable step identity, transactional
state transitions, attempt history, leases/renewal/expiry/fencing, cancellation,
bounded retries/backoff, outbox, local dispatch and injected worker execution,
conditional artifact manifests, checkpoint reuse, restart recovery/reconciliation,
orphan tracking, poison-work terminal outcomes and honest progress.

Use provider-neutral ledger and work-dispatch ports, with standard-library
`sqlite3` as the explicit local/reference transactional implementation. SQLite
proves contracts and recovery locally; it is **not approved shared multi-replica
AKS production state**. Do not add an ORM, SQLAlchemy, Alembic or database/cloud
SDK without proving a concrete need. Do not add Celery, RQ, Dramatiq, Temporal,
Redis Queue, Kafka, RabbitMQ or a cloud orchestration framework.

Do not implement hierarchical LLM digestion, prompts, summaries, Foundry document
inference, LLM retries, distributed inference quotas, RAG/Chroma/BM25 publication,
corpus cutover, multi-user authentication/Entra/production tenant authorization,
public upload endpoints, worker Kubernetes/Helm resources, HPA changes, production
queue/database/Blob provisioning or external user testing. No Azure mutation,
Kubernetes mutation, Foundry call or external OCR call is permitted.

## Architecture and package design

Keep immutable source/artifact bytes in object storage. The transactional ledger
is authoritative for job/step state, attempts, leases, cancellation, accepted
artifact references, dispatch/outbox and recovery. Redis remains conversation
memory; Chroma remains derived retrieval storage. Neither may become job, queue,
source or artifact authority. Queue messages are work references, not job history.
Assume at-least-once delivery and duplicate execution. Aim for one accepted
committed result per logical step key; never claim exactly-once execution/billing.

Reuse 17B canonical models, scoped references, extraction, serialization and error
categories. Preserve existing RAG, inference, FastAPI, Streamlit, Docker, Helm,
Redis and Chroma contracts. Use a cohesive shallow package such as
`documents/jobs/`; avoid unnecessary modules or speculative frameworks. Scope is
trusted domain context, not authentication. No public API is required.

## Jobs, steps, state and progress

Use immutable validated identity inputs. Persist job ID, scope, document/version,
source reference, processing profile/version, request idempotency key/fingerprint,
creation/update times, cancellation intent, high-level state, run/generation,
progress and terminal outcome. Suggested vocabulary includes REGISTERED, UPLOADED,
QUEUED, EXTRACTING, NORMALIZING, ANALYZING, SYNTHESIZING, VALIDATING, PUBLISHING,
COMPLETED, FAILED, CANCEL_REQUESTED, CANCELLED and PARTIAL; choose only useful
states, keeping job and step state separate. Execute only 17B/17C local stages.
Future stage vocabulary does not authorize future stage implementations.

Each independently durable step carries stage, unit, deterministic key, input
fingerprint, state, attempts, lease owner/expiry/fence, eligibility/retry timestamp,
start/finish times, sanitized failure and committed manifest. Define and document
valid transitions; terminal states must remain terminal for that run. Suggested
step vocabulary is PENDING, READY, LEASED/RUNNING, RETRY_WAIT, SUCCEEDED, FAILED,
CANCELLED. New/replayed incompatible work uses a new run/generation.

Persist counts of total known units, completed, running, retrying, failed and
cancelled plus current stage. Do not invent percentages or ETA. Known totals can
change if later work discovery is implemented. Do not store content in progress.

## Admission and execution identity

Uniqueness is `(scope, request_idempotency_key)`. Same key plus same deterministic
fingerprint returns the existing logical job; same key plus different inputs
raises a deterministic idempotency conflict, never a second job. Cover immutable
scope/document/version/source hash, profile and semantic operation/configuration.
Exclude incidental timestamps. Do not disclose cross-tenant duplicate content.

Persist stable execution inputs before work runs. Phase 17B wall-clock extraction
timestamps intentionally change extraction identity; a retry must reuse a
ledger-owned execution timestamp, source version, parser/profile/schema versions
and effective resource limits. Changing current time alone must not change retry
identity. A deliberate reprocess/profile change creates a new run/generation.

Step keys distinguish scope, source/version, run/generation, stage/unit, schema,
parser/profile, semantic configuration and relevant parent artifact hashes. They
must not include lease owner, attempt number, worker ID or current time. Same
logical retries retain the same key. Test compatible successful checkpoint reuse,
later-stage failure without repeated extraction, and changed-profile fresh work.

## Transactional ledger and SQLite safety

Define explicit provider-neutral operations for admission, scoped lookup, step
creation/transitions, claims/renewal, retry, cancellation, conditional commit,
outbox, terminal failure and recovery queries. Avoid a generic CRUD repository.
Use real explicit SQLite transactions and database constraints, not process-local
locks. Keep source/artifact I/O outside transactions and atomically accept refs.

Use only necessary tables, typically jobs, steps, attempts, manifests, outbox and
dead letters, with primary/foreign keys, scoped admission uniqueness, unique step
keys, fence/generation values, practical state checks and justified scheduler/
recovery indexes. Persist consistently normalized UTC timestamps. Configure
foreign keys and busy timeout; justify WAL if used; avoid over-tuning.

Require an explicitly configured database path; never implicitly create a root
repository database. Tests use temporary directories. Version the schema and
reject incompatible existing schemas. No database files may be committed.

## Leases, fences, attempts, retries and failures

A claim atomically grants owner, expiry and increasing fence. Renewal requires
current owner/fence and valid lease. Expired leases are recoverable. Only a valid
claimant may commit, and an old worker cannot commit after takeover. Prove A/fence
1 stalls, B/fence 2 reclaims and commits, then A's late commit fails. Timestamp
comparison alone is insufficient fencing.

Persist attempt number, worker, start/end, outcome, sanitized category, retry
classification and next eligible time across restarts. Never persist raw exception
text, filenames, paths, credentials or document content as failure information.

Retry policy includes maximum attempts, exponential/capped delay, deterministic or
injected jitter, total retry/deadline budget and durable `not_before`. Classify
RETRYABLE, NON_RETRYABLE and CANCELLED explicitly. Invalid/unsupported/encrypted/
oversized/page-limited/immutable-integrity failures are normally non-retryable.
Storage errors need context; do not automatically retry every storage_error.
Process interruption may be retryable. No provider-specific LLM retry behavior.
Exhaustion and permanent failure become terminal with sanitized dead-letter/audit
records and no infinite dispatch. Manual replay must preserve history and create
new generations when needed; no production replay API is required.

## Cancellation

Persist intent. Prevent new work admission/activation after observation. Cancel
runnable/retry-wait work, let active work settle or expire, and prevent in-flight
or stale workers from accepting results after the cancellation fence. Keep
CANCEL_REQUESTED distinct from CANCELLED until active work is settled. Do not
promise interruption of arbitrary third-party calls, refunds or immediate stops.

## Manifest commit and object lifecycle

Workers produce immutable bytes and verified ObjectRefs, then conditionally commit
using step identity, expected state and active owner/fence/generation. In one
transaction accept the manifest, mark success and create/activate successors and
their outbox records. Acknowledge the delivery afterwards. Duplicate same-result
commit may be idempotent for the appropriate owner/fence; conflicting manifests
and stale commits must fail.

Object writes and database commits are not a distributed transaction. Track
possible written-but-uncommitted objects, retain conservatively, and never delete
anything referenced by a committed manifest. Respect a configurable grace period;
cleanup must be idempotent. Prefer ledger-side intents/orphan candidates over a
broad destructive store interface. Physical deletion may remain deferred if
accurate tracking/detection, a retention contract and deterministic tests exist.
State the detection limits, including pre-registration/pending filesystem files.

## Outbox, dispatcher, worker and recovery

Whenever a transaction makes work runnable, add an outbox entry in that transaction.
Discover unsent entries, retry sending and tolerate send/ack loss and duplicates.
Job correctness must not depend on exactly-once relay delivery or queue retention.
Use a small dispatch port suitable for future Service Bus, Storage Queue or database
polling. Local in-memory transport backed by ledger/outbox authority is sufficient;
do not build a broker or add an external queue.

The worker claims eligible work, records attempts, invokes an injected handler,
verifies/conditionally commits artifacts or schedules classified failures, respects
cancellation and leaves crashed/expired leases recoverable. Exercise real 17B
extraction in a local service-level integration test, including a failure/retry
path. No LLM handler or retrieval publication.

Bound reconciliation batches. Identify/repair expired leases, undelivered outbox,
runnable steps missing dispatch and terminal jobs with inconsistent runnable work.
Detect stale artifact/object candidates where possible. Recovery must come from
persisted state, not worker memory. Never build a global destructive collector.

## Determinism, execution isolation and observability

Inject a narrow clock; do not scatter wall-clock calls. Tests control creation,
lease expiry, backoff, cancellation, reconciliation and orphan grace without sleeps.
Exercise actual SQLite transactions with concurrent admission/claims and where
practical completion/cancellation/renewal races. Database constraints must enforce
invariants independently of Python locks.

Put extraction behind an execution/handler interface where a future constrained
subprocess runner can fit. Contain parser failures so they do not corrupt durable
state. Hard CPU/RSS/time/pixel/decompression isolation may remain a documented
production-hardening gate. Do not claim public untrusted-upload readiness or build
a container sandbox platform in this phase.

Use allowlisted orchestration errors such as idempotency_conflict,
invalid_transition, job_not_found, step_not_found, lease_conflict, stale_fence,
lease_expired, retry_exhausted, cancelled, ledger_error, dispatch_error and
manifest_conflict. Never expose SQL, paths, names, keys, source content or secrets.
Optional metrics must use bounded dimensions; never label by job/document/owner,
filename, checksum, object key or exception text. Defer intrusive monitoring work.

## Required validation matrix

Test admission creation/idempotency/conflict/scope, valid/invalid/terminal
transitions, claim/renewal/expiry/takeover/fencing, persistent attempts and sanitized
failures, retry increments/backoff/budgets, atomic outbox/successor creation,
redelivery/lost acknowledgements/restart, valid/stale/duplicate/conflicting
manifest commits, pending/leased cancellation and cancellation/commit races.

Inject these crash boundaries: admission before dispatch; outbox send before ack;
duplicate delivery; lease before execution; artifact write before manifest commit;
manifest commit before delivery ack; lease expiry/resume; stale first-worker late
commit; retry-wait process restart; cancellation while leased. Verify durable
recovery, orphans/retention, compatible checkpoint reuse and profile changes.

Test scope mismatch and non-disclosing cross-scope lookup, key collisions, forged
fences, unsafe retries after failure, raw/malicious exceptions, invalid states and
SQLite configuration/path/schema safety. Include real concurrent idempotent
admission and competing claims. The real integration path is synthetic source →
admission → queued step → claim → 17B extraction → immutable artifact → conditional
manifest → success → restart → identical committed result.

Run targeted tests first, then Phase 17B documents, relevant existing regressions,
and the complete project suite. Full suite must pass unless a pre-existing
unrelated failure is independently demonstrated. Run compileall (external cache
if required), applicable repository-standard checks/Compose validation and
`git diff --check`, including untracked text whitespace. Do not invent lint/type
tooling. No tests may need cloud, network services, credentials, GPUs or OCR.
Small local measurements are optional; no production benchmarks/SLO claims.

## Review, documentation and final acceptance

Review the whole incremental implementation for races, nontransactional check/
write, timestamp-only fencing, worker-local authority, exactly-once assumptions,
regenerated retry timestamps, attempt off-by-one, cancellation/stale commits,
split outbox commits, mutable refs, lost scope, raw SQL/content logs, accidental
DBs, Redis/Chroma misuse, cloud coupling, premature LLM/RAG and overengineering.
Fix in-scope findings. Separately review secrets, debug/temp/generated artifacts,
paths, dependencies, TODO/dead code, unrelated edits, links and API compatibility.

Create this prompt and `docs/codex/reports/phase_17c_report.md`. The report must
cover executive summary/result, exact starting tree, scope, architecture, models,
state/key/fingerprint/retry identity, port/schema/transactions, leases/fences,
attempts/retries/cancellation, manifest/outbox/worker, recovery/reconciliation/
orphans/dead letters/checkpoints/progress, security/isolation/concurrency/failure
matrix/17B evidence, measurements if any, exact file inventory/test counts/static
outcomes, review fixes, limitations, exact 17D prerequisites and Git state.

PASS requires all implemented scope contracts proven, targeted/regression/full
checks passing, no private data/credentials, no cloud/cluster/inference/OCR calls
or provisioning, and no commit/push/branch/staging. Only then update README to
mark 17A, 17B and 17C complete; do not mark 17D started. Record final status and
tracked diff stat, distinguish prior Phase 16/17A/17B changes from incremental
17C, and verify baseline hashes. Confirm commit NO, push NO, branch NO, staged
NO, prior Phase 17 preserved YES.

Final response must concisely cover result, created/modified files, state/ledger/
identity/leases/retry/cancellation/manifests/outbox/recovery/orphans/terminal
semantics, extraction/concurrency/failure/test evidence, limitations, prohibited
operations not performed and incremental worktree accounting.

If all criteria pass conclude **Phase 17C — PASS**: a locally validated durable
foundation suitable for **Phase 17D — Hierarchical Evidence-Grounded Digestion**.
This is not production DB/queue infrastructure, safe public uploads, digestion,
Foundry integration, publication, multi-user authorization or Phase 17 completion.
**Do not start Phase 17D. Do not commit. Do not push.**
