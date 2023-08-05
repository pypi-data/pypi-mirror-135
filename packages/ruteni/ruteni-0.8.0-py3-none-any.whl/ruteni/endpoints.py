from asgiref.typing import HTTPScope
from pkg_resources import load_entry_point

from ruteni.core.types import (
    HTTPApp,
    HTTPAppMap,
    HTTPReceive,
    HTTPSend,
    ReadEndpoint,
    WebSocketApp,
    WriteEndpoint,
)


def load_http_endpoint_entry_point(dist: str, name: str) -> HTTPApp:
    return load_entry_point(dist, "ruteni.endpoint.http.v1", name)


def load_websocket_endpoint_entry_point(dist: str, name: str) -> WebSocketApp:
    return load_entry_point(dist, "ruteni.endpoint.websocket.v1", name)


def GET(endpoint: ReadEndpoint) -> HTTPAppMap:
    async def app(scope: HTTPScope, receive: HTTPReceive, send: HTTPSend) -> None:
        response = await endpoint(scope)
        await response(scope, receive, send)

    return dict(GET=app)


def POST(endpoint: WriteEndpoint) -> HTTPAppMap:
    async def app(scope: HTTPScope, receive: HTTPReceive, send: HTTPSend) -> None:
        response = await endpoint(scope, receive)
        await response(scope, receive, send)

    return dict(POST=app)
