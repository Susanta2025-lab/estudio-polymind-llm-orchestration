"""Fail-closed local state preflight and one process ownership domain."""
import json
import os
from pathlib import Path
import sqlite3
import stat
from contextlib import closing, contextmanager

import fcntl
from filelock import Timeout

DATABASES = ("security.sqlite", "governance.sqlite", "admission.sqlite", "jobs.sqlite",
             "pilot.sqlite", "actions.sqlite", "publication.sqlite")


def private_path(value, *, directory, owner=None):
    path = Path(value)
    if not path.is_absolute() or '..' in path.parts or any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError("Private path unavailable")
    info = path.stat()
    valid = stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode) and info.st_nlink == 1
    if not valid or info.st_uid != (os.geteuid() if owner is None else owner) or info.st_mode & 0o077:
        raise ValueError("Private path permissions unavailable")
    return path


def local_filesystem(root, *, durable=False):
    # Read the kernel's actual backing filesystem, not an operator-supplied label.
    mounts = []
    for line in Path('/proc/self/mountinfo').read_text().splitlines():
        fields, suffix = line.split(' - ', 1)
        mount = Path(fields.split()[4].replace('\\040', ' ').replace('\\134', '\\'))
        if root == mount or mount in root.parents:
            mounts.append((len(mount.parts), suffix.split()[0]))
    allowed = {'ext4', 'xfs', 'btrfs'} if durable else {'ext4', 'xfs', 'btrfs', 'overlay', 'tmpfs'}
    if not mounts or max(mounts)[1] not in allowed:
        raise ValueError("Compatible local filesystem required")


def preflight(root, *, initialize=False, container_root=None, owner=None):
    root = private_path(root, directory=True, owner=owner)
    local_filesystem(root)
    marker = private_path(root / 'deployment.json', directory=False, owner=owner)
    metadata = json.loads(marker.read_text())
    if metadata != {'version': 'phase19-state/1', 'container_root': container_root or str(root)}:
        raise ValueError("Stable state binding unavailable")
    state = private_path(root / 'private', directory=True, owner=owner)
    private_path(state / 'objects', directory=True, owner=owner)
    if initialize:
        if any((state / name).exists() for name in DATABASES):
            raise ValueError("Existing authority cannot be initialized")
    else:
        for name in DATABASES:
            path = private_path(state / name, directory=False, owner=owner)
            with closing(sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)) as db:
                if (db.execute('PRAGMA user_version').fetchone()[0] != 1
                        or db.execute('PRAGMA quick_check').fetchone()[0] != 'ok'):
                    raise ValueError("Authority integrity unavailable; reconciliation required")
    return root


@contextmanager
def ownership(root, *, initialize=False, container_root=None, owner=None):
    root = private_path(root, directory=True, owner=owner)
    lock_path = root / 'runtime.lock'
    if lock_path.exists() or lock_path.is_symlink():
        private_path(lock_path, directory=False, owner=owner)
    # Never unlink this inode; backup/maintenance and API share it.
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        if os.geteuid() == 0 and owner is not None:
            os.fchown(fd, owner, -1)
        private_path(lock_path, directory=False, owner=owner)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Timeout(str(lock_path)) from None
        preflight(root, initialize=initialize, container_root=container_root, owner=owner)
        yield root
    finally:
        os.close(fd)
