"""Phase 18 protected composition tests using real ledgers and signed test JWTs."""
import asyncio
import json
import socket
import time
from uuid import UUID, uuid4

import jwt
import pytest
from fastapi.testclient import TestClient

from development.document_demo.app import create_app
from development.document_demo.provision import provision
from development.document_demo.runtime import build
from documents.pilot.models import PilotError


@pytest.fixture
def operator_env(tmp_path, monkeypatch):
    monkeypatch.setenv("DOCUMENTS_PROFILE", "synthetic")
    root = provision(tmp_path / "runtime")
    identity = json.loads((root / "identity.json").read_text())
    runtime, workflow, runner, transport = build(root, initialize=True,
        fetch=lambda: {"keys": [identity["jwk"]]})
    # Deterministically after provisioning, independent of host clock corrections.
    virtual = [max(a.approved_at.timestamp() for a in workflow.approvals) + 1]
    for target in (runtime.authority, runtime.governance, runtime.admission, workflow.pilot, workflow.pilot.control):
        target.clock = lambda: virtual[0]
    runner.admission_ready = lambda: True

    def token(**changes):
        claims = dict(iss=identity["issuer"], sub="operator", tid="synthetic", aud="polymind-documents",
                      token_use="access", roles=["operator"], nbf=int(time.time()), exp=int(time.time()) + 3600)
        claims.update(changes)
        return jwt.encode(claims, (root / "signing.pem").read_bytes(), algorithm="RS256", headers={"kid": "fixture"})
    principal = runtime.verifier.verify(token())
    runtime.authority.register(principal)
    app = create_app(runtime, workflow, runner, run_worker=False)
    client = TestClient(app, raise_server_exceptions=False)
    client.headers["Authorization"] = "Bearer " + token()
    # All provider effects must remain in-process. Even test JWKS is in-memory here.
    monkeypatch.setattr(socket.socket, "connect", lambda *a: (_ for _ in ()).throw(AssertionError("network forbidden")))
    return root, runtime, workflow, runner, transport, principal, client, token, virtual, app


def begin(env):
    _, _, _, _, _, _, client, _, _, _ = env
    result = client.post("/documents/operator/sessions", json={"source_approval_id": "synthetic-1",
                                                             "request_key": "create-session-0001"})
    assert result.status_code == 201, result.text
    session = result.json()["session_id"]
    response = client.post(f"/documents/operator/sessions/{session}/start")
    assert response.status_code == 202, response.text
    return session, response.json()["job_id"]


def finish(env):
    _, _, _, runner, transport, _, client, _, clock, _ = env
    session, job = begin(env)
    for _ in range(12):
        clock[0] += 61
        runner.once()
        result = client.get(f"/documents/operator/sessions/{session}")
        assert result.status_code == 200, result.text
        if result.json().get("job_state") in {"COMPLETED", "FAILED", "PARTIAL", "CANCELLED"}:
            break
    assert result.json()["digest_status"] == "COMPLETE", result.text
    response = client.post(f"/documents/operator/sessions/{session}/publish", json={"expected_job_id": job})
    assert response.status_code == 200, response.text
    return session, job


@pytest.mark.parametrize("claims", [
    {"iss": "https://foreign.invalid"}, {"aud": "fixture-ui"}, {"tid": "foreign"},
    {"sub": "other"}, {"roles": ["unapproved"]}, {"token_use": "id"},
    {"exp": 1}, {"nbf": 2147483647}, {"sub": ""},
    {"idtyp": "app"}, {"roles": ["operator", "unapproved"]},
])
def test_operator_token_negatives_before_effects(operator_env, claims):
    _, _, _, _, transport, _, client, token, _, _ = operator_env
    client.headers["Authorization"] = "Bearer " + token(**claims)
    response = client.get("/documents/operator/context")
    assert response.status_code in {401, 403}
    assert response.json()["request_id"] == response.headers["x-request-id"]
    assert response.json()["category"]
    assert transport.attempts == 0


def test_complete_authorized_journey_and_bounded_replay(operator_env):
    _, runtime, workflow, _, transport, principal, client, _, clock, _ = operator_env
    session, job = finish(operator_env)
    prefix = f"/documents/operator/sessions/{session}"
    calls = transport.attempts
    for _ in range(3):
        assert client.get(prefix).status_code == 200
        assert client.post(prefix + "/start").json()["job_id"] == job
        assert client.post(prefix + "/publish", json={"expected_job_id": job}).status_code == 200
        packet = client.get(prefix + "/digest").json()
        assert packet["status"] == "COMPLETE" and packet["coverage"]["fraction"] == 1
        assert packet["evidence"] and packet["semantic_support"] == "not_evaluated"
    assert transport.attempts == calls == 3
    clock[0] += 61
    body = {"query": "What valve inspection is required?", "request_key": "question-key-0001"}
    answer = client.post(prefix + "/questions", json=body)
    assert answer.status_code == 200, answer.text
    answer = answer.json()
    assert answer["evidence_status"] == "available" and answer["citations"]
    assert answer["citations"][0]["document_id"] == str(workflow.pilot.sources["synthetic-1"].document_id)
    assert client.post(prefix + "/questions", json=body).json() == answer
    assert transport.attempts == 4
    projected = client.get(prefix).json()["usage"]
    assert projected["synthetic"] and projected["measured_input_tokens"] == 120
    assert projected["measured_output_tokens"] == 160 and projected["unsettled_reserved_tokens"] == 0
    assert client.post(prefix + "/questions", json={**body, "query": "conflicting replay"}).status_code == 409
    assert client.post("/documents/analyze", json={"query": "bypass"}).status_code == 503
    assert client.post("/query/stream", json={"query": "bypass"}).status_code == 403
    closure = client.post(prefix + "/close", json={"withdrawal": True})
    assert closure.status_code == 200 and closure.json()["retention"] == "PURGE_PENDING"
    assert any(r["class"] == "usage_reservations" for r in closure.json()["residuals"])
    assert not any(name in json.dumps(closure.json()) for name in ('"ticket"', '"provider_calls"', '"reference"'))
    assert client.get(prefix + "/digest").status_code == 403
    assert client.post(prefix + "/questions", json=body).status_code == 403
    usage = runtime.governance.usage(principal, runtime.authority)
    assert len(usage) == 4 and all(row["state"] == "SETTLED" for row in usage)
    assert transport.external_attempts == 0


def test_create_replay_and_strict_injection_rejection(operator_env):
    _, _, _, _, transport, _, client, _, _, _ = operator_env
    body = {"source_approval_id": "synthetic-1", "request_key": "create-session-0001"}
    first = client.post("/documents/operator/sessions", json=body)
    assert first.status_code == 201
    replay = client.post("/documents/operator/sessions", json=body)
    assert replay.status_code == 200 and first.json() == replay.json()
    assert client.post("/documents/operator/sessions", json={**body, "source_approval_id": "synthetic-2"}).status_code == 409
    for field in ("owner", "tenant", "path", "source_url", "provider", "budget", "role", "approval"):
        assert client.post("/documents/operator/sessions", json={**body, field: "injected"}).status_code == 422
    assert transport.attempts == 0


@pytest.mark.parametrize("control", ["cancel", "close", "withdraw", "stop"])
def test_queued_cancellation_and_stop_no_provider(operator_env, control):
    _, _, _, runner, transport, _, client, _, _, _ = operator_env
    session, _ = begin(operator_env)
    prefix = f"/documents/operator/sessions/{session}"
    if control == "stop":
        response = client.post("/documents/operator/stop")
    elif control in {"close", "withdraw"}:
        response = client.post(prefix + "/close", json={"withdrawal": control == "withdraw"})
    else:
        response = client.post(prefix + "/cancel")
    assert response.status_code in {200, 202}, response.text
    runner.once()
    assert transport.attempts == 0
    assert client.post(prefix + "/publish", json={"expected_job_id": "00000000-0000-0000-0000-000000000000"}).status_code != 200


@pytest.mark.parametrize("change", ["close", "stop", "tombstone", "permission", "expiry", "generation"])
def test_delayed_response_revalidates_actual_asgi_send(operator_env, change):
    _, runtime, workflow, _, _, p, _, _, clock, _ = operator_env
    session, _ = finish(operator_env)
    from api.security import ApplicationSecurityMiddleware
    from types import SimpleNamespace
    sent = []
    async def downstream(scope, receive, send):
        scope["state"]["release_guard"] = workflow.release_guard(p, UUID(session), active=True)
        if change == "close":
            workflow.pilot.close(p, UUID(session))
        elif change == "stop":
            workflow.pilot.stop(p)
        elif change == "tombstone":
            runtime.authority.tombstone(p, workflow.pilot.sources["synthetic-1"].document_id)
        elif change == "permission":
            with runtime.authority.transaction() as db:
                db.execute("UPDATE principals SET permissions='[]',epoch=epoch+1")
        elif change == "expiry":
            clock[0] = p.expires + 1
        else:
            with workflow.pilot.publication.authority.transaction() as db:
                db.execute("UPDATE active SET epoch=epoch+1")
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"PROTECTED_DIGEST"})
    runtime.verifier = SimpleNamespace(verify=lambda token: p)
    configuration = SimpleNamespace(authentication_mode="oidc_jwt", API_AUTH_ENABLED=False)
    async def receive():
        return {"type": "http.request", "body": b""}
    async def send(message):
        sent.append(message)
    asyncio.run(ApplicationSecurityMiddleware(downstream, configuration, lambda: runtime)(
        {"type": "http", "method": "GET", "path": "/documents/operator/context",
         "headers": [(b"authorization", b"Bearer fixture")]}, receive, send))
    assert sent[0]["status"] == 403
    assert b"PROTECTED_DIGEST" not in b"".join(m.get("body", b"") for m in sent)


def test_restart_requires_fresh_grant_and_preserves_durable_job(operator_env):
    root, _, workflow, runner, transport, p, _, _, _, _ = operator_env
    session, job = begin(operator_env)
    runtime2, workflow2, runner2, transport2 = build(root, fetch=lambda: {"keys": []})
    runner2.once()
    assert not runner2.grants and transport2.attempts == 0
    assert workflow2.status(p, UUID(session))["job_id"] == job
    runtime2.authority.register(p)
    assert workflow2.start(p, UUID(session))["job_id"] == job
    runner2.authorize(p, UUID(session))
    runner2.once()
    assert transport2.attempts == 0  # first step is deterministic plan validation


@pytest.mark.parametrize("missing", ["security.sqlite", "governance.sqlite", "pilot.sqlite", "actions.sqlite", "vectors.json"])
def test_reopen_missing_truth_never_initializes_allowance(operator_env, missing):
    root = operator_env[0]
    path = root / "private" / missing
    path.rename(path.with_suffix(".missing"))
    with pytest.raises(ValueError, match="authorities unavailable"):
        build(root)
    assert not path.exists()


@pytest.mark.parametrize("name", ["security.sqlite", "governance.sqlite", "admission.sqlite", "jobs.sqlite",
                                "publication.sqlite", "pilot.sqlite", "actions.sqlite"])
def test_truncated_authority_is_not_first_initialization(operator_env, name):
    root = operator_env[0]
    path = root / "private" / name
    path.write_bytes(b"")
    with pytest.raises(ValueError, match="authorities inconsistent"):
        build(root)
    assert path.stat().st_size == 0  # No constructor recreated security/budget truth.


def test_action_interruption_is_reconciliation_not_duplicate(operator_env):
    _, _, workflow, _, transport, p, _, _, _, _ = operator_env
    count = []
    def interrupted():
        count.append(1)
        raise RuntimeError("simulated interruption after effect")
    with pytest.raises(RuntimeError):
        workflow.actions.run(p.scope.identity(), "question", "key", {}, interrupted)
    with pytest.raises(PilotError, match="reconciliation"):
        workflow.actions.run(p.scope.identity(), "question", "key", {}, interrupted)
    assert count == [1] and transport.attempts == 0


def test_synthetic_pdf_catalog_and_intake(operator_env):
    _, _, workflow, _, transport, p, _, _, _, _ = operator_env
    result, _ = workflow.create(p, "synthetic-2", "pdf-session-key-0001")
    assert workflow.status(p, UUID(result["session_id"]))["source_id"] == "synthetic-manual/2"
    assert transport.attempts == 0


def test_malformed_fixture_response_never_complete(operator_env):
    _, _, _, runner, transport, _, client, _, clock, _ = operator_env
    session, _ = begin(operator_env)
    transport.post = lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("untrusted response"))
    for _ in range(8):
        clock[0] += 61
        runner.once()
    response = client.get(f"/documents/operator/sessions/{session}")
    assert response.status_code == 200
    assert response.json()["job_state"] == "FAILED"
    assert response.json()["digest_status"] == "FAILED"


def test_coherent_quiesced_restore_preserves_consumption_and_closure(operator_env, tmp_path):
    import shutil
    root, runtime, workflow, _, _, p, client, _, _, _ = operator_env
    session, _ = finish(operator_env)
    assert client.post(f"/documents/operator/sessions/{session}/close", json={"withdrawal": True}).status_code == 200
    before = runtime.governance.usage(p, runtime.authority)
    snapshot = tmp_path / "snapshot"
    shutil.copytree(root, snapshot)
    original = root.with_name("quiesced-original")
    root.rename(original)
    shutil.copytree(snapshot, root)
    runtime2, workflow2, runner2, transport2 = build(root, fetch=lambda: {"keys": []})
    assert runtime2.governance.usage(p, runtime2.authority) == before
    assert workflow2.status(p, UUID(session))["session_state"] == "WITHDRAWN"
    with pytest.raises(PilotError):
        workflow2.digest(p, UUID(session))
    assert not runner2.grants and transport2.attempts == 0
    with workflow2.pilot.control.transaction() as db:
        assert db.execute("SELECT COUNT(*) FROM sessions").fetchone()[0] == 1


def test_source_hash_refusal_before_document_or_provider(operator_env):
    _, runtime, workflow, _, transport, p, _, _, _, _ = operator_env
    workflow.catalog["synthetic-1"] = b"tampered bytes"
    with pytest.raises(Exception):
        workflow.create(p, "synthetic-1", "tampered-request-key-0001")
    assert transport.attempts == 0 and not runtime.governance.usage(p, runtime.authority)


def test_actual_body_limit_and_duplicate_authorization(operator_env):
    client = operator_env[6]
    assert client.post("/documents/operator/sessions", content=b"x" * 9000).status_code == 413
    credential = "Bearer " + operator_env[7]()
    assert client.get("/documents/operator/context", headers=[("Authorization", credential),
                      ("Authorization", credential)]).status_code == 401


def test_healthy_idle_readiness_and_no_inference_from_probes(operator_env):
    _, _, _, runner, transport, _, client, _, _, _ = operator_env
    runner.start()
    try:
        for _ in range(3):
            response = client.get("/ready")
            assert response.status_code == 200, response.text
            assert response.json()["publication"] == "idle"
            assert client.get("/health").status_code == 200
            assert client.get("/metrics").status_code == 200
        assert transport.attempts == 0
        assert client.post("/documents/operator/stop").status_code == 200
        assert client.get("/ready").status_code == 503
    finally:
        runner.close()


def test_concurrent_protected_http_sends_do_not_block_event_loop(operator_env):
    import httpx
    app = operator_env[9]
    credential = "Bearer " + operator_env[7]()
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://local") as client:
            results = await asyncio.wait_for(asyncio.gather(*[
                client.get("/documents/operator/context", headers={"Authorization": credential}) for _ in range(12)
            ]), timeout=15)
            assert all(r.status_code == 200 for r in results)
    asyncio.run(run())


def test_permission_in_empty_action_refused(operator_env):
    client = operator_env[6]
    assert client.post("/documents/operator/stop", json={"role": "admin"}).status_code == 422


def test_runner_reports_admission_wait_without_inference(operator_env):
    _, _, _, runner, transport, _, client, _, _, _ = operator_env
    session, _ = begin(operator_env)
    runner.admission_ready = lambda: False
    runner.once()
    assert runner.outcome == "WAITING_ADMISSION"
    response = client.get(f"/documents/operator/sessions/{session}")
    assert response.json()["worker"] == "WAITING_ADMISSION"
    assert transport.attempts == 0


def test_publication_replay_conflict_is_409_without_republication(operator_env):
    _, _, workflow, _, transport, _, client, _, _, _ = operator_env
    session, job = finish(operator_env)
    attempts = transport.attempts
    with workflow.pilot.publication.authority.transaction() as db:
        db.execute("UPDATE active SET generation=?,epoch=epoch+1", (str(uuid4()),))
    response = client.post(f"/documents/operator/sessions/{session}/publish", json={"expected_job_id": job})
    assert response.status_code == 409
    assert transport.attempts == attempts
