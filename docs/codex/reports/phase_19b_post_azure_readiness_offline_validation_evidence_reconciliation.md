# Phase 19B — Post-Azure readiness, offline validation and evidence reconciliation

24 November 2026. **Offline readiness WITH_CONDITIONS; overall Phase 19B WITH_CONDITIONS.
Production activation and acceptance remain blocked.** This is a continuation of Phase 19B,
not Phase 19C closure. The VM is **OPERATOR_REPORTED deallocated**; no Azure API, remote SSH,
identity administration, provider request, real-secret inspection, live permission issuance,
production-authority initialization, staging, commit or push occurred in this run.

## 1. Executive summary and exact scope

All three requested stages were addressed: baseline/source/evidence assessment; bounded
local verification; dated documentation, next-session preparation and reviews. Inspection
confirmed that the existing Integration Gap Resolution already implements governed scoped
Chat and Documents execution. No further runtime correction was justified. This continuation
adds 38 automated cases covering production TLS entrypoint/handshake failures and actual
seven-authority integrity/missing/damaged/partial initialization behavior. Existing interfaces,
provider-neutrality, financial semantics and local launchers remain unchanged.

The reviewed application image passed a new isolated five-service run: Documents digestion,
explicit publication, synthetic independent review, question/answer persistence, and Chat
OIDC/LangGraph/NDJSON/RAG/Redis-memory/replay. **7 mock provider calls, 0 external calls.**
All services stopped with exit 0 and dedicated projects/networks were removed. A separate
vendor-service restart retained memory and published vectors. Production/browser/semantic
acceptance is not implied by synthetic signing or reviews.

Focused regressions passed 437 cases; new verification passed 38 cases. The full offline
regression passed **3,316 tests, 158 warnings, zero failures/errors/skips in 1,198.92 s**
(exit 0). Historical 3,278-test evidence is retained
separately and is never counted as a new run. No runtime/packaging change requires a rebuild;
135 current runtime Python files match the reviewed image byte for byte.

## 2. Starting repository/Git baseline

Executed before repository edits:

```bash
git status --short --branch
git rev-parse HEAD
git log --oneline -5
git diff --stat
git diff --check
git diff --cached --stat
```

HEAD exactly matched `7bf82dc2da4a9f29561a5f493b690502c0090eb0`, on
`master...origin/master`. Last five commits: `7bf82dc`, `b48dde4`, `d7d2ec2`, `6aedae3`,
`f7d091a`. Index empty; whitespace check exit 0. Initial tracked diff: **4 files changed,
158 insertions(+), 8 deletions(-)**. Initial state matched the operator's reported inventory:

```text
 M README.md
 M docs/evaluation/phase_19_deployment_architecture.md
 M docs/evaluation/phase_19_implementation_plan.md
 M docs/operations/phase_19_vm.md
?? docs/codex/prompts/phase_19b_live_deployment_readiness_continuation.md
?? docs/codex/prompts/phase_19b_post_vm_creation_verification.md
?? docs/codex/prompts/phase_19b_ssh_bootstrap_repair_and_revalidation.md
?? docs/codex/reports/phase_19b_live_deployment_readiness_continuation.md
?? docs/codex/reports/phase_19b_post_vm_creation_verification.md
?? docs/codex/reports/phase_19b_ssh_bootstrap_repair_and_revalidation.md
```

All ten pre-existing changed/untracked files were copied and SHA256-recorded before editing
in `/tmp/polymind-postazure-20261124-jl88xo16/baseline/` and `baseline.json`; the original
tracked diff and status were also saved. No branch/history/index/remote operation occurred.
Existing historical prompts/reports remain byte-identical. Architecture, plan and VM guide
retain their full starting content as prefixes with dated appendices. README retains its
historical status narrative; current heading/roadmap/milestone are explicitly updated to
supersede old undeployed-state claims. No pre-existing implementation change was present
or discarded. No historical authority was opened or mutated.

## 3. Sources and evidence provenance

Primary repository sources: root AGENTS; Phase 19A readiness prompt/report; Phase 19B offline
prompt/report including **Integration Gap Resolution**; the three existing continuation
prompt/report pairs; deployment architecture/plan/VM guide; Compose, Dockerfile, Dockerignore;
actual deployment/storage/backup, OIDC/security/execution, governance/admission, provider,
Chat/UI/API and document/operator/pilot/publication code and tests. Existing test fixtures
and the preserved five-service harness were inspected before reuse. Entra and local-launcher
contracts were consulted from repository documentation and implementation.

Evidence classes used throughout:

- **Historical repository execution:** dated results in retained reports. The original 19B
  Chat/Documents GAPs are superseded only by the later executed Integration Gap Resolution,
  whose final full regression was 3,278 passed/one warning. Earlier overlapping counts remain
  historical, not independent totals.
- **Historical Codex Azure execution:** earlier post-provisioning and SSH-repair reports record
  their own authorized control-plane/Run Command observations and expired cutoffs. This run
  did not repeat those commands.
- **Operator-reported later Azure execution:** the present master prompt supplies completed
  private access, storage/reboot, Docker/image/Compose/model checks and deallocation. Older
  reports end before these events; no later local terminal transcript was supplied as a
  durable source. Preserve the reported scope without inventing independent verification,
  transfer-archive hashes, new timestamps or a fresh power-state query.
- **New local execution:** isolated offline pytest, cached-image topology/recovery/audit and
  parser/systemd/compilation checks described below. Raw logs/JUnit/result metadata stay
  under the unique temporary root above; durable commands/results are recorded here.

No external price/model/identity discovery was needed or performed. Historical cost tables
remain dated estimates; no new tariff, applicable quotation or bill reconciliation is claimed.

## 4. Verified Azure infrastructure outcomes

**PASS, operator-reported infrastructure foundation:** `rg-epolymind`, `vm-epolymind-dev`,
Spain Central, Ubuntu 24.04 LTS, Standard_D2s_v4, 2 vCPU/8 GiB, 64-GiB OS plus 64-GiB data
disk, no VM public IP, private Tailscale/OpenSSH, existing private VNet/subnet/restrictive NSG/
NAT. Earlier reports independently recorded provisioning/private Azure configuration and
SSH repair in their own sessions; later operator evidence closes actual private login and
reconnect within its stated scope. Tailnet policy and complete guest outbound enforcement
are not independently re-audited here.

The original SSH/cloud-init ordering failure remains **historical FAIL**. The authorized
repair and later reported reboot success establish later readiness, not retroactive successful
first boot. This task creates no infrastructure or alternate provisioning framework. Actual
current resource/permission/power/charge inventory must be revalidated under a new session.

## 5. Persistent storage and reboot evidence

**PASS, operator reported:** dedicated ext4 filesystem UUID
`c95e5fce-443b-4d90-9160-8b67758f12d9` at `/srv/polymind`, UUID-based fstab validation and
automatic remount after Azure reboot. Reported directory owners/modes: operator 10001:10001,
Redis 999:999, Chroma 10001:10001, all 0700; operator/private/objects/sources restrictive.
SSH, tailscaled and Docker services were active after reboot and private reconnect succeeded.

Device letters changed during lifecycle operations. UUID/managed-disk identity is authoritative;
**do not format, repartition or initialize that disk again**. New authority initialization is
a distinct operation, permitted only against an approved new empty authority set. Infrastructure
reboot evidence contains no application-authority, publication, financial or provider-recovery
proof because production services/authorities were never started/initialized.

## 6. Docker image provenance and transfer evidence

Operator reports successful secure transfer/import of `polymind:phase19-reviewed` on Azure,
linux/amd64, UID:GID 10001:10001, image identity:

```text
sha256:9f386acf8bddcb5d01bb028151caae24b5df604f8a56c00b7b39c7e0f8298c02
org.opencontainers.image.revision=7bf82dc2da4a9f29561a5f493b690502c0090eb0
```

New local `docker image inspect` independently confirms that exact identity, platform, user,
revision label and **3,042,749,277 bytes**. A read-only, network-disabled image audit compared
**135 runtime Python files** in api/config/deployment-phase19/documents/governance/graph/llm/
memory/rag/security/tools/ui: all byte-identical to the current working tree. The audit found
no `/app/.env`, test suite or `.pem`/`.key`/`.sqlite`/`.db` files. It is a scoped source/content
audit, not a certification of every historical image layer or reproducible dependency build.

No Docker build, pull, dependency change or model download was needed. Only tests and
Markdown change; both are excluded from this image by Dockerignore. Existing image evidence
therefore still applies to this runtime. Any later relevant runtime/dependency/Dockerfile/
model-packaging edit requires rebuild, new provenance verification and authorized transfer;
never infer that the existing Azure image contains later edits. Transfer checksums beyond
the reported matching image identity are not invented. A local image ID and a registry
manifest digest are distinct identifiers.

## 7. Digest-pinned Compose/security evidence

Operator-reported Azure images:

```text
redis@sha256:7f7d30b7fdd09467bac58198a1f166dd69789d348d4fe859cccb20e0cf287fbe
chromadb/chroma@sha256:1e0b73a187a28757c572acba508c46f48c9e8b0acaf5c20e6d95cdedce1acdf6
```

The root-owned `/opt/polymind/docker-compose.phase19.yml` and `compose.env.example` are
Azure-staged artifacts. Their pinned version passed reported syntax/security checks; API/UI/
gateway share the reviewed app image. **Tracked Compose remains unchanged**, with portable
vendor tags Redis 7.4-alpine/Chroma 1.5.9. No staged-file bytes/hash were independently
retrieved here. Local cached Redis identity/RepoDigest is
`sha256:ff02b58f971e7d7d156a1267e283fcbbeee91773b6aa36c49dac28ecfe28eadf`, not the reported
Azure Redis reference; the manifest/platform relationship is **UNKNOWN**. Chroma identity
matches the supplied reference. The local topology validates its observed cached vendor
images, not byte-equivalence of a different Azure Redis image.

Source and new tests confirm five services, explicit non-root users, read-only roots,
capability drop, no-new-privileges, bounded tmpfs/logging/restarts/resources/shutdown, fail-closed
bind mounts, internal backend/frontend, and only gateway host `127.0.0.1:9443`. API/UI retain
an egress network in production; that is not a destination allowlist. Reported Azure security
preflight is configuration-level PASS. No running production service, live TLS/login or
complete outbound-policy enforcement follows. Local test overlays remove all ports and
egress; no unrelated Docker resource was touched or pruned.

## 8. Azure offline model-execution evidence

**PASS, operator reported:** NON_ROOT_EXECUTION_PASS, PHASE19_IMPORTS_PASS,
AZURE_EMBEDDING_PASS, AZURE_RERANKER_PASS and PHASE19_AZURE_OFFLINE_RUNTIME_PASS. The image's
baked embedding/reranking models executed on Azure without container networking, as they
had locally. A nonfatal Transformers cache_dir deprecation warning is retained as a warning,
not a failed inference or production application test. No generative real-model request
was authorized or performed. New local topology also uses real MiniLM/cross-encoder artifacts;
that does not qualify sustained Azure five-service capacity.

## 9. Real Entra/OIDC readiness

**Offline PASS; real browser authentication BLOCKED.** Existing `security/identity.py` enforces
single canonical tenant/API UUIDs, exact tenant v2 issuer/JWKS, scalar API audience, RS256/key
validation, delegated access_as_user, exact PolyMind.L1Operator role, time/type checks and
no token-selected trust URL/profile. Missing/bad configuration, ID/Graph/app tokens, wrong
issuer/audience/tenant/role/scope/signature/expiry fail closed. APIs reverify identity/security;
workflow enrollment is exact issuer/tenant/access-token-subject. Email/oid/browser fields
cannot select owner. Existing security tests cover inactive/revoked state and scoped denial.

Native Streamlit forwards `st.user.tokens['access']`; Chat and Documents retain independent
execution resources/scopes, owner/tenant memory/canonical retrieval and token/session clearing.
Reauthentication only reauthorizes reads; it does not extend approvals/budgets or grant calls.
Focused tests include actual signed local JWT verification and no unauthenticated/foreign
principal execution, with isolated state and mocked provider HTTP. No real Entra endpoint,
consent, registration or browser login was used.

Exact non-secret operator decisions are tabulated in the [VM runbook](../../operations/phase_19_vm.md#operator-supplied-non-secret-configuration-decisions): tenant and API/client registration
IDs, tenant issuer/JWKS/discovery, API Application ID URI/delegated scope, v2 issuance and role
assignment/consent, enrolled access-token sub, exact origin/callback and native token exposure.
The API audience is the API UUID, not its scope URI or browser client UUID. Real cookie,
logout/expiry, token forwarding and browser callbacks remain live acceptance requirements.

## 10. Private HTTPS readiness

**Offline PASS; production private HTTPS BLOCKED.** Production entrypoint requires explicit
non-loopback HTTPS origin without path/query/fragment/userinfo; TLS minimum 1.2; private,
owned, regular, non-symlink certificate/key files; load failure occurs before listener startup.
Gateway uses exact Host/Origin checks, rejects foreign auth origins, requires WebSocket Origin,
strips incoming Forwarded/X-Forwarded headers and forwards to UI only. API/admin/DB ports
are not gateway upstreams or host-published endpoints.

New tests execute the real production TLS context creation using temporary test certificates,
then a bounded loopback client/server handshake with certificate and SAN hostname verification
and TLS 1.2/1.3. Missing/invalid cert/key, unsafe file modes/symlink and unsafe origin fail
before listener startup. Existing HTTP/WebSocket tests verify allow/deny/cookie/forwarding
contracts. Synthetic test trust is explicitly scoped and never installed as browser trust or
written to production paths.

Operator must select a private name and browser-visible port, SAN/valid chain/trust/renewal
custody, exact `<origin>/oauth2callback`, native registration and a loopback-reaching SSH
tunnel. VPN/Tailscale routing to the private VM IP alone cannot reach its host loopback.
No production name, certificate or trust decision is invented. Real browser trust and native
Entra callback remain blocked despite local handshake success.

## 11. Provider, governance and independent permission readiness

**Offline PASS; real compatibility/finance/permission BLOCKED.** Current Settings/factory/runtime
use provider-neutral infrastructure, explicit HTTPS v1 adapter path and mounted credential,
logical deployment-role mapping, selected api-key/Bearer header, no inline/file ambiguity,
private bounded files, usage-reporting and strict managed schema profiles. The validator
accepts generic HTTPS paths ending `/v1`; it does **not** enforce literal `/openai/v1/` or
verify a Foundry endpoint. That candidate dispatch path and actual capabilities require
operator evidence and separately authorized live verification. No startup model probe or
provider credential alone grants dispatch. No managed-identity/token renewal is implemented.

Retained bounded HTTP/SSE tests cover model/schema/envelope/usage, timeout, malformed/truncated
responses, 429 and cleanup. SSE remains inside inference infrastructure → provider-neutral
tokens → PolyMind NDJSON. Chat and Documents share governance/admission, reservations,
settlement, idempotency and UNKNOWN; missing usage/uncertainty prevents automatic retry.
Version-1 zero-paid approvals remain immutable and cannot satisfy the version-2 bridge.
Independent signed permissions bind principal/tenant/source/resource/configuration/models/
financial policies/catalog/admission/path/scope/time/call bounds; consumption is durable in
actions.sqlite. Read-only live trust is separate from writable authorities and test-purpose
signatures cannot satisfy it. Focused tests exercise denial before provider effects,
post-admission revalidation, exhaustion, revocation, reopen, duplicate transport replay and
financial/admission rejection without modifying policy or historical signatures.

Pending: exact approved endpoint/model/deployment/version/type/processing region, aliases,
structured/streaming/usage capabilities, credential custody, source/data terms, applicable
tariff/currency/catalog, owner/tenant budget, assigned/shared quotas and consumer coordination,
existing-obligation reconciliation and fresh independent live permission/window. Historical
Phase 17H prices/approvals or infrastructure expenditure grant none of these.

## 12. SQLite authority lifecycle readiness

**Synthetic PASS; production initialization NOT_PERFORMED.** Exact set:

| Authority | Construction/dependency and durable meaning |
|---|---|
| security.sqlite | SecurityRuntime first; verified principal/resource/grant/revocation/audit truth |
| governance.sqlite | Reviewed owner/tenant policy/catalog, reservations/settlement/UNKNOWN |
| admission.sqlite | Reviewed shared provider key/policy; RPM/TPM/active dispatch authority |
| jobs.sqlite | Canonical object store and job settings; attempts/fences/checkpoints/outbox |
| publication.sqlite | Jobs/objects, available real vector adapter and retrieval encoder |
| pilot.sqlite | Bound source/profile/model/path/financial configuration, approvals/intents/results/reviews |
| actions.sqlite | Explicit lifecycle, operator action/accepted replay and durable permission consumption |

All live authority paths remain `/state/private/<name>`; canonical objects remain
`/state/private/objects`. Preflight checks complete set, private paths, schema version and
SQLite quick_check; constructors enforce actual schema/configuration compatibility. The
`check` CLI covers preflight/config only, not the full manifest/source/secret/trust/browser/
readiness contract. Serve does not initialize a missing DB; initialization refuses any
existing authority, including a partial set. POSIX flock uses a persistent inode shared by
API/maintenance. There remains exactly one Uvicorn process and owned runner.

New tests construct the actual external runtime with isolated fake credentials/adapters,
check all seven private files/version/integrity/schema presence, reject missing/truncated
each authority and reject partial initialization with each surviving DB. Existing tests
cover unsafe paths, permissions, stable marker, second writer, complete reopen, accepted
results/consumed permissions and UNKNOWN persistence. Nothing is pointed at production.

Future dependency order is in Gate C of the runbook: freeze inputs/custody → verify existing
UUID mount/owners and approved new state → marker/config/manifest/source hashes/objects →
Redis/Chroma/model availability → explicit one-time initialize under lock → verify complete
schema/integrity → single serve. A failure after early constructors may leave partial state;
retain it as an incident, never delete/reinitialize to pass. Missing real inputs remain blocked.

## 13. Local five-service integration results

The existing harness was reused once against the reviewed image, no new framework or build:

```bash
python scripts/phase19_offline_validation.py \
 --root /tmp/polymind-postazure-20261124-jl88xo16/five-service \
 --image sha256:9f386acf8bddcb5d01bb028151caae24b5df604f8a56c00b7b39c7e0f8298c02 \
 --integration-tests
```

**Exit 0**, 79.609 s including preparation/workflow/stop/cleanup; five services healthy in
**45.899 s**. Project `polymind19b-offline-f16eb196` had internal-only networks, no published
ports or egress, read-only mounted test code, new synthetic state and ephemeral test-purpose
identity/permission material. The real production assembly used test-only clock/retrieval/
permission composition plus in-process MockHTTP; Redis/Chroma and baked encoders/reranker
were real. No actual provider credential or external inference route was present.

Result: START_DIGEST_PUBLICATION_QA_PASS and OIDC_QUERY_NDJSON_RAG_MEMORY_PASS;
**7 provider_calls (all mocks), external_calls=0**, canonical Chroma publication, Redis history,
accepted-answer storage and transport replay without extra calls. Synthetic attached reviews
only exercise review gates; they are not independent human quality findings. UI was headless;
no native browser/real Entra acceptance is claimed. All five containers exited 0; cleanup
removed only that project. Test data remains in its unique private temporary tree.

## 14. Persistence, security and failure/recovery results

Focused and new lifecycle tests verify signed identity/permission denial, owner/tenant/source
bindings, stale/revoked/expired permission, exact scopes, no zero-paid conversion, missing
configuration/credentials/capabilities, missing/unsafe/truncated state, partial initialization,
persistent lock/second writer and conservative UNKNOWN/idempotency/reopen behavior. Existing
backup tests execute stopped-writer assertion, ownership exclusion, whole-tree SHA256 copy,
new isolated restore, tamper rejection and preservation of an UNKNOWN evidence value.
They are synthetic single-host tests, not Azure disaster recovery or hostile-custodian proof.

A bounded follow-up started **only the prior test Redis/Chroma directories** under a new
internal project (`polymind19b-recovery-*`), without API/provider. Redis retained **1 key**;
Chroma retained **1 collection/2 records**. Protocol readiness and data checks passed;
controlled vendor stop took **0.539 s**, entire probe **8.741 s**, then project cleanup.
No inference was replayed. A subsequent network-disabled, read-only SQLite inspection of the
completed topology state confirmed all seven integrity_check results `ok` and exactly seven
SETTLED reservations, with zero unsettled/UNKNOWN rows. Its operator tree contained 580,337
logical file bytes; this is a final observation, not a measured growth rate or capacity bound.
Accepted-answer/permission/full-runtime reopen are covered by
existing test_phase19_execution_bridge tests; the integration fixture's startup itself is
one-shot and was not falsely presented as a full API-container restart test.

Configuration-only missing-bind/mount safety is inspected and tested in source; actual Azure
missing-mount startup, application reboot, off-disk snapshot, isolated Azure restore, rollback,
full-disk/host-loss behavior and RPO/RTO remain **GAP/BLOCKED**, not inferred from local vendor
restart. The unit's mount syntax passes; it was never installed/enabled. Complete destination
allowlist enforcement is **UNKNOWN** beyond the supplied configuration evidence. No state
was silently repaired, reset, renamed, deleted or replayed to clear a failure.

## 15. Resource measurements and limitations

New topology observations (three five-service samples, approximately eight-second spacing):

| Measurement | New local result |
|---|---:|
| Healthy startup | 45.899 s |
| First aggregate memory sample | 545.820 MiB |
| Highest sampled aggregate memory | 609.593 MiB |
| Highest sampled aggregate Docker CPU | 19.77% (100% = one logical core) |
| Highest API / UI sampled memory | 508.0 / 48.34 MiB |
| Highest gateway / Redis / Chroma sampled memory | 26.41 / 7.543 / 19.46 MiB |
| App / local Redis / Chroma logical image bytes | 3,042,749,277 / 57,337,242 / 826,133,216 |
| Controlled vendor stop | 0.539 s |

These are observed samples, not peaks or capacity limits. Full pytest was also running on
the local host; the host is not the Azure VM. Docker memory excludes some OS/kernel/cache
costs. Model loading is included in startup but no separate new encoder-only timing was
measured. Earlier 40.296/40.504-s startup, 8.428-s model load and ~585-MiB sample remain
historical observations; the new values do not invalidate them. Image bytes are not RAM;
shared application layers are not counted three times.

The actual Azure host is 2 vCPU/8 GiB with separate 64-GiB OS/data disks. Isolated Azure
embedding/reranker success and this tiny synthetic workload do not establish sustained
five-service capacity, realistic concurrent browser load, corpus/vector growth, disk latency,
backup headroom or recovery time. No VM resize is justified or performed. Billing, NAT data,
retained disks/PIP charges and current applicable prices remain unverified in this run.

## 16. Implementation changes and rationale

No production runtime defect was demonstrated, so no runtime/interface/schema/policy/provider/
dependency/Dockerfile/Compose source was changed. Reused the completed Chat/permission bridge,
provider-neutral adapters, financial ledgers, lifecycle/backup and topology harness.

New files:

- `tests/unit/test_phase19_tls.py`: 16 cases for actual TLS context/hostname-verified handshake,
  missing/invalid/unsafe cert/key and production origin refusal.
- `tests/integration/test_phase19_authority_lifecycle.py`: 22 actual-runtime cases: complete
  private integrity set, 14 missing/truncated checks and seven partial-initialization refusals.
- This report and its [clean instruction copy](../prompts/phase_19b_post_azure_readiness_offline_validation_evidence_reconciliation.md).

Updated existing README, architecture, plan and VM guide with dated supersession/provenance,
current non-activation state, exact non-secret inputs and dependency-ordered Gates A–E.
Six pre-existing historical untracked prompts/reports remain untouched. No live approval,
credential, generated state, archive, test certificate or runtime log enters the repository.

## 17. Exact regression results and warnings

Commands used the existing Python environment with a whitelist of execution environment
variables (PATH/HOME/locale/interpreter libraries), HF_HUB_OFFLINE=1,
TRANSFORMERS_OFFLINE=1, PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=1 and
TOKENIZERS_PARALLELISM=false. Repository test configuration suppresses implicit dotenv;
no real secret was read to configure tests. New pytest state and JUnit outputs use the unique
temporary root. Counts overlap with the full suite and must not be summed.

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
 tests/unit/test_phase19_deployment.py tests/integration/test_phase19_operator.py \
 tests/integration/test_phase19_execution_bridge.py tests/integration/test_document_operator.py \
 tests/unit/test_structured_provider.py tests/unit/test_security_entra.py \
 tests/unit/test_security_identity.py tests/unit/test_security_api.py \
 tests/unit/test_phase19_bounded_stream.py tests/unit/test_phase19_chat_view.py \
 tests/unit/test_documents_view.py tests/unit/test_ui_api_client.py tests/unit/test_local_apps.py \
 tests/unit/test_openai_compatible_provider.py tests/unit/test_governance.py \
 --junitxml=/tmp/polymind-postazure-20261124-jl88xo16/focused.xml \
 --basetemp=/tmp/polymind-postazure-20261124-jl88xo16/focused-state

HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
 tests/unit/test_phase19_tls.py tests/integration/test_phase19_authority_lifecycle.py \
 --junitxml=/tmp/polymind-postazure-20261124-jl88xo16/tls.xml \
 --basetemp=/tmp/polymind-postazure-20261124-jl88xo16/tls-state

HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
 --junitxml=/tmp/polymind-postazure-20261124-jl88xo16/full.xml \
 --basetemp=/tmp/polymind-postazure-20261124-jl88xo16/full-state
```

| Check | Executed result |
|---|---|
| Existing focused suite | Exit 0; **437 passed, 1 warning in 171.44 s** |
| New TLS/actual-authority tests | Exit 0; **38 passed in 19.89 s**, no warnings |
| Full offline regression | Exit 0; **3,316 passed, 158 warnings in 1,198.92 s**, no failures/errors/skips |
| All three Compose parsers | Exit 0 each, inert/empty env files |
| systemd-analyze verify | Exit 0, no install/enable |
| External-cache compileall | Exit 0 |
| make dry-run for five local launcher targets | Exit 0; launcher commands preserved |
| Image audit / topology / vendor recovery | Exit 0 each; results above |
| Git/new-file whitespace and local-link review | Final results in section 19 |

Exact additional successful commands (the generated helpers remain only in the temporary
evidence directory):

```bash
python /tmp/polymind-postazure-20261124-jl88xo16/vendor_recovery.py
python /tmp/polymind-postazure-20261124-jl88xo16/static_checks.py
python /tmp/polymind-postazure-20261124-jl88xo16/review.py
```

```bash
docker compose --env-file /dev/null -f docker-compose.yml config --quiet
DOCUMENT_DEMO_ROOT=/tmp/polymind-postazure-20261124-jl88xo16/inert-parser-path \
 docker compose --env-file /dev/null -f docker-compose.documents.yml config --quiet
docker compose --env-file deployment/phase19/compose.env.example -f docker-compose.phase19.yml config --quiet
systemd-analyze verify deployment/phase19/polymind.service
PYTHONPYCACHEPREFIX=/tmp/polymind-postazure-20261124-jl88xo16/final-bytecode python -m compileall -q .
make -n chat-api chat-ui chat-dev docs-init docs-serve
git diff --check
```

The focused warning is the existing aiohttp NotAppKeyWarning at ui/tls_gateway.py:18.
The full run reports 158 warnings: 156 pytest advisories because existing record_property
tests are incompatible with the requested default xunit2 JUnit format, plus two occurrences
of the existing aiohttp AppKey advisory. JUnit still records 3,316 tests with zero failures,
errors or skips. The historical one-warning run did not use this JUnit invocation; its
warning count is not rewritten or presented as the new outcome. No warning was suppressed
and no repository test configuration was changed to reduce the count. No configured
lint/type formatter was found;
none installed. No Docker build duplicated unchanged runtime/image inputs. Azure/real Entra/
production TLS/live provider/cloud disaster recovery checks were not executed because
production inputs and independent authorization are absent.

Intermediate failures are preserved: the first sandbox focused attempt reached 19 passes
and two gateway socket failures, then stalled in thread/HTTP work; interrupted with exit 130
and excluded from successful totals. The execution-approved offline rerun above passed.
Sandbox Docker socket inspection was denied before daemon access and retried through execution
approval. Initial image-audit mount exposed a deliberate 0700 temporary directory to UID
10001 and failed Permission denied (exit 2); individual read-only non-secret file mounts
fixed the test setup without weakening directory modes, and all 135 comparisons passed.
New-file review also caught Markdown hard-break trailing spaces in the normalized prompt;
they were removed. No application assertion required a production correction, test suppression
or policy change.

## 18. Implementation self-review findings

Reviewed production composition/consumers, tests, entire tracked diff and new files. Confirmed
provider details stay inside configuration/inference infrastructure; seven distinct authorities,
one persistent lock/runner, existing financial reservation/settlement/UNKNOWN, source/tenant/
owner and permission review boundaries remain. New tests use actual checks and unique fixtures;
they do not mirror a mocked implementation or bypass signature validation. Existing launchers,
API contracts and frozen historical provider/approval source inventories are unchanged.

Documentation review corrected the misleading possible assumptions that the generic v1
validator mandates Foundry's literal path; that the Azure-staged Compose is the tracked file;
that local Redis matches the different Azure digest; that `check` is full runtime validation;
that reported disk/service reboot means application recovery; or that the old cloud window
survives deallocation. Real browser, provider, quality, capacity, outbound and DR gaps remain
explicit. No broad redesign, abstraction or dependency was needed.

## 19. Separate pre-commit review findings

Separate review passed after correcting one report-to-prompt relative link and the new
prompt's Markdown trailing spaces. The final scanner checked **14 candidate files and 106
local Markdown links**, including explicit section anchors: zero broken links and zero
secret-payload pattern findings. Strict Git whitespace checks on all four newly created
files and tracked diff passed. A preliminary review helper incorrectly treated git
diff --no-index --check exit 1 (ordinary file difference with no diagnostics) as a whitespace
failure; accepting its documented difference status while requiring empty diagnostics
resolved that checker issue. All six historical prompt/report hashes match; three existing
architecture/plan/operations files retain their full baseline prefix, and README's dated
status supersession was manually reviewed. HEAD is unchanged and the index is empty.

Review scope is all four modified tracked Markdown files, six pre-existing historical
untracked documents, the new prompt/report and two tests. No index content exists. Generated
keys/certificates/JWTs/DBs/logs/archives remain outside Git in private temporary test state.
The newly added test key-generation code produces ephemeral TLS material only; no secret bytes are in
the test source. Documented /state, /srv, /etc, /opt and unique /tmp paths are operational/
evidence references, not machine-specific application defaults. Public fingerprints/digests/
resource identifiers in historical documents are intentional evidence, not credentials.
No real env file, binary, dependency, debug route, stale TODO or unrelated runtime change
was introduced. Pattern scans supplement manual review and are not universal leak proof.

## 20. Remaining blockers, approvals and next-session plan

[VM runbook Gates A–E](../../operations/phase_19_vm.md#next-authorized-session--gates-ae)
are executable future steps, not new authority:

1. **A:** Freeze exact non-secret Entra API/browser/enrollment, private origin/SAN/trust/callback/
   tunnel, approved source/consents/reviews, provider/capabilities/custody, tariff/budget/shared
   quota/reconciled obligations. Independent custodian supplies live permission only for an
   approved exact model plan; an execution-disabled startup must remain denied.
2. **B:** Obtain fresh Azure resource/cost/window authorization and cutoff/deallocation owners;
   confirm actual current state, private route/host/outbound policy, UUID mount/owners, exact
   image and staged pinned Compose/vendor identities. Do not reformat/redeploy to simplify it.
3. **C:** Provision private reviewed files with correct modes/owners, source hashes/bindings and
   independently managed trust. Start data dependencies; explicitly initialize only the new
   approved empty authority set once, preserving any partial or prior state for reconciliation.
4. **D:** Start exactly one API/runner, UI/gateway after protocol readiness; authorized real
   Entra/private TLS/denial/workflow testing and actual capacity observations. No inference
   until separate A3–A5 data/provider/financial/live execution gates are complete.
5. **E:** Quiesce, preserve UNKNOWN/obligations, controlled restart and authorized backup/isolated
   restore/current-truth reconciliation; record resources/costs; deallocate and independently
   verify power state, retained-resource charges and owners.

No new credentials are requested by this task. Phase 19C implementation/closure remains
**NO** until outstanding Phase 19B runtime/live/recovery/independent acceptance is resolved.
Existing Phase 17/18 deferred human/external acceptance obligations are not satisfied here.

## 21. Final readiness and evidence reconciliation matrix

PASS is always limited to the stated source/scope. BLOCKED means independent external input
or authorization is absent; UNKNOWN means evidence missing, never permission to infer success.

| Requirement | Repository/historical offline evidence | Operator-reported Azure evidence | Newly verified local evidence | Verdict / outstanding action |
|---|---|---|---|---|
| Azure VM foundation | Existing five-service/single-host architecture | Private Spain Central D2s_v4 foundation | Source/provenance reconciliation, no cloud rerun | **PASS** foundation only; new window before activation |
| Private SSH/Tailscale | Earlier repair report; original first boot FAIL retained | Actual login/reconnect and services after reboot | Historical files preserved | **PASS** reported access; revalidate next session |
| ext4/reboot | Mount-aware unit/storage checks | UUID/fstab/remount and owner/modes passed | Synthetic lifecycle/lock checks | **PASS** infrastructure, never reformat |
| Docker Engine/Compose | Existing deployment/harness | 29.10.0/v5.8.0 installed | Local parser/runtime checks | **PASS** reported Azure installation |
| Application image | Committed 7bf82dc runtime | Exact image imported/verified | ID/label/user/platform and 135 matching files | **PASS** unchanged runtime |
| Redis/Chroma identity | Tracked portable tags | Supplied pinned identities | Local identity inspected; Redis differs | **PASS** Azure reported identity; equivalence UNKNOWN |
| Compose security | Hardened source/tests | Pinned syntax/security preflight | Parser, topology isolation, clean stop | **PASS** configuration; outbound enforcement UNKNOWN |
| Azure offline retrieval models | Baked CPU artifacts | Embedding/reranker PASS | Real encoders in topology | **PASS** reported isolated Azure runtime |
| Real Entra authentication | Complete scoped offline implementation | Production inputs absent | Signed JWT/API/UI denial tests | **BLOCKED** registration/consent/enrollment/browser proof |
| Production private HTTPS | Exact gateway/protocol/file contracts | Loopback config only; no real TLS files | Host/Origin/WS plus new trusted-test handshake | **BLOCKED** real name/cert/trust/callback/browser |
| Real provider configuration | HTTPS v1/header/file/model/schema contracts | No production provider credential/config | Mock HTTP/error/usage tests | **BLOCKED** exact approved deployment/capabilities/custody |
| Governance pricing/admission | Shared policies/ledgers/idempotency/UNKNOWN | Approved real inputs absent | Fake finance/admission/replay tests | **BLOCKED** approved catalog/budgets/quota/consumer truth |
| Independent permission | v1/v2 separation and signed bound grants | No live trust/permission supplied | Test-purpose denial/revocation/reopen/consumption | **BLOCKED** independent live authority/window |
| Production SQLite initialization | Explicit new-init versus complete serve | Seven authorities not initialized | Real seven-DB synthetic lifecycle | **BLOCKED** reviewed private inputs/new-set authorization |
| Local five-service integration | Historical resolved integration | No production stack started | 7 fake/0 external calls; real data/retrieval services | **PASS** synthetic only |
| Azure five-service acceptance | Locally verified composition | Not performed | Local topology is not Azure acceptance | **BLOCKED** configuration/lifecycle/live acceptance |
| Azure backup/disaster recovery | Synthetic whole-tree backup/restore | Not performed | Unit restore/integrity and vendor restart | **BLOCKED** off-disk/current-truth/cloud recovery/RPO/RTO |
| Offline regression | Historical 3,278 passes retained | Not a cloud requirement | 3,316 passed, 158 documented warnings, zero failures/errors/skips | **PASS** |
| Documentation/reconciliation | Prior history preserved | Scope accurately labelled | Dated report/runbook/status | **PASS** bounded provenance |
| Pre-commit readiness | No Git writes authorized | No remote actions | 14 files/106 links; no payload/whitespace/link findings | **PASS** |

Acceptance gates: **1 baseline preservation PASS; 2 offline configuration contracts PASS;
3 synthetic integration/recovery PASS within the documented local scope; 4 regression PASS;
5 documentation integrity PASS; 6 Git readiness PASS.** Gate 3 does not promote untested
Azure mount/application reboot/disaster recovery, full destination firewall or sustained
capacity requirements; these remain explicitly GAP/UNKNOWN/BLOCKED above. None of these
six local acceptance gates grants activation or completes overall Phase 19B.

## 22. Git status and operator handoff

Final `git status --short --branch`:

```text
## master...origin/master
 M README.md
 M docs/evaluation/phase_19_deployment_architecture.md
 M docs/evaluation/phase_19_implementation_plan.md
 M docs/operations/phase_19_vm.md
?? docs/codex/prompts/phase_19b_live_deployment_readiness_continuation.md
?? docs/codex/prompts/phase_19b_post_azure_readiness_offline_validation_evidence_reconciliation.md
?? docs/codex/prompts/phase_19b_post_vm_creation_verification.md
?? docs/codex/prompts/phase_19b_ssh_bootstrap_repair_and_revalidation.md
?? docs/codex/reports/phase_19b_live_deployment_readiness_continuation.md
?? docs/codex/reports/phase_19b_post_azure_readiness_offline_validation_evidence_reconciliation.md
?? docs/codex/reports/phase_19b_post_vm_creation_verification.md
?? docs/codex/reports/phase_19b_ssh_bootstrap_repair_and_revalidation.md
?? tests/integration/test_phase19_authority_lifecycle.py
?? tests/unit/test_phase19_tls.py
```

Final `git diff --stat` (tracked changes only):

```text
 README.md                                          |  46 +++-
 .../evaluation/phase_19_deployment_architecture.md |  49 +++++
 docs/evaluation/phase_19_implementation_plan.md    |  52 +++++
 docs/operations/phase_19_vm.md                     | 236 ++++++++++++++++++++-
 4 files changed, 375 insertions(+), 8 deletions(-)
```

There are **4 modified tracked files and 10 untracked files**, nothing staged: six of
the untracked historical documents pre-date this run and four files are newly created.
`git diff --name-status` contains only the four requested documentation paths; the index
diff is empty. `git diff --check` and separate new-file whitespace/link/payload checks
passed. No validation container remains running, and no image rebuild/transfer is pending
for this tests/documentation-only continuation. The source HEAD is still `7bf82dc`.


Proposed checkpoint message:

```text
docs: reconcile Phase 19B Azure evidence and verify offline readiness
```

Candidate checkpoint files (operator review only; **do not stage/commit automatically**):

- `README.md`
- `docs/evaluation/phase_19_deployment_architecture.md`
- `docs/evaluation/phase_19_implementation_plan.md`
- `docs/operations/phase_19_vm.md`
- `docs/codex/prompts/phase_19b_live_deployment_readiness_continuation.md`
- `docs/codex/prompts/phase_19b_post_vm_creation_verification.md`
- `docs/codex/prompts/phase_19b_ssh_bootstrap_repair_and_revalidation.md`
- `docs/codex/prompts/phase_19b_post_azure_readiness_offline_validation_evidence_reconciliation.md`
- `docs/codex/reports/phase_19b_live_deployment_readiness_continuation.md`
- `docs/codex/reports/phase_19b_post_vm_creation_verification.md`
- `docs/codex/reports/phase_19b_ssh_bootstrap_repair_and_revalidation.md`
- `docs/codex/reports/phase_19b_post_azure_readiness_offline_validation_evidence_reconciliation.md`
- `tests/unit/test_phase19_tls.py`
- `tests/integration/test_phase19_authority_lifecycle.py`

This includes six historical documents that were already untracked on entry and are now
reviewed unchanged. It excludes all temporary execution evidence/state and existing ignored
runtime files. No commit or push occurred. Stop for operator review; no next phase began.

```text
PHASE19_POST_AZURE_BASELINE_VERIFIED: YES
AZURE_INFRASTRUCTURE_FOUNDATION: PASS
AZURE_VM_DEALLOCATED: OPERATOR_REPORTED
AZURE_OFFLINE_RUNTIME_EVIDENCE: PASS
ENTRA_OIDC_OFFLINE_READINESS: PASS
REAL_ENTRA_AUTHENTICATION: BLOCKED
PRIVATE_TLS_OFFLINE_READINESS: PASS
PRODUCTION_PRIVATE_HTTPS: BLOCKED
PROVIDER_GOVERNANCE_OFFLINE_READINESS: PASS
REAL_PROVIDER_COMPATIBILITY: BLOCKED
INDEPENDENT_LIVE_EXECUTION_AUTHORITY: BLOCKED
SQLITE_SYNTHETIC_LIFECYCLE: PASS
PRODUCTION_AUTHORITY_INITIALIZATION: NOT_PERFORMED
LOCAL_FIVE_SERVICE_INTEGRATION: PASS
AZURE_FIVE_SERVICE_ACCEPTANCE: NOT_PERFORMED
REGRESSION_TESTS: PASS
EVIDENCE_RECONCILIATION: PASS
DOCUMENTATION: PASS
PRE_COMMIT_REVIEW: PASS
PHASE19B_OFFLINE_READINESS: WITH_CONDITIONS
PHASE19B_OVERALL_COMPLETION: WITH_CONDITIONS
PHASE19C_READY: NO
AZURE_ACTIVATION_AUTHORIZED: NO
LIVE_INFERENCE_AUTHORIZED: NO
PUBLIC_EXPOSURE_AUTHORIZED: NO
GIT_COMMIT_PERFORMED: NO
GIT_PUSH_PERFORMED: NO
```
