from __future__ import annotations

import logging
from collections.abc import Iterable, Mapping
from typing import Generic, Optional, TypeVar

from asgiref.typing import HTTPScope, WebSocketScope
from ruteni.core.types import App
from ruteni.routing.types import AcceptRoute, Extractor, Node, Route
from starlette.datastructures import URLPath
from starlette.responses import RedirectResponse
from ruteni.routing import current_path

logger = logging.getLogger(__name__)


TScope = TypeVar("TScope", HTTPScope, WebSocketScope)


class IterableNode(Generic[TScope]):
    def __init__(self, nodes: Iterable[Node]) -> None:
        # TODO: assert nodes can be iterated multiple times (e.g. not a generator)
        self.nodes = nodes

    def __repr__(self) -> str:
        return "%s()" % self.__class__.__name__

    async def __call__(self, scope: TScope, route: Route) -> Optional[App]:
        for node in self.nodes:
            response = await node(scope, route)
            if response is not None:
                return response
        return None


class MappingNode(Generic[TScope]):
    def __init__(self, node_map: Mapping[URLPath, Node]) -> None:
        self.node_map = node_map

    def __repr__(self) -> str:
        return "%s()" % self.__class__.__name__

    async def __call__(self, scope: TScope, route: Route) -> Optional[App]:
        url_path = current_path(route)
        for prefix, node in self.node_map.items():
            if url_path == prefix or url_path.startswith(prefix + "/"):
                route_elem = (url_path.removeprefix(prefix), prefix)
                route.append(route_elem)
                response = await node(scope, route)
                if response is None:
                    route.pop()
                return response
        return None


class ExtractorNode(Generic[TScope]):
    def __init__(self, extractor: Extractor, child: Node) -> None:
        self.extractor = extractor
        self.child = child

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + ", extractor=%r)" % self.extractor

    async def __call__(self, scope: TScope, route: Route) -> Optional[App]:
        route_elem = self.extractor(current_path(route))
        if route_elem is None:
            return None
        route.append(route_elem)
        response = await self.child(scope, route)
        if response is None:
            route.pop()
        return response


class RedirectNode(Generic[TScope]):
    def __init__(self, accept_route: AcceptRoute, url_path: URLPath) -> None:
        self.accept_route = accept_route
        self.url_path = url_path

    def __repr__(self) -> str:
        return "%s(url_path=%r)" % (self.__class__.__name__, self.url_path)

    async def __call__(self, scope: TScope, route: Route) -> Optional[App]:
        return RedirectResponse(self.url_path) if self.accept_route(route) else None


class SlashRedirectNode(Generic[TScope]):
    def __repr__(self) -> str:
        return "%s()" % (self.__class__.__name__)

    async def __call__(self, scope: TScope, route: Route) -> Optional[App]:
        return (
            RedirectResponse(scope["path"] + "/") if current_path(route) == "" else None
        )
