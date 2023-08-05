"""
This is ruteni's toplevel application.

This application simply splits incoming requests into web (http or websocket) and
lifespan events, and route them to their respective handler.  The web handler will
process both http and websocket scopes, while the lifespan handler is simply an
asynchronous context manager whose enter/exit callbacks will be invoked when the
application starts up and shuts down respectively.

.. highlight:: python
.. code-block:: python
    # demo.py
    from ruteni.core.app import Application
    from asgiref.typing import (
        ASGIReceiveCallable,
        ASGISendCallable,
        WWWScope,
        HTTPResponseStartEvent,
        HTTPResponseBodyEvent,
    )

    async def http(
        scope: HTTPScope, receive: ASGIReceiveCallable, send: ASGISendCallable
    ) -> None:
        assert scope["type"] == "http"
        await send(
            HTTPResponseStartEvent(
                {
                    "type": "http.response.start",
                    "status": 200,
                    "headers": [(b"content-type", b"text/plain")],
                }
            )
        )
        await send(
            HTTPResponseBodyEvent(
                {
                    "type": "http.response.body",
                    "body": b"Hello, world!",
                    "more_body": False
                }
            )
        )

    async def websocket(
        scope: WebSocketScope, receive: ASGIReceiveCallable, send: ASGISendCallable
    ) -> None:
        assert scope["type"] == "websocket"
        raise NotImplementedError()

    class ContextManager:
        async def __aenter__(self) -> None:
            print("startup")

        async def __aexit__(self, *exc_info: object) -> None:
            print("shutdown")


    lifespan = Lifespan(ContextManager())
    app = Application(http, websocket, lifespan)

Run with:

> uvicorn demo:app

then visit `http://localhost:8000`
"""
from typing import cast

from asgiref.typing import (
    ASGIReceiveCallable,
    ASGISendCallable,
    HTTPScope,
    LifespanScope,
    Scope,
    WebSocketScope,
)

from .types import (
    HTTPApp,
    HTTPReceive,
    HTTPSend,
    LifespanApp,
    LifespanReceive,
    LifespanSend,
    WebSocketApp,
    WebSocketReceive,
    WebSocketSend,
)


class Application:
    """Toplevel ASGI app that demultiplexes http/websocket/lifespan streams."""

    def __init__(
        self, http: HTTPApp, websocket: WebSocketApp, lifespan: LifespanApp
    ) -> None:
        """Create an application instance.

        :param http: the app that will manage http requests
        :param websocket: the app that will manage websocket sessions
        :param lifespan: the app that will manage the lifespan session
        """
        self.http = http
        self.websocket = websocket
        self.lifespan = lifespan

    async def __call__(
        self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable
    ) -> None:
        """Process a request by routing it to the appropriate handler."""
        if scope["type"] == "http":
            await self.http(
                cast(HTTPScope, scope), cast(HTTPReceive, receive), cast(HTTPSend, send)
            )
        elif scope["type"] == "websocket":
            await self.websocket(
                cast(WebSocketScope, scope),
                cast(WebSocketReceive, receive),
                cast(WebSocketSend, send),
            )
        else:
            assert scope["type"] == "lifespan"
            await self.lifespan(
                cast(LifespanScope, scope),
                cast(LifespanReceive, receive),
                cast(LifespanSend, send),
            )
