# Phase 17H — Hierarchical Digestion Readiness Assessment

Date: 2026-11-02. Audited repository HEAD: `f2a60fa`. Scope: read-only technical assessment, with this report as the only permanent addition.

## 1. Executive summary

**Readiness: NOT READY to proceed directly to the next live hierarchical evaluation under the current L1 size contract.** The hierarchy, durable document result, publication, retrieval and grounded-answer interfaces already exist. The blocker is downstream envelope compatibility and its verification, rather than an absent digestion implementation.

The audit ran **27 focused existing tests: 27 passed, zero failures/skips, two pytest reporting warnings, in 13.85 seconds**. A pre-collection network guard recorded **zero network attempts**. These tests confirm selected hierarchy, provenance, recovery, publication and answer contracts. The complete regression suite was not repeated.

A separate synthetic, render-only probe found that application-valid results below the current 10,000-byte allowance can exceed the next reducer's rendered input bound. This occurs even in the established one-chunk/four-page L1 composition. The implementation correctly refuses the oversized request before inference. Older 3,000-byte stress evidence does not establish compatibility with this larger result allowance. Resolve and verify this contract offline before seeking a new live authorization.

After that gate, the smallest practical next evaluation is the existing **four-call full L1**: one fresh chunk analysis, one structural reduction, one root synthesis, and one grounded factual question, with persistence/publication/retrieval between synthesis and Q&A. This verifies two reduction levels but **does not demonstrate multi-chunk aggregation**. The smallest two-chunk counterpart needs **five calls** and a separately reviewed launcher/approval scope; the current L1 launcher fixes its contract at four attempts.

Attempt 6 remains the accepted single-analysis milestone described in the [closure assessment](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md), especially sections 9–15. Its live acceptance and settlement were **reported historical evidence**, not reverified against private artifacts here. Full Phase 17H remains PARTIAL; this audit does not change phase status.

## 2. Method and evidence boundaries

Findings below distinguish **source-verified**, **executed offline**, **historically reported**, and **unverified/inferred** behavior. Source inspection covered implementation, consumers, relevant tests, README, the original [17H report](phase_17h_report.md), [readiness design](../../evaluation/phase_17h_readiness.md), [Foundry runbook](../../evaluation/phase_17h_foundry_validation.md), [offline E2E report](phase_17hl_offline_e2e_contract_verification.md), and Attempt 6 integration/closure reports.

Initial `git status --short` and `git diff --stat` were empty. No existing application, configuration, test or documentation file was edited. Test outputs and the disposable probe were written under `/tmp/phase17h-hierarchy-audit-20261102/`; bytecode writing and pytest's repository cache were disabled. Application dotenv loading was suppressed by the existing test isolation mechanism. The standalone probe installed the same isolation before application settings imports.

No credentials, private operator packet, real financial/security database, historical raw response, Azure configuration or cloud service was accessed. No live launcher, signing/approval consumption, paid operation, Docker or Kubernetes operation was executed. No external pricing or current Azure quota facts were verified. No architectural or API changes were made.

## 3. Existing implementation and supporting references

### 3.1 Planning and execution of the hierarchy

**Source-verified:** multi-chunk digestion is implemented. [planning.py:106](../../../documents/digestion/planning.py#L106) validates the extraction reference, then partitions canonical source pieces while preserving order and coordinates. `_build()` inventories eligible, skipped and unsupported units; chunk IDs bind extraction/profile/structure/evidence. Text can be split without silently losing coverage; unsupported visual interpretation remains explicit.

[planning.py:231](../../../documents/digestion/planning.py#L231) builds bottom-up reduction nodes, with bounded fan-in, depth, result estimates and step count. Larger child sets produce additional reduction levels. A reduction is still created for a singleton structural group, explaining L1's one-chunk → structural → root chain. The document root is `plan.root_id`.

[workflow.py:35](../../../documents/digestion/workflow.py#L35) converts the DAG into durable dependency-bound steps. [ManagedDigestionHandler.analyze](../../../documents/digestion/managed.py#L287) selects the four managed stage profiles:

| Profile | Selection |
| --- | --- |
| `chunk` | Analysis chunk |
| `intermediate` | Non-final reducer within a structural group |
| `structural` | Final reducer for a non-root structural group |
| `root` | The plan's document root |

The existing L1 shape exercises `chunk`, `structural`, and `root`; it does not exercise the separate `intermediate` profile. Multi-chunk managed tests do exercise all four. Model execution remains behind the provider-neutral structured inference boundary in [managed.py:116](../../../documents/digestion/managed.py#L116); no new runtime integration is needed to represent a hierarchy.

### 3.2 Child propagation, provenance and validation

**Source-verified and selectively tested:** [workflow.py:108](../../../documents/digestion/workflow.py#L108) constructs every parent input from the committed children's complete `StageResult`, immutable checkpoint reference and application-owned `InheritedSummary`. It does not substitute a child filename or just a prose summary. [managed.py:152](../../../documents/digestion/managed.py#L152) renders these as generated, untrusted child material, alongside explicit required child claim links and permitted evidence IDs. Tools are unavailable; original evidence and generated material remain distinct.

[validation.py:64](../../../documents/digestion/validation.py#L64) enforces decoding/model validation, canonical result bytes, stage/kind binding, deterministic claim identity, authorized evidence membership, supported-fact structure and valid child links. An analyzed leaf must cover every supplied source evidence ID. Every reducer must link every supplied child claim. The canonical evidence resolver additionally binds scope, document version, extraction, source, block and span/line coordinates ([validation.py:22](../../../documents/digestion/validation.py#L22)).

Finalization reopens all checkpoints and reconstructs their requests in topological order, revalidating results, parent references, inherited counters and proposition sets ([workflow.py:150](../../../documents/digestion/workflow.py#L150)). [make_digest](../../../documents/digestion/validation.py#L255) walks the accepted root claim graph back to leaves, requires connected findings, and calculates full block coverage using interval unions. `COMPLETED` is a workflow state; `COMPLETE`, `PARTIAL` and `FAILED` are separate digest quality states.

There is an important qualification to “correctly propagated.” Exact leaf qualifications, limitations, questions and structured conflicts survive in immutable checkpoints/final artifacts. However, [ChildInput](../../../documents/digestion/models.py#L249) supplies immediate child results plus inherited counts and references, not the entire transitive annotation graph. Full propositions are deliberately excluded from model input ([validation.py:227](../../../documents/digestion/validation.py#L227)). A root can link a child whose prose omitted a qualification while the original qualification remains recoverable in the artifact. The validator does not establish that root prose faithfully states every qualifier or entails the sources. Contradiction detection uses explicit matching proposition subjects/stances, not general natural-language contradiction inference. These are semantic review requirements, not evidence-loss findings.

The final executive summary is the first root claim's text; named section summaries similarly use the first section claim. All root claims remain in `synthesis_claims`, and exact leaf claims remain in `findings` ([validation.py:327](../../../documents/digestion/validation.py#L327)). A useful complete narrative cannot be inferred from graph completeness alone.

### 3.3 Persistence, checkpointing, recovery and failures

**Source-verified and selectively tested:** validated stages produce immutable, content-addressed checkpoints containing the plan hash, parent references, result, inherited summary and propositions. Finalization commits a `document-digest/1` artifact plus coverage manifest; [load_digest](../../../documents/digestion/workflow.py#L184) reads accepted final manifests, rather than orphan output bytes.

[IntentStore and Worker](../../../documents/jobs/worker.py#L57) register object-write intentions before writes, inspect returned references, and commit through the job lease. [SQLiteJobLedger](../../../documents/jobs/sqlite.py#L334) checks lease ownership/fence, expiry, cancellation and terminal state; stale workers cannot accept late results. Failed dependencies terminate/cancel remaining work. Recovery uses the durable outbox, reconciliation and relay, rather than process memory.

[DocumentJobs.admit](../../../documents/jobs/service.py#L17) and [SQLite resume admission](../../../documents/jobs/sqlite.py#L253) reuse compatible successful steps only when their dependency chain is reusable and their immutable objects verify. Prompt/model/capability/profile changes invalidate reuse. An uncommitted paid result is not a reusable accepted checkpoint; automatic recomputation could charge again. Workflow recovery therefore does not imply exactly-once upstream execution.

The general worker supports bounded retries, including retry-after and retry budgets. The live L1 composition deliberately uses `RetryPolicy(max_attempts=1)` ([foundry_preflight.py:205](../../../tests/performance/foundry_preflight.py#L205)). [GovernedExecution](../../../governance/execution.py#L15) separates reservation/admission, actual usage settlement, and application acceptance. A paid response rejected by domain validation still incurs its known usage; unknown usage and accounting failure must remain visible and block continuation.

These facilities are adequate for the bounded local reference workflow with explicit operator reconciliation. They do not establish autonomous restart scheduling, distributed database coordination, hard in-process parser preemption, or live cloud exactly-once behavior. The original 17H report explicitly leaves automatic recovery within two leases unestablished. No new recovery framework is recommended for the small next evaluation.

## 4. Publication, retrieval and evidence-grounded Q&A

**Source-verified; happy path selectively executed offline:** a completed hierarchical digest can traverse the following existing integration:

| Boundary | Implemented behavior and reference |
| --- | --- |
| Accepted document result | Final digest and coverage stored through fenced manifests; reopen via `load_digest`. |
| Publication admission | [planning.accepted](../../../documents/publication/planning.py#L37) requires an uncancelled `COMPLETED` job and `COMPLETE` digest, reconstructs the accepted DAG without inference, and compares rebuilt digest/coverage with stored output. |
| RAG records | [planning.records](../../../documents/publication/planning.py#L80) publishes covered **canonical original-source text**, split into exact tokenizer-bounded spans. Generated summaries are not promoted to original evidence. |
| Prepare and activation | [PublicationService](../../../documents/publication/service.py#L83) plans immutable generations, upserts deterministic vector records, validates inventory, and explicitly activates through epoch/generation CAS. Preparation alone is not activation. |
| Retrieval | [PublicationReplica](../../../documents/publication/retrieval.py#L46) loads an expected generation, pins selected documents, combines generation/document-filtered dense retrieval with BM25, and validates reranker output. Stale replicas fail readiness. |
| Citations | [citations](../../../documents/publication/retrieval.py#L172) resolves actual source excerpts and canonical PDF physical pages/text spans against the pinned document version. |
| Derived context | [annotations](../../../documents/publication/retrieval.py#L208) separately carries qualifications, conflicting leaf findings, limitations and questions from the digest. |
| Q&A | [DocumentAnalysis](../../../documents/publication/analysis.py#L44) sends original evidence, labelled derived annotations and its answer schema through the existing provider. It validates citation membership/uniqueness and revalidates the pin before returning. No retrieved evidence skips inference. |

[AuthorizedPublication and AuthorizedAnalysis](../../../security/services.py#L5) provide authorization/governance composition. `/documents/analyze` is an additive, opt-in API ([api/app.py:300](../../../api/app.py#L300)); default application startup does not create a digestion/publication deployment automatically. The evaluation harness explicitly composes these services ([foundry_preflight.py:238](../../../tests/performance/foundry_preflight.py#L238)). No missing fundamental persistence-to-retrieval bridge was found.

Remaining verification must include a fresh accepted live chain, explicit publication activation/replica load, real pinned local embedding artifacts, selected document/version citation checks, and independent answer review. A Q&A failure does not undo an already complete digest or necessarily revoke an activated publication; the evaluator must report separate digest, publication and answer outcomes. The focused test `test_failed_qa_leaves_completed_digest_and_settled_usage` confirms this distinction.

Citation `provenance=validated` and `semantic_support=not_evaluated` are intentional contracts. Schema acceptance and valid coordinates do not certify answer entailment, required-finding recall, successful abstention or resistance to natural-language prompt injection.

## 5. Current test coverage and audit execution

The following coverage exists in source; only the selection described afterward was rerun.

| Existing tests | What they establish offline |
| --- | --- |
| [unit/documents/test_digestion.py](../../../tests/unit/documents/test_digestion.py) | Deterministic structure/order, fan-in at 1/2/4/5/17/65 chunks, multiple levels, source coverage, opposing propositions/qualifications, invalid evidence/links, no omitted children, transitive root-to-source traversal and bounds. |
| [integration/test_document_digestion.py](../../../tests/integration/test_document_digestion.py) | Real synthetic PDFs, durable reopen, reducer failure/resume, cancellation at analysis/intermediate/root/finalization, orphan writes/stale fences, corrupt checkpoint rejection and partial/unavailable policy. |
| [integration/test_managed_digestion.py](../../../tests/integration/test_managed_digestion.py) | Multi-chunk managed execution across all four stage profiles, OpenAI-compatible fake transport, reuse/invalidation, retry-after, expiry/cancellation and paid invalid evidence. |
| [integration/test_governed_digestion.py](../../../tests/integration/test_governed_digestion.py) | Managed stages under security/financial authorities, budget denial without a retry storm, cancellation retaining usage. Inspected, not rerun. |
| [integration/test_phase17hl_offline_e2e.py](../../../tests/integration/test_phase17hl_offline_e2e.py) | Current strict L1 wire/application contracts, complete digest, publication, citations, settlement and reopen/reuse. Fault cases cover first/root reducer lineage and coverage, provider failures, unknown usage, Q&A failure and revocation. Its positive L1 is explicitly **one chunk**, not multi-chunk. |
| [unit/publication](../../../tests/unit/publication/test_planning.py), [retrieval](../../../tests/unit/publication/test_retrieval.py), [analysis](../../../tests/unit/publication/test_analysis.py), [lifecycle](../../../tests/unit/publication/test_lifecycle.py), [security](../../../tests/unit/publication/test_security.py) | COMPLETE-only publication, corruption rejection, preparation/activation recovery, generation pinning, selection, revocation, annotations, citation forgery and context refusal. |
| [integration/test_publication_chroma.py](../../../tests/integration/test_publication_chroma.py) | Actual local Chroma prefilters generation/document before top-k. Inspected, not rerun; publication tests used fake embeddings/vectors. |
| [integration/test_phase17h_reliability.py](../../../tests/integration/test_phase17h_reliability.py) | Process exits around claim/write/commit/cancel and bounded PDF refusal. Inspected; existing historical results retained. |
| [unit/test_foundry_30k.py](../../../tests/unit/test_foundry_30k.py), [foundry_envelopes.py](../../../tests/performance/foundry_envelopes.py#L93) | Render stress, quota/headroom and known large-document refusal. Envelope construction still explicitly uses **3,000 canonical bytes**, legacy generation mode, rather than current strict L1's 10,000 bytes. |
| [integration/test_foundry_l1_launcher.py](../../../tests/integration/test_foundry_l1_launcher.py) | Intercepted launch composition, configuration/approval refusal, usage/timeout obligations and transport cleanup. Inspected only; no approval/signature workflow was executed in this audit. |

### Executed selection

The focused run selected these existing functions, including their parameterized cases:

- Digestion unit: `test_fanin_and_multiple_levels`, `test_qualifications_and_opposing_evidence_survive_root`, `test_reducer_cannot_omit_child_or_invent_source`, `test_root_claim_links_resolve_to_original_evidence_not_summaries`.
- Document integration: `test_reducer_failure_resumes_only_unfinished_work`, `test_cancellation_blocks_acceptance_and_preserves_prior_checkpoints`, `test_synthesis_crash_written_checkpoint_and_stale_fence`, `test_corrupt_analysis_checkpoint_rejected_on_resume`.
- Managed integration: `test_managed_end_to_end_reopen_and_checkpoint_reuse`, `test_existing_openai_provider_through_entire_durable_pipeline`.
- Strict L1 integration: `test_l1_extraction_dag_schema_digest_citations_accounting_and_reopen`, `test_failed_qa_leaves_completed_digest_and_settled_usage`.
- Publication: `test_partial_failed_digest_never_published`, `test_generation_pinning_stale_replica_and_revocation`, `test_wrong_document_and_generation_citation_fail_closed`, `test_selected_document_canonical_citations_not_semantic_certification`, `test_context_overflow_rejected_without_truncating_annotations`, `test_qualifications_and_both_conflicting_propositions_retained`.

Execution used `python -m pytest -p offline_guard -p no:cacheprovider`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `PYTHONDONTWRITEBYTECODE=1`, an external `--basetemp`, and external JUnit output. The temporary guard used the pre-collection socket/DNS denial pattern already documented in the [offline E2E report](phase_17hl_offline_e2e_contract_verification.md#recreating-the-temporary-isolation-plugins). Result: **27 passed in 13.85s; zero network attempts**. The two warnings concern `record_property` with JUnit's default `xunit2` format; no application assertion failed. Logs: `focused.log` and `focused.xml` under the temporary audit directory.

No full pytest, large-document benchmark, compileall, lint, Docker build or Compose check was needed for this report-only audit. These are not claimed as fresh passes.

## 6. Identified gaps and reproduced risks

### G1 — Current accepted output allowance does not ensure downstream fit: live gate blocker

**Executed offline:** a disposable probe extracted the existing `pdf(4, seed=1708)` fixture, used current `managed-prompt/4`, `managed-generation/2`, strict capability, stage input bound 24,800, 3,000 completion tokens, 28,000 context, and 10,000 raw/canonical result bytes. It called the existing `maximal_result(request, index, 'escaped')` helper to construct application-valid responses containing bounded qualifications, questions and limitations, then called the actual managed renderer. `NoInference.execute` could only raise; no model ran.

| Probe | Application-valid child bytes | Actual downstream rendered bytes / conservative input estimate | Observation |
| --- | ---: | ---: | --- |
| Existing one-chunk L1, analysis | — | 11,213 / 11,413 | Analysis render fits; synthetic result is 8,580 bytes. |
| Same plan, structural reducer | 8,580 | 25,542 / 25,742 | `context_exceeded` before inference. |
| Same plan, root | 8,571 | 25,416 / 25,616 | `context_exceeded` in diagnostic continuation. |
| Two-chunk variant, `chunk_characters=800`, structural reducer | 8,502 + 8,502 | 41,733 / 41,933 | Planner admits two children, but managed render refuses. Plan has two reducers and five total calls with Q&A. |
| Existing one-chunk L1, `claims` witness | 4,825 then 5,572 | Structural 15,825 / 16,025; root 16,510 / 16,710 | Both render successfully. Failure is response-shape dependent, not universal. |

The planner's [per-child capacity estimate](../../../documents/digestion/planning.py#L234) uses result bytes plus fixed overhead. The actual renderer includes trusted control/schema, required links, inherited wrappers and nested JSON escaping. Planning admission is therefore not a proof of managed request fit. Runtime bounds correctly fail closed; there was no truncation, repair or limit bypass.

The probe deliberately continued **synthetic artifact construction** after render rejection to inspect later envelopes. Its constructed `COMPLETE` artifact is not a successful managed workflow. The conservative eight-excerpt Q&A render seam from `question_envelopes()` reported `analysis_limit` at estimates **53,839** for the one-chunk escaped case and **68,550** for the two-chunk escaped case; the concise-claims case fit at **9,709**. That seam repeats long canonical excerpts and is not an executed real retrieval result. Its Q&A numbers establish a conservative annotation-growth risk; exact selected-hit compatibility still needs the integrated verification below.

These are structural counterexamples to envelope sufficiency, not semantic labels or observed Azure responses. Actual provider tokenization, the ability to emit these witnesses within 3,000 completion tokens, and their real-model likelihood were not measured. Even the one-chunk counterexample is enough to invalidate relying on old small-result stress tests as current readiness proof.

### G2 — Multi-chunk current-contract integration and launcher scope

**Verified coverage gap:** separate tests establish multi-chunk managed execution, and strict L1 establishes publication/Q&A/accounting, but the inspected strict L1 positive test fixes `len(plan.chunks) == 1`. No single inspected test establishes the full current strict 10,000-byte, multi-chunk, governed digestion-to-publication-to-Q&A path with meaningful cross-chunk qualifications/conflicts.

[LaunchConfiguration.bounded](../../../tests/performance/foundry_l1.py#L76) requires four attempts and cumulative ceilings of 100,000 input/12,000 output tokens; [execute](../../../tests/performance/foundry_preflight.py#L110) fixes live L1 to four fixture pages with the existing chunk profile. Two chunks plus structural/root and Q&A need five calls. Changing only a private attempts field cannot enable that evaluation. Do not improvise a live execution outside the reviewed launcher or reuse Attempt 6's single-call approval/output as an accepted checkpoint.

### G3 — Live reductions, document output and semantic acceptance remain unverified

**Historically reported:** Attempt 6 accepted one first-stage response and settled known usage. Neither that result nor this offline audit demonstrates accepted Azure structural/root reductions, a live COMPLETE document, live-derived publication/retrieval, or a correct grounded answer. Qualification retention in artifacts is stronger than semantic preservation in root prose. Independent claim/citation review remains necessary.

### G4 — Bounded reference-operation limits

**Source-verified/historical:** recovery requires reconciliation/relay; publication activation and replica loading are explicit; authorities are single-host SQLite; all selected annotations accompany Q&A and can grow despite bounded top-k evidence. These are limits to record, not reasons for unrelated infrastructure work before a small local evaluation. Historical L2 envelope failures remain unresolved evidence, not a current successful larger profile. This audit did not rerun L2 or extrapolate its old exact numbers to a new profile.

## 7. Recommended immediate offline engineering work

No fixes were implemented. The next authorized engineering task should be narrowly scoped to these gates:

1. **Turn G1 into permanent focused regressions and reconcile the actual contracts.** Reproduce the escaped witnesses against current strict L1. Verify rendered input including schema, child wrappers, complete links and JSON escaping, rather than only `StageRequest` or result length. Verify the exact retrieved-hit Q&A request plus all derived annotations. Select and document a bounded profile/planning policy whose permitted result shapes fit every downstream stage without dropping source coverage, lineage, qualifications or conflicts. Re-plan and rebind source/configuration hashes after any change. A bare return to the old 3,000-byte allowance is not justified: Attempt 6's historically accepted result was 3,907 canonical bytes.
2. **Add one small current-contract multi-chunk integration fixture.** Use two chunks, strict fake HTTP, actual durable worker/governance/publication/replica/analysis, selected-document evidence and explicit cross-chunk qualification/opposition. Assert the exact two-analysis → structural → root DAG and five fake calls with Q&A; check COMPLETE coverage, all child links, resolved canonical citations, independent outcome states, settled synthetic usage and reopen/reuse without new calls. Add focused omission/forged-link failure cases and a downstream oversized-result rejection case. Reuse existing recovery tests rather than rebuilding their matrix.
3. **Refresh the four-call L1 offline acceptance evidence.** Once bounds are reconciled, run only affected size/schema/DAG tests plus the existing full L1 synthetic path and selected financial/authorization refusal checks. Verify real local pinned embedding availability without downloads before future operator preparation. A complete regression rerun is unnecessary unless an implementation change exposes a broader compatibility concern.

The two-chunk rehearsal can remain wholly offline. A five-call live launcher/approval extension is only needed if a later task explicitly selects the multi-chunk live milestone; it is not required to attempt the existing four-call L1 first. No RAG redesign, provider migration, AKS work or new cloud dependency follows from these findings.

## 8. Proposed next bounded live evaluation — conditional, not authorized

### Objective and expected outcome

After section 7's acceptance gates, recommend **one fresh full L1 evaluation on the existing deterministic four-page native PDF**, through the reviewed local launcher. Objective: establish live reducer/application compatibility and a durable COMPLETE document that can be published, retrieved and used for one factual source-grounded answer. It is an integration smoke evaluation, not Phase 17H closure or proof of multi-chunk synthesis.

| Order | Work | Model calls on the successful path |
| --- | --- | ---: |
| Preparation | Deterministic PDF/extraction, canonical checks, pinned plan and job admission | 0 |
| 1 | Chunk analysis covering all four supplied source pieces | 1 |
| 2 | Structural reduction covering every accepted child claim | 1 |
| 3 | Root synthesis with complete lineage | 1 |
| Persistence/publication | Final validation, COMPLETE digest/coverage manifests, authorized local prepare/activate, replica load and evidence retrieval | 0 |
| 4 | “What is the first inspection procedure on physical page 1?” | 1 |
| Review | Independent comparison against canonical page-one procedure and all emitted factual claims | 0 |
| **Total** | **Three digestion calls plus one Q&A call; zero retries** | **4** |

The plan must be checked anew before approval. If the offline correction changes chunk/reducer count, this four-call proposal no longer applies. Stop and review its new exact call envelope; do not silently increase it. Existing model identity/region/tier are historical candidates requiring fresh operator verification, not current cloud facts established by this report.

### Token and cost estimation

Retain the existing maximum **25,000 input + 3,000 inclusive completion tokens per call**, subject to the stricter 24,800 rendered-stage input bound and capability overhead/safety checks. Four calls reserve at most **100,000 input + 12,000 output tokens**. Completion includes reasoning usage; do not add reported reasoning a second time. Byte bounds and token ceilings are separate contracts.

Render every proposed stage offline with validated complete child witnesses. Use the project's conservative serialized-input estimator plus overhead/safety for admission; label it an estimate, not billed model tokens. Record both per-stage estimates and the full reserved ceiling. The current diagnostic numbers in section 6 fail this gate and cannot be used to launch.

With approved uncached per-million EUR rates `r_in`, `r_out`, and explicit aggregate fixed/additional upper bounds `F`, `A`, calculate using exact decimals:

```text
maximum proposed run cost = 0.100000 * r_in + 0.012000 * r_out + F + A
observed catalog cost = sum(actual_input_i * r_in / 1,000,000
                          + actual_output_i * r_out / 1,000,000) + applicable extras
```

Obtain a current applicable commercial basis or an explicitly approved conversion/catalog, including effective date, currency, region, agreement/tier and every billable dependency. Unknown extras block preparation for live approval. Confirm remaining owner/tenant monthly headroom after prior attempts and unresolved obligations. The existing EUR 5 ceiling is an upper governance bound, not authorization to spend EUR 5 again or an estimate of invoice cost. This audit supplies no current price quote.

### Security, authorization and financial safeguards

- Require fresh explicit human authorization and independent signed approval for the exact full L1 configuration, window, source/generation bindings and four-call financial envelope. Full L1 uses audience `polymind-l1-live`; Attempt 6's `polymind-single-analysis-live` approval is consumed and out of scope ([approval verification](../../../tests/performance/foundry_approval.py#L102)).
- Keep application identity verification, document ownership/authorization, publication management, provider credentials and financial approval separate. Verify the existing principal/authorities and current credential validity through the approved private operator procedure; do not replace ledgers to erase debt. Credentials remain outside the repository and report.
- Use only the allowlisted PolyMind Foundry endpoint/deployment, approved model aliases, current verified shared quota/headroom and no redirects/proxy-derived credentials. Use strict managed digestion and the existing separately validated Q&A schema contract; no fallback, tools or repair call.
- Preserve [RunGuard](../../../tests/performance/foundry_budget.py#L78), durable reservation/settlement, one outstanding call, zero automatic retries, and at least 61 real seconds between starts under the current rolling-minute policy. Preserve at least 2,000 interactive TPM or any larger existing reserve; stricter available quotas win. Never enlarge quota to pass the test.
- Use only isolated local publication storage/Chroma and a hash-pinned already-present embedding model loaded without downloads ([local_retrieval](../../../tests/performance/foundry_l1.py#L146)). No paid cloud embeddings, AKS or shared publication mutation is required.
- Preserve one-use consumption/start markers, call records, checkpoints and financial evidence. A crash, uncertain start or unknown usage does not permit replay/reset. Retain sensitive prompts/results privately; permanent reports should contain sanitized conclusions/hashes/counts, not credential or upstream error material.

### Mandatory stops and success interpretation

Stop on the first provider failure, timeout, 429, truncation, malformed/invalid output, missing child/evidence coverage, unsupported critical conclusion, envelope/admission denial, cancellation, expiry/identity mismatch, publication/provenance mismatch, missing/inconsistent/excess usage, accounting failure, or unexpected billable dependency. Do not retry, repair, expand budget or continue to another model. Record paid usage even when application validation fails. Unknown usage stays unresolved pending trusted reconciliation.

Technical success requires all four expected calls and their accepted results, not merely launcher exit zero, `job_state=COMPLETED`, or `questions.status=COMPLETE`. The Q&A harness can record a schema-valid abstention as COMPLETE; for this answerable page-one question, acceptance additionally requires the correct finding and a supporting canonical page-one citation. Semantic success remains pending until independent human review. Preserve separate provider, application, digest, publication, Q&A and accounting outcomes.

## 9. Clear acceptance criteria

### Before another live inference

1. A reviewed current-contract offline result demonstrates that the chosen chunk/reducer/answer envelopes fit, including escaped output, full child links and full annotations. The G1 counterexamples are addressed or excluded by an explicit enforced contract without losing required information; successful concise fake output alone is insufficient.
2. A small current strict multi-chunk synthetic workflow passes the integration criteria in section 7. The existing four-call L1 remains reproducible after any sizing change. Negative cases fail before downstream inference/publication and preserve synthetic paid usage/checkpoints appropriately.
3. The exact future plan, model-call count, stage/schema/prompt bindings, local embedding availability, financial upper bound, existing authority/headroom checks, reviewer and stop procedure are reviewable. A fresh operator authorization is obtained separately. Nothing in this report grants it.

### To accept the next full L1 milestone

1. Exactly one analysis, one structural reduction, one root synthesis and one Q&A call; no retries/fallbacks. Each managed response passes strict provider and application/domain validation unchanged.
2. Job COMPLETED; persisted digest COMPLETE; full eligible source coverage (`fraction=1`), no failed/unsupported units; every required child claim connected through the root to canonical source evidence. Reopened checkpoints/digest verify and do not trigger additional inference.
3. Authorized publication accepted/activated; loaded generation and selected document/version agree; retrieved citation excerpts match canonical text and physical page coordinates. Generated material remains labelled as derived.
4. Page-one answer contains the fixture's expected first procedure and only supported factual conclusions, with a valid supporting page-one citation. Independently review all factual claims in the tiny smoke output, qualification/conflict treatment and any abstention. Require 100% valid citations, all required smoke findings and zero critical unsupported conclusions; unreviewed claims remain pending.
5. All known usage settles once in the matching durable records, within per-call/cumulative tokens and the approved cost ceiling; zero unknown obligations or accounting failures. Preserve reservation versus actual cost and invoice uncertainty separately.

Acceptance would close this narrow L1 integration milestone only. It would not establish multi-chunk live aggregation, the separate `intermediate` stage profile, representative semantic quality, larger-document/L2 feasibility, production reliability or external-user readiness. The smallest future multi-chunk live test is two analyses plus structural/root synthesis and one Q&A (**five calls, 125,000/15,000 maximum input/output at unchanged per-call ceilings**), requiring separate offline plan/launcher/approval work. It must not be run with the current four-call L1 contract.

## 10. Final audit and repository disposition

Implementation review traced all boundaries above and distinguished structural retention from semantic fidelity, planned versus rendered bounds, accepted checkpoints versus paid responses, and workflow completion versus publication/answer acceptance. The new report was separately reviewed for sensitive material, private configuration, accidental live instructions, broken relative file links and unsupported readiness claims. No fixes, dependencies or other permanent artifacts were introduced.

Validation: focused tests and disposable render-only probe as recorded above; new-report whitespace and relative-link checks; `git diff --check`; final `git status --short`, `git diff --stat`, and staged-diff inspection. All 58 relative file links resolve, and the report has no trailing whitespace. Final status shows this single untracked report, with no modified tracked files or staged entries; ordinary tracked `git diff --stat` is empty because it excludes untracked files. Git staging/history were untouched. **No stage, commit, push, reset or live inference occurred.**

Immediate next action: authorize a narrow offline envelope/integration engineering task addressing G1/G2, then reassess the four-call L1 proposal. Proceeding directly to live inference is not recommended.
