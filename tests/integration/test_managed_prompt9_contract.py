"""V9 source constraints, frozen complete payloads and historical fail-closed bindings."""

import json
from dataclasses import asdict
from hashlib import sha256
from pathlib import Path

import pytest
from pydantic import ValidationError

from documents.digestion.codec import read
from documents.digestion.managed import (
    ManagedDigestionHandler,
    ManagedSettings,
    classify_managed,
)
from documents.digestion.models import Checkpoint, DigestionError, Plan
from documents.digestion.validation import validate_result
from documents.digestion.workflow import admit
from documents.jobs.models import JobSettings
from documents.jobs.sqlite import SQLiteJobLedger
from documents.jobs.worker import LocalDispatcher, Worker, relay
from tests.integration.test_final_offline_azure_compatibility import (
    contracts as contracts,  # noqa: PLC0414
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
from tests.integration.test_final_offline_azure_compatibility import (
    schema_source_ids,
)
from tests.integration.test_managed_prompt7_contract import IDENTITY_V7, adapter
from tests.integration.test_managed_prompt8_contract import LINEAGE_V8
from tests.historical_managed import generation_digest
from tests.performance.foundry_l1 import LaunchConfiguration, generation_contract_digest


@pytest.mark.parametrize("stage", ["chunk", "intermediate", "structural", "root"])
def test_v9_preserves_identity_lineage_and_exact_source_authority(
    contracts, legacy_v8_contracts, stage
):
    selected = "structural" if stage == "intermediate" else stage
    old, new = legacy_v8_contracts[selected], contracts[selected]
    before = adapter(old, stage).render(old.request)[0]
    after = adapter(new, stage).render(new.request)[0]
    old_control = json.loads(before.system.split("\nCONTROL\n")[1])
    control = json.loads(after.system.split("\nCONTROL\n")[1])
    assert set(schema_source_ids(after.schema)) == set(
        old_control["allowed_evidence_ids"]
    )
    assert "allowed_evidence_ids" not in control and "schema" not in control
    for text in (IDENTITY_V7, LINEAGE_V8):
        assert before.system.count(text) == after.system.count(text) == 1
    for name in (
        "output_tokens",
        "response_bytes",
        "max_response_envelope_bytes",
        "capability",
        "total_seconds",
    ):
        assert getattr(before, name) == getattr(after, name)
    assert new.request.profile.managed_input_budget.base_bytes == 7379
    assert new.request.profile.managed_input_budget.input_bytes == 24800
    assert new.request.profile.managed_input_budget.child_bytes == 7000
    assert new.request.profile.prompt_profile == "managed-prompt/9"
    assert "copy complete UUIDs exactly" in after.system
    assert "never invent, reconstruct, splice, shorten or alter" in after.system
    assert "current authorized source-ID set" in after.system


@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
def test_frozen_v9_complete_generation_and_unchanged_other_contract_sources(
    contracts, stage
):
    root = Path(__file__).resolve().parents[2]
    expected = json.loads(
        (root / "tests/fixtures/digestion_contracts/managed_prompt9.json").read_text()
    )
    record = contracts[stage]
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
    assert (
        sha256((root / "tests/fixtures/digestion_contracts/managed_prompt9.py.txt").read_bytes()).hexdigest()
        == expected["managed_source_sha256"]
    )
    assert generation_digest(9) == expected["generation_contract_sha256"]
    # All fourteen other generation sources remain exactly v8. This proves G1/G2,
    # provider conversion, transport, settlement and composition were not altered.
    original_read = Path.read_bytes
    path = root / "documents/digestion/managed.py"
    frozen = (
        root / "tests/fixtures/digestion_contracts/managed_prompt8.py.txt"
    ).read_bytes()
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(
            Path, "read_bytes", lambda p: frozen if p == path else original_read(p)
        )
        assert (
            generation_digest(8)
            == "93ca9066491c197987f919c5d185417bf4f3d2787384acf2833011e32641c0df"
        )


@pytest.mark.parametrize("version", [5, 6, 7, 8])
@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
def test_historical_execution_binding_rejected_and_results_still_readable(
    contracts,
    legacy_v5_contracts,
    legacy_v6_contracts,
    legacy_v7_contracts,
    legacy_v8_contracts,
    version,
    stage,
):
    records = {
        5: legacy_v5_contracts,
        6: legacy_v6_contracts,
        7: legacy_v7_contracts,
        8: legacy_v8_contracts,
    }
    old = records[version][stage]
    with pytest.raises(ValidationError):
        ManagedSettings.model_validate(
            adapter(old, stage).settings.model_dump(mode="json")
        )
    with pytest.raises(DigestionError, match="^incompatible_checkpoint$"):
        adapter(contracts[stage], stage).render(old.request)
    assert validate_result(old.raw, old.request, old.index) == old.result
    digest = {
        5: "de9492c536c1435464e8d9e406cbd1491ea358bc45f817df72eb2ea2a0f69a71",
        6: "f6e568d450ac084c5977e4fef68823fb457cceacd22b361f047310c5d3512f5b",
        7: "8426ab5cfef3e4d1925c68a5f8558c5bafc487dd746f0f7ccda799c03be16c3a",
        8: "93ca9066491c197987f919c5d185417bf4f3d2787384acf2833011e32641c0df",
    }[version]
    from types import SimpleNamespace

    stale = SimpleNamespace(
        contract=None,
        policy=None,
        governance_policy=SimpleNamespace(evaluation=None),
        generation_contract_sha256=digest,
    )
    with pytest.raises(ValueError, match="Reviewed generation contract"):
        LaunchConfiguration.bounded(stale)


@pytest.mark.parametrize("version", [5, 6, 7, 8])
def test_old_checkpoint_plan_cannot_resume_with_v9(
    contracts,
    legacy_v5_contracts,
    legacy_v6_contracts,
    legacy_v7_contracts,
    legacy_v8_contracts,
    tmp_path,
    version,
):
    old = {
        5: legacy_v5_contracts,
        6: legacy_v6_contracts,
        7: legacy_v7_contracts,
        8: legacy_v8_contracts,
    }[version]["structural"]
    child = old.request.children[0]
    scope, store, limit = (
        child.artifact.scope,
        old.store,
        old.request.profile.max_artifact_bytes,
    )
    original = store.read(scope, child.artifact, max_bytes=limit)
    cp = read(store, scope, child.artifact, Checkpoint, limit)
    plan_ref = cp.parents[0]
    plan = read(store, scope, plan_ref, Plan, limit)
    ledger = SQLiteJobLedger(JobSettings(database_path=tmp_path / "jobs.sqlite"))
    job = admit(ledger, store, plan, plan_ref, request_key="historical-v8-denial")
    queue = LocalDispatcher()
    worker = Worker(
        ledger,
        queue,
        store,
        ManagedDigestionHandler(ledger, plan_ref, adapter(contracts["chunk"], "chunk")),
        owner="offline-v8-denial",
        classifier=classify_managed,
    )
    relay(ledger, queue)
    assert worker.once()
    assert ledger.get_job(scope, job.job_id).state == "FAILED"
    assert ledger.get_job(scope, job.job_id).terminal_category == "profile_mismatch"
    assert not any(s.manifest for s in ledger.steps(scope, job.job_id))
    assert store.read(scope, child.artifact, max_bytes=limit) == original
