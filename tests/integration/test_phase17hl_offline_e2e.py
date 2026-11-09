"""L1 contracts through real local components and an explicit HTTP transport fake.

Run with the pre-collection socket-denial plugin recorded in the phase report.
No live launcher, credential, approval, provider factory or remote client is used.
"""

import json
import socket
import subprocess
import sys
import time
from decimal import Decimal
from hashlib import sha256
from types import SimpleNamespace
from uuid import UUID

import pytest
from jsonschema import Draft202012Validator

from documents.digestion import workflow
from documents.digestion.codec import encode, read
from documents.digestion.managed import (
    ManagedDigestionHandler,
    classify_managed,
    generation_schema,
)
from documents.digestion.models import Checkpoint, DigestionError, StageResult
from documents.digestion.validation import EvidenceIndex
from documents.jobs.sqlite import SQLiteJobLedger
from documents.models import stable_id
from documents.publication.analysis import AnalysisRequest, DocumentAnalysis
from documents.storage import LocalObjectStore
from llm.azure_schema import provider_schema
from llm.openai_compatible import OpenAICompatibleProvider
from security.models import Action, SecurityError, _verified_principal
from security.services import AuthorizedPublication
from tests.performance import foundry_l1, foundry_preflight
from tests.performance.fixtures import INJECTION, pdf


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    def deny(*args, **kwargs):
        pytest.fail("Offline L1 attempted network access")

    for name in ("connect", "connect_ex", "sendto"):
        monkeypatch.setattr(socket.socket, name, deny)
    for name in ("create_connection", "getaddrinfo", "gethostbyname"):
        monkeypatch.setattr(socket, name, deny)


@pytest.fixture
def l1(tmp_path, monkeypatch, record_property):
    """Observe production boundaries without replacing their decisions or output."""
    state = SimpleNamespace(
        root=tmp_path, sent=[], generations=[], validated=[], errors=[], requests=[]
    )
    original_prepare = workflow.prepare
    original_admit = workflow.admit
    original_validate = workflow.validate_result
    original_analyze = ManagedDigestionHandler.analyze
    original_publish = foundry_preflight.publish
    original_execute = OpenAICompatibleProvider.execute
    original_contract = foundry_preflight.synthetic_contract

    def execute(provider, request):
        state.generations.append(request)
        return original_execute(provider, request)

    def prepare(artifact, extraction_ref, profile, store):
        state.artifact, state.store = artifact, store
        state.plan, state.plan_ref = original_prepare(
            artifact, extraction_ref, profile, store
        )
        return state.plan, state.plan_ref

    def admit(ledger, store, plan, plan_ref, **kwargs):
        state.jobs = ledger
        admitted = original_admit(ledger, store, plan, plan_ref, **kwargs)
        if not hasattr(state, "job"):
            state.job = admitted
        return admitted

    def validate(raw, request, index):
        try:
            result = original_validate(raw, request, index)
        except DigestionError as exc:
            state.errors.append(exc)
            raise
        state.validated.append((request, result, raw))
        return result

    def analyze(handler, request, job, step, store, plan):
        state.handler = handler
        state.requests.append(request)
        if state.before_analyze is not None:
            state.before_analyze(handler)
        # Neither a successful provider response nor a checkpoint is job completion.
        assert (
            handler.ledger.get_job(job.admission.scope, job.job_id).state != "COMPLETED"
        )
        assert not any(
            s.manifest
            for s in handler.ledger.steps(job.admission.scope, job.job_id)
            if s.spec.unit_id == "digest"
        )
        return original_analyze(handler, request, job, step, store, plan)

    def publish(*args, **kwargs):
        summary, state.replica = original_publish(*args, **kwargs)
        state.authority, state.operator, state.principal = args[5:8]
        return summary, state.replica

    class HTTP(foundry_preflight.OfflineHTTP):
        def post(self, url, **kwargs):
            state.sent.append((url, kwargs))
            return super().post(url, **kwargs)

        def response(self, sent, result, stage):
            data = json.loads(sent["messages"][1]["content"])
            if stage == "chunk":
                leaf = json.loads(result)
                leaf["claims"][0]["qualifications"] = [
                    {
                        "text": "Before operation.",
                        "evidence_ids": leaf["claims"][0]["evidence_ids"][:1],
                    }
                ]
                if state.two_chunks:
                    source = ''.join(p['text'] for p in data['UNTRUSTED_DOCUMENT_DATA'])
                    affirmed = 'Access is permitted during daytime.' in source
                    finding = ('Access is permitted during daytime.' if affirmed
                               else 'Access is denied during maintenance.')
                    assert finding in source
                    leaf['claims'][0].update(text=finding, subject='access',
                        stance='affirmed' if affirmed else 'denied', qualifications=[{
                            'text': 'Only during daytime.' if affirmed else 'During maintenance.',
                            'evidence_ids': leaf['claims'][0]['evidence_ids'][:1]}])
                result = json.dumps(leaf)
            elif stage in ('structural', 'root') and state.two_chunks:
                reduction = json.loads(result)
                reduction['claims'][0]['text'] = (
                    'Access is permitted: Only during daytime. Access is denied: During maintenance. '
                    'Conflicting source findings remain unresolved.')
                result = json.dumps(reduction)
            elif stage == "question":
                evidence = data["ORIGINAL_SOURCE_EVIDENCE"][0]
                if state.two_chunks:
                    evidence = next(c for c in data['ORIGINAL_SOURCE_EVIDENCE']
                                    if 'Access is permitted during daytime.' in c['excerpt'])
                result = json.dumps(
                    {
                        "answer": evidence["excerpt"],
                        "evidence_status": "available",
                        "citation_ids": [evidence["citation_id"]],
                    }
                )
            # Faults are deliberately injected only in the controlled transport fake.
            result = state.transform(result, stage)
            response = super().response(sent, result, stage)
            state.http = self
            return response

    monkeypatch.setattr(workflow, "prepare", prepare)
    monkeypatch.setattr(workflow, "admit", admit)
    monkeypatch.setattr(workflow, "validate_result", validate)
    monkeypatch.setattr(ManagedDigestionHandler, "analyze", analyze)
    monkeypatch.setattr(foundry_preflight, "publish", publish)
    monkeypatch.setattr(foundry_preflight, "OfflineHTTP", HTTP)
    monkeypatch.setattr(OpenAICompatibleProvider, "execute", execute)
    from tests.performance.foundry_budget import Contract

    # Same L1 per-experiment ceilings, with an explicitly synthetic pricing catalog.
    def contract():
        return Contract.model_validate(
            {
                **original_contract().model_dump(mode="json"),
                "attempts": 5 if state.two_chunks else 4,
                "total_input": 125000 if state.two_chunks else 100000,
                "total_output": 15000 if state.two_chunks else 12000,
                "rpm": 1,
            }
        )

    monkeypatch.setattr(foundry_preflight, "synthetic_contract", contract)

    def run(transform=lambda value, stage: value, *, before_analyze=None, two_chunks=False):
        state.transform = transform
        state.before_analyze = before_analyze
        state.two_chunks = two_chunks
        if two_chunks:
            from tests.performance import fixtures
            original_lines = fixtures.page_lines
            original_profile = foundry_preflight.profile

            def lines(page, count, rng):
                result = original_lines(page, count, rng)
                if page in (1, 3):
                    result[1] = ('Access is permitted during daytime.' if page == 1
                                 else 'Access is denied during maintenance.')
                return result

            monkeypatch.setattr(fixtures, 'page_lines', lines)
            monkeypatch.setattr(foundry_preflight, 'profile', lambda **kw: original_profile(
                **{**kw, 'chunk_characters': 800}))
        state.result = foundry_preflight.execute(tmp_path, "L1")
        record_property("synthetic_provider_calls", len(state.sent))
        return state

    run.state = state
    return run


def reopen(state):
    jobs = SQLiteJobLedger(state.jobs.settings)
    store = LocalObjectStore(state.root / "objects")
    scope = state.artifact.document.scope
    digest = workflow.load_digest(jobs, store, scope, state.job.job_id)
    return jobs, store, scope, digest


def assert_accounting(state, calls, *, unknown=False):
    result = state.result
    assert result["calls"] == len(state.sent) == calls
    assert len(result["provider_records"]) == calls
    assert len(result["governance_records"]) == calls
    assert len(result["run_records"]) == calls
    assert all(
        row["input"] == 25000 and row["output"] == 3000 for row in result["run_records"]
    )
    rows = result["governance_records"]
    if unknown:
        assert rows[-1]["state"] == "UNKNOWN"
        assert rows[-1]["actual_cost"] is None
        assert result["run_records"][-1]["finished"] is None
    else:
        assert all(row["state"] == "SETTLED" for row in rows)
        assert all(
            row["actual_input"] == 30 and row["actual_output"] == 40 for row in rows
        )
        assert (
            sum(Decimal(row["actual_cost"]) for row in rows)
            == Decimal("0.000011") * calls
        )
        assert all(Decimal(row["cost"]) > Decimal(row["actual_cost"]) for row in rows)
        assert all(row["finished"] is not None for row in result["run_records"])
        assert all(
            json.loads(row["usage"])["total"] == 70 for row in result["run_records"]
        )
    assert len({row["identity"] for row in rows}) == calls


def test_l1_extraction_dag_schema_digest_citations_accounting_and_reopen(l1):
    state = l1()
    artifact, plan = state.artifact, state.plan
    raw, manifest = pdf(4)
    assert pdf(4) == (raw, manifest)
    assert (state.root / "source.pdf").read_bytes() == raw
    assert manifest["version"] == "phase17h-pdf/1" and manifest["seed"] == 1708
    assert sha256(raw).hexdigest() == artifact.document.source.sha256
    assert len(artifact.units) == artifact.document.page_count == 4
    assert [u.text.splitlines() for u in artifact.units] == [
        p["lines"] for p in manifest["expected"]
    ]
    assert len(plan.chunks) == 1 and len(plan.chunks[0].pieces) == 4
    assert [r.level for r in plan.reducers] == [1, 2]
    assert plan.reducers[0].children == (plan.chunks[0].chunk_id,)
    assert plan.reducers[1].children == (plan.reducers[0].stage_id,)
    assert plan.root_id == plan.reducers[1].stage_id
    assert [u.kind for u in plan.structure.units] == ["document", "fallback"]
    assert state.result["job_state"] == "COMPLETED"
    assert state.result["questions"]["status"] == "COMPLETE"
    assert state.result["planned_digestion_calls"] == 3
    assert state.result["planned_calls"] == 4
    assert len(state.requests) == 3
    # Finalization and publication revalidate persisted checkpoints repeatedly.
    assert {r.stage_id for _, r, _ in state.validated} == {
        c.chunk_id for c in plan.chunks
    } | {r.stage_id for r in plan.reducers}
    assert all(
        sum(r.stage_id == req.stage_id for _, r, _ in state.validated) >= 2
        for req in state.requests
    )
    expected_schema = provider_schema(generation_schema())
    for number, (url, kwargs) in enumerate(state.sent):
        assert url == "https://offline.invalid/openai/v1/chat/completions"
        assert kwargs["allow_redirects"] is False and kwargs["stream"] is True
        payload = kwargs["json"]
        assert payload["max_completion_tokens"] == 3000
        assert "tools" not in payload and "tool_choice" not in payload
        system, data = [m["content"] for m in payload["messages"]]
        if number == 3:
            assert payload["response_format"] == {"type": "json_object"}
            assert "OUTPUT_SCHEMA" in system
            assert set(
                json.loads(system.split("\nOUTPUT_SCHEMA\n")[1])["required"]
            ) == {"answer", "evidence_status", "citation_ids"}
            context = json.loads(data)
            assert context["ORIGINAL_SOURCE_EVIDENCE"]
            assert context["DERIVED_RETRIEVAL_MATERIAL"]
            assert all(
                c["document_id"] == str(artifact.document.document_id)
                for c in context["ORIGINAL_SOURCE_EVIDENCE"]
            )
            continue
        request = state.requests[number]
        generation = state.generations[number]
        assert generation.output_tokens == 3000 and generation.response_bytes == 10000
        assert generation.max_response_envelope_bytes == 26192
        control = json.loads(system.split("\nCONTROL\n")[1])
        assert payload["response_format"] == {
            "type": "json_schema",
            "json_schema": {
                "name": "polymind_stage_result",
                "strict": True,
                "schema": expected_schema,
            },
        }
        assert control["schema"] == generation_schema()
        assert control["profile"]["stage"] == ("chunk", "structural", "root")[number]
        assert control["stage_id"] == str(request.stage_id)
        assert control["kind"] == request.stage
        assert control["max_result_bytes"] == control["max_response_bytes"] == 10000
        assert control["claim_ids_in_order"] == [
            str(stable_id(str(request.stage_id), str(i)))
            for i in range(plan.profile.max_claims)
        ]
        assert control["required_child_links"] == [
            {"stage_id": str(child.result.stage_id), "claim_id": str(c.claim_id)}
            for child in request.children
            for c in child.result.claims
        ]
        expected_evidence = {str(p.evidence_id()) for p in request.source_data} | {
            str(e)
            for child in request.children
            for c in child.result.claims
            for e in (*c.evidence_ids, *c.contradicting_evidence_ids)
        }
        assert set(control["allowed_evidence_ids"]) == expected_evidence
        returned = StageResult.model_validate_json(state.http.calls[number]["response"])
        Draft202012Validator(expected_schema).validate(
            json.loads(state.http.calls[number]["response"])
        )
        assert len(encode(returned)) <= 10000
        assert returned == state.validated[number][1]
        assert all(
            c.claim_id == stable_id(str(request.stage_id), str(i))
            and c.originating_stage == request.stage_id
            for i, c in enumerate(returned.claims)
        )
        material = json.loads(data)
        if number == 0:
            assert INJECTION in data and INJECTION not in system
            assert len(material["UNTRUSTED_DOCUMENT_DATA"]) == 4
        else:
            assert not material["UNTRUSTED_DOCUMENT_DATA"]
            assert all(
                c["material_kind"] == "generated-intermediate"
                for c in material["GENERATED_CHILD_MATERIAL"]
            )
    jobs, store, scope, digest = reopen(state)
    assert digest.status == "COMPLETE" and digest.coverage.fraction == 1
    assert (
        set(digest.coverage.eligible)
        == set(digest.coverage.included)
        == set(plan.eligible)
    )
    assert not digest.coverage.failed and not digest.coverage.unsupported
    assert [q.text for q in digest.qualifications] == ["Before operation."]
    assert not digest.contradictions  # The four-page source has no opposing FACTS.
    assert (
        digest.extraction == plan.structure.extraction and digest.plan == state.plan_ref
    )
    assert digest.profile == plan.profile.digest() and digest.root == plan.root_id
    index = EvidenceIndex(artifact)
    assert len(digest.evidence) == 4
    assert all(index.resolve(e) for e in digest.evidence)
    steps = jobs.steps(scope, state.job.job_id)
    assert len(steps) == 5 and all(s.state == "SUCCEEDED" for s in steps)
    for step in steps[1:4]:
        checkpoint = read(
            store, scope, step.manifest[0], Checkpoint, plan.profile.max_artifact_bytes
        )
        assert checkpoint.result.stage_id == UUID(step.spec.unit_id)
        assert checkpoint.inherited.analyzed_pieces == 4
        assert checkpoint.inherited.qualifications == 1
    packets = json.loads((state.root / "review-packets.json").read_text())
    answer = packets[0]["response"]
    assert answer["evidence_status"] == "available" and answer["citations"]
    assert answer["answer"] == answer["citations"][0]["excerpt"]
    for citation in answer["citations"]:
        unit = next(
            u for u in artifact.units if u.physical_page == citation["physical_page"]
        )
        assert (
            citation["excerpt"]
            == unit.text[citation["span"]["start"] : citation["span"]["end"]]
        )
        assert citation["extraction_id"] == str(artifact.extraction_id)
        assert citation["document_version_id"] == str(
            artifact.document.document_version_id
        )
        assert citation["provenance"] == "validated"
    assert_accounting(state, 4)
    # Same admission, then supported checkpoint reuse: neither executes nor charges again.
    same = workflow.admit(
        jobs,
        store,
        plan,
        state.plan_ref,
        request_key="offline-preflight",
        retry=state.job.admission.profile.retry,
    )
    assert same.job_id == state.job.job_id
    resumed = workflow.admit(
        jobs,
        store,
        plan,
        state.plan_ref,
        request_key="resume",
        resume_from=same.job_id,
        retry=same.admission.profile.retry,
    )
    from documents.jobs.worker import LocalDispatcher, Worker, relay

    queue = LocalDispatcher()
    worker = Worker(
        jobs,
        queue,
        store,
        ManagedDigestionHandler(jobs, state.plan_ref, state.handler.inference),
        owner="offline-reopen",
        classifier=classify_managed,
    )
    for _ in range(plan.profile.max_steps):
        relay(jobs, queue)
        if not worker.once():
            break
    assert workflow.load_digest(jobs, store, scope, resumed.job_id) == digest
    assert jobs.get_job(scope, resumed.job_id).state == "COMPLETED"
    assert len(state.sent) == 4
    assert (
        state.handler.inference.governance.ledger.usage(
            state.principal, state.authority
        )
        == state.result["governance_records"]
    )
    active = state.replica.reader.authority.active()
    inventory = state.replica.reader.authority.inventory()
    repeated = AuthorizedPublication(state.authority, state.replica.reader).run(
        state.operator, "plan", [same.job_id]
    )
    assert repeated.generation == active.generation
    assert state.replica.reader.authority.inventory() == inventory
    assert state.replica.reader.authority.active() == active


def test_revoked_background_authorization_denies_before_reservation(l1):
    def revoke(handler):
        governed = handler.inference.governance
        snapshot = governed.snapshot
        governed.authority.tombstone(snapshot.principal, snapshot.documents[0][0])

    state = l1(before_analyze=revoke)
    assert state.result["job_state"] == "FAILED"
    assert state.result["terminal_category"] == "security_denied"
    assert_accounting(state, 0)
    assert "publication" not in state.result


FAULTS = [
    ("json", "chunk", "serialization_error", "json_decode", 1),
    ("duplicate", "chunk", "serialization_error", "duplicate_json_key", 1),
    ("extra", "chunk", "serialization_error", "pydantic_validation", 1),
    ("uuid", "chunk", "serialization_error", "pydantic_validation", 1),
    ("stage", "chunk", "serialization_error", "stage_binding", 1),
    ("kind", "chunk", "serialization_error", "stage_binding", 1),
    ("claim", "chunk", "serialization_error", "claim_identity", 1),
    ("origin", "chunk", "serialization_error", "claim_identity", 1),
    ("evidence", "chunk", "invalid_reference", "evidence_validation", 1),
    ("coverage", "chunk", "extraction_failed", "coverage_validation", 1),
    ("lineage", "structural", "invalid_reference", "evidence_validation", 2),
    ("coverage", "structural", "extraction_failed", "coverage_validation", 2),
    ("lineage", "root", "invalid_reference", "evidence_validation", 3),
    ("coverage", "root", "extraction_failed", "coverage_validation", 3),
    ("claim", "root", "serialization_error", "claim_identity", 3),
    ("evidence", "root", "invalid_reference", "evidence_validation", 3),
    ("canonical_limit", "chunk", "extraction_limit_exceeded", "response_limit", 1),
]


def corrupt(value, case):
    data = json.loads(value)
    claim = data["claims"][0]
    foreign = str(UUID(int=987654))
    if case == "json":
        return "{SYNTHETIC_PRIVATE_PAYLOAD"
    if case == "duplicate":
        return '{"SYNTHETIC_PRIVATE_PAYLOAD":1,"SYNTHETIC_PRIVATE_PAYLOAD":2}'
    if case == "extra":
        data["SYNTHETIC_PRIVATE_PAYLOAD"] = "SYNTHETIC_PRIVATE_PAYLOAD"
    elif case == "uuid":
        data["stage_id"] = "malformed-uuid"
    elif case == "stage":
        data["stage_id"] = foreign
    elif case == "kind":
        data["kind"] = "reduction"
    elif case == "claim":
        claim["claim_id"] = foreign
    elif case == "origin":
        claim["originating_stage"] = foreign
    elif case == "evidence":
        claim["evidence_ids"] = [foreign]
    elif case == "lineage":
        claim["lineage"] = [{"stage_id": foreign, "claim_id": foreign}]
    elif case == "coverage":
        claim.update(kind="commentary", evidence_ids=[], lineage=[])
    elif case == "canonical_limit":
        # 1,600 multibyte characters fit raw UTF-8, exceed canonical ASCII JSON.
        claim["text"] = "\u0800" * 1600
    return json.dumps(data, ensure_ascii=False)


@pytest.mark.parametrize("case,target,category,diagnostic,calls", FAULTS)
def test_strict_rejection_preserves_paid_usage_and_never_completes(
    l1, case, target, category, diagnostic, calls
):
    state = l1(lambda value, stage: corrupt(value, case) if stage == target else value)
    assert state.result["job_state"] == "FAILED"
    assert state.result["terminal_category"] == category
    assert "publication" not in state.result and "questions" not in state.result
    error = state.errors[-1]
    assert error.validation_diagnostic.value == diagnostic
    assert "SYNTHETIC_PRIVATE_PAYLOAD" not in str(error)
    assert_accounting(state, calls)
    steps = state.jobs.steps(state.artifact.document.scope, state.job.job_id)
    assert len([s for s in steps if s.state == "FAILED"]) == 1
    assert not any(
        s.manifest for s in steps if s.state == "FAILED" or s.spec.unit_id == "digest"
    )
    with pytest.raises(DigestionError):
        workflow.load_digest(
            state.jobs, state.store, state.artifact.document.scope, state.job.job_id
        )


def test_mixed_qualification_provenance_stops_after_first_call(l1):
    from tests.integration.test_final_offline_azure_compatibility import qualification_witness

    def response(value, stage):
        assert stage == "chunk"  # No reducer, root or grounded Q&A call follows.
        data = qualification_witness(value, "blended")
        Draft202012Validator(provider_schema(generation_schema())).validate(data)
        return encode(StageResult.model_validate(data)).decode()

    state = l1(response)
    assert state.result["job_state"] == "FAILED"
    assert state.result["terminal_category"] == "invalid_reference"
    assert len(state.requests) == len(state.generations) == 1
    assert not state.validated
    error = state.errors[-1]
    assert error.category == "evidence_validation_failed"
    assert error.validation_diagnostic.value == "evidence_validation"
    assert error.validation_reason.value == "invalid_qualification_source"
    assert "publication" not in state.result and "questions" not in state.result
    assert_accounting(state, 1)
    scope = state.artifact.document.scope
    steps = state.jobs.steps(scope, state.job.job_id)
    failed, = [s for s in steps if s.state == "FAILED"]
    assert failed.attempt_count == 1 and not failed.manifest
    stage_ids = {str(state.plan.root_id), *(str(r.stage_id) for r in state.plan.reducers), "digest"}
    downstream = [s for s in steps if s.spec.unit_id in stage_ids]
    assert len(downstream) == 3
    assert all(s.state == "CANCELLED" and s.attempt_count == 0 and not s.manifest for s in downstream)
    with pytest.raises(DigestionError):
        workflow.load_digest(state.jobs, state.store, scope, state.job.job_id)


@pytest.mark.parametrize(
    "case", ["raw_limit", "truncated", "envelope", "unknown_usage", "exception"]
)
def test_provider_failures_accounting_and_primary_classification(l1, monkeypatch, case):
    if case == "unknown_usage":
        from llm.openai_compatible import OpenAICompatibleProvider

        monkeypatch.setattr(
            OpenAICompatibleProvider, "_usage", staticmethod(lambda value: None)
        )
    if case in ("truncated", "envelope", "exception"):
        from tests.unit.test_structured_provider import Response

        original = foundry_preflight.OfflineHTTP.post

        def post(self, url, **kwargs):
            response = original(self, url, **kwargs)
            if case == "exception":
                raise RuntimeError("SYNTHETIC_PRIVATE_PAYLOAD")
            payload = json.loads(b"".join(response.iter_content(1)))
            if case == "truncated":
                payload["choices"][0]["finish_reason"] = "length"
            else:
                payload["padding"] = "x" * 26193
            return Response(payload)

        monkeypatch.setattr(foundry_preflight.OfflineHTTP, "post", post)
    state = l1(
        lambda value, stage: value + " " * 10001 if case == "raw_limit" else value
    )
    assert state.result["job_state"] == "FAILED"
    assert state.result["terminal_category"] == (
        "governance_denied"
        if case == "unknown_usage"
        else "worker_failed"
        if case == "exception"
        else "inference_output_limit"
    )
    assert not state.errors  # Provider/governance failed before application decoding.
    assert_accounting(
        state, 1, unknown=case in ("unknown_usage", "envelope", "exception")
    )


def test_failed_qa_leaves_completed_digest_and_settled_usage(l1):
    state = l1(
        lambda value, stage: (
            json.dumps(
                {
                    "answer": "bad",
                    "evidence_status": "available",
                    "citation_ids": ["FOREIGN"],
                }
            )
            if stage == "question"
            else value
        )
    )
    assert state.result["job_state"] == "COMPLETED"
    assert state.result["questions"]["status"] == "BLOCKED"
    packet = json.loads((state.root / "review-packets.json").read_text())[0]
    assert packet["failure"] == "citation_invalid" and "response" not in packet
    assert reopen(state)[-1].status == "COMPLETE"
    assert_accounting(state, 4)


def test_authorization_and_revocation_prevent_retrieval_and_inference(l1):
    state = l1()
    authority, principal = state.authority, state.principal
    replica, doc = state.replica, state.artifact.document.document_id
    from security.services import AuthorizedAnalysis

    inference = state.handler.inference
    secured = AuthorizedAnalysis(
        authority,
        inference.governance.ledger,
        inference.admission,
        {
            principal.scope.identity(): DocumentAnalysis(
                replica,
                inference.provider,
                foundry_preflight.candidate_capability(),
                reranker=lambda q, docs, top_k: docs[:top_k],
            )
        },
    )
    query = AnalysisRequest(query="inspect", document_ids=(doc,))
    for tenant in ("fixture", "foreign-tenant"):
        stranger = _verified_principal(
            "offline", "stranger", tenant, expires=int(time.time()) + 3600
        )
        authority.register(stranger)
        with pytest.raises(SecurityError):
            secured.analyze(stranger, query)
        with pytest.raises(SecurityError):
            AuthorizedPublication(authority, replica.reader).run(
                stranger, "plan", [state.job.job_id]
            )
    with pytest.raises(SecurityError):
        secured.analyze(
            principal, AnalysisRequest(query="inspect", document_ids=(UUID(int=99),))
        )
    snapshot = authority.snapshot(principal, (doc,), Action.DOCUMENT_ANALYZE)
    authority.tombstone(principal, doc)
    with pytest.raises(SecurityError):
        replica.pin((doc,), authorization=(authority, snapshot))
    with pytest.raises(SecurityError):
        secured.analyze(principal, query)
    assert len(state.sent) == 4


@pytest.mark.parametrize("outcome", ["success", "digestion_failure", "qa_failure"])
def test_runner_exit_agrees_with_real_durable_result(l1, monkeypatch, capsys, outcome):
    def transform(value, stage):
        if outcome == "digestion_failure" and stage == "chunk":
            return "{"
        if outcome == "qa_failure" and stage == "question":
            return "{}"
        return value

    state = l1(transform)
    monkeypatch.setattr(foundry_preflight, "execute", lambda root, stage: state.result)
    monkeypatch.setattr(
        foundry_l1, "launch", lambda *args, **kwargs: pytest.fail("Live path reached")
    )
    monkeypatch.setattr(
        sys, "argv", ["foundry_l1", "--output", str(state.root / "cli")]
    )
    if outcome == "success":
        foundry_l1.main()
    else:
        with pytest.raises(SystemExit) as caught:
            foundry_l1.main()
        assert caught.value.code == 1
    result = json.loads(capsys.readouterr().out)
    assert result == {
        "stage": "L1",
        "state": state.result["job_state"],
        "calls": state.result["calls"],
        "questions_status": state.result.get("questions", {}).get("status"),
    }


@pytest.mark.parametrize("failure", [False, True])
def test_real_offline_process_exit_status(tmp_path, record_property, failure):
    # The child installs the same pre-import network guard, then uses only the
    # default offline command. It cannot load configuration or approval packets.
    script = """
import socket
def deny(*args, **kwargs):
    raise AssertionError('Offline child attempted network access')
for name in ('connect', 'connect_ex', 'sendto'):
    setattr(socket.socket, name, deny)
for name in ('create_connection', 'getaddrinfo', 'gethostbyname'):
    setattr(socket, name, deny)
import sys
from tests.performance import foundry_preflight
from tests.performance.foundry_l1 import main
if sys.argv.pop(1) == 'fail':
    original = foundry_preflight.OfflineHTTP.response
    def response(self, sent, result, stage):
        return original(self, sent, '{', stage)
    foundry_preflight.OfflineHTTP.response = response
main()
"""
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            script,
            "fail" if failure else "pass",
            "--output",
            str(tmp_path / "child"),
        ],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    durable = json.loads((tmp_path / "child" / "result.json").read_text())
    machine = json.loads(result.stdout)
    assert (
        machine["state"]
        == durable["job_state"]
        == ("FAILED" if failure else "COMPLETED")
    )
    assert machine["calls"] == durable["calls"] == (1 if failure else 4)
    assert machine["questions_status"] == durable.get("questions", {}).get("status")
    assert result.returncode == (1 if failure else 0)
    record_property("synthetic_provider_calls", durable["calls"])
