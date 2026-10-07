from datetime import datetime, timezone
from io import BytesIO
from uuid import UUID
import json

import pytest
from pydantic import ValidationError

from documents.config import ExtractionSettings
from documents.errors import DocumentError
from documents.extraction import extract
from documents.models import Scope, EvidenceRef, Span
from documents.parser import ParsedPage
from documents.provenance import resolve
from documents.serialization import serialize, deserialize
from documents.storage import LocalObjectStore

SCOPE = Scope(tenant=UUID(int=1), owner=UUID(int=2))
NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def run(tmp_path, data, mime='text/plain', **kwargs):
    return extract(BytesIO(data), scope=SCOPE, document_id=UUID(int=3),
                   display_filename=kwargs.pop('display_filename', 'fixture.pdf' if mime == 'application/pdf' else 'fixture.txt'),
                   declared_mime=mime, store=LocalObjectStore(tmp_path / 'objects'),
                   created_at=NOW, extracted_at=NOW, **kwargs)


def evidence(artifact, unit, block):
    return EvidenceRef(scope=SCOPE, document_version_id=artifact.document.document_version_id,
                       extraction_id=artifact.extraction_id, source_id=unit.source_id,
                       block_id=block.block_id, span=block.span)


def test_pdf_fidelity_matrix(tmp_path, pdf_bytes):
    artifact, ref = run(tmp_path, pdf_bytes(('text', 'blank', 'image', 'columns', 'graphics')), 'application/pdf')
    assert artifact.document.page_count == 5
    assert [u.physical_page for u in artifact.units] == [1, 2, 3, 4, 5]
    assert [u.status for u in artifact.units] == ['native_text', 'blank', 'image_only', 'native_text', 'unresolved']
    assert [u.decision.outcome for u in artifact.units] == ['native_accepted', 'native_accepted', 'ocr_required', 'native_accepted', 'manual_review']
    assert [u.text for u in artifact.units[:3]] == ['Page 1 alpha', '', '']
    assert 'Column beta' in artifact.units[3].text
    for unit in artifact.units:
        assert (unit.width, unit.height, unit.rotation) == (300, 400, 0)
        assert unit.printed_label is None and unit.ocr_confidence is None
        for block in unit.blocks:
            assert block.kind == 'text' and block.visual is None
            assert resolve(artifact, SCOPE, evidence(artifact, unit, block)) == block.source_text
    assert ref.kind == 'artifact'


def test_layout_is_explicit_not_invented(tmp_path, pdf_bytes):
    artifact, _ = run(tmp_path, pdf_bytes(('columns',)), 'application/pdf', structure_required=True)
    assert artifact.units[0].decision.outcome == 'layout_required'
    assert artifact.units[0].decision.next_tier == 'layout'
    assert artifact.units[0].blocks[0].geometry is None


@pytest.mark.parametrize('text', ['hello\nworld\n', 'αβ\r\n漢字 😀\n\nfin', '\ufeffUnicode\ré', 'a\nb', 'a'])
def test_text_exact_spans_and_replay(tmp_path, text):
    artifact, ref = run(tmp_path, text.encode('utf-8'))
    again, same_ref = run(tmp_path, text.encode('utf-8'))
    assert artifact == again and ref == same_ref
    assert artifact.document.page_count is None
    unit, = artifact.units
    assert unit.physical_page is None and unit.text == text
    assert ''.join(b.source_text for b in unit.blocks) == text
    for block in unit.blocks:
        assert resolve(artifact, SCOPE, evidence(artifact, unit, block)) == block.source_text
        assert block.normalized_text is None
    encoded = serialize(artifact)
    assert serialize(deserialize(encoded)) == encoded
    assert b'"page_count":null' in encoded
    with pytest.raises(ValidationError):
        unit.text = 'changed'


@pytest.mark.parametrize('data,mime,kwargs,category', [
    (b'', 'text/plain', {}, 'invalid_document'),
    (b'  \n', 'text/plain', {}, 'invalid_document'),
    (b'\xff', 'text/plain', {}, 'invalid_document'),
    (b'a\x00', 'text/plain', {}, 'invalid_document'),
    (b'hello', 'application/pdf', {}, 'unsupported_format'),
    (b'hello', 'image/png', {}, 'unsupported_format'),
    (b'hello', 'text/plain', {'display_filename': 'x.pdf'}, 'unsupported_format'),
    (b'hello', 'text/plain', {'display_filename': 'x.exe'}, 'unsupported_format'),
    (b'hello', 'text/plain', {'limits': ExtractionSettings(max_source_bytes=4)}, 'source_too_large'),
    (b'hello', 'text/plain', {'limits': ExtractionSettings(max_characters=4)}, 'extraction_limit_exceeded'),
    (b'a\nb\nc', 'text/plain', {'limits': ExtractionSettings(max_blocks=2)}, 'extraction_limit_exceeded'),
    (b'hello', 'text/plain', {'expected_sha256': '0'*64}, 'integrity_error'),
    (b'%PDF-1.4\nprivate document', 'application/pdf', {}, 'invalid_document'),
])
def test_input_failures(tmp_path, data, mime, kwargs, category, caplog):
    with pytest.raises(DocumentError, match=f'^{category}$'):
        run(tmp_path, data, mime, **kwargs)
    assert 'private document' not in caplog.text
    assert not (tmp_path / 'objects').exists()


def test_pdf_encrypted_truncated_and_page_limits(tmp_path, pdf_bytes):
    for data, limits, category in [
        (pdf_bytes(encrypted=True), ExtractionSettings(), 'encrypted_document'),
        (pdf_bytes()[:100], ExtractionSettings(), 'invalid_document'),
        (pdf_bytes(), ExtractionSettings(max_pages=2), 'page_limit_exceeded'),
        (pdf_bytes(), ExtractionSettings(max_characters=3), 'extraction_limit_exceeded'),
    ]:
        with pytest.raises(DocumentError, match=category):
            run(tmp_path, data, 'application/pdf', limits=limits)


def test_failed_page_accounted_and_runner_errors_sanitized(tmp_path):
    class Runner:
        version = 'fake/1'
        def parse(self, data, limits):
            return (ParsedPage(1, failed=True), ParsedPage(2, 'ok', has_graphics=False))
    artifact, _ = run(tmp_path, b'%PDF-fake', 'application/pdf', runner=Runner())
    assert len(artifact.units) == 2
    assert artifact.units[0].decision.outcome == 'failed'
    assert artifact.units[0].status == 'failed'
    class BrokenRunner(Runner):
        def parse(self, data, limits):
            raise RuntimeError('private source')
    with pytest.raises(DocumentError, match='^extraction_failed$'):
        run(tmp_path, b'%PDF-fake', 'application/pdf', runner=BrokenRunner())


def test_artifact_tampering_and_evidence_scope(tmp_path):
    artifact, _ = run(tmp_path, b'hello\nworld')
    payload = json.loads(serialize(artifact))
    for modify in [lambda p: p.update(schema_version='extraction/2'),
                   lambda p: p.update(units=[]),
                   lambda p: p['units'][0]['blocks'][0]['span'].update(end=999),
                   lambda p: p['document']['source'].update(key=str(UUID(int=0)))]:
        changed = json.loads(json.dumps(payload)); modify(changed)
        with pytest.raises(DocumentError, match='serialization_error'):
            deserialize(json.dumps(changed).encode())
    unit = artifact.units[0]; ref = evidence(artifact, unit, unit.blocks[0])
    with pytest.raises(DocumentError, match='scope_mismatch'):
        resolve(artifact, Scope(tenant=UUID(int=9), owner=UUID(int=2)), ref)
    with pytest.raises(DocumentError, match='invalid_reference'):
        resolve(artifact, SCOPE, ref.model_copy(update={'span': Span(start=0, end=999)}))
    with pytest.raises(DocumentError, match='serialization_error'):
        deserialize(b'{"schema_version":"extraction/1","schema_version":"extraction/1"}')


def test_profile_and_source_changes_get_distinct_identity(tmp_path):
    a, _ = run(tmp_path, b'one')
    b, _ = run(tmp_path, b'two')
    c, _ = run(tmp_path, b'one', structure_required=True)
    assert a.document.source.sha256 != b.document.source.sha256
    assert a.document.document_version_id != b.document.document_version_id
    assert a.extraction_id != c.extraction_id
    assert a.document.source == c.document.source


def test_legacy_pdf_behavior_is_unchanged(tmp_path, pdf_bytes):
    from rag.loaders.pdf_loader import load_pdf
    path = tmp_path / 'legacy.pdf'; path.write_bytes(pdf_bytes())
    assert load_pdf(str(path)) == 'Page 1 alpha\nPage 3 alpha\n'


def test_configuration_is_environment_driven(monkeypatch):
    monkeypatch.setenv('DOCUMENT_MAX_PAGES', '7')
    assert ExtractionSettings().max_pages == 7
    with pytest.raises(ValidationError):
        ExtractionSettings(max_pages=0)


def test_native_page_exception_keeps_inventory(tmp_path, pdf_bytes, monkeypatch, caplog):
    from pypdf import PageObject
    original = PageObject.extract_text
    calls = 0
    def fail_second(self, *args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise ValueError('private parser content')
        return original(self, *args, **kwargs)
    monkeypatch.setattr(PageObject, 'extract_text', fail_second)
    artifact, _ = run(tmp_path, pdf_bytes(), 'application/pdf')
    assert [u.status for u in artifact.units] == ['native_text', 'failed', 'native_text']
    assert artifact.units[1].physical_page == 2
    assert 'private parser content' not in caplog.text


def test_printed_labels_independent_of_physical_pages(tmp_path, pdf_bytes):
    artifact, _ = run(tmp_path, pdf_bytes(labels=True), 'application/pdf')
    assert [u.printed_label for u in artifact.units] == ['Appendix'] * 3
    assert [u.physical_page for u in artifact.units] == [1, 2, 3]


@pytest.mark.parametrize('field', ['extraction_id', 'source_id', 'block_id', 'line_start', 'has_native_text'])
def test_stored_identity_and_provenance_tampering_rejected(tmp_path, field):
    artifact, _ = run(tmp_path, b'hello')
    payload = json.loads(serialize(artifact))
    if field == 'extraction_id':
        payload[field] = str(UUID(int=99))
    elif field == 'source_id':
        payload['units'][0][field] = str(UUID(int=99))
    elif field == 'block_id':
        payload['units'][0]['blocks'][0][field] = str(UUID(int=99))
    elif field == 'line_start':
        payload['units'][0]['blocks'][0]['span'][field] = 99
    else:
        payload['units'][0]['decision']['observations'][field] = False
    with pytest.raises(DocumentError, match='serialization_error'):
        deserialize(json.dumps(payload).encode())


def test_artifact_byte_budget(tmp_path):
    with pytest.raises(DocumentError, match='extraction_limit_exceeded'):
        run(tmp_path, b'hello', limits=ExtractionSettings(max_artifact_bytes=10))
    # Source is immutable and may be orphaned until a future ledger/sweeper exists.
    assert len(list((tmp_path / 'objects').iterdir())) == 1


def test_blank_pdf_without_resource_dictionary(tmp_path):
    from pypdf import PdfWriter
    from pypdf.generic import NameObject
    writer = PdfWriter()
    page = writer.add_blank_page(width=100, height=100)
    del page[NameObject('/Resources')]
    stream = BytesIO(); writer.write(stream)
    artifact, _ = run(tmp_path, stream.getvalue(), 'application/pdf')
    assert artifact.units[0].status == 'blank'


def test_parser_diagnostics_suppressed_only_inside_runner(tmp_path, pdf_bytes, monkeypatch, caplog):
    import logging
    from pypdf import PageObject
    original = PageObject.extract_text
    def noisy(self, *args, **kwargs):
        logging.getLogger('pypdf._page').warning('synthetic private document content')
        return original(self, *args, **kwargs)
    monkeypatch.setattr(PageObject, 'extract_text', noisy)
    run(tmp_path, pdf_bytes(), 'application/pdf')
    assert not caplog.records
    logging.getLogger('pypdf._page').warning('legacy diagnostics still enabled')
    assert 'legacy diagnostics still enabled' in caplog.text


def test_invalid_page_metadata_is_sanitized(tmp_path):
    class Runner:
        version = 'fake/1'
        def parse(self, data, limits):
            return (ParsedPage(1, 'private source content', width=0),)
    with pytest.raises(DocumentError, match='^extraction_failed$'):
        run(tmp_path, b'%PDF-fake', 'application/pdf', runner=Runner())
    assert not (tmp_path / 'objects').exists()
