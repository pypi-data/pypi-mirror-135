from ruteni.routing.types import AcceptRoute, Route
from collections.abc import Collection
from starlette.datastructures import URLPath


def current_path(route: Route) -> URLPath:
    return route[-1][0]


def current_path_is(url_path: URLPath) -> AcceptRoute:
    return lambda route: current_path(route) == url_path


def current_path_in(url_paths: Collection[URLPath]) -> AcceptRoute:
    return lambda route: current_path(route) in url_paths
