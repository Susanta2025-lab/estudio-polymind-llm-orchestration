# Phase 19 private VM foundation — offline operations

Current evidence and procedure precedence are reconciled in the [27 November readiness addendum](#27-november-2026--operational-evidence-and-gate-a-readiness).
Earlier dated registration, credential, PKI, Windows and transfer procedures/pending findings
below are historical; do not repeat completed operator actions. The prior BatchMode=yes
transfer is blocked for the reported locked Windows key and disabled agent. Read the current
addendum and conditional replacement before planning a transfer.

19 November 2026. This foundation is **not approved for Azure activation or inference**.
Governed Chat and Documents are implemented, with execution denied unless a current,
independently signed, configuration-bound permission and all existing authorities validate.
Version-1 `SessionApproval.zero_paid_execution=True` records remain non-billable. Distinct
version-2 external execution sessions require their own approval and permission. A configuration
flag or login alone cannot enable inference. No live permission was issued or activated by 19B.
The [19B report](../codex/reports/phase_19b_offline_implementation_and_verification.md)
records exact evidence and conditions. Existing `make chat-*` / `make docs-*` remain local.

## Configuration and storage prerequisites

Use the existing cached CPU-only Dockerfile. Deploy a reviewed immutable application image;
all three Python services share its layers. No model downloads occur at startup. Pin vendor
image digests after review; current tested tags are Redis 7.4-alpine and Chroma 1.5.9.

`docker-compose.phase19.yml` requires every `PHASE19_*` input in
`deployment/phase19/compose.env.example`. That file contains inert deployment paths, no keys.
Keep the populated environment file outside Git, mode 0600. Do not render credential values
with `docker compose config`; the profile interpolates file paths, not secret contents.

Use an actual mounted ext4/xfs/btrfs data disk. Never Azure Files/NFS/SMB or temporary storage.
The production configuration validator also rejects overlay/tmpfs authority storage.
The systemd template checks `/srv/polymind` is a mount point before Compose starts. Review
that mount identity and fstab dependency before installation; do not enable the unit before
the applicable A1/A2 approvals.
A missing bind source is fatal (`create_host_path: false`); an empty disk is also fatal.

```text
/srv/polymind/                 private backup domain, root custodian
  operator/                   10001:10001, 0700; mounted at /state
    deployment.json           0600: {"version":"phase19-state/1","container_root":"/state"}
    configuration.json        0600, reviewed Settings; stable container paths
    manifest.json             0600, reviewed source/session/capability/profile bindings
    sources/<sha256>           approved immutable source bytes, 0600
    runtime.lock              persistent inode; never remove or replace while in use
    private/                  0700
      security.sqlite         identity/owner/document security truth
      governance.sqlite       budgets, reservations, UNKNOWN and settled costs
      admission.sqlite        shared provider RPM/TPM and dispatch evidence
      jobs.sqlite             job ledger, attempts, leases, checkpoints/outbox
      pilot.sqlite            approvals, intents, stop state, publication bindings
      actions.sqlite          idempotency and accepted Q&A results
      publication.sqlite      canonical publication state
      objects/                0700; canonical source/artifact/receipt objects, 0600
  redis/                      999:999, 0700; /data, AOF every second, no eviction
  chroma/                     10001:10001, 0700; /data, persistent vector index
```

Use root/trusted maintenance to prepare only these dedicated host directories with the
listed numeric ownership. Never recursively change unrelated paths. Source files and
manifest are operator-provisioned inputs, never inferred from browser claims. No enrollment,
consent, source approval, tariff or execution approval is created on serving/restart.

`configuration.example.json` deliberately fails validation: replace null OIDC/policy/pricing/
admission fields and empty model map with reviewed configuration. OIDC requires the existing
`entra_v2` contract: canonical tenant/API audience UUIDs, exact tenant-specific issuer/JWKS,
`access_as_user`, and exact `PolyMind.L1Operator` role. Governance requires distinct stable
paths, an approved tariff catalog covering the configured general/summarization aliases,
owner/tenant limits and the shared provider quota key/policy. Do not invent tariffs or use
new ledgers to conceal historical obligations. Authority relocation requires explicit
review, because existing pilot bindings include absolute container paths.

`manifest.json` follows `deployment.phase19.runtime.RuntimeManifest`: enrollment
`[issuer, tenant, subject]`, approved `SourceApproval` records, explicit session approvals,
`ManagedSettings`, analysis `CapabilityProfile` and `DigestionProfile`. Optional `chat` and
`execution_permissions` select the governed integration described below.
Use managed prompt 11, strict Azure schema capability and usage reporting; the existing
pilot validates bounds. Inspect model JSON schemas in the image to prepare these records.
Source bytes are indexed by their approved SHA256 filename. There is no automatic source
or session approval. Version-1 session records retain their zero-paid-execution restriction;
version-2 execution records are distinct and cannot be created by relabeling a zero-paid record.

## Identity, TLS and provider secrets

Mount mode-0600 files owned by 10001:10001: provider credential, Streamlit native OIDC secrets,
TLS certificate and TLS key. They live outside the source/image. The provider supports
`Authorization: Bearer …` and `api-key`; default behavior for existing clients is unchanged.
`OPENAI_COMPATIBLE_API_KEY_FILE` is mutually exclusive with inline credentials. No refresh,
managed-identity acquisition, discovery or renewal is implemented. A missing/unsafe/empty
file is fatal. Credentials may be supplied only after the corresponding operator gates.
The offline 19B verification used fake values exclusively in tests and did not inspect
existing real credentials.

The endpoint must be HTTPS with a v1 path, e.g. the **operator-approved** endpoint ending
`/openai/v1/`. The deployment alias goes in all required logical role mappings; response-model
aliases, token parameter, strict schema and usage capabilities are explicit manifest inputs.
The composition never performs model readiness GETs or paid calls as a startup probe.
Actual endpoint/authentication/model/streaming/schema compatibility needs separately
authorized 19B validation.

Streamlit secrets must contain real native auth registration, private callback URI,
`expose_tokens=["access"]`, cookie/client secrets and delegated API scope. The API independently
verifies the token, tenant/role, enrollment, security authority and ownership. Browser ID or
Graph tokens do not substitute for API access tokens. Do not use the local Documents issuer,
fixture signing key, fixture consent or localhost certificate in this production profile.

The gateway has an exact `PHASE19_ORIGIN`, TLS >=1.2, host/origin checks and WebSocket forwarding.
Incoming forwarded headers are discarded. It only proxies Streamlit: API health, metrics and
operator endpoints have no gateway route. TLS is bound to **127.0.0.1:9443** on the host; use
an approved private tunnel preserving the reviewed hostname/certificate. No app/container
port is bound publicly. Backend/frontend Docker networks are internal; only API/UI have an
egress network for reviewed identity/provider HTTPS. Enforce the outbound allowlist at the
host/network boundary; Compose's egress network is not a destination firewall.

## Explicit lifecycle

Safe configuration-only check, with placeholders and no mounted secrets:

```bash
docker compose --env-file deployment/phase19/compose.env.example -p polymind19 -f docker-compose.phase19.yml config --quiet
```

After offline acceptance and operator-provided private inputs, create new authorities **only**
in a dedicated new reviewed runtime, via the same API image/path/mounts:

```bash
docker compose --env-file /etc/polymind/compose.env -p polymind19 -f docker-compose.phase19.yml run --rm --no-deps api python -m deployment.phase19 initialize /state
```

Initialization requires the private directories, marker/config/manifest/source files and
retrieval service availability. Start Redis/Chroma first if initializing actual publication
adapters. It refuses any existing authority database. A partial failed initialization is an
incident to inspect, never a reason to delete/reset files or run initialize on historical data.
`serve` only reopens a complete integrity-checked set under one persistent POSIX lock.

```bash
docker compose --env-file /etc/polymind/compose.env -p polymind19 -f docker-compose.phase19.yml up -d --wait --wait-timeout 240
docker compose --env-file /etc/polymind/compose.env -p polymind19 -f docker-compose.phase19.yml stop --timeout 90
```

These are instructions, not cloud authorization. Keep one API process/runner, no replicas,
Uvicorn reload or additional workers. `on-failure:3` bounds crash restarts; the mount-aware unit provides
explicit boot sequencing. Runner grants are memory-only and discarded on restart. A browser
refresh only performs authorized reads. Expiry, consumed approvals, UNKNOWN and financial
reservations remain durable. Start/question are unavailable when the independent bridge is absent, and denied when the
selected session lacks a valid permission. Backend status supplies separate Start/Question
flags, including required review state. `health` is liveness; `ready` means administrative
Documents health, not permission for external execution. Missing JWKS/private identity access correctly
keeps readiness 503. Shutdown waits 90 seconds; runner's bounded join raises if still active.

## Offline synthetic verification

Run production contract tests using only signed test JWTs and mock providers:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python -m pytest -q tests/unit/test_phase19_deployment.py tests/integration/test_phase19_operator.py tests/integration/test_document_operator.py tests/unit/test_structured_provider.py
```

`test_document_operator.py` exercises source → durable job → complete digest → publish → Q&A
→ replay/reauthentication/reopen, with no provider network effects. The new non-fixture tests
use the real Entra verifier and authorities plus test-only embedding/vector adapters, and
assert execution denial before reservations when permission is absent. The additional
`test_phase19_execution_bridge.py` exercises actual signed test permissions end to end. Never replace production inputs with these
fixtures to claim real authentication or provider acceptance.

The 19B container experiment additionally used a temporary overlay derived from the actual
five-service profile, internal-only networks, no published ports and test-only API/identity/
TLS/provider inputs. It loaded the real baked embedding/reranker and published into real
Chroma HTTP. That overlay is synthetic evidence, not a supported production switch. The
report records its outcome and limitations; existing `docker-compose.documents.yml` remains
the supported local synthetic browser launcher.

## Quiesced backup, isolated restore and rollback

Stop new workflow intent, wait for bounded calls, inspect unresolved operations/reservations,
and stop **all five services** with the command above. Verify every container stopped and
Redis flushed AOF; do not merely stop the API. Preserve UNKNOWN obligations without retrying.
Then run as the trusted root backup custodian, with protected off-disk storage:

```bash
python -m deployment.phase19.backup snapshot /srv/polymind /protected-backup/phase19-window --writers-stopped
python -m deployment.phase19.backup restore /protected-backup/phase19-window /isolated-restore/phase19-window
```

The explicit stopped assertion is mandatory; the API lock alone cannot prove Redis/Chroma
are stopped. The tool locks the API domain, copies the whole data tree, preserves numeric
owners/modes, rejects symlinks/non-regular entries, compares SHA256 inventories before/after
and on restore, and checks restored SQLite integrity. Failures leave an unusable partial
copy for trusted inspection; they never repair or start it. Keep secret custody/config/image
identities with the backup under separate protection. Checksums detect damage, not malicious
replacement; protect the manifest too. Same-disk copies are not disaster recovery.

Restore only into a new isolated path/host; map its operator tree back to the **same `/state`
container path**. Never run it alongside a current authority/provider consumer. Verify newer
revocations, consumed permissions, financial/provider truth and immutable objects before
any serving/reconciliation. The tool deliberately cannot authorize stale financial rollback.
Rollback to a compatible image uses the same current authorities, not an older finance DB.
Cloud managed-disk snapshots, reboot, full-disk failure, independent recovery custody and
RPO/RTO remain Phase 19B validation requirements before final 19C documentation.

Before Azure: review the resolved integration and all remaining operator gates, subscription/RBAC/quota/access/egress, private
TLS/real OIDC browser proof, shared financial/admission obligations, source/capability/tariff/
execution permissions, SKU measurements, explicit cost/window/stop owner and residual retention.
B2as_v2 credits and D2as_v5 capacity cannot be qualified locally. USD 30 is a proposed envelope,
not permission. Compose stop is not Azure deallocation; any later approved cloud run must
separately verify deallocation and residual disk/network/snapshot charges.

To repeat the representative container experiment with a locally built image, use a **new**
absolute temporary directory (the harness refuses existing paths):

```bash
python scripts/phase19_offline_validation.py --root /tmp/polymind19-offline-new --image <reviewed-local-image-id>
```

This harness creates fixture keys/approvals outside Git, removes provider egress and all
published ports, loads real baked retrieval models, runs a bounded synthetic document,
samples all five containers, and stops/removes only its randomly named Compose project.
It preserves the private test data for inspection; it is never a production bootstrap or
real browser/OIDC acceptance test. Its generated configuration and counters are evidence
of the synthetic lane only. Do not supply real secrets to this harness.


## Integration gap resolution — 19 November 2026

Both paths use the same API image, SecurityRuntime, provider instance, governance/admission
SQLite authorities and existing action journal. No queue, financial ledger, service or database
schema was added. `PHASE19_EXECUTION_AUTHORITY` is the one new required Compose input: a
privately managed host directory, mounted **read-only** at `/run/secrets/execution-authority`.
Keep it outside the writable `/state` tree. Its files are owned by 10001 and mode 0600, its
directory 0700. Production verification refuses a writable authority mount. This narrow extra
mount protects independent trust/revocation custody without changing the service/storage topology.

```text
/etc/polymind/execution-authority/
  trust.json                  ApprovalTrust public key, independent key ID/operator binding
  revoked.json                JSON list of revoked canonical permission UUIDs; missing is fatal
  <permission-uuid>.jwt       independently signed execution permission
```

There is **no signing command** in the deployment. An independently authorized custodian must
review and supply any later real records. This phase only signed test-purpose records with
ephemeral keys. Do not renew, copy or consume historical Foundry approvals. The retained
`ApprovalTrust` shape is shared with the old launcher, but web permissions have distinct
issuer/audience/type/purpose and consume call identities in `actions.sqlite`, not its old
replay directory. The signer private key must never be mounted in an application container.

The JWT uses RS256, exact `typ=polymind-execution+jwt`, its independently configured `kid`,
issuer `polymind-independent-execution/1` and audience `polymind-execution/1`. Required claims:
canonical UUID `jti`, integer `iat <= nbf < exp`, lifetime at most 24 hours, `purpose=live`,
`binding`, `scopes`, `resource` and `max_calls` (1–32). The verifier rechecks signature, trust,
revocation, principal/tenant/enrollment, scope/resource and the exact server-computed binding
before dispatch and at acceptance/release boundaries. A new call also needs at least its
bounded deadline remaining on the permission and principal; Documents includes source/session
approval headroom. Consumption is durable and conservative even if later admission denies work.
It never refunds an uncertain attempt or automatically retries it.

`binding` is the existing canonical `fingerprint()` of the runtime's binding material, available
through the composed permission service for trusted offline review. It includes complete
reviewed configuration and manifest, enrollment/sources/session IDs, logical-role deployment
aliases, actual dispatch URL, managed/analysis/planning profiles, Chat policy/capabilities,
financial policy/catalog, provider quota policy/key and authority paths. It excludes secret
contents. Changed configuration or scopes require independently reviewed new permission;
a previously signed record must never be edited to broaden it. Do not hand-assemble or guess
a binding digest. Keep code/image/config identities with the independent review evidence.

For Documents, explicitly approve a new `pilot-execution-session/2` record using
`documents.pilot.models.ExecutionSessionApproval`. It has `zero_paid_execution=false`, an
`execution_permission` UUID, external consent and all inherited exposure/privacy/quality
references. Historical `pilot-session/1` still accepts **only true** and cannot satisfy the
bridge, even with a signed permission. The permission resource is
`{"session":"<session UUID>","source":"<fingerprint of full SourceApproval>"}` and its scopes
are `documents_synthesis` and/or `documents_question`. Set `execution_permissions=true` in a
reviewed manifest only when those independent inputs are ready. Absent inputs remain denied.

The retained workflow still performs source preflight, one durable runner, bounded managed
synthesis, explicit publication, question limits, financial reservation/settlement and UNKNOWN
handling. Dispatch now waits at least 61 seconds after the last shared call before claiming
another document step, consistent with the existing conservative pilot forecast. Actual
admission rechecks limits. Start/Question UI controls use the selected session's backend flags;
status polling and native reauthentication never grant execution or replay inference.

External digest presentation requires the existing two independent quality reviews. External
question generation returns `EXPERT_REVIEW_REQUIRED` with an opaque answer ID/evidence digest,
not an accepted answer. Trusted review maintenance uses the retained `review_packet`,
`answer_review_packet`, `attach_review` and `present_answer` facade contracts. Real review
records must be independently produced; tests' synthetic references are not human acceptance.
The API retains pending metadata and releases saved Q&A only after its own reviews validate.
The UI shows pending review state and never calls a provider just to refresh an accepted answer.
`POST /documents/operator/sessions/<id>/reload` explicitly rebuilds the authorized presentation
replica after restart; it does not restore worker grants or call a model.

For Chat, supply optional manifest `chat` matching `security.chat.ChatPolicy`: independent
`permission_id`, a closed list of `sessions` (safe 1–64 character ASCII identifiers), approved
`document_ids`, explicitly verified text/stream/usage capability and bounded output/deadline/
response/wire-byte limits. The permission scope is `chat`; its resource contains exactly
`{"sessions":[...],"documents":["<UUID>",...]}`. Its trust binds the one enrolled operator.
All referenced source approvals must be current and owned by that principal. An empty document
scope permits direct/tool Chat only; hybrid retrieval fails closed. Retrieval uses canonical
PublicationReplica filtering, per-document BM25, dense fusion/reranking and source-hash checks.
History is owner/tenant scoped and namespaced by the approved source set, so changing that set
cannot expose a former corpus through memory. Revocation blocks subsequent reads/releases.

The private Streamlit application now offers Documents and Chat with native access-token
forwarding. FastAPI independently verifies that API token; the client cannot grant itself a
principal or bypass the server context. Governed `/query` and `/query/stream` accept the existing
query/session fields plus a required 16–128 character `request_key` for explicit idempotent
execution. Both transports share one durable intent: changing transport replays the accepted
result in the requested format without a new model request. Changed payloads under the same
key are refused. Old local clients retain their existing behavior and optional key remains
unused in legacy mode. `/chat/context` and memory routes require the same principal/permission.

Chat preserves LangGraph routing/model roles and the NDJSON metadata/chunk/done/error format.
The streaming capability lives in additive inference modules; original pinned generation-provider
files and v10/v11 inventories remain byte-for-byte unchanged.
Bounded upstream SSE becomes provider-neutral chunks; actual usage settles through the existing
GovernedExecution path. Wire/content/model/termination bounds apply before acceptance. Missing
usage, truncation, timeout or cancellation retains UNKNOWN/unfinished evidence and blocks a new
provider call pending trusted reconciliation. An accepted result is persisted only after usage
and authorization checks. No browser or container restart resubmits a request.

Repeat both corrected paths through the existing topology using only isolated test inputs:

```bash
python scripts/phase19_offline_validation.py --root /tmp/polymind19-integration-new --image <reviewed-local-image-id> --integration-tests
```

This explicitly mounts test code read-only, uses test-purpose signatures and an in-process fake
OpenAI HTTP transport, removes all published ports/egress, and exercises real Redis/Chroma and
baked retrieval models. Test-only routes advance the fixture clock and attach synthetic review
records. They are never present in the production image or entrypoint. These tests prove offline
integration; real browser Entra consent/callback/TLS, current model capabilities/tariffs/quota,
independent live permission custody, semantic reviews and VM capacity remain independent
operator gates for Phase 19B validation.
No Azure provisioning, live inference or public exposure is authorized.

## 21 November 2026 — Current Phase 19B live-deployment readiness gate

Read-only preparation and local checks against `7bf82dc` are reclassified as a dated
Phase 19B continuation; see the [readiness report and operator packet](../codex/reports/phase_19b_live_deployment_readiness_continuation.md).
A1 resource/spending approval and A2 identity/network administration approval are still absent.
Do not run the cloud lifecycle commands above on that basis. West Europe has zero Basv2/DASv5
family quota in the observed subscription. Quota remediation, the private tunnel/egress route,
billing owner and exact window need explicit decisions before deployment. The existing
`127.0.0.1:9443` binding requires a tunnel that actually reaches host loopback; a VPN route to
the VM's private address alone does not expose this listener. No listener change is authorized
or implemented here. A3–A5 remain separate prerequisites for every later real-model plan.

Phase 19A Readiness Assessment is COMPLETE. Phase 19B Offline Implementation, Azure
Deployment, Live Integration and Validation is ACTIVE; real Entra/browser, synthetic cloud,
live Foundry, capacity/recovery and cost validation belong to that stage. Phase 19C Final
Documentation and Engineering Closure is NOT STARTED. Resolve A1 first and obtain each
independent approval before its affected action; this correction authorizes no live changes.

## 24 November 2026 — Post-provisioning verification finding

The operator subsequently provisioned `vm-epolymind-dev` in `rg-epolymind`, Spain Central.
The [post-provisioning report](../codex/reports/phase_19b_post_vm_creation_verification.md)
records actual Azure and guest evidence separately from the earlier offline assessments.
Verified: no VM public IP, Trusted Launch/Secure Boot/vTPM, two attached 64-GiB Standard
SSD LRS disks with Detach policies, expected effective subnet NSG/NAT and AKS deny,
stopped AKS, successful independent Azure Run Command recovery and installed Tailscale.

Actual cloud-init **failed** at `sshd -t` because `/run/sshd` was absent, before the
bootstrap's SSH enablement and completion marker. Ubuntu's `ssh.socket` is listening,
but effective SSH validation and private key authentication remain unverified. Do not
recreate the VM or rerun package installation blindly. A targeted service/runtime repair
requires a separately reviewed action, retaining the original failure evidence. Tailscale
is `NeedsLogin`; real enrollment is not authorized by its installation. Dummy protected
parameters worked, but real secret-safe handoff and saved tailnet policy tests remain gaps.
The data disk is unformatted/unmounted; `/srv/polymind` is absent. No storage initialization
or application launch was performed or authorized by this assessment.

The eight-hour window starts at **2026-11-24 01:26:38.7760141 UTC** and ends at
**09:26:38.7760141 UTC the same day**. The VM remained running at the report's last live
observation. The operator must cover the cutoff and verify `PowerState/deallocated`;
this task schedules no future action. NAT and its public IP were created the previous
day and continue charging independently; removal requires coordinated resource-specific
review. Retained disks also bill. USD 30 is a target, not an enforced cap. Infrastructure
readiness and application deployment readiness remain NO; real inference, public exposure
and AKS changes remain unauthorized. Phase 19B stays active; this is not 19C closure.

## 24 November 2026 — Dated post-boot SSH repair

The [SSH repair report](../codex/reports/phase_19b_ssh_bootstrap_repair_and_revalidation.md)
records the separately authorized single `systemctl enable --now ssh.service`, completed
at 07:37:07 UTC after inspection of the installed runtime-directory and socket behavior.
Current SSH readiness passes: root:root 0755 `/run/sshd`, active/enabled service and socket,
`sshd -t` exit 0, effective password/keyboard-interactive/root-login denial and public-key
authentication enabled. SSH public fingerprints and Azure Run Command recovery are preserved.
No reboot acceptance is claimed. Azure network exposure and associations remain unchanged.

The original cloud-init failure, absent completion marker and failed cloud-final.service
remain preserved; recovery does not retroactively make first boot successful. The separate
future candidate `/tmp/polymind-tailscale-cloud-init.corrected.yaml` starts the verified
service before standalone validation. It passed local checks and was not executed on the VM.
Tailscale remains NeedsLogin; real-key handoff, private Windows SSH, data filesystem and
application deployment remain gaps. No credential, enrollment, disk preparation or inference
was introduced. Full infrastructure/application deployment readiness remains NO.

The VM was still running at 07:41:42 UTC. The fixed **09:26:38.7760141 UTC today** cutoff
is unchanged. No deallocation or future scheduler was created by this repair; the operator
must cover cutoff deallocation, verify PowerState/deallocated and coordinate NAT/PIP and
disk-retention review. Retained resources may continue billing after compute deallocation.

## 24 November 2026 — Post-Azure continuation and current state

This dated continuation supersedes the earlier unmounted/unenrolled/undeployed findings
only where the operator supplied later executed evidence. The historical first-boot FAIL,
repair report and expired evaluation cutoffs above remain unchanged. **No command in this
section was executed against Azure by this offline continuation.**

The operator reports private Tailscale/OpenSSH access, ext4 data-disk preparation and reboot
remount, Docker Engine 29.10.0/Compose v5.8.0, secure image transfer/import, pinned Compose
validation and network-disabled CPU embedding/reranking PASS. SSH, tailscaled and Docker
were active after reboot. The VM was subsequently **reported deallocated**. Its actual
current Azure power state, full outbound controls and ongoing charges were not queried.

The authoritative filesystem UUID is **`c95e5fce-443b-4d90-9160-8b67758f12d9`**, mounted at
`/srv/polymind`. `/dev/sda` and `/dev/sdb` changed across lifecycle operations. **Do not format,
partition or initialize this disk again.** Verify UUID/target/filesystem and numeric owners
before future use. Reported directories: operator 10001:10001, Redis 999:999, Chroma
10001:10001, all 0700; operator/private, objects and sources also restrictive.

The transferred image is `polymind:phase19-reviewed`, identity
`sha256:9f386acf8bddcb5d01bb028151caae24b5df604f8a56c00b7b39c7e0f8298c02`, revision label
`7bf82dc2da4a9f29561a5f493b690502c0090eb0`. The local audit matches 135 runtime Python files
byte for byte; this continuation changes tests/documentation only and requires no rebuild.
A later runtime/dependency/Dockerfile/model-packaging change requires a newly verified image
and separately authorized secure transfer. A local image ID is not automatically a registry
manifest digest.

Azure-staged vendor references are:

```text
redis@sha256:7f7d30b7fdd09467bac58198a1f166dd69789d348d4fe859cccb20e0cf287fbe
chromadb/chroma@sha256:1e0b73a187a28757c572acba508c46f48c9e8b0acaf5c20e6d95cdedce1acdf6
```

The root-owned `/opt/polymind/docker-compose.phase19.yml` and `compose.env.example` were
staged/parsed on Azure. This pinned copy has **not** been copied into tracked Compose;
the repository still uses Redis 7.4-alpine/Chroma 1.5.9 tags plus the selected application
image input. Local cached Redis resolves to `sha256:ff02b58f971e7d7d156a1267e283fcbbeee91773b6aa36c49dac28ecfe28eadf`,
which differs from the operator's Azure reference. No equivalence or cross-platform manifest
relationship is inferred. Verify the exact staged digests/architecture and reviewed file
hash in the next session; do not overwrite the pinned copy with the tag-based source blindly.

Production configuration was intentionally absent: `/etc/polymind/compose.env`, provider,
Streamlit/TLS files, execution-authority directory and operator deployment/configuration/
manifest records. The seven production authorities were **not initialized**, the five-service
stack was **not started**, and the mount-aware systemd unit was **not installed/enabled**.
The gateway's loopback/security preflight is configuration evidence, not browser TLS/login
or runtime network enforcement. Full capacity, Azure backup/restore and application reboot
acceptance remain pending. See the [post-Azure report](../codex/reports/phase_19b_post_azure_readiness_offline_validation_evidence_reconciliation.md).

### Operator-supplied non-secret configuration decisions

Supply reviewed values/references through the private deployment process, without posting
credentials or signed permissions in chat/Git. No value below is selected by this run.

| Input | Exact contract / decision needed |
|---|---|
| Entra directory | Canonical public-cloud tenant UUID `T`; `OIDC_CONFIGURATION.token_profile=entra_v2`, `tenant_id=T`, `issuer=https://login.microsoftonline.com/T/v2.0`, `jwks_url=https://login.microsoftonline.com/T/discovery/v2.0/keys` |
| API registration | Canonical API client UUID as scalar `audience`; v2 access tokens; exposed Application ID URI and delegated `access_as_user`; assigned user role exactly `PolyMind.L1Operator`, with no additional token roles |
| Browser registration | Native Streamlit client UUID, tenant-specific discovery metadata URL, approved authorization-code registration/consent and exact redirect URI; requested scope `openid` plus `<API Application ID URI>/access_as_user` and any separately reviewed identity scopes |
| Enrollment | Exact `[issuer, tenant UUID, access-token subject]` in `RuntimeManifest.enrollment`; subject must be the API access-token `sub`, not email/display name/`oid` or an assumed ID-token subject |
| Native auth fields | `[auth] redirect_uri`, `server_metadata_url`, `client_id`, `expose_tokens=["access"]`; `[auth.client_kwargs] scope`; private `client_secret` and `cookie_secret` supplied only by custodian, never this table |
| Private origin | Fixed `https://<approved private hostname>:<browser-visible port>` with no path/query/fragment/credentials; matching `PHASE19_ORIGIN`, exact Host and WebSocket Origin, native redirect `<origin>/oauth2callback` |
| Certificate/trust | SAN covering that private hostname, valid server chain and private key, browser trust/distribution and renewal owner; all mounted TLS files 10001-owned, mode 0600, regular/non-symlink; do not treat test TLS material as production trust |
| Tunnel | Approved Tailscale/OpenSSH endpoint and local **loopback** forwarding to VM `127.0.0.1:9443`; private browser hostname resolves to the local tunnel, port matches origin/callback; keep SSH host verification and TLS validation |
| Source | Approved immutable bytes/SHA256, owner scope derived by `stable_id` from enrolled issuer/tenant/subject, rights/classification/transmission/retention, current SourceApproval and separate consent/exposure/privacy/quality/session approvals |
| Provider | Approved HTTPS dispatch base (Foundry candidate `/openai/v1/`), model deployment/version/type/region and response aliases, all logical roles (`general`, `fast`, `coding`, `summarization`), `api-key` versus `Authorization`, credential-custody reference; no token refresh implemented |
| Capabilities | Managed prompt 11 profiles, `azure-strict/1`, context/output/deadline/envelope limits and usage reporting; separate analysis and Chat streaming/usage capabilities. Metadata is not live compatibility proof |
| Finance/admission | Approved applicable tariff/currency/catalog covering used aliases, tenant/owner budgets, shared provider key/RPM/TPM/concurrency/interactive policy, shared-consumer/exclusivity evidence and reconciled outstanding obligations |
| Execution custody | Independently controlled read-only authority root, public trust/key ID and operator binding, revocation list; new live permission only after independent approval of frozen binding, exact scopes/resource/call bound/window. Signer key never enters the application |

`configuration.json` is explicit: inherited dotenv/environment does not fill missing production
values. Use the existing example as a field inventory, not a valid configuration. The adapter
accepts generic HTTPS v1 paths; this is not enforcement or proof of a Foundry `/openai/v1/`
endpoint. Supply the actual approved endpoint and verify compatibility only when authorized.
The native browser flow and login/logout/reauthentication/cookie/expiry behavior still need
real browser acceptance; offline signed JWT tests establish only the server contract.

### Next authorized session — Gates A–E

Each gate is a separately reviewable future step. These instructions grant no cloud, identity,
production lifecycle, signing, model-spend or public-exposure permission.

**Gate A — Freeze operator-controlled inputs.** Resolve the table above and record independent
identity/TLS, source/provider/data, finance/quota and execution-custody approvals. Keep new
model expenditure separate from infrastructure expenditure. For a no-inference startup,
review an explicit execution-disabled manifest; never substitute fake production credentials
or use the local synthetic harness as a production switch. Missing permission remains denied.
Real semantic review must remain independent; synthetic attached reviews confer no acceptance.

**Gate B — Authorize and revalidate existing infrastructure.** Obtain fresh subscription/resource,
cost ceiling, allocated-time window, cutoff and named start/stop/deallocation/residual owners.
The old four-hour session and older eight-hour cutoffs have ended. Under that authorization,
confirm exact VM identity/current power state before any activation. Revalidate private SSH,
Tailscale policy and host key; verify actual outbound destination controls separately from
Compose and NSG HTTPS permits. Verify filesystem UUID, ext4 mount and owners without disk
initialization. Verify reviewed image identity/label, architecture, staged Compose/vendor digests
and file hashes. Preserve `/opt/polymind` and mount-aware systemd expectations.

**Gate C — Provision configuration, then deliberately initialize a new authority set.**

1. Privately provision reviewed `/etc/polymind/compose.env` and the required secret files,
   with appropriate host traversal and UID 10001/0600 access. Keep signer custody separate;
   execution-authority mounts read-only. Validate metadata/modes without printing contents.
2. Confirm stable operator root `/state`. Supply `deployment.json` exactly
   `{"version":"phase19-state/1","container_root":"/state"}`, explicit `configuration.json`,
   and `manifest.json` matching `RuntimeManifest`. Preserve existing runtime.lock inode.
3. Provision approved `sources/<sha256>` with restrictive modes; verify every source hash,
   issuer/tenant/owner and approval window, model/capability/catalog/policy/path binding.
   Decide current authority reuse versus a genuinely new approved set. Reconcile any existing
   obligations; never create an empty ledger to hide them.
4. Start **only Redis/Chroma** under the reviewed Compose inputs and verify health/persistence.
   Actual initialization constructs retrieval adapters, so data service availability and
   baked model artifacts precede it. The existing image and explicit init process need no
   provider request or Entra login to create schemas.
5. Only if all seven databases are absent in the approved new state, run the existing
   `initialize /state` command above once. Actual construction order is security → governance
   → admission → jobs/publication → pilot → actions (all version 1). Source/config checks precede
   creation; models/vector construction may fail after the first authorities are created.
6. Verify all seven files exist separately: `security.sqlite`, `governance.sqlite`,
   `admission.sqlite`, `jobs.sqlite`, `pilot.sqlite`, `actions.sqlite`, `publication.sqlite`.
   Check UID/modes, schema and SQLite integrity, canonical objects and bindings. The `check`
   command validates preflight/configuration only; it does not verify all credentials,
   manifest/permission/source semantics or end-to-end readiness. Constructors validate schemas
   when the full runtime is opened. Never bypass a partial failure by deleting or resetting DBs.

Initialization does not grant enrollment, consent or execution. API middleware registers a
verified principal in the security authority, but workflow enrollment/owner/permission checks
still independently restrict it. Independently managed trust/revocation structure is required
before enabling governed execution; no signing or new live record is performed here.

**Gate D — Controlled application startup.** After lifecycle authorization, start the single
API/runner using `serve`, then UI and gateway through existing health ordering. Retain lock,
read-only roots/capability drops and `127.0.0.1:9443` only. Missing state, unsafe modes, missing
credentials, dependency/JWKS failure or unsettled obligations must remain unavailable. Check
real private HTTPS/WebSockets and native Entra browser/API access only when authorized;
exercise wrong-user/tenant/role and cross-owner denial. Login/refresh/restart do not grant
execution. Paid workflow execution additionally requires A3–A5, exact serial plan/deadline/
budget and independent live permission; absent that, execute no inference. Do not manufacture
reviews to expose a digest or answer. Observe capacity on the actual 2-vCPU/8-GiB host.

**Gate E — Recovery and closure.** Stop admission, wait for bounded work, preserve/reconcile
unsettled reservations and UNKNOWN without replay, then stop all five writers. Verify stopped
containers/AOF flush, quiesced full-tree backup and protected off-disk custody. Test an isolated
restore and controlled restart only if approved; preserve newer security/financial/revocation/
consumption truth and fixed container paths, never run a live clone. Record integrity, resource,
shutdown/recovery time and costs. Deallocate within the new window and independently confirm
actual deallocated power state. Inventory retained disks, NAT/PIP and other residual charges;
name their owners and review dates. No automatic resource deletion is implied. Azure application
reboot/restore/RPO/RTO acceptance remains distinct from the earlier infrastructure reboot.

## 25 November 2026 — Selected private HTTPS origin and Gate A update

This dated update selects repository configuration only. Phase 19A is COMPLETE;
Phase 19B — Offline Implementation, Azure Deployment, Live Integration and Validation —
remains ACTIVE; Phase 19C — Final Documentation and Engineering Closure — is NOT STARTED.
The VM is **operator-reported deallocated**; no fresh Azure inspection was performed.
No procedure below has been executed. Entra changes, VM activation/SSH, operational certificate
creation, hosts/trust changes and production startup need separate authorization.

| Contract | Selected Phase 19B private verification value |
|---|---|
| Origin / `PHASE19_ORIGIN` | `https://polymind.test:9443` |
| Exact native OIDC and Entra Web callback | `https://polymind.test:9443/oauth2callback` |
| HTTP Host / WebSocket Origin | `polymind.test:9443` / `https://polymind.test:9443` |
| Windows hosts mapping | `127.0.0.1 polymind.test` |
| Windows SSH bind / remote forwarding target | `127.0.0.1:9443` / `127.0.0.1:9443` |
| VM published gateway / container TLS port | `127.0.0.1:9443:9443` / `9443` |
| Server certificate SAN / minimum TLS | `DNS:polymind.test` / TLS 1.2 |
| Certificate approach | Dedicated private CA-signed server certificate |

`.test` is for this bounded private verification environment. No public DNS, public listener,
public CA, new service or infrastructure is required. Another explicitly approved private
hostname remains supported by the generic gateway; change the whole contract together.
The container listens on its own interface; Docker publishes it only on VM loopback.

### Gate A — Current identity and configuration evidence

Operator-reported on 25 November: API `estudio-polymind-api-dev`, application/client UUID
`5aa70f9d-9f9e-4b5b-972b-698d4d68105e`, Application ID URI
`api://5aa70f9d-9f9e-4b5b-972b-698d4d68105e`, service principal object UUID
`046ce5b0-897c-4289-ad86-e403ac6b6e20`, single tenant `AzureADMyOrg`, delegated
`access_as_user`. Enabled user role `PolyMind.L1Operator` has UUID
`e34bc374-42ff-4a6a-87e2-007b8cc788b3`. Exactly one role assignment was reported: principal
type User, principal UUID matched the signed-in operator's directory object, role UUID matched
that enabled role. This is **OPERATOR_REPORTED_PASS at configuration level only**.
No real browser login or API access-token validation follows from it.

Existing reported inventory contains API and `estudio-polymind-cli-dev`; the dedicated
`estudio-polymind-streamlit-dev` is absent. Do not modify the API or CLI registrations.
Tenant UUID and browser client UUID remain operator-supplied, not invented here.

| Gate A item | Current state |
|---|---|
| Selected origin/callback/SAN/tunnel contract | Selected in repository; offline verified |
| API role assignment | Operator-reported configuration PASS; runtime token claims unverified |
| Browser registration / exact Entra redirect acceptance | PENDING / PENDING |
| Browser identity / delegated permission / consent / client and cookie secrets | PENDING |
| Operational CA/server issuance / Windows trust / custody and validity decisions | PENDING |
| Windows hostname resolution / tunnel endpoint acceptance | PENDING |
| Runtime enrollment `[issuer, tenant, API access-token sub]` | BLOCKED; never substitute directory `oid`, email, display name or ID-token `sub` |
| Real private browser authentication / production runtime activation | BLOCKED / BLOCKED |
| Other Gate A source, consent, semantic review, provider, financial/quota and independent permission inputs | Still required; unchanged |

Gates B–E and all existing data/finance/recovery/capacity/outbound requirements remain in force.
Origin selection and user app-role assignment do not authorize inference, initialize authorities,
or satisfy independently signed execution permission.

### Native Streamlit configuration and consistency review

Use the inert [native OIDC field inventory](../../deployment/phase19/streamlit.secrets.example.toml).
It is deliberately outside `.streamlit`, has an example-only name and is never automatically
loaded, mounted or copied to the runtime secret location. Populate a **separate** private
`/etc/polymind/secrets/streamlit.toml`; never mount the example. Replace every angle-bracket
placeholder. Structural TOML parsing and Streamlit's key-presence checks do not validate
identifiers, secrets, consent or operational readiness.

The environment-specific delegated scope is
`api://5aa70f9d-9f9e-4b5b-972b-698d4d68105e/access_as_user`.
The API audience is the bare API UUID; the browser client UUID is a separate application.
Tenant-specific discovery is
`https://login.microsoftonline.com/<TENANT_UUID>/v2.0/.well-known/openid-configuration`.
Native `[auth]` uses `redirect_uri`, `server_metadata_url`, `client_id`, private `client_secret`,
private strong random `cookie_secret`, `expose_tokens=["access"]`; `[auth.client_kwargs]`
uses `scope="openid api://<API_CLIENT_UUID>/access_as_user"`. No Graph permissions are needed.

Streamlit 1.58.0 is pinned and locally installed. Its default provider accepts these fields;
its Starlette auth routes use authorization code, state/nonce and S256 when advertised by
provider metadata. Confidential-client credentials belong to Streamlit on the server.
Both UI planes forward `st.user.tokens['access']` to FastAPI; the API independently verifies
the tenant-specific Entra v2 token, API audience, delegated scope, exact role, enrollment,
revocation and owner/tenant authorization. ID/Graph tokens do not substitute. Missing execution
permission still denies model work. Token expiry/logout/reauthentication remain live acceptance.
See [Streamlit 1.58 login](https://docs.streamlit.io/1.58.0/develop/api-reference/user/st.login)
and [Microsoft authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow).

Before provisioning, the operator/custodian must compare the three independently stored values:
`PHASE19_ORIGIN + "/oauth2callback"`, native `auth.redirect_uri`, and registered Entra
`web.redirectUris` must be exactly `https://polymind.test:9443/oauth2callback`, including port
and case. Verify metadata tenant, client UUID, delegated scope and actual certificate SAN
against the approved record without printing secrets. Reject placeholders or a mismatch;
do not start services to test a guessed configuration. Existing runtime code does not perform
an automatic cross-file comparison: the UI and gateway have separate read-only mounts and
only the gateway receives `PHASE19_ORIGIN`. The new repository regression checks template
consistency; this operational comparison is still mandatory for populated external files.
Wrong callback configuration does not bypass API token or gateway checks; it breaks login.
No new configuration framework or application change is needed for this origin selection.

### Proposed Entra browser registration — operator review only

Historical procedure, 25 November. The [26 November addendum](#26-november-2026--streamlit-oidc-preparation-and-current-gate-a-evidence)
records operator-reported completion; no repeat mutation is authorized.

The following Bash/Azure CLI steps are **future individually reviewed actions**, not a script
to run as a batch. Use an already authorized administrative session in the reviewed tenant;
this task performs no login or cloud commands. Stop on any unexpected inventory, tenant,
permission, consent or redirect result. Review [CLI application commands](https://learn.microsoft.com/en-us/cli/azure/ad/app?view=azure-cli-latest)
and [delegated permissions](https://learn.microsoft.com/en-us/cli/azure/ad/app/permission?view=azure-cli-latest).

1. Verify the signed-in tenant and list applications/service principals before mutation.
   Compare the tenant to the operator-supplied UUID. Require zero dedicated browser matches;
   if one exists, inspect it rather than creating a duplicate; if multiple, stop and reconcile.

   ```bash
   az account show --query '{tenantId:tenantId}' -o json
   az ad app list --filter "displayName eq 'estudio-polymind-streamlit-dev'" --query '[].{id:id,appId:appId,displayName:displayName}' -o json
   az ad sp list --filter "displayName eq 'estudio-polymind-streamlit-dev'" --query '[].{id:id,appId:appId,displayName:displayName}' -o json
   ```

2. Discover the API scope UUID; it is **not** the app-role UUID. Verify exactly one enabled
   `access_as_user` scope, consent type/descriptions, v2 token version and existing API identity.
   Do not repair the API registration as part of browser registration without separate review.

   ```bash
   PHASE19_API_CLIENT='5aa70f9d-9f9e-4b5b-972b-698d4d68105e'
   az ad app show --id "$PHASE19_API_CLIENT" --query '{appId:appId,audience:signInAudience,uris:identifierUris,tokenVersion:api.requestedAccessTokenVersion,scopes:api.oauth2PermissionScopes}' -o json
   # Set only the discovered, reviewed enabled scope UUID:
   PHASE19_API_SCOPE_UUID='<DISCOVERED_ACCESS_AS_USER_SCOPE_UUID>'
   ```

3. Only after authorization and zero-match inventory, register the dedicated confidential
   **Web** application, single tenant, with the exact URI. No SPA/native platform, implicit
   grants, public-client fallback or client-credentials API permission is required.

   ```bash
   az ad app create --display-name estudio-polymind-streamlit-dev --sign-in-audience AzureADMyOrg --web-redirect-uris 'https://polymind.test:9443/oauth2callback' --enable-access-token-issuance false --enable-id-token-issuance false --is-fallback-public-client false --query '{id:id,appId:appId,displayName:displayName}' -o json
   # Copy the returned non-secret appId after review:
   PHASE19_BROWSER_CLIENT='<RETURNED_BROWSER_APP_UUID>'
   ```

4. Read back the exact **Web** URI and flow settings. URI is configured on the application,
   not the service principal. No wildcard or localhost substitution. `polymind.test` uses the
   explicit port; Microsoft's localhost port-matching exception does not apply.

   ```bash
   az ad app show --id "$PHASE19_BROWSER_CLIENT" --query '{appId:appId,signInAudience:signInAudience,web:web,spa:spa,publicClient:publicClient,isFallbackPublicClient:isFallbackPublicClient}' -o json
   ```

   [Microsoft redirect restrictions](https://learn.microsoft.com/en-us/entra/identity-platform/reply-url)
   support HTTPS and exact non-localhost port matching. No documented conflict was identified
   for this selection; **actual tenant acceptance remains PENDING**. If rejected, preserve the
   exact error without tokens and request review; do not silently change origin.

5. Inspect service principals by the returned app UUID. Create only if absent, then read back.

   ```bash
   az ad sp list --filter "appId eq '$PHASE19_BROWSER_CLIENT'" --query '[].{id:id,appId:appId}' -o json
   # Only if zero results, separately reviewed:
   az ad sp create --id "$PHASE19_BROWSER_CLIENT" --query '{id:id,appId:appId}' -o json
   ```

6. Add only the discovered delegated API scope (`Scope`, not `Role`). Review pending requested
   permissions before consent; adding a requested permission does not grant it.

   ```bash
   az ad app permission add --id "$PHASE19_BROWSER_CLIENT" --api "$PHASE19_API_CLIENT" --api-permissions "$PHASE19_API_SCOPE_UUID=Scope"
   az ad app permission list --id "$PHASE19_BROWSER_CLIENT" -o json
   ```

7. Assess the scope's consent type, tenant user-consent policy and conditional access with
   the authorized identity administrator. Obtain the narrow required delegated consent using
   the organization's reviewed portal flow. No unconditional `admin-consent` command is
   prescribed; it could consent every requested permission. No broad tenant-wide privilege,
   Graph API scope or modification to the CLI/API application is requested. User app-role
   assignment remains separate from browser delegated consent.

8. The credential custodian reviews validity/rotation, creates the browser application's
   confidential client secret in the authorized portal, and transfers the one-time value
   directly to the approved secret vault and private Streamlit file using the secure custody
   process. No terminal output, shell argument/history, clipboard transcript, logs, screenshot,
   chat or repository secret. Do not use a default `az ad app credential reset` that prints
   the secret or deletes other credentials. Generate the separate cookie secret privately.
   Do not create/retrieve either during this task. Portal creation alone is not API acceptance.

9. Perform read-only verification of application, service principal, required resource access,
   grants and credential **metadata only**. Confirm no implicit/public flows, unexpected
   redirects or Graph permissions. Record the browser UUID, scope UUID and consent status.

   ```bash
   az ad app show --id "$PHASE19_BROWSER_CLIENT" --query '{appId:appId,signInAudience:signInAudience,web:web,publicClient:publicClient,isFallbackPublicClient:isFallbackPublicClient,requiredResourceAccess:requiredResourceAccess}' -o json
   az ad sp list --filter "appId eq '$PHASE19_BROWSER_CLIENT'" --query '[].{id:id,appId:appId}' -o json
   az ad app permission list-grants --id "$PHASE19_BROWSER_CLIENT" -o json
   az ad app credential list --id "$PHASE19_BROWSER_CLIENT" --query '[].{keyId:keyId,displayName:displayName,start:startDateTime,end:endDateTime}' -o json
   ```

No token acquisition is part of registration verification. Runtime enrollment waits for a
separately authorized API access-token verification of exact issuer/tenant/`sub`; never
infer it from the directory role assignment. Freeze new reviewed bindings where required.

### Windows hostname resolution and private tunnel — future PowerShell procedure

The intended path is Windows browser → `polymind.test:9443` → Windows loopback →
Windows-native OpenSSH over the existing Tailscale route → VM loopback `127.0.0.1:9443` →
Docker gateway → Streamlit → internal FastAPI. Hosts resolution changes the connection
address only; URL hostname, TLS SNI/name verification, HTTP Host and WebSocket Origin stay
`polymind.test` with the selected port. Do not browse to a loopback IP or VM IP URL.

The standard hosts file is `%SystemRoot%\System32\drivers\etc\hosts`
(normally `C:\Windows\System32\drivers\etc\hosts`). After separate approval, a Windows
administrator adds exactly `127.0.0.1 polymind.test` without conflicting mappings, preserving
other entries. Do not add an IPv6 mapping for this IPv4 tunnel. Then verify in PowerShell:

```powershell
$ErrorActionPreference = 'Stop'
[System.Net.Dns]::GetHostAddresses('polymind.test') | ForEach-Object { $_.IPAddressToString }
$Phase19Listeners = @(Get-NetTCPConnection -State Listen -ErrorAction Stop | Where-Object { $_.LocalPort -eq 9443 })
if ($Phase19Listeners.Count -gt 0) { $Phase19Listeners; throw 'Port 9443 is already in use.' }
```

Require resolution only to `127.0.0.1` and the port to be free before forwarding. If occupied,
identify the owner; do not kill an unrelated listener or change the selected port silently.
`nslookup` queries DNS directly and is not proof of Windows hosts-file resolution.

Historical repair records identify user `polymindadmin`, a Windows key
`$env:USERPROFILE\.ssh\id_ed25519_polymind_azure`, and VM Ed25519 public host fingerprint
`SHA256:tGW/X/urHlViBMqFsJtgeVgrnt2xZxup3Duw/jN6vHg`. The recorded `100.108.249.65` is
**the Windows operator device**, not a VM target. No authoritative final VM tail IP/alias
was located; keep the target placeholder until reconfirmed by the operator. Verify the
existing known_hosts entry/fingerprint through the approved independent record before SSH;
never trust a fresh `ssh-keyscan` alone or accept an unexpected key change. Check Windows
known_hosts as well as any historical WSL entry: they are different files.

```powershell
$Phase19VmTarget = 'polymindadmin@<VERIFIED_VM_TAILSCALE_IP_OR_APPROVED_SSH_ALIAS>'
# Foreground Windows ssh.exe; all placeholders must be resolved before execution.
ssh.exe -N -T -o ExitOnForwardFailure=yes -o StrictHostKeyChecking=yes -o IdentitiesOnly=yes -i "$env:USERPROFILE\.ssh\id_ed25519_polymind_azure" -L 127.0.0.1:9443:127.0.0.1:9443 $Phase19VmTarget
```

Once later-authorized gateway startup, trusted TLS and tunnel are ready, open
`https://polymind.test:9443` in the approved Windows browser. Verify the listener is Windows
loopback only and inspect certificate name/chain without bypassing errors. Keep SSH in the
foreground; close the browser session/log out as appropriate, then Ctrl+C in that window
and confirm the listener disappears. Reuse existing verified Tailscale/OpenSSH, no new route.
A WSL-bound forward is a different network endpoint: Windows-to-WSL localhost forwarding
was **not verified** here. Do not assume it works or broaden the bind to `0.0.0.0` to compensate.

### Dedicated private CA and server TLS — future reviewed procedure

No operational keys/certificates/trust are created here. Before issuance the operator must
approve the CA custodian, protected offline custody/backup, CA and leaf lifetimes, renewal
lead time, revocation/distribution owner and Windows user/browser trust scope. The following
Bash/OpenSSL recipe runs only in a new protected custody workspace after that approval;
`PHASE19_CA_DAYS`, `PHASE19_LEAF_DAYS`, `PHASE19_CRL_DAYS` are reviewed positive integers,
not values selected by this task. CA validity must cover the approved leaf validity.
Use the organization's approved cryptographic policy; this recipe uses encrypted RSA-3072
CA custody and RSA-2048 server key. Passphrases are entered interactively, never arguments.

```bash
set -eu
umask 077
# Select a new protected directory outside the repository; refuse an existing CA workspace.
mkdir phase19-private-ca
cd phase19-private-ca
mkdir newcerts
: > index.txt
openssl rand -hex 16 > serial
printf '01\n' > crlnumber
cat > ca.cnf <<'EOF'
[ca]
default_ca = dedicated
[dedicated]
dir = .
database = $dir/index.txt
new_certs_dir = $dir/newcerts
certificate = $dir/ca.crt
private_key = $dir/ca.key
serial = $dir/serial
crlnumber = $dir/crlnumber
default_md = sha256
policy = server_policy
unique_subject = no
copy_extensions = none
[server_policy]
commonName = supplied
[server]
basicConstraints = critical,CA:false
keyUsage = critical,digitalSignature,keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = DNS:polymind.test
EOF
# Supply approved durations through this protected shell before proceeding.
: "${PHASE19_CA_DAYS:?Operator-approved CA validity required}"
: "${PHASE19_LEAF_DAYS:?Operator-approved server validity required}"
: "${PHASE19_CRL_DAYS:?Operator-approved CRL validity required}"
openssl genpkey -algorithm RSA -aes-256-cbc -pkeyopt rsa_keygen_bits:3072 -out ca.key
openssl req -new -x509 -sha256 -key ca.key -days "$PHASE19_CA_DAYS" -subj '/CN=PolyMind Phase19 Private Verification CA' -addext 'basicConstraints=critical,CA:true,pathlen:0' -addext 'keyUsage=critical,keyCertSign,cRLSign' -out ca.crt
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out tls.key
openssl req -new -key tls.key -subj '/CN=polymind.test' -out server.csr
openssl ca -config ca.cnf -extensions server -days "$PHASE19_LEAF_DAYS" -in server.csr -out server.crt -notext
openssl verify -purpose sslserver -verify_hostname polymind.test -CAfile ca.crt server.crt
openssl x509 -in server.crt -noout -subject -issuer -dates -ext 'subjectAltName,extendedKeyUsage'
openssl x509 -in ca.crt -noout -fingerprint -sha256
# This direct root-to-leaf recipe has no intermediate: tls.crt contains the leaf only.
cp server.crt tls.crt
chmod 600 tls.crt tls.key
```

The `openssl ca` database and serial files must be retained in protected CA custody for
renewal/revocation; do not recreate them. Never deploy `ca.key` to the VM or image. If a
separately reviewed CA hierarchy uses intermediates, `tls.crt` must contain leaf then all
required intermediates; the trusted root is distributed separately. Inspect public leaf
and CA fingerprints, validity, SAN, serverAuth, chain and public-key match before transfer.
For key matching compare these public hashes only, never print the private key:

```bash
openssl x509 -in tls.crt -pubkey -noout | openssl pkey -pubin -outform DER | openssl dgst -sha256
openssl pkey -in tls.key -pubout -outform DER | openssl dgst -sha256
```

After separate authorization, transfer only `tls.crt` and `tls.key` through the existing
host-verified encrypted channel and protected staging (no email, logs, clipboard transcript
or repository). On the VM, a trusted custodian installs only regular non-symlink single-link
files at `/etc/polymind/secrets/tls.crt` and `/etc/polymind/secrets/tls.key`,
**UID:GID 10001:10001, mode 0600**. Use dedicated root-controlled parent paths with traversal
for UID 10001 (for example `/etc/polymind` root:10001 0750 and secrets root:10001 0710),
no untrusted write access or symlink ancestors. Review existing directories before changing
them. Verify with `namei -l` and `stat` without reading private contents. Docker requires
readable source paths and mounts individual files read-only with `create_host_path:false`.
Container UID 10001 must read the mounted file through `/run/secrets`; container paths and
ownership must be verified after a separately authorized start. The gateway's `private_path`
checks effective UID, regular file, one link, no symlink ancestors and no group/other mode
bits; the operational contract also requires GID 10001 and exact 0600. Streamlit's secret
mount is read-only/missing-source fail-closed, but its parser does not enforce those file
ownership checks: custodian preflight is required for that file too.

For Windows, distribute **only the CA public certificate**, validate its SHA256 fingerprint
via the independent approved record, and import into the approved operator account's Trusted
Root Certification Authorities store after separate approval. Example PowerShell commands:

```powershell
# Use the reviewed public certificate path and inspect thumbprint/identity first.
certutil.exe -hashfile '<PUBLIC_CA_CERT_PATH>' SHA256
certutil.exe -user -addstore Root '<PUBLIC_CA_CERT_PATH>'
# Later remove only this CA after verifying its exact stored thumbprint:
certutil.exe -user -delstore Root '<VERIFIED_DEDICATED_CA_THUMBPRINT>'
```

Use the organization's browser trust policy; managed Edge/Chrome may use Windows trust,
while Firefox or managed profiles may require separately reviewed trust settings. Verify the
actual approved browser chain/name/expiry, not just import success. No verification bypass,
`curl -k`, browser exception or SSH host-check disabling is allowed. Protect server-key
backups; application containers get no CA key and browsers get no private key.

Renew before the reviewed deadline: issue a fresh leaf/key, validate SAN/chain/permissions,
securely replace through controlled stop/start because the gateway loads TLS at startup,
and recheck browser/Host/Origin behavior. Revoke compromised/superseded leaves using the
retained CA database and generate a current CRL with reviewed validity:

```bash
openssl ca -config ca.cnf -revoke server.crt
openssl ca -config ca.cnf -gencrl -crldays "$PHASE19_CRL_DAYS" -out ca.crl
```

No CRL distribution endpoint or automatic browser revocation enforcement is implemented by
this recipe. A generated CRL alone does not protect an offline browser. The operator must
review effective revocation distribution/enforcement before operational acceptance; on
compromise stop use, withdraw affected trust as needed, replace keys/certificates and verify
clients before resuming. CA compromise requires removal of that exact root from all affected
profiles and reissuance under new reviewed custody. On retirement stop the tunnel/deployment,
remove only the dedicated hosts entry and CA trust, retire server keys securely under retention
policy and preserve necessary issuance/revocation audit. No public PKI service is introduced.

## 26 November 2026 — Streamlit OIDC preparation and current Gate A evidence

This dated addendum supersedes earlier pending browser-registration findings at the
**operator-reported configuration** level only. The operator reports API v2/scope/role and
role assignment, dedicated browser Web registration, accepted exact redirect, enabled
Application service principal, required delegated API permission, persisted Principal-only
consent and one confidential credential's metadata verified on 25–26 November. Tenant-wide
consent was NOT granted. Do not repeat the historical registration/credential steps above.

The [current OIDC report](../codex/reports/phase_19b_streamlit_oidc_configuration_preparation.md)
reconciles every supplied identifier and contains the single environment-specific non-secret
reference, complete independently executable local preparation procedure, optional GPG staging
and future direct SSH installation procedure. Preserve the portable template placeholders.
Run the procedure independently after operator review, outside Codex, using the existing
client-secret value at a secure hidden prompt. Proposed local path is
`~/.config/polymind/phase19/streamlit.toml`, Linux directory 0700 and file 0600, exclusive/no-follow
creation; independent CSPRNG cookie; metadata-only validation. A populated TOML contains two
plaintext secrets. Preserve the cookie across ordinary restarts; protect encrypted staging
while inactive and avoid redundant plaintext. Actual custody/encryption is not independently
verified. No operational file or cookie was created during preparation.

| Gate A identity item | Current evidence / limit |
|---|---|
| API configuration / role assignment | OPERATOR_REPORTED_PASS; actual token claims unverified |
| Browser registration / accepted exact Web redirect | OPERATOR_REPORTED_PASS |
| Enabled browser SP / delegated API permission | OPERATOR_REPORTED_PASS |
| Operator-specific Principal consent | OPERATOR_REPORTED_PASS; no tenant-wide consent |
| Confidential client credential metadata | OPERATOR_REPORTED_PASS; actual value unseen |
| Native Streamlit configuration and secure procedure | Offline PASS; installed 1.58.0 contract and synthetic tests |
| Actual credential custody / encryption / validity | GAP; not independently verified |
| Operational cookie / populated TOML / Azure installation | PENDING; not created/provisioned by Codex |
| Runtime enrollment | BLOCKED; actual API access-token sub UNKNOWN |
| Real private browser authentication | BLOCKED; unexecuted and unauthorized |

Actual external origin, native callback and Entra URI require operator comparison before
installation: `https://polymind.test:9443` plus `/oauth2callback`. The report's validator checks
exact native fields; runtime does not automatically compare separately mounted gateway/API/
native files. Keep SAN `DNS:polymind.test`, Windows/tunnel loopback 9443 and no public exposure.

Future secret source `/etc/polymind/secrets/streamlit.toml` must be a non-symlink regular
single-link file, UID:GID 10001:10001, mode 0600; root:10001/0710 host secret-directory traversal
is the proposed maintenance policy. Compose mounts it read-only at
`/tmp/.streamlit/secrets.toml` with `create_host_path:false`, UI UID 10001:10001. Verify exact
existing host directories and SSH alias/host key; never invent a target or weaken sudo/host-key
checks. Direct SSH stdin avoids remote plaintext staging. Transfer remains a future authorized
operator action, not a task performed now. Preserve pinned Compose/image identities.

TLS issuance/trust/custody/revocation, Windows/browser/tunnel acceptance and all other Gate A
source/provider/financial/quota/independent-permission requirements plus Gates B–E remain.
The VM is operator-reported deallocated. No activation, Entra mutation, actual login,
production authority initialization or inference is authorized. No application runtime or image
change is needed. Phase 19A COMPLETE; 19B ACTIVE; 19C NOT STARTED. Next: operator review and
independent secure preparation only.


## 27 November 2026 — Operational evidence and Gate A readiness

This addendum and the [full operational review/runbook](../codex/reports/phase_19b_operational_evidence_reconciliation_and_gate_a_readiness_review.md)
are the current evidence/next-action record. Historical sections above remain dated evidence,
not instructions to repeat completed registration/credential/PKI/trust/hosts actions. The old
noninteractive transfer in the OIDC report is **blocked** for the reported passphrase-protected
Windows key with disabled agent and unconfirmed sudo -n maintenance. Do not run it unchanged.

| Completed preparation | Current provenance and limitation |
|---|---|
| API/browser registrations, exact callback, role, delegated permission, principal-only consent, one client credential metadata | OPERATOR_REPORTED_PASS; no actual token/exchange validity |
| Operational native TOML and independent cookie | OPERATOR_REPORTED_PASS; stable cookie must survive ordinary restarts |
| GPG encrypted TOML and decrypt/byte comparison, redundant plaintext cleanup | OPERATOR_REPORTED_PASS; no Azure install/independent backup custody |
| Approved direct-root PKI/root/leaf/key matching/chain/SAN | OPERATOR_REPORTED_PASS; no deployed/browser acceptance |
| Initial CRL/signature/leaf revocation check | OPERATOR_REPORTED_PASS; no automatic distribution/browser enforcement |
| Local encrypted CA backup and source comparison | OPERATOR_REPORTED_PASS; separate offline location/passphrase custody/disaster restore PENDING |
| Current-user public CA trust, machine-wide trust absent | OPERATOR_REPORTED_PASS; trust is not inherently limited to polymind.test |
| Windows loopback hosts mapping/cache flush/resolution | OPERATOR_REPORTED_PASS; hosts backup completion not evidenced |
| Native OpenSSH/local port 9443/Tailscale and VM endpoint identification | OPERATOR_REPORTED_PASS at observation time; no fresh remote reachability |
| Dedicated SSH pair/matching public derivation/configuration | OPERATOR_REPORTED_PASS; initial wrong passphrase resolved, no replacement needed |
| Existing known_hosts | OPERATOR_REPORTED_PASS, historical TOFU only; independent VM host authenticity PENDING |

Manual deadlines independently calculated from reported certificate dates: initial CRL refresh
2026-12-02T12:49:29Z (expires 2026-12-03T12:49:29Z), leaf renewal 2027-01-25T12:43:03Z
(expires 2027-02-24T12:43:03Z), root renewal 2031-05-29T12:23:59Z
(expires 2031-11-25T12:23:59Z); client credential expires 2027-05-25T07:24:50.834Z.
These are not scheduled tasks. Operator owns renewal/revocation; explicit acceptance of absent
browser revocation protection, trust-withdrawal/compromise response and backup recovery custody
is still required. Never transfer CA key/full archive/Windows private key/signer key to Azure.

**Operational Gate A BLOCKED:** unknown API access-token sub/enrollment and owner-bound source,
source/rights/privacy/consent/review/session, current provider/capabilities, finance/shared
quota/outstanding obligations, independent execution custody, backups/risk/host authenticity
and actual acceptance remain unresolved. See the report's complete matrix, not only this
local-preparation table. Enrollment is [issuer,tenant UUID,API access-token sub]; never oid,
ID-token subject, email or a fabricated value. Standard API-before-UI ordering requires that
subject/source before first login; no supported identity-only acquisition command exists.
Next is review of a narrow separately scoped bootstrap tool, not authority initialization.
Existing execution_permissions=false/chat=null/approvals=[] can deny inference only after
legitimate configuration/source/enrollment/provider-secret/finance inputs exist.

The report contains the conditional operator-executable Gates B–E, including trusted-channel
public host-key verification; strict interactive Windows SSH; encrypted-only TOML transfer
and a fixed root maintenance receiver with no blanket sudo; exact 10001:10001/0600 private
files and protected traversal; UUID/pinned artifacts/egress/capacity; deliberate seven-authority
new-state/reuse and Redis/Chroma before initialization; private TLS/native login/negative tests;
settlement/quiesced backup/separately authorized restore/deallocation and residual costs.
Its proposed maintenance helper does not exist on Azure and is compile-reviewed only. Other
secret-custodian transfer mechanisms also need review before execution. No command was run
against Azure/Windows/SSH, no production authority initialized, no model call made.

Before requesting activation, review bootstrap scope, actual approval inputs, independent
backup custody and manual revocation risk; then seek a fresh bounded maintenance packet with
subscription/resource, UTC window, infrastructure ceiling, activation cutoff, mandatory
deallocation deadline and recovery/residual owners. Explicitly prohibit inference unless
separately authorized. Keep endpoint/user/identity paths and private topology in a protected
operator record. Preserve the existing Azure-pinned Compose, image and filesystem UUID;
do not replace them with portable tags or reformat/reset storage. VM remains reported
deallocated. Phase 19A COMPLETE; 19B ACTIVE; 19C NOT_STARTED. No new runtime/image work was done.


## 27 November 2026 — Local identity bootstrap operator handoff

The new [local runbook](phase_19_identity_bootstrap.md) prepares acquisition of the actual API
subject before production initialization, using a dedicated native WSL Streamlit UI and reused
loopback HTTPS gateway. It requires no VM activation, SSH tunnel, production Compose, source,
provider or authority. Do not use production `up --no-deps`, placeholders or initialization
workarounds. The [engineering report](../codex/reports/phase_19b_local_identity_bootstrap_utility.md)
records offline tests and current networking limits. Actual authentication remains separately
authorized future work. Preserve the original production cookie and encrypted operational custody.

Windows and WSL callback listeners must both be checked before bootstrap and before the future
Azure tunnel; they must not coexist on the browser endpoint. Export remains an unsigned candidate
requiring protected operator provenance review and separately authorized enrollment/source-owner
configuration. All existing Gate A source/privacy/review/provider/finance/quota/independent
execution, backup/revocation/remote trust/transfer and live-acceptance conditions remain.
Gates B–E and pinned staged application/Redis/Chroma artifacts are unchanged; no Azure rebuild
or transfer is needed for this local utility. Operational Gate A BLOCKED; 19B ACTIVE; 19C NOT_STARTED.
