import logging

from databases import Database, DatabaseURL
from ruteni.config import config
from ruteni.plugins.sqlalchemy import metadata
from ruteni.services import Service
from starlette.datastructures import State

logger = logging.getLogger(__name__)


DATABASE_URL: DatabaseURL = config.get("RUTENI_DATABASE_URL", cast=DatabaseURL)


class DatabaseService(Database, Service):
    def __init__(self, database_url: DatabaseURL) -> None:
        Database.__init__(self, database_url)
        Service.__init__(self, "database", 1)

    async def startup(self, state: State) -> None:
        await super().startup(state)
        if config.is_devel:
            from sqlalchemy import create_engine

            engine = create_engine(str(DATABASE_URL))
            # if engine.dialect.name == "sqlite":
            metadata.create_all(engine)

        await self.connect()

    async def shutdown(self, state: State) -> None:
        await super().shutdown(state)
        await self.disconnect()


database = DatabaseService(DATABASE_URL)
