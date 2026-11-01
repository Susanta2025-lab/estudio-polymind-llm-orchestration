# Phase 17H-L — Reusable evaluation governance activation

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

**PASS — REUSABLE EVALUATION GOVERNANCE ACTIVATED**

Activation and immediate verification completed at **2026-10-16 07:31:28 UTC**
on the existing `master` branch. The operator explicitly authorized activation
and confirmed exclusive development/evaluation use of the existing owner/tenant
scope. No new identity, authority, or financial pool was created.

## A. Activation outcome

The existing authority retains base policy **`phase17hl-l1/2`** and now includes
exactly one **`polymind-evaluation/1`** overlay binding: internal tenant
`2b19ae2a…178b`, owner `40ef9362…97c1`. Both receive the approved limits. Other
owners, including other owners in this tenant, retain the base-policy limits.

The durable migration event is `59130a71-4023-50a5-8437-c7738bdd38dd`, migration
version `polymind-evaluation-migration/1`. It records the old/new policies, exact
scope and authority evidence, history/catalog hashes, quota snapshot, backup
identity/hash, operator authorization reference and applied timestamp. The event
action SHA-256 is
`4e37badfb7d29b96d7061a8cb0bfa0ee7d46758cea900c97d41864dba5fe0258`.

Private evidence is retained under:

`<PRIVATE_OPERATOR_DIRECTORY>/`

The directory is mode 0700 and its files are mode 0600. It contains the SQLite
backup, original `.env`, original readiness evidence, fresh preparation plan,
consumer inventory, source identity manifest, activation script, migration event,
verification results and file-hash inventory. Full identifiers and configuration
remain outside Git. The backup SHA-256 is
`7c978f36a8b9cefc2b630a0e3698c87de967271549df38add7a075f1509493e6`.

Backup creation used exclusive file creation and SQLite's supported backup API,
with file and directory fsync. Read-only verification confirmed integrity, exact
old policy/catalog and historical digest. Independent post-activation verification
confirmed all recorded evidence hashes, file permissions, original source inode
and device identities, authority integrity and event hash.

## B. Governance verification

Before mutation, read-only connections with `query_only=ON` confirmed that all
three authorities' table contents still exactly matched the reviewed evidence.
The persisted principal was independently rederived and matched the allowlist.
Policy, pricing, normalized OIDC settings, paths, shared quota key and provider
policy matched the existing configuration. Fresh preparation and in-memory
rollback both passed. There were no unexpected migration events, unresolved
UNKNOWN records, active obligations or provider calls.

Host process inspection found no running application, worker or evaluation
consumer. Remaining Node/Codex processes were identified; Docker had no running
containers. No process needed termination and no service was restarted. The
activation script repeated the process/container inventory and checked visible
open authority descriptors. It then acquired `BEGIN IMMEDIATE` locks on the
existing security, provider and governance authorities and rechecked their
contents. Security/provider locks remained held through governance commit and
configuration synchronization. Governance was immediately relocked after commit;
consumer absence and unchanged history were rechecked before completion.

| Constraint, for both approved owner and tenant | Previous base | Active evaluation | Remaining at verification |
| --- | ---: | ---: | ---: |
| Requests per rolling 86,400 seconds | 5 | 16 | 14 |
| Tokens per UTC day | 115,305 | 500,000 | 500,000 |
| Tokens per UTC month | 115,305 | 1,500,000 | 1,492,818 |
| Monthly EUR ceiling | 5 | 5 | 4.98409978880675719 |
| Simultaneously reserved tokens | 112,000 | 112,000 | 112,000 |
| Interactive concurrency | 1 | 1 | 1 |
| Background concurrency | 1 | 1 | 1 |

At verification, current rolling-window usage was **2 requests**; UTC-day usage
was **0 tokens / EUR 0**; UTC-month and lifetime usage were **7,182 tokens /
EUR 0.01590021119324281**. Both historical requests remained settled. Reserved
tokens/costs and unresolved obligations remained zero. Every reservation field
and every previous event remained unchanged; event count increased from 3 to 4.
The backup's historical digest remains
`8820c5af7ee41226c24a6d2b896b9a4447d42d4fa6f453d5da4cad03e013e424`.

Pricing remains **`phase17hl-pricing-eur-202610/1`**, EUR. Its digest remains
`dad37bc0f349cdfbea16e25cae028a0b5042e4e3e3daac4f141f9b566c5bc65e`.
Security and provider authority files are byte-for-byte unchanged. The provider
policy digest remains
`57da3d4bc57083653fce6d56f9767fe370c389ad6ad772c1f530507e245548f2`.
The existing shared quota key remains unchanged. Provider limits remain total
2 RPM / 30,000 TPM / concurrency 2; reserved interactive 1 RPM / 2,000 TPM /
1 slot; per-job 1 RPM / concurrency 1; background capacity 28,000 tokens/minute.
Read-only verification found no active or recent-minute provider calls.

Read-only admission arithmetic confirmed that a 25,000-input / 3,000-output
request fits current owner/tenant request, token, reservation, concurrency and
financial headroom, as well as unchanged provider capacity. Policy selection
also verified that an unlisted owner in the same tenant receives the base limits.
No real reservation, provider admission or inference call was made. Remaining
capacity is a timestamped observation, not authorization or a future guarantee.

## C. Implementation and configuration

Changes for this activation are limited to:

- `governance/evaluation.py`: added `apply_evaluation_migration`.
- `tests/unit/test_evaluation_activation.py`: five focused synthetic test cases.
- `docs/governance/evaluation-policy.md`: recorded local activation and documented
  the explicit apply helper and caller responsibilities.
- This activation report.
- Existing Git-ignored `.env`: changed only `GOVERNANCE_POLICY` to the exact stored
  serialization, after privately backing up the original file.

The apply helper runs inside the caller's writer transaction, validates exact
schema/version/integrity, prior policy, catalog digest, history digest, unresolved
obligations and audit capacity, and verifies the private backup. A parameterized
compare-and-swap changes exactly one configuration row; one migration event is
inserted in the same transaction. The helper never commits. Any mismatch raises
and the caller rolls back. Repeated activation is safely rejected with no second
event or policy mutation. The one-time private orchestration script owns locking,
backup durability, authority comparisons, commit, atomic `.env` replacement and
verification. It includes pre-admission recovery that archives the migrated
authority before backup restoration; this recovery was not needed or exercised
against the live authority.

The `.env` replacement preserved all other parsed settings and source lines.
Entra, RSA trust, pricing, security/provider paths, model generation configuration,
MiniLM and Chroma settings were preserved. Original execution packets and signed
configuration fingerprints were untouched. Future consumers must load the new
policy; stale policy configurations continue to fail closed.

Focused validation: **5 passed in 0.40 seconds**. Tests cover successful migration
with retained historical accounting, history mismatch, unsafe backup permissions,
rollback after event-insertion failure, and repeated activation without mutation.
The existing 42-test readiness evidence was reused; neither that suite nor the
full repository suite was rerun. Compilation of the changed Python module, test
and private activation script passed using an external bytecode-cache directory.
`git diff --check` passed. Independent read-only evidence verification passed.

Targeted self-review checked transaction boundaries, CAS, event insertion failure,
backup verification, exact-scope selection, configuration preservation and
recovery restrictions. The helper intentionally relies on its administrative
caller to acquire `BEGIN IMMEDIATE`, establish quiescence and validate external
authorities; it is not an application admission fallback. Separate pre-commit
review checked the task's files for sensitive identifiers, credentials, debug
output, accidental dependencies and unrelated modifications. No dependency,
provider boundary, API or generation contract changed.

## D. Safety accounting

| Operation | Count |
| --- | ---: |
| Azure inference calls | 0 |
| Azure infrastructure changes | 0 |
| L1 execution calls | 0 |
| RSA signing / approval consumption | 0 / 0 |
| Historical ledger entries modified | 0 |
| New reservations / financial obligations | 0 / 0 |
| Authorized governance configuration updates | 1 |
| Authorized migration events appended | 1 |
| Existing local `.env` policy updates | 1 |
| Git staging / commits / pushes | 0 / 0 / 0 |

`managed-prompt/3`, both 10,000-byte limits, 3,000-token completion ceiling,
four-call composition, 25,000-token input per call, 100,000/12,000 aggregate
reservations, 28,000-token context, Azure GPT-5.4 mini deployment, evidence/lineage
validation and Entra/RSA requirements remain unchanged. No AKS, Azure, L2 or
Attempt 3 operation occurred.

## E. Next step and repository state

The existing governance authority is **ready for independently authorized L1
Attempt 3 from the governance-capacity perspective**. The minimum next step is
separate authorization to prepare Attempt 3 using the active policy and the
existing Entra/RSA approval workflow. Old signed execution packets must not be
reused to authorize the changed configuration. Attempt 3 was neither prepared
nor executed here.

All unrelated tracked and untracked changes were preserved on `master`. Final
`git status --short` retains the pre-existing work and includes the activation
files above; `.env` remains ignored. `git diff --stat` reports only the pre-existing
17 tracked files, 386 insertions and 33 deletions, because this task's source,
test and documentation files are currently untracked. No staging, commit or push
occurred.
