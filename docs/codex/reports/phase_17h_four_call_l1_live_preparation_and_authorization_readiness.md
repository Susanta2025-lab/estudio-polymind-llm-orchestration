# Phase 17H — Four-Call L1 Live Preparation and Authorization Readiness

Assessment date: 2026-11-02. Repository HEAD: `f2a60fa`. Evidence is the **current
working tree**, including the existing uncommitted G1/G2 changes, rather than HEAD
alone. Scope: offline assessment and documentation only.

## 1. Executive summary

**Engineering readiness: GO for preparing a fresh four-call L1 evaluation.** No
application, test, configuration or launcher code change is demonstrated necessary
before operator preparation. The corrected sizing policy is explicitly active
in the L1 composition, a freshly generated plan has exactly one chunk and two
dependent reducers, and the targeted current offline integration passes through
durable digestion, publication, retrieval, grounded Q&A and settlement.

**Execution authorization: NOT AUTHORIZED.** Current authorized spend from this
task is zero. No launchable operator configuration, signature, reservation or
execution permission was produced. Fresh commercial/capacity evidence,
authentication, existing-authority checks and independent approval remain pending.

There is a concrete local packaging issue: the inspected embedding cache contains
the required model and loads successfully, but its eleven files are symlinks.
The launcher forbids symlinks in its approved embedding directory. **That cache
path is BLOCKED for direct launcher use.** Operator preparation must select an
already compliant directory or materialize those cached files as regular files,
then verify and pin the tree hash. This requires no model download or application
change. No private approved embedding directory was inspected, so this finding
does not establish that every existing operator model directory is unsuitable.

Three selected tests passed in **2.36 seconds**, with zero observed network
attempts. Two independently generated plans matched exactly. An additional
offline probe loaded the actual cached model on CPU and verified scratch local
Chroma write/query/inventory and generation/document filtering. These are bounded
technical checks, not live hierarchical acceptance or semantic certification.
**Phase 17H remains PARTIAL.**

### Evidence boundaries

- **PASS / current source:** inspected implementation or public configuration.
- **PASS / executed offline:** a check run during this task, with its limits stated.
- **Historical:** findings attributed to an earlier report, not freshly recovered
  from private evidence.
- **PENDING:** requires operator verification, final configuration or authorization.
- **BLOCKED:** a demonstrated incompatibility prevents the specified use.

The three required reports were reviewed: [hierarchical readiness assessment](phase_17h_hierarchical_digestion_readiness_assessment.md),
[G1/G2 hardening](phase_17h_g1_g2_offline_engineering_and_integration_hardening.md),
and [Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md).
The first report's G1/G2 gaps precede the corrective task. Attempt 6 establishes
historical single-analysis acceptance only; its consumed approval and retained
output were neither opened nor reused here.

## 2. Current implementation and configuration verification

| Finding | Classification and evidence |
| --- | --- |
| Corrected L1 sizing enabled | **PASS / source and fresh plan.** [foundry_preflight.execute](../../../tests/performance/foundry_preflight.py) explicitly selects `child_input_bytes=7000` for L1, strict capability, `managed-generation/2`, `managed-prompt/4`, four stage profiles at 24,800 input/3,000 output, and independent 10,000-byte raw/canonical result limits. |
| Complete envelope admission | **PASS / source.** [managed.py](../../../documents/digestion/managed.py) measures the trusted instructions/schema and escaped data envelope. [sizing.py](../../../documents/digestion/sizing.py) budgets escaped child results, every required claim link, evidence and wrappers. [planning.py](../../../documents/digestion/planning.py) admits bounded chunks/fan-in. |
| Output admission before checkpoint acceptance | **PASS / source.** [validation.py](../../../documents/digestion/validation.py) checks raw/canonical bounds and result contribution plus 1,024 reserved wrapper bytes. [workflow.py](../../../documents/digestion/workflow.py) also measures actual inherited metadata with a conservative reference before writing a checkpoint. No evidence truncation or repair is introduced. |
| Managed contract compatibility | **PASS / source and selected integration.** The provider-neutral structured boundary remains; three digestion stages use `azure-strict/1` and the unchanged `stage-result/1` application contract. Model role routing remains within provider infrastructure. |
| Strict validation and provenance | **PASS / source and selected integration.** Stage/kind and deterministic claim identity, evidence allowlists/source coordinates, full leaf coverage, every child claim link, canonical serialization and final root-to-leaf reconstruction remain enforced. |
| Durable persistence and recovery | **PASS / source and selected integration.** Immutable checkpoints bind plan and parents; finalization reopens/revalidates them and commits digest plus coverage through fenced worker manifests. Accepted checkpoint reuse is verified without new fake calls or settlements. |
| Publication/retrieval bridge | **PASS / source and selected integration.** COMPLETE-only accepted output is reconstructed before publication; canonical original text is published separately from generated annotations, then explicitly activated and pinned for retrieval. |
| Fresh source/configuration compatibility | **PASS / executed offline** for the unsigned synthetic-scope candidate below. **PENDING** for the actual operator scope, final complete configuration digest and approval. |

The current [L1 launcher](../../../tests/performance/foundry_l1.py) delegates its
execution composition to `foundry_preflight.execute(..., runtime=...)`; the L1
sizing choice therefore applies to both offline and live composition. Its
`LaunchConfiguration` requires four attempts and rejects incompatible ceilings,
prices, deployment isolation, timing and source-generation bindings. No
historical `LaunchConfiguration` was loaded.

The schema boundary remains two-layered: Azure strict schema is requested for
digestion, the adapter validates completion/envelope/model/usage, and the
application validates the returned domain object and provenance. Provider
completion alone never establishes application acceptance. Q&A deliberately
retains its separate JSON-object contract with trusted output schema and strict
application citation validation; it does not use the digestion strict schema.
The digestion HTTP response envelope is bounded at 26,192 bytes independently
of its 10,000-byte content allowance. Q&A retains a 12,000-byte content limit;
both paths retain the 3,000-token inclusive output ceiling and bounded deadlines.

Recovery is the existing local durable outbox/relay/reconciliation workflow,
with lease fences and compatible checkpoint reuse. It does not guarantee
exactly-once paid execution after a crash. For the live evaluation, an ambiguous
or started-but-unsettled call requires reconciliation and a new operator decision,
not automatic resume/recomputation. No distributed recovery claim is made.

## 3. Exact four-call workflow, fresh bindings and expected artifacts

The source fixture remains `phase17h-pdf/1`, seed 1708, four physical PDF pages,
six authored lines per page and the existing page-three untrusted injection text.
It is newly generated from [fixtures.py](../../../tests/performance/fixtures.py),
not a historical response/checkpoint. `document_id=UUID(int=4)` and the fixture's
fixed timestamps are part of the existing composition. Live scope comes from the
verified principal; document version/extraction/evidence identities consequently
must be regenerated under that scope.

| Call | Managed stage and dependency | Required accepted result |
| --- | --- | --- |
| 1 | `chunk`: one analysis containing all four source pieces | Validated `StageResult`, full authorized source coverage, immutable leaf checkpoint. |
| 2 | `structural`: the fallback structural group, dependent on call 1's committed checkpoint | Reduction links every child claim; inherited evidence/qualifications retained in accepted artifacts. |
| 3 | `root`: level-two document reducer, dependent on call 2's committed checkpoint | Validated root checkpoint, followed by local finalization/reopening into COMPLETE digest and coverage. |
| Local bridge | No inference: successful digest persistence, authorized publication plan/prepare/activate, replica load/readiness, selected-document retrieval and canonical citation resolution | Active immutable publication generation with source text records and separately labelled derived annotations. |
| 4 | Grounded Q&A after the bridge: “What is the first inspection procedure on physical page 1?” | Validated answer/citation IDs, selected source/version and physical page support, settled usage and independent review packet. |

The durable job itself contains **five local steps**: plan anchor, three model
stages and final digest validation. Q&A is downstream of that job. Extraction,
plan creation, digest finalization, CPU embedding, publication and retrieval add
no Azure inference calls. The separate `intermediate` profile is configured but
not selected by this one-chunk plan.

**Exactly four calls is the successful evaluation target and hard maximum, not
a requirement to continue after failure.** A failed earlier stage stops sooner.
`DocumentAnalysis` may return a local insufficient-evidence response without
inference if retrieval yields no citations; the harness may also record a valid
abstention as COMPLETE. Consequently launch exit/status alone is insufficient:
acceptance must count four completed calls with the expected stage sequence and
check that the answerable question has the correct page-one finding and citation.
Do not manufacture a fourth call to fill a short run.

### Newly generated unsigned plan

An inert provider exposing the configured deployment identity, whose `execute`
method always raises, was used solely to bind the current managed profile. Two
fresh isolated object stores received newly generated/extracted fixture material
under a new deterministic **synthetic assessment scope**. Both plan objects and
references matched exactly; all four evidence pieces resolved to their canonical
text and reproduced the complete source text without loss. No job, security or
financial authority was opened by this plan-only probe.

| Review binding | Fresh value |
| --- | --- |
| PDF source SHA-256 | `1be99e19a56040fb55c74682a19f874d4d4573f18d9f52a9a7ae19c8158ea92d` |
| PDF bytes / pages / evidence pieces | 3,537 / 4 / 4 |
| Synthetic-scope extraction SHA-256 | `841e5c121e0ab3ee05c9bd4a5cb9f5a4551b1415fb6b8cc26906f10ddadb1b22` |
| Synthetic-scope plan SHA-256/fingerprint | `8bc0776f9f5ebd11491d6cac5233a0e7f380b92a5fb19aeb96be132a9bf7bde4` |
| Bound planning profile | `e11dc86cd3247fb45cb263b403301990ca53c74c40d858fba2de28740c286e6b` |
| Managed inference configuration | `6630c6203d1638633fae7c5edfdca866917f745d89aefb34d5bc0824ab0f2f43` |
| Current authoritative generation source digest | `00bf895290e1da2fb81372ff1ea921d8d7f464ea14f41110f54313d0423ad904` |
| Application generation schema | `a051949799a312d1aa15a5959bbe7d558265cfc38f6ce992eb97fbdbdff212ab` |
| Azure strict provider schema | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` |

The plan's input budget is `input_bytes=24800`, `base_bytes=9242`,
`child_bytes=7000`; the chunk planning estimate is **11,459**, and both singleton
reducer estimates are **16,242**, at levels one and two. These are conservative
planning-envelope estimates, not actual model tokens. Managed execution separately
renders and checks each actual request with 200 overhead/safety tokens.

The plan is reproducible review evidence, **not the actual operator's executable
configuration**. Actual scope changes extraction/plan identities; fresh private
paths, existing authority policy, commercial catalog, embedding directory/hash,
times and identity remain to be supplied and reviewed. No final configuration
hash is asserted here. Rebuild the plan under that verified scope, recompute the
complete configuration digest and bind independent approval to it. Never insert
Attempt 6 output or old accepted checkpoints into this new run.

The launcher's generation digest hashes an explicit source inventory rather
than the entire transitive implementation. `sizing.py`, `workflow.py` and the
launcher itself are not direct entries. Freeze/review the complete working tree
for operator handoff as well as checking the authoritative digest. Supplemental
current file SHA-256 values are:

| File | SHA-256 |
| --- | --- |
| `documents/digestion/sizing.py` | `18356d57daf6e202e75c976dcd8023119388cde8ef0c373c4ddb390de9612a96` |
| `documents/digestion/workflow.py` | `2c31599146889e4dc8f03142266c21ad3541e346051ec788b0914b67b3141a76` |
| `tests/performance/foundry_l1.py` | `7f90695897cb4056b290f3ff79d414aa274469824b5e7f2155f10cd82679fc3c` |

This source-inventory limit does not demonstrate a current execution defect or
justify changing the launcher in this assessment. A later requirement for a
stronger transitive integrity contract would require separate engineering review.

Expected private runtime artifacts include `source.pdf`, `fixture.json`, local
content-addressed source/extraction/plan/checkpoint/digest/coverage objects,
`jobs.sqlite`, `run.sqlite`, `publication.sqlite`, local `vectors/`,
`provider-calls.json`, `responses.json`, `result.json`, `review-packets.json` and
`financial-audit.json`. Existing external security/governance/admission authorities
are reused through their approved contracts. A future actual launch also creates
one-use approval-consumption and run-start markers. None was created by this
task. Raw runtime responses remain private and must not be copied into Git.

## 4. G1/G2 compatibility assessment

**PASS / current source and fresh plan:** G1's corrected policy is enabled,
bound into the inference/planning fingerprints and enforced both before inference
and before checkpoint acceptance. Raw and canonical 10,000-byte allowances remain
independent of the inclusive 3,000-token completion reservation. They do not
guarantee that every model response can fit; oversize results fail closed without
truncation or a paid repair call. Root results also undergo the child-material
admission rule even though this plan has no later digest reducer.

**Historical supporting evidence:** the G1/G2 report records 32 focused passes
and 335 relevant regression passes, with 12 overlapping cases: **355 distinct
cases**, not 367. A subsequent nine-case G2 run verified strengthened size
witnesses. It records 31 passing current L1 integration cases. These large
selections were not repeated here. Existing G1 tests reproduce escaped overflow,
reject incompatible budgets/policy removal, and verify admitted escaped children;
the current policy-removal check was selected again as a narrow binding check.

G2's permanent [strict two-chunk integration](../../../tests/integration/test_phase17h_two_chunk.py)
is historical evidence for the complete cross-chunk qualification/opposition and
negative-case workflow using **five synthetic calls**. It does not authorize five
live calls. The intended four-call L1 remains one chunk, structural and root:
it demonstrates two reduction levels, not multi-chunk live aggregation. No new
launcher shape or cumulative envelope is needed for that intended milestone.

The Q&A full-envelope correction is present in
[analysis.py](../../../documents/publication/analysis.py). Its selected escaped
evidence/annotation regression passed again, including refusal before executor
use at an inadequate limit. No provider routing, API or streaming contract change
is needed for preparation.

## 5. Local embedding, publication and retrieval readiness

| Prerequisite | Classification and actual result |
| --- | --- |
| Required embedding model | **PASS / source and local load:** `sentence-transformers/all-MiniLM-L6-v2`, revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, from [model_artifacts.py](../../../config/model_artifacts.py). The exact revision directory exists in the ordinary local model cache. |
| Model/tokenizer contract | **PASS / executed offline:** CPU load with `local_files_only=True`; model/tokenizer limits 256; actual finite, normalized 384-dimensional embedding; measured norm approximately 1.0000000193. Retrieval profile permits 240 tokens/4,096 characters per record, normalized vectors and `source-retrieval/1`. |
| Candidate content fingerprint | **PASS / measured, approval PENDING:** eleven files, 91,578,415 bytes; content-tree SHA-256 `96ab3cd391276cb159904c4d329318ae1f3330278a7fc0450256233cf8bb78db`. See hash qualification below. |
| Cache path as approved launcher directory | **BLOCKED for direct in-place use:** all eleven files are symlinks, explicitly refused by `local_retrieval`. No regular-file operator directory was inspected or assumed. |
| Local vector store | **PASS / executed offline:** installed Chroma 1.5.9; scratch `PersistentClient`, telemetry disabled, actual model embedding, administrative upsert/query/inventory succeeded; wrong generation and wrong document returned no matches. No Chroma HTTP or remote service was used. |
| Publication/retrieval composition | **PASS / source and selected integration:** authorized plan/prepare/activate, ready replica, original-source records, generation/document pinning, citations and generated annotations. The integrated smoke uses fake embeddings/vectors; the additional real-model/Chroma check is a separate local component check. |
| Final writable isolated storage | **PENDING / operator:** approved new private audit/object/job/publication/vector paths, adequate capacity/permissions, existing authority compatibility and persistent independent replay storage. Scratch `/tmp` success does not verify those protected paths. |

The measured hash uses the launcher's sorted relative-path, NUL separator and
SHA-256-of-file-bytes algorithm, reading the cache files' existing local targets.
It is the expected content hash **if exactly those eleven paths/bytes are copied
as regular files without extra files**. It is not an existing signed configuration
pin, a hash of the symlink representations or independent verification of upstream
authenticity. The authoritative required revision is source-verified; the final
operator-approved tree fingerprint remains **PENDING** until a compliant directory
is inspected and hashed with the launcher's no-symlink rule. No copy, cache
modification, download or model installation was performed.

The live composition explicitly uses local persistent Chroma collection
`phase17hl_documents` under its new audit directory, local CPU embeddings and a
deterministic pass-through reranker. The separate application reranker model is
not required by this composition. Generic application `CHROMA_PATH`, collection
or model defaults do not redirect that explicit launcher setup. Semantic ranking
quality remains unvalidated; successful component retrieval is not an answer
quality measurement. Source text records and derived annotations remain separate.

## 6. Security, authentication and operator-approval requirements

**PASS / source:** [LaunchConfiguration and launch guards](../../../tests/performance/foundry_l1.py),
[approval verification](../../../tests/performance/foundry_approval.py),
[identity verifier](../../../security/identity.py) and
[security authority](../../../security/authority.py) preserve distinct gates:

1. Fresh explicit human authorization for the exact full four-call scope and
   complete configuration, including new source/generation/profile bindings.
2. Valid signed operator access token with correct issuer, audience, tenant,
   subject, owner scope and lifetime. Under the existing Entra v2 profile, delegated
   `access_as_user` and exactly `PolyMind.L1Operator` are required. The launcher
   uses the configuration's `oidc` object, not an assumed dotenv identity.
3. Existing registered/enabled principal and document ownership/permissions,
   including publication management. The background workflow deliberately binds
   its existing `DOCUMENT_DELETE` authorization snapshot; Q&A uses
   `DOCUMENT_ANALYZE`, and usage audit requires its existing permission. Do not
   replace these with a newly fabricated principal or authority.
4. Separately valid inference credential for the configured authentication
   method and approved target. Identity authentication and inference credentials
   are different. Credential audience/expiry/access and current target capacity
   are operator attestations/verification, not inferred from strings or booleans.
5. Independent RS256 operator approval with pinned public trust and exact
   bindings, fresh ID and current window; L1 audience `polymind-l1-live`.
   Attempt 6's consumed `polymind-single-analysis-live` artifact cannot cover it.
   The acknowledgement/configuration digest must match. Trust is provisioned
   separately from the approval and configuration; the launcher never signs.

The signature's lifetime is at most 24 hours. Configuration validation requires
more than 600 seconds before the earlier approval/credential deadline and a
compatible not-before window; runtime additionally checks principal/window expiry
and cancellation before subsequent work. Use the established operator procedure
to verify timing immediately before any separately authorized execution.

One-use consumption uses exclusive persistent creation plus file/directory fsync;
the independent run-start marker and persisted call records prevent automatic
replay. **Consumption precedes local embedding setup**, so the regular-file model
directory, tree hash and local storage should be checked before signing/launching.
A setup failure can consume approval with no inference. Never delete historical
markers, substitute authority databases or reset an outstanding run to retry.
These safeguards assume the established trusted single-host environment.

### Environment names and configuration completeness

| Input group | Required names/fields and current assessment |
| --- | --- |
| Launcher runtime secrets | `POLYMIND_L1_OPERATOR_TOKEN`, `POLYMIND_L1_AZURE_CREDENTIAL`. Presence-only check found the former set and the latter unset. No values were printed, decoded, verified or used. A set variable is not a valid-current identity claim. **PENDING** operator provisioning/verification. |
| Reviewed launch JSON | Target/model/version/SKU/endpoint/authentication, credential/approval times, generation digest/not-before, owner scope/OIDC, three existing authority paths and quota key, new audit path, local embedding path/tree hash, actual Azure RPM/TPM, admission policy, governance policy and financial `Contract`. **PASS** schema inventory; **PENDING** actual operator values and exact complete validated digest. No booleans were asserted as verified here. |
| Existing application security/governance composition | `API_AUTH_MODE`, `API_AUTH_ENABLED`, `API_DOCS_ENABLED`, `OIDC_CONFIGURATION`, `SECURITY_AUTHORITY_PATH`, `GOVERNANCE_ENABLED`, `GOVERNANCE_AUTHORITY_PATH`, `GOVERNANCE_PROVIDER_PATH`, `GOVERNANCE_PROVIDER_KEY`, `GOVERNANCE_POLICY`, `GOVERNANCE_PRICING`, `GOVERNANCE_PROVIDER_POLICY`. Source/example inspected only. With `oidc_jwt`, `API_AUTH_TOKEN` must be absent, including no empty assignment. |
| Application model/vector settings | `MODEL_ARTIFACT_DIR`, `MODEL_OFFLINE_MODE`, `VECTOR_STORE_PROVIDER`, `CHROMA_PATH`, `VECTOR_STORE_COLLECTION`; managed settings prefix `DOCUMENT_INFERENCE_`, including `DOCUMENT_INFERENCE_CHILD_INPUT_BYTES`. These do not substitute for the launcher's explicit local directory/hash and L1 profile. `MODEL_ARTIFACT_DIR` and `MODEL_OFFLINE_MODE` were unset in the assessment process; dotenv was not loaded. |

Private configuration completeness, signing-key provenance, trust/replay
permissions, live JWKS/authentication and existing authority state remain
**PENDING**. No credentials, private configurations, signatures, keys, protected
authority databases or historical replay records were opened. Public field names
and the process environment's required-name presence are the only secret-input
observations made here.

## 7. Token ceilings, financial governance and estimation methodology

| Safeguard | Verified contract and proposed scope |
| --- | --- |
| Per-call input | At most **25,000**; complete rendered managed/Q&A input capped at 24,800 plus 100 overhead and 100 safety. A stricter effective policy wins. |
| Per-call output | **3,000 inclusive completion tokens**, including any reported reasoning subset. No additional reasoning allowance. |
| Cumulative maximum | Four attempts: **100,000 input + 12,000 output = 112,000 total tokens**. Existing L1 validator requires four attempts and `fits(4)` under aggregate limits. Preserve these ceilings; no expansion is needed. |
| Context and capacity | 28,000 conservative context; run RPM 1; one outstanding inference call. Candidate shared policy is 30,000 TPM with at least 2,000 interactive TPM protected; larger existing reserves/stricter actual limits win. Live runtime spaces starts by at least 61 real seconds. Actual shared RPM/TPM and other consumers are **PENDING**. |
| Automatic paid retries | **Zero:** `RetryPolicy(max_attempts=1)`, no Q&A retry loop, bounded provider execution makes one POST, readiness retries zero in live construction. No fallback/repair call. |
| Maximum financial exposure | Required approved run `maximum = M`, **0 < M <= EUR 5**, including explicit aggregate fixed/extra bounds. This task approves **EUR 0**. The exact prospective catalog-priced exposure is **PENDING**, not a current quote. |
| Durable reservation/settlement | `GovernedExecution` reserves owner/tenant budget before provider admission, transitions to STARTED, then settles known actual usage. `RunGuard` durably retains the full per-call ceiling, never refunds it to buy another call, and blocks outstanding/unknown work. |

Sources: [financial Contract and RunGuard](../../../tests/performance/foundry_budget.py),
[governed execution](../../../governance/execution.py),
[catalog and ledger](../../../governance/ledger.py),
[provider execution](../../../llm/openai_compatible.py) and
[bounded transport](../../../llm/bounded_http.py).

The public model contract names `gpt-5.4-mini`, version `2026-03-17`, SKU
`GlobalStandard`; provider roles use the repository's configured `DEPLOYMENT`
constant. Catalog lookup is by **provider and served deployment identifier**, not
only the public model family. Those literal bindings are source-verified, not
proof that Azure currently serves the asserted model/version or pricing tier.
Actual target/model availability remains an operator verification item.

Use the exact validated catalog's positive EUR input/output `Decimal` rates
`r_in`, `r_out` and its decimal-power `price_unit = U`. The catalog must be unique,
operator approved and effective no later than execution; the model lookup must
succeed. `Contract` requires explicit `price_source`, region, tier, maximum and
fixed/extra upper bounds. Compute without floating-point rounding:

```text
per-call token upper bound = (25,000 * r_in + 3,000 * r_out) / U
four-call token upper bound = (100,000 * r_in + 12,000 * r_out) / U
run upper bound = four-call token upper bound + fixed_cost + extra_cost
require run upper bound <= M <= EUR 5
actual token catalog cost = sum((actual_input_i*r_in + actual_output_i*r_out)/U)
```

For per-million prices this is `0.100000*r_in + 0.012000*r_out + fixed_cost
+ extra_cost`. Do not use synthetic test rates, assume cache discounts, count
reasoning twice, multiply fixed aggregate costs by four, or quote historical
single-call spend as a current four-call price. Actual non-token charges require
their own approved accounting/upper-bound evidence; token-ledger settlement alone
does not establish invoice completeness.

**PENDING / operator:** current applicable commercial source/agreement, date,
currency and any conversion, model/deployment/SKU/region applicability, fixed and
incremental charges, fresh quota/shared-consumer attestations, current owner/tenant
monthly and daily headroom and unresolved obligations. The EUR 5 monthly limit is
shared remaining governance headroom, not a new EUR 5 allowance for this task.
The existing optional evaluation overlay is scope/path/policy bound; its limits
do not authorize activation or a new database. Do not migrate or reset policies.

No current private catalog was accessed and no price lookup was made externally.
Historical catalog dates/rates from the Attempt 6 report are **historical only**.
`operator_approved=True` and a non-future effective date do not independently prove
price freshness, quota validity or invoice accuracy. Until the commercial basis
and extras are reviewed, no numeric current run estimate is defensible beyond
the required **EUR 5 governance upper ceiling** and the formula above.

### Mandatory stop conditions

Stop on the first provider failure/429/timeout/refusal/truncation or invalid
protocol/model; raw/canonical/child/input/output limit breach; invalid source,
claim or child coverage; failed checkpoint/fence/dependency; expired/mismatched or
revoked identity/approval; cancellation; financial/admission denial; missing,
inconsistent or excessive usage; settlement/accounting failure; publication,
activation, readiness, retrieval or citation/provenance failure; unexpected paid
dependency; or a human-identified critical unsupported conclusion. Preserve paid
usage even if domain validation rejects a completed provider response. Unknown
usage remains outstanding and blocks automatic continuation. Do not retry,
increase limits, repair responses or continue with another model.

Semantic failure discovered after the four calls changes acceptance; no code can
retroactively prevent already incurred spend. Preserve separate provider,
application, digest, publication, answer and accounting outcomes. A failed Q&A
does not erase an already accepted digest/publication or known costs.

## 8. Offline checks executed and actual results

Temporary scripts/results are under
`/tmp/phase17h-four-call-readiness-20261102/`; these are disposable assessment
artifacts, not private authority storage or a permanent operator handoff. The
only permanent additions are this report and its normalized prompt.

Before application imports, a temporary guard replaced socket connect/connect_ex/
sendto and DNS/create_connection entry points with counting failures. Application
dotenv input was suppressed through the existing test settings isolation.
Bytecode and pytest repository-cache writes were disabled. Model loading used
offline/telemetry-disable flags and one CPU thread; scratch Chroma disabled
anonymized telemetry. This is Python-level network isolation, not an OS firewall
or a claim about all possible native-library transports.

| Check actually run | Outcome |
| --- | --- |
| Initial Git status/diff and required source/report inspection | Existing dirty G1/G2 work recorded before work; current architecture and consumer paths inspected. |
| `prepare_offline.py` using `workflow.prepare`, fresh fixture/extraction and inert configured-model provider | **PASS:** two equal plans, one chunk/two reducers/five durable specs/four planned calls; full canonical source resolution, active 7,000-byte budget; **0 network attempts, 0 inference executions**. |
| Selected current four-call E2E test | **PASS:** strict fake HTTP/application acceptance, coverage, immutable reopen, publication/retrieval, Q&A, four synthetic settlements and reuse without extra calls. No live launcher or approval helper invoked. |
| Selected removed-policy rendering test | **PASS:** incompatible binding refused before inference. |
| Selected escaped Q&A envelope test | **PASS:** complete governed envelope checked without dropping evidence/annotations. |
| Combined targeted pytest run | **3 passed in 2.36s; 0 failures/errors/skips; 0 observed network attempts.** JUnit output retained externally. |
| `check_retrieval.py` on existing cached model and scratch persistent Chroma | **PASS:** CPU load, 384-dimensional normalized embedding, actual local vector round-trip, inventory and wrong-generation/document refusal; **0 observed network attempts**. Eleven symlinks identified as direct-launch incompatibility. |
| Dependency observations | sentence-transformers 5.5.1, Chroma 1.5.9, torch 2.12.0, Pydantic 2.13.4 present. No dependency installed. A model embedding-dimension method rename emitted one `FutureWarning`; computation succeeded. |

The targeted pytest command was:

```bash
PYTHONPATH=/tmp/phase17h-four-call-readiness-20261102:. \
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
python -m pytest -p offline_guard -p no:cacheprovider \
  tests/integration/test_phase17hl_offline_e2e.py::test_l1_extraction_dag_schema_digest_citations_accounting_and_reopen \
  tests/unit/documents/test_managed_sizing.py::test_render_rejects_removed_policy_before_inference \
  tests/unit/publication/test_analysis.py::test_escaped_evidence_and_annotations_use_complete_governed_envelope \
  --basetemp=/tmp/phase17h-four-call-readiness-20261102/pytest \
  --junitxml=/tmp/phase17h-four-call-readiness-20261102/targeted.xml \
  -o junit_family=xunit1 -q
```

Selection was limited to the fresh L1 composition/binding and Q&A envelope needed
for this readiness decision. No complete regression suite, large benchmark,
historical response investigation, signer/approval test, live launcher, compileall,
Docker, Kubernetes, cloud discovery or web/pricing check was run. The historical
G1/G2 suite remains attributed evidence, not a new pass claim. Compilation/builds
were unnecessary for two Markdown additions.

Existing procedures remain available in the
[Foundry runbook](../../evaluation/phase_17h_foundry_validation.md),
[operator approval procedure](../../evaluation/phase_17hl_operator_approval.md),
[Entra guide](../../security/entra_v2.md), G1/G2 report, preflight module and
selected tests. Their historical handoffs do not authorize execution or justify
reusing stale packets. No launch command is part of this report's recommendation.

## 9. Outstanding prerequisites and blockers

| Item | Status | Smallest necessary action |
| --- | --- | --- |
| Existing cached model directory supplied directly to launcher | **BLOCKED for that path** | During separate preparation, choose a verified regular-file tree or copy cached model bytes into an approved new regular-file directory; verify revision, no symlinks, local CPU load and exact tree hash. No download or code change required. |
| Final embedding directory/hash and private storage readiness | **PENDING** | Operator supplies compliant path, pins measured hash and confirms permissions/capacity. An existing private compliant tree may already satisfy this; it was outside this assessment. |
| Actual operator-scope plan and complete final configuration | **PENDING** | Freshly generate the same fixture under verified scope, reconcile source/profile/stage identities and four-call count; validate exact configuration and freeze all reviewed source bytes. Preserve existing untracked `sizing.py` with the reviewed working tree. |
| Current commercial catalog, extras and exact maximum exposure | **PENDING** | Review applicable current EUR catalog/conversion/source and aggregate charge bounds; compute `cost(4)`, select M <= EUR 5, verify remaining headroom. No historical price assumed. |
| Authentication, inference credential and target capability/capacity | **PENDING** | Operator verifies current identity, exact scope/role/audience, credential lifetime/access, model/version/SKU and shared quota. Inference credential was absent in this process. |
| Existing security/governance/admission authority compatibility and obligations | **PENDING** | Operator verifies existing registered principal, approved policies and outstanding/UNKNOWN obligations through the authorized private process. No authority replacement, activation or reservation in this task. |
| Independent trust, retention/replay storage, new window and signature | **PENDING** | Independently review trust/key provenance and full exact configuration; obtain explicit human authorization and a fresh one-use L1 signature. Do not consume it during preparation. |
| Live hierarchy and answer/citation quality | **PENDING** | Only after separate authorization, obtain the accepted four-call chain and independent review. This task supplies no live result. |
| Application/launcher code correction before preparation | **PASS: none demonstrated necessary** | Keep existing implementation; no separate engineering task is required by current evidence. |

The model-path issue is a bounded operational preparation requirement, not an
unresolved G1/G2 implementation defect. There is no evidence requiring launcher
changes. If operator preparation reveals an actual incompatibility in the
existing contracts, stop and scope the smallest engineering task separately;
do not adjust a historical packet or weaken guards to pass.

## 10. Engineering GO / NO-GO decision

**GO for preparing the controlled four-call L1 evaluation.** Current source,
fresh deterministic planning, current targeted workflow evidence and actual local
model/vector component availability support preparation without another
application change. G1's sizing gate is resolved within this bounded profile;
G2's offline engineering evidence is sufficient for preparing the smaller L1.

This decision authorizes neither launch nor signing/reservation. The inspected
symlinked cache cannot be the final launcher directory; its compliant packaging
and the pending private/external checks must be complete before an execution
decision. Broader Phase 17H, live reductions, semantic quality, real workload
reliability, L2 and production/external-user readiness remain unestablished.

## 11. Execution authorization status

**NOT AUTHORIZED.** No explicit live instruction, validated actual-scope final
configuration, independently verified new signature or fresh identity/financial
evidence was supplied or consumed. Historical approvals/checkpoints/configuration
bindings are unusable for this new evaluation. A passing engineering assessment,
present environment variable, candidate plan or historical successful call grants
no execution rights.

Paid provider calls, cloud operations/modifications, real financial reservations,
budget consumption, signatures and authorization consumptions by this task:
**all zero**. The selected integration creates only isolated synthetic governance
rows under temporary test storage; these are not real financial obligations.

## 12. Recommended next action, review and repository preservation

Perform a **separately scoped operator preparation and final authorization review**:
resolve the local model packaging, verify private authorities/current identity
and commercial/capacity evidence, regenerate actual-scope plan and exact complete
configuration, and review the resulting four-call financial envelope and stop
procedure. Complete those static checks before seeking fresh independent signing
and explicit launch authorization. Do not launch as part of this assessment or
reuse a single-call signer/configuration. No next major phase is started.

Future acceptance requires four expected accepted calls, COMPLETE fraction-one
digest with connected provenance, persisted/reopened artifacts, successful
authorized publication/retrieval, correct page-one answer/citation, four matching
known-usage settlements, no accounting failure and independent semantic review.
Schema/citation membership alone does not prove entailment or qualifier retention
in root prose; exact qualifications/conflicts persist in artifacts while narrative
faithfulness remains a human review requirement.

Implementation self-review checked source-bound sizing, strict/Q&A distinctions,
checkpoint/recovery limits, source versus derived evidence, one-use approval,
actual versus catalog-estimated cost and separate preparation/authorization
decisions. Pre-commit review is limited to these new Markdown records: no secret,
signed payload, operational private identity/path, raw response, live handoff
command, temporary dependency or API change is introduced. Relative file links
and whitespace are checked independently because ordinary Git diff excludes
untracked files.

Repository preservation checks and final command results are recorded below.
No staging, branch switch, reset, commit, push or remote mutation occurred.

Final `git status --short` reports **10 pre-existing modified tracked files and
8 untracked files**: the original six plus these two Markdown records. There are
zero staged entries. A baseline comparison verifies the complete tracked diff
bytes, hashes of all six pre-existing untracked files, index diff, HEAD and branch
are unchanged; the only status additions are the requested report and prompt.

Final `git diff --stat` remains the pre-existing aggregate:

```text
 README.md                                       | 14 +++++++
 documents/digestion/managed.py                  | 52 +++++++++++++++++++++----
 documents/digestion/models.py                   | 10 +++++
 documents/digestion/planning.py                 | 21 +++++++++-
 documents/digestion/validation.py               |  5 +++
 documents/digestion/workflow.py                 |  8 ++++
 documents/publication/analysis.py               |  4 +-
 tests/integration/test_phase17hl_offline_e2e.py | 43 ++++++++++++++++++--
 tests/performance/foundry_preflight.py          |  1 +
 tests/unit/publication/test_analysis.py         | 40 +++++++++++++++++++
 10 files changed, 184 insertions(+), 14 deletions(-)
```

Untracked Markdown additions are not included in that tracked diff statistic.
`git diff --check` passed. Separate new-file checks passed for final newlines,
trailing whitespace, **26 relative file links** and a targeted sensitive-literal
review. The source/configuration/schema fingerprints in this report were
reconciled with the newly calculated review data. No existing documentation,
application, test or configuration file changed during this task.
