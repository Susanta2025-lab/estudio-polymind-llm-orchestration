# ruff: noqa: F811
"""Synthetic rule attribution, privacy and frozen generation requests only."""

import json
from copy import deepcopy
from dataclasses import asdict, replace
from hashlib import sha256
from pathlib import Path
from uuid import UUID

import pytest
from pydantic import ValidationError

from documents.digestion.codec import decode
from documents.digestion.diagnostics import (
    PydanticDiagnostic,
    ValidationReason,
    classify_pydantic,
    safe_path,
)
from documents.digestion.models import DigestionError, StageResult
from documents.digestion.validation import validate_result
from llm.inference import (
    InferenceOutputLimitError,
    InferenceResponseError,
    InferenceUsage,
)
from llm.structured import ProviderResultMetadata
from tests.integration.test_final_offline_azure_compatibility import (
    contracts,
)
from tests.performance.foundry_schema_diagnostics import (
    SchemaObservation,
    observe_schema,
)
from tests.source_contracts import DOMAIN_NAMES, assert_source_contract, source_sections
from tests.unit.test_structured_provider import Response, client, payload, request

SECRET = "SYNTHETIC_PRIVATE_DOCUMENT_API_TOKEN"
FOREIGN = str(UUID(int=1700777))


def rejected(record, data, reason):
    with pytest.raises(DigestionError) as caught:
        validate_result(json.dumps(data).encode(), record.request, record.index)
    error = caught.value
    assert error.validation_reason.value == reason
    assert SECRET not in str(error)
    if error.pydantic_diagnostic:
        evidence = json.dumps(error.pydantic_diagnostic.evidence())
        assert SECRET not in evidence and FOREIGN not in evidence
    return error


@pytest.mark.parametrize(
    "case,reason,path",
    [
        ("claim_uuid", "invalid_uuid", ["claims", 0, "claim_id"]),
        ("stage_uuid", "invalid_uuid", ["stage_id"]),
        ("evidence_uuid", "invalid_uuid", ["claims", 0, "evidence_ids", 0]),
        ("subject_pattern", "invalid_subject_token", ["claims", 0, "subject"]),
        ("subject_length", "invalid_subject_token", ["claims", 0, "subject"]),
        ("text_empty", "invalid_text_bound", ["claims", 0, "text"]),
        ("text_long", "invalid_text_bound", ["claims", 0, "text"]),
        ("missing", "missing_required_field", ["stage_id"]),
        ("enum", "invalid_enum", ["outcome"]),
        ("extra", "forbidden_extra_field", []),
        ("type", "invalid_field_type", ["claims", 0, "text"]),
        ("multiple", "invalid_uuid", ["stage_id"]),
    ],
)
def test_pydantic_reason_and_safe_location(contracts, case, reason, path):
    r = contracts["chunk"]
    data = json.loads(r.raw)
    claim = data["claims"][0]
    if case == "claim_uuid":
        claim["claim_id"] = SECRET
    elif case == "stage_uuid":
        data["stage_id"] = SECRET
    elif case == "evidence_uuid":
        claim["evidence_ids"] = [SECRET]
    elif case == "subject_pattern":
        claim["subject"] = "private content " + SECRET
    elif case == "subject_length":
        claim["subject"] = SECRET * 10
    elif case == "text_empty":
        claim["text"] = ""
    elif case == "text_long":
        claim["text"] = SECRET * 200
    elif case == "missing":
        del data["stage_id"]
    elif case == "enum":
        data["outcome"] = SECRET
    elif case == "extra":
        claim[SECRET] = SECRET
    elif case == "type":
        claim["text"] = {"secret": SECRET}
    elif case == "multiple":
        data.update(stage_id=SECRET, outcome=SECRET)
        claim[SECRET] = SECRET
    error = rejected(r, data, reason)
    info = error.pydantic_diagnostic.evidence()
    assert info["path"] == path
    assert info["error_count"] == (3 if case == "multiple" else 1)


@pytest.mark.parametrize(
    "path",
    [
        (SECRET,),
        ("claims", 0, SECRET),
        ("claims", FOREIGN, "text"),
        ("claims", -1, "text"),
        ("claims", True, "text"),
        ("claims", 64, "text"),
        ("claims", 0, "qualifications", 64, "text"),
        ("claims", 0, "evidence_ids", 4096),
        ("claims", 0, "subject", "str"),
        ("claims", 0, "lineage", 0, FOREIGN),
        [],
        None,
    ],
)
def test_unsafe_locations_are_discarded(path):
    assert safe_path(path) == ()


@pytest.mark.parametrize(
    "path",
    [
        ("stage_id",),
        ("claims", 0, "claim_id"),
        ("claims", 63, "text"),
        ("claims", 0, "qualifications", 0, "text"),
        ("claims", 0, "qualifications", 0, "evidence_ids", 4095),
        ("claims", 0, "lineage", 0, "stage_id"),
    ],
)
def test_known_locations_survive(path):
    assert safe_path(path) == path


def test_pydantic_order_is_independent_of_errors_iteration():
    errors = [
        {
            "type": "uuid_parsing",
            "loc": ("stage_id",),
            "input": SECRET,
            "ctx": {"error": SECRET},
        },
        {
            "type": "literal_error",
            "loc": ("outcome",),
            "input": SECRET,
            "ctx": {"expected": SECRET},
        },
    ]
    first = classify_pydantic(ValidationError.from_exception_data("private", errors))
    second = classify_pydantic(
        ValidationError.from_exception_data("private", errors[::-1])
    )
    assert first == second
    assert first.reason is ValidationReason.INVALID_UUID
    assert SECRET not in json.dumps(first.evidence())


def test_unknown_pydantic_error_and_saturated_count():
    error = ValidationError.from_exception_data(
        "private",
        [{"type": "missing", "loc": (SECRET,), "input": SECRET} for _ in range(70)],
    )
    result = classify_pydantic(error)
    assert result.evidence() == {
        "reason": "other_pydantic_validation",
        "path": [],
        "error_count": 64,
    }
    assert (
        classify_pydantic(ValueError(SECRET)).reason
        is ValidationReason.OTHER_PYDANTIC_VALIDATION
    )
    assert PydanticDiagnostic(SECRET, (SECRET,), 999).evidence() == {}


@pytest.mark.parametrize(
    "case,reason",
    [
        ("stage", "stage_id_mismatch"),
        ("kind", "stage_kind_mismatch"),
        ("claim", "claim_id_mismatch"),
        ("duplicate_claim", "duplicate_claim_id"),
        ("origin", "originating_stage_mismatch"),
        ("subject", "subject_on_nonfact"),
        ("unavailable_claims", "unavailable_with_claims"),
        ("unavailable_limitation", "unavailable_missing_limitation"),
        ("empty_analyzed", "analyzed_without_claims"),
        ("foreign", "foreign_evidence"),
        ("duplicate", "duplicate_evidence"),
        ("qualification", "invalid_qualification_source"),
        ("child", "invalid_child_link"),
        ("coverage", "missing_source_coverage"),
        ("unsupported", "unsupported_fact"),
    ],
)
def test_application_reasons(contracts, case, reason):
    r = contracts["chunk"]
    data = json.loads(r.raw)
    c = data["claims"][0]
    if case == "stage":
        data["stage_id"] = FOREIGN
    elif case == "kind":
        data["kind"] = "reduction"
    elif case == "claim":
        c["claim_id"] = FOREIGN
    elif case == "duplicate_claim":
        data["claims"].append(deepcopy(c))
    elif case == "origin":
        c["originating_stage"] = FOREIGN
    elif case == "subject":
        c.update(kind="commentary", subject="valid-token")
    elif case == "unavailable_claims":
        data["outcome"] = "unavailable"
    elif case == "unavailable_limitation":
        data.update(outcome="unavailable", claims=[], limitations=[])
    elif case == "empty_analyzed":
        data["claims"] = []
    elif case == "foreign":
        c["evidence_ids"] = [FOREIGN]
    elif case == "duplicate":
        c["evidence_ids"] *= 2
    elif case == "qualification":
        c["qualifications"] = [{"text": SECRET, "evidence_ids": [FOREIGN]}]
    elif case == "child":
        c["lineage"] = [{"stage_id": FOREIGN, "claim_id": FOREIGN}]
    elif case == "coverage":
        c.update(kind="commentary", evidence_ids=[], contradicting_evidence_ids=[])
    elif case == "unsupported":
        c.update(kind="fact", status="unsupported")
    rejected(r, data, reason)


@pytest.mark.parametrize("stage", ["structural", "root"])
@pytest.mark.parametrize(
    "case,reason",
    [
        ("missing", "missing_child_coverage"),
        ("duplicate", "duplicate_child_link"),
        ("unavailable", "unavailable_reduction"),
    ],
)
def test_reducer_reasons(contracts, stage, case, reason):
    r = contracts[stage]
    data = json.loads(r.raw)
    if case == "missing":
        for c in data["claims"]:
            c.update(kind="commentary", lineage=[])
    elif case == "duplicate":
        data["claims"][0]["lineage"] *= 2
    else:
        data.update(outcome="unavailable", claims=[], limitations=["Unavailable"])
    rejected(r, data, reason)


@pytest.mark.parametrize(
    "raw,reason",
    [
        (b"{", "malformed_json"),
        (b'{"private":1,"private":2}', "duplicate_json_key"),
        (b" " * 10001, "raw_response_limit"),
    ],
)
def test_codec_reasons(raw, reason):
    with pytest.raises(DigestionError) as caught:
        decode(raw, StageResult, 10000)
    assert caught.value.validation_reason.value == reason


@pytest.mark.parametrize("reason", ["length", "max_tokens"])
@pytest.mark.parametrize("content", [None, "", '{"partial":', "absent"])
def test_truncation_retains_usage_and_null_byte_unknown(reason, content):
    value = payload(
        choices=[{"message": {"content": content}, "finish_reason": reason}]
    )
    if content == "absent":
        del value["choices"][0]["message"]["content"]
    p = client(Response(value))
    with pytest.raises(InferenceOutputLimitError) as caught:
        p.execute(request())
    error = caught.value
    assert error.usage == InferenceUsage(21, 7, 28)
    assert error.diagnostics.response_bytes == (
        None if content in (None, "absent") else len(content)
    )
    assert error.diagnostics.failure_cause == "provider_completion_truncated"
    assert error.provider_metadata.evidence()["finish_reason"] == reason
    assert len(p.http_client.calls) == 1


@pytest.mark.parametrize(
    "case",
    [
        "complete",
        "reasoning",
        "missing_usage",
        "partial_usage",
        "invalid_usage",
        "null_stop",
        "empty_stop",
        "refusal",
        "missing_finish",
        "malformed_finish",
        "missing_choices",
        "model",
    ],
)
def test_provider_result_metadata(case):
    value = payload()
    choice = value["choices"][0]
    if case == "reasoning":
        value["usage"]["completion_tokens_details"] = {
            "reasoning_tokens": 5,
            "private": SECRET,
        }
    elif case == "missing_usage":
        value.pop("usage")
    elif case == "partial_usage":
        value["usage"] = {"completion_tokens": 0}
    elif case == "invalid_usage":
        value["usage"]["total_tokens"] = True
    elif case == "null_stop":
        choice["message"]["content"] = None
    elif case == "empty_stop":
        choice["message"]["content"] = ""
    elif case == "refusal":
        choice["message"]["refusal"] = SECRET
    elif case == "missing_finish":
        choice.pop("finish_reason")
    elif case == "malformed_finish":
        choice["finish_reason"] = [SECRET]
    elif case == "missing_choices":
        value["choices"] = []
    elif case == "model":
        value["model"] = SECRET
    p = client(Response(value))
    req = request(structured_output="json_schema", schema_profile="azure-strict/1")
    # Use the actual schema; the generic provider fixture's open object is not convertible.
    from documents.digestion.managed import generation_schema

    req = replace(req, schema=generation_schema())
    fail = case in (
        "invalid_usage",
        "null_stop",
        "refusal",
        "missing_finish",
        "malformed_finish",
        "missing_choices",
        "model",
    )
    if fail:
        with pytest.raises(InferenceResponseError) as caught:
            p.execute(req)
        info = caught.value.provider_metadata.evidence()
        assert caught.value.usage == (
            None if case == "invalid_usage" else InferenceUsage(21, 7, 28)
        )
    else:
        result = p.execute(req)
        info = result.metadata.evidence()
    assert info["prompt_tokens"] == (
        None if case in ("invalid_usage", "missing_usage", "partial_usage") else 21
    )
    assert info["reasoning_tokens"] == (5 if case == "reasoning" else None)
    assert info["completion_token_limit"] == 500 and info["response_byte_limit"] == 1000
    assert SECRET not in json.dumps(info)
    assert len(p.http_client.calls) == 1


def test_forged_provider_metadata_serialization():
    info = ProviderResultMetadata(
        finish_reason=SECRET,
        prompt_tokens=True,
        total_tokens=SECRET,
        reasoning_tokens=-1,
        completion_tokens=0,
    ).evidence()
    assert info["finish_reason"] == "other" and info["completion_tokens"] == 0
    assert (
        info["prompt_tokens"]
        is info["total_tokens"]
        is info["reasoning_tokens"]
        is None
    )
    assert SECRET not in json.dumps(info)


@pytest.mark.parametrize(
    "case,expected",
    [
        ("valid", "schema_conformant"),
        ("uuid", "schema_conformant"),
        ("extra", "schema_rejected"),
        ("duplicate", "invalid_json"),
        ("limit", "response_limit"),
        ("json", "invalid_json"),
    ],
)
def test_offline_schema_observation_never_establishes_domain_acceptance(
    contracts,
    case,
    expected,
):
    data = json.loads(contracts["chunk"].raw)
    if case == "uuid":
        data["stage_id"] = SECRET
    elif case == "extra":
        data[SECRET] = SECRET
    raw = json.dumps(data).encode()
    if case == "duplicate":
        raw = b'{"private":1,"private":2}'
    elif case == "limit":
        raw = b" " * 10001
    elif case == "json":
        raw = b"{"
    assert observe_schema(raw) is SchemaObservation(expected)
    if case == "uuid":
        with pytest.raises(DigestionError):
            decode(raw, StageResult, 10000)


@pytest.mark.parametrize(
    "case,reason",
    [
        ("encoding", "canonical_encoding_failed"),
        ("revalidation", "canonical_revalidation_failed"),
    ],
)
def test_canonical_failures_are_distinct(contracts, monkeypatch, case, reason):
    from documents.digestion import codec

    original = StageResult.model_validate

    def fail(*args, **kwargs):
        raise ValueError(SECRET)

    if case == "encoding":
        monkeypatch.setattr(codec, "canonical", fail)
    else:
        monkeypatch.setattr(StageResult, "model_validate", fail)
    with pytest.raises(DigestionError) as caught:
        codec.encode(contracts["chunk"].result)
    assert caught.value.validation_reason.value == reason
    assert caught.value.validation_diagnostic.value == "canonical_serialization"
    assert SECRET not in str(caught.value)
    assert original is not None


@pytest.mark.parametrize(
    "case,reason",
    [
        ("canonical", "canonical_response_limit"),
        ("claims", "claim_limit"),
        ("annotations", "annotation_limit"),
        ("text", "text_limit"),
    ],
)
def test_response_limits_keep_separate_reasons(contracts, case, reason):
    r = contracts["chunk"]
    data = json.loads(r.raw)
    profile = r.request.profile
    if case == "canonical":
        data["claims"][0]["text"] = "\u0800" * 1600
    elif case == "claims":
        profile = profile.model_copy(update={"max_claims": 1})
        data["claims"] *= 2
    elif case == "annotations":
        data["open_questions"] = ["Q"] * (profile.max_annotations + 1)
    else:
        data["claims"][0]["text"] = "x" * (profile.max_claim_characters + 1)
    with pytest.raises(DigestionError) as caught:
        validate_result(
            json.dumps(data, ensure_ascii=False).encode(),
            r.request.model_copy(update={"profile": profile}),
            r.index,
        )
    assert caught.value.validation_reason.value == reason
    assert caught.value.category == "synthesis_limit_exceeded"


# Reuse existing synthetic authorization fixtures, never private operator state.
from tests.approval_helpers import approval_signer  # noqa: F401
from tests.integration.test_single_call_harness import offline, rig  # noqa: F401
from tests.unit.test_security_entra import entra  # noqa: F401
from tests.unit.test_security_identity import identity  # noqa: F401


@pytest.mark.parametrize(
    "case", ["accepted", "rejected", "truncated_cleanup", "unknown", "invalid"]
)
def test_sanitized_governed_audit_retains_provider_metadata(rig, monkeypatch, case):
    from governance.ledger import GovernanceError, GovernanceLedger

    cfg, run, http, ledger, authority, principal, *_ = rig

    def transform(value):
        value["usage"]["completion_tokens_details"] = {
            "reasoning_tokens": 5,
            "private": SECRET,
        }
        choice = value["choices"][0]
        if case == "rejected":
            data = json.loads(choice["message"]["content"])
            data["claims"][0]["claim_id"] = SECRET
            choice["message"]["content"] = json.dumps(data)
        elif case == "truncated_cleanup":
            choice.update(finish_reason="length", message={"content": None})
        elif case == "unknown":
            value.pop("usage")
        elif case == "invalid":
            value["usage"]["prompt_tokens"] = SECRET
        return value

    http.transform = transform
    if case == "truncated_cleanup":

        def fail(*args):
            raise GovernanceError()

        monkeypatch.setattr(GovernanceLedger, "settle", fail)
    result = run()
    info = result["provider_metadata"]
    assert (
        info["completion_token_limit"] == 3000 and info["response_byte_limit"] == 10000
    )
    assert info["prompt_tokens"] == (None if case in ("unknown", "invalid") else 30)
    assert info["reasoning_tokens"] == (None if case in ("unknown", "invalid") else 5)
    if case == "rejected":
        assert result["validation_reason"] == "invalid_uuid"
        assert result["pydantic_diagnostic"]["path"] == ["claims", 0, "claim_id"]
        assert result["failure"] == "serialization_error"
        assert ledger.usage(principal, authority)[0]["state"] == "SETTLED"
    elif case == "truncated_cleanup":
        assert (
            result["failure"] == "inference_output_limit"
            and result["accounting_failed"]
        )
        assert (
            info["finish_reason"] == "length"
            and info["raw_response_byte_count"] is None
        )
        assert ledger.usage(principal, authority)[0]["state"] == "STARTED"
    elif case in ("unknown", "invalid"):
        assert ledger.usage(principal, authority)[0]["state"] == "UNKNOWN"
        assert result["state"] == "FAILED"
    else:
        assert result["state"] == "SUCCEEDED"
    serialized = (cfg.audit_directory / "outcome.json").read_text()
    assert SECRET not in serialized
    assert "UNTRUSTED_DOCUMENT_DATA" not in serialized
    assert '"content"' not in serialized and '"text"' not in serialized
    assert len(http.sent) == result["calls"] == 1


# These checksums were captured before any production edit. They supplement,
# and never replace, the repository's source-based approval fingerprints.
FROZEN_REQUESTS = {
    "chunk": {
        "generation": "cb41fb6fbca5f160b97ac16152955e5a5029dc83c400702821b4302232d71659",
        "payload": "b2a6745cbe2607f0bc44ff6c9b1b679c223ee66994401942e84b48461c0c5533",
        "request": "12f09a58b2798efd124334559d8c1c692d0614422ec748475b6a8b6bf69a7f3b",
    },
    "structural": {
        "generation": "d4ce5cbbce3b55d7b8ddbb83b5b118b01435ad974cb2e42c68a36d77f5ac846f",
        "payload": "409106cd46830c65f2305356a86c583e5f3403721c9bbfa43605765e6a8b7c72",
        "request": "ad3eac20bd5fd5c3871b8c43540720d3f5eb98fe0317fc9f84f0f9533513dddf",
    },
    "root": {
        "generation": "997a01bf07d9ebf16fb4ed886e7d7ada608ed1b7aa0f4b1d8d969a9d4ec53541",
        "payload": "bce41543e4b435f299a7123b748cb22c320581b37b5f32b34ced107989839b78",
        "request": "419a71edd3a494700bdd8c9c1426793fc75650fd9d61eac90ca5cfae8ac1ddf2",
    },
}


@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
@pytest.mark.parametrize("component", ["request", "generation", "payload"])
def test_complete_pre_edit_generation_contract(historical_contracts, stage, component):
    record = historical_contracts[stage]
    value = {
        "request": record.request.model_dump(mode="json"),
        "generation": asdict(record.generation),
        "payload": record.payload,
    }[component]
    actual = sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()
    assert actual == FROZEN_REQUESTS[stage][component]


def test_generation_schema_and_renderer_source_remain_frozen():
    from documents.digestion.managed import generation_schema
    from documents.jobs.models import fingerprint
    from llm.azure_schema import provider_schema

    assert (
        fingerprint(provider_schema(generation_schema()))
        == "4248844859e21a2afed6a898b2797a58d51b062b8085a4bd6328da62dbca3df2"
    )
    root = Path(__file__).resolve().parents[2]
    assert (
        sha256((root / "tests/fixtures/digestion_contracts/managed_prompt3.py.txt").read_bytes()).hexdigest()
        == MANAGED_SOURCE_SHA
    )
    fixture = root / "tests/fixtures/digestion_contracts/models.py.txt"
    approved = source_sections(fixture.read_text(encoding="utf-8"), DOMAIN_NAMES)
    actual = source_sections(
        (root / "documents/digestion/models.py").read_text(encoding="utf-8"),
        DOMAIN_NAMES,
    )
    for name in DOMAIN_NAMES:
        assert_source_contract(actual[name], approved[name])


MANAGED_SOURCE_SHA = "5b272d4a7591692eeeb328da09bc39b35d402bebd1d8ada3b891f6b1d6e8928c"


@pytest.fixture(scope="module")
def historical_contracts(tmp_path_factory):
    """Replay the hash-pinned v3 test source; never offer v3 in production."""
    import sys
    from types import ModuleType, SimpleNamespace

    from documents.digestion import managed
    from documents.storage import LocalObjectStore

    fixture = Path(__file__).resolve().parents[1] / "fixtures/digestion_contracts/managed_prompt3.py.txt"
    source = fixture.read_bytes()
    assert sha256(source).hexdigest() == MANAGED_SOURCE_SHA
    module = ModuleType("tests._historical_managed_prompt3")
    with pytest.MonkeyPatch.context() as patch:
        patch.setitem(sys.modules, module.__name__, module)
        # Only the hash-pinned repository fixture is executable here.
        exec(compile(source, str(fixture), "exec"), module.__dict__)  # noqa: S102
        for name in ("StageProfile", "ManagedSettings", "ManagedSynthesisInference"):
            patch.setattr(managed, name, getattr(module, name))
        root = tmp_path_factory.mktemp("historical-v3")
        records = contracts.__wrapped__(SimpleNamespace(mktemp=lambda name: root))
        for record in records.values():
            record.store = LocalObjectStore(root / "objects")
        return records


@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
def test_active_v4_generation_contract(contracts, stage):
    root = Path(__file__).resolve().parents[2]
    expected = json.loads((root / "tests/fixtures/digestion_contracts/managed_prompt4.json").read_text())
    record = contracts[stage]
    for component, value in {
        "request": record.request.model_dump(mode="json"),
        "generation": asdict(record.generation),
        "payload": record.payload,
    }.items():
        actual = sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()
        assert actual == expected["requests"][stage][component]
        assert actual != FROZEN_REQUESTS[stage][component]
    assert sha256((root / "documents/digestion/managed.py").read_bytes()).hexdigest() == expected["managed_source_sha256"]


@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
def test_v4_changes_only_subject_guidance(historical_contracts, contracts, stage):
    fixture = Path(__file__).resolve().parents[1] / "fixtures/digestion_contracts/managed_prompt4_subject.txt"
    clarification = " ".join(fixture.read_text().split()) + " "
    active = contracts[stage].generation
    historical = historical_contracts[stage].generation
    assert active.system.count(clarification) == 1
    assert active.system.split("\nCONTROL\n")[0].replace(clarification, "") == historical.system.split("\nCONTROL\n")[0]
    assert active.schema == historical.schema
    for name in ("output_tokens", "response_bytes", "max_response_envelope_bytes", "capability", "total_seconds"):
        assert getattr(active, name) == getattr(historical, name)


def test_historical_results_readable_but_requests_cannot_resume(historical_contracts, contracts):
    from documents.digestion.codec import encode, read
    from documents.digestion.managed import (
        ManagedSettings,
        ManagedSynthesisInference,
        StageProfile,
    )
    from documents.digestion.models import Checkpoint
    from llm.openai_compatible import OpenAICompatibleProvider

    historical = historical_contracts["chunk"]
    # The stored result and its original evidence remain valid under stage-result/1.
    assert decode(encode(historical.result), StageResult, 10000) == historical.result
    assert validate_result(historical.raw, historical.request, historical.index) == historical.result
    child = historical_contracts["structural"].request.children[0]
    # Read an actual synthetic v3 checkpoint through the immutable object store.
    checkpoint = read(historical.store, child.artifact.scope, child.artifact, Checkpoint,
        historical.request.profile.max_artifact_bytes)
    assert checkpoint.result == historical.result
    assert decode(encode(checkpoint), Checkpoint, historical.request.profile.max_artifact_bytes) == checkpoint
    provider = OpenAICompatibleProvider(base_url="https://offline.invalid/openai/v1",
        model_map={"summarization": "offline-model"}, http_client=object())
    chosen = ManagedSettings(capability=historical.generation.capability,
        generation_profile="managed-generation/2", max_response_envelope_bytes=26192,
        profiles=tuple(StageProfile(stage=s, input_tokens=24800, output_tokens=3000)
            for s in ("chunk", "intermediate", "structural", "root")))
    adapter = ManagedSynthesisInference(provider, chosen, None)
    assert adapter.config != historical.request.profile.inference_config
    assert historical.request.stage_id != contracts["chunk"].request.stage_id
    with pytest.raises(DigestionError, match="incompatible_checkpoint"):
        adapter.render(historical.request)


@pytest.mark.parametrize("stage", ["chunk", "intermediate", "structural", "root"])
def test_active_subject_rules_have_valid_witnesses_for_all_profiles(contracts, stage):
    from documents.digestion.managed import (
        ManagedSettings,
        ManagedSynthesisInference,
        StageProfile,
    )
    from llm.openai_compatible import OpenAICompatibleProvider
    from tests.performance.foundry_recalibration import candidate_capability

    r = contracts["structural" if stage == "intermediate" else stage]
    settings = ManagedSettings(
        capability=candidate_capability(strict_digestion=True),
        generation_profile="managed-generation/2",
        max_response_envelope_bytes=26192,
        profiles=tuple(
            StageProfile(stage=s, input_tokens=24800, output_tokens=3000)
            for s in ("chunk", "intermediate", "structural", "root")
        ),
    )
    provider = OpenAICompatibleProvider(
        base_url="https://offline.invalid/openai/v1",
        model_map={"summarization": "offline-model"},
        http_client=object(),
    )
    adapter = ManagedSynthesisInference(provider, settings, None, stage=stage)
    generation, _ = adapter.render(r.request)
    control = json.loads(generation.system.split("\nCONTROL\n")[1])
    assert control["profile"]["stage"] == stage
    assert control["profile"]["template_version"] == r.request.profile.prompt_profile == "managed-prompt/4"
    fixture = Path(__file__).resolve().parents[1] / "fixtures/digestion_contracts/managed_prompt4_subject.txt"
    assert " ".join(fixture.read_text().split()) in " ".join(generation.system.split())
    for instruction in (
        "Include every schema field, including default values, empty arrays and nulls.",
        "Cite ONLY allowed evidence IDs; never invent references.",
        "Use the supplied claim_ids_in_order consecutively and originating_stage=stage_id.",
        "Represent unknown or unsupported conclusions explicitly using kind/status.",
        "For analysis, reference EVERY allowed evidence ID across the claims.",
        "For reduction, include EVERY required_child_link across claim lineage;",
    ):
        assert instruction in generation.system
    data = json.loads(r.raw)
    for c in data["claims"]:
        if c["kind"] != "fact":
            c["subject"] = None
        assert c["subject"] is None or len(c["subject"]) <= 128
    assert validate_result(json.dumps(data).encode(), r.request, r.index)
    if stage == "chunk":
        data.update(
            outcome="unavailable",
            claims=[],
            limitations=["Synthetic analysis unavailable."],
        )
        assert (
            validate_result(json.dumps(data).encode(), r.request, r.index).outcome
            == "unavailable"
        )
    else:
        data.update(
            outcome="unavailable",
            claims=[],
            limitations=["Synthetic analysis unavailable."],
        )
        rejected(r, data, "unavailable_reduction")


def test_supplemental_classifier_failure_cannot_mask_domain_error(
    contracts, monkeypatch
):
    from documents.digestion import codec

    def fail(*args):
        raise ValueError(SECRET)

    monkeypatch.setattr(codec, "classify_pydantic", fail)
    data = json.loads(contracts["chunk"].raw)
    data["stage_id"] = SECRET
    error = rejected(contracts["chunk"], data, "other_pydantic_validation")
    assert error.category == "inference_contract_error"
    assert SECRET not in json.dumps(error.pydantic_diagnostic.evidence())


def test_application_acceptance_predicates_and_order_are_unchanged():
    root = Path(__file__).resolve().parents[2]
    actual = source_sections(
        (root / "documents/digestion/validation.py").read_text(encoding="utf-8"),
        ("validate_result",),
    )["validate_result"]
    approved = (
        root / "tests/fixtures/digestion_contracts/validation.py.txt"
    ).read_text(encoding="utf-8")
    assert_source_contract(actual, approved, allow_diagnostics=True)


def test_qualification_text_limit_is_not_misreported_as_source_failure(contracts):
    r = contracts["chunk"]
    data = json.loads(r.raw)
    data["claims"][0]["qualifications"] = [
        {
            "text": "x" * (r.request.profile.max_claim_characters + 1),
            "evidence_ids": data["claims"][0]["evidence_ids"],
        }
    ]
    error = rejected(r, data, "text_limit")
    assert error.validation_diagnostic.value == "evidence_validation"
    assert error.category == "evidence_validation_failed"


def test_byte_diagnostic_cannot_mask_refusal():
    value = payload(
        choices=[
            {
                "message": {"content": "\ud800", "refusal": SECRET},
                "finish_reason": "stop",
            }
        ]
    )
    p = client(Response(value))
    from documents.digestion.managed import generation_schema

    req = replace(
        request(structured_output="json_schema", schema_profile="azure-strict/1"),
        schema=generation_schema(),
    )
    with pytest.raises(InferenceResponseError) as caught:
        p.execute(req)
    assert caught.value.provider_metadata.raw_response_byte_count is None
    assert caught.value.usage == InferenceUsage(21, 7, 28)
