"""Synthetic governed execution only; all network entry points are denied."""

import json
from uuid import UUID

import pytest

from documents.digestion import codec
from documents.digestion.models import DigestionError, ValidationDiagnostic
from tests.approval_helpers import approval_signer  # noqa: F401
from tests.integration.test_single_call_harness import offline, rig  # noqa: F401
from tests.unit.test_security_entra import entra  # noqa: F401
from tests.unit.test_security_identity import identity  # noqa: F401

MARKER = "SYNTHETIC_SECRET_MODEL_EXCEPTION"
UNKNOWN = str(UUID(int=1))


@pytest.mark.parametrize(
    "case,diagnostic,category",
    [
        ("valid", None, None),
        ("json", "json_decode", "serialization_error"),
        ("duplicate", "duplicate_json_key", "serialization_error"),
        ("uuid", "pydantic_validation", "serialization_error"),
        ("extra", "pydantic_validation", "serialization_error"),
        ("stage", "stage_binding", "serialization_error"),
        ("kind", "stage_binding", "serialization_error"),
        ("outcome", "stage_binding", "serialization_error"),
        ("claim", "claim_identity", "serialization_error"),
        ("origin", "claim_identity", "serialization_error"),
        ("contract", "claim_contract", "serialization_error"),
        ("evidence", "evidence_validation", "invalid_reference"),
        ("lineage", "evidence_validation", "invalid_reference"),
        ("coverage", "coverage_validation", "extraction_failed"),
        ("canonical", "canonical_serialization", "serialization_error"),
        ("roundtrip", "canonical_serialization", "serialization_error"),
        ("limit", "response_limit", "extraction_limit_exceeded"),
    ],
)
def test_governed_validation_audit(rig, monkeypatch, case, diagnostic, category):  # noqa: F811
    cfg, run, http, ledger, authority, principal, *_ = rig

    def corrupt(value):
        data = json.loads(value["choices"][0]["message"]["content"])
        claim = data["claims"][0]
        claim["text"] = MARKER
        if case == "uuid":
            data["stage_id"] = MARKER
        elif case == "extra":
            data[MARKER] = MARKER
        elif case == "stage":
            data["stage_id"] = UNKNOWN
        elif case == "kind":
            data["kind"] = "reduction"
        elif case == "outcome":
            data["outcome"] = "unavailable"
        elif case == "claim":
            claim["claim_id"] = UNKNOWN
        elif case == "origin":
            claim["originating_stage"] = UNKNOWN
        elif case == "contract":
            claim.update(kind="commentary", subject=MARKER)
        elif case == "evidence":
            claim["evidence_ids"] = [UNKNOWN]
        elif case == "lineage":
            claim["lineage"] = [{"stage_id": UNKNOWN, "claim_id": UNKNOWN}]
        elif case == "coverage":
            claim.update(kind="commentary", evidence_ids=[])
        raw = json.dumps(data)
        if case == "json":
            raw = "{" + MARKER
        elif case == "duplicate":
            raw = '{"x":1,"x":2}'
        elif case == "limit":
            # Canonical byte ceiling is downstream of the transport response bound.
            claim["text"] = "\u0800" * 1600
            raw = json.dumps(data, ensure_ascii=False)
        value["choices"][0]["message"]["content"] = raw
        return value

    http.transform = corrupt
    if case in ("canonical", "roundtrip"):

        def fail(*args, **kwargs):
            raise ValueError(MARKER)

        if case == "canonical":
            original_canonical = codec.canonical

            def canonical(payload):
                if payload.get("schema_version") == "stage-result/1":
                    fail()
                return original_canonical(payload)

            monkeypatch.setattr(codec, "canonical", canonical)
        else:
            from documents.digestion.models import StageResult

            original = StageResult.model_validate
            calls = 0

            def validate(*args, **kwargs):
                nonlocal calls
                calls += 1
                if calls == 2:
                    fail()
                return original(*args, **kwargs)

            monkeypatch.setattr(StageResult, "model_validate", validate)
    outcome = run()
    assert len(http.sent) == outcome["calls"] == 1
    assert outcome["provider_acceptance"] == "completed_strict_response"
    assert outcome["accounting_failed"] is False
    assert ledger.usage(principal, authority)[0]["state"] == "SETTLED"
    if diagnostic is None:
        assert outcome["state"] == "SUCCEEDED"
        assert outcome["application_validation"] == "accepted"
        assert "validation_diagnostic" not in outcome
        assert "failure" not in outcome
    else:
        assert outcome["state"] == "FAILED"
        assert outcome["application_validation"] == "failed"
        assert outcome["failure"] == category
        assert outcome["validation_diagnostic"] == diagnostic
    path = cfg.audit_directory / "outcome.json"
    assert json.loads(path.read_text()) == outcome
    assert path.stat().st_mode & 0o777 == 0o600
    assert MARKER not in path.read_text()
    before = path.read_bytes()
    from tests.performance.foundry_single_call import durable_json

    with pytest.raises(FileExistsError):
        durable_json(path, {"replacement": True})
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "diagnostic", [None, MARKER, "claim_identity", {"secret": MARKER}]
)
def test_untyped_diagnostics_are_omitted(diagnostic):
    error = DigestionError("inference_contract_error", diagnostic=diagnostic)
    assert error.validation_diagnostic is None
    assert str(error) == "inference_contract_error"


def test_raw_response_limit_and_duplicate_privacy():
    from documents.digestion.models import StageResult

    for raw, limit, expected in [
        (b" " * 11, 10, ValidationDiagnostic.RESPONSE_LIMIT),
        (
            b'{"SYNTHETIC_SECRET_MODEL_EXCEPTION":1,"SYNTHETIC_SECRET_MODEL_EXCEPTION":2}',
            1000,
            ValidationDiagnostic.DUPLICATE_JSON_KEY,
        ),
    ]:
        with pytest.raises(DigestionError) as caught:
            codec.decode(raw, StageResult, limit)
        assert caught.value.validation_diagnostic is expected
        assert MARKER not in str(caught.value)


@pytest.mark.parametrize("value", [None, MARKER, "claim_identity"])
def test_missing_or_forged_diagnostic_cannot_suppress_failure(rig, monkeypatch, value):  # noqa: F811
    from tests.performance import foundry_single_call as harness

    def reject(*args):
        error = DigestionError("inference_contract_error")
        error.validation_diagnostic = value
        raise error

    monkeypatch.setattr(harness, "validate_result", reject)
    _, run, http, *_ = rig
    outcome = run()
    assert outcome["state"] == "FAILED"
    assert outcome["failure"] == "serialization_error"
    assert outcome["application_validation"] == "failed"
    assert "validation_diagnostic" not in outcome
    assert len(http.sent) == 1
    assert MARKER not in json.dumps(outcome)
