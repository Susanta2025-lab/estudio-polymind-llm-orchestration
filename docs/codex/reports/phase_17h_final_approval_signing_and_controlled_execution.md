# Phase 17H — Final approval, signing and controlled execution

Execution date: 7 November 2026 UTC. Repository: `master`, assessed HEAD
`f6555f355fd765b3fbdad068d150144bfea94ccd`. Application code and approved
configuration were not changed. The operator's final execution instruction is
preserved in the [authorization record](../prompts/phase_17h_final_approval_signing_and_controlled_execution.md).

## Outcome

**The authorized four-call live evaluation failed application acceptance after
its first paid inference call. Phase 17H remains PARTIAL; full live digestion,
publication, retrieval and grounded Q&A are not validated.** The launcher stopped
on the existing evidence-validation condition. No second inference call, retry,
replacement approval or additional live experiment was performed.

The provider returned a successful response with known usage, but a qualification
contained a reference outside the four allowed source evidence IDs. The existing
validator rejected the response before an analysis checkpoint could be accepted.
The job recorded `FAILED / invalid_reference`, with non-retryable classification;
the run guard recorded `evidence`. Provider success therefore does not imply a
successful analysis, completed hierarchy or accepted application result.

## Separate authorization and approval stages

| Stage | Result |
| --- | --- |
| PREFLIGHT | PASS; final launch checks at approximately 01:28:39 UTC |
| RSA SIGNING AUTHORIZATION | Explicitly granted for the exact configuration and destination |
| RSA SIGNATURE VERIFICATION | PASS; independent saved-artifact check at 01:21:45 UTC, repeated before launch |
| LIVE EXECUTION AUTHORIZATION | Separately and explicitly granted for the exact configuration, approval ID and artifact digest |
| FOUR-CALL EXECUTION | Stopped after 1 of at most 4 paid calls; launcher exited 1 |
| SETTLEMENT AND EVIDENCE | Usage known; governance SETTLED; shared admission finished; audit preserved |
| FINAL PHASE 17H RESULT | PARTIAL; this four-call live acceptance attempt FAILED |

The configuration SHA-256 is
`50613f94e7d2d6f560e27b5ec23a94de1d1b0a0549c3a0ed74202569c5842c76`.
The generation-contract SHA-256 is
`00bf895290e1da2fb81372ff1ea921d8d7f464ea14f41110f54313d0423ad904`.
The independently signed approval ID is `dc6c755a-0d4c-4f88-93be-81f8a7741c0a`,
and its artifact SHA-256 is
`4149e205957cb33da500965c985901ea432e42def9a07a3608be851df4a899b0`.

The operator's prior private/public/trust correspondence check was accepted as
operator-reported evidence. Signing subsequently used the same encrypted
RSA-3072 key through a masked local Windows dialog launched from WSL. Its derived
public key was checked against the existing public PEM and independent trust.
Only the authorized new approval destination was written, with permissions 0600.
No passphrase or decrypted key was written to a file, command argument, log or
report. The JWS used `RS256`, audience `polymind-l1-live`, the reviewed exact claim
bindings and the existing independent replay directory. Signing and verification
did not consume approval. The authorized launcher subsequently consumed it.

## Final launch readiness

Read-only Azure management queries verified resource
`epolymind-foundry-dev-susanta`, deployment `epolymind-gpt-54-mini`, model
`gpt-5.4-mini`, version `2026-03-17`, Spain Central, `GlobalStandard`, successful
provisioning, and exact rate limits 30 RPM / 30,000 TPM. The Azure API key was
retrieved directly from that named resource's keys API. It and the current verified
operator token were supplied to the child launcher's environment in memory.
The generic shell token was stale and was not used for live authentication; no
generic `.env` Azure key was substituted. Raw Azure CLI responses containing keys
were captured in memory and were not logged or preserved.

The final read-only preflight verified the exact canonical configuration digest,
generation contract, unsigned bindings, Entra signature and claims, operator role,
scope, registered identity and `PUBLICATION_MANAGE` permission. It also verified
the independent live trust, replay isolation, embedding tree integrity, private
input permissions, stored policy/catalog compatibility and shared-admission
policy. Constructors and audit-writing authorization methods were not used by the
read-only preflight.

Both owner and tenant selected the existing `polymind-evaluation/1` overlay with
1,500,000 monthly tokens. Before execution each had 1,495,710 monthly tokens,
500,000 daily tokens, 16 request slots and EUR 4.991182682154170454 remaining.
There were six historical settled reservations, zero unsettled reservations, zero
active calls, no conflicting live launcher, and no existing run ledger or live
marker in the approved audit directory. No policy or authority was replaced.
Shared-consumer exclusions and additional-charge applicability retained their
existing operator attestations; management quota verification does not itself
prove either commercial fact.

The configured execution start was 00:54:11 UTC. Approval and credential-use
deadlines remained 02:39:11 UTC; the cryptographically verified operator token
expires at 02:09:13 UTC. At launch the shortest remaining lifetime was 2,433
seconds, exceeding an additional conservative 1,200-second runway check. No
deadline, configuration digest or credential validity assertion was extended.

The unchanged contract allowed at most four calls, 100,000 input and 12,000 output
tokens, EUR 5 maximum, zero automatic paid retries, one concurrent inference call
and 61 seconds between call starts. The pinned catalog's full-token calculation
was EUR 0.11351636747626. The EUR 5 bound was retained as a ceiling, not a request
or permission to use the whole amount.

## Execution and application rejection

The wrapper invoked the documented CLI `python -m tests.performance.foundry_l1
--live` exactly once with the approved configuration, acknowledgement digest,
signed approval and independent trust. It supplied no alternative executor,
provider, model or configuration. The CLI began at 01:28:39 UTC. Its first and only
provider call began at approximately 01:28:52 UTC and finished at 01:29:02 UTC.
The provider duration recorded in the result was about 10.19 seconds. With only
one call, the inter-call spacing requirement was not exercised; there was no
overlap and no subsequent call before or after the failure.

The extracted source matched the existing four-page fixture. The plan contained
one analysis chunk and two reducers, followed by final digest generation,
publication and one Q&A call. The plan anchor succeeded, the chunk failed on its
first attempt, both reducer steps were cancelled without attempts, and final
digest generation was cancelled. The single committed artifact manifest belongs
to the plan anchor; it is not an accepted analysis checkpoint.

The retained response passed `StageResult` domain-schema decoding. An offline,
in-memory replay of the unchanged `validate_result` against the retained plan and
extraction reproduced `evidence_validation_failed`, diagnostic
`evidence_validation`, reason `invalid_qualification_source`. Specifically,
`claims[7].qualifications[0].evidence_ids[3]` contained
`2cd2bfa9-64d8-5157-998f-b774c9d5664d`, outside the permitted source evidence set.
This is an evidence-reference failure, not a quota, authentication, output-token
limit or financial failure. No generated reference was repaired or substituted.

No complete digest was produced. Publication and retrieval acceptance were not
reached; local vector-store initialization does not establish publication or
retrieval acceptance. Grounded Q&A was not attempted. Live G1/G2 acceptance and
independent human quality review therefore remain unvalidated for this run.

## Actual usage and settlement

| Measure | Observed result |
| --- | --- |
| Launcher invocations | 1 |
| Paid provider attempts | 1 |
| Provider outcome | success; rejected later by application validation |
| Automatic retries / additional calls | 0 / 0 |
| Actual input tokens | 2,506 |
| Actual output tokens | 2,130 |
| Actual total tokens | 4,636 |
| Catalog-accounted cost | EUR 0.010088437170011206 |
| New governance reservations | 1, SETTLED with exact actual usage/cost |
| Shared admission | Finished, `active=0`, outcome `success`, exact usage retained |
| Run guard | One finished successful provider record; terminal stop `evidence` |
| Unsettled governance reservations across the authority | 0 |
| Active shared-admission calls across the authority | 0 |

The cost was independently recomputed using
`phase17hl-pricing-eur-202610/1`: input EUR 0.659978880676 and output
EUR 3.959873284055 per million tokens. It matches the provider-linked result,
governance row and financial audit. This is pinned-catalog accounting, not an
Azure invoice or a new tariff assertion. Application rejection does not undo the
paid call or its settled usage.

The governance reservation was 11,626 estimated input plus 3,000 reserved output,
with estimated cost EUR 0.019552534318904176, then settled to actuals. Separately,
the run guard retained its full per-call 25,000/3,000 allowance record. Neither
record was reset to make another attempt possible.

At reconciliation, owner and tenant each had 1,491,074 monthly tokens, 495,364
daily tokens, 15 request slots and EUR 4.981094244984159248 remaining. These are
observations after settlement, not authorization for another run.

## Evidence preservation and review

The complete private evidence remains in the original approved
`<PRIVATE_PREPARATION_DIRECTORY>/four-call-l1-audit`. It includes the source PDF,
fixture, extraction/structure/plan objects, job ledger, run ledger, provider-call
records, responses, result, financial audit, vector-store files and live marker.
The replay consumption record is retained in the existing independent replay
directory. Its configuration and signed-artifact hashes match this run.

Offline reconciliation read the authorities using SQLite read-only connections
with query-only mode. It cross-checked the sole new governance reservation against
the baseline ticket set, provider usage, financial audit and run ledger; checked
settlement, policy compatibility, cancelled dependent stages and replay evidence;
and confirmed the retained source matched the fixture. Fourteen existing source
audit files were inventoried by SHA-256 and remained unchanged during review.
Three new 0600 private documents preserve the execution receipt, independent
review and original evidence inventory. They contain no credentials or raw
process logs. Original audit evidence and replay records were not deleted,
rewritten or reset.

Implementation self-review found no application changes or provider-specific
architecture leakage: the established provider boundary, workflow, validators,
governance and replay protections were reused. The observed acceptance failure is
preserved without weakening validation. No fix was attempted in this execution
task. Pre-commit review is limited to the two new Markdown records; secrets,
signed JWT contents, private key material and raw generated response bodies are
excluded. The two pre-existing untracked headroom-assessment documents were left
untouched. No commit, push or remote repository modification occurred.

No full pytest suite, Docker build, Kubernetes operation or broad engineering
validation was rerun: there is no application implementation change. Validation
for this task consists of the actual authorized CLI run, independent approval
verification, targeted offline validator replay, database/usage reconciliation,
source evidence checks and documentation whitespace review. Live execution's
failure is not reported as a passing test.

## Remaining limitation and next-phase boundary

The signed approval is consumed, and the run has stopped. It must not be reused,
resigned under the same identifier or paired with reset authorities. No additional
live test or paid retry is authorized. A separately scoped offline investigation
could assess evidence-ID generation reliability, but this report makes no code or
generation-prompt change and grants no authority for another inference attempt. Full live
Phase 17H acceptance remains incomplete.
