"""Inert native authentication inventory and selected deployment contract."""
from pathlib import Path

import toml
import yaml
from streamlit import auth_util
from streamlit.runtime.secrets import AttrDict

REPO = Path(__file__).resolve().parents[2]


def test_native_template_matches_selected_origin_and_installed_streamlit(monkeypatch):
    values = dict(line.split('=', 1) for line in
                  (REPO / 'deployment/phase19/compose.env.example').read_text().splitlines()
                  if line and not line.startswith('#'))
    auth = toml.loads((REPO / 'deployment/phase19/streamlit.secrets.example.toml').read_text())['auth']
    assert values['PHASE19_ORIGIN'] == 'https://polymind.test:9443'
    assert auth['redirect_uri'] == values['PHASE19_ORIGIN'] + '/oauth2callback'
    assert auth['server_metadata_url'] == 'https://login.microsoftonline.com/<TENANT_UUID>/v2.0/.well-known/openid-configuration'
    assert auth['client_id'] == '<STREAMLIT_BROWSER_CLIENT_UUID>'
    assert auth['client_secret'] == auth['cookie_secret'] == '<SUPPLIED_PRIVATELY_BY_CUSTODIAN>'
    assert auth['client_kwargs']['scope'] == 'openid api://<API_CLIENT_UUID>/access_as_user'
    # Structural compatibility only: Streamlit does not verify these placeholders.
    # Never call login or contact discovery. Use only a synthetic in-memory mapping.
    section = AttrDict(auth)
    provider = auth_util.generate_default_provider_section(section)
    assert provider['client_kwargs']['scope'] == auth['client_kwargs']['scope']
    assert auth_util.get_redirect_uri(section) == auth['redirect_uri']
    monkeypatch.setattr(auth_util, 'get_secrets_auth_section', lambda: section)
    assert auth_util.get_expose_tokens_config() == ['access']
    doc = yaml.safe_load((REPO / 'docker-compose.phase19.yml').read_text())
    mount, = doc['services']['ui']['volumes']
    assert mount['source'] == '${PHASE19_STREAMLIT_SECRET:?Supply external OIDC Streamlit secrets}'
    assert mount['target'] == '/tmp/.streamlit/secrets.toml'
    assert mount['read_only'] and mount['bind']['create_host_path'] is False
    assert not (REPO / 'deployment/phase19/secrets.toml').exists()
