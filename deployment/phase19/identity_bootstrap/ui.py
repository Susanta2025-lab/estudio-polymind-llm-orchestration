"""Maintenance UI: native access token only; no API, authority, provider or claim display."""

import os

from deployment.phase19.identity_bootstrap.core import BootstrapVerifier, validate_auth
from deployment.phase19.identity_bootstrap.files import export


def render(st, verifier, destination):
    st.title("Local identity bootstrap")
    st.info(
        "Maintenance only. Identity evidence grants no enrollment or execution permission."
    )
    st.caption(
        "Use a dedicated private browser session. After logout, clear polymind.test site data, "
        "close every private tab, stop the launcher and remove temporary configuration."
    )
    try:
        validate_auth(st.secrets.to_dict())
    except Exception:
        st.error("Configuration unavailable. Stop and review private provisioning.")
        return
    if st.button("Log out and clear display"):
        st.session_state.clear()
        st.logout()
        return
    if not st.user.is_logged_in:
        st.session_state.clear()
        st.info("Ready for separately authorized sign-in.")
        if st.button("Sign in"):
            try:
                st.login()
            except Exception:
                st.error("Authentication unavailable. Stop and review configuration.")
        return
    try:
        token = st.user.tokens.get("access")
        principal = verifier.verify(token)
        # Status must not carry across an identity change in an existing tab.
        owner = str(principal.scope.owner)
        if st.session_state.get("owner") != owner:
            st.session_state.clear()
            st.session_state["owner"] = owner
        st.success("IDENTITY_VERIFICATION: PASS; CANONICAL_OWNER_DERIVATION: PASS")
        approved = st.checkbox(
            "I authorize protected enrollment-candidate export for this session."
        )
        if st.button("Export protected candidate", disabled=not approved):
            export(token, verifier, destination, authorized=approved)
            st.session_state["exported"] = True
        if st.session_state.get("exported"):
            st.success("PROTECTED_EVIDENCE_EXPORT: PASS; EXECUTION_AUTHORIZED: NO")
            st.info("Log out, complete browser cleanup and stop the launcher now.")
    except Exception:
        st.session_state.clear()
        st.error(
            "Verification or export unavailable, expired, or already completed. "
            "Log out; reconcile private evidence before retrying."
        )


if __name__ == "__main__":
    import streamlit as st

    st.set_page_config(page_title="PolyMind identity maintenance")

    @st.cache_resource
    def verifier():
        return BootstrapVerifier()

    render(st, verifier(), os.environ["POLYMIND_BOOTSTRAP_EVIDENCE"])
