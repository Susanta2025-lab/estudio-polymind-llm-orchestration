# Phase 14 scoped Prometheus validation

This profile validates pod discovery, multi-replica scraping, and rule evaluation
in the existing `kind-polymind-phase10` environment. It is not part of the
PolyMind Helm chart and is not production monitoring infrastructure.

After positively verifying the context, create the two ConfigMaps from
`prometheus.yml` and `../../monitoring/prometheus-rules.yaml`, apply
`prometheus.yaml`, and enable the chart's scrape annotations. Prometheus discovers
only annotated pods in `polymind-phase10` and retains at most one hour in an
ephemeral volume. Query `/api/v1/targets` and `/api/v1/query` to validate both pod
targets and the `polymind:*` recorded series.

Remove only the scoped Deployment, Service, RBAC objects, ServiceAccount, and two
ConfigMaps after validation. The dedicated cluster and PolyMind workloads remain.
