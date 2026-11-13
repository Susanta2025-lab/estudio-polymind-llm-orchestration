# Phase 17I — Stage 2 Implementation and Verification

12 November 2026. Authority: [Stage 2 master prompt record](../prompts/phase_17i_implementation_and_verification.md). Scope: **Option A — Private, Operator-Supervised Local Verification**. This report records implementation and offline verification, not Stage 3 documentation finalization or official Phase 17I closure.

## Engineering disposition

**`PHASE_17I_ENGINEERING_PASS`** within the implemented bounded, single-host supervised scope.

**`PHASE_17I_OFFLINE_VERIFICATION_PASS`** — final frozen-tree regression: **3,052 passed**, including **2,163 unit / 889 integration**, zero failures/errors/skips and no warnings reported. This includes **56 new Phase 17I cases** (27 unit / 29 integration) and the extended existing sharing-attribution assertions. These engineering verdicts do not authorize real participation or new inference spending.

External-user verification remains `PHASE_17I_EXTERNAL_USER_VERIFICATION_PENDING`. Production remains `PRODUCTION_READINESS_NOT_ESTABLISHED`. Historical Phase 17 engineering remains complete; its semantic obligation is `DEFERRED_PENDING_TWO_INDEPENDENT_REVIEWERS`, **0/2**, and formal closure remains pending. No new participant, independent human review, actual-model quality measurement, live execution or production acceptance is claimed.

Initial and final committed HEAD: **`69c8f6642f95c88911bc1feeca01ee51cbf04bda`**. Initial tracked/index diffs were empty. There were 28 inherited untracked Phase 17H documents, preserved separately from this task. Read-only Git inspection verified the five-commit history and baseline. `gh run view 43280974288` independently returned Estudio PolyMind CI, completed/success, with this exact HEAD. CI was not rerun and does not authorize exposure or paid execution.

## Implemented workflow and architecture

The new `documents.pilot.SupervisedPilot` is a trusted local operator facade. It takes an existing verified principal and existing security, object, job, publication, financial and provider-admission authorities. It creates no HTTP route, participant identity or provider transport/factory. All participant interaction is a selected, guarded presentation controlled by the operator. The [operator workflow and GO/NO-GO packet](../../evaluation/phase_17i_operator_workflow.md) explains composition and use; [blank record templates](../../evaluation/phase_17i_record_templates.json) deliberately contain null approvals and fail validation until reviewed/completed.

The functional path is approved source → bounded intake/extraction → fixed durable job → managed v11 synthesis → validated COMPLETE digest/receipts → authorized publication → selected retrieval/Q&A/canonical citations → inert presentation → structured feedback → closure/withdrawal/revocation/inventory. Tests exercise that composition rather than disconnected replacements. Existing FastAPI/Streamlit/LangGraph/RAG, Ollama/OpenAI-compatible provider contracts, legacy NDJSON behavior and OIDC restrictions remain intact.

The module responsibilities are deliberately narrow:

| Module | Delivered interface/control |
| --- | --- |
| `models.py` | Frozen versioned pilot policy, source/session approvals, consent distinction, structured feedback and exact-output reviewer records |
| `control.py` | Existing private SQLite foundation reused for session epochs, stop state, operational intents, write inventory, feedback and review records; no independent monetary ledger |
| `intake.py` | Hash/owner/type/rights allowlist, byte/page/character eligibility, extraction and durable object-write intents including orphans |
| `parser.py` | Existing native pypdf runner in a supervised POSIX subprocess, resource limits, write/side-effect denial, bounded output and sanitized failures |
| `execution.py` | Existing GovernedExecution wrapped by pilot scope/model/capability/call/deadline checks and serial shared admission; financial settlement remains in GovernanceLedger |
| `scheduling.py` | Read-only conservative schedule forecast using the actual supplied policy/catalog/history and provider authority; no reservation, quota reset or spending permission |
| `service.py` | Operator session creation, intake, start/resume/step/status, publication/replica load, guarded presentation/Q&A, review packets/findings, stop/closure/withdrawal, metadata retirement and trusted reconciliation observation |
| `retention.py` | Nineteen lifecycle classes, actual object observations, accepted/orphan intent associations, generations/vectors, financial/provider observations and explicit residuals |
| `presentation.py` | Plain inert local text representation; no HTML/Markdown evaluation or terminal control interpretation |

The authenticated operator must own the selected document scope and possess publication-management permission. A participant code grants no API identity or operator privileges. Source approval binds exact document/hash, rights/classification, provider-processing permission, reviewed native-text eligibility, operator and validity interval. Session approval separately binds notice, purpose, study code, consent status/timestamp, source, retention and authorization references. Synthetic fixtures cannot claim actual consent. Real external-mode records require separate privacy, quality and exposure references; no such real approvals were obtained.

Limits are configurable downward: at most three total sessions, one open session/document job, four native PDF pages or UTF-8 text, 1,000,000 source bytes, 4,000 extracted characters, three synthesis attempts, three questions and six total provider attempts per document, with no provider retry/fallback. Managed profiles explicitly select v11; the global v10 default is unchanged. The tested profile limits serialized managed input to 24,600 units plus 200 overhead/safety units, fitting the pilot's 24,800 complete input reservation, with 3,000 output tokens. Existing model/context, complete-child, response, extraction and publication constraints still apply; these limits do not guarantee every document under four pages is eligible.

Parser bounds are 10 seconds wall, 5 seconds CPU, 512 MiB address space, 256,000 output bytes and a 2 MiB file-size backstop. Native parsing needs no scratch writes: Python filesystem writes, process launch and socket side effects are denied in the child. The parent reaps the child and removes its normal private temporary directory. This is resource containment for native parsing, **not** a syscall/container sandbox against arbitrary compromised native code. Curated operator screening remains necessary for essential columns, tables, formulas and graphics that native extraction cannot reliably classify. Global extraction behavior is unchanged.

Provider execution has an explicit 60-second request timeout and a 600-second cooperative workflow admission deadline, including Q&A. This is not an established end-to-end latency SLO or forced preemption of all local embedding/publication work. The default permission path permits only marked deterministic providers and synthetic sessions. External/paid execution requires an independently reviewed permission hook that enforces exact current authorization before reservation and again before execution. No real credential acquisition, live probe, operator-key signing, live approval consumption or new paid launcher was implemented or used. Existing cryptographic signing/replay fixtures remain synthetic test-only behavior.

For unchanged retained evidence, `associate_retained` requires an explicit approved digest-object hash, reconstructs the accepted source/plan/receipt/G1/G2 graph through existing publication verification and rechecks pilot eligibility. It grants no new inference allowance. Historical financial/provider rows remain linked in the inventory. Tests exercise correct versus wrong digest pins without another provider call. No historical private v11 artifacts were reopened or modified; the runner provides a protected reuse/review capability when the operator supplies approved evidence access.

## Security, accounting and recovery evidence

All service entries revalidate the verified operator; selection is server-derived and foreign-owner/tenant requests fail before source/result release or provider work. Session expiry, principal disable, withdrawal, stop, missing storage/vectors and stale generation deny release. Publication binding includes both generation **and epoch**, preventing ABA rollback from restoring a session. The final local sink is guarded by session, security and publication transactions. Already delivered bytes cannot be recalled. Sinks must be synchronous, bounded and non-reentrant; this is an operator runner, not a general remote streaming transport.

Publication uses `AuthorizedPublication`, and Q&A uses `AuthorizedAnalysis`. Replica/BM25 loading is an explicit operator/startup operation, never an automatic serving-time rebuild. Digest presentation includes executive synthesis, findings, qualifications/conflicts, coverage, limitations, original evidence IDs/spans and canonical PDF pages/text lines. Citation validity continues to report `semantic_support=not_evaluated`; it does not establish entailment. New external Q&A is held privately until separate exact-answer expert reviews exist. Two digest reviews cannot authorize a subsequently generated answer. Dummy review/consent-shaped records in tests are explicitly synthetic and count as zero real reviews/consents.

The only existing runtime-interface change is an optional `exclusive=False` keyword on `SQLiteInferenceAdmission.acquire`. Opt-in pilot calls require no other active quota request; updated ordinary callers also defer while an exclusive call is active. It uses the same transaction, quota key/policy/table and reservation history, without schema migration or new capacity. Existing calls retain default behavior. The active `unknown_exclusive` marker is overwritten on normal settlement; a crash leaves it active. All shared consumers must run the updated code before this behavior is relied on; old running binaries cannot enforce it.

Owner/tenant financial reservations, prices, RPM/TPM/output reservations, known/UNKNOWN settlement, duplicate admission and budget checks remain in the existing governance/admission implementations. Forged owner/tenant CallIdentity is rejected before financial rows/provider calls. The extended existing sharing test proves interactive costs belong to the requesting grantee; governed background tests and pilot composition prove exact owner attribution once. Study codes do not become financial principals.

Initial execution preflight forecasts the complete six-call envelope against the supplied current authority state. The standalone study forecast rejects 18 same-window requests under the 16-request policy, and independently rejects 500,400 daily units under the 500,000 cap. An explicit fixture schedule of 12 calls followed by six at least 86,400 seconds later fits with otherwise empty eligible fixture history. The implementation uses strict `created > at-window_seconds` request semantics and UTC day/month token/cost boundaries, including historical rows; no assumption that midnight resets rolling requests is made. Forecasts do not reserve capacity. Real ledgers/capacity/pricing were not inspected or changed; any actual plan must be rerun against its intended authorities and separately approved.

Stop is durable before best-effort cancellation and remains durable when pilot audit capacity is full. Pilot admission and publication activation serialize against stop acknowledgment. Tests stop between financial reservation and provider admission, observe RELEASED unstarted accounting and zero provider observations, and also stop during known/unknown in-flight work. Incurred known cost remains settled; UNKNOWN stays reserved and blocks pilot continuation across restart. No timeout/TTL implies a refund. Trusted reconciliation only observes already reconciled terminal financial/provider state plus an operator quiescence reference; it never invents usage or settles money. Reopening intake cannot reopen a stopped session or replay its attempt.

Restore tests use consistent SQLite snapshots **after** acknowledged stop/tombstone/settlement, plus object unavailability/restoration. They preserve revocation and exact usage. They do not certify arbitrary stale backups, hostile-host rollback, multi-host recovery, automatic two-lease recovery or upstream cancellation.

## Privacy and residual-retention boundary

The inventory accounts for sources, extraction, jobs, steps, provider receipts, checkpoints, digests, publication generations, vectors, sparse state, temporary processing, presentation data, feedback, audits, usage/reservations, backups, upstream copies, conversation memory and participant metadata. Write intents precede immutable writes; failed/unaccepted objects remain visible as conservative residuals. Object integrity/presence, accepted association and operational/financial/provider state are distinguished. Unknown storage, scratch/process copies, backups and provider custody are not relabeled deleted.

Closing/withdrawing revokes presentation and fences eligible work without deleting shared immutable sources, vectors or accepted generations. Private metadata/feedback/review/held-answer rows can be logically redacted after their approved metadata retention deadline. SQLite freelists, backups and external copies are unverified, so the result remains **`PURGE_PENDING`**, never a physical erasure certificate. Real participant records stay outside Git; no automatic retention timer or legally approved privacy procedure is claimed. Nonpersonal retained-artifact approval and participant-metadata handling require qualified acceptance before exposure. Documents demanding stronger erasure are refused.

The operator inventory supplies exact local references and scope, explicit custodian/location/deadline categories, and unknown/uncontrolled states. Actual backup/provider policies, archive locations, display/export cleanup and class-specific operated responsibilities remain external decisions. This bounded inventory is not a universal physical reference graph or deletion adapter.

## Verification and synthetic rehearsal

The final full suite executed after all Python changes and source freeze. JUnit xunit1 file attributes independently partition its 3,052 cases into 2,163 unit and 889 integration cases. The initial separate group runs are recorded as intermediate snapshots below, not misrepresented as final-tree standalone runs. No test was skipped or weakened. Counts overlap and must not be added together.

| Executed validation | Exact outcome / scope |
| --- | --- |
| Initial `python -m pytest tests/unit -q --junitxml=...` | 2,161 passed in 347.19 s; 67 legacy xunit2 `record_property` reporting warnings; predates two final added unit cases and recovery review |
| Initial `python -m pytest tests/integration -q --junitxml=...` | 884 passed, 1 failed in 806.98 s; 89 xunit2 reporting warnings; expected transitive source-fingerprint refusal during editing, before the final four added integration cases |
| Exact previously blocked observability case, isolated | 1 passed in 1.07 s; original security assertion unchanged |
| Phase 17I focused checkpoint | 56 passed in 97.91 s; recovery refinement subsequently checked with the exact missing/empty-storage case plus all new unit controls: 28 passed in 16.61 s |
| **Final `python -m pytest -q -o junit_family=xunit1 --junitxml=/tmp/phase17i-full-final.xml`** | **3,052 passed in 960.00 s (JUnit 959.917 s); 2,163 unit / 889 integration; 0 failures, 0 errors, 0 skips, 0 warnings reported** |
| Final compilation | `PYTHONPYCACHEPREFIX=/tmp/phase17i-bytecode-verified python -m compileall -q .` — exit 0 |
| New Python lint and format | Ruff checks pass for all 15 new Python files; all 15 already formatted |
| Existing modified Python critical lint | `ruff check --select E9,F63,F7,F82 llm/admission.py tests/unit/publication/test_security.py` — PASS |
| Markdown/record templates | New/current links and fragments checked; exactly three formal plan stages; JSON valid, null-filled approval records intentionally fail validation |
| Git/source preservation | Diff checks pass; 17 intended Python-file hashes unchanged across final regression; 28 inherited hashes unchanged during final review; empty staged diff; HEAD unchanged |

Newly added tests cover N1–N15; N7 also extends existing sharing attribution and reuses governed background tests. Existing identity, authority, legacy OIDC refusal, graph, provider, job/fencing, publication, source/lineage/receipt and financial suites remain regression coverage.

| Requirement | Evidence |
| --- | --- |
| N1 | Named verified-operator/approved-session test; invalid consent/external/participant-code records refused |
| N2 | Named intake test, 12 variants: hash, type, rights, personal class, bytes, characters, page count, scan, graphics, path, owner and model; explicit overhead preflight test |
| N3 | Named same-owner/tenant denial tests for digest, question and review evidence |
| N4 | Named reset/expiry/disable cases; no prepared or prior-session release |
| N5 | Named stale generation/tombstone/vector-loss cases; generation/epoch binding and final release guards |
| N6 | Named forged-owner and forged-tenant identity tests: zero financial reservations/provider calls |
| N7 | Extended existing authorized-sharing test plus governed background and pilot settled-owner assertions |
| N8 | Named source/query injection test and forged-citation refusal; existing no-tool/derived-child tests reused; actual-model resilience remains unestablished |
| N9 | Named wall/CPU/memory/disk/output child-fault cases, verified exit/termination mechanisms, actual native PDF and malformed input |
| N10 | Named known/UNKNOWN in-flight stop tests, restart/fence denial, trusted fixture reconciliation, reservation-to-admission stop test and audit-exhaustion stop |
| N11 | Named active document/six-call/three-question tests, zero-budget preflight, durable cohort cap and shared admission exclusivity/replay checks |
| N12 | Named 19-class inventory/orphan test, financial/provider record linkage and honest unknown residuals |
| N13 | Named withdrawal test and metadata-retirement deadline/redaction test; no physical purge claim |
| N14 | Named failed-status/sanitized-error test, explicit partial-output refusal, actual COMPLETE presentation and abstention contracts |
| N15 | Named storage-loss/restoration test and consistent post-stop SQLite restore/tombstone/usage drill |

The standalone `python -m tests.performance.pilot_dry_run` authors a four-page synthetic PDF and executes real local extraction, durable jobs, explicit v11 wire/receipt/G1/G2 validation, governed admission/settlement, authorized publication, selected Q&A, canonical citations, presentation, structured feedback and closure. The HTTP provider response, embeddings and reranking are deterministic substitutes. It measures application behavior, not actual model semantics or participant usefulness.

Observed rehearsal: **COMPLETE**, coverage **1.0**, **4** fake provider calls / **4** settled rows, **0** outstanding reservations, **1** canonical Q&A citation, session **CLOSED**, **PURGE_PENDING**, **0 billable calls**, **0 human reviews**. Read-only reconciliation of the synthetic rehearsal verifies 120 input / 160 output units, three background rows and one interactive row, four inactive provider observations and EUR 0.000044 under the explicitly synthetic catalog. This is test arithmetic, not paid usage or a current provider price. The tests also exercise text-line citations and all four original physical PDF pages. Protected runtime artifacts are outside Git in the task's temporary evidence directories; no private actual-participant content is included.

## Implementation review and separate pre-commit review

Implementation review corrected separate synthesis/Q&A capability selection, complete-input overhead accounting, idempotent workflow startup, publication manifest write-intent coverage, sparse-replica loading, publication epoch/ABA binding, stop/admission/activation ordering, stop durability under audit exhaustion, exact-answer expert gating, metadata redaction and truthful residual custody/deadlines. A later recovery review identified that the shared SQLite base could silently initialize missing/empty pilot storage. Explicit first-time initialization and fail-closed live/reopen checks now prevent that loss of withdrawal history. Tests cover missing storage, initialized restore, empty-file rejection and refusal to initialize an existing authority. No security assertion was weakened and no existing semantic/provenance gate was removed.

The first broad integration run had one expected source-fingerprint refusal because implementation edits were still changing Python files while a launcher fixture revalidated its transitive implementation digest. This was an execution-method mistake: the guard correctly blocked before provider work. The isolated exact case passed once sources were stable. A subsequent full run was deliberately interrupted at approximately 58% to repair the missing-control-authority defect found during review; that incomplete run is not counted as a regression pass. The interrupted log was preserved. Python sources were frozen again for final regression; the test and fingerprint guard were not changed. Earlier xunit2 runs produced legacy `record_property` reporting warnings; final evidence uses compatible xunit1 without suppressing tests or warnings.

The separate pre-commit pass reviews the complete tracked diff and all intended untracked modules/tests/documents for credentials/keys, real participant content, hard-coded host paths, unprotected routes, filesystem scope, new dependencies, raw content logging, unapproved execution, stale caches, deletion and historical changes. AST/critical lint, new-source lint/format, sensitive-literal/route checks and frozen-source hash verification support that review. It is a second review pass by the same agent, not an independent human or second-agent audit or certification.

## G01–G16 reconciliation

These classifications concern the original [risk register](../../evaluation/phase_17i_external_user_readiness_gates.md), whose assessment snapshot is preserved. Local software evidence does not approve privacy, human quality or external execution.

| Gate | Stage 2 disposition | Evidence and remaining decision |
| --- | --- | --- |
| G01 Authentication | PARTIAL | Verified operator/session boundary and expiry/disable tested; actual supervised admission and security/operator acceptance remain pending. Participant identity-provider enrollment is outside A. |
| G02 Authorization | PASS — ENGINEERING VERIFIED | Scoped runner, canonical selected retrieval, foreign/session denial, epoch/revocation and guarded release verified in local composition. This is not exposure approval. |
| G03 Consent/rights | BLOCKED — APPROVAL OR EXTERNAL EVIDENCE REQUIRED | Versioned records and invalid/unapproved denials implemented; no real consent, rights-holder or notice approval obtained. |
| G04 Privacy/provider transmission | BLOCKED — APPROVAL OR EXTERNAL EVIDENCE REQUIRED | Minimal private records, structured feedback and retention tooling exist; controller/terms/region/transfer/qualified privacy decisions absent. |
| G05 Physical deletion | PARTIAL | Logical revocation/redaction, inventory and erasure-class refusal verified; physical deletion remains PURGE_PENDING and retained-artifact policy needs acceptance. |
| G06 Expert quality | BLOCKED — APPROVAL OR EXTERNAL EVIDENCE REQUIRED | Exact-output packets/findings/answer gates exist; real qualified reviews remain 0/2 and semantic acceptance is not inferred. |
| G07 Provenance/support | PARTIAL | Exact canonical identity/page/text-span and source integrity verified; representative relevance/entailment still requires reviewers. |
| G08 Injection | PARTIAL | Scope/tools/citation authority cannot be changed by fixture source/query data; actual-model adversarial evidence remains pending. |
| G09 Reliability | PARTIAL | Bounded parser, native PDF/text, failure/resource/restore tests pass within the local scope; actual cohort 3/3 timing and representative model limits are unmeasured. |
| G10 Finance | BLOCKED — APPROVAL OR EXTERNAL EVIDENCE REQUIRED | Identity, attribution, quota/budget/schedule/UNKNOWN controls verified offline; no current real capacity/pricing/headroom or new execution approval obtained. |
| G11 Operations | PARTIAL | Stop/cancel/fencing/restart/reconciliation drills implemented; named real responder, supervision and escalation acceptance remain pending. |
| G12 Deployment/exposure | PARTIAL | No participant listener/routes, infrastructure or public ingress added; actual private host/display/egress boundary requires operator/security approval. B/C deployment is not applicable to A. |
| G13 Audit/custody | PARTIAL | Bounded content-free audit, object/call linkage, sanitized feedback and exhaustion denial verified; operated custody/archive/retention acceptance absent. |
| G14 Cleanup | PARTIAL | Executable closure/withdrawal/redaction/inventory and restore denial tested; uncontrolled copies and accepted residual policy remain pending. |
| G15 Usefulness | PARTIAL | Functional assisted workflow and feedback instrument verified synthetically; no real participant usefulness/notice-understanding evidence. |
| G16 External authority | BLOCKED — APPROVAL OR EXTERNAL EVIDENCE REQUIRED | This instruction authorizes Stage 2 engineering only. External participation/exposure and any exact new paid execution remain separately unapproved. |

## Operator handoff and remaining limitations

Separate decisions remain: engineering acceptance of this diff/tests/reference scope; independent expert-quality acceptance/adjudication; exact document and provider-processing permission; privacy/notice/metadata and artifact-retention approval; cohort/session/window and named operator approval; exact financial/capacity/signing authorization if inference is proposed; external-user execution/exposure approval; and future Stage 3 documentation/closure authorization. The [operator packet](../../evaluation/phase_17i_operator_workflow.md#draft-approval-and-notice-fields--not-approved-templates) records these as pending/NO-GO.

The engineering implementation supports bounded supervised verification; it does not provide a public or self-service participant service, distributed authorities, OCR/layout understanding, arbitrary uploads, automatic recovery/retention scheduling, provider/backup physical erasure, actual semantic quality or production readiness. A future real-provider composition must integrate its independently authorized execution permission; default fixtures are deliberately unusable for external inference. Genuine external feedback remains required for Phase 17I acceptance. No next phase or Stage 3 closure was started.

## Git disposition and exact file inventory

No staging, commit, push, branch/history change, quota/catalog migration/reset, live provider call/probe, real credential/key access, cloud/Kubernetes mutation, Docker build, participant contact or real consent collection occurred. Docker/Compose/Helm checks are not applicable to unchanged deployment behavior and were not run. No dependencies were added or installed. No standalone configured repository type-check gate was found; none is claimed passed.

Final Git command outputs and the exact file inventory follow. The three-stage planning structure is reconciled; Stage 3 documentation and closure remains explicitly unstarted. Suggested operator commit message:

```text
feat(pilot): implement bounded supervised Phase 17I verification workflow
```

### Intended changes (separate from inherited files)

Modified tracked files (3):

```text
docs/evaluation/phase_17i_implementation_and_verification_plan.md
llm/admission.py
tests/unit/publication/test_security.py
```

New Phase 17I files (19):

```text
docs/codex/prompts/phase_17i_implementation_and_verification.md
docs/codex/reports/phase_17i_implementation_and_verification.md
docs/evaluation/phase_17i_operator_workflow.md
docs/evaluation/phase_17i_record_templates.json
documents/pilot/__init__.py
documents/pilot/control.py
documents/pilot/execution.py
documents/pilot/intake.py
documents/pilot/models.py
documents/pilot/parser.py
documents/pilot/presentation.py
documents/pilot/retention.py
documents/pilot/scheduling.py
documents/pilot/service.py
tests/integration/test_supervised_pilot.py
tests/performance/pilot_dry_run.py
tests/pilot_helpers.py
tests/pilot_parser_probe.py
tests/unit/documents/test_pilot_controls.py
```

Inherited untracked Phase 17H documents (28), outside this change set:

```text
docs/codex/prompts/phase_17h_current_authorization_and_token_headroom_assessment.md
docs/codex/prompts/phase_17h_final_approval_signing_and_controlled_execution.md
docs/codex/prompts/phase_17h_v10_authentication_renewal_and_final_operator_packet_preparation.md
docs/codex/prompts/phase_17h_v10_final_operator_verification_and_conditional_live_execution.md
docs/codex/prompts/phase_17h_v10_operator_preparation_and_readiness_assessment.md
docs/codex/prompts/phase_17h_v5_authorized_catalog_migration_and_commercial_reconciliation.md
docs/codex/prompts/phase_17h_v5_complete_financial_readiness_and_operator_preparation.md
docs/codex/prompts/phase_17h_v5_execution_window_renewal_and_rsa_authorization.md
docs/codex/prompts/phase_17h_v5_final_operator_preparation_continuation.md
docs/codex/prompts/phase_17h_v5_financial_reconciliation_and_second_four_call_readiness.md
docs/codex/prompts/phase_17h_v5_four_call_readiness_reassessment.md
docs/codex/prompts/phase_17h_v5_operator_preparation_signing_and_controlled_execution.md
docs/codex/prompts/phase_17h_v8_azure_operator_preparation_and_signing_readiness.md
docs/codex/reports/phase_17h_current_authorization_and_token_headroom_assessment.md
docs/codex/reports/phase_17h_final_approval_signing_and_controlled_execution.md
docs/codex/reports/phase_17h_live_invalid_qualification_source_root_cause.md
docs/codex/reports/phase_17h_v10_authentication_renewal_and_final_operator_packet_preparation.md
docs/codex/reports/phase_17h_v10_final_operator_verification_and_conditional_live_execution.md
docs/codex/reports/phase_17h_v10_final_signing_and_controlled_live_outcome.md
docs/codex/reports/phase_17h_v10_operator_preparation_and_readiness_assessment.md
docs/codex/reports/phase_17h_v5_authorized_catalog_migration_and_commercial_reconciliation.md
docs/codex/reports/phase_17h_v5_complete_financial_readiness_and_operator_preparation.md
docs/codex/reports/phase_17h_v5_execution_window_renewal_and_rsa_authorization.md
docs/codex/reports/phase_17h_v5_final_operator_preparation_continuation.md
docs/codex/reports/phase_17h_v5_financial_reconciliation_and_second_four_call_readiness.md
docs/codex/reports/phase_17h_v5_four_call_readiness_reassessment.md
docs/codex/reports/phase_17h_v5_operator_preparation_signing_and_controlled_execution.md
docs/codex/reports/phase_17h_v8_azure_operator_preparation_and_signing_readiness.md
```

### Final Git commands

The tracked diff statistic excludes the 19 untracked Phase 17I additions listed above. The 28 inherited files are excluded from the proposed commit.

`git status --short --branch` — exit 0:

```text
## master...origin/master
 M docs/evaluation/phase_17i_implementation_and_verification_plan.md
 M llm/admission.py
 M tests/unit/publication/test_security.py
?? docs/codex/prompts/phase_17h_current_authorization_and_token_headroom_assessment.md
?? docs/codex/prompts/phase_17h_final_approval_signing_and_controlled_execution.md
?? docs/codex/prompts/phase_17h_v10_authentication_renewal_and_final_operator_packet_preparation.md
?? docs/codex/prompts/phase_17h_v10_final_operator_verification_and_conditional_live_execution.md
?? docs/codex/prompts/phase_17h_v10_operator_preparation_and_readiness_assessment.md
?? docs/codex/prompts/phase_17h_v5_authorized_catalog_migration_and_commercial_reconciliation.md
?? docs/codex/prompts/phase_17h_v5_complete_financial_readiness_and_operator_preparation.md
?? docs/codex/prompts/phase_17h_v5_execution_window_renewal_and_rsa_authorization.md
?? docs/codex/prompts/phase_17h_v5_final_operator_preparation_continuation.md
?? docs/codex/prompts/phase_17h_v5_financial_reconciliation_and_second_four_call_readiness.md
?? docs/codex/prompts/phase_17h_v5_four_call_readiness_reassessment.md
?? docs/codex/prompts/phase_17h_v5_operator_preparation_signing_and_controlled_execution.md
?? docs/codex/prompts/phase_17h_v8_azure_operator_preparation_and_signing_readiness.md
?? docs/codex/prompts/phase_17i_implementation_and_verification.md
?? docs/codex/reports/phase_17h_current_authorization_and_token_headroom_assessment.md
?? docs/codex/reports/phase_17h_final_approval_signing_and_controlled_execution.md
?? docs/codex/reports/phase_17h_live_invalid_qualification_source_root_cause.md
?? docs/codex/reports/phase_17h_v10_authentication_renewal_and_final_operator_packet_preparation.md
?? docs/codex/reports/phase_17h_v10_final_operator_verification_and_conditional_live_execution.md
?? docs/codex/reports/phase_17h_v10_final_signing_and_controlled_live_outcome.md
?? docs/codex/reports/phase_17h_v10_operator_preparation_and_readiness_assessment.md
?? docs/codex/reports/phase_17h_v5_authorized_catalog_migration_and_commercial_reconciliation.md
?? docs/codex/reports/phase_17h_v5_complete_financial_readiness_and_operator_preparation.md
?? docs/codex/reports/phase_17h_v5_execution_window_renewal_and_rsa_authorization.md
?? docs/codex/reports/phase_17h_v5_final_operator_preparation_continuation.md
?? docs/codex/reports/phase_17h_v5_financial_reconciliation_and_second_four_call_readiness.md
?? docs/codex/reports/phase_17h_v5_four_call_readiness_reassessment.md
?? docs/codex/reports/phase_17h_v5_operator_preparation_signing_and_controlled_execution.md
?? docs/codex/reports/phase_17h_v8_azure_operator_preparation_and_signing_readiness.md
?? docs/codex/reports/phase_17i_implementation_and_verification.md
?? docs/evaluation/phase_17i_operator_workflow.md
?? docs/evaluation/phase_17i_record_templates.json
?? documents/pilot/
?? tests/integration/test_supervised_pilot.py
?? tests/performance/pilot_dry_run.py
?? tests/pilot_helpers.py
?? tests/pilot_parser_probe.py
?? tests/unit/documents/test_pilot_controls.py
```

`git diff --check` — exit 0:

```text
(no output)
```

`git diff --stat` — exit 0:

```text
 ...ase_17i_implementation_and_verification_plan.md | 46 ++++++++++++++--------
 llm/admission.py                                   | 10 +++--
 tests/unit/publication/test_security.py            |  6 +++
 3 files changed, 41 insertions(+), 21 deletions(-)
```

`git diff --cached --name-only` — exit 0:

```text
(no output)
```

`git rev-parse HEAD` — exit 0:

```text
69c8f6642f95c88911bc1feeca01ee51cbf04bda
```

### Final preservation and review result

The final second-pass check verified 19 new files for whitespace, private-key/credential-URL/home-path literals and unintended artifacts; all 17 intended Python hashes match the frozen regression tree. The 28 inherited untracked document hashes remain unchanged through handoff, and the tracked diff contains only the three intended paths. All 16 gate rows are present, the current plan has exactly three formal stages, and both blank approval templates are rejected by their actual validators. Markdown targets/fragments resolve. These are bounded engineering/heuristic checks, not legal approval or security certification.

**No commit or push occurred. All 22 Phase 17I files remain unstaged/uncommitted for operator review. Stage 2 stops here; Stage 3 remains future work. External-user verification, historical human semantic acceptance and production readiness remain pending/unestablished.**
