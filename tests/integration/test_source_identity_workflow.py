"""Synthetic v8 failure shape through unchanged validation and durable workflow."""

import json
from copy import deepcopy
from hashlib import sha256
from uuid import UUID

import pytest

# Frozen canonical-output v9 characterization; v10 has separate wire regressions.
pytestmark = pytest.mark.usefixtures("managed_v9")

from jsonschema import Draft202012Validator
from test_phase17hl_offline_e2e import assert_accounting, reopen
from test_phase17hl_offline_e2e import l1 as l1  # noqa: PLC0414
from test_phase17hl_offline_e2e import offline as offline  # noqa: PLC0414
from test_reducer_sizing_offline_workflow import sized_transform

from documents.digestion.codec import encode, read
from documents.digestion.managed import classify_managed
from documents.digestion.models import Checkpoint, DigestionError, StageResult
from documents.digestion.validation import EvidenceIndex, validate_result
from documents.jobs.sqlite import SQLiteJobLedger
from documents.models import stable_id
from documents.storage import LocalObjectStore
from llm.azure_schema import provider_schema
from tests.integration.test_final_offline_azure_compatibility import (
    contracts as contracts,  # noqa: PLC0414
)
from tests.reducer_sizing_fixtures import eight_claim_result


def mixed_uuid(allowed):
    # The observable v8 shape: first four groups of one ID, final group of another.
    value = allowed[1].rsplit("-", 1)[0] + "-" + allowed[3].rsplit("-", 1)[1]
    assert str(UUID(value)) == value and value not in allowed
    return value


def corrupt_sources(data, fault):
    allowed = sorted({e for c in data["claims"] for e in c["evidence_ids"]})
    assert len(allowed) == 4
    if fault == "valid":
        return data
    foreign = mixed_uuid(allowed)
    claim = data["claims"][0 if fault == "first" else 6]
    if fault in ("mixed", "first", "foreign", "claim_id", "stage_id", "malformed"):
        value = {
            "foreign": str(UUID(int=90123)),
            "claim_id": claim["claim_id"],
            "stage_id": data["stage_id"],
            "malformed": "not-a-uuid",
        }.get(fault, foreign)
        claim["evidence_ids"] = [allowed[0], value]
    elif fault == "qualification":
        claim["qualifications"] = [
            {"text": "Synthetic condition.", "evidence_ids": [foreign]}
        ]
    elif fault == "contradiction":
        claim["contradicting_evidence_ids"] = [foreign]
    elif fault == "duplicate":
        claim["evidence_ids"] = [allowed[0], allowed[0]]
    elif fault == "coverage":
        for item in data["claims"]:
            item["evidence_ids"] = [e for e in item["evidence_ids"] if e != allowed[3]]
    else:
        raise AssertionError(fault)
    return data


FAULTS = [
    "valid",
    "mixed",
    "foreign",
    "first",
    "qualification",
    "contradiction",
    "claim_id",
    "stage_id",
    "malformed",
    "duplicate",
    "coverage",
]


@pytest.mark.parametrize("fault", FAULTS)
def test_eight_claim_four_source_shape_and_independent_g2(contracts, fault):
    record = contracts["chunk"]
    data = eight_claim_result(record.request).model_dump(mode="json")
    # Remove qualifications to match the observed chunk's empty annotations.
    for claim in data["claims"]:
        claim["qualifications"] = []
    original = deepcopy(data)
    data = corrupt_sources(data, fault)
    assert len(data["claims"]) == 8
    assert all(
        c["claim_id"] == str(stable_id(data["stage_id"], str(i)))
        and c["originating_stage"] == data["stage_id"]
        and not c["lineage"]
        for i, c in enumerate(data["claims"])
    )
    validator = Draft202012Validator(provider_schema(record.generation.schema))
    # Enum membership cannot enforce uniqueness or full-source coverage.
    assert validator.is_valid(data) == (fault in ("valid", "duplicate", "coverage"))
    raw = json.dumps(data, separators=(",", ":")).encode()
    before = sha256(raw).hexdigest()
    if fault == "valid":
        assert validate_result(
            raw, record.request, record.index
        ) == StageResult.model_validate(data)
    else:
        with pytest.raises(DigestionError) as caught:
            validate_result(raw, record.request, record.index)
        expected = {
            "qualification": "invalid_qualification_source",
            "duplicate": "duplicate_evidence",
            "coverage": "missing_source_coverage",
            "malformed": "pydantic_validation",
        }.get(fault, "foreign_evidence")
        if fault == "malformed":
            assert caught.value.validation_diagnostic.value == expected
        else:
            assert caught.value.validation_reason.value == expected
        assert classify_managed(caught.value).classification == "NON_RETRYABLE"
    assert sha256(raw).hexdigest() == before  # No repair, deletion or reassignment.
    if fault == "mixed":
        allowed = {p.evidence_id() for p in record.request.source_data}
        assert len(allowed) == 4
        returned = {UUID(e) for c in data["claims"] for e in c["evidence_ids"]}
        assert allowed < returned
        assert (
            data["claims"][6]["evidence_ids"][0]
            == original["claims"][0]["evidence_ids"][0]
        )
        assert UUID(data["claims"][6]["evidence_ids"][1]) not in allowed


@pytest.mark.parametrize("stage,calls", [("chunk", 1), ("structural", 2), ("root", 3)])
@pytest.mark.parametrize(
    "fault", ["mixed", "qualification", "claim_id", "stage_id", "malformed"]
)
def test_invalid_sources_stop_before_checkpoint_and_preserve_usage_and_history(
    l1, stage, calls, fault
):
    sized = sized_transform(l1, 6500, stage)
    rejected, previous = [], []

    def transform(value, current):
        value = sized(value, current)
        if current != stage:
            return value
        request = l1.state.requests[-1]
        data = corrupt_sources(json.loads(value), fault)
        raw = json.dumps(data, separators=(",", ":"))
        assert len(data["claims"]) == 8
        assert not Draft202012Validator(
            provider_schema(l1.state.generations[-1].schema)
        ).is_valid(data)
        for step in l1.state.jobs.steps(
            l1.state.artifact.document.scope, l1.state.job.job_id
        ):
            for ref in step.manifest:
                previous.append(
                    (
                        ref,
                        l1.state.store.read(
                            ref.scope, ref, max_bytes=request.profile.max_artifact_bytes
                        ),
                    )
                )
        rejected.append(raw)
        return raw

    state = l1(transform)
    assert state.result["job_state"] == "FAILED"
    assert state.result["terminal_category"] == (
        "serialization_error" if fault == "malformed" else "invalid_reference"
    )
    assert_accounting(state, calls)
    assert len(state.sent) == len(state.generations) == len(state.requests) == calls
    assert "publication" not in state.result and "questions" not in state.result
    assert not hasattr(state, "replica")
    assert state.result["provider_records"][-1]["response"] == rejected[0]
    assert all(r["outcome"] == "success" for r in state.result["provider_records"])
    scope = state.artifact.document.scope
    jobs, store = (
        SQLiteJobLedger(state.jobs.settings),
        LocalObjectStore(state.root / "objects"),
    )
    steps = jobs.steps(scope, state.job.job_id)
    (failed,) = [s for s in steps if s.state == "FAILED"]
    (attempt,) = jobs.attempts(scope, state.job.job_id, failed.step_id)
    assert (
        attempt.classification == "NON_RETRYABLE"
        and failed.attempt_count == 1
        and not failed.manifest
    )
    assert all(
        s.attempt_count == 0 and not s.manifest for s in steps if s.state == "CANCELLED"
    )
    for ref, raw in previous:
        assert (
            store.read(scope, ref, max_bytes=state.plan.profile.max_artifact_bytes)
            == raw
        )
    for request in state.requests[:-1]:
        saved = next(s for s in steps if s.spec.unit_id == str(request.stage_id))
        cp = read(
            store,
            scope,
            saved.manifest[0],
            Checkpoint,
            request.profile.max_artifact_bytes,
        )
        assert (
            validate_result(encode(cp.result), request, EvidenceIndex(state.artifact))
            == cp.result
        )
    with pytest.raises(DigestionError):
        reopen(state)
