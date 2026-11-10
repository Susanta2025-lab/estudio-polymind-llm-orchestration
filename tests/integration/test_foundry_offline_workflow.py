"""Real local composition, synthetic HTTP only; forbid socket connections."""
import json
import socket

import pytest

# Permanent historical canonical-output characterization.
pytestmark = pytest.mark.usefixtures("managed_v9")


from tests.performance.foundry_preflight import execute


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    def deny(*args, **kwargs):
        raise AssertionError('L0 must not access the network')
    monkeypatch.setattr(socket.socket, 'connect', deny)
    monkeypatch.setattr(socket, 'create_connection', deny)


@pytest.mark.parametrize('stage,calls,pages', [('L1', 4, 4), ('L2', 45, 200)])
def test_managed_governed_pipeline_and_pending_review(tmp_path, stage, calls, pages):
    result = execute(tmp_path, stage)
    assert result['job_state'] == 'COMPLETED'
    assert result['digest_status'] == 'COMPLETE'
    assert result['source_evidence'] == pages
    assert result['calls'] == calls
    assert len(result['run_records']) == len(result['governance_records']) == calls
    assert all(r['state'] == 'SETTLED' for r in result['governance_records'])
    assert all(r['actual_cost'] == '0.000011' for r in result['governance_records'])
    assert len(result['provider_records']) == calls
    assert all(r['duration_seconds'] >= 0 and r['measured_cost'] == '0.000011'
               and len(r['response_sha256']) == 64 for r in result['provider_records'])
    assert result['publication']['citations'] == 8
    assert result['questions']['status'] == 'COMPLETE'
    packets = json.loads((tmp_path/'review-packets.json').read_text())
    assert all(p['independent_reviewer'] is None and p['reviewer_judgment'] is None for p in packets)
    assert all(len(p['response_sha256']) == 64 for p in packets)
    assert result['billable_calls'] == 0
    if stage == 'L2':
        assert result['quality']['claim_support']['numerator'] == 4
        assert result['quality']['contradiction_qualification_preservation']['numerator'] == 2


def test_missing_usage_stops_before_second_provider_call(tmp_path, monkeypatch):
    from llm.openai_compatible import OpenAICompatibleProvider
    monkeypatch.setattr(OpenAICompatibleProvider, '_usage', staticmethod(lambda _:None))
    result = execute(tmp_path, 'L1')
    assert result['job_state'] == 'FAILED'
    assert result['calls'] == 1
    assert result['governance_records'][0]['state'] == 'UNKNOWN'
    assert result['run_records'][0]['finished'] is None
    assert 'publication' not in result


def test_governance_denial_never_reaches_provider(tmp_path, monkeypatch):
    from governance.ledger import GovernanceLedger, GovernanceError
    def deny(*args, **kwargs):
        raise GovernanceError()
    monkeypatch.setattr(GovernanceLedger, 'reserve', deny)
    result = execute(tmp_path, 'L1')
    assert result['job_state'] == 'FAILED'
    assert result['calls'] == 0
    assert not result['run_records']
    assert not result['governance_records']


def test_l1_publication_check_uses_authorization_with_oidc(tmp_path, monkeypatch):
    from config.settings import settings
    from documents.publication.retrieval import PublicationReplica
    monkeypatch.setattr(settings, 'API_AUTH_MODE', 'oidc_jwt')
    original = PublicationReplica.validate_pin
    checked = []
    def validate(self, pin):
        assert pin.authorization is not None
        checked.append(pin)
        return original(self, pin)
    monkeypatch.setattr(PublicationReplica, 'validate_pin', validate)
    result = execute(tmp_path, 'L1')
    assert checked
    assert result['calls'] == 4
    assert result['questions']['status'] == 'COMPLETE'
