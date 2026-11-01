# Phase 17H-L — Attempt 3 serialization investigation (task summary)

Reproduce the preserved Attempt 3 successful provider response offline through
decoding, managed validation, model conversion, canonical serialization,
evidence/lineage and persistence boundaries. Identify the exact exception and
contract mismatch before making any correction; do not assume the eight unused
null fields are the sole cause.

Use only synthetic/redacted repository tests. Preserve fail-closed validation,
10,000-byte provider/canonical limits, 3,000 completion tokens, evidence,
qualifications, contradictions, lineage, governance and pricing. No retries,
fallback or silent content repair. If correction requires broader contract
changes, stop and report the exact blocker.

Run affected offline tests only, including rejection, serialization limits,
single-call behavior and settlement after downstream failure. Do not repeat
the full JSON-limit or governance suites. Write the requested root-cause report
and separately explain the launcher's zero exit code for FAILED jobs.

No Azure inference, live authority initialization, signing, approval, Attempt 4
preparation/execution, audit/history/governance mutation, cloud infrastructure,
policy changes, staging, commits or pushes. Preserve the existing master tree.
Return PASS only if reproduced and corrected offline; otherwise report BLOCKED
with the exact unresolved cause.
