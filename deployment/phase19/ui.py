"""Private native-OIDC application planes; no fixture identity fallback."""
import streamlit as st

st.set_page_config(page_title='PolyMind', layout='wide')
if st.sidebar.radio('Application', ('Documents', 'Chat')) == 'Documents':
    from ui.documents_view import render
    render('http://api:8001', synthetic=False)
else:
    from ui.chat_view import render
    render('http://api:8001')
