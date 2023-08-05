import logging

import httpx
from asgiref.typing import HTTPScope
from authlib.oidc.discovery.well_known import get_well_known_url
from babel.core import LOCALE_ALIASES
from ruteni.apis import APINode
from ruteni.apis.auth import AuthPair, register_identity_provider
from ruteni.apis.users import add_user, get_user_by_email
from ruteni.core.types import HTTPReceive, HTTPSend
from ruteni.plugins.groups import get_user_groups
from ruteni.plugins.oauth import oauth
from ruteni.plugins.session import User, del_session_user, set_session_user
from ruteni.routing import current_path_is
from ruteni.routing.nodes.http import HTTPAppMapNode
from starlette.authentication import AuthCredentials, BaseUser
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse, Response

logger = logging.getLogger(__name__)


class StarletteHTTPEndpoint:
    def __init__(self, func: RequestResponseEndpoint) -> None:
        self.func = func

    async def __call__(
        self, scope: HTTPScope, receive: HTTPReceive, send: HTTPSend
    ) -> None:
        request = Request(scope, receive=receive, send=send)
        response = await self.func(request)
        await response(scope, receive, send)


class GoogleUser(BaseUser):
    """
    As of 2021/07/20, `user` is something like this:
    "iss": "https://accounts.google.com",
    "azp": "1084386621732-qjmkaojnut33[...]7q22me2p6qb1.apps.googleusercontent.com",
    "aud": "1084386621732-qjmkaojnut33[...]7q22me2p6qb1.apps.googleusercontent.com",
    "sub": "106637688186237713656",
    "hd": "undomaine.fr",
    "email": "jean.dupont@undomaine.fr",
    "email_verified": True,
    "at_hash": "ndyKkyw5_LQTsA9JKLim4A",
    "nonce": "uYnEP5r9BQK9ilJ4ruC7",
    "name": "Jean Dupont",
    "picture": "https://lh3.googleusercontent.com/a/AATXAJymU07Yz4XziVRLP3RQK3...",
    "given_name": "Jean",
    "family_name": "Dupont",
    "locale": "fr",
    "iat": 1625999571,
    "exp": 1626003171,
    """

    def __init__(self, user: dict) -> None:
        self.id = user["id"]
        self.email = user["email"]
        self.name = user["name"]
        self.given_name = user["given_name"]
        self.family_name = user["family_name"]
        self.picture = user["picture"]
        self.groups = user["groups"]
        self.locale = user["locale"]  # TODO: convert locale to 5-letter format

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.name


def authenticate(user: User) -> AuthPair:
    assert user["iss"] == "https://accounts.google.com"
    scopes = user["groups"] + ["authenticated"]
    return AuthCredentials(scopes), GoogleUser(user)


register_identity_provider("google", authenticate)


google = oauth.register(
    name="google",
    server_metadata_url=get_well_known_url(
        "https://accounts.google.com", external=True
    ),
    client_kwargs={"scope": "openid email profile"},
)


async def signin(request: Request) -> Response:
    redirect_uri = request.url_for("google-auth")
    try:
        return await google.authorize_redirect(request, redirect_uri)
    except httpx.ConnectTimeout:
        return PlainTextResponse(
            "Connection timeout redirecting to google. Please retry later."
        )


async def auth(request: Request) -> Response:
    # get the token from the URL and parse it to get the user data
    token = await google.authorize_access_token(request)
    user = await google.parse_id_token(request, token)

    # look for the user ID in the database from his/her email address
    user_info = await get_user_by_email(user["email"])

    # if the user is unknown, create a new profile
    if user_info is None:
        locale = user["locale"]
        if locale in LOCALE_ALIASES:
            locale = LOCALE_ALIASES[locale].replace("_", "-")
        user_info = await add_user(user["name"], user["email"], locale)

    # record the user ID and the groups the user belongs to
    user["id"] = user_info.id
    user["groups"] = await get_user_groups(user_info.id)
    user["provider"] = "google"

    logger.debug(f'{user["email"]} logged in; groups: {user["groups"]}')

    # record in the user data in the session
    set_session_user(request, dict(user))
    return RedirectResponse(url="/")


async def signout(request: Request) -> Response:
    del_session_user(request)
    return RedirectResponse(url="/")


api = APINode(
    "google",
    1,
    [
        HTTPAppMapNode(
            current_path_is("/signin"), {"GET": StarletteHTTPEndpoint(signin)}
        ),
        HTTPAppMapNode(
            current_path_is("/signout"), {"GET": StarletteHTTPEndpoint(signout)}
        ),
        HTTPAppMapNode(current_path_is("/auth"), {"GET": StarletteHTTPEndpoint(auth)}),
    ],
)
