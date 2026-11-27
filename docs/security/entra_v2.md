# Microsoft Entra v2 access tokens — Phase 17H-L

Current Phase 19B evidence: [27 November identity and operational review](../codex/reports/phase_19b_operational_evidence_reconciliation_and_gate_a_readiness_review.md).
Earlier dated findings below retain their original scope; actual browser/API acceptance is pending.

## Phase 18 browser-authentication distinction — 14 November 2026

The [Phase 18 local Documents application](../operations/phase_18_local_document_demo.md)
now has verified native Streamlit authorization-code/PKCE login through a
**loopback development issuer**, followed by server-verified API access tokens
and explicit owning-operator enrollment. It does not use this Entra profile and
does not establish real Azure Entra browser authentication. The configuration
below remains the existing separate access-token verifier contract. Real tenant
redirects/consent/assignment, browser token acquisition, enrollment, cookie/session
posture, network and deployment evidence require a separately reviewed plan.
Neither a working local login nor historical Entra launcher verification grants
publication, financial or paid-execution authority to a new browser deployment.

The existing OIDC verifier supports an explicit `entra_v2` profile for a single
Microsoft public-cloud tenant. Generic `oidc` remains the default and retains its
required `token_use=access` discriminator and configurable role mapping. The server
selects the profile; token claims never select a verifier or a trust URL.

Status — 12 November 2026: the [v11 execution report](../codex/reports/phase_17h_v11_controlled_live_execution_and_reconciliation.md)
records separately authorized live identity preparation and a successful four-call
Azure workflow. No-live statements below describe the original implementation
task. Authentication remains separate from domain permissions, financial approval
and independent RSA execution approval. The
[completion decision](../evaluation/phase_17_engineering_completion_and_deferred_acceptance.md)
records `PHASE_17_ENGINEERING_COMPLETE`,
`DEFERRED_PENDING_TWO_INDEPENDENT_REVIEWERS` (0/2),
`PHASE_17_FORMAL_CLOSURE_PENDING` and `NEXT_PHASE_DEVELOPMENT_PERMITTED`.
Production identity deployment is not established.

## Private .env configuration

Use this block in the application's private `.env`. Replace every
`11111111-1111-4111-8111-111111111111` with the **directory tenant UUID**, and
`22222222-2222-4222-8222-222222222222` with the **PolyMind API registration's
Application (client) ID**. These sample identifiers are synthetic, not credentials.
Use canonical lowercase hyphenated UUIDs. Keep the JSON on one line.

```dotenv
API_AUTH_MODE=oidc_jwt
API_AUTH_ENABLED=false
API_DOCS_ENABLED=false
OIDC_CONFIGURATION='{"token_profile":"entra_v2","tenant_id":"11111111-1111-4111-8111-111111111111","issuer":"https://login.microsoftonline.com/11111111-1111-4111-8111-111111111111/v2.0","audience":"22222222-2222-4222-8222-222222222222","jwks_url":"https://login.microsoftonline.com/11111111-1111-4111-8111-111111111111/discovery/v2.0/keys"}'
GOVERNANCE_ENABLED=true
```

**Remove `API_AUTH_TOKEN` entirely** from both `.env` and the process environment;
an empty assignment is also rejected. Retain the existing approved values for
`SECURITY_AUTHORITY_PATH`, `GOVERNANCE_AUTHORITY_PATH`, `GOVERNANCE_PROVIDER_PATH`,
`GOVERNANCE_PROVIDER_KEY`, `GOVERNANCE_POLICY`, `GOVERNANCE_PRICING`, and
`GOVERNANCE_PROVIDER_POLICY`. The three paths must be distinct absolute paths to
the intended private authorities. Quotas, prices and admission policy cannot be
invented to make startup pass. See the [governance contract](phase_17g.md).

Do not add `role_mapping`, `service_roles`, or custom claim mappings for this
profile. They cannot override the fixed Entra contract. The existing cache,
refresh and timeout settings remain available. No client secret is required to
verify tokens. Never save access tokens, private keys or client secrets in tracked
files. This change documents configuration; it does not alter the real `.env`.

## Issuer-side prerequisites and client request

The API registration must already issue v2 access tokens
(`api.requestedAccessTokenVersion=2`), expose the delegated `access_as_user` scope,
and define the user app-role value `PolyMind.L1Operator`. The operator must have
that role assigned on the PolyMind API enterprise application, and the client must
have delegated permission/consent. Request `<API Application ID URI>/access_as_user`
(normally `api://<API-client-UUID>/access_as_user`) through an approved interactive
user flow. Send the resulting **access token** as `Authorization: Bearer ...`.
The API audience setting is the API client UUID, not its `api://` scope URI, the
login client's ID, Microsoft Graph, Azure management, or Azure inference audience.

These claim conventions follow Microsoft's [access-token claims reference](https://learn.microsoft.com/en-us/entra/identity-platform/access-token-claims-reference).
The issuer must be the tenant-specific `/v2.0` URL; `common`, `organizations`, v1
issuers, sovereign clouds and app-only/client-credentials tokens are outside this
profile. This task does not create or change any Azure registration, consent or
role assignment, and does not acquire a live token.

## Verification and permission boundary

RS256 signature verification uses only the configured tenant-specific HTTPS JWKS
endpoint, with the existing size, key-strength, caching, refresh and timeout bounds.
No discovery, redirects, proxy inheritance, token-supplied URLs or embedded keys
are accepted. If a JWKS key supplies issuer metadata, it must match the configured
issuer or the standard tenant template, per Microsoft's [signing-key guidance](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens).

The verifier requires exact issuer, scalar API audience, matching `tid`, `ver=2.0`,
nonempty subject, integer `iat`/`nbf`/`exp`, valid lifetime without clock leeway,
and an exact space-delimited `access_as_user` scope. It rejects missing scopes,
app identities, conflicting `token_use`, and tokens without the assigned role.
Only `PolyMind.L1Operator` is accepted in the role array; additional unknown roles
are rejected. ID tokens lack the required delegated API scope; `typ=JWT` alone
does not distinguish an access token. An ID token's role does not grant access.

`PolyMind.L1Operator` maps only to `PUBLICATION_MANAGE`, the additional permission
required by the existing L1 workflow. It grants no `TENANT_ADMIN` or service
identity. Existing owned-resource read/analyze/share/delete and own-session rights
remain enforced by `SecurityAuthority`; this role is not a new read-only sandbox.
Existing publication tenant/owner checks, revocation, audit, quotas, pricing and
provider admission continue to apply. Identity remains `(issuer, tid, sub)`;
email, display name, groups, `oid`, and caller-supplied owner fields cannot remap it.

## Remaining L1 authentication gates

The launcher's private JSON `oidc` object must use the same settings as
`OIDC_CONFIGURATION`; the launcher reads that object, not the application's `.env`.
Its `owner_scope` must match the verified principal, and that principal must already
be registered and enabled in the existing security authority. Changing the profile
changes the configuration digest: obtain a new reviewed approval, never reuse an
old signed configuration hash.

The live launcher now requires a **separate operator-signed approval artifact**,
verified against an independently provisioned local RSA public-key trust policy.
The `polymind_l1_approval` JWT claim is no longer consulted. Entra authentication
still requires the same scope, role, issuer, audience, tenant and lifetime checks.
See the [approval procedure](../evaluation/phase_17hl_operator_approval.md) for the
artifact binding, `--approval`/`--approval-trust` inputs and durable replay guard.

Actual tenant/API identifiers, assignments/consent, token acceptance, JWKS egress,
authority registration and token lifetime remain deployment checks. Provisioning
a trusted operator signing key and obtaining a reviewed, unexpired live approval
are separate prerequisites. No live authentication or Azure inference was
performed. Financial and other L1 gates in the
[runbook](../evaluation/phase_17h_foundry_validation.md) remain mandatory.

## Phase 17I operator reuse — 13 November 2026

The [bounded Phase 17I workflow](../evaluation/phase_17i_operator_workflow.md) reuses an existing verified operator `Principal` and publication authority. A participant study code is a private approval-record identifier, not an Entra principal or login credential. Never share the `PolyMind.L1Operator` role, token, device-code session or host control with participants. [Engineering/documentation completion](../evaluation/phase_17i_engineering_completion_and_deferred_acceptance.md) grants no new identity enrollment, external participation or provider-execution authority; those remain separately gated. This task changes no issuer configuration or authentication contract.

## 26 November 2026 — Phase 19B native browser OIDC preparation

The operator reports the dedicated single-tenant Streamlit Web registration, exact private
callback acceptance, enabled browser service principal, API delegated permission, persisted
Principal-only consent and confidential credential metadata complete. API role assignment
remains operator-reported PASS. Tenant-wide consent is not granted; no Graph scopes or consent
expansion is required. Historical pending statements retain their original date/scope.

The [current preparation report](../codex/reports/phase_19b_streamlit_oidc_configuration_preparation.md)
contains exact non-secret browser/API identifiers and the operator-only private provisioning
procedure. Native Streamlit's client ID is the browser application's; the verifier audience
remains the API client UUID. Scope URI, object IDs, directory oid and ID-token subject cannot
substitute for API audience or API access-token sub. Enrollment remains
`[issuer, tenant UUID, API access-token sub]`; actual sub is UNKNOWN. No production enrollment
was created. Actual credential custody/encryption/validity and real browser/token acceptance
remain unverified; no secrets, operational cookies/configuration, login or Entra mutations
were performed by Codex. Authentication continues to grant no independent execution or
financial authority. The portable template and verifier contract are unchanged.


## 27 November 2026 — Operational preparation and identity-bootstrap limitation

The [current operational review](../codex/reports/phase_19b_operational_evidence_reconciliation_and_gate_a_readiness_review.md)
records OPERATOR_REPORTED_PASS for native OIDC TOML preparation, independently generated
cookie, GPG encryption/content comparison and redundant plaintext removal, in addition to the
previous registration/permission/principal-consent/credential metadata. Private values were
not accessed by Codex. Local encryption does not establish credential validity, independent
recovery custody or an Entra token exchange. Preserve the cookie across ordinary restarts.
Windows current-user trust/hostname resolution and PKI issuance are reported local configuration
passes; actual private browser authentication/API-token claims remain PENDING/BLOCKED.

Exact enrollment remains [issuer,tenant UUID,API access-token sub]. The production manifest
requires it and an owner-bound source before initialization, while standard Compose starts UI
only after API health. Middleware registers already verified principals after API construction;
it cannot acquire the missing pre-initialization subject. OIDCVerifier can validate an acquired
API token independently but does not acquire one. No supported native identity-only bootstrap
workflow exists. Review a narrowly scoped maintenance implementation separately; do not use
ID-token sub/oid, placeholder enrollment, fixture auth, debug claim dumps or production-state
initialization as a workaround. No authentication/authority rule changes in this review.

Execution-disabled startup is conditional on legitimate full inputs and does not solve this
bootstrap. All source/privacy/review/provider/financial/shared-admission and independent live
execution gates remain separate. Manual private-PKI revocation risk and independent recovery
custody also remain open. No actual Entra login/token acquisition, registration mutation,
Azure/SSH, provider request, production initialization or execution approval was performed.
Gate A BLOCKED; 19A COMPLETE; 19B ACTIVE; 19C NOT_STARTED. Next: offline operator review.


## 27 November 2026 — Isolated local identity bootstrap implementation

The [maintenance utility](../../deployment/phase19/identity_bootstrap/core.py) now reuses
OIDCVerifier without production initialization and checks `azp` against the dedicated browser
client only after the exact API token passes cryptographic production verification. Existing
production verifier semantics are unchanged. It uses verified Principal.scope for the existing
versioned canonical IDs and explicitly exports unsigned sensitive enrollment-candidate evidence,
never tokens, enrollment or execution authority. There is no ID-token/directory-oid fallback.

Follow the [operator-only runbook](../operations/phase_19_identity_bootstrap.md) for a separate
ephemeral bootstrap cookie, private native configuration, exact origin/TLS, approved external
evidence path and complete logout/browser-site/process/plaintext cleanup. Streamlit token
cookies are signed, not encrypted; logout does not establish provider-token revocation.
The [report](../codex/reports/phase_19b_local_identity_bootstrap_utility.md) distinguishes offline
synthetic verification from still unauthorized actual Entra acceptance. Production cookie,
credentials, registrations, authorities and execution gates remain unchanged. Gate A BLOCKED.
