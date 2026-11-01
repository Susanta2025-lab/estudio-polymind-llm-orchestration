# Phase 17H–L — managed-prompt/4 subject-contract implementation brief

Implementation task supplied on 29 October 2026. This clean brief preserves the
authorized scope and acceptance requirements; the complete task was supplied in
the Codex session.

Implement only the confirmed managed-generation instruction gap identified in
`../reports/phase_17hl_attempt5_post_execution_diagnostics.md`: Attempt 5 completed
one strict response, then correctly failed application validation with
`serialization_error / claim_contract / subject_on_nonfact`.

Read repository AGENTS.md and the diagnostic, live execution, operator approval,
two-layer validation and inactive generation-clarification proposal documents.
Capture the existing dirty worktree and preserve unrelated work.

Make `managed-prompt/4` the new active default in
`documents/digestion/managed.py`. Only facts may have a non-null subject. All four
non-fact kinds (`unknown`, `unsupported`, `commentary`, `structural`) must emit
null. Facts may emit null too. Populated factual subjects retain existing Token
length/pattern constraints and identify propositions. Empty/blank strings are not
null; do not reclassify claims to preserve subjects. Facts still require supported
status and authorized source support. Retain explicit field-complete generation,
deterministic claim IDs, originating stages, evidence, lineage and coverage.

Keep profile/adapter/planner/renderer bindings coherent across chunk, intermediate,
structural and root. Preserve immutable v3 source/request evidence separately;
reject stale execution bindings. Keep stored StageResult compatibility and
checkpoint integrity. Do not silently migrate plans, approvals or checkpoints.

Do not change models, validators, diagnostics, codecs, provider schemas/adapters,
security, governance, admission, financial/approval authorities, provider settings,
token/byte budgets, one-call limits, retries or fallbacks. Do not normalize outputs
or add repair passes. Do not activate the inactive proposal's qualification or
unavailable-analysis changes. Provider schema remains `azure-strict/1`; domain
contract remains `stage-result/1`.

Extend established offline tests with prompt/version assertions, all five kinds
against null/token/missing/empty/blank/invalid/type subjects, real synthetic
extraction and full validation, unchanged schema fingerprints, negative controls,
sanitized diagnostics and counting fakes. Preserve historical witnesses; classify
active expectations separately. Install network denial before application imports,
disable implicit dotenv/credential loading and use disposable local state.

Recompute executor, generation, schema, managed-configuration and synthetic rendered
request fingerprints using existing mechanisms. Do not create a future private
configuration. Review every changed file, run focused tests and diff/compilation
checks, and write the prescribed eleven-part engineering report at
`../reports/phase_17hl_managed_prompt4_subject_contract_implementation.md`.

No inference, Azure/authentication, Docker/Kubernetes, deployment, signing,
Attempt 6 preparation or execution is authorized. Attempt 5 is immutable and
SETTLED; do not open or modify protected run/trust/key/replay/financial state.
Leave all changes uncommitted; report observed checks, limitations, fingerprints
and separate future authorization prerequisites. Stop after implementation,
offline validation, reconciliation and reporting.
