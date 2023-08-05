import logging
from collections.abc import Mapping
from datetime import datetime, timedelta, timezone
from secrets import token_hex
from typing import Any, NamedTuple, Optional

from ruteni.apis.users import UserInfo, get_user_by_id, users
from ruteni.config import config
from ruteni.plugins.groups import get_user_groups
from ruteni.plugins.sqlalchemy import metadata
from ruteni.services.database import database
from ruteni.services.keys import key_service

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, and_, func
from sqlalchemy.sql import select

logger = logging.getLogger(__name__)

REFRESH_TOKEN_LENGTH: int = config.get(
    "RUTENI_REFRESH_TOKEN_LENGTH", cast=int, default=32
)
MAX_CLIENT_ID_LENGTH: int = config.get(
    "RUTENI_MAX_CLIENT_ID_LENGTH", cast=int, default=255
)
REFRESH_TOKEN_EXPIRATION: int = config.get(
    "RUTENI_REFRESH_TOKEN_EXPIRATION", cast=int, default=14 * 24 * 60 * 60  # 14 days
)
ACCESS_TOKEN_EXPIRATION: int = config.get(
    "RUTENI_ACCESS_TOKEN_EXPIRATION", cast=int, default=60 * 60  # 1 hour
)

refresh_tokens = Table(
    "refresh_tokens",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(users.c.id), nullable=False),
    Column("token", String(2 * REFRESH_TOKEN_LENGTH), unique=True, nullable=False),
    Column("client_id", String(MAX_CLIENT_ID_LENGTH), nullable=False),
    Column("issued_at", DateTime, nullable=False),
    Column("expires_at", DateTime, nullable=False),
    Column("revoked_at", DateTime, default=None),
)

access_tokens = Table(
    "access_tokens",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "refresh_token_id", Integer, ForeignKey(refresh_tokens.c.id), nullable=False
    ),
    Column("issued_at", DateTime, nullable=False),
    Column("expires_at", DateTime, nullable=False),
)


def now() -> datetime:
    "Have only one way to reference now. Also useful for unittest mock."
    return datetime.now(timezone.utc).astimezone()


def new_refresh_token() -> str:
    # TODO: though very unlikely, check that the generated token is not in the table
    return token_hex(REFRESH_TOKEN_LENGTH)


class AccessToken(NamedTuple):
    token: str
    claims: dict
    expires_at: datetime


async def create_access_claims(
    refresh_token_id: int,
    refresh_token_expires_at: datetime,
    access_token_id: int,
    issuer: str,
    issued_at: datetime,
    expires_at: datetime,
    user_id: int,
    client_id: str,
) -> tuple[UserInfo, dict]:
    user_info = await get_user_by_id(user_id)
    assert user_info
    scopes = await get_user_groups(user_id)
    return user_info, dict(
        sub=str(user_id),
        jti=str(access_token_id),
        iat=int(issued_at.timestamp()),
        exp=int(expires_at.timestamp()),
        rte=int(refresh_token_expires_at.timestamp()),
        orig_iat=0,  # TODO: https://stackoverflow.com/questions/50258431/
        iss=issuer,
        email=user_info.email,
        display_name=user_info.display_name,
        scope=scopes,
        client_id=client_id,
    )


# TODO: `keys` is a service; should this plugin be a service too?


async def create_access_token(
    refresh_token_id: int,
    refresh_token_expires_at: datetime,
    user_id: int,
    issuer: str,
    client_id: str,
) -> tuple[UserInfo, AccessToken]:
    issued_at = now()
    expires_at = issued_at + timedelta(seconds=ACCESS_TOKEN_EXPIRATION)
    access_token_id = await database.execute(
        access_tokens.insert().values(
            refresh_token_id=refresh_token_id,
            issued_at=issued_at,
            expires_at=expires_at,
        )
    )
    user, claims = await create_access_claims(
        refresh_token_id,
        refresh_token_expires_at,
        access_token_id,
        issuer,
        issued_at,
        expires_at,
        user_id,
        client_id,
    )
    token = key_service.create_token(claims)

    return user, AccessToken(token, claims, expires_at)


async def create_refresh_token(
    user_id: int, issuer: str, client_id: str
) -> tuple[UserInfo, AccessToken, str]:
    issued_at = now()
    expires_at = issued_at + timedelta(seconds=REFRESH_TOKEN_EXPIRATION)
    refresh_token = new_refresh_token()
    refresh_token_id = await database.execute(
        refresh_tokens.insert().values(
            token=refresh_token,
            issued_at=issued_at,
            expires_at=expires_at,
            user_id=user_id,
            client_id=client_id,
        )
    )
    user, access_token = await create_access_token(
        refresh_token_id, expires_at, user_id, issuer, client_id
    )

    return user, access_token, refresh_token


async def revoke_refresh_token(user_id: int, refresh_token: str) -> bool:
    rowcount = await database.execute(
        refresh_tokens.update()
        .where(
            and_(
                refresh_tokens.c.token == refresh_token,
                refresh_tokens.c.user_id == user_id,
                refresh_tokens.c.revoked_at.is_(None),
            )
        )
        .values(revoked_at=func.now())
    )
    return rowcount > 0


async def select_refresh_token(refresh_token: str) -> Optional[Mapping[Any, Any]]:
    return await database.fetch_one(
        select([refresh_tokens])
        .select_from(users.join(refresh_tokens))
        .where(refresh_tokens.c.token == refresh_token)
    )


def get_user_id_from_access_token(access_token: str, issuer: str) -> int:
    claims = key_service.get_claims(access_token, issuer)
    return int(claims["sub"])
