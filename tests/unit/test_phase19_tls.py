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


@pytest.fixture
def tls_files(tmp_path, monkeypatch):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'phase19.test.invalid')])
    now = datetime.now(timezone.utc)
    cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name)
            .public_key(key.public_key()).serial_number(x509.random_serial_number())
            .not_valid_before(now - timedelta(minutes=1))
            .not_valid_after(now + timedelta(minutes=10))
            .add_extension(x509.SubjectAlternativeName([x509.DNSName('phase19.test.invalid')]), critical=False)
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
    monkeypatch.setenv('PHASE19_ORIGIN', 'https://phase19.test.invalid:9443')
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
                server_hostname='phase19.test.invalid'), timeout=5)
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
                                  'public_cert', 'public_key', 'symlink_key'])
def test_tls_inputs_fail_before_listener(tls_files, monkeypatch, fault):
    cert, key = tls_files
    if fault.startswith('missing_'):
        (cert if fault.endswith('cert') else key).unlink()
    elif fault.startswith('invalid_'):
        (cert if fault.endswith('cert') else key).write_text('invalid test material')
    elif fault.startswith('public_'):
        (cert if fault.endswith('cert') else key).chmod(0o644)
    else:
        target = key.with_suffix('.target')
        key.rename(target)
        key.symlink_to(target)
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
