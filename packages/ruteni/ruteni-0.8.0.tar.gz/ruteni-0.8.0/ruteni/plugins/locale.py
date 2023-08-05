import logging

from ruteni.plugins.sqlalchemy import metadata

from sqlalchemy import (
    Column,
    DateTime,
    Index,
    Integer,
    String,
    Table,
    event,
    func,
    text,
)
from sqlalchemy.engine.base import Connection

logger = logging.getLogger(__name__)

locales = Table(
    "locales",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("code", String(28), nullable=False),
    Column("added_at", DateTime, nullable=False, server_default=func.now()),
    Column("disabled_at", DateTime, default=None),
)

Index(
    "ix_locales_code_not_disabled",
    locales.c.code,
    unique=True,
    sqlite_where=locales.c.disabled_at.is_(None),
    postgresql_where=locales.c.disabled_at.is_(None),
)


def after_create(target: Table, connection: Connection, **kwargs):  # type: ignore
    connection.execute(
        text("INSERT INTO %s (code) VALUES ('en-US'), ('fr-FR')" % target.name)
    )


event.listen(locales, "after_create", after_create)

# import pycountry
# for lang in pycountry.languages:
#     if hasattr(lang, 'iso639_1_code'):
#         print(lang.iso639_1_code)
#     print(lang)
