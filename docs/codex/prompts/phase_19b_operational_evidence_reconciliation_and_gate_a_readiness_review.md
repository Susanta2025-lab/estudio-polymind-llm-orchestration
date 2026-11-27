# Phase 19B — Operational evidence reconciliation and Gate A readiness review

Clean, repository-safe instruction record, 27 November 2026. The supplied master prompt
remains authoritative. This consolidated copy intentionally excludes workstation paths,
private network endpoints, operator directory identifiers and authentication-key inventory.
Actual secrets, tokens, passphrases, private keys and signed permissions must never be saved.
The operational observations are reconciled in the [report](../reports/phase_19b_operational_evidence_reconciliation_and_gate_a_readiness_review.md).

## Mission and phase boundary

Review completed operational identity, credential, PKI/TLS, Windows trust/resolution and SSH
preparation against actual source, deployment procedures, historical evidence and Gates A–E.
Establish auditable provenance, supersede stale current pending descriptions without changing
historical records, identify every Gate A blocker and prepare sequential future operator
provisioning/validation instructions. Decide whether Gate A can legitimately close.

This is an offline engineering/documentation task, not Azure deployment authorization.
19A COMPLETE; 19B ACTIVE; 19C NOT_STARTED. Do not introduce a phase/subphase or begin 19C.
Preserve provider neutrality, Chat/RAG/Documents, native Streamlit OIDC, Entra v2 verification,
RBAC/enrollment/ownership, seven SQLite authorities, independent governance/admission/execution,
Redis/Chroma, managed digestion, SSE → provider tokens → NDJSON, reviewed image/dependencies,
private Tailscale/OpenSSH and loopback-only HTTPS. No public VM IP or application exposure.

## Baseline and inspection

Read complete AGENTS.md and any applicable nested instructions. Before edits execute:

```bash
git status --short --branch
git rev-parse HEAD
git log --oneline --decorate -10
git diff --stat
git diff --check
git diff --cached --name-only
```

Inspect README; Phase 19 architecture, implementation plan and VM operations; Entra security
documentation; actual Compose/deployment configuration, manifest/enrollment/TLS/identity code;
relevant security, governance, admission, deployment/recovery and UI/API tests. Discover actual
paths. Read historical offline-foundation, post-Azure, private-HTTPS and OIDC preparation
prompts/reports, including integration-gap resolution. Preserve historical bytes.

Latest checkpoint title: `docs: prepare Phase 19B Streamlit OIDC configuration and secure credential provisioning`.
Operator CI: Estudio PolyMind CI, master, push, run 45788278749, SUCCESS, 11m38s. Reconcile
exact SHA through read-only GitHub if available. Do not fetch/pull or modify Git history.

Use explicit provenance: REPOSITORY_VERIFIED, INDEPENDENTLY_VERIFIED,
OPERATOR_REPORTED_PASS, OFFLINE_SYNTHETIC_PASS, PREPARED_NOT_EXECUTED, PENDING, BLOCKED,
NOT_AUTHORIZED, NOT_APPLICABLE. Reported output is valid evidence of the reported action;
it does not become independent verification.

## Supplied 26–27 November operational observations

Retain previously recorded tenant/API/browser registrations, v2 scope and exact role,
operator-only delegated consent, disabled implicit/public-client flows and one confidential
credential's metadata. Credential key ID is not its value. Actual credential validity,
authentication, token claims and API-token subject remain unverified.

Operator reports extracting/compiling the reviewed OIDC procedure, creating native TOML
with independently generated cookie secret, verifying private metadata, encrypting with
GPG AES-256 and comparing decrypted bytes. Redundant plaintext removed; only encrypted
staging remains. Azure installation and independent backup/recovery custody remain pending.
Preserve the cookie secret across ordinary restarts. Never inspect actual credential files.

Approved direct-root PKI: root 1825 days/180-day renewal lead; server 90 days/30-day lead;
CRL 7 days/1-day refresh lead; RSA3072/AES256 CA key, RSA2048 server key, SHA256 signatures,
DNS polymind.test; operator is CA/revocation/renewal custodian, current Windows user trust.
Root/leaf/key-match/chain/hostname/CRL issuance and local encrypted full-CA backup integrity
were reported PASS. Preserve exact public certificate dates/fingerprints in the report.
Never transfer CA key/full CA archive to Azure, containers or Windows trust storage.

Calculate precise UTC lifecycle deadlines from actual supplied expiration dates. No automatic
renewal, CRL distribution or browser CRL enforcement exists. Assess explicit manual-revocation
risk acceptance. Independent offline backup custody, passphrase custody and disaster restore
remain pending. Record resolved GPG terminal/zero-byte/noclobber failures and nonfatal cp -n
warning without claiming secure erasure.

Windows operator reports matching public DER SHA256, successful current-user-only root
installation without private key, hosts mapping 127.0.0.1 polymind.test and cache flush.
Trust is not browser acceptance and is not inherently restricted to that hostname.
Native OpenSSH/available local port/local Tailscale and endpoint identification passed;
VM peer offline is not independent Azure power evidence. Existing host-key records are TOFU;
independent VM host-key verification remains pending. Dedicated passphrase-protected SSH pair
matches its public fingerprint after resolved initial wrong-passphrase failure. Explicit
identity/IdentitiesOnly/strict checking are configured; agent stopped/disabled. No key replacement
is required. Keep host-specific endpoint/user/path/key inventory in a protected operator record.

## Complete Gate A and dependency review

Assess all runbook inputs: identity/role/consent/custody/enrollment/revocation; exact origin,
SAN/trust/CRL/lifecycle/tunnel/host authenticity/backups; immutable source SHA/ownership,
classification/rights/transmission/retention/current approval and privacy/consent/independent
semantic/session reviews; provider endpoint/deployment/version/type/region/auth/role maps,
managed prompt/schema and separate Chat capabilities/limits/usage; current tariff/currency,
owner/tenant budgets/request bounds/shared RPM/TPM/concurrency/consumers/exclusivity and
outstanding obligations; independent signing trust/operator/revocations/frozen resource,
scope/call/time binding. Historical Foundry evidence/permissions/prices confer no current authority.

Enrollment must be [issuer, tenant UUID, API access-token sub], never oid/ID-token sub/email.
Investigate identity bootstrap, manifest, native login, initialization and no-inference startup
dependencies from source. If no legitimate identity-only path exists, report the circular
dependency and propose a separately reviewable solution. Do not invent subjects, relax checks,
modify runtime or initialize production to bypass the blocker.

Recover recorded image ID/revision, Docker/Compose versions, vendor digests, disk UUID and
infrastructure configuration from existing records without contacting Azure. Preserve the
Azure-staged pinned Compose, never overwrite with portable vendor tags. VM reported deallocated.

## Future operator plan, prepared only

Before activation require fresh subscription/resource, UTC window, infrastructure ceiling,
activation cutoff/deallocation deadline, recovery/residual owners, backup custody/lifecycle
decisions and explicit inference prohibition. Do not request immediate activation.

Gate B: prepare exact identity/power/private-network, Tailscale, independent trusted-channel
host-key verification, strict SSH, UUID/mount/owner, image/vendor/staged-file provenance,
outbound enforcement and CPU/memory/disk checks. No public SSH or verification bypass.

Gate C: verify actual /etc/polymind/compose.env, secrets/provider, secrets/streamlit.toml,
secrets/tls.crt, secrets/tls.key and execution-authority contracts. Private runtime files
10001:10001/0600, regular/single-link/no symlink, protected traversal; state under approved root.
Review BatchMode=yes/sudo -n compatibility with locked Windows key and disabled agent. Prepare
a reviewed interactive alternative: no private-key copying, secret argv/env, unnecessary
plaintext staging, blanket sudo or trust bypass. Confirm new-state/reuse decisions; Redis/
Chroma readiness before explicit seven-authority initialization. No reset/delete on failure.

Gate D: correct data/API-runner/UI/gateway health ordering; loopback tunnel with dedicated
identity/strict verified host; hostname/chain/Host/WebSocket and native login/API-token/
enrollment/negative authorization/session/logout/expiry tests. No-inference only with existing
supported mechanisms, otherwise report the limitation. Gate E: stop admission, bounded settle,
UNKNOWN/reservation reconciliation, ordered shutdown, quiesced protected backup, measurements,
separately authorized restore, timely deallocation/current power proof and residual-cost evidence.
Never automatically delete Azure resources.

## Verification, documentation and handoff

Only offline source/verification/non-secret documentation and read-only GitHub are authorized.
No Azure CLI/API, Graph/Entra, VM/SSH/tunnel, private-key/personal secret/.env access, decryption,
Windows stores/hosts inspection, operational credentials/certificates, CA database mutations,
provider discovery/inference, production lifecycle, signing/permissions, public exposure,
new dependencies/infrastructure, application runtime edits or Git mutations.

Run focused discovered contract tests under established offline/no-dotenv/credential-isolation
and network controls. Full regression is optional for documentation-only changes. Record exact
commands/counts/warnings/limitations; validate local links, embedded Python compilation and
shell syntax without operational execution; git diff --check. Report defects instead of fixing
runtime outside scope. Separate engineering and pre-commit review, including provenance,
premature readiness, metadata/secret exposure, lifecycle dates, bootstrap, transfer privilege,
financial/security boundaries, stale instructions and history preservation. Final Git status,
diff statistics and empty-index evidence are mandatory.

Create this prompt and matching report; reconcile README, architecture/plan, VM and Entra docs
with dated current addenda and historical scope. Report the 18 requested sections, complete
Gate A matrix, Gate B–E plan, review acceptance gates and every requested machine-readable
status key. Proposed checkpoint only:
`docs: reconcile Phase 19B operational evidence and review Gate A readiness`.
No staging/commit/push. Stop at offline review and operator handoff; Gate A cannot close on
future promises, and review acceptance is separate from operational acceptance.
