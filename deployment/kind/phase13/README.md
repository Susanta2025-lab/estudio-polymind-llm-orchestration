# Phase 13 local availability baseline

Phase 13 reuses the dedicated single-node `polymind-phase10` Kind cluster and its
synthetic dependencies. This is a controlled laptop baseline, not cloud capacity
or a production SLO. The production chart remains dependency-neutral.

The HTTP harness uses bearer authentication and hard bounds of 32 workers, 1,000
requests, and 300 seconds. Supply the synthetic token at runtime:

```bash
export POLYMIND_BENCHMARK_TOKEN='<local synthetic token>'
python scripts/capacity_baseline.py \
  --base-url http://127.0.0.1:18001 --workload direct \
  --concurrency 4 --requests 20 --timeout 60 \
  --image polymind:phase13 --replicas 2 \
  --environment kind-single-node \
  --resources 100m-384Mi-request_1cpu-2Gi-limit
```

Workloads are `direct`, `rag`, and `stream`. JSON output records Git SHA, image,
replicas, resource description, environment, timestamps, errors, throughput,
latency percentiles, TTFT, and stream duration. Use at least 20 successful samples
before interpreting p95; treat p99 from such a small sample as directional only.

The Phase 10 inference fixture recognizes `phase13-long-stream` and returns 40
chunks one second apart. With two ready Phase 13 replicas, run the guarded
in-cluster rollout test (it refuses any other current context):

```bash
POLYMIND_BENCHMARK_TOKEN='<local synthetic token>' \
  deployment/kind/phase13/rollout_stream.sh
```

The disposable client must receive a final NDJSON `done` event while the rollout
retains service availability. Do not use the service port-forward itself as the
long-stream client: it binds to one selected pod and can close its tunnel during
termination, confounding application drain behavior.
