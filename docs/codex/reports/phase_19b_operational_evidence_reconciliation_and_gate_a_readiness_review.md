# Phase 19B — Operational evidence reconciliation and Gate A readiness review

27 November 2026. **Offline review complete; operational Gate A BLOCKED.**
Phase 19A COMPLETE; Phase 19B ACTIVE; Phase 19C NOT_STARTED.
This report and its [sanitized instruction record](../prompts/phase_19b_operational_evidence_reconciliation_and_gate_a_readiness_review.md)
authorize no deployment, identity administration, production initialization or inference.

## 1. Executive summary

The supplied observations resolve several previously pending **local preparation** items at
OPERATOR_REPORTED_PASS level: native Streamlit configuration and independent cookie generation,
encrypted staging/content comparison/plaintext cleanup, approved PKI policy, root/leaf issuance
and key matching, initial CRL, local encrypted PKI backup, Windows current-user public-root
installation, hostname resolution and dedicated SSH-key readiness. None establishes actual
Entra credential validity, a running private tunnel, deployed TLS or browser/API acceptance.

Gate A cannot close. Missing API-token subject and owner-bound source approval prevent
legitimate production initialization. Standard Compose startup depends on API readiness before
UI login, creating a bootstrap dependency with no supported identity-only acquisition command.
Current source/privacy/semantic, provider/capability, finance/shared quota/obligation and
independent execution inputs are also absent. The earlier BatchMode transfer recipe is
incompatible with the reported locked Windows key/disabled agent. A reviewed encrypted-file,
interactive SSH alternative is prepared below; it still needs authorized remote prerequisites
and actual Windows/VM validation. No runtime change is needed to adopt the supplied TLS/OIDC
configuration. A narrow identity-bootstrap implementation is recommended for separate review.

No operational files were opened. No Azure/Entra/provider/remote SSH operation occurred.
Only seven Markdown files are candidates for review; application, tests, deployment artifacts,
dependencies and historical reports/prompts are unchanged. No image rebuild is required.

## 2. Repository and CI baseline

Complete root AGENTS.md was read. Repository instruction discovery found no nested AGENTS.md.
Before edits, all mandated commands exited 0:

```bash
git status --short --branch
git rev-parse HEAD
git log --oneline --decorate -10
git diff --stat
git diff --check
git diff --cached --name-only
```

Status was only `## master...origin/master`; tracked/untracked changes, diff/stat and index
were empty. HEAD: **`f5343e46054d1ef2110307bdf941ebce6a3fd9a4`**. Local origin/master points
there too; no fetch was performed. Last ten commits, in order:

```text
f5343e4 docs: prepare Phase 19B Streamlit OIDC configuration and secure credential provisioning
e0ad729 chore: configure Phase 19B private HTTPS origin and verify deployment integration
1b11b3a docs: reconcile Phase 19B Azure evidence and verify offline readiness
7bf82dc feat: complete Phase 19B offline Azure deployment foundation
b48dde4 feat: improve local app launchers and document frontend reliability
d7d2ec2 fix(ui): resolve Streamlit document module collision and preserve legacy chat
6aedae3 docs: finalize Phase 18 local engineering closure and deployment handoff
f7d091a feat(documents): implement authenticated local document frontend and verification
f0e420b docs: assess Phase 18 frontend integration and Azure deployment readiness
faaddc2 docs: finalize Phase 17I engineering closure with external verification deferred
```

**INDEPENDENTLY_VERIFIED:** GitHub connector GET of
`/repos/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/45788278749` confirms
[Estudio PolyMind CI run 45788278749](https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/45788278749):
master, push, completed/success, attempt 1, head SHA exactly matching HEAD and checkpoint title.
`run_started_at=2026-11-26T09:02:15Z`, `updated_at=2026-11-26T09:13:53Z`; their interval is
698 seconds (11m38s), consistent with the reported duration. Updated time is not a separately
provided job-completion timestamp. This CI validates the checkpoint, not these uncommitted docs.

## 3. Evidence provenance methodology

| Classification | Meaning in this review |
|---|---|
| REPOSITORY_VERIFIED | Directly inspected source/configuration/history; establishes a contract, not deployment |
| INDEPENDENTLY_VERIFIED | Newly observed read-only CI or deterministic arithmetic/static verification |
| OPERATOR_REPORTED_PASS | Supplied executed operator observations; not re-executed by Codex |
| OFFLINE_SYNTHETIC_PASS | Newly executed isolated tests with synthetic identities/credentials/adapters |
| PREPARED_NOT_EXECUTED | Future procedure/design; no operational acceptance |
| PENDING | Required evidence or decision absent |
| BLOCKED | A prerequisite prevents completion |
| NOT_AUTHORIZED | Outside this task's authority, even if technically feasible |
| NOT_APPLICABLE | Deliberately excluded requirement, with reason |

Evidence classifications apply to individual claims. A reported pass does not promote the
associated deployed acceptance to PASS. Historical independent observations retain their date
and scope. Existing reports were hashed before editing (215 tracked prompt/report files) for
byte-preservation verification. Current dated addenda supersede old pending descriptions only
for the actions now supported by evidence; historical records are not rewritten.

Inspected sources include [runtime](../../../deployment/phase19/runtime.py),
[lifecycle](../../../deployment/phase19/__main__.py),
[storage](../../../deployment/phase19/storage.py), [backup](../../../deployment/phase19/backup.py),
[Compose](../../../docker-compose.phase19.yml), its examples/service/gateway/UI,
[Entra verifier](../../../security/identity.py), [security runtime](../../../security/runtime.py),
[middleware](../../../api/security.py), [operator app](../../../documents/operator/app.py),
[workflow](../../../documents/operator/service.py), [pilot records](../../../documents/pilot/models.py),
[execution verifier](../../../security/execution.py), Chat/UI/token forwarding, provider factory,
governance/admission and applicable tests. The historical foundation prompt/report, including
Integration Gap Resolution, post-Azure reconciliation, private-HTTPS and OIDC preparation
records were consulted. Their original disabled-Chat/permission-gap findings are superseded
by the implemented integration; those gaps are not reopened here.

Private VM endpoint, SSH user, identity path, workstation/account identifiers and full key
inventory belong in the operator's protected deployment record. Public certificate fingerprints
and already recorded image/mount identities below support verification. No new private topology
inventory is published. This is an intentionally minimized record of the supplied prompt.

## 4. Operational identity reconciliation

**OPERATOR_REPORTED_PASS:** single tenant `afabeaf8-0fea-42c9-afb4-7e5c07eff3f3`;
API `estudio-polymind-api-dev`, client `5aa70f9d-9f9e-4b5b-972b-698d4d68105e`, URI
`api://5aa70f9d-9f9e-4b5b-972b-698d4d68105e`; v2 access tokens, enabled delegated
`access_as_user`, exact user role `PolyMind.L1Operator` and operator assignment.
Browser `estudio-polymind-streamlit-dev`, client `a43f5479-4cbd-45a0-86e0-9c658e77d133`,
single-tenant Web registration, enabled service principal, accepted exact callback
`https://polymind.test:9443/oauth2callback`, delegated API permission and persisted
principal-specific consent. Tenant-wide consent was not granted. Both implicit issuance
switches and public-client fallback are disabled. No repeat registration/consent is called for.

Application/service-principal object IDs and scope/role IDs remain recorded in the
[previous identity report](phase_19b_streamlit_oidc_configuration_preparation.md#4-reconciled-entra-registration-evidence);
the newly supplied values agree. None is an API access-token subject. Their omission here
avoids another operational inventory without discarding existing evidence.

**REPOSITORY_VERIFIED:** native unnamed `[auth]` configuration has exact callback,
tenant-specific `server_metadata_url`, browser client ID, privately supplied client/cookie
secrets, `expose_tokens=["access"]`, and
`[auth.client_kwargs] scope="openid api://5aa70f9d-9f9e-4b5b-972b-698d4d68105e/access_as_user"`.
The portable [template](../../../deployment/phase19/streamlit.secrets.example.toml) stays generic.
Streamlit's installed helper/template tests pass without contacting discovery. No Graph scope
or ID token is substituted. The API uses the bare API client UUID as audience, tenant-specific
`https://login.microsoftonline.com/<tenant>/v2.0` issuer and
`https://login.microsoftonline.com/<tenant>/discovery/v2.0/keys` JWKS.

The verifier checks RS256/key/header, scalar audience, issuer/tid/ver, delegated API scope,
exact role set, integer times/lifetime and nonempty subject; it rejects app/ID/wrong-audience
tokens and token-selected trust. Middleware registers only verified principals; workflow and
Chat separately enforce enrollment/owner. Revocation/epoch/scope checks still guard release.
Real token claims, credential exchange, native login/logout/expiry and deployed API acceptance
are **PENDING/BLOCKED**, not consequences of registration metadata.

## 5. Credential preparation and custody

The single confidential credential metadata remains **OPERATOR_REPORTED_PASS**:
description `polymind-streamlit-phase19b-dev`, key ID `7319515e-0342-4c8e-aacb-b5c663c8cda9`,
expiration `2027-05-25T07:24:50.834Z`. The key ID is not the secret. No actual value was supplied
to or accessed by Codex, and successful local TOML parsing cannot prove Entra accepts it.

Operator extraction and Python syntax checks passed; preparation directory 0700/script 0600.
Hidden terminal input supplied the existing secret. Independent CSPRNG cookie generation
and configuration verification passed: uid/gid 1000:1000, mode 0600, regular, one hard link,
516 bytes. GPG AES256.CFB/one-passphrase encryption and decrypt/byte comparison passed.
Redundant plaintext was removed; remaining `streamlit.toml.gpg` is reported 474 bytes,
0600, in a 0700 directory, UID:GID 1000:1000. Each is **OPERATOR_REPORTED_PASS**, not independent
Codex inspection. No Azure installation occurred. Preserve this cookie through ordinary
deployment/restarts; rotation is a deliberate session-invalidating security change.

Independent encrypted recovery-copy location/custody, passphrase custody and restoration
acceptance are **PENDING**. The encrypted artifact is local staging, not proof of independent
backup. Ordinary unlinking does not establish secure deletion of historical storage copies.

## 6. PKI/TLS evidence and lifecycle

**OPERATOR_REPORTED_PASS:** approved development policy is direct root-to-leaf, no intermediate;
root 1825 days/renew 180 days early; server 90 days/renew 30 early; CRL 7 days/refresh 1 day early;
RSA 3072-bit CA key encrypted AES256, RSA 2048-bit unattended server key, SHA256 signatures,
DNS `polymind.test`. Project operator owns CA custody, renewal and revocation. Trust scope is
the current Windows account. OpenSSL reported 3.0.13. No Vault/public PKI/automation is introduced.

| Certificate | Reported public evidence |
|---|---|
| Root | Subject=issuer `CN=PolyMind Phase19 Private Verification CA`; critical CA:TRUE/pathlen:0; critical certificate-sign/CRL-sign; validity `2026-11-26T12:23:59Z` to `2031-11-25T12:23:59Z` |
| Root SHA256 | `DC:80:BD:D2:B4:97:87:C5:01:2B:B8:B3:A2:3D:24:70:12:8F:D5:70:FA:6E:A4:70:B8:CC:9D:B5:8B:B2:39:1C` |
| Server | Subject `CN=polymind.test`, issuer=root above; critical CA:FALSE; critical digital-signature/key-encipherment; serverAuth EKU; SAN DNS:polymind.test; validity `2026-11-26T12:43:03Z` to `2027-02-24T12:43:03Z` |
| Server SHA256 | `73:C9:F8:93:BF:4F:9F:C0:1F:CC:01:63:90:92:41:EA:3D:70:CD:98:59:62:81:FA:A6:36:5F:9A:92:D7:75:37` |

Self/chain/hostname checks, CSR verification, root-key match/encryption, server-key match,
issuance-database update and certificate-copy verification passed according to the operator.
CA workspace 0700, CA key/cert and leaf key/cert0600, UID:GID 1000:1000. `cp -n` produced a
nonfatal portability warning; subsequent copy/chain/key verification passed. This does not
justify repeating issuance. The unencrypted server key is intentional for unattended startup:
permissions, encrypted recovery, controlled transfer and access restrictions are essential.
The CA private key and complete CA backup must never enter Azure, Docker or Windows trust.

Initial CRL: **OPERATOR_REPORTED_PASS**, generation/signature `verify OK`, number 0x01,
none revoked, leaf revocation check OK, mode 0600. Last update `2026-11-26T12:49:29Z`,
next update `2026-12-03T12:49:29Z`. A successful local check covers that CRL/time only.

**INDEPENDENTLY_VERIFIED arithmetic**, Python timezone-aware timedelta and separate GNU
`date -u` calculations agreed:

| Manual action | Exact UTC deadline / boundary |
|---|---|
| Refresh initial CRL (one day early) | `2026-12-02T12:49:29Z`; current CRL expires `2026-12-03T12:49:29Z` |
| Renew server (30 days early) | `2027-01-25T12:43:03Z`; current leaf expires `2027-02-24T12:43:03Z` |
| Renew root (180 days early) | `2031-05-29T12:23:59Z`; root expires `2031-11-25T12:23:59Z` |
| Existing Entra client credential expiry | `2027-05-25T07:24:50.834Z`; no new rotation lead time has been approved |

These are deadlines, **not scheduled jobs**. At each later session recompute freshness against
the actual renewed artifacts; do not assume this initial CRL remains current. No automated CRL
publication/distribution, browser revocation enforcement or certificate renewal exists. The
gateway loads certificates at startup; verified replacement requires controlled restart.

An explicit operator acceptance of this manual revocation limitation is **PENDING and required
before Gate A closure**. Approval of certificate lifetimes alone does not accept the absence
of effective browser revocation. Accept only for bounded private development, with named owner,
deadline tracking and a rehearsable compromise procedure: stop gateway/tunnel/admission,
withdraw the exact compromised root from current-user trust where necessary, replace leaf or
root according to compromise scope, update revocation records/CRL offline, distribute verified
public trust changes and revalidate before restart. Issuing a CRL alone cannot invalidate a
browser connection here. Leaf-key compromise needs immediate containment; CA-key compromise
requires root trust withdrawal/replacement. No compromise action was executed in this review.

Local encrypted full-CA archive `phase19-private-ca-20261126.tar.gpg`: reported AES256.CFB,
8473 bytes, directory 0700/file 0600, UID:GID 1000:1000; decrypt/archive comparison passed.
There was no intermediate plaintext archive. Independent offline location, passphrase custody
and actual disaster restoration remain **PENDING**. Comparing a decrypted archive to its
source is an integrity check, not a disaster-recovery rehearsal.

## 7. Windows trust and hostname resolution

**OPERATOR_REPORTED_PASS:** exported public DER SHA256 was identical in WSL and Windows,
`dc80bdd2b49787c5012bb8b3a23d2470128fd570fa6ea470b8cc9db58bb2391c`, matching the root
certificate fingerprint. Current-user root import succeeded with the expected subject;
Current-user=True, Machine-wide=False, HasPrivateKey=False. Windows SHA1 store identifier
`D2E4B1A0C7E0A62AE3C44820FE0AB2F4E05FA2C0` is not the approved SHA256 identity check.
Machine-wide installation is **NOT_APPLICABLE**, deliberately unapproved/unnecessary.

Current-user root trust can authorize other otherwise valid certificates issued by this CA;
it is not intrinsically restricted to polymind.test. No name constraints or per-host browser
pinning are claimed. Current-user trust configuration is complete as reported, while real
browser chain/name acceptance is pending. Codex inspected no Windows store.

No prior hosts mapping/resolution was reported. Elevated PowerShell installed
`127.0.0.1 polymind.test`, flushed DNS cache and confirmed loopback resolution. This is
**OPERATOR_REPORTED_PASS**. A backup procedure was supplied; hosts-backup completion is
**PENDING evidence**. Resolution neither starts a tunnel nor establishes remote gateway health.

## 8. SSH readiness and authentication evidence

**OPERATOR_REPORTED_PASS:** native Windows OpenSSH exists, OpenSSH_for_Windows_9.5p2 /
LibreSSL 3.8.2; local port 9443 available at observation time. Local Tailscale Running/Online=True;
the identified VM peer is **Online=False**. The workstation is online; the VM peer is offline.
Its state is consistent with reported deallocation, not an Azure power-state query.

Existing VM endpoint known_hosts entries cover ED25519/RSA/ECDSA and historical TOFU.
The reported accepted ED25519 and dedicated authentication-key public fingerprints are retained
in the protected operator record; neither is independently reverified here. Never confuse
server-host fingerprint with client-authentication fingerprint. Known-host presence proves
neither Azure provenance nor a fresh authentication. The dedicated
`id_ed25519_polymind_azure` pair matched after successful passphrase-protected public derivation.
Earlier wrong-passphrase failure is resolved; no key replacement is warranted. Reported ACL
contains owner, SYSTEM and Administrators; no independent effective-ACL audit occurred.

Effective configuration selects port 22, explicit dedicated identity, IdentitiesOnly=yes and
StrictHostKeyChecking=true. Agent stopped/disabled is compatible with **interactive** `-i`
authentication. The prior driver instead sets BatchMode=yes and has no approved unlocked
agent/key: it cannot request that passphrase. It also assumes existing `sudo -n` authority
for an arbitrary Python command, which has not been evidenced. **The prior transfer procedure
is BLOCKED for this workstation arrangement**, despite historical synthetic receiver checks.
Its source file has also been removed in favor of encrypted staging, so it cannot be rerun
unchanged. Section 13 provides an alternative without weakening either key protection or sudo.

Independent host authenticity, remote SSH authentication, forwarding and deployed HTTPS all
remain **PENDING/NOT_AUTHORIZED in this task**. No endpoint, private key or Windows personal
configuration was accessed, and no SSH connection was attempted.

## 9. Security limitations and resolved failures

| Observation | Reconciliation |
|---|---|
| Initial PKI backup agent/terminal failure | Operator-reported `Inappropriate ioctl for device` / cancelled operation; produced zero bytes, not a backup |
| noclobber blocked retry | Correct refusal to overwrite remaining empty artifact; operator confirmed/removes only that empty file, configured GPG_TTY/agent terminal and succeeded |
| Successful final PKI backup | Reported creation/integrity pass supersedes failed attempts; no independent offline custody/restore follows |
| Initial SSH passphrase error | Resolved by successful derivation and matching public fingerprint; no cryptographic key failure established |
| cp -n warning | Nonfatal portability warning; later issuance/copy/chain/key checks passed |
| Local plaintext cleanup | Reported redundant TOML removed; no secure-erasure or all-historical-copies claim |
| Trust/CRL limitations | Trust extends beyond hostname; no automatic browser CRL enforcement; explicit risk decision remains |
| Topology/health limitations | Internal networks and TCP gateway probe do not prove destination filtering, TLS/name/cookie/login or billing authorization |

## 10. Complete Gate A readiness matrix

The governing definition is [Gate A — Freeze operator-controlled inputs](../../operations/phase_19_vm.md#next-authorized-session--gates-ae)
and its full input table. A1–A5 independent approval decisions in the
[implementation plan](../../evaluation/phase_19_implementation_plan.md#independent-approval-gates)
remain distinct from operational Gates A–E. No gate is silently relaxed here.

| Group / required evidence | Current provenance/status | Remaining closure evidence |
|---|---|---|
| Tenant/API v2 registration, scope/role | OPERATOR_REPORTED_PASS | Real scoped-token validation later |
| Browser Web callback/SP/disabled implicit and public fallback | OPERATOR_REPORTED_PASS | Native exchange/callback acceptance later |
| Delegated permission and operator-only persisted consent | OPERATOR_REPORTED_PASS | Actual delegated access token; no consent expansion |
| Native field/origin contract | REPOSITORY_VERIFIED; OFFLINE_SYNTHETIC_PASS | Compare all installed external files without secrets |
| Client metadata | OPERATOR_REPORTED_PASS | Current validity/rotation custody |
| Operational TOML/cookie/encryption/cleanup | OPERATOR_REPORTED_PASS | Independent custody/recovery and remote installation |
| Credential exchange validity | PENDING | Separately authorized actual Entra login |
| API access-token sub | BLOCKED | Verified token for correct audience and browser flow; private tuple |
| Enrollment and canonical owner/tenant binding | BLOCKED | Subject first, stable_id derivation, matching source owner/approver |
| Role/revocation/foreign-owner denial | OFFLINE_SYNTHETIC_PASS | Real safe test identities/records; no fabricated roles/subjects |
| Host/origin/callback/SAN consistency | REPOSITORY_VERIFIED | Operational readback after provisioning |
| PKI policy/root/leaf/key matching | OPERATOR_REPORTED_PASS | Fresh date/chain/mode acceptance before use |
| Initial CRL/signature/local revocation check | OPERATOR_REPORTED_PASS | Manual freshness/response; not browser protection |
| Manual renewal/revocation owner | OPERATOR_REPORTED_PASS | Deadline tracking and explicit residual-risk acceptance PENDING |
| Independent PKI/credential backups/passphrases | PENDING | Separate protected location/custodian and recoverability evidence |
| Current-user Windows trust/hosts resolution | OPERATOR_REPORTED_PASS | Actual browser chain/name/TLS acceptance later |
| Machine-wide root trust | NOT_APPLICABLE | Keep deliberately absent |
| Local OpenSSH/port/Tailscale and endpoint identification | OPERATOR_REPORTED_PASS | Fresh authorized peer/reachability checks; port may change availability |
| Existing host-key TOFU records | OPERATOR_REPORTED_PASS | Independently trusted VM host fingerprint PENDING |
| Dedicated authentication pair/configuration | OPERATOR_REPORTED_PASS | Real interactive authentication later |
| Transfer compatibility | BLOCKED (old driver); PREPARED_NOT_EXECUTED alternative | Verify narrow root maintenance/GPG/parser and native Windows transfer |
| Tunnel/deployed HTTPS/WebSocket/login | PENDING; NOT_AUTHORIZED now | Gate D evidence under a separate session |
| Immutable approved source bytes/SHA256 | PENDING | Actual eligible source, hash/size and rights review; none selected |
| Source ownership/current SourceApproval | BLOCKED | Enrolled owner, document/source IDs, approver and current window |
| Classification/rights/transmission/retention | PENDING | Only synthetic/licensed_public, approved_retained_nonpersonal/no erasure requirement supported |
| External consent/notice/privacy/exposure | PENDING | Actual consent date and independent approval references; no fixture substitution |
| Independent semantic/quality review | PENDING | Real review evidence; historical 0/2 stays deferred, not current approval |
| Session-specific Documents authorization | PENDING | Exact session/source/window/retention/quality and appropriate v1/v2 contract |
| Separate Chat authorization | PENDING | Closed conversation/document scopes, source/current ownership, policy/permission |
| Provider endpoint/deployment/version/type/region | PENDING | Explicit current approved dispatch resource and processing region |
| Header/credential custody | PENDING | api-key or Bearer choice; mounted valid credential; no renewal implemented |
| General/fast/coding/summarization mappings | PENDING | Reviewed aliases/response-model identities; not historical defaults |
| Managed/analysis/planning profiles | PENDING | Managed prompt11/azure-strict/1 and actual supported profile/model bounds |
| Chat streaming/usage/context/output/deadline | PENDING | Current independent capability evidence; no discovery/model request now |
| Current provider compatibility | PENDING | Separately authorized proof; historical Foundry runs do not qualify it |
| Applicable tariff/catalog/currency | PENDING | Current approved applicable model prices/FX/fees and used aliases |
| Owner/tenant budgets/request bounds | PENDING | Independent ceilings/input/output/time limits in actual configuration |
| RPM/TPM/concurrency/interactive policy | PENDING | Current allocation and shared quota key, not per-app duplicate limits |
| Shared consumers/exclusivity | PENDING | Named consumers and coordination/exclusivity evidence |
| Reservations/UNKNOWN/outstanding obligations | PENDING | Existing shared-financial/provider truth; absence of new DBs proves no historical balance |
| Independent financial approval | PENDING | Fresh model authority separate from infrastructure cost approval |
| Execution root/trust/key provenance/operator/revocations | PENDING | Independently controlled read-only records, verified subject, no signer key in VM |
| Frozen execution binding/resource/scopes/calls/window | BLOCKED | Actual configuration/source/provider/finance and subject first, then independent approval |
| Signed live permission | NOT_AUTHORIZED now; PENDING for future live operation | Fresh independently signed exact permission; no reuse/renewal of old signatures |
| New-state/reuse/storage/authority decision | PENDING | Inventory and explicit approval; preserve all seven authorities and obligations |
| Fresh infrastructure authorization/UTC cutoff/owners | NOT_AUTHORIZED now | Separate session packet; no expired window/ceiling reuse |

Structural constraints are not evidence of actual approved inputs. SourceApproval requires
rights/native-text/provider-processing approval, approved nonpersonal retention, owner and
approver/window, not just a filename. External SessionApproval additionally requires provided
consent plus exposure/privacy/quality references. Historical v1 zero-paid records cannot become
v2 execution records. Chat policy approval does not replace managed digestion/session consent.
Two independent digest reviews and separate answer reviews remain required at presentation;
this review cannot pre-approve future unseen generated content. Their review plan/owners must
be settled before execution, and actual findings attach to actual artifacts later.

Some actual deployed acceptance belongs to B–E; it cannot honestly be labeled complete in A.
If the operator wants an identity-only maintenance exception before full A closure, it needs
explicit separately reviewed scope and authorization. This report neither changes the gate
definition nor treats that possible future exception as current Gate A closure.

## 11. Gate dependency analysis

**REPOSITORY_VERIFIED:** RuntimeManifest has required nonempty enrollment and at least one
SourceApproval. `build()` checks issuer/tenant, derives tenant/owner with versioned stable_id
domains, requires all sources match that owner, reads immutable source bytes and verifies hash,
strict capabilities and priced model roles before constructing SecurityRuntime/provider/
retrieval/pilot/actions. Initialization does not discover the enrolled identity or acquire tokens.
The `check` command requires the complete authority set on reopen and validates configuration;
it is not a manifest/credential/identity-bootstrap verifier.

Standard dependency chain:

```text
verified API-token sub → enrollment + canonical owner → approved source/config/manifest
    → Redis/Chroma + deliberate initialize → API serve/readiness → UI → gateway → browser login
                                     ↑                                  ↓
                       desired first browser subject acquisition ────────┘
```

Middleware's `authority.register(verified)` happens only after the built API accepts a token;
it cannot supply the missing pre-initialization tuple. Workflow enrollment is an exact tuple,
not merely a registered principal. Browser login itself appears before API context requests in
both UI consumers, so a deliberately isolated UI could technically render login without API.
However standard Compose health ordering blocks that startup, there is no supported production
identity-only mode or sanitized verified-subject export, and bypassing dependencies does not
provide a reviewed bootstrap. No `up --no-deps ui`, placeholder enrollment, debug token display,
fixture issuer or production state initialization is proposed as an operational workaround.

OIDCVerifier.verify can validate an already acquired token without constructing authorities,
but does not acquire one. The historical Foundry launcher requires token/configuration and
approval and either runs a synthetic rehearsal or a live workflow; it is not a native-browser
identity-only acquisition path. Its CLI/environment token transport is not a new approved
bootstrap. An operator can propose another legitimate pre-existing acquisition path, but must
supply reviewed evidence of the same API/browser principal before it closes this blocker.

**Separately reviewable engineering solution:** a narrowly scoped maintenance identity-bootstrap
tool using existing native Streamlit OIDC and OIDCVerifier, same browser registration/callback,
private TLS/strict origin, no provider configuration/credential, no data services/authorities,
no workflow/routes/inference. Verify the actual API token before recording only the private
issuer/tenant/sub and derived scope; never token/ID-token/oid or public claim dump. Review token
and cookie clearing, secret mounts, no-log behavior and wrong-token/role/audience/expiry denial;
prove zero provider imports/requests and zero authority writes in tests. Temporary isolated
UI/gateway lifecycle and exact callback-port exclusivity need explicit design and operator
authorization. That solution was not implemented or authorized here. It is a real missing
workflow, not a TLS-origin defect or a reason to redesign production authority semantics.

**Existing no-inference startup is conditionally feasible**, after all legitimate inputs exist:
review `execution_permissions=false`, `chat=null` and `approvals=[]` (not a complete manifest).
Runtime then installs deny_external_execution, no Chat routes capable of execution, workflow
execution_enabled=False and runner starts without grants. Documents Start/Question deny before
reservations; `/ready` uses administrative authorities/JWKS, not model readiness probes.
Provider construction loads a real mounted credential and model mappings but sends no model
request; it cannot be omitted or faked. Redis/Chroma and real baked retrieval remain required.
The execution-authority host directory still must exist for the mandatory Compose bind even
when permissions are disabled; its custodian controls it, and no live JWT/trust file is needed
by the disabled branch. No empty revocation/trust record is manufactured as authorization.

This strategy permits later identity/read-only/negative execution validation without model
spend; it does **not** solve unknown enrollment/source/finance configuration. Chat acceptance
requires a separately reviewed configuration enabling its permission infrastructure; keep
live permission files absent and inputs disabled until separate authority exists. Runtime
`/ready` does not itself attest to Chat permission or capability readiness. Changing reviewed
manifest/policies can affect durable bindings: decide final initialization/reuse before the
first schema creation, do not promise an arbitrary later manifest toggle will reopen safely.

## 12. Outstanding operator decisions and preserved infrastructure

Before any activation: resolve the bootstrap design/review; current source/rights/privacy/
review plan; provider/configuration/custody; financial/quota/shared-obligation inputs;
independent execution custody and explicitly deferred live permission; new-state/reuse;
separate offline credential/PKI backups and passphrases/recoverability; manual revocation risk
acceptance/deadline tracking; host-key trusted verification channel; and reviewed transfer
maintenance prerequisites. Do not ask the operator to paste secrets or actual subjects into Git.

The infrastructure baseline remains **REPOSITORY_VERIFIED historical record**, based on earlier
authorized observations and later **OPERATOR_REPORTED_PASS**, not a new Azure verification:
rg-epolymind / vm-epolymind-dev, Spain Central, Standard_D2s_v4 (2 vCPU/8 GiB), Ubuntu 24.04,
64 GiB OS +64 GiB data, no public VM IP, private Tailscale/OpenSSH, ext4 `/srv/polymind`,
UUID `c95e5fce-443b-4d90-9160-8b67758f12d9`; Docker 29.10.0/Compose v5.8.0. VM **reported
deallocated**. Reboot remount/private reconnect and network-disabled CPU retrieval-model
execution are historical passes, not five-service production/capacity/recovery acceptance.
Earlier SSH/cloud-init failure and repair retain their dated outcomes.

```text
polymind:phase19-reviewed
image ID sha256:9f386acf8bddcb5d01bb028151caae24b5df604f8a56c00b7b39c7e0f8298c02
revision label 7bf82dc2da4a9f29561a5f493b690502c0090eb0
redis@sha256:7f7d30b7fdd09467bac58198a1f166dd69789d348d4fe859cccb20e0cf287fbe
chromadb/chroma@sha256:1e0b73a187a28757c572acba508c46f48c9e8b0acaf5c20e6d95cdedce1acdf6
```

The [post-Azure record](phase_19b_post_azure_readiness_offline_validation_evidence_reconciliation.md#6-docker-image-provenance-and-transfer-evidence)
records image size 3042749277 bytes, linux/amd64, user 10001:10001 and local 135-runtime-file
byte comparison. This review did not repeat that Docker audit. Application image ID is not
a registry manifest digest. Root-owned staged `/opt/polymind/docker-compose.phase19.yml`
and `compose.env.example` passed reported parsing. Their exact staged file hash/bytes remain
unknown; **do not infer a hash**. Portable source uses vendor tags. Local cached Redis digest
historically differed; no platform/index equivalence is inferred. Revalidate the staged copy
and never replace it wholesale with the repository file. Private network IDs/subnet/NSG/NAT,
subscription and current resource identifiers remain in protected historical/operator records;
fresh inventory is mandatory. No new machine-specific topology is needed in public Git.

## 13. Controlled Gate B–E provisioning plan

**Every operational command below is PREPARED_NOT_EXECUTED and NOT_AUTHORIZED now.**
Stop at unmet conditions. Values in angle brackets or prompted variables are non-secret inputs
from the protected reviewed deployment record, not invented resource selections. The plan is
sequential preparation, not permission to skip unresolved Gate A dependencies.

### Before VM activation

Freeze a fresh session packet: explicit subscription/resource IDs and tenant, approved UTC
start/end, infrastructure cost ceiling, latest activation time, mandatory stop/deallocation
deadline with enough shutdown margin, named activation/recovery/deallocation/residual-cost
owners and retained-resource review date. Reconfirm backups/passphrases/recovery ownership,
certificate/CRL freshness/risk decision and host-key verification channel. Historical four/eight
hour windows, proposed USD30 and earlier model ceilings are expired or unapproved, never reused.
Explicitly prohibit inference/provider discovery and do not enable systemd boot startup.

Identity-only maintenance, if needed before full Gate A, requires its own reviewed implementation
and bounded authorization; none of the production initialization commands below can substitute.
No activation command is supplied for automatic execution. The approved operator must separately
authorize the exact activation action only after current pre-activation checks and cutoff review.

### Gate B — Existing infrastructure revalidation

Run from the authorized operator's Azure CLI terminal **only in that future session**. Supply
PHASE19_SUBSCRIPTION from the protected packet; subscription/RG/VM outputs are private records.
These example variable values contain no credentials. Do not change the global default account.

```bash
az account show --subscription "$PHASE19_SUBSCRIPTION" --query '{id:id,tenantId:tenantId,state:state}' -o json
az vm show --subscription "$PHASE19_SUBSCRIPTION" -g rg-epolymind -n vm-epolymind-dev --query '{id:id,location:location,size:hardwareProfile.vmSize,os:storageProfile.osDisk,disks:storageProfile.dataDisks,nics:networkProfile.networkInterfaces}' -o json
az vm get-instance-view --subscription "$PHASE19_SUBSCRIPTION" -g rg-epolymind -n vm-epolymind-dev --query 'instanceView.statuses[].{code:code,time:time}' -o json
```

Require exact approved subscription/tenant/resource/SKU/disks and actual power status before
activation; stop on mismatch or cutoff. After separate activation authorization, repeat power
readback. For each NIC ID returned, review exact addresses/public-IP/NSG/subnet identities:

```bash
az network nic show --subscription "$PHASE19_SUBSCRIPTION" --ids "$PHASE19_NIC_ID" --query '{id:id,nsg:networkSecurityGroup.id,ip:ipConfigurations[].{private:privateIPAddress,public:publicIPAddress.id,subnet:subnet.id}}' -o json
az network nic list-effective-nsg --subscription "$PHASE19_SUBSCRIPTION" --ids "$PHASE19_NIC_ID" -o json
az network nic show-effective-route-table --subscription "$PHASE19_SUBSCRIPTION" --ids "$PHASE19_NIC_ID" -o json
az network vnet subnet show --subscription "$PHASE19_SUBSCRIPTION" --ids "$PHASE19_SUBNET_ID" -o json
```

Require no public VM IP and no public inbound application/SSH/cache/vector route. Review
subnet/NIC NSGs, NAT/private route and separately enforced guest/container outbound destination
policy. HTTPS-port permits/NAT/internal Compose networks do not prove destination allowlisting.
Allow only approved identity/time/DNS/Tailscale/security-update/backup traffic; inference
destination remains denied for the no-inference window. Do not test provider discovery.

For independent SSH-host verification, use an explicitly authorized trusted Azure control-plane
channel, e.g. scoped Run Command (an operational action, requiring that session's authorization):

```bash
az vm run-command invoke --subscription "$PHASE19_SUBSCRIPTION" -g rg-epolymind -n vm-epolymind-dev --command-id RunShellScript --scripts 'ssh-keygen -l -E sha256 -f /etc/ssh/ssh_host_ed25519_key.pub' --query 'value[].message' -o tsv
```

This reads the **public** host key only. Independently compare to the protected expected
fingerprint and endpoint-specific existing known_hosts record. Resolve any mismatch as an
incident; do not replace entries blindly, use ssh-keyscan as authority, or disable verification.
Inspect Tailscale peer identity on Windows and guest; workstation address is not the VM address.

Future Windows PowerShell, prompt only for non-secret protected-record values:

```powershell
$SshTarget = Read-Host 'Reviewed VM user@Tailscale-endpoint or exact SSH alias'
$Identity = Read-Host 'Existing dedicated Windows identity path'
if ($SshTarget -notmatch '^[A-Za-z0-9][A-Za-z0-9_.@-]*$') { throw 'Unreviewed SSH target syntax' }
& "$env:WINDIR\System32\OpenSSH\ssh.exe" -G -i $Identity -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes $SshTarget
& "$env:WINDIR\System32\OpenSSH\ssh.exe" -tt -i $Identity -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -o BatchMode=no $SshTarget
```

Inspect effective config privately, including ProxyCommand/forwarding/identity/known-host paths;
stop on unexpected options. Reconcile the selected dedicated key's public fingerprint from
existing protected evidence without copying its private key. Complete the interactive passphrase
prompt; verify actual authentication. On the guest:

```bash
tailscale status --json
findmnt -no UUID,FSTYPE,TARGET /srv/polymind
mountpoint --quiet /srv/polymind
lsblk -o NAME,SIZE,FSTYPE,UUID,MOUNTPOINTS
sudo stat -c '%F %u:%g %a %h %n' /srv/polymind /srv/polymind/operator /srv/polymind/operator/private /srv/polymind/operator/private/objects /srv/polymind/operator/sources /srv/polymind/redis /srv/polymind/chroma
sudo namei -l /srv/polymind/operator/private
docker version --format '{{.Server.Version}}'
docker compose version
docker image inspect polymind:phase19-reviewed --format '{{.Id}} {{.Os}}/{{.Architecture}} {{.Config.User}} {{index .Config.Labels "org.opencontainers.image.revision"}}'
docker image inspect redis@sha256:7f7d30b7fdd09467bac58198a1f166dd69789d348d4fe859cccb20e0cf287fbe --format '{{.Id}} {{json .RepoDigests}} {{.Os}}/{{.Architecture}}'
docker image inspect chromadb/chroma@sha256:1e0b73a187a28757c572acba508c46f48c9e8b0acaf5c20e6d95cdedce1acdf6 --format '{{.Id}} {{json .RepoDigests}} {{.Os}}/{{.Architecture}}'
sudo sha256sum /opt/polymind/docker-compose.phase19.yml /opt/polymind/compose.env.example
sudo stat -c '%F %u:%g %a %h %n' /opt/polymind/docker-compose.phase19.yml /opt/polymind/compose.env.example
sudo nft list ruleset
sudo iptables -S
sudo iptables -S DOCKER-USER
ss -ltn
lscpu
free -h
df -h / /srv/polymind
df -i / /srv/polymind
```

Require recorded UUID/ext4/actual mount, expected disk sizes, operator/Chroma10001 and
Redis 999 ownership 0700, private objects/sources, reviewed image/user/platform/revision and
staged vendor digests. Missing pre-production subdirectories are a deliberate provisioning
decision, not permission to format a disk. New staged-file hashes must be compared to the
approved protected artifact; an observed hash alone proves no provenance. Review staged file
bytes for five services/read-only mounts/internal networks/origin/loopback and explicit paths;
never dump populated secret files. nft/iptables inspection must cover actual forwarding path;
missing chain/tool/policy is unresolved, not an automatic pass. Tailscale JSON stays private.
Capacity acceptance still requires measured workload: at least 20% disk free, no OOM/sustained
swap, aggregate working memory under the reviewed 6 GiB planning threshold, bounded startup/
shutdown on the actual2 vCPU/8 GiB host. An idle `free` is baseline only. Stop if headroom fails.

### Gate C — Secure configuration and deliberate state lifecycle

Reconfirm Gate A inputs and exact deployment image/staged Compose before transferring anything.
Keep services stopped and systemd unenabled. Final contracts:

| Host | Container / required handling |
|---|---|
| /etc/polymind/compose.env | Host interpolation only, root-custodied 0600; path/image/origin values, no inline credentials |
| /etc/polymind/secrets/provider | /run/secrets/provider read-only,10001:10001/0600 |
| /etc/polymind/secrets/streamlit.toml | /tmp/.streamlit/secrets.toml read-only,10001:10001/0600 |
| /etc/polymind/secrets/tls.crt | /run/secrets/tls.crt read-only,10001:10001/0600 |
| /etc/polymind/secrets/tls.key | /run/secrets/tls.key read-only,10001:10001/0600 |
| /etc/polymind/execution-authority | /run/secrets/execution-authority read-only;10001:10001/0700, privately supplied records0600 |
| /srv/polymind/operator | /state,10001:10001/0700; private/objects and sources0700, records0600 |

All private files: regular, one hard link, no symlink in any component, protected traversal.
For secret parents the existing proposed root:10001/0710 policy allows UID 10001 traversal;
execution directory stays 10001/0700 under trusted parent custody. Public trust material has
no private key. Never copy ca.key, CA workspace/archive, Windows identity key or signer key.
No populated env file is opened by this offline review.

**Reviewed transfer alternative for the encrypted TOML:** use the Windows-native client
interactively to transfer **ciphertext only**, then an interactive verified SSH maintenance
session for a root-custodied fixed receiver. Do not enable an agent, copy a private key into
WSL, or change BatchMode on the old driver and assume all remaining preconditions hold.

1. In the future session, prepare one user-owned 0700 remote staging directory using trusted
   maintenance; reject symlinks/unsafe ancestors/existing ciphertext, and confirm exact target
   path. Record metadata and local ciphertext SHA256 privately. Copy only encrypted TOML
   into a protected Windows transfer location if needed; no plaintext crosses that staging
   location. Local private key remains in Windows. Never transfer the full encrypted PKI archive.
2. Preinstall only the non-secret receiver in the next subsection, root-owned 0600 under a
   root-owned, non-writable `/opt/polymind/maintenance` directory. Compare its reviewed SHA256.
   Check existing guest Python 3.11+/tomllib, GPG, gpgconf and agent availability; install nothing on
   failure. The helper path is **proposed, not an existing deployed utility**. It is an
   operator maintenance artifact, not an application/runtime/image change.
3. Transfer using native scp and the protected reviewed target; prompts remain interactive:

```powershell
$EncryptedTOML = Read-Host 'Protected Windows path containing only streamlit.toml.gpg'
$RemoteCipher = Read-Host 'Reviewed absolute remote staging filename, no spaces or shell metacharacters'
if ($RemoteCipher -notmatch '^/[A-Za-z0-9_./-]+$' -or $RemoteCipher -match '(^|/)\.\.(/|$)') { throw 'Unreviewed remote path syntax' }
& "$env:WINDIR\System32\OpenSSH\scp.exe" -i $Identity -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -o BatchMode=no $EncryptedTOML "${SshTarget}:$RemoteCipher"
if ($LASTEXITCODE -ne 0) { throw 'Ciphertext transfer failed; reconcile before retrying' }
```

4. Open a fresh verified interactive SSH session with `-tt` as in B. Compare remote encrypted
   size/hash/mode/ownership with the protected local record. Run `sudo -l` privately, then use
   **existing authorized maintenance privileges**, with interactive sudo authentication for
   the exact fixed receiver command. The helper prompts separately on `/dev/tty` for the GPG
   passphrase, never through argv/env. Root first verifies expected ciphertext SHA256 and
   metadata; it decrypts to memory, checks GPG success and exact native contract, then creates
   only the final private TOML exclusively. No decrypted staging file or shell pipeline exists.

```bash
sudo -l
sudo /usr/bin/python3 -I /opt/polymind/maintenance/install_streamlit_encrypted.py "$PHASE19_STAGED_CIPHERTEXT" "$PHASE19_EXPECTED_CIPHERTEXT_SHA256"
```

No new `NOPASSWD: python`, blanket sudo, or arbitrary-command exception is proposed. If the
operator lacks already authorized root maintenance, a custodian must perform the reviewed
installation; stop instead of broadening privilege. Encrypted SHA256/path are not credentials.
Do not pipe plaintext into a PTY (terminal echo/transformation), chain `sudo -n` assumptions,
or transfer plaintext with scp merely to work around authentication.

5. Validate installed content/metadata under UID 10001 using the same private validator,
   compare callback/origin/discovery/browser/scope/API audience and preserve the cookie.
   Print only PASS/FAIL/metadata. Verify receiver/ciphertext metadata after a lost connection
   before any retry; an already installed file must never be overwritten blindly. Remove
   only the confirmed redundant encrypted transfer artifact after successful acceptance;
   preserve original encrypted recovery custody. No secure-erasure claim is made.

This alternative is **PREPARED_NOT_EXECUTED**. Native Windows authentication, remote GPG/TTY,
privileges and actual installation are not synthetically certified. Its security properties
are source-reviewed; embedded Python is compilation-checked only. The original receiver's
historical synthetic tests do not count as tests of this alternative.

#### Future encrypted-TOML receiver (non-secret preparation artifact)

Requires an independently verified original 474-byte ciphertext/hash; a regenerated artifact
needs renewed review rather than relaxing checks. Decrypted 516-byte original size is checked.
The user-owned source may reside in its protected 0700 staging directory; ancestors must be
root or that owner and not group/world writable. Root-owned final ancestors are opened with
directory descriptors and no-follow; unsafe existing parents or final files are refused.
GPG uses a disposable root-only runtime home, not personal credential storage. Plaintext and
passphrase remain in process memory/anonymous pipe; memory erasure is not guaranteed.

```python
import getpass
import hashlib
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import tomllib
import warnings


def require(ok):
    if not ok:
        raise ValueError('Preflight rejected')


def validate(payload):
    require(len(payload) == 516)
    data = tomllib.loads(payload.decode('utf-8'))
    require(set(data) == {'auth'})
    auth = data['auth']
    tenant = 'afabeaf8-0fea-42c9-afb4-7e5c07eff3f3'
    expected = {
        'redirect_uri': 'https://polymind.test:9443/oauth2callback',
        'server_metadata_url': f'https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration',
        'client_id': 'a43f5479-4cbd-45a0-86e0-9c658e77d133',
        'expose_tokens': ['access'],
        'client_kwargs': {'scope': 'openid api://5aa70f9d-9f9e-4b5b-972b-698d4d68105e/access_as_user'},
    }
    require(set(auth) == set(expected) | {'client_secret', 'cookie_secret'})
    require(all(auth[k] == v for k, v in expected.items()))
    for key in ('client_secret', 'cookie_secret'):
        value = auth[key]
        require(type(value) is str and bool(value.strip()) and len(value) <= 16384)
        require(not any(x in value.upper() for x in ('<', '>', 'PLACEHOLDER', 'OPERATOR_CONTROLLED', 'SUPPLIED_PRIVATELY', 'REPLACE')))
        require(value != '7319515e-0342-4c8e-aacb-b5c663c8cda9')
        value.encode('utf-8', errors='strict')
    require(re.fullmatch(r'[A-Za-z0-9_-]{64}', auth['cookie_secret']) is not None)
    require(auth['client_secret'] != auth['cookie_secret'])


def main():
    require(os.geteuid() == 0 and len(sys.argv) == 3)
    os.umask(0o077)
    source, expected = Path(sys.argv[1]), sys.argv[2]
    require(source.is_absolute() and '..' not in source.parts)
    require(re.fullmatch(r'[0-9a-f]{64}', expected) is not None)
    for parent in reversed(source.parents):
        info = parent.lstat()
        require(stat.S_ISDIR(info.st_mode) and info.st_mode & 0o022 == 0)
    fd = os.open(source, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        owner = info.st_uid
        require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and stat.S_IMODE(info.st_mode) == 0o600)
        require(all(p.lstat().st_uid in (0, owner) for p in source.parents))
        require(stat.S_IMODE(source.parent.lstat().st_mode) == 0o700)
        encrypted = stream.read(65537)
    require(len(encrypted) == 474 and hashlib.sha256(encrypted).hexdigest() == expected)
    with open('/dev/tty', 'w') as terminal, warnings.catch_warnings():
        require(terminal.isatty())
        warnings.simplefilter('error', getpass.GetPassWarning)
        phrase = getpass.getpass('Encrypted TOML passphrase: ', stream=terminal)
    require(bool(phrase) and '\n' not in phrase and '\r' not in phrase)
    secret = phrase.encode('utf-8') + b'\n'
    require(len(secret) <= 1024)
    read_fd, write_fd = os.pipe()
    try:
        os.write(write_fd, secret)
        os.close(write_fd)
        write_fd = None
        with tempfile.TemporaryDirectory(prefix='polymind19-gpg-', dir='/run') as home:
            os.chmod(home, 0o700)
            try:
                result = subprocess.run([
                    '/usr/bin/gpg', '--no-options', '--homedir', home, '--batch',
                    '--pinentry-mode', 'loopback', '--no-symkey-cache',
                    '--passphrase-fd', str(read_fd), '--decrypt',
                ], input=encrypted, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                    pass_fds=(read_fd,), timeout=60, env={'PATH': '/usr/bin:/bin', 'LANG': 'C'})
            finally:
                stopped = subprocess.run([
                    '/usr/bin/gpgconf', '--homedir', home, '--kill', 'gpg-agent',
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10,
                    env={'PATH': '/usr/bin:/bin', 'LANG': 'C'})
                require(stopped.returncode == 0)
        require(result.returncode == 0)
        payload = result.stdout
        validate(payload)
    finally:
        os.close(read_fd)
        if write_fd is not None:
            os.close(write_fd)
    directory = os.open('/etc', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    created = None
    output = None
    done = False
    try:
        info = os.fstat(directory)
        require(info.st_uid == 0 and info.st_mode & 0o022 == 0)
        for part in ('polymind', 'secrets'):
            fresh = False
            try:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            except FileNotFoundError:
                os.mkdir(part, 0o700, dir_fd=directory)
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
                fresh = True
            os.close(directory)
            directory = child
            if fresh:
                os.fchown(directory, 0, 10001)
                os.fchmod(directory, 0o710)
            info = os.fstat(directory)
            require(info.st_uid == 0 and info.st_gid == 10001 and stat.S_IMODE(info.st_mode) == 0o710)
        output = os.open('streamlit.toml', os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=directory)
        created = os.fstat(output)
        with os.fdopen(os.dup(output), 'wb') as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.lseek(output, 0, os.SEEK_SET)
        require(os.read(output, 65537) == payload)
        os.fchown(output, 10001, 10001)
        info = os.fstat(output)
        require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_uid == info.st_gid == 10001)
        require(stat.S_IMODE(info.st_mode) == 0o600)
        os.fsync(output)
        os.fsync(directory)
        done = True
        print('PASS: configuration verified; uid=10001 gid=10001 mode=0600 regular=yes links=1')
    finally:
        if created is not None and not done:
            current = os.stat('streamlit.toml', dir_fd=directory, follow_symlinks=False)
            if (current.st_dev, current.st_ino) == (created.st_dev, created.st_ino):
                os.unlink('streamlit.toml', dir_fd=directory)
        if output is not None:
            os.close(output)
        os.close(directory)


if __name__ == '__main__':
    try:
        main()
    except (Exception, KeyboardInterrupt):
        print('FAIL: installation unavailable; reconcile metadata before retrying.', file=sys.stderr)
        raise SystemExit(1) from None
```

This helper authenticates ciphertext against the independently supplied hash before GPG
decompression; its memory bound relies on that known original artifact. A different/untrusted
archive is refused, not accepted as a general decrypt service. Do not authorize it as a
generic sudo receiver for other users. There is no guarantee against power loss between
exclusive file creation and completion: inspect partial state after an interruption; never
retry by deleting an unexplained final file. GPG agent runtime artifacts/cleanup must be
confirmed in the approved remote session. The helper is not operationally validated here.

**Other provisioning and state records, in order:** the provider and TLS-key custodians must
use equivalently reviewed encrypted-only transfer and fixed destination validation under
trusted interactive maintenance. The TOML helper must not be repurposed for them. Public leaf
certificate can be transferred separately and checked against its SHA256/key/chain privately;
CA public cert is needed for operator verification, not a CA private-key/archive transfer.
Require a reviewed mechanism for each real secret before execution; no generic root upload
endpoint or inline argv/env secret is introduced by this report.

Supply path/image/origin-only compose.env, provider, TOML, leaf/key and independent-authority
directory, then deployment/configuration/manifest and approved immutable sources. Use
`deployment.json={"version":"phase19-state/1","container_root":"/state"}` and exact stable
configuration paths. No inheritance/dotenv fills missing values. Owner/source approvals and
real policies must validate before schema creation. Confirm installed secret metadata via
stat/namei and a UID 10001 private validator; do not cat secrets, render populated config or
hash low-entropy provider secrets into public evidence.

Use a shell function tied to the **staged** absolute Compose file for all future commands:

```bash
p19() {
    sudo docker compose --env-file /etc/polymind/compose.env -p polymind19 -f /opt/polymind/docker-compose.phase19.yml "$@"
}
p19 config --quiet
p19 config --images
```

Require reviewed image identities, exact origin and read-only bind sources; `--quiet` alone
does not establish semantic consistency. Inventory all existing authority files/sidecars and
financial/provider obligations before approving new-state versus reuse. Never remove or
replace runtime.lock. If partial state exists, stop for reconciliation. Start only dependencies:

```bash
p19 up -d --wait --wait-timeout 240 redis chroma
p19 ps
p19 exec -T redis redis-cli ping
```

Require Chroma heartbeat health (actual Compose HTTP probe), Redis AOF/noeviction and expected
mounted persistence plus offline models. No inference/API/UI is started by this step. Only
when all seven DBs are absent in an approved genuinely new state, all binding/custody decisions
are frozen and initialization separately authorized:

```bash
p19 run --rm --no-deps api python -m deployment.phase19 initialize /state
```

Construction order is security → governance → admission → jobs → publication → pilot → actions;
models/vector construction can fail after early schemas. Initialization creates authority
structures, not verified-principal enrollment or consent. Verify seven distinct files,
UID:GID 10001:10001, mode 0600, schema version 1, quick_check and actual constructor bindings before serving:

```bash
p19 run --rm --no-deps api python -m deployment.phase19 check /state
```

`check` covers locked preflight/config only, not full semantic/credential/permission readiness.
The actual seven-authority constructors are validated on complete build/reopen. Do not create
test schemas/rows or new ledgers to claim production integrity. The set remains
security.sqlite/governance.sqlite/admission.sqlite/jobs.sqlite/pilot.sqlite/actions.sqlite/
publication.sqlite; all objects and vendor state remain within the approved backup domain.

### Gate D — Controlled startup and private acceptance

Proceed only after bootstrap/enrollment/approved source and configuration are resolved, C
accepts initialization/reuse, and the separate session authorizes lifecycle. For the reviewed
no-inference manifest described in section 11, keep live permission records absent, `chat=null`,
`approvals=[]`, permissions disabled, and provider destination blocked at the host boundary.
No fake production credential or unsupported disable flag is used.

```bash
p19 up -d --wait --wait-timeout 240 api
p19 exec -T api python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8001/health', timeout=4).status)"
p19 exec -T api python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8001/ready', timeout=4).status)"
p19 up -d --wait --wait-timeout 240 ui
p19 up -d --wait --wait-timeout 240 gateway
p19 ps
ss -ltn
docker stats --no-stream
```

Require one API/runner, healthy data services and administrative `/ready` 200, no UNKNOWN or
active reservations, expected identity JWKS access, no model startup request, host only
127.0.0.1:9443. A 503 is a blocker to investigate, never reason to bypass health ordering.
Health does not grant execution. Do not enable unattended systemd startup during a bounded
maintenance window; preserve mount-aware template for a separately reviewed future decision.

Fresh Windows port/Tailscale/hostname checks precede forwarding. In a foreground PowerShell
terminal with the same verified target/identity variables as B:

```powershell
Get-NetTCPConnection -LocalPort 9443 -State Listen -ErrorAction SilentlyContinue
[System.Net.Dns]::GetHostAddresses('polymind.test')
& "$env:WINDIR\System32\OpenSSH\ssh.exe" -N -T -i $Identity -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -o BatchMode=no -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -L 127.0.0.1:9443:127.0.0.1:9443 $SshTarget
```

Require no pre-existing listener and exact loopback resolution, then actual authenticated
forward creation with no wildcard bind. A stale known_hosts record cannot replace B's host
authenticity verification. In another terminal/browser:

```powershell
curl.exe --fail --silent --show-error --output NUL https://polymind.test:9443/
```

Require Windows client using the intended trust store, valid actual leaf/SAN/chain/dates,
no certificate bypass and browser accepted chain at `https://polymind.test:9443`. curl success
is supporting evidence, not a browser test. Inspect actual certificate fingerprint/browser
security state, exact Host and WebSocket Origin 101 behavior through the tunnel; foreign/missing
WebSocket origin and wrong Host must deny. Use a controlled reviewer test client with normal
TLS validation and no auth cookies for negative Host/Origin checks, rather than manipulating
the trusted origin or weakening certificate checks. No gateway route exposes API/admin probes.

Native login then tests the real callback/exchange, client-secret validity, API token forwarding
and server verification. Independently reconcile actual verified issuer/tid/sub with preapproved
enrollment; if it differs, stop and review owner/source/bindings, never relabel existing state.
Use approved actual test identities for wrong-role/tenant/cross-owner denial and existing trusted
revocation operations for revocation tests only when separately authorized. Without those inputs
mark live negative cases pending; do not mutate Entra merely to create a test fixture.
Exercise read-only context/source access, expired token denial, logout/frontend clearing,
reauthentication, session/restart semantics and explicit Start/Question denial with no financial
reservation/provider call. approvals=[] deliberately prevents session creation and cannot test
the full session lifecycle. Session tests need genuine approved session records first.

No-inference Documents acceptance is limited; it does not establish Chat execution, full
digestion/publication/answer reviews, paid capability or representative capacity. Those require
separate exact Chat/Documents scopes, independent approvals/call window and model authority.
Do not grant a live permission merely to demonstrate a disabled input widget. Full Chat and
Documents live tests remain later gated Phase 19B work, not a new phase or implicit next step.

### Gate E — Recovery, shutdown and deallocation

Before cutoff, stop new browser intents and trusted workflow admission. If an approved active
Documents session exists, the existing operator emergency-stop POST
`/documents/operator/stop` uses a current verified enrolled token through the existing UI;
do not put a token in curl argv/env. The stop is durable and can keep `/ready`503 on reopen;
it is not a reversible generic pause/resume toggle. With no approved sessions/grants and
execution disabled, preserve that fact rather than creating a session to stop it. For enabled
Chat there is no universal public pause endpoint: remove private ingress and use trusted
maintenance/no new intents, then quiesce the sole API. Never invent an admission-disable flag.

Allow bounded work/runner to settle inside the approved grace/window; inspect actions, jobs,
reservations, active provider admissions and operations through trusted maintenance. Keep
UNKNOWN/unfinished and consumed permissions as obligations; no retry, refund, SQL reset or
stale DB restore. If unsettled work cannot resolve before deadline, preserve conservative
evidence and stop for later reconciliation; deallocation deadline still applies.

```bash
p19 stop --timeout 90 gateway ui
p19 stop --timeout 90 api
p19 stop --timeout 90 redis chroma
p19 ps --all
```

Inspect sanitized service shutdown evidence and exit states; all five writers must be stopped,
Redis AOF flushed and no stray writer remains. A persistent API lock alone cannot prove data
service quiescence. Record host CPU/memory/disk, aggregate container peaks, timings, OOM/swap,
actual allocated duration and budget progress before shutdown. Interrupt foreground SSH tunnel
after private validation, recording closure. If shutdown hangs, preserve incident evidence,
use approved recovery ownership and still meet deallocation cutoff; do not claim a quiesced backup.

For an explicitly authorized quiesced backup, choose a **new protected off-disk location**,
root-custodied parent 0700, with enough capacity; same-disk copy is not disaster recovery.
Use the reviewed image for the root backup custodian, without host dependency installation.
PHASE19_BACKUP_PARENT is the approved existing protected off-disk directory and
PHASE19_BACKUP_NAME is a new simple basename (no slash/dot segments). Both are non-secret.
The data mount is writable solely for the existing lock; no service starts. Numeric-owner
preservation requires scoped CHOWN/DAC_OVERRIDE/FOWNER privileges for this maintenance task:

```bash
sudo docker run --rm --network none --read-only --user 0:0 --cap-drop ALL --cap-add CHOWN --cap-add DAC_OVERRIDE --cap-add FOWNER -e PYTHONDONTWRITEBYTECODE=1 --mount type=bind,src=/srv/polymind,dst=/srv/polymind --mount "type=bind,src=$PHASE19_BACKUP_PARENT,dst=/backup" --entrypoint python sha256:9f386acf8bddcb5d01bb028151caae24b5df604f8a56c00b7b39c7e0f8298c02 -m deployment.phase19.backup snapshot /srv/polymind "/backup/$PHASE19_BACKUP_NAME" --writers-stopped
```

The module inventories whole-tree hashes/owners/modes, locks the operator domain and rejects
unsafe entries. Keep protected manifest/config/image/trust evidence and encrypt backups under
the approved custody procedure. Snapshot tool does not encrypt, attest stopped writers, obtain
cloud snapshots or prove independent custody automatically. Preserve any newer external
financial/security/revocation evidence. Only if separate isolated-restore authorization exists:

```bash
sudo docker run --rm --network none --read-only --user 0:0 --cap-drop ALL --cap-add CHOWN --cap-add DAC_OVERRIDE --cap-add FOWNER -e PYTHONDONTWRITEBYTECODE=1 --mount "type=bind,src=$PHASE19_BACKUP_PARENT,dst=/backup,readonly" --mount "type=bind,src=$PHASE19_RESTORE_PARENT,dst=/restore" --entrypoint python sha256:9f386acf8bddcb5d01bb028151caae24b5df604f8a56c00b7b39c7e0f8298c02 -m deployment.phase19.backup restore "/backup/$PHASE19_BACKUP_NAME" "/restore/$PHASE19_RESTORE_NAME"
```

PHASE19_RESTORE_PARENT must be an independently approved isolated protected directory,
PHASE19_RESTORE_NAME a new simple basename; no live data mount is passed to restore.
Require a new isolated target, inventory/SQLite integrity, preserved numeric owners and stable
container `/state`; never start a concurrent restored clone or roll back spent/revoked truth.
Reboot/disk-failure/RPO/RTO testing needs its own explicit scope and time allowance; otherwise
mark pending. No automatic snapshot/resource creation or deletion is authorized by these docs.

The named operator deallocates the confirmed existing VM within the approved window and
verifies actual state, in the future authorized Azure terminal:

```bash
az vm deallocate --subscription "$PHASE19_SUBSCRIPTION" -g rg-epolymind -n vm-epolymind-dev
az vm get-instance-view --subscription "$PHASE19_SUBSCRIPTION" -g rg-epolymind -n vm-epolymind-dev --query 'instanceView.statuses[].{code:code,time:time}' -o json
az resource list --subscription "$PHASE19_SUBSCRIPTION" -g rg-epolymind --query '[].{id:id,type:type,location:location}' -o json
```

Require PowerState/deallocated; stopped/guest shutdown/Compose stop is insufficient. Record
time/deadline compliance and remaining disks/snapshots/NAT/IP/network/backup charges and
owners/review dates. Reconcile actual infrastructure billing when available; distinguish model
usage/settlement and billing lag. Preserve encrypted/security/financial evidence. No Azure
resource deletion is an automatic cleanup action.

## 14. Offline verification results

Fresh focused verification used the existing estudio_polymind interpreter and established
temporary runner/network guard copied to `/tmp/polymind19b-evidence-review-20261127`.
Only PATH/HOME/LANG/LC_ALL are inherited; PYTHONPATH, PYTHONDONTWRITEBYTECODE=1,
HF_HUB_OFFLINE=1, TRANSFORMERS_OFFLINE=1, OMP_NUM_THREADS=1 and
TOKENIZERS_PARALLELISM=false are explicit. Provider/application credential variables are
excluded. tests/conftest.py disables implicit dotenv before collection. The guard denies
non-loopback connect/connect_ex and DNS; tests use fake JWKS/provider transports and synthetic
keys/authorities only. It is test isolation, not a production destination firewall.

Exact focused invocation:

```bash
python /tmp/polymind19b-evidence-review-20261127/run_checks.py \
  tests/unit/test_phase19_oidc_template.py tests/unit/test_phase19_tls.py \
  tests/unit/test_security_entra.py tests/unit/test_phase19_chat_view.py \
  tests/unit/test_documents_view.py tests/unit/test_ui_api_client.py \
  tests/unit/test_phase19_deployment.py tests/integration/test_phase19_operator.py \
  tests/integration/test_phase19_authority_lifecycle.py \
  tests/integration/test_phase19_execution_bridge.py \
  tests/unit/test_security_authority.py tests/unit/test_security_readiness.py \
  tests/unit/test_governance.py tests/integration/test_http_cleanup_governance.py
```

Runner invokes `python -m pytest -q -p network_guard` with those paths, JUnit focused.xml,
basetemp focused-state and external focused-cache under that temporary root.
Final **exit 0; 320 passed, 4 warnings in 99.90s; zero failures/errors/skips**. Four retained
aiohttp NotAppKeyWarning occurrences are from ui/tls_gateway.py:18 in two selected-origin
cases and two gateway deployment tests; no warning was suppressed. Coverage includes native
OIDC/template/API forwarding, exact TLS/name/Host/WebSocket behavior, real synthetic Entra
verification, enrollment/owner denials, execution-disabled/no reservations, seven-authority
initialization/reopen/partial/missing/damaged failures, independent test-purpose execution
bindings/consumption/revocation, shared financial/admission denial and cleanup/UNKNOWN handling.

The first sandbox attempt stalled in socket-dependent tests and was interrupted (exit 130),
with no completed result claimed. The execution-approved rerun retained the same external
network/credential guard and passed. A process-name-only diagnostic was used; no operational
system state or credential contents were inspected.

Documentation/static validation results and final review inventory are recorded in section 15.
No operational provisioning script, GPG decrypt, certificate action, SSH, Windows configuration,
discovery/JWKS/provider request, Azure command, production Compose or production authority
operation ran. Embedded future receiver is compiled, not executed with operational inputs.
Full regression **NOT_APPLICABLE to this docs-only review** (not rerun): runtime, dependency,
API/configuration contracts and test code are unchanged. Prior 3329 full pass and 225 OIDC
preparation pass remain historical, not added to 320. No Docker build/config/startup rerun is
needed for unchanged artifacts; focused contracts inspect Compose without reading real env.

## 15. Engineering and separate pre-commit review

Engineering review found and documents the bootstrap cycle, unsupported old transfer
assumptions, required real provider/source/finance inputs even for no-inference, limited
check/health semantics, durable emergency stop and conditional manifest/reopen compatibility.
No runtime defect was silently fixed, no authority semantics changed, and no caller/interface
was modified. The encrypted-transfer alternative requires current remote prerequisites and
actual validation; compilation alone is explicitly not operational acceptance.

Separate pre-commit review checks provenance, metadata minimization, secret/private-key/token
exclusion, stale current statements, exact UTC arithmetic, supported bootstrap/startup claims,
privileges, binding/security/finance boundaries, links, embedded syntax, history preservation,
changed-file scope and empty index. Only dated current documentation is reconciled. The
selected origin/template/portable Compose, Azure-pinned artifacts and reviewed image inputs
remain unchanged. No public endpoint, dependency, debug code, temporary state or operational
artifact is added to Git. Historical prompt/report byte preservation is checked separately.

Final static validation used the temporary review checker, which reads only candidate docs,
Git baseline blobs, historical hashes and the synthetic JUnit output. It compiles code blocks
without running them, invokes bash -n without operational execution, checks local targets/
anchors, new whitespace, candidate-only secret/private-path markers, scope and index. This
pattern scan supports the separate manual review; it is not a general secret-certification claim.

```bash
python /tmp/polymind19b-evidence-review-20261127/review_docs.py
PYTHONPYCACHEPREFIX=/tmp/polymind19b-evidence-review-20261127/bytecode python -m compileall -q .
git diff --check
```

| Final validation | Actual result |
|---|---|
| Focused pytest/JUnit | Exit 0; 320 tests, 0 failures/errors/skips, 4 retained warnings, 99.90 seconds |
| Embedded Python | One new receiver and two unchanged historical OIDC provisioning blocks compiled; none operationally executed or deployment-certified |
| Bash syntax | 18 new prompt/report blocks passed bash -n; no operational command executed |
| PowerShell | Source/manual review only; native parser, Windows/SSH/GPG transfer not executed |
| Local documentation links | 26 new link targets/references checked; zero introduced missing targets/anchors |
| Historical records | 215 pre-existing tracked prompts/reports SHA256-identical to starting inventory |
| Repository compilation | Exit 0, external bytecode cache; no ownership changes or source imports |
| Whitespace/scope/secret-marker/index checks | Exit 0; seven Markdown candidates only; empty index; no new sensitive marker finding |
| Formatter/linter | No configured formatter/lint target applicable to these docs; existing Helm lint is irrelevant to unchanged Helm files; none installed |
| Docker/full regression/live operational checks | Not rerun; unchanged runtime/artifacts; no operational authorization |

Architecture remains Application/LangGraph/RAG → InferenceProvider → external adapter. Provider
SSE stays inside infrastructure, followed by provider-neutral tokens and PolyMind NDJSON.
Native OIDC/independent API verification, seven authorities, no-public-access topology and
financial/independent execution boundaries have no executable changes.

Final Git status, with HEAD unchanged and no staging:

```text
## master...origin/master
 M README.md
 M docs/evaluation/phase_19_deployment_architecture.md
 M docs/evaluation/phase_19_implementation_plan.md
 M docs/operations/phase_19_vm.md
 M docs/security/entra_v2.md
?? docs/codex/prompts/phase_19b_operational_evidence_reconciliation_and_gate_a_readiness_review.md
?? docs/codex/reports/phase_19b_operational_evidence_reconciliation_and_gate_a_readiness_review.md
```

Final git diff --stat (tracked files only):

```text
 README.md                                          | 31 ++++++++--
 .../evaluation/phase_19_deployment_architecture.md | 30 ++++++++++
 docs/evaluation/phase_19_implementation_plan.md    | 35 +++++++++++
 docs/operations/phase_19_vm.md                     | 69 +++++++++++++++++++++-
 docs/security/entra_v2.md                          | 31 ++++++++++
 5 files changed, 187 insertions(+), 9 deletions(-)
```

The two new prompt/report files are additionally untracked and were reviewed in full; they
are not included in that tracked stat. git diff --check passed and git diff --cached --name-only
returned no paths. No staging, commit, push, fetch, pull or other Git history/remote mutation
occurred. Proposed checkpoint only:
`docs: reconcile Phase 19B operational evidence and review Gate A readiness`.

## 16. Final acceptance gates

| Review gate | Verdict / evidence |
|---|---|
| 1 Repository baseline | PASS — exact clean HEAD and read-only exact-commit CI |
| 2 Operational evidence | PASS — all supplied groups classified; no operational result promoted |
| 3 Security/custody | PASS for review boundary — no operational secret access; custody/restore gaps remain |
| 4 Gate A completeness | PASS for assessment — all input groups reviewed; operational closure BLOCKED |
| 5 Dependencies | PASS for investigation — bootstrap gap and conditional no-inference supported; no workaround executed |
| 6 Provisioning preparation | PASS for conditional plan — ordered B–E, explicit stops/privilege/custody prerequisites; not execution-ready |
| 7 Verification/documentation | PASS — focused 320 pass; compilation, links, syntax, history and final diff checks passed (section 15) |
| 8 Scope | PASS — no unauthorized operations, runtime changes, Git mutations or next phase |

Passing review gates does not close operational Gate A, certify the new maintenance receiver,
approve actual inputs or grant Azure/model expenditure.

## 17. Recommended next operator action

Review this offline assessment and decide the narrow identity-only bootstrap engineering scope,
manual revocation-risk policy and independent backup custody/recovery arrangements. In parallel,
assemble actual non-secret approval references for source/privacy/reviewer plan, provider/
capabilities, finance/shared quota/obligations and independent execution custody in a protected
packet. Do not activate the VM to discover missing prerequisites or paste actual secrets/subjects
into Git. A separate implementation task is justified for the missing bootstrap workflow; it
must be reviewed and tested before any identity-maintenance session. Another runtime redesign,
TLS framework or credential replacement is not justified by current evidence.

Only after those decisions/evidence, a separate bounded maintenance authorization may cover
infrastructure revalidation/activation, trusted host-key readback, interactive SSH and secure
installation, approved authority lifecycle and no-inference browser acceptance. Actual provider
compatibility or Chat/Documents inference needs separate data/financial/per-execution authority.
Any deferred Gate A requirement must remain visible; possible future actions do not close it.
Stop after this handoff. Phase 19C remains NOT_STARTED.

## 18. Final status contract

```text
PHASE19B_OPERATIONAL_EVIDENCE_RECONCILIATION: COMPLETE_OFFLINE_REVIEW

REPOSITORY_BASELINE: REPOSITORY_VERIFIED_CLEAN_f5343e46054d1ef2110307bdf941ebce6a3fd9a4
LATEST_CI_RECONCILIATION: INDEPENDENTLY_VERIFIED_SUCCESS_45788278749_EXACT_HEAD

ENTRA_REGISTRATION: OPERATOR_REPORTED_PASS
ENTRA_DELEGATED_PERMISSION: OPERATOR_REPORTED_PASS
ENTRA_OPERATOR_SPECIFIC_CONSENT: OPERATOR_REPORTED_PASS
ENTRA_CLIENT_CREDENTIAL_METADATA: OPERATOR_REPORTED_PASS

OPERATIONAL_STREAMLIT_CONFIGURATION: OPERATOR_REPORTED_PASS
INDEPENDENT_COOKIE_SECRET_GENERATION: OPERATOR_REPORTED_PASS
ENCRYPTED_STREAMLIT_STAGING: OPERATOR_REPORTED_PASS
REDUNDANT_PLAINTEXT_CLEANUP: OPERATOR_REPORTED_PASS
ACTUAL_ENTRA_CREDENTIAL_VALIDITY: PENDING

PRIVATE_PKI_POLICY: OPERATOR_REPORTED_PASS
PRIVATE_CA_CREATION: OPERATOR_REPORTED_PASS
TLS_SERVER_CERTIFICATE_ISSUANCE: OPERATOR_REPORTED_PASS
CA_CERTIFICATE_KEY_MATCH: OPERATOR_REPORTED_PASS
TLS_CERTIFICATE_KEY_MATCH: OPERATOR_REPORTED_PASS
CRL_GENERATION: OPERATOR_REPORTED_PASS
CRL_SIGNATURE_VERIFICATION: OPERATOR_REPORTED_PASS
LOCAL_ENCRYPTED_PKI_BACKUP: OPERATOR_REPORTED_PASS
INDEPENDENT_OFFLINE_BACKUP_CUSTODY: PENDING
BACKUP_RESTORE_ACCEPTANCE: PENDING

AUTOMATED_CERTIFICATE_RENEWAL: NOT_IMPLEMENTED
AUTOMATED_CRL_DISTRIBUTION: NOT_IMPLEMENTED
BROWSER_CRL_ENFORCEMENT: NOT_ESTABLISHED
MANUAL_REVOCATION_RISK_ACCEPTANCE: PENDING

WINDOWS_CURRENT_USER_CA_TRUST: OPERATOR_REPORTED_PASS
WINDOWS_MACHINE_WIDE_CA_TRUST: NOT_APPLICABLE_REPORTED_ABSENT
WINDOWS_HOSTNAME_RESOLUTION: OPERATOR_REPORTED_PASS
WINDOWS_OPENSSH_READINESS: OPERATOR_REPORTED_PASS
TAILSCALE_LOCAL_READINESS: OPERATOR_REPORTED_PASS
VM_TAILSCALE_ENDPOINT_IDENTIFICATION: OPERATOR_REPORTED_PASS_PROTECTED_RECORD
EXISTING_SSH_HOST_KEY_RECORDS: OPERATOR_REPORTED_PASS_TOFU_ONLY
INDEPENDENT_VM_HOST_KEY_VERIFICATION: PENDING
SSH_AUTHENTICATION_KEY_PAIR: OPERATOR_REPORTED_PASS
SSH_DEDICATED_IDENTITY_CONFIGURATION: OPERATOR_REPORTED_PASS
SSH_TRANSFER_PROCEDURE_COMPATIBILITY: BLOCKED_PRIOR_DRIVER_ALTERNATIVE_PREPARED_NOT_EXECUTED
ACTUAL_REMOTE_SSH_AUTHENTICATION: PENDING_NOT_AUTHORIZED
ACTUAL_PRIVATE_SSH_TUNNEL: PENDING_NOT_AUTHORIZED
LIVE_HTTPS_ACCEPTANCE: PENDING

ACTUAL_ENTRA_AUTHENTICATION: BLOCKED
API_ACCESS_TOKEN_SUBJECT: BLOCKED
RUNTIME_ENROLLMENT: BLOCKED
IDENTITY_BOOTSTRAP_DEPENDENCY_REVIEW: REPOSITORY_VERIFIED_GAP_NO_SUPPORTED_ACQUISITION_WORKFLOW
NO_INFERENCE_STARTUP_FEASIBILITY: REPOSITORY_VERIFIED_CONDITIONAL_NOT_READY

SOURCE_APPROVAL_READINESS: BLOCKED_MISSING_APPROVED_SOURCE_AND_OWNER
PRIVACY_AND_CONSENT_READINESS: PENDING
SEMANTIC_REVIEW_READINESS: PENDING
PROVIDER_CONFIGURATION_READINESS: PENDING
PROVIDER_CAPABILITY_READINESS: PENDING
FINANCIAL_CONFIGURATION_READINESS: PENDING
SHARED_QUOTA_READINESS: PENDING
OUTSTANDING_OBLIGATIONS_RECONCILIATION: PENDING
INDEPENDENT_EXECUTION_AUTHORITY_READINESS: BLOCKED_MISSING_INPUTS_AND_INDEPENDENT_APPROVAL

GATE_A_REVIEW: COMPLETE
GATE_A_OPERATIONAL_CLOSURE: BLOCKED
GATE_A_REMAINING_BLOCKERS: IDENTITY_BOOTSTRAP_ENROLLMENT_SOURCE_PRIVACY_REVIEWS_PROVIDER_CAPABILITIES_FINANCE_QUOTA_OBLIGATIONS_EXECUTION_CUSTODY_BACKUPS_REVOCATION_RISK_HOST_AUTHENTICITY_TRANSFER_AND_LIVE_ACCEPTANCE

GATE_B_PROVISIONING_PLAN: PREPARED_NOT_EXECUTED_CONDITIONAL
GATE_C_PROVISIONING_PLAN: PREPARED_NOT_EXECUTED_CONDITIONAL
GATE_D_VALIDATION_PLAN: PREPARED_NOT_EXECUTED_CONDITIONAL
GATE_E_RECOVERY_PLAN: PREPARED_NOT_EXECUTED_CONDITIONAL

APPLICATION_RUNTIME_CODE_CHANGED: NO
APPLICATION_IMAGE_REBUILD_REQUIRED: NO
FOCUSED_REGRESSION_VERIFICATION: OFFLINE_SYNTHETIC_PASS_320_TESTS_4_WARNINGS
FULL_REGRESSION_VERIFICATION: NOT_REQUIRED_DOCUMENTATION_ONLY_NOT_RERUN
DOCUMENTATION_RECONCILIATION: COMPLETE
PRE_COMMIT_REVIEW: PASS_OFFLINE_SCOPE_WITH_OPERATIONAL_LIMITATIONS_DOCUMENTED

ACTUAL_CREDENTIALS_ACCESSED_BY_CODEX: NO
AZURE_VM_ACTIVATED: NO
AZURE_OPERATIONS_PERFORMED: NO
ENTRA_MUTATIONS: NO
REMOTE_SSH_CONNECTIONS: 0
REAL_INFERENCE_CALLS: 0
PRODUCTION_AUTHORITIES_INITIALIZED: NO
PUBLIC_EXPOSURE_INTRODUCED: NO

GIT_STAGED: NO
GIT_COMMITTED: NO
GIT_PUSHED: NO

PHASE19A_STATUS: COMPLETE
PHASE19B_STATUS: ACTIVE
PHASE19C_STATUS: NOT_STARTED

NEXT_AUTHORIZED_OPERATOR_ACTION: OFFLINE_REVIEW_AND_DECIDE_BOOTSTRAP_SCOPE_CUSTODY_RISK_AND_APPROVAL_INPUTS
NEXT_ACTION_READINESS: READY_FOR_OPERATOR_REVIEW_OPERATIONAL_EXECUTION_BLOCKED
```
