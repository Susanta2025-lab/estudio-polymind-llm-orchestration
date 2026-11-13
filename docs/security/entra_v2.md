# Microsoft Entra v2 access tokens — Phase 17H-L

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
