# Phase 17G readiness decisions

Baseline: clean master at `76ec11c79ff8d80467a3e14935d7ce06da4ce3bb`.

1. Existing authentication is a shared bearer secret. Query and memory paths are
   protected; document analysis is missing. Correct classification first, including
   body limits. Operational probes remain network-controlled.
2. Query and stream pass the raw client session to graph/memory. Introduce an
   explicit principal-bound memory facade; never migrate unscoped history.
3. Legacy RAG has no document ownership authority. Refuse legacy graph execution
   in OIDC mode before routing/retrieval/inference. Local/static behavior remains.
4. Phase 17F manifests bind exactly one owning Scope and immutable generation.
   Preserve publication/1 and exact row metadata. Generation identity includes
   scope; trusted owner registry plus generation/document filters is the v1
   authorization contract. Do not rewrite accepted rows.
5. Sharing resolves the original owner publication via a server registry. Reject
   mixed-owner selections; never construct store paths from request data.
6. Authorize document IDs before pinning/search. Dense search uses the existing
   generation/document filter. Prebuild per-document BM25 indexes at load so
   unauthorized documents do not contribute scores/statistics. Preserve legacy
   publication scoring when no security snapshot is supplied.
7. Governance precedes Phase 17E admission and bounded execute. Legacy generate
   and token streaming cannot safely carry attributable final usage/output limits:
   refuse governed execution. Background integration must preserve job attempts.
8. Bounded execute returns optional usage. Text generation returns only text;
   streaming returns chunks. Unknown usage must retain reservations across restart.
9. ObjectStore has no deletion or complete reference inventory; vector port has
   no per-row delete. File/Redis memory supports scoped clear. Local purge must
   record blocked inventory/adapter dependencies and remain PURGE_PENDING; no
   inferred object deletion or PURGED claim is safe.
10. Add narrow verified identity, SQLite authority, authorization snapshots,
    governance ledger and explicit composition. Keep job schema, scheduler,
    publication authority and inference provider ports. Final response release
    serializes against authority mutations locally; already delivered bytes
    cannot be recalled. SQLite remains single-host reference infrastructure.

OIDC requires PyJWT with cryptography, the sole new dependency family. Restrict
v1 to RS256 and configured HTTPS issuer/JWKS anchors with bounded cached fetching.
Roles come only from a configured issuer-controlled claim and operator allowlist.
No password/login/token issuance system is introduced.
