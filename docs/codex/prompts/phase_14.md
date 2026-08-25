# Phase 14 — Production Observability Integration & Capacity Calibration

This implementation phase turns PolyMind's process-local Prometheus metrics into
a production-consumable multi-replica contract without deploying an HPA or making
the application chart own a monitoring stack.

Required work includes: inventory all existing bounded metrics; preserve the
provider-neutral boundary; implement optional deployment-neutral scrape discovery;
keep monitoring CRD resources opt-in; define correct counter, gauge, and histogram
aggregation; add recording rules, operational queries, measurable SLIs, explicitly
non-committed candidate SLOs, and candidate alerts; assess the unauthenticated
same-port `/metrics` boundary; reuse the authenticated Phase 13 capacity harness;
validate two replicas and actual aggregation in the dedicated Kind environment;
retain the existing resource baseline unless stronger evidence exists; and state
target-cluster/external-inference calibration gaps honestly.

Out of scope are HPA, VPA, cluster autoscaling, PDB, topology defaults, startup
probe, cloud-specific monitoring, an application-owned Prometheus/Grafana/
Alertmanager stack, adapter deployment, tracing infrastructure, dependency or
vLLM scaling, and unsupported resource changes. Preserve bearer authentication,
NetworkPolicy, non-root/read-only/offline packaging, 135-second termination grace,
and rollout-safe NDJSON streaming. Do not commit or push.

The full externally supplied phase brief also mandates inspect-first workflow,
self-review, pre-commit review, exact validation reporting, Phase 14 artifacts,
and the 30-section report stored alongside this prompt.

