# Phase 19B — Live-deployment readiness continuation

21 November 2026. **Initial preparation completed; controlled cloud validation BLOCKED at
A1.** This is a dated Phase 19B readiness continuation. The offline foundation is complete;
Phase 19B deployment/live validation remains ACTIVE. Phase 19C final documentation and
engineering closure is NOT STARTED.
No Azure mutation, resource activation, identity administration, credential acquisition,
live execution signing, provider transmission, or paid-model request was performed.

## Stage-boundary correction — 21 November 2026

The operator reassigned the preparation evidence previously labelled Phase 19C to this
Phase 19B continuation. The earlier uncommitted prompt/report were renamed and their stage
references corrected; all observations, outcomes, quotas, tariffs and historical source/CI
identities below remain evidence from the original preparation. Original `/tmp/phase19c-*`
artifact names are retained for provenance, not as a claim that Phase 19C began. No discovery,
pricing retrieval, regression or cloud validation was rerun for this documentation correction.
Historical committed Phase 19A/19B records remain unchanged, including their contemporaneous
stage assignments. The revised boundaries supersede those assignments for current work only.

| Stage | Responsibility | Current status |
|---|---|---|
| 19A | Readiness Assessment | COMPLETE |
| 19B | Offline Implementation, Azure Deployment, Live Integration and Validation | ACTIVE |
| 19C | Final Documentation and Engineering Closure | NOT STARTED |

This relabelling grants no independent authorization. A1 remains the first blocking gate.
After prerequisite resolution, deployment, real browser authentication, synthetic cloud
validation, separately authorized Foundry execution, capacity/recovery and cost validation
all belong to Phase 19B. Final closure documentation is deferred to Phase 19C.

## Repository and CI baseline

Initial `git status --short --branch` was exactly `## master...origin/master`, with no changed
files. `git rev-parse HEAD` matched **`7bf82dc2da4a9f29561a5f493b690502c0090eb0`**, commit
`feat: complete Phase 19B offline Azure deployment foundation`. The last eight commits were
inspected. `git diff --check` passed; `git diff --cached --name-only` was empty. No existing
work was overwritten and no Git history/index operation was performed.

Read-only `gh run view 44805275341 --json headSha,headBranch,status,conclusion,createdAt,updatedAt,url,jobs,workflowName`
confirmed [Estudio PolyMind CI](https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/44805275341)
completed successfully on `master` at that exact SHA. The build job completed
**2026-11-20 19:58:17 UTC**; run update was 19:58:18 UTC. Import validation, automated tests,
Helm security validation, ordinary Compose validation and Docker build steps all succeeded.
Inspection of `.github/workflows/ci.yml` confirms CI's Compose step checks the ordinary
profile; it is not independent five-service/browser/Entra/provider acceptance.

The separate final local Phase 19B regression is **3,278 passed, 1 warning in 1,367.81 s**.
This is recorded in the committed 19B report and independently found in the retained
`/tmp/phase19b-gap-full-acceptance.log`. It is not a new continuation full-suite result or a
test count inferred from CI metadata. The historical 19B topology result is seven fake
provider calls, zero external calls, with both application planes exercised. No equivalent
Azure or real-provider result is inferred.

Read the complete 19A/19B prompts and reports, including Integration Gap Resolution,
architecture, plan, VM guide, AGENTS.md and README. Relevant supporting contracts include
`docs/security/{phase_17g,entra_v2,production-security}.md`, evaluation policy, and the
Phase 17, 17I and 18 engineering/deferred-acceptance decisions. Inspected actual deployment,
storage/backup/lifecycle, permission, Chat, UI/API and regression-test implementations.
Current code and the final 19B appendix take precedence over earlier historical GAPs.

## Authorization and current readiness matrix

The operator authorized this preparation, read-only discovery and permitted local checks.
Scoped Docker inspection/network-disabled disposable audit containers and isolated offline
tests are covered. Execution-system approvals for CLI log access, public price GETs, Docker
socket access and local test servers are technical execution approvals; **they do not satisfy
any A1–A5 business gate**. Existing authenticated Azure CLI context was used without login,
device-code flow, key retrieval, registration changes or explicit credential renewal.

| Gate / requirement | Status | Actual evidence and outstanding decision |
|---|---|---|
| Baseline and exact-commit CI | PASS | Clean expected source and successful run verified above |
| A1 Azure resources/spending | PENDING | No selected resource group, SKU/region, private route/egress, ceiling/window or named billing/stop/retention owner approved |
| A2 identity/network administration | PENDING | No current approved Entra browser registration/scope/consent/enrollment, callback, certificate, tunnel or outbound policy |
| A3 provider/source/data | PENDING | Current deployment metadata read; endpoint dispatch compatibility, capabilities and eligible hashed source/transmission/retention approvals absent |
| A4 inference finance/quota | PENDING | Deployment advertises limits; applicable tariff, shared consumers, authority reconciliation, exact plan and separate amount/window unapproved |
| A5 live execution permission | PENDING | No fresh reviewed/signed live record supplied or issued; test-purpose records cannot satisfy production |
| A6 public exposure | NOT AUTHORIZED | Private scope only; no public application ingress permitted |
| Azure account discovery | PASS, observation only | Enabled subscription/tenant identified; neither selected by operator as the Phase 19 execution scope |
| Effective existing RG permissions | PASS, read-only observation | Permissions endpoint for `rg-epolymind` returns `actions=["*"]`, empty `notActions`/dataActions; this is not approval or a policy/quota/deny-assignment guarantee |
| Candidate allocation readiness | GAP | Both exact candidate families have zero West Europe quota |
| Five-service configuration | PASS, local/static | All three Compose parsers passed; Phase 19 security/dependency contracts verified |
| Chat and Documents integrations | PASS, offline scope | Resolved implementations present; 89 focused tests pass; real browser/cloud acceptance unexecuted |
| Azure capacity/recovery | GAP | No deployed VM measurements, off-disk cloud backup, reboot or deallocation evidence |
| Current total cost quotation | GAP | Refreshed public rates; actual access/egress, invoice currency/rate/FX/tax and policy-required fees unresolved |

**First missing gate: A1.** No Azure mutation command was issued. A2 also blocks its relevant
identity/network changes even if A1 is later approved. Login, RBAC permission, successful CI
or an existing Foundry deployment is not financial or execution authorization.

## Azure inventory and immutable artifacts

`az account show` returned enabled subscription **ECI-Development**,
`970e5901-0d2d-44de-ade7-92ce4eb61a73`, tenant
`afabeaf8-0fea-42c9-afb4-7e5c07eff3f3`, user-type context. Account email and tokens were not
printed. Resource-group discovery found `rg-eci-dev`, `rg-eci-deploy-dev`, `rg-epolymind`,
`MC_rg-epolymind_epolymind-aks-dev_spaincentral` and `NetworkWatcherRG` in Spain Central.
No new resource group was created or approved.

Read-only inventory of existing `rg-epolymind` found historical AKS, ACR, user-assigned
identity, Foundry account/project, Redis Enterprise, private VNet, private DNS links and
Redis private endpoint/NIC. **No VM was listed in that group.** This is not a subscription-wide
proof that no VM exists, and the historical AKS/managed Redis/private endpoint are not
substitutes for the Phase 19 Compose VM. None was changed, started, stopped or adopted.
No access route from this operator to a future VM was demonstrated. No Phase 19 Azure
VM/disk/snapshot/NIC/resource ID, deployment timestamp or allocated hours exists from this run.

The historical application artifact is locally present:

```text
sha256:afac225fe4c952e5c26b7c9bb1c924c83d1e01cf779c4b27ef1e32b30d00adef
```

Docker reports Linux amd64, UID/GID 10001:10001, **3,042,744,308 bytes**, created
2026-11-19 09:33:59 UTC, no RepoTags/RepoDigests. This is a local content identity, not a
registry reference or Azure deployment. No image was rebuilt or pulled. A read-only,
network-disabled audit compared **152 tracked source/configuration files** against it:
150 byte-identical; `documents/operator/app.py` and `ui/tls_gateway.py` each retain one extra
trailing blank line in the image. Unified diffs contain only that blank line, and their
parsed Python ASTs are identical. Therefore executable content matches the audited committed
files; an assertion of complete byte-for-byte source identity would be false. The initial
strict audit failed on those two files; the follow-up resolved the cause without edits.
This audit is not a claim of deterministic whole-image rebuilds: the Dockerfile's base tag
and build-time dependency resolution remain separate reproducibility limits.

The image audit found no `/app` file named `.env`, with `.key`/`.pem`/`.sqlite`/`.db` suffix,
or test directory. Inspected image environment contains build/runtime defaults, no configured
provider/browser credential. These checks and existing Docker exclusions support custody;
they are not a comprehensive historical-layer secret certification.

Current local vendor RepoDigests are:

```text
redis@sha256:ff02b58f971e7d7d156a1267e283fcbbeee91773b6aa36c49dac28ecfe28eadf
chromadb/chroma@sha256:1e0b73a187a28757c572acba508c46f48c9e8b0acaf5c20e6d95cdedce1acdf6
```

The committed profile still contains tested vendor tags and an operator-supplied app image.
Before deployment, freeze these verified vendor identities in the reviewed deployment
configuration and verify image-transfer/archive hashes and the received local identity or
registry manifest digest. No mutable tag alone constitutes the acceptance identifier.

## Deployment, identity, TLS and networking

Five services remain API, UI, gateway, Redis and Chroma. API has one locked process and one
runner; seven SQLite authorities stay under `/state/private`. Bind inputs disable automatic
host-path creation. All services run explicitly non-root, read-only roots, dropped capabilities,
no-new-privileges, resource limits, `on-failure:3`, 90-second stop grace and rotated logs.
Secret/trust/revocation/permission inputs mount read-only outside writable authority state.
Health ordering is Redis/Chroma → API → UI → gateway. Gateway's TCP health is not browser/TLS
acceptance. Local locking, missing/truncated/unsafe-authority refusal and backup integrity
tests pass; production requires actual ext4/xfs/btrfs and mount-aware startup.

Only `127.0.0.1:9443` is published. Backend/frontend Docker networks are internal; API/UI
egress is not a destination firewall. The approved host/network outbound policy must enforce
identity/update/image destinations and keep provider egress disabled during synthetic validation.
**A VPN route to the VM's private address alone cannot reach host loopback.** A2 must select
an approved SSH/private tunnel reaching loopback and preserving the private HTTPS hostname,
certificate and callback. No listener rebinding or alternative gateway is implemented here.

Real Entra native Streamlit login, delegated API access token, tenant-specific issuer/JWKS,
exact API audience, `access_as_user`, `PolyMind.L1Operator`, owning-principal enrollment,
token forwarding, expiry/logout/reauthentication and cookie posture require actual browser
proof. No client secret, certificate private key, access token or live permission was read
or placed in this report. No development issuer/certificate was promoted to real acceptance.
No Entra registration, redirect, consent, role assignment, NSG, DNS or network was changed.

## Chat/RAG and Documents functional/security evidence

Inspection plus the focused offline run confirms Chat native-token forwarding, server-derived
identity, closed session/source scope, owner/tenant memory, canonical PublicationReplica
dense/per-document BM25/fusion/reranking, source hashes, LangGraph and shared governed execution.
JSON and NDJSON share durable request keys; transport replay does not dispatch another request.
Bounded SSE stays inside inference infrastructure and becomes provider-neutral tokens then
PolyMind NDJSON. Missing usage/truncation/timeout/revocation deny acceptance and retain UNKNOWN
or unfinished intent. There is no automatic retry or readiness/refresh-driven generation.

Documents retains real runtime composition, independent permission verification and durable
consumption, version-2 execution sessions, immutable version-1 zero-paid semantics, complete
source/session/principal/model/policy bindings, explicit publication, digest review gates,
separate pending-answer reviews, accepted Q&A replay and full-authority reopen. Changed,
expired, revoked or test-purpose live permissions deny execution. The focused group includes
financial/admission denial and uncertainty, permission exhaustion, cross-scope rejection and
the full offline Start/digest/publication/review/question/accepted-answer path.

Those tests use signed local identity tokens, ephemeral **test-purpose** permissions and
fake provider HTTP, with isolated local authorities and retrieval test adapters. They are
not real Entra, deployed Redis/Chroma, human reviews or live Foundry acceptance. The separate
19B container evidence did exercise real Redis/Chroma/baked encoders; it was not repeated
solely to duplicate that evidence. Existing legacy local behavior is supported by the unchanged
source and retained CI/full-suite baseline; no new interactive local-Ollama acceptance is claimed.
Neither resolved integration gap is reopened by a missing cloud approval.

## Provider, data, finance and independent quality review

Read-only ARM metadata currently identifies `epolymind-foundry-dev-susanta` in **Spain Central**,
AIServices/S0, account endpoint `https://epolymind-foundry-dev-susanta.cognitiveservices.azure.com/`,
`publicNetworkAccess=Enabled`, `disableLocalAuth=null`. This account property is not public
exposure of a VM application, proof of API-key compatibility, or approval to transmit data.
The account endpoint is **not yet a verified v1 Chat Completions dispatch URL**.

Its deployment `epolymind-gpt-54-mini` reports OpenAI `gpt-5.4-mini`, version **2026-03-17**,
`GlobalStandard`, capacity 30, provisioning Succeeded; reported limits **30 requests/60 s**
and **30,000 tokens/60 s**. These are current control-plane observations, not measured usable
quota, a commitment that no other clients consume it, or actual structured/schema/streaming/
usage tests. GlobalStandard metadata does not establish Spain-only or West-Europe-only
processing. No provider discovery/generation endpoint was called and no source was transmitted.

A3 must approve the actual dispatch endpoint/model/version/type, model capabilities, source
hashes/ownership/licence/classification and transmission/retention terms. A4 must supply the
current applicable tariff/currency, exact owner/tenant/provider authority bindings, outstanding
obligations and shared-consumer agreement. Historical EUR budgets/catalogs are not authority
for this evaluation. No historical database was opened, replaced, migrated or cleared.

**Paid-call plan: NOT EXECUTED and not yet executable.** Authorized count is zero. Before any
paid request, record each purpose/stage, exact source/schema, model/deployment, conservative
input/output maximum, ≤60-second bounded deadline, serial pacing, aggregate worst-case cost,
start/deadline/cutoff, uncertainty stop/reconciliation and receipt/usage settlement. Compute
the bound from actual planned calls and approved input/output tariff; do not assume four calls.
Separately approved Chat must retain SSE → provider-neutral token → NDJSON and share authorities.
Only then can the independent custodian issue A5 against the frozen runtime binding and exact
scope/amount/window. Do not issue live permissions now. Missing usage, timeout, truncation,
revocation or financial mismatch stops subsequent provider execution without a retry.

No new independent semantic review occurred. Phase 17H remains **0/2 human reviews** with formal
closure pending; 17I external verification remains deferred with **0 participants**. Phase 18
administrative/deployment acceptance obligations remain. Synthetic review records used in tests
do not satisfy any of them. New external digest and answer presentation each retain their own
independent quality-review gates.

## VM choice, measurements and recovery

No SKU is selected or capacity-certified. West Europe `az vm list-skus --all` reports no
restrictions for B2as_v2; D2as_v5 has `NotAvailableForSubscription` zone restrictions for zones
1 and 3. Crucially, `az vm list-usage` reports **standardBasv2Family 0/0** and
**standardDASv5Family 0/0** current/limit, despite total regional cores **0/10**. The older
standardBSFamily 0/10 and DASv4 0/10 do not qualify either exact candidate. No quota increase,
support request, replacement SKU, region change or allocation attempt was made. Even positive
quota/listing would not guarantee physical capacity.

19B's resource evidence records 40.296-second startup, 8.428-second embedding/reranker load,
584.75 MiB maximum sampled container aggregate and 35.86% maximum aggregate Docker CPU for a
tiny synthetic workload; the later integration run recorded 40.504-second startup. These are
historical local measurements, not Azure host capacity. Eight-second sampling may miss peaks;
image bytes do not measure RAM and cgroup usage omits host/kernel/cache overhead.

Within an approved cloud window, measure host/process/cgroup startup peaks, encoder/router
load, representative bounded corpus/index growth, sustained serial jobs plus concurrent
frontend reads, Chat and document latency, disk free space/IOPS/latency, Redis AOF/Chroma writes,
readiness transitions/errors/OOM/swap and backup/recovery duration. Proposed retained gates:
host memory below 6 GiB on 8 GiB, no OOM/sustained swap, ≥20% disk free, and bounded worker/UI
latency with explicit observed timing. For B-series, collect CPU credits consumed/remaining
and sustained baseline performance across the run; short burst success cannot qualify it.
If credits fail while memory fits, D-series needs approved quota/scope before comparison.

Actual Azure persistence/recovery is **NOT EXECUTED**. Cloud acceptance must cover missing-disk
startup refusal, second-writer exclusion, vendor restart, SQLite/publication reboot persistence,
consumed/revoked permission and financial obligation persistence, no UNKNOWN replay, coherent
stopped-writer backup, protected off-disk snapshot, integrity/path-bound isolated restore,
compatible-image rollback on current truth, shutdown and verified deallocation. Local tests
cover several contracts but not Azure disk/reboot semantics. Restore never starts a second live
consumer; rollback never restores stale security/financial truth. RPO/RTO remain unmeasured.

## Refreshed cost envelope and residual resources

Unauthenticated GET-only [Azure Retail Prices API](https://prices.azure.com/api/retail/prices)
queries began **2026-11-21 07:19:46 UTC**, followed all result pages, and saved raw public rows
in `/tmp/phase19c_public_prices.json`. Query filters/URLs are retained there; retrieval script
and diagnostic output are `/tmp/phase19c_public_prices.py` and `/tmp/phase19c-prices.log`.
USD/Linux PAYG, West Europe unless stated; no discounts, taxes, FX, free-tier availability or
agreement-specific rate is assumed. This refresh confirmed the selected historical rates;
it did not turn estimates into an invoice or authorize a topology. The
[official API reference](https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices)
explains retail pricing; subscription-applicable cost remains a gate.

| Item | Refreshed USD rate | Meter identity |
|---|---:|---|
| Standard_B2as_v2 | 0.0864/hour; 0.6912/8 h; 63.072/730 h | `3a119482-88fc-5dbf-b2f7-fae7145659b4` |
| Standard_D2as_v5 | 0.104/hour; 0.832/8 h; 75.92/730 h | `c47ff26a-3d0d-5e1f-bcd2-a0ba8e9cc4e9` |
| E6 Standard SSD LRS 64 GiB | 4.80/month each; two = 9.60 | `c743552a-d863-435e-8c2c-f7ec6a8d00cf` |
| Standard SSD operation row | 0.002/10,000; allowance 1 million = 0.20 | `ce957933-8287-4f8b-83ee-53a5cbe056d9`, returned E50 operation meter; confirm exact E6 applicability in final quote |
| Standard HDD LRS snapshot | 0.05/GB-month; assumed 20 billed GB = 1.00 | `78dd126f-f855-4670-8038-fd66cf0f43b9` |
| Standard public IPv4 | 0.005/hour each | `9c150bf9-2bad-430e-a53c-c213804f49ef`; none on VM |
| VpnGw1 comparison, unselected | 0.19/hour | `431b835b-2538-4faa-8763-8202f3fdbbb4`; eligibility unverified |
| NAT comparison, Global, unselected | 0.045/hour + 0.045/GB | `ae30040a-67f5-485b-b0f4-a6ef50504d9c`, `d32b6352-b66b-4c4c-8f21-60e94058e04d` |
| Internet egress paid tier | 0.087/GB; assume 1 GB charged | `9995d93a-7d35-4d3f-9c69-7a7fea447ef4` |
| Optional Log Analytics paid ingestion | 2.99/GB; no workspace proposed | `e5626349-2f1f-4563-babc-dc9219884716`, paid tier minimum 5; no free allowance assumed |

Eight allocated VM hours plus a conservative full billed month of two disks/20-GB snapshot,
one-million-operation allowance and 1-GB egress is **USD 11.5782 B / 11.7190 D, excluding
private access/egress infrastructure and unverified fees**. This is not a complete route quote.
For comparison only, 12 hours of VPN + NAT + two gateway IPs adds
`12 × (0.19 + 0.045 + 2 × 0.005) + 10 GB × 0.045 = 3.39`, yielding
**14.9682 / 15.1090**. Eight network hours instead yields the historical **13.9882 / 14.1290**.
No gateways are selected or authorized; a required alternative SKU, tunnel, cross-region
peering or security-plan charge changes that envelope. Do not create either gateway by default.

The **USD 30 total infrastructure ceiling remains a proposal** for ≤8 allocated VM hours,
≤12 dedicated network hours and ≤30-day retention conservatively quoted as one billed month.
It can only become a concrete approved ceiling after route and applicable quote resolution.
Use named stop ownership and 50/75/90% alerts; budgets notify rather than enforce a hard cap.
No paid model amount is included or approved. Local diagnostics add no monitoring service.

No new billable resource or inference action was launched by this preparation; this is not
proof that existing subscription costs are zero. This continuation's actual compute hours, resource costs,
provider token billing, provisional Cost Management entries and final invoice reconciliation
are **NOT EXECUTED**. Historical AKS/ACR/Redis/Foundry/network resources may continue incurring
charges independently; no permission to delete or deallocate them is inferred.

[Azure deallocation](https://learn.microsoft.com/en-us/azure/virtual-machines/states-billing)
must be verified separately from guest/Compose stop. Retained disks/snapshots still bill:
illustrative 9.60 + 1.00 = **10.60/month** plus operations. Unselected VPN/NAT/two IPs left
running would add **178.85/730 h** plus data, even with a deallocated VM. Retained logs,
registry, peering and policy-required services require actual inventory/ownership. Do not delete
any managed disk, snapshot or financial evidence automatically at retention expiry.

## Exact proposed operator approval packet

This packet is **unapproved**. Missing entries are decisions, not permission inferred from
silence. No cloud creation can begin until A1 is complete and applicable A2 is approved.

| Decision | Concrete proposal / operator action required |
|---|---|
| Execution scope | Confirm or replace the observed subscription/tenant above; approve a dedicated `rg-polymind-phase19-validation` resource group in West Europe, or explicitly name an approved existing scope. The proposed name is not created. Approve tags and verify effective RBAC/policy at the chosen scope. |
| VM/quota | Choose B2as_v2 for bounded credit/capacity validation or D2as_v5 for non-burstable comparison. Separately authorize/request at least 2 family vCPUs in the selected region, or supply another region for new pricing/SKU verification. Do not allocate while quota is zero; no automatic SKU enlargement/substitution. |
| Core inventory | One Linux amd64 VM, one private NIC, dedicated VNet/subnet/NSG if an existing approved network is not selected, no VM public IP, 64-GiB E6 OS disk plus 64-GiB E6 durable ext4 data disk. One coherent protected data-disk snapshot, bounded to 20 billed GB for the estimate; retain source/finance evidence. No managed database, GPU, AKS or new registry/monitoring stack. |
| Private route/egress | Name the existing approved tunnel and outbound route, endpoints/CIDRs and allocated incremental cost; prove it reaches loopback HTTPS. If absent, submit an exact separately approved access/egress design and quote. VPN/NAT comparison above is not approval to create them. |
| Spend and time | Approve an applicable-currency total amount after quote resolution (proposal USD 30 infrastructure), exact UTC start/deadline/cutoff, ≤8 allocated VM hours and any separately selected network lifetime. Name billing/stop/deallocation and residual-retention owner, alert mechanism and disposal approval process. |
| State and artifacts | Approve immutable image/config/source manifest, vendor digests, disk UUID/mount `/srv/polymind`, container `/state`, numeric owners and protected backup destination. Explicitly decide new isolated synthetic authority versus approved existing authority migration; do not reset historical truth. |
| A2 administration | Name identity/network custodian; approve exact tenant/API and Streamlit client registrations, API scope/role/consent/enrollment, HTTPS hostname/certificate/callback, browser secret/cookie custody, loopback-reaching tunnel and outbound allowlist. Supply private artifacts outside Git; provide references, never tokens/keys in chat/report. |
| Later A3–A5 | Review current Foundry metadata and source rights/retention, freeze capabilities and exact call plan, reconcile shared ledger/quota/pricing and approve separate model amount/window. Independent custodian then supplies a fresh configuration-bound live permission. Infrastructure approval covers none of these. |

After approval, continue **in this same Phase 19B**: reverify account/RBAC/quota/prices/window;
deploy only the approved VM/disks/private route; verify immutable transfer, filesystem and
mount failure behavior; prepare reviewed secrets/trust without a live provider grant; start
the same five services; validate private TLS and real Entra/API authorization plus isolated
zero-paid synthetic workflows, refresh/replay, persistence and recovery; measure capacity and
credit behavior; obtain independent A3/A4/A5 for the exact real-model plan; execute serially
with uncertainty stop/settlement and quality gates; quiesce, back up, verify restore/rollback,
deallocate and reconcile costs/residual resources; append actual results to this report.
The existing local container harness uses test identity; it cannot by itself prove the real
Entra synthetic-cloud requirement. Review the isolated fake-provider test composition before
cloud use, retaining actual Entra verification and zero provider credentials/egress. Do not
promote its fixture identity or test routes to the production entrypoint.

## Executed checks, failures and corrective disposition

The following focused command ran outside the sandbox after local-network restrictions:

```bash
env HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  tests/unit/test_phase19_deployment.py tests/integration/test_phase19_operator.py \
  tests/integration/test_phase19_execution_bridge.py tests/unit/test_phase19_bounded_stream.py \
  tests/unit/test_phase19_chat_view.py \
  --basetemp=/tmp/phase19c-pytest-approved-20261121
```

**89 passed, 1 warning in 75.24 seconds; exit 0.** Log:
`/tmp/phase19c-focused-tests-approved.log`. Warning is the existing aiohttp `NotAppKeyWarning`
for the gateway client key. No code fix was necessary. The first sandbox attempt progressed
through 19 passes and two gateway failures before stalling on HTTP/thread tests; it was
interrupted (exit 130), not counted as a completed run. The same modules passed outside the
sandbox with fake transports. No full-suite rerun duplicated unchanged-code CI/19B evidence.

These configuration/compilation commands all exited **0**:

```bash
docker compose --env-file /dev/null -f docker-compose.yml config --quiet
env DOCUMENT_DEMO_ROOT=/tmp/phase19c-inert docker compose --env-file /dev/null -f docker-compose.documents.yml config --quiet
docker compose --env-file deployment/phase19/compose.env.example -f docker-compose.phase19.yml config --quiet
systemd-analyze verify deployment/phase19/polymind.service
env PYTHONPYCACHEPREFIX=/tmp/phase19c-bytecode python -m compileall -q .
git diff --check
```

The data paths above were parser inputs only, not initialized deployment authorities.
Compilation used an external bytecode cache. No configured lint tool was found or installed.
No dependency, Docker build, five-service start, systemd install or Kubernetes operation ran.

Read-only discovery commands were `az account show`, `az group list`, `az resource list -g
rg-epolymind`, exact-candidate `az vm list-skus --location westeurope --resource-type
virtualMachines --size <candidate> --all`, `az vm list-usage --location westeurope`, scoped
`az rest --method get` to the RG Microsoft.Authorization permissions endpoint, and
`az cognitiveservices account show` / `account deployment list` for the named existing account.
Queries selected only sanitized metadata. Initial Azure inventory failed on sandbox CLI-log
writes; public pricing failed sandbox DNS; Docker run failed sandbox socket access. Each was
retried through execution approval. No failures were bypassed by changing app security.

The first image audit's Python assertion exited 1 on the two trailing-newline mismatches;
its containing shell later returned 0 after subsequent Docker inspections. The failed assertion
is explicitly retained here rather than classified as an exact-byte PASS. A separate diff/AST
comparison resolved the discrepancy as whitespace only. No live acceptance test failed:
those tests were not executed. No destructive cleanup occurred; `docker ps` showed no running
containers after the disposable audit. Temporary offline keys/state remain outside Git.

## Documentation, self-review and separate pre-commit review

Saved the corrected [Phase 19B continuation instruction](../prompts/phase_19b_live_deployment_readiness_continuation.md)
and this report. Appended dated preparation evidence to the existing architecture, plan and VM
guide; added README current Phase 19 status while retaining the dated Phase 18 history. No
parallel runbook, new formal stage, application change, API/configuration change or dependency
was added. Historical 19A/19B reports and all Phase 17/18 policy/acceptance records are unchanged.

Implementation self-review checked the source/image difference, provider-neutral boundary,
one-writer lifecycle, scope/replay/review/UNKNOWN controls, cost arithmetic, exact quota-family
names and loopback access implication. It distinguished broad RG permissions from A1, account
endpoint metadata from actual dispatch compatibility, local digest from a registry digest,
and offline test-purpose signatures from A5. No material application defect was found within
this bounded inspection; cloud prerequisites remain unresolved rather than weakened.

Before the stage-boundary correction, separate pre-commit review checked the six Markdown files for secret/key/token payloads,
runtime databases, generated artifacts, debug content, accidental dependencies, unrelated
changes, broken local links and whitespace. Operational paths/public meter IDs and necessary
subscription/resource metadata are intentional evidence; no private keys, credentials, signed
permissions or source bytes belong in these artifacts. The automated check found **90 existing
local Markdown links, zero broken links, zero whitespace findings and zero secret-payload
pattern findings** across the six changed/new files. Manual diff review found no unrelated
implementation or generated artifact. Nothing is staged or committed.

## Current readiness outcomes and remaining operator decisions

```text
PHASE_19B_BASELINE_AND_CI: PASS

AZURE_RESOURCE_AUTHORIZATION: PENDING
AZURE_IDENTITY_NETWORK_AUTHORIZATION: PENDING
REAL_PROVIDER_DATA_AUTHORIZATION: PENDING
FINANCIAL_EXECUTION_AUTHORIZATION: PENDING
SIGNED_LIVE_EXECUTION_PERMISSION: PENDING

AZURE_PRIVATE_VM_DEPLOYMENT: NOT_EXECUTED
REAL_ENTRA_BROWSER_AUTHENTICATION: NOT_EXECUTED
CHAT_RAG_CLOUD_VALIDATION: NOT_EXECUTED
DOCUMENTS_CLOUD_VALIDATION: NOT_EXECUTED
REAL_MODEL_VALIDATION: NOT_EXECUTED
PERSISTENCE_RECOVERY_VALIDATION: NOT_EXECUTED
VM_CAPACITY_VALIDATION: NOT_EXECUTED
COST_AND_FINANCIAL_RECONCILIATION: NOT_EXECUTED

PHASE_19A_READINESS_ASSESSMENT: COMPLETE
PHASE_19B_EXECUTION_STAGE: ACTIVE
PHASE_19B_LIVE_DEPLOYMENT_READINESS: BLOCKED
PHASE_19C_FINAL_DOCUMENTATION_AND_ENGINEERING_CLOSURE: NOT_STARTED
PHASE_19_ENGINEERING_CLOSURE: DEFERRED
PUBLIC_PRODUCTION_EXPOSURE_AUTHORIZED: NO
```

PERSISTENCE_RECOVERY here means **Azure acceptance**, not a retraction of passing local
contracts. Exact outstanding actions are the A1/A2 packet, quota remedy, selected private
loopback route/egress/quote, subsequent A3–A5 bindings and executed cloud/capacity/recovery/
cost evidence. Stop before restricted action. No external-user, semantic, HA or public
production readiness is established by these results.

## Stage-boundary correction review

This correction changes documentation and stage assignments only. The Azure quota findings,
spending estimates, image audit, 89-test result, local configuration passes and all pending
approvals above remain unchanged and have not been promoted to cloud acceptance. A1 must
resolve the exact subscription/resource group/RBAC, selected region/SKU and zero-family-quota
remedy, approved private loopback tunnel/egress, final applicable quote/ceiling and named
window/deallocation/residual-retention owner. A2 remains separately required for relevant
identity/network administration; A3–A5 remain independently required for later live testing.
Stop here for those operator decisions. No Azure resource, identity, provider permission,
financial authority, application code or historical committed report was changed.

Correction validation passed: eight substantive evidence sections match the original
preparation report, with only the planned execution-stage label changed in the operator
packet. All original temporary artifact paths and outcome/price rows are preserved. All
91 local Markdown links resolve, no stale links to the former uncommitted 19C filenames or
secret-payload patterns were found, and `git diff --check` passed. Historical committed
19A/19B prompts/reports have empty diffs. Manual review confirmed the revised boundaries
in the prompt, report, README status/roadmap, plan, architecture and operations guidance.
Application tests, Azure discovery, pricing and paid/provider checks were not rerun for
this documentation-only correction.

## Git status and file inventory

Only these six documentation files are in the reclassified Phase 19B continuation change set:

- `README.md`
- `docs/evaluation/phase_19_deployment_architecture.md`
- `docs/evaluation/phase_19_implementation_plan.md`
- `docs/operations/phase_19_vm.md`
- `docs/codex/prompts/phase_19b_live_deployment_readiness_continuation.md` (new)
- `docs/codex/reports/phase_19b_live_deployment_readiness_continuation.md` (new)

Preparation handoff before the stage-boundary correction: `master...origin/master`, four modified tracked Markdown files and two untracked
Markdown files, nothing staged. `git diff --stat`: **4 files changed, 53 insertions(+),
1 deletion(-)**. It covers the four tracked files only; the two new files are intentionally
untracked and listed separately. No commit or push occurred.

After the stage-boundary correction, `git status --short --branch` remains
`master...origin/master`, with four modified tracked Markdown files and the two renamed
untracked continuation Markdown files listed above; nothing staged. Current `git diff --stat`:
**4 files changed, 107 insertions(+), 8 deletions(-)**, excluding the two untracked files.
No stage, commit, push, cloud mutation or identity administration occurred.
