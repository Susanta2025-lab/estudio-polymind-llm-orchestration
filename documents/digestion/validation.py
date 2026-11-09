"""Application authority for evidence, lineage and coverage, independent of prose."""

from collections import defaultdict

from documents.digestion.codec import decode, encode
from documents.digestion.diagnostics import ValidationReason as Reason
from documents.digestion.models import (
    Contradiction,
    Coverage,
    DigestArtifact,
    DigestionError,
    InheritedSummary,
    Proposition,
    SectionSummary,
    StageResult,
    ChildInput,
    ValidationDiagnostic,
)
from documents.digestion.planning import check_request
from documents.models import stable_id


class EvidenceIndex:
    """Linear canonical indexing, O(1) source/block lookup; no repeated full scans."""
    def __init__(self, artifact):
        self.artifact = artifact
        self.blocks = {b.block_id: (u, b) for u in artifact.units for b in u.blocks}
        self.lines = {}
        for unit in artifact.units:
            if unit.physical_page is None:
                self.lines[unit.source_id] = [i for i, char in enumerate(unit.text) if char == '\n']

    def resolve(self, ref):
        from bisect import bisect_left
        doc = self.artifact.document
        pair = self.blocks.get(ref.block_id)
        if (ref.scope != doc.scope or ref.document_version_id != doc.document_version_id
                or ref.extraction_id != self.artifact.extraction_id or pair is None):
            raise DigestionError(
                "evidence_validation_failed",
                diagnostic=ValidationDiagnostic.EVIDENCE_VALIDATION,
                reason=(Reason.OTHER_EVIDENCE_VALIDATION),
            )
        unit, block = pair
        if (unit.source_id != ref.source_id or
                not block.span.start <= ref.span.start <= ref.span.end <= block.span.end):
            raise DigestionError(
                "evidence_validation_failed",
                diagnostic=ValidationDiagnostic.EVIDENCE_VALIDATION,
                reason=(Reason.OTHER_EVIDENCE_VALIDATION),
            )
        text = unit.text[ref.span.start:ref.span.end]
        lines = self.lines.get(unit.source_id)
        expected = None if lines is None else 1 + bisect_left(lines, ref.span.start)
        end = None if expected is None else expected + text.rstrip('\n').count('\n')
        if (ref.span.line_start, ref.span.line_end) != (expected, end):
            raise DigestionError(
                "evidence_validation_failed",
                diagnostic=ValidationDiagnostic.EVIDENCE_VALIDATION,
                reason=(Reason.OTHER_EVIDENCE_VALIDATION),
            )
        return text


def validate_result(raw, request, index):
    """Validate generated content; full child admission follows inherited_summary.

    The wrapper depends on application-owned lineage and artifact metadata. The
    worker must validate_child_material before committing or accepting a replay.
    """
    check_request(request)
    profile = request.profile
    result = decode(raw, StageResult, profile.response_byte_limit)
    if len(encode(result)) > profile.max_result_characters:
        raise DigestionError(
            "synthesis_limit_exceeded",
            diagnostic=ValidationDiagnostic.RESPONSE_LIMIT,
            reason=(Reason.CANONICAL_RESPONSE_LIMIT),
        )
    if profile.managed_input_budget is not None:
        from documents.digestion.sizing import result_contribution
        if result_contribution(result) > profile.managed_input_budget.child_bytes:
            raise DigestionError('synthesis_limit_exceeded',
                                 diagnostic=ValidationDiagnostic.RESPONSE_LIMIT,
                                 reason=Reason.CHILD_MATERIAL_LIMIT)
    if result.stage_id != request.stage_id or result.kind != request.stage:
        raise DigestionError(
            "inference_contract_error",
            diagnostic=ValidationDiagnostic.STAGE_BINDING,
            reason=(
                Reason.STAGE_ID_MISMATCH
                if result.stage_id != request.stage_id
                else Reason.STAGE_KIND_MISMATCH
            ),
        )
    if result.outcome == 'unavailable':
        if request.stage != 'analysis' or result.claims or not result.limitations:
            raise DigestionError(
                "inference_contract_error",
                diagnostic=ValidationDiagnostic.STAGE_BINDING,
                reason=(
                    Reason.UNAVAILABLE_REDUCTION
                    if request.stage != "analysis"
                    else Reason.UNAVAILABLE_WITH_CLAIMS
                    if result.claims
                    else Reason.UNAVAILABLE_MISSING_LIMITATION
                ),
            )
    elif request.stage == 'analysis' and not result.claims:
        raise DigestionError(
            "inference_contract_error",
            diagnostic=ValidationDiagnostic.STAGE_BINDING,
            reason=(Reason.ANALYZED_WITHOUT_CLAIMS),
        )
    if (len(result.claims) > profile.max_claims or len(result.open_questions) > profile.max_annotations
            or len(result.limitations) > profile.max_annotations):
        raise DigestionError(
            "synthesis_limit_exceeded",
            diagnostic=ValidationDiagnostic.RESPONSE_LIMIT,
            reason=(
                Reason.CLAIM_LIMIT
                if len(result.claims) > profile.max_claims
                else Reason.ANNOTATION_LIMIT
            ),
        )
    permitted = {}
    for piece in request.source_data:
        if index.resolve(piece.evidence) != piece.text:
            raise DigestionError(
                "evidence_validation_failed",
                diagnostic=ValidationDiagnostic.EVIDENCE_VALIDATION,
                reason=(Reason.OTHER_EVIDENCE_VALIDATION),
            )
        permitted[piece.evidence_id()] = piece.evidence
    links = {(child.result.stage_id, c.claim_id): c for child in request.children for c in child.result.claims}
    # Direct IDs must literally appear in supplied child claims. Other source sets
    # are inherited via validated claim links, not manufactured citation strings.
    inherited = {eid for child in request.children for claim in child.result.claims
                 for eid in (*claim.evidence_ids, *claim.contradicting_evidence_ids)}
    allowed = set(permitted) | inherited
    used, linked, ids = set(), set(), set()
    for position, claim in enumerate(result.claims):
        if (claim.claim_id != stable_id(str(request.stage_id), str(position))
                or claim.claim_id in ids or claim.originating_stage != request.stage_id):
            raise DigestionError(
                "inference_contract_error",
                diagnostic=ValidationDiagnostic.CLAIM_IDENTITY,
                reason=(
                    Reason.DUPLICATE_CLAIM_ID
                    if claim.claim_id in ids
                    else Reason.CLAIM_ID_MISMATCH
                    if claim.claim_id != stable_id(str(request.stage_id), str(position))
                    else Reason.ORIGINATING_STAGE_MISMATCH
                ),
            )
        ids.add(claim.claim_id)
        if len(claim.text) > profile.max_claim_characters or len(claim.qualifications) > profile.max_annotations:
            raise DigestionError(
                "synthesis_limit_exceeded",
                diagnostic=ValidationDiagnostic.RESPONSE_LIMIT,
                reason=(
                    Reason.TEXT_LIMIT
                    if len(claim.text) > profile.max_claim_characters
                    else Reason.ANNOTATION_LIMIT
                ),
            )
        references = (*claim.evidence_ids, *claim.contradicting_evidence_ids)
        for values in (claim.evidence_ids, claim.contradicting_evidence_ids):
            if len(set(values)) != len(values) or not set(values) <= allowed:
                raise DigestionError(
                    "evidence_validation_failed",
                    diagnostic=ValidationDiagnostic.EVIDENCE_VALIDATION,
                    reason=(
                        Reason.DUPLICATE_EVIDENCE
                        if len(set(values)) != len(values)
                        else Reason.FOREIGN_EVIDENCE
                    ),
                )
        used.update(references)
        lineage = [(link.stage_id, link.claim_id) for link in claim.lineage]
        if len(set(lineage)) != len(lineage) or not set(lineage) <= links.keys():
            raise DigestionError(
                "evidence_validation_failed",
                diagnostic=ValidationDiagnostic.EVIDENCE_VALIDATION,
                reason=(
                    Reason.DUPLICATE_CHILD_LINK
                    if len(set(lineage)) != len(lineage)
                    else Reason.INVALID_CHILD_LINK
                ),
            )
        linked.update(lineage)
        has_source = bool(claim.evidence_ids) or any(links[k].evidence_ids or links[k].lineage for k in lineage)
        if claim.kind == 'fact' and (not has_source or claim.status != 'supported'):
            raise DigestionError(
                "evidence_validation_failed",
                diagnostic=ValidationDiagnostic.EVIDENCE_VALIDATION,
                reason=(Reason.UNSUPPORTED_FACT),
            )
        for qualification in claim.qualifications:
            if (not qualification.evidence_ids or len(qualification.text) > profile.max_claim_characters
                    or len(set(qualification.evidence_ids)) != len(qualification.evidence_ids)
                    or not set(qualification.evidence_ids) <= allowed):
                raise DigestionError(
                    "evidence_validation_failed",
                    diagnostic=ValidationDiagnostic.EVIDENCE_VALIDATION,
                    reason=(Reason.TEXT_LIMIT if qualification.evidence_ids
                            and len(qualification.text) > profile.max_claim_characters
                            else Reason.INVALID_QUALIFICATION_SOURCE),
                )
        if claim.subject is not None and claim.kind != 'fact':
            raise DigestionError(
                "inference_contract_error",
                diagnostic=ValidationDiagnostic.CLAIM_CONTRACT,
                reason=(Reason.SUBJECT_ON_NONFACT),
            )
    if result.outcome == 'analyzed' and request.stage == 'analysis' and used != set(permitted):
        raise DigestionError(
            "coverage_failed",
            diagnostic=ValidationDiagnostic.COVERAGE_VALIDATION,
            reason=(Reason.MISSING_SOURCE_COVERAGE),
        )
    if request.stage == 'reduction' and linked != links.keys():
        # No silently dropped child claims/qualifiers.
        raise DigestionError(
            "coverage_failed",
            diagnostic=ValidationDiagnostic.COVERAGE_VALIDATION,
            reason=(Reason.MISSING_CHILD_COVERAGE),
        )
    for text in (*result.open_questions, *result.limitations):
        if len(text) > profile.max_claim_characters:
            raise DigestionError(
                "synthesis_limit_exceeded",
                diagnostic=ValidationDiagnostic.RESPONSE_LIMIT,
                reason=(Reason.TEXT_LIMIT),
            )
    return result


def validate_child_material(result, inherited, artifact, profile):
    """Admit unchanged result and actual lineage with a worst-size artifact ref.

    UUIDs and hashes have fixed width; reserving max_artifact_bytes for byte_size
    bounds the reference before storage. No guessed wrapper allowance is needed.
    """
    if profile.managed_input_budget is not None:
        from documents.digestion.sizing import child_contribution
        material = ChildInput(
            artifact=artifact.model_copy(update={'byte_size': profile.max_artifact_bytes}),
            result=result, inherited=inherited)
        if child_contribution(material) > profile.managed_input_budget.child_bytes:
            raise DigestionError('synthesis_limit_exceeded',
                                 diagnostic=ValidationDiagnostic.RESPONSE_LIMIT,
                                 reason=Reason.CHILD_MATERIAL_LIMIT)


def inherited_summary(result, request, children):
    """Application-owned annotation propagation; generated output cannot erase it.

    Full propositions stay in checkpoint objects, not in model input. Bounded
    counts and immutable child refs expose the inherited contract to reducers.
    Exact qualification text remains on linked original claims at every level.
    """
    subjects = defaultdict(lambda: [False, False])
    for cp in children:
        for prop in cp.propositions:
            sides = subjects[prop.subject]
            sides[0] |= prop.affirmed
            sides[1] |= prop.denied
    for claim in result.claims:
        if claim.subject and claim.stance in ('affirmed', 'denied'):
            subjects[claim.subject][claim.stance == 'denied'] = True
    propositions = tuple(Proposition(subject=key, affirmed=sides[0], denied=sides[1])
                         for key, sides in sorted(subjects.items()))
    own = len(request.source_data)
    summary = InheritedSummary(
        analyzed_pieces=sum(c.inherited.analyzed_pieces for c in children) + (own if result.outcome == 'analyzed' else 0),
        failed_pieces=sum(c.inherited.failed_pieces for c in children) + (own if result.outcome == 'unavailable' else 0),
        qualifications=sum(c.inherited.qualifications for c in children)+sum(len(c.qualifications) for c in result.claims),
        contradictions=sum(p.affirmed and p.denied for p in propositions),
        open_questions=sum(c.inherited.open_questions for c in children)+len(result.open_questions))
    return summary, propositions


def make_digest(plan, plan_ref, checkpoints, refs, index):
    expected = {c.chunk_id for c in plan.chunks} | {r.stage_id for r in plan.reducers}
    if set(checkpoints) != expected or set(refs) != expected:
        raise DigestionError('coverage_failed')
    # Walk the actual accepted claim graph from the root, not just successful calls.
    claims = {(stage, c.claim_id): c for stage, cp in checkpoints.items() for c in cp.result.claims}
    todo = [(plan.root_id, c.claim_id) for c in checkpoints[plan.root_id].result.claims]
    seen = set()
    while todo:
        key = todo.pop()
        if key in seen:
            continue
        if key not in claims:
            raise DigestionError('evidence_validation_failed')
        seen.add(key)
        todo.extend((link.stage_id, link.claim_id) for link in claims[key].lineage)
    analyzed_parts, included_parts = defaultdict(list), defaultdict(list)
    findings, evidence = [], {}
    for chunk in plan.chunks:
        result = checkpoints[chunk.chunk_id].result
        if result.outcome == 'unavailable':
            continue
        connected = all((chunk.chunk_id, c.claim_id) in seen for c in result.claims)
        if not connected:
            raise DigestionError('coverage_failed')
        findings.extend(result.claims)
        for piece in chunk.pieces:
            index.resolve(piece.evidence)
            evidence[piece.evidence_id()] = piece.evidence
            interval = (piece.evidence.span.start, piece.evidence.span.end)
            analyzed_parts[piece.evidence.block_id].append(interval)
            included_parts[piece.evidence.block_id].append(interval)

    def full(parts, block_id):
        _, block = index.blocks[block_id]
        cursor = block.span.start
        for start, end in sorted(parts[block_id]):
            if start > cursor:
                return False
            cursor = max(cursor, end)  # Union, so overlap never inflates coverage.
        return cursor == block.span.end and bool(parts[block_id])

    analyzed = tuple(key for key in plan.eligible if full(analyzed_parts, key))
    included = tuple(key for key in plan.eligible if full(included_parts, key))
    analyzed_set = set(analyzed)
    failed = tuple(key for key in plan.eligible if key not in analyzed_set)
    denominator = len(plan.eligible) + len(plan.unsupported)
    fraction = len(included)/denominator if denominator else 0
    coverage = Coverage(eligible=plan.eligible, analyzed=analyzed, failed=failed,
                        skipped=plan.skipped, unsupported=plan.unsupported, included=included, fraction=fraction)
    complete = not failed and not plan.unsupported and len(included) == len(plan.eligible)
    permitted_partial = (plan.profile.allow_partial and bool(included)
                         and fraction >= plan.profile.minimum_coverage
                         and len(failed) <= plan.profile.max_failed_units)
    status = 'COMPLETE' if complete else 'PARTIAL' if permitted_partial else 'FAILED'
    if fraction < plan.profile.minimum_coverage:
        status = 'FAILED'
    subjects = defaultdict(lambda: {'affirmed': [], 'denied': []})
    for claim in findings:
        if claim.subject and claim.stance in ('affirmed', 'denied'):
            subjects[claim.subject][claim.stance].append(claim.claim_id)
    contradictions = tuple(Contradiction(subject=subject, affirmed=tuple(sides['affirmed']),
                                        denied=tuple(sides['denied']))
                           for subject, sides in sorted(subjects.items()) if all(sides.values()))
    limitations = {text for cp in checkpoints.values() for text in cp.result.limitations}
    questions = {text for cp in checkpoints.values() for text in cp.result.open_questions}
    if not complete:
        limitations.add('Incomplete source coverage; this digest is not complete publishable knowledge.')
    if plan.unsupported:
        questions.add('Content unavailable for unsupported or unextractable source units.')
    if contradictions:
        questions.add('Conflicting source propositions remain unresolved.')
    root = checkpoints[plan.root_id].result
    summary = root.claims[0].text if root.claims else 'No supported root findings are available.'
    section_nodes = {n.structural_parent: n.stage_id for n in plan.reducers}
    sections = tuple(SectionSummary(structural_unit_id=u.structural_unit_id,
                                   stage_id=section_nodes[u.structural_unit_id],
                                   synthesis=checkpoints[section_nodes[u.structural_unit_id]].result.claims[0].text)
                     for u in plan.structure.units if u.kind in ('section', 'subsection')
                     and u.structural_unit_id in section_nodes
                     and checkpoints[section_nodes[u.structural_unit_id]].result.claims)
    return DigestArtifact(document_version_id=plan.structure.document_version_id,
                          extraction=plan.structure.extraction, plan=plan_ref, profile=plan.profile.digest(),
                          status=status, executive_summary=summary, root=plan.root_id, sections=sections,
                          findings=tuple(findings), synthesis_claims=root.claims,
                          qualifications=tuple(q for key, claim in claims.items() if key in seen
                                               for q in claim.qualifications),
                          contradictions=contradictions,
                          open_questions=tuple(sorted(questions)), coverage=coverage,
                          limitations=tuple(sorted(limitations)), evidence=tuple(evidence.values()),
                          checkpoints=tuple(refs[k] for k in checkpoints))
