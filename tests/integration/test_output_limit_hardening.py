"""Offline provider -> financial settlement -> durable job/audit regression."""
import json
import pytest

from governance.ledger import GovernanceError, GovernanceLedger
from tests.performance.foundry_preflight import OfflineHTTP, execute
from tests.unit.test_structured_provider import Response


@pytest.mark.parametrize('fault', ['none', 'unknown_usage', 'settlement', 'admission_finish'])
def test_failed_call_audit_and_settlement(tmp_path, monkeypatch, fault):
    def response(self, sent, result, stage):
        return Response(dict(model='offline-model', choices=[dict(
            message=dict(content='synthetic-sensitive-output'), finish_reason='length')],
            usage=None if fault == 'unknown_usage' else dict(prompt_tokens=30, completion_tokens=40,
                total_tokens=70, completion_tokens_details=dict(reasoning_tokens=0))))
    monkeypatch.setattr(OfflineHTTP, 'response', response)
    if fault == 'settlement':
        def fail(*args, **kwargs):
            raise GovernanceError('reservation_conflict')
        monkeypatch.setattr(GovernanceLedger, 'settle', fail)
    if fault == 'admission_finish':
        from llm.admission import SQLiteInferenceAdmission
        def fail(*args, **kwargs):
            raise GovernanceError('reservation_conflict')
        monkeypatch.setattr(SQLiteInferenceAdmission, 'finish', fail)
    result = execute(tmp_path, 'L1')
    assert result['job_state'] == 'FAILED' and result['calls'] == 1
    # Accounting failures retain the original provider failure; ledger state
    # still exposes unresolved settlement and must never imply success.
    assert result['terminal_category'] == 'inference_output_limit'
    expected = {'none': 'SETTLED', 'unknown_usage': 'UNKNOWN', 'settlement': 'STARTED', 'admission_finish': 'SETTLED'}
    assert result['governance_records'][0]['state'] == expected[fault]
    assert (result['run_records'][0]['finished'] is not None) == (fault in ('none', 'settlement'))
    record = json.loads((tmp_path/'provider-calls.json').read_text())[0]
    assert record['outcome'] == 'output_limit'
    assert record['output_limit_diagnostics']['failure_cause'] == 'provider_completion_truncated'
    assert record['output_limit_diagnostics']['usage_available'] == (fault != 'unknown_usage')
    assert 'response' not in record
    assert 'synthetic-sensitive-output' not in (tmp_path/'result.json').read_text()
    assert 'synthetic-sensitive-output' not in (tmp_path/'provider-calls.json').read_text()
    assert 'publication' not in result


def test_independent_l1_limits_preserve_four_call_accounting(tmp_path, monkeypatch):
    from llm.openai_compatible import OpenAICompatibleProvider
    from tests.performance.foundry_preflight import synthetic_contract
    from tests.performance.foundry_l1 import generation_contract_digest
    original = OpenAICompatibleProvider.execute
    captured = []
    def capture(self, request):
        captured.append(request)
        return original(self, request)
    monkeypatch.setattr(OpenAICompatibleProvider, 'execute', capture)
    from tests.performance.foundry_budget import Contract
    contract = Contract.model_validate({**synthetic_contract().model_dump(),
        'attempts': 4, 'total_input': 100000, 'total_output': 12000})
    monkeypatch.setattr('tests.performance.foundry_preflight.synthetic_contract', lambda: contract)
    assert (contract.input_tokens, contract.output_tokens, contract.total_input,
            contract.total_output, contract.context, contract.attempts) == (25000, 3000, 100000, 12000, 28000, 4)
    before = generation_contract_digest()
    result = execute(tmp_path, 'L1')
    assert result['calls'] == len(captured) == 4
    assert all(r.output_tokens == 3000 for r in captured)
    for request in captured[:3]:
        control = json.loads(request.system.split('\nCONTROL\n')[1])
        assert request.response_bytes == control['max_response_bytes'] == control['max_result_bytes'] == 10000
        assert request.max_response_envelope_bytes == 26192
        assert control['profile']['template_version'] == 'managed-prompt/7'
    assert all(r['state'] == 'SETTLED' and r['actual_cost'] == '0.000011'
               for r in result['governance_records'])
    assert generation_contract_digest() == before


def test_subject_contract_failure_settles_once_without_retry(tmp_path, monkeypatch):
    original = OfflineHTTP.response

    def response(self, sent, result, stage):
        data = json.loads(result)
        data['claims'][0].update(kind='commentary', subject='SYNTHETIC_PRIVATE_SUBJECT')
        return original(self, sent, json.dumps(data), stage)

    monkeypatch.setattr(OfflineHTTP, 'response', response)
    result = execute(tmp_path, 'L1')
    assert result['job_state'] == 'FAILED'
    assert result['terminal_category'] == 'serialization_error'
    assert result['calls'] == len(result['run_records']) == len(result['governance_records']) == 1
    assert result['run_records'][0]['finished'] is not None
    assert result['run_records'][0]['outcome'] == 'success'
    assert result['governance_records'][0]['state'] == 'SETTLED'
    assert result['governance_records'][0]['actual_cost'] == '0.000011'
