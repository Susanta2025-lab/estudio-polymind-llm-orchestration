"""Synthetic structural witnesses; no recorded provider content or identifiers."""

from documents.digestion.codec import encode
from documents.digestion.models import Claim, ClaimLink, Qualification, StageResult
from documents.models import stable_id


def eight_claim_result(request, *, canonical_bytes=None):
    """Eight claims, four source IDs, complete links and one qualification.

    The reduction shape reproduces the live witness's serialization costs using
    only synthetic source IDs and placeholder prose. All bytes are measured with
    the production codec; no private live values are copied.
    """
    evidence = tuple(p.evidence_id() for p in request.source_data) or tuple(
        sorted(
            {
                eid
                for child in request.children
                for claim in child.result.claims
                for eid in (*claim.evidence_ids, *claim.contradicting_evidence_ids)
            },
            key=str,
        )
    )
    assert len(evidence) == 4
    links = tuple(
        ClaimLink(stage_id=c.result.stage_id, claim_id=claim.claim_id)
        for c in request.children
        for claim in c.result.claims
    )
    assert not links or len(links) == 8
    kinds = (
        "fact",
        "fact",
        "fact",
        "commentary",
        "fact",
        "fact",
        "unknown",
        "structural",
    )
    claims = tuple(
        Claim(
            claim_id=stable_id(str(request.stage_id), str(i)),
            originating_stage=request.stage_id,
            text="Synthetic finding.",
            kind=kind,
            subject=("synthetic-access" if i < 2 else f"synthetic-{i}")
            if kind == "fact"
            else None,
            stance="denied" if i == 1 else "affirmed" if kind == "fact" else "unknown",
            status="unknown" if kind == "unknown" else "supported",
            evidence_ids=evidence if i >= 5 else (evidence[i % 4],),
            qualifications=(
                Qualification(
                    text="Synthetic qualification.", evidence_ids=evidence[:1]
                ),
            )
            if i == 2
            else (),
            lineage=(links[i],) if links else (),
        )
        for i, kind in enumerate(kinds)
    )
    result = StageResult(stage_id=request.stage_id, kind=request.stage, claims=claims)
    if canonical_bytes is not None:
        remaining = canonical_bytes - len(encode(result))
        assert remaining >= 0
        for i, claim in enumerate(result.claims):
            count = min(
                remaining, request.profile.max_claim_characters - len(claim.text)
            )
            updated = claim.model_copy(update={"text": claim.text + "x" * count})
            result = result.model_copy(
                update={
                    "claims": (*result.claims[:i], updated, *result.claims[i + 1 :])
                }
            )
            remaining -= count
        assert remaining == 0 and len(encode(result)) == canonical_bytes
    return result
