# Phase 18 implemented operator API

Reconciled 14 November 2026 against `f7d091ad16a458c4d4a7403e3fe3ad2b47fafc67`. Sources: [router and request DTOs](../../api/operator.py), [workflow and runner](../../documents/operator/service.py), [action persistence](../../documents/operator/actions.py), [pilot](../../documents/pilot/service.py), [middleware](../../api/security.py) and [dedicated application](../../development/document_demo/app.py). This is the current contract for the synthetic Documents composition. The [operator guide](phase_18_local_document_demo.md) describes setup, trust and recovery.

## Common authentication, authorization and release

All eleven routes require one `Authorization: Bearer <API access token>` header verified server-side. Missing/malformed/duplicate/expired/invalid credentials produce 401 (`WWW-Authenticate: Bearer`). A verified token is then checked against exact enrolled `(issuer, tenant_identity, subject)`, user kind, `PUBLICATION_MANAGE` and owning pilot scope. Session UUIDs are owner-filtered; document ownership/current security and active publication generation apply where relevant. A UUID is not authorization. Ordinary users receive no publication-management access.

All paths below have prefix **`/documents/operator`**. Every `{session_id}` is parsed as a UUID. No request may supply owner, tenant, principal, source bytes/path/URL, provider/model, quota, price, approval object, role or publication scope. Mutation DTOs use strict types and `extra="forbid"`. Start, Cancel and Stop accept an omitted/null body or `{}`; any extra object field is invalid. Bodies are bounded by the dedicated API's **8,192-byte** actual/declared request limit, even when an individual field permits 4,096 characters. This differs from the legacy application's configurable default 1 MiB boundary.

Success responses are JSON with `Cache-Control: no-store` and correlated `X-Request-ID`. Bodies below enumerate actual fields; responses are assembled dictionaries rather than a declared Pydantic response model. Route success does not bypass release revalidation: the ASGI guard checks pilot config/session epoch, security snapshot and recorded publication generation/epoch in that order. A revocation before release denies bytes. Once headers have started, denial terminates the body; clients must not treat an incomplete response as successful completion. Previously delivered data cannot be recalled.

## Endpoint contracts

### GET `/context` — 200

No input body. Returns `owner_id`, `tenant_id` (canonical UUID strings), `expires` (principal expiry epoch seconds), `enrolled=true`, `mode="SYNTHETIC_FIXTURE"`, `limits` (PilotPolicy), `stopped` (boolean) and `allowed_actions`.

Normally context actions are `select`, `start`, `publish`, `question`, `cancel`, `close`, `withdraw`, `stop`. Stopped context has `inspect`, `close`, `withdraw`, `stop`. These are a projection, not an authorization grant. Repeat reads perform no document/provider work; authentication can register/revalidate the principal and append required audit. Current enrollment/permission/scope or release failure denies access; security outage fails closed.

### GET `/sources` — 200

No input body. Returns an array of `source_approval_id`, `name`, `type` (MIME), `sha256`, `classification`, `expires` (ISO timestamp), `eligible` and `limits`. The development catalog contains two authored synthetic PDF/text choices. `eligible` checks the source approval time window, not whether sessions/budget/deadlines are available. Repeat reads do not run extraction or inference; no arbitrary filesystem listing or protected source bytes are returned. Common authentication/authorization/release and availability errors apply.

### POST `/sessions` — 201 new / 200 accepted replay

Required body: `source_approval_id` (1–128 characters matching `^[A-Za-z0-9_./:-]+$`) and `request_key` (16–128 characters matching `^[A-Za-z0-9_-]+$`). Approval IDs must still exist in the server catalog; the regex is not a filesystem-path interface.

Returns `session_id`, `source_id`, `state="OPEN"`. The owner/action/key/payload binding is recorded in `actions.sqlite` before selection effects. The server chooses an unused preprovisioned session approval, enforces session/open-job/source limits, consumes it, extracts exact approved bytes, registers the document and persists extraction/plan/immutable inventory. No provider call occurs here. Same accepted source/key returns the same result; changed payload on that key is 409. A pending intent, including one left by failed intake, is 409 reconciliation-required rather than automatic retry. Source refusal is 422; unavailable/expired/invalid approval can be 409, exhausted sessions/limits 429, stopped pilot 403. Release checks the newly created active session and security state.

### POST `/sessions/{session_id}/start` — 202

Empty/omitted body. Returns `job_id`, `state` (current durable job state). A new Start validates the persisted plan and worst-case capacity forecast, admits a job/outbox/steps under stable `pilot/{session_id}` idempotency, stores execution authorization/deadline and grants the runner the current principal in memory. It does not perform the complete digestion in the request. Same session reuses the job; restart replay supplies a fresh in-memory grant and explicitly reloads an existing permitted generation. It never extends the original deadline or retries a terminal/uncertain call.

Active session/source/current owning document authority and release checks apply. Missing plan/replica is 503; state/binding/uncertainty conflict 409; stop 403; new-job forecast/limit refusal 429. An existing-job Start replay can return 202 even when the runner will subsequently refuse execution because of deadline or unresolved obligations. It is not a recovery clearance. Accepted Start can precede a release/replica-load failure; inspect durable status rather than creating a new session as a recovery shortcut.

### GET `/sessions/{session_id}` — 200

No input body. Returns the authoritative projection below. It permits inspection with `active=False`, so a valid enrolled operator may inspect terminal/expired/stopped workflow state; it still requires current security and publication release bindings. Repeated reads perform no worker step, inference, index load, publication or settlement. Audit/authority reads still occur. Missing/foreign session or binding conflict is 409/403 as appropriate; object/ledger failures are sanitized and can be 503. A stale active publication can deny status release even for retained session state.

| Fields | Exact meaning |
| --- | --- |
| `session_id`, `session_state` | OPEN/CLOSED/WITHDRAWN/STOPPED/EXPIRED projection; stop/expiry may be derived from control facts |
| `operator`, `participant`, `document`, `execution`, `result` | Pilot labels: `OPERATOR_AUTHENTICATED`, `PARTICIPANT_SESSION_APPROVED`, `DOCUMENT_APPROVED`/`DOCUMENT_APPROVAL_EXPIRED`, `NOT_AUTHORIZED`/`EXECUTION_AUTHORIZED`/`RETAINED_RESULT_NO_NEW_EXECUTION`, `NOT_READY`/`RESULT_READY`/`SESSION_CLOSED`. The participant label is fixture vocabulary, not actual consent or a real participant |
| `job_id`, `generation` | Nullable recorded durable identities |
| `job_state`, `progress` | Present once a job exists; progress fields `total`, `completed`, `running`, `retrying`, `failed`, `cancelled`, `pending`, `current_stage` |
| `digest_status`, `coverage` | Where available: COMPLETE/PARTIAL/FAILED; coverage fields `schema_version`, `eligible`, `analyzed`, `failed`, `skipped`, `unsupported`, `included`, `fraction`. FAILED/CANCELLED jobs project `digest_status="FAILED"` |
| `source_id`, `source_sha256`, `limits`, `questions_used` | Server-approved source and PilotPolicy/consumed question count |
| `authorization_expiry` | Minimum of principal and session-approval expiry, epoch seconds; does not claim cookie expiry |
| `semantic_support`, `retention` | `not_evaluated`, `RETAINED_BY_POLICY` |
| `last_update`, `steps` | Present with a job; ISO job update time and array of `{stage,state}` |
| `outcome`, `retry_eligible`, `allowed_actions` | Outcome prefers digest status, then job state, then session state; `retry_eligible=false`. Close/withdraw always projected, start/cancel for OPEN, publish for COMPLETE, question for a recorded generation below the question ceiling. Server checks remain decisive |
| `worker` | Process runner outcome: IDLE/ACTIVE/WAITING_ADMISSION/RECONCILIATION_REQUIRED; not durable job truth |
| `usage` | Owning-scope aggregate across the ledger, not only this session: `synthetic`, `attempts`, `currency`, `unsettled`, `unknown`, `measured_input_tokens`, `measured_output_tokens`, `measured_cost`, `unsettled_reserved_tokens`, `unsettled_reserved_cost`; decimal costs are strings. No raw tickets or provider rows |

### POST `/sessions/{session_id}/publish` — 200

Required body: `expected_job_id` matching the 36-character lowercase UUID-shaped pattern and valid UUID parsing. Returns `generation`, `state="PUBLISHED"`.

Requires that exact session job, validated COMPLETE and coverage fraction 1. The server records a publish intent keyed by session/expected job, plans/prepares/activates a generation using authorized publication, stores generation/epoch/evidence fingerprint and explicitly loads presentation. The accepted replay returns its original generation only if still active. Job mismatch or replacement-generation conflict is 409; pending intent 409 reconciliation-required; incomplete/missing digest or stale/missing replica 503; active-session/source/security/limits errors apply. A failed request can leave candidate/activation effects; do not blindly republish. Release checks the current session and recorded generation/epoch.

### GET `/sessions/{session_id}/digest` — 200

No input body. Requires active session/source/document authority, COMPLETE/coverage 1 and a loaded matching active generation. Returns `document_id`, `source_sha256`, `generation`, `digest_version`, `evidence_sha256`, `status`, `coverage`, `findings`, `executive_summary`, `sections`, `synthesis_claims`, `evidence`, `qualifications`, `contradictions`, `limitations`, `open_questions`, `citations`, `semantic_support`, `verification` and `answers`.

`evidence` entries contain `evidence_id`, `reference` (canonical EvidenceRef), `excerpt`, `physical_page`. `verification="SYNTHETIC_FIXTURE"`; `semantic_support="not_evaluated"`. `answers` contains up to three accepted private action answer records for this session; any answer-generation mismatch refuses the packet. The exact nested immutable digest types are in [digestion models](../../documents/digestion/models.py), source/evidence/span types in [canonical models](../../documents/models.py), and Citation in [retrieval](../../documents/publication/retrieval.py).

Citation fields are `citation_id`, `generation`, `record_id`, `document_id`, `document_version_id`, `extraction_id`, `display_source`, nullable `physical_page`, `span`, `structural_path`, `excerpt`, `provenance="validated"`, `semantic_support="not_evaluated"`. No object-store export/raw-source download endpoint is created. Reads do not regenerate or load indexes. Missing/incomplete/stale evidence is unavailable (typically 503); closure/stop/revocation deny release. Final guards apply to the entire packet and prior accepted answers.

### POST `/sessions/{session_id}/questions` — 200

Required body: `query` (1–4,096 characters) and `request_key` with the create-key constraints. Returns `generation`, `answer`, `evidence_status`, `citations`, `semantic_support`, `limitations` and adapter-assigned `answer_id`. Evidence outcomes are `available`, `insufficient`, `conflicting`, `incomplete`; insufficient evidence is a successful abstention, not an HTTP error. `limitations` explicitly describes selected excerpts and unestablished entailment.

New execution requires active execution authorization/deadline, question ceiling, selected document and current loaded publication. Server derives selected IDs and uses `AuthorizedAnalysis` with the same authority/governance/admission through `PilotProvider`; no unbounded model access. A new submission increments the question counter before analysis; a no-hit abstention need not call the provider. Questions are synchronous rather than queued behind the runner's 61-second spacing check, so early/rapid submissions can be denied by the shared reservation window and leave a pending action intent. Accepted result is durably stored in the action table, then released under fresh guards. Same accepted key/query reuses the answer without another call or a new execution-deadline/question-limit check, but still requires an active permitted session and current generation/release checks. Changed query is 409; pending/uncertain intent is 409 reconciliation-required. Limit/financial/provider-admission failures can be 429 or sanitized 503 depending on the underlying domain error. Expired/closed/revoked/stale generation denies output. Previously accepted answer existence does not override current permission.

### POST `/sessions/{session_id}/cancel` — 202

Empty/omitted body. Returns `state="CANCEL_REQUESTED"`, `may_complete_and_bill=true`, even when no job is recorded. Requires owning operator/session with `active=False` and, for a job, `AuthorizedJobs.cancel` using document-delete authorization. Repeated cancellation requests fence eligible work without creating a new job; response is not terminal-job confirmation. Durable job cancellation/fences may change, session need not close. No physical provider interruption/refund is promised. Common scope/security/release and job availability errors apply.

### POST `/sessions/{session_id}/close` — 200

Required body: strict boolean `withdrawal`. Returns `state` (actual terminal state), `retention="PURGE_PENDING"`, `physical_erasure=false`, `residuals`, `unsettled_execution_intents` and `adapter_answers="RETAINED_PRIVATE_ACTION_RECORDS"`.

Requires current owning operator/session with `active=False`. Session denial/epoch is committed before eligible job cancellation. Repeats preserve the first CLOSED/WITHDRAWN state; switching the flag does not rewrite the original classification. Cancellation/inventory failure can return an error after closure is already durable. Each residual includes only available `class`, `state`, `custodian`, `location`, `reason`, `deadline`; no raw object IDs, tickets or provider call records. Current session/security/publication release guards remain in effect. Retained audit/financial/artifact/action state is not erased. Common denial/unavailability errors apply; a failure is not evidence that the session stayed OPEN.

### POST `/stop` — 200

Empty/omitted body. Returns `state="PILOT_STOPPED"`, `cancellation_reconciliation_required` (failure count), `in_flight_usage="MAY_COMPLETE_AND_BILL"`, `refund_claimed=false`.

Requires the enrolled owning operator; no session ID. Persists global pilot stopped flag/configuration epoch and STOPPED session transitions before best-effort cancellation. Repeats remain stopped but advance the stop epoch/audit where capacity permits; this is safe repetition, not byte-identical idempotency. No inference/refund/shutdown of unrelated services. Missing authorities can fail closed without an acknowledgment. The final configuration/security guard protects the response. There is no browser endpoint to clear stop or reset allowances.

## Failure categories and profile distinctions

| Status | Dedicated Documents response category / meaning |
| --- | --- |
| 401 | `authentication_required`; invalid/missing/expired bearer, including duplicate headers |
| 403 | `access_denied` or SecurityError category; `pilot_stopped` for closed/stopped active operations; final-release denial |
| 409 | `pilot_denied` (state/replay/job/generation conflict), `pilot_reconciliation_required` (pending/uncertain action) |
| 413 | `request_too_large` at ASGI actual/declared byte boundary |
| 422 | `invalid_request` for DTO/path validation; `pilot_source_refused` for refused approved-source intake |
| 429 | `pilot_limit` or `admission_denied` for GovernanceError |
| 503 | `pilot_not_ready`, `security_unavailable`, `service_unavailable`; missing objects/index/authorities/protocol or other domain failures are sanitized through their actual boundary |

Operator errors normally contain `detail`, `category`, `request_id`; no upstream body, private paths or stack traces. Correlation is also in `X-Request-ID`. The dedicated catch-all is sanitized 503; no stable mapping of every lower-level exception to a proposed-design category is promised. No `retry_after_seconds` field or generic automatic retry contract was added. `DocumentsClient` maps status to fixed messages, uses connect/read timeouts `(3,65)`, follows no redirects, performs no automatic retry and closes responses. It does not display server error bodies.

The operator router is also registered in `api.app`, before dynamic document routes, but the default legacy app does not create `operator_workflow` or the runner. Shared-app exception envelopes differ from the dedicated composition (some contain `detail` only). This reference must not be used to assert that simply adding OIDC settings creates a deployed Documents service.

Existing `/query`, `/query/stream` NDJSON, memory, shares/deletion, `/usage` and separately composed authorized-analysis contracts are unchanged. The synthetic entrypoint exposes no memory/share/admin routes; `/query` and `/query/stream` are denied (403 in this composition), and authenticated direct `/documents/analyze` returns 503 with a session-question instruction. The existing `AnalysisRequest` was not extended and upstream SSE is not forwarded as PolyMind NDJSON. There is no upload, permission-management, settlement, publication rollback or raw-authority HTTP endpoint in this operator surface.
