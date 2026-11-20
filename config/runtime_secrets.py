"""Explicit private file checks for mounted runtime secrets."""
import os
from pathlib import Path
import stat


def private_file(value):
    path = Path(value)
    if not path.is_absolute() or '..' in path.parts or any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('Private secret unavailable')
    info = path.stat()
    if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid != os.geteuid()
            or info.st_mode & 0o077):
        raise ValueError('Private secret unavailable')
    return path
