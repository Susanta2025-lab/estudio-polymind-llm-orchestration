# Phase 17H — R0/R1 offline evidence-provenance hardening

Date: 7 November 2026. Branch: `master`. Scope: R0 regression coverage and R1
versioned generation instructions, with offline verification and documentation.
The [task record](../prompts/phase_17h_r0_r1_evidence_provenance_hardening.md)
preserves the requested boundaries. R2 dynamic schema enums and R3 diagnostics
are excluded. Phase 17H live validation remains **PARTIAL**.

## 1. Original failure and root-cause evidence

The [controlled execution report](phase_17h_final_approval_signing_and_controlled_execution.md)
records the 7 November evaluation stopping after one of at most four paid calls.
The provider returned a schema-valid `StageResult`, but G2 rejected
`claims[7].qualifications[0].evidence_ids[3]` with domain category
`evidence_validation_failed`, diagnostic `evidence_validation`, and reason
`invalid_qualification_source`. The durable worker category was
`invalid_reference`, classified non-retryable. All 17 primary-reference
occurrences across eight claims were valid. The final qualification contained
three authorized IDs followed by one foreign, segment-blended UUID.

The [independent root-cause report](phase_17h_live_invalid_qualification_source_root_cause.md)
established correct extraction/planning IDs, equality of the reconstructed and
recorded model-facing generation-material hash, and agreement between CONTROL
and the validator allowlist. The foreign ID first appeared in provider content.
Static domain/provider schemas checked structure rather than request-specific
membership. G2 correctly rejected that membership failure before checkpoint
acceptance. These findings motivate exact-copy instructions; they do not prove
that ambiguity caused the model's error or that instructions guarantee compliance.

Original usage remains 2,506 input and 2,130 output tokens, total 4,636, with
EUR 0.010088437170011206 accounted under the approved catalog. Its approval was
consumed. Those are historical recorded facts, not new transactions or an Azure
invoice assertion. This implementation used the public reports and synthetic
fixtures only. It did not open or replay private audit evidence, production
authority databases, run guards, private configurations, or consumed approvals.
No original evidence or authority was changed.

## 2. R0 implementation and existing rejection contracts

`qualification_witness` in the existing offline Azure compatibility module authors
a deterministic synthetic analogue: eight correctly ordered claims, 17 valid
primary-reference occurrences, all four source IDs covered, and one qualification
on claim 7 with four references. Its first three references are distinct and
authorized. A parametrized test covers a valid fourth ID, an unrelated foreign
UUID, a UUID made from the first segment of one allowed ID and the remaining
segments of another, and a duplicate authorized ID in the fourth position.
No private response text or live evidence ID is embedded in these fixtures.

The blended value round-trips through `UUID`, is absent from the authorized set,
passes the unchanged Azure provider schema, and decodes through the domain
`StageResult` codec. Both foreign cases then fail G2 with exactly
`evidence_validation_failed / evidence_validation / invalid_qualification_source`.
The duplicate case fails the same qualification source contract. The distinct,
four-reference positive control passes. Removing only the late invalid entry
from each negative synthetic witness establishes that its remaining identities,
source provenance, qualification and coverage are otherwise acceptable.

The existing L1 offline integration fixture injects the blended witness only at
its explicit HTTP transport boundary. The real provider decoder, managed handler,
G2 validator, durable job ledger, admission, settlement and downstream cancellation
remain in the path. The test verifies one provider attempt, no accepted validation
or analysis manifest, a failed chunk with attempt count 1, two cancelled reducers
and cancelled digest with zero attempts/manifests, no publication or Q&A, and
failure to load a digest. Its synthetic known usage remains 30 input/40 output
tokens; governance settles EUR 0.000011 once and the run record finishes with
total usage 70. These are test catalog values, distinct from the historical live
usage above. The response remains rejected rather than repaired or retried.

Existing coverage was reused for empty and foreign qualification lists across
chunk/structural/root profiles, excessive qualification text and its separate
`text_limit` reason, invalid/duplicate primary evidence, invalid contradictory
evidence, invalid child links, missing child coverage and inherited-only source
IDs. The genuinely missing duplicate qualification and mixed late-reference cases
were added; existing rejection tests were not replicated or weakened.

Stage A ran these new R0 cases before editing production instructions: **5 passed,
153 deselected in 2.30s**, zero network attempts. An initial collection-only run
found an insertion syntax error in the test helper; it was corrected before that
passing Stage A run. G2 production code was unchanged throughout.

## 3. R1 generation clarification and architecture impact

`ManagedSynthesisInference.render` adds two short trusted instruction paragraphs:

> Copy every evidence_ids or contradicting_evidence_ids element, including nested
> qualification evidence_ids, from the current CONTROL.allowed_evidence_ids as a
> complete, unchanged identifier, including every UUID segment. Never invent,
> reconstruct, shorten, combine or modify identifiers; claim IDs and stage IDs are
> not source evidence IDs.

> Inherit qualifications/conflicts through valid child lineage, separately from
> direct source references. Do not copy an inherited qualification evidence ID
> into any new direct-reference field unless it is in the current
> CONTROL.allowed_evidence_ids.

The existing requirements for every source piece, consecutive application claim
IDs, correct originating stage, all child links, qualifications, conflicts,
unknown information, subject semantics and output limits remain intact. No
evidence inventory is repeated. The same instructions apply to chunk,
intermediate, structural and root profiles and to every supported provider mode.
There is no extra call, correction stage, retry, fallback, model condition,
dependency, response repair or schema enum. The only production changes are the
template version and these paragraphs in `managed.py`.

## 4. Versioning, historical compatibility and fingerprints

All four `StageProfile.template_version` values transition from
`managed-prompt/4` to `managed-prompt/5`. Explicit v3/v4 settings are rejected by
the current production class. `managed-stage/1`, `stage-result/1`, `managed/1`,
the constraints version, and `managed-generation/1` and `/2` retain their meanings.
The generation profiles describe existing output/capability modes; they do not
need unrelated version changes for this prompt-only transition.
An operator configuration explicitly pinning v4 must therefore be reviewed and
rebuilt for v5, with a fresh plan; this is the intentional generation compatibility
boundary, rather than an API/schema migration or automatic checkpoint upgrade.

Template versions already participate in serialized settings and the inference
configuration fingerprint. `profile()` binds that configuration and prompt
version before planning. Its fixed envelope measurement increases automatically;
the resulting profile digest, plan/stage identities, request fingerprints and
checkpoint compatibility bindings change intentionally. Neither plans nor stored
checkpoints are rewritten. Rendering an old request under the current adapter
fails `incompatible_checkpoint` before transport. The existing managed handler
also rejects a plan whose inference configuration differs.

The complete previous v4/G1 renderer is retained as a hash-pinned **test-only**
fixture, `managed_prompt4.py.txt`, SHA-256
`36e0fba04c1dd952dc7617759fc36f2106d407578ecba194204a215b1ef88a36`.
It is executed only within the established temporary class-substitution fixture
and isolated synthetic transport, with its checksum verified first and patches
restored afterward. Production never loads this file. Its pre-G1 projection still
reproduces the original v4 renderer hash and all nine existing
request/generation/payload checksums. The original v3 fixture/checksums, v4 JSON,
subject paragraph, G1 patch, model fixtures and validation fixtures retain their
bytes. Tests continue reading actual historical synthetic checkpoints under their
own identities; readability does not confer v5 execution compatibility.

The new `managed_prompt5.json` separately freezes nine active G1
request/generation/payload hashes and the active renderer source hash
`93ab242bcf386cdccae68af0f234fe705da16f8d5865b4d12cd3799b831bccef`.
Tests do not refresh golden files. Exact prompt comparisons remove only the two
new paragraphs and require all remaining prose and the generation schema to equal
the v4/G1 fixture. All four profiles have explicit instruction assertions.

For the synthetic L1/G1 configuration measured here:

| Binding | v4 | v5 |
| --- | --- | --- |
| Inference configuration | `fc462322fdea78b45729119d2a7025a6db91a72ac1c148b07f500221e17de033` | `afa43ce4e0e9dc0ac5d54271396c5c34fec548c856899d2892b0221499624d30` |
| Digestion profile digest | `b5853af440ec55046e12e2b4251c746d298d4c406c2f8ed73af1aeab8dd0deaf` | `807d0028d94698600a3217729ebbc7f57edde5cada96fb40fa02514f7f19f19c` |

These are synthetic harness fingerprints, not a newly approved private launch
configuration. The current generation contract was computed using the unchanged
repository `tests.performance.foundry_l1.generation_contract_digest()` function:

```text
Previous: 00bf895290e1da2fb81372ff1ea921d8d7f464ea14f41110f54313d0423ad904
New:      de9492c536c1435464e8d9e406cbd1491ea358bc45f817df72eb2ea2a0f69a71
```

The previous value was verified before changing `managed.py`. No digest was
overwritten to force compatibility. The launch configuration validator requires
the current digest, and independent approval verification binds the configuration
digest. A permanent offline test supplies the exact previous generation digest
and confirms configuration rejection without HTTP, a run ledger or a live marker.
The existing changed-generation test also rejects before approval consumption.
Thus an old signed configuration cannot authorize v5; the consumed failed-run
approval remains consumed and immutable. No live approval was created, signed,
verified, consumed or reset by this task. Existing suite tests use only their
ephemeral synthetic identity/approval fixtures in temporary directories.

## 5. G1 sizing and admission

The trusted prose grows by exactly **590 ASCII bytes per synthesis request**.
The allowlist inventory is unchanged. Synthetic four-page L1 measurements use
the real renderer and HTTP payload construction with mocked transport:

| Stage | System bytes v4 → v5 | CONTROL bytes, both | Data bytes, both | Canonical rendered input bytes v4 → v5 | HTTP JSON bytes v4 → v5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Chunk | 5,822 → 6,412 | 3,818 | 2,049 | 11,426 → 12,016 | 10,835 → 11,425 |
| Structural | 5,949 → 6,539 | 3,925 | 1,310 | 10,850 → 11,440 | 10,259 → 10,849 |
| Root | 5,797 → 6,387 | 3,764 | 1,248 | 10,628 → 11,218 | 10,037 → 10,627 |

System sizes include CONTROL and its delimiter. Canonical rendered input counts
the complete escaped `system`, `data` and generation `schema` envelope, as admission
does. HTTP values measure the synthetic payload with `json.dumps(...).encode()`;
they are a reproducible offline serialization measurement, not a live wire capture
or a tokenizer count. UUID identities change with the profile, but inventory
cardinality, data sizes and CONTROL byte lengths stay constant in these fixtures.

The G1 fixed envelope base increases **9,242 → 9,832 bytes**. Its rendered input
ceiling stays **24,800 bytes**, with 200 overhead/safety units, giving the existing
25,000 input reservation. The largest measured v5 L1 request estimates 12,216
input units and reserves 3,000 output, below the 28,000 context ceiling. This
repository conservatively treats canonical input bytes as estimated tokens;
these estimates are not paid usage. No ceiling was increased: four-call
100,000 input/12,000 output, per-call 25,000/3,000, 7,000-byte child contribution,
10,000-byte raw/canonical result and 26,192-byte response HTTP envelope remain.

All 11 existing managed sizing tests pass, including escaped JSON, larger bounded
results, every reducer profile, impossible fan-in, actual child wrappers/paths,
removed-policy rejection and planning/render consistency. Additional v4/v5
assertions check the exact envelope/base increase with unchanged ceilings. Existing
raw/canonical and HTTP boundary tests still reject overflow. Extra instructions
consume 590 bytes of material headroom; boundary plans may reject or repartition
under the new profile. No prompt truncation, provenance deletion or admission
weakening was used to accommodate them.

## 6. G2 evidence, inheritance and provider compatibility

`validation.py`, domain models, planning code, schemas, provider adapters and
workflow acceptance predicates are unchanged. The frozen domain and validation
source tests remain in force. `allowed_evidence_ids` remains the union of current
source pieces and direct primary/contradictory IDs on immediate child claims.
An ID appearing only in a child qualification or deeper original provenance is
not automatically a directly permitted ID at the next stage.

All child links remain mandatory. Validated child lineage, immutable checkpoint
graphs and application-owned inherited summaries preserve qualifications and
conflicts without manufacturing direct citations. The existing inherited-only
qualification test proves that copying an original qualification into a new root
qualification can fail while preserving it through valid lineage succeeds.
Two-chunk tests preserve conflicting claims, both qualifications, unresolved
conflicts, publication annotations and grounded Q&A citations. Those behaviors
were not replaced with mocks at the validation or publication boundary.

Azure strict schema conversion remains unchanged, with provider-schema fingerprint
`4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2`.
Tests verify strict full-field responses, nullable fields, bounded HTTP,
`max_completion_tokens=3000`, generic OpenAI-compatible and JSON-object contracts,
known/unknown usage, settlement and single-attempt rejection. No request-specific
evidence enum was introduced. Provider schema conformance continues to be separate
from application provenance acceptance.

## 7. Offline verification and review

Tests install a disposable socket/DNS denial plugin before collection, retain the
repository's application-settings isolation and use temporary synthetic stores,
authorities, transport, accounting and identities. No service or model is loaded
for live inference. Test logs, JUnit, measurement output and bytecode caches are
under `/tmp/phase17h-r0-r1`, outside the repository and retained live evidence.

Final focused command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=/tmp/phase17h-r0-r1:. python -m pytest -p offline_guard -p no:cacheprovider tests/integration/test_live_failure_observability.py tests/integration/test_final_offline_azure_compatibility.py tests/integration/test_foundry_l1_launcher.py tests/integration/test_output_limit_hardening.py tests/unit/documents/test_managed_inference.py tests/unit/documents/test_managed_sizing.py tests/integration/test_phase17hl_offline_e2e.py tests/integration/test_phase17h_two_chunk.py tests/integration/test_managed_digestion.py tests/unit/documents/test_digestion.py tests/unit/documents/test_strict_schema_compatibility.py tests/unit/documents/test_two_layer_output.py tests/unit/documents/test_independent_json_limits.py tests/unit/publication/test_analysis.py --basetemp=/tmp/phase17h-r0-r1/focused --junitxml=/tmp/phase17h-r0-r1/focused.xml -q
```

Result: **590 passed in 84.91s**, zero network attempts. The 45 warnings concern
the existing `record_property`/JUnit xunit2 reporting combination.

| Focused module | Passed |
| --- | ---: |
| Final offline Azure compatibility | 126 |
| Live failure observability and generation contracts | 137 |
| L1 launcher compatibility | 27 |
| Output-limit hardening | 6 |
| Managed inference | 53 |
| Managed sizing | 11 |
| L1 offline end-to-end | 32 |
| Two-chunk integration | 9 |
| Managed digestion integration | 11 |
| Digestion unit contracts | 47 |
| Strict schema compatibility | 13 |
| Two-layer output | 81 |
| Independent JSON limits | 26 |
| Publication analysis | 11 |

An intermediate development run reported 350 passed and nine failures: three
v5 goldens had not yet been captured, and six historical unbounded-profile cases
retained the temporary settings wrapper rather than the original constructor.
The separate v5 fixture was captured intentionally and the fixture now retains
the correct original class. The final focused run above passes those cases;
no test was skipped, marked xfail, excluded to hide a failure or made permissive.

The first complete run found **1 failed, 1,871 passed, one dependency warning in
261.34s**, with zero network attempts. The failure was the historical G1 patch
utility's unrelated-change mutation test for `managed.py`: the intentionally
added v5 paragraph interrupts one of the fixed v4/G1 patch's exact context blocks.
The patch and projection helper correctly failed closed and were not broadened
or refreshed. `test_g1_source_compatibility.py` now uses the checksum-verified
v4/G1 source as the input to both historical managed-source mutation tests, while
unchanged models/validation still use current production source. Active v5 source
remains separately frozen by its complete hash, exact prompt-delta comparisons
and G1 behavioral/envelope tests. This keeps historical projection testing
meaningful without projecting away the intentional v5 generation change.
The affected module plus the complete observability/generation-contract module
then passed **144 tests in 8.52s**, with zero network attempts. The full suite is
rerun after this correction; no failing case was removed or skipped.

Final complete-suite command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=/tmp/phase17h-r0-r1:. python -m pytest -p offline_guard -p no:cacheprovider --basetemp=/tmp/phase17h-r0-r1/full-final --junitxml=/tmp/phase17h-r0-r1/full-final.xml -o junit_family=xunit1 -q
```

Result: **1,872 passed, zero failures/errors/skips/xfails in 255.84s**, zero
network attempts. The one warning is the existing OpenTelemetry
`SelectableGroups` deprecation in the local Chroma publication integration test.
No test selection exclusions or new markers were used. Final JUnit records the
same 1,872 successful cases. Both full-suite commands were ordinary offline pytest
runs; neither accessed a live Azure provider or real approval authority.

Additional executed checks:

- `PYTHONPYCACHEPREFIX=/tmp/phase17h-r0-r1/bytecode python -m compileall -q .`:
  exit 0; no ownership changes required.
- `ruff check --no-cache --select E9,F63,F7,F82` on all eight changed Python files:
  exit 0, all checks passed. No project-wide Python formatter/type-checker
  configuration was found; no unrelated mass formatting or typing changes made.
- `git diff --check`: exit 0.

Implementation self-review inspected the entire production diff and test changes,
verified the prior renderer snapshot byte identity, unchanged schemas/G2 and
limits, all-stage instruction coverage, fixture patch restoration, error paths,
checkpoint identity separation and absence of provider-specific branching.
Separate pre-commit review checked the task's modified/new files for secrets,
private key material, `.env` files, machine-specific production paths, debugging
output, temporary/runtime artifacts, stale TODOs, dependencies and API changes.
The only added fixtures are reviewable synthetic hashes and historical source;
no private response, identifier inventory, database or generated runtime output
is included. Documentation links and whitespace are checked before final reporting.

Docker/Compose/Helm/Kubernetes validation is not applicable to this prompt/test
change and was not run; no packaging, dependencies or deployment configuration
changed. Kubernetes/AKS operations were explicitly excluded.

## 8. Exact changed files and documentation

| File | Change |
| --- | --- |
| `documents/digestion/managed.py` | v5 template and two instruction paragraphs |
| `tests/integration/test_final_offline_azure_compatibility.py` | R0 witnesses/controls; pinned historical v4 and active unbounded fixtures |
| `tests/integration/test_live_failure_observability.py` | v5 prompt/fingerprint/sizing assertions; preserve historical v3/v4 checks; round-trip both versions/budget policies |
| `tests/integration/test_phase17hl_offline_e2e.py` | Exact blended qualification failure through durable workflow/accounting |
| `tests/integration/test_foundry_l1_launcher.py` | Active v5 expectation and rejection of previous generation configuration |
| `tests/integration/test_output_limit_hardening.py` | Active v5 expectation; unchanged four-call limits/accounting |
| `tests/unit/documents/test_managed_inference.py` | Active v5 expectation; reject explicit v3/v4 on all profiles |
| `tests/unit/test_g1_source_compatibility.py` | Run the fixed historical G1 projection's managed-source mutation checks on the pinned v4/G1 renderer |
| `tests/fixtures/digestion_contracts/managed_prompt4.py.txt` | Add immutable previous v4/G1 renderer source fixture |
| `tests/fixtures/digestion_contracts/managed_prompt5.json` | Add active v5 source and nine deterministic contract fingerprints |
| `tests/fixtures/digestion_contracts/README.md` | Explain v4 historical replay and v5 transition |
| `README.md` | Active v5 and precise failed-live/offline-only boundary |
| `docs/evaluation/phase_17h.md` | Distinguish historical v4 success and current offline v5 |
| `docs/evaluation/phase_17h_foundry_validation.md` | Current generation/approval compatibility boundary |
| `docs/codex/prompts/phase_17h_r0_r1_evidence_provenance_hardening.md` | Preserve clean task scope and acceptance requirements |
| `docs/codex/reports/phase_17h_r0_r1_evidence_provenance_hardening.md` | This engineering evidence report |

Final `git status --short` shows **12 modified tracked files**, **four new task
files** and **five pre-existing untracked files**. `git diff --stat`
reports **12 files changed, 324 insertions, 27 deletions**; Git's unstaged diff
statistics do not include the four new untracked task files in the table.

Five pre-existing untracked authorization/execution/investigation Markdown files
were present at the start and are outside this task's changes. They remain
untouched. No Git staging, commit, push, branch change, reset or remote mutation
occurred. Final Git status and diff statistics are reported with completion.

## 9. Remaining risk, future preparation and readiness

Exact-copy wording reduces ambiguity about complete UUIDs and identifier roles;
stage-local rules clarify how to preserve qualification/conflict provenance
without turning every visible child ID into direct citation authority. This is
a justified reliability improvement, not measured proof of fewer model errors.
A model can still emit foreign IDs, omit required coverage, produce unsupported
claims or fail other strict contracts. Offline tests prove rejection and prompt
content, not that live generation always complies. R2/R3 remain unimplemented.

Before any separately authorized live reassessment, engineering/operator review
must bind the exact final generation digest and v5 settings to a fresh private
configuration and plan, remeasure the actual source/child requests against the
unchanged limits, and verify security, quota, pricing, model/capability, credential
lifetime and operational readiness through the established process. New independent
approval and explicit execution authorization would be required. Historical
checkpoints must keep their old identities; no reset of failed-run/replay state or
reuse of the consumed approval is appropriate. Those preparations, signing and
execution are not performed or authorized by this task.

**R0: PASS. R1: PASS.** The implementation, focused G1/G2/provider/integration
checks, complete offline suite, compilation, scoped lint and reviews pass. There
is no remaining offline engineering compatibility blocker. Engineering is ready
to support a separately reviewed and authorized live reassessment after the
preparations above; it is not permission to execute one. The deliberate v5
configuration/checkpoint transition remains mandatory. This task does not close
Phase 17H live validation or independently establish semantic quality. No new
paid inference is authorized.

**R0/R1 OFFLINE ENGINEERING: PASS**
