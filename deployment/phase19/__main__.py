"""Explicit lifecycle commands; serving only reopens existing authorities."""
import argparse
import os
from pathlib import Path

from deployment.phase19.storage import ownership


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('initialize', 'serve', 'check'))
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    with ownership(args.root, initialize=args.command == 'initialize'):
        if args.command == 'check':
            from deployment.phase19.runtime import configuration
            configuration(args.root)
            return
        from deployment.phase19.runtime import build
        runtime, workflow, runner, cleanup = build(args.root, initialize=args.command == 'initialize')
        if args.command == 'initialize':
            cleanup()
            return
        from documents.operator.app import create_app
        import uvicorn
        app = create_app(runtime, workflow, runner, cleanup=cleanup, chat=runner.chat)
        # Lock remains held through Uvicorn lifespan, runner join and cleanup.
        uvicorn.run(app, host='0.0.0.0', port=8001, workers=1, access_log=False,
                    timeout_graceful_shutdown=70, log_level='warning')


if __name__ == '__main__':
    os.umask(0o077)
    try:
        main()
    except Exception:
        raise SystemExit('Phase 19 configuration/state unavailable; trusted reconciliation required.') from None
