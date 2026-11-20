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
that mount identity and fstab dependency before installation; do not enable the unit in 19B.
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
file is fatal. Credentials may be supplied only after the corresponding operator gates;
19B uses fake values exclusively in tests and never inspects existing real credentials.

The endpoint must be HTTPS with a v1 path, e.g. the **operator-approved** endpoint ending
`/openai/v1/`. The deployment alias goes in all required logical role mappings; response-model
aliases, token parameter, strict schema and usage capabilities are explicit manifest inputs.
The composition never performs model readiness GETs or paid calls as a startup probe.
Actual endpoint/authentication/model/streaming/schema compatibility needs separate 19C proof.

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
RPO/RTO remain 19C acceptance requirements.

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
independent live permission custody, semantic reviews and VM capacity remain operator/19C gates.
No Azure provisioning, live inference or public exposure is authorized.
