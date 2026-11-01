# Phase 17H-L — Structured-output compatibility scope

Condensed record of the user-supplied phase prompt, 16 October 2026; not a launch authorization.

Assess Azure Foundry `epolymind-gpt-54-mini` (`gpt-5.4-mini`, `2026-03-17`, GlobalStandard, Spain Central, `/openai/v1`) for strict JSON Schema generation using the actual StageResult contract. Inspect the three-attempt postmortem and serialization/byte-limit/output-limit reports without repeating their investigations.

Implement the smallest provider-compatible strict mode only if an exact contract-preserving schema is feasible. Preserve application validation, all fields, UUIDs, evidence, timeout/HTTP bounds, accounting, security and unrelated output modes. Never strip constraints to substitute a permissive schema. Unsupported strict requests must fail before inference, without fallback. If exact conversion is impossible, report the incompatibility.

Use focused network-disabled synthetic tests for provider requests, malformed UUIDs, forbidden fields, nested/missing fields, valid responses, nonexistent evidence, serialization boundaries and settlement. No full suite or repeated governance investigation. Bind any request/schema changes into generation fingerprints and require future configuration review; preserve history.

Retain 10,000/10,000 provider/canonical bytes, 3,000 completion tokens, 25,000 input reservation, four calls, 100,000/12,000 totals, 28,000 context, 26,192 HTTP bytes, 61-second spacing, EUR 5 and `polymind-evaluation/1`.

Work on master, preserve all existing changes. No live inference, Azure changes, signing, approval consumption, Attempt 4 preparation/execution, staging, commits or pushes. Record launcher FAILED/exit-zero issue separately. Produce the compatibility report with evidence, implementation boundary, tests, risks and safety counters. Finish the focused assessment and feasible offline work, then stop with the specified PASS (live pending) or BLOCKED outcome.
