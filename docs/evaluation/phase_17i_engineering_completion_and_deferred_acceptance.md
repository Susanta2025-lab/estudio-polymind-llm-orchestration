# Phase 17I engineering completion and deferred acceptance

Decision date: **13 November 2026**. Authority: the project operator's [Stage 3 instruction](../codex/prompts/phase_17i_documentation_and_closure.md). This is the authoritative current Phase 17I engineering/documentation decision, prepared for operator review and manual documentation commit. It supersedes pre-implementation predictions about 17I in earlier handoffs, not their historical observations or Phase 17H's separate acceptance decision.

## Executive decision and three-stage model

| Classification | Decision |
| --- | --- |
| Stage 1 — Assessment | COMPLETE |
| Stage 2 — Implementation and verification | ENGINEERING PASS within bounded Option A |
| Stage 3 — Documentation and closure | DOCUMENTATION PASS — `PHASE_17I_STAGE3_DOCUMENTATION_PASS` |
| Bounded Phase 17I engineering | `PHASE_17I_ENGINEERING_COMPLETE` |
| Phase 17I documentation | `PHASE_17I_DOCUMENTATION_COMPLETE` |
| Actual external-user verification | `PHASE_17I_EXTERNAL_VERIFICATION_DEFERRED` |
| Formal external-user acceptance | `PHASE_17I_FORMAL_ACCEPTANCE_PENDING` |
| Subsequent engineering | `SUBSEQUENT_ENGINEERING_PERMITTED`, subject to its own prerequisites |
| Production readiness | NOT ESTABLISHED |

Exactly three formal development stages apply. All three engineering/documentation stages are complete. The original external-user acceptance requirement remains open with **0 actual participants**. Its deferred completion procedure is an outstanding obligation, not a fourth development stage. No single unqualified phase-complete label substitutes for these distinct classifications.

## Baseline and evidence precedence

Verified local HEAD on `master`: **`ed7dbd5ed63548bccfac9ef27a8a0f7b771ca26a`**, `feat(pilot): implement bounded supervised Phase 17I verification workflow`. Initial tracked/index diffs were empty; the 28 inherited untracked Phase 17H documents remain outside this change set. Earlier commits: `69c8f66` assessment, `b90f4ad` Phase 17 completion/deferred review, `9acfeb6` historical evidence, `f8ba9c1` v11 engineering.

Read-only GitHub verification confirms [Estudio PolyMind CI run 43391359991](https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/43391359991), completed/success, bound to this exact source commit. Reported elapsed 6m21s agrees with the run start/update timestamps, 08:12:03–08:18:24 UTC on 13 November. Stage 3 neither reruns CI nor attributes historical pytest counts to a new run.

Current source/interfaces establish implemented behavior. The [Stage 2 report](../codex/reports/phase_17i_implementation_and_verification.md) owns recorded validation. This decision owns current bounded completion; the [single gate register](phase_17i_external_user_readiness_gates.md#post-implementation--stage-3-reconciliation--13-november-2026) owns current exposure dispositions. Historical [assessment](../codex/reports/phase_17i_readiness_assessment.md), Stage 2 report/prompt and Phase 17H evidence remain unchanged, including contemporaneous unfinished-stage statements. The [Stage 3 report](../codex/reports/phase_17i_documentation_and_closure.md) records documentation validation and the exact commit inventory.

## Completed engineering scope

**Option A — Private, Operator-Supervised Local Verification** is implemented by `documents.pilot.SupervisedPilot`, a trusted local Python facade over existing authorities. The [operator reference](phase_17i_operator_workflow.md) gives exact constructor arguments, configuration, limits, operations and future GO/NO-GO. The path is:

```text
Verified operator → approved source and session → bounded native extraction
→ durable document job → governed v11 synthesis → validated COMPLETE digest
→ authorized publication → selected-document grounded Q&A
→ canonical citation presentation → structured feedback
→ session closure / withdrawal → revocation and residual inventory
```

The verified operator must have publication authority and own the source scope. Study codes and source/session approvals grant no participant principal or money authority. Hash, rights, classification, byte/page/character limits, native eligibility, model and profile binding precede provider work. One open document job, three total sessions, at most three synthesis attempts plus three questions/six provider attempts per document, and exclusive admitted provider use apply within the supported updated shared authority. PDF is at most four native pages; source bytes at most 1,000,000 and extracted characters at most 4,000. Existing tighter extraction/model/context/child/response/resource limits prevail. Small size does not guarantee eligibility.

Every managed stage explicitly selects `StageProfile.template_version="managed-prompt/11"`; the global v10 default is unchanged. Parser defaults are 10 s wall, 5 s CPU, 512 MiB address space, 256,000 output bytes and a 2 MiB file-size backstop with 32 descriptors/core dumps disabled. Python side-effect denial and POSIX subprocess supervision provide resource containment, not a native-code syscall sandbox. Provider timeout is 60 s; synthesis/Q&A share a 600 s cooperative admission deadline. These are configured ceilings, not measured real-user latency guarantees or forced preemption of all local retrieval work.

Durable admission/checkpoints reuse existing jobs, fencing, managed G1/G2 and receipts; publication uses `AuthorizedPublication`, selected Q&A uses `AuthorizedAnalysis`. Replica loading is explicit. Final session/security/publication guards bind exact generation and epoch before inert synchronous local release. Canonical citations expose original source identity, physical PDF pages or text lines, spans and excerpts. `semantic_support=not_evaluated` remains honest: structural validity is not entailment. External mode requires accepted exact-output expert findings, including separate findings for new held Q&A. Structured feedback, review packets, expiry/closure/withdrawal, stop, restart denial and residual inventory are implemented.

There is no new HTTP endpoint, participant login, Streamlit document portal, unrestricted upload UI, provider factory or public SaaS deployment. Provider-specific behavior remains behind the existing inference boundary. Existing RAG/LangGraph/tools/memory/API/UI/Ollama/OpenAI-compatible and NDJSON architecture is preserved. The Stage 2 optional `SQLiteInferenceAdmission.acquire(..., exclusive=False)` extension defaults to prior behavior; pilot exclusivity requires all shared consumers to use updated code. No source or API contract changes occur in Stage 3.

## Recorded implementation and validation evidence

| Stage 2 verification | Recorded result; not rerun in Stage 3 |
| --- | --- |
| Engineering implementation / offline verification | PASS within bounded single-host scope |
| Final pytest | **3,052 passed** in 960.00 s; JUnit 959.917 s |
| Final suite partition | **2,163 unit / 889 integration**; 0 failures/errors/skips; 0 warnings reported |
| New Phase 17I cases | **56** (27 unit / 29 integration), included in final total; N1–N15 covered |
| Compilation / relevant lint and formatting | PASS as recorded in Stage 2; not repeated |
| Local synthetic end-to-end | PASS; COMPLETE, coverage **1.0** |
| Deterministic provider calls / settled rows | **4 / 4**; 3 background + 1 interactive |
| Synthetic reservations outstanding | **0** |
| Canonical Q&A citation | **1**; PDF/text and four original page contracts also tested |
| Synthetic closure | CLOSED / `PURGE_PENDING` |
| Actual external participants | **0** |
| New billable inference | **0** |
| Independent human semantic reviews | **0/2** |

The synthetic provider responses, embeddings and reranker substitute for real models. Recorded synthetic settlement is test arithmetic, not Azure spending or a current price. Its feedback is authored fixture data, not observed usefulness. The [supported demonstration](phase_17i_operator_workflow.md#reproducible-offline-rehearsal) requires a fresh `--output` directory; Stage 3 inspects rather than repeats it. Earlier incomplete/intermediate Stage 2 runs remain historical and are not added to the final totals.

## Security, provenance, accounting and retention boundaries

The private host/operator and local SQLite authorities remain trusted, single-host references. Source/model text remains untrusted data; no tools or authority derive from it. Scope, epoch, expiry, principal disable, withdrawal, stop and stale/missing publication evidence deny release. Delivered bytes cannot be recalled. Fixture injection tests do not establish general real-model robustness, multi-host isolation, representative reliability or production security.

`GovernanceLedger` remains the financial authority; pilot control stores operational intents rather than another monetary ledger. Owner/tenant attribution, current policy/catalog, provider RPM/TPM/output/concurrency and admission history remain binding. Six-call forecasts reserve nothing. The 18-call cohort versus 16-request rolling-window and 500,400 versus 500,000 daily-token conflicts are detected, not waived. No new allowance, paid retry, policy migration, actual headroom or provider capacity approval follows from engineering completion.

Stop is durable before best-effort cancellation. In-flight work may finish and bill; known usage remains settled, UNKNOWN remains an obligation and blocks continuation across restart. `reconcile_operation` observes terminal existing financial/provider state plus a trusted quiescence reference; it cannot invent usage or refund money. Consistent post-stop restore drills do not certify arbitrary stale-backup rollback or autonomous recovery. Missing/empty control storage fails closed; first-time `initialize=True` cannot replace lost history.

The 19-class inventory distinguishes observed immutable objects, write intents/orphans, jobs/checkpoints/receipts/generations/vectors, feedback/reviews, usage, metadata, scratch, backups/provider copies and other residuals. Closure revokes presentation and fences eligible jobs; it preserves shared accepted artifacts and financial/audit history. `retire_metadata` performs logical redaction after the approved deadline. SQLite freelists, backups, provider copies and unverified storage remain residuals. **`PURGE_PENDING` is not physical deletion.** No automatic retention schedule or erasure certificate is claimed; stronger-erasure data classes are refused.

## Deferred obligations and formal closure prerequisites

`PHASE17I-EXTERNAL-USER-ACCEPTANCE` is **DEFERRED** under its [durable record](phase_17i_deferred_external_verification.md). Real usefulness, independent source/answer quality, consent/privacy/retention, external participation and new paid authorization remain pending; due date not scheduled, owner project operator. All sixteen gates have evidence-based current dispositions; G02 alone is engineering verified, while the other missing scope evidence/approvals remain partial or pending. None grants exposure.

Formal external-user acceptance requires accepted actual controlled-session evidence, reconciled usage and session/withdrawal/residual records, accepted applicable gates and criteria, and an explicit final decision, or an explicitly operator-approved revised acceptance policy. This task does not revise that policy. A future real-provider composition must integrate separately reviewed per-call permission; the default fixture permission cannot launch external work. Review of permitted retained outputs alone need not spend money.

The separate [Phase 17H human obligation](phase_17_deferred_human_semantic_review.md) remains `DEFERRED_PENDING_TWO_INDEPENDENT_REVIEWERS`, **0/2**; formal Phase 17 closure remains `PHASE_17_FORMAL_CLOSURE_PENDING`. Its current rubric and review count are unchanged. Two reviewers are a project-defined gate, not an automatic legal requirement for an independent project. Only a future explicit operator decision documenting method/limitations could revise it; this task grants no such revision. Real-user usefulness cannot substitute for that review or for pre-exposure quality evidence.

## Operator ownership and handoff

The project operator owns future scope/timing and final acceptance, private evidence custody, named responders and review coordination. Qualified domain reviewers/adjudicator own independent quality findings; source rights holders/controller/privacy/legal reviewers (DPO where applicable) own processing/notice/retention acceptance; security owner accepts actual access/exposure; financial approver/provider capacity owner accepts current budget/capacity and any separate execution. No individuals or dates are invented.

The [README roadmap](../../README.md#phase-roadmap) names broader Azure productionization of the document pipeline as the later direction, including durable cloud storage/state, distributed worker/admission infrastructure, identity hardening and production reliability controls. It does not define an approved Phase 18 implementation. No next numbered phase or new formal stage is created here. Subsequent engineering can proceed independently under its own assessment/authorization and prerequisites; this decision neither begins that work nor approves deployment, spending or participants.

Leave all Stage 3 changes unstaged/uncommitted for operator review. Preserve the 28 inherited historical files exactly and exclude them from the documentation staging inventory. No source, deployment configuration, databases, security thresholds or historical reports are changed by this decision.
