# Phase 17H — G1/G2 Offline Engineering and Integration Hardening

Date: 2026-11-02. Scope: offline source corrections and deterministic integration
verification. **Final readiness: READY WITH GAPS for preparing a fresh controlled
four-call L1 evaluation. Phase 17H remains PARTIAL. Production readiness and live
hierarchical acceptance are not established.**

## 1. Executive summary

G1 is addressed for the explicitly bounded L1 composition. The 10,000-byte raw
response and canonical result limits remain; a separate 7,000-byte rendered-child
admission policy now accounts for escaped result JSON, required claim links,
evidence IDs and reference/inherited metadata. Planning measures the complete
fixed managed prompt/schema envelope and uses the child budget to determine
reducer capacity. Chunk planning also includes its rendered source envelope.
Oversized results are rejected before checkpoint acceptance; oversized requests
are rejected before inference. No production code truncates evidence or generated
annotations to obtain a fit.

G2 now has a permanent strict two-chunk test through the actual local worker,
provider HTTP adapter, governance/accounting, durable digest, authorized
publication/activation, retrieval and grounded Q&A. Its successful path makes
exactly **five synthetic model calls**. Qualifications and structured opposition
span the two chunks, survive reopening, and appear in the Q&A's separately
labelled derived context. Checkpoint reuse produces no additional model calls or
settlements. Eight negative cases cover invalid links, absent child coverage,
one omitted child, and oversized chunk/structural/root results.

Final verification ran **32 focused tests, all passing**, and **335 relevant
regressions, all passing**. Their 12 overlapping cases mean **355 distinct test
cases**, not 367 unique cases. A final nine-case G2 run additionally verifies
that its oversized witnesses are below the unchanged canonical limit. The
four-call L1 module contributes **31 passing cases**, including its complete
successful workflow. Every final pytest run recorded zero network attempts.
Compilation and scoped lint checks passed. The final nine-case outcome and audit
checks are recorded below.

The prior [readiness assessment](phase_17h_hierarchical_digestion_readiness_assessment.md)
was read before implementation. Historical live evidence, private operator
packets, credentials, financial authorities and cloud services were not consumed.
All databases, object stores, fake responses and review packets used here are
isolated synthetic test artifacts under `/tmp/phase17h-g1-g2/`.

## 2. Root cause of G1 and permanent reproduction

The previous planner estimated a reducer child as `max_result_characters + 1024`.
That quantity describes neither the complete managed request nor its downstream
serialization. A managed request contains trusted instructions and application
schema, evidence allowlists, all required child links, structural paths, complete
child results, immutable references and inherited counters. Its system and data
strings are themselves JSON-escaped in the conservative generation estimator.
Backslashes, quotes and Unicode escapes therefore consume more downstream space
than the canonical result allowance alone suggests.

The existing runtime guard already failed closed. The defect was the missing
relationship between planning/output admission and the rendered request, not a
truncation or validator bypass. These render-only measurements were reproduced
with the current strict schema, `managed-prompt/4`, 10,000-byte limits, 24,800
input bound, 3,000 completion tokens, 28,000 context and 200 overhead/safety tokens:

| Legacy-policy witness | Valid child result bytes | Actual rendered reducer bytes | Input estimate including 200 overhead/safety |
| --- | ---: | ---: | ---: |
| One chunk, structural | 8,580 | 25,542 | 25,742 |
| One chunk, root | 8,571 | 25,416 | 25,616 |
| Two chunks, structural | 8,502 each | 41,733 | 41,933 |
| Two chunks, root | 8,673 | 25,526 | 25,726 |

Both intermediate and structural profiles are exercised at the structural
rendering seam, and root is exercised separately. `NoInference.execute` raises
if reached. Diagnostic continuation constructs synthetic checkpoint material
only to inspect later envelopes; it is not a successful managed workflow.
A separate eight-claim witness reaches **9,999 canonical bytes**, passes the old
application contract unchanged, and is explicitly rejected by the new embedded
material admission. These tests preserve evidence membership and complete links.

## 3. Implemented correction and rationale

### Bound the embedded material independently

`ManagedSettings.child_input_bytes` is optional and environment-driven through
`DOCUMENT_INFERENCE_CHILD_INPUT_BYTES`. The L1 composition explicitly selects
7,000; legacy compositions remain unchanged when it is unset. A corresponding
`ManagedInputBudget` is stored in the digestion profile and therefore bound into
plan/source-stage identities and checkpoint compatibility.

The result contribution includes its canonical JSON escaped into the managed
outer envelope, one required link for every claim, direct and contradicting
evidence IDs, and conservative list punctuation. Application validation reserves
another 1,024 bytes for the immutable reference and inherited summary. Before a
checkpoint write, the worker also checks the actual inherited summary with a
reference whose byte-size field reserves the profile's maximum artifact size.
The next request rechecks actual child material. Unexpected wrapper growth cannot
silently escape admission or cause information to be removed.

This is an additional shape-sensitive admission contract, not a replacement for
the 10,000-byte limits. For example, admitted escaped stress results in the
two-chunk measurement are **5,238 bytes per leaf, 5,361 structural and 5,291 root**.
The permanent positive tests also exercise plain text, backslashes, quotes and
Unicode, with every result larger than 3,907 bytes. This demonstrates useful
capacity above the historically reported accepted response size without reading
or claiming compatibility with that private historical response itself.

### Derive capacity from the renderer

The adapter measures empty, render-only envelopes for all four managed stage
profiles and stores their maximum fixed size. It derives the input bound from
configured stage limits, request-byte limit and capability context after output,
overhead and safety reservations. Planning adds the actual escaped path and
bounded child contributions, while retaining the separate raw StageRequest and
DAG limits. Analysis estimates include complete rendered source pieces and
evidence allowlists. Managed execution rederives the policy binding before use;
removing the policy from an unchecked profile copy is rejected.

For the tested L1 profile the fixed bound is **9,242 bytes**. Two children reserve
`9242 + 2 * 7000 = 23242`, below 24,800; a singleton reserves 16,242. More children
require the existing bounded reduction hierarchy. If even two children cannot
fit, a multi-child group fails during planning. Unfit singleton groups also fail.
No extra inference calls, repairs, tools or retries are introduced to rescue a
rejected shape.

With escaped admitted witnesses, actual two-chunk structural rendering measures
**22,362 bytes / 22,562 estimated input tokens**, below its 23,242 planning bound.
Root measures **15,803 / 16,003**, below 16,242. Analysis renders measure
10,265 and 10,372 bytes, below planning bounds 10,298 and 10,405. The test compares
rendered child JSON with every original `ChildInput` exactly, detecting loss of
claims, evidence, metadata or annotations.

### Align Q&A with governance

`DocumentAnalysis` previously added the lengths of the system, data and schema
components. Governance instead serializes the complete generation envelope,
including escaping. Q&A now uses that same complete envelope before calling its
executor. Its input and context checks include all retrieved canonical citations
and all selected derived qualifications, conflicting findings, questions and
limitations. It raises `analysis_limit` before reservation/inference on overflow.
There is no top-k reduction or annotation removal to obtain a fit.

A permanent test publishes and retrieves real local synthetic source evidence
with quotes/backslashes and a persisted escaped qualification. It demonstrates
that the old component sum is smaller, rejects at that former limit, rejects one
unit below the full context requirement, and accepts the exact full envelope
boundary while preserving identical data.

### Compatibility and architecture

No StageResult, digest, citation, API, provider-routing or streaming schema was
weakened or replaced. Optional unset policy fields are omitted from serialization
so historical profile/settings fingerprints remain readable. An initial
compatibility failure identified the need to omit the unset setting from the
public settings serialization too; that correction is verified by the existing
historical fingerprint test. Enabling the policy intentionally creates a fresh
configuration/plan binding. Old accepted checkpoints must not be relabelled as
new-policy checkpoints.

All rendering remains provider-neutral application infrastructure. The existing
provider owns strict schema adaptation and transport. Original-source evidence
remains distinct from generated summaries. Security, governed reservation and
settlement, worker fences and strict lineage/evidence validators remain active.

## 4. Permanent regression and integration tests

[G1 sizing tests](../../../tests/unit/documents/test_managed_sizing.py) contain
11 cases: legacy one-/two-chunk overflow; 9,999-byte admission rejection;
admitted large plain/backslash/quote/Unicode results and all reducer renderers;
impossible child budgets; oversized actual wrapper/path rejection; and removed
policy rejection. They use current strict capability/schema configuration and
existing permanent adversarial-result helpers.

The added [Q&A envelope regression](../../../tests/unit/publication/test_analysis.py)
uses persisted annotations and actual publication/retrieval, rather than a
render-only approximation of selected evidence. Existing selected-document,
provenance, conflicting-proposition and refusal tests also pass.

[G2 integration tests](../../../tests/integration/test_phase17h_two_chunk.py)
reuse the [L1 integration fixture](../../../tests/integration/test_phase17hl_offline_e2e.py)
and offline composition. The four-page deterministic PDF has authored access
statements on pages 1 and 3, an 800-character chunk setting, exactly two analysis
chunks, one structural reducer and one root reducer. The HTTP fake emits strict
schema-valid full results; the real OpenAI-compatible adapter parses them. The
five-call financial contract is synthetic and test-local; no live launcher or
private approval limit was enlarged.

The positive test verifies six durable workflow steps, four synthesis
checkpoints, COMPLETE digest and fraction-one eligible coverage; exact child
claim links; both original qualifications and opposing `access` stances; inherited
counters and unresolved conflict; an authored synthetic root narrative retaining
both qualifications; active authorized publication and ready replica; Q&A context
with both conflicting original findings; and an answer copied from a validated
canonical page-one citation. Reopening validates document/extraction/span
bindings. Resume uses supported checkpoints without further inference or ledger
changes.

All five known-usage calls settle once at fake usage **30 input / 40 output**
each. The synthetic catalog yields **EUR 0.000055** in total, with no UNKNOWN
obligations. This is test arithmetic, not a provider price or invoice estimate.
Negative cases stop after one, three or four calls as appropriate, retain all
known synthetic expense, never accept a failed-stage checkpoint, and never
publish a failed digest. The omitted-child case retains one real child link and
removes the other, rather than merely testing an entirely empty reducer.

## 5. Four-call L1 offline revalidation

The unchanged one-chunk source fixture still plans exactly one analysis,
structural reduction and root synthesis, followed by one Q&A call. The successful
existing test verifies strict HTTP/application contracts, complete canonical
source coverage, retained qualification, durable reopening, authorized
publication/retrieval, canonical citations and checkpoint reuse without extra
calls. Four synthetic calls settle once at total catalog arithmetic
**EUR 0.000044**. The per-call run ceilings remain 25,000 input / 3,000 output;
24,800 rendered bytes plus 200 overhead/safety consume the input ceiling.

The complete existing L1 test module passes **31 cases**, including revoked
background authorization before reservation, invalid output/link/evidence,
provider/usage failures, failed Q&A preserving the accepted digest and settled
usage, unauthorized retrieval, runner exit status and isolated offline process
execution. No live client factory, credential setup or approval consumption runs.

## 6. Executed commands and outcomes

Tests use application-settings isolation from `tests/conftest.py`, disabled
plugin autoload, disabled repository bytecode/cache writes, and external basetemp
and JUnit files. Before collection, `/tmp/phase17h-g1-g2/offline_guard.py` replaces
socket connect/connect_ex/sendto and DNS/create_connection entry points with a
counting assertion failure. Its session hook reports network attempts. This is a
disposable isolation plugin, not a production dependency. The existing L1 child
process tests install their own pre-import denial as well.

The common executed prefix was:

```bash
PYTHONPATH=/tmp/phase17h-g1-g2:. PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -p offline_guard -p no:cacheprovider
```

Final focused command (append to that prefix):

```bash
tests/unit/documents/test_managed_sizing.py tests/integration/test_phase17h_two_chunk.py tests/unit/publication/test_analysis.py tests/unit/documents/test_two_layer_output.py::test_historical_capability_and_managed_fingerprints_remain_readable --basetemp=/tmp/phase17h-g1-g2/final-focused-review --junitxml=/tmp/phase17h-g1-g2/final-focused-review.xml -o junit_family=xunit1 -q
```

Result: **32 passed in 19.90s; zero network attempts**. Breakdown: G1 11,
G2 9, publication analysis 11, historical fingerprint 1. An earlier final-focused
run also passed 32 in 20.76s. The final test-only strengthening of oversized G2
witness assertions was then checked with:

```bash
tests/integration/test_phase17h_two_chunk.py --basetemp=/tmp/phase17h-g1-g2/final-two-chunk --junitxml=/tmp/phase17h-g1-g2/final-two-chunk.xml -o junit_family=xunit1 -q
```

Result: **9 passed in 6.72s; zero network attempts**.

Final relevant regression command (same prefix):

```bash
tests/unit/documents/test_digestion.py tests/unit/documents/test_managed_inference.py tests/unit/documents/test_strict_schema_compatibility.py tests/unit/documents/test_two_layer_output.py tests/unit/documents/test_independent_json_limits.py tests/unit/publication tests/unit/test_governance.py tests/unit/test_security_authority.py tests/integration/test_managed_digestion.py tests/integration/test_governed_digestion.py tests/integration/test_phase17hl_offline_e2e.py --basetemp=/tmp/phase17h-g1-g2/final-relevant --junitxml=/tmp/phase17h-g1-g2/final-relevant.xml -o junit_family=xunit1 -q
```

Result: **335 passed in 83.53s; zero network attempts**, one dependency
`opentelemetry` import-metadata deprecation warning. This is a targeted selection,
not the full repository suite. The shared profile/planning/validation change
justified compatibility coverage beyond the new tests.

Development runs are retained here to distinguish initial failures from final
verification. Paths below are basetemp suffixes under the same temporary root;
all used the prefix above. Commands with `-x` stopped on the first failure.

| Selection / basetemp suffix | Actual development outcome |
| --- | --- |
| Existing L1 positive node / `initial`, then `initial2` | 1 passed in 2.29s; 1 passed in 1.92s |
| G2 module `-x` / `twochunk` | 1 failed: legacy raw capacity estimate still governed the new child budget; corrected planner capacity |
| G2 module `-x` / `twochunk2` | 1 failed: fake answer selected an unrelated retrieved excerpt; selected an actually retrieved supporting citation |
| G1 module `-x` / `sizing` | 1 passed, 1 failed: one root witness did not overflow; restored the exact escaped witness and kept near-limit admission as a separate case |
| G1 + G2 + added Q&A test `-x` / `focused1` | 3 passed, 1 failed: positive many-claim witness exceeded the new budget; added explicit admissible larger result shapes |
| Same selection `-x` / `focused2` | 15 passed, 1 failed: canonical text excerpt retained its newline; corrected expected source text |
| G1 + G2 + analysis module `-q` / `focused3` | 27 passed in 18.34s |
| Same expanded selection / `focused4` | 30 passed in 21.64s |
| Relevant regression selection / `relevant` | 334 passed, 1 failed in 100.84s: unset settings serialization/fingerprint mismatch; fixed before final runs |

No remaining test failure is being accepted or masked. Initial stdout was
observed through the execution tools; final JUnit files provide machine-readable
counts. A whole-file whitespace probe also found pre-existing README whitespace;
review was correctly restricted to added lines, without formatting historical text. Disposable measurement script `measure.py` additionally reproduced the
sanitized byte counts in sections 2–3 with no provider execution/network attempts.

Other validation:

- `PYTHONPYCACHEPREFIX=/tmp/phase17h-g1-g2/bytecode python -m compileall -q .`:
  passed; external bytecode avoids repository ownership changes.
- `ruff check --no-cache --select E9,F63,F7,F82` on all changed Python files:
  passed. Default configured Ruff checks on the three new Python files initially
  found nine import/style/unused-binding issues. These were fixed only in the
  new files; the default check then passed. No mass formatting was applied.
- Final whitespace, Markdown-link, source review and compilation results:
  passed: external-cache compilation, scoped/default new-file Ruff checks,
  added-line whitespace checks and all new report links; no unresolved review findings.
- Docker/Compose/Kubernetes, cloud integration, downloads and complete-suite
  execution were unnecessary and were not run.

## 7. Self-review, pre-commit review and changed files

Implementation review traced the fixed envelope and each additive child
contribution through the existing nested JSON representation. Evidence allowlists
are conservatively counted per child even when the renderer deduplicates them;
required links are never removed. The actual renderer remains the final guard.
The review also added complete source-envelope estimates and policy-removal
rejection, and fixed unset settings serialization after the compatibility test
exposed it. Application validation, evidence resolution, publication admission,
authorization, settlement and checkpoint reopening remain separate authorities.

A separate pre-commit review examined the changed files and filesystem diffs
against pre-edit copies. No secrets, real environment files, local operator
paths, debug output, temporary runtime artifacts, dependencies, API changes or
introduced TODOs belong to the change. Generated bytecode, fake source documents,
financial/security stores and test results remain external. The documentation
explains implemented behavior and leaves historical phase/evaluation reports
unchanged. Git status/diff commands were not run because the original task
explicitly prohibited Git operations; no clean-worktree claim is made.
**No staging, commit, push, reset, clean, branch change or other Git operation
occurred.**

Files changed by this task:

- [models.py](../../../documents/digestion/models.py),
  [sizing.py](../../../documents/digestion/sizing.py) (new),
  [planning.py](../../../documents/digestion/planning.py),
  [managed.py](../../../documents/digestion/managed.py),
  [validation.py](../../../documents/digestion/validation.py),
  [workflow.py](../../../documents/digestion/workflow.py).
- [Q&A analysis](../../../documents/publication/analysis.py) and
  [offline composition](../../../tests/performance/foundry_preflight.py).
- [G1 tests](../../../tests/unit/documents/test_managed_sizing.py) (new),
  [G2 tests](../../../tests/integration/test_phase17h_two_chunk.py) (new),
  [reused L1 fixture](../../../tests/integration/test_phase17hl_offline_e2e.py),
  [Q&A tests](../../../tests/unit/publication/test_analysis.py).
- [README](../../../README.md), this report, and the
  [clean task record](../prompts/phase_17h_g1_g2_offline_engineering_and_integration_hardening.md).

## 8. Remaining limitations and final readiness

**READY WITH GAPS** applies to scoped offline engineering and preparation of the
existing four-call L1. G1/G2 offline acceptance is established by the tests above;
it does not establish production readiness or complete Phase 17H.

1. Not every result below 10,000 canonical bytes is admissible in the bounded
   profile. The extra rendered-child contract intentionally rejects some valid
   shapes, including the original escaped counterexamples. Rejection is explicit,
   content-free and non-retryable through the existing worker classification.
   A real response that fails application acceptance may still incur its known
   usage; synthetic tests verify settlement in that case.
2. The policy is opt-in and enabled by the L1 composition. Unset legacy profiles
   preserve their fingerprints and old fail-closed runtime behavior; they do not
   acquire a new universal fit guarantee. Changed profiles/plans need fresh
   bindings, and sufficiently large paths/groups may be rejected at planning.
3. Transitive derived annotations and selected-document Q&A context can grow
   independently of any individual child. Complete digestion/publication does
   not guarantee every later query fits. Q&A explicitly refuses the complete
   envelope before inference; no evidence is silently discarded. Larger-document
   or multi-document feasibility is not established.
4. Byte-based conservative token estimates are not provider tokenization or
   actual billed usage. Stress witnesses do not establish that a real model can
   emit every permitted shape within 3,000 inclusive completion tokens. Strict
   output/context/usage checks continue independently.
5. Five-call integration uses deterministic fake transport, fake vectors and
   authored assertions. It establishes structural retention and plumbing, not
   real-model synthesis quality, semantic dense ranking or general entailment.
   Root prose fidelity and all factual citations still need independent review.
   The separate intermediate renderer is checked offline; this tiny DAG has no
   distinct intermediate model call.
6. Live structural/root synthesis, a live-derived COMPLETE digest, publication
   and grounded Q&A remain unverified. This work did not inspect current cloud
   model availability, quotas, pricing, local production embedding availability,
   private authorization or outstanding operator obligations.

## 9. Recommended next action

Prepare a fresh, reviewable **four-call full L1** packet using the corrected
profile and a newly bound plan: one analysis, structural reduction, root synthesis
and one grounded question, with publication/retrieval between synthesis and Q&A.
Re-render its complete bounds, verify exact call count, pinned local embedding
availability and the existing financial/identity/quota controls through the
separately authorized operator procedure. Obtain fresh explicit authorization
for that concrete configuration before any paid call. Preserve zero automatic
retries and independent semantic/citation review.

The five-call rehearsal does not authorize a five-call live launch or alter the
existing live launcher's four-call contract. Do not reuse a historical single-call
approval or relabel old checkpoints. If a two-chunk live milestone is later
selected, it needs its own reviewed launcher/approval scope. No live inference or
next major phase was started here.
