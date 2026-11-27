"""Explicit check/serve lifecycle. Serve requires separate live-auth authorization."""

import argparse
import asyncio
import os
import signal
import socket
import ssl
import sys
import time
from pathlib import Path

import toml
from aiohttp import web
from cryptography import x509
from cryptography.x509.oid import ExtendedKeyUsageOID

from deployment.phase19.identity_bootstrap.core import ORIGIN, validate_auth
from deployment.phase19.identity_bootstrap.files import REPO, directory, read_private
from ui.tls_gateway import gateway

UI_PORT = 8503
WINDOW_SECONDS = 900


def tls_context(root):
    certificate = read_private(root / "tls.crt")
    key = read_private(root / "tls.key")
    cert = x509.load_pem_x509_certificate(certificate)
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    if (
        not cert.not_valid_before_utc <= now < cert.not_valid_after_utc
        or cert.extensions.get_extension_for_class(
            x509.SubjectAlternativeName
        ).value.get_values_for_type(x509.DNSName)
        != ["polymind.test"]
        or ExtendedKeyUsageOID.SERVER_AUTH
        not in cert.extensions.get_extension_for_class(x509.ExtendedKeyUsage).value
    ):
        raise ValueError("TLS identity unavailable")
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    descriptors = []
    try:
        # OpenSSL requires filenames. Anonymous Linux descriptors avoid reopening
        # operator paths after validation and never create extra plaintext files.
        for data in (certificate, key):
            fd = os.memfd_create("bootstrap-tls", os.MFD_CLOEXEC)
            descriptors.append(fd)
            os.fchmod(fd, 0o600)
            os.write(fd, data)
        context.load_cert_chain(*(f"/proc/self/fd/{fd}" for fd in descriptors))
    finally:
        for fd in descriptors:
            os.close(fd)
    return context


def preflight(root, evidence):
    with directory(root), directory(root / ".streamlit"), directory(evidence):
        if root == evidence or root in evidence.parents or evidence in root.parents:
            raise ValueError("Separate session and evidence directories required")
        if set(p.name for p in root.iterdir()) != {".streamlit", "tls.crt", "tls.key"}:
            raise ValueError("Dedicated session directory required")
        if set(p.name for p in (root / ".streamlit").iterdir()) != {"secrets.toml"}:
            raise ValueError("Only native authentication configuration is permitted")
        if any(evidence.iterdir()):
            raise ValueError("New empty evidence directory required")
    validate_auth(
        toml.loads(read_private(root / ".streamlit/secrets.toml").decode("utf-8"))
    )
    return tls_context(root)


def reserve(port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # No reuse-port: bootstrap and future SSH tunnel must be mutually exclusive.
        listener.bind(("127.0.0.1", port))
        listener.listen(32)
        listener.setblocking(False)
        return listener
    except BaseException:
        listener.close()
        raise


def environment(root, evidence):
    return dict(
        PATH=os.defpath,
        HOME=str(root),
        LANG="C.UTF-8",
        PYTHONPATH=str(REPO),
        PYTHONDONTWRITEBYTECODE="1",
        POLYMIND_BOOTSTRAP_SESSION=str(root),
        POLYMIND_BOOTSTRAP_EVIDENCE=str(evidence),
        HF_HUB_OFFLINE="1",
        TRANSFORMERS_OFFLINE="1",
        HF_HUB_DISABLE_TELEMETRY="1",
        ANONYMIZED_TELEMETRY="false",
    )


async def supervise(root, evidence, context):
    listener = reserve(
        9443
    )  # Hold callback endpoint continuously, even during child startup.
    child = None
    runner = None
    try:
        with reserve(UI_PORT):
            pass  # Advisory only: Streamlit itself must also bind the exact port or exit.
        child = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m",
            "deployment.phase19.identity_bootstrap",
            "_ui",
            cwd=root,
            env=environment(root, evidence),
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
            start_new_session=True,
        )
        # Do not expose callback routes until the native child reports local readiness.
        from aiohttp import ClientSession, ClientTimeout

        async with ClientSession(
            trust_env=False, timeout=ClientTimeout(total=1)
        ) as client:
            deadline = time.monotonic() + 30
            while True:
                if child.returncode is not None or time.monotonic() >= deadline:
                    raise RuntimeError("UI unavailable")
                try:
                    async with client.get(
                        f"http://127.0.0.1:{UI_PORT}/_stcore/health"
                    ) as response:
                        if response.status == 200:
                            break
                except (OSError, asyncio.TimeoutError):
                    pass
                await asyncio.sleep(0.1)
        runner = web.AppRunner(
            gateway(f"http://127.0.0.1:{UI_PORT}", ORIGIN),
            access_log=None,
            shutdown_timeout=3,
        )
        await runner.setup()
        await web.SockSite(runner, listener, ssl_context=context).start()
        print("BOOTSTRAP_HTTPS: READY; EXECUTION_AUTHORIZED: NO", flush=True)
        deadline = time.monotonic() + WINDOW_SECONDS
        while child.returncode is None and time.monotonic() < deadline:
            await asyncio.sleep(0.2)
    finally:
        try:
            if runner is not None:
                await runner.cleanup()
        finally:
            listener.close()
            if child is not None:
                try:
                    os.killpg(child.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    await asyncio.wait_for(child.wait(), timeout=5)
                except asyncio.TimeoutError:
                    os.killpg(child.pid, signal.SIGKILL)
                    await child.wait()


def worker():
    # Private HOME/cwd contain no config.toml; explicit single secrets source.
    from streamlit.web import bootstrap

    root = Path(os.environ["POLYMIND_BOOTSTRAP_SESSION"])
    flags = {
        "server.address": "127.0.0.1",
        "server.port": UI_PORT,
        "server.headless": True,
        "browser.gatherUsageStats": False,
        "server.fileWatcherType": "none",
        "server.enableCORS": True,
        "server.enableXsrfProtection": True,
        "client.showErrorDetails": "none",
        "logger.level": "error",
        "secrets.files": [str(root / ".streamlit/secrets.toml")],
    }
    bootstrap.load_config_options(flags)
    bootstrap.run(str(Path(__file__).with_name("ui.py")), False, [], flags)


def main():
    os.umask(0o077)
    if sys.argv[1:] == ["_ui"]:
        worker()
        return
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "serve"))
    parser.add_argument("session", type=Path)
    parser.add_argument("evidence", type=Path)
    parser.add_argument(
        "--authorize-entra",
        action="store_true",
        help="Operator confirms separately granted live-auth network authorization",
    )
    args = parser.parse_args()
    try:
        context = preflight(args.session, args.evidence)
        if args.command == "check":
            # Port checks are loopback binds only; no discovery/login/authority construction.
            with reserve(9443), reserve(UI_PORT):
                print("BOOTSTRAP_PREFLIGHT: PASS; AUTHENTICATION_STARTED: NO")
            return
        if not args.authorize_entra:
            raise ValueError("Separate authentication authorization required")

        def stop(signum, frame):
            raise KeyboardInterrupt

        signal.signal(signal.SIGTERM, stop)
        asyncio.run(supervise(args.session, args.evidence, context))
    except (Exception, KeyboardInterrupt):
        raise SystemExit(
            "Bootstrap stopped or unavailable. Reconcile private session/evidence; no details logged."
        ) from None


if __name__ == "__main__":
    main()
