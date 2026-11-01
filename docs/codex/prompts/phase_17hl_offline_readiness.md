# Phase 17H-L — Complete Local Configuration & Offline Readiness

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](../reports/phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

Follow AGENTS.md. Inspect the current L1 launcher, approval template, runbook and
existing uncommitted changes. Complete local L1 configuration and readiness
verification without live inference.

1. Read existing `.env` privately. Use the approval template and actual
   `LaunchConfiguration` schema to prepare an unapproved draft at
   `<PRIVATE_OPERATOR_DIRECTORY>/l1-configuration-draft.json`, reusing
   verified endpoint/deployment, Entra settings, EUR assumptions and governance
   paths. Preserve existing files; review before overwriting. Leave unknowns unset
   and execution flags false. Distinguish incomplete fields from invalid values.
2. Inspect Entra/OIDC and prior operator authorization, existing security,
   governance and provider SQLite authorities, approval trust and RSA fingerprint,
   persistent replay directory, ownership, permissions and isolation. Check the
   30K TPM / 2K protected interactive TPM / one background RPM policy and proposed
   EUR 5 ceiling. Never change authority/replay records, regenerate keys, consume
   approvals or expose tokens.
3. Identify four-page L1 embeddings/runtime artifacts, inspect compatible local
   copies, verify integrity and tree hash where possible, and check Chroma/runtime
   dependencies. No downloads, dependency installation or paid resources.
4. Validate configuration/readiness gates and fail-closed behavior. Run existing
   offline L1 integration/security/approval tests, the complete pytest regression
   suite once, compilation and whitespace checks. No provider inference calls,
   including smoke tests.
5. Update the existing Phase 17H-L readiness report with PASS/BLOCKED findings,
   private draft status, exact tests, remaining operator confirmations and Git
   status. Cover Azure RPM/shared consumers, credential validity/auth compatibility,
   service-charge bounds, embeddings/runtime, audit location/retention and operator
   approval. Do not mark unverified conditions PASS.

No Azure inference or resource modifications, execution signature or financial
authorization, security/governance/replay changes, secrets in output/Git, L2
redesign, Phase 17I work, staging, commits or pushes. Stop after offline verification
for operator review.
