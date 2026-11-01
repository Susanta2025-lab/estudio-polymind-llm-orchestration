"""Synthetic authorities only. Socket access is forbidden for every test."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import json
import socket

import pytest

from governance.evaluation import evaluation_policy, prepare_evaluation_migration
from governance.ledger import EvaluationBinding, GovernanceLedger, GovernanceError, Limits, QuotaPolicy, Price, PricingCatalog
from governance.migration import history_digest
from llm.admission import AdmissionPolicy
from llm.inference import InferenceUsage
from security.models import SecurityError, _verified_principal
from tests.unit.test_governance import identity


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError('Network forbidden')
    monkeypatch.setattr(socket.socket, 'connect', forbidden)
    monkeypatch.setattr(socket.socket, 'connect_ex', forbidden)
    monkeypatch.setattr(socket, 'getaddrinfo', forbidden)


@pytest.fixture
def state(tmp_path):
    now = [datetime(2026, 10, 16, 12, tzinfo=timezone.utc).timestamp()]
    principal = _verified_principal('issuer', 'evaluation', 'development', expires=2100000000)
    prod = _verified_principal('issuer', 'production', 'production', expires=2100000000)
    peer = _verified_principal('issuer', 'unapproved', 'development', expires=2100000000)
    limits = Limits(requests_per_window=5, window_seconds=86400, interactive_concurrent=1,
                    background_concurrent=1, reserved_tokens=112000, daily_tokens=115305,
                    monthly_tokens=115305, monthly_cost='5.00')
    old = QuotaPolicy(version='phase17hl-l1/2', owner=limits, tenant=limits)
    catalog = PricingCatalog(version='synthetic/1', currency='EUR', effective_date='2026-01-01',
        operator_approved=True, prices=(Price(provider='fake', model='model', input_price='1', output_price='1', price_unit=1000000),))
    admission = AdmissionPolicy(rpm=2, tpm=30000, concurrent=2, interactive_rpm=1,
                                interactive_tpm=2000, interactive_slots=1, per_job_rpm=1)
    binding = EvaluationBinding(version='polymind-evaluation/1', scopes=(principal.scope,),
        governance_path=str(tmp_path/'gov.sqlite'), provider_path=str(tmp_path/'provider.sqlite'),
        provider_key='shared', provider_policy_sha256=sha256(admission.model_dump_json().encode()).hexdigest())
    kwargs = dict(clock=lambda: now[0], provider_path=binding.provider_path,
                  provider_key=binding.provider_key, provider_policy=admission)
    policy = evaluation_policy(old, binding)
    ledger = GovernanceLedger(binding.governance_path, policy, catalog, **kwargs)
    return ledger, principal, prod, peer, now, old, binding, kwargs


def settled(ledger, principal, n=28000, usage=True):
    ticket = ledger.reserve(principal, identity(principal), n-1, 1)
    ledger.transition(ticket, 'RESERVED', 'ADMITTING')
    ledger.transition(ticket, 'ADMITTING', 'STARTED')
    ledger.settle(ticket, InferenceUsage(n-1, 1, n) if usage else None)
    return ticket


def test_selection_and_legacy_serialization(state):
    ledger, p, prod, peer, _, old, *_ = state
    assert 'evaluation' not in json.loads(old.model_dump_json())
    assert ledger.policy.select(p.scope)[0] == 'polymind-evaluation/1'
    assert ledger.policy.select(prod.scope) == (old.version, old.owner, old.tenant)
    assert ledger.policy.select(peer.scope) == (old.version, old.owner, old.tenant)
    assert QuotaPolicy.model_validate_json(ledger.policy.model_dump_json()) == ledger.policy
    for _ in range(5): settled(ledger, prod, 2)
    with pytest.raises(GovernanceError): settled(ledger, prod, 2)
    assert settled(ledger, p)


def test_four_experiments_rolling_window_no_reset(state):
    ledger, p, _, _, now, *_ = state
    for experiment in range(4):
        for call in range(4): settled(ledger, p)
    with pytest.raises(GovernanceError): settled(ledger, p, 2)
    now[0] += 86399
    with pytest.raises(GovernanceError): settled(ledger, p, 2)
    now[0] += 1
    assert settled(ledger, p)
    with ledger.transaction() as db:
        assert db.execute('SELECT COUNT(*) FROM reservations').fetchone()[0] == 17
        assert {r[0] for r in db.execute('SELECT policy FROM reservations')} == {'polymind-evaluation/1'}


def test_daily_token_exhaustion(state):
    ledger, p, *_ = state
    for _ in range(5): settled(ledger, p, 100000)
    with pytest.raises(GovernanceError): settled(ledger, p, 2)


def test_monthly_tokens_across_days(state):
    ledger, p, _, _, now, *_ = state
    for _ in range(3):
        for _ in range(5): settled(ledger, p, 100000)
        now[0] += 86400
    with pytest.raises(GovernanceError): settled(ledger, p, 2)


def test_financial_ceiling_despite_available_tokens(state, tmp_path):
    ledger, p, _, _, _, _, binding, kwargs = state
    expensive = ledger.catalog.model_copy(update={'prices': (Price(provider='fake', model='model', input_price='1', output_price='1', price_unit=1),)})
    # A separate synthetic authority has its own explicit test-only binding.
    binding = binding.model_copy(update={'governance_path':str(tmp_path/'expensive.sqlite')})
    policy = ledger.policy.model_copy(update={'evaluation':binding})
    expensive_ledger = GovernanceLedger(binding.governance_path, policy, expensive, **kwargs)
    settled(expensive_ledger, p, 5)
    with pytest.raises(GovernanceError): settled(expensive_ledger, p, 2)


@pytest.mark.parametrize('unknown', [False, True])
def test_unresolved_carries_across_months(state, unknown):
    ledger, p, _, _, now, *_ = state
    if unknown: settled(ledger, p, 112000, usage=False)
    else: ledger.reserve(p, identity(p), 111999, 1)
    now[0] += 40*86400
    with pytest.raises(GovernanceError): ledger.reserve(p, identity(p), 1, 1)


def test_atomic_concurrent_reservations(state):
    ledger, p, *_ = state
    def reserve(_):
        try: return ledger.reserve(p, identity(p), 25000, 3000)
        except GovernanceError: return None
    with ThreadPoolExecutor(2) as pool:
        assert sum(x is not None for x in pool.map(reserve, range(2))) == 1


@pytest.mark.parametrize('change', ['path', 'provider_path', 'provider_key', 'provider_policy', 'scope', 'version'])
def test_substitution_denied(state, tmp_path, change):
    ledger, p, _, peer, _, old, binding, kwargs = state
    path, policy = ledger.path, ledger.policy
    kwargs = dict(kwargs)
    if change == 'path': path = tmp_path/'bypass.sqlite'
    elif change == 'provider_path': kwargs['provider_path'] = str(tmp_path/'bypass.sqlite')
    elif change == 'provider_key': kwargs['provider_key'] = 'bypass'
    elif change == 'provider_policy': kwargs['provider_policy'] = kwargs['provider_policy'].model_copy(update={'tpm':60000})
    elif change == 'scope': policy = evaluation_policy(old, binding.model_copy(update={'scopes':(peer.scope,)}))
    else:
        data = binding.model_dump(); data['version'] = 'polymind-evaluation/2'
        with pytest.raises(ValueError): EvaluationBinding.model_validate(data)
        return
    with pytest.raises(SecurityError): GovernanceLedger(path, policy, ledger.catalog, **kwargs)


def test_forged_scope_and_shared_tenant_cost(state):
    ledger, p, _, peer, *_ = state
    with pytest.raises(GovernanceError): ledger.reserve(peer, identity(p), 1, 1)
    for _ in range(5): settled(ledger, p, 28000)
    # Existing evaluation spending counts against the unapproved owner's base tenant limit.
    with pytest.raises(GovernanceError): ledger.reserve(peer, identity(peer), 1, 1)


def test_migration_readonly_history_rollback_and_impact(state, tmp_path):
    ledger, p, _, _, now, old, binding, kwargs = state
    legacy_path = tmp_path/'legacy.sqlite'
    legacy = GovernanceLedger(legacy_path, old, ledger.catalog, clock=lambda:now[0])
    settled(legacy, p, 3305)
    binding = binding.model_copy(update={'governance_path':str(legacy_path)})
    before_bytes = legacy_path.read_bytes()
    with legacy.transaction() as db: before = history_digest(db)
    result = prepare_evaluation_migration(legacy_path, old, ledger.catalog, binding,
                                        provider_policy=kwargs['provider_policy'], now=now[0])
    assert result['dry_run'] == result['rollback'] == 'PASS'
    assert result['history_sha256'] == before
    assert result['quotas'][p.scope.identity()]['owner']['after']['monthly_tokens_remaining'] == 1496695
    assert result['quotas'][p.scope.identity()]['owner']['after']['requests_remaining'] == 15
    assert legacy_path.read_bytes() == before_bytes
    ledger.reserve(p, identity(p), 1, 1)
    with pytest.raises(SecurityError):
        prepare_evaluation_migration(ledger.path, old, ledger.catalog, ledger.policy.evaluation,
                                     provider_policy=kwargs['provider_policy'], now=now[0])
    with pytest.raises(SecurityError): evaluation_policy(ledger.policy, binding)


def test_l1_configuration_contract_without_signing(state, tmp_path):
    import time
    from tests.performance.foundry_l1 import LaunchConfiguration, configuration_digest
    from tests.performance.foundry_preflight import synthetic_contract
    from tests.performance.foundry_recalibration import DEPLOYMENT, RESOURCE
    ledger, p, _, peer, _, old, binding, kwargs = state
    contract = synthetic_contract().model_dump(mode='json')
    contract.update(model=DEPLOYMENT, region='TEST', tier='GlobalStandard', attempts=4,
                    total_input=100000, total_output=12000, rpm=1)
    contract['catalog']['prices'][0]['model'] = DEPLOYMENT
    config = LaunchConfiguration(resource=RESOURCE, deployment=DEPLOYMENT, model='gpt-5.4-mini',
        model_version='2026-03-17', sku='GlobalStandard', endpoint=f'https://{RESOURCE}.openai.azure.com/openai/v1',
        authentication='entra_bearer', credential_valid_until=int(time.time())+3600,
        credential_audience_verified=True, quota_verified=True, shared_consumers_verified=True,
        charges_verified=True, approval_expires=int(time.time())+3600, owner_scope=p.scope.identity(),
        oidc={'issuer':'https://identity.invalid','audience':'test','jwks_url':'https://identity.invalid/keys'},
        security_path=tmp_path/'security.sqlite', governance_path=ledger.path,
        admission_path=binding.provider_path, quota_key=binding.provider_key,
        audit_directory=tmp_path/'audit', embedding_directory=tmp_path/'embedding', embedding_tree_sha256='0'*64,
        actual_azure_rpm=2, actual_azure_tpm=30000, policy=kwargs['provider_policy'],
        governance_policy=ledger.policy, contract=contract)
    assert config.contract.input_tokens == 25000 and config.contract.output_tokens == 3000
    assert config.contract.context == 28000 and config.contract.attempts == 4
    assert (config.contract.total_input, config.contract.total_output) == (100000, 12000)
    legacy = LaunchConfiguration.model_validate({**config.model_dump(), 'governance_policy':old})
    assert 'evaluation' not in legacy.model_dump()['governance_policy']
    assert configuration_digest(config) != configuration_digest(legacy)
    with pytest.raises(ValueError):
        LaunchConfiguration.model_validate({**config.model_dump(), 'owner_scope':peer.scope.identity()})
    with pytest.raises(SecurityError):
        LaunchConfiguration.model_validate({**config.model_dump(), 'quota_key':'separate'})


def test_shared_provider_admission_cannot_be_replenished(state):
    from llm.admission import SQLiteInferenceAdmission
    from llm.inference import InferenceRateLimitError
    ledger, p, _, _, now, _, binding, kwargs = state
    a = SQLiteInferenceAdmission(binding.provider_path, binding.provider_key, kwargs['provider_policy'], clock=lambda:now[0])
    b = SQLiteInferenceAdmission(binding.provider_path, binding.provider_key, kwargs['provider_policy'], clock=lambda:now[0])
    ticket = a.acquire(identity(p), 25000, 3000)
    a.finish(ticket, usage=InferenceUsage(1, 1, 2), outcome='success')
    with pytest.raises(InferenceRateLimitError): b.acquire(identity(p), 25000, 3000)


def test_actual_cost_and_multiowner_tenant_cap(state, tmp_path):
    ledger, p, _, peer, _, old, binding, kwargs = state
    binding = binding.model_copy(update={'governance_path':str(tmp_path/'cost.sqlite'), 'scopes':(p.scope, peer.scope)})
    catalog = ledger.catalog.model_copy(update={'prices':(Price(provider='fake', model='model', input_price='1', output_price='1', price_unit=1),)})
    ledger = GovernanceLedger(binding.governance_path, evaluation_policy(old, binding), catalog, **kwargs)
    ticket = ledger.reserve(p, identity(p), 3, 1)
    ledger.transition(ticket, 'RESERVED', 'ADMITTING'); ledger.transition(ticket, 'ADMITTING', 'STARTED')
    ledger.settle(ticket, InferenceUsage(1, 1, 2))
    settled(ledger, peer, 3)
    with pytest.raises(GovernanceError): settled(ledger, p, 2)
    with pytest.raises(GovernanceError): settled(ledger, peer, 2)


def test_migration_rejects_unresolved_old_authority(state, tmp_path):
    ledger, p, _, _, now, old, binding, kwargs = state
    path = tmp_path/'unresolved.sqlite'
    legacy = GovernanceLedger(path, old, ledger.catalog, clock=lambda:now[0])
    legacy.reserve(p, identity(p), 1, 1)
    binding = binding.model_copy(update={'governance_path':str(path)})
    before = path.read_bytes()
    with pytest.raises(SecurityError):
        prepare_evaluation_migration(path, old, ledger.catalog, binding, provider_policy=kwargs['provider_policy'], now=now[0])
    assert path.read_bytes() == before


def test_reserved_tokens_shared_across_workloads_and_audit_retained(state):
    ledger, p, *_ = state
    first = ledger.reserve(p, identity(p), 55999, 1)
    second = ledger.reserve(p, identity(p), 55999, 1, 'DOCUMENT_BACKGROUND')
    with pytest.raises(GovernanceError): ledger.reserve(p, identity(p), 1, 1, 'DOCUMENT_BACKGROUND')
    ledger.transition(first, 'RESERVED', 'ADMITTING')
    ledger.transition(first, 'ADMITTING', 'RELEASED')
    assert ledger.reserve(p, identity(p), 1, 1)
    with ledger.transaction() as db:
        assert db.execute('SELECT COUNT(*) FROM events').fetchone()[0] == 4
        assert db.execute('SELECT state FROM reservations WHERE ticket=?', (second,)).fetchone()[0] == 'RESERVED'


def test_evaluation_requires_eur_and_bound_authorities(state):
    ledger, _, _, _, _, _, _, kwargs = state
    with pytest.raises(SecurityError): GovernanceLedger(ledger.path, ledger.policy, ledger.catalog)
    with pytest.raises(SecurityError):
        GovernanceLedger(ledger.path, ledger.policy, ledger.catalog.model_copy(update={'currency':'USD'}), **kwargs)


def test_historical_usage_counts_after_synthetic_policy_install(state, tmp_path):
    ledger, p, _, _, now, old, binding, kwargs = state
    path = tmp_path/'history.sqlite'
    legacy = GovernanceLedger(path, old, ledger.catalog, clock=lambda:now[0])
    for _ in range(4): settled(legacy, p, 28000)
    binding = binding.model_copy(update={'governance_path':str(path)})
    target = evaluation_policy(old, binding)
    with legacy.transaction() as db:
        before = history_digest(db)
        db.execute('UPDATE configuration SET policy=? WHERE singleton=1', (target.model_dump_json(),))
        assert history_digest(db) == before
    assert not legacy.ready()
    with pytest.raises(SecurityError): legacy.reserve(p, identity(p), 1, 1)
    current = GovernanceLedger(path, target, ledger.catalog, **kwargs)
    for _ in range(12): settled(current, p, 28000)
    with pytest.raises(GovernanceError): settled(current, p, 2)
    with current.transaction() as db:
        assert db.execute('SELECT COUNT(*) FROM reservations WHERE policy=?', (old.version,)).fetchone()[0] == 4
        assert sum(r[0]+r[1] for r in db.execute('SELECT actual_input,actual_output FROM reservations')) == 448000
