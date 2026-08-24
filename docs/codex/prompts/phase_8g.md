# Phase 8G — Production Deployment Topology and Operational Hardening

## Goal

Consolidate PolyMind into a production-oriented topology without Kubernetes or
cloud provisioning. PolyMind remains the FastAPI/LangGraph/RAG control plane and
uses separately operated OpenAI-compatible inference, Redis conversation memory,
and Chroma HTTP vector storage.

## Required work

- Preserve Phase 8A–8F behavior and provider-neutral boundaries.
- Validate local, Compose, and production external-service configuration.
- Keep `/health` process-only and make `/ready` require inference, memory, vector
  storage, and a current BM25 snapshot with sanitized bounded states.
- Survive dependency outages at startup and clean up owned clients at shutdown.
- Separate query-only serving from explicit ingestion/reset administration.
- Publish a deterministic corpus version and use rollout-based BM25 refresh;
  never rebuild BM25 in request or readiness threads.
- Keep metrics per-process and labels bounded.
- Keep CPU-only CI and local Compose validation independent of live services.
- Update README and save a detailed report after self-review and validation.
- Do not implement Kubernetes/cloud infrastructure, commit, or push.

## Validation policy

Apply `AGENTS.md`; run the full tests, external-cache compile validation, diff
checks, Docker Compose configuration checks, and cached Docker build. Report
exact outcomes and remaining risks with the required 20-section final report.
