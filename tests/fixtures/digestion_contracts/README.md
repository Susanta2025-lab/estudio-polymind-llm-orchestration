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
`managed_prompt4.json` pins the new active renderer source and the three synthetic
stages' request/generation/payload checksums. Separate behavioral tests cover the
intermediate profile as well. Tests compare v3/v4 prose after removing exactly the
subject paragraph, retaining the unrelated unavailable-analysis ambiguity.
These are synthetic regression witnesses, with no live approval authority.

The active v4 change is limited to subject-contract instructions and stale-binding
rejection; the provider schema and application domain acceptance remain authoritative.
See the [v4 implementation](../../../docs/codex/reports/phase_17hl_managed_prompt4_subject_contract_implementation.md)
and [Attempt 6 closure](../../../docs/codex/reports/phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md).
The latter establishes one accepted live analysis, not full live digestion or Q&A.
Fixture execution is offline and synthetic; none of these files is a credential,
live approval, pricing authority or launch configuration.
