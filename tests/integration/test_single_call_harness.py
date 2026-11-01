"""Real composition, synthetic Entra/RSA fixtures, isolated authorities, no network."""
from dataclasses import replace
from decimal import Decimal
from hashlib import sha256
import json
import socket
import time
from uuid import uuid4

import pytest
import requests

from tests.approval_helpers import approval_signer
from tests.unit.test_security_identity import identity
from tests.unit.test_security_entra import entra
from tests.unit.test_foundry_schema_probe import catalog, previous
from tests.unit.test_structured_provider import Response
from tests.performance import foundry_single_call as harness
from tests.performance.foundry_preflight import OfflineHTTP
from tests.performance.foundry_recalibration import RESOURCE, DEPLOYMENT, candidate_policy
from tests.performance.foundry_approval import verify_artifact, bindings
from governance.ledger import EvaluationBinding, GovernanceLedger, GovernanceError, Limits, QuotaPolicy
from llm.admission import SQLiteInferenceAdmission, CallIdentity
from llm.inference import InferenceUsage
from security.authority import SecurityAuthority
from security.models import SecurityError


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    def deny(*a, **kw):
        raise AssertionError('External network forbidden')
    for name in ('connect', 'connect_ex', 'sendto'):
        monkeypatch.setattr(socket.socket, name, deny)
    for name in ('create_connection', 'getaddrinfo', 'gethostbyname'):
        monkeypatch.setattr(socket, name, deny)


@pytest.fixture
def rig(tmp_path, entra, approval_signer, monkeypatch):
    verifier, token, _, _ = entra
    access = token()
    principal = verifier.verify(access)
    root = tmp_path / 'audit'
    root.mkdir(mode=0o700)
    policy = candidate_policy()
    binding = EvaluationBinding(version='polymind-evaluation/1', scopes=(principal.scope,),
        governance_path=str(tmp_path/'governance.sqlite'), provider_path=str(tmp_path/'admission.sqlite'),
        provider_key=DEPLOYMENT, provider_policy_sha256=sha256(policy.model_dump_json().encode()).hexdigest())
    limits = Limits(requests_per_window=16, window_seconds=86400, interactive_concurrent=1,
        background_concurrent=1, reserved_tokens=112000, daily_tokens=500000, monthly_tokens=1500000, monthly_cost='5')
    gp = QuotaPolicy(version='synthetic/1', owner=limits, tenant=limits, evaluation=binding)
    prepared = harness.prepare_analysis(tmp_path/'preparation', principal.scope)
    config = harness.SingleCallConfiguration(executor_sha256=harness.executor_digest(),
        generation_contract_sha256=harness.generation_contract_digest(), resource=RESOURCE, deployment=DEPLOYMENT,
        model='gpt-5.4-mini', model_version='2026-03-17', sku='GlobalStandard',
        endpoint=f'https://{RESOURCE}.openai.azure.com/openai/v1', authentication='api_key',
        owner_scope=principal.scope.identity(), oidc=verifier.config, security_path=tmp_path/'security.sqlite',
        governance_path=binding.governance_path, admission_path=binding.provider_path, quota_key=DEPLOYMENT,
        policy=policy, governance_policy=gp, contract=harness.one_call_contract(previous(), catalog()),
        audit_directory=root, job_id=uuid4(), request_id=uuid4(), rendered_request_sha256=prepared[-1],
        fixture_sha256=prepared[-2], credential_valid_until=int(time.time())+3600,
        approval_expires=int(time.time())+3600, execution_not_before=int(time.time())-1,
        credential_audience_verified=True, quota_verified=True, shared_consumers_verified=True,
        charges_verified=True, actual_azure_rpm=2, actual_azure_tpm=30000)
    authority = SecurityAuthority(config.security_path)
    authority.register(principal)
    ledger = GovernanceLedger(config.governance_path, gp, config.contract.catalog,
        provider_path=config.admission_path, provider_key=DEPLOYMENT, provider_policy=policy)
    admission = SQLiteInferenceAdmission(config.admission_path, DEPLOYMENT, policy)
    class HTTP(OfflineHTTP):
        def __init__(self):
            super().__init__()
            self.sent = []
            self.transform = lambda x: x
            self.error = None
            self.status = 200
            self.closed = False
        def post(self, url, **kwargs):
            self.sent.append((url, kwargs))
            if self.error:
                raise self.error
            response = super().post(url, **kwargs)
            value = json.loads(b''.join(response.iter_content(1)))
            value['model'] = 'gpt-5.4-mini-2026-03-17'
            return Response(self.transform(value), status=self.status)
        def close(self): self.closed = True
    http = HTTP()
    monkeypatch.setattr(harness, 'OIDCVerifier', lambda config: verifier)
    monkeypatch.setattr(harness, 'no_retry_session', lambda: http)
    def approve(cfg=config, **kwargs):
        return approval_signer(cfg, principal, changes={'aud':'polymind-single-analysis-live', **kwargs})
    artifact, trust = approve()
    def run(cfg=config, approval=artifact, trust_value=trust, access_value=access):
        return harness.launch(cfg, harness.configuration_digest(cfg), access_value, 'SYNTHETIC', approval, trust_value)
    return config, run, http, ledger, authority, principal, approve, artifact, trust, prepared


def test_exact_one_call_and_accounting(rig):
    cfg, run, http, ledger, authority, p, *_ = rig
    result = run()
    assert result['state'] == 'SUCCEEDED'
    assert result['provider_acceptance'] == 'completed_strict_response'
    assert result['application_validation'] == 'accepted'
    assert len(http.sent) == result['calls'] == 1
    url, kw = http.sent[0]
    assert url == cfg.endpoint + '/chat/completions'
    assert kw['allow_redirects'] is False
    payload = kw['json']
    assert payload['model'] == DEPLOYMENT and payload['max_completion_tokens'] == 3000
    assert payload['response_format'] == dict(type='json_schema', json_schema=dict(
        name='polymind_stage_result', strict=True, schema=harness.provider_schema(harness.generation_schema())))
    assert http.calls[0]['stage'] == 'chunk'
    assert cfg.contract.cost(1) == Decimal('0.028379091869065')
    row = ledger.usage(p, authority)[0]
    assert row['state'] == 'SETTLED' and row['policy'] == 'polymind-evaluation/1'
    expected = cfg.contract.catalog.price('openai_compatible', DEPLOYMENT).cost(30, 40)
    assert Decimal(row['actual_cost']) == expected
    ledger.settle(row['ticket'], InferenceUsage(30, 40, 70))
    assert json.loads((cfg.audit_directory/'outcome.json').read_text()) == result
    assert http.closed
    with pytest.raises(SecurityError): run()
    assert len(http.sent) == 1


@pytest.mark.parametrize('case', ['extras', 'uuid', 'evidence', 'lineage', 'claim', 'qualification',
                                 'contradiction', 'origin', 'order', 'canonical'])
def test_application_rejection_settles_without_repair(rig, case):
    cfg, run, http, ledger, authority, p, *_ = rig
    def corrupt(value):
        data = json.loads(value['choices'][0]['message']['content'])
        claim = data['claims'][0]
        unknown = str(uuid4())
        if case == 'extras': data.update({f'unused{i}': None for i in range(1, 9)})
        elif case == 'uuid': claim['evidence_ids'] = ['malformed']
        elif case == 'evidence': claim['evidence_ids'] = [unknown]
        elif case == 'lineage': claim['lineage'] = [dict(stage_id=unknown, claim_id=unknown)]
        elif case == 'claim': claim['claim_id'] = unknown
        elif case == 'qualification': claim['qualifications'] = [dict(text='Synthetic', evidence_ids=[])]
        elif case == 'contradiction': claim['contradicting_evidence_ids'] = [unknown]
        elif case == 'origin': claim['originating_stage'] = unknown
        elif case == 'order':
            # Duplicate claim identity violates order even for one synthetic claim.
            data['claims'].append(dict(claim))
        elif case == 'canonical': claim['text'] = '\u0800' * 1600
        value['choices'][0]['message']['content'] = json.dumps(data, ensure_ascii=False)
        return value
    http.transform = corrupt
    result = run()
    assert result['state'] == 'FAILED' and result['application_validation'] == 'failed'
    assert result['provider_acceptance'] == 'completed_strict_response'
    assert len(http.sent) == 1
    assert ledger.usage(p, authority)[0]['state'] == 'SETTLED'
    assert json.loads((cfg.audit_directory/'outcome.json').read_text()) == result


@pytest.mark.parametrize('case,category,known', [
    ('400', 'inference_configuration', False), ('422', 'inference_configuration', False),
    ('timeout', 'inference_timeout', False), ('transport', 'inference_unavailable', False),
    ('401', 'inference_authentication', False), ('429', 'inference_rate_limited', False),
    ('truncated', 'inference_output_limit', True), ('malformed', 'inference_invalid_response', True),
    ('unknown', 'governance_denied', False), ('inconsistent', 'inference_invalid_response', False),
    ('interrupted', 'worker_failed', False),
])
def test_provider_errors_no_retry_primary_retained(rig, case, category, known):
    cfg, run, http, ledger, authority, p, *_ = rig
    if case in ('400', '422', '401', '429'):
        http.status = int(case)
        http.transform = lambda v: {'error': {'code':'invalid_json_schema', 'param':'response_format',
                                             'message':'PRIVATE TOKEN DOCUMENT'}}
    elif case == 'timeout': http.error = requests.Timeout('PRIVATE')
    elif case == 'transport': http.error = requests.ConnectionError('PRIVATE')
    elif case == 'interrupted': http.error = KeyboardInterrupt()
    else:
        def transform(v):
            if case == 'truncated': v['choices'][0]['finish_reason'] = 'length'
            elif case == 'malformed': v['choices'] = []
            elif case == 'unknown': v.pop('usage')
            else: v['usage']['total_tokens'] = 0
            return v
        http.transform = transform
    result = run()
    assert result['state'] == 'FAILED'
    assert result['failure'] == category
    assert len(http.sent) == 1
    assert ledger.usage(p, authority)[0]['state'] == ('SETTLED' if known else 'UNKNOWN')
    assert 'PRIVATE' not in json.dumps(result)
    if case in ('400', '422'):
        assert result['rejection']['reason'] == 'strict_schema_rejected'
    with pytest.raises(SecurityError): run()
    assert len(http.sent) == 1


@pytest.mark.parametrize('case', ['missing', 'signature', 'expired', 'operator', 'generation', 'executor', 'legacy', 'scope'])
def test_security_fails_before_reservation(rig, case):
    cfg, run, http, ledger, authority, p, approve, artifact, trust, _ = rig
    kwargs = {}
    if case == 'missing': kwargs['approval'] = None
    elif case == 'signature': kwargs['approval'] = artifact[:-12] + 'INVALIDxxxxx'
    elif case == 'expired': kwargs['approval'] = approve(exp=1)[0]
    elif case == 'operator': kwargs['trust_value'] = trust.model_copy(update={'operator_subject':'other'})
    elif case == 'legacy': kwargs['approval'] = approve(aud='polymind-l1-live')[0]
    elif case == 'scope': kwargs['cfg'] = cfg.model_copy(update={'owner_scope':'other'})
    else: kwargs['cfg'] = cfg.model_copy(update={case+'_sha256' if case == 'executor' else 'generation_contract_sha256':'0'*64})
    with pytest.raises(Exception): run(**kwargs)
    assert not http.sent and not ledger.usage(p, authority)
    assert not list(trust.replay_directory.iterdir())


def test_consumed_approval_cannot_authorize_another_directory(rig):
    cfg, run, http, ledger, authority, p, approve, artifact, trust, _ = rig
    run()
    from tests.performance.foundry_approval import consume
    claims = verify_artifact(artifact, trust, cfg, p, harness.configuration_digest(cfg))
    with pytest.raises(SecurityError): consume(claims, trust, artifact)
    assert len(http.sent) == 1


def test_guard_second_call_and_restart_impossible(rig):
    cfg, run, http, ledger, authority, p, *_ = rig
    run()
    downstream = SQLiteInferenceAdmission(cfg.admission_path, cfg.quota_key, cfg.policy)
    guard = harness.RunGuard(cfg.audit_directory/'run.sqlite', cfg.contract, downstream)
    identity = CallIdentity(p.scope.identity(), uuid4(), uuid4(), 1, cfg.executor,
                            'openai_compatible', 'summarization', DEPLOYMENT, 'gpt54mini-30k/2')
    with pytest.raises(GovernanceError): guard.acquire(identity, 100, 3000)
    assert len(guard.records()) == 1 and len(http.sent) == 1


@pytest.mark.parametrize('case', ['four', 'window', 'schema', 'price', 'request'])
def test_contract_substitution(rig, case):
    cfg, run, http, ledger, authority, p, *_ = rig
    values = cfg.model_dump()
    if case == 'four': values['contract'].update(attempts=4, total_input=100000, total_output=12000)
    elif case == 'window': values['approval_expires'] = None
    elif case == 'schema': values['provider_schema_sha256'] = '0'*64
    elif case == 'price': values['contract']['catalog']['version'] = 'wrong'
    else: values['rendered_request_sha256'] = '0'*64
    with pytest.raises(Exception): run(cfg=harness.SingleCallConfiguration.model_validate(values))
    assert not http.sent and not ledger.usage(p, authority)


@pytest.mark.parametrize('provider_error', [True, False])
def test_settlement_failure_preserves_primary(rig, monkeypatch, provider_error):
    cfg, run, http, ledger, authority, p, *_ = rig
    if provider_error: http.error = requests.Timeout()
    def fail(*args): raise GovernanceError()
    monkeypatch.setattr(GovernanceLedger, 'settle', fail)
    result = run()
    assert result['failure'] == ('inference_timeout' if provider_error else 'governance_denied')
    assert ledger.usage(p, authority)[0]['state'] == 'STARTED'
    assert len(http.sent) == 1


def test_approval_binding_explicit_and_legacy_incompatible(rig):
    cfg, _, _, _, _, p, _, artifact, trust, _ = rig
    binding = bindings(cfg, p, harness.configuration_digest(cfg))
    assert binding['execution']['executor'] == 'polymind-single-analysis/1'
    assert binding['execution']['sha256'] == cfg.executor_sha256
    verify_artifact(artifact, trust, cfg, p, harness.configuration_digest(cfg))
    wrong = cfg.model_copy(update={'executor_sha256':'0'*64})
    with pytest.raises(SecurityError): verify_artifact(artifact, trust, wrong, p, harness.configuration_digest(wrong))


def test_cli_failure_nonzero_after_durable_outcome(rig, monkeypatch, capsys):
    cfg, run, http, *_ = rig
    http.error = requests.Timeout()
    result = run()
    path = cfg.audit_directory/'configuration.json'
    harness.durable_json(path, cfg.model_dump(mode='json'))
    monkeypatch.setattr(harness, 'launch', lambda *a, **kw: result)
    monkeypatch.setattr(harness, 'load_trust', lambda p: None)
    import sys
    monkeypatch.setattr(sys, 'argv', ['single', '--live', '--configuration', str(path),
        '--approval', str(path), '--approval-trust', str(path), '--approve-sha256', harness.configuration_digest(cfg)])
    assert harness.main() == 1
    assert (cfg.audit_directory/'outcome.json').exists()


def test_http_session_no_retries(monkeypatch):
    # Exercise actual requests adapter construction, no network.
    session = harness.no_retry_session()
    try:
        assert session.trust_env is False
        assert session.get_adapter('https://').max_retries.total == 0
    finally: session.close()


def test_capacity_denial_no_provider_or_new_reservation(rig):
    cfg, run, http, ledger, authority, p, *_ = rig
    identity = CallIdentity(p.scope.identity(), uuid4(), uuid4(), 1, cfg.executor,
        'openai_compatible', 'summarization', DEPLOYMENT, 'gpt54mini-30k/2')
    ledger.reserve(p, identity, 25000, 3000, 'DOCUMENT_BACKGROUND')
    before = ledger.usage(p, authority)
    result = run()
    assert result['state'] == 'FAILED' and result['failure'] == 'governance_denied'
    assert not http.sent and ledger.usage(p, authority) == before


def test_audit_collection_failure_preserves_primary(rig, monkeypatch):
    cfg, run, http, ledger, authority, p, *_ = rig
    http.error = requests.Timeout()
    def fail(*args, **kwargs): raise GovernanceError()
    monkeypatch.setattr(GovernanceLedger, 'usage', fail)
    result = run()
    assert result['failure'] == 'inference_timeout' and result['accounting_failed']
    assert json.loads((cfg.audit_directory/'outcome.json').read_text()) == result


def test_offline_configuration_requires_new_attestations(rig, monkeypatch, capsys):
    cfg, run, http, *_ = rig
    fields = ['credential_valid_until', 'approval_expires', 'execution_not_before',
        'credential_audience_verified', 'quota_verified', 'shared_consumers_verified',
        'charges_verified', 'actual_azure_rpm', 'actual_azure_tpm']
    prepared = harness.SingleCallConfiguration.model_validate({**cfg.model_dump(), **dict.fromkeys(fields)})
    path = cfg.audit_directory/'prepared.json'
    harness.durable_json(path, prepared.model_dump(mode='json'))
    with pytest.raises(SecurityError): prepared.require_live_window()
    import sys
    monkeypatch.setattr(sys, 'argv', ['single', '--configuration', str(path)])
    assert harness.main() == 0 and not http.sent
    attestations = cfg.audit_directory/'attestations.json'
    harness.durable_json(attestations, {k:getattr(cfg, k) for k in fields})
    final = cfg.audit_directory/'final.json'
    monkeypatch.setattr(sys, 'argv', ['single', '--configuration', str(path), '--attestations', str(attestations),
                                    '--output', str(final)])
    assert harness.main() == 0 and not http.sent
    finalized = harness.SingleCallConfiguration.model_validate_json(final.read_bytes())
    assert harness.configuration_digest(finalized) != harness.configuration_digest(prepared)
    assert finalized == cfg
    assert not list(rig[8].replay_directory.iterdir())


def test_forbidden_workflows_are_unreachable(rig, monkeypatch):
    from tests.performance import foundry_l1, foundry_preflight
    def forbidden(*a, **kw): raise AssertionError('Forbidden downstream workflow')
    for module, names in ((foundry_l1, ('launch', 'local_retrieval')),
                           (foundry_preflight, ('execute', 'publish', 'questions'))):
        for name in names: monkeypatch.setattr(module, name, forbidden)
    result = rig[1]()
    assert result['state'] == 'SUCCEEDED' and len(rig[2].sent) == 1
