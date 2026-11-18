# Phase 17H v5 financial reconciliation and second four-call readiness

Assessment: 7 November 2026 UTC, with fresh Azure reads at 09:08:54–09:09:04 UTC.
Branch `master`, HEAD `2b8a5ac73beb32d7febc53f77d0c3a459c8e3394`.
Scope follows the [task record](../prompts/phase_17h_v5_financial_reconciliation_and_second_four_call_readiness.md).

**BLOCKED — FINANCIAL RECONCILIATION REQUIRED.** The November conversion and
resource-specific meter quantities are independently reconfirmed. A concrete,
prospective catalog migration has been prepared and rehearsed entirely in RAM.
It requires new explicit financial authorization before any production authority
change. Tax treatment and supported incremental charge bounds also remain
unconfirmed. No migration, signing, approval consumption, reservation or paid
inference occurred. `charges_verified` remains false.

This advances the earlier [blocked preparation](phase_17h_v5_operator_preparation_signing_and_controlled_execution.md)
by identifying the supported numerical rates, the architecture's exact catalog
constraint, the safest prospective resolution, its precise review digest and
preservation/rollback requirements. Financial headroom alone is not approval.

## 1. Independent verification of current billing

Fresh read-only Azure queries reconfirmed the exact resource and deployment,
`gpt-5.4-mini` version `2026-03-17`, `GlobalStandard`, Spain Central and successful
provisioning. These resource bindings are retained in the proposed action and
its source-evidence hashes. No API key or identity token was needed for this
financial stage; Azure CLI's existing management authentication was used without
displaying its credentials.

Azure Consumption usageDetails, API `2024-08-01`, and Cost Management ActualCost,
API `2025-03-01`, were queried independently. Complete returned pages were
checked. Matching uses the exact resource ID, not a resource-name substring.
Both sources agree on date, input/output meters and quantities, with costs equal
within their returned numeric precision. The 7 November meters contain exactly
2,506 input and 2,130 output tokens, matching the failed historical call:

| Basis | Input per million | Output per million |
| --- | ---: | ---: |
| Recorded effective USD price | 0.75 | 4.50 |
| Recorded November EUR/USD conversion | 0.897706360249562 | 0.897706360249562 |
| Derived effective EUR price | 0.6732797701871715 | 4.039678621123029 |
| Existing approved EUR catalog | 0.659978880676 | 3.959873284055 |

The exchange-rate date is 1 November 2026. Usage details identify `OnDemand`,
unit `1M`, EUR billing currency, USD pricing currency and Spain Central global
input/output meter products. The current deployment query separately establishes
model version and SKU; meter product text alone is not a version contract.

This supports the prior diagnosis of changed currency conversion rather than
unexplained token quantities. No credit or cached-token discount is assumed.
The unchanged maximum usage gives:

```text
USD 0.129 × 0.897706360249562 = EUR 0.115804120472193498
Old catalog maximum = EUR 0.11351636747626
Difference = EUR 0.002287752995933498, approximately 2.01535%.
```

These are observed Azure usage/cost records and a projection, not final invoices
or a guarantee that a future tariff cannot change. Microsoft documents the
[conversion fields and reconciliation method](https://learn.microsoft.com/en-us/azure/cost-management-billing/automate/understand-usage-details-fields).
Its [billing-data documentation](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/review-subscription-billing)
identifies cost in billing currency as before credits or taxes. A tax-inclusive
budget conclusion therefore needs additional commercial evidence.

## 2. Existing financial architecture and choice of resolution

[`GovernanceLedger`](../../../governance/ledger.py) requires exact equality between
the supplied catalog and the singleton authority configuration. The constructor
and each new reservation fail closed on mismatch. Reservations retain their
catalog version and settled actual amounts. Settlement of unfinished work uses
the instantiated current catalog, making zero unsettled obligations essential
before switching catalogs. The existing seven reservations are all SETTLED.

[`Contract`](../../../tests/performance/foundry_budget.py) and RunGuard support
aggregate `fixed_cost` and `extra_cost` in the run calculation. The shared ledger
reserves and settles token prices; it does not separately reserve those aggregate
extras. Consequently:

| Alternative | Assessment |
| --- | --- |
| Change prices only in the launch configuration | Incompatible with the authority; correctly rejected |
| Reuse old prices and simply assert `charges_verified=true` | Does not resolve the verified commercial mismatch |
| Put all conversion uplift in `extra_cost` as an exception | Requires explicit reconciliation and operator bounds; leaves future token settlements at the superseded catalog. Less clear than prospective versioning |
| Replace or reprice historical reservation rows | Violates historical preservation and is unnecessary |
| New versioned current catalog, exact controlled migration, immutable history | Recommended prospective resolution |

No existing financial-exception bypass or generic catalog-migration entry point
was found. Existing migration modules cover particular policy changes and must
not be repurposed by changing their constants. The proposal describes a narrow
operator maintenance transaction following their backup, comparison, append-only
audit and rollback discipline. No application implementation was added or changed.
Activation remains a separately authorized operation, not an admission fallback.

## 3. Exact proposed catalog and approval binding

Proposed version: **`phase17hl-pricing-eur-202611/1`**. Prospective effective date:
**2026-11-07**. It contains the existing provider/deployment pair, currency EUR,
price unit 1,000,000, and these prices:

| Field | Proposed value |
| --- | ---: |
| Input EUR / million | 0.673279770188 |
| Output EUR / million, inclusive reasoning output | 4.039678621124 |
| Full four-call token maximum EUR | 0.115804120472288 |

The existing money validator permits at most 12 decimal places. Both observed
effective EUR rates are therefore rounded **upward**, never down, to that
precision using `ROUND_CEILING`. The resulting full-token allowance exceeds the
observed-rate projection by EUR 0.000000000000094502. It is a conservative
catalog-accounting rate, not a claim that the rounded value appears on an invoice.
The contract maximum and monthly owner/tenant ceilings remain EUR 5. No token,
request, admission, identity, generation or quota policy change is proposed.

| Review binding | SHA-256 |
| --- | --- |
| Existing catalog, canonical model serialization | `dad37bc0f349cdfbea16e25cae028a0b5042e4e3e3daac4f141f9b566c5bc65e` |
| Proposed approved catalog, canonical model serialization | `59c90a122e3db199848ae0817218bc4286bab80b22920a0916d8f5a54426dd37` |
| Complete financial migration proposal, revision 2 | `53939016e34ae7b6db8fc93d8929abd0a38e53182e982ce7e02d051dc35e1677` |

The complete proposal binds old/new catalog objects, resource/deployment/model/
version/SKU/endpoint, source-evidence hashes, unchanged policy hash, exact source
history hash, authority and backup destinations, scope, proposed unique audit
event, known historical billing variance, activation preconditions and rollback
rules. Its digest is SHA-256 of UTF-8 `json.dumps(proposal, sort_keys=True,
separators=(',', ':'))`. It is **not** a launch-configuration digest or RSA approval.

The proposed post-approval catalog payload includes `operator_approved=true`
because that is the future schema-required state being requested. Its enclosing
review document explicitly says `operator_authorization=PENDING`; pure schema
validation and this proposed effect convey no actual approval. No approved live
configuration or replacement authority has been created.

## 4. Proposed activation, preservation and rollback

The proposed action changes only the current catalog selection in the same
existing governance authority, and appends one migration event. Approval would
not authorize a new authority, a history rewrite, a policy update or inference.
Before activation:

1. Obtain explicit approval of the complete proposal digest above. Quiesce all
   governance writers and confirm no conflicting live launcher. Recheck the
   current generation, schema, policy/catalog, exact history, zero unsettled
   reservations and zero active shared admissions. Any mismatch stops activation.
2. Hold the governance write lock through `BEGIN IMMEDIATE`; preserve an exclusive
   0600 SQLite backup under the private 0700 review directory. Verify configuration
   and history in the backup, then fsync the file and directory before mutation.
   A backup of the database is not a replacement live authority.
3. Compare-and-swap only `configuration.catalog`, requiring the exact old catalog,
   unchanged policy and one affected row. Verify every historical reservation and
   existing event remains identical. Append one event retaining complete old/new
   catalogs, hashes, source evidence, authorization reference, backup identity and
   billing reconciliation. Commit only after integrity and preservation checks.
4. Independently verify the committed catalog and retained history. Future launch
   configurations must explicitly use the new catalog. Stale reservations fail
   the existing current-catalog check. Do not reuse old signed configurations.

Any failure before commit rolls the transaction back; the backup is retained for
review. After commit, no automatic restoration, deletion of the audit event or
database reset is proposed. A reversal requires separate authorization and a
compensating operation, particularly if any new reservation has occurred. The
operator must not restart stale writers as though a catalog transition were
transparent. No production write or durable production backup was performed
during preparation.

The old catalog survives in the original private configurations and would also
be embedded in the migration event. Historical catalog labels, amounts, calls,
provider evidence, replay records and consumed approvals remain unchanged.

## 5. Historical accounting and current capacity

Fresh read-only governance checks select `polymind-evaluation/1`, preserve the
stored policy/catalog and find seven settled reservations with no unresolved
obligation. Both current owner and tenant snapshots have:

| Capacity | Remaining |
| --- | ---: |
| Monthly tokens | 1,491,074 |
| Daily tokens | 495,364 |
| Rolling requests | 15 |
| Outstanding-token capacity | 112,000 |
| Local catalog-accounted EUR | 4.981094244984159248 |

The observed November resource charges total **EUR 0.01928677229678173** before
taxes/credits. The corresponding local November settlements total
**EUR 0.018905755015840752**, giving a known historical difference of
**EUR 0.000381017280940978**. This difference remains explicit reconciliation;
it is not silently assigned to the next call or written over historical amounts.

For this bounded future evaluation, the stricter pre-tax budget comparison uses
the lower of local recorded headroom and EUR 5 less observed November evaluation
charges: **EUR 4.98071322770321827**. After the proposed full-token allowance this
leaves **EUR 4.86490910723093027**, still before any historical/current taxes and
incremental fixed/extra charges. The shared ledger's numeric balance itself is
unchanged. This conservative review does not reserve capacity or formally approve
the tariff.

The earlier subscription-wide charges include unrelated infrastructure. Their
attribution to this evaluation cannot be assumed. A commercial question was
presented requesting applicable tax/VAT treatment, supported incremental
fixed/network/storage/monitoring cost bounds, and whether existing unrelated
infrastructure is excluded from the evaluation budget. No fresh answer has been
received at this stopped stage.

For a verified final contract, the operator must substantiate both the run bound
and monthly scope bound, including attributable charges and historical tax
exposure. Unknown charges are not assigned zero and an arbitrary contingency is
not represented as evidence. Aggregate extras also need explicit review because
their per-run guard coverage differs from shared-ledger token settlement. If
those facts or current prices change materially, revise the concrete financial
proposal before approval rather than silently extending it.

## 6. Rehearsal, tests and private artifacts

The read-only source was backed up to SQLite **`:memory:` only**. The rehearsal
performed the exact catalog compare-and-swap and one simulated appended event,
verified seven identical reservation rows and all identical pre-existing events,
confirmed the new catalog passes `_current_policy` and the old catalog is
rejected, checked integrity, and rolled back. The original configuration and
complete history digest were restored in RAM. Production database connections
used `mode=ro`, `query_only=ON` and read transactions; no production authority
constructor or reservation/settlement method was invoked.

Fresh focused validation used the existing installed environment and network
denial plugin, selecting:

```text
tests/unit/test_governance.py
tests/unit/test_governance_migration.py
tests/unit/test_evaluation_governance.py
tests/unit/test_foundry_preflight.py
```

Result: **110 passed in 3.49 seconds; zero network attempts**. These synthetic
financial/governance/contract tests corroborate existing behavior. They do not
claim that a new production catalog migration function exists or establish
commercial approval. The separate RAM rehearsal verifies the specific proposed
SQL effect and rollback; full activation/backup failure behavior must still be
checked in the authorized maintenance operation. No full engineering suite was
repeated and no networked inference test was run.

A new operator-owned private financial review directory contains **12 files**:
four fresh Azure observations, the active revision-2 proposal/digest/rehearsal/
preservation record, two preparation source helpers, test JUnit and inventory.
Directory/file modes are 0700/0600. The private receipt records its exact
destination. An earlier local draft remains outside the active review packet
and was never approved or applied; only the revision-2 digest above is presented
for approval. No token, API key, RSA private key, passphrase, launch approval or
replacement financial authority is in this package.

Before/after hashes confirm unchanged original v5 preparation, original failed
execution, existing authorities, public trust/replay and the preceding blocked
preparation packet. The generation digest still equals
`de9492c536c1435464e8d9e406cbd1491ea358bc45f817df72eb2ea2a0f69a71`.
There are no application, prompt, schema, validator or generation changes.

## 7. Remaining readiness and authorization stages

| Stage | Actual status |
| --- | --- |
| Independent financial reconciliation | Rates/quantities verified; exact prospective resolution prepared |
| Financial migration authorization | AWAITING explicit approval of the presented proposal |
| Catalog activation | NOT PERFORMED |
| Taxes/incremental commercial bounds | PENDING operator evidence |
| `charges_verified` | FALSE |
| Fresh task-2 identity and resource credential | DEFERRED until financial resolution, as instructed |
| Current task-2 quota/capacity, shared consumers, API-key deadline/window | NOT FINALIZED |
| RSA trust/permissions/replay | Existing infrastructure preserved; refresh remains required |
| Final v5 configuration/digest | NONE |
| Exact unsigned RSA bindings | NOT GENERATED |
| New signing authorization/signature verification | NOT REQUESTED / NOT PERFORMED |
| Separate paid-execution authorization | NOT REQUESTED |
| Second four-call live attempt | NOT PERFORMED; zero paid calls/retries |
| New reservation/consumption/settlement | NONE |
| Independent semantic quality review | PENDING |

Financial approval is an additional prerequisite; it grants neither RSA signing
nor paid execution. After the financial resolution, follow the established
identity/account correlation, resource-specific credential, quota/admission,
consumer, practical UTC-window, trust/replay and canonical finalization process.
Reuse the committed v5 deterministic plan and recheck its exact limits. Preserve
the separate signing and live-execution gates in full.

## 8. Review, repository disposition and conclusion

Implementation review checked precision, upward rounding, exact catalog equality,
unresolved-settlement hazards, historical preservation, prospective effective
date, stale-writer behavior, run extras versus ledger accounting, independent
Azure quantity matching and pre-tax versus tax-inclusive exposure. Pre-commit
review covers the two new Markdown deliverables, excluding private billing
records, operator identities, credentials and runtime artifacts. Documentation
links, whitespace, secret-pattern checks and `git diff --check` pass.

No application implementation changed; broad compilation, Docker/Kubernetes and
full-suite checks were not needed or performed. `git status --short --branch`
shows `master...origin/master`, nine pre-existing untracked Markdown files and
these two new deliverables. `git diff --stat` and `git diff --cached --stat` are
empty because all additions remain untracked and no tracked/staged file changed.
No staging, commit, push or remote mutation occurred.

**BLOCKED — FINANCIAL RECONCILIATION REQUIRED.** Request explicit authorization
for the exact versioned catalog migration proposal above and obtain the missing
commercial facts. Do not mark `charges_verified=true`, finalize approval bindings,
sign, consume an approval or initiate paid inference from this report.
