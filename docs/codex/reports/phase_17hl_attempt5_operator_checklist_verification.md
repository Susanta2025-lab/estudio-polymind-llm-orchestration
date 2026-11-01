# ATTEMPT 5 — OPERATOR CHECKLIST VERIFICATION

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

26 October 2026. Branch `master`; HEAD
`af4a7a076c918ef13aea05d74bf239c0af909133`.
Current safe validation completed **2026-10-26 09:50:02 UTC**, exit 0,
zero observed network attempts. This is operator checklist verification only.
Attempt 5 was not executed; this task grants no live execution authorization.

Evidence labels used below:

- **[Preparation](phase_17hl_attempt5_operator_authorization_and_single_call_execution.md)**:
  26 October deployment, financial and private-draft preparation evidence.
- **[Handoff](phase_17hl_attempt5_final_readiness_and_operator_preparation.md)**:
  24 October engineering GO and standing operator requirements.
- **[F1](phase_17hl_f1_http_cleanup_failure_preservation.md)**:
  corrected transport boundary, current source bindings and regression evidence.
- **[Assessment](phase_17hl_attempt5_readiness_authorization_assessment.md)**:
  financial and authorization implementation analysis; its earlier F1 NO-GO is
  superseded by F1 and Handoff.
- **[Historical authorization](phase_17hl_final_operator_authorization.md)**:
  15 October catalog approval, known consumers, key consistency and standing
  retention/review decisions. Its four-call scope is historical only.
- **[Operator procedure](../../evaluation/phase_17hl_operator_approval.md#single-analysis-timing-and-preparation-handoff)**:
  current single-analysis preparation, finalization and independent signing order.
- **Current validation**: inspected external driver
  `/tmp/polymind-attempt5-checklist-readonly.py`, run with the existing project
  Python interpreter and `PYTHONDONTWRITEBYTECODE=1` from `/tmp`. It used existing
  `read_private`, `load_trust`, configuration models, authoritative digest
  functions, `window_information`, evaluation binding validation and `impact`.
  Application settings/implicit dotenv were isolated before application imports;
  the inspected existing socket/DNS denial guard was active before those imports.

The private input is the specified
`<PRIVATE_OPERATOR_DIRECTORY>/configuration.draft.json`.
Protected configuration values, operator identifiers, key ID, credentials,
signatures and replay record contents are not reproduced here. No private
signing key or stored access token was inspected.

## ENGINEERING BASELINE:

Source fingerprints: **CONFIRMED** through existing authoritative functions.

| Binding | Current SHA-256 | Authoritative source |
| --- | --- | --- |
| Executor | `82fc01aa0447d4be758124cec0120a06db49f139f69ee6425b51b8696a6ad26f` | `foundry_single_call.executor_digest()` |
| Generation source | `7d387a8595cf63e2ac944a25c4987a1b37392aa4adba8889914acf51ff9f0f59` | `foundry_l1.generation_contract_digest()` |
| Provider schema | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` | `fingerprint(provider_schema(generation_schema()))` |
| Inference configuration | `7eaa6b52ad387f9f0c82e318e9c74fa378ffda0baec85d0f7157cc4ab0553519` | `ManagedSynthesisInference.config` with the existing strict capability, explicit four stage profiles, intended deployment and unusable transport |

Match: **YES**. Draft executor/generation/schema bindings also match. No source,
fingerprint constant, catalog pin or approval was changed. The inference-settings
fingerprint is distinct from the complete final configuration digest; no final
configuration digest or acknowledgement exists for this unapproved draft.

## CHECKLIST A — FINANCIAL AND CAPACITY

**Pricing: NOT VERIFIED.** Catalog identity, serialized pin and arithmetic are
confirmed, but sufficient current commercial evidence for `charges_verified=true`
is absent. Existing catalog `phase17hl-pricing-eur-202610/1` retains serialized
SHA-256 `dad37bc0f349cdfbea16e25cae028a0b5042e4e3e3daac4f141f9b566c5bc65e`.
Assessment §G identifies the public matching prices as a synthetic review fixture;
historical operator approval of that catalog does not establish current commercial
applicability. Missing facts are the applicable model/SKU/region input and output
prices, billing unit, EUR conversion basis if applicable, effective date and
commercial provenance agreeing with this exact catalog. The calculated token
reservation is EUR **0.028379091869065**, not a verified quotation.

The supplied Azure cost-analysis CSV contents are not available in the inspected
evidence. Repository CSV discovery found only the benchmark CSV; no CSV was found
at `/tmp` top level, and local Downloads/Documents directories were absent. This
bounded search is not a claim about every possible storage location. No model
price or charge bound is inferred from the unavailable export.

**Additional charges: NOT VERIFIED.** The draft proposes fixed/extra costs of
zero. Historical authorization §B explicitly leaves their evidentiary basis
unresolved. Missing is supported absence of incremental attributable CPU/storage,
networking, service or logging charges for this one-analysis operation. Existing
AKS/Redis baseline exclusions alone do not establish zero attributable extras.
`one_call_contract` requires both amounts to remain zero; conflicting evidence
requires separate review, without changing this task's catalog or contract rules.

**30,000 TPM: CONFIRMED.** Preparation's 26 October read-only Azure deployment
query established the intended resource/deployment, GPT-5.4-mini version
`2026-03-17`, GlobalStandard, succeeded state, **30 RPM / 30,000 TPM**.
Reuse that same-day allocation evidence. Current stored/draft provider policies
agree: 30,000 TPM and 2,000 protected interactive TPM. The full 25,000-input plus
3,000-output reservation fits the remaining 28,000 TPM exactly. This confirms
allocation and arithmetic; it does not certify availability across outside users.

**Shared consumers: NOT VERIFIED.** Reuse the established dedicated PolyMind
deployment, separate ECI deployment and AKS scaled two to zero from Historical
authorization §A. Those facts were never a complete inventory. Missing is the
current assurance that other scripts, playgrounds, processes or services will
not consume the required deployment capacity or owner/tenant budget during the
execution interval. Local admission cannot enforce external consumer behavior.

**Available funds: CONFIRMED.** Current read-only authority inspection found four
SETTLED reservations, zero unresolved reservations, zero active local provider
calls and zero calls in the preceding minute. Existing evaluation policy/catalog,
shared paths/key/policy bindings and all three SQLite quick checks agree.
`impact()` returns the following for **both owner and tenant**:

| Local allowance | Remaining at validation |
| --- | ---: |
| Requests in policy window | 16 |
| Daily tokens | 500,000 |
| Monthly tokens | 1,485,423 |
| Outstanding reservation capacity | 112,000 tokens |
| Monthly EUR | 4.969124868004221809 |

These permit the proposed one-call reservation under the pinned calculation.
The shared allowance permits other authorized work too; exactly-one enforcement
comes from this executor's one-call contract and RunGuard. This is local financial
headroom, not an Azure subscription balance or current spending authorization.
The actual draft has `contract.approved=false` and is rejected. Therefore the
complete financial authorization gate does **not** currently permit execution.

**Status: PENDING OPERATOR ACTION.**

**Evidence:** Preparation's deployment query and allowances; Historical
authorization §§A–B; Assessment §G; current immutable read-only SQLite queries,
policy comparisons and `impact()` at the timestamp above.

**Missing action:** Supply the non-secret commercial reference matching the
existing catalog and the supported zero-extra-charge basis; confirm remaining
consumers are excluded for the chosen interval. Then the operator can review and
approve the proposed financial contract and adopt the supported charge/quota/
consumer attestations through the existing finalization procedure. No quota
rediscovery, budget reset or ledger/catalog edit is required. Recheck transient
local headroom immediately before any separately authorized execution.

## CHECKLIST B — ENTRA AND CREDENTIALS

**Tenant/resource association: CONFIRMED.** Reuse Preparation's same-day enabled
subscription/tenant and target-deployment association. Current `OIDCSettings`
validation confirms the intended tenant-specific Entra v2 issuer, API UUID audience
and pinned trust identity association. The draft endpoint passes the existing
`deployment_configuration` resource/host/path validation. This verifies intended
association and configuration, not current inference-credential authority.

**Operator authorization: CONFIRMED.** Current read-only SecurityAuthority data
contains exactly one matching enabled user registration with the pinned identity,
derived owner scope and `PUBLICATION_MANAGE`; the existing evaluation scope agrees.
`security.identity.OIDCVerifier.verify` requires the delegated `access_as_user`
scope and exact role set `{PolyMind.L1Operator}`. Required issuer is the configured
tenant-specific `https://login.microsoftonline.com/<tenant>/v2.0`; audience is the
configured PolyMind API client UUID, not the `api://` scope URI. These are checked
against existing protected settings without publishing their values. Stored
authorization does not establish today's token claims or assignment validity.

**Credential provenance: NOT VERIFIED.** Historical authorization §A established
inference-key presence in private storage and the configured target, explicitly
leaving resource authority/access unresolved. No later inspected report supplies
the missing non-secret origin/authorization evidence. The draft selects API-key
authentication, which the launcher sends in `api-key`. Required provenance is that
the existing key belongs to this exact resource and is authorized for the intended
deployment; key presence or a past Boolean alone is insufficient. An operator-set
API-key use deadline is not measured key expiry or a successful acceptance probe.

**Current authentication: PENDING OPERATOR ACTION.** Both
`POLYMIND_L1_OPERATOR_TOKEN` and `POLYMIND_L1_AZURE_CREDENTIAL` were absent from this
validation process (presence-only observation). No current verified principal was
created. [Historical diagnosis](phase_17hl_single_call_execution_failure_diagnosis.md#b-execution-timeline)
records successful signature/issuer/audience/lifetime/scope/role and registered-user
verification at **2026-10-16 23:34:49 UTC**, with that preparation token expiring
on 17 October. Reuse that as historical authentication evidence only. It cannot
prove current token validity or Azure inference-key provenance.

**Status: PENDING OPERATOR ACTION.**

**Evidence:** Preparation; Historical authorization §B; historical diagnosis §B;
current `OIDCSettings`, trust/scope/registration checks and environment presence;
[identity verifier](../../../security/identity.py) and
[Entra contract](../../security/entra_v2.md).

**Missing action:** The operator must use the existing approved delegated
MSAL/interactive flow for the configured API's `access_as_user` scope and role,
securely provide the token to the existing verifier, and confirm its verified
issuer/tenant/subject and derived scope match the existing trust/registration.
Do not reuse a historical signing/authentication helper with stale packet pins.
No new client, consent or authentication flow is needed. Separately record the
existing inference key's resource/deployment provenance, securely supply it at
execution, and attest its permissible use deadline. Verify fresh token claims
with `OIDCVerifier.verify`, not unverified JWT decoding. Fresh interactive
authentication is still required for this handoff; none was initiated here.

## CHECKLIST C — CONFIGURATION AND APPROVAL

**Signing-key association: CONFIRMED.** `load_trust()` validates the existing
live-purpose RSA public trust, protected replay path and configured key ID.
Its public key matches the separate public PEM and established DER fingerprint
`35785596dd2f38a3ae5fc8eeb93015a1ba3c8b4f16f06a1d73fbe521f9657816`.
The configured key ID remains protected; a future JWS header must equal exactly
`{alg: RS256, typ: polymind-approval+jwt, kid: <existing trust key ID>}`.
This confirms the stored association and public consistency only.

**Independent signer provenance: NOT VERIFIED.** Historical manual pair matching
and today's public-key checks do not establish the operator association through
an independent channel. The explicit outstanding provenance requirement in
Historical authorization and Preparation remains unresolved. No private key was
opened to attempt to resolve it.

**Private configuration readiness: PENDING OPERATOR ACTION.**
`SingleCallConfiguration.model_validate_json()` rejects the actual draft at
`contract`, as expected from `approved=false`. All nine attestations remain null;
no final configuration or signed approval exists in this packet. Draft source
bindings, existing policies/authorities, registered scope, endpoint, one-call
purpose and previously prepared request hashes agree with Preparation. No
approval flag was changed even in a hypothetical validated configuration, and
no final digest/acknowledgement or replacement packet was generated.

**Actual-scope binding: CONFIRMED.** Reuse Preparation's guarded actual-scope
`prepare_analysis()` evidence: four extracted units, one analysis, no children,
fixture hash `1be99e19a56040fb55c74682a19f874d4d4573f18d9f52a9a7ae19c8158ea92d`
and rendered-request hash
`d1a9ad26a84ed848af18ebdba1eae894401cff337b0ce72d660cf8bc01b2c271`.
Current draft hashes and derived registered scope agree. Extraction was not rerun
into the private packet. Fresh authenticated scope equality remains a requirement
before final approval; these hashes must not be transplanted into another scope.

**Nine attestations: PENDING OPERATOR ACTION.** None is populated in this draft.

| Required field | Status | Smallest supported completion |
| --- | --- | --- |
| `credential_valid_until` | PENDING OPERATOR ACTION | Adopt a justified deadline for use of the provenance-verified inference credential. |
| `approval_expires` | PENDING OPERATOR ACTION | Choose the reviewed approval expiry when authentication/signing are ready. |
| `execution_not_before` | PENDING OPERATOR ACTION | Choose the actual authorized start within that window. |
| `credential_audience_verified` | PENDING OPERATOR ACTION | Establish exact resource/deployment authority of the existing key; no inference probe is necessary. |
| `quota_verified` | PENDING OPERATOR ACTION | Carry forward the sufficient same-day allocation evidence into the final attestation. |
| `shared_consumers_verified` | PENDING OPERATOR ACTION | Complete the remaining-consumer assurance described in A for the execution interval. |
| `charges_verified` | PENDING OPERATOR ACTION | Establish the missing commercial applicability and supported zero extras described in A. |
| `actual_azure_rpm` | PENDING OPERATOR ACTION | Adopt the verified 30 RPM allocation, subject to changes before execution. |
| `actual_azure_tpm` | PENDING OPERATOR ACTION | Adopt the verified 30,000 TPM allocation; 28,000 would not cover this reservation plus protected headroom. |

Underlying evidence may already suffice, as for allocation; this table records
the missing final attestations rather than demanding a redundant cloud inquiry.

**Signed approval: PENDING OPERATOR ACTION.** No valid, current, unused approval
for a finalized Attempt 5 configuration is established. This packet contains no
JWS, and Preparation found no fresh eligible approval in existing single-call
storage. Historical expired/source-bound approvals are not substitutes. Actual
`verify_artifact()` was inspected but not invoked without a current final
configuration, verified principal and supplied fresh artifact.

The required audience is **`polymind-single-analysis-live`**, issuer
`polymind-operator-approval/1`, purpose `live`, executor
`polymind-single-analysis/1`, intended model/deployment/version/SKU above, and
one first-analysis diagnostic only. `foundry_approval.bindings()` must bind the
validated complete configuration digest, verified principal, financial/limit/
target fields, expiry and current executor/generation/schema hashes. The complete
digest also binds authority paths/policies, nine attestations and actual-scope
fixture/request hashes. The inference configuration is separately verified above;
it is not an additional explicit field in the JWS execution binding.

**Replay protection: CONFIRMED.** Existing private persistent replay storage is
separate from the run audit directory. Four consumption records remain unchanged;
the current audit directory is empty. `verify_artifact()` only verifies; it does
not check the central consumed marker. For a future successfully verified JWS,
read-only inspection must additionally establish absence of that verified `jti`'s
`<jti>.consumed.json`, existing run records and live-start marker. No current
approval ID exists here to declare unused. The exclusive/fsynced `consume()` is
the execution-time race barrier; it must not be called to test eligibility.

**Status: PENDING OPERATOR ACTION.**

**Evidence:** Current public trust/path/configuration checks; Preparation's
actual-scope rendering; Historical authorization's provenance limitation;
[single-call implementation](../../../tests/performance/foundry_single_call.py),
[approval implementation](../../../tests/performance/foundry_approval.py) and
Operator procedure. Existing approval/preflight regression tests were inspected,
not rerun or used against live authority state.

**Missing action:** Establish the pinned key's independent operator association.
After A/B evidence is complete, approve the proposed contract, use the existing
offline finalizer with the nine supported attestations to create a new final
configuration, review its validated digest, and use `bindings()` with the verified
principal. The independent operator must personally review and sign those exact
claims using the existing operator-controlled RSA process, a fresh canonical
approval UUID and the existing pinned key ID. Require integer `iat <= nbf < exp`,
`exp-iat <= 86,400`, and `exp == config.approval_expires`. Retain the trust and
replay authority. Then validate with `verify_artifact()` and inspect replay
eligibility read-only. No historical signer script may be repinned for this task.

## CHECKLIST D — FINAL PREFLIGHT

**Single-call enforcement: CONFIRMED.** Current source plus matching Handoff/F1
evidence enforce maximum one provider attempt, 25,000/3,000 token ceilings,
immutable source/schema/request bindings, no retry, fallback, reduction, Q&A or
embedding. RunGuard rejects a second call even under another logical identity.
The HTTP session uses zero retries and disables environment inheritance;
redirects are forbidden. `managed-prompt/3` remains active; prompt 4 is inactive.

**Financial gate: PENDING OPERATOR ACTION.** Current headroom/policy/obligation
checks pass, but the contract is unapproved and commercial/consumer/credential
attestations are incomplete. No funds were reserved. Local finance must be checked
again immediately before execution because this observation locks no capacity.

**Execution window: PENDING OPERATOR ACTION.** Pure `window_information()` on the
draft's unset timing fields returns `window_eligible=false`. No time window is
invented. The launcher requires
`execution_not_before <= now < min(approval_expires, credential_valid_until)-600`;
equality at the cutoff is ineligible. Signed approval, operator token and
credential deadlines must also retain more than 60 seconds at final verification/
execution. These are checks against actual current time, never historical clocks.

**Approval validity: PENDING OPERATOR ACTION.** A finalized acknowledged
configuration, fresh authenticated principal and current unused approval must be
established under C. Current signature, expiry and replay eligibility were not
marked complete using historical evidence.

**Read-only preflight: CONFIRMED.** Only the safe observations listed above were
run: private-path/public-trust validation, authoritative binding comparison,
actual draft model rejection, pure timing observation, policy/evaluation binding
validation, immutable read-only SQLite SELECT/quick-check queries, allowance
calculation and artifact-preservation checks. No live authority class was
constructed. Database connections used `mode=ro&immutable=1`, `query_only=ON`,
and first required absent WAL/SHM/journal sidecars. Before/after content hashes,
modes and modification times agree for the three authorities, trust/public key,
all existing packet files and replay records; replay inventory is unchanged.
This is a point-in-time observation, not a reserved financial/admission slot.

The general CLI was not used as a blanket preflight. Its offline review path is
non-inference, but error diagnostics/finalization can write private artifacts.
`launch()`/`_launch()` are **pending execution operations**, not read-only checks:
they construct authorities, can append authorization evidence, prepare objects,
initialize ledger/admission/run databases, call `consume()`, create
`live-started.json`, reserve finances and ultimately invoke the provider.
None was executed. No helper named eligibility/preflight was trusted by name.

**Status: PENDING OPERATOR ACTION.**

**Evidence:** Current validation; source order in `foundry_single_call` and
`foundry_approval`; Handoff §§E–G and Operator procedure.

**Missing action:** After A–C completion, repeat pure window, exact digest/source,
signature, verified identity/registration, credential-use and unused-marker checks
with current inputs. Reinspect existing financial obligations/allowances and
current shared capacity; confirm no cancellation or existing run/live-start record.
Only a separately authorized execution may perform the final atomic consumption,
reservation and live-start operations. Passing this checklist verification cannot
authorize those mutations or inference.

## SUMMARY:

**Confirmed items:** All four fingerprints and draft source bindings; same-day
deployment/allocation evidence; 28,000 + 2,000 TPM feasibility; reusable known
consumer facts; current local financial headroom and absence of unresolved work;
stored operator/trust/scope configuration; RSA public consistency and key-ID
validation; prepared actual-scope fixture/request bindings; persistent replay
mechanism; safe read-only observations; single-call/no-retry enforcement.

**Pending operator actions:** Supply commercial/zero-extras and remaining-consumer
evidence; establish inference-key provenance and fresh delegated authentication;
confirm independent signer provenance; approve/finalize the existing draft and
nine attestations; independently sign/verify a fresh exact-bound approval; repeat
time-dependent eligibility checks. None requires rebuilding authorities or
repeating the engineering audit.

**Not verified items:** Current commercial applicability, supported zero extras,
complete consumer assurance, inference-key resource authority/current validity,
independent signer provenance, and a valid current unused approval. The respective
smallest actions and existing validation mechanisms are specified in A–D.

**Blocking failures:** None demonstrated in the engineering baseline or current
authority integrity/headroom. The expected unapproved-contract rejection and
missing credentials/attestations/approval are outstanding operator gates, not a
new engineering defect. They prevent execution with the present draft.

ENGINEERING READINESS: **GO**

OPERATOR CHECKLIST: **INCOMPLETE**

LIVE EXECUTION AUTHORIZED NOW: **NO**

```text
PAID INFERENCE CALLS: 0
APPROVALS CREATED OR CONSUMED: 0
LIVE FINANCIAL RESERVATIONS: 0
PRODUCTION MODIFICATIONS: 0
COMMITS/PUSHES: 0
```

**NEXT REQUIRED OPERATOR ACTION:** Provide the commercial reference supporting
the unchanged catalog and zero-extra-charge basis, plus the remaining-consumer
assurance. Establish inference-credential and independent signer provenance before
opening a fresh authentication/signing window. Then follow the existing
single-analysis finalization/signing sequence against this draft. Do not execute
Attempt 5 under this verification task.

Review and repository validation: this task adds only this report; application,
tests, configuration, authorities, catalog and prior artifacts remain unchanged.
Self-review checked evidence age, financial headroom versus authorization,
stored versus freshly verified identity, exact source/request binding and the
signature-versus-replay distinction. Separate pre-commit review checked for
protected data, unintended instructions to execute, dependencies, unrelated edits
and broken local links. No implementation change warranted pytest/compileall,
Docker or Kubernetes work; the 426-test Handoff and 1,755-test F1 evidence is reused,
not rerun. `git diff --check` passed (exit 0). The new report's explicit
`git diff --no-index --check /dev/null <report>` produced no diagnostics (exit 1
denotes the expected new-file difference). All 11 local Markdown targets resolve;
the focused private-key/JWT/credential-assignment scan found zero matches.
Content-hash comparison preserved all 139 pre-existing modified/untracked files
in the captured worktree inventory; this report is the sole repository addition.

Final `git status --short --branch` remains `master...origin/master`, with
20 modified tracked files, 120 untracked files when expanded individually and
zero staged entries. `git diff --stat` remains **20 files changed, 832 insertions,
79 deletions**, all pre-existing tracked changes; the new untracked report is
excluded from that statistic. No staging, commit or push occurred.
