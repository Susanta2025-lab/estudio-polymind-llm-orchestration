# Phase 17H-L — Independent JSON byte limits

Status: **PASS — INDEPENDENT 10,000-BYTE LIMITS VERIFIED; 3,000-TOKEN CEILING PRESERVED**

Work performed on the existing `master` working tree on 15 October 2026. Existing tracked and untracked work was retained. This is an implementation and offline validation report, not an execution packet or operator approval.

## A. Implementation

`documents/digestion/models.py` adds `DigestionProfile.max_response_bytes`, an optional positive provider-neutral content bound, and `response_byte_limit`, which falls back to the old canonical bound for legacy profiles. `max_result_characters` remains the public configuration name for **canonical serialized bytes**; retaining its name avoids breaking existing configuration consumers. `budget()` removes only the invalid numerical comparison between bytes and reserved output tokens. Positive resource validation and context/reservation validation remain. The serializer omits the new unset field so legacy non-managed profile fingerprints remain stable.

`documents/digestion/managed.py` updates `ManagedSynthesisInference.render()` and `analyze()` to use the provider-content limit independently of the canonical bound. The prompt is explicitly versioned `managed-prompt/3`: it retains the version-2 required fields, evidence, qualifications, conflicts and lineage instructions, adds the raw UTF-8 content bound, and states that the separate completion-token ceiling can still prevent completion. `StageProfile` and the planning profile agree on that version. `ManagedSettings.max_response_envelope_bytes` optionally pins the transport bound.

`documents/digestion/validation.py:validate_result()` bounds decoding by provider-content bytes and independently bounds `encode(result)` by canonical bytes. Strict parsing, duplicate-key rejection, canonical ASCII escaping, schema, evidence and lineage checks are unchanged. Raw overflow is not accepted because canonical output would fit, and canonical expansion is not accepted because raw content fitted. No output is truncated or repaired.

`llm/structured.py:GenerationRequest` adds an optional trailing `max_response_envelope_bytes` argument. `llm/bounded_http.py:validate_request()` independently validates it. `llm/openai_compatible.py:execute()` and `llm/ollama_client.py:execute()` honor it while retaining their previous calculated envelope limit when unset. Timeouts, bounded reads, sanitized output diagnostics, usage handling and exception propagation remain unchanged. No retry or fallback was introduced.

`tests/performance/foundry_preflight.py:execute()` sets the L1 managed profile to 10,000 content bytes and 10,000 canonical bytes, and explicitly retains the 26,192-byte HTTP cap. The L2 branch retains its numeric limits. `tests/performance/foundry_l1.py:generation_contract_digest()` additionally binds validation, planning, bounded HTTP and the OpenAI-compatible adapter, so changes to enforcement cannot leave the generation contract unchanged.

Test changes are in `tests/unit/documents/test_independent_json_limits.py`, `test_output_limit_sizes.py`, `test_managed_inference.py`, `tests/integration/test_output_limit_hardening.py`, and the prompt-version assertion in `test_foundry_l1_launcher.py`. The launcher test module was not executed because its fixtures sign synthetic approvals; stale contract rejection was tested directly without signing.

Backward compatibility: unrelated numeric defaults remain unchanged, including publication/Q&A limits. The optional transport argument preserves positional callers. Managed prompt/configuration fingerprints intentionally change, so existing managed plans/checkpoints require replanning rather than reuse under the changed contract. Explicit old `managed-prompt/2` stage configurations are rejected. No API, stored result schema, serialization or provider-specific domain logic was changed.

## B. Effective L1 limits

| Resource | Effective value |
|---|---:|
| Raw provider response content | 10,000 UTF-8 bytes |
| Canonical serialized digestion result | 10,000 ASCII JSON bytes, including Unicode escapes |
| HTTP response envelope | 26,192 bytes |
| Completion reservation/request ceiling | 3,000 tokens |
| Per-call input reservation ceiling | 25,000 tokens |
| Managed rendered input allowance | 24,800, plus 200 overhead/safety |
| Total L1 input/output reservations | 100,000 / 12,000 tokens |
| Context budget | 28,000 tokens |
| Maximum calls | 4 |
| Financial ceiling | EUR 5 |
| Governance policy | `phase17hl-l1/2`, unchanged |

The financial contract, admission policy, prices and governance implementation were not edited. Provider payload tests assert `max_completion_tokens=3000`. The explicit four-call integration test uses a synthetic contract bounded to the L1 totals; the shared historical synthetic fixture otherwise defaults to larger multi-stage totals. All four calls settle at the existing synthetic price of `0.000011` each. These synthetic amounts are not Azure charges.

## C. Offline verification

Final focused selection: **310 passed, 1 deselected**. The deselected case is the L2 workflow. Tests use the existing `/tmp/output-limit-tests/offline_guard.py` plugin, which blocks socket connections, sendto and DNS, and isolates the legacy ungoverned managed-inference unit module. No full repository suite was run.

```text
PYTHONPATH=/tmp/output-limit-tests:. python -m pytest -p offline_guard \
 tests/unit/documents/test_independent_json_limits.py \
 tests/unit/documents/test_output_limit_sizes.py \
 tests/unit/documents/test_managed_inference.py \
 tests/unit/documents/test_digestion.py \
 tests/integration/test_document_digestion.py \
 tests/unit/test_output_limit_diagnostics.py \
 tests/unit/test_structured_provider.py \
 tests/unit/test_foundry_preflight.py \
 tests/integration/test_output_limit_hardening.py \
 tests/integration/test_foundry_offline_workflow.py -k 'not L2' -q
```

Both boundaries accept 2,999, 3,000, 6,000, 9,999 and exactly 10,000 measured bytes, and reject 10,001. Canonical boundary fixtures pass the real evidence validator; deterministic prose padding uses a narrowly configured 4,096-character claim limit for those size tests only. Runtime claim limits were not raised. A separate rendered-contract test sets content to 9,000 and canonical to 10,000, demonstrating independent configuration.

The existing fixtures retain their measured sizes: minimal explicit JSON 484 bytes; eight evidence-bearing claims 2,836; eight qualified claims 3,668; eight qualified claims with lineage **4,477**. Qualified and lineage results pass real evidence/lineage validation with a 3,000-token reservation. Omitted defaults, explicit defaults, UTF-8 versus ASCII escapes, canonical expansion past the bound, and raw whitespace overflow despite small canonical output are covered.

Exactly 10,000 canonical bytes produce synthetic HTTP envelopes of 10,479 bytes for ordinary prose, 10,879 for accented text, and 11,279 for emoji, backslash and quote cases. All fit 26,192. Double encoding can at most double an ASCII JSON content string; the retained cap leaves 6,192 bytes beyond that conservative 20,000-byte content envelope. Arbitrarily large provider metadata is not guaranteed to fit and remains rejected. A separate adversarial Unicode-only content response fits the raw content bound but exceeds the wire envelope when escaped; it correctly fails with unknown content-level diagnostics at the envelope boundary. It is not a valid canonical stage result. The HTTP ceiling was not increased.

Completion truncation at 3,000 tokens still fails for both `length` and `max_tokens`, with accurate content-free diagnostics and one provider call. Existing integration tests verify terminal failure, no subsequent call, known settlement, unknown usage and genuine accounting failures. Raw content overflow reports `response_bytes_exceeded`; canonical overflow retains the domain category `synthesis_limit_exceeded`. Envelope overflow retains `unknown` rather than inventing content measurements.

Initial development runs corrected an oversized emoji padding fixture and an assertion that mistakenly assumed the shared synthetic contract already used L1-only totals. An earlier expanded selection inadvertently included legacy envelope-assessment tests; their shared fixture failed during the first four-page case because its Q&A capture was empty under this workspace's governance configuration. It did not reach its 200-page cases. That historical assessment was excluded from the final focused selection; it was not repaired or used as evidence here. No L2 scope was modified.

Relevant Python compilation passed using an external `/tmp` bytecode cache. `git diff --check` passed. Task-specific source diffs were reviewed against pre-edit copies where available; review confirmed conservative child-size planning still uses canonical bytes and actual rendered input still fails closed independently. Separate limited pre-commit review checked the touched code/tests/report for sensitive material, generated artifacts, unrelated edits and accidental contract changes. No dependency or Docker change required installation or image validation.

## D. Fingerprints and compatibility

New generation-contract digest:

```text
2ff2aff8f575ed99b23108dd5d10c2f7a73a55fb6cc7e073107e0597124c7290
```

The previous hardening digest `8e096a3658ee49379c09c60d8e21b46a2d5704756d318889d63e4ae1b4f03304` is rejected by `LaunchConfiguration.bounded()` before approval access. The prior `3da39a6b00a75a7f689a49e56a4dc3255576e0d16265a2d509f259f2d533e16f` packets and earlier packets are likewise incompatible. This includes previous first-attempt/final-authorization and same-day Attempt 2 launch packets, plus any configuration bound to the preceding hardening digest. Their audit evidence remains historical and was not altered.

The integration test inspects the actual runtime requests and rendered controls for matching byte limits and template version; profile digests bind the explicit byte settings. The generation digest is stable across offline composition. Existing launcher validation recomputes it on configuration validation; existing approval validation binds the full configuration digest. Changing the generation digest therefore invalidates the old configuration and its bound approval. RSA/authentication code was not changed.

A future separately authorized experiment needs a newly reviewed configuration containing this generation digest, resulting configuration digest, the new managed profile/template fingerprints and fresh authorization bound to that configuration. No such packet was generated, signed or consumed here. Neither previous approval nor old checkpoint compatibility is implied by passing tests.

## E. Safety and working tree

Additional live inference calls: **0**. Azure modifications: **0**. Governance/financial authority changes: **0**. RSA signing: **0**. Approval consumption: **0**. Staging/commits/pushes: **0 / 0 / 0**. Synthetic fake-provider calls and temporary test databases are the only executions/writes used for validation. No `.env`, historical audit artifacts or existing SQLite authority databases were changed. No Attempt 3 preparation or execution occurred.

Final `git status --short` and `git diff --stat` were inspected. The tree remains dirty on `master`, including the user's existing changes and untracked work. Tracked diff statistics include pre-existing work and omit untracked Foundry files; they are not a task-only change count.

## F. Next step

The corrected output-budget implementation is technically ready for separate review and authorization of an L1 Attempt 3. Existing packets are incompatible and must not be reused. Input admission, complete evidence/lineage preservation, canonical size and token truncation remain independent failure conditions: a larger byte allowance does not guarantee successful generation or a successful live experiment.
