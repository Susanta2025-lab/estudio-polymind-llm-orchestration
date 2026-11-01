# Phase 17H-L — controlled policy migration and same-day L1 preparation

Operator task, 15 October 2026: prepare the second real four-request L1 attempt
for today, preserving the failed October attempt and the unsigned November packet.
Reuse completed readiness evidence and prior 67/93/195-test results.

Authorize only owner and tenant policy changes: rolling-24h requests 4 → 5,
daily tokens 112,000 → 115,305, monthly tokens 112,000 → 115,305. Keep EUR 5,
pricing, reservations, provider headroom, identities and authority paths unchanged.
Use a supported migration if available; otherwise implement a minimal audited,
versioned, atomic, idempotent, fail-closed migration. Back up before mutation;
retain all historical requests, settlements, costs, reservations and replay records.
Check authoritative accounting; do not raise maxima further if insufficient.

Retain managed-prompt/2, 3,000 canonical JSON bytes, 3,000 output tokens per call,
full evidence/lineage validation, corrected OIDC retrieval authorization, pinned
local MiniLM and isolated local Chroma. Three digestion calls plus one grounded
Q&A, maximum four requests, no automatic retry or fallback.

Prepare a separate private run-20261015-attempt2 directory, 0700 directories and
0600 files, with configuration, empty audit directory, eligibility helper, private
operator packet, policy/cost evidence and fresh unsigned review/digest. Reuse
existing RSA trust and attestations. Bind current identities, resource/deployment,
policy, generation fingerprint, EUR 5 incremental ceiling, four-call limits and
real same-day short-lived window. Never reuse the November digest as authorization.

Run focused migration/history/rollback/concurrency/admission/configuration/signature
binding tests, diff check and relevant compilation; no broad regression or repeated
readiness investigation. Review implementation and pre-commit safety.

Deliver docs/codex/reports/phase_17hl_same_day_attempt2_handoff.md with policy result,
admission decision, technical evidence, exact operator steps A authentication,
B review, C personal RSA signing, D independent verification and E live launcher.
Codex must not obtain delegated tokens, unlock/sign with the real key, consume
approval or launch inference. No Azure infrastructure changes, AKS restart, L2,
ledger reset, identity substitution, Git staging, commit or push. Return GO —
SAME-DAY L1 READY FOR OPERATOR SIGNATURE, or NO-GO — EXACT TECHNICAL BLOCKER.
