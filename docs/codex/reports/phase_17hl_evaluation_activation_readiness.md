# Phase 17H-L — Evaluation activation readiness

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

**BLOCKED — EXACT ACTIVATION PREREQUISITE**

The operator must establish that the candidate owner/tenant scope is exclusively
for development evaluation, or designate an existing dedicated evaluation scope
with trusted identity evidence. Local evidence cannot exclude production or
unrelated use. Do not approve the candidate allowlist on an assumption of isolation.
The actual-authority preparation and in-memory rollback both passed; no activation
occurred. A separate managed workload identity is not established by the available
local authority evidence and must not be silently substituted for the operator.

Assessment snapshot: **2026-10-16 06:42:02 UTC**, on existing `master`.

## A. Existing authority state

The exact existing paths are recorded in the private review artifact. Locally they
are under `<PRIVATE_AUTHORITY_DIRECTORY>/`:
`governance.sqlite`, `security.sqlite`, and `provider.sqlite`. All three are existing
mode-0600 files; `PRAGMA integrity_check` returns `ok`, `user_version=1`, and journal
mode is `delete`. Exact schemas match the implementation. No sidecars were present
in the before/after inventory; all three file hashes and sizes were unchanged.

All source connections used SQLite URI `mode=ro` and `PRAGMA query_only=ON`.
No authority constructor, readiness method, authorization method, or transaction
helper was invoked: those may write even when their names suggest validation.

The governance configuration contains exactly one row. The actual policy is
`phase17hl-l1/2`, without an evaluation overlay. Both owner and tenant limits are
5 requests per rolling 86,400 seconds, 115,305 daily and monthly tokens, EUR 5
monthly, 112,000 reserved tokens, interactive concurrency 1, and background
concurrency 1. The catalog is `phase17hl-pricing-eur-202610/1`, EUR, effective
2026-10-01, operator-approved. For the existing OpenAI-compatible deployment its
prices per million tokens are EUR 0.659978880676 input and EUR 3.959873284055 output.
The catalog is not changed.

| Authoritative accounting | Observed value |
| --- | ---: |
| Historical reservations / settled / released | 2 / 2 / 0 |
| Governance events | 3 |
| Outstanding or UNKNOWN obligations | 0 |
| Current rolling-window requests | 2 |
| Current UTC-day tokens / spending | 0 / EUR 0 |
| Current UTC-month and lifetime tokens | 7,182 |
| Current UTC-month and lifetime spending | EUR 0.01590021119324281 |
| Simultaneously reserved tokens / costs | 0 / EUR 0 |
| Active provider calls | 0 |

The first settled row retains `phase17hl-l1/1`: 1,845 input + 1,460 output =
3,305 tokens, EUR 0.00699907602956752. The second retains `phase17hl-l1/2`:
1,955 input + 1,922 output = 3,877 tokens, EUR 0.00890113516367529. These independently
queried values exactly match the supplied historical totals. Two provider records
have matching usage and job/step scopes; outcomes are `success` and `output_limit`,
both inactive. A failed experiment does not erase a settled inference charge.

The security authority contains one enabled user principal, epoch 0, with
`PUBLICATION_MANAGE`; one document, no grants or purge records, and 14 audit events.
Both launch packets use this principal's identical scope and these same three
authority paths. Tenant and owner were independently rederived using the existing
stable-ID algorithm from the security authority's stored issuer/tenant/subject;
both match. No JWT payload was accepted as unverified identity evidence. This is
persisted authorization evidence, not a fresh Entra token or cloud-role check.

The current `.env` authority paths, provider key, base policy, pricing and provider
policy match the second-attempt packet and actual authorities. OIDC settings match
after validation/default normalization; the initial raw JSON comparison differed
only in representation. The provider authority contains exactly one quota policy,
matching the packet byte serialization. Shared key: `epolymind-gpt-54-mini`.

| Provider restriction, unchanged | Value |
| --- | ---: |
| Total RPM / TPM / concurrency | 2 / 30,000 / 2 |
| Reserved interactive RPM / TPM / slots | 1 / 2,000 / 1 |
| Per-job RPM / concurrency | 1 / 1 |
| Background token capacity per minute | 28,000 |

No recent-minute calls or active calls consume provider headroom at this snapshot.
The provider-policy SHA-256 is
`57da3d4bc57083653fce6d56f9767fe370c389ad6ad772c1f530507e245548f2`.
This verifies local shared quota compatibility, not a fresh Azure quota inventory.

## B. Proposed evaluation identities

| Identity | Evidence and proposed disposition |
| --- | --- |
| Entra directory tenant | `afabeaf8…f3f3`, matching configured v2 issuer and persisted security identity |
| Internal PolyMind tenant | `2b19ae2a…178b`; derived scope, not the Entra tenant ID |
| Previous L1 owner | `40ef9362…97c1`; same in both packets, all governance rows and security principal |
| Authorized operator | Stored Entra subject `e-ud8…7yY`, user kind, enabled, `PUBLICATION_MANAGE`; API audience `5aa70f9d…105e` |
| Existing L1 development execution scope | The above tenant/owner pair, running `DOCUMENT_BACKGROUND` through the user principal; no distinct service principal in this authority |
| Separate Azure workload identity | Earlier Phase 16 report records a user-assigned managed identity, but omits identifiers and does not establish application federation; exact identity and scope cannot be verified here |

Candidate allowlist: **only** the above exact internal tenant/owner pair. It is
proposed for independent review, not approved. Full identifiers, original stored
identity, exact binding paths, configuration, provider policy, ledger evidence and
complete preparation output are in:

`/tmp/polymind-evaluation-readiness-20261016/review.json`

The artifact is mode **0600**, inside a mode **0700** directory. It contains no
access tokens, private keys or signed approvals. Preserve it privately before
activation; `/tmp` is not durable retention. The assessment harness is alongside
it as `assess.py` and is not an activation command.

Within the inspected authority, all reservation and provider rows use the L1
scope; no other registered owners or service principals exist. Development names,
a small local ledger and this absence do **not** prove that the same identities
are unused in another authority, application or production environment. The
allowance applies to every admitted request by the allowlisted scope, not merely
requests labelled as experiments. Independent operator confirmation is required.
Recommend a dedicated evaluation owner/tenant if exclusive use cannot be
established. Do not invent a new scope, map a managed identity to this user, create
an authority, or bypass existing accounting to obtain isolation. Any different
scope requires a fresh reviewed plan and explicit treatment of historical costs;
this candidate plan must not be reused to replenish a financial pool.

## C. Activation impact

The exact old identity is base `phase17hl-l1/2` with no overlay. The exact new
identity is **the same base `phase17hl-l1/2` plus `evaluation.version =
polymind-evaluation/1`** and the reviewed binding. It does not replace the base
version. Full old/new serialized policies are in the private plan.

Owner and tenant have identical observed impact:

| Constraint | Base allowance | Evaluation allowance | Base remaining | Evaluation remaining |
| --- | ---: | ---: | ---: | ---: |
| Rolling 24-hour requests | 5 | 16 | 3 | 14 |
| UTC-day tokens | 115,305 | 500,000 | 115,305 | 500,000 |
| UTC-month tokens | 115,305 | 1,500,000 | 108,123 | 1,492,818 |
| Reserved tokens | 112,000 | 112,000 | 112,000 | 112,000 |
| Monthly EUR | 5 | 5 | 4.98409978880675719 | 4.98409978880675719 |
| Interactive / background concurrency | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |

Capacity is time-specific, not an execution guarantee. With two requests still in
the rolling window, 14 remain: three complete four-request experiments plus two
requests, subject to all token, financial and provider restrictions. No experiment
is authorized by this arithmetic.

Selection is by exact trusted owner/tenant pair. Unlisted principals retain base
limits, including other owners within the same tenant. Historical rows are counted
without filtering by policy version, including released rolling-window requests
and unresolved obligations across periods. Preserve every reservation, settlement,
original policy identity and event. There is no independent evaluation money pool;
new usage also affects the shared tenant accounting of base-policy callers.
Consequently isolation confirmation matters even though base numeric limits stay
unchanged.

The overlay pins governance/provider paths, quota key and provider-policy digest.
Runtime and launcher pass these bindings; reserve checks exact current policy and
catalog, rejecting stale consumers. L1 additionally checks allowed scope before
approval consumption, then verifies authenticated principal equality. The security
path is retained and checked across local configuration and packets; it is not a
new cryptographic field in `EvaluationBinding`. These controls assume trusted
single-host administrators. They do not prevent an administrator replacing files
or code, or prove cross-host isolation. No production weakening is acceptable:
activation remains blocked until the scope-use prerequisite is resolved.

## D. Migration preparation

`prepare_evaluation_migration` ran against the actual existing governance path,
with its source connection wrapped to enforce `query_only`. It backed up only into
`:memory:`, compared exact schema, policy and catalog, calculated quotas, rehearsed
the configuration/event update in memory and rolled back. Results:
**dry_run=PASS, rollback=PASS, activation=PENDING**. No disk backup or new SQLite
authority was created. Network connections were disabled in the harness.

Migration identity: `polymind-evaluation-migration/1`. Candidate deterministic event:
`59130a71-4023-50a5-8437-c7738bdd38dd`.

- Catalog digest: `dad37bc0f349cdfbea16e25cae028a0b5042e4e3e3daac4f141f9b566c5bc65e`.
- History digest: `8820c5af7ee41226c24a6d2b896b9a4447d42d4fa6f453d5da4cad03e013e424`.

These are snapshot comparisons, not permission to apply later to changed state.
Use the existing [activation procedure](../../governance/evaluation-policy.md)
only after the scope decision and explicit activation authorization:

1. Quiesce all application, worker and L1 consumers of the three shared authorities.
   Confirm the complete consumer inventory, no active provider calls, and no
   unresolved governance obligations. Do not expire or release obligations by guess.
2. Repeat preparation using the approved exact scope and current timestamp. Recheck
   schema, integrity, exact old policy/catalog, authority paths, security identity,
   provider key/policy and history digest. Archive the current private plan.
3. While writers remain stopped, create a new exclusive mode-0600 backup in a
   mode-0700 directory using SQLite backup, with `O_EXCL`/no symlink following.
   Verify integrity, old configuration and history; hash and fsync file and parent.
   Do not copy a running WAL file or delete sidecars. No backup was made in this task.
4. On the existing authority use `BEGIN IMMEDIATE`; repeat exact comparisons and
   obligation checks, require event capacity below 100,000, and reject an existing
   migration event. Parameterized compare-and-swap of configuration must match
   old policy and catalog and change exactly one row. Insert one event atomically,
   containing migration identity, complete old/new policies, approved scopes,
   quota impacts/time, catalog/history hashes, approval reference, backup path/hash
   and retained security/provider binding evidence. Never update reservation rows.
   Any mismatch rolls back and requires new preparation; no automatic migration.
5. Synchronize all consumer policy configurations to the exact new serialization,
   retaining paths, pricing, OIDC, security authority, provider settings and replay
   storage. Old workers deliberately fail policy equality. Validate configuration
   agreement and integrity with read-only queries before reopening admissions.
   Check unchanged historical rows/digest excluding the newly added event, exactly
   one migration event, identical catalog, expected quotas and no new obligations.
   No inference or approval consumption is needed for verification.
6. Preserve original launch packets and fingerprints. Activation intentionally
   changes future configuration digests; old signed packets cannot authorize the
   new configuration. Any later experiment needs its own reviewed configuration
   and existing Entra/RSA approval process. Do not prepare Attempt 3 here.

Before **any new admissions**, rollback may restore the verified backup and old
consumer configuration while writers remain stopped; archive the migrated copy
and its audit evidence first. After **any new admission**, an old-backup restore
is prohibited because it would erase accounting. Quiesce and reconcile instead,
then obtain approval for a compensating policy migration with a new event,
preserving all requests, usage, costs and prior events. Lower limits may deny
further admission immediately. Do not use the add-only evaluation helper as an
unreviewed removal/update migration.

The local harness initially had a standard-library module-name collision and was
renamed before the successful preparation; this was not a policy or authority
failure. No activation-specific implementation defect was found. The earlier
**42 passed in 2.70 seconds** evidence is reused from the
[implementation report](phase_17hl_reusable_evaluation_governance.md); those tests,
JSON-limit tests and output-limit hardening tests were not rerun. No architectural
or implementation changes were made.

## E. Minimum operator decisions

1. Confirm exclusive development use of the exact candidate owner/tenant scope,
   including any other applications using it, or designate an existing dedicated
   evaluation scope with trusted binding evidence. Clarify any intended separate
   workload identity before including it; none is currently proposed.
2. Once isolation is resolved, explicitly authorize activation of the exact
   allowlist, shared bindings and current migration plan during coordinated
   quiescence. This is policy activation approval, not experiment approval.

No repeat EUR 5 spending approval, Azure deployment verification, or approval of
already established technical readiness is requested. No operator response is
needed to finish this preparation report; activation remains pending.

## F. Safety accounting and review

| Operation | Count |
| --- | ---: |
| Live database mutations | 0 |
| Azure inference calls | 0 |
| Azure infrastructure changes | 0 |
| RSA signing | 0 |
| Approval consumption | 0 |
| Git commits/pushes | 0 |

No Azure operations, identity creation, role changes, `.env` changes, authority
initialization, migration commit, reservations, settlements or Attempt 3 work
occurred. `managed-prompt/3`, both 10,000-byte limits, 3,000 completion tokens,
four-request workflow, Azure deployment, EUR 5 ceiling, Entra/RSA controls,
original audit records and configuration fingerprints remain unchanged.

Self-review checked the preparation helper's source-only read path, in-memory
rollback, authority compatibility, exact identity derivation, historical accounting
and production-isolation limits. Separate pre-commit review checked this report
for unmasked identity values, credentials, unsupported readiness claims and
unrelated edits. Private identifiers remain outside the repository. No tests,
builds or broad compilation were needed for this documentation-only preparation.

`git diff --check`: PASS. Final `git status --short` retains all pre-existing
tracked and untracked changes and adds only this report for this task. Branch
remains `master`; no staging, commit or push occurred. `git diff --stat` remains
17 tracked files changed, 386 insertions, 33 deletions; these are pre-existing
workspace changes, not changes made by this assessment. The new report is untracked
and therefore absent from that statistic.
