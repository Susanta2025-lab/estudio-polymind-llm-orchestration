# PolyMind Helm chart

This chart deploys only the PolyMind FastAPI control plane. External operators
must provide OpenAI-compatible inference (including vLLM), Redis, and Chroma HTTP.
The chart does not install those services, an ingress controller, monitoring, or
cloud infrastructure.

## Configure secrets

Create a Secret before installation. The Redis URL is required; the inference
API key is optional when the external service does not require authentication.

```bash
kubectl create namespace polymind
kubectl -n polymind create secret generic polymind-secrets \
  --from-literal=redis-url='rediss://user:password@redis.example.internal:6380/0' \
  --from-literal=openai-compatible-api-key='replace-me'
```

Keep credentials out of values files and shell history in real environments;
prefer the organization's secret-management workflow. A differently named
Secret and keys can be selected with `secrets.existingSecret` and the two key
settings. `secrets.create=true` exists for controlled testing, but secret values
must be supplied at install time and must never be committed.

## Validate and deploy

Set the external endpoints, served-model map, immutable corpus version, and image:

```bash
helm lint deployment/helm/polymind
helm template polymind deployment/helm/polymind
helm upgrade --install polymind deployment/helm/polymind \
  --namespace polymind \
  --set image.repository=registry.example.com/polymind \
  --set image.tag=1.0.0 \
  --set application.openaiCompatibleBaseUrl=https://inference.example.internal/v1 \
  --set application.vectorStoreHost=chroma.example.internal \
  --set application.bm25CorpusVersion=corpus-2026-08-24
kubectl -n polymind rollout status deployment/polymind-polymind
```

For complex values such as `application.openaiCompatibleModelMap`, use a
reviewed environment-specific values file. Verify that the declared BM25 version
has already been ingested and published in the external Chroma collection before
rolling replicas.

Upgrade with another `helm upgrade --install`. Review revisions using
`helm history polymind --namespace polymind` and roll back using
`helm rollback polymind REVISION --namespace polymind`. Rolling updates default
to zero unavailable replicas and one surge replica.

## Health, security, and operations

`/health` is process-only liveness. `/ready` contacts the configured inference,
Redis, and Chroma services and also requires the process-local BM25 snapshot to
match the published corpus version. A dependency outage therefore removes a pod
from Service endpoints without asking Kubernetes to restart a live process.

Containers run as UID/GID 10001, drop all Linux capabilities, disallow privilege
escalation, use the runtime-default seccomp profile, and do not mount a service
account token by default. The image currently needs a writable filesystem for
Python/runtime caches, so read-only root filesystems are not enabled.

The Service exposes `/metrics` on the same application port. Restrict metrics at
the network/ingress layer and scrape each replica independently; this chart does
not install Prometheus or a network policy. Ingress is disabled by default and
enabling it assumes an ingress controller and any TLS material already exist.

