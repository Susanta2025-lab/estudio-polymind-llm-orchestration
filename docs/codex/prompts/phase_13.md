# Phase 13 — Availability & Capacity Baseline with Rollout-Safe Streaming

## Objective

Establish reproducible evidence for PolyMind control-plane availability and
per-replica capacity, and prove that long-running authenticated NDJSON streams
behave safely during client disconnect, SIGTERM, pod termination, and a
two-replica Kubernetes rolling deployment.

## Required method

Use an evidence-first sequence: inspect and record the unchanged baseline; build
a small bounded authenticated HTTP harness; measure cold/warm behavior, CPU,
memory, and increasing concurrency; test disconnect, SIGTERM, and an active-stream
Kind rollout; then implement and re-measure only controls justified by evidence.

Preserve provider-neutral inference, the upstream SSE to provider-neutral stream
to PolyMind NDJSON boundary, memory persistence semantics, Phase 11 security, and
Phase 12 offline/non-root/read-only packaging. Do not deploy HPA, VPA, cluster or
inference autoscaling, monitoring platforms, cloud infrastructure, service mesh,
or unrelated architecture. Do not infer production sizing from laptop Kind data.

Evaluate—but do not automatically add—resource changes, probe changes,
`startupProbe`, PDB, topology controls, `preStop`, and termination/drain controls.
HPA must remain disabled. Preserve incomplete-stream no-persistence and no-retry
semantics. Use only the dedicated `kind-polymind-phase10` context and scoped test
resources. Run complete regression, compile, diff, Helm, Docker, security,
disconnect, SIGTERM, and rolling-stream validation. Save the detailed report as
`docs/codex/reports/phase_13_report.md`. Do not commit or push.
