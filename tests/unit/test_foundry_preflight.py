"""Financial refusal tests use synthetic prices, never current Azure rates."""
from dataclasses import replace
from decimal import Decimal
from uuid import uuid4

import pytest

from governance.ledger import GovernanceError
from llm.admission import CallIdentity
from llm.inference import InferenceUsage
from tests.performance.foundry_budget import Contract, RunGuard
from tests.performance.foundry_preflight import synthetic_contract


class Admission:
    def __init__(self):
        self.calls = []
        self.finishes = []
        self.fail = False

    def acquire(self, *args):
        if self.fail:
            raise GovernanceError()
        self.calls.append(args)
        return str(uuid4())

    def finish(self, ticket, **kwargs):
        self.finishes.append((ticket, kwargs))


def identity(attempt=1):
    return CallIdentity('opaque-scope', uuid4(), uuid4(), attempt, 'test/1',
                        'openai_compatible', 'summarization', 'offline-model', 'offline/1')


def contract(**changes):
    return Contract.model_validate({**synthetic_contract().model_dump(), **changes})


@pytest.fixture
def run(tmp_path):
    clock = [100.]
    admission = Admission()
    guard = RunGuard(tmp_path/'run.sqlite', contract(), admission, clock=lambda: clock[0])
    return guard, admission, clock


@pytest.mark.parametrize('changes', [
    {'approved':False}, {'currency':'USD'}, {'maximum':'5.01'}, {'maximum':'NaN'},
    {'fixed_cost':None}, {'extra_cost':None}, {'extra_cost':'6'}, {'context':27999},
    {'attempts':51}, {'input_tokens':25001}, {'output_tokens':3001}, {'rpm':3},
    {'tpm':30001}, {'tpm':27999}, {'model':'missing'}, {'region':''}, {'tier':''},
    {'total_input':1250001}, {'total_output':150001}, {'maximum':0.1},
])
def test_unknown_unapproved_or_incompatible_contract(changes):
    with pytest.raises((ValueError, GovernanceError, TypeError)):
        contract(**changes)


@pytest.mark.parametrize('field', ['maximum', 'fixed_cost', 'extra_cost'])
@pytest.mark.parametrize('value', [None, {}, [], 'not-money'])
def test_incomplete_money_is_a_schema_validation_error(field, value):
    from pydantic import ValidationError
    with pytest.raises(ValidationError) as error:
        contract(**{field: value})
    assert error.value.errors()[0]['loc'] == (field,)


def test_cost_arithmetic_includes_separate_charges():
    c = contract(fixed_cost='1', extra_cost='2')
    assert c.cost(50) == Decimal('3.155')
    assert c.fits(50) and not c.fits(51)
    assert not contract(maximum='0.003').fits(1)


def test_future_catalog_and_currency_mismatch():
    raw = synthetic_contract().model_dump()
    raw['catalog']['effective_date'] = '2999-01-01'
    with pytest.raises(ValueError):
        Contract.model_validate(raw)
    raw['catalog']['effective_date'] = '2026-01-01'
    raw['catalog']['currency'] = 'USD'
    with pytest.raises(ValueError):
        Contract.model_validate(raw)


def test_full_reservations_persist_across_restart_and_retry(tmp_path):
    clock = [100.]
    a = Admission()
    c = contract(attempts=2, maximum='0.0062')
    guard = RunGuard(tmp_path/'run.sqlite', c, a, clock=lambda:clock[0])
    first = identity()
    ticket = guard.acquire(first, 200, 100)
    guard.finish(ticket, usage=InferenceUsage(1, 1, 2), outcome='success')
    clock[0] += 61
    reopened = RunGuard(tmp_path/'run.sqlite', c, a, clock=lambda:clock[0])
    ticket = reopened.acquire(replace(first, attempt=2), 200, 100)
    reopened.finish(ticket, usage=InferenceUsage(1, 1, 2), outcome='success')
    clock[0] += 61
    with pytest.raises(GovernanceError):
        reopened.acquire(replace(first, attempt=3), 200, 100)
    assert len(a.calls) == 2
    assert sum(r['input'] for r in reopened.records()) == 50000


@pytest.mark.parametrize('usage', [None, InferenceUsage(1, None, None),
    InferenceUsage(None, 1, None), InferenceUsage(1, 1, 3), InferenceUsage(25001, 1, 25002),
    InferenceUsage(1, 3001, 3002), InferenceUsage(True, 1, 2)])
def test_unknown_partial_inconsistent_or_excess_usage_stops(run, usage):
    guard, a, clock = run
    ticket = guard.acquire(identity(), 200, 100)
    with pytest.raises(GovernanceError):
        guard.finish(ticket, usage=usage, outcome='success')
    assert guard.records()[0]['finished'] is None
    clock[0] += 61
    with pytest.raises(GovernanceError):
        guard.acquire(identity(), 200, 100)
    assert len(a.calls) == 1


@pytest.mark.parametrize('reason', ['cancelled', 'identity', 'evidence', 'publication', 'quality', 'dependency'])
def test_external_stop_is_sticky_after_restart(run, reason):
    guard, a, clock = run
    guard.stop(reason)
    guard = RunGuard(guard.path, guard.contract, a, clock=lambda:clock[0])
    with pytest.raises(GovernanceError):
        guard.acquire(identity(), 200, 100)
    assert not a.calls


@pytest.mark.parametrize('outcome', ['timeout', 'overloaded', 'configuration_failure', 'protocol_failure', 'output_limit'])
def test_first_provider_error_stops_even_with_known_usage(run, outcome):
    guard, a, clock = run
    ticket = guard.acquire(identity(), 200, 100)
    guard.finish(ticket, usage=InferenceUsage(1, 1, 2), outcome=outcome)
    assert guard.records()[0]['outcome'] == 'failed'
    assert guard.records()[0]['finished'] is not None
    clock[0] += 61
    with pytest.raises(GovernanceError):
        guard.acquire(identity(), 200, 100)


def test_crash_reservation_and_concurrency_fail_closed(run):
    guard, a, clock = run
    guard.acquire(identity(), 200, 100)
    clock[0] += 3600
    reopened = RunGuard(guard.path, guard.contract, a, clock=lambda:clock[0])
    with pytest.raises(GovernanceError):
        reopened.acquire(identity(), 200, 100)
    assert len(a.calls) == 1


def test_tpm_not_refunded_from_small_actual_usage(run):
    guard, a, clock = run
    ticket = guard.acquire(identity(), 200, 100)
    guard.finish(ticket, usage=InferenceUsage(1, 1, 2), outcome='success')
    with pytest.raises(GovernanceError):
        guard.acquire(identity(), 200, 100)
    assert len(a.calls) == 1


def test_downstream_denial_stops(run):
    guard, a, clock = run
    a.fail = True
    with pytest.raises(GovernanceError):
        guard.acquire(identity(), 200, 100)
    a.fail = False
    clock[0] += 61
    with pytest.raises(GovernanceError):
        guard.acquire(identity(), 200, 100)
    assert not a.calls


@pytest.mark.parametrize('input_tokens,output_tokens', [(25001, 100), (10, 3001), (-1, 1), (True, 1), (1, 0)])
def test_request_bounds_before_downstream(run, input_tokens, output_tokens):
    guard, a, _ = run
    with pytest.raises(GovernanceError):
        guard.acquire(identity(), input_tokens, output_tokens)
    assert not a.calls


def test_exact_model_catalog_identity(run):
    guard, a, _ = run
    with pytest.raises(GovernanceError):
        guard.acquire(replace(identity(), model='unapproved'), 100, 100)
    assert not a.calls


@pytest.mark.parametrize('changes', [{'total_input':25000}, {'total_output':3000}, {'maximum':'0.0031'}])
def test_cumulative_limits_include_every_retry(tmp_path, changes):
    clock = [100.]
    a = Admission()
    guard = RunGuard(tmp_path/'run.sqlite', contract(**changes), a, clock=lambda:clock[0])
    ticket = guard.acquire(identity(), 100, 100)
    guard.finish(ticket, usage=InferenceUsage(1, 1, 2), outcome='success')
    clock[0] += 61
    with pytest.raises(GovernanceError):
        guard.acquire(identity(2), 100, 100)
    assert len(a.calls) == 1


def test_reopen_cannot_raise_budget(run):
    guard, a, _ = run
    with pytest.raises(GovernanceError):
        RunGuard(guard.path, contract(attempts=49), a)


def test_two_connections_cannot_admit_concurrently(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    a = Admission()
    guards = [RunGuard(tmp_path/'run.sqlite', contract(), a) for _ in range(2)]
    barrier = Barrier(2)
    def acquire(guard):
        barrier.wait()
        try:
            return guard.acquire(identity(), 100, 100)
        except GovernanceError:
            return None
    with ThreadPoolExecutor(2) as pool:
        results = list(pool.map(acquire, guards))
    assert sum(r is not None for r in results) == 1
    assert len(a.calls) == 1


def test_rpm_is_independent_of_tpm(tmp_path):
    a = Admission()
    c = contract(input_tokens=1000, output_tokens=100)
    guard = RunGuard(tmp_path/'run.sqlite', c, a, clock=lambda:100.)
    for _ in range(2):
        ticket = guard.acquire(identity(), 100, 100)
        guard.finish(ticket, usage=InferenceUsage(1, 1, 2), outcome='success')
    with pytest.raises(GovernanceError):
        guard.acquire(identity(), 100, 100)
    assert len(a.calls) == 2
