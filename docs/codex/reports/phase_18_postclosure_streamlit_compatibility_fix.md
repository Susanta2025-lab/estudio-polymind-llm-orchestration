# Phase 18 post-closure Streamlit compatibility correction

Date: 14 November 2026. Verdict: **`PHASE_18_POSTCLOSURE_COMPATIBILITY_FIX_PASS`**.

The original Streamlit Chat startup failure was reproduced in a real browser,
then corrected by renaming its colliding sibling view module. Both frontend
modes, protected synthetic execution, API compatibility and the complete local
regression suite passed. This is a separately traceable maintenance correction,
not a new numbered Phase 18 stage or a revision of historical acceptance evidence.
Real-model readiness and production deployment are not claimed.

## 1. Repository baseline and preservation

HEAD is `6aedae3b1fb215baa1a0af6344a771d8cdf63c70`, the Phase 18.3 closure
commit, `docs: finalize Phase 18 local engineering closure and deployment handoff`.
The preceding implementation commit is `f7d091a`. Initial commands executed were
`git status --short --branch`, `git log --oneline -7`, `git rev-parse HEAD` and
`git diff --check`. The branch was `master...origin/master`; there were no tracked
changes, and exactly 28 intentionally untracked Phase 17H documents.

Those 28 paths and their SHA-256 hashes were captured before implementation in
`/tmp/phase18-postclosure/baseline.json` and verified unchanged afterward. No
historical report, source freeze, accepted evidence, authority, approval or
financial policy was edited. The index remains empty. No staging, commit, push,
reset, clean, merge, rebase, tag, branch or remote mutation occurred.

## 2. Architecture and complete affected-reference inventory

Investigation preceded the rename. Repository-wide `rg` searches covered
`ui.documents`, `ui/documents.py`, `documents.py`, `from documents`,
`import documents` and `DOCUMENTS_PROFILE`, including source, tests, scripts,
configuration, deployment and documentation. The initial matching-line inventory
is `/tmp/postclosure-reference-inventory.txt` (1,005 lines). AST import inventories
under `/tmp/phase18-postclosure/*-imports.txt` record the initial graph across UI,
52 backend document modules, security, governance, inference and the development
runtime. These diagnostic artifacts are outside the repository.

| Area / reference | Dependency and consequence | Action |
| --- | --- | --- |
| `ui/app.py:18` | Sole runtime `from ui.documents import render`, inside the synthetic branch | Import `ui.documents_view` |
| `ui/documents.py` | View imports Streamlit and `ui.documents_client`; no backend package implementation belongs here | Ordinary filesystem rename to `ui/documents_view.py`; contents byte-identical |
| `ui/documents_client.py` | Per-call Bearer client for `/documents/operator`; no dependency on the old view name | Unchanged |
| `ui/api_client.py` | Existing `/query/stream` NDJSON client | Unchanged; tests extended |
| `ui/__init__.py` | Empty package initializer; no alias or view re-export | Unchanged |
| `documents/models.py` | Canonical immutable `FrozenModel`, `Scope`, identity and document contracts | Unchanged |
| `documents/operator/` | Enrolled operator workflow, guarded presentation, actions and runner | Unchanged |
| `documents/pilot/` | Source/session approvals, durable execution, publication and release controls | Unchanged |
| `documents/jobs/` | Admission, durable ledger, dispatch, leases and cancellation | Unchanged |
| `documents/digestion/` | Extraction/synthesis workflow and versioned contracts | Unchanged |
| `documents/publication/` | Immutable generations, publication authority, retrieval and bounded analysis | Unchanged |
| `config/settings.py` → `security.identity` | OIDC configuration validation imports `FrozenModel` through `documents.models` | Unchanged; exercised before backend preloading in new regression |
| `api/app.py`, `api/operator.py`, `api/security.py`, `security/`, `governance/`, `llm/` | Backend imports consistently target canonical packages; no frontend-view consumer | Unchanged |
| Dockerfile, legacy Compose | Copy application tree; launch `api.app:app` and `ui/app.py` | No explicit old view filename; unchanged |
| Documents Compose and `development/document_demo/` | Explicit synthetic lifecycle launches the same `ui/app.py`, native login and separate operator runtime | No old view-name reference; unchanged |
| `deployment/helm/polymind/` | Existing API entrypoint, configuration, security and probes | No view dependency; unchanged |
| `tests/unit/test_documents_client.py` | Imports `ui.documents_client`, not the view | Unchanged |
| `tests/browser/document_journey.py`, `tests/browser/oidc_nonce.py` | Launch `ui/app.py`; native callback and lifecycle checks | No rename required; existing journey reused |
| Stage 18.2 report, implementation inventory row | Historical reference to `ui/documents.py` | Preserved as historical evidence |
| Stage 18.3 prompt, line 214 | Historical requested inspection path `ui/documents.py` | Preserved as historical instructions |

There were no frontend consumers using `from documents import ...`, no dynamic
imports of `ui.documents`, no serialized callback/module-name references, and no
launch command pointing directly to `ui/documents.py`. Dynamic backend imports
still resolve canonical document codecs. No backend imports the view. Callbacks,
the status fragment, login/logout and client composition stay inside the
byte-identical renamed view. The sole existing executable reference requiring
replacement was the import in `ui/app.py`.

## 3. Original failure and confirmed Python resolution

Python 3.10.13 and Streamlit 1.58.0 were used. A clean diagnostic inserted the
actual repository `ui/` directory first in `sys.path`, then inspected the import
spec before importing the backend:

```text
documents spec origin: <repository>/ui/documents.py
submodule_search_locations: None
from documents.models import FrozenModel
ModuleNotFoundError: No module named 'documents.models'; 'documents' is not a package
```

The package and `documents/models.py` were present. This was a module-name
collision combined with path precedence, not a missing installation, missing
file or Python-environment mismatch. Streamlit CLI bootstrap prepends the script
directory. Python finds that standalone `documents.py` before the canonical
package, and a standalone module cannot resolve `documents.models`.

The actual command was also run, without replacing application code:

```bash
DOCUMENTS_PROFILE=legacy python -m streamlit run ui/app.py
```

Cached Chromium opened the running application and established a browser session,
forcing execution of the script. Before correction it displayed the exact
`ModuleNotFoundError` and zero Chat inputs. The traceback was
`ui/app.py → config.settings → security.identity → documents.models`. After
correction the same command displayed one Chat input and no exceptions. The
isolated local launch documented in the operator guide was additionally checked
in a real browser with the same successful result.

Evidence: `/tmp/phase18-postclosure/import-before.txt`, `legacy-before.json`,
`legacy-before.log`, `legacy-after.json`, `legacy-after.log` and
`legacy-isolated.json`. No application `sys.path` workaround or `sys.modules`
alias was introduced.

## 4. Correction and architectural impact

The implementation is an ordinary filesystem rename,
`ui/documents.py → ui/documents_view.py`, plus its single caller update.
Comparison with `git show HEAD:ui/documents.py` verifies byte-for-byte preservation
of the view. The canonical backend `documents/` package and every public backend
import remain unchanged. This removes the collision rather than masking it.

The internal frontend Python module name changes intentionally. Repository
consumers were exhaustively searched; no public HTTP contract or documented
direct view-import integration was found. External code that directly imported
the internal `ui.documents` view would need the new name; retaining a compatibility
shim at the old filename would recreate the defect and is deliberately avoided.

Chat/RAG/LangGraph, routing, memory, provider abstraction, SSE-to-provider tokens,
NDJSON output, protected operator routes, source processing, publication,
financial controls and production/Helm configuration have no implementation
changes. No dependency, inference permission, cloud operation or spending grant
was added.

Changed paths are:

1. `ui/documents.py` → `ui/documents_view.py` (identical contents).
2. `ui/app.py` (one import).
3. `tests/unit/test_streamlit_startup.py` (new subprocess regressions).
4. `tests/unit/test_ui_api_client.py` (additional error/cleanup coverage).
5. `docs/operations/phase_18_local_document_demo.md` (current view name,
   configuration distinction and isolated legacy launch).
6. This corrective report.

## 5. Independent API authentication and authority findings

Safe configuration inspection printed only non-secret mode flags, presence,
path-safety booleans and equality results. No token, private key, connection
string, issuer configuration, full policy, catalog value or credential was
displayed. There were no shell overrides for the inspected settings. The local
`.env` selects `API_AUTH_MODE=oidc_jwt`, `API_AUTH_ENABLED=false`,
`GOVERNANCE_ENABLED=true` and `INFERENCE_PROVIDER=openai_compatible`; it also
supplies OIDC settings and three authority paths. `DOCUMENTS_PROFILE` is absent
there and defaults to `legacy` unless explicitly selected.

`DOCUMENTS_PROFILE` controls the frontend branch. `API_AUTH_MODE` controls
authentication; when omitted, `API_AUTH_ENABLED` retains its historical behavior.
`OIDC_CONFIGURATION` selects trusted validation parameters.
`SECURITY_AUTHORITY_PATH` identifies the enrollment/authorization authority;
governance and provider admission have separate configured paths. Selecting
`legacy` does not clear any of them. Consequently the original UI reaches the
OIDC settings validator even before deciding which page to render.

Read-only SQLite inspection found all three existing authority files present,
private, owned by the current user, regular, single-link, without symlink path
components, at schema version 1 and matching current schemas. The recorded
governance policy and shared admission policy match configuration. Evaluation
authority bindings also validate. **The configured pricing catalog differs from
the recorded governance catalog**, including the `version`, `effective_date` and
`prices` fields. `GovernanceLedger.__init__` explicitly raises
`SecurityError('security_configuration')` for that mismatch. `SecurityRuntime`
construction therefore cannot complete under this configuration, and
`api.app.lifespan` reports the generic `Required security authority unavailable`.
The message covers the composed runtime, not only the first security database.

This establishes an independent configuration inconsistency that survives the
frontend rename. The original authorities were not reopened through mutating
constructors, rewritten, migrated or reset, and no real OIDC/JWKS service was
contacted. The historical log itself was supplied by the operator; the present
diagnosis uses read-only state comparison and the constructor guard, rather than
restarting the original governed configuration.

The exact local configuration correction is to run Chat/API under the isolated
legacy profile documented in the guide: a new working directory without `.env`,
an environment allowlist, `DOCUMENTS_PROFILE=legacy`, `DEPLOYMENT_ENV=local`,
loopback bindings and historical local authentication defaults. This avoids
unintended OIDC and external-provider selection without changing any stored
configuration. For governed execution, the existing catalog discrepancy instead
requires separate operator reconciliation with the approved recorded catalog;
changing a ledger or financial check to accept the discrepancy is not a repair.
The production restrictions and synthetic authenticated lifecycle are preserved.

## 6. Legacy API liveness versus readiness

The actual legacy `api.app:app` was started on a disposable loopback port with a
clean working directory/environment, Ollama explicitly bound to local port 11434,
temporary memory, and a deliberately isolated local vector endpoint. No
credentials or paid provider were supplied. The server shut down cleanly.

| Probe | Observed result |
| --- | --- |
| `/` | HTTP 200, running |
| `/health` | HTTP 200, alive |
| `/ready` | HTTP 503, `model_unavailable` |
| Inference component | Ollama `model_unavailable` for configured logical-role models |
| Memory component | Ready |
| Vector component | `vector_unreachable` in this disposable profile |
| BM25 component | `bm25_uninitialized` |
| Authority warning | Absent under isolated legacy configuration |

Evidence is in `legacy-api.json` and `legacy-api.log` under the diagnostic
directory. This does not assess or modify the operator's historical index or
configured external provider. No model was downloaded or invoked; successful
real-model query execution is not claimed. These readiness dependencies do not
invalidate the demonstrated frontend import correction.

## 7. Regression design and why previous checks missed the failure

Three new startup cases run fresh Python subprocesses with an environment
allowlist, a temporary working directory and the real repository paths:

* Canonical package resolution with `ui/` first verifies the import-spec origin,
  package search path, `FrozenModel` and the `security.identity` consumer.
* The real legacy `ui/app.py` runs through Streamlit's `AppTest`/ScriptRunner
  with synthetic OIDC/governance settings in a temporary dotenv, exercising the
  original settings-to-identity import edge before backend preloading. It checks
  the actual Chat input and absence of Streamlit exceptions.
* The real synthetic script renders the logged-out Documents page and imports
  `render` from `ui.documents_view`. AppTest's default user only contains email;
  the test supplies logged-out user state explicitly. It makes no authenticated
  behavior claim; native login is verified separately in the browser.

All three tests failed on the original source before the rename. The canonical
and legacy cases demonstrated the original collision; the synthetic case also
requires the new module name. All pass on the corrected tree. AppTest alone does
not execute CLI bootstrap path setup, so the harness explicitly adds the script
directory, in addition to executing the real script through ScriptRunner.
Normal pytest collection may already have cached the canonical package and
test settings suppress implicit dotenv loading. Those two differences explain
why ordinary import tests and the prior suite could pass while real Streamlit
startup failed. Production module caching is not manipulated by this correction.

Five more cases extend the existing Chat client test: server error events,
malformed JSON, list-shaped/missing-type events, response closure and normalized
connection failure. Existing metadata/chunk/done and one-generation-request
coverage is retained. The production streaming client itself is unchanged.
Existing security/API and document integration tests cover legacy query behavior,
OIDC fail-closed restrictions, protected operator contracts, malformed/foreign
tokens, admission, replay, revocation, lifecycle and release guards.

## 8. Executed verification

| Level | Result |
| --- | --- |
| Original import and actual browser reproduction | Confirmed before correction; canonical package and Chat resolve after correction |
| Focused frontend/client/configuration/security/API/operator/deployment tests | **317 passed in 68.14 seconds**, no failures/errors/skips |
| Actual legacy Streamlit command | Chat input rendered; zero Streamlit exceptions |
| Isolated legacy local launch | Chat input rendered; zero Streamlit exceptions |
| Authenticated synthetic browser journey | Native login, protected context, publication, digest, Q&A, withdrawal, logout, cancellation and isolation passed |
| Browser external requests | **0** |
| Container canonical/security/API/view imports | PASS under script-directory precedence, non-root, offline |
| Container legacy and synthetic real-script renders | PASS |
| Container synthetic API startup | `/ready` 200; anonymous context 401; signed fixture context/catalog 200; OIDC legacy query routes 403; zero provider attempts |
| Both Compose configurations | `config --quiet` passed |
| Helm lint/template | Passed; optional chart-icon recommendation only |
| Full final-tree pytest | **3,136 passed in 963.07 seconds (16:03)** |
| Full suite distribution | **2,200 unit + 936 integration**, eight additional cases above the 3,128 reference |
| Full suite failures/errors/skips | **0 / 0 / 0**; no pytest warnings reported |
| Compilation | `PYTHONPYCACHEPREFIX=/tmp/phase18-postclosure/bytecode python -m compileall -q .` passed |
| Ruff | `ruff check --select F` on all changed/new Python files passed |
| Whitespace | `git diff --check` and checks for new files passed |

The complete regression command was:

```bash
python -m pytest -q -o junit_family=legacy -o faulthandler_timeout=120 \
  --junitxml=/tmp/phase18-postclosure/full-regression.xml --durations=10 \
  > /tmp/phase18-postclosure/full-regression.log 2>&1
```

The JUnit suite records 3,136 tests with zero failures/errors/skips and 962.977
seconds of suite time; the pytest terminal summary reports 963.07 seconds.
Focused evidence is `focused.xml`/`focused.log` in the same directory. Focused
modules include startup, both clients, security configuration/identity/authority/
readiness/API/Entra, fixture OIDC, API reliability, deployment topology, Helm and
the complete document-operator integration module.

The first sandboxed Streamlit attempt could not bind a socket; the approved retry
ran normally. The first sandboxed async security tests stalled on an event-loop
wait, confirmed by a separate faulthandler diagnostic; only those two task-owned
runs were terminated. The approved unsandboxed focused retry and full suite both
passed. These were execution-environment limitations, not suppressed test failures.

The browser journey reused `tests/browser/document_journey.py` with the already
available optional Playwright/Chromium tools, without installing dependencies.
A temporary external driver inserts the guide's 61-second admission spacing
before Q&A; repository browser code and runtime policy were not changed.
Evidence is `documents-browser.log`; its private disposable runtime is
`/tmp/polymind-browser-ribynb4l`. Browser identity, keys and tokens are synthetic.
No real Entra login or external inference was used. An actual browser session,
not just Streamlit's health response, established both frontend startup results.

## 9. Docker and deployment compatibility

`docker build --iidfile /tmp/phase18-postclosure/image-id .` passed with normal
cache reuse. Dependency installation and `scripts/fetch_models.py` layers were
**CACHED**: no new dependency installation or large model download was performed.
The only rebuilt application layer copies the corrected source. Image ID is
`sha256:95f75b4fcf7049cdc3f4c41fcacd362ee7f2f1c29000d3abfa2118be62bf6e10`,
size **3,042,338,475 bytes**, configured user **10001:10001**. No extra validation
tag or global Docker cleanup was used.

Offline disposable containers verified imports, both real Streamlit script
renders and authenticated synthetic API startup. The first stricter read-only
import check omitted writable `/tmp` and failed in the existing Torch temporary
cache initialization; rerunning with the deployment-style temporary filesystem
passed. The successful checks use `--network none`, `--read-only`, a private
non-root `/tmp` tmpfs, dropped capabilities and no-new-privileges. Native fixture
JWTs are generated inside the disposable runtime, never printed. The image
contains no `/app/.env` and no old `/app/ui/documents.py`.

Both legacy and Documents Compose configurations validated unchanged. Helm lint
and template succeeded with the existing API entrypoint, production auth settings,
non-root configuration and `/health`/`/ready` probes. No Kubernetes mutation or
cloud deployment was necessary for a view-module rename. No production readiness
or new Helm Documents deployment capability is asserted. All validation containers
used `--rm`; none remain running from this image. Local test servers and browser
children were shut down.

## 10. Implementation self-review and separate pre-commit review

The complete tracked diff and every new file were reviewed after validation.
The renamed view is byte-identical, the caller has one import substitution, and
the new subprocesses deliberately avoid backend preloading and operator dotenv.
Timeouts bound subprocess execution; API/client tests check resource/error
handling. No compatibility shim, global path manipulation, provider-specific
condition, backend API change, financial-policy change or speculative refactor
was introduced. No unresolved critical/high implementation finding remains.

A separate pre-commit review checked secrets/private-key/token patterns,
credential URLs, `.env` files, machine-specific implementation paths, debug/TODO
material, temporary/generated artifacts, dependencies, unrelated changes,
documentation references and historical evidence. Intended source paths derive
from the repository or test temporary directory; guide `/tmp` paths are explicit
disposable examples. Private runtime/configuration and diagnostics remain outside
the repository. New test data is synthetic. The remaining old view-path references
are historical documentation and this explanation, not executable consumers.

All tracked files under `documents/`, `api/`, `config/`, `security/`, `governance/`,
`llm/`, `graph/`, `rag/`, `memory/`, `development/` and `deployment/`, plus Docker
and Compose files, match HEAD. The inherited 28-file hash check passes. No new
security or financial authority was granted; production OIDC and legacy-query
restrictions remain enforced by the existing code and passing tests.

## 11. Final Git disposition and remaining limits

`git status --short --branch` reports `master...origin/master`, modifications to
the operator guide, Chat client tests and `ui/app.py`, deletion of the old view,
and new files for the renamed view, startup tests and this report. The original
28 untracked Phase 17H documents remain present and unchanged. The view appears
as deletion plus an untracked file because staging is reserved for the operator.

```text
$ git diff --stat
 docs/operations/phase_18_local_document_demo.md |  47 +++++++++
 tests/unit/test_ui_api_client.py                |  40 +++++++-
 ui/app.py                                       |   2 +-
 ui/documents.py                                 | 124 ------------------------
 4 files changed, 87 insertions(+), 126 deletions(-)

$ git diff --cached --name-only
(no output)
```

The tracked diff statistic excludes the three new files, including the identical
124-line renamed view. It is not a claim that the view contents were discarded.
Full status output is retained in `/tmp/phase18-postclosure/final-git-status.txt`.

The existing `.env` catalog inconsistency remains an operator configuration
reconciliation issue. Live legacy inference/retrieval readiness remains dependent
on installed models and an available populated vector/BM25 system. Real Entra,
cloud deployment, external users, semantic acceptance and financial execution
were not part of this maintenance correction. None is represented as completed.
No task-required local verification is outstanding.

**All changes are unstaged and uncommitted for operator review. No commit or push
occurred. `PHASE_18_POSTCLOSURE_COMPATIBILITY_FIX_PASS`.**
