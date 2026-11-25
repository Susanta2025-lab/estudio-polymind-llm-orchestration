# Phase 19 private VM foundation — offline operations

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
