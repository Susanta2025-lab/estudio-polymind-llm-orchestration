"""Authenticated Chat HTTP contracts; the service is explicitly composed."""
import json
from queue import Queue, Empty, Full
from threading import Thread, Event

from fastapi import Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from security.chat import ChatMemory
from security.models import SecurityError


class ChatRequest(BaseModel):
    query: str
    session_id: str = Field(default='default', min_length=1, max_length=256)
    request_key: str | None = None


def context(request, body):
    if request is None:
        raise SecurityError("unsupported_execution")
    service = getattr(request.app.state, 'authorized_chat', None)
    principal = getattr(request.state, 'principal', None)
    if service is None or principal is None or service.runtime is not request.app.state.security_runtime:
        raise SecurityError('unsupported_execution')
    if not 1 <= len(body.query) <= 4096:
        raise SecurityError()
    ctx = service.context(principal, body.session_id)
    request.state.release_guard = ctx.release
    return service, ctx


def query_response(body, request):
    service, ctx = context(request, body)
    return service.run(ctx, body.query, body.request_key)


def stream_response(body, request):
    service, ctx = context(request, body)
    if type(body.request_key) is not str or not 16 <= len(body.request_key) <= 128:
        raise SecurityError()
    def events():
        queue, stopped = Queue(maxsize=32), Event()
        def emit(event):
            if stopped.is_set():
                raise SecurityError()
            try:
                queue.put(event, timeout=3)
            except Full:
                raise SecurityError('security_unavailable') from None
        def run():
            try:
                service.run(ctx, body.query, body.request_key, stream=True, emit=emit)
            except Exception:
                if not stopped.is_set():
                    try:
                        emit({'type':'error', 'message':'Request processing failed.'})
                    except SecurityError:
                        pass
            finally:
                stopped.set()
        worker = Thread(target=run, name='authorized-chat-request', daemon=True)
        worker.start()
        try:
            while not stopped.is_set() or not queue.empty():
                try:
                    event = queue.get(timeout=0.05)
                    ctx.check()
                    yield json.dumps(event, ensure_ascii=False) + '\n'
                except Empty:
                    pass
        finally:
            stopped.set()
            worker.join(timeout=service.policy.total_seconds + 8)
    return StreamingResponse(events(), media_type='application/x-ndjson', headers={'Cache-Control':'no-store'})


def add_chat_routes(app):
    @app.get('/chat/context')
    def inspect(request: Request):
        service = request.app.state.authorized_chat
        if service is None:
            raise SecurityError('unsupported_execution')
        _, ctx = context(request, ChatRequest(query='context', session_id=service.policy.sessions[0]))
        return {'owner_id':str(ctx.principal.scope.owner), 'tenant_id':str(ctx.principal.scope.tenant),
                'sessions':list(service.policy.sessions), 'execution_enabled':service.permissions.remaining(
                    service.permissions.check(ctx.principal, service.policy.permission_id, 'chat', ctx.resource)) > 0,
                'expires':ctx.principal.expires}

    @app.post('/query')
    def query(body: ChatRequest, request: Request):
        return query_response(body, request)

    @app.post('/query/stream')
    def stream(body: ChatRequest, request: Request):
        return stream_response(body, request)

    @app.get('/memory/{session_id}')
    def history(session_id: str, request: Request):
        body = ChatRequest(query='memory', session_id=session_id)
        _, ctx = context(request, body)
        return {'session_id':session_id, 'history':ChatMemory(ctx).get_history(session_id)}

    @app.delete('/memory/{session_id}')
    def clear(session_id: str, request: Request):
        body = ChatRequest(query='memory', session_id=session_id)
        _, ctx = context(request, body)
        ChatMemory(ctx).clear_session(session_id)
        return {'session_id':session_id, 'status':'deleted'}
