# ruff: noqa: F811
"""Inventory/2 pins every v10 constructor dependency; inventory/1 stays readable."""

import json
from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from documents.digestion.managed import ManagedSettings
from documents.digestion.models import DigestionError
from documents.digestion.validation import validate_result
from tests.integration.test_final_offline_azure_compatibility import (
    capture_contracts,
)
from tests.integration.test_final_offline_azure_compatibility import (
    contracts as legacy_v9_contracts,  # noqa: F401
)
from tests.integration.test_final_offline_azure_compatibility import (
    legacy_v5_contracts as legacy_v5_contracts,  # noqa: PLC0414
)
from tests.integration.test_final_offline_azure_compatibility import (
    legacy_v6_contracts as legacy_v6_contracts,  # noqa: PLC0414
)
from tests.integration.test_final_offline_azure_compatibility import (
    legacy_v7_contracts as legacy_v7_contracts,  # noqa: PLC0414
)
from tests.integration.test_final_offline_azure_compatibility import (
    legacy_v8_contracts as legacy_v8_contracts,  # noqa: PLC0414
)
from tests.integration.test_managed_prompt7_contract import adapter
from tests.performance.foundry_l1 import LaunchConfiguration, generation_contract_digest


@pytest.fixture(scope="module")
def v10_contracts(tmp_path_factory):
    return capture_contracts(tmp_path_factory)


@pytest.mark.parametrize("version", [5, 6, 7, 8, 9])
@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
def test_v10_refuses_historical_execution_and_preserves_canonical_results(
    v10_contracts,
    legacy_v5_contracts,
    legacy_v6_contracts,
    legacy_v7_contracts,
    legacy_v8_contracts,
    legacy_v9_contracts,
    version,
    stage,
):
    old = {
        5: legacy_v5_contracts,
        6: legacy_v6_contracts,
        7: legacy_v7_contracts,
        8: legacy_v8_contracts,
        9: legacy_v9_contracts,
    }[version][stage]
    assert validate_result(old.raw, old.request, old.index) == old.result
    with pytest.raises(ValidationError):
        ManagedSettings.model_validate(
            adapter(old, stage).settings.model_dump(mode="json")
        )
    with pytest.raises(DigestionError, match="incompatible_checkpoint"):
        adapter(v10_contracts[stage], stage).render(old.request)
    fixture = (
        Path(__file__).resolve().parents[1]
        / f"fixtures/digestion_contracts/managed_prompt{version}.json"
    )
    expected = json.loads(fixture.read_text())
    stale = SimpleNamespace(
        contract=None,
        policy=None,
        governance_policy=SimpleNamespace(evaluation=None),
        generation_contract_sha256=expected.get(
            "generation_contract_sha256",
            {
                5: "de9492c536c1435464e8d9e406cbd1491ea358bc45f817df72eb2ea2a0f69a71",
                6: "f6e568d450ac084c5977e4fef68823fb457cceacd22b361f047310c5d3512f5b",
            }.get(version),
        ),
    )
    with pytest.raises(ValueError, match="Reviewed generation contract"):
        LaunchConfiguration.bounded(stale)


@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
def test_frozen_v10_request_schema_transport_and_complete_inventory(
    v10_contracts, stage
):
    root = Path(__file__).resolve().parents[2]
    expected = json.loads(
        (root / "tests/fixtures/digestion_contracts/managed_prompt10.json").read_text()
    )
    record = v10_contracts[stage]
    for key, value in {
        "request": record.request.model_dump(mode="json"),
        "generation": asdict(record.generation),
        "payload": record.payload,
    }.items():
        digest = sha256(
            json.dumps(
                value, sort_keys=True, separators=(",", ":"), default=str
            ).encode()
        ).hexdigest()
        assert digest == expected["requests"][stage][key]
    assert expected["generation_contract_sha256"] == generation_contract_digest()
    hashes = {
        name: sha256((root / name).read_bytes()).hexdigest()
        for name in expected["sources"]
    }
    assert hashes == expected["sources"]
    assert (
        sha256(
            json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        == generation_contract_digest()
    )
    assert {
        "documents/digestion/wire.py",
        "documents/digestion/receipts.py",
        "documents/digestion/codec.py",
        "documents/models.py",
        "documents/jobs/models.py",
        "documents/jobs/worker.py",
        "documents/jobs/sqlite.py",
        "documents/storage.py",
    }.issubset(hashes)
    assert record.request.profile.output_schema == "stage-result/1"
    assert record.request.profile.prompt_profile == "managed-prompt/10"
