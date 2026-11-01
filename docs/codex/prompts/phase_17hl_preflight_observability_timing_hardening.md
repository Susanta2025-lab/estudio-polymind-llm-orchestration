# Phase 17H-L — preflight observability and operational timing hardening

Task scope preserved from the supplied phase prompt (condensed, not a verbatim transcript).

Implement a small improvement to the existing single-call Azure compatibility harness:
closed, sanitized execution stages and failure categories; safe private diagnostic evidence;
explicit required live CLI arguments; offline display of the strict effective launch cutoff
`min(approval_expires, credential_valid_until) - 600`; and an ordered operator handoff.
Inspect the prior failure-diagnosis and offline-harness reports first. Do not claim the
historical cause is known. Inspect OIDC transport behavior and test failures offline;
do not change timeout, proxy, caching or retry policy without evidence.

Preserve independent RSA signing, pinned public trust, replay consumption, OIDC verification,
registered authorization, financial governance, provider admission, one-call/no-retry limits,
strict provider schema and domain validation. Inspect the historical signing workflow without
reading keys or executing it; document the existing operator-local key path if safer than edits.
Do not automatically extend authorization to 60 minutes or reduce the 600-second margin.

Use synthetic fixtures, fake transports and isolated temporary authorities. Test missing CLI
arguments, invalid configuration, time boundaries, absent credentials, digest mismatch,
authentication/authorization/fixture failures, unexpected-error sanitization, private evidence,
unsafe audit paths and unchanged preflight security barriers. Recalculate official fingerprints
and report old/new bindings. Historical approvals must remain unchanged and unsuitable for
the modified execution contract.

No Azure/Entra requests, live inference, real signing/key access, existing approval consumption,
historical packet edits, replay reset, existing authority mutation, cloud operations, schema or
budget changes, commits or pushes. Stop after offline validation and reporting.

Required report: `docs/codex/reports/phase_17hl_preflight_observability_timing_hardening.md`,
covering assessment, implementation, taxonomy, timing, security, actual test results,
fingerprints, future handoff and remaining limitations, with PASS/PARTIAL/BLOCKED conclusion.
