# Phase 17H-L — Two-layer structured output

**PASS — TWO-LAYER STRUCTURED OUTPUT IMPLEMENTED AND VERIFIED OFFLINE; AZURE LIVE COMPATIBILITY PENDING**

2026-10-16, existing `master`. Previous tracked and untracked work retained.
This is an implementation report, not an execution packet or live authorization.

## A. Architecture and capability evidence

Previously L1 digestion requested `json_object` with the full StageResult schema
in its prompt. The generic schema branch used `strict=false`. L1 digestion now
selects a versioned capability that sends `response_format.type=json_schema`,
`json_schema.name=polymind_stage_result`, `strict=true`, and the converted schema.
The original application schema still appears in the prompt. Application decoding,
Pydantic validation, evidence/identity/lineage/coverage checks, canonical byte
limits and persistence are unchanged. Canonical size is checked early within the
existing validator, before domain checks; this implementation preserves that order.

Microsoft's [structured output documentation](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs)
documents the v1 Chat Completions interface, required properties, closed objects,
references and nullable unions, and excludes the relevant string constraints. The
[model feature table](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning#api-and-feature-support)
explicitly lists GPT-5.4 mini, 2026-03-17, with structured outputs and Chat
Completions. The [Azure model availability matrix](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions)
lists the model in Global Standard. Repository configuration pins that model/version,
GlobalStandard and deployment `epolymind-gpt-54-mini`; no Azure discovery was run.
These pages were reviewed on the report date. No fundamental model/interface
incompatibility was established. Exact deployment acceptance remains unverified.

The prior exact-equivalence assessment remains a valid historical assessment of
its narrower authorization. This task explicitly authorizes structural provider
constraints plus stronger independent application validation. The provider cannot
prove evidence membership, lineage or the validity of arbitrary prose.

## B. Implementation and contract

Changed source files:

- `llm/azure_schema.py`: new deterministic converter and complexity guard.
- `llm/structured.py`: explicit optional `schema_profile='azure-strict/1'`, mode
  validation, infrastructure-owned conversion and provider compatibility checks.
- `llm/openai_compatible.py`: strict request selection through the existing bounded
  client, plus strict refusal and malformed-envelope rejection with retained usage.
- `llm/ollama_client.py`: rejects the incompatible strict profile before transport.
- `documents/digestion/managed.py`: configuration-time conversion validation,
  `managed-generation/2` gate and binding of the generated provider schema.
- `tests/performance/foundry_recalibration.py`: explicit opt-in capability
  `gpt54mini-30k/2`; the default remains the historical JSON-object capability.
- `tests/performance/foundry_preflight.py`: L1 digestion opts in; Q&A and L2 retain
  their existing modes. The synthetic provider emits explicit defaults in strict
  mode; this fixture construction is not response repair in application code.
- `tests/performance/foundry_l1.py`: generation digest includes converter source.
- `tests/unit/documents/test_two_layer_output.py`: focused new regression coverage.

The allowlist preserves all properties, primitive types, homogeneous arrays,
closed objects, supported enums, nested anyOf/null and local `$defs` references.
It requires every object property and normalizes const to a singleton enum,
including exactly `stage-result/1`. Only title/default annotations and string
minLength/maxLength/pattern/UUID format are removed. Other formats, keywords,
constructs, open objects, unresolved/remote references, recursion and excessive
complexity fail closed. No stored model, field name, application type, validator,
identifier or model response is changed.

There are 22 properties in four object schemas, and 1,790 compact ASCII provider
schema bytes. The maximum resolved container nesting is five below root depth
zero: root → claims array → Claim → qualifications array → Qualification →
evidence_ids array. This is six containers including root and three object levels.
The earlier assessment's five-container description omitted the final evidence
array. Azure documents five nesting levels without defining root/array counting;
this boundary interpretation remains an explicit deployment-confirmation risk.
Local tests enforce the stated root-zero convention and the 100-property ceiling.

The generic `json_schema` mode still sends `strict=false`, name `stage_result` and
its original schema. JSON-object and prompt callers retain previous behavior.
Unset schema_profile is omitted from serialization, and legacy managed settings
are fingerprinted without the new default generation_profile field. Historical
capability/settings records remain readable; old result/audit formats are unchanged.
The prompt text stays `managed-prompt/3` because its application instructions did
not change; the new wire contract is separately versioned as managed-generation/2.

Generation contract SHA-256:

```text
Before: 2ff2aff8f575ed99b23108dd5d10c2f7a73a55fb6cc7e073107e0597124c7290
After:  6f936342efb8e22faf23d59ebf71f7846d3255692d398c27d1e6a449ef41e247
Provider schema: 4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2
```

Recomputed configuration fingerprints for the pinned deployment and L1 settings
(24,800 stage input allowance, 3,000 output tokens, 26,192 envelope):

```text
Capability before: b21cc2919b76636013209f50d8b8858a9ebe69ed59802c54a70053607a810a26
Capability after:  d8178b3c0809fb749a6649b901438700231fba98eae19304349d2e526bff7d2c
Managed before:    12a6d4ccb1bf96e29a3f92cc9d7518eaa3e1b56e06d159deeb1e90bef17a0138
Managed after:     7eaa6b52ad387f9f0c82e318e9c74fa378ffda0baec85d0f7157cc4ab0553519
```

These were computed in memory, without a provider call or authority construction.
No future LaunchConfiguration/approval packet was created or recomputed. Its full
fingerprint depends on future operator-reviewed authority/window values. The
existing launch validator rejects the Attempt 3 generation digest before approval
access; the test invokes that gate directly without signing. Historical packets
and audits were not edited. Future execution requires fresh configuration review
and authorization; Attempt 3's signature cannot authorize this contract.

## C. Focused offline verification

**214 tests passed across the final focused selection (213) and one additional
historical compatibility test (1); no failures or skips.** The 213-test selection
completed in 7.40 seconds; the added test in 0.39 seconds. An initial run had one
new fixture failure because it combined a 40,000-input test stage with the 28,000
L1 capability; the fixture was corrected without changing production bounds.

```bash
PYTHONPATH=/tmp/polymind-strict-assessment:. python -m pytest -p offline_guard \
  tests/unit/documents/test_two_layer_output.py \
  tests/unit/documents/test_strict_schema_compatibility.py \
  tests/integration/test_attempt3_serialization.py \
  tests/unit/documents/test_independent_json_limits.py \
  tests/unit/documents/test_output_limit_sizes.py \
  tests/unit/test_structured_provider.py \
  tests/unit/test_output_limit_diagnostics.py \
  tests/integration/test_output_limit_hardening.py \
  tests/unit/documents/test_digestion.py::test_reducer_cannot_omit_child_or_invent_source \
  tests/unit/documents/test_digestion.py::test_invalid_outputs_or_source_references_rejected \
  tests/unit/documents/test_digestion.py::test_qualifications_and_opposing_evidence_survive_root -q
```

The final historical compatibility case was added and run individually afterward.
The external offline_guard plugin blocks connections, sendto and DNS from pytest
configuration onward; the new module also blocks networking independently. Tests
use the installed Draft 2020-12 JSON Schema validator with local references, fake
HTTP and synthetic content. No dependencies were installed. No full suite, live
fixture replay, L2 run or signing test ran.

Attempt 3's eight extras fail provider-schema validation. Missing mandatory text,
wrong schema version and nested forbidden fields also fail. Malformed UUIDs,
invalid subject syntax, empty/oversized strings pass structural validation but
fail Pydantic. Well-formed nonexistent evidence, invalid originating stage/claim
order, unsupported lineage, missing evidence, invalid qualifications and conflicting
evidence references remain rejected locally. Existing selected tests exercise
reducer coverage, original-source scope and qualification/conflict propagation.
A valid control passes both layers. The actual synthetic governed four-call
workflow validates each strict response against the emitted provider schema,
completes digestion and Q&A, and settles all calls.

Failure tests show one-call settlement after a structurally valid malformed UUID,
provider refusal with or without text, completion truncation, invalid envelopes,
unknown usage and accounting failures. There is no retry, fallback or second call
on failure. Known synthetic usage settles EUR 0.000011; unknown usage stays UNKNOWN.
Existing byte tests retain independent 10,000/10,001 boundaries, default expansion,
Unicode escaping, HTTP bounds and diagnostics. Historical capability/settings
round-trips and legacy managed fingerprints are tested; real historical audits
were neither opened nor rewritten.

All operational controls remain unchanged: 10,000 UTF-8 response bytes; 10,000
canonical ASCII bytes; 3,000 completion tokens; 25,000 input reservation/call;
four calls; aggregate 100,000/12,000 reservations; 28,000 context; 26,192 HTTP bytes;
at least 61-second spacing; EUR 5 ceiling; `polymind-evaluation/1`. No pricing,
quota, identity, RSA policy or governance code changed in this task.

## D. Review, compatibility and remaining work

Offline implementation is validated. Model/interface support is documented.
Actual Azure deployment/schema compatibility has not been verified live. A local
JSON Schema validator checks semantics, not Azure's request acceptance or decoder.
UUID errors and invented evidence remain possible, and must fail application
validation. Request rejection (including nesting interpretation), refusals,
truncation and token/byte pressure remain possible with strict generation.
No latency, real-model quality or spending improvements are claimed.

Implementation self-review compared task changes against pre-edit copies, checked
provider boundaries, generic-mode compatibility, schema preservation, resource
handling and accounting. It moved provider-name compatibility selection into
infrastructure. A separate pre-commit review checked touched files for secrets,
temporary/generated artifacts, unexpected dependencies, response repair and
unrelated changes. Application validation and persisted result schemas were not
edited. The reusable guideline is `docs/engineering/llm_structured_output_validation.md`;
the authorized scope is preserved under `docs/codex/prompts/`.

Minimum next step: review the code and exact schema, then obtain separate operator
authorization for deployment-specific compatibility validation with a fresh bound
configuration. Confirm Azure's nesting interpretation and exact request acceptance
before claiming live support. This report does not prepare Attempt 4 or authorize
any live call. The separate historical launcher exit-code issue remains outside
this change.

## E. Safety

Azure inference calls: **0**. Azure infrastructure changes: **0**. Governance
changes: **0**. Additional cloud spending: **0**. RSA signing: **0**. Approval
consumption: **0**. Attempt 4 preparation/execution: **0**. Git staging/commits/pushes:
**0 / 0 / 0**. Test stores are temporary synthetic fixtures, not new application
databases. Existing environment files, authority databases and historical evidence
were preserved.

Final validation: `PYTHONPYCACHEPREFIX=/tmp/two-layer-pycache python -m compileall
-q .` and `git diff --check` both passed. No configured Python formatter/linter
was found in the inspected repository configuration. Docker validation does not
apply: no dependency, container or deployment configuration changed.

Final `git status --short --branch` shows the existing dirty `master` with prior
work plus this task's additions, all unstaged. `git diff --stat` reports **17 tracked
files changed, 446 insertions, 38 deletions** across the entire existing worktree;
this includes prior work and excludes untracked files, so it is not a task-only
change count. The final generation digest was recomputed and matches the value
above. No commit or push occurred.
