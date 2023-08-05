import logging

from asgiref.typing import HTTPScope
from marshmallow import Schema, validate
from marshmallow.fields import Email, String
from ruteni.apis import APINode
from ruteni.apis.auth import AuthPair, register_identity_provider
from ruteni.apis.users import get_user_by_id
from ruteni.core.types import HTTPApp, HTTPReceive
from ruteni.endpoints import GET, POST
from ruteni.exceptions import HTTPException
from ruteni.plugins.groups import get_user_groups
from ruteni.plugins.passwords import PASSWORD_MAX_LENGTH, check_password
from ruteni.plugins.session import User, get_user_from_cookie, session_header_value
from ruteni.plugins.token import MAX_CLIENT_ID_LENGTH
from ruteni.responses import (
    HTTP_400_BAD_REQUEST_RESPONSE,
    HTTP_401_UNAUTHORIZED_RESPONSE,
)
from ruteni.routing import current_path_is
from ruteni.routing.nodes.http import HTTPAppMapNode
from ruteni.utils.form import get_form2
from starlette.authentication import AuthCredentials, BaseUser
from starlette.responses import JSONResponse, RedirectResponse

logger = logging.getLogger(__name__)


# same code as in auth/token.py
class RuteniUser(BaseUser):
    def __init__(self, user: User) -> None:
        self.id = user["id"]
        self.email = user["email"]
        self.name = user["display_name"]
        self.locale = user["locale"]
        self.groups = user["groups"]

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.name


def authenticate(user: User) -> AuthPair:
    scopes = user["groups"] + ["authenticated"]
    return AuthCredentials(scopes), RuteniUser(user)


register_identity_provider("ruteni", authenticate)


class SignInSchema(Schema):
    email = Email(required=True)  # type: ignore
    password = String(required=True, validate=validate.Length(max=PASSWORD_MAX_LENGTH))
    client_id = String(
        required=True, validate=validate.Length(max=MAX_CLIENT_ID_LENGTH)
    )


async def signin(scope: HTTPScope, receive: HTTPReceive) -> HTTPApp:
    content_type_header = None
    cookie_header = None
    for key, val in scope["headers"]:
        if key == b"content-type":
            content_type_header = val
            if cookie_header is not None:
                break
        elif key == b"cookie":
            cookie_header = val
            if get_user_from_cookie(cookie_header.decode("latin-1")):
                pass  # TODO: https://stackoverflow.com/questions/18263796/
            if content_type_header is not None:
                break

    try:
        form = await get_form2(content_type_header, receive, SignInSchema)
    except HTTPException as exc:
        return exc.response

    password_info = await check_password(form["email"], form["password"])

    if password_info is None:  # TODO: not clear what status code should be used
        return HTTP_401_UNAUTHORIZED_RESPONSE

    user_info = await get_user_by_id(password_info.user_id)
    assert user_info
    user = user_info.to_dict()
    user["provider"] = "ruteni"
    user["groups"] = await get_user_groups(user_info.id)

    morsel = session_header_value(user)
    return JSONResponse(user, headers={"Set-Cookie": morsel.OutputString()})


async def signout(scope: HTTPScope) -> HTTPApp:
    for key, val in scope["headers"]:
        if key == b"cookie":
            if get_user_from_cookie(val.decode("latin-1")):
                break
    else:
        return HTTP_400_BAD_REQUEST_RESPONSE  # TODO: which status code?

    morsel = session_header_value(None)
    return RedirectResponse(url="/", headers={"Set-Cookie": morsel.OutputString()})


api_node = APINode(
    "auth",
    1,
    [
        HTTPAppMapNode(current_path_is("/signin"), POST(signin)),
        HTTPAppMapNode(current_path_is("/signout"), GET(signout)),
    ],
)
