"""Bootstrap-specific trust, export, lifecycle and native Streamlit UI boundaries."""

import json
import os
import stat
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace

import pytest
import streamlit as st
from cryptography.hazmat.primitives.asymmetric import rsa
from streamlit.testing.v1 import AppTest

from deployment.phase19.identity_bootstrap import __main__ as launch
from deployment.phase19.identity_bootstrap import core, files
from documents.models import stable_id
from security.models import SecurityError

pytest_plugins = ["tests.identity_bootstrap_fixtures"]


@pytest.mark.parametrize(
    "change",
    [
        {"iss": "https://untrusted.invalid"},
        {"tid": core.API_CLIENT},
        {"aud": core.BROWSER_CLIENT},
        {"aud": "00000003-0000-0000-c000-000000000000"},
        {"aud": [core.API_CLIENT]},
        {"ver": "1.0"},
        {"exp": 1},
        {"nbf": 4102444800},
        {"sub": None},
        {"sub": {}},
        {"scp": None},
        {"scp": "openid"},
        {"roles": None},
        {"roles": ["other"]},
        {"roles": ["PolyMind.L1Operator", "extra"]},
        {"idtyp": "app"},
        {"token_use": "id"},
        {"azp": None},
        {"azp": core.API_CLIENT},
        {"azp": []},
        {"iat": True},
        {"exp": "4102444800"},
        {"nbf": False},
        {"roles": "PolyMind.L1Operator"},
    ],
)
def test_access_token_denial(bootstrap_identity, change):
    verifier, token = bootstrap_identity
    with pytest.raises(SecurityError, match="^authentication_required$"):
        verifier.verify(token(change))


@pytest.mark.parametrize("value", [None, "", "a.b.c", "not-a-jwt", "x" * 16385])
def test_missing_or_malformed_token(bootstrap_identity, value):
    with pytest.raises(SecurityError):
        bootstrap_identity[0].verify(value)


def test_signature_key_algorithm_and_jwks_failures(bootstrap_identity):
    verifier, token = bootstrap_identity
    for value in [
        token(
            signing_key=rsa.generate_private_key(public_exponent=65537, key_size=2048)
        ),
        token(kid="unknown"),
        token(algorithm="HS256", signing_key="synthetic-secret-" * 3),
    ]:
        with pytest.raises(SecurityError):
            verifier.verify(value)

    def failed():
        raise OSError("sensitive transport detail")

    verifier.verifier._loaded = None
    verifier.verifier._attempted = None
    verifier.verifier.fetch = failed
    with pytest.raises(SecurityError, match="^authentication_required$"):
        verifier.verify(token())


def test_identity_exactly_matches_production_domains(bootstrap_identity):
    verifier, token = bootstrap_identity
    p = verifier.verify(token())
    assert p.scope.tenant == stable_id(
        "polymind-identity/1/tenant", p.issuer, p.tenant_identity
    )
    assert p.scope.owner == stable_id(
        "polymind-identity/1/owner", p.issuer, p.tenant_identity, p.subject
    )
    assert (
        verifier.verify(
            token({"oid": "another-object", "id_token": "different-id-token-sub"})
        ).scope
        == p.scope
    )
    assert verifier.verify(token({"sub": "other-subject"})).scope.owner != p.scope.owner
    assert (
        stable_id("polymind-identity/1/tenant", p.issuer, "other-tenant")
        != p.scope.tenant
    )
    assert verifier.verify(token()).scope == p.scope


def test_export_schema_permissions_and_fresh_verification(
    bootstrap_identity, private_tree, monkeypatch
):
    verifier, token = bootstrap_identity
    _, evidence, _ = private_tree
    encoded = token()
    calls = []
    original = verifier.verify

    def verify(value):
        calls.append(value)
        return original(value)

    monkeypatch.setattr(verifier, "verify", verify)
    exported = files.export(encoded, verifier, evidence, authorized=True)
    path = evidence / files.NAME
    assert calls == [encoded]
    assert json.loads(path.read_text()) == exported
    assert set(exported) == {
        "schema_version",
        "purpose",
        "issuer",
        "tenant_id",
        "subject",
        "canonical_tenant_id",
        "canonical_owner_id",
        "api_audience",
        "verified_at_utc",
        "token_expires_at_utc",
        "execution_authorized",
    }
    assert exported["execution_authorized"] is False
    assert exported["subject"] == "synthetic-api-subject"
    assert (
        encoded not in path.read_text()
        and "unused-directory-object" not in path.read_text()
    )
    assert stat.S_IMODE(path.stat().st_mode) == 0o600 and path.stat().st_nlink == 1
    assert (
        path.stat().st_uid == os.geteuid()
        and stat.S_IMODE(evidence.stat().st_mode) == 0o700
    )
    with pytest.raises(FileExistsError):
        files.export(encoded, verifier, evidence, authorized=True)
    assert json.loads(path.read_text()) == exported


@pytest.mark.parametrize("authorized", [False, None, 1, "yes"])
def test_explicit_operator_action_required(
    bootstrap_identity, private_tree, authorized
):
    with pytest.raises(SecurityError):
        files.export(
            bootstrap_identity[1](),
            bootstrap_identity[0],
            private_tree[1],
            authorized=authorized,
        )
    assert not list(private_tree[1].iterdir())


def test_expired_after_initial_verification(
    bootstrap_identity, private_tree, monkeypatch
):
    verifier, token = bootstrap_identity
    verifier.verify(token())
    with pytest.raises(SecurityError):
        files.export(token({"exp": 1}), verifier, private_tree[1], authorized=True)
    assert not list(private_tree[1].iterdir())


@pytest.mark.parametrize(
    "fault", ["symlink", "hardlink", "directory", "fifo", "existing", "pending"]
)
def test_unsafe_or_existing_artifact_refused(bootstrap_identity, private_tree, fault):
    _, evidence, _ = private_tree
    path = evidence / files.NAME
    target = evidence / "unrelated"
    target.write_text("preserve")
    if fault == "symlink":
        path.symlink_to(target)
    if fault == "hardlink":
        os.link(target, path)
    if fault == "directory":
        path.mkdir()
    if fault == "fifo":
        os.mkfifo(path)
    if fault == "existing":
        path.write_text("existing")
    if fault == "pending":
        (evidence / files.PENDING).write_text("interrupted")
    with pytest.raises(OSError):
        files.export(
            bootstrap_identity[1](), bootstrap_identity[0], evidence, authorized=True
        )
    assert target.read_text() == "preserve"


@pytest.mark.parametrize(
    "fault",
    ["public", "symlink", "ancestor", "relative", "repository", "windows", "owner"],
)
def test_unsafe_destination_denied(
    bootstrap_identity, private_tree, monkeypatch, fault
):
    session, evidence, _ = private_tree
    destination = evidence
    if fault == "public":
        evidence.chmod(0o755)
    if fault == "ancestor":
        evidence.parent.chmod(0o777)
    if fault == "symlink":
        destination = session / "link"
        destination.symlink_to(evidence, target_is_directory=True)
    if fault == "relative":
        destination = Path("relative")
    if fault == "repository":
        destination = files.REPO
    if fault == "windows":
        destination = Path("/mnt/c/shared")
    if fault == "owner":
        monkeypatch.setattr(files.os, "geteuid", lambda: 12345)
    with pytest.raises((OSError, ValueError)):
        files.export(
            bootstrap_identity[1](), bootstrap_identity[0], destination, authorized=True
        )
    assert not (evidence / files.NAME).exists()


def test_shared_tmp_ancestor_rejected_without_test_adapter(tmp_path):
    with pytest.raises(ValueError, match="Unsafe ancestor"):
        with files.directory(tmp_path):
            pytest.fail("Shared temporary path accepted")


@pytest.mark.parametrize("failure", [OSError, KeyboardInterrupt])
def test_partial_write_or_interruption_never_publishes(
    bootstrap_identity, private_tree, monkeypatch, failure
):
    def failed(*args):
        raise failure("synthetic failure")

    monkeypatch.setattr(files.os, "fsync", failed)
    with pytest.raises(failure):
        files.export(
            bootstrap_identity[1](),
            bootstrap_identity[0],
            private_tree[1],
            authorized=True,
        )
    assert not list(private_tree[1].iterdir())


def test_concurrent_export_has_one_winner(bootstrap_identity, private_tree):
    verifier, token = bootstrap_identity
    encoded = token()

    def attempt(_):
        try:
            files.export(encoded, verifier, private_tree[1], authorized=True)
            return True
        except FileExistsError:
            return False

    with ThreadPoolExecutor(max_workers=6) as pool:
        assert sum(pool.map(attempt, range(12))) == 1
    assert len(list(private_tree[1].iterdir())) == 1


@pytest.mark.parametrize(
    "fault",
    ["missing", "placeholder", "callback", "scope", "id", "extra", "cookie", "client"],
)
def test_configuration_fail_closed(private_tree, fault):
    auth = private_tree[2].copy()
    if fault == "missing":
        auth.pop("client_secret")
    if fault == "placeholder":
        auth["client_secret"] = "<SUPPLIED_PRIVATELY_BY_CUSTODIAN>"
    if fault == "callback":
        auth["redirect_uri"] = "https://attacker.invalid/oauth2callback"
    if fault == "scope":
        auth["client_kwargs"] = {
            "scope": "openid profile https://graph.microsoft.com/User.Read"
        }
    if fault == "id":
        auth["expose_tokens"] = ["id", "access"]
    if fault == "extra":
        auth["other_provider"] = {}
    if fault == "cookie":
        auth["cookie_secret"] = "weak"
    if fault == "client":
        auth["client_id"] = core.API_CLIENT
    with pytest.raises(SecurityError, match="^security_configuration$"):
        core.validate_auth({"auth": auth})


@pytest.mark.parametrize(
    "fault", ["tls.crt", "tls.key", "public", "mismatch", "extra", "state"]
)
def test_preflight_tls_and_directory_failures(private_tree, fault):
    session, evidence, _ = private_tree
    if fault in {"tls.crt", "tls.key"}:
        (session / fault).unlink()
    if fault == "public":
        (session / "tls.key").chmod(0o644)
    if fault == "mismatch":
        (session / "tls.key").write_text("invalid synthetic key")
    if fault == "extra":
        (session / ".env").write_text("PROVIDER=forbidden")
    if fault == "state":
        (evidence / "security.sqlite").write_text("do not touch")
    with pytest.raises((ValueError, OSError)):
        launch.preflight(session, evidence)


def test_preflight_and_child_environment_are_nonoperational(private_tree, monkeypatch):
    session, evidence, _ = private_tree
    monkeypatch.setenv("OPENAI_API_KEY", "never-inherit")
    monkeypatch.setenv("HTTP_PROXY", "never-inherit")
    context = launch.preflight(session, evidence)
    import ssl

    assert context.minimum_version == ssl.TLSVersion.TLSv1_2
    env = launch.environment(session, evidence)
    assert "OPENAI_API_KEY" not in env and "HTTP_PROXY" not in env
    assert env["HOME"] == str(session) and "DEPLOYMENT_ENV" not in env


@pytest.fixture
def frontend(bootstrap_identity, private_tree, monkeypatch):
    from deployment.phase19.identity_bootstrap import ui

    st.cache_resource.clear()
    verifier, token = bootstrap_identity
    monkeypatch.setattr(
        st,
        "user",
        SimpleNamespace(
            is_logged_in=True, tokens={"access": token(), "id": "never-use"}
        ),
    )
    monkeypatch.setattr(
        st, "secrets", SimpleNamespace(to_dict=lambda: {"auth": private_tree[2]})
    )
    monkeypatch.setattr(ui, "BootstrapVerifier", lambda: verifier)
    monkeypatch.setenv("POLYMIND_BOOTSTRAP_EVIDENCE", str(private_tree[1]))
    app = AppTest.from_string(
        "import os, streamlit as st\n"
        "from deployment.phase19.identity_bootstrap.ui import render, BootstrapVerifier\n"
        'render(st, BootstrapVerifier(), os.environ["POLYMIND_BOOTSTRAP_EVIDENCE"])'
    ).run()
    assert not app.exception
    return app, private_tree[1]


def test_native_ui_explicit_export_reruns_and_no_disclosure(frontend):
    app, evidence = frontend
    assert app.button[1].disabled and not (evidence / files.NAME).exists()
    app.checkbox[0].check().run()
    app.button[1].click().run()
    assert (evidence / files.NAME).is_file() and not app.exception
    before = (evidence / files.NAME).read_bytes()
    app.run()
    assert (evidence / files.NAME).read_bytes() == before
    output = " ".join(
        str(item.value)
        for group in (app.info, app.success, app.error, app.caption)
        for item in group
    )
    for value in ("synthetic-api-subject", "unused-directory-object", "never-use"):
        assert value not in output
    app.button[1].click().run()
    assert app.error and (evidence / files.NAME).read_bytes() == before


@pytest.mark.parametrize(
    "state",
    ["anonymous", "missing_access", "id_only", "expired", "invalid_config", "logout"],
)
def test_native_ui_failure_and_logout(frontend, bootstrap_identity, monkeypatch, state):
    app, evidence = frontend
    actions = []
    monkeypatch.setattr(st, "login", lambda: actions.append("login"))
    monkeypatch.setattr(st, "logout", lambda: actions.append("logout"))
    if state == "anonymous":
        monkeypatch.setattr(st, "user", SimpleNamespace(is_logged_in=False))
    if state == "missing_access":
        monkeypatch.setattr(st, "user", SimpleNamespace(is_logged_in=True, tokens={}))
    if state == "id_only":
        monkeypatch.setattr(
            st,
            "user",
            SimpleNamespace(is_logged_in=True, tokens={"id": bootstrap_identity[1]()}),
        )
    if state == "expired":
        monkeypatch.setattr(
            st,
            "user",
            SimpleNamespace(
                is_logged_in=True, tokens={"access": bootstrap_identity[1]({"exp": 1})}
            ),
        )
    if state == "invalid_config":
        monkeypatch.setattr(st, "secrets", SimpleNamespace(to_dict=lambda: {}))
    if state == "logout":
        app.button[0].click().run()
    else:
        app.run()
    if state == "anonymous":
        app.button[1].click().run()
        assert actions == ["login"]
    elif state == "logout":
        assert actions == ["logout"]
    else:
        assert app.error
    assert not list(evidence.iterdir()) and not app.exception


def test_production_scope_expression_matches_without_importing_runtime(
    bootstrap_identity,
):
    import ast

    from documents.models import Scope

    source = files.REPO / "deployment/phase19/runtime.py"
    tree = ast.parse(source.read_text())
    build = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "build"
    )
    expression = next(
        node.value
        for node in build.body
        if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "scope" for t in node.targets)
    )
    p = bootstrap_identity[0].verify(bootstrap_identity[1]())
    scope = eval(
        compile(ast.Expression(expression), str(source), "eval"),
        {
            "Scope": Scope,
            "stable_id": stable_id,
            "issuer": p.issuer,
            "tenant": p.tenant_identity,
            "subject": p.subject,
            "__builtins__": {},
        },
    )
    assert scope == p.scope


@pytest.mark.parametrize(
    "fault", ["symlink", "hardlink", "fifo", "directory", "public", "oversized"]
)
def test_private_credential_read_refuses_unsafe_files(private_tree, fault):
    session, _, _ = private_tree
    path = session / "synthetic-input"
    if fault == "symlink":
        path.symlink_to(session / "tls.key")
    elif fault == "hardlink":
        os.link(session / "tls.key", path)
    elif fault == "fifo":
        os.mkfifo(path, 0o600)
    elif fault == "directory":
        path.mkdir(mode=0o700)
    else:
        path.write_text("x" * 65537 if fault == "oversized" else "synthetic")
        path.chmod(0o644 if fault == "public" else 0o600)
    with pytest.raises((ValueError, OSError)):
        files.read_private(path)


def test_same_token_expiry_between_display_and_export(
    bootstrap_identity, private_tree, monkeypatch
):
    from datetime import datetime, timedelta, timezone

    import jwt

    v, sign = bootstrap_identity
    token = sign()
    v.verify(token)

    class FutureDatetime:
        @classmethod
        def now(cls, tz=None):
            return datetime.now(timezone.utc) + timedelta(hours=2)

    monkeypatch.setattr(jwt.api_jwt, "datetime", FutureDatetime)
    with pytest.raises(SecurityError):
        files.export(token, v, private_tree[1], authorized=True)
    assert not list(private_tree[1].iterdir())


def test_identity_change_clears_previous_export_status(
    frontend, bootstrap_identity, monkeypatch
):
    app, evidence = frontend
    app.checkbox[0].check().run()
    app.button[1].click().run()
    assert any("PROTECTED_EVIDENCE_EXPORT: PASS" in s.value for s in app.success)
    token = bootstrap_identity[1]({"sub": "different-session-owner"})
    monkeypatch.setattr(
        st, "user", SimpleNamespace(is_logged_in=True, tokens={"access": token})
    )
    app.run()
    assert not any("PROTECTED_EVIDENCE_EXPORT: PASS" in s.value for s in app.success)
    assert (evidence / files.NAME).is_file()
