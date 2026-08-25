#!/usr/bin/env bash
set -euo pipefail

CONTEXT="kind-polymind-phase10"
NAMESPACE="polymind-phase10"
DEPLOYMENT="polymind-polymind"
CLIENT="phase13-stream-client"

if [[ "$(kubectl config current-context 2>/dev/null || true)" != "$CONTEXT" ]]; then
  echo "Refusing operation: expected context $CONTEXT." >&2
  exit 1
fi
if [[ -z "${POLYMIND_BENCHMARK_TOKEN:-}" ]]; then
  echo "POLYMIND_BENCHMARK_TOKEN is required." >&2
  exit 2
fi
if [[ "$(kubectl --context "$CONTEXT" -n "$NAMESPACE" get deployment "$DEPLOYMENT" -o jsonpath='{.spec.replicas}')" -lt 2 ]]; then
  echo "At least two PolyMind replicas are required." >&2
  exit 3
fi

kubectl --context "$CONTEXT" -n "$NAMESPACE" delete pod "$CLIENT" --ignore-not-found --wait=true
kubectl --context "$CONTEXT" -n "$NAMESPACE" run "$CLIENT" \
  --image=python:3.10-alpine --image-pull-policy=IfNotPresent --restart=Never \
  --env="TOKEN=$POLYMIND_BENCHMARK_TOKEN" --command -- python -c \
  'import json,os,urllib.request; body=json.dumps({"query":"phase13-long-stream tell me a joke","session_id":"phase13-rollout"}).encode(); request=urllib.request.Request("http://polymind-polymind:8001/query/stream",data=body,headers={"Authorization":"Bearer "+os.environ["TOKEN"],"Content-Type":"application/json","X-Request-ID":"phase13-rollout"},method="POST"); response=urllib.request.urlopen(request,timeout=90); [print(line.decode().strip(),flush=True) for line in response]'
kubectl --context "$CONTEXT" -n "$NAMESPACE" wait --for=condition=Ready "pod/$CLIENT" --timeout=30s
sleep 5
kubectl --context "$CONTEXT" -n "$NAMESPACE" rollout restart "deployment/$DEPLOYMENT"
kubectl --context "$CONTEXT" -n "$NAMESPACE" rollout status "deployment/$DEPLOYMENT" --timeout=240s
kubectl --context "$CONTEXT" -n "$NAMESPACE" wait \
  --for=jsonpath='{.status.phase}'=Succeeded "pod/$CLIENT" --timeout=120s
output="$(kubectl --context "$CONTEXT" -n "$NAMESPACE" logs "$CLIENT")"
grep -q '"type": "done"' <<<"$output"
printf '%s\n' "$output"
