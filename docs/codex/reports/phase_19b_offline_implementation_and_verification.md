# Phase 19B — Offline implementation and verification

19 November 2026. Baseline `master` at `b48dde4e4012f83c8fa2de99acbb54b8a59e0683`.
**Offline foundation implemented WITH_CONDITIONS; Azure deployment remains BLOCKED.**
No Azure command, live Entra authentication, real model request, credential renewal,
execution-approval signing, Git commit or push occurred. No historical authority was opened
or modified. Only new temporary synthetic authorities were used for validation.

## Baseline and implemented scope

Read AGENTS.md and all four complete Phase 19A deliverables, inspected current Docker/Compose,
Settings, entrypoints, OIDC/security/governance, provider factory/bounded execution, document
pilot/operator/runner/publication/object storage and tests. HEAD matched the requested baseline.
Initial Git status contained exactly the four untracked 19A Markdown files. Those remain:
19A prompt/report unchanged, architecture/plan with dated append-only implementation addenda.
No readiness research was repeated and no connected/cloud source was needed.

The implementation preserves the single-host authorities, `InferenceProvider` boundary and
existing local launchers. It does not change API NDJSON/SSE adaptation, routing, memory,
Ollama, admission algorithms, ledger schemas, prices, session consent/financial guarantees,
historical signed configuration fingerprints or existing governance records.

| Reused component | Implementation around it |
| --- | --- |
| Existing CPU-only Docker image, pinned offline retrieval models, UID 10001 | Separate five-service Compose, resource/security/health/shutdown settings; same image shared by API/UI/gateway |
| Documents operator API, security middleware, durable workflow and LocalRunner | Shared HTTP factory extracted from fixture module; compatible old import re-export; separate production runtime |
| OIDCSettings/Entra verifier, SecurityRuntime, SQLite authorities | Required tenant-specific Entra profile, explicit enrollment/source binding, private complete-authority reopen; no fixture verifier in production |
| Job ledger, canonical objects, publication authority, real Chroma adapter/encoder/reranker | Stable `/state` binding, explicit new initialization versus serve/reopen, production local-filesystem checks and exclusive persistent POSIX lock |
| Existing aiohttp TLS/WebSocket proxy factory | Shared UI module, production TLS entrypoint with required origin/cert/key, removal of incoming forwarded headers; fixture wrapper retained |
| Existing OpenAI-compatible adapter, strict schema/capabilities, governed bounded execution | Additive runtime credential-file and authentication-header configuration; strict production prerequisites and offline contract tests |
| Existing pilot UNKNOWN/idempotency/financial semantics | No retry/settlement changes; additional start/question execution denial in external workflow; memory-only runner grants preserved |

## Secure Compose and supervision

`docker-compose.phase19.yml` requires explicit paths/image/origin. It publishes only
`127.0.0.1:9443`; API, worker, Redis and Chroma have no host port. The gateway forwards only
to Streamlit. Backend/frontend networks are internal, with a separate API/UI egress network.
Compose is not an outbound destination firewall: a reviewed host/private-network policy is
still required. No public application exposure was performed.

Application containers use 10001:10001; Redis runs explicitly as 999:999 and Chroma as
10001:10001. These vendor identities were actually exercised with private writable data
mounts, dropped capabilities and read-only roots. Vendor image metadata itself declares no
non-root user; explicit Compose overrides are essential. No database or fixture-issuer ports
are published. All secret mounts are read-only, all binds disable host-path creation,
application temporary files use bounded private tmpfs, logs rotate at 3 × 5 MB/service,
restart is `on-failure:3`, and shutdown grace is 90 seconds.

Dependency order is Redis/Chroma protocol health → API administrative readiness → UI health
→ TLS gateway. Chroma uses an actual HTTP heartbeat, not just an open port. The gateway's
container probe is TCP liveness; it is **not** certificate/browser/OIDC acceptance. Production
`/ready` additionally retains the existing worker, security, control, publication, unsettled
reservation and reconciliation checks. It does not grant external execution permission.

The systemd template uses RequiresMountsFor, ConditionPathIsMountPoint and a mountpoint
precheck for `/srv/polymind`, explicit Compose inputs and bounded start/stop timeouts.
`systemd-analyze verify` passed. The unit was not installed/enabled, and VM reboot behavior
was not tested. Startup never initializes missing authorities or resumes bearer grants.

## Application and authentication outcomes

**Chat/RAG: GAP, disabled in the profile.** Existing OIDC denial guards remain untouched.
The legacy generation/stream path and UI do not have the scoped governed execution contract
needed here. Enabling them would require a distinct authorization design. Local Chat/Ollama
and NDJSON contracts continue to pass their existing regressions; static/disabled auth was
not substituted for OIDC in the deployment.

**Documents non-fixture composition: GAP overall.** The separate runtime genuinely assembles
SecurityRuntime/Entra verification, real provider adapter, approved source catalog, durable
pilot/workflow/actions/runner and real retrieval adapters, without importing development
fixtures. It supports authenticated operator context/source inspection and bounded intake.
Context and usage labels distinguish external blocked mode from synthetic mode. Missing
configuration, malformed identity, foreign tenant/owner, unsafe paths, missing capability or
unpriced role fail closed. Unit/integration tests use offline signed JWTs and test-only
retrieval adapters; no Entra network fetch is permitted in those tests.

The retained `SessionApproval.zero_paid_execution` is literally `True`, and its default
execution hook is fixture-only. A login, source approval or mounted key cannot authorize
paid execution. The external composition therefore supplies an always-denying execution
hook, disables start/question before reservations, and refuses an external workflow with
`execution_enabled=True`. The UI disables those controls. Existing synthetic behavior stays
enabled by default for its own composition. No environment flag can turn this foundation
into a paid runner. A reviewed configuration-bound independent live permission bridge is
still essential; this report does not claim an executable paid Documents workflow.

## Provider offline contract

`OPENAI_COMPATIBLE_AUTHENTICATION_HEADER` exposes the adapter's existing `Authorization`
(default/Bearer) or `api-key` behavior. `OPENAI_COMPATIBLE_API_KEY_FILE` reads a bounded,
private, owned, regular, non-symlink runtime file; simultaneous inline/file sources, unsafe
permissions, whitespace-only/oversized secrets and arbitrary header names are rejected.
There is no renewal, managed-identity acquisition or browser-token reuse for inference.

The production runtime requires explicit HTTPS v1 endpoint, role map, tenant identity,
shared financial/provider policies, approved catalog covering both used roles, strict managed
schema and usage-reporting capabilities. Defaults cannot supply missing essential production
inputs. Settings are constructed from the private reviewed configuration with explicit
defaults and no dotenv/environment inheritance. Existing bounded execution enforces time,
response bytes, schema/model/usage and normalized provider errors. Existing mocks/regressions
exercise timeout, 429, malformed/incomplete streams, usage/UNKNOWN, governance/admission and
no unauthorized retry. New tests verify factory header/file behavior and missing capability
denial before reservations. Provider adapter code and financial settlement algorithms did
not need modification.

`REAL_PROVIDER_OFFLINE_CONTRACT: PASS` means these offline contracts passed; no actual Foundry
endpoint/model/version/quota/tariff/token/header compatibility was verified. Historical
Phase 17H evidence grants no new authority. External execution remains blocked in both
application planes, so neither can bypass shared provider admission through this profile.

## Persistence, recovery and review findings

Production startup checks a private marker binding to `/state`, compatible ext4/xfs/btrfs,
private directory/object roots, all seven authority databases, schema version and SQLite
integrity before opening services. Missing/truncated/wrong-mode/symlink state is refused;
serve has no initialization fallback. SQLite is never placed on network filesystems.
The CLI holds a persistent `flock` inode through the entire Uvicorn/runner lifetime.

Self-review discovered that installed filelock 3.29 unlinks its lock file on release.
Using that implementation for this new deployment's backup/API ownership could split the
lock domain. The new deployment instead uses a persistent POSIX lock file, never unlinked.
Existing development fixture launchers retain their historical behavior. LocalRunner also
refuses duplicate/restarted thread starts and reports a worker that fails to join rather
than silently treating it as stopped. Cleanup closes the owned provider/vector resources.

The backup tool requires an explicit all-writers-stopped assertion and exclusive API lock,
copies the whole operator/Redis/Chroma tree, preserves numeric owners/modes, rejects unsafe
entries, compares SHA256 inventories and checks restored SQLite integrity. Restoration
requires a new isolated destination and never starts services. A real container test with
UID 10001 application authorities and UID 999 Redis files passed snapshot/restore and owner
preservation. The caller's stop assertion is an operational prerequisite: the API lock
cannot independently prove vendor containers stopped. Checksums protect against damage,
not a malicious backup custodian. Failed partial copies are never accepted automatically.

Actual Docker restart of the completed synthetic API/Redis/Chroma preserved the completed
job and all three SETTLED reservations. Across the observation window there were **zero new
calls**. Readiness correctly returned **503 awaiting an authorized publication replica reload**;
restart does not reload ownership-sensitive presentation automatically. All restarted services
then exited 0. Existing regressions also prove accepted Q&A survives authorized reopen,
refresh/reauthentication does not regenerate answers, and UNKNOWN/consumed/expired authority
cannot be cleared by replay. Cloud stale-truth reconciliation, off-disk snapshot custody,
reboot/full-disk behavior and RPO/RTO remain unverified.

## Representative resource evidence and limitations

The temporary synthetic overlay derives the actual hardened five-service profile. It
changes API/identity/TLS inputs explicitly, removes **all** published ports and the egress
network, and uses deterministic fixture inference. It loads the real baked embedding and
cross-encoder reranker and publishes the accepted digest through real Chroma HTTP. This is
more representative than measuring only a fixture container, but it is a tiny document and
a headless UI, not a production user workload or actual Entra/browser acceptance.

| Observation | Result |
| --- | --- |
| Five-service startup through healthy gateway | 40.296 seconds |
| Embedding + reranker loading in API | 8.428 seconds |
| Idle aggregate Docker-reported memory | 543.71 MiB |
| Maximum sampled aggregate during document processing | 584.75 MiB |
| API sampled memory | 448.7–479.4 MiB |
| Streamlit sampled memory | 46.51–57.58 MiB |
| Gateway sampled memory | 24.93–30.35 MiB |
| Redis sampled memory | 6.949–7.898 MiB |
| Chroma sampled memory | 15.59–19.34 MiB |
| Maximum sampled aggregate Docker CPU | 35.86% (100% represents one logical core) |
| Final shared application image | 3,042,576,001 bytes |
| Redis / Chroma images | 57,337,242 / 826,133,216 bytes |
| Baked retrieval artifacts | 183,383,671 bytes |
| Final synthetic operator / Redis / Chroma logical file bytes | 839,471 / 177 / 364,708 |
| Synthetic workflow | COMPLETED, digest COMPLETE, explicit canonical Chroma publication |
| Synthetic provider evidence | 3 attempts; 90 measured input / 120 output tokens; 0 external calls; 0 unsettled/UNKNOWN |
| Controlled stop | All five containers exited 0; dedicated containers/networks removed |

The fixture's EUR 0.000033 ledger value is a **synthetic tariff calculation**, not incurred
model spend. Sampling roughly every eight seconds plus Docker stats overhead can miss short
CPU/memory spikes; it includes health probes and a short-lived workflow client in the API
container. Docker memory excludes some host/kernel/cache/image/OS costs. Logical file sizes
are not allocated blocks, filesystem capacity or growth forecasts. Shared image layers are
not charged three times because API/UI/gateway use the same image. The complete image set
is about 3.93 GB logical uncompressed image size, not RAM.

This provides initial headroom evidence for a tiny synthetic workflow, **not proof that an
8-GiB VM is sufficient**. Neither Standard_B2as_v2 nor Standard_D2as_v5 is selected. Sustained
CPU, burst credits, 2-vCPU contention, browser sessions, larger corpora, vector growth,
recovery/backup and Azure disk/network latency require bounded approved cloud measurements.
The configured 5.625-GiB aggregate container ceilings are limits, not observed consumption
or reserved capacity. The USD 30 planning envelope remains unapproved.

## Exact validation record

Commands ran from the repository with existing Python dependencies. HTTP/thread tests were
run through execution-policy approval outside the sandbox after a confirmed sandbox timeout;
all identities/providers remained offline fixtures/mocks. No package was installed.

```bash
python -m pytest -q tests/unit/test_phase19_deployment.py

env HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python -m pytest -q \
  tests/unit/test_phase19_deployment.py tests/integration/test_phase19_operator.py \
  tests/integration/test_document_operator.py tests/unit/test_documents_view.py \
  tests/unit/test_provider_contract.py tests/unit/test_structured_provider.py \
  tests/unit/test_security_configuration.py tests/unit/test_security_entra.py \
  tests/unit/test_local_apps.py

env HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python -m pytest -q
PYTHONPYCACHEPREFIX=/tmp/phase19b-bytecode python -m compileall -q .
git diff --check
systemd-analyze verify deployment/phase19/polymind.service

docker compose --env-file /dev/null -f docker-compose.yml config --quiet
env DOCUMENT_DEMO_ROOT=/tmp/phase19b-inert docker compose --env-file /dev/null -f docker-compose.documents.yml config --quiet
docker compose --env-file deployment/phase19/compose.env.example -f docker-compose.phase19.yml config --quiet
docker build --iidfile /tmp/phase19b-image-id .
```

The full regression run passed **3,214 tests in 977.12 seconds**, including all 3,184 baseline
tests and the 30 new cases present at that run's collection. Subsequent self-review fixes
and six additional focused cases were verified by the final group: **305 passed, one warning,
in 69.58 seconds** (36 Phase 19 cases plus 269 affected existing regressions). The full suite
was not rerun after those narrow fixes; the final focused group covers all changed runtime,
UI/provider/security contracts. The warning is aiohttp's advisory `NotAppKeyWarning` for the
proxy's pre-existing string application key; it does not change test outcomes. Compilation,
whitespace, all three Compose parsers and systemd syntax verification passed. A stripped-
environment Compose check also rejected absent Phase 19 inputs as required; final Docker
inspection confirmed no dedicated validation containers remained running. No configured
lint/format tool was found; none was installed just for this phase.

Earlier runs are not hidden: the first new-unit run had **15 passed/1 failed**, correctly
exposing the filelock unlink behavior; after the POSIX fix, **16 passed**. An initial targeted
sandbox run timed out at 180 seconds with no completed result. The first outside-sandbox
group had **296 passed/1 failed** because the new test submitted a too-short request key and
an unknown session, reaching protocol/source denial before the intended permission assertion.
The test was corrected to create a valid owned session and assert 503 start/question denial.
Subsequent groups passed **299/71.35 seconds**, then **300/69.44 seconds**, then final **305**
as above. These counts overlap and must not be added.

Container experiment commands were `python /tmp/phase19b_docker_validation.py` (the initial
implementation of the now-preserved `scripts/phase19_offline_validation.py` harness), followed
by `python /tmp/phase19b_restart_validation.py`. Logs remain under `/tmp/phase19b-*.log`.
The reproducible harness requires `--image` and a new `--root`; it creates only a random
scoped Compose project. Initial container preparation hit host permission denial when the
harness tried to inspect its deliberately UID-10001-owned directory; inspection was moved
inside a network-disabled container. The corrected five-service run, publication and restart
passed. The final source harness's argument/random-project wrapper was compiled; the measured
run used its otherwise equivalent temporary predecessor.

Final cached image ID is
`sha256:29a9653666ab760000b49273fd801275bec958b727d38ba361b5621245000fe4`.
The earlier resource run used
`sha256:a70d091c85b96d93c44c174554f32c94f63a0e43a7ea2c86562fe033d9e5c33b`;
the restart and mixed-owner recovery checks used the final image. Builds reused dependency/
model layers; no --no-cache, prune or image deletion occurred. A mistaken preliminary
recovery no-op pulled `python:3.10-slim`; it supplied no validation evidence and was not used
for the actual recovery test. An initial actual recovery invocation lacked `PYTHONPATH` and
failed import; the corrected exact command passed:

```bash
docker run --rm --network none --user 0:0 --read-only -e PYTHONPATH=/app \
  --tmpfs /validation:rw,size=32m \
  --mount type=bind,source=/tmp/phase19b-mixed-owner-recovery.py,target=/check.py,readonly \
  sha256:29a9653666ab760000b49273fd801275bec958b727d38ba361b5621245000fe4 \
  python /check.py
```

Image-content assertions confirmed no `/app/.env`, private keys, SQLite authorities or test
suite entered the measured image. Docker disk inspection printed aggregate byte counts only.
Synthetic test keys/state remain in private temporary directories outside the repository;
no real secret file was inspected. No public port was opened during the container experiments.

## Exact file inventory and pre-commit review

Tracked files modified:

- `.env.example`
- `config/settings.py`
- `development/document_demo/app.py`
- `development/document_demo/gateway.py`
- `documents/operator/service.py`
- `llm/provider_factory.py`
- `ui/documents_view.py`

New Phase 19B files:

- `config/runtime_secrets.py`
- `deployment/phase19/__init__.py`
- `deployment/phase19/__main__.py`
- `deployment/phase19/backup.py`
- `deployment/phase19/compose.env.example`
- `deployment/phase19/configuration.example.json`
- `deployment/phase19/gateway.py`
- `deployment/phase19/polymind.service`
- `deployment/phase19/runtime.py`
- `deployment/phase19/storage.py`
- `deployment/phase19/ui.py`
- `docker-compose.phase19.yml`
- `documents/operator/app.py`
- `ui/tls_gateway.py`
- `scripts/phase19_offline_validation.py`
- `tests/unit/test_phase19_deployment.py`
- `tests/integration/test_phase19_operator.py`
- `docs/operations/phase_19_vm.md`
- `docs/codex/prompts/phase_19b_offline_implementation.md`
- `docs/codex/reports/phase_19b_offline_implementation_and_verification.md`

Existing untracked 19A files retained, with dated addenda only on the last two:

- `docs/codex/prompts/phase_19a_readiness_verification.md` — unchanged
- `docs/codex/reports/phase_19a_readiness_report.md` — unchanged
- `docs/evaluation/phase_19_deployment_architecture.md` — appended
- `docs/evaluation/phase_19_implementation_plan.md` — appended

Implementation self-review checked complete new/modified code and consumer compatibility,
provider isolation, startup/reopen/error/cleanup paths, authorization labels and financial
semantics. It fixed persistent lock behavior, duplicate runner starts, scope of inherited
configuration, volatile/network filesystem refusal, missing usage/schema/price checks,
forwarded-header spoofing and disabled UI execution controls. Tests cover those boundaries;
no broad redesign or pilot/financial schema change was introduced.

Separate pre-commit review checked all new/modified file names/content, local Markdown links,
private key/credential payload patterns, generated authorities/secrets, temporary/debug files,
TODOs, dependencies and unintended APIs. No credentials, private keys, real dotenv files,
runtime DBs or generated secret files were added. Explicit `/state`, `/srv/polymind`, `/etc`
and `/tmp` paths are documented deployment/test paths, not developer-machine dependencies.
The synthetic validation harness is intentional tooling, not a production default. Existing
Docker exclusions remain adequate and no dependency/requirements/Dockerfile change was needed.

Final `git status --short --branch` is `master...origin/master`, seven tracked modifications
and the untracked files above (Git groups the new deployment directory). Nothing is staged.
`git diff --stat` reports **7 files, 58 insertions, 176 deletions**; moved implementations now
reside in untracked new files, so this stat alone is not the complete addition count.
There are 24 untracked files including four preserved 19A files. No commit or push occurred.

## Operator blockers and verdict

The next operator review must settle the governed Chat path or explicitly retain its
exclusion, and accept a bounded independent Documents execution-permission bridge preserving
current zero-paid session and historical evidence semantics. That is still implementation
work, not merely supplying a key. Before any cloud work additionally resolve current Azure
scope/RBAC/quota, access/egress, real identity/TLS custody, stable disk/restore acceptance,
resource/cost/window ownership and separate model/source/tariff/shared-authority approvals.
No current model deployment, Entra browser flow, real inference or Azure VM capacity has
been verified by 19B. Public production acceptance remains separately unapproved.

```text
PHASE_19B_OFFLINE_IMPLEMENTATION_COMPLETE: WITH_CONDITIONS
DOCKER_COMPOSE_OFFLINE_VALIDATION: PASS
CHAT_OIDC_INTEGRATION: GAP
DOCUMENTS_NON_FIXTURE_COMPOSITION: GAP
REAL_PROVIDER_OFFLINE_CONTRACT: PASS
SINGLE_HOST_PERSISTENCE_AND_RECOVERY: PASS
AZURE_DEPLOYMENT_READINESS: BLOCKED
AZURE_PROVISIONING_AUTHORIZED: NO
LIVE_INFERENCE_AUTHORIZED: NO
PUBLIC_EXPOSURE_AUTHORIZED: NO
```

Persistence PASS is limited to the tested single-host/offline lock, complete-state reopen,
quiesced-copy/isolated-restore and no-repeat behavior. It does not assert cloud disaster
recovery or stale financial rollback safety. Stop here for operator review; Phase 19C is
not started.

## Integration Gap Resolution

19 November 2026 continuation in the same working tree. All preceding observations, test counts
and original GAP verdicts are retained as historical evidence. This section records the new
implementation and executed acceptance; its verdict supersedes the two integration GAPs only.
No Phase 19A research, cloud authentication, provisioning, real inference, credential renewal,
live-approval signing, historical-record modification or Git commit/push was performed.

### Root causes and bounded design

Chat's OIDC denial was intentional: its legacy graph had an unscoped corpus/memory path and
text/stream inference with no independent permission or governed usage settlement. Forwarding
an API token or removing that guard alone would have exposed data and bypassed finance. The
continuation adds a genuine request-scoped authorization context and uses the existing
GovernedExecution, SecurityAuthority, provider admission and action journal. Legacy unbound
OIDC calls still fail closed; local Ollama/development calls retain their interfaces.

Documents had the required durable services but `pilot-session/1.zero_paid_execution` is literally
true and its default provider hook is fixture-only. A live permission cannot change that record's
meaning. A distinct `pilot-execution-session/2` approval now explicitly carries false plus an
independent execution-permission UUID and all inherited external consent/privacy/exposure/quality
requirements. Version-1 parsing/serialization and historical approval/signature fingerprints are
unchanged. New version-2 sessions can use the existing pilot execution path; zero-paid sessions
cannot satisfy the bridge, even if another signed record exists.

Inspection also found two non-fixture workflow constraints that configuration alone could not
solve. External digest presentation already requires two independent quality reviews; generated
answers require their own reviews and return pending metadata. The operator adapter now preserves
that pending/accepted distinction and reuses the existing review/presentation methods. It does not
invent human acceptance or remove review gates. The production runner now waits conservatively
before claiming a document step, consistent with the existing forecast's 61-second call spacing,
so a low quota causes waiting rather than an unnecessary failed synthesis attempt. Actual shared
admission still makes the authoritative decision; no quota or pricing value was changed.

### Independent execution authority and Documents bridge

`security/execution.py` promotes the existing ApprovalTrust model out of the performance launcher
into reusable production infrastructure. The old launcher re-exports/imports the same model;
its verification/consumption logic and serialized trust shape remain intact. New web permissions
have their own issuer, audience, JWT type and purpose. Historical Foundry artifacts cannot be
substituted, consumed or renewed through this port.

The independent custodian supplies an RSA public-key trust record, explicit revocation list and
signed permission files. Production requires a read-only authority mount; the signer private key
is never available to the application. This required one narrowly scoped new Compose bind and
`PHASE19_EXECUTION_AUTHORITY` input, outside writable `/state`. It is a custody dependency, not a
service/storage redesign. Existing five services, networks, image strategy, database locations,
backup/restore and single-writer architecture are unchanged.

Verification enforces exact RS256 header/key/type, issuer/audience, live-versus-test purpose,
canonical permission ID, bounded integer validity/max-call fields, independently pinned operator
issuer/subject/tenant, exact resource/scopes and the canonical runtime binding. The binding
includes configuration and manifest, source/session approvals, logical model/deployment aliases,
actual endpoint, generation/analysis/planning/Chat capabilities, financial policy/catalog,
provider admission/key and stable authority paths. Secret bytes are excluded. Changed runtime
models, endpoint or capabilities cannot reuse the permission.

The Documents resource binds the precise session UUID and fingerprint of the entire source
approval. Synthesis and question scopes are distinct. Permission, token, source/session window
and headroom checks occur before a new call; source/security/control state and permission are
revalidated after admission and before acceptance. Revocation before dispatch produces no provider
request; revocation/expiry during an already dispatched call cannot undo billing, and acceptance
is withheld while accounting remains conservative.

Per-call permission consumption uses opaque call identities in the **existing actions table**.
It creates no parallel budget, provider queue or ledger. A permission's maximum cannot reset on
restart, key change or a repeated identity. Denied later admission conservatively consumes that
claim. The unchanged governed executor handles reservation, provider admission, settlement and
UNKNOWN evidence. Unfinished/UNKNOWN shared financial obligations block new claims in either
application. Existing pilot intent/step fences, deadlines, source bounds and question limits remain.

The frontend uses the selected session's separate backend Start/Question flags, including
the remaining signed call allowance. Exhaustion disables new execution while accepted reads
and intent replay remain available. A valid grant on
another session does not enable the selected session. A digest waiting for independent reviews
is shown as pending review. Q&A returns an opaque pending-answer ID/evidence fingerprint; accepted
answer text/citations are read only through the retained review/presentation gates. Accepted
answers are durable across reauthentication/reload without inference. The new explicit reload
operation rebuilds only an authorized publication replica, never worker grants or model work.

### Chat OIDC, graph, retrieval, memory and streaming path

The private Streamlit application now provides Chat alongside Documents. It uses the native
API access token, forwards it per request with redirects disabled and does not interpret a
browser claim as server authority. FastAPI independently verifies OIDC, the exact enrolled
operator and the signed Chat permission. Missing, expired, foreign-tenant/owner, wrong-role,
wrong-purpose and mismatched-scope requests fail before provider effects. There is no static,
disabled-auth or development-issuer fallback.

The permission has a closed list of conversation IDs and source document IDs. Chat uses existing
SecurityAuthority snapshots and ScopedMemory; its memory namespace includes the approved source
set. All referenced documents must be owned by the enrolled principal, active and covered by
current approved source hashes/expiry. Removing a source set cannot expose its old conversation
history under the new scope. Document revocation blocks subsequent memory/retrieval/release.
Hybrid retrieval uses the canonical PublicationReplica path: filtered dense search, per-document
BM25, reciprocal-rank fusion, reranking and provenance validation. Unfiltered legacy retrieval is
never used in an OIDC Chat request.

`graph/composition.py` extracts the existing LangGraph factory from legacy process-global provider
initialization. Existing import paths/local globals remain in `graph/langgraph_flow.py`. The same
routing/model/tool/direct/RAG nodes accept a typed, validated authorization context; unbound OIDC
guards remain. Original local helper calls receive no extra keywords, preserving existing injected
callable contracts. All provider-specific HTTP behavior remains in inference infrastructure.

`/query` retains its response fields; `/query/stream` retains metadata/chunk/done/error NDJSON.
The governed path additionally requires an explicit request key. Both transports share one durable
intent record: a JSON/NDJSON retry converts the accepted result format without a second provider
request or memory append. Changed payloads under the same key are denied. Cached RAG results also
revalidate their publication generation and canonical pin; they cannot silently replay stale
publication content. Legacy development callers still do not need the new key.

The historical `llm/structured.py`, `llm/bounded_http.py` and `llm/openai_compatible.py` retain
exact baseline bytes. Their pinned v10/v11 inventories and frozen fixtures are unchanged.
The additive streaming adapter delegates all non-streaming generation to that original adapter.
Bounded OpenAI-compatible SSE now enters the optional structured-provider port through a token
callback with final usage. GovernedExecution retains the sole reservation/admission/settlement
path, revalidating authority before dispatch and chunk release. The parser bounds total wire bytes,
deadline and content bytes; checks response-model identity, termination and usage envelope; and
closes the response. It never forwards raw SSE to clients. Chunks may be provisional, but no done,
accepted result or conversation exchange is persisted without known usage and current authority.
Missing usage, timeout, truncation, client cancellation or ambiguous failure retains UNKNOWN or
unfinished intent evidence. There is no automatic inference retry. Frontend refresh is read-only,
and uncertain partial output is removed from the view.

### Executed offline integration and regressions

The new integration tests construct the actual production runtime over isolated real security,
governance, admission, job, control, action and publication authorities. They use the real Entra
verifier with signed local identity JWTs, the real independent permission verifier with ephemeral
**test-purpose** signatures, and the OpenAI-compatible adapter over fake HTTP. Authorization
checks/signature verification are not mocked. Test composition changes the permission purpose,
retrieval adapters and clock only where needed for isolated, bounded tests; production accepts
only live-purpose records from a read-only authority mount. No live record was signed.

Coverage includes full external Start → managed digest → publication → independent review →
question → pending answer → its own review → accepted Q&A; cross-transport Chat intent replay;
LangGraph JSON/direct/tool and NDJSON execution; scoped hybrid retrieval/memory; missing/expired/
revoked/mismatched/source/role/tenant/token failures; financial and provider admission denial;
post-admission revalidation; insufficient permission window; missing usage/timeout/truncation/
429 behavior; durable call bounds; zero-paid rejection; accepted-answer and permission persistence
across a full runtime reopen; and Streamlit token forwarding/refresh/disabled-control behavior.

The existing five-service harness gained an explicit `--integration-tests` mode. It reuses the
same hardened profile, removes every published port and provider egress, mounts test code read-only,
and uses the actual production assembly with test-purpose permissions and fake provider HTTP.
Real Redis, Chroma HTTP, baked MiniLM embeddings/cross-encoder and semantic routing are exercised.
Test-only step/review routes live solely in mounted test code and are absent from the production
entrypoint/image. Synthetic review records are not real independent semantic acceptance.

The topology run completed Documents and Chat query/NDJSON/RAG/memory with **7 fake provider calls,
0 external calls**, known settled usage, and no extra call on transport replay. The frozen-source topology reached healthy status in
40.504 seconds; this is startup evidence, not VM capacity qualification. Both application
paths are therefore verified end to end, beyond configuration parsing or a standalone permission
mock. All scoped containers stop cleanly and the harness removes only its own project.

New validation commands and results (counts overlap; do not add them):

```bash
# Retained approval/provider/pilot contracts.
python -m pytest -q tests/unit/test_foundry_approval.py \
  tests/unit/test_structured_provider.py tests/unit/documents/test_pilot_controls.py

# Affected security, application, provider and compatibility group.
env HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python -m pytest -q \
  tests/integration/test_phase19_execution_bridge.py tests/integration/test_phase19_operator.py \
  tests/integration/test_document_operator.py tests/unit/test_phase19_deployment.py \
  tests/unit/test_security_api.py tests/unit/test_security_entra.py tests/unit/test_foundry_approval.py \
  tests/unit/test_structured_provider.py tests/unit/test_streaming_orchestration.py \
  tests/unit/test_ui_api_client.py tests/unit/test_local_apps.py tests/unit/test_documents_view.py \
  tests/unit/test_phase19_chat_view.py tests/unit/test_phase19_bounded_stream.py

# Final correction group: shared transport intents, stream bounds, native UI and selected-session controls.
env HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python -m pytest -q \
  tests/integration/test_phase19_execution_bridge.py tests/unit/test_documents_view.py \
  tests/unit/test_phase19_chat_view.py tests/unit/test_phase19_bounded_stream.py \
  tests/unit/test_streaming_orchestration.py tests/unit/test_ui_api_client.py

env HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python -m pytest -q
PYTHONPYCACHEPREFIX=/tmp/phase19b-gap-bytecode python -m compileall -q .
git diff --check
systemd-analyze verify deployment/phase19/polymind.service

docker compose --env-file /dev/null -f docker-compose.yml config --quiet
env DOCUMENT_DEMO_ROOT=/tmp/phase19b-gap-inert docker compose --env-file /dev/null -f docker-compose.documents.yml config --quiet
docker compose --env-file deployment/phase19/compose.env.example -f docker-compose.phase19.yml config --quiet
docker build --iidfile /tmp/phase19b-gap-final-image-id .
python scripts/phase19_offline_validation.py --root /tmp/phase19b-final-acceptance-20261119 \
  --image sha256:afac225fe4c952e5c26b7c9bb1c924c83d1e01cf779c4b27ef1e32b30d00adef --integration-tests
```

The retained contract group passed **151 tests in 17.30 seconds**. The affected group passed
**427 tests in 137.47 seconds**, with the same non-fatal aiohttp AppKey advisory as earlier.
The final correction group initially passed **86 tests in 57.96 seconds**; adding exhausted-
permission availability/read/replay checks produced **88 passed in 133.82 seconds**. A UI-specific final check passed
**23 tests in 1.72 seconds**. After moving streaming to additive modules, the historical
source-inventory/approval/provider and new integrated-path group passed **196 tests in 167.52 seconds**.
These are executed continuation results, not reused 19A/initial-19B counts. Final complete-suite result: **3,278 passed, 1 warning in 1,367.81 seconds (22:47), exit 0**.

The full suite warning is the existing aiohttp `NotAppKeyWarning` in the TLS gateway test;
there were no failures, errors or skips.

Compilation, all three Compose parsers, systemd syntax and whitespace checks passed. Dependency
and model layers were cached; no dependency install, --no-cache build, prune or image deletion
was performed. No configured lint tool was added. Final image and Compose acceptance are
recorded in the final-validation paragraph below. Logs remain `/tmp/phase19b-gap-*.log`; runtime
keys and authorities remain private temporary test artifacts outside source.

Intermediate diagnostics are retained honestly: canonical UUID consumption initially failed
before financial reservation; external Q&A then exposed the already-required quality review and
pending-answer contract; a fixture timestamp rounded slightly into the future; test grant override
argument names collided; a revocation assertion ran before the first inference-bearing step; and
a fixture memory-factory replacement lacked its optional default. Those were corrected without
relaxing authorization. An admission test initially expected 429 where the retained application
contract maps overload to 503; the contract was preserved and the assertion fixed. The first
broader group reported **413 passed/4 failed** because adding an `execution=None` keyword broke
legacy injected helper callables; conditional argument passing restored compatibility, confirmed
by **18 passing** streaming/client tests. The first Compose run used a generic RAG query with no
relevant source hits; the source-specific verification query was corrected rather than weakening
retrieval. A preliminary full run was deliberately interrupted after **291 passed in 151.36 s**
when self-review found the cross-transport idempotency gap. It is not counted as a completed run;
a later incomplete broad run exposed historical provider-file source pins (**5 failed, 926
passed, 18 setup errors** before interruption at 558.62 s). Rather than rewrite those historical
inventories, streaming was moved to additive modules and the three original files restored to
their unchanged baseline bytes. The final complete run after those corrections is the acceptance
evidence above. No historical approval, record, frozen source or inventory was changed.

### Exact continuation file inventory

Existing files modified in this continuation (including files that were already untracked at entry):

- `api/app.py`, `api/operator.py`, `api/security.py`
- `documents/operator/app.py`, `documents/operator/service.py`
- `documents/pilot/models.py`, `documents/pilot/control.py`, `documents/pilot/execution.py`, `documents/pilot/service.py`
- `governance/execution.py`
- `graph/langgraph_flow.py`, `graph/generation.py`, `graph/nodes.py`, `graph/streaming.py`
- `llm/provider_factory.py`
- `ui/api_client.py`, `ui/documents_view.py`
- `deployment/phase19/runtime.py`, `deployment/phase19/__main__.py`, `deployment/phase19/ui.py`, `deployment/phase19/compose.env.example`
- `docker-compose.phase19.yml`, `scripts/phase19_offline_validation.py`
- `tests/performance/foundry_approval.py`, `tests/unit/test_ui_api_client.py`, `tests/unit/test_documents_view.py`
- `docs/evaluation/phase_19_deployment_architecture.md`, `docs/evaluation/phase_19_implementation_plan.md`
- `docs/operations/phase_19_vm.md`, this report
- `docs/codex/prompts/phase_19b_offline_implementation.md` — continuation appendix

New continuation files:

- `api/chat.py`
- `graph/composition.py`
- `security/chat.py`, `security/execution.py`
- `ui/chat_view.py`
- `llm/bounded_stream.py`, `llm/openai_streaming.py`, `llm/streaming.py`
- `tests/integration/test_phase19_execution_bridge.py`
- `tests/unit/test_phase19_chat_view.py`, `tests/unit/test_phase19_bounded_stream.py`
- `tests/phase19_container_app.py`, `tests/phase19_container_driver.py`

The verified storage/backup modules, Dockerfile/dependencies, original development launchers,
Phase 19A prompt/report and every other pre-existing tracked/untracked change were preserved.
The architecture/plan receive dated addenda; earlier historical conclusions/test results are not
rewritten. The operator guide describes current implemented behavior and required custody inputs.

### Invariants, final review and remaining operator decisions

Self-review checked full new/modified code and all graph/provider/API/approval consumers. It
corrected legacy-callable compatibility, canonical claim identities, source-bound memory/retrieval,
publication replay validation, deadline headroom, strict stream bounds/usage, shared transport
idempotency, independent read-only trust custody, selected-session controls and pending expert
reviews. The production path always uses the existing financial/admission executor and the one
locked durable runner. Accepted content is gated again at persistence/release boundaries; bytes
already sent or an in-flight bill cannot be recalled. No host-compromise or stale-financial-rollback
resistance beyond the existing single-host authority model is claimed.

A separate pre-commit review confirmed no private key/credential payload, real dotenv, runtime
database, generated secret, unrelated dependency or new live default was added. All 60 changed/new
files were scanned; ten local Markdown links resolved. A read-only, network-disabled run of the
final image confirmed it contains no dotenv, private key, runtime DB or test suite. The test signer exists only
in test code, uses ephemeral test-purpose records and cannot satisfy production verification.
Independent authority files are protected separately from the coherent writable-state backup;
restore must retain current revocations/consumed/financial truth and never start a stale clone
alongside the current provider consumer. The existing recovery limitations remain explicit.

There is no remaining offline Chat/permission-bridge implementation blocker. Before activation,
the operator must still approve the immutable image/configuration and independently provision
current Entra registration/delegated API scope, native browser/TLS custody, eligible sources and
real consent/reviews, exact endpoint/deployment/version/capabilities, pricing/quota/shared-consumer
bindings, fresh independent live permission and execution window. Current Azure subscription/
access/egress, resource/spend ceiling and VM capacity/CPU-credit proof remain unverified. No SKU
is selected; no real semantic review is satisfied by a synthetic test. The initial USD 30 proposal
remains planning only. No cloud action or live execution becomes authorized by these passes.

Final validation and Git record: compilation with an external bytecode cache, `git diff --check`,
all three Compose configuration checks and `systemd-analyze verify` exited **0**. The cached
build exited **0**, producing
`sha256:afac225fe4c952e5c26b7c9bb1c924c83d1e01cf779c4b27ef1e32b30d00adef`.
Its final integration harness exited **0** and all five services exited **0** before project
removal. Final logs are `/tmp/phase19b-gap-final-build.log`,
`/tmp/phase19b-gap-final-compose.log` and `/tmp/phase19b-gap-full-acceptance.log`.
The earlier additive-image acceptance also passed; only the module documentation changed
before the final cached build/repeat. Original byte-pinned provider files match HEAD **3/3**.
No lint configuration was found; no new lint dependency was installed.

`git status --short --branch`: **master...origin/master**, **23 modified tracked files,
37 untracked files**, nothing staged. The exact changed-file inventory is recorded above,
including preserved earlier foundation/19A files. `git diff --stat`: **23 files changed,
284 insertions(+), 267 deletions(-)**; as usual this excludes untracked additions.
No commit, push or other Git mutation occurred.

```text
CHAT_OIDC_INTEGRATION: PASS
DOCUMENTS_GOVERNED_EXECUTION_PERMISSION: PASS
DOCUMENTS_NON_FIXTURE_COMPOSITION: PASS
REAL_PROVIDER_OFFLINE_CONTRACT: PASS
DOCKER_COMPOSE_OFFLINE_VALIDATION: PASS
PHASE_19B_OFFLINE_IMPLEMENTATION_COMPLETE: YES
AZURE_PROVISIONING_AUTHORIZED: NO
LIVE_INFERENCE_AUTHORIZED: NO
PUBLIC_EXPOSURE_AUTHORIZED: NO
```

PASS/YES here mean the executed, bounded **offline** implementation scope. Real browser/provider/
Azure/semantic acceptance and all activation permissions remain separate. Stop here after final
verification; Phase 19C is not started.
