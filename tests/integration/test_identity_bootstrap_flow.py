"""Real loopback TLS/native startup and synthetic identity-to-evidence integration."""

import asyncio
import json
import os
import ssl
import subprocess
import sys

import pytest
from aiohttp import ClientSession, TCPConnector, WSServerHandshakeError, web
from aiohttp.abc import AbstractResolver

from deployment.phase19.identity_bootstrap import __main__ as launch
from deployment.phase19.identity_bootstrap import core

pytest_plugins = ["tests.identity_bootstrap_fixtures"]


def test_real_bootstrap_tls_callback_websocket_and_shutdown(private_tree):
    session, evidence, _ = private_tree
    context = launch.preflight(session, evidence)

    class Resolver(AbstractResolver):
        async def resolve(self, host, port=0, family=0):
            return [
                dict(
                    hostname=host,
                    host="127.0.0.1",
                    port=port,
                    family=family,
                    proto=0,
                    flags=0,
                )
            ]

        async def close(self):
            pass

    async def run():
        seen = []

        async def callback(request):
            seen.append(dict(request.headers))
            return web.Response(
                text="synthetic callback",
                headers={"Set-Cookie": "synthetic=value; HttpOnly; SameSite=Lax"},
            )

        async def echo(request):
            ws = web.WebSocketResponse()
            await ws.prepare(request)
            async for message in ws:
                await ws.send_str(message.data)
            return ws

        upstream = web.Application()
        upstream.router.add_get("/oauth2callback", callback)
        upstream.router.add_get("/socket", echo)
        backend = web.AppRunner(upstream)
        await backend.setup()
        site = web.TCPSite(backend, "127.0.0.1", 0)
        await site.start()
        upstream_port = site._server.sockets[0].getsockname()[1]
        runner = web.AppRunner(
            launch.gateway(f"http://127.0.0.1:{upstream_port}", core.ORIGIN),
            access_log=None,
        )
        listener = launch.reserve(0)
        port = listener.getsockname()[1]
        try:
            with pytest.raises(OSError):
                launch.reserve(port)
            assert listener.getsockname()[0] == "127.0.0.1"
            await runner.setup()
            await web.SockSite(runner, listener, ssl_context=context).start()
            trusted = ssl.create_default_context(cafile=str(session / "tls.crt"))
            async with ClientSession(
                connector=TCPConnector(ssl=trusted, resolver=Resolver()),
                trust_env=False,
            ) as client:
                url = f"https://polymind.test:{port}"
                headers = {"Host": "polymind.test:9443", "Origin": core.ORIGIN}
                async with client.get(
                    url + "/oauth2callback?code=synthetic&state=synthetic",
                    headers=headers,
                ) as response:
                    assert (
                        response.status == 200
                        and await response.text() == "synthetic callback"
                    )
                    assert "Secure" in response.headers["Set-Cookie"]
                    assert response.headers["Cache-Control"] == "no-store"
                assert (
                    seen[0]["Host"] == headers["Host"]
                    and seen[0]["X-Forwarded-Proto"] == "https"
                )
                for changes in (
                    {"Host": "foreign.test:9443"},
                    {"Host": "polymind.test"},
                    {"Origin": "https://foreign.test"},
                ):
                    async with client.get(
                        url + "/oauth2callback", headers=headers | changes
                    ) as response:
                        assert response.status == 403
                for origin in (None, "https://foreign.test"):
                    supplied = {"Host": headers["Host"]}
                    if origin:
                        supplied["Origin"] = origin
                    with pytest.raises(WSServerHandshakeError):
                        await client.ws_connect(url + "/socket", headers=supplied)
                async with client.ws_connect(url + "/socket", headers=headers) as ws:
                    await ws.send_str("synthetic")
                    assert (await ws.receive(timeout=3)).data == "synthetic"
                await backend.cleanup()
                async with client.get(
                    url + "/oauth2callback", headers=headers
                ) as response:
                    assert response.status == 503
            with pytest.raises(ssl.SSLCertVerificationError):
                await asyncio.open_connection(
                    "127.0.0.1", port, ssl=trusted, server_hostname="wrong.invalid"
                )
        finally:
            await runner.cleanup()
            await backend.cleanup()
            listener.close()
        # Port release means a new bind is possible after cleanup.
        with launch.reserve(port):
            pass

    asyncio.run(run())


def test_synthetic_end_to_end_with_forbidden_import_connection_and_write_guards(
    private_tree, bootstrap_identity
):
    session, evidence, _ = private_tree
    verifier, token = bootstrap_identity
    payload = dict(
        token=token(), jwks=verifier.verifier.fetch(), evidence=str(evidence)
    )
    code = r"""
import importlib.abc, json, os, pathlib, socket, sqlite3, stat, sys
payload = json.load(sys.stdin)
forbidden = ('api','config.settings','llm','rag','memory','governance','redis','chromadb',
 'security.runtime','security.authority','security.execution','security.chat','documents.operator',
 'documents.jobs.sqlite','documents.pilot','documents.publication','deployment.phase19.runtime')
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self, fullname, path, target=None):
  if any(fullname == p or fullname.startswith(p+'.') for p in forbidden):
   raise AssertionError('Forbidden runtime import')
sys.meta_path.insert(0,Deny())
def deny(*a,**k): raise AssertionError('Network/database forbidden')
sqlite3.connect = socket.socket.connect = socket.socket.connect_ex = socket.getaddrinfo = deny
from deployment.phase19.identity_bootstrap import core, files, ui, __main__
assert not any(any(n == p or n.startswith(p+'.') for p in forbidden) for n in sys.modules)
original = files.ancestor
tmp = pathlib.Path('/tmp').stat()
def ancestor(info):
 if (info.st_dev,info.st_ino) == (tmp.st_dev,tmp.st_ino): return
 original(info)
files.ancestor = ancestor
evidence = pathlib.Path(payload['evidence'])
def audit(event,args):
 if event == 'open' and isinstance(args[0],str):
  flags = args[2]
  if flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT):
   # export writes descriptor-relative fixed pending name only
   assert args[0] == files.PENDING
sys.addaudithook(audit)
v = core.BootstrapVerifier(fetch=lambda:payload['jwks'])
try: files.export('invalid',v,evidence,authorized=True)
except Exception: pass
assert not list(evidence.iterdir())
class State(dict): pass
class UI:
 def __init__(self):
  from types import SimpleNamespace
  self.user = SimpleNamespace(is_logged_in=True,tokens={'access':payload['token'],'id':'never-selected'})
  self.secrets = SimpleNamespace(to_dict=lambda:json.loads(os.environ['SYNTHETIC_AUTH']))
  self.session_state = State()
  self.logout_selected = False
  self.signed_out = False
 def button(self,label,**kwargs): return self.logout_selected if label.startswith('Log out') else label.startswith('Export')
 def checkbox(self,*a): return True
 def logout(self): self.signed_out = True
 def __getattr__(self,name):
  if name == 'error': return lambda *a: (_ for _ in ()).throw(AssertionError('Unexpected UI error'))
  return lambda *a,**k: None
screen = UI()
ui.render(screen,v,evidence)
assert screen.session_state['exported'] is True
artifact = json.loads((evidence/files.NAME).read_text())
p = v.verify(payload['token'])
assert artifact['subject'] == p.subject and artifact['issuer'] == p.issuer
assert artifact['tenant_id'] == p.tenant_identity
assert artifact['canonical_owner_id'] == str(p.scope.owner)
assert artifact['canonical_tenant_id'] == str(p.scope.tenant)
assert payload['token'] not in json.dumps(artifact) and artifact['execution_authorized'] is False
assert (evidence/files.NAME).stat().st_nlink == 1
screen.logout_selected = True
ui.render(screen,v,evidence)
assert screen.signed_out and not screen.session_state
print('SYNTHETIC_END_TO_END: PASS; FORBIDDEN_IMPORTS: 0; AUTHORITY_WRITES: 0; PROVIDER_CALLS: 0')
"""
    env = launch.environment(session, evidence)
    env["SYNTHETIC_AUTH"] = json.dumps({"auth": private_tree[2]})
    # Preserve test-only offline guard for the subprocess; no operational configuration.
    if "PYTHONPATH" in os.environ:
        env["PYTHONPATH"] = os.environ["PYTHONPATH"]
    result = subprocess.run(
        [sys.executable, "-c", code],
        input=json.dumps(payload),
        text=True,
        env=env,
        cwd=session,
        capture_output=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
    assert "SYNTHETIC_END_TO_END: PASS" in result.stdout
    assert list(session.iterdir()) and len(list(evidence.iterdir())) == 1


@pytest.mark.parametrize("pythonpath_present", [False, True], ids=["absent", "present"])
def test_native_worker_flags_and_real_loopback_start_stop(
    private_tree, monkeypatch, pythonpath_present
):
    """No browser/auth request. Start pinned Streamlit, check health, terminate siblings."""
    session, evidence, _ = private_tree
    if pythonpath_present:
        configured_path = os.environ.get(
            "PYTHONPATH", os.pathsep.join((str(launch.REPO), str(session)))
        )
        monkeypatch.setenv("PYTHONPATH", configured_path)
    else:
        monkeypatch.delenv("PYTHONPATH", raising=False)
    # child uses its actual native interfaces, not a fake HTTP server
    monkeypatch.setattr(launch, "WINDOW_SECONDS", 0.5)
    original = launch.environment

    def env(root, destination):
        value = original(root, destination)
        # Synthetic guard only; launcher never inherits arbitrary PYTHONPATH operationally.
        if "PYTHONPATH" in os.environ:
            value["PYTHONPATH"] = os.environ["PYTHONPATH"]
        assert value["PYTHONPATH"] == (
            configured_path if pythonpath_present else str(launch.REPO)
        )
        return value

    monkeypatch.setattr(launch, "environment", env)
    asyncio.run(
        launch.supervise(session, evidence, launch.preflight(session, evidence))
    )
    with launch.reserve(9443), launch.reserve(launch.UI_PORT):
        pass
    assert not list(evidence.iterdir())
