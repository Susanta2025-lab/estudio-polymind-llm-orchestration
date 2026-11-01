"""Explicitly callable OFFLINE diagnostic; never imported by live execution.

This checks the exact production schema locally, not Azure service certification
or application acceptance. No response, schema error path or message is retained.
"""

import json
from enum import Enum

from jsonschema import Draft202012Validator

from documents.digestion.managed import generation_schema
from llm.azure_schema import provider_schema


class SchemaObservation(Enum):
    RESPONSE_LIMIT = "response_limit"
    INVALID_JSON = "invalid_json"
    SCHEMA_REJECTED = "schema_rejected"
    SCHEMA_CONFORMANT = "schema_conformant"


def observe_schema(raw: bytes, *, limit: int = 10000) -> SchemaObservation:
    if type(raw) is not bytes or len(raw) > limit:
        return SchemaObservation.RESPONSE_LIMIT

    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError
            result[key] = value
        return result

    def invalid_constant(value):
        raise ValueError

    try:
        value = json.loads(
            raw, object_pairs_hook=unique, parse_constant=invalid_constant
        )
    except (ValueError, TypeError, RecursionError):
        return SchemaObservation.INVALID_JSON
    validator = Draft202012Validator(provider_schema(generation_schema()))
    return (
        SchemaObservation.SCHEMA_CONFORMANT
        if validator.is_valid(value)
        else SchemaObservation.SCHEMA_REJECTED
    )
