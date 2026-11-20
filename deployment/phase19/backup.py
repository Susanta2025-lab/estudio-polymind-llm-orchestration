"""Stopped whole-tree snapshot/restore. Never starts a restored authority.

Operator must stop ALL writers (including Redis/Chroma) first. Snapshot the data
mount as one tree; the API lock alone cannot prove vendor services have stopped.
Backup custody is trusted; SHA256 detects damage, not malicious replacement.
"""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import stat

from deployment.phase19.storage import ownership, private_path, DATABASES


def inventory(root):
    result = {}
    for path in sorted(root.rglob('*')):
        info = path.lstat()
        if stat.S_ISDIR(info.st_mode):
            continue
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError('Unsafe backup entry')
        if path.name == 'runtime.lock':
            continue
        digest = sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(65536), b''):
                digest.update(chunk)
        result[str(path.relative_to(root))] = digest.hexdigest()
    return result


def copy_tree(source, target):
    def copy_file(src, dst):
        shutil.copy2(src, dst)
        info = Path(src).stat()
        if os.geteuid() == 0:
            os.chown(dst, info.st_uid, info.st_gid)
        elif info.st_uid != os.geteuid():
            raise ValueError('Trusted root required to preserve mixed service owners')
        return dst
    shutil.copytree(source, target, copy_function=copy_file,
                    ignore=shutil.ignore_patterns('runtime.lock'))
    if os.geteuid() == 0:
        for path in [source, *source.rglob('*')]:
            if path.is_dir():
                info = path.stat()
                os.chown(target / path.relative_to(source), info.st_uid, info.st_gid)


def snapshot(data, target, *, stopped=False):
    data = Path(data).absolute()
    owner = data.stat().st_uid
    if owner != os.geteuid() and os.geteuid() != 0:
        raise ValueError("Trusted backup custodian required")
    data = private_path(data, directory=True, owner=owner)
    target = Path(target).absolute()
    if not stopped or target.exists() or data == target or data in target.parents:
        raise ValueError('Stopped writers and new independent backup location required')
    with ownership(data / 'operator', container_root='/state', owner=(data / 'operator').stat().st_uid):
        before = inventory(data)
        copy_tree(data, target / 'data')
        if inventory(target / 'data') != before or inventory(data) != before:
            raise ValueError('Backup changed during snapshot; discard incomplete copy')
        (target / 'manifest.json').write_text(json.dumps({'version': 'phase19-backup/1', 'files': before}))
        os.chmod(target, 0o700)
        os.chmod(target / 'manifest.json', 0o600)


def restore(backup, target):
    backup = private_path(backup, directory=True)
    target = Path(target).absolute()
    if target.exists():
        raise ValueError('Restore requires a new isolated directory')
    record = json.loads((backup / 'manifest.json').read_text())
    if record['version'] != 'phase19-backup/1' or inventory(backup / 'data') != record['files']:
        raise ValueError('Backup integrity unavailable')
    copy_tree(backup / 'data', target)
    if inventory(target) != record['files']:
        raise ValueError('Restore integrity unavailable')
    # Validate SQLite even though container paths remain unchanged in deployment.json.
    import sqlite3
    from contextlib import closing
    for name in DATABASES:
        with closing(sqlite3.connect((target / 'operator' / 'private' / name).as_uri() + '?mode=ro', uri=True)) as db:
            if db.execute('PRAGMA quick_check').fetchone()[0] != 'ok':
                raise ValueError('Restored authority integrity unavailable')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('snapshot', 'restore'))
    parser.add_argument('source', type=Path)
    parser.add_argument('target', type=Path)
    parser.add_argument('--writers-stopped', action='store_true')
    args = parser.parse_args()
    os.umask(0o077)
    if args.command == 'snapshot':
        snapshot(args.source, args.target, stopped=args.writers_stopped)
    else:
        restore(args.source, args.target)


if __name__ == '__main__':
    main()
