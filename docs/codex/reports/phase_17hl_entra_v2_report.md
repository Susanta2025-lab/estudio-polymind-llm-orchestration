# Phase 17H-L — Entra v2 compatibility report

Historical report: the custom issuer-claim blocker below is superseded by the
[separate operator approval implementation](phase_17hl_operator_approval_report.md).

Implemented and verified offline on 2026-10-13. Live authentication and L1 launch
remain unverified. No Azure inference, paid requests, Azure resource changes,
commits or pushes occurred.

## Implementation and architecture

Inspection covered `security/identity.py`, `config/settings.py`, the identity,
configuration, authority, API, readiness and publication security tests, the
security runtime, and the existing uncommitted L1 launcher/provider work. The
baseline contained five modified tracked files and thirteen untracked files;
those changes were preserved. No provider or governance implementation was edited.

`OIDCSettings` now accepts an explicit `token_profile=entra_v2` and `tenant_id`.
The existing Settings validation already delegates to that model, so invalid
Entra configuration fails startup without changing the application configuration
boundary or adding an authentication mode. The generic OIDC profile remains the
default, with its existing purpose, role mapping and service identity behavior.

The Entra profile pins a single public-cloud tenant, tenant-specific v2 issuer
and JWKS URL, and scalar API client UUID audience. It verifies RS256 signatures,
JWKS key trust/issuer metadata, `tid`, `ver`, integer lifetime claims, `sub`, exact
delegated `access_as_user` scope and assigned `PolyMind.L1Operator` role. It rejects
ID tokens lacking delegated API scope, wrong resource tokens, application-only
identities, unknown/additional roles, missing claims, forged signatures and
token-controlled key sources. No permissive purpose fallback was added to OIDC.

The fixed role mapping grants only `PUBLICATION_MANAGE`, which the existing L1
publication workflow requires. Existing document ownership/sharing rules and
own-session operations remain authoritative; this does not introduce a read-only
L1 sandbox or tenant administration. Principal identity remains issuer/tenant/sub.
Registration, revocation, authorization, signed approval, financial accounting,
provider admission and inference boundaries are unchanged.

JWKS fetch limits, cache expiry and refresh cooldown remain intact. Explicit key
issuer metadata must be either the configured issuer or Microsoft's tenant
template. This intentionally fails closed on incompatible JWKS metadata; actual
deployed keys and egress have not been tested. There is no live token acquisition
or automatic issuer discovery.

## Tests and validation

The new tests generate ephemeral RSA keys and sign synthetic JWTs in memory.
Network connections are forbidden in the new identity tests and L1 integration
tests. Coverage includes claims/type/lifetime failures, ID-token substitution,
Graph/inference/URI/wrong-client audiences, role escalation, scope substrings,
algorithm/key confusion, JWKS metadata, rotation, cache expiry, configuration
errors, private dotenv JSON loading, profile isolation and authority scope.

The new integration test uses the existing intercepted L1 composition: a valid
Entra identity with synthetic signed approval completes four calls, publication
and cited Q&A, with settled governance records. Missing or wrong signed approval
stops before provider calls or the durable launch marker. All calls in this test
use intercepted local transport; they are not Azure calls.

Validation evidence:

- Initial identity/configuration run: **136 passed in 6.04 s**.
- Targeted regression union: **277 passed in 34.51 s**. It included identity,
  settings, authority, API, readiness, publication security, governance, governed
  digestion, both L1 integration suites and structured-provider regressions.
- Self-review identified that adding default model fields could change existing
  generic-OIDC signed configuration hashes. A serializer now preserves the exact
  original JSON shape/order for that profile, with a regression assertion.
- Final affected-suite rerun after that correction: **165 passed in 14.46 s**.
  This includes both old/new identity tests, configuration tests, and both L1
  integration suites. The broader 277-test result predates only this serializer
  correction and its test; the complete repository suite was not run.
- `PYTHONPYCACHEPREFIX=/tmp/polymind-17hl-entra-pycache python -m compileall -q .`
  passed after the final code change. The external cache avoids ownership issues.
- `git diff --check` passed. No configured lint/format tool was found. Docker and
  Kubernetes validation were not applicable to this identity-only change.

Reproduce the final affected-suite check:

```bash
python -m pytest -q tests/unit/test_security_entra.py tests/unit/test_security_identity.py tests/unit/test_security_configuration.py tests/integration/test_foundry_l1_entra.py tests/integration/test_foundry_l1_launcher.py
```

Reproduce the broader union:

```bash
python -m pytest -q tests/unit/test_security_entra.py tests/unit/test_security_identity.py tests/unit/test_security_configuration.py tests/unit/test_security_authority.py tests/unit/test_security_api.py tests/unit/test_security_readiness.py tests/unit/test_governance.py tests/unit/publication/test_security.py tests/integration/test_foundry_l1_entra.py tests/integration/test_foundry_l1_launcher.py tests/integration/test_governed_digestion.py tests/unit/test_structured_provider.py
```

## Review, configuration and remaining blockers

Implementation self-review checked trust anchors, key selection, role boundaries,
normalization of failures, cache behavior, backward compatibility and consumers
of serialized settings. No API response, provider contract, governance policy,
dependency, deployment or database migration changed. Separate pre-commit review
covered the task's complete diff and new files for credentials, generated files,
debug statements, unrelated changes, whitespace and broken local documentation
links. Keys remain in-memory test material; no real `.env` was read or modified.

Exact private `.env` instructions are in [the Entra guide](../../security/entra_v2.md)
and a commented alternative in `.env.example`. The [Phase 17G contract](../../security/phase_17g.md)
links the profile. Documentation identifies synthetic UUID substitution, removal
of even empty `API_AUTH_TOKEN`, required existing governance settings, delegated
permission/role prerequisites and the private launcher's separate `oidc` object.

Remaining authentication blockers/checks are explicit:

1. Real tenant/API IDs, delegated consent, user role assignment and a valid v2 API
   access token have not been supplied or verified in this task. Trusted JWKS
   egress and deployment token lifetime still require validation.
2. The verified principal must match the launcher's `owner_scope` and already be
   enabled in the existing security authority. A profile change requires a new
   configuration digest and reviewed approval.
3. The launcher still requires the issuer-signed `polymind_l1_approval` claim
   matching that digest. Ordinary Entra scope/role authentication is insufficient;
   actual issuer support for this custom attestation is unverified. No approval
   bypass, synthetic live identity or replacement approval mechanism was added.

The implementation is ready for user review, not authorized live execution. All
existing commercial, financial, resource and L2 blockers remain outside this task.

## Git handoff

This task modifies `security/identity.py`, `.env.example` and
`docs/security/phase_17g.md`, and adds the Entra guide, two test files, this report
and the preserved prompt. Existing uncommitted provider/launcher work is intact.
All changes are unstaged and uncommitted on `master...origin/master`.

Final `git status` inventory: eight modified tracked files and eighteen untracked
files, including the earlier work. `git diff --stat` covers tracked files only:
eight files, 130 insertions and six deletions. No commit or push occurred.
