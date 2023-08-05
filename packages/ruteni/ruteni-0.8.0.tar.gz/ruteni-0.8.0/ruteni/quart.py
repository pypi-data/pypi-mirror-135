from collections.abc import Awaitable, Callable, Iterable
from typing import cast

from asgiref.typing import WebSocketScope

from quart.wrappers.websocket import Websocket
from ruteni.core.types import WebSocketReceive, WebSocketSend
from werkzeug.datastructures import Headers

Accept = Callable[[Headers, Iterable[str]], Awaitable[None]]


class WebSocket(Websocket):
    def __init__(
        self,
        scope: WebSocketScope,
        receive: WebSocketReceive,
        send: WebSocketSend,
        accept: Accept,
    ) -> None:
        super().__init__(
            path=scope["path"],
            query_string=scope["query_string"],
            scheme=scope["scheme"],
            headers=Headers(
                tuple((key.decode(), val.decode()) for key, val in scope["headers"])
            ),
            root_path="",
            http_version="1.1",  # scope["http_version"],
            subprotocols=list(scope["subprotocols"]),
            receive=receive,
            send=send,
            accept=accept,
            scope=cast(dict[str, str], scope),
        )
