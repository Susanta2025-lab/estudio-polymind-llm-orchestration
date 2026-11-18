"""Inert, server-authorized Documents view; protected packets live for one rerun."""
from uuid import UUID, uuid4
from hashlib import sha256

import streamlit as st

from ui.documents_client import DocumentClientError, DocumentsClient


def clear_display(*, preserve_reconnect=False):
    if not preserve_reconnect:
        st.query_params.pop("document_session", None)
    for key in list(st.session_state):
        if key.startswith("doc_"):
            del st.session_state[key]


def key(name):
    return st.session_state.setdefault("doc_key_" + name, uuid4().hex)


def access_error(exc):
    # A full rerun removes protected elements outside the polling fragment too.
    st.session_state.doc_access_error = (exc.status_code, str(exc))
    st.rerun(scope="app")


def reauthenticate():
    st.warning("Your login token expired or is unavailable/invalid. The document session may still be open. "
               "Reauthentication does not extend approvals, execution deadlines or budgets.")
    session = st.session_state.get("doc_session")
    if not session:
        try:
            session = str(UUID(st.query_params.get("document_session", "")))
        except ValueError:
            session = None
    if session:
        st.text("Record this session ID privately before continuing: " + session)
    st.info("Select Reauthenticate to clear the native login, then Log in and reconnect using Existing session ID.")
    if st.button("Reauthenticate"):
        clear_display()
        # Native logout only: deliberately bypass the explicit Log out closure.
        st.logout()
        st.stop()


def render(api_url):
    st.title("Documents")
    st.info("Private synthetic operator verification. No paid inference. No real participant consent.")
    if not st.user.is_logged_in:
        clear_display()
        if st.button("Log in", key="documents_login"):
            st.login()
        st.stop()
    token = st.user.tokens.get("access")
    failure = st.session_state.get("doc_access_error")
    if not token or (failure and failure[0] == 401):
        reauthenticate()
        st.stop()
    if failure:
        st.error(failure[1])
        if st.button("Retry authorization"):
            del st.session_state["doc_access_error"]
            st.rerun()
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
        st.stop()
    if st.button("Clear frontend display"):
        clear_display()
        st.rerun()
    if st.button("Operator emergency stop"):
        try:
            st.json(client.call("POST", "/stop"))
        except DocumentClientError as exc:
            access_error(exc)
        clear_display()
        st.stop()
    try:
        context = client.call("GET", "/context")
        scope = (context["owner_id"], context["tenant_id"])
        if st.session_state.get("doc_scope") != scope:
            # A fresh page may carry an opaque reconnect hint, never authority.
            clear_display(preserve_reconnect=st.session_state.get("doc_scope") is None)
            st.session_state.doc_scope = scope
        if not st.session_state.get("doc_session") and st.query_params.get("document_session"):
            st.session_state.doc_session = str(UUID(st.query_params["document_session"]))
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
                st.session_state.doc_session = str(UUID(recover))
        session = st.session_state.get("doc_session")
        if session:
            # UUID only. Server status/digest calls reauthorize every display.
            st.query_params["document_session"] = session
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
        if isinstance(exc, DocumentClientError):
            access_error(exc)
        st.error("Invalid session ID.")


@st.fragment(run_every="3s")
def _session_panel(api_url, token, session):
    if not st.user.is_logged_in:
        clear_display()
        st.rerun(scope="app")
    if st.user.tokens.get("access") != token:
        access_error(DocumentClientError("Login changed. Authenticate again.", status_code=401))
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
            with st.form("document_question"):
                question = st.text_input("Question about the selected document", max_chars=4096)
                if st.form_submit_button("Ask bounded question"):
                    client.call("POST", prefix + "/questions", {"query": question,
                                "request_key": key("question_" + sha256(question.encode()).hexdigest())})
                    # Display only a new authorized read, never the POST response.
                    packet = client.call("GET", prefix + "/digest")
            if (packet.get("generation") != status["generation"] or
                    any(a.get("generation") != packet["generation"] for a in packet.get("answers", []))):
                raise DocumentClientError("Publication generation changed. Reconnect to revalidate.")
            st.subheader("Complete document digest")
            st.caption("Structural provenance verified; semantic support not evaluated.")
            # Inert JSON preserves canonical citations without executing links/HTML.
            st.json({k: v for k, v in packet.items() if k != "answers"})
            st.subheader("Saved Questions and Answers")
            st.caption("Accepted answers from the current authorized digest. Structural provenance does not certify semantic support.")
            for answer in packet.get("answers", []):
                # Preserve answer text, source/citation provenance, evidence status,
                # semantic_support and limitations exactly as delivered by server.
                st.json(answer)
            if not packet.get("answers"):
                st.info("No accepted answers yet.")
    except DocumentClientError as exc:
        access_error(exc)
