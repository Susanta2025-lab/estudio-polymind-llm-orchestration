# Phase 15 Kind autoscaling validation

This workflow validates interoperability on `kind-polymind-phase10`. Its `100m`
target, maximum 4 replicas, and 60-second scale-down stabilization are development
parameters, never production capacity, threshold, HA, ceiling, or SLO evidence.

Verify the current context exactly, build/load `polymind:phase15`, update Phase 10
fixtures, install PolyMind with `values.yaml`, and deploy the Phase 14 Prometheus
configuration. Install the cluster-owned reference adapter separately:

```bash
helm upgrade --install phase15-adapter prometheus-community/prometheus-adapter \
  --version 5.3.0 -n polymind-phase10 \
  -f deployment/kind/phase15/prometheus-adapter-values.yaml
```

Confirm APIService availability, custom-metric discovery, and idle zero per pod.
Port-forward the Service and run `load.py` with the synthetic local token. Watch
HPA, Deployment, pods, Prometheus, and the custom metric through scale-up,
readiness, zero return, stabilization, and scale-down. Validate direct/RAG queries,
NDJSON completion, long-stream isolation, authentication, and persistence. Observe
inference, Redis, and Chroma headroom; application scaling can amplify dependency
pressure.

Cleanup only the `phase15-adapter` release and Phase 14 Prometheus resources. If
retaining the base environment, reinstall PolyMind with Phase 10 values. Do not
delete the cluster or unrelated resources.
