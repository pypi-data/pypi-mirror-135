from typing import Optional

from starlette.datastructures import State

from ruteni.core.app import Application
from ruteni.core.lifespan import Lifespan
from ruteni.core.types import HTTPApp, WebSocketApp
from ruteni.responses import HTTP_404_NOT_FOUND_RESPONSE, not_a_websocket
from ruteni.routing.routers import HTTPNodeRouter, WebSocketNodeRouter
from ruteni.routing.types import HTTPNode, WebSocketNode
from ruteni.services import Service
from ruteni.tasks import Tasks


class Ruteni(Application):
    def __init__(
        self,
        http_node: Optional[HTTPNode] = None,
        websocket_node: Optional[WebSocketNode] = None,
        *,
        services: Optional[set[str]] = None
    ) -> None:
        state = State()
        tasks = Tasks(state)
        lifespan_app = Lifespan(tasks)

        if services is not None:
            Service.load_entry_points(services)
            tasks.on_startup(Service.start_services)
            tasks.on_shutdown(Service.stop_services)

        http_app: HTTPApp = HTTP_404_NOT_FOUND_RESPONSE
        if http_node is not None:
            http_app = HTTPNodeRouter(http_node)

        websocket_app: WebSocketApp = not_a_websocket
        if websocket_node is not None:
            websocket_app = WebSocketNodeRouter(websocket_node)

        super().__init__(http_app, websocket_app, lifespan_app)
