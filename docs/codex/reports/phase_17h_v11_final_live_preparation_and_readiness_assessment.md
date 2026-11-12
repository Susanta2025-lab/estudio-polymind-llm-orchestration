# Phase 17H v11 final live preparation and readiness assessment

12 November 2026 UTC. **TECHNICALLY_PREPARED_PENDING_OPERATOR**. This task prepares an unsigned, non-executable candidate. No status here permits RSA signing, credential use, approval consumption or paid inference. Real v11 semantic improvement remains **NOT_YET_VERIFIED**.

## 1. Verified baseline and preservation

Branch is `master`; HEAD and local `origin/master` are `ec22fa3d116696b80a1bb12ad17e2eb37db38cb3`, the supplied successful v10 commit. Initial state is exactly **14 modified tracked files, 48 untracked files and zero staged files**. Counts use expanded `git ls-files --others --exclude-standard`, not collapsed directory entries. The previous checkpoint was verified rather than assumed. Initial Git status, binary diff, statistics and SHA-256 values for **556 existing nonignored regular files** were preserved in the private temporary preparation directory. No reset, stash, clean, overwrite of historical evidence, stage, commit, push, branch switch or history/remote mutation occurs.

Read and reconciled AGENTS.md; the [live evaluation history](../../evaluation/phase_17h_live_attempts_root_causes_and_engineering_evolution.md); [v11 quality assessment](../../evaluation/phase_17h_v11_reducer_quality_and_closure_assessment.md); [v11 offline implementation](phase_17h_v11_reducer_semantic_quality_implementation.md); v10 [execution](phase_17h_v10_controlled_four_call_evaluation_and_reconciliation.md), [confirmed packet](phase_17h_v10_confirmed_operator_packet_and_rsa_signing_handoff.md), [authentication renewal](phase_17h_v10_authentication_renewal_and_final_operator_packet_preparation.md), [operator readiness](phase_17h_v10_operator_preparation_and_readiness_assessment.md), [RSA verification](phase_17h_v10_rsa_signing_and_independent_verification.md); [readiness](../../evaluation/phase_17h_readiness.md); approval, Entra, financial migration, provider and preflight documentation. Implementation review covered the specified managed/sizing/wire/workflow/validation/receipt modules, launcher/preflight/approval/single-call composition, source fixture, generation contracts and G1/G2/security/governance regressions.

The 25-member historical inventory, reconstructed from unchanged committed blobs and hash-pinned v10 source fixtures, still reproduces **`e5fb249cc9b166b5e438f1534eb855fa5ab7531e08aa09314c110a1905327ebd`**. Its prompt remains `managed-prompt/10`, inventory `generation-inventory/2`. Historical configuration remains `8e0be5429ea1e8c991338508c8b56731aa7a4ceec2ae662502236ef81c7d1e5b`. The successful four-call result, accepted checkpoints, nine manifest objects, G1/G2, publication, grounded Q&A and EUR 0.010707841465063252 token settlement remain historical observations. The original reporting discrepancy is preserved in historical `result.json`; its existing corrective source line and regression assertions remain in the working tree.

Original v10 private execution artifacts at the report's `/tmp` location are absent here. No consumed signed approval was loaded, reconstructed or repurposed. Preservation of unavailable raw/checkpoint/receipt evidence means non-access and unchanged retained reports, not a claimed fresh cryptographic reopening. Current financial authorities and replay markers are available and were inspected separately read-only. The historical v10 consumption marker exists; its authority is exhausted.

## 2. Source generation and launcher correction

Before this task's edits, production inventory/2 aggregation over captured starting bytes reproduces the reported v11 hash **`072aa2cd2a3be2ddb8e63b0577119e87312f44613c9532b56b6d6d9c5ff78fba`**. The protected L1 composition did indeed construct default v10 StageProfiles. Selecting v11 in test monkeypatches did not solve that production-launch configuration gap.

The smallest addition is `LaunchConfiguration.managed_prompt_version`, a literal accepting only `managed-prompt/10` or `managed-prompt/11`, defaulting to v10. Explicit v11 is serialized into the canonical launch configuration and therefore its signed configuration digest. Default v10 omits the new field during serialization, retaining the established default shape. Changing/removing reviewed v11 selection changes the digest; no existing v10 signed source binding becomes valid for this changed source.

`foundry_preflight.execute()` obtains the selected version from `runtime.config` and explicitly passes it to **all four** profiles: chunk, intermediate, structural and root. Supplying a separate runtime template override is rejected before authority/source access. The optional offline `template_version` argument supports a deterministic rehearsal without runtime authority. It has no live CLI flag or authority meaning. Existing `ManagedSettings` rejects mixed versions. Unknown versions fail schema validation. The default offline CLI remains v10; a v11 rehearsal must explicitly select v11 through the supported function argument.

Only two inventoried sources change relative to the preceding v11 checkpoint:

| Source | Prior SHA-256 | Prepared SHA-256 |
| --- | --- | --- |
| `tests/performance/foundry_l1.py` | 2caa28a07b09afac95bf91e23048ce33ed993dcb91269784bc58b44fd0e154af | ea629d70812f74fa574f8694dc425e260440e713cc8b228d0470e2218a4504e7 |
| `tests/performance/foundry_preflight.py` | 64eab823cb076ba05961fdbd1de09d3c66c13fd9a41ef04574d6d5cc57620f2a | 60445a72062594b6907cdb4a6bb865ae618affdc947fe8f800f8bb7747cbbf6d |

The freshly recomputed production generation fingerprint is:

```text
c9e1ea9d3be00e8f459be9f3a0693ab11429813b355d1f341b63510d41fa6b2c
```

The active v11 fixture updates only those two source hashes and the aggregate generation hash. Existing request/generation/transport witnesses remain unchanged and are validated against actual rendering. The preceding v11 JSON fixture is preserved byte-for-byte as `managed_prompt11_offline_implementation.json`, verified against its initial file hash. A new frozen `v10_sources/tests/performance/foundry_l1.py.txt` exactly matches the committed historical launcher, so historical inventory reconstruction does not read its changed working-tree replacement. No old hash is forced and no historical v10 fixture/report is edited.

V11 uses the intended reducer instructions, while chunk task prose retains its semantics. Both versions use strict `stage-proposal/1`, deterministic application-owned canonical `stage-result/1` identities, the same validator and receipt contracts, and three-object manifests. Source/configuration identity makes v10 checkpoint reuse under v11 incompatible. No provider-specific inference logic enters graph/API/UI/RAG; no dependency, runtime, endpoint adapter, validator, planner, security or financial authority implementation changes.

## 3. Fresh Azure observations and exact target

Read-only Azure CLI queries confirmed the enabled AzureCloud account, the established subscription pin in the billing lookup and the following current management facts on 12 November:

| Field | Fresh observation |
| --- | --- |
| Resource | `epolymind-foundry-dev-susanta` |
| Resource group / kind | `rg-epolymind` / AIServices |
| Region / provisioning | `spaincentral` / Succeeded |
| Deployment | `epolymind-gpt-54-mini` / Succeeded |
| Model / version | `gpt-5.4-mini` / `2026-03-17` |
| Deployment SKU / capacity | GlobalStandard / 30 |
| Allocated requests / tokens | 30 per 60 seconds / 30,000 per 60 seconds |
| Candidate API | Azure OpenAI-compatible v1 Chat Completions |
| Exact candidate base URL | `https://epolymind-foundry-dev-susanta.openai.azure.com/openai/v1` |
| Exact chat route | `/openai/v1/chat/completions` |
| Intended authentication | `api_key`, production `api-key` header |

Resource `properties.endpoint` is the generic `cognitiveservices.azure.com` URL. It is **not** silently substituted into the launcher. Resource `properties.endpoints` explicitly declares the exact named-resource `openai.azure.com` host for its OpenAI model API; its custom subdomain matches the resource. The configured project endpoint is the same exact OpenAI base URL above and passes `deployment_configuration()` with both logical roles mapped to the named deployment. No similar-looking alias is used. The generic primary URL alone would not pass this allowlist. Management proof does not prove the availability or acceptance of the v1 chat route and new strict request at data plane; no probe was sent.

The first management command hit sandbox restrictions while Azure CLI attempted its local command log. It was rerun through the execution system's approval mechanism. Subsequent permitted management and Consumption requests were read-only; no deployment, quota, permission, resource, AKS/Kubernetes or key mutation occurred. No key retrieval, rotation or inference-based credential test occurred. Deployment verification is current; refresh it again near any actual future window.

## 4. Admission, consumers and hidden-call review

The current provider authority has **zero active admissions** and its stored policy is exactly **2 RPM, 30,000 TPM, two slots**. Interactive reserve remains **one RPM, one slot and 2,000 TPM**; per-job RPM/concurrency remains one. Stored policy binding passes the existing evaluation-authority/path/key/hash checks. Deployment allocation accommodates this policy without increasing any limit.

Future controlled limits remain four calls total, 100,000 aggregate input and 12,000 aggregate output; per-call guard maxima 25,000 input and 3,000 output; managed input 24,800; context 28,000; evaluation concurrency one; provider starts at least 61 seconds apart. Sequence is exactly chunk → structural → root → grounded Q&A. The configured intermediate profile shares v11 identity but this bounded plan needs no intermediate call.

The launcher provider uses `readiness_retries=0`, one direct structured request per managed stage and no structured-output negotiation/probe. Job retry policy has `max_attempts=1`; the sticky RunGuard blocks continuation after failed/unknown provider usage, budget/admission denial or external stop. Grounded Q&A has one case and breaks on failure. No LangGraph retry/agent/tool loop participates. Local pinned embeddings and explicit deterministic reranking add no cloud calls. Recovery validates durable evidence; this task neither initiates recovery nor treats unused allowance as retry permission. Failed/partial jobs do not publish or reach Q&A; the CLI exits nonzero for incomplete digestion/Q&A. The inherited post-Q&A `billable_calls` refresh is retained and tested.

Local zero-active observation is **not** exclusive control over Azure playgrounds, external scripts, other sessions/accounts or remote consumers. No current v11 exclusivity attestation exists. Provider quota/consumer gate is therefore **PENDING**. Known historical stopped workloads are not relabeled fresh checks. Reverify local admissions and all shared consumers for the eventual interval without weakening interactive reserve.

## 5. Current governance, pricing and exact financial proposal

Security, governance and provider SQLite files were inspected using URI `mode=ro` with `PRAGMA query_only=ON`; integrity checks return `ok`. No production authority constructor, authorization snapshot, reservation, event writer, settlement or policy/catalog mutation was called. Registered scope comes from existing private records, not fabricated identity.

The persisted policy is `phase17hl-l1/2` with a `polymind-evaluation/1` scoped overlay. `QuotaPolicy.select(registered_scope)` chooses the overlay: 16 requests per rolling 86,400 seconds, 500,000 daily tokens, 1,500,000 monthly tokens, 112,000 outstanding tokens and EUR 5 monthly accounting ceiling, for both owner and tenant. Reading only base fields would incorrectly report five requests and 115,305 token quotas. That preliminary diagnostic was corrected through production selection and `governance.evaluation.impact()` without changing any policy.

Fresh owner and tenant balances each are **12 rolling requests, 500,000 daily tokens, 1,452,089 monthly tokens, 112,000 outstanding-token capacity and EUR 4.913052591409009628 monthly headroom**. The daily reset explains the difference from v10's post-run daily snapshot; its four calls are still inside the current rolling interval. There are **17 SETTLED reservations, zero outstanding obligations**; provider admissions are inactive. A full 112,000-token maximum and four requests fit both selected scopes. No capacity or money has been reserved for v11.

The authoritative catalog remains `phase17hl-pricing-eur-202611/1`, effective 7 November, SHA-256 `59c90a122e3db199848ae0817218bc4286bab80b22920a0916d8f5a54426dd37`. Current project `.env` still contains the older October catalog. **Do not build a new launch configuration from that stale pricing value**: use the reviewed authoritative current catalog and exact production validation; do not silently synchronize or edit `.env` under this task. The protected launcher reads its private LaunchConfiguration and checks equality against shared authorities, so a stale catalog would fail closed. The mismatch is an outstanding operational configuration binding, not permission to migrate/reprice anything.

Fresh Azure Consumption usage-details read completed **10:02:10 UTC**, with complete pagination and eight exact-resource meter rows. Modern usage records identify the resource through `instanceName`, not the older `resourceId` shape. The initial resourceId-only filter returned zero matches; inspecting the established modern schema corrected that diagnostic. Zero matches were not treated as zero spend. Sanitized output contains no credentials or private billing-account identity.

The latest resource/day rows include the v10 **5,854 input / 1,675 output tokens**. Input/output unit prices are **USD 0.75 / USD 4.50 per million**, pricing-to-billing conversion **0.897706360249562 EUR/USD**, exchange-rate date 1 November. Upward rounding of their exact Decimal products to twelve places reproduces the active EUR catalog rates. Current billing total for 11 November is EUR **0.01070784146505678**, versus historical settled catalog EUR **0.010707841465063252**; the tiny upward catalog-rounding difference does not justify repricing. Previously documented October-versus-November conversion differences remain historical and unchanged. Delayed usage is not a final invoice or proof that no other charges/consumers exist.

Two separate Decimal computations (precision 60), one directly from catalog values and one from fresh meter/conversion evidence, agree:

| Component | Proposed EUR |
| --- | ---: |
| 100,000 input at 0.673279770188 per million | 0.0673279770188 |
| 12,000 output at 4.039678621124 per million | 0.048476143453488 |
| Maximum catalog token exposure | **0.115804120472288** |
| 23% VAT budgeting allowance on tokens | 0.02663494770862624 |
| VAT-inclusive network contingency | 0.10 |
| Aggregate extras, rounded upward to 12 places | 0.126634947709 |
| Fixed incremental cost in the candidate scope | 0 |
| Forecast including rounded extras | **0.242439068181288** |
| Smallest covering 12-place configuration ceiling | **0.242439068182** |

The final ceiling covers forecast by EUR 0.000000000000712 and fits the current EUR accounting headroom. VAT is a budgeting assumption, not an invoice-tax determination; EUR 0.10 is contingency, not an Azure hard network cap. Reasoning output stays inside completion-token accounting and is not charged twice. The addition changes local configuration selection only; it introduces no new chargeable service or cloud embeddings. EUR 0 fixed costs remains a proposed scope assumption, including prior exclusions for unrelated unchanged services and personal/local operating costs. Its v11 acceptance and current-window applicability need explicit operator confirmation. No historical financial permission is carried forward.

Financial gate is **PENDING**: exposure is calculated and current accounting headroom fits, but positive v11 acceptance, VAT/network/exclusion scope and charges verification for an actual future window are unresolved. A EUR 5 balance is neither spending permission nor a cloud spending cap. Financial acceptance, RSA-signing authorization and paid-execution/consumption authorization remain separate decisions.

## 6. Operator, credentials, trust and time

The existing private security authority contains one enabled user registration with `PUBLICATION_MANAGE`, Principal epoch zero, and one ACTIVE controlled document at epoch zero. Its stored owner/tenant scope matches the evaluation overlay. This is a read-only registration observation, **not a currently authenticated Principal**. No historical access token was loaded or decoded to fabricate one. Current Graph account enablement and signed-OID-to-Graph correlation remain **NOT_VERIFIED** until fresh operator authentication.

The established user-controlled MSAL device-code utility exists in the operator's `auth-tools/entra_device_login.py`. It requests the pinned API's delegated `access_as_user` scope using the existing public client and tenant, and explicitly warns that application verification remains separate. Its standalone default persists a token file; it was inspected but **not invoked**, because this task forbids token persistence and unattended login. The v10 protected in-memory/anonymous-pipe procedure, followed by `OIDCVerifier.verify()`, is the appropriate established handoff to reproduce later under direct operator control; its original transient v10 dispatcher is unavailable here. Do not substitute an unattended CLI login or run the persistence-oriented utility unchanged. The later procedure must preserve in-memory transfer and validate trusted JWKS/RS256, exact tenant/issuer/API audience, integer iat/nbf/exp, delegated scope, exact role, signed OID/Graph account, stored Principal/scope and document authorization/epochs. A management token is not an application or provider inference credential.

The protected project `.env` is a regular nonsymlink mode-0600 credential-source file; its configured provider endpoint matches the exact resource host. No key was retrieved from Azure, copied to a new file, logged, rotated or tested. Presence of a key cannot prove its original issuance or current data-plane acceptance. The v10 provider-use permission ended **11 November 21:50 UTC** and the successful application token expired **11 November 21:52:02 UTC**. Both are historical and expired. V11 credential status is **PENDING_OPERATOR_CREDENTIAL_AUTHORIZATION**; data-plane acceptance remains **NOT_VERIFIED** and must not be tested by a separate paid probe.

Production `load_trust()` successfully reopened only the independently provisioned **public** live trust, with its protected external replay path. Its RSA-3072 public component matches the separate operator-public PEM: key ID `polymind-l1-35785596dd2f38a3`, DER SHA-256 **`35785596dd2f38a3ae5fc8eeb93015a1ba3c8b4f16f06a1d73fbe521f9657816`**. There are **11 consumed markers**, including v10's consumed UUID; their hashes were recorded and preserved. No private RSA file/passphrase was opened, no production signature/new signed artifact was created or verified, no approval identity was allocated and no marker was consumed. Fresh authenticated Principal-to-trust association remains pending even though public-file correspondence passes.

No future date/window was supplied: **EXECUTION_WINDOW_PENDING_OPERATOR**. No historical cutoff/deadline is reused, no early authentication is started and no expiry is invented. Future launch must be strictly before the earliest allowed cutoff, preserve the production more-than-600-second approval/credential gate, and retain the documented 20-minute practical margin across actual token, credential and approval deadlines with the conservative one-second cutoff convention. Attest shared consumers through the entire configured interval. Resolve timing before requesting fresh authentication to avoid needless expiry.

## 7. Exact source, managed configuration and G1/G2

Production extraction and pure `workflow.prepare()` used the original bounded fixture and stored registered scope in an isolated disposable object store. No Principal was synthesized, document registered, job admitted, provider slot acquired or production vector store changed. Reopening the plan through the production codec equals an independent `build_plan()` reconstruction. These objects are preparation data, not authenticated execution authority.

| Binding | Fresh value |
| --- | --- |
| Source / pages | `phase17h-pdf/1`, seed 1708, four pages, 3,537 bytes |
| Source SHA-256 | `1be99e19a56040fb55c74682a19f874d4d4573f18d9f52a9a7ae19c8158ea92d` |
| Extraction SHA-256 | `b7410e987c6658c596399d4bccce4b6e11ec07cc95f29ab1c56eb2b7f011fcd1` |
| Registered-scope candidate v11 plan SHA-256 | `c22d6675d7fb3888c071923afaea92f967e4852d034a394596be79057b4fc583` |
| Actual proposed managed-settings/config binding | `537f4190dce4f3bda8cb9cea4794f4a0ce223acbb224389e22abd6002ba4d3ef` |
| Complete canonical LaunchConfiguration SHA-256 | **NOT CREATED; mandatory actual bindings unresolved** |

The managed configuration above uses the actual deployment model identity and full production settings, not the earlier offline fixture's synthetic model configuration hash. It still is not an approved operational LaunchConfiguration. Source/scope authentication must be reconfirmed against the eventual actual Principal; a mismatch requires a new plan, never patching its hash.

Actual first-chunk rendering measures **2,937 system bytes, 1,917 data bytes and 2,423 canonical schema bytes**, a complete escaped request envelope of **7,485** conservative units, plus 100 overhead and 100 safety: **7,685 input / 10,685 complete context** with 3,000 output reserved. Strict schema conversion and transport request validation pass offline. Task-owned identities and exact source membership remain mandatory.

All four selected profiles share v11. The fixed planning base remains **6,990** bytes, compared with v10's historical 5,502. Each of the actual plan's structural/root reducers has one immediate child and empty structural path. The complete-child reservation is 7,000, yielding **13,990** conservative serialized input units, **14,190** including overhead/safety and **17,190** complete context. This bounds unknown future accepted child material, including wrappers, escaping, qualification/conflict metadata and lineage contributions. It does **not** assume that future model output has the size of a fake example. Runtime still independently admits each complete request and result, rejecting oversize/invalid output terminally.

Unchanged independent limits are managed input **24,800**, provider context **28,000**, output **3,000** per call, overhead/safety **100/100**, complete child contribution **7,000 bytes**, raw UTF-8 proposal **10,000 bytes**, canonical ASCII result **10,000 bytes** and HTTP envelope **26,192 bytes**. A 10,000-byte raw/canonical allowance does not promise that a result will also fit its 7,000-byte child wrapper; each gate remains enforced. Regression tests preserve the valid original **6,867-byte** complete child. No limit was enlarged for longer prose.

G2 source-key membership, atomic immediate-child selections, application-owned stage/claim IDs, current-stage origins, no grandchild substitutions, inherited qualifications/contradictions, exact request/table binding, immutable raw records, decoding receipts, three-object checkpoint manifests, fenced ledger commits, orphan rejection, resume/replay integrity and cross-version incompatibility remain unchanged. Current publication uses newly completed digest objects, and Q&A pins/cites the same authorized source extraction. Technical acceptance does not establish relevance or entailment; independent semantic review stays separate.

## 8. Local embeddings and semantic comparison

The durable nonsymlink MiniLM tree rehashes **11 files / 91,578,415 bytes**, revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, tree SHA-256 **`96ab3cd391276cb159904c4d329318ae1f3330278a7fc0450256233cf8bb78db`**. Every file matches its stored manifest. No download, replacement, cloud embedding request or production vector mutation occurred. The future launcher requires this absolute local tree, `local_files_only=True`, CPU loading and audit-local Chroma with telemetry disabled. Hash availability is freshly verified; actual future local model/vector opening is not preclaimed. Tests use deterministic fake encoders/vector stores and isolated Chroma contract tests.

The new [frozen semantic-validation protocol](../../evaluation/phase_17h_v11_live_semantic_validation_protocol.md) inventories the four unit lists, exact 19 valve identifiers, pre-operation timing condition and untrusted page-3 line before any v11 model output. It defines structural section content versus root integration, all seven `reducer-semantic-quality/1` dimensions, support/omission/caveat criteria, automated versus independent human judgments, two-reviewer/adjudication records, stop criteria and limits on generalization. All future result/score/reviewer fields are null. No ideal summary or review checklist is fed to model prompts. V10's technical success and reducer metadata failure remain intact. Raw pairwise scoring awaits the preserved private originals and later actual v11 outputs.

## 9. Offline validation and diagnostics

The applicable full default testpaths suite exits **0**, with **2,996 passed (2,136 unit / 860 integration), zero failures, errors or skips, one warning, 738.77 seconds and zero recorded network attempts**. JUnit independently records 2,996 tests with zero failures/errors/skips. The sole warning is the existing OpenTelemetry `SelectableGroups` deprecation in the real local Chroma publication test. This supersedes, rather than adds to, the preceding snapshot's 2,991-pass evidence.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=.:/tmp/phase17h-v11-final-preparation \
/home/home/.pyenv/versions/estudio_polymind/bin/python -m pytest \
-p offline_guard -p no:cacheprovider \
--basetemp=/tmp/phase17h-v11-final-preparation/full \
--junitxml=/tmp/phase17h-v11-final-preparation/full.xml \
-o junit_family=xunit1 -q
```

Coverage includes explicit protected v10/v11 composition under both authentication modes; all-four-profile selection; canonical configuration/digest distinction; strict provider request/schema generation; one-chunk/two-reducer/one-Q&A topology; G1 raw/canonical/wrapper/context bounds; G2 membership/lineage/identity/inheritance; immutable raw/receipt associations; fenced commits, corrupt manifests, interrupted/orphan/reuse paths; cross-version incompatibility; financial failure and authentication/authorization denial; terminal output/failure handling and CLI exit behavior; corrected call accounting; new-digest publication/retrieval/citations/Q&A with deterministic fake providers. Synthetic semantic examples remain expressly separate from Azure generation and independent reviewer judgment.

Final source checks also pass: Ruff critical `E9,F63,F7,F82` across `documents`, `llm`, `tests`; default Ruff and format check for the new preparation test; whole-repository `compileall -q .` using `/tmp/phase17h-v11-final-preparation/pycache` through `PYTHONPYCACHEPREFIX`; and `git diff --check`. No dependency was installed. Full repository default lint/format cleanup is not claimed or attempted.

An initial focused invocation had **54 passes and one setup error**, because the new module imported a composition fixture without its transitive identity/signing fixtures. Explicit fixture imports fixed it; no production change was needed. The corrected focused run has **55 passed in 23.20 seconds**, zero failures/errors/skips, zero recorded network attempts. A final post-format check of the three new preparation tests also passes **3/3 in 3.10 seconds**, zero failures/errors/skips/warnings and zero network attempts; this overlaps the full suite and is not added to its count. Ruff import/fixture-registration formatting findings were corrected. A temporary preparation script initially imported a nonexistent plan type; inspection replaced it with actual `Plan` and node `path` fields before the successful production preparation check. No failed diagnostic is reported as passing.

Pre-import `offline_guard` disables external socket connect/connect_ex, connection creation and DNS before collection, allows local IPC only and fails the session if any attempt occurs. Test plugin autoload is disabled, application settings isolation precedes imports and stores are disposable. Focused counts overlap the full suite and are **not summed**. Existing security/approval tests generate ephemeral RSA keys and consume synthetic approvals in disposable stores; these are automated denial/contract tests, not production signing, private-key access or real approval consumption.

Commands and raw logs/JUnit are protected outside Git. No Azure endpoint was contacted by tests. No Docker/Compose/build/Kubernetes work is applicable: dependencies, container configuration and deployment behavior are unchanged. No mypy or model-semantic result is claimed.

## 10. Partial unsigned manifest and unresolved bindings

Protected directory: `/tmp/phase17h-v11-final-preparation/` (0700, files 0600). The following **exact review-only artifact manifest** exists; it is not a canonical signable packet:

| File | Purpose |
| --- | --- |
| `candidate-manifest.partial.unsigned.json` | Explicit PARTIAL_UNSIGNED_NON_EXECUTABLE data, known fingerprints/limits, pending values and independent decision boundaries |
| `candidate-managed-settings.json` | All four explicit v11 profiles and complete proposed managed settings |
| `candidate-plan.json` | Reopened registered-scope v11 plan, isolated from production job admission |
| `source-manifest.json` | Original deterministic page/line fixture inventory |
| `offline-observations.json` | Actual rendering, conservative reducer bounds, selected-policy headroom, public trust and embedding checks |
| `current-billing.json` | Fresh sanitized exact-resource meter/conversion rows |
| `independent-financial-review.json` | Separate Decimal calculation and unapproved exposure proposal |
| `registered-authority-bindings.pending-authentication.json` | Existing private scope/OIDC/authority/public-trust/replay pins, explicitly not an authenticated Principal |
| `validation-summary.json` | Exact full/focused offline validation counts |
| `unsigned-packet-inventory.json` | SHA-256 inventory of all nine review files |
| `future-four-call-audit/` | Empty isolated proposed future audit directory; no run marker or operational objects |

The final inventory contains these hashes (file-byte hashes are distinct from canonical managed/launch configuration bindings):

| Artifact | SHA-256 |
| --- | --- |
| `candidate-manifest.partial.unsigned.json` | `c747cc4be871f568edf9e6e2494e03eb39e8ac1eddacbadcb03a1e7bac58b713` |
| `candidate-managed-settings.json` | `2639bf814e9f2a5ec3c985c9d7855376b967cbc0d5050540e32fbe46c1ba087c` |
| `candidate-plan.json` | `c22d6675d7fb3888c071923afaea92f967e4852d034a394596be79057b4fc583` |
| `source-manifest.json` | `d3ed0802825a52d45735c97bd04dc814112412748c515b7586650bdc2d3c59dc` |
| `offline-observations.json` | `9052438f29fbe605e020936aa005bca012a508bc0ee4734e5d69a64c8a448351` |
| `independent-financial-review.json` | `78f915971e1acd1c1d38120e038819b492e4ef3ae78a5ea50e34633363bf6de6` |
| `current-billing.json` | `3cbff200a81f1c49754a253e2830e50ae5906b2dc1e5bbd71d76f988d45d6093` |
| `validation-summary.json` | `10e78f072b64eb06ffe713d477169a88f96ac74210d52ce20b2ad666a532f1c4` |
| `registered-authority-bindings.pending-authentication.json` | `4ce0cd67256adc5998ad6c092f67d9d375d913229d1b8bbcf884f8d0d8fbe3a8` |

`validation-summary.json` adds exact observed full/focused validation results. The manifest and inventory were updated to include that evidence after the suite completed; the later 3/3 post-format check is also recorded in the manifest. Existing private OIDC/authority/replay pins are retained separately without claiming authenticated identity. No authority mutation or signature was involved. The semantic protocol hash frozen in the manifest is `d631c414eaef6a29508f710dc76056df29e9d39f0a2d9b6513df0c5a28170714`.

The existing pure canonical path is `load_configuration()` → `configuration_digest()` → `foundry_approval.bindings(config, actual_verified_principal, digest)`. It was inspected, but no fabricated Principal, missing-value substitution, true prerequisite flag or expired timestamp was supplied merely to force parsing/canonicalization. No complete LaunchConfiguration, actual-Principal bindings, signing handoff, new approval UUID, signature file or executable paid-run script was created. The manifest deliberately leaves canonical configuration/bindings hashes, Principal, dates and approval identity null. Exact existing private authority/replay/registered-scope bindings are retained in the protected pending-authentication file and must be reopened and matched to the actual Principal later, not selected from public documentation. Temporary storage is review evidence, not durable authority; retain it securely if needed for a later decision.

Required unresolved inputs are: operator-reviewed commit inventory and a committed/remotely verified CI checkpoint; future UTC not-before/target/strict-cutoff/end/credential and approval deadlines; fresh direct operator authentication and Graph correlation; explicit new secure provider-credential-use permission/deadline; shared-consumer exclusivity/accounting covering the actual validity interval; positive v11 financial acceptance including VAT/network/fixed-cost/exclusion assumptions; final pricing/cloud/headroom freshness and authority equality; confirmation of retention and protected audit/replay locations; and then exact canonical configuration/actual-Principal unsigned bindings and an unused single-use identity through the established preparation procedure. Resolve stale `.env` catalog usage in the reviewed private configuration without silently mutating the environment.

After all such facts are verified, the next boundary is a **separate RSA-signing authorization decision**. Only after separately authorized signing and independent artifact verification could a different decision authorize paid execution/one-use consumption. Neither boundary has been crossed here.

## 11. Technical, security, financial and historical reviews

The technical review traced the complete starting v11 diff and this task's small addition: all explicit-version branches, compatible strict schemas, unchanged G1/G2, managed versus launch hashes, default-v10 serialization, generation inventory, checkpoint incompatibility, publication/source/Q&A association and sticky four-call terminal behavior. The new preparation path uses actual production classes; test-only monkeypatches and fake identities are confined to offline tests. No provider-specific workaround, hidden call, broader limit, API/streaming change, resource leak or runtime fallback was introduced.

A separate security/governance pass checked no private-key opening, no real signature/new approval verification, no consumed historical artifact loading, no credential values in reports, no real approval consumption/reservation/admission/authority event, no policy/catalog edit, no cloud resource mutation and no model endpoint use. Current public trust and real consumed markers were read only. Production authorities and replay/public inputs must remain byte-identical to their recorded baseline. File hashes, report links, artifact placement, secret patterns, stale TODO/debug statements, generated files, dependencies and unrelated changes were checked independently in pre-commit review. The 11 task-added/changed files have zero scanned secret-pattern findings and zero broken relative Markdown links; the packet inventory and frozen protocol hash verify. No commit is performed.

A separate financial pass recomputed price conversion, token/VAT/contingency amounts, upward serialization ceiling and comparison with the production-selected owner/tenant policy using Decimal. It distinguishes local settlement, delayed cloud usage, invoice/tax uncertainty and positive operator acceptance. The stale environment catalog is explicitly reported rather than migrated or silently treated as current.

A separate historical-integrity pass checks unchanged old reports and fixtures, exact original committed inventory, preserved prior v11 fixture bytes, existing correction lines, actual 17 settlements and 11 consumed markers without replacing old states. Original absent private audit cannot be freshly reopened; that evidence limitation remains explicit. These are distinct passes by this preparation agent, not claims of an independent human signing or semantic review.

Final preservation checks confirm **551/556 initial files byte-identical**, with exactly five intentional current-task changes to existing files: launcher, preflight, launcher tests, contract README and active v11 fixture. All other starting files, every inherited document, previous v11 implementation/report/test sources and historical v10 fixtures remain unchanged. The prior v11 fixture is additionally retained byte-identically in its separate archive. The inherited `billable_calls` line and four regression assertions remain present. All three production authority files, public trust/public PEM and all 11 consumed-marker bytes remain unchanged. The isolated proposed audit directory is still empty and zero files are staged. No historical financial row or receipt was altered.

## 12. Proposed source-control checkpoint inventory

V11 remains **UNCOMMITTED**. A source-derived generation fingerprint covers its 25 members; it does not establish a reviewed committed production revision or matching remote CI. Before signing, create an operator-reviewed exact source checkpoint and verify the same commit and required CI remotely. Local `origin/master` equals the historical baseline but is not current remote proof. No GitHub write, CI rerun, staging, commit or push is performed here.

The proposed inventory below is file-specific. Groupings distinguish the new v11 implementation, historical preservation, tests/reports and the pre-existing correction; do not blindly stage all untracked files. Some files contain more than one group's hunks and must be reviewed accordingly.

**Implementation and launch composition (seven tracked files):** `documents/digestion/{managed,sizing,wire,workflow}.py`, `tests/performance/foundry_single_call.py`, `tests/performance/foundry_l1.py`, and `tests/performance/foundry_preflight.py`. The first five belong to the preceding v11 implementation; the launcher selector and profile propagation are this preparation addition. `foundry_preflight.py` also contains the inherited one-line `billable_calls` correction, which must not be dropped.

**Tracked tests/contract documentation (eight files):** the remaining tracked paths below. `test_foundry_l1_launcher.py` combines four inherited accounting assertions and this task's version parameterization; preserve both. All 15 tracked paths proposed for explicit review are:

```text
documents/digestion/managed.py
documents/digestion/sizing.py
documents/digestion/wire.py
documents/digestion/workflow.py
tests/conftest.py
tests/fixtures/digestion_contracts/README.md
tests/integration/test_final_offline_azure_compatibility.py
tests/integration/test_foundry_l1_launcher.py
tests/integration/test_generation_wire_v10.py
tests/integration/test_managed_prompt10_contract.py
tests/performance/foundry_l1.py
tests/performance/foundry_preflight.py
tests/performance/foundry_single_call.py
tests/unit/documents/test_generation_wire_v10_decoder.py
tests/unit/documents/test_generation_wire_v10_sizing.py
```

**Historical v10 preservation additions:** the seven exact source snapshots under `v10_sources/` plus `tests/historical_managed_v10.py`. Six snapshots and the helper predate this task; the additional original `foundry_l1.py` snapshot is new here. **Historical v11 checkpoint:** the new byte-identical `managed_prompt11_offline_implementation.json` archive. **New/current v11 tests and contracts:** active `managed_prompt11.json`, semantic fixtures and contract/integration/unit tests including the new preparation module. **V11 prompts/reports/protocols:** the three prior implementation documents plus this task's three documents. These 21 proposed untracked additions are exactly:

```text
docs/codex/prompts/phase_17h_v11_final_live_preparation_and_readiness_assessment.md
docs/codex/prompts/phase_17h_v11_reducer_semantic_quality.md
docs/codex/reports/phase_17h_v11_final_live_preparation_and_readiness_assessment.md
docs/codex/reports/phase_17h_v11_reducer_semantic_quality_implementation.md
docs/evaluation/phase_17h_v11_live_semantic_validation_protocol.md
docs/evaluation/phase_17h_v11_reducer_quality_and_closure_assessment.md
tests/fixtures/digestion_contracts/managed_prompt11.json
tests/fixtures/digestion_contracts/managed_prompt11_offline_implementation.json
tests/fixtures/digestion_contracts/v10_sources/documents/digestion/managed.py.txt
tests/fixtures/digestion_contracts/v10_sources/documents/digestion/sizing.py.txt
tests/fixtures/digestion_contracts/v10_sources/documents/digestion/wire.py.txt
tests/fixtures/digestion_contracts/v10_sources/documents/digestion/workflow.py.txt
tests/fixtures/digestion_contracts/v10_sources/tests/performance/foundry_l1.py.txt
tests/fixtures/digestion_contracts/v10_sources/tests/performance/foundry_preflight.py.txt
tests/fixtures/digestion_contracts/v10_sources/tests/performance/foundry_single_call.py.txt
tests/historical_managed_v10.py
tests/integration/test_foundry_v11_preparation.py
tests/integration/test_managed_prompt11_contract.py
tests/integration/test_reducer_semantic_quality_v11.py
tests/reducer_semantic_fixtures.py
tests/unit/documents/test_reducer_semantic_contract_v11.py
```

**Deferred inherited documentation (33 files):** preserved and excluded from automatic staging. Some are indispensable historical references, but inclusion in an archival/docs commit is an explicit operator choice, separate from blindly staging all untracked files. No content was edited:

```text
docs/codex/prompts/phase_17h_current_authorization_and_token_headroom_assessment.md
docs/codex/prompts/phase_17h_final_approval_signing_and_controlled_execution.md
docs/codex/prompts/phase_17h_v10_authentication_renewal_and_final_operator_packet_preparation.md
docs/codex/prompts/phase_17h_v10_final_operator_verification_and_conditional_live_execution.md
docs/codex/prompts/phase_17h_v10_operator_preparation_and_readiness_assessment.md
docs/codex/prompts/phase_17h_v5_authorized_catalog_migration_and_commercial_reconciliation.md
docs/codex/prompts/phase_17h_v5_complete_financial_readiness_and_operator_preparation.md
docs/codex/prompts/phase_17h_v5_execution_window_renewal_and_rsa_authorization.md
docs/codex/prompts/phase_17h_v5_final_operator_preparation_continuation.md
docs/codex/prompts/phase_17h_v5_financial_reconciliation_and_second_four_call_readiness.md
docs/codex/prompts/phase_17h_v5_four_call_readiness_reassessment.md
docs/codex/prompts/phase_17h_v5_operator_preparation_signing_and_controlled_execution.md
docs/codex/prompts/phase_17h_v8_azure_operator_preparation_and_signing_readiness.md
docs/codex/reports/phase_17h_current_authorization_and_token_headroom_assessment.md
docs/codex/reports/phase_17h_final_approval_signing_and_controlled_execution.md
docs/codex/reports/phase_17h_live_evaluation_history_documentation_report.md
docs/codex/reports/phase_17h_live_invalid_qualification_source_root_cause.md
docs/codex/reports/phase_17h_v10_authentication_renewal_and_final_operator_packet_preparation.md
docs/codex/reports/phase_17h_v10_confirmed_operator_packet_and_rsa_signing_handoff.md
docs/codex/reports/phase_17h_v10_controlled_four_call_evaluation_and_reconciliation.md
docs/codex/reports/phase_17h_v10_final_operator_verification_and_conditional_live_execution.md
docs/codex/reports/phase_17h_v10_final_signing_and_controlled_live_outcome.md
docs/codex/reports/phase_17h_v10_operator_preparation_and_readiness_assessment.md
docs/codex/reports/phase_17h_v10_rsa_signing_and_independent_verification.md
docs/codex/reports/phase_17h_v5_authorized_catalog_migration_and_commercial_reconciliation.md
docs/codex/reports/phase_17h_v5_complete_financial_readiness_and_operator_preparation.md
docs/codex/reports/phase_17h_v5_execution_window_renewal_and_rsa_authorization.md
docs/codex/reports/phase_17h_v5_final_operator_preparation_continuation.md
docs/codex/reports/phase_17h_v5_financial_reconciliation_and_second_four_call_readiness.md
docs/codex/reports/phase_17h_v5_four_call_readiness_reassessment.md
docs/codex/reports/phase_17h_v5_operator_preparation_signing_and_controlled_execution.md
docs/codex/reports/phase_17h_v8_azure_operator_preparation_and_signing_readiness.md
docs/evaluation/phase_17h_live_attempts_root_causes_and_engineering_evolution.md
```

Final `git status --short -uall`: **15 modified tracked files, 54 untracked files, zero staged**. The six additions during this preparation are the new launcher snapshot, prior-v11 archive, preparation test, condensed task prompt, report and semantic protocol. `git diff --stat` (tracked only) is:

```text
 documents/digestion/managed.py                     |  36 +++++-
 documents/digestion/sizing.py                      |   2 +-
 documents/digestion/wire.py                        |   2 +-
 documents/digestion/workflow.py                    |   6 +-
 tests/conftest.py                                  |  16 +++
 tests/fixtures/digestion_contracts/README.md       |  74 +++++++++++
 .../test_final_offline_azure_compatibility.py      |   2 +-
 tests/integration/test_foundry_l1_launcher.py      |  12 +-
 tests/integration/test_generation_wire_v10.py      | 138 +++++++++++++++++++++
 .../integration/test_managed_prompt10_contract.py  |  53 ++++++--
 tests/performance/foundry_l1.py                    |  12 +-
 tests/performance/foundry_preflight.py             |   9 +-
 tests/performance/foundry_single_call.py           |   2 +-
 .../documents/test_generation_wire_v10_decoder.py  |   4 +-
 .../documents/test_generation_wire_v10_sizing.py   |   2 +
 15 files changed, 348 insertions(+), 22 deletions(-)
```

Untracked files are intentionally absent from diff statistics. The complete baseline/final status, binary diff and source inventories remain in protected temporary evidence. Git commit/push count remains zero.

## 13. Readiness gates and final accounting

| Gate | Verdict | Boundary |
| --- | --- | --- |
| Historical v10 preservation | PASS | Original inventory/repository evidence preserved; unavailable private audit not relabeled freshly verified |
| Exact v11 source generation | PASS | Current inventory/2 recomputed; two-file launch delta explained |
| Explicit v11 four-stage configuration | PASS | Canonically bound selector drives all four profiles; mixed/unknown/override cases reject |
| Offline engineering tests | PASS | Final suite result below |
| Azure deployment verification | PASS | Fresh resource/model/version/SKU/region/allocation and declared resource-host verification |
| Current operator identity | PENDING | Registration is current; actual fresh production-authenticated Principal/Graph join absent |
| Credential authorization | PENDING | V10 permission expired; fresh v11 use permission/deadline absent |
| Provider quota and consumer exclusivity | PENDING | Allocation/local policy verified; future external consumers unattested |
| Financial readiness | PENDING | Current prices/Decimal/headroom fit; v11 financial acceptance and window assumptions absent |
| G1/G2 readiness | PASS | Actual chunk/conservative future-child admission and unchanged strict regression boundaries |
| Semantic comparison protocol | PASS | Frozen source/rubric, empty future results, independent review/adjudication required |
| Source-control/CI checkpoint | PENDING | V11 working tree has no committed remotely verified revision |
| Unsigned canonical packet | PARTIAL | Review-only manifest; actual Principal/window/canonical bindings unavailable |

Overall: **TECHNICALLY_PREPARED_PENDING_OPERATOR**. This is not live-ready or ready for the separate signing decision. No next phase, RSA operation or paid action begins automatically. Operational RSA signatures **0**; live model calls **0**; real approval consumptions **0**; real financial reservations **0**; Git staging/commits/pushes **0**. Ephemeral test signing/consumption remains isolated synthetic validation and is not counted as real operator authority.
