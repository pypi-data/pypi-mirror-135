from typing import Optional

from asgiref.typing import HTTPScope
from ruteni.core.types import App
from ruteni.responses import HTTP_405_METHOD_NOT_ALLOWED_RESPONSE, Content, Response
from ruteni.routing.types import AcceptRoute, Route


class HTTPContentNode:
    def __init__(self, accept_route: AcceptRoute, content: Content) -> None:
        self.accept_route = accept_route
        self.response = Response(content)

    def __repr__(self) -> str:
        return "%s()" % self.__class__.__name__

    async def __call__(self, scope: HTTPScope, route: Route) -> Optional[App]:
        if not self.accept_route(route):
            return None
        return (
            self.response
            if scope["method"] == "GET"
            else HTTP_405_METHOD_NOT_ALLOWED_RESPONSE
        )
