from http import HTTPStatus

from ruteni.core.types import HTTPApp
from ruteni.responses import http_response


class HTTPException(Exception):
    def __init__(self, status: HTTPStatus) -> None:
        Exception.__init__(self, status.phrase)
        self.status = status

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return (
            f"{class_name}(status={self.status.value!r}, detail={self.status.phrase!r})"
        )

    @property
    def response(self) -> HTTPApp:
        return http_response[self.status]


def mkexc(status: HTTPStatus) -> type[Exception]:
    class HTTPException(Exception):
        response = http_response[status]

        def __init__(self) -> None:
            Exception.__init__(self, f"HTTP error: {status.phrase}")

    return HTTPException


Http400BadRequestException = mkexc(HTTPStatus.BAD_REQUEST)
Http401UnauthorizedException = mkexc(HTTPStatus.UNAUTHORIZED)
Http403ForbiddenException = mkexc(HTTPStatus.FORBIDDEN)
Http404NotFoundException = mkexc(HTTPStatus.NOT_FOUND)
Http405MethodNotAllowedException = mkexc(HTTPStatus.METHOD_NOT_ALLOWED)
Http415UnsupportedMediaTypeException = mkexc(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
Http422UnprocessableEntityException = mkexc(HTTPStatus.UNPROCESSABLE_ENTITY)
Http500InternalServerErrorException = mkexc(HTTPStatus.INTERNAL_SERVER_ERROR)
