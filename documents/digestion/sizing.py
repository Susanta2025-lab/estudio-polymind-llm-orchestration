"""Conservative contributions to the existing nested managed JSON envelope.

No content is shortened. Duplicate evidence IDs are counted per child, although
the actual renderer deduplicates them, making the sum an upper bound.
"""
from documents.jobs.models import canonical

# Historical v5 reservation, retained for diagnostic/API compatibility. Runtime
# admission measures the complete ChildInput; this is not an output restriction.
CHILD_WRAPPER_BYTES = 1024


def escaped_size(value):
    """JSON embedded in a string in the outer generation envelope."""
    return len(canonical(canonical(value)).encode('ascii')) - 2


def result_contribution(result):
    links = [{'stage_id': str(result.stage_id), 'claim_id': str(c.claim_id)}
             for c in result.claims]
    evidence = sorted({str(e) for c in result.claims
                       for e in (*c.evidence_ids, *c.contradicting_evidence_ids)})
    # Extra array punctuation covers separators when concatenating child lists.
    return (escaped_size(result.model_dump(mode='json')) + escaped_size(links)
            + escaped_size(evidence) + 8)


def child_contribution(child):
    return (result_contribution(child.result)
            + escaped_size(child.model_dump(mode='json'))
            - escaped_size(child.result.model_dump(mode='json')))


def reduction_size(profile, path, children):
    budget = profile.managed_input_budget
    return (budget.base_bytes + escaped_size(path) - escaped_size(())
            + children * budget.child_bytes)


def analysis_size(request):
    pieces = [{'evidence_id': str(p.evidence_id()), 'text': p.text, 'kind': p.kind,
               'cells': p.cells, 'limitation': p.limitation} for p in request.source_data]
    evidence = sorted({str(p.evidence_id()) for p in request.source_data})
    return (reduction_size(request.profile, request.structural_path, 0)
            + escaped_size(pieces) + escaped_size(evidence))
