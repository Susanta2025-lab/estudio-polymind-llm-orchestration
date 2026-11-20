"""Private native-OIDC Chat; every display and execution is server authorized."""
from uuid import uuid4
import requests
import streamlit as st

from ui.api_client import stream_query, APIStreamError


def clear():
    for key in list(st.session_state):
        if key.startswith('secure_chat_'):
            del st.session_state[key]


def render(api_url):
    st.title('Chat')
    if not st.user.is_logged_in:
        clear()
        if st.button('Log in', key='chat_login'):
            st.login()
        st.stop()
    token = st.user.tokens.get('access')
    if not token:
        clear()
        st.warning('API access token unavailable. Reauthenticate.')
        if st.button('Reauthenticate', key='chat_reauthenticate'):
            st.logout()
        st.stop()
    placeholder = None
    try:
        response = requests.get(api_url + '/chat/context', headers={'Authorization':'Bearer ' + token},
                                timeout=(3,5), allow_redirects=False)
        try:
            if response.status_code != 200:
                raise APIStreamError('Chat authorization unavailable.')
            context = response.json()
        finally:
            response.close()
        scope = (context['owner_id'], context['tenant_id'], token)
        if st.session_state.get('secure_chat_scope') != scope:
            clear()
            st.session_state.secure_chat_scope = scope
        session = st.selectbox('Authorized conversation', context['sessions'])
        if st.button('Log out', key='chat_logout'):
            clear(); st.logout(); st.stop()
        # Reauthorized backend reads prevent expired/revoked or foreign history display.
        history = requests.get(api_url + '/memory/' + requests.utils.quote(session, safe=''),
            headers={'Authorization':'Bearer ' + token}, timeout=(3,5), allow_redirects=False)
        try:
            if history.status_code != 200:
                raise APIStreamError('Conversation authorization unavailable.')
            messages = history.json()['history']
        finally:
            history.close()
        for message in messages:
            with st.chat_message(message['role']):
                st.markdown(message['content'])
        prompt = st.chat_input('Ask within your authorized scope', disabled=not context.get('execution_enabled', False))
        if prompt:
            # Explicit submit creates one intent; refresh never resubmits inference.
            request_key = uuid4().hex
            with st.chat_message('assistant'):
                placeholder = st.empty(); answer = ''
                for event in stream_query(api_url + '/query/stream', prompt, session, 70,
                        access_token=token, request_key=request_key):
                    if event['type'] == 'metadata' and event.get('sources'):
                        st.json({'sources':event['sources']})
                    if event['type'] == 'chunk':
                        answer += event['content']; placeholder.markdown(answer)
                    elif event['type'] == 'error':
                        raise APIStreamError(event.get('message', 'Chat unavailable.'))
    except (requests.RequestException, ValueError, KeyError, APIStreamError):
        if placeholder is not None:
            placeholder.empty()
        clear()
        st.error('Chat unavailable or authorization expired. Reauthenticate without repeating uncertain requests.')
