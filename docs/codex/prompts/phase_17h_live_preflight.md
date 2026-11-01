# Phase 17H-L operator task record

Condensed record of the externally supplied Phase 17H-L prompt; not a verbatim
transcript. Scope: L0 preflight, offline preparation and operator approval handoff.

Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`, branch `master`,
expected HEAD `af4a7a076c918ef13aea05d74bf239c0af909133`. Starting Phase 17H status:
PARTIAL, bounded reliability PASS, real-model quality NOT VALIDATED, Foundry PENDING.

Read AGENTS.md and the 17H evaluation/report/observations/readiness, 17E and 17G
reports, security contract, OpenAI-compatible provider, structured/admission/factory
interfaces, managed digestion/workflow, execution/ledger and versioned quality
fixture. Inspect further files only to resolve dependencies. Reuse canonical
fixtures, document workflows and annotation-driven quality evaluator. No Foundry SDK
when the existing compatible provider suffices.

Verify clean expected Git state; preserve changes. Never branch, commit, push,
reset, stash or clean. Inspect environment names/presence only. Never print secrets,
private endpoints, resource IDs or deployment identifiers. No secret retrieval,
model discovery call, Azure CLI mutation, deployment or provisioning.

Propose EUR 5 maximum marginal validation expense, without authorizing spend.
Before model calls obtain the exact model/deployment, region/tier, input/output
prices, currency/unit/effective date/source, hourly/provisioned and other service
charges, final budget and available quota. Reject unknown or incompatible prices,
currencies or fixed costs. Do not assume promotional credit or change capacity.

Use GovernanceLedger and InferenceAdmissionPort. Absolute project limits:
50 attempts including retries; 25,000 reserved input and 3,000 reserved output per
attempt; 1,250,000 input and 150,000 output overall; one concurrent call; at most
2 RPM and 30,000 TPM. Stricter model/quota/budget constraints win. Calculate
`(reserved_input * input_rate + reserved_output * output_rate) / price_unit`, plus
known additional charges. Reserve worst-case expense before execution. Never
confuse rate estimates with billed usage. Unknown usage remains outstanding and
halts work pending trusted reconciliation; local admission is not a guarantee
about delayed Azure billing.

Prepare separately executable L1 (four-page reproducible fixture) and L2 (200-page
17H fixture). L1 covers extraction, planning, durable admission, managed inference,
hierarchy, evidence validation, complete digest, publication, retrieval/citations
and predefined fact evaluation. Stop before L2 if any critical step fails. L2
covers distant facts, contradictions, qualifications/revisions, missing evidence,
false premises, injected instructions and abstention against the versioned rubric.
Include all evaluation calls in the same ceiling; refuse L2 if the complete DAG
and evaluations cannot fit. Do not drop evidence requirements to fit.

Preserve question/rubric, selected documents/versions, response hash, actual
citations, expected findings, extracted factual claims, independent reviewer
judgment, unsupported conclusions, qualifications/contradictions, abstention and
uncertainty. Never fabricate human review or call an LLM judgment independent
human review. Report metric numerators/denominators and reviewer coverage. Candidate
targets: 100% valid citations, 95% supported claims, 90% finding coverage, zero
critical unsupported conclusions. One sparse PDF cannot certify representative
expert quality.

Stop on financial/token/call limit, governance/admission denial, identity mismatch,
repeated 429/timeouts, capability mismatch, uncertain usage, invalid evidence,
critical unsupported conclusions, publication inconsistency, unexpected billing
dependency or cancellation. No fallback model, quota increase or endless retry.

This session must add only necessary small local validation modules and focused
tests, run fully offline fake inference, provide explicit-unknown cost/configuration
templates, and write `docs/codex/reports/phase_17h_live_preflight.md` plus
`docs/evaluation/phase_17h_foundry_validation.md`. Do not rerun the prior 732-test
baseline without production changes justifying broader regression.

Report exact baseline, known/missing model facts, capability requirements/pricing
sources, proposed exposure, L1/L2 calls/reservations/fit, dry results, security/audit
readiness, privacy, approval requirements and blockers. Finish with requested Git
status/stat/check/index/log outputs and separate untracked inventory. Leave all
changes unstaged/uncommitted. Conclude L0 PASS/BLOCKED/PARTIAL, L1/L2 NOT STARTED,
AWAITING APPROVAL. Explicitly report zero billable Foundry calls, deployments,
Azure mutations, commits/pushes and Phase 17I work. Do not start L1 automatically.

## L1 integration continuation — 2026-10-13

Prepare the existing four-page L1 workflow for the named PolyMind GPT-5.4 mini
30K deployment, implementation and offline verification only. Preserve prior work.
Add an operator-bound launcher using actual provider/identity/admission/governance
contracts; default offline, require verified explicit approval, retain canonical
publication/citations and private audit evidence. Limit L1 to four attempts,
100K input/12K output reservations, one concurrent request and one background
request/minute with at least 2K interactive TPM. EUR 5 remains unapproved. Test
intercepted HTTP, credentials/endpoint isolation, complete envelopes, durable
accounting and fail-closed behavior. Reuse 198-test evidence, run affected tests
and full regression once. Update report/runbook/template; do not change L2 or
perform Azure inference, resource changes, commits, pushes or Phase 17I work.
