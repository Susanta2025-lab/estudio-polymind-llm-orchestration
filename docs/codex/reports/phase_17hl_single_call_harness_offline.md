# Phase 17H-L — Single-call Azure compatibility harness, offline

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

**PASS — SINGLE-CALL HARNESS IMPLEMENTED AND VERIFIED OFFLINE; OPERATOR AUTHORIZATION PENDING**

16 October 2026, existing `master`. This report authorizes no live action. Existing
tracked and untracked work was retained; nothing was staged, committed or pushed.

## A. Architecture

`tests/performance/foundry_single_call.py` provides the independently versioned
`polymind-single-analysis/1` execution capability. It reconstructs the existing
four-page fixture (`phase17h-pdf/1`, seed 1708), extraction, EvidenceIndex, plan and
first managed analysis request. It renders that request through
ManagedSynthesisInference and executes it through GovernedExecution. It does not
run the worker's remaining plan, the four-call L1 launcher, reducers, publication,
grounded Q&A or L2. Planning additional nodes does not execute them.

The existing SecurityAuthority, Entra OIDCVerifier, GovernanceLedger,
SQLiteInferenceAdmission, RunGuard, pricing catalog, evaluation scope and RSA
approval trust remain the authorities. No parallel ledger, policy, identity store
or migration was introduced. Synthetic tests create isolated temporary authorities;
private preparation accesses the real authorities read-only.

The frozen SingleCallConfiguration requires exactly one attempt, a literal maximum
of one call, aggregate 25,000 input / 3,000 output reservations and the exact approved
catalog. RunGuard durably records its one allowance before downstream provider
admission. GovernedExecution's reservation transitions prohibit duplicate execution
of the same request identity. Existing approval consumption and an exclusive,
fsynced run marker provide additional replay fences. Failure, timeout and restart
never replenish that allowance. These are the project's existing single-host
transaction/replay guarantees, not protection against a hostile filesystem owner.

The RSA workflow retains its existing issuer, RS256 header validation, pinned
public trust, registered operator binding, expiration checks and durable consumption.
The new audience is `polymind-single-analysis-live`. Signed bindings additionally
name the executor, its implementation digest, generation digest and provider-schema
digest. The whole configuration digest also binds deployment, authority paths,
owner/tenant, job/request identities, fixture and rendered request. Legacy
`polymind-l1-live` signatures cannot authorize this workflow. Legacy configuration
serialization and approval bindings are unchanged when no executor field exists.

A live CLI invocation must explicitly use `--live`, load a private validated
configuration, pass its exact digest, supply independent RSA approval/trust, and
verify a fresh Entra access token through a newly constructed verifier. Registered
identity authorization precedes execution. Credential/window and capacity
attestations must be present and current. The same ledger and shared provider
admission enforce historical consumption and available capacity before inference.
As in the existing launcher, an approval can be consumed before a later admission
fails; it cannot then be reused.

## B. Implementation and validation sequence

Files changed by this task:

| File | Change |
| --- | --- |
| `tests/performance/foundry_single_call.py` | New bounded configuration, independent source binding, preparation, single-stage composition, private durable audit, offline finalization and explicit live CLI |
| `tests/performance/foundry_approval.py` | Additive executor bindings and separate audience; preserve legacy behavior |
| `governance/execution.py` | Attempt both financial and admission cleanup; preserve the primary exception when cleanup also fails |
| `llm/bounded_http.py` | Bounded, closed-taxonomy rejection diagnostics for 400/422 |
| `tests/integration/test_single_call_harness.py` | New end-to-end synthetic harness tests |
| `tests/unit/test_single_call_diagnostics.py` | New sanitized diagnostic envelope tests |
| `docs/codex/reports/phase_17hl_single_call_harness_offline.md` | This report |

The provider sends the actual converted schema, `response_format.type=json_schema`,
name `polymind_stage_result`, `strict=true`. The application subsequently calls the
unchanged `validate_result`, including strict Pydantic StageResult decoding, UUIDs,
identity/order/origin, evidence membership and coverage, lineage, qualifications,
contradictions, string constraints, canonical serialization and byte limits. No
output repair, extra-field removal, evidence substitution or truncation exists.

The provider/application fields in `outcome.json` distinguish observed strict
provider completion, evidenced schema rejection and unobserved acceptance from
application acceptance, failure and validation not reached. Provider completion is
recorded before accounting cleanup, so settlement failure cannot erase that fact.
The audit retains result hash/canonical size on success, sanitized failure category,
accounting-failure marker, run records and financial evidence. It excludes model
response text, prompts, source text, bearer tokens and exception messages.

Known actual usage settles before downstream application validation. Malformed
response envelopes and truncation retain valid reported usage. Missing/inconsistent
usage remains unresolved and stops the run. A settlement failure leaves its durable
reservation available for reconciliation; primary provider errors survive secondary
cleanup failures. Both accounting cleanup paths are attempted. Successful provider
execution with failed accounting is itself terminal failure. Audit-read failures
also force failure while retaining an already-known primary category. The CLI
returns nonzero for a terminal failed outcome, after audit finalization.

Durable JSON evidence uses exclusive creation, 0600 permissions, file fsync and
parent-directory fsync. Failure to persist evidence fails the command. An abrupt
kill or filesystem failure can prevent a final outcome file; existing durable
approval/run markers and RESERVED/ADMITTING/STARTED obligations still prevent
unattended replay. No claim of an atomic transaction spanning these independent
existing databases is made.

HTTP 400/422 diagnostics read at most 4,096 bytes within the existing bounded
transport deadline. Only status and a closed reason are retained. A schema-specific
code plus response-format parameter, or the recognized invalid-schema prefix with
its matching code/parameter, establishes `strict_schema_rejected`. Unknown,
malformed or oversized error envelopes retain `request_configuration`; status alone
never establishes a schema rejection. Existing authentication, overload, timeout,
transport and protocol categories remain unchanged. No error prose is logged.

The real session uses requests, disables environment proxies, mounts an HTTPS
HTTPAdapter with retry total zero, disables readiness retries, and the existing
bounded request disables redirects. There is no new HTTP client or fallback model.

### Limits and cost

| Control | Bound |
| --- | --- |
| Attempts / fallback models / model retries | 1 / 0 / 0 |
| Per-call and aggregate input/output reservations | 25,000 / 3,000 tokens |
| Planning context | 28,000 tokens |
| Provider content | 10,000 UTF-8 bytes |
| Canonical result | 10,000 ASCII bytes |
| HTTP envelope | 26,192 bytes |
| Monthly ceiling / evaluation policy | EUR 5 / `polymind-evaluation/1` |

The real prepared catalog was checked against its approved digest and version
`phase17hl-pricing-eur-202610/1`. Recalculation using Decimal catalog arithmetic:

```text
(25000 × 0.659978880676 + 3000 × 3.959873284055) / 1000000
= EUR 0.028379091869065
```

This is the maximum inference reservation, not a promise of available capacity or
actual cost. The financial ledger reserves the conservative rendered input estimate
and output allowance; RunGuard also records the full authorized token bounds.
Historical financial records were not refunded, reset or rewritten. Current
read-only capacity evidence is private; actual admission must recheck capacity.

### Fingerprints

Both supplied starting fingerprints were verified before editing. The starting
generation digest was
`6f936342efb8e22faf23d59ebf71f7846d3255692d398c27d1e6a449ef41e247`.
Only `llm/bounded_http.py` changed among the existing generation-digest source
list. Thus the final generation hash changes without changing schema, prompt or
application validators. Historical reports/contracts remain unchanged; stale
approvals fail validation rather than being silently promoted. The historical
preparation helper remains pinned to its historical generation hash.

| Final binding | SHA-256 |
| --- | --- |
| Generation | `a06c39717a3f7c78115e42ec12aaf7c4417cda498018ab8ec56c7927a864fa10` |
| Provider schema, unchanged | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` |
| Single-call executor | `5624647a3f1a0fb559c85ca0ca06997320d42f9585b7528055505c12dbcca10f` |
| Prepared configuration | `3c2ce6dd5c0f886e0e6d601f5d12a7b4d6fdb65923141bad3df08a3486a1c675` |

The executor hash covers sorted file hashes of all Python source under documents,
governance, security, llm and tests/performance. This deliberately broad binding
includes the executor, approval utilities, accounting and execution dependencies.
Unrelated edits within those directories will also require renewed configuration
review. The rendered first-stage request and fixture hash exactly match the prior
preparation; fresh job/request UUIDs identify the new run.

## C. Verification

**146 passed, zero failed, in 28.31 seconds** on the final focused run:

```text
python -m pytest tests/integration/test_single_call_harness.py \
  tests/unit/test_single_call_diagnostics.py \
  tests/unit/test_governance.py tests/unit/test_foundry_approval.py \
  -q --disable-warnings --maxfail=2
```

The actual invocation used `pytest.main` with those arguments after globally
replacing socket connect/connect_ex/sendto and connection/DNS helpers with rejecting
functions. New modules also install their own network-denying fixtures. There were
67 new harness/diagnostic cases and 79 directly relevant shared-governance/approval
regressions. The previous 214-test structured-output suite, seven-test preparation
suite and full repository suite were not rerun. An initial new-test run had one
expectation mismatch (`worker_failed` is the existing interrupted-execution category);
the assertion was corrected and the final run passed.

Coverage includes the exact strict schema/deployment/one-POST request, valid result,
eight forbidden fields, malformed and nonexistent evidence UUIDs, lineage, claim
identity/order/origin, qualifications/contradictions and canonical overflow.
Provider cases include HTTP 400/422, authentication/rate limits, timeout, transport
failure, truncation, malformed envelope and absent/inconsistent usage. Every such
execution sends at most one fake request and cannot replay. The actual session
adapter's retry total is separately verified without contacting a server.

Security coverage includes absent/invalid/expired approval, wrong operator,
configuration/generation/executor/schema mismatch, legacy audience, scope mismatch,
replay after restart, exact signed bindings, and valid synthetic Entra/RSA execution.
Existing approval tests additionally cover concurrent replay and fsync failure.
Other tests prove no forbidden workflow entry point is called, exhausted governance
capacity prevents a provider call/new reservation, known settlement is idempotent,
application failure still settles, interrupted/unknown work remains unresolved,
settlement/audit-read failure retains the primary error, and failed CLI outcomes
return nonzero. Offline preparation/finalization produces no consumption or call.

`git diff --check` passed. `PYTHONPYCACHEPREFIX=/tmp/polymind-single-call-pycache
python -m compileall -q .` passed, avoiding unrelated bytecode ownership changes.
No configured lint tool was identified. No dependencies, Docker or Kubernetes
configuration changed; Docker/Kubernetes validation was inapplicable.

Implementation self-review examined the complete task diff and new modules,
compatibility, source binding, private-file handling, single-call enforcement,
unknown usage, cleanup errors and audit finalization. Findings addressed during
review included capturing provider completion before settlement and preserving
primary errors when audit collection fails. Separate pre-commit review found no
introduced secrets, raw error logging, private keys, committed private artifacts,
new dependencies, dead fallback paths or application-validator changes.

## D. Private handoff and next operator action

Installed handoff:

`<PRIVATE_OPERATOR_DIRECTORY>/HANDOFF.md`

All packet directories are 0700 and files 0600. It contains the validated prepared
configuration, null attestation template, schema, first-stage request, extraction
objects, read-only capacity observation, preservation hashes and manifest. Its label:

**PREPARED — NOT SIGNED — NOT AUTHORIZED FOR LIVE EXECUTION**

The implementation/configuration capability is complete; live window, credential
and capacity attestations intentionally remain null. This configuration cannot
launch until the operator supplies them through offline `--attestations --output`
finalization. No timestamp was invented or inherited. That creates a new exact
configuration digest; only that final digest may be reviewed and signed.

Before a live call, obtain separate authorization, fresh Entra verification, current
credential/audience/window and capacity attestations, registered identity/trust
agreement, and an independently signed approval with the new audience and execution
binding. Follow the private handoff's validation/finalization commands and existing
operator-controlled signing workflow. Only afterward may an explicitly authorized
`--live` invocation verify and consume that approval and attempt one request.
Never pass this configuration to foundry_l1 or reuse earlier approvals.

Remaining uncertainties are external: Azure acceptance of the actual schema's
nesting boundary, current deployment/credential validity and available live
capacity. No deployment discovery or live compatibility claim is made. A successful
single analysis would not establish four-call L1, publication/Q&A or L2 readiness.

## E. Safety and repository state

| Action | Real operations |
| --- | ---: |
| Azure inference calls | 0 |
| Azure infrastructure changes | 0 |
| Entra authentication | 0 |
| Operator RSA signatures/private-key access | 0 |
| Approval consumption | 0 |
| Cloud spending | 0 |
| Governance migrations/policy changes | 0 |
| L1 Attempt 4 execution | 0 |
| Git staging/commits/pushes | 0 |

Signing/authentication/consumption tests use only existing ephemeral synthetic
fixtures and temporary authorities. Preparation installed a socket-denying audit
hook. The historical packet, referenced real authority files, pinned public trust
and existing replay records were hashed before/after preparation and installation
and remained unchanged. No historical audit was edited.

Final `git status --short --branch` remains dirty `master`, with the user's original
work plus the task changes listed above. `git diff --stat` reports **18 tracked files
changed, 499 insertions, 44 deletions**, including pre-existing work. Of those tracked
files this task changed only governance/execution.py and llm/bounded_http.py;
foundry_approval.py was already untracked. New untracked files are omitted from
Git's diff statistic. No commit or push occurred.
