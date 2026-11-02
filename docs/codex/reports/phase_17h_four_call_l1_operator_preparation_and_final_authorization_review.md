# Phase 17H — Four-Call L1 Operator Preparation and Final Authorization Review

Assessment date: 2 November 2026. Assessed HEAD:
`b15713e6b6d22ef166a70cb0e3bf63d0dc542951`, branch `master`.
Scope: offline operator preparation, local model preservation and documentation.

## 1. Executive summary

**Engineering readiness: GO** for final operator preparation under the existing
four-call L1 contract. **Operator preparation: READY WITH GAPS. Live execution
authorization: NOT AUTHORIZED.** The public engineering prerequisites pass, and
the temporary model packaging risk is resolved. An actual approval-ready private
packet still requires current identity, authority, commercial, quota, storage and
window evidence. Independent approval cannot responsibly be issued from this
public preparation report alone. **Phase 17H remains PARTIAL.**

The exact checkpoint has a successful GitHub Actions run. Two fresh public-scope
plans reproduce the established one-chunk/two-reducer hierarchy and hashes.
Three targeted current offline tests passed in **2.30 seconds**, with zero
failures/errors/skips and zero observed network attempts. The required embedding
model is now preserved outside temporary storage and Git: **11 regular files,
91,578,415 bytes, no symlinks**, tree SHA-256:

```text
96ab3cd391276cb159904c4d329318ae1f3330278a7fc0450256233cf8bb78db
```

Offline CPU loading, the actual launcher local-retrieval factory and isolated
Chroma operations passed on the durable copy. No application, test, launcher or
configuration code was changed; no concrete blocking engineering defect was
demonstrated. Known acceptance limits require explicit operator review, especially
the distinction between a successful harness status and a correct four-call answer.

No protected configuration, credentials, keys, trust file, replay records or real
authority database was opened. No inference, cloud modification, Kubernetes,
signing, approval consumption or real reservation occurred. No Git mutation
occurred. Public GitHub CI metadata and public Microsoft documentation were read.

Evidence labels: **PASS/source** means inspected current implementation;
**PASS/offline** means executed bounded local verification; **historical** means
attributed prior evidence; **PENDING/operator** means unverified private or cloud
state. No PENDING condition is treated as a PASS.

## 2. Source and CI checkpoint verification

Initial `git status --short`, tracked diff and staged diff were empty. HEAD is
the supplied `b15713e` checkpoint. Read-only GitHub API inspection confirms
[Estudio PolyMind CI run #42](https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/41458857637),
push event, attempt 1, exact full HEAD above, **completed/success**. It started
at `2026-11-02T14:06:49Z`; metadata was updated at `14:14:00Z`. Its `build` job
and test, compile, Helm validation, Compose validation and Docker-build steps all
report success. No remote jobs were triggered or rerun. Remote test counts were
not recovered from logs; success metadata is the current CI evidence.

The [CI reconciliation report](phase_17h_ci_failure_and_historical_contract_reconciliation.md)
provides historical complete local-suite evidence: **1,850 passed, zero failures,
errors or skips, 530.73 seconds**, zero observed main-interpreter network attempts.
That complete suite was not repeated. HEAD includes the G1/G2 implementation and
historical test corrections; earlier dirty-tree reports are historical snapshots.

Reviewed evidence also includes the [hierarchy assessment](phase_17h_hierarchical_digestion_readiness_assessment.md),
[G1/G2 engineering report](phase_17h_g1_g2_offline_engineering_and_integration_hardening.md),
[previous four-call preparation](phase_17h_four_call_l1_live_preparation_and_authorization_readiness.md),
[model packaging report](phase_17h_g1_g2_git_checkpoint_and_embedding_packaging.md),
[Attempt 6 closure](phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md),
[Foundry runbook](../../evaluation/phase_17h_foundry_validation.md) and
[independent approval procedure](../../evaluation/phase_17hl_operator_approval.md).
Attempt 6 establishes historical single-analysis acceptance only. Its consumed
approval, retained output and historical financial observations were not reused.

Current [L1 composition](../../../tests/performance/foundry_preflight.py) explicitly
selects `managed-generation/2`, `managed-prompt/4`, `azure-strict/1`, unchanged
application `stage-result/1` validation and **7,000-byte child-material admission**.
Raw and canonical result ceilings remain independently 10,000 bytes; the HTTP
response-envelope ceiling is 26,192 bytes. Oversize material is rejected without
truncation, evidence repair or another model call.

[Evidence validation](../../../documents/digestion/validation.py) binds scope,
document version, extraction, source/block/span coordinates, allowed evidence,
deterministic claim identities and every child claim link. Finalization reopens
and revalidates immutable checkpoints before committing digest and coverage.
The provider-neutral inference boundary, API and streaming contracts are unchanged.

## 3. Durable embedding validation

The existing external model manifest identified the previous regular-file package
under `/tmp/polymind-local-embedding-p30beqpd/`. Before copying, every file's size
and SHA-256 was checked against that manifest, and the complete tree fingerprint
was independently recomputed. The source was present and matched exactly.

A new exclusive model-only parent was created at this home-relative location:

```text
~/.local/share/estudio-polymind/phase17h-l1-embedding-20261102/
  model-manifest.json
  all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/
```

The revision directory is the candidate `embedding_directory`. The manifest is
outside it and does not alter its fingerprint. The operator must resolve this
location to an absolute path for launch configuration; literal `~` is not a
launcher-compatible absolute path. This measured candidate is not a signed or
approved configuration pin.

The sandbox approved the narrowly scoped external-directory copy. Existing model
directories were not overwritten. Source/destination ancestors were checked for
symlinks and unsafe writable traversal (the sticky `/tmp` ancestor is expected).
Source files were opened with `O_NOFOLLOW`; destination files used exclusive
creation, mode 0600, followed by flush/fsync. New directories are mode 0700 and
owned by current UID 1000. Parent directories through the new tree were fsynced.
The source package was rehashed unchanged after copying.

| Exact relative file inventory | Bytes |
| --- | ---: |
| `1_Pooling/config.json` | 190 |
| `README.md` | 10,502 |
| `config.json` | 612 |
| `config_sentence_transformers.json` | 116 |
| `model.safetensors` | 90,868,376 |
| `modules.json` | 349 |
| `sentence_bert_config.json` | 53 |
| `special_tokens_map.json` | 112 |
| `tokenizer.json` | 466,247 |
| `tokenizer_config.json` | 350 |
| `vocab.txt` | 231,508 |

**PASS/offline:** exact set, no special entries, no symlinks, matching per-file
hashes and tree hash before and after loading. Revision matches the authoritative
[model inventory](../../../config/model_artifacts.py) and retrieval profile.
Provenance reuses the earlier locally verified snapshot/blob evidence; it is not
a new authenticated upstream checkout. No model download or dependency install
was attempted.

**PASS/offline:** `SentenceTransformer(local_path, local_files_only=True,
device='cpu')`; model/tokenizer limits 256/256; 384 finite dimensions; norm
`1.0000000192877587`. `source-retrieval/1` uses normalized vectors, 240 tokens and
4,096 characters per record. The actual `foundry_l1.local_retrieval` factory
accepted the durable directory and matching hash. Wrong-hash and symlink fixtures
were refused before use.

Actual local Chroma write/query/inventory used three synthetic records; generation
and document filters excluded unrelated records, and version metadata round-tripped.
No independent version-prefilter capability is claimed. The adapter was closed.
These component checks complement the fake-embedding E2E test; they are not a full
real-embedding publication or live semantic-quality test.

Free storage was **883,659,706,368 bytes before** and **883,568,078,848 bytes after**
the durable copy, adequate for its 91.6 MB payload. Actual future audit/vector/object
storage capacity, retention and operator approval remain PENDING. The copy is on
the persistent home filesystem rather than `/tmp`; it is not an independently
backed-up or immutable operator repository. Preserve it and its external manifest.

## 4. Exact proposed four-call plan

Fresh generation used `phase17h-pdf/1`, seed 1708, four physical pages and six
authored lines/page, including the established page-three untrusted injection.
The PDF is **3,537 bytes**. Extraction produced four evidence pieces whose
canonical resolved text exactly reconstructs every source unit. Document ID is
`UUID(int=4)`; fixed fixture timestamps remain unchanged. A deterministic public
synthetic `Scope` was used solely for planning; no operator principal was issued
or claimed and no security/financial authority was opened by plan generation.

| Sequence | Dependency and required outcome |
| --- | --- |
| Call 1: `chunk` | All four source pieces in one analysis; strict accepted result and immutable checkpoint. |
| Call 2: `structural`, level 1 | Committed call-1 checkpoint, complete child result, evidence and every required claim link. |
| Call 3: `root`, level 2 | Committed call-2 checkpoint, same strict lineage/size requirements. |
| Local bridge | Reopen/revalidate all checkpoints; persist COMPLETE digest and full coverage; authorize publication plan/prepare/activation; load ready replica; retrieve selected original evidence and resolve citations. No inference. |
| Call 4: grounded Q&A | Only after successful bridge: “What is the first inspection procedure on physical page 1?” Correct finding: “Unit 0001 procedure 0: inspect valve 5153 before operation.” Validate cited original page-one evidence and independent semantic support. |

The durable digestion job has **five local steps**: plan anchor → chunk →
structural → root → digest finalization. Q&A is downstream. The configured
`intermediate` profile is not selected. Extraction, CPU embedding, publication,
retrieval and citation resolution add no Azure model calls. A successful evaluation
must show exactly four completed calls; failure must stop earlier. Two-chunk G2
evidence uses five synthetic calls and cannot be substituted for this live scope.

Current plan estimates are **11,459** for the chunk and **16,242** for each reducer.
The managed planning budget is `input_bytes=24800`, `base_bytes=9242`,
`child_bytes=7000`. These conservative planning estimates are not billed tokens.
The public plan was generated independently into two fresh stores; objects,
references and dependency graph matched exactly.

An inert configured-deployment provider rendered the actual public-scope chunk
without executing it: **11,426 rendered bytes + 200 overhead/safety = 11,626
admitted input**, output reservation 3,000, context 28,000. Reducer and Q&A actual
live inputs depend on accepted model output and retrieval; their final hashes and
sizes cannot be computed truthfully before those results exist.

Passive observation of the existing successful synthetic E2E case measured:

| Synthetic call | Full rendered envelope bytes | Input with 200 overhead/safety | Reserved output |
| --- | ---: | ---: | ---: |
| chunk | 11,426 | 11,626 | 3,000 |
| structural | 10,942 | 11,142 | 3,000 |
| root | 10,628 | 10,828 | 3,000 |
| Q&A | 8,078 | 8,278 | 3,000 |

These are fixture-output witnesses, not predictions of live output sizes. All
full envelopes pass the 24,800-byte input bound and 28,000-token conservative
context check. Runtime rechecks every actual escaped envelope; the G1 child bound
and reserved wrapper material constrain downstream admission without truncation.

Required private artifacts include `source.pdf`, `fixture.json`, content-addressed
source/extraction/plan/checkpoint/digest/coverage/publication objects, `jobs.sqlite`,
`run.sqlite`, `publication.sqlite`, `vectors/`, `provider-calls.json`, `responses.json`,
`result.json`, `review-packets.json` and `financial-audit.json`. Reuse the existing
external security/governance/admission authorities. A separately authorized run
also records one-use approval consumption centrally and `live-started.json` in
its audit directory. This task created neither real marker nor real reservation.

## 5. Configuration and source bindings

The following were freshly recomputed at current HEAD, with the configured served
deployment identity and the current G1-enabled settings. They reproduce the
earlier public preparation evidence without importing historical checkpoints.

| Public review binding | SHA-256 |
| --- | --- |
| PDF source bytes | `1be99e19a56040fb55c74682a19f874d4d4573f18d9f52a9a7ae19c8158ea92d` |
| Public synthetic-scope extraction | `841e5c121e0ab3ee05c9bd4a5cb9f5a4551b1415fb6b8cc26906f10ddadb1b22` |
| Public synthetic-scope plan / fingerprint | `8bc0776f9f5ebd11491d6cac5233a0e7f380b92a5fb19aeb96be132a9bf7bde4` |
| Bound planning profile | `e11dc86cd3247fb45cb263b403301990ca53c74c40d858fba2de28740c286e6b` |
| Managed inference configuration | `6630c6203d1638633fae7c5edfdca866917f745d89aefb34d5bc0824ab0f2f43` |
| Authoritative generation source inventory | `00bf895290e1da2fb81372ff1ea921d8d7f464ea14f41110f54313d0423ad904` |
| Application generation schema | `a051949799a312d1aa15a5959bbe7d558265cfc38f6ce992eb97fbdbdff212ab` |
| Azure strict provider schema | `4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2` |

Public scope is explicitly `uuid5(NAMESPACE_URL, 'phase17h-four-call-readiness/tenant')`
and `uuid5(NAMESPACE_URL, 'phase17h-four-call-readiness/owner')`. Reproduction uses
the current fixture generator, fixed timestamps, exact settings/profile above,
`workflow.prepare`, the configured deployment's inert `model_id`, and the
launcher generation/schema digest functions. These hashes establish a public
review plan, not a live operator binding.

The launcher's generation digest covers an explicit source inventory, not every
transitive file. HEAD and clean engineering tree also matter. Fresh supplemental
hashes for relevant omitted files are:

| File | SHA-256 |
| --- | --- |
| `documents/digestion/sizing.py` | `18356d57daf6e202e75c976dcd8023119388cde8ef0c373c4ddb390de9612a96` |
| `documents/digestion/workflow.py` | `2c31599146889e4dc8f03142266c21ad3541e346051ec788b0914b67b3141a76` |
| `tests/performance/foundry_l1.py` | `7f90695897cb4056b290f3ff79d414aa274469824b5e7f2155f10cd82679fc3c` |

**PENDING/operator:** authenticate a real principal, derive verified owner scope,
rebuild extraction/plan identities under that scope, and finalize the complete
private `LaunchConfiguration`. The configuration includes current commercial
catalog, quota/authority policies and locations, times, actual model path/hash,
OIDC settings and target. Its digest is `sha256(config.model_dump_json().encode())`.
No such complete digest is asserted here; no fake final JSON was created.
Only afterward can `foundry_approval.bindings(config, verified_principal, digest)`
produce the actual unsigned approval binding. A managed-settings fingerprint is
not the complete launch-configuration digest. Old v3, pre-G1 v4 or single-analysis
requests/checkpoints cannot be relabelled or resumed under this contract.

## 6. Current offline readiness evidence

Disposable scripts, logs, JSON and JUnit are outside Git at
`/tmp/phase17h-operator-preparation-20261102/`. The durable model manifest also
remains beside the model tree. Scratch evidence is not an authority or final packet.

| Executed check | Actual result |
| --- | --- |
| Current Git and GitHub CI metadata/job inspection | PASS; clean initial tree, exact HEAD, successful run/job/steps. |
| `prepare_offline.py` | PASS; two identical fresh plans, four canonical source pieces, one chunk/two reducers/five job steps, zero inference calls/network attempts. |
| Configured chunk render-only probe | PASS; correct managed configuration binding, 11,626 admitted input, 3,000 output; zero inference/network calls. |
| `preserve_model.py` | Exit 0; exclusive durable local copy, exact inventory/per-file/tree verification, permissions/capacity/fsync. |
| `verify_local.py` | Exit 0; actual CPU model, launcher local factory, scratch Chroma, negative hash/link checks, unchanged content, zero network attempts. |
| Selected existing offline pytest cases | **3 passed, 1 existing JUnit `record_property` warning, 2.30 s**, exit 0; zero failures/errors/skips/network attempts. |
| `check_decimal.py` | PASS; three exact arithmetic vectors, aggregate fixed/extra counted once, float/bool money rejected; no authority access/reservation. |
| `python -m compileall -q .` with external bytecode cache | Exit 0. |

The targeted command was:

```bash
PYTHONPATH=/tmp/phase17h-operator-preparation-20261102:. \
PYTHONDONTWRITEBYTECODE=1 PYTEST_PLUGINS=offline_guard,observe_envelopes \
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
python -m pytest -q -p no:cacheprovider \
  tests/integration/test_phase17hl_offline_e2e.py::test_l1_extraction_dag_schema_digest_citations_accounting_and_reopen \
  tests/unit/documents/test_managed_sizing.py::test_render_rejects_removed_policy_before_inference \
  tests/unit/publication/test_analysis.py::test_escaped_evidence_and_annotations_use_complete_governed_envelope \
  --junitxml=/tmp/phase17h-operator-preparation-20261102/targeted.xml
```

The E2E case exercises real application validators, durable reopening, publication,
retrieval/citations, four fake HTTP calls and synthetic settlement/reuse. The
observer only records envelopes and delegates unchanged decisions. No approval
signing/consumption tests or live launcher were invoked. Existing test settings
isolation suppresses dotenv before application imports. Plan/model probes install
the same isolation. HF/Transformers offline flags and Python socket/DNS-denial
guards were enabled for plan/model/pytest work. Zero observed attempts is a
Python-process observation, not an OS firewall certification.

Installed versions used: sentence-transformers 5.5.1, Chroma 1.5.9, Torch 2.12.0,
Pydantic 2.13.4. Two existing encoder-method rename FutureWarnings occurred;
both model operations succeeded. Compilation used
`PYTHONPYCACHEPREFIX=/tmp/phase17h-operator-preparation-20261102/bytecode`.
No Python implementation changed, so no new production tests or lint-driven
refactors were added. Full pytest and local Docker/Compose/Helm checks were not
repeated: the exact checkpoint's CI already verifies them. No Kubernetes operation
was performed.

## 7. Azure, capacity and financial prerequisites

The [launcher schema](../../../tests/performance/foundry_l1.py) currently restricts
resource `epolymind-foundry-dev-susanta`, served deployment `epolymind-gpt-54-mini`,
model `gpt-5.4-mini`, version `2026-03-17`, SKU `GlobalStandard`. Its v1 endpoint
allowlist and general/summarization role mapping are source-verified. This does
not verify what Azure currently serves. No authenticated Azure discovery or
inference request was made.

| Required current evidence | Status and required operator verification |
| --- | --- |
| Target/model/version/SKU/region and endpoint | PENDING; confirm actual deployed model, response aliases, current SKU/region and access. Do not substitute another deployment or probe via paid inference. |
| Actual RPM/TPM and shared consumers | PENDING; obtain timestamped deployment/shared-pool allocation and usage evidence. Public defaults and historical 30K observations are insufficient. |
| Valid inference credential | PENDING; selected `api_key` or `entra_bearer`, correct target/audience/access, attested validity covering the window; no credential inspected here. |
| Existing security/governance/admission authorities | PENDING; existing approved paths/policies/quota key, registered/enabled principal, no replacement ledgers. |
| Current EUR catalog | PENDING; applicable commercial agreement/source, date, region, Global Standard model/version and served-deployment lookup; positive input/output decimal rates and unit. |
| Additional charges | PENDING; bound applicable fixed/incremental charges, storage/network/monitoring, taxes and currency conversion where applicable; evidence is required even for a zero charge conclusion. |
| Remaining financial/token headroom | PENDING; existing owner and tenant daily/monthly balances, other consumers, reserved/unknown obligations across periods, actual billing/reconciliation evidence. |
| Independent approval/trust/replay/window | PENDING; see section 8. No current usable window is established. |

Current public [Microsoft quota guidance](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/quota)
describes deployment allocation and affiliated deployments using shared quota.
It does not attest this target's actual capacity. Public pricing-page requests
to the current and legacy Azure OpenAI pricing URLs both timed out in the browser
tool. No applicable current EUR quote was recovered; search-result/historical
rates were not adopted. The operator must supply the current applicable catalog
and independently approved cost evidence. No cloud change is proposed to resolve
capacity gaps.

Retain these engineering/financial ceilings without enlargement:

- At most **four calls**; per call **25,000 input / 3,000 inclusive output**;
  cumulative **100,000 input / 12,000 output**. Reasoning is within completion
  usage, not an extra output allowance.
- Full managed/Q&A rendered input limit 24,800, plus 100 overhead and 100 safety;
  conservative context 28,000. Actual usage remains separately validated.
- **Zero automatic paid retries**, worker `max_attempts=1`, bounded transport one
  POST, live readiness retries zero, no fallback/repair loop.
- **One outstanding inference call**, run RPM 1, minimum **61 real seconds between
  starts**. Candidate shared admission is RPM 2 / TPM 30,000, with at least
  2,000 interactive TPM, one interactive RPM/slot, per-job RPM/concurrency 1.
  Larger existing reserves and stricter actual policies win. With full 28,000
  request allowance, background capacity must also retain that shared reserve;
  verify actual allocation and all consumers before approval.
- Approved exposure `M` must satisfy **0 < M <= EUR 5**, subject to actual remaining
  owner/tenant headroom and all charges. This task grants **EUR 0** spending
  authority. A EUR 5 policy limit is not a fresh EUR 5 available balance.

The exact decimal upper-bound method, for positive current EUR rates `ri`, `ro`
per decimal-power unit `U` and aggregate fixed/extra bounds `F`, `E`, is:

```text
per-call tokens = (25,000*ri + 3,000*ro) / U
four-call tokens = (100,000*ri + 12,000*ro) / U
run upper bound = four-call tokens + F + E
require run upper bound <= M <= EUR 5
also require sufficient existing owner/tenant headroom and token/rate capacity
```

[Price.cost](../../../governance/ledger.py) uses Decimal with precision 60;
[Contract.cost/fits](../../../tests/performance/foundry_budget.py) checks the
aggregate call count, token and monetary ceilings. Three arithmetic-only vectors
matched independently calculated 60-digit Decimal expectations exactly, including
12-decimal rates and nonzero aggregate extras. Example synthetic rates
`ri=1.234567890123`, `ro=4.567890123456`, `U=1000000`, `F=0.012345678901`,
`E=0.098765432109` produced **0.289382581503772** exactly. This is an arithmetic
witness, not a current price quote or approved catalog. Floats/bools were refused.
Recalculate with the actual validated monetary strings; do not round after review,
assume cache discounts, count reasoning twice or multiply aggregate extras by four.

Governed execution durably reserves before inference and settles known actual
usage even when later domain validation rejects output. RunGuard retains full
per-call ceilings and blocks unfinished/unknown work; no refund buys a fifth call.
Existing UNKNOWN obligations must be reconciled by the operator. Historical
Attempt 6 catalog cost cannot establish current headroom or an Azure invoice.

## 8. Security and independent approval requirements

**PASS/source:** identity authentication, existing application permissions,
financial/governance admission and independent operator approval are separate
gates. **PENDING/operator:** all actual identity, credential and authority state.

Use the existing OIDC verifier and security authority. Under Entra v2, verify
issuer/audience/tenant/signature, delegated `access_as_user`, exactly
`PolyMind.L1Operator`, exact verified subject/derived owner scope, expiry and
registration. Do not obtain identity by unverified JWT decoding. Publication
requires `PUBLICATION_MANAGE`; digestion uses its existing `DOCUMENT_DELETE`
authorization snapshot, Q&A `DOCUMENT_ANALYZE`, and usage audit its existing
permission. Revalidate rather than changing authority policy. Runtime secrets
remain separate `POLYMIND_L1_OPERATOR_TOKEN` and `POLYMIND_L1_AZURE_CREDENTIAL`;
neither was read or tested in this task.

Independent approval uses the existing pinned RSA public trust, 2048–8192 bits,
verified provenance and exact operator issuer/subject/tenant. Trust must not come
from the approval's unverified header, embedded key or sender-selected URL.
Approval and trust must be `purpose=live`; full L1 audience is
`polymind-l1-live`. Single-analysis approvals use a different audience and cannot
authorize this evaluation. No signing key or approval artifact was opened or made.

The exact configuration digest/acknowledgement and complete unsigned binding
must match the independent review: identity/scope, target/model/version/SKU/region,
prices/charges, ceilings, authority policies/locations, model tree and times.
Only the separately authorized operator may subsequently decide whether to sign.
Fresh canonical UUID approval ID and RS256 protected header rules remain unchanged.

Persistent replay storage is independent of the audit directory and survives
key rotation. Exclusive consumption records, file/directory fsync, independent
`live-started.json` and durable call records guard replay. **Consumption precedes
local embedding setup**, so model/storage checks must precede any future launch.
Do not delete markers, switch replay directories, replace authorities or issue a
new approval merely to bypass outstanding work. Protection assumes the established
trusted single host; it is not distributed/hostile-administrator protection.

The permitted future start must satisfy `now >= execution_not_before` and
`now < min(approval_expires, credential_valid_until) - 600 seconds`; equality at
the cutoff is ineligible. Configuration requires a compatible interval and more
than 600 seconds remaining. Signature `iat <= nbf < exp`, issue-to-expiry at most
86,400 seconds, expiry equal to configured approval expiry. Fresh operator token
must have more than 60 seconds remaining at verification; runtime rechecks the
earliest principal/approval/credential deadline with a 60-second margin and
cancellation before later work. Allow time for all four calls, pacing and local
work; do not assume a historical window remains valid. Times are authoritative UTC.

## 9. Execution safety and live acceptance evidence

Source inspection confirms explicit failure paths stop or prevent downstream
inference for failed/mismatched/expired authentication or approval, revoked
authorization, admission/financial denial, provider refusal/error/429/timeout,
invalid protocol/JSON/schema/domain output, missing evidence/child links, size or
usage breach, settlement failure, checkpoint/fence/dependency failure, and
publication/replica/citation exceptions. Preserve original errors and known costs;
unknown accounting remains outstanding. Cancellation also stops continuation.

The composition uses local CPU embeddings/Chroma and no tools/cloud reranker.
An unexpected paid dependency invalidates this reviewed scope and requires a stop;
the launcher is not a universal detector of arbitrary new paid dependencies.
No automatic replay, fallback, retry, paid repair, budget enlargement or replacement
authority recovery is permitted.

**Acceptance limitation:** `DocumentAnalysis` can return local insufficient
evidence without a model call; the harness can label a schema-valid abstention
`questions.status=COMPLETE`. This is existing documented behavior, not evidence
that the answerable fixture succeeded. An exception-free launch or COMPLETE
question status alone cannot certify the required four-call milestone. Do not
manufacture an extra call to fill a short run. Wrong semantics discovered after
the calls invalidates acceptance; it cannot undo already incurred charges.

Accept the separately authorized live experiment only with all of:

1. Frozen source/configuration/publication provenance, valid independent approval
   and preserved one-use/replay evidence for this exact four-call scope.
2. Exactly four provider attempts in order chunk → structural → root → Q&A;
   zero retries/fallbacks; all usage known, bounded and successfully SETTLED,
   no accounting failure or unresolved new obligation, and additional charges
   reconciled against approved evidence.
3. Workflow `COMPLETED`, digest **COMPLETE**, coverage fraction **1**, all four
   eligible source pieces covered, every child claim linked, immutable checkpoints
   reopened/revalidated and final digest/coverage persisted.
4. Successful authorized publication prepare/activation, ready replica, pinned
   document/version/generation, original-source retrieval and canonical citations.
   Generated annotations remain distinct from original evidence.
5. Correct page-one valve-5153-before-operation answer with valid original
   citation(s), no unsupported conclusions or instruction-injection compliance.
6. Independent human review packet records factual entailment, page/excerpt
   accuracy, qualifications/contradictions, abstention correctness, disagreements
   and reviewer judgment. Structural validation does not establish semantic support.

Retain distinct provider, application, digest, publication, answer and accounting
outcomes. Q&A failure does not erase an already accepted digest or settled cost.
Even a successful four-call fixture does not establish multi-chunk live quality,
representative-corpus reliability or production readiness.

## 10. Outstanding operator actions in dependency order

These actions are a handoff, not authorization to perform protected work here.

1. **Verify the real operator identity through the existing approved verifier**
   under operator-controlled access. Confirm current registration, exact scope,
   permissions and identity lifetime; do not fabricate a principal.
2. Inspect existing security/governance/admission policies and retained obligations
   through the approved read-only workflow. Reconcile unknown/outstanding work and
   establish actual owner/tenant financial and token headroom. Preserve authorities.
3. Obtain fresh timestamped target/model/version/SKU/region, inference-credential
   validity, RPM/TPM/shared-consumer attestations and applicable current EUR
   commercial catalog/additional-charge evidence. No paid probe or cloud mutation.
4. Calculate exact Decimal exposure with those rates/charges and choose a ceiling
   no greater than EUR 5 and actual available headroom. Verify shared reserves and
   paced four-call feasibility under existing policy. Resolve gaps before approval.
5. Review/pin the preserved model's absolute directory and tree hash. Verify new
   durable private audit/object/job/publication/vector storage, permissions/capacity,
   retention, existing independent trust and persistent replay directory. Reuse
   existing trust; do not reprovision keys or authority databases.
6. Rebuild the fixture/extraction/plan under verified actual scope with current
   frozen source; confirm exactly one chunk/two reducers and four total calls.
   Finalize fresh permissible timestamps, complete validated private configuration,
   exact digest and unsigned `bindings()` output. Preserve all actual review artifacts.
7. Submit the complete private packet and this report for independent review.
   Recheck source, financial evidence, identity and window immediately before any
   later decision. **Signing and execution require separate explicit authorization
   and are outside this task.** No signature, consumption or launch is recommended
   while any prerequisite remains pending.

No missing model, dependency or current application defect blocks that preparation
sequence. The unresolved private/cloud evidence blocks final approval and live
execution, rather than requiring an application redesign.

## 11. Self-review, separate pre-commit review and final repository state

Implementation self-review checked actual launcher selection, G1 binding/admission,
source evidence and lineage, durable accounting, local model integrity/resource
cleanup, exact plan dependencies, approval/window/replay constraints, and the
acceptance limitation above. No code correction or scope expansion was justified.

Separate pre-commit review covers the complete two-file addition, relative links,
whitespace, credentials/private-key markers, generated artifacts, unrelated changes,
claims of current private/cloud verification and unintended API/dependency changes.
Only this report and its normalized prompt belong to the repository deliverable;
all scripts/logs/databases/bytecode/models remain outside Git. Home-relative model
and scratch paths document measured artifacts, not application configuration
defaults or private authority locations. No real dotenv, credentials, signatures,
private configuration or upstream responses were copied into documentation.

Final `git diff --check` exited 0. Explicit new-file whitespace/high-signal
credential checks passed, all **14 relative file links resolve**, measured report
bindings agree with generated evidence, and supplemental source hashes remain
unchanged. Read-only `git status`/`git diff --stat` verified the final inventory.
The final status is two untracked Markdown deliverables; tracked and staged diffs
are empty. Ordinary `git diff --stat` therefore prints nothing and excludes these
new files. No stage, commit, push, reset, clean or branch switch occurred.

## 12. Recommendation, authorization status and exact next action

| Independent classification | Result |
| --- | --- |
| Engineering readiness | **GO** for the existing four-call operator preparation scope. |
| Operator preparation | **READY WITH GAPS**; actual private packet/current external prerequisites remain pending. |
| Live execution authorization | **NOT AUTHORIZED**; this report grants no permission or spend. |

**Exact next recommended operator action:** authenticate the real operator using
the existing approved verifier and confirm current authority registration and
scope through the operator-controlled read-only process. Then follow steps 2–7
above. Do not sign or launch from this report. Final authorization and every Git
operation remain the repository owner's responsibility.
