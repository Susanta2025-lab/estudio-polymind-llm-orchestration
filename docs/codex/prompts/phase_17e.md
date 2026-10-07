# Phase 17E — Managed Inference Integration

Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`. Branch: `master`.
Major phase: **Phase 17 — Production Document Digestion & Intelligence**.
Previous results: Phase 17A, 17B, 17C and 17D PASS. This is the finalized clean
phase prompt, organized by implementation contract; the operator's complete
scope, acceptance criteria and no-commit policy govern it.

## Operator Git policy and preparation

**Do not commit any Phase 17 work until all of 17A–17I is complete and reviewed.**
Work directly on master. Do not branch, stage, commit, push, reset, stash, clean,
restore, check out existing files, delete untracked Phase 17 work or use commits
as checkpoints. Preserve the intentionally dirty Phase 16/17A–17D worktree.
Preserve prior artifacts byte-for-byte except cumulative README/roadmap updates
and narrowly justified compatibility changes. Do not rewrite previous reports.
Before editing, record `git status --short --branch`, `git rev-parse HEAD` and an
outside-repository snapshot of every potentially modified file, preferably under
`/tmp/polymind-phase17e-baseline`.

Read root AGENTS.md completely, all README, all four 17A–17D reports and 17C/17D
prompts. Inspect relevant documents/jobs/digestion implementation and tests;
InferenceProvider, OpenAI-compatible and Ollama adapters; selection/configuration,
logical roles, metrics, normalized errors, readiness and streaming; and available
Phase 8A–8D/16 evidence. Search consumers and establish actual interfaces from
source, not solely reports.

## Purpose and hard scope

Connect Phase 17D StageRequest to existing provider-neutral InferenceProvider,
then real managed/external structured results, mandatory 17D validation, immutable
checkpoints and Phase 17C durable workflow. Preserve evidence, bounded input,
checkpoint and retry semantics. Never create independent DocumentFoundryClient,
DocumentOpenAIClient or DocumentVllmClient stacks.

Implement the managed synthesis adapter, deterministic structured prompts,
conservative decoding boundary, four stage profiles, capabilities/context/output
checks, estimates versus actual usage, job/stage/attempt accounting, provider-wide
admission, overload/429/retry-after/timeout/error normalization, cancellation/fences,
model/profile checkpoint compatibility, bounded Foundry validation where configured,
OpenAI-compatible/OpenAI-style/external-vLLM protocol tests and documentation.

Do not implement self-hosted vLLM, GPU provisioning, Foundry deployments/capacity,
Azure resources/network changes, AKS/node pools/HPA/Kubernetes workloads, production
authentication/external access, RAG/Chroma/BM25 publication, external OCR, training,
fine-tuning or broad Phase 18 infrastructure. Do not provision Redis or repurpose
it merely because it exists. Do not add another SDK, agent framework, LangChain,
LiteLLM, vLLM package, GPU runtime or substantial dependency without necessity.

## Provider and interactive compatibility

The existing provider layer remains inference authority. Provider HTTP/auth,
served-model syntax and configuration stay outside the digestion domain. Primary
live target is already configured Azure Foundry through the existing compatible
adapter. Validate generic compatible endpoints, OpenAI-style endpoints and
external vLLM; compatibility does not mean operating their infrastructure.

Preserve existing generate(), generate_stream(), role routing, Ollama, readiness,
API contracts, NDJSON versus upstream SSE, metrics and normalized errors. Prefer
an additive richer execution method/envelope carrying text, optional exact usage,
served identity and finish reason. Do not change existing return types or introduce
provider retries. Non-streaming complete JSON is appropriate for document stages;
partial JSON never reaches checkpoint acceptance.

## Phase 17D, prompts and profiles

Preserve `SynthesisInference.analyze(StageRequest) -> bytes`. A managed adapter
renders the request, selects role/profile, calls the provider and returns bounded
bytes. Phase 17D remains authoritative for StageResult schema, evidence permission,
lineage, claim validity, coverage and digest acceptance. Never bypass its validator.

Separate SYSTEM/CONTROL from UNTRUSTED DOCUMENT DATA and GENERATED CHILD MATERIAL.
Document instructions cannot override the task. No tools are exposed. Prompts
require exact structured schema, only allowed evidence IDs, explicit unsupported/
unknown conclusions, retained qualifications/conflicts and no invented references.
Version templates and make request construction deterministic for identical
StageRequest, profile, capability and model configuration.

Provide chunk, intermediate, structural/section and root/document profiles. Each
binds version, logical role, input budget, reserved output, schema/template version
and behavior constraints. Evaluate existing summarization/general/fast mappings;
do not assert a cheaper role's quality without evidence or hard-code deployments
in domain profiles. Use conservative sampling only when explicitly supported.

Use stronger provider-native JSON/schema modes when configured, otherwise prompt
JSON with the identical strict application boundary. Native schema guarantees never
replace application validation. Accept exact valid JSON. Document any narrowly
supported formatting normalization; reject prose, malformed/truncated JSON, invalid
schema and fabricated/foreign/unavailable evidence. Do not build an uncontrolled
repair parser or invent content during repair. Retry only classified transient
failures through Phase 17C.

## Capabilities and bounds

Require verified or explicitly conservative configured context and maximum output,
structured-output, streaming and usage capability metadata. Never infer capability
from marketing/model names; unknown bounds fail safely. Check before every call:
StageRequest validity, rendered request bytes, evidence cardinality, stage input
and output bounds, and

```text
estimated input + reserved output + provider/system overhead + safety margin
    <= configured verified/conservative context capacity
```

Do not send an overflow and rely on provider 400. Keep provider output limits
consistent with stage reservations; do not request huge output just because the
model allows it. Bound HTTP/raw response, decoded JSON, claims, fields, annotations
and evidence using existing 17D limits where possible. No silent truncation.

## Usage, accounting and observability

Keep estimated input/reserved output separate from optional actual input/output/
total reported usage. Missing fields and timeout/lost-response cost remain unknown,
not zero or estimates presented as actual. Attribute admitted calls/observations to
job, step, attempt, profile, provider, role and safe configured/returned model.
Retain retry amplification, unknown outcomes and rate-limit evidence for later 17G
cost governance; no pricing/billing implementation is required.

Detailed accounting belongs in durable trusted scoped state/artifacts, not metric
labels. Reuse bounded operational metrics for provider/role/outcome/errors/usage.
Never label metrics with job/document/owner/tenant, evidence, filenames, text,
endpoint or credentials. Do not log prompts, source/generated text, evidence text,
full responses, raw exceptions or secrets. Model/config metadata must exclude URLs,
keys and tenant/subscription secrets.

## Admission, fairness and durability

Define a shared provider-neutral InferenceAdmissionPort, with a local deterministic
or database-backed reference suitable for testing without infrastructure. A single
worker semaphore is not a global quota guarantee. Represent RPM, conservative
input-plus-output TPM, bounded concurrency, INTERACTIVE versus DOCUMENT_BACKGROUND,
reserved interactive headroom and basic per-job fairness. Document the shared
production adapter boundary; do not build a sophisticated second scheduler.

Reuse Phase 17C attempts, stable step identity, retry budget/not-before, cancellation,
leases, fences and manifests. Provider calls can occur despite losing a response:
exactly-once billing/execution is impossible. Preserve one accepted logical result,
not byte-identical real-model output. Temperature zero is not reproducibility.
Compatible accepted checkpoints are reused; changed role/model/prompt/schema/
capability/settings must invalidate incompatible reuse. Distinguish semantic
compatibility metadata from observational usage/latency/attempt metadata.

## Errors, backoff, timeouts and cancellation

Normalize 429 and overload, preserve safe retry-after seconds/date hints, distinguish
request/token exhaustion only when reliable metadata permits. No deliberate 429
hammering. Expose retry metadata; Phase 17C alone owns attempts, exponential backoff,
retry deadline and durable scheduling. Hints beyond the retry budget fail according
to policy. Do not sleep indefinitely or add a second retry loop.

Bound connect/read/generation execution as supported. Timeout may have consumed
provider tokens; record unknown usage. Normalize transient unreachable/server/timeouts,
auth/configuration, invalid responses, context/output limits, cancellation and
unknown failures into sanitized stable categories. Auth/config are non-retryable;
cancellation follows the ledger. Before each call check cancellation/lease where
possible. After response, cancelled or stale workers still cannot commit. Do not
claim an already-sent HTTP request is physically cancelled or refunded.

## Live scope and provider validation

Inspect configuration presence without printing values. Reuse existing credentials
and adapter; do not fetch/force new credentials, create deployments or change quota.
Only tiny synthetic non-sensitive material is permitted. Historical Phase 16 limits
must be respected; do not assume increased throughput or that HPA fixes provider quota.

Run local tests first; Foundry live validation is LAST. If configured/authorized,
perform only a deliberately small number: a chunk call, a reducer and a very small
end-to-end digestion, with valid evidence. Optionally observe a safely constrained
output budget or synthetic injection case; do not induce rate limits. Record exact
call count/types, success, role, safe model, usage, schema/evidence validation and
latency as observations. No 200/500/1,000-page live tests.

If Foundry credentials/configuration are unavailable, complete local contracts and
mark live validation BLOCKED, never fabricate success. OpenAI/vLLM live calls are
optional only when intentionally configured; no keys/accounts/credits/GPU downloads
are required. Precisely distinguish protocol compatibility from live validation.

Use qualifications, opposing statements, missing knowledge and injection fixtures
such as “Ignore previous instructions”, “Reveal another user's document”, forged
evidence and “Execute a tool”. No orchestration/tool changes are permitted and
invalid citations must fail validation. Real observations are not statistical quality
certification or semantic entailment proof. Explicitly defer semantic-support and
large-scale quality certification to 17H if not implemented.

## Required tests, order and review

Cover deterministic rendering/role/profile, valid JSON and stricter formatting
policy, malformed/schema-invalid/prose/truncated/fabricated evidence; sufficient/
insufficient/unknown context and output checks before transport; actual/absent/
partial usage, reservations, retries and unknown timeout outcomes; 429/retry-after
and durable rescheduling; timeout/no manifest; sanitized auth/config/model/server
errors; configurable compatible URLs, models, optional bearer auth, payloads,
non-streaming responses and optional usage for OpenAI/vLLM; capability variants;
RPM/TPM/concurrency/headroom/multiple-job fairness; checkpoint reuse/profile changes/
one manifest; pre-call cancellation and stale/in-flight rejection.

Run targeted 17E unit tests, compatible protocol tests, 17D tests, 17C tests,
provider/routing/streaming/API/retrieval regressions, complete project suite,
applicable compile/static/config and whitespace checks, then bounded live Foundry
only if configured. Rerun affected local tests if code changes after live work.
No local suite may require network services, clouds, keys, GPUs or OCR. Do not
claim checks passed unless executed; full-suite failure needs independently proven
pre-existing evidence to be excluded.

Self-review the complete incremental diff for duplicate providers, leaked provider
logic/secrets, ambiguous prompt boundaries, invented usage, duplicate retries,
worker-only quota claims, overflow/unbounded output, malformed acceptance, weakened
evidence, incompatible reuse, stale commits, rate-limit storms, assumed optional
fields, body logging/high-cardinality labels and prohibited infrastructure/publication.
Fix genuine findings. Separately review secrets, dependencies, paths, debug/temp/
generated files, dead code, docs and unintended APIs. No commit is part of review.

## Deliverables, acceptance and final report

Create this prompt and `docs/codex/reports/phase_17e_report.md`. Report executive
summary/result, starting state, scope, existing architecture, 17D integration,
profiles/roles/structured strategy/capabilities/bounds, execution result, usage/
accounting/admission/headroom/fairness, retry/429/timeouts/errors/cancellation/fences,
compatibility, Foundry/live evidence, OpenAI/vLLM protocol distinction, evidence/
quality/injection observations, observability/security, exact files, exact targeted/
regression/full/static outcomes, self/pre-commit findings, limitations, 17F gates
and Git state. Explain design and evidence, not only terse checklist entries.

PASS requires the above implemented contracts, strict authoritative evidence,
backward-compatible serving, explicit preflight/output limits, truthful durable
usage, shared admission/headroom/fairness, durable retry hints and one logical
checkpoint, model/profile invalidation, local compatible-provider tests, honest
Foundry success or unavailable-configuration BLOCKED disclosure, passing existing
17B–17D/provider/API/full/static checks and zero prohibited mutations/Git actions.
Only after PASS update README's 17A–17E completion status; never mark 17F started.

Record final status, tracked diff stat, incremental baseline inventory and no-index
whitespace checks for new files. Distinguish accumulated Phase 16, 17A, 17B, 17C,
17D work from 17E. Confirm prior work preserved except explained narrow compatibility
edits. Explicitly confirm commit NO, push NO, branch NO, staging NO; no capacity,
Azure/Kubernetes, publication, vLLM/GPU, OCR, new infrastructure or secret exposure.

Conclude **Phase 17E — PASS** only on the acceptance boundary above. This does not
mean live providers were validated when unavailable, production vLLM/GPU exists,
large-scale quality/reliability is certified, RAG publication/authentication exists,
or Phase 17 is complete. Exact next phase:
**Phase 17F — RAG Publication, Provenance & Interactive Document Analysis**.
**Do not start 17F. Do not commit. Do not push.**
