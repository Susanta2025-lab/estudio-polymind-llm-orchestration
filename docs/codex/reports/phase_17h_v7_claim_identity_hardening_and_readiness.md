# Phase 17H v7 claim-identity hardening and offline readiness

Recorded 9 November 2026 UTC. The [task record](../prompts/phase_17h_v7_claim_identity_hardening_and_readiness.md)
preserves the authorized scope and permanent restriction against Git mutation.
**PASS — V7 CLAIM-IDENTITY HARDENING COMPLETE; OFFLINE READINESS VERIFIED.**
The targeted instruction clarification, independent G1/G2 enforcement, historical
compatibility and complete synthetic workflow pass. This establishes eligibility
for a separate operator-preparation review, not paid execution or Phase 17H
completion. All work remains unstaged and uncommitted.

## Starting state and evidence

The branch is `master`, with reviewed v6 HEAD
`bdd7ab3039fbd9707c10d40a132007598a1921cb`, one commit ahead of the locally
recorded remote tracking branch. Initial tracked and staged diffs were empty.
There were 23 untracked files: 19 previously unrelated Markdown documents and
the four v6 investigation additions. Both investigation documents and both test
modules were inspected. The existing 34 claim-identity cases were retained:
24 unit cases and ten workflow cases. Only the unit module's prompt assertion
needed updating for the intended new wording; its identity rejection predicates
and all ten workflow tests are unchanged.

`AGENTS.md`, the [v6 investigation](phase_17h_v6_git_checkpoint_claim_identity_and_live_readiness.md),
[sizing reconciliation](phase_17h_v5_reducer_sizing_offline_reconciliation.md)
and [historical execution report](phase_17h_v5_execution_window_renewal_and_rsa_authorization.md)
were read. Relevant renderer, profiles, schemas, request construction, validators,
sizing, workflow, historical contract tests and source-inventory mechanism were
inspected. The initial production generation digest matched expected v6 exactly:

```text
f6e568d450ac084c5977e4fef68823fb457cceacd22b361f047310c5d3512f5b
```

The v6 renderer was frozen byte-identically before editing, with its source hash
checked against the unchanged existing v6 fingerprint fixture. Initial tracked
and untracked file hashes were inventoried outside the repository for subsequent
scope and preservation checks. No old phase report or private audit was rewritten.

## Historical failure and remaining causal uncertainty

The latest live v5 attempt ran 9 November 2026, 00:30:37–00:32:03 UTC. Its chunk
analysis passed; the first reducer's provider call succeeded, but its output was
initially rejected by the conservative historical child-material reservation.
The completed v6 replay established that corrected sizing admits its 6,867-byte
complete child contribution, exposing an independent identity failure. All eight
claims had correct current-stage positional claim IDs and used the immediate
child stage UUID for `originating_stage`. The top-level result stage was correct.
Strict production validation rejected the output before a reducer checkpoint
was committed. Root, publication and Q&A were never reached.

The demonstrated defect is in the returned model output, not an application
identity-algorithm or validation inconsistency. The strongest supported causal
explanation is confusion between the stage generating a new claim and the
origins of inherited findings. The v6 shorthand `originating_stage=stage_id` is
consistent with validation but does not explicitly scope the right-hand value to
CONTROL or explain restated child claims. Nested child results contain other
stage UUIDs. This is an avoidable interpretive risk, not proof of the model's
internal reasoning or proof that ambiguity caused that one response.

This task does not repeat private-response reconstruction or invent a repaired
live response. The original remains invalid. Synthetic tests reproduce its
eight-claim origin-copying shape without private prose or identifiers. A clearer
prompt can address the identified ambiguity; it cannot establish future model
compliance or retrospectively validate the original response.

## Narrow implementation and identity rules

Only one production file changes: `documents/digestion/managed.py`.
`StageProfile.template_version` becomes `managed-prompt/7`, and
`ManagedSynthesisInference.render` replaces exactly one identity instruction with:

> Use CONTROL.claim_ids_in_order consecutively for this response. Set the result
> stage_id and every claims[i].originating_stage to the current CONTROL.stage_id,
> including claims that restate child findings. Copy source-stage identities only
> into lineage using CONTROL.required_child_links; never copy a child's
> originating_stage into a new claim.

The requested wording fits without shortening. All four managed profiles use
the same shared instruction. There is no profile-specific identity exception.

| Identity or provenance role | Authoritative value and location |
| --- | --- |
| Current generation | `CONTROL.stage_id`, copied from `request.stage_id`; also required as result `stage_id` |
| Current claim at position `i` | `CONTROL.claim_ids_in_order[i]`, generated by unchanged `stable_id(str(request.stage_id), str(i))` |
| Current claim origin | Exact current `CONTROL.stage_id`, even when restating a child finding |
| Immediate child identity | Child result's UUID and claim ID, supplied in `CONTROL.required_child_links` |
| Inherited findings/qualifications/conflicts | Validated claim `lineage` plus application-owned inherited metadata and immutable checkpoints |
| Original document evidence | Exact `CONTROL.allowed_evidence_ids`; existing evidence-copying and source-resolution rules remain intact |

Chunk requests have kind `analysis` and use the chunk UUID. Intermediate and
structural requests have kind `reduction` and use the current reduction-node
UUID. Root requests also have kind `reduction`, with the current UUID equal to
`plan.root_id`. Profile labels such as `root` are not origin values. A restated
finding is a newly identified current-result claim; the child's own origin and
ID remain unchanged in its stored result and in the new claim's lineage links.

Independent application validation still requires exact current-stage origins,
correct unique positional IDs, valid source references, qualified provenance and
complete child coverage. The generic UUID-shaped result schema continues to
leave these semantic relationships to application validation. There is no ID
rewrite, normalization, substitution, response repair, new schema constraint,
extra inference stage, retry, fallback, model exception or dependency change.
The provider-neutral `GenerationRequest` interface is unchanged.

## Explicit v6-to-v7 contract and compatibility

The production source-inventory mechanism,
`tests.performance.foundry_l1.generation_contract_digest`, now returns:

```text
managed-prompt/7
8426ab5cfef3e4d1925c68a5f8558c5bafc487dd746f0f7ccda799c03be16c3a
```

Only the managed renderer source changes within that complete inventory. Tests
compare the actual v6/v7 rendered prose for every profile and require the exact
single replacement above. They compare generation schemas and all response,
capability and timeout fields directly; they do not refresh historical expected
values to hide additional behavior changes.

| Contract component | v6 | v7 |
| --- | --- | --- |
| Template identity | `managed-prompt/6` | `managed-prompt/7` |
| Identity guidance | Unscoped shorthand equality | Explicit current CONTROL stage, new claim IDs and child lineage roles |
| Stage-result schema | `stage-result/1` | Identical |
| Claim-ID algorithm and strict G2 predicates | Existing application authority | Identical, no repairs |
| Fixed managed input envelope | 9,973 bytes | 10,236 bytes, measured |
| Input allocation / context | 24,800 / 28,000 | Identical |
| Per-child material limit | 7,000 bytes | Identical |
| Digestion raw/canonical response | 10,000 bytes each in L1 | Identical |
| Q&A raw response allowance | 12,000 bytes | Identical |
| Completion reservation | 3,000 tokens per call | Identical |
| Transport response envelope | 26,192 bytes for digestion | Identical |
| Financial, admission, governance, replay | Existing contracts | Identical |

The v5 source snapshot and v5/v6 JSON fingerprints remain unchanged. New
`managed_prompt6.py.txt` freezes the exact committed v6 renderer; its existing
source SHA-256 is `6d744cf9ef412beaa2e25a48c80c2959ed6edf9d5fc8f873eaf1643686839f8f`.
Historical replay uses these hash-pinned classes only in offline fixtures. The
existing v6 fingerprint and wrapper-only-difference tests now run against that
frozen renderer. Existing v4/v5 historical expectations remain intact.

New `managed_prompt7.json` freezes actual synthetic requests, generation objects
and HTTP payloads for chunk, structural and root, together with the complete
generation digest and current renderer source hash
`67dc3f1af618d04db82bc662822c8d0233039bf5b79bb0f9d6427ae8f3e29fd3`.
Intermediate generation is independently rendered and compared in the
four-profile contract and sizing tests. Round-trip tests retain bounded and
unbounded v4/v5/v6 bindings and add v7. Historical data remains readable under
its own unchanged identity and source contracts.

Old v5/v6 template settings are rejected by the current settings model. Current
adapters reject old request bindings. New durable-handler tests reopen actual
synthetic historical checkpoints/plans, attempt to execute with the v7 adapter,
and fail with `profile_mismatch` before any new artifact manifest or provider
call. The historical checkpoint bytes stay unchanged. Launch-configuration tests
reject both prior generation digests. These intentional execution-binding changes
require fresh planning and operator configuration; they do not migrate or repair
stored evidence or silently resume old generation.

## Actual sizing evidence

Measurements use the production renderer, codec and compact ASCII JSON envelope
containing complete system text, nested data and schema. The existing estimator
conservatively treats these bytes as input tokens; provider billed usage is a
separate quantity. The fixed-base increase is exactly **263 bytes**, verified
against frozen v6, rather than merely accepted from the earlier estimate.

| Planning quantity | Measured v7 bytes |
| --- | ---: |
| Maximum fixed envelope across four profiles | 10,236 |
| Empty-path single-child reservation | 17,236 |
| Empty-path two-child reservation | 24,236 |
| Input allocation | 24,800 |
| Two-child remaining input margin | 564 |
| Full maximum context: 24,800 + 100 overhead + 100 safety + 3,000 output | 28,000 |

Eighteen reducer sizing cases render every combination of intermediate,
structural and root profiles, one/two actual child results, and ordinary,
quote/backslash/control-character or accented/BMP/astral-Unicode material.
Children are generated and validated against real synthetic extraction, then
serialized with their actual artifacts and inherited metadata. Paths are tested
through the same rendering and planning functions. The table lists actual
input bytes; each complete context reservation adds 200 overhead/safety and
3,000 output tokens.

| Material/path variant | Children | Intermediate input | Structural input | Root input | Planner bound |
| --- | ---: | ---: | ---: | ---: | ---: |
| Ordinary | 1 | 16,120 | 16,129 | 16,132 | 17,248 |
| Ordinary | 2 | 21,679 | 21,688 | 21,691 | 24,248 |
| Quotes, backslash, newline | 1 | 16,240 | 16,249 | 16,252 | 17,268 |
| Quotes, backslash, newline | 2 | 21,899 | 21,908 | 21,911 | 24,268 |
| Accented/BMP/astral Unicode | 1 | 16,240 | 16,249 | 16,252 | 17,268 |
| Accented/BMP/astral Unicode | 2 | 21,899 | 21,908 | 21,911 | 24,268 |

The largest actual reservation in that matrix is **25,111** including overhead,
safety and output, within 28,000. The largest displayed planner reservation is
24,268 + 200 + 3,000 = **27,468**. The identical escaped/Unicode numbers arise
from the chosen synthetic strings' serialized lengths, not an assumption that
these encodings are interchangeable. Separate original-source chunk cases measure
10,387 ordinary, 10,578 escaped and 10,407 Unicode input bytes, with complete
context reservations 13,587, 13,778 and 13,607. Their original text and evidence
are validated through extraction and production result validation.

Excessive structural paths are rejected in every reducer matrix case rather
than enlarging the allocation. Exact 6,999/7,000/7,001-byte complete-child tests
remain unchanged and run under v7: the first two fit, the last fails before
checkpoint commit at all three L1 digestion stages. Existing Unicode/JSON-layer,
maximum artifact-reference integer and multi-child upper-bound regressions are
retained. The 7,271 historical reservation/6,867 actual witness remains a sizing
regression, and its wrong-origin analogue remains invalid under G2.

## Complete synthetic workflow and identity regressions

The retained 34 identity cases still test all four managed profiles, current
origins, first-only/last-only/all-eight wrong origins, correct IDs and allowed
evidence paired with invalid identity, inherited versus new identities,
qualification/conflict preservation, pre-commit refusal, NON_RETRYABLE failure,
earlier checkpoint and settlement preservation, and absence of publication/Q&A
after invalid digestion. Prompt assertions now explicitly distinguish
`CONTROL.stage_id`, current positional IDs, `CONTROL.required_child_links` and
original source evidence. No negative identity assertion was weakened.

New coverage adds 21 actual sizing cases and 15 v7 contract/compatibility cases.
The latter cover exact changes for four profiles, three frozen complete payloads,
six v5/v6 settings/request denials and two durable historical-plan denials. Six
additional current-version bounded/unbounded round trips and one additional
stale-digest/template case extend existing tests. Tests use production functions
and explicit synthetic transports/stores; no private output is copied.

The complete L1 path remains chunk, first structural reducer, root reducer,
local digest/publication/retrieval and grounded Q&A. For the original sizing
analogue, fresh v7 measurements are:

| Stage | Actual input | Planner bound | Complete context | Canonical result | Complete child |
| --- | ---: | ---: | ---: | ---: | ---: |
| Chunk | 12,420 | 12,453 | 15,620 | 3,317 | 5,337 |
| First reducer | 15,554 | 17,236 | 18,754 | 4,783 | 6,867 |
| Root | 17,087 | 17,236 | 20,287 | 1,311 | 2,172 |
| Grounded Q&A | 9,174 | Actual retrieved-envelope check | 12,374 | 245 raw UTF-8 bytes | Not a reducer child |

The successful 6,999- and 7,000-byte variants have first-reducer canonical sizes
4,915 and 4,916; root inputs are 17,219 and 17,220, within the 17,236 reservation.
The reducer input itself is unchanged when only its generated output grows.
Every successful run has four provider-transport calls, zero billable calls,
complete source coverage, current v7 identities, validated child lineage, four
original evidence IDs, retained qualification entries and unresolved contradiction.
Publication yields eight canonical citations; local retrieval is ready and Q&A
cites an exact original-source excerpt. Contradiction annotations reach Q&A.

All known synthetic call usage is SETTLED and reconciles across run guard,
governance and provider records. Invalid outputs still retain settled successful
provider usage and earlier valid checkpoints. The failing attempt has count one
and NON_RETRYABLE classification; dependants remain unattempted. The 7,000-byte
successful workflow is reopened and resumed without another provider call or
charge. Existing recovery/finalization and forged-source, invalid qualification,
malformed identity, oversized material and invalid-citation fixtures remain
authoritative. Placeholder synthesis and exact-source synthetic answers prove
structural contract behavior, not independent semantic correctness.

## Validation results

The focused network-disabled run passed **235 tests in 37.20 seconds**, with no
warnings and zero network attempts. It includes the existing 34 identity cases,
new sizing and v7 contracts, historical observability and sizing workflows.
Initial new-module Ruff findings were import organization and dictionary-literal
style; they were corrected without changing test behavior or production source.
The subsequent full suite exercises the final versions of those test files.

The complete final suite passed **1,987 tests in 329.37 seconds (5m29s)**:
**1,371 unit and 616 integration**. JUnit independently records zero failures,
errors or skips; there were no xfails. The pre-collection socket/DNS guard
reported **zero network attempts**. This is 43 additional cases beyond the
1,944-case v6 checkpoint-plus-investigation suite, retaining all 34 prior identity
cases. The full run was executed after the test formatting/import corrections.

The only warning was the existing OpenTelemetry `SelectableGroups` deprecation
in the real local Chroma publication test. No assertion was suppressed, no test
was excluded and no validation predicate or limit was relaxed.

| Check | Actual result |
| --- | --- |
| Focused identity, sizing, historical and v7 regression | 235 passed, 37.20s, zero warnings/network attempts |
| Complete offline pytest | 1,987 passed, 329.37s, one existing warning, zero network attempts |
| Ruff critical rules on all 11 changed/new or retained relevant Python files | PASS |
| Default Ruff on both identity and both new v7 modules | PASS |
| Ruff format check on those four plus the adapted sizing workflow | PASS, five files formatted |
| Scoped mypy, 11 Python files | Success: no issues found |
| Whole-repository external-cache compilation | Exit 0 |
| `docker compose config --quiet` | Exit 0 |
| `git diff --check` | Exit 0 |
| Existing historical fixture and dated-report hashes | Unchanged |
| New v6 snapshot versus committed renderer | Byte-identical |
| Complete generation-contract digest versus frozen v7 fixture | Exact match |
| Local Markdown links and sensitive-pattern review | PASS; no findings |

The complete-suite command was:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  PYTHONPATH=.:/tmp/phase17h-g1-g2 python -m pytest \
  -p offline_guard -p no:cacheprovider \
  --basetemp=/tmp/phase17h-v7-offline/full \
  --junitxml=/tmp/phase17h-v7-offline/full.xml \
  -o junit_family=xunit1 -q
```

The independent pre-collection guard denies socket connection, send and DNS
helpers before application imports. Permanent offline workflow fixtures also
deny network access. The temporary fixture-freezing helper installed the same
guard and application-settings isolation before capturing synthetic payloads;
it did not access a live provider or credentials. Temporary logs, JUnit and
per-case sizing receipts are outside the repository. No new test-runner
dependency was added. These overlapping focused/full counts are not additive.

Mypy used the already installed local executable, with `--follow-imports=skip`
and `--ignore-missing-imports`, matching the established scoped checks; no
installation was performed. Compilation used an external bytecode cache rather
than changing repository filesystem ownership. No Docker image rebuild or
Kubernetes/Helm operation was necessary for this prompt-only production change.

## Offline technical-readiness assessment and operator prerequisites

| Dimension | Assessment |
| --- | --- |
| Generation contract | Explicit v7 version and new complete source-inventory digest; exact wording delta verified |
| Claim-identity acceptance risk | Targeted ambiguity removed from instructions; current-stage/lineage rules explicit and independent rejection retained; actual model compliance remains unmeasured |
| Evidence provenance | G2 predicates, source-ID copying/resolution, lineage and qualification authority unchanged |
| Hierarchical sizing | Measured v7 envelopes fit unchanged input/context limits and 7,000-byte child boundary |
| Durable processing | Focused checkpoint/finalization, historical-plan refusal, failure accounting and recovery checks pass |
| Complete synthetic workflow | Four calls and intervening local digest/publication/retrieval pass; no claim of live acceptance |
| Publication and Q&A | Grounded source citations and inherited annotations pass offline; invalid digestion cannot publish |
| Historical compatibility | v5/v6 fingerprints reproducible; historical data readable, incompatible current execution refused |
| Financial/governance contracts | Source, policy interfaces and limits unchanged; synthetic accounting reconciles; historical allowance is context only |
| Operator readiness | Fresh authentication, validated configuration, practical window and independent authorizations still required |
| Real model behavior | Not established by offline tests; historical v5 output remains rejected |
| Semantic quality | Independent human source/claim/citation review remains pending |

Unlike unchanged v6, v7 implements the targeted clarification proposed by the
investigation. This resolves the identified instruction-scoping risk within
engineering scope. It does not remove residual model noncompliance: even explicit
instructions can be ignored or misapplied. Strict G2 must continue rejecting
wrong origins, wrong IDs or invalid sources. No statistical failure probability
or Azure acceptance improvement was measured in this offline task.

The [historical execution report](phase_17h_v5_execution_window_renewal_and_rsa_authorization.md)
confirms approval consumption for the 9 November failed v5 run. Its final
disposition was recorded at 00:39:49.288362 UTC. The v6 review's read-only public
trust/replay inspection at 08:07:06.919929 UTC independently found the matching
consumption marker intact. Those are historical confirmations, not renewed
operator authentication or permission. No approval store or private package was
opened for mutation, and no live configuration or signature was created here.
The consumed approval cannot authorize another attempt, even aside from its
expired window and obsolete generation binding.

Historical financial context remains the approved November catalog
`phase17hl-pricing-eur-202611/1`, EUR 0.242439068181288 full four-call allowance
and EUR 5 ceiling. The allowance includes the conservative 23% token VAT assumption
and EUR 0.10 VAT-inclusive provisional network contingency, with approved local
cost/exclusion semantics. It is not a hard Azure spending cap or new confirmation
of actual invoice taxation. No current financial/headroom or cloud observation
was performed in this task. The last recorded v6 local ledger check was
08:05:15.021219 UTC, with nine settled reservations, no unsettled/active calls
and sufficient local allowance/token headroom at that time only.

The historical target was `epolymind-gpt-54-mini`, model `gpt-5.4-mini` version
`2026-03-17`, GlobalStandard in Spain Central, with observed 30 RPM / 30,000 TPM.
The latest historical prelaunch identity/resource/consumer checks were at
00:30:36 UTC. Token expiry was 01:27:14 UTC; approval, key-use and exclusive-use
attestations ended at 01:00 UTC. These observations and deadlines are stale.
This task makes no claim about present deployment availability, quota, other
consumers, operator identity, credentials or practical execution authority.

After engineering review, the next eligible step is a **separate operator-preparation
review**. It must create a fresh v7-bound configuration and unused audit/replay
identity; verify current deployment/model/capability and pinned local embeddings;
renew financial/headroom, consumer exclusions, identity/permissions and a
practical execution window; and prepare exact unsigned bindings. A later new
RSA authorization, independently verified saved approval and separate paid
execution authorization are required. Preserve four-call limits, 25,000/3,000
per-call input/output, 100,000/12,000 aggregate tokens, one outstanding call,
61-second spacing, zero automatic paid retries and no fallback. None of those
future gates is authorized or performed by this task.

No Entra login, Azure authentication, inference-key retrieval, Azure request,
paid inference, operator RSA signature, live approval consumption, live authority
mutation, historical-settlement modification or replay reset occurred. The full
offline tests include synthetic cryptographic/replay fixtures operating only on
disposable keys and temporary stores; they do not use the operator key or live
approval. Stronger wording and offline passes do not complete Phase 17H or its
live hierarchical digestion, grounded Q&A and semantic-quality gates.

## File manifest and review boundaries

The production change is confined to the two described hunks in `managed.py`.
Supporting tracked changes are:

```text
README.md
docs/evaluation/phase_17h_foundry_validation.md
documents/digestion/managed.py
tests/integration/test_final_offline_azure_compatibility.py
tests/integration/test_foundry_l1_launcher.py
tests/integration/test_live_failure_observability.py
tests/integration/test_output_limit_hardening.py
tests/integration/test_reducer_sizing_offline_workflow.py
tests/unit/documents/test_managed_inference.py
```

The already untracked `tests/unit/documents/test_claim_stage_identity.py` has
the updated explicit-role prompt assertions. The other three v6 investigation
files are preserved byte-identically. Six new v7 files are:

```text
docs/codex/prompts/phase_17h_v7_claim_identity_hardening_and_readiness.md
docs/codex/reports/phase_17h_v7_claim_identity_hardening_and_readiness.md
tests/fixtures/digestion_contracts/managed_prompt6.py.txt
tests/fixtures/digestion_contracts/managed_prompt7.json
tests/integration/test_managed_prompt7_contract.py
tests/unit/documents/test_managed_prompt7_sizing.py
```

README and the current runbook now identify v7, the current-versus-child-stage
rule, unchanged sizing/provenance and separate operator gates. Dated reports
retain their historical descriptions. There are no API, dependency, Docker,
infrastructure, financial policy, database schema or provider-interface changes.

Implementation self-review inspected the complete tracked diff and all new or
adapted files, current/inherited/evidence identity separation, shared profile
behavior, schema equality, sizing arithmetic, old-binding refusal, failure
accounting, recovery and publication gates. The actual generation delta and
preserved source inventory substantiate the absence of semantic repair or
validator relaxation. A separate final pre-commit/security review checks secrets,
credentials, private keys, `.env` files, private identities/output, hard-coded
production paths, generated/debug artifacts, new TODOs, accidental dependencies,
unrelated changes and Markdown links. It found no sensitive content or unrelated
implementation. The source inventory confirms no validator, schema, identity
algorithm, accounting, authorization or provider-interface change. No commit is
part of either review.

## Ending Git state and final engineering verdict

Final `git status`, `git diff --stat`, `git diff --cached --stat` and HEAD were
checked. Branch remains `master`, HEAD remains
`bdd7ab3039fbd9707c10d40a132007598a1921cb`, and there has been no remote refresh
or mutation. There are **nine modified tracked files**, all unstaged, with
**69 insertions and 32 deletions**. There are **29 untracked files**: the initial
23 plus six v7 additions. One of the initial untracked files, the unit identity
module, has the intended prompt-assertion update. The other 22 retain their
initial hashes, including all 19 unrelated Markdown documents and the v6 prompt,
report and workflow tests. All existing historical contract fixtures are also
hash-identical. Untracked files do not appear in ordinary `git diff --stat`.

The staged diff is empty. No `git add`, commit, push, amend, reset, rebase,
history rewrite or branch/tag mutation was performed. The existing v6 checkpoint
was not undone. Implementation, test and documentation changes remain available
for operator review and manual staging/commit.

**PASS — V7 CLAIM-IDENTITY HARDENING COMPLETE; OFFLINE READINESS VERIFIED.**
The prompt now explicitly separates current generation/claim identity from
child lineage and original evidence. New generation identity and digest, actual
sizing, strict G1/G2, durable processing, compatibility and the complete synthetic
workflow are verified. Residual model noncompliance and semantic-quality risk
remain explicit. The next eligible action is a separately authorized operator-
preparation review; no signing or paid-execution authorization is implied.

Git staging: **NO**. Git commit: **NO**. Git push: **NO**.
Paid Azure inference: **NO**. Operator RSA signing: **NO**.
