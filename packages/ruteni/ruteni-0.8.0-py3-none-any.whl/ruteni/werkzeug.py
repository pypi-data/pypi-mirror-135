from asgiref.typing import HTTPScope

from werkzeug.datastructures import Headers
from werkzeug.sansio.request import Request as _Request


class Request(_Request):
    def __init__(self, scope: HTTPScope) -> None:
        remote_addr, remote_port = (
            scope["client"] if scope["client"] is not None else (None, None)
        )
        super().__init__(
            method=scope["method"],
            scheme=scope["scheme"],
            server=scope["server"],
            root_path="",
            path=scope["path"],
            query_string=scope["query_string"],
            headers=Headers(
                tuple((key.decode(), val.decode()) for key, val in scope["headers"])
            ),
            remote_addr=remote_addr,
        )
