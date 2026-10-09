# Phase 17G — Multi-User Security, Quotas & Cost Governance

Date: 2026-10-08. Verification closure: 2026-10-09. Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`.
Authority: [normalized prompt and continuation](../prompts/phase_17g.md).
Design: [readiness decisions](phase_17g_design.md).
Operations: [configuration and composition contract](../../security/phase_17g.md).

## 1. Executive summary

Phase 17G adds a provider-independent identity and authorization boundary,
same-tenant document grants, security epochs, scoped conversation-memory access,
authorized publication retrieval, durable owner/tenant token and cost admission,
versioned operator pricing, and known/unknown usage accounting. Logical deletion
denies access independently of publication rollback. Existing inference, job,
publication, vector and memory implementations remain the underlying ports.

The work remains uncommitted and unstaged. No cloud deployment, live Foundry
inference, identity provisioning or Kubernetes operation was performed.

## 2. Phase result and acceptance boundary

**Phase 17G — PASS within the explicitly accepted single-host local/reference
scope.** Final closure verified the security-critical invariants and readiness,
corrected schema-drift readiness, and completed **690 tests in 94.03 seconds** with
no failures or skips. Lightweight validation passed. No unresolved mandatory
application-level bypass was identified in the supported boundary. This is not
production/public-user approval or certification of unsupported storage quotas,
physical purge, distributed authorities or live Foundry behavior. Section 26
records the acceptance matrix and exact closure evidence.

A complete suite passed **650 tests in 77.90 seconds** at an earlier implementation
snapshot. Further implementation/test edits followed, including accounting
identity hardening, additional workflow tests and readiness checks. A focused run
launched before the last five-file edit completed with **77 passed in 23.51
seconds**. The test command launched after those five edits completed with **46
passed in 9.17 seconds**, including the new direct-graph security bypass test.
These overlapping results must not be added together or described as a final
full-suite count.

The 2026-10-09 closure supersedes the earlier no-rerun checkpoint: it adds
19 readiness cases and three targeted adversarial cases, corrects schema-drift
readiness, and runs the complete suite once. See section 26 for final measured
results and the bounded local acceptance matrix. Historical results above remain
snapshot evidence and are not summed. Docker and Helm were not rerun.

Two deliberate runtime restrictions remain: legacy query/stream execution is
refused in OIDC mode, and physical purge remains **PURGE_PENDING**. Neither is
hidden behind a multi-user deployment or verified physical-deletion claim.

## 3. Starting Git baseline

Implementation began on clean `master` at
`76ec11c79ff8d80467a3e14935d7ce06da4ce3bb`, matching the expected Phase 17F commit.
Initial `git status --short --branch` showed only `## master...origin/master`.
HEAD, five-commit history and initial `git diff --check` matched the operator's
requirements. The external baseline directory
`/tmp/polymind-phase17g-baseline` contains HEAD/status/diff observations, inventory
and SHA-256 hashes for **241 tracked files**. Existing Phase 17F history was
preserved; no normalization/reset operation was used.

## 4. Assessment and design

Inspection established that shared bearer authentication covered query/memory but
omitted `/documents/analyze`; caller session IDs reached memory unchanged; legacy
RAG lacked ownership authority; Phase 17F manifests bound exactly one owning
Scope; bounded provider execute returned optional usage, while legacy generation
returned only text/chunks; and immutable object/vector ports lacked safe complete
per-document deletion. These findings drove the design record.

Security composes existing boundaries rather than replacing them:

```text
verified JWT -> immutable Principal -> durable authorization snapshot
             -> authorized owning publication and selected retrieval
             -> owner/tenant reservation -> Phase 17E provider admission
             -> bounded provider execute -> reconciliation
             -> final authorization and guarded response release
```

No document-job schema, provider protocol, publication metadata schema, vector
database, memory backend or scheduler was replaced. SQLite reference databases
use private files, schema checks, foreign keys and short immediate transactions.
They are not production distributed authorities.

## 5. Authentication and configuration

`API_AUTH_MODE` supports disabled/static_bearer/oidc_jwt. Leaving it unset preserves
the original API_AUTH_ENABLED contract. Static bearer remains a shared internal
credential, never a user identity. OIDC requires complete issuer/JWKS configuration,
security authority and enabled governance, with conflicting legacy token settings
rejected. Production retains its external-service/authentication/docs/model gates.

`OIDCVerifier` uses PyJWT and cryptography for RS256 signature verification. The
operator chooses exact issuer, audience, fixed HTTPS JWKS URL, tenant/role/purpose
claim mapping and allowed role permissions. The verifier validates signature,
algorithm/key type, kid, issuer, audience, expiration, nbf, subject, tenant and
purpose. Only bounded public RSA key sets are accepted. Redirects, environment
proxy use, token key URLs and embedded-key headers are disallowed. Controlled
refresh supports rotation without token-controlled network targets.

Synthetic locally generated RSA/EC fixtures exercise valid tokens, expiry, future
nbf, issuer/audience/signature errors, absent/malformed subject/tenant/role claims,
unsupported algorithms, none, key confusion, unknown kid, malicious headers,
oversized/malformed/static tokens, JWKS outage and rotation. The maintained API
was checked against [PyJWT documentation](https://pyjwt.readthedocs.io/en/stable/api.html).
No live identity provider was contacted for verification. Private signing keys
are generated only in test memory; none is stored as a repository credential.

## 6. Principal mapping and authority

Principal construction is restricted to the server verification boundary and
uses immutable fields. Versioned domain-separated UUIDv5 mapping includes issuer,
external tenant and subject, preserving canonical Scope while preventing request
scope overrides. Different issuer/tenant/subject tuples produce separate scopes.
Identity naming does not grant access to old arbitrary-scope artifacts.

`SecurityAuthority` durably registers verified identities and trusted canonical
document ownership. Missing/unknown actions or ownership deny access. Role
permissions come only from verified issuer claims and an operator-approved map.
Same-tenant administrators can disable principals; old request snapshots and
subsequent token registration then fail. No HTTP principal constructor, password
store, login, refresh issuance or public registration flow was added.

## 7. Sharing and cross-owner publication

Owners or approved same-tenant administrators can create/revoke READ/ANALYZE grants
to registered same-tenant principals. Compatible duplicates are idempotent.
Shared users cannot reshare, delete or administer publication. Cross-tenant and
unregistered-grantee requests are denied without resource-existence detail.

`AuthorizedAnalysis` maps authorized document ownership to an operator-supplied
registry of original-owner DocumentAnalysis services. Canonical objects remain
with their owners. V1 rejects mixed-owner selections before publication lookup;
an individually shared document remains usable. Paths and generations are never
constructed from a client owner/tenant override.

## 8. Dense, sparse, RRF and citation isolation

Authorization precedes pinning and search. Existing Chroma generation/document
filters constrain dense candidates before top-k. Generation identity already
contains canonical scope; the trusted ownership/registry check supplies the scope
binding without changing publication/1 metadata or old accepted rows.

Replica load additionally builds immutable per-document BM25 indexes. Authorized
requests score selected documents only, excluding unauthorized corpus statistics
from their sparse ranking. No request-time rebuild is introduced. Legacy scoring
remains unchanged when using the legacy trusted publication path.

Existing RRF, reranker identity checks and canonical evidence resolution remain.
Secure selected validation avoids opening unrelated canonical documents for
request validation. Tests observe dense filters and provider context, verify
denial before search/provider work and prove shared access resolves owner scope.
Final authorization accompanies provenance validity; semantic entailment remains
outside this phase.

## 9. Session and legacy execution policy

`ScopedMemory` derives a versioned SHA-256 effective key from tenant, owner and
visible session ID. Reads, appends and clears are authority-guarded for both file
and Redis implementations. Returned file messages omit internal session keys.
Synthetic Alice/Bob/Carol sessions remain separate; old unscoped history is not
adopted. Disabling a principal blocks read/write/clear and re-registration.

OIDC `/query` and `/query/stream` fail closed before graph execution. Router,
generation helpers and factory-created governed providers also refuse unsafe
unbound legacy execution. This is an intentional compatibility restriction:
legacy RAG has no private-document authority and legacy generation cannot provide
the required bounded attribution. Local/static query and NDJSON paths remain.
No Streamlit login or authenticated legacy-memory migration was introduced.

## 10. Revocation, streaming and release guarantees

Authorization snapshots bind principal state, selected documents, owning scopes,
document epochs and policy version. Grant changes/tombstones invalidate snapshots.
Controlled synchronization tests pause provider execution, commit revocation or
tombstone, then complete inference: no protected answer/citations return, while
measured upstream usage remains settled.

Middleware guards actual output release with a short local SQLite transaction.
Revocation committed before release prevents subsequent protected bytes. Each
send is bounded to five seconds. A started stream is terminated on later denial;
bytes already sent remain delivered. Tests exercise both pre-header denial and
revocation between body emissions. These are ASGI release-boundary tests, not
claims of governed upstream token-streaming support. Governed legacy token
streaming is refused rather than counted using character estimates.

## 11. Publication and job administration

`AuthorizedPublication` requires PUBLICATION_MANAGE and matching tenant; OIDC
publication-service mutations also demand explicit authorization. No public
publish/activate/rollback route exists. `AuthorizedJobs` resolves jobs through
trusted DocumentJobs using the principal's own scope, checks document access and
restricts cancellation. Tests cover owner job lookup, foreign read/cancel denial,
ordinary-user admin denial and trusted reconciliation.

Security state is separate from publication history. A tested G1 -> G2 removal ->
tombstone -> G1 rollback sequence still denies document access. Other untombstoned
documents remain usable.

## 12. Hierarchical quotas and pricing

`GovernanceLedger` checks owner and tenant limits atomically. Policies require
explicit request-window, interactive/background inference concurrency, outstanding
token-reservation, daily/monthly token and monthly monetary limits. The implemented
concurrency dimension counts inference attempts, not queued/running jobs. Stored
document count, byte/page/storage ceilings and total job concurrency remain
unsupported v1 dimensions; no comprehensive-storage-quota claim is made.

Pricing is versioned, operator-approved and model/provider-specific, with one
currency, an effective date and nonnegative decimal-string unit prices. Decimal
power-of-ten units preserve finite exact decimal calculations. Missing pricing,
model mismatch, invalid catalog/policy or conflicting persisted configuration
fails closed. No current cloud price was hard-coded or assumed.

Simultaneous 8-unit reservations against a 10-unit owner or tenant budget produce
exactly one admitted row. Rejected governance execution makes no provider call.
Attempt keys bind job/step/attempt independently of descriptive profile metadata;
changed metadata cannot create a second execution for the same logical attempt.

## 13. Provider admission and managed digestion

`GovernedExecution` reserves before existing InferenceAdmissionPort acquisition,
then executes the bounded provider once. Conservative serialized-byte input
estimates include configured overhead/safety, and explicit output limits are
checked before admission. These are conservative reservations, not provider bill
guarantees. No fallback model or second retry scheduler was added.

ManagedSynthesisInference accepts explicit governed composition. Its handler
verifies owning principal/document binding while retaining Phase 17C lease/fence,
checkpoint and retry semantics. Missing governed context refuses execution in
governed mode. Integration tests verify all completed stages appear once in both
ledgers, quota denial preserves prior checkpoints with zero provider calls, and
cancellation after paid work preserves usage without accepting cancelled output.
Governance/security job failures are sanitized non-retryable categories.

## 14. Usage and crash accounting

Reservations record scope, workload, attempt identity, policy/catalog, provider,
model, estimated input, reserved output/cost, measured counts/cost when known,
state and time. Admission is idempotent; execution claiming prevents duplicated
upstream calls; repeated identical settlement does not double-charge. Genuine
retry attempts retain separate rows.

Provider-admission rejection before execution releases unspent governance state.
After execution may start, cancellation, timeout or incomplete usage retain
measured expense or conservative unknown reservations. Unknown usage survives
restart and period rollover, and consumes outstanding token capacity. Later
trusted measured settlement can reconcile it. No TTL turns unknown into zero.
Abandoned pre-execution/started records remain for trusted investigation; no
automatic release/recovery daemon is supplied.

Own usage is bounded and scoped. Tenant administrators have a trusted aggregate
reader; ordinary users cannot select another owner. Detailed accounting stays
outside Prometheus labels.

## 15. Tombstones and physical purge

Deletion records DELETE_REQUESTED and TOMBSTONED in one transaction, advances
security epoch and revokes grants. Duplicate requests preserve the tombstone.
Trusted purge tracking records required artifact classes and a durable
PURGE_PENDING reason. Restart/idempotency and continued denial are tested.

No physical delete adapter or complete shared-reference inventory is available.
Therefore no source, checkpoint, manifest or vector is destructively removed, no
collection is reset and **PURGED is never returned**. This conservatively avoids
collateral deletion or silent corruption of accepted generations. It is tracked
blocked local purge, not completed erasure or backup/provider deletion
certification. Comprehensive partial-physical-purge interruption scenarios cannot
be certified without those adapters.

## 16. Audit, privacy and readiness

Security audit rows contain bounded opaque identifiers, allowlisted actions and
outcomes, timestamps and policy version. Required mutation audit shares the state
transaction; capacity failure rolls back mutation. Denied mutations also attempt
sanitized audit recording. Append-only audit capacity fails closed rather than
silently deleting history. Governance has a separate content-free event ledger.
Neither is tamper-proof or compliance-certified.

Validation errors are bounded instead of reflecting invalid input. Streaming
failure logs no longer include session IDs or arbitrary exception tracebacks for
the changed paths. No identity/content/account IDs were added as Prometheus labels.
Docker context now excludes local authority database files and sidecars.

Health remains liveness. Readiness composes existing dependency/publication gates
with configured authorized analysis, security/governance/provider-admission
databases, audit capacity and JWKS freshness. The final five-file edit added
database/capacity readiness composition. Its source completion was confirmed at the prior checkpoint. Closure now
exercises unavailable databases, audit capacity, JWKS and composition, including
schema/version drift after startup; see section 26.

## 17. Internal checkpoint status

| Checkpoint | Recorded outcome |
| --- | --- |
| G1 | Clean baseline, implementation inspection, external hashes and design record completed |
| G2 | Identity, endpoint correction, authority and synthetic verification tests implemented |
| G3 | Sharing, owner-publication resolution, retrieval/session isolation and revocation tests implemented |
| G4 | Transactional governance/pricing and managed provider-admission composition implemented and focused tests passed |
| G5 | Tombstones, audit and durable blocked purge tracking implemented; physical deletion intentionally remains pending |
| G6 | Historical regression and focused evidence preserved; final closure results and acceptance matrix recorded in section 26 |

This table records delivered work without claiming the original exhaustive
adversarial matrix has been independently satisfied in every dimension.

## 18. Historical test evidence

The following results came from completed commands in this session. No completed
test group was repeated during continuation finalization.

| Executed scope | Measured result | Timing/meaning |
| --- | --- | --- |
| Initial endpoint/API reliability | 19 passed in 0.69 s | Early middleware correction |
| Identity/API/deployment foundation | 72 passed, 1 failed in 20.05 s | Test fixture rejected malformed kid during token creation; corrected subsequently |
| Identity/API/publication/streaming | 104 passed in 24.72 s | After fixture correction and initial integration |
| Authority/governance | 15 passed in 1.21 s | Early reservation/isolation checks |
| Managed inference/digestion regressions | 46 passed in 8.71 s | Existing managed contracts |
| Publication security | 4 passed in 2.96 s | Retrieval, paused-provider revocation/tombstone and rollback |
| API security | 10 passed in 6.75 s | Authentication and ASGI release guards |
| Complete pytest suite | **650 passed in 77.90 s** | Earlier snapshot; not final-tree certification |
| Accounting/identity/API/publication affected checks | 54 passed in 13.85 s | After reservation-identity/token-capacity corrections |
| Authority/configuration/publication security | 24 passed in 6.58 s | Additional ownership/configuration/admin checks |
| Governed digestion integration | 3 passed in 2.83 s | Both ledgers, budget denial and cancellation |
| Focused Phase 17G group | **77 passed in 23.51 s** | Launched before final five-file edit; log recovered during continuation |
| API security + managed-inference unit tests | **46 passed in 9.17 s** | Launched after final five-file edit; includes new direct-graph helper test; result recovered during continuation |

The malformed-kid failure was a fixture issue, not a bypass: the JWT encoder
refused the header before verification. The corrected fixture changes the encoded
header directly, and subsequent identity runs passed. No expected final total was
manufactured. The final closure result is recorded separately in section 26.

## 19. Build and validation evidence

Before later edits, external-cache compileall exited 0, Docker Compose
`config --quiet` exited 0, offline Helm lint/template exited 0 (icon recommendation
only), and diff whitespace checks passed. No configured Ruff/Flake8/mypy or other
standalone lint/type gate was found; none was installed or invented.

The cached Docker build initially encountered sandbox Docker-socket permission
denial, then succeeded through the execution approval mechanism. Its completed
log records image manifest-list digest
`sha256:f4c8c1db9ce154a4c46566d6a0464d64e20398e140e2e3e7fe78819985e7cc00`.
It used normal cache and no additional validation tag, prune, image deletion or
unrelated service rebuild. The build context was captured before later source and
Docker-ignore edits; that successful image is not claimed to contain final code.

Dependencies added were PyJWT 2.15.0, cryptography 50.0.2 and its cffi 2.1.1 /
pycparser 3.0 support dependencies. The existing environment lacked JWT and
cryptography support. Installation was explicitly approved through the execution
policy. No GPU/runtime/cloud SDK or unrelated framework was added.

At the earlier continuation checkpoint, no tests, Docker build, Compose/Helm/compile
checks or previously completed source inspection were rerun. Only pending process results, the
uncertain final method additions, new documentation and outstanding pre-commit/
Git handoff were examined.

## 20. Self-review findings and corrections

Implementation review corrected the missing document endpoint classification,
unscoped sparse statistics in authorized requests, unrestricted legacy graph
execution, duplicate logical-attempt identity dependent on profile metadata,
unknown usage escaping outstanding token capacity, publication administration
without explicit OIDC authority, audit-denial handling, database-capacity
readiness wiring, invalid-input reflection and authority database Docker-context
exposure. Tests were added/run during implementation as recorded above.

The last five-file patch was applied successfully before interruption. The earlier continuation
confirmed the new methods and recovered the already-running test results rather
than applying it again. No production code correction was made during
continuation; the remaining work was documentation/review/handoff.

## 21. Pre-commit review scope

Prior architecture and focused test review evidence was reused. Outstanding
finalization review checks changed/new file inventory, obvious credential/private-
key material, runtime/generated artifacts, dependency scope, documentation links,
index state and whitespace. Synthetic keys are generated in memory. Operator
paths in `.env.example` are documentation placeholders, not machine-specific
credentials. Temporary baseline/build/test artifacts remain outside the repository.
Final automated scan and Git observations are appended below.

The review is not a penetration test. Section 26 records executable closure
evidence; source inspection is not treated as executable proof or exhaustive
crash/race certification.

## 22. Remaining limitations and verification gaps

- The historical 650-test pass predates later code. Final suite/readiness and
  lightweight validation evidence is in section 26. The cached Docker image still
  predates final code; a final-image build was explicitly excluded from closure.
- Original mandatory matrices exceed the recorded tests: exhaustive malformed
  JWKS variants, all crash boundaries, every quota dimension and every API/job/
  retention combination are not certified by the available results.
- OIDC legacy query/stream paths remain disabled. No governed token streaming,
  Streamlit identity login, legacy-memory adoption or automatic document-memory
  persistence is implemented.
- Sharing is same-tenant only; mixed-owner selections are refused. Operator
  registration/composition is required; no user onboarding/upload exists.
- Physical erasure remains PURGE_PENDING. Safe complete reference inventories
  and per-artifact deletion/reconciliation need further approved work before any
  PURGED claim. There is no legal-hold or automatic retention scheduler.
- SQLite is single-host reference infrastructure. Distributed authorization,
  admission, revocation-release semantics, host hardening and production rollout
  remain unproven. Audit capacity requires operator management; no archival daemon
  or online catalog/policy migration is included.
- Concurrency quotas cover inference attempts. Storage quotas and total queued/
  running job counts are unsupported. Byte estimates are conservative assumptions,
  not measured provider billing ceilings. External upstream consumers are outside
  the quota boundary.
- Worker execution requires a valid owner-bound principal context; long-lived
  service delegation is not implemented. Unknown/crashed attempts require trusted
  reconciliation and are not automatically refunded.
- Live Azure Foundry document digestion remains **BLOCKED / PENDING**. No new
  real-model, 200–1000+ page, semantic-quality or external-user claim is made.

## 23. Documentation and next-phase prerequisites

The operator contract documents every new setting, composition prerequisite,
identity namespace, supported policy dimension and intentional restriction. The
README was updated minimally, preserving badges, organization and historical
Phase 16–17F results. Prompt, design and report artifacts are retained under
docs/codex. Historical reports were not rewritten.

The operator authorized bounded verification closure on 2026-10-09; section 26
records its acceptance decision. Final diff review and commit/push remain with the
operator. No next phase was started. Phase 17H remains **200–1000+ Page Reliability, Failure & Quality
Validation**: long documents, concurrent users/jobs, isolation/revocation under
load, budget exhaustion, provider 429/timeouts, crash/retry recovery, large-corpus
publication, citation relevance/faithfulness and contradiction/qualification
retention. Live Foundry validation requires a separately approved bounded scope.
Phase 17I external-user verification remains not started.

## 24. Git and prohibited-action confirmation

Commit created: **NO**. Push performed: **NO**. Branch created: **NO**.
Files staged: **NO**. Azure mutation: **NO**. AKS/Kubernetes mutation: **NO**.
Foundry capacity change: **NO**. Live Foundry calls: **NO**.
Cloud Chroma reset/restart: **NO**. Cloud Redis reset/restart: **NO**.
External identity provisioning: **NO**. Production database provisioning: **NO**.
Phase 17H implementation: **NO**. Phase 17I implementation: **NO**.

The final inventory and Git command results follow. `git diff --stat` excludes
untracked additions, which are listed separately. All work is for operator review.

## 25. Historical pre-commit and Git handoff evidence

The outstanding heuristic scan covered **39 changed/new files** and found no
private-key blocks, credential-shaped literals, runtime/environment artifacts,
machine-specific home paths, broken local documentation links or new-file trailing
whitespace. This is a bounded pattern/link scan, not a secret-scanner certification.

Modified tracked files (**17**):

```text
.dockerignore
.env.example
README.md
api/app.py
api/security.py
config/settings.py
documents/digestion/managed.py
documents/jobs/errors.py
documents/publication/analysis.py
documents/publication/retrieval.py
documents/publication/service.py
graph/generation.py
graph/nodes.py
graph/streaming.py
llm/admission.py
llm/provider_factory.py
requirements.txt
```

New untracked files (**22**), excluded from Git diff stat:

```text
docs/codex/prompts/phase_17g.md
docs/codex/reports/phase_17g_design.md
docs/codex/reports/phase_17g_report.md
docs/security/phase_17g.md
governance/__init__.py
governance/execution.py
governance/ledger.py
security/__init__.py
security/authority.py
security/database.py
security/identity.py
security/memory.py
security/models.py
security/runtime.py
security/services.py
tests/integration/test_governed_digestion.py
tests/unit/publication/test_security.py
tests/unit/test_governance.py
tests/unit/test_security_api.py
tests/unit/test_security_authority.py
tests/unit/test_security_configuration.py
tests/unit/test_security_identity.py
```

Deleted files: **none**.

Final committed HEAD: `76ec11c79ff8d80467a3e14935d7ce06da4ce3bb`.

`git status --short --branch` — exit 0:

```text
## master...origin/master
 M .dockerignore
 M .env.example
 M README.md
 M api/app.py
 M api/security.py
 M config/settings.py
 M documents/digestion/managed.py
 M documents/jobs/errors.py
 M documents/publication/analysis.py
 M documents/publication/retrieval.py
 M documents/publication/service.py
 M graph/generation.py
 M graph/nodes.py
 M graph/streaming.py
 M llm/admission.py
 M llm/provider_factory.py
 M requirements.txt
?? docs/codex/prompts/phase_17g.md
?? docs/codex/reports/phase_17g_design.md
?? docs/codex/reports/phase_17g_report.md
?? docs/security/phase_17g.md
?? governance/
?? security/
?? tests/integration/test_governed_digestion.py
?? tests/unit/publication/test_security.py
?? tests/unit/test_governance.py
?? tests/unit/test_security_api.py
?? tests/unit/test_security_authority.py
?? tests/unit/test_security_configuration.py
?? tests/unit/test_security_identity.py
```

`git diff --stat` — exit 0:

```text
 .dockerignore                      |   6 +++
 .env.example                       |  16 ++++++
 README.md                          |  32 ++++++++---
 api/app.py                         | 107 +++++++++++++++++++++++++++++++++++--
 api/security.py                    |  76 +++++++++++++++++++++++---
 config/settings.py                 |  40 +++++++++++++-
 documents/digestion/managed.py     |  31 ++++++++++-
 documents/jobs/errors.py           |   1 +
 documents/publication/analysis.py  |  13 +++--
 documents/publication/retrieval.py |  56 +++++++++++++++++--
 documents/publication/service.py   |  58 +++++++++++++++-----
 graph/generation.py                |   9 ++++
 graph/nodes.py                     |   4 ++
 graph/streaming.py                 |   9 ++--
 llm/admission.py                   |   7 +++
 llm/provider_factory.py            |   8 +++
 requirements.txt                   |   4 ++
 17 files changed, 427 insertions(+), 50 deletions(-)
```

`git diff --check` — exit 0:

```text
(no output)
```

`git diff --cached --name-only` returned no paths (exit 0); the index is unchanged.

The report appendix itself is an unstaged, untracked documentation addition;
its completion does not change the tracked diff stat or file inventory above.
No test/build/configuration validation was repeated during this finalization.
**The prior checkpoint verdict was PARTIAL. Section 26 supersedes it with closure evidence.**

## 26. Final verification and acceptance closure — 2026-10-09

### Scope and essential correction

The closure began on `master` at the expected
`76ec11c79ff8d80467a3e14935d7ce06da4ce3bb`, with an empty index and exactly the
recorded 17 modified tracked / 22 untracked files. No reset, cleanup or restoration
was needed. Existing architecture and successful test evidence were reused.

New executable probes exposed one defect: SQLite `quick_check` can succeed even
when the authority's application schema is incompatible. All three authorities
reported ready after a post-construction schema/version change. The smallest fix
stores the already-required schema definition and compares it, plus user_version,
in `security/database.py` and `llm/admission.py` readiness. This covers security,
governance and provider admission without migration, schema mutation, interface
changes or provider-specific logic. SQLite connections remain bounded by existing
transactions and close on error. Failures yield false readiness and the API's
existing sanitized 503 response. Only synthetic temporary databases were altered.

### Readiness verification

`tests/unit/test_security_readiness.py` adds **19 cases**:

| Branch | Cases | Final result |
| --- | ---: | --- |
| Security/governance/provider-admission database becomes unavailable | 3 | VERIFIED: component and runtime return false |
| Incompatible schema or user_version after startup, each authority | 6 | VERIFIED after essential readiness correction |
| Security audit and governance event capacity exhausted | 2 | VERIFIED: component and runtime return false |
| Fresh trusted JWKS, stale JWKS with unavailable refresh, unusable JWKS | 3 | VERIFIED: only fresh trusted state succeeds |
| API authorized-analysis composition: usable, absent, empty registry, unready publication, absent runtime | 5 | VERIFIED: usable composition returns 200; other cases return sanitized 503 |

Every fixture first asserts that the real local SecurityRuntime is ready with
usable databases, available audit capacity and synthetic public JWKS. API tests
stub unrelated dependencies; authorized-analysis composition itself is exercised.
No live identity-provider or inference endpoint is used.

Initial targeted run: **13 passed, 6 failed in 10.54 s**. All failures were the
schema-drift defect above. After correction, only those six readiness cases were
rerun: **6 passed, 16 deselected in 1.09 s** (the selection also excluded three
explicitly named adversarial tests). The three adversarial tests then ran by exact
node ID: **3 passed in 0.80 s**. Thus all **19 new readiness cases** and **3 new
adversarial cases** have passing evidence, with all rerun together in the final
complete suite. These counts overlap the complete suite and must not be added to
its total. The previously successful 46-test and 77-test groups were not rerun.

### Security-critical acceptance matrix

Paths below are relative to `tests/`. VERIFIED denotes sufficient executable
evidence for the supported single-host local boundary, not exhaustive malicious
host, network timing, live-provider or distributed certification. Assessment
identified duplicate execution, equal missing/foreign errors and authorized
reranker injection as NEEDS TARGETED TEST; all three are now VERIFIED by the new
cases. No assessed in-scope invariant remains NEEDS TARGETED TEST or BLOCKED.

| Invariant | Classification | Executable evidence / boundary |
| --- | --- | --- |
| Invalid/unverified JWT cannot construct Principal | VERIFIED | `unit/test_security_identity.py`: claims, signature, algorithm/key confusion, headers, malformed tokens, constructor refusal |
| Client cannot override tenant/owner Scope | VERIFIED | `test_valid_immutable_server_scope_and_cache`; API uses verified middleware principal |
| Cross-tenant/unauthorized access denied before retrieval | VERIFIED | `publication/test_security.py::test_real_analysis_denies_before_search_or_provider_and_shared_owner_resolution` under `unit/` |
| Shared user cannot delete, reshare or publish | VERIFIED | Authority sharing/action matrix; publication administration test requires approved permission |
| Missing and foreign documents have equal errors | VERIFIED | New `unit/test_security_authority.py::test_missing_and_foreign_documents_have_identical_denials`; includes same- and cross-tenant documents; no timing-equivalence claim |
| Dense filter applied before top-k | VERIFIED | Publication security test observes selected document filter; scoped fake vector port filters before slicing; production adapter contract remains existing boundary |
| BM25 restricted before ranking | VERIFIED | Authorized publication test disables whole-corpus scoring and succeeds using isolated document indexes |
| RRF/reranker cannot insert unauthorized records | VERIFIED | Existing retrieval provenance tests plus new `unit/publication/test_security.py::test_authorized_reranker_cannot_insert_unselected_record`; foreign insertion denied before provider |
| Canonical citations require current authorization | VERIFIED | Canonical/citation tests plus paused-provider revoke/tombstone tests and final release guard |
| Rollback cannot bypass tombstones | VERIFIED | `test_rollback_never_restores_revoked_or_tombstoned_access` |
| Revocation during inference blocks protected final answer | VERIFIED | Paused provider synchronization with revoke and tombstone; measured usage remains settled |
| Already emitted bytes are not retractable | VERIFIED | `unit/test_security_api.py::test_stream_revocation_blocks_future_bytes_after_acknowledgement` explicitly preserves earlier bytes |
| Revocation blocks subsequent protected output | VERIFIED | Same streaming test and `test_final_release_blocks_after_analysis_before_response_start` |
| Identical client session IDs isolated across principals | VERIFIED | Scoped file/Redis memory test and domain-separated session identity test |
| Legacy unscoped memory never automatically adopted | VERIFIED | Scoped memory test preserves legacy history separately and begins each principal history empty |
| OIDC query/stream/direct graph helpers cannot bypass policy | VERIFIED | API legacy refusal and direct-helper tests; these endpoints remain intentionally disabled |
| Concurrent owner/tenant reservations cannot overspend | VERIFIED | `unit/test_governance.py::test_atomic_eight_of_ten_reservation_race`, both owner and tenant cases |
| Budget denial prevents provider execution | VERIFIED | Governance denial unit test and governed-digestion exhaustion integration test |
| Duplicate logical attempts do not execute or charge twice | VERIFIED | Ledger duplicate/settlement tests plus new `test_duplicate_execution_calls_provider_and_charges_once` asserts one provider call and one settled charge |
| Unknown usage remains reserved/unsettled | VERIFIED | Restart/period-rollover/reconciliation and provider-timeout tests |
| Cancellation preserves incurred usage | VERIFIED | `integration/test_governed_digestion.py::test_cancellation_after_paid_work_preserves_both_ledgers` |
| Tombstones deny access durably | VERIFIED | Authority restart/idempotency and publication rollback tests |
| Deletion cannot expose another owner's artifacts | VERIFIED | Action/scope denial matrix; untouched owner remains readable; no physical deletion adapter invoked |
| Physical purge never falsely reports completed | VERIFIED | Authority and rollback tests assert durable PURGE_PENDING; no PURGED result |
| Complete physical erasure | BLOCKED | Safe retained-generation/shared-reference deletion inventory and adapters absent; PURGE_PENDING is truthful and intentional |
| Storage quotas and total queued/running-job quotas | OUT OF SCOPE | Unsupported dimensions explicitly excluded by closure scope; inference-attempt/token/cost limits remain enforced |
| Distributed multi-replica authority, public external-user approval | OUT OF SCOPE | Trusted single-host SQLite reference only; no rollout approval |
| Mixed-owner analysis, OIDC legacy execution | OUT OF SCOPE | Mixed-owner selection and legacy execution deliberately refused |
| Live Foundry digestion | BLOCKED / PENDING | Requires separately authorized bounded live validation; no paid call in closure |

This classification follows the closure prompt's explicit local/reference scope.
It does not retroactively claim every feature of the original broader phase
prompt is implemented. Unsupported features are named above and in section 22.

### Final complete regression and lightweight validation

`python -m pytest -q` was run **exactly once** during closure and exited 0:

```text
690 passed in 94.03s (0:01:34)
```

**Failures: 0. Skips: 0. No warnings were reported in the pytest output.**
The final suite includes all 19 new readiness cases and three additional
adversarial cases.

The earlier **650 passed in 77.90 s** remains historical snapshot evidence.
The final run occurred after all production and test changes. Only report text
was updated afterward; no second complete suite was run. No skips or warnings
were hidden or converted into passes.

- `PYTHONPYCACHEPREFIX=/tmp/polymind-phase17g-pycache python -m compileall -q .`: completed without errors using external bytecode cache.
- `docker compose config --quiet`: completed without errors.
- `git diff --check`: passed; final report/Git handoff checks follow below.
- Installed PyJWT 2.15.0, cryptography 50.0.2, cffi 2.1.1 and pycparser 3.0 match requirements pins. Local package metadata checks confirmed active dependency constraints, including typing_extensions 4.15.0. Nothing was installed or upgraded.
- Docker build and Helm checks were deliberately not repeated. The historical cached image is not a final-source image certification.

### Bounded self-review and pre-commit review

The schema checks and all closure test additions were reviewed for error paths,
connection cleanup, compatibility, meaningful assertions and scope. No security
bypass, new public API, provider leakage, dependency or production configuration
change was introduced by closure. Historical full-source review was reused.

A bounded scan of all 40 changed/new files found no private-key block, serialized
JWT, credential-shaped literal, machine-specific home path, runtime database,
secret file or new-file trailing whitespace. Synthetic signing keys remain in
memory; probes contain no real access tokens. Existing audit functions still
write only allowlisted actions and opaque IDs, with no document or prompt input;
closure did not change audit payloads or response error content. This is a
heuristic review, not secret-scanner or penetration-test certification.

Inventory reconciles to **17 modified tracked + 23 untracked = 40 files**. The
only addition beyond the prior 39-file inventory is
`tests/unit/test_security_readiness.py`. Three existing untracked test modules were
extended; the schema-readiness correction modifies the existing untracked
`security/database.py` and tracked `llm/admission.py`. There are no deletions,
staged files, runtime artifacts or unrelated implementation changes. Report edits
preserve historical results and identify the previous PARTIAL checkpoint as such.

### Remaining limitations and Phase 17H handoff

OIDC legacy `/query` and `/query/stream` remain disabled; physical purge remains
**PURGE_PENDING**, never PURGED. There is no complete distributed security
authority, public external-user approval, guaranteed provider billing ceiling,
full cloud backup/provider deletion guarantee or Phase 17H semantic/large-document
certification. Live Azure Foundry document digestion remains **BLOCKED / PENDING**.
Mixed-owner analysis, storage quotas and total job concurrency remain unsupported.

Phase 17H should address long-document reliability and semantic/citation quality,
concurrent workload isolation/revocation, exhaustion and provider failure handling,
crash/retry recovery and large-corpus publication. Physical purge and distributed
security need separately scoped engineering before stronger claims. No Phase 17H
implementation, live cloud call, Azure/Kubernetes mutation or external-user test
was started. The operator retains final review and commit/push responsibility.

### Final Git command outputs

`git status --short --branch` — exit 0:

```text
## master...origin/master
 M .dockerignore
 M .env.example
 M README.md
 M api/app.py
 M api/security.py
 M config/settings.py
 M documents/digestion/managed.py
 M documents/jobs/errors.py
 M documents/publication/analysis.py
 M documents/publication/retrieval.py
 M documents/publication/service.py
 M graph/generation.py
 M graph/nodes.py
 M graph/streaming.py
 M llm/admission.py
 M llm/provider_factory.py
 M requirements.txt
?? docs/codex/prompts/phase_17g.md
?? docs/codex/reports/phase_17g_design.md
?? docs/codex/reports/phase_17g_report.md
?? docs/security/phase_17g.md
?? governance/
?? security/
?? tests/integration/test_governed_digestion.py
?? tests/unit/publication/test_security.py
?? tests/unit/test_governance.py
?? tests/unit/test_security_api.py
?? tests/unit/test_security_authority.py
?? tests/unit/test_security_configuration.py
?? tests/unit/test_security_identity.py
?? tests/unit/test_security_readiness.py
```

`git diff --stat` — exit 0:

```text
 .dockerignore                      |   6 +++
 .env.example                       |  16 ++++++
 README.md                          |  32 ++++++++---
 api/app.py                         | 107 +++++++++++++++++++++++++++++++++++--
 api/security.py                    |  76 +++++++++++++++++++++++---
 config/settings.py                 |  40 +++++++++++++-
 documents/digestion/managed.py     |  31 ++++++++++-
 documents/jobs/errors.py           |   1 +
 documents/publication/analysis.py  |  13 +++--
 documents/publication/retrieval.py |  56 +++++++++++++++++--
 documents/publication/service.py   |  58 +++++++++++++++-----
 graph/generation.py                |   9 ++++
 graph/nodes.py                     |   4 ++
 graph/streaming.py                 |   9 ++--
 llm/admission.py                   |  12 +++++
 llm/provider_factory.py            |   8 +++
 requirements.txt                   |   4 ++
 17 files changed, 432 insertions(+), 50 deletions(-)
```

`git diff --check` — exit 0:

```text
(no output)
```

`git diff --cached --name-only` — exit 0:

```text
(no output)
```

`git log -1 --oneline` — exit 0:

```text
76ec11c feat: implement Phase 17F RAG publication and document analysis
```

### Complete final changed-file inventory

`git diff --stat` excludes the untracked additions listed here.

```text
Modified tracked:
.dockerignore
.env.example
README.md
api/app.py
api/security.py
config/settings.py
documents/digestion/managed.py
documents/jobs/errors.py
documents/publication/analysis.py
documents/publication/retrieval.py
documents/publication/service.py
graph/generation.py
graph/nodes.py
graph/streaming.py
llm/admission.py
llm/provider_factory.py
requirements.txt

New untracked:
docs/codex/prompts/phase_17g.md
docs/codex/reports/phase_17g_design.md
docs/codex/reports/phase_17g_report.md
docs/security/phase_17g.md
governance/__init__.py
governance/execution.py
governance/ledger.py
security/__init__.py
security/authority.py
security/database.py
security/identity.py
security/memory.py
security/models.py
security/runtime.py
security/services.py
tests/integration/test_governed_digestion.py
tests/unit/publication/test_security.py
tests/unit/test_governance.py
tests/unit/test_security_api.py
tests/unit/test_security_authority.py
tests/unit/test_security_configuration.py
tests/unit/test_security_identity.py
tests/unit/test_security_readiness.py
```

Commit created: **NO**. Push performed: **NO**. Branch created: **NO**.
Files staged: **NO**. Azure mutation: **NO**. Kubernetes mutation: **NO**.
Paid provider call: **NO**. Phase 17H started: **NO**.

**Final Phase 17G verdict: PASS for the accepted local/reference scope.**
All changes remain uncommitted and unstaged for operator review.
