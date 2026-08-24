# Phase 8D Report — Observability & Inference Metrics

## 1. Phase Result

PASS

Phase 8D adds process-local Prometheus-compatible instrumentation for inference,
semantic application routes, and readiness while preserving the Phase 8A–8C
provider, API, streaming, retry, and request-correlation behavior.

## 2. Observability Architecture

The new `llm.metrics.Metrics` component owns a dedicated Prometheus collector
registry and concurrency-safe counters/histograms. Provider adapters surround
their existing operations with a provider-neutral observation object. They parse
only their own protocol telemetry into the typed `InferenceUsage` value; graph,
RAG, tools, memory, UI, and public API code do not parse provider payloads.

Instrumentation makes no extra network request, does not buffer a stream, and
does not change `InferenceProvider.generate()` or `generate_stream()` return
types. A dedicated registry avoids collisions with default/process collectors and
supports isolated test registries without duplicate registration on app imports.

## 3. Metrics Surface

`GET /metrics` returns the Prometheus text exposition content type and renders the
dedicated in-process registry. The endpoint only serializes collectors: it does
not invoke readiness, inference, retrieval, or a provider. Metric families are:

- `inference_requests_total`
- `inference_request_duration_seconds`
- `inference_time_to_first_token_seconds`
- `inference_stream_duration_seconds`
- `inference_errors_total`
- `inference_tokens_total`
- `application_requests_total`
- `application_request_duration_seconds`
- `readiness_checks_total`
- `readiness_check_duration_seconds`

No Prometheus server, Grafana, dashboard, alerting, or tracing service was added.

## 4. Inference Metrics

Every completed adapter operation records exactly one request outcome and one
duration observation. Dimensions are provider, logical role, configured served
model, operation (`generate` or `stream`), and outcome (`success` or `error`).
Failures additionally increment `inference_errors_total` with the Phase 8C
normalized category; raw messages and upstream bodies never become labels.

Histograms use fixed buckets from 10 ms through 120 seconds. Served model is safe
in this architecture because it is resolved from bounded startup configuration,
not a request field. Tool-only flows never call an adapter and therefore cannot
create an inference sample.

## 5. Streaming & TTFT

Streaming duration covers the adapter generator lifetime, including upstream
connection/setup, chunk iteration, and protocol termination. Outcome is an error
for normalized failures, malformed/incomplete streams, or early generator close.

TTFT starts immediately before the provider HTTP operation and is recorded once,
at the first non-empty content string actually yielded. OpenAI-compatible SSE
comments, assistant-role deltas, empty content, and usage-only chunks are ignored.
Ollama empty/final metadata chunks are also ignored. Failure before content does
not create a TTFT sample. Measurement observes in place and does not buffer,
duplicate, or delay chunks.

## 6. Token Usage & Throughput

`InferenceUsage` represents optional prompt, completion, and total counts. The
OpenAI-compatible adapter accepts non-negative integer fields from a response
`usage` object, including a usage-only streaming chunk. Ollama accepts its native
non-negative `prompt_eval_count` and `eval_count`; total is derived only when both
exact native counts exist. Booleans, negative values, malformed fields, and absent
usage are ignored. Usage is recorded at most once per operation, and no local
tokenizer or estimated count is used.

No tokens-per-second gauge is stored. Standard monitoring can derive throughput
from the completion-token counter rate together with observed operation timing;
when completion usage is absent, no throughput claim is possible.

## 7. Readiness & Route Metrics

Each `/ready` invocation records the returned provider/status outcome and elapsed
discovery time after the existing readiness operation completes. `/metrics` never
triggers `/ready`. Application counters and duration histograms cover `query` and
`stream` operations with `rag`, `direct`, `tool`, or sanitized `unknown` route and
success/error outcome. Tool requests appear at the application level but not as
inference.

## 8. Cardinality & Security Review

Allowed labels are:

- provider;
- logical role;
- configured served model;
- operation;
- outcome;
- bounded semantic route;
- normalized error category;
- fixed token type.

Unknown application routes are collapsed to `unknown`. Request IDs, session IDs,
queries, prompts, source filenames, document content, URLs, exception messages,
credentials, and upstream response bodies are not labels or metric values. Tests
rendered the registry with private prompt/error fixtures and confirmed they were
absent. Because the app has no authentication layer, production deployments
should restrict `/metrics` at the network or ingress boundary.

## 9. Request Correlation & Logging

Metrics remain aggregate and contain no request ID. Existing `X-Request-ID`
generation/validation and streaming context restoration remain intact. Completion
logs carry the request ID plus provider, role, configured model, operation,
outcome, duration, TTFT-recorded state where applicable, and normalized error
category. Application completion logs contain request ID, route, operation,
outcome, and duration. The former request logger that printed/wrote queries and
session IDs was replaced with safe operational logging, eliminating prompt and
session-content exposure and duplicate success events.

## 10. Files Changed

Modified:

- `README.md`
- `api/app.py`
- `llm/inference.py`
- `llm/ollama_client.py`
- `llm/openai_compatible.py`
- `requirements.txt`
- `tests/unit/test_api_reliability.py`
- `utils/logger.py`

Added:

- `llm/metrics.py`
- `tests/unit/test_observability.py`
- `docs/codex/prompts/phase_8d.md`
- `docs/codex/reports/phase_8d_report.md`

Deleted:

- None.

## 11. Tests Added / Updated

Observability tests cover successful and failed inference counters, duration
histogram observations, normalized error categories, raw-error exclusion, TTFT
with metadata/empty chunks, exactly-once TTFT, failure-before-token behavior,
partial stream outcome, OpenAI-compatible non-streaming/streaming/absent usage,
Ollama native usage, readiness metrics, route bounding, forbidden-label review,
Prometheus endpoint format/provider independence, and tool-only inference
exclusion. Existing provider and orchestration regression tests remain unchanged
and passing.

## 12. Validation Results

- `python -m pytest -q`: 96 passed in the final validation run.
- `PYTHONPYCACHEPREFIX=/tmp/polymind-phase8d-pycache python -m compileall -q .`: passed.
- `git diff --check`: passed.
- `docker compose config --quiet`: passed.
- `docker build .`: passed using normal cache behavior; no `--no-cache` and no
  additional validation tag were used.
- Linting: no configured linter or formatter was found.
- Metrics security inspection: passed through rendered-output tests and explicit
  label/source scans; no prompt, request/session ID, raw error, credential, or
  document label exists.

## 13. Implementation Self-Review

Architecture review confirmed that provider-specific usage parsing remains in
adapters and no observability logic entered RAG/business routing. Request and
duration metrics finish once, TTFT observes only actual content, streams remain
incremental, and exact usage remains optional.

The review found and fixed four issues: duplicate provider success logs were
removed; application success is set only after response serialization data is
constructed; repeated usage chunks cannot double-count an operation; and Python
booleans are rejected as token counts. It also corrected endpoint content-type
construction so the Prometheus media type is returned exactly.

Compatibility review found no `/query` response change, no NDJSON event change,
no request-ID or readiness response change, no generation retry, and no Ollama or
external OpenAI-compatible architecture regression.

## 14. Pre-Commit Review

The working tree contains only scoped Phase 8D implementation, tests,
documentation, and the one direct dependency addition. Secret/debug/TODO scans
found no new credential, private key, runtime `.env`, hard-coded local path,
temporary artifact, debug print, TODO, or dead code. Fake credentials in existing
provider tests and pre-existing experiment/semantic-router print statements were
recognized as non-production fixtures/pre-existing findings. Existing ignored
`.env` and bytecode files were not modified or added.

Public API payloads and Docker/Compose topology are unchanged. The only dependency
change is `prometheus-client==0.26.0`, a small official client; the Docker build
confirmed compatibility. The build also reconfirmed the pre-existing large
CUDA/ML dependency footprint, which this phase did not expand beyond the metrics
client.

No commit was created.
No push was performed.

## 15. Documentation

README now documents the metrics endpoint, families, TTFT definition, exact usage
rules, throughput derivation, provider differences, route/readiness coverage,
bounded labels, security boundary, instrumentation-only scope, and single-process
registry limitation. The clean Phase 8D prompt and this report are stored under
`docs/codex/`.

## 16. Remaining Risks / Technical Debt

Phase 8D metrics are process-local. The current single-worker Uvicorn commands are
compatible, but a future multi-worker/multi-replica deployment must use supported
multiprocess collection or scrape and aggregate individual processes. Metrics are
not authenticated inside the application and need production network protection.
Provider token usage remains unavailable when an upstream omits it, intentionally.
No dashboards, alert rules, durable history, tracing, or multi-host aggregation
exist; all are deliberately deferred external infrastructure.

Separately, the repository's pre-existing pinned ML stack makes Docker images and
dependency rebuilds very large, including CUDA packages. Phase 8D did not redesign
or add to that stack other than the small metrics client.

## 17. Phase 8E Readiness

READY

Phase 8D preserves the provider-neutral control-plane boundary and supplies
quantitative per-process behavior without coupling memory to metrics. Externalized
Memory / Multi-Replica Readiness can proceed. Phase 8E should account for the
documented fact that metrics and the current file-backed memory are process-local;
metrics aggregation itself remains outside the memory phase unless explicitly
scoped.
