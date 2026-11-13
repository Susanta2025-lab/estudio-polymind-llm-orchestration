# CODEX MASTER PROMPT — PHASE 17I STAGE 3
## Documentation, Engineering Closure and Deferred External Verification

**Project:** Estudio PolyMind
**Phase:** 17I — External User Verification
**Stage:** 3 of 3 — Documentation and Closure
**Task type:** Documentation, evidence reconciliation and project-state finalization

---

## 1. Mission

Complete **Phase 17I Stage 3 — Documentation and Closure**, following the successful implementation and verification of the bounded, operator-supervised local pilot workflow.

The operator requires exactly three formal stages for every project phase:

1. **Assessment** — COMPLETE.
2. **Implementation and Verification** — COMPLETE.
3. **Documentation and Closure** — THIS TASK.

Do not create additional formal development stages.

This task must:

- Finalize and reconcile the Phase 17I documentation.
- Verify that current documentation accurately describes implemented functionality.
- Establish the authoritative Phase 17I engineering-completion decision.
- Update README, roadmap and relevant operator/security/evaluation documentation.
- Preserve historical implementation and validation evidence.
- Track outstanding external-user verification as a deferred acceptance requirement.
- Produce a clear handoff for future development.
- Leave the repository ready for an operator-reviewed documentation commit.

**Do not repeat implementation or successful automated validation.**

Do not conduct an external-user pilot.

### Important closure distinction

Phase 17I engineering and its three-stage development workflow may be marked complete.

However, actual external-user verification has not occurred.

Therefore, do not declare the original external-user acceptance requirement satisfied.

The intended disposition is:

`PHASE_17I_ENGINEERING_COMPLETE`

`PHASE_17I_DOCUMENTATION_COMPLETE`

`PHASE_17I_EXTERNAL_VERIFICATION_DEFERRED`

`PHASE_17I_FORMAL_ACCEPTANCE_PENDING`

`SUBSEQUENT_ENGINEERING_PERMITTED`

These are separate classifications, not interchangeable PASS labels.

Formal closure of the external-verification obligation will occur only when actual accepted evidence exists or the operator explicitly approves a revised acceptance policy.

---

## 2. Verify the committed baseline

Repository:

`Susanta2025-lab/estudio-polymind-llm-orchestration`

Latest reported source commit:

`ed7dbd5ed63548bccfac9ef27a8a0f7b771ca26a`

Commit message:

`feat(pilot): implement bounded supervised Phase 17I verification workflow`

GitHub Actions:

- Workflow: Estudio PolyMind CI
- Run ID: `43391359991`
- Status: Completed
- Conclusion: SUCCESS
- Reported elapsed time: 6m21s

Earlier baselines:

- `69c8f66` — Phase 17I readiness assessment.
- `b90f4ad` — Phase 17 engineering completion and deferred semantic review.
- `9acfeb6` — Phase 17H evidence preservation.
- `f8ba9c1` — Phase 17H v11 engineering.

Verify actual Git HEAD and working-tree state rather than assuming they remain unchanged.

Run:

```bash
git status --short --branch
git log --oneline -5
git rev-parse HEAD
git diff --check
```

Read `AGENTS.md` and honor repository development policies.

The previous working tree contained 28 unrelated untracked historical Phase 17H documents.

Preserve those files exactly.

Do not stage or include them automatically.

No reset, clean, stash, rebase, history rewrite, commit or push.

---

## 3. Read the authoritative evidence

Inspect the following documents.

### Phase 17I assessment

- `docs/codex/reports/phase_17i_readiness_assessment.md`
- `docs/evaluation/phase_17i_implementation_and_verification_plan.md`
- `docs/evaluation/phase_17i_external_user_readiness_gates.md`

### Phase 17I implementation

- `docs/codex/reports/phase_17i_implementation_and_verification.md`
- `docs/codex/prompts/phase_17i_implementation_and_verification.md`
- `docs/evaluation/phase_17i_operator_workflow.md`
- `docs/evaluation/phase_17i_record_templates.json`

### Previous phase handoff

- `docs/evaluation/phase_17_engineering_completion_and_deferred_acceptance.md`
- `docs/evaluation/phase_17_deferred_human_semantic_review.md`
- `docs/codex/reports/phase_17h_v11_controlled_live_execution_and_reconciliation.md`
- `docs/security/phase_17g.md`
- `docs/security/entra_v2.md`
- `docs/security/production-security.md`
- `docs/governance/evaluation-policy.md`

### Code contracts

Inspect the current implementation under:

- `documents/pilot/`
- `llm/admission.py`
- Relevant security, governance and publication interfaces.
- Relevant Phase 17I tests.

Use source inspection to validate documentation accuracy.

Do not run or modify production services.

Do not modify completed historical reports merely because they were written before later results became available.

---

## 4. Preserve the Stage 2 engineering evidence

The committed Stage 2 report records:

| Verification | Recorded result |
|---|---|
| Engineering implementation | PASS |
| Offline verification | PASS |
| Full pytest suite | 3,052 passed |
| Unit tests | 2,163 passed |
| Integration tests | 889 passed |
| New Phase 17I tests | 56 |
| Reported failures/errors/skips | 0 |
| N1–N15 coverage | Implemented |
| Local synthetic end-to-end rehearsal | PASS |
| Synthetic provider calls | 4 |
| Synthetic reservations outstanding | 0 |
| Digest coverage | 1.0 |
| Actual external participants | 0 |
| New billable inference | 0 |
| Independent human semantic reviews | 0/2 |

These are historical recorded outcomes.

Do not rerun the full 3,052-test suite solely to produce Stage 3 documentation.

Do not describe the synthetic financial settlement as actual Azure spending.

Do not confuse the deterministic provider with actual-model semantic validation.

The Stage 2 result supports engineering closure within the bounded single-host scope, not general production acceptance.

---

## 5. Finalize the implemented capability documentation

The Phase 17I system implements:

**Option A — Private, Operator-Supervised Local Verification**

Document the implemented workflow accurately:

```text
Verified operator
       |
       v
Approved source and session
       |
       v
Bounded native extraction
       |
       v
Durable document job
       |
       v
Governed v11 synthesis
       |
       v
Validated COMPLETE digest
       |
       v
Authorized publication
       |
       v
Selected-document grounded Q&A
       |
       v
Canonical citation presentation
       |
       v
Structured feedback
       |
       v
Session closure / withdrawal
       |
       v
Revocation and residual inventory
```

### Required capability documentation

Explain:

1. `documents.pilot.SupervisedPilot` and its trusted operator-facade boundary.
2. Existing verified operator principal and publication authority.
3. Participant study codes and approval records.
4. Document hash, rights, classification and size validation.
5. Bounded native PDF/text extraction.
6. Parser resource limits and known sandbox limitations.
7. Explicit v11 synthesis profile.
8. Durable job admission and checkpoint verification.
9. Authorized publication and selected-document analysis.
10. Canonical citation identity and source evidence.
11. Guarded inert presentation.
12. Structured feedback and review records.
13. Session expiration and withdrawal.
14. Emergency stop, cancellation and restart reconciliation.
15. Shared inference admission and financial accounting.
16. Retention inventory and `PURGE_PENDING`.

Use exact source interfaces and configuration names.

Do not describe nonexistent public HTTP endpoints, participant login, Streamlit document portal or unrestricted upload UI.

### Operational restrictions

Document the actual limits:

- Up to three total approved sessions.
- One open document job.
- One exclusive admitted provider request within the supported shared authority.
- Up to four native PDF pages or approved UTF-8 text.
- Maximum 1,000,000 source bytes.
- Maximum 4,000 extracted characters.
- Maximum three synthesis attempts.
- Maximum three Q&A questions.
- Maximum six total provider attempts per document.
- No unapproved paid retries.
- Explicit v11 profile selection.
- Existing tighter model and resource limits still apply.

Record parser bounds and relevant timeouts from current source.

Do not imply that every document within these simple size limits is automatically eligible.

---

## 6. Finalize operator documentation

Review and update:

`docs/evaluation/phase_17i_operator_workflow.md`

Ensure it serves as a practical operator reference.

It must explain:

### A. Safe local setup

How an authorized operator composes the existing pilot services.

Identify prerequisite databases, object store, publication authority, admission authority and inference configuration.

Do not include actual credentials, private keys or machine-specific paths.

### B. Synthetic verification

Provide a reproducible offline demonstration command using the existing supported entry point:

```bash
python -m tests.performance.pilot_dry_run
```

Verify that this entry point still exists and is correctly described.

Clearly label deterministic provider behavior as synthetic.

### C. Real-participant preparation

Describe the future GO/NO-GO procedure, including consent, source approval, privacy review, independent quality evidence, financial authorization, access restrictions and operator responsibility.

Do not treat blank record templates as completed approvals.

### D. Stop and recovery

Describe exactly what the operator can stop and what remains potentially billable.

Explain known versus UNKNOWN usage, preserved checkpoints, immutable evidence and restart restrictions.

### E. Cleanup

Document access revocation, session reset, retained artifacts, metadata policy, provider/backup limitations and `PURGE_PENDING`.

Never promise physical deletion that the implementation cannot prove.

---

## 7. Reconcile all sixteen readiness gates

Use the existing register:

`docs/evaluation/phase_17i_external_user_readiness_gates.md`

Preserve the original assessment snapshot.

Add a clearly dated **Post-Implementation / Stage 3 Reconciliation** section or an equivalent non-destructive current-state view.

Use Stage 2 evidence for G01–G16.

The latest recorded dispositions are:

| Gate | Stage 2 outcome |
|---|---|
| G01 Authentication | PARTIAL |
| G02 Authorization | ENGINEERING VERIFIED |
| G03 Consent and rights | APPROVAL PENDING |
| G04 Privacy and provider transmission | APPROVAL PENDING |
| G05 Physical deletion | PARTIAL |
| G06 Expert semantic quality | PENDING |
| G07 Provenance and support | PARTIAL |
| G08 Prompt injection | PARTIAL |
| G09 Reliability | PARTIAL |
| G10 Financial authorization | PENDING |
| G11 Operational procedures | PARTIAL |
| G12 Deployment/exposure | PARTIAL |
| G13 Audit and custody | PARTIAL |
| G14 Cleanup | PARTIAL |
| G15 Usefulness | PARTICIPANT EVIDENCE PENDING |
| G16 External execution authorization | PENDING |

Confirm every classification against actual Stage 2 evidence.

Do not convert PARTIAL or approval-pending gates into PASS merely because a module exists or tests pass.

Explain which requirements have been implemented technically and which still require future decisions.

Do not add duplicate gate registers unnecessarily.

---

## 8. Record deferred external-user verification

Create or update a durable deferred-acceptance record.

Preferred filename, unless an equivalent already exists:

`docs/evaluation/phase_17i_deferred_external_verification.md`

Record:

**Obligation ID:** `PHASE17I-EXTERNAL-USER-ACCEPTANCE`

**Current status:** `DEFERRED`

**Engineering prerequisite:** Completed within Option A scope.

**Actual participants completed:** 0.

**Real-world usability feedback:** Pending.

**Independent source/answer quality evidence:** Pending.

**Consent/privacy authorization:** Pending.

**External participation approval:** Pending.

**New paid inference authorization:** Not granted.

**Formal acceptance:** Pending.

**Responsible party:** Project operator.

**Due date:** Not scheduled.

Do not invent users, approval dates, experts, test sessions, budget grants or survey results.

### Future acceptance procedure

Document the exact steps required when real external testing is chosen:

1. Select the approved pilot document and participant scope.
2. Validate source-processing rights and eligible document classification.
3. Complete relevant privacy/consent/retention decisions.
4. Obtain the applicable independent quality evidence.
5. Validate current authority, budgets, provider capacity and operational stop controls.
6. Obtain separate participation and paid-execution authorization where required.
7. Execute controlled sessions.
8. Collect real usefulness, correctness, citation and error feedback.
9. Reconcile usage and participant/session records.
10. Complete withdrawal, revocation and residual-retention accounting.
11. Apply the accepted Phase 17I criteria.
12. Issue the final external-user verification decision.

Do not execute these future activities in Stage 3.

This deferred acceptance process is an outstanding obligation, **not a fourth formal development stage**.

---

## 9. Preserve Phase 17H's separate deferred review

The previous Phase 17H obligation remains:

`DEFERRED_PENDING_TWO_INDEPENDENT_REVIEWERS`

Completed reviewers: **0/2**.

Formal Phase 17 acceptance remains pending under the existing decision.

Do not merge this requirement with Phase 17I's real-participant verification.

These are different evidence obligations.

Also, an independent project does not automatically have a legal requirement for two external experts.

The earlier two-reviewer requirement is a project-defined quality gate.

The operator may explicitly revise that gate in a future decision, provided the revised evaluation method and limitations are documented.

**This Stage 3 task does not authorize that change.**

Preserve the currently accepted rubric and review count.

---

## 10. Update README and the phase roadmap

The current README still contains Phase 17I statements written before implementation, including:

`PLANNED / NOT STARTED`

Update all current-state statements that are now obsolete.

The new README should clearly communicate:

### Completed

- Phase 17A–17H bounded reference engineering.
- Phase 17H controlled Azure v11 technical evaluation.
- Phase 17I Stage 1 assessment.
- Phase 17I Stage 2 bounded implementation and offline verification.
- Phase 17I Stage 3 documentation, once this task passes.

### Pending

- Phase 17H's two independent human reviews.
- Actual Phase 17I external-user sessions.
- Independent real-document/answer quality acceptance.
- Consent/privacy/retention and exposure approvals.
- New paid model authorization.
- Formal external-user acceptance.
- Production deployment readiness.

Include the Phase 17I regression outcome of 3,052 tests and identify it as recorded Stage 2 evidence.

Explain that Option A is a private, operator-supervised local workflow, not a public SaaS deployment.

Link to the implementation report, operator guide, readiness gate register and deferred-acceptance record.

Preserve the original architecture and existing README sections.

Avoid rewriting the historical Phase 17A–17H timeline.

---

## 11. Final engineering completion decision

Create:

`docs/evaluation/phase_17i_engineering_completion_and_deferred_acceptance.md`

This document must be the authoritative Phase 17I status decision.

Include:

- Project baseline.
- Three-stage development model.
- Completed engineering scope.
- Implementation and validation evidence.
- Synthetic end-to-end outcome.
- Security, provenance and accounting boundaries.
- External participation limitations.
- Deferred acceptance obligations.
- Formal closure prerequisites.
- Operator ownership and future work handoff.

Use the following target classification, subject to verification:

`PHASE_17I_ENGINEERING_COMPLETE`

`PHASE_17I_DOCUMENTATION_COMPLETE`

`PHASE_17I_EXTERNAL_VERIFICATION_DEFERRED`

`PHASE_17I_FORMAL_ACCEPTANCE_PENDING`

`SUBSEQUENT_ENGINEERING_PERMITTED`

Do not use a single unqualified `PHASE_17I_COMPLETE` status that would falsely imply external-user verification happened.

The three-stage engineering/documentation workflow is complete after successful Stage 3 validation.

The original Phase 17I external acceptance remains open.

No fourth formal stage is created.

---

## 12. Documentation review and validation

This is a documentation-first task.

No new implementation feature is authorized.

Do not modify source code, security controls, provider contracts, databases or deployment configuration merely to complete documentation.

If documentation reveals a genuine critical implementation problem:

- Record the defect.
- Identify the affected existing contract and tests.
- State the targeted remediation needed.
- Do not hide the defect.
- Do not mark the affected gate PASS.

Do not silently expand this task into a new engineering phase.

### Required validation

Perform:

```bash
git diff --check
git status --short --branch
git diff --stat
git diff --cached --name-only
```

Check all newly created Markdown files for whitespace issues.

Validate local relative links and heading anchors.

Verify JSON record templates remain valid and their intentionally blank approvals remain unapproved.

Review all current Phase 17I status declarations for consistency.

Check that historical Phase 17H and Stage 2 records remain intact.

Inspect changed documentation for:

- Secrets.
- Real identities.
- Tokens or private keys.
- Machine-specific operational paths.
- Protected audit/runtime material.
- Unsupported deployment claims.
- Invented consent or reviewer records.
- Inconsistent test counts.
- Fabricated cost figures.
- Incorrect physical-deletion claims.
- Broken documentation links.

Do not rerun the full 3,052-test suite or repeat successful CI merely for documentation finalization.

Do not initiate Azure, Ollama, vLLM or any other real inference.

Do not provision, deploy or contact external participants.

---

## 13. Final Stage 3 report

Create:

`docs/codex/reports/phase_17i_documentation_and_closure.md`

Save a faithful task prompt under:

`docs/codex/prompts/phase_17i_documentation_and_closure.md`

The report must include:

### Executive decision

- Stage 1 — COMPLETE.
- Stage 2 — ENGINEERING PASS.
- Stage 3 — DOCUMENTATION PASS, if verified.
- Phase 17I bounded engineering — COMPLETE.
- Actual external-user verification — DEFERRED/PENDING.
- Formal external-user acceptance — PENDING.
- Production readiness — NOT ESTABLISHED.

### Evidence reconciliation

- Exact Git commit and successful CI record.
- Recorded 3,052-test result.
- Synthetic end-to-end outcome.
- Implementation scope and limitations.
- Source/provenance and security boundaries.
- Financial and retention boundaries.

### Documentation changes

- Every modified file.
- Every new file.
- Links checked.
- Status updates.
- Gate reconciliation.
- Deferred-acceptance entry.
- Operator runbook changes.

### Pending decisions

Identify the responsible future decision-makers and required evidence for:

- Independent quality acceptance.
- Privacy and processing rights.
- Retention and cleanup.
- Real participant approval.
- Actual study execution.
- Paid inference, if used.
- Formal acceptance.

Do not invent dates or approvals.

### Handoff

Identify the next actual roadmap workstream, if any.

Do not invent Phase 18 implementation requirements or claim that production deployment has already been approved.

Any subsequent development may proceed independently, subject to its own prerequisites.

---

## 14. Git safety and commit preparation

The operator manually manages Git commits and pushes.

Do not:

- Stage files.
- Commit.
- Push.
- Reset.
- Clean.
- Stash.
- Rebase.
- Delete the 28 inherited historical Phase 17H documents.
- Rewrite execution history.

At the end, give an exact file-specific staging inventory for the Stage 3 documentation changes.

Separate intended Stage 3 changes from inherited files.

Suggested commit message:

`docs: finalize Phase 17I engineering closure with external verification deferred`

Leave all changes uncommitted.

---

## 15. Final acceptance rules

### Stage 3 PASS requires

1. Documentation accurately reflects the committed implementation.
2. Three-stage policy is consistent across current phase documents.
3. README and roadmap no longer incorrectly describe Phase 17I engineering as not started.
4. Existing technical results and CI are preserved accurately.
5. All 16 readiness gates have a current evidence-based disposition.
6. External-user verification remains explicitly deferred.
7. Phase 17H's separate two-human-review obligation remains unchanged.
8. Production readiness is not falsely claimed.
9. Documentation links and integrity checks pass.
10. Git changes are restricted to authorized documentation.
11. No external interaction, cloud spending or unapproved execution occurred.

If these conditions are satisfied, conclude:

**`PHASE_17I_STAGE3_DOCUMENTATION_PASS`**

**`PHASE_17I_ENGINEERING_COMPLETE`**

**`PHASE_17I_EXTERNAL_VERIFICATION_DEFERRED`**

**`PHASE_17I_FORMAL_ACCEPTANCE_PENDING`**

**`SUBSEQUENT_ENGINEERING_PERMITTED`**

If any required condition fails, report PARTIAL/BLOCKED with exact remediation instead of manufacturing a PASS.

---

## Final instruction to Codex

Complete **Phase 17I Stage 3 — Documentation and Closure** now.

Do not repeat the successful implementation or 3,052-test validation.

Reconcile the README, roadmap, current acceptance gates, operator documentation and technical evidence.

Declare the **bounded Phase 17I engineering work complete**, while keeping actual external-user verification as a separately tracked deferred acceptance obligation.

Do not create new development stages, recruit reviewers or participants, deploy services, spend money or change the existing quality thresholds.

Deliver the finished documentation and final evidence report for operator review, without committing or pushing.
