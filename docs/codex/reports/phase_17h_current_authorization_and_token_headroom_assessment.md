# Phase 17H — Current Authorization and Token Headroom Assessment

Assessment started 6 November and completed 7 November 2026 UTC. Repository HEAD:
`f6555f355fd765b3fbdad068d150144bfea94ccd` (`master`).
Scope: offline source review, public GitHub CI metadata, existing isolated offline
tests, arithmetic and the two requested documents. No implementation changes.

## Decision

**Four-call live execution: NO-GO / NOT AUTHORIZED.** Under the supplied November
allowance, **111,015 remaining tokens cannot cover the unchanged 112,000-token
maximum**. The 985-token deficit is a real worst-case authorization blocker. It is
**not an upfront 112,000-token ledger reservation or proof that call one will be
rejected**: governance reserves each rendered request and settles actual usage
before admitting the next. A run could fit, or could stop after paid partial work.
Low historical consumption cannot justify assuming completion will fit.

The best-supported option is **A: retain the contract and wait until 1 December
2026 00:00:00 UTC**, subject to a fresh accounting snapshot. An otherwise unused
115,305-token month has 3,305 tokens beyond this maximum. Reset does not release
unresolved obligations, reset a rolling request window, refresh credentials,
establish commercial applicability or grant execution approval.

There is also an important authority-selection uncertainty: the supplied balance
and five request slots resemble the legacy policy, whereas the optional scoped
evaluation overlay has larger limits. Historical activation is not current proof
that this operator's scope selects that overlay. **Resolve that discrepancy by an
operator-controlled read-only check before making any authorization decision.**
This assessment neither adopts a larger allowance nor changes any authority.

| Dimension | Classification | Basis |
| --- | --- | --- |
| Engineering readiness | GO | Source contracts and focused offline regressions pass; live quality remains unvalidated. |
| Operator identity | Historical PASS / Current PENDING | Operator reports successful OIDC and registration checks on 6 November; no current credentials inspected. |
| Governance authority | PENDING | Selection, scope, stored configuration and current obligations require private read-only reconciliation. |
| Monthly token headroom | BLOCKED | Supplied 111,015 versus unchanged 112,000 maximum; actual selected policy remains unverified. |
| Financial headroom | PENDING | EUR 4.991182682154170454 reported; applicable current prices and all charges unverified. |
| Azure deployment/quota | PENDING | Target is code-pinned; actual deployment, allocation and shared consumers unverified. |
| Independent approval | NOT AUTHORIZED | No current independent approval verified; no artifact opened, generated, signed or consumed. |
| Four-call live execution | NO-GO | Token maximum not covered and other current gates remain pending. |

**Can we safely authorize the four-call L1 evaluation under the current November
2026 token limits without modifying existing governance policies? No, on the
supplied evidence and unchanged full-maximum contract.** This does not mean the
implementation necessarily rejects the first call, or that every actual four-call
run would consume 112,000 tokens. A separately reviewed smaller configuration
could be feasible without policy changes, but is not established or approved here.

## Evidence boundaries and observed figures

The following are **timestamped operator-reported observations from 6 November
2026**, preserved as supplied, not fresh private-state verification:

| Metric | Owner | Tenant |
| --- | ---: | ---: |
| Daily tokens used | 0 | 0 |
| Monthly tokens used | 4,290 | 4,290 |
| Monthly tokens remaining | 111,015 | 111,015 |
| Monthly cost remaining | EUR 4.991182682154170454 | EUR 4.991182682154170454 |
| Unsettled reservations | 0 | 0 |
| Requests in rolling window | 0 | 0 |
| Remaining request slots | 5 | 5 |

The operator reports six settled historical reservations, zero active inference
calls, one historical output-limit failure, and no unresolved obligations.
November 1 Attempt 6 consumed 2,476 input plus 1,814 inclusive output = **4,290
tokens**, with **EUR 0.008817317845829546** catalog-accounted cost. The public
[Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md)
supports that historical attempt; it does not establish today's private balances
or an Azure invoice. Earlier October usage must not be added to November settled
usage merely because it remains in lifetime history.

The monthly limit inferred from the observations is `4290 + 111015 = 115305`.
The inferred EUR ceiling is exactly
`4.991182682154170454 + 0.008817317845829546 = 5.000000000000000000`.
Neither inference substitutes for reading the selected limits. Daily usage of zero
does not independently establish the daily allowance.

No private database, private configuration, signing key, token file, signed
approval, replay directory or durable model package was inspected. The model's
previous verification remains historical evidence in the
[operator preparation report](phase_17h_four_call_l1_operator_preparation_and_final_authorization_review.md).
This task did not acquire tokens or perform an OIDC/JWKS request. No Azure request,
paid inference, cloud modification, Kubernetes operation, real reservation or
authority mutation occurred. Existing offline tests use their established isolated
synthetic authorities and HTTP fixtures; these are not identities or approvals for
the real operator. Signing/consumption and live-launcher tests were not invoked.

## Repository and CI baseline

Initial `git status --short` was empty. HEAD is the documentation checkpoint
`f6555f355fd765b3fbdad068d150144bfea94ccd`, dated 2 November 2026 16:34:28 UTC,
`docs(phase17h): record four-call L1 operator readiness review`.
Read-only GitHub connector queries for this exact SHA returned
[Estudio PolyMind CI run 43](https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/41482828266),
push event, attempt 1, **completed/success**, started 2 November 16:34:40 UTC and
updated 16:41:26 UTC. The `build` job and imports/compile, automated tests, Helm,
Compose and Docker-build steps all succeeded. No remote jobs were triggered.
Test counts were not obtained from remote logs; this is exact-SHA CI metadata,
not a claim that a new complete suite or Docker build ran locally today.

Reviewed supporting documentation includes the
[G1/G2 engineering report](phase_17h_g1_g2_offline_engineering_and_integration_hardening.md),
[historical CI reconciliation](phase_17h_ci_failure_and_historical_contract_reconciliation.md),
[four-call preparation](phase_17h_four_call_l1_live_preparation_and_authorization_readiness.md),
[operator preparation](phase_17h_four_call_l1_operator_preparation_and_final_authorization_review.md),
[evaluation activation](phase_17hl_evaluation_policy_activation.md),
[Foundry runbook](../../evaluation/phase_17h_foundry_validation.md) and
[approval procedure](../../evaluation/phase_17hl_operator_approval.md).
Historical reports retain their own timestamps and scope; they do not authorize
remaining calls or reuse Attempt 6's consumed single-analysis approval.

## Implementation map and engineering contracts

Paths below refer to the assessed HEAD. No interface, configuration fingerprint
or source binding was changed.

| Contract / limit | Exact implementation responsibilities |
| --- | --- |
| Four inference calls, dependencies, no paid retries | [foundry_preflight.py](../../../tests/performance/foundry_preflight.py) `execute`: four-page `pdf` fixture, one chunk and two reducers, worker `RetryPolicy(max_attempts=1)`; `publish` bridges to `questions`; [foundry_l1.py](../../../tests/performance/foundry_l1.py) `LaunchConfiguration.bounded` requires `attempts == 4`, `contract.fits(4)`. |
| Cumulative input/output, call ceilings and monetary maximum | [foundry_budget.py](../../../tests/performance/foundry_budget.py) `Contract` fields, `valid`, `cost`, `fits`; `RunGuard.acquire`, `finish`, `stop`. L1 additionally requires total input <=100,000, total output <=12,000, output exactly 3,000, context <=28,000 and RPM 1. |
| Rendered G1 input and child admission | [managed.py](../../../documents/digestion/managed.py) `StageProfile`, `ManagedSettings.stages`, `ManagedSynthesisInference.profile`, `render`; [sizing.py](../../../documents/digestion/sizing.py) `escaped_size`, `result_contribution`, `child_contribution`, `analysis_size`, `reduction_size`; [planning.py](../../../documents/digestion/planning.py) `check_request`, `_build` / `reduce_group`. |
| G1 byte limits | L1 `execute` fixes stage input at 24,800 bytes, output at 3,000; capability overhead/safety 100 each, context 28,000. Managed result raw/canonical limits independently 10,000 bytes; HTTP envelope 26,192 bytes; child material <=7,000 including escaping, evidence, links and 1,024 wrapper bytes. No truncation or repair. |
| Strict G2 evidence and lineage | [validation.py](../../../documents/digestion/validation.py) `EvidenceIndex.resolve`, `validate_result`, `inherited_summary`, `make_digest`: source identity/span/block checks, authorized evidence, deterministic claim IDs, complete source and child-claim coverage, qualifications/conflicts. |
| Checkpoints and finalization | [workflow.py](../../../documents/digestion/workflow.py) `prepare`, `admit`, `DigestionHandler._load`, `request`, `__call__`, `load_digest`: deterministic plan equality, immutable references and parents, plan/profile binding, reopening and revalidation of every checkpoint; actual child material checked before checkpoint commit. |
| Stage selection | `ManagedDigestionHandler.analyze`: chunk, structural level 1, root level 2. Configured `intermediate` stage is unused by this one-chunk fixture. G2 two-chunk regression uses five synthetic inference calls; it is not the live four-call plan. |
| Provider protocol and output controls | [foundry_recalibration.py](../../../tests/performance/foundry_recalibration.py) `candidate_capability`, `deployment_configuration`; [structured.py](../../../llm/structured.py) `CapabilityProfile`; [openai_compatible.py](../../../llm/openai_compatible.py) `execute`, `_usage`; [bounded_http.py](../../../llm/bounded_http.py) `validate_request`, `request_json`, `result_text`. |
| Provider settings | Strict digestion `managed-generation/2`, `managed-prompt/4`, `azure-strict/1`; Q&A JSON-object contract. `max_completion_tokens=3000` includes reasoning; `reasoning_effort=low`, no temperature/tools/streaming, one bounded POST, live `readiness_retries=0`. Output truncation and malformed usage fail; known usage survives later rejection. |
| Grounded Q&A | [analysis.py](../../../documents/publication/analysis.py) `DocumentAnalysis.analyze`: original-source citations, generation/version pins, full escaped envelope <=24,800 bytes, 3,000 output in this composition, citation validation and pin revalidation. |
| Governance | [ledger.py](../../../governance/ledger.py) `Price`, `PricingCatalog`, `Limits`, `EvaluationBinding`, `QuotaPolicy.select`, `GovernanceLedger.reserve`, `transition`, `settle`; [execution.py](../../../governance/execution.py) `GovernedExecution.execute`. |
| Shared admission | [admission.py](../../../llm/admission.py) `AdmissionPolicy.bounds`, `SQLiteInferenceAdmission.acquire`, `finish`; [foundry_l1.py](../../../tests/performance/foundry_l1.py) `Runtime.wait` and `LaunchConfiguration.bounded`. |
| Identity and authorization | [identity.py](../../../security/identity.py) `OIDCSettings.trusted_urls`, `OIDCVerifier.verify`; [models.py](../../../security/models.py) `Principal`; [authority.py](../../../security/authority.py) `_principal`, `authorize`, `snapshot`, `revalidate`. |
| Independent approval and replay | [foundry_approval.py](../../../tests/performance/foundry_approval.py) `ApprovalTrust`, `bindings`, `verify_artifact`, `consume`; launcher `configuration_digest`, `verify_approval`, `launch`, `generation_contract_digest`. |

The successful offline E2E verifies the one-chunk → structural → root DAG,
reopened checkpoints, COMPLETE digest with full coverage, authorized publication,
retrieval and Q&A through actual application acceptance. Structural validity is
not semantic quality. `DocumentAnalysis` can return insufficient evidence without
inference, and a schema-valid abstention can yield `questions.status=COMPLETE`.
Eventual acceptance must independently require exactly four attempts, correct
page-one valve-5153 finding, supported original citations and human review. Do not
add a call to make a short/failed run appear complete.

## Ledger accounting semantics

`GovernanceLedger.reserve` evaluates tenant rows and then owner rows filtered
within that tenant in one atomic transaction. Either scope can deny. It reads all
reservation history in scope, irrespective of the row's stored policy version;
switching a policy does not erase prior obligations or current-period usage.
Only successful admission inserts a reservation; a denial writes an audit event.

UTC boundaries derive from `datetime.fromtimestamp(now, timezone.utc)`: daily
start is the same UTC date at midnight; monthly start is day 1 at midnight.
Settled usage/cost counts when reservation **`created >= boundary`**, not when
settlement occurs. Thus an October-created call settled in November belongs to
October once settled; while unresolved it counts in every current period.
At 1 December 00:00 UTC a new reservation belongs to December. The code has no
upper timestamp filter; operators should flag future-dated/corrupt records rather
than assuming they are excluded.

| State | Token/cost accounting | Concurrency and requests |
| --- | --- | --- |
| SETTLED | Actual input + actual output; `actual_cost`; only current day/month by creation time. Full known usage settles even if domain validation subsequently fails. | Not active. Still a request while inside its rolling window. |
| RELEASED | Excluded from token and cost obligations. | Not active. Still a request inside its rolling window. |
| RESERVED | Full reserved input/output and cost in current day, month and outstanding-token cap, even if created in an earlier period. | Active in its workload; counts as a recent request when in window. |
| ADMITTING | Same full obligations as RESERVED. | Active; no provider work yet. |
| STARTED | Full obligations until settlement, including across periods/restart. | Active. |
| UNKNOWN | Full reserved obligations, even with partial actual counts and across periods/restart. | Not in governance's active-state list, but continues consuming outstanding/daily/monthly tokens and cost. The affected run guard blocks continuation. |

Request windows are rolling, **`created > now - limits.window_seconds`**, across
all row states, including RELEASED and SETTLED. Equality at the lower boundary is
excluded. Neither midnight nor a month boundary alone resets a rolling 86,400-second
window. Active governance concurrency includes RESERVED/ADMITTING/STARTED in the
requested workload; unresolved tokens are shared across workloads.

Each new reservation must fit outstanding reserved tokens, daily and monthly
tokens, monthly cost, request count and workload concurrency for **both** scopes.
Existing unsettled full obligations are added to the new call; they do not expire.
Settlement with both nonnegative counts records actual counts and Decimal cost;
missing counts become UNKNOWN. Reconciliation may move UNKNOWN to SETTLED with
consistent evidence, never by assuming zero. Duplicate `(tenant, owner, job,
step, attempt)` returns the same ticket only for identical reservation parameters;
the subsequent state transition prevents executing that attempt twice. Distinct
stage identities in the same evaluation produce separate rows and see the
preceding stages' settlements.

`governance/evaluation.py:impact` mirrors these boundaries, actual-versus-reserved
rules and request counts for read-only analysis of supplied rows. Production
`usage`/`tenant_usage` methods are not safe substitutes for this task's pure
read-only check: constructors/transactions and authorization can write audits.

### Policy selection discrepancy

`QuotaPolicy.select(scope)` chooses `EvaluationBinding.limits()` only for an exact
allowlisted `Scope`. That overlay currently defines 16 requests / 86,400 seconds,
112,000 simultaneous reserved tokens, 500,000 daily tokens, 1,500,000 monthly
tokens and EUR 5 monthly, concurrency 1 for each workload. Other scopes, including
an unlisted owner in the same tenant, get base owner/tenant limits. Selected
tenant limits still account for all tenant consumers.

The legacy `phase17hl-l1/2` examples and current supplied figures imply 5 requests
and 115,305 monthly tokens. The historical
[activation report](phase_17hl_evaluation_policy_activation.md) says an overlay was
installed in October; it is not proof of current configuration or scope selection.
With a genuinely applicable 1,500,000-token overlay and only 4,290 current usage,
remaining tokens would be 1,495,710, not 111,015. Possible explanations include a
base-policy dashboard, a different scope, different configuration, or an observation
that intentionally reports base limits. None is established here. No policy,
allowlist or path may be changed to make an observation fit.

## Reservation sequence and the 985-token question

There are three independent accounting layers:

1. **Owner/tenant governance:** `GovernedExecution.execute` computes
   `len(canonical({system, data, schema}).encode()) + overhead + safety`, reserves
   that input plus the requested output, transitions RESERVED → ADMITTING, then
   requests downstream admission. Downstream refusal releases this governance
   reservation. Before the provider it revalidates authorization/fencing and
   transitions to STARTED. Its `finally` settles known actual usage or records
   UNKNOWN, then finishes downstream accounting. This completes before the next
   synchronous call returns to the workflow.
2. **Run guard:** downstream is `RunGuard`, which checks the rendered estimate
   against contract ceilings but durably records the **full configured per-call
   allowance** (25,000/3,000). `fits(next_call_count)` checks full ceilings,
   cumulative limits and computed maximum cost. Settlements never refund these
   full per-call run records. There is no upfront four-call ledger debit, but the
   reviewed run ceiling remains 100,000/12,000 independently of actual refunds.
   Unknown/inconsistent/excess usage, downstream denial or provider failure stops
   the run; a new approval cannot be used to conceal an unresolved run.
3. **Shared provider admission:** `SQLiteInferenceAdmission.acquire` reserves the
   submitted rendered estimate plus output in a rolling 60-second window.
   `finish` records usage/outcome and releases its active slot, but does **not**
   refund that minute's token or request allowance. Active calls retain slots
   indefinitely until explicit completion. All consumers must share the same
   database, quota key and byte-identical policy.

Thus the launcher does **not** reserve 112,000 tokens upfront or per stage group.
It reserves per inference call, including a separate final Q&A call. Strict
validation/checkpoint failures after a response do not undo paid accounting.
If downstream admission fails after the run guard recorded a call, the durable run
record remains unresolved and the run stops even though governance was RELEASED.
Automatic paid retry count remains zero.

`LaunchConfiguration.bounded` checks `contract.fits(4)` against declared cumulative
and monetary ceilings; it does not compare all 112,000 tokens or the full monetary
maximum with the live ledger balance before call one. With no other blockers,
111,015 tokens can cover a first request of at most 28,000. Later calls see actual
settled usage. In a nominal worst case, three calls consume 84,000 and leave
27,015, insufficient for a fourth 28,000 reservation. Rejection can therefore occur
late. A smaller actual reservation or prior actual usage could make it fit; there
is no guaranteed late rejection either.

Conservative rendered estimates are not the same as hard actual-usage bounds:
`GovernanceLedger.settle` does not cap actual counts at its reservation, and
`RunGuard.finish` checks actual input against the contract's 25,000, not the
smaller rendered estimate. Do not prove worst-case completion by treating a
historical or estimated rendered count as an enforced billed-usage limit.

| Quantity | Meaning / evidence |
| --- | --- |
| 112,000 | Theoretical unchanged contract maximum: 4 × (25,000 + 3,000). Not one governance reservation. |
| <=28,000 per call | Nominal ceiling; governance/provider reserve the actual conservative rendered estimate plus 3,000 output. |
| 11,459 chunk; 16,242 each reducer | Historical public-scope G1 planning estimates in the 2 November preparation report, not current private-scope rendering or usage. |
| 11,626 / 11,142 / 10,828 / 8,278 inputs, each plus 3,000 output | Historical synthetic-envelope observations for chunk/structural/root/Q&A from that report. Depend on fixture-generated outputs; not live bounds or billed usage. |
| Existing offline HTTP usage | Synthetic reports used to exercise settlement. Not Azure consumption and not evidence of model cost. |
| Attempt 6: 2,476 / 1,814 | Historical provider-reported actual tokens for one analysis; catalog cost EUR 0.008817317845829546. Not a four-call forecast or independently verified invoice. |

The small deterministic source does not demonstrate that all nominal ceilings
are necessary. G1 already constrains child material and the accepted DAG has only
one child per reducer. However, actual generated claims, escaping, inherited
annotations, Q&A retrieval material and output/reasoning vary. The prior
output-limit failure is evidence against silently reducing output allowance.

## Alternatives, without implementation or authorization

| Option | Feasibility and risk | Required evidence / independent approval |
| --- | --- | --- |
| **A. Preserve contract; wait for December** | Best supported. At 1 December 00:00 UTC, settled November-created usage drops from the month; unused base limit 115,305 covers 112,000 with 3,305 spare. Conditional on no new usage, unresolved carryover or policy mismatch. Rolling windows are separate. | Fresh selected-policy/owner/tenant snapshot, other-consumer quiescence/capacity evidence, prices/charges, identity/credential lifetime, artifacts and execution window. **Fresh independent approval required**; historical approvals/windows do not roll forward. |
| **B. Smaller independently reviewed contract** | Partially supported by existing configuration: lower input per call and totals are permitted. Output must remain exactly 3,000 and attempts exactly four in the current L1 launcher. Planning and Q&A limits are fixed in `execute`/`questions`; lowering guard input alone can reject a valid later request after paid work. No automatic profile rescaling. | Prove all rendered requests, G1/G2 bounds, unchanged DAG and actual-usage contract fit; review the new complete configuration and SHA-256. **Fresh independent approval required**. No policy increase needed if it fits existing limits. Current report does not establish that proof. |
| **C. Existing maximum; sequential settlement** | Implemented mechanics permit actual refunds in governance, never in the run guard or provider minute window. Could finish below November limit; could stop after one to three paid calls or an UNKNOWN obligation. Does not fund full approved maximum. **Not recommended as justification for full-run authorization under supplied allowance.** | Fresh balances and explicit review of partial-run exposure would still be needed. **Fresh independent approval required**, but approval does not override denial or supply missing headroom. |
| **D. Formal policy revision** | Technically possible only as separately governed work; not within this immutable assessment. Configuration/ledger exact-match checks reject edits in isolation. Existing overlay may already apply, but that must be verified, not newly selected by altering scope. | Proper authority, rationale, impact/history accounting, backup/rollback and independently reviewed synchronized configuration. `evaluation_policy` rejects replacing an existing overlay; `apply_evaluation_migration` supports only its narrowly guarded legacy transition, not arbitrary increases. **Fresh independent approval required**. Do not increase limits simply to force the experiment. |

For B, keeping four outputs at 3,000 means a uniform input ceiling must be at
most `floor((111015 - 12000) / 4) = 24753`. An illustrative **24,750 input**,
**99,000 total input**, unchanged 12,000 total output gives **111,000**, leaving
only **15 tokens** against the supplied monthly balance. Pure `Contract` validation
and `fits(4)` accept these illustrative token settings with synthetic prices.
They are neither a candidate private configuration nor an approved recommendation.
Keeping input at 25,000 while reducing only total input to 99,000 fails `fits(4)`.

The unchanged stage/Q&A renderers admit envelopes up to 24,800 + 200 = 25,000
estimated input, greater than 24,750. A tighter contract changes admission and
actual-usage stop thresholds; it does not automatically change prompts, model,
reasoning or completion settings. Changing the stage profiles to align them would
alter prompt/configuration bindings and requires separate engineering review.
Historical contracts remain serialized/fingerprinted as before; do not mutate
old records. Smaller output or arbitrary per-stage budgets are not exposed as
safe L1 configuration-only alternatives at this HEAD.

## Identity, independent approval and execution window

The reported 6 November verification is **Historical PASS**, not evidence of
current token validity. `OIDCSettings` for `entra_v2` pins the canonical tenant
UUID, API audience UUID, tenant-specific v2 issuer and JWKS URL. `OIDCVerifier`
requires RS256, signature/key validation, exact issuer/audience/tenant,
`ver=2.0`, delegated `access_as_user`, user identity, valid exp/nbf/iat types and
relationships, and exactly `PolyMind.L1Operator`. That role grants only
`PUBLICATION_MANAGE`; owned-resource permissions remain in SecurityAuthority.
Derived owner/tenant scope binds issuer, tenant identity and `sub`, not email or
an interchangeable object-ID claim. `_principal` requires the same registered,
enabled identity, permissions and kind. Snapshots revalidate expiry and epochs.
Live `launch` authorizes an existing registration; it does not register a new user.

The inference credential is a separate secret from the operator API token.
Selected authentication, target/audience/access and attested credential validity
must cover the window. No existing token's lifetime or current Azure credential
validity was checked here.

`ApprovalTrust` requires independently provisioned live RSA public trust
(2,048–8,192 bits), operator issuer/subject/tenant and persistent replay location.
`verify_artifact` requires exact RS256 protected header, issuer
`polymind-operator-approval/1`, audience `polymind-l1-live`, purpose live, fresh
canonical UUID ID, exact claim set and exact full configuration/identity/target/
budget/limit/expiry binding. Single-analysis approvals have a different audience.
The canonical configuration SHA-256 and explicit acknowledgement must match;
changes to limits, policies, artifacts, pricing or execution times invalidate the
old binding. `generation_contract_digest` additionally binds its explicit source
inventory; that inventory is not every transitive source file, so exact HEAD and
reviewed tree still matter.

`consume` uses exclusive creation and file/directory fsync in a persistent replay
directory independent of the run audit directory. The same ID cannot be reused
after restart or key changes. `launch` also checks existing run records and writes
`live-started.json`. Consumption precedes local embedding setup: setup failure
does not refund approval. Never erase markers or replace authorities for recovery.
This is established single-host protection, not distributed or hostile-host proof.

Source window rules are: configured start plus 600 seconds must be strictly less
than approval/credential expiry; configuration validation also requires more than
600 seconds remaining at validation/launch. Start requires `now >=
execution_not_before`. Signed `iat <= nbf < exp`, at most 86,400 seconds from issue
to expiry, exact configured approval expiry; signature verification and runtime
require the earliest approval, credential or principal expiry to exceed `now+60`.
`Runtime.wait` checks cancellation and expiry while pacing. Allow time for the
three >=61-second inter-call gaps plus provider and local processing; the schema's
minimum lifetime is not a guarantee every run completes within its window.

All current identity, authority and independent approval gates remain PENDING /
NOT AUTHORIZED until verified during an eventual separately authorized window.

## Financial and Azure capacity evidence

`Price.cost` uses Decimal precision 60; `money` rejects floats/bools, negative,
nonfinite or overprecise monetary values. `PricingCatalog` requires operator
approval, unique provider/model prices and an effective date; `price` selects by
provider and served deployment/model string. Governance rejects future-effective
catalogs. A date, catalog pin or approval boolean does **not** verify present
commercial applicability, region, SKU, model version, taxes or conversion.

For current applicable positive EUR rates `ri`, `ro` per power-of-ten unit `U`,
aggregate fixed upper bound `F`, aggregate extra upper bound `E`, and ceiling `M`:

```text
token_upper = (100000 * ri + 12000 * ro) / U
run_upper = token_upper + F + E
require run_upper <= M <= Decimal('5')
require run_upper <= current owner AND tenant remaining financial headroom
```

For B use its reviewed four-call token ceilings. Compute with Decimal strings,
precision 60, and retain exact serialized values. Count fixed/extra bounds once,
not per call; output includes reasoning, with no assumed caching discounts.
`Contract.cost` adds fixed/extra bounds and `fits` checks the declared maximum;
governance reserves and settles **token cost only**. No automatic run-level
headroom lock includes external charges. Those obligations and shared activity
need independent reconciliation. `Contract.cost` combines Decimal results in the
ambient Decimal context, whereas `Price.cost` explicitly uses precision 60; the
operator's independent 60-digit calculation should also check rounding-sensitive
edges. No implementation precision change was made during this assessment.

Historical one-call full-token catalog cost EUR 0.028379091869065 gives a
four-call comparison of **EUR 0.113516367476260** (zero historical fixed/extra),
leaving **EUR 4.877666314677910454** against the supplied balance. This is
comparison arithmetic, **not a current EUR quote, invoice or spending authority**.
The nominal EUR 5 allowance itself exceeds the reported available balance by
EUR 0.008817317845829546. Authorization must use a verified all-in upper bound
that fits both balances; neither a low historical cost nor `maximum=5` proves it.

| Required evidence | Exact content needed before approval |
| --- | --- |
| Commercial catalog | Timestamped authoritative applicable EUR input/output prices and unit, account/offer or agreement, effective period, source/reference and approver; confirm applicability to exact deployment, model/version, SKU and region. Reconcile the pinned October catalog with present terms; do not silently replace it. |
| Target | Resource `epolymind-foundry-dev-susanta`, deployment `epolymind-gpt-54-mini`, model `gpt-5.4-mini`, version `2026-03-17`, `GlobalStandard`, allowlisted HTTPS v1 endpoint and response aliases. Historical region `spaincentral` is not a fresh verification; actual region must equal reviewed `contract.region`. |
| Incremental charges | Supported upper bounds for fixed/reserved deployment charges, network/storage/monitoring and applicable taxes/currency conversion; distinguish sunk costs from incremental evaluation exposure. A zero must have evidence. |
| Remaining finances | Current owner and entire tenant selected limits, actual current-month catalog usage, all unresolved reserved costs across periods, unrelated shared consumers and external charge obligations; reconciliation with provider/billing evidence where available. |
| Azure allocation | Timestamped control-plane/portal evidence of actual deployment RPM/TPM, SKU capacity and relevant shared pool/subscription/region consumers. No inference probe required. Source configuration alone does not attest allocation. |
| Shared provider authority | Existing path/key/policy fingerprint, all consumers using that authority, active and recent-minute requests, protected interactive reserve, stricter operational reservations and actual availability for the whole window. |
| Pacing/concurrency | One outstanding run call, RPM 1, >=61 real seconds between starts; four calls require at least 183 seconds between first and fourth starts. Candidate shared policy: total RPM 2, TPM 30,000, concurrency 2, protected interactive RPM 1 / TPM >=2,000 / slot 1, per-job RPM/concurrency 1. Full background 28,000 plus reserve needs 30,000; larger existing reserve may prevent full-ceiling compatibility. |
| Reservation compatibility | Owner/tenant request slots for all four, daily/monthly/outstanding/cost capacity; shared minute/request/active capacity; `fits(4)` and every actual rendered request under selected contract. No stale snapshot guarantees exclusive future capacity. |

No authenticated Azure discovery or public price lookup was performed for this
assessment; all present applicability and allocation claims remain pending.

## Precise remaining read-only operator checks

These are instructions for the operator, **not executed actions or permission
to launch**. The immediate next action is to reconcile effective policy selection
and the reported balance on the **existing** authorities. With separate read
authorization, use SQLite URI `mode=ro`, `PRAGMA query_only=ON` and a read
transaction on each existing file; do not instantiate SecurityAuthority,
GovernanceLedger, SQLiteInferenceAdmission or RunGuard. Do not use `immutable=1`
on a potentially active WAL database, or make a copied/replacement authority.

1. On governance, read `SELECT policy,catalog FROM configuration WHERE singleton=1`
   and parse as existing `QuotaPolicy`/`PricingCatalog` values without constructing
   a database object. Compare byte serialization/fingerprints with approved
   configuration. For the already verified real scope, call pure
   `QuotaPolicy.select(scope)` and record selected version and both limits.
   Check any `evaluation.scopes`, existing bound authority paths/key and provider
   policy digest; report only sanitized match results, never credentials/claims.
2. Read **all tenant rows**, with bound real-tenant parameter:
   `SELECT owner,state,created,input,output,cost,actual_input,actual_output,actual_cost,workload FROM reservations WHERE tenant=?`.
   Keep the tenant-wide list and owner-filtered list. At one recorded UTC timestamp,
   reproduce `reserve` / pure `impact` exactly, including all unsettled states,
   RELEASED request counts, strict rolling-window boundary and creation-time
   periods. Record state counts, request-window and active counts by workload,
   actual current-day/month tokens/costs, unresolved amounts of any age, and
   remaining limits. Confirm expected six settled rows and no new obligations;
   account for other owners. Check schema/integrity read-only as appropriate.
3. On shared admission, read `SELECT policy FROM quota_policy WHERE quota=?` and
   `SELECT scope,job,workload,started,estimated_input,reserved_output,active,outcome FROM inference_calls WHERE quota=? AND (started>? OR active=1)`
   with existing quota and `now-60`. Compare policy fingerprint and reproduce
   total/background/per-job recent and active gates. Confirm no unreconciled
   external work; no minute refund from actual usage.
4. Independently confirm the existing enabled registered identity/tenant/permission
   match and authority health without calling audit-writing APIs during the
   read-only check. An eventual authorized window requires fresh cryptographic
   authentication using the established utility/verifier, without publishing tokens.

Record clock, scope-match booleans, selected policy version, catalog/policy pins
and sanitized numeric results. A consistent/quiescent snapshot is necessary;
separate database reads are not an atomic reservation of future shared capacity.
If actual valid selection contradicts 111,015, obtain a corrected operator
observation and reassess; do not silently substitute the overlay allowance.

After reconciliation, retain NO-GO and choose A unless a separate B review proves
all bounds. For A repeat the same checks after 1 December reset. Refresh exact
commercial target/charge/quota/shared-consumer evidence, local embedding hash and
storage, registered identity, credential lifetime and execution window. Only
after all readiness gates pass should the operator seek a **new independent
approval for the exact configuration** and separate explicit execution
authorization. This task does not authorize signing, consuming or running it.

## Executed offline checks and coverage limits

Focused command (existing installed Python 3.10.13, no dependency installation):

```bash
PYTHONPATH=/tmp/phase17h-headroom-assessment-20261106:. \
PYTHONDONTWRITEBYTECODE=1 PYTEST_PLUGINS=offline_guard \
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
python -m pytest -q -p no:cacheprovider \
  tests/unit/test_governance.py \
  tests/unit/test_evaluation_governance.py \
  tests/unit/test_foundry_preflight.py \
  tests/unit/test_foundry_30k.py \
  tests/unit/documents/test_managed_sizing.py \
  tests/integration/test_phase17hl_offline_e2e.py \
  tests/integration/test_phase17h_two_chunk.py \
  --junitxml=/tmp/phase17h-headroom-assessment-20261106/focused.xml
```

**Exit 0: 178 passed, zero failures/errors/skips/xfails, 40 warnings, 49.85 s.**
Warnings are existing JUnit `record_property` / xunit2 compatibility warnings.
The assessment-only `/tmp` plugin installs socket/DNS denial before collection;
E2E modules also fence sockets and subprocess exit tests install their own denial.
No application acceptance, validator, accounting or stop condition was bypassed.
No test skip/xfail or new repository test was added. Synthetic transport responses
are the existing offline test mechanism, not fabricated live success evidence.

Coverage includes atomic owner/tenant admission, identical-attempt deduplication,
RELEASED/UNKNOWN/actual settlement, historical usage across policy selection,
daily/monthly exhaustion, unresolved carryover across months, rolling request and
provider windows, persistent nonrefunded run allowances, unknown/excess usage,
shared admission/concurrency, G1 escaped child bounds and rejection, strict G2
lineage/coverage, checkpoint reuse/tampering, publication, citations and Q&A.
`test_l1_configuration_contract_without_signing` exercises configuration/scope
binding without approval creation. Approval source and existing regression cases
in `test_foundry_approval.py` were reviewed, **not run**, because they generate and
consume synthetic signed artifacts; this task prohibits signing/consumption.
Exact-HEAD CI provides prior complete-suite success, not current live approval.

A separate pure offline `arithmetic.py` probe used Decimal precision 60 and
existing `Contract` validation. Exit 0 confirmed the 985 deficit, 115,305 inferred
limit, 24,753 arithmetic maximum uniform input, 111,000 illustrative exposure,
15-token margin, December 3,305 margin, historical financial comparison and
`fits(4)` rejection when only cumulative input is reduced. It creates no
principal, authority, provider, reservation or launch configuration. Its network
counter recorded zero blocked attempts. Temporary outputs are outside Git.

Remaining regression gaps relevant to a future B review: no dedicated end-to-end
case at exactly this November 111,015 balance demonstrating late denial versus
settlement recovery; no regression proves every accepted G1 result and Q&A
envelope fits a 24,750 (or other smaller) L1 input contract; existing accounting
tests do not explicitly pin all UTC midnight/month-start equalities and a
cross-boundary settlement's creation-time attribution. These source conclusions
are not mislabeled as newly executed test cases. Add such coverage only in a
separately scoped engineering task, with unchanged acceptance rules.

No full local suite, compileall, Docker, Compose, Helm, formatting tool or cloud
validation was run: this is a documentation-only assessment with focused offline
verification requested, and exact-HEAD CI already records broader checks. No
application code or dependency changed.

## Self-review, pre-commit review and final state

Self-review checked all three accounting layers independently, policy selection
and tenant history, unknown/failed obligations, conservative estimates versus
actual usage, partial-paid-run failure paths, smaller-contract configuration
limits, independent signatures/window/replay, Decimal calculations and external
commercial uncertainty. The identified selection discrepancy and missing reduced-
contract envelope proof remain explicit pending items, not hidden PASS claims.
Provider-neutral inference, strict evidence, G1/G2 and historical compatibility
remain intact because no implementation changed.

Separate pre-commit review is limited to the two new Markdown deliverables:
source links, financial figures, command outcomes, secrets/private-artifact
exclusion, absence of real identities/credentials or runnable live approvals,
unrelated changes and unsupported authorization claims. No secret/configuration
file, generated test output or temporary script is included in the deliverables.
Final `git diff --check` exited 0. A separate scan of both new files found no
trailing whitespace or private-key/JWT material; all **31 relative file links**
resolved. `git diff --no-index --check /dev/null <new-file>` produced no whitespace
diagnostics for either file (exit 1 represents the new-file difference).
JUnit independently records 178 tests, zero failures/errors/skips, 49.847 seconds.
No staging, commit, push, branch change or other Git mutation occurred.

Final `git status` reports branch `master`, no tracked modifications or staged
changes, and exactly these two untracked files:

```text
docs/codex/prompts/phase_17h_current_authorization_and_token_headroom_assessment.md
docs/codex/reports/phase_17h_current_authorization_and_token_headroom_assessment.md
```

`git diff --stat` and `git diff --cached --stat` are empty because the deliverables
remain untracked. The source HEAD is unchanged; no commit or push occurred.

Only the matching prompt and this report are intended repository changes.
**Phase 17H remains PARTIAL; live inference remains NOT AUTHORIZED.**
