from collections.abc import Mapping
from typing import Optional, cast, get_args

from asgiref.typing import HTTPScope
from pkg_resources import load_entry_point
from ruteni.core.types import HTTPApp, HTTPAppMap, Method
from ruteni.endpoints import load_http_endpoint_entry_point
from ruteni.responses import HTTP_405_METHOD_NOT_ALLOWED_RESPONSE
from ruteni.routing.types import AcceptRoute, HTTPNode, Route

ALL_METHODS: tuple[Method, ...] = get_args(Method)


def load_http_node_entry_point(dist: str, name: str) -> HTTPNode:
    return load_entry_point(dist, "ruteni.node.http.v1", name)


class HTTPAppMapNode:
    def __init__(self, accept_route: AcceptRoute, app_map: HTTPAppMap) -> None:
        self.accept_route = accept_route
        self.app_map = app_map

    async def __call__(self, scope: HTTPScope, route: Route) -> Optional[HTTPApp]:
        method = cast(Method, scope["method"])
        return (
            self.app_map.get(method, HTTP_405_METHOD_NOT_ALLOWED_RESPONSE)
            if self.accept_route(route)
            else None
        )


class HTTPEntryPointAppMapNode(HTTPAppMapNode):
    def __init__(
        self, accept_route: AcceptRoute, entry_map: Mapping[Method, tuple[str, str]]
    ) -> None:
        super().__init__(
            accept_route,
            {
                method: load_http_endpoint_entry_point(*info)
                for method, info in entry_map.items()
            },
        )
