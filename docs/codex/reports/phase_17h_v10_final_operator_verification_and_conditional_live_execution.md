# Phase 17H v10: final operator verification and conditional live execution

11 November 2026 UTC. Final verdict: **OPERATOR_VERIFICATION_INCOMPLETE**.
Stage decision: **BLOCKED — current application authentication is not verified**.
Additional independent operator inputs remain pending. No operational packet,
RSA signature, approval consumption or paid inference was produced.

## 1. Executive summary

The exact reviewed v10 checkout, generation inventory and applicable successful CI
remain intact. Fresh Azure management reads verify the intended deployment,
model/version/class and 30 RPM/30,000 TPM allocation. Existing protected stores
pass read-only integrity checks. All 13 historical settlements exactly match the
post-v8 audit; none is unsettled. There are no active admission calls, all ten
consumed approval markers remain present, and fourteen sealed v8 audit files
match their historical inventory. The public RSA files and local embedding tree
match their historical fingerprints.

Progression stops before operational Stage B. The available application token
fails the production Entra verifier; decoding only its expiry without trust also
indicates past expiry, which is not substituted for signed identity verification.
No Foundry runtime credential is supplied. There is no fresh exclusive window,
credential-use deadline, positive v10 financial allowance, independently authorized
v10 signing decision or separately authorized paid invocation. Historical receipts
are expired/configuration-specific and cannot satisfy these requirements.

Independent work continued after that gate: pricing observations, ledger/replay
reconciliation, source-byte comparison, focused offline tests and the documented
synthetic dry run were completed. No valid packet fingerprint or launch window
can honestly be presented for signing yet. This is an authentication and missing
operator-evidence boundary, not a newly discovered v10 implementation defect.

## 2. Source, Git and GitHub CI

| Check | Actual result |
| --- | --- |
| Repository / branch | Required repository, master |
| HEAD | ec22fa3d116696b80a1bb12ad17e2eb37db38cb3 |
| Local origin/master | Same full SHA |
| Tracked/index changes at entry | None |
| Pre-existing untracked documents | 23 Markdown files, preserved |
| Initial git diff --check | Exit 0 |
| Production generation_contract_digest() | e5fb249cc9b166b5e438f1534eb855fa5ab7531e08aa09314c110a1905327ebd |
| Generation/version | managed-prompt/10, generation-inventory/2 |
| Inventory/transport contract tests | Current 25-source fixture and representative request/schema/HTTP hashes pass |

The initial requested status, HEAD/ref, recent log and whitespace commands were
run. No fetch, tracking-ref update or remote mutation was performed. The connected
GitHub jobs API freshly returns completed/success for build job 129833074697 in
[CI run 42817169571](https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/42817169571),
including every listed test/compile/Helm/Compose/Docker step. The prior operator
assessment independently recorded 2,595 CI passes on this exact SHA. That count
is historical verified log evidence, not a newly downloaded log or local full
regression result in this task. The prior 749 distinct readiness passes are also
historical. Unchanged tracked source and fresh inventory checks leave that CI
applicable; no full suite rerun was necessary.

The user-supplied Antigravity source-audit PASS/no-critical-or-high finding remains
externally supplied evidence. This task does not claim to have independently
obtained that audit transcript.

## 3. Current Azure target and quota

Scoped management reads completed during this assessment around 07:24–07:27 UTC;
private evidence records exact timestamps and resource identity. The enabled
subscription and tenant match the historical pins. Full resource ID, including
subscription and resource group, was checked privately; identifiers beyond the
user-specified target are omitted here.

| Dimension | Current observation |
| --- | --- |
| Resource | epolymind-foundry-dev-susanta |
| Region | spaincentral, Spain Central |
| Deployment | epolymind-gpt-54-mini |
| Model/version | gpt-5.4-mini / 2026-03-17 |
| Deployment class | GlobalStandard |
| Resource/deployment provisioning | Succeeded |
| Rate allocations, renewal 60 seconds | 30 requests; 30,000 tokens |
| Endpoint | Historical configured v1 host passes production allowlist and matches a current named-resource endpoint |
| API route | /openai/v1/chat/completions, derived by existing provider |
| Public route | Enabled; ACL default Allow |
| Private endpoints / customer storage / diagnostic exports | None reported |

Deployment model/capability and resource/deployment inventories were read. No
unexpected change in the compared target fields was observed. This is not an
assertion that every property/ETag is historically identical or that inference
access has been tested. No deployment/quota/resource was created or changed.
The existing Azure CLI management session was used; no interactive Azure login,
application-token acquisition or resource-key retrieval occurred.

The initial sandboxed CLI invocation failed because its session file is outside
writable roots. Execution-policy escalation allowed the same scoped account read
and the prepared read-only management/billing inspector. The initial sandboxed
inspector failure was also retried through that mechanism. No approval rejection
or authentication bypass occurred. Management-session availability does not
establish PolyMind application identity or Foundry data-plane credentials.

## 4. Strict schema and request serialization

Fresh focused tests pass the current generation fixture and actual strict-schema
converter/transport contracts. The three digestion requests carry stage-proposal/1
under response_format=json_schema with strict=true; canonical construction remains
local. Nonstreaming generation, max_completion_tokens=3000 and low reasoning effort
remain unchanged; Q&A retains its separate JSON-object interface. The converter's
existing depth convention counts root at zero and limits nested containers to
five. No schema or converter limit was changed.

Current [Microsoft model feature documentation](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning#api-and-feature-support)
lists structured output and Chat Completions for gpt-5.4-mini 2026-03-17.
[Microsoft structured-output documentation](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs)
describes response_format on inference calls, required/closed objects and bounded
schema nesting. No independently documented free schema-only compilation endpoint
was established. No schema probe was sent.

**LIVE_SCHEMA_ACCEPTANCE_UNVERIFIED** remains the exact status. The fresh offline
passes do not establish Azure acceptance of this particular composition. A future
independently approved evaluation may observe it on Call 1 only after the operator
expressly accepts this uncertainty. Schema rejection must terminate immediately,
without retry, fallback, weakened schema or extra call.

## 5. Shared consumers and operational exclusivity

Current management inventory shows the known AKS cluster and node pool stopped,
the other inventoried container application stopped, and no container instances.
The named resource has the expected deployment; another account's deployments and
regional quota inventory were read separately. These reads do not establish that
portal playgrounds, scripts, other users or remote sessions are excluded.

The actual admission policy matches the historical configuration exactly:
2 RPM, 30,000 TPM, two concurrent slots; interactive reserve one RPM/slot and
2,000 TPM; background per-job one RPM/slot, with at most 28,000 TPM available.
Read-only admission shows zero active and zero last-minute calls. A process-argument
inspection finds zero L1/single-call launcher processes. It cannot exclude arbitrary
clients or prove distributed exclusivity. **A new operator-attested exclusive
window is missing.** No shared policy was changed and no consumer was stopped.

## 6. Application identity and separate provider credential

The historical approved configuration supplies tenant-specific entra_v2 trust
anchors and the application audience. The production verifier was invoked against
the existing process token, with no token value printed or saved. It returned
SecurityError both in sandboxed inspection and with approved network access for
public JWKS retrieval. The latter rules out claiming that merely granting network
access established identity. No Principal was manufactured from saved metadata.
An unverified expiry-only diagnostic indicates the supplied token has expired;
it is explicitly not accepted as trusted signature/claim evidence.

The pinned registration row is currently enabled, has PUBLICATION_MANAGE and epoch
zero, and matches the historical owner/tenant mapping. SQLite integrity is good.
These static facts do not authenticate the current operator. Current signed
issuer/audience/subject/tenant, delegated access_as_user, exact PolyMind.L1Operator,
nbf/expiry, signed OID/Graph-enabled-account correlation, actual authorized source
snapshot and permission/revocation revalidation remain unverified.

POLYMIND_L1_AZURE_CREDENTIAL is absent from the executing environment. No resource
key was silently acquired. An available management session is a different authority
from both the application token and inference credential. Fresh login would require
the established operator-approved memory-only device workflow, current window and
attestations; no current interactive-login authorization was inferred from old
procedures. No login or refresh was initiated.

## 7. Public RSA trust and signer authority

Current live public trust loads through the production read_private/load_trust
checks. The independent public PEM and trust key have identical public numbers;
RSA size is 3,072 bits. Public DER SHA-256:

`35785596dd2f38a3ae5fc8eeb93015a1ba3c8b4f16f06a1d73fbe521f9657816`

Key ID: `polymind-l1-35785596dd2f38a3`; purpose: live. Locations remain the existing
protected operator public-key and L1 trust stores outside Git. Replay location is
separate from the historical audit destination. No trust was provisioned/replaced,
private key opened, correspondence to private material rechecked, or signature made.

Public correspondence is VERIFIED; current independently authorized signer identity
and permission for an exact new packet are PENDING. Existing verifier requirements
remain RS256, exact trusted key/header, issuer polymind-operator-approval/1,
audience polymind-l1-live, purpose live, canonical unused UUID, integer iat/nbf/exp,
<=24-hour issue-to-expiry lifetime and exact operator/configuration/financial/target
bindings. Signing and execution approvals remain separate. No fresh approval exists
that was provided and verified for this v10 packet; no historical artifact is reused.

## 8. Operational storage and embeddings

Existing selected historical security/governance/admission files are absolute,
private, outside the repository, operator-owned, mode 0600, single-link regular
files without symlink traversal. Historical audit, replay and embedding directories
pass private directory checks at mode 0700. Selected locations are distinct.
About 880 GB disk space is available. No operational path was created or repaired.
A fresh v10 audit destination is not selected/verified because packet gates fail.

All three SQLite authorities were opened with URI mode=ro, PRAGMA query_only=ON,
without authority constructors. Integrity checks return ok; observed journal mode
is delete, locking mode normal and synchronous 2/FULL. This verifies current readable
state and settings, not a destructive lock-contention test or a new physical fsync
fault experiment. Fourteen historical audit files retain their sealed hashes.
Production object atomic-link/fsync and durable three-object manifest behavior remain
covered by applicable source/tests; no real object store was initialized for inspection.

Embedding model: sentence-transformers/all-MiniLM-L6-v2; source-pinned revision
1110a243fdf4706b3f48f1d95db1a4f5529b4d41. All eleven regular local files, including
weights/tokenizer/pooling/configuration, are present, private and non-symlinked.
Their tree digest matches the protected historical execution pin:

`96ab3cd391276cb159904c4d329318ae1f3330278a7fc0450256233cf8bb78db`

The current inventory matches the previously approved pinned artifact tree; no
new upstream provenance claim is inferred solely from model naming. Eight CPUs
and about 14 GB available memory were observed. Source retains CPU/local_files_only
loading, existing Chroma adapter and disabled telemetry. No real model load,
download, remote embedding call or new real vector store occurred. Fresh synthetic
publication/Q&A passes, but actual selected v10 destination/model opening remains
a launch-time verification after the missing gates are satisfied.

## 9. Pricing evidence and financial approval boundary

The governance configuration still contains phase17hl-pricing-eur-202611/1,
effective 7 November, with canonical hash
59c90a122e3db199848ae0817218bc4286bab80b22920a0916d8f5a54426dd37.
Catalog/policy equality to the historical approved contract is verified; no
migration/repricing occurred. Current account Consumption pagination completed.
Six exact-resource input/output meter records show OnDemand, unit 1M, USD prices
0.75/4.50, EUR billing and conversion 0.897706360249562. Resource-ID comparison
was checked against the current control-plane resource. Upward rounding reproduces
catalog input EUR 0.673279770188/M and output EUR 4.039678621124/M.

Current observed resource Consumption totals EUR 0.07662058440684063;
Cost Management independently totals EUR 0.07662058440684052. Their precision
difference is tiny; neither is final invoice/tax evidence. Observed meters support
the catalog arithmetic, not a guarantee of unchanged prospective pricing. No cached
input discount is assumed. Inclusive reasoning-output treatment remains the
existing contract; current invoice VAT treatment, account financial authority,
future charge applicability and other consumers' obligations are not fully verified.

| Conditional historical-assumption calculation | EUR |
| --- | ---: |
| 100,000 input + 12,000 output | 0.115804120472288 |
| 23% token VAT budgeting allowance | 0.02663494770862624 |
| Networking contingency, historically VAT-inclusive | 0.10 |
| Aggregate extras rounded upward to 12 decimals | 0.126634947709 |
| Total with consistently serialized extras | 0.242439068181288 |

Fresh Decimal arithmetic at precision 60 confirms these values. The exact
unrounded total is EUR 0.24243906818091424; serialization conservatively adds
EUR 0.00000000000037376. The prompt's historical forecast and production contract
use the rounded-extras total. VAT/network treatment and local-cost exclusions were
explicit historical operator decisions. They are not silently converted into a
new approved v10 exposure. **Current approved v10 paid exposure: none established.**
The EUR 5 comparison/monthly ceiling is neither approval to spend nor an Azure cap.
Pricing as a complete prospective commercial gate remains PENDING.

## 10. Read-only governance, settlements and replay

| Current local capacity, each owner and tenant scope | Remaining |
| --- | ---: |
| Rolling requests | 16 |
| Daily tokens | 500,000 |
| Monthly tokens | 1,459,618 |
| Outstanding-token capacity | 112,000 |
| Catalog-accounted monthly EUR | 4.923760432874072880 |

The existing policy selects polymind-evaluation/1. These local balances would fit
four requests and 112,000 reserved tokens under the historical cost scenario;
no reservation was made. They exclude unverified external commercial obligations
and do not authorize spend. Financial headroom as a complete launch gate remains
PENDING despite verified local capacity.

There are exactly 13 SETTLED reservations, zero unsettled and zero active provider
admissions. Every saved post-v8 financial-audit reservation equals its current
row, including historical catalog/usage/amount/state. Current row-inventory hash:
55d39c1ccb1259a18e74a7ac7f4d00db07143296c39ed016ae46b15e3f946928.
Ten consumed markers pass private-file and filename/approval-ID consistency checks.
Protected authority/trust/public/replay bytes match before and after local inspection.
No markers were deleted/reset and no settlements reopened, repriced or duplicated.
No discrepancy in the final authoritative comparison was found.

An initial local reconciliation reader targeted the older preparation's empty
audit path and returned FileNotFoundError; after locating the actual completed
v8 window-renewal audit, the comparison passed. Another reader initially used an
incorrect literal permission spelling; replacing that comparison with the actual
Action.PUBLICATION_MANAGE enum value confirmed the permission. These were
read-only diagnostic-tool mistakes, corrected without operational/source edits.

## 11. Source, plan, configuration and window

Production fixtures.pdf(4) reproduces the exact phase17h-pdf/1 benchmark bytes and
matches the preserved v8 source.pdf byte-for-byte. Source digest:

`1be99e19a56040fb55c74682a19f874d4d4573f18d9f52a9a7ae19c8158ea92d`

The fixture remains four pages, six lines and seed 1708. Fresh synthetic extraction,
planning and canonical acceptance are exercised by the documented dry run and
contract tests. They do not verify an authenticated operational source snapshot.
No operational extraction/plan was created through a real write-capable store,
and no historical plan was modified. Current owner-scoped plan hash, fresh canonical
configuration digest and unsigned approval-binding hash are **NOT CREATED**.
The exact generation is verified locally but is **not bound into a fresh approved
operational packet**. No old configuration timestamp/generation was patched to
appear current, no new authority identity introduced and no true prerequisite flag
invented.

No fresh execution-not-before, target launch, cutoff, expiry, API-key use deadline
or exclusivity attestation exists for this task. No valid execution window is
claimed. Preserve twenty-minute practical authority headroom, startup overhead,
>=61-second starts and four bounded calls when a real window is agreed. Prior
windows have elapsed; they cannot be extended by documentation.

The L1 parser was inspected directly. Supported live inputs are --live,
--configuration, --approve-sha256, --approval and --approval-trust. Its default
--output path runs a network-forbidden synthetic rehearsal. It does **not** load
and validate a supplied operational configuration in that branch. Therefore the
successful dry run below is explicitly not a successful final-packet preflight.
No invented --dry-run flag or alternate launcher was used.

## 12. Stage results and stopping gates

| Stage | Result |
| --- | --- |
| A: current operator verification | Partial; cloud/local checks verified, actual application identity fails and remaining operator attestations absent |
| B: fresh execution-packet preparation | Not entered operationally; dependent identity, exclusivity/window and positive financial gates missing |
| C: independent RSA authorization/signing | Not entered; no exact final packet or independent signing authorization |
| D: separate paid execution | Not entered; no verified signature or separate exact paid authorization |

This is not READY_FOR_INDEPENDENT_RSA_AUTHORIZATION and not merely waiting on
signing. Immediate state is BLOCKED at authentication, with further
PENDING_OPERATOR_ACTION items. The next operator actions are to explicitly
schedule/authorize the established fresh application-authentication workflow,
supply an exclusive practical UTC interval and credential-use deadline, confirm
current commercial assumptions/authority and approve a concrete positive v10
financial maximum after packet preparation. Those inputs allow protected
preparation and actual Principal verification. Only then can a concrete exact
configuration be submitted to an independently authorized signer, followed by
saved-signature verification and separate paid-execution authorization.

No authorization is requested against a nonexistent packet. General conditional
workflow instructions do not supply the missing exact signing/spend decisions.
Future evidence must be refreshed; these point-in-time reads cannot silently
serve as a later immediate-prelaunch snapshot.

## 13. Execution, accounting and semantic outcomes

Operational live launcher invocations: **0**. Paid provider calls attempted: **0**;
accepted: **0**. New paid usage: **0 input / 0 output / EUR 0 incurred by this task**.
This is not a zero-cost statement about the subscription's existing services.
New approval consumption, reservations and settlements: **0**. No provider-call
outcome table is applicable because no operational call was attempted.

No live v10 raw provider record, decoding receipt, canonical checkpoint, publication
or Q&A output exists from this task. G1/G2 and durable receipt behavior have fresh
synthetic evidence, not live acceptance. No live semantic-review denominator exists;
claim support, qualification/contradiction handling, omissions, abstention,
citation correctness and unsupported-inference quality remain NOT EVALUATED.
No semantic pass, publication eligibility or Phase 17H closure is claimed.

## 14. Validation, self-review and pre-commit review

Fresh focused command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=.:/tmp/phase17h-g1-g2 python -m pytest \
-p offline_guard -p no:cacheprovider \
tests/integration/test_managed_prompt10_contract.py \
tests/unit/documents/test_strict_schema_compatibility.py \
--basetemp=/tmp/phase17h-v10-final-verification-20261111/focused-valid \
--junitxml=/tmp/phase17h-v10-final-verification-20261111/focused-valid.xml -q
```

Result: **31 passed in 8.32 seconds; zero network attempts**. An earlier command
named a nonexistent test_azure_schema.py and collected no tests; it is not counted
as a pass. The correct existing module was discovered before the successful run.

The documented `python -m tests.performance.foundry_l1 --output <fresh-private-tmp>`
command exits zero: L1 COMPLETED, four synthetic calls, Q&A COMPLETE. All runtime
stores for this rehearsal are isolated disposable stores; no real authority,
provider credential or approval is used. No --live command was invoked.
Whole-repository compileall passed with an external bytecode-cache directory.
Git whitespace checks passed. No implementation/test/dependency/container change
required Docker/Helm/Kubernetes validation or another full regression suite.

Self-review checked current-versus-historical evidence labels, actual parser
behavior, public trust versus signer authority, management identity versus
application/provider identity, financial headroom versus permission, synthetic
versus operational planning, and immutable accounting/replay preservation.
No implementation correction or architecture change was required or attempted.

Separate documentation review checks the two new files for secret/private-key/JWT
material, sensitive operator configuration and signed artifacts, raw provider
content, unsupported pass claims, link targets, whitespace and unrelated edits.
No such sensitive payload is included. Temporary management/reconciliation
receipts, synthetic stores, test XML and bytecode stay outside Git in the task's
private /tmp evidence directory. Existing checkout preservation is checked by
hash inventory; all 23 inherited untracked reports/prompts are retained.

## 15. Final Git state and disposition

Only the requested matching prompt and this report are added, both untracked.
Final branch master and HEAD/local origin/master remain the required full SHA.
Final status: zero tracked modifications, zero staged changes, 25 untracked
Markdown documents (23 inherited plus these two). git diff --stat and
 git diff --cached --stat are empty; untracked documents are correctly excluded.
No production/generation/historical-fixture or prior-document change occurred.

**Final verdict: OPERATOR_VERIFICATION_INCOMPLETE.** Cloud and offline engineering
are verified within the stated boundaries. Current application authentication,
provider credential, prospective commercial/financial approval, exclusivity/window,
independent signer authority and separate paid approval prevent controlled
progression. Signing and live execution remain unperformed.

Git staging: NO. Commit: NO. Push: NO. Branch/history/remote mutation: NO.
Operational authority mutation: NO. Interactive authentication: NO.
RSA signing: NO. Approval consumption: NO. Paid inference: NO.
