"""Fixture entrypoint; shared HTTP contracts live in documents.operator.app."""
import os

from documents.operator.app import create_app


def configured_app():
    from development.document_demo.runtime import build
    root = os.environ["DOCUMENT_DEMO_ROOT"]
    # OS lock spans API + runner ownership. No second authority writer process.
    from filelock import FileLock
    lock = FileLock(root + "/runtime.lock", timeout=0)
    lock.acquire()
    try:
        runtime, workflow, runner, _ = build(root, deployment_env=os.environ.get("DEPLOYMENT_ENV", "local"))
        app = create_app(runtime, workflow, runner)
        app.state.process_lock = lock
        return app
    except BaseException:
        lock.release()
        raise
