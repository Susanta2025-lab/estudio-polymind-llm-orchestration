# Phase 17H–L: generation instruction clarifications

> **ARCHIVED — 1 November 2026.** This is the original historical proposal.
> [managed_prompt_4.patch](managed_prompt_4.patch) is inactive and must not be
> applied as a current runtime update. Its broader qualification and unavailable-analysis
> changes were not automatically deployed. The active `managed-prompt/4` is the
> separately validated, narrower fact-only subject-contract correction described
> in the authoritative [v4 implementation report](../reports/phase_17hl_managed_prompt4_subject_contract_implementation.md).
> The [Attempt 6 closure report](../reports/phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md)
> is authoritative for successful single-call live validation. The patch remains
> byte-for-byte preserved. Statements below describe the original proposal-era state.

Status: **Proposed; READY FOR REVIEW; inactive**. Candidate: `managed-prompt/4`.
The runtime remains `managed-prompt/3`, `managed-generation/2`, `stage-result/1`
for strict digestion. No live evaluation or model acceptance improvement is claimed.

## Exact production fragments and replacement

The fragments below were extracted from `ManagedSynthesisInference.render()`.
All other instruction text, task suffixes, dynamic controls and serialization
remain as currently implemented. The complete versioned proposed change is
[managed_prompt_4.patch](managed_prompt_4.patch). It is a documentation artifact,
never imported or applied by application code.

### M1: local semantic constraints

Original:

```text
Represent unknown or unsupported conclusions explicitly using kind/status.
```

Replacement (spaces between lines are intentional):

```text
subject must be null on every non-fact claim. A non-null fact subject must be 1-128
characters matching ^[a-zA-Z0-9_./:-]+$. A fact must have status=supported and valid
direct evidence or supplied child links with acceptable source support.
Use kind=unknown/status=unknown or kind=unsupported/status=unsupported for those findings.
Within each evidence reference array use each allowed ID at most once; use only exact
supplied stage/claim pairs for lineage, with no duplicate child links within a claim.
```

`Claim.subject` uses `Token` from `documents/jobs/models.py`: minimum 1, maximum
128 and exactly the stated pattern. `validate_result()` rejects subjects on
non-facts. Facts need `status == supported` and either direct evidence IDs or
linked children with direct evidence or their own lineage. This is the actual
structural support predicate; it does not certify that prose is entailed by a
source. The proposed kind/status pairs are valid examples rather than a new
cross-field validator. Direct, contradicting and qualification reference arrays
remain membership-checked; child link pairs must exactly match supplied children.
Qualification arrays additionally require at least one evidence ID.

The unchanged instruction remains explicit: use `claim_ids_in_order`
consecutively, and `originating_stage=stage_id`. No repair is suggested.

### M2: qualification inheritance

Original (following the unchanged reduction lineage instruction):

```text
child text is not original source evidence. Preserve all child qualifications/conflicts.
```

Replacement:

```text
child text is not original source evidence. Preserve qualifying information through
required child lineage. Include a qualification directly only when its nonempty,
unique evidence IDs are allowed at this stage. Never manufacture ancestor evidence
IDs, invent sources or discard required child links. Application-owned immutable
child artifacts retain inherited qualifications and contradictions.
```

The actual direct allowed set is source evidence plus IDs literally present in
immediate child claims' `evidence_ids` or `contradicting_evidence_ids`. It excludes
IDs found only in child qualifications and IDs reachable only through ancestor
lineage. `render()` supplies exactly this set. Reduction coverage requires every
immediate child stage/claim pair across output lineage. Immutable checkpoints,
`inherited_summary()` and `make_digest()` retain the child graph, qualification
counts/text and propositions even when a reducer does not copy a qualifier.

Positive synthetic example: a chunk claim has qualification Q supported by E.
A structural claim links that chunk claim and does not directly cite E. Its root
parent links the structural claim and emits no copied qualification. E is absent
from the root's allowed direct IDs; the immutable child graph still preserves Q.
The persisted-qualification test in the compatibility suite verifies this graph
and accepted digest, including the retained qualification text.

Negative synthetic example: the root copies Q with evidence E into its own
qualification although E is absent from its current allowed direct set. JSON
Schema can accept its shape, but `validate_result()` rejects it with
`invalid_qualification_source`. It must retain the required lineage instead;
no ancestor citation can be invented or promoted into source authority.

### M3: unavailable analysis

Original:

```text
For analysis, reference EVERY allowed evidence ID across the claims.
```

Replacement:

```text
For analyzed analysis, reference EVERY allowed evidence ID across claims in evidence_ids
or contradicting_evidence_ids and obey all support rules. Only analysis may use
outcome=unavailable: emit zero claims and
at least one nonempty limitation; do not fabricate evidence or unsupported findings
to satisfy analyzed coverage. Reduction must use outcome=analyzed.
```

`validate_result()` requires unavailable results to be analysis, have no claims
and have limitations. `Text` makes each limitation nonempty; annotation, text and
byte limits still apply. Analyzed analysis requires claims and complete source
coverage through evidence_ids or contradicting_evidence_ids (qualification-only
citations do not count). A reduction cannot declare unavailable, including with empty claims.
This revision conditions coverage without relaxing any domain acceptance rule.

## Offline verification and activation

The new proposal witness tests render all four current profiles, validate a
contract-compatible analyzed response for each and separately exercise unavailable
analysis versus unavailable reduction. Existing end-to-end tests exercise immutable
qualification/contradiction inheritance. The proposed patch passes `git apply
--check` but has **not** been applied. Neither tests nor runtime import it.
These are consistency checks of instructions against deterministic validators;
they do not test a model's interpretation or predict its acceptance rate.

Activation requires separate authorization or completion and review of the next
diagnostic experiment. Review and apply the patch, migrate both StageProfile's
`template_version` and the adapter's bound `prompt_profile` to `managed-prompt/4`,
and re-run all profiles, coverage, provenance, governance and immutable-checkpoint
tests. The StageResult/provider schema need not change for this wording revision.
The renderer source, source-based generation digest, executor digest, adapter
configuration, planning profile, rendered controls, stage IDs and request hashes
will change. Old checkpoints and approvals must not be silently rebound or reused;
retain immutable historical artifacts and prepare fresh separately authorized
configuration/approval bindings through the existing workflow. Rollback restores
the old template/profile together and requires its matching plan/checkpoints.
