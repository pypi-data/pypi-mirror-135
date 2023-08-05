from unittest import IsolatedAsyncioTestCase

from asgiref.typing import ASGIVersions, HTTPScope, WebSocketScope
from ruteni.core.types import HTTPReceive, HTTPSend, WebSocketReceive, WebSocketSend
from ruteni.responses import Response
from ruteni.routing.nodes.http import HTTPAppMapNode
from ruteni.routing.nodes.websocket import WebSocketAppNode
from ruteni.routing.types import Route
from ruteni.status import HTTP_405_METHOD_NOT_ALLOWED


class TestHTTPAppMapNode(IsolatedAsyncioTestCase):
    async def test_call(self) -> None:
        async def get(scope: HTTPScope, receive: HTTPReceive, send: HTTPSend) -> None:
            self.assertEqual(scope["method"], "GET")

        async def post(scope: HTTPScope, receive: HTTPReceive, send: HTTPSend) -> None:
            self.assertEqual(scope["method"], "POST")

        http_scope = HTTPScope(
            {
                "type": "http",
                "asgi": ASGIVersions({"spec_version": "", "version": "3.0"}),
                "http_version": "",
                "method": "GET",
                "scheme": "http",
                "path": "/",
                "raw_path": b"",
                "query_string": b"",
                "root_path": "",
                "headers": ((b"", b""),),
                "client": None,
                "server": None,
                "extensions": None,
            }
        )

        # the node must return None if AcceptRoute returns False
        def accept_route_false(route: Route) -> bool:
            return False

        node = HTTPAppMapNode(accept_route_false, {"GET": get})
        response = await node(http_scope, [(http_scope["path"], None)])
        self.assertIsNone(response)

        # the node must return an app or 405 if AcceptRoute returns True
        def accept_route_true(route: Route) -> bool:
            return True

        # GET should return `get`
        node = HTTPAppMapNode(accept_route_true, {"GET": get})
        response = await node(http_scope, [(http_scope["path"], None)])
        self.assertEqual(response, get)

        # POST is not allowed
        http_scope["method"] = "POST"
        response = await node(http_scope, [(http_scope["path"], None)])
        assert isinstance(response, Response)
        self.assertEqual(response.status, HTTP_405_METHOD_NOT_ALLOWED)

        # POST is now allowed
        node = HTTPAppMapNode(accept_route_true, {"POST": post})
        response = await node(http_scope, [(http_scope["path"], None)])
        self.assertEqual(response, post)


class TestWebSocketAppNode(IsolatedAsyncioTestCase):
    async def test_call(self) -> None:
        async def app(
            scope: WebSocketScope, receive: WebSocketReceive, send: WebSocketSend
        ) -> None:
            pass

        websocket_scope = WebSocketScope(
            {
                "type": "websocket",
                "asgi": ASGIVersions({"spec_version": "", "version": "3.0"}),
                "http_version": "",
                "scheme": "http",
                "path": "/",
                "raw_path": b"",
                "query_string": b"",
                "root_path": "",
                "headers": ((b"", b""),),
                "client": None,
                "server": None,
                "subprotocols": ("",),
                "extensions": None,
            }
        )

        # the node must return None if AcceptRoute returns False
        def accept_route_false(route: Route) -> bool:
            return False

        node = WebSocketAppNode(accept_route_false, app)
        response = await node(websocket_scope, [(websocket_scope["path"], None)])
        self.assertIsNone(response)

        # the node must return an app or 405 if AcceptRoute returns True
        def accept_route_true(route: Route) -> bool:
            return True

        node = WebSocketAppNode(accept_route_true, app)
        response = await node(websocket_scope, [(websocket_scope["path"], None)])
        self.assertEqual(response, app)
