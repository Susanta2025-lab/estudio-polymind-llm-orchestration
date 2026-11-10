# Phase 17H v10 task scope

The supplied task requests implementation of the completed post-v9 architecture
review's single generation-wire model, deterministic constructor and audited
request/table/response/checkpoint association. This is a clean scope record; the
original detailed request is retained in the task conversation.

The starting expectation is master at
`6e0319e29984ad019edced0e076b3b0a4ae8c007`, managed-prompt/9, generation digest
`f270aa81cbd5764d2b4739bf3ac3692653b1fe4c8ffbd67860e642137cb2579d`.
Verify actual state, preserve inherited uncommitted v8/v9 work, read AGENTS.md,
post-v9 review/ADR, v9 engineering report, v7/v8 execution reports, current Foundry
runbook and historical fixtures before editing. Do not repeat the completed
open-source investigation.

Resolve durable association first, reusing immutable object storage, provider
records, job attempts, lease fencing and checkpoint commitment. An additive
immutable receipt is authorized; destructive migration, checkpoint rewrite, new
approval credentials or fundamental storage redesign require stopping with the
exact blocker. Define commit order and conservative crash/replay recovery.

Implement application-owned sorted E source mappings using exact v9 authority,
atomic C immediate-child pairs in plan-child/accepted-claim order, current stage
and origin IDs, and positional claim IDs using the unchanged stable_id algorithm.
The model retains responsibility for substantive ordered claims, evidence and
child-support selections, qualifications, conflicts, questions and limitations.
Never repair invalid references, attach all evidence/children, reorder/drop claims
or invent substantive content.

Use one explicitly versioned, bounded, strict wire schema and decoder across
strict and prompt modes. Validate raw size, duplicate JSON keys, exact object
fields/scalar types, list limits, reference membership/duplicates, request/table
binding and canonical limits. Construct stage-result/1 and run unchanged G2 and
complete G1 admission. Preserve canonical storage, publication, retrieval,
grounded Q&A, source offsets and historical v5–v9 readability.

Freeze complete v9 source and inventory before active changes. Introduce
managed-prompt/10 and bind every mapping/decoder/receipt dependency into the new
generation inventory. Preserve historical fingerprints and fail closed on stale
settings, plans, launch configurations and approvals.

Preserve 24,800 managed input, 28,000 context, 7,000 complete-child bytes, 3,000
output tokens, established raw/canonical/HTTP limits, exactly the L1 topology
chunk -> first reducer -> root -> Q&A, at most four paid calls, minimum 61-second
starts, one concurrent call, no automatic paid retries and no fallback.

Add permanent mapping, pair, identity, strict decoder, corrupt binding, crash,
replay, fencing, reuse, settlement and negative dependent-call regressions.
Execute the real synthetic extraction/planning/generation/validation/checkpoint/
publication/retrieval/Q&A interfaces, retaining an eight-claim quality witness,
qualifications, unresolved contradictions and original citations. Measure actual
v9/v10 serialization, all four profiles, source cardinalities 0/1/4/128/129/256,
one/two-child reductions and exact escaped/Unicode path limits.

Run the complete offline suite with the existing pre-collection network-denial
guard and disposable authorities/stores; relevant focused, historical, schema,
workflow and crash tests; Ruff and applicable format checks; scoped mypy;
compilation with external cache; Compose configuration; git diff --check.
Report exact unique test counts and network attempts, not summed overlapping runs.
Perform separate critical implementation and pre-commit reviews, correct genuine
findings, preserve permanent report/ADR and update only current documentation.

No Azure inference, Microsoft Entra authentication, credential retrieval, real
private-key access, RSA signing, approval consumption, cloud/resource changes,
Kubernetes launch, financial/policy/replay mutations or historical-evidence deletion
is authorized. Synthetic local security/approval fixtures are permitted. Do not
download/install local models or new dependencies automatically. Never stage,
commit, push, change branches/tags/history or mutate GitHub state.

Return PASS only after all deterministic engineering, historical compatibility,
full synthetic workflow, crash/recovery, full offline and applicable static checks
pass. Distinguish engineering correctness from unobserved Azure/schema/model and
semantic compliance. A new operator-preparation phase remains manual and separate;
this task must not prepare or launch a paid evaluation.
