# Phase 19B — Local Identity Bootstrap Utility

27 November 2026. Project: Estudio PolyMind, repository
`Susanta2025-lab/estudio-polymind-llm-orchestration`, branch `master`.

Clean engineering scope record of the supplied **CODEX MASTER PROMPT — PHASE 19B**.
Operational credentials, actual subject values and private infrastructure inventory are
excluded. The supplied non-secret registration contract is retained in the narrowly scoped
implementation and the preceding OIDC/operational reports. This record preserves requirements;
it is not operational authentication, enrollment or execution authorization.

## Mission and boundaries

Investigate, design, implement and comprehensively verify offline a minimal local maintenance
utility that resolves the circular dependency between acquiring a verified Microsoft Entra API
access-token identity and production runtime initialization. Required identity:
`[issuer, tenant UUID, API access-token sub]`, with existing canonical tenant/owner derivation.
It must run in existing Windows/WSL development facilities without Azure activation, API/runtime
initialization, Redis, Chroma, production SQLite authorities, sources, providers, inference,
financial reservations or execution permissions.

Preserve 19A COMPLETE, 19B ACTIVE, 19C NOT_STARTED. Do not introduce another phase/subphase,
a production service, identity authority, authentication bypass, general token inspector,
automatic enrollment or replacement for native Streamlit OIDC/existing API verification.
Preserve Chat/RAG, Documents, security, governance/admission, finance, providers, persistence,
recovery, API and streaming contracts. Read root/applicable AGENTS.md and inspect actual source,
consumers, tests/configuration/docs before editing. Leave everything unstaged/uncommitted.

## Baseline and investigation

Before edits run `git status --short --branch`, `git rev-parse HEAD`,
`git log --oneline --decorate -10`, `git diff --stat`, `git diff --check`, and
`git diff --cached --name-only`. Reconcile supplied checkpoint
`b5f16926100ca1712f85c39f5fc579fbad88829d`, title
`docs: reconcile Phase 19B operational evidence and review Gate A readiness`.
Read-only CI reconciliation is allowed: Estudio PolyMind CI, master/push,
[run 45926112597](https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/45926112597),
reported success/11m46s.

Read the operational evidence reconciliation report, especially Gate A matrix/dependencies,
operator decisions, Gates B–E and final addendum; previous private HTTPS and native OIDC
preparation reports. Inspect actual identity/runtime/middleware, production manifest/storage/
lifecycle/UI/gateway, reusable TLS gateway, both frontend token consumers, Compose, Entra/VM
operations docs, existing stable_id domains, pinned Streamlit auth/session internals, secure
filesystem/exclusive-write patterns, Docker/dependencies and local launchers.

Independently confirm unknown API sub → enrollment/canonical owner → owner-bound source →
manifest → runtime/API readiness → UI → gateway → browser login → unknown API sub. Existing
production health dependencies must not be weakened. Determine whether a secure pre-existing
identity-only acquisition path exists before adding one.

## Architecture selection

Compare A: native WSL Streamlit plus loopback private TLS gateway; B: isolated minimal Docker
Compose UI/gateway; C: existing implemented path. Assess isolation/custody, Windows networking,
callback compatibility, native OIDC, gateway/verifier reuse, dependencies/complexity,
reproducibility/testability/teardown, accidental production-state access and browser/token risks.
Implement only the simplest secure option. Document rejection reasons and an actual architecture
with Windows browser → private HTTPS → local gateway → native Streamlit → Entra → API token →
existing verifier → verified principal → explicit protected enrollment candidate. Identify trust,
credentials/tokens, destinations, writable paths and lifecycle ownership.

Keep origin `https://polymind.test:9443`, callback `/oauth2callback`, exact Host
`polymind.test:9443`, exact WebSocket Origin, SAN DNS:polymind.test and TLS >=1.2. Investigate
Windows/WSL or Docker loopback reachability; do not assume it. Fail closed on port conflicts and
exclude simultaneous future Azure SSH forwarding. No public listener/DNS/forwarding/firewall
exception, wildcard origin, new redirect URI or disabled TLS verification. Reuse gateway factory;
any indispensable shared refactor must preserve interfaces/defaults, add regression tests and
reassess image provenance.

## Implementation contracts

Provide an explicit bounded maintenance entrypoint, no restart/production hooks/providers,
authorities/enrollment or synthetic fallback. Provide non-operational input preflight where useful.
Reuse native unnamed Streamlit OIDC and the supplied dedicated tenant/browser/API registration:
exact existing callback, tenant metadata, confidential browser client, privately supplied existing
Entra secret, `expose_tokens=["access"]`, and `openid api://<API-client>/access_as_user`.
Only `access_as_user` scope and exact `PolyMind.L1Operator` role. No Graph, extra consent,
registration/credential regeneration, implicit/public-client fallback or alternative provider.

Actual encrypted OIDC/client secret/production cookie/TLS key/CA/recovery archives stay outside
Codex access. Design a future operator-only procedure, justify/protect any short-lived plaintext,
never accept credential arguments/logs/shared temporary files/uncontrolled `.env`. Assess a
separate ephemeral bootstrap cookie while preserving the production cookie. Address shared
origin/native cookie names, stale cookies, session isolation and cleanup.

Select only native API access token; logged-in state alone is insufficient. Reuse actual
OIDCSettings/OIDCVerifier contract and preserve cryptographic signature/trusted keys/algorithms,
tenant v2 issuer/tid, bare API UUID audience, v2, exp/nbf/iat lifetime, delegated scope, exact role
set and subject validation. Investigate `azp`; if needed add exact bootstrap browser-client
binding without changing production semantics. Never trust solely unverified claims, ID-token
sub, directory oid, email/name, application/SP IDs or historical/different-client assumptions.
Fail closed on invalid/unavailable tokens/JWKS.

Canonical identifiers must reuse production stable_id/versioned domains byte-for-byte, preferably
verified Principal fields, without importing/constructing production runtime or registering a
principal. If pure-function extraction is indispensable, prove output compatibility.

Export only explicitly authorized fresh-verification evidence: schema/purpose, issuer/tenant/API
sub, canonical tenant/owner, API audience, verification/expiry UTC and execution_authorized=false.
No tokens, codes/cookies, secrets/full JWT/headers, email/name/unnecessary directory identifiers.
Absolute approved external destination, protected 0700 parent, 0600 operator-owned regular file,
one link, no symlink traversal/overwrite, safe partial-write/interruption handling, repeated/
concurrent protection; no Git/shared Windows default. This unsigned candidate is neither an
execution authority nor manifest; hashes alone do not prove authenticity/approval/current validity.

Provide minimal UI states for configuration, authorized login, failure/verification/export,
logout/expiry, with sanitized statuses and cleanup controls. Do not display tokens/subjects/full
claims or encourage copying to terminals/JWT websites. Cover reruns/clicks/concurrent sessions.
Review pinned native callback/state/nonce/code exchange/conditional PKCE, cookies, token exposure,
expiry/logout/multiple tabs/stale sessions/termination. Do not claim encryption/revocation or
memory/secure-deletion guarantees without evidence.

## Offline tests and regression

All identities/credentials/certificates synthetic. No Entra/Azure/provider/discovery/download/
telemetry/public listeners. Inject deterministic JWKS/discovery and signed JWTs; allow scoped
loopback integration only. Prove no transitive provider/runtime imports, authority constructors/
writes, Redis/Chroma/provider connections, inference/reservations/execution permissions, including
failure paths. Never fall back to production after a security failure.

Cover valid/missing/malformed API tokens; signature/algorithm/key/JWKS failures; wrong issuer/tid/
aud/version/times/subject/scope/role/additional roles; application/ID/Graph substitution; malformed
claims and unexpected azp. Reuse existing verifier tests plus bootstrap integration. Prove exact
production/stable/domain-separated canonical identities independent of oid/ID-token sub/runtime.
Test explicit/fresh export/schema/minimization, modes/ownership/links/symlinks/ancestors/repository/
shared-storage rejection, overwrite/partial/interruption/repeat/concurrency/expiry/unauthorized
failure. Test native configuration/missing/placeholders/login/token selection/verification/export/
reruns/stale tokens/logout/cleanup/conflicts and no sensitive display/logging.

Test real synthetic TLS/hostname/Host/WS Origin/callback, unsafe transport configuration,
missing/invalid/mismatched/unsafe certificate/key, occupied ports/loopback/shutdown/upstream
failure; reuse existing gateway security tests. Implement synthetic identity → existing verifier
→ canonical scope → explicit export → logout/shutdown E2E with production-state guards.
Distinguish units, components, synthetic E2E and real native Entra browser acceptance (unauthorized).

Run full offline pytest, existing Entra/authority/API/runtime/owner/init/gateway/native auth/Chat/
Documents/Phase19/governance/admission regressions, whitespace, available lint/types, external-cache
compilation and relevant inert Compose parsing. Exclude operational env/dotenv. Report exact
commands/counts/pass/fail/error/skip/durations/warnings/limits, intermediate failures/corrections
and final reruns. No unrelated test changes or unapproved dependency installs.

## Provenance, documents and handoff

Assess local image need, shared production-code impact and existing Azure image acceptability
separately. Historically staged `polymind:phase19-reviewed`, image ID
`sha256:9f386acf8bddcb5d01bb028151caae24b5df604f8a56c00b7b39c7e0f8298c02`, source
`7bf82dc2da4a9f29561a5f493b690502c0090eb0`. Never rebuild/transfer/overwrite it or pinned vendor
artifacts here. Do not infer image equivalence if shared code changed.

Create this prompt, matching explanatory report and a dedicated operator guide if justified.
Update README, Entra/VM operations and Phase19 architecture/plan with dated current addenda.
Preserve historical prompt/report bytes, minimize private inventory and never track actual
candidate/identity/credentials. Report all twenty requested topics: executive/baseline/dependency,
alternatives/architecture/implementation/native OIDC/verifier/canonical/export/custody/isolation/
threats/new/full tests/provenance/runbook/blockers/reviews/final gates/status.

Future runbook: prerequisites/revision/evidence/ports/Windows trust/SAN/lifecycle/custody/evidence;
operator-only encrypted restoration and ephemeral cookie/TLS provisioning; exact bounded launch;
separately authorized browser authentication; explicit sanitized protected export; logout/site
cleanup/shutdown/listener checks/plaintext cleanup/preserved encrypted custody; subsequent trusted
enrollment/source-owner review only. Never ask the operator to paste subject/tokens/evidence.

Separate engineering and pre-commit reviews must cover authentication/derivation/substitution/
claims/production security/azp/leaks/cookies/filesystem races/partial writes/imports/network/
listeners/shutdown/complexity/scope/historical preservation. Fix material findings, inspect all
new files, rerun final status/diff/stat/whitespace/index and provide complete inventory and exact
results. Suggested checkpoint only: `feat: implement Phase 19B local identity bootstrap utility`.

Acceptance gates 1–10 cover baseline/dependency, architecture, native authentication/verifier,
canonical equivalence, protected evidence, runtime isolation, sessions/transport, full offline
regression (or documented blocker), executable future runbook, scope/provenance. Populate every
supplied final-status field with actual evidence and limitations. Passing is offline engineering
readiness only: Gate A operational closure BLOCKED, actual token NOT_ACQUIRED, enrollment
NOT_PERFORMED; 19A COMPLETE, 19B ACTIVE, 19C NOT_STARTED.

## Strict exclusions and stopping condition

No Azure CLI/API/VM/SSH/forwarding, Graph/actual Entra discovery/JWKS/token/browser exchange,
registration/permission mutations, actual operational credentials/.env/decryption/TLS or CA/SSH
private keys/PKI archive access, Windows hosts/trust changes, production Compose/runtime/state,
production Redis/Chroma, provider credential discovery/requests/inference/reservations/signing,
public exposure, new infrastructure/dependencies, Git staging/commit/push/history changes.
Read-only GitHub evidence and scoped offline synthetic local tests are allowed. If infeasible,
report evidence/blocker without bypass. Stop after offline implementation/verification/docs and
operator review handoff; do not acquire identity, initialize production, close Gate A or start 19C.
