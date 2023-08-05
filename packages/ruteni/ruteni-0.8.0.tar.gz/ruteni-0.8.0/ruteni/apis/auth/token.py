import logging
from datetime import datetime, timezone
from http.cookies import SimpleCookie

from asgiref.typing import HTTPScope
from marshmallow import Schema, validate
from marshmallow.fields import Email, String
from ruteni.apis import APINode
from ruteni.apis.auth import AuthPair, register_identity_provider
from ruteni.config import config
from ruteni.core.types import HTTPApp, HTTPReceive
from ruteni.endpoints import POST
from ruteni.exceptions import HTTPException
from ruteni.plugins.cookie import set_cookie
from ruteni.plugins.groups import get_user_groups
from ruteni.plugins.passwords import PASSWORD_MAX_LENGTH, check_password
from ruteni.plugins.session import User
from ruteni.plugins.site import SITE_NAME
from ruteni.plugins.token import (
    MAX_CLIENT_ID_LENGTH,
    REFRESH_TOKEN_LENGTH,
    create_access_token,
    create_refresh_token,
    get_user_id_from_access_token,
    revoke_refresh_token,
    select_refresh_token,
)
from ruteni.responses import HTTP_401_UNAUTHORIZED_RESPONSE
from ruteni.routing import current_path_is
from ruteni.routing.nodes.http import HTTPAppMapNode
from ruteni.utils.form import get_content_type_header, get_form2
from starlette.authentication import AuthCredentials, BaseUser
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

JWT_ISSUER: str = config.get("RUTENI_AUTH_JWT_ISSUER", default=SITE_NAME)
ACCESS_TOKEN_COOKIE_NAME: str = config.get(
    "RUTENI_AUTH_ACCESS_TOKEN_COOKIE_NAME", default="access_token"
)


# same code as in auth/session.py
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
    try:
        form = await get_form2(get_content_type_header(scope), receive, SignInSchema)
    except HTTPException as exc:
        return exc.response

    password_info = await check_password(form["email"], form["password"])

    if password_info is None:
        return HTTP_401_UNAUTHORIZED_RESPONSE

    user_info, access_token, refresh_token = await create_refresh_token(
        password_info.user_id, JWT_ISSUER, form["client_id"]
    )

    user = user_info.to_dict()
    user["provider"] = "ruteni"
    user["groups"] = await get_user_groups(user_info.id)

    result = {
        "access_token": access_token.claims,
        "refresh_token": refresh_token,
        "user": user,
    }
    logger.debug(f"signin response: {result}")

    response = JSONResponse(result)
    set_cookie(response, ACCESS_TOKEN_COOKIE_NAME, access_token.token)
    return response


class RefreshTokenSchema(Schema):
    refresh_token = String(
        required=True, validate=validate.Length(equal=2 * REFRESH_TOKEN_LENGTH)
    )


async def signout(scope: HTTPScope, receive: HTTPReceive) -> HTTPApp:
    content_type_header = None
    cookie_header = None
    for key, val in scope["headers"]:
        if key == b"content-type":
            content_type_header = val
            if cookie_header is not None:
                break
        elif key == b"cookie":
            cookie_header = val
            if content_type_header is not None:
                break

    if cookie_header is None:
        return HTTP_401_UNAUTHORIZED_RESPONSE

    cookie: SimpleCookie = SimpleCookie(cookie_header.decode("latin-1"))
    access_token_morsel = cookie.get(ACCESS_TOKEN_COOKIE_NAME, None)
    if access_token_morsel is None:
        return HTTP_401_UNAUTHORIZED_RESPONSE

    # TODO: if the access token is expired, this will fail
    user_id = get_user_id_from_access_token(access_token_morsel.value, JWT_ISSUER)

    try:
        form = await get_form2(content_type_header, receive, RefreshTokenSchema)
    except HTTPException as exc:
        return exc.response

    success = await revoke_refresh_token(user_id, form["refresh_token"])

    response = JSONResponse(success)
    response.delete_cookie(ACCESS_TOKEN_COOKIE_NAME)
    return response


async def refresh(scope: HTTPScope, receive: HTTPReceive) -> HTTPApp:
    try:
        form = await get_form2(
            get_content_type_header(scope), receive, RefreshTokenSchema
        )
    except HTTPException as exc:
        return exc.response

    # TODO: implement…
    raise NotImplementedError("FIXME")

    row = await select_refresh_token(form["refresh_token"])

    if row is None:
        # raise ServiceUserException("invalid-token")
        return HTTP_401_UNAUTHORIZED_RESPONSE

    if row["disabled_reason"] is not None:
        return HTTP_401_UNAUTHORIZED_RESPONSE
        # raise ServiceUserException(
        #     "account-disabled",
        #     public=dict(reason=row["disabled_reason"]),
        #     private=dict(id=row["id"], info=disabled),
        # )

    if row["revoked_at"] is not None:
        return HTTP_401_UNAUTHORIZED_RESPONSE
        # raise ServiceUserException(
        #     "revoked-token",
        #     public=dict(at=row["revoked_at"]),
        #     private=dict(id=row["id"]),
        # )

    if row["expires_at"] < datetime.now(timezone.utc).astimezone():
        return HTTP_401_UNAUTHORIZED_RESPONSE
        # raise ServiceUserException(
        #     "expired-token",
        #     public=dict(at=expires_at),
        #     private=dict(id=row["id"]),
        # )

    access_token = await create_access_token(
        row["id"], row["expires_at"], row["user_id"], JWT_ISSUER, row["client_id"]
    )

    response = JSONResponse({"access_token": access_token.claims})
    set_cookie(response, ACCESS_TOKEN_COOKIE_NAME, access_token.token)
    return response


api_node = APINode(
    "jauthn",
    1,
    [
        HTTPAppMapNode(current_path_is("/signin"), POST(signin)),
        HTTPAppMapNode(current_path_is("/signout"), POST(signout)),
        HTTPAppMapNode(current_path_is("/refresh"), POST(refresh)),
    ],
)
