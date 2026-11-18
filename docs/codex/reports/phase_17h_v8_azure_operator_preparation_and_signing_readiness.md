# Phase 17H v8 Azure operator preparation and signing readiness

## Final outcome — separately authorized controlled execution

**LIVE EVALUATION FAILED — STRICT ORIGINAL-SOURCE REFERENCE REJECTION.**
After separate explicit paid-execution and one-time-consumption authorization,
the single production-launcher invocation ran **20:30:01.760580–20:30:25.649469 UTC**
on 9 November 2026. It started within the unchanged **20:34:59** strict cutoff.
Exactly **one** Azure call completed: **2,749 input / 1,609 output tokens**,
catalog token cost **EUR 0.008350688989635328**.

The chunk response was rejected with `evidence_validation_failed` /
`foreign_evidence`, mapped to `NON_RETRYABLE` / `invalid_reference`. Offline
reconstruction using the exact saved plan, extraction, renderer, request hash and
unmodified response reproduces the rejection. The seventh claim's second
`evidence_ids` entry combines the first four UUID groups of one allowed source
identifier with the last group of another and is outside the four authorized
IDs. All eight current claim IDs/origins are correct; response and input limits
fit. No identifier was repaired or substituted. Reducers, publication and Q&A
were not reached, so live reducer lineage remains unvalidated.

The approval was consumed exactly once. The one new governance reservation is
SETTLED, giving **thirteen settled / zero unsettled**, with **zero active admission
calls**. All twelve earlier settlements and nine prior consumed markers retain
their original contents. Catalog and governance/admission policies are unchanged.
The credential holder closed and the transfer socket is absent. The fourteen-file
execution audit is preserved byte-for-byte during independent read-only review.

See the [complete execution and reconciliation report](phase_17h_v8_controlled_four_call_execution.md)
and [separate authorization task record](../prompts/phase_17h_v8_controlled_four_call_execution.md).
The earlier preparation/signing sections below are dated history; they do not
convey reusable readiness or another execution authorization. The strict launch
cutoff has passed and this approval is consumed. **No retry, extra provider call,
replacement approval or engineering fix is authorized.** Phase 17H remains open.

Git staging: **NO**. Git commit: **NO**. Git push: **NO**.
RSA signing: **YES — separately authorized and verified earlier**.
Approval consumption: **YES — exactly once, explicitly authorized**.
Paid inference: **YES — exactly one provider call**.


## Authorized RSA signing and separate paid-execution gate

**PASS — RSA APPROVAL INDEPENDENTLY VERIFIED; PAID-EXECUTION AUTHORIZATION REQUIRED.**
The operator explicitly authorized RSA signing of exactly configuration
`31e738353602ec072c4f9d334bddffaca3b89cbbd2ee912bcdcaf10243bfb389` and independently
verified unsigned bindings
`c92842eb9d353d868e576d49f1b716d602f8002284b96c7adc3c1d26ebc849f4`.
That authorization was recorded privately with approval consumption and paid
execution explicitly false. It did not authorize inference.

The protected credential session was retained. Its unsigned-preparation verifier
was archived with a hash equal to its original immutable preparation manifest.
A separately pinned private signing-stage continuation was installed in the
existing helper hook, preserving the earlier verifier and every configuration,
binding and production-source byte. This is a documented private tooling stage
transition; no claim is made that the dispatcher itself remained unchanged.
The continuation verifies all original manifest members, reading that one member
from its preserved archive, plus every newly pinned signing-stage helper. No
manifest or equality check was silently bypassed. Actual-Principal bindings were
independently reconstructed again through production functions before signing.

Ruff undefined-name and Python compilation checks passed for the new private
signing helpers. The established RSA-3072 procedure was rebound to the exact v8
configuration/bindings and proposed unused UUID. Before key access, fresh
OIDC/Graph, registration, exact binding, source/generation, public trust,
financial/admission, replay and empty-audit checks passed at **20:09:56 UTC**.

The operator entered the existing key passphrase only in the established local
masked Windows dialog. The decrypted key's public component matched both the
independent public file and pinned trust. A new independently authenticated
pre-sign checkpoint passed at **20:11:35 UTC**, after that dialog. The protected
signer then made exactly one authorized RS256 signature at **20:11:47 UTC** and
saved the compact approval exclusively in a private mode-0600 file. The private
key object was discarded after signing; no passphrase, plaintext key, token or
inference credential was persisted or displayed.

The saved signed-approval SHA-256 is:

```text
782f0b530815bfd6637428db2342afdb76029e3ca89c3fb2e2c921fc6780bc3c
```

At **20:12:00 UTC**, a separate process reauthenticated the actual held operator
token and checked Graph/registration again, reopened the saved artifact and ran
production `verify_artifact()` with the actual Principal, exact configuration,
reviewed digest and independent public trust. Header/algorithm/key ID, signature,
purpose/audience/issuer, timestamps, expiry, every binding and the proposed UUID
passed. Its artifact hash matches the exclusive saved-file bytes and signing
receipt. The approval remains **UNUSED** and the new audit directory **EMPTY**.
The original nine consumed markers, historical audits and all twelve settled
reservations remain unchanged. No approval consumption or inference occurred.

Post-signing Azure deployment/quota/network/consumer observations were refreshed
at **20:12:32 UTC**, with financial reconciliation at **20:12:33 UTC**. The expected
model/version/SKU and 30 RPM/30,000 TPM allocation remain valid. The catalog,
approved allowance **EUR 0.242439068181288**, owner/tenant headroom and twelve
settled/zero-unsettled usage disposition remain unchanged; active admission is
zero. The operator's explicit **19:45–21:30 UTC** exclusivity attestation remains
the operational consumer guarantee, distinct from inventory.

| Final execution-readiness dimension | Result |
| --- | --- |
| Exact signed configuration / unsigned bindings | VERIFIED; fingerprints above unchanged |
| Saved RSA signature and complete production verifier | PASS independently at 20:12:00 UTC |
| Fresh actual operator permissions and enabled Graph account | PASS |
| Token / configured credential validity | 21:06:41 UTC |
| Approval expiry / attested API-key deadline | 21:30 / 21:30 UTC |
| Confirmed exclusive deployment/shared-quota interval | 19:45–21:30 UTC |
| Execution not before / target | 20:20 / 20:30 UTC |
| Effective exclusive cutoff | **Launch strictly before 20:34:59 UTC** |
| Four-call catalog/VAT/network budgeting allowance | EUR 0.242439068181288; not an Azure hard cap |
| Financial/governance/admission headroom | PASS; twelve settled, zero unsettled, zero active |
| Approval consumption / audit destination | UNUSED / EMPTY |
| Paid-execution authorization | **NOT GRANTED** |
| Paid Azure inference | **NOT STARTED** |

The concrete proposal is one controlled production-launcher invocation, at most
four Azure calls, minimum 61-second start spacing, concurrency one, zero automatic
paid retries and no fallback, using only these exact configuration and signed
approval fingerprints. Its private reviewed proposal explicitly leaves paid
execution and approval consumption unauthorized. Fresh actual lifetime,
source/configuration, signature/replay, Azure/credential and financial checks
remain mandatory immediately before any later launcher invocation. Execution
must not begin before 20:20 or at/after the effective cutoff; no deadline may be
extended silently. If authorization or final checks cannot complete in time,
stop without launching or resetting replay/history.

This task stops at the **separate explicit paid-execution authorization gate**.
There is no automatic launcher invocation. Full live v8 success and independent
semantic acceptance remain unvalidated; Phase 17H remains open.

Git staging: **NO**. Git commit: **NO**. Git push: **NO**.
RSA signing: **YES — explicitly authorized, one signature, independently verified**.
Approval consumption: **NO**. Paid inference: **NO**.

The branch and HEAD remain unchanged; v8 remains uncommitted and no new CI success
is claimed. `git diff --stat` remains 12 pre-existing tracked files, +134/-47;
the index is empty. Only this task's existing prompt/report are updated in the
repository. Earlier sections below preserve the pre-signing preparation history.

## Current renewal — confirmed evening schedule

The original **16:00–18:00 UTC window has expired**. Its schedule, draft,
proposed approval identity and audit destination will not be reused. A new
private preparation packet, fresh unused approval identity and empty private
four-call audit destination have been created. Historical evidence and consumed
markers remain intact. The initial current-time check was **19:30:36 UTC on
9 November 2026**; the proposed evening schedule was still practical.

The operator separately and explicitly confirmed the entire schedule and
exclusive deployment/shared-quota use, including playgrounds, external clients
and other consumers, for **19:45–21:30 UTC on 9 November 2026**. This is an
operator attestation, not an inference from stopped Azure resources.

| Confirmed step | UTC |
| --- | --- |
| Exclusive deployment/shared-quota interval | 19:45–21:30 |
| Fresh Entra login | Approximately 19:50 |
| Configuration and binding verification | 20:00–20:10 |
| Separate RSA authorization / independent saved-signature verification | 20:10–20:20 |
| Separate paid-execution authorization | 20:20–20:30 |
| Execution not before | 20:20 |
| Target launcher start | 20:30 |
| Operator's strict launcher cutoff | 20:35 |
| Approval expiry | 21:30 |
| Operator-attested API-key use deadline | 21:30 |
| Actual verified token expiry | **21:06:41** |
| Effective strict launcher cutoff | **Strictly before 20:34:59** |

The actual cutoff must be strictly earlier than the minimum of the operator's
20:35 cutoff, approval expiry minus twenty minutes, API-key use deadline minus
twenty minutes, token expiry minus twenty minutes and any stricter applicable
launcher boundary. The prepared arithmetic uses an exclusive integer-second
cutoff one second before that minimum. The production ten-minute boundary is
also retained. If the resulting cutoff cannot support the target and controlled
evaluation, stop for a newly confirmed practical window; never extend it silently.
The final configuration will conservatively cap credential validity at the
earlier of the attested API-key deadline and actual token expiry.

At **19:31:52 UTC**, fresh source planning, generation inventory, embedding
integrity and read-only security/governance/admission checks pass. Generation is
still `managed-prompt/8` with SHA-256
`93ca9066491c197987f919c5d185417bf4f3d2787384acf2833011e32641c0df`.
HEAD, the twelve unstaged tracked modifications and the source bytes reviewed
in the earlier checkpoint are unchanged. The fresh deterministic plan still has
one chunk, two reducers and one Q&A call, with plan SHA-256
`08cefd0669d2638d2ff8e4a3295f9aabcdc0a0dec4f09a23a4eb974a6288274d`.
All eleven local embedding files match their pinned tree hash. No CI success for
uncommitted changes is claimed.

Renewed read-only Azure and financial observations at **19:33–19:34 UTC** pass.
The expected model/version/SKU, 30 RPM/30,000 TPM allocation, endpoint,
API-key authentication policy, public route and diagnostics/storage configuration
remain consistent. The current resource Consumption token total is
**EUR 0.06826989541720903**. Relative to the earlier observation, input/output
meter quantities increased by exactly **11,131 / 5,211 tokens**, independently
matching the failed v7 evaluation's settled usage. The approved catalog and
full next-run allowance **EUR 0.242439068181288** remain unchanged.

All twelve settlement rows exactly match the preserved v7 financial audit,
including the unchanged earlier nine rows; unsettled usage and active/recent
admission calls remain zero. Both scopes still have eleven requests, 472,902 daily
and 1,463,976 monthly tokens, 112,000 outstanding-token capacity and
EUR 4.932111121863708208 catalog-accounted monthly headroom. The conservative
comparison, still adding the entire v7 cost on top of currently observed billing
and therefore potentially double counting posted charges, leaves
**EUR 4.63847855828307794894** after VAT budgeting and the entire next-run
allowance below the EUR 5 comparison ceiling. This is not an Azure spending cap.
Historical catalog charges are preserved; VAT/network budgeting and delayed
invoice observations remain separate from token ledger settlements.

The initial fresh Entra flow began at **19:50 UTC** and passed all identity
checks, with token expiry 20:54:44. At **20:00:38**, the private finalizer stopped
on a missing `private_path` import before writing a configuration or unsigned
bindings. Its error receipt and complete packet were preserved; the memory
helper cleared the token and resource key. This was a private preparation-tooling
failure, not a production generation, binding, financial or cloud incompatibility.

The missing import was corrected in a new private packet. Ruff undefined-name
checking passes for all private helpers, supplementing syntax/compilation checks.
A single recovery device flow began at **20:02 UTC**, and the operator completed
it. The new actual Principal again passes RS256, pinned issuer/audience,
delegated scope, exact PolyMind.L1Operator role, registration, tenant,
PUBLICATION_MANAGE, Graph enabled-account and signed-OID correlation. The named
resource key was securely reacquired at **20:02:42 UTC**. Neither login's token
nor key was persisted or displayed. The successful helper retains credentials
only in protected process memory; no automatic login renewal or live executor
exists in that helper. No deadline or exclusivity interval was extended.

**The current verified token expires at 21:06:41 UTC.** Configuration credential
validity is conservatively capped at that same time, while the operator-attested
API-key use deadline remains **21:30 UTC**. Approval expiry remains **21:30**.
The production ten-minute credential/approval boundary is **20:56:41** and the
twenty-minute authority boundary is **20:46:41**. The operator's **20:35** cutoff
is stricter; the effective exclusive integer-second cutoff is **20:34:59 UTC**.
Launch must be strictly before that time, and not before **20:20**. The **20:30**
target remains practical. Intrinsic expiry of the Azure API key is not asserted.

Final read-only Azure observations completed at **20:02:38 UTC**, and financial
reconciliation at **20:02:39 UTC**. Resource Consumption is still
**EUR 0.06826989541720903**; Cost Management independently reports
**EUR 0.06826989541720902**. Current catalog/policy hashes, all twelve exact
settlement rows and governance/admission headroom remain unchanged. The approved
full four-call allowance remains **EUR 0.242439068181288**. The above conservative
VAT-adjusted comparison still leaves EUR 4.63847855828307794894 below the scope
ceiling. It deliberately may double count posted v7 cost and is not an invoice
reconciliation claim or a hard Azure spending cap.

A fresh offline selection passes **94 tests in 36.52 seconds**, with zero network
attempts and zero failures/errors/skips, covering v8 sizing, frozen v8/historical
contracts and actual launcher compatibility. Ten additional private timing
arithmetic checks cover exact/short lifetimes, token/deadline minima and missing
exclusivity. All existing source filenames/bytes, historical reports, protected
authorities and the exact nine-marker replay inventory remain unchanged; only
this task's own report/task record is updated.

**PASS — V8 CONFIGURATION READY; RSA AUTHORIZATION REQUIRED**

A new LaunchConfiguration was created at **20:03:06 UTC** using the confirmed
schedule and actual verified lifetime. Its exact production canonical JSON bytes
were saved privately with mode 0600, reopened through `load_configuration()` and
compared with the original validated model. The saved byte SHA-256 equals
production `configuration_digest()`:

```text
31e738353602ec072c4f9d334bddffaca3b89cbbd2ee912bcdcaf10243bfb389
```

The new unsigned approval bindings were created through production `bindings()`
from the actual authenticated Principal. Their sorted compact JSON was saved
privately without reformatting monetary values. Its canonical and saved-byte
SHA-256 are identical:

```text
c92842eb9d353d868e576d49f1b716d602f8002284b96c7adc3c1d26ebc849f4
```

At **20:03:08 UTC**, a separate process independently reauthenticated the actual
access token, including Graph/registration checks, reopened the saved
configuration, reconstructed every binding through the production function and
compared exact serialized types/values. It independently reconstructed the
fifteen-member generation inventory and digest. It also reopened/rebuilt the
actual four-page plan against the authenticated scope, verified the embedding
tree, RSA public trust and public-file correspondence, and rechecked financial
headroom, the unused approval identity, empty audit directory, exact source/file
inventory, immutable private artifact hashes and protected authorities/replay.
Its sanitized receipt is
`PASS_INDEPENDENT_UNSIGNED_CONFIGURATION_AND_ACTUAL_PRINCIPAL_BINDINGS`.
No Principal was reconstructed from metadata and no private signing key was opened.

| Final dimension | Result |
| --- | --- |
| V8 source and generation contract | PASS; expected digest, existing uncommitted source disclosed |
| Exact structural-path/child boundary regressions | PASS |
| Deterministic plan / actual node reservations | PASS: one chunk, two reducers, one Q&A; unchanged limits |
| Azure deployment/model/version/SKU and actual quota | PASS at 20:02:38 UTC |
| Shared consumers and exclusivity | PASS inventory plus explicit operator 19:45–21:30 UTC attestation |
| Current Principal, signature, Graph, role and permissions | PASS; expiry 21:06:41 UTC |
| Financial/governance/admission capacity | PASS; twelve settled, zero unsettled, zero active calls |
| Execution window | Valid; target 20:30, effective strict cutoff 20:34:59 UTC |
| Canonical configuration SHA-256 | VERIFIED as above |
| Exact unsigned approval bindings | VERIFIED independently as above |
| Independent RSA public trust | PASS: 3,072-bit; pinned DER fingerprint unchanged |
| New approval UUID | Fresh, unused; no marker created |
| New audit destination | Empty, private, distinct from every prior run and replay store |
| Historical audits/approvals/settlements | Preserved; all nine consumed markers unchanged |
| Live inference | **NOT STARTED** |

The configuration retains four calls; 25,000/3,000 input/output per call;
100,000/12,000 aggregate tokens; 28,000 context; 61-second call-start spacing;
concurrency one; zero automatic paid retries; no fallback; and unchanged source,
raw/canonical response, full-child and Q&A contracts. Runtime actual-child and
retrieved-Q&A checks remain mandatory. V8 model compliance and independent live
semantic acceptance remain unproven.

The strict operator/effective cutoff is an additional controlled-wrapper
condition, frozen in the private attestation/artifact inventory; it must be
rechecked before any later launch. The production LaunchConfiguration binds
not-before, approval expiry and the capped credential-validity deadline.
Uncommitted source remains a disclosed operational risk; a user-controlled v8
commit and successful CI are preferred before signing. Any source/configuration
change invalidates readiness and requires revalidation; no fresh CI success is
claimed for the unpushed changes.

**Current authorization gate: explicit RSA signing authorization for exactly
these fingerprints and independently verified bindings.** Signing is not yet
authorized or performed. A future signed artifact must be independently verified,
then all time-sensitive checks and unused-approval predicates must be refreshed
before requesting separate paid-execution authorization. If either gate cannot
be completed within the valid window, stop; never extend deadlines or rerun
inference automatically. This task stops at the RSA question and does not request
paid execution.

Git staging: **NO**. Git commit: **NO**. Git push: **NO**.
RSA signing: **NO**. Approval consumption: **NO**. Paid inference: **NO**.

The existing twelve tracked modifications remain unstaged, with unchanged
`git diff --stat`: **12 files changed, 134 insertions, 47 deletions**. There are
still thirty-two untracked files, including this task's existing prompt/report;
this renewal adds no Git-visible file. The index remains empty. All historical
reports and engineering files retain their prior hashes. Only this preparation
report and its task record were updated. The earlier checkpoint below is retained
solely as dated history, including its earlier blocking verdict.

## Earlier preparation checkpoint — 15:22 UTC (historical)

The following preserves the earlier checkpoint as dated evidence. Its expired
schedule and pending 16:40 login are historical, not current authority.

Recorded 9 November 2026 UTC. **BLOCKED — V8 ENGINEERING, FINANCIAL OR OPERATOR
PREFLIGHT.** The outstanding preflight is fresh, suitably timed operator
authentication. Engineering, current read-only Azure checks and financial
reconciliation pass. The operator confirmed the execution window and separately
attested exclusivity, then chose to authenticate around **16:40 UTC**. This is a
preserved preparation checkpoint, not a signing-ready configuration or a failed
model evaluation. No RSA authorization is requested yet.

The [task record](../prompts/phase_17h_v8_azure_operator_preparation_and_signing_readiness.md)
preserves the scope and subsequent operator steering. Private preparation files,
source inventories, management responses, settlement comparisons and test evidence
are outside Git in an operator-owned directory with mode 0700; private files use
0600. No credential or real operator identity is included here.

## Starting Git and generation state

Actual branch is `master`; HEAD is
`6e0319e29984ad019edced0e076b3b0a4ae8c007`, the expected v7 checkpoint. At entry,
12 tracked files were modified, 30 files were untracked and the index diff was
empty. The v8 implementation, historical compatibility adjustments and new
boundary regressions are **uncommitted**. No fresh GitHub CI success is claimed
for these local changes. A user-controlled v8 commit and successful CI remain
preferred before signing; neither operation is authorized for Codex.

A private SHA-256 inventory covers all **485 existing Git-visible files**.
Its sorted compact JSON fingerprint is
`25b7b5f31aec4faa9c1a6890578dbc7dd6074f5214fb4ef5c4a39ff0f0a44bab`.
The production generation inventory was reconstructed independently from the
actual fifteen source paths and compared with the production function. Fourteen
members match committed HEAD bytes; only `documents/digestion/managed.py`
differs. Its source hash is
`7f67a5fcf123abd736ed8e88037f9f69df6d05e070410f8bba448f2215a8a334`.

The active template and complete generation fingerprint are exactly:

```text
managed-prompt/8
93ca9066491c197987f919c5d185417bf4f3d2787384acf2833011e32641c0df
```

Review of the production diff confirms only the template version and explicit
immediate-child pair instructions changed. Validators, codec, planning, workflow,
provider boundary, publication, security, governance and launcher implementation
remain unchanged. This preparation makes no production change.

## Engineering, boundaries and fresh deterministic plan

AGENTS.md, both v8 reports, the v7 execution report, Foundry runbook, independent
operator approval procedure and relevant generation/validation/workflow/security/
governance/launcher consumers were inspected. The Antigravity finding recorded
in the boundary supplement concerns permanent assertions for the measured
166/167-character boundary. Those regressions were independently rerun here;
no separate external Antigravity transcript was available in the inspected
repository, so no broader external audit certification is claimed.

Current-stage claim IDs remain positional IDs from the current stage; origins
must identify that stage. Direct lineage authority is the exact immediate-child
`(stage_id, claim_id)` pair, not independent membership of the component UUIDs.
Cross-level and cross-child substitutions, duplicate links within a claim and
missing child coverage fail unchanged validation. Original source and
qualification evidence membership remains separately enforced. No generated-ID
repair, source fabrication, truncation, retry or fallback is introduced.

Durable workflow review confirms validation of the result, inherited metadata
and complete child wrapper before checkpoint storage. Finalization reopens and
revalidates the graph. Regressions preserve accepted earlier checkpoints and
settled usage when later output fails. V5/v6/v7 results remain readable under
their historical contracts, while stale settings/plans/generation bindings are
rejected for v8 execution. Failed digestion blocks publication and Q&A. Passing
synthetic workflow tests exercise publication authorization, retrieval and
citations resolving original source offsets and excerpts.

Fresh planning used the launcher's actual deterministic four-page PDF recipe,
native extraction, existing owner scope and current v8 settings. Every extracted
line matched the recipe; every planned evidence piece resolved exactly and all
source text was retained. It produces **one chunk, two reducers, then one grounded
Q&A call**. The fresh plan fingerprint is:

```text
08cefd0669d2638d2ff8e4a3295f9aabcdc0a0dec4f09a23a4eb974a6288274d
```

| Reservation or boundary | Fresh verified result |
| --- | ---: |
| Managed input allocation | 24,800 |
| Context ceiling | 28,000 |
| Complete-child maximum | 7,000 bytes |
| Maximum fixed envelope | 10,630 bytes |
| Empty-path two-child reservation | 24,630 bytes |
| Available two-child structural-path margin | **170 bytes** |
| Exact boundary with 170/171 escaped path bytes | 24,800 accepted / 24,801 rejected |
| Exact complete boundary contexts | 28,000 accepted / 28,001 rejected |
| Actual fresh chunk input including overhead/safety | 13,014 |
| Actual chunk complete context including output | 16,014 |
| Each actual L1 reducer: children / path | One / empty |
| Each actual L1 reducer planner input reservation | 17,630 |
| Each actual L1 reducer complete context reservation | 20,830 |
| Digestion raw / canonical output ceilings | 10,000 / 10,000 bytes |
| Digestion HTTP envelope ceiling | 26,192 bytes |
| Q&A raw response ceiling | 12,000 bytes |

All planned nodes fit their actual paths and maximum child reservations. The
exact path tests cover intermediate, structural and root profiles with ordinary,
escaped and Unicode paths. The 6,999/7,000/7,001-byte child boundary regressions
also pass. These conservative serialized-byte estimates are not billed tokens.
Future live child outputs and retrieved Q&A material must still pass their
actual runtime checks; no preparation can pre-certify those unknown outputs.

The pinned local embedding tree has eleven regular files and matches its
configuration hash. The launcher selects local-only CPU loading and disabled
Chroma telemetry. No embedding download or external embedding call occurred.

## Current Azure deployment and consumer findings

Authorized management/billing reads completed at **15:12:20 UTC**. The initial
sandboxed management read failed; the same scoped read-only script was rerun
through the execution-approval mechanism. No raw Azure error or key was printed.

Subscription and tenant match the established private pins; the subscription is
Enabled. The expected resource and deployment exist in Spain Central and are
Succeeded. The deployment serves `gpt-5.4-mini`, version `2026-03-17`,
GlobalStandard, with **30 RPM / 30,000 TPM**. Model inventory reports Chat
Completions support and GenerallyAvailable lifecycle. Microsoft's current
[model/version feature table](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning#api-and-feature-support)
also lists structured output, system messages and completion-token support for
this model/version. Offline strict-schema compatibility passes; this does not
certify a future model response's application compliance.

The configured v1 endpoint host matches an endpoint of the exact named Azure
resource. The selected authentication mode is resource API key, with the existing
protected exact-resource management retrieval process prepared for the timed
identity step. No inference credential has yet been retrieved in this task.
The [Azure v1 interface documentation](https://learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle)
supports the existing base-URL/API-key composition; no inference endpoint was
probed or invoked.

Public network access remains enabled, ACL default action is Allow and no private
endpoint connections or customer-owned storage attachments are configured. The
resource has no diagnostic export settings. The established public financial
route remains applicable. No Azure resource was created, resized, restarted or
modified; no Kubernetes access was needed.

The selected account lists only the evaluation deployment. Regional model
allocation is 30K of 1,000K TPM for GlobalStandard. The other inventoried account
lists a separate DataZoneStandard deployment at 10K, matching the 10K of 200K
DataZone quota partition. Known AKS/node-pool consumers and the other application
are stopped; container-instance inventory is empty. These management reads do
not prove absence of playgrounds or external clients. The operator's separate,
explicit 16:00–18:00 deployment/shared-quota exclusivity attestation supplies that
operational prerequisite.

## Financial reconciliation and governance/security capacity

The catalog remains `phase17hl-pricing-eur-202611/1`, canonical hash
`59c90a122e3db199848ae0817218bc4286bab80b22920a0916d8f5a54426dd37`.
The unchanged approved financial contract hash is
`c5f6338684146f44abe763c794b6b872a23930d65548eefd87c5e2196935699d`.
Current Consumption meters still show USD 0.75/4.5 per million input/output tokens
and November EUR conversion 0.897706360249562. The catalog's EUR prices reproduce
the approved upward rounding to twelve decimals. Independent Fraction arithmetic
and the production cost function agree on the full four-call token reservation.

| Reviewed component | EUR |
| --- | ---: |
| Four-call maximum catalog token cost | 0.115804120472288 |
| Token VAT budgeting allowance, 23% | 0.02663494770862624 |
| Provisional VAT-inclusive networking contingency | 0.10 |
| Conservatively rounded combined extras | 0.126634947709 |
| Full approved anticipated allowance | **0.242439068181288** |
| Scope comparison ceiling | 5.00 |

Consumption pagination completed with 89 subscription rows, including six
resource-specific OnDemand input/output meter rows. Resource token cost totals
**EUR 0.03972485300058354**. Cost Management independently totals
**EUR 0.03972485300058352**; the tiny serialization difference is below
EUR 0.000000000001. No new resource meter class is observed. GlobalStandard
remains [pay-per-token](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types).
These delayed observations are not final invoice or VAT verification.

All twelve current reservation rows exactly match the saved v7 financial audit;
the nine earlier rows also match their independent prelaunch snapshot. The v7
audit's entire sixteen-file inventory is unchanged. Provider captures, enriched
records, run-guard usage and settlements agree on all three v7 calls: **11,131
input, 5,211 output, EUR 0.028545042416639792**. All twelve reservations are
SETTLED; unsettled usage and active/recent-minute admission calls are zero.
Historical rows retain their original catalogs and charges; none was repriced.

To avoid treating delayed billing as complete, the comparison conservatively
adds the entire known v7 catalog cost to all observed resource billing, then
applies the 23% allowance and the whole proposed run allowance. This may double
count billing already posted, but leaves **EUR 4.67358896045552730164** below the
EUR 5 scope ceiling. It does not invent an invoice settlement or convert VAT/
networking into governance token debits. Approved unrelated unused/unmodified
Azure infrastructure and personal local resources remain excluded on their
existing terms. The EUR 0.10 networking contingency is provisional; neither the
allowance nor the comparison ceiling is an enforced Azure spending cap.

At **15:10:29 UTC**, both owner and tenant select `polymind-evaluation/1` and have:

| Remaining capacity, each scope | Value |
| --- | ---: |
| Rolling requests | 11 |
| Daily tokens | 472,902 |
| Monthly tokens | 1,463,976 |
| Outstanding-token capacity | 112,000 |
| Catalog-accounted monthly EUR | 4.932111121863708208 |

The complete four-request, 112,000-token reservation and full financial allowance
fit both scopes. The existing admission policy matches configuration and has no
active or recent-minute calls. No conflicting local launcher was found. Existing
security storage passes read-only integrity inspection; current authenticated
operator permissions remain pending the scheduled device login.

All authority connections used SQLite `mode=ro`, `query_only=ON` and integrity
checks, without mutating authority constructors or reservations. The full v8
engineering authority/replay preservation inventory still matches byte for byte.
No catalog, governance/admission policy or historical settlement was modified.

## Operator authentication and confirmed execution window

The operator explicitly selected the following UTC times on 9 November 2026,
separately confirmed exclusivity, and agreed to authenticate around 16:40 UTC:

| Event | UTC |
| --- | --- |
| Execution not before | 16:00 |
| Target launcher start | 17:00 |
| Strict exclusive launcher cutoff | **17:15** |
| Approval expiry | 18:00 |
| Operator-attested API-key use deadline | 18:00 |
| Confirmed exclusive deployment/shared-quota interval | 16:00–18:00 |
| Fresh operator token expiry | **Not yet issued or verified** |

The canonical approval/key expiration-minus-ten-minute boundary would be 17:50.
The controlled wrapper additionally requires twenty minutes to the earliest
authority deadline, including actual token expiry; the operator's 17:15 cutoff
also applies. None of these times is extended. API-key use deadline is an
operator attestation, not an intrinsic key-expiry claim.

No fresh device flow was initiated around 15:10 solely to hold credentials until
the later launch. The protected memory-only helper is prepared with core dumps
disabled and no signing, live execution or automatic authentication-renewal path.
The established verifier will check RS256, issuer/audience, delegated scope,
exact PolyMind.L1Operator role, registered user/tenant, PUBLICATION_MANAGE, enabled
Graph account and signed-OID correlation. Those are **pending current checks**,
not inferred from historical successful logins. If the actual fresh lifetime
cannot support the confirmed cutoff and required runway, preparation must stop
for a revised practical window or suitable fresh authority before signing.

## Unsigned configuration, fingerprints and independent verification

A fresh private draft selects the v8 generation digest, existing exact owner and
authorities, unchanged approved contract, confirmed window and new audit path.
It explicitly sets credential verification **false** pending the timed protected
retrieval. It is not represented as a validated LaunchConfiguration. A new private
approval UUID is proposed and verified unused; no replay marker is created. The
new private audit directory is empty. All nine historical consumed markers are
preserved, including v7. No old configuration or signed approval is reused.

| Artifact or verification | Current result |
| --- | --- |
| Final canonical configuration SHA-256 | **Not finalized; fresh authentication/credential readiness pending** |
| Exact unsigned approval-binding SHA-256 | **Not created; actual fresh Principal required** |
| Production canonical serializer and loader | Inspected; exact saved canonical bytes required during finalization |
| Separate-process saved-configuration/binding verifier | Prepared and syntax checked; not yet executed |
| Independent RSA public trust | PASS: 3,072-bit RSA; independent public file matches trust |
| Public DER SHA-256 | `35785596dd2f38a3ae5fc8eeb93015a1ba3c8b4f16f06a1d73fbe521f9657816` |
| Proposed approval identity | Fresh and unused; private UUID omitted |
| New audit destination | Private, empty, separate from historical replay authority |
| Historical approvals | Preserved; consumed markers retained |

The prepared independent verifier accepts the actual fresh access token only
through an anonymous process pipe, independently invokes OIDC verification and
the registered-user/Graph checks, and reconstructs bindings through production
`bindings()`. It will compare exact serialized types/values, saved byte hashes,
complete generation digest, public trust, UUID, audit destination and current
headroom. No Principal is manufactured from historical metadata. This describes
prepared tooling, not a completed verification receipt.

Management and commercial evidence must be refreshed near that final step; the
current approximately 15:12 observations cannot silently serve as fresh 16:40
attestations. Existing source hashes and HEAD must be rechecked. Any source or
configuration change invalidates preparation and requires revalidation. No final
configuration/binding digest is asserted merely to satisfy a report field.

## Validation, self-review and separate pre-commit review

Fresh focused offline testing passed **453 tests in 142.63 seconds**. JUnit
independently records 453 tests, zero failures/errors/skips; the network guard
reports **zero network attempts**. The selection includes v8/v7 sizing and exact
path boundaries, child-material reconciliation, G1 source compatibility, current
claim identity/direct lineage, failure workflows, v8/v7 frozen generation,
historical v5/v6/v7 refusal, launcher/Entra, strict Azure compatibility, synthetic
publication/Q&A and approval/replay. The earlier 2,067-test full suite is reviewed
historical evidence; it was not rerun or relabeled as a fresh full-suite result.

Whole-repository `python -m compileall -q .` passed with an external bytecode
cache. `git diff --check` passed. Private preparation helper syntax was checked
using AST parsing. No dependencies were installed. Docker/Compose/Kubernetes
validation was unnecessary for this read-only preparation and documentation task;
none was run.

Self-review traced actual source inventory, strict evidence/pair authority,
checkpoint commitment/recovery, launcher timing, canonical serialization,
protected credential lifecycle and financial separation. A private reconciliation
reader initially decoded saved SQLite timestamp floats as Decimal; the exact-row
comparison correctly stopped. It was corrected to retain their original JSON
types. A subsequent price comparison correctly required the catalog's approved
upward rounding rather than raw currency multiplication. Both corrections were
private read-only analysis tooling; no production or historical data changed.

The separate pre-commit review checks this task's prompt/report for credentials,
private identities, private key material, local sensitive paths, unresolved local
links and claims exceeding completed evidence. Prior tracked/untracked files and
historical reports remain unchanged. Temporary scripts, management/billing
responses, actual UUIDs and sensitive artifacts remain outside Git. No private
signing key was opened.

## Final decision table, remaining risks and exact gates

| Dimension | Current result |
| --- | --- |
| V8 source and generation contract | PASS; uncommitted source explicitly disclosed |
| Boundary regression verification | PASS |
| L1 deterministic four-call plan | PASS |
| Azure deployment/model/version | PASS at 15:12; renew near final authentication |
| Quota and consumers | PASS inventory plus explicit 16:00–18:00 operator exclusivity attestation |
| Operator identity and permissions | **PENDING fresh device login around 16:40** |
| Financial/governance headroom | PASS; recheck during final verification |
| Execution window | Confirmed; actual token-lifetime practicality pending |
| Canonical configuration digest | **PENDING finalization** |
| Exact unsigned approval bindings | **PENDING actual-Principal independent verification** |
| RSA public trust | PASS |
| Approval UUID | Unused |
| Audit destination | Empty |
| Historical approvals | Preserved and consumed as recorded |
| Live inference | **NOT STARTED** |

The immediate blocker is operator-timed authentication, not an engineering or
financial incompatibility. Continue near 16:40 with fresh management/commercial
reads, the one-time operator device step, actual token/credential verification,
canonical finalization and independent unsigned binding verification. Do not
request RSA authorization until all rows pass and exact final fingerprints are
recorded. If a genuine engineering incompatibility is discovered, stop and report
it without changing validators or expanding scope.

After successful preparation, the first explicit authorization gate is:

> Do you authorize RSA signing of this exact Phase 17H v8 configuration and its independently verified approval bindings?

This quoted future gate is procedure documentation, **not a current signing
request**. A separately authorized future signing operation must be independently
verified before any separate paid-inference authorization can be requested.
Neither gate is crossed here. Model compliance, full live four-call success and
independent semantic acceptance remain unvalidated; Phase 17H is not closed.

## Git disposition

The twelve pre-existing tracked modifications remain unstaged. Their
`git diff --stat` is unchanged: **12 files changed, 134 insertions, 47 deletions**.
The original thirty untracked files are retained. Only this task's clean prompt
and report are added to Git-visible files, for thirty-two untracked files total.
The index diff remains empty; HEAD and branch are unchanged. Private inventories
preserve the exact existing source/untracked inventory rather than mistaking the
tracked diff stat for the complete v8 change set.

**Git staging: NO**
**Git commit: NO**
**Git push: NO**
**RSA signing: NO**
**Approval consumption: NO**
**Paid inference: NO**
