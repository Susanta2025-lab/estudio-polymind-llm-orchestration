# Phase 17H–L — Attempt 5 Final Readiness and Operator Preparation

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

For the historical examples below, `PROJECT_ROOT` means the absolute path to a local checkout; `PYTHON` means the absolute path to the project Python 3.10.13 interpreter. Define them with shell assignments such as `PROJECT_ROOT="<absolute checkout path>"` and `PYTHON="<absolute project interpreter path>"`, substituting local paths; these schematic values are not executable examples. `PYTHON_311` and `PYTHON_312`, where used, mean absolute paths to the independently installed Python 3.11.8 and 3.12.9 interpreters. Define them analogously with `PYTHON_311="<absolute Python 3.11.8 path>"` and `PYTHON_312="<absolute Python 3.12.9 path>"`. Their original execution results are retained; temporary drivers and guards are historical evidence, not installed project commands.

Date: 24 October 2026. Branch: `master`.
HEAD: `af4a7a076c918ef13aea05d74bf239c0af909133`.
[Task prompt](../prompts/phase_17hl_attempt5_final_readiness_and_operator_preparation.md).

## A. Executive summary

**ENGINEERING GO. OPERATOR PREPARATION: READY (non-executing handoff).
EXECUTION AUTHORIZED NOW: NOT VERIFIED.**

The F1 correction remains present; all four authoritative bindings match the
[F1 report](phase_17hl_f1_http_cleanup_failure_preservation.md). The requested
guarded offline selection passed **426 tests**, with zero failures, errors, skips,
warnings or observed network attempts. No additional confirmed engineering blocker
prevents preparation of the single-analysis diagnostic. No implementation or test
was changed. The prior **1,755-test** full regression is reused, not rerun.

The handoff is ready for protected operator work; an executable private
configuration and current approval are **not established** by this assessment.
Existing evidence is reconciled below without reopening a C1–C7 audit. Attempt 5
was not executed or authorized here. **Phase 17H remains PARTIAL** until live-model
acceptance and the remaining evaluation requirements are demonstrated.

## B. F1 closure

Inspection of `llm/bounded_http.py:request_json` confirms one POST and one response
close in `finally`. Expected cleanup I/O exceptions (`OSError`,
`requests.RequestException`) preserve an earlier failure. The `completed` flag is
set only after bounded reading and unique-key JSON decoding succeed. A cleanup-only
I/O failure rejects that result with sanitized `InferenceConnectionError`; an
incomplete response is never accepted. Redirect/configuration, output-limit,
timeout and protocol categories survive expected cleanup errors. No retry was added.

`OpenAICompatibleProvider.close` preserves an active primary failure during owned
session cleanup and normalizes cleanup-only I/O failure. Externally supplied
sessions are not closed by the provider. The 56 unit and 21 governed F1 cases
passed again, including exact primary exception preservation, single cleanup,
normal success, unchanged categories, UNKNOWN obligations and already SETTLED usage.
Unexpected programming/control-flow cleanup exceptions remain outside the narrow
expected-I/O handling policy, as documented in F1.

The single-call launcher's externally owned session still has its direct
`finally: session.close()` after `execute_stage` persists the outcome. That
unchanged caller boundary can affect the outer shutdown result; it does not erase
durable stage accounting. This previously documented lifecycle limitation remains
nonblocking for preparation; no new reproducible blocker or redesign is introduced.

## C. Current source bindings

These were recomputed under settings isolation and pre-import network denial,
using the authoritative functions, not copied into a configuration or approval.

| Binding | Current SHA-256 | Comparison with F1 |
|---|---|---|
| Executor — `foundry_single_call.executor_digest()` | `82fc01aa0447d4be758124cec0120a06db49f139f69ee6425b51b8696a6ad26f` | Exact match |
| Generation source — `foundry_l1.generation_contract_digest()` | `7d387a8595cf63e2ac944a25c4987a1b37392aa4adba8889914acf51ff9f0f59` | Exact match |
| Provider schema — `fingerprint(provider_schema(generation_schema()))` | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` | Exact match |
| Inference configuration — `ManagedSynthesisInference.config` | `7eaa6b52ad387f9f0c82e318e9c74fa378ffda0baec85d0f7157cc4ab0553519` | Exact match |

The inference configuration was constructed with the single-call strict capability,
explicit four stage profiles (24,800 input / 3,000 output), generation profile 2,
26,192-byte envelope and intended deployment mapping, exactly as in F1. An unusable
transport and offline endpoint were sufficient: this fingerprints managed inference
settings/model, not credentials or the actual private launch configuration.
`configuration_digest(config)` is a separate digest of the validated complete
operator configuration; that value remains operator-owned and was not generated.

The retained 260-file F1 pre-edit public snapshot differs only in the two documented
F1 production files. Their post-fix state is reconciled by the matching authoritative
digests. No relevant source change since the verified correction is indicated.
No fingerprint algorithm or historical approval was refreshed.

## D. Preserved generation contract and execution inventory

The contract remains `managed-prompt/3`, `managed-generation/2`, `azure-strict/1`,
`stage-result/1`, with capability `gpt54mini-30k/2` and managed inference `managed/1`.
The existing frozen renderer, model/validation source references and nine
request/generation/payload oracles passed. Deterministic ordered claim IDs,
stage binding, original evidence, qualification, coverage and lineage validation
remain enforced. There is no automatic repair, fallback model or retry.
`managed-prompt/4` and the application-owned-identifier proposal remain inactive.

| Non-secret binding | Required value / ownership |
|---|---|
| Executor / purpose | `polymind-single-analysis/1`; one governed first-chunk analysis diagnostic; approval purpose `live` |
| Fixture | Established deterministic four-page synthetic PDF: `pdf(4, seed=1708)`; four extracted units and one analysis chunk; no substituted document |
| Resource / deployment | `epolymind-foundry-dev-susanta` / `epolymind-gpt-54-mini` |
| Model / version / SKU | `gpt-5.4-mini` / `2026-03-17` / `GlobalStandard` |
| Interface / endpoint | Azure OpenAI v1 Chat Completions; HTTPS resource host permitted by `deployment_configuration`, `/openai/v1/chat/completions`; actual endpoint/authentication selection is operator-owned |
| Schema / payload | `response_format.type=json_schema`, name `polymind_stage_result`, `strict=true`; system and user messages; `stream=false`, `reasoning_effort=low`, `max_completion_tokens=3000`; no temperature or tools |
| Calls / token reservation | Maximum calls 1; input 25,000, completion 3,000; aggregate input/output 25,000/3,000; context 28,000; per-run RPM 1 |
| Independent byte ceilings | Raw UTF-8 content 10,000; canonical compact ASCII JSON 10,000; HTTP envelope 26,192 |
| Operator identity | Verified Entra v2 user, configured tenant/issuer/API audience, delegated `access_as_user`, exact `PolyMind.L1Operator` role; derived scope equals `owner_scope`; existing enabled SecurityAuthority registration and permissions |
| Authority/scope configuration | Actual `owner_scope`, `oidc`, `security_path`, `governance_path`, `admission_path`, `quota_key`, `policy`, `governance_policy` with existing evaluation binding; operator-owned, no invented identities or scope UUIDs |
| Request bindings | New `job_id`, `request_id`, private `audit_directory`, actual-scope `fixture_sha256`, `rendered_request_sha256`; validated complete configuration digest and acknowledgement; all operator-owned |
| Approval | Independent pinned RSA trust and persistent replay authority; audience **`polymind-single-analysis-live`**; exact source/configuration/operator/financial/request binding and fresh unused approval ID |
| Execution attestations | All nine: `credential_valid_until`, `approval_expires`, `execution_not_before`, `credential_audience_verified`, `quota_verified`, `shared_consumers_verified`, `charges_verified`, `actual_azure_rpm`, `actual_azure_tpm` |

Resource/model values above are current code-enforced intended settings, **not
fresh cloud-state verification**. Historical intended region is Spain Central;
actual `contract.region` remains a reviewed operator binding.

The financial structure remains `Contract` plus `one_call_contract`, catalog
`phase17hl-pricing-eur-202610/1`, pinned serialized catalog SHA-256
`dad37bc0f349cdfbea16e25cae028a0b5042e4e3e3daac4f141f9b566c5bc65e`.
It requires one attempt, zero fixed/extra charges, `fits(1)=true`, `fits(2)=false`
and approved EUR maximum greater than zero and at most 5. The prior validated
catalog calculation is EUR `0.028379091869065` for the full token reservation.
That calculation uses the public **synthetic review fixture**, not a current
commercial quotation. Neither that amount nor the historical EUR 5 ceiling is
present spending authority. Pricing mismatch or unsupported zero-extras assumptions
must stop the operator process for separate review, without changing the pin.

## E. Single-call safety

`SingleCallConfiguration` rejects changed source/schema, incompatible financial
contracts and insufficient shared capacity. `execute_stage` accepts only the
prepared first analysis, with no children and matching real scope/fixture/request
bindings. It invokes neither structural/root reduction nor Q&A, embedding or the
four-call launcher. `RunGuard.acquire` durably records the bounded reservation
before downstream admission/provider execution; a second call fails even with a
different logical identity. Governance identity and STARTED transitions separately
reject duplicates. The HTTPS session retains `max_retries=0`, `trust_env=false`;
redirects are forbidden. Maximum provider attempts is one; automatic retries and
fallback calls are zero.

Approval is verified before one-use, exclusive, fsynced consumption and the
exclusive live-start marker. Existing run records/markers prevent duplicate launch;
changing run directories or signatures does not clear persistent replay protection.
Failure does not refund an approval. Known usage settles before application
validation; missing/invalid usage remains UNKNOWN/unresolved, never zero. Original
financial history and obligations remain chargeable across policy/period boundaries.
Terminal sanitized `outcome.json` records acceptance, failure category, attempt
evidence and accounting; errors stop the run. Audit-write failures also fail closed.
No success or failure permits a second call within this operation.

## F. Reused operator evidence

This reconciles existing evidence; it does not repeat static compatibility tests
beyond the explicitly requested focused regression. Historical NOT VERIFIED items
are not promoted to completed checks.

| Condition | Latest evidence | Classification | Required next action |
|---|---|---|---|
| Static Azure/application compatibility | [20 October offline audit](phase_17hl_final_offline_azure_compatibility_audit.md), [22 October observability](phase_17hl_live_failure_observability_and_contract_options.md), current unchanged contract/focused tests | VERIFIED | Reuse; local schema validity does not certify future model acceptance |
| Deployment allocation/identity | [15 October final authorization §A](phase_17hl_final_operator_authorization.md): succeeded target/version/SKU, 30 RPM/30,000 TPM | REQUIRES REFRESH | Operator confirms this established target/allocation evidence still applies; no wholesale rediscovery required |
| Pricing structure / calculation | Same report: operator-approved EUR catalog/ceiling; [Attempt 5 assessment §G](phase_17hl_attempt5_readiness_authorization_assessment.md): exact pin and bounded arithmetic | VERIFIED (structure/arithmetic); REQUIRES REFRESH (commercial applicability) | Reuse pin/calculation; operator confirms current exact terms and supported absence of separate charges; earlier missing charge bases remain unverified |
| Governance/financial enforcement | Attempt 5 assessment §§F–H, F1, unchanged source and current focused accounting tests | VERIFIED | Reuse mechanism/policy evidence; no new authority, migration or budget pool |
| Current allowances and obligations | Attempt 5 assessment §G explicitly did not inspect protected stores | OPERATOR-OWNED | Inspect existing owner/tenant allowances, history and UNKNOWN obligations; preserve all prior debt/replay state |
| Identity and independent signing trust | Final authorization: RSA pair consistency only, provenance unresolved; Attempt 5 §H verifies mechanism offline | VERIFIED (mechanism); OPERATOR-OWNED (current identity/provenance/approval) | Reuse existing registration/trust; verify actual principal/permissions, independent key association and exact current approval |
| Credentials / timing | Final authorization §B and Attempt 5 §H: presence did not prove authority; no current validity established | OPERATOR-OWNED | Establish protected credential target/permissions and fresh token/deadlines; verify immediately before future launch |
| Shared capacity / consumers | Final authorization: historical allocation, dedicated deployment, separate ECI and AKS zero; complete shared-consumer attestation unresolved | REQUIRES REFRESH | Confirm current consumers/capacity; full 28,000 background reservation plus protected 2,000 interactive TPM requires 30,000 TPM |
| Exact current configuration/request/approval | Matching F1 source bindings here; private packet and actual-scope request not inspected | OPERATOR-OWNED | Finalize current exact-scope configuration and bindings through existing single-call workflow; no old helper pin bypass |
| Retention/review | Final authorization §A: 90 days, existing private audit storage, cleanup owner and human reviewer | VERIFIED (standing decision) | Carry forward existing decision; operator maps this run to those existing responsibilities without reapproving duration |

No demonstrated BLOCKED engineering condition remains. Previously missing
credential provenance, charge bases, complete consumer review, fresh identity and
signer provenance remain missing until the operator establishes them; elapsed time
and historical checklists are not evidence of completion.

## G. Operator preparation

Use the existing [single-analysis timing/preparation instructions](../../evaluation/phase_17hl_operator_approval.md#single-analysis-timing-and-preparation-handoff)
and current `foundry_single_call.SingleCallConfiguration` / `foundry_approval.bindings`.
The earlier four-call sections of the runbook and final authorization report supply
historical evidence, not the execution scope or audience for this handoff. Do not
use their four-call command, signing packet or stale helper constants.

1. Review the four source bindings above and frozen configuration/limits.
2. Confirm the established deployment, pinned commercial terms and allocation still
   apply; refresh only changed or execution-time facts, including shared consumers.
3. Confirm existing authority references, actual owner/tenant allowances and
   unresolved obligations; retain the standing storage/retention/reviewer decision.
4. Establish the real verified operator scope and protected configuration. Prepare
   the same fixture in that scope, obtain actual fixture/rendered-request digests,
   new request/run identities and validated complete configuration acknowledgement.
5. Through independent operator review/signing, obtain or verify a fresh approval
   bound to the exact current configuration and source, audience
   `polymind-single-analysis-live`. No prior approval is asserted suitable here.
6. Immediately before any future launch verify signature, unused ID, credentials
   and windows. Require `execution_not_before <= now < min(approval_expires,
   credential_valid_until)-600`; equality at cutoff is ineligible. Approval/token/
   credential final verification also requires more than 60 seconds remaining.
   Approval `exp` equals configuration expiry; `iat <= nbf < exp`, maximum 24-hour
   signed lifetime. API-key use deadline is an operator attestation.
7. Only after separate explicit user authorization and all existing gates pass,
   execute the governed **single-call** launcher once. This report supplies no
   automatic script, live command, signed artifact or permission to launch now.
8. Inspect sanitized terminal outcome and durable accounting/replay evidence.
9. Stop after that one accepted or failed attempt. UNKNOWN usage or failed audit
   requires investigation; it never permits retry, repair or ledger replacement.

Ready: source inventory, frozen experiment definition, regression evidence and
existing procedure references. Operator-owned: real identities, authority paths,
funds/obligations, actual-scope hashes, current configuration digest, credentials,
time/capacity attestations and independent approval. No placeholder UUID or purported
executable private configuration is provided.

## H. Test results, reuse and review

Newly executed with existing Python 3.10.13, no environment/package changes:

```text
"$PYTHON" /tmp/polymind-attempt5-final-verify.py snapshot
"$PYTHON" /tmp/polymind-attempt5-final-verify.py bindings
"$PYTHON" /tmp/polymind-attempt5-final-verify.py focused
```

The inspected driver invokes `python -m pytest -q -c <repository>/pytest.ini` with
exactly the seven module paths below, external basetemp/JUnit/cache paths, sanitized
application/credential environment, `/tmp/polymind-attempt5-final/work` CWD and public
tests symlink. `PYTEST_PLUGINS=polymind_e2e_offline_guard`,
`PYTHONPATH=/tmp:<repository>`, `PYTHONDONTWRITEBYTECODE=1`. The existing reviewed
guard installs socket/DNS monkeypatches and an audit hook before application imports,
counts attempts and fails swallowed attempts. Root conftest isolates implicit dotenv.
Bindings use the reviewed F1 binding script with the same isolation and guard.
This is Python-level denial, not an OS firewall or a claim about arbitrary native
subprocess networking. Selected synthetic harness tests mock transport and identity;
no unreviewed live-capable script or real launcher invocation was made.

| Selected module | Passed |
|---|---:|
| `tests/unit/test_http_cleanup.py` | 56 |
| `tests/integration/test_http_cleanup_governance.py` | 21 |
| `tests/integration/test_live_failure_observability.py` | 112 |
| `tests/integration/test_single_call_harness.py` | 46 |
| `tests/integration/test_single_call_preflight.py` | 28 |
| `tests/integration/test_final_offline_azure_compatibility.py` | 116 |
| `tests/unit/test_source_contracts.py` | 47 |
| **Total** | **426** |

Result: exit 0, **32.14 seconds**, failures 0, errors 0, skipped 0, warnings 0,
observed network attempts 0. Binding computation also recorded 0 network attempts.
Evidence: `/tmp/polymind-attempt5-final/{focused.log,focused.xml,focused-command.json,bindings.log}`.
No new tests were added. Regression fixtures exercise only ephemeral synthetic
RSA approvals, identities and disposable financial authorities; those are distinct
from live signing/consumption and live funds, all zero for this assessment.

Reused: F1 full regression **1,755 passed**, 42 existing warnings, 365.09 seconds,
zero failures/errors/skips/observed network attempts, including 77 F1 additions.
Matching post-fix fingerprints, the public source comparison and passing focused
tests support reuse; no trigger for another full run was found. Existing compileall,
lint-debt and portability evidence is reused, not newly claimed as executed.
Docker/build/cloud checks are inapplicable to this documentation-only assessment.

Self-review followed cleanup precedence, ownership, request boundaries, reservation/
settlement ordering, replay and sanitized terminal paths. No implementation finding
requires correction in this scope. Separate pre-commit review covers only the two
new Markdown deliverables: no secrets, protected contents, actual scope IDs, approval
artifact, execution script, dependency, policy/API change or historical report edit.
Final whitespace and public-file preservation checks passed. All 262 snapshotted
pre-existing public files remain unchanged by this task. Index remains empty.
`git status --short --branch` retains the existing dirty `master` tree, plus these
two new documents. `git diff --stat` remains **20 files changed, 832 insertions(+),
79 deletions(-)**; untracked deliverables are not included in that tracked statistic.

## I. Final decision

**ENGINEERING GO; OPERATOR PREPARATION READY; EXECUTION AUTHORIZED NOW NOT VERIFIED.**
No outstanding confirmed engineering blocker remains for single-analysis
preparation. The next operator action is review of this exact binding inventory,
then completion of the protected current configuration/evidence and independent
approval process above. Readiness is not permission to spend or execute.

Residual limits remain the unchanged external-session shutdown boundary, offline
inability to certify live-model acceptance, known prompt ambiguities, unknown
historical Attempt 4 predicate, and single-host persistent-state governance assumptions.
These do not justify a prompt/schema/policy change or another general audit here.

Paid inference calls, cloud operations, live financial reservations, live approval
creation/signing/consumption, protected record access, production/test modifications,
commits, pushes and staging: **0 each**. Only this report and its prompt were added.
Phase 17H remains PARTIAL; no next phase or live attempt was started.
