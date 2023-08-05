from __future__ import annotations

import asyncio
import logging
from collections.abc import Mapping
from typing import Optional, Union

from pkg_resources import iter_entry_points
from starlette.datastructures import State
from toposort import toposort

logger = logging.getLogger(__name__)

# https://mode.readthedocs.io/en/latest/userguide/services.html

ServiceSpec = tuple[str, int]


class Service:
    available_services: set[Service] = set()  # WeakSet[Service] = WeakSet()
    enabled_services: set[Service] = set()  # WeakSet[Service] = WeakSet()
    started_services: list[Service] = []

    def __init__(
        self,
        name: str,
        version: int,
        requires: Optional[set[Union[Service, ServiceSpec]]] = None,
    ) -> None:
        self.name = name
        self.version = version
        self.requires = requires or set()
        Service.available_services.add(self)

    def add_requirement(self, name: str, version: int) -> None:
        self.requires.add((name, version))

    @property
    def spec(self) -> ServiceSpec:
        return self.name, self.version

    @property
    def full_name(self) -> str:
        return f"{self.name} v{self.version}"

    @property
    def started(self) -> bool:
        return self in Service.started_services

    async def startup(self, state: State) -> None:
        # self.emit("startup")
        Service.started_services.append(self)  # TODO: wrong if fails in subclass
        logger.info(f"{self.full_name}: started")

    async def shutdown(self, state: State) -> None:
        Service.started_services.remove(self)
        # self.emit("shutdown")
        logger.info(f"{self.full_name}: stopped")

    @classmethod
    def enable(cls, service: Service) -> None:
        cls.enabled_services.add(service)

    @classmethod
    def load_entry_points(cls, names: set[str]) -> None:
        entry_points = {
            f"{entry_point.dist.key}:{entry_point.name}": entry_point
            for entry_point in iter_entry_points("ruteni.service.v1")
            if entry_point.dist
        }
        for name in names:
            if name not in entry_points:
                logger.error(f'unknown service "${name}"')
                continue
            entry_point = entry_points[name]
            # entry_point.dist.version
            service = entry_point.load()
            cls.enable(service)

    @classmethod
    async def start_services(cls, state: State) -> None:
        services: set[Service] = set()
        queue: set[Service] = set(cls.enabled_services)
        dependencies: dict[Service, set[Service]] = {}
        while len(queue):
            service = queue.pop()
            services.add(service)
            dependencies[service] = {
                other for other in service.requires if isinstance(other, Service)
            }
            queue.update(
                other for other in dependencies[service] if other not in services
            )

        # find batches of services that can be started in parallel
        for batch in toposort(dependencies):
            logger.debug("service startup batch:", batch)
            tasks = tuple(service.startup(state) for service in batch)
            await asyncio.gather(*tasks)  # TODO: use anyio task group

        missing = tuple(
            service.spec
            for service in cls.enabled_services
            if service not in cls.started_services
        )
        assert (
            len(missing) == 0
        ), f"some services failed to register at startup: {missing}"

    @classmethod
    async def stop_services(cls, state: State) -> None:
        for service in tuple(cls.started_services):
            try:
                await service.shutdown(state)
            except Exception:
                logger.exception("stop")

    @classmethod
    def get_required_services(cls) -> Mapping[ServiceSpec, set[Service]]:
        required_services: dict[ServiceSpec, set[Service]] = {}
        for service in cls.started_services:
            for require in service.requires:
                if isinstance(require, tuple):
                    if require in required_services:
                        required_services[require].add(service)
                    else:
                        required_services[require] = {service}
        logger.debug(f"required services: ${required_services}")
        return required_services


ServiceSet = set[Union[Service, ServiceSpec]]
