import logging
from typing import NamedTuple, Optional

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from ruteni.apis.users import add_user, users
from ruteni.config import config
from ruteni.plugins.sqlalchemy import metadata
from ruteni.services.database import database

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    and_,
    func,
)
from sqlalchemy.sql import select

logger = logging.getLogger(__name__)

PASSWORD_MAX_LENGTH: int = config.get(
    "RUTENI_PASSWORD_MAX_LENGTH", cast=int, default=40
)

passwords = Table(
    "passwords",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(users.c.id), nullable=False),
    Column("hashed_password", String, nullable=False),  # TODO: length as pref?
    Column("added_at", DateTime, nullable=False, server_default=func.now()),
    Column("disabled_at", DateTime, default=None),
)


Index(
    "ix_passwords_user_id_not_disabled",
    passwords.c.user_id,
    unique=True,
    sqlite_where=passwords.c.disabled_at.is_(None),
    postgresql_where=passwords.c.disabled_at.is_(None),
)


ph = PasswordHasher()


class Credential(NamedTuple):
    user_id: int
    hashed_password: str


async def get_credential(email: str) -> Optional[Credential]:
    row = await database.fetch_one(
        select([users.c.id, passwords.c.hashed_password])
        .select_from(users.join(passwords))
        .where(
            and_(
                users.c.email == email,
                users.c.disabled_at.is_(None),
                passwords.c.disabled_at.is_(None),
            )
        )
    )
    return Credential(row["id"], row["hashed_password"]) if row else None


async def check_password(email: str, password: str) -> Optional[Credential]:
    credential = await get_credential(email)
    if credential is None:
        return None
    logger.debug("signin:", email, password, "~", credential.hashed_password)
    try:
        if ph.verify(credential.hashed_password, password):
            return credential
    except VerifyMismatchError:
        pass
    return None


async def add_password(user_id: int, password: str) -> int:
    return await database.execute(
        passwords.insert().values(user_id=user_id, hashed_password=ph.hash(password))
    )


async def register_user(
    display_name: str, email: str, locale: str, password: str
) -> tuple[int, int]:
    user_info = await add_user(display_name, email, locale)
    password_id = await add_password(user_info.id, password)
    return user_info.id, password_id
