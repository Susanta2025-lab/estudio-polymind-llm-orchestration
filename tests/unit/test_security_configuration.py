import pytest
from pydantic import ValidationError

from config.settings import Settings
from tests.unit.test_governance import configuration


def configured(tmp_path):
    policy,catalog=configuration()
    return dict(_env_file=None,API_AUTH_MODE='oidc_jwt',API_AUTH_ENABLED=False,API_AUTH_TOKEN=None,
        OIDC_CONFIGURATION={'issuer':'https://issuer.invalid','audience':'polymind','jwks_url':'https://issuer.invalid/keys'},
        SECURITY_AUTHORITY_PATH=str(tmp_path/'security.sqlite'),GOVERNANCE_ENABLED=True,
        GOVERNANCE_AUTHORITY_PATH=str(tmp_path/'governance.sqlite'),GOVERNANCE_POLICY=policy.model_dump(mode='json'),
        GOVERNANCE_PRICING=catalog.model_dump(mode='json'),GOVERNANCE_PROVIDER_PATH=str(tmp_path/'provider.sqlite'),
        GOVERNANCE_PROVIDER_KEY='test-only',GOVERNANCE_PROVIDER_POLICY={'rpm':100,'tpm':100000,'concurrent':10,
            'interactive_rpm':50,'interactive_tpm':50000,'interactive_slots':5,'per_job_rpm':10})


def test_explicit_modes_preserve_legacy_contract(tmp_path):
    assert Settings(_env_file=None).authentication_mode=='disabled'
    assert Settings(_env_file=None,API_AUTH_ENABLED=True,API_AUTH_TOKEN='x'*32).authentication_mode=='static_bearer'
    assert Settings(_env_file=None,API_AUTH_MODE='static_bearer',API_AUTH_TOKEN='x'*32).authentication_mode=='static_bearer'
    assert Settings(**configured(tmp_path)).authentication_mode=='oidc_jwt'


@pytest.mark.parametrize('change',[
    {'GOVERNANCE_ENABLED':False},{'OIDC_CONFIGURATION':None},{'API_AUTH_ENABLED':True},
    {'API_AUTH_TOKEN':'static-token'},{'GOVERNANCE_POLICY':None},{'GOVERNANCE_PRICING':None},
    {'SECURITY_AUTHORITY_PATH':'relative.sqlite'},{'API_AUTH_MODE':'disabled'},
    {'GOVERNANCE_PROVIDER_KEY':None},
])
def test_incomplete_or_conflicting_multiuser_configuration_rejected(tmp_path,change):
    with pytest.raises(ValidationError):Settings(**{**configured(tmp_path),**change})


def test_governed_factory_blocks_all_unbound_generation(tmp_path):
    from llm.provider_factory import create_inference_provider
    from security.models import SecurityError
    from llm.inference import ModelRole
    provider=create_inference_provider(Settings(**configured(tmp_path)))
    for method in (provider.generate,provider.generate_stream,provider.execute):
        with pytest.raises(SecurityError):method('unattributed',ModelRole.GENERAL)
