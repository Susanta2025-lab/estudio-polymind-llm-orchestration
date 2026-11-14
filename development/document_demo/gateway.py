"""Local TLS boundary for native Streamlit, including WebSocket origin checks."""
import asyncio
import ssl

from aiohttp import ClientError, ClientSession, ClientTimeout, WSMsgType, web


def gateway(backend, origin):
    @web.middleware
    async def sanitized(request, handler):
        try:
            return await handler(request)
        except (ClientError, asyncio.TimeoutError):
            return web.Response(status=503, text="Local UI unavailable.", headers={"Cache-Control": "no-store"})
    app = web.Application(client_max_size=1_048_576, middlewares=[sanitized])

    async def session(app):
        app["client"] = ClientSession(trust_env=False, timeout=ClientTimeout(total=65, connect=3))
        yield
        await app["client"].close()
    app.cleanup_ctx.append(session)

    async def proxy(request):
        if request.host != origin.removeprefix("https://"):
            raise web.HTTPForbidden()
        supplied = request.headers.get("Origin")
        if supplied and supplied != origin:
            raise web.HTTPForbidden()
        if (request.path.startswith("/auth/") and request.headers.get("Sec-Fetch-Site") == "cross-site"):
            raise web.HTTPForbidden()
        headers = {k: v for k, v in request.headers.items()
                   if k.lower() not in {"host", "connection", "upgrade", "content-length", "transfer-encoding"}}
        headers["Host"] = request.host
        headers["X-Forwarded-Proto"] = "https"
        client = request.app["client"]
        if request.headers.get("Upgrade", "").lower() == "websocket":
            if supplied != origin:
                raise web.HTTPForbidden()
            protocols = request.headers.get("Sec-WebSocket-Protocol", "").split(", ")
            async with client.ws_connect(backend + request.path_qs, headers=headers, protocols=protocols) as upstream:
                downstream = web.WebSocketResponse(protocols=protocols)
                await downstream.prepare(request)

                async def forward(source, target):
                    async for msg in source:
                        if msg.type == WSMsgType.TEXT:
                            await target.send_str(msg.data)
                        elif msg.type == WSMsgType.BINARY:
                            await target.send_bytes(msg.data)
                        else:
                            break
                    await target.close()
                await asyncio.gather(forward(upstream, downstream), forward(downstream, upstream))
                return downstream
        async with client.request(request.method, backend + request.path_qs, headers=headers,
                                  data=await request.read(), allow_redirects=False) as upstream:
            response = web.Response(status=upstream.status, body=await upstream.read())
            for key, value in upstream.headers.items():
                if key.lower() == "set-cookie":
                    response.headers.add(key, value + ("; Secure" if "; secure" not in value.lower() else ""))
                elif key.lower() not in {"content-length", "transfer-encoding", "connection", "content-encoding"}:
                    response.headers.add(key, value)
            response.headers["Cache-Control"] = "no-store"
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["Referrer-Policy"] = "no-referrer"
            return response
    app.router.add_route("*", "/{path:.*}", proxy)
    return app


def serve(root, backend="http://127.0.0.1:8501", port=9443, host="127.0.0.1"):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(root / "tls.crt", root / "tls.key")
    web.run_app(gateway(backend, f"https://localhost:{port}"), host=host, port=port,
                ssl_context=context, access_log=None)
