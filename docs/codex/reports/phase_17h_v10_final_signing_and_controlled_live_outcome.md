# Phase 17H v10: final signing and controlled live outcome — continuation

11 November 2026 UTC. **OPERATOR_INPUTS_PENDING**.

This report records only new continuation evidence and decisions. The completed
[authentication and packet-preparation report](phase_17h_v10_authentication_renewal_and_final_operator_packet_preparation.md)
remains unchanged. No final packet, signing handoff, signature or paid evaluation
has been completed. The current provider gate is `PROVIDER_CREDENTIAL_PENDING`:
a securely loadable candidate exists, but scope and authorization for this
evaluation remain unconfirmed.

## Continuation baseline and current verification

The first current-time check was **19:12:41 UTC**. HEAD remains
`ec22fa3d116696b80a1bb12ad17e2eb37db38cb3`; the production generation digest remains
`e5fb249cc9b166b5e438f1534eb855fa5ab7531e08aa09314c110a1905327ebd`.
The baseline inventory contains 535 nonignored regular files, including all prior
reports and 27 inherited untracked documents. No source audit, architecture
review, historical test suite or synthetic workflow was restarted. The existing
2,595-test CI, 127 focused passes and successful synthetic rehearsal retain their
previous evidence boundaries; they are not new runs in this continuation.

Fresh read-only local checks at **19:13 UTC** confirm the same policies, catalog
and headroom: both scopes retain 16 rolling requests, 500,000 daily tokens,
1,459,618 monthly tokens, 112,000 outstanding-token capacity and
EUR 4.923760432874072880 monthly accounting headroom. There are thirteen SETTLED
reservations, zero unsettled reservations, zero active/recent admissions and ten
preserved consumed approval markers. All thirteen rows match the completed-v8
audit; the fourteen historical audit files retain their sealed hashes. Private
storage and public RSA trust checks pass without authority constructors or writes.

Azure management refresh verifies the expected deployment at **19:17:22 UTC**:
`epolymind-gpt-54-mini`, model `gpt-5.4-mini` version `2026-03-17`, GlobalStandard,
Spain Central, 30 RPM/30,000 TPM. Known AKS/node-pool/container-app states remain
stopped, no container instances are reported, and local launcher/admission checks
are empty. These observations do not establish distributed consumer exclusivity.

Six exact-resource meter records retrieved again reproduce catalog
`phase17hl-pricing-eur-202611/1`: EUR 0.673279770188/M input and
EUR 4.039678621124/M output from the previously established USD rates/conversion.
At **19:19:32 UTC**, production `Contract` confirms the unchanged four-call forecast
EUR 0.242439068181288 fits the already approved ceiling **EUR 0.242439068182**.
No additional identical financial approval was requested. Invoice VAT remains
unverified, accepted budgeting assumptions remain distinct, and commercial,
quota and financial observations must be refreshed near the actual final packet.
No ledger/catalog/policy or historical settlement was modified.

## Existing credential: secure supply verified, scope and approval pending

The operator identified the existing project-root `.env` key as the candidate and
authorized non-inference inspection of its loading path. Read-only checks confirm
the file is regular, operator-owned, single-link, nonsymlinked, mode **0600** and
Git-ignored. Existing `dotenv_values()` loads a nonempty candidate of usable local
format without displaying it. No secret was placed in a command argument, report,
log or new file, and no Azure key retrieval/regeneration was performed.

The `.env` endpoint passes the production named-resource allowlist. It differs
from the draft's hostname; the draft endpoint independently matches the current
named-resource endpoint. No endpoint was silently changed. An initial diagnostic
asserted exact URL equality and failed; the subsequent closed diagnostic correctly
distinguishes endpoint equality from same-resource allowlist membership. That
initial assertion was not treated as a credential-validity failure or a pass.

The established controlled wrapper supplies held credentials through the exact
`POLYMIND_L1_AZURE_CREDENTIAL` environment name read by the production launcher.
A separate local anonymous-pipe check verified that the existing candidate can
reach that environment slot in a child process and be discarded, without files,
command-line secrets, provider contact or launcher invocation. Core dumps were
disabled. This verifies local supply mechanics, not resource-key provenance or
data-plane acceptance.

The operator's latest explicit statement is:

- Original resource-key issuance is not independently verified.
- Approval of this candidate for this specific evaluation is pending confirmation.
- Authorized use through **21:50 UTC** is proposed, not finally attested.
- Provider acceptance is unverified; no inference test is authorized.

Those facts remain pending. Management authentication, endpoint coincidence and
key presence were not substituted for a resource-scoped approved credential.
No alternate bearer token, replacement key or free/hidden data-plane probe was
used. No private credential cache or key copy was created.

## Latest proposed window and authentication timing

The earlier 19:30 target and no-later-than-19:34:59 effective cutoff could not
safely accommodate unresolved inputs, fresh authentication, exact-packet review,
independent signing and separate execution authorization. No deadline was silently
extended. The operator then supplied this replacement proposal:

| Field | Latest proposed UTC value, 11 November 2026 |
| --- | --- |
| Not-before | 20:30 |
| Target start | 21:00 |
| Strict launch cutoff | 21:05 |
| Evaluation end | 21:30 |
| Configured approval expiry | 21:50 |
| Credential-use deadline | 21:50, subject to actual validity and approval |
| Exclusivity end | 21:50 |
| Attester | Susanta Hazra, pending final confirmation |

The proposed exclusivity end now covers proposed configured authority deadlines,
resolving the previous arithmetic discrepancy. **Actual exclusivity is still
unattested.** The operator expressly leaves playgrounds, external scripts, other
clients/accounts, interactive sessions and other shared-quota consumers pending
exclusion/accounting. `shared_consumers_verified` remains false.

With otherwise adequate authority, the existing one-second convention would
produce an effective exclusive launch cutoff of **21:04:59 UTC**. Actual earlier
token/provider/approval boundaries win. This is conditional arithmetic, not an
attested window or execution permission.

The previously verified application token is unavailable because its memory-only
session closed; it must not be reused. No fresh device flow was initiated in this
continuation while scope/use authority and exclusivity remained pending. An early
renewal could expire before this later target. Once those inputs are resolved,
renewal around the proposed 20:30 preparation period is a practical proposal,
subject to the actual returned expiry. Production RS256/claim/Graph/registration/
source-epoch checks and twenty-minute practical headroom must then pass. No future
token expiration or 21:50 validity is assumed in advance.

## Proposed configuration and remaining gates

The new protected temporary draft is:

```text
/tmp/phase17h-v10-auth-packet-20261111/continuation-20261111T1912Z/
configuration.v10.latest-window.pending-operator-facts.json
```

Its sidecar records the latest proposal and explicitly false operator/exclusivity/
credential-approval attestations. The draft uses existing schema fields, current
generation and unchanged authorities, the approved twelve-decimal financial
ceiling and proposed timestamps. A proposed audit destination is named but not
created. All previous candidate/configuration artifacts remain unchanged.

Actual production `load_configuration()` rejects exactly four required-true
prerequisites, as it should: `credential_audience_verified`, `quota_verified`,
`shared_consumers_verified` and `charges_verified`. Current quota/meters were
observed, but freshness/applicability at the later execution window has not been
finalized. No flag was changed to true to obtain parser success.

Existing candidate hashes were rechecked without regenerating the benchmark or
repeating prior offline validation:

| Artifact | Preserved SHA-256 |
| --- | --- |
| Source | 1be99e19a56040fb55c74682a19f874d4d4573f18d9f52a9a7ae19c8158ea92d |
| Extraction reference | b7410e987c6658c596399d4bccce4b6e11ec07cc95f29ab1c56eb2b7f011fcd1 |
| Canonical plan | 4390d9e59a4e626507673e5eec281538c50e9bfff33d8471cf1816f3cbc0fabf |

The source bytes and canonical plan fingerprint remain equal to those pins;
the preserved extraction reference retains the expected extraction hash. The
previous production reopening/extraction checks remain applicable; no new source
registration, job admission or vector store was created.

Final canonical configuration digest: **NOT CREATED**. Final actual-Principal
approval bindings and unused approval identity: **NOT CREATED**. There is no
exact-configuration signing handoff yet. No signer or private key was accessed.
Independent signing and separate paid-execution approvals remain unrequested
until there is a concrete verified packet to approve.

## Outcome and next operator action

**OPERATOR_INPUTS_PENDING**. Secure candidate loading is verified, while its
resource provenance/specific evaluation approval and authorized deadline remain
pending. The later timing/exclusivity proposal also awaits final attestation.
The next operator action is to resolve those facts; no repeated financial
decision is needed. Then perform useful fresh authentication, current-window
revalidation and exact packet/binding verification before requesting independent
signing. No attestation or approval is inferred from elapsed time.

Provider calls attempted/accepted: **0/0**. New usage/settlement: **0 input,
0 output, EUR 0**. G1/G2 live acceptance, canonical checkpoints, three-object
manifests, publication, grounded Q&A and semantic quality were not evaluated in
this continuation. Existing synthetic evidence is not a live outcome.

Final preservation checks retain all 535 baseline files and all selected existing
authority/replay inputs. Only this new continuation report is added to the
repository; earlier reports are unchanged. Final `git status --short -uall`
contains 28 untracked Markdown documents and no tracked/staged modifications.
`git diff --stat`, staged diff statistics and `git diff --check` are empty/clean.
No tests/compilation were rerun for this documentation and read-only continuation.

Git staging: **NO**. Git commit: **NO**. Git push: **NO**.
Resource-key retrieval: **NO**. RSA signing: **NO**.
Approval consumption: **NO**. Live inference: **NO**. Paid provider calls: **0**.
