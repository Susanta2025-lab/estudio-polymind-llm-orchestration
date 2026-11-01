# Reusable Evaluation Governance Policy — task record

Implement and verify offline a reusable `polymind-evaluation/1` policy for
explicitly authorized development owner/tenant scopes. Work on existing master;
preserve all pre-existing tracked and untracked changes. No staging, commit or push.

Approved offline allowances for both owner and tenant: 16 requests per rolling
86,400 seconds; 500,000 daily tokens; 1,500,000 monthly tokens; EUR 5 monthly cost;
112,000 simultaneously reserved tokens; interactive/background concurrency 1 each.
Preserve provider admission constraints, per-job limits, prices, no-retry behavior,
audit retention, usage settlements and historical costs. No reset, replenishment
or automatic policy change on experiment failure. Unknown obligations fail closed.

Inspect ledger, migration, policy serialization, identity authorization, shared
SQLite configuration, L1 launcher and tests. Use the smallest safe isolation
extension without parallel authorities bypassing global admission or financial
controls. Reject unauthorized scope/policy substitution and version mismatches.

Preserve managed-prompt/3, independent 10,000-byte provider/canonical JSON ceilings,
3,000 completion / 25,000 input tokens per request, four L1 requests, aggregate
100,000 input / 12,000 output reservations, 28,000 context, existing Foundry
deployment, local MiniLM/Chroma and evidence/qualification/contradiction/lineage checks.
Keep Entra, RBAC and RSA approvals unchanged. Recommend standing low-risk grants
only as future design, with explicit controls for production/high-risk changes.

Use synthetic authorities and network-blocked focused tests for scope selection,
production isolation, repeated experiments, request windows, token/cost exhaustion,
settled/unknown obligations, concurrent reservations, substitution, migration and
rollback/history, and L1 compatibility. Do not rerun unrelated suites/investigations.
Prepare a versioned migration plan, impacts, backup/rollback, dry run and precise
operator activation procedure; never mutate live databases, `.env`, replay markers,
signed packets, original audit evidence or existing policy records.

No Azure operations, inference, live activation, RSA signing, approval consumption,
Attempt 3 execution or authorization. Report architecture, implementation, focused
validation, migration readiness, future workflow and zero-action safety counters in
`docs/codex/reports/phase_17hl_reusable_evaluation_governance.md`.
Required result: PASS — REUSABLE EVALUATION POLICY IMPLEMENTED OFFLINE; ACTIVATION
PENDING, or BLOCKED with the exact technical issue, report/tests and next operator action.
