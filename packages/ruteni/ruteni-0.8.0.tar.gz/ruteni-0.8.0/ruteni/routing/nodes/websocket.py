from typing import Optional

from asgiref.typing import WebSocketScope
from pkg_resources import load_entry_point
from ruteni.core.types import WebSocketApp
from ruteni.endpoints import load_websocket_endpoint_entry_point
from ruteni.routing.types import AcceptRoute, Route, WebSocketNode


def load_websocket_node_entry_point(dist: str, name: str) -> WebSocketNode:
    return load_entry_point(dist, "ruteni.node.websocket.v1", name)


class WebSocketAppNode:
    def __init__(self, accept_route: AcceptRoute, app: WebSocketApp) -> None:
        self.accept_route = accept_route
        self.app = app

    async def __call__(
        self, scope: WebSocketScope, route: Route
    ) -> Optional[WebSocketApp]:
        return self.app if self.accept_route(route) else None


class WebSocketEntryPointNode(WebSocketAppNode):
    def __init__(self, accept_route: AcceptRoute, dist: str, name: str) -> None:
        super().__init__(accept_route, load_websocket_endpoint_entry_point(dist, name))
