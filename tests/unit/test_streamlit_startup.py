"""Run the real Streamlit script in fresh interpreters, before backend imports.

Pytest collection imports the backend first and normally hides this collision.
AppTest uses Streamlit's ScriptRunner; explicitly include the CLI bootstrap's
script-directory precedence as well (AppTest does not run the CLI bootstrap).
"""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]


def run_python(code, cwd, **settings):
    # Never inherit operator credentials or consult the repository's real dotenv.
    env = {k: os.environ[k] for k in ("PATH", "SYSTEMROOT", "LD_LIBRARY_PATH") if k in os.environ}
    env.update(PYTHONPATH=str(ROOT), PYTHONDONTWRITEBYTECODE="1",
               STREAMLIT_BROWSER_GATHER_USAGE_STATS="false", **settings)
    result = subprocess.run([sys.executable, "-c", code], cwd=cwd, env=env,
                            capture_output=True, text=True, timeout=40)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


def test_backend_package_with_streamlit_path_precedence(tmp_path):
    run_python(f"""
import importlib.util
import sys
from pathlib import Path
root = Path({str(ROOT)!r})
sys.path.insert(0, str(root / 'ui'))
spec = importlib.util.find_spec('documents')
assert Path(spec.origin) == root / 'documents' / '__init__.py', spec.origin
assert spec.submodule_search_locations is not None
from documents.models import FrozenModel
from security.identity import OIDCSettings
assert FrozenModel.__module__ == 'documents.models'
""", tmp_path)


@pytest.mark.parametrize("profile", ["legacy", "synthetic"])
def test_real_streamlit_script_in_clean_process(tmp_path, profile):
    if profile == "legacy":
        # Exercise the exact settings -> security.identity -> documents edge.
        # These are synthetic config values; no runtime authority is opened.
        from tests.unit.test_security_configuration import configured
        configuration = configured(tmp_path)
        configuration.pop("_env_file")
        lines = []
        for name, value in configuration.items():
            if value is not None:
                encoded = json.dumps(value) if not isinstance(value, str) else value
                lines.append(name + "=" + json.dumps(encoded))
        (tmp_path / ".env").write_text("\n".join(lines))
        assets = tmp_path / "ui" / "assets"
        assets.mkdir(parents=True)
        (assets / "susanta.png").write_bytes((ROOT / "ui/assets/susanta.png").read_bytes())
    run_python(f"""
import sys
from contextlib import nullcontext
from types import SimpleNamespace
from unittest.mock import patch
import streamlit as st
from streamlit.testing.v1 import AppTest
sys.path.insert(0, {str(ROOT / 'ui')!r})
# AppTest's default user_info has only email, with no native login state.
# This checks the logged-out view; actual OIDC is a separate browser journey.
user = patch.object(st, 'user', SimpleNamespace(is_logged_in=False)) if {profile!r} == 'synthetic' else nullcontext()
with user:
    app = AppTest.from_file({str(ROOT / 'ui/app.py')!r}).run(timeout=20)
assert not app.exception, [e.message for e in app.exception]
from config.settings import settings
assert settings.DOCUMENTS_PROFILE == {profile!r}
if {profile!r} == 'legacy':
    assert settings.authentication_mode == 'oidc_jwt'
    assert len(app.chat_input) == 1
    assert app.chat_input[0].placeholder == 'Ask anything...'
else:
    from ui.documents_view import render
    assert render.__module__ == 'ui.documents_view'
    assert app.title[0].value == 'Documents'
    assert [b.label for b in app.button] == ['Log in']
    assert not app.chat_input
""", tmp_path, DOCUMENTS_PROFILE=profile)
