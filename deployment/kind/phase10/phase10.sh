#!/usr/bin/env bash
set -euo pipefail

CLUSTER="polymind-phase10"
CONTEXT="kind-polymind-phase10"
NAMESPACE="polymind-phase10"
RELEASE="polymind"
IMAGE="polymind:phase10"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
FIXTURES="$ROOT/deployment/kind/phase10/fixtures.yaml"
VALUES="$ROOT/deployment/kind/phase10/values.yaml"
CHART="$ROOT/deployment/helm/polymind"
KIND_BIN="${KIND_BIN:-kind}"
HELM_BIN="${HELM_BIN:-helm}"

require_context() {
  local actual
  actual="$(kubectl config current-context 2>/dev/null || true)"
  if [[ "$actual" != "$CONTEXT" ]]; then
    echo "Refusing operation: expected context $CONTEXT, found ${actual:-none}." >&2
    exit 1
  fi
}

create() {
  if "$KIND_BIN" get clusters | grep -Fxq "$CLUSTER"; then
    echo "Kind cluster $CLUSTER already exists."
  else
    "$KIND_BIN" create cluster --name "$CLUSTER" --config "$ROOT/deployment/kind/phase10/kind-config.yaml"
  fi
  require_context
}

build() { docker build --tag "$IMAGE" "$ROOT"; }
load() { require_context; "$KIND_BIN" load docker-image "$IMAGE" --name "$CLUSTER"; }

deploy() {
  require_context
  kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl --context "$CONTEXT" apply -f -
  kubectl --context "$CONTEXT" --namespace "$NAMESPACE" apply -f "$FIXTURES"
  kubectl --context "$CONTEXT" --namespace "$NAMESPACE" create secret generic polymind-phase10-secrets \
    --from-literal=redis-url='redis://phase10-redis:6379/0' \
    --dry-run=client -o yaml | kubectl --context "$CONTEXT" --namespace "$NAMESPACE" apply -f -
  kubectl --context "$CONTEXT" --namespace "$NAMESPACE" rollout status deployment/phase10-inference --timeout=180s
  kubectl --context "$CONTEXT" --namespace "$NAMESPACE" rollout status deployment/phase10-redis --timeout=180s
  kubectl --context "$CONTEXT" --namespace "$NAMESPACE" rollout status deployment/phase10-chroma --timeout=180s
  "$HELM_BIN" upgrade --install "$RELEASE" "$CHART" --namespace "$NAMESPACE" -f "$VALUES" --wait=false
}

bootstrap() {
  require_context
  local version="${1:-phase10-v1}"
  kubectl --context "$CONTEXT" --namespace "$NAMESPACE" delete pod phase10-bootstrap --ignore-not-found
  kubectl --context "$CONTEXT" --namespace "$NAMESPACE" run phase10-bootstrap \
    --image="$IMAGE" --image-pull-policy=Never --restart=Never \
    --env="VECTOR_STORE_HOST=phase10-chroma" --env="VECTOR_STORE_PORT=8000" \
    --env="VECTOR_STORE_COLLECTION=phase10_knowledge" --env="BM25_CORPUS_VERSION=$version" \
    --command -- python deployment/kind/phase10/bootstrap_corpus.py
  kubectl --context "$CONTEXT" --namespace "$NAMESPACE" wait --for=condition=Ready pod/phase10-bootstrap --timeout=120s || true
  kubectl --context "$CONTEXT" --namespace "$NAMESPACE" wait --for=jsonpath='{.status.phase}'=Succeeded pod/phase10-bootstrap --timeout=180s
  kubectl --context "$CONTEXT" --namespace "$NAMESPACE" logs phase10-bootstrap
}

smoke() {
  require_context
  kubectl --context "$CONTEXT" --namespace "$NAMESPACE" rollout status deployment/polymind-polymind --timeout=300s
  kubectl --context "$CONTEXT" --namespace "$NAMESPACE" port-forward service/polymind-polymind 18001:8001 >/tmp/polymind-phase10-port-forward.log 2>&1 &
  local forward_pid=$!
  trap 'kill "$forward_pid" 2>/dev/null || true' RETURN
  for _ in {1..30}; do curl -fsS http://127.0.0.1:18001/health >/dev/null 2>&1 && break; sleep 1; done
  curl -fsS http://127.0.0.1:18001/health
  curl -fsS http://127.0.0.1:18001/ready
  curl -fsS http://127.0.0.1:18001/metrics | grep -m1 '^# HELP '
  curl -fsS -H 'Content-Type: application/json' -H 'X-Request-ID: phase10-query' \
    -d '{"query":"Tell me a short joke","session_id":"phase10"}' http://127.0.0.1:18001/query
  curl -fsS -H 'Content-Type: application/json' -H 'X-Request-ID: phase10-stream' \
    -d '{"query":"Tell me a short joke","session_id":"phase10-stream"}' http://127.0.0.1:18001/query/stream
}

destroy() {
  if "$KIND_BIN" get clusters | grep -Fxq "$CLUSTER"; then
    "$KIND_BIN" delete cluster --name "$CLUSTER"
  else
    echo "Kind cluster $CLUSTER does not exist."
  fi
}

help() {
  echo "usage: $0 {create|build|load|deploy|bootstrap [version]|smoke|destroy}"
}

case "${1:-help}" in
  create) create ;;
  build) build ;;
  load) load ;;
  deploy) deploy ;;
  bootstrap) bootstrap "${2:-phase10-v1}" ;;
  smoke) smoke ;;
  destroy) destroy ;;
  help|-h|--help) help ;;
  *) help >&2; exit 2 ;;
esac
