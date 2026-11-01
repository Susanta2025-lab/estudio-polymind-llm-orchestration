# Phase 17H-L — Operator approval compatibility report

Implemented and tested offline on 2026-10-13. The custom Entra issuer-claim blocker
is removed: the launcher now authenticates its operator normally and independently
verifies a signed operator approval artifact. No live Azure request, cloud change,
automatic approval, commit or push occurred. No live signing key or approval was
created; all signing performed by tests used ephemeral synthetic keys.

## Inspection and implementation

The starting worktree contained eight modified tracked files and eighteen
untracked files. Inspection covered AGENTS.md, the launcher, signed JWT approval
check, Entra verifier and Settings integration, governance/run ledgers, security
and launcher tests, approval template, runbook, and prior readiness/Entra reports.
Existing provider changes, identity verification and governance implementation
were preserved. Pre-edit copies of the launcher, launcher tests and approval
runbook/template were retained outside the repository for diff review.

`tests/performance/foundry_approval.py` provides a narrow evaluation-launcher
approval boundary using existing PyJWT/cryptography dependencies. Its independent
`ApprovalTrust` file pins one operator RSA public key, key ID, exact authenticated
issuer/subject/tenant and persistent replay directory. Trust cannot come from the
artifact or launch configuration. Public PEMs must be RSA 2048–8192 bits; artifacts
use RS256 with the dedicated `polymind-approval+jwt` header type and fixed issuer/
audience values, separating approval from identity tokens. No discovery, key URL,
embedded key, signing operation or test override exists in the live path.

The signed binding covers the verified identity and owner scope, unchanged full
configuration digest, exact Foundry resource/endpoint/deployment/model/version/
SKU/region, EUR spending ceiling and fixed/additional cost bounds, token limits,
attempt/rate/TPM/context limits and expiration. Full configuration hashing also
binds prices, policies, authority locations and local model artifacts. JSON types
and values must match exactly. All lifetime fields are strict integer timestamps;
validity is at most 24 hours, expiration must match the launch configuration, and
existing runtime expiry/cancellation gates remain active. Both artifact and trust
must have explicit live purpose. Test-purpose keys/artifacts are rejected.

`foundry_l1` continues to verify Entra/OIDC signature, trust, issuer, audience,
tenant, lifetime, scope and role through the existing verifier, then checks owner
scope and publication permission before approval verification. It does not inspect
`polymind_l1_approval` at all. A valid legacy claim without the separate artifact
fails closed. Existing registered-principal authorization, governance/catalog
matching, provider admission and run accounting remain unchanged.

Before local retrieval or provider construction, the launcher exclusively creates
a per-approval-ID consumption record in the independently configured replay
directory, fsyncing the file and directory. The directory must be outside the run
audit tree. The record contains hashes/IDs only, never raw tokens or signatures.
The original run marker is retained and now fsynced with its parent directory too.
Concurrent use permits only one consumer. Replay after restart, reuse of a
consumed ID with a new signature, and reuse with a newly signed audit-directory
configuration fail. Partial consumption and setup failures remain consumed; there
is no automatic rollback, refund, retry or reconciliation. Existing financial
ledgers are never cleared or replaced.

## Compatibility and review

The default offline CLI behavior is unchanged. Generic OIDC and strict Entra
profiles, provider APIs, governance schemas and `LaunchConfiguration` serialization
remain unchanged. Moving `private_path` into the approval module retains its
imported name in the launcher for existing consumers. New bounded private reads
also recheck open file metadata and refuse symlinks/nonregular/insecure files.

Live invocation deliberately requires two new arguments: `--approval` and
`--approval-trust`, in addition to the existing configuration hash acknowledgement.
Old JWT-only live approval is not supported as a fallback. Existing run markers
still block launches even with a newly valid artifact. This intentional live CLI
change is documented in the runbook and approval procedure.

Self-review checked signature/domain separation, independently provisioned trust,
identity binding, serialization, expiration at verification and consumption,
exclusive replay writes, directory durability, failure behavior, resource cleanup
and existing authority/ledger checks. Review additionally enforced that central
replay state cannot reside in the replaceable run audit directory. No dependency,
cloud resource, inference adapter, authentication rule or ledger migration changed.

Separate pre-commit review checked all task files for credential/private-key
markers, temporary/generated files, debug statements, unrelated modifications,
whitespace and local documentation links. Test signing code is isolated in
`tests/approval_helpers.py`; the live path never imports it. No real `.env` was
read or changed. The existing Entra/provider work remains intact.

## Offline validation

- Initial approval/launcher union: **87 passed in 16.78 s**.
- Final targeted regression: **388 passed in 44.39 s**. It covers approval claims,
  signatures, header/key substitution, missing/test/expired/mismatched approvals,
  each explicit identity/target/financial/token binding, trust policy, private
  file loading, concurrent/restarted replay, fsync/setup failures, legacy markers,
  CLI argument/loading behavior, Entra negative authentication with an otherwise
  valid approval, and normal OIDC/Entra L1 integration.
- The successful L1 cases use ordinary access tokens without custom approval
  claims, complete four intercepted calls, publish canonical evidence and cited
  Q&A, and settle governance records. Missing/invalid approvals cause no provider
  calls; one test confirms existing authority/ledger bytes remain unchanged.
- Existing unknown-usage/timeout tests still retain financial obligations and
  refuse restart. Default CLI rehearsal still forbids network connections.
- Full-repository compilation passed with bytecode directed to an external cache:
  `PYTHONPYCACHEPREFIX=/tmp/polymind-17hl-approval-pycache python -m compileall -q .`.
- `git diff --check` passed; the approval template parses as JSON. No configured
  lint/format tool exists. Docker/cloud checks were not applicable. The complete
  repository test suite was not rerun.

Final regression command:

```bash
python -m pytest -q tests/unit/test_foundry_approval.py tests/integration/test_foundry_l1_launcher.py tests/integration/test_foundry_l1_entra.py tests/unit/test_security_entra.py tests/unit/test_security_identity.py tests/unit/test_security_configuration.py tests/unit/test_governance.py tests/unit/test_foundry_preflight.py tests/unit/test_foundry_30k.py tests/unit/test_structured_provider.py tests/integration/test_governed_digestion.py
```

## Operator handoff and blockers

The [approval procedure](../../evaluation/phase_17hl_operator_approval.md) specifies
independent trust provisioning, artifact fields/signature format, unsigned review
material, explicit operator signing, CLI handoff and durable replay obligations.
The [runbook](../../evaluation/phase_17h_foundry_validation.md),
[template](../../evaluation/phase_17h_foundry_approval.template.json),
[Entra guide](../../security/entra_v2.md) and `.env.example` now reference the new
mechanism. Templates remain proposal-only, with test purpose/unset fields and no
signature; none can authorize a live launch. Prior reports retain historical
results with a supersession link.

Remaining blockers are independent trusted operator-key provisioning, private
persistent replay storage and an actual reviewed/unexpired live signature. Real
Entra consent/role/token and authority registration, deployment credentials,
verified EUR pricing/quota/shared-consumer limits and local embedding/runtime
readiness remain unverified. No external identity or Foundry endpoint was contacted.
The old need for custom Entra issuer-claim support no longer applies. All financial
and L2 acceptance restrictions remain unchanged; this task grants no live spend.

The reference remains single-host. It cannot protect against an administrator
replacing trusted keys, relabeling test keys as production trust, deleting or
restoring replay/ledger files, or using independent hosts/registries. Protect and
retain the independent trust and replay state; do not reset it to retry. A new
approval ID is a new authorization, not a mechanism to bypass reconciliation.

Final worktree: eight modified tracked files and twenty-four untracked files,
including all prior work. `git diff --stat` shows eight tracked files with 130
insertions and six deletions; Git excludes the untracked launcher and new approval
files from that statistic. All changes are unstaged/uncommitted on
`master...origin/master`. No commit or push occurred.
