"""Strict bounded deterministic JSON for immutable digestion objects."""

import json
from io import BytesIO

from documents.jobs.models import canonical, fingerprint
from documents.models import stable_id
from documents.digestion.models import DigestionError


def encode(model):
    try:
        payload = model.model_dump(mode='json')
        type(model).model_validate(payload)
        return canonical(payload).encode('ascii')
    except Exception:
        raise DigestionError('inference_contract_error') from None


def decode(data, model, limit):
    if not isinstance(data, bytes) or len(data) > limit:
        raise DigestionError('synthesis_limit_exceeded')
    try:
        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError()
                result[key] = value
            return result
        return model.model_validate(json.loads(data, object_pairs_hook=unique))
    except Exception:
        raise DigestionError('inference_contract_error') from None


def put(store, scope, model, limit):
    data = encode(model)
    if len(data) > limit:
        raise DigestionError('synthesis_limit_exceeded')
    identity = stable_id('digestion-object/1', fingerprint(model.model_dump(mode='json')))
    return store.put(scope, 'artifact', identity, BytesIO(data), max_bytes=limit)


def read(store, scope, ref, model, limit):
    return decode(store.read(scope, ref, max_bytes=limit), model, limit)
