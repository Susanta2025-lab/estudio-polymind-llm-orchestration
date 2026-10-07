"""Immutable object port and POSIX local adapter; root is operator-controlled.

The caller supplies trusted scope, never an authorization token inferred from a key.
No delete/list API: test cleanup belongs to the temporary-directory owner.
"""

import hashlib
import os
import stat
from pathlib import Path
from typing import BinaryIO, Literal, Protocol
from uuid import UUID, uuid4

from documents.errors import DocumentError
from documents.models import ObjectRef, Scope, stable_id


class ObjectStore(Protocol):
    def put(self, scope: Scope, kind: Literal["source", "artifact"], object_id: UUID,
            stream: BinaryIO, *, max_bytes: int, expected_sha256: str | None = None) -> ObjectRef: ...

    def read(self, scope: Scope, ref: ObjectRef, *, max_bytes: int) -> bytes: ...

    def inspect(self, scope: Scope, ref: ObjectRef, *, max_bytes: int) -> ObjectRef: ...


class LocalObjectStore:
    """Atomic link-if-absent publication, verified idempotent writes, no overwrite.

    Directory fds and O_NOFOLLOW resist symlink substitution, including ancestors.
    Requires POSIX dir_fd/link support; not a Windows or hostile-host sandbox.
    """

    def __init__(self, root: Path):
        self.root = Path(os.path.abspath(root))

    def _directory(self) -> int:
        fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
        try:
            for part in self.root.parts[1:]:
                try:
                    os.mkdir(part, mode=0o700, dir_fd=fd)
                except FileExistsError:
                    pass
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                os.close(fd)
                fd = child
            return fd
        except BaseException:
            os.close(fd)
            raise

    @staticmethod
    def _check(scope: Scope, ref: ObjectRef, max_bytes: int):
        if scope != ref.scope:
            raise DocumentError("scope_mismatch")
        if max_bytes < 1 or ref.byte_size > max_bytes:
            raise DocumentError("source_too_large")
        if ref.key != stable_id(scope.identity(), ref.kind, str(ref.object_id)):
            raise DocumentError("invalid_reference")

    def _read(self, fd: int, ref: ObjectRef, max_bytes: int, *, collect: bool) -> bytes:
        try:
            raw = os.open(str(ref.key), os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        except FileNotFoundError:
            raise DocumentError("object_not_found") from None
        with os.fdopen(raw, "rb") as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise DocumentError("storage_error")
            if info.st_size > max_bytes:
                raise DocumentError("source_too_large")
            digest, count = hashlib.sha256(), 0
            data = bytearray()
            while chunk := stream.read(min(65536, max_bytes - count + 1)):
                count += len(chunk)
                if count > max_bytes:
                    raise DocumentError("source_too_large")
                digest.update(chunk)
                if collect:
                    data.extend(chunk)
            if count != ref.byte_size or digest.hexdigest() != ref.sha256:
                raise DocumentError("integrity_error")
            return bytes(data)

    def put(self, scope, kind, object_id, stream, *, max_bytes, expected_sha256=None):
        if max_bytes < 1 or kind not in ("source", "artifact") or not isinstance(object_id, UUID):
            raise DocumentError("invalid_reference")
        fd = None
        temporary = f".pending-{uuid4()}"
        try:
            fd = self._directory()
            raw = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                          0o600, dir_fd=fd)
            digest, size = hashlib.sha256(), 0
            with os.fdopen(raw, "wb") as output:
                while chunk := stream.read(min(65536, max_bytes - size + 1)):
                    if not isinstance(chunk, bytes):
                        raise DocumentError("storage_error")
                    size += len(chunk)
                    if size > max_bytes:
                        raise DocumentError("source_too_large")
                    digest.update(chunk)
                    output.write(chunk)
                output.flush()
                os.fsync(output.fileno())
            checksum = digest.hexdigest()
            if expected_sha256 is not None and checksum != expected_sha256:
                raise DocumentError("integrity_error")
            ref = ObjectRef(scope=scope, kind=kind, object_id=object_id,
                            key=stable_id(scope.identity(), kind, str(object_id)),
                            sha256=checksum, byte_size=size)
            try:
                os.link(temporary, str(ref.key), src_dir_fd=fd, dst_dir_fd=fd,
                        follow_symlinks=False)
            except FileExistsError:
                try:
                    self._read(fd, ref, max_bytes, collect=False)
                except DocumentError as exc:
                    if exc.category in ("integrity_error", "source_too_large"):
                        raise DocumentError("object_conflict") from None
                    raise
            os.unlink(temporary, dir_fd=fd)
            os.fsync(fd)
            return ref
        except DocumentError:
            raise
        except Exception:
            raise DocumentError("storage_error") from None
        finally:
            if fd is not None:
                try:
                    os.unlink(temporary, dir_fd=fd)
                except FileNotFoundError:
                    pass
                except OSError:
                    raise DocumentError("storage_error") from None
                finally:
                    os.close(fd)

    def _access(self, scope, ref, max_bytes, collect):
        self._check(scope, ref, max_bytes)
        fd = None
        try:
            fd = self._directory()
            return self._read(fd, ref, max_bytes, collect=collect)
        except DocumentError:
            raise
        except Exception:
            raise DocumentError("storage_error") from None
        finally:
            if fd is not None:
                os.close(fd)

    def read(self, scope, ref, *, max_bytes):
        return self._access(scope, ref, max_bytes, True)

    def inspect(self, scope, ref, *, max_bytes):
        self._access(scope, ref, max_bytes, False)
        return ref
