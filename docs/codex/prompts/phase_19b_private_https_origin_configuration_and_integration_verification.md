# CODEX MASTER PROMPT — PHASE 19B
## PRIVATE HTTPS ORIGIN CONFIGURATION AND INTEGRATION VERIFICATION

**Project:** Estudio PolyMind — Provider-Neutral LLM Orchestration Platform
**Repository:** Susanta2025-lab/estudio-polymind-llm-orchestration
**Branch:** master
**Expected starting HEAD:** 1b11b3ab766240c162d1970bae438c00752c6c6f
**Phase:** 19 — Azure Linux VM Deployment and Real-Model Integration
**Stage:** 19B — Offline Implementation, Azure Deployment, Live Integration and Validation
**Task:** Private HTTPS origin configuration, offline integration verification and documentation reconciliation
**Execution environment:** Local WSL Ubuntu, estudio_polymind Python environment and Docker Desktop
**Date:** 25 November 2026
**Azure VM status:** Operator-reported deallocated
**Azure VM activation:** NOT AUTHORIZED
**Microsoft Entra mutations:** NOT AUTHORIZED
**Real-model inference:** NOT AUTHORIZED
**Public exposure:** NOT AUTHORIZED
**Git staging/commit/push:** NOT AUTHORIZED

Clean repository copy of the supplied instruction with formatting and repeated lists
consolidated. The supplied master prompt controls execution; this record grants no new authority.

# 1. OBJECTIVE AND MISSION

Continue existing Phase 19B live-deployment preparation without repeating completed engineering.
Establish a consistent explicitly selected private HTTPS origin across production templates,
native Streamlit OIDC, Microsoft Entra browser redirects, private hostname resolution,
Tailscale/OpenSSH, TLS identity/trust, exact HTTP Host/WebSocket Origin validation, offline
regression/integration and operational evidence reconciliation.

Selected private verification origin: `https://polymind.test:9443`.
Adoption in relevant repository templates and current operational documentation is authorized.
Actual cloud-side configuration, operational certificate provisioning, OS trust-store changes
and production activation are not authorized. Prefer configuration/documentation to application
code. Do not introduce infrastructure or redesign existing architecture for this hostname.

# 2. MANDATORY PROJECT-STAGE POLICY

- Phase 19A — Readiness Assessment: COMPLETE.
- Phase 19B — Offline Implementation, Azure Deployment, Live Integration and Validation: ACTIVE.
- Phase 19C — Final Documentation and Engineering Closure: NOT STARTED.

All task activities remain within 19B. Do not introduce 19D or new formal phases/subphases.
Task success does not complete 19B or establish production readiness.

# 3. MANDATORY REPOSITORY INSPECTION AND BASELINE PROTECTION

Before editing execute:

```bash
git status --short --branch
git rev-parse HEAD
git log --oneline -8
git diff --stat
git diff --check
git diff --cached --name-only
```

Verify actual baseline against `1b11b3ab766240c162d1970bae438c00752c6c6f`.
Investigate/document differences; never reset. Preserve all tracked/staged/untracked operator
work. Read complete root AGENTS.md and comply with architecture/configuration/security/
testing/Docker/Git requirements. Inspect actual consumers, tests and source before editing.

## 3.1 Phase 19 engineering records

- docs/codex/prompts/phase_19a_readiness_verification.md
- docs/codex/prompts/phase_19b_offline_implementation.md
- docs/codex/prompts/phase_19b_live_deployment_readiness_continuation.md
- docs/codex/prompts/phase_19b_post_azure_readiness_offline_validation_evidence_reconciliation.md
- docs/codex/reports/phase_19b_offline_implementation_and_verification.md
- docs/codex/reports/phase_19b_post_azure_readiness_offline_validation_evidence_reconciliation.md

Read Integration Gap Resolution and subsequent dated reconciliation records.

## 3.2 Deployment and security

Inspect docker-compose.phase19.yml, deployment/phase19/, compose.env.example,
configuration.example.json, gateway.py, ui.py, polymind.service, ui/tls_gateway.py,
docs/security/entra_v2.md, Dockerfile and .dockerignore. Locate actual native Streamlit OIDC
consumers/templates; do not assume a proposed template exists.

## 3.3 Operational documentation

Inspect README.md, docs/operations/phase_19_vm.md,
docs/evaluation/phase_19_deployment_architecture.md and
docs/evaluation/phase_19_implementation_plan.md.

## 3.4 Existing verification

Inspect tests/unit/test_phase19_tls.py, test_phase19_deployment.py,
test_phase19_chat_view.py; tests/integration/test_phase19_operator.py,
test_phase19_execution_bridge.py, test_phase19_authority_lifecycle.py; actual gateway,
native OIDC/Entra tests and the Phase 19 local container validation harness.

Search tracked source/templates/tests/docs for PHASE19_ORIGIN, polymind.private.example,
polymind.test, oauth2callback, redirect_uri, server_metadata_url, streamlit.toml, 9443,
127.0.0.1 and localhost. Classify references as current Phase 19 deployment configuration,
portable example, historical evidence, synthetic fixture, local development or unrelated
configuration. No indiscriminate repository-wide replacement.

# 4. ESTABLISHED PROJECT BASELINE AND OPERATOR EVIDENCE

## 4.1 Azure infrastructure

Preserve resource group rg-epolymind, VM vm-epolymind-dev, Spain Central, Standard_D2s_v4,
Ubuntu 24.04 LTS, 2 vCPU/8 GiB, separate 64-GiB OS/data disks, no public IP, existing private
Tailscale/OpenSSH, persistent ext4, Docker Engine/Compose, reviewed application/vendor images
and five services. VM remains operator-reported deallocated. No fresh independent Azure claim.

## 4.2 Microsoft Entra API registration

Operator-supplied configuration evidence, 25 November 2026:

| Field | Value |
|---|---|
| Display name | estudio-polymind-api-dev |
| API client UUID | 5aa70f9d-9f9e-4b5b-972b-698d4d68105e |
| Application ID URI | api://5aa70f9d-9f9e-4b5b-972b-698d4d68105e |
| API service principal object UUID | 046ce5b0-897c-4289-ad86-e403ac6b6e20 |
| Supported account type | AzureADMyOrg |
| Delegated scope | access_as_user |
| Application role | PolyMind.L1Operator |
| Application role UUID | e34bc374-42ff-4a6a-87e2-007b8cc788b3 |
| Role enabled / member type | true / User |

Operator verified exactly one API role assignment: User principal, principal UUID matched
signed-in operator's directory object, role UUID matched enabled PolyMind.L1Operator.
Record as operator-reported configuration verification, not real browser authentication or
API access-token verification. Never infer enrollment subject from directory object ID,
email, display name or ID-token subject. Keep environment IDs in scoped non-secret operational
configuration/records, never portable application logic.

## 4.3 Existing Entra inventory

Reported existing registrations: estudio-polymind-api-dev and estudio-polymind-cli-dev.
Proposed estudio-polymind-streamlit-dev was absent. Browser registration, service principal,
delegated permission, consent and confidential credentials remain pending.

# 5. SELECTED PRIVATE HTTPS CONFIGURATION

| Parameter | Selected value |
|---|---|
| Private hostname | polymind.test |
| Scheme | HTTPS |
| Browser-visible port | 9443 |
| Private origin | https://polymind.test:9443 |
| OIDC callback path | /oauth2callback |
| Exact redirect URI | https://polymind.test:9443/oauth2callback |
| Expected HTTP Host | polymind.test:9443 |
| Expected WebSocket Origin | https://polymind.test:9443 |
| Windows hostname mapping | 127.0.0.1 polymind.test |
| Local SSH bind / forwarding port | 127.0.0.1 / 9443 |
| Remote SSH forwarding target | 127.0.0.1:9443 |
| VM gateway host binding | 127.0.0.1:9443 |
| Gateway container port | 9443 |
| Certificate SAN | DNS:polymind.test |
| Certificate approach | Dedicated private CA-signed server certificate |
| Minimum TLS | TLS 1.2 |
| Public exposure | Prohibited |

`.test` is for bounded private verification, not a public production domain. No public DNS,
Azure DNS, Application Gateway, Load Balancer, public IP or public certificate issuance.
Remain configurable for another explicitly approved private hostname; no hardcoded gateway
hostname. Report exact verified Entra/Streamlit/browser/repository conflicts, never silently
substitute another origin.

# 6. MANDATORY SAFETY AND ARCHITECTURAL BOUNDARIES

## 6.1 Azure and Entra

No VM start/restart/resize/redeploy; new remote SSH; Azure network/NSG/NAT/disk/resource changes;
Entra application/service-principal creation/modification; delegated grants/admin consent;
client-secret creation/retrieval/rotation; real Entra login/token acquisition; production
Compose activation; Kubernetes/AKS. Prepare operator procedures only.

## 6.2 TLS and secret custody

No persistent operational CA keys, operational server generation/install, Windows/WSL trust
changes, hosts-file edits, browser verification disabling, SSH host verification disabling,
credential/token/private-key retrieval/printing or committed real env/native secrets.
Temporary synthetic certificates/keys only in isolated offline tests, never deployment reuse.

## 6.3 Provider and financial safety

No Foundry/OpenAI/external inference requests, real-credential readiness probes, live execution
permissions, financial reservations, tariff/budget/quota changes, historical obligation changes
or resets. Preserve provider/financial/execution governance. Zero real inference calls.

## 6.4 Runtime/persistence

Preserve five services, one API/runner, seven independent SQLite authorities, persistent
Redis/Chroma, source ownership/enrollment, independent execution permission, initialization/
serving separation, mount-aware systemd, Chat/RAG and Documents. No production authority
initialization/migration/rename/modification.

## 6.5 Git/dependencies

No staging/commit/push/reset/restore/stash/clean/rebase/GitHub settings, unnecessary dependencies,
new services/frameworks, unrelated refactor or unrelated image/volume/container deletion.

# 7. STAGE 1 — READINESS VERIFICATION

## 7.1 Private origin contract

Inspect entrypoint and consumers: explicit HTTPS; reject localhost/127.0.0.1/::1 browser hosts,
paths/query/fragment/userinfo; TLS/key loading, TLS minimum, PHASE19_ORIGIN, existing port,
exact Host/Origin. Determine need for code changes; expected generic configuration compatibility
must be verified, not assumed.

## 7.2 Compose contract

Verify `127.0.0.1:9443:9443`, no new ports/topology/public listeners/API/UI/Redis/Chroma
exposure/containers. TLS/native secret binds remain read-only, missing-source fail-closed.

## 7.3 Native OIDC

Inspect installed native authentication requirements and relationship among origin, redirect,
registered URI, tenant metadata, browser UUID, delegated API scope, token forwarding and API
identity/authorization. Find actual inert template and consistency validation/coverage gaps.

## 7.4 Private hostname/tunnel

Windows browser → polymind.test:9443 → Windows loopback → OpenSSH over Tailscale → VM
loopback:9443 → Docker gateway → Streamlit → FastAPI. Verify hosts resolution preserves URL,
HTTP Host and TLS identity. Distinguish Windows-native from WSL forwarding; no assumption
Windows-to-WSL localhost works. Prefer Windows-native OpenSSH absent equivalent safe evidence.

## 7.5 Private TLS trust

Assess exact DNS SAN, serverAuth usage, validity, complete chain, browser trust, CA/server-key
custody, renewal/revocation, restrictive ownership/modes. Operator reviews lifetimes/custodians;
do not select operational values independently.

## 7.6 Readiness output

Source-grounded PASS/GAP/FAIL/BLOCKED/NOT_APPLICABLE matrix, distinguishing existing
implementation, operator evidence, fresh offline verification, remaining operational/configuration
blockers and required changes. Proceed only with narrow justified in-scope changes.

# 8. STAGE 2 — CONFIGURATION IMPLEMENTATION AND OFFLINE VERIFICATION

## 8.1 Compose environment template

Replace `PHASE19_ORIGIN=https://polymind.private.example:9443` in
`deployment/phase19/compose.env.example` with `PHASE19_ORIGIN=https://polymind.test:9443`.
Document selected 19B private verification origin; retain inertness and all unrelated variables.
This origin must not validate otherwise incomplete production configuration.

## 8.2 Native OIDC template

Update suitable existing template; if absent, justify one minimal inert non-secret example
in Phase 19 deployment directory, not a duplicate. Represent:

```toml
[auth]
redirect_uri = "https://polymind.test:9443/oauth2callback"
server_metadata_url = "https://login.microsoftonline.com/<TENANT_UUID>/v2.0/.well-known/openid-configuration"
client_id = "<STREAMLIT_BROWSER_CLIENT_UUID>"
client_secret = "<SUPPLIED_PRIVATELY_BY_CUSTODIAN>"
cookie_secret = "<SUPPLIED_PRIVATELY_BY_CUSTODIAN>"
expose_tokens = ["access"]

[auth.client_kwargs]
scope = "openid api://<API_CLIENT_UUID>/access_as_user"
```

Verify installed Streamlit/consumer fields and retain additional required settings. Separately
document environment scope `api://5aa70f9d-9f9e-4b5b-972b-698d4d68105e/access_as_user`.
Tenant/browser UUIDs remain operator-supplied. Placeholders are not verified operational
credentials/IDs. Examples must not become unintended runtime secrets or override configuration.

## 8.3 Gateway/consistency

Verify generic support, no hostname hardcoding. For material origin/callback/native mismatch
vulnerability, establish requirement and configuration boundary, add focused regression, apply
smallest compatible correction preserving portability. Avoid separate configuration framework
or redundant sources of truth. Contract: `redirect_uri = PHASE19_ORIGIN + "/oauth2callback"`.

## 8.4 Proposed Entra browser procedure

Prepare, never execute: estudio-polymind-streamlit-dev, AzureADMyOrg, Web, confidential web
application, exact `https://polymind.test:9443/oauth2callback`, delegated access_as_user on API
client 5aa70f9d-9f9e-4b5b-972b-698d4d68105e. Verify code-flow/confidential requirements against
authoritative Microsoft/Streamlit docs when accessible. Individually reviewable steps:

1. Application inventory and duplicate protection.
2. API scope UUID discovery.
3. Dedicated browser registration.
4. Exact Web redirect configuration.
5. Service principal creation if required.
6. Delegated API permission configuration.
7. Required consent assessment.
8. Private confidential credential provisioning.
9. Read-only registration verification.

Never modify API/CLI apps; no unnecessary Graph permissions/broad tenant privileges/implicit
or public-client flows without independent justification. No acceptance claim until authorized
registration verifies actual URI. Credential procedure must avoid secret terminal output,
history, logs and chat.

## 8.5 Windows hostname/SSH procedure

Prepare hosts mapping `127.0.0.1 polymind.test`, standard hosts path, and shell-appropriate
equivalent to:

```bash
ssh -N -T -o ExitOnForwardFailure=yes -o StrictHostKeyChecking=yes \
 -L 127.0.0.1:9443:127.0.0.1:9443 <VERIFIED_VM_SSH_TARGET>
```

Use verified Tailscale/OpenSSH endpoint evidence if available; otherwise explicit placeholder.
Never invent username/IP/name/host fingerprint. Include local port availability, existing
host-key verification, Windows resolution verification, private browser and controlled tunnel
shutdown. Do not execute tunnel or edit hosts.

## 8.6 Private TLS provisioning procedure

Reproducible reviewed dedicated CA/server-key/issuance with DNS SAN polymind.test, serverAuth,
required chain, Windows browser trust, protected CA custody, secure key transfer, renewal/
revocation and trust removal. Respect `/etc/polymind/secrets/tls.crt` and `tls.key`,
10001:10001, 0600, regular files/no symlinks. Verify host directory traversal/container mounts.
No CA key on VM/image; browser only public trust material. No operational generation/install.

## 8.7 Focused regression

Inspect existing coverage and reuse synthetic temporary material. Positive: selected origin,
exact Host/WS Origin, callback traversal, hostname-verified TLS handshake/SAN/TLS minimum,
Compose loopback mapping and configurable other private names. Negative: HTTP/localhost/
loopback origins, paths/query/fragment, wrong Host, wrong/absent required WS Origin,
missing/invalid/untrusted/wrong-SAN TLS, unsafe permissions/symlink secrets, forwarded-header
bypass, backend admin/health non-exposure, authentication and execution boundaries.
Do not rewrite synthetic fixture domains just for resemblance; add narrow exact selection
coverage where missing.

## 8.8 Compose/local integration

Inspect invocation and run inert Compose parse, e.g.:

```bash
docker compose --env-file deployment/phase19/compose.env.example \
 -f docker-compose.phase19.yml config --quiet
```

No production activation. Local integration uses dedicated temporary state, synthetic
credentials/certs, no real Entra/provider, no production paths/public exposure. Reuse harness;
no unnecessary expensive five-service repeats for config/docs changes with adequate coverage.
Explain omitted integration scope.

## 8.9 Required regression execution

Focused first, actual TLS/gateway/deployment/native OIDC/Entra tests. At minimum assess:

```bash
python -m pytest -q tests/unit/test_phase19_tls.py \
 tests/unit/test_phase19_deployment.py tests/unit/test_phase19_chat_view.py \
 tests/integration/test_phase19_operator.py tests/integration/test_phase19_execution_bridge.py
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python -m pytest -q
```

Use existing mechanisms preventing real cloud/provider interactions; HF flags alone do not
prove all network disabled. Exclude actual infrastructure/credential-dependent external checks
with reasons. External-cache compilation, configured lint/type tools, TOML/config parsing,
inert Compose and git diff --check. Record exact commands/exits/pass/fail/skip/error/warnings,
durations, failures/corrections/retests and omissions. Never add overlapping suite counts.

## 8.10 Image/deployment provenance

Determine runtime Python/configuration/Dockerfile/dependency/build-context/behavior/image/
Azure-staged-template effects. Separate runtime from docs/external config. Identify exact
reason/future action for rebuild/revalidation/transfer. Never claim reviewed Azure image has
new runtime files. No unnecessary large rebuild/transfer or silent image identity replacement.

# 9. STAGE 3 — DOCUMENTATION AND EVIDENCE RECONCILIATION

## 9.1 Prompt

Inspect before overwriting; save clean Markdown at
`docs/codex/prompts/phase_19b_private_https_origin_configuration_and_integration_verification.md`.

## 9.2 Current operational docs

Update materially relevant VM runbook, architecture, implementation plan, README and deployment
docs with selected origin/callback/SAN/Windows mapping/VM loopback. Current Gate A: repository
origin selected, operator API role configuration verified, browser registration/identity/consent
pending, actual issuance/trust pending, API access-token subject enrollment pending, browser
auth pending, production activation pending. Preserve unrelated blockers, historical reports
and prior PASS/GAP/FAIL. Dated addenda for reconciliation. Do not change unrelated dev/test origins.

## 9.3 Comprehensive report

Create `docs/codex/reports/phase_19b_private_https_origin_configuration_and_integration_verification.md`:

1. Executive summary.
2. Actual starting Git baseline.
3. Scope/authorization.
4. Sources/provenance.
5. Operator Entra evidence.
6. Initial readiness.
7. Selected configuration.
8. Architecture compatibility.
9. Configuration/implementation changes.
10. Native OIDC contract.
11. Proposed browser registration.
12. Windows resolution/tunnel.
13. TLS provisioning/trust.
14. Exact regression/integration evidence.
15. Image/deployment provenance.
16. Engineering self-review.
17. Pre-commit review.
18. Blockers/operator decisions.
19. Final readiness matrix.
20. Next live-verification recommendation.
21. Git handoff.

Explain sufficiently for independent review. Distinguish historical repository evidence,
operator external evidence, fresh offline tests, proposed future procedures and unverified live.

## 9.4 Self-review

Complete diff: config/callback/TLS hostname consistency, secrets/network/SSH/browser trust,
provider neutrality/compatibility/coverage/dependencies/abstractions, readiness claims and
unrelated changes. Correct material findings and repeat affected tests.

## 9.5 Separate pre-commit review

```bash
git status --short --branch
git diff --stat
git diff --name-status
git diff --check
git diff --cached --name-only
```

Inspect untracked separately. No real credentials/secrets/tokens/CA/server private keys/native
secrets/runtime DBs/generated certs/temp/binaries/unnecessary duplication/unsupported live
claims. Leave uncommitted; provide candidate files/proposed message.

# 10. ACCEPTANCE GATES

1. Baseline PASS only actual Git recorded/operator work preserved.
2. Consistency PASS only selected origin/callback/Host/WS/SAN/tunnel port consistently documented/templates.
3. Architecture PASS only five services/private bind/provider-neutral boundaries preserved.
4. TLS/gateway PASS only applicable positive/negative tests executed.
5. OIDC readiness PASS only registration/redirect/scope/private credentials established;
   actual registration/auth separate.
6. Regression PASS only required checks successful/findings resolved; unexecuted never PASS.
7. Documentation PASS only consistent reproducible reviewable current procedures.
8. Security/Git PASS only no unauthorized cloud/credentials/inference/production/Git mutation.

# 11. REQUIRED FINAL READINESS MATRIX

| Area | Allowed status |
|---|---|
| Repository baseline | PASS/GAP/FAIL |
| Selected private origin | PASS/GAP/FAIL |
| Deployment consistency | PASS/GAP/FAIL |
| Native OIDC template | PASS/GAP/FAIL |
| Entra API role | OPERATOR_REPORTED_PASS/GAP/FAIL |
| Browser registration | PENDING/VERIFIED |
| Entra redirect acceptance | PENDING/VERIFIED |
| Offline TLS | PASS/GAP/FAIL |
| Gateway Host/Origin | PASS/GAP/FAIL |
| SSH procedure | PASS/GAP/FAIL |
| Actual Windows resolution | PENDING/VERIFIED |
| Operational TLS provisioning | PENDING/VERIFIED |
| Actual browser trust | PENDING/VERIFIED |
| Real Entra browser auth | BLOCKED/VERIFIED |
| Runtime subject enrollment | BLOCKED/VERIFIED |
| Production HTTPS | BLOCKED/VERIFIED |
| Regression | PASS/GAP/FAIL |
| Documentation | PASS/GAP/FAIL |
| Pre-commit | PASS/GAP/FAIL |

Configured readiness is not operational readiness; offline TLS is not browser trust;
Entra role assignment is not authenticated access.

# 12. FINAL STATUS CONTRACT

End report and final response with explicit evidence-derived values, not desired outcomes:

```text
PHASE19B_PRIVATE_ORIGIN_CONFIGURATION: PASS/GAP/FAIL
SELECTED_PRIVATE_ORIGIN: https://polymind.test:9443
SELECTED_OIDC_REDIRECT_URI: https://polymind.test:9443/oauth2callback
CONFIGURATION_CONSISTENCY: PASS/GAP/FAIL
ARCHITECTURE_COMPATIBILITY: PASS/GAP/FAIL
OFFLINE_TLS_VERIFICATION: PASS/GAP/FAIL
GATEWAY_SECURITY_VERIFICATION: PASS/GAP/FAIL
STREAMLIT_OIDC_CONFIGURATION: PASS/GAP/FAIL
ENTRA_API_ROLE_ASSIGNMENT: OPERATOR_REPORTED_PASS/GAP/FAIL
ENTRA_BROWSER_REGISTRATION: PENDING/VERIFIED
ENTRA_REDIRECT_URI_ACCEPTANCE: PENDING/VERIFIED
SSH_TUNNEL_PROCEDURE: PASS/GAP/FAIL
OPERATIONAL_TLS_PROVISIONING: PENDING/VERIFIED
BROWSER_CERTIFICATE_TRUST: PENDING/VERIFIED
REAL_ENTRA_AUTHENTICATION: BLOCKED/VERIFIED
RUNTIME_SUBJECT_ENROLLMENT: BLOCKED/VERIFIED
PRODUCTION_PRIVATE_HTTPS: BLOCKED/VERIFIED
APPLICATION_RUNTIME_CODE_CHANGED: YES/NO
APPLICATION_IMAGE_REBUILD_REQUIRED: YES/NO/REVIEW_REQUIRED
AZURE_STAGED_CONFIGURATION_UPDATE_REQUIRED: YES/NO
FOCUSED_REGRESSION_VERIFICATION: PASS/GAP/FAIL
FULL_OFFLINE_REGRESSION_VERIFICATION: PASS/GAP/FAIL
DOCUMENTATION_RECONCILIATION: PASS/GAP/FAIL
PRE_COMMIT_REVIEW: PASS/GAP/FAIL
AZURE_VM_ACTIVATED_DURING_TASK: YES/NO
ENTRA_MUTATIONS_DURING_TASK: YES/NO
OPERATIONAL_CERTIFICATES_CREATED: YES/NO
PRODUCTION_AUTHORITIES_MODIFIED: YES/NO
PRODUCTION_SERVICES_ACTIVATED: YES/NO
REAL_INFERENCE_CALLS_DURING_TASK: <ACTUAL_COUNT>
PUBLIC_EXPOSURE_INTRODUCED: YES/NO
GIT_STAGED: YES/NO
GIT_COMMIT_CREATED: YES/NO
GIT_PUSH_PERFORMED: YES/NO
PHASE19A_STATUS: COMPLETE
PHASE19B_STATUS: ACTIVE
PHASE19C_STATUS: NOT_STARTED
NEXT_ACTION_READINESS: READY_FOR_OPERATOR_REVIEW/BLOCKED
```

# 13. FINAL HANDOFF AND STOP CONDITION

Concise summary; created/modified files; whether code needed; exact regressions; final readiness
matrix; operational decisions; image/Azure-staged changes; proposed message; confirm no Git
stage/commit/push; recommend separately authorized next action. Suggested message:

```text
chore: configure Phase 19B private HTTPS origin and verify deployment integration
```

Expected next action after review/approval: register dedicated estudio-polymind-streamlit-dev
with `https://polymind.test:9443/oauth2callback`. Report blocking offline compatibility instead
if found. STOP after handoff: no registration, operational certificates, VM activation, live
inference or Phase 19C.

END OF CODEX MASTER PROMPT
