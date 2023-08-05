import io
import json
import urllib
from cgi import parse_multipart
from collections.abc import Container
from typing import Any, Optional

from asgiref.typing import HTTPScope
from marshmallow import Schema
from marshmallow.exceptions import ValidationError
from ruteni.core.types import HTTPReceive
from ruteni.exceptions import HTTPException
from ruteni.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from werkzeug.http import parse_options_header


def get_content_type_header(scope: HTTPScope) -> Optional[bytes]:
    for key, val in scope["headers"]:
        if key == b"content-type":
            return val
    return None


async def get_chunk(receive: HTTPReceive) -> bytes:
    event = await receive()

    if event["type"] == "http.disconnect":
        raise HTTPException(HTTP_400_BAD_REQUEST)

    assert event["type"] == "http.request"

    # TODO: if the server is really ASGI compliant, both event["body"] and
    # event["more_body"] should be defined, but uvicorn may not define those
    if "body" not in event or event.get("more_body", False):
        raise HTTPException(HTTP_400_BAD_REQUEST)

    return event["body"]


def parse_content_type(
    header: Optional[bytes], allowed_types: Optional[Container] = None
) -> tuple[str, dict[str, str]]:
    if header is None:
        raise HTTPException(HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    content_type, options = parse_options_header(
        header.decode("latin-1"), multiple=False
    )

    if allowed_types and content_type not in allowed_types:
        raise HTTPException(HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    return content_type, options


def extract_form(body: bytes, content_type: str, options: dict[str, str]) -> dict:
    if content_type == "application/json":
        try:
            raw_form = json.loads(body)
        except json.decoder.JSONDecodeError:
            raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY)
    elif content_type == "multipart/form-data":
        raw_form = parse_multipart(io.BytesIO(body), dict(boundary=b"--"))  # options
        if len(raw_form) == 0:  # TODO: detect errors
            raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY)
    elif content_type == "application/x-www-form-urlencoded":
        raw_form = {
            key.decode(): val[0].decode()
            for key, val in urllib.parse.parse_qs(body).items()
        }

    return raw_form


async def receive_form(
    content_type_header: Optional[bytes], receive: HTTPReceive
) -> dict[str, Any]:
    content_type, options = parse_content_type(
        content_type_header,
        (
            "application/json",
            "multipart/form-data",
            "application/x-www-form-urlencoded",
        ),
    )
    # we only allow one chunk; convert to a loop if this can be a problem
    body = await get_chunk(receive)
    return extract_form(body, content_type, options)


async def get_form2(
    content_type_header: Optional[bytes], receive: HTTPReceive, Schema: type[Schema]
) -> dict:
    raw_form = await receive_form(content_type_header, receive)
    schema = Schema()
    try:
        return schema.load(raw_form)
    except ValidationError:
        raise HTTPException(HTTP_400_BAD_REQUEST)


async def get_json_body(
    scope: HTTPScope,
    receive: HTTPReceive,
    content_type: Optional[bytes] = b"application/json",
) -> dict:
    if get_content_type_header(scope) != content_type:  # TODO: relax?
        raise HTTPException(HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    body = await get_chunk(receive)  # TODO: use loop version
    # TODO: have a marshmallow schema to validate report?
    try:
        return json.loads(body.decode("utf-8"))
    except json.decoder.JSONDecodeError:
        raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY)
