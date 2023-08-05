from asgiref.typing import WebSocketAcceptEvent, WebSocketCloseEvent, WebSocketScope
from ruteni.core.types import WebSocketReceive, WebSocketSend


class WebSocket:
    async def __call__(
        self, scope: WebSocketScope, receive: WebSocketReceive, send: WebSocketSend
    ) -> None:
        print("websocket", scope["path"])
        accept = True
        while True:
            event = await receive()
            if event["type"] == "websocket.connect":
                if accept:
                    await send(
                        WebSocketAcceptEvent(
                            {
                                "type": "websocket.accept",
                                "headers": (),
                                "subprotocol": None,
                            }
                        )
                    )
                else:
                    await send(
                        WebSocketCloseEvent(
                            {"type": "websocket.close", "code": 1000, "reason": None}
                        )
                    )
                    return
            elif event["type"] == "websocket.receive":
                print("received", event["text"], event["bytes"])
            else:
                assert event["type"] == "websocket.disconnect"
                print("closed:", event["code"])
                return
