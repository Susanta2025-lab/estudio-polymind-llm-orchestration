# Phase 17H-L — Structured-output compatibility assessment

**BLOCKED — EXACT STRUCTURED-OUTPUT COMPATIBILITY ISSUE**

16 October 2026. Assessment on existing `master`; prior tracked and untracked changes preserved. Strict generation was not enabled. The existing StageResult generation schema cannot be represented exactly within the documented Azure strict subset without dropping validation constraints. This is a documented-contract blocker, not an observed Azure rejection.

## A. Compatibility evidence

The supplied deployment is `epolymind-gpt-54-mini`, model `gpt-5.4-mini`, version `2026-03-17`, GlobalStandard, Spain Central. Repository launch configuration pins that deployment/model/version/tier; region comes from the supplied context and postmortem, not fresh Azure discovery. No deployment or credential query was made.

Microsoft's [reasoning-model feature table](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning#api-and-feature-support) explicitly lists structured outputs and Chat Completions for `gpt-5.4-mini`, `2026-03-17`. That establishes model-level documentation, not deployment verification.

Azure's [structured-output documentation](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs#json-schema-support-and-limitations) documents v1 support; every property must be required, objects must forbid additional properties, and local references, arrays and nested nullable unions are supported. Limits are 100 object properties and five nesting levels. String `minLength`, `maxLength`, `pattern` and `format` are unsupported. These restrictions apply to Chat Completions and Responses. The page's supported-model list omits newer models present in the separate feature table. No evidence establishes a deployment-specific exception to the keyword restrictions.

The actual adapter posts to `/openai/v1/chat/completions`. The prospective strict payload is:

```python
response_format = {
    'type': 'json_schema',
    'json_schema': {
        'name': 'polymind_stage_result',
        'strict': True,
        'schema': generation_schema(),
    },
}
```

This illustrates the request shape, **not an approved or compatible request**. No empty substitute schema was used. The exact generated schema was inspected locally and tested with the installed JSON Schema validator.

The existing request selects the deployment through `model`, sends system/user messages, `stream=False`, `max_completion_tokens=3000`, and `reasoning_effort='low'`; temperature is omitted. The bounded adapter uses the existing client, timeout, deadline, transport ceiling, usage extraction and normalized errors. It is not the Responses API. No second client is needed to express the wire format.

## B. Exact schema assessment and blocker

`generation_schema()` starts with `StageResult.model_json_schema()` and marks all properties required recursively. There are 22 declared properties across four closed object definitions: StageResult (7), Claim (11), Qualification (2), ClaimLink (2). All object boundaries already have `additionalProperties=false`; all local references resolve. The longest instance path is root → claims array → Claim → qualifications/lineage array → Qualification/ClaimLink (five container levels, three object levels). Complexity is not the blocking issue.

| Schema location | Actual constraint | Assessment |
|---|---|---|
| StageResult.stage_id; Claim.claim_id/originating_stage; ClaimLink.stage_id/claim_id | string, `format: uuid` | UUID constraint cannot be retained in the documented subset |
| Claim.evidence_ids/contradicting_evidence_ids items; Qualification.evidence_ids items | string, `format: uuid` | Same blocker for evidence references |
| Claim.text; Qualification.text; open_questions/limitations items | `minLength: 1`, `maxLength: 4096` | Nonempty bounded text cannot be represented exactly |
| Claim.subject string branch | length 1–128, `pattern: ^[a-zA-Z0-9_./:-]+$` | Token syntax and length cannot be represented exactly |
| Claim.subject null branch | `type: null` inside `anyOf` | Preserve null; do not make other fields nullable |
| schema_version | `const: stage-result/1` | Could become a singleton enum without changing accepted values |
| Default annotations | null, arrays, enum defaults, schema version | Could remove annotations after requiring explicit fields; keep model defaults unchanged |

Requiring explicit defaults is already the generation contract. The storage model still accepts omitted default fields, so omission of a default is not falsely described as a Pydantic failure. Missing mandatory claim text is rejected by both validators. Arrays are homogeneous item schemas, not fixed positional tuples; no tuple-keyword conversion is needed. Titles/default annotations and the singleton const are not the decisive incompatibility.

Removing format/pattern/length constraints changes the accepted output language. Local counterexamples prove that a stripped schema accepts malformed claim UUIDs, empty text, 4,097-character text and an invalid subject that the original schema rejects. Finite enums for source identifiers could restrict particular requests but would not be an equivalent conversion of the general schema, and would not solve arbitrary constrained prose. No compliant, narrow exact conversion was established.

The user explicitly prohibited permissive substitute schemas and required reporting incompatibility when exact conversion is impossible. Therefore no converter, strict capability, runtime change or live enablement was added. Keeping Pydantic unchanged while stripping provider constraints would still violate that instruction.

## C. Current versus proposed behavior and implementation boundary

Current L1 capability selects `json_object`. The existing generic `json_schema` branch sends `name='stage_result'` and **`strict=False`**. The enum spelling alone is not strict support. New fake-transport assertions document both existing paths with the exact nested generation schema; they do not endorse sending that schema as strict.

A compatible strict closed-object schema could prevent Attempt 3's eight extra properties. Malformed evidence UUID prevention additionally requires enforceable identifier constraints; Azure's documented subset does not establish that guarantee. Even correctly formatted UUIDs can cite nonexistent evidence. Application validation remains mandatory for stage/claim identity, originating stage, evidence membership and coverage, qualifications, contradictions, lineage, claim ordering and canonical byte bounds. No repair, property filtering, evidence substitution, truncation, retry or fallback was introduced.

Task changes:

- `tests/unit/documents/test_strict_schema_compatibility.py`: assessment assertions, fake current-mode requests, synthetic structural failures, unknown evidence, and local proof against constraint stripping.
- `tests/unit/documents/test_independent_json_limits.py`: corrected the stale-contract test's SimpleNamespace fixture to include `governance_policy.evaluation=None`; runtime validation is unchanged.
- This report and a condensed phase-scope record in `docs/codex/prompts/phase_17hl_structured_output_compatibility.md`.

No production source changed. Strict-mode pre-inference rejection and `strict=True` request tests are not claimed as implemented: exact-schema incompatibility stops before introducing that mode. Existing `json_object`, permissive `json_schema`, Ollama, publication, API, financial settlement and security behavior remain unchanged.

Generation-contract digest was recomputed and remains:

```text
2ff2aff8f575ed99b23108dd5d10c2f7a73a55fb6cc7e073107e0597124c7290
```

The fingerprint already includes managed schema generation, models, validation, planning, structured contracts, bounded HTTP, the adapter and L1 composition. Assessment tests/docs do not change it. Stale earlier digests remain rejected before approval access. This task does not invalidate Attempt 3's fingerprint or authorize reuse of its approval. Any future request/schema implementation must change the bound contract, reject stale configurations and undergo fresh configuration review and separate authorization. No launch packet was created.

All limits remain: 10,000 UTF-8 content bytes; 10,000 canonical ASCII bytes; 3,000 completion tokens; 25,000 input reservation per call; four calls; 100,000/12,000 total reservations; 28,000 context; 26,192 HTTP bytes; 61-second spacing; EUR 5; `polymind-evaluation/1`. No quota, price or governance authority changed.

## D. Offline regression verification

Focused selection covers the new assessment module plus existing Attempt 3, independent byte limits, output-size, provider, output diagnostics and accounting tests. An external pytest plugin blocks socket connect/connect_ex/sendto, create_connection and DNS from pytest configuration onward. The new module also blocks networking independently. Existing `jsonschema` was available; no dependency was installed. Its format checker was explicitly enabled, and validation used local references only. This checks JSON Schema semantics, not Azure acceptance.

Synthetic cases cover malformed evidence UUID, eight extra properties, both together, unknown claim/qualification/lineage fields, missing mandatory text, valid output and valid UUID with nonexistent evidence. The last case passes local schema validation and fails the actual evidence validator. Existing workflow tests verify one-call schema rejection with known usage settled, no retry or subsequent stage, unknown usage fail-closed, retained original output-limit category, sanitized audit diagnostics, and accounting failure handling. No governance investigation or signing tests were rerun.

Boundary coverage includes exactly 10,000 and 10,001 bytes, canonical default expansion, Unicode escaping, raw versus canonical independence, transport overflow, completion truncation, malformed envelopes and missing/inconsistent usage. The previous failures are accepted as established; no private response replay or renewed root-cause investigation occurred.

Initial selection: 152 passed, one failed because the old stale-contract fixture lacked the new governance-policy attribute. After the fixture-only correction: 153 passed. Two current-mode payload cases were then added; final results are recorded below.

## E. Remaining risks and smallest safe next step

Strict support for the actual deployment and this exact schema remains unverified. Sending the current schema with `strict=True` could be rejected. Refusal, truncation and incomplete outputs remain failure paths even for a supported schema. No latency or token-consumption effects were measured; explicit fields and provider schema processing may change both, within unchanged ceilings.

The smallest safe next step is to obtain authoritative Azure confirmation of support for the exact string constraints on this model/interface, without inference. If unsupported, exact conversion requires reconsidering the stated requirement in a separately scoped design decision; silently using a weaker provider schema is not an acceptable implementation here. Only after resolving that issue should strict capability gating, exact payload tests and a newly fingerprinted managed profile be implemented. Actual model behavior would still require a separately authorized live validation. No Attempt 4 is prepared or recommended for immediate execution.

The separate launcher defect remains: `foundry_l1.main()` prints a terminal FAILED result and returns normally; only exceptions invoke `parser.exit(1)`. It needs a separately verified nonzero exit after audit finalization. No launcher refactoring or fix was mixed into this assessment.

## F. Safety and review

Azure inference calls: **0**. Azure infrastructure changes: **0**. Governance migrations: **0**. New spending: **0**. RSA signing: **0**. Approval consumption: **0**. Attempt 4 preparation/execution: **0**. Git staging/commits/pushes: **0 / 0 / 0**.

Existing historical audits, approvals and authorities were not opened or modified. Existing integration fixtures use disposable synthetic test stores; no new application database or migration was introduced. The original tracked diff is preserved byte-for-byte. Self-review checked schema paths, null/default distinctions, scoped test changes and the no-conversion decision. Separate pre-commit review checked new files for sensitive content, debug code, dependencies, local runtime paths, unrelated changes and unsupported success claims. No runtime API, provider boundary or stored contract changed. Docker validation is not applicable to tests/documentation-only changes.

### Final validation record

Final focused run: **155 passed, 0 failed, 0 skipped in 3.84 seconds**, including 13 new assessment cases. Command:

```bash
PYTHONPATH=/tmp/polymind-strict-assessment:. python -m pytest -p offline_guard \
  tests/unit/documents/test_strict_schema_compatibility.py \
  tests/integration/test_attempt3_serialization.py \
  tests/unit/documents/test_independent_json_limits.py \
  tests/unit/documents/test_output_limit_sizes.py \
  tests/unit/test_structured_provider.py \
  tests/unit/test_output_limit_diagnostics.py \
  tests/integration/test_output_limit_hardening.py -q
```

`python -m compileall -q .` passed with `PYTHONPYCACHEPREFIX` under `/tmp`; `git diff --check` passed. No configured Python formatter/linter was found in the inspected standard configuration files. No full-suite execution occurred. Mock results do not prove Azure generation compliance.

Final `git status --short --branch`: existing dirty `master` retained, with three new untracked assessment files and the fixture correction in the already-untracked independent-limit test. `git diff --stat`: **17 files changed, 386 insertions, 33 deletions**, entirely pre-existing tracked changes; byte-for-byte comparison of the tracked diff before/after passed. These totals exclude untracked files and are not a task-only diff. No files were staged, committed or pushed.
