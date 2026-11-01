# Two-layer validation for LLM structured output

Provider-constrained generation and application acceptance are separate contracts.
A provider schema reduces structural generation errors. Only the application can
accept a result for persistence. Passing the first layer does not imply passing
the second.

Status — 1 November 2026: [Attempt 6](../codex/reports/phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md)
completed one strict provider response under active managed-prompt/4, passed
application validation and settled known usage with no automatic retries. This
supplies exact-deployment single-analysis evidence beyond the historical capability
review below. It does not validate every schema, representative model quality,
full live hierarchical digestion or grounded Q&A. Phase 17H remains PARTIAL.

## Assess capability before selecting a mode

Record the provider, deployment, model version, interface, API version, schema
subset, limits and evidence date. Distinguish documentation, local contract tests
and successful deployment verification. Do not infer capability from a model name
or assume that Azure, another OpenAI-compatible service and Ollama accept identical
keywords. A `json_schema` mode with `strict=false` is not strict generation.

For this implementation, Microsoft's [structured output specification](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs)
documents Chat Completions `response_format`, v1, closed objects, required fields,
nullable unions and references, with 100 properties and five nesting levels. Its
string subset excludes format, pattern and length constraints. The [reasoning
model feature table](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning#api-and-feature-support)
lists structured outputs and Chat Completions for GPT-5.4 mini, 2026-03-17.
These are documentation findings reviewed on 2026-10-16, not live deployment proof.

## Layer 1: provider structure

Use a deterministic, versioned conversion from the authoritative application
schema. Preserve property names, types, arrays, closed object boundaries, enums,
nullable alternatives and local references. Require every property for generation,
including fields with storage defaults. Convert a constant to a singleton enum.

PolyMind's `azure-strict/1` removes only `title`/`default` annotations and string
`format: uuid`, `minLength`, `maxLength`, `pattern`. Unknown keywords, other formats,
open objects, unresolved or remote references, recursion and excessive complexity
fail configuration validation. The converter is deliberately narrower than every
construct Azure might support. Extend its rules only after a new assessment and
regression tests; never add a generic recursive keyword-stripping operation.

The StageResult schema has 22 properties and 1,790 compact ASCII bytes after
conversion. Its deepest container path is StageResult → claims array → Claim →
qualifications array → Qualification → evidence_ids array. The local guard counts
five nested containers below a root at depth zero (three object levels). Azure's
published nesting wording does not specify root/array counting; acceptance of this
boundary must be verified with the actual deployment. Do not claim a local JSON
Schema validator proves Azure acceptance.

## Layer 2: authoritative application acceptance

Keep strict parsing, duplicate-key rejection, Pydantic types and validators,
`extra='forbid'`, UUID syntax, bounded text, subject patterns, exact schema version,
allowed evidence membership, stage and claim identity, ordering, qualifications,
contradictions, lineage and complete coverage. Canonically serialize with defaults
and escaping and enforce the independent canonical byte ceiling before persistence.
Do not drop properties, repair identifiers, truncate content or bypass validation.

For example, a malformed UUID can satisfy the provider's string schema and fail
Pydantic. A syntactically correct UUID can satisfy both schema layers and fail
evidence membership. Neither failure is a reason to weaken application acceptance.
The provider schema is intentionally a structural subset of the acceptance contract.

Managed generation now defaults to `managed-prompt/4`. It explicitly permits a
non-null subject only on `kind="fact"`; `unknown`, `unsupported`, `commentary` and
`structural` must emit `subject=null`. Facts may also use null. Populated factual
subjects retain the existing 1–128 character Token constraints and fact support
requirements. Every generated field remains required, so omission is not the
generated equivalent of explicit null even though stored models supply defaults.
The `stage-result/1` domain validator and `azure-strict/1` schema are unchanged:
the schema still permits a non-fact with a populated subject, and application
validation still rejects it without repair or another call.

Explicit v3 stage settings are rejected by the active configuration model.
Requests must match the active prompt profile and inference configuration; old
plans/checkpoints cannot be rebound for execution. Previously validated results
and immutable checkpoints remain readable under their original contracts.
Historical v3 renderer/request witnesses are retained separately in offline tests.
New live work requires fresh planned requests, source/configuration bindings and
independent authorization; historical approvals do not authorize v4. See the
[implementation report](../codex/reports/phase_17hl_managed_prompt4_subject_contract_implementation.md)
for the migration evidence and deferred work.

## Failure handling and operations

Refusals, incomplete output, transport errors and malformed envelopes remain
possible. Reject them with content-free errors. Preserve known usage and settle
billable work even when later validation rejects the result; missing usage stays
unknown. Do not silently retry, switch models or fall back to a less strict mode.
Use the existing bounded client, deadline and accounting path.

Budget completion tokens, raw UTF-8 bytes, canonical ASCII bytes and HTTP envelope
bytes independently. Test explicit defaults, Unicode escaping and exactly-at-limit
and over-limit cases. Include fake transport tests for the exact request and both
validation layers, plus governed workflow failure and success controls. Block
network access during offline tests.

Version and fingerprint the conversion rules, strict selection, generated schema
and workflow configuration. Preserve historical audit formats and old evidence,
but reject stale execution configurations. A changed generation contract requires
fresh review and operator authorization before live use; old signed approval is
not transferable. A live verification should test the exact schema and interface,
then retain evidence of request acceptance, complete output and local validation.
