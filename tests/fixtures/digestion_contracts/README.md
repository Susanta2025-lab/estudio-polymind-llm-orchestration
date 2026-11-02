# Approved digestion source references

These fixed source excerpts replace only the interpreter-dependent AST digests
in `test_live_failure_observability.py`. The model and validation excerpts are
test data, never imported or executed. Do not regenerate them from production during tests or automatically
refresh them when a contract changes. Any intentional baseline edit needs an
explicit contract review.

Before capturing the excerpts, all six original domain-class AST digests and the
original metadata-stripped `validate_result` digest were verified to match under
Python 3.10.13. Removing only Python 3.12's added empty `type_params` field from
the investigative AST dump reproduced those same seven digests. The correction
therefore preserves the previously approved source, without approving new
production semantics. `Text` is additionally frozen because the selected models
inherit its field constraints.

`tests/source_contracts.py` compares token names and exact token spelling. It uses
AST nodes only to locate declarations and diagnostic source spans; it never
serializes an AST. The model references include complete declarations, bases,
decorators, constraints, validators, serializers, defaults and docstrings.

Excluded lexical details are comments, token locations, non-logical line breaks
and indentation width. Logical statement boundaries and INDENT/DEDENT block
boundaries remain significant. String contents, spaces inside strings, literal
spelling, operators, parentheses and execution order remain significant. Formatted
strings are rejected for explicit review because their tokenization changed in
Python 3.12; none of these frozen sections uses them.

Only `diagnostic` and `reason` keywords on a directly raised `DigestionError` may
be excluded from the validation comparison. Their values must be enum reads
already present in this fixed reference, or conditional selections between those
enum reads using exactly an already-approved diagnostic conditional test. New
calls, assignments and other expressions fail closed. Categories, positional
arguments, unknown keywords and all acceptance predicates remain protected.
Adding/removing permitted metadata also ignores its argument separators. This
narrows the former normalizer, which discarded every keyword without inspection.
Existing behavioral tests continue checking actual reason attribution and public
errors; synthetic exhaustive cases check unchanged acceptance under inert edits.

The historical complete `managed.py` byte checksum, provider-schema fingerprint and
nine frozen v3 request/generation/payload checksums remain unchanged. Source token
comparison does not replace any approval, provider or generation fingerprint.

See the [portability correction report](../../../docs/codex/reports/phase_17hl_ast_test_portability_fix.md)
for provenance, version checks, mutation evidence and limitations.

## Subject-contract prompt migration

`managed_prompt3.py.txt` preserves the complete pre-migration `managed.py`, with
SHA-256 `5b272d4a7591692eeeb328da09bc39b35d402bebd1d8ada3b891f6b1d6e8928c`.
Unlike the model/validation excerpts, this fixture is executed **only by the
historical offline test fixture**, after verifying that exact checksum. Temporary
class substitutions reproduce the nine original v3 request/generation/payload
checksums and are restored before active tests run. The transport and all state
are disposable synthetic fixtures. Production does not load this file or offer
version-3 execution. Do not update its bytes or the original checksums to follow
the active default.

`managed_prompt4_subject.txt` is the separately reviewed v4 instruction paragraph.
`managed_prompt4.json` pins the pre-G1 v4 renderer source and the three synthetic
stages' request/generation/payload checksums. Separate behavioral tests cover the
intermediate profile as well. Tests compare v3/v4 prose after removing exactly the
subject paragraph, retaining the unrelated unavailable-analysis ambiguity.
These are synthetic regression witnesses, with no live approval authority.

The v3-to-v4 migration is limited to subject-contract instructions and stale-binding
rejection; the provider schema and application domain acceptance remain authoritative.
See the [v4 implementation](../../../docs/codex/reports/phase_17hl_managed_prompt4_subject_contract_implementation.md)
and [Attempt 6 closure](../../../docs/codex/reports/phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md).
The latter establishes one accepted live analysis, not full live digestion or Q&A.
Fixture execution is offline and synthetic; none of these files is a credential,
live approval, pricing authority or launch configuration.

## G1 optional admission compatibility

The original references above retain their bytes and checksums. G1 in `d940443`
intentionally added an optional rendered-child budget to the profile, renderer,
and application validator. Comparing those complete current declarations directly
to pre-G1 source would prohibit that intentional addition. Historical v3 replay
also cannot accept the G1-only settings input.

`managed_g1.patch` records exactly the three modules' source delta from
`d940443^` to `d940443`. It is a fixed, separately reviewable compatibility
exception, not a regenerated golden or replacement fingerprint. The test-only
`tests/g1_source_compatibility.py` reverses those exact contextual hunks in memory
before the original historical source/hash comparisons. Every hunk is mandatory,
must occur exactly once, and preserves all other source. Changed predicates,
missing additions, broader exception code or edits to historical source still
fail. Tests do not regenerate the patch, execute projected source, or write it
back to production. Mutation tests exercise this fail-closed boundary.

Historical v3 and pre-G1 v4 fixtures explicitly omit `child_input_bytes` before
their original strict settings constructor. Current v4 code with the policy unset
must reproduce all nine original v4 request/generation/payload checksums. Current
L1 fixtures retain `child_input_bytes=7000` and their independent 10,000-byte
raw/canonical limits. Matching historical/current configurations render their own
requests; cross-policy requests fail with `incompatible_checkpoint`. Existing
stored results/checkpoints remain readable under their original contracts.

See the [CI reconciliation report](../../../docs/codex/reports/phase_17h_ci_failure_and_historical_contract_reconciliation.md)
for the verified failure inventory, exact regression commands and limitations.
