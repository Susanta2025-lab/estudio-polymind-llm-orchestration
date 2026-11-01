# Phase 17H-L — Resolve L1 operator approval compatibility

Follow AGENTS.md. Inspect the current L1 launcher, signed approval implementation,
Entra v2 changes, tests and reports.

Replace the live launcher's dependency on an issuer-signed `polymind_l1_approval`
JWT claim with a separate, cryptographically verified operator approval artifact.

Requirements:
- Preserve strict Microsoft Entra v2 token authentication and the existing
  role/scope requirements.
- Bind approval to the verified operator identity, configuration digest, exact
  Foundry deployment, spending ceiling, token limits and expiration.
- Require a trusted operator signature and prevent approval replay.
- Never accept unsigned, expired, mismatched or test-only approval in live mode.
- Preserve existing governance ledgers and fail-closed behavior.
- Maintain backward compatibility where appropriate.
- Add offline positive/negative tests and update the approval template and runbook.

No live Azure requests, cloud changes, automatic approval, commits or pushes.

Run targeted tests and report any remaining blockers. Leave changes uncommitted.
