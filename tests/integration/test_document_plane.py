"""Local end-to-end object/artifact/evidence round trip without external services."""

from datetime import datetime, timezone
import hashlib
from io import BytesIO
from uuid import UUID

import pytest
from documents.config import ExtractionSettings
from documents.extraction import extract
from documents.models import EvidenceRef, Scope
from documents.provenance import resolve
from documents.serialization import deserialize
from documents.storage import LocalObjectStore


@pytest.mark.parametrize('filename', ['../../escape.txt', '/absolute.txt', r'..\..\escape.txt'])
def test_source_artifact_and_provenance_roundtrip(tmp_path, filename):
    source = ('Line αβ 😀\r\n' * 1000).encode('utf-8')
    scope = Scope(tenant=UUID(int=10), owner=UUID(int=20))
    store = LocalObjectStore(tmp_path / 'isolated')
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    artifact, ref = extract(BytesIO(source), scope=scope, document_id=UUID(int=30),
                            display_filename=filename, declared_mime='text/plain', store=store,
                            created_at=now, extracted_at=now,
                            limits=ExtractionSettings(max_source_bytes=len(source)),
                            expected_sha256=hashlib.sha256(source).hexdigest())
    assert store.read(scope, artifact.document.source, max_bytes=len(source)) == source
    restored = deserialize(store.read(scope, ref, max_bytes=2_000_000))
    assert restored == artifact
    unit = restored.units[0]
    block = unit.blocks[-1]
    evidence = EvidenceRef(scope=scope, document_version_id=restored.document.document_version_id,
                           extraction_id=restored.extraction_id, source_id=unit.source_id,
                           block_id=block.block_id, span=block.span)
    assert resolve(restored, scope, evidence) == 'Line αβ 😀\r\n'
    assert block.span.line_start == 1000
    assert len(list((tmp_path / 'isolated').iterdir())) == 2
    assert list(tmp_path.iterdir()) == [tmp_path / 'isolated']
