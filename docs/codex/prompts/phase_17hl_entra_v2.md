# Phase 17H-L — Entra v2 access-token compatibility

Implement Microsoft Entra ID v2 access-token compatibility for Phase 17H-L.

Follow AGENTS.md and inspect the existing security/identity.py, config/settings.py,
security tests and current uncommitted work.

Requirements:
- Support the existing OIDC verifier and Microsoft Entra v2 access tokens without
  weakening existing security.
- Validate signature, trusted JWKS, issuer, audience, tenant, lifetime and required
  delegated scope `access_as_user`.
- Map the assigned `PolyMind.L1Operator` role to narrowly scoped L1 permissions.
- Reject ID tokens, wrong audiences, unauthorized roles, missing scopes and
  untrusted signing keys.
- Add comprehensive offline tests using synthetic signed JWTs.
- Document the exact configuration needed in .env, without storing secrets.
- Preserve existing providers and governance behavior.

No Azure inference, paid calls, Azure resource changes, commits or pushes.

Run targeted regression tests and report any remaining authentication blockers.
Leave changes uncommitted.
