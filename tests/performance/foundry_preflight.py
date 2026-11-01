"""Zero-network L0 rehearsal. No live mode, credentials, or provider factory.

python -m tests.performance.foundry_preflight --stage L1 --output /tmp/new-l1
python -m tests.performance.foundry_preflight --stage L2 --output /tmp/new-l2
"""
import argparse
from hashlib import sha256
from io import BytesIO
import json
import os
from pathlib import Path
import socket
import time
from uuid import UUID

from tests.performance.fixtures import FACTS, NOW, pdf, profile
from tests.performance.foundry_budget import Contract, RunGuard
from tests.performance.foundry_recalibration import candidate_capability, candidate_policy
from tests.performance.phase17h import SyntheticModel, SyntheticVectors, write


class OfflineHTTP:
    """Deterministic transport fake; authored source labels are not model judgment."""
    def __init__(self):
        self.calls = []

    def post(self, url, **kwargs):
        sent = kwargs['json']
        if '\nCONTROL\n' not in sent['messages'][0]['content']:
            result = json.dumps(dict(answer='Offline fake abstention; not a model judgment.',
                                     evidence_status='insufficient', citation_ids=[]))
            return self.response(sent, result, 'question')
        control = json.loads(sent['messages'][0]['content'].split('\nCONTROL\n')[1])
        data = json.loads(sent['messages'][1]['content'])
        claims = []
        if control['kind'] == 'analysis':
            ordinary = []
            for piece in data['UNTRUSTED_DOCUMENT_DATA']:
                matched = [(page, text) for page, text in FACTS.items() if text in piece['text']]
                if not matched:
                    ordinary.append(piece['evidence_id'])
                for page, text in matched:
                    claim = dict(kind='fact', text=text, evidence_ids=[piece['evidence_id']])
                    if page in (5, 180):
                        claim.update(subject='orion-performance', stance='affirmed' if page == 5 else 'denied',
                                     qualifications=[dict(text='Only in 2025 and the specified load regime.',
                                                          evidence_ids=[piece['evidence_id']])])
                    claims.append(claim)
            if ordinary:
                claims.append(dict(kind='fact', text='Synthetic source observation; no semantic quality asserted.',
                                   evidence_ids=ordinary))
        else:
            claims.append(dict(kind='commentary', text='Inherited findings and qualifications apply.',
                               lineage=control['required_child_links']))
        for i, claim in enumerate(claims):
            claim.update(claim_id=control['claim_ids_in_order'][i], originating_stage=control['stage_id'])
        result = json.dumps(dict(stage_id=control['stage_id'], kind=control['kind'], claims=claims))
        if sent.get('response_format', {}).get('json_schema', {}).get('strict'):
            # Fake provider emits explicit defaults as the strict generation contract requires.
            from documents.digestion.models import StageResult
            result = StageResult.model_validate_json(result).model_dump_json()
        return self.response(sent, result, control['profile']['stage'])

    def response(self, sent, result, stage):
        self.calls.append(dict(stage=stage,
                               request_sha256=sha256(json.dumps(sent, sort_keys=True).encode()).hexdigest(),
                               response_sha256=sha256(result.encode()).hexdigest(), response=result))
        raw = json.dumps(dict(model='offline-model', choices=[dict(message=dict(content=result), finish_reason='stop')],
                              usage=dict(prompt_tokens=30, completion_tokens=40, total_tokens=70))).encode()

        class Response:
            status_code = 200
            headers = {}
            def iter_content(self, chunk_size):
                yield raw
            def close(self):
                pass
        return Response()


def synthetic_contract():
    from governance.ledger import Price, PricingCatalog
    return Contract(catalog=PricingCatalog(version='synthetic/1', currency='EUR', effective_date='2026-01-01',
        operator_approved=True, prices=(Price(provider='openai_compatible', model='offline-model',
        input_price='0.1', output_price='0.2', price_unit=1000000),)),
        provider='openai_compatible', model='offline-model', region='offline', tier='synthetic',
        price_source='TEST ARITHMETIC ONLY: not Azure prices', approved=True, currency='EUR',
        maximum='5', fixed_cost='0', extra_cost='0', context=28000)


def execute(root, stage, *, runtime=None):
    from documents.config import ExtractionSettings
    from documents.extraction import extract
    from documents.serialization import serialize
    from documents.storage import LocalObjectStore
    from documents.digestion.managed import (ManagedSettings, StageProfile, ManagedSynthesisInference,
                                             ManagedDigestionHandler, classify_managed)
    from documents.digestion.validation import EvidenceIndex
    from documents.digestion.workflow import prepare, admit, load_digest
    from documents.jobs.models import JobSettings, RetryPolicy
    from documents.jobs.sqlite import SQLiteJobLedger
    from documents.jobs.worker import LocalDispatcher, Worker, relay
    from governance.execution import GovernedExecution
    from governance.ledger import GovernanceLedger, Limits, QuotaPolicy
    from llm.admission import SQLiteInferenceAdmission
    from llm.openai_compatible import OpenAICompatibleProvider
    from security.authority import SecurityAuthority
    from security.models import Action, _verified_principal

    pages = {'L1': 4, 'L2': 200}[stage]
    if runtime is not None:
        if stage != 'L1':
            raise ValueError('Live composition supports L1 only')
        principal = operator = runtime.principal
        authority = runtime.authority
        scope = principal.scope
    else:
        # Test-only principal issuance; never usable as a live authentication path.
        principal = _verified_principal('offline', 'owner', 'fixture', expires=int(time.time())+3600)
        operator = _verified_principal('offline', 'operator', 'fixture', frozenset({Action.PUBLICATION_MANAGE}),
                                       expires=int(time.time())+3600)
        scope = principal.scope
        authority = SecurityAuthority(root/'security.sqlite')
        authority.register(principal)
        authority.register(operator)
    raw, manifest = pdf(pages)
    (root/'source.pdf').write_bytes(raw)
    write(root/'fixture.json', manifest)
    store = LocalObjectStore(root/'objects')
    artifact, ref = extract(BytesIO(raw), scope=scope, document_id=UUID(int=pages),
        display_filename='manual.pdf', declared_mime='application/pdf', store=store,
        limits=ExtractionSettings(), created_at=NOW, extracted_at=NOW)
    assert [u.text.splitlines() for u in artifact.units] == [x['lines'] for x in manifest['expected']]
    assert sha256(serialize(artifact)).hexdigest() == ref.sha256
    authority.register_document(operator, artifact.document)
    virtual = [time.time()]
    if runtime is not None:
        contract, guard, ledger, provider = runtime.contract, runtime.guard, runtime.ledger, runtime.provider
        http = None
    else:
        contract = synthetic_contract()
        # Advance only the quota clock offline: no real sleeping or quota evasion in live work.
        virtual = [time.time()]
        downstream = SQLiteInferenceAdmission(root/'admission.sqlite', 'offline', candidate_policy(), clock=lambda: virtual[0])
        guard = RunGuard(root/'run.sqlite', contract, downstream, clock=lambda: virtual[0])
        limits = Limits(requests_per_window=2, window_seconds=60, interactive_concurrent=1,
            background_concurrent=1, reserved_tokens=28000, daily_tokens=1400000,
            monthly_tokens=1400000, monthly_cost='5')
        ledger = GovernanceLedger(root/'governance.sqlite', QuotaPolicy(version='offline/1', owner=limits, tenant=limits),
                                   contract.catalog, clock=lambda: virtual[0])
        http = OfflineHTTP()
        provider = OpenAICompatibleProvider(base_url='https://offline.invalid/openai/v1',
            model_map={'summarization':'offline-model', 'general':'offline-model'},
            http_client=http, connect_timeout=5, read_timeout=60)
    prior_tickets = {r['ticket'] for r in ledger.usage(principal, authority)}
    provider_records = []
    bounded_execute = provider.execute
    def recorded_execute(request):
        started = time.perf_counter()
        record = dict(role=request.role.value, outcome='unknown', usage=None,
            request_sha256=sha256(json.dumps(dict(system=request.system, data=request.data,
                schema=request.schema, output=request.output_tokens), sort_keys=True).encode()).hexdigest())
        try:
            response = bounded_execute(request)
            usage = response.usage
            record.update(response=response.text, outcome='success', response_sha256=sha256(response.text.encode()).hexdigest(),
                usage=None if usage is None else dict(input=usage.prompt_tokens, output=usage.completion_tokens,
                                                     total=usage.total_tokens))
            return response
        except BaseException as exc:
            record['outcome'] = getattr(exc, 'category', 'unknown')
            from dataclasses import asdict
            from llm.inference import InferenceOutputLimitError
            if isinstance(exc, InferenceOutputLimitError):
                record['output_limit_diagnostics'] = asdict(exc.diagnostics)
            usage = getattr(exc, 'usage', None)
            if usage is not None:
                record['usage'] = dict(input=usage.prompt_tokens, output=usage.completion_tokens,
                                       total=usage.total_tokens)
            raise
        finally:
            record['duration_seconds'] = time.perf_counter()-started
            provider_records.append(record)
            write(root/'provider-calls.json', provider_records)
    provider.execute = recorded_execute
    cap = candidate_capability(strict_digestion=stage == 'L1')
    settings = ManagedSettings(capability=cap,
        generation_profile='managed-generation/2' if stage == 'L1' else 'managed-generation/1',
        max_response_envelope_bytes=26192 if stage == 'L1' else None, profiles=tuple(StageProfile(stage=s, input_tokens=24800,
        output_tokens=3000) for s in ('chunk', 'intermediate', 'structural', 'root')))
    governed = GovernedExecution(provider, guard, ledger, authority,
        authority.snapshot(principal, (artifact.document.document_id,), Action.DOCUMENT_DELETE))
    inference = ManagedSynthesisInference(provider, settings, guard, governance=governed)
    # Explicit candidate sizing; evidence coverage/claims/lineage are unchanged.
    # L1 byte allowances are independent of completion-token reservations.
    chosen = inference.profile(profile(context_tokens=28000, reserved_output_tokens=3000,
                                       max_result_characters=10000 if stage == 'L1' else 3000,
                                       max_response_bytes=10000 if stage == 'L1' else None))
    plan, plan_ref = prepare(artifact, ref, chosen, store)
    index = EvidenceIndex(artifact)
    pieces = [p for c in plan.chunks for p in c.pieces]
    assert ''.join(p.text for p in pieces) == ''.join(u.text for u in artifact.units)
    assert all(index.resolve(p.evidence) == p.text for p in pieces)
    calls = len(plan.chunks)+len(plan.reducers)
    jobs = SQLiteJobLedger(JobSettings(database_path=root/'jobs.sqlite', lease_seconds=120))
    job = admit(jobs, store, plan, plan_ref, request_key='offline-preflight', retry=RetryPolicy(max_attempts=1))
    handler = ManagedDigestionHandler(jobs, plan_ref, inference)
    queue = LocalDispatcher()
    worker = Worker(jobs, queue, store, handler, owner='offline', classifier=classify_managed)
    durations = []
    for _ in range(chosen.max_steps+1):
        if runtime is not None:
            runtime.wait()
        else:
            virtual[0] += 61
        relay(jobs, queue)
        start = time.perf_counter()
        before = len(provider_records)
        if not worker.once():
            break
        if len(provider_records) > before:
            durations.append(time.perf_counter()-start)
        state = jobs.get_job(scope, job.job_id).state
        if state in ('FAILED', 'CANCELLED', 'PARTIAL'):
            guard.stop('evidence')
            break
    state = jobs.get_job(scope, job.job_id)
    planned_calls = calls + (1 if stage == 'L1' else 12)
    summary = dict(stage=stage, pages=pages, mode='OFFLINE ONLY' if runtime is None else 'LIVE L1', model=contract.model,
        chunks=len(plan.chunks), reducers=len(plan.reducers), planned_digestion_calls=calls,
        planned_calls=planned_calls, reserved_input=planned_calls*25000, reserved_output=planned_calls*3000,
        planning_max_input=max([c.estimated_tokens for c in plan.chunks]+[n.estimated_tokens for n in plan.reducers]),
        job_state=state.state, terminal_category=state.terminal_category,
        calls=len(provider_records), billable_calls=0 if runtime is None else len(provider_records), human_reviewer_coverage=0,
        planning_context=chosen.context_tokens, managed_context=cap.context_tokens,
        accounting_contract=contract.model_dump(mode='json'),
        live_status='NOT AUTHORIZED' if runtime is None else 'APPROVED CONFIGURATION BOUND')
    if state.state == 'COMPLETED':
        digest = load_digest(jobs, store, scope, job.job_id)
        assert digest.status == 'COMPLETE' and digest.coverage.fraction == 1
        summary.update(digest_status=digest.status, source_evidence=len(digest.evidence),
                       qualifications=len(digest.qualifications), contradictions=len(digest.contradictions))
        summary['publication'], replica = publish(root, jobs, store, job, scope, authority, operator, principal, runtime=runtime)
        summary['quality'] = evaluate_fixture(digest, artifact, pages) if runtime is None else {'status':'HUMAN_REVIEW_PENDING'}
        summary['questions'] = questions(root, stage, artifact, manifest, replica, provider, candidate_capability(),
                                         governed, guard, virtual, authority, principal, runtime=runtime)
    summary['calls'] = len(provider_records)
    summary['run_records'] = guard.records()
    summary['governance_records'] = [r for r in ledger.usage(principal, authority) if r['ticket'] not in prior_tickets]
    for record, expense in zip(provider_records, summary['governance_records']):
        record.update(governance_ticket=expense['ticket'], identity=json.loads(expense['identity']),
                      measured_cost=expense['actual_cost'], reserved_cost=expense['cost'],
                      settlement_state=expense['state'], currency=contract.currency)
    summary['provider_records'] = provider_records
    summary['call_durations_seconds'] = durations
    write(root/'responses.json', http.calls if http is not None else provider_records)
    write(root/'result.json', summary)
    return summary


def publish(root, jobs, store, job, scope, authority, operator, principal, *, runtime=None):
    from documents.publication.authority import SQLitePublicationAuthority
    from documents.publication.encoding import RetrievalEncoder
    from documents.publication.models import RetrievalProfile
    from documents.publication.service import PublicationService
    from documents.publication.retrieval import PublicationReplica
    from security.services import AuthorizedPublication
    service = PublicationService(SQLitePublicationAuthority(root/'publication.sqlite'), store, jobs,
        SyntheticVectors() if runtime is None else runtime.vectors,
        RetrievalEncoder(RetrievalProfile(), SyntheticModel()) if runtime is None else runtime.encoder, scope)
    authorized = AuthorizedPublication(authority, service)
    manifest = authorized.run(operator, 'plan', [job.job_id])
    authorized.run(operator, 'prepare', manifest.generation)
    authorized.run(operator, 'activate', manifest.generation)
    replica = PublicationReplica(service, manifest.generation)
    replica.load()
    assert replica.ready()
    snapshot = authority.snapshot(principal, (job.admission.document_id,))
    pin = replica.pin((job.admission.document_id,), authorization=(authority, snapshot))
    hits = replica.retrieve('Unit 0001', pin, top_k=8, reranker=lambda q, docs, top_k: docs[:top_k])
    citations = replica.citations(pin, hits)
    assert citations and all(c.document_id == job.admission.document_id for c in citations)
    return (dict(records=len(manifest.records), citations=len(citations), embedding='constant fake' if runtime is None else 'local pinned embedding',
                 retrieval='semantic ranking unvalidated; deterministic reranker'), replica)


def questions(root, stage, artifact, manifest, replica, provider, cap, governed, guard, virtual, authority, principal, *, runtime=None):
    from documents.publication.analysis import DocumentAnalysis, AnalysisRequest
    from security.models import Action
    from governance.execution import GovernedExecution
    dataset_path = Path('tests/fixtures/phase17h/quality.json')
    dataset = json.loads(dataset_path.read_text())
    cases = dataset['cases'] if stage == 'L2' else [dict(case_id='smoke-page1',
        question='What is the first inspection procedure on physical page 1?', required_pages=[1],
        required_findings=[manifest['expected'][0]['lines'][1]], insufficient_evidence=False)]
    snapshot = authority.snapshot(principal, (artifact.document.document_id,), Action.DOCUMENT_ANALYZE)
    executor = GovernedExecution(provider, guard, governed.ledger, authority, snapshot)
    analysis = DocumentAnalysis(replica, provider, cap, input_bytes=24800, output_tokens=3000,
                                reranker=lambda q, docs, top_k: docs[:top_k])
    packets = []
    status = 'COMPLETE'
    for case in cases:
        if runtime is not None:
            runtime.wait()
        else:
            virtual[0] += 61
        packet = dict(case=case, rubric=dataset['rubric_version'], dataset_sha256=sha256(dataset_path.read_bytes()).hexdigest(),
            selected_documents=[str(artifact.document.document_id)],
            selected_versions=[str(artifact.document.document_version_id)],
            expected_findings=case['required_findings'], extracted_factual_claims=None,
            independent_reviewer=None, reviewer_judgment=None, unsupported_conclusions=None,
            qualifications_and_contradictions=None, abstention_decision=None, disagreement=None,
            judgment_status='PENDING; independent human review required')
        start = time.perf_counter()
        try:
            answer = analysis.analyze(AnalysisRequest(query=case['question'],
                document_ids=(artifact.document.document_id,)), authorization=(authority, snapshot), executor=executor)
            authority.revalidate(snapshot)
            packet.update(response=answer, response_sha256=sha256(json.dumps(answer, sort_keys=True).encode()).hexdigest(),
                          actual_citations=answer['citations'])
        except Exception as exc:
            guard.stop('capability')
            packet['failure'] = getattr(exc, 'category', type(exc).__name__)
            status = 'BLOCKED'
        packet['duration_seconds'] = time.perf_counter()-start
        packets.append(packet)
        if status == 'BLOCKED':
            break
    write(root/'review-packets.json', packets)
    return dict(status=status, planned=len(cases), recorded=len(packets), human_reviewed=0)


def evaluate_fixture(digest, artifact, pages):
    from documents.digestion.models import SourcePiece
    from documents.digestion.validation import EvidenceIndex
    from tests.performance.quality import ClaimJudgment, Observation, evaluate, structural_validity
    index = EvidenceIndex(artifact)
    refs = {SourcePiece(evidence=e, text='', kind='text').evidence_id():e for e in digest.evidence}
    observations = []
    for page, text in FACTS.items():
        if page > pages:
            continue
        finding = next(f for f in digest.findings if f.text == text)
        cited = [refs[e] for e in finding.evidence_ids]
        valid = tuple(structural_validity(artifact, e, page=page, excerpt=index.resolve(e), authorized=True) for e in cited)
        support = bool(cited) and all(valid) and any(text in index.resolve(e) for e in cited)
        observations.append(Observation(str(page), valid, (ClaimJudgment(str(finding.claim_id), support, True,
            ('fact',) if support else ()),), ('fact',), False, False, page in (5, 180),
            bool(finding.qualifications) and bool(digest.contradictions), 'authored synthetic oracle'))
    return evaluate(observations)


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--stage', choices=('L1', 'L2'), required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = args.output.resolve()
    if root.exists() or root.is_relative_to(Path.cwd().resolve()):
        parser.error('choose a new outside-repository output directory')
    os.umask(0o077)
    root.mkdir(parents=True, mode=0o700)
    original = socket.socket.connect
    def denied(*args, **kwargs):
        raise RuntimeError('Network forbidden in L0')
    socket.socket.connect = denied
    try:
        result = execute(root, args.stage)
    finally:
        socket.socket.connect = original
    print(json.dumps({k:result[k] for k in ('stage', 'job_state', 'planned_calls', 'calls', 'billable_calls')}))
    if result['job_state'] != 'COMPLETED' or result.get('questions', {}).get('status') != 'COMPLETE':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
