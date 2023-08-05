import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ruteni.config import config
from ruteni.services import Service
from starlette.datastructures import State

logger = logging.getLogger(__name__)

SCHEDULER_WAIT: bool = config.get("RUTENI_SCHEDULER_WAIT", cast=bool, default=False)


class SchedulerService(Service):
    def __init__(self) -> None:
        Service.__init__(self, "scheduler", 1)
        self._scheduler = AsyncIOScheduler()

    async def startup(self, state: State) -> None:
        await Service.startup(self, state)
        self._scheduler.start(self)

    async def shutdown(self, state: State) -> None:
        await Service.shutdown(self, state)
        self._scheduler.shutdown(wait=SCHEDULER_WAIT)


scheduler = SchedulerService()
