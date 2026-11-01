# Phase 17H-L separate operator approval

Status — 1 November 2026: [Attempt 6 is CLOSED/PASS](../codex/reports/phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md)
for one application-accepted analysis with settled usage and zero automatic
retries. Its approval is consumed. No current authorization is conveyed by this
procedure; earlier zero-spend statements describe the implementation task. Full
live L1 digestion and grounded Q&A remain NOT VALIDATED; Phase 17H remains PARTIAL.

The L1 launcher verifies two independent signatures: the identity provider's
access-token signature authenticates the operator; a separately trusted operator
key approves the exact execution plan. Neither credential substitutes for the
other. The issuer no longer needs to emit `polymind_l1_approval`. Generic OIDC and
strict [Entra v2 authentication](../security/entra_v2.md) retain their contracts.

This document describes an operator-controlled procedure, not permission to run
L1. Current authorized spend remains zero. No signing key, live approval or Azure
request was created during implementation.

## Independent signing trust

Provision a private, operator-owned JSON file outside the repository, mode 0600.
Its schema is `ApprovalTrust` in `tests/performance/foundry_approval.py`:

```json
{
  "version": "polymind-approval-trust/1",
  "purpose": "live",
  "key_id": "operator-key-version",
  "public_key_pem": "<independently verified RSA public PEM; JSON-escaped newlines>",
  "operator_issuer": "<exact verified token issuer>",
  "operator_subject": "<exact verified sub, not email or oid>",
  "operator_tenant": "<exact verified tid>",
  "replay_directory": "/private/persistent-l1-approval-consumption"
}
```

This is a schematic example, not a loadable trust file. The trusted administrator
must verify the public-key fingerprint and its association with the named operator
through an independent channel. Never obtain a trusted key from the approval
artifact, its header or its sender's unverified configuration. The launcher uses
only this pinned key; no network key discovery, embedded keys or key URLs exist.
Only RSA public keys of 2048–8192 bits are accepted; private PEMs are rejected.
Keep the private signing key under the operator's control outside the launcher.
Use an existing approved signing process; no key generation/signing command is
part of live execution.

Pre-create the replay directory outside the repository, mode 0700, owned by the
launcher operator. It must be independent of the per-run audit directory (not that
directory or a descendant). Provision it once and retain it across launches and
key rotation. The trust file is separate from `LaunchConfiguration`, and the
signed artifact cannot select or replace this directory or its verification key.
Protect the trust file and its containing directory against untrusted writers.

There is no built-in production key, test-key allowlist or `--allow-test` option.
Both artifact and trust policy must explicitly say `purpose=live`; `test` is
rejected even with a valid signature. Tests use ephemeral keys in isolated offline
fixtures. Administrators must never provision fixture keys as live trust: a
verifier cannot discover that an administrator mislabeled a key's provenance.

## Review and sign the exact artifact

1. Prepare the private launch configuration using the existing
   [L1 runbook](phase_17h_foundry_validation.md). Reuse the real security,
   governance and admission authorities. Validate it using `load_configuration`
   and retain its returned configuration digest. Financial contract approval
   booleans alone do not authorize execution.
2. Authenticate the operator through the configured verifier. Confirm exact
   issuer, subject, tenant and derived owner scope, assigned role/scope,
   registration and authorization. Do not derive identity from unverified JWT
   decoding. The trust file must name this same authenticated operator.
3. Prepare unsigned review material using
   `foundry_approval.bindings(config, verified_principal, digest)`. This helper
   only produces data; it does not sign or approve. Review the entire validated
   configuration as well as the explicit bindings. Copy the resulting object
   unchanged into the `binding` field below. Monetary strings must preserve the
   validated serialization; do not round or reformat after review.
4. The authorized operator decides whether to sign. A refusal leaves execution
   blocked. Use a fresh canonical UUID for `jti`, integer UTC epoch seconds for
   `iat` and `nbf`, and `exp` exactly equal to `config.approval_expires` and
   `binding.expires`. Require `iat <= nbf < exp`, no future validity start, and at
   most 24 hours from issue to expiration. The launch configuration still requires
   approval/credential validity exceeding ten minutes at launch; the authenticated
   token must have more than a request-minute remaining.

The compact JWS has this protected header (no other header fields are allowed):

```json
{"alg":"RS256","typ":"polymind-approval+jwt","kid":"operator-key-version"}
```

The signed JSON payload has exactly these fields:

```json
{
  "iss": "polymind-operator-approval/1",
  "aud": "polymind-l1-live",
  "jti": "<fresh canonical UUID>",
  "iat": "<integer epoch seconds, not a string>",
  "nbf": "<integer epoch seconds, not a string>",
  "exp": "<integer epoch seconds, not a string>",
  "purpose": "live",
  "binding": "<object returned by bindings(), not a string>"
}
```

These placeholders are intentionally invalid. The
[approval template](phase_17h_foundry_approval.template.json) contains the expanded
unsigned payload and trust shapes, defaulted to `purpose=test` with unset fields.
The binding contains exact configuration digest, operator identity/owner scope,
resource, endpoint, deployment, model/version, SKU and region, currency and spending
ceiling including fixed/additional costs, per-request and total input/output token
limits, attempt/rate/TPM/context limits and expiration. The configuration digest
additionally binds all prices, quota policies, authority locations, inference
options, local artifact hash and other launch fields.

Sign these JSON claims as a standard compact JWS with RSASSA-PKCS1-v1_5/SHA-256
(`RS256`). For an approved offline Python signing process using the existing PyJWT
library, the signing operation is `jwt.encode(reviewed_payload, operator_private_key,
algorithm='RS256', headers=reviewed_header)`. This is performed by the operator,
not the launcher or this implementation task. No custom JSON canonicalization is
required for signing: JWS signs its encoded payload bytes. The verifier compares
all decoded bindings with the validated plan, with exact JSON types/values.

Store only the resulting compact JWS in an operator-owned 0600 artifact outside
Git. Do not place the private key, access token or Azure credential in that file.
The launcher bounds artifact/trust input sizes and rejects unsigned JSON, expired
or mismatched artifacts, forged signatures, unknown keys, unexpected headers and
test-purpose artifacts/trust.

## Launch handoff and replay behavior

After independent approval and all existing prerequisites, the CLI inputs are:

```text
python -m tests.performance.foundry_l1 --live
  --configuration /private/l1-config.json
  --approve-sha256 <validated-configuration-digest>
  --approval /private/operator-approval.jwt
  --approval-trust /private/approval-trust.json
```

This is schematic argument documentation, not an instruction to execute now.
Runtime secrets remain the separate `POLYMIND_L1_OPERATOR_TOKEN` and
`POLYMIND_L1_AZURE_CREDENTIAL` environment variables. The default command without
`--live` remains a network-forbidden rehearsal. Old live invocations lacking the
new approval/trust inputs deliberately fail closed. `LaunchConfiguration` and
its digest format are unchanged; no migration or replacement of existing
security/governance/admission ledgers is needed. Old custom JWT claims have no
approval authority. Existing legacy run markers still block reuse.

Before local preparation/provider creation, the launcher exclusively creates
`<approval UUID>.consumed.json` in the trusted replay directory and fsyncs both the
file and directory. The record stores only approval ID, key ID, artifact hash and
configuration hash. The existing exclusive per-run `live-started.json` and call
records remain additional barriers. Exactly one concurrent consumer can succeed.
Resigning or rotating keys cannot reuse the same approval ID; modifying the plan
invalidates the original artifact, and a fresh audit directory does not reset
central consumption. Do not create new approval IDs merely to retry outstanding
financial work: a new authorization requires operator review and reconciliation.

Partial writes, preparation failures, unknown usage, timeouts and crashes consume
approval conservatively. Never delete markers, replace ledgers or switch replay
trust directories to retry. Investigate and reconcile retained obligations before
seeking any new authorization. The scheduler retains expiry/cancellation checks
before later calls and the existing no-retry behavior. Replay protection assumes
a trusted single host and persistent local filesystem; it does not resist an
administrator deleting/restoring state or coordinate independent hosts.

Current local identity/authority, trust/replay and embedding readiness evidence
is consolidated in the [final readiness report](../codex/reports/phase_17h_live_preflight.md#final-technical-readiness-and-l1-handoff--2026-10-14).
Reuse those existing artifacts; do not reprovision them. Remaining external
attestations cover credential validity/access, Azure RPM/shared consumers,
commercial source/charge bounds, retention and independent key provenance, plus
the final reviewed configuration, fresh identity and actual signature. Custom
Entra approval-claim issuance is not required. L2 restrictions remain unchanged.

## Single-analysis timing and preparation handoff

This section applies to `tests.performance.foundry_single_call`, whose approval
audience is `polymind-single-analysis-live`. Historical configurations and approvals
are unsuitable after executor changes. Do not run historical packet signing scripts
or alter their pinned digests to reuse them.

**Launch strictly before `min(approval_expires, credential_valid_until) - 600 seconds`.**
The exact cutoff is ineligible. Approval expiration alone is not the launch deadline.
For example, a 00:39–01:09 Lisbon window with the same credential-use deadline
requires launch strictly before 00:59 Lisbon. UTC is the authoritative display;
local conversion must account for the date's UTC offset.

Offline review (no authentication, signing, consumption or inference):

```text
python -m tests.performance.foundry_single_call --configuration /private/new-config.json
```

The JSON `execution_window` contains UTC start, approval expiration, credential-use
deadline, exclusive `launch_before_utc`, required 600-second margin, review time,
remaining launch seconds and `window_eligible`. Null deadlines yield no eligible
window. Eligibility describes timing only, not authorization or capacity. For API
keys, credential-use deadline is an operator attestation, not measured key expiry.
Time continues to pass after review; the launcher checks again. The independent
operator token must also satisfy existing identity and signed-approval checks.

Use this order for a future separately authorized attempt:

1. Complete static validation and inspect configuration, limits and implementation bindings.
2. Confirm the existing operator-controlled key path is known locally:
   `<PRIVATE_SIGNING_DIRECTORY>/operator-private.pem` (a symbolic private location,
   not a shell variable or instruction to create or relocate a key).
   Keep this path ready to paste into the operator-only prompt; do not export key contents.
3. Prepare and verify non-expiring fixture, schema, trust and public-fingerprint artifacts.
4. Obtain fresh authentication and credential-validity evidence under separate authorization.
5. Finalize fresh window/capacity attestations with the existing offline
   `--attestations /private/fresh.json --output /private/new-final.json` workflow.
   Review the exact resulting configuration digest and displayed launch deadline.
6. Independently sign with the existing RSA key after explicit operator confirmation.
   The operator-controlled signer must verify the pinned public-key fingerprint,
   use hidden passphrase input, and verify that the key's public fingerprint matches
   before signing. Never put a passphrase in arguments or environment variables.
7. Verify the signed approval against the reviewed configuration and pinned public trust.
8. Check remaining eligible launch time using the offline review command above.
9. Only after explicit operator authorization, invoke the one-call launcher once with
   `--live`, `--configuration`, `--approve-sha256`, `--approval`, and `--approval-trust`.

The inspected historical signer pins a particular packet, digest and 1,800-second
window; it remains unchanged. Preparing the reusable path in step 2 removes the
need to locate it during the live window without changing independent signing.
The generic single-call finalizer accepts explicit integer timestamps, not a duration
flag. A future reviewed configuration may select timestamps within existing policy:
RSA `exp - iat` must be at most 86,400 seconds, `iat <= nbf < exp`, credential validity
must be adequate, and the 600-second margin remains mandatory. The historical signer
cannot be reused for a different duration. No automatic 60-minute extension exists.

Failure output uses closed stages/categories without exception text. Early failures
report provider attempt `NO`; failures after entering execution report `UNKNOWN`
unless existing run evidence establishes more. Optional `preflight-diagnostic-*.json`
files are private observations, distinct from `live-started.json` and `outcome.json`.
They do not authorize execution or consume approval. `approval_consumption_entered`
means that consumption was entered, not proof it completed; consult the existing
replay authority. An unsafe/unavailable audit path yields console diagnostics only.
Never remove replay markers or treat diagnostic presence as permission to retry.
