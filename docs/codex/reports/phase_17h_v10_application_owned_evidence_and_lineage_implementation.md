# Phase 17H v10: application-owned evidence and lineage implementation

10 November 2026. **PASS — PHASE 17H V10 APPLICATION-OWNED EVIDENCE AND LINEAGE IMPLEMENTED; OFFLINE VERIFIED.**
This report distinguishes deterministic engineering from unobserved model compliance.
No operator preparation or live evaluation is performed or authorized.

## 1. Executive summary

One `stage-proposal/1` wire boundary now separates substantive model output from
canonical `stage-result/1`. The application assigns source mappings, atomic
immediate-child mappings, stage/origin identities and positional claim identities.
The model still selects support and writes substantive content. Invalid output
fails without reference repair, coverage filling, reordering, dropped claims or
extra inference. Canonical models, G2 and publication/retrieval/Q&A contracts are
preserved. An additive receipt and raw record share the existing fenced atomic
checkpoint manifest. No database migration or checkpoint schema change is needed.

## 2. Starting repository state

Actual branch `master`, HEAD `6e0319e29984ad019edced0e076b3b0a4ae8c007` match the
request. Entry status is 16 modified tracked files and 45 untracked files, with
no staged changes. These include substantial inherited v8/v9 engineering and
historical documentation. They are not attributed wholesale to v10.

Before active source changes, the actual v9 generation digest was recomputed and
matched `f270aa81cbd5764d2b4739bf3ac3692653b1fe4c8ffbd67860e642137cb2579d`.
All 15 inventory/1 sources were frozen byte-for-byte under
`tests/fixtures/digestion_contracts/v9_sources/`; the managed renderer is also
available as `managed_prompt9.py.txt`. `managed_prompt9_inventory.json` records
the exact initial source inventory and preserved generation fingerprint. Initial
Git status/diff and a file-hash inventory were retained under `/tmp` for delta
review. Real operator authorities, approval markers and signing keys were not
opened or inventoried by this task.

## 3. Post-v9 ADR review

The mandatory AGENTS, post-v9 report/assessment, v9 readiness report, v7/v8 live
failure reports, current Foundry runbook and historical fixtures were read.
Implementation inspection traced request objects, deterministic identities,
provider audit hashes, governance/admission, object storage, intent registration,
lease fencing, checkpoint commitment, recovery and publication graph reopening.
The already completed RAPTOR/wdoc/LangChain/AI Document Assistant investigation
was used as design evidence, not repeated. No external package or framework was
introduced. The old ADR and live reports remain historical and unchanged.

## 4. Final request/table/response binding

A reference manifest commits to the complete canonical StageRequest hash,
`stage-decoder/1`, sorted authorized source UUIDs and ordered complete child pairs.
The request includes stage/profile/path, exact source EvidenceRefs/spans and
accepted child ObjectRefs/results/inherited summaries. The proposal's singleton
request_binding is checked exactly. It is a consistency value, not authentication.

An application-created immutable provider record binds that request/table digest
to the exact returned bytes, plan ObjectRef, job/step, attempt/fence, managed
configuration and generation hashes. A receipt binds the record to the exact
canonical checkpoint and result hash. Merely supplying an E key, response hash,
model-generated binding or orphan receipt cannot establish acceptance.

## 5. Existing audit/checkpoint mechanisms reused

The implementation reuses LocalObjectStore atomic link-if-absent/fsync publication,
scoped hashed ObjectRefs, IntentStore fencing, JobLedger attempts and multi-object
manifests, SQLite synchronous FULL commitment and dependent outbox activation.
The existing Foundry raw provider capture/usage audit remains intact; the new
record includes the identical request-audit hash for direct comparison. Canonical
checkpoint identity remains content-derived through the existing codec.

## 6. Receipt persistence and recovery policy

The [new decision record](../../adr/phase_17h_v10_generation_wire_receipt_decision.md)
specifies the full design and all fourteen required failure/replay scenarios.
Execution settles known provider usage before raw capture and decoding, then
performs strict construction, G2 and complete inherited G1 admission, writes
checkpoint/receipt, verifies the association and atomically commits three refs:
checkpoint, receipt, raw record. All three are retained by the existing manifest
object registry. No dependent is activated before that commit.

On restart, child consumption and publication reconstruct exact requests/tables,
verify the original successful attempt/fence and immutable hashes, decode again,
compare canonical bytes and recheck G2/parents/inheritance/G1. Repeated resumes
follow ledger-owned reuse edges, requiring identical manifests at every hop.
Duplicate successful delivery/commit is idempotent; stale fences cannot commit.

Interrupted uncommitted work is conservatively failed under the existing
one-attempt L1 policy. Raw/checkpoint/receipt orphans do not authorize recovery
inference or automatic adoption. A settled call can remain without an accepted
checkpoint after a crash. This preserves zero paid retries; it does not promise
exactly-once provider delivery or automatic completion of interrupted work.

## 7. Generation-wire schema

`stage-proposal/1` has required version, request_binding, outcome, ordered claims,
open_questions and limitations. Claims carry text, kind, status, subject, stance,
evidence_refs, contradicting_evidence_refs, qualifications and child_refs.
Qualifications carry text and evidence_refs. There are no model-generated
canonical stage, origin or claim IDs, or independently chosen child components.
Object properties decrease from 22 to 17, with three object shapes rather than
four. The historical canonical schema helper remains for historical compatibility;
active rendering and decoding use only the one wire schema.

The decoder checks exact object keys and scalar types, unique JSON keys, raw byte
limit, versions/binding, claim/annotation/reference bounds, exact membership and
within-array uniqueness before construction. It does not rely on permissive
Pydantic coercion. Provider schemas use only the existing converter's string enums,
local references, null and anyOf constructs. Unsupported collection-bound keywords
are not added; equivalent local checks are mandatory in every mode.

## 8. Source-reference mapping

E keys enumerate the sorted unique v9 authority set: current SourcePiece evidence
IDs plus immediate-child claims' direct supporting and contradicting IDs.
Qualification-only inherited references never create new direct authority.
CONTROL includes the trusted E-to-original-UUID mapping. Request-specific enums
constrain all three selection positions, including qualification evidence. The v10 wire authority bound is 256 in every transport mode; a larger non-strict max_evidence setting cannot enlarge this wire bound. Empty
authority uses null schema items; only empty arrays survive local string/membership
validation. Syntax alone never authorizes a key. Source authorization remains
independent of the aliases and is rechecked by G2/EvidenceIndex.

## 9. Atomic child-pair mapping

C keys enumerate actual immediate children in immutable plan-child order, followed
by each accepted child's stored claim order. One C key resolves to a full
(stage_id, claim_id) pair. Grandchild substitution and cross-child component mixing
cannot be expressed as an authorized atomic selection. The model must still
select actual supporting child claims; omitted coverage fails unchanged G2.
Compact child views retain substantive fields, direct E selections, qualifications,
questions, limitations and inherited counts. Qualification sources outside the
direct table remain identified as inherited evidence, without gaining authority.

## 10. Application-owned identities

Claim order is preserved exactly. Every canonical claim receives
`stable_id(str(request.stage_id), str(position))`; current originating_stage and
result stage_id come from the request. The established stable_id function is
unchanged and included in inventory/2 through documents/models.py. Empty-analysis,
explicit unavailability/limitations, claim bounds and semantic kind/status rules
remain independently enforced. Historical identities are never rewritten.

## 11. Canonical constructor and consumer compatibility

The constructor expands only explicit valid selections into original UUIDs and
complete ClaimLinks, then builds a fresh StageResult. Managed analyze() continues
returning canonical bytes to its application interface. A trusted per-call capture
callback persists raw evidence before construction; the durable handler requires
that record before accepting a v10 result. The older single-analysis harness also
decodes active wire output and retains a separate immutable proposal audit before
canonical validation. No harness is invoked live or prepared for an operator.

`stage-result/1`, `synthesis-checkpoint/1`, ChildInput, digest storage, publication,
retrieval and grounded Q&A types remain unchanged. V10 step manifest arity is
additively three rather than one; generic job API tuple types are unchanged, but
external consumers assuming a single ref must recognize this version-specific
convention. Published citation authority remains original scoped EvidenceRef,
including extraction/block offsets, lines and excerpts. Aliases are not published
as authoritative citation IDs.

## 12. Preserved G1/G2 invariants

Validation.py is byte-identical to the initial v9 source. G2 still owns canonical
identity, source authority, immediate-pair membership, duplicate rejection, fact
support and coverage checks. Complete inherited child admission remains required
before commitment and after reopening. Wire size cannot substitute for canonical
or escaped child size. Input 24,800, context 28,000, output 3,000, complete child
7,000 and L1 raw/canonical 10,000/HTTP 26,192 limits remain. The planner adds a
conservative 64 bytes per source to v10 analysis accounting; reduction retains
the full canonical child allocation. Rendered requests are independently admitted
before any provider call. L1 remains chunk/first reducer/root/Q&A, at most four,
one concurrent, at least 61-second starts, no paid retries or fallback.

## 13. Production and composition files

Production application changes are managed.py (wire rendering, capture and canonical
return), wire.py (mapping/schema/strict construction), receipts.py (association
models/reopening), workflow.py (additive manifests and graph verification), and
sizing.py (conservative v10 source reserve). No provider transport, strict converter,
G2 validator, security/governance authority, database schema or publication model
is changed. Evaluation composition changes are foundry_l1.py (inventory/2),
foundry_preflight.py and workloads.py (wire-aware synthetic providers), and
foundry_single_call.py (wire decoding/raw proposal audit for the existing consumer).

## 14. Permanent tests and file manifest

There are 389 new unique permanent cases: 268 decoder/authority/identity cases,
46 complete sizing cases, 57 workflow/receipt/recovery cases and 18 generation/
historical compatibility cases. Existing canonical-output characterizations are
explicitly routed through the exact frozen v9 generator with current G1/G2,
worker, storage and publication. Their historical expectations are preserved.
Active v10 is separately tested through actual production interfaces; it is not
made to accept canonical model output to satisfy old tests.

Task-owned modified/new files, including this report, are listed below. The frozen source directory's
15 entries preserve historical code, not a second active implementation. The
manifest distinguishes v10 deltas from inherited working-tree changes.

- `README.md`
- `docs/evaluation/phase_17h_foundry_validation.md`
- `documents/digestion/managed.py`
- `documents/digestion/sizing.py`
- `documents/digestion/workflow.py`
- `tests/fixtures/digestion_contracts/README.md`
- `docs/codex/reports/phase_17h_v10_application_owned_evidence_and_lineage_implementation.md`
- `tests/conftest.py`
- `tests/integration/test_attempt3_serialization.py`
- `tests/integration/test_claim_stage_identity_workflow.py`
- `tests/integration/test_final_offline_azure_compatibility.py`
- `tests/integration/test_foundry_l1_launcher.py`
- `tests/integration/test_foundry_offline_workflow.py`
- `tests/integration/test_governed_digestion.py`
- `tests/integration/test_http_cleanup_governance.py`
- `tests/integration/test_live_failure_observability.py`
- `tests/integration/test_managed_digestion.py`
- `tests/integration/test_managed_prompt7_contract.py`
- `tests/integration/test_output_limit_hardening.py`
- `tests/integration/test_phase17h_two_chunk.py`
- `tests/integration/test_phase17hl_offline_e2e.py`
- `tests/integration/test_reducer_sizing_offline_workflow.py`
- `tests/integration/test_single_call_harness.py`
- `tests/integration/test_validation_diagnostics.py`
- `tests/performance/foundry_l1.py`
- `tests/performance/foundry_preflight.py`
- `tests/performance/foundry_single_call.py`
- `tests/performance/workloads.py`
- `tests/unit/documents/test_claim_stage_identity.py`
- `tests/unit/documents/test_managed_inference.py`
- `tests/unit/documents/test_managed_sizing.py`
- `tests/unit/documents/test_two_layer_output.py`
- `docs/adr/phase_17h_v10_generation_wire_receipt_decision.md`
- `docs/codex/prompts/phase_17h_v10_application_owned_evidence_and_lineage.md`
- `documents/digestion/receipts.py`
- `documents/digestion/wire.py`
- `tests/fixtures/digestion_contracts/managed_prompt10.json`
- `tests/fixtures/digestion_contracts/managed_prompt9.py.txt`
- `tests/fixtures/digestion_contracts/managed_prompt9_inventory.json`
- `tests/fixtures/digestion_contracts/v9_sources/documents/digestion/diagnostics.py.txt`
- `tests/fixtures/digestion_contracts/v9_sources/documents/digestion/managed.py.txt`
- `tests/fixtures/digestion_contracts/v9_sources/documents/digestion/models.py.txt`
- `tests/fixtures/digestion_contracts/v9_sources/documents/digestion/planning.py.txt`
- `tests/fixtures/digestion_contracts/v9_sources/documents/digestion/sizing.py.txt`
- `tests/fixtures/digestion_contracts/v9_sources/documents/digestion/validation.py.txt`
- `tests/fixtures/digestion_contracts/v9_sources/documents/digestion/workflow.py.txt`
- `tests/fixtures/digestion_contracts/v9_sources/documents/publication/analysis.py.txt`
- `tests/fixtures/digestion_contracts/v9_sources/llm/azure_schema.py.txt`
- `tests/fixtures/digestion_contracts/v9_sources/llm/bounded_http.py.txt`
- `tests/fixtures/digestion_contracts/v9_sources/llm/openai_compatible.py.txt`
- `tests/fixtures/digestion_contracts/v9_sources/llm/structured.py.txt`
- `tests/fixtures/digestion_contracts/v9_sources/tests/performance/fixtures.py.txt`
- `tests/fixtures/digestion_contracts/v9_sources/tests/performance/foundry_preflight.py.txt`
- `tests/fixtures/digestion_contracts/v9_sources/tests/performance/foundry_recalibration.py.txt`
- `tests/generation_wire_fixtures.py`
- `tests/historical_managed.py`
- `tests/integration/test_direct_child_lineage_workflow.py`
- `tests/integration/test_generation_wire_v10.py`
- `tests/integration/test_managed_prompt10_contract.py`
- `tests/integration/test_managed_prompt8_contract.py`
- `tests/integration/test_managed_prompt9_contract.py`
- `tests/integration/test_source_identity_workflow.py`
- `tests/unit/documents/test_direct_child_lineage.py`
- `tests/unit/documents/test_generation_wire_v10_decoder.py`
- `tests/unit/documents/test_generation_wire_v10_sizing.py`
- `tests/unit/documents/test_managed_prompt9_sizing.py`
- `tests/unit/documents/test_source_reference_schema.py`

## 15. Historical compatibility

Original v5–v9 fingerprint JSON and earlier managed source fixtures are unchanged.
Historical results still validate under their preserved request contracts. New
settings, current rendering and launch bindings refuse historical versions; old
approvals cannot become v10 authority. Historical checkpoint/result/source/claim/
lineage values are not rewritten. Existing settlement/replay tests use disposable
fixtures; no real historical financial or approval state is accessed or modified.
The v9 15-source inventory can be independently recomputed from preserved bytes.

## 16. New generation fingerprint

`managed-prompt/10`, generation-inventory/2 (25 sources):

```text
e5fb249cc9b166b5e438f1534eb855fa5ab7531e08aa09314c110a1905327ebd
```

`managed_prompt10.json` pins every source SHA-256 and exact representative
request, generation envelope and actual HTTP payload hashes. Inventory/2 expands
the old 15-file list explicitly and tests the full new digest. Every new imported
mapping/decoder/receipt helper is covered, including identity and durable binding
infrastructure. Existing approval schemas are unchanged; the fresh complete digest
changes their configuration binding and makes old execution fail closed.

## 17. V9 versus v10 serialization

The same native four-page extraction and eight-claim substantive witness are
constructed under both preserved v9 and current v10. IDs/configuration differ by
contract; substantive fields and source spans are the same. Values below are
actual UTF-8 system/data bytes, compact ASCII schema/envelope/canonical bytes and
real provider-builder requests JSON serialization. They are not model token billing.
The intermediate profile uses the same representative reducer request as structural.

| Profile | System v9/v10 | Data v9/v10 | Schema v9/v10 | Strict schema v9/v10 | Envelope v9/v10 | HTTP requests JSON v9/v10 | Output v9/v10 | Canonical v9/v10 | Complete child v9/v10 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| chunk | 4159/2937 | 2049/1917 | 3017/2423 | 2038/1715 | 9439/7485 | 8907/7199 | 3317/1893 | 3317/3317 | 5333/5333 |
| intermediate | 4991/2993 | 3968/2056 | 3017/2474 | 2038/1766 | 12564/7959 | 12032/7682 | 4126/1925 | 4126/4126 | 6206/6206 |
| structural | 5000/3002 | 3968/2056 | 3017/2474 | 2038/1766 | 12573/7968 | 12041/7691 | 4126/1925 | 4126/4126 | 6206/6206 |
| root | 5003/3005 | 4777/2056 | 3017/2474 | 2038/1766 | 13449/7971 | 12917/7694 | 4126/1925 | 4126/4126 | 6206/6206 |

Chunk envelope decreases 1,954 bytes (20.7%); root decreases 5,478 (40.7%).
Root wire output decreases 2,201 bytes (53.3%). Canonical result/complete child
storage has zero byte growth for the equivalent witness. Complete conservative
context estimates, including 200 overhead/safety and 3,000 output, are chunk
12,639 -> 10,685; intermediate 15,764 -> 11,159; structural 15,773 -> 11,168;
root 16,649 -> 11,171. These estimates use the existing one-byte-per-estimated-token
policy; they do not establish actual tokenizer counts, latency or financial savings.

Reconstructed reference-manifest diagnostic size is 296 bytes for the four-source
chunk and 935 for eight-pair reducers. These are side-band reconstruction sizes,
not another full manifest serialized into context or persisted in the receipt.
The actual model-facing E mapping/C key lists and binding are included in the
system measurements above. Structural path overhead is zero in this baseline;
separate permanent tests cover empty, escaped and Unicode paths at exact limits.
The one-claim production-builder capture stores 1,248-byte receipts and
1,583–1,616-byte raw records, in addition to 1,256–1,658-byte checkpoints.
This is additional bounded audit storage; canonical storage itself is unchanged.

The old review measured 848 bytes of source/identity/pair copying instructions.
Those canonical UUID-copying duties, positional candidate arrays and pair assembly
instructions are removed. Replacement selection/binding guidance and compact
substantive child material are included in the measured net sizes. The model
still copies a consistency binding and must select semantically correct keys.

Sizing regressions measure all profiles at 0/1/4/128/129/256 sources (257 rejected),
one/two-child reductions and exact ASCII/escaped/Unicode acceptance and +1 rejection.
The 256-source schema capacity does not promise G1 admission; large fully serialized
requests are rejected before inference. No capacity is automatically enlarged.


Additional production-builder diagnostics measure all 24 profile/cardinality
combinations below using distinct one-character native source spans and, for
reducers, one canonical child. These differ from the four-page comparison above.
HTTP sizes are actual default requests JSON serialization through an injected
local transport. Rejected rows are sizing-only diagnostics; production admission
rejects them before inference. Empty chunk material is invalid analysis input.

| Profile / sources | System | Data | Schema / strict | Envelope | HTTP JSON | Admitted |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| chunk/0 | 2762 | 91 | 2392 / 1684 | 5345 | 5054 | No |
| chunk/1 | 2805 | 170 | 2408 / 1700 | 5505 | 5216 | Yes |
| chunk/4 | 2937 | 410 | 2423 / 1715 | 5958 | 5672 | Yes |
| chunk/128 | 8541 | 10478 | 3191 / 2483 | 25126 | 24964 | No |
| chunk/129 | 8587 | 10560 | 3237 / 2529 | 25322 | 25165 | No |
| chunk/256 | 14429 | 20974 | 4126 / 3418 | 45261 | 45231 | No |
| intermediate/0 | 2783 | 504 | 2408 / 1700 | 5851 | 5562 | Yes |
| intermediate/1 | 2826 | 508 | 2424 / 1716 | 5920 | 5633 | Yes |
| intermediate/4 | 2958 | 523 | 2439 / 1731 | 6100 | 5816 | Yes |
| intermediate/128 | 8562 | 1291 | 3207 / 2499 | 13984 | 13824 | No |
| intermediate/129 | 8608 | 1298 | 3253 / 2545 | 14089 | 13934 | No |
| intermediate/256 | 14450 | 2187 | 4142 / 3434 | 22471 | 22443 | No |
| structural/0 | 2792 | 504 | 2408 / 1700 | 5860 | 5571 | Yes |
| structural/1 | 2835 | 508 | 2424 / 1716 | 5929 | 5642 | Yes |
| structural/4 | 2967 | 523 | 2439 / 1731 | 6109 | 5825 | Yes |
| structural/128 | 8571 | 1291 | 3207 / 2499 | 13993 | 13833 | No |
| structural/129 | 8617 | 1298 | 3253 / 2545 | 14098 | 13943 | No |
| structural/256 | 14459 | 2187 | 4142 / 3434 | 22480 | 22452 | No |
| root/0 | 2795 | 504 | 2408 / 1700 | 5863 | 5574 | Yes |
| root/1 | 2838 | 508 | 2424 / 1716 | 5932 | 5645 | Yes |
| root/4 | 2970 | 523 | 2439 / 1731 | 6112 | 5828 | Yes |
| root/128 | 8574 | 1291 | 3207 / 2499 | 13996 | 13836 | No |
| root/129 | 8620 | 1298 | 3253 / 2545 | 14101 | 13946 | No |
| root/256 | 14462 | 2187 | 4142 / 3434 | 22483 | 22455 | No |

A separate adversarial inherited-qualification diagnostic found 55 valid shapes
within the approved eight-claim/eight-annotation profile. All rendered inside
the existing reservation; the minimum measured margin was 1,900 bytes. Both
supplemental diagnostics reported zero network attempts. Their counts are not
added to pytest totals or represented as model-quality observations.

## 18. Offline validation

The final complete run passed **2,595 tests**: **1,815 unit and 780 integration**,
with **zero failures, errors or skips and zero network attempts**, in **729.33
seconds**. JUnit independently confirms every count. All **389 new permanent
cases** are included in that total, rather than added to it. A defined historical
contract selection of **72 unique cases** comprises the v7/v8/v9 contract modules
and fifteen new v5–v9 refusal/readability cases; the suite additionally exercises
broader frozen-generation, canonical G1/G2 and publication characterizations.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  PYTHONPATH=.:/tmp/phase17h-g1-g2 python -m pytest \
  -p offline_guard -p no:cacheprovider \
  --basetemp=/tmp/phase17h-v10-offline/full-verified \
  --junitxml=/tmp/phase17h-v10-offline/full-verified.xml \
  -o junit_family=xunit1 -q
```

The existing pre-collection socket/DNS denial plugin runs before application
imports. Application settings are isolated and all security, approval, financial,
object and publication stores are disposable synthetic stores outside the real
operator environment. One pre-existing OpenTelemetry SelectableGroups deprecation
warning is reported by the real local Chroma integration test.

| Final applicable check | Actual result |
| --- | --- |
| Complete offline pytest | 2,595 passed; 0 failed/errors/skipped; 0 network attempts |
| Stable focused wire/schema/sizing/receipt/contract run | 388 passed in 179.02 s; 0 network attempts; overlaps full suite |
| Final decoder plus historical strict-schema check | 349 passed in 8.77 s, including the subsequently added active-schema refusal case; 0 network attempts; overlaps full suite |
| Focused recovery/compatibility/concurrency/launcher selection | 130 passed in 148.04 s; 0 network attempts; overlaps full suite |
| Ruff critical E9,F63,F7,F82 | All digestion/jobs/publication, llm and tests pass |
| Default Ruff | Eight new source/test/helper modules pass |
| Applicable Ruff format check | Eight new source/test/helper modules already formatted |
| Scoped mypy | No issues in eleven changed/new source/test files |
| Whole repository compileall | Exit 0, external bytecode cache; no ownership changes |
| Docker Compose config --quiet | Exit 0; no service build/start or Kubernetes operation |
| git diff --check | Exit 0 |
| Current generation/source inventory comparison | All 25 source hashes match the v10 fixture |
| Preservation review | 37 critical existing sources unchanged; no unrelated historical report changes |
| Task-delta secret/key and relative-link review | Zero findings / zero broken relative links |

Mypy uses the already installed executable from the local iberian_shakti Python
environment with the project interpreter selected through --python-executable,
--follow-imports=skip, --ignore-missing-imports and --explicit-package-bases.
This is scoped checking, not a claim of unrestricted whole-repository typing or
formatting. No dependency or model is installed. Docker build is not applicable
to these Python/schema changes; no dependency or container configuration changes.

Exploratory runs exposed stale canonical-generation assumptions, a historical
schema monkeypatch targeting the wrong module, missing fixture re-exports, old
v5/v6 JSON files without an aggregate digest field, a duplicate test module name
and a missing temporary parent directory. These were corrected without changing
historical acceptance expectations, security/provenance validation or G2. Runs
interrupted during setup or source review are not represented as passes. The
final complete run above uses the frozen final source and determines disposition.
Logs, JUnit, sizing diagnostics and bytecode remain under /tmp outside Git.

## 19. Crash/replay/recovery validation

Fault injection covers before/after immutable raw capture, decoder interruption,
before/during/after receipt persistence, before/after atomic manifest commitment,
reopening, idempotent repeated commitment, stale fences, duplicate delivery,
three successive checkpoint resumes, orphan retention and corrupt request/table/
raw/canonical/generation/audit/artifact hashes. Known provider usage is settled
before rejection. Invalid chunk/first reducer/root proposals prevent downstream
calls and publication; prior accepted checkpoints remain unchanged.

## 20. Security and governance review

Aliases derive only from already authorized immutable inputs. Model output cannot
supply scope, original UUID authority, plan/stage identity or pair components.
Request/table consistency is distinct from authentication. IntentStore and ledger
checks retain scope, cancellation, current lease and fence. Publication authorization,
RBAC, principal/owner/tenant boundaries, financial reservations/settlement, admission,
approval signatures and replay consumption are unchanged. No real authorities,
credentials, private keys, policies, financial rows or replay markers are modified.
Synthetic signing/authentication cases in disposable test stores are not operator
RSA signing or Microsoft Entra authentication.

## 21. Remaining model-compliance risks

Authorized key selection can still be semantically wrong. Structural acceptance
cannot establish entailment, citation relevance, omission/qualification quality or
safe interpretation of conflicting claims. The model can refuse, truncate, omit
coverage or return an incorrect binding. Such outputs fail rather than trigger
repair/retry/fallback. Exact live completion sufficiency and representative semantic
quality still require separately authorized observation and independent human review.
The standard Ollama model manifest directory is empty; no suitable installed local
instruction model was verified. Optional comparison is skipped without download,
service start, inference or infrastructure change.

## 22. Azure schema compatibility limitations

The unchanged azure-strict/1 converter accepts the exact wire composition offline.
The actual bounded HTTP builder carries it under strict=true. No Azure request is
made, so exact deployment schema acceptance, refusal/truncation behavior, array
selection compliance and actual billed usage remain unverified. Provider schema
constraints do not replace local uniqueness, collection bounds, coverage or G2.
No claim of Azure compliance or financial improvement follows from these tests.

## 23. Separate review and next operator phase

A separate critical pass reviewed hidden repair, table contamination/order, IDs,
immediate lineage, canonical expansion/G1, receipt commit ordering, recovery,
generation inventory, historical execution, provider neutrality, audit integrity,
usage/accounting, complexity and semantic attribution risks. It found and corrected
one-hop-only checkpoint reuse: verification now follows all ledger reuse edges.
It also separated collection resource limits from table membership, so empty or
singleton authority rejects foreign/duplicate selections as evidence errors. It
retained the canonical managed analyze() interface rather than exposing
wire bytes to its consumers. Tests exercise repeated resumes and canonical output.
This is a separate Codex review pass, not a claim of external human/model review.

Pre-commit review checks the task delta for keys/credentials, real runtime paths,
logs/debug/generated artifacts, dead code, dependencies, unrelated edits, stale
claims, broken documentation links and API drift. Historical reports and approvals
are preserved; temporary diagnostics/JUnit/bytecode stores stay outside Git.
One accidental empty placeholder outside the workspace was removed through the
execution approval mechanism; it is not a task artifact. No dependency is installed.

After manual code and report review, a separate operator-preparation phase is
technically reasonable for this exact v10 fingerprint. It must verify current
capability/authorities/financial headroom and create fresh independently authorized
configuration/signing/execution bindings. Do not reuse approvals or treat synthetic
success as spend authority. Adaptive digestion/call-count optimization remains a
separate planning phase; the controlled L1 topology is unchanged.

## 24. Final Git status

Final branch is master at unchanged HEAD
`6e0319e29984ad019edced0e076b3b0a4ae8c007`. `git status --short -uall` records
**32 modified tracked files and 74 untracked files**, compared with 16/45 at
entry. The task-owned manifest above has **67 modified/new files**; remaining
status entries are inherited work, including the unchanged pre-existing
managed_prompt7_sizing.py modification. No staged changes exist.

Final `git diff --stat` reports:

```text
32 files changed, 666 insertions(+), 202 deletions(-)
```

This tracked statistic includes inherited v8/v9 work and excludes untracked
artifacts. It is not a count of only v10 additions. `git diff --cached --stat`
is empty. No staging, commit, push, reset, rebase or tag operation occurred.
Git history, real approvals and remote state are unchanged. All implementation
work remains available for user review. No next operator phase has been started.

Git staging: **NO**. Git commit: **NO**. Git push: **NO**.
Azure inference: **NO**. RSA signing: **NO**. Approval consumption: **NO**.
