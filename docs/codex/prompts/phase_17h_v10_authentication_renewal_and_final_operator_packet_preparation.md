# Codex Task — Phase 17H v10: Authentication Renewal and Final Operator-Packet Preparation

Task supplied by the operator on 11 November 2026. This clean task record preserves
the requested objective, stages, numerical bindings, restrictions and subsequent
operator decisions. It contains no credentials or authentication user code.

## 1. Objective

Complete the remaining authentication renewal, financial confirmation,
exclusive-window preparation and execution-packet preparation for Estudio PolyMind
Phase 17H v10. The completed engineering assessment is the baseline; the principal
remaining blocker is current application authentication.

Responsibilities:

1. Renew and verify Microsoft Entra application authentication using the established
   MSAL device-code workflow.
2. Verify operator identity, registration, permissions and source scope.
3. Verify whether an approved Azure Foundry inference credential can be supplied.
4. Reconfirm current Azure, shared-consumer and operational conditions.
5. Reconcile verified EUR pricing with the proposed v10 allowance.
6. Establish requirements for a fresh exclusive execution window.
7. Prepare exact v10 source, plan and canonical configuration through existing
   authorized preparation mechanisms, only when prerequisites permit.
8. Validate the proposed operational packet without paid inference.
9. Determine whether the packet is ready for independent RSA signing.

Do not perform RSA signing or live paid inference. Do not restart the completed
architectural review, redesign v10, or bypass authorization, replay, security or
financial controls. Follow AGENTS.md.

## 2. Verified engineering baseline

Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`, branch `master`.
Verified commit: `ec22fa3d116696b80a1bb12ad17e2eb37db38cb3`.
Current generation: `managed-prompt/10`, inventory `generation-inventory/2`.
Expected generation SHA-256:
`e5fb249cc9b166b5e438f1534eb855fa5ab7531e08aa09314c110a1905327ebd`.
GitHub Actions run `42817169571`: 2,595 tests passed. Earlier focused readiness:
749 passed; subsequent final operator verification: another 31 focused passes and
a successful synthetic four-call rehearsal.

These observations do not authorize live inference. Reverify current source and
generation fingerprints before operational preparation. Do not modify the
generation contract or historical fixtures.

## 3. Required references and source inspection

Read completely:

1. `AGENTS.md`.
2. `docs/codex/reports/phase_17h_v10_final_operator_verification_and_conditional_live_execution.md`.
3. `docs/codex/reports/phase_17h_v10_operator_preparation_and_readiness_assessment.md`.
4. `docs/codex/reports/phase_17h_v10_application_owned_evidence_and_lineage_implementation.md`.
5. `docs/adr/phase_17h_v10_generation_wire_receipt_decision.md`.
6. `docs/evaluation/phase_17h_foundry_validation.md`.
7. Existing v8/v9 historical authentication, signing, financial and execution-window reports.

Inspect the existing MSAL device-code helper, Entra verifier, SecurityAuthority,
principal registration, `foundry_l1.py`, `foundry_preflight.py`,
`foundry_approval.py`, protected configuration requirements and read-only
governance/admission facilities. Recover real commands and configuration from
code/evidence. Do not invent flags, keys or alternative authentication workflows.
Historical reports are references, not current authorization.

## Stage A — authentication renewal

### 4. Precise existing failure

The previous 11 November report found Azure management authentication available,
successful Foundry deployment inspection, an application token rejected by
production verification, an untrusted expired-token diagnostic, enabled registered
principal with PUBLICATION_MANAGE and epoch zero, and absent
`POLYMIND_L1_AZURE_CREDENTIAL`. No fresh authentication or credential acquisition
was performed.

Determine the actual failure. Distinguish expiry, issuer, audience, delegated
scope, role, signature, JWKS/trust, tenant/subject, disabled/revoked operator and
configuration mismatch. Do not assume expiry is the only cause. Never derive a
trusted Principal from an unverified JWT.

### 5. Authorized interactive renewal

The operator authorizes initiation of the existing interactive MSAL device-code
authentication workflow for this preparation task. Identify its helper, verify
the configured tenant and client/API audience, and confirm production delegated
scopes before initiation. Allow the operator to complete authentication through
Microsoft's official browser interface and wait for the helper's result.

Do not bypass MFA, conditional access, consent or device requirements. Do not
switch tenants/apps to bypass verification or automatically retry a meaningful
security rejection. Display only the normal Microsoft verification URL/user code
through the intended interface. Do not simulate approval or modify the helper.

Keep tokens in memory where the established workflow supports it. Never print,
log, commit, embed in Markdown, put in command history, send to unrelated services,
or persist tokens in unapproved caches. If the helper necessarily uses a protected
cache, inspect and honor that contract rather than inventing persistence.

### 6. Production token verification

Use actual production verification for RS256, issuer, audience, tenant, subject,
expiration, not-before, issued-at, delegated `access_as_user`, exact
`PolyMind.L1Operator`, owner/tenant mapping, enabled registered principal,
`Action.PUBLICATION_MANAGE`, source ownership and permission epochs, and correct
registered operator identity. Apply established mandatory signed-OID/Graph and
enabled-account correlation checks.

Assess remaining lifetime against preparation and later four-call execution.
Preserve the stricter 20-minute practical authorization headroom, beyond the
launcher's ten-minute minimum. Do not extend expiry or call near-expiry authority
ready. Record `APPLICATION_AUTHENTICATION_VERIFIED` only after production success;
otherwise record `APPLICATION_AUTHENTICATION_BLOCKED` with a sanitized failure
class. Do not create protected packets under an unverified identity.

## Stage B — provider credential and operator conditions

### 7. Foundry credential

Management authentication is distinct from the data-plane credential expected in
`POLYMIND_L1_AZURE_CREDENTIAL`. Inspect the actual provider contract and identify
supported Entra bearer or explicitly supplied approved resource API-key use.
Use only the implemented permitted mechanism. Do not silently retrieve resource
keys, create/rotate keys, modify RBAC or expose material.

If an approved bearer path exists, verify audience and expiry. If a key is
required, request supply through the established secure operator mechanism;
never put its value in a report or source file. Verify resource, mechanism,
audience/key scope, validity, approved use deadline and nonreliance on expired
historical credentials. No paid test call. Explicitly disclose if data-plane
acceptance remains unverified.

### 8. Deployment and quota

Reconfirm fresh relevant target fields through approved read-only management:

| Parameter | Required target |
| --- | --- |
| Resource | epolymind-foundry-dev-susanta |
| Region | Spain Central |
| Deployment | epolymind-gpt-54-mini |
| Model/version | gpt-5.4-mini / 2026-03-17 |
| Class | GlobalStandard |
| API | /openai/v1/chat/completions |
| Allocation | 30 RPM / 30,000 TPM |

Do not change resources/quota, deploy a model or use another region/deployment.
Keep `LIVE_SCHEMA_ACCEPTANCE_UNVERIFIED`: offline compatibility is established,
but no free schema-compilation endpoint exists. Do not run a separate schema
probe. The later signed-packet review must acknowledge this uncertainty; only
Call 1 of a separately authorized evaluation may observe acceptance.

### 9. Shared-consumer exclusivity

Recheck known AKS/node-pool/ECI workloads, playground usage, scripts, other provider
clients and interactive sessions, shared resource/deployment consumers, admission
policy, allocation and interactive reserve. Stopped workloads and zero local
admissions do not exclude external clients. Do not stop others' workloads or alter
shared policy.

Obtain fresh operator attestation specifying UTC date, proposed start/cutoff,
scope, attesting operator, known competitors and actual usability. If absent,
identify exactly what is missing and mark `EXCLUSIVE_WINDOW_PENDING_OPERATOR`.
Do not invent an attestation or infer one from stopped containers.

## Stage C — finance and governance

### 10. Pricing and maximum budget

Reconfirm applicability of catalog `phase17hl-pricing-eur-202611/1`, effective
`2026-11-07`, SHA-256
`59c90a122e3db199848ae0817218bc4286bab80b22920a0916d8f5a54426dd37`.
Existing EUR rates per million: input `0.673279770188`, output
`4.039678621124`. Exact-resource observations used USD `0.75`/`4.50` and
`0.897706360249562 EUR/USD`. Do not assume perpetual applicability.

Maximum: four provider calls, 100,000 input and 12,000 output tokens. Recompute
with Decimal and the exact active catalog:

| Historical-assumption component | EUR |
| --- | ---: |
| Tokens | 0.115804120472288 |
| 23% token VAT budgeting allowance | 0.02663494770862624 |
| Network contingency | 0.10 |
| Serialized aggregate extras | 0.126634947709 |
| Total | 0.242439068181288 |

Separate token prices, assumptions, unverified invoice VAT, contingency and current
approved exposure. Historical arithmetic is not fresh spending authorization.
The historical EUR 5 ceiling is neither permission to spend EUR 5 nor an Azure cap.

### 11. Financial authority and headroom

Reinspect existing authorities read-only. Historical remaining capacity was 16
rolling requests; 500,000 daily, 1,459,618 monthly and 112,000 outstanding tokens;
monthly accounting EUR `4.923760432874072880`. Historical state: 13 settled,
zero unsettled reservations, zero active admissions and ten consumed markers.

Do not reserve, consume, reset, modify settlements, reprice history, delete audit,
create replacement authorities or switch replay directories. Maintain exact
authority locations and policy bindings.

Prepare a four-call financial proposal identifying model/deployment, tokens,
catalog, verified extras, maximum exposure, owner/tenant allowance, shared-use
implications and remaining assumptions. Ask for a fresh positive financial
decision only after exact exposure is established. Capacity is not approval.
Without approval use `V10_FINANCIAL_AUTHORIZATION_PENDING`; never construct a
signed approval from unapproved assumptions.

## Stage D — proposed v10 operator packet

### 12. Canonical benchmark

Use unchanged `phase17h-pdf/1`: four pages, six lines, seed 1708, source SHA-256
`1be99e19a56040fb55c74682a19f874d4d4573f18d9f52a9a7ae19c8158ea92d`.
Reconfirm byte equality with preserved v8 source and authorized owner/extraction
scope under the renewed identity. Do not change contents, recipe or difficulty.

### 13. Source/plan preparation and mutation boundary

Only after identity and safe-preparation gates pass, use existing production
preparation mechanisms for a new v10 owner-scoped source and plan. Verify owner,
tenant, immutable source, extraction, original offsets, stable references,
authorized scope, stage graph, generation, embeddings and resource/deployment.

Embedding model: `sentence-transformers/all-MiniLM-L6-v2`, revision
`1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, tree SHA-256
`96ab3cd391276cb159904c4d329318ae1f3330278a7fc0450256233cf8bb78db`;
eleven expected local files. No model download, revision change or new production
vector store except an explicitly authorized existing workflow requirement.

New configuration and disposable verification artifacts may be prepared in the
designated protected preparation location. Existing operational authority,
admission, financial, replay and historical state must not change. If actual
source/plan registration requires consequential authority writes beyond safe
preparation, identify the operation and obtain its required authorization first.
Never use direct database writes to bypass that boundary.

### 14. Canonical configuration

Use production configuration code and unchanged schema to bind generation/digest;
Azure tenant/subscription/resource; deployment/model/API; actual verified operator
and owner scope; immutable source/canonical plan; embedding pin; governance,
shared-admission and pricing authorities; approved maximum exposure; audit and
replay destinations; actual credentials and validity; execution window; and
existing launcher/verifier bindings. Independently recompute its digest.

Do not patch historical fingerprints/timestamps or invent approval UUIDs for
consumed identities. Any new unused identifier must come through established
preparation and remain unused until independently authorized execution.

### 15. Actual packet preflight versus rehearsal

`python -m tests.performance.foundry_l1 --output ...` is network-forbidden
synthetic rehearsal. That branch does not validate an externally supplied
operational configuration. Do not use it as final-packet validation.

Separately check actual proposed canonical parsing, generation, source/plan,
identity/owner, endpoint, catalog, governance, storage/embeddings, credentials,
limits, strict schema, G1/G2, receipt/checkpoint paths, replay, authorization
fields and window through supported interfaces. Do not call `--live`, make
provider calls or consume approval. Real flags are `--live`, `--configuration`,
`--approve-sha256`, `--approval`, `--approval-trust`; no invented `--dry-run`.
Unsigned input is not launch authority.

### 16. Window and lifetime

Prepare actual timing only with current authentication and operator attestations.
Maximum four calls, concurrency one, at least 61 seconds between starts, no paid
retries, fallback, additional schema/downstream calls, and first-terminal-failure
termination. Account for credential/approval expiry, not-before restrictions,
20-minute practical margin, spacing, startup, latency, cutoff and exclusivity.

Do not invent preferred UTC times. If no usable window is attested, propose a
schedule with approval pending. Never call a token launch-ready if it expires
before the proposed window. Identify whether separately approved renewal will
be needed immediately before signing/execution.

## Stage E — final verification and handoff

### 17. Final checks

Independently verify exact source/generation, authenticated Principal/permissions,
provider credential, deployment/quota/consumers, RSA public trust, catalog,
headroom and positive allowance, source/plan, embeddings, canonical digest,
storage/replay preservation, exclusive window, lifetime and approval bindings.
Do not label incomplete fields verified. When external facts prevent an exact
configuration, retain maximum safe evidence and identify missing fields.

### 18. Exactly one primary verdict

- `READY_FOR_INDEPENDENT_RSA_AUTHORIZATION`: all identity, provider, deployment,
  operational, finance, exclusive-window, fresh-configuration/hash and binding
  gates satisfied. Next step is independently authorized signing, not signing here.
- `OPERATOR_PACKET_PREPARED — AUTHORIZATION_PENDING`: complete proposed packet
  exists but independent decisions remain pending; disclose nonfinal fields.
- `AUTHENTICATION_RENEWED — PACKET_PREPARATION_INCOMPLETE`: authentication succeeds
  but source/provider/finance/window/operational requirements prevent completion.
- `AUTHENTICATION_BLOCKED`: current production identity verification cannot succeed.
- `OPERATOR_PREPARATION_BLOCKED`: verified cloud/storage/security/governance/finance
  condition prevents progression.

Do not force PASS.

### 19. Signing handoff only if ready

Provide nonsecret canonical configuration/generation/source/plan hashes and
identities, target, verified identity references, financial ceiling/catalog,
not-before/expiry, public key fingerprint/ID, unused approval identity if properly
created, independent signer authorization requirement and immutable configuration
location. No private key, token, provider credential, private configuration/source
contents or fabricated approval. Stop before signing: exact-configuration signing
requires a separate authorization. Never call the signer or live launcher here.

### 20. Required documentation

Create this matching prompt record and
`docs/codex/reports/phase_17h_v10_authentication_renewal_and_final_operator_packet_preparation.md`.
The report must cover executive outcome, source/CI/generation, authentication
method and production results, Principal/permissions/lifetime, provider readiness,
Azure/quota/consumers/exclusivity, RSA public trust, pricing/cost/financial decision,
read-only admission/settlement/replay, source/plan, embedding/storage, canonical
digest if created, actual offline preflight, timing, remaining authorizations,
signing handoff if ready, one final verdict and final Git state. Include no secrets
or private authority material. If stopped early, retain successful checks and the
exact blocker.

### 21. Git and implementation restrictions

No staging, commits, push, reset/rebase, branch/history changes, production/test
edits, generation-fixture changes, G1/G2 changes, replacement pricing records,
historical approval changes, replay deletion/reset, settlement reopening or
existing operator-authority modification. Preserve every inherited untracked file.
Only create requested prompt/report, necessary temporary verification outside the
repository, and new protected preparation artifacts through explicitly authorized
existing mechanisms. Leave both documents untracked/uncommitted; preserve prior
reports.

### 22. Absolute execution boundary

Allowed: established authorized interactive device login; production token
validation; authorized read-only cloud/operational inspection; offline tests and
synthetic checks; approved nonspending preparation; nonsecret handoff.

Forbidden: RSA signing, approval consumption, paid inference, live launcher,
hidden schema probes, automatic retries, cloud changes, unauthorized key
extraction, policy/ledger mutation, authority replacement, unapproved source
registration and Git staging/commit/push. The operator personally completes
authentication and independent decisions. Initiation is not control bypass.

### 23. Final response requirements

Provide a concise status/evidence table for new Entra authentication, production
Principal, PUBLICATION_MANAGE, provider credential, deployment, RPM/TPM, consumers,
exclusive window, RSA public trust, storage, embedding revision, pricing,
headroom, positive finance, source/plan, canonical configuration/fingerprint,
actual offline packet verification and independent signing readiness. State one
verdict, exact blockers, next operator action, execution-time renewal requirement
and signing readiness. Preserve success even if a later gate fails; stop at the
first unresolved material gate.

Finish with Git staging/commit/push, RSA signing, approval consumption and live
inference all NO, and paid provider calls 0. Engineering needs no redesign:
prioritize verifiable identity and current independently verified facts. Never
reuse expired tokens, signatures/windows or assumed financial authority.

## Subsequent operator steering preserved

The operator reported that login was completed. The helper must still return
success and production verification must run; the message alone is not proof.

The operator then explicitly declared the window pending: proposed attester
Susanta Hazra remained subject to confirmation; date, not-before, target, strict
cutoff and end were all pending. Historical stopped workload observations must
not become a fresh attestation. Playgrounds, scripts, other accounts and shared
consumers were not excluded/accounted for.

The provider mechanism was confirmed as a resource API key supplied through
`POLYMIND_L1_AZURE_CREDENTIAL`; availability was unconfirmed and its use deadline
unset. Resource-key retrieval was explicitly unauthorized. Continue offline and
read-only verification, but do not create a final launch-ready packet, sign,
consume authority or infer until missing requirements are satisfied.

The operator subsequently positively approved a maximum budgeting allowance of
**EUR 0.242439068181288**, financial only: at most four calls to
`epolymind-gpt-54-mini`, 100,000 input/12,000 output tokens, catalog
`phase17hl-pricing-eur-202611/1`, token allowance EUR 0.115804120472288 and
aggregate extras EUR 0.126634947709 including 23% token VAT budgeting and EUR 0.10
network contingency. Fixed cost EUR 0 and the stated exclusions were accepted.
Current pricing must be revalidated for the eventual execution window. No
automatic retries, fallback or additional calls. This does not authorize signing,
key retrieval, approval consumption or paid execution. Remaining preparation and
verification may continue under existing controls.

The operator next proposed 12 November 2026, not-before 09:00 UTC, target 09:05,
strict cutoff 09:10, evaluation end 09:30, and credential/approval validity
preferably through 09:50. Final attestation and API-key availability were expressly
pending; resource-key retrieval/regeneration remained forbidden.

That proposal was subsequently superseded by **11 November 2026**, not-before
**19:05 UTC**, target **19:30**, strict launch cutoff **19:35**, evaluation end
**20:00**, attesting operator Susanta Hazra subject to final confirmation, and
proposed credential-use deadline **20:20**, subject to actual validity and
operator approval. Exclusivity is only proposed: playgrounds, scripts, other
accounts and shared-quota consumers must first be excluded/accounted for.
Credential availability remains unconfirmed. Continue permitted preparation and
verification without RSA signing, approval consumption or paid execution.

Actual draft parsing exposed the existing twelve-decimal `money()` constraint:
the exact EUR 0.242439068181288 forecast cannot populate `contract.maximum`.
The operator explicitly approved **EUR 0.242439068182** as the smallest
representable configuration ceiling, increasing the ceiling by
EUR 0.000000000000712 while leaving the four-call forecast unchanged. All prior
financial limits and pricing-revalidation conditions remain. This is financial
only, with no authority to retrieve keys, sign, consume approval or execute
inference. No production monetary precision rule may be changed.
