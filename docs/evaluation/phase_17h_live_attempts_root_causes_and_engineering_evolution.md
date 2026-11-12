# Phase 17H Azure Foundry live evaluations: root causes and engineering evolution

Documentation assessment: 12 November 2026. Historical execution cutoff: the successful 11 November 2026 v10 evaluation. Repository baseline: `master`, `ec22fa3d116696b80a1bb12ad17e2eb37db38cb3`.

## 1. Executive summary

Estudio PolyMind progressed from a locally tested managed-document pipeline to a controlled, fully executed four-call Azure Foundry evaluation. This required successive corrections to representation budgets, error attribution, generation constraints, stage identity, immediate-child lineage and durable evidence association. The application consistently distinguished receiving model output from accepting it as trustworthy checkpoint material. Several successful, billable provider responses were correctly rejected by application validation.

The discoverable record contains **11 actual live evaluations and 17 provider calls**. Nine evaluations terminated unsuccessfully; two of those had accepted upstream digestion checkpoints. Azure Attempt 6 succeeded at its explicitly authorized **single-analysis** goal but did not execute the full workflow. The final v10 evaluation completed chunk analysis, structural reduction, root reduction, digest construction, publication and grounded Q&A. Its four calls, three checkpoints, nine managed manifest objects and settlements were independently reconciled in the contemporaneous [v10 execution report][V10].

For mutually exclusive progress counts, this is **seven failures without accepted chunk output, three partial-workflow evaluations** (the successful bounded Attempt 6 plus failed v5 and v7 workflows), and **one fully successful workflow**. “Partial” describes workflow reach, not a replacement for the recorded terminal state: v5 and v7 FAILED, Attempt 6 SUCCEEDED.

The decisive v10 change removed canonical identity construction from the model's duties. The model selected request-local `E` source keys and atomic `C` child-pair keys in `stage-proposal/1`; deterministic application code constructed canonical claims and their stage origins. Immutable raw records and decoding receipts were committed with checkpoints under the existing durable workflow authority. Existing G1/G2 acceptance remained mandatory.

**Current engineering position:**

- **Phase 17H v10 controlled live evaluation: SUCCESSFUL.**
- **G1/G2 integrity and four-call execution: VERIFIED for the evaluated fixture.**
- **Semantic-quality acceptance for structural/root reducers: NOT YET SATISFACTORY.**
- **General production readiness: NOT ESTABLISHED.**

Reducer prose overemphasized processing metadata and opaque aliases. The four-page fixture and correct tested Q&A do not establish representative summary quality, expert acceptance or general reliability. This documentation does not formally close Phase 17H and authorizes no further evaluation.

## 2. Scope and evidence methodology

### 2.1 Inventory and evidence hierarchy

Read-only discovery covered `docs/codex/reports/`, `docs/codex/prompts/`, `docs/evaluation/`, `docs/adr/`, `docs/security/`, the earlier engineering postmortem, `tests/performance/`, `tests/integration/`, `tests/fixtures/`, and relevant `documents/`, `llm/`, `security/` and `governance/` implementation. Git status, history, commit statistics and the existing source/test diff were inspected without checkout changes. Repository instructions were read before writing. Search inventory found 85 relevant report files, 64 prompts, six evaluation documents and three ADRs; these are discovery counts, not counts of independent experiments. File content and chronology, rather than names, determine inclusion.

Evidence priority is: retained execution/settlement/checkpoint records, contemporaneous diagnostic reconstruction, committed implementation and frozen contracts, then later summaries. The first-three-attempt postmortem and [Attempt 6 closure][A6] explicitly identify the older evidence they reconcile. Later engineering tests explain mechanisms; they do not create new historical live outcomes. Prompts establish intended scope, not proof of execution. No external research, Azure read, authentication, credential access, signing, approval operation or inference was needed for this documentation.

**Access limitation:** the private v10 sanitized inventory at the location identified by [V10][V10] is not present in this workspace. No private credentials, source payloads or authority databases were opened. Receipt-level and private-artifact conclusions below are attributed to their existing sanitized reports; this task does not claim fresh cryptographic or database verification of unavailable originals. Repository implementation and frozen fixtures were inspected directly. Original private receipt basenames are indexed in section 12 to support a separately permitted future audit.

### 2.2 Interpretation rules

**Established recorded fact** means an explicit outcome in the cited execution/diagnostic record. **Evidence-supported conclusion** means the observed artifacts and documented code path support the explanation. **Interpretation** identifies a plausible mechanism without claiming access to model reasoning. **NOT VERIFIED** denotes missing evidence, not zero or a negative result.

Five boundaries remain distinct:

1. Provider admission/request attempt and known billable usage.
2. Provider completion, including strict response handling where configured.
3. Application decoding, domain validation, G2 provenance and G1 admission.
4. Durable fenced checkpoint-manifest acceptance.
5. Full digest, publication, retrieval and grounded-Q&A completion.

A provider completion does not establish boundaries 3–5. Attempt 6's application acceptance also must not be relabeled a durable three-stage workflow result.

### 2.3 Names, dates and generation bindings

“Azure Attempt 1–6” names experiments, whereas `managed-prompt/N` names generation templates. They are **not the same sequence**. L0/L1/L2 identify evaluation scope; offline rehearsals and test invocations are neither paid experiments nor additional attempt numbers. This report uses H01–H11 only as chronological row labels. No historical attempt is renamed.

A prompt number alone is insufficient to reproduce execution. Source-derived generation hashes also changed for enforcement, diagnostics and inventory changes. In particular, pre-G1 and post-G1 v4 are not identical source bindings. Commit dates identify repository checkpoints, not necessarily the date the earlier uncommitted implementation was evaluated.

## 3. Preparation and chronological live-evaluation register

### 3.1 Earliest preparation and blocked non-evaluations

The [original Phase 17H report][BASE] established bounded local reliability and a quality-evaluation harness, while expressly leaving real-model quality and Foundry validation pending. The [live-preflight history][PRE] records preparation through 13–14 October: candidate Azure v1 Chat Completions compatibility; exact deployment/model mapping; API-key headers; low reasoning effort and completion limits; OIDC principal registration; pinned local embeddings; financial inputs; shared quota; and independent operator approval. Large offline L2 envelopes did not fit the managed allocation. Synthetic successful workflows were not live results.

The Entra-v2 work verified tenant-specific production OIDC behavior offline. The initial custom issuer approval-claim requirement was subsequently replaced by an independently signed approval artifact, rather than weakening Entra trust. Neither this preparation nor schema assessment proves a paid authentication, endpoint, deployment or HTTP request failure. The actual early billable failures recovered below occurred after provider work. There is **no recovered evidence of an early paid 401/403, wrong-resource key rejection or strict-schema HTTP 400/422**. Those risks were investigated during preparation, not invented here as incidents. [Entra implementation][ENTRA]; [approval implementation][APPROVAL]; [strict compatibility assessment][STRICT].

The 16 October strict-schema compatibility preparation reported **zero calls**, because the four-call launcher could not lawfully satisfy a one-stage authorization. A governed single-analysis harness was needed. A separate signed 16–17 October launch subsequently failed **before provider inference**: no durable authorization event, live marker, consumption marker or financial reservation was found. Its exact invocation time and original exception were unavailable. Expiry of the practical launch cutoff was a reproducible possibility, not a confirmed cause. Its approval was unconsumed for the inspected packet. This is an additional failed launch, **not H04 or a twelfth paid evaluation**. [Preparation][PROBE]; [pre-provider diagnosis][NOINFERENCE].

Other zero-call preparations include the earlier Attempt 5 blocked handoffs, the 7 November v5 pricing stop, the v5 device-login session without a usable token, and the initial 11 November v10 expired/unverified application-token gate. Later authorization resolved some of these blockers in separate records. Their report titles must not override their zero-call contents. [Attempt 5 chronology][A5]; [v5 pricing stop][V5BLOCK]; [v5 financial readiness][FIN]; [v10 initial verification][V10BLOCK].

### 3.2 Actual evaluations

All named targets below are the historical Azure deployment **`epolymind-gpt-54-mini`**, model `gpt-5.4-mini`, version `2026-03-17`, GlobalStandard, Spain Central. Later management verification explicitly associates it with resource `epolymind-foundry-dev-susanta`. Early deployment context is established by [the postmortem][POST]; this is not a new cloud observation. Times are UTC; a missing time is NOT VERIFIED. Counts mean actual provider attempts / completed responses, not application acceptance.

| ID / historical experiment | Date and observed time UTC | Active generation | Authorization and goal | Provider attempts / completed | Successful application stages | Terminal category, checkpoint and approval disposition | Strongest available evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H01 / Azure Attempt 1, L1-1 | 15 October; exact time NOT VERIFIED here | `managed-prompt/1`, established by the diagnosis's version-2 correction | Approved four-call L1; one invocation, no retry/fallback | 1 / 1 | Extraction and plan; no accepted analysis | FAILED `extraction_limit_exceeded`, underlying `synthesis_limit_exceeded`; no chunk checkpoint. Consumption supported by later preserved historical markers; individual signed artifact not reopened | [First-failure reconstruction][A1], [postmortem][POST] |
| H02 / Azure Attempt 2, L1-2 | 15 October; exact call time NOT VERIFIED; prepared window 14:44:35–15:44:35 | `managed-prompt/2`; handoff generation `3da39a6b00a75a7f689a49e56a4dc3255576e0d16265a2d509f259f2d533e16f` | Separate four-call L1 packet; same no-retry intent | 1 / 0 completed-success responses (`output_limit`, known usage) | No accepted analysis | FAILED `governance_denied` masked original provider error. Historical consumption supported by later markers; individual artifact not reopened | [Attempt 2 handoff][A2], [output-limit correction][OUTPUT], [postmortem][POST] |
| H03 / Azure Attempt 3, L1-3 | 16 October; exact time NOT VERIFIED here | `managed-prompt/3`, JSON-object mode | Approved four-call L1; stopped after first response | 1 / 1 | Extraction and plan; no accepted analysis | FAILED `serialization_error` / NON_RETRYABLE. Historical CLI misleadingly returned exit 0. Consumed historical approval; no downstream continuation | [Original-response diagnosis][A3], [postmortem][POST] |
| H04 / Azure Attempt 4 | 19 October; time NOT VERIFIED | Strict `managed-prompt/3` context supported by subsequent audit; exact executed source hash NOT VERIFIED | Single governed analysis; not a complete four-call workflow | 1 / 1 strict response path | Provider completion; local acceptance failed | FAILED `serialization_error`, `accounting_failed=false`; exact predicate NOT VERIFIED. Historical consumed-marker sequence supports one use; original artifact not reopened | [Compatibility audit][AUDIT], [observability report][OBS], [Attempt 6 comparison][A6] |
| H05 / Azure Attempt 5 | 29 October; exact time NOT VERIFIED here | `managed-prompt/3`, strict schema | Separately authorized one-call analysis after earlier zero-call preparations | 1 / 1, `completed_strict_response`, `stop` | Provider completion only; rejected by domain validator | FAILED `serialization_error`; `claim_contract / subject_on_nonfact`. One settled row; approval consumed in historical sequence | [Post-execution diagnostic evidence][A5], [Attempt 6 reconciliation][A6] |
| H06 / Azure Attempt 6 | 1 November, call 14:27:20.597429–14:27:28.451192 | `managed-prompt/4`, `managed-generation/2`, `azure-strict/1`; executor `polymind-single-analysis/1` | Independently approved **one** analysis, 25,000/3,000 token maxima, zero retries | 1 / 1, strict completion, `stop` | Application accepted unchanged canonical first-chunk result, 3,907 bytes; exit 0 | SUCCEEDED at bounded goal; not full durable L1. One settlement, approval CONSUMED | [Closure primary-evidence inventory D1–D6][A6] |
| H07 / first November four-call L1 | 7 November, launcher 01:28:39; call approximately 01:28:52–01:29:02 | Post-G1 `managed-prompt/4`; generation `00bf895290e1da2fb81372ff1ea921d8d7f464ea14f41110f54313d0423ad904`; HEAD `f6555f3` | Separate RSA signing and explicit paid four-call authorization; EUR 5 ceiling | 1 / 1 | Plan only; chunk response rejected | FAILED `invalid_reference`, NON_RETRYABLE; `invalid_qualification_source`; no chunk checkpoint, CONSUMED | [Execution and settlement][NOV7], [original-output investigation][QUAL] |
| H08 / v5 second four-call evaluation | 9 November, launcher 00:30:37–00:32:03 | `managed-prompt/5`; generation `de9492c536c1435464e8d9e406cbd1491ea358bc45f817df72eb2ea2a0f69a71`; HEAD `2b8a5ac` | Fresh renewed exact packet; separate signing and paid approval, at most four calls, no retry/fallback | 2 / 2 | Chunk checkpoint accepted; first reducer rejected | FAILED `extraction_limit_exceeded`, domain `synthesis_limit_exceeded / response_limit`; no reducer checkpoint; CONSUMED | [Renewal report's subsequent execution section][V5LIVE], [sizing reconstruction][SIZE] |
| H09 / v7 four-call evaluation | 9 November, launcher 12:57:29.539785–12:59:53.492296 | `managed-prompt/7`; generation `8426ab5cfef3e4d1925c68a5f8558c5bafc487dd746f0f7ccda799c03be16c3a`; HEAD `6e0319e` | Exact independently signed and separately paid-authorized four-call packet | 3 / 3 | Chunk and first reducer checkpoints accepted | Root FAILED `invalid_child_link`, workflow `invalid_reference`, NON_RETRYABLE; no root checkpoint; CONSUMED | [Three-call record and independent reconstruction][V7LIVE] |
| H10 / v8 four-call evaluation | 9 November, launcher 20:30:01.760580–20:30:25.649469; call 20:30:14.114285 | `managed-prompt/8`; generation `93ca9066491c197987f919c5d185417bf4f3d2787384acf2833011e32641c0df`; v8 working-tree changes over HEAD `6e0319e` | Exact v8 packet, separate signing/paid decisions, at most four calls | 1 / 1 | Plan only; no accepted chunk | FAILED `foreign_evidence`, workflow `invalid_reference`, NON_RETRYABLE; CONSUMED | [Live audit reconciliation][V8LIVE], [v9 original-request reconstruction][V9] |
| H11 / v10 four-call evaluation | 11 November, launcher 21:00:01.805004–21:03:23.432854 | `managed-prompt/10`, `generation-inventory/2`; committed HEAD `ec22fa3`; exact hash in section 8 | Exact financial ceiling, separate independent RSA signature, then explicit paid-execution/consumption authorization | 4 / 4 | All three checkpoints; complete digest; active publication; grounded Q&A | COMPLETED, exit 0; technical execution successful, semantic review incomplete; CONSUMED exactly once | [Execution receipt/settlement reconciliation][V10], [independent signing verification][SIGN] |

**No additional v6 or v9 paid evaluation is established.** V6 was an offline sizing/replay generation and v9 an offline request-local source-schema generation. Azure Attempt 6 was v4, not v6. “Second v5 four-call evaluation” in the operator authorization refers to the second four-call evaluation after H07; it does not establish an unseen first paid v5 evaluation. The seven-settlement pre-H08 and nine-settlement post-H08 snapshots support that interpretation. H09 brought the total to twelve, H10 to thirteen, H11 to seventeen. [V5LIVE][V5LIVE], [V7LIVE][V7LIVE], [V8LIVE][V8LIVE], [V10][V10].

### 3.3 Additional recoverable early source fingerprints

These bind historical code, not model-produced claim identities. They complement the register rather than substituting current source for old execution:

| Evaluation | Generation source SHA-256 | Evidence qualification |
| --- | --- | --- |
| H03 | `2ff2aff8f575ed99b23108dd5d10c2f7a73a55fb6cc7e073107e0597124c7290` | Original-response diagnosis matched the retained packet [A3][A3] |
| H05 | `7d387a8595cf63e2ac944a25c4987a1b37392aa4adba8889914acf51ff9f0f59` | Historical supplied binding matched offline recomputation; terminal outcome and settlement were operator-observed supplied evidence, not privately reread in that diagnostic task [A5][A5] |
| H06 | `74cf9320b0ebf6d45df531e81827c5a8710b5b4d58fa75aad05dfa5039552290` | Closure directly recomputed source binding against retained final configuration; configuration SHA-256 `6d5a9cb4a190b3cf1195ccfe609e079aea499262ab0d54171d7572d132d80299` [A6][A6] |
| Offline v6, no paid evaluation | `f6e568d450ac084c5977e4fef68823fb457cceacd22b361f047310c5d3512f5b` | Frozen/checkpointed before v7 instruction change [V7][V7] |
| Offline v9, no paid evaluation | `f270aa81cbd5764d2b4739bf3ac3692653b1fe4c8ffbd67860e642137cb2579d` | Full inventory/1 frozen before v10 [IMPL][IMPL] |

## 4. Failure analysis and causal progression

### 4.1 Representation, output limits and errors: H01–H03

H01 returned 2,597 UTF-8 bytes. Application defaults expanded that representation by 874 bytes to 3,471 canonical ASCII JSON bytes, exceeding the 3,000-byte canonical limit. Extraction had succeeded; the historical `extraction_limit_exceeded` mapping obscured the actual analysis-normalization failure. The first correction required all schema properties/defaults in generation and explained the compact ASCII budget under v2. The later v3 change made provider-content, canonical-result and HTTP-envelope limits independent: 10,000 / 10,000 / 26,192 bytes in L1, while retaining 3,000 completion tokens. No content was truncated to force acceptance. [A1][A1], [independent limits][BYTES].

H02 exposed a separate observability/accounting defect: provider `output_limit` was replaced by a later `RunGuard.finish()` governance exception. `governance_denied` therefore does not prove genuine quota denial. The original trigger—response-byte overflow versus a completion/finish limit—cannot be reconstructed from 1,922 output tokens. The correction preserved the primary exception and separately recorded accounting failure, with bounded finish/byte/usage metadata. Unknown usage must block continuation, not be fabricated as zero. [Output-limit hardening][OUTPUT], [A6][A6].

H03 was valid JSON but not a valid closed application model: one malformed evidence UUID plus eight forbidden top-level fields, `unused1`–`unused8`. Neither canonical serialization nor domain provenance checking had been reached. Diagnostic removal of only the fields still failed; changing only the UUID still failed. The two-change counterfactual was an offline explanation, not accepted repair. Strict provider schema support was subsequently investigated. A separate CLI correction made unsuccessful terminal state produce a nonzero exit after audit/settlement; historical exit 0 did not imply success. [A3][A3], [regression reconciliation][REG].

### 4.2 Strict provider schema did not replace application acceptance: H04–H06

The exact Pydantic schema could not simply be sent as strict Azure schema: the supported subset excluded string `format`, length and pattern constraints. `llm/azure_schema.py` deliberately converts only an explicitly bounded subset, requiring closed objects/all properties and preserving supported nested structure. The two-layer design retained stricter local UUID, identity, evidence and lineage checks. This was a compatibility correction discovered offline, not a recovered live HTTP rejection. [Strict assessment][STRICT], [two-layer implementation][TWOLAYER].

H04 demonstrated strict completion followed by local `serialization_error`; the specific predicate remains unknown. Later typed diagnostics reduced this uncertainty for subsequent runs. A separately confirmed response/session cleanup defect could mask a primary exception and was fixed, but **is not a proven cause of H04**. [Observability][OBS], [cleanup correction][CLEANUP].

H05 then supplied a precise independent cause: a populated `subject` on a non-factual claim. The generation schema/instructions did not explicitly express the validator's fact-only populated-subject relationship. V4 instructed `subject=null` for `unknown`, `unsupported`, `commentary` and `structural`; facts could retain null or valid populated subjects. The validator was not weakened, and no claim was reclassified. H06's v4 response passed unchanged, but only in the one-call harness. Its success did not exercise reducers, durable complete-digest acceptance or Q&A. [Attempt 5 diagnostics][A5], [v4 implementation][SUBJECT], [Attempt 6 scope][A6].

### 4.3 G1: complete input sizing and admission

G1 concerns the full rendered request and output contribution, not just billed token counts or model context advertising. It must include instructions, schema, trusted controls, escaped source/child JSON, links, immutable references, structural paths and inherited metadata, plus reserved completion tokens. The 2 November hardening followed offline evidence that legal canonical children could produce oversized reducer envelopes. A 7,000-byte child-material allocation was made explicit for L1, with fixed-envelope planning and checks before inference and checkpoint acceptance. The managed input allocation was 24,800; with 100 overhead, 100 safety and 3,000 reserved output, the maximum conservative context reservation was 28,000. [G1/G2 engineering][GATES], commit `d940443`.

H08 exposed an overly conservative early child-admission quantity. Its reducer raw/canonical JSON was 4,783 bytes, both within 10,000, and its request input estimate was 16,007 plus 3,000 output, within context. But escaped result contribution 6,247 plus a fixed 1,024-byte wrapper gave 7,271, over the 7,000 child allowance by 271. Actual bounded wrapper cost was 620, producing **6,867**, which fit by 133. This was an intentional fail-closed v5 policy that overreserved this wrapper, not an escaping bug or exhausted model token window. [Original execution][V5LIVE], [measured reconciliation][SIZE].

V6 replaced that early fixed-wrapper test with a necessary result-contribution bound, followed by complete actual child-material admission using inherited metadata and a conservative maximum artifact-reference integer. Finalization/replay also enforced the complete child bound. The planner retained 7,000 per child and did not enlarge the budget. With v6 fixed envelope 9,973, two children reserved 23,973 before overhead; three would not fit. That correction addressed sizing only. It could not validate identities in the rejected historical response. [SIZE][SIZE], [v6 checkpoint][V6], commit `bdd7ab3`.

### 4.4 G2: evidence, identity and immediate-child lineage

G2 resolves original `EvidenceRef` spans against extraction and scope, validates the current result's deterministic claim IDs and origins, restricts direct source references to current authority, and requires complete valid immediate-child claim links. Inherited qualifications/conflicts persist through accepted lineage and application-owned summaries; merely seeing a UUID inside inherited material does not grant direct citation authority. Checkpoint compatibility binds the generation/planning profile and immutable parent graph. [Validator](../../documents/digestion/validation.py), [workflow](../../documents/digestion/workflow.py).

V6 replay of H08 admitted the corrected 6,867-byte contribution and then exposed **all eight new reducer claims using the child stage as `originating_stage`**. Their positional claim IDs were correct and current-stage-specific. The independent invariant was `claim.originating_stage == request.stage_id`: restating an inherited finding creates a new claim at the current stage. Child origins belong in lineage, not in the new claim's origin. The rejected result remained invalid, with `inference_contract_error / claim_identity / originating_stage_mismatch`. Source-origin/current-generation confusion is a supported interpretation, not proven model reasoning. [V6][V6].

V7 explicitly scoped result stage and every claim origin to `CONTROL.stage_id`, including restated findings. H09 then passed current-stage identities in all three responses and accepted its first two checkpoints. The root failed a different invariant: it used the immediate reducer's **stage ID paired with chunk/grandchild claim IDs**. All eight pairs were outside the supplied immediate-child set. Correct stage IDs and plausible prose did not authorize mixed pairs. Raw/canonical sizes, child bounds and request context all fit; this was not recurring G1 failure. [V7 instructions][V7], [H09 original-output review][V7LIVE].

V8 strengthened pair-copying and role separation, clarified direct-child versus descendant identity, and retained inherited evidence distinctions. Its offline structural-path boundary tests checked real escaped request sizes. H10 failed at the chunk, before live reducers could test the intended lineage correction. Offline lineage success must not be relabeled live reducer verification. [V8 engineering][V8], [structural boundary regressions][V8BOUND], [V8LIVE][V8LIVE].

### 4.5 Foreign evidence references: H07, H10 and v9

H07 had valid primary evidence but one unauthorized value at `claims[7].qualifications[0].evidence_ids[3]`. Three other qualification references and all 17 primary-reference occurrences were authorized. Original-input reconstruction matched the captured generation hash and independently resolved all four source pieces; the foreign value first appeared in retained provider content. Static schemas validated type/shape rather than request membership. The application correctly rejected before a chunk checkpoint. R0 added mixed/foreign/duplicate qualification regressions; R1's v5 instructions explicitly required complete unchanged IDs and stage-local qualification inheritance. Dynamic enums were deliberately deferred. [Original diagnosis][QUAL], [R0/R1][R01], commit `2b8a5ac`.

H10 showed that explicit copying instructions still did not guarantee compliant generation: the seventh claim's second primary reference, `claims[6].evidence_ids[1]`, was a well-shaped but foreign UUID. Its first four groups matched one authorized source and last group another. This observable relationship does not establish intent or identify the correct citation. All eight claim identities/origins passed; no qualifications were present. Having all four legitimate IDs elsewhere did not authorize a fifth. [V8LIVE][V8LIVE], [v9 reconstruction][V9].

Repairing either historical reference by nearest match, deleting it, or borrowing another stage's ID would invent the provider's intended evidentiary support and compromise the audit. The application must reject rather than manufacture provenance.

V9 introduced request-local membership enums for supporting, contradicting and qualification source references using the existing strict converter. A shared source definition bounded the strict inventory to 256 IDs, split into branches of at most 128. Empty direct-source authority needed an explicit empty-array-compatible policy rather than an invalid empty enum or expanded permission. Exact memberships and complete G1 were still checked locally. This was **OFFLINE VERIFIED**, not Azure acceptance of that exact schema or evidence of reliable model selection. The post-v9 review recognized the remaining burden of copying opaque global IDs and composing child pairs. [V9][V9], [post-v9 assessment][POSTV9].

## 5. Version-by-version engineering evolution matrix

Validation labels refer to the stated change and reach. Historical passing test counts are not reruns performed for this document.

| Version/attempt | Observed problem | Confirmed cause or bounded interpretation | Engineering change and location | Validation / committed evidence | Remaining limitation |
| --- | --- | --- | --- | --- | --- |
| Initial Phase 17H / preparation | Local success could be mistaken for real-model validation | Synthetic providers do not establish generation behavior | Reliability/quality harness and explicit L0/L1/L2 evidence boundaries | **OFFLINE VERIFIED**, [BASE][BASE], commit `af4a7a0` | Representative expert quality and real inference pending |
| Entra/approval preparation | Entra token does not carry arbitrary application approval claim | Authentication and exact execution consent are different authorities | Entra-v2 production verifier; independent RS256 approval, `security/identity.py`, `foundry_approval.py` | **OFFLINE VERIFIED**, [ENTRA][ENTRA], [APPROVAL][APPROVAL]; later live usage | No inference authorization from identity alone |
| v1 / H01 → v2 | Canonical default expansion exceeded limit | 2,597 raw → 3,471 canonical bytes | Require complete fields/defaults and explicit canonical budget in `managed.py` | Original-output replay; historical 195-test selection [A1][A1] | Prompt instructions cannot enforce byte arithmetic |
| v2 / H02 | Provider output error hidden | `RunGuard.finish()` replaced primary exception | Preserve original error; sanitized diagnostics and accounting-failure separation | **OFFLINE VERIFIED**, [OUTPUT][OUTPUT] | Exact H02 limit trigger unresolved |
| v3 byte limits / H03 | Byte/token coupling; schema-invalid JSON | Independent representations; JSON-object mode insufficient | Separate response/canonical/envelope limits, versioned rendering, stricter CLI terminal exit | Historical 310-test byte-limit selection, seven H03 regressions [BYTES][BYTES], [A3][A3] | UUID membership not guaranteed by structural schema |
| Strict v3 / H04 | Provider schema incompatibility risk; local rejection after completion | Unsupported string constraints confirmed offline; H04 predicate unknown | Explicit `azure-strict/1` converter and two-layer validation | **OFFLINE VERIFIED** converter; **LIVE VERIFIED** strict completion [TWOLAYER][TWOLAYER], [A6][A6] | No attribution of H04 to a particular domain rule |
| Diagnostic/cleanup hardening | Coarse failure taxonomy and exception masking risks | Missing reason detail; independent cleanup masking defect | Closed typed diagnostics; bounded metadata; preserve primary failure across HTTP cleanup | **OFFLINE VERIFIED**, 1,631-test observability / 1,755-test cleanup regressions [OBS][OBS], [CLEANUP][CLEANUP] | Historical missing data cannot be recovered retroactively |
| v3 H05 → v4 H06 | Non-fact populated subject rejected | Instruction/domain contract gap | Explicit fact-only subject paragraph, unchanged validator | 35-case subject matrix; **LIVE VERIFIED** one unchanged accepted response [SUBJECT][SUBJECT], [A6][A6] | No complete L1 or human semantic claim |
| Post-G1 v4 | Valid child results could overflow fully rendered request | Missing planning/output relationship | Fixed-envelope planning, 7,000-byte child policy, complete request admission, strict two-chunk workflow | **OFFLINE VERIFIED**, 355 distinct selected cases; `d940443`, `b15713e` compatibility reconciliation [GATES][GATES], [CI][CI] | Generated content can still exceed child allocation |
| Post-G1 v4 H07 → v5 | Mixed unauthorized qualification source | Returned foreign ID; static schema lacks request membership | R0 mixed-reference regression, R1 complete-ID/stage-local inheritance guidance | **OFFLINE VERIFIED**, historical 1,872-test regression, `2b8a5ac` [R01][R01] | Guidance alone does not prevent foreign IDs |
| v5 financial preparation | Catalog and November billing conversion differed | Approximately 2.01535% projected token difference | Separately authorized prospective catalog migration; VAT/network assumptions, no repricing | **VERIFIED administrative reconciliation**, [CAT][CAT], [FIN][FIN]; not a model-generation test | Allowances are not final invoice charges |
| v5 H08 → v6 | 7,271-byte conservative child rejection | Fixed wrapper 1,024 exceeded measured bounded 620 | Centralize complete actual child admission, replay/finalization checks, retained 7,000 limit | **OFFLINE VERIFIED** replay and boundary/workflow tests; `bdd7ab3` [SIZE][SIZE] | Replay exposes independent wrong origins; no v6 paid run |
| v6 → v7 H09 | Child-stage origins in all eight reducer claims | Wrong origin invariant; interpretive ambiguity plausible | Explicit current CONTROL stage and lineage-only source-stage instruction | **OFFLINE VERIFIED** identity/workflow regressions; `6e0319e`; **LIVE VERIFIED** current origins in H09 [V7][V7], [V7LIVE][V7LIVE] | Root pairs still mixed child stage and grandchild IDs |
| v7 H09 → v8 H10 | Root immediate-child lineage invalid | Eight foreign (stage, claim) pairs | Stronger atomic-pair guidance/role separation; path-boundary sizing regressions | **OFFLINE VERIFIED** lineage and sizing; retained in `ec22fa3` [V8][V8], [V8BOUND][V8BOUND] | H10 never reached reducers; live lineage change untested then |
| v8 H10 → v9 | Foreign primary evidence ID despite copying guidance | Static provider schema allowed arbitrary strings | Request-local source enums for all source-bearing positions, bounded schema growth | **OFFLINE VERIFIED**, frozen v8/v9 schemas/sources; retained in `ec22fa3` [V9][V9] | Exact v9 schema not evaluated live; canonical IDs/pair copying remain model duties |
| v9 → v10 | Repeated global-ID and pair-construction risk | Failures show avoidable identity reproduction burden; recurrence frequency unknown | `wire.py`, `receipts.py`, managed renderer/handler, workflow; deterministic constructor and atomic manifests | **OFFLINE VERIFIED** contract/decoder/crash/reuse tests; `ec22fa3`; **LIVE VERIFIED** H11 [WIRE][WIRE], [V10][V10] | Authorized selections do not prove prose entailment |
| Post-H11 local reporting fix | Historical `billable_calls=3` despite four actual calls | Snapshot preceded Q&A; `calls` refreshed afterward | One-line refresh in `foundry_preflight.py`, four regression lines | User-reported **3 passed in 5.43s**; uncommitted at documentation start | Historical result unchanged; current source differs from executed fingerprint |

Frozen contracts under [tests/fixtures/digestion_contracts](../../tests/fixtures/digestion_contracts/README.md) preserve v3, pre-G1 v4, later G1 distinctions, v5–v9 renderers and v10 inventory/transport expectations. `managed_prompt9_inventory.json` and `v9_sources/` freeze the entire 15-file inventory before the 25-file v10 transition. Historical tests use pinned snapshots explicitly; production does not load old renderers. Source-compatibility tests were reconciled for intentional G1 changes rather than silently regenerating historical fingerprints. These controls let later hardening coexist with readable old artifacts.

## 6. Authentication, signing and financial-governance evolution

Microsoft Entra device-code authentication acquired a delegated application access token for the operator. Production OIDC verification checked signature/JWKS, tenant-specific issuer, scalar API audience, lifetime, `access_as_user` and exact `PolyMind.L1Operator` role. Local Operator Principal registration and enabled status were independent checks. The mapped permission `PUBLICATION_MANAGE` allowed the publication-management workflow; existing source ownership/scope and revocation remained authoritative. Later preparation also correlated the token's signed account identifier with the enabled Graph account. Earlier Graph-only enabled-account observations did not establish that join. [ENTRA][ENTRA], [V5BLOCK][V5BLOCK], [SIGN][SIGN].

The **Entra application credential** authenticated/authorized the operator to PolyMind; the **provider credential** authenticated the Azure inference request. A valid Graph/management token, configured endpoint or nonempty key cannot substitute for a correctly authorized inference credential. Earlier controlled evaluations securely obtained the named resource's key in memory. V10 ultimately used the operator-authorized existing `.env` API-key loading path, supplied to the launcher's protected runtime environment. The `.env` endpoint differed from a draft hostname but passed the named-resource allowlist; exact URL inequality was not proof of wrong resource. No new key retrieval was used for the final v10 launch. This history describes the already recorded controls, not credential contents. [v10 continuation][V10CONT], [V10][V10].

Independent **RSA-3072 / RS256** signing bound a reviewed immutable canonical configuration and its exact generation/executor, deployment, principal/scope, financial, timing, trust and policy bindings. The independently provisioned public trust was separate from the model key and Entra token. Signing did not consume approval. Persistent, fsynced one-use approval records outside replaceable audit directories prevented restarting with the same approval, new signature or audit-directory substitution. Partial setup after consumption did not automatically restore authority. [APPROVAL][APPROVAL], [operator procedure](phase_17hl_operator_approval.md).

Three decisions were deliberately independent: accepting financial exposure, authorizing private-key signing for exact bindings, and authorizing paid execution plus consumption. A financial ceiling is neither a signature nor permission to make a call. A valid signature proves exact consent bindings, not that the operator has authorized its present consumption. Expired identity or changed source/configuration requires renewed preparation, not reuse of historical receipts. The v10 signing report explicitly ended with paid authorization still required; the execution report records the later separate decision. [SIGN][SIGN], [V10][V10].

Shared admission protected a 30,000 TPM/30 RPM deployment allocation while preserving interactive reserve. The controlled background workflow used one concurrent call, at least 61 seconds between starts, a bounded four-call guard and no automatic retry/fallback. Local admission does not exclude remote consumers; management observations and explicit operator exclusivity attestations covered different evidence needs. The reusable `polymind-evaluation/1` policy was explicitly activated on 16 October with 16 daily requests, 500,000 daily tokens, 1,500,000 monthly tokens, unchanged EUR 5 monthly ceiling and 112,000 outstanding-token capacity. Historical reservations were preserved rather than resetting quota pools. [Policy activation][POLICY], [V7LIVE][V7LIVE].

Read-only preparation used queries and integrity checks without authority constructors/authorization methods that could write audit events. Catalog/policy migrations, signing, approval consumption and live settlement were separately authorized operational mutations. Successful execution legitimately appended security/governance/admission records; immutable historical rows and sealed artifacts could remain unchanged without entire active database files remaining byte-identical. No such operational mutation was performed for this history.

## 7. Financial and token-usage reconstruction

The following are **historical settled catalog token costs**, not retrospective repricing or invoice totals. H01–H06 use `phase17hl-pricing-eur-202610/1`, H07 also retained October catalog, H08–H11 use `phase17hl-pricing-eur-202611/1`. November migration applied prospectively. Reasoning tokens reported as part of completion/output must not be charged twice. Where original private rows are unavailable here, “verified” refers to the cited historical reconciliation, not a fresh ledger read.

| Evaluation | Calls | Actual input | Actual output | Settled catalog token cost EUR | Financial evidence / state |
| --- | ---: | ---: | ---: | ---: | --- |
| H01, 15 October | 1 | 1,845 | 1,460 | 0.00699907602956752 | SETTLED, [POST][POST] |
| H02, 15 October | 1 | 1,955 | 1,922 | 0.00890113516367529 | SETTLED despite failed provider outcome, [POST][POST] |
| H03, 16 October | 1 | 1,994 | 932 | 0.005006599788807204 | SETTLED, [POST][POST] |
| H04, 19 October | 1 | NOT VERIFIED | NOT VERIFIED | NOT VERIFIED | `accounting_failed=false`; later history includes settled row, exact row unavailable [A6][A6] |
| H05, 29 October | 1 | 2,342 | 1,852 | 0.008879355860613052 | SETTLED; 320 reasoning tokens included in output [A5][A5] |
| H06, 1 November | 1 | 2,476 | 1,814 | 0.008817317845829546 | SETTLED; 400 reasoning tokens included in output [A6][A6] |
| H07, 7 November | 1 | 2,506 | 2,130 | 0.010088437170011206 | SETTLED under October catalog [NOV7][NOV7] |
| H08, 9 November v5 | 2 | 6,836 | 3,920 | 0.020438080703811248 | Two SETTLED rows [V5LIVE][V5LIVE] |
| H09, 9 November v7 | 3 | 11,131 | 5,211 | 0.028545042416639792 | Three SETTLED rows [V7LIVE][V7LIVE] |
| H10, 9 November v8 | 1 | 2,749 | 1,609 | 0.008350688989635328 | One SETTLED row [V8LIVE][V8LIVE] |
| H11, 11 November v10 | 4 | 5,854 | 1,675 | 0.010707841465063252 | Four SETTLED rows [V10][V10] |

Verified-amount subtotal **excluding H04**: 39,688 input + 22,525 output = 62,213 tokens; **EUR 0.116733575433653438**. This is not total all-attempt spend. The first-three subtotal is 10,108 tokens and EUR 0.020906810982050014, matching the original postmortem. No missing value is treated as zero. All 17 reservations were reported settled after H11, with zero outstanding; the missing H04 amount prevents a complete independently reconstructed cost total from this table.

The November catalog input/output rates were EUR 0.673279770188 / 4.039678621124 per million, rounded upward to 12 decimals from resource-specific EUR/USD conversion evidence. The approved four-call token maximum was EUR 0.115804120472288. A 23% token VAT budgeting allowance and EUR 0.10 VAT-inclusive network contingency produced rounded aggregate extras EUR 0.126634947709, and forecast EUR 0.242439068181288. V10's configuration ceiling rounded upward to **EUR 0.242439068182**. [Migration][CAT], [financial assumptions][FIN].

For H11, actual token cost + **all approved extras** = `0.010707841465063252 + 0.126634947709` = **EUR 0.137342789174063252**. This conservative comparison fits the ceiling but does not measure actual tax/network charges. Monthly governance headroom is a local accounting balance, not an Azure hard spending cap or new run permission.

Actual Azure Consumption/Cost Management observations are separate: H07's November quantities matched 2,506/2,130 tokens, but EUR conversion gave approximately EUR 0.01029175456708111, versus settled October-catalog EUR 0.010088437170011206. The recorded difference EUR 0.000203317397069904 motivated prospective migration without rewriting the old row. H06's resource/day ActualCost was EUR 0.00899501772970062, distinct from its pinned-catalog settlement. Subscription-wide unrelated infrastructure cost cannot be attributed to these calls. These delayed observations are not final invoices or a VAT ruling. [Pricing investigation][V5BLOCK].

## 8. Successful v10 case study: 11 November 2026

### 8.1 Exact committed source and approved packet

The [execution record][V10] and [independent signature report][SIGN] agree on:

| Binding | Recorded executed value |
| --- | --- |
| Committed HEAD | `ec22fa3d116696b80a1bb12ad17e2eb37db38cb3` |
| Generation / inventory | `managed-prompt/10` / `generation-inventory/2`, 25 source files |
| Generation SHA-256 | `e5fb249cc9b166b5e438f1534eb855fa5ab7531e08aa09314c110a1905327ebd` |
| Canonical configuration SHA-256 | `8e0be5429ea1e8c991338508c8b56731aa7a4ceec2ae662502236ef81c7d1e5b` |
| Unsigned bindings SHA-256 | `e7aef1e7a0b272939b9b72bbe9e65bf25d542c67ff10084a1d339240957a2b3f` |
| Saved signed artifact SHA-256 | `c98ef7dfa7e5c35319f874c761647672dbc3721eedf5a54ee7b6b7571603e87d` |
| Deployment / model / region | `epolymind-gpt-54-mini` / `gpt-5.4-mini`, `2026-03-17` / Spain Central |
| Source PDF SHA-256 | `1be99e19a56040fb55c74682a19f874d4d4573f18d9f52a9a7ae19c8158ea92d` |
| Extraction SHA-256 | `b7410e987c6658c596399d4bccce4b6e11ec07cc95f29ab1c56eb2b7f011fcd1` |
| Plan SHA-256 | `4390d9e59a4e626507673e5eec281538c50e9bfff33d8471cf1816f3cbc0fabf` |
| Maximum calls / input / output | 4 / 100,000 / 12,000; one active call, no retries or fallback |
| Approved maximum exposure | EUR 0.242439068182 |

The source fingerprint is the same bounded `phase17h-pdf/1`, seed 1708, four-page fixture used earlier; plans changed with generation/profile bindings. Successful CI with 2,595 tests on the committed SHA and focused offline preparation are historical supporting evidence, not the live result and not tests rerun for this history. [v10 readiness][V10READY].

Financial approval preceded the signing decision. Fresh actual-Principal/source/policy checks passed before key access and after the masked passphrase dialog. Exactly one RSA-3072/RS256 signature was made at 20:49:21; a separate process independently verified the saved artifact at 20:49:35 with production verification and independent trust. The signing report explicitly left paid execution unauthorized. The later operator decision authorized this exact paid evaluation and one-use consumption. [SIGN][SIGN], [V10][V10].

The execution window began 20:30, targeted 21:00, required launch strictly before 21:04:59, and ended evaluation at 21:30. Approval/provider-use/exclusivity ended 21:50, application token expiry 21:52:02. Final management/quota/consumer/meter refresh passed at 20:56:13 and actual production checks repeated before invocation. No retry, schema probe or alternate executor was added.

### 8.2 Application-owned generation and evidence construction

V10 preserved the provider-neutral boundary: application managed inference → `InferenceProvider`/structured request → existing OpenAI-compatible adapter → external Azure service. Azure subset conversion stayed in provider infrastructure. LangGraph/RAG/UI did not acquire model-specific identifier workarounds.

The provider emitted `stage-proposal/1`, with text, semantic fields, source selections and child selections. Application tables mapped **`E1..En`** to sorted authorized source IDs, and **`C1..Cm`** to complete immediate-child `(stage_id, claim_id)` pairs in immutable plan-child/claim order. Separate pair components were no longer model choices. The canonical constructor assigned current stage and origins and `stable_id(str(request.stage_id), str(position))`, preserving response order. It neither inferred missing support nor repaired invalid selections. [Wire/receipt decision][WIRE], [implementation][IMPL], [wire source](../../documents/digestion/wire.py).

A singleton request-binding digest committed the exact StageRequest and mapping tables. It detected transplantation across requests but was not a credential or independent proof of origin. The immutable application-created provider record bound actual returned raw bytes to request/table/generation hashes, plan, job/step and original attempt/fence. The decoding receipt bound that raw record to the constructed canonical checkpoint. The existing fenced ledger atomically committed the ordered **checkpoint, receipt, raw record** manifest with step success and dependent outbox activation. Mere object presence or a valid-looking receipt could not authorize a checkpoint. [Receipts source](../../documents/digestion/receipts.py), [workflow source](../../documents/digestion/workflow.py).

On reopening, production verification reconstructed exact requests/tables from immutable accepted parents, checked raw and canonical hashes and receipt associations, decoded deterministically and reran G2, inherited-summary/parent checks and complete G1. Multi-hop reuse followed ledger-owned original acceptance edges rather than assigning new evidence to old responses. Interrupted uncommitted objects remained orphans; no paid replay or automatic adoption was allowed. Application-owned canonical identity reduced copying risk; the model still had to choose genuinely supporting authorized keys and provide useful prose.

### 8.3 Actual sequential calls and settlements

The launcher started **21:00:01.805004** and finished **21:03:23.432854**, exit **0**, with L1 COMPLETED and Q&A COMPLETE. [V10][V10] reconciles provider captures, run records and exact Decimal settlements:

| Call | Start UTC | Stage | Input | Output | Catalog token cost EUR |
| --- | --- | --- | ---: | ---: | ---: |
| 1 | 21:00:15.462216 | Chunk | 1,571 | 485 | 0.003016966650210488 |
| 2 | 21:01:16.602364 | Structural reducer | 1,538 | 789 | 0.00422281071861598 |
| 3 | 21:02:17.728016 | Root reducer | 1,221 | 317 | 0.002102652722295856 |
| 4 | 21:03:19.565600 | Grounded Q&A | 1,524 | 84 | 0.001365411373940928 |
| Total | | | **5,854** | **1,675** | **0.010707841465063252** |

Start gaps were **61.140148**, **61.125652** and **61.837584 seconds**. Each previous call finished before the next began; observed concurrency was one. There were zero retries, fallback calls, extra probes or second launcher invocations. Three digestion requests exercised the strict wire schemas; Q&A retained its separate JSON-object contract. All four new reservations were SETTLED. Thirteen historical rows were unchanged; seventeen total settlements, zero outstanding, zero active admissions and no unresolved/stopped call remained. One new consumed marker was added while ten historical markers retained their bytes.

### 8.4 Durable checkpoint, publication and citation evidence

A network-forbidden independent reopening checked scoped immutable hashes and SQLite read-only state. The five job steps succeeded once: plan, chunk, structural reducer, root reducer and final digest. Three managed stages each committed three associated objects, so **all nine managed manifest objects** were accepted. The reported canonical claim counts were 4 / 2 / 2. Complete input/context estimates were 7,685/10,685; 7,549/10,549; and 6,766/9,766. Accepted manifests retained original attempt/fence 1/1. Production `_verify_proposals()` verified associations and deterministically reconstructed canonical outputs without identity substitution. [V10][V10].

The complete digest matched independent `make_digest()` reconstruction and had coverage fraction **1**. That is implemented source-span coverage, not a semantic recall score. The accepted active publication contained one approved document and four ORIGINAL/SOURCE_TEXT records resolving exact extraction text. The pinned local MiniLM embedding tree and isolated audit-local Chroma store served publication/retrieval; no cloud embedding call or replacement model download was needed.

Grounded Q&A completed with one citation passing document/version/extraction, physical-page, offset and exact-excerpt checks. The tested first-page valve-inspection answer matched the expected identifier and pre-operation instruction. Publication success is established by the accepted manifest and resolved records, not by vector-store initialization. The audit was sealed; reconciliation did not reactivate publication, consume another approval or make another provider call. [V10][V10].

### 8.5 What the result establishes

For this fixture, exact source and configuration, v10 demonstrated live acceptance of the actual credential and three strict digestion schemas; all three durable managed stages; application-owned identity/provenance construction; complete G1/G2 reopening; digest/publication/retrieval/Q&A composition; sequential admission; single-use consent; and known-usage settlement. It did not establish arbitrary document reliability, crash-free completion in all circumstances, broad contradiction/qualification performance, expert semantic quality, multi-host production behavior or general production readiness.

## 9. Semantic-quality findings and post-evaluation reporting defect

The recorded separate source/content comparison matched **4/4 leaf unit/valve lists and 19/19 valve identifiers** against original pages. Chunk content and the one tested grounded Q&A answer were source-grounded in those checks. However, the retained formal review fields still showed **0/1 human-reviewed responses**, with factual-support annotations and independent-reviewer judgments null. These deterministic/preliminary checks must not be represented as completed independent human semantic acceptance. [V10][V10].

The structural/root prose concentrated on child-wrapper counts and opaque `C1–C4`/`E3` labels instead of a useful standalone domain synthesis. Local aliases appearing in prose are not canonical citations and can be misleading across requests. G2 can establish that selected references are authorized and structurally connected; it cannot prove that the text entails the source, preserves important caveats or selects the most useful domain content. Therefore successful provenance is necessary but insufficient for summary quality. Broad semantic claims from a single small fixture are unjustified.

A separate informational defect affected the original successful `result.json`: **`billable_calls: 3`**, despite four actual calls. `calls` was refreshed after Q&A; `billable_calls` had been snapshotted before Q&A. Four provider captures, four durable run records and four new settled rows establish the actual count. The discrepancy did not reduce the call guard or erase accounting. [Original discrepancy record][V10].

After that evaluation, the user made a targeted **uncommitted** correction: one line refreshed `billable_calls` after Q&A in [foundry_preflight.py](../../tests/performance/foundry_preflight.py), and four lines in [test_foundry_l1_launcher.py](../../tests/integration/test_foundry_l1_launcher.py) asserted returned and saved counters equal four. The supplied targeted result was **3 passed in 5.43s**. This task inspected and preserved both modifications exactly; it did not rerun tests or claim the fix was present during the successful evaluation. The historical result/report remains immutable. Because the composition is fingerprinted, current working-tree bytes must not be presented as the exact executed v10 generation snapshot.

## 10. Engineering lessons tied to the observed record

1. **Strict JSON schema is one gate.** H03 needed structural enforcement; H05 still failed a kind/subject relationship, H07/H10 source membership and H09 child lineage. Each required an independent application predicate.
2. **Assign canonical identities in the application.** H08's later origin rejection and H09's mixed lineage pairs show why model reproduction of UUID roles was fragile. V10 eliminated model-generated canonical IDs and made pair selection atomic, while retaining semantic selection duties.
3. **Keep source provenance distinct from immediate-child lineage.** A root may inherit original source support through a reducer without directly linking chunk claim IDs as if they were that reducer's claims. Qualification-only inherited sources do not automatically become current direct authority.
4. **Count paid failure honestly.** A provider can return and settle successfully while its result fails before any accepted checkpoint. H07/H10 had no accepted chunk; H08/H09 had only partial accepted graphs.
5. **Budget end to end.** H01's defaults, later escaped reducer envelopes and H08's wrapper overreservation concern different representations. Raw bytes, canonical bytes, child contribution, complete request estimate and completion tokens need separate boundary tests.
6. **Bind consent to immutable exact bytes.** Changes to prompt, validator, decoder, inventory or launcher can change effective behavior. Independent signatures, one-use markers and fresh configuration hashes prevent old approvals from covering new generations.
7. **Stop after terminal failure.** H08's remaining root/Q&A and H09's Q&A did not run. Unused call allowance did not authorize repair, fallback, or replay of a consumed signature.
8. **Prefer settlements over stale informational counters.** H11's `billable_calls=3` was contradicted by four captures/run records/settlements. Preserving the defect and documenting the later fix protects historical credibility.
9. **Accepted checkpoints are not proof of usefulness.** V10 proved its structural chain while reducer prose remained unsatisfactory. Quality acceptance needs source-based judgments and domain synthesis criteria in addition to membership.
10. **Freeze historical generations.** Pinning v3–v9 snapshots and v10 inventory allows later improvements without rewriting the evidence that produced past outcomes. A later corrected validator/prompt must not retroactively turn rejected output into an accepted historical stage.

## 11. Remaining work, evidence gaps and closure criteria

A future **separately scoped, versioned reducer-quality improvement** should require structural/root outputs to synthesize domain facts, obligations, exceptions and cross-page relationships, with processing metadata kept out of substantive summaries unless requested. It should discourage opaque alias prose and preserve qualifications, contradictions and original-source attribution. This report implements none of that work and schedules or requests no paid inference.

Changing reducer instructions changes generation behavior and must not silently mutate the successfully evaluated `managed-prompt/10` fingerprint. Use a new reviewed generation identity, freeze the successful v10 contract and maintain explicit checkpoint/configuration incompatibility. The post-evaluation reporting correction likewise cannot be substituted into the historical fingerprint without acknowledgement.

Appropriate future regressions include grounded reducer synthesis on multiple domain fixtures; absence of alias/processing-metadata dominance; explicit retention of qualifications, contradictions and uncertainty; semantic-support and omission judgments; exact source citations; multi-hop immediate-child lineage; wrong/foreign key rejection; request-binding/receipt corruption; crash/orphan/fence/reuse controls; Unicode/escaped input and child/output boundaries; and final Q&A/call-counter accounting. Offline tests demonstrate mechanisms, not new live model quality. Any eventual live validation would require a separate task and authorization.

Formal closure should reconcile the accepted technical run with independent human source/claim/citation review, resolve reducer-quality acceptance against a defined rubric, establish representative document coverage and reliability limits, and explicitly assess outstanding performance/L2/operational gates in [Phase 17H readiness](phase_17h_readiness.md). A bounded L1 success is insufficient to inherit all those gates.

Six unresolved evidence-gap groups remain in this reconstruction:

| Gap | Exact missing or incomplete evidence | Consequence |
| --- | --- | --- |
| G-A | H02's original output-limit subtype/finish metadata | Error masking confirmed; byte overflow versus truncation remains unknown |
| G-B | H04 exact rejecting predicate and actual usage/cost row | No invented diagnosis, zero cost or complete spend total |
| G-C | Exact early invocation times and some executed generation/configuration/signature bindings | Early template mapping is supported, but full packet-level reproduction is incomplete; H04 exact hash especially unverified |
| G-D | Original 16–17 October no-inference launch exception/invocation time | Pre-provider boundary confirmed; expiry remains conditional |
| G-E | Unavailable original private receipt inventories in this workspace | This history relies on identified sanitized original-artifact reconciliations rather than a fresh private audit |
| G-F | Independent completed human semantic judgments and representative quality evidence | Preliminary grounded findings cannot establish broad quality or formal phase closure |

Model-internal reasoning and final invoice treatment are additional explicit limits, not evidence that these missing facts were measured. No current authentication, approval or replay authority is implied by any historical deadline or hash.

## 12. Evidence index and audit navigation

Links below are repository-relative. The most direct available execution and reconstruction reports are preferred over intention-only prompts. Most early reports preserve symbolic private locations. None of the historical handoff commands or expired approvals should be executed.

| Evidence family | Claims supported / original records identified |
| --- | --- |
| [Original Phase 17H report][BASE], [preflight chronology][PRE] | Earliest local scope, L0/L1/L2, deployment/authentication/configuration risks and zero-call preparation |
| [Three-attempt postmortem][POST], [H01 diagnosis][A1], [H03 diagnosis][A3] | Actual first three failures, original response reconstruction, exact token/cost subtotal and no accepted chunks |
| [Attempt 2 handoff][A2], [output-limit correction][OUTPUT], [independent byte limits][BYTES] | v2 mapping, masking mechanism, v3 version/limit separation; not new live outcomes |
| [Strict assessment][STRICT], [two-layer implementation][TWOLAYER], [strict live preparation][PROBE] | Unsupported schema subset risk, converter responsibility, zero-call one-stage preparation |
| [No-inference diagnosis][NOINFERENCE] | Empty audit/security/admission/replay boundary and conditional cutoff explanation |
| [Compatibility audit][AUDIT], [observability][OBS], [cleanup][CLEANUP] | H04 rejection boundary; typed diagnostics and independently identified cleanup masking; no fabricated H04 predicate |
| [Attempt 5 diagnostics][A5], [v4 subject implementation][SUBJECT] | Later terminal outcome superseding earlier no-call handoffs; fact-only subject rule |
| [Attempt 6 closure][A6] | Primary D1 final refreshed configuration; D2 immutable `outcome.json`; D3 financial row; D4 run interval; D5/D6 consumption/live-start records. Includes six-attempt chronology and scope distinction |
| [G1/G2 hardening][GATES], [CI reconciliation][CI] | Child-budget planning, strict two-chunk integration, frozen compatibility reconciliation |
| [7 November execution][NOV7], [qualification investigation][QUAL], [R0/R1][R01] | H07 exact paid attempt, original-output membership failure and v5 corrective instructions/regressions |
| [v5 pricing stop][V5BLOCK], [catalog migration][CAT], [financial readiness][FIN] | ActualCost versus pinned catalog; authorized prospective migration, VAT/network assumptions and blocked login preparation |
| [v5 renewal/execution][V5LIVE], [sizing reconciliation][SIZE], [v6 investigation][V6] | H08 two calls; `controlled-execution-review.json`, disposition and 87-file private inventory; actual wrapper sizes and subsequently exposed stage-origin failure |
| [v7 engineering][V7], [v7 execution][V7LIVE], [v8 engineering][V8], [path boundaries][V8BOUND] | H09 three provider calls, two checkpoints, exact root pair mismatch; offline lineage/sizing response |
| [v8 execution][V8LIVE], [v9 reconstruction/implementation][V9] | H10 one-call source rejection; 14-file sealed audit, actual request/response hashes, schema-local membership evolution |
| [Post-v9 ADR][POSTV9], [v10 receipt ADR][WIRE], [v10 implementation][IMPL] | Responsibility redesign, deterministic decoder, manifest association, fail-closed recovery and generation inventory transition |
| [v10 readiness][V10READY], [initial verification][V10BLOCK], [continuation][V10CONT] | Committed source/CI/offline support, expired application authentication stop, later secure existing-key supply mechanics |
| [v10 independent signing][SIGN], [v10 execution/reconciliation][V10] | Exact signature/configuration/generation, later paid decision, four-call execution/settlement and checkpoint reconstruction |
| [V10 private evidence inventory described in the execution report][V10] | `live-execution.receipt.json`, `final-prelaunch-verification.json`, `v10-post-execution-review.json`, `v10-preliminary-semantic-observations.json`, `v10-controlled-execution-audit-inventory.json`, `post-execution-preservation.json`; 32 sealed `four-call-audit` files including unchanged human-review packet. Identified, not freshly opened here |
| [Fixture conventions](../../tests/fixtures/digestion_contracts/README.md), [v10 contract test](../../tests/integration/test_managed_prompt10_contract.py), [wire integration tests](../../tests/integration/test_generation_wire_v10.py) | Frozen generation/source/HTTP expectations; invalid-stage cancellation/settlement, crash windows, corrupt association denial, fenced/idempotent commit and repeated reuse |
| [Managed inference](../../documents/digestion/managed.py), [wire decoder](../../documents/digestion/wire.py), [receipt verification](../../documents/digestion/receipts.py), [G2 validation](../../documents/digestion/validation.py), [sizing](../../documents/digestion/sizing.py), [workflow](../../documents/digestion/workflow.py) | Current implementation cross-check; use historical snapshots/commits for earlier behavior |
| [Provider converter](../../llm/azure_schema.py), [OIDC verifier](../../security/identity.py), [authority](../../security/authority.py), [governed execution](../../governance/execution.py), [ledger](../../governance/ledger.py), [approval](../../tests/performance/foundry_approval.py) | Provider-neutral boundaries, security registration/authorization, accounting and one-use binding mechanics |

Git anchors inspected: `af4a7a0` (initial reliability/evaluation), `4ee06b6` (managed/governed hardening), `f2a60fa` (Attempt 6 evidence), `d940443` (G1/G2), `b15713e` (historical compatibility), `2b8a5ac` (v5 provenance guidance), `bdd7ab3` (v6 sizing), `6e0319e` (v7 identities), `ec22fa3` (v8–v10). Earlier uncommitted live states must be reconstructed from their bound hashes/snapshots, not inferred solely from these later commit dates.

[BASE]: ../codex/reports/phase_17h_report.md
[PRE]: ../codex/reports/phase_17h_live_preflight.md
[POST]: ../engineering/postmortems/Estudio_PolyMind_Phase17HL_L1_Three_Attempts_Postmortem_2026-10-16.md
[A1]: ../codex/reports/phase_17hl_first_failure_diagnosis.md
[A2]: ../codex/reports/phase_17hl_same_day_attempt2_handoff.md
[A3]: ../codex/reports/phase_17hl_l1_attempt3_serialization_root_cause.md
[A5]: ../codex/reports/phase_17hl_attempt5_post_execution_diagnostics.md
[A6]: ../codex/reports/phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md
[OUTPUT]: ../codex/reports/phase_17hl_output_limit_hardening.md
[BYTES]: ../codex/reports/phase_17hl_independent_json_byte_limits.md
[REG]: ../codex/reports/phase_17hl_regression_reconciliation.md
[STRICT]: ../codex/reports/phase_17hl_structured_output_compatibility.md
[TWOLAYER]: ../codex/reports/phase_17hl_two_layer_structured_output.md
[PROBE]: ../codex/reports/phase_17hl_azure_strict_schema_live_compatibility.md
[NOINFERENCE]: ../codex/reports/phase_17hl_single_call_execution_failure_diagnosis.md
[AUDIT]: ../codex/reports/phase_17hl_final_offline_azure_compatibility_audit.md
[OBS]: ../codex/reports/phase_17hl_live_failure_observability_and_contract_options.md
[CLEANUP]: ../codex/reports/phase_17hl_f1_http_cleanup_failure_preservation.md
[SUBJECT]: ../codex/reports/phase_17hl_managed_prompt4_subject_contract_implementation.md
[GATES]: ../codex/reports/phase_17h_g1_g2_offline_engineering_and_integration_hardening.md
[CI]: ../codex/reports/phase_17h_ci_failure_and_historical_contract_reconciliation.md
[NOV7]: ../codex/reports/phase_17h_final_approval_signing_and_controlled_execution.md
[QUAL]: ../codex/reports/phase_17h_live_invalid_qualification_source_root_cause.md
[R01]: ../codex/reports/phase_17h_r0_r1_evidence_provenance_hardening.md
[V5BLOCK]: ../codex/reports/phase_17h_v5_operator_preparation_signing_and_controlled_execution.md
[CAT]: ../codex/reports/phase_17h_v5_authorized_catalog_migration_and_commercial_reconciliation.md
[FIN]: ../codex/reports/phase_17h_v5_complete_financial_readiness_and_operator_preparation.md
[V5LIVE]: ../codex/reports/phase_17h_v5_execution_window_renewal_and_rsa_authorization.md
[SIZE]: ../codex/reports/phase_17h_v5_reducer_sizing_offline_reconciliation.md
[V6]: ../codex/reports/phase_17h_v6_git_checkpoint_claim_identity_and_live_readiness.md
[V7]: ../codex/reports/phase_17h_v7_claim_identity_hardening_and_readiness.md
[V7LIVE]: ../codex/reports/phase_17h_v7_controlled_four_call_execution.md
[V8]: ../codex/reports/phase_17h_v8_lineage_hardening_and_offline_readiness.md
[V8BOUND]: ../codex/reports/phase_17h_v8_structural_path_boundary_regressions.md
[V8LIVE]: ../codex/reports/phase_17h_v8_controlled_four_call_execution.md
[V9]: ../codex/reports/phase_17h_v9_source_identity_reliability_and_offline_readiness.md
[POSTV9]: ../adr/phase_17h_post_v9_generation_wire_assessment.md
[WIRE]: ../adr/phase_17h_v10_generation_wire_receipt_decision.md
[IMPL]: ../codex/reports/phase_17h_v10_application_owned_evidence_and_lineage_implementation.md
[ENTRA]: ../codex/reports/phase_17hl_entra_v2_report.md
[APPROVAL]: ../codex/reports/phase_17hl_operator_approval_report.md
[POLICY]: ../codex/reports/phase_17hl_evaluation_policy_activation.md
[V10READY]: ../codex/reports/phase_17h_v10_operator_preparation_and_readiness_assessment.md
[V10BLOCK]: ../codex/reports/phase_17h_v10_final_operator_verification_and_conditional_live_execution.md
[V10CONT]: ../codex/reports/phase_17h_v10_final_signing_and_controlled_live_outcome.md
[SIGN]: ../codex/reports/phase_17h_v10_rsa_signing_and_independent_verification.md
[V10]: ../codex/reports/phase_17h_v10_controlled_four_call_evaluation_and_reconciliation.md
