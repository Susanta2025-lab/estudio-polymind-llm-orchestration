"""Actual native Streamlit callback rejects a signed ID token with wrong nonce."""
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time


def run():
    os.environ["DOCUMENTS_PROFILE"] = "synthetic"
    from development.document_demo.provision import provision
    from playwright.sync_api import sync_playwright
    parent = Path(tempfile.mkdtemp(prefix="polymind-nonce-"))
    root = provision(parent / "runtime")
    repo = Path(__file__).resolve().parents[2]
    env = {**os.environ, "PYTHONPATH": str(repo) + os.pathsep + os.environ.get("PYTHONPATH", ""),
           "SSL_CERT_FILE": str(root / "tls.crt"), "REQUESTS_CA_BUNDLE": str(root / "tls.crt")}
    commands = [
        [sys.executable, "-c", "from development.document_demo.identity import issuer_app; import uvicorn; "
         + f"uvicorn.run(issuer_app({str(root)!r},nonce_transform=lambda n:'wrong-nonce'),host='127.0.0.1',port=9444,"
         + f"ssl_keyfile={str(root / 'tls.key')!r},ssl_certfile={str(root / 'tls.crt')!r},access_log=False)"],
        [sys.executable, "-m", "streamlit", "run", str(repo / "ui/app.py"), "--server.address", "127.0.0.1",
         "--server.port", "8501", "--server.headless", "true", "--browser.gatherUsageStats", "false",
         "--secrets.files", str(root / ".streamlit/secrets.toml")],
        [sys.executable, "-m", "development.document_demo", "gateway", str(root)],
    ]
    children = []
    output = (parent / "runtime.log").open("w")
    try:
        for command in commands:
            children.append(subprocess.Popen(command, env=env, cwd=root, stdout=output, stderr=subprocess.STDOUT))
        for port in (9443, 9444, 8501):
            for _ in range(150):
                try:
                    with socket.create_connection(("localhost", port), timeout=.2):
                        break
                except OSError:
                    time.sleep(.1)
            else:
                raise RuntimeError("Local startup failed")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(ignore_https_errors=True)
            callbacks = []
            page.on("request", lambda r: callbacks.append(r.url.split("?")[0]) if "/oauth2callback" in r.url else None)
            page.goto("https://localhost:9443")
            with page.expect_navigation(wait_until="networkidle"):
                page.get_by_role("button", name="Log in", exact=True).click()
            page.get_by_role("button", name="Log in", exact=True).wait_for()
            assert callbacks
            assert not [c for c in page.context.cookies() if c["name"].startswith("_streamlit_user")]
            assert not page.get_by_text("Verified enrolled operator", exact=True).count()
            browser.close()
        print("Native signed-token nonce mismatch denied; no authentication cookie installed", flush=True)
    finally:
        for child in children:
            child.terminate()
        for child in children:
            child.wait(timeout=15)
        output.close()


if __name__ == "__main__":
    run()
