import os
import stat
from collections.abc import Iterable
from typing import Optional

import anyio
from asgiref.typing import HTTPScope
from ruteni.core.types import App
from ruteni.responses import (
    HTTP_400_BAD_REQUEST_RESPONSE,
    HTTP_404_NOT_FOUND_RESPONSE,
    HTTP_405_METHOD_NOT_ALLOWED_RESPONSE,
)
from ruteni.routing.nodes import current_path
from ruteni.routing.types import PathLike, Route
from starlette.responses import FileResponse


class StaticHTTPNode:
    def __init__(self, directories: Iterable[PathLike]) -> None:
        self.directories = [os.path.realpath(directory) for directory in directories]
        for directory in self.directories:
            stat_result = os.stat(directory)
            assert stat.S_ISDIR(stat_result.st_mode)

    def __repr__(self) -> str:
        root_dir = os.path.dirname(os.path.dirname(__file__))  # TODO: fragile
        relpaths = [
            os.path.relpath(directory, root_dir) for directory in self.directories
        ]
        return "%s(directories=%r)" % (self.__class__.__name__, relpaths)

    async def __call__(self, scope: HTTPScope, route: Route) -> Optional[App]:
        url_path = current_path(route)
        if len(url_path) == 0 or url_path[0] != "/":
            return HTTP_400_BAD_REQUEST_RESPONSE

        if scope["method"] != "GET":
            return HTTP_405_METHOD_NOT_ALLOWED_RESPONSE

        for directory in self.directories:

            full_path = os.path.realpath(os.path.join(directory, url_path[1:]))

            # get the stat info for the file, and detect if it does not exist
            try:
                stat_result = await anyio.to_thread.run_sync(os.stat, full_path)
            except FileNotFoundError:
                continue

            # the path exists; test that the path is indeed a descendant of `directory`
            # to prevent requests using `../..` from going too far up the hierarchy
            if os.path.commonprefix([full_path, directory]) != directory:
                return HTTP_400_BAD_REQUEST_RESPONSE

            # return its content if it's a regular file, or error 400 otherwise
            return (
                FileResponse(full_path, stat_result=stat_result)
                if stat.S_ISREG(stat_result.st_mode)
                else HTTP_400_BAD_REQUEST_RESPONSE
            )

        return HTTP_404_NOT_FOUND_RESPONSE
