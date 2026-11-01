# Phase 17H-L — preflight observability and operational timing hardening

**PASS — offline implementation and validation complete. No live attempt prepared or executed.**

Date: 2026-10-17. Branch: `master`. Existing dirty repository work is preserved.

## A. Initial assessment

Read the existing single-call failure diagnosis and offline harness reports, then inspected
`foundry_single_call`, `foundry_approval`, `foundry_l1`, `security.identity`, security
authorization, governed execution, related tests and the operator runbook. The historical
failure's exact cause remains unresolved; this change does not establish a network,
credential, argument or timing explanation for that invocation.

The CLI discarded exceptions and suggested private audit evidence even when none existed.
Configuration was already required by argparse, but acknowledgement was not explicitly
required for live mode, and missing approval/trust reached a generic exception. The window
validator required strictly more than 600 seconds before both deadlines, without displaying
the resulting launch cutoff.

Actual ordering includes an important additional check: after configuration/window/private
paths/credential/acknowledgement, OIDC and principal scope checks are followed by RSA
verification **before** registered security authorization. Fixture construction and digest
checks precede governance/admission construction and RunGuard replay checking. RSA is
verified again immediately before consumption; the durable live marker precedes document
registration, provider construction and governed execution. This order remains intact.
Fixture preparation writes object storage; authority authorization can write security audit
records; constructing authorities/RunGuard can initialize state. Diagnostics do not call any
of these solely to record a failure.

## B. Implementation summary

| File | Change |
| --- | --- |
| `tests/performance/foundry_single_call.py` | Invocation-local diagnostic tracker, explicit stage boundaries, sanitized CLI failures, private exclusive diagnostic files, required live arguments and UTC timing review |
| `tests/integration/test_single_call_preflight.py` | 28 offline regression cases, synthetic identities/transports and isolated authorities |
| `tests/integration/test_single_call_harness.py` | Existing CLI test supplies the now-required digest and accepts the optional diagnostic keyword in its fake launcher |
| `docs/evaluation/phase_17hl_operator_approval.md` | Single-analysis handoff, exclusive deadline, key-path preparation and duration constraints |
| `docs/codex/prompts/phase_17hl_preflight_observability_timing_hardening.md` | Condensed phase requirements, explicitly labeled as such |
| This report | Findings, verification and new fingerprints |

No shared provider, identity, authority, schema or financial implementation was changed by
this task. The single-call path expands the existing `verify_approval` checks into visible
boundaries, retaining digest, OIDC, scope/permission and RSA verification in the same order.
The legacy L1 helper remains unchanged. Existing positional launcher inputs still work;
an optional keyword carries invocation-local diagnostics to the CLI. Unexpected exceptions
still propagate to direct Python callers; the CLI and diagnostic files never serialize them.

## C. Diagnostic taxonomy

All stages/categories emitted by the implementation are source literals; no exception message,
claim, endpoint, path, credential, approval content or response body is copied into them.
Expected exception types receive the applicable category; all other errors retain
`unexpected_internal_error`. Categories describe a proven boundary, not an inferred root cause.

| Stage | Expected failure category |
| --- | --- |
| `configuration_loading` | `configuration_unavailable` |
| `configuration_validation`, `configuration_finalization` | `invalid_configuration` |
| `execution_window` | `window_not_started`, `window_insufficient_remaining_time`, or broad `window_requirements_not_met` |
| `private_path_validation` | `private_path_invalid` |
| `approval_loading` | `approval_unavailable` |
| `credential_presence` | `credential_missing` |
| `configuration_acknowledgement` | `approval_digest_mismatch` |
| `operator_identity_verification` | `operator_authentication_failed` |
| `operator_scope_verification`, `security_authorization` | `operator_authorization_failed` |
| `signed_approval_verification` (both checks) | `approval_verification_failed` |
| `fixture_preparation` | `fixture_validation_failed` |
| `fixture_digest_verification` | `fixture_mismatch` |
| `governance_initialization` | `governance_unavailable` for filesystem errors; other unexpected failures remain generic |
| `replay_protection` | `replay_rejected` |
| `approval_consumption` | `approval_consumption_failed` |
| `live_marker_creation` | `live_marker_failed` |
| `provider_initialization`, `provider_execution` | `unexpected_internal_error` for escaping exceptions; existing outcome taxonomy remains authoritative for handled execution failures |

Console failures show state, stage, category and provider-attempt status. Before execution,
`NO` follows from control flow. On entering `execute_stage`, status becomes `UNKNOWN`:
entering governed execution is insufficient evidence of an HTTP attempt. An escaping error
then reports `FAILED`, rather than claiming preflight blocked the request. Existing successful
or handled-failure outcomes retain their state/call summary and durable execution evidence.

Optional `preflight-diagnostic-<random UUID>.json` records contain only schema version
`single-call-preflight-diagnostic/1`, state, stage, category, nullable provider-attempt flag,
and `approval_consumption_entered`. The latter is conservative: entering consumption does
not prove that its write completed. These files are observations, never authorization,
financial state, replay records or replacement live outcomes.

Persistence rechecks the existing owner/mode/type/symlink/outside-repository path validator.
It neither creates the audit directory nor uses a fallback location. Files use existing
exclusive creation, no-follow, mode 0600 and file/directory fsync. Separate failures get
separate names; an invocation attempts persistence only once. Existing evidence is never
overwritten. An invalid/unloaded configuration cannot select a diagnostic directory. A
validated configuration can receive early-window evidence only if its audit directory is
safe. Persistence failure preserves the original blocked operation and console diagnostics.
A partial file remains possible on filesystem/fsync failure; diagnostic completeness is not
a security prerequisite and does not grant permission to retry.

## D. Timing improvements

Offline configuration review and successful finalization now include `execution_window`:
review time, execution start, approval expiration, credential-use deadline, exclusive launch
cutoff, required margin, remaining launch seconds and timing eligibility. Times are explicit
UTC ISO 8601 values. Null deadlines cannot produce an eligible window.

The calculation is `min(approval_expires, credential_valid_until) - 600`. Eligibility is
`execution_not_before <= now < cutoff`; the cutoff itself is rejected. The live validator
uses one clock sample, shared with its diagnostic classification. Timing review is not an
authorization, identity or capacity check. Negative remaining time remains visible. API-key
credential-use validity remains attested rather than independently measured.

The generic finalizer accepts explicit timestamp attestations, not a duration option. No
window was extended or created. Existing RSA policy caps issue-to-expiration at 86,400
seconds, retains `iat <= nbf < exp`, and requires the exact configured expiration. All
credential, token and margin checks remain. The historical signer additionally pins its
1,800-second window and cannot authorize a different duration unchanged.

## E. Security verification and OIDC assessment

The historical operator signer was read as source only. It pins packet/review/configuration
hashes, requires explicit `SIGN`, uses hidden passphrase input, checks the trusted public
fingerprint and the signing key's public fingerprint before signing, rechecks prerequisites,
verifies the generated signature, and writes exclusively. It was neither executed nor
modified. No private key was read. The runbook recommends having the existing local path
ready before fresh credentials are obtained; it adds no signing automation.

OIDC has a bounded 3-second client timeout, no redirects/environment proxies, bounded JWKS
size, refresh controls and sanitized `authentication_required` failures. A new verifier can
fail closed on transient transport errors. That is an availability sensitivity, not evidence
of a historical defect or grounds for changing trust behavior. Offline regressions exercise
both injected fetch failures and the real `_fetch` path with a fake HTTP client raising
ReadTimeout/ConnectError, verify normalized failures and no installed keys, and assert the
unchanged timeout/redirect/proxy settings. No retry, caching or timeout change was made.
Issuer, audience, lifetime, signature, scope, roles and registered-principal checks remain.

Existing RSA binding, double verification, exclusive consumption, replay marker, RunGuard,
governance reservation/settlement and provider admission protections remain. Tests cover
preflight non-consumption/non-inference, existing replay/accounting behavior, and uncertainty
if an exception escapes after execution entry. The single-call limit, no retry policy,
600-second margin, EUR 5 ceiling, pricing/token budgets, strict schema and domain validation
are unchanged. Real authorities, approvals, historical packets and cloud resources were
not modified. Synthetic tests generate fixture signatures and mutate temporary authorities
only; no real signing, authentication or provider call occurred.

## F. Offline validation and reviews

Final focused regression command:

```text
python -m pytest tests/integration/test_single_call_preflight.py tests/integration/test_single_call_harness.py tests/unit/test_single_call_diagnostics.py tests/unit/test_foundry_approval.py tests/unit/test_security_entra.py tests/unit/test_governance.py -q --disable-warnings --maxfail=2
```

**270 passed, 0 failed, 0 skipped, in 32.15 seconds.** New integration cases deny network
connections and use synthetic fixtures. Existing relevant suites retain their fake transports
and isolated authorities. The first narrower run had 69 passes and one assertion failure:
floating-point epoch subtraction needed a microsecond absolute tolerance. The test was
corrected; eligibility and strict comparison were not weakened.

`git diff --check` passed. `PYTHONPYCACHEPREFIX=/tmp/polymind-preflight-pycache python -m
compileall -q .` passed. No configured lint tool was found in the inspected project
configuration locations. Docker/Kubernetes checks are inapplicable: no dependency, image,
deployment or service configuration changed. The unrelated full test suite was not run.

Implementation self-review compared the complete harness change with its saved starting
source and inspected new tests/docs. It checked duplicate RSA verification order, unchanged
exceptions for direct callers, evidence exclusion/permissions, no new authority side effects,
resource cleanup, missing arguments, exact boundaries and conservative request status.
A single clock sample avoids disagreement between window enforcement and its diagnostics.
Separate pre-commit review found no introduced credentials, private key material, raw exception
logging, debug output, dependencies, temporary repository artifacts or unrelated edits.
Historical files and the existing dirty tracked changes were left intact.

## G. Fingerprint changes

Calculated before and after using the official `executor_digest()`,
`generation_contract_digest()` and existing provider-schema binding:

| Binding | SHA-256 |
| --- | --- |
| Old executor | `5624647a3f1a0fb559c85ca0ca06997320d42f9585b7528055505c12dbcca10f` |
| New executor | `584ad53eec07266b16c0b5b197972ddf03abc198e859e5133c0f563fe1b7a4b2` |
| Generation, unchanged | `a06c39717a3f7c78115e42ec12aaf7c4417cda498018ab8ec56c7927a864fa10` |
| Provider schema, unchanged | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` |

The executor hashes Python sources under documents/governance/security/llm/tests/performance.
Only `foundry_single_call.py` changed in that set during this task. Tests and documentation
are outside that binding. Updating a future configuration's executor hash changes its whole
configuration digest and RSA execution binding. No future configuration digest was created:
that requires separately reviewed fresh inputs. Historical signed artifacts remain unchanged
and are **unsuitable for this modified execution contract**. No replacement approval was
prepared or signed.

## H. Future operator handoff

Follow the updated operator runbook: static validation/configuration inspection; have the
existing private-key path ready locally; verify non-expiring artifacts; obtain separately
authorized fresh identity/credential evidence; finalize timestamps and review the exact new
digest; independently confirm and sign with pinned public-fingerprint verification; verify
the signature; check the exclusive launch cutoff; invoke the one-call launcher once only
after explicit operator authorization. Avoid repeated static inspections inside the window.
No step involving real authentication, signature preparation, approval consumption or
inference was performed by this implementation task.

## I. Remaining limitations and repository state

The historical root cause is still unknown. The new diagnostics cannot reconstruct discarded
exceptions or distinguish all underlying OIDC failures. A missing diagnostic file is not proof
that nothing happened. Filesystem interruptions and hostile-owner races retain the existing
single-host private-path threat model; diagnostics do not replace durable replay/governance
state. Azure strict-schema acceptance and downstream compatibility remain unverified live.

Final `git status --short --branch` reports dirty `master` with the existing 18 modified
tracked files and prior untracked artifacts, plus the phase additions/edits listed above.
`git diff --stat` remains **18 files changed, 499 insertions(+), 44 deletions(-)**, entirely
pre-existing tracked changes. This task's implementation, tests and documentation are all
untracked files in the starting repository or new untracked additions, so that statistic
does not show this task's changes. Nothing was staged. **No commit or push occurred.**
Work stops after offline validation and reporting; no next execution phase is initiated.
