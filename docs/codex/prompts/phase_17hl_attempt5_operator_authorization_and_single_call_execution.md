# ESTUDIO POLYMIND — PHASE 17H–L

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](../reports/phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

## Azure Foundry Attempt 5 — Operator Authorization and Single-Call Execution

### 1. Objective

Proceed with **Attempt 5**, the controlled Azure Foundry live chunk-analysis diagnostic experiment.

The user has explicitly requested that Attempt 5 begin.

This authorizes preparation and **at most one paid inference call**, provided all existing operator approval, security, cost and execution gates pass.

Do not bypass any gate. Do not sign an approval on behalf of an independent operator.

Do not restart broad technical auditing or implement additional features.

### 2. Azure target

Use the supplied resource information:

```text
Subscription: ECI-Development
Subscription ID: <AZURE_SUBSCRIPTION_ID>
Tenant ID: <AZURE_TENANT_ID>
Resource: <FOUNDRY_RESOURCE_NAME>
Resource group: rg-epolymind
Project: epolymind-project-dev
Endpoint: https://<FOUNDRY_RESOURCE_NAME>.services.ai.azure.com/
Deployment: epolymind-gpt-54-mini
Model: gpt-5.4-mini
Version: 2026-03-17
Deployment SKU: GlobalStandard
Azure quota shown: 30,000 TPM allocated
```

The supplied project resource ID is:

```text
/subscriptions/<AZURE_SUBSCRIPTION_ID>/resourceGroups/rg-epolymind/providers/Microsoft.CognitiveServices/accounts/<FOUNDRY_RESOURCE_NAME>/projects/epolymind-project-dev
```

Use Azure OpenAI v1 Chat Completions through the existing adapter.
Do not use the separate ECI model deployment.
Do not change model, endpoint family or API protocol.

### 3. Read existing handoff

Read `AGENTS.md`, followed by:

```text
docs/codex/reports/phase_17hl_attempt5_final_readiness_and_operator_preparation.md
docs/codex/reports/phase_17hl_f1_http_cleanup_failure_preservation.md
docs/evaluation/phase_17hl_operator_approval.md
tests/performance/foundry_single_call.py
tests/performance/foundry_approval.py
tests/performance/foundry_budget.py
```

Use the existing single-analysis operator workflow.
Do not use the older four-call L1 launcher or historical approval packets.

### 4. Confirm current engineering bindings

Verify, without modifying code:

```text
Executor: 82fc01aa0447d4be758124cec0120a06db49f139f69ee6425b51b8696a6ad26f
Generation source: 7d387a8595cf63e2ac944a25c4987a1b37392aa4adba8889914acf51ff9f0f59
Provider schema: 4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2
Inference configuration: 7eaa6b52ad387f9f0c82e318e9c74fa378ffda0baec85d0f7157cc4ab0553519
```

If any required fingerprint has changed unexpectedly, STOP.

Preserve `managed-prompt/3`, `managed-generation/2`, `azure-strict/1`,
`stage-result/1`, `reasoning_effort=low`, `max_completion_tokens=3000`,
Strict JSON Schema, and existing deterministic claim IDs and validation predicates.

### 5. Minimal operator preflight

Reuse previously verified evidence. Do not repeat the full C1–C7 audit.

Confirm only current mandatory gates:

1. Deployment is the specified PolyMind model and the reported 30,000 TPM allocation remains applicable, with sufficient uncommitted capacity.
2. Existing pinned pricing and cost ceilings are applicable and current owner/tenant funds and obligations permit this one call.
3. Valid Entra operator identity and existing registered permissions.
4. Correct active inference credentials.
5. Correct protected authority paths, existing approval trust and persistent replay state.
6. Actual-scope fixture and rendered-request hashes match the final execution configuration.
7. Fresh, independently signed and unused approval for audience `polymind-single-analysis-live`.
8. Execution window and all nine required attestations satisfy the existing validators.

The supplied message ends with: “Use the established independent operator process if”.
No continuation was supplied or inferred.
