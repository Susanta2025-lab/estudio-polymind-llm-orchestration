"""Current strict 10k result contract versus complete downstream envelopes."""
import json
from io import BytesIO
from uuid import UUID

import pytest

from documents.digestion.codec import encode, put
from documents.digestion.managed import (
    ManagedSettings,
    ManagedSynthesisInference,
    StageProfile,
)
from documents.digestion.models import Checkpoint, DigestionError, InheritedSummary
from documents.digestion.planning import build_plan
from documents.digestion.sizing import (
    CHILD_WRAPPER_BYTES,
    child_contribution,
    reduction_size,
    result_contribution,
)
from documents.digestion.validation import (
    EvidenceIndex,
    inherited_summary,
    validate_result,
)
from documents.digestion.workflow import DigestionHandler
from documents.extraction import extract
from documents.jobs.models import fingerprint
from documents.storage import LocalObjectStore
from llm.inference import InferenceContextError
from tests.performance.fixtures import NOW, SCOPE, pdf, profile
from tests.performance.foundry_envelopes import NoInference, maximal_result
from tests.performance.foundry_recalibration import candidate_capability


def adapter(child_bytes=None):
    settings = ManagedSettings(capability=candidate_capability(strict_digestion=True),
        generation_profile='managed-generation/2', child_input_bytes=child_bytes,
        max_response_envelope_bytes=26192, profiles=tuple(StageProfile(
            stage=s, input_tokens=24800, output_tokens=3000)
            for s in ('chunk', 'intermediate', 'structural', 'root')))
    return ManagedSynthesisInference(NoInference(), settings, None)


def setup(tmp_path, *, bounded=False, chunk_characters=800):
    store = LocalObjectStore(tmp_path/'objects')
    artifact, ref = extract(BytesIO(pdf(4)[0]), scope=SCOPE, document_id=UUID(int=4),
        display_filename='synthetic.pdf', declared_mime='application/pdf', store=store,
        created_at=NOW, extracted_at=NOW)
    inference = adapter(7000 if bounded else None)
    chosen = inference.profile(profile(context_tokens=28000, reserved_output_tokens=3000,
        max_result_characters=10000, max_response_bytes=10000, chunk_characters=chunk_characters))
    plan = build_plan(artifact, ref, chosen)
    return store, artifact, inference, plan


def checkpoint(store, plan, request, result, cps, refs):
    inherited, propositions = inherited_summary(result, request, tuple(cps[c.result.stage_id] for c in request.children))
    cp = Checkpoint(plan_hash=fingerprint(plan.model_dump(mode='json')), parents=tuple(
        c.artifact for c in request.children), result=result, inherited=inherited, propositions=propositions)
    cps[request.stage_id] = cp
    refs[request.stage_id] = put(store, SCOPE, cp, plan.profile.max_artifact_bytes)


def near_limit(request, index):
    result, _ = maximal_result(request, index, 'claims')
    # All eight claims and canonical evidence remain; annotations fill unused bytes.
    for field in ('open_questions', 'limitations'):
        for i in range(request.profile.max_annotations):
            best = None
            for length in range(1, request.profile.max_claim_characters+1):
                text = (('\\"' * 128)[:length-1] + str(i))
                candidate = result.model_copy(update={field: (*getattr(result, field), text)})
                if len(encode(candidate)) > 10000:
                    break
                best = candidate
            if best is not None:
                result = best
    assert 9900 <= len(encode(result)) <= 10000
    return validate_result(encode(result), request, index)


def plain_result(request, index, escape=None):
    legacy = request.model_copy(update={'profile': request.profile.model_copy(update={'managed_input_budget': None})})
    result, _ = maximal_result(legacy, index, 'escaped')
    result = result.model_copy(update={field: tuple(text.replace('\\', 'a') for text in getattr(result, field))
                                      for field in ('open_questions', 'limitations')})
    if escape is not None:
        original = result
        low, high = 0, request.profile.max_claim_characters
        while low < high:
            middle = (low+high+1)//2
            candidate = original.model_copy(update={field: tuple(text.replace('a', escape, middle)
                for text in getattr(original, field)) for field in ('open_questions', 'limitations')})
            if result_contribution(candidate) + CHILD_WRAPPER_BYTES <= 7000 and len(encode(candidate)) <= 10000:
                low, result = middle, candidate
            else:
                high = middle-1
    return validate_result(encode(result), request, index), len(encode(result))


@pytest.mark.parametrize('chunks', [1, 2])
def test_legacy_10k_results_reproduce_escaped_downstream_overflow(tmp_path, chunks):
    store, artifact, inference, plan = setup(tmp_path, chunk_characters=3200 if chunks == 1 else 800)
    assert len(plan.chunks) == chunks
    index, cps, refs = EvidenceIndex(artifact), {}, {}
    # Render-only diagnostic continuation: never execute or claim workflow success.
    for node in (*plan.chunks, *plan.reducers):
        key = getattr(node, 'chunk_id', None) or node.stage_id
        request = DigestionHandler.request(plan, key, cps, refs)
        if request.stage == 'reduction':
            for stage in (('root',) if key == plan.root_id else ('intermediate', 'structural')):
                with pytest.raises(InferenceContextError):
                    inference.bind(None, stage).analyze(request)
                generation, _ = inference.bind(None, stage).render(request, _check_limits=False)
                assert 'required_child_links' in generation.system
                assert 'inherited' in generation.data and 'qualifications' in generation.data
        result, size = maximal_result(request, index, 'escaped')
        assert 8000 < size <= 10000
        checkpoint(store, plan, request, result, cps, refs)


def test_bounded_output_admission_rejects_application_valid_10k_shape(tmp_path):
    _, artifact, _, plan = setup(tmp_path, bounded=True)
    request = DigestionHandler.request(plan, plan.chunks[0].chunk_id, {}, {})
    # The old application contract accepts this unchanged near-10k witness.
    legacy = request.model_copy(update={'profile': request.profile.model_copy(update={'managed_input_budget': None})})
    result = near_limit(legacy, EvidenceIndex(artifact))
    assert result_contribution(result) + CHILD_WRAPPER_BYTES > 7000
    with pytest.raises(DigestionError, match='synthesis_limit_exceeded'):
        validate_result(encode(result), request, EvidenceIndex(artifact))
    assert len(encode(result)) <= request.profile.max_result_characters == 10000


@pytest.mark.parametrize('escape', [None, '\\', '"', '\u0800'])
def test_bounded_plan_admits_over_3907_bytes_and_every_reducer_fits(tmp_path, escape):
    store, artifact, inference, plan = setup(tmp_path, bounded=True)
    assert len(plan.chunks) == len(plan.reducers) == 2
    index, cps, refs = EvidenceIndex(artifact), {}, {}
    for node in (*plan.chunks, *plan.reducers):
        key = getattr(node, 'chunk_id', None) or node.stage_id
        request = DigestionHandler.request(plan, key, cps, refs)
        # Complete claims/annotations above the historical response size still fit.
        result, size = plain_result(request, index, escape)
        assert 3907 < size <= 10000
        assert result_contribution(result) + CHILD_WRAPPER_BYTES <= 7000
        if request.children:
            assert all(child_contribution(c) <= 7000 for c in request.children)
            for stage in (('root',) if key == plan.root_id else ('intermediate', 'structural')):
                generation, estimate = inference.bind(None, stage).render(request)
                assert json.loads(generation.data)['GENERATED_CHILD_MATERIAL'] == [
                    c.model_dump(mode='json') for c in request.children]
                bound = reduction_size(plan.profile, request.structural_path, len(request.children))
                assert estimate-200 <= bound <= 24800
                assert estimate+generation.output_tokens <= generation.capability.context_tokens
            assert node.estimated_tokens == bound
        else:
            generation, estimate = inference.render(request)
            assert estimate-200 <= node.estimated_tokens <= 24800
        checkpoint(store, plan, request, result, cps, refs)


@pytest.mark.parametrize('child_bytes', [8000, 16000])
def test_impossible_fanin_is_rejected_during_planning(tmp_path, child_bytes):
    _, artifact, _, plan = setup(tmp_path)
    inference = adapter(child_bytes)
    with pytest.raises(DigestionError, match='synthesis_limit_exceeded'):
        build_plan(artifact, plan.structure.extraction, inference.profile(plan.profile))


def test_actual_child_wrapper_and_path_are_checked_without_truncation(tmp_path):
    store, artifact, inference, plan = setup(tmp_path, bounded=True)
    cps, refs = {}, {}
    index = EvidenceIndex(artifact)
    for chunk in plan.chunks:
        request = DigestionHandler.request(plan, chunk.chunk_id, cps, refs)
        result, _ = plain_result(request, index)
        checkpoint(store, plan, request, result, cps, refs)
    request = DigestionHandler.request(plan, plan.reducers[0].stage_id, cps, refs)
    huge_path = request.model_copy(update={'structural_path': ('\\"'*5000,)})
    with pytest.raises(DigestionError, match='synthesis_limit_exceeded'):
        inference.bind(None, 'structural').analyze(huge_path)
    child = request.children[0]
    inherited = InheritedSummary(qualifications=10**2000)
    huge_child = child.model_copy(update={'inherited': inherited})
    malformed = request.model_copy(update={'children': (huge_child, *request.children[1:])})
    with pytest.raises(DigestionError, match='synthesis_limit_exceeded'):
        inference.bind(None, 'structural').analyze(malformed)
    assert request.children[0] == child


def test_render_rejects_removed_policy_before_inference(tmp_path):
    _, _, inference, plan = setup(tmp_path, bounded=True)
    request = DigestionHandler.request(plan, plan.chunks[0].chunk_id, {}, {})
    tampered = request.model_copy(update={'profile': request.profile.model_copy(update={'managed_input_budget': None})})
    with pytest.raises(DigestionError, match='incompatible_checkpoint'):
        inference.analyze(tampered)
