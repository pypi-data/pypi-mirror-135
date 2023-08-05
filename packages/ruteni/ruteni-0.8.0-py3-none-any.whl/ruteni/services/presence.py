import logging

from ruteni.apis.users import users
from ruteni.config import config
from ruteni.plugins.session import get_user_from_environ
from ruteni.plugins.socketio import sio
from ruteni.plugins.sqlalchemy import metadata
from ruteni.services import Service
from ruteni.services.database import database
from ruteni.services.keys import key_service
from socketio import AsyncNamespace
from socketio.exceptions import ConnectionRefusedError
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, and_, func
from sqlalchemy_utils import IPAddressType
from starlette.datastructures import State

logger = logging.getLogger(__name__)

NAMESPACE = config.get("RUTENI_PRESENCE_NAMESPACE", default="/ruteni/presence")

connections = Table(
    "connections",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("sid", String(28), nullable=False),
    Column("ip_address", IPAddressType, nullable=False),
    Column("user_id", Integer, ForeignKey(users.c.id), nullable=False),
    Column("opened_at", DateTime, nullable=False, server_default=func.now()),
    Column("closed_at", DateTime, default=None),
)


class PresenceNamespace(AsyncNamespace):
    async def on_connect(self, sid: str, environ: dict[str, str]) -> bool:
        # async with sio.eio.session(sid) as session:
        #     session["username"] = username

        # get the current user
        user = get_user_from_environ(environ)
        if user is None:
            raise ConnectionRefusedError("not authenticated")

        connection_id = await database.execute(
            connections.insert().values(
                sid=sid, user_id=user["id"], ip_address=environ["REMOTE_ADDR"]
            )
        )
        token = key_service.encrypt(str(connection_id))
        await self.emit("token", token)
        logger.info(f"{user['name']} is connected")
        return True

    async def on_disconnect(self, sid: str) -> None:
        # TODO: could there be identical sids for different connections over time?
        await database.execute(
            connections.update()
            .where(and_(connections.c.sid == sid, connections.c.closed_at.is_(None)))
            .values(closed_at=func.now())
        )
        logger.info(f"{sid}.disconnect")


class PresenceService(Service):
    def __init__(self) -> None:
        Service.__init__(self, "presence", 1, {key_service})

    async def startup(self, state: State) -> None:
        await super().startup(state)
        sio.register_namespace(PresenceNamespace(NAMESPACE))

    async def shutdown(self, state: State) -> None:
        await super().shutdown(state)
        # TODO: unregister


presence = PresenceService()
