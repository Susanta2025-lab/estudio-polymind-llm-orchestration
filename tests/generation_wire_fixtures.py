"""Synthetic immutable v10 requests and model-authored selections for regressions."""

from io import BytesIO
from uuid import UUID

from documents.digestion.codec import put
from documents.digestion.models import Checkpoint
from documents.digestion.validation import (
    EvidenceIndex,
    inherited_summary,
    validate_result,
)
from documents.digestion.wire import references
from documents.digestion.workflow import DigestionHandler, prepare
from documents.extraction import extract
from documents.jobs.models import canonical, fingerprint
from documents.storage import LocalObjectStore
from tests.performance.fixtures import NOW, SCOPE, pdf, profile
from tests.performance.foundry_envelopes import NoInference
from tests.performance.foundry_recalibration import candidate_capability
from tests.reducer_sizing_fixtures import eight_claim_result


def inference(*, strict=True, bounded=True, legacy=False):
    if legacy:
        from tests.historical_managed import (
            ManagedSettings,
            ManagedSynthesisInference,
            StageProfile,
        )
    else:
        from documents.digestion.managed import (
            ManagedSettings,
            ManagedSynthesisInference,
            StageProfile,
        )
    return ManagedSynthesisInference(
        NoInference(),
        ManagedSettings(
            capability=candidate_capability(strict_digestion=strict),
            generation_profile="managed-generation/2"
            if strict
            else "managed-generation/1",
            child_input_bytes=7000 if bounded else None,
            max_response_envelope_bytes=26192,
            profiles=tuple(
                StageProfile(stage=s, input_tokens=24800, output_tokens=3000)
                for s in ("chunk", "intermediate", "structural", "root")
            ),
        ),
        None,
    )


def proposal(request, result=None):
    """Authored fixture, never production repair or a decoder inverse used at runtime."""
    result = result or eight_claim_result(request)
    table = references(request)
    evidence = {str(e): f"E{i + 1}" for i, e in enumerate(table.evidence)}
    pairs = {(str(s), str(c)): f"C{i + 1}" for i, (s, c) in enumerate(table.children)}
    out = result.model_dump(mode="json")
    del out["stage_id"], out["kind"]
    out.update(schema_version="stage-proposal/1", request_binding=table.digest)
    for c in out["claims"]:
        del c["claim_id"], c["originating_stage"]
        c["evidence_refs"] = [evidence[e] for e in c.pop("evidence_ids")]
        c["contradicting_evidence_refs"] = [
            evidence[e] for e in c.pop("contradicting_evidence_ids")
        ]
        c["child_refs"] = [
            pairs[(p["stage_id"], p["claim_id"])] for p in c.pop("lineage")
        ]
        for q in c["qualifications"]:
            q["evidence_refs"] = [evidence[e] for e in q.pop("evidence_ids")]
    return out


def cases(root, *, chunk_characters=3200, strict=True, legacy=False):
    store = LocalObjectStore(root / "objects")
    artifact, extraction = extract(
        BytesIO(pdf(4)[0]),
        scope=SCOPE,
        document_id=UUID(int=4),
        display_filename="synthetic.pdf",
        declared_mime="application/pdf",
        store=store,
        created_at=NOW,
        extracted_at=NOW,
    )
    adapter = inference(strict=strict, legacy=legacy)
    bound = adapter.profile(
        profile(
            context_tokens=28000,
            reserved_output_tokens=3000,
            max_result_characters=10000,
            max_response_bytes=10000,
            chunk_characters=chunk_characters,
        )
    )
    plan, plan_ref = prepare(artifact, extraction, bound, store)
    index, checkpoints, refs, records = EvidenceIndex(artifact), {}, {}, {}
    for key in [c.chunk_id for c in plan.chunks] + [n.stage_id for n in plan.reducers]:
        request = DigestionHandler.request(plan, key, checkpoints, refs)
        # Two-child sizing uses a smaller canonical witness; eight claims are
        # retained in the one-child L1 quality/recovery witness.
        if len(plan.chunks) == 1:
            result = eight_claim_result(request)
        else:
            from documents.digestion.models import Claim, ClaimLink, StageResult
            from documents.models import stable_id

            result = StageResult(
                stage_id=key,
                kind=request.stage,
                claims=(
                    Claim(
                        claim_id=stable_id(str(key), "0"),
                        originating_stage=key,
                        text="Synthetic.",
                        kind="fact" if request.stage == "analysis" else "commentary",
                        evidence_ids=tuple(
                            p.evidence_id() for p in request.source_data
                        ),
                        lineage=tuple(
                            ClaimLink(stage_id=c.result.stage_id, claim_id=k.claim_id)
                            for c in request.children
                            for k in c.result.claims
                        ),
                    ),
                ),
            )
        validate_result(
            canonical(result.model_dump(mode="json")).encode(), request, index
        )
        inherited, propositions = inherited_summary(
            result,
            request,
            tuple(checkpoints[c.result.stage_id] for c in request.children),
        )
        cp = Checkpoint(
            plan_hash=fingerprint(plan.model_dump(mode="json")),
            parents=(plan_ref, extraction)
            if request.stage == "analysis"
            else tuple(c.artifact for c in request.children),
            result=result,
            inherited=inherited,
            propositions=propositions,
        )
        refs[key] = put(store, SCOPE, cp, bound.max_artifact_bytes)
        checkpoints[key] = cp
        records[
            "chunk"
            if request.stage == "analysis"
            else "root"
            if key == plan.root_id
            else "structural"
        ] = (request, result, index, cp, refs[key])
    return adapter, records, plan, plan_ref, store
