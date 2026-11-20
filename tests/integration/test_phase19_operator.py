"""Non-fixture assembly with real OIDC/security/finance and test-only adapters."""
import json
import socket
import time
from uuid import UUID

import jwt
import pytest
from fastapi.testclient import TestClient

from development.document_demo.provision import provision
from development.document_demo.runtime import build as fixture_build
from development.document_demo.fixtures import FixtureModel, FixtureVectors
from deployment.phase19.runtime import build, configuration, deny_external_execution
from deployment.phase19.storage import ownership
from documents.models import Scope, stable_id
from documents.operator.app import create_app
from documents.pilot.models import PilotError


@pytest.fixture
def external(tmp_path, monkeypatch):
    monkeypatch.setenv('DOCUMENTS_PROFILE', 'synthetic')
    demo = provision(tmp_path / 'fixture')
    rt, flow, _, _ = fixture_build(demo, initialize=True)
    root = tmp_path / 'external'; root.mkdir(mode=0o700)
    (root / 'private').mkdir(mode=0o700); (root / 'private/objects').mkdir(mode=0o700)
    (root / 'sources').mkdir(mode=0o700)
    tenant = '12345678-1234-1234-1234-123456789abc'
    audience = '12345678-1234-1234-1234-123456789def'
    issuer = 'https://login.microsoftonline.com/' + tenant + '/v2.0'
    enrollment = (issuer, tenant, 'external-operator')
    scope = Scope(tenant=stable_id('polymind-identity/1/tenant', issuer, tenant),
                  owner=stable_id('polymind-identity/1/owner', issuer, tenant, enrollment[2]))
    source = next(iter(flow.pilot.sources.values())).model_copy(update={'owner': scope, 'approved_by': scope.owner})
    values = dict(DEPLOYMENT_ENV='production', API_AUTH_MODE='oidc_jwt', API_DOCS_ENABLED=False,
        OIDC_CONFIGURATION=dict(token_profile='entra_v2', tenant_id=tenant, issuer=issuer, audience=audience,
            jwks_url=f'https://login.microsoftonline.com/{tenant}/discovery/v2.0/keys'),
        GOVERNANCE_ENABLED=True, SECURITY_AUTHORITY_PATH=str(root / 'private/security.sqlite'),
        GOVERNANCE_AUTHORITY_PATH=str(root / 'private/governance.sqlite'),
        GOVERNANCE_PROVIDER_PATH=str(root / 'private/admission.sqlite'),
        GOVERNANCE_POLICY=rt.governance.policy.model_dump(mode='json'),
        GOVERNANCE_PRICING=rt.governance.catalog.model_dump(mode='json'),
        GOVERNANCE_PROVIDER_POLICY=rt.admission.policy.model_dump(mode='json'), GOVERNANCE_PROVIDER_KEY='external-test/1',
        INFERENCE_PROVIDER='openai_compatible', OPENAI_COMPATIBLE_BASE_URL='https://provider.invalid/openai/v1/',
        OPENAI_COMPATIBLE_API_KEY_FILE=str(root / 'provider'),
        OPENAI_COMPATIBLE_MODEL_MAP={role: 'offline-model' for role in ('general','fast','coding','summarization')},
        MEMORY_PROVIDER='redis', REDIS_URL='redis://redis:6379/0', VECTOR_STORE_PROVIDER='chroma_http',
        VECTOR_STORE_HOST='chroma', MODEL_OFFLINE_MODE=True, MODEL_ARTIFACT_DIR='/opt/polymind/models')
    manifest = dict(version='phase19-runtime/1', enrollment=enrollment, sources=[source.model_dump(mode='json')],
        approvals=[flow.approvals[0].model_copy(update={'approved_by': scope.owner}).model_dump(mode='json')],
        managed=flow.pilot.managed_settings.model_dump(mode='json'),
        analysis=flow.pilot.analysis_capability.model_dump(mode='json'),
        planning=flow.pilot.planning_profile.model_dump(mode='json'))
    files = {'configuration.json': json.dumps(values), 'manifest.json': json.dumps(manifest),
             'deployment.json': json.dumps(dict(version='phase19-state/1', container_root=str(root))),
             'provider': 'offline-test-only', 'sources/' + source.sha256: flow.catalog[source.approval_id].decode()}
    for name, value in files.items():
        (root / name).write_text(value); (root / name).chmod(0o600)
    import sentence_transformers
    monkeypatch.setattr(sentence_transformers, 'SentenceTransformer', lambda *a, **k: FixtureModel())
    monkeypatch.setattr(sentence_transformers, 'CrossEncoder', lambda *a, **k: None)
    import config.model_artifacts
    monkeypatch.setattr(config.model_artifacts, 'validate_model_artifacts', lambda *a: None)
    import rag.vector_store_factory
    class Vectors(FixtureVectors):
        def close(self):
            pass
    monkeypatch.setattr(rag.vector_store_factory, 'create_publication_vector_store',
        lambda *a, **k: Vectors(root / 'private/test-vectors.json', initialize=not (root / 'private/test-vectors.json').exists()))
    monkeypatch.setattr(socket.socket, 'connect', lambda *a: (_ for _ in ()).throw(AssertionError('No network')))
    identity = json.loads((demo / 'identity.json').read_text())
    def token(**changes):
        claims = dict(iss=issuer, sub=enrollment[2], tid=tenant, aud=audience, ver='2.0', iat=int(time.time()),
            nbf=int(time.time()) - 1, exp=int(time.time()) + 3600, scp='access_as_user', roles=['PolyMind.L1Operator'])
        claims.update(changes)
        return jwt.encode(claims, (demo / 'signing.pem').read_bytes(), algorithm='RS256', headers={'kid': 'fixture'})
    with ownership(root, initialize=True):
        runtime, workflow, runner, cleanup = build(root, initialize=True)
    runtime.verifier.fetch = lambda: {'keys': [identity['jwk']]}
    principal = runtime.verifier.verify(token())
    runtime.authority.register(principal)
    yield root, runtime, workflow, runner, cleanup, token, identity
    runner.close(); cleanup()


def test_non_fixture_http_identity_and_denied_execution(external):
    root, runtime, workflow, runner, cleanup, token, _ = external
    assert not getattr(workflow.pilot.provider, 'pilot_fixture', False)
    with TestClient(create_app(runtime, workflow, runner)) as client:
        assert client.get('/documents/operator/context').status_code == 401
        client.headers['Authorization'] = 'Bearer ' + token()
        context = client.get('/documents/operator/context').json()
        assert context['mode'] == 'EXTERNAL_EXECUTION_BLOCKED'
        assert context['execution_enabled'] is False
        assert 'start' not in context['allowed_actions']
        assert client.get('/documents/operator/sources').status_code == 200
        assert client.post('/query', json={'query': 'no'}).status_code == 403
        for changes in ({'exp': 1}, {'sub': 'other'}, {'tid': 'other'}, {'aud': 'other'},
                        {'roles': ['admin']}, {'scp': 'openid'}, {'token_use': 'id'}):
            client.headers['Authorization'] = 'Bearer ' + token(**changes)
            assert client.get('/documents/operator/context').status_code in {401, 403}
        client.headers['Authorization'] = 'Bearer ' + token()
        created = client.post('/documents/operator/sessions', json={
            'source_approval_id': next(iter(workflow.catalog)), 'request_key': 'external-test-create-0001'})
        assert created.status_code == 201, created.text
        session = created.json()['session_id']
        for suffix in ('/start', '/questions'):
            response = client.post('/documents/operator/sessions/' + session + suffix,
                json={} if suffix == '/start' else {'query': 'test', 'request_key': 'external-question-0001'})
            assert response.status_code == 503, response.text
        assert not runner.grants
    with runtime.governance.transaction() as db:
        assert db.execute('SELECT COUNT(*) FROM reservations').fetchone()[0] == 0
    with pytest.raises(PilotError):
        deny_external_execution(None, None, None, None)


def test_reopen_discards_execution_grants_and_keeps_authorities(external):
    root, _, old, runner, _, _, _ = external
    from deployment.phase19.backup import inventory
    before = inventory(root / 'private')
    with ownership(root):
        runtime, workflow, new_runner, cleanup = build(root)
        try:
            assert not new_runner.grants and not workflow.execution_enabled
            assert workflow.pilot.control.ready()
            assert inventory(root / 'private') == before
        finally:
            cleanup()


@pytest.mark.parametrize('change', [
    {'OIDC_CONFIGURATION': None}, {'API_AUTH_MODE': 'disabled'}, {'GOVERNANCE_ENABLED': False},
    {'OPENAI_COMPATIBLE_API_KEY_FILE': None}, {'OPENAI_COMPATIBLE_BASE_URL': 'http://provider/v1'},
    {'OPENAI_COMPATIBLE_BASE_URL': 'https://provider/legacy'}, {'DOCUMENTS_PROFILE': 'synthetic'},
    {'GOVERNANCE_PROVIDER_PATH': '/other/admission.sqlite'}, {'MEMORY_PROVIDER': 'file'},
    {'VECTOR_STORE_PROVIDER': 'chroma_local'},
])
def test_production_missing_or_unsafe_configuration(external, change):
    root = external[0]
    path = root / 'configuration.json'
    values = json.loads(path.read_text()); values.update(change); path.write_text(json.dumps(values))
    with pytest.raises(ValueError):
        configuration(root)


@pytest.mark.parametrize('missing', ['managed_usage', 'analysis_usage', 'strict_schema'])
def test_missing_provider_capability_denied_before_effects(external, missing):
    root, runtime, workflow, _, _, _, _ = external
    path = root / 'manifest.json'; manifest = json.loads(path.read_text())
    if missing == 'managed_usage':
        manifest['managed']['capability']['usage_reporting'] = False
    elif missing == 'analysis_usage':
        manifest['analysis']['usage_reporting'] = False
    else:
        manifest['managed']['capability'].pop('schema_profile')
    path.write_text(json.dumps(manifest))
    with ownership(root):
        with pytest.raises(ValueError):
            build(root)
    with runtime.governance.transaction() as db:
        assert db.execute('SELECT COUNT(*) FROM reservations').fetchone()[0] == 0
