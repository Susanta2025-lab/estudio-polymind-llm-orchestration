"""Interpreter-bound local launchers; application settings and processing stay unchanged."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import signal
import socket
import stat
import subprocess
import sys
import tempfile
import time

REPO = Path(__file__).resolve().parents[1]
MODEL_MAP = {"general": "mistral:latest", "coding": "qwen2.5:3b",
             "summarization": "gemma2:2b", "fast": "phi3:mini"}


class LaunchError(Exception):
    pass


def require_modules(*names):
    missing = [name for name in names if importlib.util.find_spec(name) is None]
    if missing:
        raise LaunchError(f"Selected Python {sys.executable} lacks: {', '.join(missing)}. "
                          "Activate the existing project environment or set make PYTHON=/path/to/python.")


def outside_repo(value):
    path = Path(value).expanduser().resolve()
    if path == REPO or REPO in path.parents:
        raise LaunchError("Choose a private runtime directory outside the repository.")
    return path


def available_ports(*ports):
    # Advisory check; bind failures after this race are still handled by services.
    for port in ports:
        with socket.socket() as probe:
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                probe.bind(("127.0.0.1", port))
            except OSError:
                raise LaunchError(f"Loopback port {port} is unavailable. Stop its owner; "
                                  "Chat and Documents must run separately.") from None


def clean_environment():
    # No PATH lookup is needed for Python: sys.executable was selected by Make
    # before this environment is constructed. Never copy proxies or credentials.
    env = {name: os.environ[name] for name in ("SYSTEMROOT", "LD_LIBRARY_PATH", "LANG", "LC_ALL")
           if name in os.environ}
    env.update(PATH=os.defpath, PYTHONPATH=str(REPO), PYTHONDONTWRITEBYTECODE="1",
               PYTHONUNBUFFERED="1", DEPLOYMENT_ENV="local")
    return env


def chat_environment():
    root = outside_repo(os.environ.get("CHAT_RUNTIME") or
                        str(Path(tempfile.gettempdir()) / f"polymind-chat-{os.getuid()}"))
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    info = root.stat()
    if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
        raise LaunchError("CHAT_RUNTIME must be owned by you with private permissions (0700).")
    # Refuse local settings that could reintroduce a second configuration source.
    if any((root / name).exists() or (root / name).is_symlink() for name in (".env", ".streamlit")):
        raise LaunchError("CHAT_RUNTIME must contain no .env or .streamlit configuration.")
    assets = root / "ui"
    if ((not assets.is_symlink() and assets.exists())
            or (assets.is_symlink() and assets.resolve() != REPO / "ui")):
        raise LaunchError("CHAT_RUNTIME/ui conflicts with the repository asset link.")
    if not assets.is_symlink():
        try:
            assets.symlink_to(REPO / "ui", target_is_directory=True)
        except FileExistsError:
            # Separate API/UI terminals may initialize the same runtime together.
            if not assets.is_symlink() or assets.resolve() != REPO / "ui":
                raise LaunchError("CHAT_RUNTIME/ui conflicts with the repository asset link.") from None
    chroma = Path(os.environ.get("CHAT_CHROMA_PATH") or root / "chroma_db").expanduser().resolve()
    if (root / "memory.json").is_symlink():
        raise LaunchError("CHAT_RUNTIME/memory.json must not be a symlink.")
    env = clean_environment()
    env.update(HOME=str(root), DOCUMENTS_PROFILE="legacy", INFERENCE_PROVIDER="ollama",
               OLLAMA_URL="http://127.0.0.1:11434/api/chat", OLLAMA_MODEL_MAP=json.dumps(MODEL_MAP),
               API_HOST="127.0.0.1", API_PORT="8001", API_AUTH_MODE="disabled", API_AUTH_ENABLED="false",
               GOVERNANCE_ENABLED="false", MEMORY_PROVIDER="file", MEMORY_FILE=str(root / "memory.json"),
               VECTOR_STORE_PROVIDER="chroma_local", CHROMA_PATH=str(chroma),
               BM25_CORPUS_VERSION=os.environ.get("CHAT_CORPUS_VERSION") or "development",
               API_URL="http://127.0.0.1:8001/query", STREAM_URL="http://127.0.0.1:8001/query/stream",
               MODEL_OFFLINE_MODE="true", HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1",
               HF_HUB_DISABLE_TELEMETRY="1", ANONYMIZED_TELEMETRY="false",
               HF_HOME=str(Path(os.environ.get("CHAT_HF_HOME") or Path.home() / ".cache/huggingface").expanduser().resolve()))
    if os.environ.get("CHAT_MODEL_ARTIFACT_DIR"):
        env["MODEL_ARTIFACT_DIR"] = str(Path(os.environ["CHAT_MODEL_ARTIFACT_DIR"]).expanduser().resolve())
    print(f"Local Chat: Python={sys.executable}; runtime={root}; Chroma={chroma}", flush=True)
    print("Ollama must provide all four configured models. Check http://127.0.0.1:8001/ready; "
          "an absent/unpublished corpus is not ready. No models are downloaded.", flush=True)
    return root, env


def chat_commands(*, configured=False):
    host = "0.0.0.0" if configured else "127.0.0.1"
    api = [sys.executable, "-m", "uvicorn", "api.app:app", "--host", host, "--port", "8001"]
    if configured:
        api.append("--reload")
    ui = [sys.executable, "-m", "streamlit", "run", str(REPO / "ui/app.py"),
          "--server.address", host, "--server.port", "8501"]
    if not configured:
        ui += ["--browser.gatherUsageStats", "false", "--server.headless", "true"]
    return api, ui


def supervise(commands, cwd, env):
    """Stop sibling processes (including Uvicorn reload children) on any exit."""
    children = []
    def stop(_signum, _frame):
        raise KeyboardInterrupt
    previous = signal.signal(signal.SIGTERM, stop)
    try:
        for command in commands:
            children.append(subprocess.Popen(command, cwd=cwd, env=env, start_new_session=True))
        while all(child.poll() is None for child in children):
            time.sleep(0.2)
        return next(child.returncode or 1 for child in children if child.returncode is not None)
    except KeyboardInterrupt:
        return 0
    finally:
        signal.signal(signal.SIGTERM, previous)
        for child in children:
            try:
                os.killpg(child.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        deadline = time.monotonic() + 15
        for child in children:
            try:
                child.wait(timeout=max(0, deadline - time.monotonic()))
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                child.wait()


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("command", choices=("dev", "chat-api", "chat-ui", "chat-dev", "docs-init", "docs-serve"))
    command = parser.parse_args().command
    try:
        if command == "dev":
            require_modules("uvicorn", "prometheus_client", "streamlit")
            return supervise(chat_commands(configured=True), Path.cwd(), dict(os.environ))
        if os.environ.get("DEPLOYMENT_ENV") == "production":
            raise LaunchError("Local development launchers are forbidden in a production environment.")
        if command.startswith("docs-"):
            value = os.environ.get("DOCS_RUNTIME", "")
            if not value.strip():
                raise LaunchError("DOCS_RUNTIME is required: make docs-init DOCS_RUNTIME=/tmp/NEW-private-directory")
            root = outside_repo(value)
            if command == "docs-init" and root.exists():
                raise LaunchError("DOCS_RUNTIME already exists. Choose a NEW directory; never reset approvals.")
            if command == "docs-serve" and not (root / "private/manifest.json").is_file():
                raise LaunchError("DOCS_RUNTIME is not initialized. Initialize a NEW directory first.")
            require_modules("uvicorn", "prometheus_client", "streamlit", "jwt", "cryptography", "authlib")
            env = clean_environment()
            env.update(DOCUMENTS_PROFILE="synthetic", HOME=str(root), DOCUMENT_BIND="127.0.0.1")
            if command == "docs-serve":
                available_ports(8001, 8501, 9443, 9444)
            # The existing lifecycle owns initialization, OIDC, worker and cleanup.
            args = [sys.executable, "-m", "development.document_demo",
                    "initialize" if command == "docs-init" else "serve", str(root)]
            cwd = root if command == "docs-serve" else Path(tempfile.gettempdir())
        else:
            require_modules(*(("uvicorn", "prometheus_client") if command == "chat-api" else
                              ("streamlit",) if command == "chat-ui" else
                              ("uvicorn", "prometheus_client", "streamlit")))
            available_ports(*((8001,) if command == "chat-api" else (8501,) if command == "chat-ui" else (8001, 8501)))
            cwd, env = chat_environment()
            api, ui = chat_commands()
            if command == "chat-dev":
                return supervise((api, ui), cwd, env)
            args = api if command == "chat-api" else ui
        os.chdir(cwd)
        os.execve(sys.executable, args, env)
    except (LaunchError, OSError) as exc:
        print(f"Local launcher: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
