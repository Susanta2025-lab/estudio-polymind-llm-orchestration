# Phase 12 Report — Deterministic Model Packaging & Control-Plane Image Optimization

## 1. Phase Result

PASS

The control-plane image is CPU-only, contains its required revision-pinned local
models, succeeds offline as UID/GID 10001 with a read-only root, and is 76.94%
smaller than the measured baseline while preserving the established contracts.

## 2. Baseline Image Analysis

The unchanged `polymind:phase12-baseline` image measured 3,175,520,907 bytes
(3.18 GB decimal). Its pip layer was 6.01 GB unpacked. Container inspection found
Torch `2.12.0+cu130`, approximately 2.725 GB of `site-packages/nvidia`, 1.141 GB
of Torch, 699 MB of Triton, and 25 MB of CUDA Python packages. Explicit frozen
requirements included 17 NVIDIA packages, three CUDA packages, and Triton.

No MiniLM artifacts existed in the image. `rag.embeddings` downloaded
`sentence-transformers/all-MiniLM-L6-v2` lazily; `rag.reranker` downloaded
`cross-encoder/ms-marco-MiniLM-L-6-v2` at import. Default cache selection was the
non-root user's home. Semantic routing did not own a third model: it reused the
embedding model and lazily computed 39 intent-example vectors. Host cache evidence
showed about 88 MB per model cache entry.

## 3. Final Image Architecture

The final image remains based on `python:3.10-slim`. It installs the exact CPU
Torch wheel first, installs pinned application dependencies, downloads only the
files required from two immutable model revisions at build time, removes fetch
metadata/cache, creates UID/GID 10001, copies runtime code, and starts uvicorn as
that user. LLM inference, Redis, and Chroma HTTP remain external services.

## 4. Dependency Optimization

All direct `cuda-*`, `nvidia-*`, and `triton` entries were removed. Torch changed
from `2.12.0` (resolved as CUDA 13.0) to `2.12.0+cpu`. The CPU wheel is isolated in
`requirements-ml-cpu.txt`, uses PyTorch's CPU-only index, and is installed with
`--no-deps`; all its dependencies are version-pinned in `requirements.txt` and
installed immediately afterward. Existing application, local ML, UI, Chroma,
Redis, provider, and test packages were retained to avoid unrelated redesign.

## 5. Deterministic Model Inventory

| Purpose | Identifier | Revision | Acquisition | Runtime path |
| --- | --- | --- | --- | --- |
| Dense retrieval and semantic routing | `sentence-transformers/all-MiniLM-L6-v2` | `1110a243fdf4706b3f48f1d95db1a4f5529b4d41` | `snapshot_download` during build | `/opt/polymind/models/embedding` |
| Cross-encoder reranking | `cross-encoder/ms-marco-MiniLM-L-6-v2` | `c5ee24cb16019beea0893ab7796b1df96625c6b8` | `snapshot_download` during build | `/opt/polymind/models/reranker` |

Both upstream repositories expose Apache-2.0 metadata. Recorded model-weight
SHA-256 values are `53aa51172d142c89d9012cce15ae4d6cc0ca6895895114379cacb4fab128d9db`
for the embedding model and
`821d1aa69520101d6e0737f78a042ae25b19e5cb9160701909d10434f4aeb0ae`
for the reranker. Revision identity is authoritative; checksums provide additional
inspection evidence and are documented here rather than used as a second registry.

## 6. Runtime Model Behavior

Application import constructs neither model. Embedding and reranker construction
remain lazy; semantic routing shares the embedding instance and lazily computes
intent vectors. Production supplies a local artifact directory and enables both
Transformers and Hub offline modes. A missing/incomplete artifact raises a clear
role-specific validation/loading error and cannot silently download or switch.
`/ready` remains inexpensive and does not load or generate with the models; image
validation provides the deterministic artifact guarantee.

## 7. Model Cache / Filesystem Strategy

Read-only artifacts live at `/opt/polymind/models`. `HF_HOME` and
`SENTENCE_TRANSFORMERS_HOME` resolve to `/tmp/polymind-cache`; `TMPDIR=/tmp`.
The image has no root/user home cache. Files are world-readable and were loaded by
UID/GID 10001. Kubernetes supplies a 256 MiB ephemeral `/tmp` `emptyDir`; no model,
memory, or vector data is written to the image filesystem in production.

## 8. Read-Only Root Filesystem

ENABLED

The Helm security context now sets `readOnlyRootFilesystem: true`. Live Kind pods
loaded both artifacts and served the application with only `/tmp` writable.

## 9. Cold-Start Findings

In the offline container smoke run, first embedding load plus encode was 0.270 s,
first reranker load plus prediction was 0.190 s, and semantic-router intent setup
plus routing was 0.290 s. These are single local laptop observations, not formal
benchmarks. Application import completed before model initialization. Existing
probe timings required no inflation.

## 10. Image Size Results

```text
Baseline:   3,175,520,907 bytes (3.18 GB decimal)
Final:        732,420,653 bytes (0.73 GB decimal)
Reduction:  2,443,100,254 bytes (2.44 GB decimal)
Percentage: 76.94%
```

Largest remaining contributors are the CPU Torch installation (734 MB unpacked),
the broader Python application stack (about 1.1 GB unpacked total), and 175 MB of
required model artifacts. Chroma/Streamlit and their transitive pandas, PyArrow,
Kubernetes, ONNX Runtime, and telemetry dependencies remain potential future
analysis areas, but removing them would require a separately scoped architecture.

## 11. Docker Layer Review

Pip uses `--no-cache-dir`; model fetch metadata and root caches are deleted in the
fetch layer. Fetch allow-patterns avoid unused TensorFlow/ONNX/OpenVINO artifacts.
The artifact layer is 184 MB unpacked and is not duplicated by recursive `chown`.
The source layer fell from 67.3 MB to 2.9 MB because `.dockerignore` excludes docs,
tests, local data/vector state, caches, build output, and runtime memory JSON.
No compiler/build-tool stage or package-manager cache was added.

## 12. Kubernetes / Helm Changes

The chart configures artifact/offline/cache/temp environment variables, enables a
read-only root, mounts a single `/tmp` `emptyDir`, and bounds it to 256 MiB. Probe
configuration and rollout strategy are unchanged. The existing Kind chart/fixture
architecture was reused; no dependency service entered the production chart.

## 13. Security Regression Review

Bearer authentication, disabled production docs, Secret/existingSecret handling,
default NetworkPolicy, TLS-capable disabled-by-default Ingress, request-size limit,
private metrics policy, UID/GID 10001, non-root enforcement, dropped capabilities,
no privilege escalation, RuntimeDefault seccomp, and disabled service-account
token remain intact. Live pods reported read-only roots, UID 10001, and `/tmp` as
the sole mount. Model artifacts contain no credentials.

## 14. API / RAG Compatibility

`/query`, `/query/stream`, NDJSON events, dense retrieval, cross-encoder reranking,
semantic routing, deterministic BM25 version gating, Redis memory, Chroma local/HTTP,
Ollama, and OpenAI-compatible provider code/contracts are unchanged. Kind smoke
validated health, readiness, authentication rejection, docs suppression, an
authenticated query, and streaming NDJSON through the existing external fixtures.

## 15. Files Changed

Modified: `.dockerignore`, `.env.example`, `.github/workflows/ci.yml`, `Dockerfile`,
`Makefile`, `README.md`, `config/settings.py`, Helm README/templates/values,
`docs/security/production-security.md`, `rag/embeddings.py`, `rag/reranker.py`,
`requirements.txt`, and relevant unit tests.

Added: `config/model_artifacts.py`, `requirements-ml-cpu.txt`,
`scripts/fetch_models.py`, `scripts/validate_container_models.py`,
`tests/unit/test_model_artifacts.py`, this report, and the Phase 12 prompt artifact.

Deleted: none.

## 16. Dependencies

`torch==2.12.0` changed to `torch==2.12.0+cpu` through the dedicated CPU index.
Direct `cuda-bindings`, `cuda-pathfinder`, `cuda-toolkit`, 17 `nvidia-*` packages,
and `triton==3.7.0` were removed. No new Python package was added. All other pinned
versions remain unchanged.

## 17. Tests Added / Updated

Tests cover the complete two-role inventory, 40-character revisions, baked/local
source resolution, incomplete/relative artifact validation, lazy reranker import,
production offline configuration, Helm offline environment, read-only root,
bounded `/tmp`, and the non-root Docker identity. The standalone container smoke
checks application import, artifacts, embedding dimension, reranking, routing,
CPU Torch, and offline flags.

## 18. Validation Results

- Phase 11 GitHub Actions on `a5be0b9`: success.
- `python -m pytest -q`: 168 passed, 1 skipped in 18.42 s; the skip was only the
  PATH-based Helm subprocess test, followed by direct Helm validation.
- External-cache compile validation: passed.
- `git diff --check`: passed.
- `docker compose config --quiet`: passed.
- `pip check` in final image: no broken requirements.
- Helm lint: 1 chart linted, 0 failed (icon recommendation only).
- Helm template: passed; rendered security/model/temp settings inspected.
- Cached production Docker build: passed.
- Final image/layer inspection: passed; size 732,420,653 bytes.
- CPU/GPU inspection: Torch `2.12.0+cpu`, `torch.version.cuda=None`, CUDA unavailable;
  no NVIDIA, CUDA, or Triton distribution/directory present.
- Non-root/read-only runtime: passed as UID/GID 10001 with network disabled.
- Embedding, reranker, and semantic-router smoke: passed.
- Kind: passed after republishing the existing synthetic `phase10-v1` corpus;
  two replicas ready with read-only root and `/tmp` mount.
- Phase 11 security regression: unit, rendered-manifest, and live smoke passed.

## 19. Offline Runtime Validation

PASS. `docker run --network none --read-only` with only a 256 MiB `/tmp` tmpfs
successfully imported the application, loaded both models, produced a 384-element
embedding, reranked documents, and selected the expected semantic `rag` route.

## 20. Implementation Self-Review

Review found and fixed: an initial build-script module path omission; unrestricted
snapshot fetching that attempted unused model formats; eager reranker loading; an
artifact-duplicating recursive `chown` layer; and a CPU-index installation layout
that allowed unnecessary resolver work. The final design uses explicit PYTHONPATH,
required-file allow-patterns, lazy loading, root-owned/readable immutable artifacts,
and CPU Torch installed first with pinned dependencies afterward. No provider or
RAG semantics leaked into packaging infrastructure.

## 21. Pre-Commit Review

The worktree contains only intended Phase 12 modifications/additions. Secret,
private-key, `.env`, generated artifact, debug, TODO, machine-path, CUDA/GPU,
compatibility, and scope reviews found no release blocker. Model bytes exist only
inside the built image, not the Git worktree. The existing Kind cluster/release was
used and left running at two ready replicas; it was not destroyed.

An ignored, pre-existing local `.env` file is present; it was neither opened nor
modified and remains excluded from Docker context and Git status.

No commit was created.
No push was performed.

## 22. Documentation

README documents CPU installation, exact model revisions, offline behavior, local
development, update procedure, and validation command. Helm/security docs now
describe the immutable artifacts and read-only `/tmp` contract. Phase prompt and
this detailed report were added under `docs/codex` without changing prior reports.

## 23. Remaining Risks / Technical Debt

### Phase 12 concerns

Build success still depends on availability of the two upstream Hugging Face
revisions and the PyTorch CPU index; runtime does not. Model licenses and revision
IDs are documented, but no signing/SBOM platform exists. The installed production
requirements still include development/UI and heavy Chroma transitive packages,
so a future explicitly scoped dependency split could reduce the image further.
Cold-start timings are single-machine observations. The Transformers reranker emits
a harmless deprecation warning about `cache_dir` inside its library abstraction.

### Deliberately deferred platform work

HPA, PDB, topology spread, cloud deployment, tracing, load/capacity tests, OAuth,
service mesh, external artifact registry, signing/SBOM, GPU/vLLM deployment, model
hot swapping, and larger availability/observability controls remain out of scope.

## 24. Phase 13 Readiness

READY

Phase 12 removed the control-plane GPU/runtime-download risks, materially reduced
the immutable image, and live-validated two secure replicas. The repository is
ready for `Phase 13 — Availability, Observability & Capacity Baseline`, subject to
normal user review and commit/push outside this run.
