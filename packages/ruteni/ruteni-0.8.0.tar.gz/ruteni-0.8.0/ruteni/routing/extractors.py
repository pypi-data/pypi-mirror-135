import re
from typing import Optional
from uuid import UUID

from ruteni.routing.types import RouteElem
from starlette.datastructures import URLPath


def uuid_extractor(url_path: URLPath) -> Optional[RouteElem]:
    if (
        len(url_path) >= 37
        and url_path[0] == "/"
        and (len(url_path) == 37 or url_path[37] == "/")
    ):
        try:
            uuid = UUID(url_path[1:37])
        except ValueError:
            pass
        else:
            return (url_path[37:], uuid)
    return None


def int_extractor(url_path: URLPath) -> Optional[RouteElem]:
    parts = url_path.split("/", 2)
    if len(parts) >= 2 and parts[0] == "":  # i.e. url_path[0] == "/"
        try:
            value = int(parts[1])
        except ValueError:
            pass
        else:
            return ("/" + parts[2] if len(parts) > 2 else "", value)
    return None


class PrefixExtractor:
    def __init__(self, prefix: URLPath) -> None:
        self.prefix = prefix

    def __repr__(self) -> str:
        return "%s(prefix=%r)" % (self.__class__.__name__, self.prefix)

    def __call__(self, url_path: URLPath) -> Optional[RouteElem]:
        return (
            (url_path.removeprefix(self.prefix), self.prefix)
            if url_path == self.prefix or url_path.startswith(self.prefix + "/")
            else None
        )


class RegexExtractor:
    def __init__(self, pattern: URLPath) -> None:
        self.pattern = pattern + "(/.*)"
        self.prog = re.compile(pattern)

    def __repr__(self) -> str:
        return "%s(pattern=%r)" % (self.__class__.__name__, self.pattern)

    def __call__(self, url_path: URLPath) -> Optional[RouteElem]:
        result = self.prog.fullmatch(url_path)
        if result is None:
            return None
        groups = result.groups()
        return (groups[-1], groups[:-1])
