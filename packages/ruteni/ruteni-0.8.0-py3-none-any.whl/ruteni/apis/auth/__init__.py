import logging
from collections.abc import Callable

from asgiref.typing import WWWScope
from ruteni.plugins.session import User, get_user
from starlette.authentication import AuthCredentials, BaseUser, UnauthenticatedUser
from starlette.datastructures import State

logger = logging.getLogger(__name__)

AuthPair = tuple[AuthCredentials, BaseUser]
AuthFunc = Callable[[User], AuthPair]

providers: dict[str, AuthFunc] = {}


def register_identity_provider(name: str, func: AuthFunc) -> None:
    providers[name] = func


async def authenticate(scope: WWWScope) -> AuthPair:
    user = get_user(scope)
    if user:
        for provider, func in providers.items():
            if user["provider"] == provider:
                return func(user)
        logger.warn(f'unknown identity provider: {user["provider"]}')
    return AuthCredentials(), UnauthenticatedUser()


async def init(state: State) -> None:
    if len(providers) == 0:
        logger.warn("no identity provider was added with register_identity_provider")
    logger.info("started")


# context.tasks.on_startup(init)

"""
content_security_policy = create_content_security_policy(
    script=True, connect=True, style=True, img=True
)

add_html_file_route(
    "ap/signin",
    resource_filename(__name__, "/resources/index.html"),
    content_security_policy,
)

from starlette.middleware.authentication import AuthenticationMiddleware
context.add_middleware(AuthenticationMiddleware, backend=SessionAuthenticationBackend())
"""
