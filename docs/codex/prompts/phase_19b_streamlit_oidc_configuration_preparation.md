# CODEX MASTER PROMPT — PHASE 19B
## Streamlit OIDC configuration preparation and secure credential provisioning readiness

Clean instruction record, 26 November 2026. Repeated requirements are consolidated below;
the supplied user instruction remains authoritative. No operational credentials are included.

Project: Estudio PolyMind — Provider-Neutral LLM Orchestration Platform.
Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`; branch `master`.
Phase 19 — Azure Linux VM Deployment and Real-Model Integration.
Stage 19B — Offline Implementation, Azure Deployment, Live Integration and Validation.
Environment: local WSL Ubuntu, `estudio_polymind` Python environment.
VM: operator-reported deallocated. VM activation, Entra mutations, actual credential access,
real authentication, real-model inference and Git staging/commit/push are NOT AUTHORIZED.

## Objective

Continue from completed private HTTPS engineering and the newly completed dedicated Entra
browser registration. Reconcile evidence; prepare exact non-secret native Streamlit OIDC
configuration; prepare an independently executable secure operator provisioning procedure;
establish independent cookie generation; verify native/UI/API/enrollment compatibility;
prepare future Azure handoff; document outstanding authentication/deployment blockers.
Do not repeat HTTPS engineering or introduce unnecessary runtime changes. Codex must not
access actual client secrets or generate operational credentials on the operator's behalf.

## Mandatory inspection and baseline

Read complete root AGENTS.md. Before editing run:

```bash
git status --short --branch
git rev-parse HEAD
git log --oneline -5
git diff --stat
git diff --check
git diff --cached --name-only
```

Expected checkpoint message: `chore: configure Phase 19B private HTTPS origin and verify deployment integration`.
Verify actual SHA; never invent or reset it. Preserve operator changes. Operator-reported CI:
Estudio PolyMind CI, master, push, run `45778620125`, SUCCESS, 7m32s. Reconcile exact revision
using available read-only GitHub access; otherwise retain operator-reported classification.

Inspect:

- `deployment/phase19/streamlit.secrets.example.toml`
- `deployment/phase19/compose.env.example`
- `deployment/phase19/configuration.example.json`
- `deployment/phase19/ui.py`
- `deployment/phase19/gateway.py`
- `docker-compose.phase19.yml`
- `docs/operations/phase_19_vm.md`
- `docs/security/entra_v2.md`
- `docs/evaluation/phase_19_deployment_architecture.md`
- `docs/evaluation/phase_19_implementation_plan.md`
- `docs/codex/reports/phase_19b_private_https_origin_configuration_and_integration_verification.md`
- `tests/unit/test_phase19_oidc_template.py`
- `tests/unit/test_phase19_tls.py`

Inspect actual Chat/Documents native authentication consumers, API identity verification,
runtime enrollment, installed Streamlit version and native helpers. Do not assume proposed
code exists. Previously verified Streamlit version: 1.58.0.

Prior HTTPS task evidence is historical: focused 315 passed; full 3329 passed; 0 failures,
errors, skips or real inference calls; 8/8 gates PASS. It established selected private origin,
generic gateway compatibility, TLS/hostname/Host/WebSocket Origin checks, native template,
Windows-native SSH and private CA procedures without runtime changes or required image rebuild.
Preserve historical evidence and do not claim those runs were repeated unless actually run.

## Operator-reported executed Entra evidence, 25–26 November 2026

Tenant `afabeaf8-0fea-42c9-afb4-7e5c07eff3f3`, Azure account Enabled, single tenant/AzureADMyOrg.

API registration:

- Name `estudio-polymind-api-dev`.
- Client ID `5aa70f9d-9f9e-4b5b-972b-698d4d68105e`.
- Application ID URI `api://5aa70f9d-9f9e-4b5b-972b-698d4d68105e`.
- API SP object ID `046ce5b0-897c-4289-ad86-e403ac6b6e20`.
- Requested access-token version 2.
- Enabled delegated scope `access_as_user`, UUID `276cbb61-4f0d-4f08-9ce2-f62c5140813e`, consent Admin.
- Enabled User role `PolyMind.L1Operator`, UUID `e34bc374-42ff-4a6a-87e2-007b8cc788b3`.
- Operator role assignment matched directory principal and role UUIDs.

Dedicated browser registration:

- Name `estudio-polymind-streamlit-dev`.
- Client ID `a43f5479-4cbd-45a0-86e0-9c658e77d133`.
- Application object ID `11fb33b1-2149-4e74-a6ac-5f7295147607`.
- SP object ID `6a15b03a-f544-43eb-b486-d29a52ddfa8b`.
- AzureADMyOrg, Web platform, SP type Application, SP enabled.
- Implicit access-token issuance false; implicit ID-token issuance false; fallback public client false.
- Registered exact redirect `https://polymind.test:9443/oauth2callback`, accepted by Entra.

Exactly required delegated permission: resource API client ID above, permission scope UUID above,
type Scope. Persisted consent independently read back by operator: browser SP → API SP above,
consent type Principal, principal/operator directory object ID
`3c1c6ec4-ac53-485d-af7c-ff015f8fbe57`, granted `access_as_user`.
Tenant-wide consent NOT GRANTED. Preserve least privilege; no Graph permissions or tenant-wide consent.

Confidential credential:

- Description `polymind-streamlit-phase19b-dev`.
- Key ID `7319515e-0342-4c8e-aacb-b5c663c8cda9`.
- Start `2026-11-26T08:24:50.834Z`; expiration `2027-05-25T07:24:50.834Z`.
- Count 1; metadata PASS, operator-reported.
- Actual secret NOT PROVIDED TO CODEX.
- Location: operator-controlled personal storage outside repository; custodian: project operator.
- Encryption/access restriction NOT INDEPENDENTLY VERIFIED.

Never confuse key ID with secret value. Do not retrieve, rotate, recreate or inspect the
secret. Do not claim its possession, encryption or operational validity was independently verified.

## Fixed HTTPS selection

Preserve `PHASE19_ORIGIN=https://polymind.test:9443`; callback
`https://polymind.test:9443/oauth2callback`; SAN `DNS:polymind.test`; Windows hosts mapping
`127.0.0.1 polymind.test`; local/remote SSH forwarding `127.0.0.1:9443`;
VM publication `127.0.0.1:9443:9443`. Public exposure PROHIBITED. No origin change authorized.

## Security and architectural boundaries

Do not search personal folders, read real `.env` or secrets, decrypt personal credential files,
ask for pasted credentials, generate persistent operational cookie secrets, print/log/copy/
transmit real credentials, store credentials in Git or create operational Streamlit files.
Synthetic credentials only in isolated offline tests. Operator executes independently outside
Codex. No VM start/restart, remote SSH, Entra/consent/credential changes, real access/refresh
tokens, login, provider requests, production Compose/authorities or live permission issuance.
No new infrastructure/model expenditure. Specific task boundaries override broad prior authorization.

Preserve five services, generic environment-driven gateway, native Streamlit, API authorization,
seven SQLite authorities, Redis/Chroma persistence, provider-neutral inference, Chat/RAG,
Documents, independent execution authority, financial governance and local workflows.
No new auth framework, secret-management service, dependency or configuration framework.
No staging, commit, push, reset, clean or history rewriting.

## Stage 1 — readiness

Verify native `redirect_uri`, `server_metadata_url`, `client_id`, `client_secret`,
`cookie_secret`, `expose_tokens` and `auth.client_kwargs.scope`. Verify unnamed default provider
for existing `st.login()` consumers; do not replace authentication.

Verify API profile `entra_v2`, tenant above, issuer
`https://login.microsoftonline.com/afabeaf8-0fea-42c9-afb4-7e5c07eff3f3/v2.0`, JWKS
`https://login.microsoftonline.com/afabeaf8-0fea-42c9-afb4-7e5c07eff3f3/discovery/v2.0/keys`,
audience bare API UUID, required `access_as_user` and `PolyMind.L1Operator`.
Distinguish client IDs, application/SP object IDs, operator directory ID and API token subject.
Never use browser ID or Application ID URI as API audience or infer subject from directory ID.
Enrollment is `[issuer, tenant UUID, API access-token sub]`; actual sub remains UNKNOWN until
separately authorized verified authentication. No guessed enrollment or placeholder subjects.

Produce evidence-grounded readiness matrix: API, browser app, accepted redirect, SP, delegated
permission, principal consent, credential metadata, native configuration, API expectations,
custody, enrollment, real authentication. Use PASS/GAP/FAIL/PENDING/BLOCKED/OPERATOR_REPORTED_PASS.

## Stage 2 — exact configuration and secure procedure

Prepare this environment-specific non-operational report reference:

```toml
[auth]
redirect_uri = "https://polymind.test:9443/oauth2callback"
server_metadata_url = "https://login.microsoftonline.com/afabeaf8-0fea-42c9-afb4-7e5c07eff3f3/v2.0/.well-known/openid-configuration"
client_id = "a43f5479-4cbd-45a0-86e0-9c658e77d133"
client_secret = "<OPERATOR_SUPPLIED_SECRET>"
cookie_secret = "<INDEPENDENT_RANDOM_SECRET>"
expose_tokens = ["access"]

[auth.client_kwargs]
scope = "openid api://5aa70f9d-9f9e-4b5b-972b-698d4d68105e/access_as_user"
```

Verify against repository and installed implementation. Retain portable
`deployment/phase19/streamlit.secrets.example.toml` placeholders; no environment-specific
substitution there or unnecessary duplicate sources.

Design a short local WSL procedure, preferably standard library, independently run after review:
dedicated outside-repository Linux directory (prefer not `/mnt/c`), mode 0700; secure non-echoing
client-secret prompt that fails closed without secure terminal; independent CSPRNG cookie;
correct TOML escaping; initial file mode 0600; no overwrite; reject unsafe/symlink destinations;
parse/validate without content display; sanitized outcome/file metadata only. Proposed path
`~/.config/polymind/phase19/streamlit.toml`; another adequately protected path may be selected.
Do not execute with real credentials or create actual operational file.

Cookie generator equivalent to `secrets.token_urlsafe(48)`, independent of Entra/Foundry/TLS/
execution/development secrets, never identifier-derived or printed. Preserve across ordinary
restarts; changing it can invalidate browser cookies.

Existing secret may stay encrypted until needed; avoid persistent/redundant plaintext.
Explain populated TOML contains two plaintext secrets despite mode 0600. Recommend protected
encrypted staging while inactive. Provide preparation/metadata-only verification, optional
existing-GPG encryption, controlled decryption, temporary-file handling. No installation or
personal encrypted-file inspection. Ordinary deletion is not guaranteed secure erasure.

Operator preflight must compare actual gateway origin + callback, Streamlit redirect and
registered Entra Web URI exactly; correct tenant discovery, browser ID, API scope and audience,
token exposure and independent secrets; no Graph scopes or unresolved operational placeholders.
Do not claim automatic cross-file runtime validation if only operator preflight exists.

Prepare future `/etc/polymind/secrets/streamlit.toml` install, do not execute: regular file,
no symlinks, UID:GID 10001:10001, mode0600. Verify actual Compose source/destination,
read-only bind, missing-source failure, host-directory traversal, service UID/topology.
Use approved Tailscale/OpenSSH approach; never invent target/fingerprint/path. No credentials
in command arguments/environment/logs/broad remote temporary paths. Metadata/consistency
verification must not display secrets. No VM connection/transfer.

Synthetic isolated verification: native parsing/exact redirect/discovery/browser/scope/exposure,
cookie independence, TOML escaping, restrictive initial creation, overwrite refusal, unsafe
destinations, placeholder rejection, secret-free output, API identity and both UI consumers.
Prefer report procedure plus temporary synthetic verification over permanent application utility;
justify a reusable utility first if necessary. Reuse meaningful regression.

Check actual paths and run applicable focused tests:

```bash
python -m pytest -q \
  tests/unit/test_phase19_oidc_template.py \
  tests/unit/test_phase19_tls.py \
  tests/unit/test_security_entra.py \
  tests/unit/test_phase19_chat_view.py \
  tests/unit/test_documents_view.py \
  tests/unit/test_ui_api_client.py
git diff --check
```

Use established offline credential/network isolation; no real discovery/token/provider requests.
Full offline regression required for runtime/dependency/shared contract changes. Documentation/
operator procedure only: focused plus synthetic checks suffice with recorded rationale; do not
repeat previous 3329-test suite merely to duplicate evidence. Exact commands, exit codes,
counts/warnings/failures/corrections/unexecuted checks must be recorded.

## Stage 3 — records and review

Inspect before writing prompt/report paths:
`docs/codex/prompts/phase_19b_streamlit_oidc_configuration_preparation.md` and
`docs/codex/reports/phase_19b_streamlit_oidc_configuration_preparation.md`.

Report must explain executive summary; actual Git/CI; authorization; all Entra evidence;
exact reference; API compatibility; complete operator-executable procedure in one section;
cookie generation; encryption/custody; future Azure transfer; offline results; self-review;
pre-commit review; blockers; final matrix; next action; Git handoff. No real credentials.

Reconcile operations guide, README and relevant current Phase19 readiness docs with dated
addenda: browser registration, redirect acceptance, SP, delegated permission, principal consent
and credential metadata complete at operator-reported level. Preserve historical reports and
PASS/GAP/FAIL findings. Do not claim browser login, TLS provisioning or enrollment completed.

Self-review secrets/identity/native config/TOML/ownership/modes/prompt/independent cookies,
plaintext lifetime, accidental staging, unnecessary runtime changes and readiness provenance.
Separate pre-commit review; inspect new untracked files separately; run:

```bash
git status --short --branch
git diff --stat
git diff --name-status
git diff --check
git diff --cached --name-only
```

No searches outside repository for real credentials. Leave changes uncommitted.

## Acceptance gates and final handoff

Gate1 actual baseline/preserved existing work. Gate2 consistent identifier/permission/consent
evidence. Gate3 exact native config. Gate4 reviewed synthetically tested operator procedure.
Gate5 custody procedure design only; actual custody separately classified. Gate6 applicable
executed checks pass. Gate7 reproducible docs/blockers. Gate8 no unauthorized credential,
cloud/Entra/auth/inference/Git action. Never PASS an unexecuted operational check.

Final handoff: concise summary, exact non-secret config, complete procedure, created/modified
files, exact verification, blockers, image implications and proposed checkpoint:
`docs: prepare Phase 19B Streamlit OIDC configuration and secure credential provisioning`.
Expected next action: operator review then independent private preparation. STOP after report.
No credentials, VM activation, real login/inference or Phase19C.

End report and final response with these explicit evidence-derived values (allowed variants
shown here as instructions, not findings):

```text
PHASE19B_STREAMLIT_OIDC_PREPARATION: PASS/GAP/FAIL
ENTRA_API_CONFIGURATION: OPERATOR_REPORTED_PASS/GAP/FAIL
ENTRA_API_ROLE_ASSIGNMENT: OPERATOR_REPORTED_PASS/GAP/FAIL
ENTRA_BROWSER_REGISTRATION: OPERATOR_REPORTED_PASS/GAP/FAIL
ENTRA_REDIRECT_URI_ACCEPTANCE: OPERATOR_REPORTED_PASS/GAP/FAIL
ENTRA_BROWSER_SERVICE_PRINCIPAL: OPERATOR_REPORTED_PASS/GAP/FAIL
ENTRA_DELEGATED_PERMISSION: OPERATOR_REPORTED_PASS/GAP/FAIL
ENTRA_OPERATOR_SPECIFIC_CONSENT: OPERATOR_REPORTED_PASS/GAP/FAIL
ENTRA_CLIENT_CREDENTIAL_METADATA: OPERATOR_REPORTED_PASS/GAP/FAIL
EXACT_STREAMLIT_OIDC_CONFIGURATION: PASS/GAP/FAIL
API_IDENTITY_CONFIGURATION_COMPATIBILITY: PASS/GAP/FAIL
SECURE_PROVISIONING_PROCEDURE: PASS/GAP/FAIL
COOKIE_SECRET_GENERATION_PROCEDURE: PASS/GAP/FAIL
SYNTHETIC_PROVISIONING_VERIFICATION: PASS/GAP/FAIL
ACTUAL_CLIENT_SECRET_ACCESSED_BY_CODEX: YES/NO
ACTUAL_CREDENTIAL_ENCRYPTION_VERIFIED: YES/NO
OPERATIONAL_COOKIE_SECRET_CREATED: YES/NO
OPERATIONAL_STREAMLIT_TOML_CREATED: YES/NO
AZURE_STREAMLIT_CONFIGURATION_PROVISIONED: YES/NO
REAL_ENTRA_AUTHENTICATION: BLOCKED/VERIFIED
RUNTIME_SUBJECT_ENROLLMENT: BLOCKED/VERIFIED
APPLICATION_RUNTIME_CODE_CHANGED: YES/NO
APPLICATION_IMAGE_REBUILD_REQUIRED: YES/NO/REVIEW_REQUIRED
FOCUSED_REGRESSION_VERIFICATION: PASS/GAP/FAIL
FULL_REGRESSION_VERIFICATION: PASS/GAP/FAIL/NOT_REQUIRED
DOCUMENTATION_RECONCILIATION: PASS/GAP/FAIL
PRE_COMMIT_REVIEW: PASS/GAP/FAIL
AZURE_VM_ACTIVATED: YES/NO
ENTRA_MUTATIONS: YES/NO
REAL_INFERENCE_CALLS: <ACTUAL_COUNT>
PUBLIC_EXPOSURE_INTRODUCED: YES/NO
GIT_STAGED: YES/NO
GIT_COMMITTED: YES/NO
GIT_PUSHED: YES/NO
PHASE19A_STATUS: COMPLETE
PHASE19B_STATUS: ACTIVE
PHASE19C_STATUS: NOT_STARTED
NEXT_ACTION_READINESS: READY_FOR_OPERATOR_REVIEW/BLOCKED
```
