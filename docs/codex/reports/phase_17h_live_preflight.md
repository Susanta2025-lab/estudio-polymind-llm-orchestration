# Phase 17H-L: L0 preflight and operator handoff

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

Historical approval note: the issuer-signed JWT claim requirement recorded below
is superseded by the [separate operator approval implementation](phase_17hl_operator_approval_report.md).

> Current status: see **Final technical readiness and L1 handoff — 2026-10-14** below. Earlier sections preserve historical evidence.

Date: 2026-10-13. **L0 — PARTIAL.** Zero-cost inspection, financial guard,
offline workflows, tests, configuration/cost template and approval checklist are
prepared. Actual deployment/capability/price/quota/identity prerequisites cannot
be verified from absent configuration. An operator-bound live launcher and the
complete real-output request envelope remain blocked; the delivered CLI exposes
only offline stages. This is not a claim that all requested live preparation is
ready or that model calls may begin.

**L1 — NOT STARTED, AWAITING APPROVAL.**
**L2 — NOT STARTED, AWAITING APPROVAL.**

## Baseline and scope

Initial `git status --short --branch` returned only
`## master...origin/master`. `git rev-parse HEAD` returned exactly
`af4a7a076c918ef13aea05d74bf239c0af909133`. Initial `git diff --check` had no
output. No existing changes needed preservation; no branch/index/history changes
were made. The prior Phase 17H 732-test baseline was not rerun.

Read root AGENTS.md, the requested 17H report/methodology/observations/readiness,
17E/17G report sections and security contract, provider/factory/structured/admission
modules, managed digestion/workflow, governance execution/ledger, and the versioned
quality fixture. Additional reads resolved concrete dependencies: planning/profile
bounds, durable retry settings, private database foundation, existing managed and
governance tests, fixture generator/evaluator, publication analysis/retrieval and
authorized service wrappers. No model discovery or cloud resource inspection ran.

All changes are new evaluation/test/documentation files. Production provider,
application, graph, document, security and governance APIs are unchanged. No SDK,
dependency, Docker, Helm, model runtime or database migration was introduced.

## Configuration facts and missing prerequisites

Presence-only inspection of the process and root `.env` found **all 17** of these
names absent in both locations: `INFERENCE_PROVIDER`, `OPENAI_COMPATIBLE_BASE_URL`,
`OPENAI_COMPATIBLE_API_KEY`, `OPENAI_COMPATIBLE_MODEL_MAP`,
`DOCUMENT_INFERENCE_CAPABILITY`, `DOCUMENT_INFERENCE_PROFILES`,
`DOCUMENT_DIGESTION_PROFILE`, `API_AUTH_MODE`, `OIDC_CONFIGURATION`,
`SECURITY_AUTHORITY_PATH`, `GOVERNANCE_ENABLED`, `GOVERNANCE_AUTHORITY_PATH`,
`GOVERNANCE_PROVIDER_PATH`, `GOVERNANCE_PROVIDER_KEY`, `GOVERNANCE_POLICY`,
`GOVERNANCE_PRICING`, and `GOVERNANCE_PROVIDER_POLICY`. The `.env` file exists;
no values were emitted or copied. No secret was fetched.

| Requirement | Known | Missing / decision |
| --- | --- | --- |
| Endpoint | Adapter appends `/chat/completions`; candidate Azure v1 base ends `/openai/v1` | Actual endpoint and compatible contract |
| Deployment/model | `summarization` digestion; `general` question role | Exact deployment, underlying model/version and returned aliases |
| Authentication | Current adapter sends static Bearer header | Supported credential mechanism, audience, role, lifetime; no token refresh |
| API version | Candidate v1 needs no dated query parameter | Confirmation selected deployment supports v1 chat completions |
| JSON/output | Prompt/JSON object/non-strict JSON schema; two selectable output parameters | Verified mode, parameter, sampling support and finish behavior |
| Context/usage | Explicit capability and input/output usage contracts exist | Actual limits, overhead, reasoning-token billing and complete usage semantics |
| Timeout/retry | Defaults connect 5 s/read 120 s/managed total 60 s; jobs three attempts | Approve candidate read/total 60 s, lease 120 s, one attempt |
| Admission | Existing SQLite 17E plus additional run-wide guard | Available RPM/TPM/concurrency and all shared consumers |
| Identity | Owner snapshot for digestion; analyze snapshot for Q&A; publication operator | Verified live principals, scope, issuer configuration and validity |
| Audit | Private distinct local SQLite authorities and immutable objects | Operator-approved location, retention and cleanup owner |
| Price/budget | Proposed maximum EUR 5, not authorized | All actual rates, unit, currency, date/source, tier, region and charges |

The [runbook](../../evaluation/phase_17h_foundry_validation.md) records exact
requirements and redacted configuration names. Public documentation was consulted
only; no Foundry resource was contacted. Microsoft's
[v1 API contract](https://learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle)
supports the candidate endpoint/version description. The current adapter's Bearer
header must not be assumed compatible with an Azure `api-key` requirement. A
chosen incompatible header/dated API contract requires a narrow reviewed provider
change before live work; this preflight did not speculate on an absent deployment.

## Proposed exposure and stage fit

Applicable commercial price: **UNKNOWN**. The
[Azure pricing page](https://azure.microsoft.com/en-us/pricing/details/azure-openai/)
is a source for the operator to select the matching commercial schedule, not an
approved price catalog. Model, region and pricing tier were not supplied. Fixed
or provisioned charges and separately billed services are also UNKNOWN, never
assumed zero. No credit is assumed and no capacity change is proposed.

The [private-fill approval template](../../evaluation/phase_17h_foundry_approval.template.json)
has null unknowns and false approval flags. The proposed maximum marginal spend
is **EUR 5**. The actual confirmed monetary exposure cannot be calculated until
all price inputs and charge bounds are known. Current incurred Foundry spend from
this work is zero because no billable calls were made.

| Stage | Digestion | Questions | Planned attempts | Reserved input | Reserved output |
| --- | ---: | ---: | ---: | ---: | ---: |
| L1, four pages | 3 (one chunk, two reducers) | 1 | 4 | 100,000 | 12,000 |
| L2, 200 pages | 33 (23 chunks, ten reducers) | 12 | 45 | 1,125,000 | 135,000 |
| Combined | 36 | 13 | 49 | 1,225,000 | 147,000 |
| Absolute ceiling including retries | — | — | 50 | 1,250,000 | 150,000 |

For input rate I, output rate O and unit U, combined planned maximum is
`(1225000 * I + 147000 * O) / U + fixed_charge_bound + other_charge_bound`.
For all 50 attempts replace token totals with 1,250,000 and 150,000. F/A are counted
once for the run. No cached-input discount is used. The guard supports confirmed
EUR contracts at or below 5 only; foreign currency is rejected rather than
converted without an approved exchange-rate contract.

**L2 numerically fits attempts/tokens only. Budget and actual quota fit are UNKNOWN;
L2 is not admitted.** One spare attempt remains, with automatic retries disabled.
The proposed TPM permits only one full 28,000-token reservation in a minute.
All actual available quotas must be stricter-or-equal inputs; historical Phase 16
10,000 TPM evidence is not current quota. If that were the available quota, the
full candidate reservation would fail preflight.

The Phase 17H PDF recipe can be reused directly. Its old fake profile cannot:
6,000 output exceeds this task's 3,000 cap. The candidate explicitly uses context
28,000/output 3,000/result characters 3,000 without changing full coverage, evidence,
claim or lineage requirements. The existing profile validator requires the last
bound <= output reservation. Real output may not fit this smaller result envelope.

The 17D planning maximum is 6,776 for L1 and 18,848 for L2. Observed rendered
governance input bounds with fake output are at most 10,052 and 16,474 respectively,
including question calls. Those are **reservations, not usage**. Neither the 17D
estimate nor short fake child results proves worst-case managed prompts fit 25,000.
Generated evidence/lineage/inherited annotations can enlarge future requests.
Before live L2, verify the full managed envelope and all Q&A inputs; if it fails,
provide a revised complete DAG and recalculate costs/calls. Do not silently drop
evidence, questions or qualifications. This unresolved proof is a technical blocker,
not permission to spend part of the budget finding out.

## Local implementation and financial safety

`tests/performance/foundry_budget.py` composes a private SQLite run guard with
the existing `InferenceAdmissionPort`; `GovernedExecution` continues to use the
17G ledger for owner/tenant reservation and settlement. The run guard additionally
retains full maximum reservations across L1/L2/retries and restarts, uses exact
Decimal pricing, includes fixed/extra charges, pins its contract, limits cumulative
attempts/tokens, enforces one outstanding request, and limits rolling RPM/TPM.
Unknown work cannot automatically resume or be refunded. The first provider
failure halts further calls, stricter than the requested repeated-error stop.

Provider admission has mandatory interactive headroom; its concurrency two is
not the project limit. The additional run guard imposes one total outstanding
call across interactive and background work. Local authority files must be shared
by all stages/workers, never copied or reset to regain balance. Unknown usage in
17G stays UNKNOWN; the run guard also retains the outstanding call and stop state.
Reconciliation is a trusted future operator action, not an automatic TTL.

This is tested single-host reference accounting, not distributed authority or an
Azure bill guarantee. Delayed Azure metering, other consumers, token classes and
unbounded fixed costs require independent verification. Operator attestations
must correspond to the real subscription's catalog; a local approval boolean is
not evidence of that correspondence.

`tests/performance/foundry_preflight.py` runs separately selectable offline L1/L2
through the actual document pipeline and provider parser with deterministic fake
HTTP. It records per-provider request/response hashes, role/attempt identity,
duration, usage, ledger ticket, reserved/measured synthetic cost and settlement;
job/digest/publication and question packets hold validation outcomes. The fake
catalog is explicitly labelled test arithmetic, not an Azure price claim.

## Executed synthetic results and interpretation

Final standalone rehearsal artifacts are retained outside the repository at
`/tmp/polymind-17hl-l1-final` and `/tmp/polymind-17hl-l2-final`. These contain PDFs,
fixture manifests, private authority databases, immutable objects, responses,
pending review packets and result JSON. Their `planned_calls` field predates the
final naming correction and means digestion calls (3/33); final tests record total
planned calls (4/45) and separate `planned_digestion_calls`.

Both standalone stages completed with exit 0. L1 used **4 fake calls**, extracted
all four pages, accepted all four evidence pieces, published eight retrieval
records and resolved eight citations. Its one question has a response hash and
pending review. The native page-1 procedure is its predefined fact; the 200-page
ORION fact labels do not exist in the four-page fixture.

L2 used **45 fake calls**, extracted all 200 pages, accepted all 200 evidence
pieces, built a COMPLETE digest, retained two qualifications and one contradiction,
published 400 records and resolved eight retrieval citations. All 12 rubric
questions traversed the bounded authorized Q&A path. Fake Q&A deliberately abstains;
these responses are not semantic successes. Similar/unauthorized-document case
text was sent against the one selected synthetic PDF; actual adversarial selection
case setup remains required before live evaluation and is not claimed tested here.

The existing annotation evaluator measured four authored synthetic digest facts:
structurally valid citations **4/4**, exact-source-supported claims **4/4**, required
findings **4/4**, qualification/contradiction preservation **2/2**, critical unsupported
conclusions **0**. Digest abstention has **0 evaluated cases / null rate**. L1 has
no ORION digest labels and therefore zero denominators/null rates. Reviewer coverage
is **0/1 L1 question responses and 0/12 L2 question responses**; factual claims have
not been independently extracted/judged, so claim-review denominator is unknown.
All human reviewer fields remain null. No human result or expert certification
was fabricated; the 95%/90% targets remain NOT VALIDATED.

Synthetic per-call usage is 30 input/40 output, with arithmetic cost EUR 0.000011
under the fake catalog. These are not actual model usage or billable costs. Fake
embeddings and identity reranking prove retrieval plumbing, not semantic ranking.
The source injection is retained as untrusted data; no actual-model injection
resilience is claimed.

## Tests, review and validation

Targeted tests cover unknown/unapproved/mismatched prices and currencies, fixed
charges, exact cost, quota/token/attempt boundaries, retries, restart, concurrency
across connections, RPM versus TPM, missing/partial/inconsistent/excess usage,
admission denial, provider failure, identity mismatch and explicit stop categories.
Integration tests forbid network connections, execute both stages, prove unknown
usage stops after one call with ledger UNKNOWN, and prove governance denial makes
zero provider calls. Existing evaluator tests were reused.

The initial cost unit group passed **53 tests**. An initial combined collection
failed because unit/integration filenames collided under pytest's import mode;
the new integration file was renamed. The corrected combined group passed **67
tests in 40.16 s**. After adding concurrency/RPM and per-call audit assertions,
the group passed **69 tests in 45.55 s**. These overlapping runs are not additive.
The final post-review command was:

```bash
python -m pytest -q tests/unit/test_foundry_preflight.py tests/integration/test_foundry_offline_workflow.py tests/unit/documents/test_phase17h_evaluation.py --basetemp=/tmp/polymind-17hl-tests-final
```

It exited 0: **69 passed in 40.51 s**, with no failures/skips/warnings reported.
Log: `/tmp/polymind-17hl-tests-final.log`. Final-code L1/L2 artifacts are in
`/tmp/polymind-17hl-tests-final/test_managed_governed_pipeline0` and
`/tmp/polymind-17hl-tests-final/test_managed_governed_pipeline1`. They record total
planned/actual calls **4/4** and **45/45**. The two deliberate denial cases record
FAILED with one call/UNKNOWN usage and FAILED with zero calls, respectively.

During implementation the profile's result/output invariant rejected the first
candidate before inference. The candidate was corrected explicitly, preserving
evidence rules. Early rehearsal wiring used an incorrect authorization argument
and publication-wrapper method; both were corrected to the existing interfaces
and covered by successful integration tests. No production contract was changed.

Self-review inspected the full new code and docs, bounded loops, shared authority,
usage settlement, retry/cancellation behavior, evidence validation, privacy and
absence of provider leakage. It found and fixed a restart window: the guard now
commits known provider failure and its permanent stop state in the **same** SQLite
transaction. Review also corrected the result summary to include question calls
in total planned reservations. Fake-versus-live and pending-versus-reviewed states
are explicit throughout.

`PYTHONPYCACHEPREFIX=/tmp/polymind-17hl-pycache python -m compileall -q .` exited 0
after final source edits. No ownership changes were made. There is no configured
Python linter/formatter gate found in repository build/CI configuration. Docker
build/Compose and Kubernetes checks were not applicable: no runtime, dependency or
deployment files changed. No Docker/Kubernetes operations were performed.

Separate pre-commit review scanned all eight new UTF-8 files for private-key/JWT/
credential-URL patterns, machine-specific home paths, unexpected binary/runtime
artifacts, oversized files, whitespace and broken local Markdown links. No findings
were reported. `git diff --no-index --check /dev/null <file>` additionally checked
each untracked file, since ordinary `git diff --check` excludes them. The tracked
production tree remains unchanged. This bounded heuristic scan is not a general
security certification.

## Security, privacy and remaining operator approval

The offline pipeline uses synthetic verified-principal fixtures only. The test
issuance helper is not a live identity mechanism. Live authority readiness is
BLOCKED by absent OIDC/principal/scope settings; only local composition is tested.
Publication uses the existing authorized wrapper. Governance snapshots revalidate
owner/document scope and Q&A authorization. No user data or real credentials are
included in generated fixtures or tracked artifacts.

The CLI creates a private 0700 output directory with umask 077; security, governance
and run databases use the existing private-path checks and 0600 creation. Store
raw responses and canonical source/evaluation packets locally for reviewer access,
not in Git or public logs. Synthetic deployment/owner identifiers in private audit
files are test values. Existing logs may include model identifiers, so any future
live log remains private. Preserve unknown-cost ledgers until trusted reconciliation.
No deletion/purge certification is implied; retention and scoped cleanup require
an operator owner. No temporary artifact was copied into the checkout.

Exact handoff: privately supply deployment/model/version, Azure region/tier,
endpoint/API/auth contract, context/output/usage capabilities, matched input/output
rates with currency/unit/effective date/source, known fixed/hourly and extra-service
charge bounds, available/shared quotas, verified principals and owner scope,
audit paths/retention and independent reviewer. Verify the complete managed request
envelope and bind a live launcher to those verified objects without test identities,
fake prices, virtual time or budget reset. Then approve the calculated maximum
(proposed <= EUR 5) and L1. L2 needs a separate approval and accepted L1 evidence.

Approval is required by the user's explicit Phase 17H-L gate, not an inferred
repository restriction. A generic approval of EUR 5 alone cannot resolve unknown
prices/authentication or approve L2. No live launcher should be enabled merely by
flipping the template's boolean. Phase 17I remains out of scope and unstarted.

## Final Git and action accounting

All eight new files are untracked and unstaged; existing tracked files are unchanged:

```text
docs/codex/prompts/phase_17h_live_preflight.md
docs/codex/reports/phase_17h_live_preflight.md
docs/evaluation/phase_17h_foundry_approval.template.json
docs/evaluation/phase_17h_foundry_validation.md
tests/integration/test_foundry_offline_workflow.py
tests/performance/foundry_budget.py
tests/performance/foundry_preflight.py
tests/unit/test_foundry_preflight.py
```

Final command results (all exit 0):

```text
$ git status --short --branch
## master...origin/master
?? docs/codex/prompts/phase_17h_live_preflight.md
?? docs/codex/reports/phase_17h_live_preflight.md
?? docs/evaluation/phase_17h_foundry_approval.template.json
?? docs/evaluation/phase_17h_foundry_validation.md
?? tests/integration/test_foundry_offline_workflow.py
?? tests/performance/foundry_budget.py
?? tests/performance/foundry_preflight.py
?? tests/unit/test_foundry_preflight.py

$ git diff --stat
(no output: untracked files are listed separately above)

$ git diff --check
(no output)

$ git diff --cached --name-only
(no output)

$ git log -1 --oneline
af4a7a0 test: add Phase 17H reliability benchmarks and quality evaluation
```

Billable Foundry requests: **0**. Model deployment changes: **0**.
Azure resource mutations: **0**. Git commits/pushes: **0**. Phase 17I work: **0**.

**L0 — PARTIAL.**
**L1 — NOT STARTED, AWAITING APPROVAL.**
**L2 — NOT STARTED, AWAITING APPROVAL.**

## GPT-5.4 mini — 30,000 TPM Deployment Recalibration

2026-10-13. This section supersedes readiness/configuration statements above;
the original L0 evidence (including 69 tests and its eight-file inventory) remains
historical. Starting and final committed HEAD is
`af4a7a076c918ef13aea05d74bf239c0af909133`, on `master`. All eight prior untracked
files were preserved. No 10K recalibration was applied.

**L0 — PARTIAL. L1 technical readiness — BLOCKED for live execution; offline
envelope and workflow checks PASS. L1 and L2 — NOT STARTED, AWAITING APPROVAL.**
There is no demonstrated L1 envelope failure in the four tested stress families.
Endpoint/authentication, live security/admission bindings and an operator-bound
live launcher remain technical prerequisites. This is deliberately not an
unconditional L1 technical PASS based on fake responses.

### Deployment and capability evidence

The operator confirmed resource `epolymind-foundry-dev-susanta`, deployment
`epolymind-gpt-54-mini`, model `gpt-5.4-mini`, version `2026-03-17`, Global Standard,
Global scope, subscription ECI-Development. The October 13 portal observation was
30K / 1M TPM allocation and 0% rate limiting. This is operator-reported screenshot/
portal evidence, not an independently inspected screenshot or API admission test.
The separate `eci-gpt-54-mini` deployment is excluded by the local configuration
allowlist, including mixed role mappings; it was neither accessed nor modified.

Published evidence checked October 13:

- [Microsoft model catalog](https://ai.azure.com/catalog/models/gpt-5.4-mini):
  Chat Completions, version, 400K context and 128K maximum output.
- [Microsoft reasoning guide](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning):
  candidate `reasoning_effort=low`, `max_completion_tokens`, no temperature/top-p;
  completion usage includes reasoning tokens. The 3,000 output reservation covers
  reasoning plus visible output, not 3,000 visible tokens plus reasoning. No
  assumption that mini supports every option of another GPT model is required.
- [Azure v1 lifecycle](https://learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle):
  base path `/openai/v1`, Chat Completions deployment alias, no dated API-version
  query. The current adapter sends Bearer authentication and does not acquire or
  refresh tokens. Endpoint host, credential mechanism/audience/lifetime and Azure
  permissions remain unverified; an API-key-header configuration is not implemented.
- [Structured outputs](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs):
  use JSON-object output with existing application schema/evidence validation.
  Existing non-strict JSON-schema mode is not a strict-schema guarantee. Candidate
  response aliases are model name and dated model name; actual returned alias and
  complete usage/finish behavior await authorized L1. `length` stops execution;
  unsupported finish reasons and malformed output fail closed.

One narrow provider correction adds explicit optional reasoning effort to the
neutral capability and OpenAI-compatible bounded request. Unset serialization and
profile fingerprints remain unchanged. Ollama rejects an explicitly unsupported
setting before I/O. No domain Azure conditions, second provider stack, SDK or new
dependency were introduced. Existing timeout defaults remain connect 5 s/read
120 s/total 60 s; live configuration must bind read and total to 60 s, lease 120 s,
and one job attempt. A total deadline cannot interrupt a blocking read sooner
than its read timeout. Unknown usage after timeout stays outstanding; no refund.

### Admission and complete rendered envelopes

Azure TPM is 30,000. Actual Azure RPM is unknown (historically 10); neither the
subscription pool nor TPM proves current RPM. Candidate shared application policy
is 2 RPM, 30K TPM, two slots with one reserved interactive slot and one background
slot, 1 interactive RPM and **2,000 interactive TPM**. The run guard still allows
only **one validation request at a time**. Background throughput is at most 1 RPM.
The 2,000 reserve is a proposal, increasing the prior fake policy's one token; it
never replaces a larger operational reserve. Other deployment consumers must be
identified and use the same admission authority. A separate external consumer
cannot be bounded by this local ledger.

The run ceiling remains 25,000 reserved input + 3,000 reserved output = 28,000.
With 2,000 protected TPM this just fits 30K; headroom of 2,001 rejects it. At
10K protected headroom, input must be at most 17K with 3K output. No evidence was
truncated to satisfy these limits. Rolling reservations remain charged for the
minute even after small actual usage; active slots do not expire with the minute.
[Azure quota documentation](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/quota)
explains its approximate character/output-based admission estimate and short RPM
windows. These differ from both our conservative byte estimate and billed tokens;
local acceptance does not guarantee Azure acceptance or delayed billing.

Retained stress artifact: `/tmp/polymind-17hl-30k-envelopes-3/results.json`.
Each case uses exact native fixture extraction, canonical source verification,
actual managed schemas/system/user rendering, inherited results and application
validation. Children approach or reach the complete 3,000-byte canonical bound.
Q&A uses the real renderer, full inherited annotations and eight longest canonical
excerpts through a replica seam; it does not claim actual semantic retrieval.
The families test prose, JSON escaping, multiple claims/lineage, and opposing
findings/qualifications. These are conservative adversarial examples, not a proof
of every schema-compliant string or independent semantic judgments.

| Fixture / family | Largest digestion input | Largest Q&A input | Outcome |
| --- | ---: | ---: | --- |
| L1 prose | 11,843 | 16,499 | Fits |
| L1 escaped | 13,915 | 22,727 | Fits |
| L1 multiple claims | 12,839 | 9,200 | Fits |
| L1 contradictions | 13,723 | 23,039 | Fits |
| L2 prose | 24,629 | 82,387 | Q&A blocked |
| L2 escaped | 32,141 | 144,891 | Reductions and Q&A blocked |
| L2 multiple claims | 28,578 before stop | Not reached | Full lineage blocked |
| L2 contradictions | 31,533 | 154,403 | Reductions and Q&A blocked |

Every request adds 3,000 output tokens. Each background row adds 2,000 protected
TPM to its combined reservation. L1's largest tested background envelope therefore
needs 18,915 deployment TPM; its largest interactive Q&A needs 26,039. These are
necessary bounds for the tested cases, not a smaller universally safe quota.
The chosen full reservation profile needs **30,000 TPM** including headroom.
L2 escaped reduction alone needs 37,141 with headroom, beyond scope. Diagnostic
`complete=true` means offline structural construction completed even after a
recorded render failure; it never authorizes a failed request.

Three independent L2 blockers are confirmed:

1. Escaped child serialization reaches 32,141 input tokens, exceeding 25K.
2. Thirty-two required child claim links need at least 3,754 canonical result
   bytes even with one-character prose, exceeding the 3,000-byte result bound.
3. All 12 questions overflow with rich globally inherited annotations, even in
   the prose family (82,363–82,387 input). Contradiction-heavy Q&A reaches 154,403.

Smallest future experiments: lower reducer fan-in to two and recalculate the
entire DAG/attempt budget; separately introduce bounded, evidence-complete Q&A
annotation retrieval or paging with explicit contradiction/qualification retention
and rubric coverage tests. These changes need new design review and may require
more calls than the 50-attempt contract. Increasing quota alone cannot fix the
lineage result bound. Do not remove links, globally truncate annotations, relax
quality, change the estimator merely to admit requests, or approve the current
45-call L2 plan. No such redesign was implemented.

### Monetary bounds and scheduling

The [Microsoft March 17 launch pricing table](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/introducing-openai%E2%80%99s-gpt-5-4-mini-and-gpt-5-4-nano-for-low-latency-ai/4500569)
lists Standard Global USD 0.75 input / 4.50 output per million tokens (cached input
0.075 is not used). Publication date is not a confirmed contract effective date.
The dynamic Azure pricing page could not be retrieved during this inspection;
region, commercial agreement and actual EUR schedule remain unverified. These
figures are reference arithmetic, not Azure billing approval.

| Plan | Attempts | Reserved input | Reserved output | Indicative USD |
| --- | ---: | ---: | ---: | ---: |
| L1: 3 digestion + 1 Q&A | 4 | 100,000 | 12,000 | 0.12900 |
| Original L2: 33 digestion + 12 Q&A (blocked) | 45 | 1,125,000 | 135,000 | 1.45125 |
| Combined original plans | 49 | 1,225,000 | 147,000 | 1.58025 |
| One remaining separately approved attempt | 1 | 25,000 | 3,000 | 0.03225 |
| Entire 50-attempt ceiling | 50 | 1,250,000 | 150,000 | 1.61250 |

Formula: `(reserved_input * approved_input_rate + reserved_output *
approved_output_rate) / approved_price_unit + approved_additional_charges`.
EUR values remain **unknown**. EUR 5 remains an unapproved proposal. No cache or
credit is assumed. Pay-per-token Global Standard is operator-confirmed, but absence
of fixed/provisioned and separately billed services must still be confirmed; unknown
extras cannot be entered as zero. Automatic retries are zero. Any authorized retry
uses the same durable 50-attempt, token and financial ledger and the same stage
gates. No new budget database may clear existing outstanding reservations.

Conservative scheduling uses at least 61 seconds between validation starts, plus
waiting for the previous request to finish and all shared quotas. At that spacing,
L1 needs at least 183 seconds to its fourth start; original L2 needs 2,684 seconds
(~44.7 minutes) to its 45th start. Add request latency/admission waits; these are
not duration guarantees. There are no extra evaluation-model calls.

### Verification and approval handoff

Initial focused run: **79 passed in 12.67 s**. Final targeted union, including the
new contradiction-heavy L1 assertion: **198 passed in 65.68 s**. Command:

```bash
python -m pytest -q tests/unit/test_foundry_preflight.py tests/unit/test_foundry_30k.py tests/unit/test_structured_provider.py tests/integration/test_foundry_offline_workflow.py tests/unit/documents/test_phase17h_evaluation.py tests/unit/documents/test_managed_inference.py tests/integration/test_managed_digestion.py tests/integration/test_governed_digestion.py
```

Log: `/tmp/polymind-17hl-30k-final-tests.log`. This scopes regression to financial
and quota guards, changed provider capabilities, managed/governed execution and
fake L1/L2. Both fake workflows pass end to end with network connections forbidden:
4/45 calls, COMPLETE digests, canonical publication, citations and pending human
packets. Unknown usage stops before a second call; governance denial makes zero
calls. Short fake L2 success does not override the rich-envelope blockers. The
original 69-test evidence is preserved; the 732-test suite was not rerun.

Presence-only recheck found all 17 previously listed configuration names absent
in both process environment and root `.env`; no credential values were printed.
Before L1, the operator must supply/confirm privately:

- Endpoint, Azure region, supported authentication, audience/lifetime and both
  logical role mappings to the PolyMind deployment; actual response aliases.
- Actual RPM, protected interactive reserve, all shared consumers and authority
  policy, plus live principal/tenant/owner and publication/analyze permissions.
- Exact EUR input/output rates or approved conversion, unit, source/effective date,
  commercial tier, fixed/infrastructure charges and final monetary ceiling.
- Existing private durable ledger/object locations, restart/reconciliation policy,
  retention owner and human reviewer; no fresh ledger to evade prior obligations.
- A reviewed operator-bound live execution composition with the same guard, one
  attempt per job, no fallback/retry and all stop conditions, then explicit L1
  authorization. The delivered CLI remains offline-only; template approval alone
  cannot launch inference. L2 needs corrections, successful L1 and separate approval.

Review artifacts contain only synthetic sources/responses. Store future responses,
identity metadata and ledgers privately outside the repository with restricted
permissions; never embed credentials/endpoints in tracked reports. Human review is
pending, reviewer coverage zero; no expert semantic-quality certification is made.

Final inventory relative to HEAD: modified `llm/structured.py`,
`llm/openai_compatible.py`, `llm/ollama_client.py`,
`tests/unit/test_structured_provider.py`; eleven untracked files listed below.
The first eight preflight files are preserved, with report/runbook/template and
fake harness updated; three new files add recalibration and envelope tests.

```text
docs/codex/prompts/phase_17h_live_preflight.md
docs/codex/reports/phase_17h_live_preflight.md
docs/evaluation/phase_17h_foundry_approval.template.json
docs/evaluation/phase_17h_foundry_validation.md
tests/integration/test_foundry_offline_workflow.py
tests/performance/foundry_budget.py
tests/performance/foundry_preflight.py
tests/unit/test_foundry_preflight.py
tests/performance/foundry_envelopes.py
tests/performance/foundry_recalibration.py
tests/unit/test_foundry_30k.py
```

Azure Foundry calls, paid inference, quota/deployment/resource changes, ECI project
changes, Git commits/pushes and Phase 17I implementation: **all zero**.

Self-review confirmed unchanged unset capability fingerprints, explicit adapter
behavior, no provider-specific document-domain code, and retained fail-closed
financial accounting. Scoped `compileall` passed using an external bytecode cache.
Pre-commit inspection of all 15 changed/untracked files found no introduced private
keys, credential strings, trailing whitespace, generated databases or dependency
changes. Synthetic URL/credential rejection cases are test data. The approval JSON
parses successfully. No Docker/infrastructure validation was necessary.

Final Git checks: `master...origin/master`, four tracked modifications and eleven
untracked files, all unstaged. `git diff --stat`: 4 files, 51 insertions, 1 deletion
(untracked files excluded by Git). `git diff --check` and
`git diff --cached --name-only` returned no output. Last commit remains
`af4a7a0 test: add Phase 17H reliability benchmarks and quality evaluation`.

## L1 Azure integration readiness — 2026-10-13

This section supersedes the earlier absent-live-launcher finding. **L0 PARTIAL;
L1 offline integration PASS; L1 live execution NOT STARTED; L2 BLOCKED, unchanged.**
Committed baseline remains `af4a7a076c918ef13aea05d74bf239c0af909133` on `master`.
The preceding eleven untracked files and four tracked modifications were preserved.

### Implementation and technical readiness

`tests/performance/foundry_l1.py` now binds the existing four-page workflow to the
real OpenAI-compatible adapter, existing Phase 17E admission and Phase 17G ledger.
It defaults to a network-forbidden dry run. The workflow's optional runtime uses
an authenticated real principal, approved price catalog and existing authority
paths. Fake principals/prices and constant vectors remain exclusively in rehearsal
and intercepted test construction. Live publication instead loads approved local
embedding artifacts and an isolated local Chroma collection through existing
adapters. This does not use a separately billed evaluation/embedding model, or
modify shared Chroma, Redis or AKS. Local costs and artifact availability still
require operator confirmation. No L2 redesign was introduced.

Live approval requires both an explicit CLI configuration-hash acknowledgement and
an RS256 access-token claim `polymind_l1_approval` carrying the same hash. Existing
OIDC signature/issuer/audience/purpose validation runs before the claim is read;
principal scope must match configuration and the existing security authority must
already authorize publication management. The launcher does not register a
synthetic principal, disable authorization or mint approval. An issuer unable to
attest the claim is a blocker, not a reason to bypass verification. The trusted
private configuration must use the actual deployed identity anchors and policies.

Configuration includes exact endpoint/authentication, credential validity,
operator-approved EUR catalog and charges, quota/headroom/consumer attestation,
existing ledger paths and local embedding tree hash. Changing it invalidates the
signed approval. The private audit path is outside Git; an exclusive durable marker
consumes approval once. Existing attempts or marker refuse restart, including after
an uncertain/failed start; reconciliation never clears financial debt automatically.
No current operator token, Azure credential or live configuration was supplied.
Presence-only inspection of the two new token/credential variable names and five
representative provider/OIDC/governance names found all absent; no values were read
or printed. Actual authentication, issuer approval support and runtime availability
therefore remain **BLOCKED**, despite offline integration PASS.

Narrow production changes in this task: `OpenAICompatibleProvider` accepts an
explicit `authentication_header` (`Authorization` by default, or `api-key`), and
bounded HTTP disables/rejects redirects. Existing callers retain Bearer behavior.
No second provider stack or dependency was added. The launcher's session disables
environment proxy/credential behavior and closes on success/failure. The earlier
reasoning-effort corrections remain intact. The [Microsoft v1 reference](https://learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle),
rechecked October 13, confirms the two REST authentication headers and v1 endpoint
contract. No Azure endpoint was contacted to test them.

Both logical roles map only to the PolyMind deployment. JSON-object validation,
`reasoning_effort=low`, `max_completion_tokens=3000`, no sampling parameters,
configured response aliases, 5-second connect/60-second read and request deadline,
and inclusive completion/reasoning accounting use existing bounded contracts.
Model output sufficiency, actual served alias, Azure usage and credential acceptance
remain live observations. API-key/Bearer selection is explicit, never guessed.

The new composition preserves canonical source validation, durable admission,
managed synthesis, evidence checks, authorized publication and one authorized
question. Private per-call records include response hash/text, token usage,
duration and normalized outcome. Financial records remain durable on timeout or
missing usage. Existing ledger records are excluded from this run's per-call
correlation but remain visible to shared budget enforcement. Reviewer claims,
judgment and semantic metrics remain pending; no fabricated human labels are used.

### Financial and operational gate

The L1 contract restricts four total attempts, 100,000 reserved input, 12,000 output,
one request in flight and one start per rolling minute, with no automatic retries.
Full four-call reservations plus known fixed/additional costs must fit an approved
EUR ceiling no greater than EUR 5. Every call still passes shared owner/tenant and
provider admission. Shared policies must preserve at least 2K interactive TPM;
larger headroom and smaller actual quotas win. The candidate per-request maximum
is 25K + 3K, while the retained largest tested L1 envelope is 23,039 + 3,000.
The scheduler waits at least 61 seconds between starts, checks cancellation and
expiry, and stops rather than retrying admission denial. Unknown usage is retained.

**Current authorized spend is EUR 0.** USD 0.129 remains indicative four-call token
arithmetic only. Exact EUR rates or approved conversion, catalog source/effective
date, region, actual Azure RPM, all consumers, fixed/infrastructure charges and
remaining budget must be verified before approval. A 30K portal allocation is not
proof of per-request admission. Application reservations cannot guarantee delayed
Azure billing.

### Offline evidence and regression

The earlier 198-test result and all benchmark/envelope evidence remain historical
and were reused. No large-document benchmark was repeated. New tests use genuine
RS256 verification with in-memory test keys, existing SQLite authorities and the
real HTTP adapter with intercepted transport; sockets are forbidden. They cover
both headers, role/alias/payload compatibility, canonical publication/citations,
four unique identities, durable restart refusal, missing/altered signed approval,
wrong deployment/ECI/model, unknown pricing/charges, headroom/quota rejection,
unknown usage and timeout. Default dry-run is also exercised with live construction
replaced by a failing sentinel.

- Initial affected provider/fake workflow check: **58 passed in 39.76 s**.
- New launcher/provider check: **76 passed in 4.97 s**.
- Final focused financial/envelope/provider/launcher union: **159 passed in 26.70 s**.
- Complete regression, run **once** after production adapter changes finalized:
  `python -m pytest -q` — **842 passed in 166.28 s**.
  Log: `/tmp/phase17hl-l1-full-regression.log`.
- Final affected fake-workflow check after audit correlation changes:
  **4 passed in 41.77 s**. Log: `/tmp/phase17hl-l1-final-workflow.log`.

After full regression, a launcher cleanup self-review hardened transport/vector
closure even when final audit writing fails. This evaluation-launcher correction
and additional approval/timeout tests were checked separately; the full suite was
not repeated. The final launcher-only result is recorded below. Scoped compilation
passed with bytecode outside the repository. No infrastructure build or new
dependency was needed.

### Operator handoff and complete inventory

The updated runbook documents configuration fields, digest computation, signed
approval, private paths, separate credential inputs, local artifact hashing,
cancellation and consumed-approval behavior. The template adds an intentionally
invalid `launcher_configuration_template`; null commercial/authentication fields
and false confirmations must not be treated as approval. Obtain an actual trusted
issuer attestation only after the operator has reviewed the exact plan, prices,
identity/owner scope, authority locations, quotas, audit retention and local model
artifacts. L2 remains separately blocked by its three established envelope/lineage
failures, requiring a later design change and separate approval.

All modified tracked files relative to HEAD:

```text
llm/bounded_http.py
llm/ollama_client.py
llm/openai_compatible.py
llm/structured.py
tests/unit/test_structured_provider.py
```

All untracked files (the original eleven plus two new launcher/test files):

```text
docs/codex/prompts/phase_17h_live_preflight.md
docs/codex/reports/phase_17h_live_preflight.md
docs/evaluation/phase_17h_foundry_approval.template.json
docs/evaluation/phase_17h_foundry_validation.md
tests/integration/test_foundry_l1_launcher.py
tests/integration/test_foundry_offline_workflow.py
tests/performance/foundry_budget.py
tests/performance/foundry_envelopes.py
tests/performance/foundry_l1.py
tests/performance/foundry_preflight.py
tests/performance/foundry_recalibration.py
tests/unit/test_foundry_30k.py
tests/unit/test_foundry_preflight.py
```

No billable Foundry requests, live Azure inference, Azure resource/quota/deployment
mutations, ECI changes, Git commits/pushes, or Phase 17I work occurred. Stop here for
operator review and explicit L1 approval; do not execute the live command.

Final launcher-only verification: **24 passed in 5.84 s**, including audit-write
failure resource cleanup (`/tmp/phase17hl-l1-launcher-final.log`). All final launcher
changes are covered by this targeted rerun; the one full regression predates that
small evaluation-launcher cleanup correction.

Final pre-commit inspection covered all 18 changed/untracked files: no introduced
private-key/credential markers, trailing whitespace, runtime databases/PDF/log
artifacts or dependencies. Private audit data remains outside Git. Approval JSON
parses and final scoped compilation passes. `git diff --check` is clean; index is
empty. Git reports five tracked modifications (66 insertions, two deletions) and
13 untracked files. All are unstaged/uncommitted; HEAD and branch are unchanged.

## Local configuration and offline readiness — 2026-10-14

This assessment supersedes earlier statements that the local authorities, trust,
EUR catalog and embedding artifacts were absent or uninspected. **Offline checks
pass; live L1 remains BLOCKED and authorized spend remains EUR 0.** No inference
request, Azure operation, model download, dependency installation, key generation,
live signing, approval consumption or authority/replay mutation occurred. The existing
application changes were inspected and preserved; no implementation was changed.

| Gate | Status | Evidence / remaining condition |
| --- | --- | --- |
| Private unapproved draft | PASS | Existing draft reviewed; three verified fields added; original retained in dated private backup; 0600 file under 0700 directory. |
| Endpoint/deployment boundary | PASS locally | Draft matches private `.env` and passes the existing deployment validator; endpoint availability was not probed. |
| Entra configuration and prior authorization | PASS locally | Strict Entra v2 schema; trust issuer/tenant and registered user agree; security audit records prior allowed authentication and `PUBLICATION_MANAGE`. Current token validity/claims were not reverified. |
| Existing authority integrity | PASS | All three SQLite files pass `integrity_check`, schema version 1; configured governance policy/catalog and provider policy match stored serialized values. No reservations or provider calls exist. |
| Trust/replay storage | PASS locally | Private operator-owned files/directories, distinct authorities outside Git, no symlink components or untrusted-writable parents. Live-purpose RSA trust matches operator public-key file; replay directory empty and preserved. |
| Independent key attestation | BLOCKED | Public-key equality does not establish independent operator confirmation of the fingerprint. |
| Shared local quota | PASS | 30,000 TPM, 2,000 protected interactive TPM, shared 2 RPM, one interactive RPM, one background RPM, one background slot. Actual Azure RPM and all consumers remain unconfirmed. |
| EUR catalog / spending authorization | BLOCKED for execution | Existing catalog is marked approved and matches the authority; proposed EUR 5 is not execution authorization. Charge bounds and pricing-source evidence remain unset. |
| Embedding/runtime setup | PASS locally | Pinned cached embedding integrity verified, materialized without symlinks, launcher retrieval setup and Chroma persistence exercised offline. No semantic quality or live execution claim. |
| Complete launch configuration / signature | BLOCKED | Nine fields unset, four verification flags false, contract approval false; no execution signature created. |
| Private run audit / retention | BLOCKED | Run directory, retention/cleanup owner and operator approval remain unspecified. |

### Private draft and security findings

The requested `<PRIVATE_OPERATOR_DIRECTORY>/l1-configuration-draft.json`
already existed. After review, only `owner_scope`, `embedding_directory` and
`embedding_tree_sha256` changed. The owner scope was derived from the exact trust
identity and matched against the existing enabled user registration and prior
allowed publication authorization; no token was decoded to manufacture identity.
The original bytes remain in
`l1-configuration-draft.before-offline-readiness-20261014.json` beside the draft.
The execution system approved the scoped write outside the workspace. Unknown
fields remain null and all execution gates remain false. The catalog's existing
`operator_approved=true` was preserved as historical pricing approval, distinct
from `contract.approved=false` and execution authorization.

The private draft has exactly the `LaunchConfiguration` fields. Populated values
match the existing private environment, policies and authority records. The nine
remaining unset fields are `authentication`, `credential_valid_until`,
`approval_expires`, `audit_directory`, `actual_azure_rpm`, `contract.price_source`,
`contract.maximum`, `contract.fixed_cost` and `contract.extra_cost`.
`credential_audience_verified`, `quota_verified`, `shared_consumers_verified` and
`charges_verified` remain false, as does `contract.approved`. The draft cannot be
loaded as an approved configuration. Direct loading currently raises `TypeError`
from `Decimal(None)` in the existing money validator. A diagnostic-only in-memory
copy with null entries omitted gives the expected missing-field/literal-gate
validation errors; no populated-value schema error was found. This error-reporting
limitation is retained explicitly, not misreported as a valid launch configuration.
No approved configuration digest was issued.

The three authorities were opened only with SQLite `mode=ro&immutable=1`, after
checking for absent WAL/journal sidecars; application authority constructors and
authorization methods were not invoked on them. Before/after hashes and metadata
confirm `.env`, authorities, trust and public-key files were unchanged. The private
signing key was not opened. The RSA key is 3072 bits. Its SHA-256 fingerprint over
DER SubjectPublicKeyInfo is
`35785596dd2f38a3ae5fc8eeb93015a1ba3c8b4f16f06a1d73fbe521f9657816`.
An operator must independently confirm its provenance and binding. Local ownership
and persistence checks do not attest backups, retention or multi-host replay safety.

The configured EUR catalog is effective 2026-10-01. Four maximum reservations
(100,000 input plus 12,000 output tokens) calculate to EUR **0.11351636747626**,
excluding unknown fixed/additional charges. This is arithmetic on the existing
operator-marked catalog, not a newly verified commercial quote or spending grant.
The authority's owner/tenant policy allows four requests and 112,000 tokens; the
four-call L1 reservation uses that full allowance, so sharing it with interactive
work requires operator review as well as provider headroom confirmation.

### Local artifacts and validation

Four-page L1 uses `sentence-transformers/all-MiniLM-L6-v2`, revision
`1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, dimension 384. This launcher uses a
deterministic reranker callback, so it does not require loading the separate
cross-encoder. No local generative model is required; eventual generation uses the
external provider boundary. The cached pinned cross-encoder revision also exists,
but was not needed or qualified for this L1 path.

All 11 embedding snapshot files exist and match their content-addressed cache
blobs (Git blob SHA-1 for small files; SHA-256 for the safetensors weights). This
checks local integrity, not independent upstream provenance. The cached snapshot
uses symlinks, rejected by the launcher. A verified copy with regular files was
prepared under the private draft directory, without modifying the cache. Its
launcher-compatible sorted-path/content tree SHA-256 is
`96ab3cd391276cb159904c4d329318ae1f3330278a7fc0450256233cf8bb78db`.
The exact `local_retrieval` function accepted the copied directory/hash, loaded
CPU embeddings with `local_files_only=True`, checked retrieval-profile/tokenizer
compatibility, and created/closed an isolated temporary Chroma store. No embedding
encode or provider inference was performed. Separate Chroma persistence testing
used an explicit synthetic vector, without a model-backed embedding function.
Installed runtime versions include sentence-transformers 5.5.1, transformers 5.9.0,
torch 2.12.0 and chromadb 1.5.9. No required local runtime dependency was missing.

Tests ran against an exact copy of Git-visible source, including existing untracked
implementation files, in a private temporary directory excluding `.env`. A Python
startup audit hook denied socket connect, DNS and sendto operations, inherited by
Python child processes, with Hugging Face/Transformers offline flags. This avoided
loading live credentials or authority locations. One initial collection attempt
selected the system Python after changing directories and stopped with 14 import
errors before executing tests. Using the explicit existing project interpreter
resolved that harness issue; no dependencies were installed.

- Complete regression: **1,018 passed in 201.68 seconds**, one completed suite run.
- Full repository compilation: PASS, `PYTHONPYCACHEPREFIX` directed to a temporary
  external cache; no ownership changes.
- `git diff --check`: PASS.

Private verification artifacts and logs remain under
`/tmp/polymind-17hl-readiness-xpfu_vvp/`; this temporary evidence directory is not an
approved live audit location. Targeted results and final review follow below.

### Remaining operator handoff

Confirm actual Azure RPM/concurrency and every shared consumer, including whether
all use the same local admission authority. Confirm API-key validity, selected
API-key versus bearer authentication, credential audience/lifetime and live API
compatibility; presence of a key or token file is insufficient. Supply pricing
source evidence, fixed/provisioned and additional-service charge upper bounds,
and explicit spending ceiling approval. Choose a private run audit directory,
retention/cleanup owner and independent reviewer; confirm model provenance and
independent RSA fingerprint binding. At eventual launch, freshly verify the
operator token and exact owner scope, set reviewed expirations and prerequisites,
and obtain a separately signed approval for the exact validated configuration.
No signature or financial authorization is part of this task. Human review and
live evidence remain outstanding; L2 and Phase 17I are unchanged.

### Final targeted checks and pre-commit review

Targeted offline L1 integration, workflow, approval, Entra/OIDC, authority/readiness,
preflight and 30K checks: **341 passed in 114.04 seconds**. This includes missing,
invalid, expired, mismatched and test-purpose approval rejection with intercepted
HTTP; synthetic fixture signing is isolated from the real trust/key/replay state.
Additional direct checks confirmed that an absent embedding directory and a wrong
tree hash fail closed without creating the retrieval audit directory.

Final self-review confirmed that only the three reviewed private draft fields were
changed, the original backup matches its initial hash, execution flags remain
false, and all protected existing configuration/authority/trust records are
unchanged. The private replay directory remains empty. No implementation/API,
provider boundary, dependency or governance schema changed. Separate pre-commit
review checked task documentation for real credential leakage, generated artifacts,
local links, whitespace and unintended scope changes. Private files remain outside
Git; temporary test evidence was not added to the checkout. Docker builds and
cloud checks were unnecessary because no image/deployment code changed.

Final Git state is `master...origin/master`, eight modified tracked files and
25 untracked files, with no staged changes. This task adds the preserved offline
readiness prompt and updates this already-untracked readiness report; all prior
work remains. `git diff --stat` reports eight tracked files, 130 insertions and six
deletions; it excludes untracked documentation and implementation. No staging,
commit or push occurred. Stop here for operator review; live L1 remains BLOCKED.

## Final technical readiness and L1 handoff — 2026-10-14

**TECHNICAL READY for the documented controlled four-page L1 experiment.**
**LIVE AUTHORIZATION PENDING.** This means the offline-verifiable implementation
and local runtime prerequisites pass; the private draft deliberately remains
unlaunchable until independent operator attestations and approval are complete.
It does not certify endpoint availability, Azure access rights, actual RPM,
commercial charges, model output quality or successful live execution.

The previous 1,018-test full regression and 341-test targeted baseline remain
historical evidence. The assessment did not repeat cloud, Entra or financial
investigations. It preserved all initial uncommitted work and the existing
security/governance/provider authorities, approval trust and replay storage.
L2 remains blocked by context/lineage limits; Phase 17I was not started.

### A. Technical readiness matrix

| Area | Offline technical status | Evidence and execution boundary |
| --- | --- | --- |
| Provider configuration | READY | Actual `.env` base is `https://epolymind-foundry-dev-susanta.openai.azure.com/openai/v1`; draft corrected from the different `services.ai.azure.com` host. Neither endpoint was probed. Both launcher roles (`general`, `summarization`) map exclusively to `epolymind-gpt-54-mini`; all four generic environment roles also map there. |
| Payload and authentication | READY | Draft selects API key; launcher explicitly sends `api-key`, disables environment proxy/auth inheritance and redirects, and supplies low reasoning effort, `max_completion_tokens=3000`, non-streaming JSON object and no sampling overrides. Response aliases accept deployment, model and configured dated model ID. Payload/header tests intercept HTTP. Key presence is not proof of access. |
| Document pipeline | READY | Four-page native PDF extraction, canonical hash/exact text and evidence resolution, one chunk plus structural/root synthesis, full coverage/lineage checks and schema validation pass offline. Q&A now actually transmits its schema. No evidence trimming, repair calls or requirement relaxation. |
| Embeddings and RAG | READY | Existing pinned MiniLM tree passes launcher hash checks, loads CPU/local-only, encodes a 384-dimensional vector, writes/reads isolated temporary Chroma and rejects unrelated document selection. Wrong tree hash fails before vector storage creation. Authorized publication/retrieval/citation tests pass. |
| Identity and authorization | READY locally | Previously verified Entra identity/authorization and registered authorities retained. Live construction uses OIDC verification and the existing security authority, never fixture principal issuance. Fresh token validity is checked at execution; no fresh external identity/access claim is made here. |
| Quota and financial safeguards | READY locally | Four attempts, 100,000 input and 12,000 output run reservations; 25,000/3,000 per-call bounds; one outstanding request, 61-second start spacing, 30,000 TPM ceiling and at least 2,000 protected interactive TPM. Existing immutable policies/catalog remain unchanged. Azure RPM/shared-consumer attestation and commercial charge bounds remain external. |
| Audit and evaluation | READY | Provider request/response hashes, sanitized error categories, usage including reasoning within completion totals, latency, run/governance settlement, canonical artifacts, publication and response/citation review packets remain available. Independent human judgments are pending, never synthesized as passing. |
| Launcher and signed approval | READY | Existing authority files required; no replacements initialized in this assessment. Configuration digest, exact operator/target/budget/limit bindings, independent RSA trust, expiry and durable replay checks remain enforced. Missing, expired, mismatched or test-purpose approvals refuse execution. No live approval was issued or consumed. |

The launcher constructs capability/stage settings explicitly through
`candidate_capability()` and `ManagedSettings`; generic
`DOCUMENT_INFERENCE_CAPABILITY`, `DOCUMENT_INFERENCE_PROFILES` and
`DOCUMENT_DIGESTION_PROFILE` are absent in `.env` but are not required for this
execution path. Likewise, API-key header selection comes from the launch draft,
not a generic factory environment switch. Therefore no generic application
configuration or provider factory was changed. The local path does not use AKS,
Redis, shared Chroma or a cloud embedding service. The previously verified paused
AKS baseline was accepted without reinspection or resource changes.

Transport connect/read timeouts are 5/60 seconds; managed and Q&A requests use a
60-second total budget, with bounded response reads. The total budget is checked
around reads, not an asynchronous hard cancellation deadline; a socket read can
last until its inactivity timeout. Job lease is 120 seconds and maximum attempts
is one. No readiness/model-discovery call, fallback or automatic HTTP repair/retry
occurs. Unknown usage and provider/network/timeout/quota failures retain obligations
and stop continuation; known low usage does not refund full run reservations.

The documented source is a deterministic, generated **real PDF file**, including
adversarial page-three text. It is evaluation input, not a synthetic model result.
Live construction uses real verified identity, approved prices, the Azure adapter,
local pinned embeddings and Chroma. Offline HTTP/model/vector/identity fakes are
confined to rehearsal/test branches. The reranker is the documented deterministic
pass-through callback; semantic ranking and answer support still require review.
No separate real-world PDF was supplied; readiness does not extend to arbitrary
PDFs or certify semantic quality. The operator handoff retains the documented
fixture rather than silently introducing a different source or request plan.

### B. Changes and verification

The task changed these repository files, preserving their earlier work:

| File | Reason |
| --- | --- |
| `documents/publication/analysis.py` | Include the exact Q&A JSON schema in trusted system instructions for prompt/JSON-object adapters, and include its size in the existing conservative bound. API output and provider-neutral interfaces remain unchanged. |
| `tests/unit/publication/test_analysis.py` | Assert the model-facing prompt includes the required output contract. |
| `tests/integration/test_foundry_l1_launcher.py` | Assert the fourth intercepted Azure-format request really carries that schema. |
| `tests/performance/foundry_budget.py` | Normalize null/malformed monetary draft fields to Pydantic validation errors rather than leaking a raw Decimal `TypeError`/`InvalidOperation`. Valid financial serialization and policy remain unchanged. |
| `tests/unit/test_foundry_preflight.py` | Add 12 field-specific invalid-money cases. |
| `tests/performance/foundry_envelopes.py` | Update conservative Q&A envelope accounting to include the newly transmitted schema. |
| `tests/unit/test_foundry_30k.py` | Update measured contradiction-heavy L1 question size from 23,039 to 23,548; retain all fit/coverage checks and limits. |
| `docs/evaluation/phase_17h_foundry_validation.md` | Explain final configuration, schema accounting and fixture scope; point to current handoff. |
| `docs/evaluation/phase_17hl_operator_approval.md` | Reuse established local readiness instead of asking to reprovision trust/authorities; retain independent external attestations. |
| `docs/codex/prompts/phase_17hl_final_handoff.md` | Preserve the task brief and restrictions. |
| `docs/codex/reports/phase_17h_live_preflight.md` | Consolidate current readiness, tests and operator handoff here. |

Outside Git, exactly three fields changed in the existing private
`<PRIVATE_OPERATOR_DIRECTORY>/l1-configuration-draft.json`: endpoint now
matches `.env`, `authentication=api_key`, and `contract.maximum="5"` records the
accepted planning ceiling. The execution system approved this scoped private
write. An exact 0600 backup named
`l1-configuration-draft.before-final-handoff-20261014.json` remains beside it.
No signing key was opened. No approval flags or attestations were manufactured.
The draft still fails schema validation, now through ordinary validation errors.

Regression ran against a copy of Git-visible source without `.env`, using the
existing project interpreter, an inherited startup audit hook denying socket
connect/DNS/sendto, and Hugging Face/Transformers offline flags. No dependencies
were installed. This scope exercises both changed behavior and its managed,
publication, governance and signed-launch consumers without rerunning the entire
1,018-test suite.

- Initial focused run: **362 passed, 5 setup errors in 122.58 s**. All five errors
  shared the stale envelope-size checker after the prompt change.
- First envelope rerun: **25 passed, 1 failed in 12.71 s**. All fit checks passed;
  only the old exact 23,039 snapshot remained. Updated it to the observed 23,548,
  with no threshold relaxation.
- Final envelope rerun: **26 passed in 13.13 s**. Together with the unaffected
  passing cases and separate evidence group, **455 distinct selected tests pass**
  across these recorded runs; this is not a claim of one clean 455-test invocation.
- Separate extraction, digestion/evidence and model-artifact group: **88 passed
  in 15.66 s**.
- Direct local runtime checks: pinned embedding hash/load, actual local encode,
  isolated Chroma write/retrieval and selection isolation PASS; bad hash rejected.
- Full repository compilation with external bytecode cache and `git diff --check`:
  PASS. No configured lint/format tool was found. Docker rebuild/Compose and Azure
  checks were unnecessary because dependencies, images and deployment did not change.

Focused command (run from the credential-free source copy):

```bash
python -m pytest -q \
  tests/integration/test_foundry_l1_launcher.py \
  tests/integration/test_foundry_l1_entra.py \
  tests/integration/test_foundry_offline_workflow.py \
  tests/integration/test_managed_digestion.py \
  tests/integration/test_governed_digestion.py \
  tests/integration/test_publication_chroma.py \
  tests/unit/test_structured_provider.py tests/unit/test_foundry_approval.py \
  tests/unit/test_foundry_preflight.py tests/unit/test_foundry_30k.py \
  tests/unit/test_governance.py tests/unit/documents/test_managed_inference.py \
  tests/unit/publication
python -m pytest -q tests/unit/test_foundry_30k.py
python -m pytest -q tests/unit/documents/test_digestion.py \
  tests/unit/documents/test_extraction.py tests/unit/test_model_artifacts.py
```

Private temporary verification logs/source/runtime artifacts remain under
`/tmp/polymind-17hl-final-80l1t8rh/`. These are not the live audit directory.
The existing test group also retains offline L2 refusal/lineage regression; this
is not L2 execution authorization or redesign.

### C. Consolidated operator handoff

Reuse existing local evidence, registered identity, EUR pricing catalog,
immutable ledger policies, pinned embeddings, signing trust and persistent replay
directory. Do not regenerate any authority or key. The remaining operator work
can be reviewed as **one execution packet**, containing these external facts:

1. **Credential and shared quota:** confirm that the supplied API key is valid
   for the exact configured endpoint/deployment; set a conservative credential
   validity deadline and `credential_audience_verified`. For an API key this is
   an operator use deadline/resource-authority attestation, not a JWT `aud` claim
   or an invented intrinsic expiry. Supply actual Azure RPM, confirm 30,000 TPM
   and every shared consumer, then set `quota_verified` and
   `shared_consumers_verified`. Existing admission needs at least 2 RPM; a lower
   real allocation blocks execution. Respect both provider headroom and the
   existing owner/tenant 112,000-token allowance; do not relax ledger policy.
2. **Commercial and retention:** supply the source supporting the existing EUR
   catalog and defensible incremental fixed/additional charge upper bounds in
   `contract.price_source`, `fixed_cost`, `extra_cost`; explicitly exclude only
   the accepted existing AKS/Redis baseline. Do not assume unknown charges zero.
   Confirm the proposed maximum EUR 5 and set `charges_verified` and
   `contract.approved` only through actual authorization. Choose a private 0700
   per-run `audit_directory`, with retention/cleanup owner and independent
   reviewer. No new billable infrastructure is needed. The historical EUR
   0.11351636747626 token-only reservation is catalog arithmetic, not a new quote.
3. **Identity, key and final signature:** independently confirm the existing
   public-key fingerprint
   `35785596dd2f38a3ae5fc8eeb93015a1ba3c8b4f16f06a1d73fbe521f9657816`
   and its operator provenance; obtain a fresh verified Entra access token and
   choose `approval_expires`/credential deadlines covering the run. Keep the
   existing replay directory. Validate the final exact configuration, review
   unsigned bindings and obtain the separate live signature through the
   [operator procedure](../../evaluation/phase_17hl_operator_approval.md).

The draft's seven null fields are `credential_valid_until`, `approval_expires`,
`audit_directory`, `actual_azure_rpm`, `contract.price_source`,
`contract.fixed_cost` and `contract.extra_cost`. Four verification flags plus
`contract.approved` remain false. These are authorization/external-evidence gates,
not missing provider or document-processing implementation. The key fingerprint
and catalog arithmetic above reuse prior evidence; this task did not certify
independent provenance or current commercial terms.

**Exact proposed next action:** have the operator finalize and review this single
private packet, validate it with `load_configuration`, and obtain an independently
signed configuration-bound approval. Only after separate live authorization, use
the existing launcher arguments:

```text
python -m tests.performance.foundry_l1 --live
  --configuration <final-private-configuration.json>
  --approve-sha256 <validated-configuration-digest>
  --approval <operator-issued-approval.jwt>
  --approval-trust <existing-private-trust.json>
```

Supply fresh `POLYMIND_L1_OPERATOR_TOKEN` and `POLYMIND_L1_AZURE_CREDENTIAL` through
the private runtime environment, not command-line values or saved shell history.
This schematic command was **not executed**. It authorizes no spending. At most
four serialized provider requests may run, with no retry; failure stops earlier.
Preserve all approval/run markers and obligations even if preparation fails.
After that separately authorized run, an independent reviewer must assess source
support, qualifications, contradictions, injection resistance and citations in
the retained packets. Do not advance automatically to L2.

### D. Review and safety accounting

Self-review checked changed interfaces and repository consumers, all tracked
changes plus relevant pre-existing launcher/approval implementations, payload
schema visibility, admission accounting, evidence validation, replay behavior,
error paths and resource closure. The discovered envelope consumer was updated
and retested. The only production behavior change is additive trusted schema
instructions; prompts can now reject slightly sooner at the existing input bound.
No provider-specific branch was introduced into document/domain code, and no API
response format, dependency, migration or ledger policy changed.

Separate pre-commit review checks task files for secrets/private keys, debug and
temporary artifacts, local links, whitespace and unrelated changes. `.env` remains
ignored and Docker-excluded. Temporary logs/models/vectors stay outside Git.
Existing unrelated modifications were preserved. Before/after hashes, modes and
modification times confirm `.env`, all three existing authorities (and any
present sidecars), approval trust and replay contents are unchanged. The draft
backup is byte-identical to the initial draft and exactly the three intended
fields differ. Private signing keys were not read, generated or changed.

- Azure inference/provider requests: **0**.
- Azure resources inspected or modified in this task: **0**; paused AKS unchanged.
- Live approval artifacts issued or consumed: **0**. Test-only ephemeral approvals
  were exercised solely in isolated test directories.
- Financial spending authorized: **none**. EUR 5 remains the proposed ceiling.
- Authorities/replay reset, deleted or replaced: **none**.
- Git staging, commits and pushes: **none**.

Final `git status --short`: **10 modified tracked files and 26 untracked files**,
all unstaged, including preserved earlier work. `git diff --stat`: **10 files,
138 insertions, 8 deletions**; that tracked-only statistic omits untracked
launcher/tests/runbooks/reports. No stage, commit or push occurred.
