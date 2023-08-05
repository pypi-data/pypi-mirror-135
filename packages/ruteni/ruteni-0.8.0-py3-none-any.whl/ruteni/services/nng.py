import logging
from abc import ABC, abstractmethod
from asyncio import CancelledError, Task, create_task
from collections.abc import AsyncGenerator
from typing import Optional

from pynng import Respondent0, Surveyor0, Timeout
from ruteni.config import config
from ruteni.services import Service
from starlette.datastructures import State

logger = logging.getLogger(__name__)

SURVEY_TIME: int = config.get("RUTENI_NNG_SURVEY_TIME", cast=int, default=500)
SURVEY_ADDRESS: str = config.get(
    "RUTENI_NNG_SURVEY_ADDRESS", default="tcp://127.0.0.1:13131"
)


class Handler(ABC):
    @abstractmethod
    def handles(self, message: bytes) -> Optional[bytes]:
        ...


class NNGService(Service):
    def __init__(self) -> None:
        Service.__init__(self, "nng", 1)
        self.responder_task: Optional[Task] = None
        self.handlers: list[Handler] = []

    async def listen_surveys(self) -> None:
        try:
            with Respondent0(dial=SURVEY_ADDRESS) as responder:
                while True:
                    message = await responder.arecv()
                    for handler in self.handlers:
                        response = handler.handles(message)
                        if response is not None:
                            await responder.asend(response)
                            break
                    logger.warn(f"unhandled survey {message}")
        except CancelledError:
            pass
        finally:
            self.responder_task = None

    async def survey(
        self, message: bytes = b"ping", survey_time: int = SURVEY_TIME
    ) -> AsyncGenerator[bytes, None]:
        with Surveyor0(listen=SURVEY_ADDRESS) as surveyor:
            surveyor.survey_time = survey_time
            await surveyor.asend(message)
            while True:
                try:
                    response = await surveyor.arecv()
                    yield response
                except Timeout:
                    break

    async def startup(self, state: State) -> None:
        await super().startup(state)
        self.responder_task = create_task(self.listen_surveys())

    async def shutdown(self, state: State) -> None:
        await super().shutdown(state)
        if self.responder_task and not self.responder_task.cancelled():
            self.responder_task.cancel()
            await self.responder_task


nng = NNGService()
