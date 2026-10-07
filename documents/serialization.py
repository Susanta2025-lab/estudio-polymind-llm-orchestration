"""Canonical UTF-8 JSON, explicit nulls, no pickle or implicit migrations."""

import json
from documents.errors import DocumentError
from documents.models import ExtractionArtifact


def serialize(artifact: ExtractionArtifact) -> bytes:
    try:
        # Revalidate even models constructed by copy/construct bypasses.
        data = artifact.model_dump(mode="json")
        ExtractionArtifact.model_validate(data)
        return json.dumps(data, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False).encode("utf-8")
    except Exception:
        raise DocumentError("serialization_error") from None


def deserialize(data: bytes, *, max_bytes: int = 32_000_000) -> ExtractionArtifact:
    if len(data) > max_bytes:
        raise DocumentError("serialization_error")
    try:
        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError("duplicate field")
                result[key] = value
            return result
        payload = json.loads(data.decode("utf-8"), object_pairs_hook=unique)
        return ExtractionArtifact.model_validate(payload)
    except Exception:
        raise DocumentError("serialization_error") from None
