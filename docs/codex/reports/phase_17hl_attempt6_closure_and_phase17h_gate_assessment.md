# Azure Foundry Attempt 6 closure and Phase 17H gate assessment

Date: 1 November 2026. Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`.
Mode: documentation, local evidence reconciliation and read-only verification.

## 1. Executive closure decision

**AZURE FOUNDRY ATTEMPT 6: PASS. Attempt 6: CLOSED — PASS.** The independently
authorized experiment completed one provider call, passed application validation
and settled its known usage. Current retained metadata independently agrees with
the operator-supplied result: `SUCCEEDED`, `calls=1`, `accounting_failed=false`,
`SETTLED`, 2,476 input tokens, 1,814 output tokens and catalog-accounted cost
**EUR 0.008817317845829546**. No contradictory execution evidence was found within
the inspection boundary. This is local catalog accounting, not an Azure invoice.

**Managed-prompt/4 single-call Azure acceptance: PASS** for this exact synthetic
first-chunk analysis. **The scoped offline diagnostic-hardening work package:
COMPLETE**, supported by its implementation and regression reports. **Full Phase
17H: PARTIAL. Full L1 live hierarchical digestion: NOT VALIDATED. Production
readiness: NOT ESTABLISHED.** The two live reductions, COMPLETE digest,
publication/retrieval and grounded Q&A acceptance sequence remain outstanding,
alongside representative semantic quality and workload reliability evidence.

**Phase 17G remains COMPLETED/PASS within its accepted single-host local/reference
scope**, as defined in the [authoritative Phase 17G report](phase_17g_report.md).
This closure neither reopens that accepted scope nor extends it to distributed or
production certification. No existing phase status file was changed.

Attempt 6's single-use authorization has been consumed. This report authorizes
no further inference, signing, financial reservation or next-phase execution.
Provider calls made by this documentation task: **0**.

## 2. Scope and evidence provenance

Evidence labels apply throughout this report:

| Label | Meaning and limit |
| --- | --- |
| **D — DIRECTLY VERIFIED FROM CURRENT ARTIFACT** | Read-only inspection or deterministic calculation performed in this closure task. This establishes retained local state, not independent Azure service or invoice verification. |
| **R — VERIFIED FROM EXISTING REPOSITORY REPORT** | A named existing report was inspected. Its historical findings and test outcomes are attributed to that report; they were not all reproduced here. |
| **O — OPERATOR-SUPPLIED SANITIZED EVIDENCE** | Authorized task/continuation evidence, including human authorization and preparation observations. No secret or signed payload was opened to recreate it. |
| **I — INFERENCE OR UNVERIFIED** | A reasoned implication or an explicit gap, never represented as a recovered historical fact. |

Diagnostic confidence is separate: **CONFIRMED** identifies an established cause;
**PARTIALLY CONFIRMED** identifies a demonstrated boundary with unresolved detail;
**UNKNOWN** means retained evidence does not establish it; **INFERRED** marks a
conclusion derived from other observations. In particular, R findings may have
been directly established by an earlier investigator without being D findings now.

The current narrow evidence inventory is:

| ID | Artifact or observation | Verified fields; omitted material |
| --- | --- | --- |
| D1 | Final refreshed Attempt 6 configuration, `configuration.final-attempt6-refresh.json` | Validated configuration digest, source/schema bindings, deployment identity, bounds, catalog and nine populated attestations. Private scopes/authority locations were used internally and not published. |
| D2 | Immutable `outcome.json` | State, calls, provider/application acceptance, accounting flag, sanitized usage metadata, canonical byte count and matching settlement snapshot. No raw response was read. |
| D3 | Existing governance database, matching reservation only | One matching job/request row, `SETTLED`, reserved/actual token counts and catalog costs; compared with D2. No authority constructor was instantiated. |
| D4 | Existing `run.sqlite` | One call, one finished call, outcome `success`, persisted start/finish times. |
| D5 | Existing `live-started.json` | Presence, matching configuration digest and executor. Approval identity was compared internally, not published. |
| D6 | Existing central approval-consumption marker | Presence, matching configuration digest and matching approval identity with D5. Marker fields only; no JWT or signing key was read. |
| D7 | Current source and Git state | Authoritative executor/generation/schema calculations, validation/launcher/governance source inspection, initial/final inventory and preservation checks. |

JSON inspection emitted only allowlisted metadata. SQLite inspection used
`mode=ro&immutable=1` and `PRAGMA query_only=ON`; no WAL/rollback-journal sidecars
were present for the two queried databases. Content hashes of six inspected
metadata/database/marker files were retained externally and checked for
preservation. No raw provider response, private key, credential, JWT content,
passphrase or actual private scope identity was exposed.

The supplied authorization, Entra verification, key provenance and financial
headroom observations remain **O**. Presence and consistency of local markers
are **D**; a new cryptographic verification or cloud authentication was neither
performed nor implied. No Azure service, web source or invoice was contacted.

## 3. Repository state and source bindings

**D:** Branch is `master`; HEAD is
`af4a7a076c918ef13aea05d74bf239c0af909133`. The initial file-level porcelain
inventory contained **20 modified tracked files, 128 untracked files and zero
staged files**. Git's directory-collapsed status displayed 120 untracked entries;
the file inventory resolves those directories into the 128 individual files.
Tracked diff statistics were **20 files, 894 insertions and 81 deletions**.
These are pre-existing aggregate changes, not changes made by this closure task.

An external baseline recorded hashes for **411 Git-visible existing files** and
the initial porcelain status. It does not claim a complete content inventory of
ignored/protected storage. The only repository addition from this task is this
report; all captured pre-existing content and status entries are preserved.

| Binding | Current value | Reconciliation |
| --- | --- | --- |
| Final configuration SHA-256 | `6d5a9cb4a190b3cf1195ccfe609e079aea499262ab0d54171d7572d132d80299` | D: recomputed with the current configuration model/digest; matches D2, D5, D6 and O. |
| Executor source SHA-256 | `d9af24e556305246ec145d15b3511e3e65fcf4e955e5b5f0dc550b4119b58a75` | D: authoritative recomputation; matches D1 and R v4 reports. |
| Generation source SHA-256 | `74cf9320b0ebf6d45df531e81827c5a8710b5b4d58fa75aad05dfa5039552290` | D: authoritative recomputation; matches D1 and the matching implementation/readiness reports. |
| Provider schema SHA-256 | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` | D: current schema conversion/fingerprint; matches D1 and R. |

The calculations used
[executor/configuration validation](../../../tests/performance/foundry_single_call.py),
[generation/configuration digest functions](../../../tests/performance/foundry_l1.py),
[managed generation](../../../documents/digestion/managed.py) and
[schema conversion](../../../llm/azure_schema.py). The inference-settings
fingerprint is a different object from the complete launch-configuration digest;
the two are not interchangeable.

For this calculation, application dotenv loading was suppressed, environment
inputs cleared, bytecode writes disabled, and a pre-import audit guard denied
network/socket creation, subprocesses, database connections and file writes.
The calculation passed. One import-time `socket.__new__` attempt was denied in
each guarded import process; a follow-up import-only check identified that event.
No socket connection, DNS lookup, external request, signing or authority database
initialization occurred. This is Python-level guarding, not a firewall claim.

## 4. Five unsuccessful billable attempts: chronology and comparison table

Attempts 1–5 failed application acceptance or bounded execution after billable
provider work. Attempt 6 succeeded. The separate preflight-only launch is excluded.
Token columns are input/output; costs are EUR catalog-accounted amounts.

| Attempt | Date in 2026 | Provider observation | Application/terminal result | Tokens | Actual catalog cost | Evidence |
| --- | --- | --- | --- | ---: | ---: | --- |
| 1 | 15 October | Response returned | FAILED; `extraction_limit_exceeded`; canonical size rejection | 1,845 / 1,460 | 0.00699907602956752 | R: [first-failure diagnosis](phase_17hl_first_failure_diagnosis.md), [three-attempt postmortem](../../engineering/postmortems/Estudio_PolyMind_Phase17HL_L1_Three_Attempts_Postmortem_2026-10-16.md) |
| 2 | 15 October | `output_limit` | FAILED; masking produced `governance_denied` | 1,955 / 1,922 | 0.00890113516367529 | R: [postmortem](../../engineering/postmortems/Estudio_PolyMind_Phase17HL_L1_Three_Attempts_Postmortem_2026-10-16.md), [output-limit hardening](phase_17hl_output_limit_hardening.md) |
| 3 | 16 October | Syntactically valid JSON returned | FAILED; `serialization_error`; closed application model rejected content | 1,994 / 932 | 0.005006599788807204 | R: [Attempt 3 root cause](phase_17hl_l1_attempt3_serialization_root_cause.md) |
| 4 | 19 October | Strict `json_schema` response path completed | FAILED; `serialization_error`; calls=1; accounting_failed=false | UNKNOWN | UNKNOWN | O historical summary; R: [offline compatibility audit](phase_17hl_final_offline_azure_compatibility_audit.md), [observability review](phase_17hl_live_failure_observability_and_contract_options.md) |
| 5 | 29 October | `completed_strict_response`, finish `stop` | FAILED; `serialization_error`; `claim_contract / subject_on_nonfact`; calls=1 | 2,342 / 1,852 | 0.008879355860613052 | R: [post-execution diagnostics](phase_17hl_attempt5_post_execution_diagnostics.md), based on its later O terminal evidence |
| 6 | 1 November | `completed_strict_response`, finish `stop` | SUCCEEDED; application accepted; calls=1 | 2,476 / 1,814 | 0.008817317845829546 | D1–D6 and O |

Attempts 1–3 have settled cost evidence in their historical reports; Attempt 5
reports `SETTLED` and `accounting_failed=false`. No Attempt 4 token count, actual
cost or exact rejecting predicate is reconstructed here. No six-attempt spend
total is asserted with that missing record.

## 5. Root causes, corrections and unresolved historical uncertainties

### Attempt 1 — canonical expansion, CONFIRMED

**R:** The provider response was **2,597 UTF-8 bytes**. Pydantic inserted omitted
defaults, and canonical compact ASCII JSON became **3,471 bytes**, exceeding the
original **3,000-byte** canonical ceiling. The historical application mapping
surfaced `extraction_limit_exceeded`; the failure occurred during analysis
normalization, not PDF extraction. The measured default expansion was 874 bytes.
This was not demonstrated completion-token exhaustion: output usage was 1,460
against a 3,000-token reservation. The exact original finish reason was not retained.

The initial correction exposed default fields and canonical ASCII budgeting in
generation instructions. Subsequent [independent JSON byte-limit work](phase_17hl_independent_json_byte_limits.md)
separated raw-response and canonical-result limits and set the relevant L1 limits
to **10,000 bytes each**, retaining **3,000 completion tokens** and **26,192 HTTP
envelope bytes**. This removed representation/token coupling without truncating
content or weakening evidence validation. Historical 195-test diagnosis and
310-test independent-limit selections are R outcomes, not new runs here.

### Attempt 2 — error masking CONFIRMED; original trigger UNKNOWN

**R:** A provider `output_limit` exception was replaced by a later
`RunGuard.finish()` governance exception. Thus terminal `governance_denied` does
not prove an actual quota denial. Retained records do not establish whether the
original provider condition was response-byte overflow or provider truncation/
finish behavior. The 1,922 output tokens alone do not recover that distinction.

The [output-limit correction](phase_17hl_output_limit_hardening.md) fixed
finish-time masking and added sanitized cause/byte/finish/usage diagnostics.
Subsequent governance cleanup preserves a primary provider exception while
separately retaining `accounting_failed` when settlement also fails. Unknown
usage remains unresolved and blocks continuation; it is never fabricated as zero.
Focused error-precedence, settlement and containment regressions support the
mechanism. Later diagnostics cannot recreate missing historical metadata.

### Attempt 3 — malformed evidence UUID and forbidden fields, CONFIRMED

**R:** Valid JSON failed `StageResult.model_validate`: one malformed **evidence
UUID** and eight forbidden top-level fields, `unused1` through `unused8`.
Canonical encoding, domain evidence checks and checkpoint persistence were not
reached. This is not a confirmed deterministic `claim_id` failure.

Removing only the extra fields still failed UUID parsing. Correcting only the
UUID still failed object closure. Correcting both passed an in-memory offline
counterfactual; it was not approved runtime repair, accepted recovery or persisted
evidence. [Seven synthetic regressions](phase_17hl_l1_attempt3_serialization_root_cause.md)
preserved independent rejection and valid controls.

Historical `response_format=json_object` constrained JSON syntax without enforcing
the full application schema. Subsequent
[strict compatibility](phase_17hl_structured_output_compatibility.md) and
[two-layer output work](phase_17hl_two_layer_structured_output.md) introduced strict
provider schema generation while retaining local UUID, deterministic identity,
membership and lineage checks. A separate launcher defect allowed failed jobs to
return process exit zero. Current source maps unsuccessful terminal outcomes to
exit 1; the retained root-cause report predates that correction and is preserved.
The [offline regression reconciliation](phase_17hl_regression_reconciliation.md)
records the corresponding CLI expectation update. Attempt 6 exit zero is consistent
with its successful outcome, not proof that the historical defect never existed.

### Attempt 4 — application rejection boundary PARTIALLY CONFIRMED

**O/R:** One governed billable call completed the strict response path, then
failed application validation as `serialization_error`, state FAILED,
`calls=1`, `accounting_failed=false`. **The exact rejecting predicate remains
UNKNOWN.** No malformed UUID, extra-field violation or `subject_on_nonfact`
predicate is assigned to this attempt. Strict completion and application
acceptance are distinct observations.

The [initial diagnostic hardening](phase_17hl_diagnostic_hardening.md) and
[later observability work](phase_17hl_live_failure_observability_and_contract_options.md)
added closed stage/reason attribution and sanitized provider metadata. Offline
schema/evidence integration established valid witnesses and intentional local
rejections; it did not recover Attempt 4's missing cause.

The [F1 cleanup report](phase_17hl_f1_http_cleanup_failure_preservation.md)
separately confirmed that expected response/session-close I/O errors could replace
a primary inference failure. The correction preserves that primary exception and
normalizes cleanup-only failure. Its 77 additions passed within a 1,755-test
offline regression; the pre-fix 47-case selection exposed 25 failures and then
passed after correction. This confirms a cleanup defect, **not** that cleanup
caused Attempt 4's historical application rejection. Unexpected programming/
control-flow cleanup failures and caller-owned session lifecycle remain within
the limitations documented by F1.

### Attempt 5 — instruction-to-validator contract gap, CONFIRMED

**R, with later O terminal evidence:** The strict response completed, but
`validate_result()` correctly rejected a populated subject on a non-factual claim:
`claim_contract / subject_on_nonfact`. The active `managed-prompt/3` instructions
and generation schema did not explicitly convey the domain's fact-only populated
subject rule. Strict structural schema success did not enforce that relationship.

Usage was 2,342 input and 1,852 output tokens; **320 reasoning tokens were already
included in output**, not added again. Finish reason was `stop`; accounting did
not fail and the financial row was `SETTLED`. The exact historical subject value,
non-fact kind, claim index and any later unexecuted predicates remain unknown.

The [managed-prompt/4 implementation](phase_17hl_managed_prompt4_subject_contract_implementation.md)
explicitly requires `subject=null` for `unknown`, `unsupported`, `commentary` and
`structural`; facts may retain null or a valid populated subject. Domain validation,
strict schema, deterministic identities, evidence checking and lineage remain
authoritative. No model-generated claim is silently repaired or reclassified.
The 35-case subject matrix and four non-fact rejection controls demonstrate this
instruction correction while preserving fail-closed acceptance.

The [24 October final-readiness checkpoint](phase_17hl_attempt5_final_readiness_and_operator_preparation.md),
[authorization/preparation report](phase_17hl_attempt5_operator_authorization_and_single_call_execution.md)
and [retained live-execution report](phase_17hl_attempt5_live_execution_report.md)
include earlier blocked/unexecuted observations. The later 29 October
[post-execution report](phase_17hl_attempt5_post_execution_diagnostics.md) records
the separately authorized provider invocation. Both chronological facts are
preserved. Attempt 5's confirmed subject error does not identify Attempt 4's cause.

### Failure-to-correction traceability matrix

| Historical failure | Evidence | Correction | Offline verification, R | Attempt 6 relevance | Residual uncertainty |
| --- | --- | --- | --- | --- | --- |
| 1: canonical expansion | First-failure diagnosis; independent byte-limit report | Explicit defaults; independent 10,000-byte limits; token ceiling retained | Default-expansion, raw/canonical/Unicode boundaries; 310-test limit selection | Accepted canonical result 3,907 bytes fits corrected ceiling | No universal guarantee all valid future outputs fit; original finish metadata absent |
| 2: provider error masked | Output-limit report and three-attempt postmortem | Preserve primary exception; closed diagnostics; fail-closed unknown accounting | Error precedence and STARTED/UNKNOWN/SETTLED controls | Successful provider outcome and settled row stay distinct from application result | Exact original output-limit trigger remains UNKNOWN |
| 3: schema-invalid JSON | Attempt 3 root-cause report | Strict provider schema plus unchanged local identity/evidence checks; failed CLI exit fix | Seven Attempt 3 cases; two-layer/CLI reconciliation | Strict response plus full local acceptance observed | Schema still cannot guarantee domain semantics or future compliance |
| 4: unidentified local rejection | Compatibility audit and observability report | Stage/reason diagnostics; metadata; separate F1 cleanup preservation | 1,631-test observability regression; F1 1,755-test regression | Current audit distinguishes both acceptances and accounting | Exact Attempt 4 predicate remains UNKNOWN; F1 is not its proven cause |
| 5: non-fact subject | Attempt 5 diagnostics and v4 implementation | Explicit fact-only subject instructions, v4 binding; no repair | 447 selected checks; 35-case matrix; 108 integration checks | One v4 live result accepted unchanged | Historical claim details unknown; one success does not estimate reliability |
| Separate preflight-only launch | Single-call execution failure diagnosis | Per-stage preflight categories, timing display and handoff | 28 preflight cases in timing-hardening report | Better preparation observations; no extra paid inference implied | Precise historical failed operation remains unresolved |

Counts in this matrix describe different historical selections/snapshots. They
overlap and must not be added into a cumulative test count.

## 6. Non-billable preflight and operator-script preparation lessons

**R:** The signed/prepared 16–17 October launch after Attempt 3 did not establish
an additional billable model failure. The
[read-only launch diagnosis](phase_17hl_single_call_execution_failure_diagnosis.md)
found no provider inference, financial reservation for that job, approval-consumption
marker or live-start marker in the retained evidence. Its combined historical
authority/audit observations placed the failure before inference; the precise
failed preflight operation was unresolved. The execution-window cutoff was a
reproducible possibility, not a confirmed historical cause. This closure reuses
that report and does not freshly inspect the old private packet.

The [preflight observability/timing correction](phase_17hl_preflight_observability_timing_hardening.md)
added sanitized stages/categories and an explicit exclusive cutoff:
`min(approval_expires, credential_valid_until) - 600 seconds`. Stage-entry evidence
does not itself prove successful authorization consumption. Better diagnostics
improve attribution without retroactively solving the old failure.

**O:** Attempt 6 preparation also encountered automation defects before paid
inference. They are recorded separately from application/model failures:

| Preparation issue | Correction or disposition |
| --- | --- |
| Incorrect uniqueness check for deterministic fixture/request hashes | Treat deterministic hashes as stable content bindings; execution identities and one-use authorization provide distinctness. |
| Python `/dev/tty` `r+` input-handling failure | Operator input handling corrected. No claim-validation rule changed. |
| Trust discovery expected a JSON object but encountered a list | Corrected discovery assumptions; then used the established explicit trusted path. No new trust authority was invented. |
| Entra token had insufficient remaining lifetime for signing gate | Operator refreshed authentication and finalized a new approved execution window. No refresh was performed by this closure task. |
| Earlier invocation supplied an empty DIGEST argument | Rejected before inference; corrected handoff used the exact final digest. |

These observations are operator-supplied; the scripts were not executed or used
to open secrets here. Their correction did not modify the application's strict
validation logic and did not establish additional paid calls. They are not counted
as extra billable attempts or as the separate 16–17 October historical launch.

## 7. Managed-prompt/4 and Attempt 6 engineering readiness

**R:** The [v4 implementation report](phase_17hl_managed_prompt4_subject_contract_implementation.md)
records **447 distinct selected passing checks**, zero final failures/skips and
zero observed network attempts. Its 22-test final recheck is overlapping evidence,
not 22 additional distinct tests. Active execution rejects stale v3 labels/bindings;
archived v3 witnesses and already validated historical results remain readable
under their original context. No old plan is silently upgraded or resumed.

The [Attempt 6 offline integration report](phase_17hl_attempt6_offline_integration_readiness.md)
records **108 distinct passing checks**, zero final failures/skips and zero
observed network attempts. Real four-page fixture preparation rendered one chunk;
all four stage profiles used v4 instructions. Synthetic accepted output traversed
the adapter, governance and full validator; non-fact populated subjects still
failed without repair. One-call synthetic settlement and second-admission refusal
were checked. An initial relative-fixture-path setup error was corrected only in
disposable storage and remains documented there.

**D:** Source inspection confirms v4 selection and explicit subject guidance,
separate byte/token limits, strict provider schema, no retry/fallback loop and
the full local `validate_result()` acceptance path. The matching source/schema
hashes tie those reports to the inspected implementation. Historical test results
are reused as R evidence; this documentation task does not claim a fresh full
regression run or service-side reliability measurement.

## 8. Attempt 6 authorization and live execution chronology

Execution identity, **D1/O**: Azure resource `epolymind-foundry-dev-susanta`;
deployment `epolymind-gpt-54-mini`; model `gpt-5.4-mini`, version `2026-03-17`;
SKU `GlobalStandard`; region `spaincentral`. Executor is
`polymind-single-analysis/1`; prompt `managed-prompt/4`; generation profile
`managed-generation/2`; provider schema `azure-strict/1`; domain `stage-result/1`.
These are retained configuration bindings, not newly queried Azure properties.

| Order/time, UTC | Evidence and interpretation |
| --- | --- |
| 29 October readiness | R: v4 implementation and offline integration completed before operator preparation. |
| 1 November preparation | O: financial headroom/admission, existing SecurityAuthority registration/exact permissions and Entra v2 delegated identity checks passed. Nine attestations and explicit one-call financial approval were finalized. |
| Final independent approval | O: RS256 approval verified for audience `polymind-single-analysis-live`; final one-call operator authorization supplied. This is distinct from identity authentication and financial approval. |
| 14:17:09 | D1: refreshed approved execution window starts. |
| Before guarded provider admission | D5/D6: persistent consumption and live-start evidence present and bound to the same configuration/approval identity. Source establishes consumption precedes provider execution; no new cryptographic verification was performed here. |
| 14:27:20.597429–14:27:28.451192 | D4: durable run call start/finish interval. These are local guard timestamps, not independently measured HTTP latency or Azure server timestamps. |
| 14:37:09 | D1: exclusive launch cutoff, ten minutes before approval expiry; the observed call start precedes it. |
| 14:47:09 / 15:00:45 | D1: approval expiry / attested credential-use deadline. These historical deadlines grant no current execution permission. |
| Terminal output and exit | O: `{"state":"SUCCEEDED","calls":1}`, launcher exit 0. D2/D4 independently agree on successful state and one finished call. |
| Final local audit | D2/D3: application accepted, accounting not failed, known usage SETTLED. |

The final refreshed configuration digest is the value in section 3. Earlier
preparation packets/windows are not substituted for it. This task did not rerun
the launcher, renew identity, verify a live token or sign/consume another approval.

## 9. Provider acceptance, application validation and result classification

**D2:** `provider_acceptance=completed_strict_response`,
`application_validation=accepted`, `state=SUCCEEDED`, `calls=1`,
`accounting_failed=false`. No failure field is present; the supplied sanitized
`failure: NONE` is consistent with that absence. Finish reason is `stop`.
The accepted canonical result is **3,907 ASCII JSON bytes**, within 10,000.

The adapter-completion marker alone would not prove JSON Schema/domain validity.
Here the separate application-acceptance field records successful return from
`validate_result()` after governed execution and authority revalidation. Current
[runner source](../../../tests/performance/foundry_single_call.py) sets SUCCEEDED
only after that acceptance and canonical result hashing. The inspected
[validator](../../../documents/digestion/validation.py) retains decoding/model,
canonical-size, stage, deterministic identity, evidence membership/coverage,
claim-domain and applicable lineage checks. No raw response was opened or replayed
to repeat those checks in this task.

**INFERRED from D2/D7:** The retained result passed those implemented structural
and domain gates on this run. Citation membership and complete authorized-source
coverage do not independently prove natural-language entailment or human-rated
quality. Application success is neither a semantic audit nor complete digestion.

## 10. Financial reservation, actual usage, settlement and cost

**D1–D4:** The contract allows one attempt, at most 25,000 input and 3,000 output
tokens, zero automatic retries, and the existing **EUR 5 monthly governance
ceiling**. The approved catalog is `phase17hl-pricing-eur-202610/1`, effective
1 October 2026, currency EUR. Fixed and extra cost bounds in this contract are
zero; this records the approved accounting contract, not independent proof that
Azure can impose no incremental charges.

| Measure | Verified value | Meaning |
| --- | ---: | --- |
| Maximum input/output envelope | 25,000 / 3,000 tokens | Approved per-call ceilings, not measured use |
| Pinned full-envelope token cost | EUR 0.028379091869065 | D: recomputed from the approved catalog for 25,000/3,000 |
| Actual pre-call governance reservation | 11,413 input / 3,000 output | D3: conservative rendered-input estimate plus output reservation |
| Reservation row `cost` | EUR 0.019411958817320188 | D2/D3: reserved catalog cost; distinct from settled actual cost |
| Actual input | 2,476 tokens | D2/D3 |
| Actual output | 1,814 tokens | D2/D3 |
| Actual reported total | 4,290 tokens | D2 and arithmetic 2,476 + 1,814 |
| Reported reasoning usage | 400 tokens | D2: already included in output; not another charge or additive total |
| Actual catalog-accounted cost | **EUR 0.008817317845829546** | D2/D3; independently recomputed locally with exact decimal arithmetic |
| Settlement / accounting failure | SETTLED / false | One matching governance row and one completed run call |

The matching governance row was selected by the private configuration's job
identity, checked against its request identity, and compared with the immutable
outcome snapshot. No private identity was printed. All selected settlement fields
agree. No reservation was created or consumed by this task.

**O:** Commercial approval retained the pinned October EUR catalog with a fresh
operator attestation. November USD token rates had previously been reviewed.
**UNVERIFIED:** Independently verified November EUR conversion and applicability
of every potential incremental charge were not established by this audit. The
amount above is locally catalog-accounted spend, **not a guaranteed Azure invoice
amount**. No claim is made about complete monthly account headroom after this run
or unrelated cloud charges.

## 11. Security, one-use approval, replay protection and retained evidence

The [operator-approval documentation](../../evaluation/phase_17hl_operator_approval.md)
is under `docs/evaluation/`, with a separate historical
[implementation report](phase_17hl_operator_approval_report.md). Its L1 audience
and single-analysis audience are distinct; Attempt 6 used
`polymind-single-analysis-live`. Authentication, domain permissions, commercial
approval and independent signature approval remain separate gates.

**D5/D6:** The durable launch marker and central consumption marker exist, share
the final configuration binding, and identify the same approval internally.
The run database independently contains exactly one completed successful call.
The consumption marker has approval/key identifiers and artifact/configuration
hash fields. Its artifact hash was not recomputed against the signed JWT, because
JWT contents were deliberately not opened. **O:** independent RS256 verification
and final human authorization passed during the actual execution.

**D7:** Source verifies approval before consumption, creates consumption with
exclusive persistent filesystem semantics, then creates the live marker before
provider execution. The one-call RunGuard and durable financial transitions
provide additional containment. Marker presence plus one recorded call supports
local one-use containment; it does not audit every possible external Azure caller.
No replay attempt was made to test a consumed approval.

Retain the original configuration/windows, audit, run/governance records and
launch/consumption markers under existing operator retention/access controls.
Do not delete, relocate, regenerate or reset them to retry. Previously signed
artifacts remain private and untouched. Single-host persistent replay protection
is not distributed consensus or protection against privileged state rollback.
This task creates no new retention policy or approval authority.

## 12. What the success demonstrates — and does not demonstrate

**Demonstrated for this run, D/R/O:** The selected Azure configuration produced
one completed strict response under v4 instructions; the application accepted
that first-chunk result unchanged; known usage settled once; local records agree
on one call and no accounting failure. This supplies the live application
acceptance missing from the preceding diagnostic experiments.

**Not demonstrated:** First or second hierarchical reduction; a COMPLETE document
digest; publication/retrieval and a grounded answer; representative document
semantics; expert citation/entailment assessment; acceptance frequency across
documents or repeat runs; real workload tail latency/recovery/capacity; large-document
live L2 success; OCR/visual fidelity; distributed governance; comprehensive Azure
deployment hardening; invoice accuracy; production/public-user readiness.

The fixture was a deterministic four-page synthetic PDF and the test selected
one first-chunk managed analysis. One successful synthetic call is not a reliable
estimate of model failure probability. Earlier failed outputs remain failures;
their evidence was not repaired or overwritten to obtain this closure.

## 13. Phase 17H–L work-package status

| Scope | Disposition | Evidence and boundary |
| --- | --- | --- |
| Phase 17G | **COMPLETED/PASS within local/reference scope** | R: [17G closure](phase_17g_report.md), 690 final closure tests; no production/distributed extension inferred. |
| Attempt 6 experiment | **CLOSED — PASS** | D/O: accepted single call and matching settlement/markers. |
| Managed-prompt/4 single-call Azure acceptance | **PASS** | Exact synthetic first-chunk analysis only. |
| Scoped offline diagnostic hardening | **COMPLETE** | R: diagnostic implementation, [regression reconciliation](phase_17hl_regression_reconciliation.md), [offline E2E](phase_17hl_offline_e2e_contract_verification.md), [configuration isolation](phase_17hl_full_suite_configuration_isolation.md), observability, F1, v4 and integration reports. Historical unknowns were preserved rather than invented. |
| Full Phase 17H | **PARTIAL** | R: [original 17H report](phase_17h_report.md), [phase prompt](../prompts/phase_17h.md); one call supplies only a narrow live milestone. |
| Phase 17I — External User Verification | **PLANNED / NOT STARTED in available phase evidence** | R: 17H report and [17A roadmap](phase_17a_report.md). Requires accepted prior gates and separately approved external exposure. |
| Phase 17J | **UNKNOWN / no established definition or completion evidence found** | Local roadmap/report search does not establish a separate 17J acceptance scope. |
| Phase 17K | **UNKNOWN / no established definition or completion evidence found** | No completion inferred from workstream naming. |
| Phase 17L | **UNKNOWN / no established definition or completion evidence found** | No completion inferred from “17H–L” naming; it is not evidence of individual phase acceptance. |

The complete offline engineering package and the incomplete broader evaluation
phase are different scopes. Earlier reports' conditional live-readiness statements
remain accurate at their dates; this report adds the later narrow acceptance.

## 14. Phase 17H closure-gate assessment

The [Foundry validation runbook](../../evaluation/phase_17h_foundry_validation.md)
defines L1 as digestion plus one native-page factual question. Its original
sequence includes chunk analysis, first structural reduction, second/root
reduction and grounded Q&A. A complete digest and authorized publication/retrieval
bridge the hierarchy and question. Historical runbook “not started” checkpoints
are retained; they do not negate the later individual experiments.

| Gate | Current evidence | Decision |
| --- | --- | --- |
| Chunk analysis | Attempt 6 accepted one four-page first-chunk result | **PASS for exact single-call test**; complete durable L1 workflow still pending |
| First hierarchical reduction | Offline witnesses/regressions; no accepted live reducer evidence verified here | **NOT VALIDATED live** |
| Second hierarchical reduction | Offline root witnesses/regressions; no accepted live root evidence verified here | **NOT VALIDATED live** |
| COMPLETE digest and publication | No complete accepted live sequence established | **NOT VALIDATED live** |
| Grounded Q&A and citation review | No Attempt 6 Q&A call or independent answer review | **NOT VALIDATED live** |
| Representative semantics/expert quality | One synthetic analysis; no new human claim-level assessment | **PENDING** |
| Real workload reliability | Earlier bounded offline evidence remains; one successful live sample | **PARTIAL / live reliability not established** |

**Recommendation: retain full Phase 17H = PARTIAL.** No independent evidence found
in this assessment establishes all original criteria, and no explicit scope
change authorizes redefining the phase around a single chunk. Do not mark L1/L2,
external-user verification or production readiness complete from Attempt 6.

## 15. Remaining risks, next development milestone and actionable acceptance criteria

The next acceptance milestone is **a separately reviewed, explicitly authorized
full-L1 hierarchical digestion and grounded-Q&A evaluation on the established
four-page fixture**. It is a recommendation, not authorization or a new packet.
Attempt 6's consumed approval cannot cover remaining calls or resume a larger run.

Before requesting that future execution, make its scope reviewable using existing
offline engineering and gates. The acceptance criteria are:

1. Reconcile exact current source, prompt, schema and intended full-L1 composition
   against the runbook. Generate/review fresh plan and stage bindings under that
   future task; do not splice single-call output into an old plan or reuse old
   source approvals. Keep strict validation, evidence/lineage and no silent repair.
2. Demonstrate accepted live chunk analysis, first reduction and second/root
   reduction in the governed durable workflow, then verify COMPLETE digest,
   full source/child coverage, inherited qualifications/contradictions and
   immutable checkpoint/lineage consistency.
3. Publish/retrieve under the established security scope and execute the predefined
   native-page factual question. Validate citations against canonical source text
   and selected document/version; record independent human assessment of factual
   support, required findings, abstention and unsupported conclusions.
4. Pin a current reviewed commercial basis, capacity/headroom and fresh independent
   identity/financial/signature authorization for the exact future call envelope.
   The original L1 envelope is four calls, not Attempt 6's one call. Stop on a
   critical failure; do not expand retry, budget or scope automatically.
5. Retain per-stage provider/application outcomes, closed diagnostics, actual
   tokens, accounting flags, matching settlements and final exit/result evidence.
   Unknown usage must remain unresolved and fail closed. Prove local call bounds
   through records without issuing an unauthorized replay test.
6. Assess the resulting L1 evidence before considering a separately authorized L2.
   Recheck large-document context, fan-in, result-size and Q&A envelope constraints;
   a four-page acceptance does not remove previously documented L2 limits.

Full Phase 17H additionally requires representative documents, independent
semantic/citation quality and real workload reliability evidence under its
[quality rubric](../../evaluation/phase_17h.md). The runbook's historical targets
are 100% structural citations, at least 95% independently supported claims,
at least 90% required findings and zero critical unsupported conclusions.
Record numerators/denominators, reviewed/total responses and claims, disagreements
and pending review; do not count unreviewed content as supported. Representative
large-document evaluation and accepted reliability/quality limits must precede
separate Phase 17I external-user exposure approval.

Residual risks include UNKNOWN Attempt 2 trigger and Attempt 4 predicate; remaining
instruction ambiguities documented by the compatibility audit; schema/domain gaps
requiring model compliance; unmeasured semantic quality and reliability; single-host
governance/replay limits; caller-owned shutdown limitations; and unverified invoice/
November EUR/possible incremental-charge applicability. None contradicts the
observed single-call success, and none is erased by closing it.

## 16. Validation, Git diff review and final disposition

This documentation task inspected `AGENTS.md`, repository state, the specifically
requested historical reports, applicable phase/runbook definitions, relevant
implementation and selected regression source. It preserved prior reports,
including their blocked/preparation-era statuses. It changed no implementation,
schema, test, prompt, policy, financial contract or phase status file.

Validation consists of initial/final `git status`, `git diff --stat`,
`git diff --check`, a separate new-file whitespace check, relative Markdown link
resolution, numeric/source reconciliation, current configuration/source/schema
digest calculations, exact-decimal catalog arithmetic, narrow read-only
settlement/marker comparisons and baseline preservation checks. The report's
complete new-file diff was reviewed separately because ordinary Git diff excludes
untracked files. No full pytest, compileall, lint, Docker/Kubernetes or cloud
validation was needed or run for this documentation-only change.

Final preservation checks establish **zero changed or removed captured existing
files**, **one new report**, **zero new staged entries**, unchanged branch/HEAD,
and unchanged tracked diff statistics: **20 files, 894 insertions, 81 deletions**.
Final file-level status is the original 20 modified tracked / 128 untracked paths
plus this report: **20 modified tracked / 129 untracked / zero staged**.
The six inspected private metadata/database/marker content hashes remain unchanged.
All new relative Markdown file targets resolve; whitespace checks pass.

The implementation self-review for this task is an evidence/diff review: it
separates provider from application acceptance, bounds each cause by its actual
evidence, preserves unknown historical diagnoses, distinguishes reserved and
actual costs, retains October-catalog/invoice limitations and avoids broad phase
closure. A separate pre-commit review of the new report checked for secret/key/
token material, actual private scopes, raw provider content, executable live
handoff commands, accidental source/dependency changes, temporary artifacts,
unrelated edits and broken links. No sensitive artifact was reproduced.

Documentation created: this report only. Historical evidence preserved: **yes**.
Secrets exposed: **0**. New Azure/provider calls: **0**. New signatures or approval
consumptions: **0**. New financial reservations/mutations: **0**. Cloud operations:
**0**. Git staging, commits and pushes: **0 / 0 / 0**.

**Final disposition: Attempt 6 CLOSED — PASS; managed-prompt/4 exact single-call
integration PASS; offline diagnostic-hardening package COMPLETE; Phase 17G
COMPLETED/PASS within its defined scope; full Phase 17H PARTIAL. The next gate is
full-L1 live hierarchical digestion plus grounded Q&A and independent review,
under a future separate authorization.**
