# Reusable evaluation policy

Status — 12 November 2026: the [v11 controlled evaluation](../codex/reports/phase_17h_v11_controlled_live_execution_and_reconciliation.md)
completed 4/4 calls and settled EUR 0.009675030297596252 locally, with zero
outstanding reservations and one consumed approval. Final Azure invoice, VAT and
network charges are not verified. The
[completion decision](../evaluation/phase_17_engineering_completion_and_deferred_acceptance.md)
records `PHASE_17_ENGINEERING_COMPLETE`,
`DEFERRED_PENDING_TWO_INDEPENDENT_REVIEWERS` (0/2),
`PHASE_17_FORMAL_CLOSURE_PENDING` and `NEXT_PHASE_DEVELOPMENT_PERMITTED`.
The [deferred-review register](../evaluation/phase_17_deferred_human_semantic_review.md)
tracks acceptance; no policy, accounting threshold or spend authority changes.
Unknown usage continues to retain obligations and block continuation.

Historical 1 November checkpoint: [Attempt 6](../codex/reports/phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md)
closed PASS with one accepted analysis, known usage SETTLED and no automatic paid
retry. EUR 0.008817317845829546 remains its pinned October local-catalog cost,
not a current price or independently verified invoice. No budget reset or new
inference authorization follows from either historical result.

`polymind-evaluation/1` is an optional, versioned overlay inside the existing
`QuotaPolicy.evaluation` configuration. It is not a second database or a replacement
production policy. The base version, owner and tenant limits remain unchanged.
The fixed evaluation limits for both owner and tenant are 16 requests per rolling
86,400 seconds, 500,000 tokens per UTC day, 1,500,000 tokens per UTC month, EUR 5
per UTC month, 112,000 simultaneously reserved tokens, and one concurrent request
in each of the interactive and document-background classes.

Only exact server-derived tenant/owner pairs in the operator-owned allowlist
receive evaluation limits. All other principals, including other owners within
an allowlisted tenant, receive base limits. These are dedicated development
identities: do not authorize a production identity for evaluation or reuse an
evaluation identity for production. An Entra tenant identifier alone is NOT the
internal `Scope.tenant`; use the existing verified principal's derived Scope.
The allowlist is policy administration, not a client request parameter. RBAC still
revalidates each execution. This does not provide isolation from an administrator
who can edit policies, replace databases or change application code.

Every request counts against all historical owner and tenant rows in the same
authority, regardless of the policy version on the row. Evaluation spending thus
also counts against a non-evaluation caller's base tenant limits. Selected limits
are not independent pools: new experiments never acquire a fresh EUR 5 budget.
Settled calls still count in the rolling request window; released calls also
retain their request count. Actual usage replaces reservations only after known
settlement. Unknown and unfinished reservations survive period boundaries.
No history is deleted and no allowances are forgiven or reset by migration.

The binding pins the existing governance path, provider admission path, shared
quota key and SHA-256 of `AdmissionPolicy.model_dump_json()`. Both application
runtime and L1 pass these into the ledger; mismatches fail before ledger creation.
L1 additionally validates the authorized evaluation scope before approval
consumption. Provider RPM, TPM, concurrency and per-job limits remain unchanged.
All workers must use these same single-host authorities. SQLite is not a
cross-host or AKS distributed admission authority; distributed deployment would
require a centralized transactional governance/admission service before use.
Never clone the authority for a new experiment. Changing the binding requires a
new explicitly reviewed migration; arbitrary new scope transitions are not
supported by the preparation function.

## Preparation and activation procedure

The existing local development authority was activated on 2026-10-16; see the
[activation report](../codex/reports/phase_17hl_evaluation_policy_activation.md).
This does not authorize activation on any other authority or scope.

The offline preparation API is `governance.evaluation.prepare_evaluation_migration`. It opens its source
read-only, takes a SQLite snapshot into memory, checks schema/version/integrity,
compares the exact old policy and pricing catalog, rejects unresolved obligations
and full audit storage, calculates before/after owner and tenant quotas, and
rehearses configuration replacement plus an audit event followed by rollback.
It returns the complete old/new policies, catalog/history hashes, deterministic
event ID, evaluation time and remaining quotas. It does not open the provider
authority or assert that configured paths are the operator's correct authorities.

The binding JSON template is deliberately non-deployable operator input: replace
all placeholders with approved dedicated development scopes and existing shared
authority identifiers. Compute the provider policy hash locally from the exact
existing validated model. Do not substitute new quota keys, paths or prices.
Construct the overlay using `evaluation_policy(old_policy, binding)`; this retains
the base policy. No change to `.env` is part of offline preparation.

Activation on any authority requires explicit operator approval of the complete resulting
policy, allowlist, authority bindings, impact report and migration event. The
expected L1 base policy is `phase17hl-l1/2`; actual state must be verified at
activation, not inferred from that name. Stop on any mismatch. No approval for
activation, Attempt 3 or an experiment is provided by this document.

`governance.evaluation.apply_evaluation_migration` applies a prepared plan inside
a caller-owned `BEGIN IMMEDIATE` transaction. It validates the old policy, catalog,
schema, history, obligations and private backup before compare-and-swap and event
insertion. It never commits. Repeated activation fails closed without another
event. The caller owns quiescence, durable backup, authority-binding checks,
commit, configuration synchronization and recovery.

After approval, an operator performs the following controlled procedure:

1. Quiesce all application and L1 writers sharing governance and provider
   authorities. Confirm no unresolved governance or provider obligations and
   verify all consumers use the same paths/key/provider policy. Retain existing
   security authority, pricing, run evidence and approval replay storage.
2. Prepare the plan again against the actual existing authority using its exact
   old `QuotaPolicy`, unchanged `PricingCatalog`, approved `EvaluationBinding`,
   unchanged `AdmissionPolicy` and current UTC timestamp. Compare it with the
   approved policy/scopes; review current remaining quotas. Archive the plan
   privately. Negative remaining quotas mean admission remains denied.
3. Take an exclusive, new mode-0600 backup in a private mode-0700 directory using
   SQLite's backup API (not a raw copy of a running WAL database). Verify backup
   integrity, exact old configuration and history digest, hash the file, fsync
   file and parent directory. Keep writers stopped throughout this operation.
4. On the existing authority, use `BEGIN IMMEDIATE`. Recheck exact schema,
   `user_version=1`, integrity, old serialized policy, unchanged catalog,
   `history_digest`, absence of unresolved obligations and audit count <100000.
   Any mismatch rolls back and requires a fresh plan. Perform parameterized
   `UPDATE configuration SET policy=? WHERE singleton=1 AND policy=? AND catalog=?`
   with the new/old serialized model JSON and catalog; require exactly one changed
   row. Do not update any reservation. Insert the plan's deterministic event ID
   into `events` with the first approved scope, current timestamp and JSON action
   containing migration identity, complete old/new policy, scopes, quota impacts,
   history/catalog hashes, approval reference, backup path and backup hash.
   Commit both writes atomically; an existing event is a stop condition, never
   permission to replay or overwrite history.
5. Update each consumer's policy configuration to the exact approved resulting
   policy while keeping all authority paths and provider settings fixed. The old
   runtime's reserve/ready checks deliberately reject a changed configuration.
   Validate readiness and configuration agreement before reopening admissions.
   Do not consume an experiment approval or execute inference as a migration check.

On any transaction failure, roll back and retain backup/evidence for investigation.
Before reopening writers, rollback can restore the verified backup plus old
configuration while archiving the failed migrated copy and its audit evidence.
After ANY new admissions, never restore an older backup: that would erase usage.
Instead quiesce, reconcile obligations and approve a compensating policy change
with a new audit event, retaining every reservation, cost and prior event. Reverting
to lower quotas can immediately deny admission; it never removes consumed usage.

## Repeated experiments and future authentication

After activation, distinct experiment/job/step identities, run directories,
per-experiment reservations and signed approvals reuse the same policy and shared
authorities. Four requests at 25,000 input plus 3,000 output tokens reserve at most
100,000 input / 12,000 output per L1 run. Four such experiments fit 16 requests and
448,000 tokens before considering prior consumption, costs or unknown obligations.
This is capacity, not a guarantee of admission. Failed experiments do not change
policy; exhaustion requires waiting for the applicable natural window, reconciliation
of proven usage, or separately approved policy administration.

Entra authentication, RBAC and RSA approval validation/consumption remain mandatory
as currently implemented. A future design could authorize low-risk experiments
through a dedicated Entra application role and server-side standing grant bounded
by development scopes, approved model/operation, EUR 5 budget, duration and
per-experiment limits. Issue auditable unique execution IDs, revalidate identity
and grant revocation on every call, retain replay prevention, cancellation and
usage settlement, and deny production or high-risk operations. This would require
an explicit future security change and tests; it is not implemented here. Production
migrations and high-risk operations retain explicit operator approval controls.
