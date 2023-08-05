import os
import stat
from collections.abc import Mapping
from typing import Optional

import anyio
from asgiref.typing import HTTPScope
from ruteni.core.types import App
from ruteni.responses import (
    HTTP_405_METHOD_NOT_ALLOWED_RESPONSE,
    HTTP_500_INTERNAL_SERVER_ERROR_RESPONSE,
)
from ruteni.routing.types import AcceptRoute, FileMatch, PathLike, Route
from starlette.responses import FileResponse


class FileNode:
    def __init__(
        self,
        accept_route: AcceptRoute,
        file_path: PathLike,
        *,
        media_type: Optional[str] = None,
        headers: Optional[Mapping] = None,
    ) -> None:
        stat_result = os.stat(file_path)  # TODO: util
        assert not stat.S_ISDIR(stat_result.st_mode)
        self.accept_route = accept_route
        self.file_path = file_path
        self.media_type = media_type
        self.stat_result = stat_result
        self.headers = headers
        self.response = FileResponse(
            self.file_path,
            stat_result=self.stat_result,
            media_type=self.media_type,
            headers=self.headers,
        )

    def __repr__(self) -> str:
        return "%s(file_path=%r, media_type=%r, content_length=%r)" % (
            self.__class__.__name__,
            self.file_path,
            self.media_type,
            self.stat_result.st_size,
        )

    async def __call__(self, scope: HTTPScope, route: Route) -> Optional[App]:
        if not self.accept_route(route):
            return None
        return (
            self.response
            if scope["method"] == "GET"
            else HTTP_405_METHOD_NOT_ALLOWED_RESPONSE
        )


class CustomFileNode:
    def __init__(
        self,
        match: FileMatch,
        *,
        media_type: Optional[str] = None,
        headers: Optional[Mapping] = None,
    ) -> None:
        self.match = match
        self.media_type = media_type
        self.headers = headers

    def __repr__(self) -> str:
        return "%s(media_type=%r)" % (self.__class__.__name__, self.media_type)

    async def __call__(self, scope: HTTPScope, route: Route) -> Optional[App]:
        # TODO: the matching function probably needs to be able to return an error
        file_path = self.match(scope, route)
        if file_path is None:
            return None

        if scope["method"] != "GET":
            return HTTP_405_METHOD_NOT_ALLOWED_RESPONSE

        try:
            stat_result = await anyio.to_thread.run_sync(os.stat, file_path)
        except FileNotFoundError:
            return HTTP_500_INTERNAL_SERVER_ERROR_RESPONSE

        return (
            FileResponse(
                file_path,
                stat_result=stat_result,
                media_type=self.media_type,
                headers=self.headers,
            )
            if not stat.S_ISDIR(stat_result.st_mode)
            else HTTP_500_INTERNAL_SERVER_ERROR_RESPONSE
        )
