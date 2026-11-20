"""Local fixture TLS entrypoint."""
import ssl
from aiohttp import web
from ui.tls_gateway import gateway


def serve(root, backend="http://127.0.0.1:8501", port=9443, host="127.0.0.1"):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(root / "tls.crt", root / "tls.key")
    web.run_app(gateway(backend, f"https://localhost:{port}"), host=host, port=port,
                ssl_context=context, access_log=None)
