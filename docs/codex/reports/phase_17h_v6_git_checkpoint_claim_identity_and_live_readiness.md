# Phase 17H v6 Git checkpoint, claim identity and live-readiness review

Recorded 9 November 2026 UTC. The [task record](../prompts/phase_17h_v6_git_checkpoint_claim_identity_and_live_readiness.md)
preserves the sequential scope and authorization boundaries.

**CONDITIONAL — V6 CHECKPOINTED; CLAIM-IDENTITY RISK REQUIRES REVIEW.**
The sizing correction is preserved in one reviewed local commit. Offline
engineering checks pass and strict rejection remains intact. An unconditional
technical live-readiness PASS is not justified: the historical reducer copied
child-stage origins into all eight newly identified claims, and unchanged v6
identity guidance has no targeted mitigation for that behavior. Recommend the
separately reviewed prompt clarification below before another paid evaluation.
No generation correction is implemented by this investigation. This verdict
authorizes neither signing nor inference; Phase 17H remains partial.

## Independent starting-state verification and checkpoint

Starting branch was `master`, with HEAD
`2b8a5ac73beb32d7febc53f77d0c3a459c8e3394`. The actual starting state matched
the reconciliation: 16 modified tracked files, eight new task files and 19
pre-existing unrelated untracked Markdown documents. There were no staged
changes. Tracked `git diff --stat` was 220 insertions and 58 deletions across
16 files; untracked additions were absent from that statistic.

The complete tracked diff, eight additions, relevant production consumers,
tests, configuration and documentation were reviewed before staging. The
generation digest was independently recomputed using the production inventory:

```text
managed-prompt/6
f6e568d450ac084c5977e4fef68823fb457cceacd22b361f047310c5d3512f5b
```

The change is narrow. Early result validation measures the escaped result,
required links and evidence contribution without a guessed wrapper. The worker
then measures the complete unchanged child with actual inherited metadata and
the maximum artifact-size integer before artifact storage/checkpoint commit.
Finalization reconstructs inherited metadata and repeats complete material
validation, including the root. Both production callers of `validate_result`
are in this workflow. The separate single-analysis harness has no hierarchical
child budget or managed checkpoint publication. The exported historical
1,024-byte constant remains for diagnostics/compatibility, without controlling
current output admission. The per-child limit remains 7,000 bytes.

The permanent witness demonstrates 4,783 canonical bytes, 7,271 historical
reserved bytes and 6,867 actual child bytes. The result is not shortened or
repaired. Boundary tests admit 6,999/7,000 and reject 7,001 before checkpoint
commit at chunk, structural and root stages. Evidence identifiers, qualifications,
conflicts, coverage and immutable lineage are preserved. The identity/provenance
predicates are unchanged; no provider-specific branch, dependency, infrastructure
change or retry was introduced.

Historical `managed_prompt5.py.txt` is byte-identical to the starting HEAD's
renderer. Reversing the exact sizing patch restores byte-identical starting
`validation.py`. Existing v3/v4/v5 fingerprints, historical fixtures and approval
records were not modified. Compatibility tests explicitly preserve v4/v5 bounded
and unbounded bindings while rejecting them in the current renderer.

The pre-staging full suite passed 1,910 tests. The subsequent staged whitespace
check caught blank context lines in the newly added `reducer_sizing.patch`;
ordinary unstaged `git diff --check` had not inspected that untracked fixture.
The patch was regenerated with zero context. Its reverse projection still
restores exactly the same source, and its fail-closed mutation tests still pass.
This is the only review correction to the supplied checkpoint content; it
changes neither production source nor the v6 digest. A 308-test compatibility,
observability, sizing and workflow rerun passed after that correction.

Exactly these files were explicitly staged; no broad staging command was used:

```text
M README.md
M docs/evaluation/phase_17h_foundry_validation.md
M documents/digestion/diagnostics.py
M documents/digestion/managed.py
M documents/digestion/sizing.py
M documents/digestion/validation.py
M documents/digestion/workflow.py
M tests/g1_source_compatibility.py
M tests/integration/test_final_offline_azure_compatibility.py
M tests/integration/test_foundry_l1_launcher.py
M tests/integration/test_live_failure_observability.py
M tests/integration/test_output_limit_hardening.py
M tests/integration/test_phase17hl_offline_e2e.py
M tests/performance/foundry_l1.py
M tests/unit/documents/test_managed_inference.py
M tests/unit/test_g1_source_compatibility.py
A docs/codex/prompts/phase_17h_v5_reducer_sizing_offline_reconciliation.md
A docs/codex/reports/phase_17h_v5_reducer_sizing_offline_reconciliation.md
A tests/fixtures/digestion_contracts/managed_prompt5.py.txt
A tests/fixtures/digestion_contracts/managed_prompt6.json
A tests/fixtures/digestion_contracts/reducer_sizing.patch
A tests/integration/test_reducer_sizing_offline_workflow.py
A tests/reducer_sizing_fixtures.py
A tests/unit/documents/test_reducer_sizing_reconciliation.py
```

The staged manifest was compared exactly with the reviewed 24-file inventory.
Each staged blob matched its reviewed working-file bytes, with only the documented
patch representation correction. All other initial content hashes remained
unchanged. `git diff --cached --check` then passed. The sandbox initially denied
writing `.git/index.lock`; staging and commit proceeded through the execution
approval mechanism, within the user's explicit local-commit authorization.

The single local checkpoint is:

```text
bdd7ab3039fbd9707c10d40a132007598a1921cb
fix(digestion): reconcile reducer child sizing and preserve v6 contracts
24 files changed, 1837 insertions(+), 58 deletions(-)
```

Task B began only after this commit. Immediately afterward, the tracked working
tree and index were clean, with only the original 19 unrelated untracked
documents remaining. No push, amend, history rewrite or remote mutation occurred.

## Historical failure: evidence and strongest supported explanation

The [execution report](phase_17h_v5_execution_window_renewal_and_rsa_authorization.md)
records the authorized v5 attempt at 00:30:37–00:32:03 UTC on 9 November. Both
provider calls succeeded. The chunk checkpoint was accepted; the first reducer
was rejected before checkpoint commit. The historical v5 result validator
stopped first at its 7,271-byte child admission quantity. Root reduction,
publication and grounded Q&A were not reached.

A fresh network-disabled reconstruction read only the historical audit, SQLite
manifests and immutable object bytes. Artifact sizes/hashes were verified. The
current production validator revalidated the accepted chunk. Under corrected
sizing the original reducer again reached and failed claim identity:

| Predicate or measurement | Observed result |
| --- | --- |
| Raw/canonical reducer bytes | 4,783 / 4,783 |
| Complete bounded child bytes | 6,867, within 7,000 |
| Top-level result stage versus requested stage | Match |
| Positional claim-ID mismatches | 0 of 8 |
| Duplicate claim IDs | 0 |
| Claim IDs copied from children | 0 |
| Originating-stage mismatches | 8 of 8 |
| Distinct returned originating-stage UUIDs | 1 |
| Origins equal to immediate child stage | 8 of 8 |
| Origins equal to inherited child-claim origins | 8 of 8 |
| Application rejection | `inference_contract_error` / `claim_identity` / `originating_stage_mismatch` |

The full historical audit inventory matched before and after the replay, with
zero network attempts. Only counts and categorical findings are recorded here;
no private model prose or identifiers were copied into fixtures or this report.
The historical response remains invalid. Predicates after the first identity
failure are not claimed to pass.

The demonstrated proximate cause is model-output noncompliance with the current
stage binding: the provider emitted the child's origins with fresh current-stage
claim IDs. The pattern supports **source-origin/current-generation conflation**
as the strongest explanation. It does not prove the model's internal reasoning,
or prove that prompt ambiguity caused the error. There is no observed mismatch
between application ID construction and the identities supplied in CONTROL.
Correct positional IDs alone do not authorize a claim with the wrong origin.

## Exact stage identity and prompt/schema consistency

`originating_stage` is a UUID, not a stage name or version string. For every
generated claim at zero-based position `i`, validation requires both:

```text
claim.originating_stage == request.stage_id
claim.claim_id == stable_id(str(request.stage_id), str(i))
```

`stable_id` is the repository's UUID5 helper over unambiguous canonical JSON
parts. Claim IDs must also be unique. The same helper generates the ordered ID
table supplied to the model. The result's top-level `stage_id` must equal the
request UUID and its `kind` must equal the request's `analysis`/`reduction` kind.

| Managed profile | StageRequest kind | Required origin of every output claim |
| --- | --- | --- |
| `chunk` | `analysis` | Current analysis chunk's `chunk_id` |
| `intermediate` | `reduction` | Current reduction node's `stage_id` |
| `structural` | `reduction` | Current reduction node's `stage_id` |
| `root` | `reduction` | Current root reduction node's `stage_id`, equal to `plan.root_id` |

Restating a child finding creates a claim in the current result, with the current
stage origin and current positional ID. The original child's stage and claim ID
remain unchanged in its checkpoint and are referenced through `ClaimLink`
entries in the new claim's `lineage`. Inherited qualifications and contradictions
are carried through those validated links and application-owned summaries.
They do not make the new claim originate in the child stage. Evidence IDs remain
source references and cannot substitute for either claim or stage identity.

The shared managed renderer puts the exact current UUID in `CONTROL.stage_id`,
the ordered generated IDs in `CONTROL.claim_ids_in_order`, and immediate-child
stage/claim pairs in `CONTROL.required_child_links`. The system prompt says:

> Use the supplied claim_ids_in_order consecutively and originating_stage=stage_id.

It separately requires complete child lineage, marks child material untrusted
and instructs inheritance of qualifications/conflicts. All managed profiles use
this shared identity instruction. Handler selection distinguishes chunks, the
root, structural reducers and intermediate reducers; it does not reinterpret
their identity semantics.

The schema requires UUID-typed claim and stage fields, with explicit default
fields in the managed generation schema. It is a generic shape contract: it has
no per-request UUID constant or cross-field equality assertion. Thus an otherwise
schema-valid UUID belonging to a child can pass provider schema checks and still
fail production application validation. That division is consistent and remains
intentional; provider JSON Schema acceptance never establishes G2 acceptance.

The v6 text states the intended equality and is internally consistent with the
validator. However, its shorthand `stage_id` is not explicitly scoped to
`CONTROL.stage_id`, and it does not explicitly explain that inherited/restated
findings receive new stage origins. Nested child results and required links
contain other `stage_id` fields. This leaves avoidable interpretive risk while
asking the model to preserve lineage. There is no contradictory instruction to
retain a child's origin in newly generated output, so a proven prompt defect
cannot be inferred from the one invalid response.

V6 changes only sizing guidance relative to v5; the identity sentence and schema
are unchanged. It is sufficient to state the mathematical rule, but insufficient
evidence exists to accept the repeat live risk without targeted review. The same
failure class can affect later intermediate, structural or root reducers and
other workflows using this renderer. Chunk generation also shares the validator,
although it has no child-stage origin to copy. No model-specific or Azure-specific
identity exception exists.

## New deterministic regressions and validation

[Unit regressions](../../../tests/unit/documents/test_claim_stage_identity.py)
add **24 cases** using synthetic extraction, the real planner, shared managed
renderer, production codec and `validate_result`. Each of four managed profiles
has valid current-stage/positional-ID assertions; schema-valid wrong origins at
the first, last or all eight positions; wrong-stage-generated claim IDs with a
correct origin; and rejection of profile names as origins. Valid evidence IDs
and correct positional IDs do not mask the wrong origin. Child checkpoint
material stays byte-identical. The intermediate profile is exercised directly
against a valid reduction request; it is not an extra call in the four-call L1.

[Workflow regressions](../../../tests/integration/test_claim_stage_identity_workflow.py)
add **10 cases**. Nine inject first-only, last-only or all-eight wrong origins
at chunk, first reducer and root through the explicit synthetic HTTP transport.
Production validation rejects each before committing the failing checkpoint;
the attempt is NON_RETRYABLE with count one, dependants have zero attempts and
no manifest, and no publication/retrieval replica/Q&A is created. Reopened prior
checkpoint manifests and objects remain identical and valid, including their
qualification/contradiction metadata. Successful provider usage stays SETTLED,
including the invalid output's paid-call analogue; no usage is refunded or
erased. The saved synthetic provider response remains exactly the fault input.

The positive four-call case verifies current identities through persisted
checkpoints, two retained qualification entries, unresolved contradiction, all four
original evidence references, complete lineage, publication with eight citations,
ready retrieval and grounded Q&A with contradiction annotations. Existing sizing
tests additionally cover 7,000-byte recovery without another provider call,
pre-commit and finalization material checks, and the exact historical sizing
shape. Existing G2 tests retain unauthorized source/qualification/lineage and
coverage rejection. No production validation or generation code was changed in
Tasks B/C.

| Check | Actual outcome |
| --- | --- |
| Complete offline suite before checkpoint | **1,910 passed**, 318.15s; zero failures/errors/skips; zero network attempts |
| Post-whitespace-fixture checkpoint regression | **308 passed**, 36.73s |
| Initial identity-only run | **33 passed**, 8.71s, before adding the positive workflow case |
| Final post-investigation regression | **873 passed**, 101.81s; includes all **34 new cases**, zero failures/errors/skips and zero network attempts |
| Ruff critical rules on checkpoint's 17 Python files | PASS |
| Default Ruff and formatting on five standalone checkpoint helper/test files | PASS |
| Scoped mypy on checkpoint's 17 Python files | PASS |
| Ruff critical rules on digestion and both new test modules | PASS |
| Default Ruff, format check and scoped mypy on both new modules | PASS |
| Whole-repository external-cache compilation, before and after investigation | PASS |
| `docker compose config --quiet` | PASS |
| Staged and final `git diff --check` checks | PASS after documented fixture correction |

The full-suite warning was the existing OpenTelemetry `SelectableGroups`
deprecation in the real local Chroma test. The 308-case rerun used default JUnit
format and reported seven `record_property`/xunit2 compatibility warnings; the
final regression explicitly used xunit1 and had no warnings. Mypy was not on the
active environment's executable path; the already installed executable from
another local environment was used with `--follow-imports=skip` and
`--ignore-missing-imports`. No dependency was installed. Counts are overlapping
runs and must not be added together as independent coverage.

The full-suite command was:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  PYTHONPATH=.:/tmp/phase17h-g1-g2 python -m pytest \
  -p offline_guard -p no:cacheprovider \
  --basetemp=/tmp/phase17h-v6-review/checkpoint-tests \
  --junitxml=/tmp/phase17h-v6-review/checkpoint-tests.xml \
  -o junit_family=xunit1 -q
```

The final regression used the same pre-collection socket/DNS guard and selected
all `tests/unit/documents`, both new modules, sizing workflows, final Azure
compatibility, failure observability, full L1 offline E2E, validation diagnostics,
launcher, approval/replay and G1 source-compatibility suites. The guard is external
test tooling, not a new repository dependency. Logs/JUnit and sanitized aggregate
replay receipts remain outside Git in the temporary review directory.

Docker build and Kubernetes/Helm checks were not rerun: no dependency, Docker,
chart, deployment or cluster changes were made. There was no cloud request.
No external LLM, live provider factory, operator signing helper or live launcher
was run. Existing synthetic cryptographic tests use disposable test keys and
temporary replay stores; they do not access the operator private key or consume
the live approval.

## Proposed generation clarification, separate from committed v6

Recommend replacing only the shorthand identity sentence in a future
`managed-prompt/7` with this proposed wording:

> Use CONTROL.claim_ids_in_order consecutively for this response. Set the result
> stage_id and every claims[i].originating_stage to the current CONTROL.stage_id,
> including claims that restate child findings. Copy source-stage identities only
> into lineage using CONTROL.required_child_links; never copy a child's
> originating_stage into a new claim.

This makes the existing validator semantics explicit. It does not authorize
copying arbitrary lineage, changing historical claims or repairing a response.
No retry, extra inference stage, schema relaxation, new ID semantics or provider
bypass is proposed. Neither this text nor any new template identity has been
installed in production code. There is **no implemented v7 digest**.

The proposed prose is 263 ASCII envelope bytes longer than the existing
sentence. Holding all other content fixed, the current 9,973-byte fixed base
would become approximately 10,236, and the empty-path two-child bound would rise
from 23,973 to 24,236, leaving 564 bytes below 24,800. This is indicative arithmetic
only; a future implementation must rerender every profile and structural-path
case and rerun planner/sizing/workflow tests. The current input allocation and
7,000-byte child bound must not be enlarged to accommodate wording casually.

Any adopted change requires a new template version, source inventory digest,
managed configuration/plan bindings and frozen current-generation fixtures.
Preserve v6 fixtures as history, prove byte-exact intended prose changes and
schema invariance, reject stale v6 generation/configuration/approval bindings,
and retain these strict identity-negative tests. Recompute the actual new digest
after implementation; never label changed generation behavior with the v6
fingerprint. Existing stored artifacts remain historical evidence, not reusable
execution authority. The clarification cannot guarantee model compliance or
establish semantic quality offline.

## Fresh engineering and operational readiness

The engineering assessment is fresh for the checkpoint plus uncommitted tests.
There is no fresh Azure authentication, quota, billing or shared-consumer claim.
The operator sources are the preserved [window/execution report](phase_17h_v5_execution_window_renewal_and_rsa_authorization.md),
[November catalog migration](phase_17h_v5_authorized_catalog_migration_and_commercial_reconciliation.md)
and [financial/operator preparation](phase_17h_v5_complete_financial_readiness_and_operator_preparation.md),
with read-only local evidence as described below.

| Engineering requirement | Finding |
| --- | --- |
| Committed sizing and generation | Checkpoint above; exact v6 digest unchanged |
| Managed profiles/schema | Four profiles share consistent identity rules; historical bindings rejected by current renderer |
| Strict G1/G2 | Actual child sizing, allowed IDs, qualifications, coverage and stage-bound identity stay fail-closed |
| Four-call workflow | Chunk, structural reducer, root, publication/retrieval and Q&A pass synthetically |
| Checkpoints/finalization/recovery | Pre-storage and finalization validation, reopened earlier checkpoints and no-charge recovery pass |
| Publication/Q&A | Positive source-grounded path passes; invalid identity prevents publication and Q&A |
| Evidence repair | No fabricated sources, normalization, substitution or automatic identity repair |
| Inference boundary | Provider-neutral managed generation through existing OpenAI-compatible adapter; no runtime leakage |
| Retry/fallback | L1 durable policy allows one attempt; no fallback/model substitution; run guard preserves completed and unknown usage |
| Live acceptance | Unresolved eight-claim historical origin copying; v6 identity instruction unchanged; no v6 live result |

Historical observations retain these actual times, all UTC:

| Evidence | Actual observation time and present limitation |
| --- | --- |
| November catalog activation verification | 7 November 11:42:16; prospective catalog transition, not current cloud billing verification |
| Financial preparation Azure refresh | 7 November 14:33:08–14:33:33; superseded by later reads, still historical |
| Latest historical credential/identity metadata | 9 November 00:02:53; verified token expired 01:27:14 |
| Historical control-plane/quota/consumer check | 9 November 00:05:34, repeated 00:17:08.753318 and immediately prelaunch |
| Saved RSA signature verification | 9 November 00:16:41; authenticates the consumed v5 artifact, not future execution |
| Final prelaunch identity/deployment/consumer gates | 9 November 00:30:36; supported the completed attempt only |
| Historical settled-call reconciliation | 9 November 00:38:06.412660; nine total settlements and zero unsettled/active then |
| Historical final disposition | 9 November 00:39:49.288362; approval consumed, no next attempt authorized |
| Fresh local SQLite/configuration review | 9 November 08:05:15.021219; local authority predicates only, no current cloud/authentication evidence |
| Fresh local public-trust/replay inspection | 9 November 08:07:06.919929; public-key fingerprint and consumed marker only, no operator authentication |

The historical target is deployment `epolymind-gpt-54-mini` at
`epolymind-foundry-dev-susanta`, model `gpt-5.4-mini` version `2026-03-17`, Spain
Central, GlobalStandard. The historical observed allocation was 30 RPM and
30,000 TPM. Current source still explicitly restricts the evaluation target,
28,000 context, strict schema, low reasoning effort and inclusive output-token
accounting. These source restrictions do not establish the present cloud model,
provisioning status, quota or capacity.

The preserved November catalog is `phase17hl-pricing-eur-202611/1`, with EUR
0.673279770188 input and EUR 4.039678621124 inclusive output per million tokens.
The four-call token maximum is EUR 0.115804120472288. With the approved 23% token
VAT allowance, EUR 0.10 VAT-inclusive provisional networking contingency and
upward-rounded extras of EUR 0.126634947709, the full allowance remains
**EUR 0.242439068181288**, within the **EUR 5** ceiling. The VAT/network
assumptions and exclusions remain operator budget semantics, not measured tax
treatment, a network hard cap or a subscription-wide spending guarantee.

At 08:05:15 UTC, raw SQLite connections used `mode=ro` and `query_only=ON`, with
integrity checks, without opening mutating authority/admission constructors or
constructing an authenticated Principal from saved metadata. Local catalog,
governance policy and admission policy matched the preserved approved
configuration. There were nine SETTLED reservations, zero unsettled reservations,
zero active calls and zero calls in the recent admission minute. Read-only
arithmetic confirmed the complete allowance and 112,000-token/four-request
capacity fit both saved owner and tenant limits at that moment. Configuration
and authority file hashes were unchanged across the check. This neither reserves
capacity nor proves external billing, operator permission or exclusive use.

The same local review found that the historical configuration still binds v5
and its execution window is expired. Do not feed it to the current launcher or
treat its saved verification flags as renewed attestations. The intended future
limits remain four calls, 25,000 input and 3,000 output per call, 100,000 aggregate
input and 12,000 aggregate output, one outstanding call, at least 61 seconds
between starts, zero automatic retries and no fallback. The provider admission
policy also protects 2,000 interactive TPM and an interactive slot; the L1 run
itself permits concurrency one.

The independent public trust was loaded read-only through its restrictive local
loader at 08:07:06 UTC. Its RSA-3072 public DER fingerprint matches the preserved
fingerprint. The separate replay directory retains the consumption marker whose
configuration/artifact hashes match the last v5 execution. Trust and replay file
hashes were unchanged across inspection. No JWT/private key was opened for
signing, no new signature was created and no approval was consumed. Public trust
is necessary infrastructure, not current operator authorization.

The last operator's exact signed identity, enabled-account correlation,
registration, scope and publication permissions were checked historically, last
at 00:30:36 UTC; no fresh identity was verified here. The operator-attested key-use
deadline and exclusive deployment/shared-quota window ended at 01:00 UTC. The
canonical launch cutoff was 00:50 UTC, additionally constrained by the operator
procedure's twenty-minute launch margin. All these times have passed. The old
credential-holding helper was closed; key availability or a persistent API key
must not be inferred as present authority.

Historical stopped-consumer inventories and absence of diagnostic exports support
only their observation times. They cannot prove that playgrounds, external clients
or other consumers are currently absent. New practical-window and exclusive-use
attestations, fresh deployment/quota/financial-route observations and fresh
authenticated operator/permission verification belong in a subsequent explicitly
scoped operator-preparation task. No new login, inference-key retrieval, Azure
resource read/mutation, signing or paid call occurred in this review.

## Separate readiness conclusions and remaining prerequisites

| Dimension | Verdict |
| --- | --- |
| Offline engineering readiness | **PASS within offline reference scope**: sizing checkpoint and production validation/regression evidence are sound |
| Claim-identity acceptance risk | **REQUIRES REVIEW**: observed systematic child-origin copying; no proof of recurrence frequency, and no targeted mitigation under unchanged v6 |
| Generation-contract compatibility | **PASS for exact committed v6**; v5 configuration/approval cannot authorize it; proposed clarification requires a separately versioned contract |
| Financial/governance readiness | **Local prerequisites pass at the recorded time**; approved allowance fits, but current cloud/consumer/commercial assumptions need renewal |
| Operator authorization readiness | **BLOCKED**: no current authenticated operator/window and prior signature is consumed and expired |
| Eligibility for another controlled live evaluation | **Not eligible now**: resolve/review identity risk, then prepare a fresh generation-bound configuration and independent authorizations |

The historical eight-of-eight failure is an unacceptable *unresolved* acceptance
risk for declaring unchanged v6 technically ready without conditions. It is not
evidence that every future call will fail. Recommended next work is explicit
current-stage/child-lineage guidance under a new generation identity, with
regressions and byte-budget review, before paying for another attempt. If an
operator elects to retain v6, that residual acceptance risk needs an explicit
reviewed decision; these offline passes do not settle it.

After that engineering decision, a future task must prepare and validate new
configuration and audit destinations, current financial/headroom/consumer
evidence, a fresh practical window and authenticated operator, unused replay
identity and new exact unsigned approval bindings. New RSA authorization,
independent saved-artifact verification and separate paid-execution approval are
required. None is performed or implied here. The old approval cannot be replayed,
and remaining calls from the historical failed job are not a continuation right.

Other residual risks remain unchanged: actual model outputs can exceed byte or
completion-token limits, fabricate evidence, drop coverage/qualifications, violate
identity or produce semantically poor findings despite schema compliance.
Synthetic outputs prove deterministic application behavior, not Azure acceptance
or independent human semantic quality. Publication, live grounded Q&A and full
Phase 17H quality acceptance remain unvalidated on Azure.

## Self-review, security and ending Git disposition

Implementation self-review traced current versus inherited identity, positional
ID generation, schema/application predicate separation, all four profile paths,
pre-commit rejection, settlement preservation and publication gates. No finding
required changing a G2 predicate, an application API or generation behavior.
A separate final review covered new tests and documentation for private tokens,
signing keys, identity values, live prose, `.env` material, debug output,
hard-coded production paths, generated artifacts, stale TODOs, dependencies,
unrelated changes and broken local links. No such material was added. The
checkpoint secret/local-path scan had no findings; private reconstruction helpers
and authority paths remain outside Git. The existing Docker context exclusions
for `.env`, local authorities and runtime material were inspected.

Final branch is `master`, one local commit ahead of the locally recorded remote
tracking branch. There was no remote refresh or push. `git status`,
`git diff --stat`, `git diff --cached --stat` and HEAD were checked. Tracked and
staged diffs are empty. The 19 original unrelated Markdown documents are still
untracked and hash-identical to the initial inventory. Four additional files
from this investigation are untracked and intentionally uncommitted:

```text
docs/codex/prompts/phase_17h_v6_git_checkpoint_claim_identity_and_live_readiness.md
docs/codex/reports/phase_17h_v6_git_checkpoint_claim_identity_and_live_readiness.md
tests/unit/documents/test_claim_stage_identity.py
tests/integration/test_claim_stage_identity_workflow.py
```

Thus ending short status has 23 untracked files, zero modified tracked files
and zero staged files. Ordinary `git diff --stat` is empty because all subsequent
investigation additions remain untracked. Exactly one local commit occurred,
containing only the reviewed v6 checkpoint. No push occurred. No paid inference,
operator signing, login, approval consumption, authority mutation, historical
settlement alteration, replay reset or automatic identity repair occurred.

**Final engineering verdict: CONDITIONAL — V6 CHECKPOINTED; CLAIM-IDENTITY RISK
REQUIRES REVIEW.** The accepted sizing correction is independently preserved;
the generation proposal and investigation remain separately reviewable.
