# Phase 17H-L — single-call execution failure diagnosis

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

Diagnosis date: 2026-10-17. Scope: read-only, offline investigation of the supplied final configuration and approval. The only repository addition made by this task is this report.

## A. Root-cause conclusion

**PARTIAL — FAILURE BOUNDARY IDENTIFIED; ROOT CAUSE REQUIRES ADDITIONAL EVIDENCE**

The exact original exception cannot be recovered from the available artifacts. No failed prerequisite was demonstrated for the historical invocation. In particular, the configured audit directory is the packet's `audit/` directory, not another directory. Configuration validation, the configuration digest, current executor binding, RSA signature, approval audience, and reconstructed signed binding all pass offline checks.

The evidence places the failure before a completed, durable security authorization and before provider inference for this configured execution. It does not select one exact failing function within that boundary. `main()` in `tests/performance/foundry_single_call.py:320–322` discards the original exception. The original command, exact invocation timestamp, runtime environment, and any traceback are unavailable in the inspected evidence. Operator-reported signing and launch steps are distinguished below from directly verified artifacts.

**Provider classification: CONFIRMED — Failure before provider inference**, for the supplied configuration and its job, using the combined audit, security, admission, financial and replay evidence described below. This is not an Azure-wide request-count or billing assertion, nor proof about a command using a different configuration. It assumes the existing durable evidence has not been removed; no evidence of removal was found.

An important reproducible boundary is `SingleCallConfiguration.require_live_window()` at `tests/performance/foundry_single_call.py:114–117`: the invocation must start before **2026-10-16 23:59:00 UTC**, because more than 600 seconds must remain. Approval expiration at **2026-10-17 00:09:00 UTC** is not the launch cutoff. This is a conditional explanation, not an established root cause. Current expiration cannot prove historical expiration.

## B. Execution timeline

All times here are UTC; Lisbon was UTC+1 on these dates. File modification times are corroborating filesystem metadata, not execution logs.

| Time | Evidence and interpretation |
| --- | --- |
| 2026-10-16 17:52:10 | Configured audit directory's modification time; it remains empty. |
| 2026-10-16 23:34:49 (`1792193689`) | Existing sanitized authentication evidence records `VERIFIED`, signature/audience/issuer/lifetime/scope/role checks, registered-operator match and governance-policy match. |
| 2026-10-16 23:39:00 (`1792193940`) | Configured execution window begins. |
| 2026-10-16 23:39:01 | Final configuration and unsigned-review modification times. Review records verification at `1792193941`; approval `iat` and `nbf` are also `1792193941`. These signed times were prepared before signing and do not identify invocation time. |
| 2026-10-16 23:44:04.290271 | Signed approval file modification time. Its signature verifies against the existing trusted RSA public key. |
| Unknown | Operator reports loading both environment variables, independently signing/verifying, and invoking the launcher once, receiving the generic failure. No precise invocation time or exact executed command was available. |
| 2026-10-16 23:59:00 (`1792195140`) | Latest-window rejection begins: remaining lifetime is exactly 600 seconds. |
| 2026-10-17 00:09:00 (`1792195740`) | Approval expiration and configured credential-use deadline. Authentication mode is `api_key`; the latter is the configured use deadline, not independently measured Azure key expiration. |
| 2026-10-17 00:43:46 (`1792197826`) | Expiration recorded for the operator token used during preparation. This does not prove the same token was supplied during launch. |

The authentication evidence file is `/tmp/polymind-auth-window-1792193940-evidence.json`. Its producing script was inspected as source, not executed. It verifies identity and existing authority membership before preparing the review; it does not prove successful verification in the later launcher process.

## C. Execution-stage evidence

The last directly proven successful preparation stage is production of a correctly signed approval for the matching final configuration. No successful stage inside the original `launch()` invocation is directly logged. The first missing expected durable checkpoint is the authorization event generated by `SecurityAuthority.authorize()` (`security/authority.py:140–159`), called at launcher line 255. Both allowed and ordinarily denied authorization append an event. There are no security events at or after the window start. A failure opening or committing the authority transaction could also leave no event, so absence does not prove that `authorize()` was never entered.

| Candidate / exact source boundary | Observed and expected condition | Finding / exception category |
| --- | --- | --- |
| Configuration loading and executor binding: `foundry_single_call.py:86–105,294` | Actual `SingleCallConfiguration.model_validate_json()` succeeds. Current executor digest is `5624647a3f1a0fb559c85ca0ca06997320d42f9585b7528055505c12dbcca10f`, matching configuration. Generation/schema and capacity validators pass. | No reproducible configuration validation failure. A different file or historical source state remains unverified. |
| Window: `require_live_window()`, lines 108–117; called at 245 | All nine attestations are present. Expected start is at/after `1792193940`, with deadline strictly greater than invocation time plus 600 seconds, and adequate attested capacity. | Synthetic clock checks pass at `1792193940`, `1792194240`, `1792195139`; fail at `1792193939`, `1792195140`, `1792195740` with `SecurityError('unsupported_execution')`. Original invocation time unknown. |
| Private paths: `foundry_approval.private_path()`, lines 42–54; launcher 246–248 | All three configured authority files and the configured audit directory pass actual read-only private-path validation. Directory is mode 0700. | No present path discrepancy or permission-validator failure. Historical transient filesystem errors cannot be reconstructed. |
| Credential presence: launcher 249–250 | Nonblank credential is required. Runtime environment values were not retained or inspected. | Operator reports loading it; original presence cannot be independently established. Failure would be `SecurityError('authentication_required')`. |
| Acknowledgement/digest: `foundry_l1.verify_approval()`, lines 114–116 | Actual model digest exactly equals `46691c43bd45374bf5812da1474fd33b45aeb52f67ef5796b1d94ab9b9e5709d`, as do review and signed binding. | No artifact mismatch. Actual `--approve-sha256` argument remains unknown. Mismatch would be `SecurityError('access_denied')`. |
| Entra verification: `security/identity.py:145–196`, reached from `foundry_l1.py:117` | Preparation evidence reports valid token and matching identity. Launcher creates a fresh verifier; `_key()` can fetch JWKS through `_fetch()` (lines 83–140). | No launcher-time token or JWKS/transport evidence. Fresh preparation authentication does not rule out later token/header/expiry/network failure. These are normalized to `SecurityError('authentication_required')`. No OIDC network verification was attempted during diagnosis. |
| Signed approval: `foundry_approval.verify_artifact()`, lines 102–132 | Header exactly matches expected RS256/type/key ID. Signature, fixed issuer and strict audience `polymind-single-analysis-live` verify. Payload equals reviewed payload. Canonical binding hash matches review; rebuilding `bindings()` from configuration and review identity matches the signed binding. Trust identity and derived scope match. Replay directory lies outside audit directory. | Static checks pass. Signature verification explicitly disabled only historical `exp`/`iat`/`nbf` time enforcement; it is not a current authorization. Invocation-time checks remain unknown. Rejection would be `SecurityError('access_denied')`. |
| Registered authorization: `security/authority.py:95–104,140–159` | Read-only principal row matches review identity, tenant, user kind and exactly `PUBLICATION_MANAGE`; disabled is false. Security schema and version match source; `quick_check` is `ok`; audit contains 19 rows, far below default limit. | No static authority defect found. No authority constructor or authorization method was invoked, because these can write. No authorization event exists for this window. |
| Fixture: launcher 256–258 / `prepare_analysis()` 120–145 | Expected generated fixture/request hashes must match configuration. Actual audit directory has no `objects/` output. | Not established as reached; no fixture mismatch demonstrated. The helper writes object storage, so it was not run against private artifacts. A diagnostic attempt to find a `fixture` field in `first-stage.json` raised `KeyError`; inspection confirmed this is a request document, not a manifest. That diagnostic error is unrelated to the launcher failure. |
| Governance construction: launcher 259–262 | Occurs after authorization and fixture preparation. Model-level authority bindings already validate. | No evidence this stage was reached. Constructors were not invoked and no migration or admission was attempted. |
| Replay guard and consumption: launcher 263–268 | Requires no prior guard calls/live marker; then verifies and consumes approval before writing live-start marker. | No run database, live marker or matching consumption marker exists. No reproducible replay rejection for this approval. |

The original exception class and exact failed validation are therefore **unresolved**. Window, acknowledgement, runtime credentials, OIDC retrieval/verification, and an early filesystem/authority transaction failure remain distinguishable possibilities, not diagnoses. No speculative source fix is justified.

## D. Approval and replay state

Private packet:

`<PRIVATE_OPERATOR_DIRECTORY>/`

The actual configuration field is:

`<PRIVATE_AUDIT_DIRECTORY>`

This is exactly the earlier inspected packet audit directory. It contains no entries: no `run.sqlite`, `live-started.json`, `outcome.json`, `CANCEL` or generated objects.

The actual trust references `<PRIVATE_REPLAY_DIRECTORY>`. There is no `<HISTORICAL_APPROVAL_ID>.consumed.json`. Three other approval-consumption markers remain present; they were not removed or treated as consumption of this approval. `consume()` creates an exclusive marker before inference and does not roll it back. Available evidence therefore shows this approval **unconsumed**, not reusable: its authorization is historical and expired.

## E. Provider and financial state

The configuration references these existing authorities, all under `<PRIVATE_AUTHORITY_DIRECTORY>/`:

| Authority | Read-only findings |
| --- | --- |
| `security.sqlite` | 19 audit rows; latest timestamp `1792141167.9793065`. Zero events at/after `1792193940`. Registered principal and schema checks pass. |
| `provider.sqlite` | Three older admission records: two `success`, one `output_limit`; all inactive. Zero records for configured job `<HISTORICAL_JOB_ID>`; zero records at/after window start. Latest timestamp `1792141158.8578022`. |
| `governance.sqlite` | Three older reservations, all `SETTLED`. Zero reservations for the configured job; zero reservations or events at/after window start. Latest reservation timestamp `1792141158.8424346`. No unresolved reservations anywhere in this authority. |

The prior settled actual costs remain EUR `0.00699907602956752`, `0.00890113516367529`, and `0.005006599788807204`. They belong to earlier activity and must not be attributed to this failed launch. There is no reservation, settlement, provider admission or local financial obligation attributable to this job. No Azure billing API was queried, and these records are not a statement about unrelated Azure charges.

The inference path requires financial reservation, then RunGuard/provider admission, before provider execution (`governance/execution.py:30–45`). The configured job has **zero recorded provider attempts**, with no RunGuard database or live-start marker and no security authorization event. Combined with absent approval consumption, these independent prerequisites establish failure before inference through this execution contract. The conclusion does not rest solely on absence of the RSA marker. There is no provider response record for this run.

Database connections used `mode=ro&immutable=1` and `PRAGMA query_only=ON` after confirming no WAL or rollback-journal sidecars existed. No application database constructors were called. Content hashes and modification times for all three databases were identical before and after queries.

## F. Recommended fix

The smallest safe next action is to recover the **existing launch command with credential values omitted, exact invocation time/timezone, and any already captured exception or terminal evidence**. Do not rerun to obtain it. An asynchronous request for the command and time was made during diagnosis; neither was supplied before this report was written.

If the invocation was at/after `1792195140`, the exact primary failure is the 600-second lifetime check at launcher line 115, raising `SecurityError('unsupported_execution')` at line 117. This requires a future, separately authorized fresh preparation/review/signing process and timely invocation, not a launcher change. That conditional result must not be promoted to a confirmed diagnosis without the timestamp and correct command.

If the command identifies another configuration, acknowledgement or approval, inspect those existing artifacts read-only before drawing conclusions. If it confirms the expected arguments and an eligible invocation time, retained authentication/exception evidence is needed to distinguish the remaining early failures. Do not refresh tokens or probe the network as part of this diagnosis.

No implementation change is recommended on current evidence. If a future task explicitly authorizes better diagnostics, a narrowly scoped proposal is to preserve a closed, sanitized stage/error category for failures before `execute_stage()`, without logging tokens, claims, raw exceptions or upstream bodies; test it entirely offline. That is a diagnostic improvement, not an established fix for this failure. Any executor or bound dependency change requires recalculated fingerprints, fresh configuration review and a new independent RSA approval. The current approval must not be reused for a changed contract.

## G. Safety verification

No live inference, launcher invocation, automatic retry, network authentication, token refresh, RSA signing, signing-key read, approval consumption, authority construction, governance admission/migration, financial reset, Azure/AKS operation, or modification of existing private artifacts was performed. No protected source was edited. Sensitive JSON/JWT files were read through inspected `read_private()`/`load_trust()` mechanisms; no full JWT, credential, private key or authentication claims were printed. Offline signature checks used the existing public key. Historical clock substitution was confined to an isolated diagnostic process and changed no artifact timestamps or authorizations.

Validation comprised actual read-only configuration validation and digest checks, offline RSA verification and binding reconstruction, six synthetic window-boundary checks, private-path checks, read-only database inspection and security schema/integrity checks. No full pytest, compileall or Docker validation was run: this is a report-only investigation, and those checks would not recover the lost invocation exception. `git diff --check` passed.

Self-review retained the distinction between verified preparation and unknown invocation behavior, between settled earlier activity and this job, and between an offline-reproduced time boundary and the unknown original failure. Pre-commit review found no credentials or new implementation artifacts in this report. Existing repository work was preserved.

`git status --short` showed 18 pre-existing modified tracked files and numerous pre-existing untracked phase artifacts; this task adds only this report. `git diff --stat` remained **18 files changed, 499 insertions(+), 44 deletions(-)**, all pre-existing tracked changes (untracked reports are not included by that command). **No staging, commit or push occurred.** Diagnosis stops here; compatibility execution was not repeated.
