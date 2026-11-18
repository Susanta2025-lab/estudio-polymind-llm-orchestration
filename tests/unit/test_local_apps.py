"""Local startup contracts, tested without live inference or operator authorities."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

import pytest

from development import local_apps as launch


@pytest.fixture
def chat_root(tmp_path, monkeypatch):
    root = tmp_path / "chat"
    monkeypatch.setenv("CHAT_RUNTIME", str(root))
    for name in ("CHAT_CHROMA_PATH", "CHAT_CORPUS_VERSION", "CHAT_HF_HOME", "CHAT_MODEL_ARTIFACT_DIR"):
        monkeypatch.delenv(name, raising=False)
    return root


def test_real_settings_exclude_repository_dotenv_and_hostile_shell(chat_root, tmp_path, monkeypatch):
    # A fake repository dotenv reproduces the governed-root problem without
    # reading, changing or copying the operator's actual secret configuration.
    repo = tmp_path / "repo"
    (repo / "config").mkdir(parents=True)
    (repo / "config/settings.py").write_bytes((launch.REPO / "config/settings.py").read_bytes())
    (repo / "config/__init__.py").touch()
    (repo / ".env").write_text("DEPLOYMENT_ENV=production\nINFERENCE_PROVIDER=openai_compatible\n"
                               "MEMORY_HISTORY=99\nAPI_AUTH_MODE=oidc_jwt\n")
    monkeypatch.setattr(launch, "REPO", repo)
    for name in ("OPENAI_COMPATIBLE_API_KEY", "AZURE_TOKEN", "HTTPS_PROXY", "OIDC_CONFIGURATION",
                 "GOVERNANCE_PRICING", "API_AUTH_TOKEN", "PYTHONPATH"):
        monkeypatch.setenv(name, "hostile-synthetic-value")
    monkeypatch.setenv("INFERENCE_PROVIDER", "openai_compatible")
    monkeypatch.setenv("MEMORY_HISTORY", "88")
    cwd, env = launch.chat_environment()
    assert not any(name in env for name in ("OPENAI_COMPATIBLE_API_KEY", "AZURE_TOKEN", "HTTPS_PROXY",
                                            "OIDC_CONFIGURATION", "GOVERNANCE_PRICING", "API_AUTH_TOKEN"))
    result = subprocess.run([sys.executable, "-c", """
import json
from config.settings import settings as s
assert s.DEPLOYMENT_ENV == 'local' and s.DOCUMENTS_PROFILE == 'legacy'
assert s.INFERENCE_PROVIDER == 'ollama' and s.OPENAI_COMPATIBLE_API_KEY is None
assert s.authentication_mode == 'disabled' and not s.GOVERNANCE_ENABLED
assert s.OIDC_CONFIGURATION is None and s.MEMORY_HISTORY == 6
assert s.MEMORY_PROVIDER == 'file' and s.VECTOR_STORE_PROVIDER == 'chroma_local'
assert s.STREAM_URL == 'http://127.0.0.1:8001/query/stream'
assert s.MODEL_OFFLINE_MODE and s.OLLAMA_URL == 'http://127.0.0.1:11434/api/chat'
print(json.dumps(s.OLLAMA_MODEL_MAP))
"""], cwd=cwd, env=env, capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == launch.MODEL_MAP
    assert env["MEMORY_FILE"] == str(chat_root / "memory.json")
    assert env["CHROMA_PATH"] == str(chat_root / "chroma_db")


def test_real_chat_frontend_with_isolated_environment(chat_root):
    cwd, env = launch.chat_environment()
    result = subprocess.run([sys.executable, "-c", f"""
from streamlit.testing.v1 import AppTest
app = AppTest.from_file({str(launch.REPO / 'ui/app.py')!r}).run(timeout=20)
assert not app.exception, [e.message for e in app.exception]
assert len(app.chat_input) == 1
assert app.title[0].value == '🧠 Estudio PolyMind'
"""], cwd=cwd, env=env, capture_output=True, text=True, timeout=40)
    assert result.returncode == 0, result.stderr
    assert (cwd / "ui/assets/susanta.png").is_file()


@pytest.mark.parametrize("name", [".env", ".streamlit", "ui", "memory.json"])
def test_refuse_runtime_configuration_or_asset_conflicts(chat_root, name):
    chat_root.mkdir(mode=0o700)
    if name == "memory.json":
        (chat_root / name).symlink_to(chat_root / "absent-authority")
    else:
        (chat_root / name).touch()
    with pytest.raises(launch.LaunchError):
        launch.chat_environment()


def test_private_directory_and_repository_boundary(chat_root, monkeypatch):
    chat_root.mkdir(mode=0o755)
    # This rejection fixture must stay public even under an inherited 077 umask.
    chat_root.chmod(0o755)
    with pytest.raises(launch.LaunchError, match="private permissions"):
        launch.chat_environment()
    with pytest.raises(launch.LaunchError, match="outside"):
        launch.outside_repo(str(launch.REPO / "new-runtime"))


def test_explicit_local_artifacts_and_index(chat_root, tmp_path, monkeypatch):
    monkeypatch.setenv("CHAT_CHROMA_PATH", str(tmp_path / "index"))
    monkeypatch.setenv("CHAT_CORPUS_VERSION", "local-v1")
    monkeypatch.setenv("CHAT_HF_HOME", str(tmp_path / "cache"))
    monkeypatch.setenv("CHAT_MODEL_ARTIFACT_DIR", str(tmp_path / "models"))
    _, env = launch.chat_environment()
    assert env["CHROMA_PATH"] == str(tmp_path / "index")
    assert env["BM25_CORPUS_VERSION"] == "local-v1"
    assert env["HF_HOME"] == str(tmp_path / "cache")
    assert env["MODEL_ARTIFACT_DIR"] == str(tmp_path / "models")


def test_concurrent_asset_link_creation_is_safe(chat_root, monkeypatch):
    original = Path.symlink_to
    def simultaneous_link(path, target, **kwargs):
        original(path, target, **kwargs)
        raise FileExistsError("other launcher created the same link")
    monkeypatch.setattr(Path, "symlink_to", simultaneous_link)
    cwd, _ = launch.chat_environment()
    assert (cwd / "ui").resolve() == launch.REPO / "ui"


def test_missing_dependencies_in_real_empty_python_environment(tmp_path):
    environment = tmp_path / "empty-environment"
    subprocess.run([sys.executable, "-m", "venv", "--without-pip", str(environment)], check=True, timeout=30)
    result = subprocess.run(["make", "-s", "chat-api", f"PYTHON={environment / 'bin/python'}"],
                            cwd=launch.REPO, capture_output=True, text=True, timeout=15)
    assert result.returncode != 0
    assert "lacks: uvicorn, prometheus_client" in result.stderr
    assert str(environment / "bin/python") in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("target,module", [("api", "uvicorn"), ("ui", "streamlit")])
def test_historical_make_uses_selected_python_and_preserves_environment(tmp_path, target, module):
    # A deliberately broken standalone executable must never be selected.
    fake = tmp_path / module
    fake.write_text("#!/bin/sh\nexit 91\n")
    fake.chmod(0o755)
    selected = tmp_path / "selected-python"
    selected.write_text("#!/bin/sh\nprintf '%s\\n' \"$@\"\nprintf '%s\\n' \"$API_AUTH_MODE\"\n")
    selected.chmod(0o755)
    env = {**os.environ, "PATH": str(tmp_path) + os.pathsep + os.environ["PATH"], "API_AUTH_MODE": "oidc_jwt"}
    result = subprocess.run(["make", "--no-print-directory", "-s", target, f"PYTHON={selected}"],
                            cwd=launch.REPO, env=env, capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines()[:2] == ["-m", module]
    assert result.stdout.splitlines()[-1] == "oidc_jwt"


def test_make_help_and_recipes_from_another_working_directory(tmp_path):
    for target in ("api", "ui", "dev", "chat-api", "chat-ui", "chat-dev", "docs-init", "docs-serve"):
        result = subprocess.run(["make", "-n", "-f", str(launch.REPO / "Makefile"), target,
                                 f"PYTHON={sys.executable}"], cwd=tmp_path,
                                capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, result.stderr
        assert sys.executable in result.stdout
    help_result = subprocess.run(["make", "help"], cwd=launch.REPO, capture_output=True, text=True, timeout=10)
    for word in ("chat-api", "chat-ui", "chat-dev", "docs-init", "docs-serve", "DOCS_RUNTIME", "PYTHON"):
        assert word in help_result.stdout


def test_missing_dependency_reports_selected_interpreter(monkeypatch):
    monkeypatch.setattr(launch.importlib.util, "find_spec", lambda _: None)
    with pytest.raises(launch.LaunchError, match="lacks: uvicorn, prometheus_client") as error:
        launch.require_modules("uvicorn", "prometheus_client")
    assert sys.executable in str(error.value) and "PYTHON=" in str(error.value)


@pytest.mark.parametrize("target", ["chat-api", "chat-ui", "docs-init", "docs-serve"])
def test_production_environment_is_rejected(target, monkeypatch):
    monkeypatch.setenv("DEPLOYMENT_ENV", "production")
    monkeypatch.setattr(sys, "argv", ["local_apps", target])
    assert launch.main() == 2


@pytest.mark.parametrize("target", ["docs-init", "docs-serve"])
def test_documents_require_runtime(target, monkeypatch):
    monkeypatch.delenv("DEPLOYMENT_ENV", raising=False)
    monkeypatch.delenv("DOCS_RUNTIME", raising=False)
    monkeypatch.setattr(sys, "argv", ["local_apps", target])
    assert launch.main() == 2


@pytest.mark.parametrize("target,verb", [("docs-init", "initialize"), ("docs-serve", "serve")])
def test_documents_delegate_to_existing_lifecycle(tmp_path, monkeypatch, target, verb):
    root = tmp_path / "private runtime"
    if verb == "serve":
        (root / "private").mkdir(parents=True)
        (root / "private/manifest.json").touch()
    monkeypatch.delenv("DEPLOYMENT_ENV", raising=False)
    monkeypatch.setenv("DOCS_RUNTIME", str(root))
    monkeypatch.setenv("DOCUMENT_BIND", "0.0.0.0")
    monkeypatch.setenv("API_AUTH_MODE", "disabled")
    monkeypatch.setenv("OPENAI_COMPATIBLE_API_KEY", "synthetic-secret")
    monkeypatch.setattr(sys, "argv", ["local_apps", target])
    monkeypatch.setattr(launch, "available_ports", lambda *ports: None)
    monkeypatch.setattr(os, "chdir", lambda path: None)
    def execute(executable, args, env):
        assert executable == sys.executable
        assert args == [sys.executable, "-m", "development.document_demo", verb, str(root)]
        assert env["DOCUMENTS_PROFILE"] == "synthetic"
        assert env["DOCUMENT_BIND"] == "127.0.0.1"
        assert env["HOME"] == str(root)
        assert "API_AUTH_MODE" not in env and "OPENAI_COMPATIBLE_API_KEY" not in env
        raise SystemExit(17)
    monkeypatch.setattr(os, "execve", execute)
    with pytest.raises(SystemExit) as error:
        launch.main()
    assert error.value.code == 17


def test_existing_documents_directory_is_not_modified(tmp_path, monkeypatch):
    marker = tmp_path / "preserve"
    marker.write_text("original")
    monkeypatch.delenv("DEPLOYMENT_ENV", raising=False)
    monkeypatch.setenv("DOCS_RUNTIME", str(tmp_path))
    monkeypatch.setattr(sys, "argv", ["local_apps", "docs-init"])
    assert launch.main() == 2
    assert marker.read_text() == "original" and list(tmp_path.iterdir()) == [marker]


def test_port_conflict_is_explained_without_starting_children(monkeypatch):
    class BusySocket:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def bind(self, address):
            raise OSError("busy")
        def setsockopt(self, *args):
            pass
    monkeypatch.setattr(launch.socket, "socket", BusySocket)
    with pytest.raises(launch.LaunchError, match="port 8001 is unavailable"):
        launch.available_ports(8001)


def test_chat_commands_bind_interpreter_entrypoints_and_loopback():
    api, ui = launch.chat_commands()
    assert api[:4] == [sys.executable, "-m", "uvicorn", "api.app:app"]
    assert ui[:4] == [sys.executable, "-m", "streamlit", "run"]
    assert str(launch.REPO / "ui/app.py") in ui
    assert "127.0.0.1" in api and "127.0.0.1" in ui
    historical_api, historical_ui = launch.chat_commands(configured=True)
    assert "--reload" in historical_api
    assert "0.0.0.0" in historical_api and "0.0.0.0" in historical_ui


@pytest.mark.parametrize("stop", ["child-exit", "sigterm"])
def test_supervisor_cleans_up_siblings(tmp_path, stop):
    pidfile = tmp_path / "child.pid"
    script = f"import os,time; open({str(pidfile)!r},'w').write(str(os.getpid())); time.sleep(60)"
    commands = [[sys.executable, "-c", script]]
    if stop == "child-exit":
        commands.append([sys.executable, "-c", "import time; time.sleep(.5); raise SystemExit(7)"])
    code = (f"from development.local_apps import supervise; "
            f"raise SystemExit(supervise({commands!r}, {str(tmp_path)!r}, None))")
    process = subprocess.Popen([sys.executable, "-c", code], cwd=launch.REPO)
    try:
        deadline = time.monotonic() + 10
        while not pidfile.exists() and process.poll() is None and time.monotonic() < deadline:
            time.sleep(.02)
        assert pidfile.exists()
        if stop == "sigterm":
            process.send_signal(signal.SIGTERM)
        assert process.wait(timeout=20) == (0 if stop == "sigterm" else 7)
        with pytest.raises(ProcessLookupError):
            os.kill(int(pidfile.read_text()), 0)
    finally:
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=20)
