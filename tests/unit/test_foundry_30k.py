"""No Azure requests: deployment allowlist, headroom, windows and full envelopes."""
from dataclasses import replace
from uuid import uuid4

import pytest

from llm.admission import CallIdentity, SQLiteInferenceAdmission
from llm.inference import InferenceConfigurationError, InferenceRateLimitError, InferenceUsage
from tests.performance.foundry_recalibration import (
    DEPLOYMENT, RESOURCE, candidate_capability, candidate_policy, deployment_configuration, reservation,
)


def identity():
    return CallIdentity('offline', uuid4(), uuid4(), 1, 'test/1', 'openai_compatible',
                        'summarization', DEPLOYMENT, 'gpt54mini-30k/1')


@pytest.mark.parametrize('host', ['openai.azure.com', 'services.ai.azure.com'])
def test_only_polymind_configuration(host):
    deployment_configuration(f'https://{RESOURCE}.{host}/openai/v1/',
        {'general':DEPLOYMENT, 'summarization':DEPLOYMENT}, RESOURCE, DEPLOYMENT)


@pytest.mark.parametrize('change', ['eci-endpoint', 'eci-model', 'eci-resource', 'eci-deployment',
    'mixed-role', 'query', 'credential-url', 'plain-http', 'gateway', 'missing-role'])
def test_other_deployment_and_ambiguous_endpoint_refused(change):
    url = f'https://{RESOURCE}.openai.azure.com/openai/v1'
    models = {'general':DEPLOYMENT, 'summarization':DEPLOYMENT}
    resource, deployment = RESOURCE, DEPLOYMENT
    if change == 'eci-endpoint': url = 'https://eci-foundry-dev-susanta.openai.azure.com/openai/v1'
    if change == 'eci-model': models = {k:'eci-gpt-54-mini' for k in models}
    if change == 'eci-resource': resource = 'eci-foundry-dev-susanta'
    if change == 'eci-deployment': deployment = 'eci-gpt-54-mini'
    if change == 'mixed-role': models['coding'] = 'eci-gpt-54-mini'
    if change == 'query': url += '?api-version=unexpected'
    if change == 'credential-url': url = url.replace('https://', 'https://user:synthetic@')
    if change == 'plain-http': url = url.replace('https://', 'http://')
    if change == 'gateway': url = 'https://gateway.invalid/openai/v1'
    if change == 'missing-role': del models['general']
    with pytest.raises(ValueError):
        deployment_configuration(url, models, resource, deployment)


def test_28k_background_reserves_2k_interactive(tmp_path):
    admission = SQLiteInferenceAdmission(tmp_path/'admission.sqlite', 'offline', candidate_policy(), clock=lambda:100.)
    ticket = admission.acquire(identity(), 25000, 3000)
    admission.finish(ticket, usage=InferenceUsage(1, 1, 2), outcome='success')
    interactive = admission.acquire(identity(), 1000, 1000, 'INTERACTIVE')
    admission.finish(interactive, usage=InferenceUsage(1, 1, 2), outcome='success')
    with pytest.raises(InferenceRateLimitError):
        admission.acquire(identity(), 0, 1, 'INTERACTIVE')


@pytest.mark.parametrize('headroom,input_tokens,allowed', [(2000,25000,True), (2001,25000,False),
    (10000,25000,False), (10000,17000,True), (2000,26000,False)])
def test_stricter_interactive_headroom_wins(tmp_path, headroom, input_tokens, allowed):
    admission = SQLiteInferenceAdmission(tmp_path/'admission.sqlite', 'offline',
                                         candidate_policy(interactive_tpm=headroom), clock=lambda:100.)
    if allowed:
        assert admission.acquire(identity(), input_tokens, 3000)
    else:
        with pytest.raises(InferenceConfigurationError):
            admission.acquire(identity(), input_tokens, 3000)


def test_rolling_window_recovers_without_refunding_actual_usage(tmp_path):
    now = [100.]
    admission = SQLiteInferenceAdmission(tmp_path/'admission.sqlite', 'offline', candidate_policy(), clock=lambda:now[0])
    ticket = admission.acquire(identity(), 25000, 3000)
    admission.finish(ticket, usage=InferenceUsage(1, 1, 2), outcome='success')
    now[0] = 159.9
    with pytest.raises(InferenceRateLimitError):
        admission.acquire(identity(), 100, 100)
    now[0] = 161.
    assert admission.acquire(identity(), 100, 100)


def test_active_request_does_not_expire_with_minute(tmp_path):
    now = [100.]
    admission = SQLiteInferenceAdmission(tmp_path/'admission.sqlite', 'offline', candidate_policy(), clock=lambda:now[0])
    admission.acquire(identity(), 100, 100)
    now[0] = 500.
    with pytest.raises(InferenceRateLimitError):
        admission.acquire(identity(), 100, 100)


def test_candidate_is_bounded_below_model_context_and_omits_sampling():
    cap = candidate_capability()
    assert cap.context_tokens == 28000 < 400000
    assert cap.max_output_tokens == 3000 < 128000
    assert cap.output_parameter == 'max_completion_tokens'
    assert cap.temperature is None and cap.reasoning_effort == 'low'
    assert reservation(25000)['minimum_deployment_tpm'] == 30000


@pytest.fixture(scope='module')
def envelopes(tmp_path_factory):
    from tests.performance.foundry_envelopes import assess
    root = tmp_path_factory.mktemp('complete-envelopes')
    # This fixture measures the renderer with a fake replica/provider. It does
    # not exercise authenticated execution or inherit operator configuration.
    from types import SimpleNamespace

    import config.settings as application_config
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(application_config, 'settings', SimpleNamespace(authentication_mode='disabled'))
        return {(pages,mode):assess(root/f'{pages}-{mode}', pages, mode)
                for pages in (4,200) for mode in ('prose','escaped','claims','conflicts')}


def test_near_maximum_results_are_actually_valid_and_full_coverage(envelopes):
    for pages in (4,200):
        case = envelopes[pages,'prose']
        assert case['complete'] and case['provider_calls'] == 0
        assert len(case['records']) == (3 if pages == 4 else 33)
        assert all(r['result_bytes'] == 3000 for r in case['records'])


def test_l2_escaped_children_exceed_input_with_no_truncation(envelopes):
    case = envelopes[200,'escaped']
    assert any(r.get('failure') == 'context_exceeded' and r['rendered']['input'] > 25000
               and r['rendered']['minimum_deployment_tpm'] > 30000 for r in case['records'])
    assert case['complete']  # Offline structural construction continues only to assess every stage.
    assert len(case['questions']) == 12
    assert all(q.get('failure') == 'analysis_limit' for q in case['questions'])


def test_l2_full_claim_lineage_cannot_fit_output(envelopes):
    case = envelopes[200,'claims']
    assert not case['complete']
    failed = case['records'][-1]
    assert failed['required_links'] == 32
    assert failed['result_bytes'] > 3000
    assert failed['failure'] == 'complete_lineage_exceeds_result_bound'
    assert all(n <= 3000 for n in failed['child_result_bytes'])


def test_all_l2_questions_preserved_even_when_refused(envelopes):
    assert len(envelopes[200,'prose']['questions']) == 12
    assert all(q['input'] > 25000 for q in envelopes[200,'prose']['questions'])


def test_l1_complete_envelopes_include_contradiction_heavy_results(envelopes):
    for mode in ('prose', 'escaped', 'claims', 'conflicts'):
        case = envelopes[4, mode]
        assert case['complete'] and case['provider_calls'] == 0
        assert len(case['records']) == 3 and len(case['questions']) == 1
        assert all(not r.get('failure') and r['rendered']['run_fits']
                   and r['rendered']['provider_fits'] for r in case['records'])
        assert all(not q.get('failure') and q['run_fits'] and q['provider_fits']
                   for q in case['questions'])
    # Includes the output schema in the trusted prompt for JSON-object mode.
    assert envelopes[4, 'conflicts']['questions'][0]['input'] == 23548
