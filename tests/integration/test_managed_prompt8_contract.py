"""Exact lineage-only prompt migration and fail-closed historical bindings."""

import json
from dataclasses import asdict
from hashlib import sha256
from pathlib import Path

import pytest
from pydantic import ValidationError

from documents.digestion.codec import read
from documents.digestion.managed import ManagedDigestionHandler, classify_managed
from documents.digestion.models import Checkpoint, DigestionError, Plan
from documents.digestion.validation import validate_result
from documents.digestion.workflow import admit
from documents.jobs.models import JobSettings
from documents.jobs.sqlite import SQLiteJobLedger
from documents.jobs.worker import LocalDispatcher, Worker, relay
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
from tests.integration.test_managed_prompt7_contract import IDENTITY_V7, adapter
from tests.historical_managed import generation_digest
from tests.performance.foundry_l1 import LaunchConfiguration, generation_contract_digest


@pytest.fixture(scope="module")
def contracts(legacy_v8_contracts):
    return legacy_v8_contracts


LINEAGE_V8 = (
    "For each claim's direct lineage, copy exact (stage_id, claim_id) pairs together from "
    "CONTROL.required_child_links without modification. Never pair an immediate child's "
    "stage_id with a grandchild's claim_id or substitute earlier-stage/ancestor claim IDs. "
    "Inherited lineage is reached through these direct links; preserve required child "
    "coverage, source provenance, qualifications and conflicts. "
)


@pytest.mark.parametrize("stage", ["chunk", "intermediate", "structural", "root"])
def test_v8_changes_only_lineage_guidance_and_template_binding(
    contracts, legacy_v7_contracts, stage
):
    selected = "structural" if stage == "intermediate" else stage
    old, new = legacy_v7_contracts[selected], contracts[selected]
    before = adapter(old, stage).render(old.request)[0]
    after = adapter(new, stage).render(new.request)[0]
    old_text, new_text = (g.system.split("\nCONTROL\n")[0] for g in (before, after))
    assert old_text.count(IDENTITY_V7) == new_text.count(IDENTITY_V7) == 1
    assert new_text.count(LINEAGE_V8) == 1
    assert old_text.replace(IDENTITY_V7, IDENTITY_V7 + LINEAGE_V8) == new_text
    for name in (
        "schema",
        "output_tokens",
        "response_bytes",
        "max_response_envelope_bytes",
        "capability",
        "total_seconds",
    ):
        assert getattr(before, name) == getattr(after, name)
    old_budget, new_budget = (
        r.request.profile.managed_input_budget for r in (old, new)
    )
    assert new_budget.base_bytes - old_budget.base_bytes == len(LINEAGE_V8) == 394
    assert new_budget.base_bytes == 10630
    assert old_budget.input_bytes == new_budget.input_bytes == 24800
    assert old_budget.child_bytes == new_budget.child_bytes == 7000
    assert new.request.profile.prompt_profile == "managed-prompt/8"
    root = Path(__file__).resolve().parents[2]
    frozen = (
        root / "tests/fixtures/digestion_contracts/managed_prompt7.py.txt"
    ).read_text()
    active = (
        root / "tests/fixtures/digestion_contracts/managed_prompt8.py.txt"
    ).read_text()
    # Freeze the complete source delta too, including all non-prompt code.
    addition = active[
        active.index("            \"For each claim's direct lineage") : active.index(
            "            'Represent unknown"
        )
    ]
    assert frozen.replace("managed-prompt/7", "managed-prompt/8") == active.replace(
        addition, ""
    )


@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
def test_frozen_v8_full_generation(contracts, stage):
    root = Path(__file__).resolve().parents[2]
    expected = json.loads(
        (root / "tests/fixtures/digestion_contracts/managed_prompt8.json").read_text()
    )
    record = contracts[stage]
    for key, value in {
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
            == expected["requests"][stage][key]
        )
    assert (
        sha256(
            (
                root / "tests/fixtures/digestion_contracts/managed_prompt8.py.txt"
            ).read_bytes()
        ).hexdigest()
        == expected["managed_source_sha256"]
    )
    original_read = Path.read_bytes
    managed_path = root / "documents/digestion/managed.py"
    frozen = (
        root / "tests/fixtures/digestion_contracts/managed_prompt8.py.txt"
    ).read_bytes()
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(
            Path,
            "read_bytes",
            lambda path: frozen if path == managed_path else original_read(path),
        )
        assert generation_digest(8) == expected["generation_contract_sha256"]
    assert generation_contract_digest() != expected["generation_contract_sha256"]


@pytest.mark.parametrize("version", [5, 6, 7])
@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
def test_old_settings_requests_and_launch_binding_cannot_execute_under_v8(
    contracts,
    legacy_v5_contracts,
    legacy_v6_contracts,
    legacy_v7_contracts,
    version,
    stage,
):
    old = {5: legacy_v5_contracts, 6: legacy_v6_contracts, 7: legacy_v7_contracts}[
        version
    ][stage]
    current = adapter(contracts[stage], stage)
    with pytest.raises(ValidationError):
        contracts[stage].managed.ManagedSettings.model_validate(
            adapter(old, stage).settings.model_dump(mode="json")
        )
    with pytest.raises(DigestionError, match="^incompatible_checkpoint$"):
        current.render(old.request)
    assert validate_result(old.raw, old.request, old.index) == old.result
    historical_digest = {
        5: "de9492c536c1435464e8d9e406cbd1491ea358bc45f817df72eb2ea2a0f69a71",
        6: "f6e568d450ac084c5977e4fef68823fb457cceacd22b361f047310c5d3512f5b",
        7: "8426ab5cfef3e4d1925c68a5f8558c5bafc487dd746f0f7ccda799c03be16c3a",
    }[version]
    from types import SimpleNamespace

    stale = SimpleNamespace(
        contract=None,
        policy=None,
        governance_policy=SimpleNamespace(evaluation=None),
        generation_contract_sha256=historical_digest,
    )
    with pytest.raises(ValueError, match="Reviewed generation contract"):
        LaunchConfiguration.bounded(stale)


@pytest.mark.parametrize("version", [5, 6, 7])
def test_old_checkpoint_plan_cannot_resume_with_v8(
    contracts,
    legacy_v5_contracts,
    legacy_v6_contracts,
    legacy_v7_contracts,
    tmp_path,
    version,
):
    old = {5: legacy_v5_contracts, 6: legacy_v6_contracts, 7: legacy_v7_contracts}[
        version
    ]["structural"]
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
