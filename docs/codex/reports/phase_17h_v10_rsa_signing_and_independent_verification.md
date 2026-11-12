# Phase 17H v10: authorized RSA signing and independent verification

11 November 2026 UTC. **READY_FOR_SEPARATELY_AUTHORIZED_LIVE_EXECUTION**.
Signing is complete; approval consumption and paid execution remain unauthorized.

## Exact authorization and unchanged packet

Susanta Hazra explicitly authorized one RSA-3072/RS256 signing operation for the
exact packet in the unchanged
[signing handoff report](phase_17h_v10_confirmed_operator_packet_and_rsa_signing_handoff.md).
That instruction separately prohibited approval consumption and Azure inference.

| Binding | Authorized and verified value |
| --- | --- |
| Configuration SHA-256 | `8e0be5429ea1e8c991338508c8b56731aa7a4ceec2ae662502236ef81c7d1e5b` |
| Unsigned-bindings SHA-256 | `e7aef1e7a0b272939b9b72bbe9e65bf25d542c67ff10084a1d339240957a2b3f` |
| Approval UUID | `861e0191-2e2a-4a77-be29-86414f7eed2f` |
| Generation | managed-prompt/10 |
| Generation SHA-256 | `e5fb249cc9b166b5e438f1534eb855fa5ab7531e08aa09314c110a1905327ebd` |
| Deployment | epolymind-gpt-54-mini |
| Financial ceiling | EUR 0.242439068182 |
| Execution not-before / target | 20:30 / 21:00 UTC |
| Effective strict launcher cutoff | Strictly before 21:04:59 UTC |
| Evaluation end | 21:30 UTC |
| Approval/credential/exclusivity end | 21:50 UTC |
| Actual application-token expiry | 21:52:02 UTC |
| RSA key ID | polymind-l1-35785596dd2f38a3 |
| Public DER SHA-256 | `35785596dd2f38a3ae5fc8eeb93015a1ba3c8b4f16f06a1d73fbe521f9657816` |

No configuration/binding byte, source/plan identity, authority, catalog, settlement,
policy or replay marker was changed. No replacement approval identity was created.

## Fresh checks and controlled signing

The prior management snapshot had reached its freshness boundary, so approved
read-only management/consumer/meter inspection was repeated. It passed at
**20:46:48 UTC**, confirming the same target, 30 RPM/30,000 TPM allocation,
known stopped workloads and pricing route. Current owner/tenant headroom still
fits the four-call forecast EUR 0.242439068181288 under the approved ceiling.
Thirteen historical reservations remain SETTLED, zero unsettled; admissions are
inactive. External exclusivity remains the operator's final attestation.

The established signing procedure was rebound to the exact v10 fingerprints,
existing proposed UUID and a new signing-attempt nonce. Following the historical
controlled stage-transition mechanism, the original unsigned-preparation
dispatcher and helper manifest were archived under their original hashes. A
separately pinned signing-stage dispatcher/manifest was installed in the existing
memory-session hook. The unchanged original packet inventory is checked against
those preserved originals; no equality check was omitted to accommodate the
transition. New temporary helpers pass syntax and critical Ruff checks.

At **20:47:27 UTC**, the independent actual-Principal pre-key checkpoint passed:
production Entra verification, enabled signed-OID/Graph correlation, registered
PUBLICATION_MANAGE, source ownership/analyze/delete checks, epoch zero, current
bindings/generation/plan/embedding, public trust, headroom and unused replay state.

Only after that checkpoint, the authorized signer opened the existing encrypted
private key. The operator entered its passphrase solely in the established masked
local Windows dialog. The decrypted RSA-3072 public component matched both the
independent public file and configured live trust. No passphrase, plaintext key,
access token or API key was displayed or written to a new file.

A fresh post-dialog actual-Principal checkpoint passed at **20:49:21 UTC** before
the one authorized signature. The signer checked its nonce, exact packet, unused
UUID, private/public trust correspondence, twenty-minute headroom, cutoff and
preserved authority bytes again. It then performed exactly **one RS256 signing
operation at 20:49:21 UTC**. Actual iat/nbf are that signing time; expiry is exactly
21:50 UTC. The decrypted key was discarded. No retry or replacement occurred.

## Saved artifact and independent production verification

The compact approval was exclusively saved in the protected location, mode 0600:

```text
/tmp/phase17h-v10-auth-packet-20261111/final-packet-20261111T1928Z/approval.v10.four-call.jwt
```

Signed-artifact SHA-256:

```text
c98ef7dfa7e5c35319f874c761647672dbc3721eedf5a54ee7b6b7571603e87d
```

At **20:49:35 UTC**, a separate process received the held token through an anonymous
pipe, freshly authenticated the actual Principal again, reopened the saved
artifact and called production `foundry_approval.verify_artifact()` with the
actual configuration/digest and independently provisioned live public trust.
RS256, exact key ID/header, issuer/audience/purpose, UUID, iat/nbf/exp, operator/
tenant/owner, model/deployment, financial ceiling and every canonical binding
passed. Saved bytes match the signing receipt's hash. No approval content was
printed. Result:
`RSA_APPROVAL_INDEPENDENTLY_VERIFIED_PAID_AUTHORIZATION_REQUIRED`.

The private `rsa-independent-verification.json` receipt, signing result, before-key
and post-dialog checkpoints remain alongside the artifact. The ten prior consumed
markers are unchanged; the new UUID has **no consumed marker**. The four-call audit
directory remains **empty**. There are no new reservations, settlements, checkpoints,
publication results or Q&A outputs. Paid provider calls attempted/accepted: **0/0**.

## Separate paid decision and remaining limits

The next required authorization is one controlled production-launcher invocation
for this exact configuration and signed-artifact fingerprints, the confirmed
window, existing UUID and maximum EUR 0.242439068182 exposure. It must explicitly
permit one-time approval consumption. At most four calls, concurrency one,
minimum 61-second starts, no automatic/manual retries under this approval, no
fallback and no additional schema probe remain mandatory. First terminal failure
ends the run without repair or an additional paid call.

Provider credential acceptance and exact live strict-schema acceptance remain
unverified; no separate probe was used. These can only be observed by the first
call of a separately authorized evaluation. Successful signing establishes
neither inference access nor model compliance/semantic quality. Before any later
launch, fresh identity/credential/signature, cutoff, resource/quota/consumers,
headroom and replay checks remain mandatory. Do not launch at/after the effective
cutoff or silently extend the confirmed window.

## Preservation and Git

Only this new sanitized report is added to the repository during this signing
task. All 537 pre-existing nonignored files, including earlier reports, remain
unchanged. Production/tests/generation files and the approved configuration are
unchanged. Temporary signing controls and receipts remain outside the repository;
no private-key or credential value is included here. Documentation secret/link
review and final preservation checks pass. No previous engineering audit or full
test suite was repeated.

Final Git state: zero tracked/staged modifications, 30 untracked Markdown documents.
`git diff --stat` and staged statistics are empty; `git diff --check` passes.

Git staging: **NO**. Git commit: **NO**. Git push: **NO**.
RSA signing: **YES — one explicitly authorized operation, independently verified**.
Approval consumption: **NO**. Live inference: **NO**. Paid provider calls: **0**.
