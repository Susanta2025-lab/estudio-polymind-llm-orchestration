# Phase 17H-L: zero-cost preparation and live approval contract

> **Current status — 12 November 2026:** controlled v11 Azure Foundry evaluation
> completed 4/4 successful calls, 3/3 checkpoints, G1/G2, provenance, complete
> digest, publication and grounded Q&A PASS. `PHASE_17_ENGINEERING_COMPLETE`;
> `DEFERRED_PENDING_TWO_INDEPENDENT_REVIEWERS` (0/2);
> `PHASE_17_FORMAL_CLOSURE_PENDING`; `NEXT_PHASE_DEVELOPMENT_PERMITTED`.
> See the [completion decision](phase_17_engineering_completion_and_deferred_acceptance.md)
> and [review register](phase_17_deferred_human_semantic_review.md). Production
> readiness remains unestablished. This runbook grants no new execution authority.

## Historical engineering checkpoints

The dated v10/v9 notes below preserve their original engineering-task conclusions.
Their active-profile and unfinished-live statements apply to those checkpoints;
the 12 November status above supersedes them for current project tracking.

**10 November v10 engineering update (active contract):**
[managed-prompt/10](../codex/reports/phase_17h_v10_application_owned_evidence_and_lineage_implementation.md)
replaces canonical model output with `stage-proposal/1`. Models select exact
request-bound E source keys and atomic C immediate-child keys; the application
assigns stage/origin/positional claim identities and constructs canonical
`stage-result/1`. V9's strict source membership protection is retained as E-key
enums and strengthened by the same deterministic decoder in every transport mode.
No reference repair or automatic evidence/lineage attachment is performed.

An accepted v10 step manifest contains the unchanged checkpoint, immutable
decoding receipt and exact raw proposal record. Existing ledger fencing and
atomic manifests bind them together. Recovery and publication reconstruct the
exact request/tables and re-decode before accepting the canonical graph. Orphans
cannot authorize inference or become checkpoints. See the
[receipt and recovery decision](../adr/phase_17h_v10_generation_wire_receipt_decision.md).
Historical single-checkpoint manifests remain readable under their original
profiles. The generation inventory expands to version 2; new configuration must
pin the complete new digest in the v10 report. Historical approvals remain
incompatible and consumed markers must be preserved.

All runtime ceilings remain: 24,800 managed input, 28,000 context, 7,000 complete
child, 10,000 raw/canonical bytes, 3,000 output, maximum four L1 calls, one concurrent
call, minimum 61-second starts, zero automatic paid retries and no fallback.
A future operator phase must manually review v10, verify the exact Azure schema,
current authorities and financial/admission headroom, and obtain new separate
signing and paid-execution authorizations. No such preparation or execution is
performed by this engineering task. The dated v9 and earlier guidance below is
historical where superseded by this update. Live compliance remains unverified.

**9 November v9 offline update:** The [v8 controlled evaluation](../codex/reports/phase_17h_v8_controlled_four_call_execution.md)
stopped after one provider-successful chunk call: G2 rejected one foreign original
source UUID at `claims[6].evidence_ids[1]`. All eight claim identities were correct.
All four allowed IDs appearing elsewhere did not authorize that extra reference.
No checkpoint, reducer, publication or Q&A was accepted. Usage is settled and the
approval is consumed. The earlier v7 run also remains a failed lineage evaluation.

At that checkpoint, generation was [managed-prompt/9](../codex/reports/phase_17h_v9_source_identity_reliability_and_offline_readiness.md).
Strict digestion now restricts direct evidence, contradicting evidence and nested
qualification references to the exact current authorized source set in the
request-specific `SourceEvidence` schema definition. The set is unchanged: source
pieces plus direct supporting/contradicting IDs from immediate child claims;
qualification-only inherited IDs do not become new direct authority. An empty
set uses null items, permitting only empty reference arrays in a valid UUID result.
G2 still rejects null items, foreign/malformed IDs, duplicates and missing coverage.

Strict requests carry the authorized set once in the response schema; redundant
`CONTROL.schema` and `CONTROL.allowed_evidence_ids` are omitted. Prompt-based
modes retain those fields and explicit complete, indivisible UUID-copying rules.
Strict configuration allows at most 256 IDs; enums are partitioned into at most
two existing `anyOf` branches of 128 IDs (4,608 UUID characters per branch).
No result model, source authorization, transport, checkpoint or publication API
changes. Invalid output is never repaired. These are generation constraints,
not proof that a deployed endpoint accepts this exact new schema or that a model
chooses semantically correct sources.

The v7 current-stage identities and v8 exact immediate-child lineage rules remain.
Direct links must copy `(stage_id, claim_id)` pairs together from
`CONTROL.required_child_links`. Qualifications/conflicts continue through valid
lineage. G1/G2 validation source and independent acceptance predicates are unchanged.

Measured maximum empty-material L1 envelope: 7,251 bytes; fixed planning reserve:
7,379 including 128 bytes of enum scaffolding. Empty-path one/two-child reserves
are 14,379/21,379, leaving 3,421 path bytes for two children under 24,800. Actual
system/data/schema and bounded transport serialization still require admission.
The 28,000 context, 7,000 complete-child, 10,000 raw/canonical response and 3,000
output limits remain. Maximum paid L1 calls: four; automatic retries: zero.

The v9 generation digest is
`f270aa81cbd5764d2b4739bf3ac3692653b1fe4c8ffbd67860e642137cb2579d`.
Historical v5/v6/v7/v8 bindings remain incompatible with current execution;
historical checkpoints remain readable. Existing consumed approvals stay consumed.
The v9 task is offline only. A future controlled attempt requires fresh v9-bound
planning/configuration, endpoint/schema capability review, current authority and
financial checks, independently authorized RSA signing, and separate explicit paid
execution authorization. Do not reuse old approvals or infer authority from
synthetic success. Full live four-call compliance and semantic quality remain open.

## Current interpretation of the historical runbook

The dated proposals and handoffs below preserve earlier NOT STARTED, missing-key,
JSON-object and L0/L1/L2 checkpoints. Their pending states describe their dates,
not the current v11 workflow. Current explicit v11 uses `stage-proposal/1` with
application-owned `stage-result/1` identities, immutable raw records and receipts;
all G1/G2, complete-child, context and transport limits remain enforced. Default
v10 selection remains compatible. The successful
[v11 execution](../codex/reports/phase_17h_v11_controlled_live_execution_and_reconciliation.md)
needs no repeat to obtain two human reviews under the unchanged
[frozen protocol](phase_17h_v11_live_semantic_validation_protocol.md).

The single-analysis and full-L1 approvals have separate audiences; every consumed
historical approval, including v11's, grants no further authority. Identity,
permissions, credential use, financial acceptance, exact-configuration RSA signing
and paid execution remain separate gates. Local EUR 0.009675030297596252 token
settlement is not final Azure invoice/VAT/network verification. Representative
production quality, scale, workload reliability and external exposure remain
separate prerequisites; the engineering-completion decision does not pass them.

## Historical L0 proposal and subsequent dated handoffs

L0 prepares a validation project; it authorizes no inference. See the
[preflight report](../codex/reports/phase_17h_live_preflight.md) for executed
evidence and blockers. Phase 17H remains PARTIAL. L1 and L2 are NOT STARTED.

## Executable offline stages

Run separately from the repository root in the existing Python environment:

```bash
python -m tests.performance.foundry_preflight --stage L1 --output /tmp/new-17hl-l1
python -m tests.performance.foundry_preflight --stage L2 --output /tmp/new-17hl-l2
```

Both commands are **offline rehearsals**, not live launch commands. The CLI has
no live mode, constructs only a fake HTTP transport, blocks socket connections,
and never loads credentials or invokes the provider factory. Choose fresh paths
outside the checkout. The main process uses umask 077. Synthetic quotas use a
virtual clock advanced 61 seconds between requests; this is not live pacing.
Live composition remains blocked until the operator inputs and full request
envelopes below have been verified. Do not repurpose the test principal issuer,
synthetic price catalog, fake embeddings, or virtual clock for live execution.

The executable composition uses the unchanged Phase 17H PDF generator and source
verification, native extraction, `prepare`/`admit`, `ManagedDigestionHandler`,
`ManagedSynthesisInference`, `GovernedExecution`, `GovernanceLedger`, and
`SQLiteInferenceAdmission`. Fake responses pass through the existing
`OpenAICompatibleProvider.execute` transport parser. The normal hierarchy,
evidence validation, COMPLETE digest, authorized publication, selected-document
retrieval, canonical citation resolution and `DocumentAnalysis` are exercised.
No Foundry SDK, production interface change, dependency, or separate digest
implementation is added.

The candidate profile retains the six-lines/page fixture, 3,200-character chunks,
fan-in four, eight claims, eight annotations, full coverage and all lineage rules.
Context is bounded to 28,000, output to 3,000 and result characters to 3,000.
The old profile used 60,000/6,000/6,000 respectively. The existing profile validator
requires result characters <= reserved output. This explicit candidate size
change does not permit dropping evidence or accepting partial output; a result
that cannot fit must fail. Real-model expressiveness within 3,000 characters is
unvalidated. Do not quietly reduce claims, source coverage or the rubric.

## Endpoint and capability requirements

The adapter appends `/chat/completions` to the configured base URL. A candidate
v1 base has the public format `https://<resource>.openai.azure.com/openai/v1`
or `https://<resource>.services.ai.azure.com/openai/v1`. Microsoft documents that
v1 removes the dated `api-version` requirement and accepts deployment names in
the model field. This identifies a candidate API contract, not the absent local
deployment. [Microsoft v1 documentation](https://learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle).

The current provider sends only `Authorization: Bearer <configured secret>`;
it has no Entra token acquisition/refresh, `api-key` header configuration, or
dated Azure URL/query builder. A valid operator-supplied Entra access token may
fit this transport, but audience, role and lifetime must be verified. Do not
assume an Azure API key works as a bearer token for the selected deployment.
If the chosen service requires `api-key` or a dated deployment URL, stop and
make a separately reviewed narrow adapter change. Do not paste a query string
into the base URL or introduce a Foundry SDK to bypass this check.

`summarization` must map to the approved deployment for all digestion stages;
`general` must map to that same deployment for question answers. Other role
entries are required by application Settings if the factory is used, but do not
authorize other workloads. Returned model aliases must be explicitly verified.
The candidate must support system/user chat messages, bounded nonstreaming JSON,
the selected `max_tokens` or `max_completion_tokens` parameter, and unambiguous
`prompt_tokens` and `completion_tokens`. Verify whether output counts include
reasoning tokens and whether every billable token class is covered by the rates.
Reject unknown usage semantics or additional token meters.

`CapabilityProfile` requires verified context/output limits, overhead, safety,
response mode (`prompt`, `json_object`, or non-strict `json_schema`), supported
temperature behavior, aliases and usage reporting. Strict Azure JSON-schema
support is not implied by the adapter's `strict:false` request. Prompt-only JSON
still undergoes the full application schema/evidence checks. No automatic repair,
model fallback or unbounded legacy generation is allowed.

Repository defaults: connect 5 s, read 120 s; managed total 60 s; readiness 3 s
with one retry and 0.1 s backoff; job attempts default three. The candidate uses
read 60 s, total 60 s, lease 120 s and **one attempt per step** (no automatic
retry). Bounded transport does not perform model retries. Never run `/models`
readiness/discovery to choose a deployment. The model/deployment must be supplied
by the operator. Every eventual retry counts as a new inference attempt.

## Redacted configuration and operator inputs

Copy the [approval template](phase_17h_foundry_approval.template.json) to private
operator storage; fill every null there. Do not put endpoint/deployment/principal
identifiers or credentials in tracked documentation. Its approval flags are false
and unknown prices are null deliberately; it is not runnable Settings JSON.

Required configuration names, whose values must remain private:

```text
INFERENCE_PROVIDER=openai_compatible
OPENAI_COMPATIBLE_BASE_URL=<verified-v1-base>
OPENAI_COMPATIBLE_API_KEY=<secret supplied through private environment>
OPENAI_COMPATIBLE_MODEL_MAP=<all roles; summarization/general use approved deployment>
DOCUMENT_INFERENCE_CAPABILITY=<verified CapabilityProfile JSON>
DOCUMENT_INFERENCE_PROFILES=<four bounded StageProfile entries>
DOCUMENT_DIGESTION_PROFILE=<reviewed candidate DigestionProfile JSON>
API_AUTH_MODE=oidc_jwt
OIDC_CONFIGURATION=<approved issuer/audience/JWKS/role mapping>
GOVERNANCE_ENABLED=true
SECURITY_AUTHORITY_PATH=<private absolute security SQLite path>
GOVERNANCE_AUTHORITY_PATH=<private absolute governance SQLite path>
GOVERNANCE_PROVIDER_PATH=<private absolute provider-admission SQLite path>
GOVERNANCE_PROVIDER_KEY=<shared upstream quota identity>
GOVERNANCE_POLICY=<owner and tenant QuotaPolicy>
GOVERNANCE_PRICING=<exact approved PricingCatalog>
GOVERNANCE_PROVIDER_POLICY=<shared AdmissionPolicy>
```

For OIDC also set `API_AUTH_ENABLED=false` and **unset** `API_AUTH_TOKEN`, including
an empty assignment. See [17G's operator contract](../security/phase_17g.md).
Only the verified identity path may issue live principals. Digestion needs the
owning principal and a `DOCUMENT_DELETE` snapshot, as required by the existing
managed handler; Q&A needs `DOCUMENT_ANALYZE`. Publication needs an approved
`PUBLICATION_MANAGE` operator. The principal must remain valid for the whole
stage; there is no delegated long-lived job identity or automatic refresh.

All authorities must be distinct private files on one trusted host. Share the
same run guard and governance/admission authorities across L1, L2 and retries;
never allocate a fresh budget for each stage or reset unresolved expense. A live
launcher must bind these verified objects, replace the test-only fake transport
and clock, and verify the L1 acceptance receipt before admitting L2. This binding
is deliberately not exposed as a CLI switch in L0 while identity/authentication
and request feasibility remain unresolved.

## Financial approval: proposal of at most EUR 5

No price is currently applicable because model, version, region and tier are
unknown. [Azure's pricing page](https://azure.microsoft.com/en-us/pricing/details/azure-openai/)
distinguishes token-based Standard pricing from provisioned capacity and warns
that displayed estimates are not binding quotes. Obtain the operator's actual
matching price schedule, source and effective date. No promotional credit or
cached-input discount is assumed. No deployment or capacity change is permitted.

Let `I` and `O` be approved input/output rates, `U` the pricing unit, `F` a known
upper bound on attributable fixed/hourly charges over the approved run duration,
and `A` all other separately billed charges. Every value is currently **UNKNOWN**.
The budget currency must be EUR for the proposed guard; it refuses other currencies,
unknown charges, future-effective/mismatched catalogs and budgets over EUR 5.
A different currency/limit requires a revised reviewed contract, not guessed FX.

| Workload | Attempts | Reserved input | Reserved output | Maximum reserved cost |
| --- | ---: | ---: | ---: | --- |
| L1: digestion + one native-page factual question | 4 | 100,000 | 12,000 | `(100000 I + 12000 O) / U` |
| L2: digestion + all 12 rubric questions | 45 | 1,125,000 | 135,000 | `(1125000 I + 135000 O) / U` |
| Combined planned | 49 | 1,225,000 | 147,000 | `(1225000 I + 147000 O) / U + F + A` |
| Absolute ceiling, including one spare attempt | 50 | 1,250,000 | 150,000 | `(1250000 I + 150000 O) / U + F + A` |

Fixed/extra charges are counted once across the run, not once per stage. Confirm
whether any provisioned/hourly charge exists, even on an existing deployment;
record both its amount and marginal attribution. Unknown or unbounded duration
charges block execution. Separately billed evaluators, embeddings, search,
storage or infrastructure are not silently included. L0 uses local fake vectors;
live local embedding artifacts and their absence of external calls must be verified
before use. No additional evaluation LLM is approved.

The 49 planned attempts fit the numeric project ceiling; only one spare remains.
Cost and actual quota fit are **UNKNOWN**. L2 is **not admitted**: managed prompts
depend on generated children and inherited findings. Fake rendered requests fit,
but this does not prove that all valid real child outputs or Q&A annotations fit
25,000 input tokens. Verify the complete managed request envelope, not just the
17D planning estimator. If it cannot fit, propose a new complete DAG and recalculate
all calls (including L1, questions and retries); refuse L2 until approved. Do not
omit inherited evidence or rubric cases to force the 50-call ceiling.

## Accounting and mandatory stops

`foundry_budget.RunGuard` implements `InferenceAdmissionPort` around the existing
17E authority, underneath `GovernedExecution`. It atomically persists a full
25,000-input/3,000-output run reservation before downstream admission. Full run
reservations are never refunded from smaller usage. The existing 17G ledger
separately reserves the rendered bound and settles measured expense. RunGuard
counts all stages/workloads and retries against cumulative tokens, attempts and
exact Decimal cost including F/A, with a durable single outstanding-call rule.
Configuration is pinned on reopen. A crash/denial leaves a conservative outstanding
reservation; there is no automatic reset, refund or reconciliation command.

The candidate provider policy uses RPM 2, TPM 30,000, concurrency 2 with one
interactive slot, one interactive RPM and one interactive TPM reserved. The
existing policy requires positive interactive headroom. RunGuard imposes the
stricter **one total concurrent request**, RPM <=2 and TPM <=30,000 across both
workloads. Full 28,000-token reservations effectively allow one call per minute;
wait at least 61 real seconds between requests in live work. Any stricter available
quota wins and must be represented before admission. Never enlarge a quota.

Stop on the **first** provider failure, timeout or 429 (stricter than repeated
failure), missing/partial/inconsistent usage, usage above reservation, any
admission/governance denial, identity mismatch, capability/schema incompatibility,
invalid evidence, critical unsupported conclusion, publication inconsistency,
unexpected billable dependency or cancellation. Application validation failures
terminate the worker stage before further provider work. Security/governance
denial cannot be treated as a retryable model failure. Cancelled or crashed work
retains its financial obligation pending trusted reconciliation.

The guard is additional local admission, not a guarantee about delayed Azure
billing. Rate-limit estimates are never billed usage. Record both the reserved
maximum and observed usage/cost; reconcile against trusted provider/billing
evidence. External consumers and service-side metering remain outside this guard.

## Evidence and stage gates

L1 must pass extraction, planning, durable admission, managed hierarchy, canonical
evidence validation, COMPLETE digest, publication/retrieval/citations, and independent
review of the predefined native-page question before L2. Stop on any critical
failure. The four-page source has no ORION facts from pages 5/100/180/199; its
smoke question uses the reproducible page-1 procedure instead.

L2 uses the exact versioned 200-page recipe and `phase17h-ground-truth/1`, with
`phase17h-rubric/1`. Its 12 questions cover direct and distant reasoning, opposition,
qualifications, revised values, missing evidence, false premises and injected
instructions. Real authorization/selection controls for similar or unauthorized
documents need explicit case setup before live evaluation; repeating their text
against one authorized PDF is not isolation evidence. L0 merely rehearses those
question requests and preserves pending packets.

The annotation-driven `tests.performance.quality.evaluate` remains authoritative.
Packets retain question/rubric, selected document/version, response hash, actual
citations, required findings and nullable fields for extracted factual claims,
independent reviewer, unsupported conclusions, qualifications/contradictions,
abstention and disagreements. Resolve citations against canonical source text;
annotate each factual claim independently. A second LLM is neither authorized
nor an independent human reviewer. Never fill reviewer fields from fake output.

Report citation validity, supported claims, required findings, critical unsupported
conclusions, qualification/contradiction preservation and abstention with both
numerators and denominators, plus reviewed responses/total responses and reviewed
claims/total claims. Pending or disputed claims are not silently counted as
supported. Historical targets: 100% structural citations, >=95% independently
supported claims, >=90% required findings, zero critical unsupported conclusions.
One low-density synthetic PDF cannot certify representative expert semantic quality.

## Final operator handoff

Approval is needed because the Phase 17H-L task explicitly withholds live spend
authorization. First supply the missing non-secret deployment/capability/pricing/
quota facts through the private template and resolve the blockers. Then approve
the exact EUR limit, full proposed cost calculation, principal/scope, retention,
model/region/tier, stage plan and L1 execution. L2 requires separate approval and
accepted L1 evidence. Merely approving EUR 5 without these facts is insufficient.
No approval is requested for the already completed offline work.

## GPT-5.4 mini — 30,000 TPM Deployment Recalibration

2026-10-13. This update supersedes the earlier unknown-deployment and short-response
envelope assessment, preserving the original L0 evidence. See the detailed
[recalibration report](../codex/reports/phase_17h_live_preflight.md#gpt-54-mini--30000-tpm-deployment-recalibration)
for sources, all eight stress cases, price arithmetic and file inventory.

Operator-confirmed: `epolymind-gpt-54-mini` in
`epolymind-foundry-dev-susanta`, GPT-5.4 mini version 2026-03-17, Global Standard,
Global scope, 30K TPM on October 13. The portal/screenshot observation is supplied
by the operator, not independently inspected. `eci-gpt-54-mini` remains excluded.
No Azure request was made to verify deployment, quota or authentication.

Published model support permits the candidate Azure v1 Chat Completions contract:
`max_completion_tokens=3000`, `reasoning_effort=low`, no temperature/top-p,
JSON-object output validated against application schemas. Reasoning is included
in completion usage and output limit. Model context is 400K, output maximum128K;
our run uses a stricter 28K context envelope. Real output sufficiency and aliases
remain L1 observations, never reasons to silently increase limits.

Candidate shared admission reserves 2,000 TPM, one RPM and one slot for interactive
work; background has at most 28K TPM, one RPM and one slot. Run concurrency is one,
shared application RPM at most two. A larger existing interactive reserve wins.
Azure RPM, other consumers and operational headroom are still unknown. At full
reservation use at least 61 seconds between starts and wait for completion/admission.
Azure estimates and short-window enforcement can still refuse a locally valid call.

L1's four conservative structural families pass. Maximum background input is
13,915 (18,915 TPM including output and headroom); contradiction-heavy Q&A input
is 23,039 (26,039 combined). The permitted ceiling stays 25K input + 3K output,
not the measured fake response usage. Four calls reserve 100K input/12K output.
The fake full pipeline passes, but **live L1 technical readiness is BLOCKED** until
endpoint/authentication, principal/governance/admission bindings and a reviewed
operator-bound live launcher exist. Stress tests are not proof of every possible
model response or independent human quality review.

**L2 is technically infeasible under the current complete-evidence plan.**
Escaped reductions reach 32,141 input; complete 32-link lineage requires 3,754
result bytes versus 3,000 allowed; all 12 rich-annotation Q&A requests overflow
(even prose reaches 82,387 input; contradictions reach 154,403). Do not truncate
or weaken evidence, lineage, qualifications, contradictions or the rubric. Future
small experiments should reduce reducer fan-in and bound Q&A via evidence-complete
retrieval/paging, then re-plan every call and cost before seeking approval. These
are recommendations, not implemented capabilities. More quota alone is insufficient.

At published reference USD 0.75/M input and 4.50/M output, uncached reservations
cost L1 USD 0.12900; original blocked L2 USD 1.45125; combined USD 1.58025; one spare
attempt USD 0.03225. All 50 attempts cost USD 1.61250 plus unknown extras. Source:
[Microsoft March 17 launch table](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/introducing-openai%E2%80%99s-gpt-5-4-mini-and-gpt-5-4-nano-for-low-latency-ai/4500569),
checked October 13. Publication date is not the operator's pricing effective date.
EUR 5 is still only a proposal. Require approved EUR rates or explicit conversion,
region/agreement/tier, currency/unit/date, all fixed and additional charges, quota
and final maximum. Unknown charges block admission. Automatic retries remain zero;
a separately authorized retry uses the same cumulative ledger. L2 is separately gated.

Reproduce offline only, with new private outside-repository output directories:

```bash
python -m tests.performance.foundry_envelopes --output /tmp/new-17hl-envelope-audit
python -m tests.performance.foundry_preflight --stage L1 --output /tmp/new-17hl-l1-offline
python -m tests.performance.foundry_preflight --stage L2 --output /tmp/new-17hl-l2-offline
```

The envelope diagnostic never invokes a model. Its `complete` flag describes
structural fixture construction; inspect every record's failure and admission
flags. It intentionally continues offline after oversized render detection to
measure dependent stages. The fake workflow remains useful regression evidence,
not permission to run the rich L2 DAG. Retained results avoid another benchmark run.

Final targeted verification: **198 passed in 65.68 s**, including financial
persistence/unknown usage, 30K headroom, rolling windows, provider output parameters,
JSON mode, model aliases, full rendered envelopes and network-forbidden fake
workflows. The earlier 69-test result is historical. No full 732-test rerun.

All 17 relevant configuration names remain absent from process and `.env`.
Privately complete the approval template, including endpoint/auth mechanism,
actual RPM/headroom/consumers, exact pricing and extras, identity scope, existing
ledger locations, retention and independent reviewer. Do not copy credentials into
this repository. The approval template is not an executable live launcher.
**L0 PARTIAL; L1 NOT STARTED, AWAITING APPROVAL; L2 NOT STARTED, AWAITING APPROVAL.**

## L1 Azure integration readiness — 2026-10-13

This section supersedes the earlier missing-launcher finding. The operator-bound
launcher now exists in `tests/performance/foundry_l1.py`; **offline integration
PASS**, **live execution NOT STARTED**. Actual authentication, identity, pricing
and shared authority configuration remain unverified, so **L0 remains PARTIAL**.
L2 remains blocked and its architecture was not changed.

The default command is safe to run without configuration or credentials:

```bash
python -m tests.performance.foundry_l1 --output /tmp/new-private-l1-dry-run
```

It refuses existing/repository output directories and forbids socket connections.
Live execution requires an additional `--live` option, a private configuration
file and `--approve-sha256` matching that configuration. **Do not invoke live mode
until the operator separately approves L1.** This task did not invoke it against
Azure; integration tests intercepted all HTTP.

Copy only `launcher_configuration_template` from the approval template to a
private JSON file, then replace every null/false prerequisite with verified data.
It is intentionally invalid as supplied. The exact schema is
`LaunchConfiguration` in the launcher. Reuse actual existing OIDC settings,
security database, governance policy/catalog and admission database/key/policy;
the launcher refuses missing authorities and configuration mismatches. Do not
initialize replacements to clear debt or relax policies. Owner scope must equal
the verified principal's scope; that principal must already be registered with
`PUBLICATION_MANAGE` and retain ownership/analyze authorization through every call.
No synthetic identity or price is created by live construction.

The configured OIDC verifier still authenticates the access token, including the
[Entra v2 scope and role contract](../security/entra_v2.md). The custom issuer claim
`polymind_l1_approval` is **no longer required or accepted as approval**. Approval
now comes from a separate compact RS256 JWS artifact and independently provisioned
public-key trust file. See the [operator approval procedure](phase_17hl_operator_approval.md)
for exact schemas, signature format, trust provisioning and replay handling.

Live mode additionally requires `--approval /private/operator-approval.jwt` and
`--approval-trust /private/approval-trust.json`. The existing `--approve-sha256`
acknowledgement remains required. The digest is SHA256 of validated
`LaunchConfiguration.model_dump_json().encode()` (not raw file bytes). Use
`load_configuration(private_path)` locally to calculate it without printing the
configuration. The verified principal must match `owner_scope`, the signing-key
trust policy and the signed artifact. Changing endpoint, prices, limits, paths,
identity anchors or expiry invalidates approval. No signing keys or approvals are
created by the launcher. The proposal template remains unsigned and invalid for
live mode; its `purpose=test` is explicitly rejected.

`POLYMIND_L1_OPERATOR_TOKEN` and `POLYMIND_L1_AZURE_CREDENTIAL` are separate runtime
environment inputs. Never place their values in the template, shell history,
reports or Git. No credential was retrieved during this task. Authentication
selection is explicit: `entra_bearer` sends `Authorization: Bearer ...`; `api_key`
sends `api-key: ...`. The [Microsoft v1 contract](https://learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle)
documents both REST headers, `/openai/v1` and the absence of a dated API-version
requirement. Exact resource host and credential authority/audience still require
operator verification. No token acquisition/refresh or Azure model discovery is
implemented. Approval and credential lifetime must initially exceed ten minutes;
the scheduler stops when less than a request-minute remains.

The endpoint allowlist accepts only the named PolyMind resource's public
`openai.azure.com` or `services.ai.azure.com` v1 host, with no query, userinfo or
port. Private gateways need a separately reviewed change. Both `general` and
`summarization` map to the named deployment. Bounded HTTP refuses redirects;
proxy/environment credentials are disabled on the launcher's owned session.
The established candidate uses JSON object, low reasoning effort, 3,000 inclusive
completion tokens, no sampling parameters, approved response aliases and complete
usage. There is no provider/model fallback or automatic retry.

Live L1 uses the same native PDF extraction, canonical verification, durable job,
managed hierarchy, evidence validation and authorized publication/Q&A workflow as
the rehearsal. Publication uses an isolated local Chroma collection under the audit
directory, the existing Chroma adapter and an approved local embedding model loaded
with `local_files_only=True`. No shared Chroma, Redis, AKS or cloud embedding service
is configured or changed. Approve local CPU/storage costs explicitly. The local
embedding tree digest binds sorted relative file names followed by NUL and each
file's binary SHA256; symlinks are refused. The operator must verify that the hashed
tree is the pinned MiniLM revision before signing. Ranking retains the deterministic
reranker used by this smoke fixture; expert semantic ranking is not certified.

The run guard caps **four attempts, 100K input, 12K output**, one concurrent request
and one start per rolling minute; the scheduler waits at least 61 seconds and checks
cancellation/expiry each second. Shared admission preserves at least 2K interactive
TPM, or the larger configured reserve. A smaller effective bound refuses execution;
there is no silent evidence reduction. Actual Azure RPM and all shared consumers
must be attested. Full four-call cost must fit the approved EUR contract including
fixed/extras before execution; every call is additionally checked against durable
run and owner/tenant budget. The USD 0.129 reference is not an approved EUR quote.
The maximum possible authorized contract is EUR 5; current authorized spend is zero.

A durable exclusive approval-ID record in the independently configured replay
directory consumes the signed approval before preparation can lead to inference.
The record and parent directory are fsynced. Consumption is shared across runs and
signing-key rotation, independent of the per-run audit directory. The existing
exclusive `live-started.json` and call records remain additional guards, including
for legacy runs. A failed/uncertain start consumes approval too. Preserve all
markers and ledger records; never switch replay directories to retry.
Unknown usage, timeout, 429, cancellation or validation failure stops the run;
there is no automatic refund. A private `CANCEL` file requests cancellation before
the next scheduled step. A crash retains ledger obligations even if a summary was
not written. This is a single-host guard, not protection against an administrator
deleting its files or a guarantee about delayed Azure billing.

Private audit files include per-call hashes/text/usage/duration/outcome, durable
financial settlement, fixture manifest, canonical artifacts, publication evidence,
and the response/citation human-review packet. Runtime errors are sanitized; no
raw upstream errors, tokens or headers are saved. Reviewer fields remain pending.
The actual response cannot be called independently supported until reviewed.

Verification: complete regression ran once, **842 passed in 166.28 s**. Focused
checks passed **159 tests in 26.70 s**; final fake-workflow checks passed **4 in
41.77 s**. After an audit-failure resource-cleanup correction, the final launcher
checks passed **24 in 5.84 s**, including transport closure on audit write failure.
Full regression was not repeated. Detailed commands/evidence are in the report.

## Final offline handoff — 2026-10-14

The existing private draft now matches the actual `.env` endpoint, selects
`api_key` authentication and records a proposed incremental EUR 5 ceiling.
Approval remains false; no live signature has been issued or consumed. Use this
existing draft and authorities, not a fresh template or replacement ledgers.
The launcher supplies its own capability and stage profiles; absent generic
`DOCUMENT_INFERENCE_*` environment entries do not make this launcher incomplete.
It explicitly chooses the `api-key` header and does not use the generic provider
factory. Both live roles resolve only to `epolymind-gpt-54-mini`.

Q&A now sends its exact output schema in trusted prompt instructions, including
in JSON-object mode, and reserves the additional bytes. The four-page
contradiction-heavy question envelope increases from 23,039 to 23,548 conservative
input tokens, still below the 25,000 per-call limit. No bounds were relaxed.
The source remains the documented deterministic native four-page PDF evaluation
fixture; this is a controlled real-model experiment, not validation of arbitrary
customer PDFs. Live identity, prices, inference and embeddings must be real.
Semantic claims remain pending independent review.

Follow the final report's consolidated operator handoff and the separate
[approval procedure](phase_17hl_operator_approval.md). No live invocation is
authorized by this documentation. L2 remains blocked.
