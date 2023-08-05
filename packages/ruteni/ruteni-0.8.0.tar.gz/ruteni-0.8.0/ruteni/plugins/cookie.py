from typing import Optional

from ruteni.config import config
from starlette.responses import Response

COOKIE_SECURE: bool = config.get(
    "RUTENI_COOKIE_SECURE", cast=bool, default=(not config.is_devel)
)
COOKIE_HTTPONLY: bool = config.get("RUTENI_COOKIE_HTTPONLY", cast=bool, default=True)
COOKIE_PATH: str = config.get("RUTENI_COOKIE_PATH", default="/")
COOKIE_DOMAIN: Optional[str] = config.get("RUTENI_COOKIE_DOMAIN", default=None)
COOKIE_SAMESITE: str = config.get("RUTENI_COOKIE_SAMESITE", default="lax")


def set_cookie(response: Response, name: str, value: str) -> None:
    response.set_cookie(
        name,
        value,
        path=COOKIE_PATH,
        domain=COOKIE_DOMAIN,
        secure=COOKIE_SECURE,
        httponly=COOKIE_HTTPONLY,
        samesite=COOKIE_SAMESITE,
    )
