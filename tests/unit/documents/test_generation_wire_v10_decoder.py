"""Deterministic v10 authority, atomic pairs, exact types and canonical identities."""

from copy import deepcopy
from dataclasses import replace
from uuid import UUID

import pytest
from jsonschema import Draft202012Validator

from documents.digestion.codec import encode
from documents.digestion.models import DigestionError
from documents.digestion.validation import validate_result
from documents.digestion.wire import construct, references, schema
from documents.jobs.models import canonical
from documents.models import stable_id
from llm.azure_schema import provider_schema
from tests.generation_wire_fixtures import cases, proposal


@pytest.fixture(scope="module")
def records(tmp_path_factory):
    return cases(tmp_path_factory.mktemp("wire-unit"))[1]


def decode(data, request, table=None):
    return construct(canonical(data).encode(), request, table or references(request))


@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
def test_exact_canonical_round_trip_and_original_offsets(records, stage):
    request, expected, index, _, _ = records[stage]
    table = references(request)
    data = proposal(request, expected)
    before = deepcopy(data)
    raw = decode(data, request)
    assert validate_result(raw, request, index) == expected
    assert data == before
    assert raw == encode(expected)
    for i, claim in enumerate(expected.claims):
        assert claim.claim_id == stable_id(str(request.stage_id), str(i))
        assert claim.originating_stage == request.stage_id
    for piece in request.source_data:
        assert index.resolve(piece.evidence) == piece.text
        assert piece.evidence_id() in table.evidence
    assert expected.claims[2].qualifications
    assert expected.claims[0].stance == "affirmed"
    assert expected.claims[1].stance == "denied"
    assert Draft202012Validator(provider_schema(schema(table))).is_valid(data)
    assert "stage_id" not in data and "claim_id" not in canonical(data)


@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
@pytest.mark.parametrize(
    "field", ["evidence_refs", "contradicting_evidence_refs", "qualification"]
)
@pytest.mark.parametrize(
    "bad",
    [
        "E99",
        "E0",
        "e1",
        " E1",
        "E01",
        "C1",
        str(UUID(int=8)),
        None,
        1,
        True,
        {},
        ["E1"],
    ],
)
def test_invalid_source_selections_fail_without_repair(records, stage, field, bad):
    request, expected, _, _, _ = records[stage]
    data = proposal(request, expected)
    if field == "qualification":
        data["claims"][0]["qualifications"] = [
            {"text": "Condition.", "evidence_refs": [bad]}
        ]
    else:
        data["claims"][0][field] = [bad]
    original = deepcopy(data)
    with pytest.raises(DigestionError):
        decode(data, request)
    assert data == original


@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
@pytest.mark.parametrize(
    "field", ["evidence_refs", "contradicting_evidence_refs", "qualification"]
)
def test_duplicate_source_selections_fail(records, stage, field):
    request, expected, _, _, _ = records[stage]
    data = proposal(request, expected)
    if field == "qualification":
        data["claims"][0]["qualifications"] = [
            {"text": "Condition.", "evidence_refs": ["E1", "E1"]}
        ]
    else:
        data["claims"][0][field] = ["E1", "E1"]
    with pytest.raises(DigestionError):
        decode(data, request)


@pytest.mark.parametrize("stage", ["structural", "root"])
@pytest.mark.parametrize(
    "bad", ["C99", "C0", "c1", " C1", "C01", "E1", "C1/C2", None, 1, True, {}, ["C1"]]
)
def test_atomic_child_keys_cannot_mix_or_substitute_pairs(records, stage, bad):
    request, expected, _, _, _ = records[stage]
    data = proposal(request, expected)
    data["claims"][0]["child_refs"] = [bad]
    with pytest.raises(DigestionError):
        decode(data, request)


@pytest.mark.parametrize("stage", ["structural", "root"])
def test_pair_order_membership_duplicates_coverage_and_grandchildren(records, stage):
    request, expected, index, _, _ = records[stage]
    table = references(request)
    assert table.children == tuple(
        (c.result.stage_id, k.claim_id)
        for c in request.children
        for k in c.result.claims
    )
    assert len(table.children) == 8
    data = proposal(request, expected)
    data["claims"][0]["child_refs"] = ["C1", "C2"]
    assert validate_result(decode(data, request), request, index)
    data["claims"][0]["child_refs"] = ["C1", "C1"]
    with pytest.raises(DigestionError):
        decode(data, request)
    data = proposal(request, expected)
    data["claims"][0]["child_refs"] = []
    with pytest.raises(DigestionError, match="coverage_failed"):
        validate_result(decode(data, request), request, index)
    data["claims"][0]["child_refs"] = [str(records["chunk"][1].claims[0].claim_id)]
    with pytest.raises(DigestionError):
        decode(data, request)


@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
@pytest.mark.parametrize(
    "change", ["stage", "path", "config", "table", "sources", "generation"]
)
def test_exact_request_and_table_binding(records, stage, change):
    request, expected, _, _, _ = records[stage]
    table = references(request)
    raw = canonical(proposal(request, expected)).encode()
    if change == "table":
        table = replace(table, evidence=tuple(reversed(table.evidence)))
    elif change == "stage":
        request = request.model_copy(update={"stage_id": UUID(int=88)})
    elif change == "path":
        request = request.model_copy(update={"structural_path": ("different",)})
    elif change == "config":
        request = request.model_copy(
            update={
                "profile": request.profile.model_copy(
                    update={"inference_config": "1" * 64}
                )
            }
        )
    elif change == "generation":
        request = request.model_copy(
            update={
                "profile": request.profile.model_copy(
                    update={"prompt_profile": "managed-prompt/9"}
                )
            }
        )
    elif request.stage == "analysis":
        request = request.model_copy(
            update={"source_data": tuple(reversed(request.source_data))}
        )
    else:
        child = request.children[0]
        request = request.model_copy(
            update={
                "children": (
                    child.model_copy(
                        update={
                            "result": child.result.model_copy(
                                update={"claims": tuple(reversed(child.result.claims))}
                            )
                        }
                    ),
                )
            }
        )
    with pytest.raises(DigestionError):
        construct(raw, request, table)


@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
@pytest.mark.parametrize(
    "fault",
    [
        "version",
        "binding",
        "extra",
        "missing",
        "claims_type",
        "claim_type",
        "text_type",
        "empty_text",
        "kind_type",
        "status",
        "stance",
        "subject_type",
        "subject_pattern",
        "too_many_claims",
        "too_many_annotations",
        "too_many_qualifications",
        "qualification_extra",
        "questions_type",
        "question_type",
        "refs_type",
        "canonical_id",
        "canonical_stage",
    ],
)
def test_strict_decoder_structure_types_and_bounds(records, stage, fault):
    request, result, _, _, _ = records[stage]
    data = proposal(request, result)
    c = data["claims"][0]
    if fault == "version":
        data["schema_version"] = "stage-proposal/2"
    elif fault == "binding":
        data["request_binding"] = "0" * 64
    elif fault == "extra":
        data["unknown"] = 1
    elif fault == "missing":
        del data["outcome"]
    elif fault == "claims_type":
        data["claims"] = {}
    elif fault == "claim_type":
        data["claims"][0] = []
    elif fault == "text_type":
        c["text"] = 12
    elif fault == "empty_text":
        c["text"] = ""
    elif fault == "kind_type":
        c["kind"] = True
    elif fault == "status":
        c["status"] = "invented"
    elif fault == "stance":
        c["stance"] = []
    elif fault == "subject_type":
        c["subject"] = 1
    elif fault == "subject_pattern":
        c["subject"] = "invalid subject"
    elif fault == "too_many_claims":
        data["claims"].append(deepcopy(c))
    elif fault == "too_many_annotations":
        data["limitations"] = ["x"] * (request.profile.max_annotations + 1)
    elif fault == "too_many_qualifications":
        c["qualifications"] = [{"text": "x", "evidence_refs": ["E1"]}] * (
            request.profile.max_annotations + 1
        )
    elif fault == "qualification_extra":
        c["qualifications"] = [{"text": "x", "evidence_refs": ["E1"], "extra": 1}]
    elif fault == "questions_type":
        data["open_questions"] = "x"
    elif fault == "question_type":
        data["open_questions"] = [False]
    elif fault == "refs_type":
        c["evidence_refs"] = "E1"
    elif fault == "canonical_id":
        c["claim_id"] = str(UUID(int=1))
    elif fault == "canonical_stage":
        data["stage_id"] = str(request.stage_id)
    with pytest.raises(DigestionError):
        decode(data, request)


@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
@pytest.mark.parametrize(
    "raw",
    [
        b"{",
        b"[]",
        b"null",
        b"{}",
        b"NaN",
        b"\xff",
        b'{"outcome":1,"outcome":2}',
        b'{"claims":[{"text":"a","text":"b"}]}',
    ],
)
def test_raw_json_fail_closed(records, stage, raw):
    request = records[stage][0]
    with pytest.raises(DigestionError):
        construct(raw, request, references(request))


@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
def test_raw_limit_empty_outcome_missing_coverage_and_order(records, stage):
    request, result, index, _, _ = records[stage]
    data = proposal(request, result)
    raw = canonical(data).encode()
    with pytest.raises(DigestionError, match="synthesis_limit_exceeded"):
        construct(
            raw + b" " * request.profile.response_byte_limit,
            request,
            references(request),
        )
    data["claims"].reverse()
    reordered = validate_result(decode(data, request), request, index)
    assert [c.text for c in reordered.claims] == [
        c.text for c in reversed(result.claims)
    ]
    assert reordered.claims[0].kind == result.claims[-1].kind
    assert reordered.claims[0].claim_id == stable_id(str(request.stage_id), "0")
    data.update(
        claims=[], outcome="unavailable", limitations=["Explicit unavailable analysis."]
    )
    canonical_result = decode(data, request)
    if stage == "chunk":
        assert not validate_result(canonical_result, request, index).claims
        data["outcome"] = "analyzed"
        with pytest.raises(DigestionError):
            validate_result(decode(data, request), request, index)
    else:
        with pytest.raises(DigestionError):
            validate_result(canonical_result, request, index)
    data = proposal(request, result)
    for c in data["claims"]:
        c.update(
            kind="commentary",
            subject=None,
            evidence_refs=[],
            contradicting_evidence_refs=[],
            qualifications=[],
            child_refs=[],
        )
    with pytest.raises(DigestionError, match="coverage_failed"):
        validate_result(decode(data, request), request, index)


def test_deterministic_sorted_source_table_and_multilevel_lineage(records):
    request, result, index, _, _ = records["root"]
    table = references(request)
    assert table.evidence == tuple(sorted(table.evidence, key=str))
    restored = type(request).model_validate_json(request.model_dump_json())
    assert references(restored) == table
    assert decode(proposal(request, result), restored) == encode(result)
    assert all(pair[0] == records["structural"][0].stage_id for pair in table.children)
    assert all(pair[0] != records["chunk"][0].stage_id for pair in table.children)
    assert validate_result(decode(proposal(request, result), request), request, index)


@pytest.mark.parametrize("fault", ["valid", "E1", "C1"])
def test_empty_authority_never_authorizes_a_syntactically_valid_alias(records, fault):
    from documents.digestion.models import StageRequest

    request = StageRequest(
        stage_id=UUID(int=123),
        stage="reduction",
        profile=records["root"][0].profile,
        structural_path=(),
    )
    table = references(request)
    assert not table.evidence and not table.children
    data = {
        "schema_version": "stage-proposal/1",
        "request_binding": table.digest,
        "outcome": "analyzed",
        "claims": [
            {
                "text": "Explicit limitation.",
                "kind": "commentary",
                "status": "unknown",
                "subject": None,
                "stance": "unknown",
                "evidence_refs": [],
                "contradicting_evidence_refs": [],
                "qualifications": [],
                "child_refs": [],
            }
        ],
        "open_questions": [],
        "limitations": ["No substantive source conclusions."],
    }
    if fault != "valid":
        data["claims"][0]["evidence_refs" if fault == "E1" else "child_refs"] = [fault]
        with pytest.raises(DigestionError):
            decode(data, request)
    else:
        result = validate_result(decode(data, request), request, records["root"][2])
        assert not result.claims[0].evidence_ids and not result.claims[0].lineage


@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
@pytest.mark.parametrize("delta", [-1, 0])
def test_canonical_expansion_has_its_own_exact_byte_boundary(records, stage, delta):
    request, result, _, _, _ = records[stage]
    size = len(encode(result))
    request = request.model_copy(
        update={
            "profile": request.profile.model_copy(
                update={"max_result_characters": size + delta}
            )
        }
    )
    data = proposal(request, result)
    assert len(canonical(data).encode()) < size - 1
    if delta < 0:
        with pytest.raises(DigestionError, match="synthesis_limit_exceeded"):
            decode(data, request)
    else:
        assert decode(data, request) == encode(result)


def test_active_strict_schema_configuration_rejects_unknown_constructs(monkeypatch):
    from documents.digestion import managed
    from llm.inference import InferenceConfigurationError
    from tests.generation_wire_fixtures import inference

    bad = managed.wire_schema()
    bad["unknown"] = True
    monkeypatch.setattr(managed, "wire_schema", lambda: bad)
    with pytest.raises(InferenceConfigurationError):
        inference()
