import logging
from typing import Optional

from ruteni.config import config

from socketio import ASGIApp, AsyncRedisManager, AsyncServer

logger = logging.getLogger(__name__)

USE_REDIS: bool = config.get("RUTENI_SOCKETIO_USE_REDIS", cast=bool, default=False)

if USE_REDIS:
    from ruteni.plugins.redis import REDIS_URL  # this will enable redis

    redis_url: Optional[str] = REDIS_URL
else:
    redis_url = None


client_manager = AsyncRedisManager(redis_url) if redis_url else None
sio = AsyncServer(async_mode="asgi", client_manager=client_manager)
app = ASGIApp(sio, socketio_path="/socket.io")  # TODO: fix constant path
