import logging
from collections.abc import Awaitable, Callable
from typing import Generic, TypeVar

logger = logging.getLogger(__name__)

TContext = TypeVar("TContext")
Callback = Callable[[TContext], Awaitable[None]]


class Tasks(Generic[TContext]):
    def __init__(self, context: TContext) -> None:
        self.context = context
        self.startup_tasks: list[Callback] = []
        self.shutdown_tasks: list[Callback] = []

    async def __aenter__(self) -> None:
        for startup in self.startup_tasks:
            await startup(self.context)

    async def __aexit__(self, *exc_info: object) -> None:
        for shutdown in self.shutdown_tasks:
            try:
                await shutdown(self.context)
            except Exception:
                logger.exception("shutdown")

    def on_startup(self, callback: Callback) -> None:
        self.startup_tasks.append(callback)

    def on_shutdown(self, callback: Callback) -> None:
        self.shutdown_tasks.append(callback)
