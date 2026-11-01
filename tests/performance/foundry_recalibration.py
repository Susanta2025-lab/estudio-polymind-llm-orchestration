"""Offline 30K policy and deployment isolation contract; no Azure discovery."""
from urllib.parse import urlsplit

from llm.admission import AdmissionPolicy
from llm.structured import CapabilityProfile

DEPLOYMENT = 'epolymind-gpt-54-mini'
RESOURCE = 'epolymind-foundry-dev-susanta'


def deployment_configuration(base_url, model_map, resource, deployment):
    """Allow only the operator-named PolyMind v1 target; never use an ECI alias.

    This is a local validation-project allowlist, not domain logic or proof of
    credential authority. Private-link/custom gateway URLs require separate review.
    """
    url = urlsplit(base_url)
    if (resource != RESOURCE or deployment != DEPLOYMENT
            or url.scheme != 'https' or url.username or url.password or url.port
            or url.query or url.fragment or url.path.rstrip('/') != '/openai/v1'
            or url.hostname not in {f'{RESOURCE}.openai.azure.com', f'{RESOURCE}.services.ai.azure.com'}
            or not model_map or set(model_map.values()) != {DEPLOYMENT}
            or not {'general', 'summarization'} <= model_map.keys()):
        raise ValueError('Validation deployment isolation failed')


def candidate_policy(*, interactive_tpm=2000):
    # Explicit proposal: increase old synthetic headroom (1) to 2000. A larger
    # existing operational reserve wins; never overwrite a live authority policy.
    return AdmissionPolicy(rpm=2, tpm=30000, concurrent=2, interactive_rpm=1,
        interactive_tpm=interactive_tpm, interactive_slots=1, per_job_rpm=1, per_job_concurrent=1)


def candidate_capability(*, strict_digestion=False):
    # Model limit is 400k; using 28k here deliberately constrains the run instead.
    return CapabilityProfile(version='gpt54mini-30k/2' if strict_digestion else 'gpt54mini-30k/1', context_tokens=28000,
        max_output_tokens=3000, overhead_tokens=100, safety_tokens=100,
        output_parameter='max_completion_tokens', reasoning_effort='low',
        schema_profile='azure-strict/1' if strict_digestion else None,
        temperature=None, structured_output='json_schema' if strict_digestion else 'json_object', streaming=False, usage_reporting=True,
        response_models=('gpt-5.4-mini', 'gpt-5.4-mini-2026-03-17'))


def reservation(input_tokens, output_tokens=3000, *, interactive_tpm=2000, workload='DOCUMENT_BACKGROUND'):
    combined = input_tokens + output_tokens
    headroom = interactive_tpm if workload == 'DOCUMENT_BACKGROUND' else 0
    return dict(input=input_tokens, output=output_tokens, combined=combined,
                protected_interactive_tpm=headroom, minimum_deployment_tpm=combined+headroom,
                run_fits=input_tokens <= 25000 and output_tokens <= 3000 and combined <= 28000,
                provider_fits=combined+headroom <= 30000)
