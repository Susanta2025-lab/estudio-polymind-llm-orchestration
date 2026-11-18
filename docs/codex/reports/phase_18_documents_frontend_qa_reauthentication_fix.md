# Phase 18 Documents frontend Q&A and reauthentication maintenance

## Scope and root causes

This maintenance change works on the existing branch and preserves the preexisting
Makefile, README, operator-guide changes and untracked work. No commit, push,
reset, stash or discard was performed. Backend implementation and persistence
remain unchanged.

The question form previously rendered only its immediate POST response. The
three-second fragment rerun removed that conditional element. The server already
persists accepted question results and includes them in reauthorized digest reads.
Separately, native Streamlit identity-cookie lifetime exceeds the fixture's
900-second API-token lifetime. A browser can therefore look logged in while its
API credential has expired. The existing explicit Log out control attempts to
close the selected session and is unsuitable as a recovery action.

## Implementation and modified files

- `ui/documents_view.py`: renders Saved Questions and Answers exclusively from the
  latest authorized digest, including a fresh read after question submission;
  removes the transient POST rendering and avoids duplicating answers in the main
  digest JSON. Retains inert JSON for answer text, canonical source/citation
  fields, evidence status, semantic-support labels and limitations. Checks packet
  and answer generations against the selected server session. Preserves polling,
  form submission and query-bound idempotency keys. An opaque UUID URL hint
  restores selection after normal page refresh; it is validated as a UUID only
  after current operator context succeeds, and all status/digest reads still
  require server authorization. Clear and logout remove it.
- `ui/documents_client.py`: adds an optional normalized HTTP status attribute to
  the existing sanitized exception. Existing exception messages and callers stay
  compatible; no upstream body or credential is attached.
- `tests/unit/test_documents_view.py`: Streamlit ScriptRunner tests exercise saved
  results, repeated reruns, fresh-page reconnect, multiple answers, access loss,
  missing credentials, generation mismatches and explicit closure controls.
- `tests/unit/test_documents_client.py`: checks normalized status metadata.
- `tests/integration/test_document_operator.py`: signed synthetic token expiry,
  foreign-principal refusal, authorized reconnection, persisted answers and no
  extra provider calls; checks unchanged deadline, approval, revocation and
  question-limit enforcement after issuing a new test credential.
- `tests/browser/document_journey.py`: adds actual timed polling and page-refresh
  recovery assertions to the existing optional acceptance runner.
- `docs/operations/phase_18_local_document_demo.md`: appends saved-answer and
  recovery instructions, preserving the guide's preexisting edits.
- This report.

## Authentication and security decisions

A normalized 401 triggers an application rerun so protected output outside the
fragment is also removed. The next render displays only recovery instructions
and the opaque session ID, with no automatic API retry. Missing credentials use
the same recovery screen. Other request failures similarly remove protected
output and require explicit authorization retry. The polling fragment also
checks whether native identity has disappeared or its access token changed.

Reauthenticate clears frontend document state and invokes native `st.logout()`
without any document Close/Withdraw call. The operator records the opaque ID
privately, then selects native Log in and manually reconnects through the existing
server-authorized recovery form. Only the opaque session UUID may be retained as a URL reconnect hint for normal
refreshes. Tokens and protected packets are never added to URLs, local storage
or custom cookies. The ID grants no authority. Native redirects
start new frontend sessions, so manual communication avoids assuming that
Streamlit session state survives authentication. The native logout transition
clears the URL hint before redirect; manual recovery revalidates everything.

Installed Streamlit 1.58.0 login/logout implementations were inspected. They
redirect through native OIDC and clear the native identity on logout; they have
no knowledge of backend document closure. This matches the official
[authentication lifecycle documentation](https://docs.streamlit.io/develop/concepts/connections/authentication).
The explicit Log out path retains its existing selected-session close attempt;
Close and Withdraw retain their behavior. An explicit stop after native logout
prevents further rendering while the redirect is pending.

All reads remain subject to current server identity, ownership, authorization,
active-session and publication-release guards. No token is decoded or trusted
locally, no refresh-token behavior is added, and no token claims, security policy,
source approval, 59-minute session approval, 600-second execution deadline,
question allowance or provider/financial limit is renewed. No operator runtime
was modified or removed. Integration tests use disposable pytest fixtures and
in-process synthetic inference, with outbound connections forbidden.

## Validation

- Final frontend/client/Chat startup command: `python -m pytest tests/unit/test_documents_view.py tests/unit/test_documents_client.py tests/unit/test_streamlit_startup.py -q`:
  **36 passed in 4.35s** after the URL-hint correction. A normal fresh-page
  test reloads results automatically from its copied UUID hint rather than
  requiring manual reconnect; invalid and unauthorized hints cannot release
  protected packets or trigger arbitrary API paths. Clear/logout remove hints.
  If the token has expired at refresh time, the recovery screen still communicates
  the UUID hint before clearing it for native reauthentication.
- Focused frontend, OIDC fixture, original Chat/Streamlit startup, operator,
  supervised pilot and document plane/digestion/jobs suite outside the sandbox:
  **161 passed, 1 failed in 166.14s**. The failure was a new test incorrectly
  expecting 403/429 for expired approval; the implemented API contract returns
  HTTP 409 `pilot_denied`. Corrected the test without changing application code.
- Corrected four authority-boundary integration cases: **4 passed in 35.82s**.
  The earlier focused run also passed actual signed-token expiration/recovery,
  retained answers, foreign-principal rejection and unchanged provider-call
  counts. Final frontend additions passed separately as recorded above.
- Initial sandbox integration/full runs were interrupted after TestClient hung
  in the AnyIO thread portal; a diagnostic run captured its blocked stack.
  Approved execution outside the sandbox allowed these tests to progress.
- First broad outside-sandbox attempt was interrupted: **335 passed, 2 failed
  in 432.87s**. It had collected the old expired-approval assertion before its
  correction, and encountered an HTTP 500 during publication setup in existing
  `test_delayed_response_revalidates_actual_asgi_send[close]`. That existing case
  passed in the focused suite. This interrupted run is not a complete PASS.
- Complete broad rerun, `python -m pytest -q` outside the sandbox:
  **3,179 passed, 1 failed in 1149.80s (19:09)**; exit status 1. All collected
  document/OIDC/security/governance checks passed. The remaining failure is
  preexisting untracked `tests/unit/test_local_apps.py::test_private_directory_and_repository_boundary`.
  The existing client backup test calls `development.document_demo.__main__.main`,
  which sets process umask to `077` without restoring it. The launcher test then
  requests a `0755` directory but receives `0700`, so its expected permissions
  rejection does not occur. A two-test reproduction produced **1 passed,
  1 failed in 0.35s**, confirming the umask remained `077`; the launcher case
  alone with process umask `022` **passed in 0.04s**. No launcher or CLI changes
  were made, in accordance with this maintenance scope. The earlier publication
  setup HTTP 500 did not recur in this completed broad run.
  The broad run collected frontend modules before the final UUID-refresh-hint
  adjustment; the final **36-test** frontend/client/Chat-startup run separately
  verifies those last changes. The broad run is complete but is not a clean PASS.
- `PYTHONPYCACHEPREFIX=/tmp/phase18-frontend-pycache python -m compileall -q .`:
  **passed**, including a repeat after the final code/test edits. No ownership
  changes were made. `git diff --check`: **passed**.
- Optional `python -m tests.browser.document_journey`: **blocked**,
  `ModuleNotFoundError: No module named 'playwright'`, before runtime creation.
  Real timed fragment polling/browser refresh assertions were added but not
  executed. No 15-minute wait or live/paid inference was used.

## Review and limitations

Implementation self-review inspected the complete implementation/test diff and
all document-client error consumers. It confirmed no backend/provider boundary
change, additional persistence, automatic question replay, processing restart or
publication replay. It added an explicit stop after logout and polling checks
for changed/missing native identity. The pre-commit review found no introduced
credentials, private configuration, temporary runtime artifacts, dependencies,
backend API changes or unrelated implementation edits. The preexisting working
tree changes remain for the operator's separate review.

Browser acceptance requires optional Playwright/Chromium, absent from the current
interpreter; the attempted runner fails before provisioning at the Playwright
import. No dependency was installed. ScriptRunner tests simulate identity and
native logout; signed-token integration tests exercise actual API authorization,
but neither substitutes for a completed real-browser OIDC reauthentication test.
Access loss is observed at the next request/poll, not by push revocation. Already
viewed content cannot be recalled from operator copies. Native Streamlit logout
also does not clear identities in other existing browser sessions. Reconnecting
after native authentication requires privately recording the session ID before
redirect; ordinary refresh restores the UUID hint and revalidates it.

Docker/Kubernetes checks are not applicable: containers, deployment configuration,
dependencies and backend code were not changed. No configured lint tool was found
and Ruff is not installed. No paid provider credentials or services were used.

## Working tree review

`git status --short` shows the task's modified frontend/client, existing client
tests, operator integration test, browser runner and operator guide, plus the new
frontend tests and this report. Preexisting Makefile, README, guide edits and
untracked local-launch/Phase 17h artifacts remain intact. `git diff --stat`
includes those earlier changes and omits untracked files:

```text
 Makefile                                        | 47 +++++++++----
 README.md                                       |  6 ++
 docs/operations/phase_18_local_document_demo.md | 92 +++++++++++++++---------
 tests/browser/document_journey.py               | 10 +++
 tests/integration/test_document_operator.py     | 62 +++++++++++++++++
 tests/unit/test_documents_client.py             |  1 +
 ui/documents_client.py                          |  6 +-
 ui/documents_view.py                            | 93 ++++++++++++++++++++-----
 8 files changed, 250 insertions(+), 67 deletions(-)
```

No commit or push occurred. No git settings, history or remote state changed.

## Frontend verification verdict before test-isolation continuation

Both requested fixes are implemented and supported by focused tests. Saved
answers come only from fresh authorized digest reads across polling reruns and
normal authorized page refresh. Native reauthentication makes no backend closure,
withdrawal, processing or publication call; signed-token recovery tests confirm
that an otherwise authorized backend session and its accepted answers survive.
Backend persistence and all approval/deadline/admission limits remain unchanged.
Final frontend/client/Chat-startup tests pass, and all collected document,
security and governance tests passed in the completed broad run. Overall broad
verification remains qualified by the unrelated umask-dependent launcher test;
real-browser polling/OIDC recovery acceptance remains blocked by missing
Playwright. No commit or push occurred.

## Test-isolation continuation — 18 November 2026

Only these files changed during this continuation:

- `tests/unit/test_documents_client.py` — restore the invoking test's original
  umask in `finally` after the CLI call and assertions.
- `tests/unit/test_local_apps.py` — explicitly set the temporary rejection
  fixture's mode to `0755` after creation, independent of the process umask.
- This report.

All earlier tracked and untracked work remains intact. No application, CLI,
Chat/RAG, digestion, authentication, governance or financial implementation was
changed. The production document-demo CLI still sets umask `077`. No commit,
push, reset, stash or clean occurred.

### Root cause confirmed and refined

The original two-test sequence reproduced the reported failure: starting with
umask `022`, `test_backup_cannot_recurse_into_its_runtime` followed by
`test_private_directory_and_repository_boundary` produced **1 passed, 1 failed
in 0.50s**, leaving umask `077`.

Restoring the invoking test's mask fixed that sequence and both affected modules
(**44 passed in 2.78s**). However, the subsequent uninterrupted full run still
reported **3,183 passed, 1 failed in 789.46s (13:09)**, with the same launcher
permission test failing. This established that the original diagnosis was
correct but incomplete: other existing in-process CLI harnesses also set `077`.

A second narrow reproduction used the existing, no-network missing-input test
`tests/unit/test_foundry_approval.py::test_live_cli_requires_new_inputs[--approval]`
followed by the launcher permission test. It reproduced **1 passed, 1 failed in
0.39s** and left umask `077`. The harness refuses missing approval input before
any execution; no paid or live inference was invoked.

The remaining problem was the permission test's implicit assumption that
`mkdir(mode=0755)` produces exactly `0755`. The final correction explicitly
applies `chmod(0755)` to that disposable test fixture. The fixture is deliberately
public so the existing application permission check must reject it. This neither
weakens that check nor changes any runtime's permissions. Keeping the caller's
`try/finally` restoration also prevents the document-demo test from leaking its
own process-state change. It restores the caller's actual mask, rather than
forcing every caller to use `022`.

### Final verification

- Originally failing test independently under umask `077`: **1 passed in 0.04s**.
- Original document-demo/launcher sequence under `022`: **2 passed in 0.41s**;
  the driver verified that umask was still `022` afterward.
- Document-demo test, separate CLI missing-input test, then launcher test under
  an initially restrictive `077`: **3 passed in 0.56s**; the driver verified
  that the caller's `077` mask remained intact.
- Affected modules plus both missing-input harness cases:
  `python -m pytest tests/unit/test_documents_client.py tests/unit/test_foundry_approval.py::test_live_cli_requires_new_inputs tests/unit/test_local_apps.py -q`:
  **46 passed in 2.82s**.
- `git diff --check`: **passed**. Compilation of both changed test files with
  bytecode directed outside the repository: **passed**.
- One uninterrupted full suite completed during this continuation with
  **3,183 passed, 1 failed**. It preceded the final explicit-mode fixture
  correction and therefore is not a final clean full-suite PASS. The remaining
  failure was reproduced and fixed by the targeted checks above; a second
  13-minute full run was not repeated for this test-fixture-only correction.

### Final status and remaining verification limits

The original failure is resolved in the final independent test, original ordered
sequence, additional CLI-contaminated sequence and affected regression tests.
The runtime's restrictive permissions remain unchanged. The complete full run
is recorded honestly as having preceded the final fixture correction; no clean
post-correction full-suite result is claimed. Manual frontend verification
remains with the operator. No browser or live-application acceptance was
repeated, no dependencies were installed, and no cloud or paid inference was
performed. Work stops here at the test-isolation correction.
