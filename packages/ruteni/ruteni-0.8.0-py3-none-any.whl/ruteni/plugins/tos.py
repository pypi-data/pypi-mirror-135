from ruteni.plugins.sqlalchemy import metadata

from sqlalchemy import Column, DateTime, Integer, Table, event, func, text
from sqlalchemy.engine.base import Connection

tos = Table(
    "tos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("date", DateTime, nullable=False, server_default=func.now()),
)


def after_create(target: Table, connection: Connection, **kwargs):  # type: ignore
    connection.execute(text("INSERT INTO %s DEFAULT VALUES" % target.name))


event.listen(tos, "after_create", after_create)


# from ruteni.plugins.tos import tos
# tos = Integer(required=True, validate=validate.Range(min=0))
# current_tos = await database.fetch_val(select(func.max(tos.c.id)))
# if current_tos != signin["tos"]:
#    raise HTTPException(status_code=status.HTTP_401HTTP_401__UNAUTHORIZED)
