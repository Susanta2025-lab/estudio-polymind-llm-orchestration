"""Streamlit ScriptRunner regressions; protected packets are server-read only."""
from copy import deepcopy
from types import SimpleNamespace
from uuid import uuid4

import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

from ui import documents_view as view
from ui.documents_client import DocumentClientError


@pytest.fixture
def frontend(monkeypatch):
    session = str(uuid4())
    state = SimpleNamespace(calls=[], answers=[], failure=None, closed=False, generation="generation-1", logouts=[])
    class Client:
        def __init__(self, *args):
            pass
        def call(self, method, path, body=None):
            state.calls.append((method, path, body))
            if state.failure:
                raise DocumentClientError("Login expired." if state.failure == 401 else "Access denied.", status_code=state.failure)
            if path == "/context":
                return dict(owner_id="owner", tenant_id="tenant")
            if path == "/sources":
                return [dict(name="manual", classification="synthetic", eligible=True, source_approval_id="source")]
            if path.endswith("/close"):
                state.closed = True
                return dict(retention="PURGE_PENDING")
            if path.endswith("/questions"):
                answer = dict(answer="Accepted answer " + str(len(state.answers) + 1), answer_id=str(uuid4()),
                              generation="generation-1", evidence_status="available", semantic_support="not_evaluated",
                              citations=[dict(document_id="canonical-source", excerpt="Valve inspection")], limitations=["Synthetic only"])
                state.answers.append(answer)
                return {"untrusted_post_only": True}
            if path.endswith("/digest"):
                return dict(generation=state.generation, answers=deepcopy(state.answers), executive_summary="protected digest")
            return dict(session_state="CLOSED" if state.closed else "OPEN", generation="generation-1", digest_status="COMPLETE", job_id="job")
    monkeypatch.setattr(view, "DocumentsClient", Client)
    monkeypatch.setattr(st, "user", SimpleNamespace(is_logged_in=True, tokens={"access": "synthetic"}))
    monkeypatch.setattr(st, "logout", lambda: state.logouts.append(True))
    app = AppTest.from_string("from ui.documents_view import render\nrender('http://synthetic')")
    app.session_state.doc_scope = ("owner", "tenant")
    app.session_state.doc_session = session
    app.run()
    assert not app.exception
    return app, state, session


def click(app, label):
    next(b for b in app.button if b.label == label).click().run()
    assert not app.exception


def packets(app):
    return " ".join(j.value for j in app.json)


def test_saved_answers_submit_rerun_and_new_page_reconnect(frontend):
    app, state, session = frontend
    for i in range(2):
        next(t for t in app.text_input if t.label.startswith("Question about")).set_value("Question " + str(i))
        click(app, "Ask bounded question")
        assert "Accepted answer " + str(i + 1) in packets(app)
    keys = [c[2]["request_key"] for c in state.calls if c[0] == "POST"]
    for _ in range(3):
        app.run()
        assert "Accepted answer 1" in packets(app) and "Accepted answer 2" in packets(app)
        assert "canonical-source" in packets(app) and "not_evaluated" in packets(app) and "Synthetic only" in packets(app)
        assert "untrusted_post_only" not in packets(app)
    assert [c[2]["request_key"] for c in state.calls if c[0] == "POST"] == keys
    fresh = AppTest.from_string("from ui.documents_view import render\nrender('http://synthetic')")
    fresh.query_params["document_session"] = session
    fresh.run()
    assert not fresh.exception
    assert "Accepted answer 2" in packets(fresh)
    assert len([c for c in state.calls if c[0] == "POST"]) == 2


@pytest.mark.parametrize("failure", [401, 403, 409])
def test_access_loss_removes_protected_content_and_blocks_calls(frontend, failure):
    app, state, session = frontend
    click(app, "Ask bounded question")
    state.failure = failure
    app.run()
    assert "Accepted answer" not in packets(app) and "protected digest" not in packets(app)
    calls = len(state.calls)
    app.run()
    assert len(state.calls) == calls
    if failure == 401:
        assert "token expired" in app.warning[0].value
        assert session in " ".join(t.value for t in app.text)
        click(app, "Reauthenticate")
        assert state.logouts == [True] and not state.closed
        assert "document_session" not in app.query_params
        assert len(state.calls) == calls
        # Native redirect starts a new frontend session; manual server recovery.
        state.failure = None
        recovered = AppTest.from_string("from ui.documents_view import render\nrender('http://synthetic')").run()
        next(t for t in recovered.text_input if t.label == "Existing session ID").set_value(session)
        click(recovered, "Reconnect")
        assert "Accepted answer" in packets(recovered)
        assert [c[1] for c in state.calls if c[0] == "POST"] == ["/sessions/" + session + "/questions"]


@pytest.mark.parametrize("change", ["closed", "generation", "answer_generation"])
def test_inactive_or_mismatched_packets_never_display(frontend, change):
    app, state, _ = frontend
    click(app, "Ask bounded question")
    if change == "closed":
        state.closed = True
    elif change == "generation":
        state.generation = "foreign"
    else:
        state.answers[0]["generation"] = "foreign"
    app.run()
    assert "Accepted answer" not in packets(app)


@pytest.mark.parametrize("action", ["Log out", "Close session", "Withdraw session"])
def test_explicit_closure_semantics(frontend, action):
    app, state, _ = frontend
    click(app, "Ask bounded question")
    click(app, action)
    assert "Accepted answer" not in packets(app)
    assert state.closed
    closure = next(c for c in state.calls if c[1].endswith("/close"))
    assert closure[2] == {"withdrawal": action == "Withdraw session"}
    assert bool(state.logouts) == (action == "Log out")


def test_missing_token_never_calls_api(frontend, monkeypatch):
    app, state, _ = frontend
    click(app, "Ask bounded question")
    calls = len(state.calls)
    monkeypatch.setattr(st, "user", SimpleNamespace(is_logged_in=True, tokens={}))
    app.run()
    assert len(state.calls) == calls
    assert "Accepted answer" not in packets(app)
    click(app, "Reauthenticate")
    assert len(state.calls) == calls and not state.closed


def test_logged_out_identity_clears_protected_display(frontend, monkeypatch):
    app, state, _ = frontend
    click(app, "Ask bounded question")
    calls = len(state.calls)
    monkeypatch.setattr(st, "user", SimpleNamespace(is_logged_in=False))
    app.run()
    assert len(state.calls) == calls
    assert "Accepted answer" not in packets(app)
    assert "doc_session" not in app.session_state


def test_refresh_hint_has_no_authority_and_contains_only_session_id(frontend):
    app, state, session = frontend
    assert app.query_params == {"document_session": [session]}
    state.failure = 403
    fresh = AppTest.from_string("from ui.documents_view import render\nrender('http://synthetic')")
    fresh.query_params["document_session"] = session
    fresh.run()
    assert not fresh.exception and "protected digest" not in packets(fresh)
    assert not any(c[0] == "POST" for c in state.calls)


def test_invalid_refresh_hint_cannot_select_arbitrary_api_path(frontend):
    _, state, _ = frontend
    state.calls.clear()
    fresh = AppTest.from_string("from ui.documents_view import render\nrender('http://synthetic')")
    fresh.query_params["document_session"] = "../foreign"
    fresh.run()
    assert not fresh.exception
    assert fresh.error[0].value == "Invalid session ID."
    assert all("/sessions" not in c[1] for c in state.calls)


def test_clear_display_removes_refresh_hint_and_answers(frontend):
    app, _, _ = frontend
    click(app, "Ask bounded question")
    click(app, "Clear frontend display")
    assert "document_session" not in app.query_params
    assert "Accepted answer" not in packets(app)


def test_expired_login_on_refresh_communicates_uuid_hint(frontend):
    _, state, session = frontend
    state.failure = 401
    fresh = AppTest.from_string("from ui.documents_view import render\nrender('http://synthetic')")
    fresh.query_params["document_session"] = session
    fresh.run()
    assert not fresh.exception
    assert session in " ".join(t.value for t in fresh.text)
    assert "protected digest" not in packets(fresh)
    click(fresh, "Reauthenticate")
    assert "document_session" not in fresh.query_params and not state.closed
