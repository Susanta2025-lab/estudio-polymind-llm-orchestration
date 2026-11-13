"""Linux/POSIX resource-contained native parser, using the existing parser port.

This bounds accidental/hostile resource use; it is not a syscall/network sandbox.
No untrusted path or executable is accepted. Child diagnostics are discarded.
"""

import json
import os
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path

from documents.config import ExtractionSettings
from documents.errors import DocumentError
from documents.parser import NativePdfRunner, ParsedPage


@dataclass(frozen=True)
class ParserBounds:
    wall_seconds: float = 10
    cpu_seconds: int = 5
    memory_bytes: int = 512 * 1024 * 1024
    disk_bytes: int = 2 * 1024 * 1024
    output_bytes: int = 256000

    def __post_init__(self):
        if (
            not 0 < self.wall_seconds <= 30
            or not 1 <= self.cpu_seconds <= 20
            or not 32 * 1024 * 1024 <= self.memory_bytes <= 1024**3
            or not 1024 <= self.output_bytes <= self.disk_bytes <= 4 * 1024 * 1024
        ):
            raise ValueError("invalid parser bounds")


class IsolatedPdfRunner:
    version = NativePdfRunner.version

    def __init__(self, bounds=None):
        self.bounds = bounds or ParserBounds()

    def parse(self, data, limits):
        if os.name != "posix" or len(data) > limits.max_source_bytes:
            raise DocumentError("extraction_failed")
        return self._run(data, limits)

    def _run(self, data, limits):
        b = self.bounds
        # Input/output pipes are bounded independently; the child has only a
        # bounded source, no document path. Temporary working directory is empty.
        payload = (
            json.dumps(
                {"limits": limits.model_dump(mode="json"), "bounds": asdict(b)}
            ).encode()
            + b"\n"
            + data
        )
        with tempfile.TemporaryDirectory(prefix="polymind-pilot-parser-") as directory:
            env = {
                "PATH": os.defpath,
                "PYTHONIOENCODING": "utf-8",
                "PYTHONDONTWRITEBYTECODE": "1",
                "TMPDIR": directory,
            }
            # Absolute module root comes from this installed implementation,
            # never from a source/participant record or current working directory.
            env["PYTHONPATH"] = str(Path(__file__).resolve().parents[2])
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "documents.pilot.parser"],
                    input=payload,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    env=env,
                    cwd=directory,
                    timeout=b.wall_seconds,
                    check=False,
                )
                if result.returncode or len(result.stdout) > b.output_bytes:
                    raise DocumentError("extraction_failed")
                values = json.loads(result.stdout)
                pages = tuple(ParsedPage(**v) for v in values)
                if (
                    not pages
                    or len(pages) > limits.max_pages
                    or sum(len(p.text) for p in pages) > limits.max_characters
                    or any(p.failed for p in pages)
                ):
                    raise DocumentError("extraction_failed")
                return pages
            except (subprocess.TimeoutExpired, ValueError, TypeError, OSError):
                raise DocumentError("extraction_failed") from None


def _child():
    import resource

    header = sys.stdin.buffer.readline(8192)
    config = json.loads(header)
    b = ParserBounds(**config["bounds"])
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_CPU, (b.cpu_seconds, b.cpu_seconds))
    resource.setrlimit(resource.RLIMIT_AS, (b.memory_bytes, b.memory_bytes))
    resource.setrlimit(resource.RLIMIT_FSIZE, (b.disk_bytes, b.disk_bytes))
    resource.setrlimit(resource.RLIMIT_NOFILE, (32, 32))

    def read_only(event, args):
        if event == "open":
            _, mode, flags = args
            if (mode and any(c in mode for c in "wax+")) or (
                flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC)
            ):
                raise PermissionError("parser writes forbidden")
        if event in {
            "os.mkdir",
            "os.rename",
            "os.remove",
            "os.rmdir",
            "os.link",
            "os.symlink",
            "subprocess.Popen",
            "os.system",
            "socket.connect",
            "socket.bind",
        }:
            raise PermissionError("parser side effects forbidden")

    # Native extraction needs no scratch writes. Deny Python filesystem writes,
    # subprocesses and sockets rather than giving every file a separate quota.
    # This is defense in depth, not a security sandbox for arbitrary native code.
    sys.addaudithook(read_only)
    limits = ExtractionSettings(**config["limits"])
    data = sys.stdin.buffer.read(limits.max_source_bytes + 1)
    pages = NativePdfRunner().parse(data, limits)
    raw = json.dumps([asdict(p) for p in pages]).encode()
    if len(raw) > b.output_bytes:
        raise DocumentError("extraction_limit_exceeded")
    sys.stdout.buffer.write(raw)


if __name__ == "__main__":
    try:
        _child()
    except Exception:  # noqa: BLE001 - child must never emit parser diagnostics
        raise SystemExit(1) from None
