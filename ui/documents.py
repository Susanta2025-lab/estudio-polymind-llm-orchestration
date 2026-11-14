"""Inert, server-authorized Documents view; protected packets live for one rerun."""
from uuid import uuid4
from hashlib import sha256

import streamlit as st

from ui.documents_client import DocumentClientError, DocumentsClient


def clear_display():
    for key in list(st.session_state):
        if key.startswith("doc_"):
            del st.session_state[key]


def key(name):
    return st.session_state.setdefault("doc_key_" + name, uuid4().hex)


def render(api_url):
    st.title("Documents")
    st.info("Private synthetic operator verification. No paid inference. No real participant consent.")
    if not st.user.is_logged_in:
        clear_display()
        if st.button("Log in", key="documents_login"):
            st.login()
        st.stop()
    token = st.user.tokens.get("access")
    if not token:
        clear_display()
        st.error("API access token unavailable. Log out and authenticate again.")
        if st.button("Log out"):
            st.logout()
        st.stop()
    client = DocumentsClient(api_url, token)
    if st.button("Log out"):
        try:
            if st.session_state.get("doc_session"):
                client.call("POST", "/sessions/" + st.session_state.doc_session + "/close", {"withdrawal": False})
        except DocumentClientError:
            pass
        clear_display()
        st.logout()
    if st.button("Clear frontend display"):
        clear_display()
        st.rerun()
    if st.button("Operator emergency stop"):
        try:
            st.json(client.call("POST", "/stop"))
        except DocumentClientError as exc:
            st.error(str(exc))
        clear_display()
        st.stop()
    try:
        context = client.call("GET", "/context")
        scope = (context["owner_id"], context["tenant_id"])
        if st.session_state.get("doc_scope") != scope:
            clear_display()
            st.session_state.doc_scope = scope
        st.success("Verified enrolled operator")
        st.json(context)
        sources = client.call("GET", "/sources")
        chosen = st.selectbox("Approved synthetic source", sources,
                              format_func=lambda s: s["name"] + " — " + s["classification"])
        st.json(chosen)
        if st.button("Create session", disabled=not chosen["eligible"]):
            result = client.call("POST", "/sessions", {"source_approval_id": chosen["source_approval_id"],
                                 "request_key": key("create_" + chosen["source_approval_id"])})
            st.session_state.doc_session = result["session_id"]
        # Recovery accepts an opaque session identity only. Server checks scope.
        with st.form("recover_document_session"):
            recover = st.text_input("Existing session ID")
            if st.form_submit_button("Reconnect") and recover:
                from uuid import UUID
                st.session_state.doc_session = str(UUID(recover))
        session = st.session_state.get("doc_session")
        if session:
            st.text("Session " + session)
            prefix = "/sessions/" + session
            if st.button("Start durable job"):
                client.call("POST", prefix + "/start")
            if st.button("Cancel processing"):
                st.json(client.call("POST", prefix + "/cancel"))
            if st.button("Close session"):
                st.json(client.call("POST", prefix + "/close", {"withdrawal": False}))
                st.stop()
            if st.button("Withdraw session"):
                st.json(client.call("POST", prefix + "/close", {"withdrawal": True}))
                st.stop()
            _session_panel(api_url, token, session)
        st.caption("Clear display and logout do not erase retained objects, audit, usage or backups. Withdrawal may leave PURGE_PENDING.")
    except (DocumentClientError, ValueError) as exc:
        # Exception strings from this adapter are fixed categories, never upstream bodies.
        st.error(str(exc) if isinstance(exc, DocumentClientError) else "Invalid session ID.")


@st.fragment(run_every="3s")
def _session_panel(api_url, token, session):
    client = DocumentsClient(api_url, token)
    prefix = "/sessions/" + session
    try:
        # Every protected rerender uses the current server, even for completed jobs.
        client.call("GET", "/context")
        status = client.call("GET", prefix)
        st.subheader("Processing status")
        st.json(status)
        if status.get("digest_status") == "COMPLETE" and status["session_state"] == "OPEN":
            if st.button("Authorize publication"):
                client.call("POST", prefix + "/publish", {"expected_job_id": status["job_id"]})
                status = client.call("GET", prefix)
        if status.get("generation") and status["session_state"] == "OPEN":
            packet = client.call("GET", prefix + "/digest")
            st.subheader("Complete document digest")
            st.caption("Structural provenance verified; semantic support not evaluated.")
            # st.json is inert; it cannot fetch links or execute source/model HTML.
            st.json(packet)
            with st.form("document_question"):
                question = st.text_input("Question about the selected document", max_chars=4096)
                if st.form_submit_button("Ask bounded question"):
                    answer = client.call("POST", prefix + "/questions", {"query": question,
                                         "request_key": key("question_" + sha256(question.encode()).hexdigest())})
                    st.json(answer)
    except DocumentClientError as exc:
        st.error(str(exc))
