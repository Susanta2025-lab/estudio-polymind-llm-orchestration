# Phase 17H–L — AST test portability correction

> Publication note — 1 November 2026: this document preserves a historical checkpoint. Private locations and environment identifiers are symbolic where shown; original dates, decisions and outcomes are retained. Historical handoffs are inactive and must not be run. See [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md) for the later accepted single-call result and remaining Phase 17H gates.

For the historical examples below, `PROJECT_ROOT` means the absolute path to a local checkout; `PYTHON` means the absolute path to the project Python 3.10.13 interpreter. Define them with shell assignments such as `PROJECT_ROOT="<absolute checkout path>"` and `PYTHON="<absolute project interpreter path>"`, substituting local paths; these schematic values are not executable examples. `PYTHON_311` and `PYTHON_312`, where used, mean absolute paths to the independently installed Python 3.11.8 and 3.12.9 interpreters. Define them analogously with `PYTHON_311="<absolute Python 3.11.8 path>"` and `PYTHON_312="<absolute Python 3.12.9 path>"`. Their original execution results are retained; temporary drivers and guards are historical evidence, not installed project commands.

Date: 23 October 2026. Branch: `master`.
Starting HEAD: `af4a7a076c918ef13aea05d74bf239c0af909133`.
Scope: test portability only, offline, with the existing dirty working tree preserved.
Prompt: [task instructions](../prompts/phase_17hl_ast_test_portability_fix.md).

## Root cause and reproduction

Two functions in
[`test_live_failure_observability.py`](../../../tests/integration/test_live_failure_observability.py)
hashed the textual output of `ast.dump(..., include_attributes=False)`:

- `test_generation_schema_and_renderer_source_remain_frozen` hashed six complete
  domain class nodes: DigestionProfile, ClaimLink, Qualification, Claim,
  StageResult and StageRequest.
- `test_application_acceptance_predicates_and_order_are_unchanged` hashed the
  complete validate_result function after a NodeTransformer removed every keyword
  from every DigestionError call.

The first occurred at original lines 613–623; the second at original lines
707–727. Searching all repository tests found no other AST serialization hashes.
Other SHA-256 checks hash bytes or canonical JSON, and are not implicated.
`ast.parse` itself is not the defect: serializing its interpreter-owned node
fields into a frozen digest is.

Both `python --version` and `python3 --version` returned **3.10.13**. Recomputing
all seven old AST fingerprints with that interpreter matched the expected values
before any edit. Running the same investigation on already-installed **3.12.9**
changed all seven hashes without any source mutation:

| Contract | Original expected / actual on 3.10.13 | Actual on 3.12.9 |
| --- | --- | --- |
| DigestionProfile | `3a86fedb9dd9b7848b61d879d10820475b44fa6d5b9c16c6fd9358b47e592610` | `a27c0df912308af039b4eec7659d66e06dc35c721b4fb96fed3efa61d4f4d6d7` |
| ClaimLink | `ef20d51ec6997db08f3151a7db9a5bc85c36a474a90a87e73f6c6130e3338ae0` | `382237c22de6b48afba02716f6e06b79ed18273a12fa0820de43b43e827c8f2e` |
| Qualification | `6ebdaadd5f5b1230c3d28934941045999a1337d7e5772fe5d6c711fa2e5b17f1` | `b17062f6fd57e5c9526999bd9ade61b7e19478ad0f5b78fa2e0fa3b0582e66e6` |
| Claim | `0c64cf43cd8333eca8b537a9dab0c1cd155e0021aff16aa2305c8264b85ed993` | `a9c64721bc3ef393aae73e4933bbc717d63b43e9250247e0477b5ebb9b564d27` |
| StageResult | `d3178ca4a04d81cd07fb094e4a771c66d75ddb5a91850ae6f5c428abd42771e7` | `a355918049af00da856c798645c9bb439ee0ef9f0fc212ca7d85c770406f6feb` |
| StageRequest | `914db1a4b5dd10991e0ae18970d67a663eb4e761f7230363ca05b57587ae54a2` | `3472381448aa7321c06b829c72328e4b1d4cca11e8dd3024150d8e0980a9f6ef` |
| validate_result, old normalization | `28f2b6a8563c605c1e384e880ceb87c035e86b31875d1856d2f34fbaca7e4923` | `c6da353d402bb2b88f4564da25e213dce6ae08ce17b6ee31857e79a99675a0ed` |

Python 3.12 adds `type_params` to ClassDef and FunctionDef. For example,
`class Frozen: field: int` dumps with `decorator_list=[]` on 3.10 and with
`decorator_list=[], type_params=[]` on 3.12. A separate investigative transformer
removed only that empty field from the in-memory 3.12 dump: **all seven hashes
then matched the original 3.10 values exactly**. No actual predicates, field types
or instructions differed. The full managed.py byte checksum also matched its
existing approved constant on both interpreters.

This distinguishes an AST schema/serialization change from a source change,
incorrect baseline or true contract regression. It is not a new grammar feature
used by these sources: the additional field is empty. The user-reported 3.13.5
failure is consistent with this class of defect, but its exact dump was not
locally observed because Python 3.13 is unavailable. No interpreter or dependency
was installed to extend verification.

## Replacement and baseline provenance

[`tests/source_contracts.py`](../../../tests/source_contracts.py) compares symbolic
token names and token spellings against fixed, reviewable source excerpts in
[`tests/fixtures/digestion_contracts`](../../../tests/fixtures/digestion_contracts/README.md).
AST nodes only locate source spans and identify metadata expressions; no AST
serialization or interpreter-dependent field inventory enters the comparison.

The two fixture files were captured only after matching the original fingerprints.
A separate provenance check parsed the completed fixtures with Python 3.10.13
and confirmed **7/7 match the original hardcoded AST hashes**. Those retired AST
hashes are recorded above, not recomputed as new test expectations. The fixture
data is independent of the production source at test time. There is no baseline
refresh tool, network dependency, approval-packet dependency or current-source
hash assigned as its own expected result.

The validation reference freezes the entire validate_result function, including
statement order, predicates, limits, lineage, coverage, state updates, categories
and return value. The model reference freezes all six previously covered classes,
including their complete validators and serializers. It additionally freezes the
shared Text alias, closing a gap where an inherited string constraint could change
without editing one of the selected classes.

Token locations, comments, non-logical newlines and indentation width are ignored.
Logical newlines and INDENT/DEDENT boundaries remain significant. String contents,
including spaces, literal spelling, operators, decorators, docstrings, parentheses
and execution order remain protected. Consequently some harmless source rewrites
still require review; the mechanism is conservative about contract changes.
Formatted strings explicitly fail closed because Python 3.12 changed their
tokenization; none of the frozen excerpts contains them.

For validation only, diagnostic/reason keywords on a directly raised DigestionError
may be omitted. Allowed expressions are enum reads already present in the fixed
reference, or conditional selections between those reads with an exactly approved
diagnostic conditional test. Calls or assignments outside those existing approved
tests, new enum members and other executable expressions fail closed. Positional
arguments, unknown keywords, categories and acceptance predicates are retained.
Argument separators associated with removed metadata are reconstructed so inert
metadata additions/removals do not cause false mismatches. Calls outside direct
raise statements receive no metadata exception.

This is stricter than the old transformer, which removed all keywords without
checking their names, expression safety or call context. Conservative diagnostic
edits outside the documented approved expression set require explicit review;
they cannot silently broaden that exception.

## Preserved contracts and mutation evidence

No production file changed during this task. The complete managed.py byte checksum
remains `5b272d4a7591692eeeb328da09bc39b35d402bebd1d8ada3b891f6b1d6e8928c`.
The provider-schema fingerprint remains
`4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2`.
All nine existing request/generation/payload baselines remain unchanged. Together
with the complete managed source check, these retain protection for system
instructions, prompt version, schema, all four stage profiles, controls,
Azure-facing configuration, reasoning effort and token/byte limits. No generation,
provider, governance or approval fingerprint was refreshed.

[`test_source_contracts.py`](../../../tests/unit/test_source_contracts.py) adds
**47 cases**. Controlled source copies are syntax-checked before comparison, and
negative tests require the intended `Frozen source contract changed` assertion,
rather than accepting a syntax/import exception. The validation mutations cover:

- Removing the deterministic claim-identity predicate.
- Weakening source coverage and reduction coverage independently.
- Removing evidence membership, qualification membership and child lineage checks.
- Changing stage binding, response limits, annotation limits and claim rules.
- Changing the public error category.

Nine domain mutations cover all six classes and Text: field types, enum contracts,
required fields, numeric/string bounds, model validation and serialization behavior.
A synthetic generation-instruction mutation is also rejected. The unchanged
complete managed-source checksum separately protects every real instruction; the
cross-version probe confirms that a controlled in-memory change from `Cite ONLY`
to `Cite ANY` fails that existing checksum without writing production files.

Positive cases cover repeated deterministic output, an independently written
literal token oracle, whitespace/comments, CRLF, Unicode byte offsets and approved
diagnostic enum edits/removals. An exhaustive synthetic four-predicate example
executes **all 16 input combinations** before and after inert diagnostic changes:
acceptance and each public rejection category are identical. This executes only
fixed synthetic code, never the frozen production source excerpts. Existing
application behavioral tests remain intact.

Additional cases reject executable diagnostic calls, assignment expressions,
unapproved conditional tests, unknown enum members and unknown error keywords.
Declaration selection checks decorators and rejects missing/duplicate names.

## Interpreter verification

| Interpreter | Actual execution |
| --- | --- |
| Python 3.10.13 | Original fingerprint reproduction; fixture provenance; focused, integration and full pytest runs; dependency-free cross-version probe |
| Python 3.11.8 | Dependency-free probe of actual frozen source comparisons, controlled mutations, diagnostic exception and original managed checksum |
| Python 3.12.9 | Original mismatch reproduction and empty-type_params explanation; same dependency-free probe |
| Python 3.13 / reported 3.13.5 | Not installed; no execution claimed |

The same dependency-free probe produced identical canonical JSON on 3.10.13,
3.11.8 and 3.12.9. Its SHA-256 observation was
`c2abe5cfedc8d688bfdf5a722b2dda963d34a6579535112c0b53487eb1e09eec`
on all three. This digest records a comparison result, not a new production or
test approval fingerprint. Each run checked eight source sections, seven
semantic/prompt mutations, a diagnostic-only edit and zero network attempts.

An attempted 3.12 pytest invocation could not start: its pre-existing installation
first lacked Pygments. A retry using already-installed system Python packages
found an incompatible typing_extensions lacking Sentinel while loading the
unchanged root conftest. No package was installed, no isolation hook bypassed and
no 3.12 pytest success claimed. The standalone probe imports only the stdlib,
test helper and existing network guard; it does not import application settings
or dependencies. Full application semantic acceptance is verified by the normal
3.10 suite, with 3.13 application execution still pending.

## Verification results and commands

All actual regression runs load the inspected existing
`/tmp/polymind_e2e_offline_guard.py` before collection. It denies socket/DNS entry
points, installs a socket audit hook, counts attempts and fails sessions even if
an attempted connection exception is caught. Existing tests/conftest.py and
settings_isolation.py are unchanged. The guard is Python-level isolation, not an
OS firewall assertion about arbitrary external programs.

| Check | Result |
| --- | --- |
| Original observability module after replacement | 112 passed, 4.25 s; zero network attempts |
| Final focused unit + observability selection | **159 passed**, 6.09 s; zero failures/errors/skips/network attempts |
| All integration tests | **495 passed**, 38 existing warnings, 226.97 s; zero failures/errors/skips/network attempts |
| Full configured regression | **1,678 passed**, 42 baseline warnings, **420.75 s**; zero failures/errors/skips/network attempts; exit 0 |
| Ruff check, all three task Python files | PASS, zero findings |
| Ruff format check, all three task Python files | PASS, three already formatted |
| Repository compileall, external bytecode cache | PASS, exit 0 |
| git diff --check | PASS |
| Seven fixture excerpts versus original 3.10 AST digests | PASS, 7/7 match |
| Public pre-existing Python source preservation | PASS, 160/161 unchanged; only the intended test module edited |

JUnit comparison against the previous observability full-final inventory confirms
that **all 1,631 prior case identities remain present and passed**, with exactly
47 additional cases. The focused and integration selections overlap the full
run and are not additional unique tests. No skip, xfail or weakened assertion
was introduced. The 42 full-suite warnings are the existing record_property /
JUnit xunit2 incompatibility warnings, not new production behavior.

One development focused run had **1 failed / 158 passed** because a mutation's
substring occurred twice (the acceptance predicate and diagnostic explanation).
The fixture was corrected to target the complete acceptance condition uniquely;
the intended contract assertion then passed. The cross-version probe also needed
its prompt mutation corrected from absent `Use ONLY` to the actual `Cite ONLY`.
These intermediate fixture-construction errors are not counted as successful
verification and did not alter any production source or baseline.

Reproducible commands, from the repository root:

```sh
PYTHONPATH=/tmp:. python -m pytest -p polymind_e2e_offline_guard \
 tests/unit/test_source_contracts.py \
 tests/integration/test_live_failure_observability.py -q \
 --junitxml=/tmp/polymind-ast-portability/focused-final.xml
PYTHONPATH=/tmp:. python -m pytest -p polymind_e2e_offline_guard \
 tests/integration -q --junitxml=/tmp/polymind-ast-portability/integration.xml
PYTHONPATH=/tmp:. PYTEST_PLUGINS=polymind_e2e_offline_guard \
 PYTEST_ADDOPTS=--junitxml=/tmp/polymind-ast-portability/full.xml \
 python -m pytest -q
ruff check tests/source_contracts.py tests/unit/test_source_contracts.py \
 tests/integration/test_live_failure_observability.py
ruff format --check tests/source_contracts.py tests/unit/test_source_contracts.py \
 tests/integration/test_live_failure_observability.py
PYTHONPYCACHEPREFIX=/tmp/polymind-ast-portability/pycache python -m compileall -q .
git diff --check
git status --short --branch
git diff --stat
git diff --cached --name-only
```

The investigation, probe, logs and JUnit artifacts reside outside the repository
in `/tmp/polymind-ast-portability/`. The dependency-free probe was executed as:

```sh
PYTHONPATH=/tmp:. python /tmp/polymind-ast-portability/cross_version.py
PYTHONPATH=/tmp:. "$PYTHON_311" \
 /tmp/polymind-ast-portability/cross_version.py
PYTHONPATH=/tmp:. "$PYTHON_312" \
 /tmp/polymind-ast-portability/cross_version.py
```

These are recorded execution-environment paths, not hardcoded implementation
dependencies. Docker and Kubernetes validation are inapplicable to this test-only
change and were not run. Pre-existing production lint/format debt was not changed
or represented as globally clean.

## Task-only inventory and review

Modified existing file (already untracked at task start):

- `tests/integration/test_live_failure_observability.py` — replace only the two
  AST-hash checks, retain all existing test names and generation baselines.

Created files:

- `tests/source_contracts.py` — dependency-free test comparison helper.
- `tests/unit/test_source_contracts.py` — 47 targeted regression cases.
- `tests/fixtures/digestion_contracts/models.py.txt` — fixed approved model excerpts.
- `tests/fixtures/digestion_contracts/validation.py.txt` — fixed approved function.
- `tests/fixtures/digestion_contracts/README.md` — provenance and exclusion policy.
- `docs/codex/prompts/phase_17hl_ast_test_portability_fix.md` — clean supplied prompt.
- `docs/codex/reports/phase_17hl_ast_test_portability_fix.md` — this report.

Implementation self-review examined the full task-only diff, source-selection
boundaries, UTF-8 offsets, literal preservation, indentation, diagnostic expression
safety, missing/duplicate declarations and mutation failure reasons. All earlier
test cases and fixed request/schema/source baselines are preserved. The additional
Text baseline improves inherited-constraint protection. No production interface,
resource lifecycle, provider boundary or application behavior changed.

Separate pre-commit review checked the task files for credentials, real dotenv
files, private keys, operator packets, response bodies, debug statements, generated
runtime artifacts, new dependencies, dead code, stale TODOs and unrelated edits.
No such material was introduced. Source fixtures contain public Python contracts,
not real documents. The sole exec use is explicitly limited to fixed synthetic
test code, with a documented Ruff suppression. No other lint suppression was added.

The starting working tree was already dirty, including production files from
earlier work. A public Python source manifest verifies all those production and
isolation files remained byte-for-byte unchanged by this task. The unchanged
tracked Git stat is **20 files changed, 812 insertions, 76 deletions**, all
pre-existing. The task files are untracked and therefore absent from that stat.
Nothing was staged. No commit, push, branch operation or remote mutation occurred.
No private configuration or real document content was read. Azure calls, paid
inference calls, cloud operations and operator approvals/signing are all **zero**.

## Verdict and remaining limitations

**Locally verified; Python 3.13 verification pending.** Full offline regression
and local quality checks pass. The source mechanism has been exercised across
3.10, 3.11 and 3.12, without
claiming a full application run on the latter two. Unsupported new source syntax
or diagnostic expressions require explicit review rather than automatic baseline
refreshes. Source comparison supplements existing behavioral tests; it does not
claim to prove the correctness of arbitrary dependency changes.

**Phase 17H remains PARTIAL.** This correction provides no authorization for a
live inference attempt and makes no Azure compatibility or readiness claim.
