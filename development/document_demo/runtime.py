"""Explicit local fixture composition over the production document authorities.

No default provider factory, credential resolver, Azure SDK or test import is used.
First initialization and reopen are separate operations; missing truth is fatal.
"""
import json
import os
import ssl
import sqlite3
import time
from contextlib import closing
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from types import SimpleNamespace
from uuid import UUID, uuid4

import httpx

from documents.digestion.managed import ManagedSettings, StageProfile
from documents.digestion.models import DigestionProfile
from documents.jobs.models import JobSettings
from documents.jobs.sqlite import SQLiteJobLedger
from documents.models import Scope, stable_id
from documents.operator.actions import Actions
from documents.operator.service import LocalRunner, OperatorWorkflow
from documents.pilot import SessionApproval, SourceApproval, SupervisedPilot
from documents.publication.authority import SQLitePublicationAuthority
from documents.publication.encoding import RetrievalEncoder
from documents.publication.models import RetrievalProfile
from documents.publication.service import PublicationService
from documents.storage import LocalObjectStore
from governance.ledger import Limits, Price, PricingCatalog, QuotaPolicy
from llm.admission import AdmissionPolicy
from llm.openai_compatible import OpenAICompatibleProvider
from llm.structured import CapabilityProfile
from security.models import Action
from security.runtime import SecurityRuntime

from development.document_demo.fixtures import FixtureHTTP, FixtureModel, FixtureVectors
from development.document_demo.identity import FixtureOperatorVerifier

DATABASES = ("security.sqlite", "governance.sqlite", "admission.sqlite", "jobs.sqlite",
             "pilot.sqlite", "actions.sqlite", "publication.sqlite", "vectors.json")
TEXT = b"Valve inspection is required before operation.\nField safety was not tested.\n"


def build(root, *, initialize=False, deployment_env="local", fetch=None):
    if deployment_env not in {"local", "compose"} or os.environ.get("DEPLOYMENT_ENV") == "production":
        raise ValueError("Fixture execution is forbidden in production")
    root = Path(root).resolve()
    cfg = json.loads((root / "identity.json").read_text())
    # Identity fixture is loopback-only, never an arbitrary configured issuer.
    from urllib.parse import urlsplit
    if urlsplit(cfg["issuer"]).hostname != "localhost" or urlsplit(cfg["issuer"]).scheme != "https":
        raise ValueError("Loopback fixture identity required")
    private = root / "private"
    if initialize:
        private.mkdir(mode=0o700, exist_ok=False)
    elif not (private / "manifest.json").is_file() or any(not (private / p).is_file() for p in DATABASES):
        raise ValueError("Recorded authorities unavailable; reconciliation required")
    if not initialize:
        # Reference constructors permit explicit first creation. Reopen must
        # never mistake a truncated authority for that initial empty database.
        for name in DATABASES:
            if not name.endswith(".sqlite"):
                continue
            try:
                with closing(sqlite3.connect((private / name).as_uri() + "?mode=ro", uri=True)) as db:
                    if db.execute("PRAGMA user_version").fetchone()[0] != 1:
                        raise ValueError("Recorded authorities inconsistent; reconciliation required")
            except sqlite3.Error:
                raise ValueError("Recorded authorities inconsistent; reconciliation required") from None
    now = datetime.now(timezone.utc)
    scope = Scope(tenant=stable_id("polymind-identity/1/tenant", cfg["issuer"], "synthetic"),
                  owner=stable_id("polymind-identity/1/owner", cfg["issuer"], "synthetic", "operator"))
    if initialize:
        sources, approvals = [], []
        for index, (name, raw) in enumerate((("manual.txt", TEXT), ("manual.pdf", synthetic_pdf())), 1):
            source = SourceApproval(approval_id=f"synthetic-{index}", source_id=f"synthetic-manual/{index}",
                document_id=UUID(int=1800 + index), owner=scope, sha256=sha256(raw).hexdigest(),
                filename=name, mime="text/plain" if name.endswith("txt") else "application/pdf",
                classification="synthetic", rights_reference="authored-fixture/1", rights_approved=True,
                native_text_reviewed=True, provider_processing_approved=True,
                retention="approved_retained_nonpersonal", erasure_required=False,
                approved_by=scope.owner, approved_at=now, expires_at=now + timedelta(hours=1))
            sources.append(source.model_dump(mode="json"))
            for number in range(1, 4):
                approvals.append(SessionApproval(session_id=uuid4(), study_code=f"P{number:03}",
                    notice_version="synthetic/1", purpose="supervised_document_verification", mode="synthetic",
                    consent="synthetic_fixture", consent_at=None, approval_reference="synthetic-only/1",
                    source_approval=source.approval_id, approved_by=scope.owner, approved_at=now,
                    expires_at=now + timedelta(minutes=59), provider_processing_approved=True,
                    retention_reference="synthetic-retention/1", metadata_retention_until=now + timedelta(days=7)
                ).model_dump(mode="json"))
        manifest = dict(version="document-demo/1", sources=sources, approvals=approvals)
        (private / "manifest.json").write_text(json.dumps(manifest))
    else:
        manifest = json.loads((private / "manifest.json").read_text())
    limits = Limits(requests_per_window=100, window_seconds=86400, interactive_concurrent=1,
                    background_concurrent=1, reserved_tokens=112000, daily_tokens=500000,
                    monthly_tokens=1500000, monthly_cost="5")
    policy = QuotaPolicy(version="synthetic/1", owner=limits, tenant=limits)
    catalog = PricingCatalog(version="synthetic/1", currency="EUR", effective_date="2026-01-01",
        operator_approved=True, prices=(Price(provider="openai_compatible", model="offline-model",
            input_price="0.1", output_price="0.2", price_unit=1000000),))
    admission = AdmissionPolicy(rpm=2, tpm=30000, concurrent=2, interactive_rpm=1, interactive_tpm=2000,
                                interactive_slots=1, per_job_rpm=1, per_job_concurrent=1)
    configuration = SimpleNamespace(SECURITY_AUTHORITY_PATH=str(private / "security.sqlite"),
        OIDC_CONFIGURATION=dict(issuer=cfg["issuer"], audience="polymind-documents", jwks_url=cfg["issuer"] + "/jwks",
                                role_mapping={"operator": (Action.PUBLICATION_MANAGE,)}),
        GOVERNANCE_AUTHORITY_PATH=str(private / "governance.sqlite"), GOVERNANCE_POLICY=policy.model_dump(),
        GOVERNANCE_PRICING=catalog.model_dump(), GOVERNANCE_PROVIDER_PATH=str(private / "admission.sqlite"),
        GOVERNANCE_PROVIDER_KEY="document-demo/1", GOVERNANCE_PROVIDER_POLICY=admission.model_dump())
    runtime = SecurityRuntime(configuration)
    runtime.verifier = FixtureOperatorVerifier(runtime.verifier.config)
    def trusted_jwks():
        with httpx.Client(verify=ssl.create_default_context(cafile=str(root / "tls.crt")),
                          trust_env=False, timeout=3, follow_redirects=False) as client:
            result = client.get(cfg["issuer"] + "/jwks")
            result.raise_for_status()
            if len(result.content) > 65536:
                raise ValueError("fixture_jwks_limit")
            return result.json()
    runtime.verifier.fetch = fetch or trusted_jwks
    objects = LocalObjectStore(private / "objects")
    jobs = SQLiteJobLedger(JobSettings(database_path=private / "jobs.sqlite", lease_seconds=120))
    transport = FixtureHTTP()
    provider = OpenAICompatibleProvider(base_url="https://fixture.invalid/v1",
        model_map={"general": "offline-model", "summarization": "offline-model"}, http_client=transport,
        connect_timeout=5, read_timeout=60)
    provider.pilot_fixture = True
    capability = CapabilityProfile(version="synthetic-capability/1", context_tokens=28000, max_output_tokens=3000,
        overhead_tokens=100, safety_tokens=100, output_parameter="max_completion_tokens", streaming=False,
        usage_reporting=True, structured_output="json_object")
    strict = capability.model_copy(update=dict(version="synthetic-capability/2", structured_output="json_schema",
                                              schema_profile="azure-strict/1"))
    managed = ManagedSettings(capability=strict, child_input_bytes=7000, generation_profile="managed-generation/2",
        max_response_envelope_bytes=26192, profiles=tuple(StageProfile(stage=s, input_tokens=24600, output_tokens=3000,
            template_version="managed-prompt/11") for s in ("chunk", "intermediate", "structural", "root")))
    vectors = FixtureVectors(private / "vectors.json", initialize=initialize)
    publication = PublicationService(SQLitePublicationAuthority(private / "publication.sqlite"), objects, jobs,
        vectors, RetrievalEncoder(RetrievalProfile(), FixtureModel()), scope)
    planning = DigestionProfile(context_tokens=28000, reserved_output_tokens=3000, template_tokens=64,
        chunk_characters=3200, max_fan_in=4, max_result_characters=10000, max_response_bytes=10000,
        max_claims=8, max_claim_characters=256, max_annotations=8, max_source_units=5000, max_chunks=900,
        max_steps=1000, max_artifact_bytes=32000000, max_depth=32, minimum_coverage=1, max_failed_units=0)
    pilot = SupervisedPilot(control_path=private / "pilot.sqlite", authority=runtime.authority, objects=objects,
        jobs=jobs, governance=runtime.governance, admission=runtime.admission, provider=provider,
        managed_settings=managed, analysis_capability=capability, planning_profile=planning,
        publication=publication, sources=tuple(SourceApproval.model_validate(s) for s in manifest["sources"]),
        reranker=lambda q, docs, top_k: docs[:top_k], initialize=initialize)
    workflow = OperatorWorkflow(pilot, Actions(private / "actions.sqlite", initialize=initialize),
        (cfg["issuer"], "synthetic", "operator"), {"synthetic-1": TEXT, "synthetic-2": synthetic_pdf()},
        tuple(SessionApproval.model_validate(a) for a in manifest["approvals"]))
    def ready_for_step():
        # Include durable previous calls after restart; a restarted transport
        # counter cannot reset the shared RPM/TPM window.
        with runtime.admission._transaction() as db:
            last = db.execute("SELECT MAX(started) FROM inference_calls WHERE quota=?",
                              (runtime.admission.quota_key,)).fetchone()[0]
        return last is None or time.time() >= last + 61
    runner = LocalRunner(workflow, admission_ready=ready_for_step)
    return runtime, workflow, runner, transport


def synthetic_pdf():
    from io import BytesIO
    from pypdf import PdfWriter
    from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject
    writer = PdfWriter()
    page = writer.add_blank_page(width=612, height=792)
    font = writer._add_object(DictionaryObject({NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"), NameObject("/BaseFont"): NameObject("/Helvetica")}))
    page[NameObject("/Resources")] = DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})})
    stream = DecodedStreamObject()
    stream.set_data(b"BT /F1 12 Tf 40 750 Td (Valve inspection is required before operation.) Tj 0 -20 Td (Field safety was not tested.) Tj ET")
    page[NameObject("/Contents")] = writer._add_object(stream)
    out = BytesIO()
    writer.write(out)
    return out.getvalue()
