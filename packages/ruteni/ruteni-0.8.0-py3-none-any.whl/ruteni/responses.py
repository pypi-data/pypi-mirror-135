from collections.abc import Iterable
from http import HTTPStatus
from typing import Optional

from asgiref.typing import (
    HTTPResponseBodyEvent,
    HTTPResponseStartEvent,
    HTTPScope,
    WebSocketCloseEvent,
    WebSocketScope,
)

from ruteni.content import TEXT_PLAIN_CONTENT_TYPE, Content
from ruteni.core.types import (
    Header,
    HTTPReceive,
    HTTPSend,
    WebSocketReceive,
    WebSocketSend,
)


class Response:
    def __init__(
        self,
        content: Optional[Content] = None,
        *,
        headers: Optional[Iterable[Header]] = None,
        status: int = HTTPStatus.OK
    ) -> None:
        self.status = status
        self.headers = tuple(headers) if headers else ()
        self.set_content(content or Content(b"", b"application/octet-stream"))

    def set_content(self, content: Content) -> None:
        # TODO: `headers` could be a tuple but it raises an exception in uvicorn
        headers = list(
            self.headers
            + (
                (b"content-length", str(len(content.body)).encode("latin-1")),
                (b"content-type", content.content_type),
            )
        )
        self.start_event = HTTPResponseStartEvent(
            {
                "type": "http.response.start",
                "status": self.status,
                "headers": headers,
            }
        )
        self.body_event = HTTPResponseBodyEvent(
            {"type": "http.response.body", "body": content.body, "more_body": False}
        )

    async def __call__(
        self, scope: HTTPScope, receive: HTTPReceive, send: HTTPSend
    ) -> None:
        await send(self.start_event)
        await send(self.body_event)


def mkres(status: HTTPStatus) -> Response:
    return Response(
        Content(status.phrase.encode("utf-8"), TEXT_PLAIN_CONTENT_TYPE), status=status
    )


http_response = {status: mkres(status) for status in HTTPStatus}

HTTP_200_OK_RESPONSE = mkres(HTTPStatus.OK)
HTTP_400_BAD_REQUEST_RESPONSE = mkres(HTTPStatus.BAD_REQUEST)
HTTP_401_UNAUTHORIZED_RESPONSE = mkres(HTTPStatus.UNAUTHORIZED)
HTTP_403_FORBIDDEN_RESPONSE = mkres(HTTPStatus.FORBIDDEN)
HTTP_404_NOT_FOUND_RESPONSE = mkres(HTTPStatus.NOT_FOUND)
HTTP_405_METHOD_NOT_ALLOWED_RESPONSE = mkres(HTTPStatus.METHOD_NOT_ALLOWED)
HTTP_415_UNSUPPORTED_MEDIA_TYPE_RESPONSE = mkres(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
HTTP_422_UNPROCESSABLE_ENTITY_RESPONSE = mkres(HTTPStatus.UNPROCESSABLE_ENTITY)
HTTP_500_INTERNAL_SERVER_ERROR_RESPONSE = mkres(HTTPStatus.INTERNAL_SERVER_ERROR)


class WebSocketClose:
    def __init__(self, reason: Optional[str] = None, code: int = 1000) -> None:
        self.event = WebSocketCloseEvent(
            {"type": "websocket.close", "code": code, "reason": reason}
        )

    async def __call__(
        self, scope: WebSocketScope, receive: WebSocketReceive, send: WebSocketSend
    ) -> None:
        await send(self.event)


not_a_websocket = WebSocketClose("Not Found")  # TODO: better name
