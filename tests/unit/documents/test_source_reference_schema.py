"""Bounded source enums through the production converter and HTTP request builder."""

from dataclasses import replace
from uuid import UUID

import pytest

# Frozen canonical-output v9 characterization; v10 has separate wire regressions.
pytestmark = pytest.mark.usefixtures("managed_v9")

from jsonschema import Draft202012Validator
from pydantic import ValidationError

from tests.historical_managed import generation_schema
from documents.digestion.sizing import escaped_size
from documents.jobs.models import canonical
from llm.azure_schema import provider_schema
from llm.inference import InferenceContextError
from tests.integration.test_final_offline_azure_compatibility import schema_nodes
from tests.unit.documents.test_managed_sizing import adapter
from tests.unit.test_structured_provider import Response, client, payload, request


@pytest.mark.parametrize("count", [0, 1, 4, 128, 129, 256])
def test_bounded_source_schema_actual_converter_and_provider_serialization(count):
    allowed = [str(UUID(int=i + 1)) for i in range(count)]
    schema = generation_schema(allowed)
    converted = provider_schema(schema)
    Draft202012Validator.check_schema(converted)
    source = converted["$defs"]["SourceEvidence"]
    branches = source.get("anyOf", [source])
    assert [v for branch in branches for v in branch.get("enum", [])] == allowed
    assert all(len(branch.get("enum", [])) <= 128 for branch in branches)
    assert all(sum(map(len, branch.get("enum", []))) <= 4608 for branch in branches)
    assert sum(len(node.get("enum", [])) for node in schema_nodes(converted)) < 500
    for name, field in [
        ("Claim", "evidence_ids"),
        ("Claim", "contradicting_evidence_ids"),
        ("Qualification", "evidence_ids"),
    ]:
        assert converted["$defs"][name]["properties"][field]["items"] == {
            "$ref": "#/$defs/SourceEvidence"
        }
    # Prove the fixed 128-byte reserve covers enum scaffolding at both branches.
    growth = len(canonical(schema)) - len(canonical(generation_schema([])))
    assert growth <= 128 + escaped_size(allowed)
    instance = {
        "stage_id": str(UUID(int=998)),
        "kind": "analysis",
        "claims": [],
        "schema_version": "stage-result/1",
        "outcome": "analyzed",
        "open_questions": [],
        "limitations": [],
    }
    provider = client(Response(payload()), kind="foundry")
    generation = replace(
        request(structured_output="json_schema", schema_profile="azure-strict/1"),
        schema=schema,
    )
    provider.execute(generation)
    sent = provider.http_client.calls[0][1]["json"]
    assert sent["response_format"]["json_schema"]["schema"] == converted
    assert sent["response_format"]["json_schema"]["strict"] is True
    assert len(provider.http_client.calls) == 1
    Draft202012Validator(converted).validate(instance)
    # Test each reference position with all members, foreign UUIDs, malformed values.
    for value, valid in [(v, True) for v in allowed] + [
        (str(UUID(int=99999)), False),
        ("bad-uuid", False),
    ]:
        for field in ("evidence_ids", "contradicting_evidence_ids", "qualification"):
            claim = {
                "claim_id": str(UUID(int=997)),
                "originating_stage": instance["stage_id"],
                "text": "Synthetic.",
                "kind": "commentary",
                "status": "supported",
                "subject": None,
                "stance": "unknown",
                "evidence_ids": [],
                "contradicting_evidence_ids": [],
                "qualifications": [],
                "lineage": [],
            }
            if field == "qualification":
                claim["qualifications"] = [
                    {"text": "Condition.", "evidence_ids": [value]}
                ]
            else:
                claim[field] = [value]
            instance["claims"] = [claim]
            assert Draft202012Validator(converted).is_valid(instance) == valid


def test_empty_set_rejects_every_uuid_but_keeps_empty_arrays():
    schema = generation_schema([])
    assert schema["$defs"]["SourceEvidence"] == {"type": "null"}
    # Null items cannot be consumed by the unchanged UUID result model either.
    from documents.digestion.models import Qualification

    with pytest.raises(ValidationError):
        Qualification(text="Condition", evidence_ids=[None])


def test_excess_schema_cardinality_fails_before_transport():
    with pytest.raises(InferenceContextError):
        generation_schema([str(UUID(int=i + 1)) for i in range(257)])
    settings = adapter(7000).settings
    with pytest.raises(ValidationError, match="at most 256"):
        type(settings).model_validate(
            {**settings.model_dump(mode="json"), "max_evidence": 257}
        )


def test_request_schemas_are_isolated_and_static_schema_remains_unchanged():
    generic = generation_schema()
    first = generation_schema([str(UUID(int=1))])
    second = generation_schema([str(UUID(int=2))])
    first["$defs"]["SourceEvidence"]["enum"].append("bad")
    assert second["$defs"]["SourceEvidence"]["enum"] == [str(UUID(int=2))]
    assert generation_schema() == generic and "SourceEvidence" not in generic["$defs"]
