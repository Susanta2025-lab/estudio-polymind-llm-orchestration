"""Trusted test-only child faults after production parser limits are installed."""

import sys

from documents.errors import DocumentError
from documents.parser import NativePdfRunner, ParsedPage
from documents.pilot.parser import _child


def faulty(*args):
    fault = sys.argv[1]
    if fault in {"wall", "cpu"}:
        while True:
            pass
    if fault == "memory":
        return bytearray(1024**3)
    if fault == "disk":
        with open("forbidden-scratch", "wb") as stream:
            stream.write(b"x" * 4000000)
    if fault == "output":
        return (ParsedPage(1, text="x" * 100000),)
    return ()


NativePdfRunner.parse = faulty
try:
    _child()
except MemoryError:
    raise SystemExit(61) from None
except PermissionError:
    raise SystemExit(62) from None
except DocumentError:
    raise SystemExit(63) from None
except Exception:  # noqa: BLE001 - test child reports only exit codes
    raise SystemExit(1) from None
