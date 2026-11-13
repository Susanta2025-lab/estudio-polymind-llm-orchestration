"""Hash allowlist before parsing; every immutable write has a durable intent."""

from hashlib import sha256
from io import BytesIO

from documents.config import ExtractionSettings
from documents.extraction import extract
from documents.models import ObjectRef, stable_id
from documents.pilot.models import PilotError
from documents.pilot.parser import IsolatedPdfRunner


class RecordingStore:
    def __init__(self, store, control, session):
        self.store, self.control, self.session = store, control, session

    def put(self, scope, kind, object_id, stream, *, max_bytes, expected_sha256=None):
        data = stream.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise PilotError("pilot_source_refused")
        ref = ObjectRef(
            scope=scope,
            kind=kind,
            object_id=object_id,
            key=stable_id(scope.identity(), kind, str(object_id)),
            byte_size=len(data),
            sha256=sha256(data).hexdigest(),
        )
        self.control.object(self.session, ref, "WRITE_INTENT")
        written = self.store.put(
            scope,
            kind,
            object_id,
            BytesIO(data),
            max_bytes=max_bytes,
            expected_sha256=expected_sha256,
        )
        if ref != written:
            raise PilotError()
        self.control.object(self.session, ref, "WRITTEN")
        return ref

    def read(self, *args, **kwargs):
        return self.store.read(*args, **kwargs)

    def inspect(self, *args, **kwargs):
        return self.store.inspect(*args, **kwargs)


def intake(data, approval, scope, store, policy, *, now, limits=None):
    if (
        type(data) is not bytes
        or not data
        or len(data) > policy.max_source_bytes
        or scope != approval.owner
        or sha256(data).hexdigest() != approval.sha256
    ):
        raise PilotError("pilot_source_refused")
    base = limits or ExtractionSettings()
    bounded = ExtractionSettings(
        max_source_bytes=min(base.max_source_bytes, policy.max_source_bytes),
        max_pages=min(base.max_pages, policy.max_pages),
        max_characters=min(base.max_characters, policy.max_characters),
        max_blocks=min(base.max_blocks, 4000),
        max_artifact_bytes=base.max_artifact_bytes,
    )
    artifact, ref = extract(
        BytesIO(data),
        scope=scope,
        document_id=approval.document_id,
        display_filename=approval.filename,
        declared_mime=approval.mime,
        store=store,
        limits=bounded,
        expected_sha256=approval.sha256,
        created_at=now,
        extracted_at=now,
        runner=IsolatedPdfRunner(),
    )
    if any(
        u.decision.outcome != "native_accepted"
        or u.status == "failed"
        or u.decision.observations.has_images is not False
        or u.decision.observations.has_graphics is not False
        for u in artifact.units
    ):
        raise PilotError("pilot_source_refused")
    return artifact, ref
