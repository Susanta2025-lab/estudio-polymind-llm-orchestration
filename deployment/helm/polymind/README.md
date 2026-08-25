# PolyMind Helm chart

This chart deploys only the PolyMind FastAPI control plane. External operators
must provide OpenAI-compatible inference (including vLLM), Redis, and Chroma HTTP.
The chart does not install those services, an ingress controller, monitoring, or
cloud infrastructure.

## Configure secrets

Create a Secret before installation. The Redis URL and PolyMind API token are
required; the inference API key is optional when the external service does not
require authentication.

```bash
kubectl create namespace polymind
kubectl -n polymind create secret generic polymind-secrets \
  --from-literal=redis-url='rediss://user:password@redis.example.internal:6380/0' \
  --from-literal=api-auth-token='supply-a-runtime-token-of-at-least-32-characters' \
  --from-literal=openai-compatible-api-key='replace-me'
```

Keep credentials out of values files and shell history in real environments;
prefer the organization's secret-management workflow. A differently named
Secret and keys can be selected with `secrets.existingSecret` and the two key
settings, including `secrets.apiAuthTokenKey`. `secrets.create=true` exists for controlled testing, but secret values
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

The default 135-second termination grace is bounded by the 120-second upstream
inference read timeout plus 15 seconds for application and transport shutdown.
Uvicorn stops accepting new work on SIGTERM and waits for active responses; the
Kubernetes Service removes terminating pods. No sleep-based `preStop` hook is
used. Streams exceeding the grace budget can still be terminated and are never
automatically retried.

Production authentication and docs behavior are secure chart defaults. Clients
must send `Authorization: Bearer <token>` to query and streaming endpoints.
Rotate Secret values by updating the externally managed Secret and rolling the
Deployment; secrets are read only at process startup.

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
account token by default. The root filesystem is read-only. Revision-pinned local
models are baked into `/opt/polymind/models`; a bounded 256 MiB `emptyDir` at
`/tmp` is the only writable filesystem and contains transient library caches.

The Service exposes `/metrics` on the same application port. Restrict metrics at
the network/ingress layer and scrape each replica independently; this chart does
not install Prometheus or a network policy. Ingress is disabled by default and
enabling it assumes an ingress controller and any TLS material already exist.

The public Ingress path defaults to `/query`, which includes `/query/stream` but
does not route probes, metrics, docs, OpenAPI, memory, or CLI-only administration.
Configure `ingress.className`, hosts, annotations, and `ingress.tls` for the
operated TLS boundary. The chart installs no controller or certificate manager.

NetworkPolicy is enabled by default and selects only this release's pods. Replace
the example gateway, monitoring, DNS, Redis, Chroma, and inference selectors with
real labels. External dependencies require reviewed `ipBlocks` or a CNI/egress
gateway because standard NetworkPolicy cannot select DNS names. The Phase 10 Kind
override disables policy because Kind's default CNI does not enforce it.

See `docs/security/production-security.md` and `docs/security/threat-model.md` for
the complete endpoint, Secret rotation, network, proxy, and residual-risk contract.
