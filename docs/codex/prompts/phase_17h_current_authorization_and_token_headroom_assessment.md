# Codex Task — Phase 17H Current Authorization Readiness and Token Headroom Assessment

## Context

You are working in the Estudio PolyMind repository:

https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration

Phase 17H concerns the controlled four-call Azure Foundry L1 evaluation.

Previous engineering work established:

- G1/G2 hierarchical digestion engineering and historical contract compatibility: PASS.
- GitHub Actions CI: PASS.
- Four-call L1 offline workflow: PASS.
- Durable all-MiniLM-L6-v2 embedding model: verified.
- Operator preparation: READY WITH GAPS.
- Live execution: NOT AUTHORIZED.

The current operator has obtained a fresh Microsoft Entra token through the existing MSAL device-code utility. Cryptographic OIDC verification and registered-principal matching passed during the operator's checks on November 6, 2026.

Treat these as timestamped operator-reported evidence, not proof that credentials remain valid now.

Existing private authorities must remain unchanged.

## Current financial and quota observations

Read-only checks on November 6, 2026 reported:

| Metric | Owner | Tenant |
|---|---:|---:|
| Daily tokens used | 0 | 0 |
| Monthly tokens used | 4,290 | 4,290 |
| Monthly tokens remaining | 111,015 | 111,015 |
| Monthly cost remaining | EUR 4.991182682154170454 | EUR 4.991182682154170454 |
| Unsettled reservations | 0 | 0 |
| Requests in rolling window | 0 | 0 |
| Remaining request slots | 5 | 5 |

The four-call contract currently allows:

- Maximum four inference calls.
- 25,000 input tokens per call.
- 3,000 inclusive output tokens per call.
- 100,000 total input tokens.
- 12,000 total output tokens.
- Maximum aggregate token exposure: 112,000.
- Zero automatic paid retries.
- Maximum financial exposure: EUR 5, subject to verified remaining headroom.

**Observed monthly token shortfall: 985 tokens.**

The current nominal four-call maximum does not fit the November monthly allowance.

Historical ledger data:

- Six settled reservations.
- Zero active inference calls.
- One historical output-limit failure.
- No reported unresolved obligations.
- November 1 Attempt 6 consumed 4,290 tokens and EUR 0.008817317845829546.

Do not assume earlier non-November usage counts against the current monthly period.

## Objective

Independently assess the existing implementation and determine whether the full four-call L1 workflow can be authorized under the current immutable governance and financial constraints.

Investigate the 985-token shortfall and identify the safest contract-compliant options.

**This is an offline, read-only assessment. Do not authorize or execute live inference.**

## Task 1 — Verify the current engineering baseline

Review the current repository HEAD, Git status, GitHub CI evidence and relevant Phase 17H documentation.

Confirm:

1. Four-call hierarchy: chunk → structural → root → grounded Q&A.
2. G1 rendered-input and child-material admission controls.
3. Strict evidence and checkpoint validation.
4. Provider request/output limits.
5. Governance, quota admission and settlement behavior.
6. Independent signed approval and replay protection.

Identify the exact modules, configuration classes and methods responsible for each relevant limit.

Do not modify existing implementation.

## Task 2 — Audit actual ledger accounting semantics

Inspect the existing governance and admission implementation.

Verify:

- UTC daily accounting boundaries.
- UTC calendar-month boundaries.
- Rolling request-window calculations.
- Owner and tenant limit enforcement.
- Per-evaluation policy selection.
- Treatment of SETTLED, RELEASED, RESERVED, STARTED and UNKNOWN states.
- Whether settled usage counts actual rather than reserved tokens.
- Whether unresolved reservations remain counted across accounting periods.
- How future reservations interact with existing obligations.
- How the ledger handles consecutive calls within the same evaluation.

Reconcile the operator-reported November 6 observations with source-level rules.

Do not query private databases unless separately authorized. If private state is required, document the precise read-only check for the operator.

## Task 3 — Investigate the 985-token shortfall

The observed calculation is:

111,015 available monthly tokens − 112,000 maximum planned tokens = −985 tokens.

Determine whether this is a genuine blocking condition under the exact current execution contract.

Important questions:

1. Does the actual L1 launcher reserve the entire 112,000-token allowance upfront?
2. Does it reserve per call or per stage?
3. How are reservations settled before admitting subsequent calls?
4. Can actual settled usage legitimately release capacity for later calls?
5. Does the run-level budget remain a separate fixed 112,000-token commitment?
6. Do the governance, evaluation-specific and shared admission policies impose stricter limits?
7. Would the current execution be rejected before the first call, or could rejection occur later?
8. Are the current nominal per-call ceilings necessary for this deterministic four-page fixture?

Distinguish clearly between:

- The theoretical maximum token exposure.
- The actual admission reservations.
- Estimated token consumption.
- Previously observed synthetic token usage.
- Actual billed token consumption.

Do not assume that low historical model usage guarantees sufficient capacity.

## Task 4 — Assess contract-compliant alternatives

Evaluate these options without implementing them:

**Option A — Preserve the existing contract and wait for the accounting-period reset.**

Determine whether this resolves the monthly capacity shortfall and what other prerequisites must be refreshed.

**Option B — Use a smaller independently reviewed evaluation contract.**

Determine whether the current architecture supports smaller per-call or cumulative ceilings without weakening G1/G2, changing model behavior, breaking planning, or invalidating historical contracts.

A smaller budget is acceptable only if supported by the actual code and independently approved as a new configuration. Do not silently reduce limits.

**Option C — Retain the existing maximum but rely on sequential settlement.**

Establish whether this is supported by actual reservation semantics and whether it creates a risk of completing only part of the paid evaluation.

**Option D — Formal policy revision.**

Assess whether a properly approved increase would be technically possible, but do not recommend bypassing limits simply to force a live evaluation.

For each option, document feasibility, risks, required evidence and whether fresh independent approval is necessary.

Do not change quotas, financial limits, configuration fingerprints, token reservations or authority records.

## Task 5 — Review current identity and authorization status

Use historical operator evidence only as evidence of previously successful verification.

Confirm the existing contracts for:

- Microsoft Entra v2 delegated authentication.
- `PolyMind.L1Operator`.
- `PUBLICATION_MANAGE`.
- Registered owner/tenant scope.
- OIDC expiration and credential lifetime.
- Independent RSA approval.
- Configuration SHA-256 binding.
- Persistent replay prevention.
- Valid execution window.

Do not acquire or display tokens.

Do not read private keys, token files or signed approval artifacts.

Do not sign, approve or consume anything.

Mark live identity and approval readiness PENDING until verified within the eventual execution window.

## Task 6 — Financial and quota readiness

Review the existing catalog and financial calculation implementation.

Determine the exact evidence required to establish:

- Current applicable EUR input/output prices.
- Applicable deployment, model, version, SKU and region.
- Incremental fixed charges.
- Remaining owner and tenant financial headroom.
- Azure RPM/TPM allocation.
- Shared capacity and consumers.
- Four-call pacing and maximum concurrency.
- Reservation compatibility with the selected option.

Use `Decimal` arithmetic for monetary calculations.

Historical pricing may be used for comparison, not as proof of present applicability.

No Azure inference requests or cloud modifications.

## Task 7 — Offline verification

Run only the focused offline tests necessary to establish the assessment conclusions.

Prefer existing tests for:

- Governance budget and accounting boundaries.
- Reservation and settlement behavior.
- Quota admission.
- Four-call L1 workflow.
- G1/G2 sizing and strict hierarchy.
- Approval binding and rejection behavior.

Do not introduce test skips, xfails, mocks that bypass application acceptance, or artificial success conditions.

If an important contract question remains untested, identify the missing regression coverage. Do not introduce production changes during this assessment.

## Task 8 — Final readiness decision

Provide a concise decision matrix:

| Dimension | Classification |
|---|---|
| Engineering readiness | GO / NO-GO |
| Operator identity | Historical PASS / Current PENDING / FAIL |
| Governance authority | PASS / PENDING / FAIL |
| Monthly token headroom | PASS / BLOCKED |
| Financial headroom | PASS / PENDING / BLOCKED |
| Azure deployment/quota | PASS / PENDING / FAIL |
| Independent approval | AUTHORIZED / NOT AUTHORIZED |
| Four-call live execution | GO / NO-GO |

Answer explicitly:

**Can we safely authorize the four-call L1 evaluation under the current November 2026 token limits without modifying existing governance policies?**

Identify the best-supported option and the exact next operator action.

## Permanent deliverables

Create:

`docs/codex/reports/phase_17h_current_authorization_and_token_headroom_assessment.md`

And:

`docs/codex/prompts/phase_17h_current_authorization_and_token_headroom_assessment.md`

The report must preserve the observed figures, cite relevant source paths and methods, document executed checks, identify uncertainties and distinguish historical evidence from current verification.

## Restrictions

- No paid inference.
- No Azure resource changes.
- No AKS or Kubernetes operations.
- No private credential, signing-key or token inspection.
- No approval generation, signing or consumption.
- No financial reservations.
- No governance or admission database mutations.
- No quota or token-limit changes.
- No application-code modifications.
- No fabricated operator identities.
- No automatic retries or fallback calls.
- No Git staging, commits, pushes, resets, cleans or branch changes.
- No unrelated documentation or code changes.

Do not broaden the task into deployment or Phase 17I development.

## Final Codex response

Summarize:

1. Whether the 985-token shortfall is a real admission blocker.
2. Exact reservation and settlement semantics.
3. Whether a smaller contract is supported.
4. Whether waiting for December resolves the capacity issue.
5. Financial and Azure capacity prerequisites.
6. Final GO/NO-GO classification.
7. Exact remaining operator steps.
8. Permanent report location.

**Stop after completing the offline assessment. Live inference remains NOT AUTHORIZED.**
