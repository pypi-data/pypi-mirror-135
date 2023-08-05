import traceback
from typing import AsyncContextManager, Optional

from asgiref.typing import (
    LifespanScope,
    LifespanShutdownCompleteEvent,
    LifespanShutdownEvent,
    LifespanShutdownFailedEvent,
    LifespanStartupCompleteEvent,
    LifespanStartupEvent,
    LifespanStartupFailedEvent,
)

from .types import LifespanReceive, LifespanSend


class Lifespan:
    """A generic ASGI-lifespan manager."""

    def __init__(self, context_manager: AsyncContextManager) -> None:
        self.context_manager = context_manager
        self.started: Optional[bool] = None

    async def __call__(
        self, scope: LifespanScope, receive: LifespanReceive, send: LifespanSend
    ) -> None:
        assert self.started is None
        self.started = False
        event = await receive()
        assert event == LifespanStartupEvent({"type": "lifespan.startup"})
        try:
            async with self.context_manager:
                await send(
                    LifespanStartupCompleteEvent({"type": "lifespan.startup.complete"})
                )
                self.started = True
                event = await receive()  # TODO: asyncio.exceptions.CancelledError
                assert event == LifespanShutdownEvent({"type": "lifespan.shutdown"})
        except BaseException:
            message = traceback.format_exc()
            if self.started:
                await send(
                    LifespanShutdownFailedEvent(
                        {"type": "lifespan.shutdown.failed", "message": message}
                    )
                )
            else:
                await send(
                    LifespanStartupFailedEvent(
                        {"type": "lifespan.startup.failed", "message": message}
                    )
                )
            raise
        else:
            await send(
                LifespanShutdownCompleteEvent({"type": "lifespan.shutdown.complete"})
            )
