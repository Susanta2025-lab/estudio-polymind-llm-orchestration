# Local application launchers

Activate the existing Python 3.10 project environment, then run `make help` from
the repository. All application targets use `PYTHON` (default `python`). To select
an interpreter explicitly, append `PYTHON=/path/to/project/bin/python`. A pyenv
shim is fine: the isolated launcher captures `sys.executable` before clearing its
environment. No global Uvicorn or Streamlit executable is used.

## Local Ollama Chat/RAG

Run in two terminals using the same optional `CHAT_*` values:

```bash
make chat-api
make chat-ui
```

Or supervise both services in one terminal:

```bash
make chat-dev
```

Open **http://127.0.0.1:8501**. The API binds **127.0.0.1:8001**. Ctrl-C stops
each foreground service; for `chat-dev` it stops both. SIGTERM to the combined
supervisor also stops both. A child failure shuts down its sibling and returns
failure. The API intentionally runs without automatic reload in this isolated
workflow; restart it after backend changes.

This is the original `api.app:app` / `ui/app.py` application: LangGraph,
semantic/model routing, hybrid Chroma/BM25 retrieval, reranking, provider-neutral
inference and NDJSON streaming remain unchanged. It uses explicitly disabled
authentication **only for this private loopback local workflow**. Use local test
content, not governed workloads.

The launcher discards inherited application settings, credentials, proxy settings
and Python import paths. It sets an explicit repository import path and uses a
private working directory outside the repository. It refuses `.env` and
`.streamlit` configuration there. A `ui` asset link keeps the existing relative
image path working. Its isolated `HOME` also avoids personal Streamlit secrets
and configuration. It never edits the repository `.env` or any historical
security/governance authority.

| Variable | Default / contract |
| --- | --- |
| `CHAT_RUNTIME` | System temporary directory + `polymind-chat-UID` (normally `/tmp/polymind-chat-1000`). Created privately if absent; existing directory must belong to you and have 0700 permissions. Persistent between launches; never automatically deleted. |
| `CHAT_CHROMA_PATH` | `CHAT_RUNTIME/chroma_db`, an absolute local Chroma path after expansion. An explicitly selected existing local index is also supported. |
| `CHAT_CORPUS_VERSION` | `development`; must match the index's published corpus version. |
| `CHAT_HF_HOME` | Existing `~/.cache/huggingface` cache, resolved before `HOME` isolation. |
| `CHAT_MODEL_ARTIFACT_DIR` | Optional existing artifact directory containing `embedding/` and `reranker/`. |

Relative overrides resolve against the invocation directory. Prefer absolute
paths. Example using an existing **local** retrieval index:

```bash
make chat-dev CHAT_RUNTIME=/tmp/polymind-chat-session \
  CHAT_CHROMA_PATH="$PWD/chroma_db" CHAT_CORPUS_VERSION=development
```

Startup does not ingest, publish, reset or populate an index. A fresh runtime has
no corpus and correctly returns HTTP 503 from `/ready` with
`collection_unavailable` / `bm25_uninitialized`. Use an already populated local
index with matching published version to establish retrieval readiness. Do not
run historical `make ingest`, `make rebuild` or `make clean` assuming they inherit
this isolated configuration; those targets retain their configured semantics.

The existing Ollama service must provide these exact names:

| Role | Ollama model |
| --- | --- |
| general | `mistral:latest` |
| coding | `qwen2.5:3b` |
| summarization | `gemma2:2b` |
| fast | `phi3:mini` |

Ollama is fixed to `http://127.0.0.1:11434/api/chat`. These targets never select a
cloud provider, substitute missing models or download models. Embedding and
reranker loading is offline; the pinned artifacts must already exist in the
chosen cache or artifact directory for actual routed queries. `/ready` checks
inference, memory, Chroma and BM25; it does not load every embedding/reranker
artifact or prove successful generation.

```bash
curl --noproxy '*' --fail-with-body http://127.0.0.1:8001/ready
curl --noproxy '*' http://127.0.0.1:11434/api/tags
```

`/` and `/health` establish liveness only. Missing Ollama models, an unreachable
service or an unavailable corpus remain visible in `/ready`; inspect its status
and model map. Start the existing local Ollama service or install the intended
models separately under operator control. No startup retry loop installs them.

## Authenticated synthetic Documents

Choose a **new, nonexistent private directory outside the repository**:

```bash
make docs-init DOCS_RUNTIME=/tmp/polymind-documents-new
make docs-serve DOCS_RUNTIME=/tmp/polymind-documents-new
```

`DOCS_RUNTIME` is mandatory. Initialization refuses existing directories without
changing them. Serving requires an initialized runtime. The targets execute the
existing `python -m development.document_demo initialize/serve` lifecycle using
the selected interpreter and a clean environment; they do not implement another
document runtime. A production deployment environment is rejected by the local
launchers.

Open **https://localhost:9443**, using `localhost` exactly. Trust only that fresh
runtime's `tls.crt` for this local test. The existing private OIDC issuer remains
on 9444, internal FastAPI on 8001 and internal Streamlit on 8501. The existing
API process owns the locked durable runner/worker. Authentication, authorities,
quotas, publication and session controls remain in force. Inference is synthetic
and in-process; there is no paid provider fallback.

Ctrl-C or SIGTERM to the lifecycle supervisor stops its four services. Worker
shutdown can take about 70 seconds for an in-flight bounded operation. Retain
the runtime and its approvals/history; startup never deletes it. Expired or
exhausted approvals require a separately selected new runtime, not resetting an
existing directory. See the [Documents operator guide](phase_18_local_document_demo.md)
for login, approved sources, durable jobs, publication, Q&A, retention and limits.
Internal readiness is available at `http://127.0.0.1:8001/ready` while serving.

## Compatibility and troubleshooting

`make api`, `make ui` and `make dev` preserve the historical shell/`.env`
configuration, authentication semantics, entrypoints, external bind addresses
and API reload behavior. Their interpreter is corrected to module execution.
`dev` now supervises and cleans up both processes. These commands can still fail
if governed authorities/configuration require reconciliation. The local launchers
do not repair pricing mismatches or bypass those safeguards.

If `which uvicorn` points to a user-level executable with a system-Python
shebang, it no longer affects these targets. Check `python -c 'import sys;
print(sys.executable)'` and `python -m uvicorn --version`. A missing module error
means the selected Python lacks that dependency: activate the existing project
environment or set `PYTHON`, rather than installing globally. The new launchers
report missing startup dependencies with the selected interpreter path.

Chat and Documents share ports **8001/8501** and must be started separately.
New launchers check requested loopback ports before spawning services and report
a conflict; a subsequent bind race can still fail in the underlying service.
Inspect owners with `ss -ltnp`, stop the appropriate foreground process with
Ctrl-C, then launch the other workflow. Do not kill unrelated services. Empty
Chat indices and missing offline artifacts are dependency problems, not reasons
to weaken readiness or change the processing algorithms.
