"""Strict five-call offline hierarchy, reusing the four-call L1 composition."""
import json

import pytest
from jsonschema import Draft202012Validator
from test_phase17hl_offline_e2e import assert_accounting, corrupt, reopen
from test_phase17hl_offline_e2e import (
    l1 as l1,  # noqa: PLC0414 -- pytest fixture re-export
)
from test_phase17hl_offline_e2e import (
    offline as offline,  # noqa: PLC0414 -- pytest fixture re-export
)

from documents.digestion import workflow
from documents.digestion.codec import encode, read
from documents.digestion.managed import (
    ManagedDigestionHandler,
    classify_managed,
    generation_schema,
)
from documents.digestion.models import Checkpoint, DigestionError, StageResult
from documents.digestion.sizing import CHILD_WRAPPER_BYTES, result_contribution
from documents.jobs.worker import LocalDispatcher, Worker, relay
from llm.azure_schema import provider_schema


def test_two_chunk_strict_hierarchy_publication_qa_and_reuse(l1):
    state = l1(two_chunks=True)
    plan = state.plan
    assert len(plan.chunks) == len(plan.reducers) == 2
    assert plan.reducers[0].children == tuple(c.chunk_id for c in plan.chunks)
    assert plan.reducers[1].children == (plan.reducers[0].stage_id,)
    assert [c['stage'] for c in state.http.calls] == ['chunk', 'chunk', 'structural', 'root', 'question']
    assert state.result['job_state'] == 'COMPLETED'
    assert state.result['questions']['status'] == 'COMPLETE'
    assert state.result['planned_calls'] == 5
    assert state.replica.ready()
    assert str(state.replica.reader.authority.active().generation) == state.replica.expected_version
    for number, (_, sent) in enumerate(state.sent[:4]):
        assert sent['json']['response_format']['json_schema']['strict'] is True
        result = json.loads(state.http.calls[number]['response'])
        Draft202012Validator(provider_schema(generation_schema())).validate(result)
        request = state.requests[number]
        assert {(str(c.result.stage_id), str(f.claim_id)) for c in request.children for f in c.result.claims} == {
            (link['stage_id'], link['claim_id']) for f in result['claims'] for link in f['lineage']}
    jobs, store, scope, digest = reopen(state)
    assert digest.status == 'COMPLETE' and digest.coverage.fraction == 1
    assert set(digest.coverage.included) == set(digest.coverage.eligible) == set(plan.eligible)
    assert not digest.coverage.failed and not digest.coverage.unsupported
    assert len(digest.checkpoints) == 4
    assert len(jobs.steps(scope, state.job.job_id)) == 6
    assert all(s.state == 'SUCCEEDED' for s in jobs.steps(scope, state.job.job_id))
    assert {q.text for q in digest.qualifications} == {'Only during daytime.', 'During maintenance.'}
    assert 'Only during daytime.' in digest.executive_summary
    assert 'During maintenance.' in digest.executive_summary
    assert 'unresolved' in digest.executive_summary
    conflict, = digest.contradictions
    assert conflict.subject == 'access' and conflict.resolution == 'unresolved'
    assert {*conflict.affirmed, *conflict.denied} == {f.claim_id for f in digest.findings}
    for step in jobs.steps(scope, state.job.job_id):
        if step.spec.unit_id == str(plan.root_id):
            cp = read(store, scope, step.manifest[0], Checkpoint, plan.profile.max_artifact_bytes)
            assert cp.inherited.analyzed_pieces == 4
            assert cp.inherited.qualifications == 2 and cp.inherited.contradictions == 1
    qa = json.loads(state.generations[-1].data)
    annotations, = qa['DERIVED_RETRIEVAL_MATERIAL']
    assert {q['text'] for q in annotations['qualifications']} == {q.text for q in digest.qualifications}
    assert {f['stance'] for f in annotations['conflicting_findings']} == {'affirmed', 'denied'}
    assert annotations['contradictions'][0]['resolution'] == 'unresolved'
    packet, = json.loads((state.root/'review-packets.json').read_text())
    answer = packet['response']
    assert answer['answer'] == answer['citations'][0]['excerpt']
    assert 'Access is permitted during daytime.' in answer['answer']
    assert answer['citations'][0]['physical_page'] == 1
    for citation in answer['citations']:
        unit = next(u for u in state.artifact.units if u.physical_page == citation['physical_page'])
        span = citation['span']
        assert citation['excerpt'] == unit.text[span['start']:span['end']]
        assert citation['document_version_id'] == str(state.artifact.document.document_version_id)
        assert citation['extraction_id'] == str(state.artifact.extraction_id)
        assert citation['provenance'] == 'validated'
    assert_accounting(state, 5)
    resumed = workflow.admit(jobs, store, plan, state.plan_ref, request_key='two-chunk-resume',
        resume_from=state.job.job_id, retry=state.job.admission.profile.retry)
    queue = LocalDispatcher()
    worker = Worker(jobs, queue, store,
        ManagedDigestionHandler(jobs, state.plan_ref, state.handler.inference),
        owner='two-chunk-reopen', classifier=classify_managed)
    for _ in range(plan.profile.max_steps):
        relay(jobs, queue)
        if not worker.once():
            break
    assert workflow.load_digest(jobs, store, scope, resumed.job_id) == digest
    assert len(state.sent) == 5
    assert state.handler.inference.governance.ledger.usage(state.principal, state.authority) == state.result['governance_records']


@pytest.mark.parametrize('fault,target,calls', [
    ('lineage', 'structural', 3), ('coverage', 'structural', 3), ('omit_child', 'structural', 3),
    ('lineage', 'root', 4), ('coverage', 'root', 4),
    ('oversized', 'chunk', 1), ('oversized', 'structural', 3), ('oversized', 'root', 4),
])
def test_two_chunk_rejection_keeps_usage_and_prevents_publication(l1, fault, target, calls):
    def transform(value, stage):
        if stage != target:
            return value
        if fault == 'omit_child':
            result = json.loads(value)
            links = result['claims'][0]['lineage']
            assert len({link['stage_id'] for link in links}) == 2
            result['claims'][0]['lineage'] = links[:1]
            return json.dumps(result)
        if fault != 'oversized':
            return corrupt(value, fault)
        result = json.loads(value)
        # Below 10k canonical, but cannot be admitted to a downstream envelope.
        result['open_questions'] = [('\\"' * 100) + str(i) for i in range(8)]
        output = StageResult.model_validate(result)
        assert len(encode(output)) < 10000
        assert result_contribution(output) + CHILD_WRAPPER_BYTES > 7000
        return json.dumps(result)
    state = l1(transform, two_chunks=True)
    assert state.result['job_state'] == 'FAILED'
    assert state.result['terminal_category'] == ('extraction_limit_exceeded' if fault == 'oversized'
        else 'invalid_reference' if fault == 'lineage' else 'extraction_failed')
    assert 'publication' not in state.result and 'questions' not in state.result
    assert_accounting(state, calls)
    steps = state.jobs.steps(state.artifact.document.scope, state.job.job_id)
    assert all(not s.manifest for s in steps if s.state == 'FAILED' or s.spec.unit_id == 'digest')
    with pytest.raises(DigestionError):
        workflow.load_digest(state.jobs, state.store, state.artifact.document.scope, state.job.job_id)
