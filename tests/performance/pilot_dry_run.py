"""Offline synthetic pilot runner. No live mode, credentials or participant input.

python -m tests.performance.pilot_dry_run --output /tmp/new-pilot-fixture
"""

import argparse
import json
import os
import socket
from pathlib import Path


def execute(root):
    from pytest import MonkeyPatch

    from tests.settings_isolation import isolate_application_settings

    with MonkeyPatch.context() as patch:
        isolate_application_settings(patch)

        def denied(*_args, **_kwargs):
            raise RuntimeError("Network forbidden in synthetic pilot")

        patch.setattr(socket.socket, "connect", denied)
        from documents.pilot.models import Feedback
        from tests.performance.fixtures import pdf
        from tests.pilot_helpers import complete, composition

        raw, _ = pdf(4)
        env = composition(root, raw=raw, pdf=True)
        pilot, op, approval, _, http, _, _ = env
        complete(env)
        packets = []
        pilot.present(op, approval.session_id, packets.append)
        pilot.question(
            op,
            approval.session_id,
            "What is inspected before operation?",
            packets.append,
        )
        pilot.feedback(
            op,
            approval.session_id,
            Feedback(
                usefulness=4, would_repeat=True, notice_understood=True, issue="none"
            ),
        )
        review = pilot.review_packet(op, approval.session_id)
        closure = pilot.close(op, approval.session_id)
        usage = pilot.governance.usage(op, pilot.authority)
        summary = {
            "mode": "SYNTHETIC_ONLY",
            "digest_status": packets[0]["status"],
            "coverage": packets[0]["coverage"]["fraction"],
            "calls": len(http.calls),
            "settled": sum(r["state"] == "SETTLED" for r in usage),
            "outstanding": sum(
                r["state"] not in {"SETTLED", "RELEASED"} for r in usage
            ),
            "qa_citations": len(packets[1]["citations"]),
            "billable_calls": 0,
            "session_state": closure["state"],
            "purge_status": closure["purge_status"],
            "human_reviews": 0,
            "external_user_verification": "PENDING",
        }
        for filename, value in (
            ("summary.json", summary),
            ("closure.json", closure),
            ("review-packet.json", review),
        ):
            path = root / filename
            with path.open("x", encoding="utf-8") as stream:
                json.dump(value, stream, ensure_ascii=True, indent=2)
                stream.write("\n")
        return summary


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.output.absolute()
    if (
        root.exists()
        or ".." in root.parts
        or root.is_relative_to(Path.cwd().resolve())
        or any(p.is_symlink() for p in root.parents)
    ):
        parser.error("choose a fresh private output directory outside the checkout")
    os.umask(0o077)
    root.mkdir(mode=0o700, parents=True)
    print(json.dumps(execute(root), sort_keys=True))


if __name__ == "__main__":
    main()
