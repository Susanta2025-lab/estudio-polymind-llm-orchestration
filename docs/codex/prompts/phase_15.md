# Phase 15 — Validated Application Autoscaling

Implement and functionally validate: PolyMind per-pod active synchronous queries
→ Prometheus → hardened recording rule → Prometheus Adapter/equivalent →
`custom.metrics.k8s.io` → `autoscaling/v2` Pods `AverageValue` HPA → replicas.

Fresh idle pods must publish zero with bounded labels and correct cleanup. Real
scrape failures remain missing. Preserve namespace/pod identity and exclude streams
from the primary signal. Keep adapter mapping outside the application chart. Add
a disabled-by-default HPA requiring deliberate target and maximum configuration;
omit Deployment replicas while enabled. Add no application RBAC, PDB, topology
defaults, startup probe, VPA, KEDA, cluster autoscaling, or dependency autoscaling.

Add deterministic tests and run full regression, compile, diff, Helm, Prometheus,
Compose, image/runtime, security, and scoped Kind validation. Prove authenticated
load → metric → adapter → HPA → scale-up → Ready pods → zero → stabilized
scale-down, plus authentication, direct/RAG, NDJSON, stream isolation, termination,
and persistence. Clean scoped resources. Kind values are never production sizing,
capacity, HA, SLO, target, or ceiling evidence; target-cluster and downstream
capacity calibration remain required. Do not commit or push.
