from collections.abc import Awaitable, Callable, Mapping
from typing import Literal, TypeVar, Union

from asgiref.typing import (
    HTTPDisconnectEvent,
    HTTPRequestEvent,
    HTTPResponseBodyEvent,
    HTTPResponseStartEvent,
    HTTPScope,
    HTTPServerPushEvent,
    LifespanScope,
    LifespanShutdownCompleteEvent,
    LifespanShutdownEvent,
    LifespanShutdownFailedEvent,
    LifespanStartupCompleteEvent,
    LifespanStartupEvent,
    LifespanStartupFailedEvent,
    WebSocketAcceptEvent,
    WebSocketCloseEvent,
    WebSocketConnectEvent,
    WebSocketDisconnectEvent,
    WebSocketReceiveEvent,
    WebSocketResponseBodyEvent,
    WebSocketResponseStartEvent,
    WebSocketScope,
    WebSocketSendEvent,
)

Header = tuple[bytes, bytes]

HTTPReceiveEvent = Union[HTTPRequestEvent, HTTPDisconnectEvent]
HTTPReceive = Callable[[], Awaitable[HTTPReceiveEvent]]
HTTPSendEvent = Union[
    HTTPResponseStartEvent,
    HTTPResponseBodyEvent,
    HTTPServerPushEvent,
    HTTPDisconnectEvent,
]
HTTPSend = Callable[[HTTPSendEvent], Awaitable[None]]
HTTPApp = Callable[[HTTPScope, HTTPReceive, HTTPSend], Awaitable[None]]

ReadEndpoint = Callable[[HTTPScope], Awaitable[HTTPApp]]
WriteEndpoint = Callable[[HTTPScope, HTTPReceive], Awaitable[HTTPApp]]

Method = Literal["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
HTTPAppMap = Mapping[Method, HTTPApp]

WebSocketReceive = Callable[
    [],
    Awaitable[
        Union[WebSocketConnectEvent, WebSocketReceiveEvent, WebSocketDisconnectEvent]
    ],
]
WebSocketSend = Callable[
    [
        Union[
            WebSocketAcceptEvent,
            WebSocketSendEvent,
            WebSocketResponseStartEvent,
            WebSocketResponseBodyEvent,
            WebSocketCloseEvent,
        ]
    ],
    Awaitable[None],
]
WebSocketApp = Callable[
    [WebSocketScope, WebSocketReceive, WebSocketSend], Awaitable[None]
]


LifespanReceiveEvent = Union[LifespanStartupEvent, LifespanShutdownEvent]
LifespanReceive = Callable[[], Awaitable[LifespanReceiveEvent]]
LifespanSendEvent = Union[
    LifespanStartupCompleteEvent,
    LifespanStartupFailedEvent,
    LifespanShutdownCompleteEvent,
    LifespanShutdownFailedEvent,
]
LifespanSend = Callable[[LifespanSendEvent], Awaitable[None]]
LifespanApp = Callable[[LifespanScope, LifespanReceive, LifespanSend], Awaitable[None]]

TScope = TypeVar("TScope", HTTPScope, WebSocketScope, LifespanScope)
TReceive = TypeVar("TReceive", HTTPReceive, WebSocketReceive, LifespanReceive)
TSend = TypeVar("TSend", HTTPSend, WebSocketSend, LifespanSend)
App = Callable[[TScope, TReceive, TSend], Awaitable[None]]

# in the previous definition, TScope, TReceive, TSend cannot be any combination
# it would be nice if we could do this (see https://github.com/python/mypy/issues/3904):
# Receive = {
#     HTTPScope: HTTPReceive,
#     WebSocketScope: WebSocketReceive,
#     LifespanScope: LifespanReceive,
# }
# Send = {
#     HTTPScope: HTTPSend,
#     WebSocketScope: WebSocketSend,
#     LifespanScope: LifespanSend,
# }
# App = Callable[[TScope, Receive[TScope], Send[TScope]], Awaitable[None]]

WWWApp = Union[HTTPApp, WebSocketApp]
ASGIApp = Union[HTTPApp, WebSocketApp, LifespanApp]
