"""Focused instruction, provider protocol and generation-isolation requirements."""

from dataclasses import replace
from functools import partial

import pytest
from pydantic import ValidationError

from documents.digestion import managed
from documents.digestion.models import DigestionError
from documents.digestion.wire import construct, references
from documents.jobs.models import canonical
from llm.bounded_http import validate_request
from llm.inference import InferenceConfigurationError
from tests.generation_wire_fixtures import cases, inference, proposal


@pytest.fixture
def versions(tmp_path, monkeypatch):
    old = cases(tmp_path / "v10")
    monkeypatch.setattr(
        managed,
        "StageProfile",
        partial(managed.StageProfile, template_version="managed-prompt/11"),
    )
    new = cases(tmp_path / "v11")
    return old, new


@pytest.mark.parametrize("stage", ["intermediate", "structural", "root"])
def test_substantive_content_and_provenance_are_separate(versions, stage):
    old, new = versions
    request = new[1]["structural" if stage == "intermediate" else stage][0]
    generation, estimate = new[0].bind(None, stage).render(request)
    prose = generation.system.split("\nCONTROL\n")[0]
    # Individual requirements, rather than a golden copy of the full prompt.
    for requirement in (
        "grounded domain findings",
        "provenance metadata",
        "claim.text",
        "evidence_refs",
        "child_refs",
        "request-local E/C aliases",
        "meaningful literal identifiers",
        "named entities",
        "measurements",
        "procedures",
        "requirements",
        "results",
        "relationships",
        "qualifications, uncertainty, conflicts and limitations",
        "Do not invent facts or relationships to satisfy coverage",
        "actual support",
        "never substitute grandchild references",
        "Inherited source support is distinct from direct source authority",
        "Do not claim direct inspection",
        "avoid repetition",
        "source subject",
    ):
        assert requirement in prose
    if stage == "structural":
        assert "section-level conclusions" in prose
        assert "do not merely enumerate child claims" in prose
    if stage == "root":
        assert "standalone whole-document synthesis" in prose
        assert "main subject or purpose where supported" in prose
        assert "unsupported cross-section conclusions" in prose
    assert generation.output_tokens == 3000
    assert generation.response_bytes == 10000
    assert generation.max_response_envelope_bytes == 26192
    assert generation.capability.context_tokens == 28000
    assert estimate + 3000 <= 28000
    validate_request(generation)
    with pytest.raises(InferenceConfigurationError):
        validate_request(replace(generation, output_tokens=3001))
    # No stronger schema/authority or larger limits are introduced by v11 prose.
    before = old[0].settings.model_dump(mode="json")
    after = new[0].settings.model_dump(mode="json")
    for profile in before["profiles"]:
        profile["template_version"] = "managed-prompt/11"
    assert before == after
    assert (
        old[2].profile.managed_input_budget.input_bytes
        == new[2].profile.managed_input_budget.input_bytes
        == 24800
    )
    assert (
        old[2].profile.managed_input_budget.child_bytes
        == new[2].profile.managed_input_budget.child_bytes
        == 7000
    )
    assert (
        new[2].profile.managed_input_budget.base_bytes
        > old[2].profile.managed_input_budget.base_bytes
    )


@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
def test_profiles_requests_and_raw_proposals_are_version_bound(versions, stage):
    old, new = versions
    assert old[0].config != new[0].config
    for current, other in ((old, new), (new, old)):
        req = other[1][stage][0]
        with pytest.raises(DigestionError, match="incompatible_checkpoint"):
            current[0].bind(None, stage).render(req)
    old_request, old_result = old[1][stage][:2]
    new_request = new[1][stage][0]
    raw = canonical(proposal(old_request, old_result)).encode()
    with pytest.raises(DigestionError, match="incompatible_checkpoint"):
        construct(raw, new_request, references(new_request))


def test_mixed_stage_versions_are_rejected():
    settings = inference().settings.model_dump(mode="json")
    settings["profiles"][0]["template_version"] = "managed-prompt/11"
    with pytest.raises(ValidationError, match="same managed prompt version"):
        managed.ManagedSettings.model_validate(settings)
    settings["profiles"][0]["template_version"] = "managed-prompt/999"
    with pytest.raises(ValidationError):
        managed.ManagedSettings.model_validate(settings)
