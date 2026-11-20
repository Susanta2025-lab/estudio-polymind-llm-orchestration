"""Native-token forwarding and refresh behavior without browser/OIDC network."""
from types import SimpleNamespace

import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest
from ui import chat_view


@pytest.fixture
def frontend(monkeypatch):
    state=SimpleNamespace(gets=[],posts=[],status=200,token='offline-access-token')
    monkeypatch.setattr(st,'user',SimpleNamespace(is_logged_in=True,tokens={'access':state.token}))
    def get(url,**options):
        state.gets.append((url,options))
        value={'owner_id':'owner','tenant_id':'tenant','sessions':['private'],'execution_enabled':True}
        if '/memory/' in url:value={'history':[{'role':'assistant','content':'Previously accepted private answer'}]}
        return SimpleNamespace(status_code=state.status,json=lambda:value,close=lambda:None)
    monkeypatch.setattr(chat_view.requests,'get',get)
    def stream(*args,**kwargs):
        state.posts.append((args,kwargs))
        yield {'type':'chunk','content':'New authorized answer'}
        yield {'type':'done','response':'New authorized answer'}
    monkeypatch.setattr(chat_view,'stream_query',stream)
    app=AppTest.from_string("from ui.chat_view import render\nrender('http://api:8001')").run()
    assert not app.exception
    return app,state


def test_native_access_token_forwarded_once_and_refresh_is_read_only(frontend):
    app,state=frontend
    app.chat_input[0].set_value('hello').run()
    assert not app.exception and len(state.posts)==1
    kwargs=state.posts[0][1]
    assert kwargs['access_token']==state.token and len(kwargs['request_key'])==32
    for _ in range(3):app.run()
    assert len(state.posts)==1
    assert all(options['headers']=={'Authorization':'Bearer '+state.token} and options['allow_redirects'] is False
               for _,options in state.gets)


def test_expired_authority_hides_history_and_never_submits(frontend):
    app,state=frontend;state.status=403
    app.run()
    assert not app.exception
    assert 'Previously accepted' not in ' '.join(m.value for m in app.markdown)
    assert state.posts==[] and app.error


def test_missing_access_token_never_contacts_api(frontend,monkeypatch):
    app,state=frontend;before=len(state.gets)
    monkeypatch.setattr(st,'user',SimpleNamespace(is_logged_in=True,tokens={}))
    app.run()
    assert not app.exception and len(state.gets)==before and state.posts==[]
    assert 'Previously accepted' not in ' '.join(m.value for m in app.markdown)


def test_uncertain_partial_answer_is_removed_and_not_replayed(frontend,monkeypatch):
    from ui.api_client import APIStreamError
    app,state=frontend
    calls=[]
    def fail(*args,**kwargs):
        calls.append(True)
        yield {'type':'chunk','content':'Unaccepted partial output'}
        raise APIStreamError('Unknown outcome')
    monkeypatch.setattr(chat_view,'stream_query',fail)
    app.chat_input[0].set_value('hello').run()
    assert not app.exception and len(calls)==1 and app.error
    assert 'Unaccepted partial output' not in ' '.join(m.value for m in app.markdown)
    app.run();assert len(calls)==1
