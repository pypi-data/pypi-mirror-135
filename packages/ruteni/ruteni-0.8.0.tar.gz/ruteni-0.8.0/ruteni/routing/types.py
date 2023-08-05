import os
from collections.abc import Awaitable, Callable, MutableSequence
from typing import Literal, Optional, Tuple, TypeVar, Union
from uuid import UUID

from asgiref.typing import HTTPScope, WebSocketScope
from ruteni.core.types import App, HTTPApp, WebSocketApp
from starlette.datastructures import URLPath

PathLike = Union[str, os.PathLike[str]]

ParamTypeName = Literal["str", "path", "int", "float", "uuid"]
Param = Union[str, URLPath, int, float, UUID]
RouteElem = tuple[URLPath, Optional[Union[Param, Tuple[Param, ...]]]]
Route = MutableSequence[RouteElem]
Extractor = Callable[[URLPath], Optional[RouteElem]]

HTTPNode = Callable[[HTTPScope, Route], Awaitable[Optional[HTTPApp]]]
HTTPRouter = Callable[[HTTPScope], HTTPApp]

WebSocketNode = Callable[[WebSocketScope, Route], Awaitable[Optional[WebSocketApp]]]
WebSocketRouter = Callable[[WebSocketScope], WebSocketApp]

TScope = TypeVar("TScope", HTTPScope, WebSocketScope)

Node = Callable[[TScope, Route], Awaitable[Optional[App]]]
Router = Callable[[TScope], App]


# from starlette.convertors import CONVERTOR_TYPES
# CONVERTOR_TYPES keys: ["str", "path", "int", "float", "uuid"]
# from werkzeug.routing import DEFAULT_CONVERTERS
# DEFAULT_CONVERTERS keys: ["default", "string", "any", "path", "int", "float", "uuid"]
AcceptRoute = Callable[[Route], bool]
FileMatch = Callable[[HTTPScope, Route], Optional[PathLike]]
