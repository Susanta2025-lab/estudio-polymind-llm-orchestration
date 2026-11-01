# Phase 17H-L — Azure strict-schema live compatibility

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

## A. Test status

**BLOCKED — OPERATOR APPROVAL OR GOVERNANCE PREREQUISITE**

16 October 2026, existing `master`. **Azure inference calls: 0.** No provider
acceptance or application-validation result exists for this experiment.

The existing `LaunchConfiguration` explicitly requires four calls, and its live
composition proceeds through digestion, publication and Q&A. It cannot safely be
used for this authorization. The existing RSA verification/consumption utilities
are reusable, but there is no complete single-stage governed launcher/approval
configuration. In accordance with the prompt's preparation-only fallback, this
phase adds only a small offline preparation helper and stops for operator handoff.
No attempt was made to edit or reuse Attempt 3's signed approval.

The prepared packet is **non-executable, not a signable JWT, and not a finalized
launch configuration**. Fresh Entra verification, credential/window attestations,
a finalized one-stage executor bound into the configuration, and independent
operator RSA signing remain outstanding. Persisted identity agreement is not
fresh authentication. No credential lifetime or old approval window was reused.

## B. Request contract

Both authorized fingerprints were recomputed from current source before preparation
and again during final verification; both match exactly:

| Contract | SHA-256 |
| --- | --- |
| Generation | `6f936342efb8e22faf23d59ebf71f7846d3255692d398c27d1e6a449ef41e247` |
| Converted provider schema | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` |

The target remains `epolymind-gpt-54-mini`, GPT-5.4 mini version `2026-03-17`,
GlobalStandard, Spain Central. Existing local deployment configuration and `.env`
endpoint/model mapping agree. No fresh Azure resource discovery was performed.
The adapter interface is `/openai/v1/chat/completions`; **no endpoint was contacted**.
The prepared response format is `json_schema`, name `polymind_stage_result`,
`strict=true`, with the real converted schema from `llm/azure_schema.py`.

Inspection and the reused two-layer evidence establish 22 fields in four closed
object schemas, all fields required, retained nested types/local references and
nullable unions. Unsupported string constraints are removed only by the provider
converter; Pydantic and domain validation source is unchanged by this task. The
exact schema digest confirms no substitute or flattened schema was prepared.
The documented nesting risk remains five containers below root, six including
root, and three object levels. Only a live request can settle Azure's acceptance
of this exact boundary; this report makes no new documentation compatibility claim.

Prepared limits: one call, 25,000 input-token reservation, 3,000 completion tokens,
28,000 planning context, 10,000 UTF-8 provider-content bytes, 10,000 canonical ASCII
bytes, and 26,192 HTTP-envelope bytes. No fallback or retry is configured in the
review material. `Contract.attempts=1`, aggregate input/output limits are
25,000/3,000, and `fits(2)` is false. Its pre-existing EUR 5 ceiling remains
unchanged; the one-call token/count bounds determine the exact reservation.

`tests/performance/foundry_schema_probe.py` uses the existing extraction, planning,
EvidenceIndex, DigestionHandler request construction and managed rendering path.
It prepares only the first analysis request from fixture `phase17h-pdf/1`, seed
1708, four pages. The PDF hash remains
`1be99e19a56040fb55c74682a19f874d4d4573f18d9f52a9a7ae19c8158ea92d`.
Four source pieces resolve against the real evidence index. The rendered input
estimate is 10,903 tokens, inside the reservation. The plan contains subsequent
reducers, but none are executed. Fresh experiment, job and request UUIDs are in
the private packet; they do not create durable admitted jobs or reservations.

Private artifacts are under:

`<PRIVATE_OPERATOR_DIRECTORY>/`

They include the first-stage request, full converted schema, managed settings,
financial contract, existing authority/configuration references, unsigned review
packet, read-only capacity evidence, extraction/plan objects, preservation hashes
and `HANDOFF.md`. All directories are 0700 and files 0600. The review packet digest
is `6c8d95c26ab2b5accde5a007ab33e695d11938241475f8a873d3f0c5a1c9eb3c`.
It deliberately records null credential/approval expiration and executor binding.
This digest must not be represented as a finalized execution authorization.

## C. Validation results

| Check | Result |
| --- | --- |
| Provider acceptance / HTTP status | Not attempted / unavailable |
| Provider structural response validation | Not reached |
| Raw and canonical response size | Unavailable; no response |
| Pydantic / UUID validation | Not reached on live content |
| Evidence membership, stage/claim identity, coverage, qualification, contradiction and lineage | Not reached on live content |
| Finish reason / refusal / truncation | Unavailable |
| Source evidence preparation | Passed |
| Fresh Entra operator authentication | Outstanding |
| New RSA signature / approval consumption | Neither performed |

The existing bounded HTTP method has one POST and disables redirects. Its HTTP
400/422 path discards the rejection body and emits a generic configuration error.
A future one-stage executor must retain safe status/rejection diagnostics through
the existing transport instrumentation before distinguishing schema rejection
from other request errors. No new HTTP client or speculative error-body logging
was introduced here. Retry behavior of the eventual live session must be checked
and pinned to zero before signing/execution; no live session was constructed here.

Seven new focused offline tests passed in 0.49 seconds. They cover exact catalog
cost, one-call bounds, no mutation of old contract data, changed catalog rejection,
incompatible financial inputs, generation/schema drift, deterministic first-stage
rendering, fresh identifiers and a provider stub that cannot execute. Network
connections/DNS are blocked in these tests; private preparation also installs a
network-denying audit hook. The previously verified 214 tests were not rerun.

## D. Accounting and governance

Read-only SQLite queries with `query_only=ON` verified authority integrity, active
`polymind-evaluation/1`, approved scope, exact `.env` policy/catalog/provider/OIDC
agreement, pinned RSA trust versus the registered principal, shared quota key,
and no active/recent-minute provider calls. The principal is registered, enabled
and has the required publication-management permission. This does not authenticate
a current operator session. No authority constructor/migration or admission was
used to produce the capacity snapshot.

Catalog `phase17hl-pricing-eur-202610/1` retains digest
`dad37bc0f349cdfbea16e25cae028a0b5042e4e3e3daac4f141f9b566c5bc65e`.
Exact maximum inference cost is:

```text
(25000 × 0.659978880676 + 3000 × 3.959873284055) / 1000000
= EUR 0.028379091869065
```

| Accounting item | Result |
| --- | --- |
| New Azure inference calls | 0 |
| Actual input/output usage | Unavailable; no inference |
| Planned maximum reservation | EUR 0.028379091869065 |
| Actual reserved / settled experiment cost | EUR 0 / EUR 0 |
| Experiment reservation/settlement state | Not created / not applicable |
| Unresolved existing obligations | 0 at observation |
| Existing settled history | 3 calls, 10,108 tokens, EUR 0.020906810982050014 |
| Remaining monthly cost, owner and tenant | EUR 4.979093189017949986 |
| Remaining rolling requests, owner and tenant | 14 |
| Remaining UTC-day tokens, owner and tenant | 497,074 |
| Remaining UTC-month tokens, owner and tenant | 1,489,892 |
| Remaining simultaneous token reservation capacity | 112,000 |

Observation timestamp: Unix 1792153399 (2026-10-16 12:23:19 UTC). These are
observations, not reserved capacity. Admission must recheck them after operator
participation. The packet was installed later following sandbox approval; final
hash checks confirmed protected histories/configuration remained unchanged.
Historical obligations were neither refunded nor reset. Unknown future usage
must retain the existing fail-closed unresolved accounting behavior.

## E. Next engineering action and review

This result does **not** establish Azure schema compatibility or support preparation
of Attempt 4. Follow the private handoff: complete the isolated first-analysis
executor with existing GovernedExecution, one-call RunGuard, bounded provider,
real validate_result and settlement; preserve independent structural/application
outcomes and safe rejection diagnostics. Bind its implementation and exact final
configuration before operator signing. Obtain fresh verified Entra identity and
current credential/window attestations, then use the existing operator-controlled
RSA bindings, verification and durable consumption workflow. Never run the
four-call launcher using this packet. No private key was accessed or signature
created. The explicit instruction to stop if a compliant one-call approval path
is absent is the reason this preparation does not perform live inference.

Self-review checked new files, existing execution/approval consumers, provider
boundaries, fail-closed hash checks, read-only authority access and absence of an
execution path in preparation. No existing interfaces, validators, generation
source files, runtime configurations or accounting implementations were changed.
Separate pre-commit review found no credentials, raw responses, private identity
bindings or generated audit artifacts in the new repository files. The only new
repository files are the preparation helper, its focused tests and this report.
No dependencies or Docker configuration changed; Docker validation is inapplicable.

Final validation: focused tests above; `git diff --check` and external-cache
`python -m compileall -q .` passed. Private artifact manifest/permissions,
preservation hashes and both authorized contract fingerprints passed final checks.

## F. Safety and repository state

Azure inference calls **0** (maximum authorized: 1); Azure infrastructure changes
**0**; governance migrations **0**; financial ceiling increases **0**; automatic
retries **0**; RSA signing without operator participation **0**; Attempt 4 calls
**0**; L2 calls **0**; approval consumption **0**; Git staging/commits/pushes **0**.

`git status --short --branch` retains existing dirty `master`, all previous tracked
and untracked work, and the three new files named above. `git diff --stat` remains
**17 tracked files changed, 446 insertions, 38 deletions**, entirely pre-existing
tracked work; the new files are untracked and are excluded from that statistic.
No commit or push occurred.
