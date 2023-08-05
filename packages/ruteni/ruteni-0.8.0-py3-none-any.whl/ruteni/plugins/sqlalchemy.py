from typing import Literal

from sqlalchemy import MetaData

metadata = MetaData()


async def dump_sql(dialect_name: Literal["sqlite", "mysql", "postgresql"]) -> str:

    import asyncio

    from sqlalchemy import create_engine
    from sqlalchemy.sql.type_api import TypeEngine

    DATABASE_URLS = {
        "sqlite": "sqlite:///::memory::",
        "mysql": "mysql://localhost",
        "postgresql": "postgresql://localhost",
    }
    DATABASE_URL = DATABASE_URLS[dialect_name]

    loop = asyncio.get_running_loop()
    fut = loop.create_future()

    def executor(sql: TypeEngine) -> None:
        fut.set_result(sql.compile(dialect=engine.dialect))

    engine = create_engine(DATABASE_URL, strategy="mock", executor=executor)
    metadata.create_all(engine)

    await fut
    return fut.result()
