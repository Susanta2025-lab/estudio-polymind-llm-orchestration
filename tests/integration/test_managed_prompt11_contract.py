"""V11 exact requests/transport/inventory, independent of frozen v10 evidence."""

import json
from dataclasses import asdict
from functools import partial
from hashlib import sha256
from pathlib import Path
from types import SimpleNamespace

import pytest

from documents.digestion import managed
from tests.historical_managed_v10 import generation_digest
from tests.integration.test_final_offline_azure_compatibility import capture_contracts
from tests.performance.foundry_l1 import LaunchConfiguration, generation_contract_digest


@pytest.fixture(scope="module")
def v11_contracts(tmp_path_factory):
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(
            managed,
            "StageProfile",
            partial(managed.StageProfile, template_version="managed-prompt/11"),
        )
        return capture_contracts(tmp_path_factory)


@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
def test_explicit_v11_request_transport_and_inventory(v11_contracts, stage):
    root = Path(__file__).resolve().parents[2]
    expected = json.loads(
        (root / "tests/fixtures/digestion_contracts/managed_prompt11.json").read_text()
    )
    assert expected["prompt_version"] == "managed-prompt/11"
    assert expected["inventory_version"] == "generation-inventory/2"
    hashes = {
        name: sha256((root / name).read_bytes()).hexdigest()
        for name in expected["sources"]
    }
    assert hashes == expected["sources"]
    assert expected["generation_contract_sha256"] == generation_contract_digest()
    assert (
        sha256(
            json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        == generation_contract_digest()
    )
    assert (
        generation_digest()
        == "e5fb249cc9b166b5e438f1534eb855fa5ab7531e08aa09314c110a1905327ebd"
    )
    assert generation_digest() != generation_contract_digest()
    record = v11_contracts[stage]
    assert record.request.profile.prompt_profile == "managed-prompt/11"
    for name, value in {
        "request": record.request.model_dump(mode="json"),
        "generation": asdict(record.generation),
        "payload": record.payload,
    }.items():
        assert (
            sha256(
                json.dumps(
                    value, sort_keys=True, separators=(",", ":"), default=str
                ).encode()
            ).hexdigest()
            == expected["requests"][stage][name]
        )


def test_executed_v10_inventory_cannot_authorize_current_code():
    stale = SimpleNamespace(
        contract=None,
        policy=None,
        governance_policy=SimpleNamespace(evaluation=None),
        generation_contract_sha256=generation_digest(),
    )
    with pytest.raises(ValueError, match="Reviewed generation contract"):
        LaunchConfiguration.bounded(stale)
