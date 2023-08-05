from typing import Generic, Optional

from asgiref.typing import HTTPScope, WebSocketCloseEvent, WebSocketScope
from ruteni.core.types import (
    HTTPReceive,
    HTTPSend,
    HTTPSendEvent,
    WebSocketReceive,
    WebSocketSend,
)
from ruteni.responses import (
    HTTP_404_NOT_FOUND_RESPONSE,
    HTTP_500_INTERNAL_SERVER_ERROR_RESPONSE,
)
from ruteni.routing.types import Node, Route, TScope


class BaseRouter(Generic[TScope]):
    def __init__(self, node: Node) -> None:
        self.node = node


class Responder:
    def __init__(self, _send: HTTPSend) -> None:
        self._send = _send
        self.state: Optional[str] = None

    async def send(self, event: HTTPSendEvent) -> None:
        self.state = event["type"]
        await self._send(event)


class HTTPNodeRouter(BaseRouter[HTTPScope]):
    async def __call__(
        self, scope: HTTPScope, receive: HTTPReceive, send: HTTPSend
    ) -> None:
        responder = Responder(send)
        try:
            route: Route = [(scope["path"], None)]
            response = await self.node(scope, route)
            if response is not None:
                await response(scope, receive, responder.send)
            else:
                await HTTP_404_NOT_FOUND_RESPONSE(scope, receive, responder.send)
        except Exception as exc:
            if responder.state is None:  # no response was initiated
                await HTTP_500_INTERNAL_SERVER_ERROR_RESPONSE(scope, receive, send)
            raise exc


class WebSocketNodeRouter(BaseRouter[WebSocketScope]):
    async def __call__(
        self, scope: WebSocketScope, receive: WebSocketReceive, send: WebSocketSend
    ) -> None:
        try:
            route: Route = [(scope["path"], None)]
            response = await self.node(scope, route)
            if response is not None:
                await response(scope, receive, send)
            else:
                # TODO: websocket.http.response
                await send(
                    WebSocketCloseEvent(
                        {"type": "websocket.close", "code": 1000, "reason": "not found"}
                    )
                )
        except Exception as exc:
            await send(
                WebSocketCloseEvent(
                    {"type": "websocket.close", "code": 1011, "reason": None}
                )
            )
            raise exc
