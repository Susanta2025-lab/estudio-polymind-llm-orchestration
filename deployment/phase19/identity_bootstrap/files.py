"""Descriptor-relative private files; atomic, exclusive candidate publication on Linux."""

import json
import os
import stat
from contextlib import contextmanager
from pathlib import Path

from deployment.phase19.storage import local_filesystem
from security.models import SecurityError

REPO = Path(__file__).resolve().parents[3]
NAME = "enrollment-candidate.json"
PENDING = ".enrollment-candidate.pending"


def ancestor(info):
    if info.st_uid not in {0, os.geteuid()} or info.st_mode & 0o022:
        raise ValueError("Unsafe ancestor")


@contextmanager
def directory(value):
    """Walk every component without resolving symlinks or trusting path-based stat."""
    path = Path(value)
    if (
        not path.is_absolute()
        or ".." in path.parts
        or path == REPO
        or REPO in path.parents
        or path == Path("/")
        or path == Path("/mnt")
        or Path("/mnt") in path.parents
    ):
        raise ValueError("External private Linux directory required")
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        ancestor(os.fstat(fd))
        for part in path.parts[1:]:
            child = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd
            )
            os.close(fd)
            fd = child
            ancestor(os.fstat(fd))
        info = os.fstat(fd)
        if info.st_uid != os.geteuid() or stat.S_IMODE(info.st_mode) != 0o700:
            raise ValueError("Operator-owned 0700 directory required")
        local_filesystem(path)
        yield fd
    finally:
        os.close(fd)


def regular(fd):
    info = os.fstat(fd)
    if (
        not stat.S_ISREG(info.st_mode)
        or info.st_nlink != 1
        or info.st_uid != os.geteuid()
        or stat.S_IMODE(info.st_mode) != 0o600
    ):
        raise ValueError("Operator-owned single-link 0600 file required")
    return info


def read_private(path, *, limit=65536):
    path = Path(path)
    with directory(path.parent) as parent:
        fd = os.open(
            path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent
        )
        try:
            regular(fd)
            data = os.read(fd, limit + 1)
            if len(data) > limit:
                raise ValueError("Private file too large")
            return data
        finally:
            os.close(fd)


def export(token, verifier, destination, *, authorized=False):
    """One fixed candidate per explicitly approved directory, shared across tabs/processes."""
    if authorized is not True:
        raise SecurityError("access_denied")
    from deployment.phase19.identity_bootstrap.core import candidate

    # Never export a stored Principal: cryptographically reverify the current token.
    evidence = candidate(verifier.verify(token))
    data = (json.dumps(evidence, sort_keys=True, ensure_ascii=True) + "\n").encode()
    with directory(destination) as parent:
        fd = None
        created = None
        try:
            # A crash may leave this marker. Refuse rather than silently retry.
            fd = os.open(
                PENDING,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
                dir_fd=parent,
            )
            created = os.fstat(fd)
            regular(fd)
            with os.fdopen(os.dup(fd), "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            regular(fd)
            # link() is an atomic no-replace publication; final name never contains partial JSON.
            os.link(
                PENDING,
                NAME,
                src_dir_fd=parent,
                dst_dir_fd=parent,
                follow_symlinks=False,
            )
        finally:
            try:
                if created is not None:
                    current = os.stat(PENDING, dir_fd=parent, follow_symlinks=False)
                    if (current.st_dev, current.st_ino) == (
                        created.st_dev,
                        created.st_ino,
                    ):
                        os.unlink(PENDING, dir_fd=parent)
                os.fsync(parent)
            finally:
                if fd is not None:
                    os.close(fd)
    return evidence
