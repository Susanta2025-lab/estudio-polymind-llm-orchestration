# Phase 17H v5 final operator preparation continuation

Date: 8 November 2026 UTC. Branch `master`; HEAD remains
`2b8a5ac73beb32d7febc53f77d0c3a459c8e3394`. The
[task record](../prompts/phase_17h_v5_final_operator_preparation_continuation.md)
preserves this continuation's boundaries.

**OPERATOR PREPARATION: PASS — AWAITING SIGNING AUTHORIZATION.** Fresh delegated
authentication, same-account Graph verification, enabled registration and
publication permission passed. The resource-specific API key is held only in a
protected process. Current Azure/local admission checks and explicit operator
exclusion/window attestations support the final configuration. Canonical loading
and a separate saved-artifact review passed. Exact unsigned bindings exist.

No RSA signing, approval consumption, reservation or paid inference occurred.
The encrypted private key was not opened. Human semantic review remains PENDING.
Financial readiness and its approved EUR 0.242439068181288 aggregate allowance
were preserved without repeating the financial investigation or changing a
catalog, authority, historical settlement or earlier approval.

## 1. Previous login failure and sanitized diagnostics

The [previous stopped-stage report](phase_17h_v5_complete_financial_readiness_and_operator_preparation.md)
recorded `STOPPED / DEVICE_LOGIN / AssertionError`, no usable token and no key
acquisition. The helper combined device-flow acquisition and result checking
under one stage, then asserted that `result.get('access_token')` was a nonempty
string. A token-less MSAL error result therefore became a generic assertion and
its underlying `error` was discarded.

The retained record has no response or traceback capable of conclusively
distinguishing that explicit assertion from an internal library assertion, or
identifying expiration versus refusal/another identity-provider error. Those
details cannot now be recovered without inventing evidence. The established
failure boundary is device-flow acquisition/result handling, before local OIDC,
Graph, registration checks or Azure key acquisition. Expiration is compatible
with the historical timing, but is not asserted as the proven original cause.

The installed MSAL implementation was inspected. It documents success via
`access_token` and failures via `error`, and polls until a terminal result or the
flow deadline. A locally expired polling loop can return its last pending error.
The new operator-only helper separates initiation, waiting, result validation,
OIDC verification, Graph correlation, registration and resource-key stages.
It saves only a closed allowlist of OAuth error codes, bounded integer AAD codes,
elapsed time and local flow-deadline status. It omits raw responses, descriptions,
tokens, correlation data, user codes and exception text from diagnostic artifacts.
No application authentication implementation was changed.

Seven isolated diagnostic tests passed in **0.001 seconds**, covering expired
and declined results, missing/malformed tokens, credential omission, unknown
error-text omission and bounded integer-code filtering. No signing or network
operation occurs in those tests. The new real device flow then completed
successfully after the operator reported completion; no replacement flow or
authentication bypass was needed.

## 2. Fresh identity and resource-specific credential

The existing pinned tenant, public client, API audience and `access_as_user`
scope were reused. `OIDCVerifier` checked RS256 against its configured JWKS,
exact issuer/audience, delegated Entra v2 purpose/scope and exactly
`PolyMind.L1Operator`. The verified principal matched the independent approval
trust, derived owner/tenant scope, enabled existing registration, user kind and
`PUBLICATION_MANAGE` permissions.

A second pinned-key signature verification obtained the signed `oid`; only
then was the exact Graph user queried. Graph's returned ID matched that signed
OID and `accountEnabled=true`. This completes the same-account correlation that
was unfinished in earlier preparation. No unverified token claim authorized an
identity, permission or management query.

The verified token expires at **9 November 2026, 00:11:34 UTC**. The named Azure
resource's keys API securely returned its current key. The generic `.env` key
was not used. Token, key and raw key response were not printed, placed in command
arguments, logged or written to files. Credentials remain in the preparation
process's memory. The independent artifact verifier did not reconstruct a
principal from unverified metadata or retrieve the secrets.

Resource-key correspondence follows from the exact resource-scoped management
query. Its **00:05 UTC use deadline is an explicit operator attestation**, not
an intrinsic or independently measured Azure API-key expiry. A later authorized
launch must recheck credential availability, identity lifetime and current
conditions; preparation creates no paid access authorization.

## 3. Current Azure and shared-consumer evidence

Read-only checks after authentication and again immediately before finalization
confirmed the expected enabled subscription/tenant, resource
`epolymind-foundry-dev-susanta`, deployment `epolymind-gpt-54-mini`, model
`gpt-5.4-mini` version `2026-03-17`, Spain Central, GlobalStandard and successful
provisioning. Deployment limits remain **30 RPM / 30,000 TPM**.

The reviewed public route remains enabled, with no resource private endpoint,
customer-owned storage attachment or diagnostic export settings. No new
contradictory evidence requiring financial re-investigation was found. No price,
billing profile, financial authority, deployment, quota or network setting was
changed. No exploratory provider call or model discovery was performed.

Current consumer-state reads show the PolyMind AKS cluster stopped, no container
instances and the other inventoried container application stopped. Local shared
admission has zero active/recent calls and no conflicting L1 launcher was found.
These observations cannot prove absence of external consumers. The operator
separately and explicitly confirmed that no AKS workload, container instance,
application, playground session, script, batch job or outside consumer will use
this deployment or shared quota. The subsequent window confirmation binds that
attestation to the reviewed period. No resource was started, stopped or deployed.

## 4. Governance, trust, source and deterministic plan

Read-only SQLite connections, `query_only=ON` and read transactions verified
schema/integrity, exact stored policy/catalog and the existing evaluation scope.
The selected overlay remains `polymind-evaluation/1`; seven historical
reservations remain SETTLED, with ten existing events and zero unsettled work.
Both scopes currently have:

| Capacity | Remaining |
| --- | ---: |
| Monthly tokens | 1,491,074 |
| Daily tokens | 500,000 |
| Rolling request slots | 16 |
| Outstanding-token capacity | 112,000 |
| Catalog-accounted EUR | 4.981094244984159248 |

The daily/request differences from 7 November follow normal UTC-day/rolling-window
semantics. No capacity reset, new allowance or policy change was performed.
The full approved contract allowance fits current headroom; no capacity is
reserved by these observations.

The approved financial Contract's exact serialization SHA-256 remains
`c5f6338684146f44abe763c794b6b872a23930d65548eefd87c5e2196935699d`.
Its current catalog, EUR 0.126634947709 aggregate extras, zero attributable fixed
cost under the approved exclusions, EUR 0.242439068181288 allowance and EUR 5
ceiling were reused unchanged. They retain the approved VAT/network budgeting
semantics and are not invoice or external hard-cap assertions.

Existing independent live RSA-3072 public trust matches the separate public PEM
and freshly verified operator. Public DER SHA-256 remains
`35785596dd2f38a3ae5fc8eeb93015a1ba3c8b4f16f06a1d73fbe521f9657816`.
Replay permissions/isolation and historical consumption records were checked
without mutation. Private-key correspondence/decryption remains a future
authorized signing step; no encrypted private-key content was read now.

The actual current planner rebuild reproduces one chunk and two dependent
reducers, followed by the local complete digest/publication and one Q&A call.
Plan SHA-256 remains
`e536899c1d871d4246d7751a258bcab7c9fd3e5a9cce1773e5001d24c416b030`.
Source evidence resolves exactly. Fresh rendering gives chunk G1 estimate
12,216 with 3,000 output reserved; the one-child reducer bound remains 17,032
including overhead/safety. Actual complete Q&A sizing must still pass before
call 4. No annotation/provenance truncation or accepted live checkpoint was
manufactured. The pinned embedding tree's eleven files match its prior digest;
no model was loaded or downloaded.

All twelve generation-source inventory files match committed HEAD. The current
generation contract is unchanged:

```text
de9492c536c1435464e8d9e406cbd1491ea358bc45f817df72eb2ea2a0f69a71
```

## 5. Explicit window and canonical final configuration

The operator expressly confirmed:

| Timing | UTC |
| --- | --- |
| Execution not before | 8 November 2026, 23:15 |
| Target launch by | 8 November 2026, 23:35 |
| Approval expiry | 9 November 2026, 00:05 |
| Operator-attested key use deadline | 9 November 2026, 00:05 |
| Verified identity-token expiry | 9 November 2026, 00:11:34 |

The canonical launcher's exclusive ten-minute cutoff is **23:55 UTC**. The
earlier target provides a thirty-minute margin to the approval/key deadline and
exceeds the extra twenty-minute preparation runway check. This provides room
for signing/verification, 183 seconds of minimum first-to-fourth start spacing,
provider/local work and settlement; passing time must still be checked at every
subsequent gate. No deadline may be silently extended if it becomes ineligible.

The seven pending fields were completed from their actual sources: token/key
resource verification, current Azure quota, local admission plus explicit
consumer exclusion, preserved approved financial readiness, and the explicit UTC
start/expiry/use-deadline confirmation. The prior candidate and preparation
packages were preserved rather than overwritten.

The new private `configuration.v5.reviewed.json` passed `load_configuration`.
Its canonical `configuration_digest`, independently repeated on the saved file,
is:

```text
d53a4a45f3d914ee85d703a6b6a848f047455b62dba725e57713b70f2311854d
```

This digest binds the exact new audit destination, approved financial contract,
current v5 generation, identities, authorities, limits and window. The original
failed-run configuration and consumed approval cannot authorize this plan.

## 6. Unsigned bindings and mandatory signing stop

`foundry_approval.bindings(config, principal, digest)` used the freshly verified,
sealed principal in the memory process. It wrote only unsigned JSON review data.
A separate process reopened the final configuration, independently recomposed
the full binding structure, compared its exact JSON types/values, checked the
operator against pinned trust and verified the preservation and timing evidence.
Saved configuration/binding review passed at approximately **23:05:45 UTC**.
No fake or metadata-reconstructed Principal was supplied to the verifier.

The bindings include exact canonical digest, issuer/subject/tenant/owner scope,
resource/endpoint/deployment/model/version/SKU/region, EUR 5 ceiling, fixed/extra
amounts, four-call/token/context/rate limits and approval epoch **1794182700**.
Full identity-bearing bindings remain in the private review artifact, not Git.
The intended signed-artifact filename is `approval.v5.four-call.jwt` in that same
private directory; it has not been created. A fresh approval UUID will be chosen
only during separately authorized signing, with the existing independent key and
replay authority.

**STOP: explicit RSA signing authorization is required for this exact digest,
binding, destination and expiry.** The authorization question is presented in
the final handoff. No passphrase dialog was opened. Even an affirmative signing
response will not authorize consumption or paid execution. After authorized
signing and independent saved-signature verification, a separate live-execution
authorization gate remains mandatory.

## 7. Private preservation, validation and repository disposition

The new isolated private directory contains **30 files** plus the empty
`four-call-audit` directory. Directories are 0700 and files 0600. It retains the
final configuration/digests, deterministic-plan identity, approved finance and
current governance/control-plane evidence, sanitized login outcomes, explicit
attestations, unsigned bindings, independent review, helper/test source and
per-file inventory. It contains no token, API key, raw key response, private key,
passphrase, signed approval, live marker or run ledger.

Before/after manifests preserve existing authority files, earlier v5 preparation,
public trust, original failed-run evidence and replay records. Replay filenames
and hashes are unchanged. No historical record was reset or reused. The new
audit directory is empty and independent from persistent replay storage.

Fresh validation consists of seven diagnostic tests, the successful real pinned
authentication and read-only Graph/resource/control checks, local authority/
source/embedding/plan/render checks, actual canonical configuration loading and
independent saved-binding verification. No full suite, application compilation,
Docker build or Kubernetes validation was needed; no application implementation,
dependency, prompt or schema changed. Implementation self-review checked secret
redaction, diagnostic closure, trusted signed-OID correlation, lifetime/window
runway, financial-contract identity, all seven prerequisite sources, audit/replay
isolation and exact canonical binding. Pre-commit review covers only the two new
Markdown records and excludes credentials, operator identifiers and raw provider
content. Documentation checks and `git diff --check` pass.

`git status --short --branch` shows `master...origin/master`, fifteen pre-existing
untracked Markdown files and these two new deliverables. `git diff --stat` and
`git diff --cached --stat` remain empty because no tracked or staged file changed.
No staging, commit, push or remote modification occurred.

**PREPARATION PASS — SIGNING AUTHORIZATION REQUIRED.** All preparation blockers
are resolved for the exact current artifacts and confirmed window. The remaining
gates are explicit RSA signing, successful saved-signature verification and
separate explicit paid-execution authorization with fresh prelaunch checks.
No live application acceptance or independent semantic quality is claimed.
