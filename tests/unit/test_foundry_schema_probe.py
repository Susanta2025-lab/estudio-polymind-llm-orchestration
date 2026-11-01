"""Focused offline preparation checks; never inspect real credentials or sign."""
from copy import deepcopy
from decimal import Decimal
import socket

import pytest

from documents.models import Scope
from governance.ledger import PricingCatalog
from tests.performance import foundry_schema_probe as probe


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def deny(*args, **kwargs):
        raise AssertionError('Preparation must remain offline')
    monkeypatch.setattr(socket.socket, 'connect', deny)
    monkeypatch.setattr(socket, 'getaddrinfo', deny)


def catalog():
    return PricingCatalog(version='phase17hl-pricing-eur-202610/1', currency='EUR',
        effective_date='2026-10-01', operator_approved=True, prices=[dict(
            provider='openai_compatible', model=probe.DEPLOYMENT,
            input_price='0.659978880676', output_price='3.959873284055', price_unit=1000000)])


def previous():
    return dict(provider='openai_compatible', model=probe.DEPLOYMENT, region='spaincentral',
        tier='GlobalStandard', price_source='Synthetic review fixture', approved=True,
        currency='EUR', maximum='5', fixed_cost='0', extra_cost='0', attempts=4,
        total_input=100000, total_output=12000, context=28000)


def test_one_call_exact_price_and_no_mutation():
    old = previous()
    before = deepcopy(old)
    contract = probe.one_call_contract(old, catalog())
    assert old == before
    assert contract.fits(1) and not contract.fits(2)
    assert contract.cost(1) == Decimal('0.028379091869065')
    assert contract.maximum == Decimal('5')
    assert (contract.total_input, contract.total_output) == (25000, 3000)


def test_changed_catalog_rejected():
    changed = catalog().model_copy(update={'version': 'changed/1'})
    with pytest.raises(ValueError, match='catalog changed'):
        probe.one_call_contract(previous(), changed)


@pytest.mark.parametrize('field,value', [('model', 'other'), ('extra_cost', '0.01')])
def test_incompatible_financial_contract(field, value):
    old = previous()
    old[field] = value
    with pytest.raises(Exception):
        probe.one_call_contract(old, catalog())


@pytest.mark.parametrize('changed', ['generation', 'schema'])
def test_drift_fails_closed(monkeypatch, changed):
    # Start from a synthetic matching binding so each mutation is tested independently.
    monkeypatch.setattr(probe, 'GENERATION', probe.generation_contract_digest())
    if changed == 'generation':
        monkeypatch.setattr(probe, 'generation_contract_digest', lambda: '0'*64)
    else:
        monkeypatch.setattr(probe, 'provider_schema', lambda schema: {'type': 'object'})
    with pytest.raises(ValueError, match='contract changed'):
        probe.verified_schema()


def test_first_stage_is_non_executable_and_fresh(tmp_path, monkeypatch):
    # Synthetic review binding only; never refresh the historical authorized hash.
    monkeypatch.setattr(probe, 'GENERATION', probe.generation_contract_digest())
    from uuid import UUID
    scope = Scope(tenant=UUID(int=1), owner=UUID(int=2))
    first = probe.prepare_stage(tmp_path/'first', scope)
    second = probe.prepare_stage(tmp_path/'second', scope)
    assert first['executable'] is False and first['provider_calls'] == 0
    assert first['generation_contract_sha256'] == probe.generation_contract_digest()
    assert first['first_stage']['stage'] == 'analysis'
    assert len(first['first_stage']['source_data']) == 4
    assert first['rendered_request_sha256'] == second['rendered_request_sha256']
    for field in ('experiment_id', 'job_id', 'request_id'):
        assert UUID(first[field]) != UUID(second[field])
    assert first['estimated_input_tokens'] <= 25000
    assert first['response_format']['json_schema']['strict'] is True
    with pytest.raises(RuntimeError, match='cannot perform inference'):
        probe.PreparationProvider().execute(None)


def test_historical_generation_binding_remains_stale_and_blocked(tmp_path):
    from uuid import UUID
    assert probe.generation_contract_digest() != probe.GENERATION
    with pytest.raises(ValueError, match='Authorized generation contract changed'):
        probe.prepare_stage(tmp_path / 'blocked', Scope(tenant=UUID(int=1), owner=UUID(int=2)))
    assert not (tmp_path / 'blocked').exists()
