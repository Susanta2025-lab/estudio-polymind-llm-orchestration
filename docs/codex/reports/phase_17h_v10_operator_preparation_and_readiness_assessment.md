# Phase 17H v10 — operator preparation and readiness assessment

Assessment: 10 November 2026 UTC. **CONDITIONAL — V10 ENGINEERING READY;
OPERATOR OR CLOUD EVIDENCE INCOMPLETE.** Outcome B.

## 1. Executive summary and evidence boundary

The exact committed v10 source, successful GitHub CI, complete generation binding,
bounded provider-schema conversion/serialization, G1/G2, durable associations and
four-call controls are verified. No independently confirmed blocking engineering
defect was found. No engineering correction, CI remediation, redesign or new
generation is recommended from this assessment.

Current deployment state, authenticated operator access, signing trust/authority,
commercial applicability, financial/admission balances and fresh launch bindings
are not established. Those are prerequisites for operator progression, not facts
inferred from yesterday's successful authentication or settlements. **No current
paid exposure is authorized by this task.** Exact Azure schema acceptance remains
`LIVE_SCHEMA_ACCEPTANCE_UNVERIFIED`.

All mandatory references were read: AGENTS.md; the
[v10 implementation report](phase_17h_v10_application_owned_evidence_and_lineage_implementation.md),
[receipt ADR](../../adr/phase_17h_v10_generation_wire_receipt_decision.md),
[post-v9 review](phase_17h_post_v9_architecture_review_and_inference_simplification.md),
[v9 report](phase_17h_v9_source_identity_reliability_and_offline_readiness.md),
[v8 execution](phase_17h_v8_controlled_four_call_execution.md),
[v7 execution](phase_17h_v7_controlled_four_call_execution.md),
[Foundry runbook](../../evaluation/phase_17h_foundry_validation.md), current and
historical generation fixtures, and the production/evaluation implementations
identified below. The runbook's dated sections are historical where superseded.

A filename/content search of accessible repository documentation/tests found no
v10 Antigravity audit artifact. The user's supplied conclusion, “PASS — V10
INDEPENDENT SOURCE AUDIT ACCEPTABLE,” with no critical/high defects, is external
evidence. It was not independently verified against an audit transcript. Existing
references to earlier Antigravity findings do not supply that missing v10 audit.
No transcript or audit file was invented.

## 2. Exact Git baseline and committed-file review

| Observation | Verified result |
| --- | --- |
| Branch | `master` |
| Full HEAD | `ec22fa3d116696b80a1bb12ad17e2eb37db38cb3` |
| Local `origin/master` | Same full SHA |
| Actual remote master via read-only GitHub ref API | Same full SHA |
| Commit message | `feat(digestion): implement Phase 17H v8-v10 provenance and generation-wire hardening` |
| Commit timestamp | 2026-11-10 12:36:02 UTC |
| Entry tracked/index differences | None |
| Entry untracked files | 21 pre-existing Markdown documents |
| Initial `git diff --check` | Exit 0 |

Initial commands were `git status --short`, `git log --oneline -5`,
`git rev-parse HEAD`, `git rev-parse origin/master`, `git diff --check` and
`git branch --show-current`. No fetch or tracking-ref update was performed.
GitHub's actual remote ref was checked independently of the cached local ref.

The commit contains 85 changed files, 12,845 insertions and 202 deletions. The
v7/v8 execution records, v8/v9/v10 engineering reports, v10 ADR, active fixture,
historical renderers and full 15-source frozen v9 inventory are committed.
All 25 active inventory sources match both their fixture hashes and `git show
HEAD:<path>` bytes. Commit filename review found no private environment,
key/JWT/database/operator configuration file; private-key block-marker inspection
of its changed files found zero occurrences. This is a scoped source review,
not a forensic certification of every secret in all historical Git objects.
`.gitignore` excludes real dotenv inputs; `.dockerignore` additionally excludes
dotenv inputs and SQLite/database files and sidecars. No runtime secret was read.

## 3. Actual GitHub Actions verification

[Estudio PolyMind CI, run 42817169571](https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/42817169571)
tested the exact full SHA above on a push to master, attempt 1. Status
`completed`, conclusion `success`; created 12:36:16 UTC and updated 12:42:57 UTC
on 10 November. The jobs API reports one job, `build`, ID `129833074697`,
completed/success. No failed, cancelled or skipped job/step was returned.

All listed steps succeeded: checkout, Python setup, dependency installation,
compileall, automated tests, Helm setup/security lint/template, Compose config
and Docker build, followed by cleanup. The committed `.github/workflows/ci.yml`
runs unrestricted `python -m pytest` under Python 3.10 with testpaths `tests`.
The actual job log independently records **2,595 collected, 2,595 passed in
197.37 seconds**. Active wire/receipt/contract tests are included. This is actual
CI evidence, separate from the implementation report's prior 2,595-test local run.
No workflow was rerun or changed. CI status is **VERIFIED**, not CI_UNVERIFIED,
CI_PENDING or CI_FAILED.

## 4. Recomputed generation identity and compatibility

Production `tests/performance/foundry_l1.py::generation_contract_digest()` returns:

```text
managed-prompt/10
generation-inventory/2
e5fb249cc9b166b5e438f1534eb855fa5ab7531e08aa09314c110a1905327ebd
```

An independent SHA-256 calculation over the sorted compact JSON dictionary of
source-path → source-SHA256 values returns the same digest. Every one of the
25 source hashes matches `tests/fixtures/digestion_contracts/managed_prompt10.json`.
The fresh permanent contract tests also reproduce all nine pinned representative
request/generation/HTTP-payload hashes for chunk, structural and root. The
intermediate profile is separately exercised in current renderer diagnostics and
sizing tests. No fingerprint/schema fixture was refreshed or overwritten.

Inventory/2 covers managed rendering; wire schema/table/decoder; receipt and
checkpoint codec; deterministic identities; planning/sizing/G2/diagnostics;
workflow; worker/ledger/models/storage; provider/strict converter/structured
contract; publication analysis; L1/single-call composition, fixtures, preflight
and capability selection. The inspected new generation helpers are included.
Security/pricing/admission authority is separately configuration-bound and
reviewed; a generation digest alone is not an authorization credential.

Frozen v9's 15 source files independently reproduce every recorded hash and
aggregate `f270aa81cbd5764d2b4739bf3ac3692653b1fe4c8ffbd67860e642137cb2579d`.
Frozen v5–v9 result readability and rejection of old settings/requests/launch
digests pass the fresh compatibility tests. V7 and v8 fingerprints remain
`8426ab5cfef3e4d1925c68a5f8558c5bafc487dd746f0f7ccda799c03be16c3a` and
`93ca9066491c197987f919c5d185417bf4f3d2787384acf2833011e32641c0df`.
Readable historical results do not authorize execution or cross-generation
checkpoint reuse. Fresh v10 configuration binding is mandatory.

## 5. Current model-facing contract and canonical authority

`documents/digestion/managed.py` emits `stage-proposal/1` from
`wire.schema(references(request))`. Required top-level fields are schema_version,
request_binding, outcome, claims, open_questions and limitations. Each ordered
claim requires text, kind, status, subject, stance, evidence_refs,
contradicting_evidence_refs, qualifications and child_refs; qualifications require
text and evidence_refs. Stage/origin/claim UUIDs are not generated by the model.

`E1..En` resolve sorted authorized original-source UUIDs from current source pieces
and immediate children's direct supporting/contradicting evidence. Qualification-only
inherited IDs do not enlarge direct authority. `C1..Cm` resolve complete immediate
child `(stage_id, claim_id)` pairs in plan-child/claim order. The request binding
commits to the complete canonical StageRequest, source/pair tables and
`stage-decoder/1`. It detects inconsistency; it is not authentication.

`wire.construct()` checks bytes, duplicate JSON keys, exact object/scalar types,
version/binding, bounds, namespace/membership and duplicates. It preserves claim
order, resolves only explicit selections and assigns current stage/origin and
`stable_id(str(stage_id), str(position))`. It constructs unchanged `stage-result/1`
before independent G2 and complete child admission. There is no repair, dropped
claim, fabricated reference, automatic coverage attachment or extra model call.
Canonical source offsets/excerpts remain publication/Q&A authority.

## 6. Azure resource and deployment assessment

| Parameter | Current local expectation | Accessible evidence and limit |
| --- | --- | --- |
| Resource | `epolymind-foundry-dev-susanta` | Literal launcher/allowlist pin; historical v7/v8 observation, current cloud identity pending |
| Deployment | `epolymind-gpt-54-mini` | Literal pin and both role mappings; current deployment pending |
| Model/version | `gpt-5.4-mini` / `2026-03-17` | Literal configuration pin and allowed response aliases; current served version pending |
| Region | Spain Central | Historical observation and intended financial scope; `Contract.region` is a supplied string, not a hard-coded live location check |
| Class | `GlobalStandard` | Literal pin; current SKU pending |
| API | `/openai/v1/chat/completions` | Production builder/allowlist and current public v1 documentation; current deployment compatibility pending |
| Allocation | Historical 30 RPM / 30,000 TPM | Last recorded v8 checks on 9 November; no current quota observation |
| Shared consumers | Exclusive window must be independently attested | Yesterday's stopped-resource inventory/exclusivity does not cover a new window |
| Credential | Explicit `api_key` or `entra_bearer` | Separate application operator token; no current credential validity/authority verified |

Current public [Microsoft v1 documentation](https://learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle)
supports the versionless v1 contract and deployment-name model selection.
[Microsoft's model feature table](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning#api-and-feature-support)
lists structured outputs and Chat Completions for this model/version. These are
capability documents, not observations of this resource or exact v10 schema.

`deployment_configuration()` permits only HTTPS named-resource hosts under
`openai.azure.com` or `services.ai.azure.com`, path `/openai/v1`, with no userinfo,
port, query or fragment. Both summarization/general must use the approved
deployment. No private operational configuration was opened, so the actual next
endpoint has not been compared with a fresh packet. `api_key` uses `api-key`;
`entra_bearer` uses `Authorization: Bearer`. No token acquisition/refresh or
model-discovery probe is performed by this assessment.

Current Azure control-plane/resource/RBAC/billing verification needs a separately
authorized operator step and, if necessary, authentication. No Azure CLI, MSAL,
resource endpoint, JWKS endpoint or inference request was invoked here. Network
access was limited to authorized read-only GitHub CI/ref inspection and public
documentation retrieval. No Azure deployment-state claim is marked current.

## 7. Offline strict-schema compatibility and live limitation

All four production profiles pass the unchanged `azure-strict/1` converter,
Draft202012 witness validation and actual provider request serialization with
injected synthetic HTTP. Each converted schema has **17 total object properties**,
three object shapes, finite local refs to Claim, Qualification, SourceEvidence
and ChildReference, exact required-property sets and additionalProperties=false.
The converter's maximum container depth is **5 with root at zero** (six container
nodes on the longest qualification/evidence path). This is at the existing local
converter limit; its counting convention is not independent proof of Azure's
interpretation of the published nesting limit.

The four-source chunk has 19 enum values/197 value characters; eight-pair reducers
have 27/213, including fixed literals and the singleton binding. Sources are
bounded at 256 and split at 128 values per enum branch. The fresh matrix exercises
0/1/4/128/129/256 and rejection at 257 for every profile. anyOf occurs within
definitions/properties for nullable subject and split reference enums, never at
the root. Empty source/child authority uses null items; local decoding accepts
only empty reference arrays, rejects null elements/foreign keys and does not make
empty chunk analysis admissible. Array uniqueness/cardinality and removed string
constraints remain mandatory local checks.

The actual builder sends nonstreaming system/user messages, deployment model,
max_completion_tokens=3000, reasoning_effort=low, no sampling parameters, and
response_format=json_schema with strict=true and the converted schema. Its retained
schema name `polymind_stage_result` labels a response format; the required wire
schema_version remains stage-proposal/1. The decoder's canonical result then
passes unchanged G2. Q&A uses its existing separate JSON-object contract.

Public [Microsoft structured-output documentation](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs)
documents required fields, closed objects, local definitions, nullable alternatives,
enums/anyOf, a 100-property limit and five nesting levels. It describes schema
submission as part of inference. No independently documented non-billable
schema-only validation/compilation endpoint was established from the accessible
documentation. The repository's historical `foundry_schema_probe.py` is a
generation-pinned, separately approved one-call preparation path, not a free
schema compiler or current v10 authorization. It was not invoked.

**`LIVE_SCHEMA_ACCEPTANCE_UNVERIFIED`.** No hidden probe, max-token trick, free-tier
assumption or provider request was used. A future approved four-call experiment
can observe acceptance on its first chunk and stop on rejection. That uncertainty
must be explicitly reviewed before signing/execution; it does not authorize an
extra fifth call or a separate probe. Offline passes establish local compatibility
only, not model compliance, completion sufficiency or semantic accuracy.

## 8. G1 resource readiness and fresh sizing

Current `foundry_preflight.py`, managed settings, sizing and provider code retain
input allocation **24,800**, complete context **28,000**, output reservation
**3,000**, complete child **7,000 bytes**, digestion raw/canonical **10,000 bytes
each**, HTTP envelope **26,192 bytes**. Q&A has 24,800 input bytes, 3,000 output,
12,000 raw bytes, and the generic HTTP bound `12000*6+8192 = 80,192`.
The larger Q&A HTTP bound is existing behavior, not the digestion limit.

Fresh eight-claim/four-source measurements use current production rendering,
conversion, decoding and requests-style JSON serialization. Input adds the
existing 100 overhead + 100 safety; context adds 3,000 reserved output.

| Profile | System/data bytes | Schema/strict bytes | Complete envelope | Input/context estimate | HTTP JSON bytes | Wire/canonical | Complete child |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Chunk | 2,937 / 1,917 | 2,423 / 1,715 | 7,485 | 7,685 / 10,685 | 7,196 | 1,893 / 3,317 | 5,333 |
| Intermediate | 2,993 / 2,056 | 2,474 / 1,766 | 7,959 | 8,159 / 11,159 | 7,679 | 1,925 / 4,126 | 6,206 |
| Structural | 3,002 / 2,056 | 2,474 / 1,766 | 7,968 | 8,168 / 11,168 | 7,688 | 1,925 / 4,126 | 6,206 |
| Root | 3,005 / 2,056 | 2,474 / 1,766 | 7,971 | 8,171 / 11,171 | 7,691 | 1,925 / 4,126 | 6,206 |

HTTP diagnostics use synthetic model name offline-model, three characters shorter
than the prior report's synthetic name; this explains the three-byte HTTP-only
difference. Schema/envelope/wire/canonical measurements agree with the v10 report.
The complete child includes inherited metadata and artifact material; permanent
G1 tests independently apply worst-size artifact references before commitment.
Source maps, atomic pair lists, singleton binding, strict schema, qualification/
contradiction material and full canonical expansion are included. Planner analysis
adds 64 conservative bytes per authorized source; reduction retains full canonical
child reservations despite the compact wire projection.

An independent production preflight rehearsal using the ordinary authored fake
responses completes all four calls, with eight publication citations:

| Call | Full envelope | Input/context estimate | HTTP JSON | Response format |
| --- | ---: | ---: | ---: | --- |
| Chunk | 7,485 | 7,685 / 10,685 | 7,196 | Strict schema |
| First reducer | 6,152 | 6,352 / 9,352 | 5,865 | Strict schema |
| Root | 5,897 | 6,097 / 9,097 | 5,605 | Strict schema |
| Grounded Q&A | 7,986 | 8,186 / 11,186 | 7,758 | JSON object |

The ordinary rehearsal's maximum planned input is 12,502. Its reducer prose is
smaller than the separate eight-claim witness above. Fresh permanent workflow
tests additionally exercise the eight-claim, qualified, contradictory witness
through publication, citations and reopening. Exact ASCII/quote/backslash/newline/
BMP/astral Unicode path boundaries, one/two children, source cardinalities and
canonical expansion are covered by the sizing/decoder tests. Boundary overflow
is rejected; schema capacity is not a promise of G1 admission.

These are conservative ASCII-JSON byte-based estimates, not optimistic measured
token counts or provider billing. All required benchmark request families fit
the tested witnesses without increasing limits. Actual live children, retrieved
annotations and completion sufficiency remain unknown; production must admit
each actual request/output and stop when it cannot fit. A synthetic Q&A envelope
cannot preapprove an unknown future live Q&A payload.

## 9. G2 provenance and semantic limitation

`documents/digestion/validation.py` is byte-identical to its frozen v9 inventory
entry. Its authority remains independent of wire construction. Inspection and
fresh tests verify original scoped EvidenceRefs/spans, exact source membership,
source coverage, qualification/contradiction references, current stage/origin,
positional IDs, exact immediate pairs, complete child coverage, duplicate rejection,
invalid-stage refusal, inherited summaries and final original-source resolution.
Finalization/publication reopen the accepted graph rather than trusting model
success. Qualification-only inherited evidence is retained without acquiring new
direct source authority.

An authorized E key can still cite text that does not substantively support the
claim; an authorized C key can represent a poor semantic synthesis. Structural
membership, full coverage and G2 do not establish entailment. After an authorized
successful evaluation, an independent human reviewer should annotate each factual
claim against original evidence and review omissions, qualifications, conflicts,
abstention and citation excerpts/offsets. Preserve numerators/denominators and
pending/disputed judgments under the existing quality rubric; do not infer quality
from fake output or use automatic repair/model-based source correction.

## 10. Durable checkpoints, receipts and recovery

Source inspection covers `receipts.py`, `workflow.py`, codec, LocalObjectStore,
IntentStore/Worker and SQLiteJobLedger. V10 manifests are ordered canonical
checkpoint → decoding receipt → exact raw provider record. Historical manifests
retain one checkpoint reference. No checkpoint/model/database migration is required;
the ledger already supports atomic multiple-ObjectRef manifests.

Known usage settles in GovernedExecution before managed raw capture and decoding.
Raw records bind plan/job/step, original attempt/fence, complete request/table,
generation/audit/config hashes and exact response hash/text. Receipts bind raw
ObjectRef, canonical checkpoint and canonical result hash. G2, inherited summary
and complete G1 checks precede checkpoint/receipt acceptance. Intent registration
and hash/scope inspection precede fenced atomic ledger commitment, success and
dependent activation. Object writes use private temporary files, fsync and atomic
link-if-absent; SQLite uses synchronous FULL transactions.

Reopening reconstructs requests/tables, verifies immutable bytes, original
successful attempt/fence, manifest association and canonical re-decoding, then
reruns G2/inheritance/parents/G1. Multihop reuse follows ledger-owned edges with
identical manifests. Fresh tests cover repeated resumes, orphan/corrupt artifacts,
all interruption windows, stale fences, idempotent commitment and duplicate delivery.
Uncommitted records are never automatically adopted; the one-attempt L1 policy
does not reissue inference. A crash may leave settled usage without an accepted
checkpoint. This is conservative recovery, not exactly-once provider delivery.

Operational preparation still must verify private audit/replay directories and
existing security/governance/admission files: absolute outside-repository paths,
operator ownership, no symlink/hard-link substitution, private permissions,
distinct authority files, audit isolation, sufficient disk space and working
SQLite/object fsync/atomic-link semantics. Verify the approved local embedding
tree/revision and digest, local-only loading and CPU/vector-store capacity.
No actual operational path, permission, store or database was changed or opened
through a write-capable constructor. Disposable test storage does not verify
the next operator destination. No additional v10 production storage migration
or service is identified.

## 11. Security, operator identity and RSA authority

`verify_approval()` verifies the application access token, exact owner scope and
**`Action.PUBLICATION_MANAGE`**. The launcher separately requires the existing
registered enabled principal through SecurityAuthority. Digestion uses a scoped
`DOCUMENT_DELETE` authorization snapshot as the existing owned-resource contract;
Q&A uses DOCUMENT_ANALYZE. Source/document grants, owner/tenant and revocation
epochs remain enforced. PUBLICATION_MANAGE is not permission to change governance
or grant tenant administration.

The Entra v2 profile requires tenant-specific issuer/JWKS, API audience, RS256,
expiry/not-before/issuance, delegated `access_as_user`, a user identity and exactly
`PolyMind.L1Operator`, mapped to PUBLICATION_MANAGE. Current principal, registration,
actual delegated role/scope, Azure RBAC/credential authority and useful lifetime
are pending. An application API token is separate from the provider credential;
historical Graph/OID correlation and historical successful authentication do not
prove today's enabled account or usable token. No verification that could fetch
JWKS, authenticate or refresh credentials was invoked against real authority.

`foundry_approval.py` requires independently provisioned live public trust, RSA
2,048–8,192 bits, exact key ID/header, RS256, issuer polymind-operator-approval/1,
audience polymind-l1-live, purpose live, canonical UUID, integer iat/nbf/exp,
maximum 24-hour artifact lifetime, exact operator issuer/subject/tenant and exact
canonical binding. The binding includes the configuration digest, Foundry target,
financial ceiling/charges, limits and expiry. Configuration includes generation,
paths, policy/catalog, identity, embedding and timing. Any change invalidates the
signature. Operator identity, financial approval and independent signing authority
are separate requirements.

L1's source recipe is bound through the inventoried fixture/composition and the
configured owner scope; the deterministic plan is reconstructed from those inputs.
The existing approval schema does not add independent source/plan digest fields.
Fresh operator review should retain those derived artifact hashes alongside the
canonical configuration, without inventing new approval fields or editing the
implemented contract during preparation.

Historical v7/v8 records describe RSA-3072 public trust verification and separately
authorized signing. No designated current public-trust artifact/fingerprint or
independent signing authorization was verified here; no private key, token,
approval or trust configuration was opened to infer one. Trust correspondence and
current signer authority therefore remain PENDING_OPERATOR. The verifier is ready
in source/synthetic tests; no actual saved v10 signature was created or verified
by this assessment. Synthetic fixture signatures are not operational RSA signing.

## 12. Governance, admission and four-call failure contract

The live composition remains chunk → structural first reducer → root → grounded
Q&A. It admits one step attempt, forbids managed attempt !=1, allows at most
four full run reservations (100,000 input/12,000 output), one outstanding call,
one start per rolling minute and runtime scheduling of at least **61 seconds**.
No automatic paid retry or model fallback exists. The provider session disables
environment proxies, refuses redirects, uses 5/60-second connect/read and
60-second total generation bounds, and is closed on failure.

LaunchConfiguration requires more than 600 seconds of approval/credential
lifetime and a not-before plus 600 seconds earlier than both deadlines. Runtime
checks approval, credential and principal expiry before scheduling, refusing when
60 seconds or less remain, and checks cancellation during one-second wait loops.
Historical operator wrappers additionally required a twenty-minute launch margin
and a stricter explicit cutoff. Those are separate operator controls; they must
be established for the new packet rather than assumed to be enforced by the
launcher's ten-minute configuration check.

The candidate shared policy is 2 RPM/30,000 TPM, two slots with one interactive
slot/RPM and at least 2,000 interactive TPM reserved. Background is at most one
slot/RPM and 28,000 TPM; a larger existing interactive reserve wins. Local
admission cannot establish the absence of external clients or prevent Azure's
short-window enforcement. Current quota/exclusivity must be checked separately.

EvaluationBinding validates exact shared authority paths/key/policy hash and
allowlisted scopes. Its evaluation limits are 16 requests/86,400 seconds,
112,000 outstanding tokens, 500,000 daily tokens, 1,500,000 monthly tokens and
EUR 5 owner/tenant monthly accounting. Existing non-evaluation policies and
other scopes remain distinct. These source values are not today's balances or
new authorization. RunGuard never refunds its full token/call reservations from
smaller usage; unresolved work blocks continuation. Known measured usage settles;
unknown/excess/inconsistent usage retains conservative obligations.

| Failure | Existing termination behavior |
| --- | --- |
| HTTP 400/422 including confirmed strict-schema rejection | Sanitized configuration error; no retry/fallback; schema reason retained only when recognized |
| HTTP 401/403/other failure, timeout, 429/5xx | Normalized provider error; L1 one-attempt policy stops even if generic classifier is RETRYABLE |
| Refusal/malformed strict envelope | Protocol failure; no accepted checkpoint |
| Output truncation/raw/HTTP limit | Output-limit failure; known valid usage retained for settlement |
| Wrong binding/version/table | incompatible_checkpoint/profile_mismatch; terminal affected run |
| Unknown E/C key or duplicate | Evidence rejection/invalid_reference; no repair |
| Missing source/child coverage | Coverage rejection; no downstream work/publication |
| Incorrect canonical identity/semantic shape | Independent G2 contract rejection |
| Receipt/checkpoint/attempt/fence/hash association failure | Fail-closed verification or ledger/storage failure; no accepted dependent |
| G1/G2 rejection | Failed stage, cancelled dependents, no publication/Q&A; prior accepted bytes preserved |

Fresh fault tests verify failures at chunk/first/root, one attempt, settled known
usage, no failed-stage manifest, cancelled unattempted dependents and no publication
or Q&A. Failure classifiers and retry policies were not modified. No real
admission, policy, authority, reservation or settlement constructor was invoked.
Normal authority/usage helpers can write audit rows or initialize configuration;
they are not safe substitutes for a deliberately read-only operational inspection.

## 13. Financial calculation and unresolved commercial applicability

The authoritative code contract requires approved EUR pricing, an effective date
not in the future, matching provider/deployment, positive rates, full four-call
fit and explicit fixed/extras. `Price.cost()` uses Decimal arithmetic. The local
EUR 5 maximum is a configured comparison/admission ceiling, not an Azure spending
cap or reusable user authorization.

Current public [Azure pricing guidance](https://azure.microsoft.com/en-us/pricing/details/azure-openai/)
states that prices depend on agreement/date/currency; its accessible table does
not supply a current account-applicable EUR quote. The
[Microsoft model launch price table](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/introducing-openai%E2%80%99s-gpt-5-4-mini-and-gpt-5-4-nano-for-low-latency-ai/4500569)
still provides reference USD 0.75/M input, 0.075/M cached input and 4.50/M output.
At uncached reference rates, maximum 100,000 input + 12,000 output is **USD
0.129**, before extras. This reference is not current verified account pricing
or an applicable EUR tariff. No cached-input discount is assumed.

For verified EUR input/output rates I/O per million, the conservative token
exposure remains **0.1 I + 0.012 O**, plus verified fixed, tax/network/contingency
allowances. V10's smaller wire payload does not reduce the approved maximum
reservation, because actual billed usage/completion behavior is still unknown.

The pre-existing local historical migration summary
`phase_17h_v5_authorized_catalog_migration_and_commercial_reconciliation.md`
reports catalog phase17hl-pricing-eur-202611/1, effective 7 November, with
input **EUR 0.673279770188/M**, output **EUR 4.039678621124/M**, including reasoning
in output. Its catalog hash is
`59c90a122e3db199848ae0817218bc4286bab80b22920a0916d8f5a54426dd37`.
That untracked pre-existing report is historical evidence, not a current opened
authority or newly committed commercial approval.

Independent Decimal recalculation of that historical scenario gives:

| Component | Historical-rate scenario EUR |
| --- | ---: |
| Maximum four-call tokens | 0.115804120472288 |
| 23% token VAT budgeting allowance | 0.02663494770862624 |
| VAT-inclusive networking contingency | 0.10 |
| Conservatively serialized aggregate extras | 0.126634947709 |
| Total using serialized extras | **0.242439068181288** |

This is conditional arithmetic, not a currently approved v10 forecast. Historical
23% VAT was a budgeting instruction, not independently established invoice tax.
Commercial applicability, current meter classes/currency/conversion, cached usage
semantics, tax treatment, public network/diagnostics/storage route, fixed charges
and shared-consumer obligations must be checked for the new window. No account
pricing/billing API or current authority was opened, no tariff was substituted,
and no reservation or settlement was created.

Current budget headroom, rolling/daily/monthly request/token headroom, outstanding
reservations, active provider calls and maximum approved exposure remain unknown
operational facts. Last historical v8 values cannot be used as current balances.
Verify both owner and tenant and the same shared admission authority using a
separately designated read-only mechanism (for SQLite, mode=ro plus query_only,
without constructing audit-writing authorities). Unknown obligations must remain
reserved; do not reset/reprice/reopen them. If a new tariff conflicts with the
stored catalog, stop for separately authorized reconciliation. **No positive
paid-execution allowance is granted here; authorized exposure from this task is 0.**

## 14. Historical execution, settlements and replay integrity

The committed v7 report records three provider calls, 11,131 input/5,211 output,
EUR 0.028545042416639792 catalog cost, two accepted checkpoints and rejected root
lineage; no publication/Q&A. The committed v8 report records one provider call,
2,749 input/1,609 output, EUR 0.008350688989635328, rejected chunk source membership
and no accepted checkpoint. Both approvals were consumed. Latest v8/v9 summaries
record 13 settled reservations, zero unsettled/active calls and ten consumed
markers. V5 financial history includes an explicitly recorded prospective catalog
transition; old settlement amounts/catalog labels were preserved. V9 is offline
engineering, not evidence of another successful live attempt.

Those are attributed historical observations. Their private rows/markers/audit
files were not reopened today, so **current** settlement/replay inventory is
PENDING_OPERATOR. No claim of fresh byte-for-byte private-store reconciliation
is made. All accessible pre-existing checkout files and historical reports are
preserved by this task.

The approval verifier compares exact configuration/bindings; LaunchConfiguration
rejects old generation hashes; managed plans/settings reject incompatible
generation; receipt recovery checks exact request/config/attempt associations.
`consume()` uses exclusive O_EXCL/O_NOFOLLOW creation of the approval UUID marker
with file/directory fsync, outside the run audit directory and shared across key
rotation. `live-started.json` is a separate exclusive guard. Partial/uncertain
launch consumes authority; there is no reset or automatic replay command.
Fresh tests verify repeated approval rejection and changed-configuration denial.
This is a trusted single-host protection, not resistance to an administrator
deleting state or a distributed exactly-once guarantee.

Previous signatures cannot authorize v10, even if still cryptographically valid.
No old approval/window/call balance is reused. Before any new signing, independently
verify historical markers remain consumed, preserve settlement/audit state and
choose/review a fresh unused identity without consuming it in preparation.

## 15. Fresh offline verification and reproducibility

All rerun tests use PYTHONDONTWRITEBYTECODE=1,
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1, PYTHONPATH=.:/tmp/phase17h-g1-g2, the inspected
existing `-p offline_guard -p no:cacheprovider`, disposable --basetemp and JUnit
outside the checkout. The guard denies socket connect/connect_ex/sendto and
connection/DNS helpers before collection; configuration isolation suppresses
implicit application dotenv loading. No live provider factory/credential source
was used. Synthetic signature/auth fixtures and disposable authorities do not
represent operational signing/authentication or real-state mutation.

| Fresh check | Actual outcome |
| --- | --- |
| Focused wire/sizing/receipts/contracts/launcher/approval/preflight/30K/Entra selection | **646 passed**, 477 unit + 169 integration, 107.76 seconds, zero failures/errors/skips, zero network attempts |
| Transport errors/evaluation finance/independent G2 lineage selection | **103 passed**, all unit, 6.79 seconds, zero failures/errors/skips, zero network attempts |
| Independent fingerprint/source/production-schema/builder/canonical/full-L1 diagnostic | Exit 0; 25 source and committed-byte matches; four profiles; synthetic L1 COMPLETED, Q&A COMPLETE, four calls, eight citations, zero network attempts |
| Frozen v9 source inventory reconstruction | 15/15 hashes and aggregate match |
| `PYTHONPYCACHEPREFIX=<temporary-cache> python -m compileall -q .` | Exit 0; no ownership changes or checkout bytecode output |
| Documentation preservation/security/link/whitespace review | Passed, as described below |
| Final `git diff --check` | Exit 0 |

The two fresh selections are disjoint: **749 unique tests**; their counts are
not added to the prior full-suite or CI totals. JUnit independently verifies
counts and absence of failures/errors/skips. The complete expensive suite was
not rerun. The original implementation's 2,595 local passes and today's actual
2,595 CI passes remain separate evidence.

The 646-case selection contains these modules: unit/documents/
test_generation_wire_v10_decoder.py and test_generation_wire_v10_sizing.py;
integration/test_generation_wire_v10.py and test_managed_prompt10/9/8/7_contract.py;
integration/test_foundry_l1_launcher.py and test_foundry_l1_entra.py; unit/
test_foundry_approval.py, test_foundry_preflight.py and test_foundry_30k.py.
The 103-case selection is unit/test_structured_provider.py,
unit/test_evaluation_governance.py and unit/documents/test_direct_child_lineage.py.

Diagnostic script/JSON, JUnit, logs, disposable stores, checkout preservation
hashes and external bytecode cache reside under
`/tmp/phase17h-v10-readiness-20261110/`. The first focused invocation had a missing
temporary parent directory and reported 50 passes/596 setup errors; it is not
claimed as a passing run or an application defect. JUnit output created that
parent; the corrected invocation used a fresh basetemp and passed all 646.
No test expectation or production code was changed to obtain the pass.

No new tests/dependencies/workflows or implementation edits were needed. Local
Docker/Compose/Helm/Kubernetes operations were unnecessary for this documentation
assessment and not run; successful CI container/config checks are attributed to
CI, not claimed as local checks. No full lint/type run is claimed for unchanged
implementation.

## 16. Required operator readiness checklist

VERIFIED applies only to the specific evidence in that row. Pending operational
rows cannot be inferred from a neighboring verified source/test row. There are
no confirmed BLOCKED engineering/security/financial defects in this assessment;
unknown live state must still prevent signing/execution until its relevant gate
is satisfied.

| Requirement | Status | Evidence | Required next action |
| --- | --- | --- | --- |
| Exact committed v10 source | VERIFIED | Full SHA, clean tracked tree, local/actual remote refs match | Preserve/freeze exact reviewed source |
| GitHub CI | VERIFIED | Run 42817169571, build 129833074697, 2,595 passes | Recheck if source changes |
| Generation fingerprint | VERIFIED | Production + independent hash, 25/25 sources | Pin exact digest in fresh private configuration |
| Historical compatibility | VERIFIED | Frozen inventory and v5–v9 contract tests | Never execute old settings as v10 |
| G1 admission | VERIFIED | Sizing matrix and actual renderer/builder | Apply to each actual live payload |
| G2 validation | VERIFIED | Unchanged validator, positive/negative tests | Preserve independent runtime enforcement |
| Decoder/receipt integrity | VERIFIED | Binding, corruption, crash/recovery tests | Preserve three-object association |
| Synthetic four-call execution | VERIFIED | Fresh production rehearsal and permanent workflow tests | Do not equate with live model compliance |
| Independent audit transcript | PENDING_OPERATOR | User conclusion external; no local v10 file | Supply actual audit if independent transcript verification is required |
| Resource identity | PENDING_OPERATOR | Literal local pin; historical observation | Verify selected current resource/subscription/tenant |
| Deployment identity | PENDING_OPERATOR | Literal local deployment | Verify current deployment and endpoint |
| Served model/version | PENDING_OPERATOR | Local gpt-5.4-mini / 2026-03-17 pin | Verify actual served version/aliases |
| Region/class | PENDING_OPERATOR | Historical Spain Central/GlobalStandard | Verify actual location/SKU and financial match |
| API/strict capability documentation | VERIFIED | Public v1/model docs and current builder | Bind exact next endpoint/capability |
| Actual configured endpoint/API | PENDING_OPERATOR | No fresh private configuration opened | Compare approved v1 host/path and auth mechanism |
| Offline strict-schema compatibility | VERIFIED | Four profiles, real converter/builder, no network | Freeze exact schemas/generation |
| Live strict-schema acceptance | PENDING_OPERATOR | LIVE_SCHEMA_ACCEPTANCE_UNVERIFIED | Review uncertainty; observe only in separately authorized provider work, stop on rejection |
| Free schema compilation probe | NOT_APPLICABLE | No independently established non-billable mechanism | Do not invoke a probe on an assumption |
| Current RPM/TPM allocation | PENDING_OPERATOR | Historical 30/30,000 only | Verify current allocation without changing it |
| Shared consumers/exclusivity | PENDING_OPERATOR | Historical window expired | Verify consumers and attest a fresh exclusive window |
| Current operator identity | PENDING_OPERATOR | Only historical identity evidence | Independently verify current user, tenant, subject and enabled registration |
| Application/RBAC/source/publication rights | PENDING_OPERATOR | Required permissions verified in code | Verify actual delegated role/scope, Azure rights and owned source authorization |
| OIDC/token/provider credential readiness | PENDING_OPERATOR | No live token/key inspected | Separately authorize authentication if needed; verify audience and practical lifetime |
| Signing-key trust/current signer authority | PENDING_OPERATOR | Historical public trust only | Verify public fingerprint/key ID/operator correspondence and independent authority |
| Approval verifier | VERIFIED | Strict RS256 bindings and fresh tests | Independently verify actual saved artifact only after authorized signing |
| Replay protection mechanism | VERIFIED | Durable exclusive markers, no reset, fresh tests | Preserve same replay authority |
| Actual consumed-marker inventory | PENDING_OPERATOR | Historical ten consumed markers | Designated read-only comparison; no reset/reuse |
| Governance/admission policy mechanism | VERIFIED | Scope/path/policy binding, no-replenishment tests | Verify actual authorities and selected policy unchanged |
| Applicable current input/output tariff | PENDING_OPERATOR | Public USD reference; historical EUR catalog | Verify commercial applicability/effective date/meters/currency/unit |
| Cached input/VAT/network/fixed allowances | PENDING_OPERATOR | Historical uncached + 23% + EUR 0.10 scenario | Confirm current conservative assumptions and exclusions |
| Cost arithmetic/reserved usage | VERIFIED | 100,000/12,000; Decimal formula and historical scenario recomputed | Recalculate with verified current applicable rates/extras |
| Current v10 cost forecast | PENDING_OPERATOR | No current approved tariff/contract | Review exact complete four-call maximum |
| Budget headroom | PENDING_OPERATOR | Historical balances only | Read-only owner/tenant + commercial/shared obligations check |
| Reservation/token/request headroom | PENDING_OPERATOR | No current operational ledger read | Verify rolling/daily/monthly/outstanding/active usage for both scopes |
| Historical settlement state | PENDING_OPERATOR | Reports say 13 SETTLED, zero unsettled | Verify rows unchanged and no new unresolved usage |
| Maximum authorized paid exposure | PENDING_OPERATOR | This assessment authorizes zero; historical EUR 5 is inactive authority | Obtain fresh explicit financial and paid-execution authorization |
| Exact immutable benchmark source recipe/hash | VERIFIED | phase17h-pdf/1, four pages/six lines, seed 1708; same source SHA as historical record | Bind actual private source/extraction to verified owner scope |
| Current operator-scoped plan | PENDING_OPERATOR | Only disposable current synthetic plan | Produce/review fresh immutable v10 plan without paid work |
| Generation contract for execution | VERIFIED | Exact managed-prompt/10 digest above | Include in new canonical configuration |
| Fresh configuration | PENDING_OPERATOR | None generated/operationally approved here | Prepare exact target/principal/source/plan/catalog/policy/paths/embedding bindings |
| Operational storage/embedding readiness | PENDING_OPERATOR | Requirements in code; disposable checks only | Verify actual private paths, ownership, modes, capacity and local embedding tree |
| Practical launch/credential window | PENDING_OPERATOR | No active window from this task | Independently establish not-before, cutoff, expiry and exclusivity |
| Independent RSA signing approval | PENDING_OPERATOR | Explicitly withheld by this task | Separate authorization for exact reviewed configuration/bindings |
| Saved v10 signature verification | PENDING_OPERATOR | No operational artifact created | Verify independently after separately authorized signing |
| Separate paid-execution approval | PENDING_OPERATOR | Explicitly withheld | Separate approval of exact signed packet, exposure and one controlled invocation |
| Independent semantic/citation quality | PENDING_OPERATOR | No accepted live v10 output | Review source versus output after authorized evaluation |
| New database/storage migration | NOT_APPLICABLE | Existing multiple-ref manifest/unchanged database schema | None identified |

Benchmark source SHA-256:
`1be99e19a56040fb55c74682a19f874d4d4573f18d9f52a9a7ae19c8158ea92d`.
This is a public synthetic fixture hash, not private source text or a live scope.

## 17. Pending authorizations and recommended next phase

**Next appropriate step: operator verification.** No engineering correction or
GitHub CI remediation is currently indicated. The user can separately authorize
a narrowly scoped operator-verification/preparation step to establish current
Azure identity/deployment/quota/consumers, application identity/permissions,
public trust, operational storage, current pricing and read-only ledger/replay
state. Interactive authentication, credential acquisition and operational packet
creation remain outside this task; none is implicitly authorized by this report.

Before requesting independent RSA signing, finish those current evidence checks,
prepare/review a fresh exact v10 source/plan/configuration and unused replay
identity, calculate the full applicable allowance, establish a practical window,
confirm signer authority/public trust and explicitly review the remaining live
schema/model uncertainty. Do not derive a Principal from old saved metadata or
reuse old unsigned/signed bindings. External audit transcript retrieval is an
evidence-completeness action, not an independently discovered engineering blocker.

Then obtain **separate RSA signing authorization** for that concrete configuration
and bindings. Independently verify the saved signed artifact and recheck current
conditions. Only after that obtain **separate paid-execution authorization** for
one controlled invocation and the exact maximum exposure. Neither authorization
is requested, issued or consumed here. If authorized later, at most four calls,
single concurrency, >=61-second starts, zero retries/fallback and first-failure
termination remain mandatory. No extra schema probe is included. Semantic quality
review follows accepted live output; full Phase 17H closure is not established.

## 18. Self-review, pre-commit review and final Git state

A separate assessment self-review checked source-versus-cloud evidence labels,
schema-depth convention, wire-versus-canonical sizing, Q&A's distinct transport
limit, settlement-before-decoder ordering, conservative unknown-usage treatment,
multihop checkpoint reuse, historical approval exclusion and the difference
between generation binding and authority. No confirmed blocking defect emerged.
The outcome remains CONDITIONAL because current operational evidence is missing,
despite verified CI and offline engineering. No independent reviewer/sub-agent
participation is claimed by this task.

The documentation-only pre-commit review checks both new files for private keys,
tokens/passwords, private operator configuration/source prose, raw responses,
unintended paths/dependencies, stale claims, broken links, whitespace and scope
drift. A before/after inventory verifies all **529 pre-existing nonignored
checkout files** unchanged, including the 21 inherited untracked documents.
Generated tests/stores/logs/JUnit/bytecode remain outside the checkout. This is
not a private authority-file preservation audit; those files were not opened.
Only the two authorized documentation files are new. No production/API/schema/
policy/financial/historical record was edited; architecture is unchanged.

Final `git status --short`: **zero tracked modifications, zero staged changes,
23 untracked Markdown files** (21 inherited plus this prompt/report). Branch,
HEAD and local origin/master remain as recorded above. Final `git diff --stat`
is empty; untracked documents are correctly excluded from that statistic.
`git diff --check` passes. No staging, commit, push, ref/history change, cloud
operation or real operational state mutation occurred.

**Final decision: CONDITIONAL — V10 ENGINEERING READY; OPERATOR OR CLOUD EVIDENCE
INCOMPLETE.** Exact source and offline controls are ready for a separately scoped
operator-verification phase; current signing and paid execution remain gated.

**Git staging: NO
Git commit: NO
Git push: NO
Azure authentication: NO
Azure inference: NO
RSA signing: NO
Approval consumption: NO
Operational state mutation: NO**
