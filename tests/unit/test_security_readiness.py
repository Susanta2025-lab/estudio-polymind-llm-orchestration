"""Closure probes use only temporary authorities and synthetic JWKS."""
import sqlite3
from types import SimpleNamespace

import pytest

from config.settings import Settings
from security.runtime import SecurityRuntime
from security.services import AuthorizedAnalysis
from tests.unit.test_security_configuration import configured
from tests.unit.test_security_identity import identity  # noqa: F401


@pytest.fixture
def runtime(tmp_path, identity):
    result = SecurityRuntime(Settings(**configured(tmp_path)))
    result.verifier = identity[0]
    assert result.ready()
    return result


@pytest.mark.parametrize('component', ['authority', 'governance', 'admission'])
def test_unavailable_database_fails_runtime_readiness(runtime, component):
    database = getattr(runtime, component)
    database.path.rename(database.path.with_suffix('.saved'))
    database.path.mkdir()
    assert database.ready() is False
    assert runtime.ready() is False


@pytest.mark.parametrize('component', ['authority', 'governance', 'admission'])
@pytest.mark.parametrize('damage', ['version', 'schema'])
def test_incompatible_schema_fails_runtime_readiness(runtime, component, damage):
    database = getattr(runtime, component)
    with sqlite3.connect(database.path) as db:
        if damage == 'version':
            db.execute('PRAGMA user_version=99')
        else:
            table = {'authority': 'principals', 'governance': 'reservations',
                     'admission': 'inference_calls'}[component]
            db.execute(f'ALTER TABLE {table} ADD COLUMN incompatible TEXT')
    assert database.ready() is False
    assert runtime.ready() is False


@pytest.mark.parametrize('component', ['authority', 'governance'])
def test_exhausted_audit_capacity_fails_runtime_readiness(runtime, component):
    if component == 'authority':
        runtime.authority.audit_limit = 1
        runtime.authority.audit_authentication(True)
    else:
        runtime.governance.event_limit = 1
        with runtime.governance.transaction() as db:
            db.execute("INSERT INTO events VALUES('fixture','tenant','owner','RESERVE',0)")
    assert getattr(runtime, component).ready() is False
    assert runtime.ready() is False


@pytest.mark.parametrize('state', ['fresh', 'stale', 'unusable'])
def test_jwks_readiness(runtime, state):
    verifier = runtime.verifier
    if state == 'stale':
        verifier.clock = lambda: verifier._loaded + verifier.config.cache_seconds + 1
        verifier.fetch = lambda: (_ for _ in ()).throw(OSError('synthetic outage'))
    elif state == 'unusable':
        verifier._keys = {}
        verifier._loaded = verifier._attempted = None
        verifier.fetch = lambda: {'keys': []}
    assert verifier.ready() is (state == 'fresh')
    assert runtime.ready() is (state == 'fresh')


@pytest.mark.parametrize('composition', ['usable', 'missing', 'empty', 'publication_unready', 'runtime_missing'])
def test_oidc_api_readiness_composes_authorized_analysis(runtime, monkeypatch, composition):
    from api import app as module
    from llm.inference import ReadinessStatus

    healthy = SimpleNamespace(ready=True, status='ready', provider='fake',
                              corpus_version='v1', loaded_version='v1', expected_version='v1')
    monkeypatch.setattr(module.settings, 'API_AUTH_MODE', 'oidc_jwt')
    monkeypatch.setattr(module.inference_provider, 'check_readiness', lambda: SimpleNamespace(
        ready=True, status=ReadinessStatus.READY, provider='fake', models={}))
    monkeypatch.setattr(module.memory_store, 'check_readiness', lambda: healthy)
    monkeypatch.setattr(module, 'check_vector_store_readiness', lambda: healthy)
    monkeypatch.setattr(module, 'check_bm25_readiness', lambda **kwargs: healthy)
    publications = {'fixture': SimpleNamespace(replica=SimpleNamespace(
        ready=lambda: composition != 'publication_unready'))}
    secured = AuthorizedAnalysis(runtime.authority, runtime.governance, runtime.admission,
                                 {} if composition == 'empty' else publications)
    monkeypatch.setattr(module.app.state, 'document_analysis', None, raising=False)
    monkeypatch.setattr(module.app.state, 'security_runtime',
                        None if composition == 'runtime_missing' else runtime, raising=False)
    monkeypatch.setattr(module.app.state, 'authorized_analysis',
                        None if composition == 'missing' else secured, raising=False)
    response = module.readiness()
    assert response.status_code == (200 if composition == 'usable' else 503)
    if composition != 'usable':
        assert b'security_unavailable' in response.body
    assert str(runtime.authority.path).encode() not in response.body
