# Phase 17H v5 operator preparation, signing and controlled execution

Assessment: 7 November 2026 UTC. Branch: `master`. Starting and final HEAD:
`2b8a5ac73beb32d7febc53f77d0c3a459c8e3394`.

**OPERATOR PREPARATION: BLOCKED.** Fresh resource-specific Azure billing evidence
establishes a different EUR conversion from the pinned approved catalog. The
task explicitly requires stopping on a material financial discrepancy and forbids
silently replacing that catalog. Configuration finalization, unsigned approval
bindings and both authorization gates were therefore not reached. No RSA signing,
approval consumption, reservation or paid inference occurred.

The discrepancy is material to the exact commercial verification required for
`charges_verified=true`; it is not a lack of numeric headroom or a claim that the
project is about to exceed EUR 5. Neither the catalog nor the financial ceiling,
historical settlements or authority state was changed.

## 1. Starting evidence and integrity

The six requested reports/runbooks were inspected, including the untracked
[v5 readiness reassessment](phase_17h_v5_four_call_readiness_reassessment.md),
the [R0/R1 report](phase_17h_r0_r1_evidence_provenance_hardening.md),
[root-cause report](phase_17h_live_invalid_qualification_source_root_cause.md),
[earlier controlled execution](phase_17h_final_approval_signing_and_controlled_execution.md),
[Foundry validation](../../evaluation/phase_17h_foundry_validation.md) and
[operator approval procedure](../../evaluation/phase_17hl_operator_approval.md).
The [task record](../prompts/phase_17h_v5_operator_preparation_signing_and_controlled_execution.md)
preserves this task's scope and explicit gates.

The existing private v5 preparation package is present and remains unchanged.
The current `generation_contract_digest()` returns:

```text
de9492c536c1435464e8d9e406cbd1491ea358bc45f817df72eb2ea2a0f69a71
```

All 12 inventoried generation source files match committed HEAD byte-for-byte.
The historical 1,872-test R0/R1 result, 551-test reassessment and reported passing
CI were retained as historical evidence; they are not new test runs or a new CI
query. No current source regression was found requiring that investigation again.

## 2. Fresh operator authentication and credential readiness

The existing device-login utility's pinned public client, tenant, issuer,
audience, scope and MSAL device flow were reused in a preparation-only process.
Unlike its token-file saving entry point, this process kept the access token
exclusively in memory. The operator completed the interactive login.

The existing `OIDCVerifier` verified RS256 against the configured JWKS, exact
issuer/audience, Entra v2 delegated access purpose, `access_as_user`, exactly
`PolyMind.L1Operator`, and the principal's derived scope. Read-only registration
comparison established the same issuer/subject/tenant as independent live trust,
the registered owner/tenant, enabled local registration, user kind and
`PUBLICATION_MANAGE`. At the observed verification the token had more than the
additional 1,800-second preparation requirement remaining. Verified expiry:
**2026-11-07 10:07:32 UTC**.

Microsoft Graph separately reported `accountEnabled=true` for the Azure CLI
signed-in account. This preparation did not correlate that Graph object's `id`
with the verified access token's signed `oid`; the Graph result must not be
represented as a completed same-account join. That correlation remains a
prerequisite for a future final readiness verdict if remote account status is
required in addition to enabled local registration.

The exact named Azure resource's control-plane keys API returned its current API
key securely. The key response and selected key stayed in process memory and
were discarded after the readiness check. No generic `.env` key was used. No
token, API key, raw key response, encrypted/private key content or passphrase
was displayed, saved in evidence, or passed in command arguments. The token
process was closed after the financial blocker; future preparation must obtain
fresh credentials. The API-key use deadline remains unattested, and no intrinsic
Azure key expiry is asserted.

## 3. Azure deployment, quota and consumers

Read-only management queries at approximately 08:53–08:57 UTC verified the expected
subscription and tenant, enabled subscription, unique named resource and:

| Property | Observed |
| --- | --- |
| Resource | `epolymind-foundry-dev-susanta` |
| Deployment | `epolymind-gpt-54-mini` |
| Model / version | `gpt-5.4-mini` / `2026-03-17` |
| Region / deployment SKU | `spaincentral` / `GlobalStandard` |
| Resource and deployment provisioning | `Succeeded` |
| Deployment capacity | 30 |
| Rate limits per 60 seconds | 30 requests / 30,000 tokens |

The resource model catalog lists this exact model version as generally available
with Chat Completions and GlobalStandard support. Microsoft's current
[reasoning-model feature table](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning)
supports structured outputs for the model/version, and documents inclusive
reasoning/output token limits and billing. This corroborates capability
compatibility without making an exploratory provider call. Actual v5 application
acceptance remains untested.

Expected current resource fields match. The activity query since 01:00 UTC
returned the earlier List Keys operation and no observed configuration writes;
this is bounded, potentially delayed control-plane evidence, not proof that no
change of any kind occurred. No complete historical ETag baseline was available.

The subscription inventory and scoped state queries show the PolyMind AKS
cluster and node pool stopped, no container instances, and the other inventoried
container application stopped with minimum replicas zero. No Kubernetes access,
deployment, resource mutation, start or stop was performed. Local process
inspection found no conflicting L1 launcher. These observations cannot exclude
playgrounds, external scripts, other accounts or future starts. Fresh explicit
consumer-exclusion confirmation remains pending; `shared_consumers_verified`
was not set true.

## 4. Pricing, actual billing and financial blocker

The pinned local catalog remains `phase17hl-pricing-eur-202610/1`:

| Basis | Input EUR / million | Output EUR / million | Four-call maximum EUR |
| --- | ---: | ---: | ---: |
| Approved pinned catalog | 0.659978880676 | 3.959873284055 | 0.11351636747626 |
| November billing rates, derived below | 0.6732797701871715 | 4.039678621123029 | 0.115804120472193498 |

Azure Cost Management ActualCost and Azure Consumption usageDetails were both
queried read-only. The latter records the named resource in Spain Central,
OnDemand products `5.4 mini Inp Gl` and `5.4 mini Opt Gl`, unit `1M`, USD pricing
currency, EUR billing currency, input effective price USD 0.75 and output USD
4.50, with exchange rate **0.897706360249562 EUR/USD**, dated 1 November 2026.
Multiplication with Decimal precision 60 gives the second row. The projection
uses the unchanged maximum 100,000 input and 12,000 inclusive output tokens:

```text
USD (0.100 × 0.75 + 0.012 × 4.50) = USD 0.129
USD 0.129 × 0.897706360249562 = EUR 0.115804120472193498
Difference from pinned catalog = EUR 0.002287752995933498, approximately 2.01535%.
```

The 7 November quantities are exactly 0.002506 million input and 0.002130 million
output, matching the retained failed call's 2,506/2,130 provider tokens. Summing
the two usage-detail costs gives **EUR 0.01029175456708111**. The resource/day
ActualCost aggregate reports EUR 0.0102917545670811 at its returned precision.
The retained governance settlement is **EUR 0.010088437170011206** under the
approved catalog. Its difference from the usage-detail sum is
**EUR 0.000203317397069904**. Those records were reconciled, not rewritten.
The 1 November resource quantities likewise match the earlier run's 2,476 input
and 1,814 output tokens; ActualCost reports EUR 0.00899501772970062 for that date.

These are independently retrieved Azure usage/cost observations, not final
invoice amounts or a guarantee of future tariff stability. Meter products do
not themselves bind the model version; the current deployment query supplies
that independent configuration evidence. Public retail EUR searches returned
zero matching rows and were not treated as zero price or price approval.

Subscription ActualCost for 1–7 November also reports approximately EUR 6.454341
across resources, including existing Redis, networking, registries and unrelated
application resources. That subscription total is not this evaluation's spend
and is not the local EUR 5 governance budget. The two Foundry quantities explain
the observed billed evaluation usage to the available granularity; delayed or
unreported external usage cannot be excluded.

The original fixed/extra zeros, incremental attribution of existing costs,
monitoring/network/storage exposure and taxes have not been freshly attested.
No tax-inclusive total is asserted. The financial contract cannot honestly be
marked verified on current evidence. Separately reviewed financial resolution
is required; this task does not authorize a catalog migration, financial
exception, new conversion allowance or settlement correction.

## 5. Governance and admission snapshot

At **08:55:15 UTC**, schema/integrity checks and exact stored policy/catalog
comparisons passed using SQLite `mode=ro`, `query_only=ON` and read transactions.
No production authority constructor or audit-writing authorization method was
used. Stored registration/trust matches the freshly verified principal's scope.
Pure policy selection returns **`polymind-evaluation/1`**, not the smaller base
policy, with these balances in both owner and tenant scopes:

| Capacity | Remaining |
| --- | ---: |
| Monthly tokens, allowance 1,500,000 | 1,491,074 |
| Daily tokens, allowance 500,000 | 495,364 |
| Rolling requests, allowance 16 | 15 |
| Outstanding-token capacity | 112,000 |
| Catalog-accounted EUR | 4.981094244984159248 |

There are seven settled historical reservations, zero unsettled reservations,
zero active or recent shared-admission calls and no new reservation. The failed
call remains settled at known actual usage. Background admission retains 28,000
TPM, one RPM and one concurrent slot; the run's 25,000/3,000 per-call maximum
fits exactly. Both the catalog estimate and the billing-rate projection fit
recorded financial headroom. The EUR 5 contract ceiling remains a ceiling and
exceeds the current recorded balance; it is not the expected charge or available
spend. This snapshot reserves no future capacity.

## 6. Deterministic v5 plan, sizing and configuration status

The actual `build_plan` rebuild equals the preserved v5 plan using its native
extraction and current managed adapter/configuration. All source pieces resolve
through the existing EvidenceIndex. Plan fingerprint:
`e536899c1d871d4246d7751a258bcab7c9fd3e5a9cce1773e5001d24c416b030`.

| Paid step | Identity |
| --- | --- |
| Chunk | `fc0d3901-3444-5421-b30c-97231f8eea0a` |
| Structural reduction | `46ea2147-fdd6-5ba7-89aa-dda16d323ddc` |
| Root reduction | `aeec6738-1bef-56ff-8e70-4957cfaa63a4` |
| Grounded Q&A | Only after complete local digest, publication and retrieval |

Fresh rendering gives the exact chunk G1 estimate **12,216**, reserving 3,000
output. The preserved/current fixed envelope is 9,832 bytes; each one-child
reducer's planner bound is 16,832 bytes, or 17,032 with overhead/safety. The
prior reassessment's bounded Q&A witness is 24,223 input, leaving 777 context
units after output. That witness is not an actual generated Q&A request or a
universal annotation bound. Actual complete Q&A sizing remains mandatory before
call 4; no provenance truncation is permitted.

The four-call/100,000-input/12,000-output totals, 28,000 context, 7,000 child
contribution, 10,000 managed result, concurrency one, minimum 61-second spacing
and zero automatic retries remain unchanged. No inference or synthetic accepted
live checkpoint was created by these read-only checks.

The existing pending candidate was preserved with all seven pending fields
unchanged. No final `load_configuration` success or canonical
`configuration_digest` is claimed. **Final configuration digest: NONE.**
No invalid model construction, substituted clock or injected digest was used.

The proposed 09:00–09:45 UTC window, targeted launch by 09:10 UTC and at least
1,200 seconds of runtime runway were presented for operator coordination only.
They were not finalized or treated as an attested API-key deadline. After the
financial stop, a future attempt must coordinate and verify a fresh window.

## 7. Approval gates, acceptance and settlement

The existing independently pinned RSA-3072 public key matches the separate
public PEM. Its DER SHA-256 remains
`35785596dd2f38a3ae5fc8eeb93015a1ba3c8b4f16f06a1d73fbe521f9657816`.
Live trust, replay permissions and existing consumed historical marker were
verified read-only. No encrypted private key was opened or decrypted. The
historical consumed approval remains unchanged and cannot authorize v5.

| Stage | Actual status |
| --- | --- |
| Unsigned `bindings(config, principal, digest)` | NOT GENERATED; valid final configuration absent |
| RSA signing authorization, gate 1 | NOT REQUESTED; preparation blocked earlier |
| RSA signing / new approval | NOT PERFORMED / NONE |
| Saved new signature verification | NOT APPLICABLE |
| Separate paid-execution authorization, gate 2 | NOT REQUESTED |
| Controlled live launcher invocation | NOT PERFORMED |
| New paid calls / retries | 0 / 0 |
| New provider input/output / catalog cost | 0 / 0 tokens / EUR 0 |
| New reservation, replay consumption, settlement | NONE; no new obligation |
| Transport/schema/provenance/checkpoints | NOT EXERCISED for v5 live execution |
| Complete digest/publication/retrieval/Q&A | NOT REACHED |
| Independent human semantic review | PENDING |

The preparation review is a separate evidence reconciliation, not independent
human semantic acceptance. No current execution evidence or successful live
application result is implied.

## 8. Private preservation, validation and repository review

A new isolated operator-owned private preparation directory, identified in the
private preservation receipt, retains **23 files** containing sanitized Azure
deployment/capability/quota/consumer/billing reads, financial reconciliation,
identity verification metadata, local governance/admission/plan review,
preservation manifests and the blocked-stage verdict. Its empty
`unlaunched-audit` directory has never been used. Directory permissions are 0700
and evidence files are 0600. There is no final configuration, unsigned binding,
approval artifact, token, API key, private key or passphrase in the packet.

Before/after SHA-256 manifests establish unchanged original v5 package,
historical execution package, replay records, public trust and existing
security/governance/admission files. The pinned 11-file local embedding tree was
rehashed and matches the existing approved digest; no model was loaded/downloaded.
Private preservation used exclusive destination creation and verified copied
hashes. No original failed-run directory, replay record or authority was reused,
reset, deleted or modified.

Executed validation comprises fresh identity verification, scoped read-only
Azure queries and in-memory credential acquisition, authority integrity/schema
and accounting checks, public trust/replay checks, deterministic planning,
chunk rendering, embedding/source hashes and preservation checks. An initial
local helper assertion used the inventory wrapper rather than its
`source_sha256` member; it was corrected before the successful read-only check.
An initial login helper used the project environment without MSAL; the installed
authentication environment's existing packages were then reused. No dependency
was installed. Sandbox network failures were retried only through explicit
execution-policy escalation; these were control-plane/login reads, not paid
inference attempts.

No broad pytest rerun, compileall, Docker build, Kubernetes check or application
change was needed for this preparation-only task. Documentation whitespace and
link checks, secret-exclusion review and `git diff --check` are the final
repository validation. Implementation review confirmed unchanged provider-neutral
architecture, prompts, schemas, G1/G2 validation and launcher. Separate pre-commit
review covers only the two new Markdown deliverables and excludes credentials,
signed JWTs, private billing records and runtime artifacts from the repository.

Final `git status --short --branch` shows `master...origin/master`, the seven
pre-existing untracked Markdown files and these two new untracked deliverables.
`git diff --stat` and `git diff --cached --stat` are empty because no tracked or
staged file changed. No staging, commit, push, branch operation or remote mutation
occurred.

## 9. Conclusion and remaining boundaries

**OPERATOR PREPARATION: BLOCKED. Phase 17H remains PARTIAL.** Resolve the proven
catalog-versus-November-billing discrepancy through a separately reviewed
financial decision before resuming finalization. Reconcile actual Azure charges
and cost attribution without silently rewriting local historical settlements.
Consumer exclusion, incremental extras/taxes, API-key use deadline, same-account
Graph correlation, current credentials and a practical future UTC window remain
unfinished prerequisites. An affirmative response to an earlier proposed window
would not resolve the financial discrepancy or authorize signing/inference.

Once all prerequisites are genuinely satisfied, canonical configuration
validation, exact unsigned bindings and separate explicit signing authorization
are still required. Only after authorized signing and independent saved-artifact
verification may the separate paid-execution gate be presented. R2/R3, code fixes,
quota/policy changes and additional live attempts remain outside this task.
