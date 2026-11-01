"""Bounded offline DAG stress: maximal valid children, never model execution.

python -m tests.performance.foundry_envelopes --output /tmp/new-envelope-audit
"""
from io import BytesIO
import json
from pathlib import Path
from uuid import UUID

from documents.digestion.codec import encode, put
from documents.digestion.managed import ManagedSettings, ManagedSynthesisInference, StageProfile
from documents.digestion.models import (Checkpoint, Claim, ClaimLink, Qualification, StageResult)
from documents.digestion.validation import EvidenceIndex, inherited_summary, make_digest, validate_result
from documents.digestion.workflow import DigestionHandler, prepare
from documents.jobs.models import canonical, fingerprint
from documents.models import stable_id
from tests.performance.fixtures import SCOPE, NOW, pdf, profile
from tests.performance.foundry_recalibration import candidate_capability, reservation
from tests.performance.phase17h import write


class NoInference:
    name = 'openai_compatible'
    def model_id(self, role):
        return 'offline-envelope'
    def execute(self, request):
        raise AssertionError('Envelope assessment must never execute inference')


def maximal_result(request, index, mode):
    """Fill the existing 3000-byte canonical result budget without dropping links.

    These are adversarial structural fixtures, not independent semantic labels.
    quotes/backslashes test both JSON serialization layers of managed prompts.
    """
    limit = request.profile.max_result_characters
    evidence = tuple(p.evidence_id() for p in request.source_data)
    if not evidence:
        evidence = tuple(dict.fromkeys(e for child in request.children for claim in child.result.claims
                                       for e in claim.evidence_ids))[:1]
    links = tuple(ClaimLink(stage_id=child.result.stage_id, claim_id=claim.claim_id)
                  for child in request.children for claim in child.result.claims)
    def claim(i):
        return Claim(claim_id=stable_id(str(request.stage_id), str(i)), originating_stage=request.stage_id,
            text='x', kind='fact' if request.stage == 'analysis' else 'commentary',
            evidence_ids=evidence if i == 0 else evidence[:1], lineage=links if i == 0 else ())
    result = StageResult(stage_id=request.stage_id, kind=request.stage, claims=(claim(0),))
    if len(encode(result)) > limit:
        return None, len(encode(result))  # Complete lineage cannot fit, even with one-character prose.
    if mode == 'claims':
        for n in range(2, request.profile.max_claims+1):
            proposed = result.model_copy(update={'claims': tuple(claim(i) for i in range(n))})
            if len(encode(proposed)) <= limit:
                result = proposed
    else:
        if mode == 'conflicts' and request.stage == 'analysis':
            result = result.model_copy(update={'claims':tuple(claim(i).model_copy(update={
                'subject':'stress-opposition', 'stance':'affirmed' if i == 0 else 'denied'}) for i in range(2))})
        # One real canonical evidence ID supports structural qualification checks.
        if evidence:
            original = result.claims[0]
            qualified = original.model_copy(update={'qualifications':(Qualification(
                text='Qualification must survive every reduction.', evidence_ids=evidence[:1]),)})
            result = result.model_copy(update={'claims':(qualified, *result.claims[1:])})
        char = '\\' if mode in ('escaped', 'conflicts') else 'a'
        # Unique stage-prefixed annotations cannot be hidden by set deduplication.
        for field in ('open_questions', 'limitations'):
            for i in range(request.profile.max_annotations):
                prefix = f'{request.stage_id}:{i}:'
                best = None
                for length in range(1, request.profile.max_claim_characters-len(prefix)+1):
                    value = prefix + char*length
                    proposed = result.model_copy(update={field:(*getattr(result, field), value)})
                    if len(encode(proposed)) <= limit:
                        best = proposed
                    else:
                        break
                if best is None:
                    break
                result = best
    # Fill remaining bytes with ordinary characters, preserving the complete schema.
    for i in range(len(result.claims)):
        while len(result.claims[i].text) < request.profile.max_claim_characters:
            claims = list(result.claims)
            claims[i] = claims[i].model_copy(update={'text':claims[i].text+'x'})
            proposed = result.model_copy(update={'claims':tuple(claims)})
            if len(encode(proposed)) > limit:
                break
            result = proposed
    return validate_result(encode(result), request, index), len(encode(result))


def assess(root, pages, mode):
    from documents.config import ExtractionSettings
    from documents.extraction import extract
    from documents.storage import LocalObjectStore
    from documents.serialization import serialize
    from hashlib import sha256
    root.mkdir(parents=True)
    store = LocalObjectStore(root/'objects')
    raw, manifest = pdf(pages)
    artifact, ref = extract(BytesIO(raw), scope=SCOPE, document_id=UUID(int=pages),
        display_filename='manual.pdf', declared_mime='application/pdf', store=store, limits=ExtractionSettings(),
        created_at=NOW, extracted_at=NOW)
    assert [u.text.splitlines() for u in artifact.units] == [x['lines'] for x in manifest['expected']]
    assert sha256(serialize(artifact)).hexdigest() == ref.sha256
    settings = ManagedSettings(capability=candidate_capability(), profiles=tuple(
        StageProfile(stage=s, input_tokens=24800, output_tokens=3000)
        for s in ('chunk', 'intermediate', 'structural', 'root')))
    inference = ManagedSynthesisInference(NoInference(), settings, None)
    chosen = inference.profile(profile(context_tokens=28000, reserved_output_tokens=3000, max_result_characters=3000))
    plan, plan_ref = prepare(artifact, ref, chosen, store)
    index = EvidenceIndex(artifact)
    checkpoints, refs, records = {}, {}, []
    stages = [(c.chunk_id, 'chunk') for c in plan.chunks]
    for node in plan.reducers:
        siblings = [n for n in plan.reducers if n.structural_parent == node.structural_parent]
        kind = 'root' if node.stage_id == plan.root_id else ('structural' if node == siblings[-1] else 'intermediate')
        stages.append((node.stage_id, kind))
    for stage_id, kind in stages:
        request = DigestionHandler.request(plan, stage_id, checkpoints, refs)
        captured = []
        from llm.structured import GenerationRequest
        from unittest.mock import patch
        def capture(*args, **kwargs):
            value = GenerationRequest(*args, **kwargs)
            captured.append(value)
            return value
        failure = None
        try:
            with patch('documents.digestion.managed.GenerationRequest', capture):
                inference.bind(None, kind).render(request)
        except Exception as exc:
            failure = getattr(exc, 'category', type(exc).__name__)
        if not captured:
            records.append(dict(stage=kind, stage_id=str(stage_id), failure=failure))
            break
        generation = captured[0]
        estimate = len(canonical(dict(system=generation.system, data=generation.data, schema=generation.schema)).encode()) + 200
        rendered = dict(system_bytes=len(generation.system.encode()), user_bytes=len(generation.data.encode()),
                        schema_bytes=len(canonical(generation.schema).encode()), **reservation(estimate))
        result, size = maximal_result(request, index, mode)
        record = dict(stage=kind, stage_id=str(stage_id), rendered=rendered, child_count=len(request.children),
                      child_result_bytes=[len(encode(c.result)) for c in request.children],
                      required_links=sum(len(c.result.claims) for c in request.children), result_bytes=size)
        records.append(record)
        if failure:
            record['failure'] = failure
        if result is None:
            record['failure'] = 'complete_lineage_exceeds_result_bound'
            break
        inherited, propositions = inherited_summary(result, request, tuple(checkpoints[c.result.stage_id] for c in request.children))
        cp = Checkpoint(plan_hash=fingerprint(plan.model_dump(mode='json')), parents=(plan_ref,),
                        result=result, inherited=inherited, propositions=propositions)
        checkpoints[stage_id] = cp
        refs[stage_id] = put(store, SCOPE, cp, chosen.max_artifact_bytes)
    questions = None
    if len(checkpoints) == len(stages):
        digest = make_digest(plan, plan_ref, checkpoints, refs, index)
        assert digest.status == 'COMPLETE' and digest.coverage.fraction == 1
        questions = question_envelopes(artifact, digest, plan, pages, settings.capability)
    outcome = dict(pages=pages, mode=mode, chunks=len(plan.chunks), reducers=len(plan.reducers),
                   complete=len(checkpoints) == len(stages), records=records, questions=questions,
                   provider_calls=0, semantics='structural stress only; not human review')
    write(root/'result.json', outcome)
    return outcome


def question_envelopes(artifact, digest, plan, pages, capability):
    """Exercise the actual Q&A renderer with worst selected source excerpts.

    All annotations are derived exactly as PublicationReplica.annotations does.
    No semantic search claim: conservative eight longest canonical source excerpts.
    """
    from documents.publication.analysis import AnalysisRequest, AnalysisOutput, DocumentAnalysis, SYSTEM
    from documents.publication.retrieval import Citation
    from types import SimpleNamespace
    from llm.structured import GenerationResult
    paths = {p.evidence.block_id:c.path for c in plan.chunks for p in c.pieces}
    units = sorted([u for u in artifact.units for _ in range(2)], key=lambda u:len(u.text), reverse=True)
    citations = []
    for i in range(8):
        unit = units[i % len(units)]
        citations.append(Citation(citation_id=f'C{i+1}', generation=UUID(int=900), record_id=UUID(int=i+1),
            document_id=artifact.document.document_id, document_version_id=artifact.document.document_version_id,
            extraction_id=artifact.extraction_id, display_source=artifact.document.display_filename,
            physical_page=unit.physical_page, span=unit.blocks[0].span,
            structural_path=paths[unit.blocks[0].block_id], excerpt=unit.text))
    conflicting = {key for c in digest.contradictions for key in (*c.affirmed, *c.denied)}
    annotations = [dict(document_id=str(artifact.document.document_id), status=digest.status,
        qualifications=[q.model_dump(mode='json') for q in digest.qualifications],
        contradictions=[c.model_dump(mode='json') for c in digest.contradictions],
        conflicting_findings=[f.model_dump(mode='json') for f in digest.findings if f.claim_id in conflicting],
        limitations=digest.limitations, open_questions=digest.open_questions)]
    # Replica seam isolates rendering from already-covered publication storage.
    class Replica:
        def pin(self, *args, **kwargs):
            return SimpleNamespace(snapshot=(SimpleNamespace(generation=UUID(int=900)),))
        def retrieve(self, *args, **kwargs): return []
        def citations(self, *args): return citations
        def annotations(self, *args): return annotations
        def validate_pin(self, *args): pass
    captured = []
    class Capture:
        def execute(self, request):
            captured.append(len(canonical(dict(system=request.system, data=request.data, schema=request.schema)).encode())
                            + capability.overhead_tokens + capability.safety_tokens)
            return GenerationResult('{"answer":"offline","evidence_status":"insufficient","citation_ids":[]}')
    questions = ([dict(case_id='smoke-page1', question='What is the first inspection procedure on physical page 1?')]
                 if pages == 4 else json.loads(Path('tests/fixtures/phase17h/quality.json').read_text())['cases'])
    rows = []
    for case in questions:
        analysis = DocumentAnalysis(Replica(), Capture(), capability, input_bytes=24800, output_tokens=3000)
        data = []
        def capture_data(value):
            result = canonical(value)
            if isinstance(value, dict) and 'ORIGINAL_SOURCE_EVIDENCE' in value:
                data.append(result)
            return result
        failure = None
        try:
            from unittest.mock import patch
            with patch('documents.publication.analysis.canonical', capture_data):
                analysis.analyze(AnalysisRequest(query=case['question'], document_ids=(artifact.document.document_id,)))
        except Exception as exc:
            failure = getattr(exc, 'category', type(exc).__name__)
        schema = AnalysisOutput.model_json_schema()
        system = SYSTEM + '\nOUTPUT_SCHEMA\n' + canonical(schema)
        estimate = len(canonical(dict(system=system, data=data[0], schema=schema)).encode()) + 200
        row = dict(case_id=case['case_id'], **reservation(estimate, workload='INTERACTIVE'))
        if failure:
            row['failure'] = failure
        else:
            assert captured[-1] == estimate
        rows.append(row)
    return rows


def main():
    import argparse
    import os
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = args.output.resolve()
    if root.exists() or root.is_relative_to(Path.cwd().resolve()):
        parser.error('new outside-repository output required')
    os.umask(0o077)
    results = [assess(root/f'{pages}-{mode}', pages, mode) for pages in (4, 200)
               for mode in ('prose', 'escaped', 'claims', 'conflicts')]
    write(root/'results.json', results)
    print(json.dumps([dict(pages=r['pages'], mode=r['mode'], complete=r['complete'],
        failures=[x.get('failure') for x in r['records'] if x.get('failure')],
        questions=r['questions']) for r in results], indent=2))


if __name__ == '__main__':
    main()
