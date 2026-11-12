"""Explicit protected-launch configuration and zero-network v11 rehearsal."""

import json
from types import SimpleNamespace

import pytest

from documents.digestion import managed
from tests.approval_helpers import (
    approval_signer,  # noqa: F401 - Pytest fixture dependency.
)
from tests.integration.test_foundry_l1_launcher import (  # noqa: F401 - Pytest fixtures.
    composition,
    deny_network,
)
from tests.performance import foundry_preflight
from tests.performance.foundry_l1 import LaunchConfiguration, configuration_digest
from tests.unit.test_security_identity import (
    identity,  # noqa: F401 - Pytest fixture dependency.
)


def test_v11_configuration_is_bound_and_default_shape_is_preserved(composition):  # noqa: F811 - Pytest fixture.
    default, _, http, _, _ = composition
    assert default.managed_prompt_version == "managed-prompt/10"
    assert "managed_prompt_version" not in default.model_dump()
    explicit = LaunchConfiguration.model_validate(
        {**default.model_dump(), "managed_prompt_version": "managed-prompt/11"}
    )
    assert explicit.model_dump()["managed_prompt_version"] == "managed-prompt/11"
    assert configuration_digest(explicit) != configuration_digest(default)
    assert (
        LaunchConfiguration.model_validate_json(explicit.model_dump_json()) == explicit
    )
    with pytest.raises(ValueError):
        LaunchConfiguration.model_validate(
            {**default.model_dump(), "managed_prompt_version": "managed-prompt/999"}
        )
    assert not http.sent


def test_explicit_v11_rehearsal_binds_all_profiles_and_new_digest(
    tmp_path, monkeypatch
):
    observed = []
    original = managed.ManagedSettings

    def settings(**kwargs):
        value = original(**kwargs)
        observed.append(value)
        return value

    monkeypatch.setattr(managed, "ManagedSettings", settings)
    result = foundry_preflight.execute(
        tmp_path, "L1", template_version="managed-prompt/11"
    )
    assert {p.stage for p in observed[0].profiles} == {
        "chunk",
        "intermediate",
        "structural",
        "root",
    }
    assert {p.template_version for p in observed[0].profiles} == {"managed-prompt/11"}
    assert (
        result["chunks"],
        result["reducers"],
        result["calls"],
        result["billable_calls"],
    ) == (1, 2, 4, 0)
    assert result["job_state"] == "COMPLETED"
    assert result["questions"]["status"] == "COMPLETE"
    assert result["publication"]["citations"]
    assert len(json.loads((tmp_path / "provider-calls.json").read_text())) == 4


def test_runtime_template_override_rejected_before_authority_access(tmp_path):
    with pytest.raises(ValueError, match="LaunchConfiguration"):
        foundry_preflight.execute(
            tmp_path,
            "L1",
            runtime=SimpleNamespace(),
            template_version="managed-prompt/11",
        )
    assert not list(tmp_path.iterdir())
