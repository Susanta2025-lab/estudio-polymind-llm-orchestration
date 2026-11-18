# Local application Makefile compatibility and configuration isolation

## Executive summary and verdict

The local launch interfaces and interpreter correction are implemented without
changing either application plane. Historical `api`, `ui` and `dev` retain their
configured authentication/inference semantics. New Chat targets explicitly select
local Ollama in a private environment; Documents targets invoke the existing
Phase 18 lifecycle. No global packages, system executables, production settings,
governed authorities or application algorithms were changed.

**Verdict: PASS for the requested startup-maintenance scope.** Both actual
browser workflows, all targeted checks and continued regression coverage are
verified. There is no outstanding startup blocker. All 3,163 collected test
cases are covered by the saved evidence described below. The initial broad
run timed out; this report does not claim a successful single full-suite run.
Interrupted or sandbox-blocked runs are not counted as successful processes.

## Starting repository and audit

The initial branch was `master`, HEAD
`d7d2ec28bf96ed7caae2be42bf38046ffa90ba33`. There were no tracked modifications.
There were 28 pre-existing untracked Phase 17h prompt/report files, preserved
throughout this task; their names are listed in the appendix.

Before selecting the correction, the audit read the complete Makefile,
`config/settings.py`, `api/app.py`, `ui/app.py`, `ui/documents_view.py`, the
Documents lifecycle/provisioning/runtime composition and Phase 18 operator guide.
It inspected startup/settings isolation tests, document client/OIDC/operator
tests, the browser journey, requirements, CI, README consumers, model artifacts
and retrieval readiness. No application interface change was necessary.

Non-destructive interpreter checks reproduced the reported mismatch:

| Check | Observed value |
| --- | --- |
| `command -v python` | `/home/home/.pyenv/shims/python` |
| `python --version` | Python 3.10.13 |
| `sys.executable` / `pyenv which python` | `/home/home/.pyenv/versions/estudio_polymind/bin/python` |
| `command -v uvicorn` | `/home/home/.local/bin/uvicorn` |
| User Uvicorn shebang | `#!/usr/bin/python3` |
| `pyenv which uvicorn` | Project environment's `bin/uvicorn` |
| Installed project packages | Uvicorn 0.48.0, prometheus-client 0.26.0, Streamlit 1.58.0 |

The sandbox initially denied network inspection and local connections. An
approved `ss` inspection outside it found ports 8001, 8501, 9443 and 9444 free,
with Ollama listening on 127.0.0.1:11434. Its `/api/tags` returned all four exact
required model names. No models were installed or substituted.

## Root causes and architecture

The original Makefile invoked standalone `uvicorn`, allowing PATH to select a
system-Python executable while the required packages were installed in the pyenv
environment. Module execution now binds Uvicorn and Streamlit to `PYTHON ?=
python`. The helper uses that running interpreter's absolute `sys.executable`
before constructing a clean child environment, so clearing PATH cannot select
system Python through a pyenv shim.

Settings specify `env_file=".env"`; legacy construction consults the current
working directory. Selecting `DOCUMENTS_PROFILE=legacy` does not disable it.
Shell variables are another configuration source. The new Chat launcher solves
both at the process boundary: an environment allowlist and a private directory
outside the repository, with no `.env` or `.streamlit` files. An explicit
repository import path and `ui` asset link preserve original imports and assets.
An isolated child HOME avoids personal Streamlit configuration/secrets; existing
offline model caches are selected separately before that isolation.

Chat still uses `api.app:app`, `ui/app.py`, the original graph/routing/RAG code,
local file memory and the provider-neutral streaming boundary. Documents still
uses `development.document_demo`: private HTTPS/OIDC, internal Streamlit and
FastAPI, one API-owned durable runner/worker, existing authorities and in-process
deterministic inference. It does not import the legacy graph/provider factory.
The two workflows share 8001/8501 and are intentionally started separately.

## Files changed

| File | Purpose |
| --- | --- |
| `Makefile` | Interpreter-bound historical commands; Chat/Documents targets; explicit help and safe variable export |
| `development/local_apps.py` | Standard-library launcher isolation, prerequisites, port checks and combined Chat/configured-service cleanup |
| `tests/unit/test_local_apps.py` | Startup, interpreter, isolation, frontend, validation and process-cleanup regressions |
| `docs/operations/local_applications.md` | Exact commands, settings, readiness, shutdown and troubleshooting |
| `docs/operations/phase_18_local_document_demo.md` | Replace manual Chat isolation recipe and link Make lifecycle equivalents |
| `README.md` | Link the separated startup workflows |
| This report | Audit, rationale, evidence, limitations and review findings |

No dependency manifests, application/backend/frontend modules, configuration
implementation, deployment files or durable schemas were changed.

## Command contracts

| Target | Exact behavior |
| --- | --- |
| `make api` | `$(PYTHON) -m uvicorn api.app:app --reload --host 0.0.0.0 --port 8001`; existing configuration semantics |
| `make ui` | `$(PYTHON) -m streamlit run ui/app.py --server.address 0.0.0.0 --server.port 8501`; existing configuration semantics |
| `make dev` | Supervise those configured services using the selected Python; stop sibling/process groups on failure or interruption |
| `make chat-api` | Original API, isolated local settings, 127.0.0.1:8001, no automatic reload |
| `make chat-ui` | Original Chat frontend, isolated matching settings, http://127.0.0.1:8501 |
| `make chat-dev` | Supervise both isolated Chat services; Ctrl-C/SIGTERM stops both |
| `make docs-init DOCS_RUNTIME=/tmp/NEW-private-directory` | Selected Python executes existing `development.document_demo initialize`; missing runtime argument, repository path or existing directory refused |
| `make docs-serve DOCS_RUNTIME=/tmp/NEW-private-directory` | Selected Python executes existing `development.document_demo serve`; requires initialized runtime and free 8001/8501/9443/9444; browser entrypoint https://localhost:9443 |

`CHAT_RUNTIME` defaults to the system temporary directory plus
`polymind-chat-UID`; existing directories require owner-only permissions.
`CHAT_CHROMA_PATH` defaults to its `chroma_db`; `CHAT_CORPUS_VERSION` defaults to
`development`. `CHAT_HF_HOME` selects an existing offline cache; optional
`CHAT_MODEL_ARTIFACT_DIR` selects existing embedding/reranker artifacts. The usage
guide specifies exact defaults and absolute-path handling. Arguments are exported
as environment data rather than interpolated as shell code.

Chat explicitly sets Ollama at 127.0.0.1:11434 with `general=mistral:latest`,
`coding=qwen2.5:3b`, `summarization=gemma2:2b`, `fast=phi3:mini`, local file
memory, local Chroma and local API URLs. It explicitly disables authentication
only in this isolated loopback development workflow. Historical targets retain
their safeguards. New development targets reject a production deployment
environment. They do not ingest/reset indices, download models or reconcile
governance/pricing.

## Automated verification

Completed new launcher regression run:

```bash
python -m pytest tests/unit/test_local_apps.py -q \
  --junitxml=/tmp/polymind-local-launcher-targeted.xml
```

**27 passed in 2.85 seconds, zero failures.** Coverage includes a fake conflicting
standalone Uvicorn/Streamlit, selected-interpreter Make recipes, clean-process
Settings and actual Streamlit AppTest, a hostile synthetic repository `.env`
and shell, exact model mappings/endpoints, private memory/index paths,
production rejection, missing/invalid Documents runtime handling, unchanged
existing-directory contents, delegation to the existing Documents lifecycle,
port errors, missing dependencies in an actual empty virtual environment,
concurrent asset-link creation, sibling failure and SIGTERM cleanup.

An initial combined relevant run was interrupted before producing a completion
summary. A diagnostic rerun inside the sandbox completed 68 cases then blocked
in the first existing OIDC test's Starlette/AnyIO TestClient, before handling its
request. The saved stack is `/tmp/polymind-local-launcher-focused.log`. It was
stopped rather than counted as a pass. Outside the sandbox, the unchanged OIDC
test module completed: **12 passed in 1.50 seconds**.

The affected existing regression set also completed successfully:

```bash
python -m pytest tests/unit/test_streamlit_startup.py \
  tests/unit/test_settings_isolation.py tests/unit/test_documents_client.py \
  tests/unit/test_provider_readiness.py tests/unit/test_ollama_provider.py \
  tests/integration/test_document_operator.py -q \
  --junitxml=/tmp/polymind-local-launcher-relevant.xml -o faulthandler_timeout=60
```

**136 passed in 124.66 seconds, zero failures.** This includes existing real
frontend startup/configuration isolation, Ollama and normalized missing-model /
service failure contracts, strict document schemas, complete authorized
document workflow with network effects forbidden, durable lifecycle,
publication/replay, revocation, cancellation and authority failure cases.
Together with the separate launcher and OIDC runs, these establish 175 distinct
targeted cases; they are not added to the overlapping full-suite total.

The broad regression command was:

```bash
timeout 900 python -m pytest -q \
  --junitxml=/tmp/polymind-local-launcher-full.xml -o faulthandler_timeout=60
```

It reached its 900-second bound, **exit 124**, after **1,972 pass markers**.
Its saved output contains only normal progress percentages and pass dots: no
failure, error, skip or other outcome markers. It did not produce a final
summary/JUnit file and is **not a successful complete-suite process**.

To preserve completed work, final sequential collection was saved separately:
**3,163 cases collected**. There are no repository collection-order hooks.
The only two test additions during the broad run occur at positions 2,601/2,602
in the final collection, after the completed prefix, so that prefix is unchanged.
The continuation manifest combines those 1,972 sequential pass markers with
the successful targeted JUnit cases and the separately completed OIDC module.
Deduplication establishes **2,100 already verified distinct cases**, leaving
**1,063 remaining cases**. No already verified case was selected again for the
continuation.

```bash
timeout 600 python /tmp/polymind-local-launcher-remaining.py
```

That temporary evidence-only driver selects the remaining exact node IDs and
executes the selected project Python's pytest module. It completed **exit 0:
1,063 passed, 7 warnings in 110.65 seconds**, zero failures/errors/skips. A
post-run check reconstructed all JUnit node IDs and verified exact set equality
with the continuation manifest. Thus **2,100 + 1,063 = 3,163 collected cases**
have passing evidence across the bounded runs; overlapping targeted results
are not added twice. This is continued coverage, not a fabricated monolithic
suite summary. The seven warnings concern existing `record_property` tests
with default `junit_family=xunit2`; they are reporting-format warnings. No tests
were rerun merely to suppress them.

The last pass-marker case at the interrupted-run boundary was separately
checked through normal teardown and process exit: **1 passed in 0.60 seconds**,
exit 0, recorded in `/tmp/polymind-local-launcher-boundary.xml`. This boundary
check is not added to the distinct coverage count.

Evidence files are `/tmp/polymind-local-launcher-full.log`,
`/tmp/polymind-local-launcher-all-collected.txt`,
`/tmp/polymind-local-launcher-resume-manifest.json`,
`/tmp/polymind-local-launcher-remaining.log` and
`/tmp/polymind-local-launcher-remaining.xml`, alongside targeted logs/XML already
listed. The temporary verification drivers and runtime fixtures are outside
the repository and are not deliverable application code.

The following final checks also completed:

| Command/check | Result |
| --- | --- |
| `make help` and dry-run application recipes | Passed; all required commands/variables documented |
| `python -m uvicorn --version` | Uvicorn 0.48.0, CPython 3.10.13 |
| `python -m streamlit --version` | Streamlit 1.58.0 |
| `PYTHONPYCACHEPREFIX=/tmp/polymind-local-launcher-pycache python -m compileall -q .` | Exit 0; external cache, no ownership changes |
| `git diff --check` | Exit 0 |
| `docker compose config --quiet` | Exit 0 |
| New/updated guide and report relative-link check | No broken local links |
| Final application listener inspection | 8001, 8501, 9443, 9444 free; pre-existing Ollama still listening |

No configured lint/format tool was found in the repository. No new lint tool or
runtime dependency was installed. Docker image and Kubernetes validation were
not needed: this change concerns host launchers, without dependency, image,
chart, manifest or service-topology changes.

## Live local verification

Before the interruption, a new Chat runtime without an index started both
services and accurately returned `/ready` HTTP 503:
`collection_unavailable`, `bm25_uninitialized`; Ollama and file memory were
ready. A private copy of the existing local Chroma corpus returned HTTP 200,
with all four components and model roles ready. The first browser assertion
used overly strict emoji/text matching and timed out although the model response
had been persisted; that attempt is not counted as a completed browser check.

The resumed bounded Chat browser smoke test passed using a new private copy of
the corpus. It started `make chat-dev`, received `/ready` HTTP 200, submitted a
greeting through the actual Streamlit UI, and displayed a completed direct
response from `mistral:latest`. There were zero external browser requests and no
frontend exceptions. Supervisor shutdown released both ports. Hashes before and
after confirmed the source repository `.env` and Chroma files were unchanged.
Evidence: `/tmp/polymind-local-dual-chat-0p_t5kw4/evidence.json`, browser body,
screenshot and service log; harness log
`/tmp/polymind-local-dual-chat-smoke.log`.

The interruption left a Documents supervisor from the first attempt running.
Only that scoped supervisor was terminated; its existing cleanup stopped all
four services. Its runtime was retained and never reset/reused. The resumed
verification created a separate new runtime and uses the existing
`tests/browser/document_journey.py` with lifecycle calls routed through
`make docs-init`/`make docs-serve`. Optional Playwright/Chromium tooling already
present under `/tmp` was reused; nothing was installed. It checks current
admission timing, rather than changing limits or approvals.

The resumed Documents journey **passed**, exit 0, with saved acceptance:
`auth=true`, `complete_journey=true`, `browser_isolation=true`, `cancel=true`,
`external_browser_requests=0`. It verified fresh Make initialization and
existing-directory refusal with unchanged file hashes, idle `/ready` HTTP 200,
native OIDC callback, authenticated operator context, Secure/HttpOnly/SameSite
identity cookies, browser isolation and invalid-state rejection. It then
created an approved-source session, started the durable job, observed complete
digestion, authorized publication, read canonical evidence, asked a selected
document question, withdrew the session, logged out, and exercised a second
session's cancellation/closure. The harness waited for the existing admission
window before Q&A; no quota or approval was altered. SIGTERM to the Make-run
lifecycle cleaned up all four ports.

Evidence: `/tmp/polymind-local-dual-docs-smoke.log` and
`/tmp/polymind-browser-gw8u26q1/acceptance.json`, with service logs and the private
disposable runtime in that evidence directory. An expected invalid-callback
warning came from the negative authentication test. The existing Authlib
dependency emitted its upstream HTTPX deprecation warning; runtime behavior
passed and no dependency change was made.

## Self-review and pre-commit review

Review kept all provider-specific launch settings inside development
infrastructure, with no changes to graph, API, RAG or document algorithms.
Historical shell/dotenv behavior and external binds remain deliberate. New
launchers have fixed loopback inference/service endpoints and do not forward
credentials, cloud settings, proxies or uncontrolled Python paths. Offline
embedding/reranker loading and telemetry settings prevent automatic model
downloads by the Chat workflow.

Two meaningful findings were corrected: the initial advisory port probe treated
TCP TIME_WAIT as an occupied listener (it now uses socket reuse), and concurrent
API/UI startup could race when creating the same asset link (an equivalent link
is accepted, conflicting links still fail). Combined startup uses process groups
and bounded cleanup; single-service launchers replace themselves with the bound
interpreter. Documents cleanup remains owned by its existing supervisor.

The separate pre-commit review checked the complete tracked diff and all new
task files for credentials, local machine paths in executable code, generated
runtime artifacts, unintended configuration/API changes and unrelated edits.
No secrets, debug artifacts, accidental dependencies, stale TODOs or unrelated
implementation changes were found. No commit, push, reset, stash, merge or
remote mutation was performed.
All synthetic keys, authorities, screenshots and logs stay outside the worktree.
The existing Docker ignore rules continue to exclude real dotenv, keys,
authorities and browser runtime state. No dependencies or Docker configuration
changed, so an image rebuild is not required for this host-startup maintenance.

## Limitations and acceptance checklist

- A new Chat runtime does not contain a retrieval corpus. Full readiness requires
  a populated local index with the selected published version; startup does not
  create one or mask its absence.
- Actual routed queries require the existing pinned offline embedding/reranker
  artifacts. Readiness does not exercise every model or every routed RAG query.
- The live model check exercised a representative direct Chat stream; automated
  contracts cover routing, retrieval and normalized provider failure behavior.
- Chat and Documents use 8001/8501 sequentially. Preflight is advisory; a later
  bind race still fails in the underlying service.
- Governed `make api/dev` authority construction was deliberately not activated
  or repaired. Their interpreter/argument/environment contracts are tested;
  historical pricing/governance failures remain out of scope.
- Synthetic Documents is not a paid inference test or production identity
  deployment. Existing approval, session, token and certificate limits apply.
- A single uninterrupted full-suite pass is not claimed. The 900-second attempt
  timed out; the continuation and explicit manifest matching establish coverage
  of every collected case across runs. Seven existing JUnit-format warnings
  remain documented, without changing application or test behavior.

| Acceptance area | Status / evidence |
| --- | --- |
| Selected project interpreter; no standalone executable mismatch | PASS: Make module recipes, controlled-executable regression and actual module version checks |
| Dedicated isolated Chat API/UI and combined startup | PASS: recipes, subprocess settings/frontend tests and real browser stream |
| Governed dotenv/cloud/credential isolation | PASS: hostile synthetic dotenv/shell tests, explicit environment and unchanged actual dotenv hash |
| Original Chat processing and contracts preserved | PASS: original entrypoints/code unchanged, ready existing-corpus copy and live Mistral stream |
| Missing corpus/model/service reported honestly | PASS: fresh-index HTTP 503 and provider readiness contracts; no downloads/substitution |
| Existing Phase 18 lifecycle and authentication | PASS: Make delegation, fresh initialization and complete native-auth browser journey |
| Runtime/authority preservation | PASS: existing-directory hash refusal, no resets/deletions and no authority/configuration edits |
| Shutdown and sequential operation | PASS: sibling/SIGTERM regression tests, both live shutdowns, final ports free |
| Automated regression | PASS: 27 launcher, 136 affected existing and 12 OIDC cases; all 3,163 collected cases covered across the bounded runs described above |
| Production/governed compatibility | Configuration/argument contracts preserved; governed live execution intentionally excluded |
| No paid inference/cloud activation | PASS: local Ollama and in-process synthetic provider only |
| Operator review and Git safety | All changes remain uncommitted; no push or remote mutation |

No architecture phase follows automatically. The deliverable is ready for
operator review. The existing governance/pricing discrepancy is excluded from
this maintenance task.

## Final Git state

HEAD and branch remain unchanged. Task changes consist of three modified
tracked files and four new untracked files:

```text
 M Makefile
 M README.md
 M docs/operations/phase_18_local_document_demo.md
?? development/local_apps.py
?? docs/operations/local_applications.md
?? tests/unit/test_local_apps.py
?? docs/codex/reports/local_dual_application_makefile_compatibility.md
```

`git diff --stat` reports **3 tracked files changed, 51 insertions,
46 deletions**; it does not include the four untracked additions. The 28 original
untracked files below remain present and untouched. All task changes are left
uncommitted for operator review. **No commit or push occurred.**

## Preserved pre-existing untracked files

The following original files remain uncommitted and outside this task's edits.
Paths below are relative to `docs/codex/`:

```text
prompts/phase_17h_current_authorization_and_token_headroom_assessment.md
prompts/phase_17h_final_approval_signing_and_controlled_execution.md
prompts/phase_17h_v10_authentication_renewal_and_final_operator_packet_preparation.md
prompts/phase_17h_v10_final_operator_verification_and_conditional_live_execution.md
prompts/phase_17h_v10_operator_preparation_and_readiness_assessment.md
prompts/phase_17h_v5_authorized_catalog_migration_and_commercial_reconciliation.md
prompts/phase_17h_v5_complete_financial_readiness_and_operator_preparation.md
prompts/phase_17h_v5_execution_window_renewal_and_rsa_authorization.md
prompts/phase_17h_v5_final_operator_preparation_continuation.md
prompts/phase_17h_v5_financial_reconciliation_and_second_four_call_readiness.md
prompts/phase_17h_v5_four_call_readiness_reassessment.md
prompts/phase_17h_v5_operator_preparation_signing_and_controlled_execution.md
prompts/phase_17h_v8_azure_operator_preparation_and_signing_readiness.md
reports/phase_17h_current_authorization_and_token_headroom_assessment.md
reports/phase_17h_final_approval_signing_and_controlled_execution.md
reports/phase_17h_live_invalid_qualification_source_root_cause.md
reports/phase_17h_v10_authentication_renewal_and_final_operator_packet_preparation.md
reports/phase_17h_v10_final_operator_verification_and_conditional_live_execution.md
reports/phase_17h_v10_final_signing_and_controlled_live_outcome.md
reports/phase_17h_v10_operator_preparation_and_readiness_assessment.md
reports/phase_17h_v5_authorized_catalog_migration_and_commercial_reconciliation.md
reports/phase_17h_v5_complete_financial_readiness_and_operator_preparation.md
reports/phase_17h_v5_execution_window_renewal_and_rsa_authorization.md
reports/phase_17h_v5_final_operator_preparation_continuation.md
reports/phase_17h_v5_financial_reconciliation_and_second_four_call_readiness.md
reports/phase_17h_v5_four_call_readiness_reassessment.md
reports/phase_17h_v5_operator_preparation_signing_and_controlled_execution.md
reports/phase_17h_v8_azure_operator_preparation_and_signing_readiness.md
```
