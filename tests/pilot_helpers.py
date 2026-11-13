"""Deterministic pilot composition; real domain services, no provider network."""

import json
import time
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from uuid import UUID, uuid4

from documents.digestion.managed import ManagedSettings, StageProfile
from documents.jobs.models import JobSettings
from documents.jobs.sqlite import SQLiteJobLedger
from documents.pilot import SessionApproval, SourceApproval, SupervisedPilot
from documents.publication.authority import SQLitePublicationAuthority
from documents.publication.encoding import RetrievalEncoder
from documents.publication.models import RetrievalProfile
from documents.publication.service import PublicationService
from documents.storage import LocalObjectStore
from governance.ledger import (
    GovernanceLedger,
    Limits,
    Price,
    PricingCatalog,
    QuotaPolicy,
)
from llm.admission import SQLiteInferenceAdmission
from llm.openai_compatible import OpenAICompatibleProvider
from security.authority import SecurityAuthority
from security.models import Action, _verified_principal
from tests.performance.fixtures import profile
from tests.performance.foundry_preflight import OfflineHTTP
from tests.performance.foundry_recalibration import (
    candidate_capability,
    candidate_policy,
)
from tests.performance.phase17h import SyntheticModel, SyntheticVectors


class PilotHTTP(OfflineHTTP):
    def __init__(self):
        super().__init__()
        self.hook = None
        self.forged = False
        self.abstain = False

    def post(self, *args, **kwargs):
        if self.hook:
            self.hook()
        return super().post(*args, **kwargs)

    def response(self, sent, result, stage):
        if stage == "question":
            evidence = json.loads(sent["messages"][1]["content"])[
                "ORIGINAL_SOURCE_EVIDENCE"
            ][0]
            result = json.dumps(
                {
                    "answer": "Evidence is insufficient."
                    if self.abstain
                    else evidence["excerpt"],
                    "evidence_status": "insufficient" if self.abstain else "available",
                    "citation_ids": []
                    if self.abstain
                    else ["FORGED" if self.forged else evidence["citation_id"]],
                }
            )
        return super().response(sent, result, stage)


def composition(
    root,
    *,
    raw=b"Valve inspection is required before operation.\nField safety was not tested.\n",
    pdf=False,
    policy=None,
    budget="5",
):
    root = Path(root)
    root.mkdir(exist_ok=True)
    now = datetime.now(timezone.utc)
    clock = [now.timestamp()]
    operator = _verified_principal(
        "pilot-fixture",
        "operator",
        "synthetic",
        frozenset({Action.PUBLICATION_MANAGE}),
        expires=int(time.time()) + 3600,
    )
    security = SecurityAuthority(root / "security.sqlite", clock=lambda: clock[0])
    security.register(operator)
    objects = LocalObjectStore(root / "objects")
    jobs = SQLiteJobLedger(
        JobSettings(database_path=root / "jobs.sqlite", lease_seconds=120)
    )
    limits = Limits(
        requests_per_window=100,
        window_seconds=86400,
        interactive_concurrent=1,
        background_concurrent=1,
        reserved_tokens=112000,
        daily_tokens=500000,
        monthly_tokens=1500000,
        monthly_cost=budget,
    )
    catalog = PricingCatalog(
        version="synthetic/1",
        currency="EUR",
        effective_date="2026-01-01",
        operator_approved=True,
        prices=(
            Price(
                provider="openai_compatible",
                model="offline-model",
                input_price="0.1",
                output_price="0.2",
                price_unit=1000000,
            ),
        ),
    )
    governance = GovernanceLedger(
        root / "governance.sqlite",
        QuotaPolicy(version="fixture/1", owner=limits, tenant=limits),
        catalog,
        clock=lambda: clock[0],
    )
    admission = SQLiteInferenceAdmission(
        root / "admission.sqlite", "fixture", candidate_policy(), clock=lambda: clock[0]
    )
    http = PilotHTTP()
    provider = OpenAICompatibleProvider(
        base_url="https://offline.invalid/openai/v1",
        model_map={"summarization": "offline-model", "general": "offline-model"},
        http_client=http,
    )
    provider.pilot_fixture = True
    managed = ManagedSettings(
        capability=candidate_capability(strict_digestion=True),
        child_input_bytes=7000,
        generation_profile="managed-generation/2",
        max_response_envelope_bytes=26192,
        profiles=tuple(
            StageProfile(
                stage=s,
                input_tokens=24600,
                output_tokens=3000,
                template_version="managed-prompt/11",
            )
            for s in ("chunk", "intermediate", "structural", "root")
        ),
    )
    publication = PublicationService(
        SQLitePublicationAuthority(root / "publication.sqlite"),
        objects,
        jobs,
        SyntheticVectors(),
        RetrievalEncoder(RetrievalProfile(), SyntheticModel()),
        operator.scope,
    )
    source = SourceApproval(
        approval_id="source-1",
        source_id="synthetic-manual/1",
        document_id=UUID(int=171),
        owner=operator.scope,
        sha256=sha256(raw).hexdigest(),
        filename="manual.pdf" if pdf else "manual.txt",
        mime="application/pdf" if pdf else "text/plain",
        classification="synthetic",
        rights_reference="authored-fixture/1",
        rights_approved=True,
        native_text_reviewed=True,
        provider_processing_approved=True,
        retention="approved_retained_nonpersonal",
        erasure_required=False,
        approved_by=operator.scope.owner,
        approved_at=now,
        expires_at=now + timedelta(hours=1),
    )
    args = {
        "control_path": root / "pilot.sqlite",
        "authority": security,
        "objects": objects,
        "jobs": jobs,
        "governance": governance,
        "admission": admission,
        "provider": provider,
        "managed_settings": managed,
        "analysis_capability": candidate_capability(),
        "planning_profile": profile(
            context_tokens=28000,
            reserved_output_tokens=3000,
            max_result_characters=10000,
            max_response_bytes=10000,
        ),
        "publication": publication,
        "sources": (source,),
        "clock": lambda: clock[0],
        "reranker": lambda q, docs, top_k: docs[:top_k],
    }
    if policy:
        args["policy"] = policy
    pilot = SupervisedPilot(**args, initialize=True)
    approval = SessionApproval(
        session_id=uuid4(),
        study_code="P001",
        notice_version="draft/1",
        purpose="supervised_document_verification",
        mode="synthetic",
        consent="synthetic_fixture",
        consent_at=None,
        approval_reference="synthetic-only/1",
        source_approval=source.approval_id,
        approved_by=operator.scope.owner,
        approved_at=now,
        expires_at=now + timedelta(minutes=59),
        provider_processing_approved=True,
        retention_reference="fixture-retention/1",
        metadata_retention_until=now + timedelta(days=7),
    )
    return pilot, operator, approval, raw, http, clock, args


def begin(env):
    pilot, op, approval, raw, _http, _clock, _args = env
    pilot.create_session(op, approval)
    plan = pilot.select_source(op, approval.session_id, raw)
    pilot.start(op, approval.session_id)
    return plan


def complete(env):
    p, op, approval, _raw, _http, clock, _args = env
    begin(env)
    for _ in range(8):
        clock[0] += 61
        status = p.step(op, approval.session_id)
        if status.get("job_state") in {"COMPLETED", "PARTIAL", "FAILED", "CANCELLED"}:
            break
    assert status["job_state"] == "COMPLETED", status
    assert status["digest_status"] == "COMPLETE"
    p.publish(op, approval.session_id)
    return status
