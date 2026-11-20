"""Offline deployment invariants, actual private files, exclusion and recovery."""
import json
import os
from pathlib import Path
import sqlite3

from filelock import Timeout
import pytest
import yaml

from deployment.phase19.storage import DATABASES, ownership, preflight, private_path
from deployment.phase19.backup import snapshot, restore, inventory
from llm.provider_factory import provider_credential, _create_inference_provider
from config.settings import Settings

REPO = Path(__file__).resolve().parents[2]


def state(root, binding=None):
    root.mkdir(mode=0o700, parents=True)
    (root / 'private').mkdir(mode=0o700)
    (root / 'private/objects').mkdir(mode=0o700)
    (root / 'deployment.json').write_text(json.dumps({'version': 'phase19-state/1', 'container_root': binding or str(root)}))
    (root / 'deployment.json').chmod(0o600)
    for name in DATABASES:
        with sqlite3.connect(root / 'private' / name) as db:
            db.execute('CREATE TABLE evidence (value TEXT)')
            db.execute("INSERT INTO evidence VALUES ('UNKNOWN:retained')")
            db.execute('PRAGMA user_version=1')
        (root / 'private' / name).chmod(0o600)
    return root


def test_compose_isolation_and_dependencies():
    doc = yaml.safe_load((REPO / 'docker-compose.phase19.yml').read_text())
    services = doc['services']
    assert set(services) == {'api', 'ui', 'gateway', 'redis', 'chroma'}
    assert services['api']['depends_on'] == {s: {'condition': 'service_healthy'} for s in ('redis', 'chroma')}
    assert services['ui']['depends_on']['api']['condition'] == 'service_healthy'
    assert services['gateway']['depends_on']['ui']['condition'] == 'service_healthy'
    assert services['gateway']['ports'] == ['127.0.0.1:9443:9443']
    for name, svc in services.items():
        assert svc['user'] not in {'root', '0', '0:0'}
        assert svc['read_only'] and svc['cap_drop'] == ['ALL']
        assert svc['security_opt'] == ['no-new-privileges:true']
        assert svc['restart'] == 'on-failure:3'
        assert svc['stop_grace_period'] == '90s'
        assert svc['logging']['options'] == {'max-size': '5m', 'max-file': '3'}
        assert svc['mem_limit'] and svc['cpus'] and svc['healthcheck']
        if name != 'gateway':
            assert 'ports' not in svc
        for mount in svc.get('volumes', []):
            assert mount['bind']['create_host_path'] is False
    assert doc['networks']['backend']['internal']
    assert doc['networks']['frontend']['internal']
    assert services['redis']['networks'] == services['chroma']['networks'] == ['backend']
    assert services['api']['command'] == ['python', '-m', 'deployment.phase19', 'serve', '/state']
    assert all(m['read_only'] for m in services['gateway']['volumes'])
    assert 'development.document_demo' not in (REPO / 'docker-compose.phase19.yml').read_text()


def test_authority_lock_and_restart(tmp_path):
    root = state(tmp_path / 'state')
    before = inventory(root)
    with ownership(root):
        with pytest.raises(Timeout):
            with ownership(root):
                pytest.fail('second writer')
    with ownership(root):
        assert inventory(root) == before
    assert (root / 'runtime.lock').exists()


@pytest.mark.parametrize('failure', ['missing', 'empty', 'permission', 'symlink', 'marker', 'object_root'])
def test_reopen_never_repairs_or_resets(tmp_path, failure):
    root = state(tmp_path / 'state')
    db = root / 'private/governance.sqlite'
    if failure == 'missing':
        db.unlink()
    elif failure == 'empty':
        db.write_bytes(b'')
    elif failure == 'permission':
        db.chmod(0o644)
    elif failure == 'symlink':
        other = root / 'other'; db.rename(other); db.symlink_to(other)
    elif failure == 'marker':
        (root / 'deployment.json').write_text('{}')
    else:
        (root / 'private/objects').rmdir()
    with pytest.raises((ValueError, OSError, sqlite3.Error)):
        with ownership(root):
            pytest.fail('unsafe reopen')
    if failure == 'missing':
        assert not db.exists()
    if failure == 'empty':
        assert db.read_bytes() == b''


def test_initialization_refuses_existing_truth(tmp_path):
    root = state(tmp_path / 'state')
    with pytest.raises(ValueError, match='Existing authority'):
        preflight(root, initialize=True)


def test_backup_restore_isolated_complete_and_tamper_denied(tmp_path):
    data = tmp_path / 'data'; data.mkdir(mode=0o700)
    root = state(data / 'operator', binding='/state')
    for service in ('redis', 'chroma'):
        (data / service).mkdir(mode=0o700)
        (data / service / 'durable').write_bytes(b'persistent vendor state')
    backup = tmp_path / 'backup'
    with pytest.raises(ValueError):
        snapshot(data, backup)
    with ownership(root, container_root='/state'):
        with pytest.raises(Timeout):
            snapshot(data, backup, stopped=True)
    before = inventory(data)
    snapshot(data, backup, stopped=True)
    target = tmp_path / 'isolated'
    restore(backup, target)
    assert inventory(target) == before
    with sqlite3.connect(target / 'operator/private/governance.sqlite') as db:
        assert db.execute('SELECT value FROM evidence').fetchone()[0] == 'UNKNOWN:retained'
    with pytest.raises(ValueError):
        restore(backup, target)
    (backup / 'data/redis/durable').write_bytes(b'corrupted')
    with pytest.raises(ValueError, match='integrity'):
        restore(backup, tmp_path / 'another')


@pytest.mark.parametrize('header', ['Authorization', 'api-key'])
def test_mounted_credential_factory_header(tmp_path, header):
    secret = tmp_path / 'provider'; secret.write_text('offline-test-secret\n'); secret.chmod(0o600)
    cfg = Settings(_env_file=None, INFERENCE_PROVIDER='openai_compatible',
        OPENAI_COMPATIBLE_API_KEY_FILE=str(secret), OPENAI_COMPATIBLE_AUTHENTICATION_HEADER=header)
    provider = _create_inference_provider(cfg)
    try:
        assert provider.headers[header] == ('Bearer offline-test-secret' if header == 'Authorization' else 'offline-test-secret')
        assert 'offline-test-secret' not in repr(cfg)
    finally:
        provider.close()
    secret.chmod(0o644)
    with pytest.raises(ValueError):
        provider_credential(cfg)


@pytest.mark.parametrize('content', ['', 'a b', 'x' * 16385])
def test_bad_secret_fails_closed(tmp_path, content):
    secret = tmp_path / 'provider'; secret.write_text(content); secret.chmod(0o600)
    cfg = Settings(_env_file=None, OPENAI_COMPATIBLE_API_KEY_FILE=str(secret))
    with pytest.raises(ValueError):
        provider_credential(cfg)


def test_secret_configuration_conflicts_denied():
    with pytest.raises(ValueError):
        Settings(_env_file=None, OPENAI_COMPATIBLE_API_KEY='inline', OPENAI_COMPATIBLE_API_KEY_FILE='/secret')
    with pytest.raises(ValueError):
        Settings(_env_file=None, OPENAI_COMPATIBLE_AUTHENTICATION_HEADER='arbitrary-header')


def test_runner_rejects_duplicate_start_and_stops():
    from types import SimpleNamespace
    from documents.operator.service import LocalRunner
    runner = LocalRunner(SimpleNamespace(pilot=object()), interval=0.01)
    runner.start()
    try:
        with pytest.raises(RuntimeError):
            runner.start()
    finally:
        runner.close()
    assert not runner.thread.is_alive()
    with pytest.raises(RuntimeError):
        runner.start()


def test_remote_filesystem_denied(monkeypatch, tmp_path):
    from deployment.phase19.storage import local_filesystem
    original = Path.read_text
    for filesystem in ('nfs', 'nfs4', 'cifs', 'smb3', 'fuse'):
        monkeypatch.setattr(Path, 'read_text', lambda p, *a, fs=filesystem, **k:
            f'1 1 0:1 / / rw - {fs} remote rw\n' if str(p) == '/proc/self/mountinfo' else original(p, *a, **k))
        with pytest.raises(ValueError):
            local_filesystem(tmp_path)


def test_external_workflow_cannot_enable_execution_by_flag():
    from documents.operator.service import OperatorWorkflow
    with pytest.raises(ValueError, match='permission integration'):
        OperatorWorkflow(None, None, (), {}, (), synthetic=False, execution_enabled=True)


def test_gateway_host_origin_cookie_and_forwarded_headers():
    import asyncio
    from aiohttp import ClientSession, web
    from ui.tls_gateway import gateway
    async def run():
        seen = []
        async def upstream(request):
            seen.append(dict(request.headers))
            return web.Response(text='private-ui', headers={'Set-Cookie': 'session=test; HttpOnly'})
        upstream_app = web.Application(); upstream_app.router.add_route('*', '/{tail:.*}', upstream)
        upstream_runner = web.AppRunner(upstream_app); await upstream_runner.setup()
        upstream_site = web.TCPSite(upstream_runner, '127.0.0.1', 0); await upstream_site.start()
        upstream_port = upstream_site._server.sockets[0].getsockname()[1]
        proxy_runner = web.AppRunner(gateway(f'http://127.0.0.1:{upstream_port}', 'https://private.example'))
        await proxy_runner.setup()
        proxy_site = web.TCPSite(proxy_runner, '127.0.0.1', 0); await proxy_site.start()
        port = proxy_site._server.sockets[0].getsockname()[1]
        try:
            async with ClientSession(trust_env=False) as client:
                for headers, path in [({'Host':'foreign.example'}, '/'),
                        ({'Host':'private.example','Origin':'https://foreign.example'}, '/'),
                        ({'Host':'private.example','Sec-Fetch-Site':'cross-site'}, '/auth/login')]:
                    async with client.get(f'http://127.0.0.1:{port}'+path, headers=headers) as response:
                        assert response.status == 403
                assert not seen
                async with client.get(f'http://127.0.0.1:{port}/', headers={'Host':'private.example',
                        'Origin':'https://private.example','X-Forwarded-Host':'attacker',
                        'Forwarded':'host=attacker','X-Forwarded-Proto':'http'}) as response:
                    assert response.status == 200 and await response.text() == 'private-ui'
                    assert '; Secure' in response.headers['Set-Cookie']
                    assert response.headers['Cache-Control'] == 'no-store'
                assert seen[0]['Host'] == 'private.example'
                assert seen[0]['X-Forwarded-Proto'] == 'https'
                assert 'X-Forwarded-Host' not in seen[0] and 'Forwarded' not in seen[0]
        finally:
            await proxy_runner.cleanup(); await upstream_runner.cleanup()
    asyncio.run(run())


def test_gateway_websocket_requires_exact_origin():
    import asyncio
    from aiohttp import ClientSession, WSServerHandshakeError, web
    from ui.tls_gateway import gateway
    async def run():
        async def echo(request):
            socket = web.WebSocketResponse(); await socket.prepare(request)
            async for msg in socket:
                await socket.send_str(msg.data)
            return socket
        app = web.Application(); app.router.add_get('/socket', echo)
        runner = web.AppRunner(app); await runner.setup()
        site = web.TCPSite(runner, '127.0.0.1', 0); await site.start()
        upstream_port = site._server.sockets[0].getsockname()[1]
        proxy = web.AppRunner(gateway(f'http://127.0.0.1:{upstream_port}', 'https://private.example'))
        await proxy.setup(); proxy_site = web.TCPSite(proxy, '127.0.0.1', 0); await proxy_site.start()
        port = proxy_site._server.sockets[0].getsockname()[1]
        try:
            async with ClientSession(trust_env=False) as client:
                with pytest.raises(WSServerHandshakeError):
                    await client.ws_connect(f'http://127.0.0.1:{port}/socket', headers={'Host':'private.example'})
                async with client.ws_connect(f'http://127.0.0.1:{port}/socket',
                        headers={'Host':'private.example','Origin':'https://private.example'}) as socket:
                    await socket.send_str('bounded-test')
                    assert (await socket.receive(timeout=3)).data == 'bounded-test'
        finally:
            await proxy.cleanup(); await runner.cleanup()
    asyncio.run(run())
