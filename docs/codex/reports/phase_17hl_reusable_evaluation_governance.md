# Phase 17H-L — Reusable evaluation governance

**PASS — REUSABLE EVALUATION POLICY IMPLEMENTED OFFLINE; ACTIVATION PENDING**

Completed on existing `master`, with existing tracked and untracked work retained.
This report concerns offline implementation and synthetic verification only. No
actual authority was opened or migrated, and no Attempt 3 packet was prepared.

## A. Policy architecture

`polymind-evaluation/1` is a separately versioned overlay in the existing
`QuotaPolicy`, selected by exact server-derived owner/tenant scope. It uses the
same reservations and events as production governance, without a parallel ledger.
The base policy identity and limits remain intact. Unlisted owners, including
owners in an evaluation tenant, retain the base policy. Operators must designate
dedicated development identities; an allowlisted identity must not also be used
for production. This is an authorization boundary based on identity, not an
inferred classification of prompt content.

| Allowance | Evaluation owner and tenant |
| --- | ---: |
| Requests per rolling 86,400 seconds | 16 |
| Tokens per UTC day | 500,000 |
| Tokens per UTC month | 1,500,000 |
| Cost per UTC month | EUR 5 |
| Simultaneously reserved tokens | 112,000 |
| Interactive concurrency | 1 |
| Background concurrency | 1 |

Selection changes applicable limits, not accounting membership. Every historical
reservation in the applicable owner/tenant scope remains counted, including rows
with a prior policy version. There is no per-policy financial pool. Settled and
released requests retain rolling-window counts; actual settled usage determines
token/cost spending. Unknown and unfinished obligations carry reserved usage and
cost across periods. No automatic forgiveness, replenishment, retry or policy
mutation was added.

The overlay pins the governance authority path, provider authority path, shared
provider quota key and provider-policy digest. This rejects accidental separate
authorities or altered admission settings before ledger creation. Existing shared
provider admission still controls RPM/TPM/concurrency/per-job limits. Policy and
catalog equality checks in each reservation reject stale workers or substitutions.
An administrator able to alter policies, files or code remains trusted, as in the
existing private single-host authority model. Distributed operation requires a
central authority architecture; this task does not claim cross-host SQLite safety.

## B. Implementation

Files modified by this task:

- `governance/ledger.py`: validated evaluation binding, fixed versioned limits,
  scope selection, shared-authority validation and selected-policy audit identity.
  Pre-existing uncommitted policy freshness checks were preserved.
- `security/runtime.py`: passes existing provider authority configuration for
  binding validation.
- `tests/performance/foundry_l1.py`: validates evaluation scope and authority
  binding in launch configuration and passes the binding inputs into the ledger.
  This file was already untracked and its existing launcher was retained.

Files added:

- `governance/evaluation.py`: policy construction and read-only migration
  preparation with quota impacts and in-memory configuration/event rollback.
- `tests/unit/test_evaluation_governance.py`: synthetic policy, isolation,
  accounting, concurrency, migration and L1 configuration tests.
- `docs/governance/evaluation-binding.template.json`: placeholder-only binding.
- `docs/governance/evaluation-policy.md`: architecture, activation and rollback
  procedure, repeated-experiment workflow and future authentication recommendation.
- `docs/codex/prompts/phase_17hl_reusable_evaluation_governance.md`: clean task record.
- This report.

Existing `governance/migration.py` was inspected and reused for its history digest;
its prior migration implementation was not edited. No schema change is necessary.
Absent an overlay, policy serialization omits the new field, preserving legacy
configuration JSON and signed configuration inputs. Enabling an overlay changes
the configuration digest intentionally and requires new operator approval.

No generation code was changed. `managed-prompt/3`, both independent 10,000-byte
ceilings, 3,000 completion tokens, 25,000 input reservation, four L1 requests,
100,000/12,000 aggregate reservations, 28,000 context, deployment selection,
MiniLM/Chroma and evidence/qualification/contradiction/lineage logic remain as found.
Entra verification, RBAC, RSA verification and approval consumption are unchanged.

## C. Validation

Final focused run: **42 passed in 2.70 seconds**, no skips or failures:

```text
python -m pytest tests/unit/test_evaluation_governance.py \
  tests/unit/test_governance.py tests/unit/test_governance_migration.py -q
```

The run used `PYTHONPATH=/tmp/polymind-evaluation-offline:.` with a temporary
`sitecustomize.py` replacing socket connect/connect_ex, create_connection and DNS
resolution with failures before pytest imports. New evaluation tests additionally
block socket access with an autouse fixture. All authority paths were temporary
synthetic test paths. No RSA-signing fixtures or live launcher calls were used.

Coverage verifies exact owner/tenant selection; production default isolation;
four four-request experiments under one policy; rolling-window boundary at
86,400 seconds; daily and monthly token exhaustion; EUR 5 independently exhausting
before tokens; actual rather than reserved settled costs; shared tenant spending
across two authorized owners; unknown/unsettled obligations across months;
concurrent atomic reservations; shared reserved-token capacity across workload
classes; retained events; shared provider throughput; forged scopes; path/key/
provider-policy substitution; policy version mismatch; EUR-only enforcement;
legacy serialization; L1 configuration limits and unauthorized scope rejection.

Synthetic installation tests retain historical rows and their original policy
identities, reject stale workers and show that four old requests plus twelve new
requests exhaust the same rolling allowance. The existing migration tests cover
exclusive backup, idempotence, concurrent migration, transactional rollback and
rejection of changed catalog/schema/policy/unsettled obligations. New preparation
tests prove byte-for-byte preservation of the source SQLite file and rollback of
in-memory policy and event changes.

Additional validation:

- `git diff --check`: PASS.
- `PYTHONPYCACHEPREFIX=/tmp/polymind-evaluation-offline/pycache python -m compileall -q governance security/runtime.py tests/performance/foundry_l1.py tests/unit/test_evaluation_governance.py`: PASS.
- Self-review inspected policy serialization, all ledger construction consumers,
  provider/financial boundaries, history selection and migration error handling.
  Resource cleanup on preparation errors and decimal precision were tightened
  before final validation.
- Separate pre-commit review found no introduced secrets, credentials, real `.env`
  content, machine-specific deployment paths, debug statements, generated database
  artifacts, dependencies, dead code or unrelated edits. Template paths are
  intentional operator placeholders. Existing unrelated changes were retained.

No unrelated suites or prior generation-failure investigations were rerun. Docker,
Helm and full-repository compilation were not needed for these Python policy-only
changes; no container, dependency or deployment configuration changed. No applicable
Python lint command was found in the inspected project build configuration.

## D. Migration readiness

Prepared migration identity: `polymind-evaluation-migration/1`. Expected existing
L1 base policy from the repository's migration contract: `phase17hl-l1/2` (5
requests and 115,305 daily/monthly tokens). Actual live state was deliberately not
queried and must be compared exactly at future activation. The target preserves
that base policy and adds `polymind-evaluation/1` for approved scopes only.

Dry-run outcome: **PASS on synthetic authorities; activation PENDING**. For a
synthetic settled request using 3,305 tokens and EUR 0.003305, preparation produced:

| Remaining quota | Before | Evaluation target |
| --- | ---: | ---: |
| Rolling requests | 4 | 15 |
| Daily tokens | 112,000 | 496,695 |
| Monthly tokens | 112,000 | 1,496,695 |
| Reserved tokens | 112,000 | 112,000 |
| Monthly EUR | 4.996695 | 4.996695 |

These are test figures, not a claim about actual remaining live allowances. The
plan records full old/new policy, catalog hash, history hash, scope-specific quota
impacts, timestamp and deterministic migration event ID. It rehearses policy and
audit-event writes in memory and rolls back, leaving the source unchanged. The
operator must rerun preparation against a quiesced, approved authority later.

The precise future activation procedure is in
[Evaluation policy](../../governance/evaluation-policy.md#preparation-and-activation-procedure).
It requires explicit approval of policy/scopes/bindings and a current impact plan;
quiescing shared consumers; reconciliation of outstanding obligations; a private,
exclusive SQLite backup with integrity/hash/fsync checks; exact compare-and-swap
under `BEGIN IMMEDIATE`; an atomic migration audit event with backup and approval
references; and coordinated consumer configuration/readiness checks. No live
activation command was supplied or executed by this task.

Rollback before new admissions can restore the verified backup while retaining
migration evidence. After new admissions, rollback must be a compensating policy
change preserving all rows; restoring an old backup would erase consumption and
is explicitly prohibited. Existing audit retention limits remain enforced.

Minimum next operator action: review and approve the exact dedicated development
scope allowlist and existing shared-authority bindings, together with the policy
and migration procedure. Activation and any later experiment are separate actions;
this result grants neither authorization nor an Attempt 3 approval.

## E. Future workflow

After activation, additional approved development experiments use distinct run,
job and step identities and per-experiment budgets against the same authority.
Failed runs settle known usage or retain unknown obligations. They do not trigger
a new migration. Four maximal L1 experiments require 16 requests and 448,000 tokens
before prior spending, provider headroom and costs; admission still checks every
constraint. Exhaustion never creates a fresh budget automatically.

Individual experiment approval authorizes a bounded execution. Policy approval
changes standing allowances or authorized scopes. They are separate controls.
Current RSA signing requirements remain mandatory. The design recommendation is
a future revocable Entra role plus a server-side standing development grant,
limited by scope, duration, model/operation, cost and experiment size, with unique
execution IDs, replay protection, cancellation and per-call revalidation. This is
not implemented; production migrations and high-risk operations retain explicit
approval controls.

## F. Safety and repository state

| Operation | Count |
| --- | ---: |
| Azure inference calls | 0 |
| Azure infrastructure changes | 0 |
| Live database mutations | 0 |
| RSA signing | 0 |
| Approval consumption | 0 |
| Git commits/pushes | 0 |

No `.env`, replay markers, signed packets, original evidence or actual policy
records were changed. No staging, branch switch or remote operation occurred.

`git status --short` was inspected before and after work: branch remains `master`,
with pre-existing modifications and untracked files retained. Task modifications
are enumerated in section B. `git diff --stat` reports **17 tracked files changed,
386 insertions, 33 deletions**, including the user's substantial pre-existing work;
it excludes untracked files, including the new policy module, docs/tests and the
already-untracked launcher. This is the full workspace statistic, not a claim
that all those changes belong to this task. All work remains uncommitted.
