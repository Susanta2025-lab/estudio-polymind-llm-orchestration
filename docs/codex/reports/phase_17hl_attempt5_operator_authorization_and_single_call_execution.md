# Phase 17H–L — Attempt 5 operator authorization and single-call execution

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

26 October 2026. [Supplied prompt](../prompts/phase_17hl_attempt5_operator_authorization_and_single_call_execution.md).

**BLOCKED BEFORE LIVE EXECUTION — independent operator evidence is required.**
The user has authorized preparation and at most one gated inference call. Preparation
was performed; no live launcher was invoked, no inference request was made, and no
approval was signed or consumed. Engineering bindings match. Current deployment
allocation and local financial headroom were verified, but current commercial
applicability, complete consumer review, credential provenance, authenticated
operator identity, independent signing provenance and fresh approval remain
unestablished. Phase 17H remains PARTIAL; model acceptance is untested by this task.

## Current engineering and deployment evidence

The required handoff, F1 report, operator runbook and three implementation files
were read. Existing regression and compatibility evidence was reused. No C1–C7
audit, full regression, application feature work or engineering source edit was
performed.

The authoritative binding functions were recomputed with application environment
and implicit dotenv isolated, before-import socket/DNS denial, and an unusable
transport. The computation completed with exit 0 and zero network attempts.

| Binding | Recomputed SHA-256 |
| --- | --- |
| Executor | `82fc01aa0447d4be758124cec0120a06db49f139f69ee6425b51b8696a6ad26f` |
| Generation source | `7d387a8595cf63e2ac944a25c4987a1b37392aa4adba8889914acf51ff9f0f59` |
| Provider schema | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` |
| Inference configuration | `7eaa6b52ad387f9f0c82e318e9c74fa378ffda0baec85d0f7157cc4ab0553519` |

All four match the supplied bindings. The existing generation contracts, strict
schema, deterministic claim identifiers, application predicates, low reasoning
effort, 3,000 completion-token limit and 26,192-byte HTTP envelope are preserved.

Read-only Azure CLI queries on 26 October confirmed the active subscription
ECI-Development (`<AZURE_SUBSCRIPTION_ID>`), tenant
`<AZURE_TENANT_ID>`, and enabled account state. The explicit
deployment query returned `epolymind-gpt-54-mini`, provisioning state `Succeeded`,
OpenAI model `gpt-5.4-mini`, version `2026-03-17`, SKU `GlobalStandard`, capacity
30, and rate limits 30 requests and 30,000 tokens per 60 seconds. This confirms
allocation, not uncommitted capacity across every external consumer.

The new draft selects the supplied resource host with the existing adapter's v1
base path:
`https://epolymind-foundry-dev-susanta.services.ai.azure.com/openai/v1`.
Its request path remains `/openai/v1/chat/completions`. Historical authority
references were inspected as data only; no historical configuration, approval,
signing script, stale schema preparation helper or four-call launcher was used
for execution. The new draft does not carry forward the historical inference host.

## Existing authority and financial state

Existing security, governance and provider authorities were opened with SQLite
`mode=ro` and `PRAGMA query_only=ON`; their constructors, migrations and reservation
methods were not invoked. The existing registered scope was derived from pinned
trust identity using the unchanged scope algorithm, without constructing a
purported authenticated principal. Exactly one matching enabled user registration
was found, with `PUBLICATION_MANAGE` and matching trust identity. This verifies
stored registration, not fresh Entra authentication.

The pinned live-purpose approval trust and replay authority retain private ownership
and permissions. The public DER key fingerprint matches the established value
`35785596dd2f38a3ae5fc8eeb93015a1ba3c8b4f16f06a1d73fbe521f9657816`.
This establishes public-key consistency, not independent operator association.
Four persistent approval-consumption records remain present and untouched.

All four financial reservations are SETTLED. There are zero unresolved reservations,
zero active provider calls and zero provider calls in the preceding minute in the
existing local authority. Both owner and tenant allowances, calculated with the
existing evaluation policy and `impact()` function at preparation time, are:

| Allowance | Remaining |
| --- | ---: |
| Requests in the policy window | 16 |
| Daily tokens | 500,000 |
| Monthly tokens | 1,485,423 |
| Outstanding reserved tokens | 112,000 |
| Monthly EUR | 4.969124868004221809 |

The existing catalog serialized SHA-256 remains
`dad37bc0f349cdfbea16e25cae028a0b5042e4e3e3daac4f141f9b566c5bc65e`.
Its calculation for 25,000 input and 3,000 completion tokens is EUR
`0.028379091869065`. Local allowances cover that proposed reservation. These are
catalog arithmetic and local ledger findings, not a refreshed commercial quotation
or proof that zero fixed/additional charges remains defensible. The draft carries
the historical monetary terms as a proposal with `contract.approved=false`.
No balance, obligation, catalog, authority policy or replay history was reset.

## Concrete private preparation

New private review material was created at:

```text
<PRIVATE_OPERATOR_DIRECTORY>/
```

The directory is mode 0700; generated JSON files are mode 0600. Contents include
`configuration.draft.json`, `attestations.template.json`, `payload.review.json`,
`preparation-evidence.json`, synthetic extraction objects and an empty `audit/`.
New job and request identities were generated. The fixture uses the existing
`prepare_analysis()` function and deterministic `pdf(4, seed=1708)`, with the
existing registered scope, four extracted units and one first analysis with no
children. No reduction, Q&A or embedding stage was invoked.

| Prepared binding | SHA-256 |
| --- | --- |
| Fixture | `1be99e19a56040fb55c74682a19f874d4d4573f18d9f52a9a7ae19c8158ea92d` |
| Rendered request | `d1a9ad26a84ed848af18ebdba1eae894401cff337b0ce72d660cf8bc01b2c271` |

The regenerated inference configuration also matches the required fingerprint.
The stored payload review contains only the synthetic request and strict schema,
with the prescribed deployment, two messages, no streaming, low reasoning effort
and 3,000 completion tokens. A future final configuration must retain these
bindings and verify the freshly authenticated principal has this scope.

The draft's unapproved financial contract is intentionally rejected by
`SingleCallConfiguration.model_validate()` at `contract`; all nine attestations
remain null. No validated final configuration digest, configuration acknowledgement,
authenticated unsigned approval binding or signed artifact was produced. A raw
file hash must not be substituted for the missing final configuration digest.

Preparation used the inspected offline denial guard and settings isolation. It
completed with exit 0 and zero observed network attempts. Before/after SHA-256,
modes and modification times match for the three authorities, trust, public-key
file, repository `.env` and four replay records. Replay inventory is unchanged.
The preparation script remains outside Git at
`/tmp/polymind-attempt5-prepare-current.py`; it does not acquire identity, read the
private signing key, sign, consume approval or launch inference.

## Remaining operator gates and continuation

| Gate | Result |
| --- | --- |
| Target and allocation | Verified live; complete consumer/headroom confirmation still required |
| Financial enforcement and local headroom | Verified read-only; current commercial applicability and supported zero extras still required |
| Entra identity and permissions | Stored registration verified; no current authenticated principal |
| Active inference credential | Runtime credential variable absent; resource provenance and validity still required |
| Protected authority/trust/replay paths | Existing references and private storage verified; independent key association still required |
| Fixture/rendered request | Prepared for existing registered scope; final authenticated configuration still required |
| Fresh independent unused approval | Missing; historical single-call approvals are expired and ineligible |
| Window and nine attestations | Missing; no execution window is finalized |

The runtime operator-token variable is absent. The stored token's unverified expiry
hint is in the past; decoding it was used only to reject it as a freshness candidate,
never to authenticate. Historical approval expiry hints are also in the past; no
signature or eligibility was inferred from those hints. No current approval was
found in the existing single-call storage.

An asynchronous request asked for current pricing/zero-extra-charge applicability,
complete consumer headroom, inference-credential provenance, signing-key operator
association, and paths to any fresh protected token or approval. No secrets were
requested. Those external facts cannot be supplied by copying historical true
flags into this draft.

Continue through the existing
[single-analysis operator procedure](../../evaluation/phase_17hl_operator_approval.md#single-analysis-timing-and-preparation-handoff)
using this new draft. After current commercial evidence is established, the
operator can review the proposed financial contract. Authenticate through the
existing delegated Entra process and verify exact scope, permissions and trust
identity. Establish credential provenance and all nine fresh attestations before
using the existing offline finalizer to write a new final configuration. Review
its validated digest and configuration, then generate bindings with
`foundry_approval.bindings()` using the verified principal. Independent signing
must use audience `polymind-single-analysis-live`, the current pinned public trust,
a fresh unused approval ID, exact bindings and expiry equal to the configuration.
Do not run or repin historical signing scripts.

Immediately before the sole possible launch, revalidate current identity,
credential evidence, unused signature, local obligations and capacity. Require
`execution_not_before <= now < min(approval_expires, credential_valid_until)-600`
and the existing token/approval validity checks. The user authorization in this
task remains conditional on these gates. No paid call is justified by this report.
Once one call is attempted, inspect immutable outcome and accounting and stop;
failure, UNKNOWN usage or cleanup failure never authorizes another call.

## Review and validation

Self-review checked source binding preservation, endpoint and protocol selection,
read-only authority access, historical-data handling, synthetic scope binding,
financial arithmetic and the distinction between preparation and authorization.
No engineering change was necessary or made. Separate pre-commit review covers
only this prompt/report: no credentials, private keys, JWTs, actual owner identifiers,
synthetic payload contents, runtime databases or approval artifacts are included.
The private signing key was not read. Existing retention and reviewer decisions
are retained; durable authorities and replay records remain in their existing
storage.

Existing 426-test focused and 1,755-test full regression results are reused from
the handoff/F1 reports; they were not rerun. No pytest, compileall, Docker build or
Kubernetes operation was required for these documentation/private-preparation
changes. The newly executed validations are authoritative fingerprint computation,
Azure read-only account/deployment queries, read-only authority and allowance
checks, scope fixture rendering, deliberate unapproved-draft rejection, and
protected-artifact preservation checks. No application API, model contract,
dependency or provider-neutral boundary changed.

Final `git diff --check` passed (exit 0). Both new documents passed their separate
`git diff --no-index --check /dev/null <file>` checks with no diagnostics; exit 1
indicates the expected new-file difference. Local Markdown targets resolve, and
focused private-key/JWT/credential-assignment scans found no matches in either
deliverable. Private packet reinspection confirmed mode 0700 directory, 0600 JSON,
empty audit, zero approval files, unapproved contract and nine null attestations.

`git status --short --branch` reports `master...origin/master`, 20 modified tracked
files, 114 untracked entries and zero staged entries. Two new untracked entries
are this task's prompt and report; existing work is retained. `git diff --stat`
remains 20 files changed, 832 insertions and 79 deletions, identical to the initial
tracked statistic. Untracked files do not appear in that statistic. No commit,
push, staging or Git remote mutation occurred.
