# Phase 8D — Observability & Inference Metrics

## Objective

Add lightweight, production-style, provider-neutral observability without
deploying an external monitoring platform. Preserve Phase 8A–8C APIs, reliability,
request correlation, Ollama support, and the external OpenAI-compatible/vLLM
boundary.

## Required implementation

- Expose a standard metrics endpoint that never triggers inference or readiness.
- Measure inference counts, outcomes, latency, normalized errors, stream lifetime,
  and time to first non-empty generated content.
- Record exact provider-reported token usage only when available.
- Add bounded semantic-route and readiness metrics.
- Keep protocol-specific usage parsing inside provider adapters.
- Exclude sensitive and unbounded data from metric labels and output.
- Retain request IDs in safe logs, not metrics.
- Use deterministic CPU-only tests with no live external service.

## Constraints and workflow

Do not add monitoring infrastructure, vLLM, GPU support, tracing, multi-process
aggregation, or unrelated architecture. Inspect, plan, implement, test,
self-review, fix, pre-commit review, document, validate, and report. Save phase
artifacts under `docs/codex/`. Do not commit or push.
