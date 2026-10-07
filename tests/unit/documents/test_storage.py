from concurrent.futures import ThreadPoolExecutor
import hashlib
from io import BytesIO
from uuid import UUID

import pytest
from pydantic import ValidationError

from documents.errors import DocumentError
from documents.models import ObjectRef, Scope, stable_id
from documents.storage import LocalObjectStore

SCOPE = Scope(tenant=UUID(int=1), owner=UUID(int=2))


def put(store, data=b'source', scope=SCOPE, **kwargs):
    return store.put(scope, 'source', UUID(int=3), BytesIO(data), max_bytes=100, **kwargs)


def test_immutable_verified_read_inspect_and_conflict(tmp_path):
    store = LocalObjectStore(tmp_path)
    ref = put(store)
    assert ref == put(store)
    assert ref.sha256 == hashlib.sha256(b'source').hexdigest()
    assert store.read(SCOPE, ref, max_bytes=100) == b'source'
    assert store.inspect(SCOPE, ref, max_bytes=100) == ref
    with pytest.raises(DocumentError, match='object_conflict'):
        put(store, b'changed')
    assert store.read(SCOPE, ref, max_bytes=100) == b'source'
    with pytest.raises(DocumentError, match='source_too_large'):
        store.read(SCOPE, ref, max_bytes=2)
    (tmp_path / str(ref.key)).write_bytes(b'broken')
    with pytest.raises(DocumentError, match='integrity_error'):
        store.read(SCOPE, ref, max_bytes=100)
    assert len(list(tmp_path.iterdir())) == 1


def test_missing_object_and_checksum_rejection(tmp_path):
    store = LocalObjectStore(tmp_path)
    with pytest.raises(DocumentError, match='integrity_error'):
        put(store, expected_sha256='0'*64)
    assert not list(tmp_path.iterdir())
    ref = put(store)
    (tmp_path / str(ref.key)).unlink()
    with pytest.raises(DocumentError, match='object_not_found'):
        store.inspect(SCOPE, ref, max_bytes=100)


def test_scope_isolation_and_unsafe_reference(tmp_path):
    store = LocalObjectStore(tmp_path)
    ref = put(store)
    other = Scope(tenant=UUID(int=9), owner=SCOPE.owner)
    other_ref = put(store, scope=other)
    assert other_ref.key != ref.key and other_ref.sha256 == ref.sha256
    with pytest.raises(DocumentError, match='scope_mismatch'):
        store.read(other, ref, max_bytes=100)
    with pytest.raises(ValidationError):
        ObjectRef(scope=SCOPE, kind='source', object_id=UUID(int=3), key='../../outside', sha256='0'*64, byte_size=0)
    forged = ref.model_copy(update={'key': '../../outside'})
    with pytest.raises(DocumentError, match='invalid_reference'):
        store.read(SCOPE, forged, max_bytes=100)


def test_symlink_root_ancestor_and_object_rejected(tmp_path):
    real = tmp_path / 'real'; real.mkdir()
    link = tmp_path / 'link'; link.symlink_to(real, target_is_directory=True)
    for root in (link, link / 'child'):
        with pytest.raises(DocumentError, match='storage_error'):
            put(LocalObjectStore(root))
    store = LocalObjectStore(real)
    key = stable_id(SCOPE.identity(), 'source', str(UUID(int=3)))
    outside = tmp_path / 'outside'; outside.write_bytes(b'secret')
    (real / str(key)).symlink_to(outside)
    with pytest.raises(DocumentError, match='storage_error'):
        put(store)
    assert outside.read_bytes() == b'secret'


def test_oversized_stream_cleanup_and_short_reads(tmp_path):
    store = LocalObjectStore(tmp_path)
    with pytest.raises(DocumentError, match='source_too_large'):
        put(store, b'x'*101)
    assert not list(tmp_path.iterdir())
    class ShortReader(BytesIO):
        def read(self, size):
            return super().read(min(size, 1))
    ref = store.put(SCOPE, 'source', UUID(int=3), ShortReader(b'abc'), max_bytes=3)
    assert store.read(SCOPE, ref, max_bytes=3) == b'abc'


def test_concurrent_different_writes_never_overwrite(tmp_path):
    store = LocalObjectStore(tmp_path)
    def attempt(data):
        try:
            return put(store, data)
        except DocumentError:
            return None
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(attempt, [b'one', b'two']))
    successes = [r for r in results if r is not None]
    assert len(successes) == 1
    assert store.read(SCOPE, successes[0], max_bytes=100) in (b'one', b'two')
    assert len(list(tmp_path.iterdir())) == 1
