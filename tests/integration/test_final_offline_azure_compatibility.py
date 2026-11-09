"""Exact production contracts, synthetic witnesses and structural/semantic gaps.

No provider factory, approval, credential, network or content repair is used.
Run with the independent pre-collection network guard recorded in the report.
"""

import json
from copy import deepcopy
from dataclasses import replace
from types import SimpleNamespace
from uuid import UUID

import pytest
from jsonschema import Draft202012Validator

from documents.digestion import workflow
from documents.digestion.codec import decode, encode
from documents.digestion.managed import ManagedDigestionHandler, generation_schema
from documents.digestion.models import DigestionError, StageResult
from documents.digestion.validation import validate_result
from documents.models import stable_id
from llm.azure_schema import provider_schema
from llm.inference import InferenceConfigurationError
from llm.openai_compatible import OpenAICompatibleProvider
from tests.performance import foundry_preflight

STAGES = ("chunk", "structural", "root")
FOREIGN = str(UUID(int=17000001))


@pytest.fixture(scope="module")
def contracts(tmp_path_factory):
    return capture_contracts(tmp_path_factory)


@pytest.fixture(scope="module")
def legacy_v4_contracts(tmp_path_factory):
    """Replay the pinned v4 renderer without G1, preserving its original binding."""
    return capture_contracts(tmp_path_factory, historical_settings=True, historical_version=4)


@pytest.fixture(scope="module")
def legacy_v5_contracts(tmp_path_factory):
    """Replay the unchanged hash-pinned v5 renderer with its original binding."""
    return capture_contracts(tmp_path_factory, historical_version=5)


@pytest.fixture(scope="module")
def legacy_v5_unbounded_contracts(tmp_path_factory):
    return capture_contracts(tmp_path_factory, historical_settings=True, historical_version=5)


@pytest.fixture(scope="module")
def legacy_v6_contracts(tmp_path_factory):
    return capture_contracts(tmp_path_factory, historical_version=6)


@pytest.fixture(scope="module")
def legacy_v6_unbounded_contracts(tmp_path_factory):
    return capture_contracts(tmp_path_factory, historical_settings=True, historical_version=6)


@pytest.fixture(scope="module")
def v4_g1_contracts(tmp_path_factory):
    """The prior generation contract, retaining its original G1 admission."""
    return capture_contracts(tmp_path_factory, historical_version=4)


@pytest.fixture(scope="module")
def unbounded_contracts(tmp_path_factory):
    return capture_contracts(tmp_path_factory, historical_settings=True)


def capture_contracts(tmp_path_factory, *, historical_settings=False, historical_version=None):
    """Observe real planning/rendering/HTTP/validation without changing decisions."""
    from documents.digestion import managed
    from documents.storage import LocalObjectStore

    if historical_version is not None:
        import sys
        from hashlib import sha256
        from pathlib import Path
        from types import ModuleType

        version = historical_version
        fixture = Path(__file__).resolve().parents[1] / f"fixtures/digestion_contracts/managed_prompt{version}.py.txt"
        source = fixture.read_bytes()
        expected = json.loads(fixture.with_suffix("").with_suffix(".json").read_text())
        expected_source = (expected["managed_source_sha256"] if version in (5, 6) else
                           "36e0fba04c1dd952dc7617759fc36f2106d407578ecba194204a215b1ef88a36")
        assert sha256(source).hexdigest() == expected_source
        module = ModuleType(f"tests._historical_managed_prompt{version}")
        with pytest.MonkeyPatch.context() as patch:
            patch.setitem(sys.modules, module.__name__, module)
            # Execute only the fixed, hash-pinned synthetic historical fixture.
            exec(compile(source, str(fixture), "exec"), module.__dict__)  # noqa: S102
            for name in ("StageProfile", "ManagedSettings", "ManagedSynthesisInference"):
                patch.setattr(managed, name, getattr(module, name))
            return capture_contracts(tmp_path_factory, historical_settings=historical_settings)

    records = []
    original_settings = managed.ManagedSettings
    original_analyze = ManagedDigestionHandler.analyze
    original_execute = OpenAICompatibleProvider.execute
    original_validate = workflow.validate_result
    original_post = foundry_preflight.OfflineHTTP.post
    active = {}

    def historical_configuration(**kwargs):
        # The current L1 harness always selects G1. Historical replay must omit
        # that one new input BEFORE the original strict settings constructor.
        assert kwargs.pop("child_input_bytes") == 7000
        settings = original_settings(**kwargs)
        assert "child_input_bytes" not in settings.model_dump(mode="json")
        return settings

    def analyze(handler, request, *args):
        active["request"] = request
        return original_analyze(handler, request, *args)

    def execute(provider, generation):
        if "\nCONTROL\n" in generation.system:
            active["generation"] = generation
        return original_execute(provider, generation)

    def post(http, url, **kwargs):
        if "\nCONTROL\n" in kwargs["json"]["messages"][0]["content"]:
            active["url"], active["payload"] = url, deepcopy(kwargs["json"])
        return original_post(http, url, **kwargs)

    def validate(raw, request, index):
        result = original_validate(raw, request, index)
        if request.stage_id not in {r.request.stage_id for r in records}:
            assert request == active["request"]
            records.append(
                SimpleNamespace(
                    request=request,
                    index=index,
                    result=result,
                    raw=raw,
                    generation=active["generation"],
                    url=active["url"],
                    payload=active["payload"],
                )
            )
        return result

    with pytest.MonkeyPatch.context() as patch:
        if historical_settings:
            patch.setattr(managed, "ManagedSettings", historical_configuration)
        patch.setattr(ManagedDigestionHandler, "analyze", analyze)
        patch.setattr(OpenAICompatibleProvider, "execute", execute)
        patch.setattr(foundry_preflight.OfflineHTTP, "post", post)
        patch.setattr(workflow, "validate_result", validate)
        root = tmp_path_factory.mktemp("synthetic-compatibility")
        outcome = foundry_preflight.execute(root, "L1")
        classes = SimpleNamespace(**{name: getattr(managed, name) for name in (
            "StageProfile", "ManagedSettings", "ManagedSynthesisInference")})
        classes.ManagedSettings = original_settings
    assert outcome["job_state"] == "COMPLETED"
    assert outcome["digest_status"] == "COMPLETE"
    assert outcome["calls"] == 4
    assert all(r["state"] == "SETTLED" for r in outcome["governance_records"])
    assert len(records) == 3
    for record in records:
        record.store = LocalObjectStore(root / "objects")
        record.managed = classes
    return dict(zip(STAGES, records, strict=True))


def schema_nodes(node):
    if isinstance(node, dict):
        yield node
        for child in node.values():
            yield from schema_nodes(child)
    elif isinstance(node, list):
        for child in node:
            yield from schema_nodes(child)


def qualification_witness(raw, case):
    """Synthetic eight-claim/17-primary-reference analogue; no live content/IDs."""
    data = json.loads(raw)
    original = data["claims"][0]
    allowed = original["evidence_ids"]
    assert len(allowed) == len(set(allowed)) == 4
    data["claims"] = []
    for position, count in enumerate((1, 1, 1, 1, 4, 1, 4, 4)):
        claim = deepcopy(original)
        claim.update(
            claim_id=str(stable_id(data["stage_id"], str(position))),
            text="Synthetic source finding.",
            evidence_ids=allowed if count == 4 else [allowed[position % 4]],
            qualifications=[],
        )
        data["claims"].append(claim)
    references = allowed[:3]
    if case == "valid":
        references.append(allowed[3])
    elif case == "foreign":
        references.append(FOREIGN)
    elif case == "blended":
        blended = allowed[0].split("-")[0] + "-" + allowed[1].split("-", 1)[1]
        assert str(UUID(blended)) == blended and blended not in allowed
        references.append(blended)
    elif case == "duplicate":
        references.append(allowed[0])
    else:
        raise AssertionError(case)
    data["claims"][-1]["qualifications"] = [
        {"text": "Only under the supplied source conditions.", "evidence_ids": references}
    ]
    return data


@pytest.mark.parametrize("case", ("valid", "foreign", "blended", "duplicate"))
def test_multi_reference_qualification_membership(contracts, case):
    record = contracts["chunk"]
    data = qualification_witness(record.raw, case)
    Draft202012Validator(provider_schema(generation_schema())).validate(data)
    raw = encode(StageResult.model_validate(data))
    decoded = decode(raw, StageResult, record.request.profile.response_byte_limit)
    allowed = {p.evidence_id() for p in record.request.source_data}
    assert len(decoded.claims) == 8
    assert sum(len(c.evidence_ids) for c in decoded.claims) == 17
    assert all(set(c.evidence_ids) <= allowed for c in decoded.claims)
    qualification = decoded.claims[-1].qualifications[0]
    assert len(qualification.evidence_ids) == 4
    assert len(set(qualification.evidence_ids[:3])) == 3
    assert set(qualification.evidence_ids[:3]) <= allowed
    if case == "valid":
        assert len(set(qualification.evidence_ids)) == 4
        assert validate_result(raw, record.request, record.index) == decoded
    else:
        if case != "duplicate":
            assert qualification.evidence_ids[3] not in allowed
        with pytest.raises(DigestionError) as caught:
            validate_result(raw, record.request, record.index)
        assert caught.value.category == "evidence_validation_failed"
        assert caught.value.validation_diagnostic.value == "evidence_validation"
        assert caught.value.validation_reason.value == "invalid_qualification_source"
        # Removing only the late invalid entry establishes valid surrounding provenance.
        data["claims"][-1]["qualifications"][0]["evidence_ids"].pop()
        assert validate_result(encode(StageResult.model_validate(data)), record.request, record.index)


@pytest.mark.parametrize("stage", STAGES)
def test_exact_rendered_contract_and_unmodified_witness(contracts, stage):
    record = contracts[stage]
    request, generation, payload = record.request, record.generation, record.payload
    schema = provider_schema(generation_schema())
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(json.loads(record.raw))
    assert generation.schema == generation_schema()
    assert record.url == "https://offline.invalid/openai/v1/chat/completions"
    assert payload["response_format"] == {
        "type": "json_schema",
        "json_schema": {
            "name": "polymind_stage_result",
            "strict": True,
            "schema": schema,
        },
    }
    assert payload["stream"] is False and "text" not in payload
    assert payload["model"] == "offline-model"
    assert payload["max_completion_tokens"] == generation.output_tokens == 3000
    assert payload["reasoning_effort"] == "low" and "temperature" not in payload
    assert "tools" not in payload and "tool_choice" not in payload
    assert generation.role.value == "summarization"
    assert generation.response_bytes == 10000
    assert generation.max_response_envelope_bytes == 26192
    control = json.loads(generation.system.split("\nCONTROL\n")[1])
    assert control["profile"]["stage"] == stage
    assert control["profile"]["template_version"] == "managed-prompt/7"
    assert control["kind"] == request.stage
    assert control["stage_id"] == str(request.stage_id)
    assert control["schema"] == generation.schema
    assert control["max_result_bytes"] == control["max_response_bytes"] == 10000
    assert control["max_claim_characters"] == request.profile.max_claim_characters
    assert control["max_annotations"] == request.profile.max_annotations
    assert control["claim_ids_in_order"] == [
        str(stable_id(str(request.stage_id), str(i)))
        for i in range(request.profile.max_claims)
    ]
    expected_links = [
        {"stage_id": str(child.result.stage_id), "claim_id": str(claim.claim_id)}
        for child in request.children
        for claim in child.result.claims
    ]
    assert control["required_child_links"] == expected_links
    expected_evidence = {str(p.evidence_id()) for p in request.source_data} | {
        str(e)
        for child in request.children
        for claim in child.result.claims
        for e in (*claim.evidence_ids, *claim.contradicting_evidence_ids)
    }
    assert set(control["allowed_evidence_ids"]) == expected_evidence
    assert validate_result(record.raw, request, record.index) == record.result
    # Canonicalization changes representation only; every generated value survives.
    assert json.loads(encode(record.result)) == json.loads(record.raw)
    assert len(record.raw) <= 10000 and len(encode(record.result)) <= 10000


def test_schema_transformations_are_exhaustively_classified():
    original = generation_schema()
    before = deepcopy(original)
    converted = provider_schema(original)
    removed = set()

    def compare(source, target):
        for key, value in source.items():
            if key in {
                "title",
                "default",
                "format",
                "minLength",
                "maxLength",
                "pattern",
            }:
                removed.add(key)
                assert key not in target
            elif key == "const":
                assert target["enum"] == [value]
            elif key == "required":
                assert target[key] == list(source["properties"])
            elif key in {"properties", "$defs"}:
                assert value.keys() == target[key].keys()
                for name, child in value.items():
                    compare(child, target[key][name])
            elif key == "anyOf":
                assert len(value) == len(target[key])
                for child, other in zip(value, target[key], strict=True):
                    compare(child, other)
            elif key == "items":
                compare(value, target[key])
            else:
                assert target[key] == value
        assert set(target) == (set(source) - removed - {"const"}) | (
            {"enum"} if "const" in source else set()
        )

    compare(original, converted)
    assert original == before
    assert removed == {
        "title",
        "default",
        "format",
        "minLength",
        "maxLength",
        "pattern",
    }
    objects = [n for n in schema_nodes(converted) if n.get("type") == "object"]
    assert len(objects) == 4
    assert sum(len(n["properties"]) for n in objects) == 22
    for node in objects:
        assert node["additionalProperties"] is False
        assert node["required"] == list(node["properties"])
    assert converted["$defs"]["Claim"]["properties"]["subject"]["anyOf"] == [
        {"type": "string"},
        {"type": "null"},
    ]


CASES = (
    ("malformed_claim_uuid", "pydantic_validation"),
    ("malformed_evidence_uuid", "pydantic_validation"),
    ("empty_text", "pydantic_validation"),
    ("over_model_text", "pydantic_validation"),
    ("subject_pattern", "pydantic_validation"),
    ("subject_length", "pydantic_validation"),
    ("stage", "stage_binding"),
    ("kind", "stage_binding"),
    ("unavailable_with_claims", "stage_binding"),
    ("claim_id", "claim_identity"),
    ("origin", "claim_identity"),
    ("duplicate_claim", "claim_identity"),
    ("position", "claim_identity"),
    ("subject_on_commentary", "claim_contract"),
    ("foreign_evidence", "evidence_validation"),
    ("duplicate_evidence", "evidence_validation"),
    ("foreign_contradiction", "evidence_validation"),
    ("foreign_lineage", "evidence_validation"),
    ("empty_qualification_sources", "evidence_validation"),
    ("foreign_qualification_source", "evidence_validation"),
    ("coverage", "coverage_validation"),
    ("profile_text_bound", "response_limit"),
    ("annotation_bound", "response_limit"),
    ("unicode_expansion", "response_limit"),
)


def mutate(record, case):
    data = json.loads(record.raw)
    claim = data["claims"][0]
    if case == "malformed_claim_uuid":
        claim["claim_id"] = "SYNTHETIC_INVALID_UUID"
    elif case == "malformed_evidence_uuid":
        claim["evidence_ids"] = ["SYNTHETIC_INVALID_UUID"]
    elif case == "empty_text":
        claim["text"] = ""
    elif case == "over_model_text":
        claim["text"] = "x" * 4097
    elif case == "subject_pattern":
        claim.update(kind="fact", subject="invalid subject")
    elif case == "subject_length":
        claim.update(kind="fact", subject="x" * 129)
    elif case == "stage":
        data["stage_id"] = FOREIGN
    elif case == "kind":
        data["kind"] = "reduction" if record.request.stage == "analysis" else "analysis"
    elif case == "unavailable_with_claims":
        data["outcome"] = "unavailable"
    elif case == "claim_id":
        claim["claim_id"] = FOREIGN
    elif case == "origin":
        claim["originating_stage"] = FOREIGN
    elif case in {"duplicate_claim", "position"}:
        other = deepcopy(claim)
        if case == "position":
            other["claim_id"] = str(stable_id(str(record.request.stage_id), "1"))
        data["claims"].append(other)
        if case == "position":
            data["claims"].reverse()
    elif case == "subject_on_commentary":
        claim.update(kind="commentary", subject="synthetic")
    elif case == "foreign_evidence":
        claim["evidence_ids"] = [FOREIGN]
    elif case == "duplicate_evidence":
        control = json.loads(record.generation.system.split("\nCONTROL\n")[1])
        # Root source sets can be carried exclusively by lineage. In that case
        # any direct reference also fails membership, independently of duplication.
        evidence = control["allowed_evidence_ids"]
        claim["evidence_ids"] = [evidence[0] if evidence else FOREIGN] * 2
    elif case == "foreign_contradiction":
        claim["contradicting_evidence_ids"] = [FOREIGN]
    elif case == "foreign_lineage":
        claim["lineage"] = [{"stage_id": FOREIGN, "claim_id": FOREIGN}]
    elif case in {"empty_qualification_sources", "foreign_qualification_source"}:
        claim["qualifications"] = [
            {
                "text": "Synthetic qualification",
                "evidence_ids": [] if case.startswith("empty") else [FOREIGN],
            }
        ]
    elif case == "coverage":
        claim.update(kind="commentary", evidence_ids=[], lineage=[], qualifications=[])
    elif case == "profile_text_bound":
        claim["text"] = "x" * (record.request.profile.max_claim_characters + 1)
    elif case == "annotation_bound":
        data["limitations"] = ["Synthetic"] * (
            record.request.profile.max_annotations + 1
        )
    elif case == "unicode_expansion":
        claim["text"] = "\u0800" * 1600
    else:
        raise AssertionError(case)
    return data


@pytest.mark.parametrize("stage", STAGES)
@pytest.mark.parametrize("case,diagnostic", CASES)
def test_provider_valid_application_invalid(contracts, stage, case, diagnostic):
    record = contracts[stage]
    data = mutate(record, case)
    Draft202012Validator(
        record.payload["response_format"]["json_schema"]["schema"]
    ).validate(data)
    raw = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode()
    assert len(raw) <= record.request.profile.response_byte_limit
    with pytest.raises(DigestionError) as caught:
        validate_result(raw, record.request, record.index)
    assert caught.value.validation_diagnostic.value == diagnostic
    assert "SYNTHETIC_INVALID_UUID" not in str(caught.value)
    assert json.loads(raw) == data  # No output repair on failure.


@pytest.mark.parametrize("stage", STAGES)
def test_multiple_claim_witness_and_nullable_subject(contracts, stage):
    record = contracts[stage]
    data = json.loads(record.raw)
    other = deepcopy(data["claims"][0])
    other.update(
        claim_id=str(stable_id(str(record.request.stage_id), "1")),
        kind="commentary",
        subject=None,
        evidence_ids=[],
        lineage=[],
    )
    data["claims"].append(other)
    Draft202012Validator(provider_schema(generation_schema())).validate(data)
    raw = json.dumps(data).encode()
    assert validate_result(
        raw, record.request, record.index
    ) == StageResult.model_validate(data)


@pytest.mark.parametrize("stage", STAGES)
def test_zero_claim_outcome_rules(contracts, stage):
    record = contracts[stage]
    data = json.loads(record.raw)
    data.update(
        claims=[], outcome="unavailable", limitations=["Synthetic unavailable input"]
    )
    Draft202012Validator(provider_schema(generation_schema())).validate(data)
    if stage == "chunk":
        assert (
            "For analysis, reference EVERY allowed evidence ID across the claims."
            in record.generation.system
        )
        assert record.request.source_data and not data["claims"]
        assert (
            validate_result(
                json.dumps(data).encode(), record.request, record.index
            ).outcome
            == "unavailable"
        )
    else:
        with pytest.raises(DigestionError) as caught:
            validate_result(json.dumps(data).encode(), record.request, record.index)
        assert caught.value.validation_diagnostic.value == "stage_binding"


@pytest.mark.parametrize("stage", STAGES)
def test_render_rejects_wrong_profile_and_config_before_provider(contracts, stage):
    record = contracts[stage]
    from documents.digestion.managed import (
        ManagedSettings,
        ManagedSynthesisInference,
        StageProfile,
    )

    provider = OpenAICompatibleProvider(
        base_url="https://offline.invalid/openai/v1",
        model_map={"summarization": "offline-model"},
        http_client=object(),  # No usable transport.
    )
    settings = ManagedSettings(
        capability=record.generation.capability,
        child_input_bytes=7000,
        generation_profile="managed-generation/2",
        max_response_envelope_bytes=26192,
        profiles=tuple(
            StageProfile(stage=s, input_tokens=24800, output_tokens=3000)
            for s in ("chunk", "intermediate", "structural", "root")
        ),
    )
    adapter = ManagedSynthesisInference(provider, settings, None, stage=stage)
    assert adapter.config == record.request.profile.inference_config
    request = record.request.model_copy(
        update={
            "profile": record.request.profile.model_copy(
                update={"inference_config": "0" * 64}
            )
        }
    )
    with pytest.raises(DigestionError, match="incompatible_checkpoint"):
        adapter.render(request)
    wrong = "root" if stage == "chunk" else "chunk"
    with pytest.raises(InferenceConfigurationError, match="Stage profile mismatch"):
        adapter.bind(None, wrong).render(record.request)
    provider.model_map["summarization"] = "changed-model"
    with pytest.raises(DigestionError, match="incompatible_checkpoint"):
        adapter.render(record.request)


@pytest.mark.parametrize("stage", STAGES)
def test_omitted_defaults_and_duplicate_keys_are_distinct(contracts, stage):
    record = contracts[stage]
    data = record.result.model_dump(mode="json", exclude_defaults=True)
    assert not Draft202012Validator(provider_schema(generation_schema())).is_valid(data)
    assert (
        validate_result(json.dumps(data).encode(), record.request, record.index)
        == record.result
    )
    raw = record.raw.rstrip()
    duplicate = raw[:-1] + b',"schema_version":"stage-result/1"}'
    with pytest.raises(DigestionError) as caught:
        validate_result(duplicate, record.request, record.index)
    assert caught.value.validation_diagnostic.value == "duplicate_json_key"


@pytest.mark.parametrize("stage", STAGES)
def test_output_token_reservation_mismatch_rejected(contracts, stage):
    record = contracts[stage]
    # Provider validation enforces the ceiling independently of rendered prose.
    from llm.bounded_http import validate_request

    with pytest.raises(InferenceConfigurationError):
        validate_request(replace(record.generation, output_tokens=3001))


def bounded_witness(record, size):
    """Author fixture before execution, under the actual 256-character cap."""
    data = json.loads(record.raw)
    original = data["claims"][0]
    data["claims"] = []
    for position in range(record.request.profile.max_claims):
        claim = deepcopy(original)
        claim.update(
            claim_id=str(stable_id(str(record.request.stage_id), str(position))),
            text="x",
        )
        data["claims"].append(claim)
    # Sixteen bounded annotations plus eight bounded claim texts can fill the
    # byte budget without changing any runtime profile or evidence rule.
    data["open_questions"] = ["x"] * record.request.profile.max_annotations
    data["limitations"] = ["x"] * record.request.profile.max_annotations
    remaining = size - len(encode(StageResult.model_validate(data)))

    def padding():
        nonlocal remaining
        text = ""
        for _ in range(record.request.profile.max_claim_characters - 1):
            if remaining == 0:
                break
            # Each U+0800 occupies six canonical bytes and three raw UTF-8 bytes.
            character = "\u0800" if remaining >= 6 else "x"
            text += character
            remaining -= 6 if character == "\u0800" else 1
        return text

    for claim in data["claims"]:
        claim["text"] += padding()
    for key in ("open_questions", "limitations"):
        for position in range(len(data[key])):
            data[key][position] += padding()
    assert remaining == 0
    raw = encode(StageResult.model_validate(data))
    assert len(raw) == size
    return raw


@pytest.mark.parametrize("stage", STAGES)
@pytest.mark.parametrize("size", (10000, 10001))
def test_canonical_boundary_under_unchanged_l1_profile(legacy_v4_contracts, stage, size):
    # This historical independent-output-limit contract predates child admission.
    # Current G1 rejection of the same witness is checked separately below.
    record = legacy_v4_contracts[stage]
    assert record.request.profile.managed_input_budget is None
    raw = bounded_witness(record, size)
    Draft202012Validator(provider_schema(generation_schema())).validate(json.loads(raw))
    if size == 10000:
        assert encode(validate_result(raw, record.request, record.index)) == raw
    else:
        # Isolate canonical overflow with compact UTF-8, without changing values
        # or any configured profile limit.
        data = json.loads(raw)
        utf8 = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode()
        assert (
            len(utf8) < 10000 and len(encode(StageResult.model_validate(data))) == 10001
        )
        with pytest.raises(DigestionError) as caught:
            validate_result(utf8, record.request, record.index)
        assert caught.value.validation_diagnostic.value == "response_limit"


@pytest.mark.parametrize("stage", STAGES)
def test_current_l1_canonical_10k_witness_exceeds_child_budget(contracts, stage):
    from documents.digestion.sizing import CHILD_WRAPPER_BYTES, result_contribution

    record = contracts[stage]
    raw = bounded_witness(record, 10000)
    result = StageResult.model_validate_json(raw)
    assert len(raw) == record.request.profile.response_byte_limit == 10000
    assert len(encode(result)) == record.request.profile.max_result_characters == 10000
    assert record.request.profile.managed_input_budget.child_bytes == 7000
    assert result_contribution(result) + CHILD_WRAPPER_BYTES > 7000
    with pytest.raises(DigestionError, match="^synthesis_limit_exceeded$") as caught:
        validate_result(raw, record.request, record.index)
    assert caught.value.validation_diagnostic.value == "response_limit"
    assert encode(result) == raw  # Rejection does not truncate or repair evidence.


@pytest.mark.parametrize("stage", STAGES)
def test_current_l1_canonical_limit_precedes_child_admission(contracts, stage):
    record = contracts[stage]
    canonical = bounded_witness(record, 10001)
    raw = json.dumps(json.loads(canonical), ensure_ascii=False,
                     separators=(",", ":")).encode()
    assert len(raw) < record.request.profile.response_byte_limit == 10000
    assert len(canonical) > record.request.profile.max_result_characters == 10000
    with pytest.raises(DigestionError, match="^synthesis_limit_exceeded$") as caught:
        validate_result(raw, record.request, record.index)
    assert caught.value.validation_reason.value == "canonical_response_limit"
    assert encode(StageResult.model_validate_json(raw)) == canonical


@pytest.mark.parametrize("stage", STAGES)
@pytest.mark.parametrize("size", (10000, 10001))
def test_raw_boundary_under_unchanged_l1_profile(contracts, stage, size):
    record = contracts[stage]
    raw = record.raw + b" " * (size - len(record.raw))
    Draft202012Validator(provider_schema(generation_schema())).validate(json.loads(raw))
    if size == 10000:
        assert validate_result(raw, record.request, record.index) == record.result
    else:
        with pytest.raises(DigestionError) as caught:
            validate_result(raw, record.request, record.index)
        assert caught.value.validation_diagnostic.value == "response_limit"


def test_qualification_copy_is_not_equivalent_to_lineage_inheritance(
    tmp_path,
    monkeypatch,
):
    original_response = foundry_preflight.OfflineHTTP.response
    original_validate = workflow.validate_result
    observed = {}

    def response(http, sent, result, stage):
        if stage in ("chunk", "structural"):
            control = json.loads(sent["messages"][0]["content"].split("\nCONTROL\n")[1])
            data = json.loads(result)
            data["claims"][0]["qualifications"] = [
                {
                    "text": "Synthetic original qualification",
                    "evidence_ids": [control["allowed_evidence_ids"][0]],
                }
            ]
            # Author the synthetic provider output before transport/validation;
            # the real workflow then persists its exact immutable child artifact.
            result = json.dumps(data)
        elif stage == "root":
            observed["control"] = json.loads(
                sent["messages"][0]["content"].split("\nCONTROL\n")[1]
            )
        return original_response(http, sent, result, stage)

    def validate(raw, request, index):
        result = original_validate(raw, request, index)
        if request.children and request.children[0].result.kind == "reduction":
            observed.update(raw=raw, request=request, index=index, result=result)
        return result

    monkeypatch.setattr(foundry_preflight.OfflineHTTP, "response", response)
    monkeypatch.setattr(workflow, "validate_result", validate)
    outcome = foundry_preflight.execute(tmp_path, "L1")
    assert (
        outcome["job_state"] == "COMPLETED" and outcome["digest_status"] == "COMPLETE"
    )
    request, index = observed["request"], observed["index"]
    qualification = request.children[0].result.claims[0].qualifications[0]
    evidence = str(qualification.evidence_ids[0])
    assert original_validate(observed["raw"], request, index) == observed["result"]
    copied = json.loads(observed["raw"])
    copied["claims"][0]["qualifications"] = [qualification.model_dump(mode="json")]
    Draft202012Validator(provider_schema(generation_schema())).validate(copied)
    with pytest.raises(DigestionError) as caught:
        original_validate(json.dumps(copied).encode(), request, index)
    assert caught.value.validation_diagnostic.value == "evidence_validation"
    assert evidence not in observed["control"]["allowed_evidence_ids"]


@pytest.mark.parametrize("stage", STAGES)
@pytest.mark.parametrize(
    "case", ("empty_analyzed", "unsupported_fact", "source_free_fact")
)
def test_additional_outcome_and_fact_requirements(contracts, stage, case):
    record = contracts[stage]
    data = json.loads(record.raw)
    if case == "empty_analyzed":
        data["claims"] = []
        expected = "stage_binding" if stage == "chunk" else "coverage_validation"
    else:
        claim = data["claims"][0]
        claim["kind"] = "fact"
        if case == "unsupported_fact":
            claim["status"] = "unsupported"
        else:
            claim.update(evidence_ids=[], lineage=[])
        expected = "evidence_validation"
    Draft202012Validator(provider_schema(generation_schema())).validate(data)
    with pytest.raises(DigestionError) as caught:
        validate_result(json.dumps(data).encode(), record.request, record.index)
    assert caught.value.validation_diagnostic.value == expected


@pytest.mark.parametrize("stage", ("structural", "root"))
def test_duplicate_real_child_link_is_rejected(contracts, stage):
    record = contracts[stage]
    data = json.loads(record.raw)
    data["claims"][0]["lineage"] *= 2
    Draft202012Validator(provider_schema(generation_schema())).validate(data)
    with pytest.raises(DigestionError) as caught:
        validate_result(json.dumps(data).encode(), record.request, record.index)
    assert caught.value.validation_diagnostic.value == "evidence_validation"


def test_actual_single_analysis_contract_with_deployment_alias(tmp_path):
    from documents.models import Scope
    from tests.performance.foundry_recalibration import DEPLOYMENT
    from tests.performance.foundry_single_call import prepare_analysis
    from tests.unit.test_structured_provider import HTTP, Response, payload

    # Render-only preparation uses synthetic source and scope, never a packet,
    # credential, live authority, approval or executable launcher.
    _, request, index, generation, _, _ = prepare_analysis(
        tmp_path, Scope(tenant=UUID(int=1), owner=UUID(int=2))
    )
    control = json.loads(generation.system.split("\nCONTROL\n")[1])
    data = StageResult.model_validate(
        {
            "stage_id": control["stage_id"],
            "kind": control["kind"],
            "claims": [
                {
                    "claim_id": control["claim_ids_in_order"][0],
                    "originating_stage": control["stage_id"],
                    "kind": "fact",
                    "text": "Synthetic source observation",
                    "evidence_ids": control["allowed_evidence_ids"],
                }
            ],
        }
    ).model_dump(mode="json")
    raw = json.dumps(data, separators=(",", ":"))
    http = HTTP(
        Response(
            payload(
                model="gpt-5.4-mini-2026-03-17",
                choices=[{"message": {"content": raw}, "finish_reason": "stop"}],
            )
        )
    )
    provider = OpenAICompatibleProvider(
        base_url="https://offline.invalid/openai/v1",
        model_map={"summarization": DEPLOYMENT},
        http_client=http,
    )
    returned = provider.execute(generation)
    sent = http.calls[0][1]["json"]
    assert len(http.calls) == 1 and sent["model"] == DEPLOYMENT
    assert sent["response_format"]["json_schema"]["strict"] is True
    Draft202012Validator(sent["response_format"]["json_schema"]["schema"]).validate(
        data
    )
    assert returned.text == raw
    accepted = validate_result(returned.text.encode(), request, index)
    assert accepted.model_dump(mode="json") == data
    assert returned.usage.total_tokens == 28
