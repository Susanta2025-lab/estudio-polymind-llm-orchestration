# Phase 17H v5 authorized catalog migration and commercial reconciliation

Date: 7 November 2026 UTC. Branch: `master`. HEAD remains
`2b8a5ac73beb32d7febc53f77d0c3a459c8e3394`. The
[operator task record](../prompts/phase_17h_v5_authorized_catalog_migration_and_commercial_reconciliation.md)
preserves the explicit authorization boundary.

**CATALOG MIGRATION: PASS — independently verified.** The exact authorized
prospective catalog transition was applied to the existing governance authority.
The EUR 5 limits, seven historical settlements, their pricing-version labels,
nine existing events, old evidence and consumed approvals were preserved. Exactly
one migration event was appended. A durable exclusive backup retains the prior
catalog and complete history.

**BLOCKED — FINANCIAL RECONCILIATION REQUIRED** remains the overall preparation
decision. The 23% VAT budgeting instruction has been incorporated into the cost
assessment, and Azure's canonical active EUR/Portugal billing profile is linked
to the usage records. Networking and local operating-cost attribution still need
supported bounds or explicit reviewed assumptions. Independent commercial review
is PENDING. `charges_verified=false`; configuration finalization, signing,
approval consumption and paid inference did not occur.

## 1. Exact authorization and pre-migration safety

The operator explicitly authorized only the
[previously prepared versioned catalog proposal](phase_17h_v5_financial_reconciliation_and_second_four_call_readiness.md).
Its approved canonical SHA-256 was independently recomputed as:

```text
53939016e34ae7b6db8fc93d8929abd0a38e53182e982ce7e02d051dc35e1677
```

This uses the previously documented UTF-8 sorted compact JSON serialization.
The separate raw-file SHA-256 is
`2116994396a48650f9a7a81231f2db1bb9bcdc9395ff7d15178ddb1f0e92c4b8`;
it also matches the preserved review artifact. No proposal content or historical
approval status field was rewritten. The actual new authorization is recorded
separately in the migration event and execution receipt.

Before applying, checks reconfirmed the expected schema/user version/integrity,
source catalog, unchanged policy, exact source history, seven settled reservations,
zero unsettled obligations and zero active shared admissions. There were no
conflicting live launchers, other processes holding the authority files, active
repository Python runtimes or running Docker containers. No service was stopped
or started. These are scoped single-host observations, not a distributed lock.
The maintenance operation additionally held exclusive SQLite write transactions
on the provider-admission and governance authorities during the change, preventing
concurrent admission/configuration changes while checking and committing.

The only authority data mutation was the governance current-catalog selection
and one appended migration event. Provider admission was locked and read without
changing its data. Security, quota policy, replay records and audit packages were
verified unchanged. Neither a fresh runtime identity token nor an inference key
was acquired for this administrative operation.

## 2. Applied catalog and retained financial limits

| Binding | Result |
| --- | --- |
| Previous catalog | `phase17hl-pricing-eur-202610/1`, retained in backup, historical records and audit event |
| New current catalog | `phase17hl-pricing-eur-202611/1` |
| Prospective effective date | 2026-11-07 |
| Provider / served deployment | `openai_compatible` / `epolymind-gpt-54-mini` |
| Currency / unit | EUR / 1,000,000 tokens |
| Input rate | EUR 0.673279770188 |
| Output rate, inclusive reasoning-output contract | EUR 4.039678621124 |
| Maximum four-call token calculation | EUR 0.115804120472288 |
| Contract and owner/tenant monthly ceilings | EUR 5, unchanged |

Both approved rates use the previously reviewed upward rounding to 12 decimal
places. No price was silently substituted after approval. The new catalog's
canonical model-serialization SHA-256 is:

```text
59c90a122e3db199848ae0817218bc4286bab80b22920a0916d8f5a54426dd37
```

The existing policy still selects `polymind-evaluation/1` for the registered
scope. Request/token limits, monthly cost limits, owner/tenant scope and admission
policy were not modified. No reservation, provider usage or settlement was added.

## 3. Backup, transaction and independent verification

The backup was created at the proposal's exact approved private destination using
exclusive creation, 0600 permissions and no symlink traversal. SQLite's backup
API copied committed data from a separate read-only source while the governance
writer lock was held. Its schema, configuration and history were reopened and
verified; file and directory were fsynced before the catalog mutation.

Backup SHA-256:

```text
0dd1263c71d2eb394a889695efea1705b6a83768bfd786cdafd36d9b61b7e210
```

The transaction used `BEGIN IMMEDIATE`, full synchronous durability and an exact
compare-and-swap on old catalog plus unchanged policy, requiring one affected
configuration row. It preserved every reservation and old event, then inserted
the proposal's unique event **`70a36ec6-4f77-486e-9381-8c01202f51bc`**. That event
retains full old/new catalog objects, proposal/source/policy/history hashes,
authorization scope, backup identity, known prior billing variance, unchanged
EUR 5 ceiling and `charges_verified=false`. It conveys no signing or inference
permission. No automatic retry, replacement event or post-commit rollback ran.

The maintenance receipt records approximately 11:40 UTC. A separate verifier
confirmed the committed effect at **11:42:16 UTC**, using independently opened
read-only handles for the current authority and backup. It established:

- All **seven** reservation rows, including amounts, usage, states and old catalog
  versions, are identical to the backup.
- All **nine** prior events are identical, with exactly **ten** events afterward.
- The only configuration difference is the approved catalog selection; the policy
  hash remains `9c9fb0c8683748d906c08ee68d3a0f0d11cc12f53c503a294bee165b666c2ee9`.
- Filtering out the new event reproduces the approved pre-migration history hash
  `bd9a8281060b5c76c1cf3515448f3c0695f9c1febbf365166ca763a09053fb6b`.
- The current catalog passes the existing `_current_policy` check; the previous
  catalog is rejected for new reservations. No production ledger constructor or
  reservation was used to test that check.
- Original proposal/source artifacts, previous preparation and failed execution
  evidence, independent public trust and replay records remain byte-identical.

This is independent automated verification of the maintenance effect in a
separate process. It is not an independent human commercial or semantic review.

## 4. Fresh Azure billing, profile and configuration findings

Fresh read-only management/billing observations were obtained around
**11:45–11:46 UTC**. The target remains resource `epolymind-foundry-dev-susanta`,
deployment `epolymind-gpt-54-mini`, model `gpt-5.4-mini` version `2026-03-17`,
Spain Central, GlobalStandard, provisioned successfully. No deployment, resource,
billing-account, tax setting, logging destination or network setting was changed.

The active billing account is an Individual Microsoft Customer Agreement account.
Following canonical account/profile IDs returned by Azure resolved the initial
lookup failure. Its single active profile is linked to the exact usage profile,
with **EUR currency and Portugal billing country**. The profile response did not
return tax exemption/registration treatment. The canonical invoice query for
1 October through 7 November returned zero invoices; it does not establish that
no invoice exists outside that query or that VAT is zero. Personal billing
addresses, invoice download URLs and raw credential responses were not retained.

The explicitly instructed **23% VAT remains a conservative budgeting assumption**,
not an assertion of actual invoice treatment. The missing invoice treatment
does not override that authorized budgeting assumption or require pretending
that an actual VAT rate has been independently established.

Fresh complete usage-detail pages still contain only the known input/output
meter pairs for 1 and 7 November at the named Foundry resource, with unchanged
November conversion. Their total is **EUR 0.01928677229678173** before taxes and
credits. Local historical November settlements remain
**EUR 0.018905755015840752**. The known **EUR 0.000381017280940978** difference
was retained as reconciliation metadata and was not written over historical
settlements. ActualCost is not a tax-inclusive invoice; see Microsoft's
[billing-data guidance](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/review-subscription-billing).

## 5. Defensible incremental-cost assessment

| Category | Current evidence and supported conclusion |
| --- | --- |
| Base model hosting/fixed provider capacity | The exact deployment is GlobalStandard with the unmodified base model; fresh resource meters contain only token charges. Microsoft's [deployment comparison](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types) identifies this SKU as pay-per-token. No separate hourly/provisioned base-model charge is identified for this configuration. This finding depends on keeping the reviewed deployment and route. |
| Cloud storage | The approved launcher uses local object files, SQLite, Chroma and pinned local CPU embeddings. Its private storage is a WSL ext4 filesystem. No Azure Blob/remote storage service participates in this L1 path. This supports no newly attributable Azure storage service operation, without assigning zero monetary cost to the operator's local disk. |
| Resource diagnostic exports | The fresh resource diagnostic-settings list is empty. There is no configured customer Log Analytics/storage/Event Hub export from this resource. Chroma telemetry is disabled in source and no telemetry-export environment names are configured in the observed process. This supports no new export-sink usage under current configuration, not a guarantee against future configuration changes. |
| Network | Public endpoint access is enabled; there are no resource private-endpoint connections. The launcher disables environment proxies and redirects. These facts avoid assuming use of the separately billed existing private endpoint, but do not establish an account-specific egress tariff or a hard billable-traffic bound. Networking is not assigned zero. |
| Local operations | CPU inference for embeddings, local storage, ISP/electricity and retention attribution remain operator commercial facts. No monetary zero is assumed. |

The current subscription usage evidence separately identifies existing registry,
Redis, DNS, public-IP/private-endpoint networking, PostgreSQL, load-balancer and
other application's monitoring resources. The approved local L1 composition does
not invoke them or start/deploy infrastructure. Their separately identified
recurring baseline is excluded from **incremental inference cost** on that
combined billing-and-dependency evidence. They remain part of the Azure
subscription bill; no subscription-wide zero-cost claim or baseline refund is
made. This exclusion does not remove potentially attributable network usage.

A narrow offline serializer probe captured the real provider payload before any
transport, using the unchanged domain/provider schemas. Fixed payload overhead
was checked with empty/plain/escaped/Unicode string witnesses. Under the existing
24,800-byte complete input envelope, the four admitted HTTP request bodies total
at most **97,231 bytes**. The three synthesis response limits plus Q&A response
limit total **158,768 bytes**, for **255,999 application-body bytes** combined.
This is an application serializer/client-response budget, not a guaranteed Azure
wire-byte meter bound: headers, TLS, read-ahead and retransmissions are separate.
There was no provider call or substitution of accepted live output.

For context, Microsoft's [public bandwidth reference](https://azure.microsoft.com/en-us/pricing/details/bandwidth/)
lists USD 0.087/GB for Europe's first paid internet-egress tier. Using the observed
November conversion, one GB would be EUR 0.078100453341711894, or
EUR 0.09606355761030562962 with the 23% assumption. No free allowance is relied
on. This is a **conditional reference calculation**, not verification of this
account's network tariff, a measured wire-traffic cap or approval of an arbitrary
one-GB contingency. A supported account-specific bound, or a separately reviewed
positive contingency with explicit assumptions, remains necessary.

## 6. VAT-inclusive component arithmetic and headroom

Decimal arithmetic at precision 60 gives:

| Component | EUR |
| --- | ---: |
| New catalog full-token maximum | 0.115804120472288 |
| 23% VAT allowance on those tokens | 0.02663494770862624 |
| Tokens plus assumed VAT | **0.14243906818091424** |
| Prior observed November resource usage plus new maximum, both with assumed VAT | 0.1661617981059557679 |
| EUR 5 monthly remainder after that component calculation | 4.8338382018940442321 |

These are component bounds under the explicit VAT assumption. They are not a
complete approved all-in run bound while network/local extras remain unresolved.
The available arithmetic margin does not authorize unspecified charges.

The independently read governance balances are unchanged in both scopes:
1,491,074 monthly tokens, 495,364 daily tokens, 15 rolling request slots, 112,000
outstanding-token capacity and EUR 4.981094244984159248 in catalog-accounted
headroom. Seven reservations remain settled; there is no new reservation or
usage. That ledger balance has not been rewritten to represent Azure invoice
taxes or known historical conversion differences.

Existing run contracts include aggregate `fixed_cost`/`extra_cost`; the shared
ledger accounts token prices. A future reviewed configuration must explicitly
bound all attributable extras and check their full aggregate against both the
run ceiling and conservative scope headroom. The original pending candidate
still contains the historical catalog and unverified zeros; it was deliberately
preserved. It must not be treated as a newly launchable configuration after this
catalog transition. A fresh reviewed configuration is required later.

## 7. Validation and evidence preservation

The one-off maintenance helper is outside application code. Before activation,
**nine isolated tests passed in 0.211 seconds**: exact effect/history preservation,
changed-history refusal, durable backup verification and no overwrite, duplicate
event refusal, rollback after injected post-update failure, schema drift refusal,
unsettled-work refusal, wrong-source refusal and wrong-target-digest refusal.
Those tests used disposable synthetic authorities; the production migration ran
once successfully under the exact user approval, with no automatic retry.
The maintenance source SHA-256 recorded in the event is
`60c599d648289461f4fb1e9f1f008d456ea088fa298bd82cc9c38b53bfa8aa55`.

The separate verification process passed all current/backup/history/public-trust/
replay preservation comparisons. Current relevant source files match committed
HEAD, and the generation contract remains
`de9492c536c1435464e8d9e406cbd1491ea358bc45f817df72eb2ea2a0f69a71`.
The earlier 110-test financial/governance selection remains historical evidence;
it was not rerun or represented as fresh coverage. The full engineering suite,
Docker build and Kubernetes checks were not repeated. No dependency was added.

A new private execution/commercial packet contains **26 files**, including the
applied receipt, independent verification, tested maintenance source/tests,
sanitized Azure/billing-profile observations, local configuration evidence and
commercial assessment. Directory/file modes are 0700/0600, with a per-file hash
inventory. The backup remains at its original approved destination and was not
copied into a replacement authority. Original review packages remain unchanged;
the existing financial review directory gained only its authorized backup and
applied receipt. Tokens, API keys, private signing keys and passphrases are absent.

Implementation self-review checked exact authorization, canonical/raw checksum
distinction, private paths and exclusive backup, lock ordering, source equality,
unsettled-work refusal, CAS rowcount, append-only audit, rollback-before-commit,
stale-catalog rejection, preservation comparisons and commercial assumptions.
Pre-commit review covers the two new Markdown records, including secret/private
identity exclusion, links, figures, whitespace, accidental artifacts and scope.
No application, schema, prompt, provider, validator or public API changed.

Final `git status --short --branch` shows `master...origin/master`, eleven
pre-existing untracked Markdown records and these two new deliverables.
`git diff --stat` and `git diff --cached --stat` remain empty. Documentation
checks and `git diff --check` pass. No staging, commit, push or remote mutation
occurred.

## 8. Remaining blockers and stopping point

The approved catalog discrepancy is resolved prospectively. Before complete
financial readiness, the remaining operator/reviewer inputs are:

1. A supported account-specific incremental network-charge bound, or explicit
   approval of a positive contingency and its assumptions. Application-body
   limits and a generic public tariff are useful evidence but not a completed
   account-specific charge contract.
2. Confirmation of whether local CPU/disk/retention/ISP/electricity expenses are
   excluded from the incremental evaluation budget; otherwise supported bounds
   for those attributable expenses. Existing unrelated Azure baseline costs have
   already been separated using current resource billing and actual dependencies.
3. Independent commercial review of the complete aggregate calculation, VAT
   assumption, exclusions and final fixed/extra limits. This review is PENDING;
   automated migration verification does not substitute for it.

After those financial conditions are resolved, the established fresh identity
and permissions/account linkage, resource key and attested use deadline, current
quota/shared-consumer admission, scope headroom, future practical UTC window,
trust/replay checks and new canonical v5 configuration/bindings remain necessary.
No old token/window or consumer attestation was renewed by this migration.

As explicitly requested, work stops after migration verification and commercial
findings. **No RSA signing was requested or performed, no approval was consumed,
and no paid Azure inference occurred.** Human semantic review remains PENDING;
no second four-call live attempt has begun.
