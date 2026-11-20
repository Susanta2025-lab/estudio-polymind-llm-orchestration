# Estudio PolyMind — Phase 19B: Offline Azure VM Deployment Implementation

## Objective

Implement and verify the offline deployment foundation for Estudio PolyMind Phase 19:
Azure Linux VM Deployment & Real-Model Integration. Produce a secure, locally testable
configuration for subsequent controlled Azure VM validation. Do not provision Azure
resources or execute real-model inference.

Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`.
Baseline: `master`, HEAD `b48dde4`, CI `44409425956` PASS, 3,184 regression tests PASS.
Phase 19A assessment is complete, offline implementation ready with conditions.
Preserve the four uncommitted Phase 19A documentation files and historical evidence.
19A is complete; 19B offline implementation/verification is current; 19C controlled
Azure validation/documentation is not started.

## Mandatory initial verification

Read AGENTS.md, Git status and complete Phase 19A deliverables:

- `docs/codex/reports/phase_19a_readiness_report.md`
- `docs/evaluation/phase_19_deployment_architecture.md`
- `docs/evaluation/phase_19_implementation_plan.md`
- `docs/codex/prompts/phase_19a_readiness_verification.md`

Inspect Dockerfiles, Compose, settings, entrypoints, authentication, worker and provider
interfaces and reusable tests. Confirm offline implementation requires no Azure or paid
provider activity. Do not redesign architecture or repeat Phase 19A research.

## Secure dedicated deployment

Provide separate Phase 19 Docker Compose configuration, reusing existing images/components:
private authorized operator → HTTPS gateway → Streamlit/FastAPI → one document worker →
durable local authorities, Redis, Chroma → provider-neutral approved external adapter.
Require private UI/API communication, no public database/worker/cache/vector ports,
persistent mounts, non-root execution, private filesystem modes, health/readiness,
controlled start/stop, bounded logs/restarts, explicit environment/secrets. Preserve all
`make chat-*` and `make docs-*` behavior. Development issuer, synthetic inference and
localhost TLS must never become production defaults. Missing essential authentication,
inference or authority configuration must fail closed.

## Persistence and single-worker safety

Preserve security/governance/admission SQLite, jobs/checkpoints, canonical objects,
publication/citations, Q&A, financial reservations/audit, Redis/Chroma persistence.
Use stable explicit host paths and compatible local filesystems. Prevent concurrent
authority writers; preserve locks/leases and state across restart. Provide controlled
stop/backup/restore. Never automatically replay potentially billable uncertain work.
Do not introduce PostgreSQL, Blob Storage, Kafka, Celery/distributed queues, or put
SQLite on Azure Files/SMB/NFS. Do not alter existing financial/governance records.

## Authentication and application integration

Chat's legacy path rejects OIDC and its Streamlit client does not forward credentials.
Implement a narrow authenticated path only if existing identity, authorization and
governance contracts can be reused without weakening them. Preserve streaming, routing,
memory and provider neutrality. Never bypass denial guards. If substantial redesign
is needed, document the blocker and keep Chat disabled in the deployment.

Documents currently has only synthetic composition. Preserve the operator workflow;
provide separate non-fixture composition where supported, reusing the operator API,
durable runner and security services. Require valid external OIDC; never substitute
a development issuer. Offline identity fixtures are test-only; no live Entra contact.

## Real-model preparation: offline only

Preserve InferenceProvider, logical roles, streaming/structured output, schema/capability
contracts, admission/quota/finance, idempotency and immutable usage. Configure/validate
external endpoint, deployment alias, capabilities and authentication mechanism. Secrets
must be runtime inputs, never code/image contents. Verify requests/schemas with mocks,
strict errors, timeouts/rate limits, missing capability/authorization/financial denial,
UNKNOWN handling and no unauthorized retries. Neither Chat nor Documents may bypass
shared provider admission. Use fake/local HTTP endpoints only. No Azure calls, credential
renewal, paid inference or new execution-approval signing. Phase 17H historical Foundry
evidence is not current execution authorization.

## Resource and cost readiness

Compare Phase 19A candidates `Standard_B2as_v2` (2 vCPU/8 GiB, burstable) and
`Standard_D2as_v5` (2 vCPU/8 GiB, non-burstable); do not select without evidence.
Where Docker permits, measure aggregate memory/CPU, image/persistent disk footprint,
startup/readiness, embedding/reranker overhead, Redis/Chroma, and one bounded synthetic
document workflow. Prefer representative composition measurements. Document local
limits and Azure CPU-credit validation still required. Do not claim 8 GiB sufficient
without evidence. The proposed USD 30 ceiling is planning, not spend authorization.

## Verification

Focused automated tests must address Compose validity/dependencies/isolation/ports,
secret exclusion, persistence, one writer, readiness/shutdown; required auth,
invalid/expired identity, missing config, no fixture fallback, cross-owner/tenant denial,
governance/finance; unchanged local Chat and synthetic Documents, durable accepted
Q&A/authorized reload, provider-neutral contracts and no restart-driven inference;
missing mounts/permissions, durable restart, UNKNOWN reconciliation, duplicate workers,
and coherent backup/restore. Run targeted tests then full regression where feasible,
Docker/Compose, compile and configured lint checks. Reuse dependencies and Docker cache;
no unrelated builds/pruning. Record exact commands/counts/failures/unavailable checks.

## Scope

Allowed: necessary narrow config/composition/application/security/provider changes,
dedicated deployment files, offline tests/synthetic local validation and operations docs.
Forbidden: Azure provisioning/mutation/login/activation; real inference; new credentials
or renewal; live Entra; public application exposure; new managed infrastructure; unrelated
Phases 1–18 work; resetting/replacing governance truth; broad rewrites; Git commit, push,
reset, stash or clean. Report essential unimplemented requirements as GAP/BLOCKER.

## Deliverables

Create this prompt and
`docs/codex/reports/phase_19b_offline_implementation_and_verification.md`.
Append dated implementation addenda to the Phase 19 architecture/plan; retain historical
19A conclusions. Provide concise deployment prerequisites/startup, storage, identity,
provider/security, synthetic verification, backup/restore, shutdown and cloud gates.

## Final review and verdict

Perform implementation self-review and separate pre-commit review. Confirm no credentials,
private keys, runtime databases or generated secrets enter source. Report exact changed
files, reuse/implementation, Compose, Chat, Documents/provider status, persistence/recovery,
resources/limits, exact tests, operator blockers and Git status; nothing committed/pushed.

```text
PHASE_19B_OFFLINE_IMPLEMENTATION_COMPLETE: YES/NO/WITH_CONDITIONS
DOCKER_COMPOSE_OFFLINE_VALIDATION: PASS/GAP/FAIL
CHAT_OIDC_INTEGRATION: PASS/GAP/FAIL
DOCUMENTS_NON_FIXTURE_COMPOSITION: PASS/GAP/FAIL
REAL_PROVIDER_OFFLINE_CONTRACT: PASS/GAP/FAIL
SINGLE_HOST_PERSISTENCE_AND_RECOVERY: PASS/GAP/FAIL
AZURE_DEPLOYMENT_READINESS: READY_WITH_CONDITIONS/BLOCKED
AZURE_PROVISIONING_AUTHORIZED: NO
LIVE_INFERENCE_AUTHORIZED: NO
PUBLIC_EXPOSURE_AUTHORIZED: NO
```

Stop after offline implementation/verification. Do not deploy Azure or begin Phase 19C
without explicit operator review and authorization.

## Continuation — Integration Gap Resolution (19 November 2026)

Continue the same Phase 19B working tree, read its latest report and preserve all existing
tracked/untracked changes. Resolve Chat OIDC and Documents non-fixture execution gaps only.
Do not repeat 19A research or redesign the verified five-service Compose, persistence,
provider-neutral contract or recovery mechanisms.

For Chat, reuse verified OIDC principals, ownership, tenant isolation and authorization;
establish an explicit execution scope and forward native Streamlit credentials to FastAPI.
Preserve `/query`, `/query/stream`, LangGraph routing, hybrid RAG, conversation memory,
NDJSON and existing local Ollama/development behavior. Enforce shared admission/security/
finance and isolate retrieval/memory. Replace denial guards only with actual authorization.
An explicitly authorized single-operator scope is sufficient. No disabled-auth/static-token/
fixture fallback is allowed in production. Report a precise blocker if safe integration
requires substantial redesign.

For Documents, preserve the meaning of `SessionApproval.zero_paid_execution=True` and the
fixture-only hook. Implement a distinct, independently authorized, configuration-bound
execution permission, binding principal/tenant/source/deployment/financial policy/scope.
Revalidate validity and revocation at execution boundaries. Reuse existing pilot/operator/
governance/admission and OpenAI-compatible provider paths. Preserve quotas, budgets,
deadlines, idempotency, reservation/settlement, UNKNOWN, no unauthorized retries and all
session guarantees. Do not add a financial ledger or paid-execution shortcut. UI controls
must rely on backend authority. Test with isolated synthetic records and fake providers;
do not modify historical approvals or activate paid execution.

Inspect relevant implementations and consumers first. Add focused tests for scoped Chat
OIDC, missing/expired/invalid tokens, unauthorized/cross-tenant requests, streaming,
retrieval/memory isolation, legacy compatibility and financial/admission enforcement.
For Documents test valid independent permission, missing/expired/revoked/mismatched denial,
zero-paid immutability, full Start → Digest → Publication → Q&A, duplicate/retry prevention,
reservation/settlement/UNKNOWN, execution revalidation, restart and persisted results.
Where practical exercise both paths through the existing private topology with offline
fixtures. Run targeted regressions then one complete `python -m pytest -q` after corrections
if feasible, Compose checks, compilation and `git diff --check`. Do not sum overlapping counts.

Retain every earlier scope restriction: no Azure/login/real Entra/provider call, credential
renewal, live execution signing, historical authority mutation, policy/price/quota change,
public ports, new distributed infrastructure or Git commit/push/reset/stash/clean.

Append a clearly separated **Integration Gap Resolution** section to the existing report,
preserving historical findings. Update architecture/plan/operator documentation only for
implemented behavior. Report both root causes, exact files, authorization paths, retained
security/financial invariants, executed evidence, operator blockers and Git status.

```text
CHAT_OIDC_INTEGRATION: PASS/GAP/FAIL
DOCUMENTS_GOVERNED_EXECUTION_PERMISSION: PASS/GAP/FAIL
DOCUMENTS_NON_FIXTURE_COMPOSITION: PASS/GAP/FAIL
REAL_PROVIDER_OFFLINE_CONTRACT: PASS/GAP/FAIL
DOCKER_COMPOSE_OFFLINE_VALIDATION: PASS/GAP/FAIL
PHASE_19B_OFFLINE_IMPLEMENTATION_COMPLETE: YES/WITH_CONDITIONS/NO
AZURE_PROVISIONING_AUTHORIZED: NO
LIVE_INFERENCE_AUTHORIZED: NO
PUBLIC_EXPOSURE_AUTHORIZED: NO
```

A PASS requires executed evidence beyond parsing or isolated mocked authorization.
Stop after resolving/verifying these gaps. Do not start Phase 19C or Azure deployment.
