"""Local lifecycle: explicit initialize, serve, and coherent quiesced backup."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("command", choices=("initialize", "serve", "identity", "gateway", "backup"))
    parser.add_argument("root", type=Path)
    parser.add_argument("--destination", type=Path)
    args = parser.parse_args()
    if os.environ.get("DEPLOYMENT_ENV") == "production":
        parser.error("Fixture runtime is forbidden in production")
    os.umask(0o077)
    root = args.root.resolve()
    if args.command == "initialize":
        from development.document_demo.provision import provision
        from development.document_demo.runtime import build
        provision(root)
        build(root, initialize=True)
        print("Synthetic runtime initialized; three total sessions, approvals expire in one hour.")
    elif args.command == "identity":
        from development.document_demo.identity import issuer_app
        import uvicorn
        uvicorn.run(issuer_app(root), host=os.environ.get("DOCUMENT_BIND", "127.0.0.1"), port=9444,
                    ssl_keyfile=str(root / "tls.key"), ssl_certfile=str(root / "tls.crt"), access_log=False)
    elif args.command == "gateway":
        from development.document_demo.gateway import serve
        serve(root, backend=os.environ.get("DOCUMENT_UI_BACKEND", "http://127.0.0.1:8501"),
              host=os.environ.get("DOCUMENT_BIND", "127.0.0.1"))
    elif args.command == "backup":
        from filelock import FileLock
        if (args.destination is None or args.destination.exists()
                or args.destination.resolve().is_relative_to(root)):
            parser.error("A new backup destination outside the runtime is required")
        # Same process lock as the API/runner. Stop all services first. All
        # authorities/objects/actions/consumed approvals copied together.
        with FileLock(str(root / "runtime.lock"), timeout=0):
            shutil.copytree(root, args.destination)
        print("Quiesced snapshot created. Restore only at the original absolute runtime path.")
    else:
        import signal
        def shutdown(signum, frame):
            raise KeyboardInterrupt
        signal.signal(signal.SIGTERM, shutdown)
        repo = str(Path(__file__).resolve().parents[2])
        env = {k: v for k, v in os.environ.items() if not any(
            marker in k.upper() for marker in ("AZURE", "OPENAI", "TOKEN", "PASSWORD", "SECRET", "OLLAMA", "API_KEY",
                "API_AUTH", "OIDC_", "GOVERNANCE_", "SECURITY_", "MEMORY_", "VECTOR_", "CHROMA"))}
        env.update(DOCUMENT_DEMO_ROOT=str(root), DOCUMENTS_PROFILE="synthetic", DEPLOYMENT_ENV="local",
                   DOCUMENTS_API_URL="http://127.0.0.1:8001", SSL_CERT_FILE=str(root / "tls.crt"),
                   REQUESTS_CA_BUNDLE=str(root / "tls.crt"), PYTHONPATH=repo + os.pathsep + env.get("PYTHONPATH", ""))
        commands = [
            [sys.executable, "-m", "development.document_demo", "identity", str(root)],
            [sys.executable, "-m", "uvicorn", "development.document_demo.app:configured_app", "--factory",
             "--host", "127.0.0.1", "--port", "8001", "--no-access-log"],
            [sys.executable, "-m", "streamlit", "run", repo + "/ui/app.py", "--server.address", "127.0.0.1",
             "--server.port", "8501", "--browser.gatherUsageStats", "false", "--server.headless", "true",
             "--secrets.files", str(root / ".streamlit/secrets.toml"), "--server.enableCORS", "true",
             "--server.enableXsrfProtection", "true", "--server.corsAllowedOrigins", "https://localhost:9443"],
            [sys.executable, "-m", "development.document_demo", "gateway", str(root)],
        ]
        children = []
        try:
            for command in commands:
                children.append(subprocess.Popen(command, env=env, cwd=root))
            print("Private synthetic UI: https://localhost:9443 — trust only this runtime's tls.crt.")
            while all(p.poll() is None for p in children):
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            for process in children:
                if process.poll() is None:
                    process.terminate()
            for process in children:
                try:
                    process.wait(timeout=70)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


if __name__ == "__main__":
    main()
