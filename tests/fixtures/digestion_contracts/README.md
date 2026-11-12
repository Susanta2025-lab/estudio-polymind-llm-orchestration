# V11 reducer-quality profile (12 November 2026)

`managed-prompt/11` is an explicit opt-in profile. Set `template_version` to
`managed-prompt/11` on **all four** configured `StageProfile` objects, including
chunk and intermediate. Mixed versions are rejected. The default remains v10;
no existing caller silently receives new reducer instructions. No capability,
byte, token, child, financial or quota limit is enlarged. Configure the existing
`ManagedSettings.profiles` input (or its existing environment-driven equivalent);
there is no new provider-specific switch or executable live-evaluation packet.

```python
profiles = tuple(
    StageProfile(stage=stage, input_tokens=24800, output_tokens=3000,
                 template_version="managed-prompt/11")
    for stage in ("chunk", "intermediate", "structural", "root")
)
```

`managed_prompt11.json` pins the current 25-file `generation-inventory/2`, its
aggregate source hash, and nine synthetic request/generation/HTTP payload hashes.
The complete source inventory already includes the renderer containing all v11
instructions; no inventory-format expansion or untracked production dependency
is needed. The aggregate identifies the implementation supporting both versions;
selected profile, capability, provider/model and the six implementation source
hashes additionally bind each managed configuration and plan. Changing sources
even with the v10 setting does **not** retain the executed historical v10 hash.

The unchanged `managed_prompt10.json` remains the executed v10 baseline. Seven
changed inventory members are frozen verbatim under `v10_sources/`, including
the pre-reporting-correction `foundry_preflight.py`. The other eighteen members
must still match their pinned source hashes. `tests/historical_managed_v10.py`
verifies all 25 and materializes the original renderer/config binding solely in
temporary test stores. Original nine golden hashes remain unchanged. This is
synthetic historical-contract replay, never regeneration of live responses or
loading old implementation code into production. The baseline is also recoverable
from commit `ec22fa3d116696b80a1bb12ad17e2eb37db38cb3`.

Current readers reopen accepted v10 checkpoint/receipt/raw-record associations
under the historical request and config. Current managed execution rejects the
old config. v10/v11 requests and proposals cannot be transplanted, and accepted
checkpoints are not reused across versions. The general resume API can create a
new queued reprocessing job with zero reused stages; this grants no inference
permission. Old approvals fail the current source-inventory binding.

The v11 fixture and fake-output regressions establish deterministic compatibility
and acceptance only. Real-model improvement and independent semantic approval
remain unverified. See the
[implementation report](../../../docs/codex/reports/phase_17h_v11_reducer_semantic_quality_implementation.md)
and [quality assessment](../../../docs/evaluation/phase_17h_v11_reducer_quality_and_closure_assessment.md).

---

# Approved digestion source references

**V10 transition, 10 November 2026:** active generation is `managed-prompt/10`
with `stage-proposal/1` output and deterministic construction of unchanged
`stage-result/1`. The older migration sections below retain their historical
checkpoints. `managed_prompt9.py.txt`, `v9_sources/` and
`managed_prompt9_inventory.json` freeze the exact 15-file v9 source contract
before this transition. `tests/historical_managed.py` executes only the hash-pinned
managed fixture for explicit historical characterizations; other snapshots are
hash/source data. Production does not load them or accept old managed settings.
`managed_prompt10.json` pins the expanded 25-file generation-inventory/2 plus
current representative request/generation/HTTP hashes. Tests never regenerate
these fingerprints. See the
[v10 decision](../../../docs/adr/phase_17h_v10_generation_wire_receipt_decision.md)
and [implementation report](../../../docs/codex/reports/phase_17h_v10_application_owned_evidence_and_lineage_implementation.md).


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

## Exact evidence-copying prompt migration

Active generation now uses `managed-prompt/5`. The v3 and pre-G1 v4 fixtures and
their original hashes above retain their bytes. `managed_prompt4.py.txt` freezes
the complete prior v4/G1 renderer, SHA-256
`36e0fba04c1dd952dc7617759fc36f2106d407578ecba194204a215b1ef88a36`.
Like the pinned v3 fixture, it is executed only inside the isolated synthetic
historical fixture, after checksum verification, with temporary class substitutions
restored afterward. Production does not load historical renderer files or accept
v4 stage configuration. Its pre-G1 projection still matches the original
`managed_prompt4.json` source hash and nine request/generation/payload hashes.
The G1 projection utility's managed-source mutation tests also use this pinned
historical source: v5's new prose intentionally changes one fixed patch context.
The original patch remains exact and unchanged; active v5 is checked separately.
Both v4 budget configurations and stored checkpoints remain readable as historical
data; they do not authorize execution with the changed v5 contract.

`managed_prompt5.json` independently pins the active renderer and nine synthetic
G1 request/generation/payload hashes. These were captured intentionally for this
version transition; tests never refresh them. Behavioral tests compare v4/v5 prose
after removing exactly the two evidence-copying paragraphs, check their sizing
delta, preserve schema equality, and reject cross-version execution. All four
stage profiles must include the new instructions. See the
[R0/R1 engineering report](../../../docs/codex/reports/phase_17h_r0_r1_evidence_provenance_hardening.md)
for the generation-contract transition and remaining live-validation boundary.

### V11 controlled-launch preparation

`managed_prompt11_offline_implementation.json` preserves the byte-identical
preceding offline implementation fixture (generation `072aa2cd2a3be2ddb8e63b0577119e87312f44613c9532b56b6d6d9c5ff78fba`).
The active `managed_prompt11.json` inventory now includes the explicit launcher
selection addition in `foundry_l1.py` and `foundry_preflight.py`; its request,
generation-rendering and transport witnesses are unchanged. The preparation
report records the new generation hash and the exact two-file difference.
The additional frozen `v10_sources/tests/performance/foundry_l1.py.txt` is the
original committed launcher, preserving the historical v10 inventory recipe.

Protected launch configuration opts in with
`"managed_prompt_version": "managed-prompt/11"`. The launcher binds that field
into its canonical configuration hash and applies it to chunk, intermediate,
structural and root profiles. Missing selection retains v10; the field is omitted
from default-v10 serialization to preserve the established shape. Changing or
removing a reviewed v11 selection changes the digest. Runtime overrides are
rejected. This mechanism grants no execution authority. A zero-network rehearsal
can use `foundry_preflight.execute(root, "L1", template_version="managed-prompt/11")`;
its identities, prices, outputs and embeddings are synthetic. It is not an
operational packet preflight or a semantic-quality result.
