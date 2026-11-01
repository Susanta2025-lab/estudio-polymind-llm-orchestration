"""Strict bounded deterministic JSON for immutable digestion objects."""

import json
from io import BytesIO

from documents.digestion.diagnostics import PydanticDiagnostic, classify_pydantic
from documents.digestion.diagnostics import ValidationReason as Reason
from documents.digestion.models import DigestionError, ValidationDiagnostic
from documents.jobs.models import canonical, fingerprint
from documents.models import stable_id


def encode(model):
    reason = Reason.CANONICAL_ENCODING_FAILED
    try:
        payload = model.model_dump(mode='json')
        reason = Reason.CANONICAL_REVALIDATION_FAILED
        type(model).model_validate(payload)
        reason = Reason.CANONICAL_ENCODING_FAILED
        return canonical(payload).encode('ascii')
    except Exception:
        raise DigestionError(
            "inference_contract_error",
            diagnostic=ValidationDiagnostic.CANONICAL_SERIALIZATION,
            reason=reason,
        ) from None


class _DuplicateJSONKey(ValueError):
    pass


def decode(data, model, limit):
    if not isinstance(data, bytes) or len(data) > limit:
        raise DigestionError(
            "synthesis_limit_exceeded",
            diagnostic=ValidationDiagnostic.RESPONSE_LIMIT,
            reason=Reason.RAW_RESPONSE_LIMIT,
        )
    try:
        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise _DuplicateJSONKey()
                result[key] = value
            return result
        payload = json.loads(data, object_pairs_hook=unique)
    except _DuplicateJSONKey:
        raise DigestionError(
            "inference_contract_error",
            diagnostic=ValidationDiagnostic.DUPLICATE_JSON_KEY,
            reason=Reason.DUPLICATE_JSON_KEY,
        ) from None
    except Exception:
        raise DigestionError(
            "inference_contract_error",
            diagnostic=ValidationDiagnostic.JSON_DECODE,
            reason=Reason.MALFORMED_JSON,
        ) from None
    try:
        return model.model_validate(payload)
    except Exception as exc:  # noqa: BLE001 - Preserve existing fail-closed normalization.
        try:
            detail = classify_pydantic(exc)
        except Exception:  # noqa: BLE001 - Supplemental diagnostics cannot mask rejection.
            detail = PydanticDiagnostic(Reason.OTHER_PYDANTIC_VALIDATION)
        raise DigestionError(
            "inference_contract_error",
            diagnostic=ValidationDiagnostic.PYDANTIC_VALIDATION,
            reason=detail.reason,
            pydantic=detail,
        ) from None


def put(store, scope, model, limit):
    data = encode(model)
    if len(data) > limit:
        raise DigestionError('synthesis_limit_exceeded')
    identity = stable_id('digestion-object/1', fingerprint(model.model_dump(mode='json')))
    return store.put(scope, 'artifact', identity, BytesIO(data), max_bytes=limit)


def read(store, scope, ref, model, limit):
    return decode(store.read(scope, ref, max_bytes=limit), model, limit)
