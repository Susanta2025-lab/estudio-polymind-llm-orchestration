"""Explicit real-browser acceptance runner (not part of default pytest collection).

Requires the optional Playwright harness and Chromium; starts only loopback
services with a fresh synthetic authority set. No mocks of st.user or HTTP.
Run: python -m tests.browser.document_journey
"""
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
from urllib.parse import urlsplit


def run():
    os.environ["DOCUMENTS_PROFILE"] = "synthetic"
    from development.document_demo.provision import provision
    from development.document_demo.runtime import build
    from playwright.sync_api import sync_playwright
    parent = Path(tempfile.mkdtemp(prefix="polymind-browser-"))
    root = provision(parent / "runtime")
    build(root, initialize=True)
    repo = Path(__file__).resolve().parents[2]
    env = {**os.environ, "PYTHONPATH": str(repo) + os.pathsep + os.environ.get("PYTHONPATH", "")}
    stream = (parent / "runtime.log").open("w")
    process = subprocess.Popen([sys.executable, "-m", "development.document_demo", "serve", str(root)],
                               env=env, stdout=stream, stderr=subprocess.STDOUT)
    evidence = {"auth": False, "complete_journey": False, "browser_isolation": False,
                "cancel": False, "external_browser_requests": 0}
    try:
        for port in (9443, 9444, 8501, 8001):
            for _ in range(150):
                if process.poll() is not None:
                    raise RuntimeError("Local service failed; inspect " + str(parent / "runtime.log"))
                try:
                    with socket.create_connection(("localhost", port), timeout=.2):
                        break
                except OSError:
                    time.sleep(.1)
            else:
                raise RuntimeError("Local service startup timeout")
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context(ignore_https_errors=True)
            def network(request):
                if urlsplit(request.url).hostname not in {"localhost", "127.0.0.1", None}:
                    evidence["external_browser_requests"] += 1
            context.on("request", network)
            page = context.new_page()
            page.goto("https://localhost:9443")
            page.get_by_role("button", name="Log in", exact=True).click()
            page.get_by_text("Verified enrolled operator", exact=True).wait_for()
            cookies = context.cookies()
            auth = [c for c in cookies if c["name"].startswith("_streamlit_user")]
            assert len(auth) == 2 and all(c["secure"] and c["httpOnly"] and c["sameSite"] == "Lax" for c in auth)
            evidence["auth"] = True
            assert context.request.get("https://localhost:9443/auth/logout",
                headers={"Origin": "https://foreign.invalid"}).status == 403
            isolated = browser.new_context(ignore_https_errors=True)
            other = isolated.new_page()
            other.goto("https://localhost:9443")
            other.get_by_role("button", name="Log in", exact=True).wait_for()
            assert not other.get_by_text("Verified enrolled operator", exact=True).count()
            evidence["browser_isolation"] = True
            # Arbitrary callback state cannot install a login in a clean context.
            other.goto("https://localhost:9443/oauth2callback?code=invalid&state=unbound")
            other.get_by_role("button", name="Log in", exact=True).wait_for()
            assert not [c for c in isolated.cookies() if c["name"].startswith("_streamlit_user")]
            isolated.close()
            print("OIDC callback, API operator, Secure cookies, state rejection and isolation verified", flush=True)
            page.get_by_role("button", name="Create session", exact=True).click()
            page.get_by_role("button", name="Start durable job", exact=True).click()
            page.get_by_role("button", name="Authorize publication", exact=True).wait_for(timeout=280000)
            page.get_by_role("button", name="Authorize publication", exact=True).click()
            page.get_by_text("Complete document digest", exact=True).wait_for()
            page.get_by_role("textbox", name="Question about the selected document", exact=True).fill("What valve inspection is required?")
            page.get_by_role("button", name="Ask bounded question", exact=True).click()
            # Answer lives in a freshly authorized presentation packet on rerender.
            page.get_by_text('"evidence_status":"available"', exact=False).first.wait_for(timeout=15000)
            assert "document_version_id" in page.inner_text("body")
            assert "not_evaluated" in page.inner_text("body")
            page.get_by_role("button", name="Withdraw session", exact=True).click()
            page.get_by_text('"retention":"PURGE_PENDING"', exact=False).first.wait_for()
            evidence["complete_journey"] = True
            page.get_by_role("button", name="Log out", exact=True).click()
            page.get_by_role("button", name="Log in", exact=True).wait_for()
            assert not [c for c in context.cookies() if c["name"].startswith("_streamlit_user")]
            page.get_by_role("button", name="Log in", exact=True).click()
            page.get_by_text("Verified enrolled operator", exact=True).wait_for()
            page.get_by_role("button", name="Create session", exact=True).click()
            page.get_by_role("button", name="Start durable job", exact=True).click()
            page.get_by_role("button", name="Cancel processing", exact=True).click()
            page.get_by_text('"may_complete_and_bill":true', exact=False).first.wait_for()
            page.get_by_role("button", name="Close session", exact=True).click()
            evidence["cancel"] = True
            page.get_by_role("button", name="Log out", exact=True).click()
            page.get_by_role("button", name="Log in", exact=True).wait_for()
            browser.close()
        assert evidence["external_browser_requests"] == 0
        print(json.dumps(evidence), flush=True)
        (parent / "acceptance.json").write_text(json.dumps(evidence))
        print("Runtime evidence directory: " + str(parent), flush=True)
    finally:
        process.terminate()
        try:
            process.wait(timeout=80)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        stream.close()


if __name__ == "__main__":
    run()
