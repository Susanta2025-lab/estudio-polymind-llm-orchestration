# Phase 17H v5 complete financial readiness and remaining operator preparation

Date: 7 November 2026 UTC. Branch `master`. HEAD:
`2b8a5ac73beb32d7febc53f77d0c3a459c8e3394`.
The [task record](../prompts/phase_17h_v5_complete_financial_readiness_and_operator_preparation.md)
preserves the new financial decisions and remaining authorization boundaries.

**FINANCIAL READINESS: PASS under the explicitly approved assumptions and
unchanged four-call/public-endpoint scope.** The existing contract represents
the new catalog, 23% token VAT allowance, EUR 0.10 VAT-inclusive network
contingency and approved cost exclusions without an application change or any
new financial-authority mutation. The reviewed aggregate run allowance is
**EUR 0.242439068181288**, within the unchanged EUR 5 ceiling.

**OPERATOR PREPARATION: BLOCKED:** the fresh device-login attempt ended without
a usable access token. Shared-consumer exclusion and a practical confirmed UTC
window/API-key use deadline also remain pending. No final LaunchConfiguration
digest or unsigned approval binding exists for this stage. Signing and paid
execution remain separately unauthorized. No inference, reservation, approval
consumption or historical settlement change occurred.

## 1. What the operator resolved

The operator accepted the earlier
[catalog migration and commercial report](phase_17h_v5_authorized_catalog_migration_and_commercial_reconciliation.md)
and explicitly confirmed these financial treatments:

- Existing unrelated Azure infrastructure is excluded from incremental L1 cost
  only while the reviewed launcher does not invoke or modify it.
- Personal laptop CPU/disk/electricity, household internet and local retention
  are excluded personal operating resources, not incremental Azure charges.
- Use 23% VAT as a conservative allowance pending actual invoice treatment.
- Include EUR 0.10 **VAT-inclusive** provisional networking contingency for the
  existing workload and unchanged public route. It is a budgeting allowance,
  not an Azure network hard cap.

These decisions resolve the open operator cost-attribution and contingency
questions. The earlier report remains unchanged as historical evidence. This
assessment independently checks the resulting arithmetic, serialization,
contract behavior, current resource conditions and scope headroom. It does not
claim an independent invoice audit or human semantic review.

## 2. Existing contract representation and exact arithmetic

`Contract.fixed_cost` and `Contract.extra_cost` are existing aggregate run
allowances. No field, schema, provider, prompt or generation change is necessary.
The current authority catalog remains `phase17hl-pricing-eur-202611/1`, whose
canonical SHA-256 is
`59c90a122e3db199848ae0817218bc4286bab80b22920a0916d8f5a54426dd37`.
Its input/output rates remain EUR 0.673279770188 / EUR 4.039678621124 per million.

| Component | EUR |
| --- | ---: |
| 100,000 input + 12,000 inclusive output under current catalog | 0.115804120472288 |
| 23% VAT allowance on those tokens | 0.02663494770862624 |
| Operator-approved VAT-inclusive network contingency | 0.10 |
| Exact extras before serialization rounding | 0.12663494770862624 |
| `extra_cost`, rounded upward to supported 12 decimals | **0.126634947709** |
| `fixed_cost` under reviewed scope and exclusions | **0** |
| `Contract.cost(4)` | **0.242439068181288** |
| Unchanged `maximum` | **5** |

The network contingency already includes VAT and is not taxed a second time.
The upward rounding adds EUR 0.00000000000037376 to the combined allowance;
it does not enlarge the approved EUR 0.10 network component. Exact Decimal
arithmetic at precision 60 and a separate rational/Fraction calculation agree.
The existing `money` validator accepts the 12-decimal representation.

Canonical serialization of the reviewed financial `Contract` has SHA-256:

```text
c5f6338684146f44abe763c794b6b872a23930d65548eefd87c5e2196935699d
```

This is a financial contract fingerprint, **not** a finalized launch
configuration digest, signed approval or authorization to make calls. Its
`price_source` documents the current catalog, approved exclusions, VAT assumption,
contingency semantics and unresolved actual invoice treatment.

Existing `Contract.cost(n)` adds aggregate extras once for every cumulative
call-count check. The review checks `n=0..4`, `fits(4)=true`, and refusal of five
calls. The unchanged RunGuard uses that full contract while enforcing four
attempts, token limits, rate and concurrency limits. The shared governance ledger
continues reserving/settling token costs; it does not separately debit aggregate
VAT/network extras. Independent full-run financial comparison therefore includes
those extras and known historical billing differences before any paid launch.
This existing boundary is explicit rather than represented as an unimplemented
ledger feature.

## 3. Fresh evidence supporting the assumptions

Read-only Azure refresh completed **14:33:08–14:33:33 UTC**. It reconfirmed the
expected enabled subscription/tenant and named resource, deployment
`epolymind-gpt-54-mini`, base model `gpt-5.4-mini` version `2026-03-17`, Spain
Central, GlobalStandard and successful provisioning. The allocation remains
30 RPM / 30,000 TPM.

The public endpoint remains enabled, with no resource private endpoints,
customer-owned storage attachment or diagnostic export settings. Current
resource usage contains only the four known input/output meter entries from
the earlier two November calls, using the same USD prices/EUR conversion.
No new fixed, storage, monitoring or other resource-specific meter appeared.
The reviewed local launcher and provider path are unchanged; it does not invoke
or modify the separately billed registry, Redis, DNS, private-endpoint, database
or other application's monitoring infrastructure. Personal operating resources
are now explicitly excluded by the operator rather than assumed free.

Microsoft's [deployment comparison](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types)
continues identifying GlobalStandard as pay-per-token. The previous local
dependency/serializer evidence remains applicable: the launcher uses pinned CPU
embeddings, local files/SQLite/Chroma, disabled Chroma telemetry, no redirects or
environment proxy use, and bounded application payloads. No new telemetry-export
environment names are configured in the observed process. No unidentified
material extra charge was found within this unchanged scope.

The public [bandwidth reference](https://azure.microsoft.com/en-us/pricing/details/bandwidth/)
still supports the earlier scale comparison, but neither that reference nor
application byte limits is treated as an account-specific wire-meter cap. The
operator has expressly accepted that uncertainty through the provisional
EUR 0.10 VAT-inclusive allowance. Actual charges remain subject to later billing
reconciliation. A changed route/workload, newly enabled chargeable service or
material conflicting billing evidence invalidates this scoped readiness and
requires a stop and fresh review; the allowance is not silently expanded.

The previously linked active EUR/Portugal billing profile and empty invoice
query remain evidence of the account context, not proof of an actual VAT rate.
Use of 23% here is the explicit operator budgeting instruction. Neither zero VAT
nor a tax exemption is assumed.

## 4. Financial and governance comparison

The review used current read-only governance state and exact catalog/policy
comparison. Seven reservations remain settled, with no unsettled obligation or
new reservation. Both scopes select `polymind-evaluation/1` and retain:

| Metric | Owner and tenant |
| --- | ---: |
| Monthly tokens remaining | 1,491,074 |
| Daily tokens remaining | 495,364 |
| Rolling requests remaining | 15 |
| Outstanding-token capacity | 112,000 |
| Catalog-accounted EUR remaining | 4.981094244984159248 |

Conservative comparison also includes the observed EUR 0.01928677229678173
historical November resource charges with the 23% allowance. After that amount
and the complete proposed allowance, remaining monthly scope margin is
**EUR 4.7338382018936704721**. This is a review calculation, not a change to the
ledger balance or a capacity reservation.

The EUR 5 limit is retained as a ceiling. The reviewed allowance is substantially
smaller, but financial headroom alone is not the basis for passing: approval of
the assumptions, current scope evidence, contract representation and full
aggregate comparison are all present. Actual invoices and any realized network
charge must still be reconciled without rewriting old settlements.

## 5. Remaining operator preparation

Following the financial review, the established Entra device flow was initiated
with the existing pinned client/tenant/API scope. The preparation process keeps
credentials in protected memory and includes no signing, approval-consumption or
paid-execution command. It is designed to verify the existing OIDC signature,
issuer/audience, delegated purpose/scope, exact L1 role and registered
owner/tenant/`PUBLICATION_MANAGE` permission. A signed `oid` is verified against
the pinned JWKS before querying the exact Graph account's enabled status; no
unverified claim may supply the account identity.

At the final check around **15:02 UTC**, the device-flow attempt ended with no
usable access token; the sanitized process result is `STOPPED / DEVICE_LOGIN /
AssertionError`. The specific identity-provider error was not retained and is
not inferred from that category. No affirmative login-completion reply was
received. Resource-specific key acquisition therefore did not occur. No fresh
token or key-readiness PASS is claimed. Historical tokens remain expired and are
not reused; credentials were not written to artifacts. No replacement device
flow was automatically started after this prerequisite failure.

Fresh control-plane consumer observations show the PolyMind AKS cluster/node
pools stopped, no container instances and the other inventoried container
application stopped. Outside consumers and future starts cannot be excluded by
management data alone. Explicit shared-consumer exclusion remains pending.

A proposed 14:30–15:30 UTC window, target 14:50, and API-key use permission until
15:30 were presented for coordination only. No affirmative window/deadline or
consumer attestation has been received. No timestamps have been finalized, and
an elapsed proposed target must be recoordinated rather than silently extended.
The API-key use deadline will be an operator attestation, not an Azure expiry.

The private finalization helper is prepared but unexecuted. It requires those
affirmative facts, a fresh verified principal and at least a conservative
20-minute minimum runway; it rechecks current shared authorities, independent
RSA-3072 public trust, replay isolation, the pinned embedding tree and actual v5
planner/rendering before canonical configuration validation. It cannot produce
a valid configuration or binding from missing attestations. No encrypted private
key is opened during preparation.

## 6. Stage status and validation

| Stage | Actual status |
| --- | --- |
| Complete financial assessment | PASS for approved assumptions and unchanged scope |
| Existing contract representation | PASS; no application changes |
| Current catalog migration | Previously applied and preserved; no new authority write |
| Fresh operator authentication | STOPPED at device flow; no usable token |
| Resource-specific inference credential | Pending successful verified login |
| Azure deployment/quota | Verified 14:33 UTC; refresh required if stale before launch |
| Shared-consumer attestation | PENDING |
| API-key use deadline and practical UTC window | PENDING |
| Final v5 configuration/digest | NOT GENERATED |
| Exact unsigned RSA bindings | NOT GENERATED |
| RSA signing authorization/signature | NOT REQUESTED / NOT PERFORMED |
| Separate paid-execution authorization | NOT REQUESTED |
| Paid calls/retries/new reservations | 0 / 0 / 0 |
| Human semantic review | PENDING |

Fresh validation includes the Decimal/Fraction calculations, canonical Contract
validation and cumulative-cost/attempt assertions, read-only authority matching,
scope capacity and source-bound Azure checks. Two existing targeted financial
tests passed in **0.35 seconds**: aggregate-charge arithmetic and catalog
date/currency rejection. No full engineering suite, model inference, Docker
build or Kubernetes operation was needed or performed. The established v5
generation contract remains
`de9492c536c1435464e8d9e406cbd1491ea358bc45f817df72eb2ea2a0f69a71`.

A new private 0700 directory with **16 files**, each 0600, retains fresh Azure
observations, the reviewed financial contract, assessment and preparation helper
sources. Its per-file inventory also hashes the unchanged authorities and
historical private packages. The exact destination is recorded in the private
preservation receipt. Prior configurations, migration backup, financial history,
consumed approvals and evidence remain preserved. No signing key, token, API key,
passphrase or raw key response is in those artifacts.

Implementation review checked network VAT is not counted twice, aggregate
extras are counted once, rounding is conservative, operator exclusions match
actual dependencies, actual tax/cap limitations remain explicit and financial
approval is separate from execution. Pre-commit review covers only the two new
Markdown records; links, whitespace and secret-exclusion checks passed, as did
`git diff --check`. Final `git status --short --branch` shows
`master...origin/master`, thirteen pre-existing untracked Markdown records and
these two new deliverables. `git diff --stat` and `git diff --cached --stat` are
empty because no tracked/staged file changed. No staging, commit or push occurred.

Work can continue when the operator is ready for a new interactive login and
provides the pending consumer/window facts. Do not reuse the ended device-flow
code, request RSA signing before the final validated configuration/digest and
actual unsigned bindings exist, or infer paid permission from any financial
decision in this report.
