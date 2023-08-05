from asyncio import Event, create_task
from typing import Optional

from ruteni.app import Ruteni
from uvicorn import Config, Server


class UvicornTestServer(Server):
    def __init__(
        self, ruteni: Ruteni, host: str = "127.0.0.1", port: int = 8000
    ) -> None:
        self._startup_done = Event()
        super().__init__(config=Config(ruteni, host=host, port=port, log_level="error"))

    async def startup(self, sockets: Optional[list] = None) -> None:
        await super().startup(sockets=sockets)
        self.config.setup_event_loop()
        self._startup_done.set()

    async def up(self) -> None:
        self._serve_task = create_task(self.serve())
        await self._startup_done.wait()

    async def down(self) -> None:
        self.should_exit = True
        await self._serve_task
