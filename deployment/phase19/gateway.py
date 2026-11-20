"""Explicit private TLS entrypoint over the existing tested proxy factory."""
import os
import ssl
from urllib.parse import urlsplit

from aiohttp import web
from ui.tls_gateway import gateway
from deployment.phase19.storage import private_path


def main():
    origin = os.environ['PHASE19_ORIGIN']
    parsed = urlsplit(origin)
    if (parsed.scheme != 'https' or not parsed.hostname or parsed.hostname in {'localhost', '127.0.0.1', '::1'}
            or parsed.path or parsed.query or parsed.fragment or parsed.username or parsed.password):
        raise ValueError('Explicit private HTTPS origin required')
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(private_path('/run/secrets/tls.crt', directory=False),
                            private_path('/run/secrets/tls.key', directory=False))
    web.run_app(gateway('http://ui:8501', origin), host='0.0.0.0', port=9443,
                ssl_context=context, access_log=None, shutdown_timeout=65)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        raise SystemExit('Private TLS configuration unavailable.') from None
