"""Pilot intake, parser containment, identity and actual-window scheduling."""

import subprocess
from uuid import uuid4

import pytest
from pydantic import ValidationError

from documents.config import ExtractionSettings
from documents.errors import DocumentError
from documents.pilot import PilotError, SourceApproval, SupervisedPilot
from documents.pilot.execution import PilotExecution
from documents.pilot.models import PilotPolicy
from documents.pilot.parser import IsolatedPdfRunner, ParserBounds
from documents.pilot.scheduling import forecast
from governance.execution import GovernedExecution
from governance.ledger import QuotaPolicy
from llm.admission import CallIdentity
from llm.inference import ModelRole
from llm.structured import GenerationRequest
from security.models import Action
from tests.performance.fixtures import pdf
from tests.pilot_helpers import begin, composition


@pytest.mark.parametrize(
    "change",
    [
        "hash",
        "type",
        "rights",
        "personal",
        "bytes",
        "characters",
        "pages",
        "scan",
        "graphics",
        "path",
        "owner",
        "model",
    ],
)
def test_pilot_intake_rejects_unapproved_hash_type_rights_and_limits_before_parse_or_provider(
    tmp_path, change
):
    raw = b"Native authored fixture.\n"
    is_pdf = change in {"pages", "scan", "graphics"}
    if change == "bytes":
        raw = b"x" * 1_000_001
    if change == "characters":
        raw = b"x" * 4001
    if change == "type":
        raw = b"%PDF-malformed"
    if is_pdf:
        raw, _ = pdf(
            5 if change == "pages" else 1,
            kinds=["image"]
            if change == "scan"
            else ["figure"]
            if change == "graphics"
            else None,
        )
    env = composition(tmp_path, raw=raw, pdf=is_pdf)
    p, op, approval, raw, http, _clock, args = env
    original = args["sources"][0]
    if change in {"rights", "personal", "path", "owner"}:
        changes = {
            "rights": {"rights_approved": False},
            "personal": {"classification": "personal"},
            "path": {"filename": "../outside.txt"},
            "owner": {"owner": original.owner.model_copy(update={"owner": uuid4()})},
        }[change]
        with pytest.raises((ValidationError, PilotError)):
            source = SourceApproval.model_validate({**original.model_dump(), **changes})
            SupervisedPilot(**{**args, "sources": (source,)})
    else:
        p.create_session(op, approval)
        if change == "hash":
            raw += b"tamper"
        if change == "model":
            p.provider.model_map["summarization"] = "substituted-model"
        with pytest.raises((PilotError, DocumentError)):
            p.select_source(op, approval.session_id, raw)
    assert not http.calls and not p.governance.usage(op, p.authority)


@pytest.mark.parametrize("scope_change", ["owner", "tenant"])
def test_pilot_forged_call_scope_is_denied_without_reservation_or_provider(
    tmp_path, scope_change
):
    env = composition(tmp_path)
    p, op, approval, _raw, http, _clock, args = env
    begin(env)
    snapshot = p.authority.snapshot(
        op, (args["sources"][0].document_id,), Action.DOCUMENT_DELETE
    )
    executor = PilotExecution(
        p,
        op,
        approval.session_id,
        GovernedExecution(p.provider, p.admission, p.governance, p.authority, snapshot),
    )
    request = GenerationRequest(
        "trusted",
        "{}",
        ModelRole.GENERAL,
        p.analysis_capability,
        100,
        1000,
        {},
        total_seconds=60,
    )
    scope = op.scope.model_copy(update={scope_change: uuid4()})
    identity = CallIdentity(
        scope.identity(),
        uuid4(),
        uuid4(),
        1,
        "interactive/1",
        p.provider.name,
        "general",
        "offline-model",
        request.capability.version,
    )
    with pytest.raises(PilotError):
        executor.execute(request, identity=identity)
    assert not http.calls and not p.governance.usage(op, p.authority)


@pytest.mark.parametrize("fault", ["wall", "cpu", "memory", "disk", "output"])
def test_pilot_parser_cpu_memory_wall_and_disk_exhaustion_is_contained(
    tmp_path, monkeypatch, fault
):
    real_run = subprocess.run
    observed = []

    def probe(command, **kwargs):
        command = [command[0], "-m", "tests.pilot_parser_probe", fault]
        result = real_run(command, **kwargs)
        observed.append(result.returncode)
        return result

    monkeypatch.setattr(subprocess, "run", probe)
    runner = IsolatedPdfRunner(
        ParserBounds(
            wall_seconds=0.05 if fault == "wall" else 4,
            cpu_seconds=1,
            memory_bytes=512 * 1024 * 1024,
            output_bytes=1024,
            disk_bytes=2048,
        )
    )
    with pytest.raises(DocumentError, match="extraction_failed"):
        runner.parse(
            b"%PDF-test-fault", ExtractionSettings(max_pages=4, max_characters=4000)
        )
    if fault != "wall":
        assert observed == [{"cpu": -9, "memory": 61, "disk": 62, "output": 63}[fault]]
    assert not list(tmp_path.iterdir())


def test_pilot_isolated_native_pdf_and_malformed_failure(tmp_path):
    raw, _ = pdf(1)
    runner = IsolatedPdfRunner()
    pages = runner.parse(raw, ExtractionSettings(max_pages=4, max_characters=4000))
    assert len(pages) == 1 and "inspect valve" in pages[0].text
    with pytest.raises(DocumentError):
        runner.parse(b"%PDF-malformed", ExtractionSettings())


def test_pilot_schedule_rejects_18_calls_and_500400_daily_units_without_quota_change(
    tmp_path,
):
    p, op, _approval, _raw, http, clock, _args = composition(tmp_path)
    limits = p.governance.policy.owner.model_copy(update={"requests_per_window": 16})
    # Isolated fixture policy, never mutate a real authority or reset history.
    from governance.ledger import GovernanceLedger

    p.governance = GovernanceLedger(
        tmp_path / "historical-fixture.sqlite",
        QuotaPolicy(version="historical-fixture/1", owner=limits, tenant=limits),
        p.governance.catalog,
        clock=lambda: clock[0],
    )

    def call(at, inp=24800, out=3000):
        return {
            "at": at,
            "input": inp,
            "output": out,
            "provider": "openai_compatible",
            "model": "offline-model",
            "workload": "DOCUMENT_BACKGROUND",
        }

    # Keep the 18-call daily-limit case in one UTC day, including when the
    # suite runs just before midnight. Forecasting is not execution permission.
    now = (int(clock[0]) // 86400 + 1) * 86400
    with pytest.raises(PilotError, match="limit"):
        forecast(
            p.governance,
            p.admission,
            p.authority,
            op,
            [call(now + i * 61) for i in range(18)],
        )
    # Daily conflict independently of the rolling request count: 500,400.
    daily_limits = limits.model_copy(update={"requests_per_window": 100})
    daily_ledger = GovernanceLedger(
        tmp_path / "daily-fixture.sqlite",
        QuotaPolicy(version="daily-fixture/1", owner=daily_limits, tenant=daily_limits),
        p.governance.catalog,
        clock=lambda: clock[0],
    )
    with pytest.raises(PilotError, match="limit"):
        forecast(
            daily_ledger,
            p.admission,
            p.authority,
            op,
            [call(now + i * 61) for i in range(18)],
        )
    schedule = [call(now + i * 61) for i in range(12)] + [
        call(now + 86400 + i * 61) for i in range(6)
    ]
    result = forecast(p.governance, p.admission, p.authority, op, schedule)
    assert result["status"] == "FORECAST_FITS_NOT_AUTHORIZATION"
    assert not p.governance.usage(op, p.authority) and not http.calls


def test_pilot_concurrency_intent_and_replay_survive_restart(tmp_path):
    env = composition(tmp_path)
    p, op, approval, _raw, _http, _clock, args = env
    begin(env)
    operation = uuid4()
    p.control.begin(approval.session_id, op.scope.identity(), operation, "question")
    restored = SupervisedPilot(**args)
    with pytest.raises(PilotError, match="reconciliation"):
        restored.control.begin(
            approval.session_id, op.scope.identity(), uuid4(), "synthesis"
        )
    restored.control.finish(operation)
    with pytest.raises(PilotError):
        restored.control.begin(
            approval.session_id, op.scope.identity(), operation, "question"
        )


def test_pilot_default_never_executes_external_or_unmarked_provider(tmp_path):
    p, _op, _approval, _raw, http, _clock, args = composition(tmp_path)
    p.provider.pilot_fixture = False
    with pytest.raises(PilotError):
        SupervisedPilot(**args)
    assert not http.calls


def test_shared_admission_exclusivity_is_atomic_and_backward_compatible(tmp_path):
    p, op, _approval, _raw, _http, _clock, _args = composition(tmp_path)

    def identity():
        return CallIdentity(
            op.scope.identity(),
            uuid4(),
            uuid4(),
            1,
            "fixture/1",
            "openai_compatible",
            "general",
            "offline-model",
            "fixture/1",
        )

    from llm.inference import InferenceRateLimitError, InferenceUsage

    serial = p.admission.acquire(identity(), 100, 100, "INTERACTIVE", exclusive=True)
    with pytest.raises(InferenceRateLimitError):
        p.admission.acquire(identity(), 100, 100, "INTERACTIVE")
    p.admission.finish(serial, usage=InferenceUsage(1, 1, 2), outcome="success")
    regular = p.admission.acquire(identity(), 100, 100, "INTERACTIVE")
    with pytest.raises(InferenceRateLimitError):
        p.admission.acquire(identity(), 100, 100, "INTERACTIVE", exclusive=True)
    p.admission.finish(regular, usage=InferenceUsage(1, 1, 2), outcome="success")


def test_stop_persists_when_pilot_audit_is_full(tmp_path):
    env = composition(tmp_path, policy=PilotPolicy(audit_limit=2))
    p, op, approval, _raw, http, _clock, args = env
    p.create_session(op, approval)
    with p.control.transaction() as db:
        p.control.event(db, approval.session_id, "FIXTURE_CAPACITY")
    p.stop(op)
    restored = SupervisedPilot(**args)
    with restored.control.transaction() as db:
        assert restored.control._config(db)["stopped"] == 1
    assert not http.calls


def test_pilot_cannot_reset_cohort_cap_by_closing_sessions(tmp_path):
    p, op, approval, _, http, _, _ = composition(tmp_path)
    for i in range(3):
        session = approval.model_copy(
            update={"session_id": uuid4(), "study_code": f"P{i + 1:03}"}
        )
        p.create_session(op, session)
        p.close(op, session.session_id)
    with pytest.raises(PilotError, match="limit"):
        p.create_session(op, approval.model_copy(update={"session_id": uuid4()}))
    assert not http.calls


def test_pilot_profiles_reserve_overhead_before_source_admission(tmp_path):
    p, _, _, _, http, _, args = composition(tmp_path)
    values = p.managed_settings.model_dump(mode="json")
    for profile in values["profiles"]:
        profile["input_tokens"] = 24800
    with pytest.raises(PilotError):
        SupervisedPilot(
            **{
                **args,
                "managed_settings": p.managed_settings.__class__.model_validate(values),
            }
        )
    assert not http.calls
