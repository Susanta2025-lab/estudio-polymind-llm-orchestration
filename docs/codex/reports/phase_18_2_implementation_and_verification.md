# Phase 18.2 — Secure document frontend implementation and verification

## Executive engineering decision

**Stage verdict: `PHASE_18_2_ENGINEERING_PASS`, `PHASE_18_2_LOCAL_INTEGRATION_PASS` and `PHASE_18_2_OFFLINE_VERIFICATION_PASS`.** All applicable local T01–T15 gates are established by the final frozen-tree regression, actual authenticated browser journeys and local container verification. The final regression passed **3,128 tests in 1,130.78 seconds**, with zero failures, errors, skips or pytest warnings. No unresolved critical/high implementation defect was identified in the implementation and separate pre-commit reviews. Verification completed on 14 November 2026; this is bounded local engineering acceptance, not production security or semantic-quality certification.

The implemented scope is a **private, local, synthetic owning-operator document application**. It extends Streamlit, adds the eleven approved FastAPI contracts, composes the existing Phase 17 authorities and services, and supplies a single-host runner independent of browser requests. The real browser journey has been demonstrated, including OIDC code login, verified API context, processing, COMPLETE validation, explicit publication, original evidence, grounded Q&A, withdrawal and logout. Separate browser checks establish cancellation, token expiry, missing-object failure and actual server restart. No public upload, ordinary-user enrollment, cloud deployment or paid inference path was added.

Exactly three formal stages remain. This work is Stage 18.2; Stage 18.3 documentation and closure has not begun. `AKS_NOT_REQUIRED` and `PRODUCTION_READINESS_NOT_ESTABLISHED` remain binding. The preserved [master prompt and authorization addendum](../prompts/phase_18_2_implementation_and_verification.md) and the four committed Stage 18.1 documents control this report.

## Baseline and preservation

Starting and current HEAD is `f0e420b6a4ab479ffaa166d000d55c91164f154b`, on `master...origin/master`. Initial `git status --short --branch`, seven-commit log, `git rev-parse HEAD` and `git diff --check` matched the requested assessment baseline. The tracked worktree and index were initially unchanged. Exactly **28 inherited untracked Phase 17H Markdown files** were present. Their SHA-256 inventory is preserved outside the repository and checked again at handoff.

The supplied CI evidence was independently read with `gh run view`: **Estudio PolyMind CI**, run **43469571976**, completed/success at this exact HEAD, created **2026-11-13T17:07:11Z**, updated **17:18:15Z**, elapsed **11m04s**. [Baseline CI run](https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/43469571976). It was not rerun or used as proof of the new implementation.

All **25 source hashes** in `tests/fixtures/digestion_contracts/managed_prompt11.json` match the committed inventory exactly. No accepted v11 inventory, generation digest, historical execution artifact, Phase 17 report, live approval or source/provenance contract was updated. A temporary edit of a frozen helper was detected by regression, removed exactly, and replaced with test-harness clock isolation; that failed intermediate run is recorded below.

No staging, commit, push, rebase, reset, clean, tag, remote mutation or cloud operation occurred.

## Implementation inventory

Ordinary `git diff --stat` excludes the new untracked files. The complete intended inventory is twelve changed tracked files, twenty-two new application/test/configuration files, and the two new Phase 18.2 Markdown artifacts. The 28 inherited files are separate.

| Changed tracked file | Function and compatibility impact |
|---|---|
| `.dockerignore` | Excludes Streamlit auth configuration, the supported private runtime directory, PEM/private-key files and browser outputs from the image context. Existing secret/database exclusions remain |
| `.gitignore` | Excludes private local Streamlit/runtime state and browser-generated outputs |
| `api/app.py` | Registers the fixed operator router before dynamic document routes; leaves runtime composition explicit and unconfigured operator access closed |
| `api/security.py` | Supports one ordered operator release guard at actual ASGI sends; moves blocking identity/SQLite handoffs off the event loop; preserves existing bearer, byte-limit, correlation and streaming behavior |
| `config/settings.py` | Adds explicit synthetic Documents UI profile and API address, rejects it in production, and suppresses implicit dotenv loading for that explicit profile |
| `documents/pilot/scheduling.py` | Accepts an optional trusted forecast timestamp; actual financial/provider admission still independently rechecks current state |
| `documents/pilot/service.py` | Uses one captured governance timestamp for the complete forecast, fixing a real-clock rejection of the first proposed call |
| `requirements.txt` | Pins only the narrow OIDC additions, `Authlib==1.9.5` and `joserfc==1.7.7`; existing cryptography is reused |
| `tests/conftest.py` | Anchors default reference job time once per pytest session and advances it by real monotonic elapsed time, avoiding backwards host-clock corrections in fast queue-draining fixtures. Explicit fake clocks and production clock source are untouched |
| `tests/unit/documents/test_pilot_controls.py` | Anchors the synthetic 18-call daily-budget schedule within one UTC day, preventing a midnight rollover from invalidating the assertion; runtime daily quota logic is unchanged |
| `tests/unit/publication/test_api.py` | Updates the old blanket prohibition on publication routes to permit the required operator route while continuing to forbid generic legacy publish/revoke/rollback routes |
| `ui/app.py` | Selects the dedicated Documents view only in the explicit synthetic profile; legacy Chat implementation remains intact |

| New file | Function |
|---|---|
| `api/operator.py` | Eleven approved typed contracts, strict extra-field rejection, canonical job UUID validation, sanitized pilot errors, current authorization and transport-release binding |
| `documents/operator/__init__.py` | Operator adapter package |
| `documents/operator/actions.py` | Private SQLite action intents/results, payload binding, accepted replay and fail-closed ambiguous-intent handling |
| `documents/operator/service.py` | Narrow enrolled-operator workflow, authorized projections, publication/Q&A replay, retention response, ordered release guard and single-lane runner |
| `development/__init__.py` | Explicit development adapter namespace |
| `development/document_demo/__init__.py` | Synthetic document composition package |
| `development/document_demo/__main__.py` | Explicit initialize/serve/identity/gateway/quiesced-backup lifecycle; strips inherited provider/security credential configuration; supervises and terminates scoped child processes |
| `development/document_demo/app.py` | Dedicated FastAPI fixture composition, process writer lock, document readiness and metrics; denies legacy query execution and direct analyze bypass |
| `development/document_demo/runtime.py` | One `SecurityRuntime` and exact shared authorities, existing extraction/jobs/pilot/publication/analysis composition, explicit v11 capabilities and fixed fixture approvals |
| `development/document_demo/fixtures.py` | Credential-free deterministic HTTP substitute, constant synthetic embedding model, private persistent synthetic vector adapter; no network fallback |
| `development/document_demo/identity.py` | Loopback test metadata/JWKS, one-time authorization codes, S256 PKCE, separate ID/API tokens and strict fixture operator token contract |
| `development/document_demo/provision.py` | Explicit first-time ephemeral test signing/TLS keys, private local secrets and synthetic identity configuration |
| `development/document_demo/gateway.py` | Local TLS/WebSocket boundary, exact host/origin restrictions, Secure cookie enforcement and sanitized unavailability |
| `docker-compose.documents.yml` | Separate single-host Compose entrypoint; only loopback TLS ports published, private runtime mount, UID 10001, read-only root and bounded scratch |
| `ui/documents_client.py` | Per-call bearer client, bounded connect/read timeouts, no redirects/retries, sanitized messages and response cleanup |
| `ui/documents.py` | Verified context/catalog, stable actions, reconnect, three-second status fragment, inert complete packet/evidence display, bounded question form and distinct lifecycle controls |
| `tests/unit/test_documents_client.py` | HTTP cleanup/confidentiality, strict requests, production rejection and recursive-backup refusal |
| `tests/unit/test_document_oidc_fixture.py` | Redirect/scope/protocol rejection and one-time code/client/PKCE binding |
| `tests/integration/test_document_operator.py` | Real signed-JWT/HTTP/authority/worker journey, negative authorization, replay, release races, restore, faults, readiness and conflict handling |
| `tests/browser/__init__.py` | Explicit optional browser harness namespace |
| `tests/browser/document_journey.py` | Actual Chromium/Streamlit/TLS/issuer/API/worker complete journey, isolated context, invalid callback state, origin denial, cancellation and logout |
| `tests/browser/oidc_nonce.py` | Actual native callback rejection of a correctly signed ID token with the wrong nonce |

The two Markdown additions are the [preserved prompt](../prompts/phase_18_2_implementation_and_verification.md) and this report. No routine debugging log, key, token, database, generated PDF, screenshot or protected runtime packet is added to Git.

## Architecture and protected runtime

The frontend remains Python/Streamlit and the API remains FastAPI. The common router is additive in `api.app`. The dedicated development entrypoint deliberately composes only the approved document plane: importing the legacy application would also instantiate its legacy graph/provider/memory infrastructure and could read unrelated configuration. The document entrypoint therefore reuses the security middleware/router and existing domain ports without constructing the legacy provider factory. This is an explicit local profile, not a production-validator bypass or second document pipeline.

`SecurityRuntime.authority`, `.governance` and `.admission` are supplied unchanged to `SupervisedPilot`, publication and selected-document analysis. Immutable objects, job/outbox/checkpoint truth, publication authority, pilot control and action mappings have distinct private paths. There is no parallel financial ledger or user-created allowance. `FileLock` excludes a second API/runner process for the same runtime. One worker thread belongs to that owning API process; it survives browser reruns and HTTP disconnects.

The runner reconciles recorded job state, uses the existing dispatch/lease/fence/manifest machinery and preserves the existing one-attempt policy. Its 120-second lease exceeds the bounded 60-second provider operation with a commit margin. It observes the durable shared provider window before stepping; status distinguishes `WAITING_ADMISSION`, active, idle and reconciliation-required conditions. It never runs from a GET/status request. Accepted checkpoints remain in the existing immutable object/job machinery; an interrupted claimed step may become terminal rather than receive an automatic new inference attempt.

Bearer authorization grants exist only in runner memory. Restart does not reload bearer tokens or silently authorize execution. The operator must authenticate and replay Start for the existing session/job to reauthorize a permitted continuation and explicit replica load. UNKNOWN or ACTIVE unresolved execution truth still blocks unsafe continuation. The runtime never recreates missing recorded authorities or clears consumed approvals to extend the demonstration.

Every operator route requires the verified principal, exact `(issuer, tenant, subject)` enrollment, user identity, `PUBLICATION_MANAGE` and exact owning pilot scope. Source and document identities come from server fixtures. Browser requests cannot choose ownership, paths, provider/model, prices, budgets, approvals, publication scope or privileges. Empty mutation bodies reject injected fields. Ordinary users and participant-facing privileged interfaces were not introduced.

The complete approved endpoint vocabulary is implemented. Session creation returns 201, accepted replay 200; Start queues/reuses one job and returns 202; Cancel returns 202 with honest in-flight liability; publication conflict returns 409. Q&A has a durable request-key/payload binding and returns the accepted answer on replay. Direct `/documents/analyze` remains unavailable in this profile, and legacy `/query` and `/query/stream` remain denied. Separately configured legacy/authorized analysis behavior is unchanged.

## Authentication and actual browser evidence

The mandatory early checkpoint was completed before the rest of the UI: installed **Streamlit 1.58.0** completed its native authorization-code callback through a loopback fixture issuer and TLS gateway, acquired a distinct **API-audience access token**, and passed the existing server JWT verifier. The API never authorizes from email, `st.user` identity claims or an ID token.

The issuer requires the exact registered client/redirect/scope, state and nonce, uses S256 PKCE and one-time short-lived codes, and signs separate ID and access tokens with ephemeral test RSA keys. API verification retains RS256/key/issuer/audience/purpose/nbf/exp checks. The fixture operator verifier additionally rejects app identities and extra roles without weakening the generic/Entra verifier. Exact enrollment and owning scope are enforced separately by the workflow. Unit/API negatives execute before document/provider effects.

Real Chromium verification uses the actual UI, native callback routes, HTTPS gateway, JWT-protected HTTP API and independent worker. It does not mock `st.user`, the OAuth callback or the document service. It verifies isolated browser contexts, unbound callback-state denial, cross-origin logout denial, native signed-token nonce mismatch denial, cookie clearing on logout and API-token expiry while an identity cookie remains valid.

Native Streamlit identity/token cookies are **signed, readable browser cookies**, not encrypted cookies or an opaque server-side session vault. The gateway enforces **Secure**, **HttpOnly** and **SameSite=Lax** on identity/token cookies. The XSRF cookie is Secure and intentionally JavaScript-readable for Streamlit's XSRF protocol. Native identity cookies can persist for 30 days; fixture API tokens expire after 900 seconds. Each protected rerender/action uses the API, so the shorter API/session authority remains decisive. Browser expiry testing retained the valid identity cookie, replaced only its API token with a correctly signed expired test token, and observed denial with no verified operator view. Tokens were absent from rendered body and browser localStorage.

Logout best-effort closes the current backend session before clearing native cookies and local state. It does not physically purge retained records or invalidate every previously copied bearer JWT; durable authority disable/epoch changes are the emergency revocation boundary. Previously delivered content cannot be recalled. Those native signed-cookie limitations remain unsuitable for an unreviewed public/confidential deployment.

Certificates and signing keys are generated under a private temporary runtime, never committed or baked into images. Browser harnesses allow the ephemeral self-signed certificate; server-to-server requests explicitly verify its test CA, and the container TLS check also verifies the certificate. No publicly trusted certificate, OS trust-store installation or live Entra tenant integration is claimed. Native CORS/XSRF protections remain enabled, with exact allowed origin and gateway host/WebSocket origin checks.

Authlib and joserfc were installed narrowly into the existing isolated Python environment with dependencies unchanged. Playwright/Chromium were installed only under `/tmp` as an optional verification harness. Authlib emits an upstream httpx-client deprecation warning in browser process logs; it did not fail authentication. No broad application/frontend dependency stack was added.

## Workflow, presentation and retention observations

The actual browser journey selected an authored synthetic technical text, created one approved session, started a durable job, observed progress through the three-second polling fragment, saw validated COMPLETE coverage 1, explicitly authorized publication, read original evidence and asked the authored valve-inspection question. The answer retained document/version/extraction/generation/span/line/excerpt identity and `semantic_support=not_evaluated`. The session was withdrawn with `PURGE_PENDING`, then logged out. A second authenticated session exercised Cancel, Close and Logout. Browser transport observation recorded zero external requests.

A separate browser fault run waited for durable admission, removed only that disposable runtime's plan object, and observed FAILED with no publication action. It then stopped and restarted the real local server processes, reconnected to the same recorded session, and verified unchanged consumed-session and financial records. Closure reported retained residuals rather than physical erasure. Another browser negative verified expiry and cross-origin denial. The supporting disposable driver/logs remain outside the repository; only sanitized observations are recorded here.

The new integration tests also complete the same source/job/digest/publication/question/closure journey over authenticated HTTP. Repeated create/start/publish/question actions do not create another accepted job/generation/provider execution. A mismatched payload with the same request key is denied. A crash after an action intent but before accepted-result association leaves reconciliation-required state; it never retries a possibly executed call. This conservative refusal is intentional, not a claim of autonomous recovery of unknowable results.

The UI renders model/source packets with inert `st.json`, including summary, findings, sections, synthesis claims, full coverage, qualifications, contradictions, limitations, open questions, evidence and canonical citations. It never treats structural citation validity as semantic entailment. PARTIAL/FAILED do not enable complete publication/presentation. Accepted answers are read back through a freshly authorized digest packet rather than retained in a global UI cache. Only opaque IDs and action keys are session-scoped. Clear Display, Cancel, Close, Withdraw, Logout and Stop are distinct operations.

Withdrawal/closure fence future protected presentation and preserve audit, financial, object, checkpoint, generation and action-result records. The adapter explicitly discloses retained private answer action records and projects the existing pilot inventory to retention categories. Financial tickets, provider-call rows and object/checkpoint identifiers remain in the trusted maintenance inventory and are not returned by Close. `PURGE_PENDING` does not mean source bytes, indexes, receipts, backups or upstream copies were physically erased. Synthetic fixture approvals are not participant consent, and no reviewer findings were fabricated.

## Actual response-send authorization and concurrency

Handlers capture current security/session/publication bindings and attach one ordered guard to actual ASGI response sends: **PilotControl session/configuration → SecurityAuthority snapshot → publication active generation/epoch**. It replaces the generic security-only guard for operator responses rather than nesting session locks inside a security transaction. There is no authority transaction across inference, extraction or a long upstream request.

The guard protects response headers and body handoff, with a five-second bounded send. A transport-specific denial bypasses endpoint exception-to-response handlers, so a denied release cannot be converted into a second protected response. If headers were already sent, the body is terminated without the protected packet. Separate tests revoke close/stop/document/permission/expiry/generation authority after preparation and before send; protected bytes are absent. Existing streaming revocation tests remain applicable.

Browser testing exposed synchronous SQLite lock waits blocking the event loop when a guard awaited transport. Authentication and complete guard ownership now run on worker threads, retaining each SQLite connection's thread affinity while sending through the originating event loop. Concurrent protected-request tests verify completion without the previous event-loop deadlock. This change preserves existing static/disabled and NDJSON behavior.

## Financial and provider verification

The runtime constructs only the deterministic fixture HTTP object and synthetic embedding/vector substitutes. It never imports production fixtures from `tests`, reads a real provider key, calls Azure, loads a real model as fallback or enables paid retries. The transport accepts only its exact fixture URL and increments an external-attempt counter before denying any other provider URL. Unit/integration network denial and browser request capture supplement that instrumentation. Public package/image/model-artifact downloads during dependency/build validation are separate from runtime provider execution.

Every synthetic synthesis/Q&A attempt still passes the existing pilot execution boundary, owning security snapshot, shared provider admission and governance reservation/settlement. The complete HTTP journey uses **three synthesis attempts plus one question**, four synthetic SETTLED records, zero unsettled records and zero external attempts. Fixture usage is **120 input / 160 output tokens** and local catalog arithmetic **EUR 0.000044**, explicitly synthetic and not a bill or measured model cost. The API projects only owning-scope totals, known settled usage/cost, unknown count and retained unsettled token/cost reservations. A separate exact-runtime check also asked an unsupported weather question, observed abstention with no citations, then obtained a supported valve citation: five total synthetic attempts, five settled records, zero external attempts, and accepted abstention replay without another call.

The unchanged policy preserves three total sessions, one open job/lane, 1 MB/four native pages/4,000 extracted characters, three synthesis attempts, three questions/six total attempts, 24,800 input and 3,000 output reservation limits, 60-second provider and 600-second workflow bounds. Existing tighter admission/capability limits apply. The global managed-prompt/10 default is unchanged; only this explicit workflow uses v11. Real execution permissions, quotas and historical consumed approvals were not renewed or reset.

## Reliability, failure and restore

Job truth is the existing SQLite ledger/outbox/checkpoint system, not the browser or an in-memory queue. Polling/readiness never invokes inference or publication. Browser reconnection uses an existing opaque session ID subject to fresh API authorization. Restart drops execution grants, preserves recorded jobs/actions/approvals and requires valid authorization before continuation. Missing authorities, truncated or uninitialized authority files, incompatible bindings, missing active generations/indexes and unresolved obligations fail closed. Reopen validates all seven SQLite authorities in read-only mode before invoking any reference constructor, preventing accidental initialization of truncated security or financial truth.

The tests cover queued cancellation, stop/close/withdrawal release races and existing in-flight settlement/UNKNOWN behavior. Cancellation cannot promise physical provider interruption or a refund; the UI/API disclose `MAY_COMPLETE_AND_BILL`. Stop writes durable denial before best-effort cancellation or acknowledgment. Expired leases/stale fences cannot commit newer results. Existing checkpoint compatibility and interrupted-publication tests are retained.

Coherent local restore tests copy a quiesced complete runtime, restore at the same absolute paths and verify consumed approval count, withdrawal, generation/security truth and settled reservations. No automatic database reset or budget renewal occurs. The supported backup command takes the same process lock as the API/runner and rejects destinations inside the runtime to prevent recursive copies. An arbitrary stale/incoherent snapshot is not authorized to roll back revocations or financial truth; reconcile retained evidence before reopening. Distributed disaster recovery and rollback-resistant external authority are not claimed.

## Verification results and T01–T15 disposition

There are **76 new pytest cases**: **29 unit** and **47 integration**, collected from the three new test modules. The two explicit repository browser harnesses and the supplementary browser fault/expiry/restart driver are reported separately, not added to pytest totals. Intermediate attempts are not added together as acceptance evidence.

The final frozen-tree command was:

```bash
python -m pytest -q -o junit_family=legacy --junitxml=/tmp/phase18-final-verification.xml --durations=10
```

| Final regression measure | Observed result |
|---|---|
| Complete suite | **3,128 passed** |
| Unit cases | **2,192 passed**, including 29 new cases |
| Integration cases | **936 passed**, including 47 new cases |
| Failures / errors / skips / pytest warnings | **0 / 0 / 0 / 0** |
| Pytest elapsed duration | **1,130.78 seconds (18m50.78s)** |
| JUnit suite duration | 1,130.696 seconds; timestamp `2026-11-14T01:12:26.139025+00:00` |
| Frozen source/test/configuration inventory | **397 files unchanged** through final verification and handoff |
| SHA-256 of serialized freeze manifest | `628b50100ede0b017961e4cf93db7c6f92630889fc9f5176c661d2fc248ae34c` |

The final log and JUnit artifact are `/tmp/phase18-final-verification.log` and `/tmp/phase18-final-verification.xml`; the hash inventory is `/tmp/phase18-final-verification-tree.json`. These are local disposable verification evidence, not committed runtime data. Only this report was finalized after source freeze. The final focused authority set passed all **76 new cases in 115.20 seconds**; the boundary set including the existing security middleware passed **87 cases in 96.63 seconds**. Those are separate rechecks of overlapping cases, not additional suite totals.

| Group | Evidence exercised | Final disposition |
|---|---|---|
| T01 Authentication | Native fixture login; existing generic/Entra signature, key, issuer, audience, purpose and time negatives; new exact enrollment, app-identity and extra-role denials before document/provider effects | PASS |
| T02 Browser/session | Real code callback, PKCE/code negatives, actual state/nonce rejection, Secure/HttpOnly/SameSite cookies, origin restrictions, isolated contexts, token confidentiality, expiry and logout | PASS |
| T03 Source eligibility | Real synthetic text/PDF intake; new catalog/body/injection/hash checks plus existing native parser, malformed/encrypted/scanned/layout/size/approval tests | PASS |
| T04 Durable actions | Accepted create/start/publish/question replay, payload conflict, pending intent interruption refusal, no duplicate inference/publication | PASS |
| T05 Worker recovery | Persisted status, fresh grant on reopen, browser disconnect/reconnect, actual server restart; existing outbox, checkpoint, lease/fence and compatibility tests | PASS |
| T06 Cancellation/stop | Real browser cancellation; HTTP queued controls; delayed ASGI revocation; existing running cancellation, durable stop and UNKNOWN liability tests | PASS |
| T07 Digest/provenance | COMPLETE/coverage gates and full inert packet; original canonical spans; forged/stale citation, qualification and PARTIAL/FAILED core tests; real failed browser view | PASS |
| T08 Selected Q&A | Real cited browser answer, HTTP accepted replay and direct-analyze denial; existing abstention/conflicting evidence/cross-owner/generation/revocation tests | PASS |
| T09 Finance/provider | Shared owning authorities, four synthetic settlements, projected usage, zero runtime provider network; existing budget/RPM/TPM/output/exclusive-attempt/UNKNOWN negatives | PASS |
| T10 Fault/recovery | Missing and truncated authority/object and malformed provider integration; missing-plan browser failure; existing DB lock/corruption, audit exhaustion, vector loss, activation/crash/replica and provider protocol/timeout/429 tests | PASS |
| T11 Privacy/restore | Actual withdrawal/PURGE_PENDING; coherent same-path restore with preserved consumption/financial truth; existing tombstone/UNKNOWN/restore tests | PASS |
| T12 UI/API | Complete actual Streamlit/API/worker journey and safe presentation; client timeout/cleanup/error contracts; unchanged legacy query/memory/NDJSON regression | PASS |
| T13 Container/deployment | Cached image build; UID 10001, private mounts, read-only root, TLS, readiness, denied unauthenticated access, writer exclusion and restart; Compose/Helm pass | PASS for required local contracts; conditional live Kind unavailable |
| T14 Operations | Healthy empty catalog, worker/admission wait, audit/financial/stale/publication failure signals; repeated health/status/readiness causes zero inference | PASS |
| T15 Authenticated E2E | Actual native login→source→durable job→COMPLETE→explicit publication→canonical citation→Q&A→withdrawal→logout; cancellation, expiry, isolation, FAILED/restart and delayed ASGI revocation | PASS |

The dedicated Kind context `kind-polymind-phase10` exists, but its loopback API refused connections. Only explicitly named read-only checks were attempted. The active context was the remote `epolymind-aks-dev`; it was not mutated or used as a fallback. Kind workload verification is therefore unavailable/conditional, not a fabricated PASS. No new cluster or Azure resource was created.

### Intermediate failures and corrections

An interrupted early regression recorded 370 passes, one generation-wire failure and 19 JUnit-format warnings in 402.31 seconds; it is not a full-suite result. A subsequent complete attempt recorded 3,114 passes and three failures in 906.84 seconds: a new fixture approval-time boundary, a historical queue-draining timing failure and the obsolete blanket publication-route assertion. The fixture and assertion were corrected without weakening runtime checks.

A temporary attempt to stabilize job time inside the historical preflight helper caused three exact v11 source-inventory failures: 3,115 passes/three failures in 882.04 seconds. The helper was restored exactly; accepted inventory/hashes were not edited. A first scoped test adapter incorrectly replaced a ledger class with a function and failed 16 crash-hook cases; retaining the class interface fixed those tests. Further queue-draining timing evidence motivated the final session-scoped, test-only monotonic UTC anchor in `tests/conftest.py`, preserving actual elapsed-time lease checks and explicitly injected clocks. Its initial unconditional document import broke a copied minimal configuration-only subprocess; the fixture now only patches an already-loaded document module, and 130 focused configuration/lease/client/auth tests passed. Session scope also covers module-level historical replay fixture setup, which precedes function-scoped fixtures. Production clock source remains unchanged.

A later complete application-tree run recorded **3,120 passes / one failure in 962.12 seconds**. The sole failure was the pre-existing daily-budget test scheduling 18 calls across UTC midnight and therefore incorrectly expecting a single-day ceiling rejection. The test schedule is now anchored at the next UTC midnight; neither daily budget logic nor any allowance was changed. Its focused calendar/auth/client/configuration verification passed **53 tests in 4.18 seconds**. A subsequent full attempt recorded 3,085 passes and 36 setup errors in 802.61 seconds: all 36 shared one historical module fixture that still used the unpatched wall clock before function setup. The isolated case passed in 24.53 seconds. Session-wide test clock installation fixes that setup ordering while retaining actual elapsed time, explicit test clocks and every frozen source hash. The final full run below uses that final fixture tree.

These attempts and isolated rechecks are diagnostic history, not a sum of passing tests. The final acceptance result below supersedes them on the final frozen tree.

## Deployment/configuration and safe local commands

The supported modes are legacy local Chat, explicit synthetic local Documents, and the existing production profile. Synthetic execution is rejected under production settings and by the development entrypoint itself. This phase does not make the historical Helm query-plane chart an OIDC document deployment.

The normal isolated Python environment now includes the two pinned OIDC packages. From the repository root, choose a **new private runtime outside the source tree**:

```bash
python -m development.document_demo initialize /tmp/polymind-documents
python -m development.document_demo serve /tmp/polymind-documents
```

Open `https://localhost:9443` and trust only this runtime's ephemeral `tls.crt` for local testing. The synthetic issuer is on loopback TLS 9444; API 8001 and Streamlit 8501 bind to loopback and are not intended as browser entrypoints. Ctrl-C/SIGTERM supervises shutdown of the scoped children. Restart uses the same Serve command and state path, with fresh operator authorization for work. Initialize refuses an existing runtime; it never resets the cohort. Source/session fixture approvals expire after roughly one hour, API tokens after 15 minutes and test TLS after two days.

For a quiesced snapshot, first stop the runtime and reconcile any UNKNOWN/in-flight records, then choose a new destination outside it:

```bash
python -m development.document_demo backup /tmp/polymind-documents --destination /tmp/polymind-documents-snapshot
```

Restore all authorities/objects/action records coherently at the original absolute path. Do not copy individual ledgers, mix epochs or restore an older allowance as new spend authority.

The separate Compose file leaves `docker-compose.yml` intact. Container initialization must use the **final container path** `/runtime/state`, because authority bindings intentionally include absolute paths. Choose a **new empty** dedicated parent directory; the ownership command below is restricted to that mount. Do not substitute an unrelated existing directory. Build and initialize with ordinary cache:

```bash
export DOCUMENT_DEMO_ROOT=/tmp/polymind-documents-container
mkdir -p "$DOCUMENT_DEMO_ROOT"
docker compose -f docker-compose.documents.yml build
docker compose -f docker-compose.documents.yml run --rm --no-deps --workdir /app --user 0 documents chown 10001:10001 /runtime
docker compose -f docker-compose.documents.yml run --rm --no-deps --workdir /app documents python -m development.document_demo initialize /runtime/state
```

The first initializer runs only the scoped mount-ownership operation. Actual authority initialization runs as UID 10001. Start, restart and stop the same runtime with:

```bash
docker compose -f docker-compose.documents.yml up -d
docker compose -f docker-compose.documents.yml restart
docker compose -f docker-compose.documents.yml down
```

Only `127.0.0.1:9443` and `127.0.0.1:9444` are published. API, Streamlit internals, databases, objects and derived indexes have no published management ports. The read-only image runs as `10001:10001`; `/tmp` is a 64 MB UID-owned tmpfs. The runtime mount contains separate identity/TLS configuration and private object/security/governance/admission/jobs/pilot/action/publication/index paths. No Redis or Chroma server is exposed by this profile.

Validation used a temporary Compose image-ID override to reuse the already built image without creating an extra validation tag. The project-specific validation service was started, inspected, restarted, checked again and shut down; its dedicated private bind state was retained. No global prune, image deletion, unrelated container/volume deletion or `--no-cache` build occurred.

## Review, limitations and Stage 18.3 handoff

Implementation review examined all changed/new application files, consumers of shared interfaces, route ordering, privilege boundaries, action concurrency, cancellation/UNKNOWN settlement, thread/connection ownership, process shutdown, immutable identities, error paths and legacy compatibility. It fixed the forecast timestamp race, event-loop release deadlock, response-denial exception handling, strict fixture token role/purpose behavior, UUID/conflict response contracts, explicit admission-wait status, owning financial projection, minimized closure inventory, truncated-authority reinitialization hazard and recursive backup hazard.

A separate pre-commit review is recorded in the final validation addendum. It checks secrets/keys/tokens, actual environment files, private data, absolute local paths, databases/generated artifacts, debug/dead code, accidental dependencies, public management routes, historical-file preservation and index/Git state. Static analysis runs the Ruff F rules on the changed Python surface; no unconfigured global formatter or unsupported security certification is claimed.

Remaining limits are intentional: synthetic deterministic language/embedding/ranking fixtures do not establish real-model semantic quality; native signed browser cookies are not a production BFF/vault; real Entra enrollment and Azure VM deployment remain unverified; this is one host/one owning operator with conservative manual reconciliation, not distributed HA/DR or public multi-tenant reliability. Full physical erasure, sensitive sources, public exposure and external-user acceptance remain excluded. Previously delivered content cannot be recalled. Test TLS and automatic fixture login are development-only.

Stage 18.3 should document the implemented startup, TLS trust/auth posture, API/error contracts, mount initialization, approved data/limits, stop/restart/restore/retention procedures, exact final test evidence and operational restrictions. It should update README and appropriate security/deployment/architecture runbooks only to implemented behavior and collect the operator's administrative closure decision. No Stage 18.3 closure, external review, deployment or paid inference has begun here.

The classifications remain unchanged:

```text
PHASE_17_ENGINEERING_COMPLETE
DEFERRED_PENDING_TWO_INDEPENDENT_REVIEWERS
PHASE_17_FORMAL_CLOSURE_PENDING
PHASE_17I_ENGINEERING_COMPLETE
PHASE_17I_EXTERNAL_VERIFICATION_DEFERRED
PHASE_17I_FORMAL_ACCEPTANCE_PENDING
SUBSEQUENT_ENGINEERING_PERMITTED
```

Independent human reviews remain **0/2**. Local synthetic browser evidence does not replace Phase 17I external-user verification.

## Final validation addendum

The source freeze and final complete regression described above passed. The actual final browser log, `/tmp/phase18-final-verification-browser.log`, records `auth=true`, `complete_journey=true`, `browser_isolation=true`, `cancel=true` and `external_browser_requests=0`. The separate native nonce harness denied a correctly signed mismatched nonce without installing authentication cookies. The supplementary browser evidence records API-token expiry denial, token absence from body/localStorage, cross-origin denial, FAILED rather than COMPLETE after a missing plan, actual server restart/reconnection, preserved consumed-session/financial truth, `PURGE_PENDING` and logout denial. Delayed-response revocation is separately verified at the real ASGI send boundary in integration tests.

Ruff F checks on all changed/new Python files, compilation using an external bytecode cache, original and Documents Compose configuration, Helm lint and Helm template all passed. Helm's optional chart-icon recommendation is informational. No unrelated global formatting, live Kind workload or cloud deployment result is asserted. The only browser-runtime dependency warning observed was the Authlib upstream deprecation described above; pytest's final result had no warnings.

The final normal cached image build produced **`sha256:dd4f92ee54358761999f299cbbdb66ccdd23115c6c7f37991b934d77965253cf`**, **3,042,328,251 bytes**, configured user **`10001:10001`**. Its network-disabled/read-only-root smoke initialized and reopened the synthetic runtime, confirmed secret exclusion and zero provider attempts, and refused a deliberately truncated disposable governance authority without recreating it. The final Compose TLS/readiness check reported healthy idle with an empty publication catalog, denied unauthenticated context with the normalized category/correlation contract, rejected a concurrent writer, confirmed private SQLite permissions, and reopened the preserved authorities after restart. The scoped Compose container/network was shut down; private bind state was retained. No unrelated resources were changed.

The separate final pre-commit inspection covered **36 intended files: 12 tracked changes and 24 new files** (22 application/test/configuration files plus prompt/report). It found no embedded private key, JWT, real environment file, unintended runtime database, hard-coded home path, application import from `tests`, or new-file whitespace defect. Manual review additionally covered safe output/logging, fixed-route ordering, dependency scope, privilege exposure, cleanup and error paths. All **28 inherited Phase 17H files**, all **25 frozen v11 sources**, and all **397 source-freeze files** still match their recorded SHA-256 values. The final review inventory is `/tmp/phase18-final-precommit-review.json`.

Final Git checks: HEAD remains `f0e420b6a4ab479ffaa166d000d55c91164f154b`; `git diff --check` passes; `git diff --cached --name-only` is empty. `git status --short --branch` shows `master...origin/master`, the twelve intended tracked changes and the intended new files alongside the 28 preserved historical untracked files. The ordinary tracked `git diff --stat` is **12 files changed, 109 insertions, 16 deletions**; it excludes the explicitly enumerated new files. Nothing was staged, committed or pushed.

Suggested operator-reviewed commit message only:

```text
feat(documents): implement authenticated local document frontend and verification
```

Final classifications:

```text
PHASE_18_2_ENGINEERING_PASS
PHASE_18_2_LOCAL_INTEGRATION_PASS
PHASE_18_2_OFFLINE_VERIFICATION_PASS
AKS_NOT_REQUIRED
PHASE_18_3_DOCUMENTATION_PENDING
PRODUCTION_READINESS_NOT_ESTABLISHED
```
