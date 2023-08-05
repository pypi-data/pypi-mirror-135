import logging
from asyncio import CancelledError, Task, create_task, sleep
from typing import Optional
from urllib.parse import quote

from blinker import signal
from pynng.exceptions import NNGException
from ruteni.config import config
from ruteni.services import Service, ServiceSpec
from ruteni.services.nng import Handler, nng
from starlette.datastructures import State

logger = logging.getLogger(__name__)


SEPARATOR: str = config.get("RUTENI_SERVICES_SEPARATOR", default=",")
SLEEP_TIME: int = config.get("RUTENI_SERVICES_SLEEP_TIME", cast=int, default=10)

# https://dzone.com/articles/monitoring-microservices-with-health-checks
# https://stackoverflow.com/questions/55784790/
# https://everttimberg.io/blog/python-circuit-breaker/


class HealthCheckService(Service, Handler):
    def __init__(self) -> None:
        Service.__init__(self, "health-check", 1)
        self.missing_signal = signal(f"{self.name}:missing-services")
        self.check_task: Optional[Task] = None

    def handles(self, message: bytes) -> Optional[bytes]:
        if message != b"services":
            return None
        names = []
        for service in Service.started_services:
            names.append(quote(service.name))
        return SEPARATOR.join(names).encode()

    async def check_services(self) -> None:
        try:
            while True:
                await sleep(SLEEP_TIME)  # TODO: use scheduler
                remote_services: dict[str, int] = {}
                # print(remote_services)
                try:
                    async for message in nng.survey(b"services"):
                        names = message.decode().split(SEPARATOR)
                        for name in names:
                            if name in remote_services:
                                remote_services[name] += 1
                            else:
                                remote_services[name] = 1
                except NNGException:
                    logger.exception("nng")
                else:
                    local_specs: set[ServiceSpec] = set(
                        (service.name, service.version)
                        for service in Service.started_services
                    )
                    # TODO: check version
                    missing_services: set[str] = set(
                        spec[0]
                        for spec in Service.get_required_services().keys()
                        if (
                            spec[0] not in local_specs
                            and spec[0] not in remote_services
                        )
                    )
                    if len(missing_services):
                        logger.warn(f"missing services: {missing_services}")
                        self.missing_signal.send(self, names=missing_services)
        except CancelledError:
            pass
        finally:
            self.check_task = None

    async def startup(self, state: State) -> None:
        await super().startup(state)
        self.check_task = create_task(self.check_services())

    async def shutdown(self, state: State) -> None:
        await super().shutdown(state)
        if self.check_task and not self.check_task.cancelled():
            self.check_task.cancel()
            await self.check_task


health_check = HealthCheckService()
