# Phase 17H v5 execution window renewal and RSA authorization

Recorded 9 November 2026 UTC. This is an operator continuation, with no application
implementation change. The [task record](../prompts/phase_17h_v5_execution_window_renewal_and_rsa_authorization.md)
preserves the requested gates and subsequent operator timing instructions.

**LIVE EXECUTION BLOCKED — EXPIRED OR INVALID AUTHORITY**, applying to any further
invocation because the signed approval has been consumed. The completed attempt
had valid authority and failed at reducer validation. Configuration, separate RSA
signing authorization, saved-signature verification and separate paid-execution
authorization all passed. One controlled launcher invocation made two paid calls
and stopped without retries. Both calls settled; no complete digest, publication
or grounded Q&A was produced. Phase 17H remains partial.

## Repository and generation contract

Starting and final branch: `master`. Starting and final committed HEAD:

```text
2b8a5ac73beb32d7febc53f77d0c3a459c8e3394
```

The current `managed-prompt/5` generation-contract digest remains:

```text
de9492c536c1435464e8d9e406cbd1491ea358bc45f817df72eb2ea2a0f69a71
```

All twelve generation-source inventory files match committed HEAD. No application
code, generation prompt, schema, dependency, configuration interface, financial
catalog or authority policy was changed. No Kubernetes/AKS mutation or unrelated
resource operation occurred.

## Previous checkpoint and interruption reconciliation

Preparation began with `rsa-signing-readonly-checkpoint.json` and
`verification-process-state-correction.json` in the historical private
`phase17h-v5-final-operator-continuation-20261108` package. The checkpoint's file
SHA-256 matches the correction's recorded hash. The correction supersedes the
checkpoint narrative claiming loss of the original memory process: that helper
was running at the historical verification, while the signer had exited at
`AWAITING_FRESH_VERIFIED_OPERATOR_CHECKPOINT` before signing.

The three historical terminal handles are unavailable to this session. Empty
status polls returned `Unknown process id`; no command text was sent to them.
A host process-name inspection showed no Python helper, but that observation
alone was not treated as proof of previous-session process state. The old signed
artifact is absent, its proposed approval remains unconsumed and its live audit
directory remains empty. Historical files were preserved unchanged.

The previous configuration digest
`d53a4a45f3d914ee85d703a6b6a848f047455b62dba725e57713b70f2311854d`
and its unsigned bindings were retained only as historical evidence. Neither was
reused for this changed window, and earlier signing authorization did not transfer.

## Confirmed execution window and fresh credentials

The first operator-confirmed renewal ended at 01:15 UTC. Fresh authentication
passed identity/Graph/registration checks but returned a token expiring 01:05:53
UTC. The preparation helper required complete-window coverage plus a one-minute
margin and stopped before resource-key retrieval or finalization. It released
its token, created no signature and did not automatically repeat authentication.
The stopped attempt was preserved in a separate private package named
`phase17h-v5-window-renewal-20261109-credential-blocked`.

The operator then explicitly confirmed these revised times and requested another
device login:

| Item | UTC, 9 November 2026 |
| --- | --- |
| Execution not before | 00:15 |
| Target launch | 00:35 |
| Approval expiry | 01:00 |
| Operator-attested API-key use deadline | 01:00 |
| Canonical exclusive launcher cutoff | 00:50 |
| Fresh verified operator-token expiry | 01:27:14 |

The cutoff is exclusive: launch must occur before 00:50. The controlled workflow
also requires at least twenty minutes of remaining authority at launch. The
00:35 target supplies twenty-five minutes to the earlier approval/key deadline.
The token covers the entire confirmed window with an additional 27 minutes and
14 seconds. Time-sensitive checks must be repeated at later gates.

Pinned OIDC verification checked the identity-provider RS256 signature, exact
issuer/audience, delegated scope and required operator role. The authenticated
principal matches independent approval trust, registered enabled user identity,
derived owner/tenant scope and publication permission. A separately verified
signed OID was correlated exactly with an enabled Graph account; unverified
claims did not authorize the correlation. Fresh credential metadata was recorded
at 00:02:53 UTC. Private identity fields remain outside Git.

The named resource's exact management keys API returned its resource-specific
credential. The token and API key are held only in the preparation process's
memory; neither was written to files, logged or placed in command arguments.
The API-key deadline is an explicit operator use restriction, not a measured
intrinsic Azure-key expiry. Credential availability requires rechecking later.

## Current Azure, consumer and financial checks

Fresh control-plane checks completed at approximately 00:05:34 UTC. They confirmed
the enabled expected subscription/tenant, resource `epolymind-foundry-dev-susanta`,
deployment `epolymind-gpt-54-mini`, model `gpt-5.4-mini` version `2026-03-17`, Spain
Central, GlobalStandard, successful provisioning and 30 RPM / 30,000 TPM.

The approved direct public route remains enabled, without resource private
endpoints, customer storage attachments or diagnostic exports. The inventoried
AKS cluster remains stopped, container-instance inventory is empty and the other
inventoried container application remains stopped. These observations alone
cannot exclude playgrounds or outside consumers. The operator separately and
explicitly confirmed exclusive deployment/shared-quota use for the revised
00:15–01:00 UTC period before finalization. No shared consumer was started or
stopped by this task.

The approved November catalog `phase17hl-pricing-eur-202611/1` and exact reviewed
financial contract were preserved. The four-call allowance remains
**EUR 0.242439068181288**, within the **EUR 5** ceiling. The approved VAT/network
contingency and exclusions retain their existing budgeting semantics; they are
not an Azure hard cap or independently verified invoice tax treatment. Fresh
route and consumer evidence supports continued use of those assumptions. No
financial migration, historical settlement rewrite or capacity reset occurred.

Read-only SQLite checks verified policy/catalog identity, schema/integrity and
sufficient owner and tenant headroom for all 112,000 reserved tokens and four
requests. Seven historical reservations remain settled with ten existing events;
there are no unsettled reservations, active admission calls or recent admission
calls. Sensitive headroom amounts remain in the private evidence. These reads do
not reserve capacity or prevent subsequent external activity.

## Deterministic plan, embeddings and independent public trust

The rebuilt plan matches the existing deterministic plan digest
`e536899c1d871d4246d7751a258bcab7c9fd3e5a9cce1773e5001d24c416b030`:
one chunk, two dependent reducers, local completion/publication and one grounded
Q&A call. Source evidence resolves exactly. The first chunk estimate is 12,216
input tokens with 3,000 output reserved; the existing one-child reducer bound is
17,032 including overhead/safety. Actual complete Q&A sizing remains mandatory
before call four. Human semantic acceptance remains pending.

The pinned eleven-file local embedding tree matches its approved SHA-256. No
embedding download or load occurred. Existing independent RSA-3072 public trust
matches the separately stored public key and verified operator. Public DER
SHA-256:

```text
35785596dd2f38a3ae5fc8eeb93015a1ba3c8b4f16f06a1d73fbe521f9657816
```

Replay storage is independent of the new audit destination. A fresh proposed
approval UUID differs from the earlier unsigned attempt and is unused. Historical
consumption markers were neither removed nor modified. The existing signing and
verification helper sources and masked local passphrase workflow were inspected;
their historical pinned configurations must not be executed as current authority.
The encrypted private key was not opened during read-only preparation. It was
subsequently unlocked only for the separately authorized single signing attempt
described below. No new signing key was generated.

## New canonical configuration and exact unsigned bindings

The fresh private package is `phase17h-v5-window-renewal-20261109-revised-0100`
under the existing private L1 root. Directories are 0700 and files 0600. Its
`four-call-audit` directory was empty at preparation and signing verification.
It now retains the consumed authorized run's evidence. At the unsigned checkpoint,
the proposed signed-artifact path did not exist; the subsequently authorized
artifact is recorded below. The canonical `load_configuration` result agrees with
`configuration_digest`; new configuration SHA-256:

```text
a382daf01d4ff9a07fc43ac11b597ff7bcb223e3466c526efa6a1d268a232ce3
```

`foundry_approval.bindings(config, principal, digest)` ran with the actual freshly
verified principal. The complete exact identity-bearing object is preserved in
private `approval-bindings.unsigned.json` and in the read-only signing checkpoint.
It is intentionally not copied into this repository report. Exact saved unsigned
file SHA-256:

```text
b19f998905942a400dd0c28173f07fd46457349291e184ae326d13ca523363d8
```

Bindings contain the new configuration digest, exact operator/scope,
resource/endpoint/deployment/model/version/SKU/region, approved budget strings,
four-call/token/context/rate limits and expiry epoch `1794186000`. Limits remain
25,000 input and 3,000 output tokens per call, 100,000 aggregate input, 12,000
aggregate output and 28,000 context. Concurrency is one, minimum call-start
spacing is 61 seconds, automatic paid retries are zero and fallback is prohibited.

The private `rsa-signing-readonly-checkpoint.json`, created at 00:05:34 UTC,
contains the full requested readiness record: new digest and complete unsigned
bindings, verified principal/token expiry, approval/window/deadline times, public
fingerprint, fresh proposed ID and unused replay status, current financial and
governance evidence, empty audit destination and both authorization flags false.
It contains no credential, token, passphrase or private signing key.

A separate process reopened the saved configuration through the private loader,
recomputed its canonical digest, reconstructed every unsigned binding for exact
JSON-type/value comparison and checked timing, public-trust identity, preserved
authorities/replay and empty audit destination. This review passed at
**00:07:31 UTC**. It did not reconstruct an authenticated Principal from metadata,
retrieve credentials or claim to verify a nonexistent signed artifact.

## Authorized RSA signing and independent saved-artifact verification

The operator's new affirmative reply explicitly authorized RSA signing of the
exact digest and freshly verified bindings presented in the signing handoff.
Private `rsa-signing-authorization.json` retains the exact reply and digest/file
hash, with approval-consumption and paid-execution flags false. The fresh proposed
approval UUID was retained; the earlier unsigned attempt's UUID was not reused.

The existing signer was adapted only in private operator tooling to pin this
configuration, unsigned-file hash, authorization and unique attempt. The memory
helper's previously inspected dynamic verification hook supplied its actual
freshly authenticated Principal to a read-only verifier. It did not obtain a
Principal from unsigned metadata and did not sign, consume approvals or infer.
The original preparation hook was preserved before routing subsequent calls to
these read-only checks.

A restrictive private-file loader initially rejected a temporary helper source
whose file mode was not 0600 during source preservation. Its mode was corrected
and preservation completed without repeating authorization, replacing the
approval ID or opening the key. A sanitized reconciliation record preserves this
administrative failure. The signer had not started; this was not a failed or
repeated signing attempt.

Fresh operator, same-account Graph, registry, binding, public-trust, replay,
governance and admission checks passed at 00:15:40 UTC before private-key access.
The established local masked Windows passphrase dialog then unlocked the existing
encrypted RSA-3072 key. Its public component matched both the separate public PEM
and independent pinned trust. The passphrase was neither requested in chat nor
placed in command arguments, logs or audit files. Key material remained in the
signer process and was released after the single signature.

A second check with the actual freshly verified Principal passed at 00:16:29 UTC,
after the dialog completed. The signer required this checkpoint's matching
digest, approval UUID and nonce, current verified principal lifetime, complete
binding match, unused replay status and current timestamp. It rechecked unchanged
configuration/bindings/public trust/authority/replay files and an empty audit
destination before signing. Exclusive attempt/artifact creation prevents an
automatic second signing run.

Exactly one approval was issued at **00:16:34 UTC**, expiring **01:00 UTC**, with
audience `polymind-l1-live`, issuer `polymind-operator-approval/1`, purpose `live`,
matching pinned key ID, integer issue/not-before/expiry claims and the exact
current bindings. The saved 0600 `approval.v5.four-call.jwt` SHA-256 is:

```text
762d3b267335532398115fe54d34622c9cade03eb8b391c095c35f855ef79f0f
```

At **00:16:41 UTC**, the separate memory/verifier process reopened the saved
artifact through `read_private` and invoked canonical `verify_artifact` with the
actual reverified operator Principal and independently pinned public trust. The
RS256 signature, exact header/key ID, issuer/audience/purpose, fresh approval ID,
issuance/not-before/expiry, every binding and artifact hash passed. The verifier
also checked operator scope/registration and exact enabled Graph-account
correlation, financial/admission headroom, unused replay status, unchanged
authorities and the empty new audit destination. The sanitized receipt is
`rsa-independent-verification.json`; the signed approval was not consumed.

## Execution readiness presented before separate live authorization

Fresh scoped Azure control-plane and consumer checks passed again at
**00:17:08 UTC**, after saved-signature verification. They reconfirmed the expected
subscription/resource/deployment/model/version/SKU/quota, approved public financial
route, absence of diagnostic exports and the inventoried stopped consumers.
`azure-readiness-pre-live.json` retains the private evidence. The operator's
explicit revised-window exclusivity attestation remains necessary because these
reads cannot prove absence of all external consumers.

| Requirement | Readiness |
| --- | --- |
| Generation contract | `managed-prompt/5`; committed-source digest unchanged |
| Configuration digest | Exact `a382daf01d4ff9a07fc43ac11b597ff7bcb223e3466c526efa6a1d268a232ce3` |
| RSA signature | Saved RS256 artifact independently verified; artifact hash recorded above |
| Operator identity | Fresh signature/scope/registration/Graph PASS; expires 01:27:14 UTC |
| Azure credential | Exact-resource API key held in memory; operator use deadline 01:00 UTC |
| Deployment and quota | Expected model/version/GlobalStandard; 30 RPM / 30,000 TPM |
| Shared-consumer exclusions | Fresh inventory checks plus explicit exclusive-use attestation through 01:00 UTC |
| Financial allowance and headroom | Approved November catalog and complete allowance fit current headroom |
| Governance/admission | Evaluation policy unchanged; all seven historical reservations settled; no active/recent calls |
| Execution window | 00:15–01:00 UTC; target 00:35; canonical exclusive cutoff 00:50 |
| Controlled-launch safety margin | At least twenty minutes to the earliest authority deadline at actual launch |
| Approval replay / audit | Approval unused; new live audit directory empty |
| Four-call deterministic plan | One chunk, two reducers, publication and one Q&A; runtime G1/G2 and actual Q&A sizing still required |
| Maximum estimated allowance | EUR 0.242439068181288, within EUR 5 ceiling; approved contingency limitations unchanged |
| Retry and fallback policy | Zero automatic paid retries; no fallback or model substitution |

The readiness table describes the preauthorization handoff, when replay was
unused and the audit directory was empty. The launcher subsequently repeated
identity, credential availability, signature, replay, governance/admission,
deployment/consumer and remaining-runway checks before the separately authorized
single invocation. The later canonical cutoff did not waive the twenty-minute
controlled-launch margin.

## Authorization gates and actual execution status

| Gate | Result |
| --- | --- |
| Renewed timing and exclusive-use attestations | Confirmed for revised window |
| Configuration and saved unsigned bindings | PASS |
| RSA signing authorization for new digest | Explicitly granted and privately recorded |
| RSA signing | PASS; exactly one saved RS256 approval |
| Saved signed-artifact independent verification | PASS at 00:16:41 UTC |
| Separate paid-execution authorization | Explicitly granted for the exact signed configuration |
| Controlled launcher invocation | Exactly one; exit code 1 |
| Approval consumption / live reservation | Approval consumed; two new reservations SETTLED |
| Paid Azure inference | TWO CALLS; both provider requests succeeded |
| Publication / grounded Q&A / semantic acceptance | NOT REACHED; not validated |

The operator explicitly answered the separate gate: “I separately authorize the
second paid Phase 17H v5 four-call Azure Foundry evaluation using this exact signed
approval and configuration”. Private `live-execution-authorization.json` records
that actual reply, exact configuration/artifact hashes, existing approval UUID,
one permitted launcher invocation, maximum four calls, zero retries and no fallback.
The signing authorization record was preserved unchanged as its earlier gate;
paid authorization was recorded separately.

## Controlled paid execution and terminal validation failure

The already established controlled wrapper was rebound in private operator
tooling to the reviewed configuration, existing signed artifact and new audit
receipt. The actual application entry point remained the committed
`python -m tests.performance.foundry_l1 --live` command. Its provider, durable
worker, generation prompt, G1/G2 admission/validation, provenance, accounting,
publication and Q&A logic were unchanged. The wrapper was invoked once through
the execution-approval mechanism; it has no retry or fallback path.

Because the current token existed only in the verified memory helper, an
ephemeral private Unix-domain socket handed credentials directly to the approved
external launcher process. Both endpoints verified the local peer's UID/PID and
an attempt nonce. The staging directory and socket had restrictive permissions;
the socket was removed after the transfer. Neither token nor API key was placed
in a regular file, command argument or log. This transport was confined to private
operator tooling and did not change an application interface.

Fresh Azure deployment/network/shared-consumer checks passed again immediately
before launch. The launcher securely reread the named resource's current key and
matched it to the memory-held credential. Fresh OIDC signature/scope, exact signed
OID/Graph account, registration, canonical signature/bindings, existing public
trust, generation/HEAD, pinned embeddings, evaluation headroom, unused replay and
empty audit checks passed at **00:30:36 UTC**. Remaining authority was **1,762
seconds**, exceeding the required twenty-minute margin. Thus the applicable
prelaunch verdict was **LIVE EXECUTION AUTHORIZED — CONTROLLED LAUNCH ELIGIBLE**.

The single CLI invocation started **00:30:37 UTC** and finished **00:32:03 UTC**,
before the 00:35 target and the confirmed expiry. Approval consumption and the
exclusive live marker were preserved. The actual call-start gap was
**61.122190713882446 seconds** and observed concurrency was one.

| Paid call | Input tokens | Output tokens | Provider / application result |
| --- | ---: | ---: | --- |
| Chunk analysis | 2,614 | 1,685 | Provider success; validated checkpoint committed |
| First reducer | 4,222 | 2,235 | Provider success; result rejected by byte-budget validation |
| Remaining reducer and Q&A | 0 | 0 | Not executed after the terminal failure |

The job terminated `FAILED`, category `extraction_limit_exceeded`. The failed
reducer's attempt was `NON_RETRYABLE`; the remaining reducer and final digest step
were cancelled without an attempt. The run guard stopped for `evidence`.
Publication, retrieval and grounded Q&A were not reached. No evidence-ID repair,
response truncation, schema change, model substitution or replacement signature
was performed.

Offline reconstruction reproduced both exact saved request hashes and the
deterministic plan/source fixture. Input estimates were **12,216** and **16,007**,
each with 3,000 output reserved and within the approved context. The first
checkpoint's evidence, inherited summary and propositions revalidated exactly.
The reducer's raw response and canonical result were each **4,783 bytes**, within
their respective **10,000-byte** limits. Its calculated escaped child-material
contribution plus the reserved 1,024-byte wrapper was **7,271 bytes**, exceeding
the existing **7,000-byte** child-material budget by **271 bytes**.

Replaying committed `validate_result` reproduced `synthesis_limit_exceeded` with
diagnostic `response_limit`; the existing code supplies no finer reason enum for
this check. The workflow maps that domain failure to `extraction_limit_exceeded`.
This establishes a child-material sizing rejection rather than a credential,
transport, source-reference or completion-token failure. The rejected reducer
was not committed as a checkpoint. Human semantic acceptance remains pending.

## Settlement, provenance preservation and final disposition

The two calls used **6,836 input + 3,920 output = 10,756 total tokens**, within
all per-call and aggregate limits. Exact November catalog-accounted cost is
**EUR 0.020438080703811248**. Adding the entire approved fixed/additional allowance
conservatively gives **EUR 0.147073028412811248**, below the approved full-run
allowance **EUR 0.242439068181288** and EUR 5 ceiling. These are catalog/budget
figures, not a new invoice-tax or networking-charge assertion.

Both new governance reservations are `SETTLED`; provider usage, run-guard usage,
governance usage/cost and the final financial audit agree. There are **zero
unsettled reservations** and **zero active admission calls**. All seven historical
settlement rows match the earlier preserved financial audit exactly. Existing
policy/catalog values, static authority inputs and old replay-marker contents
are unchanged. The only new replay entry is this approval's consumed marker.
The credential-holding memory helper was closed normally with exit code zero;
the controlled driver exited one after the application's failure.

Private `controlled-execution-review.json` retains exact accounting, spacing,
state and offline validation evidence. `final-execution-disposition.json` records
the consumed authority and stopped outcome; `final-private-artifact-inventory.json`
inventories **87 private files** at preservation. Executed operator-helper source
versions were preserved separately, including the final credential handoff, so
earlier drafts and signing/preparation records remain intact. Directories/files
were checked for owner-only access and absence of symlinks. The source audit was
unchanged during offline reconciliation; receipts were appended outside it.

The offline reviewer required corrections to mirror the worker's reducer-stage
selection and to accept an absent optional diagnostic reason. Its completed
review then passed. These corrections affected only offline reconstruction;
no paid request, accepted artifact or settlement was changed or repeated.

No remaining planned call is authorized as a continuation or retry. The consumed
signature cannot be replayed, despite the original wall-clock window having
remaining time. Preserve the rejection and assess the child-material budget in a
separate task before any new live configuration/signing/execution authorization.

## Validation, review and Git disposition

The approval contract/replay suite passed **69 tests in 10.74 seconds**. Existing
sanitized login-diagnostic tests passed **7 tests in 0.001 seconds**. Live
authentication/control-plane checks, read-only authority checks, committed-source
comparison, embedding/plan/render checks, canonical loading and separate saved
binding review passed. Helper syntax was checked with the Python AST parser.

Self-review checked window/credential coverage, exact verified-OID correlation,
scope/registration, complete binding comparison, unchanged approved finances,
replay isolation, exclusive artifact creation, private permissions and absence
of any signing or inference path in preparation. Pre-commit review of the two
new Markdown deliverables found no credentials, private identities, private keys,
raw provider bodies or unrelated application changes. Historical packages and
authority/replay hashes were checked unchanged.

No full application suite, whole-repository compilation, Docker build or
Kubernetes validation was run: this continuation changes no application code,
dependency, deployment or schema. Relevant offline tests and actual operator
preparation checks provide the validation for this task; Phase 17H is not declared
complete.

`git diff --check` passes. `git status --short --branch` shows the existing
untracked Markdown work plus this task's prompt/report. `git diff --stat` and
`git diff --cached --stat` are empty because no tracked or staged file changed.
No Git staging, commit, push or remote modification occurred.

**Final decision: LIVE EXECUTION BLOCKED — EXPIRED OR INVALID AUTHORITY.**
This classification applies to further execution because the approval is consumed.
The separately authorized invocation itself ran within valid authority and
stopped at the first reducer's child-material byte limit after two settled calls.
No retry is authorized. Full four-call live acceptance, complete publication,
grounded Q&A and human semantic review remain unvalidated; Phase 17H is not complete.
