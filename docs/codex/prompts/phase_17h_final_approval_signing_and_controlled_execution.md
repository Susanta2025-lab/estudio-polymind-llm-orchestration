# Phase 17H — Final approval, signing and controlled execution

This records the final execution authorization supplied by the operator on
7 November 2026. The preceding task required read-only preflight, an independent
RSA signing authorization, signature verification without consumption, and a
second explicit authorization before any paid inference. The operator separately
reported successful local encrypted-key verification, subsequently authorized
signing to the exact proposed private destination, and then supplied the following
execution authorization. Those permissions were separate decisions; historical
Attempt 6 authorization conveyed no authority for this run.

## Execution authorization supplied by the operator

I separately and explicitly authorize the Phase 17H four-call Azure Foundry L1 live evaluation using the following exact artifacts:

**Configuration SHA-256:**
50613f94e7d2d6f560e27b5ec23a94de1d1b0a0549c3a0ed74202569c5842c76

**Signed approval ID:**
dc6c755a-0d4c-4f88-93be-81f8a7741c0a

**Signed artifact SHA-256:**
4149e205957cb33da500965c985901ea432e42def9a07a3608be851df4a899b0

Before launch:

1. Securely supply the resource-specific Azure API key and verified operator token without displaying or storing their values in logs.
2. Revalidate the configuration, signature, operator identity, governance and financial headroom, execution window, and replay status.
3. Confirm that the remaining credential and approval lifetimes safely cover the full four-call evaluation.
4. Stop without launching if any prerequisite fails.

Execution constraints:

- Exactly four authorized inference calls maximum.
- Zero automatic paid retries.
- One concurrent call.
- Minimum 61 seconds between call starts.
- No model, deployment, policy, or configuration changes.
- Preserve the existing financial and token limits.
- Stop on any failed acceptance or admission condition.

Use only the existing approved launcher and signed artifact.

After execution, report actual tokens, catalog-accounted costs, governance settlements, digest/publication/Q&A results, and the final Phase 17H outcome.

Do not initiate additional live tests or retries. Do not modify application code, reset authorities, or commit or push changes.

This authorization applies only to the exact approved four-call evaluation.
