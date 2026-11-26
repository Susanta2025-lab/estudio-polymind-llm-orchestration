"""Production TLS entrypoint contracts using ephemeral, explicitly test-only keys."""
import asyncio
from datetime import datetime, timedelta, timezone
import ssl

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import pytest

from deployment.phase19 import gateway as entrypoint


@pytest.fixture(params=['phase19.test.invalid', 'polymind.test'])
def tls_files(tmp_path, monkeypatch, request):
    hostname = request.param
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, hostname)])
    now = datetime.now(timezone.utc)
    cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name)
            .public_key(key.public_key()).serial_number(x509.random_serial_number())
            .not_valid_before(now - timedelta(minutes=1))
            .not_valid_after(now + timedelta(minutes=10))
            .add_extension(x509.SubjectAlternativeName([x509.DNSName(hostname)]), critical=False)
            .sign(key, hashes.SHA256()))
    certificate, private_key = tmp_path / 'tls.crt', tmp_path / 'tls.key'
    certificate.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    private_key.write_bytes(key.private_bytes(serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
    for path in (certificate, private_key):
        path.chmod(0o600)
    original = entrypoint.private_path
    paths = {'/run/secrets/tls.crt': certificate, '/run/secrets/tls.key': private_key}
    monkeypatch.setattr(entrypoint, 'private_path', lambda path, **kwargs: original(paths[path], **kwargs))
    monkeypatch.setenv('PHASE19_ORIGIN', f'https://{hostname}:9443')
    return certificate, private_key


def test_production_context_completes_hostname_verified_tls_handshake(tls_files, monkeypatch):
    captured = {}
    monkeypatch.setattr(entrypoint.web, 'run_app', lambda app, **kwargs: captured.update(kwargs))
    entrypoint.main()
    context = captured['ssl_context']
    assert context.minimum_version == ssl.TLSVersion.TLSv1_2
    assert captured['port'] == 9443 and captured['access_log'] is None

    async def run():
        async def echo(reader, writer):
            try:
                writer.write(await reader.readexactly(4))
                await writer.drain()
            finally:
                writer.close()
                await writer.wait_closed()
        server = await asyncio.start_server(echo, '127.0.0.1', 0, ssl=context)
        try:
            client = ssl.create_default_context(cafile=str(tls_files[0]))
            reader, writer = await asyncio.wait_for(asyncio.open_connection(
                '127.0.0.1', server.sockets[0].getsockname()[1], ssl=client,
                server_hostname=x509.load_pem_x509_certificate(tls_files[0].read_bytes())
                    .extensions.get_extension_for_class(x509.SubjectAlternativeName)
                    .value.get_values_for_type(x509.DNSName)[0]), timeout=5)
            try:
                assert writer.get_extra_info('ssl_object').version() in {'TLSv1.2', 'TLSv1.3'}
                writer.write(b'test')
                await writer.drain()
                assert await asyncio.wait_for(reader.readexactly(4), timeout=5) == b'test'
            finally:
                writer.close()
                await writer.wait_closed()
        finally:
            server.close()
            await server.wait_closed()
    asyncio.run(run())


@pytest.mark.parametrize('fault', ['missing_cert', 'missing_key', 'invalid_cert', 'invalid_key',
                                  'public_cert', 'public_key', 'symlink_key', 'symlink_cert'])
def test_tls_inputs_fail_before_listener(tls_files, monkeypatch, fault):
    cert, key = tls_files
    if fault.startswith('missing_'):
        (cert if fault.endswith('cert') else key).unlink()
    elif fault.startswith('invalid_'):
        (cert if fault.endswith('cert') else key).write_text('invalid test material')
    elif fault.startswith('public_'):
        (cert if fault.endswith('cert') else key).chmod(0o644)
    else:
        path = cert if fault.endswith('cert') else key
        target = path.with_suffix('.target')
        path.rename(target)
        path.symlink_to(target)
    def forbidden(*args, **kwargs):
        pytest.fail('Unsafe TLS configuration reached the listener')
    monkeypatch.setattr(entrypoint.web, 'run_app', forbidden)
    with pytest.raises((OSError, ValueError)):
        entrypoint.main()


@pytest.mark.parametrize('origin', ['http://phase19.test.invalid:9443', 'https://localhost:9443',
    'https://127.0.0.1:9443', 'https://[::1]:9443', 'https://phase19.test.invalid/path',
    'https://user:password@phase19.test.invalid', 'https://phase19.test.invalid?query=1',
    'https://phase19.test.invalid#fragment'])
def test_unsafe_production_origin_denied_before_tls_loading(monkeypatch, origin):
    monkeypatch.setenv('PHASE19_ORIGIN', origin)
    monkeypatch.setattr(entrypoint, 'private_path', lambda *a, **k: pytest.fail('Origin was accepted'))
    with pytest.raises(ValueError, match='private HTTPS origin'):
        entrypoint.main()


def test_selected_origin_verified_https_callback_and_websocket(tls_files, monkeypatch):
    """Exercise real TLS entrypoint + proxy; fixture upstream has UI routes only."""
    from aiohttp import ClientSession, TCPConnector, WSServerHandshakeError, web
    from aiohttp.abc import AbstractResolver
    from ui.tls_gateway import gateway
    import os

    origin = os.environ['PHASE19_ORIGIN']
    hostname = origin.split('://')[1].split(':')[0]
    captured = {}
    monkeypatch.setattr(entrypoint.web, 'run_app', lambda app, **kw: captured.update(kw))
    entrypoint.main()

    class LoopbackResolver(AbstractResolver):
        async def resolve(self, host, port=0, family=0):
            return [dict(hostname=host, host='127.0.0.1', port=port, family=family, proto=0, flags=0)]

        async def close(self):
            pass

    async def run():
        seen = []

        async def callback(request):
            seen.append(dict(request.headers))
            return web.Response(text='synthetic callback reached')

        async def echo(request):
            ws = web.WebSocketResponse()
            await ws.prepare(request)
            async for message in ws:
                await ws.send_str(message.data)
            return ws

        upstream = web.Application()
        upstream.router.add_get('/oauth2callback', callback)
        upstream.router.add_get('/socket', echo)
        runner = web.AppRunner(upstream)
        await runner.setup()
        site = web.TCPSite(runner, '127.0.0.1', 0)
        await site.start()
        proxy = web.AppRunner(gateway(f'http://127.0.0.1:{site._server.sockets[0].getsockname()[1]}', origin))
        try:
            await proxy.setup()
            tls_site = web.TCPSite(proxy, '127.0.0.1', 0, ssl_context=captured['ssl_context'])
            await tls_site.start()
            port = tls_site._server.sockets[0].getsockname()[1]
            url = f'https://{hostname}:{port}'
            context = ssl.create_default_context(cafile=str(tls_files[0]))
            async with ClientSession(connector=TCPConnector(ssl=context, resolver=LoopbackResolver()), trust_env=False) as client:
                headers = {'Host': origin.removeprefix('https://'), 'Origin': origin,
                           'Forwarded': 'host=attacker', 'X-Forwarded-Host': 'attacker', 'X-Forwarded-Proto': 'http'}
                async with client.get(url + '/oauth2callback?code=synthetic&state=synthetic', headers=headers) as response:
                    assert response.status == 200
                    assert await response.text() == 'synthetic callback reached'
                assert seen[0]['Host'] == headers['Host']
                assert seen[0]['X-Forwarded-Proto'] == 'https'
                assert 'Forwarded' not in seen[0] and 'X-Forwarded-Host' not in seen[0]
                for changes in ({'Host': 'attacker'}, {'Host': hostname}, {'Origin': 'https://attacker'}):
                    async with client.get(url + '/oauth2callback', headers=headers | changes) as response:
                        assert response.status == 403
                assert len(seen) == 1
                for supplied in (None, 'https://attacker'):
                    ws_headers = {'Host': headers['Host']}
                    if supplied:
                        ws_headers['Origin'] = supplied
                    with pytest.raises(WSServerHandshakeError) as error:
                        await client.ws_connect(url + '/socket', headers=ws_headers)
                    assert error.value.status == 403
                async with client.ws_connect(url + '/socket', headers=headers) as ws:
                    await ws.send_str('synthetic')
                    assert (await ws.receive(timeout=3)).data == 'synthetic'
                # These requests reach only the UI fixture, never an API upstream.
                for path in ('/health', '/ready', '/metrics', '/documents/operator/context'):
                    async with client.get(url + path, headers=headers) as response:
                        assert response.status == 404
            for client_context, server_name in ((ssl.create_default_context(), hostname), (context, 'wrong.test.invalid')):
                with pytest.raises(ssl.SSLCertVerificationError):
                    await asyncio.wait_for(asyncio.open_connection('127.0.0.1', port,
                        ssl=client_context, server_hostname=server_name), timeout=5)
        finally:
            await proxy.cleanup()
            await runner.cleanup()

    asyncio.run(run())
