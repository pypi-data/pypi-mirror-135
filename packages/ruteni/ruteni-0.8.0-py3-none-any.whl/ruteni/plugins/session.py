import binascii
import json
import logging
from base64 import b64decode, b64encode
from http.cookies import Morsel, SimpleCookie
from typing import Any, Optional

import itsdangerous
from asgiref.typing import WWWScope
from itsdangerous.exc import BadTimeSignature, SignatureExpired
from ruteni.config import config

logger = logging.getLogger(__name__)

USER_SESSION_PATH: str = config.get("RUTENI_USER_SESSION_PATH", default="/")
USER_SESSION_NAME: str = config.get("RUTENI_USER_SESSION_NAME", default="user")
MAX_AGE: int = config.get("RUTENI_SESSION_MAX_AGE", cast=int, default=2 * 7 * 24 * 3600)
COOKIE_NAME: str = config.get("RUTENI_SESSION_COOKIE_NAME", default="session")
SAME_SITE: str = config.get("RUTENI_SESSION_SAME_SITE", default="lax")
SECRET_KEY: str = config.get("RUTENI_SESSION_SECRET_KEY")

signer = itsdangerous.TimestampSigner(SECRET_KEY)

User = dict[str, Any]


def session_header_value(user: Optional[User]) -> Morsel:
    morsel: Morsel = Morsel()
    morsel["path"] = USER_SESSION_PATH
    if user is not None:
        value = signer.sign(b64encode(json.dumps(dict(user=user)).encode())).decode()
        morsel.set(COOKIE_NAME, value, value)
        # expires, comment, domain, version
        morsel["httponly"] = True
        morsel["max-age"] = MAX_AGE
        morsel["samesite"] = SAME_SITE
        morsel["secure"] = not config.is_devel
    else:
        morsel.set(COOKIE_NAME, "", "")
        morsel["max-age"] = 0
    return morsel


def get_user_from_session(value: str, max_age: int = MAX_AGE) -> Optional[User]:
    try:
        data = signer.unsign(value, max_age=max_age)
    except (BadTimeSignature, SignatureExpired):
        return None

    try:
        decoded = b64decode(data)
    except binascii.Error:
        return None

    try:
        session = json.loads(decoded)
    except json.decoder.JSONDecodeError:
        return None

    return session.get(USER_SESSION_NAME, None)


def get_user_from_cookie(value: str) -> Optional[User]:
    cookie: SimpleCookie = SimpleCookie(value)
    return (
        get_user_from_session(cookie[COOKIE_NAME].value)
        if COOKIE_NAME in cookie
        else None
    )


def get_user(scope: WWWScope) -> Optional[User]:
    for key, val in scope["headers"]:
        if key == b"cookie":
            return get_user_from_cookie(val.decode("latin-1"))
    return None


def get_user_from_environ(environ: dict[str, str]) -> Optional[User]:
    return (
        get_user_from_cookie(environ["HTTP_COOKIE"])
        if "HTTP_COOKIE" in environ
        else None
    )
