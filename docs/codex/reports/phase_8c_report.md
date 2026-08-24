# Phase 8C Report — Reliability, Readiness & Error Handling

## 1. Phase Result

PASS

Phase 8C adds provider-neutral readiness, bounded readiness-only retries,
operational error classification, request correlation, and reliability tests while
preserving both inference adapters and the existing query/NDJSON boundaries.

## 2. Reliability Architecture

`InferenceProvider` now has one narrow `check_readiness()` operation returning a
sanitized `ReadinessResult`. Provider protocol details remain in their adapters:
OpenAI-compatible discovery uses `/models`; Ollama discovery uses `/api/tags`.
Provider construction remains network-free, so an unavailable inference service
does not prevent API startup. No vLLM runtime or failover behavior was added.

## 3. Liveness & Readiness

The existing root endpoint remains compatible. `GET /health` reports process
liveness without contacting inference. `GET /ready` returns HTTP 200 only when the
provider responds with a valid discovery payload and all configured logical-role
models are present. It returns HTTP 503 with a sanitized status for unreachable,
timeout, authentication, overload, missing-model, protocol, or upstream failures.
Neither readiness implementation generates tokens.

## 4. Error Taxonomy

The small taxonomy covers provider unreachable, timeout, authentication,
rate/overload, model unavailable, malformed protocol, and generic upstream
failure. HTTP 401/403 map to authentication, 404 to model unavailable for
generation, 408/504 to timeout, 429/502/503 to overload, connection failures to
unreachable, malformed payloads to protocol failure, and remaining HTTP failures
to generic upstream failure. Public query errors and stream events remain generic
and never contain response bodies or credentials.

## 5. Retry Policy

Only idempotent model-discovery readiness probes retry. The default is one
additional attempt, a three-second per-attempt timeout, and 0.1-second bounded
linear backoff; validation limits retries to five and backoff to five seconds.
Authentication, missing-model, and protocol failures do not retry. Generation is
never automatically retried because a timed-out request may have reached the
server. Streams are never restarted, including after visible tokens, preventing
duplicate generation and output.

## 6. Request Correlation & Logging

HTTP middleware accepts a safe 1–64 character `X-Request-ID` or generates a UUID
hex ID, attaches it to request context, and returns it in the response header.
Streaming restores that context for the iterator lifetime. Provider failures,
stream failures, readiness outcomes, and API failures include the ID and safe
classification fields. Prompts, conversations, retrieved documents, credentials,
authorization headers, and upstream bodies are not logged by this work.

## 7. Streaming Failure Behavior

Pre-token and post-token provider failures terminate with the existing sanitized
NDJSON `error` event. Non-streaming availability failures normalize to HTTP 503;
protocol and generic gateway failures normalize to HTTP 502 rather than blindly
mirroring upstream status. No stream retry occurs. Persistence remains after
complete generation only, so an incomplete assistant response and its user message
are not written to conversation history.

## 8. Files Changed

Modified:

- `.env.example`, `README.md`
- `api/app.py`, `config/settings.py`, `graph/streaming.py`
- `llm/inference.py`, `llm/ollama_client.py`, `llm/openai_compatible.py`, `llm/provider_factory.py`
- `tests/unit/test_model_routing.py`, `tests/unit/test_openai_compatible_provider.py`, `tests/unit/test_streaming_orchestration.py`

Added:

- `llm/operational.py`
- `tests/unit/test_api_reliability.py`, `tests/unit/test_provider_readiness.py`
- `docs/codex/prompts/phase_8c.md`, `docs/codex/reports/phase_8c_report.md`

Deleted:

- None.

The untracked repository-level `AGENTS.md` was supplied before implementation and
was not modified as part of the phase.

## 9. Tests Added / Updated

The suite now covers shared Ollama/OpenAI-compatible readiness success, discovery
URLs, cleanup, unreachable, timeout, authentication, overload, generic upstream,
missing model, malformed discovery payload, transient recovery, retry exhaustion,
non-retryable behavior, representative generation HTTP statuses, invalid
readiness configuration, liveness independence, readiness status behavior,
request-ID validation, and no retry/persistence after partial streaming output.

## 10. Validation Results

- `python -m pytest -q`: 87 passed in 0.57 seconds on final validation.
- `PYTHONPYCACHEPREFIX=/tmp/polymind-phase8c-pycache python -m compileall -q .`: passed. The external cache avoided the known local memory cache ownership issue.
- `git diff --check`: passed.
- `docker compose config --quiet`: passed.
- `docker build .`: passed using cache; dependency layers were cached and no additional tag was created.
- Dedicated linting: no configured linter was found.
- Secret/debug/TODO scan: no new secret, credential, debug, or TODO finding; existing semantic-router print calls predate and are outside this phase.

## 11. Implementation Self-Review

The provider-neutral boundary remains intact and startup performs no readiness
network call. Review confirmed readiness is discovery-only, retries cannot
duplicate inference, public errors remain sanitized, response resources close,
and successful-only persistence remains intact. One issue was found: middleware
context ends before a streaming body is consumed. The request ID is now captured
at the endpoint and restored for the iterator lifetime. Test module stubs were
also isolated after an initial order-pollution failure.

## 12. Pre-Commit Review

The working tree contains only scoped Phase 8C changes plus the pre-existing
untracked `AGENTS.md`. No files were deleted, no dependency was added, no API
payload or NDJSON event shape changed, and no provider/GPU service entered Docker
or CI. The scan found only deliberate fake credentials in tests and documented
Bearer terminology. No `.env`, private key, generated bytecode, temporary file,
hard-coded local path, new TODO, or debug statement is included.

No commit was created.
No push was performed.

## 13. Documentation

README configuration and operations sections now explain liveness versus
readiness, discovery behavior, retry safety, request IDs, failure sanitization,
and provider-unavailable startup. The phase prompt and this report are stored
under `docs/codex/`.

## 14. Remaining Risks / Technical Debt

Readiness is an instantaneous probe rather than a cache or circuit breaker, by
design. Provider model-list behavior can vary among OpenAI-compatible servers;
adapters require the standard `data[].id` shape. HTTP status alone cannot prove
whether a generation reached an upstream server, which is why generation retries
remain disabled. Broader metrics, distributed tracing, alerting, and historical
readiness trends are deliberately deferred rather than partially implemented.

## 15. Phase 8D Readiness

READY

Operational categories, correlation IDs, readiness outcomes, and safe logging
fields now provide stable inputs for Phase 8D Observability & Inference Metrics
without coupling orchestration code to Ollama or vLLM protocol details.
