# Phase 17E — Managed Inference Integration

Date: 2026-10-07. Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`.
Branch: `master`. Authority: [finalized phase prompt](../prompts/phase_17e.md).
Foundations: [17A](phase_17a_report.md), [17B](phase_17b_report.md),
[17C](phase_17c_report.md), [17D](phase_17d_report.md).

## 1. Executive summary

The hierarchical digestion workflow now has an implementation of its synthesis
boundary that invokes the existing inference providers. It renders deterministic
control/data-separated requests, enforces configured capability and output limits,
records durable quota reservations and optional provider usage, and returns bytes
to the unchanged Phase 17D evidence/schema validator. Existing Phase 17C fencing
and immutable manifest acceptance remain authoritative.

OpenAI-compatible and Ollama providers gain an additive bounded `execute()` method.
Existing generate, streaming, readiness, role routing, API, RAG and model selection
behavior are preserved. A SQLite reference admission adapter coordinates processes
sharing the same local authority, quota key and policy. It is not an AKS deployment.

## 2. Phase result

**Phase 17E — PASS**, under the prompt's explicitly permitted unavailable-live-
configuration path. **Foundry live validation: BLOCKED.** No endpoint, model map,
provider selection or API key was present in the operator process or repository
`.env`. No credentials were fetched or fabricated. **Live Foundry calls: 0**.
OpenAI and vLLM live validation were not performed. Their **protocol compatibility
is validated**, not live operation or model quality.

The complete suite passed **543 tests in 50.34 seconds**, including **97 new tests**.
This establishes application integration and deterministic local contracts. It does
not establish real-model semantic quality, production shared quota infrastructure,
large-document reliability, publication, authentication or Phase 17 completion.

## 3. Starting worktree state

HEAD: `f9b47fda4658935b64826f1d4abe0488c64f21ae`. Before edits:

```text
## master...origin/master
 M README.md
 M docs/codex/reports/phase_16_report.md
?? docs/codex/prompts/phase_17a.md
?? docs/codex/prompts/phase_17b.md
?? docs/codex/prompts/phase_17c.md
?? docs/codex/prompts/phase_17d.md
?? docs/codex/reports/phase_17a_report.md
?? docs/codex/reports/phase_17b_report.md
?? docs/codex/reports/phase_17c_report.md
?? docs/codex/reports/phase_17d_report.md
?? documents/
?? tests/integration/
?? tests/unit/documents/
```

`/tmp/polymind-phase17e-baseline` contains exact copies and SHA-256 hashes of all
**213 tracked/unignored files**, plus initial status, HEAD, tracked stat and empty
index diff. Initial tracked changes were **1,674 insertions / 1 deletion** across
README and the Phase 16 report. Those accumulated edits are not Phase 17E changes.

## 4. Scope and exclusions

Implemented managed synthesis, prompts/profiles, capability checks, additive provider
results, bounded transport, shared reference admission/accounting, retry hints,
fenced workflow integration and local tests. No dependency was added. No public
endpoint, worker deployment, scheduler daemon, cloud SDK or second provider stack
was introduced. RAG, Chroma, BM25, Redis, API/UI, Docker and deployment files are
unchanged. No cloud/cluster operation, capacity change, external OCR, model download,
vLLM/GPU installation, paid infrastructure or live model consumption occurred.

## 5. Existing inference architecture

`InferenceProvider` retains name, model_id, readiness, generate, generate_stream and
close. `create_inference_provider()` still selects existing Ollama/OpenAI-compatible
adapters from the same settings and logical maps. The optional
`StructuredInferenceProvider` protocol extends that boundary with execute; legacy
third-party providers remain valid for interactive work but fail safely if selected
for managed synthesis without bounded generation support.

Provider transport/auth and protocol-specific payloads remain in `llm/`. The new
`bounded_http` helper is shared by the existing adapters; it is not another client,
factory, credentials mechanism or independent Foundry/OpenAI/vLLM stack.

## 6. Phase 17D integration

`ManagedSynthesisInference.analyze(StageRequest) -> bytes` implements the established
contract. A small protected execution hook in DigestionHandler permits its managed
subclass to bind durable job/step/attempt context. The base fake path is unchanged.
The handler always sends returned bytes through existing `validate_result()` before
building Checkpoint, inherited annotations or final manifests.

No changes were made to StageRequest, StageResult, evidence validation, planning,
canonical extraction, checkpoint schemas, coverage or immutable object storage.
The integration tests include a complete existing OpenAI-compatible provider →
mocked HTTP → 17D → 17C workflow using real local PDF extraction.

## 7. Managed synthesis adapter

The adapter receives an existing provider, explicit ManagedSettings and an
InferenceAdmissionPort. It binds the managed configuration fingerprint into a
DigestionProfile before planning. Each executing stage creates a context-bound
adapter view rather than mutating shared provider generation settings. Preflight
and active-fence checks precede admission and transport. The admitted call has a
durable unknown observation before the network request can occur.

Construction does not invoke inference or readiness. There is no fallback from
bounded execution to unbounded legacy generate, and no automatic model replacement.

## 8. Prompt/profile architecture

Four StageProfiles distinguish chunk analysis, intermediate reduction, structural
reduction and root synthesis. Each carries `managed-stage/1`, `managed-prompt/1`,
`stage-result/1`, an input/output budget and
`retain-evidence-qualifications-conflicts/1`. Structural selection uses the final
reducer for a structural parent; earlier batching levels are intermediate. Root
selection is explicit from the immutable plan. All four are exercised end-to-end.

The system message contains only application control, schema, approved IDs/links
and bounds. The user message separately names UNTRUSTED_DOCUMENT_DATA,
UNTRUSTED_STRUCTURAL_PATH and GENERATED_CHILD_MATERIAL. Source text cannot become
system instructions. Stable claim IDs are supplied in required positional order;
models must select them, not derive UUIDs. Every required child link is supplied.
Request construction is deterministic; no tool definitions or tool executor exist.

## 9. Provider-neutral model roles

All four profiles use existing **summarization**. Phase 17D already restricts its
profile role to summarization, and neither fast nor general has demonstrated a
quality advantage for this workflow. Retaining the role avoids an unnecessary
schema change and unverified cheaper-model substitution. The provider's existing
role map supplies the served identifier; no deployment names enter domain profiles.
This is a conservative policy choice, not a measured model-quality conclusion.

## 10. Structured-output strategy

Configured modes are prompt-only JSON, JSON-object mode and JSON-schema mode.
OpenAI-compatible execute translates these to response_format where supported;
Ollama translates them to its existing endpoint's format/options conventions.
Schema mode does not assume every endpoint supports strict native enforcement.
Application validation remains mandatory in every mode.

The response policy is deliberately exact: no fence stripping, prefix removal or
repair. Markdown fences, extra prose, duplicate keys, truncated/malformed JSON,
unknown fields and invalid evidence fail. Native refusal/tool/length finish reasons
are not accepted as complete results. Only complete non-streaming content proceeds.

## 11. Capability model

`CapabilityProfile` requires explicit context capacity, maximum output, provider
message overhead, safety margin and a version. It also records structured-output,
streaming and usage capabilities, optional supported temperature, output parameter
selection and a returned-model allowlist for versioned identities versus aliases.
These are deployment-verified or deliberately conservative **operator-configured
bounds**. The implementation never infers model capacity from a name and ships no
purported Foundry capability default. Missing required metadata fails construction.

ManagedSettings uses `DOCUMENT_INFERENCE_` with nested settings support. Profiles
and capability are mandatory; request bytes default to 256,000, allowed evidence
count to 256, and total response deadline to 60 seconds. A caller must still select
appropriate lower production/live limits. The request maximum is not a quota grant.

## 12. Context and output validation

Phase 17D's deterministic planning check runs first and revalidates serialized
StageRequest. The rendered control, data and schema are measured as ASCII JSON
bytes, conservatively counted as estimated tokens. Overhead and safety margin are
added separately. Stage input, rendered bytes, allowed evidence cardinality and
configured model capacity are checked before admission/transport. The entire
configured stage maximum must also fit capability during settings validation.

Output requested from the provider cannot exceed its capability or the Phase 17D
planning reservation. Raw HTTP bytes have a derived bound of six times content
bytes plus 8,192 bytes for protocol metadata; UTF-8 content has the 17D result-byte
bound. The existing validator additionally bounds normalized serialized size,
claims, strings and annotations. Overflow fails; neither input nor output is
silently truncated. Context estimates are intentionally conservative, not measured
tokenizer counts or claimed actual provider usage.

## 13. Usage representation

Existing InferenceUsage carries optional exact prompt, completion and total token
counts. OpenAI-compatible usage parsing still accepts only nonnegative integers;
missing or malformed fields remain unknown. Ollama retains its existing exact
native-count behavior, deriving total only when both counts exist.

Each admission row separately stores estimated input and reserved output. It never
replaces them with actual usage, refunds reservations based on small observed usage,
or records a timeout as zero tokens. Partial provider usage remains partial. A
parsed length-rejected response can retain actual usage even though no checkpoint
is accepted. A response lost before parsing has unknown usage.

## 14. Additive execution result

GenerationRequest contains system/data messages, role, explicit capability, bounded
output/content size, schema and deadline. GenerationResult contains text, optional
InferenceUsage, safe configured/returned served model and optional finish reason.
Errors use existing provider-neutral exceptions plus configuration/context/output
categories; rate-limit errors add optional retry_after. Existing text/stream return
types and callers remain unchanged.

Document execution deliberately does not inherit arbitrary interactive generation
parameters, including tools or enormous max_tokens. It uses explicit immutable
request settings. Temperature is omitted by default; zero/low temperature is sent
only when configured as supported. It does not promise identical generated bytes.

## 15. Per-job accounting

SQLite inference_calls stores quota identity, scoped job/step/attempt identity,
stage profile, provider, role, configured model, capability version, start time,
estimated input, reserved output, active state, sanitized outcome and nullable
actual usage. A uniqueness constraint prevents a second admitted execution for
one scoped step attempt. Repeated attempts produce separate rows; resumed accepted
checkpoints produce no fictitious new usage rows.

Transport success is distinct from checkpoint acceptance. Invalid evidence can
have known billed usage while the workflow rejects its manifest. Usage rows are
observations, never acceptance authority. Scoped records access is for trusted
operators, not a production user-authorization API. Job attempts also record
admission/429 failures; a quota denial does not fabricate a provider call row.

## 16. Admission architecture

InferenceAdmissionPort defines acquire and finish. SQLiteInferenceAdmission uses
short BEGIN IMMEDIATE transactions, separate connections and durable policy/call
rows. Two adapters/connections compete atomically; no Python semaphore or worker
mutex owns quota. All workers for one provider quota must share the same database,
quota key and policy. Reopening with a conflicting policy or incompatible schema
fails safely. The reference database is separate from the unchanged 17C v1 schema.

This is **single-host multi-process reference coordination**, not a distributed
AKS backend. A production shared database/service implementation must preserve the
port's atomic semantics and use one authoritative quota scope across all replicas.
No Redis, Azure resource or migration infrastructure was provisioned.

## 17. RPM and TPM reservations

A rolling 60-second window counts admitted calls and input-plus-output reservations.
Completed errors and small actual responses retain their full window reservation.
Concurrency counts active rows independently of the rolling window. A request that
cannot fit its workload token partition is rejected as configuration, rather than
retried forever. Contention returns a bounded 60-second retry hint without sleeping.
Shared quota policy is explicit operator input; no capacity is inferred from HPA.

## 18. Interactive headroom and fairness

Policy reserves positive RPM, TPM and concurrent slots for INTERACTIVE; document
calls cannot consume that portion. Per-job concurrent and rolling request limits
provide basic fairness. Tests prove two jobs can progress, one cannot take every
background slot, and interactive admission remains possible after the document
partition fills. This is not round-robin scheduling or a starvation-free SLO.

Existing interactive API calls are not automatically routed through this new
admission authority; preserving that API behavior is intentional. Background work
is capped below total configured quota regardless. The port represents interactive
reservations for a future coordinated deployment, but **uncoordinated interactive
or external clients can still exhaust upstream quota**. Global enforcement applies
to participating callers, not every consumer of an independently operated account.

## 19. Retry and rate-limit handling

HTTP 429 maps to the existing overloaded category and carries sanitized Retry-After
seconds or HTTP-date metadata. Invalid hints are ignored; very long finite hints
are clamped to the maximum supported job retry window, causing deadline exhaustion
rather than an early retry. No response body is inspected to guess token versus
request exhaustion; absent reliable distinction, the category is generic overload.

Failure gains optional retry_after. The only scheduling change is
`max(existing exponential delay, retry_after)`, followed by the original attempt
and deadline checks. Not-before is persisted by the same 17C transaction and outbox.
Tests prove 23-second hints survive scheduling, retries accept one manifest, and
hints exceeding a 10-second job budget cause retry_exhausted. No provider retry or
second scheduler exists. Admission denials consume bounded workflow attempts too.

## 20. Timeout semantics

Existing provider connect/read settings bound network phases. Bounded execution
also checks a monotonic deadline while reading the response; one-byte body reads
prevent slow trickles hiding inside a large buffered read. A socket read timeout
wrapped by requests is normalized as timeout. Responses close on all paths.

The deadline is cooperative around synchronous requests, not hard OS preemption:
DNS/connect behavior and an in-progress read can extend observed wall time by the
underlying network timeout. Worker leases must be sized above the bounded call and
validation time or renewed by supervision. No heartbeat daemon was added. A timed-
out HTTP call may still execute upstream; neither physical cancellation nor a
refund is promised. Usage remains unknown unless actually received.

## 21. Error normalization

Managed classification maps overload, timeout and unreachable/server failures to
retryable inference_rate_limited, inference_timeout and inference_unavailable.
Authentication, configuration/model mismatch, invalid protocol, context and output
limits are non-retryable. Unknown errors remain sanitized and non-retryable.
HTTP 400/422 become configuration failures without reflecting upstream body text;
500 is transient unavailable, while existing 502/503 overload behavior is retained.
No new interactive status mapping or readiness vocabulary was required.

## 22. Cancellation and fencing

Before admission and again immediately before transport, the managed handler renews
its existing lease through the ledger, checking ownership, fence, expiry and
cancellation. Cancellation can still race with sending an HTTP request; this is
explicitly not an exactly-once external execution boundary.

After response, existing IntentStore registration and manifest commit reject stale,
expired or cancelled work. Integration tests cancel or expire a lease while the
provider response is in flight: actual usage is retained, but no stage manifest is
accepted. Prior accepted checkpoints remain intact. No new cancellation scheduler
or physical upstream cancellation claim was added.

## 23. Checkpoint compatibility and reproducibility

The existing inference_config fingerprint now binds managed settings, stage
versions/budgets/schema/template/constraints, capability metadata, provider family
and configured served model. This flows through existing plan, step and dependency
hashes. Model, prompt-profile or capability-version changes invalidate reuse in
integration tests. Operator version changes are required when an alias silently
points to a newly deployed model; local metadata cannot detect such remote changes.

Actual usage, attempts, latency and returned observations do not change semantic
checkpoint identity. Accepted artifacts are reused byte-for-byte. An unaccepted
retry may produce different model text and may be billed twice. The guarantee is
one accepted logical manifest, not identical real-model execution.

## 24. Azure Foundry integration

The same configured OpenAI-compatible provider can target Foundry's compatible
base URL and role map. Its bounded path supports explicitly selected
max_completion_tokens instead of max_tokens, omitted unsupported sampling, optional
JSON response modes and configured returned-model aliases. Existing bearer-secret
configuration/factory is reused. No Foundry-specific client or domain condition was
introduced. Compatibility is tested with a synthetic managed endpoint shape.

Historical Phase 16 evidence records a deployment with **10 RPM / 10,000 TPM**.
That history is not evidence of present capacity or current credentials. No fresh
Azure inspection or quota change occurred. Conservative full-JSON reservations can
exceed that small quota; configure fitting stages or fail preflight, never bypass
admission to force a live success.

## 25. Foundry bounded live validation

After the full local suite, presence-only inspection of the current process and
repository `.env` found all four inference selection/base URL/key/model-map settings
absent. Only booleans were emitted, never values. The default local configuration
is not an intentionally configured Foundry target. Evidence is recorded outside
the repository in `/tmp/polymind-phase17e-live-status.json`.

**BLOCKED — credentials/endpoint/model configuration unavailable locally.** Exact
call counts: chunk **0**, reducer **0**, end-to-end **0**, constrained-output **0**,
injection **0**, quota probes **0**. No cloud secret retrieval, deployment discovery,
capacity increase or forced credential setup occurred. Phase 16 live evidence is
not reused as proof of Phase 17E live digestion.

## 26. OpenAI-compatible protocol validation

Mocked HTTP contract tests verify configured base URL/model mapping, system/user
message separation, bounded non-streaming payloads, prompt/JSON-object/schema
capabilities, optional usage, response-model allowlists, cleanup, raw/content limits,
429/retry-after, timeout including wrapped read timeout, slow response deadline,
authentication/configuration/server errors, malformed JSON and unexpected models.

A separate integration drives the existing OpenAICompatibleProvider through the
entire durable synthetic PDF digestion workflow. This proves provider reuse plus
real application validation, not an independently generated checkpoint fixture.

## 27. OpenAI compatibility

OpenAI-style `/v1/chat/completions` request/response shapes pass local contract tests.
No OpenAI key, account or credits were required. **Live OpenAI validation: not
performed.** This does not claim every model accepts every optional parameter;
capability/output-parameter/response-model configuration remains explicit.

## 28. External vLLM compatibility

Configurable external base URL, served alias, optional/required bearer header,
max_tokens, non-streaming choices/message, optional usage and normalized errors
pass local tests. **External vLLM protocol compatibility validated; live vLLM not
performed.** No vLLM package, model download, server, container, GPU or AKS resource
was installed or operated.

## 29. Evidence-validation results

The managed path rejects fabricated evidence through unchanged Phase 17D validation.
An integration shows known provider usage alongside invalid_reference terminal
failure and no accepted stage manifest. The full existing 17D suite additionally
covers foreign scope/version/extraction, parent-unavailable IDs, wrong lineage,
coverage gaps and immutable resume. No validator rule was relaxed for real models.
The successful synthetic PDF pipeline preserves six original evidence references
and full structural coverage. No real-model evidence result was observed live.

## 30. Qualification/contradiction observations

Existing 17D deterministic tests still prove application-owned qualification and
contradiction inheritance across reducers. Managed prompts request retention, and
required links prevent silently dropping child claims. **Live quality observations:
none**, because no live target was configured. Semantic entailment and natural-
language contradiction quality remain explicitly deferred to Phase 17H. Valid
citation IDs do not certify claim truth, and synthetic responses are not a quality
benchmark.

## 31. Prompt-injection boundary

The adapter test source contains ignoring instructions, forged evidence and tool
execution directives. It proves these remain in the untrusted user-data message,
not system control; no tool parameter is exposed. Forged responses fail downstream
validation. Existing 17D adversarial tests remain passing. **Live prompt-injection
test: not run.** Prompt wording is not presented as a semantic security guarantee.

## 32. Observability and accounting

Bounded provider execution reuses existing inference request/duration/error and
actual-token metrics with existing provider/logical-role/configured-model labels.
No job, document, owner, endpoint, filename, evidence or text label was added.
Detailed reservations, unknown usage and retry amplification are available through
scoped durable call rows and existing workflow attempt records. Monetary prices,
billing, dashboards and a separate worker metrics platform are out of scope.

## 33. Security/secrets and pre-commit review

Reviewed changed/new source, tests and documentation for credentials, raw response
logging, source exposure, tool payloads, unsafe identifiers, debug code, runtime
paths, generated files, dependencies and API changes. Only synthetic credentials
appear in protocol fixtures. No real `.env`, DB, private document, model artifact,
key, response content or temporary log was added to the Git inventory. New database
files use private mode in an explicit operator-controlled directory; obvious
symlinks/special files and incompatible schemas fail closed. This is not hostile-
host filesystem protection or production tenant authorization.

Prior prompts/reports and all prior tests are preserved. The only old document
implementation edits are a narrow execution-context hook, additive failure metadata
and retry-delay handling. Separate baseline/whitespace/link checks are recorded in
the final audit below. No staging or commit is part of this review.

## 34. Exact files created and modified

Created **9 files**:

```text
documents/digestion/managed.py
llm/admission.py
llm/bounded_http.py
llm/structured.py
tests/integration/test_managed_digestion.py
tests/unit/documents/test_managed_inference.py
tests/unit/test_structured_provider.py
docs/codex/prompts/phase_17e.md
docs/codex/reports/phase_17e_report.md
```

Modified **7 existing files**:

```text
README.md
documents/digestion/workflow.py
documents/jobs/errors.py
documents/jobs/sqlite.py
llm/inference.py
llm/ollama_client.py
llm/openai_compatible.py
```

README receives only the cumulative phase status/report/configuration pointer.
The three earlier document files receive the narrowly justified compatibility
changes described above; their prior artifacts remain readable, with no schema
migration. All other baseline bytes, including the Phase 16 report and 17A–17D
prompts/reports/tests, remain unchanged.

## 35. Targeted tests

Final targeted local runs after review fixes:

| Command | Result |
| --- | --- |
| `python -m pytest tests/unit/documents/test_managed_inference.py -q` | **35 passed in 1.09 s** |
| `python -m pytest tests/unit/test_structured_provider.py -q` | **51 passed in 0.20 s** |
| `python -m pytest tests/integration/test_managed_digestion.py -q` | **11 passed in 7.12 s** |
| `python -m pytest tests/unit/documents/test_digestion.py tests/integration/test_document_digestion.py -q` | **66 passed in 22.08 s** |
| `python -m pytest tests/unit/documents/test_job_ledger.py tests/integration/test_document_jobs.py -q` | **95 passed in 2.91 s** |

Logs are outside the repository under `/tmp/polymind-phase17e-*.log`. Existing 17D
and 17C focused runs preceded final transport-only review fixes; the final full
suite reran them with all final source changes. Counts overlap and must not be added
to the full-suite count. No tests use a live provider or cloud service.

## 36. Provider/API regression tests

**159 passed in 0.79 seconds** across provider contracts, OpenAI-compatible, Ollama,
model routing, streaming orchestration, API reliability, readiness, retrieval,
vector storage and observability. Command:

```bash
python -m pytest tests/unit/test_provider_contract.py tests/unit/test_openai_compatible_provider.py tests/unit/test_ollama_provider.py tests/unit/test_model_routing.py tests/unit/test_streaming_orchestration.py tests/unit/test_api_reliability.py tests/unit/test_provider_readiness.py tests/unit/test_retrieval_regression.py tests/unit/test_vector_store.py tests/unit/test_observability.py -q
```

## 37. Full-suite and static validation

`python -m pytest -q`: **543 passed in 50.34 seconds**, no failures or skips.
This is the starting 446 tests plus 97 Phase 17E cases. The final full run includes
all self-review source fixes. No implementation changed after this run.

`PYTHONPYCACHEPREFIX=/tmp/polymind-phase17e-pycache python -m compileall -q .`,
`docker compose config --quiet` and `git diff --check` passed. External bytecode
cache avoids unrelated ownership changes. New untracked files receive additional
no-index whitespace and EOF checks. No configured formatter/linter/type checker
was found in the existing project workflow; none was installed. Docker build was
not needed because dependencies, Dockerfile, images and deployment configuration
were unchanged. No Kubernetes validation or mutation was needed.

## 38. Implementation self-review findings

Reviewed all incremental code and the provider/worker/validator interfaces. Fixed:
reported usage lost on length-rejected output; requests-wrapped read timeouts;
large buffered reads hiding slow trickles from deadline checks; overload Retry-After
hints on HTTP 502/503; overly long valid
retry hints being discarded; and admission opening an incompatible unrelated
SQLite database. Added focused regressions for each. Kept bounded response reading
inside the provider layer and retained exact downstream validation.

Checked that per-call settings never mutate interactive parameters, reservations
precede transport, unknown cost survives missing responses, failed results cannot
commit, model/profile changes invalidate reuse, and no provider-specific condition
entered document logic. No evidence/schema weakening, retry loop, automatic repair,
cloud mutation or retrieval publication was introduced.

## 39. Remaining limitations and operational setup

Real Foundry integration still needs the explicitly blocked bounded live run once
an already authorized endpoint/model/key and conservative capabilities are available.
Model quality, semantic entailment, large documents, reliability certification,
production shared admission, authentication and cost policy remain unproven.

Unfinished admission rows retain concurrency indefinitely rather than assuming a
crashed worker means its external call stopped or cost zero. An authorized operator
must establish termination and settle the ticket as unknown with `finish()` before
reclaiming that slot. No automatic abandoned-call recovery/retention daemon is
implemented. This favors safety over availability and is a production-adapter gate.
The rolling limiter does not guarantee upstream quota windows exactly match it;
upstream 429 still takes the durable retry path.

To wire trusted application execution, use the existing provider factory, explicit
ManagedSettings, one shared SQLiteInferenceAdmission per quota authority, and
`managed.profile(planning_profile)` **before** prepare/admit. Execute with
ManagedDigestionHandler and Worker(classifier=classify_managed). Keep ledger leases
longer than network/validation time or supervise renewal. Store both databases and
objects in operator-controlled paths, never in source control. Example composition:

```python
provider = create_inference_provider(provider_settings)
managed = ManagedSynthesisInference(provider, ManagedSettings(), admission)
plan, plan_ref = prepare(artifact, extraction_ref, managed.profile(planning_profile), store)
job = admit(ledger, store, plan, plan_ref, request_key=request_key)
handler = ManagedDigestionHandler(ledger, plan_ref, managed)
worker = Worker(ledger, dispatcher, store, handler,
                owner=worker_identity, classifier=classify_managed)
# Existing relay/worker/reconciliation supervision controls execution.
# The caller owns provider.close() and durable resource lifetimes.
```

ManagedSettings loads explicit `DOCUMENT_INFERENCE_CAPABILITY` and
`DOCUMENT_INFERENCE_PROFILES` JSON or nested environment settings. Admission path,
quota key and AdmissionPolicy are explicit constructor inputs; there are no
implicit quota or database defaults. Capability/output-parameter support must be
verified for the actual deployment. Do not copy synthetic test sizing as production
capacity, expose trusted scope as authentication or assume new API endpoints exist.

## 40. Exact Phase 17F prerequisites

The exact next phase is **Phase 17F — RAG Publication, Provenance & Interactive
Document Analysis**. It can consume accepted immutable digest/checkpoint artifacts,
original evidence references, explicit COMPLETE/PARTIAL outcomes, versioned managed
profiles and durable execution/accounting. It must implement publication selection,
coherent dense/BM25 generations, provenance-preserving retrieval/citations and
interactive document analysis without mistaking generated summaries for sources.

Keep the blocked live Foundry/quality gate visible, retain 17G identity/cost and
17H quality/reliability gates, and do not claim public access or production shared
state. No Phase 17F implementation has started.

## 41. Git/no-commit state and worktree accounting

Prior work is not attributed to this phase: Phase 16 contributes its closure report;
17A its prompt/report and initial roadmap; 17B canonical document/storage/extraction
modules and tests; 17C jobs/ledger/worker/tests; 17D planning/evidence/digestion/tests.
Those files remain present. Only the three explicitly listed 17C/17D compatibility
files and cumulative README differ from their phase-start snapshots; all earlier
reports, tests and other implementation bytes remain unchanged.

Commit created: **NO**. Push performed: **NO**. Branch created: **NO**.
Files staged: **NO**. Prior Phase 17 work preserved: **YES**, with the three named,
reviewed additive compatibility edits and cumulative README update.

Foundry capacity change **NO**; Azure resource mutation **NO**; Kubernetes mutation
**NO**; RAG publication **NO**; vLLM deployment **NO**; GPU provisioning **NO**;
external OCR **NO**; new paid infrastructure **NO**; live inference consumption
**NO**; secret exposure **NO**. Phase 17F not started. All work remains uncommitted
for the operator's full Phase 17A–17I review.

Final baseline audit: **206 of 213 prior files byte-identical**, with exactly the
seven listed intentional modifications. Incremental existing-file diff against
the outside snapshot:

| File | Added | Removed |
| --- | ---: | ---: |
| README.md | 12 | 6 |
| documents/digestion/workflow.py | 5 | 1 |
| documents/jobs/errors.py | 6 | 1 |
| documents/jobs/sqlite.py | 2 | 1 |
| llm/inference.py | 16 | 0 |
| llm/ollama_client.py | 41 | 0 |
| llm/openai_compatible.py | 41 | 0 |

Nine new files are additional to those counts. The outside audit is
`/tmp/polymind-phase17e-audit.json`; the existing-file incremental diff is
`/tmp/polymind-phase17e-incremental.diff`. No-index whitespace, EOF, relative-report
links, secret-pattern heuristics, unchanged HEAD/master and empty index checks
passed. These are scoped engineering checks, not a security certification.

Final tracked `git diff --stat` includes accumulated prior work and excludes all
untracked files:

```text
 README.md                             |   50 +
 docs/codex/reports/phase_16_report.md | 1631 ++++++++++++++++++++++++++++++++-
 llm/inference.py                      |   16 +
 llm/ollama_client.py                  |   41 +
 llm/openai_compatible.py              |   41 +
 5 files changed, 1778 insertions(+), 1 deletion(-)
```

Final `git status --short --branch`:

```text
## master...origin/master
 M README.md
 M docs/codex/reports/phase_16_report.md
 M llm/inference.py
 M llm/ollama_client.py
 M llm/openai_compatible.py
?? docs/codex/prompts/phase_17a.md
?? docs/codex/prompts/phase_17b.md
?? docs/codex/prompts/phase_17c.md
?? docs/codex/prompts/phase_17d.md
?? docs/codex/prompts/phase_17e.md
?? docs/codex/reports/phase_17a_report.md
?? docs/codex/reports/phase_17b_report.md
?? docs/codex/reports/phase_17c_report.md
?? docs/codex/reports/phase_17d_report.md
?? docs/codex/reports/phase_17e_report.md
?? documents/
?? llm/admission.py
?? llm/bounded_http.py
?? llm/structured.py
?? tests/integration/
?? tests/unit/documents/
?? tests/unit/test_structured_provider.py
```
