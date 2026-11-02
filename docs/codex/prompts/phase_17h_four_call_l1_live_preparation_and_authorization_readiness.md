# Phase 17H — Four-Call L1 Live Evaluation Preparation and Authorization Readiness

Normalized user prompt, received 2026-11-02. Repository: Estudio PolyMind.

## Context and scope

Phase 17H remains PARTIAL. The previous G1/G2 engineering task addressed
downstream inference sizing and validated the strict two-chunk offline workflow.
Read these reports before proceeding:

- `docs/codex/reports/phase_17h_hierarchical_digestion_readiness_assessment.md`
- `docs/codex/reports/phase_17h_g1_g2_offline_engineering_and_integration_hardening.md`
- `docs/codex/reports/phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md`

The next milestone is a controlled Azure Foundry evaluation involving exactly
four model calls. This task is preparation and readiness assessment only.
Do not execute live inference or consume any authorization.

## Tasks

1. Inspect current source, configuration, tests and evidence. Verify that the
   corrected G1 sizing policy is active in the intended L1 configuration; the
   four-call workflow fits managed-inference contracts; strict provider and
   application validation, provenance, hierarchical claim links, durable
   checkpointing, recovery and publication remain integrated. Identify actual
   implementation/configuration blockers and whether further code changes are needed.
2. Review the existing launcher and configuration without changing the launcher.
   Verify a newly generated plan for chunk analysis, structural reduction, root
   synthesis, then grounded Q&A after successful persistence, publication and
   retrieval. Confirm call count, dependencies, source bindings, corrected sizing
   and expected artifacts. Never reuse historical approvals, checkpoints or
   configuration bindings. A demonstrated launcher blocker requires a separate
   engineering task.
3. Check local prerequisites offline: embedding availability and expected
   fingerprint; publication/vector/retrieval configuration; required environment
   names and completeness without secrets; security and financial integration;
   deterministic reviewable configuration; existing preflight/validation
   procedures. Use lightweight targeted checks; no full regression suite without
   a specific new issue.
4. Review fresh explicit exact-configuration authorization, independent signed
   approval, authentication and identity scope, per-call and cumulative ceilings,
   documented maximum financial exposure, one outstanding call, zero automatic
   paid retries, durable reservation/settlement and stop conditions. Retain
   25,000 input and 3,000 inclusive output tokens per call unless stricter limits
   are required. Assess 100,000 input/12,000 output cumulatively for four calls.
   Explain estimation through configured model/catalog contracts. Invent no
   prices; assume no historical Azure price/quota/credential is current. Mark
   required external information/private operator evidence pending instead of
   accessing paid services or protected artifacts.
5. Classify findings PASS (current source/offline verification), PENDING (operator
   verification/fresh authorization), or BLOCKED (demonstrated technical or
   operational issue). Give separate engineering GO/NO-GO for preparation and
   execution AUTHORIZED/NOT AUTHORIZED decisions. Recommend minimal corrections.

## Restrictions

Primarily read-only. Do not modify application code, tests, configuration or
existing documentation. Do not execute paid inference/cloud operations or alter
AKS/cloud resources. Do not access/consume private signed approvals, credentials
or protected authority databases. Do not create real financial reservations or
consume budgets. Do not invoke a launcher that could initiate live execution.
Do not weaken security, validation, provenance or financial controls. Do not
stage, commit, push, reset, clean or switch branches. Do not repeat completed
investigations without new evidence. Only the permanent report and this
normalized prompt record may be added to the repository.

## Required deliverable and acceptance

Create
`docs/codex/reports/phase_17h_four_call_l1_live_preparation_and_authorization_readiness.md`
with executive summary; implementation/configuration verification; exact workflow
and artifacts; G1/G2 compatibility; local embedding/publication/retrieval;
security/authentication/operator approvals; token/cost governance and estimation;
executed offline checks and results; outstanding prerequisites/blockers;
engineering decision; execution authorization; recommended next action.

Distinguish current verification, historical evidence, assumptions and operator
verification. Include no private credentials, signed payloads, confidential raw
responses or sensitive operational identifiers. Completion requires reviewed L1
and G1/G2 paths, assessed local prerequisites, documented financial/authorization
requirements, identified blockers and defensible decisions, with no paid
inference, cloud modification or authorization consumption.

Final response: concise engineering and execution decisions, confirmed technical
prerequisites, outstanding blockers/operator actions, checks performed and report
path. Do not launch the evaluation; end with assessment and recommendations.
