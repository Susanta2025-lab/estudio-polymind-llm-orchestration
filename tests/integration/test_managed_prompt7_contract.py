"""Exact v7 guidance and generation-bound rejection of historical execution."""

import json
from dataclasses import asdict
from hashlib import sha256
from pathlib import Path

import pytest
from pydantic import ValidationError

from documents.digestion.codec import read
from documents.digestion.managed import ManagedDigestionHandler
from documents.digestion.models import Checkpoint, DigestionError, Plan
from documents.digestion.validation import validate_result
from documents.digestion.workflow import admit
from documents.jobs.models import JobSettings
from documents.jobs.sqlite import SQLiteJobLedger
from documents.jobs.worker import LocalDispatcher, Worker, relay
from llm.openai_compatible import OpenAICompatibleProvider
from tests.integration.test_final_offline_azure_compatibility import (
    contracts as contracts,  # noqa: PLC0414 - pytest fixture re-export.
)
from tests.integration.test_final_offline_azure_compatibility import (
    legacy_v5_contracts as legacy_v5_contracts,  # noqa: PLC0414
)
from tests.integration.test_final_offline_azure_compatibility import (
    legacy_v6_contracts as legacy_v6_contracts,  # noqa: PLC0414
)
from tests.performance.foundry_l1 import generation_contract_digest

IDENTITY_V6 = (
    "Use the supplied claim_ids_in_order consecutively and originating_stage=stage_id. "
)
IDENTITY_V7 = (
    "Use CONTROL.claim_ids_in_order consecutively for this response. Set the result stage_id "
    "and every claims[i].originating_stage to the current CONTROL.stage_id, including claims "
    "that restate child findings. Copy source-stage identities only into lineage using "
    "CONTROL.required_child_links; never copy a child's originating_stage into a new claim. "
)


def adapter(record, stage):
    module = record.managed
    return module.ManagedSynthesisInference(
        OpenAICompatibleProvider(
            base_url="https://offline.invalid/openai/v1",
            model_map={"summarization": "offline-model"},
            http_client=object(),
        ),
        module.ManagedSettings(
            capability=record.generation.capability,
            child_input_bytes=7000,
            generation_profile="managed-generation/2",
            max_response_envelope_bytes=26192,
            profiles=tuple(
                module.StageProfile(stage=s, input_tokens=24800, output_tokens=3000)
                for s in ("chunk", "intermediate", "structural", "root")
            ),
        ),
        None,
        stage=stage,
    )


@pytest.mark.parametrize("stage", ["chunk", "intermediate", "structural", "root"])
def test_v7_changes_exactly_identity_guidance_and_template_binding(
    contracts, legacy_v6_contracts, stage
):
    selected = "structural" if stage == "intermediate" else stage
    old, new = legacy_v6_contracts[selected], contracts[selected]
    old_generation, _ = adapter(old, stage).render(old.request)
    new_generation, _ = adapter(new, stage).render(new.request)
    before, after = (
        g.system.split("\nCONTROL\n")[0] for g in (old_generation, new_generation)
    )
    assert before.count(IDENTITY_V6) == after.count(IDENTITY_V7) == 1
    assert before.replace(IDENTITY_V6, IDENTITY_V7) == after
    assert old_generation.schema == new_generation.schema
    for name in (
        "output_tokens",
        "response_bytes",
        "max_response_envelope_bytes",
        "capability",
        "total_seconds",
    ):
        assert getattr(old_generation, name) == getattr(new_generation, name)
    assert new.request.profile.prompt_profile == "managed-prompt/7"
    assert old.request.profile.prompt_profile == "managed-prompt/6"
    old_budget, new_budget = (
        r.request.profile.managed_input_budget for r in (old, new)
    )
    assert old_budget.child_bytes == new_budget.child_bytes == 7000
    assert old_budget.input_bytes == new_budget.input_bytes == 24800
    assert (
        new_budget.base_bytes - old_budget.base_bytes
        == len(IDENTITY_V7) - len(IDENTITY_V6)
        == 263
    )
    assert new_budget.base_bytes == 10236
    assert new.request.profile.inference_config != old.request.profile.inference_config
    assert new.request.stage_id != old.request.stage_id


@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
def test_frozen_v7_requests_generation_and_http_payload(contracts, stage):
    root = Path(__file__).resolve().parents[2]
    expected = json.loads(
        (root / "tests/fixtures/digestion_contracts/managed_prompt7.json").read_text()
    )
    record = contracts[stage]
    for component, value in {
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
            == expected["requests"][stage][component]
        )
    assert (
        sha256((root / "documents/digestion/managed.py").read_bytes()).hexdigest()
        == expected["managed_source_sha256"]
    )
    assert generation_contract_digest() == expected["generation_contract_sha256"]


@pytest.mark.parametrize("version", [5, 6])
@pytest.mark.parametrize("stage", ["chunk", "structural", "root"])
def test_v5_v6_configuration_and_request_cannot_execute_under_v7(
    contracts, legacy_v5_contracts, legacy_v6_contracts, version, stage
):
    old = {5: legacy_v5_contracts, 6: legacy_v6_contracts}[version][stage]
    current = adapter(contracts[stage], stage)
    with pytest.raises(ValidationError):
        contracts[stage].managed.ManagedSettings.model_validate(
            adapter(old, stage).settings.model_dump(mode="json")
        )
    with pytest.raises(DigestionError, match="^incompatible_checkpoint$"):
        current.render(old.request)
    assert validate_result(old.raw, old.request, old.index) == old.result


@pytest.mark.parametrize("version", [5, 6])
def test_historical_checkpoint_plan_is_rejected_by_v7_durable_handler(
    contracts, legacy_v5_contracts, legacy_v6_contracts, tmp_path, version
):
    old = {5: legacy_v5_contracts, 6: legacy_v6_contracts}[version]["structural"]
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
    job = admit(ledger, store, plan, plan_ref, request_key="historical-plan-v7-denial")
    queue = LocalDispatcher()
    from documents.digestion.managed import classify_managed

    worker = Worker(
        ledger,
        queue,
        store,
        ManagedDigestionHandler(ledger, plan_ref, adapter(contracts["chunk"], "chunk")),
        owner="offline-v7-denial",
        classifier=classify_managed,
    )
    relay(ledger, queue)
    assert worker.once()
    assert ledger.get_job(scope, job.job_id).state == "FAILED"
    assert ledger.get_job(scope, job.job_id).terminal_category == "profile_mismatch"
    assert not any(s.manifest for s in ledger.steps(scope, job.job_id))
    assert store.read(scope, child.artifact, max_bytes=limit) == original
