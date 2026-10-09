# Phase 17G operator contract

This is a trusted single-host reference implementation. It does not authorize
public-user exposure or establish a distributed production security database.
See the [phase report](../codex/reports/phase_17g_report.md) for verification scope
and outstanding acceptance gates.

## Authentication modes

`API_AUTH_MODE` accepts `disabled`, `static_bearer`, or `oidc_jwt`. Leaving it unset
preserves `API_AUTH_ENABLED`: false means disabled, true means static bearer.
Static bearer retains the existing minimum 32-character, whitespace-free token
requirement. Neither disabled mode nor a shared static token identifies a user.

For OIDC, set `API_AUTH_ENABLED=false` and completely **unset** `API_AUTH_TOKEN`.
An empty token variable is still configured and is rejected. Do not copy the
empty legacy token entry from `.env.example` into an OIDC configuration.
Conflicting modes fail settings validation. Production continues to require
authentication, disabled API documentation, external inference/Redis/Chroma,
and offline model artifacts under the existing deployment contract.

`OIDC_CONFIGURATION` is JSON matching `security.identity.OIDCSettings`:

| Field | Contract |
| --- | --- |
| `issuer` | Exact allowed HTTPS issuer |
| `audience` | Required API audience |
| `jwks_url` | Explicit operator-selected HTTPS trust anchor |
| `tenant_claim` | Required tenant claim; default `tid` |
| `roles_claim` | Issuer-controlled role array; default `roles` |
| `purpose_claim`, `purpose_value` | Required access-token discriminator; defaults `token_use`, `access` |
| `role_mapping` | Operator-approved mapping from issuer roles to application Action names; empty by default |
| `service_roles` | Trusted role names identifying service principals; empty by default |
| `cache_seconds` | JWKS freshness, default 300; maximum 3600 |
| `refresh_seconds` | Refresh cooldown, default 30; maximum 300 |
| `timeout_seconds` | Fetch timeout/deadline, default 3; maximum 10 |

The supported contract is RS256 with RSA public keys of 2048–8192 bits, an
explicit `kid`, and JWT or at+jwt header type. Signature, issuer, audience,
expiration, not-before, subject, tenant, and configured token purpose are checked.
An identity provider using another algorithm or purpose convention needs an
explicit compatible configuration/implementation; verification never falls back
to shared-token or anonymous access. This is access-token verification, not an
OIDC login/registration/refresh-token system.

JWKS responses are limited to 64 KiB and 32 keys. The verifier does not follow
redirects, use environment proxies, discover issuers, or fetch token-supplied key
URLs. Unexpected headers, including `jku`, `x5u`, embedded keys and critical
extensions, are rejected. Cached keys expire; unknown keys trigger only controlled
refresh. A removed key can remain accepted until cache expiration, so key rotation
and incident response must account for that window. Tokens and raw claims are not
logged. Verification uses [PyJWT's maintained decode/JWK interfaces](https://pyjwt.readthedocs.io/en/stable/api.html)
with cryptography; no custom signing or signature verification is implemented.

## Scope, ownership and sharing

Only the verifier issues immutable `Principal` objects. Canonical identity uses
the existing UUIDv5 helper with unambiguous JSON tuples and versioned domains:

```text
tenant = stable_id("polymind-identity/1/tenant", issuer, external_tenant)
owner  = stable_id("polymind-identity/1/owner", issuer, external_tenant, subject)
```

UUIDs provide stable names, not authorization. HTTP requests cannot supply a
trusted Principal or override canonical scope. Verified identities are registered
in `SecurityAuthority`; canonical Documents are registered through trusted
publication operators. Existing arbitrary legacy scopes are not automatically
claimed by new identities, and immutable artifacts are not relabelled.

Owners may read/analyze, share/revoke and tombstone their documents. Shared users
receive READ/ANALYZE only. Grantees must already be registered verified principals
in the same tenant; an arbitrary identifier is not proof of membership. Only
operator-approved issuer role mappings can grant tenant administration or
publication-management authority. A tenant administrator can disable a registered
principal through the trusted authority interface. No user-controlled role field
or public publication mutation endpoint is provided.

Authenticated routes include:

- `POST /documents/analyze`
- `POST /documents/{document_id}/shares` with `{"grantee_id":"<registered-owner-UUID>"}`
- `DELETE /documents/{document_id}/shares/{grantee_id}`
- `DELETE /documents/{document_id}`
- `GET /memory/{session_id}` and `DELETE /memory/{session_id}`
- `GET /usage` with bounded `limit` and `offset`

Sharing/deletion/usage routes require a verified principal even in legacy modes.
There is no upload, login, public job-admission or public publication endpoint.
`AuthorizedJobs` wraps trusted `DocumentJobs` for owner-scoped reads/cancellation;
`AuthorizedPublication` wraps explicit publication operations. Raw publication
service mutations require authorization when OIDC mode is active.

## Retrieval composition

The operator supplies an `AuthorizedAnalysis` instance on
`app.state.authorized_analysis`. Its registry maps canonical **owning**
`Scope.identity()` values to existing `DocumentAnalysis` instances. Each instance
must have its owner's read-only `PublicationReplica`, immutable object inventory,
job ledger, encoder, explicit capability profile and selected generation. Load
replicas explicitly before accepting traffic. No request constructs a filesystem
path or publication authority from client identifiers.

The registry's authority must be the same object as
`app.state.security_runtime.authority`. Use the runtime's governance ledger and
provider admission instance as well. Runtime construction uses the validated
settings below; the operator may construct it before lifespan to compose services.
The legacy opt-in `app.state.document_analysis` is not a substitute for authorized
analysis in OIDC mode.

Sharing resolves the owner's publication without copying documents. V1 rejects
mixed-owner document selections. Authorization occurs before generation pinning
and search. Dense filtering uses the existing generation/document filter;
generation identity already binds canonical owner scope. Publication/1 metadata
is retained exactly: no accepted vector row or manifest is migrated in place.
Authorized requests use per-document BM25 indexes built at replica load, so
unselected documents do not contribute BM25 scores/statistics. Legacy scoring is
preserved outside this authorized path. Secure scoring across selected documents
therefore differs intentionally from whole-corpus BM25 scoring.

RRF and reranking preserve record identity. Selected source integrity and
canonical citations are validated with the existing provenance rules. Grants,
document epochs, principal state, expiry and tombstones are revalidated before
return. Structurally valid provenance does not certify semantic entailment.

## Revocation and sessions

Grant changes and tombstones advance document security epochs independently of
publication history. Rollback cannot restore authorization. Principal changes
invalidate request snapshots. The middleware guards actual response release with
a local SQLite transaction serialized against authority mutations. A revocation
committed before release blocks protected output. Each guarded send has a bounded
five-second timeout; no database transaction spans inference. If a response has
already started, a denied later release terminates the body. Delivered bytes
cannot be recalled, and incomplete bodies are not successful completed answers.
This reference serialization can limit throughput and is not an AKS guarantee.

`ScopedMemory` wraps the existing file/Redis adapters. Its effective storage key
is SHA-256 over a versioned JSON tuple containing tenant, owner and visible session
ID. Reads, append and clear use that key and an authority guard. The visible ID
stays unchanged; internal keys are stripped from returned file-memory messages.
Old unscoped memory is never imported into authenticated namespaces. Document
analysis currently does not persist its answers in conversation memory.

**Legacy `/query` and `/query/stream` are disabled in OIDC mode**, before graph
routing, legacy retrieval, memory or inference. Direct graph helpers and factory
providers also fail closed. The legacy corpus has no proven private authorization
metadata, and the legacy generation APIs lack the required accounting bounds.
Local/static workflows retain their existing behavior. There is no new Streamlit
login or governed token-streaming capability.

## Required governance configuration

OIDC requires `GOVERNANCE_ENABLED=true`. Supply three distinct absolute paths in
existing private operator-controlled directories:

- `SECURITY_AUTHORITY_PATH`
- `GOVERNANCE_AUTHORITY_PATH`
- `GOVERNANCE_PROVIDER_PATH`

New SQLite files are private (0600). Obvious symlinks, hard links and incompatible
schemas are refused. Security/governance files also reject permissive file modes.
These adapters are trusted single-host references, not hostile-host sandboxes,
network-filesystem databases or independent copies for multiple AKS replicas.

`GOVERNANCE_POLICY` is a JSON `QuotaPolicy` with an explicit `version` and `owner`
and `tenant` Limits. Both levels require operator values for
`requests_per_window`, `window_seconds`, `interactive_concurrent`,
`background_concurrent`, `reserved_tokens`, `daily_tokens`, `monthly_tokens`, and
`monthly_cost`. There are no invented production allowances. Concurrency is
**inference-attempt concurrency**, not the count of queued/running document jobs.
Stored document count, bytes/pages, storage ceilings and total job concurrency
are not enforced by this v1 ledger and must not be advertised as implemented.

`GOVERNANCE_PRICING` is an operator-approved JSON `PricingCatalog`:
`version`, `currency`, `effective_date` (YYYY-MM-DD), `operator_approved=true`, and
`prices`. Each price contains `provider`, exact configured served `model`, decimal
string `input_price`/`output_price`, and `price_unit` (a decimal power of ten).
Prices are nonnegative and currency is catalog-wide. Missing model prices and
future-effective catalogs fail closed. No Azure/OpenAI/vLLM price is assumed.

Budgets use exact decimal arithmetic. Catalog/policy content is persisted and
must match on reopen. Online policy/catalog migration is not implemented. Do not
reset or replace the ledger to evade existing expenses or unsettled reservations;
an operational migration must preserve those obligations before changing policy.

`GOVERNANCE_PROVIDER_KEY` identifies the actual shared upstream quota, and
`GOVERNANCE_PROVIDER_POLICY` uses the existing Phase 17E `AdmissionPolicy` schema.
All participating local workers must share that provider authority. Unrelated
external consumers remain outside application quota enforcement.

## Execution and reconciliation

`GovernedExecution` composes:

```text
authorization -> atomic owner+tenant reservation -> Phase 17E admission
              -> bounded execute -> usage settlement -> final authorization
```

Input estimates conservatively count serialized JSON bytes plus configured
overhead/safety allowance; output uses an explicit provider bound. These are
reservations, not authoritative actual tokens or a guaranteed upstream bill cap.
Each job/step/attempt is uniquely accountable. Duplicate admissions return the
same ticket but cannot claim execution again. Genuine retries require a distinct
attempt and remain scheduled by Phase 17C.

Before provider execution, both quota levels are checked in one transaction.
Provider-admission rejection releases unspent reservation; once execution may
have started, errors/cancellation retain known expense or unknown reservations.
Measured input and output settle once under the recorded catalog. Partial or
absent usage remains UNKNOWN with reserved cost/tokens retained across restart
and period boundaries. No TTL silently refunds it. Crashes before settlement
retain their durable state; trusted reconciliation needs external evidence.
The low-level ledger `settle` operation accepts trusted measured usage, including
later completion of UNKNOWN records; it is never an HTTP mutation endpoint.
Abandoned RESERVED/ADMITTING records require operator investigation; there is no
automatic crash-recovery release daemon.

For managed digestion, supply `ManagedSynthesisInference(..., governance=...)`
with an owner-bound `GovernedExecution`, an owner-only document snapshot
(`DOCUMENT_DELETE` action), and the same provider admission authority. The handler
checks job owner/document binding and retains its original lease/fence and
checkpoint rules. The principal must remain valid; long-lived delegated job
credentials are not implemented. Missing governed context refuses execution.

An owner reads only their records through `/usage`. Trusted tenant administrators
may use `tenant_usage` for aggregates, without another owner's call details.
Budget denial does not change model, retry rapidly or clear prior expense.
Governed provider text/stream methods are refused; streaming characters are never
reported as measured tokens.

## Retention, audit and readiness

Deletion atomically records DELETE_REQUESTED and TOMBSTONED, revokes grants and
denies subsequent access. Trusted `track_purge` records content classes requiring
reconciliation: source, extraction, checkpoints, retained manifests/vectors,
temporary objects and conversation references. Its persisted result is
**PURGE_PENDING**, with an explicit missing-inventory/delete-adapter reason.

The current immutable ObjectStore and vector port cannot prove complete safe
per-document deletion across shared references and retained generations. No
objects, collections or shared artifacts are deleted, and PURGED is never claimed.
Tombstones and audit records survive this pending state and publication rollback.
No deletion from backups, upstream providers or unintegrated cloud storage is
certified. Legal holds and automatic retention scheduling are not implemented.

Audit events are content-free, bounded and append-only within configured capacity.
They record opaque identity/resource IDs, allowlisted actions/outcomes and policy
version; no prompts, answers, JWTs, source text or embeddings. Capacity exhaustion
fails closed rather than silently discarding audit history. Mutations and their
required audit entries share a transaction. No tamper-proof/compliance-certified
logging claim is made. Detailed accounting is not placed in Prometheus labels.

`/health` remains independent liveness. `/ready` retains existing dependency gates
and additionally requires configured authorized publications, usable authority
databases, available audit capacity and a fresh verified JWKS cache. Missing
security components deny serving. The final added readiness paths have an
explicit verification gap recorded in the report; no live IdP check was run.

Live Azure Foundry document-digestion validation remains **BLOCKED / PENDING**.
Phase 17H reliability/quality certification and Phase 17I external verification
remain future gates; this work authorizes neither.
